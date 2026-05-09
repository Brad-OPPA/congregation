# 위크보드 ↔ 스프레드시트 연결 구조

> **여호와의증인 수원 연무 회중 주간 보드** 운영 원리 정본
> *작성: 2026-05-09*

---

## 📌 한눈에 보기

| 항목 | 값 |
|---|---|
| **Production URL** | https://brandon-weekboard.vercel.app |
| **GitHub Repo** | `Brad-OPPA/weekboard` |
| **데이터 소스** | Google Sheets `16BK1pn7kofDu7nJywgA4IQvIxDEaeomTWMFfx7UN0oQ` |
| **Stack** | Next.js 16 (App Router) · React 19 · TypeScript |
| **호스팅** | Vercel (region: `icn1` 서울) |
| **갱신 주기** | 10초 ISR (시트 수정 후 최대 10초 내 반영) |

---

## 🌳 1. 시트 ↔ 코드 매핑 트리

탭 9가지가 각각 전용 렌더러에 1:1 매핑됩니다. 시트 탭 이름이 곧 디스패치 키입니다.

### 📅 주말집회 (디폴트 탭)
- **시트 컬럼**: `일자` · `회중` · `연사` · `공개강연 제목` · `공강 사회` · `파수대 낭독` · `마치는 기도` · `후대 집단`
- **렌더러**: `page.tsx::renderTab()` → `WeekendCardsClient`
- **카드 단위**: 한 행 = 한 카드
- **시트 색 활용**:
  - 공개강연 제목 셀 노란색 → `🟡 특별 카드` 표시
  - 후대 집단 셀 배경색 → 카드 우하단 색칩
- **자동 처리**: 월별 그룹핑 + 검색창 + 오늘 이전 자동 숨김

### 🎙 마이크임명
- **시트 구조**: R0 시트 제목 (한 셀) · R1 헤더 · R2~ 월별 데이터
- **컬럼**: 월 │ 주말집회(일) 2명 │ 주중집회(목) 2명
- **렌더러**: `renderMicCards()` → `MicCardsClient`
- **카드 단위**: 한 카드 = 1개월
- **자동**: 지난 월 자동 숨김

### 🧹 청소 집단
- **시트 구조**: R0 제목 · R1 헤더 · R2~ 월별 + 마지막 행 안내문구
- **컬럼**: 월 │ 주말 영의 열매 │ 주중 영의 열매
- **렌더러**: `renderCleaningCards()` (인라인)
- **색 매핑** (코드에 박음 — 시트엔 조건부 서식 없음):
  - 자제 `#F6B26B` · 온화 `#FCCD7E` · 기쁨 `#CEE1F3`
  - 평화 `#FFF1CC` · 믿음 `#D9EAD3` · 선함 `#D9D9D9`
- **자동**: 빈 카드는 별도 fold 섹션으로 분리

### 🅿️ 주차임명
- **시트 구조**: R0 제목 · R1 헤더 · R2~ 격주 데이터
- **컬럼**: 기간 (`04월19일~05월02일`) │ 주차담당 2명
- **렌더러**: `renderParkingCards()` → `ParkingCardsClient`
- **그룹핑**: 끝 월 기준 (격주가 두 달에 걸치면 끝 월에 포함)
- **자동**: 끝 날짜 < 오늘 자동 숨김

### 🚗 순방계획표 (순회감독자 방문 주간)
- **시트 구조**:
  - R0: 시트 제목 (B칸)
  - R1: 헤더 7컬럼
  - R2: C/D = 부부 형제·자매 이름
  - R3 B: 모임 장소·시간 (1주 통째 merge)
  - R3+: 요일 행 (`5월19일\n화요일`) + 슬롯 행들
- **컬럼**: 요일·인도자 │ 모임장소·시간 │ 오전 │ (merge) │ 오후 │ (merge) │ 집회 │ 식사
- **렌더러**: `renderSunbangCards()` (인라인, 가장 복잡)
- **동행자 로직**:
  - C/D = 오전 동행자 (남편 측 / 부인 측)
  - E/F = 오후 동행자
  - 일요일은 4×4 = 16셀, 평일은 4×2 = 8셀
- **인도자 분기**: A 셀 `오전:`/`오후:` 로 시작 → 인도자, 그 외 → 동행자

### 📚 공개강연 제목표
- **시트 구조**: R0 헤더만, R1+ 강연 데이터
- **컬럼**: A 골자번호 │ B 제목 │ C 2024 │ D 2025 │ E 2026 │ F 2027
- **렌더러**: `renderTalksCards()` → `TalksCardsClient`
- **카드 단위**: 강연 1개 = 1 카드
- **시트 글자색 활용**: B 보라색 = 30분 길이 골자
- **안내 문구**: A 숫자 아니고 B 비면 안내로 분리

