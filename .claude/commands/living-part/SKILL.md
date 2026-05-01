---
name: living-part
description: 주중집회 **그리스도인 생활 파트 (CBS·회중의필요 제외)** 원고 1건을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3`. **6단 방어(v2) 프로토콜(`.claude/shared/multi-layer-defense.md`)** 준수. WOL 에서 subtype 자동 파싱 (living_talk / living_discussion / living_video / living_interview / living_qna 5종). living-part-planner → subtype별 보조 리서치 병렬 → Planner 재검수 → living-part-script → Planner 재검수 → docx → fact-checker·jw-style-checker·timing-auditor·quality-monotonic-checker 최종 감수. 결과 `그리스도인 생활_{제목}_YYMMDD.docx`. 트리거 "/living-part", "생활 파트 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# living-part — 그리스도인 생활 파트 (단일 주차, 6단 방어(v2))

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx (빌더 작성 후 PDF 자동 추가 예정)

## 이 스킬의 범위
- 주차 교재 "그리스도인 생활" **한 파트** 원고
- 회중의 필요는 `/local-needs`, CBS 는 `/cbs`
- subtype 5종 자동 분기:
  - `living_talk` · `living_discussion` · `living_video` · `living_interview` · `living_qna`

## 🛡 품질 원칙 — 6단 방어(v2) 프로토콜
`.claude/shared/multi-layer-defense.md` 준수. 실행 전 Read.
**4단**: ① Planner 지시서 → ② 서브 자체 검수 → ③ Planner 재검수 → ④ 3종 최종 감사

## 인자 규약
`now|next1|next2|next3`

## ⚠ WOL-first 수집
1. 주차 인덱스 → "그리스도인 생활" 섹션 (CBS·local_needs 제외) 파트 개수 확인
2. 2개 이상이면 원준님께 선택 질문
3. 파트 제목·부제·시간·형식·참조 WOL verbatim
4. `living_video` 면 비디오 URL·길이 수집

## 🚫 할루시네이션 금지 (공통)
공식 출판물 확인분만. `[확인 필요]`. 출처 URL. verbatim. 경험담 게재분만.

모든 Agent 말미:
> ⚠ 할루시네이션 금지 / ⚠ 6단 방어(v2) 프로토콜 준수

## 📖 저작권
jw.org 공개, 장문 verbatim 허용.

## 저장 위치
베이스: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/03.그리스도인 생활/YYMMDD-MMDD/`
파일명: `그리스도인 생활_{제목}_YYMMDD.docx`

## 실행 단계 (6단 방어(v2))

### 1. 주차 확정 + 파트 선택 (다중 파트면 원준님께 질문)

### 2. 🤖 ① + ② — living-part-planner 1차 (지시서 + subtype 판별)

