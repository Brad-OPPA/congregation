# 🚚 세션 인수인계 — 2026-05-03 정본

이 파일은 **새 세션이 시작될 때 자동으로 읽어야 합니다**.
직전 세션 노트는 `HANDOFF_260425_overnight.md` (보존, 참고용).

---

## 📌 최근 세션 (2026-05-03 후반·심야 자동) — 5-Layer 신뢰 모델 완성

### 1. Layer 5 NWT verbatim 검증 도착 — `_automation/nwt_cache.py` + `verify_spec_scriptures`

- 모듈: `_automation/nwt_cache.py` (66 책 한국어 이름→번호, ref 파서, WOL 챕터 fetch + 절별 추출, 캐시 저장, verbatim 비교)
- 캐시 위치: `_automation/nwt_cache/{book:02d}_{chap:03d}.json`
- WOL HTML 패턴: `<span id="v{B}-{C}-{V}-{N}" class="v">…</span>` — 한 절이 여러 span 으로 분할되는 경우 (시구 단위) 모두 합쳐 한 절로 저장
- 정규화: NFC + smart quote → straight + `+`·`*` 각주 마커 제거 + 공백 통일
- validators API: `verify_spec_scriptures(spec, builder_name, fail_hard=True)` — spec 재귀 walker 가 5종 키 쌍 인식 (`ref+verbatim`, `ref+text`, `verse_ref+verse`, `wol_scripture_ref+wol_scripture`, `scripture_ref+scripture_text`)
- 4 빌더 hook 완료 — `NWT_VERIFY=0` 환경변수 opt-out

### 2. Layer 4 정정 — 3 빌더의 silent swallow 제거 (가짜 PASS 차단)

- build_cbs_v10 / build_spiritual_gems / build_watchtower 가 `verify_docx_against_inventory_auto` 를 `try/except: pass` 로 감싸 SeedImageHardFail 까지 silence — Layer 4 게이트 무력화 상태였음
- 정정: try/except 제거. 카탈로그 미존재는 wrapper 가 silent skip, anchor 불일치만 propagate.
- build_treasures_talk 는 처음부터 정상 → 4 빌더 모두 작동 일관

### 3. Layer 5 audit — 기존 spec 의 진짜 verbatim 미일치 catch

- CBS 260521 spec: 4 인용 중 2건 진짜 미일치
  - **요한복음 11:25** — claimed "예수께서 **그에게** 말씀하셨다" (1단어 추가)
  - **요한복음 13:34, 35** — 마침따옴표 누락
- 영보·10분 260521/260604: 0건 (또는 ref+verbatim 쌍 자체 없음 — 별도 형식)
- CBS 260521 spec 직접 정정 X (Phase E main-claude-edit-policy 준수). 다음 CBS 빌드부터 Layer 5 자동 차단 → cbs-script 재작성 강제.

### 4. Agent prompt 의무 명시 — 4 정의 갱신

`treasures-talk-script.md` / `spiritual-gems-script.md` / `cbs-script.md` / `watchtower-study-planner.md` 머리말에 "🔒 Layer 0/1/5 카탈로그·NWT 의무" 블록 추가:

- preflight 산출물 + content_inventory 첫째 Read
- mwb anchor = truth source, 카탈로그 외 자료 임의 인용 금지
- 동영상 cue verbatim·성구 NWT verbatim·삽화 src 매칭만
- "anchor 따라 자연스럽게 — agent 자기식 부풀림 X"

### 5. Preflight 5 슬롯 추가 — 학생·5분·생활·회중필요·사회자

`preflight.py` 에:

- `preflight_mid_student(week, num)` — 학생 과제 1~4 (mwb 야외봉사 섹션 h3 슬롯 검증)
- `preflight_mid_talk5(week)` — 5분 연설
- `preflight_living_part(week)` — 생활 파트 + subtype 자동 분류 (talk/discussion/video/interview/qna)
- `preflight_local_needs(week, topic)` — 장로의회 주제 미입력 시 manual 안내
- `preflight_chair(week, lfb_docids=...)` — 모든 주중 슬롯 합산

총 9 슬롯 지원: mid-talk10·cbs·week-study·dig-treasures·mid-student1~4·mid-talk5·living-part·local-needs·chair

### 6. _ARCHITECTURE.md 완성도 표 갱신

5-Layer 모두 ✅ — 사용자 검수 부담 0 도달.

