---
name: publictalk
description: 주말집회 공개 강연 30분 원고(서술형)를 1개씩 자동 생성한다. 로컬 골자 (`S01.공개강연/골자/PB_NNN-KO*.pdf` 구형 또는 `S01.공개강연/골자/S-34_KO_NNN.docx` 신형) 를 Read 해서 public-talk-builder 가 기획(아키텍처·요점별 에이전트 지시서) 을 짜고, 그 지시서대로 scripture-deep·illustration-finder·experience-collector·application-builder·publication-cross-ref 가 병렬 리서치한 뒤, Claude 본체가 30분 서술형 원고를 통합 작성한다. 산출물은 docx + PDF (`S01.공개강연/김원준 공개강연/{번호:03d}_{슬러그}/` 폴더). 최종 감수는 fact-checker + jw-style-checker + timing-auditor + quality-monotonic-checker (4종 병렬, ⑥ 단계). 트리거 "/publictalk", "공개강연 만들어 줘", "공개강연 N번".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# publictalk — 공개 강연 30분 원고 자동 생성 (1편 단위)

## ⭐ 이 스킬의 특징 (다른 스킬과 차이)

- **주중·파수대 스킬과 달리 "3주치" 개념 없음** — 공개 강연은 강연자 로테이션이라 "이번 주 것" 이 고정되지 않는다. 한 번 실행 = **한 강연 번호 1편** 생성.
- **public-talk-builder 가 orchestrator 역할** — 단순 아웃라인 제공자가 아니라 **"기획자 (architect)"** 로서 30분 원고 설계도를 만들고, 그 설계도 안에 **"각 요점에 다른 에이전트가 수집할 재료 명세서"** 까지 작성. 다른 에이전트들은 그 명세서대로 타겟된 재료만 수집 → 원고 품질이 높아짐.
- **골자 소스는 로컬 PDF** — `docs.jw.org` 는 로그인 필요해서 자동 fetch 불가. 사용자가 이미 다운로드해 둔 PDF 를 Read.

## 🎙️ 대화형 시작 흐름 (사용자 지정, 필수 준수)

사용자가 `/publictalk` 또는 "공개강연 만들어 줘" 를 치면:

### 1단계 — 강연 번호 묻기
> "몇 번 공개 강연 원고를 만들어 드릴까요? (1~194 중 번호)"

### 2단계 — 로컬 골자 확인 및 골자 소스 확인
번호를 받으면 즉시 **두 형식 모두** 검색:
```
# 신형 골자 (S-34 시리즈, .docx)
~/Dropbox/02.WatchTower/02.▣ 집회(Meetings)/S01.공개강연/골자/S-34_KO_{번호:03d}.docx
# 구형 골자 (PB 시리즈, .pdf)
~/Dropbox/02.WatchTower/02.▣ 집회(Meetings)/S01.공개강연/골자/PB_{번호:03d}-KO*.pdf
```
**골자 폴더 직속에 둠 — `KO/` 하위 폴더 없음.** 두 형식 중 어느 것이든 발견되면 Case A.

**Case A — 로컬 골자 있음**:
- 신형 (`S-34_KO_NNN.docx`) 우선 사용 (최신 개정판이 이 형식으로 배포됨)
- 둘 다 있으면 신형 우선, 사용자에게 "신형 S-34 골자를 사용합니다 (구형 PB_NNN.pdf 도 있지만 최신본 우선)" 안내
> "로컬에 `S-34_KO_{NNN}.docx` (또는 `PB_{NNN}-KO*.pdf`) 골자 파일이 있습니다. 이 골자로 작성할까요? 아니면 최신 골자를 직접 주시겠어요?"

사용자 선택:
- (a) "있는 골자로" / "로컬" / "이걸로" → 로컬 파일 Read → 3단계로
- (b) "새 골자 주겠다" / "최신으로" → 사용자가 골자 텍스트/파일 경로 제공할 때까지 대기 → 받으면 3단계로

**Case B — 로컬 골자 없음**:
> "로컬에 `S-34_KO_{NNN}.docx` 또는 `PB_{NNN}-KO*.pdf` 골자 파일이 없습니다. `docs.jw.org/ko/-/cds-cat-docs-outlines` 에서 해당 번호 골자를 다운로드해서 `S01.공개강연/골자/` 에 넣어주시거나, 골자 텍스트를 직접 붙여넣어 주세요."

사용자가 파일 넣거나 텍스트 제공할 때까지 대기.

### 3단계 — 골자 Read 및 제목 추출
- **신형 .docx**: `python -X utf8 -c "from docx import Document; ..."` 로 paragraphs 추출 (cp949 인코딩 회피 위해 `-X utf8` + `sys.stdout = io.TextIOWrapper(..., encoding='utf-8')` 필수)
- **구형 .pdf**: Read 도구 (Claude 는 PDF 직접 읽기 가능)
- 사용자 제공 텍스트라면 그대로 사용
- 제목·표어 성구·요점 추출 → 사용자에게 1줄 확인:
  > "번호 NNN · 제목 '{제목}' · 표어 성구 {성구} 로 진행하겠습니다. 리서치 시작합니다..."

### 4단계 이후 — 아래 [실행 파이프라인] 진행 (자동)

**예외**: 사용자가 처음부터 `/publictalk 179` 처럼 번호를 같이 주거나, `/publictalk 179 로컬` 처럼 소스까지 주면 1-2단계 스킵 가능. 단 제목·표어 성구 확인(3단계 마지막 줄)은 **반드시** 거쳐서 빨리 잘못 가는 걸 막을 것.

### ⭐ Stage 0 — 메인 사전 종합 분석 (의무, 2026-05-02)

builder 호출 직전, 메인 Claude 가 **자율 종합** — 사용자 명시 지시 없이도:

1. **골자 폴더 `ls`** — 같은 폴더의 .jpg/.png N장 추출 (시각자료 1·2 정확본)
2. **누적 메모리 Read** — `~/.claude/projects/-Users-brandon-Claude/memory/feedback_*.md` (골자 고정·본문 호명 0·사회자 섹션 0·메타 번역체 회피·서론·결론 연계·시각자료 4단계·인물 성별·신선한 후크·R-Conv·70:30 등)
3. **같은 강연 번호 이전 ver 검수 보고서** — `research-{factcheck/style/timing/quality}/publictalk_{NNN}_*` + `research-public-talk/{NNN}_planner_*` Read → 누적 결함 회피 매트릭스
4. **모범 강연 (2024 특별강연·mid-talk10) 패턴** 비교
5. 위 종합을 builder 지시서에 **사전 박힘** → illustration-finder·script 가 자율 반영

