# 🚀 BOOTSTRAP — 새 컴퓨터 복구 절차 (확정 정본 2026-05-02)

> **목적**: 어떤 Mac/Linux 에서 GitHub 백업만으로 회중 자료 자동 생성 환경을 **0 → 100%** 복구.
> **전제**: 사용자 = 김원준 (eltc9584@gmail.com). Dropbox 계정 동일.
> **레포 2개**: `congregation` (META, main) / `congregation-automation` (\_automation, master).

---

## 0. 핵심 원칙

1. **GitHub 가 진실의 원천** — 두 레포 푸시되어 있으면 어떤 기기에서도 복구 가능.
2. **Dropbox 는 docx/PDF 출력 동기화** — 빌더 출력을 모든 기기가 공유.
3. **비밀 파일 (`weekly_secrets.py`, `kakao_tokens.json`) 은 GitHub 에 없음** — 새 기기에서 수동 재구성 필수.
4. **하드코딩 경로 금지** — 모든 빌더는 `Path.home()` 패턴 사용 (Mac·Linux 양립).

---

## 1. 필수 환경

| 항목 | 버전 | 설치 |
|---|---|---|
| OS | macOS 14+ / Linux | — |
| Python | 3.10 ~ 3.14 | Homebrew `brew install python@3.14` 또는 시스템 |
| LibreOffice | 24+ (PDF 변환용) | `brew install --cask libreoffice` |
| 폰트 — 맑은 고딕 | malgun.ttf | `~/Library/Fonts/` 수동 복사 (Windows 폰트 추출) |
| 폰트 — Noto Sans KR | latest | `brew install --cask font-noto-sans-cjk-kr` |
| gh CLI | 2.40+ | `brew install gh` |
| git | 2.40+ | macOS 기본 |
| Claude Code | 최신 | https://claude.com/claude-code |

Python 패키지 (모두 pip):

```
python-docx==1.2.0
python-pptx==1.0.2
lxml==6.1.0
Pillow==12.2.0
requests==2.33.1
docx2pdf==0.1.8         # Mac 보조 (LibreOffice 우선)
beautifulsoup4==4.12.3  # WOL HTML 파싱
PyYAML==6.0.2           # meta.yaml 처리
```

---

## 2. 1회 셋업 (새 기기)

### Step 1 — 디렉토리 골격

```bash
mkdir -p ~/Claude/Projects
cd ~/Claude/Projects
```

### Step 2 — gh 인증 + repo clone

```bash
gh auth login   # GitHub.com / HTTPS / 웹 브라우저 / 토큰 저장
gh repo clone Brad-OPPA/congregation Congregation
cd Congregation
gh repo clone Brad-OPPA/congregation-automation _automation
```

> **권한**: 두 레포 모두 Private. `gh auth login` 시 `repo` 스코프 필수.

### Step 3 — Python 의존성

```bash
cd ~/Claude/Projects/Congregation/_automation
pip3 install python-docx python-pptx lxml Pillow requests beautifulsoup4 PyYAML docx2pdf
```

특정 버전 고정 시:

```bash
pip3 install "python-docx==1.2.0" "python-pptx==1.0.2" "lxml==6.1.0" "Pillow==12.2.0" "requests==2.33.1" "beautifulsoup4==4.12.3" "PyYAML==6.0.2"
```

### Step 4 — LibreOffice + 폰트

```bash
brew install --cask libreoffice
# soffice CLI 가 PATH 에 있어야 PDF 자동 변환 됨
which soffice  # → /opt/homebrew/bin/soffice 또는 /usr/local/bin/soffice
```

맑은 고딕 폰트 확보 (Windows 기기에서 `C:\Windows\Fonts\malgun.ttf` 복사):

```bash
cp malgun.ttf ~/Library/Fonts/
```

Noto Sans KR (백업 폰트):

```bash
brew tap homebrew/cask-fonts
brew install --cask font-noto-sans-cjk-kr
```

