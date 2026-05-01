---
name: local-needs
description: 주중집회 그리스도인 생활 섹션의 **회중의 필요 (local_needs)** 파트 원고 + 슬라이드를 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3` (없으면 대화형). 원준님께 **자유 형식 multi-line 브리프** (주제·핵심 내용·성구·할 수 있는 것/없는 것·격려·분량) 입력 받아 local-needs-planner 가 **브리프 요약 → 7 카테고리 후보 확장(성구·출판물·적용·경험담·예화·문답·삽화) → 7개 서브 리서치 지시서** 작성 → 7개 보조 리서치 병렬(wol-researcher·scripture-deep·publication-cross-ref·illustration-finder·qa-designer·application-builder·experience-collector, 모두 필수) → Planner 1차 재검수 → planner 가 script.md + slides_plan.json + meta.yaml 생성 → Planner 2차 재검수 → slides-builder 로 pptx → `build_local_needs.py --pdf` 로 docx + PDF 렌더 (legacy 모드 기본) → fact-checker·jw-style-checker·timing-auditor·quality-monotonic-checker 4종 최종 감수. **6단 방어(v2) 프로토콜(`.claude/shared/multi-layer-defense.md`)** 준수. 지부 서신·순회감독자 방문 준비는 범위 제외. 트리거 "/local-needs", "회중의 필요 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# local-needs — 회중의 필요 (단일 주차, 6단 방어 v2 + 풍부한 브리프)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx + pptx (`build_local_needs.py` 빌더 보유, PDF 자동 변환 — 2026-04-25)

## 분류 — 부정기 단독 스킬

**publictalk 와 동급의 부정기 단독 호출 스킬.** `midweek-now/next1/next2/next3` 일괄 스킬에서 자동 호출되지 **않는다**. 사용자가 `/local-needs` 를 직접 입력했을 때만 실행. 진입 시 **장로의회 주제 입력 필수** (대화형 단정형 질문).

## 🎯 이 스킬이 특수한 이유

다른 파트는 WOL 에 주제·성구·요점이 다 있음. 회중의 필요는:
- 입력 = **원준님의 풍부한 자유 형식 브리프** (multi-line)
- 성구·출판물·요점·경험담·예화·적용·문답·삽화 전부 **planner 가 브리프로부터 확장**
- → 보조 리서치 7개 **모두 필수**
- → 브리프 요약 + 지시서 작성이 전체 품질 좌우

## 🛡 품질 원칙 — 6단 방어(v2) 프로토콜

모든 에이전트 호출은 `.claude/shared/multi-layer-defense.md` 준수. 실행 전 Read.

**6단 요약**:
- ① Planner 1차 (브리프 요약 + 7 카테고리 확장 + 7개 서브 지시서 작성)
- ② 7개 리서치 병렬 (지시서 따라 + 자체 검수)
- ③ Planner 1차 재검수 (리서치 결과 검토)
- ④ Planner 자체 작성 (script.md + slides_plan.json + meta.yaml)
- ⑤ Planner 2차 재검수 (자체 작성 검증 — 브리프 충실성·옛 형식·격려·적용·성구·분량)
- ⑥ 최종 감수 3종 (fact-checker · jw-style-checker · timing-auditor)

## 이 스킬의 범위
- 회중의 필요 한 편 원고 + PPT 한 세트
- **제외**: 지부 서신·순회감독자 방문 준비
- 다른 생활 파트는 `/living-part`, CBS 는 `/cbs`

## 인자 규약
`now|next1|next2|next3` (없으면 대화형)

## 0. 실행 전 필수 입력 — 풍부한 브리프 (자유 형식 multi-line)

진입 시 원준님께 자유 형식 multi-line 입력을 받는다 (단정형·메뉴 나열 X, 풍부하게 받기):

```
"이번 회중의 필요 — 어떻게 만들고 싶으세요?
 - **주제**: 한 줄 또는 짧은 설명
 - **핵심 내용**: 다루고 싶은 항목들 (자유롭게 나열)
 - **성서 구절**: 떠오르는 성구 또는 '없으면 찾아줘'
 - **할 수 있는 것 / 없는 것** (적용 가이드라인)
 - **격려 (선택)**: 강조할 축복·약속
 - **분량**: 시간 (기본 15분)

 주제만 알려주시면 (취지 살려) 클로드가 나머지 구조도 만들 수 있어요."
