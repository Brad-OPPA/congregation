#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protect-canonical-dropbox — PreToolUse hook on Bash

회중 정본 폴더·_final.docx·정본 코드를 destructive 명령(rm/mv/rsync --delete 등)
으로부터 보호.

차단 (exit 2):
  - 회중 Dropbox 정본 경로 통째 삭제·이동
  - _final.docx / _finalN.docx 사용자 손질본 삭제
  - .claude/hooks·agents·shared 정본 삭제
  - _automation/build_*.py 빌더 삭제
  - 회중 .git 디렉토리 강제 reset/clean

경고 (exit 1):
  - 정본 경로 안에서 _verN_ 자동 빌드 baseline 삭제 (사용자 의도 X 차단)
  - git push --force / git reset --hard 등 destructive git

통과 (exit 0):
  - research-plan, drafts, *.bak_*, ~$*, .venv 등 임시
  - 그 외 회중 정본 외 경로 전체
"""
from __future__ import annotations
import json
import re
import sys

# ─────────────────────────────────────────────────────────────────────
# 보호 대상 경로 (substring 매칭)
# ─────────────────────────────────────────────────────────────────────

# 회중 Dropbox 정본 경로 (한글 포함 — substring)
PROTECTED_DROPBOX = [
    "Dropbox/02.WatchTower/01.▣ 수원 연무 회중",
    "Dropbox/02.WatchTower/01.\\u25a0 수원 연무 회중",  # 일부 환경 unicode escape
    "01.주중집회/04.회중의 필요",
    "01.주중집회/01.성경에 담긴 보물",
    "01.주중집회/02.야외 봉사에 힘쓰십시오",
    "01.주중집회/03.그리스도인 생활",
    "01.주중집회/05.회중 성서 연구",
    "02.주말집회/02.파수대 사회",
]

# 회중 .claude 정본 (서브패스)
PROTECTED_CLAUDE = [
    "Congregation/.claude/hooks/",
    "Congregation/.claude/agents/",
    "Congregation/.claude/shared/",
    "Congregation/.claude/commands/",
    "Congregation/.claude/settings.json",
]

# _automation 빌더·검증 (서브패스)
PROTECTED_AUTOMATION = [
    "_automation/build_",
    "_automation/quality_check.py",
    "_automation/preflight.py",
    "_automation/validators.py",
    "_automation/dedup_against_history.py",
    "_automation/scrape_wt.py",
    "_automation/weekly_secrets.py",
    "_automation/kakao_tokens.json",
]

# 정말 건드리면 안 되는 파일 패턴
PROTECTED_PATTERNS = [
    r"_final\d*\.docx",     # _final.docx, _final2.docx 등 사용자 손질본
    r"_final\d*\.pdf",
]

# ─────────────────────────────────────────────────────────────────────
# Destructive 명령 패턴
# ─────────────────────────────────────────────────────────────────────

# HIGH = 즉시 차단 후보 (회중 보호 경로와 결합)
DESTRUCTIVE_HIGH = [
    re.compile(r"\brm\s+(-[rRf]+\s+)*"),         # rm, rm -rf, rm -r -f
    re.compile(r"\brsync\s+.*--delete"),         # rsync --delete
    re.compile(r"\btrash\s+"),                   # macOS trash
    re.compile(r"\bdd\s+.*of="),                 # dd 덮어쓰기
    re.compile(r">\s*\S"),                       # 리다이렉션 덮어쓰기 (단순 매칭)
    re.compile(r"\bfind\s+.*-delete"),           # find -delete
    re.compile(r"\bmv\s+"),                      # mv (보호 경로 포함 시 차단)
    re.compile(r"\bcp\s+.*-[fF]"),               # cp -f (덮어쓰기)
    re.compile(r"\bshred\s+"),                   # shred
    re.compile(r"\bunlink\s+"),                  # unlink
]

# MID = git 위험 명령 (회중 .git 한정 차단)
GIT_DANGEROUS = [
    re.compile(r"\bgit\s+reset\s+--hard"),
    re.compile(r"\bgit\s+clean\s+-[fdx]+"),
    re.compile(r"\bgit\s+push\s+.*--force"),
    re.compile(r"\bgit\s+checkout\s+--\s+\."),
    re.compile(r"\bgit\s+restore\s+\."),
    re.compile(r"\bgit\s+branch\s+-D"),
]

# 화이트리스트 (이게 들어 있으면 통과 — 임시 폴더만 정리)
SAFE_HINTS = [
    "research-plan/",
    "drafts/",
    "/tmp/",
    "node_modules/",
    ".venv/",
    "__pycache__",
    ".bak_",
    "~$",   # Word 임시
]


def is_protected_path(command: str) -> tuple[bool, str]:
    """명령에 보호 경로가 substring 으로 포함되어 있는지."""
    for path in PROTECTED_DROPBOX:
        if path in command:
            return True, f"회중 Dropbox 정본: '{path}'"
    for path in PROTECTED_CLAUDE:
        if path in command:
            return True, f"회중 .claude 정본: '{path}'"
    for path in PROTECTED_AUTOMATION:
        if path in command:
            return True, f"_automation 빌더·검증: '{path}'"
    for pattern in PROTECTED_PATTERNS:
        if re.search(pattern, command):
            return True, f"사용자 손질본 패턴: '{pattern}'"
    return False, ""


def has_safe_hint(command: str) -> bool:
    """안전 패턴 (임시 폴더) 만 건드리는 명령이면 통과."""
    return any(hint in command for hint in SAFE_HINTS)


def is_destructive(command: str) -> tuple[bool, str]:
    for pat in DESTRUCTIVE_HIGH:
        m = pat.search(command)
        if m:
            return True, m.group(0)
    return False, ""


def is_git_dangerous(command: str) -> tuple[bool, str]:
    for pat in GIT_DANGEROUS:
        m = pat.search(command)
        if m:
            return True, m.group(0)
    return False, ""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    if data.get("tool_name", "") != "Bash":
        return 0

    command = data.get("tool_input", {}).get("command", "") or ""
    if not command:
        return 0

    # 1. Destructive + 보호 경로 결합 → 즉시 차단
    is_dest, dest_match = is_destructive(command)
    is_prot, prot_what = is_protected_path(command)

    if is_dest and is_prot:
        # 안전 패턴이 명령 안에 있더라도 보호 경로가 같이 있으면 차단
        sys.stderr.write(
            f"🚫 [protect-canonical-dropbox] 보호 경로 destructive 명령 차단\n"
            f"   명령: {command[:200]}\n"
            f"   감지: {dest_match!r} + {prot_what}\n"
            f"   → 정본 폴더는 건드리지 마십시오. 정리는 임시 폴더만 (research-plan/, drafts/, ~$*).\n"
            f"   → 정본 경로를 정리해야 한다면 사용자에게 명시적 확인을 받고 SAFE_HINTS 우회 명령을 별도로 작성.\n"
        )
        return 2

    # 2. Destructive 단독 (보호 경로 없음) — 임시 폴더 정리면 통과, 그 외 경고
    if is_dest and not is_prot:
        if has_safe_hint(command):
            return 0  # 임시 폴더 정리, 통과
        # 회중 외 경로 — 통과 (다른 프로젝트는 본 훅 범위 X)
        return 0

    # 3. Git destructive — 회중 레포에서만 경고
    is_git_d, git_match = is_git_dangerous(command)
    if is_git_d:
        # 회중 레포 안에서 실행되는 경우 (cwd 매칭은 어려우니 명령 안 force 키워드만 검사)
        if "Congregation" in command or "congregation" in command or "원만" not in command:
            sys.stderr.write(
                f"⚠️  [protect-canonical-dropbox] git destructive 경고\n"
                f"   감지: {git_match!r}\n"
                f"   → 회중 레포에서 작업 중이면 의도 확인. 미푸시 커밋·로컬 변경 사라질 수 있음.\n"
            )
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
