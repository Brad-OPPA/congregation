---
name: chair
description: 주중집회 **사회자 전체 대본** 1편 생성. 입장 안내 → 환영·시작 노래 → 시작 기도 4단 전문 → 소개말 → 성경에 담긴 보물 (10분 연설·영적 보물 찾기·성경 낭독 + 학생 칭찬·조언) → 야외봉사 학생 과제 3건 + 칭찬·조언 → 중간 노래 → 그리스도인 생활 (생활 프로 or 회중적 필요) → 회중 성서 연구 → 복습·발표 권유·다음 주 예고·임명 호명 → 광고 블록 → 마치는 노래 + 마침 기도 4단 전문까지 한 주 전체 사회자 원고. 수원 연무 회중 기준 7:30 pm 시작, 1시간 45분, 9개 고정 시간 마커. 인자 `now|next1|next2|next3` (없으면 대화형). **6단 방어(v2) 프로토콜(`.claude/shared/multi-layer-defense.md`) 준수** — ① Planner 지시서(chair-script-builder 가 ① 단계 책임) → ② 보조(prayer-composer × 2 시작·마침) 자체 검수 → ③ chair-script-builder 가 보조 산출물 재검수 → ④ chair-script-builder 가 본 대본 작성 + 자체 검수 → ⑤ chair-script-builder 가 최종 QA(재검수) → ⑥ fact-checker + jw-style-checker + timing-auditor(6300초) 최종 게이트. 마크다운 → `build_chair.py` 로 docx/PDF 변환. 트리거 "/chair", "사회자 대본", "이번 주 사회 원고", "주중 사회 대본", "생봉 사회 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# chair — 주중집회 사회자 전체 대본 (단일 주차, 6단 방어)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md`.
> **파일명에 사용자 이름 금지** — 메모리 정책 `feedback_filename_no_name.md`.

**출력 형식:** docx + PDF (자동 변환)

## 이 스킬의 범위
- 주중집회 사회자 한 편 (한 주차) 만 생성
- 다른 파트 (10분 연설·영적 보물·학생 과제·CBS·생활 등) 는 각자 스킬 별도
- 일괄 스킬(`/midweek-*`) 에는 자동 편입 X — 별도 작업

## 🛡 품질 원칙 — 6단 방어(v2) 프로토콜

이 스킬의 모든 에이전트 호출은 `.claude/shared/multi-layer-defense.md` 의 6단 방어 프로토콜을 따른다. 실행 전 반드시 Read.

**6단 요약**:
1. Planner (`chair-script-builder` 가 ① 단계 책임 — 보조에게 지시서)
2. 보조 (`prayer-composer` 시작·마침 2회) 자체 검수 (`_selfcheck.md`)
3. Planner 1차 재검수 (`_planner_review_research.md`, 미흡 시 재호출)
4. Script (`chair-script-builder` 가 본 대본 작성 + 자체 검수 `_selfcheck_script.md`)
5. Planner 2차 재검수 (기획자 최종 QA, `_planner_review_script.md`)
6. **최종 게이트** — fact-checker + jw-style-checker + timing-auditor(6300초)

> 본 스킬은 `chair-script-builder` 단일 에이전트가 Planner·Script·QA 3역을 겸한다 (정의 본문에 따라). 기존 자산이라 손대지 않고 호출 패턴만 6단 흐름에 맞춰 운용.

## 인자 규약
`now|next1|next2|next3` (없으면 대화형)

| 인자 | 의미 |
|---|---|
| `now` | 이번 주 목요일 주중집회 (오늘 날짜 기준 이번 주 목) |
| `next1` | 다음 주 목요일 |
| `next2` | 다다음 주 목요일 |
| `next3` | 그 다음 주 목요일 |

## ⚠ CRITICAL: 콘텐츠 수집 규칙 (WOL-first)

> "wol.jw.org → 집회 → 생활과 봉사 → 해당 주차" 페이지를 그대로 따라가서 본문 기반 작성

### 절대 규칙
1. WOL 주차 인덱스부터: `https://wol.jw.org/ko/wol/dt/r8/lp-ko/YYYY/M/D` (D 는 그 주의 월요일)
2. 각 파트 (10분 연설 제목, 영적 보물 찾기 질문, 성경 낭독 범위, 야외봉사 과제명·장면·학습 요점, 생활 프로 제목, CBS 자료) 를 그대로 파싱
3. 학습 요점 번호는 wol 응답에서 직접 확인 — 추론 X
4. 성경 낭독 본문 verbatim — `https://wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/{권}/{장}` 에서 신세계역 그대로 복사 (띄어쓰기·구두점·절 번호 보존)

