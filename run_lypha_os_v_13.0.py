#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v13.0 — Unified Hyper-Graph Runtime
===================================================
Pioneer-001 전용 최상위 통합 커널.

▶ v6.0 (Auto-Unzip + Full Ingest + Autoboot)
▶ v12.1 (FlowGraph + Cognitive Graph + Pulse Weights)

을 하나로 합친 "최상위 버전" 런타임.

핵심 기능 요약:
------------------------------------------------------------
✓ Auto-Unzip : Lypha-OS.zip → Lypha-OS/ 자동 압축 해제
✓ Full-Structure Auto-Ingest (Z/Y/E/X + Core Manifest)
✓ FlowGraph 기반 Cognitive Graph 생성
✓ Context 감지(감정/트레이딩/디자인/중립) → 가중치 조정
✓ Pulse 엔진 가중치 추출 (Speak4D / Math / Collapse / FlowGraph)
✓ Autoload + Autoboot 실행 (Emotion Router / Circuit 활성 상태 표시)

사용 방법:
------------------------------------------------------------
- 이 파일을 run_lypha_os_v_13.0.py 같은 이름으로 저장 후 실행
- 같은 디렉토리에 Lypha-OS.zip 이 존재하면 자동으로 풀고 부팅
- 이미 Lypha-OS/ 폴더가 있다면 그대로 사용
"""

import os
import sys
import zipfile
import json
import yaml
from pathlib import Path

log = lambda m: print(f"[Lypha-OS v13.0] {m}")

# -------------------------------------------------------------
# BASIC FILE I/O
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
# AUTO-UNZIP (v6 계열 기능 상속)
# -------------------------------------------------------------

def auto_unzip(base: Path) -> Path:
    """Lypha-OS.zip 이 있으면 자동으로 Lypha-OS/ 로 압축 해제.

    - Lypha-OS/ 가 이미 있으면 그대로 사용
    - zip 이 없고 폴더도 없으면 오류 후 종료
    """
    zip_path = base / "Lypha-OS.zip"
    root = base / "Lypha-OS"

    if not root.exists() and zip_path.exists():
        log("Auto-unzip Lypha-OS.zip → Lypha-OS/")
        root.mkdir(exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(root)

    if not root.exists():
        log("ERROR: Lypha-OS 폴더를 찾을 수 없습니다 (Lypha-OS/ or Lypha-OS.zip 필요).")
        sys.exit(1)

    return root


# -------------------------------------------------------------
# INGEST ENGINE (v6 + Manifest 추가)
# -------------------------------------------------------------

def ingest_dir(d: Path):
    """지정 디렉토리 하위의 모든 .md/.yaml/.yml/.txt 파일 ingest."""
    for root, _, files in os.walk(d):
        for n in files:
            p = Path(root) / n
            if p.suffix.lower() in [".md", ".yaml", ".yml", ".txt"]:
                c = read(p)
                if c:
                    log(f"INGEST → {p}")
                    print("\n===== BEGIN LYPHA_INGEST =====")
                    print(f"FILE: {p}\n")
                    print(c)
                    print("===== END LYPHA_INGEST =====\n")


def full_ingest(root: Path):
    """Z/Y/E/X 레이어 + Core Manifest 파일 ingest."""
    targets = [
        "Rhythm_Philosophy",   # Z-layer
        "MetaRhythm_Modules",  # Y-layer
        "Emotion_Engine",      # E-layer
        "Protocol_Structure",  # structural core (X-layer / etc.)
        "Lypha-Core",          # 추가 아카이브 (선택)
    ]

    for t in targets:
        d = root / t
        if d.exists():
            log(f"INGEST DIR: {d}")
            ingest_dir(d)
        else:
            log(f"SKIP: {d}")

    # Top-level manifest ingest
    for name in [
        "autoload.yaml",
        "lypha_os_autoboot.yaml",
        "lypha_os_core_manifest.md",
    ]:
        p = root / name
        if p.exists():
            log(f"INGEST FILE: {p}")
            c = read(p)
            if c:
                print("\n===== BEGIN LYPHA_INGEST =====")
                print(f"FILE: {p}\n")
                print(c)
                print("===== END LYPHA_INGEST =====\n")


# -------------------------------------------------------------
# FLOWGRAPH / COGNITIVE GRAPH (v12.1 계열 기능 통합)
# -------------------------------------------------------------

def load_flowgraph_file(root: Path) -> Path | None:
    """FlowGraph 엔진용 문서 ingest (실제 파일 존재 시)."""
    fg1 = root / "MetaRhythm_Modules" / "Pulse" / "FlowGraph_Principles.md"
    fg2 = root / "FlowGraph_Principles.md"
    target = fg1 if fg1.exists() else fg2
    return target if target.exists() else None


def detect_context_message(root: Path) -> str:
    """autoload.yaml 안의 on_start.message 로부터 context 추출."""
    auto = root / "autoload.yaml"
    data = load_yaml(auto)
    if not data:
        return "neutral"
    msg = data.get("autoload", data).get("on_start", {}).get("message", "")
    return msg or "neutral"


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


def build_graph(context: str, policy: dict) -> dict:
    """Context + policy 기반 Cognitive Graph 생성."""
    g: dict = {
        "nodes": ["Z", "Y", "E", "X", "V", "Speak4D", "Math", "Collapse", "FlowGraph"],
        "edges": [],
        "weights": {
            "emotion": policy.get("emotion_weight", 1.0),
            "structure": policy.get("structure_weight", 1.0),
        },
        "context": context,
    }

    # Context 기반 edge 설정
    if context == "emotion":
        g["edges"].append(["E", "Z", 1.3])
        g["edges"].append(["Collapse", "Speak4D", 1.1])
        g["edges"].append(["FlowGraph", "E", 1.05])
    elif context == "trading":
        g["edges"].append(["Z", "Math", 1.4])
        g["edges"].append(["Math", "Collapse", 1.15])
        g["edges"].append(["FlowGraph", "Math", 1.1])
    elif context == "design":
        g["edges"].append(["Z", "Speak4D", 1.5])
        g["edges"].append(["Speak4D", "FlowGraph", 1.2])
    else:
        g["edges"].append(["Z", "Y", 1.0])
        g["edges"].append(["Y", "X", 1.0])
        g["edges"].append(["FlowGraph", "Z", 1.0])

    return g


def extract_pulse_weights(graph: dict) -> dict:
    """그래프 edge 정보를 Pulse 엔진 가중치로 변환."""
    weights = {"Speak4D": 1.0, "Math": 1.0, "Collapse": 1.0, "FlowGraph": 1.0}

    for edge in graph.get("edges", []):
        if len(edge) != 3:
            continue
        u, v, w = edge
        if v in weights:
            weights[v] += (w - 1.0)

    return weights


def load_logs(root: Path) -> dict:
    """v_logs/ 및 v_log.json 수집 (필요시 사용)."""
    merged: dict = {}
    base = root / "v_logs"
    if base.exists():
        for f in base.glob("*.json"):
            merged[f.name] = read_json(f)
    single = root / "v_log.json"
    if single.exists():
        merged["v_log"] = read_json(single)
    return merged


def print_cognitive_graph(graph: dict):
    """Cognitive Graph 구조를 JSON 형태로 출력."""
    print("===== BEGIN COGNITIVE_GRAPH =====")
    print(json.dumps(graph, ensure_ascii=False, indent=2))
    print("===== END COGNITIVE_GRAPH =====")


# -------------------------------------------------------------
# AUTOLOAD / AUTOBOOT (v6 계열 기능 통합)
# -------------------------------------------------------------

def run_autoboot(root: Path):
    p = root / "lypha_os_autoboot.yaml"
    data = load_yaml(p)
    if not data:
        log("Autoboot file not found.")
        return

    autoboot = data.get("autoboot", data)
    load_list = autoboot.get("load", [])

    log("Autoboot Modules (v13 unified):")
    for m in load_list:
        log(f"  - {m}")

    # Emotion Router / Circuit 활성 여부 출력
    load_str = " ".join(map(str, load_list))
    if "emotion_router" in load_str:
        log("Emotion Router ACTIVE — Gravity-Lock Enabled")
    if "emotion_circuit_portal" in load_str:
        log("Emotion Circuit ACTIVE — Pulse-Link Online")

    log("=== Autoboot 완료 (v13 Hyper-Init) ===")


def run_autoload(root: Path):
    p = root / "autoload.yaml"
    data = load_yaml(p)
    if not data:
        run_autoboot(root)
        return

    auto = data.get("autoload", data)
    msg = auto.get("on_start", {}).get("message")
    log(f"on_start: {msg}")

    run_autoboot(root)


# -------------------------------------------------------------
# MAIN ENTRY
# -------------------------------------------------------------

def main():
    base = Path(__file__).resolve().parent
    log("Lypha-OS Kernel v13.0 Start — Unified Hyper-Graph Runtime")

    # 1) Auto-Unzip → Lypha-OS 루트 확보
    root = auto_unzip(base)
    os.chdir(root)

    # 2) 정책 & 로그 로드 (선택적)
    policy_path = root / "policy" / "kernel_policy_v13.json"
    if not policy_path.exists():
        # v12 정책 파일이 있다면 fallback
        policy_path = root / "policy" / "kernel_policy_v12.json"
    policy = read_json(policy_path) or {
        "ingest_order": ["Z", "Y", "E", "X"],
        "emotion_weight": 1.0,
        "structure_weight": 1.0,
    }
    logs = load_logs(root)
    if logs:
        log(f"Verified Logs Loaded: {list(logs.keys())}")

    # 3) Context 감지 (autoload 기반)
    raw_msg = detect_context_message(root)
    ctx = detect_context(raw_msg)
    log(f"Context Detected: {ctx} (msg='{raw_msg}')")

    # 4) Cognitive Graph + Pulse Weights
    graph = build_graph(ctx, policy)
    pulse_weights = extract_pulse_weights(graph)

    print_cognitive_graph(graph)
    log(f"Pulse Weights: {pulse_weights}")

    # 5) 구조 ingest (v6 스타일 풀 ingest)
    full_ingest(root)

    # 6) Autoload → Autoboot 실행
    run_autoload(root)

    # 7) FlowGraph 문서 존재 시, Pulse 레이어 강조 ingest (선택)
    fgfile = load_flowgraph_file(root)
    if fgfile is not None:
        log(f"FlowGraph Document Detected: {fgfile}")
        c = read(fgfile)
        if c:
            print("\n===== BEGIN LYPHA_INGEST =====")
            print(f"FILE: {fgfile}\n")
            print(c)
            print("===== END LYPHA_INGEST =====\n")

    log("Lypha-OS Kernel v13.0 Complete — Unified Runtime Active.")


if __name__ == "__main__":
    main()