### Step 5 — Dropbox 동기화

Dropbox 데스크톱 앱 설치·로그인 후 `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/` 자동 동기화 확인. 빌더는 이 경로에 docx/PDF 출력.

```bash
ls "~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/"
# 01.성경에 담긴 보물  02.야외 봉사에 힘쓰십시오  03.그리스도인 생활  04.회중의 필요  05.회중 성서 연구
```

폴더가 안 보이면 Dropbox 동기화 완료 대기.

### Step 6 — Claude Code 슬래시 명령 심볼릭 링크

```bash
mkdir -p ~/.claude
[ -L ~/.claude/commands ] && rm ~/.claude/commands
ln -s ~/Claude/Projects/Congregation/.claude/commands ~/.claude/commands
ls ~/.claude/commands  # 21개 슬래시 명령 (cbs, mid-talk10, dig-treasures, ...)
```

이 심링크가 없으면 회중 폴더 안에서도 `/cbs` 등 슬래시 명령 미작동.

### Step 7 — `weekly_secrets.py` 생성

> ⚠ 이 파일은 **GitHub 에 없음**. 새 기기에서 직접 생성 필요.
> 이전 기기에서 백업해 둔 파일이 있으면 단순 복사. 없으면 아래처럼 새로 작성.

```bash
cd ~/Claude/Projects/Congregation/_automation
cp weekly_secrets.example.py weekly_secrets.py  # template (커밋됨)
# 그 후 weekly_secrets.py 안의 GMAIL_APP_PASSWORD·KAKAO_* 값 채워넣기
```

채워야 할 값:
- `GMAIL_ADDRESS` = "eltc9584@gmail.com"
- `GMAIL_APP_PASSWORD` = Google 계정 → 보안 → 2단계 인증 → 앱 비밀번호 → 16자리 발급
- `RECIPIENTS` = 5명 리스트 (이름·이메일·존칭)
- `KAKAO_REST_API_KEY`·`KAKAO_REDIRECT_URI`·`KAKAO_CLIENT_SECRET` = https://developers.kakao.com/console/app 의 본인 앱 (메모앱 메시지 권한)

### Step 8 — Kakao OAuth 토큰 재발급

`kakao_tokens.json` 도 GitHub 에 없음. 새 기기에서 OAuth 재인증:

```bash
cd ~/Claude/Projects/Congregation/_automation
python3 kakao_auth.py
# 브라우저 열림 → Kakao 로그인 → 권한 동의 → localhost:5000/oauth 리다이렉트
# kakao_tokens.json 자동 저장됨
```

### Step 9 — 동작 검증

```bash
cd ~/Claude/Projects/Congregation/_automation
# (a) 빌더 정상 import
python3 -c "from build_cbs_v10 import build_cbs_v10; print('OK')"
# (b) docx2pdf / soffice 양립
python3 -c "from build_treasures_talk import auto_convert_to_pdf; print('OK')"
# (c) Gmail SMTP (실제 발송 X, 인증만)
python3 -c "import smtplib, weekly_secrets as s; smtplib.SMTP_SSL('smtp.gmail.com',465).login(s.GMAIL_ADDRESS, s.GMAIL_APP_PASSWORD); print('Gmail OK')"
# (d) Kakao 토큰
python3 -c "import json; t=json.load(open('kakao_tokens.json')); print('Kakao OK, expires:', t.get('expires_at'))"
```

전부 OK 면 새 기기 셋업 완료.

---

## 3. Claude Code 안에서 테스트 빌드

```
cd ~/Claude/Projects/Congregation
claude
```

대화 시작 후:

```
/cbs next1
```

(또는 이미 빌드한 주차) — 6단 방어(v2) 흐름이 0 에러로 완주하면 복구 성공.

---

## 4. 백업·복구 안전장치 점검

다음 4 가지가 모두 GitHub 또는 Dropbox 에 있어야 어떤 기기에서도 복구 가능:

