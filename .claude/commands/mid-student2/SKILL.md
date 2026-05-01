---
name: mid-student2
description: 주중집회 야외봉사 섹션 **학생 과제 #1 (WOL 4번 슬롯)** 원고 1건을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3`. **4단 방어 프로토콜(`.claude/shared/multi-layer-defense.md`)** 준수. WOL 에서 과제 타입 자동 파싱 (apply_conversation_start / apply_follow_up / apply_bible_study / apply_explaining_beliefs). student-assignment-planner(과제번호 2) → 3개 보조 리서치(scripture-deep·experience-collector·application-builder) → Planner 재검수 → student-assignment-script → Planner 재검수 → docx → fact-checker·jw-style-checker·timing-auditor 최종 감수. 결과 `학생 과제_{타입}_YYMMDD.docx`. 트리거 "/mid-student2", "학생과제 1 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# mid-student2 — 야외봉사 학생 과제 #1 (WOL 4번 슬롯, 4단 방어)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx (빌더 작성 후 PDF 자동 추가 예정)

## 이 스킬의 범위
- 야외봉사 학생 과제 3건 중 **첫 번째** (WOL 프로그램 4번 슬롯)
- 타입 WOL 자동 파싱:
  - `apply_conversation_start` 대화 시작하기
  - `apply_follow_up` 관심이 자라도록 돕기
  - `apply_bible_study` 제자가 되도록 돕기
  - `apply_explaining_beliefs` 우리의 신앙 설명하기 (실연 또는 연설)
- 성경 낭독은 `/mid-student1`, 5분 연설은 `/mid-talk5`

## 🛡 품질 원칙 — 4단 방어 프로토콜
`.claude/shared/multi-layer-defense.md` 준수. 실행 전 Read.
**4단**: ① Planner 지시서 → ② 서브 자체 검수 → ③ Planner 재검수 → ④ 3종 최종 감사

## 인자 규약
`now|next1|next2|next3`

## ⚠ WOL-first 수집
1. 주차 인덱스 → "야외봉사 → 4번 슬롯" href
2. 과제 타입·시간(3~4분)·장면(setting: 가정/공원/직장/비공식)·학습 요점 WOL verbatim
3. WOL 지정 setting 만 사용, 임의 변경 금지
4. 성구·상황 제시문 WOL 원문 그대로

## 🚫 할루시네이션 금지 (공통)
과제 타입·장면·시간·학습 요점 WOL verbatim. 대사는 학습 요점 원칙 적용. [확인 필요] placeholder 허용.

모든 Agent 말미:
> ⚠ 할루시네이션 금지 / ⚠ 4단 방어 프로토콜 준수

## 저장 위치
베이스: `C:\Users\yoone\Dropbox\02.WatchTower\01.▣ 수원 연무 회중\01.주중집회\02.야외 봉사에 힘쓰십시오\01.학생 과제\YYMMDD_M월 D-D일\`
파일명: `학생 과제_{타입}_YYMMDD.docx`
- 타입: apply_conversation_start→대화시작 / apply_follow_up→관심자라기 / apply_bible_study→제자되도록돕기 / apply_explaining_beliefs→신앙설명

## 실행 단계 (4단 방어)

### 1. 주차 확정 + 폴더

### 2. 🤖 ① + ② — student-assignment-planner 1차 (지시서)

```
Agent(student-assignment-planner)
  프롬프트: "{YYMMDD} 학생 과제 #1 (WOL 4번 슬롯) 기획 1차 (4단 방어 ①).
  과제번호 2 고정. 타입 WOL 자동 파싱.

  수집:
    - 과제 타입 + 장면 setting + 시간(3~4분) + 학습 요점 번호·원문
    - 제시 성구·상황 (WOL 원문)
    - 상대자 역할 (보조자/집주인)
    - apply_explaining_beliefs 는 demonstration/talk 분기

  저장: `research-plan/student-assignment/{YYMMDD}_2_{타입}/` outline.md + meta.yaml
  meta.yaml: week_date, assignment_number=2, assignment_type, subtype(explaining 시),
             setting, time_minutes, study_point, scenario_prompt,
             helper_required, placeholders{student, helper}, gender_restriction=none

  ⭐⭐ instructions_to_subresearchers (① 필수):
    3개 서브(scripture-deep·experience-collector·application-builder) 지시서.
    실연 대사 품질 보강 목적.

  ⚠ 할루시네이션 / 4단 방어."
