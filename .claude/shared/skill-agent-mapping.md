# SKILL ↔ Agent 매핑 정본 (2026-05-09)

회중 자료 자동화의 **SKILL 절차 단계 ↔ 34 에이전트 호출** 단방향 매핑. 메인 Claude 가 각 SKILL 을 실행할 때 단계마다 어떤 에이전트를 어떤 순서로 호출하는지의 **유일한 진실 원천**.

## 출처

- plan: `~/.claude/plans/adaptive-wandering-thunder.md` (회중 자료 자동화 v2)
- 정본 골자: 4 계층 (오케스트레이터·슬롯 리더·작업·게이트) + 특수 에이전트
- 확장: 4 계층 v2 = 계층 2 (planner) / 계층 3 (작업) / 계층 4 (게이트) / 계층 5 (특수)
- 매핑 대상 SKILL 18종 + 34 에이전트

---

## 4 계층 분류 (34 에이전트)

### 계층 2 — 슬롯 리더 = planner (9)

자기 슬롯 outline + meta.yaml 생성, 보조 에이전트 지시서 발행, 최종 spec dict 책임.

| 에이전트 | 슬롯 | 호출자 SKILL |
|---|---|---|
| `watchtower-study-planner` | 파수대 연구 (60분) | `/weekly`, `/week-study` |
| `cbs-planner` | 회중 성서 연구 (30분) | `/weekly`, `/cbs`, `/midweek-now`, `/midweek-next1/2/3` |
| `treasures-talk-planner` | 10분 연설 | `/weekly`, `/mid-talk10`, `/midweek-*` |
| `spiritual-gems-planner` | 영적 보물찾기 | `/weekly`, `/dig-treasures`, `/midweek-*` |
| `living-part-planner` | 그리스도인 생활 (CBS·local 제외) | `/living-part`, `/midweek-*` |
| `student-assignment-planner` | 학생 과제 5종 | `/mid-student2/3/4`, `/midweek-*` |
| `student-talk-planner` | 5분 연설 (apply_talk) | `/mid-talk5`, `/midweek-*` |
| `local-needs-planner` | 회중의 필요 (planner+script 통합) | `/local-needs`, `/midweek-*` |
| `public-talk-builder` | 공개 강연 30분 (기획자) | `/publictalk` |

### 계층 3 — 작업 에이전트 (12)

#### research 4종 (병렬)
| 에이전트 | 역할 | 호출자 SKILL |
|---|---|---|
| `scripture-deep` | 성구 nwtsty verbatim·원어·배경 | `/weekly`, `/week-study`, `/cbs`, `/mid-talk10`, `/dig-treasures`, `/mid-talk5`, `/mid-student2/3/4`, `/local-needs`, `/publictalk` |
| `publication-cross-ref` | 「파」·「통」·「예-1」·「훈」 출판물 횡단 | `/weekly`, `/week-study`, `/cbs`, `/mid-talk10`, `/dig-treasures`, `/mid-talk5`, `/local-needs`, `/publictalk`, `/living-part` |
| `illustration-finder` | 외부 14축 예화·삽화·시드 이미지 | `/weekly`, `/week-study`, `/mid-talk10`, `/dig-treasures`, `/mid-talk5`, `/local-needs`, `/publictalk` |
| `experience-collector` | 「연감」·「파」 "삶"·JW 방송 경험담 | `/weekly`, `/week-study`, `/cbs (선택)`, `/mid-talk10`, `/dig-treasures`, `/mid-talk5`, `/mid-student2/3/4`, `/local-needs`, `/publictalk`, `/living-part` |

#### application 1종
| 에이전트 | 역할 | 호출자 SKILL |
|---|---|---|
| `application-builder` | 4축 적용점 (가정·직장/학교·회중·개인 영성) | `/weekly`, `/week-study`, `/cbs`, `/mid-talk10`, `/dig-treasures`, `/mid-talk5`, `/mid-student2/3/4`, `/local-needs`, `/publictalk`, `/living-part` |

