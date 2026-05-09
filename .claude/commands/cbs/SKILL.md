---
name: cbs
description: 주중집회 ⑩번 "회중성서연구 사회 (30분)" 원고 1편을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3` (없으면 대화형). **6단 방어(v2) 프로토콜(`.claude/shared/multi-layer-defense.md`)** 준수 — ① Planner 가 지시서 전달 → ② 각 서브 자체 검수 → ③ Planner 재검수 → ④ fact-checker·jw-style-checker·timing-auditor·quality-monotonic-checker 최종 게이트. cbs-planner → 4개 보조(qa-designer·scripture-deep·publication-cross-ref·application-builder) + 선택 2개(experience-collector·illustration-finder) → Planner 재검수 → cbs-script → Planner 재검수 → `content_cbs_YYMMDD.py` → `build_cbs.py` 로 docx/PDF. 트리거 "/cbs", "회중성서연구 만들어 줘", "CBS 원고".
---

## 🚨 STAGE 0 — Preflight 의무 (2026-05-03, 4-Layer 신뢰 모델)

```bash
cd ~/Claude/Projects/Congregation/_automation
python3 preflight.py cbs {YYMMDD}
python3 slot_content_inventory.py {YYMMDD} {mwb_doc_url}
```

FAIL → 즉시 정지 (agent 0, 토큰 0). PASS → 카탈로그 저장.

## 🚨 Agent 의무 — content_inventory 사용

planner/script prompt 첫 줄: "의무 Read: `research-illustration/{YYMMDD}/_content_inventory.json` — mwb anchor (paragraphs·videos·scriptures·publications) 따라 골격. 카탈로그 외 자료 X."

설계도면: `research-meta/_ARCHITECTURE.md` §cbs

## 🚨 Layer 4 자동 검증

빌더 build 직후 `verify_docx_against_inventory_auto(out_path, "회중 성서 연구", builder_name)` 자동 호출 — anchor 누락 시 `SeedImageHardFail`.

## 🛡️ 팀 에이전트 호출 시 정본 prepend 의무 (2026-05-09 도입)

이 SKILL 이 planner / 보조 / script 에이전트를 Task 로 호출할 때 메인 Claude 는 정본 가이드라인을 prompt 맨 위에 직접 prepend 한다 (Claude Code Task 도구는 hook 으로 prompt augmentation 미지원 검증됨).

```python
# 호출 예시 — 각 에이전트 호출 직전
from team_briefings import get_briefing_for_team, prepend_to_prompt

