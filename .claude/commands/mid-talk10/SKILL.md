---
name: mid-talk10
description: 주중집회 ①번 "성경에 담긴 보물 — 10분 연설" 원고 1편을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3` (없으면 대화형). **6단 방어(v2) 프로토콜(`.claude/shared/multi-layer-defense.md`) + 서론·예화·삽화 품질 표준(`.claude/shared/intro-and-illustration-quality.md`)** 준수 — ① Planner 지시서(🟢 착수 블록 복사 의무 포함) → ② 서브 자체 검수(🔴 종료 블록) → ③ Planner 1차 재검수 → ④ Script 작성+자체 검수 → ⑤ Planner 2차 재검수(기획자 최종 QA) → ⑥ fact-checker·jw-style-checker·timing-auditor·quality-monotonic-checker 최종 게이트. treasures-talk-planner → 5개 보조 리서치(scripture-deep·publication-cross-ref·illustration-finder·experience-collector·application-builder) → Planner 1차 재검수 → treasures-talk-script → **assembly-coordinator (조합·매핑·R1~R10 1차 검증, 옵션 B 2026-04-30 도입)** → Planner 2차 재검수 → `content_YYMMDD.py` 스펙 변환 → `build_treasures_talk.py` 로 4페이지 docx/PDF 렌더 → 4종 최종 감수 (fact·jw-style·timing·quality-monotonic). 트리거 "/mid-talk10", "10분 연설 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# mid-talk10 — 성경에 담긴 보물 10분 연설 (단일 주차, 6단 방어(v2))

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx + PDF (자동 변환)

## 이 스킬의 범위
- 10분 연설 **한 편** (한 주차) 만 생성
- 3주치 일괄 생성은 `/midweek-now`·`/midweek-next1/2/3` 또는 `/weekly` 가 담당
- 다른 주중 파트(영보·학생과제·5분연설·생활·CBS)는 각자 스킬 별도

## 🛡 품질 원칙 — 6단 방어(v2) 프로토콜 + 서론·예화·삽화 품질 표준

### 이 스킬이 준수하는 공유 파일 2개

1. **`.claude/shared/multi-layer-defense.md`** — 6단 방어 프로토콜(v2). ① 지시서 → ② 서브 자체 → ③ Planner 1차 재검수 → ④ Script 자체 → ⑤ **Planner 2차 재검수(기획자 최종 QA)** → ⑥ 최종 감사 3종.
2. **`.claude/shared/intro-and-illustration-quality.md`** — 서론·예화·삽화 품질 표준. 이 스킬(`mid-talk10`) 의 차등 적용표 행:
   - 14축 활용 하한 **3축**, 서론 후크 후보 **3~5개**, 요점당 예화 후보 **2~3개**
   - 적절성 8필터 **필수 전부**
   - 최근 10년 JW 출판물 회피 **권장**
   - 🟢 착수 전 리마인드 블록 + 🔴 종료 후 자체 검수 블록 모든 서브·Script 에이전트에 **의무**

아래 모든 Agent 호출 프롬프트에는 "공유 파일 2개 Read 의무 + 🟢🔴 블록 복사·PASS 의무" 가 **기본 전제**.


**원준님 지침(2026-04-24): 품질 최우선, 오류 0 목표.**

이 스킬의 모든 에이전트 호출은 `.claude/shared/multi-layer-defense.md` 의 6단 방어(v2) 프로토콜에 따른다. 실행 전에 해당 문서를 반드시 Read 하여 각 단계의 포맷·파일명·재호출 한도를 확인.

**4단 요약**:
1. Planner → 각 서브에게 **지시서** 전달 (`meta.yaml` 의 `instructions_to_subresearchers` 키)
2. 서브 에이전트 **자체 검수** (`_selfcheck.md` 작성)
3. Planner **재검수** (`_planner_review.md` 작성, 미흡 시 해당 서브 재호출)
4. **최종 게이트** — fact-checker + jw-style-checker + timing-auditor

## 인자 규약

| 인자 | 대상 주차 |
|---|---|
| `now` | 오늘 기준 이번 주 목요일 집회 |
| `next1` | 다음 주 |
| `next2` | 2주 뒤 |
| `next3` | 3주 뒤 |
| (없음) | 원준님께 대화형으로 "몇째 주?" 묻기 |

## ⚠ CRITICAL: 콘텐츠 수집 규칙 (WOL-first 의무사항)

> "wol.jw.org 접속 → 집회 → 생활과 봉사 → 해당 주차 확인 → 10분 프로 링크를 따라가서 그 본문을 기반으로 작성"

### 절대 규칙
1. 매주 WOL 주차 인덱스부터 시작: `https://wol.jw.org/ko/wol/dt/r8/lp-ko/YYYY/M/D`
2. "성경에 담긴 보물" 섹션 href 를 그대로 따라갈 것. 주제·성구·참조 자료는 매주 바뀜.
3. 장 번호/제목만 보고 추측 금지. WOL 주차 페이지가 유일한 진리 소스.
4. 내부 링크 (보통 `/pc/r8/lp-ko/YYYYNNNN/N/0`) 를 실제로 열고 본문 확인.
5. 주차 링크 타임아웃 → 재시도 3회까지. 그래도 실패하면 원준님께 확인.

