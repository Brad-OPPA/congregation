# 회중 작업 공간 (congregation)

이 폴더는 김원준 형제의 **여호와의증인 회중 활동** 관련 맥락입니다. 사용자는 한국어 답변을 선호합니다.

## 한눈에 보는 구조 (2026-04-25 기준)

```
[원준님 입력]
   ↓ /weekly (월요일 1회) 또는 /midweek-now /next1 /next2 /next3
[일괄 스킬]  ← 산출물 묶음 확인 yes/no 1회
   ↓ Skill(단편, args="now/next1/next2/next3")
[단편 스킬 11개]  ← 묶음 컨텍스트 받으면 자체 묻기 X
   ↓ Agent(planner) → Agent(script) → Agent(보조 리서치) → 감수 게이트
[에이전트 32개]  ← research-*/{YYMMDD}/ 저장
   ↓ content_*.py 생성 → python build_*.py
[빌더 5개]  ← docx + PDF 자동 변환
   ↓ os.makedirs + doc.save
[디스크 출력]
```

### 출력 폴더 (생활과 봉사 공식 순서)

```
01.주중집회/
├── 01.성경에 담긴 보물/{01.10분 연설, 02.영적 보물 찾기, 03.성경 낭독}/{YYMMDD-MMDD}/
├── 02.야외 봉사에 힘쓰십시오/{01.학생 과제, 02.5분 연설}/{YYMMDD-MMDD}/
├── 03.그리스도인 생활/{YYMMDD-MMDD}/
├── 04.회중의 필요/{YYMMDD-MMDD}/
└── 05.회중 성서 연구/{YYMMDD-MMDD}/
02.주말집회/
└── 02.파수대 사회/{YYMMDD-MMDD}/
```

### 파일명 (한국어 prefix 통일)

| 파트 | 파일명 |
|---|---|
| 10분 연설 | `10분 연설_{주제}_YYMMDD.docx` |
| 영적 보물 찾기 | `영적 보물 찾기_YYMMDD.docx` |
| 성경 낭독 | `성경 낭독_YYMMDD.docx` |
| 학생 과제 | `학생 과제_{타입}_YYMMDD.docx` |
| 5분 연설 | `5분 연설_{주제}_YYMMDD.docx` |
| 그리스도인 생활 | `그리스도인 생활_{제목}_YYMMDD.docx` |
| 회중의 필요 | `회중의 필요_{주제}_YYMMDD.docx` |
| 회중 성서 연구 | `회중 성서 연구_훈{장}-{장}_YYMMDD.docx` |
| 파수대 사회 | `파수대 사회_YYMMDD.docx` |

재생성 시 `_verN_` 자동 부여 (디스크 최대 +1). publictalk 만 별도 정책.

---

## 🎤 10분 연설 자동화 (확정 정본 2026-05-01)

`/mid-talk10 {now|next1|next2|next3}` — 사용자 입력 1회 + 검수 1회. planner ① → 5 보조 ② → planner ③ → script ④ → assembly ⑤ → planner ⑥ → 빌드 ⑦ → 4종 게이트 ⑧ (FAIL 시 자동 재작성, 5회 한도).

> 📘 모든 세부 (호출 체인 / R1~R18 / 사용자 NG list / WOL 최근 10년 검증 / 12 메모리 정책): `research-meta/10분-연설-자동화-구조.md` (확정 정본)
> 📘 R1~R18 표준 패턴: `research-meta/10분-연설-표준패턴.md`

---

## 📜 파수대 연구 사회 자동화 (확정 정본 2026-05-02)

`/week-study` — 3주치 기본 (또는 `/week-study {특정주차만}`). 사용자 입력 1회 + 검수 1회. WOL 인덱스·docid → 베이스 스캐폴드 (`scrape_wt.py` + `spec_from_article()` 17블록 자동 파싱) → 5 보조 병렬 → add_cue 깊이 보강 (95% 미달 시 1차~4차 라운드, 최대 4회) → 재빌드 → 4종 게이트.

> 📘 모든 세부 (호출 체인 / W1~W12 / urllib timeout shim / add_cue 4 라운드 / 외부 14축 / 시행착오): `research-meta/파수대-사회-자동화-구조.md` (확정 정본)

핵심 차이 (vs 10분): 「」 출판물 인용 ≥ 10, 외부 14축 ≥ 3, block 단위 host_cue 주입.

---

## 🎙️ 공개 강연 자동화 (정본 단일화 2026-05-02)

`/publictalk {번호}` — 사용자 입력 1회 + 검수 1회. 메인 Stage 0 자율 종합 (골자 폴더 ls + 누적 메모리 + 이전 ver 검수) → 6 보조 → script → assembly → 빌드 → 4종 게이트.

> 📘 모든 세부 (호출 체인 / 22 영구 규칙 / R 33룰 / 모델 분배 / 시각자료 N 가변): `research-meta/공개강연-자동화-구조.md` (확정 정본)
> 📘 정형 표현: `.claude/shared/publictalk-formal-expressions.md`

