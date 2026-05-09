#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent-prebrief-hook — PreToolUse hook on Task

회중 자료 작성 팀 에이전트가 호출되기 *직전*에 팀 규칙집(브리핑)을
stderr 로 자동 주입한다. 에이전트가 SKILL.md 를 읽지 않아도 핵심 패턴·금칙어·
사용자 NG 를 즉시 알고 작업을 시작하도록 강제.

대상 팀 (v2):
  - local-needs       (회중의 필요)
  - cbs               (회중 성서 연구)
  - week-study        (파수대 연구 사회)
  - mid-talk          (10분 / 5분 연설)
  - dig-treasures     (영적 보물찾기)

브리핑 구조:
  [COMMON]      — 모든 회중 팀 공통 (금칙어·NWT verbatim·6단 방어)
  [TEAM_SPEC]   — 팀별 특이 의무 (정본 경로 + 핵심 요점)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/brandon/Claude/Projects/Congregation")
META = PROJECT_ROOT / "research-meta"
SHARED = PROJECT_ROOT / ".claude" / "shared"


# ─────────────────────────────────────────────────────────────────────
# COMMON 브리핑 — 모든 회중 팀 공통 의무
# ─────────────────────────────────────────────────────────────────────

COMMON_BRIEFING = f"""\
🛡️  [회중 자료 팀 — 공통 의무]

🚫 금칙어 (정본): {SHARED}/banned-vocabulary.md
   • 예배 ❌ → 집회 ✓
   • 신앙 ❌ → 믿음 ✓ (성구 verbatim 제외)
   • 사역 ❌ → 전파 활동 ✓
   • 간증 ❌ → 경험담 ✓
   • 복음(단독) ❌ → 좋은 소식 ✓ (마태복음 등 책 이름 안은 OK)

🔴 NWT 연구용 (nwtsty) verbatim — 모든 성구 인용 의무
   • URL: https://wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/{{책}}/{{장}}
   • 책 이름 — 일반판 vs 연구용 구분 의무:
     필리피 ❌ → 빌립보서 ✓
     테살로니카 ❌ → 데살로니가전서/후서 ✓
     갈라티아 ❌ → 갈라디아서 ✓
     에페소 ❌ → 에베소서 ✓
     콜로새 ❌ → 골로새서 ✓

🛡️ 6단 방어 v2: {SHARED}/multi-layer-defense.md
   ① 본인 작성 → ② 자체 검수 → ③ planner 재검수 → ④ script →
   ⑤ planner 2차 → ⑥ 4종 게이트 (fact·style·timing·quality) PASS

🚫 메인 Claude 직접 정정 금지 (Phase E): {SHARED}/main-claude-edit-policy.md
   content_*.py / script.md / docx 메인이 직접 Edit X.

🔁 직전 주차 중복 회피 (Phase G, 모든 회중 자료 슬롯 공통)
   빌드 직후 ⑥ 4종 게이트 직전에 dedup 검사 의무:
     python3 _automation/run_dedup_for_slot.py <slot> <new.docx>
   slot: local-needs / cbs / week-study / mid-talk10 / dig-treasures /
         mid-talk5 / living-part / student
   - HIGH (≥ 0.80) → 재작성 / WARN (≥ 0.65) → 참고
"""


# ─────────────────────────────────────────────────────────────────────
# 팀별 특이 의무 (TEAM_SPECIFIC)
# ─────────────────────────────────────────────────────────────────────

LOCAL_NEEDS_SPEC = f"""\
\n📜 [회중의 필요 팀 — 특이 의무]

정본 1 — P1~P13 연설형 패턴 (2026-05-07 v6)
   {META}/local-needs-v6-speech-form-patterns.md
   • P1. 5단 성구 패턴은 도입에서만 1회
   • P2. 도입 이후 성구는 서술형 prose ("함께 보시겠습니다" 금지)
   • P3. 한 요점 = 한 성구만 INDENT 블록 낭독
   • P5. 5개 이상 항목은 "3 영역" 음성 cue
   • P7. 도입 — 익명의 관찰자 framing
   • P12. 결론 첫·끝 문장 같은 표현 반복 금지

정본 2 — 출력 경로 + Phase F (자동 빌드 한계)
   {META}/local-needs-final-output-routing.md
   • 정본 경로: ~/Dropbox/.../01.주중집회/04.회중의 필요/{{YYMMDD-MMDD}}/
   • 🚫 사용자 _final.docx 자동 갱신 금지 (markdown 패치로만)
"""

