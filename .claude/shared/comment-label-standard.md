# Comment 라벨·강조 표준 (회중 자료 docx 시각화 정본)

> **이 파일이 회중 자동화 전체의 라벨·강조 표준 정본이다.**
> 모든 script 에이전트·빌더가 이 표준을 따른다.
> 작성: 2026-05-01 / 정책: Phase E (validators.py `validate_label_format` 자동 적용)

## 1. 영적 보물찾기 (`spiritual_gems`)

각 gem 의 `comment` list 는 **반드시** 다음 3개 라벨을 별도 run 으로 포함:

```python
"comment": [
    ["① 핵심 — ", "b"],
    ["...핵심 본문...", ""],
    ["\n② 적용 — ", "b"],
    ["...적용 본문...", ""],
    ["\n③ 배울점 — ", "b"],
    ["...배울점 본문...", ""],
]
```

**규칙**:
- 번호 ①·②·③ 필수 (한자/영문 번호 X)
- 라벨 용어: **핵심 / 적용 / 배울점** ("표제·배우는 점·핵심내용" 등 변형 금지)
- "—" (em dash) 뒤 공백 1개
- ②·③ 라벨 앞에 `\n` 줄바꿈 필수 (① 은 줄바꿈 없음)
- 스타일 `"b"` (볼드) 필수 — 라벨에 노랑 강조 `"yb"` 사용 금지
- **별도의 list 항목**으로 분리 (인라인 평문 안에 박지 말 것)

**금지 패턴**:
- ❌ `["표제 — 여자야, ...", "b"]` (다른 용어)
- ❌ `["배우는 점", "b"]` (변형)
- ❌ `["핵심 — 시온의 의가...", ""]` (평문 인라인 + 번호 없음 + 볼드 X)

## 2. 노랑 하이라이트 (`"yb"`) 사용 가이드

`"yb"` = 노랑 + 볼드. `build_treasures_talk.add_run` 에서 처리.

**원칙** (`_automation/CLAUDE.md §7`):
> "단락당 1-2개 핵심 구문만 (남발하면 시인성 저하)"

**적용 규칙**:
- 각 항(① 핵심 / ② 적용 / ③ 배울점) 당 본문에서 1-2개 핵심 구문만
- 라벨 자체에 `"yb"` 사용 금지 — 라벨은 항상 `"b"`
- 성구 verbatim·출판물 verbatim 인용 안에 들어간 텍스트 미터치 (이미 별도 처리)
- 어원 표기 (히브리어 `「헤세드」`·`「요체르」` 등) 는 `"b"` (노랑 X)
- 깊이 단락 (어근 짝·고고학 결합) 은 2-3개까지 허용

**예시**:
```python
["① 핵심 — ", "b"],
["예언자에게 ", ""],
["죄를 명확히 알리라는 책무", "yb"],   # 핵심 구문 1개
["가 부과됩니다.", ""],
```

## 3. 다른 슬롯 라벨 표준 (점진 적용)

| 슬롯 | 라벨 표준 | 비고 |
|---|---|---|
| 영적 보물찾기 | ① 핵심 / ② 적용 / ③ 배울점 (위 §1) | validators.py 자동 검증 (Phase E) |
| 10분 연설 (`treasures_talk`) | (별도 — 6단계 narrative: 흥미·성구유도·낭독·설명·예·교훈) | 향후 표준 명시 예정 |
| CBS (`cbs`) | 5블록 + Q&A. 각 문답: 공식 질문 verbatim → [낭독자 ...] 마커 → 청중 대기 | cbs-script.md 참조 |
| 파수대 사회 (`watchtower`) | 17블록 + 시간 마커 (2'·5'·8'·... 3분 단위) | watchtower-study-planner 참조 |
| 5분 연설 (`mid_talk5`) | 서론(30초) → 요점 1~2개(각 1.5~2분) → 결론(30초) | student-talk-script 참조 |
| 사회자 대본 (`chair`) | 9 고정 시간 마커 (By H:MM pm) | chair-script-builder 참조 |

## 4. validators.py 자동 검증

`/Users/brandon/Claude/Projects/Congregation/_automation/validators.py` 의 `validate_label_format(spec, slot_name)` 가 빌더 build 직전 자동 호출.

영보 (`slot_name="spiritual_gems"`) 의 경우:
- 모든 gem 의 comment 에서 "① 핵심 —" / "② 적용 —" / "③ 배울점 —" 라벨이 `"b"` 스타일로 존재하는지 확인
- 누락 시 `ValueError` raise → docx 미생성

## 5. 정본 참조 — 다른 파일

| 파일 | 변경 |
|---|---|
| `dig-treasures/SKILL.md` | 본 파일 참조로 라벨·강조 표준 명시 |
| `.claude/agents/spiritual-gems-script.md` | "라벨 표준 Read 의무" 명시 |
| `.claude/agents/spiritual-gems-planner.md` | 동일 |
| `_automation/validators.py` | `validate_label_format` 가 본 표준에 따라 검증 |

## 6. 변경 이력

- 2026-05-01: 초판 신설. 260507/260514/260521 3 파일 라벨 불일치 사고 후 표준 정립.