brief = get_briefing_for_team("cbs")
augmented = prepend_to_prompt(original_prompt, brief)
Agent(subagent_type="cbs-planner", prompt=augmented, ...)
```

또는 CLI:
```bash
python3 _automation/team_briefings.py cbs
```

세부: Congregation/CLAUDE.md "회중 팀 에이전트 호출 시 정본 prepend 의무" 섹션.

## 🔁 직전 주차 중복 회피 (Phase G, 2026-05-09 도입)

⑥ 4종 게이트 직전에 **dedup 검사 의무**:

```bash
python3 _automation/run_dedup_for_slot.py cbs <빌드된 docx 경로>
```

- HIGH 위반 (단락 유사도 ≥ 0.80) → 재작성 권고 (exit 2)
- WARN (≥ 0.65) → 참고 (exit 1)
- 통과 → exit 0

**검사 대상**: 본문 핵심 사례·예화·해설 단락 (사회자 표준 멘트·URL 참조·고정 라벨 자동 제외).
**역할**: 도입 illustration / 결론 한 문장 / 예화가 직전 주차에서 그대로 복제되는 사고 방지.

세부: `_automation/dedup_against_history.py` (라이브러리) + `run_dedup_for_slot.py` (wrapper).

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# cbs — 회중 성서 연구 사회 30분 (단일 주차, 6단 방어(v2))

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx + PDF (자동 변환)

## 이 스킬의 범위
- CBS 사회 원고 **한 편** (한 주차) 만 생성
- 3주치 일괄 생성은 `/midweek-*` 또는 `/weekly` 가 담당
- 다른 주중 파트는 각자 스킬 별도

## 🛡 품질 원칙 — 6단 방어(v2) 프로토콜

**원준님 지침(2026-04-24): 품질 최우선, 오류 0 목표.**

이 스킬의 모든 에이전트 호출은 `.claude/shared/multi-layer-defense.md` 의 6단 방어(v2) 프로토콜에 따른다. 실행 전 반드시 Read.

**4단 요약**:
1. Planner → 각 서브에게 **지시서** (`meta.yaml` 의 `instructions_to_subresearchers`)
2. 서브 **자체 검수** (`_selfcheck.md`)
3. Planner **재검수** (`_planner_review.md`, 미흡 시 재호출)
4. **최종 게이트** — fact-checker + jw-style-checker + timing-auditor

## 인자 규약
`now|next1|next2|next3` (없으면 대화형)

## ⚠ CRITICAL: 콘텐츠 수집 규칙 (WOL-first)

> "wol.jw.org → 집회 → 생활과 봉사 → 해당 주차 → '8. 회중 성서 연구' 링크를 그대로 따라가서 본문 기반 작성"

### 절대 규칙

1. 무조건 WOL 주차 인덱스부터: `https://wol.jw.org/ko/wol/dt/r8/lp-ko/YYYY/M/D`
2. "8. 회중 성서 연구" href 를 직접 따라갈 것. 책·장 범위는 매주 바뀔 수 있음.
   - 스케줄 추론 금지 — href 그대로 (보통 `/pc/r8/lp-ko/YYYYNNNN/14/0`)
   - 링크 가리키는 페이지의 **책 이름·장 번호·장 제목을 먼저 확인** 후 docid 로 본문 수집
3. **장 번호와 책 약어만으로 내용 추측 금지.** (과거 실패: 「훈」 80 ≠ 「예수」 80)
4. chapter URL 이 실제 해당 장을 가리키는지 WOL 응답 제목으로 확인.
5. 타임아웃 → 재시도 3회. 직접 URL 시도 시도 반드시 책 제목·장 제목 WOL 응답에서 확인.

### 현재 사이클 「훈」 책 docid 맵핑 (참고용, 과신 금지)

2026년 4-5월 시점 확인치. 다음 사이클 전환 시 무효.

- 훈 78장 — `1102016088` "예수께서 왕국 소식을 전파하시다"
- 훈 79장 — `1102016089` "예수께서 많은 기적을 행하시다"
- 훈 80장 — `1102016090` "예수께서 12사도를 선택하시다"
- 훈 81장 — `1102016091` "산상 수훈"

⚠ docid 접두사 주의: `1102016XXX` = 「훈」(2016) / `1102014XXX` = 「예수」(2014). 두 책은 주제가 완전히 다름.

### 실패 사례 (절대 반복 금지)

260430 주차 초기 스펙(v1-v3)은 docid 1102014680/81 (「예수」 80-81장: 훌륭한 목자 / 아버지와 하나) 를 「훈」 으로 오인. 실제 「훈」 80-81장은 "12사도 선택" / "산상 수훈". 원인: "8. 회중 성서 연구" 링크를 실제로 따라가지 않고 장 번호만으로 추론.

## 🚫 할루시네이션 절대 금지 (모든 에이전트 공통)

1. wol.jw.org · 신세계역 연구용 성서 · 공식 JW 출판물에서 **실제로 확인한 내용만**.
2. 확인 못 한 항목 `[확인 필요]` placeholder.
3. 모든 인용 출처 URL + 출판물 이름 + 호수/면/항 포함.
4. 성구 신세계역 연구용 verbatim.
5. 경험담 공식 출판물 게재분만.
6. 예화·비유 출처 명시.
7. **「훈」 docid 접두사 오인 금지** — `1102016XXX` 만 사용.

