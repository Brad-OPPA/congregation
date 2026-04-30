# 🚚 세션 인수인계 — 2026-04-29 정본

이 파일은 **새 세션이 시작될 때 자동으로 읽어야 합니다**.
직전 세션 노트는 `HANDOFF_260425_overnight.md` (보존, 참고용).

## ⚡ 새 세션 첫 할 일

```bash
pwd  # 기대: /Users/brandon/Library/CloudStorage/Dropbox/ClaudeFile/Congregation
     # 또는 02.WatchTower/01.▣ 수원 연무 회중 (작업 워크스페이스)
git status -s
git log --oneline -5
```

## 🧭 환경 — Mac/Windows 양립 (2026-04-29 안정화)

| 항목 | Mac (현재) | Windows |
|---|---|---|
| 메타 워크스페이스 | `~/Library/CloudStorage/Dropbox/ClaudeFile/Congregation/` | `C:\Users\yoone\Dropbox\ClaudeFile\Congregation\` |
| 작업 워크스페이스 | `~/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/` | `C:\Users\yoone\Dropbox\02.WatchTower\01.▣ 수원 연무 회중\` |
| Hook command | `python3 -X utf8 "$CLAUDE_PROJECT_DIR/.claude/hooks/*.py"` (양립) | 동일 |
| PDF 변환 | LibreOffice (`/Applications/LibreOffice.app`) 우선 + docx2pdf fallback | docx2pdf 우선 |
| 폰트 | 맑은 고딕 (`~/Library/Fonts/malgun.ttf`) + Noto Sans KR 백업 | OS 기본 맑은 고딕 |

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

## 🚨 다음주 (~2026-05-07) 우선 처리 — 구 노트북 Claude 삭제 후 일괄 정리

**컨텍스트**: 2026-04-30 Mac 으로 META + 자동화 옮김. 새 정본은 `~/Claude/Projects/Congregation/` (이 파일 위치). 구 노트북 (Windows yoone) 에 Claude Code 아직 설치 + 옛 경로 참조 중. 사용자가 "구 노트북 Claude 삭제했어" 신호 주면 아래 5단계 일괄 진행:

1. **구 노트북 잔여 확인** (사용자 직접) — Windows PowerShell:
   ```
   cd "C:\Users\yoone\Dropbox\ClaudeFile\Congregation" && git status -s && git log --oneline -3
   cd "C:\Users\yoone\Dropbox\02.WatchTower\01.▣ 수원 연무 회중\_automation" && git status -s && git log --oneline -3
   ```
   비어있으면 OK. 떠 있으면 push (`git add . && git commit -m "구 노트북 잔여" && git push`).

2. **Mac 에서 GitHub 최신 동기화**:
   ```bash
   cd ~/Claude/Projects/Congregation && git pull
   cd ~/Claude/Projects/Congregation/_automation && git pull
   ```

3. **Dropbox 옛 META 삭제** (비가역 — 사전 확인) — `rm -rf ~/Dropbox/ClaudeFile/Congregation/`

4. **WS `_automation/` 삭제** (비가역 — 사전 확인) — `rm -rf "~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/_automation/"`. 출력 폴더 (01.주중집회 등) 는 그대로 둠.

5. **문서 갱신**:
   - 이 HANDOFF.md — 환경 표를 Mac 단독으로
   - `CLAUDE.md` — 옛 Windows 경로 표기 (`C:\Users\yoone\.claude\skills\` 등) → Mac 경로
   - `_automation/CLAUDE.md` — 자동 commit 정책 안의 Windows 경로 정리

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

### 즉시 가능

- `/midweek-now` 등 다른 스킬 — 새 주차 자료 생성
- `/local-needs` — 장로의회 주제 받으면 즉시
- `/publictalk` — 공개 강연 골자 받으면 즉시

## 📞 새 세션 시작 스크립트

```
HANDOFF.md 읽고 git status 확인해줘.
```
