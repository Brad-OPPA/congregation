# 6단 방어 프로토콜 (Multi-Layer Defense) — 기존 "4단 방어" 의 확장

**적용 대상**: 주중집회·주말집회 모든 파트 스킬과 관련 에이전트
**제정**: 2026-04-24 (v1 — 4단) → **2026-04-25 (v2 — 6단 확장)**
**확장 사유 (v2)**: 원준님 지침 — "최종감수 전에 기획자가 나와서 기획대로 됐는지 재검수" + "에이전트가 일 시작 전 할 일 리마인드·종료 후 검수 의무화"
**원칙**: 원고의 모든 인용·해설·적용이 공식 출판물 근거를 갖도록 **6중 방어**. 에이전트는 **3번 리마인드** (지시서 → 🟢 착수 블록 → 🔴 종료 블록), 산출물은 **4회 검증** (자체 → Planner 1차 → Planner 2차 → 최종 감사 3종).
**연결 표준**: `.claude/shared/intro-and-illustration-quality.md` — 서론·예화·삽화·적절성 품질 규칙과 🟢🔴 블록 정본. 이 6단 방어의 각 게이트에서 본 파일의 체크가 병행된다.

---

## 구조 도식

```text
┌──────────────────────────────────────────────────────────────┐
│ ① 착수 전 방향 지침  (Planner → 각 서브에게)                 │
│    · 주제·요점·중점 범위를 분석                              │
│    · 서브 에이전트별 "지시서" 를 meta.yaml 에 기록           │
│    · 각 서브가 무엇을·어디서·어떤 깊이로 수집할지 명시       │
│    · ⭐ 지시서에 품질 공유 파일 Read 의무 + 🟢 착수 블록 복사 │
│      의무 + 차등 적용표 행 발췌 포함 (신규)                  │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ② 서브 에이전트 자체 검수  (각 서브 수집 후 즉시)            │
│    · 수집 항목을 원본 URL 로 재조회                          │
│    · 글자 단위·항 단위 대조 → 차이 있으면 수정               │
│    · `_selfcheck.md` 에 통과/위반 기록                       │
│    · ⭐ `_selfcheck.md` 에 🔴 종료 블록 복사·PASS/FAIL 판정   │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ③ Planner 1차 재검수  (서브 결과 → 지시서 대비)              │
│    · Planner 가 모든 서브 산출물을 Read                      │
│    · ① 지시서 대비 누락·방향 이탈 여부 점검                  │
│    · 🟢🔴 블록 존재·PASS 여부 확인                           │
│    · `_planner_review.md` 에 기록                            │
│    · NEEDS-RERUN 인 서브는 재호출 → ② 로 복귀                │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ④ Script 작성 + 자체 검수                                    │
│    · Script 에이전트가 outline.md + meta.yaml + 서브 재료를  │
│      통합해 완성 원고 생성                                   │
│    · 산출물 최상단에 🟢 착수 블록 복사·체크                  │
│    · `_selfcheck.md` 에 🔴 종료 블록 + 지시서·기획 대비 자체  │
│      판정 기록                                               │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ⑤ Planner 2차 재검수 ★신규 (최종 감사 직전, 기획자 최종 QA)  │
│    · Planner 를 다시 호출                                    │
│    · Script 완성본 ↔ 원 기획(outline.md·meta.yaml) 대조      │
│    · 이탈·누락·우회·강조점 왜곡·시간 배분 어긋남 점검        │
│    · 서론·예화·해설의 🟢🔴 블록 모두 PASS 확인               │
│    · `_planner_final_review.md` 에 판정: PASS | NEEDS-FIX    │
│    · NEEDS-FIX 이면 Script 재호출 → ④ 로 복귀                │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ⑥ 최종 통합 감사  (원고 확정 후 병렬 3개 게이트)             │
│    · fact-checker — 성구 verbatim · 인용 실존 · URL 유효성   │
│      + 공유 파일 적절성 8필터·14축 관련 사실 검증             │
│    · jw-style-checker — 용어·호칭·경어체                     │
│      + 공유 파일 삽화 종교 도상 금지·타 종교 교리 긍정 여부   │
│    · timing-auditor — 낭독 시간 (영보 제외)                  │
│    · HIGH 위반 1건 이상 → 재빌드 강제 → ④ 또는 ⑤ 로 복귀     │
└──────────────────────────────────────────────────────────────┘
```

**게이트별 산출물 파일 네이밍 규약**:

