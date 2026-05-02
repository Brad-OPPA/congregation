# Planner ③ 1차 재검수 — 260514 CBS 「훈」(=실제 lfb) 84-85장

> 재검수자: cbs-planner (③ 단계, 6단 방어 v2)
> 재검수일: 2026-05-02
> 대상 산출물: 6개 서브 (qa-designer · scripture-deep · publication-cross-ref · application-builder · experience-collector · illustration-finder)
> 검증 방식: 산출물 전체 Read + 핵심 검증 포인트 WOL 직접 fetch (curl)

---

## 전체 판정

**PASS** (meta.yaml 정정 2건 직접 적용 후)

6개 서브 모두 ② 자체 검수 PASS 상태로 산출. ③ 단계에서 추가로 발견된 cross-cutting 이슈 2건 (요 9:25 verbatim · publication symbol jy→lfb) 은 본 재검수가 직접 정정 — Edit 도구로 meta.yaml + outline.md 수정 완료. 서브 재호출 (NEEDS-RERUN) 불필요. 다음 단계 (④ cbs-script 작성) 로 진행 가능.

---

## 6축 결과

### A. 지시서 중점 범위·키워드 반영 — PASS

| 서브 | 지시서 핵심 | 실제 수집 | 판정 |
|------|------------|-----------|------|
| qa-designer | 6단 구조 (필수질문→답변→보강→삽화질문→배우는점→마지막질문) × 양 장 | 84장·85장 모두 6단 구조 그대로 / WOL 노란박스 (필수) 질문 verbatim (글자 단위 100% 일치 확인) / 후속 질문 5개 (84장 3 + 85장 2) + 삽화 질문 답변 + 마지막 질문 적용 3축 | PASS |
| scripture-deep | 핵심 4성구 (시 27:13, 마 22:29, 마 14:30, 요 9:25) 연구노트·통찰·원어·6+ 출처 | 4성구 × 1·2·3·4·5·6·7·8 섹션 완비 / 출처 6+ 모두 충족 / 원어 4-5단어 분석 / 직전 주차 대비 +40% 단조 증가 | PASS |
| publication-cross-ref | 84장 5 + 85장 5 키워드 횡단 검색 / 「통찰」·「파」·「예수」·「깨」·「하」 | 12편 인용 (84장 6 + 85장 6) / 「통」 4편 + 「파」 3편 + 단행본 3편 (jy·ia·cl) / 직전 주차 대비 12편 vs 3편 강한 단조 증가 / docid 14건 별도 검증 표 | PASS |
| application-builder | 4축 × 2-3 카드 / 자기점검 1-2 / scripture-deep 영역 외 보강 성구 / 정치·인물 거명 금지 | 9 카드 (가정 3 / 직장학교 2 / 회중 2 / 영성 2) / 자기점검 2 (Q1·Q2) / 보강 성구 빌 4:6-7 + 벧전 3:15 (scripture-deep 4성구와 중복 0) / 정치 0건 인물 0건 | PASS |
| experience-collector | 84장 (두려움 극복) + 85장 (압력 속 충성) 짧은 1-2분 분량 / 「파」 2018-2025 / 가명 정책 / 정치 박해 회피 | 7건 (84장 4 + 85장 3) / 파24·파22 + jw.org 러시아 뉴스 / 가명·실명 출판물 그대로 / 정치 박해 ⚠ 플래그 처리 (출판물 톤 그대로 유지 안내) | PASS |
| illustration-finder | 84장 시선 비유 + 85장 친절 두 단계 + 단순 증언 비유 각 2-3개 / 종교 도상·인물 거명·정치 비유 금지 | 6개 (장당 3) / 운전·평행봉·야간산행 (84장) + 의사재방문·법정증인·안전점검 (85장) / 일반 비유 표기 100% / 종교 도상 0 정치 0 인물 0 | PASS |

### B. 피해야 할 항목 미포함 — PASS

| 위반 가능 항목 | 검사 결과 |
|---------------|----------|
| 정치·국가 예시 | 0건 (러시아 박해 사례는 jw.org 공식 출판물 인용 한정 + 사회자 톤 조절 ⚠ 플래그) |
| 회중 특정 인물 거명 | 0건 (모든 사례 일반 상황·가명·실명 공개 출판물 한정) |
| 외국어판 인용 | 0건 (한국어 wol 직접 fetch 100%, 영문 NWT는 번역 비교 결만 언급) |
| 진화론 긍정·타 종교 교리 긍정 | 0건 |
| 본문 verbatim 재서술 (사회자 영역) | 0건 (qa-designer·application 모두 단락 번호·핵심 표현만 인용) |
| 공식 (필수) 연구 질문 재서술 | 0건 (verbatim 그대로) |
| 상투적 청중 호명 9개 표현 | 0건 (qa-designer 후속 질문 모두 "어디에 있다고 보십니까?" / "구체적 방법은 무엇이겠습니까?" 형태) |

