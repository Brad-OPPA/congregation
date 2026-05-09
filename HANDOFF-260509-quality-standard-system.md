# HANDOFF — 회중 자료 품질 표준 시스템 (2026-05-09)

> **다음 세션이 이 파일 하나만 읽으면** 오늘 한 작업·정의된 표준·미해결 점 모두 즉시 파악.
> SessionStart hook 가 회중 cwd 일 때 이 파일 핵심 자동 stderr 출력.

---

## 🎯 사용자 핵심 의도 (절대 잊지 말 것)

1. **"빌드할수록 퀄리티 올라간다"** — 단조 증가
2. **"한 번 한 이야기 영구 자산"** — 매번 다시 알려줄 필요 X
3. **"매번 새로운 클로드와 같은 이야기 또 하는 것"** — 진짜 pain (컨텍스트 reset)
4. **"표준 안에서 작업"** — 일률 X, 슬롯별 적합
5. **"OK 시점 = 그 수준 최소 유지"** — 무리한 상승 X
6. **"본문에 있는 것은 빠지면 안 됨"** — 모든 슬롯 무관용
7. **"너무 방대해지면 또 제대로 못 한다"** — 작게, 정확히

---

## 📚 정의된 사용자 품질 표준 (정본)

`/Users/brandon/Claude/Projects/Congregation/.claude/shared/user-quality-standard.md`

### 핵심 원칙 (v3, 2026-05-09)
- **현재 단계 = 마음에 쏙 들 때까지 퀄리티 올리는 중** (단조 증가)
- **사용자 OK 시점 → 그 수준 ≥ 85% 유지** (무리한 상승 X)
- 표준 §1~§5 모두 충족 노력
- 본문 누락은 무관용 (§2.4, OK 시점 무관)

### §1 형식 표준 (빌더 박힘)
- 줄높이 1.0 (`build_watchtower.py::_add_para`)
- 시간 마커 노랑 배경 + 빨강 글자 (`_render_time_marker`)
- 키워드 볼드 자동 (`**키워드**` → 볼드+노랑)
- 중요 구 노랑 하이라이트 자동 (`[Y]...[/Y]`)
- 삽화 모두 임베드 (image_dir 필수)

### §2 깊이 표준
- §2.1 항 안 모든 성구 깊이 (verbatim + 연구 노트 + 상호 참조 + 항 본문 연결 해설)
- §2.2 출판물 인용 광범위 탐색 → 가장 적합한 1개 + "왜 적합" 멘트
- §2.3 항당 모든 성구 다룸 (1개만 픽업 X)
- §2.4 **본문 누락 금지** (모든 슬롯 공통)
- §2.5 적용 4축 (회중·전도·가정·개인) — 출판물 기반

### §3 자동 검사 메트릭 (threshold 0.85)
빌더 자동 통합 — `quality_monotonic_check.py`:
| 메트릭 | 절대 하한 |
|---|---|
| 글자수 | baseline × 0.85 |
| 「출판물」 인용 | baseline × 0.85 |
| 성구 인용 | baseline × 0.85 |
| 이미지 | baseline × 0.85 |
| 깊이 단락 | baseline × 0.85 |

### §6.1 파수대 (week-study) 특이 의무
- 오프닝 1분 — 4축 짧게 (주제·주제 성구·요점·복습 질문 3가지 미리)
- 결론 1분 — 배운 것 + 적용 (분량 기준, 문장 수 X)
- 복습 섹션 — "어떻게 대답하시겠습니까?" + 본문 질문 + **사회자 해설/답** (파수대 전용)

---

## 🔧 신규 자산 (오늘 만든 것 — 영구)

### Hooks (`.claude/hooks/`)
| 파일 | 역할 |
|---|---|
| `agent-prebrief-hook.py` | Task 호출 직전 정본 + baseline 자동 prepend |
| `agent-postcheck-hook.py` | Task 결과 직후 P1~P13·금칙어·NG 검사 |
| `protect-canonical-dropbox.py` | 정본 폴더 destructive 명령 차단 |
| `skill-standard-loader.py` | Skill 트리거 시 표준 자동 stderr |
| `session-start-git-pull.py` | 세션 시작 시 git pull (확장 예정) |