## 🚫 할루시네이션 절대 금지 (모든 에이전트 공통)

1. wol.jw.org · 신세계역 연구용 성서 · 공식 JW 출판물에서 **실제로 확인한 내용만** 산출물에 넣는다.
2. 확인 못 한 항목은 `[확인 필요 — WOL 원문 복사]` placeholder.
3. 모든 인용은 출처 URL + 출판물 이름 + 호수/면/항 포함.
4. 성구는 신세계역 연구용 verbatim. 기억 재구성 금지.
5. 경험담은 공식 출판물 실제 게재분만.
6. 예화·비유도 출처 명시.

모든 Agent 호출 프롬프트 말미에 공통 문구 첨부:

> ⚠ 할루시네이션 절대 금지: 훈련 데이터 기억이 아니라 wol.jw.org·신세계역 연구용 성서·공식 JW 출판물에서 **실제로 확인한 내용만** 저장할 것. 확인 못 한 항목은 `[확인 필요]` placeholder. 모든 인용은 출처 URL + 출판물 이름/호수/면/항 포함. 성구는 verbatim. 경험담·예화도 출처 명시 필수.
>
> ⚠ 6단 방어(v2) 프로토콜 준수: `.claude/shared/multi-layer-defense.md` 를 먼저 Read 해서 당신의 역할(①/②/③/④ 중 어느 단계인지) 확인 후 작업.

## 📖 저작권 정책

jw.org 및 wol.jw.org 는 공개 자료이므로 저작권 고려 없음 (2026-04-22). 장문 verbatim 허용. 출처 URL 명시는 필수.

## 실행 단계 (6단 방어(v2) 흐름)

### 1. 주차 확정 + 폴더 찾기/생성
- 인자에서 YYMMDD 계산 (목요일 집회일)
- 베이스: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/`
- 폴더 네이밍: `YYMMDD-MMDD`. 기존 재사용.
- 시드 이미지 `{YYMMDD}_treasures.jpg` 확인.

### 2. 🤖 ① + ② 단계 — treasures-talk-planner 호출 (지시서 포함)

Planner 가 wol 파싱 + 아웃라인 설계 + **각 서브에게 내릴 지시서** 를 meta.yaml 에 함께 적는다.

```
Agent(treasures-talk-planner)
  프롬프트: "{YYMMDD} 주차 '성경에 담긴 보물 — 10분 연설' 기획 (6단 방어(v2) ① 단계).

  주차 인덱스 https://wol.jw.org/ko/wol/dt/r8/lp-ko/YYYY/M/D 에서 시작,
  주제·부제·요점 3개·핵심 성구·참조 자료 문자열·삽화 URL 수집 및 서론·요점·결론 아웃라인 설계.

  ⚠ 저장 경로: `research-plan/treasures-talk/{YYMMDD}/` 로 저장.
  outline.md + meta.yaml 2파일.

  meta.yaml 필수 키 (스킬 관례):
    week_date: YYMMDD
    bible_reading_range: '...'
    topic, subtopic
    points: [3개 — 각 요점 제목·핵심 성구·참조 자료 약어+URL]
    scripture_refs: [성구 목록]
    wol_publication_refs: [참조 자료 약어 + URL]
    research_dirs:
      bible:        research-bible/{YYMMDD}/
      topic:        research-topic/{YYMMDD}/
      illustration: research-illustration/{YYMMDD}/
      experience:   research-experience/{YYMMDD}/
      application:  research-application/{YYMMDD}/

  ⭐⭐ 추가 필수 키 — instructions_to_subresearchers (6단 방어(v2) ① 단계):
    각 서브 에이전트에게 구체적으로 무엇을 어떻게 수집할지 지시서를 기록.
    포맷은 .claude/shared/multi-layer-defense.md 의 예시 참조.
    키: scripture-deep / publication-cross-ref / illustration-finder /
        experience-collector / application-builder (5개)
    각 값은 (중점·우선 범위·피하기 항목) 포함 자연어 지시.

  ⚠ 할루시네이션 절대 금지: (공통 문구)
  ⚠ 6단 방어(v2) 프로토콜: 당신의 ① 단계 책임은 '지시서 작성'. 지시서가 구체적일수록
    서브 에이전트의 실수가 줄어든다. 애매한 문구 금지."
