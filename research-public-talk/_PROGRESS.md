# S-34 공개강연 골자 분할 작업 진행 상황

마지막 업데이트: 2026-04-22

## 목표
`S-34_KO_공개강연_골자_1-194.pdf` (388쪽) 를 강연 번호별 개별 PDF 194개로 분할.

## 현재 상태

### ✅ 완료
- **PDF 구조 분석 완료**: 2쪽 단위로 194개 chunk 구성됨.
  - chunk N = 강연 #N (N=2..194)
  - chunk 1 (1-2쪽) = 강연 #40 의 2026년 1월 신판 (중복)
  - chunk 40 (79-80쪽) = 강연 #40 원판
  - **강연 #1 은 PDF에 수록되어 있지 않음**
- **194개 PDF 분할 완료**: `S-34_split/` 폴더에 생성.
  - `_manifest.json` / `_manifest.txt` 포함.
- **구형 골자 페이지 OCR 완료**: 총 163개 garbled 페이지를 tesseract `-l kor` 로 OCR.
  - 결과물: `/tmp/ocr_out/page_NNN.txt` (WSL 임시, 재부팅 시 소실됨).
  - 번역문 검증으로 chunk 91/92/119/120/122/123/124 가 각각 강연 #91/92/119/120/122/123/124 임을 확인.
- **신형 (2026판) 페이지 제목 추출 성공**: 페이지 최상단 블록 (y≈48-64) 위치에서 제목을 직접 추출 가능.

### 🟡 진행 중 — 제목 품질 개선
- 현재 파일명에 제목이 없는 파일 약 96개 (구형 페이지 위주).
  - 예: `005번.pdf`, `014번.pdf`, `017번.pdf` ~ `036번.pdf` 다수
- **원인**: 구형 페이지는 커스텀 폰트 (CID) 로 인코딩되어 텍스트 추출 시 깨짐.
  OCR은 가능하지만, 제목 영역의 기울어진/굵은 글꼴이 tesseract로 잘 안 읽힘.
- **진행 중이던 접근**: 각 chunk 첫 쪽의 최상단 블록 bbox 를 600 DPI 로 재렌더링 → `tesseract --psm 7` 로 단일 줄 OCR.
  - 스크립트: `_scripts/render_title_strips.py`
  - 1차 시도 결과는 노이즈 많음 → 더 타이트한 크롭 필요.

### ⏳ 남은 작업
1. **제목 추출 개선**
   - 옵션 A: `render_title_strips.py` 로 재렌더링 + 타이트 크롭 + PSM 6/7 재시도.
   - 옵션 B: tesseract 대신 고품질 OCR (네이버 Clova OCR, Google Vision 등) 사용.
   - 옵션 C: wol.jw.org 에서 S-34 강연 1-194번 공식 제목 목록을 긁어와서 매칭.
   - 옵션 D: 사용자가 수작업으로 파일명 교정.
2. **정리**
   - `/tmp/ocr_out/` OCR 결과물을 저장소에 영구 저장할지 판단.
   - `C:\Users\yoone\tmp_*.py` 임시 스크립트 정리.

## 재개 방법

```bash
# 1. 현재 상태 점검
cd "/mnt/c/Users/yoone/Dropbox/congregation"
ls research-public-talk/S-34_split/ | wc -l   # 196 (194 PDF + 2 manifest) 기대

# 2. Python 환경 (Windows Python 3.10 사용 — PyMuPDF 1.27.2 설치됨)
powershell.exe -NoProfile -Command "& 'C:\Users\yoone\AppData\Local\Programs\Python\Python310\python.exe' 'C:\Users\yoone\Dropbox\congregation\research-public-talk\_scripts\split_pdf.py'"

# 3. OCR 환경 (WSL, 설치 완료)
tesseract --list-langs   # eng, kor, osd 출력되어야 함
```

## 주요 경로
- 원본 PDF: `research-public-talk/S-34_KO_공개강연_골자_1-194.pdf`
- 분할 출력: `research-public-talk/S-34_split/` (194 PDFs + manifest)
- 스크립트: `research-public-talk/_scripts/`
- Windows Python: `C:\Users\yoone\AppData\Local\Programs\Python\Python310\python.exe`
  - PyMuPDF 1.27.2.2, pypdf 6.10.2 설치됨
- WSL tesseract: `tesseract` (한국어팩 `kor` 설치됨)

## 핵심 발견
- **chunk → 강연번호 매핑은 깔끔함**: `chunk_idx` 가 `talk_num` 과 거의 그대로 일치 (chunk 1 = #40 신판 예외).
- **구형/신형 혼재**: 구형(2015년경) 쪽은 CID 폰트로 텍스트 추출 안 됨, 신형(2026.1.) 쪽은 정상 추출.
- **footer 마커로 번호 확정**: `S-34-KO No. N` (신형) / `No. N-KO` (구형) 패턴이 footer에 ASCII 로 박혀 있어 인코딩 상관없이 추출 가능.
