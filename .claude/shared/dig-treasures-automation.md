# 영적 보물찾기 자동화 종합 가이드 (정본)

> **이 파일이 영적 보물찾기 (`/dig-treasures`) 자동화의 구조·hook·정량 메트릭 종합 정본이다.**
> 매주 동일 퀄리티 + 깊이·다양성·적용점 자동 보장. 10개·100개 빌드해도 일관.
> 작성: 2026-05-01 (Phase E v2)

---

## §1. 전체 흐름 (단계별 책무)

```
[원준님 입력 또는 mid-study2 일괄]
   ↓
[① Planner 1차] — spiritual-gems-planner
   · WOL 주차 인덱스 fetch → 공식 질문 2개·표어 성구·통독 범위
   · 20성구 선정·outline.md·meta.yaml·5 보조 지시서
   ↓
[② 5 보조 병렬] — scripture-deep · publication-cross-ref · application-builder · experience-collector · illustration-finder
   · 각자 자체 검수 🔴 종료 블록
   ↓
[③ Planner 1차 재검수] — spiritual-gems-planner
   · 5 보조 산출물 vs 지시서 6축 대조
   · _planner_review_research.md (PASS / NEEDS-RERUN)
   ↓
[④ Script 작성] — spiritual-gems-script
   · 5 보조 + outline + meta 통합 → script.md
   · gem-narrative-standard 적용 (다각도 ≥2·4축 균형·자기점검)
   · 자체 검수 _selfcheck_script.md
   ↓
[⑤ gem-coordinator] — gem-coordinator (NEW v2)
   · 5블록 매핑 + R1~R10 1차 grep 검증
   · _gem_assembly_report.md + spec dict 드래프트
   ↓
[⑥ Planner 2차 재검수] — spiritual-gems-planner
   · script.md vs outline.md 6축 대조 + gem-coordinator 보고서 검토
   · _planner_final_review.md
   ↓
[⑦ content_sg_*.py 변환] — Agent 위임 (general-purpose)
   · script.md → spec dict → _automation/content_sg_{YYMMDD}.py
   ↓
[⑧ build_spiritual_gems.py 실행]
   · validators.py 자동 호출 (10 룰 자동 차단)
   · docx + PDF 디스크 안착
   ↓
[⑨ ⑥ 4종 병렬 감사] — fact-checker · jw-style-checker · timing-auditor (영보 N·A) · quality-monotonic-checker
   · HIGH 1건이라도 → Stop hook 자동 차단 + 재호출
```

**메인 Claude 의 역할**: 단계 간 호출·결과 수집·spec dict 변환 위임·빌더 실행만. **콘텐츠 직접 정정 0건** (`main-claude-edit-policy.md`).

---

## §2. 자료 수집 의무 표 (5 보조 정량)

각 보조 에이전트가 한 주차에 산출해야 할 **최소 의무**. 미달 시 ③ 재검수에서 NEEDS-RERUN.

| 보조 | 산출 폴더 | 정량 의무 | 깊이 항목 |
|---|---|---|---|
| **scripture-deep** | `research-bible/{YYMMDD}/gems_NN-*.md` (20개) | 20성구 × NWT verbatim + 어근 ≥3 + 평행 성구 ≥5 + 신약 성취 1~2 | 어원·평행·신약 성취 |
| **publication-cross-ref** | `research-topic/{YYMMDD}/gems_NN-cross-ref.md` (20개) + `gems_official-question-refs.md` | 「통」·「파」·「예-1·2」·「하」 횡단 ≥10 출처 + 공식 질문 verbatim | 교리 깊이 |
| **application-builder** | `research-application/{YYMMDD}/gems_NN-apply.md` (20개) | 20성구 × 4축 분포 (각 ≥2~4 — 가정·직장/학교·회중/전도·개인 영성) + 자기점검 질문 ≥10 | 일상 적용 |
| **experience-collector** | `research-experience/{YYMMDD}/gems_*.md` (5~8) | 핵심 5~8 성구 매칭 공식 경험담 (verbatim 출처·호수·면) | 경험담 |
| **illustration-finder** | `research-illustration/{YYMMDD}/gems_*.md` (5~8) | 14축 결합 후보 5~8 성구 (1차 자료 ≥2건 교차) | 고고학·일상 비유 |

**각 보조 의무 — 공통**:
- 🟢 착수 + 🔴 종료 블록 (intro-and-illustration-quality.md 정본)
- 호출자 접두사 `gems_` 적용 (다른 planner 와 폴더 충돌 방지)
- 가짜 docid 0건 (validators 가 ⑧ 단계에서 자동 차단)

---

## §3. 검증 자동화 표 (어디서·무엇을·어떻게)

