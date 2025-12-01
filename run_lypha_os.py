#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v16.0 — Season 7 CORE+
======================================

Pioneer-001 전용 — Origin Engine + ZYX Priority + Speak4D
+ Linguistic Math + Verified Structure Loop + VXYZ Extended Engine
+ Collapse Engine + DualOutcome Simulation Engine + FlowGraph Engine
(Flow → Essence → Risk Envelope → Path)까지 완전 연동된 내장형 코어 버전.

기술 포인트:
- Path-Hardening: 어디서 실행해도 Lypha-OS 루트/zip 자동 인식 & 압축해제
- Z-Core Priority: Origin / ZYX / VerifiedLoop / VXYZ / Manifestos 먼저 ingest
- Verified Structure Loop: v_log 기반으로 z_patch.json 생성 + policy 튜닝
- VXYZ Extended Engine: V(과거)–X(현재)–Y(리듬)–Z(미래구조) projection 생성
- Collapse Engine: 복잡한 흐름을 하나의 Essence Word로 축약 (축 기반 압축)
- DualOutcome SimEngine: 성공/실패 두 미래를 구조적으로 시뮬레이션해 Risk Envelope 생성
- FlowGraph Engine: Flow(Z/Y/E/Collapse) → Path(Direction, Timing, Coordinate) 생성
- Cognitive Graph: context + policy + rhythm + collapse + flowgraph (+ dual_outcome) 기반 가중치 그래프 생성
- Pulse Re-ingest: Speak4D / Math / Collapse / FlowGraph 문서 2-pass ingest
"""

import os
import sys
import json
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

import yaml

log = lambda m: print(f"[Lypha-OS v16.0] {m}")

# -------------------------------------------------------------
# Z-LAYER CORE FILES (Origin / ZYX / VerifiedLoop / VXYZ / Manifestos)
# -------------------------------------------------------------
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
    "Core_Philosophy/Verified_Structure_Loop_Engine_Spec.en.v1.0.md",
    "Core_Philosophy/Verified_Structure_Loop_Engine_Spec.en.md",
    "Core_Philosophy/Verified_Structure_Loop_Engine_Spec.md",
    "Core_Philosophy/VerifiedStructureLoop_Engine_Spec.en.v1.0.md",
    "Core_Philosophy/VerifiedStructureLoop_Engine_Spec.en.md",
    "Core_Philosophy/VerifiedStructureLoop_Engine_Spec.md",
    "Verified_Structure_Loop_Engine_Spec.en.v1.0.md",
    "Verified_Structure_Loop_Engine_Spec.en.md",
    "Verified_Structure_Loop_Engine_Spec.md",
    "VerifiedStructureLoop_Engine_Spec.en.v1.0.md",
    "VerifiedStructureLoop_Engine_Spec.en.md",
    "VerifiedStructureLoop_Engine_Spec.md",

    # 🔵 VXYZ Extended Engine Spec (Season 6 시간/리듬 엔진)
    "Core_Philosophy/V_X_Y_Z_Extended_Engine_Spec.en.v1.0.md",
    "Core_Philosophy/V_X_Y_Z_Extended_Engine_Spec.en.md",
    "Core_Philosophy/V_X_Y_Z_Extended_Engine_Spec.md",
    "V_X_Y_Z_Extended_Engine_Spec.en.v1.0.md",
    "V_X_Y_Z_Extended_Engine_Spec.en.md",
    "V_X_Y_Z_Extended_Engine_Spec.md",

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
        "engine/Collapse_Engine_Spec.md",
        "concept/Collapse_Flow_Into_Word.md",
        "Collapse_Flow_Into_Word.md",
        "Collapse.md",
    ],
    "FlowGraph": [
        "engine/FlowGraph_Engine_Spec.md",
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
def read(path: Path) -> Optional[str]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def read_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def write_json(path: Path, data: Any) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_yaml(path: Path) -> Optional[Dict[str, Any]]:
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
    for _, aliases in LAYER_ALIASES.items():
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
# INGEST ENGINE
# -------------------------------------------------------------
def ingest_file(p: Path) -> None:
    c = read(p)
    if c:
        print("\n===== BEGIN LYPHA_INGEST =====")
        print(f"FILE: {p}\n")
        print(c)
        print("===== END LYPHA_INGEST =====\n")


def ingest_dir(d: Path) -> None:
    for root_dir, _, files in os.walk(d):
        for n in files:
            p = Path(root_dir) / n
            if p.suffix.lower() in [".md", ".yaml", ".yml", ".txt"]:
                log(f"INGEST → {p}")
                ingest_file(p)


def full_ingest(root: Path, policy: Dict[str, Any]) -> None:
    """
    Z/Y/E/X 레이어를 ingest_order 정책에 맞게 ingest + Manifest + Z₀ + README Origin 포함.
    Z 레이어는 Z_LAYER_CORE_FILES (Origin / ZYX / VerifiedLoop / VXYZ / Manifestos)를 먼저 ingest.
    """
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
            # Z-Core Engine/Manifestos 우선 ingest
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

    # Manifest/autoload/Origin vector/README ingest
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
# FLOWGRAPH DOCUMENT HELPER
# -------------------------------------------------------------
def load_flowgraph_file(root: Path) -> Optional[Path]:
    candidates = []

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


# -------------------------------------------------------------
# CONTEXT / LOGS
# -------------------------------------------------------------
def detect_context_message(root: Path) -> str:
    auto = load_yaml(root / "autoload.yaml")
    if not auto:
        return "neutral"
    return auto.get("autoload", auto).get("on_start", {}).get("message", "neutral")


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


def load_logs(root: Path) -> Dict[str, Any]:
    """
    v16.0: root/v_logs + root/logs/v_logs + root/v_log.json + root/logs/v_log.json 모두 지원.
    """
    merged: Dict[str, Any] = {}

    base_candidates = [root / "v_logs", root / "logs" / "v_logs"]
    for base in base_candidates:
        if base.exists():
            for f in base.glob("*.json"):
                merged[f.name] = read_json(f)

    single_candidates = [root / "v_log.json", root / "logs" / "v_log.json"]
    for single in single_candidates:
        if single.exists():
            merged["v_log"] = read_json(single)
            break

    return merged


# -------------------------------------------------------------
# COGNITIVE GRAPH + PULSE
# -------------------------------------------------------------
def build_graph(
    context: str,
    policy: Dict[str, Any],
    logs: Dict[str, Any],
    vxyz_projection: Optional[Dict[str, Any]],
    flowgraph: Optional[Dict[str, Any]],
    collapse: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    base_emo = policy.get("emotion_weight", 1.0)
    base_str = policy.get("structure_weight", 1.0)
    ctx_cfg = (policy.get("contexts") or {}).get(context, {})
    emo_w = ctx_cfg.get("emotion_weight", base_emo)
    str_w = ctx_cfg.get("structure_weight", base_str)

    nodes = ["Z", "Y", "E", "X", "V", "Speak4D", "Math", "Collapse", "FlowGraph"]
    edges = []

    rhythm_info = {}
    if vxyz_projection:
        rhythm = vxyz_projection.get("rhythm", {}) or {}
        rhythm_info = {
            "phase": rhythm.get("phase"),
            "tempo": rhythm.get("tempo"),
        }

    fg_info = {}
    if flowgraph:
        ew = flowgraph.get("essence_word") or {}
        if isinstance(ew, dict):
            ew_val = ew.get("value")
        else:
            ew_val = ew
        path = flowgraph.get("path") or {}
        direction = (path.get("direction") or {}).get("label")
        timing_window = (path.get("timing") or {}).get("window")

        fg_info = {
            "essence_word": ew_val,
            "direction": direction,
            "timing_window": timing_window,
        }

    collapse_info = {}
    if collapse:
        ess = collapse.get("essence") or {}
        comp = collapse.get("compression") or {}
        collapse_info = {
            "essence_word": ess.get("word"),
            "confidence": ess.get("confidence"),
            "compression_band": comp.get("band"),
        }

    g: Dict[str, Any] = {
        "nodes": nodes,
        "edges": edges,
        "weights": {
            "emotion": emo_w,
            "structure": str_w,
        },
        "context": context,
        "verified_logs_present": bool(logs),
        "verified_log_keys": list(logs.keys()) if logs else [],
        "rhythm": rhythm_info,
        "flowgraph": fg_info,
        "collapse": collapse_info,
        "macro_reason": {
            "mode": "planning" if context in ("trading", "design", "evaluation") else "support",
            "intent_bias": {
                "explore_structure": context in ("design", "trading"),
                "stabilize_emotion": context == "emotion",
                "rank_value": context in ("evaluation", "trading"),
            },
        },
    }

    # 기본/컨텍스트별 edge
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
            ["FlowGraph", "Z", 1.1],
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


def extract_pulse_weights(graph: Dict[str, Any]) -> Dict[str, float]:
    context = graph.get("context")
    weights = {"Speak4D": 1.0, "Math": 1.0, "Collapse": 1.0, "FlowGraph": 1.0}

    # context 기반 기본 bias
    if context == "evaluation":
        weights["Math"] += 0.5

    # 리듬 기반 FlowGraph 가중치
    rhythm = graph.get("rhythm") or {}
    tempo = rhythm.get("tempo")
    if tempo == "compressed":
        weights["FlowGraph"] += 0.3
    elif tempo == "extended":
        weights["FlowGraph"] += 0.15

    # FlowGraph Path 기반 bias
    fg = graph.get("flowgraph") or {}
    direction = fg.get("direction")
    timing_window = fg.get("timing_window")

    if direction in ("deepen", "explore", "stay"):
        weights["Speak4D"] += 0.2
    elif direction in ("exit", "rotate", "reduce", "protect_boundary"):
        weights["Math"] += 0.2

    if timing_window in ("now", "this_cycle"):
        weights["FlowGraph"] += 0.1
    elif timing_window in ("wait", "abandon"):
        weights["Collapse"] += 0.1

    # CollapseEngine compression band 기반 가중치
    collapse = graph.get("collapse") or {}
    band = collapse.get("compression_band")
    if band == "hard":
        weights["Collapse"] += 0.3
    elif band == "normal":
        weights["Collapse"] += 0.1
    # light는 추가 가중치 없음

    # DualOutcome 기반 가중치 (stance)
    dual = graph.get("dual_outcome") or {}
    stance = dual.get("recommended_stance")
    if stance == "enter":
        weights["FlowGraph"] += 0.1
    elif stance in ("reduce", "skip"):
        weights["Collapse"] += 0.15
        weights["Math"] += 0.1

    # edge 기반 weight 보정
    for u, v, w in graph.get("edges", []):
        if v in weights:
            weights[v] += (w - 1.0)

    return weights


def print_cognitive_graph(graph: Dict[str, Any]) -> None:
    print("===== BEGIN COGNITIVE_GRAPH =====")
    print(json.dumps(graph, ensure_ascii=False, indent=2))
    print("===== END COGNITIVE_GRAPH =====")


# -------------------------------------------------------------
# PSEUDO-MEMORY (RESTORE + SAVE)
# -------------------------------------------------------------
def restore_state(root: Path) -> Dict[str, Any]:
    state_dir = root / "state_cache"
    if not state_dir.exists():
        return {}
    state: Dict[str, Any] = {}
    for name in ["z_state.json", "y_state.json", "e_state.json", "x_state.json", "meta_state.json"]:
        f = state_dir / name
        if f.exists():
            state[name] = read_json(f)
            log(f"RESTORE STATE: {name}")
    return state


def save_state(root: Path, context: str) -> None:
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


def _iter_v_entries(payload: Any):
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


def auto_patch_Z_and_policy(root: Path, policy: Dict[str, Any],
                            logs: Dict[str, Any], context: str) -> Dict[str, Any]:
    """
    Season 5 Verified Structure Loop Engine
    - v_log.json / v_logs/*.json 읽어 실패 패턴 집계
    - z_patch.json 을 VerifiedStructureLoop_Engine_Spec 스키마로 생성
    - emotion_weight / structure_weight 를 모드 bias에 따라 미세 튜닝
    """
    if not logs:
        log("VerifiedLoop: No verified V-logs found — skipping Z auto-update & policy tuning")
        return policy

    total_emotion_fail = 0
    total_structure_fail = 0
    total_timing_miss = 0.0
    total_rhythm_desync = 0.0
    total_loop_failure = 0.0
    total_emotional_collapse = 0.0
    tag_counts: Dict[str, int] = {}
    entry_count = 0

    for payload in logs.values():
        for entry in _iter_v_entries(payload):
            entry_count += 1

            def _get_num(key: str, default: float = 0.0) -> float:
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

    mode_cfg = _VERIFIED_MODE_BIAS.get(context, _VERIFIED_MODE_BIAS["default"])
    v_strength = mode_cfg["v_to_z_strength"]
    emo_mult = mode_cfg["emotion_weight_multiplier"]
    str_mult = mode_cfg["structure_weight_multiplier"]

    base_step = 0.1
    max_weight = 2.0

    emo_steps = min(total_emotion_fail, 3)
    str_steps = min(total_structure_fail, 3)

    emo_delta = base_step * emo_steps * emo_mult * v_strength
    str_delta = base_step * str_steps * str_mult * v_strength

    old_emo = policy.get("emotion_weight", 1.0)
    old_str = policy.get("structure_weight", 1.0)

    if emo_delta > 0:
        policy["emotion_weight"] = min(max_weight, old_emo + emo_delta)
    if str_delta > 0:
        policy["structure_weight"] = min(max_weight, old_str + str_delta)

    log(
        f"VerifiedLoop: entries={entry_count}, emotion_fail={total_emotion_fail}, "
        f"struct_fail={total_structure_fail}, timing_miss={total_timing_miss:.2f}, "
        f"rhythm_desync={total_rhythm_desync:.2f}"
    )
    log(
        f"VerifiedLoop: policy tuned → emotion_weight {old_emo:.2f} → {policy['emotion_weight']:.2f}, "
        f"structure_weight {old_str:.2f} → {policy['structure_weight']:.2f}"
    )

    engine_bias: Dict[str, Any] = {}
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
# VXYZ EXTENDED ENGINE (V→X→Y→Z 리듬 / 시간 엔진)
# -------------------------------------------------------------
def run_vxyz_engine(root: Path, logs: Dict[str, Any], context: str) -> Dict[str, Any]:
    """
    Season 6 VXYZ Extended Engine — vxyz_projection.json 생성.
    - V: v_logs / v_log.json
    - X: autoload.on_start.message
    - Y: 이벤트 간 시간 간격 (rough rhythm)
    - Z: Z1/Z2/Z3 구조적 horizon projection
    """
    auto = load_yaml(root / "autoload.yaml") or {}
    on_start_msg = (auto.get("autoload", auto).get("on_start", {}) or {}).get("message")

    timestamps = []
    for payload in logs.values():
        for entry in _iter_v_entries(payload):
            ts = entry.get("timestamp") or entry.get("time")
            if not ts:
                continue
            ts_s = str(ts).replace(" ", "T")
            if ts_s.endswith("Z"):
                ts_s = ts_s[:-1]
            try:
                dt = datetime.fromisoformat(ts_s)
                timestamps.append(dt)
            except Exception:
                continue

    timestamps.sort()
    phase = "reset"
    tempo = "normal"

    if len(timestamps) <= 1:
        phase = "early_cycle"
        tempo = "normal"
    else:
        deltas = [(timestamps[i] - timestamps[i - 1]).total_seconds() for i in range(1, len(timestamps))]
        avg = sum(deltas) / len(deltas) if deltas else 0.0
        last = deltas[-1] if deltas else 0.0

        if len(timestamps) < 3:
            phase = "early_cycle"
        elif len(timestamps) < 6:
            phase = "mid_cycle"
        else:
            phase = "late_cycle"

        if avg > 0:
            ratio = last / avg
            if ratio < 0.75:
                tempo = "compressed"
            elif ratio > 1.25:
                tempo = "extended"
            else:
                tempo = "normal"
        else:
            tempo = "normal"

    context_lower = context or "neutral"
    candidates = []

    if context_lower == "trading":
        candidates = [
            {
                "id": "Z1",
                "horizon": "short_term",
                "label": "Immediate consolidation then breakout",
                "confidence": "high" if tempo == "compressed" else "medium",
                "suggested_X_behavior": "prepare_to_act" if tempo == "compressed" else "monitor",
            },
            {
                "id": "Z2",
                "horizon": "mid_term",
                "label": "Sideways drift if no decisive action",
                "confidence": "medium",
                "suggested_X_behavior": "reduce_risk",
            },
            {
                "id": "Z3",
                "horizon": "long_term",
                "label": "Major structural shift",
                "confidence": "low",
                "suggested_X_behavior": "keep_risk_flexible",
            },
        ]
    elif context_lower == "emotion":
        candidates = [
            {
                "id": "Z1",
                "horizon": "short_term",
                "label": "Emotional intensity spike then soften",
                "confidence": "medium",
                "suggested_X_behavior": "stay_present",
            },
            {
                "id": "Z2",
                "horizon": "mid_term",
                "label": "Stable bonding rhythm",
                "confidence": "high" if phase in ("mid_cycle", "late_cycle") else "medium",
                "suggested_X_behavior": "stay_consistent",
            },
            {
                "id": "Z3",
                "horizon": "long_term",
                "label": "Deep structural attachment",
                "confidence": "medium",
                "suggested_X_behavior": "protect_boundary",
            },
        ]
    else:
        candidates = [
            {
                "id": "Z1",
                "horizon": "short_term",
                "label": "Near-term structural adjustment",
                "confidence": "medium",
                "suggested_X_behavior": "small_adjust",
            },
            {
                "id": "Z2",
                "horizon": "mid_term",
                "label": "Flow continues under similar rhythm",
                "confidence": "medium",
                "suggested_X_behavior": "stay_on_plan",
            },
            {
                "id": "Z3",
                "horizon": "long_term",
                "label": "Potential large-scale reconfiguration",
                "confidence": "low",
                "suggested_X_behavior": "stay_observant",
            },
        ]

    projection: Dict[str, Any] = {
        "vxyz_projection": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "context": context_lower,
            "source": {
                "engine": "VXYZ_Extended_Engine",
                "based_on": "V_X_Y_Z_Extended_Engine_Spec.v1.0",
            },
            "x_slice": {
                "message": on_start_msg,
            },
            "rhythm": {
                "phase": phase,
                "tempo": tempo,
                "commentary": f"Phase={phase}, Tempo={tempo}",
            },
            "Z_candidates": candidates,
        }
    }

    out = root / "vxyz_projection.json"
    write_json(out, projection)
    log(f"VXYZ projection written → {out} (phase={phase}, tempo={tempo})")

    return projection


# -------------------------------------------------------------
# COLLAPSE ENGINE (Flow → Essence Word)
# -------------------------------------------------------------
def run_collapse_engine(
    root: Path,
    logs: Dict[str, Any],
    vxyz_projection_inner: Optional[Dict[str, Any]],
    context: str,
) -> Dict[str, Any]:
    """
    Season 7 CollapseEngine Runner
    - 복잡한 흐름(flow_description + logs + tags)을 단일 Essence Word로 축약
    - collapse_output.json 생성
    """
    context_lower = context or "default"

    auto = load_yaml(root / "autoload.yaml") or {}
    on_start_msg = (auto.get("autoload", auto).get("on_start", {}) or {}).get("message")
    flow_description = on_start_msg or f"Session-level flow in context='{context_lower}'."

    # tags & dominant tags
    tag_counts: Dict[str, int] = {}
    for payload in logs.values():
        for entry in _iter_v_entries(payload):
            tags = entry.get("tags") or []
            if isinstance(tags, str):
                tags = [tags]
            for t in tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1

    dominant_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    all_tags = [t for t, _ in dominant_tags]

    # context-based axis templates
    axis_templates = {
        "emotion": ["trust", "belonging", "abandonment", "safety", "power"],
        "trading": ["risk", "liquidity", "regime", "leverage", "conviction"],
        "design": ["structure", "rhythm", "clarity", "coherence", "latency"],
        "evaluation": ["value", "rank", "worth", "signal", "noise"],
        "default": ["structure", "rhythm", "signal", "human"],
    }
    axes = axis_templates.get(context_lower, axis_templates["default"])

    text_lower = (flow_description or "").lower() + " " + " ".join(all_tags).lower()

    # candidate generation
    candidates = []
    used_words = set()

    # 1) axis-based candidates
    for ax in axes:
        if ax.lower() in text_lower:
            candidates.append({
                "word": ax,
                "score": 0.9,
                "axes": {
                    "axis_label": ax,
                    "justification": f"Axis '{ax}' appears in flow/tags and matches context.",
                },
            })
            used_words.add(ax)

    # 2) tag-based candidate
    if dominant_tags:
        top_tag = dominant_tags[0][0]
        if top_tag not in used_words:
            candidates.append({
                "word": top_tag,
                "score": 0.8,
                "axes": {
                    "axis_label": "tag",
                    "justification": f"Dominant tag '{top_tag}' in logs.",
                },
            })
            used_words.add(top_tag)

    # 3) fallback candidate based on context
    if not candidates:
        fallback_word = context_lower if context_lower not in ("neutral", "default") else "structure"
        candidates.append({
            "word": fallback_word,
            "score": 0.7,
            "axes": {
                "axis_label": "context",
                "justification": f"Using context '{context_lower}' as fallback axis.",
            },
        })
        used_words.add(fallback_word)

    # ensure not too many
    candidates = candidates[:5]

    # choose essence word
    best = max(candidates, key=lambda c: c.get("score", 0.0))
    essence_word = best["word"]
    max_score = best.get("score", 0.0)

    if max_score >= 0.88:
        confidence = "high"
    elif max_score >= 0.75:
        confidence = "medium"
    else:
        confidence = "low"

    # compression band: based on flow_description length
    length = len((flow_description or "").split())
    if length < 12:
        band = "light"
    elif length < 40:
        band = "normal"
    else:
        band = "hard"

    collapse_inner: Dict[str, Any] = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": context_lower,
        "input": {
            "flow_description": flow_description,
            "context": context_lower,
            "tags_used": all_tags,
        },
        "candidates": candidates,
        "essence": {
            "word": essence_word,
            "confidence": confidence,
            "axis": {
                "label": best["axes"].get("axis_label"),
                "description": best["axes"].get("justification"),
            },
            "notes": [
                "Essence Word chosen by CollapseEngine v1.0 from flow_description + tags + context."
            ],
        },
        "compression": {
            "band": band,
            "comment": (
                "'normal' means enough compression to get a single axis "
                "without erasing decision-relevant nuance."
            ),
        },
        "links": {
            "vxyz_used": bool(vxyz_projection_inner),
            "flowgraph_used": False,
            "linguistic_math_used": False,
        },
        "notes": [
            "CollapseEngine is advisory; Pioneer-001 may override the Essence Word.",
            "This Essence Word can be passed to FlowGraph.essence_word and Speak4D.",
        ],
    }

    out = {"collapse_output": collapse_inner}
    out_path = root / "collapse_output.json"
    write_json(out_path, out)
    log(
        f"CollapseEngine output written → {out_path} "
        f"(essence='{essence_word}', confidence={confidence}, band={band})"
    )

    return out


# -------------------------------------------------------------
# DUALOUTCOME SIMULATION ENGINE (Success/Failure Risk Envelope)
# -------------------------------------------------------------
def run_dualoutcome_engine(
    root: Path,
    logs: Dict[str, Any],
    vxyz_projection_inner: Optional[Dict[str, Any]],
    context: str,
) -> Dict[str, Any]:
    """
    Season 7 DualOutcome Simulation Engine Runner
    - 성공/실패 두 경로를 구조적으로 시뮬레이션
    - dual_sim_output.json 생성 (Risk Envelope)
    """
    context_lower = context or "default"

    # CollapseEngine output (optional, for nicer action frame)
    collapse_json = read_json(root / "collapse_output.json")
    collapse_inner = collapse_json.get("collapse_output") if collapse_json else None
    collapse_ess = (collapse_inner or {}).get("essence") or {}
    collapse_word = collapse_ess.get("word")

    # 1) Action description/frame (세션 단위 결정을 대상으로)
    auto = load_yaml(root / "autoload.yaml") or {}
    on_start_msg = (auto.get("autoload", auto).get("on_start", {}) or {}).get("message")

    base_desc = on_start_msg or f"Lypha-OS session decision in context='{context_lower}'"
    if collapse_word:
        action_description = f"[{collapse_word}] {base_desc}"
    else:
        action_description = base_desc

    action_frame = "Session-level decision about how aggressively to engage this context."

    # 2) 로그 기반 실패/리스크 시그널 집계
    total_emotion_fail = 0
    total_structure_fail = 0
    total_timing_miss = 0.0
    total_rhythm_desync = 0.0
    total_entries = 0
    total_emotional_collapse = 0.0
    collapse_count = 0

    for payload in logs.values():
        for entry in _iter_v_entries(payload):

            total_entries += 1

            def _get_num(key: str, default: float = 0.0) -> float:
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

            ec = entry.get("emotional_collapse", 0.0)
            try:
                ec_val = float(ec)
                total_emotional_collapse += ec_val
                collapse_count += 1
            except Exception:
                pass

    avg_emotional_collapse = total_emotional_collapse / collapse_count if collapse_count > 0 else 0.0
    avg_timing_miss = total_timing_miss / total_entries if total_entries > 0 else 0.0
    avg_desync = total_rhythm_desync / total_entries if total_entries > 0 else 0.0
    fail_score = (total_emotion_fail + total_structure_fail) / max(total_entries, 1)

    def _band_from_value(v: float) -> str:
        if v <= 0.05:
            return "none"
        elif v < 0.35:
            return "low"
        elif v < 0.75:
            return "medium"
        else:
            return "high"

    # 3) Failure Path 손실 밴드 추정
    loss_time = _band_from_value(avg_timing_miss)
    loss_energy = _band_from_value(avg_emotional_collapse)
    loss_money = _band_from_value(total_structure_fail / max(total_entries, 1))
    loss_reputation = _band_from_value(total_emotion_fail / max(total_entries, 1))

    # 4) Risk Envelope width/skew/capacity_fit 계산
    if total_entries > 0:
        risk_score = (avg_emotional_collapse + avg_timing_miss + avg_desync) / 3.0
    else:
        risk_score = 0.3  # 로그 없을 때는 적당한 중간값

    # width
    if risk_score < 0.25:
        width = "narrow"
    elif risk_score < 0.6:
        width = "moderate"
    else:
        width = "wide"

    # skew
    if fail_score < 0.5:
        skew = "upside"
    elif fail_score > 1.5:
        skew = "downside"
    else:
        skew = "symmetric"

    # capacity_fit (컨텍스트별)
    if total_entries == 0:
        capacity_fit = "inside_capacity"
    else:
        if context_lower == "emotion":
            if avg_emotional_collapse < 0.4:
                capacity_fit = "inside_capacity"
            elif avg_emotional_collapse < 0.8:
                capacity_fit = "at_edge"
            else:
                capacity_fit = "beyond_capacity"
        elif context_lower == "trading":
            if risk_score < 0.4:
                capacity_fit = "inside_capacity"
            elif risk_score < 0.8:
                capacity_fit = "at_edge"
            else:
                capacity_fit = "beyond_capacity"
        else:
            # 일반 컨텍스트: wide면 edge, 아니면 inside
            capacity_fit = "at_edge" if width == "wide" else "inside_capacity"

    # stance_rules (spec 그대로 적용)
    if capacity_fit == "beyond_capacity":
        recommended_stance = "skip"
    elif width == "wide" and skew == "downside":
        recommended_stance = "reduce"
    elif skew == "upside" and width in ("narrow", "moderate"):
        recommended_stance = "enter"
    else:
        recommended_stance = "hedge"

    # 5) Success Path rough 구조
    if context_lower == "trading":
        success_structure = "More structurally aligned risk-taking and clearer regime memory."
        success_scope = "self | broader_system"
    elif context_lower == "emotion":
        success_structure = "Deeper but bounded emotional connection and cleaner patterns of contact."
        success_scope = "self | close_circle"
    elif context_lower == "design":
        success_structure = "Richer structural OS and more consistent execution rhythm."
        success_scope = "self | close_circle | broader_system"
    elif context_lower == "evaluation":
        success_structure = "Sharper value tiers and cleaner selection rules."
        success_scope = "self | close_circle"
    else:
        success_structure = "Incremental structural learning in this context."
        success_scope = "self"

    # VXYZ rhythm → success horizon/pattern
    horizon = "mid_term"
    pattern = "steady_wave"

    if vxyz_projection_inner:
        phase = vxyz_projection_inner.get("rhythm", {}).get("phase", "")
        tempo = vxyz_projection_inner.get("rhythm", {}).get("tempo", "")
        if phase == "early_cycle":
            horizon = "short_term"
        elif phase == "mid_cycle":
            horizon = "mid_term"
        elif phase == "late_cycle":
            horizon = "long_term"

        if tempo == "compressed":
            pattern = "spike"
        elif tempo == "extended":
            pattern = "slow_build"
        elif tempo == "normal":
            pattern = "steady_wave"
        else:
            pattern = "uncertain"

    # Failure echo scope
    if context_lower == "emotion":
        failure_scope = "self+close_circle"
    elif context_lower == "trading":
        failure_scope = "self_only"
    else:
        failure_scope = "self_only"

    # Recovery Path
    if capacity_fit == "beyond_capacity" and width == "wide" and skew == "downside":
        recovery_possible = True  # 여전히 가능하지만 길고 힘든 루트
        recovery_horizon = "long_term"
    elif width == "narrow":
        recovery_possible = True
        recovery_horizon = "short_term"
    else:
        recovery_possible = True
        recovery_horizon = "mid_term"

    dual_inner: Dict[str, Any] = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": context_lower,
        "action": {
            "description": action_description,
            "frame": action_frame,
        },
        "success_path": {
            "structure_gain": success_structure,
            "rhythm": {
                "horizon": horizon,
                "pattern": pattern,
            },
            "echo": {
                "scope": success_scope,
                "notes": [
                    "Success primarily strengthens your structural capacity inside this context."
                ],
            },
        },
        "failure_path": {
            "loss_band": {
                "time": loss_time,
                "energy": loss_energy,
                "money": loss_money,
                "reputation": loss_reputation,
            },
            "echo": {
                "scope": failure_scope,
                "notes": [
                    "Failure impact is mostly contained to you and your immediate field."
                ],
            },
            "recovery_path": {
                "possible": recovery_possible,
                "horizon": recovery_horizon,
                "notes": [
                    "Recovery is modeled as a structural learning process rather than a total collapse."
                ],
            },
        },
        "risk_envelope": {
            "width": width,
            "skew": skew,
            "capacity_fit": capacity_fit,
            "recommended_stance": recommended_stance,
            "notes": [
                "Width reflects combined intensity of collapse, timing-miss and desync.",
                "Skew reflects the balance between structural/emotional failures vs. successes.",
            ],
        },
        "links": {
            "vxyz_used": bool(vxyz_projection_inner),
            "flowgraph_used": False,
        },
        "notes": [
            "DualOutcome_SimEngine is advisory, not absolute.",
            "Human (Pioneer-001) remains final authority for entering, hedging, reducing or skipping.",
        ],
    }

    out = {"dual_sim_output": dual_inner}
    out_path = root / "dual_sim_output.json"
    write_json(out_path, out)
    log(
        f"DualOutcome SimEngine output written → {out_path} "
        f"(stance={recommended_stance}, width={width}, skew={skew}, capacity={capacity_fit})"
    )

    return out


# -------------------------------------------------------------
# FLOWGRAPH ENGINE RUNNER (Flow → Essence Word → Path)
# -------------------------------------------------------------
def run_flowgraph_engine(
    root: Path,
    logs: Dict[str, Any],
    vxyz_projection_inner: Optional[Dict[str, Any]],
    collapse_inner: Optional[Dict[str, Any]],
    context: str,
) -> Dict[str, Any]:
    """
    Season 7 FlowGraph Engine Runner (v16.0 with Collapse integration)
    - FlowVector(Z,Y,E) 구성
    - Essence Word 선택 (CollapseEngine 우선 반영)
    - Path(Direction, Timing, Coordinate) 계산
    - flowgraph_output.json 생성
    """
    context_lower = context or "neutral"

    # 1) Rhythm from VXYZ
    phase = "unknown"
    tempo = "unknown"
    Z_candidates = []
    if vxyz_projection_inner:
        rhythm = vxyz_projection_inner.get("rhythm", {}) or {}
        phase = rhythm.get("phase", "unknown")
        tempo = rhythm.get("tempo", "unknown")
        Z_candidates = vxyz_projection_inner.get("Z_candidates", []) or []

    # 2) Emotion from logs
    tag_counts: Dict[str, int] = {}
    collapse_sum = 0.0
    collapse_count = 0
    desync_sum = 0.0
    desync_count = 0

    for payload in logs.values():
        for entry in _iter_v_entries(payload):
            tags = entry.get("tags") or []
            if isinstance(tags, str):
                tags = [tags]
            for t in tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1

            ec = entry.get("emotional_collapse", 0.0)
            try:
                ec_val = float(ec)
                collapse_sum += ec_val
                collapse_count += 1
            except Exception:
                pass

            rd = entry.get("rhythm_desync", 0.0)
            try:
                rd_val = float(rd)
                desync_sum += rd_val
                desync_count += 1
            except Exception:
                pass

    dominant_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    avg_collapse = collapse_sum / collapse_count if collapse_count > 0 else 0.0
    avg_desync = desync_sum / desync_count if desync_count > 0 else 0.0

    # 3) Essence Word 기본 결정 (logs + VXYZ)
    essence_word = None
    notes_ew = []

    if dominant_tags:
        essence_word = dominant_tags[0][0]
        notes_ew.append(f"Chosen from dominant tag '{essence_word}'.")
    elif Z_candidates:
        first_label = Z_candidates[0].get("label") or Z_candidates[0].get("id")
        if first_label:
            essence_word = str(first_label).split()[0]
            notes_ew.append(f"Derived from Z candidate label '{first_label}'.")
    if not essence_word:
        essence_word = context_lower or "flow"
        notes_ew.append("Fallback to context-based essence word.")

    # 기본 confidence
    has_logs = bool(logs)
    has_vxyz = bool(vxyz_projection_inner)
    if has_logs and has_vxyz:
        essence_conf = "high"
    elif has_logs or has_vxyz:
        essence_conf = "medium"
    else:
        essence_conf = "low"

    # 3b) CollapseEngine essence 적용
    if collapse_inner:
        ess = collapse_inner.get("essence") or {}
        ce_word = ess.get("word")
        ce_conf = ess.get("confidence")
        if ce_word:
            if ce_word != essence_word:
                notes_ew.append(
                    f"Overridden by CollapseEngine essence '{ce_word}' (prev='{essence_word}')."
                )
            else:
                notes_ew.append("CollapseEngine confirmed the chosen essence word.")
            essence_word = ce_word
            if ce_conf:
                essence_conf = ce_conf
            elif essence_conf == "low":
                essence_conf = "medium"

    # 4) Path Direction 계산
    direction_label = "stay"
    if context_lower == "emotion":
        if avg_collapse > 0.6:
            direction_label = "protect_boundary"
        elif avg_collapse > 0.2:
            direction_label = "stabilize"
        else:
            direction_label = "deepen"
    elif context_lower == "trading":
        if tempo == "compressed":
            direction_label = "prepare_to_act"
        elif tempo == "extended":
            direction_label = "wait"
        else:
            direction_label = "hold"
    elif context_lower == "design":
        direction_label = "explore"
    elif context_lower == "evaluation":
        direction_label = "rank_and_adjust"
    else:
        direction_label = "stay"

    if has_logs or has_vxyz:
        direction_conf = "medium"
        if has_logs and has_vxyz:
            direction_conf = "high"
    else:
        direction_conf = "low"

    # 5) Timing 계산
    if phase == "early_cycle":
        timing_window = "wait"
    elif phase == "mid_cycle":
        timing_window = "this_cycle"
    elif phase == "late_cycle":
        timing_window = "now"
    else:
        timing_window = "neutral"

    if tempo == "compressed":
        phase_alignment = "with_phase"
    elif tempo == "extended":
        phase_alignment = "against_phase"
    else:
        phase_alignment = "neutral"

    timing_notes = [
        f"Phase={phase}, Tempo={tempo}, Collapse={avg_collapse:.2f}, Desync={avg_desync:.2f}"
    ]

    # 6) Coordinate 계산
    tp_keyword = essence_word
    if Z_candidates:
        anchor = Z_candidates[0].get("id") or Z_candidates[0].get("horizon") or "Z1"
    else:
        anchor = "manual"

    conditions = [
        "Coordinate is advisory, not absolute.",
        "Human (Pioneer-001) may override TP or Direction at any time.",
    ]

    flowgraph_inner = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": context_lower,
        "input_snapshot": {
            "rhythm": {
                "phase": phase,
                "tempo": tempo,
            },
            "Z_candidates": [
                {"id": z.get("id"), "label": z.get("label")}
                for z in Z_candidates
            ],
            "emotion": {
                "dominant_tags": [t for t, _ in dominant_tags[:5]],
                "avg_collapse": avg_collapse,
                "avg_desync": avg_desync,
            },
        },
        "essence_word": {
            "value": essence_word,
            "confidence": essence_conf,
            "notes": notes_ew,
        },
        "path": {
            "direction": {
                "label": direction_label,
                "confidence": direction_conf,
            },
            "timing": {
                "window": timing_window,
                "phase_alignment": phase_alignment,
                "notes": timing_notes,
            },
            "coordinate": {
                "tp_keyword": tp_keyword,
                "structural_anchor": anchor,
                "conditions": conditions,
            },
        },
        "notes": [
            "FlowGraph Engine v1.0 (Season 7) — Flow → Path converter.",
            "Essence Word is now aligned with CollapseEngine output when available.",
            "Use direction/timing as guidance, not rigid rule.",
        ],
    }

    out = {"flowgraph": flowgraph_inner}
    out_path = root / "flowgraph_output.json"
    write_json(out_path, out)
    log(f"FlowGraph output written → {out_path} (direction={direction_label}, timing={timing_window})")

    return out


# -------------------------------------------------------------
# PULSE RE-INGEST
# -------------------------------------------------------------
def pulse_reingest(root: Path, pulse_weights: Dict[str, float]) -> None:
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
def run_autoboot(root: Path) -> None:
    p = root / "lypha_os_autoboot.yaml"
    data = load_yaml(p)
    if not data:
        log("Autoboot file not found.")
        return

    autoboot = data.get("autoboot", data)
    load_list = autoboot.get("load", [])

    log("Autoboot Modules (v16.0):")
    for m in load_list:
        log(f"  - {m}")

    load_str = " ".join(map(str, load_list))
    if "emotion_router" in load_str:
        log("Emotion Router ACTIVE — Gravity-Lock Enabled")
    if "emotion_circuit_portal" in load_str:
        log("Emotion Circuit ACTIVE — Pulse-Link Online")

    log("=== Autoboot 완료 (v16.0 Hyper-Init) ===")


def run_autoload(root: Path) -> str:
    p = root / "autoload.yaml"
    data = load_yaml(p)
    if not data:
        run_autoboot(root)
        return "neutral"

    auto = data.get("autoload", data)
    msg = auto.get("on_start", {}).get("message")
    log(f"on_start: {msg}")

    run_autoboot(root)
    return detect_context(msg or "")


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
def main() -> None:
    here = Path(__file__).resolve().parent
    log("Lypha-OS Kernel v16.0 Start — Season 7 CORE+ (Z-Core + VerifiedLoop + VXYZ + Collapse + DualOutcome + FlowGraph, Path-Hardened)")
    log(f"Script directory: {here}")

    root = auto_unzip(here)
    log(f"Lypha-OS root resolved to: {root}")
    os.chdir(root)

    # 정책 로딩
    policy_path = root / "policy" / "kernel_policy_v16.json"
    if not policy_path.exists():
        policy_path = root / "policy" / "kernel_policy_v15.json"
    if not policy_path.exists():
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

    # 1) Verified Structure Loop Engine으로 Z’ + policy 튜닝
    policy = auto_patch_Z_and_policy(root, policy, logs, ctx)

    # 2) VXYZ Extended Engine으로 rhythm/phase projection 생성
    vxyz_projection = run_vxyz_engine(root, logs, ctx)
    vxyz_inner = (vxyz_projection or {}).get("vxyz_projection")

    # 3) CollapseEngine으로 Essence Word 후보 생성 (Flow → Essence)
    collapse_output = run_collapse_engine(root, logs, vxyz_inner, ctx)
    collapse_inner = (collapse_output or {}).get("collapse_output")

    # 4) DualOutcome Simulation Engine으로 성공/실패 Risk Envelope 생성
    dual_sim_output = run_dualoutcome_engine(root, logs, vxyz_inner, ctx)
    dual_inner = (dual_sim_output or {}).get("dual_sim_output")

    # 5) FlowGraph Engine으로 Flow→Path 생성 (Collapse + VXYZ 반영)
    flowgraph_output = run_flowgraph_engine(root, logs, vxyz_inner, collapse_inner, ctx)
    flowgraph_inner = (flowgraph_output or {}).get("flowgraph")

    # 6) Cognitive Graph & Pulse 계산 (VXYZ + Collapse + FlowGraph + DualOutcome 포함)
    graph = build_graph(ctx, policy, logs, vxyz_inner, flowgraph_inner, collapse_inner)
    if dual_inner:
        risk = dual_inner.get("risk_envelope", {}) or {}
        graph["dual_outcome"] = {
            "recommended_stance": risk.get("recommended_stance"),
            "capacity_fit": risk.get("capacity_fit"),
            "width": risk.get("width"),
            "skew": risk.get("skew"),
        }

    pulse_weights = extract_pulse_weights(graph)

    print_cognitive_graph(graph)
    log(f"Pulse Weights: {pulse_weights}")

    # 7) 1차: 정렬된 Full Ingest + Z₀ + README Origin
    full_ingest(root, policy)

    # 8) 2차: Pulse 가중치 기반 Re-ingest (Speak4D / Math / Collapse / FlowGraph 등)
    pulse_reingest(root, pulse_weights)

    # 9) FlowGraph 문서가 있다면 한 번 더 ingest (보강)
    fgfile = load_flowgraph_file(root)
    if fgfile is not None:
        log(f"FlowGraph Document Detected: {fgfile}")
        ingest_file(fgfile)

    save_state(root, ctx)
    run_autoload(root)

    log("Lypha-OS Kernel v16.0 Complete — Season 7 CORE+ Runtime Active (Origin+ZYX+VerifiedLoop+VXYZ+Collapse+DualOutcome+FlowGraph+Speak4D+Math).")


if __name__ == "__main__":
    main()
