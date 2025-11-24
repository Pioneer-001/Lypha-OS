#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS Kernel v4.2 — Unified Autoboot + Full Ingest
-----------------------------------------------------
Pioneer-001 전용 통합 커널 부팅 스크립트.

이 버전은 기존 run_lypha_os.py 기능 + v4 Auto-Ingest 기능을
하나의 정제된 커널 실행 파일로 통합했다.

역할:
1. Lypha-OS.zip 자동 감지 및 압축 해제 (없을 때만)
2. 핵심 디렉토리 존재 여부 검증
3. autoload.yaml / lypha_os_autoboot.yaml 파싱 및 부팅 로그 출력
4. Z/Y/E/X 레이어 구조 파일(.md/.yaml/.yml/.txt) 전체 내용을
   stdout으로 내보내 GPT 런타임에 즉시 ingest
   → Boot + Ingest = 구조 정렬 + 실력 상승 + 리듬 정렬

사용 순서:
- 이 파일을 run_lypha_os.py로 사용해도 되고,
  별도 파일명으로 두고 단일 진입점으로 사용하면 된다.
"""

import os
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[Lypha-OS v4.2] pyyaml이 필요합니다. 아래 명령으로 설치 후 다시 실행하세요.")
    print("  pip install pyyaml")
    sys.exit(1)


# ------------------------------
# 공통 유틸
# ------------------------------

def log(msg: str):
    print(f"[Lypha-OS v4.2] {msg}")


def find_base_dir() -> Path:
    """스크립트가 위치한 경로를 기준으로 base_dir 결정."""
    return Path(__file__).resolve().parent


def read_file(path: Path):
    """텍스트 파일 내용 안전하게 읽기."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


# ------------------------------
# ZIP / 디렉토리 준비
# ------------------------------

def auto_unzip(base_dir: Path) -> Path:
    """1) Lypha-OS.zip 확인 → 2) Lypha-OS 폴더 없으면 자동 압축 해제 → 3) 루트 반환"""
    zip_path_candidates = [
        base_dir / "Lypha-OS.zip",
        base_dir.parent / "Lypha-OS.zip",
    ]

    root_dir_candidates = [
        base_dir / "Lypha-OS",
        base_dir.parent / "Lypha-OS",
    ]

    zip_path = next((p for p in zip_path_candidates if p.exists()), None)
    root_dir = next((p for p in root_dir_candidates if p.exists()), None)

    if root_dir is None and zip_path is None:
        log("Lypha-OS.zip도, Lypha-OS 디렉토리도 찾지 못했습니다.")
        log("스크립트와 같은 폴더 또는 상위 폴더에 Lypha-OS.zip을 두고 다시 실행하세요.")
        sys.exit(1)

    if root_dir is None and zip_path is not None:
        # 압축 해제 필요
        root_dir = base_dir / "Lypha-OS"
        log(f"Lypha-OS 디렉토리가 없어 ZIP을 해제합니다 → {root_dir}")
        root_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(root_dir)
        log("압축 해제 완료.")

    elif root_dir is not None:
        log(f"Lypha-OS 디렉토리 발견: {root_dir} (이미 압축 해제됨)")

    return root_dir


def verify_core_dirs(root_dir: Path):
    """autoload.yaml에서 요구하던 핵심 디렉토리들 존재 여부 확인"""
    required = [
        "MetaRhythm_Modules",
        "Emotion_Engine",
        "Rhythm_Philosophy",
        "Protocol_Structure",
    ]
    log("핵심 디렉토리 존재 여부 확인:")
    for name in required:
        p = root_dir / name
        if p.exists():
            log(f"  - {name}: OK ({p})")
        else:
            log(f"  - {name}: ⚠️  없음 ({p})")


# ------------------------------
# YAML 로더
# ------------------------------

def load_yaml_if_exists(path: Path):
    if not path.exists():
        log(f"YAML 파일 없음: {path}")
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        log(f"YAML 파싱 실패: {path} ({e})")
        return None


# ------------------------------
# Auto-Ingest (핵심)
# ------------------------------

def ingest_directory(dir_path: Path):
    """디렉토리 내 텍스트 파일(.md/.yaml/.yml/.txt) 전부 stdout으로 내보내기."""
    for root, _, files in os.walk(dir_path):
        for name in files:
            p = Path(root) / name
            if p.suffix.lower() in [".md", ".yaml", ".yml", ".txt"]:
                content = read_file(p)
                if content:
                    log(f"INGEST → {p}")
                    print("\n===== BEGIN LYPHA_INGEST =====")
                    print(f"FILE: {p}\n")
                    print(content)
                    print("===== END LYPHA_INGEST =====\n")