```

planner 완료 후 메인 Claude 가 meta.yaml 을 Read 해서 서브 호출에 활용.

**참조 자료 약어 해독**:
- `「파」` = 파수대 연구용. `「파09」 9/15` = 2009년 9월 15일호. `「파18.11」` = 2018년 11월호
- `「익」` = 여호와께 가까이 가십시오
- `「통」` = 통찰 1·2권
- `「예-2」` = 예수 — 길이요 진리요 생명 2권

### 3. 🤖 ② 단계 — 5개 보조 리서치 병렬 (지시서 수신 + 자체 검수)

meta.yaml 의 instructions_to_subresearchers 를 각 서브 호출 프롬프트에 **인라인 포함**. 한 메시지에 5개 Agent 블록 동시 호출:

```
Agent(scripture-deep)
  프롬프트: "meta.yaml(research-plan/treasures-talk/{YYMMDD}/meta.yaml) 를 먼저 Read.
  그중 scripture_refs 와 **instructions_to_subresearchers.scripture-deep** 지시서를 준수하여
  각 성구에 대해 신세계역 연구용 본문·연구 노트·상호 참조·원어·역사 배경 심층 조사.
  research-bible/{YYMMDD}/ 에 성구별 .md 파일로 저장.

  ② 자체 검수 단계 (필수):
  수집 완료 후 각 성구를 wol.jw.org 연구용 URL 로 **재조회** 하여 글자 단위 대조.
  research-bible/{YYMMDD}/_selfcheck.md 작성 (포맷은 multi-layer-defense.md 참조).
  HIGH 위반 있으면 스스로 수정 후 재검수. 2회 시도해도 실패하면 status: FAILED.

  ⚠ 할루시네이션 절대 금지 / ⚠ 6단 방어(v2) 프로토콜 준수."

Agent(publication-cross-ref)
  프롬프트: "meta.yaml + instructions_to_subresearchers.publication-cross-ref 준수.
  meta.yaml 의 topic 으로 wol 출판물 횡단 검색. 파수대·깨어라·통찰·예수책·하느님의 사랑·JW 방송 관련 단락,
  출처 URL 포함, research-topic/{YYMMDD}/cross-ref.md 에 저장.

  ② 자체 검수: 각 인용 단락의 URL 재조회해서 본문 일치 확인.
  research-topic/{YYMMDD}/_selfcheck.md 작성.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."

Agent(illustration-finder)
  프롬프트: "meta.yaml + instructions_to_subresearchers.illustration-finder 준수.
  meta.yaml 의 points 3개에 맞는 자연·역사·일상 비유 요점당 2-3개 후보. 서론·결론 도입 예화 포함.
  research-illustration/{YYMMDD}/ 에 저장.

  ② 자체 검수: 유명인 발언·수치·연도 일차 자료 교차 검증.
  research-illustration/{YYMMDD}/_selfcheck.md 작성.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."