```
Agent(living-part-planner)
  프롬프트: "{YYMMDD} 생활 파트 '{선택_제목}' 기획 1차 (6단 방어(v2) ①).
  subtype 자동 파싱 (living_talk/living_discussion/living_video/living_interview/living_qna).

  수집:
    - 파트 제목·부제·시간·형식 (WOL verbatim)
    - 참조 자료 (출처 URL)
    - (video) 비디오 URL·길이·내용 요약
    - (interview) 인터뷰이 배경·인터뷰 질문 초안
    - (qna) 질문 목록·짧은 답 포인트

  저장: `research-plan/living-part/{YYMMDD}_{슬러그}/` outline.md + meta.yaml

  meta.yaml: week_date, part_title, part_subtitle, subtype,
             time_minutes, references,
             video_info/interview_info/qna_info (해당 subtype 만),
             research_dirs: {topic, application, experience}/{YYMMDD}/

  ⭐⭐ instructions_to_subresearchers (① 필수):
    subtype 별 필요 서브 지시서:
      - living_talk: publication-cross-ref + application-builder + experience-collector
      - living_discussion: publication-cross-ref + application-builder + qa-designer
      - living_video: publication-cross-ref (비디오 주제 관련 출판물)
      - living_interview: experience-collector (인터뷰이 유형 맞는 경험담 패턴)
      - living_qna: publication-cross-ref + application-builder

  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 3. 🤖 ② — subtype별 보조 리서치 병렬

subtype 에 따라 필요한 서브만 호출. 각 호출 프롬프트에 instructions 인용 + 자체 검수 지시:

```
Agent(publication-cross-ref)
  프롬프트: "meta.yaml + instructions.publication-cross-ref.
  part_title/subtitle 로 wol 횡단 3-5개 단락 (출처 URL).
  research-topic/{YYMMDD}/cross-ref.md + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(application-builder)  [living_talk/discussion/qna]
  프롬프트: "meta.yaml + instructions.application-builder.
  주제 실생활 적용 4축 각 2-3개 + 자기점검.
  research-application/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(experience-collector)  [living_talk/interview]
  프롬프트: "meta.yaml + instructions.experience-collector.
  주제 부합 공식 경험담 2-3개 (출처 URL·실명 주의).
  research-experience/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(qa-designer)  [living_discussion]
  프롬프트: "meta.yaml + instructions.qa-designer.
  토의 질문 + 청중 답변 유도 후속 질문 + 예상 답변 골격.
  research-qa/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 4. 🤖 ③ — living-part-planner 재검수

```
Agent(living-part-planner)  [재검수]
  프롬프트: "해당 서브 산출물 + _selfcheck 전수 Read. subtype별 지시서 대비 A~F 점검.
  `_planner_review_research.md`: PASS | NEEDS-RERUN + 재지시."
```

### 5. 🤖 ① + ② — living-part-script

```
Agent(living-part-script)
  프롬프트: "outline.md + meta.yaml + _planner_review_research.md + research_dirs Read.
  subtype별 포맷:
    [living_talk] 서술형 완성 원고 (서론·요점·결론, 시간 엄수)
    [living_discussion] 사회자 진행 문답 (토의·청중 대기·보강)
    [living_video] 도입 + `[비디오 재생: URL, 길이]` + 토론 질문 + 마무리
    [living_interview] 사회자·인터뷰이 번갈아 + 답변 가이드
    [living_qna] 사회자 Q&A + 짧은 답 포인트

  한 문장 60음절, 담당자·인터뷰이 placeholder.
  research-plan/living-part/{YYMMDD}_{슬러그}/script.md.

  ② 자체 검수: 모든 인용 원본 재조회, _selfcheck_script.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 6. 🤖 ③ — living-part-planner script 재검수

```
Agent(living-part-planner)  [script 재검수]
  프롬프트: "script.md + _selfcheck_script.md Read.
  A. 시간 적정 / B. subtype 포맷 일관 / C. NWT verbatim (성구 있을 때)
  D. topic 논지 근거 / E. 경험담 출처 일치 / F. video URL·길이 정확 (해당 시).
  `_planner_review_script.md`: PASS | NEEDS-REWRITE."
```

### 7. docx 렌더
```bash
python content_living_YYMMDD.py
```
(`build_living_part.py` 추후 작성, subtype 5종 지원)

### 8. 🤖 ④ — 최종 감사 4종 병렬

```
Agent(fact-checker) → research-factcheck/{YYMMDD}/factcheck_living.md
Agent(jw-style-checker) → research-style/{YYMMDD}/
Agent(timing-auditor) → research-timing/{YYMMDD}/ (목표 {time_minutes}분, video 재생 시간 차감)
```
HIGH 1건 이상 → 재빌드 (2회까지).

### 9. 확인 및 보고
- docx/PDF 경로, subtype, 실측 시간, placeholder 확인
- ③ 재검수 통과 + ④ 감수 카운트

## 개정 이력
- 2026-04-24 v2 — 6단 방어(v2) 적용
- 2026-04-23 v1 — living-part-planner/script 2단 초안

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/living-part` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `그리스도인 생활_{제목}_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3`) 호출 시

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
