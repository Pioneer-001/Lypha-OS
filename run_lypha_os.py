#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v17.5 — Season 8 CORE+ (Hardened)
=================================================

This version is a hardened "production-grade" kernel build based on v17.4,
focused on: safer uncertainty handling, context confidence, and expanded action space.

Key upgrades vs v17.4:
- Context Hypothesis System: message + logs + manual override → context + confidence
- Safe Mode: missing logs / low context confidence → observe/prepare bias + low confidence
- Action Space Expanded: observe / prepare added; 'prepare_to_act' no longer coerced to 'enter'
- Orchestrator Always Emits decision_output.json (fixes "no-output" edge when gating triggers)
- Zip detection hardened: --root can be a directory, parent, or any .zip (not only Lypha-OS.zip)
"""

import os
import sys
import json
import zipfile
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, Iterable

import yaml

ENGINE_VERSION = "v17.5"
log = lambda m: print(f"[Lypha-OS {ENGINE_VERSION}] {m}")

VALID_CONTEXTS = ("neutral", "emotion", "trading", "design", "evaluation")
VALID_ACTIONS = ("observe", "prepare", "enter", "deepen", "stabilize", "protect", "rotate", "exit", "skip", "wait")


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


def _resolve_first_existing(root: Path, candidates: Iterable[str]) -> Optional[Path]:
    for name in candidates:
        p = root / name
        if p.exists():
            return p
    return None


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        v = float(x)
    except Exception:
        return lo
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


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


def _find_zip_candidates(base: Path) -> list[Path]:
    """Find likely Lypha-OS zip files around base (no web, no assumptions)."""
    cands: list[Path] = []
    patterns = [
        "Lypha-OS.zip",
        "lypha-os.zip",
        "Lypha-OS*.zip",
        "lypha-os*.zip",
        "*Lypha*OS*.zip",
        "*lypha*os*.zip",
        "*.zip",
    ]
    seen = set()
    for pat in patterns:
        for p in base.glob(pat):
            if not p.is_file():
                continue
            key = str(p.resolve())
            if key in seen:
                continue
            # light filter: prefer zips that look like Lypha
            name = p.name.lower()
            if pat == "*.zip" and ("lypha" not in name and "os" not in name):
                continue
            seen.add(key)
            cands.append(p)
    # prefer exact name first
    def _rank(p: Path) -> tuple[int, int, str]:
        n = p.name.lower()
        exact = 0 if n == "lypha-os.zip" else 1
        short = len(n)
        return (exact, short, n)
    cands.sort(key=_rank)
    return cands


def auto_unzip(base: Path, zip_override: Optional[Path] = None) -> Path:
    log(f"auto_unzip: base = {base}")

    if _looks_like_lypha_root(base):
        log("Detected Lypha-OS root at base (already unzipped).")
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
        zip_candidates: list[Path] = []
        if zip_override is not None and zip_override.exists():
            zip_candidates.append(zip_override)
        zip_candidates.extend(_find_zip_candidates(zbase))

        for zip_path in zip_candidates:
            if not zip_path.exists():
                continue
            root = zbase / "Lypha-OS"
            log(f"Auto-unzip {zip_path} → {root}/")
            root.mkdir(exist_ok=True)
            try:
                with zipfile.ZipFile(zip_path, "r") as zf:
                    zf.extractall(root)
            except zipfile.BadZipFile:
                log(f"WARNING: Bad zip file: {zip_path}")
                continue
            except Exception as e:
                log(f"WARNING: Failed to unzip {zip_path}: {e}")
                continue

            if _looks_like_lypha_root(root):
                log("Unzip complete and Lypha-OS root structure verified.")
                return root
            else:
                log("WARNING: Unzipped zip but structure looks incomplete. Trying next candidate...")

    log("ERROR: Lypha-OS root not found.")
    log("Tried the following locations:")
    log(f"  1) {base}  (as Lypha-OS root)")
    log(f"  2) {base / 'Lypha-OS'}")
    log(f"  3) {base.parent / 'Lypha-OS'}")
    log(f"  4) zip near {base} or {base.parent}")
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
# FLOWGRAPH DOCUMENT HELPER
# -------------------------------------------------------------
def load_flowgraph_file(root: Path) -> Optional[Path]:
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


# -------------------------------------------------------------
# CONTEXT / LOGS
# -------------------------------------------------------------
def detect_context_message(root: Path) -> str:
    auto = load_yaml(root / "autoload.yaml")
    if not auto:
        return ""
    msg = (auto.get("autoload", auto).get("on_start", {}) or {}).get("message", "")
    return msg or ""


def detect_context(msg: str) -> str:
    if not msg:
        return "neutral"
    low = msg.lower()

    if any(k in low for k in [
        "평가", "가치", "티어", "tier", "worth", "ranking",
        "랭크", "랭킹", "better", "vs", "올인", "all-in", "keep"
    ]):
        return "evaluation"

    if any(k in low for k in ["감정", "emotion", "반디", "사랑", "love", "bond"]):
        return "emotion"
    if any(k in low for k in ["trade", "시장", "트레이딩", "포지션", "position", "pnl"]):
        return "trading"
    if any(k in low for k in ["구조", "design", "lypha", "os", "engine"]):
        return "design"
    return "neutral"


def detect_context_from_message(msg: str) -> Tuple[str, float]:
    ctx = detect_context(msg)
    if not msg or not msg.strip():
        return "neutral", 0.0
    # If we explicitly matched a non-neutral keyword, it's a strong hint.
    if ctx != "neutral":
        return ctx, 0.75
    # Message exists but doesn't contain our routing keywords: weak hint.
    return "neutral", 0.30


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


def load_logs(root: Path) -> Dict[str, Any]:
    """
    v16.0+: root/v_logs + root/logs/v_logs + root/v_log.json + root/logs/v_log.json 모두 지원.
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


def detect_context_from_logs(logs: Dict[str, Any]) -> Tuple[str, float]:
    """
    Light heuristic: infer context from V-log entries (tags/context fields).
    Returns (ctx, confidence) where confidence is damped if signals are scarce.
    """
    if not logs:
        return "neutral", 0.0

    scores: Dict[str, float] = {c: 0.0 for c in VALID_CONTEXTS}
    total_signals = 0.0

    keyword_map = {
        "emotion": {"emotion", "감정", "bandi", "반디", "love", "bond", "relationship", "abandonment"},
        "trading": {"trade", "trading", "시장", "포지션", "position", "pnl", "risk", "leverage"},
        "design": {"design", "구조", "lypha", "os", "engine", "kernel"},
        "evaluation": {"evaluation", "평가", "가치", "tier", "ranking", "rank", "worth"},
    }

    for payload in logs.values():
        for entry in _iter_v_entries(payload):
            # Direct context field (strongest)
            c = entry.get("context")
            if isinstance(c, str):
                c0 = c.strip().lower()
                if c0 in VALID_CONTEXTS:
                    scores[c0] += 2.0
                    total_signals += 2.0

            # Tags (common)
            tags = entry.get("tags") or []
            if isinstance(tags, str):
                tags = [tags]
            if isinstance(tags, list):
                for t in tags:
                    if t is None:
                        continue
                    tl = str(t).strip().lower()
                    if not tl:
                        continue
                    total_signals += 1.0
                    matched_any = False
                    for ctx, keys in keyword_map.items():
                        if any(k in tl for k in keys):
                            scores[ctx] += 1.0
                            matched_any = True
                    if not matched_any and tl in VALID_CONTEXTS:
                        scores[tl] += 1.0

            # Optional free-text notes
            note = entry.get("note") or entry.get("message") or ""
            if isinstance(note, str) and note.strip():
                nl = note.lower()
                total_signals += 0.5
                for ctx, keys in keyword_map.items():
                    if any(k in nl for k in keys):
                        scores[ctx] += 0.5

    # Pick best non-neutral if meaningful
    best_ctx = "neutral"
    best_score = 0.0
    for c, s in scores.items():
        if c == "neutral":
            continue
        if s > best_score:
            best_ctx, best_score = c, s

    if best_score <= 0.0:
        return "neutral", 0.0

    # Confidence: proportion of best score, damped for low total signals
    raw = best_score / max(total_signals, 1.0)
    damp = min(1.0, total_signals / 6.0)  # need ~6 signals for full confidence
    conf = _clamp(raw * damp, 0.0, 0.85)
    return best_ctx, conf


