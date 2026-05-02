# _selfcheck.md — illustration-finder 260528 (영적 낙원)

## 🔴 종료 후 자체 검수 블록

| 게이트 | 기준 | 결과 | 증거 |
|---|---|---|---|
| ① 외부 14축 ≥ 3 | 적절성 8필터 통과 후 3축 이상 | **PASS** | 14축 5번 (생태계 질서) + 11번 (자연 비유) + 14번 (상실·회복 공감) — 일차 출처 URL 모두 명시 |
| ② 요점당 예화 후보 ≥ 2 | 총 ≥ 6 | **PASS** | 요점 1: 1-A·1-B·1-C (3개) / 요점 2: 2-A·2-B·2-C (3개) / 요점 3: 3-A·3-B·3-C (3개) → 총 9개 |
| ③ 시드 이미지 결정 | 골자 폴더 .jpg/.png 우선, 없으면 wol src URL + 다운로드 명세 | **PASS** | 골자 폴더 부재 확인 → wol mp/r8/lp-ko/mwb26/2026/190 (large) + 189 (small) src URL 추출 + curl content-type/length 검증 (image/jpeg, 165278) + download_image.py 인계용 yaml 명세 작성 |
| ④ 적절성 8필터 | 8 항목 전부 통과 | **PASS** | 진화 ❌ / 정치 ❌ / 타종교 ❌ / 미검증 ❌ / 사생활 ❌ / 비증인 권위 본문 호명 ❌ (예 자리만 짧게) / 논쟁 ❌ / 14축 본문 침입 ❌ |

## 종합: **PASS** (재작업 불필요)

## 추가 점검 항목

| 점검 | 결과 |
|---|---|
| 결론 도입 예화 1개 ✅ | 식탁 콜백 + 4 장면 삽화 도입 콘셉트 |
| 서론 후크 후보 3~5개 ✅ | 4개 (A·B·C·D) |
| R3 본문 침입 0 권장 ✅ | 모든 외부 자료 예 자리에만 / 학술 동사·연도·왕조 본문 진입 X |
| R16 비유 메시지 중복 X ✅ | 서론 A (가족 식탁) ↔ 요점 1 (식탁 점검) 비유 중복 점검 — 식탁 = 같지만 메시지 다름 (서론은 빈 의자 / 요점 1 은 끼니 점검) |
| 사용자 NG 어휘 0 ✅ | "가정 경배"·"신자"(단독)·"여호와의 임재"·"수동적..." grep 0건 |
| 일차 출처 URL 명시 ✅ | 외부 ① ScienceDirect+Earth.com / 외부 ② DesertUSA+Geography Realm / 외부 ③ Cambridge+Wikipedia |
| 결론 집교 삽화 임베드 명세 R12 ✅ | mp/r8/lp-ko/mwb26/2026/190 large + 189 small + 4 장면 매핑 해설 |
| R15 정형 표현 "삽화를 함께 보시겠습니다" ✅ | 결론 도입 예화 안에 박혀 있음 |
| R13 서론 ↔ 결론 콜백 키워드 "식탁" ✅ | 서론 A·C·D 와 결론 도입 예화 모두 식탁 콜백 |

## 발굴한 자료 verbatim 재조회 (할루시네이션 차단)

| 자료 | 재조회 결과 |
|---|---|
| WOL 본 주차 (202026164) | curl GET 38862 bytes — 본문 삽화 1개 (id=f1) — img src=/ko/wol/mp/r8/lp-ko/mwb26/2026/190 + data-img-small-src=/ko/wol/mp/r8/lp-ko/mwb26/2026/189 + alt 4 장면 caption 일치 ✅ |
| WOL 결론 삽화 jpg | curl HEAD content-type: image/jpeg / content-length: 165278 ✅ |
| 외부 ① 일차 출처 | PMC7593183 + Earth.com 4-predator coexistence — WebSearch 응답으로 확인 ✅ |
| 외부 ② 일차 출처 | DesertUSA Oasis ecosystem + Geography Realm — WebSearch 응답으로 확인 ✅ |
| 외부 ③ 일차 출처 | Cambridge "Whose fault is famine?" + Wikipedia Great Famine Ireland — WebSearch 응답으로 확인 ✅ |

## 메인 / planner 인계 메모

1. **다운로드 단계**: download_image.py 가 illustrations.md 내 yaml 블록 (id=fig1_conclusion) 의 src_url + fallback_url 순으로 시도. content-type 검증 후 download_target 경로에 저장.
2. **script 가 받을 핵심 매핑**: 4 장면 ↔ 3 요점 표 (illustrations.md 안). script 는 결론 도입 예화 자리에서 이 매핑을 그대로 풀어 쓰면 됨.
3. **외부 자료 본문 침입 경고**: planner·script 가 외부 자료를 본문에 진입시키지 말 것. **예 자리에 1~2 문장**, 학술 동사 ("정리"·"보여주다"·"밝혀주다"·"짚다") + 출처명 결합 패턴 금지. 출처는 각주/research-illustration/ 폴더 안에만.
4. **서론 후크 추천 순위**: A (가족 식탁) > B (사막 오아시스) > C > D. A 가 결론 콜백 ("식탁") 과 가장 자연스럽게 연결됨.
5. **요점별 추천 예화**: 1-A (가족 식탁 점검) / 2-A (입원실 방문 — 결론 삽화 ④ 매칭) / 3-A (회중 적대 화해). 모두 결론 삽화 4 장면과 자연 매핑.
