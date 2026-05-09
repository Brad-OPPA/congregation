#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent-prebrief-hook — PreToolUse hook on Task

회중 자료 작성 팀 에이전트가 호출되기 *직전*에 팀 규칙집(브리핑)을
stderr 로 자동 주입한다. 에이전트가 SKILL.md 를 읽지 않아도 핵심 패턴
(P1~P13)·금칙어·사용자 NG 를 즉시 알고 작업을 시작하도록 강제.

대상 에이전트:
  - local-needs-*       (회중의 필요)  ← v1 우선 적용
  - cbs-*               (회중 성서 연구)
  - mid-talk*           (10분 / 5분 연설)
  - week-study-*        (파수대 연구)
  - dig-treasures / gem-* (영적 보물)

이 훅은 **권고형** (exit 1) — 에이전트 실행은 진행되되 메인 Claude 가
브리핑을 보고 task 프롬프트에 정본 인용을 추가하도록 유도.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/brandon/Claude/Projects/Congregation")
META = PROJECT_ROOT / "research-meta"
SHARED = PROJECT_ROOT / ".claude" / "shared"


# ─────────────────────────────────────────────────────────────────────
# 팀별 브리핑 템플릿 (정본 경로 + 핵심 의무 요약)
# ─────────────────────────────────────────────────────────────────────

LOCAL_NEEDS_BRIEFING = f"""\
🛡️  [회중의 필요 팀 — 사전 브리핑]

본 task 는 'local-needs' 팀 에이전트입니다. 시작 전 다음 정본을 반드시 준수하십시오.

📜 정본 1 — P1~P13 연설형 패턴 (2026-05-07 v6 확정)
   {META}/local-needs-v6-speech-form-patterns.md

   핵심 의무:
   • P1. 5단 성구 패턴은 **도입에서만 1회** (소개·낭독안내·verbatim·핵심추출)
   • P2. 도입 이후 성구는 **서술형 prose** ("함께 보시겠습니다" 금지, "(낭독)" 금지)
   • P3. 한 요점 = 한 성구만 INDENT 블록 낭독, 나머지는 짧은 산문 인용
   • P4. 🔴 모든 성구는 **NWT 연구용 (nwtsty) verbatim** —
        빌립보서·데살로니가·유다서 등 책 이름 표기 의무 (필리피·테살로니카 ❌)
   • P5. 5개 이상 항목은 **3 영역 음성 cue** ("첫째 영역은 ...입니다")
   • P6. 어휘: 정체❌→출처✓ / 본문 NWT verbatim 어구 (조심스러우면서도·치른다 등)
   • P7. 도입 — 익명의 관찰자 framing
   • P12. 결론 첫·끝 문장 같은 표현 반복 금지

📜 정본 2 — 출력 경로 + Phase F (2026-05-07)
   {META}/local-needs-final-output-routing.md

   핵심 의무:
   • 정본 경로: ~/Dropbox/.../01.주중집회/04.회중의 필요/{{YYMMDD-MMDD}}/
   • 🚫 사용자 _final.docx 자동 갱신 금지 — 변경은 markdown 패치(`final_to_finalN_패치.md`)로만
   • 🚫 자동 빌드 docx 를 정본으로 보고 X — baseline 자료(`_verN_`)로만 보존

📜 정본 3 — 베이스 표준 (ver4)
   {META}/local-needs-ver4-standard.md (5단 흐름·시간 마커·pptx 6장·폰트)

🚫 금칙어 (정본)
   {SHARED}/banned-vocabulary.md
   • 예배 ❌ / 신앙 ❌ → 믿음 ✓ / 사역 ❌ → 전파 활동 ✓
   • 복음(단독) ❌ → 좋은 소식 ✓ / 간증 ❌ / 평안(설명문) ❌

🛡️ 6단 방어 v2 (`{SHARED}/multi-layer-defense.md`)
   ① 본인 작성 → ② 자체 검수 → ③ planner 1차 재검수 → ④ script 작성 →
   ⑤ planner 2차 재검수 → ⑥ 4종 게이트 (fact·style·timing·quality) PASS

🚫 메인 Claude 직접 정정 금지 (Phase E)
   {SHARED}/main-claude-edit-policy.md
   — content_*.py / script.md / docx 메인이 직접 Edit X.
     의심 어휘 발견 시 jw-style-checker 또는 본 에이전트 재호출.

→ 위 정본을 task 프롬프트에 인용/링크해서 에이전트에 명시적으로 전달하십시오.
   에이전트는 읽었다 가정하지 말고 본인이 Read 의무.
"""


# 다른 팀들 (확장 여지 — 일단 v1 은 local-needs 만 활성화)
TEAM_BRIEFINGS = {
    "local-needs": LOCAL_NEEDS_BRIEFING,
    # "cbs": CBS_BRIEFING,           # TODO v2
    # "mid-talk": MID_TALK_BRIEFING, # TODO v2
    # "week-study": WT_BRIEFING,     # TODO v2
    # "dig-treasures": GEM_BRIEFING, # TODO v2
}


def detect_team(subagent_type: str, description: str, prompt: str) -> str | None:
    """에이전트 이름 / description / prompt 로 어느 팀인지 감지."""
    haystack = " ".join([
        subagent_type or "",
        description or "",
        prompt[:500] if prompt else "",  # prompt 앞부분만
    ]).lower()

    # local-needs 우선 검사 (v1)
    if "local-needs" in haystack or "회중의 필요" in haystack or "회중의필요" in haystack:
        return "local-needs"

    # 추후 확장
    # if "cbs" in haystack or "회중 성서 연구" in haystack: return "cbs"
    # if "mid-talk" in haystack or "10분 연설" in haystack: return "mid-talk"
    # if "week-study" in haystack or "파수대" in haystack: return "week-study"
    # if "dig-treasures" in haystack or "영적 보물" in haystack: return "dig-treasures"

    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # 파싱 실패 시 silent pass

    tool = data.get("tool_name", "")
    if tool != "Task":
        return 0  # Task 외 도구는 무시

    tool_input = data.get("tool_input", {}) or {}
    subagent_type = tool_input.get("subagent_type", "") or ""
    description = tool_input.get("description", "") or ""
    prompt = tool_input.get("prompt", "") or ""

    team = detect_team(subagent_type, description, prompt)
    if not team:
        return 0  # 회중 팀 외 일반 에이전트 호출은 통과

    briefing = TEAM_BRIEFINGS.get(team)
    if not briefing:
        return 0

    # 권고형 — exit 1: 메인 Claude 가 stderr 메시지를 보고 task 진행 시 반영
    sys.stderr.write(briefing)
    return 1


if __name__ == "__main__":
    sys.exit(main())
