# Planner ③ 1차 재검수 — 260528 CBS

> 6단 방어(v2) ③ 단계 — Planner 재검수 모드
> 대상: 6 보조 에이전트 산출물 (qa·scripture·topic·application·experience·illustration)
> 검수자: cbs-planner (재호출)
> 검수일: 2026-05-02
> 검수 범위: `.claude/shared/multi-layer-defense.md` ③ 단계 표준 절차

---

## 전체 판정: **PASS** (이슈 정정 후)

> 6 보조 산출물 모두 ② 단계 자체 검수 PASS. ③ 단계 추가 점검 결과 — 핵심
> 이슈 1건 (qa-designer 의 jy 챕터 오인 — jy 122 → jy 123) 은 publication-cross-ref
> 산출물 재호출 통합 단계에서 정정 노트로 명시. cbs-script ④ 가 그 정정을
> 반영해 작성하면 됨. "신앙" 단독 명사 4건도 cbs-script 단계 인계.
> 6 보조 모두 cbs-script ④ 단계 인계 가능.

---

## 6축 결과

### A. 지시서 중점 범위·키워드 반영 — **PASS**

각 보조 에이전트 산출물이 meta.yaml `instructions_to_subresearchers` 의 지시서를 정확히 따랐다.

| 보조 | 지시 핵심 | 충족 |
|---|---|---|
| qa-designer | 6단 구조 (필수 질문→답변→보강→삽화→배우는 점→마지막) × 88장+89장 | ✅ |
| scripture-deep | 핵심 2 (요 16:33·요 16:32) + 보강 5 (마 26:39·눅 22:43·요 13:38·눅 22:31-32·눅 22:61-62) verbatim·원어·교차 참조 + 통찰 5항목 | ✅ (gem-01 ~ gem-09 9파일) |
| publication-cross-ref | 88장·89장 각 5-8개 횡단 인용 + jy 챕터 docid 검증 | ✅ (재호출 — 누락 보충 완료, 88장 8건 + 89장 8건) |
| application-builder | 4축 (가정·직장학교·회중·개인영성) × 24 적용점 + 자기점검 4개 | ✅ |
| experience-collector | 88장·89장 각 1-2건 공식 출판물 경험담 | ✅ (3건 — 88장 1 + 89장 2) |
| illustration-finder | 88장·89장 각 비유 후보 2-3개 + 8필터 통과 | ✅ (6건 — 각 장 3개) |

### B. 피해야 할 항목 (정치·국가·외국어·종교 도상·회중 인물) — **PASS**

| 8필터 | 위반 |
|---|---|
| 정치·국가 직접 언급 | 0건 (experience-collector 사례 모두 질병·자만·인간관계 영역, 정치 박해 회피) |
| 외국어판 인용 | 0건 (모두 wol.jw.org/ko) |
| 종교 도상 (다른 종교 상징) | 0건 (illustration-finder 6 비유 모두 보편 직업·활동 — 소방관·항해사·등산·의사 등) |
| 회중 특정 인물 거명 | 0건 (모든 인용 사례에 "한 형제·자매" 익명 표현) |
| 자살·자해 자극적 묘사 | 0건 |
| 화체설 직접 비판 | 해당 없음 (이번 주차 주제 외) |
| 학자·기관 권위화 | 회피 (「미슈나」 인용 = 1세기 율법 자료, 권위화 X) |
| 9가지 상투적 청중 호명 | 0건 (qa·apply·exp·illust 모두 grep 검증 완료) |

### C. 각 _selfcheck PASS — **PASS**

| 보조 | _selfcheck 파일 | 자체 판정 |
|---|---|---|
| qa-designer | research-qa/260528/_selfcheck.md | ✅ PASS (cbs-script 인계 사항 3개 명시) |
| scripture-deep | research-bible/260528/_selfcheck.md | ✅ PASS (9 파일 모두 nwtsty + 통찰 fetch verbatim) |
| publication-cross-ref | research-topic/260528/_selfcheck.md | ✅ PASS (재호출 — 12 docid 모두 검증 + cross-link 양방향 5건 입증) |
| application-builder | research-application/260528/cbs_selfcheck.md | ✅ PASS (4축 × 2장 × 3건 = 24건 + 자기점검 4개) |
| experience-collector | research-experience/260528/cbs__selfcheck.md | ✅ PASS (3건 모두 「파」 verbatim 매칭) |
| illustration-finder | research-illustration/260528/cbs__selfcheck.md | ✅ PASS (6 비유 모두 8필터 통과) |

