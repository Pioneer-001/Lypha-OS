#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v14.4 — TOTAL No-X EDITION (Z-Core Priority, Path-Hardened, VerifiedLoop Engine)
=============================================================================================== 
Pioneer-001 전용 — Origin Engine + ZYX Priority + Speak4D + Linguistic Math + Verified Structure Loop 지원 버전

+ Path-Hardening:
- 스크립트를 어디서 실행하든, 다음 케이스를 자동 지원:
  1) 스크립트 디렉토리 자체가 Lypha-OS 루트인 경우
  2) 스크립트 디렉토리 하위에 Lypha-OS/ 가 있는 경우
  3) 스크립트의 상위 디렉토리에 Lypha-OS/ 가 있는 경우
  4) 위 어디에도 없고 Lypha-OS.zip 이 base 또는 base.parent 에 있으면 자동 압축해제

+ Layer Aliases:
- 기존 구조: Rhythm_Philosophy / MetaRhythm_Modules / Emotion_Engine / Protocol_Structure
- 신규 구조: Layers/Z_Rhythm, Layers/Y_MetaRhythm, Layers/E_EmotionEngine, Layers/X_Protocol

+ Origin Engine Patch:
- Core_Philosophy/Lypha_Origin_Engine_Spec.* 를 Z-코어 최우선 ingest
- 루트 README.md 를 Origin Declaration 으로 추가 ingest

