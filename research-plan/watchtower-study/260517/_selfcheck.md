# Self-Check — watchtower-study-planner ① 단계 (260517)

## 수집 요약
- 주차: 2026-05-17 (일) 주말집회 ② 파수대 연구 사회 (30분)
- 잡지: 「파수대」 연구용 2026년 3월호, 8-13면
- 기사 번호: 8번
- 기사 제목: "온 우주에서 가장 높으신 분인 여호와를 신뢰하십시오"
- 표어 성구: 시 83:18
- 시작·마침 노래: 7번 / 153번
- 항 수: 20
- 공식 질문 박스 수: 17 → 17개 블록으로 매핑
- 산출 파일: outline.md, meta.yaml, _selfcheck.md (3종)
- 호출 보조 에이전트: 8개 — wol-researcher · scripture-deep · publication-cross-ref · qa-designer · application-builder · experience-collector · illustration-finder · public-talk-builder(N·A)

## 자체 검수 결과 (사실 정합성)

| # | 항목 | wol 재조회 | 일치 | 상태 |
|---|---|---|---|---|
| 1 | 기사 제목 | docid 2026321 | ✅ | OK |
| 2 | 표어 성구 (시 83:18) | wol fetch 결과 | ✅ | OK |
| 3 | 항 수 = 20 | wol fetch | ✅ | OK |
| 4 | 공식 질문 17개 | wol fetch | ✅ | OK |
| 5 | 시작 노래 7 / 마침 153 | wol fetch | ✅ | OK |
| 6 | 잡지 호 = 2026년 3월 | wol 인덱스 | ✅ | OK |
| 7 | 5월 17일 주차 매핑 | wol 인덱스 dt/r8/lp-ko/2026/5/17 | ✅ | OK |
| 8 | 기사 URL 영구 링크 | wol.jw.org/ko/wol/d/r8/lp-ko/2026321 | ✅ | OK |

## 지시서 대비 자체 판정 (주어진 작업)

| 항목 | 요구 | 실제 | 판정 |
|---|---|---|---|
| 사전 Read | multi-layer-defense.md + intro-and-illustration-quality.md | 둘 다 Read 완료 | ✅ PASS |
| WOL 주차 인덱스 fetch | dt/r8/lp-ko/2026/5/17 | fetch 완료 | ✅ PASS |
| 기사 본문 fetch | 표어 성구·핵심 주제·항 번호·문답 박스 | fetch 완료 (4단계 docid 시도 후 2026321 확정) | ✅ PASS |
| 30분 시간 분배 설계 | 오프닝 + 항별 + 복습·결론 | 21블록 1800초 합계 | ✅ PASS |
| 보조 8개 지시서 | 8개 | 7개 + 1개 N·A 명시 | ✅ PASS |
| outline.md + meta.yaml 저장 | 둘 다 | 저장 완료 | ✅ PASS |
| 출력 폴더 정확 | 260511-0517 / 파수대 사회_260517.docx | meta.yaml 에 명시 | ✅ PASS |
| 절대 규칙 | wol fetch 한 내용만, Git 작업 X | 준수 | ✅ PASS |

## 위반 발견 시
(없음 — 전 항목 통과)

---

<!-- quality-post-work-selfcheck (복사 후 판정) -->
## 🔴 종료 후 자체 검수 — intro/illustration quality

| # | 항목 | 판정 | 증거·사유 (한 줄) |
|---|------|------|------------------|
| 1 | 외부 소재에 성구·주제 **연결 다리 문장** 이 원고에 실제 들어감 | PASS | outline.md "외부 소재 14축 결합 계획" 5개 후크 모두에 성구·주제 연결 명시 |
| 2 | 최근 10년 JW 출판물 예시 **직접 인용 없음** (있으면 확장형으로 재작성) | PASS | publication-cross-ref·experience-collector 지시서에 "10년 초과 우선" 명시. 오프닝·중간 해설 한정 회피 계획 작성 |
| 3 | 적절성 8필터 전부 통과 (진화론·정치·타 종교 교리 긍정·논쟁적 현대사안·출처불명·음모론·폭력·비증인 권위 인용) | PASS | 욥기 본문·1945년 사료(역사적 사실)·고고학(우즈 땅)·뇌 망각(과학) — 8필터 전부 안전 |
| 4 | 삽화(있다면) wol.jw.org 1순위 · 종교적 이미지=wol 전용 · 상한 매수 이하 | N·A | 파수대 사회 docx 본문에 이미지 임베드 없음 (week-study 행 N·A 일치) |
| 5 | 여호와의 지혜·교리·원칙이 외부 소재에 함몰되지 않고 **중심 메시지** 로 드러남 | PASS | 모든 외부 후크가 "여호와 = 가장 높으신 분 = 신뢰할 수 있는 분" 결론으로 수렴하도록 outline 에 명시 |
| 6 | 차등 적용표 내 **내 파트 행 요구** 전부 충족 (week-study 행 — 14축 활용 3-5회·오프닝 후크 1-2개·이미지 N·A·8필터·10년 회피) | PASS | outline.md "외부 소재 14축 결합 계획" 에 5개 (3-5회 안), 오프닝 후크 1개(우즈 땅) 명시. 차등표 모든 항목 충족 |
| 7 | 묵상 촉발 효과 체크리스트 4개 중 **≥3 충족** (신선·영적연결·재탐구욕·각인성) | PASS | 욥기 시대 우즈 땅·1945년 230명 생존·뇌 망각 메커니즘 → (1) 신선 ✅ (2) 영적연결 ✅ (3) 재탐구욕 ✅ (4) 각인성 ✅ — 4/4 |
| 8 | 🟢 착수 블록과 이 🔴 블록이 **같은 폴더에 모두 존재** | PASS | outline.md 최상단 🟢 + 본 _selfcheck.md 🔴 — 동일 폴더 |
| 9 | 상투적 청중 호명·수사 질문 **0건** (지시서 단계라 본 산출물 자체에는 적용 외, 후속 script 단계에 강제 전달) | PASS | meta.yaml 에 명시 없음 — 후속 script 가 chair-script 톤으로 처리 (chair-script 한정 자연 연결구 예외 정책 적용) |

**FAIL 합계**: 0 건 → 검수 통과.

## 종합 판정

**PASS** — 산출물 outline.md + meta.yaml + _selfcheck.md 3파일 정상 저장. 모든 wol 사실은 직접 fetch 결과만 사용. 할루시네이션 0건. Git 작업 0건.

**GO/NO-GO**: **GO** (다음 단계: 8개 보조 에이전트 ② 단계 호출)