### 7. source_archive 시스템 도착 — docx 옆 _source/ 폴더 자동 생성

사용자 요청 ("앞으로 소스관련 폴더 만들어서 삽화를 꼭 같이 저장해") 반영:

- 신규: `_automation/source_archive.py` — 빌드 직후 docx 옆 `_source/` 디렉토리 자동 생성
- 4 주요 빌더 (`build_treasures_talk` / `build_cbs_v10` / `build_spiritual_gems` / `build_watchtower`) build 끝부분에 hook 추가
- 보존 내용:
  - `spec.py` — spec dict Python literal 직렬화 (사람이 읽기 좋음)
  - `spec_meta.json` — 빌드 시각·MD5·이미지 목록·script.md 위치
  - `images/` — spec 안의 모든 image_path 실제 binary 사본 (MD5 함께)
  - `script.md` — research-plan/{slot}/{week}/script.md 사본 (있을 때)
- 효과: WOL 사이트 변경·이미지 교체로 인한 재현 불가 차단 + 사용자가 docx 검수 시 옆 폴더에서 즉시 spec/이미지 확인

### 9. Layer 4.5 흐름·순서 강제 차단 (사용자 가르침 — 빌더 architecture 보강)

원준님 가르침: **"빌더와 에이전트가 문제없이 만들도록 강제로 차단해야"**.

매번 spec 한 줄씩 수동 정정 ≠ 진짜 자동화. 빌더가 빌드 시점에 HARD GATE 로 차단해야 같은 mistake 재발 0.

**신규 validators (`FlowOrderHardFail`)**:

- `verify_image_flow_auto()` — preflight `_preflight_{slot}.json` 카탈로그의 이미지 등장 순서 ↔ spec 의 `intro_image_path` / `image_path` 위치 매칭. 첫 그림 = 도입 (과거 본보기), 둘째 그림 = 결론 (현대 적용). 거꾸로 박으면 차단.
- `verify_spec_flow_direction()` — spec 단락 안 시간 역순 4종 패턴 차단:
  1. "담대 → 처음부터 가능?·정반대" 결과 후 시작 의문법
  2. "M년을 사이에 둔 옛 인물 모습 그대로" 현대→과거 비유
  3. "오늘 우리 → 과거 인물 그대로" 비교
  4. "이 모습 = X 그대로" 현대 그림 → 과거 인물 동일시

**4 빌더 hook**:

- `build_treasures_talk`: image_flow + flow_direction (10분은 두 그림이 흐름의 핵심)
- `build_cbs_v10` / `build_spiritual_gems` / `build_watchtower`: flow_direction (시간 정방향만)

**agent prompt** (`treasures-talk-script.md`) 머리말에 정형 구조 + 이미지 위치 의무 박힘.

**End-to-end 검증 (3 케이스 모두 PASS)**:

- 이미지 swap → 빌드 차단 ✅
- 시간역순 텍스트 삽입 → 빌드 차단 ✅
- 정상 spec → regression 없이 통과 ✅

`_ARCHITECTURE.md` 에 Layer 4.5 신규 섹션 명시. 같은 mistake (시간 역순, 이미지 거꾸로) 가 어떤 future agent run 에서도 build 시점에 자동 차단됨.

### 10. 10분 260604 spec 정정 + 재빌드 — 사용자 명시 정정

사용자 보고: "삽화 위치도 틀리고, 삽화 소개도 없어  아예삭제하고 다시 새로 만들어"

근본 원인:

- mwb 6월호 10분 슬롯 = 정확히 2장 (page 200 본문 + page 202 도입). agent 가 page 200 을 "표지 삽화" 로 mislabel
- intro 끝 → 도입 삽화 (mwb_202) 가 갑자기 등장, 대본에 소개 멘트 없음
- before_illustration 1줄로 짧음 (본문 삽화 도입 부실)

정정 (직접 — 사용자 명시 우선):

- intro 끝에 도입 삽화 소개 1단락 추가 ("문 앞에서 노크하기 전, 한 형제가 잠시 멈춰 조용히 기도하는 모습…")
- illustration_caption 의 "표지 삽화" → "본문 삽화" 라벨 정정
- before_illustration 2단락으로 확장 (예레미야 자세·청중 반응·함께 계신 분 — 본문 삽화 흐름 미리 짚어줌)
- 재빌드 → docx 292KB + PDF 447KB + `_source/` (spec.py 18KB / script.md 13KB / mwb_200.jpg 134KB / mwb_202.jpg 116KB / spec_meta.json) 자동 생성

