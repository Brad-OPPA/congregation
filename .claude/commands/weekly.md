---
name: weekly
description: 매주 월요일 1회 실행 — 4 슬롯 × 3 주차 = 12 빌드 일괄. 메인 Claude 가 32 에이전트 오케스트레이터로 6 단계 (planner → research 4종 → application+script → assembly → 빌드 → 게이트 4종) 절차를 슬롯·주차 곱셈으로 진행. 단계별 single message multi-tool 병렬. 게이트 FAIL 시 단계 3·4 재호출 (5회 한도, SKILL 절차 책임 — Hook X). 4 슬롯 = 파수대 연구 / 회중 성서 연구 / 10분 연설 / 영적 보물찾기. 트리거 "/weekly", "주간 자료 만들어 줘".
---

# SKILL: weekly (4 슬롯 × 3 주차 일괄, 12 빌드)

## 정본 절차 (메인 Claude = 오케스트레이터, 변경 X)

메인 Claude 는 4 슬롯 = `week-study` / `cbs` / `mid-talk10` / `dig-treasures`, 3 주차 = `now` / `next1` / `next2` 를 곱한 12 빌드 매트릭스를 다음 6 단계로 진행한다. 단계 내부는 single message multi-tool 병렬, 단계 사이는 의존 순차.

### 단계 0 — Preflight (1 Bash)

```bash
git -C /Users/brandon/Claude/Projects/Congregation pull --ff-only
python3 /Users/brandon/Claude/Projects/Congregation/_automation/quality_baseline.py --list-ok
```

기존 산출물 skip 정책 (`.claude/shared/skip-existing-policy.md`) 확인. 누락 슬롯·주차만 다음 단계 진행.

### 단계 1 — planner 병렬 (single message, 12 Task)

12 Task 동시 호출:

| 슬롯 | subagent_type |
|---|---|
| 파수대 | `watchtower-study-planner` |
| CBS | `cbs-planner` |
| 10분 연설 | `treasures-talk-planner` |
| 영적 보물찾기 | `spiritual-gems-planner` |

각 prompt 에 정본 brief prepend (출처: `_automation/team_briefings.py`) + 주차 (`now`/`next1`/`next2`) + WOL 인덱스 docid 명시.

산출물: 슬롯·주차별 `outline.md` + `meta.yaml`.

### 단계 2 — research 4 보조 병렬 (single message, 48 Task = 12 × 4)

| 에이전트 | 책임 |
|---|---|
| `scripture-deep` | 핵심 성구 nwtsty verbatim 추출 |
| `publication-cross-ref` | 「파」·「통」·「예-1」·「훈」 출판물 인용 매칭 |
| `illustration-finder` | 외부 14축 예화·삽화 후보 + `download_image.py` 시드 이미지 |
| `experience-collector` | 경험담·적용 사례 |

각 prompt 에 단계 1 outline 발췌 prepend.

산출물: `research-bible/{YYMMDD}/`, `research-pub/{YYMMDD}/`, `research-illust/{YYMMDD}/`, `research-exp/{YYMMDD}/`.

### 단계 3 — application + script (의존 순차, 슬롯별 2 Task)

병렬 단위 = 12 슬롯·주차. 각 슬롯·주차 내부는 순차:

1. `application-builder` ← research 4종 결과 → 4축 적용점 (생활/봉사/교리/회중)
2. 슬롯별 script 에이전트 ← outline + research 5종 → 본문·결론·서론 LLM draft

| 슬롯 | script 에이전트 |
|---|---|
| 파수대 | (script 에이전트 통합 또는 watchtower-study-planner 가 겸임) |
| CBS | `cbs-script` |
| 10분 연설 | `treasures-talk-script` |
| 영적 보물찾기 | `spiritual-gems-script` |

산출물: `script.md` (자연스러운 본문·결론·서론, LLM 작성).

### 단계 4 — assembly + content_*.py (single message, 12 Task)

| 슬롯 | coordinator |
|---|---|
| 파수대 | `assembly-coordinator` |
| CBS | `assembly-coordinator` (또는 cbs 전용 분기) |
| 10분 연설 | `assembly-coordinator` |
| 영적 보물찾기 | `gem-coordinator` |

