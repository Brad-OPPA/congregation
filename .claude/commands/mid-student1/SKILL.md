---
name: mid-student1
description: 주중집회 ③번 "성경 낭독 (bible_reading)" 학생 과제 1건 원고를 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3`. **4단 방어 축약형 적용** — 낭독은 구조가 단순해 planner 불필요, script 가 직접 WOL 파싱 + ② 자체 검수 → ④ fact-checker·jw-style-checker·timing-auditor 최종 감사. student-assignment-script 단독 호출로 낭독 본문 verbatim + 강세·쉼 지시·7축 평가 포인트 원고 생성. 남학생 전용 (S-38-KO 11항). 결과 `성경 낭독_YYMMDD.docx`. 트리거 "/mid-student1", "성경 낭독 과제 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# mid-student1 — 성경 낭독 학생 과제 (단일 주차, 4단 방어 축약형)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx (빌더 작성 후 PDF 자동 추가 예정)

## 이 스킬의 범위
- 성경 낭독 **한 건**
- **남학생 전용** (S-38-KO 11항)
- 야외봉사 학생과제는 `/mid-student2/3/4`, 5분 연설은 `/mid-talk5`

## 🛡 품질 원칙 — 4단 방어 축약형
- 낭독은 기획 단계가 필요 없어 **① Planner 지시서·③ Planner 재검수 생략**
- ② script 자체 검수 + ④ 최종 감사만 적용
- 전체 프로토콜: `.claude/shared/multi-layer-defense.md`

## 인자 규약
`now|next1|next2|next3`

## ⚠ WOL-first 수집
1. 주차 인덱스: `https://wol.jw.org/ko/wol/dt/r8/lp-ko/YYYY/M/D`
2. "성경 낭독" 섹션 href 그대로 따라갈 것
3. 낭독 범위·시간(4분)·학습 요점 번호 WOL verbatim
4. 장 번호 추측 금지

## 🚫 할루시네이션 금지
1. 낭독 본문 신세계역 연구용 verbatim (한 단어도 바꾸지 말 것)
2. 학습 요점은 「가르치는 기술」 원문만
3. 출처 URL 필수