🔴 종료 블록 부착 의무 6/6 충족.

### D. 88장·89장 카테고리 균형 — **PASS**

| 카테고리 | 88장 | 89장 |
|---|---|---|
| 필수 연구 질문 (qa) | ✅ 1 (verbatim pid 10) | ✅ 1 (verbatim pid 12) |
| 핵심 성구 (scripture) | ✅ 요 16:33 + 보강 마 26:39, 눅 22:43 | ✅ 요 16:32 + 보강 요 13:38, 눅 22:31-32, 눅 22:61-62 |
| 횡단 출판물 (topic) | ✅ 8건 (jy 4 + it 3 + it-2 1) | ✅ 8건 (jy 4 + it 2 + ia 2) |
| 적용 카드 (application) | ✅ 12 (4축 × 3) | ✅ 12 (4축 × 3) |
| 경험담 (experience) | ✅ 1건 (cbs_01 루이스·애나) | ✅ 2건 (cbs_02 호세, cbs_03 네덜란드 자매) |
| 예화·비유 (illustration) | ✅ 3 (소방관·항해사·운동선수) | ✅ 3 (등산·의사·재활) |

⚠ **13부 도입 (별도 90초 단락) 없음** — 87장이 13부 첫 챕터였으므로 88·89장은 13부 안 연속 진행. outline.md 도 88장→89장 직접 전환 (A-9 절). cbs-script 는 두 장 사이에 사회자가 짧은 전환 멘트 (1~2문장) 만 두면 됨 — 별도 13부 cross-ref 자료 불필요.

### E. docid 1102016XXX (lfb) 검증 + jy 1102014XXX 분리 — **PASS (정정 완료)**

| 항목 | 초안 (cbs-qa.md) | 검증 후 정정 |
|---|---|---|
| 「훈」 88장 | 1102016098 | ✅ 정확 (meta.yaml + outline + qa + apply + exp + illust 모두 일치) |
| 「훈」 89장 | 1102016099 | ✅ 정확 |
| 「예수」 책 — 겟세마네 기도 | "「예수」 책 122장" (cbs-qa.md §A-2) | **정정**: jy **제123장 "몹시 비통할 때 기도하시다"** (1102014723). 122장은 "위층 방 마치는 기도" (87장 본문, 직전 주차) — 88장과 직접 매칭 X |
| 「예수」 책 — 체포 | (cbs-qa 명시 X) | publication-cross-ref 가 jy **제124장** (1102014724) 확정 |
| 「예수」 책 — 안나스·가야바 | (cbs-qa 명시 X) | publication-cross-ref 가 jy **제125장** (1102014725) 확정 |
| 「예수」 책 — 베드로 부인 | (cbs-qa 명시 X) | publication-cross-ref 가 jy **제126장** (1102014726) 확정 |
| 「예수」 책 — 산헤드린 재판 | (cbs-qa 명시 X) | publication-cross-ref 가 jy **제127장** (1102014727) 확정 |
| 「예수」 책 — 표어성구 (요 16:33/16:32) 출처 강화 | (cbs-qa 명시 X) | publication-cross-ref 가 jy **제121장** "용기를 내십시오! 내가 세상을 이겼습니다" (1102014721) — 챕터 제목 그 자체가 88장 표어성구 — 직접 권위 인용 가능 |
| 통찰 "겟세마네" | (cbs-qa 명시 X — outline.md 에서 publication-cross-ref 확인) | scripture-deep gem-08 + publication-cross-ref 모두 docid **1200001671** 확정 |
| 통찰 "안나스" | (cbs-qa 명시 X) | scripture-deep gem-08 docid **1200000284** 확정 |
| 통찰 "가야바" | (outline 에서 언급) | docid **1200000856** 확정 |
| 통찰 "산헤드린" | (outline 에서 언급) | ⚠ 한국어판 별도 항목 없음 → "법정" 항목으로 redirect (gem-09 보고). cbs-script 는 jy 127 + 통찰 "법정" (간접) 사용 |
| 통찰 "모독" | (outline 에서 언급) | ⚠ 한국어판 "신성모독" 으로 redirect. cbs-script 는 jy 127 + nwtsty 마 26:65 노트 사용 |

