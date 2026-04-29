# Congregation
수원 연무 회중 — JW 집회 원고 자동화

## 워크스페이스 구조 (Windows + Mac 양립)

이 저장소는 **Claude 메타 (정의·정책·리서치 결과)** 만 보관. Python 빌더와 출력 docx 는 별도 워크스페이스 `02.WatchTower/01.▣ 수원 연무 회중/` 에 있음 (별도 git repo: `congregation-automation`).

| 종류 | 위치 |
|---|---|
| **Claude 메타** (이 repo) | `Dropbox/ClaudeFile/Congregation/` — agents · skills · shared · research-* |
| **Python 빌더 + 출력** (별도 repo) | `Dropbox/02.WatchTower/01.▣ 수원 연무 회중/` — `_automation/` + `01.주중집회/` · `02.주말집회/` |

## hook 환경변수 (Mac/Windows/WSL 양립)

`.claude/settings.json` 의 hook command 는 절대경로 대신 `$CLAUDE_PROJECT_DIR` 환경변수를 사용. PC 별 settings.local.json 이 필요 없도록.

```json
"command": "python3 -X utf8 \"$CLAUDE_PROJECT_DIR/.claude/hooks/factcheck-numbers.py\""
```

## 변경 이력

### 2026-04-29 — 품질 단조 증가 시스템 (Phase E 완료) — 삽화 강제 + 구성 표준 + fact·quality 충돌 조정

**원준님 핵심 발견** ("10분연설 삽화도 생략, 회중성서연구 삽화도 없고 구성 자체도 문제"):
- next2 10분 연설 docx 의 `word/media/` = 0개 (삽화 누락)
- 시드 이미지 `260514_treasures.jpg` 파일 부재 → 빌더 silent skip
- illustration-finder 가 WOL 삽화 URL 텍스트로만 수집, 실제 jpg 다운로드 X
- quality-monotonic-checker 7축에 **이미지 카운트·구성 표준** 없음
- fact-checker 가 fake docid 출판 4편 제거 → quality 출판 절대 하한 (5) 미달 → 무한 루프

**Phase E 해결**:
- **`quality_check.py` 9축 확장** — measure_docx 에 `images` (zip word/media 카운트) 추가, 7축 → 9축 (A 글자/B 성구/C 출판/D 외부/E 마커/F 구조/G 깊이/H 이미지/I 구성 표준)
- **`SLOT_FLOOR` 조정** — 10분 연설·CBS images ≥ 1 강제, 출판 절대 하한 완화 (5→3 등) + C 축 MED 강등 (fact 충돌 회피)
- **`download_image.py` 신규** — WOL/jw.org 이미지 자동 다운로드 헬퍼 (URL → jpg 파일)
- **`illustration-finder.md`** — 시드 이미지 자동 다운로드 의무 명시, 슬롯별 저장 경로 정의
- **`quality-monotonic-checker.md`** — 9축 + fact cross-reference 정책 명시
- **`build_treasures_talk.py`** — image_path 명시했는데 파일 없으면 stderr 경고 (silent skip 차단)

**검증**: next2 10분 연설 (이미지 0) → quality_check.py 자동 H FAIL HIGH 정확 판정 (이전엔 안 잡혔음).

### 2026-04-29 — 품질 단조 증가 시스템 (Phase D 완료, 시스템 전면 정착)

오케스트레이터 + 메모리 베이스라인:
- **7 일괄 SKILL.md** 정책 추가 — midweek-now·next1·next2·next3 + mid-study1·2·3 (weekly 는 commands/ 위치, 이미 적용 완료)
- **메모리 `project_quality_baseline.md`** 신규 — 슬롯별 최근 PASS 빌드 메트릭 누적, 베이스라인 자동 갱신 (장기 단조 증가 추적)
- **메모리 `feedback_phase_step_protocol.md`** 신규 — 다단계 작업 시 매 phase 끝마다 5스텝 (CLAUDE.md/README/commit/push) 의무 정착
- 영향: 모든 21 스킬 + 30 에이전트 (이번 세션 추가 분 포함) 자동 단조 증가 보장 정착 완료

### 2026-04-29 — 품질 단조 증가 시스템 (Phase C 완료)

