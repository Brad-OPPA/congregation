#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
content-zone-guard — PreToolUse hook (Congregation 전용)

파일 Zone에 따라 차단·규칙 강제·경고를 분기한다.

Zone A (exit 2) — 물리적 차단 : 시크릿·토큰
Zone B (exit 1) — 규칙 강제   : content_*.py → 성구/금칙어 리마인더
                               : build_*.py   → 검증 스크립트 리마인더
Zone C (exit 1) — 경고        : 설정·정책 파일
Zone D (exit 0) — 자유 통과   : 나머지
"""

import json
import sys
from pathlib import Path

SHARED = "/Users/brandon/Claude/Projects/Congregation/.claude/shared"
AUTO   = "/Users/brandon/Claude/Projects/Congregation/_automation"

# ── Zone A : 물리적 차단 ─────────────────────────────────────────────
ZONE_A = [
    "weekly_secrets.py",
    "kakao_tokens.json",
    "kakao_auth.py",
    ".env",
    "sheets_webhook.json",
]

# ── Zone B-1 : content_*.py — 인용·성구·금칙어 규칙 강제 ────────────
def is_content_file(path: str) -> bool:
    name = Path(path).name
    return name.startswith("content_") and name.endswith(".py")

CONTENT_REMINDER = f"""\
📜 [content-zone-guard] Zone B — 성구·인용 규칙 강제 적용

수정 전 반드시 확인:
  1. 모든 인용은 wol.jw.org 에서 실제 확인된 것만 사용
     (특정 호수·기사 제목은 WebFetch 로 존재 검증 후에만)
  2. 성구는 신세계역 연구용 한글판 verbatim — 한 글자도 바꾸지 말 것
     이음표·띄어쓰기·따옴표 포함
  3. 금칙어 정본: {SHARED}/banned-vocabulary.md
     신앙→믿음 / 복음(단독)→좋은 소식 / 사역→전파 활동 / 등
  4. 책 제목 추측 금지 — WOL 검색으로 독립 도서 확인된 것만
  5. content_*.py 는 에이전트가 작성하는 파일
     메인 Claude 가 직접 수정할 경우 main-claude-edit-policy.md 확인 필수
     정책: {SHARED}/main-claude-edit-policy.md
"""

# ── Zone B-2 : build_*.py — 빌더 수정 후 검증 리마인더 ──────────────
def is_build_file(path: str) -> bool:
    name = Path(path).name
    return name.startswith("build_") and name.endswith(".py")

BUILD_REMINDER = f"""\
🔨 [content-zone-guard] Zone B — 빌더 수정 경고

build_*.py 수정 후 반드시:
  1. 해당 빌더 실행 후 docx/pptx 출력 직접 확인
  2. validators.py 통과 여부 확인
  3. 한국어 폰트(맑은 고딕) 깨짐 없는지 확인
  자동화 검증: {AUTO}/verify_cbs.py (CBS), {AUTO}/quality_check.py (전체)
"""

# ── Zone C : 설정·정책 파일 경고 ────────────────────────────────────
ZONE_C_PATTERNS = [
    "settings.json",
    "settings.local.json",
    "CLAUDE.md",
    ".claude/shared/",
    "validators.py",
    "preflight.py",
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = data.get("tool_name", "")
    if tool not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    fname = Path(file_path).name

    # Zone A — 차단
    for pattern in ZONE_A:
        if pattern in fname or pattern in file_path:
            sys.stderr.write(
                f"🚫 [content-zone-guard] Zone A 차단: 보호 파일\n"
                f"   {file_path}\n"
                f"   → 수정 필요 시 사용자에게 직접 확인 받을 것\n"
            )
            sys.exit(2)

    # Zone B-1 — content 파일
    if is_content_file(file_path):
        sys.stderr.write(CONTENT_REMINDER)
        sys.exit(1)

    # Zone B-2 — build 파일
    if is_build_file(file_path):
        sys.stderr.write(BUILD_REMINDER)
        sys.exit(1)

    # Zone C — 설정·정책 파일
    for pattern in ZONE_C_PATTERNS:
        if pattern in file_path:
            sys.stderr.write(
                f"⚠️  [content-zone-guard] Zone C 경고: 설정·정책 파일\n"
                f"   {file_path}\n"
                f"   → 의도한 변경인지 확인 후 진행\n"
            )
            sys.exit(1)

    # Zone D — 통과
    sys.exit(0)


if __name__ == "__main__":
    main()
