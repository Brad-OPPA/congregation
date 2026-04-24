# 회중 작업 공간 (congregation)

이 폴더는 김원준 형제의 **여호와의증인 회중 활동** 관련 맥락입니다. 사용자는 한국어 답변을 선호합니다.

## 주요 활동
- 주중집회(목요일) 원고 준비
- 주말집회(일요일) 원고 준비
- 3주 선행 자료 생성 (이번 주 + 다음 주 + 다다음 주)

## 사용 스킬 (slash command)
| 스킬 | 용도 |
|---|---|
| `/mid-study1` | 주중 ①번 "성경에 담긴 보물" 10분 연설 원고 |
| `/mid-study2` | 주중 ②번 "영적 보물찾기" 6~10분 문답식 원고 |
| `/mid-study3` | 주중 ③번 "회중성서연구 사회" 30분 원고 |
| `/week-study2` | 주말 ②번 "파수대 연구 사회" 실전 진행 대본 |
| `/weekly` | 매주 월요일 — 한 주치 4개 자료 일괄 생성 + Gmail 발송 |

## 사용 에이전트 (subagent)
| 에이전트 | 용도 | 저장 폴더 |
|---|---|---|
| `wol-researcher` | 주차 프로그램·본문·성구·삽화 목록화 | — |
| `publication-cross-ref` | 주제 횡단 (파수대·깨어라·통찰·예수책·JW방송 등) | `research-topic/` |
| `scripture-deep` | 성구 심층 (번역·원어·배경·병행) | `research-bible/` |
| `illustration-finder` | 예화·비유·서론·결론 초안 | `research-illustration/` |
| `qa-designer` | 문답 블록 설계 (영적보물·CBS·파수대) | `research-qa/` |
| `application-builder` | 실생활 적용 카드 (가정·직장·회중·개인) | `research-application/` |
| `timing-auditor` | 원고 낭독 시간 측정·조정 제안 | `research-timing/` |
| `jw-style-checker` | 공식 용어·호칭·신세계역 표기 감수 | `research-style/` |
| `experience-collector` | 연감·파수대·JW방송 공식 경험담 수집 | `research-experience/` |
| `public-talk-builder` | 주말 ①번 공개 강연 30분 아웃라인·재료 | `research-public-talk/` |

## 데이터 출처
- 공식 자료: **wol.jw.org** (연구용 교재, 주간 파수대, 참조서 등)
- 참고서: 「파」·「익」·「통」·「예-1」·「훈」 책 등
- 원고는 wol.jw.org의 본문·성구·참조자료를 근거로 생성

## 환경
- Python 3.10+ **필수** (파이프라인 빌더가 요구)
- 관련 메모리: `project_meeting_pipelines.md` (mid-study1/2/3 + weekend-study2 경로 맵)
- 스킬 정의 위치: 전역 `C:\Users\yoone\.claude\skills\`

## 원칙
- 원고는 wol.jw.org 공식 내용만 근거. 추측·외부 해석 최소화.
- 성구 참조·교재 인용은 정확히.
- **작업 위임·병렬화 우선** — 3단계/3파일 이상은 서브 에이전트로 위임, 의존성 없는 작업은 한 메시지 안에서 병렬 호출. 메인 Claude 컨텍스트는 의사결정·통합·git 에 보존. 세부: 메모리 `feedback_delegate_to_subagents.md`.
- **상투적 청중 호명·수사 질문 금지** — "여러분도 …해 보신 적 있으십니까?" 류 9가지 표현 일체 사용 금지. 모든 script 에이전트 + jw-style-checker 가 차단. 세부: 메모리 `feedback_script_no_cliche.md` · 공유 파일 `intro-and-illustration-quality.md` §A-4-bis.
