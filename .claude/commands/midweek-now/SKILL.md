---
name: midweek-now
description: 이번 주 목요일 주중집회 전체 자료를 일괄 생성 (회중의 필요 제외). 11개 파트 스킬을 순차 호출 — mid-talk10, dig-treasures, mid-student1~4, mid-talk5, living-part, cbs, chair (사회자 전체 대본). 각 파트는 독립 docx/PDF 로 저장되어 담당자별 배포 가능. 회중의 필요(local-needs)는 장로의회 주제 입력이 필요해 제외 — 별도로 `/local-needs` 실행. 트리거 "/midweek-now", "이번 주 주중집회 만들어 줘", "이번주 주중 다 만들어".
---

## 🛡 품질 단조 증가 집계 (필수, 2026-04-29 도입)

이 오케스트레이터가 호출하는 모든 단편 스킬은 ⑥ 단계에 quality-monotonic-checker (4종 병렬) 자동 동작. 직전 주차 대비 품질 하락 시 자동 재작성 강제.

오케스트레이터 책무 — **slot-별 quality-monotonic 결과 집계**:
- 한 슬롯이라도 NO-GO (5회 시도 후 실패) → 사용자 BLOCKING 알림
- 모두 PASS → 자동 종결 + 카톡

세부: `.claude/shared/quality-monotonic-policy.md`

# midweek-now — 이번 주 주중집회 전체 (회중의 필요 제외)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** 호출하는 단편 스킬의 산출물 그대로 (docx + PDF 등)

## 이 스킬의 범위
- **이번 주 목요일 집회** 자료 전체 일괄 생성
- 포함 파트 11개:
  1. `/mid-talk10` — 10분 연설
  2. `/dig-treasures` — 영적 보물찾기
  3. `/mid-student1` — 성경 낭독
  4. `/mid-student2` — 학생 과제 #1 (WOL 4번)
  5. `/mid-student3` — 학생 과제 #2 (WOL 5번)
  6. `/mid-student4` — 학생 과제 #3 (WOL 6번, 있는 주만)
  7. `/mid-talk5` — 5분 연설
  8. `/living-part` — 그리스도인 생활 파트
  9. `/cbs` — 회중 성서 연구
  10. `/chair` — **주중집회 사회자 전체 대본** (1시간 45분, 9개 시간 마커, 시작·마침 기도 포함). 다른 파트 다 끝난 후 마지막에 호출 — 필수 슬롯 8가지(기도 담당자·노래 3개·학생 과제·CBS 담당·다음 주 임명·광고)는 chair 본문에서 대화형 입력
- **제외 파트**: 회중의 필요(local_needs) — 장로의회 주제 입력 필요, `/local-needs` 별도 실행

## 실행 단계

### 0. 주차 확인
오늘 날짜 기준 이번 주 목요일 YYMMDD 계산. 원준님에게 1회 확정:

> 이번 주 목요일({M월 D일}) 주중집회 전체 자료를 생성합니다. 진행할까요?

### 1. 파트 스킬 호출 — ⚡ **병렬 그룹 + chair 마지막 (2026-05-09 도입)**

각 파트 스킬을 인자 `now` 로 호출. 파트 내부에서 이미 주차 UX·WOL-first·할루시네이션 금지·감수 게이트·docx 렌더까지 다 수행.

**의존성 분석**:
- 9개 파트 (mid-talk10 / dig-treasures / mid-student1~4 / mid-talk5 / living-part / cbs) → **서로 독립** ✅ 병렬 가능
- chair (사회자 대본) → 다른 파트 결과를 통합하므로 **마지막** ❌ 병렬 불가

**병렬 그룹 흐름**:

```
[그룹 A — 9 Skill 동시 호출, 한 메시지 안에] ⚡
  Skill(mid-talk10, args="now")
  Skill(dig-treasures, args="now")
  Skill(mid-student1, args="now")
  Skill(mid-student2, args="now")
  Skill(mid-student3, args="now")
  Skill(mid-student4, args="now")    # 내부에서 슬롯 없으면 자동 skip
  Skill(mid-talk5, args="now")
  Skill(living-part, args="now")
  Skill(cbs, args="now")
↓ 모두 완료 대기 (Anthropic 시스템이 자동 병렬 실행)
[그룹 B — chair 마지막]
  Skill(chair, args="now")   # 다른 파트 결과 통합 + 8가지 슬롯 대화형 입력
```

**메인 Claude = 팀 리더** 의 책무:
1. 그룹 A 9개 Skill 을 한 응답 메시지 안에 동시 호출
2. 9개 결과 받은 후 — 성공·실패 슬롯 집계 + 실패 슬롯 격리 (계속 진행, 최종 보고에 표시)
3. 그룹 B (chair) 호출 — 그룹 A 결과 누적 정보를 chair 의 대화형 입력에 활용
4. 30분 넘는 슬롯 → 사용자에게 진행 보고

**기대 효과**: 11 슬롯 순차 = 약 2시간 → 병렬 그룹 A + chair = **약 30~40분** (가장 긴 슬롯 + chair).

### 1-bis. 팀 에이전트 호출 시 정본 prepend (각 단편 스킬 내부)

각 단편 SKILL 이 회중 팀 에이전트 (cbs-planner, treasures-talk-planner 등) 를 Task 호출할 때 정본 가이드라인 prepend 의무:

