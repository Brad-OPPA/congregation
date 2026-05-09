#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-on-edit-write — Edit/Write/MultiEdit PreToolUse 통합 정본 (2026-05-09)

기존 3 hook 통합:
  - pre-tool-guard      (Edit/Write PreToolUse)        — 시크릿/설정 보호 차단
  - content-zone-guard  (Edit/Write PreToolUse)        — Zone A·B·C 분기
  - edit-restriction    (UserPromptSubmit, 알림 전용)  — 메인 Claude 직접 정정 금지 reminder

정본 원칙 (2026-05-09):
  • Zone A (시크릿) → exit 2 차단 (rm-equivalent 보호)
  • Zone B (content_*.py / build_*.py / 메인 직접 정정 금지 영역) → exit 1 + stderr 규칙 리마인더
  • Zone C (settings·CLAUDE.md·shared·validators) → exit 1 + stderr 경고
  • Zone D (그 외) → exit 0 통과
  • 자동 재호출·UserPromptSubmit 의무 책임 X — SKILL 절차가 직접 처리

stdin: {"tool_name": "Edit"|"Write"|"MultiEdit", "tool_input": {"file_path": "..."}}
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/Users/brandon/Claude/Projects/Congregation"))
SHARED = PROJECT_ROOT / ".claude" / "shared"
AUTO = PROJECT_ROOT / "_automation"
POLICY_PATH = SHARED / "main-claude-edit-policy.md"


# ─────────────────────────────────────────────────────────────────────
# Zone A — 절대 차단 (exit 2): 시크릿·토큰
# ─────────────────────────────────────────────────────────────────────

ZONE_A_BLOCKED = [
    "weekly_secrets.py",
    "kakao_tokens.json",
    "kakao_auth.py",
    "sheets_webhook.json",
    ".env",
]


# ─────────────────────────────────────────────────────────────────────
# Zone B-extra — 메인 Claude 직접 Edit 금지 영역 (exit 1, 알림)
# (main-claude-edit-policy.md §1 — Phase E)
# ─────────────────────────────────────────────────────────────────────

RESTRICTED_PATTERNS = [
    "/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/",
    "/_automation/content_",
    "/research-plan/",
    "/research-bible/",
    "/research-topic/",
    "/research-application/",
    "/research-experience/",
    "/research-illustration/",
    "/research-qa/",
    "/research-prayer/",
]


# ─────────────────────────────────────────────────────────────────────
# Zone C — 설정·정책 파일 경고 (exit 1)
# ─────────────────────────────────────────────────────────────────────

ZONE_C_PATTERNS = [
    "settings.json",
    "settings.local.json",
    "CLAUDE.md",
    ".claude/shared/",
    "validators.py",
    "preflight.py",
]


# ─────────────────────────────────────────────────────────────────────
# 분기 판정 함수
# ─────────────────────────────────────────────────────────────────────

def is_content_file(path: str) -> bool:
    name = Path(path).name
    return name.startswith("content_") and name.endswith(".py")


def is_build_file(path: str) -> bool:
    name = Path(path).name
    return name.startswith("build_") and name.endswith(".py")


# ─────────────────────────────────────────────────────────────────────
# Stderr 메시지
# ─────────────────────────────────────────────────────────────────────

CONTENT_REMINDER = f"""\
📜 [validate-on-edit-write] Zone B — content_*.py 규칙 강제

수정 전 반드시:
  1. 모든 인용은 wol.jw.org 실제 확인된 것만 (WebFetch 검증 후)
  2. 성구는 신세계역 연구용 (nwtsty) verbatim — 한 글자도 바꾸지 말 것
  3. 금칙어 정본: {SHARED}/banned-vocabulary.md
     (예배·신앙·사역·간증 등)
  4. 책 제목 추측 금지 — WOL 검색으로 독립 도서 확인된 것만
  5. content_*.py 는 에이전트 작성 파일.
     메인 Claude 직접 수정은 정책 위반: {SHARED}/main-claude-edit-policy.md
"""

BUILD_REMINDER = f"""\
🔨 [validate-on-edit-write] Zone B — build_*.py 수정 경고

build_*.py 수정 후 반드시:
  1. 해당 빌더 실행 후 docx/pptx 출력 직접 확인
  2. validators.py 통과 여부 확인
  3. 한국어 폰트(맑은 고딕) 깨짐 없는지 확인
"""

POLICY_REMINDER = f"""\
🚫 [validate-on-edit-write] Zone B — 메인 Claude 직접 Edit 금지 영역

수정 시도 파일이 정책상 금지 영역입니다:
  • Dropbox 회중 docx · _automation/content_*.py
  • research-plan/script.md · outline.md
  • research-{{bible,topic,application,experience,illustration,qa,prayer}}/*.md

콘텐츠 정정 시 jw-style-checker / spiritual-gems-script /
해당 script 에이전트 호출 의무.
정책: {POLICY_PATH}
"""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool = data.get("tool_name", "")
    if tool not in ("Edit", "Write", "MultiEdit"):
        return 0

    file_path = data.get("tool_input", {}).get("file_path", "") or ""
    if not file_path:
        return 0

    fname = Path(file_path).name

    # Zone A — 차단
    for pattern in ZONE_A_BLOCKED:
        if pattern in fname or pattern in file_path:
            sys.stderr.write(
                f"\n🚫 [validate-on-edit-write] Zone A 차단: 보호 파일\n"
                f"   {file_path}\n"
                f"   이유: 인증 토큰·시크릿 자동 수정 금지\n"
                f"   → 사용자에게 직접 확인 후 진행\n"
            )
            return 2

    # Zone B-restricted — 메인 직접 정정 금지 영역
    for pattern in RESTRICTED_PATTERNS:
        if pattern in file_path:
            sys.stderr.write(POLICY_REMINDER)
            return 1

    # Zone B-1 — content 파일
    if is_content_file(file_path):
        sys.stderr.write(CONTENT_REMINDER)
        return 1

    # Zone B-2 — build 파일
    if is_build_file(file_path):
        sys.stderr.write(BUILD_REMINDER)
        return 1

    # Zone C — 설정·정책 파일
    for pattern in ZONE_C_PATTERNS:
        if pattern in file_path:
            sys.stderr.write(
                f"\n⚠️  [validate-on-edit-write] Zone C 경고: 설정·정책 파일\n"
                f"   {file_path}\n"
                f"   → 의도한 변경인지 확인 후 진행\n"
            )
            return 1

    # Zone D — 통과
    return 0


if __name__ == "__main__":
    sys.exit(main())