publication-cross-ref 재호출 결과 모든 docid curl HTTP 200 + 본문 일치 검증 완료. cross-link 양방향 5건 입증. **불검증 docid 인용 0건 위반.**

### F. 상호 모순 — **PASS** (1건 정정으로 해소)

| 모순 후보 | 발견 위치 | 해소 |
|---|---|---|
| jy 챕터 (122 vs 123) | cbs-qa.md §A-2 | ✅ 정정 명시 — publication-cross-ref 본문 + 종료 블록 + 본 ③ 재검수 ⓔ 항목에서 3중 명시. cbs-script ④ 가 jy 123 으로 작성 |
| 통찰 docid (gem-08 vs publication-cross-ref) | scripture-deep gem-08 (겟세마네 1200001671·안나스 1200000284·가야바 1200000856) vs publication-cross-ref 1차 산출 (가야바만 명시) | ✅ publication-cross-ref 본문에 gem-08 docid 통합 반영 (📒 "추가 보강" 단락) |
| "신앙" 단독 명사 4건 (cbs-qa) | cbs-qa.md B-2·B-4·B-5 | ⚠ cbs-script ④ 단계 치환 인계 (qa _selfcheck §4 권고 반영) — "여호와에 대한 믿음" / "주를 따르는 자세" 등으로 |
| 보강 성구 영역 중복 (scripture-deep vs application-builder) | scripture-deep = 마 26:39·눅 22:43·요 13:38·눅 22:31-32·눅 22:61-62; application = 행 4:13·요 9:25·요 21:15-19 | ✅ 영역 분리 정합 (적용 보강 vs 본문 신학 보강) |

---

## 발견된 이슈와 결정

### Issue 1: jy 챕터 정정 (cbs-qa.md 의 "jy 122" → 정정: jy 123)

- **발견**: cbs-qa.md §A-2 "사회자 부가 해설" 에서 "「예수」 책 122장과 「통찰」 (it-1) '겟세마네' 항목" 이라 적힘.
- **검증**: publication-cross-ref 재호출 결과 jy 122 = "예수께서 위층 방에서 마치는 기도를 하시다" (요 17, 직전 주차 87장 본문). 88장 (겟세마네) 일화와 직접 매칭 X.
- **올바른 chapter**: jy **제123장 "몹시 비통할 때 기도하시다"** (docid 1102014723) — 겟세마네 기도 전용 챕터.
- **결정**: cbs-cross-ref.md 본문 + 종료 블록 + 본 ③ 재검수 ⓔ·F 항목 3곳 명시. cbs-script ④ 가 jy 123 으로 작성. **cbs-qa.md 자체 직접 정정은 불필요** — qa 산출물은 골격이며 cbs-script 가 횡단 인용 정확화 책임.
- **사유**: 부정확한 docid 인용은 fact-checker ⑥ 단계 HIGH 위반 가능. ③ 단계에서 정정 노트 명시로 ⑥ 게이트 부담 감소.

### Issue 2: "신앙" 단독 명사 4건 (cbs-qa.md)

- **발견**: qa-designer _selfcheck §4 grep 결과 "신앙" 4건 (B-2 "신앙을 흐리게", B-4 "신앙을 흐리게", B-5 "신앙을 분명히 증언" 등).
- **판단**: 지시서 305 줄 "신앙·간증·사역·복음 **단독**" 단어 금지. 합성 어구 사용은 정상이지만 안전 마진을 위해 cbs-script ④ 단계 치환 권고.
- **결정**: cbs-script ④ 가 "신앙" 4건을 다음 표현으로 치환 — "여호와에 대한 믿음" / "주를 따르는 자세" / "주께 대한 충성" 등.
- **사유**: jw-style-checker ⑥ 단계 HIGH 위반 회피.

