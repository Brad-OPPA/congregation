# 🚚 세션 인수인계 — 2026-04-24

이 파일은 **새 세션이 시작될 때 자동으로 읽어야 합니다**.

## 📌 이동 직후 새 세션의 첫 할 일

### 0. 현재 경로 확인
새 세션 시작 시 반드시 다음 명령으로 위치 확인:
```bash
pwd
```

기대 결과:
```
c:/Users/yoone/Dropbox/ClaudeFile/Congregation/congregation
```

만약 이전 경로(`Dropbox/congregation`)에서 시작됐다면 — **폴더 이동이 아직 안 됐거나 VS Code 가 캐시된 경로로 열림**. `Open Folder` 로 새 경로를 명시적으로 열어야 함.

### 1. 메모리 이주 (새 세션 첫 명령)
원준님이 `"메모리 이주 해줘"` 라고 말씀하시면:

```
구 경로: C:\Users\yoone\.claude\projects\c--Users-yoone-Dropbox-congregation\
신 경로: C:\Users\yoone\.claude\projects\c--Users-yoone-Dropbox-ClaudeFile-Congregation-congregation\
         (또는 유사 — Claude Code 가 새 세션 시작 시 자동 생성함)
```

수행 절차:
1. `ls ~/.claude/projects/` 로 신 폴더 정확한 이름 확인
2. 구 폴더의 `memory/` 안 모든 `.md` 파일을 신 폴더 `memory/` 로 복사 (덮어쓰기 금지, 백업 확인)
3. `MEMORY.md` 인덱스도 복사
4. 구 폴더는 **삭제하지 말고 유지** (백업용 30일)

복사해야 할 메모리 파일 목록 (10+개):
- `MEMORY.md` (인덱스)
- `feedback_address.md` (원준님 호칭)
- `feedback_chair_positive_only.md` (사회자 긍정 피드백)
- `feedback_illustration_source.md` (삽화 소스 wol 전용 + 타 종교 도상 금지 확정판)
- `feedback_publictalk_intro_source.md` (공개강연 서론 내러티브 14축)
- `project_meeting_planner_design.md`
- `project_midweek_pipeline_v2.md`
- `project_s38_meeting_guidelines.md`
- `reference_wol_urls.md`
- `reference_watchtower_folder_structure.md` (2026-04-24 신규)

## 📊 이 세션(2026-04-24)에서 완료한 것

### A. 워치타워 폴더 재편
```
02.WatchTower/01.▣ 수원 연무 회중/
├── 01.주중집회/
│   ├── 00.생봉 사회
│   ├── 01.성경에 담긴 보물/ (10분연설·영적 보물찾기·성경 낭독)
│   ├── 02.그리스도인 생활/ (생활파트·회중적필요)
│   ├── 02.야외봉사에 힘쓰십시오/ (학생과제·5분연설·회중의 필요 250328)
│   └── 03.회중성서연구 (CBS)/
├── 02.주말집회/
│   ├── 01.일요일 사회
│   └── 02.파수대
├── 03.야외 봉사
├── 04.파이오니아 모임
├── 05.지역대회
├── 06.장로 모임
├── 07.서기 자료
├── 08.회중 주소록
├── 09.자리 배치
├── 10.청소 관련
└── _automation/ (🔒 의도적 현 위치 유지 — README.md 참조)
```

### B. Dropbox 최상위 — ClaudeFile 분리 구조
```
Dropbox/
├── ClaudeFile/
│   ├── Congregation/
│   │   └── congregation/ ← 이 repo (이동 예정)
│   ├── Company/
│   │   └── company/ ✅
│   └── Personal/
│       ├── personal/ ✅
│       └── stock-brief/ ✅
└── 02.WatchTower/ (사람용 산출물 + _automation)
```

### C. Claude Code 반영 완료
- **글로벌 스킬 15개** (`~/.claude/skills/*/SKILL.md`) — 주중집회/·주말집회/ 구조로 저장 경로 업데이트
- **congregation/.claude/agents/** — chair-script-builder, living-part-planner 경로+원칙 박스 추가
- **_automation/send_weekly_mail.py** — 슬롯 4개 → 11개 확장 + 새 경로
- **메모리 2건 신규·갱신** (`reference_watchtower_folder_structure.md` 등)

### D. 공개강연 규칙 대폭 강화 (이전 세션 이어서)
- 삽화 wol.jw.org 최우선 + 타 종교 도상 금지 + 총 상한 5장
- 서론 내러티브 "출판물 메시지 + 외부 예시 결합" 공식
- 성서 적중 입증형 9축 + 사유 촉발형 5축 = 총 14축
- 리서치 물량 하한 15~20개
- 적절성 검수 8개 필터

## ⚠️ 이 세션 직전 이슈

### 유실 → 원준님이 복구 완료
초기 Bash mv 명령이 한글 경로 인코딩 문제로 실패하면서 **`주중 집회 계획표`·`S-288 우만 왕국회관`·`전도인리스트_202503.xlsx`** 3건이 일시 사라졌음. 원준님이 직접 이동해 놓으신 상태로 확인됨. 현재 `02.WatchTower/01.▣ 수원 연무 회중/` 아래 존재 여부 재확인 필요할 수 있음.

### 다른 세션에서 5분 연설 중단
원준님이 **다른 Claude Code 세션에서 `/mid-talk5 next1`** 을 돌리던 중 중단시키셨음. `research-plan/student-talk/` 에 부분 산출물 있을 수 있음 (`e62ddbc` 커밋 참조).

## 🎯 남은 작업 (새 세션에서 진행)

### 우선순위 높음
1. **메모리 이주** (위 1번 섹션)
2. **working directory 가 새 경로인지 확인**
3. **congregation repo 원격 동기화 확인**:
   ```bash
   git status
   git log --oneline -5
   git remote -v
   ```

### 그 다음
4. **중단된 /mid-talk5 재개 여부 결정** — 원준님 지시
5. **스킬의 "congregation" 하드코딩 경로 있는지 grep** — 새 경로로 업데이트 필요한 것:
   ```bash
   grep -r "Dropbox/congregation" ~/.claude/skills/
   grep -r "Dropbox\\\\congregation" ~/.claude/skills/
   ```
6. **(E) 옵션** — mid-talk10·week-study·dig-treasures 에 서론/예 품질 강화 규칙 확산 (원준님이 이전에 "마지막에" 로 보류했던 공개강연 실전 검증 전 단계)

## 🔗 이 세션 커밋 링크

GitHub: https://github.com/Brad-OPPA/congregation

최근 커밋:
- `e62ddbc` research/260430: /mid-talk5 next1 테스트 1차 (다른 세션)
- `6520ce2` agents: 워치타워 폴더 주중/주말 재편 반영 + living-part 원칙 박스 추가
- `7e4dd9a` agents: publication-cross-ref·wol-researcher 글로벌→프로젝트 repo 이관
- `67e5ffb` agents/scripture-deep: 공개강연용 H 섹션 추가 — 원어 어원 → 현재 사용 추적
- `d427a7c` agents/slides-builder: 종교적 이미지 자동 삽입 필터 + wol 전용 규칙 추가

## 📞 새 세션 시작 스크립트 (원준님 복사·붙여넣기용)

```
pwd를 확인하고 HANDOFF.md 를 읽어서 현재 상태 파악 후 메모리 이주 해줘
```
