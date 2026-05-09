# 회중의 필요 — 출력 경로 정본 (2026-05-07 확정)

> 이 메모는 `output-naming-policy.md` §1 보강. 다음 회중의 필요 빌드 시 메인 Claude 가 임시 폴더 (research-plan) 에 머무르지 않고 **무조건** 아래 정본 경로로 docx + PDF 를 떨어뜨리도록 강제한다.

---

## 1. 정본 출력 경로 (디스크 실측 기준)

```
/Users/brandon/Dropbox/02.WatchTower/01.▣ 수원 연무 회중/01.주중집회/04.회중의 필요/{YYMMDD-MMDD}/
```

- 주차 폴더: 목요일 주중집회 + 일요일 주말집회 묶음. 예: 260507(목) → `260504-0510` (해당 주 일~토 묶음).
- 사용자가 미리 만들어두는 경우가 많음 — 빌더는 `os.makedirs(exist_ok=True)` 로 안전하게 진입.
- 정책 §1 표기는 "04.회중의 필요" 1단계지만 **실제 디스크는 `01.주중집회/04.회중의 필요/`** 2단계. 디스크가 진실.

## 2. 파일명 (정책 §2 + ver_N §4)

```
회중의 필요_{주제}_YYMMDD.docx        # 첫 빌드
회중의 필요_{주제}_YYMMDD_ver2_.docx  # 두 번째
회중의 필요_{주제}_YYMMDD_ver3_.docx  # 세 번째
...
회중의 필요_{주제}_YYMMDD_final.docx  # 사용자가 직접 마무리한 사본 (특수)
```

- ver_N 자동 증분 — 같은 폴더 내 같은 prefix 중 가장 큰 N + 1 (정책 §4).
- `_final` 접미사는 사용자 직접 손질의 의도 표시. 빌더가 자동 부여하지 않음.

## 3. sandbox 한계 우회

- ❌ `mcp__workspace__bash` 의 `~/Dropbox` 접근 불가 — sandbox 매핑 안 들어 있음.
- ✅ `mcp__Control_your_Mac__osascript` 의 `do shell script "cp ..."` 로 host shell 에서 직접 복사.
- ✅ 빌더는 sandbox 의 `/sessions/.../mnt/Congregation/` 로 출력 → osascript 로 host 의 Dropbox 정본 경로로 이동.
- ✅ Mac↔sandbox 동기화 매핑: `/Users/brandon/Claude/Projects/Congregation/` ↔ `/sessions/loving-bold-wright/mnt/Congregation/` (file_handling_rules) — research-plan 안 파일은 osascript 에서도 같은 경로로 보임.

## 4. 🚫 자동 빌드 한계 — Word 직접 작성만 정본 (2026-05-07 final2 사고 4회 후 확정)

**python-docx 자동 빌드 docx 는 Mac Word / LibreOffice 의 한글 폰트 매핑을 보장 못 한다.** 4회 시도 모두 □ 깨짐:

1. **ver6 (build_local_needs)** — 단순 SPEC 빌드. East Asian "맑은 고딕" 명시했지만 Mac Word 에서 □.
2. **final2 v1 (build_final2 v1)** — _final.docx 의 first run rPr 만 추출해 사용. paragraph pPr 손실 + 모든 run 에 노랑 sample 복제 (sample 자체가 노랑).
3. **final2 v3 (highlight 제거 보강)** — 노랑 OK, 그러나 폰트 매핑 여전히 깨짐.
4. **final2 v4 (paragraph deepcopy 빌더)** — paragraph 자체 deepcopy 했지만 LibreOffice PDF 변환 시 한글 layout 깨짐 (글자 단위 분리).

→ **결론: 회중 발송 정본 docx 는 사용자가 Word 에서 직접 작성한 것만 안전.**

### 정본 작성 흐름 (확정)
1. **자동 빌드 baseline** — `build_local_needs.py` 로 ver_N docx + PDF 생성. 사용자 검토용 baseline 자료. 회중 발송 X.
2. **사용자가 Word 에서 직접 작성** — baseline 참고하면서 새 docx 작성 → `_final.docx` 로 저장.
3. **사용자가 손질 결정 후** — 메인 Claude 는 변경사항을 **markdown 패치 형태** (`final_to_finalN_패치.md`) 로 정리해서 제공. 사용자가 Word 에서 직접 적용 → `_finalN.docx` 저장.
4. **PDF 변환** — Word 의 "PDF 로 내보내기" (Word 가 폰트 임베딩 정상 처리). LibreOffice `soffice --convert-to pdf` 도 사용자 docx 에는 정상.