### C. 각 _selfcheck PASS — PASS

| 서브 | _selfcheck 위치 | 자체 판정 | FAIL 항목 |
|------|----------------|----------|----------|
| qa-designer | research-qa/260514/_selfcheck.md | PASS | 0 (🔴 9항 모두 PASS·N·A) |
| scripture-deep | research-bible/260514/_selfcheck.md | PASS | 0 (🔴 9항 모두 PASS·N·A, 직전 +40% 단조) |
| publication-cross-ref | research-topic/260514/_selfcheck_cbs.md | PASS | 0 (🔴 9항 모두 PASS·N·A, verbatim phrase 11/11 재검) |
| application-builder | research-application/260514/cbs_selfcheck.md | PASS | 0 (4축×2-3 카드·자기점검 2·정치 0·인물 0 모두 충족) |
| experience-collector | research-experience/260514/cbs__selfcheck.md | PASS (3 플래그 명시) | 0 (정치 박해 ⚠·연감/JW방송 미수집·85B/C 한국어 URL 미확인) |
| illustration-finder | research-illustration/260514/cbs__selfcheck.md | PASS | 0 (🔴 8항 모두 PASS) |

### D. 2개 장 카테고리 균형 — PASS

| 카테고리 | 84장 | 85장 |
|---------|------|------|
| 필수 (필수) 질문 | 1 (verbatim 검증) | 1 (verbatim 검증) |
| 핵심 성구 심층 | 시 27:13 + 보강 마 14:30 | 마 22:29 + 보강 요 9:25 |
| 출판물 횡단 | 6편 (jy 53·44, ia 21, it-1 갈릴리바다, w19, w09) | 6편 (jy 71, it-1 바리새파, it-2 안식일, it-1 실로암, w07, cl 15) |
| 4축 적용 | 4-5 카드 + 자기점검 Q1 (시선) | 4-5 카드 + 자기점검 Q2 (두 단계 친절) |
| 경험담 | 4건 (희귀암·코로나·산불·가정 배신) | 3건 (활동금지·러시아 3형제·러시아 4명 2025) |
| 일상 비유 | 3 (운전·평행봉·야간산행) | 3 (의사재방문·법정증인·안전점검) |

균형 양호. 두 장 모두 6 카테고리 충족.

### E. 훈 책 docid 검증 — PASS (단, publication symbol 정정 필요)

- 1102016094 (84장) — WOL 직접 fetch 결과 HTML class="pub-lfb docClass-13" → 실제 publication = **lfb** (Learn From the Bible / 「내가 좋아하는 성경 이야기」 어린이용 그림 성경 이야기책)
- 1102016095 (85장) — 동일 패턴
- meta.yaml 의 `book_actual_publication_symbol: jy` 는 잘못된 값. 본 재검수에서 `lfb` 로 정정 (Issue 2 참조).

### F. 상호 모순 — 발견 후 정정 완료

**Issue 1 (요 9:25 verbatim)** + **Issue 2 (publication symbol)** 두 건 발견. 본 재검수가 meta.yaml + outline.md 직접 정정 (아래 "발견된 이슈와 결정" 참조).

---

## 발견된 이슈와 결정

### Issue 1: 요 9:25 verbatim 정정 (scripture-deep 보고)

- **결정**: meta.yaml 정정 (read_aloud:false 인 보강 성구이지만 verbatim 명시).
- **사유**: meta.yaml `instructions_to_subresearchers.scripture-deep` 의 본문 인용 ("한 가지 아는 것은, 제가 눈이 멀었었는데 지금은 본다는 것입니다") 은 paraphrase. 신세계역 연구판 verbatim (WOL nwtsty/43/9 직접 fetch 검증) 은 다음과 같이 다름:

  > "그러자 그가 말했다. '저는 그분이 죄인인지 아닌지는 모르겠습니다. 한 가지 분명히 아는 것은 제가 눈이 멀었었지만 지금은 볼 수 있다는 것입니다.'"

  cbs-script 가 본문 인용 시 paraphrase 채택하면 fact-checker (⑥ 단계) FAIL 가능. scripture-deep 의 정정 권장 채택.