```python
# 각 단편 스킬 내부
from team_briefings import get_briefing_for_team, prepend_to_prompt
brief = get_briefing_for_team("dig-treasures")  # 팀 키
augmented = prepend_to_prompt(original_prompt, brief)
Agent(subagent_type="spiritual-gems-planner", prompt=augmented, ...)
```

세부: Congregation/CLAUDE.md "회중 팀 에이전트 호출 시 정본 prepend 의무" 섹션.

### 2. 종합 보고

모든 파트 완료 후 한 화면에 정리:

```
✅ {YYMMDD} 주중집회 자료 일괄 생성 완료

10분 연설:       10분 연설_{주제}_YYMMDD.docx
영적 보물 찾기:  영적 보물 찾기_YYMMDD.docx
성경 낭독:       성경 낭독_YYMMDD.docx
학생 과제 #1:    학생 과제_{타입}_YYMMDD.docx
학생 과제 #2:    학생 과제_{타입}_YYMMDD.docx
학생 과제 #3:    학생 과제_{타입}_YYMMDD.docx  (또는 "이번 주 없음")
5분 연설:        5분 연설_{주제}_YYMMDD.docx
생활 파트:       그리스도인 생활_{제목}_YYMMDD.docx
회중 성서 연구:  회중 성서 연구_훈{장}-{장}_YYMMDD.docx
사회자 대본:    생봉 집회 사회 YYYYMMDD.docx          # 1시간 45분 통합 진행 대본

회중의 필요: /local-needs 를 장로의회 주제와 함께 별도 실행 필요
```

### 3. 에러 처리
- 특정 파트 실패 시 → 해당 파트만 재시도, 나머지 파트는 계속
- 3회 재시도 후에도 실패 → 원준님께 에러 보고하고 나머지 파트는 정상 완료
- 모든 파트 요약 보고에 성공/실패 상태 표시

## 기억할 점
- `/midweek-now` 는 순수 오케스트레이터. 각 파트 로직은 해당 파트 스킬 본문에 있음.
- 회중의 필요는 여기 없음 → 별도로 `/local-needs` 실행 필요.
- 매주 월요일 자동 실행은 `/weekly` 가 담당 — `/weekly` 내부에서 `midweek-now/next1/next2` 순차 호출.

---

## 산출물 존재 시 skip 정책 (필수)

스킬 진입 시 출력 폴더에 산출물이 이미 있는지 먼저 확인한다. 일괄 스킬이므로 **각 파트마다 따로 묻지 않고**, 아래 §0 묶음 확인 절차로 한 번에 처리한다.

- **없음**: 정상 진행
- **있음 + 사용자 무명시**: §0 묶음 확인 표 1회 → 답 없거나 No → **skip**
- **있음 + 사용자가 "재생성·업그레이드·버전 올려·다시 만들어" 명시**: 파일명 끝에 `_verN_` 부여 후 신규 생성 (기존 파일 보존). **N 자동 결정** — 같은 폴더에서 같은 prefix 의 `_verN_` 중 최댓값 +1, 없으면 `_ver2_`.

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3 + `.claude/shared/output-naming-policy.md` §4·§4-bis.

---

## 0. 묶음 확인 (시작 시점 필수)

이 일괄 스킬은 11개 파트를 한 번에 만들기 때문에, **각 파트마다 단정형 확인을 따로 묻지 않는다**. 진입 즉시 출력 폴더의 산출물 현황을 표로 한 번에 보고하고 사용자에게 한 번만 yes/no 받는다.

```
midweek-now ({YYMMDD-MMDD}) 산출물 현황:
| 파트 | 상태 |
|---|---|
| 10분 연설 | ✅ 있음 (ver2) / ❌ 없음 |
| 영적 보물 찾기 | ... |
| 성경 낭독 | ... |
| 학생 과제 #2 | ... |
| 학생 과제 #3 | ... |
| 학생 과제 #4 | ... |
| 5분 연설 | ... |
| 그리스도인 생활 | ... |
| 회중 성서 연구 | ... |
| 사회자 대본 | ... |

빠진 것만 만들까요? 아니면 있는 것도 다시 만들까요? (있는 것은 _verN_ 새 버전 추가, 기존 보존)
```

**원준님 응답에 따른 분기:**

- 답 없음 / "응" / "빠진 것만" / "그래" → ❌ 만 신규 빌드, ✅ 는 skip
- "다시 만들어" / "전부" / "버전 올려" → ✅ 도 모두 `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- "특정 파트만 다시" (예: "10분 연설만 다시") → 명시 파트만 `_verN_` 신규

**기준 — 자리 비움 시 안전:** 원준님이 자리 비우셨을 때도 답 없음 → skip 으로 자동 작동하므로 검수·발송된 docx 가 의도치 않게 덮어쓰이지 않는다.

## 단편 스킬 호출 시 컨텍스트 전달 (중복 묻기 방지)

이 일괄 스킬은 §0 에서 결정 사항을 받은 뒤, 각 단편 스킬 호출 시 그 결정을 인자·컨텍스트로 전달한다:

- **skip 결정** → 해당 단편 스킬 호출 자체를 발생시키지 않음
- **신규 빌드 결정** → `Skill(단편, args="now")` 호출 (단편은 묶음 컨텍스트 안에서 정상 진행)
- **ver_up 결정** → `Skill(단편, args="now --from-batch=ver_up")` 형태로 컨텍스트 전달, 단편은 `_verN_` 자동 부여

각 단편 스킬은 일괄 컨텍스트 안에서 호출되면 **자체 단정형 확인 묻지 않고** 결정 그대로 실행 — chair 는 예외 (자체 슬롯 입력 별도).