| 자산 | 위치 | 복구 가능 여부 |
|---|---|---|
| 빌더 코드 (`_automation/`) | GitHub `congregation-automation` | ✅ |
| 에이전트·스킬 정의 (`.claude/`) | GitHub `congregation` | ✅ |
| 리서치 산출물 (`research-*/`) | GitHub `congregation` | ✅ |
| 회중 docx/PDF 출력 | Dropbox `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/` | ✅ |
| 폰트 malgun.ttf | 사용자 보관 (Windows 추출) | ⚠ 수동 |
| `weekly_secrets.py` | 본인 비밀번호 매니저 | ⚠ 수동 (template 은 GitHub) |
| `kakao_tokens.json` | OAuth 재발급 | ⚠ 자동 재발급 (Step 8) |

**자주 푸시 의무**: META 와 \_automation 두 레포 모두 작업 직후 `git push` (CLAUDE.md `_automation/` 자동 commit·push 정책 참조).

---

## 5. 자주 발생하는 문제·해결

| 증상 | 원인 | 해결 |
|---|---|---|
| `/cbs` 등 슬래시 명령 안 보임 | `~/.claude/commands` 심링크 누락 | Step 6 재실행 |
| docx 빌드 OK 인데 PDF 미생성 | LibreOffice·docx2pdf 둘 다 미설치 | Step 4 재실행 |
| 한국어 깨짐 (PDF) | 맑은 고딕 폰트 없음 | malgun.ttf 를 `~/Library/Fonts/` 복사 |
| Gmail 발송 인증 실패 | 앱 비밀번호 만료 또는 2단계 OFF | 새 16자리 재발급 |
| Kakao 메시지 발송 401 | refresh_token 만료 (60일) | `python3 kakao_auth.py` 재인증 |
| WOL fetch timeout | macOS Python 3.14 urllib 이슈 | `requests` 직접 사용 (각 빌더 shim 내장) |
| `Path.home() / ".../01.▣..."` 깨진 경로 | 한글 NFD 정규화 (macOS HFS+) | `unicodedata.normalize('NFC', path)` 적용 |
| git push 권한 거부 | gh 토큰 만료 | `gh auth refresh -h github.com -s repo` |

---

## 6. 일관성 체크리스트 (구조 변경 시)

작업 후 다음이 일관되게 갱신됐는지 확인:

- [ ] `CLAUDE.md` — 폴더·스킬·에이전트 표
- [ ] `HANDOFF.md` — 직전 세션 요약
- [ ] `BOOTSTRAP.md` (이 파일) — 의존성·경로 변경 반영
- [ ] `research-meta/{스킬명}-자동화-구조.md` — 호출 체인·검증 룰
- [ ] `_automation/CLAUDE.md` — 빌더 정책
- [ ] `.claude/agents/{에이전트}.md` — 에이전트 명세
- [ ] git push 양 레포 — 즉시 백업

`STRUCTURE.md` (상위 워크스페이스) 도 폴더 추가/이동 시 갱신.

---

## 7. 상위 백업 (선택, 더블 보험)

GitHub 외에 추가 백업이 필요하면:

```bash
# Time Machine 또는 외장 SSD
rsync -av --exclude '__pycache__' --exclude 'apps' \
    ~/Claude/Projects/Congregation/ \
    /Volumes/BackupSSD/Congregation_$(date +%Y%m%d)/
```

비밀 파일 별도 보관:

```bash
# weekly_secrets.py 와 kakao_tokens.json 만 암호화 보관
mkdir -p ~/Dropbox/_secrets
cp _automation/weekly_secrets.py _automation/kakao_tokens.json ~/Dropbox/_secrets/
# 또는 1Password / Bitwarden 등 비밀번호 매니저
```

---

## 개정 이력

- 2026-05-02 — 초판. 새 기기 복구 0→100% 절차 확정. CBS 260514 빌드 후 정착.
