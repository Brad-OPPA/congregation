---
description: Codex에게 짧은 자유 질문 (read-only)
allowed-tools: Bash(codex exec --sandbox read-only *)
---

# Codex 자문 (Consult)

Codex에게 **짧은 자유 질문**. 코드든 일반 질문이든.

**다른 명령과 차이:**
- `/codex:review`: **변경 코드 diff 검수**
- `/codex:challenge`: **결정·plan 비판적 검토** (Claude의 결정 요약 필수)
- `/codex:rescue`: **에러·실패 디버깅** (시도 이력·로그 정리 필수)
- `/codex:consult`: **일회성 질문** (위 셋에 안 맞는 모든 것)

## 사용 시나리오

- "이 라이브러리 vs 저 라이브러리 어떤 게 더 좋아?"
- "이 알고리즘 시간복잡도 어떻게 줄여?"
- "이 에러 메시지 의미가 뭐야?" (단발성)
- 일반 코딩 베스트 프랙티스

## 동작

### 1. 질문 받기

`$ARGUMENTS` 비어있으면 사용자에게 질문 입력 요청.

### 2. 컨텍스트 첨부 정책

기본은 **질문만** 전달. 다음 경우에만 파일 일부 첨부:
- 사용자가 명시적으로 "이 파일 보고 답해줘" 요청
- 또는 질문이 특정 코드를 직접 참조 (예: "위 코드의 X 함수")

자동 파일 검색·전체 폴더 스캔 X.

### 3. Codex 호출 (read-only sandbox)

**환경변수로 안전 전달:**

```bash
QUESTION="$ARGUMENTS" codex exec --sandbox read-only - <<PROMPT
다음 질문에 한국어로 답해주세요.

질문: ${QUESTION}

규칙:
- 읽기 전용 — 어떤 파일도 수정하지 마세요
- .env, *.key, credentials는 읽지 마세요
- 짧고 명확하게
PROMPT
```

### 4. 결과 보고

Codex 답변을 그대로 + Claude 의견 한 줄 추가 (필요 시 보완·반박).

## 사용 예
```
/codex:consult Next.js App Router vs Pages Router 어떤 거?
/codex:consult "EADDRINUSE :::3000" 에러 어떻게 해결?
```

## 주의
- 단발성 질문에 적합. 다단계 디버깅이면 `/codex:rescue` 권장
- 깊은 토론은 Codex CLI 직접 (`codex` 인터랙티브) 권장