향후 동일 패턴 차단:

- script-agent 가 mwb 본문 페이지 (200/202 등) 를 "표지" 로 부르는 mislabel — Layer 2 의무 명시 (Read 카탈로그) + Layer 4 anchor 검증으로 catch 가능. 추가로 illustration intro 흐름 의무는 jw-style-checker 보강 필요.

---

## 📌 그 전 세션 (2026-05-02 후반) — CBS 자동화 정본 확정 + BOOTSTRAP·메타룰 정착

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
Read /Users/brandon/Claude/Projects/Congregation/research-meta/_ARCHITECTURE.md
HANDOFF.md 읽고 git status 확인해줘.
```

**⚠ 2026-05-03 critical**: 새 Claude session 진입 시 위 architecture 파일 먼저 Read.
2주 동안 가르친 4-Layer 신뢰 모델 즉시 회복. 이거 안 하면 같은 실수 반복.

## 🔥 다음 세션 우선순위 (2026-05-03 마감 기준)

새 4-Layer 시스템 (Layer 0/1/3 작동, 4 ⚠ manual, 5 ❌) 는 절반 완성. 잔여:

1. **Layer 4 빌더 hook** — 모든 빌더 build 끝부분에 `verify_docx_contains_anchors` 호출 추가 (현재는 manual only)
2. **Layer 5 NWT verbatim** — 성구 본문 캐시 + 빌드 시 verbatim 비교
3. **Agent prompt 의무 명시** — `treasures-talk-script.md` / `spiritual-gems-script.md` / `cbs-script.md` 등에
   "content_inventory.json 의무 input + anchor 우선" 명시
4. **Preflight 추가 슬롯** — 학생 과제, 생활 파트, 회중의 필요, 사회자 (현재 10분/CBS/파수대/영보만)
5. **6/11주 4 슬롯 end-to-end 빌드** — 새 시스템으로 실전 검증 (사용자 검수 부담 0 증명)

이번 세션 한 정정:
- 10분 260604: placeholder → 진짜 mwb 6월호 표지 (200) + 도입 (202) 두 장 + 동영상 cue 추가
- CBS 260521: thumbnail (852) → 본 이미지 (853) 만 + lfb_86_844 도 제거
- (영보 260604 / 파수대 260524 = 이미지 안 쓰거나 진짜 → 정정 불요)

## 🚨 미마무리 결과물 상태 (2026-05-03 정직한 보고)

| docx | 이미지 | 본문 anchor | 본문 풀이 | 결론 |
|---|---|---|---|---|
| **10분 260604** | ✅ 정정 (200·202) | ✅ 동영상 cue 추가 | ⚠ agent 부풀림 그대로 (mwb 4 단락 anchor 와 흐름 안 맞음) | **부분 완성** — 다음 세션 mwb anchor 따라 본문 다시 |
| **CBS 260521** | ✅ 정정 (845·853) | — | — (Layer 4 검증 안 함) | **이미지만 OK** — 본문 검증 미실시 |
| **영보 260604** | ✅ image 없음 | — (Layer 4 안 함) | ⚠ agent 가 mwb anchor 따랐는지 미확인 | **검증 필요** |
| **파수대 260524** | ✅ 진짜 2장 | — | ⚠ 동일 | **검증 필요** |

**6/8-14 (260611) 은 빌드 안 함** — content_inventory.json 까지만 (다음 세션 빌드 대상).

## 🛠 스킬 갱신 (다음 세션 1번 우선순위)

4 SKILL.md (mid-talk10, dig-treasures, cbs, week-study) 에 다음 의무 명시 필요:

1. **빌드 시작 전 preflight 의무**:
   ```
   python3 _automation/preflight.py {slot} {week}
   FAIL → 즉시 중단. agent 호출 X.
   ```
2. **agent 호출 시 content_inventory 의무 input**:
   ```
   research-illustration/{week}/_content_inventory.json 을 첫째로 Read.
   본문 anchor (paragraphs·videos·scriptures·publications) 의무 사용.
   카탈로그 외 자료 인용 금지.
   ```
3. **빌드 후 Layer 4 hook 자동**: 빌더 build 함수 끝부분에 `verify_docx_contains_anchors` 호출 (현재는 manual)

이 3가지 명시되면 다음 주차부터 새 architecture 가 강제됨. 사용자 검수 부담 줄어듬.
