---
name: mid-student3
description: 주중집회 야외봉사 섹션 **학생 과제 #2 (WOL 5번 슬롯)** 원고 1건을 지정된 주차에 대해 생성한다. 인자 `now|next1|next2|next3`. **4단 방어 프로토콜(`.claude/shared/multi-layer-defense.md`)** 준수. WOL 과제 타입 자동 파싱. student-assignment-planner(과제번호 3) → 3개 보조 리서치(scripture-deep·experience-collector·application-builder) → Planner 재검수 → student-assignment-script → Planner 재검수 → docx → fact-checker·jw-style-checker·timing-auditor 최종 감수. 결과 `학생 과제_{타입}_YYMMDD.docx`. 트리거 "/mid-student3", "학생과제 2 만들어 줘".
---

## 🛡 품질 단조 증가 (필수, 2026-04-29 도입)

⑥ 단계는 **4종 병렬 감사** (fact-checker · jw-style-checker · timing-auditor · **quality-monotonic-checker**).

quality-monotonic-checker 가 직전 주차 동일 슬롯 docx 와 비교하여 **글자수 / 성구 인용 / 출판물「」/ 외부 14축 / 시간 마커 / 깊이 단락** 메트릭이 ≥ 95% (직전 평균) AND ≥ 절대 하한 (`shared/quality-monotonic-policy.md`) 인지 자동 검증.

FAIL 시 자동 재작성 무한 루프 (5회 한도). 사용자 검수 의존 0. **quality > timing** — timing 1800±60 → ±120초 완화.

세부: `.claude/shared/quality-monotonic-policy.md` 참조.

# mid-student3 — 야외봉사 학생 과제 #2 (WOL 5번 슬롯, 4단 방어)

> **출력 경로·파일명 정본**: `.claude/shared/output-naming-policy.md` (2026-04-25 통일).

**출력 형식:** docx (빌더 작성 후 PDF 자동 추가 예정)

## 이 스킬의 범위
- 학생 과제 3건 중 **두 번째** (WOL 5번 슬롯)
- 타입 WOL 자동 파싱 (apply_conversation_start / apply_follow_up / apply_bible_study / apply_explaining_beliefs)
- 구조는 `/mid-student2` 와 동일. **차이점: 과제번호 3, WOL 5번 슬롯**.

## 🛡 품질 원칙 — 4단 방어 프로토콜
`.claude/shared/multi-layer-defense.md` 준수. 실행 전 Read.

## 인자 규약
`now|next1|next2|next3`

## ⚠ WOL-first 수집
주차 인덱스 → "야외봉사 → **5번 슬롯**" href. 과제 타입·시간·장면·학습 요점 WOL verbatim.

## 🚫 할루시네이션 금지 / 공통 원칙 / 저작권
`/mid-student2` 와 동일.

## 저장 위치
베이스: `C:\Users\yoone\Dropbox\02.WatchTower\01.▣ 수원 연무 회중\01.주중집회\02.야외 봉사에 힘쓰십시오\01.학생 과제\YYMMDD_M월 D-D일\`
파일명: `학생 과제_{타입}_YYMMDD.docx` (mid-student2 와 동일 타입 매핑)

## 실행 단계 (4단 방어)

mid-student2 와 동일하되 아래만 다름:

### 2. 🤖 ① + ② — student-assignment-planner 1차
```
Agent(student-assignment-planner)
  프롬프트: "{YYMMDD} 학생 과제 #2 (WOL 5번 슬롯) 기획 1차 (4단 방어 ①).
  과제번호 3 고정, 타입 WOL 자동 파싱. [mid-student2 와 동일 수집·지시서 구조]
  저장: `research-plan/student-assignment/{YYMMDD}_3_{타입}/`
  meta.yaml.assignment_number = 3.
  ⭐⭐ instructions_to_subresearchers 3개(scripture-deep·experience-collector·application-builder).
  ⚠ 할루시네이션 / 4단 방어."
```

### 2.5. 🤖 role-play-scenario-designer 호출
mid-student2 §2.5 와 동일 — 과제번호 3 로 meta.yaml 경로 `research-plan/student-assignment/{YYMMDD}_3_{타입}/scenarios.yaml` 저장. `apply_explaining_beliefs(연설)` 일 때만 생략.

### 3. 🤖 ② — 3개 보조 병렬
mid-student2 와 동일 (scripture-deep·experience-collector·application-builder).
저장 폴더: research-bible/research-experience/research-application 각 {YYMMDD}/ + _selfcheck.md.

### 4. 🤖 ③ — student-assignment-planner 재검수
`_planner_review_research.md` (과제번호 3 기준).

### 5. 🤖 ① + ② — student-assignment-script
mid-student2 와 동일 포맷. 저장 `research-plan/student-assignment/{YYMMDD}_3_{타입}/script.md`.

### 6. 🤖 ③ — Planner script 재검수
`_planner_review_script.md`.

### 7. docx 렌더
```bash
python content_student3_YYMMDD.py
```

### 8. 🤖 ④ — 최종 감사 3종
fact-checker + jw-style-checker + timing-auditor (3~4분 목표).

### 9. 확인 및 보고
mid-student2 와 동일.

## 개정 이력
- 2026-04-24 v2 — 4단 방어 + 3개 보조 리서치
- 2026-04-23 v1 — 초안


---

## 산출물 존재 시 skip 정책 (필수)

### A) 단독 호출 (사용자가 `/mid-student3` 직접 입력) 시

진입 시 출력 폴더 확인:

- **없음** → 정상 진행
- **있음 + 사용자 무명시** → 단정형 확인 1회 ("이미 `학생 과제_{타입}_YYMMDD.docx` 가 있는데, 다시 만들까요? 스킵할까요?")
  - 답 없음 / "스킵" / "아니" → **skip**
  - "다시 만들어" / "버전 올려" → `_verN_` 신규 (N = 디스크 최대 + 1, 없으면 ver2)
- **있음 + 사용자가 "재생성·다시·버전 올려" 명시** → `_verN_` 신규 자동 (N 자동 증가)

### B) 일괄 스킬 (`midweek-now/next1/2/3`) 호출 시

일괄 스킬이 묶음 확인 단계에서 이미 yes/no 받았으므로 **자체 단정형 확인 묻지 않는다**. 일괄에서 받은 결정 그대로 실행:

- **skip 결정** → 호출 자체가 발생 안 함 (일괄이 이미 걸러냄)
- **신규 빌드** → 정상 진행
- **`--from-batch=ver_up`** 컨텍스트 받으면 → `_verN_` (N = 디스크 최대 + 1) 자동 부여

자세한 규칙: `.claude/shared/skip-existing-policy.md` §3 + `.claude/shared/output-naming-policy.md` §4·§4-bis.