Agent(experience-collector)
  프롬프트: "meta.yaml + instructions_to_subresearchers.experience-collector 준수.
  meta.yaml 의 points 3개 주제에 부합하는 공식 경험담(연감·파수대·JW 방송) 요점당 1-2개.
  출처 URL·실명 주의 표시. research-experience/{YYMMDD}/ 저장.

  ② 자체 검수: 각 경험담 출처 URL 재조회해서 실존·실명·연도 일치 확인.
  research-experience/{YYMMDD}/_selfcheck.md 작성.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."

Agent(application-builder)
  프롬프트: "meta.yaml + instructions_to_subresearchers.application-builder 준수.
  meta.yaml 의 points 3개에 대한 실생활 적용점 (가정·직장/학교·회중·개인 영성).
  각 요점별 3-5개 상황 + 자기점검 질문. research-application/{YYMMDD}/ 저장.

  ② 자체 검수: 공식 출판물이 제안한 적용은 출처 URL 재확인.
  research-application/{YYMMDD}/_selfcheck.md 작성.
  ⚠ 할루시네이션 금지 / 6단 방어(v2) 준수."
```

### 4. 🤖 ③ 단계 — Planner 재검수 (리서치 결과 판정)

모든 서브 완료 후 planner 를 **재호출** 하여 지시서 대비 적합성 점검:

```
Agent(treasures-talk-planner)  [재검수 모드]
  프롬프트: "당신이 앞서 지시서를 내린 5개 서브 에이전트의 산출물을 재검수 (6단 방어(v2) ③ 단계).

  다음 경로의 _selfcheck.md 와 실제 산출물을 모두 Read:
    - research-bible/{YYMMDD}/        (+ _selfcheck.md)
    - research-topic/{YYMMDD}/        (+ _selfcheck.md)
    - research-illustration/{YYMMDD}/ (+ _selfcheck.md)
    - research-experience/{YYMMDD}/   (+ _selfcheck.md)
    - research-application/{YYMMDD}/  (+ _selfcheck.md)

  meta.yaml 의 instructions_to_subresearchers 지시서 대비 다음 점검:
    A. 지시서의 중점 범위·키워드가 실제 수집에 반영됐는가
    B. 피해야 할 항목이 잘못 포함되지 않았는가
    C. 각 서브의 _selfcheck 가 통과했는가 (FAILED 없는가)
    D. 요점 3개에 대해 모든 카테고리 (성구·출판물·예화·경험담·적용) 가 골고루 수집됐는가
    E. 서로 모순되는 내용은 없는가

  결과를 `research-plan/treasures-talk/{YYMMDD}/_planner_review_research.md` 에 저장:
    - 전체 판정: PASS | NEEDS-RERUN
    - 미흡 항목 목록: (항목·미흡 이유·재수집 필요 서브·재지시사항)
    - 통과 항목 요약

  NEEDS-RERUN 이면 재지시사항을 구체적으로 적어라."
```

`PASS` 면 5 단계로. `NEEDS-RERUN` 이면 해당 서브 재호출 → 다시 3 → 4. 재호출 1회까지만 허용 (그래도 실패하면 원준님께 보고).

### 5. 🤖 ① + ② 단계 — treasures-talk-script 호출 (지시서 + 자체 검수)

```
Agent(treasures-talk-script)
  프롬프트: "research-plan/treasures-talk/{YYMMDD}/outline.md 와 meta.yaml 을 먼저 Read.
  meta.yaml 의 research_dirs 5개 폴더의 {YYMMDD} 하위 파일과 _selfcheck.md 들을 모두 Read 로 소비.
  그리고 _planner_review_research.md 도 Read 해서 planner 가 확인한 통과 항목만 사용.

  각 요점의 narrative 구조 (6단계):
    1) 흥미 유발 — 질문/상황/대조/인용/비유 중 매 요점마다 다른 방식
    2) 성구 유도
    3) 성구 낭독 (신세계역 연구용 verbatim)
    4) 성구 설명 (research-topic 의 실제 논지 기반)
    5) 예 (research-illustration/application 또는 research-experience/topic)
    6) 교훈 연결

  추가 원칙:
    - 결론 직전 '자문해 볼 점' 삽입
    - 서술형, 한 문장 60음절 이내, 약 2000~2400자

  결과는 research-plan/treasures-talk/{YYMMDD}/script.md 에 저장.

  ② 자체 검수 단계 (필수):
  script 작성 후 자기가 인용한 모든 성구·출판물·경험담을 원본 소스로 재조회해서 대조.
  research-plan/treasures-talk/{YYMMDD}/_selfcheck_script.md 작성.

  ⚠ 할루시네이션 금지 / ⚠ 6단 방어(v2) 프로토콜 준수."