---

## 📖 회중 성서 연구 사회 자동화 (확정 정본 2026-05-02)

`/cbs {now|next1|next2|next3}` — 사용자 입력 1회 + 검수 1회. cbs-planner ① (WOL "8. 회중 성서 연구" href 추적·docid 1102016XXX 검증) → 6 보조 병렬 ② → planner ③ → cbs-script ④ → planner ⑤ → content_cbs + WOL 이미지 → build_cbs_v10 ⑥ → 4종 게이트 ⑦ (timing 1800±120초, quality > timing).

> 📘 모든 세부 (호출 체인 / C1~C12 / publication symbol jy/lfb 분리 / 시간 마커 8개 / SPEC dict / 시행착오): `research-meta/회중성서연구-자동화-구조.md` (확정 정본)
> 📘 script.md → SPEC 부분 자동화 헬퍼 (60-72%): `_automation/script_to_content_cbs.py` + `test_script_to_content_cbs.py`

핵심 차이 (vs 10분/파수대): 30분 사회자, 낭독자 별도, 「훈」=lfb / 「예수」=jy 분리 표기, 시간 마커 8개 빨강 볼드, quality > timing 우선순위.

---

## 📒 자동화 구조 메타룰

스킬 6단 방어(v2) PASS ≥ 2 + 사용자 만족 → `research-meta/{스킬명}-자동화-구조.md` 정본 생성. 표준 형식 13개 항목·정착 4개·미정착 6개 목록: `research-meta/_template-and-meta-rules.md`

---

## 🚀 새 기기 복구 (BOOTSTRAP)

다른 컴퓨터에서 GitHub 백업만으로 0 → 100% 복구하려면:

> 📘 `~/Claude/Projects/Congregation/BOOTSTRAP.md` (확정 정본 2026-05-02)

핵심:

- **GitHub 가 진실의 원천** — `congregation` (META) + `congregation-automation` (\_automation) 양쪽 푸시 의무
- **Dropbox 는 docx/PDF 출력 동기화** — 빌더가 `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/` 에 출력
- **비밀 파일 GitHub 미포함** — `weekly_secrets.py`·`kakao_tokens.json` 새 기기에서 수동 재구성 (`weekly_secrets.example.py` 템플릿 활용)
- **하드코딩 경로 금지** — 모든 빌더는 `Path.home()` 패턴 (Mac·Linux 양립)

---

### 빌더 분류 (2026-04-25 기준)

- **정기 (매주 자동)**: 6개 — `mid-talk10` · `dig-treasures` · `cbs` · `mid-talk5` · `week-study` · `living-part`
- **부정기 (단독 호출)**: 3개 — `publictalk` · `local-needs` · `chair`
- **신규** (2026-04-29): `build_student_assignment.py` — 학생 과제 5종 (bible_reading + apply_conversation_start/follow_up/bible_study/explaining_beliefs) 통합 빌더. build_mid_talk5 helper import + LibreOffice PDF (build_treasures_talk.auto_convert_to_pdf 재사용)

### 정본 (모든 출력 경로·파일명·skip·버전 규칙의 진실)

`Congregation/.claude/shared/output-naming-policy.md`

### 🏆 회중의 필요 ver4 검증 표준 패턴 (2026-04-25 확정)

5단 흐름 (도입·요점 1·요점 2·요점 3·결론, 10분) / pptx 6장 / 어르신 친화 폰트 / 능동·격려 톤. 세부: `research-meta/local-needs-ver4-standard.md`

## 주요 활동

- 주중집회 (목요일) 원고 준비
- 주말집회 (일요일) 원고 준비
- 3주 선행 자료 생성 — 이번 주 + 다음 주 + 다다음 주

## 사용 스킬·에이전트

- **스킬** 18개 — 회중 로컬 `Congregation/.claude/commands/` (회중 폴더에서만 작동)
- **에이전트** 32개 — `.claude/agents/` = planner 8 / script 8 / 보조 리서치 8 / 특수 4 / 게이트 4
- **정기** (매주 자동) 6개: `mid-talk10` · `dig-treasures` · `cbs` · `mid-talk5` · `week-study` · `living-part`
- **부정기** (단독 호출) 3개: `publictalk` · `local-needs` · `chair`
- **게이트** ⑥ 단계 4종 병렬 (`fact-checker` + `jw-style-checker` + `timing-auditor` + `quality-monotonic-checker`), **quality > timing** 우선
- 전체 표 + 스킬↔에이전트 호출 체인: `research-meta/skills-and-agents-index.md`

## 훅 (자동 실행)

회중 워크스페이스 `.claude/settings.json` 에 등록.

| 이벤트 | 훅 | 동작 |
| --- | --- | --- |
| `Stop` (응답 종료) | `.claude/hooks/factcheck-numbers.py` | 회중 자료의 숫자·연도·통계 사실 재검증 |