모든 Agent 호출 프롬프트 말미에 공통 문구 첨부:

> ⚠ 할루시네이션 절대 금지: 훈련 기억이 아니라 wol.jw.org·공식 출판물에서 실제 확인한 내용만. 확인 못 한 건 `[확인 필요]`. 모든 인용에 출처 URL + 호수/면/항. 성구 verbatim.
>
> ⚠ 6단 방어(v2) 프로토콜 준수: `.claude/shared/multi-layer-defense.md` 를 먼저 Read 해서 당신의 역할 단계 확인 후 작업.

## 📖 저작권 정책
jw.org·wol.jw.org 공개 자료로 저작권 고려 없음 (2026-04-22). 장문 verbatim 허용. 출처 URL 필수.

## 저장 위치
베이스: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/05.회중 성서 연구/YYMMDD-MMDD/`

파일명: `회중 성서 연구_훈{장}-{장}_YYMMDD.docx`
- 예: `회중 성서 연구_훈78-79장_260423.docx`
- 재빌드 시 덮어쓰기 (단, 사용자가 "재생성·업그레이드·버전 올려" 명시 시 `_verN_` 부여)
- 파일명에 "김원준" 금지

## 현재 연구용 교재
「훈」 = 「하느님의 교훈이 담긴 성경 이야기」 (2016 출판) — 챕터 2개씩 매주.

⚠ 「훈」 ≠ 「예수」. docid 접두사로 구분: `1102016XXX` / `1102014XXX`.

## 포맷 요소
- 기본 폰트: 맑은 고딕, 14pt
- 장 제목: 중앙 정렬, 14pt 볼드
- 시간 마커: 우측 정렬, 빨강 (FF0000) 볼드 — `4'`, `8'`, `12'`, `16'`, `20'`, `24'`, `28'`
- 강조 성구: 파란색 (2F5496), 볼드
- (필수) 연구 질문: 빨강 볼드 "(필수)" + 검정 볼드 "연구 질문", 노란 하이라이트
- 답변 본문: 14pt

## 실행 단계 (6단 방어(v2) 흐름)

### 1. 주차 확정 + 폴더
인자에서 YYMMDD 계산. 주차 폴더 생성/재사용.

### 2. 🤖 ① + ② 단계 — cbs-planner 호출 (지시서 포함)

```
Agent(cbs-planner)
  프롬프트: "{YYMMDD} 주차 '회중 성서 연구 (30분)' 기획 (6단 방어(v2) ① 단계).
  주차 인덱스에서 '8. 회중 성서 연구' 링크를 따라가 docid 확인 (1102016XXX 「훈」 이어야 함).

  수집:
    (a) 훈 책 장 번호·장 제목 (2개)
    (b) 각 장 문단별 본문 verbatim + 핵심 인용 성구
    (c) (필수) 연구 질문 3-4개
    (d) (선택) 질문
    (e) 관련 삽화 URL

  ⚠ 저장: `research-plan/cbs/{주차}_{교재슬러그}/` outline.md + meta.yaml.

  meta.yaml 필수 키:
    week_date: YYMMDD
    book: '훈'
    chapters: [{num, title, docid}, {num, title, docid}]
    paragraphs: [{chapter, num, text, scriptures: [...]}]
    required_questions: [...]
    optional_questions: [...]
    time_markers: ['4', '8', '12', '16', '20', '24', '28']
    research_dirs:
      qa:           research-qa/{YYMMDD}/
      bible:        research-bible/{YYMMDD}/
      topic:        research-topic/{YYMMDD}/
      application:  research-application/{YYMMDD}/
      experience:   research-experience/{YYMMDD}/
      illustration: research-illustration/{YYMMDD}/

  ⭐⭐ 추가 필수 키 — instructions_to_subresearchers (6단 방어(v2) ① 단계):
    4개 필수 서브(qa-designer·scripture-deep·publication-cross-ref·application-builder) +
    선택 2개(experience-collector·illustration-finder) 에 대한 지시서.
    각 값은 (중점·우선 범위·피하기 항목) 포함 자연어.

  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수.
  ⚠ 당신의 ① 단계 책임은 지시서 작성. 특히 훈 책 docid 접두사 체크를 지시서에 명시 강조."
```

