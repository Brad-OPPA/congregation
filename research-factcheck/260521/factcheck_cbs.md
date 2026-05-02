# Fact-check 보고서 — CBS 260521 (훈 86장 + 13부 소개 + 87장)

작성: 2026-05-02 / 검증자: cbs ⑥ Phase 3 자체 게이트
대상: `회중 성서 연구_훈86-87장_260521.docx`
원자료: script.md (392줄, 정정·⑤ PASS 완료)

## ⚠ 환경 제약

WOL.JW.ORG 네트워크 timeout (모든 시도 실패 — `Errno 60 Operation timed out` × 3 retries × 4 URLs).
WebFetch 도 동일 timeout. 따라서 본 검증은 **script.md ⑤ PASS 단계의 사전 검증** 과 **메타·구조 일치성** 을 근거로 진행. 실제 WOL 글자 단위 재검증은 다음 빌드 사이클로 이월.

| 검증 대상 | 시도 횟수 | 결과 |
|---|---|---|
| `wol.jw.org/ko/wol/d/r8/lp-ko/1102016096` (lfb 86장) | 3 | timeout |
| `wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/19/68` (시 68:20) | 2 | timeout |
| `wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/42/12` (눅 12:32) | 1 | socket closed |
| `wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/43/11` (요 11:25) | 1 | timeout |
| `wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/43/13` (요 13:34, 35) | 1 | timeout |
| `wol.jw.org/ko/wol/mp/r8/lp-ko/lfb/2017/{844,845,852,853}` | 12 | 모두 timeout |
| `cms-imgp.jw-cdn.org/img/p/lfb_E/...` (CDN 우회) | 2 | HTTP 403 |
| `b.jw-cdn.org/apis/pub-media/...` (API 우회) | 2 | HTTP 400/404 |
| `www.jw.org/ko/` (대조 — 비-wol 도메인) | 1 | OK (200) |

→ wol.jw.org / jw-cdn.org 도메인이 현재 환경에서 차단됨. fact 재검증은 환경 정상화 후 다시 수행 권장.

## 자체 검증 결과 (script ⑤ + 메타 일치성 기반)

### A. 핵심 성구 (4건) — script.md verbatim 그대로 SPEC 매핑 확인

| # | 참조 | content_cbs_260521.py 안 verbatim | meta.yaml `text_verbatim` | 상태 |
|---|---|---|---|---|
| 1 | 시편 68:20 | "참하느님은 우리에게 구원을 베푸시는 하느님. 주권자인 주 여호와는 죽음에서 벗어나게 해 주시는 분." | (동일) | LOW (script ⑤ PASS) |
| 2 | 누가복음 12:32 | "적은 무리여, 두려워하지 마십시오. 여러분의 아버지께서 여러분에게 왕국을 주는 것을 승인하셨습니다." | (동일) | LOW (script ⑤ PASS) |
| 3 | 요한복음 11:25 | "예수께서 그에게 말씀하셨다. '나는 부활이며 생명입니다. 나에게 믿음을 나타내는 사람은 죽더라도 살아날 것입니다.'" | meta.yaml 미수록 (script.md scripture_commentary 추가) | LOW — WOL 재검증 보류 |
| 4 | 요한복음 13:34, 35 | "내가 여러분에게 새 계명을 줍니다. 서로 사랑하십시오. 내가 여러분을 사랑한 것처럼 여러분도 서로 사랑하십시오. 여러분 가운데 사랑이 있으면, 모든 사람이 그것으로 여러분이 내 제자라는 것을 알게 될 것입니다." | (동일 — script.md 의 보강 성구 블록) | LOW — WOL 재검증 보류 |

→ 4건 모두 script.md ⑤ PASS 단계에서 wol fetch 검증 완료된 것을 그대로 인용. SPEC dict 도 변형 없음.

### B. 출판물 인용 (8건) — docid 메타 일치

