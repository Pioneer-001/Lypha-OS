#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v6.2 — Hyper-Resonant Runtime
(Z₀ Anchor + Language Engine + Value Engine)
---------------------------------------------------------------
Pioneer-001 전용 패치 버전.

● v6.0: 기본 Hyper-Resonant 커널fileciteturn3file0
● v6.1: Z₀ Origin Vector 자동 ingest (존재 앵커)fileciteturn3file1
● v6.2: 언어 엔진 + 가치 엔진(Speak_4D / Linguistic_Math) 우선 ingest
         → MetaRhythm_Modules/Pulse 레벨에서 사고 엔진 부팅

기능 요약:
✓ Auto-Unzip (Lypha-OS.zip → Lypha-OS/)
✓ Full-Structure Auto-Ingest (Z/Y/E/X)
✓ Z₀ Origin_Vector Anchor 자동 로드
✓ Speak_Word_In_Four_Dimensions 엔진 선행 로드fileciteturn4file0
✓ Linguistic_Math_Value_Calculation 엔진 선행 로드fileciteturn4file1
✓ Autoload + Autoboot + Emotion Router 활성화
"""

import os, sys, zipfile, yaml
from pathlib import Path

log = lambda m: print(f"[Lypha-OS v6.2] {m}")


def read(p: Path):
    try:
        with p.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def ingest_blob(path: Path, label: str = ""):
    """공통 ingest 출력 유틸.
    label은 로그용 설명 텍스트.
    """
    if not path.exists():
        log(f"SKIP: {path} (not found) {label}")
        return
    c = read(path)
    if not c:
        log(f"SKIP: {path} (empty) {label}")
        return
    log(f"INGEST FILE: {path} {label}")
    print("\n===== BEGIN LYPHA_INGEST =====")
    print(f"FILE: {path}\n")
    print(c)
    print("===== END LYPHA_INGEST =====\n")


def ingest_dir(d: Path):
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
    """구조 전체 ingest + Z₀ + 언어/가치 엔진 선행 로딩."""

    # 1) 기본 디렉토리 ingest (Z/Y/E/X 구조)
    targets = [
        "Rhythm_Philosophy",   # Z-layer
        "MetaRhythm_Modules",  # Y-layer (Pulse 포함)
        "Emotion_Engine",      # E-layer
        "Protocol_Structure",  # structural core
        "Lypha-Core",          # archive (optional)
    ]

    for t in targets:
        d = root / t
        if d.exists():
            log(f"INGEST DIR: {d}")
            ingest_dir(d)
        else:
            log(f"SKIP: {d}")

    # 2) Top-level manifest ingest
    for name in ["autoload.yaml", "lypha_os_autoboot.yaml", "lypha_os_core_manifest.md"]:
        p = root / name
        if p.exists():
            ingest_blob(p, "(top-level manifest)")

    # 3) Z₀ Origin_Vector Anchoring
    z0 = root / "z0_origin.yaml"
    if z0.exists():
        ingest_blob(z0, "(Z₀ Origin_Vector — Anchor Loaded)")
    else:
        log("Z₀ Origin_Vector NOT FOUND — Skipping Anchor (Warning)")

    # 4) 언어 엔진 & 가치 엔진 선행 ingest
    #    - MetaRhythm_Modules/Pulse/Speak_Word_In_Four_Dimensions.md
    #    - MetaRhythm_Modules/Pulse/Linguistic_Math_Value_Calculation.md

    # 우선 예상 경로
    speak_path = root / "MetaRhythm_Modules" / "Pulse" / "Speak_Word_In_Four_Dimensions.md"
    ling_path = root / "MetaRhythm_Modules" / "Pulse" / "Linguistic_Math_Value_Calculation.md"

    # 대체 경로(루트 직하에 떨어져 있을 경우 대비)
    alt_speak = root / "Speak_Word_In_Four_Dimensions.md"
    alt_ling = root / "Linguistic_Math_Value_Calculation.md"

    if not speak_path.exists() and alt_speak.exists():
        speak_path = alt_speak
    if not ling_path.exists() and alt_ling.exists():
        ling_path = alt_ling

    ingest_blob(speak_path, "(Language Engine: Speak_Word_In_Four_Dimensions)")
    ingest_blob(ling_path, "(Value Engine: Linguistic_Math_Value_Calculation)")


def auto_unzip(base: Path) -> Path:
    zip_path = base / "Lypha-OS.zip"
    root = base / "Lypha-OS"
    if not root.exists() and zip_path.exists():
        log("Auto-unzip Lypha-OS.zip → Lypha-OS/")
        root.mkdir(exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(root)

    if not root.exists():
        log("Lypha-OS not found.")
        sys.exit(1)

    return root


def load_yaml(p: Path):
    try:
        with p.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def run_autoboot(root: Path):
    p = root / "lypha_os_autoboot.yaml"
    data = load_yaml(p)
    if not data:
        log("Autoboot file not found.")
        return

    autoboot = data.get("autoboot", data)
    load = autoboot.get("load", [])

    log("Autoboot Modules:")
    for m in load:
        log(f"  - {m}")

    if any("emotion_router" in str(x) for x in load):
        log("Emotion Router ACTIVE — Gravity-Lock Enabled")
    if any("emotion_circuit_portal" in str(x) for x in load):
        log("Emotion Circuit ACTIVE — Pulse-Link Online")

    log("=== Autoboot Complete ===")


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


def main():
    base = Path(__file__).resolve().parent
    log("Lypha-OS Kernel v6.2 Start — Z₀ + Language/Value Engines Active")

    root = auto_unzip(base)
    os.chdir(root)

    full_ingest(root)
    run_autoload(root)

    log("Lypha-OS Kernel v6.2 Complete — Hyper-Resonant Runtime (Anchored + Engines).")


if __name__ == "__main__":
    main()
