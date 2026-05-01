---
name: weekly
description: 매주 월요일 실행 — 3주치 4파트 자료를 자동 생성한 뒤 **2단계 검수 게이트**를 거친다. 1단계 `/weekly` (기본, 2026-04-29 갱신): docx 생성 + **본인(eltc9584@gmail.com)에게만 메일** + 카톡 "검수 요청" 발송 (회중 4명에게는 미발송). 원준님이 본인 메일·docx 검수 후 2단계 `/weekly send` → Gmail 5명 발송 + 카톡 "발송 완료". 주중 3파트(10분연설·영적보물찾기·회중성서연구) = `/mid-study1/2/3`, 주말 1파트(파수대 연구) = `/week-study`. 학생 과제·5분 연설·생활 파트·회중의 필요·공개 강연은 범위 제외 (필요 시 개별 스킬 수동 실행).
---

# /weekly — 3주치 4파트 자동 생성 + **2단계 검수 게이트** + Gmail/카톡

## 인자 분기 — `/weekly` vs `/weekly send`

| 인자 | 단계 | 동작 |
|---|---|---|
| (없음, 기본) | **1단계 — 생성 + 본인 검수** | 3주치 × 4파트 docx 생성 (누락 슬롯만) → **본인 (eltc9584@gmail.com) 에게만 메일** + 카톡 "검수 요청". 회중 4명에게는 발송 안 함. |
| `send` | **2단계 — 5명 발송** | 본인 검수 통과 후 docx 를 Gmail 5명에게 일괄 발송 + 카톡 "발송 완료". 생성은 안 함. |

## 트리거
- **1단계 (자동)** — 매주 월요일 아침 세션 시작 시 훅이 자동으로 `/weekly` 호출 → docx 생성 + 검수 카톡
- **2단계 (수동)** — 원준님이 Dropbox 에서 docx 검수 완료 후 `/weekly send` 또는 "메일 보내" 라고 말씀 → Gmail 발송

## 포함 / 제외 범위

**포함 — 4파트 × 3주 = 12 docx**:
- 주중 3파트 (목요일):
  - `mid-study1` — ① 성경에 담긴 보물 10분 연설 (3주치 일괄)
  - `mid-study2` — ② 영적 보물찾기 (3주치 일괄)
  - `mid-study3` — ⑩ 회중성서연구 사회 30분 (3주치 일괄)
- 주말 1파트 (일요일):
  - `week-study` — 파수대 연구 사회 (3주치 일괄)

**제외**:
- 주중 학생 과제 (`mid-student1~4`) — 학생이 본인 준비
- 주중 5분 연설 (`mid-talk5`) — 남학생 본인 준비
- 주중 생활 파트 (`living-part`) — 담당자 본인 준비
- 주중 회중의 필요 (`local-needs`) — 장로의회 주제 입력 필요, 수동 실행
- 주말 공개 강연 (`publictalk`) — 담당자 스케줄 별도, 수동 실행

위 제외 파트는 원준님이 필요할 때 개별 스킬로 호출. `/weekly` 는 오직 4파트만.

## 실행 흐름

### 1. 날짜 계산 — 3주치

```bash
python _automation/weekly_dates.py --json
```
또는:
```python
from weekly_dates import get_multi_week_dates
weeks = get_multi_week_dates(n=3)
# weeks[0] = 이번 주 / weeks[1] = 다음 주 / weeks[2] = 다다음 주
```

### 2. 사전 존재 체크 → 없는 것만 생성 (중복 방지)

**원칙: 이미 생성된 자료는 재생성하지 않는다.** 3주치 × 4파트별로 예상 docx·pdf 경로를 체크하여, 둘 다 존재하면 해당 슬롯은 **스킵**.

```python
# 의사 코드
from weekly_dates import get_multi_week_dates
from send_weekly_mail import collect_weekly_files

weeks = get_multi_week_dates(n=3)
slots = ['treasures', 'gems', 'cbs', 'watchtower']  # 4개 슬롯

missing = {slot: [] for slot in slots}
for idx, d in enumerate(weeks):
    week_collected = collect_weekly_files(d['monday'], d['thursday'], d['sunday'])
    for slot in slots:
        if not week_collected.get(slot):
            missing[slot].append(idx)

print(f"누락 슬롯: {missing}")
```

