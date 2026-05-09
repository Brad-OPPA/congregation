#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-on-task-call — Task PreToolUse + PostToolUse 통합 정본 (2026-05-09)

기존 4 hook 통합:
  - agent-prebrief-hook   (PreToolUse Task)  — 팀 brief stderr
  - agent-postcheck-hook  (PostToolUse Task) — 결과 P1~P13 검사 stderr
  - skill-standard-loader (PreToolUse Skill) — 사용자 품질 표준 stderr
  - skill-source-reminder (UserPromptSubmit) — SKILL Read 리마인더 stderr

정본 원칙 (2026-05-09):
  • stderr 출력만, exit 0/1 만 (차단 X)
  • 자동 재호출·재작성 책임 X — SKILL 절차가 직접 처리
  • 메인 Claude 의식 의존 X — 정본 brief 를 stderr 로 노출만 함
  • Task PreToolUse / Task PostToolUse / Skill PreToolUse 한 hook 에서 분기

stdin 분기:
  • hook_event_name=PreToolUse  + tool_name=Task   → 팀 brief
  • hook_event_name=PostToolUse + tool_name=Task   → 위반 검사
  • hook_event_name=PreToolUse  + tool_name=Skill  → 사용자 품질 표준 (회중 스킬만)
  • 그 외                                          → exit 0 통과
"""
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", "/Users/brandon/Claude/Projects/Congregation"))
META = PROJECT_ROOT / "research-meta"
SHARED = PROJECT_ROOT / ".claude" / "shared"
AUTOMATION = PROJECT_ROOT / "_automation"
STANDARD_FILE = SHARED / "user-quality-standard.md"
VOCAB_FILE_PATH = SHARED / "banned-vocabulary.md"


# ─────────────────────────────────────────────────────────────────────
# 회중 스킬 화이트리스트
# ─────────────────────────────────────────────────────────────────────

CONGREGATION_SKILLS = {
    "weekly", "week-study", "cbs", "mid-talk10", "mid-talk5",
    "dig-treasures", "local-needs", "living-part", "publictalk",
    "midweek-now", "midweek-next1", "midweek-next2", "midweek-next3",
    "mid-study1", "mid-study2", "mid-study3", "chair",
    "mid-student1", "mid-student2", "mid-student3", "mid-student4",
}


# ─────────────────────────────────────────────────────────────────────
# 팀 감지 (Task hook 공용)
# ─────────────────────────────────────────────────────────────────────

def detect_team(subagent_type: str, description: str, prompt: str) -> str | None:
    haystack = " ".join([
        subagent_type or "", description or "", (prompt or "")[:500]
    ]).lower()

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


# ─────────────────────────────────────────────────────────────────────
# 팀별 brief (PreToolUse Task)
# ─────────────────────────────────────────────────────────────────────

COMMON_BRIEFING = f"""\
🛡️  [회중 자료 팀 — 공통 의무]

🚫 금칙어 (정본): {SHARED}/banned-vocabulary.md
   • 예배 ❌ → 집회 ✓ / 신앙 ❌ → 믿음 ✓
   • 사역 ❌ → 전파 활동 ✓ / 간증 ❌ → 경험담 ✓

🔴 NWT 연구용 (nwtsty) verbatim — 모든 성구 인용 의무
   • URL: https://wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/{{책}}/{{장}}
   • 책 이름: 필리피 ❌→빌립보서 ✓ / 테살로니카 ❌→데살로니가전서/후서 ✓
              갈라티아 ❌→갈라디아서 ✓ / 에페소 ❌→에베소서 ✓ / 콜로새 ❌→골로새서 ✓

🛡️ 6단 방어 v2: {SHARED}/multi-layer-defense.md
🚫 메인 Claude 직접 정정 금지 (Phase E): {SHARED}/main-claude-edit-policy.md
🔁 직전 주차 중복 회피 (Phase G): python3 _automation/run_dedup_for_slot.py <slot> <new.docx>
"""

LOCAL_NEEDS_SPEC = f"""
📜 [회중의 필요 팀 — 특이 의무]
정본 — P1~P13 연설형 패턴 (v6): {META}/local-needs-v6-speech-form-patterns.md
   • P1. 5단 성구 패턴은 도입에서만 1회 / P2. 도입 이후 성구는 서술형 prose
   • P7. 도입 — 익명의 관찰자 framing / P12. 결론 첫·끝 같은 표현 반복 금지
