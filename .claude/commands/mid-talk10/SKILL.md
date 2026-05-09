---
name: mid-talk10
description: 주중집회 ①번 "성경에 담긴 보물 — 10분 연설" 원고 1편을 지정 주차에 대해 생성. 인자 `now|next1|next2|next3` (없으면 대화형). 메인 Claude 가 6 단계 (planner → research 4종 → application+script → assembly → 빌드 → 게이트 4종) 정본 절차로 진행. 단계 내부 single message multi-tool 병렬, 게이트 FAIL 시 단계 3·4 재호출 (5회 한도, SKILL 절차 책임). 트리거 "/mid-talk10", "10분 연설 만들어 줘".
---

# SKILL: mid-talk10 (10분 연설, 단일 슬롯)

## 정본 절차 (메인 Claude = 오케스트레이터, 변경 X)

### 단계 0 — Preflight (1 Bash)

```bash
git -C /Users/brandon/Claude/Projects/Congregation pull --ff-only
```

기존 `_verN_` 산출물 skip 정책 확인. WOL 최근 10년 동일 주제 검증 (사용자 NG list 회피).

### 단계 1 — planner 호출 (1 Task)

`Task(subagent_type="treasures-talk-planner", ...)` — prompt 에 다음 prepend:

- 정본 brief (출처: `_automation/team_briefings.py::treasures_briefing()`)
- 주차 (`now`/`next1`/`next2`/`next3`)
- R1~R18 표준 패턴 (`research-meta/10분-연설-표준패턴.md`)
- 12 메모리 정책 (사용자 NG list 회피)

산출물: `outline.md` (R1~R18 매핑) + `meta.yaml`.

### 단계 2 — research 4 보조 병렬 (single message, 4 Task)

| 에이전트 | 책임 |
|---|---|
| `scripture-deep` | 핵심 성구 nwtsty verbatim |
| `publication-cross-ref` | 「파」·「통」·「예-1」·「훈」 출판물 인용 |
| `illustration-finder` | 외부 14축 예화 + 시드 이미지 (`download_image.py`) |
| `experience-collector` | 경험담·적용 사례 |

각 prompt 에 단계 1 outline 발췌 prepend.

### 단계 3 — application + script (의존 순차, 2 Task)

1. `application-builder` ← research 4종 → 4축 적용
2. `treasures-talk-script` ← outline + research 5종 → 자연스러운 본문·결론·서론 LLM draft (R1~R18 표준 패턴 준수)

산출물: `script.md`.

### 단계 4 — assembly + content_*.py (1 Task)

`Task(subagent_type="assembly-coordinator", ...)` — script.md → `content_YYMMDD.py` spec dict 변환·검증. R1~R10 1차 검증 (옵션 B 2026-04-30 도입).

### 단계 5 — Bash 빌드 (1 Bash)

```bash
python3 _automation/build_treasures_talk.py {YYMMDD}
```

순수 렌더러. 4페이지 docx + PDF 출력. `validate_spec_integrity` 가 5요소 핵심 성구·4축 결론·서론 무결성 자동 검증.

### 단계 6 — 게이트 4종 병렬 (single message, 4 Task)

| 게이트 | 책임 |
|---|---|
| `fact-checker` | 성구 nwtsty + 출판물 docid 검증 |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름·사용자 NG list |
| `timing-auditor` | 10분 분량 (quality > timing) |
| `quality-monotonic-checker` | 9축 baseline 비교 |

### 게이트 FAIL 시 재호출 (정본 — Hook X, SKILL 절차가 처리)

- HIGH = 0 → 통과
- HIGH ≥ 1 → 위반 사유 prompt 에 prepend → 단계 3 (treasures-talk-script) · 단계 4 (assembly) 재호출 → 재빌드 + 재게이트
- 5회 한도 → 사용자 BLOCKING 알림

## 유기적 협력 (의존성 그래프)

```
scripture-deep → publication-cross-ref (성구 → 출판물)
research 4종 → application-builder (4축 적용)
research 5종 + outline → treasures-talk-script (R1~R18)
script → assembly-coordinator → spec (R1~R10 1차)
spec → build_treasures_talk.py → 4페이지 docx
docx → 4 게이트 (교차 검증)
```

## 재사용 자산

- `_automation/team_briefings.py::treasures_briefing()`
- `research-meta/10분-연설-표준패턴.md` (R1~R18)
- `research-meta/10분-연설-자동화-구조.md` (확정 정본)
- `.claude/shared/banned-vocabulary.md` / `user-quality-standard.md`

## 핵심 차이 (vs 다른 슬롯)

- 4페이지 docx (10분 연설 전용)
- R1~R18 표준 패턴 의무
- 사용자 NG list 12 메모리 정책
- 5요소 핵심 성구 + 4축 결론·서론
