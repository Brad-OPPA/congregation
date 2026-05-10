# HANDOFF — 파수대 정본 ver13 (2026-05-10 → 5/11)

## 이번 세션 (5/10 밤 ~ 새벽) 결론

**핵심 fix = INTEGRATED_COMMENTARY 자료에 핵심 명사구 [Y] 마커 박기.**

이전 ver12 까지의 진단:
- 사용자가 사진까지 보내며 "핵심만 강조" 명시했는데 ver12 docx 노랑 핵심 = 87~133개로 부족
- 원인 = INTEGRATED_COMMENTARY 텍스트 자료 자체에 `**`·`[Y]` 마커 0개. 빌더 v9 자동 강조 폐기 후 명시 마커만 처리 → 강조 부족

해결:
- **publication-cross-ref Task 3 병렬** → 작은 출력 (PHRASES dict 만, 32K 토큰 안)
- **메인 Claude re.sub** 으로 INTEGRATED 텍스트에 [Y]...[/Y] 마커 자동 삽입 (LLM 호출 없이 결정적)
- 결과: 노랑 핵심 명사구 87 → 426 (5/17), 77 → 400 (5/24), 133 → 421 (5/31) = **4~5배 증가**

---

## 산출 (Dropbox 정본 3 슬롯)

| 슬롯 | 파일 | 노랑 핵심 ≤25자 | 메인 박스 | 이미지 | 복습 답 |
|---|---|---|---|---|---|
| 5/17 | `260511-0517/파수대 사회_260517_ver13_.docx` + PDF | 426 | 6 | 4 | 3 |
| 5/24 | `260518-0524/파수대 사회_260524_ver13_.docx` + PDF | 400 | 7 | 2 | 3 |
| 5/31 | `260525-0531/파수대 사회_260531_ver13_.docx` + PDF | 421 | 3 | 3 | 5 |

**5/10 (이번 주 일요일)** = 사용자 평이름 정본 `파수대 사회_260510.docx` 보존 (사용자 명시 "5/10 손대지 말 것").

**5/31 사용자 OK 정본** = `_ver10_`·`_ver11_` 보존.

---

## git 영구화 (모두 push 완료)

### congregation-automation submodule (`master`)
- `82acc13` — 빌더 v9 (낭독 박스 통합 라벨 + 자동 강조 폐기 + body_runs `<strong>` 보존)

### congregation main repo (`main`)
- `a513993` — Phase A·B·C (script 에이전트 + /week-study 스킬 + 체크리스트 v3)
- `44e3051` — ver12 build script
- `ab5bb15` — 5/17 이미지 매핑 fix (string key 'f1~f4' 순서 fallback)
- `b272c13` — **ver13: PHRASES dict 3 슬롯 + ver13_build.py ([Y] 마커 자동 삽입)**

### 자료 보존 위치
- `research-plan/watchtower/{ymd}_canon/integrated_commentary.py` — INTEGRATED 5필드 (5/10·17·24·31)
- `research-bible/{ymd}_canon_v4/key_scripture_narratives.py` — NARRATIVES (5/10·17·24·31_v5)
- `research-illust/{ymd}_canon_v4/downloaded.py` — IMAGE_PATHS
- `research-illust/{ymd}_canon_v4/recap_answers.py` — RECAP_ANSWERS
- `research-illust/canon_v8_illust.py` — 12 삽화 [Y] description+commentary
- `research-illust/phrases_260{517,524,531}.py` — 핵심 명사구 dict (NEW)
- `research-illust/ver13_build.py` — [Y] 마커 자동 삽입 빌드 코드 (NEW)

---

## 자동화 인프라 v10 (이미 작성 완료)

- `.claude/agents/watchtower-study-script.md` — 자동화 핵심 lock-in 에이전트
- `.claude/commands/week-study/SKILL.md` — 스킬 갱신 (script 호출 통합)
- `.claude/shared/canonical-build-checklist.md` v3 — 9 항목 + 저녁 명시
- plan: `/Users/brandon/.claude/plans/adaptive-wandering-thunder.md` v11

---

## 🚨 내일 (5/11) 이어서 할 작업

### 1. ver13 PDF 검수 (사용자)
- 5/17·24·31 PDF 직접 확인
- 노랑 핵심 강조 패턴 = 사용자 명시 (5/10 사진) 과 일치하는지
- OK 또는 보강 사항 명시

### 2. (사용자 OK 후) 6/7 다음 주차 자동 빌드
- `/week-study now` (또는 `/weekly`) 호출
- watchtower-study-script ★ 자동화 흐름 검증
- 매주 동일 톤 보장 확인 — 사용자 OK 첫 검증

### 3. 자동화 인프라 정착 (사용자 검수 후)
- watchtower-study-script 에이전트 호출 패턴 안정화
- INTEGRATED 자료 작성 자동화 (publication-cross-ref + experience-collector + application-builder 병렬)
- PHRASES 자동 추출 → 마커 삽입 워크플로우 정착

### 4. 5/10 처리 (선택, 사용자 명시 후)
- 사용자가 "5/10 손대지 말 것" 명시 유지
- 또는 ver13 패턴으로 빌드할지 사용자 결정

---

## 메타 — 시간·코인 낭비 회피 (5/10 교훈)

- ❌ 매번 새 빌드 (canon_v3 → v4 → ... → ver12 → ver13) 누더기 반복
- ❌ Task 호출 시 출력 토큰 한도 (32K) 추산 안 함 → 1시간+ idle
- ❌ 같은 명시 반복 받음 (사용자 짜증)

✅ **이번 ver13 fix 패턴 = 작은 출력 + 메인 Claude 결정적 변환**
- LLM 출력 = phrases dict (작음)
- 메인 Claude = re.sub (LLM 호출 없음)
- 토큰 초과 X, 빠름

다음에도 큰 텍스트 변환은 이 패턴 — 핵심 추출만 LLM, 변환은 결정적 코드.

---

## 단일 진실의 원천

- **plan 파일**: `/Users/brandon/.claude/plans/adaptive-wandering-thunder.md` v11
- **체크리스트**: `.claude/shared/canonical-build-checklist.md` v3
- **이 HANDOFF**: 5/11 시작 시 첫 read

내일 시작 시 plan 파일 + 이 HANDOFF + 사용자 검수 결과 read 후 작업.