정본 — 출력 경로: ~/Dropbox/.../01.주중집회/04.회중의 필요/{{YYMMDD-MMDD}}/
🚫 사용자 _final.docx 자동 갱신 금지 (markdown 패치로만)
"""

CBS_SPEC = f"""
📖 [회중 성서 연구 팀 — 특이 의무]
정본: {META}/회중성서연구-자동화-구조.md
   • WOL docid 접두사 1102016XXX 만 사용
   • publication symbol 분리: 「훈」=lfb / 「예수」=jy
   • 30분 사회자, 낭독자 별도 / 시간 마커 8개 빨강 볼드
   • quality > timing (1800±120s) / 빌더: build_cbs_v10.py
"""

WEEK_STUDY_SPEC = f"""
📜 [파수대 연구 사회 팀 — 특이 의무]
정본: {META}/파수대-사회-자동화-구조.md
   • WOL article docid → scrape_wt.py 17블록 자동 파싱
   • 깊이 = 외부 5 출판물 + 14축 외부 자료 결합
   • 60분 사회자 실시간 진행 대본 / 색상: 사회자 노랑 / 성구 빨강
   • host_cue 95% 미달 시 add_cue 4 라운드 재호출
"""

MID_TALK_SPEC = f"""
🎤 [10분 연설 팀 — 특이 의무]
정본 1: {META}/10분-연설-자동화-구조.md
정본 2: {META}/10분-연설-표준패턴.md
   • 본 주차 「파」·「집교」 1:1 매핑 (외부 14축 본문 침입 금지)
   • 본문/예 분리 / 출처 호명 X (각주만)
🚫 사용자 NG (HIGH 즉시 차단):
   • "가정 경배" ❌ → "가족 성서 연구" ✓ / "신자" ❌ → "형제 자매" ✓
   • "여호와의 임재" ❌ / "수동적" ❌
"""

DIG_TREASURES_SPEC = f"""
💎 [영적 보물찾기 팀 — 특이 의무]
정본: {SHARED}/dig-treasures-automation.md
   • WOL 주차 인덱스 → 공식 질문 2개·표어 성구·통독 범위 자동 fetch
   • 5 보조 병렬 호출 / build_spiritual_gems.py 빌드
   • R1~R10 정량 메트릭 (gem-coordinator)