CBS_SPEC = f"""\
\n📖 [회중 성서 연구 팀 — 특이 의무]

정본 — 회중성서연구 자동화 구조 (2026-05-02)
   {META}/회중성서연구-자동화-구조.md
   • WOL docid 접두사 1102016XXX 만 사용 (다른 docid 차단)
   • publication symbol 분리: 「훈」=lfb / 「예수」=jy (혼동 금지)
   • 30분 사회자, 낭독자는 별도 형제
   • 시간 마커 8개: 4'·7'·10'·15'·18'·21'·23'·29' (빨강 볼드)
   • 책 호칭: 전면="「훈」"·"「내가 좋아하는 성경 이야기」" / 횡단="「예수」 책 NN장"
   • quality > timing (1800±120s)
   • 파일명: 회중 성서 연구_훈{{N-M}}장_{{THU_YYMMDD}}.docx
   • 빌더: build_cbs_v10.py + cbs_data_v10.py
"""

WEEK_STUDY_SPEC = f"""\
\n📜 [파수대 연구 사회 팀 — 특이 의무]

정본 — 파수대 사회 자동화 구조 (2026-05-02)
   {META}/파수대-사회-자동화-구조.md
   • WOL article docid → scrape_wt.py 베이스 스크래핑 (17블록 자동 파싱)
   • 깊이 = 외부 5 출판물 + 14축 외부 자료 결합
   • 60분 사회자 실시간 진행 대본 (예습 노트 X)
   • 색상: 사회자 노랑 / 성구 빨강 / 출판물 볼드 / 「」 인용 볼드
   • 17블록 + 5 소제목 + 3 복습 + 결론
   • host_cue 주입 95% 미달 시 add_cue 4 라운드 재호출
   • 파일명: 파수대 사회_{{SUN_YYMMDD}}.docx (일요일 발표일)
"""

MID_TALK_SPEC = f"""\
\n🎤 [10분 연설 팀 — 특이 의무]

정본 1 — 10분 연설 자동화 구조 (2026-05-01)
   {META}/10분-연설-자동화-구조.md
정본 2 — R1~R18 표준 패턴
   {META}/10분-연설-표준패턴.md

핵심 의무:
   • 본문 = 본 주차 「파」·「집교」 1:1 매핑 (외부 14축 본문 침입 금지)
   • 출처 호명 X (각주·references 만)
   • 본문/예 분리 — 외부 자료는 "예" 단락에서만
   • 6단계 narrative + 결론 = 집교 삽화 + 서론 콜백
   • 서론 5 흐름 (모범 PDF 직접 모방)
   • WOL 최근 10년 검증 의무 (할루시네이션 차단)

🚫 사용자 NG 어휘 (HIGH 즉시 차단):
   • "가정 경배" ❌ → "가족 성서 연구" ✓
   • "신자" ❌ → "형제 자매" ✓
   • "여호와의 임재" ❌ → 다른 표현
   • "수동적" ❌
"""

DIG_TREASURES_SPEC = f"""\
\n💎 [영적 보물찾기 팀 — 특이 의무]

정본 — 영적 보물찾기 자동화 (Phase E v2, 2026-05-01)
   {SHARED}/dig-treasures-automation.md

핵심 의무:
   • WOL 주차 인덱스 → 공식 질문 2개·표어 성구·통독 범위 자동 fetch
   • 20성구 선정 (planner outline 단계)
   • 5 보조 병렬: scripture-deep / publication-cross-ref / application-builder /
                  experience-collector / illustration-finder
   • script.md → content_sg_{{YYMMDD}}.py 변환
   • build_spiritual_gems.py 빌드
   • R1~R10 정량 메트릭 측정 (gem-coordinator)
   • 다각도·14축·깊이·4축 균형 (정보 측정만, 자연스러움 우선)
"""


TEAM_BRIEFINGS = {
    "local-needs": COMMON_BRIEFING + LOCAL_NEEDS_SPEC,
    "cbs": COMMON_BRIEFING + CBS_SPEC,
    "week-study": COMMON_BRIEFING + WEEK_STUDY_SPEC,
    "mid-talk": COMMON_BRIEFING + MID_TALK_SPEC,
    "dig-treasures": COMMON_BRIEFING + DIG_TREASURES_SPEC,
}