→ **사용자 추가 지시 0회 목표**. "골자 봐라"·"4단계 통합해라"·"매칭률 100%"·"서론·결론 연계" 같은 것 일일이 알려줄 필요 없게.

상세 명세: `research-meta/공개강연-자동화-구조.md` §1 [Stage 0]

## 🚫 할루시네이션 절대 금지 (최상위 규칙)

이 스킬이 호출하는 모든 Agent (public-talk-builder · scripture-deep · publication-cross-ref · illustration-finder · experience-collector · application-builder · jw-style-checker · timing-auditor) 는 아래를 준수:

1. **공식 JW 출판물·신세계역 연구용 성서·골자 PDF 에서 실제로 확인한 내용만** 산출물에 넣는다. 훈련 데이터 기억·추측으로 인용·경험담·예화를 만들지 말 것.
2. **확인 못 한 항목은 명시적 placeholder** `[확인 필요]`. 빈 칸이 창작 인용보다 안전하다.
3. **모든 인용은 출처 URL + 출판물 이름/호수/면/항** 필수. URL 없는 인용 금지.
4. **성구 본문은 신세계역 연구용 성서 verbatim.**
5. **경험담은 공식 출판물에 실제 게재된 것만.** 창작 금지.
6. **예화·비유도 출처 명시 필수.**

**모든 Agent 호출 프롬프트 말미에 다음 공통 문구를 반드시 첨부:**

> ⚠ 할루시네이션 절대 금지: 훈련 데이터 기억이 아니라 공식 JW 출판물 (wol.jw.org) · 신세계역 연구용 성서 · 사용자가 제공한 골자 PDF 에서 **실제로 확인한 내용만** 저장할 것. 확인 못 한 항목은 `[확인 필요]` placeholder. 모든 인용은 출처 URL + 출판물 이름/호수/면/항 포함. 성구는 verbatim. 경험담·예화도 출처 명시 필수.

## 📖 저작권 정책

jw.org 및 wol.jw.org 는 공개 자료이므로 저작권은 고려하지 않는다 (사용자 지침, 2026-04-22). 파수대·깨어라·통찰·훈 책 등의 장문 verbatim 인용·단락 전문 복사 모두 허용. 단, 출처 URL 명시는 할루시네이션 방지 차원에서 여전히 필수.

## 🎯 공개 강연 표준 구조 (30분)

| 구간 | 시간 (초) | 누적 | 내용 |
|---|---|---|---|
| 오프닝 (사회자) | 60 | 1분 | 강연자 소개·제목 발표 |
| **서론** | 180~240 | 4분 | 청중 관심 유도·주제 제시·강연 예고 |
| **요점 1** | 360~420 | 11분 | 성구·설명·예화·적용 |
| **요점 2** | 360~420 | 18분 | 성구·설명·예화·적용 |
| **요점 3** | 360~420 | 25분 | 성구·설명·예화·적용 |
| **결론** | 180 | 28분 | 요점 복습·청중 결단 촉구 |
| 마무리 (사회자) | 60 | 29~30분 | 감사·다음 순서 예고 |

**강연자 낭독 구간 총합 = 약 1500~1680초 (25~28분)**. 오프닝/마무리 사회자 대사 60초+60초 제외.

## 💾 저장 경로

```
~/Dropbox/02.WatchTower/02.▣ 집회(Meetings)/S01.공개강연/김원준 공개강연/{번호:03d}_{슬러그}/
  ├── {번호:03d}_{슬러그}_ver1.docx
  └── {번호:03d}_{슬러그}_ver1.pdf
```

- **번호**: 3자리 0 패딩 (예: `001`, `025`, `179`)
- **슬러그**: 강연 제목에서 공백·특수문자 제거하거나 `_` 로 치환. 한글은 그대로 유지. 예: "세상의 환상적인 것을 멀리하고 왕국의 실제적인 것을 추구하라" → `세상의환상적인것을멀리하고왕국의실제적인것을추구하라` (약 30자 이내로 적절히 축약 권장)
- 같은 번호 재실행 시 **파일명에 `_verN_` 을 한 단계 올려서** 저장 (메모리 `feedback_version_bump.md` 규칙). 기존 `_ver1_` 이 있으면 `_ver2_`.
- 파일명에 "김원준" 등 사용자 이름 포함 금지 (메모리 `feedback_filename_no_name.md` 규칙).

## 🤖 실행 파이프라인 (3단계 이후 자동)

### [단계 A] public-talk-builder = 기획자 (단독 실행)

골자 텍스트를 넘겨주고 **30분 원고 설계도 + 요점별 에이전트 지시서** 를 받는다.

```
Agent(public-talk-builder)
  프롬프트:
  "공개 강연 {번호}번 '{제목}' 30분 원고 기획.

  [골자 본문 — PDF 전문 또는 사용자 제공 텍스트]
  {골자 verbatim 삽입}

  이 골자를 보고 다음 두 가지 산출물을 research-public-talk/{번호}_{YYMMDD}.md 에 저장:

  (1) 30분 원고 설계도:
      - 표어 성구 (골자 그대로)
      - 서론 뼈대 (관심 유도 방법·주제 문장·요점 예고) — bullet
      - 요점 1·2·3: 한 문장 요약, 핵심 성구 1-2개, 낭독할지 언급할지, 시간 배분
      - 결론 뼈대
      - 시간 배분 표

  (2) ★ 요점별 다른 에이전트 지시서 (이 스킬의 핵심):
      - 요점 1 → scripture-deep 에: '{성구 ref} 심층 조사 — 연구 노트·상호참조·원어'
      - 요점 1 → illustration-finder 에: '{요점 문구} 에 맞는 {자연/역사/일상 중 택1} 예화 1-2개'
      - 요점 1 → experience-collector 에: '{요점 주제} 관련 증인 공식 경험담 1-2개'
      - 요점 1 → application-builder 에: '{요점 주제} 실생활 적용 (가정·직장·전도 축) 3-5개'
      - 요점 1 → publication-cross-ref 에: '{요점 키워드} 로 파수대·깨어라·통찰 횡단 검색'
      - 요점 2·3 도 동일 형식

  각 지시서는 Claude 본체가 그대로 복사해서 다른 에이전트에게 전달할 수 있게 완결된 프롬프트 형태로 작성할 것.

  [할루시네이션 금지 공통 문구]"
```