### 3. 🤖 ② 단계 — 4개 필수 + 선택 2개 병렬 (지시서 수신 + 자체 검수)

한 메시지에 Agent 블록 4~6개 동시 호출:

```
Agent(qa-designer)
  프롬프트: "meta.yaml + instructions_to_subresearchers.qa-designer 지시서 준수.
  required_questions/optional_questions 기반 사회용 Q&A 설계.
  각 질문마다 청중 답변 유도용 후속 질문 2-3개, 예상 답변 골격, 사회자 연결 멘트.
  research-qa/{YYMMDD}/cbs-qa.md 저장.

  ② 자체 검수: 공식 질문 원문 vs 작성한 질문 비교. 확장 질문이 원 취지와 맞는지.
  research-qa/{YYMMDD}/_selfcheck.md 작성.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."

Agent(scripture-deep)
  프롬프트: "meta.yaml + instructions_to_subresearchers.scripture-deep 준수.
  paragraphs.scriptures 핵심 성구 각각을 신세계역 연구용 본문·연구 노트·상호 참조·원어·역사 배경.
  research-bible/{YYMMDD}/ 성구별 .md.

  ② 자체 검수: 각 성구 wol 연구용 URL 재조회해서 글자 단위 대조.
  research-bible/{YYMMDD}/_selfcheck.md.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."

Agent(publication-cross-ref)
  프롬프트: "meta.yaml + instructions_to_subresearchers.publication-cross-ref 준수.
  chapters 주제로 wol 출판물 횡단 검색. 파수대·깨어라·통찰·예수책·하느님의 사랑·여호와께 가까이·JW 방송
  관련 단락 5-8개 (출처 URL), research-topic/{YYMMDD}/cross-ref.md.

  ② 자체 검수: 각 인용 URL 재조회 본문 일치 확인.
  research-topic/{YYMMDD}/_selfcheck.md.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."

Agent(application-builder)
  프롬프트: "meta.yaml + instructions_to_subresearchers.application-builder 준수.
  chapters 주제 실생활 적용점 (가정·직장/학교·회중·개인 영성) 축별 2-3개 + 자기점검 질문.
  research-application/{YYMMDD}/cbs-apply.md.

  ② 자체 검수: 공식 출판물 제안 적용은 출처 URL 재확인.
  research-application/{YYMMDD}/_selfcheck.md.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."
```

(선택 — Planner 가 지시서에 포함시킨 경우에만):

```
Agent(experience-collector)
  프롬프트: "(지시서 준수) chapters 주제 관련 공식 경험담 2-3개.
  research-experience/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(illustration-finder)
  프롬프트: "(지시서 준수) chapters 핵심 교훈 예화·비유 각 장당 2-3개.
  research-illustration/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 4. 🤖 ③ 단계 — cbs-planner 재검수

```
Agent(cbs-planner)  [재검수 모드]
  프롬프트: "당신이 지시서를 내린 서브 산출물을 재검수 (6단 방어(v2) ③).

  경로: research-qa/{YYMMDD}/ · research-bible/{YYMMDD}/ · research-topic/{YYMMDD}/ ·
  research-application/{YYMMDD}/ · (선택 시 research-experience·research-illustration)
  및 각 폴더의 _selfcheck.md.

  meta.yaml 의 instructions_to_subresearchers 지시서 대비 점검:
    A. 중점 범위·키워드 반영 여부
    B. 피해야 할 항목 포함 안 됨
    C. 각 _selfcheck 통과 (FAILED 없음)
    D. 2개 장 각각 모든 카테고리 고루 수집
    E. 훈 책 docid 오인 없음 (1102016XXX)
    F. 서로 모순 없음

  결과 `research-plan/cbs/{YYMMDD}/_planner_review_research.md`:
    - 판정: PASS | NEEDS-RERUN
    - 미흡 항목: (항목·이유·재수집 서브·재지시)

  NEEDS-RERUN 이면 재지시사항 구체적으로."