```

원준님 응답 = **풍부한 브리프 텍스트**. 다음 단계의 planner 가 이걸 받아 구조화.
주제만 와도 planner 가 브리프 확장.

### 예시 입력 (실제 케이스 — 2026-04-25 원준님 지시)

> "다음 주는 회중에서 야외봉사할 때 우리가 '오늘의 봉사' 라는 앱을 사용해.
>  그 앱을 사용할 때 개인정보 보호법에 위배되지 않도록 조심해야 한다는 내용.
>  관련 내용:
>    - 개인정보 보호법에 어떤 것들이 민감한지
>    - 야외봉사할 때 어떤 것들을 조심해야 하는지
>    - 성서 구절 (성경 말씀처럼 법을 잘 준수)
>    - 직접적으로 할 수 있는 것 / 할 수 없는 것
>  격려: 이런 것에 힘쓸 때 어떤 축복이 있는지"

planner 는 이 브리프를:
1. 1줄 요약 + 5~7개 핵심 항목 + 강조점 + 분량으로 구조화
2. 7개 서브에이전트 각각에 "전체 흐름 + 너의 역할 + 너에게 해당하는 브리프 발췌" 지시서 작성
3. 7개 병렬 리서치 호출 → 1차 재검수 → script 작성 → 2차 재검수

## ⚠ WOL-first 보조 수집
주제 관련 공식 출판물·파수대·회중 관리서 wol 교차 검색. 성구·인용 verbatim.

## 🚫 할루시네이션 금지 (공통)
1. 주제는 원준님 제공 그대로
2. 성구·출판물 wol 원문 verbatim
3. 회중 특정 사건·인물은 eldership_context 범위 내만
4. 경험담 공식 출판물 게재분만
5. [확인 필요] placeholder 허용

모든 Agent 프롬프트 말미:
> ⚠ 할루시네이션 금지 / ⚠ 6단 방어(v2) 프로토콜 준수

## 📖 저작권
jw.org 공개 자료, 장문 verbatim 허용 (2026-04-22).

## 저장 위치 (정본: output-naming-policy.md §1·§2)

```
베이스: ~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/04.회중의 필요/{YYMMDD-MMDD}/
산출물: 회중의 필요_{주제}_YYMMDD.docx
        회중의 필요_{주제}_YYMMDD.pdf      (build_local_needs.py 자동 변환)
        회중의 필요_{주제}_YYMMDD.pptx     (slides-builder 가 별도 작성)
