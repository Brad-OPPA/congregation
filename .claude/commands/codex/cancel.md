---
description: 진행 중인 Codex 호출 종료 (기본 PID 선택, 전체 종료는 별도 확인)
allowed-tools: Bash(pgrep -fl codex), Bash(kill -TERM *), Bash(kill -KILL *), Bash(pkill -f codex)
---

# Codex 취소 (Cancel)

진행 중인 Codex 호출 종료. **기본은 PID 선택 종료** — 전체 종료는 명시적 확인 필요.

## 사용 시나리오

- `/codex:review`나 `/codex:rescue` 실행 후 너무 오래 걸려서 중단
- Codex가 무한 루프나 hang 상태일 때
- 잘못 호출했을 때

## 동작 (안전 우선)

### 1. 실행 중인 Codex 프로세스 찾기

```bash
pgrep -fl codex
```

찾은 결과를 사용자에게 표시 (PID·명령어 일부).

### 2. 사용자 확인 — 어떤 걸 종료할지

목록 보여주고 **반드시 사용자 선택받기**:
- **A. 특정 PID만** (기본·권장) — 사용자가 PID 지정
- **B. 전체 종료** — 다른 터미널·다른 프로젝트의 Codex까지 모두 죽음. **명시적 "전체 죽여" 확인 필요**
- **C. 그냥 둠**

기본 동작은 **B 절대 자동 X**.

### 3. 종료

**A. 특정 PID 종료** (안전 시그널 우선):
```bash
kill -TERM <PID>
# 5초 대기 후 안 죽었으면
kill -KILL <PID>
```

**B. 전체 종료** (사용자가 명시적으로 "전체 죽여"라고 했을 때만):
```bash
pgrep -fl codex   # 다시 한번 목록 보여주고 재확인
pkill -f codex
```

**금지:**
- `kill 1`, `kill -1` 같은 PID 1 또는 시그널 1 호출 금지
- 사용자 확인 없는 `pkill -f codex` 자동 실행 금지

### 4. 종료 확인
```bash
pgrep -fl codex
```
없으면 ✅, 남아있으면 어느 PID 남았는지 보고.

## 사용 예
```
/codex:cancel
```

## 주의

- **`pkill -f codex` 자동 실행 절대 금지** — 다른 터미널·세션의 Codex까지 죽일 수 있음
- 종료 시점에 Codex가 파일 수정 중이거나 외부 명령 실행 중이면 **중간 상태가 남을 수 있음** (특히 `--sandbox workspace-write` 사용 중일 때)
- 우리 6 명령은 모두 read-only sandbox라 데이터 손실 위험은 낮음, 하지만 0이 아님
- PID 1 (init) 또는 시스템 critical 프로세스는 절대 죽이지 않음 (사용자가 잘못 입력해도 거부)
