# 4단 방어 프로토콜 (Multi-Layer Defense)

**적용 대상**: 주중집회·주말집회 모든 파트 스킬과 관련 에이전트
**제정**: 2026-04-24 — 원준님 품질 우선 지침에 따름
**원칙**: 원고의 모든 인용·해설·적용이 공식 출판물 근거를 갖도록 **4중 방어**

---

## 구조 도식

```
┌──────────────────────────────────────────────────────────────┐
│ ① 착수 전 방향 지침  (Planner → 각 서브에게)                 │
│    · 주제·요점·중점 범위를 분석                              │
│    · 서브 에이전트별 "지시서" 를 meta.yaml 에 기록           │
│    · 각 서브가 무엇을·어디서·어떤 깊이로 수집할지 명시       │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ② 서브 에이전트 자체 검수  (각 서브 수집 후 즉시)            │
│    · 수집한 모든 항목을 원본 URL 로 재조회                   │
│    · 글자 단위·항 단위 대조 → 차이 있으면 수정               │
│    · `_selfcheck.md` 에 통과/위반 기록                       │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ③ 보고 + Planner 재검수  (메인 Claude 가 Planner 재호출)    │
│    · Planner 가 모든 서브 산출물을 Read                      │
│    · ① 지시서 대비 누락·방향 이탈 여부 점검                  │
│    · 미흡 항목을 `_planner_review.md` 에 기록                │
│    · 재수집 필요한 서브는 재호출                             │
└──────────────────────────────────────────────────────────────┘
                          ↓
              (Script 에이전트도 ①~③ 동일 적용)
                          ↓
┌──────────────────────────────────────────────────────────────┐
│ ④ 최종 통합 감사  (원고 완성 후 병렬 3개 게이트)             │
│    · fact-checker — 성구 verbatim · 인용 실존 · URL 유효성   │
│    · jw-style-checker — 용어·호칭·경어체                     │
│    · timing-auditor — 낭독 시간 (영보 제외)                  │
│    · HIGH 위반 1건 이상 → 재빌드 강제                        │
└──────────────────────────────────────────────────────────────┘
```

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

```
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

### ④ 최종 통합 감사

원고(script.md + docx) 완성 후 **3개 감수 에이전트 병렬 호출**:

```
Agent(fact-checker)         → research-factcheck/{YYMMDD}/
Agent(jw-style-checker)     → research-style/{YYMMDD}/
Agent(timing-auditor)       → research-timing/{YYMMDD}/   (영보 제외)
```

**재빌드 판정**: 3개 중 하나라도 HIGH 위반이 있으면 재빌드. script 재생성 → docx 재렌더 → 동일 감수 재호출해서 HIGH 0건 확인.

---

## 재호출 한도

- 서브 에이전트 ②→재수집: 서브 스스로 2회까지
- Planner ③ NEEDS-RERUN: 1회까지 (그래도 실패하면 메인 Claude 가 원준님께 보고)
- ④ 재빌드: 2회까지 (그래도 실패하면 원준님께 수동 확인 요청)

무한 루프 방지.

---

## 이 프로토콜이 적용되는 스킬

- Phase 1 (첫 적용): `/mid-talk10`, `/cbs`, `/local-needs`
- Phase 2: `/dig-treasures`, `/mid-talk5`, `/living-part`
- Phase 3: `/mid-student1/2/3/4`, `/week-study`, `/publictalk`

학생 과제 실연(mid-student2/3/4) 은 원준님 예시 수령 후 고도화 시 Phase 3 에 포함.

---

## 스킬 본문에 삽입할 표준 호출 문구

각 스킬의 Agent 호출 프롬프트 **맨 위** 에 다음 한 줄을 넣어 프로토콜 준수를 명시:

> ⚠ 이 호출은 `.claude/shared/multi-layer-defense.md` 의 4단 방어 프로토콜에 따른다. 해당 문서를 먼저 Read 해서 본인의 역할(①/②/③/④ 중 어느 단계인지) 을 확인한 뒤 작업하라.

---

## 개정 이력

- 2026-04-24 v1 — 초안 (원준님 지침: 품질 최우선·오류 0 목표)