```

### 6. 🤖 ③ 단계 — Planner script 재검수

```
Agent(treasures-talk-planner)  [script 재검수 모드]
  프롬프트: "script.md 와 _selfcheck_script.md 를 Read. outline.md 대비 다음 점검:
    A. 요점 3개 모두 6단계 구조로 완성됐는가
    B. 성구 인용이 신세계역 연구용 verbatim 인가
    C. 참조 자료가 research-topic 의 실제 논지를 근거로 하는가 (창작 아닌가)
    D. 실생활 예·경험담이 research-application/experience 에서 온 것인가
    E. 흥미 유발 방식이 요점마다 다른가

  결과를 `research-plan/treasures-talk/{YYMMDD}/_planner_review_script.md` 에 저장:
    - 판정: PASS | NEEDS-REWRITE
    - 수정 필요 단락: (단락·이유·수정 방향)

  NEEDS-REWRITE 이면 script 에이전트에게 전달할 수정 지시를 구체적으로 적어라."
```

`PASS` 면 7 단계로. `NEEDS-REWRITE` 면 script 에이전트 재호출 (수정 지시 포함). 1회까지.

### 7. content_YYMMDD.py 스펙 변환 (Claude 본체)

script.md 를 Read 해서 paragraph 리스트·시간 마커·각주 번호(p 스타일)·references 리스트로 **변환만** 담당. 원고 내용을 새로 쓰지 않는다.

저장: `~/Claude/Projects/Congregation/_automation\content_YYMMDD.py`.
기존 `content_260423.py` 등을 템플릿으로 사용.

paragraph = `[(text, style), ...]` 스타일: `b` bold / `r` red(EE0000) / `y` yellow / `t` time marker / `i` italic / `g` gray / `h` heading / `p` 윗첨자 각주 마커.

시간 마커 예: `1'30"`, `4'`, `6'`, `7'`, `8'30"`, `9'30"`.

#### 각주 references (필수)

```python
"references": [
    {"num": 1, "label": "...", "url": "https://wol.jw.org/..."},
    {"num": 2, "label": "「파수대」 2018년 11월호 ...", "url": "..."},
    {"group": "기본 자료"},
    {"label": "WOL 주차 페이지", "url": "..."},
    {"label": "성구 — 신세계역 연구용", "url": "..."},
],
```

규칙: 본문 `"p"` 마커 숫자 = references 의 `num`. wol.jw.org / jw.org 도메인만. 번호는 본문 순서대로.

### 8. docx/PDF 렌더

```bash
cd "~/Claude/Projects/Congregation/_automation"
python content_YYMMDD.py
python -c "from docx2pdf import convert; convert('입력.docx', '출력.pdf')"
```

출력: `10분 연설_{주제}_YYMMDD.docx` 및 `.pdf`.
- 같은 날짜 재빌드 시 덮어쓰기 (`_verN_` 표기는 사용자가 "재생성·업그레이드·버전 올려" 명시했을 때만)
- 파일명에 "김원준" 금지

### 9. 🤖 ⑥ 단계 — 최종 통합 감사 (4종 병렬)

```
Agent(fact-checker)
  프롬프트: "{docx_path} 와 script.md 에 대해 성구 verbatim · 출판물 인용 실존 ·
  URL 유효성 · 경험담 출처 · 유명인 발언 독립 검증.
  결과 research-factcheck/{YYMMDD}/factcheck_treasures.md 에 저장.
  ⚠ 훈련 기억으로 검증하지 말 것 — 반드시 WebFetch 로 원본 재조회."

Agent(jw-style-checker)
  프롬프트: "{docx_path} 감수.
  필수 금칙어: 예배/사역/신앙/간증/복음(단독)/평안(설명문).
  신세계역 표기·경어체·높임법·정치 중립 점검.
  결과 research-style/{YYMMDD}/ 저장."

Agent(timing-auditor)
  프롬프트: "{docx_path} 낭독 시간 단락별 시뮬레이션. 목표 10분(600초) 대비
  초과·부족분과 삭제/축약/유지 추천을 research-timing/{YYMMDD}/ 저장."
```