### 🚫 메인 Claude 금지
- python-docx 로 생성한 docx 를 **회중 발송용 정본** 으로 Dropbox 정본 폴더에 두는 것
- python-docx 빌드 docx 를 사용자에게 "정본" 이라고 보고하는 것
- 사용자 손질본 (`_final.docx`) 을 자동 빌드로 "갱신" 하는 것 — 폰트 깨짐 보장 X

### ✅ 메인 Claude 권장
- 변경사항은 **markdown 패치** 로 정리 (`final_to_finalN_패치.md` 형태)
- baseline docx 는 `_verN_` 으로만 보존, 정본 폴더에 _final 또는 _finalN 은 사용자 작성본만
- 사용자가 PDF 도 Word 로 직접 내보내도록 안내

## 4-bis. 🔍 자동 변환물 시각 검증 의무 (Phase F-bis, 2026-05-07)

**메인 Claude 는 자동 변환·생성한 파일을 정본 폴더에 저장하기 전에 본인이 직접 시각 검증한다.** 사용자가 깨짐을 매번 발견하게 두지 않는다.

### 사고 사례 (2026-05-07 pptx → PNG)
- sandbox LibreOffice (`/usr/bin/soffice`) 가 pptx 의 한글 폰트를 못 찾아서 PNG 출력에 한글이 □ 로 깨짐 → 메인이 검증 안 하고 정본 폴더에 저장 → 사용자가 매번 발견. 사용자 "맨날 내가 다 봐줘야 하나" 지적.

### ✅ 의무 절차
1. **변환은 host 측에서**: sandbox 변환 (`mcp__workspace__bash` 의 `soffice`) 은 한글 폰트 누락 위험. **반드시 `osascript do shell script "/Applications/LibreOffice.app/Contents/MacOS/soffice ..."`** 로 host Mac 의 LibreOffice 사용. 사용자 Mac 의 한글 폰트 정상 매핑됨.
2. **PNG 변환**: host 측 `pdftoppm` (보통 `/opt/homebrew/bin/pdftoppm` 또는 시스템 PATH) 사용.
3. **본인 시각 확인**: file tool `Read` 로 PNG 직접 확인. 한글이 □ 로 보이면 깨짐.
4. **깨짐 발견 시**: 정본 폴더 저장 절대 금지. 사용자에게 솔직히 보고 + 다른 변환 경로 제안.
5. **정상 확인된 것만 저장**: Dropbox 정본 폴더에 osascript cp.

### 적용 범위
- pptx → PNG / pptx → PDF
- docx → PDF
- 그 외 모든 자동 변환물 (영상, 이미지 후처리 등)

### 호출 예시
```python
# host LibreOffice 변환
do shell script "
SOFFICE='/Applications/LibreOffice.app/Contents/MacOS/soffice'
\"$SOFFICE\" --headless --convert-to pdf --outdir /tmp /path/to/file.pptx
/opt/homebrew/bin/pdftoppm -r 200 -png /tmp/file.pdf /tmp/slide
"
# 시각 검증
Read("/tmp/slide-1.png")
# 정상이면 정본 폴더 cp
```

## 5. 다음 회중의 필요 빌드 체크리스트

```
[ ] 1. Dropbox 정본 폴더 존재 확인 (osascript ls)
[ ] 2. 기존 ver_N 최대값 확인 → N+1 결정
[ ] 3. SPEC 파일 작성/수정 → /sessions/.../mnt/Congregation/_automation/content_local_needs_{YYMMDD}_v?.py
[ ] 4. build_local_needs.py 실행 → /sessions/.../mnt/Congregation/research-plan/local-needs/{date_topic}/ 에 docx 임시 출력
[ ] 5. auto_convert_to_pdf 호출 → 동행 PDF 생성
[ ] 6. osascript cp 두 번 → Dropbox 정본 폴더에 ver_(N+1) 부여하여 이동
[ ] 7. 사용자에게 Dropbox 절대 경로 + computer:// 링크 보고
[ ] 8. 사용자가 마무리해서 _final.docx 보내면 PDF 짝지어 동행 복사
```

**원칙: 임시 (`research-plan`) 출력은 빌드 직후 1회용. 사용자 보고 시점에는 무조건 Dropbox 정본 경로.**

---

## 변경 이력

- 2026-05-07: 작성 (메인 Claude 가 ver6 임시 폴더 누락 + 폰트 깨짐 사고 후 학습. 사용자 "또 같은 이야기를 또 하게 할까?" 지적).
- 2026-05-07 (보강): final2 자동 빌드 4회 모두 □ 깨짐 사고 → §4 강화. python-docx 자동 빌드 docx = baseline 자료, 회중 발송 정본 = 사용자 Word 직접 작성. 변경사항은 markdown 패치 형태로 전달.