#### script 4종 (slot 별 1종)
| 에이전트 | 슬롯 | 호출자 SKILL |
|---|---|---|
| `treasures-talk-script` | 10분 연설 본문 | `/weekly`, `/mid-talk10`, `/midweek-*` |
| `spiritual-gems-script` | 영적 보물찾기 본문 | `/weekly`, `/dig-treasures`, `/midweek-*` |
| `cbs-script` | CBS 사회자 진행 원고 | `/weekly`, `/cbs`, `/midweek-*` |
| `living-part-script` | 생활 파트 subtype 5종 원고 | `/living-part`, `/midweek-*` |
| `student-assignment-script` | 학생 과제 5종 원고 | `/mid-student1/2/3/4`, `/midweek-*` |
| `student-talk-script` | 5분 연설 본문 | `/mid-talk5`, `/midweek-*` |
| `public-talk-script` | 공개 강연 30분 서술 | `/publictalk` |
| `chair-script-builder` | 사회자 전체 대본 (Planner+Script+QA 겸직) | `/chair`, `/midweek-*` |

#### assembly 3종
| 에이전트 | 슬롯 | 호출자 SKILL |
|---|---|---|
| `assembly-coordinator` | 10분 연설 / 파수대 / CBS 통용 spec dict 검증·생성 | `/weekly`, `/week-study`, `/cbs`, `/mid-talk10`, `/midweek-*` |
| `gem-coordinator` | 영적 보물찾기 5블록 매핑·R1~R10 | `/weekly`, `/dig-treasures`, `/midweek-*` |
| `publictalk-assembly-coordinator` | 공개 강연 30분 흐름 1:1 매핑·R1~R20 | `/publictalk` |

### 계층 4 — 게이트 (4)

⑥ 단계 4종 병렬 감사. **quality > timing**, HIGH 위반 ≥ 1 이면 단계 3·4 재호출.

| 에이전트 | 역할 | 호출자 SKILL |
|---|---|---|
| `fact-checker` | 성구·출판물·URL nwtsty 정확도 | 모든 SKILL 의 ⑥ 단계 |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름·9 금지 표현 | 모든 SKILL 의 ⑥ 단계 |
| `timing-auditor` | 분량·시간 마커·낭독 속도 | `/dig-treasures` 제외 모든 SKILL ⑥ 단계 |
| `quality-monotonic-checker` | 9축 메트릭 baseline 비교 | 모든 SKILL 의 ⑥ 단계 (자동) |

### 계층 5 — 특수 (5)

필요 슬롯에서만 호출. 독립 사용도 가능.

| 에이전트 | 역할 | 호출자 SKILL |
|---|---|---|
| `qa-designer` | 듀얼 모드 (Q&A 블록 / 수사적 질문) | `/cbs`, `/dig-treasures (선택)`, `/local-needs`, `/publictalk`, `/living-part (discussion)`, `/week-study` |
| `prayer-composer` | 시작·마침 기도 4단 전문 | `/chair` (opening + closing 2회), 독립·필요시 호출 |
| `role-play-scenario-designer` | 학생 과제 실연 4종 가상 시나리오 | `/mid-student2/3/4` |
| `slides-builder` | python-pptx 슬라이드 렌더러 | `/local-needs` |
| `wol-researcher` | wol.jw.org 1차 리서치 (주차 단위) | `/week-study`, `/local-needs` |

---

## SKILL → 단계별 에이전트 매핑 (정본)

### `/weekly` (4 슬롯 × 3 주차 = 12 빌드 일괄)

> 메인 Claude 가 single message multi-tool 로 단계 내부 병렬 호출. 단계 사이는 의존 순차.

