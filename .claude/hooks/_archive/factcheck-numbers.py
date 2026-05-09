#!/usr/bin/env python3
"""
Stop hook — A·B 카테고리 사실 주장 사후 검증.

A: 카운팅 ("에이전트 N개" 류)
B: 존재 여부 ("X 가 있다·없다")

응답에 매칭 패턴이 있고, 같은 turn 에 검증성 도구 호출(Glob/Grep/Read/Bash/...)
이 0건이면 exit 2 + stderr 로 Claude 에 재검증 요구.

설계: feedback_count_with_tools.md + feedback_self_factcheck_pre_response.md
설치: .claude/settings.json 의 hooks.Stop 으로 등록.
"""
import json
import re
import sys
from pathlib import Path

VERIFICATION_TOOLS = {
    "Glob", "Grep", "Read", "Bash", "WebFetch", "WebSearch", "PowerShell"
}

# False positive 화이트리스트 (스킬·문서 표준 표현은 매칭 전 제거)
WHITELIST_PATTERNS = [
    r'(10|5|30|60)\s*분\s*(연설|방어|성서|회중|집회|기도)',
    r'[1-6]\s*단\s*방어',
    r'Phase\s*[1-9]',
    r'20\s*개의?\s*성구',
    r'\d{4}-\d{2}-\d{2}',
    r'오[전후]\s*\d{1,2}:\d{2}',
    r'\d{1,2}:\d{2}\s*(am|pm|AM|PM)',
    r'S-38(-KO)?\s*\d+\s*항',
    r'(이번|다음|다다음)\s*주',
    r'\d+\s*분\s*(전|후|간|동안)?',  # "10분", "30분" 시간 마커
    r'(\d+|n)\s*페이지',
    r'주차',
    r'(\d+|n)\s*번째\s*주',
]

# 검출 패턴 (이름: 정규식)
DETECTION_PATTERNS = {
    "A:counting":
        r'(에이전트|스킬|파일|폴더|단계|항목|개수|함수|변수|항|줄)\s*'
        r'(은|는|이|가)?\s*\d+\s*개',
    "A:total":
        r'총\s*\d+\s*(개|건|가지|줄)',
    "A:n_of_x":
        r'\d+\s*개의?\s*(에이전트|스킬|파일|폴더|함수|변수|항목|줄)',
    "B:existence":
        r'(에이전트|스킬|파일|폴더|함수)[가-힣]*\s*'
        r'(존재한다|존재하지\s*않|없다|있다|있습니다|없습니다)',
}


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    # 무한 루프 방지 — hook 으로 재시작된 응답에선 hook 작동 안 함
    if payload.get("stop_hook_active"):
        sys.exit(0)

    transcript_path = payload.get("transcript_path")
    if not transcript_path or not Path(transcript_path).exists():
        sys.exit(0)

    try:
        lines = Path(transcript_path).read_text(encoding="utf-8").splitlines()
    except Exception:
        sys.exit(0)

    # 뒤에서부터 마지막 user 메시지 찾기 → 현재 turn 시작점
    last_user_idx = None
    for i in range(len(lines) - 1, -1, -1):
        try:
            obj = json.loads(lines[i])
        except Exception:
            continue
        if obj.get("type") == "user":
            last_user_idx = i
            break

    if last_user_idx is None:
        sys.exit(0)

    # 현재 turn 의 assistant 텍스트 + 도구 호출 수집
    response_parts: list[str] = []
    tool_uses: set[str] = set()

    for i in range(last_user_idx + 1, len(lines)):
        try:
            obj = json.loads(lines[i])
        except Exception:
            continue
        if obj.get("type") != "assistant":
            continue

        content = obj.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue

        for block in content:
            btype = block.get("type")
            if btype == "text":
                response_parts.append(block.get("text", ""))
            elif btype == "tool_use":
                name = block.get("name", "")
                if name:
                    tool_uses.add(name)

    response_text = " ".join(response_parts)
    if not response_text.strip():
        sys.exit(0)

    # 화이트리스트 제거
    filtered = response_text
    for pat in WHITELIST_PATTERNS:
        filtered = re.sub(pat, " ", filtered)

    # 검출
    matched = [name for name, pat in DETECTION_PATTERNS.items()
               if re.search(pat, filtered)]
    if not matched:
        sys.exit(0)

    # 매칭 substring 수집 (디버그용, 최대 5개)
    matched_details: list[str] = []
    for name, pat in DETECTION_PATTERNS.items():
        for m in re.finditer(pat, filtered):
            matched_details.append(f"  - [{name}] '{m.group(0).strip()}'")
            if len(matched_details) >= 5:
                break
        if len(matched_details) >= 5:
            break

    # 같은 turn 에 검증성 도구 호출이 있었나
    if tool_uses & VERIFICATION_TOOLS:
        sys.exit(0)

    # 검증 안 했음 — 경고
    sys.stderr.write(
        "[FactCheck Hook] 응답에 사실 주장 패턴 감지: "
        + ", ".join(matched) + "\n"
        "매칭 위치:\n" + "\n".join(matched_details) + "\n"
        "이번 turn 도구 호출: "
        + (", ".join(sorted(tool_uses)) if tool_uses else "(없음)") + "\n\n"
        "검증성 도구(Glob/Grep/Read/Bash/WebFetch/PowerShell) 호출 0건.\n\n"
        "규칙: 숫자·개수·존재 여부는 머리로 답하지 말고 도구로 실측한 뒤 "
        "답해주세요.\n"
        "(memory: feedback_count_with_tools.md, "
        "feedback_self_factcheck_pre_response.md)\n\n"
        "응답 안의 카운팅/존재 주장을 Glob/Grep/Bash 로 실측하고 결과 기반으로 "
        "다시 답해주세요. 만약 매칭이 false positive (인용문·스킬 정의·고정 표현 등) "
        "라면 그 이유를 한 줄 명시하고 그대로 답해도 됩니다.\n"
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