| 게이트 | 파일 |
| --- | --- |
| ① | `meta.yaml` 의 `instructions_to_subresearchers` 키 |
| ② | 서브 각자 폴더의 `_selfcheck.md` (🔴 블록 포함) |
| ③ | `research-plan/{파트}/{주차}/_planner_review.md` |
| ④ | `research-plan/{파트}/{주차}/_selfcheck.md` (Script 자체) |
| ⑤ | `research-plan/{파트}/{주차}/_planner_final_review.md` ★신규 |
| ⑥ | `research-factcheck/{YYMMDD}/`, `research-style/{YYMMDD}/`, `research-timing/{YYMMDD}/` |

---

## 단계별 책임과 파일 포맷

### ① Planner 착수 전 방향 지침

Planner 는 주차 WOL 파싱 후 `meta.yaml` 에 다음 키를 반드시 포함한다:

```yaml
instructions_to_subresearchers:
  scripture-deep: |
    이 주차 핵심 성구: 사 40:3, 사 40:31.
    중점 — 연구 노트·상호 참조·'닦아라'의 히브리어 원의.
    (피하기: 다른 장의 성구 끌어오지 말 것)
  publication-cross-ref: |
    주제 키워드: '여호와께 가르침받기', '희생'.
    우선 검색 범위: 「파수대」 연구용 2018-2025, 「익」 200-250면.
    각 단락 3~5개 충분. (피하기: 외국어판 인용 금지)
  illustration-finder: |
    요점 1 (과거 이스라엘의 귀환) 에 맞는 역사 비유 2~3개.
    요점 2 (현대 적용) 에 맞는 일상 비유 2~3개.
    (피하기: 회중 특정 인물 언급 금지)
  experience-collector: |
    주제: 희생해서 여호와께 배움. 젊은이 경험담 우선.
    연감·파수대·JW 방송 2020년 이후. (피하기: 실명 공개된 아동)
  application-builder: |
    4축 (가정·직장/학교·회중·개인 영성) 중 특히 직장·학교 포커스.
    자기점검 질문 1~2개. (피하기: 정치·국가 관련 예시)
```

각 서브 에이전트는 자기 지시서를 **먼저 Read** 한 뒤 수집에 착수한다.

### ② 서브 에이전트 자체 검수

각 서브는 수집 완료 후 동일 폴더에 `_selfcheck.md` 를 작성한다:

```markdown
# Self-Check — scripture-deep ({YYMMDD})

## 수집 요약
- 심층 조사한 성구 수: N개
- 수집 파일: gem-01-isa-40-3.md, gem-02-isa-40-31.md, ...

## 자체 검수 결과

| # | 성구 | 원본 URL 재조회 | 글자 대조 | 상태 |
|---|---|---|---|---|
| 1 | 사 40:3 | https://wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/23/40 | ✅ 일치 | OK |
| 2 | 사 40:31 | ... | ✅ 일치 | OK |
| ... | | | | |

## 지시서 대비 자체 판정
- 지시서 요구사항: "연구 노트·상호 참조·'닦아라'의 히브리어 원의"
- 실제 수집: ✅ 모든 항목 포함
- 누락 없음

## 위반 발견 시
(없음 — 전 항목 통과)
```

검수 결과가 HIGH 위반 1건이라도 있으면 서브는 **자체 수정** 후 재검수. 그래도 통과하지 못하면 `status: FAILED` 로 보고하고 종료 (Planner 가 ③ 단계에서 판단).

### ③ Planner 재검수

메인 Claude 가 모든 서브 완료 후 Planner 를 **재호출** (재검수 모드):