## 데이터 출처

- 공식 자료: **wol.jw.org** (연구용 교재, 주간 파수대, 참조서)
- 참고서: 「파」·「익」·「통」·「예-1」·「훈」 책 등
- 원고는 wol.jw.org 의 본문·성구·참조자료를 근거로 생성

## 환경

- Python 3.10+ **필수** (파이프라인 빌더가 요구)
- 스킬 정의: 회중 로컬 `Congregation/.claude/commands/` (`~/.claude/commands/` 심링크)
- 에이전트 정의: 회중 로컬 `.claude/agents/` (32개 — 2026-04-30 assembly-coordinator 신규)
- 공유 정책: 회중 로컬 `.claude/shared/`
  - `multi-layer-defense.md` — 4단/6단 방어 프로토콜 (⑥ 4종 병렬, 2026-04-29 갱신)
  - `intro-and-illustration-quality.md` — 서론·예화·삽화 품질 표준
  - `skip-existing-policy.md` — 산출물 존재 시 skip 정책
  - `student-role-play-style.md` — 학생 시연 톤
  - **`quality-monotonic-policy.md`** ← 신규 (2026-04-29) — 슬롯별 절대 하한선 + 단조 증가 7축 점검 + 재작성 무한 루프 (5회 한도) + quality > timing 우선순위
- 관련 메모리: `project_meeting_pipelines.md` (mid-study1/2/3 + week-study 경로 맵)

## 원칙

- 원고는 wol.jw.org 공식 내용만 근거. 추측·외부 해석 최소화.
- 성구 참조·교재 인용 정확히. **"예배"** 단어 금지 — "집회" 등 공식 용어만.
- 회중 자료 감수는 변경분이 아닌 **세션 내 모든 신규/재빌드 docx 전체** 대상 (`jw-style-checker`).
- **작업 위임·병렬화 우선** — 3단계/3파일 이상은 서브 에이전트로 위임, 의존성 없는 작업은 한 메시지 안에서 병렬 호출. 메인 컨텍스트는 의사결정·통합·git 에 보존. 세부: 메모리 `feedback_delegate_to_subagents.md`.
- **상투적 청중 호명·수사 질문 금지** — "여러분도 …해 보신 적 있으십니까?" 류 9가지 표현 일체 금지. 모든 script 에이전트 + jw-style-checker 가 차단. 세부: 메모리 `feedback_script_no_cliche.md` · `intro-and-illustration-quality.md` §A-4-bis.
- **품질 단조 증가 (2026-04-29 도입, Phase A·B·C·D·E 정착)** — 새 빌드의 정량 메트릭 (글자수·성구·출판물「」·외부 14축·시간 마커·깊이 단락·**이미지·구성 표준**) 이 직전 주차 동일 슬롯 docx 보다 같거나 풍부해야 함. quality-monotonic-checker 가 **9축** 자동 NO-GO + 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** (timing FAIL 이라도 quality PASS 면 통과). **fact ↔ quality cross-reference**: fact-checker 가 fake docid 출판 인용 제거 시 quality C 축 MED 강등. **이미지 silent skip 차단**: illustration-finder 가 `download_image.py` 로 시드 이미지 자동 다운로드 의무. 정책: `shared/quality-monotonic-policy.md`
- **메인 Claude 직접 정정 금지 (Phase E, 2026-05-01)** — 메인은 docx·content_*.py·script.md·outline.md 등 콘텐츠 파일을 직접 Edit/Write 하지 않는다. 의심 어휘·라벨 오류 발견 시 반드시 jw-style-checker (또는 해당 script 에이전트) 호출 → WOL WebFetch 검증 → script 재작성 → Agent 가 content_*.py 변환 → 빌더 (`validators.py` 자동 차단) 재실행. 메인의 직관 정정·임시 변환 우회 차단. 정책: `shared/main-claude-edit-policy.md`. 정본 단일화: `shared/banned-vocabulary.md` (금칙어) + `shared/comment-label-standard.md` (라벨).
- **영적 보물찾기 자동화 v2 (Phase E v2, 2026-05-01)** — 매주 자동 빌드 시 동일 퀄리티 보장. 자동화 구조 세부사항 (전체 흐름·5 보조 자료 수집 의무·검증 자동화 표·hook 작동 시점·정량 메트릭·회귀 적용 절차·단순/복잡 정정 분리) 은 `shared/dig-treasures-automation.md` 참조. 핵심 강제 메커니즘: validators 빌드 시 자동 차단 (라벨·금칙어·사용자 NG·의심 어휘) + gem-coordinator (R1~R10 측정) + Stop hook 3종 (factcheck·quality-loop·fact-loop) 자동 재호출 강제. 다각도·14축·깊이·4축 균형은 정보 측정만 (자연스러움 우선, 강제 X). 메인 Claude 정정은 단순(WOL fetch 정답 명확) 직접 / 복잡(해석 필요) Agent 위임.
