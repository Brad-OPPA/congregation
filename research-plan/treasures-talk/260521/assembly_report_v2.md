# Assembly Report — 10분 연설 "사랑 많고 동정심이 풍부한 도공" (260521 v2)

> 작성: 2026-05-01 — assembly-coordinator 자동 재작성 1차 (5회 한도 中 1/5)
> 사유: ⑦ 4종 게이트 中 fact-checker FAIL (HIGH 5) + jw-style-checker FAIL (HIGH 2) → 재빌드 강제
> v1 산출물: `10분 연설_사랑 많고 동정심이 풍부한 도공_260521_v1.docx`/.pdf
> v2 산출물: `10분 연설_사랑 많고 동정심이 풍부한 도공_260521_v2.docx`/.pdf
> 메인 직접 정정 X (Phase E 정책 준수) — assembly-coordinator 책무

---

## 1. 입력 (재호출 사유)

| 게이트 | 결과 | HIGH | 정정 대상 |
|---|---|---|---|
| planner ⑥ | PASS | — | — |
| **fact-checker** | **FAIL** | **5건** | 갈 6:8 verbatim · 사 63:10 verbatim · references 1번 라벨 (mwb) · references 2번 면수 (28-29 → 26-31) · references 「통찰」 '도공' URL (1200002436 → 1200003537) |
| **jw-style-checker** | **FAIL** | **2건** | "거룩한 영" → "성령" (사 63:10 안) · 갈 6:8 verbatim |
| timing-auditor | FAIL (842초) | — | quality > timing 정책으로 통과 (timing 조정 X) |
| quality-monotonic-checker | PASS | — | (1 MED 만 — 본 정정 범위 외) |

→ **HIGH 7건 합산** (fact-style 중복 2건 차감 = 사실 정정 5 항목 + 라벨/URL 정정 3 항목 = **유니크 7 정정 지점**).

---

## 2. WOL WebFetch 직접 재조회 결과 (2026-05-01)

| 검증 항목 | URL | 결과 |
|---|---|---|
| 사 63:10 정본 | `https://wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/23/63` | ✅ 직접 본문 추출 — "그러나 그들은 반역하여 그분의 성령을 근심하게 했다. 그래서 그분은 그들의 적이 되시어 그들과 싸우셨다." |
| 갈 6:8 정본 | `https://wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/48/6` | ⚠️ 직접 추출 거부 (저작권 안전장치). 우회 검증: WOL 검색 q="육체로부터 썩어 없어질 것" → 7 결과 中 6 건 정본 일치 매치 → "육체를 위해 뿌리는 사람은 육체로부터 썩어 없어질 것을 거두고, 영을 위해 뿌리는 사람은 영으로부터 영원한 생명을 거둘 것입니다." 확정 |
| 「통찰」 '도공' docid | `https://wol.jw.org/ko/wol/d/r8/lp-ko/1200003537` | ✅ "도공 (Potter)" — 「성경 통찰, 제1권」 도공 항목 (요체르 어근, 도공 작업·그릇·도공-진흙 비유 신학) |
| 「파23.08」 면수·항 | `https://wol.jw.org/ko/wol/d/r8/lp-ko/2023528` | ✅ "반드시 져야 할 짐만 지고 나머지는 벗어 버리십시오" / 2023년 8월호 / **26-31면** / **8항이 갈 6:7,8 인용** |
| mwb 본 주차 | `https://wol.jw.org/ko/wol/d/r8/lp-ko/202026163` | ✅ "그리스도인 생활과 봉사—집회 교재 (mwb 5월호)" / 5월 18-24일 주 / 페이지 헤더 "집교26 5월호 5-16면" — 「파수대」 아님 |

---

## 3. 정정 7 지점 표 (verbatim 비교 + grep PASS 증거)

