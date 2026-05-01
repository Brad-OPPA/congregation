---
name: mid-student4
description: 주중집회 야외봉사 섹션 **학생 과제 #3 (WOL 6번 슬롯, 있는 주만)** 원고 1건을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3`. **4단 방어 프로토콜(`.claude/shared/multi-layer-defense.md`)** 준수. WOL 페이지에 6번 슬롯이 없으면 "학생 과제 #3 없음" 메시지 출력 후 종료. 있을 때 타입 자동 파싱 후 student-assignment-planner(과제번호 4) → 3개 보조 리서치 → Planner 재검수 → student-assignment-script → Planner 재검수 → docx → fact-checker·jw-style-checker·timing-auditor. 결과 `학생 과제_{타입}_YYMMDD.docx`. 트리거 "/mid-student4", "학생과제 3 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# mid-student4 — 야외봉사 학생 과제 #3 (WOL 6번 슬롯, 조건부, 4단 방어)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx (빌더 작성 후 PDF 자동 추가 예정)

## 이 스킬의 범위
- 학생 과제 3건 중 **세 번째** (WOL 6번 슬롯)
- **WOL 에 6번 슬롯이 없는 주는 실행 안 함** — "이번 주 학생 과제 #3 없음" 메시지 후 종료
- 구조는 `/mid-student2/3` 와 동일. **차이점: 과제번호 4, 조건부 실행**.

## 🛡 품질 원칙 — 4단 방어 프로토콜
`.claude/shared/multi-layer-defense.md` 준수. 실행 전 Read.

## 인자 규약
`now|next1|next2|next3`

## ⚠ WOL-first 수집 + 조건부 처리
1. 주차 인덱스 → "야외봉사" 블록 열기
2. **6번 슬롯 존재 여부 먼저 확인**:
   - 없으면 → "⚠ {YYMMDD} 주차는 학생 과제 #3(WOL 6번 슬롯) 없음. 실행 생략." 출력 후 종료
   - 있으면 → 아래 단계 진행
3. 있을 때 타입·시간·장면·학습 요점 WOL verbatim

## 🚫 할루시네이션 금지 / 공통 / 저작권
`/mid-student2` 와 동일.

## 저장 위치
베이스: `C:\Users\yoone\Dropbox\02.WatchTower\01.▣ 수원 연무 회중\01.주중집회\02.야외 봉사에 힘쓰십시오\01.학생 과제\YYMMDD_M월 D-D일\`
파일명: `학생 과제_{타입}_YYMMDD.docx` (mid-student2 와 동일 타입 매핑)

## 실행 단계 (4단 방어)

### 0. WOL 6번 슬롯 존재 확인 (선행 게이트)
WebFetch 로 주차 페이지 1회 조회. "학생 과제" 섹션 내 3건 모두 있는지 확인. 2건이면 종료 (원준님께 보고).

### 1. 주차 확정 + 폴더

### 2. 🤖 ① + ② — student-assignment-planner 1차
```
Agent(student-assignment-planner)
  프롬프트: "{YYMMDD} 학생 과제 #3 (WOL 6번 슬롯) 기획 1차 (4단 방어 ①).
  과제번호 4 고정, 타입 WOL 자동 파싱.

  선행 검증: WOL 6번 슬롯 실제 존재 재확인. 없으면 빈 outline 저장하고
  meta.yaml 에 `slot_absent: true` 표시.

  저장: `research-plan/student-assignment/{YYMMDD}_4_{타입}/`
  meta.yaml.assignment_number = 4. [mid-student2/3 과 동일 수집·지시서 구조]
  ⭐⭐ instructions_to_subresearchers 3개.
  ⚠ 할루시네이션 / 4단 방어."
```

### 2.5. 🤖 role-play-scenario-designer 호출
`slot_absent: true` 면 생략. 그렇지 않으면 mid-student2 §2.5 와 동일 — 과제번호 4 로 `research-plan/student-assignment/{YYMMDD}_4_{타입}/scenarios.yaml` 저장. `apply_explaining_beliefs(연설)` 일 때만 생략.

### 3. 🤖 ② — 3개 보조 병렬
`slot_absent: true` 면 생략. 그렇지 않으면 mid-student2 와 동일.

### 4. 🤖 ③ — Planner 재검수
`slot_absent` 인 경우 생략. 그렇지 않으면 mid-student2 와 동일.

### 5. 🤖 ① + ② — student-assignment-script
`slot_absent` 인 경우 생략. 그렇지 않으면:
저장 `research-plan/student-assignment/{YYMMDD}_4_{타입}/script.md`.

### 6. 🤖 ③ — Planner script 재검수
`slot_absent` 인 경우 생략.

### 7. docx 렌더
```bash
python content_student4_YYMMDD.py
```

### 8. 🤖 ④ — 최종 감사 3종
`slot_absent` 인 경우 생략. 그렇지 않으면 fact-checker + jw-style-checker + timing-auditor.

### 9. 확인 및 보고
- 슬롯 존재 여부 (있음/없음) 보고
- 있을 때: docx/PDF 경로·과제 타입·③ 통과·④ HIGH/MEDIUM/LOW
- 없을 때: "이번 주 학생 과제 #3 없음 — 생성 건너뜀" 명시

## 개정 이력
- 2026-04-24 v2 — 4단 방어 + 3개 보조 리서치 (조건부 실행 유지)
- 2026-04-23 v1 — 초안

---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/mid-student4` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `학생 과제_{타입}_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3`) 호출 시

일괄 스킬이 묶음 확인 단계에서 이미 yes/no 받았으므로 **자체 단정형 확인 묻지 않는다**. 일괄에서 받은 결정 그대로 실행:

- **skip 결정** → 호출 자체가 발생 안 함 (일괄이 이미 걸러냄)
- **신규 빌드** → 정상 진행 (이번 주에 슬롯 없으면 자체 자동 skip — 이건 본문 다른 정책)
- **`--from-batch=ver_up`** 컨텍스트 받으면 → `_verN_` (N = 디스크 최대 + 1) 자동 부여

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3 + `.claude/shared/output-naming-policy.md` §4·§4-bis.