### ⛪ 야외봉사 계획표
- **시트 구조**: R0 시트 제목·변경일 · R1 헤더 · R2+ 데이터
- **컬럼**: 요일 │ 봉사방법 │ 시간 │ 장소 │ 인도자
- **렌더러**: `renderYaeoiCards()` (인라인)
- **슬롯 분기 로직** (가장 정교):
  - A=요일 (월~일) → 새 카드 시작
  - A 비고 B/C/D 중 하나 → 같은 요일 새 슬롯
  - A·B·C·D 모두 비고 E만 → 직전 슬롯에 보조자 추가
  - A `*` 시작 → 안내 문구 (별도 영역)
- **시트 색 활용**: B 셀 배경색 → 슬롯 박스 색
  - 줌=회색, 호별=노랑, 전시대=파랑/연두
- **시간대 자동 분류**: 시간 텍스트 → 오전/오후/저녁 알약 색

### 👥 회중 직책표 (`회중 직책표` 또는 `회중종체 임명표`)
- **시트 구조** (3 섹션):
  - R0: 시트 제목 (A:F merge)
  - R1~R15: 직책 영역
    - A/B = 좌측 직책+담당자
    - C/D = 가운데 직책+담당자
    - E/F = 야외봉사 집단 (감독자/보조자 페어)
  - R19 `장로` 헤더 → R20~22 명단 (6×N 평면)
  - R24 `봉사의 종` 헤더 → R25 명단
- **렌더러**: `renderJcCards()` → `JcCardsClient`
- **카드 4유형**:
  - A. 직책 카드 (직책+담당자+보조자)
  - B. 야외봉사 집단 카드 (영의 열매 6색)
  - C. 장로 명단 카드
  - D. 봉사의 종 명단 카드
- **보조자 로직**: 라벨이 `보조자`/`안내인` 으로 시작하면 직전 직책에 합침

### 📋 그 외 모든 탭 → `renderGenericCards()` 폴백
- 한 행 = 한 카드
- 시트 헤더 = 라벨, 셀 값 = 본문
- 셀 색은 값 박스 배경에 그대로 적용

---

## ⚙️ 2. 작동 원리 (요청 → 렌더 흐름)

```
사용자 브라우저
    │ GET https://brandon-weekboard.vercel.app/?tab=주말집회
    ▼
Vercel Edge (icn1·서울)
    │
    ▼
┌─ Next.js Server Component (app/page.tsx::Page) ──────────┐
│                                                            │
│ ① ENV 체크                                                 │
│    └ GOOGLE_SHEETS_ID + (API_KEY 또는 SERVICE_ACCOUNT)    │
│                                                            │
│ ② lib/sheets.ts::fetchWorkbook()                          │
│    ├ 인증 분기:                                            │
│    │   • SERVICE_ACCOUNT_KEY → JWT → OAuth2 → Bearer     │
│    │   • 없으면 → API_KEY 폴백                             │
│    │                                                       │
│    ├ Google Sheets API v4 호출                            │
│    │   GET /spreadsheets/{ID}                             │
│    │       ?includeGridData=true                          │
│    │       &fields=sheets(properties, data,               │
│    │                      merges, conditionalFormats)     │
│    │                                                       │
│    └ Next.js ISR 캐시 (revalidate: 10초)                  │
│         · 첫 사용자 stale 즉시 반환                        │
│         · 백그라운드 새 fetch                              │
│                                                            │
│ ③ buildTab() — 시트 1탭 → SheetTab 객체                   │
│    · rowData → Cell[][] {v, bg, fg}                       │
│    · backgroundColor → bg (흰색은 undefined)              │
│    · foregroundColor → fg (디폴트 검정은 undefined)       │
│    · merges 의도적 비활성화 (같은 값 두 번 X)             │
│    · conditionalFormats 매칭 후 셀에 색 부여              │
│       (TEXT_CONTAINS '기쁨' → #CEE1F3 등)                │
│    · hiddenByUser → hiddenRows / hiddenCols Set           │
│                                                            │
│ ④ renderTab() 디스패치 — 탭 title 로 전용 렌더러 선택      │
│                                                            │
│ ⑤ 모든 탭 prerender → React tree 생성                     │
│                                                            │
│ ⑥ TabSwitcherClient 로 props 전달                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
    │
    ▼
사용자 브라우저
    │
    ▼
React Hydration → 탭 전환 client-side (네트워크 X, 즉시)
검색 입력 client-side (searchKey 미리 계산됨)
```