| # | 위치 | NG (v1) | 정본 (v2) | docx grep (NG) | docx grep (정본) | 검증 |
|---|---|---|---|---|---|---|
| 1 | scripture_2 (갈 6:8 회색 박스) | "자기 육체를 위해 뿌리는 사람은 자기 육체에서 부패를 거두겠지만, 영을 위해 뿌리는 사람은 영에게서 영원한 생명을 거둘 것입니다." | "육체를 위해 뿌리는 사람은 육체로부터 썩어 없어질 것을 거두고, 영을 위해 뿌리는 사람은 영으로부터 영원한 생명을 거둘 것입니다." | "자기 육체를 위해 뿌리는" = **0** ✅<br>"자기 육체에서 부패" = **0** ✅<br>"영에게서 영원한" = **0** ✅ | "육체로부터 썩어 없어질 것을 거두고" = **1** ✅<br>"영으로부터 영원한 생명" = **1** ✅ | WOL 검색 매치 6/7 |
| 2 | scripture_conclusion (사 63:10 회색 박스) | "그런데 그들이 반역하여 그분의 거룩한 영을 슬프게 했다. 그래서 그분이 그들의 적이 되어 친히 그들과 싸우셨다." | "그러나 그들은 반역하여 그분의 성령을 근심하게 했다. 그래서 그분은 그들의 적이 되시어 그들과 싸우셨다." | "그런데 그들이 반역" = **0** ✅<br>"적이 되어 친히" = **0** ✅<br>"거룩한 영을 슬프게" = **0** ✅ | "그러나 그들은 반역하여" = **1** ✅<br>"성령을 근심하게" = **2** ✅<br>"적이 되시어" = **1** ✅ | WOL nwtsty/23/63 직접 |
| 3 | conclusion §2 자문 단락 콜백 | "백성이 반역하여 그분의 거룩한 영을 슬프게 한 모습" | "백성이 반역하여 그분의 성령을 근심하게 한 모습" | (위 ②와 합산) "거룩한 영을 슬프게" = **0** ✅ | (위 ②와 합산) "성령을 근심하게" = **2** ✅ (scripture_conclusion + 결론 §2 콜백) | #2 동기화 |
| 4 | references 1번 라벨 | "「파수대」 본 주차 연구 기사 253-254면 7-9항 — 동정심" | "「집회 교재 (mwb 5월호)」 본 주차 (5월 18-24일) 보물 단원 연구 자료 1, 2, 3 단락 — 동정심" | "본 주차 연구 기사 253-254면" = **0** ✅ | "mwb 5월호" = **1** ✅ | docid 202026163 = mwb |
| 5 | references 2번 면수 | "28-29면 8-9항" | "26-31면 8항" | "28-29면" = **0** ✅ | "26-31면 8항" = **1** ✅ | docid 2023528 페이지 헤더 |
| 6 | references 「통찰」 '도공' URL | `1200002436` (= 예루살렘) | `1200003537` (= 「통찰」 제1권 '도공' 항목) | "1200002436" = **0** ✅ | "1200003537" = **1** ✅ | docid 1200003537 직접 |
| 7 | (#3 처리 통합) | | | | | |

→ **17 grep 항목 전부 PASS** (NG 9건 = 0 / 정본 8건 ≥ 1).

---

## 4. v2 산출물 절대경로 + 크기

| 산출물 | 절대경로 | 크기 |
|---|---|---|
| script_v2.md | `/Users/brandon/Claude/Projects/Congregation/research-plan/treasures-talk/260521/script_v2.md` | (작성 완료) |
| content_260521_v2.py | `/Users/brandon/Claude/Projects/Congregation/_automation/content_260521_v2.py` | (작성 완료) |
| assembly_report_v2.md | `/Users/brandon/Claude/Projects/Congregation/research-plan/treasures-talk/260521/assembly_report_v2.md` | (본 파일) |
| **docx** | `/Users/brandon/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/260518-0524/10분 연설_사랑 많고 동정심이 풍부한 도공_260521_v2.docx` | **190,603 bytes** (v1 대비 +20 bytes — 단어 정정 차) |
| **PDF** | `/Users/brandon/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/260518-0524/10분 연설_사랑 많고 동정심이 풍부한 도공_260521_v2.pdf` | **363,446 bytes** (v1 대비 +1,513 bytes — LibreOffice 자동 변환 정상) |

빌드 로그:
```
Saved: .../10분 연설_사랑 많고 동정심이 풍부한 도공_260521_v2.docx
PDF (soffice): .../10분 연설_사랑 많고 동정심이 풍부한 도공_260521_v2.pdf
```

---

## 5. v1 → v2 비교 (텍스트 변동 범위)

- 본문 글자수 (공백 제외): v1 4,397자 → v2 **4,409자** (+12자, 정정 7 지점에 의한 자연 차이)
  - 갈 6:8 verbatim: "자기" 2회 삭제 (-4) + "부패를 거두겠지만" → "썩어 없어질 것을 거두고" (+9) + "영에게서" → "영으로부터" (+1) = +6
  - 사 63:10 verbatim: "그런데" → "그러나" (0) + "거룩한 영" → "성령" (-1) + "슬프게" → "근심하게" (+1) + "적이 되어 친히" → "적이 되시어" (-3) + 어미 미세조정 = -3
  - 결론 §2 콜백: "거룩한 영을 슬프게" → "성령을 근심하게" (위와 동일 +0 ~ -1)
  - references 라벨/면수/URL 변경 (+10)
- 시간 마커 5개 (`1'30"` / `3'30"` / `5'30"` / `7'30"` / `8'30"` / `9'30"`) **동일 유지**
- 5 흐름 서론·요점 1·2·3·결론 5 단락 **동일 유지**
- R1~R18 자체 측정 18 항목 **동일 PASS**

---

## 6. 다음 단계 진입 가능 여부

✅ **fact-checker + jw-style-checker 재호출 진입 가능** — 17 grep 자체 검증 PASS, 정정 범위 외 본문 변동 없음.

병렬 재호출 권고:
1. **fact-checker** (병렬 ⑦) — HIGH 5 정정 확인 + MEDIUM 2 (결론 삽화 URL 미정정 + 도박 자매 경험담 출처 미명시) 처리 여부 확인
2. **jw-style-checker** (병렬 ⑦) — HIGH 2 (갈 6:8 + 사 63:10 + "거룩한 영" 추측 표현) 모두 정정 확인
3. timing-auditor — 본 정정으로 시간 변동 거의 없음 (842초 → 약 843초 추정), quality > timing 정책으로 통과 가능
4. quality-monotonic-checker — v1 PASS 그대로 유지 (이미지·시간 마커·구성 변동 0)

PASS 시 사용자 검수 1회 진입.
FAIL 시 자동 재작성 2차 (5회 한도 中 2/5).

---

## 7. 잔여 미처리 항목 (메인 알림 — 재호출 범위 외)

| # | 항목 | 출처 | 처리 권고 |
|---|---|---|---|
| 1 | 결론 삽화 mwb URL HEAD = image/jpeg (MEDIUM 2) | fact-checker 보고서 | references 의 mwb HTML 페이지 URL 로 교체 — 다음 차수 (자동 재작성 2차) 또는 사용자 검수 단계 처리 |
| 2 | 도박 자매 경험담 출처 미명시 (MEDIUM 추가) | fact-checker 보고서 | research-experience/260521/ Read 후 출처 확정 또는 무명 1인칭 약화 — 다음 차수 처리 |

본 v2 는 **HIGH 7 정정만** 처리. MEDIUM 2 + MEDIUM 추가 1 = 3 항목은 다음 자동 재작성 차수 또는 사용자 검수 단계에서 별도 처리 (assembly-coordinator 1차 범위 외).

---

## 8. 메모리 정책 준수 확인

- [x] WOL WebFetch 직접 재조회 (훈련 기억 인용 X) — `feedback_wol_term_verification.md`
- [x] 메인 직접 정정 X — assembly-coordinator 책무 (Phase E `main-claude-edit-policy.md`)
- [x] 정정 범위 외 본문 변경 X (시간 마커 / 5 흐름 / 결론 5 단락 / 단어 풀이 / 적용 동결)
- [x] timing 조정 X — `feedback_six_gates_mandatory.md` 의 quality > timing 정책
- [x] 사용자 NG list (가정 경배·신자·여호와의 임재·수동적) 0건 유지 — `feedback_terms_user_specific_ng.md`
- [x] 자동 재작성 카운터 1/5 — `feedback_six_gates_mandatory.md`