**주의**: public-talk-builder 의 기본 스펙은 "원고 작성 금지, 아웃라인만" 이다. 이 스킬에서는 그 제약을 유지하고, 본체가 원고를 쓴다. 기획자 역할에 충실하게.

### [단계 B] 6개 에이전트 병렬 — 기획서 지시대로

> ⚠ 각 에이전트는 자기 정의 .md 의 **🟢 착수 블록 (주의사항·꼭 해야할 것 주지)** 을 자기 응답 첫 줄에 명시 후 시작. 모든 에이전트 model = opus. 응답 끝에 **🔴 종료 블록 (자체 검수)** 결과 첨부. (6단 방어 v2 — `Congregation/.claude/shared/multi-layer-defense.md`)


단계 A 산출물(`research-public-talk/{번호}_{YYMMDD}.md`) 을 Read 해서 각 에이전트 지시서를 추출. **한 메시지에 6개 Agent 블록 동시 호출**:

```
Agent(scripture-deep)
  프롬프트: "[public-talk-builder 가 생성한 성구 지시서 그대로]
  결과는 research-bible/publictalk_{번호}/ 에 성구별 .md 로 저장.
  [할루시네이션 금지 공통 문구]"

Agent(illustration-finder)
  프롬프트: "[public-talk-builder 가 생성한 예화 지시서]
  research-illustration/publictalk_{번호}/ 에 저장.
  [할루시네이션 금지 공통 문구]"

Agent(experience-collector)
  프롬프트: "[public-talk-builder 가 생성한 경험담 지시서]
  research-experience/publictalk_{번호}/ 에 저장.
  [할루시네이션 금지 공통 문구]"

Agent(application-builder)
  프롬프트: "[public-talk-builder 가 생성한 적용 지시서]
  research-application/publictalk_{번호}/ 에 저장.
  [할루시네이션 금지 공통 문구]"

Agent(publication-cross-ref)
  프롬프트: "[public-talk-builder 가 생성한 출판물 횡단 지시서]
  research-topic/publictalk_{번호}/ 에 저장.
  [할루시네이션 금지 공통 문구]"

Agent(qa-designer)  # ★ 공개 강연 모드 2 (수사적 질문·청중 인터랙션 + 서론 후크·결론 여운 설계)
  프롬프트: "[public-talk-builder 가 생성한 수사적 질문·인터랙션·서론 후크 지시서]
  ⚠ 이 호출은 qa-designer 모드 2 (공개 강연) — 공개 강연 경로(publictalk_) 이므로 에이전트 정의 G-mode2 섹션 지침대로 수행.
  산출물:
  ① 서론 후크 설계 (G-mode2-4b) — 5종 중 1종 선택 + A/B/C 3안 + 1차 자료 출처 + 표어 성구 전환 문장
  ② 수사적 질문 12개+ (A/B/C 3안)
  ③ 청중 인터랙션 3~5개
  ④ 감정 몰입 장면 1~2개 (결론부 필수)
  ⑤ 성구 낭독 유도문
  ⑥ 결론 여운 문장 3~5개 (선언형, 감사 인사 금지)
  research-qa/ 에 파일명 `{번호}_rhetorical_YYMMDD.md` 형식 저장.
  [할루시네이션 금지 공통 문구]"
```

**공개 강연 파이프라인 전체 에이전트 호출 = 8개**:
- 단계 A: public-talk-builder (1)
- 단계 B: 위 6개 (scripture-deep, illustration-finder, experience-collector, application-builder, publication-cross-ref, qa-designer mode 2)
- 단계 F: jw-style-checker, timing-auditor (2)

**`{번호}`** 는 3자리 패딩 (예: `publictalk_179`).

폴더 매핑 전체 목록 (공통):
- `research-public-talk/` ← public-talk-builder
- `research-bible/` ← scripture-deep
- `research-illustration/` ← illustration-finder
- `research-experience/` ← experience-collector
- `research-application/` ← application-builder
- `research-topic/` ← publication-cross-ref
- `research-style/` ← jw-style-checker
- `research-timing/` ← timing-auditor

베이스: `~/Dropbox/ClaudeFile/Congregation/` (기존 주중·주말 스킬 공용).

### [단계 B-3] **public-talk-builder 1차 재검수** (Planner 1차 — 6단 방어 v2 ③단계)

단계 B 의 6개 리서치 산출물을 모두 모은 직후, **기획자(public-talk-builder)** 를 다시 호출해 다음을 검증:

```
Agent(public-talk-builder)
  프롬프트: "[1차 재검수 모드] 공개 강연 {NNN}번 「{제목}」.

  단계 A 에서 작성한 기획서 (research-public-talk/{NNN}_{YYMMDD}.md) 와
  단계 B 의 6개 산출물을 비교 검토:
  - research-bible/publictalk_{NNN}/
  - research-topic/publictalk_{NNN}/
  - research-illustration/publictalk_{NNN}/
  - research-experience/publictalk_{NNN}/
  - research-application/publictalk_{NNN}/
  - research-qa/{NNN}_rhetorical_{YYMMDD}.md

  체크 (R 룰 grep 의무 — Phase 1-G, 2026-05-02):
  - R1 글자수 후보: 보조 리서치 합산 ≥ 12,000자 (script 가 6,500~9,000 으로 추릴 풍부 베이스라인)
  - R3 성구 후보: scripture-deep 산출물에 낭독 후보 ≥ 10개 (script 가 6~8 선정)
  - R4 외부 14축 후보: illustration-finder + publication-cross-ref 합쳐 ≥ 8축 사용
  - R5 이미지 후보: illustration-finder 산출물에 wol/jwb 우선 ≥ 5장 + ext 백업 ≥ 3장
  - R6 청중 인터랙션 후보: qa-designer 산출물에 ≥ 15개
  - R8 서론 후크 후보: qa-designer G-mode2-4b 5종 중 1종 + A/B/C 3안 모두 존재
  - R-J5 친숙한 비유 후보: illustration-finder 에 일상 비유 ≥ 5개

  R 룰 1건이라도 미달 시 해당 에이전트 재호출 지시. 모두 PASS 면 단계 C 진입.

  결과 저장: research-public-talk/{NNN}_planner_review_research_{YYMMDD}.md
  형식: 각 R 룰별 측정값·PASS/FAIL·근거 파일 경로 표 의무"
```

PASS 후에만 단계 C 진입.

### [단계 C] **public-talk-script 에이전트** = 30분 서술형 원고 작성 ⭐⭐ 품질 핵심

