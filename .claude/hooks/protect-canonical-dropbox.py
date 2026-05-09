#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
protect-canonical-dropbox — PreToolUse hook on Bash (정본 v2, 2026-05-09)

회중 정본 폴더·_final.docx·정본 코드를 destructive 명령(rm/mv/rsync --delete 등)
으로부터 보호.

설계 원칙 (정본화 v2):
  1. **read-only 첫 단어 (find/ls/grep/cat/...) 면 무조건 통과** — false positive 0.
  2. destructive 명령 + 보호 경로 결합 시에만 차단. 단독 destructive 는 통과
     (회중 외 경로 작업일 수 있음).
  3. redirect (`> /file`) 는 토큰 분리 후 명시적 검사 — 코드 안 `->` `2>&1`·정규식 `r">..."`
     같은 false positive 0.
  4. git destructive 는 cwd 가 회중 레포일 때만 경고.

차단 (exit 2):
  - 회중 Dropbox 정본 경로에서 rm/mv/rsync --delete/find -delete/cp -f 등
  - _final.docx / _finalN.docx 사용자 손질본 삭제·이동
  - .claude/hooks·agents·shared 정본 삭제·이동
  - _automation/build_*.py 빌더 삭제·이동

통과 (exit 0):
  - read-only 명령 (find / ls / grep / cat / head / tail / wc / stat / ...)
  - 임시 폴더 (research-plan/, drafts/, /tmp/, ~$*, .bak_*) 정리
  - 회중 외 경로 destructive