# ─────────────────────────────────────────────────────────────────────
# 팀 감지 (subagent_type / description / prompt 분석)
# ─────────────────────────────────────────────────────────────────────

def detect_team(subagent_type: str, description: str, prompt: str) -> str | None:
    haystack = " ".join([
        subagent_type or "", description or "", (prompt or "")[:500]
    ]).lower()

    # 우선순위: 더 구체적인 것부터 (week-study 가 mid-talk 보다 먼저,
    # local-needs 가 가장 먼저 — false positive 방지)
    if "local-needs" in haystack or "회중의 필요" in haystack or "회중의필요" in haystack:
        return "local-needs"
    if "week-study" in haystack or "파수대" in haystack or "watchtower" in haystack \
            or "wt-" in haystack or "wt_" in haystack:
        return "week-study"
    if "cbs" in haystack or "회중 성서 연구" in haystack or "회중성서연구" in haystack:
        return "cbs"
    if "dig-treasures" in haystack or "영적 보물" in haystack or "spiritual-gems" in haystack \
            or "gem-" in haystack:
        return "dig-treasures"
    if "mid-talk" in haystack or "10분 연설" in haystack or "10분연설" in haystack \
            or "5분 연설" in haystack or "treasures-talk" in haystack:
        return "mid-talk"

    return None


def main() -> int:
    """PreToolUse hook 정식 방식 (2026-05-09 v2):

    stdout JSON 으로 `updatedInput.prompt` 반환 → Task 도구의 prompt 필드 자체를
    팀 브리핑 + 원본 prompt 형태로 augmentation. 서브에이전트가 시작 시점에
    가이드라인 포함된 prompt 를 받음.

    이전 v1 (stderr + exit 1) 은 메인 Claude 만 보였고 서브에이전트는 못 받음 —
    실전 검증으로 발견된 한계 (HANDOFF-260509 참조).
    """
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    if data.get("tool_name", "") != "Task":
        return 0

    tool_input = data.get("tool_input", {}) or {}
    original_prompt = tool_input.get("prompt", "") or ""

    team = detect_team(
        tool_input.get("subagent_type", "") or "",
        tool_input.get("description", "") or "",
        original_prompt,
    )
    if not team:
        return 0

    briefing = TEAM_BRIEFINGS.get(team)
    if not briefing:
        return 0

    # 새 prompt = 팀 브리핑 + 구분선 + 원본 prompt
    augmented = (
        briefing
        + "\n\n"
        + "─" * 60 + "\n"
        + "위 정본 가이드라인을 반드시 준수하며 아래 task 를 수행하십시오.\n"
        + "(에이전트는 정본 파일을 본인이 Read 한 뒤 작업 시작 권장)\n"
        + "─" * 60 + "\n\n"
        + original_prompt
    )

    # Dual output (호환성 + fallback):
    #
    # 1) stdout JSON — PreToolUse hookSpecificOutput.updatedInput
    #    (Claude Code 환경이 Task prompt augmentation 을 지원하면 자동 작동.
    #     2026-05-09 검증: macOS Claude Code CLI 에서는 Task 도구의 prompt
    #     augmentation 미지원 — 그래도 미래 환경 대비 유지.)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": {**tool_input, "prompt": augmented},
        }
    }
    print(json.dumps(output, ensure_ascii=False))

    # 2) stderr — 메인 Claude 알림 (의식적 prepend 권고)
    #    위 stdout JSON 이 실제로 적용 안 됐을 경우 메인 Claude 가 이 메시지를
    #    보고 task 호출 prompt 에 직접 정본을 prepend 하도록 유도.
    sys.stderr.write(
        f"\n🛡️ [회중 자료 팀 — '{team}' 호출 감지]\n"
        f"메인 Claude 의무: Task 호출 prompt 에 다음 정본 가이드라인을 직접 prepend.\n"
        f"(Claude Code Task 도구는 hook 으로 prompt 자동 augmentation 미지원 검증됨)\n"
        f"\n팀 브리핑 (이 task prompt 맨 위에 인용 의무):\n"
    )
    sys.stderr.write("─" * 60 + "\n")
    sys.stderr.write(briefing)
    sys.stderr.write("─" * 60 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