| 단계 | 검증 도구 | 차단 항목 | 트리거 | 위반 시 |
|---|---|---|---|---|
| 빌드 직전 (`build_spiritual_gems.py L289`) | `validators.validate_spec_integrity` | 필수 키 / HIGH 금칙어 / 사용자 NG / 의심 어휘 / 라벨 표준 / 14축 ≥5 / 깊이 ≥7 / 4축 균형 (각 ≥4) / 다각도 (각 gem ≥2, 예외 ≤4) | spec dict 호출 시 | ValueError raise → docx 미생성 |
| ⑤ gem-coordinator | R1~R10 grep | 글자·성구·출판·14축·깊이·4축·다각도·라벨·NWT verbatim·docid | script.md 산출 직후 | NEEDS-FIX 보고 → script 또는 5 보조 재호출 |
| Stop hook 1 | `factcheck-numbers.py` | 미검증 수치·통계 | 메인 응답 종료 시 | sys.exit 2 차단 |
| Stop hook 2 | `quality-loop-enforcer.py` | quality-monotonic-checker NO-GO | 동일 | sys.exit 2 차단 + 재작성 메시지 주입 |
| Stop hook 3 | `fact-loop-enforcer.py` | fact-checker HIGH ≥1 | 동일 | sys.exit 2 차단 + 재호출 메시지 주입 |
| UserPromptSubmit hook 1 | `skill-source-reminder.py` | 정책 Read 의무 reminder | 사용자 prompt 입력 시 | stderr 알림 |
| UserPromptSubmit hook 2 | `edit-restriction-hook.py` | 메인 Claude 직접 정정 영역 reminder | 동일 | stderr 알림 (정책 인지) |
| ⑥ 4종 감사 | fact-checker · jw-style-checker · timing-auditor (N·A 영보) · quality-monotonic-checker | 사실·용어·단조 증가 | docx 빌드 후 | HIGH 1건이라도 재빌드 |

---

## §4. Hook 작동 시점 (chronological)

```
[사용자 prompt 입력]
   ↓ UserPromptSubmit
   ├─ skill-source-reminder.py (정책 Read 의무)
   └─ edit-restriction-hook.py (메인 직접 정정 금지 영역)
   ↓
[메인 Claude 작업 — 빌드까지]
   ↓ 빌드 시점 (build_spiritual_gems.py)
   ├─ validators.py 10 룰 자동 차단 (HIGH → ValueError raise)
   ↓ 빌드 후 (디스크 안착)
[⑥ 4종 감사 + ⑤ gem-coordinator 재검토]
   ↓
[메인 Claude 응답 종료 시]
   ↓ Stop
   ├─ factcheck-numbers.py (수치)
   ├─ quality-loop-enforcer.py (quality NO-GO 차단)
   └─ fact-loop-enforcer.py (fact HIGH 차단)
```

---

## §5. 정량 메트릭 (영보 슬롯 절대 하한 + v2 강화)

`quality-monotonic-policy.md` §1 동기화. 모두 validators.py 가 자동 차단 (HIGH).

| 축 | 절대 하한 | v1 정책 | v2 강화 | 비고 |
|---|---|---|---|---|
| A. 글자수 | ≥7,500 | ≥7,500 | (동일) | script 본문 |
| B. 성구 인용 | ≥50 | ≥50 | (동일) | verse_ref + 평행 |
| C. 출판물「」 | ≥10 | ≥10 | (동일) | docid 실존 검증 |
| D. 외부 14축 | ≥2 | ≥2 | **≥5** | gem-narrative §2 |
| E. 시간 마커 | N·A | N·A | (동일) | 영보 시간 비강제 |
| F. 슬롯 구조 | 100% | 100% | (동일) | 20성구 × 3항 |
| G. 깊이 단락 | (정책 ≥5) | ≥5 | **≥7** | 어원·고고·과학·평행 |
| H. 이미지 | 0 | 0 | (동일) | 영보 N·A |
| I. 구성 표준 | 100% | 100% | (동일) | 5블록 |
| J. 라벨 일관성 | 100% | 100% | (동일) | ① 핵심·② 적용·③ 배울점 |
| **L. 다각도 (NEW, 권고)** | (없음) | (없음) | **참고 측정** (강제 X) — 키워드 매칭으로 어원·평행·고고·신약 성취·일상·교리 카운트 | gem-narrative §2 (이모지 미사용) |

> **4축 균형 폐기** (2026-05-01) — 영보는 통독 범위 주제 특성상 4축 (가정·직장·회중·개인) 모두 자연스럽게 적용하기 어려움. 강제 검증 X. application-builder 산출 시 참고용 분포 정보만 표시.

---

## §6. 회귀 적용 절차 (v2 강화 후)

직전 빌드 메트릭이 v2 베이스라인 미달 시 자동 재작성 루프 (5회 한도):

