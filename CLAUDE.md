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
[에이전트 32개]  ← research-*/{YYMMDD}/ 저장
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

---

## 🎤 10분 연설 자동화 (확정 정본 2026-05-01)

`/mid-talk10 {now|next1|next2|next3}` — **사용자 입력 1회로 4종 게이트 PASS 까지 자동 작동**.

흐름: planner ① → 5 보조 ② → planner ③ → script ④ → assembly ⑤ → planner ⑥ → 빌드 ⑦ → **🚨 4종 게이트 자동 호출 ⑧** (`fact-checker` · `jw-style-checker` (WOL 최근 10년 + 사용자 NG list) · `timing-auditor` · `quality-monotonic-checker`) → FAIL 1건 이상 시 **자동 재작성** (해당 영역 재호출, 5회 한도) → PASS → 사용자 검수.

원준님 개입 = 입력 1회 + 검수 1회 = **총 2회**.

**세부 명세 (호출 체인 / R1~R18 자동 검증 룰 / 모범 정형 표현 / 사용자 NG list / WOL 최근 10년 검증 / 12 메모리 정책 / 단계별 trigger·input·output·재시도)**:
> 📘 `~/Claude/Projects/Congregation/research-meta/10분-연설-자동화-구조.md` (확정 정본)
> 📘 `~/Claude/Projects/Congregation/research-meta/10분-연설-표준패턴.md` (R1~R18)

**12 정책 메모리** (`~/.claude/projects/-Users-brandon/memory/`):
`feedback_speech_no_source_naming` · `feedback_speech_main_skeleton` · `feedback_speech_main_vs_example` · `feedback_speech_six_step_narrative` · `feedback_speech_intro_5flow` · `feedback_speech_no_redundant_metaphor` · `feedback_speech_natural_flow` · `feedback_planner_no_writing` · `feedback_research_breadth` · `feedback_builder_assembly_role` · `feedback_wol_term_verification` · `feedback_terms_user_specific_ng` · `feedback_six_gates_mandatory`

**확정 정본 — 더 이상 변경 X**. 다음 주차 (`/mid-talk10 next3` 등) 동일 퀄리티 자동 보장.

---

## 📜 파수대 연구 사회 자동화 (확정 정본 2026-05-02)

`/week-study` — 3주치 기본 (또는 `/week-study {특정주차만}`) — **사용자 입력 1회로 베이스 스크래핑 → 깊이 보강 → 4종 게이트 PASS 까지 자동 작동**.

흐름: skip 정책 묶음 확인 ① → WOL 주차 인덱스 → docid 추출 ② → 베이스 스크래핑 + 스캐폴드 docx ③ → **5 보조 리서치 병렬 dispatch ④** (publication-cross-ref · scripture-deep · application-builder · illustration-finder · experience-collector) → 통합 + add_cue 깊이 보강 ⑤ → 재빌드 ⑥ → 품질 메트릭 자체 검증 (95% 미달 시 add_cue 라운드 추가, 최대 4회) ⑦ → **🚨 4종 게이트 자동 호출 ⑧** (`fact-checker` · `jw-style-checker` · `timing-auditor` · `quality-monotonic-checker`) → FAIL 1건 이상 시 **자동 재작성** (5회 한도) → PASS → 사용자 검수.

원준님 개입 = 입력 1회 + 검수 1회 = **총 2회**.

**세부 명세 (호출 체인 / W1~W12 자동 검증 룰 / urllib timeout 회피 shim / add_cue 4 라운드 깊이 보강 표준 / 외부 14축 후보 / 자산 위치 / 시행착오)**:
> 📘 `~/Claude/Projects/Congregation/research-meta/파수대-사회-자동화-구조.md` (확정 정본)

**핵심 차이점 (vs 10분 연설)**:
- 베이스 스캐폴드는 `scrape_wt.py` + `spec_from_article()` 자동 (17블록·5소제목·삽화·복습 자동 파싱)
- 깊이는 `add_cue(numbers, runs)` 호출 목록 — block 단위 host_cue 주입
- 직전 주차 95% 미달 시 add_cue 추가 라운드 (1차~4차 표준)
- 「」 출판물 인용 ≥ 10, 외부 14축 ≥ 3 (week-study 차등 적용표 행)

**확정 정본 — 더 이상 변경 X**. 다음 주차 (`/week-study` 등) 동일 퀄리티 자동 보장.

---

## 🎙️ 공개 강연 자동화 (확정 정본 2026-05-02)

`/publictalk {번호}` — **사용자 입력 1회로 골자 PDF Read → 6 보조 리서치 → assembly 검증 → 4종 게이트 PASS 까지 자동 작동**.

흐름: 골자 PDF Read (S-34_KO_NNN.docx 또는 PB_NNN-KO*.pdf) ① → public-talk-builder = 기획자 (설계도 + 6개 에이전트 지시서) ② → 6개 보조 리서치 병렬 (scripture-deep · illustration-finder · experience-collector · application-builder · publication-cross-ref · qa-designer mode 2) ③ → public-talk-builder 1차 재검수 (R 룰 후보 풍부도) ④ → public-talk-script = 30분 서술형 원고 ⑤ → **publictalk-assembly-coordinator (R1~R20 + R-Conv + R-J1~J5 자체 grep, Phase 3-C 2026-05-02 신규)** ⑥ → public-talk-builder 2차 재검수 ⑦ → 빌드 (validators.validate_md_text 자동 차단 + docx2pdf → soffice fallback) ⑧ → **🚨 4종 게이트 자동 호출 ⑨** (`fact-checker` · `jw-style-checker` · `timing-auditor` (1800±120초) · `quality-monotonic-checker`) → FAIL 1건 이상 시 **자동 재작성** (해당 영역 재호출, 5회 한도 ver1→ver5) → PASS → 사용자 검수.

