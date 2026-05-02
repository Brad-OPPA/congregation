# Planner ③ 1차 재검수 — 260521 CBS

> 6단 방어(v2) ③ 단계 — Planner 재검수 모드
> 대상: 6 보조 에이전트 산출물 (qa·scripture·topic·application·experience·illustration)
> 검수자: cbs-planner (재호출)
> 검수일: 2026-05-02
> 검수 범위: `.claude/shared/multi-layer-defense.md` ③ 단계 표준 절차

---

## 전체 판정: **PASS** (이슈 정정 후)

> 6 보조 산출물 모두 ② 단계 자체 검수 PASS 상태로 인계됨. ③ 단계 추가 점검 결과 — 핵심
> 발견 이슈 1건 (jy 챕터 정정) 은 메타·outline 직접 정정 완료. 경험담 익명화 권장은
> meta.yaml 노트 추가 + cbs-script ④ 단계에서 적용. 6 보조 모두 cbs-script ④ 단계 인계 가능.

---

## 6축 결과

### A. 지시서 중점 범위·키워드 반영 — **PASS**

각 보조 에이전트 산출물이 meta.yaml `instructions_to_subresearchers` 의 지시서를 정확히 따랐다.

| 보조 | 지시 핵심 | 충족 |
|---|---|---|
| qa-designer | 6단 구조 (필수 질문→답변→보강→삽화→배우는 점→마지막) × 86장+87장 + 13부 90초 한도 | ✅ |
| scripture-deep | 핵심 2 (시 68:20·눅 12:32) + 보강 2 (요 11:25·요 13:34-35) verbatim·원어·교차 참조 | ✅ |
| publication-cross-ref | 86장·13부·87장 각 5-8개 횡단 인용 + jy 챕터 docid 검증 | ✅ (오히려 meta.yaml 초안 정정) |
| application-builder | 4축 (가정·직장학교·회중·개인영성) × 11 적용점 + 자기점검 3개 | ✅ |
| experience-collector | 86장·87장 각 2-3건 공식 출판물 경험담 | ✅ (6건) |
| illustration-finder | 86장·13부·87장 각 비유 후보 2-3개 + 8필터 통과 | ✅ (8개) |

### B. 피해야 할 항목 (정치·국가·외국어·종교 도상·회중 인물) — **PASS**

| 8필터 | 위반 |
|---|---|
| 정치·국가 직접 언급 | 0건 (아르템 경험담 → "어떤 형제 수감" 일반화 명시) |
| 외국어판 인용 | 0건 (모두 wol.jw.org/ko) |
| 종교 도상 (다른 종교 상징) | 0건 (87장 비유에서 "국기" 회피, 결혼반지 단일) |
| 회중 특정 인물 거명 | 0건 |
| 자살·자해 자극적 묘사 | 0건 |
| 화체설 직접 비판 | 회피 (헬라어 *에스틴* 분석으로만) |
| 학자·기관 권위화 | 회피 (여호와 말씀 정확성 틀로만) |
| 9가지 상투적 청중 호명 | 0건 (qa-designer grep 검증) |

### C. 각 _selfcheck PASS — **PASS**

| 보조 | _selfcheck 파일 | 자체 판정 |
|---|---|---|
| qa-designer | research-qa/260521/_selfcheck.md | ✅ PASS |
| scripture-deep | research-bible/260521/_selfcheck_cbs.md | ✅ PASS |
| publication-cross-ref | research-topic/260521/_selfcheck_cbs.md | ✅ PASS |
| application-builder | research-application/260521/cbs_selfcheck.md | ✅ PASS |
| experience-collector | research-experience/260521/cbs__selfcheck.md | ✅ PASS |
| illustration-finder | research-illustration/260521/cbs__selfcheck.md | ✅ PASS |

🔴 종료 블록 부착 의무 6/6 충족.

### D. 3-부분 (86장 / 13부 소개 / 87장) 카테고리 균형 — **PASS**

| 카테고리 | 86장 | 13부 소개 | 87장 |
|---|---|---|---|
| 필수 연구 질문 (qa) | ✅ 1 (verbatim) | — (없음, 90초 도입형) | ✅ 1 (verbatim) |
| 핵심 성구 (scripture) | ✅ 시 68:20 + 요 11:25 보강 | — (별도 성구 없음) | ✅ 눅 12:32 + 요 13:34-35 보강 |
| 횡단 출판물 (topic) | ✅ 8건 | ✅ 5건 | ✅ 8건 |
| 적용 카드 (application) | ✅ 4 | ✅ 1+α | ✅ 6 |
| 경험담 (experience) | ✅ 3건 | — (없음, 87장 cbs_87_sue 1줄 인용 권장) | ✅ 3건 |
| 예화·비유 (illustration) | ✅ 3 | ✅ 2 | ✅ 3 |

