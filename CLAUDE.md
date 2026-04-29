# 회중 작업 공간 (congregation)

이 폴더는 김원준 형제의 **여호와의증인 회중 활동** 관련 맥락입니다. 사용자는 한국어 답변을 선호합니다.

## 한눈에 보는 구조 (2026-04-25 기준)

```
[원준님 입력]
   ↓ /weekly (월요일 1회) 또는 /midweek-now /next1 /next2 /next3
[일괄 스킬]  ← 산출물 묶음 확인 yes/no 1회
   ↓ Skill(단편, args="now/next1/next2/next3")
[단편 스킬 11개]  ← 묶음 컨텍스트 받으면 자체 묻기 X
   ↓ Agent(planner) → Agent(script) → Agent(보조 리서치) → 감수 게이트
[에이전트 30개]  ← research-*/{YYMMDD}/ 저장
   ↓ content_*.py 생성 → python build_*.py
[빌더 5개]  ← docx + PDF 자동 변환
   ↓ os.makedirs + doc.save
[디스크 출력]
```

### 출력 폴더 (생활과 봉사 공식 순서)

```
01.주중집회/
├── 01.성경에 담긴 보물/{01.10분 연설, 02.영적 보물 찾기, 03.성경 낭독}/{YYMMDD-MMDD}/
├── 02.야외 봉사에 힘쓰십시오/{01.학생 과제, 02.5분 연설}/{YYMMDD-MMDD}/
├── 03.그리스도인 생활/{YYMMDD-MMDD}/
├── 04.회중의 필요/{YYMMDD-MMDD}/
└── 05.회중 성서 연구/{YYMMDD-MMDD}/
02.주말집회/
└── 02.파수대 사회/{YYMMDD-MMDD}/
```

### 파일명 (한국어 prefix 통일)

| 파트 | 파일명 |
|---|---|
| 10분 연설 | `10분 연설_{주제}_YYMMDD.docx` |
| 영적 보물 찾기 | `영적 보물 찾기_YYMMDD.docx` |
| 성경 낭독 | `성경 낭독_YYMMDD.docx` |
| 학생 과제 | `학생 과제_{타입}_YYMMDD.docx` |
| 5분 연설 | `5분 연설_{주제}_YYMMDD.docx` |
| 그리스도인 생활 | `그리스도인 생활_{제목}_YYMMDD.docx` |
| 회중의 필요 | `회중의 필요_{주제}_YYMMDD.docx` |
| 회중 성서 연구 | `회중 성서 연구_훈{장}-{장}_YYMMDD.docx` |
| 파수대 사회 | `파수대 사회_YYMMDD.docx` |

재생성 시 `_verN_` 자동 부여 (디스크 최대 +1). publictalk 만 별도 정책.

### 빌더 분류 (2026-04-25 기준)

- **정기 (매주 자동)**: 6개 — `mid-talk10` · `dig-treasures` · `cbs` · `mid-talk5` · `week-study` · `living-part`
- **부정기 (단독 호출)**: 3개 — `publictalk` · `local-needs` · `chair`
- **신규** (2026-04-29): `build_student_assignment.py` — 학생 과제 5종 (bible_reading + apply_conversation_start/follow_up/bible_study/explaining_beliefs) 통합 빌더. build_mid_talk5 helper import + LibreOffice PDF (build_treasures_talk.auto_convert_to_pdf 재사용)

### 정본 (모든 출력 경로·파일명·skip·버전 규칙의 진실)

`Congregation/.claude/shared/output-naming-policy.md`

### 🏆 회중의 필요 ver4 검증 표준 패턴 (2026-04-25 원준님 확정)

회중의 필요 (`/local-needs`) 빌드 시 다음 패턴을 **표준** 으로 따른다. 표본: `04.회중의 필요/260504-0510/회중의 필요_야외봉사 슬기롭게_260507_ver4_.docx`.

**제목·톤** — 능동·격려형 ("우리는 …할 수 있습니다"). 부정·경계형 ("신중함·조심") 금지.