## 🚫 할루시네이션 절대 금지 (모든 에이전트 공통)

1. wol.jw.org · 신세계역 연구용 성서 · 공식 JW 출판물에서 **실제로 확인한 내용만**.
2. 확인 못 한 항목 `[확인 필요]` placeholder.
3. 모든 인용 출처 URL + 출판물 이름 + 호수/면/항 포함.
4. 성구 신세계역 연구용 verbatim.
5. 경험담 공식 출판물 게재분만.

모든 Agent 호출 프롬프트 말미에 공통 문구 첨부:

> ⚠ 할루시네이션 절대 금지: 훈련 기억이 아니라 wol.jw.org·공식 출판물에서 실제 확인한 내용만. 확인 못 한 건 `[확인 필요]`. 모든 인용에 출처 URL + 호수/면/항. 성구 verbatim.
>
> ⚠ 6단 방어 프로토콜 준수: `.claude/shared/multi-layer-defense.md` 를 먼저 Read 해서 당신의 역할 단계 확인 후 작업.

## 🚫 상투적 청중 호명·수사 질문 금지

사회자 대본은 `chair-script-builder` 정의에 명시된 9가지 금지 표현을 절대 쓰지 않는다 (jw-style-checker HIGH 위반). 정책 정본: `.claude/shared/intro-and-illustration-quality.md` §A-4-bis · 메모리 `feedback_script_no_cliche.md`.

## 📖 저작권 정책
jw.org·wol.jw.org 공개 자료. 장문 verbatim 허용. 출처 URL 필수.

## 저장 위치

