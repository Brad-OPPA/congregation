#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
edit-restriction-hook — UserPromptSubmit hook (Phase E §S8, 2026-05-01)

메인 Claude 가 main-claude-edit-policy.md 에 정의된 금지 영역을
직접 Edit/Write 하는지 감시·경고. (현재는 알림 전용; 차단은 정책 자체 + 메인 자율 준수)

작동:
- 사용자 prompt 가 들어올 때마다 호출
- 최근 메인 Claude 의 Edit/Write 사용 흔적이 금지 영역에 있으면 stderr 경고

환경변수: EDIT_RESTRICTION_BYPASS=1 → 알림 무력화
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/Users/brandon/Claude/Projects/Congregation"))
POLICY_PATH = PROJECT_ROOT / ".claude/shared/main-claude-edit-policy.md"

# 금지 영역 (main-claude-edit-policy.md §1)
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


def main():
    # 본 hook 은 prompt 컨텍스트 전 호출 — 차단보단 알림 + 메인이 정책 인지하도록
    if os.environ.get("EDIT_RESTRICTION_BYPASS") == "1":
        return 0
    if not POLICY_PATH.exists():
        return 0
    # stderr 알림: 메인 Claude 가 정책 인지하도록
    sys.stderr.write(
        f"\n📌 [edit-restriction-hook] 메인 Claude 직접 Edit 금지 영역 reminder:\n"
        f"   - Dropbox 회중 docx · _automation/content_*.py · research-plan/script.md · outline.md ·\n"
        f"     research-{{bible,topic,application,experience,illustration,qa,prayer}}/*.md\n"
        f"   콘텐츠 정정 시 jw-style-checker / spiritual-gems-script / 해당 script 에이전트 호출 의무.\n"
        f"   정책: {POLICY_PATH}\n\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
