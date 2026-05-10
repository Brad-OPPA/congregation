---
name: week-study
description: 주말집회 "파수대 연구 사회" 60분 통합 정본 docx 1편 자동 생성. 인자 `now|next1|next2|next3` (없으면 대화형). 메인 Claude 가 6 단계 (planner → 7 research 병렬 → watchtower-study-script ★ → Bash 빌드 → 4종 게이트) 자동 절차로 진행. 단계 내부 single message multi-tool 병렬, 게이트 FAIL 시 단계 3 (script) 재호출 (5회 한도). ver11 + 9 항목 + 저녁 추가 명시 통합 정본 자동화. 매주 동일 톤 보장. 트리거 "/week-study", "파수대 사회 만들어 줘", "파수대 예습".
---

# SKILL: week-study (파수대 연구 사회, 통합 정본 자동화 v10)

## 정본 (단일 진실의 원천)

**정본 = ver11 패턴 + 9 항목 (낮 명시) + 저녁 추가 명시 = 단일 통합 정본**.

세부: `/Users/brandon/.claude/plans/adaptive-wandering-thunder.md` v10 + `.claude/shared/canonical-build-checklist.md`

**자동화 의무**: `/week-study` 호출 1회 = 매주 동일 톤 통합 정본 docx. 매번 사람 수동 작성 X.

## 정본 절차 (메인 Claude = 오케스트레이터)

### 단계 0 — Preflight (1 Bash)

```bash
git -C /Users/brandon/Claude/Projects/Congregation pull --ff-only
```

기존 `_verN_` 산출물 skip 정책 (`.claude/shared/skip-existing-policy.md`). 사용자 확정 OK build (`ok-builds.json`) 가 있으면 baseline.

### 단계 1 — planner 호출 (1 Task)

`Task(subagent_type="watchtower-study-planner", ...)` — prompt prepend:
- 정본 brief (`_automation/team_briefings.py::watchtower_briefing()`)
- 주차 (`now`/`next1`/`next2`/`next3`)
- WOL 인덱스 docid 1102016XXX 검증 의무

산출물: `outline.md` (17 블록 spec) + `meta.yaml`.

### 단계 2 — 7 research 병렬 (single message, 7 Task)

| 에이전트 | 책임 | 산출 |
|---|---|---|
| `scripture-deep` | 본항 인용 성구 + 표어 성구 nwtsty verbatim + 어근·평행 | `research-bible/{ymd}_canon_v4/key_scripture_narratives.py` |
| `publication-cross-ref` | 「파」 과거호 / 「통」 / 「예-1」 / 「훈」 출판물 인용 ≥ 10 (INTEGRATED.depth) | INTEGRATED.depth 부분 |
| `illustration-finder` | 시드 이미지 다운로드 + 본항 강화 [Y] description+commentary | `research-illust/{ymd}_canon_v4/downloaded.py` + `illust_commentary.py` |
| `qa-designer` | 복습 답변 3~5개 (인물 회상·어근) | `research-illust/{ymd}_canon_v4/recap_answers.py` |
| `experience-collector` | 회중 경험담·jw.org 체험기 footnote_excerpt | INTEGRATED.footnote_excerpt 부분 |
| `application-builder` | 항별 4축 (가정·직장·회중·개인) 적용 + 자기점검 | INTEGRATED.key_point + real_life 부분 |
| `prayer-composer` (선택) | 시작·마침 기도 (필요 시) | `research-prayer/{ymd}/` |

각 prompt 에 단계 1 outline 발췌 prepend.

5 자료 통합 산출 = `research-plan/watchtower/{ymd}_canon/integrated_commentary.py` (publication-cross-ref + experience-collector + application-builder 통합 결과). publication-cross-ref 가 통합 책임자 또는 메인 Claude 가 단계 2 종료 후 통합.

### 단계 3 — watchtower-study-script ★ (1 Task, 자동화 핵심 lock-in)

`Task(subagent_type="watchtower-study-script", ...)`

책임:
- outline.md + 5 research 자료 + 자동 base spec.py → spec dict 자동 통합
- INTEGRATED 17 블록 5필드 박기
- NARRATIVES key_scripture[*] 박기
- RECAP_ANSWERS spec.recap_section
- 결론 paragraphs 자동 작성 (인물 회상 + 4축 + 표어)
- 메인 성구 박스 (NAKDOK 매칭 + NWT verbatim fetch)
- spec stock 청소 + 이미지 정확 매핑

산출:
- `script.md` (사람용 사회자 진행 원고)
- `content_wt_{ymd}.py` (자동 빌드 코드)
- `_selfcheck.md` (자체 검수)