### 본 산출물 (docx + PDF)
베이스: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/00.생봉 사회/YYYYMMDD/`

파일명: `생봉 집회 사회 YYYYMMDD.docx` / `.pdf`
- 예: `생봉 집회 사회 20260507.docx`
- ⚠ **파일명에 "김원준" 금지** (메모리 `feedback_filename_no_name.md`). 기존 샘플 (예: `생봉 집회 사회 20260311_김원준.docx`) 은 기존 자산이라 그대로 보존.
- 재빌드 시 덮어쓰기 (단, 사용자가 "재생성·업그레이드·버전 올려" 명시 시 `_verN_` 부여)

### 중간 산출물 (마크다운·기도 등)
- `Congregation/research-chair/YYYYMMDD_chair.md` — 사회자 대본 본문
- `Congregation/research-chair/YYYYMMDD/_selfcheck.md` — chair-script-builder ② 자체 검수
- `Congregation/research-chair/YYYYMMDD/_planner_review_research.md` — ③ 재검수
- `Congregation/research-chair/YYYYMMDD/_selfcheck_script.md` — ④ script 자체 검수
- `Congregation/research-chair/YYYYMMDD/_planner_review_script.md` — ⑤ 기획자 최종 QA
- `Congregation/research-prayer/YYYYMMDD_midweek_opening.md` · `..._closing.md` — 시작·마침 기도 전문
- `Congregation/research-factcheck/YYYYMMDD/factcheck_chair.md` — ⑥ fact-checker
- `Congregation/research-style/YYYYMMDD/style_chair.md` — ⑥ jw-style-checker
- `Congregation/research-timing/YYYYMMDD/timing_chair.md` — ⑥ timing-auditor

## 포맷 요소 (chair-script-builder 정의 + 기존 샘플 톤)

- 기본 폰트: 맑은 고딕, 11~14pt (블록별 `chair-script-builder` 정의 따름)
- **9개 시간 마커**: 우측 정렬, 빨강 (FF0000) 볼드 — `By 7:35 pm` / `By 7:36 pm` / `By 7:46 pm` / `By 7:56 pm` / `By 8:00 pm` / `By 8:01 pm` / `By 8:16~8:20 pm` / `By 8:25 or 8:35 pm` / `By 9:05 pm` / `By 9:08 pm`
- 학생 과제 시간 합산해서 자동 계산
- 무대 지시 (`< ... >`): 회색 이탤릭 또는 들여쓰기
- 강조 성구 인용: 파란색 (2F5496), 볼드
- 학생 칭찬·조언 ①②③⑤ 블록: 번호 ② 는 조언과 인용 (팜플렛 원문 verbatim)
- 시작·마침 기도 전문: 별도 단락, 약간의 들여쓰기

## 입력 슬롯 (필수 vs 선택)

`chair-script-builder` 정의에 따라 다음 슬롯이 필요:

### 필수 (비면 생성 불가)
| 슬롯 | 예시 |
|---|---|
| `meeting_date` | "2026-05-07" (목요일) |
| `chair_name` | "김원준" |
| `prayer_opening_by` | "최표 형제" or "김원준" or "(미정)" |
| `prayer_closing_by` | "김문출 형제" |
| `songs.opening` | { number, title, scripture } |
| `songs.middle` | { number, title } |
| `songs.closing` | { number, title } |
| `parts.bible_reading.student` | "최종찬 형제" |
| `parts.apply_1`, `apply_2`, `apply_3` | 각각 type / setting / student / helper / minutes / study_point / context |
| `parts.cbs.speaker` · `reader` · `material` | "김창기 형제" / "최원규 형제" / "성경 이야기 책 11부 68-69장" |
| `next_week.assignments` | bible_reading + apply 3종 담당자 |

### 선택
- `parts.treasures_talk.speaker`, `parts.spiritual_gems.speaker` — 비어 있어도 wol 자동 파싱
- `parts.living_part` — title / speaker / minutes / subtype (living or local_needs)
- `next_week.subject` — wol 자동 파싱 가능
- `advertisements` — 원문 붙여넣기 또는 "준비중" placeholder
- `special_week` — circuit_overseer / convention / memorial (있으면 CBS 블록 치환)

### wol 에서 자동 파싱 (입력 불필요)
- 연설 제목·부제·영적 보물 찾기 질문·성경 낭독 범위
- 학생 과제 학습 요점 번호·내용·제안 장면
- 생활 프로 제목·시간·기반 자료
- 다음 주 주제·성경 읽기 범위

## 실행 단계 (6단 방어 흐름)

### 1. 인자 파싱 + 주차 확정 + 폴더 준비
- 인자 (`now|next1|next2|next3`) → 목요일 YYYYMMDD 계산
- 산출물 폴더 (`00.생봉 사회/YYYYMMDD/`) 존재 + docx 파일 확인 → skip 정책 (`.claude/shared/skip-existing-policy.md`)
- 중간 산출물 폴더 (`research-chair/YYYYMMDD/`) 생성/재사용

### 2. 입력 슬롯 수집 (대화형)
필수 슬롯 비어 있으면 사용자에게 한 번에 표로 묻는다 (글로벌 정책 #5 — 단정형 우선, 다만 대상이 8가지라 표 1회 제시 후 yes/no + 보완). wol 에서 자동 파싱 가능한 항목은 묻지 않는다.

```
필요한 입력:
- 시작 기도 / 마침 기도 담당자
- 노래 3개 번호 (opening/middle/closing)
- 학생 과제 3건 — 각각 (타입·장면·학생·보조·시간·학습 요점·맥락)
- CBS 사회·낭독자
- 다음 주 임명 4종 (성경 낭독·대화 시작·관심 자라도록·제자가 되도록)
- 광고 (원문 또는 "준비중")
- 특수 주간 여부 (순회/대회/기념식)
```

### 3. 🤖 ① 단계 — chair-script-builder Planner 호출 (지시서 작성)

```
Agent(chair-script-builder)  [Planner 모드 — ① 단계]
  프롬프트: "{YYYYMMDD} 주차 주중집회 사회자 대본 기획 (6단 방어 ① 단계).

  입력 슬롯 (위 2단계 수집분 전부 전달).

  6단 방어 ① 단계 책임 = 보조(prayer-composer × 2)에게 줄 지시서 작성.
  결과 저장: research-chair/{YYYYMMDD}/meta.yaml + outline.md

  meta.yaml 필수 키:
    meeting_date, week_start, chair_name, prayer_opening_by, prayer_closing_by,
    songs (opening/middle/closing), parts (treasures_talk/spiritual_gems/bible_reading/
    apply_1~3/living_part/cbs), next_week, advertisements, special_week,
    time_markers (9개 자동 계산)

  ⭐⭐ 추가 필수 키 — instructions_to_subresearchers (① 단계):
    prayer-composer 2회 (opening · closing) 에 대한 지시서.
    각 값은 (meeting_type=midweek, prayer_type, subject, bible_reading,
             key_points, related_bible_person, prayer_by, avoid_metaphors,
             avoid_jesus_epithets) 포함 자연어.

  ⚠ 할루시네이션 금지 / 6단 방어 준수.
  ⚠ wol.jw.org 주차 인덱스 WebFetch 로 각 파트 메타 파싱 필수."
```

### 4. 🤖 ② 단계 — prayer-composer × 2 병렬 (지시서 수신 + 자체 검수)

한 메시지에 Agent 블록 2개 동시 호출:

```
Agent(prayer-composer)  [opening]
  프롬프트: "research-chair/{YYYYMMDD}/meta.yaml 의
  instructions_to_subresearchers.prayer-composer-opening 지시서 준수.

  결과: research-prayer/{YYYYMMDD}_midweek_opening.md (기도 전문 4단 + 메타).

  ② 자체 검수: research-prayer/{YYYYMMDD}/_selfcheck_opening.md
  (이전 주차 기도와 비유·예수 수식어 중복 확인).
  ⚠ 할루시네이션 금지 / 6단 방어 준수."

