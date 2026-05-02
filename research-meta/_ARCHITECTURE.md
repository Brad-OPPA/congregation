# 회중 자동화 — 진짜 설계도면 (2026-05-03 정본)

> 이 문서는 매 세션 새로 시작하는 Claude 가 즉시 architecture 회복할 수 있게 하는 정본.
> 사용자 (원준님) 가 2주에 걸쳐 가르친 핵심을 영구 저장.

## 핵심 원칙 (사용자 가르침 — 절대 변경 X)

1. **재료 (ingredients) = MUST**. 양념 (리서치) 은 그 다음. 요리 (docx) 는 마지막.
2. **재료 못 확보 = 즉시 정지**. agent 호출 0, 토큰 0, 시간 0. 빌드 시작 자체 X.
3. **agent·메인 Claude 신뢰 X**. **코드만 신뢰**. 약속 텍스트가 아니라 실행 가능한 검증만.
4. **사용자 검수 부담 0** 이 진짜 자동화의 정의. 매주 docx 열어 catch 하면 자동화 X.
5. **mwb anchor 가 truth source**. agent 가 자기식으로 부풀리면 안 됨. anchor 따라 자연스럽게 풀어내기만.

---

## Layer 0 — 재료 수집 (코드만, 신뢰 가능)

### 0-A: 이미지 카탈로그 (`slot_image_inventory.py`)
- mwb·lfb 페이지 직접 fetch (urllib + curl fallback)
- `<img src>` 만 (data-img-small-src = thumbnail 무시)
- 슬롯별 분류 (h2/h3 헤더 위치 기반)

### 0-B: 본문 카탈로그 (`slot_content_inventory.py`)
- 본문 단락 (pid·verbatim)
- 동영상 cue (`[동영상 「...」]`)
- 성구 ref (책·장:절)
- 출판물 인용 (「파」, 「깨」, 「통」)
- 이미지 (재포함, alt 텍스트 매핑)

### 0-C: 향후 추가 — NWT 성구 본문 카탈로그
- 성구 ref + URL → 신세계역 verbatim cache
- 빌드 시 spec 의 성구 인용 ↔ NWT cache 비교 (Layer 5)

---

## Layer 1 — Preflight (빌드 시작 차단 가능, HARD GATE 1)

`preflight.py {slot} {week} [args]`

각 슬롯별 필수 재료 확보 가능 여부 검증:

| 슬롯 | 검증 내용 |
|---|---|
| `mid-talk10` | mwb 주차 article fetch + 본문 anchor + 이미지 ≥ 1장 |
| `dig-treasures` | mwb fetch + "2. 영적 보물 찾기" 슬롯 anchor + 1-3장 범위 |
| `cbs` | lfb chapter docids 모두 fetch + 각 페이지 figure ≥ 1 |
| `week-study` | wt article fetch + 17블록 + 5소제목 + 복습 질문 |
| `mid-student1~4` | mwb fetch + 학생 과제 슬롯 + 낭독 범위 |
| `mid-talk5` | mwb fetch + 5분 연설 슬롯 |
| `living-part` | mwb fetch + 그리스도인 생활 슬롯 + subtype 자동 분류 |
| `local-needs` | (장로의회 주제 입력 필요 — 스킵) |
| `chair` | 모든 슬롯 합산 |
| `publictalk` | 골자 폴더 PDF + .jpg/.png ls |

**FAIL → 즉시 정지**. agent 호출 안 함. 빌드 시작 안 함. 사용자에게 명시적 보고:
> "재료 미확보. 다음 중 하나: (a) WOL 미배포, (b) docid 변경, (c) URL 패턴 변경."

**PASS → 카탈로그 저장**: `research-illustration/{week}/_preflight_{slot}.json` + `_content_inventory.json`

---

## Layer 2 — Agent (카탈로그 의무 사용)

agent 호출 시 다음을 prompt 에 의무 박힘:

1. **카탈로그 input 의무**: `_preflight_*.json` + `_content_inventory.json` Read 필수
2. **카탈로그 외 자료 사용 금지** (free internet 에서 임의 인용 X)
3. **mwb anchor 흐름 따르기**:
   - 동영상 cue 있으면 verbatim 인용
   - 핵심 성구 ref 정확 (NWT verbatim)
   - 표지 삽화 / 본문 삽화 위치 정확
4. **양념 (research) 은 anchor 보강만** — 부풀림 X

### 슬롯별 정형 구조 (사용자 가르침)

#### 10분 연설 (성경에 담긴 보물 ①)
```
1. 서론: 동영상 + 주제 소개 (왜 이 책·이 사람을 살펴보는지)
2. 요점 1: mwb 본문 첫 핵심 + 인용 성구 + 양념 (배경 검색)
3. 요점 2: 두 번째 핵심 + 성구 + 양념
4. (요점 3): 세 번째 핵심 (있으면) + 성구 + 양념
5. 자문해 볼 점: "내가 / 우리는 어떻게?" — 앞 요점 다시 떠올리며 적용·교훈
6. 삽화 보강: mwb 표지/본문 삽화로 메시지 시각화 + 추가 설명
7. 결론: 행동 촉구
```