---

## 🎯 3. 핵심 정책

| 원칙 | 구현 방식 |
|---|---|
| **시트가 진실의 원천** | 색 · 텍스트 · 헤더 라벨 모두 시트 그대로. 자동 변환 X |
| **숨김 동기화** | 시트 hidden 행/열/탭 → 앱에서도 자동 안 보임 |
| **실시간(준)** | ISR 10초 — 시트 수정 후 최대 10초 내 카드 갱신 |
| **지난 일정 자동 숨김** | 오늘 이전 날짜 · 끝 월 < 현재월 → 카드 X |
| **탭 전환 즉시** | 모든 탭 server prerender → client 한꺼번에 전달 |
| **카드 디자인 = 탭 이름** | `renderTab()` title 매칭 디스패치 (8가지 + generic 폴백) |
| **인증 양쪽 호환** | 서비스 계정(JWT) 우선 → API key 폴백 → 비공개 시트 가능 |
| **합쳐진 셀 의도적 비활성화** | 베델연사 같은 값을 두 카드에 두 번 안 보여주기 위함 |

---

## 🔌 4. 환경 변수

| Key | 용도 | 필수? |
|---|---|---|
| `GOOGLE_SHEETS_ID` | 시트 ID (`16BK1pn7...`) | ✅ |
| `GOOGLE_SHEETS_API_KEY` | 폴백 인증 (공개 시트) | ⚠️ 둘 중 하나 |
| `GOOGLE_SERVICE_ACCOUNT_KEY` | 우선 인증 (비공개 시트, JSON 전체) | ⚠️ 둘 중 하나 |
| `GOOGLE_SHEETS_SHEET_NAME` | 디폴트 탭 (없으면 `주말집회`) | ❌ |

---

## 🧱 5. 코드 파일 구조

```
apps/weekboard/
├─ app/
│  ├─ page.tsx ............. Server Component (메인 디스패처, 1938줄)
│  ├─ layout.tsx ........... 전역 레이아웃
│  ├─ globals.css .......... 카드 디자인 (티켓 모양 등)
│  ├─ tab-switcher-client.tsx .. 클라이언트 탭 전환 (즉시)
│  ├─ weekend-cards-client.tsx . 주말집회 (월별 그룹 + 검색)
│  ├─ mic-cards-client.tsx ..... 마이크임명
│  ├─ parking-cards-client.tsx . 주차임명
│  ├─ talks-cards-client.tsx ... 공개강연 제목표
│  ├─ jc-cards-client.tsx ...... 회중 직책표
│  └─ highlight.tsx ............ 검색어 하이라이트
│
├─ lib/
│  └─ sheets.ts ............ Google Sheets API + 변환 (542줄)
│                            · 인증 (JWT/API key)
│                            · fetchTab / fetchWorkbook
│                            · buildTab (Cell 변환)
│                            · 조건부 서식 매칭
│                            · 합쳐진 셀 처리
│
├─ vercel.json ............. region icn1 설정
├─ .env.local .............. 로컬 환경변수 (커밋 금지)
└─ package.json ............ Next.js 16 + React 19
```

---

## 🆕 6. 새 탭 추가하는 법

1. **시트에 새 탭 만들기** (예: `목사봉헌계획`)
2. **`page.tsx::renderTab()` 의 if 분기 추가**:
   ```typescript
   if (tab.title === "목사봉헌계획") return renderMyCustomCards(tab);
   ```
3. **렌더 함수 작성** — 시트 좌표 → 카드 props 가공
4. **(선택) 클라이언트 컴포넌트 만들기** — 검색·필터 등 인터랙션 필요 시

> 그냥 두면 자동으로 `renderGenericCards()` 폴백 — 한 행 = 한 카드, 헤더가 라벨, 셀이 본문.

---

## 📐 7. 데이터 타입 (`lib/sheets.ts`)

```typescript
type Cell = {
  v: string;         // 표시할 문자열
  bg?: string;       // 배경색 hex (#F6B26B 등, 흰색은 undefined)
  fg?: string;       // 글자색 hex (디폴트 검정은 undefined)
};

type SheetTab = {
  id: number;                    // Google 내부 sheetId
  title: string;                 // 탭 이름
  index: number;                 // 시트 안 탭 순서
  rows: Cell[][];                // 헤더 + 데이터 (2차원)
  hiddenRows: Set<number>;       // 숨긴 행
  hiddenCols: Set<number>;       // 숨긴 열
};

type SheetWorkbook = {
  tabs: SheetTab[];              // 보이는 탭 목록 (hidden 탭 자동 제외)
};
```