Agent(prayer-composer)  [closing]
  프롬프트: "research-chair/{YYYYMMDD}/meta.yaml 의
  instructions_to_subresearchers.prayer-composer-closing 지시서 준수.
  ⚠ avoid_metaphors / avoid_jesus_epithets 에 opening 에서 사용한 것 포함 (중복 금지).

  결과: research-prayer/{YYYYMMDD}_midweek_closing.md.
  ② 자체 검수: research-prayer/{YYYYMMDD}/_selfcheck_closing.md.
  ⚠ 할루시네이션 금지 / 6단 방어 준수."
```

### 5. 🤖 ③ 단계 — chair-script-builder 1차 재검수

```
Agent(chair-script-builder)  [재검수 모드 — ③ 단계]
  프롬프트: "당신이 ① 단계에서 지시서 내린 보조 산출물을 재검수.
  경로: research-prayer/{YYYYMMDD}_midweek_opening.md · _closing.md
  + 각 _selfcheck_*.md.

  점검:
    A. opening · closing 비유·예수 수식어 중복 0
    B. 주차 주제·성경 읽기 범위·key_points 반영
    C. _selfcheck FAILED 없음
    D. 톤·호흡·인물 적절

  결과: research-chair/{YYYYMMDD}/_planner_review_research.md
    - 판정: PASS | NEEDS-RERUN
    - NEEDS-RERUN 이면 prayer-composer 재지시사항 구체적으로."
```

`PASS` → 6. `NEEDS-RERUN` → 해당 prayer-composer 재호출 (1회).

### 6. 🤖 ④ 단계 — chair-script-builder Script 작성

```
Agent(chair-script-builder)  [Script 모드 — ④ 단계]
  프롬프트: "research-chair/{YYYYMMDD}/meta.yaml · outline.md ·
  _planner_review_research.md 먼저 Read.
  research-prayer/{YYYYMMDD}_midweek_opening.md · _closing.md Read.

  본 대본 작성 = research-chair/{YYYYMMDD}_chair.md.

  본문 블록 (chair-script-builder 정의 본문 그대로):
    [블록 0] 입장 안내 + 환영 + 시작 노래 + 시작 기도 (opening 전문 그대로 삽입)
    [블록 1] 소개말 By 7:36 pm
    [블록 2] 성경에 담긴 보물 (10분 연설 → 영보 → 성경 낭독 verbatim → 칭찬·조언 ①②③⑤)
    [블록 3] 야외 봉사 진입 By 8:01 pm
    [블록 3a~3c] 학생 과제 3건 + 칭찬·조언 ①②③⑤ (학습 요점 종료 후 공개)
    [블록 4] 그리스도인 생활 섹션 전환 + 중간 노래
    [블록 5] 회중적 필요 / 생활 프로
    [블록 6] 회중 성서 연구 (CBS)
    [블록 7] 복습 + 다음 주 소개 + 임명 호명 (3분)
    [블록 8] 광고 블록
    [블록 9] 마치는 노래 + 마침 기도 (closing 전문 그대로 삽입)

  9개 시간 마커 자동 계산해서 우측 빨강 볼드 표기.
  성경 낭독 본문 verbatim 신세계역.
  학생 칭찬·조언 ①②③⑤ (긍정 피드백 원칙, ④ 사전 표기 X).
  금지 표현 8종 회피.

  ② 자체 검수: research-chair/{YYYYMMDD}/_selfcheck_script.md
  (성구 verbatim 재조회, 학습 요점 팜플렛 원문 일치, 시간 마커 9개 누락 0).

  ⚠ 할루시네이션 금지 / 6단 방어 준수."
```

### 7. 🤖 ⑤ 단계 — chair-script-builder 2차 재검수 (기획자 최종 QA)

```
Agent(chair-script-builder)  [최종 QA 모드 — ⑤ 단계]
  프롬프트: "research-chair/{YYYYMMDD}_chair.md 와 _selfcheck_script.md Read.
  outline.md · meta.yaml 대비 점검:
    A. 9개 시간 마커 전부 표기·정확
    B. 성구 인용 신세계역 verbatim
    C. 학생 칭찬·조언 ①②③⑤ 구조 (④ 표기 없음)
    D. 시작·마침 기도 전문 삽입 (research-prayer/ 본문 그대로)
    E. 금지 표현 8종 부재
    F. 다음 주 임명 4종 호명 누락 없음
    G. 광고 블록 — 원문 or 'placeholder' 명시
    H. 인용 표기 정규화 (「사람들을 사랑하십시오—X」 요점 N / 『가르치는 기술』 N과)

  결과: research-chair/{YYYYMMDD}/_planner_review_script.md
    - 판정: PASS | NEEDS-REWRITE
    - NEEDS-REWRITE 이면 chair-script-builder ④ 단계에 줄 구체 수정 지시."