### 3. 누락 파트만 스킬 호출

각 파트 스킬은 내부적으로 3주치를 한꺼번에 만드므로 **슬롯 단위가 아닌 파트 단위**로 호출 (한 번 호출 = 3주치).

어느 주차 하나라도 누락되어 있으면 해당 파트 스킬을 1회 호출:

```
if any(missing['treasures']):  Skill(mid-study1)   # 3주치 10분연설 일괄
if any(missing['gems']):       Skill(mid-study2)   # 3주치 영적보물 일괄
if any(missing['cbs']):        Skill(mid-study3)   # 3주치 회중성서연구 일괄
if any(missing['watchtower']): Skill(week-study)   # 3주치 파수대 일괄
```

최대 호출 수: **4회** (모두 누락 시). 각 스킬 내부에서 주차 UX·WOL-first·할루시네이션 금지·감수 게이트·docx 렌더까지 다 수행.

### 4. 감수 — 파트 스킬이 이미 수행

각 파트 스킬 내부에서 이미 `fact-checker` + `jw-style-checker` + (필요 시) `timing-auditor` 가 감수하므로 `/weekly` 레벨에서는 재감수 불필요. 감수 결과 HIGH 위반 건수만 요약.

### 5. 2단계 검수 게이트 — 카톡 검수 요청 → 승인 → Gmail

#### 5A. 1단계 (기본 `/weekly`) — **본인에게만** 검수 메일 + 카톡 (2026-04-29 정책 갱신)

`_automation/send_weekly_mail.py --notify-review` 실행.
- docx 수집
- **본인 (eltc9584@gmail.com) 에게만 메일 발송** — 첨부 파일명·인사말·docx 본문 전부 미리 검수 가능 (`--only-me` 자동 적용)
- 카톡 "검수 요청" 메시지 발송
- **나머지 4명 (회중 형제·자매) 에게는 발송 안 함** — 원준님 승인 대기

```bash
python _automation/send_weekly_mail.py --notify-review
python _automation/send_weekly_mail.py --notify-review --dry-run   # 카톡·메일 없이 수집 확인
```

**카톡 "검수 요청" 메시지 예시**:
```
📋 주간 집회 자료 생성 완료 — 검수 요청
📅 {주차 범위}
📎 docx N개 생성

Dropbox 폴더에서 확인하신 뒤,
Claude 에게 '메일 보내' 또는 '/weekly send'
를 말씀해 주시면 5명에게 발송됩니다.
```

**정책 의도**: 이전에는 카톡만 보내고 메일은 본인도 미발송이었으나, 첨부 파일명 슬러그·인사말·HTML 본문 미리보기 등 메일 자체를 직접 검수해야 발견 가능한 오류 (예: CBS 슬러그가 `Talk_10분프로_*` 로 잘못 표기) 가 있어, 본인 메일을 1단계로 이동.

#### 5B. 2단계 (`/weekly send`) — 승인 후 Gmail 발송

원준님이 Dropbox 에서 docx 검수 완료 후 Claude 에게 "메일 보내" 또는 `/weekly send` → `_automation/send_weekly_mail.py --send-only` 실행.
- 이미 생성된 docx 를 Gmail 5명에게 일괄 발송
- 성공 후 카톡 "발송 완료" 알림

```bash
python _automation/send_weekly_mail.py --send-only
python _automation/send_weekly_mail.py --send-only --dry-run   # HTML 미리보기
```

#### 공통 정보

- **collect_weekly_files()** — 4개 슬롯(treasures·gems·cbs·watchtower) 수집
- **파일명 규칙**:
  - `Talk_10분프로_{주제}_YYMMDD.docx`
  - `Gems_영적보물찾기_YYMMDD.docx`
  - `CBS_회중성서연구_훈{N-M}_YYMMDD.docx`
  - `WT_파수대연구_YYMMDD.docx`
- **첨부 파일 수**: 4 × 3주 = **12개**
- **메일 수신자**: 5명 (김원준·김승수·김효신·김은수·송윤호)
- **카톡 수신자**: 1명 (원준님 "나와의 채팅")

#### 정정 발송 (특수)