⚠ 13부 소개에 경험담·핵심성구는 의도적으로 비움 (90초 한도). qa-designer 가 13부 소개에
사회자 단독 멘트로 처리하도록 설계 — 정합.

### E. docid 1102016XXX (lfb) 검증 + jy 1102014XXX 분리 — **PASS (정정 완료)**

| 항목 | 초안 (meta.yaml v1) | 검증 후 정정 |
|---|---|---|
| 「훈」 86장 | 1102016096 | ✅ 정확 |
| 「훈」 13부 소개 | 1102016143 | ✅ 정확 |
| 「훈」 87장 | 1102016097 | ✅ 정확 |
| 「예수」 책 — 나사로 부활 | "90장 [확인 필요]" | **정정**: jy 제90장 (1102014690) + 제91장 (1102014691, 214-215면) 두 챕터 |
| 「예수」 책 — 주의 만찬 | "121장 [확인 필요]" | **정정**: jy **제117장** (1102014717) — 121장은 "용기를 내십시오" (요 16장) 다른 일화 |

publication-cross-ref WOL fetch (curl HTTP 200 + `<title>` 검증) 결과로 정정. WOL 직접 검증
(2026-05-02 by Planner 재검수): jy 117 = "주의 만찬" / jy 90 = "「부활이며 생명입니다」" /
jy 91 = "나사로가 부활되다" / jy 121 = "용기를 내십시오! 내가 세상을 이겼습니다" — 모두 일치.

### F. 상호 모순 — **PASS** (1건 정정으로 해소)

| 모순 후보 | 발견 위치 | 해소 |
|---|---|---|
| jy 챕터 (90/121 vs 90+91/117) | meta.yaml note + outline §0/§7-§8 + cbs-apply.md §7 | ✅ 정정 완료 (meta.yaml + outline.md 2곳 + cbs-apply.md 1곳) |
| 보강 성구 영역 중복 (scripture-deep vs application-builder) | scripture-deep = 시 68:20/눅 12:32/요 11:25/요 13:34-35; application = 살전 4:13-14/빌 2:3-4 | ✅ 영역 분리 정합 |
| 13부 90초 한도 다중 보조 분량 | qa·application·illustration 모두 90초 한도 명시 | ✅ 정합 |

---

## 발견된 이슈와 결정

### Issue 1: jy 챕터 정정 (주의 만찬 = 117장 / 나사로 = 90+91장 두 챕터)

- **발견**: publication-cross-ref 가 WOL fetch (curl HTTP 200 + 챕터 헤더 직접 확인) 로 meta.yaml
  초안의 "jy 90장 (단일) / jy 121장" 추정 정정.
- **검증**: Planner 재검수에서 WOL 직접 fetch 재확인 — jy 117 "주의 만찬" / jy 90 "부활이며
  생명입니다" / jy 91 "나사로가 부활되다" / jy 121 "용기를 내십시오! 내가 세상을 이겼습니다"
  (요한 16장 끝, 87장 본문과 직접 매칭 X).
- **결정**: meta.yaml + outline.md + cbs-apply.md 3곳 직접 정정 완료.
- **사유**: 부정확한 docid 인용은 cbs-script 단계에서 fact-checker 게이트 HIGH 위반 (URL
  실존 검증 실패) 가능. ③ 단계에서 정정해 ⑥ 게이트 부담 감소.
- **정정 적용 위치**:
  1. `meta.yaml` `note_on_book` 블록 — jy 90+91 / jy 117 명시 + 121장 정정 사유
  2. `outline.md` §2 86장 교차 참조 — 1102014690/691 docid 명시
  3. `outline.md` §2 87장 교차 참조 — 1102014717 docid 명시 + 121장 정정 사유 + 보조 jy
     118/120/122 추가
  4. `outline.md` §8 참고 출처 — 동일 정정 적용
  5. `research-application/260521/cbs-apply.md` §7 교차 참고 — 117장 정정 명시

### Issue 2: 경험담 익명화 권장 (cbs_86_matthew + cbs_87_artem)