"""

TEAM_BRIEFINGS = {
    "local-needs":   COMMON_BRIEFING + LOCAL_NEEDS_SPEC,
    "cbs":           COMMON_BRIEFING + CBS_SPEC,
    "week-study":    COMMON_BRIEFING + WEEK_STUDY_SPEC,
    "mid-talk":      COMMON_BRIEFING + MID_TALK_SPEC,
    "dig-treasures": COMMON_BRIEFING + DIG_TREASURES_SPEC,
}


# ─────────────────────────────────────────────────────────────────────
# 위반 검사 (PostToolUse Task)
# ─────────────────────────────────────────────────────────────────────

NWT_GENERAL_NAMES = {
    "필리피": "빌립보서",
    "테살로니카": "데살로니가전서/후서",
    "갈라티아": "갈라디아서",
    "에페소": "에베소서",
    "콜로새": "골로새서",
}

BANNED_VOCAB = {
    "예배": "집회",
    "신앙": "믿음",
    "사역": "전파 활동",
    "간증": "경험담",
}

USER_NG_FALLBACK = {
    "가정 경배": "가족 성서 연구",
    "신자": "형제·자매",
    "여호와의 임재": "여호와의 영광",
    "수동적": "능동적",
}

USER_NG_SECTION = "## 2-bis. 사용자 직접 명시 NG 표현 (HIGH 즉시 NG)"
USER_NG_NEXT = "## 2-ter."

P2_LOOK_PATTERN = re.compile(
    r"함께\s+[가-힣]+\s*\d+\s*[:：]\s*\d+(?:[~∼\-]\s*\d+)?\s*(?:절\s*)?(?:을|를)?\s*보시겠습니다"
)
P6_IDENTITY_PATTERN = re.compile(r"정체.{0,30}(앱|출처|어플)|((앱|출처|어플)).{0,30}정체")


def load_user_ng_vocab() -> dict:
    try:
        text = VOCAB_FILE_PATH.read_text(encoding="utf-8")
    except Exception:
        return USER_NG_FALLBACK
    start = text.find(USER_NG_SECTION)
    if start < 0:
        return USER_NG_FALLBACK
    end = text.find(USER_NG_NEXT, start)
    section = text[start:end] if end > 0 else text[start:]
    vocab: dict = {}
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| NG 표현"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) >= 3:
            ng = re.sub(r"\*\*([^*]+)\*\*", r"\1", cells[1]).strip()
            ng_core = re.split(r"\s*\(", ng)[0].strip()
            rep = re.sub(r"\*\*([^*]+)\*\*", r"\1", cells[2]).strip()
            rep_core = rep.split(" / ")[0].strip()
            if ng_core and rep_core:
                vocab[ng_core] = rep_core
    return vocab or USER_NG_FALLBACK


def check_violations(text: str) -> dict:
    user_ng = load_user_ng_vocab()
    high: list[dict] = []
    mid: list[dict] = []

    for general, study in NWT_GENERAL_NAMES.items():
        if general in text:
            idx = text.find(general)
            ctx = text[max(0, idx - 30):idx + 30].replace("\n", " ")
            high.append({"type": "P4_NWT_BOOK_NAME", "found": general, "should_be": study, "context": f"…{ctx}…"})

    for word, replacement in BANNED_VOCAB.items():
        idx = text.find(word)
        if idx >= 0:
            ctx = text[max(0, idx - 30):idx + 30].replace("\n", " ")
            high.append({"type": "BANNED_VOCAB", "found": word, "should_be": replacement, "context": f"…{ctx}…"})

    for word, replacement in user_ng.items():
        idx = text.find(word)
        if idx >= 0:
            ctx = text[max(0, idx - 30):idx + 30].replace("\n", " ")
            high.append({"type": "USER_NG_VOCAB", "found": word, "should_be": replacement, "context": f"…{ctx}…"})

    p2_matches = P2_LOOK_PATTERN.findall(text)
    if len(p2_matches) >= 2:
        mid.append({"type": "P2_MULTIPLE_LOOK", "count": len(p2_matches),
                    "note": "'함께 보시겠습니다' 는 도입에서만 1회 허용 (P2 정본)"})

    m = P6_IDENTITY_PATTERN.search(text)
    if m:
        idx = m.start()
        ctx = text[max(0, idx - 30):idx + 30].replace("\n", " ")
        mid.append({"type": "P6_IDENTITY", "found": m.group(0), "should_be": "출처", "context": f"…{ctx}…"})

    return {"high": high, "mid": mid}


def extract_response_text(data: dict) -> str:
    resp = data.get("tool_response")
    if resp is None:
        return ""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        content = resp.get("content")
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
                elif isinstance(item, str):
                    parts.append(item)
            return "\n".join(parts)
        if isinstance(content, str):
            return content
        for key in ("result", "output", "text", "message"):
            if key in resp and isinstance(resp[key], str):
                return resp[key]
        return json.dumps(resp, ensure_ascii=False)
    if isinstance(resp, list):
        return "\n".join(str(x) for x in resp)
    return str(resp)


# ─────────────────────────────────────────────────────────────────────
# 사용자 품질 표준 (PreToolUse Skill)
# ─────────────────────────────────────────────────────────────────────

def load_quality_standard_summary() -> str:
    if not STANDARD_FILE.exists():
        return f"⚠️ 표준 정본 없음: {STANDARD_FILE}"
    return f"""\
🎯 [회중 자료 사용자 품질 표준 — 매 스킬 시작 의무]

정본 (반드시 Read): {STANDARD_FILE}