- **정정 내역 (meta.yaml)**: `scripture_reads` 항의 요한복음 9:25 entry 에 `text_verbatim` + `note_verbatim` 두 키 추가. cbs-script 에게 verbatim 채택 의무 안내.

### Issue 2: publication symbol jy vs lfb (publication-cross-ref 보고)

- **결정**: 정본 = **`lfb`** (Learn From the Bible / 「내가 좋아하는 성경 이야기」). meta.yaml 의 `book_actual_publication_symbol: jy` 는 옛 회중 자료 (260205·260423·260507) 가 동일하게 잘못 표기해 온 값을 그대로 답습한 것.
- **검증 방식**: WOL `https://wol.jw.org/ko/wol/d/r8/lp-ko/1102016094` 직접 fetch → HTML `class="article ... pub-lfb docClass-13"` 명시. 동일 페이지가 어린이용 그림 성경 이야기책의 84장임을 확인. 「예수」 책 (jy) 의 동일 사건은 53·44·71 장 docid 1102014656·1102014647·1102014791 별도 존재 (publication-cross-ref §0 docid 검증 표 14건 모두 검증 완료).
- **회중 통칭 "훈"**: 책 표지·목차 표기는 어린이용 그림책으로 회중 내 별칭. 어른 회중 성서 연구에서 어린이용 본문을 사용하는 이유는 회중 내 결정·관행 (본 재검수 범위 외).
- **정정 내역**:
  1. **meta.yaml**:
     - `book_actual_publication_symbol`: `jy` → **`lfb`**
     - `book_actual_full`: "예수 — 길, 진리, 생명" → **"내가 좋아하는 성경 이야기 (Learn From the Bible)"**
     - 신규 키 `related_publication_symbol: jy` + `related_publication_full: "예수 — 길, 진리, 생명"` 추가 (횡단 자료 보존).
     - `note_on_book` 본문 — "publication 은 「예수」 책" → "publication = lfb. 동일 일화의 성인용 권위 해설은 jy 44·53·71 장에 별도 존재. 회중 통칭 + 실제 lfb + 횡단 자료 jy 세 층위 보존" 으로 재기술.
  2. **outline.md**:
     - "교재: 「훈」 ··· publication symbol = `jy`" → "publication symbol = `lfb` ※ 횡단 자료 = jy 44·53·71장"
     - §0 의 "⚠ docid 검증 결과" 박스 — 정정 일자·발견 경위·세 층위 보존 명시.
     - §9 "script 에게 전달할 종합 지시" 끝의 ⚠ 항 — "실제 publication symbol = jy" → "실제 publication symbol = lfb. 회중 호칭 + 실제 lfb + 횡단 권위 자원 jy 세 층위 다름을 인지하고 작업"
- **하위 영향**: 6 서브 산출물의 docid 자체는 모두 정확 (1102016094/095). 산출물 본문 안의 jy 표기는 그대로 두되 (각 서브가 의도적으로 횡단 jy 자료를 인용했음 — 옳음), cbs-script 단계에서 책 표지 호칭은 "훈" 또는 "「내가 좋아하는 성경 이야기」 84-85장" 으로, 횡단 인용은 "「예수」 책 44/53/71장 = jy" 로 분리 명시할 것.

### Issue 3: application 분량 (application-builder 자체 보고)

- **결정**: 분량 (4축 × 2-3 카드 = 9 카드) 그대로 유지. 단조 위반 아님으로 판정.
- **사유**: meta.yaml `instructions_to_subresearchers.application-builder` 가 명시적으로 "각 축 2-3 카드" 로 분량을 한정. 이는 사용자(planner) 의 직접 분량 제어. 직전 baseline (260430) 의 4축 × 5 = 20 카드 케이스와 비교해 단순 수치 감소가 발생하나, 그 baseline 케이스는 사용자 지시가 4축×5 였던 다른 운영 패턴. 본 호출의 9 카드 = 사용자 직접 제어. quality-monotonic-checker (⑥ 단계) 에서 "사용자 직접 분량 제한 케이스" 로 분류해 단조 평가 면제 권장. application-builder _selfcheck.md §4 가 baseline 비교 + 출처 정밀도·구조 동등 이상 입증 (URL 6/[확인 필요] 0, 보강 성구 신규 도입, 행동 구체성 향상, 자기점검 별도 §섹션 분리) → 밀도·구조 단조 PASS.
- **추가 조치**: 없음. application-builder 자체가 ④ Script 작성 시 cbs-script 에게 "정죄·협박형 표현 회피·심화 카드 0 의도적" 도 함께 전달하므로 톤 부조화 위험 없음.

