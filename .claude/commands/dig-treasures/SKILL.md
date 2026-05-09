---
name: dig-treasures
description: 주중집회 ②번 "영적 보물찾기" 원고 1편을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3` (없으면 대화형). **6단 방어(v2) 프로토콜(`.claude/shared/multi-layer-defense.md`) + 서론·예화·삽화 품질 표준(`.claude/shared/intro-and-illustration-quality.md`)** 준수 — ① Planner 지시서(🟢 착수 블록 포함) → ② 서브 자체 검수(🔴 종료 블록) → ③ Planner 1차 재검수 → ④ Script 작성+자체 검수 → ⑤ Planner 2차 재검수(기획자 최종 QA) → ⑥ fact-checker + jw-style-checker 최종 게이트 (시간 제약 없는 포맷이라 timing-auditor 제외). spiritual-gems-planner → 5개 보조 리서치(scripture-deep·publication-cross-ref·application-builder·experience-collector·illustration-finder) → Planner 1차 재검수 → spiritual-gems-script → Planner 2차 재검수 → `content_sg_YYMMDD.py` → `build_spiritual_gems.py` docx/PDF. 20개 성구 × 3항(핵심·적용·배울점). 트리거 "/dig-treasures", "영적 보물찾기 만들어 줘", "영보 만들어줘".
---

## 🚨 STAGE 0 — Preflight 의무 (2026-05-03, 4-Layer 신뢰 모델)

```bash
cd ~/Claude/Projects/Congregation/_automation
python3 preflight.py dig-treasures {YYMMDD}
python3 slot_content_inventory.py {YYMMDD} {mwb_doc_url}
```

FAIL → 즉시 정지 (agent 0, 토큰 0). PASS → 카탈로그 저장.

## 🚨 Agent 의무 — content_inventory 사용

planner/script prompt 첫 줄: "의무 Read: `research-illustration/{YYMMDD}/_content_inventory.json` — mwb anchor (paragraphs·videos·scriptures·publications) 따라 골격. 카탈로그 외 자료 X."

설계도면: `research-meta/_ARCHITECTURE.md` §dig-treasures

## 🚨 Layer 4 자동 검증

빌더 build 직후 `verify_docx_against_inventory_auto(out_path, "영적 보물", builder_name)` 자동 호출 — anchor 누락 시 `SeedImageHardFail`.

## 🛡️ 팀 에이전트 호출 시 정본 prepend 의무 (2026-05-09 도입)

이 SKILL 이 planner / 보조 / script 에이전트를 Task 로 호출할 때 메인 Claude 는 정본 가이드라인을 prompt 맨 위에 직접 prepend 한다 (Claude Code Task 도구는 hook 으로 prompt augmentation 미지원 검증됨).

```python
# 호출 예시 — 각 에이전트 호출 직전
from team_briefings import get_briefing_for_team, prepend_to_prompt

brief = get_briefing_for_team("dig-treasures")
augmented = prepend_to_prompt(original_prompt, brief)
Agent(subagent_type="spiritual-gems-planner", prompt=augmented, ...)
```

또는 CLI:
```bash
python3 _automation/team_briefings.py dig-treasures
```

세부: Congregation/CLAUDE.md "회중 팀 에이전트 호출 시 정본 prepend 의무" 섹션.

## 🔁 직전 주차 중복 회피 (Phase G, 2026-05-09 도입)

⑥ 4종 게이트 직전에 **dedup 검사 의무**:

```bash
python3 _automation/run_dedup_for_slot.py dig-treasures <빌드된 docx 경로>
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

# dig-treasures — 영적 보물찾기 (단일 주차, 6단 방어(v2))

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx + PDF (자동 변환)

## 이 스킬의 범위
- 영적 보물찾기 **한 편** (한 주차)
- 20개 주요 성구 × 3항 (핵심·적용·배울점)
- **시간 제약 없음** — timing-auditor 제외
- 공식 질문(WOL) + 20개 영적 보물 해설 함께

## 🛡 품질 원칙 — 6단 방어(v2) + 서론·예화 품질 표준

### 실행 전 Read 의무 공유 파일 2개

1. **`.claude/shared/multi-layer-defense.md`** — 6단 방어(v2). 단계: ① Planner 지시서(🟢 착수 블록 복사 의무) → ② 서브 자체 검수(🔴 종료 블록) → ③ Planner 1차 재검수 → ④ Script 작성+자체 검수 → ⑤ **Planner 2차 재검수(기획자 최종 QA)** → ⑥ fact-checker + jw-style-checker (영보 시간 제약 없음 → timing-auditor 제외).
2. **`.claude/shared/intro-and-illustration-quality.md`** — 서론·예화·삽화 품질 표준. `dig-treasures` 차등 적용표 행: 14축 선택 2~3개 성구에 결합, 적절성 8필터 **필수 전부**, 삽화 N·A, 서론 N·A.

