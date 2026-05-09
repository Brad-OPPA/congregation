"""
UserPromptSubmit 훅 — 회중 워크스페이스 전용.
사용자 메시지에 스킬·에이전트·매핑·훅 관련 질문이 감지되면, 응답 시작 전
SKILL.md / agents/*.md / settings.json 을 도구로 직접 읽으라는 강제 리마인더를
시스템 컨텍스트로 주입한다. 메모리·시스템 리마인더 요약만 보고 추측 답변하는 사이클 차단.
"""
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = data.get("prompt", "") or ""

PATTERNS = [
    r"/(cbs|dig-treasures|mid-talk\d+|mid-student\d+|mid-study\d+|midweek-(now|next\d)|living-part|local-needs|week-study|publictalk|weekly)\b",
    r"(스킬|에이전트|subagent|매핑|호출\s*체인|훅|hook)",
]

if any(re.search(p, prompt, flags=re.IGNORECASE) for p in PATTERNS):
    print(
        "[회중 워크스페이스 강제 리마인더]\n"
        "이 메시지는 스킬·에이전트·매핑·훅과 관련됩니다. 답하기 전 다음 중 관련된 것을 "
        "반드시 도구로 직접 읽어야 합니다:\n"
        "  - 스킬 목록: Glob '~/.claude/commands/*' 또는 .claude/commands/*\n"
        "  - 스킬 본문: '<repo>/.claude/commands/<name>/SKILL.md' Read 또는 Grep\n"
        "  - 에이전트 목록: Glob '/Users/brandon/Claude/Projects/Congregation/.claude/agents/*.md'\n"
        "  - 훅·권한 설정: '/Users/brandon/Claude/Projects/Congregation/.claude/settings.json' Read\n"
        "메모리·시스템 리마인더 요약·CLAUDE.md 표를 단독 근거로 답하지 말 것. "
        "도구 결과를 인용한 뒤에만 개수·매핑·경로를 단언하라."
    )

sys.exit(0)