```text
Agent(treasures-talk-planner)  [재검수 모드]
  프롬프트: "당신이 앞서 지시서를 내린 서브 에이전트들이 수집을 완료했습니다.
  다음 경로의 산출물을 모두 Read 해서 당신이 의도한 방향대로 됐는지 재검수하세요.

  산출물 경로:
    - research-bible/{YYMMDD}/         (scripture-deep)
    - research-bible/{YYMMDD}/_selfcheck.md
    - research-topic/{YYMMDD}/         (publication-cross-ref)
    - research-topic/{YYMMDD}/_selfcheck.md
    - research-illustration/{YYMMDD}/  (illustration-finder)
    - research-illustration/{YYMMDD}/_selfcheck.md
    - research-experience/{YYMMDD}/    (experience-collector)
    - research-experience/{YYMMDD}/_selfcheck.md
    - research-application/{YYMMDD}/   (application-builder)
    - research-application/{YYMMDD}/_selfcheck.md

  당신이 meta.yaml 의 instructions_to_subresearchers 에 적어둔 지시서 대비
  다음을 점검:
    A. 지시서의 중점 범위·키워드가 실제 수집에 반영됐는가
    B. 피해야 할 항목이 잘못 포함되지 않았는가
    C. 각 서브의 _selfcheck 가 통과했는가
    D. 요점 3개에 대해 모든 카테고리(성구·출판물·예화·경험담·적용) 가 골고루 수집됐는가
    E. 서로 모순되는 내용은 없는가

  결과를 `research-plan/treasures-talk/{YYMMDD}/_planner_review.md` 에 저장:
    - 전체 판정: PASS | NEEDS-RERUN
    - 미흡 항목 목록: (항목·미흡 이유·재수집 필요 서브·재지시사항)
    - 통과 항목 요약

  NEEDS-RERUN 이면 해당 서브의 재지시사항도 구체적으로 적어라 — 메인 Claude 가
  그 지시로 서브 재호출할 것이다."
```

재검수 리포트가 `PASS` 이면 ④ 로 진행. `NEEDS-RERUN` 이면 해당 서브 재호출 → 다시 ② → ③.

### ④ Script 작성 + 자체 검수

Script 에이전트가 outline.md · meta.yaml · 서브 재료 전부를 Read 하여 완성 원고 생성. 산출물에 다음 두 블록 **반드시 포함**:

1. **산출물 최상단**: `.claude/shared/intro-and-illustration-quality.md` 의 🟢 착수 전 리마인드 블록을 복사, 모든 ☐→☑ 체크 완료
2. **동일 폴더 `_selfcheck.md`**: 같은 공유 파일의 🔴 종료 후 자체 검수 블록 복사, 8개 항목 PASS/FAIL/N·A 판정 + 지시서·기획 대비 자체 판정 요약

FAIL 있으면 Script 가 **스스로 수정 재생성** 후 재판정. 2회까지 시도해도 실패면 `status: FAILED` 보고.

### ⑤ Planner 2차 재검수 ★신규 (기획자 최종 QA, 최종 감사 직전)

메인 Claude 가 Planner 를 **두 번째로 호출** — 이번엔 script 완성본이 원래 기획을 제대로 구현했는지 대조:

```text
Agent({planner-name})  [2차 재검수 모드]
  프롬프트: "당신이 앞서 `outline.md` 와 `meta.yaml` 에 설계한 기획을 기준으로,
  Script 에이전트가 생성한 완성 원고(`script.md`) 가 그 기획대로 제대로 만들어졌는지
  최종 QA 하세요. 최종 감사(⑥) 로 넘어가기 직전의 마지막 관문입니다.

  Read 할 파일:
    - research-plan/{파트}/{주차}/outline.md         (원 기획)
    - research-plan/{파트}/{주차}/meta.yaml          (원 지시서·시간 배분)
    - research-plan/{파트}/{주차}/script.md          (완성 원고)
    - research-plan/{파트}/{주차}/_selfcheck.md      (Script 자체 판정)
    - .claude/shared/intro-and-illustration-quality.md (품질 규칙 정본)

  다음 **6축 대조**:
    A. 요점 개수·순서·제목 — 기획과 일치하는가? (요점 빠짐·추가·뒤바뀜 없음)
    B. 외부 소재 반영 — Planner 가 지시서에 명시한 외부 자료·14축 소재가 원고에 실제 등장하는가?
    C. 강조점 정확도 — Planner 가 의도한 결론·교훈이 왜곡 없이 살아 있는가?
    D. 시간 배분 — 각 요점 예상 분량이 meta.yaml 의 time_budget 과 부합하는가?
    E. 공유 파일 🟢🔴 블록 — 두 블록 모두 존재하고 전 항목 PASS 인가?
    F. 이탈·우회 — 지시서에서 '피하기' 로 지정한 항목을 원고가 어기지 않았는가?

  결과를 `research-plan/{파트}/{주차}/_planner_final_review.md` 에 저장:
    - 전체 판정: PASS | NEEDS-FIX
    - 6축별 판정·증거·사유
    - NEEDS-FIX 이면: 구체적 수정 지시사항 (어느 단락·어느 문장을 어떻게)
    - PASS 이면: ⑥ 최종 감사로 진행해도 됨 명시

  NEEDS-FIX 이면 메인 Claude 가 Script 에이전트를 재호출해 그 지시대로 수정 → 다시 ⑤."
```