아래 모든 Agent 호출 프롬프트에는 "공유 파일 2개 Read 의무 + 🟢🔴 블록 복사·PASS 의무" 가 기본 전제.

## 인자 규약
`now|next1|next2|next3`

## 📐 라벨·강조·다각도·4축 + gem-coordinator — 정본 참조

> **2026-05-02 압축** — 라벨 용어·다각도·4축·자기점검·gem-coordinator R1~R10 본문은 **정본 일원화**.
>
> | 영역 | 정본 |
> |---|---|
> | 라벨 용어 (① 핵심 / ② 적용 / ③ 배울점) | `.claude/shared/comment-label-standard.md` |
> | 다각도·4축·R1~R10·자기점검 / Phase E v2 / hook·정량 메트릭 | `.claude/shared/dig-treasures-automation.md` |
> | gem narrative 표준 | `.claude/shared/gem-narrative-standard.md` |
> | gem-coordinator (5블록 매핑·spec dict 드래프트) | `.claude/agents/gem-coordinator.md` |
>
> `validators.py` 가 빌드 시 10 룰 자동 차단 — 위반 시 docx 미생성. spiritual-gems-planner·script·gem-coordinator 는 위 정본 의무 Read.

## ⚠ WOL-first 수집 규칙
1. 주차 인덱스: `https://wol.jw.org/ko/wol/dt/r8/lp-ko/YYYY/M/D`
2. "영적 보물 찾기" 섹션 href 따라갈 것. 공식 질문·참조·성구 매주 바뀜.
3. 공식 질문 참조 자료(「파YY.MM」 등) WOL 페이지 값 그대로.
4. 통독 범위(예: 이사야 54-55장) WOL 에서 확인.
5. 타임아웃 → 재시도 3회.

## 🚫 할루시네이션 금지 (공통)
공식 출판물 실제 확인 내용만. `[확인 필요]` placeholder. 출처 URL + 호수/면/항 필수. 성구 verbatim.

모든 Agent 프롬프트 말미:
> ⚠ 할루시네이션 금지 / ⚠ 6단 방어(v2) 프로토콜 준수 (.claude/shared/multi-layer-defense.md Read)

## 📖 저작권
jw.org 공개 자료, 장문 verbatim 허용.

## 저장 위치
베이스: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/02.영적 보물 찾기/YYMMDD-MMDD/`
파일명: `영적 보물 찾기_YYMMDD.docx`

## 포맷
- 맑은 고딕 14pt
- 사회자 진행 대사: 14pt 볼드 노랑 하이라이트
- 답변 포인트: 12pt
- 장별 소제목: 13.5pt 볼드

## 실행 단계 (6단 방어(v2))

### 1. 주차 확정 + 폴더

### 2. 🤖 ① + ② — spiritual-gems-planner 1차 (지시서 포함)

```
Agent(spiritual-gems-planner)
  프롬프트: "{YYMMDD} '영적 보물찾기' 기획 1차 (6단 방어(v2) ①).
  주차 인덱스에서 공식 질문 2개·표어 성구·참조 자료·통독 범위 수집.
  통독 범위 전체에서 영적 통찰 풍부한 절 20개 선정 (교리·원칙·예언 성취·
  실생활 적용·여호와 속성·예수 모본 기준).

  저장: `research-plan/spiritual-gems/{YYMMDD}/` outline.md + meta.yaml
  meta.yaml 필수:
    week_date, bible_reading_range,
    official_questions: [각 질문 + 참조 + URL],
    headline_scripture,
    selected_gems: [20개 성구 + NWT verbatim + 선정 이유],
    research_dirs: {bible, topic, application, experience, illustration}/{YYMMDD}/

  ⭐⭐ instructions_to_subresearchers (① 필수):
    5개 서브에게 지시서(중점·우선·피하기).

  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 3. 🤖 ② — 5개 보조 병렬 (지시서 수신 + 자체 검수)