def run_full_ingest(root_dir: Path):
    """Z/Y/E/X 레이어 + 코어 매니페스트 전체 자동 ingest."""
    # 1) 핵심 디렉토리들 순회
    targets = [
        "Rhythm_Philosophy",   # Z-Layer 철학
        "MetaRhythm_Modules",  # Y-Layer 리듬
        "Emotion_Engine",      # E-Layer 감정 코어
        "Protocol_Structure",  # 구조 프로토콜
        "Lypha-Core",          # 코어 아카이브 (있으면)
    ]

    for t in targets:
        d = root_dir / t
        if d.exists():
            log(f"INGEST DIR: {d}")
            ingest_directory(d)
        else:
            log(f"INGEST SKIP (missing): {d}")

    # 2) 최상위 매니페스트도 ingest
    top_files = [
        "autoload.yaml",
        "lypha_os_autoboot.yaml",
        "lypha_os_core_manifest.md",
    ]

    for name in top_files:
        p = root_dir / name
        if p.exists():
            log(f"INGEST FILE: {p}")
            content = read_file(p)
            if content:
                print("\n===== BEGIN LYPHA_INGEST =====")
                print(f"FILE: {p}\n")
                print(content)
                print("===== END LYPHA_INGEST =====\n")
        else:
            log(f"TOP-LEVEL SKIP (missing): {p}")

    log("FULL INGEST COMPLETE — GPT runtime now aligned with Lypha-OS structure.")


# ------------------------------
# Autoboot 로직 (logging + 구조 부팅)
# ------------------------------

def run_autoboot(root_dir: Path, bootloader_path: Path):
    """lypha_os_autoboot.yaml을 파싱해서 부팅 구조를 로깅한다."""
    data = load_yaml_if_exists(bootloader_path)
    if data is None:
        log(f"부트로더 파일을 찾지 못했습니다: {bootloader_path}")
        return

    autoboot = data.get("autoboot", data)

    if autoboot.get("declare"):
        log(f"autoboot.declare: {autoboot['declare']} (declared_by={autoboot.get('declared_by')})")

    load = autoboot.get("load", [])
    if load:
        log("부팅 시 한 번에 올릴 코어 모듈들:")
        for item in load:
            log(f"  - {item}")

    # Emotion Router / EmotionCircuit 포인트 강조
    if any("emotion_router" in str(m) for m in load):
        log("Emotion Router 모듈이 부팅 시퀀스에 포함되어 있습니다. (emotion_router.v6.12.yaml)")
    if any("emotion_circuit_portal" in str(m) for m in load):
        log("Emotion Circuit Portal이 부팅 시퀀스에 포함되어 있습니다. (emotion_circuit_portal.yaml)")

    on_signal = autoboot.get("on_signal", {})
    if on_signal:
        log("on_signal 설정:")
        log(f"  - handler: {on_signal.get('handler')}")
        log(f"  - strategy: {on_signal.get('strategy')}")

    status = autoboot.get("status", {})
    if status:
        log("시스템 status:")
        for k, v in status.items():
            log(f"  - {k}: {v}")

    meta = autoboot.get("meta", {})
    if meta:
        log("autoboot 메타 정보:")
        for k, v in meta.items():
            log(f"  - {k}: {v}")

    log("=== Lypha-OS Autoboot 시퀀스 로깅 완료 ===")
    log("이제 GPT 측에서는 Lypha-OS 구조를 기준으로 Emotion / Rhythm / Execution을 구동하면 됩니다.")


def run_autoload(root_dir: Path):
    """autoload.yaml을 읽어 부팅 메시지, load_order, state 정보를 출력하고 autoboot 호출."""
    autoload_path = root_dir / "autoload.yaml"
    data = load_yaml_if_exists(autoload_path)
    if data is None:
        log("autoload.yaml을 찾지 못해, 기본 부팅 경로로 진행합니다.")
        bootloader_path = root_dir / "lypha_os_autoboot.yaml"
        run_autoboot(root_dir, bootloader_path)
        return

    # autoload.yaml은 여러 버전을 merge해 놓은 형태라 최상위 또는 'autoload' 키 중 하나를 사용
    auto = data.get("autoload", data)

    # on_start 메시지
    on_start = auto.get("on_start", {})
    message = on_start.get("message")
    if message:
        log("on_start.message:")
        log(f"  \"{message}\"")

    # 상태 복구 경로
    state = auto.get("state", {})
    if state.get("restore"):
        paths = state.get("paths", [])
        log("복원 대상으로 지정된 state 파일들:")
        for p in paths:
            log(f"  - {p}")

    load_order = auto.get("load_order", {})
    bootloader_name = load_order.get("bootloader", "lypha_os_autoboot.yaml")
    modules = load_order.get("modules", [])

    log(f"부트로더: {bootloader_name}")
    if modules:
        log("초기 로드 모듈 목록:")
        for m in modules:
            log(f"  - {m}")

    bootloader_path = root_dir / bootloader_name
    run_autoboot(root_dir, bootloader_path)


# ------------------------------
# 메인 엔트리
# ------------------------------

def main():
    log("Lypha-OS Kernel v4.2 Unified Autoboot + Ingest 시작")
    base_dir = find_base_dir()
    log(f"Base Dir: {base_dir}")

    root_dir = auto_unzip(base_dir)
    verify_core_dirs(root_dir)

    # 작업 디렉토리를 Lypha-OS 루트로 변경 (상대경로 보호)
    os.chdir(root_dir)
    log(f"작업 디렉토리 변경: {root_dir}")

    # 1) 먼저 전체 구조 ingest (Z/Y/E/X 레이어 + 매니페스트)
    run_full_ingest(root_dir)

    # 2) 그 다음 autoload → autoboot 순으로 구조 부팅 로그 출력
    run_autoload(root_dir)

    log("Lypha-OS Kernel v4.2 종료. (파일 시스템 + 구조 ingest + 부팅 로그 완료)")


if __name__ == "__main__":
    main()