**재빌드 판정**: 3개 중 HIGH 위반 1건 이상이면 재빌드 강제. script 재작성 → docx 재렌더 → 동일 3개 재호출. 2회까지. 그래도 실패하면 원준님께 수동 확인 요청.

### 10. 확인 및 보고
- 생성된 docx/PDF 경로 마크다운 링크
- 4페이지 검증 (PDF 읽기)
- ③ 재검수 통과 여부 + ④ 최종 감수 HIGH/MEDIUM/LOW 카운트
- 재빌드 횟수

## 포맷 필수 요소
- 13pt 맑은 고딕, 좁은 마진 (0.5 인치)
- 정확히 4페이지
- 시간 마커: 우측 정렬, 빨간 볼드, 노란 하이라이트
- 성구: 회색 하이라이트, 들여쓰기
- 노란 하이라이트 = 흥미 유발/핵심 문장, 빨강 = 강조 단어, 볼드 = 요점
- 삽화 이미지 임베드 (`{YYMMDD}_treasures.jpg`), 중앙 정렬, 약 4.2 인치 폭
- 이탤릭 회색 삽화 캡션

## 파이프라인
- `_automation\build_treasures_talk.py` — docx 포맷터
- `_automation\content_YYMMDD.py` — 주차별 내용

## 개정 이력
- 2026-04-24 v2 — 6단 방어(v2) 프로토콜 적용 (원준님 품질 최우선 지침)
- 2026-04-23 v1 — planner/script 2단 체인으로 초안

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/mid-talk10` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `10분 연설_…YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3` 또는 `mid-study1`) 호출 시

일괄 스킬이 묶음 확인 단계에서 이미 yes/no 받았으므로 **자체 단정형 확인 묻지 않는다**. 일괄에서 받은 결정 그대로 실행:

- **skip 결정** → 호출 자체가 발생 안 함 (일괄이 이미 걸러냄)
- **신규 빌드** → 정상 진행
- **`--from-batch=ver_up`** 컨텍스트 받으면 → `_verN_` (N = 디스크 최대 + 1) 자동 부여

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3 + `.claude/shared/output-naming-policy.md` §4·§4-bis.

---

## 🎤 본문 정책·영구 규칙·R 룰·정형 표현 — 정본 참조

> **2026-05-02 압축** — 본문 정책·R 룰·정형 표현·6단계 narrative·서론 이미지 옵션·4종 게이트 결과 처리는 **정본 일원화**. 토큰 절감 + 회귀 방지.
>
> | 영역 | 정본 |
> |---|---|
> | 12 영구 규칙 (본문/예 분리·출처 호명 X·6단계 narrative·결론 3가지 의무·책무 분리 등) | `research-meta/10분-연설-자동화-구조.md` |
> | R1~R18 정량 룰 명세 (글자수·성구·출판·외부 14축·시간 마커·깊이 단락 등) | `research-meta/10분-연설-표준패턴.md` |
> | 모범 PDF 정형 표현 (서론 후크·성구 유도·결론 행동 촉구) | `research-meta/10분-연설-자동화-구조.md` §정형 표현 |
> | 서론 이미지 옵션 (옵션 A 골자 본문 / 옵션 B 외부 후크) | 정본 §서론 이미지 |
> | 4종 게이트 자동 분기 (fact·style·timing·quality-monotonic) | 정본 §자동 재작성 (5회 한도) |
> | 사용자 NG list + 의심 어휘 | `.claude/shared/banned-vocabulary.md` §2-bis / §2-ter |
> | 관련 메모리 7종 | `~/.claude/projects/-Users-brandon-Claude/memory/feedback_speech_*.md` |
>
> treasures-talk-planner · treasures-talk-script · assembly-coordinator 는 **위 정본 의무 Read** 후 작업.
