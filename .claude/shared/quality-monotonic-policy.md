# 품질 단조 증가 정책 (Quality Monotonic Policy)

> **절대 원칙**: 새 빌드의 품질은 **직전 주차 동일 슬롯 대비 같거나 더 풍부**해야 한다. 어느 정량 메트릭이라도 -5% 초과 감소하면 자동 FAIL → 재작성 강제.

도입: 2026-04-29 (사용자 검수 의존 0 자동화 보장)
적용: ⑥ 단계 4번째 감수자 `quality-monotonic-checker` 가 매 빌드 자동 점검.

---

## 1. 슬롯별 절대 하한선 (Phase E 갱신, 2026-04-29 — image 추가 + 출판 완화)

어떤 빌드도 **절대로 이 수치 이하로 떨어질 수 없음**. 직전 주차 95% 보다 작더라도 이 하한 우선.

> **Phase E 조정**: 출판물 절대 하한 → fact-checker docid 검증과 충돌 회피 위해 완화. 직전 95% 비교는 그대로 (단조 증가 핵심). 출판 위반 등급 → MED 강등 (HIGH X).
>
> **Phase E 추가 — 이미지 카운트 (`H_images` 축)**: 10분 연설·CBS 는 시드 이미지 ≥ 1 강제. 빌더 silent skip 차단 — 다운로드 의무는 illustration-finder.

| 슬롯 | 글자수 | 성구 | 출판「」 | 외부 14축 | 시간 마커 | **이미지** | 구조 |
|---|---|---|---|---|---|---|---|
| 10분 연설 | ≥ 3,200 | ≥ 4 | ≥ 3 | ≥ 1 | 6 | **≥ 1** | 6단계 narrative (흥미·성구유도·낭독·설명·예·교훈) |
| 영적 보물 | ≥ 7,500 | ≥ 50 | ≥ 10 | ≥ 2 | (N·A) | 0 | 20성구 × 3항 (핵심·적용·배울점) |
| 회중 성서 | ≥ 6,500 | ≥ 4 | ≥ 3 | ≥ 1 | 11 | **≥ 1** | 5블록 + Q&A |
| 파수대 사회 | ≥ 18,000 | ≥ 35 | ≥ 10 | ≥ 3 | 15 | 0 | 17블록 + 깊이 해설 |
| 5분 연설 | ≥ 1,400 | ≥ 2 | ≥ 1 | ≥ 1 | 5 | 0 | 2요점 narrative |
| 사회자 대본 | ≥ 4,500 | ≥ 8 | ≥ 2 | (N·A) | 9 | 0 | 9고정 마커 |
| 그리스도인 생활 | ≥ 1,800 | ≥ 2 | ≥ 2 | ≥ 1 | 3 | 0 | subtype별 |
| 회중의 필요 | ≥ 2,000 | ≥ 4 | ≥ 2 | (N·A) | 5 | 0 | 5단 흐름 |
| 공개 강연 | ≥ 12,000 | ≥ 30 | ≥ 8 | ≥ 3 | 8 | 0 | 30분 서술형 |
| 학생 과제 (낭독) | ≥ 1,200 | ≥ 1 | 0 | (N·A) | 2 | 0 | 본문 verbatim + 평가 7축 |
| 학생 과제 (시연) | ≥ 1,500 | ≥ 2 | ≥ 1 | (N·A) | 4 | 0 | 학생·상대자 alternating |

**근거**: 각 슬롯의 직전 3주 docx 의 평균 95% (또는 정책 명시 요구). 시간 마커는 표준 카운트.

---

## 2. 단조 증가 규칙 (PASS 조건)

매 빌드는 다음 **모두** 만족해야 통과:

```
조건 ①  절대 하한선 ≥ 위 표 (어떤 빌드도 이하 X)
조건 ②  직전 주차 동일 슬롯 대비 모든 메트릭 ≥ 95%
        (글자·성구·출판·외부 14축)
조건 ③  6단 방어 ⑥ 통과 (HIGH 0, fact·jw-style·timing·quality 4종)
```

→ 한 항목이라도 FAIL 시 **자동 재작성 무한 루프** (5회 한도, 그래도 실패 시 BLOCKING).

---

## 3. quality-monotonic-checker 점검 7축

