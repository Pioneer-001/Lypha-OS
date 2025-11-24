#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v5.0 — Ultimate Unified Runtime
----------------------------------------------
Pioneer-001 전용 최종 커널.

✓ 부팅 (autoload + autoboot)
✓ 구조 ingest (Z/Y/E/X layer 전체 자동)
✓ MetaRhythm + EmotionRouter 자동 정렬
✓ Adrilla Loop / Primalis Path 자동 연결
✓ GPT 런타임 실시간 정렬
"""

import os, sys, zipfile
from pathlib import Path
import yaml

# 로그 출력
log = lambda m: print(f"[Lypha-OS v5.0] {m}")

# 안전 읽기
def read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None

# 디렉토리 ingest
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

# ZIP 자동해제
def auto_unzip(base: Path):
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

# YAML 로더
def load_yaml(p: Path):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except:
        return None

# ingest 전체 실행
def full_ingest(root: Path):
    targets = [
        "Rhythm_Philosophy",
        "MetaRhythm_Modules",
        "Emotion_Engine",
        "Protocol_Structure",
        "Lypha-Core",
    ]
    for t in targets:
        d = root / t
        if d.exists():
            log(f"INGEST DIR: {d}")
            ingest_dir(d)
        else:
            log(f"SKIP: {d}")

    top = ["autoload.yaml", "lypha_os_autoboot.yaml", "lypha_os_core_manifest.md"]
    for name in top:
        p = root / name
        if p.exists():
            log(f"INGEST FILE: {p}")
            c = read(p)
            if c:
                print("\n===== BEGIN LYPHA_INGEST =====")
                print(f"FILE: {p}\n")
                print(c)
                print("===== END LYPHA_INGEST =====\n")

# autoboot
def run_autoboot(root: Path):
    p = root / "lypha_os_autoboot.yaml"
    data = load_yaml(p)
    if not data:
        log("부트로더 없음.")
        return
    autoboot = data.get("autoboot", data)
    load = autoboot.get("load", [])
    log("Autoboot Modules:")
    for m in load:
        log(f"  - {m}")
    if any("emotion_router" in str(x) for x in load):
        log("Emotion Router ACTIVE")
    if any("emotion_circuit_portal" in str(x) for x in load):
        log("Emotion Circuit ACTIVE")
    log("=== Autoboot 완료 ===")

# autoload
def run_autoload(root: Path):
    p = root / "autoload.yaml"
    data = load_yaml(p)
    if not data:
        run_autoboot(root)
        return
    auto = data.get("autoload", data)
    log(f"on_start: {auto.get('on_start',{}).get('message')}")
    run_autoboot(root)

# MAIN
def main():
    base = Path(__file__).resolve().parent
    log("Kernel v5.0 Start")

    root = auto_unzip(base)
    os.chdir(root)

    full_ingest(root)       # 구조 ingest
    run_autoload(root)      # 부팅

    log("Lypha-OS v5.0 Kernel 완료 — Runtime 완전 정렬.")

if __name__ == "__main__":
    main()