책임: script.md → spec dict 검증·생성 (`content_*_YYMMDD.py`). 4축·5요소·핵심 성구·시간 마커 누락 시 빌드 차단 트리거.

### 단계 5 — Bash 빌드 (single message, 12 Bash 병렬)

```bash
python3 _automation/build_watchtower.py {YYMMDD}
python3 _automation/build_cbs_v10.py {YYMMDD}
python3 _automation/build_treasures_talk.py {YYMMDD}
python3 _automation/build_spiritual_gems.py {YYMMDD}
```

순수 렌더러 (LLM 호출 0). `validate_spec_integrity` / `verify_spec_scriptures` / `enforce_all_seed_images` 가 spec 무결성 자동 검증 후 docx + PDF 출력.

### 단계 6 — 게이트 4종 병렬 (single message, 48 Task = 12 × 4)

| 게이트 | 책임 |
|---|---|
| `fact-checker` | 성구·출판물·URL·docid 검증 |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름·사용자 NG list |
| `timing-auditor` | 분량·시간 마커 (timing FAIL ≠ 빌드 NO-GO; quality > timing) |
| `quality-monotonic-checker` | 9축 baseline 비교 (글자수·성구·출판물·외부 14축·시간 마커·깊이 단락·이미지·구성·SPEC) |

게이트 4종 모두 PASS = 슬롯·주차 통과. quality-monotonic 결과를 timing-auditor 가 참고, jw-style 위반 시 fact-checker 가 인용 재검증 (교차 검증).

### 게이트 FAIL 시 재호출 (정본 — Hook 책임 X, SKILL 절차가 처리)

게이트 결과 통합 후:

- HIGH 위반 = 0 → 빌드 정본 채택, 다음 슬롯·주차 진행
- HIGH 위반 ≥ 1 → 위반 사유 + 해당 슬롯 prompt 에 prepend → 단계 3 (script) · 단계 4 (assembly) 재호출 (해당 슬롯·주차만, 격리) → 단계 5 재빌드 → 단계 6 재게이트
- 5회 한도 도달 → 사용자 BLOCKING 알림 (`재작성 5회 도달, 슬롯 X 주차 Y 수동 검토 필요`)

다른 슬롯·주차에 영향 X (격리 보장).

## 유기적 협력 (의존성 그래프)

```
scripture-deep ─┐
                ├─→ publication-cross-ref (성구 → 출판물 매칭)
                │       ↓
                ├─→ application-builder (성구 + 출판물 → 4축 적용)
                │       ↓
illustration-finder ─→ script (예화 + 출판물 + 성구 → 본문)
                │       ↓
experience-collector ─→ script (경험담 + 본문 → 결론)
                ↓
            coordinator → spec dict (`content_*.py`)
                ↓
            빌더 → docx + PDF
                ↓
            4 게이트 (교차 검증) → PASS / 단계 3·4 재호출
```

## 재사용 자산 (영구 라이브러리)

- `_automation/team_briefings.py` — 5팀 정본 brief
- `_automation/quality_baseline.py` — OK builds 우선 사용 분기
- `_automation/mark_ok_build.py` — 사용자 OK 등록
- `.claude/shared/ok-builds.json` — 5/31 v3 1호 baseline
- `.claude/shared/skill-agent-mapping.md` — SKILL 단계 ↔ 에이전트 매핑 정본
- `.claude/shared/banned-vocabulary.md` — 금칙어·사용자 NG
- `.claude/shared/user-quality-standard.md` — 사용자 품질 표준
- 빌더 5종의 `validate_spec_integrity` / `verify_spec_scriptures` / `enforce_all_seed_images`

## 출력

12 docx + 12 PDF (회중 정본 폴더 + Dropbox), 게이트 통과 리포트, 재호출 통계.

자동 빌드 산출물은 baseline (`_verN_`) 으로 보존. 회중 발송 정본은 사용자 손질본 (`_final.docx`) 별도.