**PASS 이어야 ⑥ 로 진행 가능**. NEEDS-FIX 시 ④ 로 복귀해 수정 → 다시 ⑤.

### ⑥ 최종 통합 감사

원고(script.md + docx) 확정 후 **3개 감수 에이전트 병렬 호출**:

```text
Agent(fact-checker)         → research-factcheck/{YYMMDD}/
Agent(jw-style-checker)     → research-style/{YYMMDD}/
Agent(timing-auditor)       → research-timing/{YYMMDD}/   (영보 제외)
```

**각 감수자는 공유 파일 규칙에서 본인 담당 항목을 독립 재검**:

- `fact-checker` — 성구 verbatim · 인용 실존 · URL 유효성 + 공유 파일 14축·적절성 8필터 관련 **사실 검증** (연도·인명·수치·출처 1차 자료 교차)
- `jw-style-checker` — 용어·호칭·경어체 + 공유 파일 **삽화 종교 도상 금지**·**타 종교 교리 긍정 여부**·**정치 중립성** 감수
- `timing-auditor` — 낭독 시간 (영보 제외)

**재빌드 판정**: 3개 중 하나라도 HIGH 위반이 있으면 재빌드. script 재생성 → ⑤ Planner 2차 재검수 → docx 재렌더 → 동일 감수 재호출해서 HIGH 0건 확인.

---

## 재호출 한도

- 서브 에이전트 ②→재수집: 서브 스스로 2회까지
- Planner ③ NEEDS-RERUN: 1회까지 (그래도 실패하면 메인 Claude 가 원준님께 보고)
- Script ④ 자체 수정: 2회까지
- **Planner ⑤ NEEDS-FIX**: 2회까지 (그래도 실패하면 원준님께 보고)
- ⑥ 재빌드: 2회까지 (그래도 실패하면 원준님께 수동 확인 요청)

무한 루프 방지. 어느 한도에 걸리면 현재까지의 산출물과 실패 사유를 원준님께 그대로 보고하고 판단을 요청.

---

## 이 프로토콜이 적용되는 스킬

- Phase 1 (4단, 2026-04-24): `/mid-talk10`, `/cbs`, `/local-needs`
- Phase 2 (4단): `/dig-treasures`, `/mid-talk5`, `/living-part`
- Phase 3 (4단): `/mid-student1/2/3/4`, `/week-study`, `/publictalk`
- **Phase 4 (6단 확장, 2026-04-25)**: `/mid-talk10`, `/dig-treasures`, `/week-study` — 서론·예화·삽화 품질 표준 결합. Planner 2차 재검수 의무화. (나머지 스킬은 순차 확장 예정.)

학생 과제 실연(mid-student2/3/4) 은 원준님 예시 수령 후 고도화 시 Phase 3 에 포함.

---

## 스킬 본문에 삽입할 표준 호출 문구

각 스킬의 Agent 호출 프롬프트 **맨 위** 에 다음 문구를 넣어 프로토콜 준수를 명시:

> ⚠ 이 호출은 `.claude/shared/multi-layer-defense.md` 의 **6단 방어 프로토콜(v2)** 에 따른다. 먼저 해당 문서를 Read 해서 본인의 역할(①~⑥ 중 어느 단계인지) 을 확인한 뒤 작업하라.
>
> 또한 `.claude/shared/intro-and-illustration-quality.md` 를 **반드시 Read** 하고, 본인이 해당 파트의 차등 적용표 행에서 요구하는 규칙을 숙지하라. 산출물 최상단에 🟢 착수 전 리마인드 블록을 복사·체크하고, 완료 후 `_selfcheck.md` 에 🔴 종료 후 자체 검수 블록을 복사·판정하는 것이 **작업 개시·완료의 필수 조건**이다.

---

## 개정 이력

- 2026-04-24 v1 — 초안 (원준님 지침: 품질 최우선·오류 0 목표). 4단 구조.
- **2026-04-25 v2** — 6단 확장. ⑤ Planner 2차 재검수(기획자 최종 QA) 신규 추가. 🟢 착수 블록 · 🔴 종료 블록 의무화. `.claude/shared/intro-and-illustration-quality.md` 와 교차 참조 체계 확립. Phase 4 스킬군(mid-talk10·dig-treasures·week-study) 최초 적용.
