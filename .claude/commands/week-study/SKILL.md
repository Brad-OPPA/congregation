---
name: week-study
description: 주말집회 "파수대 연구 사회" 60분 통합 정본 docx 1편 자동 생성. 인자 `now|next1|next2|next3` (없으면 대화형). **ver13 정본** (사용자 OK 2026-05-11) 자동 lock-in — INTEGRATED 자료 [Y] 마커 자동 삽입 + 빌더 v9 (낭독 성구 박스 통합 라벨 + 자동 강조 폐기 + body_runs <strong> 보존) + 5/17·24·31 baseline ≥ 100% 의무. 메인 Claude 가 7 단계 자동 절차로 진행 (planner → 7 research 병렬 → watchtower-study-script ★ → PHRASES 추출 → [Y] 마커 자동 삽입 → 빌드 → 4종 게이트). 단계 내부 single message multi-tool 병렬, 게이트 FAIL 시 단계 3 (script) 재호출 (5회 한도). 매주 동일 톤 보장 — 매번 사람 수동 작성 X. 트리거 "/week-study", "파수대 사회 만들어 줘", "파수대 예습".
---

# SKILL: week-study (파수대 연구 사회, ver13 절대 정본 자동화 v13)

## ✅ ver13 절대 정본 (2026-05-11 사용자 OK)

**baseline = `.claude/shared/ok-builds.json` v2** — 5/17·24·31 ver13 모두 등록.

| 슬롯 | 노랑 핵심 ≤25자 | 메인 박스 | 이미지 | 단락 |
|---|---|---|---|---|
| 5/17 ver13 | 426 | 6 | 4 | 504 |
| 5/24 ver13 | 400 | 7 | 2 | 506 |
| 5/31 ver13 | 421 | 8 | 3 | 560 |

**다음 주차 (6/7~) 부터 모든 빌드 = ver13 메트릭 ≥ 100% 의무**. 미달 시 quality-monotonic-checker NO-GO + 자동 재빌드 (5회 한도).

세부:
- plan: `/Users/brandon/.claude/plans/adaptive-wandering-thunder.md` v13
- 체크리스트: `.claude/shared/canonical-build-checklist.md` v4
- ver13 빌드 코드 참조: `research-illust/ver13_build.py`
- PHRASES 자료: `research-illust/phrases_260{517,524,531}.py`

---

## 🔒 자동화 의무 (매주 동일 톤)

`/week-study` 호출 1회 = 매주 자동 ver13 식 통합 정본 docx 생성.
- 매번 사람 수동 작성 X (PHRASES dict, content_wt_*.py 모두 자동)
- 매번 결과 다르게 X (자료 변경 X 시 결과 동일)
- 사용자 검수 = 검증 OK 후 baseline 업데이트만

---

## 정본 절차 (메인 Claude = 오케스트레이터)

### 단계 0 — Preflight (1 Bash)

```bash
git -C /Users/brandon/Claude/Projects/Congregation pull --ff-only
```

기존 `_verN_` 산출물 skip 정책 (`.claude/shared/skip-existing-policy.md`). ok-builds.json baseline = ver13 채택.

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
| `publication-cross-ref` | 「파」 과거호 / 「통」 / 「예-1」 / 「훈」 출판물 인용 ≥ 10 (INTEGRATED.depth) | INTEGRATED.depth |
| `illustration-finder` | 시드 이미지 다운로드 + 본항 강화 [Y] description+commentary | `research-illust/{ymd}_canon_v4/downloaded.py` + `illust_commentary.py` |
| `qa-designer` | 복습 답변 3~5개 (인물 회상·어근) | `research-illust/{ymd}_canon_v4/recap_answers.py` |
| `experience-collector` | 회중 경험담·jw.org 체험기 footnote_excerpt | INTEGRATED.footnote_excerpt |
| `application-builder` | 항별 4축 (가정·직장·회중·개인) 적용 + 자기점검 | INTEGRATED.key_point + real_life |
| `prayer-composer` (선택) | 시작·마침 기도 (필요 시) | `research-prayer/{ymd}/` |

각 prompt 에 단계 1 outline 발췌 prepend.

5 자료 통합 → `research-plan/watchtower/{ymd}_canon/integrated_commentary.py` (publication-cross-ref + experience-collector + application-builder 통합 결과).

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

### 단계 4 ★★ — PHRASES 추출 + [Y] 마커 자동 삽입 (ver13 정본 핵심)