## 저장 위치
베이스: `C:\Users\yoone\Dropbox\02.WatchTower\01.▣ 수원 연무 회중\01.주중집회\01.성경에 담긴 보물\03.성경 낭독\YYMMDD_M월 D-D일\`
파일명: `성경 낭독_YYMMDD.docx`

⚠ **섹션 분류 근거**: 성경 낭독은 프로그램 3번이자 "성경에 담긴 보물" 섹션의 마지막 항목 (10분 연설 1번, 영적 보물찾기 2번, 성경 낭독 3번). 4~6번(학생 과제 실연) 과 7번(5분 연설) 부터가 "야외봉사에 힘쓰십시오" 섹션이므로 성경 낭독은 해당 섹션에 **포함되지 않음**.

## 실행 단계 (4단 축약형)

### 1. 주차 확정 + 폴더

### 2. 🤖 ② — student-assignment-script 단독 호출 (WOL 파싱 + 원고 + 자체 검수)

```
Agent(student-assignment-script)
  프롬프트: "{YYMMDD} 주차 성경 낭독 (bible_reading) 완성 원고 생성.
  과제번호 1, 타입 bible_reading 고정. planner 없이 단독 실행.

  1단계 — WOL 직접 파싱:
    주차 인덱스 https://wol.jw.org/ko/wol/dt/r8/lp-ko/YYYY/M/D 에서 '성경 낭독' href 따라가
    verbatim 수집:
      - 낭독 범위 (예: 이사야 40:1-17)
      - 할당 시간 (보통 4분)
      - 학습 요점 번호·제목·본문 (팜플렛 「가르치는 기술」 원문 verbatim)
      - 낭독 본문 verbatim (신세계역 연구용)
      - 삽화 URL (있으면)

  2단계 — bible_reading 포맷 완성 원고:
    1) 헤더: 과제 번호·타입·담당자(`_________` placeholder)·낭독 범위·시간·학습 요점 번호
    2) 학습 요점 본문 (팜플렛 원문 + 출처 URL)
    3) ⭐⭐ **조언과 적용 지점 지정** (이 스킬 핵심):
       학습 요점(예: '의미 강세', '적절한 멈춤', '유창성' 등 「가르치는 기술」 해당 과)을
       낭독 본문 내에서 **구체적으로 적용할 지점 2~3곳**을 미리 선정.
       각 지점에 인라인 주석 `[적용: ...]` 표기. 예:
         - 학습 요점 '의미 강세' → "40:3 '광야에서 여호와의 **길을 닦아라**' [적용: '닦아라' 에 강세]"
         - 학습 요점 '적절한 멈춤' → "40:6 '한 목소리가 '외쳐라!' 하니' [적용: '외쳐라!' 앞뒤 짧은 쉼]"
       이 지점들은 학생이 연습할 때 의식적으로 적용하고,
       사회자가 조언 시점에 칭찬할 '예상 우수 지점'으로도 기능.
    4) 낭독 본문 verbatim
       - 단락별 13pt
       - 강세 단어 **볼드**, 쉼 `|`, 짙은 쉼 `||`
       - 중요 개념 노란 하이라이트
       - 3) 에서 지정한 조언과 적용 지점에 `[적용: ...]` 인라인 표기 유지
    5) 7축 평가 체크리스트 (정확성·내용 이해·유창성·의미 강세·변조·적절한 멈춤·자연스러움)
       — 오늘의 학습 요점과 관련 있는 축 1~2개에 ⭐ 표시
    6) 예상 소요 시간 메모

  결과: research-plan/student-assignment/{YYMMDD}_1_bible_reading/script.md
  meta.yaml 도 함께 (week_date, assignment_number=1, assignment_type=bible_reading,
    scripture_range, time_minutes=4, study_point{number,title,body},
    gender_restriction=male_only).

  ② 자체 검수 (필수):
    낭독 본문을 wol.jw.org 신세계역 연구용 URL 로 **재조회**하여 글자 단위 대조.
    학습 요점 본문도 팜플렛 원문 재조회 대조.
    research-plan/student-assignment/{YYMMDD}_1_bible_reading/_selfcheck_script.md 작성.
    HIGH 위반 있으면 스스로 수정 후 재검수 (2회 시도).

  한 문장 60음절 이내, 실전 낭독용.
  ⚠ 할루시네이션 금지 / ⚠ 4단 방어 프로토콜 준수 (.claude/shared/multi-layer-defense.md Read)."
```

### 3. docx 렌더

```bash
cd "C:\Users\yoone\Dropbox\02.WatchTower\01.▣ 수원 연무 회중\_automation"
python content_student1_YYMMDD.py
```
(`build_student_assignment.py` 추후 작성)

### 4. 🤖 ④ — 최종 감사 3종 병렬

```
Agent(fact-checker)
  프롬프트: "{docx_path} 낭독 본문 성구 verbatim 대조, 학습 요점 팜플렛 원문 일치 확인.
  research-factcheck/{YYMMDD}/factcheck_student1.md.
  ⚠ WebFetch 로 원본 재조회."

Agent(jw-style-checker)
  프롬프트: "{docx_path} 감수. 금칙어·신세계역·경어체·높임법.
  research-style/{YYMMDD}/ 저장."

Agent(timing-auditor)
  프롬프트: "{docx_path} 낭독 시간 시뮬레이션. 목표 4분(240초) 대비 추천.
  research-timing/{YYMMDD}/ 저장."
```
HIGH 1건 이상 → 재빌드 (2회까지).

### 5. 확인 및 보고
- docx/PDF 경로, 낭독 범위 + 학습 요점 요약
- 담당자 placeholder 확인
- ④ HIGH/MEDIUM/LOW 카운트

## 개정 이력
- 2026-04-24 v2 — 4단 방어 축약형 (①③ 생략, ②④ 적용) + fact-checker + timing-auditor 필수화
- 2026-04-23 v1 — script 단독 초안

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/mid-student1` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `성경 낭독_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3`) 호출 시

일괄 스킬이 묶음 확인 단계에서 이미 yes/no 받았으므로 **자체 단정형 확인 묻지 않는다**. 일괄에서 받은 결정 그대로 실행:

- **skip 결정** → 호출 자체가 발생 안 함 (일괄이 이미 걸러냄)
- **신규 빌드** → 정상 진행
- **`--from-batch=ver_up`** 컨텍스트 받으면 → `_verN_` (N = 디스크 최대 + 1) 자동 부여

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3 + `.claude/shared/output-naming-policy.md` §4·§4-bis.