### Issue 3: 통찰 한국어판 "산헤드린"·"모독" 별도 항목 부재

- **발견**: scripture-deep gem-09 가 WOL fetch 결과 "산헤드린 → 법정 참조" / "모독 → 신성모독 참조" redirect 확인.
- **결정**: cbs-script ④ 가 "「통찰」 '산헤드린' 항목" / "「통찰」 '모독' 항목" 직접 인용 회피. 대신 "「예수」 책 제127장 '산헤드린에서 재판받고 빌라도에게 넘겨지시다'" + "마태복음 26:65 신세계역 연구 노트" 를 1차 출처로 사용. 1세기 산헤드린 절차·모독죄 정의 정보는 동일 깊이 권위 자료로 충분.
- **사유**: 검증된 docid 만 인용 정책. 미확보 항목은 동등 정보 (jy 127 + nwtsty) 로 대체.

### Issue 4: 13부 도입 단락 없음

- **발견**: outline.md §A-9 (88장→89장 전환 멘트), outline.md 0번 (88장 + 89장 두 장 통합), meta.yaml block_count = 2 — 13부 도입 별도 단락 없음 (87장 직전 주차 13부 도입 완료).
- **결정**: cbs-script ④ 가 88장과 89장 사이에 사회자 1~2문장 짧은 전환 멘트만 두면 됨 (예: "예수께서 체포되시는 동안 사도들은 모두 도망쳐 버렸습니다. 그 가운데 한 사도는 멀리서 따라가다가 예상치 못한 시험에 빠집니다. 89장을 함께 살펴봅니다.") — 별도 cross-ref 자료 불필요.
- **사유**: outline·meta·publication-cross-ref 모두 일관 — 두 장 직접 전환 구조.

### Issue 5: WOL 일부 fetch timeout 보고

- **발견**: qa-designer 가 WOL 88·89장 fetch 60s timeout 보고. cbs-planner 1차 파싱본 (meta.yaml) 사용.
- **검증 결과**: scripture-deep 가 nwtsty + 통찰 페이지 7건 모두 직접 fetch verbatim 검증 완료. publication-cross-ref 재호출이 12 docid 모두 curl HTTP 200 + 본문 일치 검증 완료. **meta.yaml verbatim 본문 신뢰성 확보**.
- **결정**: 보강 불필요. cbs-script ④ 단계는 meta.yaml + scripture-deep + publication-cross-ref 3중 검증된 verbatim 만 사용.

---

## 통과 항목 요약

| 통과 검증 | 결과 |
|---|---|
| 6 보조 산출물 모두 ② 단계 자체 검수 PASS | ✅ |
| 🟢 착수 블록 + 🔴 종료 블록 부착 6/6 | ✅ |
| qa-designer 필수 연구 질문 verbatim 일치 (88장·89장 2/2) | ✅ |
| scripture-deep verbatim + 7 URL fetch 검증 (nwtsty 4 + 통찰 3) | ✅ |
| publication-cross-ref 12 docid HTTP 200 검증 + cross-link 양방향 5건 입증 | ✅ |
| publication symbol 분리 (lfb 1102016XXX vs jy 1102014XXX vs ia 1102013XXX vs it 12000XXXXX) | ✅ |
| jy 챕터 정정 (cbs-qa 의 122 → 123) cross-ref 본문·_selfcheck·재검수 3곳 명시 | ✅ |
| 시간 마커 8개 (4·7·10·15·18·21·23·29) outline·meta·qa 일치 | ✅ |
| 30분 (1800초) ±120초 시간 분배 가능성 | ✅ |
| 외부 14축 결합 ≥ 2 (cbs 차등 적용표 임계) | ✅ (eq) — 1세기 매장 풍습·헬라어 nikao·헬라어 시네드리온·미슈나 야간 재판·1세기 가야바 집 구조·혈한증 (눅 22:44 땀) 등 6축 |
| 출판물「」 ≥ 3 (cbs 차등 적용표 임계) | ✅ (12개 unique 횡단 인용 — jy 6 + it 3 + it-2 1 + ia 2) |
| 4축 적용 균형 (가정·직장학교·회중·개인영성) | ✅ (24건 — 4축 × 2장 × 3건) |
| 9가지 상투적 청중 호명 회피 | ✅ (qa·apply·exp·illust grep 0건) |
| 정치·국가·종교 도상·회중 인물 거명 회피 | ✅ |
| 본문 verbatim 재서술·공식 질문 verbatim 재서술 회피 | ✅ |
| 경험담 4 요소 (출판물·docid·URL·항) 완비 3/3 | ✅ |
| 비유 후보 8필터 통과 (6/6) | ✅ |
| 할루시네이션 0건 | ✅ |

