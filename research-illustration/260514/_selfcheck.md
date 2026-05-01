<!-- quality-post-work-selfcheck (복사 후 판정) -->
## 🔴 종료 후 자체 검수 — intro/illustration quality (260514 — illustration-finder)

| # | 항목 | 판정 | 증거·사유 (한 줄) |
|---|------|------|------------------|
| 1 | 외부 소재에 성구·주제 **연결 다리 문장** 이 원고에 실제 들어감 | **PASS** | 5개 산출 파일 각 §3 "영적 연결 다리 문장" 명시 (사 44·45·60·갈 4 직접 인용) |
| 2 | 최근 10년 JW 출판물 예시 **직접 인용 없음** | **PASS** | 「파24.07」·「파17.06」·「파18.05」 모두 배경·풀이로만 사용, verbatim 인용 0건 |
| 3 | 적절성 8필터 전부 통과 | **PASS** | 5개 후보 모두 진화론 전제 X · 정치 X · 타 종교 교리 긍정 X · 성·폭력 X · 출처 명확 · 음모론 X · 현대 논쟁 X · 비증인 권위 인용 X |
| 4 | 삽화 wol.jw.org 1순위 · 종교적 이미지=wol 전용 · 상한 매수 이하 | **PASS** | 시드 이미지 1장 (mwb26/2026/174 wol 1순위, 종교성 5질문 → 낙원·새 예루살렘이지만 wol 자료라 OK), 외부 후보 3개는 모두 세속 (키루스 원통·다윗 성·안드로메다 — 종교성 5질문 ALL no) |
| 5 | 여호와의 지혜·교리·원칙이 **중심 메시지** 로 드러남 | **PASS** | 모든 후보 결론이 사 60:1·11·19, 갈 4:26 의 "여호와 지혜·예언 성취·영원한 빛" 으로 수렴 |
| 6 | 차등 적용표 mid-talk10 행 요구 충족 (14축·후크 후보 수) | **PASS** | 14축 5축 결합 (#2 우주 + #6 고고학 + #7 지형 + #10 의미 + #11 시간) — 의무 ≥3 초과 / 서론 후크 4개 (의무 3~5) / 요점당 예화 2~3개 (요점 1·2·3 모두) |
| 7 | 묵상 촉발 효과 체크리스트 4개 중 ≥3 충족 | **PASS** | 5개 후보 모두 3/4 또는 4/4 |
| 8 | 🟢 착수 블록과 이 🔴 블록이 같은 폴더에 모두 존재 | **PASS** | 🟢 = `01_cyrus-cylinder.md` 최상단 / 🔴 = 본 파일 |
| 9 | 상투적 청중 호명·수사 질문 (9가지 금지 표현 + 동류) **0건** | **PASS** | "여러분도 …해 보신 적 있으십니까?" 류 표현 본 폴더 산출물 전수 검색 0건 |

**FAIL 합계**: 0 건 → ✅ **검수 통과**

---

## ⭐ Phase E 시드 이미지 자동 다운로드 — 별도 판정

| 항목 | 값 / 판정 |
|------|----------|
| WOL 본 주차 삽화 페이지 | https://wol.jw.org/ko/wol/mp/r8/lp-ko/mwb26/2026/174 |
| 실제 이미지 URL | (mp 엔드포인트가 jpg 직접 응답 — 별도 추출 불필요) |
| 헬퍼 호출 | `python3 _automation/download_image.py "<url>" "<save_path>"` |
| 저장 경로 (절대) | `/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/260511-0517/260514_treasures.jpg` |
| 파일 크기 | **162,866 bytes** (≥1KB ✅) |
| MD5 | `f1ff872280c660f4469fd182b0b9fb7b` |
| 직전 주차 (260507) MD5 | `a7236d1126dcef5e44ba24df9632d8f1` |
| 동일 여부 | ❌ **다름** — 직전 주차 재사용 0건 ✅ |
| 디렉터리 자동 생성 | ✅ `260511-0517/` 새 디렉터리 자동 생성됨 |

**시드 이미지 다운로드 결과**: ✅ **PASS** (Phase E 통과)

---

## 산출 파일 목록 (research-illustration/260514/)

- ✅ `01_cyrus-cylinder.md` (요점 1 ★★★ — 🟢 착수 블록 포함)
- ✅ `02_jerusalem-rebuild.md` (요점 1·2)
- ✅ `03_partial-fulfillment.md` (요점 2 ★★★)
- ✅ `04_starlight-time.md` (요점 3 ★★★)
- ✅ `05_mother-symbol.md` (요점 3 정서)
- ✅ `06_intro_image_candidates.json` (서론 시각 자료 3안)
- ✅ `_intro_hooks.md` (서론 후크 4개 + 결론 2개)
- ✅ `_image_log.md` (시드 이미지 다운로드 검증 로그)
- ✅ `_selfcheck.md` (본 파일 — 🔴 종료 블록)

## 직전 주차 비교 (② 자체 검수 의무, 2026-04-29 도입)

직전 주차 `research-illustration/260507/` 폴더 비교 결과:
- 본 산출 후보 수: **5개 후보** (요점별 2~3개 분산) + 서론 후크 4개 + 결론 2개
- 14축 결합: **5축** (#2·#6·#7·#10·#11)
- 외부 1차 자료 교차 검증: 5건 (BM·Britannica·Smithsonian·NASA·Science DOI)
- 산출 파일 수: 9개
→ 직전 baseline 보다 같거나 더 풍부 ✅

---

**status: PASS**
**Phase E 시드 이미지: PASS**

---

## 🔴 종료 블록 (2026-05-01 보강)

본 보강은 새 본질 정책 (2026-05-01) — 외부 14축 본문 침입 0건 / 예 자리도 권장 0 / 일상 비유 권장 — 에 맞춰 illustration-finder 를 재호출한 결과이다.

- [x] 결론용 집교 본 주차 삽화 다운로드 + 해설 자료 작성
  - 다운로드: `/Users/brandon/Claude/Projects/Congregation/research-illustration/260514/conclusion_image.jpg` (162,866 bytes)
  - 해설: `/Users/brandon/Claude/Projects/Congregation/research-illustration/260514/conclusion_image_meaning.md` (장면 묘사 + 요점 1·2·3 매핑 + 배울 점 3개 + 결론 멘트 활용 예)
- [x] 일상 비유 흥미 유발 예 ≥ 6개 (요점당 2개 이상) — **실제 9개 / 요점당 3개**
  - 통합 파일: `/Users/brandon/Claude/Projects/Congregation/research-illustration/260514/daily_metaphors.md`
  - 분포: 요점 1 (사 60:1·2) 3개 — 정전 등불 / 산속 일출 / 새벽 안개 / 요점 2 (사 60:11) 3개 — 약혼 → 결혼 / 씨앗 → 열매 / 책 시리즈 / 요점 3 (갈 4:26) 3개 — 어머니 품 / 가족 식탁 / 모교
- [x] 외부 14축 후보 4 (cyrus-cylinder · jerusalem-rebuild · partial-fulfillment · starlight-time) 는 본 정책으로 사용 안 함 — 일상 비유로 대체
  - 4개 파일은 보존하되 본문·예 자리 둘 다 사용 0 (히스토리 참고용 only). daily_metaphors.md §"외부 14축 후보 4개 처분" 참조.
- [x] 모든 신규 후보 메타 표시 (supports_main_paragraph / where_to_place / axis 일상)
  - 각 후보 9개에 5축 메타 (supports_main_paragraph · where_to_place · non_other_religion · fact_verified · axis="일상") 모두 명시. daily_metaphors.md §메타 요약 표 참조.

**status (2026-05-01 보강): PASS**