```

빌더: `~/Claude/Projects/Congregation/_automation\build_local_needs.py`
- 기본 모드 = `legacy` (원준님 옛 형식 — 평문 산문, 인라인 시간 마커, 노랑 하이라이트 키 구문)
- 옵션 = `modern` (PASTEL 박스·4축·아이콘 라벨)
- spec 의 `style` 필드로 분기. 누락 시 legacy.

> **표준 패턴**: ver4 검증 패턴 + 어르신 친화 큰 글자 (제목 48pt·본문 32pt·작은글씨 16pt italic 회색 #6E6E6E) — `local-needs-planner.md` §"🏆 ver4 검증 표준 패턴" 따름. 능동 톤 + 5단 흐름 + 할 수 없는 것 목록화 + 법 사유 표기 + pptx 6장.

## 실행 단계 (6단 방어 v2)

### 0. 풍부한 브리프 대화형 입력 (위 §0 참조)

### 0-bis. 원준님 스타일 옛 자료 참고 (필수)

`local-needs-planner` 는 진입 직후 다음 두 docx 를 Read 해 형식 패턴을 학습한다.

```
~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/04.회중의 필요/
├── 250328\야외봉사의 목적을 달성하는데 지원하는 방법_김원준20250328.docx
└── 250516\후대를 나타태십시오_김원준250512.docx
```

추출 항목 (planner 가 instructions 와 script 작성에 직접 반영):

- **구조**: 도입 (성구·비유·질문) → 요점 1·2·3 (각 요점 끝에 시간 마커 인라인) → 결론 (요점 재요약 + 격려 + 종료 마커)
- **시간 마커**: 본문 안에 인라인 우측정렬 빨강 볼드 (`1'50"` `4'20"` `6'` `8'10"` `9'30"`). 섹션 박스·헤더 사용 안 함.
- **노랑 하이라이트**: 단락 안 핵심 어구만 부분적으로 (전환어 `첫째로/두번째로/세번째로/마지막으로` 항상 노랑 + 볼드).
- **성구**: 좌측 들여쓰기 (약 0.4~0.5") 단락. 박스·배경 X. 본문 그대로 한 단락. 신세계역 verbatim.
- **톤**: 1인칭 복수 ("우리"), 직접 청중에게 묻는 빈도 적음 (의문문은 후크에서만).
- **인용**: 성구 verbatim 1~2회, 출판물 인용 (파·통·익) 0~1회. 최소.
- **적용**: 4축 (가정·봉사·회중·개인) 라벨링 **없음** — 결론 산문 안에 자연스럽게 통합.
- **경험담**: 한 단락 짧게 (성서 인물 + 현대 경험 1).
- **결론 호소**: "함께 …합시다" / 격려 문장 + 마지막 시간 마커.

→ 새 docx 는 **legacy 모드** (`spec.style = "legacy"`) 로 빌더에 전달, 옛 형식 그대로 재현.

### 1. 주차 확정 + 폴더

### 2. 🤖 ① — local-needs-planner 1차 (브리프 요약 + 7 카테고리 확장 + 7 서브 지시서)

```
Agent(local-needs-planner)  [1차 — 브리프 요약 + 주제 확장]
  프롬프트: "{YYMMDD-MMDD} 회중의 필요 기획 1차 (6단 방어 v2 단계 ①).

  원준님 브리프:
  ---
  {원준님이 입력한 multi-line 텍스트 그대로}
  ---

  ⭐⭐ 단계 ① 브리프 요약 (필수):
    - 1줄 주제 요약
    - 5~7개 핵심 항목 추출
    - 강조점 (격려·축복)
    - 분량 시간 (기본 15분)
    - 전체 흐름 다이어그램 (도입 → 요점 1·2·3 → 결론)

  ⭐⭐ 단계 ② 옛 자료 참고 (필수, §0-bis):
    250328 + 250516 docx 두 개 Read 해 형식 패턴 학습.
    인스트럭션·script 작성에 형식 가이드 그대로 반영.

  ⭐⭐ 단계 ③ 주제 확장 — 7 카테고리 후보 각 3~5개 meta.yaml 기록:
    1. candidate_scriptures: [{ref, url, why}] — 브리프 명시 성구 + 추가 후보
    2. candidate_publications: [{약어, 제목, 호수, 면, url}] — 파수대·회중관리서 등
    3. candidate_applications_by_axis: {가정,봉사,회중,개인: [...]}
       — 브리프의 "할 수 있는 것 / 없는 것" 반영
    4. candidate_experiences: [{출처, 요약, url}]
    5. candidate_illustrations: [{출처, 요약}]
    6. candidate_qa_blocks: [{질문, 응답 가이드}] — 청중 응답 문답 후보
    7. candidate_wol_images: [{wol_url, src, caption}] — 종교적 삽화 (wol 만)

  ⭐⭐ 단계 ④ instructions_to_subresearchers (필수):
    7개 서브에이전트 각각에 다음 템플릿으로 지시서 작성 →
      [전체 요약]: 1줄 + 5~7개 핵심 항목
      [너의 역할]: 너가 담당할 부분 + 무엇을 산출해야 하는지
      [원준님 브리프 발췌]: 너에게 해당하는 부분만
      [출력 형식]: research-{TYPE}/{YYMMDD-MMDD}/local-needs/ 에 ...
    7개 서브: wol-researcher · scripture-deep · publication-cross-ref ·
             illustration-finder · qa-designer · application-builder · experience-collector

  저장: `research-plan/local-needs/{YYMMDD}_{슬러그}/` 에
        meta.yaml + outline.md + brief_summary.md (브리프 요약)
  ⚠ 할루시네이션 / 6단 방어 v2."
```

### 3. 🤖 단계 ② — 7개 보조 병렬 (전부 필수, 지시서 수신 + 자체 검수)

`public-talk-builder` 만 제외 — 공개강연 전용. 나머지 7개 리서치 에이전트 병렬 호출.

```
Agent(wol-researcher)
  프롬프트: "meta.yaml + instructions.wol-researcher 준수.
  ⓐ 그 주차 wol 주변 자료 (생활과 봉사 페이지 → local_needs 블록 권장 시간·참조)
  ⓑ 주제 키워드 wol 검색 → 상위 출판물 페이지 5~10개 URL 수집
  ⓒ 종교적 삽화 후보 — wol 페이지 안 이미지 src URL 수집 (외부 종교화 절대 금지, wol 만)
  research-wol/{YYMMDD}/ 저장.
  ② 자체 검수: 모든 URL 재조회 200 OK 확인, _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어 v2."

Agent(scripture-deep)
  프롬프트: "meta.yaml + instructions.scripture-deep 준수.
  candidate_scriptures 우선 2~3개 심화 (신세계역 verbatim·연구 노트·상호 참조·원어).
  research-bible/{YYMMDD}/ 저장.
  ② 자체 검수: wol URL 재조회 글자 대조, _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어 v2."

Agent(publication-cross-ref)
  프롬프트: "meta.yaml + instructions.publication-cross-ref 준수.
  candidate_publications 확인 + wol 횡단 5-8개 단락 (「파」·「익」·「통」·「예-1」, 출처 URL).
  research-topic/{YYMMDD}/cross-ref.md + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어 v2."

Agent(illustration-finder)
  프롬프트: "meta.yaml + instructions.illustration-finder 준수.
  텍스트 예화·비유 candidate_illustrations 2~3개 선정 + 일차 자료 교차 검증.
  + wol-researcher ⓒ 가 수집한 종교적 이미지 URL 후보 검증 (종교성 이진 판정 통과만).
  research-illustration/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어 v2 / 외부 종교 그림 절대 금지."

Agent(qa-designer)
  프롬프트: "meta.yaml + instructions.qa-designer 준수.
  회중의 필요는 종종 청중 응답을 받는다. 주제 관련 문답 2~3 블록 설계
  (질문 → 청중 응답 받기 → 핵심 답 정리 → 적용). 가정/회중/야외봉사 3 라벨.
  research-qa/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어 v2 / 자연스러운 실천 (과도한 설계 금지)."

Agent(application-builder)
  프롬프트: "meta.yaml + instructions.application-builder 준수.
  candidate_applications_by_axis 실전 시나리오 구체화 (축별 2-3 + 자기점검).
  ※ 옛 docx 는 4축 라벨링을 명시적으로 쓰지 않음 — script 작성 시 산문 안에 통합.
     application-builder 는 4축 자료를 그대로 만들고, planner 가 script 작성 단계에서 풀어 통합.
  research-application/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어 v2."

Agent(experience-collector)
  프롬프트: "meta.yaml + instructions.experience-collector 준수.
  candidate_experiences 원문 확인 + 주제 관련 공식 경험담 1~2개 추가 (출처 URL·실명 주의).
  research-experience/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어 v2."
```

### 4. 🤖 단계 ③ — local-needs-planner 2차 (리서치 1차 재검수)

```
Agent(local-needs-planner)  [2차 — 재검수]
  프롬프트: "7개 서브 산출물 + _selfcheck.md 전수 Read.
  meta.yaml 지시서 + candidate_* 대비 점검:
    A. 중점 반영 / B. 피하기 항목 회피 / C. _selfcheck 통과
    D. 5 카테고리 균형 / E. 주제 초점 유지 / F. 모순 없음
  결과 `_planner_review_research.md`: PASS | NEEDS-RERUN + 재지시."
```

`NEEDS-RERUN` → 해당 서브 1회 재호출.

### 5. 🤖 단계 ④ — local-needs-planner 3차 (script + slides_plan + meta.yaml 작성)

```
Agent(local-needs-planner)  [3차 — script 작성]
  프롬프트: "PASS 됐다. 완성 원고 + 슬라이드 사양 산출.
  Read: meta.yaml · outline.md · _planner_review_research.md ·
        research-{bible,topic,application,experience,illustration}/{YYMMDD}/ (+ _selfcheck)

  산출 2파일:
    1. script.md — 장로 낭독용 완성 원고 (10~15분)
       구조: 도입(주제·관심 유발) → 성구 2~3개 해설 → 4축 적용 → 경험담·예화 → 결론·실천 권고
       한 문장 60음절, 구어체
    2. slides_plan.json — 슬라이드 시퀀스
       {'slides': [{title/bullets/scripture/image/quote/takeaway} 유형]}

  ② 자체 검수: 모든 성구·인용·경험담 원본 재조회 대조.
  _selfcheck_script.md 작성.
  ⚠ 할루시네이션 / 6단 방어 v2. eldership_context 범위 내."
```

### 6. 🤖 단계 ⑤ — local-needs-planner 4차 (script 2차 재검수, 자체 작성 검증)

```
Agent(local-needs-planner)  [4차 — script 2차 재검수, 단계 ⑤]
  프롬프트: "script.md + slides_plan.json + meta.yaml + brief_summary.md +
        _selfcheck_script.md Read.
  자체 작성 검증 체크리스트 (6단 방어 v2 단계 ⑤):
    A. 원준님 브리프의 모든 핵심 항목 5~7개 반영됐는가?
    B. 옛 docx 형식 (인라인 시간 마커·노랑 하이라이트·평문 산문) 재현됐는가?
    C. 격려 부분이 결론에 자연스럽게 들어갔는가?
    D. 적용 ('할 수 있는 것 / 없는 것') 이 명확한가?
    E. 성구 신세계역 verbatim 인가?
    F. 분량 시간 ({time_minutes}분, 보통 15분) 맞는가?
    G. 슬라이드-원고 동기화 (notes = 섹션 전문)
    H. 주제 초점 유지 / I. 경험담 출처 일치
    J. spec.style = 'legacy' 명시
  결과 `_planner_review_script.md`: PASS | NEEDS-REWRITE + 수정 지시."
```

`NEEDS-REWRITE` → planner 3차 재호출 (1회).

### 7. 🤖 slides-builder 호출

```
Agent(slides-builder)
  프롬프트: "research-plan/local-needs/{YYMMDD}_{슬러그}/ 의
  slides_plan.json + script.md + meta.yaml Read, python-pptx 로 slides.pptx 렌더.
  공용 템플릿 `research-plan/slides/_template.pptx` 사용.
  출력: slides.pptx + build_log.md.
  자체 요약·윤문 금지."
```

### 8. 최종 복사 + docx 렌더 (build_local_needs.py)

1. slides.pptx → `회중의 필요_{주제}_YYMMDD.pptx` 로 복사 (output-naming-policy §1·§2 경로)
2. script.md → `content_local_needs_{YYMMDD}.py` SPEC dict 생성 (`style="legacy"` 기본)
3. 빌더 실행 — **legacy 모드 기본 (옛 형식)**:

```bash
python build_local_needs.py spec.py out.docx --pdf
```

   - 기본 모드 = `legacy` (옛 형식, 평문 산문·인라인 시간 마커·노랑 하이라이트)
   - `--mode modern` 인자 = modern 모드 (PASTEL 박스·4축 명시·아이콘 라벨)
   - spec 의 `style` 필드로 분기. 누락 시 legacy.
   - `--pdf` 옵션 = docx + PDF 동시 자동 생성

   → `회중의 필요_{주제}_YYMMDD.docx` + `.pdf` 자동 생성

### 9. 🤖 단계 ⑥ — 최종 감사 4종 병렬

```
Agent(fact-checker) → research-factcheck/{YYMMDD}/factcheck_local_needs.md
Agent(jw-style-checker) → research-style/{YYMMDD}/
Agent(timing-auditor) → research-timing/{YYMMDD}/  (목표 {time_minutes}분)
```
HIGH 1건 이상 → 재빌드 (2회까지).

### 10. 확인 및 보고
- docx + pptx 경로, 슬라이드 매수
- ③ 재검수 통과 + ④ HIGH/MEDIUM/LOW 카운트
- 담당 장로 placeholder

## 개정 이력
- 2026-04-25 v4 — **6단 방어(v2) + 풍부한 자유 형식 multi-line 브리프 입력** + planner 브리프 요약 의무 + 7개 서브 지시서 템플릿 ([전체 요약]·[너의 역할]·[브리프 발췌]·[출력 형식]) + planner 2차 재검수 체크리스트 (브리프 충실성·격려·할 수 있는 것/없는 것) + 빌더 `--pdf` 명시 + 예시 (야외봉사 앱 + 개인정보 보호법) 본문 포함
- 2026-04-25 v3 — 원준님 옛 형식 (legacy) 빌더 정정 + §0-bis 옛 자료 참고 + 7개 리서치 (wol·qa 추가) + 7카테고리 확장 + style=legacy 기본 + 분류 (단독 부정기 스킬) 명시
- 2026-04-24 v2 — 6단 방어(v2) + 주제 확장 5카테고리 + 보조 리서치 5개 필수
- 2026-04-23 v1 — 초안

---

## 산출물 존재 시 skip 정책 (필수)

이 스킬은 **단독 호출 전용** — 일괄 스킬(midweek-*) 의 11개 파트에 포함되지 않으므로 일괄 컨텍스트는 적용 안 된다.

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `회중의 필요_{주제}_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3 + `.claude/shared/output-naming-policy.md` §4·§4-bis.

---

## 서론 이미지 옵션 (2026-04-25 보강)

빌더 spec dict 에 다음 키를 선택적으로 추가하면 도입 마지막 단락 직후 이미지가 임베드된다:

```python
spec = {
    ...
    "intro_image_path": "C:/path/to/intro.jpg",   # 선택
    "intro_image_caption": "도입 삽화 — '오늘의 봉사' 앱 화면",  # 선택
    "intro_image_width": 4.0,                      # 선택 (기본 4.0 인치)
    ...
}
```

후보는 illustration-finder 의 `intro_image_candidates.json` 산출물에서 가져온다 (planner 가 매핑).

> **마크업 체크리스트**: 각 에이전트는 자기 폴더 `_progress.md` 에 체크박스로 진행 표시. 정책: `.claude/shared/markdown-checklist-policy.md`.
