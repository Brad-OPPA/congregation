# jw-style-checker v2 — CBS 260514 재감사

**대상**: `~/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/05.회중 성서 연구/260511-0517/회중 성서 연구_훈84-85장_260514.docx` (재빌드본)
**일자**: 2026-05-02
**모드**: 메인 Claude 직접 검증 (Task 도구 미가용 환경) + WOL 직접 fetch
**v1 결과**: HIGH 1건 (라벨) + MED 1건 ("진리의 은혜")
**v2 결과**: **HIGH 0건 + MED 0건 → PASS**

## 라벨 정상화

`(필수 질문 — 마지막 질문)` (em dash U+2014) 정본으로 정정.

| 항목 | 결과 |
|---|---|
| em dash 라벨 출현 | **2회** (장 2개 → 기대 2회 ✅) |
| underscore 잔존 | **0회** ✅ |
| 정정 위치 | `_automation/build_cbs_v10.py` L487 (`render_section_tag` 호출 인자) |

원인: 빌더의 `render_section_tag()` 호출 인자에 직접 박힌 라벨 문자열에서 em dash 가 underscore 로 잘못 작성돼 있었음.

## 금칙어 스캔 (banned-vocabulary.md 정본 기준)

| 어휘 | 출현 | 결과 |
|---|---|---|
| 예배 | 0회 | PASS |
| 복음을 전 | 0회 | PASS |
| 간증 | 0회 | PASS |
| 신앙 | 0회 | PASS |

## "진리의 은혜" WOL 검증

WOL 정확 매칭 검색: `https://wol.jw.org/ko/wol/s/r8/lp-ko?q=%22%EC%A7%84%EB%A6%AC%EC%9D%98+%EC%9D%80%ED%98%9C%22`

**결과: 검색 결과 없음 (0건)** — JW 공식 출판물에서 사용되지 않는 표현으로 확인됨. MED 위반.

### 정정

- 블록 8 (85장 illustration short_application): "자기가 받은 진리의 은혜를 한 줄로 표현" → "자기가 받게 된 진리의 좋은 영향을 한 줄로 표현"
- 블록 9 (85장 Q3 field_service): "자신이 받은 진리의 은혜를 단순하고 솔직한 말로 분명히 증언" → "자신이 진리에서 받게 된 좋은 영향을 단순하고 솔직한 말로 분명히 증언"

재빌드 후 docx 검증: "진리의 은혜" 0건, "진리의 좋은 영향" 1건 + "진리에서 받게 된 좋은 영향" 1건 = 2건 정정 완료.

## 종합

- HIGH: **0건**
- MED: **0건**
- LOW: 0건

**jw-style-checker v2 종합: PASS**