```
[새 빌드 산출 docx]
   ↓
[validators 빌드 시 자동 검증]
   ├─ 10 룰 통과 → 디스크 안착
   └─ HIGH ≥1 → ValueError raise → 재호출
       ↓
   [메인 Claude 가 보강 필요 메트릭 식별]
       ├─ 14축 < 5 → publication-cross-ref + illustration-finder 재호출
       ├─ 깊이 < 7 → scripture-deep 재호출 (어원·고고 보강)
       ├─ 4축 균형 미달 → application-builder 재호출 (부족 축)
       ├─ 다각도 < 2 → spiritual-gems-script 재호출
       ├─ NWT verbatim 위반 → spiritual-gems-script 재호출
       └─ docid 가짜 → publication-cross-ref 재호출
   ↓
[보조 산출물 갱신 → script 재작성 → spec dict 재변환 → 빌더 재실행]
   ↓
[validators 재검증]
   ├─ PASS → 디스크 안착 + ⑥ 4종 감사
   └─ FAIL → 재호출 (5회 한도)
       ↓
   [5회 한도 도달 시 BLOCKING 알림]
       └─ 사용자 수동 검수·결정 필요
```

---

## §7. 메인 Claude 의 역할 — 직접 정정 금지 영역 (다시 강조)

`main-claude-edit-policy.md` 와 동기화:

**금지** (Edit/Write 시 정책 위반):
- `_automation/content_sg_*.py`
- `research-plan/spiritual-gems/*/script.md`·`outline.md`·`meta.yaml`
- `research-bible|topic|application|experience|illustration/{YYMMDD}/*.md`
- `Dropbox/02.WatchTower/01.▣ 수원 연무 회중/.../*.docx`

**허용** (시스템 코드·정책):
- `_automation/build_*.py`·`validators.py`
- `.claude/shared/*.md`
- `.claude/agents/*.md`
- `.claude/hooks/*.py`
- `.claude/settings.json`
- 본 가이드 자체

**우회 시 작동**: edit-restriction-hook.py 가 stderr reminder 출력. 메인 Claude 자율 준수가 1차 안전망.

---

## §8. 메인 Claude 정정 — 단순/복잡 분리 정책 (Phase E v2-bis, 2026-05-01)

"무조건 위임" 원칙 폐기. 정정 종류 따라:

### A. 메인 Claude 직접 Edit 허용 (단순 정정)
- WOL fetch 로 정답이 명확한 글자 단위 위반
- NWT verbatim 어순·표기 정정
- 사용자 NG 표기 (예: "한놈" → "힌놈")
- 가짜 docid·면 번호 삭제
- 1~3 라인 이내 변경
- 의미·구조 변경 없음

### B. Agent 위임 의무 (복잡 정정)
- 단락 재작성·구조 변경 (5+ 라인)
- 새 자료·내용 추가
- 어조·관점·강조점 변경
- 다중 위치 의미 변경
- WOL fetch 로 정답 모호 (해석 필요)

세부: `.claude/shared/main-claude-edit-policy.md` v2

## §9. fact-checker docx 직접 추출 의무 (Phase E v2-bis)

fact-checker 가 docx 검수 시 script.md·캐시된 옛 본문 의존 금지. 반드시 docx 자체 텍스트 추출 후 검사:

```bash
unzip -p "{docx_path}" word/document.xml | grep -E "{검사_패턴}"
```

**사유**: 260528 빌드 사고 — fact-checker 가 script.md 본문 또는 옛 docx 캐시 참조하여 false positive 보고. docx 가 정정 반영됐는데 미정정으로 잘못 판단 → fact-loop-enforcer false trigger. 정책 갱신: `.claude/agents/fact-checker.md` §🔴 v2-bis.

## §10. Stop hook 3종 강제 메커니즘

| hook | 트리거 조건 | 차단 효과 |
|---|---|---|
| `factcheck-numbers.py` | 미검증 수치·통계 발견 | sys.exit 2 (응답 차단) |
| `quality-loop-enforcer.py` | quality-monotonic-checker NO-GO 보고서 (30분 안 작성) | sys.exit 2 + 재작성 메시지 |
| `fact-loop-enforcer.py` | research-factcheck/{YYMMDD}/factcheck_*.md HIGH ≥1 | sys.exit 2 + 재호출 메시지 |

bypass: `QUALITY_LOOP_BYPASS=1` / `FACT_LOOP_BYPASS=1` 환경변수 (긴급용).

## §11. 변경 이력

- 2026-05-01 v1: Phase E v2 — 영적 보물찾기 자동화 v2 신설. gem-coordinator + gem-narrative-standard + validators 5 함수 통합. CLAUDE.md 간소화 + 본 가이드 신설.
- 2026-05-01 v2 (본 세션 추가): "무조건 위임" 폐기 → 단순/복잡 분리 (§8) + fact-checker docx 직접 추출 의무 (§9) + Stop hook 3종 (§10) + 4축 균형·다각도·깊이 강제 폐기 (정보 측정만, 자연스러움 우선) + fact-loop-enforcer.py + edit-restriction-hook.py 신설.