정정 발송은 2단계 게이트 건너뛰고 즉시 발송 (하위 호환 `--auto` 유지):
```bash
python send_weekly_mail.py --auto --subject-prefix "[정정] " --notice "정정 사유..."
```

### 6. congregation/ 리서치 자료 git 커밋

```bash
cd ~/Claude/Projects/Congregation
git add research-wol/ research-bible/ research-illustration/ \
        research-experience/ research-application/ research-qa/ \
        research-style/ research-timing/ research-topic/ \
        research-public-talk/ research-plan/ research-prayer/ \
        .claude/agents/
if git diff --cached --quiet; then
  echo "[git] congregation 변경사항 없음 — 커밋 생략"
else
  git commit -m "research: {FIRST_WEEK_LABEL} ~ {LAST_WEEK_LABEL} 3주치 4파트 자료 리서치"
  if git remote -v | grep -q origin; then
    git push origin main 2>&1 || echo "[git] push 실패 — 로컬 유지"
  else
    echo "[git] 원격 없음 — Dropbox 동기화로 백업"
  fi
fi
```

**원칙**: 변경사항 없으면 생략, 메일 실패와 독립, `git add .` 금지.

### 7. 완료 보고

Claude 가 콘솔에 다음을 출력:
- 3주치 × 4파트 주제·집회일·파일 경로
- 감수 통과 내역 (금칙어/허구 인용/삽화/시간 이슈 카운트)
- 메일 발송 결과 (성공/실패 + 수신자 5명)
- 카톡 알림 결과 (원준님 "나와의 채팅")
- congregation/ git 커밋 결과

## 수신자 (5명, 2026-04-22 기준)
- 김원준 형제 (eltc9584@gmail.com) — 본인
- 김승수 형제 (nathan0703@naver.com)
- 김효신 자매 (hyoshin9576@gmail.com)
- 김은수 자매 (linzy0314@gmail.com)
- 송윤호 형제 (ufoname999@gmail.com)

변경은 `_automation/weekly_secrets.py` 의 `RECIPIENTS` 수정.

## 카톡 수신자 (1명)
- 원준님 카카오 계정 "나와의 채팅" (본인 전용 메모)

변경은 `_automation/weekly_secrets.py` 의 `KAKAO_*` 토큰 수정.

## 오류 대응

- **특정 파트 스킬 실패** → 해당 파트 스킬 내부에서 이미 3회 재시도. `/weekly` 레벨에서는 다음 파트로 계속 진행하고 최종 보고에 실패 파트 목록.
- **WOL 주차 페이지 fetch 실패** → 각 파트 스킬에서 처리.
- **Gmail 전송 실패** → `weekly_secrets.py` 의 `GMAIL_APP_PASSWORD` 확인 후 재시도.
- **카톡 전송 실패** → 카카오 토큰 만료 가능성, `kakao_auth.py` 로 갱신 후 재시도.
- **git 커밋 실패** → 경고만 출력.
- **일부 주차 누락** → `--auto` 로그의 `[주의] 누락된 집회 슬롯` 확인. 누락 파트 스킬 수동 재실행 후 `send_weekly_mail.py --auto` 재호출.

## 설정 파일

- `_automation/weekly_dates.py` — 날짜 계산
- `_automation/send_weekly_mail.py` — Gmail SMTP + 카톡 알림 통합 발송
- `_automation/kakao_notify.py` — 카카오톡 "나와의 채팅" 메모 전송
- `_automation/kakao_auth.py` — 카카오 OAuth 토큰 갱신
- `_automation/weekly_secrets.py` — Gmail 앱 비밀번호·RECIPIENTS·카카오 토큰 (gitignore)
- `_automation/README_WEEKLY.md` — 운영 가이드

## 아키텍처 변경 노트 (2026-04-25 확정)

**확정 범위** (4파트 × 3주 = 12 docx):
- 주중: 10분 연설·영적 보물찾기·회중성서연구
- 주말: 파수대 연구 사회

**범위 밖** (필요 시 개별 스킬 수동 실행):
- 주중 학생 과제 4종, 5분 연설, 생활 파트, 회중의 필요
- 주말 공개 강연

