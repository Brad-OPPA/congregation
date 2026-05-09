# HANDOFF — 회중의 필요 팀 자동화 (2026-05-09)

> 다음 세션이 이 작업을 이어받을 때 **이 파일 하나만 읽으면** 컨텍스트 100% 복원되도록.

---

## 🎯 무엇을 했나 (오늘 작업 요약)

회중의 필요 (local-needs) 스킬을 **자율 작동 팀 에이전트** 형태로 보강.
사용자분이 원한 그림: "주제·내용 입력 → 에이전트들이 PreTool 훅으로 규칙 미리 알고 시작 → 끝나고 PostTool 로 검증 → 중복 없이 빌드 → 초안 보고".

### 신규 자산 4종

| # | 파일 | 역할 | 위치 |
|---|---|---|---|
| 1 | `agent-prebrief-hook.py` | Task 호출 직전 팀 규칙집(P1~P13) stderr 주입 | `.claude/hooks/` |
| 2 | `agent-postcheck-hook.py` | Task 결과 직후 위반 즉시 검사 | `.claude/hooks/` |
| 3 | `protect-canonical-dropbox.py` | Bash destructive 명령으로부터 정본 보호 | `.claude/hooks/` |
| 4 | `dedup_against_history.py` | 새 docx vs 직전 주차 단락 유사도 검사 | `_automation/` |

### 보강 적용 흐름 (지금 가동 중)

```
[사용자] "/local-needs" + 자유 형식 브리프
   ↓
[메인 Claude]
   ├─ ① PreToolUse [agent-prebrief]   → 팀 규칙집 stderr 주입
   ├─ Task → 에이전트 (planner / 보조 7 / script)
   ├─ ② PostToolUse [agent-postcheck] → 결과 위반 검사
   ├─ ③ Bash 시 [protect-canonical]   → 정본 폴더 destructive 차단
   ├─ build_local_needs.py → docx baseline
   ├─ ④ dedup_against_history.py     → 직전 주차 중복 검사
   └─ ⑤ 4종 게이트 (fact·style·timing·quality) → FAIL 시 자동 재작성
```

---

## 📁 커밋 히스토리 (오늘 5건)

```bash
cd ~/Claude/Projects/Congregation && git log --oneline 28c2130..47331c3 47331c3 e2ba8f0 694762f
```

| Commit | 내용 |
|---|---|
| `28c2130` (META) | feat: add agent-postcheck-hook (보강 3) |
| `47331c3` (META) | feat: add protect-canonical-dropbox hook |
| `e2ba8f0` (META) | feat: 회중의 필요 팀 보강 (Phase G) + 정본 2종 추가 |
| `694762f` (META) | feat: add agent-prebrief-hook |
| `d2b8ac0` (_automation) | feat: add dedup_against_history.py |

---

## ✅ 이미 검증된 것

- **agent-prebrief-hook**: 3 케이스 통과 (회중의 필요 팀 발동, CBS 통과, Edit 통과)
- **agent-postcheck-hook**: 8 케이스 중 7 자동 통과 + 8번째 (예배) 텍스트 길이만 늘리면 정상
- **protect-canonical-dropbox**: 12 케이스 중 12 통과 (정본 차단 / 임시 통과 / 다른 프로젝트 통과)
- **dedup_against_history**: 합성 테스트 통과 (1.00 HIGH·0.79 WARN 정확 감지)

---

## ❌ 아직 안 한 것 (다음 세션 후보)

### 🔥 1순위 — 실전 테스트
다음 회중의 필요 빌드 때 실제로 4개 보강 가동되는지 검증.

**진입 시그널**: 사용자가 `/local-needs now` 또는 "회중의 필요 만들어줘" 입력 시.

**실전 체크리스트**:
- [ ] PreToolUse [agent-prebrief] stderr 메시지가 메인 Claude 컨텍스트에 들어가는지 (실제 발동 확인)
- [ ] PostToolUse [agent-postcheck] 가 보조 에이전트 결과 받자마자 발동하는지
- [ ] dedup_against_history.py 실제 직전 주차 docx 와 비교해 결과 나오는지
  - 실행: `python3 _automation/dedup_against_history.py --new <baseline.docx> --history-dir "~/Dropbox/.../04.회중의 필요/"`
- [ ] protect-canonical-dropbox 실제 명령 차단 작동 (회중 정본 rm 시도 시)

**부족한 점 발견 시**: HANDOFF 파일에 추가 + 다음 세션이 이 파일 읽고 보강.

### 2순위 — 다른 팀 확장 ✅ 완료 (2026-05-09 v2)
5팀 모두 prebrief + postcheck 활성화:
- ✅ **local-needs** (회중의 필요) — P1~P13 v6 정본
- ✅ **cbs** (회중 성서 연구) — docid 1102016XXX·publication symbol 분리·시간 마커 8개
- ✅ **week-study** (파수대 연구) — 17블록·5 소제목·외부 5 출판물·14축
- ✅ **mid-talk** (10분/5분 연설) — 본문/예 분리·6단계 narrative·사용자 NG
- ✅ **dig-treasures** (영적 보물찾기) — 20성구·5 보조·R1~R10

