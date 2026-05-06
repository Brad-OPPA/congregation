---
description: Claude가 막혔을 때 Codex가 다른 접근으로 해결 시도 (주력 명령) - read-only 진단
allowed-tools: Bash(codex exec --sandbox read-only *)
---

# Codex 구조 (Rescue) ⭐ 주력 명령

Claude가 같은 에러를 반복하거나 막혔을 때, Codex에게 **다른 접근 방식**으로 해결을 의뢰.

**`/codex:consult`와 차이:** consult는 단발성 질문, rescue는 **구조화된 디버깅 의뢰** (시도 이력·로그·파일 정리 필수).

## 사용 시나리오

- Claude가 같은 버그를 3번 시도했는데 안 풀림
- 테스트가 자꾸 실패하는데 원인 파악 안 됨
- 의존성 충돌·환경 문제

## 동작

### 1. 상황 컨텍스트 정리 (필수)

rescue 호출 전 Claude는 **반드시 다음 4개 명시**:
- **목표**: 무엇을 하려 했나
- **시도**: 지금까지 어떤 접근을 했나 (실패한 것들 모두)
- **에러 / 증상**: 정확한 에러 메시지·로그
- **관련 파일 경로**: 프로젝트 내부 경로만

이 4개가 빠지면 rescue 호출 **거부** 후 사용자에게 정리 요청. 빠진 채로 부르면 consult로 강등.

### 2. Codex에게 구조 요청 (read-only sandbox)

**환경변수로 안전 전달:**

```bash
GOAL="[목표]" ATTEMPTS="[시도들]" ERRORS="[에러/증상]" FILES="[파일 경로]" \
ARGS="$ARGUMENTS" CWD="$(pwd)" \
codex exec --sandbox read-only - <<PROMPT
Claude가 다음 문제로 막혔습니다. 다른 관점·접근으로 해결책을 제시해주세요. 한국어로.

목표: ${GOAL}
시도한 접근: ${ATTEMPTS}
에러/증상: ${ERRORS}
관련 파일: ${FILES}

현재 폴더: ${CWD}
사용자 추가 지시: ${ARGS}

규칙:
- **읽기 전용** — 어떤 파일도 수정하지 마세요. 해결책은 텍스트로만 제시
- 다음 파일은 **절대 읽지 마세요**: .env, .env.*, *.key, *_secret*, *_password*, credentials, ~/.aws/*, ~/.ssh/*
- 프로젝트 루트 밖의 파일은 읽지 마세요
- 코드 수정은 Claude가 사용자 승인 후 적용
PROMPT
```

### 3. 해결책 검토·적용

Codex 답을 받으면:
1. **Claude가 시도해보지 않은 새 접근** 식별
2. 사용자에게 보여주고 **명시적 승인** 요청
3. 승인 시 Claude가 직접 코드 적용 (Codex 아님)

### 4. 안 풀리면

Codex도 못 풀면: `/codex:consult`로 일반 질문 전환 또는 사용자 직접 개입 요청.

## 사용 예
```
/codex:rescue                          # 가장 최근 막힘 상황 정리해서 호출
/codex:rescue 인증 토큰 갱신이 안 됨    # 추가 지시
```

## 차이점 요약

| 명령 | 용도 | 필수 입력 |
|---|---|---|
| `/codex:review` | 변경 diff 검수 | 미커밋 변경 |
| `/codex:rescue` | 막힘 해결책 | 목표·시도·에러·파일 4종 |
| `/codex:consult` | 단발 질문 | 질문 텍스트 |
| `/codex:challenge` | plan·결정 반박 | 결정·근거·대안 3종 |
