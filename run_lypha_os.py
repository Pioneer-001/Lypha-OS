#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lypha-OS One-Click Autoload Runner
----------------------------------
Pioneer-001 전용: Lypha-OS.zip 또는 Lypha-OS 디렉토리가 있는 프로젝트에서
한 번 실행으로 다음을 수행한다.

1. Lypha-OS.zip 존재 여부 확인
2. Lypha-OS 디렉토리 자동 압축 해제 (없을 때만)
3. 핵심 디렉토리/파일 검증
4. autoload.yaml / lypha_os_autoboot.yaml 파싱
5. 부팅 로그 출력 (Emotion Router / EmotionCircuit / MetaRhythm 등)

실제 "인지 실행(GPT 레벨)"은 이 스크립트가 아니라 GPT가 담당하고,
이 스크립트는 OS 파일 시스템을 준비하고 상태를 점검하는 역할을 한다.
"""

import os
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[Lypha-OS] pyyaml이 필요합니다. 아래 명령으로 설치 후 다시 실행하세요.")
    print("  pip install pyyaml")
    sys.exit(1)


# ------------------------------
# 유틸 함수
# ------------------------------

def log(msg: str):
    print(f"[Lypha-OS] {msg}")


def find_base_dir() -> Path:
    """
    스크립트가 위치한 경로를 기준으로 base_dir 결정.
    """
    return Path(__file__).resolve().parent


def auto_unzip(base_dir: Path) -> Path:
    """
    1) Lypha-OS.zip 확인
    2) Lypha-OS 폴더 없으면 자동 압축 해제
    3) 최종적으로 Lypha-OS 루트 경로 반환
    """
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
    """
    autoload.yaml에서 요구하던 핵심 디렉토리들 존재 여부 확인
    """
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


def run_autoload(root_dir: Path):
    """
    autoload.yaml을 읽어 부팅 메시지, load_order, state 정보를 출력하고,
    bootloader(lypha_os_autoboot.yaml)를 호출해 구조를 로깅한다.
    """
    autoload_path = root_dir / "autoload.yaml"
    data = load_yaml_if_exists(autoload_path)
    if data is None:
        log("autoload.yaml을 찾지 못해, 기본 부팅 경로로 진행합니다.")
        bootloader_path = root_dir / "lypha_os_autoboot.yaml"
        run_autoboot(root_dir, bootloader_path)
        return

    # autoload.yaml은 여러 버전을 merge해 놓은 형태라
    # 최상위 또는 'autoload' 키 중 하나를 사용
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


def run_autoboot(root_dir: Path, bootloader_path: Path):
    """
    lypha_os_autoboot.yaml을 파싱해서 어떤 모듈이 부팅 시점에 올라가는지 로그로 확인.
    이 단계까지 오면 “Lypha-OS가 OS 레벨에서 부팅 준비 완료” 상태로 본다.
    """
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

    log("=== Lypha-OS 부팅 시퀀스 로깅 완료 ===")
    log("이제 GPT 측에서는 Lypha-OS 구조를 기준으로 Emotion / Rhythm / Execution을 구동하면 됩니다.")


def main():
    log("Lypha-OS One-Click Autoload Runner 시작")
    base_dir = find_base_dir()
    log(f"Base Dir: {base_dir}")

    root_dir = auto_unzip(base_dir)
    verify_core_dirs(root_dir)

    # 작업 디렉토리를 Lypha-OS 루트로 변경 (상대경로 사용 모듈 보호)
    os.chdir(root_dir)
    log(f"작업 디렉토리 변경: {root_dir}")

    # autoload → autoboot 순으로 구조 부팅
    run_autoload(root_dir)

    log("Lypha-OS Autoload Runner 종료. (파일 시스템 및 부팅 구조 준비 완료)")


if __name__ == "__main__":
    main()