원준님 개입 = 입력 1회 + 검수 1회 = **총 2회**.

**세부 명세 (호출 체인 / R1~R20 + R-Conv + R-J1~J5 자동 검증 룰 / 모범 정형 표현 / 자동 재작성 5회 한도 / 외부 자료 우선순위)**:
> 📘 `~/Claude/Projects/Congregation/research-meta/공개강연-자동화-구조.md` (확정 정본)
> 📘 `~/Claude/Projects/Congregation/.claude/shared/publictalk-formal-expressions.md` (모범 정형 표현 사전 — 서론 후크 5종×3안·성구 유도·결론 5단락)

**핵심 차이점 (vs 10분 연설)**:

- 30분 서술형 — 6,500~9,000자 (R1), 시간 마커 ≥ 12 (R2), 낭독 성구 6~8개 (R3)
- 비증인 청중 포함 — 내부 용어 절제, "여러분" 호명만 (서론 호명 7종 금지)
- 외부 1차 자료 ≥ 5축 (R4) — 14축 (성서 적중 9 + 사유 촉발 5) 활용
- 시각자료 ≤ 5장 (R5), wol/jwb 비율 ≥ 60%
- 결론 R-Conv "오늘 우리는 세 가지를… 첫째·둘째·셋째…" 의무 (사용자 의견 ② 2026-05-02)
- 예수의 가르침 5요소 R-J1~J5 (간결성·논리·질문·수사·비유) 자동 측정 (사용자 의견 ③ 2026-05-02)
- 한 번 실행 = 1편 (3주치 개념 없음 — 강연자 로테이션)

**확정 정본 — 더 이상 변경 X**. 다음 강연 번호 (`/publictalk N`) 동일 퀄리티 자동 보장.

---

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

회중 로컬 `Congregation/.claude/commands/` 에 등록 (`~/.claude/commands/` 심볼릭 링크). 회중 폴더에서만 작동.

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

회중 로컬 `.claude/agents/` 에 32개 에이전트 등록 (2026-04-30: assembly-coordinator 신규).

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

### 특수 빌더·조합 (4)

`prayer-composer` (기도문) · `slides-builder` (pptx) · `role-play-scenario-designer` (학생 시연 시나리오) · **`assembly-coordinator`** (10분 연설 조합·매핑·R1~R10 1차 검증, 2026-04-30 신규 — script ↔ build 사이 단계)

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
- 스킬 정의: 회중 로컬 `Congregation/.claude/commands/` (`~/.claude/commands/` 심링크)
- 에이전트 정의: 회중 로컬 `.claude/agents/` (32개 — 2026-04-30 assembly-coordinator 신규)
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
- **품질 단조 증가 (2026-04-29 도입, Phase A·B·C·D·E 정착)** — 새 빌드의 정량 메트릭 (글자수·성구·출판물「」·외부 14축·시간 마커·깊이 단락·**이미지·구성 표준**) 이 직전 주차 동일 슬롯 docx 보다 같거나 풍부해야 함. quality-monotonic-checker 가 **9축** 자동 NO-GO + 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** (timing FAIL 이라도 quality PASS 면 통과). **fact ↔ quality cross-reference**: fact-checker 가 fake docid 출판 인용 제거 시 quality C 축 MED 강등. **이미지 silent skip 차단**: illustration-finder 가 `download_image.py` 로 시드 이미지 자동 다운로드 의무. 정책: `shared/quality-monotonic-policy.md`
- **메인 Claude 직접 정정 금지 (Phase E, 2026-05-01)** — 메인은 docx·content_*.py·script.md·outline.md 등 콘텐츠 파일을 직접 Edit/Write 하지 않는다. 의심 어휘·라벨 오류 발견 시 반드시 jw-style-checker (또는 해당 script 에이전트) 호출 → WOL WebFetch 검증 → script 재작성 → Agent 가 content_*.py 변환 → 빌더 (`validators.py` 자동 차단) 재실행. 메인의 직관 정정·임시 변환 우회 차단. 정책: `shared/main-claude-edit-policy.md`. 정본 단일화: `shared/banned-vocabulary.md` (금칙어) + `shared/comment-label-standard.md` (라벨).
- **영적 보물찾기 자동화 v2 (Phase E v2, 2026-05-01)** — 매주 자동 빌드 시 동일 퀄리티 보장. 자동화 구조 세부사항 (전체 흐름·5 보조 자료 수집 의무·검증 자동화 표·hook 작동 시점·정량 메트릭·회귀 적용 절차·단순/복잡 정정 분리) 은 `shared/dig-treasures-automation.md` 참조. 핵심 강제 메커니즘: validators 빌드 시 자동 차단 (라벨·금칙어·사용자 NG·의심 어휘) + gem-coordinator (R1~R10 측정) + Stop hook 3종 (factcheck·quality-loop·fact-loop) 자동 재호출 강제. 다각도·14축·깊이·4축 균형은 정보 측정만 (자연스러움 우선, 강제 X). 메인 Claude 정정은 단순(WOL fetch 정답 명확) 직접 / 복잡(해석 필요) Agent 위임.
