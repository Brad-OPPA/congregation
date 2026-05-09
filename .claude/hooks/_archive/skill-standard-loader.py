#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skill-standard-loader.py — PreToolUse hook on Skill

회중 슬래시 커맨드 (/weekly, /week-study, /cbs, /mid-talk10, /dig-treasures,
/local-needs, /midweek-now 등) 가 트리거되는 순간 사용자 품질 표준 정본을
메인 Claude 에 자동 주입.

사용자가 매 빌드 결과 검토하며 지적한 표준이 영구 자산으로 쌓여 다음 빌드부터
자동 적용 — "할수록 퀄리티가 올라간다" 단조 증가의 시작점.

stdout JSON: PreToolUse hookSpecificOutput 으로 args 또는 description 보강
stderr: 메인 Claude 알림용 (의식적 적용 권고)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

PROJECT = Path("/Users/brandon/Claude/Projects/Congregation")
STANDARD_FILE = PROJECT / ".claude" / "shared" / "user-quality-standard.md"

# 회중 스킬 (Skill 도구로 호출되는 슬래시 커맨드)
CONGREGATION_SKILLS = {
    "weekly", "week-study", "cbs", "mid-talk10", "mid-talk5",
    "dig-treasures", "local-needs", "living-part", "publictalk",
    "midweek-now", "midweek-next1", "midweek-next2", "midweek-next3",
    "mid-study1", "mid-study2", "mid-study3", "chair",
    "mid-student1", "mid-student2", "mid-student3", "mid-student4",
}


def load_standard_summary() -> str:
    """user-quality-standard.md 의 핵심 요약 (stderr 주입용)."""
    if not STANDARD_FILE.exists():
        return f"⚠️ 표준 정본 없음: {STANDARD_FILE}"

    return f"""\
🎯 [회중 자료 사용자 품질 표준 — 매 스킬 시작 의무]

정본 (반드시 Read): {STANDARD_FILE}

핵심 (모든 빌드 의무):
   §1 형식 — 줄높이 1.0 / 시간 마커 노랑 배경+빨강 글자 / 키워드 볼드 / 중요 구 하이라이트 / 삽화 모두 임베드
   §2.1 항 안 모든 성구 깊이 다룸 (1개만 X) — verbatim + 연구 노트 + 상호 참조 + 항 본문 연결 해설
   §2.2 출판물 인용 — 광범위 탐색(파수대·통찰·예수·하느님의사랑·여호와께가까이·깨어라!) → 가장 적합한 1개 + "왜 적합" 멘트
   §2.3 항당 모든 성구 다룸 (5개 있으면 5개 다)
   §2.4 적용 4축 (회중·전도·가정·개인) — 출판물 기반, 구체적 실천
   §6.1 파수대 — 오프닝 4축 짧게 (주제·주제 성구·요점·복습 질문 3가지) / 결론 짧게 (배운 것 + 적용 1~2 문장)

🔁 단조 증가 — 빌드할수록 퀄리티가 올라가야 함 (직전 주차 95% 이상)
   • 빌더 자동 검사: quality_monotonic_check.py 가 빌드 직후 자동 호출
   • 기준 미달 시 NO-GO + 재작성 권고

🚫 메인 Claude 의무:
   1. 표준 정본 즉시 Read (위 경로)
   2. 보조 에이전트 호출 시 prompt 에 표준 prepend (team_briefings.py 사용)
   3. 빌드 결과 단조 증가 자동 검사 통과 확인
   4. 사용자가 새 표준 명시 시 user-quality-standard.md 즉시 갱신

→ 표준 미준수 시 사용자가 또 같은 검수 반복하게 됨. 영구 자산화 의무.
"""


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    # Skill 도구만 검사
    if data.get("tool_name", "") != "Skill":
        return 0

    tool_input = data.get("tool_input", {}) or {}
    skill_name = tool_input.get("skill", "")

    # 회중 스킬 외는 통과
    if skill_name not in CONGREGATION_SKILLS:
        return 0

    # stderr 로 표준 요약 출력 (메인 Claude 의식적 적용용)
    summary = load_standard_summary()
    sys.stderr.write("\n" + "=" * 60 + "\n")
    sys.stderr.write(summary)
    sys.stderr.write("=" * 60 + "\n")

    # stdout JSON — PreToolUse 권한 결정 (allow + 추가 컨텍스트)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "회중 스킬 — 사용자 품질 표준 정본 자동 주입",
            "additionalContext": summary,
        }
    }
    print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
