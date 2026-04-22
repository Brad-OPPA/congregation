# S-34 공개강연 골자 분할 작업 진행 상황

마지막 업데이트: 2026-04-22

## 목표
`S-34_KO_공개강연_골자_1-194.pdf` (388쪽) 중 **30분 신판 골자만** 추출·정리.
(45분 구판은 공개 강연 시간이 30분으로 개편되면서 더 이상 사용하지 않음 → 폐기.)

## 현재 상태

### ✅ 완료
- **PDF 구조 분석**: 2쪽 단위 194개 chunk. chunk N = 강연 #N (N=2..194), chunk 1 = 강연 #40 의 2026년 1월 신판 (중복).
- **194개 PDF 분할**: `S-34_split/` 폴더에 생성 (`_manifest.json` / `.txt`).
- **신판/구판 자동 분류**: footer 마커로 구분.
  - 신형(30분): `S-34-KO No. N` 패턴 — 78개
  - 구형(45분): `No. N-KO` 패턴 — 111개
  - 미검출(footer 도 CID 깨짐, OCR 로 구형 확인): 5개 (119/120/122/123/124)
- **구판 116개 격리**: `S-34_split/_archive_old45/` 로 이동 (물리 삭제 대신 격리 — 필요 시 폴더째 rm).
- **신판 60개 제목 확정·리네임**: PDF 1페이지 상단 12% 를 고해상도(DPI 3.5) 렌더링 → composite 이미지(1800px) 8장 → Claude vision 으로 제목 직독 → `NNN번_제목.pdf` 리네임.
  - 확정 제목: `research-public-talk/S-34_new30_titles.json`
  - 원본 이미지(임시): `C:\tmp\composite_titles_v2\` (재부팅 시 소실)

### 🎯 결과
- `S-34_split/` 최종 상태: **신판 78개 PDF 전부 제목 포함**, 제목 누락 0.
- `S-34_split/_archive_old45/`: 구판 116개 완전 삭제 완료 (2026-04-22).
- 참고 파일:
  - `S-34_titles.json` — wol.jw.org 색인 목록(구판 기준, 참고용). 신판 제목은 다름.
  - `S-34_new30_titles.json` — **신판(30분) 60개 확정 제목**. 파일명 교정에 사용.
  - `S-34_titles_sources.md` — 수집 과정 기록.
  - `S-34_illustrations.json` — **신판 78개 시각 자료 동반 여부**. 본문 "시각 자료" 단어 + `[시각 자료 N]` 태그 자동 검색.

### 🖼 시각 자료 판정 결과 (78개 중)
- **시각 자료 있음**: 69개 (유의사항 "제공된 시각 자료" 문구 + 본문 `[시각 자료 N]` 태그 중 하나 이상 검출)
- **시각 자료 없음**: 9개 — `026, 038, 047, 050, 055, 056, 098, 153, 176`

### ✅ 정리 완료
- `C:\Users\yoone\tmp_*.py` 임시 스크립트 전부 정리.
- `C:\tmp\composite_*`, `/mnt/c/tmp/s34_*` 등 작업용 임시 파일 정리.

## 주요 경로
- 원본 PDF: `research-public-talk/S-34_KO_공개강연_골자_1-194.pdf`
- 분할 출력 (최종): `research-public-talk/S-34_split/` — 78 PDFs + manifest
- 격리(구판): `research-public-talk/S-34_split/_archive_old45/` — 116 PDFs
- 스크립트: `research-public-talk/_scripts/`
- 제목 JSON: `research-public-talk/S-34_new30_titles.json`
- Windows Python: `C:\Users\yoone\AppData\Local\Programs\Python\Python310\python.exe` (PyMuPDF 1.27.2.2)

## 핵심 발견
- **30분 신판 ≠ wol 색인 제목**: wol.jw.org 의 S-34 색인 페이지(1200274680)는 구판 기준. 기존 제목이 있던 98개와 wol 제목 대조 시 22%는 완전 다른 제목. 신판은 반드시 PDF 실물에서 제목을 읽어야 함.
- **footer 마커가 신/구 구분의 결정적 단서**: CID 폰트로 본문이 깨져도 footer 의 `S-34-KO No. N` / `No. N-KO` 는 ASCII 로 박혀 있어 추출 가능. 예외는 119/120/122/123/124 다섯 개.
- **용어 표기**: 2026년 현재 JW 공식 번역은 "하느님". wol 색인은 구판 용어("하나님")를 보존하고 있으므로 신판과 혼용 금지.

## 재개 방법
```bash
cd "/mnt/c/Users/yoone/Dropbox/congregation"
ls research-public-talk/S-34_split/ | grep -v _archive | wc -l   # 80 (78 PDF + 2 manifest) 기대
ls research-public-talk/S-34_split/_archive_old45/ | wc -l        # 116 기대
```