```

### 2.5. 🤖 role-play-scenario-designer 호출 — 가상 상황극 시나리오 설계

student-assignment-planner 산출 meta.yaml 을 근거로 3~5개 가상 시나리오 설계. 다음 단계 script 에이전트가 이 시나리오 중 하나를 선택해 대사 작성.

```
Agent(role-play-scenario-designer)
  프롬프트: "research-plan/student-assignment/{YYMMDD}_2_{타입}/meta.yaml 을 먼저 Read.
  .claude/shared/student-role-play-style.md 와 .claude/shared/multi-layer-defense.md 도 Read.

  assignment_type 과 setting (호별방문/공개증거/비공식) 에 맞는 가상 상황극 시나리오
  3~5개 설계. 각 시나리오는 scene·householder_profile·initial_trigger·emotional_arc·
  study_point_natural_fit·recommended_opening·household_reaction_bank 포함.

  결과: research-plan/student-assignment/{YYMMDD}_2_{타입}/scenarios.yaml
  recommended_default (기본 선택 id) + selection_rationale 명시.

  ② 자체 검수:
    - meta.yaml 의 setting 과 일치 / 3~5개가 서로 다른 집주인 유형 커버 /
      조언과 체현 자연스러움 / 회중 특정 언급 없음
    _selfcheck_scenarios.md 작성.
  ⚠ 할루시네이션 / 4단 방어 / 스타일 가이드 준수."
```

이 단계는 `apply_explaining_beliefs(연설)` 일 때는 **생략** (회중 대상이라 시나리오 불필요). meta.yaml 의 `subtype: talk` 이면 skip.

### 3. 🤖 ② — 3개 보조 병렬 (지시서 수신 + 자체 검수)

```
Agent(scripture-deep)
  프롬프트: "meta.yaml + instructions.scripture-deep.
  scenario_prompt 의 제시 성구가 있다면 그 성구 심층 (NWT 연구용 + 연구 노트 + 상호 참조).
  research-bible/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 4단 방어."

Agent(experience-collector)
  프롬프트: "meta.yaml + instructions.experience-collector.
  assignment_type 과 setting 에 부합하는 비슷한 상황 공식 경험담 2-3개.
  '이런 반응에 이렇게 응답' 패턴 중심.
  research-experience/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 4단 방어."

Agent(application-builder)
  프롬프트: "meta.yaml + instructions.application-builder.
  거부·관심 유발 실제 적용 + 상대자 반응 예시 (대사 현실성).
  research-application/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 4단 방어."
```

### 4. 🤖 ③ — student-assignment-planner 재검수

```
Agent(student-assignment-planner)  [재검수]
  프롬프트: "3개 서브 + _selfcheck Read. meta.yaml 지시서 대비 A~E 점검.
  `_planner_review_research.md`: PASS | NEEDS-RERUN + 재지시."