---

## cbs-script ④ 단계 인계 메모

### 우선 적용 사항

1. **jy 챕터 인용**: 횡단 인용 시 정확한 챕터 사용
   - 88장 (겟세마네 기도) → **jy 제123장 "몹시 비통할 때 기도하시다"** (docid 1102014723) — ⚠ jy 122 절대 인용 금지
   - 88장 (체포) → jy 제124장 "그리스도가 배반당하고 붙잡히시다" (1102014724)
   - 88장 (안나스·가야바 끌려감) → jy 제125장 "안나스에게 그리고 가야바에게 끌려가시다" (1102014725)
   - 88장 (표어 요 16:33) → jy 제121장 "용기를 내십시오! 내가 세상을 이겼습니다" (1102014721) — 챕터 제목이 표어성구 그 자체, 직접 권위 인용 가능
   - 89장 (베드로 부인) → jy 제126장 "베드로가 예수를 부인하다" (1102014726)
   - 89장 (산헤드린 재판) → jy 제127장 "산헤드린에서 재판받고 빌라도에게 넘겨지시다" (1102014727)

2. **통찰 docid**:
   - 88장 (겟세마네 어원) → 통찰 "겟세마네" (1200001671)
   - 88장 (안나스 인물) → 통찰 "안나스" (1200000284)
   - 88·89장 (가야바 인물) → 통찰 "가야바" (1200000856)
   - 88장 (눅 22:44 땀) → 통찰 "땀" (1200004273)
   - 88장 (가룟 유다) → 통찰 "유다, II" (1200002541)
   - ⚠ "산헤드린"·"모독" 항목은 한국어판 별도 항목 없음 → jy 127 + nwtsty 마 26:59·26:65 노트 사용

3. **「믿음을 본받으십시오」 (ia) 베드로 시리즈 — 89장 회복 1차 자료**:
   - 89장 (호언·시련) → ia 제22장 "시련을 겪으면서도 충성을 나타내다" (1102013268)
   - 89장 (회복·용서) → ia 제23장 "예수께 용서를 배우다" (1102013269)

4. **경험담 (experience-collector 검증 docid)**:
   - 88장 → 「파수대」 연구용 2024년 docid 2024245 (cbs_01 루이스·애나)
   - 89장 → 「파수대」 연구용 2021년 docid 2021445 (cbs_02 호세, cbs_03 네덜란드 자매 — 시간 빡빡 시 cbs_03 생략)

5. **"신앙" 단독 명사 4건 치환** (qa-designer 인계 사항):
   - cbs-qa.md B-2·B-4·B-5 의 "신앙" 4건 → "여호와에 대한 믿음" / "주를 따르는 자세" / "주께 대한 충성" 으로 치환

6. **시간 마커 8개**: `4'·7'·10'·15'·18'·21'·23'·29'` 빨강 볼드 우측정렬.

7. **(필수) 연구 질문**: 빨강 라벨 "(필수) 연구 질문" + 노랑 하이라이트 + 검정 볼드. verbatim 보존.

8. **핵심 성구**: 파란색 #2F5496 (요 16:33 / 요 16:32).

9. **publication symbol 분리**: 전면 = 「훈」 88장 / 「훈」 89장 (lfb 1102016XXX) / 횡단 = 「예수」 책 NN장 (jy 1102014XXX) — "책" 명시 의무 / 「믿음을 본받으십시오」 NN장 (ia 1102013XXX) / 「통찰」 "XX" 항목 (it 12000XXXXX) — 절대 혼동 금지.

10. **30분 (1800초) ±120초** — quality > timing 정책. timing FAIL 이라도 quality PASS 면 통과.

