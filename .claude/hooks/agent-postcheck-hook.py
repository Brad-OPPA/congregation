#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent-postcheck-hook — PostToolUse hook on Task

회중 자료 작성 팀 에이전트가 결과를 반환한 *직후* P1~P13 패턴·금칙어 위반을
빠르게 정규식 검사하여, 4종 게이트 도달 전에 메인 Claude 에 즉시 경고.

위반 발견 시 stderr 로 "재호출 권고" 메시지 출력 → 메인 Claude 가 보고 즉시
같은 에이전트 재호출 또는 jw-style-checker 호출 결정.

대상 에이전트: agent-prebrief-hook 과 동일 (현재 v1: local-needs-* 만)

검사 항목 (HIGH = 즉시 재작성 권고):
  • P4 위반 — NWT 일반판 책 이름 (필리피·테살로니카 등) → 연구용으로 교정 필요
  • 금칙어 — 예배·사역·복음(단독)·간증 등 (성구 verbatim 외 맥락)

검사 항목 (MID = 참고):
  • P2 위반 — "함께 [참조] 보시겠습니다" 가 2회 이상 (도입에서만 1회 허용)
  • P6 위반 — "정체" 가 "앱"·"출처" 근처에 등장
"""
from __future__ import annotations
import json
import re
import sys

# ─────────────────────────────────────────────────────────────────────
# 1. 검사할 팀 감지 (prebrief hook 과 동일 로직)
# ─────────────────────────────────────────────────────────────────────

def detect_team(subagent_type: str, description: str, prompt: str) -> str | None:
    """v2: 5팀 모두 감지."""
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
# 2. 위반 검사 패턴
# ─────────────────────────────────────────────────────────────────────

# HIGH: NWT 일반판 책 이름 (연구용 nwtsty 가 아님 — P4 위반)
NWT_GENERAL_NAMES = {
    "필리피": "빌립보서",
    "테살로니카": "데살로니가전서/후서",
    # "유다" 단독은 false positive 위험 (이름·지명) — 주변 문맥 필요해서 제외
    # "야고보" 는 일반판도 동일. 제외
    # "베드로" 도 동일. 제외
    # "갈라티아" → 갈라디아서 (연구용은 갈라디아서)
    "갈라티아": "갈라디아서",
    "에페소": "에베소서",
    "콜로새": "골로새서",
}

# HIGH: 금칙어 (성구 verbatim 외 맥락 — 기본은 무조건 위반으로 표시)
# 한글에서 \b 는 작동하지 X — substring 으로 검사
BANNED_VOCAB = {
    "예배": "집회",
    "신앙": "믿음",  # 성구 verbatim 제외 필요하지만 매우 보수적으로
    "사역": "전파 활동",
    "간증": "경험담",
    # "복음" 은 "좋은 소식" 안에 끼면 OK 라 단순 검사 어려움 — 일단 제외
    # "평안" 은 NWT 성구 verbatim ("평안히") 와 충돌 — 일단 제외
}

# HIGH: 사용자 직접 NG 어휘 — banned-vocabulary.md "## 2-bis" 섹션 동적 파싱
# add_user_ng.py 로 추가된 항목이 다음 hook 호출부터 즉시 적용됨.
VOCAB_FILE_PATH = "/Users/brandon/Claude/Projects/Congregation/.claude/shared/banned-vocabulary.md"
USER_NG_SECTION = "## 2-bis. 사용자 직접 명시 NG 표현 (HIGH 즉시 NG)"
USER_NG_NEXT = "## 2-ter."

# Fallback (정본 파일 read 실패 시)
USER_NG_FALLBACK = {
    "가정 경배": "가족 숭배",
    "신자": "형제·자매",
    "여호와의 임재": "여호와의 영광",
    "수동적": "능동적",
}


def load_user_ng_vocab() -> dict:
    """banned-vocabulary.md 의 2-bis 섹션 표 → {ng: replacement} dict."""
    try:
        from pathlib import Path
        text = Path(VOCAB_FILE_PATH).read_text(encoding="utf-8")
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
            rep_core = rep.split(" / ")[0].strip()  # 첫 번째 옵션
            if ng_core and rep_core:
                vocab[ng_core] = rep_core
    return vocab or USER_NG_FALLBACK


# 모듈 로드 시 한 번 (hook 매번 새 프로세스라 캐싱 의미 X)
USER_NG_VOCAB = load_user_ng_vocab()

# MID: 도입 외 "함께 [성구] 보시겠습니다" 다회 등장 (P2 위반)
P2_LOOK_PATTERN = re.compile(r"함께\s+[가-힣]+\s*\d+\s*[:：]\s*\d+(?:[~∼\-]\s*\d+)?\s*(?:절\s*)?(?:을|를)?\s*보시겠습니다")

# MID: P6 "정체" + "앱"/"출처" 인근
P6_IDENTITY_PATTERN = re.compile(r"정체.{0,30}(앱|출처|어플)|((앱|출처|어플)).{0,30}정체")


def check_violations(text: str) -> dict:
    """텍스트에서 위반 검사. 결과 dict 반환."""
    high: list[dict] = []
    mid: list[dict] = []

    # HIGH 1: NWT 일반판 책 이름
    for general, study in NWT_GENERAL_NAMES.items():
        if general in text:
            # 주변 문맥 발췌
            idx = text.find(general)
            context = text[max(0, idx - 30):idx + 30].replace("\n", " ")
            high.append({
                "type": "P4_NWT_BOOK_NAME",
                "found": general,
                "should_be": study,
                "context": f"…{context}…",
            })

    # HIGH 2: 금칙어 (substring 검사)
    for word, replacement in BANNED_VOCAB.items():
        idx = text.find(word)
        if idx >= 0:
            context = text[max(0, idx - 30):idx + 30].replace("\n", " ")
            high.append({
                "type": "BANNED_VOCAB",
                "found": word,
                "should_be": replacement,
                "context": f"…{context}…",
            })

    # HIGH 3: 사용자 직접 NG (회중 전체 공통)
    for word, replacement in USER_NG_VOCAB.items():
        idx = text.find(word)
        if idx >= 0:
            context = text[max(0, idx - 30):idx + 30].replace("\n", " ")
            high.append({
                "type": "USER_NG_VOCAB",
                "found": word,
                "should_be": replacement,
                "context": f"…{context}…",
            })

    # MID 1: P2 다회 등장
    p2_matches = P2_LOOK_PATTERN.findall(text)
    if len(p2_matches) >= 2:
        mid.append({
            "type": "P2_MULTIPLE_LOOK",
            "count": len(p2_matches),
            "note": "'함께 보시겠습니다' 는 도입에서만 1회 허용 (P2 정본)",
        })

    # MID 2: P6 정체
    if P6_IDENTITY_PATTERN.search(text):
        m = P6_IDENTITY_PATTERN.search(text)
        idx = m.start()
        context = text[max(0, idx - 30):idx + 30].replace("\n", " ")
        mid.append({
            "type": "P6_IDENTITY",
            "found": m.group(0),
            "should_be": "출처",
            "context": f"…{context}…",
        })

    return {"high": high, "mid": mid}


# ─────────────────────────────────────────────────────────────────────
# 3. PostToolUse stdin 파싱 — Claude Code 의 다양한 포맷 robust 처리
# ─────────────────────────────────────────────────────────────────────

def extract_response_text(data: dict) -> str:
    """tool_response 에서 텍스트 추출. 포맷이 dict/list/str 다양할 수 있음."""
    resp = data.get("tool_response")
    if resp is None:
        return ""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        # content: [{"type":"text","text":"..."}]
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
        # fallback: result / output 필드 시도
        for key in ("result", "output", "text", "message"):
            if key in resp and isinstance(resp[key], str):
                return resp[key]
        return json.dumps(resp, ensure_ascii=False)
    if isinstance(resp, list):
        return "\n".join(str(x) for x in resp)
    return str(resp)


# ─────────────────────────────────────────────────────────────────────
# 4. 메인
# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    if data.get("tool_name", "") != "Task":
        return 0

    tool_input = data.get("tool_input", {}) or {}
    team = detect_team(
        tool_input.get("subagent_type", ""),
        tool_input.get("description", ""),
        tool_input.get("prompt", ""),
    )
    if not team:
        return 0  # 회중 외 팀은 통과

    text = extract_response_text(data)
    if not text or len(text) < 20:
        return 0  # 결과물 없거나 너무 짧음 (검사 의미 X)
    # 실제 에이전트 결과는 보통 수백~수천자, 20자 이하는 진짜 빈 응답

    result = check_violations(text)
    high = result["high"]
    mid = result["mid"]

    if not high and not mid:
        return 0  # 위반 없음

    # 위반 보고 (팀 라벨 동적)
    team_labels = {
        "local-needs": "회중의 필요", "cbs": "회중 성서 연구",
        "week-study": "파수대 사회", "mid-talk": "10분 연설",
        "dig-treasures": "영적 보물찾기",
    }
    label = team_labels.get(team, team)
    lines = [f"🔍 [agent-postcheck] {label} 팀 에이전트 결과 검사"]

    if high:
        lines.append(f"\n🚨 HIGH 위반 {len(high)}건 — 즉시 재작성 권고:")
        for v in high[:5]:
            lines.append(f"  • [{v['type']}] '{v['found']}' → '{v['should_be']}'")
            lines.append(f"      문맥: {v['context']}")
        if len(high) > 5:
            lines.append(f"  … 외 {len(high) - 5}건")
        lines.append("")
        lines.append("→ 메인 Claude: 같은 에이전트를 정본 명시적 인용하여 재호출")
        lines.append("  또는 jw-style-checker 호출하여 자동 정정 트리거")

    if mid:
        lines.append(f"\n⚠️ MID 위반 {len(mid)}건 — 참고:")
        for v in mid[:3]:
            if "context" in v:
                lines.append(f"  • [{v['type']}] '{v.get('found','')}' / 문맥: {v['context']}")
            else:
                lines.append(f"  • [{v['type']}] {v.get('note', v)}")

    sys.stderr.write("\n".join(lines) + "\n")

    # PostToolUse 에서는 exit 코드로 도구 실행 자체를 막을 수 없음 (이미 완료됨).
    # exit 1 = 메인 Claude 에 강한 경고 신호.
    return 1 if (high or mid) else 0


if __name__ == "__main__":
    sys.exit(main())
