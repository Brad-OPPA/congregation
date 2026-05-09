#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fact-loop-enforcer — Stop hook (Phase E §S6, 2026-05-01)

fact-checker 가 HIGH 위반 보고했는데도 메인 Claude 가 무시하고 종료하려는 경우 차단.
research-factcheck/{YYMMDD}/factcheck_*.md 의 최신 보고서 파싱.

작동:
- HIGH 1건 이상 → stderr 로 "재호출 필수" 메시지 + sys.exit(2)
- HIGH 0건 → sys.exit(0) (통과)
- 보고서 없음 → sys.exit(0) (대상 작업 없음)

환경변수: FACT_LOOP_BYPASS=1 → 차단 무력화 (긴급용)
"""
import os
import re
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/Users/brandon/Claude/Projects/Congregation"))
FACT_DIR = PROJECT_ROOT / "research-factcheck"


def find_latest_report():
    if not FACT_DIR.exists():
        return None
    candidates = list(FACT_DIR.glob("*/factcheck_*.md"))
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    most_recent = candidates[0]
    age_seconds = (datetime.now().timestamp() - most_recent.stat().st_mtime)
    if age_seconds > 1800:  # 30분 이전 보고서 무시
        return None
    return most_recent


def parse_report(path):
    text = path.read_text(encoding="utf-8")
    high_count = 0
    # "HIGH: N건" 패턴 또는 표 안의 "| HIGH |"
    m = re.search(r"HIGH[:\s]*(\d+)\s*건", text)
    if m:
        high_count = int(m.group(1))
    else:
        high_count = len(re.findall(r"\|\s*HIGH\s*\|", text))
    return {"high_count": high_count, "path": str(path)}


def main():
    if os.environ.get("FACT_LOOP_BYPASS") == "1":
        return 0
    report = find_latest_report()
    if not report:
        return 0
    info = parse_report(report)
    if info["high_count"] == 0:
        return 0
    sys.stderr.write(
        f"\n⚠ [fact-loop-enforcer] fact HIGH {info['high_count']}건 감지 — 할루시네이션·verbatim 위반 위험.\n"
        f"   Report: {info['path']}\n"
        f"   조치: jw-style-checker → spiritual-gems-script (또는 해당 script) 재호출 → "
        f"content_*.py 재변환 (Agent 위임) → 빌더 재실행.\n"
        f"   메인 Claude 가 직접 정정 금지 (main-claude-edit-policy.md).\n"
        f"   (bypass: FACT_LOOP_BYPASS=1)\n\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