```

### 5. 🤖 ① + ② — student-assignment-script

```
Agent(student-assignment-script)
  프롬프트: "outline.md + meta.yaml + _planner_review_research.md Read.
  research_dirs 3개 (+ _selfcheck) Read.
  scenarios.yaml 도 Read (role-play-scenario-designer 산출).
  recommended_default 시나리오를 기본 선택, 필요시 다른 id 로 변경 가능.
  선택한 시나리오의 scene·householder_profile·initial_trigger·emotional_arc·
  household_reaction_bank 를 대사 작성 근거로 삼는다.

  ⭐⭐ **실연 대사 스타일 가이드 준수 필수**:
  `.claude/shared/student-role-play-style.md` 를 먼저 Read 하고 그 규칙대로 작성.
  (원준님 샘플 4개 기반 — 화자 라벨 `전도인:` / `집주인:` / `보조자:` 풀네임,
   구어체 축약, 감탄·호응, 교재 질문 그대로, 성구 verbatim·절 번호 인라인,
   학습 요점 체현, 호칭 맞춤 등)

  타입별 포맷:
    [실연: conversation_start/follow_up/bible_study/explaining_beliefs(demo)]
      헤더 (과제 번호·타입·장면·시간·학습 요점 번호·학습 요점 본문)
      + 장면 설정 문장 (한 줄)
      + 대사 블록 — 화자 `전도인:` / `집주인:` (/ `보조자:`) 풀네임 라벨
        * 스타일 가이드의 흐름 구조 A (연구·재방문) 또는 B (공개 증거) 적용
        * 한 대사 2~4문장, 구어체, 감탄·호응 풍부
        * 성구 낭독은 신세계역 연구용 verbatim, 절 번호 인라인
        * 낭독자 교대 ('여기를 어르신께서 읽어주시겠어요' / '여기는 제가 낭독해드릴께요')
        * ⚠ `[요점 적용: ...]` 인라인 주석 금지 — 학습 요점은 대사로 자연스럽게 체현
        * 영상·삽화 있으면 대사로 반드시 언급
        * 상대자 대사는 자기 경험·저항·일상 관점 담기 (일방적 긍정 금지)
      + 마지막 단계 대사 (관심 유발·후속 제안)

    [연설: explaining_beliefs(talk)]
      2~5분 서술형 축약 (서론·본론·결론)
      학습 요점 체현, 한 문장 60음절 이내

  담당자·보조자는 `___________` placeholder.
  결과: research-plan/student-assignment/{YYMMDD}_2_{타입}/script.md.

  ② 자체 검수:
    - 성구 verbatim 확인 (wol 연구용 URL 재조회)
    - 학습 요점 본문 팜플렛 원문 일치
    - 스타일 가이드 위반 체크 (`[요점 적용]` 주석 남았는지, 딱딱한 설교조 등)
    _selfcheck_script.md 작성.
  ⚠ 할루시네이션 / 4단 방어."
```

### 6. 🤖 ③ — student-assignment-planner script 재검수

```
Agent(student-assignment-planner)  [script 재검수]
  프롬프트: "script.md + _selfcheck_script.md Read.
  A. 타입 포맷 정확 / B. setting 유지 / C. 시간 분량 / D. 학습 요점 체현
  E. 대사 자연스러움 / F. 성구 verbatim.
  `_planner_review_script.md`: PASS | NEEDS-REWRITE."
```

### 7. docx 렌더
```bash
python content_student2_YYMMDD.py
```
(`build_student_assignment.py` 추후 작성)

### 8. 🤖 ④ — 최종 감사 3종 병렬

```
Agent(fact-checker) → research-factcheck/{YYMMDD}/factcheck_student2.md
Agent(jw-style-checker) → research-style/{YYMMDD}/
Agent(timing-auditor) → research-timing/{YYMMDD}/ (목표 3~4분)
```
HIGH 1건 이상 → 재빌드 (2회까지).

### 9. 확인 및 보고
- docx/PDF 경로, 과제 타입·장면·시간
- placeholder 확인, ③ 재검수 통과, ④ HIGH/MEDIUM/LOW

## 개정 이력
- 2026-04-24 v2 — 4단 방어 + 3개 보조 리서치 필수 (원준님 품질 지침)
- 2026-04-23 v1 — planner/script 2단 초안

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/mid-student2` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `학생 과제_{타입}_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3`) 호출 시

일괄 스킬이 묶음 확인 단계에서 이미 yes/no 받았으므로 **자체 단정형 확인 묻지 않는다**. 일괄에서 받은 결정 그대로 실행:

- **skip 결정** → 호출 자체가 발생 안 함 (일괄이 이미 걸러냄)
- **신규 빌드** → 정상 진행
- **`--from-batch=ver_up`** 컨텍스트 받으면 → `_verN_` (N = 디스크 최대 + 1) 자동 부여

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3 + `.claude/shared/output-naming-policy.md` §4·§4-bis.