```

`PASS` → 5. `NEEDS-RERUN` → 해당 서브 재호출 (1회).

### 5. 🤖 ① + ② 단계 — cbs-script 호출

```
Agent(cbs-script)
  프롬프트: "research-plan/cbs/{YYMMDD}/outline.md · meta.yaml ·
  _planner_review_research.md 먼저 Read.
  research_dirs 의 폴더와 _selfcheck.md 들을 모두 Read.

  각 장(2개)은 약 15분 분량:
    - 장 제목 (중앙 14pt 볼드)
    - 낭독 진행 도입
    - 첫 낭독 요청 + 시간 마커 `4'`
    - 낭독 본문 (14pt) — 훈 책 본문 요약/핵심 서술 2-3 단락
    - 강조 성구 (파랑 볼드)
    - (필수) 연구 질문 (빨강+검정 볼드)
    - 질문 반복 (14pt 볼드 노랑)
    - 답변 (14pt, 2-3 단락) — qa 예상 답변 + topic 출판물 + application 적용 + (선택) experience/illustration
    - 다음 시간 마커 + 반복

  낭독자는 사회자와 별도 → `[낭독자 {{reader_label}} — 문단 N]` 마커.
  청중 답변 `[청중 대기]` 마커.
  장 2개 합계 30분.

  결과 research-plan/cbs/{YYMMDD}/script.md.

  ② 자체 검수: script 의 모든 성구·출판물 인용·경험담을 원본 재조회 대조.
  research-plan/cbs/{YYMMDD}/_selfcheck_script.md 작성.

  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."
```

### 6. 🤖 ③ 단계 — cbs-planner script 재검수

```
Agent(cbs-planner)  [script 재검수 모드]
  프롬프트: "script.md 와 _selfcheck_script.md Read. outline.md 대비 점검:
    A. 2장 모두 완전 15분 분량 + 시간 마커 정확
    B. 성구 인용 신세계역 연구용 verbatim
    C. (필수) 연구 질문 원문 그대로
    D. 답변이 research-topic 실제 논지 근거 (창작 아님)
    E. 훈 책 본문 왜곡 없음

  결과 `research-plan/cbs/{YYMMDD}/_planner_review_script.md`:
    - 판정: PASS | NEEDS-REWRITE
    - 수정 필요 단락: (단락·이유·수정 방향)
    - NEEDS-REWRITE 이면 script 에게 전달할 구체 수정 지시."