INTEGRATED 자료에 핵심 명사구 [Y] 마커가 박혀야 사용자 명시 패턴과 일치.

#### 4-A. PHRASES 추출 (1 Task, 작은 출력)

`Task(subagent_type="general-purpose", description="{ymd} PHRASES 추출", ...)` 또는 `publication-cross-ref` mode 2:

**핵심 — 출력 토큰 한도 회피 의무**:
- 입력: INTEGRATED_COMMENTARY 17 블록 dict (큼)
- 출력: PHRASES dict 만 (작음 — 5K자 안)
- 절대 텍스트 전체를 다시 출력하지 X (32K 토큰 초과 회피)

prompt 양식:
```
파수대 사회 {ymd} INTEGRATED_COMMENTARY 17 블록 5필드 (answer/depth/key_point/real_life/footnote_excerpt) 텍스트에서 핵심 명사구 1~3개씩만 추출.

원본 자료: research-plan/watchtower/{ymd}_canon/integrated_commentary.py

추출 규칙:
- 5~25자 짧은 핵심 명사구만 (긴 문장 X)
- 어근·평행·핵심 동사구·인용 어구 우선
- 한 단락당 1~3개 (과다 X)
- 「출판물명」·성구 ref·수치 X
- 성구 verbatim 안 어구 X
- 원본 텍스트에 정확히 등장하는 어구만 (re.sub 매칭)

출력: Python dict literal 만 (chat 출력, 파일 X)
```python
PHRASES = {
  (block_idx, 'field_name'): ["명사구1", "명사구2"],
  ...
}
```

비어있는 필드는 키 omit. dict literal 만 chat 출력.
```

산출 저장: `research-illust/phrases_{ymd}.py`

#### 4-B. [Y] 마커 자동 삽입 (Python re.sub, LLM 호출 0)

메인 Claude 가 결정적 코드로 INTEGRATED 텍스트에 마커 박음:

```python
def insert_yhl(text, phrases):
    """텍스트에 [Y]phrase[/Y] 마커 삽입. 이미 박힌 곳 skip."""
    if not text or not phrases: return text
    sorted_phrases = sorted(set(phrases), key=lambda x: -len(x))
    for ph in sorted_phrases:
        if not ph or len(ph) < 3: continue
        pat = re.compile(re.escape(ph))
        m = pat.search(text)
        if m:
            before = text[:m.start()]
            if before.count('[Y]') > before.count('[/Y]'):
                continue
            text = text[:m.start()] + '[Y]' + m.group() + '[/Y]' + text[m.end():]
    return text
```

빌드 시 INTEGRATED 17 블록 × 5필드 모두 적용 → spec dict.

### 단계 5 — Bash 빌드 (1 Bash)

```bash
python3 "/path/to/Dropbox/.../{folder}/content_wt_{ymd}.py"
```

또는 `research-illust/ver13_build.py` 패턴 그대로 (3 슬롯 통합 빌드).

`build_watchtower v9` 자동 적용:
- 낭독 성구 박스 통합 라벨 ("낭독 성구 ref verbatim" 회색 바탕 검은 볼드)
- 자동 강조 폐기 (명시 [Y] 마커만 처리)
- body_runs `<strong>` 보존
- LibreOffice PDF 자동 변환

### 단계 6 — 게이트 4종 병렬 (single message, 4 Task)

| 게이트 | 책임 |
|---|---|
| `fact-checker` | 성구 NWT verbatim · 출판물 URL · docid |
| `jw-style-checker` | 용어·금칙어·NWT 책 이름·NG 어휘 |
| `timing-auditor` | 분량·시간 마커 (quality > timing) |
| `quality-monotonic-checker` | **ver13 baseline ≥ 100% 의무** |

#### quality-monotonic-checker 자동 검증 (의무)

baseline = `ok-builds.json` v2 의 ver13 entries (5/17·24·31).

신규 docx 메트릭 ≥ baseline:
- 노랑 ≤25자 (highlight_short) ≥ 400
- 메인 박스 ≥ 6
- 이미지 ≥ 2
- 단락 ≥ 500
- 출판물 인용 ≥ 120

미달 1축이라도 → NO-GO.

### 게이트 FAIL 시 재호출 (SKILL 절차)

- HIGH = 0 → 통과
- HIGH ≥ 1 → 위반 사유 prompt 에 prepend → **단계 3 (watchtower-study-script) 또는 단계 4 (PHRASES) 재호출** → 재빌드 + 재게이트
- 5회 한도 → 사용자 BLOCKING 알림

