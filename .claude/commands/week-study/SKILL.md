---
name: week-study
description: 주말집회 "파수대 연구 사회" 실전 진행 대본 (사회자 실시간 script) 1편을 지정 주차에 대해 생성. 인자 `now|next1|next2|next3` (없으면 대화형). 메인 Claude 가 6 단계 (planner → research 4종 → application+script → assembly → 빌드 → 게이트 4종) 정본 절차로 진행. 단계 내부 single message multi-tool 병렬, 게이트 FAIL 시 단계 3·4 재호출 (5회 한도, SKILL 절차 책임). 트리거 "/week-study", "파수대 사회 만들어 줘", "파수대 예습".
---

# SKILL: week-study (파수대 연구 사회, 단일 슬롯)

## 정본 절차 (메인 Claude = 오케스트레이터, 변경 X)

### 단계 0 — Preflight (1 Bash)

```bash
git -C /Users/brandon/Claude/Projects/Congregation pull --ff-only
```

기존 `_verN_` 산출물 존재 시 skip 정책 (`.claude/shared/skip-existing-policy.md`) 확인. 사용자 확정 OK build (`ok-builds.json`) 가 있으면 baseline 으로 채택.

### 단계 1 — planner 호출 (1 Task)

`Task(subagent_type="watchtower-study-planner", ...)` — prompt 에 다음을 prepend:

- 정본 brief (출처: `_automation/team_briefings.py::watchtower_briefing()`)
- 주차 (`now`/`next1`/`next2`/`next3`)
- WOL 인덱스 docid 1102016XXX 검증 의무

산출물: `outline.md` (17 블록 spec) + `meta.yaml` (주차·기사·표어 성구).

### 단계 2 — research 병렬 (single message, 4 Task)

| 에이전트 | 책임 |
|---|---|
| `scripture-deep` | 핵심 성구 + 표어 성구 nwtsty verbatim |
| `publication-cross-ref` | 「파」 과거호 / 「통」 / 「예-1」 / 「훈」 출판물 인용 ≥ 10 |
| `illustration-finder` | 외부 14축 ≥ 3 (고고학·지형·과학·역사 우선), 시드 이미지 다운로드 |
| `experience-collector` | 회중 경험담·적용 사례 |

각 prompt 에 단계 1 outline 발췌 prepend.

### 단계 3 — application + script (의존 순차, 2 Task)

1. `application-builder` ← research 4종 → 항별 4축 적용 결합
2. (script 에이전트 통합 또는 watchtower-study-planner 가 항별 사회자 대사·해설 LLM draft)

산출물: `script.md` (오프닝 → 항별 블록 [시간 마커·소제목·질문·요약·해설·사회자 대사·성구 낭독] → 복습 → 결론).

### 단계 4 — assembly + content_*.py (1 Task)

`Task(subagent_type="assembly-coordinator", ...)` — script.md → `content_wt_YYMMDD.py` spec dict 변환·검증. block 단위 host_cue 주입, add_cue 깊이 보강 (95% 미달 시 자동 1차~4차 라운드, 최대 4회).

### 단계 5 — Bash 빌드 (1 Bash)

```bash
python3 _automation/build_watchtower.py {YYMMDD}
```

순수 렌더러. `validate_spec_integrity` 가 17 블록·시간 마커·인용 ≥ 10·외부 14축 ≥ 3 무결성 자동 검증 후 docx + PDF 출력.

### 단계 6 — 게이트 4종 병렬 (single message, 4 Task)

| 게이트 | 책임 |
|---|---|
| `fact-checker` | 성구·출판물·URL·docid 검증 |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름 |
| `timing-auditor` | 분량·시간 마커 (quality > timing) |
| `quality-monotonic-checker` | 9축 baseline 비교 |

### 게이트 FAIL 시 재호출 (정본 — Hook X, SKILL 절차가 처리)

- HIGH = 0 → 통과
- HIGH ≥ 1 → 위반 사유 prompt 에 prepend → 단계 3 (script) · 단계 4 (assembly) 재호출 (격리) → 재빌드 + 재게이트
- 5회 한도 → 사용자 BLOCKING 알림

## 유기적 협력 (의존성 그래프)

```
scripture-deep → publication-cross-ref (성구 → 출판물 ≥ 10)
research 4종 → application-builder (4축 적용)
research 5종 + outline → script (사회자 대사 LLM draft)
script → assembly-coordinator → spec (17 블록)
spec → build_watchtower.py → docx
docx → 4 게이트 (교차 검증)
```

## 재사용 자산

- `_automation/team_briefings.py::watchtower_briefing()`
- `_automation/scrape_wt.py::spec_from_article()` (17 블록 자동 파싱)
- `_automation/quality_baseline.py` (OK builds 우선)
- `.claude/shared/ok-builds.json` — 5/31 v3 baseline
- `.claude/shared/banned-vocabulary.md` / `user-quality-standard.md`

## 핵심 차이 (vs 다른 슬롯)

- 「」 출판물 인용 ≥ 10
- 외부 14축 ≥ 3
- block 단위 host_cue 주입
- add_cue 깊이 보강 4 라운드 (95% 미달 시 자동)