- **발견**: experience-collector 자체 검수에서 이미 명시 — cbs_86_matthew (7세 아동) 실명 →
  "한 소년" 익명화 / cbs_87_artem 정치 박해 회피 → "어떤 형제가 수감 중에…" 일반화.
- **결정**: meta.yaml `note_on_book` 끝부분에 ⚠ 경험담 익명화 노트 추가 — cbs-script ④ 단계에서
  자동 적용되도록 명시. 별도 파일 정정은 보류 (script ④ 단계 책임).
- **사유**: 산출물 자체는 출판물 verbatim 유지 (검증 추적성). script 단계에서 회중 자료에
  표기 시점에 익명화 적용이 정책 표준.
- **적용 위치**: `meta.yaml` `note_on_book` 끝 ⚠ 노트 추가 완료.

### Issue 3: WOL fetch 일부 timeout (qa-designer 보고)

- **발견**: qa-designer 가 WOL 일부 fetch 타임아웃을 meta.yaml verbatim 의존으로 처리 보고.
- **검증 결과**: scripture-deep 가 4편 모두 nwtsty + dx + bc URL 17건 직접 fetch verbatim
  검증 완료. publication-cross-ref 가 16 docid 모두 curl HTTP 200 + 본문 일치 검증 완료.
  핵심 본문 (86장·13부·87장 + 필수 질문 + 핵심 성구 + 13부 핵심 교훈 3개) 8건 모두 verbatim
  일치 — meta.yaml verbatim 신뢰성 확보.
- **결정**: 보강 불필요. cbs-script ④ 단계는 meta.yaml + scripture-deep + publication-cross-ref
  3중 검증된 verbatim 만 사용하도록 한다.
- **사유**: 추가 fetch 시도는 timeout 재발 위험. 현재 verbatim 검증 충분.

### Issue 4: scripture-deep 보강 성구 verbatim 검증 완료

- **발견**: scripture-deep 가 meta.yaml 의 보강 성구 4편 (시 68:20·눅 12:32·요 11:25·요 13:34-35)
  의 nwtsty verbatim + 17 URL 직접 fetch 검증 완료 보고.
- **결정**: 추가 검증 불필요. cbs-script 가 이 4편을 그대로 인용 가능. application-builder 의
  보강 성구 (살전 4:13-14·빌 2:3-4) 는 절 참조만 — fact-checker (⑥ 단계) 가 1회 verbatim
  확인 권장 (cbs_selfcheck.md §3 명시).

---

## 통과 항목 요약

| 통과 검증 | 결과 |
|---|---|
| 6 보조 산출물 모두 ② 단계 자체 검수 PASS | ✅ |
| 🟢 착수 블록 + 🔴 종료 블록 부착 6/6 | ✅ |
| qa-designer 필수 연구 질문 verbatim 일치 (86장·87장 2/2) | ✅ |
| scripture-deep verbatim + 17 URL fetch 검증 | ✅ |
| publication-cross-ref 16 docid HTTP 200 검증 | ✅ |
| publication symbol 분리 (lfb 1102016XXX vs jy 1102014XXX) | ✅ |
| jy 챕터 정정 (90+91·117) 메타·outline·cbs-apply 3곳 동기화 | ✅ |
| 시간 마커 8개 (4·7·10·15·18·21·23·29) 일치 | ✅ |
| 30분 (1800초) ±60초 시간 분배 가능성 | ✅ |
| 13부 소개 90초 한도 일관 준수 (qa·application·illustration) | ✅ |
| 외부 14축 결합 ≥ 2 (cbs 차등 적용표 임계) | ✅ (4축 — 베다니 지형·1세기 매장 풍습·헬라어 카이노스·해석학 에스틴) |
| 출판물「」 ≥ 3 (cbs 차등 적용표 임계) | ✅ (16개 unique 횡단 인용) |
| 4축 적용 균형 (가정·직장학교·회중·개인영성) | ✅ (3+3+3+2 = 11) |
| 9가지 상투적 청중 호명 회피 | ✅ (qa grep 0건) |
| 정치·국가·종교 도상·회중 인물 거명 회피 | ✅ |
| 본문 verbatim 재서술·공식 질문 verbatim 재서술 회피 | ✅ |
| 경험담 4 요소 (출판물·호수·면·URL) 완비 6/6 | ✅ |
| 경험담 익명화·일반화 메타 노트 추가 | ✅ (meta.yaml ⚠ 블록) |
| 비유 후보 8필터 통과 (8/8) | ✅ |
| 할루시네이션 0건 | ✅ |