> **2026-04-25 변경 — 본체 직접 작성 폐지**: 회차마다 본체가 짜깁기해서 일관성이 깨지는 퇴보 패턴을 끊기 위해 신규 `public-talk-script` 에이전트가 30분 원고를 직접 작성한다. 본체는 호출만. 영구 규칙 12개 (골자 파트 시간 ±0 / 시간 마커 파트 단위 / `[…낭독]` 자동 인식 / 시각자료 illustration-finder 결정대로 / 후크 qa-designer 결정대로 / 청중 호칭·금칙어·verbatim·8필터·시인성·참조 자료 하이퍼링크) 는 모두 `Congregation/.claude/agents/public-talk-script.md` 에 영구 박힘. 194개 강연 모두에 동일 적용. 아래 본문은 **참조용 보존**.

```
Agent(public-talk-script)
  프롬프트: "공개 강연 {NNN}번 「{제목}」 30분 원고 작성.

  입력 7개 Read:
  - research-public-talk/{NNN}_{YYMMDD}.md  (기획서)
  - research-bible/publictalk_{NNN}/         (성구)
  - research-topic/publictalk_{NNN}/         (출판물)
  - research-illustration/publictalk_{NNN}/  (시각자료 — 슬롯·캡션·임베드 라인 결정대로)
  - research-experience/publictalk_{NNN}/    (경험담)
  - research-application/publictalk_{NNN}/   (적용)
  - research-qa/{NNN}_rhetorical_{YYMMDD}.md (수사장치)

  같은 강연 번호 이전 ver 가 있으면 research-style/* + research-timing/* 모두 의무 Read 후 누적 지적 반영.
  영구 규칙 12개 모두 준수 (자기 정의 .md 참조).
  자체 검수 통과 후 research-public-talk/{NNN}_{슬러그}_원고_ver{N}_{YYMMDD}.md 저장.

  [할루시네이션 금지 공통 문구]"
```

본체는 산출물 .md 를 **수정 없이 그대로** 다음 단계 D-E 빌더에 넘긴다.

---

> **이하는 참조용 보존 (이전 본체 작성 시절 12개 기준 — 모두 public-talk-script.md 에 영구 흡수됨)**

단계 A·B 산출물을 **모두 Read** 로 통합해 30분 서술형 원고 작성:

- `research-public-talk/{번호}_{YYMMDD}.md` — 설계도
- `research-bible/publictalk_{번호}/*.md` — 성구 심층
- `research-illustration/publictalk_{번호}/*` — 예화
- `research-experience/publictalk_{번호}/*` — 경험담
- `research-application/publictalk_{번호}/*` — 적용
- `research-topic/publictalk_{번호}/*` — 출판물 횡단
- `research-qa/{번호}_rhetorical_{YYMMDD}.md` — 수사적 질문·청중 인터랙션·감정 몰입 장면·성구 낭독 유도문·결론 여운 문장

**각 요점의 narrative 구조 (6단계 — mid-study1 의 10분 연설 구조를 30분 스케일에 맞게 확장)**:

1. **흥미 유발** (30~60초) — 청중이 궁금해하거나 공감할 수 있는 질문/상황/사실/대조 중 하나 (요점마다 다른 방식)
2. **성구 유도 + 낭독** (40~60초) — "그 점을 [책 장:절]에서 확인해 보겠습니다" → 신세계역 연구용 verbatim 낭독
3. **성구 설명** (90~120초) — `research-bible` 의 연구 노트·원어·상호참조 + `research-topic` 의 과거 파수대 논지를 종합
4. **예화 또는 경험담** (60~120초) — `research-illustration` 또는 `research-experience` 에서 1개 선택·서술
5. **적용 포인트** (60~90초) — `research-application` 의 구체적 상황 1-2개 + 자기점검 질문 1개
6. **요점 마무리 + 다음 요점 전환** (15~30초) — 요점을 주제 전체에 연결

요점 1개 = 약 6~7분 (360~420초). **3개 요점 = 18~21분.** 서론 4분 + 결론 3분 + 사회자 2분 = 27~30분 안착.

**절대 원칙**:
- 🔒 **성구는 신세계역 연구용 성서 verbatim** — 한 단어도 바꾸지 말 것
- 🔒 **설명 내용은 참조 자료의 실제 논지 기반** — 창작하지 말 것
- 🔒 **예화·경험담은 research-* 폴더에서 확인한 것만** — 임의 픽션 금지
- 🔒 **비증인 청중 고려** — 내부 용어(회중·봉사의 종·개척자) 는 짧게 풀이하거나 피하고, 신·예수·성서라는 공통 언어 중심
- 📏 매 요점마다 흥미 유발 방식을 **다르게** (질문/사실/예화/뉴스/대조)
- 📏 수사적 질문은 요점 진입·결론 직전에 자연스럽게 삽입
- 📏 **서술형 원고** (강의가 아니라 강연) — 소리 내어 읽었을 때 자연스러운 문장

---

## 🎬 서론·문체·시각자료·외부 자료 정책 — 정본 참조

> **2026-05-02 압축** — 본 섹션의 상세 룰은 **정본 일원화**. 토큰 절감 + 회귀 방지.
>
> | 영역 | 정본 |
> |---|---|
> | 절대 금지 표현 (서론 안녕하십니까·여러분·강연자 자기소개·메타 도입) | `_automation/validators.py` (빌드 시 자동 차단) + `shared/banned-vocabulary.md` |
> | 후크 5종 (역사·숫자·대조·질문·유명인) + A/B/C 3안 | `shared/publictalk-formal-expressions.md` §후크 |
> | 외부 소재 우선순위 (1차 자료 > 20년+ JW > 최근 10년 회피) | `research-meta/공개강연-자동화-구조.md` §5 |
> | 외부 14축 (성서 적중 9 + 사유 촉발 5) — 여호와의 지혜 입증 | 정본 §12 외부 14축 후보 |
> | BAD vs GOOD 서론 예시 | 정본 §3 모범 정형 표현 + 부록 (archive 완벽-프로세스 §1·부록 A) |
> | R-No-Chair·R-No-Source-Naming (사용자 피드백 ①·④) | 정본 §0 영구 규칙 14·15 + §2-1-bis |
>
> public-talk-builder·qa-designer mode 2·illustration-finder 는 **위 두 정본을 의무 Read** 후 지시서·산출물 작성. 메인 Claude 는 슬래시 명령 입력 시 정본 한 번만 Read 한다.

---


## 🎨 원고 시인성 강조 마크업 (빌더 지원 문법)

`build_publictalk.py` 는 아래 인라인 마크업을 지원. 원고 작성 시 **적극 사용**해 강연자가 손대지 않고 낭독할 수 있도록 강조 포인트를 미리 표시.