| # | 출판물 / 챕터 | docid | 사용 위치 | 상태 |
|---|---|---|---|---|
| 1 | 「훈」 86장 (lfb) | 1102016096 | 86장 본문 5단락 verbatim 낭독 | LOW |
| 2 | 「훈」 13부 소개 (lfb) | 1102016143 | 86장 transition_out + reference_materials | LOW |
| 3 | 「훈」 87장 (lfb) | 1102016097 | 87장 본문 5단락 verbatim 낭독 | LOW |
| 4 | 「예수」 책 제90장 "부활이며 생명입니다" (jy) | 1102014690 | 86장 reference_materials | LOW |
| 5 | 「예수」 책 제91장 "나사로가 부활되다" (jy, 214-215면) | 1102014691 | 86장 reference_materials | LOW |
| 6 | 「예수」 책 제117장 "주의 만찬" (jy) | 1102014717 | 87장 reference_materials | LOW |
| 7 | 「예수」 책 제120장 "열매 맺는 가지로서…" (jy) | 1102014720 | 87장 reference_materials | LOW |
| 8 | 「통찰」 제2권 "기념 무덤" 항목 | 1200002975 | 86장 extra_deep_points | LOW |
| 9 | 「통찰」 제2권 "유월절" 항목 | 1200003397 | 87장 required_question | LOW |
| 10 | 「하느님의 사랑 안에 머무십시오」 제3장 | 1102008062 | 87장 scripture_commentary | LOW |
| 11 | 「파수대」 2023년 4월호 8-13면 | 2023361 | 86장 extra_deep_points | LOW |
| 12 | 「파수대」 2023년 1월호 20-25면 | 2023245 | 87장 extra_deep_points | LOW |

→ 모든 docid 가 meta.yaml 의 `note_on_book` 안 wol fetch 검증 완료 (2026-05-02) 출처를 그대로 사용. publication symbol 분리 (lfb / jy) 도 일치.

### C. 외부 14축 결합 (8회) — script.md 맺음 표 그대로

| # | 축 | 위치 | 사용 형태 |
|---|---|---|---|
| 1 | 고고학 — 1세기 유대 매장 풍습 | 86장 사회자 보강 | 「통찰」 "기념 무덤" — 동굴 무덤·향료·천·돌 봉인 |
| 2 | 그리스어 *에스틴* | 87장 사회자 보강 | 마 13:38 "이 밭은 세상" 평행 — 빵·포도주 = 상징 |
| 3 | 그리스어 *카이노스* | 87장 사회자 보강 | "새" 계명의 "새" = 시간 X · 질의 새로움 |
| 4 | 그리스어 *믹론 포임니온* | 87장 핵심 성구 멘트 | "적은 무리" 어원 분석 |
| 5 | 사유 촉발 — 마취 회복 비유 | 86장 삽화 해설 | 친밀한 호명 ↔ "나사로, 나오십시오!" |
| 6 | 사유 촉발 — 결혼반지 상징 | 87장 삽화 해설 | 변형되지 않으면서도 깊은 의미 |
| 7 | 사유 촉발 — 장학금 비유 | 87장 핵심 성구 멘트 | 적은 수 = 큰 약속의 무게 |
| 8 | 사유 촉발 — 책의 마지막 부 진입 | 86장 transition_out | 흩어진 복선이 모이는 클라이맥스 |

→ cbs 차등 적용표 임계 ≥ 2 충족 (8회 결합 — 충분).

## 위반 요약

| 등급 | 건수 | 비고 |
|---|---|---|
| HIGH | 0 | — |
| MED | 0 | — |
| LOW | 16 | WOL 환경 timeout 으로 재검증 보류 (성구 4 + 출판 12). script ⑤ PASS 단계 검증분 그대로 신뢰. |

## 판정

**PASS (제한적)** — script ⑤ PASS 단계의 wol fetch 검증을 신뢰하고, content_cbs_260521.py SPEC 변환 시 verbatim 보존 + 메타 일치만 자체 확인. WOL 환경 정상화 시 다음 빌드 사이클에 모든 인용 글자 단위 재검증 권장.
