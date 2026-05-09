#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality-loop-enforcer — Stop hook (Phase E, 2026-05-01)

quality-monotonic-checker 가 NO-GO 보고했는데도 메인 Claude 가 무시하고
종료하려는 경우를 차단. research-quality/{YYMMDD}/ 의 최신 보고서를 파싱.

작동:
- HIGH FAIL ≥ 1 AND rewrite_attempts < 5 → stderr 로 "재작성 필수" 메시지 + sys.exit(2)
- rewrite_attempts ≥ 5 → 사용자 BLOCKING 알림 (stderr) + sys.exit(2)
- HIGH FAIL = 0 → sys.exit(0) (통과)
- 보고서 없음 → sys.exit(0) (대상 작업 없음 — 통과)

환경변수:
- QUALITY_LOOP_BYPASS=1 → 차단 무력화 (긴급용)
"""
import os
import re
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/Users/brandon/Claude/Projects/Congregation"))
QUALITY_DIR = PROJECT_ROOT / "research-quality"
MAX_REWRITE_ATTEMPTS = 5


def find_latest_quality_report():
    """research-quality/{YYMMDD}/quality_*.md 중 mtime 가장 최신."""
    if not QUALITY_DIR.exists():
        return None
    candidates = list(QUALITY_DIR.glob("*/quality_*.md"))
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    # 최근 30분 안에 작성된 것만 — 옛 보고서 무시
    most_recent = candidates[0]
    age_seconds = (datetime.now().timestamp() - most_recent.stat().st_mtime)
    if age_seconds > 1800:  # 30분
        return None
    return most_recent


def parse_quality_report(path):
    """보고서에서 verdict + HIGH FAIL count + rewrite attempts 추출."""
    text = path.read_text(encoding="utf-8")
    # verdict
    verdict = "UNKNOWN"
    if re.search(r"verdict[:\s]+GO\b", text, re.IGNORECASE) or re.search(r"판정[:\s]*\*\*\s*PASS\s*\*\*", text):
        verdict = "GO"
    if re.search(r"verdict[:\s]+NO-?GO\b", text, re.IGNORECASE) or re.search(r"판정[:\s]*\*\*\s*NO-?GO\s*\*\*", text):
        verdict = "NO-GO"

    # HIGH FAIL 카운트
    high_fail_count = len(re.findall(r"HIGH\s+FAIL", text))

    # rewrite attempts (e.g., "재작성 1/5", "시도 2/5")
    m = re.search(r"(?:재작성|시도)\s*(\d+)\s*/\s*5", text)
    rewrite_attempts = int(m.group(1)) if m else 0

    return {
        "verdict": verdict,
        "high_fail_count": high_fail_count,
        "rewrite_attempts": rewrite_attempts,
        "path": str(path),
    }


def main():
    # bypass
    if os.environ.get("QUALITY_LOOP_BYPASS") == "1":
        return 0

    report_path = find_latest_quality_report()
    if not report_path:
        return 0  # 최근 quality 보고서 없음 → 통과

    info = parse_quality_report(report_path)

    if info["verdict"] != "NO-GO" and info["high_fail_count"] == 0:
        return 0  # PASS — 통과

    # NO-GO 또는 HIGH FAIL ≥ 1
    if info["rewrite_attempts"] >= MAX_REWRITE_ATTEMPTS:
        sys.stderr.write(
            f"\n🚨 [quality-loop-enforcer] BLOCKING — quality NO-GO {info['rewrite_attempts']}회 시도 후 실패.\n"
            f"   Report: {info['path']}\n"
            f"   사용자 수동 검수·결정이 필요합니다. (bypass: QUALITY_LOOP_BYPASS=1)\n\n"
        )
        return 2

    sys.stderr.write(
        f"\n⚠ [quality-loop-enforcer] quality NO-GO 감지 — HIGH FAIL {info['high_fail_count']}건, "
        f"재작성 {info['rewrite_attempts']}/{MAX_REWRITE_ATTEMPTS}회 사용.\n"
        f"   Report: {info['path']}\n"
        f"   조치: spiritual-gems-script (또는 해당 script 에이전트) 재호출하여 부족 메트릭 보강 → "
        f"content_*.py 재변환 (Agent 위임) → 빌더 재실행 → ⑥ 4종 재감사.\n"
        f"   (bypass: QUALITY_LOOP_BYPASS=1)\n\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