```

### 7. content_cbs_YYMMDD.py 자동 변환 (헬퍼)

```bash
cd ~/Claude/Projects/Congregation/_automation
python3 script_to_content_cbs.py {YYMMDD}
```

헬퍼가 `script.md` + `meta.yaml` → SPEC dict 자동 변환. Agent 호출 불필요. 회귀 테스트 골든 (260514·260521·260528) 으로 검증된 매핑 사용.

**자동 추출되는 필드** (구조적·verbatim):
- `version`, `doc_intro_topic`, `doc_intro_reader` (READER placeholder)
- `chapters[].title`, `is_first`, `timers` (8개 표준 시간 마커)
- `chapters[].reading_paragraphs` (meta.yaml verbatim, smart-quote 변환)
- `chapters[].key_scripture.{quote,ref,url}` (url 은 nwtsty 자동 생성)
- `chapters[].required_question.question` (script.md 노란박스)
- `chapters[].required_question.answer_items` (청중 답변 + 사회자 보강 첫째/둘째/셋째 split)
- `chapters[].illustration.scenes[].{question,image_path}` (image_path 는 `lfb_{N}_{seq}.jpg` 자동 생성)
- `chapters[].thanks_line` (chapter[1] 만, READER placeholder)
- `chapters[].transition_out`, `next_chapter_reading_prompt` (chapter[0] 만)

**합성이 필요한 필드** (헬퍼는 best-effort 후 검수 권고 — script.md 에 1:1 매칭 안 됨):
- `extra_deep_points` — 사회자 보강의 핵심 단락 정리
- `scripture_commentary[].relation` — 성구별 해설
- `reference_materials` — 출판물 인용 표를 SPEC 형식으로 (`label`/`url`/`summary` 3필드)
- `illustration.scenes[].bg_text` — 삽화 묘사 + 캡션 결합
- `illustration.short_application` — 두 삽화 통합 적용
- `takeaway.q1_scripture_lesson` / `q2_about_jehovah` — 참조 성구·여호와 정리

새 패턴 등장 시 `_automation/test_script_to_content_cbs.py` 골든 추가 후 헬퍼 보강. 회귀 결과는 `python3 test_script_to_content_cbs.py` 로 확인.

⚠️ 합성 필드는 cbs-script Agent 의 prose 와 SPEC 의 prose 가 다르게 큐레이션된 경우가 있어 fully-automatic 1:1 변환은 **현재 60-72% 매치**. 나머지는 메인 Claude 의 검수·정정으로 채움.

### 8. docx/PDF 렌더

```bash
cd "~/Claude/Projects/Congregation/_automation"
python content_cbs_YYMMDD.py
```

(`build_cbs.py` 가 docx + PDF 동시 생성)

### 9. 🤖 ④ 단계 — 최종 통합 감사 (4종 병렬)

```
Agent(fact-checker)
  프롬프트: "{docx_path} script.md 성구 verbatim · 출판물 인용 실존 · URL 유효성 ·
  경험담 출처 독립 검증. research-factcheck/{YYMMDD}/factcheck_cbs.md 저장.
  특히 훈 책 docid 접두사 확인 (1102016XXX).
  ⚠ 훈련 기억 금지, WebFetch 로 원본 재조회."

Agent(jw-style-checker)
  프롬프트: "{docx_path} 감수.
  금칙어 + 신세계역 표기 + 경어체 + 높임법 + 정치 중립.
  research-style/{YYMMDD}/ 저장."

Agent(timing-auditor)
  프롬프트: "{docx_path} 시간 시뮬레이션. 목표 30분(1800초) 대비.
  research-timing/{YYMMDD}/ 저장."
```

HIGH 위반 1건 이상 → 재빌드 강제. 2회까지.

### 10. 확인 및 보고
- docx/PDF 경로
- ③ 재검수 통과 + ④ 최종 감수 HIGH/MEDIUM/LOW 카운트
- 재빌드 횟수

## 기억할 점
- **30분 분량** — 훈 책 2장 (4'+8'+12'+16' = 1장, 20'+24'+28' = 2장)
- 시간 마커 필수, 빨강 볼드
- 성구 파란색 (2F5496)
- (필수) 연구 질문 명시
- 훈 책 docid 접두사 `1102016XXX` 체크

## 개정 이력
- 2026-04-24 v2 — 6단 방어(v2) 프로토콜 적용
- 2026-04-23 v1 — cbs-planner/script 2단 체인 초안 (mid-study3 이관)

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/cbs` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `회중 성서 연구_훈{장}_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3` 또는 `mid-study3`) 호출 시

일괄 스킬이 묶음 확인 단계에서 이미 yes/no 받았으므로 **자체 단정형 확인 묻지 않는다**. 일괄에서 받은 결정 그대로 실행:

- **skip 결정** → 호출 자체가 발생 안 함 (일괄이 이미 걸러냄)
- **신규 빌드** → 정상 진행
- **`--from-batch=ver_up`** 컨텍스트 받으면 → `_verN_` (N = 디스크 최대 + 1) 자동 부여

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
