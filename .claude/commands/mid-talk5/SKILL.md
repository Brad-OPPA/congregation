---
name: mid-talk5
description: 주중집회 야외봉사 섹션 마지막 **5분 연설 (apply_talk)** 원고 1건을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3`. **6단 방어(v2) 프로토콜(`.claude/shared/multi-layer-defense.md`)** 준수. student-talk-planner → 5개 보조 리서치 필수(scripture-deep·publication-cross-ref·illustration-finder·experience-collector·application-builder) → Planner 재검수 → student-talk-script → Planner 재검수 → docx/PDF → fact-checker·jw-style-checker·timing-auditor·quality-monotonic-checker 최종 감수. 회중 전체 대상 격려·권면 톤 2~5분 서술형. S-38-KO 11항 **남학생만**. 결과 `5분 연설_{주제}_YYMMDD.docx`. 트리거 "/mid-talk5", "5분 연설 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# mid-talk5 — 야외봉사 5분 연설 (단일 주차, 6단 방어(v2))

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx + PDF (자동 변환)

## 이 스킬의 범위
- 야외봉사 마지막 5분 연설 **한 건**
- 담당자 **남학생** (S-38-KO 11항) — 회중 전체 대상 격려
- 학생 실연/낭독은 `/mid-student1~4`

## 🛡 품질 원칙 — 6단 방어(v2) 프로토콜
`.claude/shared/multi-layer-defense.md` 준수. 실행 전 Read.
**4단**: ① Planner 지시서 → ② 서브 자체 검수 → ③ Planner 재검수 → ④ 3종 최종 감사

## 인자 규약
`now|next1|next2|next3`

## ⚠ WOL-first 수집
1. 주차 인덱스 → "집회 → 생활과 봉사 → 야외봉사 → 5분 연설" href
2. 주제·부제·핵심 성구·요점 WOL verbatim
3. 시간 5분 (3~5분) WOL 원문 따르기

## 🚫 할루시네이션 금지 (공통)
공식 출판물 확인 내용만. `[확인 필요]`. 출처 URL 필수. 성구 verbatim. 경험담 게재분만.

모든 Agent 말미:
> ⚠ 할루시네이션 금지 / ⚠ 6단 방어(v2) 프로토콜 준수

## 📖 저작권
jw.org 공개, 장문 verbatim 허용.

## 저장 위치
베이스: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/02.야외 봉사에 힘쓰십시오/02.5분 연설/YYMMDD-MMDD/`
파일명: `5분 연설_{주제}_YYMMDD.docx`

## 실행 단계 (6단 방어(v2))

### 1. 주차 확정 + 폴더

### 2. 🤖 ① + ② — student-talk-planner 1차 (지시서 포함)

```
Agent(student-talk-planner)
  프롬프트: "{YYMMDD} 5분 연설(apply_talk) 기획 1차 (6단 방어(v2) ①).
  주차 인덱스에서 주제·부제·핵심 성구·요점 1~2개·참조 자료 수집.
  서론(30초)·요점(각 1.5~2분)·결론(30초) 아웃라인.

  저장: `research-plan/student-talk/{YYMMDD}/` outline.md + meta.yaml
  meta.yaml: week_date, topic, subtopic, key_scripture, points[1~2],
             references, time_minutes=5, gender_restriction=male_only,
             research_dirs: {bible,topic,illustration,experience,application}

  ⭐⭐ instructions_to_subresearchers (① 필수):
    5개 서브(scripture-deep·publication-cross-ref·illustration-finder·
           experience-collector·application-builder)에게 지시서.
    특히 야외봉사 격려·권면 톤에 맞는 재료에 집중.

  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 3. 🤖 ② — 5개 보조 병렬 (모두 필수)

```
Agent(scripture-deep)
  프롬프트: "meta.yaml + instructions.scripture-deep.
  key_scripture 심층 (NWT verbatim·연구 노트·상호 참조·원어).
  research-bible/{YYMMDD}/ + _selfcheck.md. ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(publication-cross-ref)
  프롬프트: "meta.yaml + instructions.publication-cross-ref.
  topic 으로 wol 횡단 (파수대·통찰·하느님의 사랑·JW 방송) 단락 3-5개.
  research-topic/{YYMMDD}/cross-ref.md + _selfcheck.md. ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(illustration-finder)
  프롬프트: "meta.yaml + instructions.illustration-finder.
  points 맞는 자연·역사·일상 비유 요점당 2-3개 + 서론·결론 도입 예화.
  research-illustration/{YYMMDD}/ + _selfcheck.md. ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(experience-collector)
  프롬프트: "meta.yaml + instructions.experience-collector.
  topic 부합 야외봉사 공식 경험담 (연감·파수대·JW 방송) 2-3개.
  research-experience/{YYMMDD}/ + _selfcheck.md. ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(application-builder)
  프롬프트: "meta.yaml + instructions.application-builder.
  points 야외봉사 실전 적용 (방문 시기·인사말·안내 책자·재방문 연결).
  research-application/{YYMMDD}/ + _selfcheck.md. ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 4. 🤖 ③ — student-talk-planner 재검수

```
Agent(student-talk-planner)  [재검수]
  프롬프트: "5개 서브 + _selfcheck 전수 Read. 지시서 대비 A~E 점검.
  `_planner_review_research.md`: PASS | NEEDS-RERUN + 재지시."
```

### 5. 🤖 ① + ② — student-talk-script

```
Agent(student-talk-script)
  프롬프트: "outline.md + meta.yaml + _planner_review_research.md Read.
  research_dirs 5개 폴더 + _selfcheck Read.

  서술형 완성 원고:
    서론(30초) — 야외봉사 형제자매 공감
    요점 1(1.5~2분) — 성구·해설·구체 적용
    요점 2(있으면)
    결론(30초) — 격려·실천 다짐

  야외봉사 격려 톤, 한 문장 60음절, 약 660~1650자.
  담당자 placeholder.
  research-plan/student-talk/{YYMMDD}/script.md.

  ② 자체 검수: 모든 인용 원본 재조회, _selfcheck_script.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 6. 🤖 ③ — student-talk-planner script 재검수

```
Agent(student-talk-planner)  [script 재검수]
  프롬프트: "script.md + _selfcheck_script.md Read.
  A. 5분 분량 / B. NWT verbatim / C. topic 논지 근거
  D. 야외봉사 톤 일관 / E. 경험담·예화 출처 일치.
  `_planner_review_script.md`: PASS | NEEDS-REWRITE."
```

### 7. docx 렌더
```bash
python content_talk5_YYMMDD.py
```
(`build_mid_talk5.py` 작성 완료 (PDF 자동 변환 포함))

### 8. 🤖 ④ — 최종 감사 4종 병렬

```
Agent(fact-checker) → research-factcheck/{YYMMDD}/factcheck_talk5.md
Agent(jw-style-checker) → research-style/{YYMMDD}/
Agent(timing-auditor) → research-timing/{YYMMDD}/ (목표 5분 = 300초)
```
HIGH 1건 이상 → 재빌드 (2회까지).

### 9. 확인 및 보고
- docx/PDF 경로
- ③ 재검수 통과 + ④ HIGH/MEDIUM/LOW

## 개정 이력
- 2026-04-24 v2 — 6단 방어(v2) + 5개 보조 리서치 필수 (10분 연설과 동일 구조)
- 2026-04-23 v1 — 3개 선택 리서치 초안

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/mid-talk5` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `5분 연설_…YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
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