#### 영적 보물 찾기 (성경에 담긴 보물 ②, 10분 문답)
```
- 주간 성서 읽기 범위 (예: 예레미야 1-3장) 안 추가 영적 보물
- mwb 의 공식 질문 + 자유로운 청중 답변 유도
- 각 보물 = 핵심·적용·배울점 3항
```

#### 성경 낭독 (성경에 담긴 보물 ③, 4분)
```
- 주간 범위 중 핵심 부분 (mwb 명시)
- 낭독자 verbatim NWT
- 강세·쉼·억양 7축 평가 포인트
```

#### CBS (회중성서연구 사회, 30분)
```
- 주차의 lfb 챕터 (보통 2개) 본문 진행
- 각 챕터: 시간 마커 + 낭독 + 핵심 성구 + (필수) 연구 질문 + 답변 + 사회자 보강
- 낭독자 별도 (사회자 ≠ 낭독자)
- 「훈」 책 (lfb 1102016XXX) 본문 + 「예수」 책 (jy 1102014XXX) 횡단 인용
- 시간 마커 8개: 4'·7'·10'·15'·18'·21'·23'·29'
```

#### 파수대 사회 (60분)
```
- wt article 17 블록
- 각 블록: 시간 마커 + 공식 질문 + 본문 요약 + 깊이 해설 + 성구 낭독 + 다음 블록 안내
- 외부 14축 (자연·역사·과학·고고학) 3-5회 결합
```

#### 5분 연설 (apply_talk, 야외봉사 ④)
```
- mwb 5분 연설 골자
- 회중 전체 대상 격려·권면 톤
- 남학생만 (S-38-KO 11항)
```

#### 그리스도인 생활 파트 (5종 자동 분기)
```
subtype: living_talk / living_discussion / living_video / living_interview / living_qna
mwb 안 분기 자동 파싱 → subtype별 보조 리서치
```

#### 회중의 필요 (장로의회 주제 입력 필요)
```
- 5단 흐름 (도입·요점 1·2·3·결론, 10분)
- pptx 6장 (어르신 친화 폰트)
- 능동·격려 톤
- 표준: research-meta/local-needs-ver4-standard.md
```

#### 사회자 대본 (전체 1시간 45분)
```
- 입장 → 시작 노래 + 기도 → 모든 파트 사회 → 마침 노래 + 기도
- 9개 고정 시간 마커
- 각 학생/연사 칭찬·조언 멘트 포함
```

#### 공개 강연 (30분 서술형)
```
- 사용자 골자 폴더의 PDF + 이미지 사용
- mwb anchor X (강연 소속 다름)
- R-Golja-Fixed: 골자 폴더의 .jpg/.png 만 사용
```

---

## Layer 3 — 빌더 (HARD GATE 2, 빌드 차단)

`validators.verify_spec_against_inventory_auto()` — 이미 작동 (2026-05-03):

- spec 의 모든 image_path → 카탈로그 src ID 매칭
- spec ⊆ catalog 검증
- 매칭 실패 = HARD FAIL (placeholder, 다른 페이지 이미지, fake docid 차단)

10개 빌더 모두 hook 적용됨. md 기반 빌더 (publictalk, chair) 도 `enforce_md_seed_images` hook.

---

## Layer 4 — Anchor 검증 (HARD GATE 3, 빌드 후 차단 가능)

`validators.verify_docx_contains_anchors()` — 이미 작동 (2026-05-03):

- docx 본문에 동영상 cue · 성구 ref · 출판물 cue 모두 등장 검증
- 누락 = HARD FAIL

**TODO**: 모든 빌더의 build 함수 끝부분에 hook 추가. 현재는 manual verify 만.

---

## Layer 5 — NWT verbatim 검증 (TODO, HARD GATE 4)

- 성구 인용 본문 ↔ NWT cache 글자 단위 비교
- 정규화 (smart quote, 공백) 후 fuzzy match
- 불일치 = HARD FAIL

이게 추가되면 "눅 22:31, 32 verbatim 미일치" 같은 인시던트 자동 차단.

---

## 신뢰 모델 (사용자 명시)

| 주체 | 신뢰 | 책무 |
|---|---|---|
| **사용자 (원준님)** | — | 검수 거의 0 (예외만). 명시 정정 X (시스템이 알아서). |
| **메인 Claude** | X | 오케스트레이터. 콘텐츠 직접 수정 X (Phase E). |
| **Agent (32개)** | X | 카탈로그 의무 사용. spec 작성 후 자체 PASS 보고 못 함. |
| **코드 (Layer 0/1/3/4/5)** | ✅ **유일 신뢰** | 모든 검증 게이트. agent 가 우회 불가. |

---

## 매주 작업 흐름 (목표 상태)