⑥ 단계의 4번째 감수자가 다음 7축 자동 측정:

| 축 | 점검 내용 | 위반 등급 |
|---|---|---|
| A. 글자수 | ≥ 직전 95% AND ≥ 절대 하한 | A FAIL → HIGH |
| B. 성구 인용 수 | ≥ 직전 95% AND ≥ 하한 | B FAIL → HIGH |
| C. 출판물「」 인용 수 | ≥ 직전 95% AND ≥ 하한 | C FAIL → HIGH |
| D. 외부 14축 결합 (어원·고고학·과학·역사·천문) | ≥ 직전 카운트 AND ≥ 정책 하한 | D FAIL → HIGH |
| E. 시간 마커 정합성 | 슬롯별 표준 마커 수 ±1 | E FAIL → MED |
| F. 슬롯 구조 (6단계·20×3·17블록 등) | 100% 부합 | F FAIL → HIGH |
| G. 깊이 단락 (어원·고고학·과학) | 직전 주차 동등 카운트 | G FAIL → MED |

**판정**:
- A·B·C·D·F 중 하나라도 FAIL → **NO-GO + 재작성 강제** + 부족 메트릭 보강 지시
- E·G FAIL → MED 경고 (재작성 권장이지만 게이트 통과)
- 모두 PASS → GO

---

## 4. timing vs quality 우선순위

- **quality > timing** (정책 강제)
- timing-auditor ±60초 → **±120초** 로 완화
- 깊이 단락 보존이 timing 보다 우선
- 사회자 실전 발화 ±10% 변동 흡수

---

## 5. 강제 재작성 무한 루프

```
⑥ 4 게이트 병렬 감사
  ↓
quality-monotonic-checker FAIL?
  ↓ Yes
script 재작성 (정확한 부족 메트릭 + 보강 지시 전달)
  ↓
content_*.py 자동 재변환 + 빌더 재실행 + ⑥ 재감사
  ↓
quality-monotonic-checker 재판정
  ↓ FAIL?
재작성 횟수 < 5? → 다시 시도
재작성 횟수 ≥ 5? → BLOCKING (사용자 보고 + 안전장치)
```

---

## 6. 베이스라인 자동 갱신 (장기 단조 증가)

매 빌드 PASS 시 — 그 빌드의 메트릭이 **새 베이스라인** 이 됨. 메모리 시스템에 자동 누적:
- `~/.claude/projects/-Users-brandon/memory/project_quality_baseline.md`
- 슬롯별 최근 PASS 빌드 메트릭 평균
- 다음 빌드는 이 새 베이스라인 95% 비교

→ 슬롯이 실제로 개선되는 만큼 베이스라인도 함께 올라감. "만들수록 업그레이드" 정확히 구현.

---

## 7. 사용자 개입 정도

| 시나리오 | 개입 |
|---|---|
| 정상 빌드 (quality PASS) | **0** |
| 1회 재작성으로 PASS | 0 |
| 5회 재작성으로 PASS | 0 |
| 5회 시도해도 FAIL | **1회** (BLOCKING 알림 + 사용자 결정) |

---

## 8. Python 헬퍼

`02.WatchTower/01.▣ 수원 연무 회중/_automation/quality_check.py` 가 정량 측정 + 비교 함수 제공:

```python
from quality_check import measure_docx, compare_quality, SLOT_FLOOR

new_metrics  = measure_docx("path/to/new.docx")
prev_metrics = [measure_docx(p) for p in prev_paths]
verdict = compare_quality(new_metrics, prev_metrics, SLOT_FLOOR['watchtower'])
# verdict = {"axis_A": "PASS", "axis_B": "FAIL", ..., "rewrite_required": bool}
```

quality-monotonic-checker 에이전트는 이 헬퍼를 호출.

---

## 9. 적용 단계 (4 phases)

| Phase | 영역 | 상태 |
|---|---|---|
| A | 정책 + 헬퍼 + 새 에이전트 정착 (이 파일 포함) | 진행 중 |
| B | 정기 4 슬롯 (10분·영보·CBS·파수대) 정책 적용 | 대기 |
| C | 부정기 + 학생 + 특수 빌더 적용 | 대기 |
| D | 오케스트레이터 + 메모리 베이스라인 + Stop hook | 대기 |