세부: `.claude/agents/watchtower-study-script.md`

### 단계 4 — Bash 빌드 (1 Bash)

```bash
python3 "/path/to/Dropbox/.../{folder}/_source/spec.py"  # 변경 없을 시
python3 "/path/to/Dropbox/.../{folder}/content_wt_{ymd}.py"  # 통합 빌드
```

또는:
```bash
cd /Users/brandon/Claude/Projects/Congregation/_automation
python3 -c "exec(open('/path/to/content_wt_{ymd}.py').read())"
```

`content_wt_{ymd}.py` 가 INTEGRATED + NARRATIVES + RECAP + 메인박스 + 이미지 통합 후 `build_watchtower(spec, OUT)` 호출 → docx + PDF 출력 + LibreOffice PDF 자동 변환.

### 단계 5 — 게이트 4종 병렬 (single message, 4 Task)

| 게이트 | 책임 |
|---|---|
| `fact-checker` | 성구 NWT verbatim · 출판물 URL · docid 검증 |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름·NG 어휘 |
| `timing-auditor` | 분량·시간 마커 (quality > timing) |
| `quality-monotonic-checker` | 9축 baseline (5/31 ver11) ≥ 100% |

### 게이트 FAIL 시 재호출 (SKILL 절차)

- HIGH = 0 → 통과
- HIGH ≥ 1 → 위반 사유 prompt 에 prepend → **단계 3 (watchtower-study-script) 재호출** → 재빌드 + 재게이트
- 5회 한도 → 사용자 BLOCKING 알림

## 유기적 협력 (의존성 그래프 v10)

```
WOL scrape (자동, body_runs <strong> 보존)
    ↓
watchtower-study-planner → outline.md
    ↓
[7 research 병렬]
  ├─ scripture-deep → NARRATIVES
  ├─ publication-cross-ref → INTEGRATED.depth
  ├─ experience-collector → INTEGRATED.footnote_excerpt
  ├─ application-builder → INTEGRATED.key_point + real_life
  ├─ illustration-finder → IMAGE_PATHS + illust_commentary
  ├─ qa-designer → RECAP_ANSWERS
  └─ prayer-composer → 기도 (선택)
    ↓
watchtower-study-script ★ (lock-in)
    → 5 자료 통합 → spec dict + content_wt_{ymd}.py + script.md
    ↓
build_watchtower v9 (낭독 박스·자동 강조 폐기·body_runs)
    → docx + PDF
    ↓
[4 게이트 병렬]
  fact + style + timing + quality
    → FAIL → script 재호출 (5회 한도)
    → PASS → 사용자 산출물 (매주 동일 톤)
```

## 재사용 자산

- `.claude/agents/watchtower-study-script.md` ★ — 자동화 핵심
- `.claude/agents/watchtower-study-planner.md` — outline
- `_automation/build_watchtower.py` v9 — 낭독 박스 + 자동 강조 폐기 + body_runs
- `_automation/scrape_wt.py` v9 — `<strong>` 보존
- `_automation/team_briefings.py::watchtower_briefing()`
- `.claude/shared/canonical-build-checklist.md` v3 — 9 항목 + 저녁 명시
- `.claude/shared/quality-monotonic-policy.md` — 베이스라인 ver11 100%
- `.claude/shared/ok-builds.json` — 5/31 ver11 baseline
- `research-illust/v11_pattern_build.py` — 4 슬롯 통일 빌드 패턴 참고
- `/Users/brandon/.claude/plans/adaptive-wandering-thunder.md` v10 — 단일 진실의 원천

## 핵심 차이 (vs 다른 슬롯)

- 60분 17 블록 (cbs 30분 7~12 문단 vs 다름)
- 「」 출판물 인용 ≥ 10
- 외부 14축 ≥ 3
- block 단위 host_cue 주입 (자동 base)
- INTEGRATED·NARRATIVES·RECAP 5 자료 통합 (script 에이전트 책임)
- ver11 베이스라인 ≥ 100%

## 자동화 보장 (매번 동일 톤)

- script 에이전트 = 자료에 박기만 책임 (자료 자체 변경 X)
- 자동 강조 폐기 (빌더 자동 칠 X — 명시 [Y] 마커만)
- 5/31 ver11 베이스라인 ≥ 100% 의무 (quality-monotonic-checker)
- 4 게이트 통과 의무 (fact·style·timing·quality)
- 매번 결과 다르게 X (자료 변하지 않으면 결과 동일)