**5단 흐름** (10분 기준)
| 단계 | 시간 마커 | 책무 |
|---|---|---|
| 도입 | 1'30" | 일상 도구·상황 + 핵심 성구 + 능동 가치 |
| 요점 1 | 3'30" | 대상의 출처·근본·책임 명확화 (오해 방지) |
| 요점 2 | 6' | 할 수 있는 것 ✓ + **할 수 없는 것 ❌ 목록 5가지** + 관련 법·규정 한 줄 + 항목별 빨강 사유 |
| 요점 3 | 8'30" | 문제 발생 시 행동 절차 (즉시 보고 대상 명시 — 집단감독자·장로) |
| 결론 | 9'30" | 격려·축복 + 마무리 성구 + "함께 …합시다" |

**시각** — 인라인 시간 마커 5개 (빨강 #EE0000 볼드 우측정렬), 노랑 하이라이트 (전환어+핵심어구), 성구 좌측 0.4-0.5" 들여쓰기 (박스 X), 평문 산문 (4축 라벨 X).

**성구** — 4~5개 분산 (도입·각 요점·결론), 신세계역 verbatim, URL+호수·면 명시.

**pptx 6장**
1. 제목 (파랑) + 핵심 성구
2. 출처 명확화 (✕ 카드 + ✓ 카드)
3. 할 수 없는 것 N가지 (빨강 + 16pt italic 회색 사유 footer)
4. 할 수 있는 것 (파랑)
5. 문제 발생 시 (초록) — 보고 대상 명시
6. 격려·축복 (황금색) + 마무리 성구

**폰트 사이즈** — 어르신 친화: 제목 48pt / 헤더 40pt / 본문 32pt / 카드 22~30pt / 작은 글씨 16pt italic 회색 #6E6E6E (세부: planner §ver4 패턴).

**법적·외부 규정** — 주제 관련 법(한국 법 우선) 한 줄 + 항목별 사유 표기 ("법 위반 가능"·"민감 정보 저장 우려"). 단정적 법 해석 X — "제한합니다·우려" 같은 신중 표현.

세부: `local-needs-planner.md` §"🏆 ver4 검증 표준 패턴".

## 주요 활동

- 주중집회 (목요일) 원고 준비
- 주말집회 (일요일) 원고 준비
- 3주 선행 자료 생성 — 이번 주 + 다음 주 + 다다음 주

## 사용 스킬 (slash command)

글로벌 `C:\Users\yoone\.claude\skills\` 에 19개 스킬 등록.

### 주중집회 (목요일) — 3개 섹션

#### Ⅰ. 하느님의 말씀에서 보물찾기

| 스킬 | 위치 | 용도 |
| --- | --- | --- |
| `/mid-talk10` | ① | "성경에 담긴 보물" 10분 연설 |
| `/dig-treasures` | ② | "영적 보물찾기" 문답 (성구 20개 × 3항) |
| `/mid-student1` | ③ | 성경 낭독 학생 과제 (남학생 전용) |

#### Ⅱ. 봉사 직무에 향상되십시오

| 스킬 | 용도 |
| --- | --- |
| `/mid-student2`~`/mid-student4` | 야외봉사 학생 시연 과제 |
| `/mid-talk5` | 야외봉사 마지막 5분 연설 (남학생) |

#### Ⅲ. 그리스도인 생활

| 스킬 | 용도 |
| --- | --- |
| `/living-part` | 생활 파트 (talk / discussion / video / interview / qna 자동 분기) |
| `/local-needs` | 회중의 필요 (장로의회 주제 입력 → 원고 + pptx) |
| `/cbs` | ⑩ 회중성서연구 사회 30분 (주중집회의 마지막 파트) |

### 주말집회 (일요일)

| 스킬 | 위치 | 용도 |
| --- | --- | --- |
| `/publictalk` | ① | 공개 강연 30분 (로컬 골자 PDF 기반) |
| `/week-study` | ② | 파수대 연구 사회 — 3주치 일괄 |

### 일괄 (3주치 또는 통합)

| 스킬 | 용도 |
| --- | --- |
| `/midweek-now`·`next1`·`next2`·`next3` | 주중집회 10개 파트 일괄 (회중의 필요 제외) |
| `/mid-study1`·`/mid-study2`·`/mid-study3` | 10분연설 / 영적보물 / CBS 각 3주치 (legacy) |

## 사용 에이전트 (subagent)

회중 로컬 `.claude/agents/` 에 30개 에이전트 등록.

### 리서치 (8) — 결과를 `research-*/` 폴더에 저장

| 에이전트 | 용도 | 저장 폴더 |
| --- | --- | --- |
| `wol-researcher` | 주차 프로그램·본문·성구·삽화 목록화 | `research-wol/` |
| `publication-cross-ref` | 주제 횡단 (파·깨·통·예-1·JW방송) | `research-topic/` |
| `scripture-deep` | 성구 심층 (번역·원어·배경·병행) | `research-bible/` |
| `illustration-finder` | 예화·비유·서론·결론 초안 | `research-illustration/` |
| `qa-designer` | 문답 블록 설계 | `research-qa/` |
| `application-builder` | 실생활 적용 카드 | `research-application/` |
| `experience-collector` | 공식 경험담 수집 | `research-experience/` |
| `public-talk-builder` | 공개 강연 30분 아웃라인·재료 | `research-public-talk/` |

### 기획 planner (8) — 스킬별 지시서 작성

`treasures-talk-planner` · `spiritual-gems-planner` · `cbs-planner` · `watchtower-study-planner` · `living-part-planner` · `local-needs-planner` · `student-assignment-planner` · `student-talk-planner`

### 대본 script (8) — 실제 원고 작성

`treasures-talk-script` · `spiritual-gems-script` · `cbs-script` · `living-part-script` · `student-assignment-script` · `student-talk-script` · `chair-script-builder` · `public-talk-script`

### 특수 빌더 (3)

`prayer-composer` (기도문) · `slides-builder` (pptx) · `role-play-scenario-designer` (학생 시연 시나리오)

### 감수 게이트 (4) — 2026-04-29 4종으로 확장

| 에이전트 | 용도 | 저장 폴더 |
| --- | --- | --- |
| `fact-checker` | 사실·인용·성구 표기 검증 | `research-factcheck/` |
| `jw-style-checker` | 공식 용어·호칭·신세계역 표기 | `research-style/` |
| `timing-auditor` | 낭독 시간 측정·조정 제안 (±60→±120초 완화) | `research-timing/` |
| **`quality-monotonic-checker`** ← 신규 | 직전 주차 대비 품질 단조 증가 검증 (글자·성구·출판·외부 14축). FAIL 시 자동 재작성 강제 (5회 한도). 정책: `shared/quality-monotonic-policy.md` | `research-quality/` |

⑥ 단계는 **4종 병렬**. **quality > timing** — timing FAIL 이라도 quality PASS 면 통과.

## 스킬 ↔ 에이전트 호출 체인

각 스킬이 실제 호출하는 에이전트 (`SKILL.md` 직접 파싱). 모든 스킬은 종료 시 **공통 감수 게이트** (`fact-checker` + `jw-style-checker` + `timing-auditor`) 를 통과.

| 스킬 | planner | script | 보조 리서치 / 특수 |
| --- | --- | --- | --- |
| `/mid-talk10` | treasures-talk-planner | treasures-talk-script | scripture-deep · publication-cross-ref · illustration-finder · experience-collector · application-builder |
| `/dig-treasures` | spiritual-gems-planner | spiritual-gems-script | 위와 동일 (timing-auditor 제외 — 시간 제약 없음) |
| `/mid-student1` | (없음) | student-assignment-script | 단독 호출 |
| `/mid-student2`·`/mid-student3` | student-assignment-planner | student-assignment-script | scripture-deep · application-builder · experience-collector + role-play-scenario-designer |
| `/mid-student4` | student-assignment-planner | student-assignment-script | role-play-scenario-designer |
| `/mid-talk5` | student-talk-planner | student-talk-script | scripture-deep · publication-cross-ref · illustration-finder · experience-collector · application-builder |
| `/living-part` | living-part-planner | living-part-script | subtype별 보조 (qa-designer · application-builder · experience-collector · publication-cross-ref 등) |
| `/local-needs` | local-needs-planner | (planner 가 직접 작성) | scripture-deep · publication-cross-ref · application-builder · experience-collector · illustration-finder + slides-builder |
| `/cbs` | cbs-planner | cbs-script | qa-designer · scripture-deep · publication-cross-ref · application-builder + (선택) experience-collector · illustration-finder |
| `/week-study` | watchtower-study-planner | (planner 가 직접 작성) | wol-researcher · scripture-deep · publication-cross-ref · qa-designer · application-builder · experience-collector · illustration-finder · public-talk-builder |
| `/publictalk` | — | — | public-talk-builder 가 기획·통합. scripture-deep · publication-cross-ref · illustration-finder · experience-collector · application-builder · qa-designer |

## 훅 (자동 실행)

회중 워크스페이스 `.claude/settings.json` 에 등록.

| 이벤트 | 훅 | 동작 |
| --- | --- | --- |
| `Stop` (응답 종료) | `.claude/hooks/factcheck-numbers.py` | 회중 자료의 숫자·연도·통계 사실 재검증 |

## 데이터 출처

- 공식 자료: **wol.jw.org** (연구용 교재, 주간 파수대, 참조서)
- 참고서: 「파」·「익」·「통」·「예-1」·「훈」 책 등
- 원고는 wol.jw.org 의 본문·성구·참조자료를 근거로 생성

## 환경

- Python 3.10+ **필수** (파이프라인 빌더가 요구)
- 스킬 정의: 글로벌 `C:\Users\yoone\.claude\skills\` (19개)
- 에이전트 정의: 회중 로컬 `.claude/agents/` (30개)
- 공유 정책: 회중 로컬 `.claude/shared/`
  - `multi-layer-defense.md` — 4단/6단 방어 프로토콜 (⑥ 4종 병렬, 2026-04-29 갱신)
  - `intro-and-illustration-quality.md` — 서론·예화·삽화 품질 표준
  - `skip-existing-policy.md` — 산출물 존재 시 skip 정책
  - `student-role-play-style.md` — 학생 시연 톤
  - **`quality-monotonic-policy.md`** ← 신규 (2026-04-29) — 슬롯별 절대 하한선 + 단조 증가 7축 점검 + 재작성 무한 루프 (5회 한도) + quality > timing 우선순위
- 관련 메모리: `project_meeting_pipelines.md` (mid-study1/2/3 + week-study 경로 맵)

## 원칙

- 원고는 wol.jw.org 공식 내용만 근거. 추측·외부 해석 최소화.
- 성구 참조·교재 인용 정확히. **"예배"** 단어 금지 — "집회" 등 공식 용어만.
- 회중 자료 감수는 변경분이 아닌 **세션 내 모든 신규/재빌드 docx 전체** 대상 (`jw-style-checker`).
- **작업 위임·병렬화 우선** — 3단계/3파일 이상은 서브 에이전트로 위임, 의존성 없는 작업은 한 메시지 안에서 병렬 호출. 메인 컨텍스트는 의사결정·통합·git 에 보존. 세부: 메모리 `feedback_delegate_to_subagents.md`.
- **상투적 청중 호명·수사 질문 금지** — "여러분도 …해 보신 적 있으십니까?" 류 9가지 표현 일체 금지. 모든 script 에이전트 + jw-style-checker 가 차단. 세부: 메모리 `feedback_script_no_cliche.md` · `intro-and-illustration-quality.md` §A-4-bis.
- **품질 단조 증가 (2026-04-29 도입, Phase A·B 정착)** — 새 빌드의 정량 메트릭 (글자수·성구·출판물「」·외부 14축·시간 마커·깊이 단락) 이 직전 주차 동일 슬롯 docx 보다 같거나 풍부해야 함. 어떤 메트릭이라도 -5% 초과 감소 시 quality-monotonic-checker 가 자동 NO-GO + 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** (timing FAIL 이라도 quality PASS 면 통과). 정책: `shared/quality-monotonic-policy.md`