| 단계 | 호출 에이전트 (병렬) | 호출 횟수 |
|---|---|---:|
| ① planner | `watchtower-study-planner` + `cbs-planner` + `treasures-talk-planner` + `spiritual-gems-planner` | 12 (4 슬롯 × 3 주차) |
| ② research 4 보조 | `scripture-deep` + `publication-cross-ref` + `illustration-finder` + `experience-collector` | 48 (12 × 4) |
| ③ application + script | `application-builder` (먼저) → 슬롯 script 4종 (`treasures-talk-script` / `spiritual-gems-script` / `cbs-script` + 파수대는 planner 겸직) | 12 + 12 |
| ④ assembly | `assembly-coordinator` (3 슬롯) + `gem-coordinator` (영보) | 12 |
| ⑤ Bash 빌드 | (에이전트 X — `python3 _automation/build_*.py`) | 12 |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` | 48 (12 × 4) |

### `/week-study` (파수대 연구, 단일 슬롯, 3 주차)

| 단계 | 호출 에이전트 |
|---|---|
| 1차 리서치 | `wol-researcher` |
| ② 5 보조 병렬 | `scripture-deep` + `publication-cross-ref` + `illustration-finder` + `experience-collector` + `application-builder` + `qa-designer` |
| ③ Planner QA | `watchtower-study-planner` (1차 재검수) |
| ④ Script | (`watchtower-study-planner` 가 chair_script.md 직접 생성) |
| ⑤ Planner 최종 QA | `watchtower-study-planner` (2차) |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/cbs` (회중 성서 연구, 단일 슬롯)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner | `cbs-planner` (지시서 작성) |
| ② 4 필수 + 2 선택 병렬 | `qa-designer` + `scripture-deep` + `publication-cross-ref` + `application-builder` + (선택) `experience-collector` + `illustration-finder` |
| ③ planner 재검수 | `cbs-planner` |
| ④ script | `cbs-script` |
| ⑤ planner 최종 QA | `cbs-planner` |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/mid-talk10` (10분 연설, 단일 슬롯)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner | `treasures-talk-planner` |
| ② 5 보조 병렬 | `scripture-deep` + `publication-cross-ref` + `illustration-finder` + `experience-collector` + `application-builder` |
| ③ planner 1차 재검수 | `treasures-talk-planner` |
| ④ script | `treasures-talk-script` |
| ④' assembly | `assembly-coordinator` (조합·매핑·R1~R10) |
| ⑤ planner 2차 재검수 | `treasures-talk-planner` |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/dig-treasures` (영적 보물찾기, 단일 슬롯)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner | `spiritual-gems-planner` |
| ② 5 보조 병렬 | `scripture-deep` + `publication-cross-ref` + `application-builder` + `experience-collector` + `illustration-finder` |
| ③ planner 1차 재검수 | `spiritual-gems-planner` |
| ④ script | `spiritual-gems-script` |
| ④' assembly | `gem-coordinator` (5블록·R1~R10) |
| ⑤ planner 2차 재검수 | `spiritual-gems-planner` |
| ⑥ 게이트 3종 (timing 제외) | `fact-checker` + `jw-style-checker` + `quality-monotonic-checker` |

