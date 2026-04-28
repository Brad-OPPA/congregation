# Self-Check — treasures-talk-planner ① 단계 (260514)

**대상 주차**: 260514 (2026-05-11 ~ 2026-05-17 / 집회일 목 2026-05-14)
**단계**: ① 착수 전 방향 지침 (지시서 작성)
**status**: **PASS**

---

## 작성 산출물

| 파일 | 경로 | 상태 |
|---|---|---|
| outline.md | research-plan/treasures-talk/260514/outline.md | 작성 완료 |
| meta.yaml | 같은 폴더 | 작성 완료 |
| _selfcheck.md | 같은 폴더 (본 파일) | 작성 완료 |

---

## ① 단계 자체 검수 (지시서 작성 대비)

| # | 점검 항목 | 판정 | 증거·사유 |
|---|---|---|---|
| 1 | wol 주차 인덱스 fetch 실재 확인 | PASS | 1순위 URL `dt/r8/lp-ko/2026/5/11` 작동 확인. 응답에서 성경 읽기 범위 "이사야 60-61장", 10분 연설 제목 "여자야, 일어나서 빛을 비추어라", 본문 링크 `/pc/r8/lp-ko/202026162/1/0`, 노래 146·156·119, 삽화 mwb26/2026/174 모두 추출. |
| 2 | 10분 연설 본문 페이지 fetch | PARTIAL | 한국어 본문 페이지(`/pc/r8/lp-ko/202026162/1/0`) 다수 timeout. 영문 cross-check (`/en/wol/d/r1/lp-e/202026162`) 로 요점 3개·각 성구·참조 출판물(w24.07 30 ¶1-2 / ¶3-4 / ¶5–31 ¶2) 정확 추출 성공. 한국어 약어는 표준 매핑 (`「파24.07」 30면 N항`) 적용. 낭독 본문 verbatim 은 scripture-deep 가 ② 단계에서 wol nwtsty 직접 재조회 후 정본 확정 — outline.md 의 잠정 본문에 [확인 필요] 표기 완료. |
| 3 | 요점 3개 정확 반영 | PASS | wol 지정 그대로 — (1) 여자=고대 예루살렘 / (2) 부분 성취 / (3) 위에 있는 예루살렘 더 큰 성취. 임의 재서술 없음. |
| 4 | 출력 폴더명 결정 | PASS | 작업 워크스페이스에 기존 `2605` 폴더가 `260504-0510`(next1) 만 존재 → 일관성 확보 위해 next2 도 동일 패턴 `260511-0517` (월-일) 신규 채택. meta.yaml `output_folder_name` 명시. |
| 5 | meta.yaml 필수 키 전부 포함 | PASS | week_date · week_label · output_folder_name · bible_reading_range · topic · subtopic(빈 문자열 — wol 부제 없음) · points(3) · scripture_refs · wol_publication_refs · research_dirs · output_paths · instructions_to_subresearchers 5종 + common 모두 포함 |
| 6 | 5개 서브 지시서 구체성 | PASS | scripture-deep / publication-cross-ref / illustration-finder / experience-collector / application-builder 모두 (a) 대상 항목 (b) 중점 (c) 우선 (d) 저장 파일명 (e) 피하기 (f) 연결 목표 (g) 공통 의무 6항 포함 |
| 7 | 14축 활용 ≥3축 명시 | PASS | 요점 1: #6 #11 #14 / 요점 2: #6 #7 #5 / 요점 3: #7 + 원어어원(메테르) + #14 — 총 6축 이상, 요점당 1축 이상 |
| 8 | 서론 후크 후보 3~5개 | PASS | A 키루스 원통 #6 / B 도시 야경 #2 / C 70년 유배 회복 #11+#14 / D 자기점검 #10 / E 240개국 1000개 언어 #7 — 5개 |
| 9 | 요점당 예화 후보 2~3개 | PASS | 요점 1: 3개 / 요점 2: 3개 / 요점 3: 3개 |
| 10 | 적절성 8필터 회피 명시 | PASS | "타 종교 도상 X / 정치(이란·이스라엘 분쟁) X / 진화론 긍정 X / 음모론 X / 폭력 X / 출처 불명 X / 비증인 권위 인용 X / 논쟁 현대 사안 X" 모든 서브 지시서에 "피할 것" 항목으로 명시 |
| 11 | 최근 10년 출판물 직접 인용 회피 계획 | PASS | 「파24.07」은 wol 지정 참조이므로 배경 근거로만 사용, 원고 낭독 금지 — outline.md §10 + meta.yaml common §5 에 명시 |
| 12 | 🟢 착수 블록 / 🔴 종료 블록 복사 의무 명시 | PASS | meta.yaml common §2, §3 에 모든 서브가 본인 산출물 최상단 🟢 블록 복사·☑, `_selfcheck.md` 에 🔴 블록 복사·8(9)항목 PASS/FAIL 판정 의무 명시 |
| 13 | 차등 적용표 mid-talk10 행 발췌 인용 | PASS | meta.yaml common §5 에 "14축 ≥3축 / 후크 3~5개 / 예화 2~3개 / 8필터 필수 / 최근 10년 회피 / 삽화 wol 전용" 발췌 |
| 14 | 출력 경로 META 측 절대경로 | PASS | `/Users/brandon/Library/CloudStorage/Dropbox/ClaudeFile/Congregation/research-plan/treasures-talk/260514/` 사용 (META 측). docx 출력 경로는 meta.yaml `output_paths.base` 에 작업 워크스페이스 절대경로로 별도 명시 |
| 15 | 할루시네이션 0 — 확인 못한 것 [확인 필요] 표기 | PASS | (a) 사 60:1, 2 / 갈 4:26 낭독 verbatim 본문 / (b) 삽화 URL `mwb26/2026/174` 정확 패스 — 모두 outline.md 에서 "[확인 필요 — scripture-deep / illustration-finder 가 wol 재조회 후 확정]" 표기 |
| 16 | 상투적 청중 호명·수사 질문 9개 금지 명시 | PASS | outline.md §10 "주의 금기" + meta.yaml application-builder 지시서 "피할 것" 에 §A-4-bis 참조 명시 |

**FAIL 합계**: 0 건 → ① 단계 통과

---

## HIGH 위반 점검 결과

- 없음. ② 단계 (서브 자체 검수) 진행 가능.

---

## 다음 단계 (메인 Claude 에게)

본 ① 단계 산출물(outline.md + meta.yaml) 을 토대로 5개 보조 리서치 에이전트를 병렬 호출:

1. `scripture-deep` → research-bible/260514/
2. `publication-cross-ref` → research-topic/260514/
3. `illustration-finder` → research-illustration/260514/ (intro_image_candidates.json 포함)
4. `experience-collector` → research-experience/260514/
5. `application-builder` → research-application/260514/

각 서브는 본 meta.yaml 의 `instructions_to_subresearchers` 본인 키 + `common_instructions_all_subagents` 를 Read 한 뒤 작업 개시.

---

**판정 (메인 Claude 에게 보고용)**: **GO**

- 모든 필수 산출물 작성 완료
- 16개 점검 항목 전부 PASS
- 잠정 본문 / 삽화 URL 의 [확인 필요] 항목은 ② 단계 서브 (scripture-deep · illustration-finder) 가 재조회 후 정본 확정하도록 지시서에 명시
- 다음 단계 (② 5개 보조 리서치 병렬 호출) 진행 가능

작성: treasures-talk-planner ① 단계 / 2026-04-29
