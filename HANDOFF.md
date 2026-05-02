# 🚚 세션 인수인계 — 2026-05-02 정본

이 파일은 **새 세션이 시작될 때 자동으로 읽어야 합니다**.
직전 세션 노트는 `HANDOFF_260425_overnight.md` (보존, 참고용).

---

## 📌 최근 세션 (2026-05-02 후반) — CBS 자동화 정본 확정 + BOOTSTRAP·메타룰 정착

### 1. 260514 (5/14 목) CBS 「훈」 84-85장 빌드 — 6단 방어(v2) PASS

- `/cbs next1` — 84장 "예수께서 물 위를 걸으시다" + 85장 "안식일에 눈먼 사람을 고치시다"
- 흐름: cbs-planner ① → 6 보조 병렬 ② (qa·scripture·topic·application + experience·illustration) → planner ③ 1차 재검수 → cbs-script ④ → planner ⑤ 2차 재검수 → 빌드 ⑥ → 4종 게이트 ⑦
- 게이트 v1: timing PASS / quality PASS / fact HIGH 4 / style HIGH 1 → 정정 후 v2 모두 PASS
- 정정 사항 (5건 HIGH + 3건 MED): 마 14:30·벧전 3:15 verbatim, 「예수」 44장 표현, 요 9:7 노트 출처, 라벨 em dash, "진리의 은혜", 플라나스테 어원, 「예수」 53장 야경시
- 산출: `~/Dropbox/.../05.회중 성서 연구/260511-0517/회중 성서 연구_훈84-85장_260514.docx` (312 KB) + PDF (653 KB)
- vs 260507 (옛, 비표준 파일명): 글자 +40% / 출판물 +850% / 외부 14축 +275% / 깊이 단락 +120%

### 2. publication symbol jy/lfb 분리 정책 (정본 확정)

- **회중 통칭 "훈"** = 실제 발행물 `lfb` (Learn From the Bible / 「내가 좋아하는 성경 이야기」), docid `1102016XXX`
- **「예수」 책** = `jy` (Jesus — The Way), docid `1102014XXX`
- 옛 docx (260205·260423·260507) 모두 jy 표기 잘못 — 신규 빌드부터 lfb 정본
- script 표기 분리 의무: 전면 = "훈"·"「내가 좋아하는 성경 이야기」" / 횡단 = "「예수」 책 NN장"
- fact-checker 가 publication symbol 검증 의무

### 3. CBS 자동화 구조 문서화 (10분 연설·파수대·공개강연과 동일 패턴)

- 신규: `research-meta/회중성서연구-자동화-구조.md` (확정 정본, 13 섹션)
  - 호출 체인 ① ~ ⑨ / C1~C12 검증 룰 / publication symbol 분리 정책 / 시간 마커 8개 / SPEC dict 표준 / Mac 경로 / 시행착오 / 14축 후보 / 베이스라인 메트릭
- `CLAUDE.md` 갱신: **📖 회중 성서 연구 사회 자동화 (확정 정본 2026-05-02)** 섹션 추가

### 4. 자동화 구조 메타룰 확정

- 스킬이 정본 확정되면 (= ⑥ 4종 게이트 PASS, 변경 X 약속) `research-meta/{스킬명}-자동화-구조.md` 별도 파일 생성
- 13 항목 표준 포맷 (핵심 원칙·호출 체인·검증 룰·WOL URL·시간 마커·SPEC·Mac 경로·게이트·정정 정책·시행착오·14축·베이스라인·개정 이력)
- 정착 4개: 10분 연설·파수대·공개강연·CBS / 미정착 6개: dig-treasures·mid-talk5·living-part·mid-student1~4·local-needs·chair

### 5. 새 기기 복구 안전장치 (BOOTSTRAP)

- 신규: `BOOTSTRAP.md` — GitHub 백업만으로 0→100% 복구하는 9-Step 절차
  - 의존성 (Python·LibreOffice·폰트·gh·Dropbox)
  - repo clone (META + \_automation 양쪽)
  - 심링크 (`~/.claude/commands` → `Congregation/.claude/commands`)
  - `weekly_secrets.py` 수동 재구성 (`weekly_secrets.example.py` 템플릿 활용)
  - Kakao OAuth 재발급 (`kakao_auth.py`)
  - 동작 검증 4개 (build import · PDF 변환 · Gmail SMTP · Kakao 토큰)
- 신규: `_automation/weekly_secrets.example.py` — 빈 값 템플릿 (GitHub 커밋 안전)
- `CLAUDE.md` 갱신: **🚀 새 기기 복구 (BOOTSTRAP)** 섹션 추가

### 6. _automation 양쪽 repo push 완료