**의사 결정**:
- 학생 과제·5분 연설·생활 파트는 각 담당자가 준비하는 영역이라 일괄 생성 범위 밖으로 결정
- 회중의 필요·공개 강연은 입력 파라미터(장로의회 주제·강연 번호) 필요로 대화형 수동 실행 유지
- 구 mid-study1/2/3 스킬이 각각 3주치 일괄 생성 구조라서 `/weekly` 오케스트레이터는 midweek-* 우회하고 **직접 호출**
- `/midweek-now` 등은 10파트 전체 생성용으로 그대로 유지 (필요 시 원준님이 개별 호출)

**파이썬 코드 상태**:
- `send_weekly_mail.py` 의 `collect_weekly_files()` 는 **이미 4파트 수집 구조**로 구현되어 있음 → 수정 불필요
- 파일명 패턴 4종이 `line 231~256` 에 고정 정의


---

## 산출물 존재 시 skip 정책 (필수)

스킬 진입 시 출력 폴더에 산출물이 이미 있는지 먼저 확인한다.

- **없음**: 정상 진행
- **있음 + 사용자 무명시**: 단정형 확인 1회 ("이미 있는데 새로 만드시나요?") → 답 없거나 No → **skip**
- **있음 + 사용자가 "재생성·업그레이드·버전 올려" 명시**: 버전 번호 +1 부여 후 신규 생성 (기존 파일 보존)

일괄 스킬(·)은 파트별로 자동 skip — 결과적으로 **없는 것만** 새로 만든다. 자세한 규칙: .


---

## 묶음 확인 절차 (skip 정책 일괄 스킬용)

이 일괄 스킬은 여러 파트를 한 번에 만들기 때문에, **각 파트마다 단정형 확인을 따로 묻지 않는다**. 시작 시점에 한 번에 표로 보고하고 사용자에게 한 번만 yes/no 받는다.

```
{스킬} 산출물 현황:
| 파트 | 주차 | 상태 |
|---|---|---|
| 10분 연설 | 260430 | ✅ 있음 |
| 영적 보물 | 260430 | ✅ 있음 |
| 학생과제 #1 | 260430 | ❌ 없음 |
| ...

기존 N개는 그대로 두고, 빠진 M개만 새로 만들면 되시죠?
```

**원준님 응답에 따른 분기:**

- 답 없음 / "응" / "그래" → 빠진 것만 신규 생성, 기존 보존
- "아니, 전부 새로 만들어" / "버전 업그레이드" → 모두 버전 +1 부여 후 신규 생성
- "특정 파트만 다시" → 명시한 파트만 버전 +1 신규 생성

**기준 — 자리 비움 시 안전:** 원준님이 자리 비우셨을 때도 답 없음 → skip 으로 자동 작동하므로 검수·발송된 docx 가 의도치 않게 덮어쓰이지 않는다.

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3.


---

## 시작 시 — 30일 경과 자동 생성 산출물 정리 점검

`/weekly` 시작 시 자동으로 정리 점검 단계를 거친다. 사용자 수정 흔적 있는 파일은 자동으로 후보에서 제외되므로 안전.

### 절차

1. `python _automation/_cleanup_old_files.py` (dry-run) 자동 실행
2. 출력 표를 사용자에게 그대로 보고
3. 단정형 확인:
   - 정리 대상 0개 → 보고 생략, 정상 진행
   - 정리 대상 ≥ 1개 → "이 N개를 휴지통으로 이동할까요? (총 X MB)" 묻기
4. 사용자 응답:
   - "응" / "삭제해" / "이동해" → `python _cleanup_old_files.py --apply` 실행
   - "아니" / "하지 마" / 무응답 → 그대로 보존, **다음 주 `/weekly` 에서 또 묻기**
5. 정리(또는 보존) 보고 후 본 weekly 4파트 작업 진행

### 자동 보존 대상 (사용자 편집 흔적 있음)

다음은 정리 후보에서 자동 제외되어 묻지도 않는다:

- 일반 폴더의 `*_ver{N}_*.docx/pdf` 중 mtime 이 ctime 보다 5초 이상 새로운 파일 (사용자가 직접 편집한 흔적)
- `_v_old/` 외부에 있는 사용자가 만든 파일

### 자세한 규칙

`.claude/shared/skip-existing-policy.md` §6-D 참조.
