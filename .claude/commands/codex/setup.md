---
description: Codex CLI 환경 점검·셋업 (로그인 상태·버전·기본 설정 확인) - read-only
allowed-tools: Bash(codex --version), Bash(codex login status), Bash(which codex), Bash(ls -la ~/.codex/), Bash(grep *)
---

# Codex 셋업 점검

Codex CLI 환경이 정상 동작 가능한지 확인. 처음 1회 실행 권장.

## 점검 항목

### 1. CLI 설치 확인
```bash
which codex
codex --version
```
설치 안 됐으면: 사용자에게 `brew install openai/tap/codex` **안내만** (자동 설치 금지).

### 2. 로그인 상태
```bash
codex login status
```
미로그인 시: 사용자에게 `codex login` **안내만** (자동 실행 금지).

### 3. 설정 파일 확인 — 사전 필터링 (raw cat 금지)

토큰·시크릿이 raw 출력되지 않도록 **사전 필터**:

```bash
ls -la ~/.codex/
# 민감 키워드 라인 제외
grep -ivE 'token|secret|password|api[_-]?key|auth' ~/.codex/config.toml | head -50
```

추가로 보고 시:
- 절대 경로의 username 부분 → `~/...`로 축약
- 이메일·이름 같은 개인 식별 정보 → 마스킹

### 4. 결과 보고

각 항목 ✅ / ⚠️ / ❌ 표시 + 마지막에 한 줄 요약.
모두 ✅면: "준비 완료, 다른 codex 명령 사용 가능".

## 사용 예
```
/codex:setup
```

## 주의
- 이 명령은 **read-only 점검**만. 어떤 셋업·설치·로그인도 자동 실행하지 않음
- 미로그인·미설치 발견 시 사용자가 직접 처리하도록 명령어만 안내
- `cat ~/.codex/config.toml` 직접 호출 X — 항상 `grep -ivE` 사전 필터 사용