```
사용자: /weekly 또는 /midweek-* 한 줄
   ↓
[Layer 0/1] preflight.py — 모든 슬롯 재료 확보 검증
   ├─ FAIL: 즉시 보고. 사용자 입력 (예: docid 정정) 받기.
   └─ PASS: _preflight_*.json + _content_inventory.json 저장
   ↓
[Layer 2] agent 호출 (각 슬롯) — 카탈로그 의무 input
   ├─ 5 보조 리서치 병렬 (양념)
   ├─ Planner (mwb anchor + 사용자 정형 구조 + 양념)
   └─ Script (자연스러운 발표문)
   ↓
[Layer 3/4/5] 빌더 — spec 자동 검증
   ├─ image_path ↔ 카탈로그 매칭 (Layer 3)
   ├─ docx 본문 ↔ anchor 매칭 (Layer 4)
   └─ NWT verbatim (Layer 5, TODO)
   FAIL 시 docx 생성 0 + 명시적 메시지
   ↓
[빌드 통과] docx + PDF 자동 생성
   ↓
사용자 검수: 5분 (smoke check), 내용 정정 0
```

---

## 인시던트 로그 (학습 자료)

### 2026-05-03 — 10분 연설 260604 placeholder 가짜 PASS
- agent 가 mwb 6월호 표지 다운로드 실패 → 직전 주차 (260528) 영적 낙원 placeholder 복사
- silent PASS 보고 → quality·timing·factcheck·jw-style 모두 통과 (가짜)
- **사용자가 docx 검수 catch** → 신뢰 깨짐
- **fix**: Layer 3 (image md5 ≠ prev) + Layer 4 (동영상 cue 등장 검증) 추가

### 2026-05-03 — CBS 260521 thumbnail 임베드
- agent 가 lfb 87장 페이지의 `<img src=853 data-img-small-src=852>` 한 태그를 두 이미지로 오인
- meta.yaml 에 두 URL 모두 등록 → 빌더가 852 (60x60 thumbnail) 임베드
- **fix**: validators.py size < 50KB hard gate + illustration-finder.md E-3-ter 정책

### 2026-05-03 — 10분 연설 260604 동영상 cue 누락
- mwb 본문에 `[동영상 「예레미야 소개」 시청]` cue 명시
- agent 가 자기식 서론 작성 → 동영상 cue 자체 누락
- **fix**: Layer 4 (verify_docx_contains_anchors) 추가, 사용자 제시 anchor 직접 박힘

---

## 완성도 체크 (2026-05-03 갱신 — 5-Layer 신뢰 모델 완료)

| Layer | 상태 |
|---|---|
| 0-A 이미지 카탈로그 | ✅ 작동 (`slot_image_inventory.py`) |
| 0-B 본문 카탈로그 | ✅ 작동 (`slot_content_inventory.py`) |
| 0-C NWT verbatim 캐시 | ✅ 작동 (`nwt_cache.py` — `_automation/nwt_cache/{book:02d}_{chap:03d}.json`) |
| 1 Preflight | ✅ 작동 (`preflight.py` — 9 슬롯: mid-talk10/cbs/week-study/dig-treasures/mid-student1~4/mid-talk5/living-part/local-needs/chair) |
| 2 Agent prompt 의무 | ✅ 갱신 (4 agent: treasures-talk-script / spiritual-gems-script / cbs-script / watchtower-study-planner — Layer 0/1/5 의무 Read 박힘) |
| 3 spec ↔ catalog | ✅ 작동 (`verify_spec_against_inventory_auto`, 10 빌더 hook) |
| 4 docx ↔ anchor | ✅ 작동 (`verify_docx_against_inventory_auto`, 4 빌더 build 끝 자동 호출. silent swallow 제거 — SeedImageHardFail propagate) |
| 5 NWT verbatim | ✅ 작동 (`verify_spec_scriptures` + `nwt_cache.compare_verbatim`. 4 빌더 hook. `+`·`*`·smart-quote·공백 정규화 후 비교. `NWT_VERIFY=0` 환경변수 opt-out) |

### Layer 5 audit 결과 (2026-05-03 — 기존 spec 검증)

기존 빌드 spec 에 NWT verbatim audit 실행:
- **CBS 260521**: 4 인용 중 2건 진짜 미일치 발견
  - 요한복음 11:25 — claimed "예수께서 그에게 말씀하셨다" vs NWT "예수께서 말씀하셨다" (1단어 추가)
  - 요한복음 13:34, 35 — 마침따옴표 누락 (`...` vs `...."` 종결)
- **영보 260521·260604, 10분 260521·260604**: 미일치 0건 (또는 ref+verbatim 쌍 자체 없음)

CBS 260521 spec 직접 정정은 메인 Claude 정책상 금지 (Phase E §main-claude-edit-policy.md). 다음 CBS 빌드부터 Layer 5 자동 차단 → script agent 재작성.

---

## 다음 세션 진입 시

새 Claude session 이면 즉시 이 파일을 Read 해서 architecture 회복:

```
다음 세션 첫 명령:
> Read /Users/brandon/Claude/Projects/Congregation/research-meta/_ARCHITECTURE.md
```

이게 사용자 검수 부담 0 으로 가는 진짜 자동화의 설계도면.

**원준님이 2주 동안 가르친 모든 것이 여기 있습니다.**