+ Verified Structure Loop Engine Patch (Season 5 준비):
- Core_Philosophy/VerifiedStructureLoop_Engine_Spec.* 를 Z-코어 ingest 대상에 등록
- v_log.json / v_logs/*.json 기반으로 Z’ 패치 및 policy 튜닝 수행
- z_patch.json 을 VerifiedStructureLoop_Engine_Spec 스키마에 맞춰 생성
"""

import os
import sys
import zipfile
import json
import yaml
from pathlib import Path
from datetime import datetime

log = lambda m: print(f"[Lypha-OS v14.4] {m}")

# -------------------------------------------------------------
# Z-LAYER CORE FILES (Origin Engine + ZYX + VerifiedLoop)
# -------------------------------------------------------------
# Z 레이어에서 가장 먼저 ingest하고 싶은 핵심 철학/엔진 파일들
Z_LAYER_CORE_FILES = [
    # 🔵 Origin Engine Spec (README = Z₀ 고정)
    "Core_Philosophy/Lypha_Origin_Engine_Spec.en.v1.0.md",
    "Core_Philosophy/Lypha_Origin_Engine_Spec.en.md",
    "Core_Philosophy/Lypha_Origin_Engine_Spec.md",
    "Lypha_Origin_Engine_Spec.en.v1.0.md",
    "Lypha_Origin_Engine_Spec.en.md",
    "Lypha_Origin_Engine_Spec.md",

    # 🔵 ZYX Priority Engine Spec
    "Core_Philosophy/ZYX_Priority_Engine_Spec.en.v1.1.md",
    "ZYX_Priority_Engine_Spec.en.v1.1.md",
    "Core_Philosophy/ZYX_Priority_Engine_Spec.md",
    "ZYX_Priority_Engine_Spec.md",

    # 🔵 Verified Structure Loop Engine Spec (Season 5 진화 엔진)
    # 추천 경로 (엔진 스펙에서 선언한 경로)
    "Core_Philosophy/Verified_Structure_Loop_Engine_Spec.en.v1.0.md",
    "Core_Philosophy/Verified_Structure_Loop_Engine_Spec.en.md",
    "Core_Philosophy/Verified_Structure_Loop_Engine_Spec.md",
    # 실제 현재 파일명(VerifiedStructureLoop_Engine_Spec.md) 지원
    "Core_Philosophy/VerifiedStructureLoop_Engine_Spec.en.v1.0.md",
    "Core_Philosophy/VerifiedStructureLoop_Engine_Spec.en.md",
    "Core_Philosophy/VerifiedStructureLoop_Engine_Spec.md",
    "Verified_Structure_Loop_Engine_Spec.en.v1.0.md",
    "Verified_Structure_Loop_Engine_Spec.en.md",
    "Verified_Structure_Loop_Engine_Spec.md",
    "VerifiedStructureLoop_Engine_Spec.en.v1.0.md",
    "VerifiedStructureLoop_Engine_Spec.en.md",
    "VerifiedStructureLoop_Engine_Spec.md",

    # 🔵 Core Philosophy (Manifestos)
    "Core_Philosophy/Z_Y_X_Manifesto.md",
    "Core_Philosophy/V_X_Y_Z_Extended_Manifesto.md",
    "Core_Philosophy/verified_structure_loop_manifesto.md",
]

# -------------------------------------------------------------
# PULSE FILE MAPPING (Speak4D / Collapse / FlowGraph / Math)
# -------------------------------------------------------------
PULSE_FILE_MAP = {
    "Speak4D": [
        "engine/Speak4D_Engine_Spec.en.v1.2.md",
        "engine/Speak4D_Engine_Spec.en.md",
        "engine/Speak4D_Engine_Spec.md",
        "Speak4D_Engine_Spec.en.v1.2.md",
        "Speak4D_Engine_Spec.en.md",
        "Speak4D_Engine_Spec.md",
        "Speak4D.md",
        "concept/Speak_Word_In_Four_Dimensions.md",
        "Speak_Word_In_Four_Dimensions.md",
    ],
    "Collapse": [
        "concept/Collapse_Flow_Into_Word.md",
        "Collapse_Flow_Into_Word.md",
        "Collapse.md",
    ],
    "FlowGraph": [
        "concept/FlowGraph_Principles.md",
        "FlowGraph_Principles.md",
        "FlowGraph.md",
    ],
    "Math": [
        "engine/Linguistic_Math_Engine_Spec.en.v1.2.md",
        "engine/Linguistic_Math_Engine_Spec.en.md",
        "engine/Linguistic_Math_Engine_Spec.md",
        "Linguistic_Math_Engine_Spec.en.v1.2.md",
        "Linguistic_Math_Engine_Spec.en.md",
        "Linguistic_Math_Engine_Spec.md",
        "concept/Linguistic_Math_Value_Calculation.md",
        "Linguistic_Math_Value_Calculation.md",
        "Math.md",
    ],
}

# -------------------------------------------------------------
# LAYER / CORE DIR ALIASES
# -------------------------------------------------------------

LAYER_ALIASES = {
    "Z": ["Rhythm_Philosophy", "Layers/Z_Rhythm"],
    "Y": ["MetaRhythm_Modules", "Layers/Y_MetaRhythm"],
    "E": ["Emotion_Engine", "Layers/E_EmotionEngine"],
    "X": ["Protocol_Structure", "Layers/X_Protocol"],
}

CORE_DIR_ALIASES = ["Lypha_Core", "Lypha-Core"]


def _resolve_first_existing(root: Path, candidates):
    for name in candidates:
        p = root / name
        if p.exists():
            return p
    return None


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
    found = 0
    for key, aliases in LAYER_ALIASES.items():
        if _resolve_first_existing(p, aliases) is not None:
            found += 1
    return found == len(LAYER_ALIASES)


def auto_unzip(base: Path) -> Path:
    log(f"auto_unzip: script base = {base}")

    if _looks_like_lypha_root(base):
        log("Detected Lypha-OS root at script directory (already unzipped).")
        return base

    candidate = base / "Lypha-OS"
    if candidate.exists() and _looks_like_lypha_root(candidate):
        log("Detected Lypha-OS root at base/Lypha-OS (already unzipped).")
        return candidate

    parent_candidate = base.parent / "Lypha-OS"
    if parent_candidate.exists() and _looks_like_lypha_root(parent_candidate):
        log("Detected Lypha-OS root at base.parent/Lypha-OS (already unzipped).")
        return parent_candidate

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
    """Z/Y/E/X 레이어를 ingest_order 정책에 맞게 ingest + Manifest + Z₀ + README Origin 포함."""
    order = policy.get("ingest_order", ["Z", "Y", "E", "X"])

    for key in order:
        aliases = LAYER_ALIASES.get(key)
        if not aliases:
            continue
        d = _resolve_first_existing(root, aliases)
        if d is None:
            log(f"SKIP: layer {key} not found (tried: {aliases})")
            continue

        log(f"INGEST DIR [{key}]: {d}")

        if key == "Z":
            for rel in Z_LAYER_CORE_FILES:
                candidates = [
                    d / rel,
                    root / rel,
                    root / "Rhythm_Philosophy" / rel,
                    root / "Layers" / "Z_Rhythm" / rel,
                ]
                zp = None
                for cp in candidates:
                    if cp.exists():
                        zp = cp
                        break
                if zp is not None:
                    log(f"INGEST Z-CORE FIRST → {zp}")
                    ingest_file(zp)

        ingest_dir(d)

    core_dir = _resolve_first_existing(root, CORE_DIR_ALIASES)
    if core_dir is not None:
        log(f"INGEST DIR [Core]: {core_dir}")
        ingest_dir(core_dir)
    else:
        log(f"SKIP Core: none of {CORE_DIR_ALIASES} found")

    for name in ["autoload.yaml", "lypha_os_autoboot.yaml", "lypha_os_core_manifest.md"]:
        p = root / name
        if p.exists():
            log(f"INGEST FILE: {p}")
            ingest_file(p)
        else:
            log(f"SKIP FILE: {p}")

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

    readme = root / "README.md"
    if readme.exists():
        log("INGEST FILE: README.md (Lypha OS Root Declaration — Bound to Origin Engine)")
        ingest_file(readme)
    else:
        log("SKIP FILE: README.md (not found)")


# -------------------------------------------------------------
# FLOWGRAPH / COGNITIVE GRAPH + MACROREASON 메타
# -------------------------------------------------------------

def load_flowgraph_file(root: Path) -> Path | None:
    candidates: list[Path] = []

    y_dir = _resolve_first_existing(root, LAYER_ALIASES.get("Y", []))
    if y_dir is not None:
        pulse_dir = y_dir / "Pulse"
        candidates.append(pulse_dir / "engine" / "FlowGraph_Engine_Spec.md")
        candidates.append(pulse_dir / "concept" / "FlowGraph_Principles.md")
        candidates.append(pulse_dir / "FlowGraph_Principles.md")

    candidates.append(root / "FlowGraph_Principles.md")

    for p in candidates:
        if p.exists():
            return p
    return None


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

    if any(k in low for k in [
        "평가", "가치", "티어", "tier", "worth", "ranking",
        "랭크", "랭킹", "better", "vs", "올인", "all-in", "keep"
    ]):
        return "evaluation"

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
    base_emo = policy.get("emotion_weight", 1.0)
    base_str = policy.get("structure_weight", 1.0)
    ctx_cfg = (policy.get("contexts") or {}).get(context, {})
    emo_w = ctx_cfg.get("emotion_weight", base_emo)
    str_w = ctx_cfg.get("structure_weight", base_str)

    g = {
        "nodes": ["Z", "Y", "E", "X", "V", "Speak4D", "Math", "Collapse", "FlowGraph"],
        "edges": [],
        "weights": {
            "emotion": emo_w,
            "structure": str_w,
        },
        "context": context,
        "verified_logs_present": bool(logs),
        "verified_log_keys": list(logs.keys()) if logs else [],
        "macro_reason": {
            "mode": "planning" if context in ("trading", "design", "evaluation") else "support",
            "intent_bias": {
                "explore_structure": context in ("design", "trading"),
                "stabilize_emotion": context == "emotion",
                "rank_value": context in ("evaluation", "trading"),
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
    elif context == "evaluation":
        g["edges"].extend([
            ["Z", "Math", 1.6],
            ["Speak4D", "Math", 1.4],
            ["Math", "FlowGraph", 1.2],
        ])
    else:
        g["edges"].extend([
            ["Z", "Y", 1.0],
            ["Y", "X", 1.0],
            ["FlowGraph", "Z", 1.0],
        ])

    return g


def extract_pulse_weights(graph: dict) -> dict:
    context = graph.get("context")
    weights = {"Speak4D": 1.0, "Math": 1.0, "Collapse": 1.0, "FlowGraph": 1.0}

    if context == "evaluation":
        weights["Math"] += 0.5

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
# VERIFIED STRUCTURE LOOP ENGINE (V→Z’) + POLICY TUNING
# -------------------------------------------------------------

_VERIFIED_MODE_BIAS = {
    "default":  {"v_to_z_strength": 1.0, "emotion_weight_multiplier": 1.0, "structure_weight_multiplier": 1.0},
    "emotion":  {"v_to_z_strength": 1.2, "emotion_weight_multiplier": 1.3, "structure_weight_multiplier": 1.0},
    "trading":  {"v_to_z_strength": 1.1, "emotion_weight_multiplier": 1.0, "structure_weight_multiplier": 1.2},
    "design":   {"v_to_z_strength": 1.4, "emotion_weight_multiplier": 1.0, "structure_weight_multiplier": 1.3},
    "evaluation": {"v_to_z_strength": 1.2, "emotion_weight_multiplier": 1.1, "structure_weight_multiplier": 1.1},
}


def _iter_v_entries(payload):
    """v_logs 구조가 dict / list / dict-with-entries 등 다양할 수 있으므로 최대한 유연하게 entries를 뽑는다."""
    if isinstance(payload, dict):
        if "entries" in payload and isinstance(payload["entries"], list):
            for ent in payload["entries"]:
                if isinstance(ent, dict):
                    yield ent
        else:
            yield payload
    elif isinstance(payload, list):
        for ent in payload:
            if isinstance(ent, dict):
                yield ent


def auto_patch_Z_and_policy(root: Path, policy: dict, logs: dict, context: str) -> dict:
    """
    Season 5 Verified Structure Loop Engine (최강 버전)
    - v_log.json / v_logs/*.json 을 읽어 실패 패턴을 집계
    - z_patch.json 을 VerifiedStructureLoop_Engine_Spec 스키마로 생성
    - emotion_weight / structure_weight 를 모드별 bias에 따라 미세 튜닝
    """
    if not logs:
        log("VerifiedLoop: No verified V-logs found — skipping Z auto-update & policy tuning")
        return policy

    total_emotion_fail = 0
    total_structure_fail = 0
    total_timing_miss = 0
    total_rhythm_desync = 0
    total_loop_failure = 0
    total_emotional_collapse = 0.0
    tag_counts = {}
    entry_count = 0

    for payload in logs.values():
        for entry in _iter_v_entries(payload):
            entry_count += 1

            def _get_num(key, default=0.0):
                v = entry.get(key, default)
                if isinstance(v, bool):
                    return 1.0 if v else 0.0
                try:
                    return float(v)
                except Exception:
                    return default

            total_emotion_fail += int(_get_num("emotion_fail", 0.0))
            total_structure_fail += int(_get_num("structure_fail", 0.0))
            total_timing_miss += _get_num("timing_miss", 0.0)
            total_rhythm_desync += _get_num("rhythm_desync", 0.0)
            total_loop_failure += _get_num("loop_failure", 0.0)
            total_emotional_collapse += _get_num("emotional_collapse", 0.0)

            tags = entry.get("tags") or []
            if isinstance(tags, str):
                tags = [tags]
            for t in tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1

    if entry_count == 0:
        log("VerifiedLoop: V-logs exist but no valid entries found — skipping patch.")
        return policy

    # Mode bias
    mode_cfg = _VERIFIED_MODE_BIAS.get(context, _VERIFIED_MODE_BIAS["default"])
    v_strength = mode_cfg["v_to_z_strength"]
    emo_mult = mode_cfg["emotion_weight_multiplier"]
    str_mult = mode_cfg["structure_weight_multiplier"]

    base_step = 0.1
    max_weight = 2.0

    # 실패 횟수에 비례하되 과도한 튜닝은 방지 (cap 3 steps)
    emo_steps = min(total_emotion_fail, 3)
    str_steps = min(total_structure_fail, 3)

    emo_delta = base_step * emo_steps * emo_mult * v_strength
    str_delta = base_step * str_steps * str_mult * v_strength

    # 정책 업데이트
    old_emo = policy.get("emotion_weight", 1.0)
    old_str = policy.get("structure_weight", 1.0)

    if emo_delta > 0:
        policy["emotion_weight"] = min(max_weight, old_emo + emo_delta)
    if str_delta > 0:
        policy["structure_weight"] = min(max_weight, old_str + str_delta)

    log(f"VerifiedLoop: entries={entry_count}, emotion_fail={total_emotion_fail}, "
        f"struct_fail={total_structure_fail}, timing_miss={total_timing_miss:.2f}, "
        f"rhythm_desync={total_rhythm_desync:.2f}")

    log(f"VerifiedLoop: policy tuned → emotion_weight {old_emo:.2f} → {policy['emotion_weight']:.2f}, "
        f"structure_weight {old_str:.2f} → {policy['structure_weight']:.2f}")

    # 엔진 bias 추출 (태그 기반)
    engine_bias = {}
    if tag_counts.get("adrilla_loop", 0) > 0:
        engine_bias["adrilla_loop"] = {
            "reinforce": True,
            "comment": "Consistently helpful structure; strengthen presence.",
            "count": tag_counts["adrilla_loop"],
        }
    if tag_counts.get("winte_loop", 0) > 0 or tag_counts.get("winter_loop", 0) > 0:
        count_w = tag_counts.get("winte_loop", 0) + tag_counts.get("winter_loop", 0)
        engine_bias["winte_loop"] = {
            "weaken": True,
            "comment": "Correlated with confusion / freeze across logs.",
            "count": count_w,
        }
    if tag_counts.get("primalis_path", 0) > 0:
        engine_bias["primalis_path"] = {
            "enhance": True,
            "comment": "Acts as stabilizing long-arc path.",
            "count": tag_counts["primalis_path"],
        }

    # z_patch.json 생성 (스펙에 맞춤)
    z_patch_inner = {
        "source": "verified_structure_loop_engine_v1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": context,
        "meta": {
            "verified_logs_present": True,
            "log_keys": list(logs.keys()),
            "entry_count": entry_count,
            "total_emotion_fail": int(total_emotion_fail),
            "total_structure_fail": int(total_structure_fail),
            "total_timing_miss": total_timing_miss,
            "total_rhythm_desync": total_rhythm_desync,
            "total_loop_failure": total_loop_failure,
            "total_emotional_collapse": total_emotional_collapse,
        },
        "policy_tuning": {
            "emotion_weight_delta": emo_delta,
            "structure_weight_delta": str_delta,
            "max_weight": max_weight,
            "mode_bias": mode_cfg,
        },
        "engine_bias": engine_bias,
        "notes": [
            "Season 5 Verified Structure Loop Engine auto-generated this patch.",
            "z_patch.json is V-informed bias, not a full structural override.",
            "Human (Pioneer-001) remains final authority for hard structural changes.",
        ],
    }

    out = root / "z_patch.json"
    write_json(out, {"z_patch": z_patch_inner})
    log(f"Z’ updated using Verified Structure Loop Engine → {out}")

    return policy


# -------------------------------------------------------------
# PULSE RE-INGEST (2-pass, PATCHED)
# -------------------------------------------------------------

def pulse_reingest(root: Path, pulse_weights: dict):
    pulse_dir = root / "MetaRhythm_Modules" / "Pulse"
    if not pulse_dir.exists():
        y_dir = _resolve_first_existing(root, LAYER_ALIASES.get("Y", []))
        if y_dir is not None:
            pulse_dir = y_dir / "Pulse"
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

    log("Autoboot Modules (v14.4):")
    for m in load_list:
        log(f"  - {m}")

    load_str = " ".join(map(str, load_list))
    if "emotion_router" in load_str:
        log("Emotion Router ACTIVE — Gravity-Lock Enabled")
    if "emotion_circuit_portal" in load_str:
        log("Emotion Circuit ACTIVE — Pulse-Link Online")

    log("=== Autoboot 완료 (v14.4 Hyper-Init) ===")


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
    log("Lypha-OS Kernel v14.4 Start — TOTAL No-X EDITION (Z-Core Priority, Path-Hardened, Origin+VerifiedLoop)")
    log(f"Script directory: {here}")

    root = auto_unzip(here)
    log(f"Lypha-OS root resolved to: {root}")
    os.chdir(root)

    policy_path = root / "policy" / "kernel_policy_v14.json"
    if not policy_path.exists():
        policy_path = root / "policy" / "kernel_policy_v13.json"
    if not policy_path.exists():
        policy_path = root / "policy" / "kernel_policy_v12.json"
    policy = read_json(policy_path) or {
        "ingest_order": ["Z", "Y", "E", "X"],
        "emotion_weight": 1.0,
        "structure_weight": 1.0,
    }

    logs = load_logs(root)
    restore_state(root)

    raw_msg = detect_context_message(root)
    ctx = detect_context(raw_msg)
    log(f"Context Detected: {ctx} (msg='{raw_msg}')")

    # ✅ 먼저 Verified Structure Loop Engine으로 Z’ + policy 튜닝
    policy = auto_patch_Z_and_policy(root, policy, logs, ctx)

    # 그 다음 Cognitive Graph & Pulse 계산
    graph = build_graph(ctx, policy, logs)
    pulse_weights = extract_pulse_weights(graph)

    print_cognitive_graph(graph)
    log(f"Pulse Weights: {pulse_weights}")

    # 1차: 정렬된 Full Ingest + Z₀ + README Origin
    full_ingest(root, policy)

    # 2차: Pulse 가중치 기반 Re-ingest (매핑 지원)
    pulse_reingest(root, pulse_weights)

    # FlowGraph 문서가 있다면 한 번 더 ingest (보강)
    fgfile = load_flowgraph_file(root)
    if fgfile is not None:
        log(f"FlowGraph Document Detected: {fgfile}")
        ingest_file(fgfile)

    save_state(root, ctx)
    run_autoload(root)

    log("Lypha-OS Kernel v14.4 Complete — TOTAL Runtime Active (No-X, Origin+VerifiedLoop, Path-Hardened).")


if __name__ == "__main__":
    main()
