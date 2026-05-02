# 회중 자동화 — 스킬·에이전트 인덱스

> CLAUDE.md 에서 분리 (2026-05-02). CLAUDE.md 는 5줄 요약만 유지.

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
