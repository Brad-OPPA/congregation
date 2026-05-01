# 메인 Claude 직접 Edit 제약 정책

> **메인 Claude 는 회중 자료의 콘텐츠 영역을 직접 Edit/Write 하지 않는다.**
> 모든 콘텐츠 정정은 검증 게이트를 거친 에이전트(jw-style-checker·script 등) 를 통해서만.
> 작성: 2026-05-01 / 트리거: 본 세션 "사역→봉사" 직관 정정 사고

## 1. 금지 영역 (메인 Claude Edit/Write 차단)

| 경로 | 사유 |
|---|---|
| `/Users/brandon/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/**/*.docx` | 검증 게이트 우회 위험 — 디스크 직접 편집 금지 |
| `/Users/brandon/Claude/Projects/Congregation/_automation/content_*.py` | 데이터 파일 — Agent (script + 일반 변환) 만 작성·수정 가능 |
| `/Users/brandon/Claude/Projects/Congregation/research-plan/**/script.md` | script 에이전트만 작성 |
| `/Users/brandon/Claude/Projects/Congregation/research-plan/**/outline.md` · `meta.yaml` | planner 에이전트만 작성 |
| `/Users/brandon/Claude/Projects/Congregation/research-{bible,topic,application,experience,illustration,qa,wol,prayer,public-talk}/**/*.md` | 보조 리서치 에이전트만 작성 |

## 2. 허용 영역 (메인 Claude Edit/Write 가능)

| 경로 | 사유 |
|---|---|
| `/Users/brandon/Claude/Projects/Congregation/_automation/build_*.py` · `validators.py` · `quality_check.py` | 빌더·검증 헬퍼 — 시스템 코드 |
| `/Users/brandon/Claude/Projects/Congregation/.claude/shared/*.md` | 정책 정본 |
| `/Users/brandon/Claude/Projects/Congregation/.claude/agents/*.md` | 에이전트 정의 |
| `/Users/brandon/Claude/Projects/Congregation/.claude/commands/**/SKILL.md` | 스킬 정의 |
| `/Users/brandon/Claude/Projects/Congregation/.claude/hooks/*.py` | hook 스크립트 |
| `/Users/brandon/Claude/Projects/Congregation/.claude/settings.json` | hook·권한 설정 |
| `/Users/brandon/Claude/Projects/Congregation/CLAUDE.md` · `_automation/CLAUDE.md` | 프로젝트 지침 |
| `/Users/brandon/.claude/plans/*.md` | plan 파일 |

## 3. 의심 어휘 발견 시 절차

메인 Claude 가 콘텐츠 (script.md·content_*.py·docx) 안에서 의심 어휘를 발견하면 — **직접 Edit 금지**. 다음 절차 의무:

1. `jw-style-checker` 에이전트 호출 (대상 파일 명시)
2. 에이전트가 `banned-vocabulary.md` + WOL WebFetch 로 권장 어휘 결정
3. 에이전트의 보고서에 따라 `spiritual-gems-script` (또는 해당 script 에이전트) 재호출 → script 가 정정
4. 정정된 script.md 를 일반 변환 Agent (general-purpose) 에 위임 → content_*.py 갱신
5. 빌더 재실행 → validators.py 가 자동 검증 → 통과 시 docx 디스크 안착

**메인 Claude 의 직접 Edit 단계 0개.**

## 4. 위반 사례 (학습용)

### 사례 1 (2026-05-01) — "사역→봉사" 직관 정정

- **상황**: jw-style-checker 가 jw-style-checker.md §3 표 누락으로 "사역" HIGH 위반 미감지. 메인 Claude 가 grep 으로 "사역" 4건 직접 발견 후 Edit 으로 "사역→봉사·메시아 사역→메시아의 봉사" 변환.
- **문제**: WOL WebFetch 검증 없이 직관 선택. "메시아의 봉사" 가 wol.jw.org 표준 표현인지 미검증.
- **올바른 절차**: jw-style-checker 호출 → WebFetch wol.jw.org → 권장 어휘 결정 → spiritual-gems-script 재호출 → content_sg_*.py 재변환 (Agent 위임) → 빌드.

## 5. 강제 메커니즘 (Phase E 향후 확장)

현재 본 정책은 **선언적**. 향후 `.claude/hooks/edit-restriction-hook.py` 신설 — 메인 Claude 의 Edit/Write 호출 시 경로 검사 후 금지 영역이면 차단.

지금까지는 메인 Claude 가 본 정책을 자율 준수.

## 6. 변경 이력

- 2026-05-01: 초판 신설. "사역→봉사" 직관 정정 사고 후 정책 정립.