| 마크업 | 효과 | 사용 지점 |
|---|---|---|
| `==text==` | **볼드 + 노랑 하이라이트** | 수사적 질문, 핵심 문장, 감정 몰입 장면, 시각 자료 지시 |
| `!!text!!` | **빨강 볼드** | 연도, 인명, 핵심 개념, 강조 단어 |
| `**text**` | **볼드** | 일반 강조, 요점 단어 |
| `*text*` | *이탤릭* | 성구 낭독 본문 (인용 블록 `>` 와 함께) |
| `` `[N'NN"]` `` | 빨강볼드 + 노랑 (단독 라인 우측 정렬) | 시간 마커 |
| `> *성구*` | 이탤릭 회색 인용 블록 | 성구 verbatim 낭독 |

### 사용 비율 가이드
- `==노랑 하이라이트==` 는 **단락당 0~2개** (남발하면 시인성 저하)
- `!!빨강 볼드!!` 는 단락당 1~3개 가능 (연도·인명·핵심 개념에 밀집 가능)
- 모든 수사적 질문에는 `==...==` 또는 `**...**` 강조 필수
- 시각 자료 지시문은 반드시 `==[시각 자료 N — 설명]==` 형식

---

## ⭐ 원고 문체·시각자료 — 정본 참조

> **2026-05-02 압축** — "2024 스타일" 12 기준 + 시각자료 10-0~10-5 + 단계적 논증은 **정본 일원화**.
>
> | 영역 | 정본 |
> |---|---|
> | 12 기준 (구어체·인터랙션·시간 마커·일상 비유·감정 몰입·수사 질문 밀도·하이라이트 3색·전환구·성구 활용·시각자료·결론 행동 촉구·단계적 논증) | `shared/publictalk-formal-expressions.md` §문체 + 정본 §3 모범 정형 표현 |
> | 시각자료 우선순위·종교성 이진 판정·총 5장 상한·소스 4단계·유형 A/B 엄격도·마크업 표기 | 정본 §5 시각자료 |
> | 낭독 정형 (`[책 장:절] (낭독)` + NWT verbatim + URL) | 정본 §2-1-bis R-Scripture-Format |
> | PPTX 별도 관리 (모범 강연 패턴) | 정본 §0 영구 규칙 16 + §2-1-bis R-Visual-PPTX |
>
> public-talk-script 는 **정본 + formal-expressions 의무 Read** 후 30분 원고 작성.

---


### [단계 C-1] **publictalk-assembly-coordinator** (Phase 3-C, 2026-05-02)

public-talk-script 가 .md 원고를 산출한 직후, **publictalk-assembly-coordinator** 를 호출하여 R 룰 정량 grep + 골자 1:1 매핑 + 보조 리서치 활용도 1차 검증.

```
Agent(publictalk-assembly-coordinator)
  프롬프트: "공개 강연 {NNN}「{제목}」 ver{N} 원고 조합·매핑·R 룰 검증.

  입력:
  - 기획서: research-public-talk/{NNN}_{YYMMDD}.md
  - 원고: research-public-talk/{NNN}_{슬러그}_원고_ver{N}_{YYMMDD}.md
  - 보조 리서치 6종 (research-bible/topic/illustration/experience/application/qa)
  - 골자 PDF (S01.공개강연/골자/...)

  R1~R20 + R-Conv + R-J1~J5 정량 grep 표 작성.
  골자 1:1 매핑 표 작성.
  보조 리서치 활용도 표 작성.
  HIGH 위반 발견 시 public-talk-script 재호출 권고 (수정 지점 라인 번호 명시).
  PASS 시 public-talk-builder 2차 재검수 진입 권고.

  결과 저장: research-public-talk/{NNN}_assembly_report_ver{N}_{YYMMDD}.md
  [할루시네이션 금지 공통 문구]"
```

PASS 후 단계 C-2 진입. HIGH 위반 시 단계 C 재실행 (자동 재작성 5회 한도).

정본: `research-meta/공개강연-자동화-구조.md` §2 R 룰 / `.claude/agents/publictalk-assembly-coordinator.md`.

### [단계 C-2] **public-talk-builder 2차 재검수 = 기획자 최종 QA** (Planner 2차 — 6단 방어 v2 ⑤단계)

public-talk-script 가 .md 원고 작성·자체 검수까지 마친 직후, **기획자가 한 번 더 본다**:

```
Agent(public-talk-builder)
  프롬프트: "[기획자 최종 QA 모드 — 2차 재검수] 공개 강연 {NNN}번 「{제목}」.

  단계 A 의 기획서 vs 단계 C 의 .md 원고 (research-public-talk/{NNN}_{슬러그}_원고_ver{N}_{YYMMDD}.md) 비교.

  체크 (R1~R20 + R-Conv + R-J 자동 grep 의무 — Phase 1-G, 2026-05-02):

  [정량 R 룰]
  - R1 글자수 6,500~9,000 (30분 = 25분 낭독 × 280자/분)
  - R2 시간 마커 ≥ 12 (서론·요점1·2·3·결론 + 30초 단위 분할)
  - R3 낭독 성구 6~8 + 언급 성구 4~6
  - R4 외부 14축 사용 ≥ 5축 (성서 적중 9 + 사유 촉발 5 중)
  - R5 임베드 이미지 ≤ 5 (wol/jwb 비율 ≥ 60%)
  - R6 청중 인터랙션 ≥ 12 (2~3분당 1개)
  - R7 사용자 NG list grep = 0 (가정 경배·여호와의 임재·수동적·신자 단독)
  - R8 서론 첫 3문장 — 후크·문제제기·연결 다리 모두 존재
  - R9 「」 출판물 인용 + URL ≥ 5
  - R10 신세계역 verbatim 인용 블록 (성구 6~8개 모두) 존재
  - R20 결론 행동 촉구 — 구체적 (날짜·시간·장소 또는 즉시 가능 행동)

  [의견 반영 R 룰]
  - R-Conv 결론에 "오늘 배운 3가지" 명시 (사용자 의견 ②)

  [예수의 가르침 5요소]
  - R-J1 간결성 — 평균 문장 길이 ≤ 28자 (한국어 호흡)
  - R-J2 논리 — 각 요점 = 성구 → 추론 → 결론 3단 구조
  - R-J3 사고 자극 질문 — 수사적 질문 ≥ 12개 (분당 0.4개)
  - R-J4 인상 깊은 수사 — 대조·반복·점층 등 ≥ 6회
  - R-J5 친숙한 비유 — 일상 비유 ≥ 3 (요점당 1개)

  [정성 체크]
  - 기획서의 30분 흐름·요점 시간·시각 자료 슬롯·낭독 위치 모두 원고에 반영됐나
  - 원고가 기획서 의도에서 벗어난 부분 (즉흥 추가·누락) 있나
  - 골자 파트 시간 ±0 어긋나는 단락 있나

  HIGH 위반 (R7 NG list / R10 verbatim 누락 / R-Conv 결론 3가지 누락 등) 발견 시 public-talk-script 재호출 (수정 지점 명시).
  R1~R6 정량 미달 시 해당 보조 에이전트 재호출 + script 재호출.
  모두 PASS 면 단계 D 빌드 진입.

  결과 저장: research-public-talk/{NNN}_planner_review_script_ver{N}_{YYMMDD}.md
  형식: R 룰별 측정값·PASS/FAIL·재호출 대상·근거 라인 번호 표 의무"
```

