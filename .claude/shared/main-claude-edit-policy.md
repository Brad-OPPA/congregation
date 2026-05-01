# 메인 Claude 직접 Edit 제약 정책 (v2 — 단순/복잡 분리)

> **무조건 위임 X — 단순한 정정은 메인 직접·복잡 정정만 Agent 위임.**
> 효율과 안전의 균형: 1~3 글자 치환 같은 명백한 정정에 Agent 호출 오버헤드 X.
> 작성: 2026-05-01 v1 / 갱신: 2026-05-01 v2 (사용자 결정 — "무조건 위임" 원칙 폐기)

## 1. 정책 분류

### A. 메인 Claude 직접 Edit **허용** (단순 정정)

다음 조건 모두 충족 시 메인 직접 처리 OK:

1. **wol.jw.org 직접 fetch 로 정답 확인 후** 정정
2. **명백한 글자 단위 위반** — 추측·창작·해석 0:
   - NWT verbatim 글자 어긋남 (wol fetch 비교 후 글자 단위 교체)
   - 사용자 NG 표기 (예: "한놈" → "힌놈")
   - 가짜 docid·잘못된 면 번호 **삭제** (대체 출처 추가는 Agent)
   - 어순·맞춤법·띄어쓰기 정정
3. **1~3 라인 이내 변경** (단락 재작성 X)
4. **의미·구조 변경 없음** — 표기·표현만 정정

### B. Agent 위임 **의무** (복잡 정정)

다음 중 하나라도 해당하면 Agent 호출 의무:

1. **단락 재작성·구조 변경** (5+ 라인)
2. **새 자료·콘텐츠 추가** (출처·통계·예화·경험담 신규)
3. **어조·관점·강조점 변경**
4. **wol fetch 로도 정답이 명확하지 않음** — 해석 필요
5. **다중 위치 의미적 정합성** (한 곳 수정이 다른 곳 영향)
6. **사용자 직관 정정 사고 위험 영역** (예: 신학 어휘·교리 용어)

### C. 절대 Edit 금지 영역 (v2 유지)

- 회중 docx 디스크 직접 편집 금지 — 항상 빌더 통해서만
- 메모리 (`~/.claude/projects/.../memory/`) 의 사용자 권한 영역

## 2. 영역별 메인 Edit 허용 매트릭스

| 경로 | 단순 정정 (A) | 복잡 정정 (B) |
|---|---|---|
| `/Dropbox/02.WatchTower/.../*.docx` | ❌ 절대 금지 (빌더 통해서만) | ❌ 절대 금지 |
| `/_automation/content_*.py` | ✅ **허용** (메인 직접 OK) | ⚠ Agent 위임 의무 |
| `/research-plan/**/script.md` | ✅ **허용** (단순 표기 정정) | ⚠ spiritual-gems-script 재호출 |
| `/research-plan/**/outline.md` · `meta.yaml` | ✅ **허용** (단순 정정) | ⚠ spiritual-gems-planner 재호출 |
| `/research-{bible,topic,...}/**/*.md` | ✅ **허용** | ⚠ 해당 보조 재호출 |
| `/_automation/*.py` (빌더·validators) | ✅ 허용 | ✅ 허용 |
| `.claude/shared/*.md` · `.claude/agents/*.md` · `.claude/hooks/*.py` | ✅ 허용 | ✅ 허용 |
| `.claude/settings.json` | ✅ 허용 | ✅ 허용 |

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

## 3. 의심 어휘 발견 시 절차 (v2 — 분류별)

### 3-A. 명백한 단순 정정 (메인 직접 OK)

WOL fetch 로 정답이 명확하면 메인 직접:
- 표기 (예: "한놈" → "힌놈") — wol 검색 결과로 결정
- NWT verbatim 글자 단위 어긋남 — wol nwtsty fetch 비교
- 가짜 docid·면 번호 — 인용 자체 삭제

### 3-B. 복잡한 의심 어휘 (Agent 위임)

- 신학 어휘 (예: "사역" → ?·"신학" → ?) — wol 매치 다양해 해석 필요 → jw-style-checker
- 표 밖 의심 어휘 + 권장 대안 모호 → jw-style-checker WOL WebFetch 의무
- 다중 위치 의미 변경 → 해당 script 에이전트 재호출

## 4. 위반 사례 (학습용)

### 사례 1 (2026-05-01) — "사역→봉사" 직관 정정

- **상황**: jw-style-checker 가 jw-style-checker.md §3 표 누락으로 "사역" HIGH 위반 미감지. 메인 Claude 가 grep 으로 "사역" 4건 직접 발견 후 Edit 으로 "사역→봉사·메시아 사역→메시아의 봉사" 변환.
- **문제**: WOL WebFetch 검증 없이 직관 선택. "메시아의 봉사" 가 wol.jw.org 표준 표현인지 미검증.
- **올바른 절차**: jw-style-checker 호출 → WebFetch wol.jw.org → 권장 어휘 결정 → spiritual-gems-script 재호출 → content_sg_*.py 재변환 (Agent 위임) → 빌드.

## 5. 강제 메커니즘 (Phase E 향후 확장)

현재 본 정책은 **선언적**. 향후 `.claude/hooks/edit-restriction-hook.py` 신설 — 메인 Claude 의 Edit/Write 호출 시 경로 검사 후 금지 영역이면 차단.

지금까지는 메인 Claude 가 본 정책을 자율 준수.

## 6. 변경 이력

- 2026-05-01 v1: 초판 신설. "사역→봉사" 직관 정정 사고 후 "무조건 위임" 정책.
- 2026-05-01 v2: **사용자 결정 — "무조건 위임 원칙 폐기"**. 단순/복잡 분리 정책 도입. WOL fetch 로 정답이 명확한 글자 단위 정정은 메인 직접 허용 (Agent 호출 오버헤드 절약). 복잡 정정 (5+ 라인·새 자료·해석 필요) 만 Agent 의무.