### `/living-part` (그리스도인 생활, subtype 5종 분기)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner + subtype 판별 | `living-part-planner` |
| ② subtype별 보조 병렬 | `publication-cross-ref` + (`application-builder` / `experience-collector` / `qa-designer` 중 subtype 매칭) |
| ③ planner 재검수 | `living-part-planner` |
| ④ script | `living-part-script` |
| ⑤ planner 최종 QA | `living-part-planner` |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/local-needs` (회중의 필요, planner 가 script 까지 직접)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner (브리프 요약·지시서) | `local-needs-planner` |
| ② 7 보조 병렬 (모두 필수) | `wol-researcher` + `scripture-deep` + `publication-cross-ref` + `illustration-finder` + `qa-designer` + `application-builder` + `experience-collector` |
| ③ planner 1차 재검수 | `local-needs-planner` |
| ④ planner script + slides_plan | `local-needs-planner` (script.md + slides_plan.json + meta.yaml 직접 작성) |
| ④' 슬라이드 렌더 | `slides-builder` |
| ⑤ planner 2차 재검수 | `local-needs-planner` |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/chair` (사회자 전체 대본)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner (지시서) | `chair-script-builder` (Planner 모드) |
| ② 보조 (기도 2회) | `prayer-composer` × 2 (opening · closing) |
| ③ Planner 재검수 | `chair-script-builder` |
| ④ script (본 대본) | `chair-script-builder` (Script 모드) |
| ⑤ Planner 최종 QA | `chair-script-builder` |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor (6300초)` + `quality-monotonic-checker` |

### `/publictalk` (공개 강연 30분, 부정기)

| 단계 | 호출 에이전트 |
|---|---|
| A. 기획 (architect) | `public-talk-builder` (요점별 에이전트 지시서까지) |
| B. 6 에이전트 병렬 | `scripture-deep` + `illustration-finder` + `experience-collector` + `application-builder` + `publication-cross-ref` + `qa-designer (mode2)` |
| C. 본문 작성 | `public-talk-script` |
| C' assembly | `publictalk-assembly-coordinator` (R1~R20·R-Conv·R-J1~J5) |
| ⑤ planner 최종 QA | `public-talk-builder` (2차 재검수) |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/mid-talk5` (5분 연설)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner | `student-talk-planner` |
| ② 5 보조 병렬 | `scripture-deep` + `publication-cross-ref` + `illustration-finder` + `experience-collector` + `application-builder` |
| ③ planner 재검수 | `student-talk-planner` |
| ④ script | `student-talk-script` |
| ⑤ planner 최종 QA | `student-talk-planner` |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/mid-student1` (성경 낭독, 6단 축약형)

| 단계 | 호출 에이전트 |
|---|---|
| ② script (단독) | `student-assignment-script` (WOL 파싱 + 본문 verbatim) |
| ⑥ 게이트 3종 | `fact-checker` + `jw-style-checker` + `timing-auditor` |

### `/mid-student2` · `/mid-student3` · `/mid-student4` (학생 과제 5종)

| 단계 | 호출 에이전트 |
|---|---|
| ① planner | `student-assignment-planner` (지시서) |
| ①' 시나리오 | `role-play-scenario-designer` (apply_* 4종일 때) |
| ② 3 보조 병렬 | `scripture-deep` + `experience-collector` + `application-builder` |
| ③ planner 재검수 | `student-assignment-planner` |
| ④ script | `student-assignment-script` |
| ⑤ planner 최종 QA | `student-assignment-planner` |
| ⑥ 게이트 4종 | `fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker` |

### `/midweek-now` · `/midweek-next1/2/3` (주중 일괄)

각 SKILL 은 다음 7~9 슬롯의 `/mid-*` SKILL 을 순차 호출:
- `/mid-talk10` → `/dig-treasures` → `/mid-student1/2/3/4` → `/mid-talk5` → `/living-part` → `/cbs` → `/chair` (회중의 필요는 별도)

→ 단계별 에이전트 호출은 각 하위 SKILL 의 매핑 따름.

---

## 호출 빈도 별 요약

### 매주 호출 (정기 자동)
- 계층 2: `watchtower-study-planner`, `cbs-planner`, `treasures-talk-planner`, `spiritual-gems-planner`, `living-part-planner`, `student-assignment-planner`, `student-talk-planner`
- 계층 3: 모든 research 4종 + `application-builder` + script 7종 + assembly 2종 (assembly + gem)
- 계층 4: 4 게이트 (매주 약 30~50회)
- 계층 5: `qa-designer` (cbs/local 등), `wol-researcher` (week-study)

### 부정기 호출 (단독)
- `chair-script-builder` (사회자 담당 주만)
- `prayer-composer` (chair 호출 시)
- `local-needs-planner` (회중의 필요 발생 주만)
- `slides-builder` (local-needs 호출 시)
- `public-talk-builder`, `public-talk-script`, `publictalk-assembly-coordinator` (공개 강연 담당 주만)
- `role-play-scenario-designer` (학생 과제 apply_* 4종일 때만)

### 독립·필요시 호출
- 모든 에이전트는 사용자가 직접 Task 호출하거나 다른 에이전트가 협력 호출 가능 (특히 research·application·qa·illustration 류).

---

## 게이트 FAIL 시 재호출 (SKILL 절차 책임)

```
⑥ 게이트 4종 결과 통합
   ↓
모든 PASS? → 빌드 = 정본
   ↓
HIGH FAIL ≥ 1?
   ↓
위반 사유 + 해당 슬롯 prompt 에 prepend
   ↓
계층 3 의 해당 작업 에이전트 재호출 (single Task, 슬롯 단위 격리)
   ↓
재빌드 + 재게이트
   ↓
5회 한도 도달 시 사용자 BLOCKING 알림
```

**hook 의 책임 X** — SKILL 절차 자체가 재호출.

---

## 변경 이력

- 2026-05-09 신규 (정본 v1) — plan `adaptive-wandering-thunder.md` C 섹션 기반 34 에이전트 4 계층 분류 + SKILL 18종 단계별 매핑.