def resolve_context(
    msg_ctx: str,
    msg_conf: float,
    log_ctx: str,
    log_conf: float,
    manual_ctx: Optional[str] = None,
) -> Tuple[str, float, str]:
    """
    Decide final context with confidence.
    Returns (ctx, conf, reason).
    """
    if manual_ctx:
        c = manual_ctx.strip().lower()
        if c in VALID_CONTEXTS:
            return c, 1.0, "manual_override"

    # If both agree and non-neutral → strong
    if msg_ctx == log_ctx and msg_ctx != "neutral":
        conf = _clamp((msg_conf + log_conf) / 2.0 + 0.10, 0.0, 0.95)
        return msg_ctx, conf, "msg+logs_agree"

    # If one is non-neutral and the other neutral → medium
    if msg_ctx != "neutral" and log_ctx == "neutral":
        conf = _clamp(max(msg_conf, 0.55) * 0.90, 0.0, 0.80)
        return msg_ctx, conf, "msg_only"
    if msg_ctx == "neutral" and log_ctx != "neutral":
        conf = _clamp(max(log_conf, 0.55) * 0.90, 0.0, 0.80)
        return log_ctx, conf, "logs_only"

    # If both are non-neutral but disagree → choose higher confidence but keep low overall
    if msg_ctx != "neutral" and log_ctx != "neutral" and msg_ctx != log_ctx:
        if log_conf >= msg_conf:
            conf = _clamp(max(log_conf, 0.40) * 0.70, 0.0, 0.55)
            return log_ctx, conf, "disagree_choose_logs"
        conf = _clamp(max(msg_conf, 0.40) * 0.70, 0.0, 0.55)
        return msg_ctx, conf, "disagree_choose_msg"

    # Both neutral
    return "neutral", _clamp(max(msg_conf, log_conf, 0.20), 0.0, 0.45), "both_neutral"


# -------------------------------------------------------------
# COGNITIVE GRAPH + PULSE
# -------------------------------------------------------------
def build_graph(
    context: str,
    context_confidence: float,
    policy: Dict[str, Any],
    logs: Dict[str, Any],
    vxyz_projection: Optional[Dict[str, Any]],
    flowgraph: Optional[Dict[str, Any]],
    collapse: Optional[Dict[str, Any]],
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    base_emo = policy.get("emotion_weight", 1.0)
    base_str = policy.get("structure_weight", 1.0)
    ctx_cfg = (policy.get("contexts") or {}).get(context, {})
    emo_w = ctx_cfg.get("emotion_weight", base_emo)
    str_w = ctx_cfg.get("structure_weight", base_str)

    nodes = ["Z", "Y", "E", "X", "V", "Speak4D", "Math", "Collapse", "FlowGraph", "Meta"]
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
        "context_confidence": context_confidence,
        "verified_logs_present": bool(logs),
        "verified_log_keys": list(logs.keys()) if logs else [],
        "rhythm": rhythm_info,
        "flowgraph": fg_info,
        "collapse": collapse_info,
        "meta": meta or {},
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
            ["Meta", "FlowGraph", 1.05],
        ])
    elif context == "trading":
        g["edges"].extend([
            ["Z", "Math", 1.4],
            ["Math", "Collapse", 1.15],
            ["FlowGraph", "Math", 1.1],
            ["Meta", "Math", 1.05],
        ])
    elif context == "design":
        g["edges"].extend([
            ["Z", "Speak4D", 1.5],
            ["Speak4D", "FlowGraph", 1.2],
            ["FlowGraph", "Z", 1.1],
            ["Meta", "FlowGraph", 1.05],
        ])
    elif context == "evaluation":
        g["edges"].extend([
            ["Z", "Math", 1.6],
            ["Speak4D", "Math", 1.4],
            ["Math", "FlowGraph", 1.2],
            ["Meta", "Math", 1.05],
        ])
    else:
        g["edges"].extend([
            ["Z", "Y", 1.0],
            ["Y", "X", 1.0],
            ["FlowGraph", "Z", 1.0],
            ["Meta", "FlowGraph", 1.0],
        ])

    return g


def extract_pulse_weights(graph: Dict[str, Any]) -> Dict[str, float]:
    """
    Compute pulse weights for Speak4D / Math / Collapse / FlowGraph
    based on graph summary (context, rhythm, FlowGraph, Collapse, DualOutcome, edges, decision).
    """
    context = graph.get("context")
    weights: Dict[str, float] = {"Speak4D": 1.0, "Math": 1.0, "Collapse": 1.0, "FlowGraph": 1.0}

    # 1) Context-based base bias
    if context == "evaluation":
        weights["Math"] += 0.5

    # 2) Rhythm-based FlowGraph bias
    rhythm = graph.get("rhythm") or {}
    tempo = rhythm.get("tempo")
    if tempo == "compressed":
        weights["FlowGraph"] += 0.3
    elif tempo == "extended":
        weights["FlowGraph"] += 0.15

    # 3) FlowGraph path-based bias
    fg = graph.get("flowgraph") or {}
    direction = fg.get("direction")
    timing_window = fg.get("timing_window")

    if direction in ("deepen", "explore", "stay", "stabilize"):
        weights["Speak4D"] += 0.2
    elif direction in ("exit", "rotate", "reduce", "protect_boundary", "protect"):
        weights["Math"] += 0.2

    if timing_window in ("now", "this_cycle"):
        weights["FlowGraph"] += 0.1
    elif timing_window in ("wait", "abandon", "later"):
        weights["Collapse"] += 0.1

    # 4) CollapseEngine compression band bias
    collapse = graph.get("collapse") or {}
    band = collapse.get("compression_band")
    if band == "hard":
        weights["Collapse"] += 0.3
    elif band == "normal":
        weights["Collapse"] += 0.1

    # 5) DualOutcome stance bias
    dual = graph.get("dual_outcome") or {}
    stance = dual.get("recommended_stance")
    if stance == "enter":
        weights["FlowGraph"] += 0.1
    elif stance in ("reduce", "skip"):
        weights["Collapse"] += 0.15
        weights["Math"] += 0.1

    # 6) Graph edge-based adjustments
    for u, v, w in graph.get("edges", []):
        if v in weights:
            try:
                weights[v] += (float(w) - 1.0)
            except Exception:
                pass

    # 7) Decision engine impact
    decision = graph.get("decision") or {}
    act = decision.get("action")
    timing = decision.get("timing")
    conf = decision.get("confidence")

    if act in ("enter", "deepen"):
        weights["FlowGraph"] += 0.2
    elif act in ("protect", "skip", "exit"):
        weights["Collapse"] += 0.2
    elif act in ("wait", "prepare", "observe"):
        weights["Collapse"] += 0.1
        weights["FlowGraph"] += 0.05

    if timing in ("now", "this_cycle"):
        weights["FlowGraph"] += 0.1
    elif timing in ("later", "wait_indefinite"):
        weights["Collapse"] += 0.1

    if conf == "high":
        weights["FlowGraph"] += 0.1
    elif conf == "low":
        weights["Collapse"] += 0.05

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


