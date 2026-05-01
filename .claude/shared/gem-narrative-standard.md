# Gem 다각도·적용 4축 균형 표준 (영적 보물찾기 정본)

> **이 파일이 영적 보물찾기 자동화의 gem 미니 narrative 표준 정본이다.**
> spiritual-gems-script·spiritual-gems-planner·application-builder·gem-coordinator 모두 이 표준 따름.
> 작성: 2026-05-01 (Phase E v2) / 정책: validators.py + gem-coordinator 자동 검증

## 1. Gem 미니 narrative 표준

각 gem 의 `comment` list 는 다음 흐름을 따른다 (`comment-label-standard.md` 와 함께):

```
① 핵심 — 성구의 직접 의미 (1~2 문장)
② 적용 — 4축 중 ≥1 + 자기점검 질문 1개 권장
③ 배울점 — 다각도 표시 ≥2 각도 (어원·평행·고고·신약 성취·일상·교리)
```

### Comment 구조 (예시)

```python
"comment": [
    ["① 핵심 — ", "b"],
    ["성구의 직접 의미. 핵심 메시지 1~2 문장.", ""],
    ["\n② 적용 — ", "b"],
    ["[4축 중 1축] 적용 본문. ", ""],
    ["[자기점검 질문]", "yb"],
    ["\n③ 배울점 — ", "b"],
    ["히브리어 어근 「N」 의 의미는 ... 평행 성구로 창 N:N 이 ...", ""],
],
```

## 2. 다각도 — 6 각도 (각 gem ≥2 강제, 키워드 매칭으로 자동 검증)

각 gem 의 ③ 배울점에서 다음 6 각도 중 **최소 2 각도** 자연스러운 한국어 서술로 포함. **이모지·라벨 마커 불필요** — `validators.count_angles_per_gem` 가 키워드 매칭으로 자동 검증.

| 각도 | 검증 키워드 | 권장 자료 |
|---|---|---|
| 어원 | 히브리어, 그리스어, 어근, Strong, 동사 ~의 의미 | scripture-deep + 「통찰」 어휘 항목 |
| 평행 | 평행 성구, 상호 참조, 같은 어근 ~ 등장 | scripture-deep 상호 참조 + NWT 연구 노트 |
| 고고·역사 | 발굴, 유물, 비문, 오벨리스크, 라기스, 사해 사본, BC, 고고학 | 「통찰」 인명·지명 + illustration-finder 14축 |
| 신약 성취 | 1세기 성취, 예수께서 ~ 인용, 누가 N, 마 N, 사도행전 | scripture-deep + 「예-1」·「예-2」 |
| 일상 적용 | 일상, 가정·직장·회중·개인, 오늘 우리도, 매일 | application-builder + illustration-finder |
| 교리 깊이 | 「통」, 「파」, 「예-1」, 「하」 verbatim 인용 (1~2 문장) | publication-cross-ref |

**예외**: gem 의 verse 길이 < 30자 (예: "여호와는 나의 목자라") → 1 각도 허용. 단 전체 20 gem 중 1 각도 only 인 gem 수 ≤ 4건.

## 3. 적용 영역 — 참고용 분류 (강제 폐기, 2026-05-01)

영보 주제는 통독 범위에 따라 직장·가정·회중 적용 자연스러움이 다름. **4축 균형 강제 폐기** — 적용은 **자연스러움 우선**.

application-builder 가 산출 시 다음 4 영역을 **참고용으로** 분류 가능 (분포 표 첨부 권장, 강제 X):

| 영역 | 키워드 | 정의 |
|---|---|---|
| 가정 | 부부·자녀·가족·식사·자녀양육 | 가족 단위에서의 적용 |
| 직장/학교 | 동료·상사·과제·시험·일·생업 | 직업·교육 환경 |
| 회중/전도 | 형제·자매·집회·봉사·구역·관심자·전도인 | 회중 활동·야외 봉사 |
| 개인 영성 | 기도·연구·묵상·자기점검·인격 | 개인 영적 생활 |

**원칙**:
- 각 gem 의 ② 적용은 **그 성구에 가장 자연스러운 1~2 영역** 만 — 모든 축 강제 적용 X
- 통독 범위 주제에 따라 한쪽 영역 집중 OK (예: 사 60-61 메시아 사명 → 회중·전도 집중)
- application-builder 가 산출 시 분포 정보만 표시, 빌더 검증 X

## 4. 자기점검 질문 표준

20 gem 중 **≥10개** gem 에 자기점검 질문 1개 권장. 형식:

- 의문문 + 노랑 강조 (`"yb"`) — 청중이 묵상하도록
- "여러분도 …해 보신 적 있으십니까?" 류 상투 호명 금지 (intro-and-illustration-quality.md A-4-bis)
- 구체 행동·관계·결심에 초점

**좋은 예**:
- "이번 주 가족 학습에서 어떤 부드러움을 적용해 볼 수 있을까?"
- "한 가지 굳어진 마음을 어떻게 다시 진흙으로 만들겠는가?"

**나쁜 예**:
- ❌ "여러분도 그렇게 생각하시지요?" (상투 호명)
- ❌ "어떻게 생각하십니까?" (모호)

## 5. 출판물 verbatim 인용 표준

gem 깊이 단락 (③ 배울점) 에서 「통」·「파」·「예-1·2」·「하」 등 **verbatim 1~2 문장** 직접 인용 가능.

**규칙**:
- 본문 안 출처 호명 금지 — 예: ❌ "「파」 19.12 11면이 짚는 것처럼…"
- 출판물 verbatim 은 큰따옴표 + `"b"` 스타일
- 각주 윗첨자 (`"p"` 스타일) + references 섹션에 출처 명시 (호수·면·항)
- 가짜 docid 절대 금지 (validators.py `validate_docid_real` 자동 차단)

**예**:
```python
[" 「통」 자비 12항은 이렇게 말합니다 — \"", ""],
["회개하지 않아서 참으로 처벌을 받기에 마땅한 자들에게는 결코 처벌을 면제해 주지 않으신다", "b"],
[".\"", ""],
```

## 6. validators.py 자동 검증

`/Users/brandon/Claude/Projects/Congregation/_automation/validators.py` 가 본 표준 자동 차단:

| 검증 함수 | 본 표준 항목 | 위반 시 |
|---|---|---|
| `validate_label_format` | §1 라벨 표준 | ValueError raise |
| `count_angles_per_gem` (S3 신규) | §2 각 gem ≥2 각도 | ValueError raise |
| `validate_application_balance` (S3 신규) | §3 4축 균형 | ValueError raise |
| `count_self_check_questions` (S3 옵션) | §4 ≥10 자기점검 | warning (강제 아님) |
| `validate_docid_real` (S3 신규) | §5 가짜 docid | ValueError raise |

## 7. 정본 참조 — 다른 파일

| 파일 | 변경 |
|---|---|
| `comment-label-standard.md` | 본 표준 §1 참조 추가 |
| `dig-treasures/SKILL.md` | 본 표준 + gem-coordinator 단계 명시 |
| `spiritual-gems-script.md` | Read 의무 + 자체 검수에 §2·§3·§4 항목 추가 |
| `spiritual-gems-planner.md` | 동일 + ⑤ 재검수에 본 표준 점검 |
| `application-builder.md` | 영보용 4축 균형 산출 표준화 (§3) |

## 8. 변경 이력

- 2026-05-01: 초판 신설 (Phase E v2). 영보 자동화 v2 의 깊이·다양성·적용점 강화.
