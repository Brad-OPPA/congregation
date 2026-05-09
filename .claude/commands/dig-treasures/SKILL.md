---
name: dig-treasures
description: 주중집회 ②번 "영적 보물찾기" 원고 1편을 지정 주차에 대해 생성. 인자 `now|next1|next2|next3` (없으면 대화형). 메인 Claude 가 6 단계 (planner → research 4종 → application+script → assembly → 빌드 → 게이트 4종) 정본 절차로 진행. 단계 내부 single message multi-tool 병렬, 게이트 FAIL 시 단계 3·4 재호출 (5회 한도, SKILL 절차 책임). 트리거 "/dig-treasures", "영적 보물찾기 만들어 줘", "영보 만들어줘".
---

# SKILL: dig-treasures (영적 보물찾기, 단일 슬롯)

## 정본 절차 (메인 Claude = 오케스트레이터, 변경 X)

### 단계 0 — Preflight (1 Bash)

```bash
git -C /Users/brandon/Claude/Projects/Congregation pull --ff-only
```

기존 `_verN_` 산출물 skip 정책 확인.

### 단계 1 — planner 호출 (1 Task)

`Task(subagent_type="spiritual-gems-planner", ...)` — prompt 에 다음 prepend:

- 정본 brief (출처: `_automation/team_briefings.py::gems_briefing()`)
- 주차 (`now`/`next1`/`next2`/`next3`)
- 20개 성구 × 3항 (핵심·적용·배울점) 의무
- R1~R10 표준 패턴

산출물: `outline.md` (20 성구 매핑) + `meta.yaml`.

### 단계 2 — research 4 보조 병렬 (single message, 4 Task)

| 에이전트 | 책임 |
|---|---|
| `scripture-deep` | 20 성구 nwtsty verbatim |
| `publication-cross-ref` | 출판물 인용 매칭 |
| `illustration-finder` | 외부 14축 예화 + 시드 이미지 |
| `experience-collector` | 경험담·적용 사례 |

각 prompt 에 단계 1 outline 발췌 prepend.

### 단계 3 — application + script (의존 순차, 2 Task)

1. `application-builder` ← research 4종 → 4축 적용 (자연스러움 우선, 강제 X)
2. `spiritual-gems-script` ← outline + research 5종 → 핵심·적용·배울점 LLM draft

산출물: `script.md` (20 성구 × 3항).

### 단계 4 — assembly + content_sg.py (1 Task)

`Task(subagent_type="gem-coordinator", ...)` — script.md → `content_sg_YYMMDD.py` spec dict 변환·검증. R1~R10 측정 (다각도·14축·깊이·4축 균형은 정보 측정만).

### 단계 5 — Bash 빌드 (1 Bash)

```bash
python3 _automation/build_spiritual_gems.py {YYMMDD}
```

순수 렌더러. validators 가 라벨·금칙어·사용자 NG·의심 어휘 자동 차단 후 docx + PDF 출력.

### 단계 6 — 게이트 4종 병렬 (single message, 4 Task)

| 게이트 | 책임 |
|---|---|
| `fact-checker` | 20 성구 nwtsty + 출판물 docid 검증 |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름 |
| `timing-auditor` | 분량 (시간 제약 작은 포맷, 참고만) |
| `quality-monotonic-checker` | 9축 baseline 비교 |

### 게이트 FAIL 시 재호출 (정본 — Hook X, SKILL 절차가 처리)

- HIGH = 0 → 통과
- HIGH ≥ 1 → 위반 사유 prompt 에 prepend → 단계 3 (spiritual-gems-script) · 단계 4 (gem-coordinator) 재호출 → 재빌드 + 재게이트
- 5회 한도 → 사용자 BLOCKING 알림

## 유기적 협력 (의존성 그래프)

```
scripture-deep → publication-cross-ref (20 성구 → 출판물)
research 4종 → application-builder (4축 적용)
research 5종 + outline → spiritual-gems-script (3항 × 20)
script → gem-coordinator → spec (R1~R10 측정)
spec → build_spiritual_gems.py → docx
docx → 4 게이트 (교차 검증)
```

## 재사용 자산

- `_automation/team_briefings.py::gems_briefing()`
- `.claude/shared/dig-treasures-automation.md` (Phase E v2 자동화 구조)
- `_automation/download_image.py` (시드 이미지)
- `.claude/shared/banned-vocabulary.md` / `user-quality-standard.md`

## 핵심 차이 (vs 다른 슬롯)

- 20 성구 × 3항 (핵심·적용·배울점)
- 시간 제약 작은 포맷 (timing-auditor 참고만)
- validators 자동 차단 (라벨·금칙어·NG·의심 어휘)
- 자연스러움 우선 (4축 균형 정보 측정만, 강제 X)
- 메인 Claude 정정: 단순 (WOL fetch 정답 명확) 직접 / 복잡 (해석 필요) Agent 위임