"""
from __future__ import annotations
import json
import re
import sys

# ─────────────────────────────────────────────────────────────────────
# 보호 대상 경로 (substring 매칭)
# ─────────────────────────────────────────────────────────────────────

PROTECTED_PATHS = [
    # Dropbox 정본
    "Dropbox/02.WatchTower/01.▣ 수원 연무 회중",
    "01.주중집회/04.회중의 필요",
    "01.주중집회/01.성경에 담긴 보물",
    "01.주중집회/02.야외 봉사에 힘쓰십시오",
    "01.주중집회/03.그리스도인 생활",
    "01.주중집회/05.회중 성서 연구",
    "02.주말집회/02.파수대 사회",
    # 회중 .claude 정본
    "Congregation/.claude/hooks/",
    "Congregation/.claude/agents/",
    "Congregation/.claude/shared/",
    "Congregation/.claude/commands/",
    "Congregation/.claude/settings.json",
    # 빌더·검증 코드
    "_automation/build_",
    "_automation/quality_check.py",
    "_automation/preflight.py",
    "_automation/validators.py",
    "_automation/dedup_against_history.py",
    "_automation/scrape_wt.py",
    "_automation/weekly_secrets.py",
    "_automation/kakao_tokens.json",
]

PROTECTED_FINAL_PATTERN = re.compile(r"_final\d*\.(docx|pdf)")

# ─────────────────────────────────────────────────────────────────────
# Read-only 명령 첫 단어 — 이게 첫 토큰이면 즉시 통과
# ─────────────────────────────────────────────────────────────────────

READ_ONLY_FIRST = {
    "find", "ls", "grep", "cat", "head", "tail", "wc", "stat",
    "file", "less", "more", "awk", "sed",
    "python3", "python", "node", "git",
    "echo", "printf", "pwd", "which", "type", "whereis",
    "diff", "cmp", "comm", "tr", "sort", "uniq", "cut",
    "tree", "du", "df", "tar", "md5", "shasum", "openssl",
    "test", "true", "false", "env", "export", "set", "unset",
    "date", "sleep", "history",
}

# ─────────────────────────────────────────────────────────────────────
# Destructive 명령 — 명령 첫 단어 (또는 ; | && || 직후 첫 단어) 만 검사
# ─────────────────────────────────────────────────────────────────────

DESTRUCTIVE_FIRST = {
    "rm", "rmdir", "unlink", "shred", "trash",
    "mv", "rename",
    "truncate",
    "dd",  # of= 만 위험하지만 일단 포함
}

# rsync 와 cp 는 옵션 보고 판단
RSYNC_DELETE = re.compile(r"\brsync\s+.*--delete")
CP_FORCE = re.compile(r"\bcp\s+(-\w*[fF]\w*\s+|--force\s+)")
SED_INPLACE = re.compile(r"\bsed\s+(-\w*i\w*|-i\b|--in-place\b)")
FIND_DELETE = re.compile(r"\bfind\s+.*-delete\b")

GIT_DANGEROUS = [
    re.compile(r"\bgit\s+reset\s+--hard"),
    re.compile(r"\bgit\s+clean\s+-[fdx]+"),
    re.compile(r"\bgit\s+push\s+.*--force"),
    re.compile(r"\bgit\s+checkout\s+--\s+\."),
    re.compile(r"\bgit\s+restore\s+\."),
    re.compile(r"\bgit\s+branch\s+-D"),
]

# ─────────────────────────────────────────────────────────────────────
# Redirect overwrite — `> /file` 형태만, lookbehind 정확히
# ─────────────────────────────────────────────────────────────────────

# `> ` (공백) + 파일경로 시작 (`/`·`~`·문자) — 단 `2>&1` `1>/dev/null` 등 제외
# lookbehind = `>` 앞 글자가 숫자·`&`·`>`·`-` 가 아니어야
REDIRECT_OVERWRITE = re.compile(
    r"(?:^|[\s;|])>\s*(?!&)(?:/dev/null\b|/dev/stderr\b)?(?P<target>[/\w~][\w/.~\-]*)"
)
# append redirect (>>) 도 동일
REDIRECT_APPEND = re.compile(
    r"(?:^|[\s;|])>>\s*(?P<target>[/\w~][\w/.~\-]*)"
)


def split_subcommands(command: str) -> list[str]:
    """명령을 ;·|·&&·||·& 로 분리 → 각 sub-command 리스트."""
    return [c.strip() for c in re.split(r"\s*(?:&&|\|\||;|\||&)\s*", command) if c.strip()]


def first_word(subcmd: str) -> str:
    if not subcmd:
        return ""
    parts = subcmd.split()
    if not parts:
        return ""
    # 절대 경로 명령 (예: /usr/bin/find) → basename
    return parts[0].split("/")[-1]


def is_protected(command: str) -> tuple[bool, str]:
    """명령에 보호 경로가 substring 으로 포함되어 있는지."""
    for p in PROTECTED_PATHS:
        if p in command:
            return True, p
    if PROTECTED_FINAL_PATTERN.search(command):
        return True, "사용자 손질본 (_final.docx)"
    return False, ""


def is_destructive(command: str) -> tuple[bool, str]:
    """첫 단어 또는 sub-command 첫 단어가 destructive 인지.

    read-only 첫 단어 (find/ls/grep/...) 는 즉시 False.
    """
    subs = split_subcommands(command)
    if not subs:
        return False, ""

    for sub in subs:
        fw = first_word(sub)
        if fw in READ_ONLY_FIRST:
            # sed -i 예외
            if fw == "sed" and SED_INPLACE.search(sub):
                return True, "sed -i (in-place)"
            # find -delete 예외
            if fw == "find" and FIND_DELETE.search(sub):
                return True, "find -delete"
            # git destructive 예외
            if fw == "git":
                for gp in GIT_DANGEROUS:
                    m = gp.search(sub)
                    if m:
                        return True, m.group(0)
            # 그 외 read-only 통과
            continue
        if fw in DESTRUCTIVE_FIRST:
            return True, fw
        # rsync --delete
        if fw == "rsync" and RSYNC_DELETE.search(sub):
            return True, "rsync --delete"
        # cp -f
        if fw == "cp" and CP_FORCE.search(sub):
            return True, "cp -f"
        # redirect overwrite
        m = REDIRECT_OVERWRITE.search(sub)
        if m:
            return True, f"> {m.group('target')[:50]}"
        m = REDIRECT_APPEND.search(sub)
        if m:
            return True, f">> {m.group('target')[:50]}"

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

    is_dest, dest_match = is_destructive(command)
    if not is_dest:
        return 0

    is_prot, prot_what = is_protected(command)
    if not is_prot:
        # destructive 단독 (보호 경로 외) → 통과
        return 0

    # destructive + 보호 경로 → 차단
    sys.stderr.write(
        f"🚫 [protect-canonical-dropbox] 보호 경로 destructive 명령 차단\n"
        f"   명령: {command[:200]}\n"
        f"   감지: {dest_match!r} + 보호 경로: {prot_what!r}\n"
        f"   → 정본 폴더는 건드리지 마십시오. 정리는 임시 폴더만 "
        f"(research-plan/, drafts/, /tmp/, ~$*).\n"
        f"   → 정본 경로를 정리해야 한다면 사용자에게 명시적 확인을 받고 "
        f"별도 명령 작성.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