---

## 통과 항목 요약

1. **WOL verbatim 정합성** — qa-designer 의 (필수) 연구 질문 84장·85장 모두 글자 단위 100% 일치 (curl 직접 검증). 핵심 성구 시 27:13 / 마 22:29 / 마 14:30 / 요 9:25 verbatim scripture-deep 산출물에서 신세계역 연구판 fetch 후 그대로 채택.
2. **단조 증가 (양 축)** — scripture-deep +40% (643→899줄) / publication-cross-ref +400% (3→12편) / experience-collector A등급 5→6건. 모두 직전 주차(260430) 대비 PASS.
3. **adjacent quality** — application-builder 보강 성구 (빌 4:6-7 / 벧전 3:15) 가 scripture-deep 4성구 (시 27:13·마 22:29·마 14:30·요 9:25) 와 중복 0. 자료 분배 깔끔.
4. **카테고리·층위 분리** — 84장(시선·두려움)·85장(친절 두 단계·압력 속 단순 증언) 두 축이 모든 서브에서 일관되게 짝을 이룸. cbs-script 가 두 블록 (4'~15' / 15'~28') 으로 갈라 진행할 때 각 블록 내부의 6단 구조 (필수질문→답변→보강→삽화질문→배우는점→마지막질문) 자료 모두 충족.
5. **상투 호명·정치·인물·종교 도상·진화론·외국어판** — 6 서브 전부 0건. ⑥ jw-style-checker 에서 추가 위반 발견 가능성 낮음.
6. **🟢🔴 블록 의무** — 6 서브 _selfcheck 모두 🔴 9항 표 (또는 동등) 작성, FAIL 0건. (qa-designer · experience-collector 84장 파일 · illustration-finder 의 Q&A 문서 자체에는 🟢 착수 블록 직접 복사. scripture-deep · publication-cross-ref 는 "조사 대시보드" 블록으로 동등 구현.)

---

## NEEDS-RERUN 시 재지시

**N/A** — 본 재검수에서 발견된 이슈 2건은 모두 meta.yaml + outline.md 직접 정정으로 해결. 6 서브 산출물 자체는 그대로 유지 가능. 서브 재호출 불필요.

---

## ⑤ 단계 (Planner 2차 재검수) 를 위한 인계 메모

1. **요 9:25 verbatim 채택 의무** — cbs-script 가 본 절을 사회자 인용 또는 본문 인용으로 사용할 경우, meta.yaml 의 새 `text_verbatim` 키 또는 scripture-deep `gem-04-jn-9-25.md` §1-1 의 verbatim 그대로 사용해야 함. paraphrase 채택 시 ⑤ NEEDS-FIX 강제.
2. **publication symbol 표기** — cbs-script 가 책 호칭을 다음 패턴으로 사용:
   - 전면 호칭: "「훈」" (회중 통칭) 또는 "「내가 좋아하는 성경 이야기」 84-85장"
   - 횡단 인용 시: "「예수」 책 44/53/71장" (jy 영역) 으로 분리 명시. lfb 와 jy 를 같은 책으로 묶지 말 것.
3. **러시아 박해 사례 (85-B / 85-C)** — cbs-script 사용 시 jw.org 공식 출판물 표현 그대로. "정권 비판"·"정치 비교" 0건 유지. 한국어 URL 미확인 ⚠ 플래그는 ⑥ fact-checker 가 wol.jw.org/ko 한국어판 재검색 후 동일 한국어 보도 발견 시 URL 보강.
4. **빌 4:6-7 / 벧전 3:15 verbatim** — application-builder 가 절 참조만 표기 (WOL fetch timeout 으로 verbatim 미확인). cbs-script 가 본 두 절을 사회자 낭독·인용으로 사용할 경우 신세계역 연구용 nwtsty 직접 fetch 후 verbatim 사용. ⑥ fact-checker 도 한 번 더 확인.

---

**다음 단계**: ④ cbs-script 호출 (산출물 = 본 폴더의 `script.md`). cbs-script 는 본 _planner_review.md + outline.md + meta.yaml + 6 서브 산출물을 모두 Read 하여 30분 사회 진행 대본 작성.

---

작성: 2026-05-02 by cbs-planner (③ 단계, 6단 방어 v2)