11. **할루시네이션 절대 금지** — 검증된 docid 만 인용. 「파수대」 특정 호 인용은 검증된 2024245, 2021445 만. 「통찰」 산헤드린·모독은 별도 항목 인용 회피.

### 권장 시간 매핑 (qa-designer + illustration-finder + experience-collector 통합)

| 시간 | 블록 | 1순위 활용 |
|---|---|---|
| 0~1' | 사회자 오프닝 | 두 장 통합 도입 한 문장 |
| 1'~4' | 88장 4단락 낭독 + 표어성구 요 16:33 | 낭독자 |
| 4'~7' | 88장 (필수)Q + 답변 + 보강 | qa §A-1·A-2 + jy 123 (겟세마네) + 통찰 "겟세마네" 어원 + 통찰 "땀" + 비유 88-1 (소방관) + 「미슈나」 야간 재판 (간접 보강) |
| 7'~10' | 88장 삽화·확장Q·마지막Q·3축 적용·경험담 | qa §A-3~A-6 + 비유 88-2 (항해사) + 경험담 cbs_01 (루이스·애나) |
| 10'~15' | 89장 전환 멘트 + 6단락 낭독 + 표어성구 요 16:32 | 낭독자 + jy 121 (요 16:32 권위 출처) |
| 15'~18' | 89장 (필수)Q + 답변 + 보강 | qa §B-1·B-2 + jy 126 + ia 22 (베드로 호언) + 통찰 "가야바" + 비유 89-1 (등산) |
| 18'~21' | 89장 핵심 성구 보강 (눅 22:31-32 중재 기도) + 확장Q | scripture-deep gem-06 + 비유 89-2 (의사) + 경험담 cbs_02 (호세) |
| 21'~23' | 89장 삽화 + 산헤드린 보강 | qa §B-4 + jy 127 + nwtsty 마 26:59·26:65 (산헤드린 헬라어·모독) |
| 23'~29' | 89장 마지막Q + 3축 적용 + ia 23 (회복) + 결론 | qa §B-5 + ia 23 (베드로 회복) + 비유 89-3 (재활) + 두 장 통합 결론 + 다음 주 90-91장 예고 |
| 29'~30' | 마침 | 짧은 격려 한 줄 |

### 보강 성구 verbatim 확인 (fact-checker ⑥ 단계 권장)

- 마 26:39·눅 22:43·요 13:38·눅 22:31-32·눅 22:61-62 — scripture-deep gem-03 ~ gem-07 에 nwtsty verbatim 모두 확보. cbs-script 는 그대로 사용.
- 행 4:13·요 9:25·요 21:15-19 (application-builder 보강) — 절 참조만. fact-checker ⑥ 가 1회 verbatim 확인 권장.
- 레위기 24:16 (모독죄 율법) — gem-09 §2-3 verbatim 확보.

---

## NEEDS-RERUN 시 재지시 (해당 없음)

본 ③ 단계 검수 결과 **PASS** — NEEDS-RERUN 0건. 모든 보조 산출물이 cbs-script ④ 단계 인계 가능 상태. publication-cross-ref 누락은 본 검수 직전 재호출로 보충 완료. jy 챕터 정정·통찰 docid 통합·"신앙" 치환 권고는 ③ 단계에서 명시 완료, cbs-script ④ 가 반영하면 됨.

---

## 6단 방어(v2) 진행 상태

- ✅ ① Planner 착수 전 방향 지침 (meta.yaml `instructions_to_subresearchers` 6건)
- ✅ ② 서브 에이전트 자체 검수 (6/6 _selfcheck PASS — publication-cross-ref 는 재호출로 누락 보충 완료)
- ✅ **③ Planner 1차 재검수 (본 _planner_review.md — PASS)**
- ⏳ ④ Script 작성 + 자체 검수 (대기)
- ⏳ ⑤ Planner 2차 재검수 (대기)
- ⏳ ⑥ 4종 게이트 (fact·jw-style·timing·quality-monotonic) (대기)

---

🔴 종료 블록 — Planner ③ 1차 재검수 종료. cbs-script ④ 단계로 인계.