부정기 + 학생 + 특수 빌더 — 모든 단편 스킬 자동 보장:
- **부정기 5 SKILL** — mid-talk5 · living-part · local-needs · chair · publictalk
- **학생 4 SKILL** — mid-student1·2·3·4
- **4 planner** — student-talk · student-assignment · living-part · local-needs
- **5 script** — student-talk · student-assignment · living-part · chair-script-builder · public-talk-script
- **3 추가 보조** — qa-designer · wol-researcher · public-talk-builder
- **3 특수 빌더** — prayer-composer · slides-builder · role-play-scenario-designer
- 영향: 모든 단편 스킬 (총 13개) 자동 단조 증가 강제

### 2026-04-29 — 품질 단조 증가 시스템 (Phase B 완료)

- **정기 4 슬롯 SKILL.md 정책 섹션 추가** — mid-talk10 · dig-treasures · cbs · week-study (글로벌 `~/.claude/skills/`)
- **4 planner ⑤ 단계 책무 추가** — treasures-talk-planner · spiritual-gems-planner · cbs-planner · watchtower-study-planner (직전 주차 비교 NEEDS-REWRITE 판정 의무)
- **3 script ④ 베이스라인 확인 추가** — treasures-talk-script · spiritual-gems-script · cbs-script (시작 전 직전 script.md Read)
- **5 보조 에이전트 ② 단조 증가 의무** — scripture-deep · publication-cross-ref · illustration-finder · experience-collector · application-builder (직전 산출물 비교, 부족 시 PARTIAL 처리)
- 영향: `/weekly` 다음 호출부터 자동 품질 단조 증가 강제 (사용자 검수 의존 0)

### 2026-04-29 — 품질 단조 증가 시스템 도입 (Phase A)

- **신규 정책 `shared/quality-monotonic-policy.md`** — 슬롯별 절대 하한선 (10분·영보·CBS·파수대 등 11종) + 단조 증가 7축 점검 (글자·성구·출판·외부 14축·시간 마커·구조·깊이 단락)
- **신규 에이전트 `quality-monotonic-checker`** — ⑥ 단계 4번째 감수자. fact-checker·jw-style-checker·timing-auditor 와 4종 병렬. FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0
- **신규 헬퍼 `_automation/quality_check.py`** — measure_docx + compare_quality 헬퍼 함수
- **`shared/multi-layer-defense.md` 갱신** — ⑥ 단계 3종 → 4종 명시 + quality > timing 우선순위
- **`agents/timing-auditor.md` 갱신** — ±60 → ±120초 완화 (사회자 실전 ±10% 변동 흡수) + quality 우선 명시
- 검증: next2 파수대 (-77% 사례) → quality_check.py 자동 NO-GO 정확 판정 (HIGH 3 / MED 1)

### 2026-04-29 — Mac 환경 적응 + 발송 인프라 안정화 + 에이전트 정책 일관화 + 학생 과제 빌더 정착

- **`build_student_assignment.py` 신규 작성** — 학생 과제 5종 (bible_reading + apply_conversation_start/follow_up/bible_study/explaining_beliefs) 통합 빌더. 회중 자동화의 유일한 미작성 빌더 정착. (`congregation-automation` repo 참조)

- 회중 워크스페이스 `.claude/settings.json` hook command 환경변수화 (Windows 절대경로 → `$CLAUDE_PROJECT_DIR`)
- next2 (5/14·5/17) 4 슬롯 풀세트 빌드 (10분 연설·영적 보물·CBS·파수대 사회) — 6단 방어 통과, 4 docx + 4 PDF (맑은 고딕 임베드)
- 5명 [정정] 메일 발송 5/5 성공 (12 첨부 정확)
- **/weekly 1단계 정책 갱신**: 카톡만 → **본인에게만 메일+카톡** (회중 4명은 본인 검수 후 2단계 발송). 첨부 슬러그·HTML 본문·인사말 직접 검수 가능
- 세부 인프라 변경 (LibreOffice + 빌더 + send_weekly_mail collect/슬러그 NFC/VER_RE/yymmdd 중복 등): `02.WatchTower/01.▣ 수원 연무 회중/_automation/README_WEEKLY.md` 의 "변경 이력" 참조
- **에이전트 30종 전체 점검** — frontmatter·shared 정책 reference 검증. 9개 에이전트 (cbs-planner·cbs-script·chair-script-builder·living-part-planner·living-part-script·local-needs-planner·public-talk-script·scripture-deep·timing-auditor) 에 `multi-layer-defense.md` reference 한 줄 일괄 추가. CLAUDE.md 카운트 29→30 갱신 (public-talk-script 추가 명시).
- Hook 스크립트 (factcheck-numbers.py, skill-source-reminder.py) syntax + manual 실행 검증 PASS.
