# 🚚 세션 인수인계 — 2026-04-25 갱신

이 파일은 **새 세션이 시작될 때 자동으로 읽어야 합니다**.

## ⚡ 새 세션 첫 할 일 (3단계)

```bash
# 1. 위치 확인
pwd   # 기대: c:/Users/yoone/Dropbox/ClaudeFile/Congregation

# 2. git 상태 확인
git status
git log --oneline -5
git remote -v

# 3. 메모리 상태 확인
ls ~/.claude/projects/c--Users-yoone-Dropbox-ClaudeFile-Congregation/memory/
```

기대 결과:
- 작업 위치 정상 (`Dropbox/ClaudeFile/Congregation`)
- origin/main 동기화 완료, 최신 커밋 `5b44b93` 또는 그 이후
- 메모리 파일 12개 (MEMORY.md + feedback_*·project_*·reference_* 11개)

## 🧭 영구 운영 원칙 (반드시 준수)

| 원칙 | 메모리 파일 | 핵심 |
|---|---|---|
| 호칭 | `feedback_address.md` | "원준" / "원준님" — "형제님" 금지 |
| **작업 위임·병렬화 우선** | `feedback_delegate_to_subagents.md` | 3단계/3파일 이상은 서브 위임, 의존성 없으면 병렬 |
| **상투 청중 호명 금지** | `feedback_script_no_cliche.md` | "여러분도 …해 보신 적" 류 9개 금지 |
| 사회자 조언 긍정 | `feedback_chair_positive_only.md` | ④ 주의점 후보 0건 |
| 공개강연 삽화 | `feedback_illustration_source.md` | wol 1순위, 종교 도상 금지 |
| 공개강연 서론 | `feedback_publictalk_intro_source.md` | 외부 1차 자료 + 출판물 메시지 |
| 안 된다 결론 전 우회 | `feedback_no_giveup.md` | 시간 부족·불가 핑계 거의 무효 |

## 📊 이번 세션(2026-04-25) 누적 변경

### 완료된 작업
1. **메모리 이주 확인** — 구·신 폴더 동일성 검증 (이미 이주 완료 상태)
2. **publictalk 스킬 경로 정정** — `Dropbox/congregation` → `Dropbox/ClaudeFile/Congregation`
3. **README.md 신규** (`82e396d`)
4. **6단 방어(v2) + 서론·예화·삽화 품질 표준 도입** (`bc94561`)
   - `.claude/shared/intro-and-illustration-quality.md` 신규 (🟢 착수 / 🔴 종료 블록 + 14축 + 차등 적용표)
   - `.claude/shared/multi-layer-defense.md` 4단 → 6단 확장 (⑤ Planner 2차 재검수 신규)
   - 에이전트 7개 + 스킬 3개(mid-talk10·dig-treasures·week-study) 업데이트
5. **`/mid-talk5 now` (260430) 완주** (`ecd243c`)
   - 주제: "종교 단체에 꼭 속해 있어야 합니까?" (히 10:24, 25 / 약 1:27)
   - 4단 방어 전 과정 PASS (재빌드 4회로 수렴)
   - script.md 1,166음절 / 실전 277초
6. **"형제 여러분, " 호칭 제거** (`9afafca`)
7. **상투 청중 호명·수사 질문 회피 정책** (`5b44b93`)
   - 메모리 신규 + 공유 파일 §A-4-bis + jw-style-checker 점검 축 G + script 5개 박스
8. **5분 연설 docx + PDF 빌더 작성**
   - `_automation/build_mid_talk5.py` 신규 (절 번호 위첨자 처리 포함)
   - `_automation/content_talk5_260430.py` 신규
   - `02.WatchTower/.../5분연설/Talk5_종교단체에속해야합니까_260430.docx` (40KB) + `.pdf` (166KB)
9. **CLAUDE.md 원칙 추가** — 위임·병렬화 + 청중 호명 금지

### git 상태
- origin/main 최신: `5b44b93` (또는 이후 커밋 추가됨)
- 5개 커밋 push 완료: README → 6단방어 → /mid-talk5 → 형제여러분 → 상투호명

## 🎯 남은 작업·다음 세션 진입점

### 즉시 가능
- **다음 주차 (`/mid-talk5 next1` = 2026-05-07)** 자동 생성 — 전체 4단 방어 사이클 가능
- **`/midweek-now`** 등 다른 스킬 — 이번 시점 기준 next1·next2 등으로
- **`/local-needs`** — 장로의회 주제 받으면 즉시 시작 가능

### 다른 세션이 만든 untracked 파일들 정리 필요
다른 Claude Code 세션이 새벽에 작업한 산출물들이 unstaged 상태로 남아 있음. 다음 세션 시작 시 `git status` 확인하고 필요시 처리:
- `HANDOFF_260425_overnight.md` (새벽 세션 인수인계)
- `research-application/260430/cbs_*.md`, `gems_*.md`
- `research-bible/260430/cbs_*.md`, `gems_*.md`
- `research-topic/260430/cbs_*.md`, `gems_*.md`
- `research-experience/260430/gems_*.md`
- `research-illustration/260430/gems_*.md`
- `research-plan/cbs/`, `research-plan/living-part/`, `research-plan/spiritual-gems/`, `research-plan/student-assignment/`, `research-plan/treasures-talk/`
- `research-qa/260430/`

→ 이 산출물들이 진짜 필요한 작업의 결과면 commit, 폐기물이면 정리.

### docx/PDF 빌더 미작성 상태
- `build_cbs.py`, `build_spiritual_gems.py`, `build_watchtower.py`, `build_treasures_talk.py`, `build_publictalk.py` ✅ 존재
- `build_mid_talk5.py` ✅ 이번 세션에서 신규 작성
- `build_living_part.py` 등 다른 5분/생활 파트 빌더는 미존재 — 필요 시 build_mid_talk5.py 패턴 응용

## 📞 새 세션 시작 스크립트 (원준님 복사·붙여넣기용)

```
HANDOFF.md 읽고 git status 확인해줘. 그리고 untracked 파일들이 다른 세션의 결과물인지 폐기물인지 판단해서 정리하자.
```

또는 바로 다음 작업 지시:

```
/mid-talk5 next1 진행해줘
```
