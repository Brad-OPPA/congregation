# 스킬 ↔ 에이전트 상관관계 (2026-04-30 스냅샷)

> 출처: `~/.claude/skills/` (글로벌 스킬 20개) + `~/Claude/Projects/Congregation/.claude/agents/` (회중 에이전트 32개) 직접 추출.
> 정책 정본: `.claude/shared/multi-layer-defense.md` (6단 방어), `.claude/shared/output-naming-policy.md` (출력 정책).

---

## 1️⃣ 단편 스킬 13개 — 실제 호출 체인

각 스킬은 `planner → script → 보조 리서치 → 공통 감수 게이트 4종` 흐름:

| # | 스킬 | Planner | Script | 보조 리서치 / 특수 |
|---|---|---|---|---|
| 1 | `/mid-talk10` | treasures-talk-planner | treasures-talk-script + **assembly-coordinator** | scripture-deep · publication-cross-ref · illustration-finder · experience-collector · application-builder |
| 2 | `/dig-treasures` | spiritual-gems-planner | spiritual-gems-script | (mid-talk10 과 동일 5종) |
| 3 | `/mid-student1` | (없음) | student-assignment-script | 단독 — 낭독 단순 |
| 4 | `/mid-student2` | student-assignment-planner | student-assignment-script | scripture-deep · application-builder · experience-collector + role-play-scenario-designer |
| 5 | `/mid-student3` | student-assignment-planner | student-assignment-script | (#4 와 동일) |
| 6 | `/mid-student4` | student-assignment-planner | student-assignment-script | role-play-scenario-designer |
| 7 | `/mid-talk5` | student-talk-planner | student-talk-script | (mid-talk10 과 동일 5종) |
| 8 | `/living-part` | living-part-planner | living-part-script | subtype별 (qa-designer · application-builder · experience-collector · publication-cross-ref) |
| 9 | `/local-needs` | local-needs-planner | (planner 직접 작성) | scripture-deep · publication-cross-ref · application-builder · experience-collector · illustration-finder + slides-builder |
| 10 | `/cbs` | cbs-planner | cbs-script | qa-designer · scripture-deep · publication-cross-ref · application-builder + (선택) experience-collector · illustration-finder |
| 11 | `/chair` | chair-script-builder (1·4단계 책임) | chair-script-builder | prayer-composer × 2 (시작·마침) |
| 12 | `/publictalk` | public-talk-builder | public-talk-script | scripture-deep · publication-cross-ref · illustration-finder · experience-collector · application-builder · qa-designer |
| 13 | `/week-study` | watchtower-study-planner | (planner 직접 작성) | wol-researcher · scripture-deep · publication-cross-ref · qa-designer · application-builder · experience-collector · illustration-finder · public-talk-builder |

---

## 2️⃣ 공통 감수 게이트 (모든 스킬 종료 시 4종 병렬 호출)

| 게이트 | 기능 | 비고 |
|---|---|---|
| **fact-checker** | 사실·인용·성구 표기 검증 | research-factcheck/ 저장 |
| **jw-style-checker** | 공식 용어·호칭·신세계역 표기 | research-style/ 저장 |
| **timing-auditor** | 낭독 시간 측정 (±60→±120초 완화) | dig-treasures 만 제외 (시간 제약 없음). research-timing/ 저장 |
| **quality-monotonic-checker** | 직전 주차 대비 품질 단조 증가 (9축, 5회 한도 자동 재작성) | research-quality/ 저장. **quality > timing** — timing FAIL 이라도 quality PASS 면 통과 |

---

## 3️⃣ 일괄 스킬 7개 — 단편 호출자

| 일괄 스킬 | 호출하는 단편 |
|---|---|
| `/mid-study1` | `/mid-talk10` × now/next1/next2 (3주치) |
| `/mid-study2` | `/dig-treasures` × 3주치 |
| `/mid-study3` | `/cbs` × 3주치 |
| `/midweek-now` | 11개 단편 — mid-talk10 + dig-treasures + mid-student1~4 + mid-talk5 + living-part + cbs + chair (회중의 필요 제외) |
| `/midweek-next1` | 11개 단편 (다음 주) |
| `/midweek-next2` | 11개 단편 (2주 뒤) |
| `/midweek-next3` | 11개 단편 (3주 뒤) |

---

## 4️⃣ 글로벌 명령 (`~/.claude/commands/`, 회중 외)

| 명령 | 용도 |
|---|---|
| `/weekly` | 매주 월요일 — 3주치 4파트 자동 생성 + 메일 + 카톡 (1단계 본인 검수, 2단계 5명 발송) |
| `/email-draft` | 영문 비즈니스 메일 초안 (베트남 사업) |
| `/trip-report` | 출장 보고서 .docx + 발표 자료 .pptx |

---

## 5️⃣ 에이전트 31개 — 카테고리별 분류

### 🔍 리서치 (8) — 결과를 `research-*/` 폴더에 저장

| 에이전트 | 용도 | 저장 폴더 |
|---|---|---|
| `wol-researcher` | 주차 프로그램·본문·성구·삽화 목록화 | research-wol/ |
| `publication-cross-ref` | 주제 횡단 (파·깨·통·예-1·JW방송) | research-topic/ |
| `scripture-deep` | 성구 심층 (번역·원어·배경·병행) | research-bible/ |
| `illustration-finder` | 예화·비유·서론·결론 초안 | research-illustration/ |
| `qa-designer` | 문답 블록 설계 | research-qa/ |
| `application-builder` | 실생활 적용 카드 | research-application/ |
| `experience-collector` | 공식 경험담 수집 | research-experience/ |
| `public-talk-builder` | 공개 강연 30분 아웃라인·재료 | research-public-talk/ |

### 📐 기획 Planner (8) — 스킬별 지시서 작성

`treasures-talk-planner` · `spiritual-gems-planner` · `cbs-planner` · `watchtower-study-planner` · `living-part-planner` · `local-needs-planner` · `student-assignment-planner` · `student-talk-planner`

### ✍ 대본 Script (8) — 실제 원고 작성

`treasures-talk-script` · `spiritual-gems-script` · `cbs-script` · `living-part-script` · `student-assignment-script` · `student-talk-script` · `chair-script-builder` · `public-talk-script`

### ⭐ 특수 빌더·조합 (4)

| 에이전트 | 용도 |
|---|---|
| `prayer-composer` | 기도문 (시작·마침) |
| `slides-builder` | pptx 슬라이드 |
| `role-play-scenario-designer` | 학생 시연 시나리오 |
| **`assembly-coordinator`** ⭐ 신규 (2026-04-30) | 10분 연설 본문 흐름 조합·매핑·R1~R10 1차 검증 — script ↔ build 사이 단계, 옵션 B |

### 🛡 감수 게이트 (4) — 2026-04-29 4종으로 확장

`fact-checker` · `jw-style-checker` · `timing-auditor` · `quality-monotonic-checker`

---

## 6️⃣ 에이전트 → 사용처 (역색인)

| 에이전트 | 사용하는 스킬 |
|---|---|
| **scripture-deep** | mid-talk10 · dig-treasures · mid-student2/3 · mid-talk5 · local-needs · cbs · publictalk · week-study (8개) |
| **publication-cross-ref** | mid-talk10 · dig-treasures · mid-talk5 · living-part · local-needs · cbs · publictalk · week-study (8개) |
| **illustration-finder** | mid-talk10 · dig-treasures · mid-talk5 · living-part · local-needs · publictalk · week-study (7개) |
| **experience-collector** | 거의 전 스킬 (cbs/dig-treasures 는 선택) |
| **application-builder** | 거의 전 스킬 |
| **qa-designer** | living-part · local-needs · cbs · publictalk · week-study |
| **wol-researcher** | week-study · local-needs |
| **public-talk-builder** | publictalk · week-study · local-needs |
| **prayer-composer** | chair 만 |
| **slides-builder** | local-needs 만 |
| **role-play-scenario-designer** | mid-student2/3/4 |
| **fact-checker / jw-style-checker / quality-monotonic-checker** | 전 스킬 (필수) |
| **timing-auditor** | 전 스킬 (dig-treasures 제외) |

---

## 📊 한눈 요약 (전체 흐름)

```
[원준님 입력 /XXX]
    ↓
[일괄 스킬 7개] ─────→ [단편 스킬 13개] ─────→ [planner 8개]
                                              ↓
                                          [script 8개]
                                              ↓
                                  [리서치 8개 + 특수 3개]
                                              ↓
                              [공통 감수 게이트 4종 병렬]
                                              ↓
                                  [content_*.py + build_*.py]
                                              ↓
                                  [docx + PDF 출력 → Dropbox WS]
```

---

## 🔧 빌드 환경 (2026-04-30 검증)

| 항목 | 상태 |
|---|---|
| Python 3.14.4 (Homebrew) | ✅ |
| python-docx 1.2.0 · lxml 6.1.0 · requests 2.33.1 | ✅ |
| Pillow 12.2.0 · python-pptx 1.0.2 · XlsxWriter 3.2.9 | ✅ (이번 세션 설치) |
| LibreOffice (`/Applications/LibreOffice.app` + `soffice` Homebrew) | ✅ |
| 정본 빌더 12개 syntax | ✅ |
| Path.home() 경로 4개 (META + 출력) | ✅ |
| 글로벌 스킬 20개 / 회중 에이전트 32개 / Hooks 2개 | ✅ |

---

## 📍 인프라 위치

```
~/Claude/Projects/Congregation/                    ← 새 META 정본 (이 파일 위치)
├── .claude/
│   ├── agents/         (31개)
│   ├── shared/         (8개 정책)
│   ├── hooks/          (2개)
│   └── settings.json   (UserPromptSubmit + Stop hook 등록)
├── _automation/        (빌더 + .git congregation-automation)
├── research-*/         (15개 — 에이전트 산출물)
└── .git (congregation, main)

~/.claude/
├── skills/             (20개 — 슬래시 스킬)
├── commands/           (3개 — weekly · email-draft · trip-report)
└── projects/-Users-brandon/memory/   (자동 메모리)

~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/      ← 출력 (그대로)
├── 01.주중집회/        (5 섹션)
└── 02.주말집회/
```

---

## 📅 변경 이력

- **2026-04-30 (1차)** — 최초 작성. Dropbox META → `~/Claude/Projects/Congregation/` 합병 직후 스냅샷.
- **2026-04-30 (2차)** — `assembly-coordinator` 신규 (10분 연설 옵션 B 조합 단계). 31 → 32 에이전트.
- 단편 스킬 13개 (CLAUDE.md 명시 11개 + chair + publictalk).
- 감수 게이트 quality-monotonic-checker 신규 (2026-04-29).
- Pillow + python-pptx 신규 설치 (2026-04-30).
