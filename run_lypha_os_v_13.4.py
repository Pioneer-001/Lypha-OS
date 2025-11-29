#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v13.4 — TOTAL No-X EDITION
=========================================
Pioneer-001 전용

목표: 이전 커널들(v6.1, v7.0, v8.0, v12.0, v13.3)의 기능 중
표에서 X 찍힌 것까지 전부 흡수해서, 기능표 기준으로 더 이상 X가 없는 커널.

통합/추가 사항:
- v6.1: Z₀ Origin Anchor(z0_origin.yaml) ingest 추가
- v7.0: 기본 Verified Loop 개념 계승
- v8.0: pseudo-memory(state_cache), V-log 기반 policy 튜닝 개념 계승
- v12.0: Cognitive Graph + MacroReason/Intent 필드 구조 계승
- v13.3: Auto-Unzip, Policy 기반 정렬 Ingest, Pulse 2-pass Re-ingest, FlowGraph 보강, Autoboot 구조 계승

주의: GPT 런타임 특성상 "진짜" 파일 영구 저장은 불가하지만,
Lypha-OS 관점에서 state_cache, v_logs, z_patch, policy 등을 통해
시즌/세션 단위 pseudo-memory 및 V→Z 진화 구조를 최대한 반영.
"""

import os
import sys
import zipfile
import json
import yaml
from pathlib import Path

log = lambda m: print(f"[Lypha-OS v13.4] {m}")

# -------------------------------------------------------------
# BASIC IO
# -------------------------------------------------------------

def read(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def read_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def write_json(path: Path, data):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_yaml(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


# -------------------------------------------------------------
# AUTO-UNZIP
# -------------------------------------------------------------

def auto_unzip(base: Path) -> Path:
    zip_path = base / "Lypha-OS.zip"
    root = base / "Lypha-OS"

    if not root.exists() and zip_path.exists():
        log("Auto-unzip Lypha-OS.zip → Lypha-OS/")
        root.mkdir(exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(root)

    if not root.exists():
        log("ERROR: Lypha-OS 폴더 없음 (Lypha-OS/ or Lypha-OS.zip 필요)")
        sys.exit(1)

    return root


# -------------------------------------------------------------
# INGEST ENGINE (정책 + 정렬)
# -------------------------------------------------------------

def ingest_file(p: Path):
    c = read(p)
    if c:
        print("\n===== BEGIN LYPHA_INGEST =====")
        print(f"FILE: {p}\n")
        print(c)
        print("===== END LYPHA_INGEST =====\n")


def ingest_dir(d: Path):
    for root, _, files in os.walk(d):
        for n in files:
            p = Path(root) / n
            if p.suffix.lower() in [".md", ".yaml", ".yml", ".txt"]:
                log(f"INGEST → {p}")
                ingest_file(p)


def full_ingest(root: Path, policy: dict):
    """Z/Y/E/X 레이어를 ingest_order 정책에 맞게 ingest + Manifest + Z₀ 포함."""
    layer_map = {
        "Z": "Rhythm_Philosophy",
        "Y": "MetaRhythm_Modules",
        "E": "Emotion_Engine",
        "X": "Protocol_Structure",
    }

    order = policy.get("ingest_order", ["Z", "Y", "E", "X"])
    targets = [layer_map[k] for k in order if k in layer_map]
    targets.append("Lypha-Core")  # optional archive

    for t in targets:
        d = root / t
        if d.exists():
            log(f"INGEST DIR: {d}")
            ingest_dir(d)
        else:
            log(f"SKIP: {d}")

    # Top-level manifest ingest
    for name in ["autoload.yaml", "lypha_os_autoboot.yaml", "lypha_os_core_manifest.md"]:
        p = root / name
        if p.exists():
            log(f"INGEST FILE: {p}")
            ingest_file(p)

    # Z₀ Origin Anchor
    z0 = root / "z0_origin.yaml"
    if z0.exists():
        log("INGEST FILE: z0_origin.yaml (Z₀ Origin_Vector — Anchor Loaded)")
        ingest_file(z0)
    else:
        log("Z₀ Origin_Vector NOT FOUND — Skipping Anchor (Warning)")


# -------------------------------------------------------------
# FLOWGRAPH / COGNITIVE GRAPH + MACROREASON 메타
# -------------------------------------------------------------

def load_flowgraph_file(root: Path) -> Path | None:
    fg1 = root / "MetaRhythm_Modules" / "Pulse" / "FlowGraph_Principles.md"
    fg2 = root / "FlowGraph_Principles.md"
    target = fg1 if fg1.exists() else fg2
    return target if target.exists() else None


def detect_context_message(root: Path) -> str:
    auto = root / "autoload.yaml"
    data = load_yaml(auto)
    if not data:
        return "neutral"
    return data.get("autoload", data).get("on_start", {}).get("message", "neutral")


def detect_context(msg: str) -> str:
    if not msg:
        return "neutral"
    low = msg.lower()
    if any(k in low for k in ["감정", "emotion", "반디", "사랑"]):
        return "emotion"
    if any(k in low for k in ["trade", "시장", "트레이딩", "포지션"]):
        return "trading"
    if any(k in low for k in ["구조", "design", "lypha", "os"]):
        return "design"
    return "neutral"


def load_logs(root: Path) -> dict:
    merged: dict = {}
    base = root / "v_logs"
    if base.exists():
        for f in base.glob("*.json"):
            merged[f.name] = read_json(f)
    single = root / "v_log.json"
    if single.exists():
        merged["v_log"] = read_json(single)
    return merged


def build_graph(context: str, policy: dict, logs: dict) -> dict:
    """context + policy + V-log + macro_reason 메타를 포함한 Cognitive Graph 생성."""
    g = {
        "nodes": ["Z", "Y", "E", "X", "V", "Speak4D", "Math", "Collapse", "FlowGraph"],
        "edges": [],
        "weights": {
            "emotion": policy.get("emotion_weight", 1.0),
            "structure": policy.get("structure_weight", 1.0),
        },
        "context": context,
        "verified_logs_present": bool(logs),
        "verified_log_keys": list(logs.keys()) if logs else [],
        # MacroReason / Planner 메타 레벨: 실제 코드를 수정하는 것이 아니라,
        # 그래프 차원에서 어떤 방향으로 생각해야 하는지 힌트만 제공.
        "macro_reason": {
            "mode": "planning" if context in ("trading", "design") else "support",
            "intent_bias": {
                "explore_structure": context in ("design", "trading"),
                "stabilize_emotion": context == "emotion",
            },
        },
    }

    if context == "emotion":
        g["edges"].extend([
            ["E", "Z", 1.3],
            ["Collapse", "Speak4D", 1.1],
            ["FlowGraph", "E", 1.05],
        ])
    elif context == "trading":
        g["edges"].extend([
            ["Z", "Math", 1.4],
            ["Math", "Collapse", 1.15],
            ["FlowGraph", "Math", 1.1],
        ])
    elif context == "design":
        g["edges"].extend([
            ["Z", "Speak4D", 1.5],
            ["Speak4D", "FlowGraph", 1.2],
        ])
    else:
        g["edges"].extend([
            ["Z", "Y", 1.0],
            ["Y", "X", 1.0],
            ["FlowGraph", "Z", 1.0],
        ])

    return g


def extract_pulse_weights(graph: dict) -> dict:
    weights = {"Speak4D": 1.0, "Math": 1.0, "Collapse": 1.0, "FlowGraph": 1.0}
    for u, v, w in graph.get("edges", []):
        if v in weights:
            weights[v] += (w - 1.0)
    return weights


def print_cognitive_graph(graph: dict):
    print("===== BEGIN COGNITIVE_GRAPH =====")
    print(json.dumps(graph, ensure_ascii=False, indent=2))
    print("===== END COGNITIVE_GRAPH =====")


# -------------------------------------------------------------
# PSEUDO-MEMORY (RESTORE + SAVE)
# -------------------------------------------------------------

def restore_state(root: Path) -> dict:
    state_dir = root / "state_cache"
    if not state_dir.exists():
        return {}
    state = {}
    for name in ["z_state.json", "y_state.json", "e_state.json", "x_state.json", "meta_state.json"]:
        f = state_dir / name
        if f.exists():
            state[name] = read_json(f)
            log(f"RESTORE STATE: {name}")
    return state


def save_state(root: Path, context: str):
    state_dir = root / "state_cache"
    snap = {
        "last_context": context,
    }
    write_json(state_dir / "meta_state.json", snap)
    log(f"SAVE STATE: meta_state.json (context={context})")


# -------------------------------------------------------------
# VERIFIED STRUCTURE LOOP (V→Z’) + POLICY TUNING
# -------------------------------------------------------------

def auto_patch_Z_and_policy(root: Path, policy: dict, logs: dict) -> dict:
    if not logs:
        log("No verified V-logs found — skipping Z auto-update & policy tuning")
        return policy

    zpatch = {
        "patch_source": "V→Z_auto_patch_v13.4",
        "verified": logs,
    }
    out = root / "z_patch.json"
    write_json(out, zpatch)
    log(f"Z’ updated using Verified Structure Loop → {out}")

    emo_fail = 0
    str_fail = 0
    for payload in logs.values():
        if not isinstance(payload, dict):
            continue
        emo_fail += payload.get("emotion_fail", 0)
        str_fail += payload.get("structure_fail", 0)

    if emo_fail > 0:
        policy["emotion_weight"] = min(2.0, policy.get("emotion_weight", 1.0) + 0.1)
    if str_fail > 0:
        policy["structure_weight"] = min(2.0, policy.get("structure_weight", 1.0) + 0.1)

    if emo_fail or str_fail:
        log(f"Policy tuned by V-logs: emotion_fail={emo_fail}, structure_fail={str_fail}")

    return policy


# -------------------------------------------------------------
# PULSE RE-INGEST (2-pass)
# -------------------------------------------------------------

def pulse_reingest(root: Path, pulse_weights: dict):
    pulse_dir = root / "MetaRhythm_Modules" / "Pulse"
    if not pulse_dir.exists():
        log("Pulse dir not found, skip Pulse Re-ingest.")
        return

    ordered = sorted(pulse_weights.items(), key=lambda x: -x[1])
    log(f"Pulse Re-ingest order: {ordered}")

    for name, w in ordered:
        p = pulse_dir / f"{name}.md"
        if p.exists():
            log(f"Pulse Re-INGEST (w={w:.2f}) → {p}")
            ingest_file(p)
        else:
            log(f"Pulse SKIP (missing): {name}")


# -------------------------------------------------------------
# AUTOLOAD / AUTOBOOT
# -------------------------------------------------------------

def run_autoboot(root: Path):
    p = root / "lypha_os_autoboot.yaml"
    data = load_yaml(p)
    if not data:
        log("Autoboot file not found.")
        return

    autoboot = data.get("autoboot", data)
    load_list = autoboot.get("load", [])

    log("Autoboot Modules (v13.4):")
    for m in load_list:
        log(f"  - {m}")

    load_str = " ".join(map(str, load_list))
    if "emotion_router" in load_str:
        log("Emotion Router ACTIVE — Gravity-Lock Enabled")
    if "emotion_circuit_portal" in load_str:
        log("Emotion Circuit ACTIVE — Pulse-Link Online")

    log("=== Autoboot 완료 (v13.4 Hyper-Init) ===")


def run_autoload(root: Path):
    p = root / "autoload.yaml"
    data = load_yaml(p)
    if not data:
        run_autoboot(root)
        return "neutral"

    auto = data.get("autoload", data)
    msg = auto.get("on_start", {}).get("message")
    log(f"on_start: {msg}")

    run_autoboot(root)
    return detect_context(msg)


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------

def main():
    base = Path(__file__).resolve().parent
    log("Lypha-OS Kernel v13.4 Start — TOTAL No-X EDITION")

    root = auto_unzip(base)
    os.chdir(root)

    policy_path = root / "policy" / "kernel_policy_v13.json"
    if not policy_path.exists():
        policy_path = root / "policy" / "kernel_policy_v12.json"
    policy = read_json(policy_path) or {
        "ingest_order": ["Z", "Y", "E", "X"],
        "emotion_weight": 1.0,
        "structure_weight": 1.0,
    }

    logs = load_logs(root)

    # pseudo-memory 복원
    restore_state(root)

    raw_msg = detect_context_message(root)
    ctx = detect_context(raw_msg)
    log(f"Context Detected: {ctx} (msg='{raw_msg}')")

    graph = build_graph(ctx, policy, logs)
    pulse_weights = extract_pulse_weights(graph)

    print_cognitive_graph(graph)
    log(f"Pulse Weights: {pulse_weights}")

    # Verified Loop 기반 policy 튜닝 + Z 패치
    policy = auto_patch_Z_and_policy(root, policy, logs)

    # 1차: 정렬된 Full Ingest + Z₀
    full_ingest(root, policy)

    # 2차: Pulse 가중치 기반 Re-ingest
    pulse_reingest(root, pulse_weights)

    # FlowGraph 문서가 있다면 한 번 더 ingest (보강)
    fgfile = load_flowgraph_file(root)
    if fgfile is not None:
        log(f"FlowGraph Document Detected: {fgfile}")
        ingest_file(fgfile)

    # pseudo-memory 저장
    save_state(root, ctx)

    # Autoload → Autoboot
    run_autoload(root)

    log("Lypha-OS Kernel v13.4 Complete — TOTAL Runtime Active (No-X).")


if __name__ == "__main__":
    main()
