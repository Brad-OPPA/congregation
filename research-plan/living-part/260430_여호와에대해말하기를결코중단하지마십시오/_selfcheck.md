# 셀프체크 — living-part-planner + living-part-script (260430 생활 파트)

조사일: 2026-04-24
파트: 여호와에 대해 말하기를 결코 중단하지 마십시오
subtype: living_video

---

## planner 종료 체크리스트

- [x] 주차·파트 제목·시간·subtype 확정
  - 주차: 2026-04-27 / 집회: 2026-04-30 / 시간: 15분 / subtype: living_video
- [x] subtype 별 §2~ 블록 구조 준수
  - §2 비디오 정보 / §3 도입 / §4 재생 지시 / §5 토의 질문 2개 / §6 마무리
- [x] 핵심 성구 낭독 지시
  - 질문 1 후 전 11:6 낭독 / 질문 2 후 요1 5:3 낭독 (verbatim 포함)
- [x] (living_video) 영상 정보 4요소
  - 제목: 여호와는 "멀리 떨어져 계시지 않습니다"
  - 재생시간: 369.792초 (약 6분 10초) — CDN API 직접 확인
  - URL: pub-jwb-101 track 7 KO / CDN 링크 포함
  - 주제: 커피숍 전도 장면 — 거절 후 마음이 바뀐 여성 드라마
- [x] (living_video) 토의 질문 2개 (비디오 후)
  - 질문 1: wol verbatim 기반 / 질문 2: planner 설계 (요1 5:3 연결)
- [x] §종합 지시 블록 완비 (§10)
- [x] 2파일 한 폴더 저장
  - outline.md / meta.yaml — 동일 폴더 확인
- [x] 특수 주간 플래그 처리 — 모두 false
- [x] chair-script-builder·living-part-script·local-needs-planner·cbs-planner 건드리지 않음

---

## script 종료 체크리스트

| # | 항목 | 결과 | 비고 |
| --- | --- | --- | --- |
| 1 | planner 2파일(outline.md + meta.yaml) Read 완료 | PASS | |
| 2 | `part_type` = `living_part` 확인 | PASS | local_needs·cbs 아님 |
| 3 | subtype = `living_video` → C형 블록 구조 준수 | PASS | 블록 1~6 |
| 4 | 한 문장 60음절 이내 | PASS | 전체 문장 점검 완료 |
| 5 | 성구 verbatim (전 11:6 · 요1 5:3) | PASS | outline §10 원문 그대로 |
| 6 | read_aloud: false 성구 (딤전 1:13 · 눅 6:45) 낭독 마커 없음 | PASS | 보강 멘트 내용 반영만 |
| 7 | 청중 대기 마커만 사용 (가상 답변 없음) | PASS | `[청중 대기 — 약 50초]` ×2 |
| 8 | 인터뷰이 완성 대사 0건 | PASS | interviewee_label: null |
| 9 | 영상 재생 지시 블록 포함 + 영상 내용 재서술 없음 | PASS | [영상 재생] 마커 + "영상에서도 보셨듯이" 한 마디만 |
| 10 | 자기 소개·사회자 섹션 소개 0건 | PASS | |
| 11 | 금지 표현 ("시작하기 전에" / "우선" / "오늘 제가 여러분께") 0건 | PASS | |
| 12 | 시간 목표 15분 ±15초 | PASS | 서두1:00 + 요점1:30 + 영상6:10 + Q1 3:00 + Q2 2:50 + 마무리0:30 = 15:00 |
| 13 | 특수 주간 플래그 전부 false 확인 | PASS | circuit_overseer·convention·memorial 모두 false |
| 14 | script.md 저장 완료 | PASS | 동일 폴더 내 |
| 15 | 다른 에이전트 파일(outline.md · meta.yaml) 수정 없음 | PASS | |

---

## 시간 상세

| 구간 | 예상 시간 | 누적 |
| --- | --- | --- |
| [블록 1] 서두 | 1분 00초 | 1:00 |
| [블록 2] 교재 4요점 + 영상 소개 | 1분 30초 | 2:30 |
| [블록 3] 영상 재생 | 6분 10초 | 8:40 |
| [블록 4] 토의 질문 1 | 3분 00초 | 11:40 |
| [블록 5] 토의 질문 2 | 2분 50초 | 14:30 |
| [블록 6] 마무리 | 0분 30초 | 15:00 |

목표 15분 — 편차 0초 (허용 ±15초 이내)

---

## 경고 및 주의 사항

1. **영상 스트리밍 URL 확인 필요**
   - `https://www.jw.org/ko/라이브러리/동영상/#ko/mediaitems/VODOurActivities/pub-jwb-101_7_VIDEO`
   - 사회자가 집회 전 JW 라이브러리 앱에서 직접 재생 확인 권장.

2. **청중 발언 시간 변동**
   - 청중 발언 길이에 따라 Q1·Q2 블록이 ±30초 내외로 변동될 수 있음.
   - 마무리 블록 길이로 조정 가능.

3. **담당자 자격**
   - S-38 24항 기준 동영상 단순 재생 파트는 사회자 직접 진행 가능 (chair_allowed).

4. **성구 낭독 배분**
   - 전 11:6 · 요1 5:3: 낭독 (read_aloud: true)
   - 딤전 1:13 · 눅 6:45: 보강 멘트 언급만 (read_aloud: false)

---

## PASS/FAIL 판정

| 항목 | 결과 |
| --- | --- |
| planner 판별 정확 | PASS |
| subtype 판별 정확 | PASS |
| 영상 제목 확인 | PASS |
| 영상 재생시간 수치 확인 (CDN) | PASS |
| 영상 URL 재생 가능 여부 | 요주의 (사회자 직접 확인 필요) |
| 성구 verbatim 2개 낭독 포함 | PASS |
| 토의 질문 구조 2개 | PASS |
| 시간 배분 합계 15분 | PASS (15:00 정확) |
| script.md 저장 | PASS |
| 특수 주간 플래그 | PASS (모두 false) |

**종합 판정: PASS (영상 URL 사전 확인 조건부)**