PASS 후 단계 D 빌드 진입. (이 단계가 누락되면 본체가 작성 망친 것을 누구도 못 잡고 빌드까지 감 → 이번 회차 전까지의 퇴보 원인 중 하나.)

### [단계 D] 저장 폴더 생성 + 스펙 파일

강연 번호와 슬러그로 저장 폴더 결정:

```python
import os, re
NUMBER = "179"  # 3자리 패딩
TITLE = "세상의 환상적인 것을 멀리하고 왕국의 실제적인 것을 추구하라"
SLUG = re.sub(r'[\s\-_\.]+', '', TITLE)[:40]  # 공백·특수문자 제거, 40자 이내
FOLDER = fr"~/Dropbox/02.WatchTower/02.▣ 집회(Meetings)/S01.공개강연/김원준 공개강연/{NUMBER}_{SLUG}"
os.makedirs(FOLDER, exist_ok=True)
```

**스펙 파일**: `_automation/content_publictalk_{NUMBER}.py` (기존 mid-study1 의 `content_YYMMDD.py` 방식 차용)

구조: `spec` 딕셔너리 — 공개 강연용 필드 (mid-study1 의 10분 구조를 30분으로 확장):

```python
spec = {
    "number": "179",
    "title": "세상의 환상적인 것을 멀리하고 왕국의 실제적인 것을 추구하라",
    "motto_scripture_ref": "요한1서 2:15",
    "motto_scripture_text": "[신세계역 verbatim]",
    "speaker": "김원준",
    "duration_sec": 1800,   # 30분
    "intro": [...],          # 서론 paragraph 리스트
    "point1": {
        "time_marker": "5'",
        "heading": "요점 1 한 문장",
        "paragraphs": [...],
    },
    "point2": { ... },
    "point3": { ... },
    "conclusion": [...],
    "time_marker_end": "29'",
}
```

paragraph 형식: `[(text, style), ...]`
style: `b`=bold, `r`=red(EE0000), `y`=yellow highlight, `t`=time marker, `i`=italic, `g`=gray scripture box, `B`=blue #0070C0

### [단계 E] docx + PDF 생성

**🛡 빌드 직전 자동 차단 (Phase 1-D, 2026-05-02)**: `build_publictalk.py` 가 `validators.validate_md_text()` 를 호출해 다음 HIGH 위반 1건이라도 발견 시 ValueError 로 docx 디스크 안착 차단:
- §2 금칙어 (신앙·복음·사역·간증·교회·세례 등 18개) — 정본 `shared/banned-vocabulary.md`
- §2-bis 사용자 NG list (가정 경배·여호와의 임재·수동적·신자 단독)
- §2-ter 추상·창작 의심 표현 (...의 임재 명사형·1차/2차 강림·성례·은혜의 보좌)

NWT verbatim 인용 블록 (`> *성구*` 또는 `> 성구`) 은 자동 제외. FAIL 시 public-talk-script 자동 재호출 (단계 F-2 의 자동 재작성 루프와 동일).



**빌더 파일 존재 여부 확인**:
```bash
ls "$HOME/Claude/Projects/Congregation/_automation/build_publictalk.py"
```