---

## 자동화 의존성 그래프 (ver13 정본)

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
watchtower-study-script ★ — spec dict 통합
    → content_wt_{ymd}.py + script.md
    ↓
PHRASES 추출 ★★ (단계 4-A, 작은 출력)
    → research-illust/phrases_{ymd}.py
    ↓
[Y] 마커 자동 삽입 (단계 4-B, Python re.sub)
    → INTEGRATED 5필드 모두 [Y] 박힘
    ↓
build_watchtower v9 (낭독 박스·자동 강조 폐기·body_runs)
    → docx + PDF
    ↓
[4 게이트 병렬]
  fact + style + timing + quality (ver13 ≥ 100%)
    → FAIL → script 또는 PHRASES 재호출 (5회 한도)
    → PASS → 사용자 산출물 (매주 동일 톤)
```

---

## 재사용 자산 (모두 git 영구화)

### 빌더 (`automation 82acc13` master)
- `_automation/build_watchtower.py` v9 — 낭독 박스 + 자동 강조 폐기 + body_runs
- `_automation/scrape_wt.py` v9 — `<strong>` 보존
- `_automation/team_briefings.py::watchtower_briefing()`

### 에이전트
- `.claude/agents/watchtower-study-script.md` ★ — 자동화 핵심 lock-in
- `.claude/agents/watchtower-study-planner.md` — outline
- 7 research 에이전트 (scripture-deep · publication-cross-ref · illustration-finder · qa-designer · experience-collector · application-builder · prayer-composer)

### 정책·체크리스트
- `.claude/shared/canonical-build-checklist.md` v4 — 9 항목 + 저녁 명시 + ver13 baseline
- `.claude/shared/quality-monotonic-policy.md` — ver13 100% 의무
- `.claude/shared/ok-builds.json` v2 — ver13 baseline (5/17·24·31)
- `/Users/brandon/.claude/plans/adaptive-wandering-thunder.md` v13 — 단일 진실의 원천

### ver13 빌드 코드 (참조용)
- `research-illust/ver13_build.py` — 3 슬롯 통합 빌드
- `research-illust/phrases_260{517,524,531}.py` — PHRASES dict
- `research-illust/canon_v8_illust.py` — 12 삽화 [Y] description+commentary

### 자료 (자동 수집/생성)
- `research-plan/watchtower/{ymd}_canon/integrated_commentary.py` — INTEGRATED 5필드
- `research-bible/{ymd}_canon_v4/key_scripture_narratives.py` — NARRATIVES
- `research-illust/{ymd}_canon_v4/downloaded.py` — IMAGE_PATHS
- `research-illust/{ymd}_canon_v4/recap_answers.py` — RECAP_ANSWERS

---

## 핵심 차이 (vs 다른 슬롯)

- 60분 17 블록
- 「」 출판물 인용 ≥ 120
- 외부 14축 ≥ 3
- block 단위 host_cue 주입 (자동 base)
- 6 자료 통합 (INTEGRATED·NARRATIVES·RECAP·이미지·삽화 commentary·PHRASES)
- ver13 베이스라인 ≥ 100% (5축 자동 검증)

## 자동화 보장 (매번 동일 톤)

- script 에이전트 = 자료 박기만 (자료 자체 변경 X)
- 자동 강조 폐기 → 명시 [Y] 마커만
- ver13 baseline ≥ 100% (quality-monotonic-checker)
- 4 게이트 통과 의무 (fact·style·timing·quality)
- 매번 결과 다르게 X (자료 변경 X 시 결과 동일)

---

## NOT 할 것 (반복 차단 — 5/10 교훈)

- ❌ canon_vN 패턴 새로 만들기 — ver13 패턴 그대로
- ❌ Task 호출 시 출력 32K 토큰 초과 — PHRASES dict 만 출력 (작은 LLM 출력 + 결정적 변환)
- ❌ 자료 (INTEGRATED·NARRATIVES·RECAP) 매번 새로 만들기 — research 에이전트 자동
- ❌ 빌더 새 fix — v9 그대로
- ❌ 사용자 정본 (`_ver10_`·`_ver11_`·`_ver13_`·평이름) 변경 — 보존
- ❌ 같은 명시 또 받기 — plan v13 단일 진실의 원천
- ❌ 사용자 검수 의존 — 자동 검증 (4 게이트) 통과 후 사용자 OK