- `congregation` (META): `799e75a` CBS 260514 6단 방어(v2) PASS (30 files / +5503)
- `congregation-automation`: `6fd155c` raw_hun_84/85 + Mac 경로 새 함수
- 추가 commit (이 세션 끝에): BOOTSTRAP + CBS 자동화 구조 + CLAUDE.md 갱신

---

## 📌 이전 세션 (2026-05-02 전반) — 파수대 사회 자동화 정본 확정

### 1. 260517 (5월 11–17일) 파수대 사회 1주 빌드

- 사용자 요청: `/week-study 다다음주만`
- 기사: docid `2026321`, "온 우주에서 가장 높으신 분인 여호와를 신뢰하십시오", 시 83:18
- 17 블록 + 5 소제목 + 4 삽화 + 3 복습 질문
- **흐름**: WOL 스크래핑 (urllib timeout → requests shim) → 베이스 docx → 5 보조 리서치 병렬 → add_cue 4 라운드 깊이 보강 → 재빌드 → jw-style 금칙어 0건 검증
- **품질 메트릭 (vs 260510 baseline)**: chars 109% / 성구 96% / 출판물「」 100% / 외부 14축 8개 ✅ 모두 PASS
- **산출**: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/02.주말집회/02.파수대 사회/260511-0517/파수대 사회_260517.docx` (566 KB) + PDF (1.05 MB)
- **리서치 자료**: `research-{topic,bible,application,illustration,experience}/260517/`

### 2. 파수대 자동화 구조 문서화 (10분 연설과 동일 패턴)

- 신규: `research-meta/파수대-사회-자동화-구조.md` (확정 정본, 11 섹션)
  - 호출 체인 ① ~ ⑩ / W1~W12 검증 룰 / urllib shim 표준 코드 / add_cue 4 라운드 / 외부 14축 후보 / 자산 위치 / 시행착오 정리
- `CLAUDE.md` 갱신: **📜 파수대 연구 사회 자동화 (확정 정본 2026-05-02)** 섹션 추가 (10분 연설 섹션 직후)
- 다음 주차 (`/week-study`) 호출 시 동일 퀄리티 자동 보장

### 3. 환경 메모

- macOS Python 3.14 의 urllib 이 wol.jw.org 에 timeout 발생 — `requests` 로 monkey-patch shim 표준화 (정본 §4)
- pip 모듈 설치는 `--user --break-system-packages` 필수 (Homebrew Python PEP 668)

---

## ⚡ 새 세션 첫 할 일

```bash
pwd  # 기대: /Users/brandon/Claude/Projects/Congregation (META — 이 폴더)
     # 또는 ~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/ (출력 폴더)
