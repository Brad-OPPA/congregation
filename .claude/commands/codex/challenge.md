---
description: Claude의 plan·결정에 Codex가 반박·도전 (read-only, 구현 전 검토 전용)
allowed-tools: Bash(codex exec --sandbox read-only *)
---

# Codex 도전 (Challenge)

Claude가 내린 **결정·plan·접근법**(아직 구현 전)에 Codex가 비판적 검토. "왜 그게 최선인가? 다른 더 나은 길은 없는가?"

**`/codex:review`와 차이:** review는 **이미 구현된 diff** 검수, challenge는 **구현 전 plan/결정** 검토.

## 사용 시나리오

- Claude가 plan.md 작성 → 구현 전 검증
- 라이브러리·아키텍처 선택 결정 직후
- "이 접근법이 정말 최선인가?" 의심 들 때

## 동작

### 1. 도전 대상 구체화 (필수)

challenge 호출 전 Claude는 **반드시 다음 3개 명시**:
- **결정**: 무엇을 선택했나
- **근거**: 왜 그게 최선이라 판단했나
- **고려한 대안**: 어떤 옵션을 검토했나

이 3개가 없으면 challenge 호출 거부 후 사용자에게 정리 요청.

### 2. Codex에게 도전 (read-only sandbox)

**환경변수로 사용자 인자 전달 → unquoted heredoc 안전 확장:**

```bash
DECISION="[결정 요약]" RATIONALE="[근거]" ALTERNATIVES="[고려한 대안]" ARGS="$ARGUMENTS" \
codex exec --sandbox read-only - <<PROMPT
다음은 Claude가 내린 결정입니다. 비판적 관점에서 반박·대안 제시해주세요. 한국어로.

결정: ${DECISION}
근거: ${RATIONALE}
고려한 대안: ${ALTERNATIVES}

사용자 추가 지시: ${ARGS}

규칙:
- 읽기 전용 — 어떤 파일도 수정하지 마세요
- .env, *.key, credentials는 읽지 마세요
PROMPT
```

(환경변수는 셸 메타문자가 와도 추가 해석 안 됨 → 셸 주입 방어. unquoted heredoc은 변수 확장 정상)

### 3. 결과 통합

Codex의 반박을 받으면:
- **유효한 비판**: 인정하고 plan 업데이트
- **무효한 비판**: Claude 입장 유지, 이유 설명
- **회색 영역**: 사용자에게 판단 요청

각 항목별 Claude의 1차 응답 함께 제시.

## 사용 예
```
/codex:challenge                  # 가장 최근 결정 도전
/codex:challenge 성능 관점에서      # 특정 관점에서 도전
```