---

## cbs-script ④ 단계 인계 메모

### 우선 적용 사항

1. **jy 챕터 인용**: 횡단 인용 시 「예수」 책 **제117장** (주의 만찬) / 제90장+제91장 (나사로
   부활) docid 1102014717 / 1102014690 / 1102014691 정확 표기. 121장 절대 인용 금지.
2. **경험담 익명화**: cbs_86_matthew → "한 소년" / cbs_87_artem → "어떤 형제가 수감 중에…"
   국가명 미명시. 출처 표기는 「파수대」 호수만 명시 (각주에 인물 가명 처리).
3. **시간 마커 8개**: `4'·7'·10'·15'·18'·21'·23'·29'` 빨강 볼드 우측정렬.
4. **(필수) 연구 질문**: 빨강 라벨 "(필수) 연구 질문" + 노랑 하이라이트 + 검정 볼드.
5. **핵심 성구**: 파란색 #2F5496 (시 68:20 / 눅 12:32).
6. **publication symbol 분리**: 전면 = 「훈」 86장 / 「훈」 13부 소개 / 「훈」 87장 (lfb
   1102016XXX) / 횡단 = 「예수」 책 NN장 (jy 1102014XXX) — 절대 혼동 금지.
7. **30분 (1800초) ±60초** — quality > timing 정책. timing FAIL 이라도 quality PASS 면 통과.

### 권장 시간 매핑 (qa-designer + illustration-finder 매핑 표 참조)

| 시간 | 블록 | 1순위 활용 |
|---|---|---|
| 0~1' | 사회자 오프닝 | — |
| 1'~4' | 86장 5단락 낭독 | 낭독자 |
| 4'~7' | 86장 (필수)Q + 답변 + 보강 | qa §1.2 + 비유 후보 1 (마취 회복 호명) + 1세기 매장 풍습 |
| 7'~10' | 86장 핵심 성구·삽화·마지막Q | 시 68:20 + 요 11:25 보강 + 비유 후보 2 (부모의 깨움) + 경험담 cbs_86_emma_arnold 1건 |
| 10'~11'30" | 13부 소개 90초 | qa §2 + 비유 후보 1 (책의 마지막 부 진입) |
| 11'30"~15' | 87장 5단락 낭독 | 낭독자 |
| 15'~18' | 87장 (필수)Q + 답변 + 보강 | qa §3.2 + 비유 후보 1 (한 해 한 번 가족 기념일) |
| 18'~21' | 87장 핵심 성구·확장Q | 눅 12:32 + 비유 후보 3 (장학금 적은 무리) + 경험담 cbs_87_monica |
| 21'~23' | 87장 삽화 | 비유 후보 2 (결혼반지 상징) |
| 23'~29' | 87장 마지막Q + 3축 + 경험담 + 결론 | application 3축 + 요 13:34-35 보강 + 경험담 cbs_87_artem (일반화) |
| 29'~30' | 복습·맺음말 | qa §4 |

### 보강 성구 verbatim 확인 (fact-checker ⑥ 단계 권장)

- 살전 4:13-14 (86장 적용 보강) — application-builder 절 참조만 처리. fact-checker 가 nwtsty
  verbatim 1회 확인.
- 빌 2:3-4 (87장 적용 보강) — 동일.

---

## NEEDS-RERUN 시 재지시 (해당 없음)

본 ③ 단계 검수 결과 **PASS** — NEEDS-RERUN 0건. 모든 보조 산출물이 cbs-script ④ 단계 인계
가능 상태. jy 챕터 정정·경험담 익명화 노트 추가는 ③ 단계에서 직접 처리 완료.

---

## 6단 방어(v2) 진행 상태

- ✅ ① Planner 착수 전 방향 지침 (meta.yaml `instructions_to_subresearchers` 6건)
- ✅ ② 서브 에이전트 자체 검수 (6/6 _selfcheck PASS)
- ✅ **③ Planner 1차 재검수 (본 _planner_review.md — PASS)**
- ⏳ ④ Script 작성 + 자체 검수 (대기)
- ⏳ ⑤ Planner 2차 재검수 (대기)
- ⏳ ⑥ 4종 게이트 (fact·jw-style·timing·quality-monotonic) (대기)

---

🔴 종료 블록 — Planner ③ 1차 재검수 종료. cbs-script ④ 단계로 인계.