핵심 (모든 빌드 의무):
   §1 형식 — 줄높이 1.0 / 시간 마커 노랑 배경+빨강 글자 / 키워드 볼드 / 삽화 임베드
   §2.1 항 안 모든 성구 깊이 다룸 — verbatim + 연구 노트 + 상호 참조 + 항 본문 연결
   §2.2 출판물 인용 — 광범위 탐색 → 가장 적합한 1개 + "왜 적합" 멘트
   §2.3 항당 모든 성구 다룸 (5개 있으면 5개 다)
   §2.4 적용 4축 (회중·전도·가정·개인) — 출판물 기반, 구체적 실천
   §6.1 파수대 — 오프닝 4축 짧게 / 결론 짧게

🔁 단조 증가 — 빌드할수록 퀄리티가 올라가야 함 (직전 주차 95% 이상)
"""


# ─────────────────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────────────────

def handle_pretool_task(data: dict) -> int:
    tool_input = data.get("tool_input", {}) or {}
    team = detect_team(
        tool_input.get("subagent_type", "") or "",
        tool_input.get("description", "") or "",
        tool_input.get("prompt", "") or "",
    )
    if not team:
        return 0

    briefing = TEAM_BRIEFINGS.get(team)
    if not briefing:
        return 0

    sys.stderr.write(
        f"\n🛡️ [validate-on-task-call] 회중 팀 '{team}' 호출 감지\n"
        f"메인 Claude 의무: 아래 정본을 task prompt 에 prepend.\n"
    )
    sys.stderr.write("─" * 60 + "\n")
    sys.stderr.write(briefing)
    sys.stderr.write("─" * 60 + "\n")
    return 0  # 차단 X — stderr 만


def handle_posttool_task(data: dict) -> int:
    tool_input = data.get("tool_input", {}) or {}
    team = detect_team(
        tool_input.get("subagent_type", "") or "",
        tool_input.get("description", "") or "",
        tool_input.get("prompt", "") or "",
    )
    if not team:
        return 0

    text = extract_response_text(data)
    if not text or len(text) < 20:
        return 0

    result = check_violations(text)
    high = result["high"]
    mid = result["mid"]
    if not high and not mid:
        return 0

    team_labels = {
        "local-needs": "회중의 필요", "cbs": "회중 성서 연구",
        "week-study": "파수대 사회", "mid-talk": "10분 연설",
        "dig-treasures": "영적 보물찾기",
    }
    label = team_labels.get(team, team)
    lines = [f"\n🔍 [validate-on-task-call] {label} 팀 결과 검사"]

    if high:
        lines.append(f"\n🚨 HIGH 위반 {len(high)}건 — 재작성 권고:")
        for v in high[:5]:
            lines.append(f"  • [{v['type']}] '{v['found']}' → '{v['should_be']}'")
            lines.append(f"      문맥: {v['context']}")
        if len(high) > 5:
            lines.append(f"  … 외 {len(high) - 5}건")
        lines.append("→ SKILL 절차의 단계 6 게이트 재호출 책임 (hook 자동 트리거 X)")

    if mid:
        lines.append(f"\n⚠️ MID 위반 {len(mid)}건 — 참고:")
        for v in mid[:3]:
            if "context" in v:
                lines.append(f"  • [{v['type']}] '{v.get('found','')}' / 문맥: {v['context']}")
            else:
                lines.append(f"  • [{v['type']}] {v.get('note', v)}")

    sys.stderr.write("\n".join(lines) + "\n")
    return 1  # stderr 알림 신호 — 차단 X


def handle_pretool_skill(data: dict) -> int:
    tool_input = data.get("tool_input", {}) or {}
    skill_name = tool_input.get("skill", "")
    if skill_name not in CONGREGATION_SKILLS:
        return 0
    summary = load_quality_standard_summary()
    sys.stderr.write("\n" + "=" * 60 + "\n")
    sys.stderr.write(summary)
    sys.stderr.write("=" * 60 + "\n")
    return 0


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    event = data.get("hook_event_name", "")
    tool = data.get("tool_name", "")

    if event == "PreToolUse" and tool == "Task":
        return handle_pretool_task(data)
    if event == "PostToolUse" and tool == "Task":
        return handle_posttool_task(data)
    if event == "PreToolUse" and tool == "Skill":
        return handle_pretool_skill(data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