### 자동화 도구 (`_automation/`)
| 파일 | 역할 |
|---|---|
| `team_briefings.py` | 5팀 brief 단일 모듈 (COMMON + TEAM_SPEC) |
| `quality_metrics.py` | 9축 정량 메트릭 추출 |
| `quality_baseline.py` | 슬롯별 직전 N개 평균 → baseline (0.85) |
| `quality_monotonic_check.py` | 새 docx vs baseline 가중 검사 (PASS/WARN/FAIL) |
| `dedup_against_history.py` | 직전 주차 단락 유사도 (false positive 보강) |
| `run_dedup_for_slot.py` | 8슬롯 dedup wrapper |
| `_dedup_helper.py` | 빌더 자동 통합 (auto_run_dedup + auto_run_quality_monotonic) |
| `add_user_ng.py` | 사용자 NG 자동 등록 |
| `add_user_standard.py` | 사용자 표준 즉시 추가 |
| `orchestrator.py` | 일괄 빌드 진행 추적 + 카톡 보고 |
| `automation_health_check.py` | 8 카테고리 인프라 점검 |
| `check_content_completeness.py` | WOL 본문 vs docx 누락 자동 검사 |

### 빌더 통합 (5 빌더)
- `build_watchtower.py` / `build_cbs_v10.py` / `build_treasures_talk.py` / `build_spiritual_gems.py` / `build_local_needs.py`
- 모두 `_dedup_helper.auto_run_dedup` + `auto_run_quality_monotonic` 자동 통합 (Phase G + H)

### 정본 (영구 자산)
- `.claude/shared/user-quality-standard.md` — 사용자 표준 정본 (v3)
- `.claude/shared/banned-vocabulary.md` — 사용자 NG 어휘 (동적 추가)
- `.claude/commands/{cbs,week-study,mid-talk10,dig-treasures,local-needs}/SKILL.md` — Phase G + prepend 의무 명시

---

## 🚨 진행 중 작업 — 5/25-31 파수대 v2/v3 빌드

### 위치
`~/Dropbox/.../02.주말집회/02.파수대 사회/260525-0531/`

### 현재 상태
- ✅ v1 (자동 빌드 — 형편없음, 이미지 0, 출판물 4)
- ✅ v2_ver2_ (recap commentary 추가 — 이미지 3, 출판물 8~9, monotonic PASS)
- ✅ v3 (4축 적용 + 12블록 출판물 보강 — char=24232, pub=45, scripture=139, img=3)
- ✅ **v3 = OK build 1호** (사용자 "지금까지 한 것 중 제일 마음에 듦" 명시 2026-05-09)
- ✅ v4 dry-run (다음 주차 자동 적용 검증) — 서론 4축 + 결론 stock 제거 + 핵심 성구 5요소 + "표어 성구" NG fix 자동 작동 확인

### v2 메트릭 vs baseline
| | v2 | baseline |
|---|---:|---:|
| 글자수 | 20,389 | 22,274 (92%) |
| 「출판물」 인용 | 9 | 13.3 (68%) |
| 성구 인용 | 124 | 136.7 (91%) |
| 이미지 | 3 | 1.6 (176%) ✅ |
| 깊이 단락 | 102 | 115 (89%) |
| **본문 누락 검사** | **PASS** | — |
| **monotonic 종합** | **PASS** | (가중치 합산) |

### 미해결
- ~~「출판물」 인용 9 < baseline 13.3 (68%) — v3 보강 후 재확인~~ ✅ v3 = 45 (211% baseline)
- ~~사용자 docx 직접 검토 — OK 또는 추가 보강 결정~~ ✅ v3 OK 명시
- ~~OK 시점 도달 시 `mark_ok_build.py` 도구 만들어서 baseline 동결~~ ✅ 도구 생성 + v3 등록 완료

### 다음 주차 자동 적용 (2026-05-09 빌더 코드 패치)
빌더 코드에 박힌 자동화 — stderr 리마인더 의존 X, 다음 주차부터 자동 작동:
- `scrape_wt._build_intro_paragraph` — "알아보십시오 함께 살펴보겠습니다" 이중 종결어 fix
- `scrape_wt._key_scripture_section` — 5요소 dict list 반환 (verbatim + study_note + cross_refs + context_link + publication_quote)
- `scrape_wt.spec_from_article` — `intro_points_preview` + `intro_recap_preview` 새 필드 자동 채움 (소제목 + 복습 질문 verbatim)
- `scrape_wt.spec_from_article` — 결론 stock 제거 + 4축 환기 자동 합성 (소제목 회상 + 4축 적용 권면 + 마무리)
- `build_watchtower._render_opening` — 4축 (③요점 미리 ④복습 질문 미리) 출력
- `build_watchtower._render_key_scripture_items` — 5요소 dict list 들여쓰기 출력 (str fallback 유지)
- `quality_baseline.compute_baseline` — OK builds 우선 사용 (없으면 직전 N 주차 fallback)

