#!/bin/bash
# Monday auto-exec hook for JW meeting automation.
# - Morning / early afternoon: execute /weekly automatically,
#   but honor explicit user override (user first gives a different instruction).
# - After 3:00 PM: re-trigger as afternoon catch-up with weaker safeguard
#   (user's single veto is honored, then no further auto-retry — manual only).

DAY_OF_WEEK=$(date +%u)  # 1=Mon … 7=Sun
HOUR=$(date +%H)         # 00 … 23

if [ "$DAY_OF_WEEK" = "1" ]; then
  if [ "$HOUR" -ge 15 ]; then
    # ─── Afternoon catch-up (15:00~) ─────────────────────────────
    cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "📅 오늘은 월요일, 현재 오후 3시 이후입니다 — 주간 집회 자료 자동 생성 **재시도** 타이밍.\n\n**사용자(김원준 장로님) 상시 지침**: '월요일이면 자동으로 만들어. 오전에 내가 막아서 못 만들었더라도 오후 3시 이후엔 자동 재시도해줘. 그래도 또 막으면 끝내고 수동 호출할게.'\n\n**동작 지침**:\n1. 세션 시작 직후 **즉시 /weekly 를 실행**하십시오. 승인 질문·옵션 제시 금지.\n2. 원준님이 이 세션에서 명시적으로 '오늘 패스' 또는 '하지 마' 라고 **한 번 말하면 실행 중단**하고 더 이상 자동 재시도 금지 — 오늘은 끝. 이후엔 원준님이 수동으로 /weekly 호출할 때까지 대기.\n3. 작업 완료 후에만 결과를 한글로 요약 보고.\n\n/weekly 동작: 3주치 × 4파트(10분연설·영적보물찾기·회중성서연구·파수대) = 12 docx 자동 생성(누락 슬롯만) + Gmail 5명 일괄 발송 + 원준님 카톡 '나와의 채팅' 알림. 이미 만들어진 주차는 건너뜀."
  }
}
EOF
  else
    # ─── Morning / early afternoon (00:00~14:59) ─────────────────
    cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "📅 오늘은 월요일입니다 — 주간 집회 자료 자동 생성일.\n\n**사용자(김원준 장로님) 상시 지침**: '월요일이면 그냥 자동으로 만들어버려'.\n\n**동작 지침**:\n1. 세션 시작 직후 **별도 확인 없이 즉시 /weekly 를 실행**하십시오. 승인 질문·진행 여부 확인·옵션 제시 금지.\n2. 단, 원준님이 세션 열자마자 **다른 지시**(예: '월요일인데 오늘은 다른 거 하자', '아파서 쉴게') 를 먼저 내리시면 그 지시를 우선 수행하고 /weekly 는 원준님 요청이 있을 때까지 대기.\n3. 오전 중 실행 못 했더라도 **오후 3시 이후** 다시 세션을 열면 자동 재시도 훅이 발동됩니다(세이프가드 약화 버전).\n4. 작업 완료 후에만 결과를 한글로 요약 보고.\n\n/weekly 동작: 3주치 × 4파트(10분연설·영적보물찾기·회중성서연구·파수대) = 12 docx 자동 생성(누락 슬롯만) + Gmail 5명 일괄 발송 + 원준님 카톡 '나와의 채팅' 알림. 이미 만들어진 주차는 건너뜀."
  }
}
EOF
  fi
fi