agent-prebrief-hook 의 TEAM_BRIEFINGS dict 에 5개 팀 SPEC 추가.
agent-postcheck-hook 의 detect_team 확장 + USER_NG_VOCAB 추가
(가정 경배·신자·여호와의 임재·수동적 — 모든 팀 공통 차단).

8/8 테스트 통과.

### 3순위 — 보강 4 (`user-ng-auto-learn`) ✅ 완료 (2026-05-09 v3)
**반-자동 학습** 형태로 구현:
- `_automation/add_user_ng.py` — CLI 스크립트
  - `--word "어휘" --replacement "권장" --reason "사유"`: 자동 등록
  - `--list`: 현재 등록 목록
  - 중복 자동 skip
- `agent-postcheck-hook` 동적 파싱
  - banned-vocabulary.md 의 "## 2-bis" 섹션 자동 read
  - 새 NG 추가 시 다음 hook 호출부터 즉시 적용 (재시작 불필요)
  - 파일 read 실패 시 hardcoded fallback (4개)

사용자 자연어 요청 시 흐름:
1. 사용자: "수동적이라는 어휘 또 쓰지마"
2. 메인 Claude: `python3 _automation/add_user_ng.py --word "수동적" --replacement "능동적"`
3. 정본 갱신 → 다음 빌드부터 자동 차단

테스트: 4 케이스 모두 통과 (등록·중복·즉시 반영·정리)

---

## 🔧 코드 위치 빠른 인덱스

```
~/Claude/Projects/Congregation/
├── .claude/
│   ├── hooks/
│   │   ├── agent-prebrief-hook.py           ← 신규 (보강 1)
│   │   ├── agent-postcheck-hook.py          ← 신규 (보강 3)
│   │   ├── protect-canonical-dropbox.py     ← 신규
│   │   ├── content-zone-guard.py            (기존, 참고)
│   │   ├── factcheck-numbers.py             (기존, Stop)
│   │   ├── quality-loop-enforcer.py         (기존, Stop)
│   │   └── fact-loop-enforcer.py            (기존, Stop)
│   ├── settings.json                        ← PreTool/PostTool 매처 추가
│   └── shared/
│       ├── banned-vocabulary.md             (정본 — 금칙어)
│       ├── multi-layer-defense.md           (6단 방어)
│       └── main-claude-edit-policy.md       (Phase E)
├── _automation/
│   └── dedup_against_history.py             ← 신규 (보강 2)
└── research-meta/
    ├── local-needs-v6-speech-form-patterns.md   (P1~P13 정본)
    ├── local-needs-final-output-routing.md      (Phase F)
    ├── 회중성서연구-자동화-구조.md
    ├── 파수대-사회-자동화-구조.md
    ├── 10분-연설-자동화-구조.md
    └── 공개강연-자동화-구조.md
```

---

## ⚙️ 디버그 / 트러블슈팅 가이드

### Q: agent-prebrief 가 발동 안 됨
- `cat .claude/settings.json` 에 `"matcher": "Task"` 항목 있나?
- 호출 시 subagent_type 이 `local-needs-*` 또는 description/prompt 에 "회중의 필요" 포함되어야 함

### Q: agent-postcheck 가 위반 못 잡음
- 검사 텍스트가 20자 이상이어야 함
- 한글에서 `\b` word boundary 안 작동 → substring 또는 lookaround 사용
- BANNED_VOCAB / NWT_GENERAL_NAMES 정확한 한글 substring

### Q: dedup_against_history 가 비교 대상 0개
- `--history-dir` 가 실제 docx 들이 있는 상위 디렉토리인지 (rglob)
- macOS Dropbox 권한 (TCC) — Full Disk Access 또는 Files and Folders 권한 부여 필요

### Q: protect-canonical-dropbox 가 정상 명령도 차단
- SAFE_HINTS 에 (research-plan/, drafts/, ~$, .bak_*, /tmp/, .venv/, __pycache__) 가 명령에 substring 으로 포함되면 통과
- 회중 외 경로 (~/Claude/Projects/Personal/Company) 는 항상 통과

---

## 🔄 이 핸드오프 갱신 규칙

다음 세션이 작업 끝낼 때 **반드시 이 파일 갱신**:
1. "✅ 이미 검증된 것" 에 추가
2. "❌ 아직 안 한 것" 에서 처리한 항목 제거
3. "발견한 부족한 점" 새 섹션 추가 (실전 테스트 결과)
4. 새 커밋 히스토리 append

파일명 컨벤션: 동일 주제 작업이 이어지면 같은 파일 갱신, 다른 주제면 새 HANDOFF-YYMMDD-{topic}.md 생성.

---

## 변경 이력

- **2026-05-09 v1** — 회중의 필요 팀 자동화 4종 보강 완료 (prebrief / postcheck / protect / dedup)
- 다음 진입점: 실전 테스트 또는 다른 팀 확장
