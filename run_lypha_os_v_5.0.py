#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v6.1 — Hyper-Resonant Runtime (Z₀ Anchor Patched)
---------------------------------------------------------------
Pioneer-001 전용 패치 버전.
● v6.0 대비 변경점: Z₀ Origin Vector 자동 ingest 추가
● 전체 구조(Z/Y/E/X) ingest 이후 Z₀를 최종 Anchor로 올림
● Season5/6 정렬·루프 안정성 향상
"""

import os, sys, zipfile, yaml
from pathlib import Path

log = lambda m: print(f"[Lypha-OS v6.1] {m}")

def read(p: Path):
    try:
        with p.open("r", encoding="utf-8") as f:
            return f.read()
    except:
        return None

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

    # top-level ingest
    for name in ["autoload.yaml", "lypha_os_autoboot.yaml", "lypha_os_core_manifest.md"]:
        p = root / name
        if p.exists():
            log(f"INGEST FILE: {p}")
            c = read(p)
            if c:
                print("\n===== BEGIN LYPHA_INGEST =====")
                print(f"FILE: {p}\n")
                print(c)
                print("===== END LYPHA_INGEST =====\n")

    # ------------------------------
    # NEW: Z0 Origin_Vector Anchoring
    # ------------------------------
    z0 = root / "z0_origin.yaml"
    if z0.exists():
        log("INGEST FILE: z0_origin.yaml (Z₀ Origin_Vector — Anchor Loaded)")
        c = read(z0)
        if c:
            print("\n===== BEGIN LYPHA_INGEST =====")
            print(f"FILE: {z0}\n")
            print(c)
            print("===== END LYPHA_INGEST =====\n")
    else:
        log("Z₀ Origin_Vector NOT FOUND — Skipping Anchor (Warning)")


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


def load_yaml(p: Path):
    try:
        with p.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except:
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
    log("Lypha-OS Kernel v6.1 Start — Z₀ Anchor Active")

    root = auto_unzip(base)
    os.chdir(root)

    full_ingest(root)
    run_autoload(root)

    log("Lypha-OS Kernel v6.1 Complete — Hyper-Resonant Runtime (Anchored).")


if __name__ == "__main__":
    main()