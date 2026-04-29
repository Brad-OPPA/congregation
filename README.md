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

### 2026-04-29 — Mac 환경 적응 + 발송 인프라 안정화 + 에이전트 정책 일관화

- 회중 워크스페이스 `.claude/settings.json` hook command 환경변수화 (Windows 절대경로 → `$CLAUDE_PROJECT_DIR`)
- next2 (5/14·5/17) 4 슬롯 풀세트 빌드 (10분 연설·영적 보물·CBS·파수대 사회) — 6단 방어 통과, 4 docx + 4 PDF (맑은 고딕 임베드)
- 5명 [정정] 메일 발송 5/5 성공 (12 첨부 정확)
- **/weekly 1단계 정책 갱신**: 카톡만 → **본인에게만 메일+카톡** (회중 4명은 본인 검수 후 2단계 발송). 첨부 슬러그·HTML 본문·인사말 직접 검수 가능
- 세부 인프라 변경 (LibreOffice + 빌더 + send_weekly_mail collect/슬러그 NFC/VER_RE/yymmdd 중복 등): `02.WatchTower/01.▣ 수원 연무 회중/_automation/README_WEEKLY.md` 의 "변경 이력" 참조
- **에이전트 30종 전체 점검** — frontmatter·shared 정책 reference 검증. 9개 에이전트 (cbs-planner·cbs-script·chair-script-builder·living-part-planner·living-part-script·local-needs-planner·public-talk-script·scripture-deep·timing-auditor) 에 `multi-layer-defense.md` reference 한 줄 일괄 추가. CLAUDE.md 카운트 29→30 갱신 (public-talk-script 추가 명시).
- Hook 스크립트 (factcheck-numbers.py, skill-source-reminder.py) syntax + manual 실행 검증 PASS.
