---
name: cbs
description: 주중집회 ⑩번 "회중성서연구 사회 (30분)" 원고 1편을 지정 주차에 대해 생성. 인자 `now|next1|next2|next3` (없으면 대화형). 메인 Claude 가 6 단계 (planner → research 4종 → application+script → assembly → 빌드 → 게이트 4종) 정본 절차로 진행. 단계 내부 single message multi-tool 병렬, 게이트 FAIL 시 단계 3·4 재호출 (5회 한도, SKILL 절차 책임). 트리거 "/cbs", "회중성서연구 만들어 줘", "CBS 원고".
---

# SKILL: cbs (회중 성서 연구 사회 30분, 단일 슬롯)

## 정본 절차 (메인 Claude = 오케스트레이터, 변경 X)

### 단계 0 — Preflight (1 Bash)

```bash
git -C /Users/brandon/Claude/Projects/Congregation pull --ff-only
```

기존 `_verN_` 산출물 skip 정책 + 주차별 publication symbol (`jy` / `lfb`) 확인.

### 단계 1 — planner 호출 (1 Task)

`Task(subagent_type="cbs-planner", ...)` — prompt 에 다음 prepend:

- 정본 brief (출처: `_automation/team_briefings.py::cbs_briefing()`)
- 주차 (`now`/`next1`/`next2`/`next3`)
- WOL "8. 회중 성서 연구" href 추적 + docid 1102016XXX 검증 의무
- 「훈」=lfb / 「예수」=jy 분리 표기 의무

산출물: `outline.md` + `meta.yaml` (장 범위·publication symbol).

### 단계 2 — research 병렬 (single message, 4 Task)

| 에이전트 | 책임 |
|---|---|
| `scripture-deep` | 핵심 성구 nwtsty verbatim |
| `publication-cross-ref` | 「훈」 (lfb) / 「예수」 (jy) 출판물 인용 |
| `illustration-finder` | WOL 이미지 + 외부 14축 예화 후보 |
| `experience-collector` | 회중 경험담·적용 사례 |

각 prompt 에 단계 1 outline 발췌 prepend.

### 단계 3 — application + script (의존 순차, 2 Task)

1. `application-builder` ← research 4종 → 4축 적용
2. `cbs-script` ← outline + research 5종 → 자연스러운 사회자·낭독자 분리 본문 LLM draft

산출물: `script.md` (사회자 30분 + 낭독자 별도, 시간 마커 8개 빨강 볼드).

### 단계 4 — assembly + content_cbs.py (1 Task)

`Task(subagent_type="assembly-coordinator", ...)` — script.md → `content_cbs_YYMMDD.py` SPEC dict 변환·검증 (`script_to_content_cbs.py` 헬퍼 60-72% 자동화 활용).

WOL 이미지 다운로드 + 시간 마커 8개 무결성 검증.

### 단계 5 — Bash 빌드 (1 Bash)

```bash
python3 _automation/build_cbs_v10.py {YYMMDD}
```

순수 렌더러. SPEC dict 무결성 검증 후 docx + PDF 출력. timing 1800±120초 목표 (quality > timing 우선순위).

### 단계 6 — 게이트 4종 병렬 (single message, 4 Task)

| 게이트 | 책임 |
|---|---|
| `fact-checker` | 성구 nwtsty + lfb/jy docid 검증 |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름 (빌립보서·로마서·유다서) |
| `timing-auditor` | 1800±120초, quality > timing |
| `quality-monotonic-checker` | 9축 baseline 비교 |

### 게이트 FAIL 시 재호출 (정본 — Hook X, SKILL 절차가 처리)

- HIGH = 0 → 통과
- HIGH ≥ 1 → 위반 사유 prompt 에 prepend → 단계 3 (cbs-script) · 단계 4 (assembly) 재호출 → 재빌드 + 재게이트
- 5회 한도 → 사용자 BLOCKING 알림

## 유기적 협력 (의존성 그래프)

```
scripture-deep → publication-cross-ref (성구 → lfb/jy 인용)
research 4종 → application-builder (4축 적용)
research 5종 + outline → cbs-script (사회자·낭독자 분리)
script → assembly-coordinator → SPEC (시간 마커 8개)
SPEC → build_cbs_v10.py → docx
docx → 4 게이트 (교차 검증)
```

## 재사용 자산

- `_automation/team_briefings.py::cbs_briefing()`
- `_automation/script_to_content_cbs.py` (script → SPEC 헬퍼)
- `_automation/test_script_to_content_cbs.py`
- `.claude/shared/banned-vocabulary.md` / `comment-label-standard.md`

## 핵심 차이 (vs 다른 슬롯)

- 30분 사회자 + 낭독자 별도
- 「훈」=lfb / 「예수」=jy 분리 표기
- 시간 마커 8개 빨강 볼드
- quality > timing 우선순위
