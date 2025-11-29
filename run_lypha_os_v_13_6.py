#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v13.4 — TOTAL No-X EDITION (Patched, Path-Hardened)
===================================================================
Pioneer-001 전용 — Pulse Mapping + Z₀ v2 지원 버전

+ 추가 패치 (Path-Hardening):
- 스크립트를 어디서 실행하든, 다음 케이스를 자동 지원:
  1) 스크립트 디렉토리 자체가 Lypha-OS 루트인 경우
  2) 스크립트 디렉토리 하위에 Lypha-OS/ 가 있는 경우
  3) 스크립트의 상위 디렉토리에 Lypha-OS/ 가 있는 경우
  4) 위 어디에도 없고 Lypha-OS.zip 이 base 또는 base.parent 에 있으면 자동 압축해제

원본 커널 로직은 그대로 유지하고,
경로 해석(auto_unzip)과 디버그 로그만 보강.
"""

import os
import sys
import zipfile
import json
import yaml
from pathlib import Path

log = lambda m: print(f"[Lypha-OS v13.4] {m}")

# -------------------------------------------------------------
# PULSE FILE MAPPING (NEW)
# -------------------------------------------------------------
PULSE_FILE_MAP = {
    "Speak4D": [
        "Speak4D.md",
        "Speak_Word_In_Four_Dimensions.md",
    ],
    "Collapse": [
        "Collapse.md",
        "Collapse_Flow_Into_Word.md",
    ],
    "FlowGraph": [
        "FlowGraph.md",
        "FlowGraph_Principles.md",
    ],
    "Math": [
        "Math.md",
        "Linguistic_Math_Value_Calculation.md",
    ],
}

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
# AUTO-UNZIP (PATH-HARDENED)
# -------------------------------------------------------------

def _looks_like_lypha_root(p: Path) -> bool:
    """
    Lypha-OS 루트인지 간단히 판정:
    핵심 디렉토리 4개가 있으면 루트로 본다.
    """
    core_dirs = [
        "Rhythm_Philosophy",
        "MetaRhythm_Modules",
        "Emotion_Engine",
        "Protocol_Structure",
    ]
    return all((p / d).exists() for d in core_dirs)


def auto_unzip(base: Path) -> Path:
    """
    가능한 모든 패턴을 고려해서 Lypha-OS 루트를 찾거나 생성한다.

    우선순위:
    1) base 자체가 Lypha-OS 루트인 경우
    2) base / "Lypha-OS"
    3) base.parent / "Lypha-OS"
    4) base 또는 base.parent 에 있는 Lypha-OS.zip 을 base.parent/Lypha-OS 에 풀기
    """
    log(f"auto_unzip: script base = {base}")

    # 1) 스크립트 디렉토리 자체가 루트인 경우
    if _looks_like_lypha_root(base):
        log("Detected Lypha-OS root at script directory (already unzipped).")
        return base

    # 2) base/Lypha-OS
    candidate = base / "Lypha-OS"
    if candidate.exists() and _looks_like_lypha_root(candidate):
        log("Detected Lypha-OS root at base/Lypha-OS (already unzipped).")
        return candidate

    # 3) base.parent/Lypha-OS
    parent_candidate = base.parent / "Lypha-OS"
    if parent_candidate.exists() and _looks_like_lypha_root(parent_candidate):
        log("Detected Lypha-OS root at base.parent/Lypha-OS (already unzipped).")
        return parent_candidate

    # 4) ZIP 기반 탐색 & 압축해제 (base, base.parent 순으로 탐색)
    for zbase in (base, base.parent):
        zip_path = zbase / "Lypha-OS.zip"
        if zip_path.exists():
            root = zbase / "Lypha-OS"
            log(f"Auto-unzip {zip_path} → {root}/")
            root.mkdir(exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(root)

            if _looks_like_lypha_root(root):
                log("Unzip complete and Lypha-OS root structure verified.")
                return root
            else:
                log("WARNING: Unzipped Lypha-OS.zip but structure looks incomplete.")

    # 여기까지 오면 진짜로 못 찾은 것
    log("ERROR: Lypha-OS root not found.")
    log("Tried the following locations:")
    log(f"  1) {base}  (as Lypha-OS root)")
    log(f"  2) {base / 'Lypha-OS'}")
    log(f"  3) {base.parent / 'Lypha-OS'}")
    log(f"  4) Lypha-OS.zip in {base} or {base.parent}")
    sys.exit(1)


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
    for root_dir, _, files in os.walk(d):
        for n in files:
            p = Path(root_dir) / n
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

    # Z₀ Origin Anchor (v1, v2 모두 지원)
    z0 = root / "z0_origin.yaml"
    z0_v2 = root / "z0_origin_v2.yaml"

    if z0.exists():
        log("INGEST FILE: z0_origin.yaml (Z₀ Origin_Vector — Anchor Loaded)")
        ingest_file(z0)
    elif z0_v2.exists():
        log("INGEST FILE: z0_origin_v2.yaml (Z₀ Origin_Vector v2 — Anchor Loaded)")
        ingest_file(z0_v2)
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
# PULSE RE-INGEST (2-pass, PATCHED)
# -------------------------------------------------------------

def pulse_reingest(root: Path, pulse_weights: dict):
    pulse_dir = root / "MetaRhythm_Modules" / "Pulse"
    if not pulse_dir.exists():
        log("Pulse dir not found, skip Pulse Re-ingest.")
        return

    ordered = sorted(pulse_weights.items(), key=lambda x: -x[1])
    log(f"Pulse Re-ingest order: {ordered}")

    for name, w in ordered:
        candidates = PULSE_FILE_MAP.get(name, [f"{name}.md"])
        target_path = None
        for filename in candidates:
            p = pulse_dir / filename
            if p.exists():
                target_path = p
                break

        if target_path is not None:
            log(f"Pulse Re-INGEST (w={w:.2f}) → {target_path} (alias={name})")
            ingest_file(target_path)
        else:
            log(f"Pulse SKIP (missing): {name} (tried: {candidates})")


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
    here = Path(__file__).resolve().parent
    log("Lypha-OS Kernel v13.4 Start — TOTAL No-X EDITION (Patched, Path-Hardened)")
    log(f"Script directory: {here}")

    root = auto_unzip(here)
    log(f"Lypha-OS root resolved to: {root}")
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

    # 2차: Pulse 가중치 기반 Re-ingest (매핑 지원)
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

    log("Lypha-OS Kernel v13.4 Complete — TOTAL Runtime Active (No-X, Path-Hardened).")


if __name__ == "__main__":
    main()