git status -s
git log --oneline -5
```

## 🧭 환경 — Mac 단독 (2026-05-01 마이그레이션 완료)

| 항목 | 위치 |
|---|---|
| **메타 워크스페이스 (정본)** | `~/Claude/Projects/Congregation/` |
| **빌더 코드** | `~/Claude/Projects/Congregation/_automation/` (별도 git repo: congregation-automation) |
| **출력 폴더 (docx/PDF)** | `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/`, `02.주말집회/` (Dropbox 동기화 유지) |
| **글로벌 슬래시 명령** | `~/.claude/commands/` → 심링크 → `Congregation/.claude/commands/` (회중 폴더에서만 작동) |
| **회중 에이전트** | `Congregation/.claude/agents/` (32개) |
| **Hook command** | `python3 -X utf8 "$CLAUDE_PROJECT_DIR/.claude/hooks/*.py"` |
| **PDF 변환** | LibreOffice (`/Applications/LibreOffice.app` + Homebrew `soffice`) 우선 + docx2pdf fallback |
| **폰트** | 맑은 고딕 (`~/Library/Fonts/malgun.ttf`) + Noto Sans KR 백업 |
| **Python** | 3.14.4 (Homebrew) — python-docx 1.2.0 / lxml 6.1.0 / Pillow 12.2.0 / python-pptx 1.0.2 / requests 2.33.1 |

> **마이그레이션 이력**: 2026-04-30 ~ 05-01 — Dropbox 옛 META + WS `_automation/` + claude-migration 백업 380MB 휴지통 이동 (`~/.Trash/dropbox-cleanup-260501/`, 회복 가능). 구 노트북 (Windows yoone) Claude Code 는 사용자 직접 삭제 예정 — Mac=GitHub 동기화 확인 완료 (잔여 push 없음).

## 🛠 핵심 인프라 (2026-04-29 정착)

### 워크스페이스 분리

- **META** (`Dropbox/ClaudeFile/Congregation/`) — repo `congregation`
  - `.claude/agents/` (30개), `.claude/shared/` (7개 정책), `.claude/hooks/` (2개)
  - `research-*/` (subagent 산출물 14종)
- **WS** (`Dropbox/02.WatchTower/01.▣ 수원 연무 회중/`) — repo `congregation-automation`
  - `_automation/` (Python 빌더 + send_weekly_mail + content_*.py)
  - `01.주중집회/`, `02.주말집회/` (사람용 docx + PDF 출력)

### `/weekly` 1단계 정책 (2026-04-29 갱신)

- **1단계** (기본): docx 생성 + **본인(eltc9584@gmail.com) 에게만 메일** + 카톡 "검수 요청"
- **2단계** (`/weekly send`): 본인 검수 후 5명 (본인 포함) 발송 + 카톡 "발송 완료"

### 발송 인프라 4 버그 수정 (2026-04-29)

- NFC 정규화 (macOS HFS+/APFS NFD 한글 매칭)
- `VER_RE` trailing `_?` 지원 (`_ver14_` 같은 파일)
- gems 슬롯 monday 만 매칭 (thursday 제거)
- yymmdd 중복 제거 (10분 연설 ver suffix 처리)

## 📊 직전 세션 (2026-04-29) 누적 변경

### 양쪽 repo push 완료

- `congregation` (META): `7cdcff0`+ (agents 30 + CLAUDE.md + README + 9 mld reference)
- `congregation-automation`: `f25e532`+ (README_WEEKLY 변경 이력 + 코드 5개 commit)

### 상세
1. next2 (5/14 목 + 5/17 일) 4 슬롯 풀세트 빌드 (10분 연설·영적 보물·CBS·파수대 사회) — 6단 방어 통과, 4 docx + 4 PDF (맑은 고딕 임베드)
2. 5명 [정정] 메일 발송 5/5 성공 (12 첨부, 슬러그 4종 정확)
3. LibreOffice 26.2.2 설치 + 빌더 4개 패치 (LibreOffice 우선 + docx2pdf fallback)
4. 맑은 고딕 + Noto Sans KR 폰트 사용자 등록
5. send_weekly_mail.py 5건 정정 (NFC + VER_RE + gems + yymmdd + 1단계 정책)
6. /weekly 스킬 1단계 정책 갱신 (`~/.claude/commands/weekly.md`)
7. 9개 에이전트에 multi-layer-defense reference 일괄 추가
8. CLAUDE.md 카운트 29→30 갱신
9. .gitignore 정리 (`.claude/.claude/`, `_debug_*`, `_preview_*`, `*.out.txt`)
10. HANDOFF 통합 갱신 (이 파일)

## ✅ 2026-05-01 마이그레이션 완료 — Mac 단독 환경 정착

5단계 정리 작업 모두 완료:

| # | 항목 | 상태 |
|---|---|---|
| 1 | 구 노트북 git push 잔여 확인 | ✅ Mac=GitHub 동기화 (양 repo `752880e`/`4fa97ff` 일치, 잔여 0) |
| 2 | Mac git pull | ✅ pull 할 것 없음 (이미 최신) |
| 3 | Dropbox 옛 META 삭제 (`Dropbox/ClaudeFile/Congregation/`) | ✅ 휴지통 이동 (152 MB) |
| 4 | WS `_automation/` 삭제 | ✅ 휴지통 이동 (12 MB) |
| 5 | 문서 갱신 (HANDOFF + CLAUDE.md Mac 단독) | ✅ 이 갱신으로 완료 |

추가 정리:
- ✅ `~/.claude/skills/` broken 심링크 제거
- ✅ `~/.claude/commands/` → `Congregation/.claude/commands/` 심링크 정상 작동 (21개 슬래시 명령)
- ✅ `mid-talk10/SKILL.md` 우리 정책 갱신 새 위치로 복사
- ✅ Dropbox claude-migration + _claude-global 백업 정리 (211 MB + 5.1 MB 휴지통)
- 휴지통 위치: `~/.Trash/dropbox-cleanup-260501/` (380 MB) — 30일 후 자동 영구 삭제

**남은 책임 (사용자 직접)**:
- 구 노트북 (Windows yoone) Claude Code 앱 삭제 — Mac 정본 동기화 끝났으니 안전. Dropbox 옛 위치는 이미 사라짐 (Mac 휴지통 이동 동기화)

**관련 메모리**: `~/.claude/projects/-Users-brandon/memory/project_old_laptop_cleanup_pending.md`
**관련 커밋**: `c5cd946` (congregation-automation) — 빌더 경로 Mac/Windows 양립 (이미 push 됨)

---

## 🎯 다음 세션 진입점

### 잔존 작업 (우선순위 낮음)

| # | 항목 | 영향 |
|---|---|---|
| 1 | `build_student_assignment.py` 빌더 미작성 | 학생 과제 #1~4 빌드 시 build_mid_talk5 패턴 응용 중 |
| 2 | Task #9: 훅 강화 (마감 전 미완 task 자동 점검) | 카톡/메일 빠뜨림 같은 실수 재발 방지 |
| 3 | Noto Sans KR 빌더 폰트 변경 | 선택적 — 현재 맑은 고딕 등록으로 충분 |
| 4 | publictalk_132_V2 + publictalk_033·040 등 untracked | 다른 세션 산출물, 진행 중인지 끝났는지 미확인 |

### 🛠 토큰·시간 최적화 — 이월 작업 (2026-05-02 보류, publictalk 작업 충돌)

**전체 계획**: `~/.claude/plans/mutable-plotting-platypus.md` (사용자 승인 완료)
**전제**: CBS 품질 그대로 유지 (단조 증가, HIGH 0, NWT verbatim, 할루시네이션 0)
**예상 효과**: 토큰 -34%, 시간 -37%, 매 세션 컨텍스트 -29%

**보류 사유**: A·B·C 모두 publictalk 관련 파일을 동시 편집해 publictalk 스킬 조정 작업과 충돌 위험. publictalk 마무리되면 재개.

| 영역 | 작업 | 충돌 |
|---|---|---|
| A | `Congregation/CLAUDE.md` 385→150줄 + `research-meta/{automation-meta-rules,local-needs-ver4-standard,agents-index,automation-flows-summary}.md` 4개 신규 | "공개 강연 자동화 (확정 정본)" 섹션 압축 — publictalk 정책 변경 중이면 충돌 |
| B | `.claude/shared/agent-common-rules.md` 신규 + 32 agents 머리말 일괄 치환 | publictalk 관련 10+ 에이전트 머리말 변경 |
| C | 8 agents model 다운그레이드 (Opus→Sonnet 6 + Opus→Haiku 2): illustration-finder, qa-designer, wol-researcher, slides-builder, role-play-scenario-designer, public-talk-builder, assembly-coordinator, gem-coordinator | `public-talk-builder` 직접 수정 |
| D | `_automation/script_to_content_cbs.py` 신규 + cbs SKILL.md 7단계 갱신 | publictalk 무관, 충돌 X — **이번 세션에서 완료 (60-72% 부분 자동화)** |

#### 영역 D 완료 결과 (2026-05-02 부분 성공)

- 헬퍼: `_automation/script_to_content_cbs.py` (1,222줄) + 회귀 `_automation/test_script_to_content_cbs.py` (165줄)
- 회귀 테스트 결과: 260514 68.7% / 260521 71.7% / 260528 60.7% leaf 매치 (전부 FAIL)
- **자동 추출 완벽**: version·timers·reading_paragraphs·key_scripture·required_question.question·illustration.scenes 구조·thanks_line·transition_out 등 구조적·verbatim 필드
- **합성 필요 (Agent 보강)**: extra_deep_points·scripture_commentary[].relation·reference_materials·illustration.bg_text/answer/short_application·takeaway.q1/q2 — script.md 의 보강 단락이 SPEC dict 에서 다른 어휘·다른 단락 구조로 큐레이션됨
- 실용 효과: cbs-script Agent 가 SPEC 작성 부담 ~30-40% 감소 (구조 골격 자동, 합성만 채움). 1 Agent 호출 완전 제거는 못 함.

#### Path A — 100% 자동화 향후 작업 (publictalk 작업 후)

100% 1:1 변환 가능하려면 cbs-script 에이전트가 다음을 script.md 에 verbatim 박도록 형식 변경 필요:

- `### 사회자 깊이 단락` (4-5개 산문) → `extra_deep_points`
- `### 성구 해설` (각 성구별 1-2단락) → `scripture_commentary[].relation`
- `### 출판물 인용 표` (label/url/summary 3컬럼 markdown table) → `reference_materials`
- `### 삽화 배경 설명` + `### 삽화 적용` → `illustration.scenes[].bg_text/answer`
- `### 두 삽화 통합 적용` → `illustration.short_application`
- `### 참조 성구 정리` + `### 여호와에 대해 배움` → `takeaway.q1_scripture_lesson`/`q2_about_jehovah`

cbs-script.md (에이전트 정의) 의 출력 형식 섹션을 위 헤더 패턴으로 강화 + cbs SKILL.md 5단계의 cbs-script 호출 프롬프트에 명시. 작업 시간 ~1-2시간. 적용 후 헬퍼 회귀 테스트 100% PASS 가능.

**재개 진입점** (publictalk 작업 완료 후):

```
계획 ~/.claude/plans/mutable-plotting-platypus.md 의 영역 A·B·C 진행해 줘.
```

### 즉시 가능

- `/midweek-now` 등 다른 스킬 — 새 주차 자료 생성
- `/local-needs` — 장로의회 주제 받으면 즉시
- `/publictalk` — 공개 강연 골자 받으면 즉시

## 📞 새 세션 시작 스크립트

```
HANDOFF.md 읽고 git status 확인해줘.
```
