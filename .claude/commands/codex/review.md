---
description: Claude의 변경사항을 Codex로 cross-model 검수 (주력 명령) - 수정 제안만, 자동 적용 금지
allowed-tools: Bash(codex review *), Bash(git status *)
---

# Codex 교차 검수 ⭐ 주력 명령

Claude Code가 방금 한 작업(미커밋 변경)을 OpenAI Codex로 2차 검수. 다른 모델이 보면 Claude가 놓친 버그·로직 결함·보안 이슈를 잡아냄.

**원칙: 수정 제안만 받고, 자동 적용 X.** 사용자 확인 후 Claude가 적용.

## 동작 순서

### 1. 변경사항 확인
```bash
git status --short
```
변경 없으면 종료 (사용자에게 알림).

### 2. Codex 검수 실행 — 인자 분기 규칙

`$ARGUMENTS` 분석:

**(a) 비어있음** → 미커밋 변경 검수
```bash
codex review --uncommitted
```

**(b) `--base <BRANCH>` 또는 `--commit <SHA>` 형태** → 해당 모드
```bash
codex review $ARGUMENTS
```
예: `/codex:review --base main` → `codex review --base main`

**(c) 자유 텍스트 (예: "보안 위주")** → uncommitted + 추가 지시
```bash
codex review --uncommitted "$ARGUMENTS"
```

**판단:** `$ARGUMENTS`가 `--`로 시작하면 (b), 아니면 (c).

### 3. 결과 분류·보고 (한국어)

- 🔴 **치명적**: 버그·보안·데이터 손실
- 🟡 **검토 필요**: 로직·구조·성능
- ⚪ **선택사항**: 스타일·minor

각 이슈마다 파일·라인·제안 명시.

### 4. 수정 여부 확인

**자동 수정 절대 금지.** "수정해" 들으면 권장사항 반영, "그대로 둬" 종료.
Codex 권장이 잘못됐다고 판단되면 따르지 말고 사용자에게 보고.

## 사용 예
```
/codex:review                    # 미커밋 변경 전체
/codex:review 보안 위주           # 추가 지시
/codex:review --base main        # main 대비
```

## 주의
- Codex는 ChatGPT Plus/Pro 구독 호출 (API 비용 X), 일일 사용량 한도 있음
- 30초~수 분 소요
- Codex 의견 무조건 따르지 말 것 — Claude 판단도 함께 고려