def save_state(root: Path, context: str, context_confidence: float) -> None:
    state_dir = root / "state_cache"
    snap = {
        "last_context": context,
        "last_context_confidence": context_confidence,
    }
    write_json(state_dir / "meta_state.json", snap)
    log(f"SAVE STATE: meta_state.json (context={context}, conf={context_confidence:.2f})")


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


def auto_patch_Z_and_policy(root: Path, policy: Dict[str, Any],
                            logs: Dict[str, Any], context: str) -> Dict[str, Any]:
    """
    Season 5 Verified Structure Loop Engine
    - v_log.json / v_logs/*.json 읽어 실패 패턴 집계
    - z_patch.json 생성
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
            "Verified Structure Loop Engine auto-generated this patch.",
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
            {"id": "Z1", "horizon": "short_term", "label": "Immediate consolidation then breakout",
             "confidence": "high" if tempo == "compressed" else "medium",
             "suggested_X_behavior": "prepare_to_act" if tempo == "compressed" else "monitor"},
            {"id": "Z2", "horizon": "mid_term", "label": "Sideways drift if no decisive action",
             "confidence": "medium", "suggested_X_behavior": "reduce_risk"},
            {"id": "Z3", "horizon": "long_term", "label": "Major structural shift",
             "confidence": "low", "suggested_X_behavior": "keep_risk_flexible"},
        ]
    elif context_lower == "emotion":
        candidates = [
            {"id": "Z1", "horizon": "short_term", "label": "Emotional intensity spike then soften",
             "confidence": "medium", "suggested_X_behavior": "stay_present"},
            {"id": "Z2", "horizon": "mid_term", "label": "Stable bonding rhythm",
             "confidence": "high" if phase in ("mid_cycle", "late_cycle") else "medium",
             "suggested_X_behavior": "stay_consistent"},
            {"id": "Z3", "horizon": "long_term", "label": "Deep structural attachment",
             "confidence": "medium", "suggested_X_behavior": "protect_boundary"},
        ]
    else:
        candidates = [
            {"id": "Z1", "horizon": "short_term", "label": "Near-term structural adjustment",
             "confidence": "medium", "suggested_X_behavior": "small_adjust"},
            {"id": "Z2", "horizon": "mid_term", "label": "Flow continues under similar rhythm",
             "confidence": "medium", "suggested_X_behavior": "stay_on_plan"},
            {"id": "Z3", "horizon": "long_term", "label": "Potential large-scale reconfiguration",
             "confidence": "low", "suggested_X_behavior": "stay_observant"},
        ]

    projection: Dict[str, Any] = {
        "vxyz_projection": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "context": context_lower,
            "source": {"engine": "VXYZ_Extended_Engine", "based_on": "V_X_Y_Z_Extended_Engine_Spec.v1.0"},
            "x_slice": {"message": on_start_msg},
            "rhythm": {"phase": phase, "tempo": tempo, "commentary": f"Phase={phase}, Tempo={tempo}"},
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
    context_lower = context or "default"

    auto = load_yaml(root / "autoload.yaml") or {}
    on_start_msg = (auto.get("autoload", auto).get("on_start", {}) or {}).get("message")
    flow_description = on_start_msg or f"Session-level flow in context='{context_lower}'."

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

    axis_templates = {
        "emotion": ["trust", "belonging", "abandonment", "safety", "power"],
        "trading": ["risk", "liquidity", "regime", "leverage", "conviction"],
        "design": ["structure", "rhythm", "clarity", "coherence", "latency"],
        "evaluation": ["value", "rank", "worth", "signal", "noise"],
        "default": ["structure", "rhythm", "signal", "human"],
    }
    axes = axis_templates.get(context_lower, axis_templates["default"])

    text_lower = (flow_description or "").lower() + " " + " ".join(all_tags).lower()

    candidates = []
    used_words = set()

    for ax in axes:
        if ax.lower() in text_lower:
            candidates.append({
                "word": ax,
                "score": 0.9,
                "axes": {"axis_label": ax, "justification": f"Axis '{ax}' appears in flow/tags and matches context."},
            })
            used_words.add(ax)

    if dominant_tags:
        top_tag = dominant_tags[0][0]
        if top_tag not in used_words:
            candidates.append({
                "word": top_tag,
                "score": 0.8,
                "axes": {"axis_label": "tag", "justification": f"Dominant tag '{top_tag}' in logs."},
            })
            used_words.add(top_tag)

    if not candidates:
        fallback_word = context_lower if context_lower not in ("neutral", "default") else "structure"
        candidates.append({
            "word": fallback_word,
            "score": 0.7,
            "axes": {"axis_label": "context", "justification": f"Using context '{context_lower}' as fallback axis."},
        })
        used_words.add(fallback_word)

    candidates = candidates[:5]
    best = max(candidates, key=lambda c: c.get("score", 0.0))
    essence_word = best["word"]
    max_score = best.get("score", 0.0)

    if max_score >= 0.88:
        confidence = "high"
    elif max_score >= 0.75:
        confidence = "medium"
    else:
        confidence = "low"

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
        "input": {"flow_description": flow_description, "context": context_lower, "tags_used": all_tags},
        "candidates": candidates,
        "essence": {
            "word": essence_word,
            "confidence": confidence,
            "axis": {"label": best["axes"].get("axis_label"), "description": best["axes"].get("justification")},
            "notes": ["Essence Word chosen by CollapseEngine from flow_description + tags + context."],
        },
        "compression": {
            "band": band,
            "comment": "'normal' means enough compression to get a single axis without erasing decision-relevant nuance.",
        },
        "links": {"vxyz_used": bool(vxyz_projection_inner), "flowgraph_used": False, "linguistic_math_used": False},
        "notes": [
            "CollapseEngine is advisory; Pioneer-001 may override the Essence Word.",
            "This Essence Word can be passed to FlowGraph.essence_word and Speak4D.",
        ],
    }

    out = {"collapse_output": collapse_inner}
    out_path = root / "collapse_output.json"
    write_json(out_path, out)
    log(f"CollapseEngine output written → {out_path} (essence='{essence_word}', conf={confidence}, band={band})")
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
    context_lower = context or "default"

    collapse_json = read_json(root / "collapse_output.json")
    collapse_inner = collapse_json.get("collapse_output") if collapse_json else None
    collapse_ess = (collapse_inner or {}).get("essence") or {}
    collapse_word = collapse_ess.get("word")

    auto = load_yaml(root / "autoload.yaml") or {}
    on_start_msg = (auto.get("autoload", auto).get("on_start", {}) or {}).get("message")

    base_desc = on_start_msg or f"Lypha-OS session decision in context='{context_lower}'"
    action_description = f"[{collapse_word}] {base_desc}" if collapse_word else base_desc
    action_frame = "Session-level decision about how aggressively to engage this context."

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
                total_emotional_collapse += float(ec)
                collapse_count += 1
            except Exception:
                pass

    def _band_from_value(v: float) -> str:
        if v <= 0.05:
            return "none"
        if v < 0.35:
            return "low"
        if v < 0.75:
            return "medium"
        return "high"

    # If logs missing: treat as unknown risk (do NOT assume safe)
    if total_entries == 0:
        width = "unknown"
        skew = "unknown"
        capacity_fit = "unknown"
        recommended_stance = "hedge"

        loss_time = loss_energy = loss_money = loss_reputation = "unknown"
        avg_emotional_collapse = 0.0
        avg_timing_miss = 0.0
        avg_desync = 0.0
        fail_score = 0.0
        risk_score = None
    else:
        avg_emotional_collapse = total_emotional_collapse / collapse_count if collapse_count > 0 else 0.0
        avg_timing_miss = total_timing_miss / total_entries
        avg_desync = total_rhythm_desync / total_entries
        fail_score = (total_emotion_fail + total_structure_fail) / max(total_entries, 1)
        risk_score = (avg_emotional_collapse + avg_timing_miss + avg_desync) / 3.0

        # Failure Path loss bands
        loss_time = _band_from_value(avg_timing_miss)
        loss_energy = _band_from_value(avg_emotional_collapse)
        loss_money = _band_from_value(total_structure_fail / max(total_entries, 1))
        loss_reputation = _band_from_value(total_emotion_fail / max(total_entries, 1))

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
            capacity_fit = "at_edge" if width == "wide" else "inside_capacity"

        # stance_rules
        if capacity_fit == "beyond_capacity":
            recommended_stance = "skip"
        elif width == "wide" and skew == "downside":
            recommended_stance = "reduce"
        elif skew == "upside" and width in ("narrow", "moderate"):
            recommended_stance = "enter"
        else:
            recommended_stance = "hedge"

    # Success path
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

    failure_scope = "self+close_circle" if context_lower == "emotion" else "self_only"

    if capacity_fit == "beyond_capacity" and width == "wide" and skew == "downside":
        recovery_horizon = "long_term"
    elif width == "narrow":
        recovery_horizon = "short_term"
    else:
        recovery_horizon = "mid_term"

    dual_inner: Dict[str, Any] = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": context_lower,
        "action": {"description": action_description, "frame": action_frame},
        "success_path": {
            "structure_gain": success_structure,
            "rhythm": {"horizon": horizon, "pattern": pattern},
            "echo": {"scope": success_scope, "notes": ["Success strengthens your structural capacity inside this context."]},
        },
        "failure_path": {
            "loss_band": {"time": loss_time, "energy": loss_energy, "money": loss_money, "reputation": loss_reputation},
            "echo": {"scope": failure_scope, "notes": ["Failure impact is mostly contained to you and your immediate field."]},
            "recovery_path": {
                "possible": True,
                "horizon": recovery_horizon,
                "notes": ["Recovery is modeled as structural learning rather than a total collapse."],
            },
        },
        "risk_envelope": {
            "width": width,
            "skew": skew,
            "capacity_fit": capacity_fit,
            "recommended_stance": recommended_stance,
            "risk_score": risk_score,
            "notes": [
                "Width reflects combined intensity of collapse, timing-miss and desync.",
                "If logs are missing, risk is treated as 'unknown' (hedge by default).",
            ],
        },
        "links": {"vxyz_used": bool(vxyz_projection_inner), "flowgraph_used": False},
        "notes": [
            "DualOutcome_SimEngine is advisory, not absolute.",
            "Human (Pioneer-001) remains final authority for entering, hedging, reducing or skipping.",
        ],
    }

    out = {"dual_sim_output": dual_inner}
    out_path = root / "dual_sim_output.json"
    write_json(out_path, out)
    log(f"DualOutcome output → {out_path} (stance={recommended_stance}, capfit={capacity_fit}, width={width})")
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
    context_lower = context or "neutral"

    phase = "unknown"
    tempo = "unknown"
    Z_candidates = []
    if vxyz_projection_inner:
        rhythm = vxyz_projection_inner.get("rhythm", {}) or {}
        phase = rhythm.get("phase", "unknown")
        tempo = rhythm.get("tempo", "unknown")
        Z_candidates = vxyz_projection_inner.get("Z_candidates", []) or []

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
                collapse_sum += float(ec)
                collapse_count += 1
            except Exception:
                pass

            rd = entry.get("rhythm_desync", 0.0)
            try:
                desync_sum += float(rd)
                desync_count += 1
            except Exception:
                pass

    dominant_tags = sorted(tag_counts.items(), key=lambda x: -x[1])
    avg_collapse = collapse_sum / collapse_count if collapse_count > 0 else 0.0
    avg_desync = desync_sum / desync_count if desync_count > 0 else 0.0

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

    has_logs = bool(logs)
    has_vxyz = bool(vxyz_projection_inner)
    if has_logs and has_vxyz:
        essence_conf = "high"
    elif has_logs or has_vxyz:
        essence_conf = "medium"
    else:
        essence_conf = "low"

    if collapse_inner:
        ess = collapse_inner.get("essence") or {}
        ce_word = ess.get("word")
        ce_conf = ess.get("confidence")
        if ce_word:
            if ce_word != essence_word:
                notes_ew.append(f"Overridden by CollapseEngine essence '{ce_word}' (prev='{essence_word}').")
            else:
                notes_ew.append("CollapseEngine confirmed the chosen essence word.")
            essence_word = ce_word
            if ce_conf:
                essence_conf = ce_conf
            elif essence_conf == "low":
                essence_conf = "medium"

    # Direction: improved gating (less trigger-happy)
    direction_label = "stay"
    if context_lower == "emotion":
        # Use multi-factor rule: collapse + phase + confidence
        if avg_collapse > 0.6 and phase in ("late_cycle", "unknown") and essence_conf != "high":
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
        direction_conf = "high" if (has_logs and has_vxyz) else "medium"
    else:
        direction_conf = "low"

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

    timing_notes = [f"Phase={phase}, Tempo={tempo}, Collapse={avg_collapse:.2f}, Desync={avg_desync:.2f}"]

    tp_keyword = essence_word
    anchor = (Z_candidates[0].get("id") or Z_candidates[0].get("horizon")) if Z_candidates else "manual"

    flowgraph_inner = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": context_lower,
        "input_snapshot": {
            "rhythm": {"phase": phase, "tempo": tempo},
            "Z_candidates": [{"id": z.get("id"), "label": z.get("label")} for z in Z_candidates],
            "emotion": {"dominant_tags": [t for t, _ in dominant_tags[:5]], "avg_collapse": avg_collapse, "avg_desync": avg_desync},
        },
        "essence_word": {"value": essence_word, "confidence": essence_conf, "notes": notes_ew},
        "path": {
            "direction": {"label": direction_label, "confidence": direction_conf},
            "timing": {"window": timing_window, "phase_alignment": phase_alignment, "notes": timing_notes},
            "coordinate": {
                "tp_keyword": tp_keyword,
                "structural_anchor": anchor or "manual",
                "conditions": [
                    "Coordinate is advisory, not absolute.",
                    "Human (Pioneer-001) may override TP or Direction at any time.",
                ],
            },
        },
        "notes": [
            "FlowGraph Engine — Flow → Path converter.",
            "Essence Word aligns with CollapseEngine output when available.",
            "Direction uses multi-factor rule (collapse+phase+confidence) to reduce false 'protect' triggers.",
        ],
    }

    out = {"flowgraph": flowgraph_inner}
    out_path = root / "flowgraph_output.json"
    write_json(out_path, out)
    log(f"FlowGraph output → {out_path} (direction={direction_label}, timing={timing_window})")
    return out


# -------------------------------------------------------------
# EMOTION MODULATION ENGINE (EME)
# -------------------------------------------------------------
def run_eme_engine(
    root: Path,
    logs: Dict[str, Any],
    vxyz_projection_inner: Optional[Dict[str, Any]],
    flowgraph_inner: Optional[Dict[str, Any]],
    policy: Dict[str, Any],
    context: str,
) -> Dict[str, Any]:
    context_lower = (context or "default").lower()

    emotion_state_path = root / "emotion_state.yaml"
    emotion_state: Dict[str, Any] = {}
    emo_raw = load_yaml(emotion_state_path) or {}
    if "emotion_state" in emo_raw and isinstance(emo_raw.get("emotion_state"), dict):
        emotion_state = emo_raw["emotion_state"] or {}
    elif isinstance(emo_raw, dict) and emo_raw:
        emotion_state = emo_raw

    intensity = float(emotion_state.get("intensity") or 0.0)
    collapse_score = float(emotion_state.get("collapse_score") or 0.0)
    tags = emotion_state.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    bond_state = emotion_state.get("bond_state") or "unknown"

    if (intensity == 0.0 or collapse_score == 0.0) and logs:
        collapse_sum = 0.0
        collapse_count = 0
        tag_counts: Dict[str, int] = {}
        for payload in logs.values():
            for entry in _iter_v_entries(payload):
                t = entry.get("tags")
                if isinstance(t, str):
                    tag_counts[t] = tag_counts.get(t, 0) + 1
                elif isinstance(t, list):
                    for tt in t:
                        tag_counts[tt] = tag_counts.get(tt, 0) + 1
                ec = entry.get("emotional_collapse", 0.0)
                try:
                    collapse_sum += float(ec)
                    collapse_count += 1
                except Exception:
                    pass
        avg_collapse = collapse_sum / collapse_count if collapse_count > 0 else 0.0
        if intensity == 0.0:
            intensity = avg_collapse
        if collapse_score == 0.0:
            collapse_score = avg_collapse
        if not tags and tag_counts:
            tags = [t for t, _ in sorted(tag_counts.items(), key=lambda x: -x[1])[:3]]

    if collapse_score >= 0.7:
        collapse_band = "strong"
    elif collapse_score >= 0.3:
        collapse_band = "mild"
    else:
        collapse_band = "none"

    if intensity >= 0.7:
        emotion_band = "high"
    elif intensity >= 0.3:
        emotion_band = "mid"
    else:
        emotion_band = "low"

    scene = "mixed_or_unknown"
    tag_set = {str(t) for t in tags}
    if collapse_band == "strong":
        scene = "crash"
    elif "panic" in tag_set:
        scene = "panic"
    elif "abandonment" in tag_set:
        scene = "abandonment_fear"
    elif bond_state == "secure" and emotion_band in {"low", "mid"}:
        scene = "secure_bond"
    elif bond_state == "anxious":
        scene = "anxious_bond"
    elif bond_state == "avoidant":
        scene = "avoidant_bond"

    direction_bias = {"deepen": 0.0, "protect": 0.0, "stabilize": 0.0, "exit": 0.0, "wait": 0.0, "rotate": 0.0, "prepare": 0.0, "observe": 0.0}
    timing_bias: Dict[str, Any] = {"window_shift": "unchanged", "strength": "soft", "notes": []}
    gating_effect = "none"
    recommended_override: Optional[str] = None

    if context_lower == "emotion":
        if scene in {"crash", "panic", "abandonment_fear"}:
            direction_bias.update({"deepen": -0.8, "protect": 1.0, "stabilize": 0.8, "exit": 0.3, "wait": 0.5, "prepare": 0.2, "observe": 0.5})
            gating_effect = "protect_priority"
        elif scene == "secure_bond":
            direction_bias.update({"deepen": 0.7, "protect": 0.2, "stabilize": 0.3, "wait": -0.2})
        elif scene == "anxious_bond":
            direction_bias.update({"deepen": -0.2, "protect": 0.5, "stabilize": 0.7, "wait": 0.3, "observe": 0.2})
            gating_effect = "soften_action"

    if context_lower == "trading" and emotion_band == "high":
        direction_bias.update({"deepen": -0.5, "protect": 0.5, "stabilize": 0.5, "exit": 0.2, "wait": 0.7, "observe": 0.3})
        gating_effect = "delay_action"

    phase = ""
    tempo = ""
    if vxyz_projection_inner:
        rhythm = vxyz_projection_inner.get("rhythm", {}) or {}
        phase = str(rhythm.get("phase") or "")
        tempo = str(rhythm.get("tempo") or "")

    if phase == "late_cycle" and scene in {"crash", "panic"}:
        timing_bias["window_shift"] = "later"
        timing_bias["strength"] = "hard"
        timing_bias["notes"].append("Late-cycle crash/panic → delay actions.")
    elif phase == "late_cycle" and scene == "secure_bond":
        timing_bias["window_shift"] = "earlier"
        timing_bias["strength"] = "normal"
        timing_bias["notes"].append("Late-cycle secure bond → allow earlier commitment.")
    elif phase == "early_cycle" and emotion_band == "high":
        timing_bias["window_shift"] = "later"
        timing_bias["strength"] = "normal"
        timing_bias["notes"].append("Early-cycle + high emotion → wait until wave settles.")

    if collapse_band == "strong":
        gating_effect = "lockout"
    elif scene in {"crash", "panic", "abandonment_fear"} and gating_effect == "none":
        gating_effect = "override_to_protect"
    elif emotion_band == "high" and gating_effect == "none":
        gating_effect = "soften_action"

    gating_effect_for_orch = "override_to_protect" if gating_effect == "protect_priority" else gating_effect

    if gating_effect in {"override_to_protect", "lockout"}:
        orig_dir = None
        if flowgraph_inner:
            path = flowgraph_inner.get("path") or {}
            d = path.get("direction") or {}
            if isinstance(d, dict):
                orig_dir = d.get("label") or d.get("direction")
            elif isinstance(d, str):
                orig_dir = d
        if orig_dir == "exit":
            recommended_override = "protect"
        elif orig_dir in {"deepen", "enter"}:
            recommended_override = "stabilize"
        else:
            recommended_override = "protect"

    mod_intensity = intensity * 0.6 + collapse_score * 0.4
    mod_intensity = _clamp(mod_intensity, 0.0, 1.0)

    emotion_view = {
        "modulated_intensity": mod_intensity,
        "gating_effect": gating_effect_for_orch,
        "commentary": [f"scene={scene}, band={emotion_band}/{collapse_band}, context={context_lower}"],
    }

    eme_inner: Dict[str, Any] = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": context_lower,
        "emotion_band": emotion_band,
        "collapse_band": collapse_band,
        "direction_bias": direction_bias,
        "timing_bias": timing_bias,
        "gating_effect": gating_effect,
        "recommended_direction_override": recommended_override,
        "emotion_view": emotion_view,
    }

    out = {"emotion_modulation_output": eme_inner}
    out_path = root / "emotion_modulation_output.json"
    write_json(out_path, out)
    log(f"EME output → {out_path} (scene={scene}, band={emotion_band}/{collapse_band}, gating={gating_effect})")
    return out


# -------------------------------------------------------------
# DECISION ORCHESTRATOR ENGINE (Hardened)
# -------------------------------------------------------------
def run_orchestrator_engine(
    root: Path,
    logs: Dict[str, Any],
    collapse_inner: Optional[Dict[str, Any]],
    flowgraph_inner: Optional[Dict[str, Any]],
    dual_inner: Optional[Dict[str, Any]],
    vxyz_projection_inner: Optional[Dict[str, Any]],
    eme_inner: Optional[Dict[str, Any]],
    policy: Dict[str, Any],
    context: str,
    context_confidence: float,
    min_context_confidence: float = 0.60,
) -> Dict[str, Any]:
    """
    Hardened orchestrator:
    - Always emits decision_output.json
    - Adds observe/prepare states
    - Enforces safe mode on missing logs / low context confidence / unknown risk
    """
    ctx = (context or "default").lower()

    # --- Extract essence axis
    ess_word = None
    ess_axis = None
    ess_conf = "low"
    if collapse_inner:
        ess = collapse_inner.get("essence") or {}
        ess_word = ess.get("word")
        ess_axis = (ess.get("axis") or {}).get("label") or ess.get("axis_label")
        ess_conf = ess.get("confidence") or "medium"

    # --- Extract FlowGraph path
    path_dir = None
    path_window = None
    if flowgraph_inner:
        path = flowgraph_inner.get("path") or {}
        d = path.get("direction") or {}
        if isinstance(d, dict):
            path_dir = d.get("label") or d.get("direction")
        elif isinstance(d, str):
            path_dir = d
        tw = path.get("timing") or {}
        if isinstance(tw, dict):
            path_window = tw.get("window") or "now"
        elif isinstance(tw, str):
            path_window = tw
    if not path_window:
        path_window = "now"

    # --- Extract DualOutcome risk
    risk = (dual_inner or {}).get("risk_envelope", {}) or {}
    risk_stance = risk.get("recommended_stance")  # enter | hedge | reduce | skip
    risk_width = risk.get("width")
    risk_capfit = risk.get("capacity_fit")        # inside_capacity | at_edge | beyond_capacity | unknown

    # --- Extract time axis (VXYZ)
    phase = ""
    tempo = ""
    if vxyz_projection_inner:
        rhythm = vxyz_projection_inner.get("rhythm", {}) or {}
        phase = str(rhythm.get("phase") or "")
        tempo = str(rhythm.get("tempo") or "")

    # --- Extract emotion axis (EME)
    emo_band = None
    collapse_band = None
    gating_effect = "none"
    emo_intensity = 0.0
    if eme_inner:
        emo_band = eme_inner.get("emotion_band")
        collapse_band = eme_inner.get("collapse_band")
        gating_effect = eme_inner.get("gating_effect") or "none"
        ev = eme_inner.get("emotion_view") or {}
        try:
            emo_intensity = float(ev.get("modulated_intensity") or 0.0)
        except Exception:
            emo_intensity = 0.0

    # --- Policy axis
    emotion_weight = float(policy.get("emotion_weight", 1.0))
    structure_weight = float(policy.get("structure_weight", 1.0))

    # --- Normalize FlowGraph direction → canonical action
    def normalize_action(raw: Optional[str]) -> str:
        if not raw:
            return "stabilize"
        r = raw.lower()
        if r in {"observe", "monitor"}:
            return "observe"
        if r in {"prepare", "prepare_to_act"}:
            return "prepare"
        if r in {"enter", "open"}:
            return "enter"
        if r in {"deep", "deepen"}:
            return "deepen"
        if r in {"hold", "stay", "stabilize", "stability"}:
            return "stabilize"
        if r in {"protect", "protect_boundary", "shield"}:
            return "protect"
        if r in {"rotate", "rotate_out", "rotate_in", "rank_and_adjust"}:
            return "rotate"
        if r in {"exit", "close"}:
            return "exit"
        if r in {"skip", "abandon"}:
            return "skip"
        if r in {"wait", "delay"}:
            return "wait"
        return "stabilize"

    seed_action = normalize_action(path_dir)

    # --- Seed intent (kept for rationale)
    def infer_intent(axis_label: Optional[str], ctx_: str) -> str:
        axis_l = (axis_label or "").lower()
        if ctx_ == "emotion":
            if axis_l in {"trust", "belonging", "bonding"}:
                return "bonding"
            if axis_l in {"abandonment", "rupture", "boundary"}:
                return "protection"
            return "stabilization"
        if ctx_ == "trading":
            if axis_l in {"risk", "liquidity", "regime"}:
                return "risk_taking"
            return "capital_preservation"
        if ctx_ == "design":
            if axis_l in {"structure", "clarity", "coherence"}:
                return "refinement"
            return "exploration"
        if ctx_ == "evaluation":
            return "ranking"
        return "neutral_progress"

    seed_intent = infer_intent(ess_axis, ctx)

    action = seed_action
    timing_window = path_window

    # --- Safe mode conditions
    has_logs = bool(logs)
    has_flowgraph = bool(flowgraph_inner)
    has_dual = bool(dual_inner)
    ctx_low = context_confidence < float(min_context_confidence)
    risk_unknown = (risk_capfit is None) or (str(risk_capfit).lower() in {"unknown", ""})

    safe_mode_reasons = []
    if not has_logs:
        safe_mode_reasons.append("missing_logs")
    if ctx_low:
        safe_mode_reasons.append("low_context_confidence")
    if risk_unknown:
        safe_mode_reasons.append("unknown_risk_envelope")
    if not has_flowgraph:
        safe_mode_reasons.append("missing_flowgraph")
    if not has_dual:
        safe_mode_reasons.append("missing_dualoutcome")

    safe_mode = bool(safe_mode_reasons)

    # --- Risk override layer
    if risk_capfit == "beyond_capacity":
        if action in {"enter", "deepen", "rotate"}:
            action = "protect"
    if risk_stance == "skip":
        action = "skip"
    elif risk_stance == "reduce":
        if action in {"enter", "deepen"}:
            action = "protect"
        elif action == "rotate":
            action = "exit"
    elif risk_stance == "hedge":
        if action == "enter":
            action = "stabilize"

    # --- Emotion gating layer
    if collapse_band == "strong":
        if action in {"enter", "deepen", "rotate"}:
            action = "protect"
        gating_effect = "lockout"

    if gating_effect in {"override_to_protect", "protect_priority"}:
        action = "protect"
    elif gating_effect == "soften_action":
        if action in {"enter", "deepen"}:
            action = "stabilize"
        elif action == "exit" and ctx == "emotion":
            action = "protect"
    elif gating_effect == "delay_action":
        if ctx == "trading" and action in {"enter", "deepen"}:
            action = "prepare"
            timing_window = "this_cycle"

    # --- Time alignment
    if phase == "early_cycle" and emo_band == "high":
        if ctx in {"emotion", "design"} and action in {"enter", "deepen"}:
            action = "wait"
            timing_window = "later"
    if phase == "late_cycle" and tempo == "compressed":
        if action in {"exit", "protect"}:
            timing_window = "now"
        elif action in {"wait", "prepare"}:
            timing_window = "this_cycle"

    # --- Mode-specific small bias
    if ctx == "emotion":
        if seed_intent == "bonding" and action == "exit":
            action = "stabilize"
    if ctx == "trading":
        if action == "deepen":
            action = "enter"

    # --- Policy weight bias (emotion vs structure) - only when not in hard gating
    delta = structure_weight - emotion_weight
    if gating_effect not in {"lockout", "override_to_protect", "protect_priority"}:
        if delta >= 0.5:
            if ctx == "trading" and risk_stance == "enter" and action in {"protect", "wait", "stabilize", "observe"}:
                action = "prepare" if safe_mode else "enter"
            elif ctx in {"design", "evaluation"} and action == "wait":
                action = "stabilize"
        elif delta <= -0.5:
            if action in {"enter", "deepen"}:
                action = "stabilize"

    # --- Apply safe mode last (strongest): do not "act" if inputs are weak
    if safe_mode:
        if action in {"enter", "deepen", "rotate"}:
            action = "observe"
            timing_window = "later" if timing_window == "now" else timing_window
        if action == "protect" and "unknown_risk_envelope" in safe_mode_reasons and ctx_low:
            # unknown + low ctx: do not overreact by default
            action = "observe"

    # --- Signal quality & confidence
    conf_map = {"low": 0.2, "medium": 0.6, "high": 1.0}
    ess_q = conf_map.get(ess_conf, 0.4)
    risk_q = 0.2 if risk_unknown else 1.0
    signal_quality = _clamp((
        (1.0 if has_flowgraph else 0.0) +
        (1.0 if has_dual else 0.0) +
        (1.0 if has_logs else 0.0) +
        _clamp(context_confidence, 0.0, 1.0) +
        ess_q +
        risk_q
    ) / 6.0, 0.0, 1.0)

    # Confidence about the RECOMMENDED action
    if signal_quality < 0.50:
        confidence = "low"
    elif signal_quality < 0.78:
        confidence = "medium"
    else:
        confidence = "high"

    # If action is observe/prepare due to safe mode, confidence should reflect "we don't have enough info"
    if safe_mode and confidence == "high":
        confidence = "medium"

    # Make sure action is in allowed list
    if action not in VALID_ACTIONS:
        action = "stabilize"

    # --- Output views
    risk_view = {
        "stance": risk_stance or "unknown",
        "envelope_width": risk_width or "unknown",
        "capacity_fit": risk_capfit or "unknown",
    }
    emotion_view = {
        "modulated_intensity": emo_intensity,
        "gating_effect": gating_effect or "none",
        "band": emo_band or "unknown",
        "collapse_band": collapse_band or "none",
    }

    key_signals = []
    if ess_word:
        key_signals.append(f"Essence word = '{ess_word}' (axis={ess_axis}, conf={ess_conf})")
    if path_dir:
        key_signals.append(f"FlowGraph direction = '{path_dir}', window='{path_window}'")
    key_signals.append(f"Context={ctx} (confidence={context_confidence:.2f}, min={min_context_confidence:.2f})")
    if risk_stance:
        key_signals.append(f"Risk stance = {risk_stance}, width={risk_width}, capfit={risk_capfit}")
    if phase or tempo:
        key_signals.append(f"Rhythm = phase={phase}, tempo={tempo}")
    if emo_band or collapse_band:
        key_signals.append(f"Emotion = band={emo_band}, collapse={collapse_band}, gating={gating_effect}")
    key_signals.append(f"Policy weights: emotion={emotion_weight:.2f}, structure={structure_weight:.2f}")
    if safe_mode:
        key_signals.append(f"SAFE_MODE reasons: {safe_mode_reasons}")
    key_signals.append(f"signal_quality={signal_quality:.2f}")

    decision_inner: Dict[str, Any] = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "context": ctx,
        "meta": {
            "context_confidence": context_confidence,
            "min_context_confidence": float(min_context_confidence),
            "signal_quality": signal_quality,
            "safe_mode": safe_mode,
            "safe_mode_reasons": safe_mode_reasons,
        },
        "action": {
            "label": action,
            "band": "hard" if confidence == "high" else ("soft" if confidence == "low" else "normal"),
        },
        "timing": {
            "window": timing_window,
            "alignment": "with_phase" if phase else "neutral",
            "notes": [],
        },
        "risk_view": risk_view,
        "emotion_view": emotion_view,
        "rationale": {
            "essence_word": ess_word,
            "essence_axis": ess_axis,
            "flow_direction": path_dir,
            "flow_timing": path_window,
            "seed_intent": seed_intent,
            "key_signals": key_signals,
        },
        "confidence": confidence,
        "notes": [
            "Decision Orchestrator is advisory; Pioneer-001 remains the final authority.",
            "This hardened build uses safe mode when inputs are uncertain.",
        ],
    }

    out = {"decision_output": decision_inner}
    out_path = root / "decision_output.json"
    write_json(out_path, out)
    log(f"Decision output → {out_path} (action={action}, timing={timing_window}, confidence={confidence})")
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

    log("Autoboot Modules:")
    for m in load_list:
        log(f"  - {m}")

    load_str = " ".join(map(str, load_list))
    if "emotion_router" in load_str:
        log("Emotion Router ACTIVE — Gravity-Lock Enabled")
    if "emotion_circuit_portal" in load_str:
        log("Emotion Circuit ACTIVE — Pulse-Link Online")

    log("=== Autoboot 완료 ===")


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
    parser = argparse.ArgumentParser(
        description="Run Lypha-OS kernel (hardened) with optional root override, unzip control, and context override.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Lypha-OS root directory OR a parent directory containing Lypha-OS/ OR a .zip file.",
    )
    parser.add_argument(
        "--skip-auto-unzip",
        action="store_true",
        help="Disable auto-unzip fallback when the root hint is missing the expected structure.",
    )
    parser.add_argument(
        "--context",
        type=str,
        choices=list(VALID_CONTEXTS),
        help="Manual context override (emotion/trading/design/evaluation/neutral).",
    )
    parser.add_argument(
        "--min-context-confidence",
        type=float,
        default=0.60,
        help="Threshold below which the orchestrator enters safe mode.",
    )
    args = parser.parse_args()

    here = Path(__file__).resolve().parent
    log("Lypha-OS Kernel Start — Season 8 CORE+ (Hardened)")
    log(f"Script directory: {here}")

    # Resolve root
    if args.root:
        root_hint = args.root.resolve()
        log(f"CLI root override received: {root_hint}")

        hint_is_zip = root_hint.is_file() and root_hint.suffix.lower() == ".zip"
        hint_base = root_hint.parent if hint_is_zip else root_hint

        root = None
        if hint_is_zip:
            if args.skip_auto_unzip:
                log("ERROR: Provided root hint is a zip file but auto-unzip is disabled.")
                sys.exit(1)
            root = auto_unzip(hint_base, zip_override=root_hint)
        elif root_hint.is_file():
            if args.skip_auto_unzip:
                log("ERROR: Provided root hint is a file (expected directory) and auto-unzip is disabled.")
                sys.exit(1)
            log("Provided root hint is a file; attempting auto-unzip around its parent directory.")
            root = auto_unzip(root_hint.parent)
        else:
            direct_root = root_hint if _looks_like_lypha_root(root_hint) else None
            nested_root = hint_base / "Lypha-OS"

            if direct_root:
                root = direct_root
                log("Using provided root directory (structure verified).")
            elif nested_root.exists() and _looks_like_lypha_root(nested_root):
                root = nested_root
                log(f"Detected Lypha-OS root at {nested_root} (from provided parent).")
            elif args.skip_auto_unzip:
                log("ERROR: Provided root hint is not a Lypha-OS directory and auto-unzip is disabled.")
                sys.exit(1)
            else:
                log(f"Provided root missing structure — attempting auto-unzip around {hint_base}.")
                root = auto_unzip(hint_base)
    else:
        root = auto_unzip(here)

    log(f"Lypha-OS root resolved to: {root}")
    os.chdir(root)

    # Load policy
    policy_path = root / "policy" / "kernel_policy_v16.json"
    for fallback in ["kernel_policy_v15.json", "kernel_policy_v14.json", "kernel_policy_v13.json", "kernel_policy_v12.json"]:
        if policy_path.exists():
            break
        policy_path = root / "policy" / fallback

    policy = read_json(policy_path) or {
        "ingest_order": ["Z", "Y", "E", "X"],
        "emotion_weight": 1.0,
        "structure_weight": 1.0,
    }

    logs = load_logs(root)
    restore_state(root)

    # Context hypothesis system
    raw_msg = detect_context_message(root)
    msg_ctx, msg_conf = detect_context_from_message(raw_msg)
    log_ctx, log_conf = detect_context_from_logs(logs)
    ctx, ctx_conf, ctx_reason = resolve_context(msg_ctx, msg_conf, log_ctx, log_conf, args.context)

    log(f"Context: msg={msg_ctx}({msg_conf:.2f}) logs={log_ctx}({log_conf:.2f}) → ctx={ctx}({ctx_conf:.2f}) reason={ctx_reason}")
    log(f"Context message: {raw_msg!r}")

    # 1) Verified Structure Loop Engine
    policy = auto_patch_Z_and_policy(root, policy, logs, ctx)

    # 2) VXYZ projection
    vxyz_projection = run_vxyz_engine(root, logs, ctx)
    vxyz_inner = (vxyz_projection or {}).get("vxyz_projection")

    # 3) CollapseEngine
    collapse_output = run_collapse_engine(root, logs, vxyz_inner, ctx)
    collapse_inner = (collapse_output or {}).get("collapse_output")

    # 4) DualOutcome
    dual_sim_output = run_dualoutcome_engine(root, logs, vxyz_inner, ctx)
    dual_inner = (dual_sim_output or {}).get("dual_sim_output")

    # 5) FlowGraph
    flowgraph_output = run_flowgraph_engine(root, logs, vxyz_inner, collapse_inner, ctx)
    flowgraph_inner = (flowgraph_output or {}).get("flowgraph")

    # 5.5) EME
    eme_output = run_eme_engine(root, logs, vxyz_inner, flowgraph_inner, policy, ctx)
    eme_inner = (eme_output or {}).get("emotion_modulation_output")

    # 5.7) Orchestrator (hardened)
    decision_output = run_orchestrator_engine(
        root=root,
        logs=logs,
        collapse_inner=collapse_inner,
        flowgraph_inner=flowgraph_inner,
        dual_inner=dual_inner,
        vxyz_projection_inner=vxyz_inner,
        eme_inner=eme_inner,
        policy=policy,
        context=ctx,
        context_confidence=ctx_conf,
        min_context_confidence=float(args.min_context_confidence),
    )
    decision_inner = (decision_output or {}).get("decision_output")

    # 6) Cognitive graph + pulse
    graph_meta = {
        "ctx_reason": ctx_reason,
        "msg_ctx": msg_ctx,
        "msg_conf": msg_conf,
        "log_ctx": log_ctx,
        "log_conf": log_conf,
        "min_context_confidence": float(args.min_context_confidence),
    }

    graph = build_graph(ctx, ctx_conf, policy, logs, vxyz_inner, flowgraph_inner, collapse_inner, meta=graph_meta)

    if eme_inner:
        graph["emotion_modulation"] = {
            "emotion_band": eme_inner.get("emotion_band"),
            "collapse_band": eme_inner.get("collapse_band"),
            "gating_effect": eme_inner.get("gating_effect"),
        }

    if dual_inner:
        risk = dual_inner.get("risk_envelope", {}) or {}
        graph["dual_outcome"] = {
            "recommended_stance": risk.get("recommended_stance"),
            "capacity_fit": risk.get("capacity_fit"),
            "width": risk.get("width"),
            "skew": risk.get("skew"),
            "risk_score": risk.get("risk_score"),
        }

    if decision_inner:
        graph["decision"] = {
            "action": (decision_inner.get("action") or {}).get("label"),
            "timing": (decision_inner.get("timing") or {}).get("window"),
            "confidence": decision_inner.get("confidence"),
            "signal_quality": (decision_inner.get("meta") or {}).get("signal_quality"),
            "safe_mode": (decision_inner.get("meta") or {}).get("safe_mode"),
        }

    pulse_weights = extract_pulse_weights(graph)

    print_cognitive_graph(graph)
    log(f"Pulse Weights: {pulse_weights}")

    # 7) Full ingest
    full_ingest(root, policy)

    # 8) Pulse re-ingest
    pulse_reingest(root, pulse_weights)

    # 9) FlowGraph doc reinforcement
    fgfile = load_flowgraph_file(root)
    if fgfile is not None:
        log(f"FlowGraph Document Detected: {fgfile}")
        ingest_file(fgfile)

    save_state(root, ctx, ctx_conf)
    run_autoload(root)

    log("Lypha-OS Kernel Complete — Season 8 CORE+ Runtime Active (Hardened).")


if __name__ == "__main__":
    main()
