# 시드 이미지 다운로드 검증 로그 (Phase E)

## 본 주차 시드 이미지 — 260514

| 항목 | 값 |
|------|----|
| WOL 본 주차 삽화 페이지 | https://wol.jw.org/ko/wol/mp/r8/lp-ko/mwb26/2026/174 |
| 실제 이미지 URL | https://wol.jw.org/ko/wol/mp/r8/lp-ko/mwb26/2026/174 (mp 엔드포인트가 jpg 직접 응답) |
| 도메인 검증 | wol.jw.org ✅ (download_image.py 화이트리스트 통과) |
| 저장 경로 | /Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/260511-0517/260514_treasures.jpg |
| 파일 크기 | 162,866 bytes (≥1KB ✅) |
| MD5 | f1ff872280c660f4469fd182b0b9fb7b |
| 다운로드 시각 | 2026-04-29 |

## 직전 주차 비교 (재사용 검증)

| 항목 | 260507 (이전) | 260514 (현재) |
|------|-------------|--------------|
| 파일명 | 260507_treasures.jpg | 260514_treasures.jpg |
| MD5 | a7236d1126dcef5e44ba24df9632d8f1 | f1ff872280c660f4469fd182b0b9fb7b |
| 결과 | — | ✅ **다른 이미지** — 직전 주차 재사용 0건 |

## 캡션 (meta.yaml 기반)

> 낙원이 된 땅에서 사람들이 삶을 즐기고 있습니다. 저 멀리 상징적인 도시 새 예루살렘에서 강이 흘러나오고, 강 양쪽에는 나무들이 울창하게 자라고 있습니다.

## 활용 시점

요점 3 진입 직전 또는 결론 전 — "위에 있는 예루살렘" 의 시각적 형상화 (갈 4:26 + 사 60:19)

## 다운로드 명령 (재현 가능)

```bash
python3 "/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/_automation/download_image.py" \
  "https://wol.jw.org/ko/wol/mp/r8/lp-ko/mwb26/2026/174" \
  "/Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/260511-0517/260514_treasures.jpg"
```

## 헬퍼 stderr 출력

```
[download_image] OK 162,866 bytes → /Users/brandon/Library/CloudStorage/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/01.성경에 담긴 보물/01.10분 연설/260511-0517/260514_treasures.jpg
```

**Phase E 다운로드 결과: PASS** ✅
