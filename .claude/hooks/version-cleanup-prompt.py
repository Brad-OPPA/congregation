#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version-cleanup-prompt — Stop hook (2026-05-09)

_automation/ 에 _v{N}.py 버전 파일이 쌓인 경우,
작업 종료 시 이전 버전 정리 여부를 Claude 가 사용자에게 물어보도록 메시지 주입.

작동:
- _v{N}.py 패턴 파일이 있고, 같은 기반명의 구버전이 존재 → stderr 메시지 + exit 2
- 이미 이번 세션에서 한 번 물어봤으면 → exit 0 (재질문 방지)
- 없으면 → exit 0 (통과)

플래그 파일: /tmp/.congregation-cleanup-asked (1시간 쿨다운)
"""
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/Users/brandon/Claude/Projects/Congregation"))
AUTOMATION_DIR = PROJECT_ROOT / "_automation"
ASKED_FLAG = Path("/tmp/.congregation-cleanup-asked")
COOLDOWN_SECONDS = 3600  # 1시간 쿨다운 (같은 세션에서 반복 질문 방지)


def already_asked() -> bool:
    """최근 1시간 내에 이미 물어봤으면 True."""
    if ASKED_FLAG.exists():
        age = time.time() - ASKED_FLAG.stat().st_mtime
        if age < COOLDOWN_SECONDS:
            return True
    return False


def mark_asked():
    """플래그 파일 갱신."""
    ASKED_FLAG.touch()


def stop_hook_active() -> bool:
    """stdin JSON 에서 stop_hook_active 확인 — True 면 이미 Stop 훅으로 재개된 중."""
    try:
        data = json.loads(sys.stdin.read())
        return bool(data.get("stop_hook_active", False))
    except Exception:
        return False


def find_versioned_groups() -> dict:
    """
    _automation/ 에서 버전 파일 그룹을 찾는다.
    반환: { base_stem: [(ver_num, Path), ...] }  — 버전 2개 이상인 그룹만
    """
    if not AUTOMATION_DIR.exists():
        return {}

    py_files = list(AUTOMATION_DIR.glob("*.py"))
    groups = defaultdict(list)

    for f in py_files:
        stem = f.stem
        m = re.match(r'^(.+?)_v(\d+)$', stem)
        if m:
            base, ver = m.group(1), int(m.group(2))
            groups[base].append((ver, f))
        else:
            # 버전 없는 파일 = v0 (원본)
            groups[stem].append((0, f))

    # 구버전이 실제로 존재하는 그룹만 (= 파일 수 >= 2)
    result = {}
    for base, versions in groups.items():
        if len(versions) >= 2:
            versions.sort(key=lambda x: x[0])
            result[base] = versions

    return result


def main() -> int:
    # stop_hook_active 이면 이미 이 훅 때문에 재개된 것 → 무한루프 방지
    if stop_hook_active():
        return 0

    # 쿨다운 중이면 스킵
    if already_asked():
        return 0

    groups = find_versioned_groups()
    if not groups:
        return 0

    # 메시지 구성
    lines = [
        "",
        "🗂  [version-cleanup-prompt] _automation/ 에 버전 파일이 쌓여 있습니다.",
        "",
    ]

    old_count = 0
    for base, versions in sorted(groups.items()):
        max_ver = versions[-1][0]
        lines.append(f"  [{base}]")
        for ver_num, path in versions:
            if ver_num == max_ver:
                label = "✅ 최신"
            else:
                label = "🗑  구버전"
                old_count += 1
            ver_label = f"_v{ver_num}" if ver_num > 0 else "(원본)"
            lines.append(f"    {ver_label:10s}  {path.name}  {label}")
        lines.append("")

    lines += [
        f"❓ 이번 작업이 최종 완료되었다면 구버전 {old_count}개를 삭제해드릴 수 있습니다.",
        "   사용자에게 '이번 작업 최종인가요? 구버전 파일 정리할까요?' 라고 물어보고,",
        "   'ㅇㅇ' / '네' / '응' 이면 구버전 파일을 삭제하세요.",
        "   '아니요' 이면 그냥 넘어가세요.",
        "",
    ]

    sys.stderr.write("\n".join(lines))
    mark_asked()
    return 2


if __name__ == "__main__":
    sys.exit(main())