**빌더가 없으면** (최초 실행) — `build_treasures_talk.py` (mid-study1 빌더) 를 템플릿으로 복사하여 `build_publictalk.py` 생성. 차이점:
- 페이지 수 제약 없음 (10분 연설은 4페이지, 공개 강연은 자유)
- 시간 마커 구간이 6분 간격 (5'/11'/18'/25'/28')
- 삽화 임베드 선택사항 (골자에 있으면 포함)
- 30분 낭독 기준 폰트·여백 (13~14pt 맑은 고딕, 좁은 마진 0.5")

**빌드 실행**:
```bash
cd "~/Claude/Projects/Congregation/_automation"
"python3" content_publictalk_{NUMBER}.py
```

(빌더가 docx 생성 → docx2pdf 로 PDF 도 자동 생성 — mid-study1 패턴 그대로)

출력 경로 확인:
```
S01.공개강연/김원준 공개강연/{NUMBER}_{SLUG}/{NUMBER}_{SLUG}_ver1.docx
                                                       /_ver1.pdf
```

같은 파일명 존재 시 → `_ver2_`, `_ver3_` 순으로 버전 올림.

### [단계 F] 최종 감수 게이트 (4종 병렬, ⑥단계)

docx 생성 직후 **4종 감수 에이전트 한 메시지에 병렬 호출** (`shared/multi-layer-defense.md` ⑥단·`shared/quality-monotonic-policy.md` 준수):

```
Agent(fact-checker)
  프롬프트: "방금 생성한 공개 강연 docx ({docx_path}) 의 사실·인용·성구 표기 검증.
  ① 「파수대」/「깨어라」/「통찰」 등 출판물 인용이 wol.jw.org 에 실제 존재하는지 WebFetch 교차 확인 (호수·면·기사 제목 일치 필수).
  ② 신세계역 연구용 성구 본문 verbatim 대조 (URL 패턴 wol.jw.org/ko/wol/b/r8/lp-ko/nwtsty/...).
  ③ 외부 1차 자료 (역사·고고학·과학·유명인 발언) 출처 URL 유효성·날짜·인물 정확성.
  ④ 경험담이 공식 출판물 게재본인지 확인 — 창작·각색 발견 시 HIGH 위반.
  fake docid·존재하지 않는 출판물 인용은 즉시 제거 권고 (quality-monotonic-checker 의 C 축 MED 강등 trigger).
  결과: research-factcheck/publictalk_{번호}_{YYMMDD}.md
  [할루시네이션 금지 공통 문구]"

Agent(jw-style-checker)
  프롬프트: "방금 생성한 공개 강연 docx ({docx_path}) 의 공식 용어·호칭·어투 감수.
  신세계역 성구 표기, 경어체 일관성, 높임법 (여호와께서·예수께서),
  '교회→회중' · '하나님→여호와' · '목사→장로/봉사의 종' 준수,
  정치/민족 중립 표현 확인. `shared/banned-vocabulary.md` 정본 금칙어 자동 스캔.
  특히 공개 강연은 비증인 청중도 포함되므로 내부 용어를 과하게 쓰지 않았는지 점검.
  '형제 여러분/사랑하는 형제 자매 여러분' 등 공개 강연 금칙 호칭 발견 시 HIGH 위반.
  수정 지점 리스트 + 수정본을 research-style/publictalk_{번호}/ 에 저장.
  [할루시네이션 금지 공통 문구]"

Agent(timing-auditor)
  프롬프트: "방금 생성한 공개 강연 docx ({docx_path}) 의 낭독 시간을 단락별로 시뮬레이션.
  목표 30분 = 1800±120초 (quality-monotonic-policy 완화 기준 — quality > timing 우선).
  사회자 오프닝·마무리 120초 제외하면 강연자 낭독 1680초 내외.
  서론·요점1·2·3·결론 각 구간 시간 마커 vs 실제 예상 낭독 시간 비교.
  초과·부족분과 삭제/축약/유지 추천을 research-timing/publictalk_{번호}/ 에 저장.
  [할루시네이션 금지 공통 문구]"

Agent(quality-monotonic-checker)
  프롬프트: "방금 생성한 공개 강연 docx ({docx_path}) 의 품질 단조 증가 검증.
  비교 기준: 같은 강연 번호의 직전 ver docx (없으면 직전 강연 번호의 최신 ver).
  9축 메트릭 자동 측정: 글자수 / 성구 인용 수 / 출판물「」 인용 수 / 외부 14축 (성서 적중 9 + 사유 촉발 5) 사용 수 / 시간 마커 수 / 깊이 단락 수 / 임베드 이미지 수 / 청중 인터랙션 수 / 수사적 질문 수.
  기준: ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`).
  fact-checker 가 fake docid 출판 인용 제거했으면 C 축 MED 강등 (cross-reference).
  FAIL 1건 이상 시 자동 재작성 trigger (5회 한도). PASS 시 단계 G 로 진행.
  결과: research-quality/publictalk_{번호}_{YYMMDD}.md
  [할루시네이션 금지 공통 문구]"
```

**자동 재작성 (사용자 검수 의존 0)**: 4종 중 1건이라도 FAIL → 해당 영역 재호출 (style FAIL → public-talk-script 재호출 / quality FAIL → 보강 리서치 재호출 / timing FAIL 단독 + quality PASS → 통과). 최대 5회 한도 후 사용자 수동 검토 요청.

**quality > timing 우선순위**: timing-auditor 가 ±120초 초과를 보고해도 quality-monotonic-checker 가 PASS 이면 빌드 통과 (정책: `shared/quality-monotonic-policy.md`).

### [단계 F-2] 재감수 게이트 ⭐ 필수 (사용자 지침 2026-04-23)

수정 후 재빌드했으면 **반드시 감수 에이전트를 한 번 더 호출**해 최종 검증. "업그레이드했다"는 표현이 재감수 없이는 주장에 불과함. 기계적 치환이라도 새 오류·일관성 이탈·시간 영향을 만들 수 있음.

```
Agent(jw-style-checker)  # 재감수
  프롬프트: "재빌드된 docx ({new_docx_path}) 재감수.
  직전 감수(*_style_*.md)에서 지적된 N건 수정이 모두 반영되었는지 확인하고,
  새로 발생한 위반·일관성 이탈 여부 추가 점검.
  산출물: research-style/publictalk_{번호}_re{N}_style_{YYMMDD}.md
  [할루시네이션 금지 공통 문구]"

Agent(timing-auditor)  # 재감수
  프롬프트: "재빌드된 docx ({new_docx_path}) 재측정.
  직전 감사(*_timing_*.md)의 조정 제안 반영 후 실제 시간 변화 확인.
  산출물: research-timing/publictalk_{번호}_re{N}_timing_{YYMMDD}.md
  [할루시네이션 금지 공통 문구]"
```

**재감수 루프 상한**: 최대 2회 (`_re1_`, `_re2_`). 2회 후에도 중대 위반 남으면 사용자에게 수동 검토 요청.

### [단계 F-3] ⑨ 결과 처리 — 자동 재작성 분기 (Phase 1-F, 2026-05-02)

단계 F (4종 게이트) 와 단계 F-2 (재감수) 결과를 메인 Claude 가 자동 분기. **사용자 검수 의존 0** — mid-talk10 ⑨단계와 동일 패턴.

```
[단계 F·F-2 결과 → ⑨ 분기 로직]

if all 4 gates PASS:
    → 단계 G 보고 (최종 docx + 사용자 검수 단계로)
elif quality-monotonic PASS AND only timing FAIL (±120 초과 단순 분량):
    → 단계 G 보고 (quality > timing 우선 — 정책: shared/quality-monotonic-policy.md)
elif fact-checker FAIL:
    → public-talk-script 재호출 (수정 지점: research-factcheck/publictalk_{번호}_*.md 의 HIGH 항목)
    → 단계 D~F 재실행 (자동 재빌드 + 재감수)
elif jw-style-checker FAIL (NG list / 의심 어휘 / 금칙어):
    → public-talk-script 재호출 (해당 단어 치환 지시)
    → 단계 D~F 재실행
elif quality-monotonic FAIL (9축 중 직전 95% 미달 또는 절대 하한 미달):
    → 보강 필요 영역 파악 (글자수/성구/외부 14축/이미지 등) → 해당 보조 에이전트 재호출 → public-talk-script 재호출
    → 단계 D~F 재실행

루프 카운터: ver1 → ver2 → ver3 → ver4 → ver5 (자동 재작성 5회 한도)
ver5 후에도 1건 이상 FAIL → 사용자에게 BLOCKING 알림 (수동 개입 요청)
```

**재작성 trigger 매핑**:
| FAIL 게이트 | 재호출 대상 | 수정 지점 |
|---|---|---|
| fact-checker | public-talk-script | 가짜 출판물 인용 제거·성구 verbatim 정정 |
| jw-style-checker | public-talk-script | NG list / 금칙어 / 의심 어휘 치환 |
| timing-auditor (단독) | (skip — quality > timing) | — |
| quality-monotonic (글자수) | public-talk-script | 단락 보강 |
| quality-monotonic (성구) | scripture-deep + public-talk-script | 추가 성구 인용 |
| quality-monotonic (외부 14축) | illustration-finder + public-talk-script | 외부 1차 자료 추가 |
| quality-monotonic (이미지) | illustration-finder | 시드 이미지 다운로드 강제 |

**원준님 개입 = 입력 1회 + 검수 1회 = 총 2회** (mid-talk10 정본과 동일).

### [단계 G] 확인 및 보고

Claude 본체가 사용자에게 다음을 출력:

1. **생성된 docx/PDF 경로** (마크다운 링크)
2. **강연 개요**: 번호·제목·표어 성구·세 요점 한 줄씩
3. **리서치 출처 요약**: 연구 노트 N개, 파수대 N편, 통찰 N항목, 경험담 N개, 예화 N개
4. **감수 결과**:
   - jw-style-checker 이슈 N건 (핵심 N건 / 참고 N건)
   - timing-auditor 실측 예상 소요 시간 (초)
5. **다음 번호 추천** (선택): "다음은 {번호+1}번 만들어드릴까요?"

### [단계 H] Git 자동 커밋 (사용자 지침 2026-04-23)

원고 생성·감수 루프 완료 후 `congregation` repo 에 자동 커밋. 원격 있으면 push 도 시도.

```bash
cd ~/Claude/Projects/Congregation
# 공개 강연 관련 리서치·감수 산출물만 선택적으로 add
git add research-public-talk/ research-bible/ research-illustration/ \
        research-experience/ research-application/ research-qa/ \
        research-style/ research-timing/ .claude/agents/
# 변경 있으면만 커밋
if git diff --cached --quiet; then
  echo "[git] 변경사항 없음 — 커밋 생략"
else
  git commit -m "publictalk: {번호}번 {제목} ver{N} 생성 및 감수"
  # 원격 있으면 push 시도
  if git remote -v | grep -q origin; then
    git push origin main 2>&1 || echo "[git] push 실패 — 커밋은 로컬 유지됨"
  else
    echo "[git] 원격 없음 — 로컬 커밋만 유지 (Dropbox 동기화로 백업됨)"
  fi
fi
```

**원칙**: 변경 없으면 skip. 커밋 실패해도 원고 생성 결과는 디스크·Dropbox 에 안전히 남음. 생성된 docx/pdf 는 `02.WatchTower` 경로(별도 repo 아님)라 Dropbox 자체 이력에 의존.

## 📋 예외·엣지 케이스

- **번호가 1~194 범위 밖** → "공개 강연 번호는 1~194 범위입니다. 다시 입력해 주세요."
- **골자 PDF 가 로컬에 있으나 텍스트 추출 실패** → 사용자에게 PDF 텍스트 붙여넣기 요청
- **골자의 요점 개수가 2개 또는 4개** → 3개가 기본이지만 2/4개도 허용. 구조 유연 적용
- **빌드 실패** (Python 에러) → 에러 로그 전체 사용자에게 보여주고 재시도 여부 확인
- **docx2pdf 실패** — Word 가 설치돼 있어야 변환됨. 실패하면 docx 만 저장하고 "PDF 는 수동 변환 필요" 안내

## 📚 정본·참조 문서 (Phase 1-3 도입 후)

| 문서 | 용도 |
|---|---|
| `research-meta/공개강연-자동화-구조.md` | **확정 정본** — 호출 체인·R1~R20+R-Conv+R-J 룰 명세·자동 재작성 5회 한도 |
| `.claude/shared/banned-vocabulary.md` | 금칙어 §2 / 사용자 NG §2-bis / 의심 어휘 §2-ter — validators.py 자동 차단 |
| `.claude/shared/publictalk-formal-expressions.md` | **모범 정형 표현 사전** — 서론 후크 5종×3안 / 성구 유도 / 청중 인터랙션 / 결론 5단락 / 시각자료 도입 |
| `.claude/shared/quality-monotonic-policy.md` | 품질 단조 증가 9축 — quality > timing |
| `.claude/agents/publictalk-assembly-coordinator.md` | 단계 C-1 — R 룰 자체 grep + 골자 매핑 + 보조 리서치 활용도 |

`public-talk-script` 와 `publictalk-assembly-coordinator` 는 위 5개 문서를 모두 Read 후 작업 개시.

## 🔧 파이프라인 파일 (초기 구축 필요)

최초 실행 시 다음 파일들이 없을 수 있음. 있는지 확인하고 없으면 mid-study1 의 파일들을 템플릿으로 생성:

- `_automation/build_publictalk.py` — docx + PDF 포맷터 (30분 분량 레이아웃)
- `_automation/content_publictalk_{NUMBER}.py` — 각 강연별 스펙 (실행 시마다 생성)
- `_automation/build_all_publictalks.py` (선택) — 생성된 모든 공개강연 스펙 일괄 재빌드

## 🎯 기억할 점

- **한 번 실행 = 1편** — 주중 스킬의 "3주치" 로직 적용 안 함
- **기획자 모델** — public-talk-builder 가 설계도 + 에이전트 지시서 둘 다 만든다. 다른 에이전트들은 그 지시서대로 타겟된 재료만 수집.
- **골자 소스** — 로컬 PDF 우선, 없으면 사용자 제공
- **대화형 시작** — 번호 묻기 → 골자 소스 확인 → 제목·성구 1줄 확인 → 자동 진행
- **비증인 청중** — 공개 강연은 외부인도 대상. 내부 전문 용어 절제
- **버전 올리기** — 같은 이름 덮어쓰지 않고 `_ver2_`, `_ver3_` 으로 (비교용)
- **파일명 이름 금지** — "김원준" 같은 이름은 파일명에 포함하지 않음


---

## 산출물 존재 시 skip 정책 (필수)

스킬 진입 시 출력 폴더에 산출물이 이미 있는지 먼저 확인한다.

- **없음**: 정상 진행
- **있음 + 사용자 무명시**: 단정형 확인 1회 ("이미 있는데 새로 만드시나요?") → 답 없거나 No → **skip**
- **있음 + 사용자가 "재생성·업그레이드·버전 올려" 명시**: 버전 번호 +1 부여 후 신규 생성 (기존 파일 보존)

일괄 스킬(·)은 파트별로 자동 skip — 결과적으로 **없는 것만** 새로 만든다. 자세한 규칙: .
