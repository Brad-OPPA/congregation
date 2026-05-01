---
name: midweek-next3
description: 3주 뒤 목요일 주중집회 전체 자료를 일괄 생성 (회중의 필요 제외). 11개 파트 스킬을 인자 `next3` 로 순차 호출 — mid-talk10, dig-treasures, mid-student1~4, mid-talk5, living-part, cbs, chair (사회자 전체 대본). 각 파트 독립 docx/PDF. 회중의 필요는 별도로 `/local-needs next3` 실행. 트리거 "/midweek-next3", "3주 뒤 주중집회 만들어 줘".
---

## 🛡 품질 단조 증가 집계 (필수, 2026-04-29 도입)

이 오케스트레이터가 호출하는 모든 단편 스킬은 ⑥ 단계에 quality-monotonic-checker (4종 병렬) 자동 동작. 직전 주차 대비 품질 하락 시 자동 재작성 강제.

오케스트레이터 책무 — **slot-별 quality-monotonic 결과 집계**:
- 한 슬롯이라도 NO-GO (5회 시도 후 실패) → 사용자 BLOCKING 알림
- 모두 PASS → 자동 종결 + 카톡

세부: `.claude/shared/quality-monotonic-policy.md`

# midweek-next3 — 3주 뒤 주중집회 전체 (회중의 필요 제외)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** 호출하는 단편 스킬의 산출물 그대로 (docx + PDF 등)

## 이 스킬의 범위
- **3주 뒤 목요일 집회** 자료 전체 일괄 생성
- 포함 파트 11개 — `/midweek-now` 와 동일 (주차만 다름)
- **제외 파트**: 회중의 필요 — `/local-needs next3` 별도

## 실행 단계

### 0. 주차 확인
오늘 기준 3주 뒤 목요일 YYMMDD 계산 후 원준님 확정.

### 1. 파트 스킬 순차 호출 (인자 `next3`)

1. Skill(mid-talk10, args="next3")
2. Skill(dig-treasures, args="next3")
3. Skill(mid-student1, args="next3")
4. Skill(mid-student2, args="next3")
5. Skill(mid-student3, args="next3")
6. Skill(mid-student4, args="next3")
7. Skill(mid-talk5, args="next3")
8. Skill(living-part, args="next3")
9. Skill(cbs, args="next3")
10. Skill(chair, args="next3")          # 마지막 — 다른 파트 다 끝난 후 통합 사회자 대본 (chair 본문에서 8가지 슬롯 대화형 입력)

### 2. 종합 보고
`/midweek-now` 와 동일 포맷.

### 3. 에러 처리
`/midweek-now` 와 동일.


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
midweek-next3 ({YYMMDD-MMDD}) 산출물 현황:
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
- **신규 빌드 결정** → `Skill(단편, args="next3")` 호출 (단편은 묶음 컨텍스트 안에서 정상 진행)
- **ver_up 결정** → `Skill(단편, args="next3 --from-batch=ver_up")` 형태로 컨텍스트 전달, 단편은 `_verN_` 자동 부여

각 단편 스킬은 일괄 컨텍스트 안에서 호출되면 **자체 단정형 확인 묻지 않고** 결정 그대로 실행 — chair 는 예외 (자체 슬롯 입력 별도).