```
Agent(scripture-deep)
  프롬프트: "meta.yaml + instructions.scripture-deep 준수.
  selected_gems 20개 각 NWT 연구용 본문·연구 노트·상호 참조·원어·역사 배경.
  research-bible/{YYMMDD}/gem-NN-*.md.
  ② 자체 검수: wol URL 재조회 글자 대조, _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(publication-cross-ref)
  프롬프트: "meta.yaml + instructions.publication-cross-ref 준수.
  selected_gems 20개 각각 인용·해설한 출판물 wol 횡단 (파수대·깨어라·통찰·
  예수책·하느님의 사랑·여호와께 가까이·이사야의 예언·JW 방송).
  각 성구당 단락 2-3개 (출처 URL·호수·면·항).
  공식 질문 참조 자료 본문도 함께 확인.
  research-topic/{YYMMDD}/gem-NN-cross-ref.md + official-question-refs.md + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(application-builder)
  프롬프트: "meta.yaml + instructions.application-builder 준수.
  selected_gems 20개 실생활 적용점 (가정·직장/학교·회중·개인 영성 중 맞는 축).
  각 성구당 1-2개 상황 + 자기점검 질문.
  research-application/{YYMMDD}/gem-NN-apply.md + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(experience-collector)
  프롬프트: "meta.yaml + instructions.experience-collector 준수.
  selected_gems 중 경험담 뒷받침 5-8개 성구 선정, 공식 경험담 매칭.
  research-experience/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."

Agent(illustration-finder)
  프롬프트: "meta.yaml + instructions.illustration-finder 준수.
  selected_gems 중 예화 보강 5-8개 성구 대상 자연·역사·일상 비유.
  research-illustration/{YYMMDD}/ + _selfcheck.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 4. 🤖 ③ — spiritual-gems-planner 재검수

```
Agent(spiritual-gems-planner)  [재검수]
  프롬프트: "5개 서브 산출물 + _selfcheck 전수 Read. meta.yaml 지시서 대비:
    A. 중점 반영 / B. 피하기 회피 / C. _selfcheck 통과 / D. 20개 성구 균형
    E. 공식 질문 참조 자료 정확 / F. 모순 없음
  `_planner_review_research.md`: PASS | NEEDS-RERUN + 재지시."
```

### 5. 🤖 ① + ② — spiritual-gems-script 호출

```
Agent(spiritual-gems-script)
  프롬프트: "outline.md + meta.yaml + _planner_review_research.md Read.
  research_dirs 5개 폴더 (+ _selfcheck) Read.

  사회자 진행 스크립트 흐름:
    1) 도입 (14pt 노랑)
    2) 공식 질문 2개 각각:
       - 성구 낭독 요청·감사·질문·답변 포인트 (research-topic 참조 자료 기반)
    3) 영적 보물 전환 (14pt 볼드 노랑)
    4) 장별 그룹핑된 20개 성구 × 3항 해설
       - 장 소제목 (13.5pt 볼드)
       - 각 성구: 핵심 내용 / 적용점 / 배울점
       - 푸터 '📎 참고:' WOL·출판물·상호참조 하이퍼링크
    5) 마무리

  작성 원칙:
    - 한 성구 2가지 통찰 가능하면 둘 다
    - 연구 노트 + 출판물 + 적용 엮기
    - 다양한 서두 (반복 금지)
    - 성구 NWT 연구용 verbatim

  결과: research-plan/spiritual-gems/{YYMMDD}/script.md

  ② 자체 검수: 모든 성구·인용·경험담 원본 재조회, _selfcheck_script.md.
  ⚠ 할루시네이션 / 6단 방어(v2)."
```

### 6. 🤖 ③ — spiritual-gems-planner script 재검수

```
Agent(spiritual-gems-planner)  [script 재검수]
  프롬프트: "script.md + _selfcheck_script.md Read.
  A. 공식 질문 2개 포함 / B. 20개 성구 모두 3항 완성 / C. NWT verbatim
  D. topic 논지 근거 / E. 장별 그룹핑 / F. 하이퍼링크 매칭
  `_planner_review_script.md`: PASS | NEEDS-REWRITE + 지시."
```

### 7. content_sg_YYMMDD.py 스펙 변환 (메인 Claude)
script.md Read → 기존 `content_sg_*.py` 템플릿에 맞춰 paragraph/스타일/하이퍼링크 변환. 원고 새로 쓰지 않음.

### 8. docx/PDF 렌더
```bash
cd "~/Claude/Projects/Congregation/_automation"
python content_sg_YYMMDD.py
```
(build_spiritual_gems.py 가 docx + PDF 동시)

### 9. 🤖 ④ — 최종 감사 (2종 병렬, timing-auditor 제외)

```
Agent(fact-checker)
  프롬프트: "{docx_path} 성구·출판물·URL·경험담 독립 검증.
  research-factcheck/{YYMMDD}/factcheck_gems.md.
  ⚠ WebFetch 원본 재조회 필수."

Agent(jw-style-checker)
  프롬프트: "{docx_path} 감수. 금칙어·신세계역·경어체·높임법·정치 중립.
  research-style/{YYMMDD}/ 저장."
```

⚠ timing-auditor 호출 금지 (시간 제약 없음).
HIGH 1건 이상 → 재빌드 (2회까지).

### 10. 확인 및 보고
- docx/PDF 경로
- ③ 재검수 통과 + ④ HIGH/MEDIUM/LOW 카운트

## 기억할 점
- 20개 성구 × 3항 / 시간 비강제 / NWT verbatim / 답변은 참조 자료 실제 논지 중심

## 개정 이력
- 2026-04-24 v2 — 6단 방어(v2) 프로토콜 적용
- 2026-04-23 v1 — spiritual-gems-planner/script 2단 초안 (mid-study2 이관)

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/dig-treasures` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `영적 보물 찾기_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3` 또는 `mid-study2`) 호출 시

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
