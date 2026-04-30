# 보조 지시서 (3/5) — illustration-finder

> meta.yaml `instructions_to_subresearchers.illustration-finder` 의 확장.
> ⭐ Phase E 의무 — 시드 이미지 자동 다운로드 (silent skip 차단).

## 🟢 착수 전 리마인드

- [ ] 공유 파일 3종 Read · 차등 적용표 `mid-talk10` 행 숙지
- [ ] outline.md · meta.yaml Read
- [ ] 🟢 블록 복사·체크
- [ ] _selfcheck.md 에 🔴 블록 + 시드 이미지 다운로드 성공 판정 확약

## 1. ⭐ 시드 이미지 자동 다운로드 (Phase E)

### 1.1 사용 헬퍼

`/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/_automation/download_image.py`

### 1.2 절차

1. WOL 본 주차 정확 삽화 페이지 진입:
   `https://wol.jw.org/ko/wol/mp/r8/lp-ko/mwb26/2026/174`
2. 페이지에서 실제 이미지 src URL 추출 (mp 페이지가 jpg 직링크 아니면 WebFetch 후 `<img>` src 추출 → wol.jw.org / cms-imgp.jw-cdn.org / b.jw-cdn.org 도메인만 허용).
3. 다운로드:
   ```bash
   python3 "/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/_automation/download_image.py" \
     "<추출한 이미지 URL>" \
     "/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/260511-0517/260514_treasures.jpg"
   ```
4. 검증:
   - 파일 ≥ 1KB
   - 디렉터리 자동 생성 OK
   - 저장 경로 `_selfcheck.md` 에 절대 경로 + 바이트 기록

### 1.3 절대 금지

- **직전 주차 (260507) 이미지 재사용 금지** — 본 주차 mwb26/2026/174 강제
- 외부(비-wol/jw-cdn) 도메인 이미지 다운로드 금지 (헬퍼가 자동 차단)

## 2. 요점별 텍스트 예화 (이미지 임베드 아닌 본문 묘사용)

### 요점 1 "고대 예루살렘 상징" (2~3개)

- ★★★ #6 고고학: BC 539년 키루스 원통 (대영박물관 ME 90920) — 바빌로니아 포로 해방 칙령 비문. 사 44·45 의 키루스 예언 1차 성취. 이사야 60장 회복 약속 직전 단계.
- ★★ #7 지형: 폐허 → 재건된 예루살렘 (느헤미야 시대 성벽 복원, 케슬린 케년 발굴 결과).
- ★ #8 문헌: 요세푸스 「유대 고대사」 의 키루스 칙령 본문 보존.

### 요점 2 "부분 성취" (2~3개)

- ★★★ #6 고고학·#8 문헌: 마카베오·헤롯 시대 성벽·망루 — 재건 예루살렘이 "성문 늘 열림" 평화 도시 아니었음. 요세푸스 「유대 전쟁사」 증언.
- ★★ #11 시간·유한성: AD 70 두 번째 멸망 — 1차 성취 비영구.
- ★ #10 인생 의미: 지상 도시는 사 60장 빛을 다 못 담음.

### 요점 3 "위에 있는 예루살렘" (2~3개)

- ★★★ #2 우주 구조: 별빛 시간 지연 vs 사 60:19 시간 지연 없는 영원한 빛.
- ★★ #10 어머니·자녀 비유.
- ★ #13 어느 도시에 속해 있는가.

## 3. [추가 책무, 2026-04-25] 서론 이미지 후보

`research-illustration/260514/intro_image_candidates.json` 작성:

```json
[
  {
    "candidate": "A",
    "axis": "#6 고고학·#7 지형",
    "description": "폐허가 된 고대 예루살렘 발굴 사진 (외부 위키커먼즈 공개 도메인)",
    "image_url": "<wikicommons URL>",
    "license": "Public Domain / CC0",
    "religiosity_check": "no (세속 고고학 유적)",
    "use_point": "intro hook"
  },
  ...
]
```

판정: 종교성 5질문 ALL "no" — wol 외부 OK. "yes" 1개라도 → wol 전용.

## 4. 산출 파일 (research-illustration/260514/)

- `01_cyrus-cylinder.md` (키루스 원통 ★★★)
- `02_jerusalem-rebuild.md` (1차 성취 후 재건)
- `03_partial-fulfillment.md` (마카베오·헤롯·AD 70 ★★★)
- `04_starlight-time.md` (별빛 시간 지연 ★★★)
- `05_mother-symbol.md` (어머니 비유)
- `06_intro_image_candidates.json` (서론 시각 자료 후보)
- `260514_treasures.jpg` 다운로드 검증 로그 (`_image_log.md`)
- `_selfcheck.md` (🔴 블록 + 시드 이미지 PASS/FAIL 명시)

## 5. 피할 것

- 타 종교 도상 절대 금지 (서양 종교화·이콘·불화 등 — 위키커먼즈에 있어도 탈락)
- 상업 스톡 이미지
- 성적·폭력적·충격적 장면
- 출처 불명 전승·도시전설
- 진화론 긍정
- 정치·정당
- 최근 10년 JW 출판물 예화 직접 재사용 (변형·배경으로만)
- 직전 주차 이미지 (260507_treasures.jpg) 재사용

## 6. 상한

본문 임베드 시드 이미지 1장 (mwb26/2026/174) — Phase E 최소 1장 강제. 추가 이미지는 권장 안 함.

## 7. 연결 목표

각 예화·시각 자료가 어느 요점·어느 단락에 어떻게 연결될지 명시. 시드 이미지 활용 시점 = "요점 3 진입 직전 또는 결론 전".