```

`PASS` → 8. `NEEDS-REWRITE` → ④ 단계 재호출 (1회).

### 8. build_chair.py 호출 — docx/PDF 변환

```bash
cd "~/Claude/Projects/Congregation/_automation"
python build_chair.py --week YYYYMMDD
```

`build_chair.py` 가:
- `Congregation/research-chair/YYYYMMDD_chair.md` Read
- 9개 시간 마커 우측 빨강 볼드 적용
- 성구 인용 파랑 볼드
- 무대 지시 회색 이탤릭
- 출력: `00.생봉 사회/YYYYMMDD/생봉 집회 사회 YYYYMMDD.docx` + `.pdf` (libreoffice 또는 docx2pdf)

### 9. 🤖 ⑥ 단계 — 최종 통합 감사 (4종 병렬)

```
Agent(fact-checker)
  프롬프트: "{docx_path} 와 _chair.md 비교 — 성구 verbatim · 출판물 인용 실존 ·
  URL 유효성 · 학습 요점 팜플렛 원문 일치 · 시간 마커 정확.
  결과: research-factcheck/{YYYYMMDD}/factcheck_chair.md.
  ⚠ 훈련 기억 금지, WebFetch 로 원본 재조회."

Agent(jw-style-checker)
  프롬프트: "{docx_path} 감수.
  금칙어 8종 + 신세계역 표기 + 경어체 + 높임법 + 정치 중립 +
  상투적 청중 호명·수사 질문 9가지 부재.
  결과: research-style/{YYYYMMDD}/style_chair.md."

Agent(timing-auditor)
  프롬프트: "{docx_path} 시간 시뮬레이션. 목표 1시간 45분(6300초) 대비.
  각 블록별 시간 측정 + 9개 시간 마커 정확성.
  결과: research-timing/{YYYYMMDD}/timing_chair.md."
```

HIGH 위반 1건 이상 → 재빌드 강제 (최대 2회).

### 10. 확인 및 보고
- docx/PDF 경로
- ③ 재검수 + ⑤ 기획자 최종 QA 통과 여부
- ⑥ 최종 감수 HIGH/MEDIUM/LOW 카운트 (3종)
- 재빌드 횟수
- 시작·마침 기도 전문 생성 확인 (담당자 무관 항상 2회)

## 기억할 점
- **1시간 45분 = 6300초** (timing-auditor 목표)
- 9개 시간 마커 (`By 7:35 / 7:36 / 7:46 / 7:56 / 8:00 / 8:01 / 8:16~8:20 / 8:25 or 8:35 / 9:05 / 9:08 pm`)
- 시작·마침 기도 둘 다 항상 전문 생성 (담당자 무관)
- 학생 칭찬·조언 ①②③⑤ (긍정 피드백, ④ 표기 X)
- 학생 원고와 사회자 대본은 **독립 산출물** — chair-script-builder 가 학생 outline/script 를 Read 하지 않음. `chair_advice_candidates.md` 만 Read.
- 호칭 분기 — 과제 타입 × 학생 성별
- 인용 표기 「사람들을 사랑하십시오—X」 요점 N / 『가르치는 기술』 N과
- 파일명에 "김원준" 금지 (신규 산출물만, 기존 샘플 보존)

## 개정 이력
- 2026-04-25 v1 — 신규 작성. chair-script-builder 에이전트(기존 자산) 호출 패턴을 6단 방어 흐름에 맞춰 정의. build_chair.py 동시 신규 추가.

---

## 산출물 존재 시 skip 정책 (필수)

스킬 진입 시 출력 폴더에 산출물이 이미 있는지 먼저 확인한다.

- **없음**: 정상 진행
- **있음 + 사용자 무명시**: 단정형 확인 1회 ("이미 있는데 새로 만드시나요?") → 답 없거나 No → **skip**
- **있음 + 사용자가 "재생성·업그레이드·버전 올려" 명시**: 파일명 끝에 `_verN_` (N=2,3,...) 부여 후 신규 생성 (기존 보존)

자세한 규칙: `.claude/shared/skip-existing-policy.md`.