---

## 📋 사용자 지적 사항 (오늘 다 수정)

### 형식 (모두 ✅)
1. 줄높이 1.08 → 1.0
2. 시간 마커 빨강 → 노랑+빨강
3. 키워드 볼드 자동
4. 중요 구 하이라이트 자동
5. 삽화 임베드 (image_dir 패치)
6. "표어 성구" → "주제 성구" (라벨 정확 + banned-vocab 등록)

### 깊이 (대부분 ✅, 출판물 인용만 baseline 미달)
7. 핵심 성구 해설 깊이 (cross-ref 5 인용)
8. 참조 자료 딥 (scripture-deep 4 핵심 + 17 추가)
9. 적용 출판물 깊이 (4축 v3 진행)
10. 본문 누락 금지 (PASS)
11. 어떻게 대답하시겠습니까? + 해설 (recap commentary)

### 표준 갱신 (모두 ✅)
12. 오프닝 1분 4축
13. 결론 1분
14. 일률 X 슬롯별 적합
15. OK 시점 baseline 유지

---

## 🚧 다음 세션 진입점 (우선순위)

### 1️⃣ 최우선 — SessionStart hook 강화
다음 세션 시작 시 메인 Claude 자동 인식:
```python
# .claude/hooks/session-start-git-pull.py 확장
# 또는 신규 .claude/hooks/session-start-load-standards.py
- user-quality-standard.md 핵심 stderr 출력
- banned-vocabulary.md 사용자 NG 섹션 stderr
- 이 HANDOFF 파일 핵심 stderr (진행 중·미해결)
```
**효과**: "매번 새 Claude 와 같은 이야기" pain 해결.

### 2️⃣ v3 빌드 결과 검토
- `~/Dropbox/.../260525-0531/파수대 사회_260531_ver2_.docx`
- 사용자 docx 직접 검토
- OK → `mark_ok_build.py` 도구 만들어서 baseline 동결
- 더 보강 → application 자료의 추가 출판물 인용 통합

### 3️⃣ mark_ok_build.py 도구 (OK 시점 도달 시)
```bash
python3 _automation/mark_ok_build.py <docx> --reason "..."
```
- docx 메트릭 추출 → `.claude/shared/ok-builds.json` 등록
- quality_baseline 가 OK builds 우선 사용 (있으면)
- §5.1 좋은 사례에 발췌 자동 추가

### 4️⃣ 다른 슬롯 동일 흐름 적용
- CBS / 10분 연설 / 영적 보물 / 회중의 필요
- 각 SKILL 도 동일하게 monotonic 자동 검사 통과 + 사용자 OK 도달

---

## 🔄 환경 정보 (다음 세션 첫 응답 전 확인)

- **환경**: macOS Claude Desktop App (`CLAUDE_CODE_ENTRYPOINT=claude-desktop`)
- **CLI 도 설치됨**: `/opt/homebrew/bin/claude`
- **회중 .claude/agents/ 등록**: ❌ Cowork/Desktop 모두 자동 인식 X
  - subagent_type 으로 cbs-planner, watchtower-study-planner 등 호출 시 "Agent type not found"
  - **대안**: general-purpose 에이전트 + team_briefings.py prepend 사용
- **Skill 도구**: 작동 (`/weekly`, `/week-study` 등 호출 가능)
- **회중 .claude/commands/*/SKILL.md**: 인식됨

---

## 변경 이력

- **2026-05-09 v1** — 회중 자료 품질 표준 시스템 구축 완료. 사용자 표준 정본 + 자동 검사 도구 + 빌더 통합 + Skill PreTool hook + 5팀 적용. 5/25-31 파수대 v2/v3 빌드 진행 중. 다음 세션 = SessionStart hook 강화 + 사용자 docx 검토 + OK baseline 동결.
