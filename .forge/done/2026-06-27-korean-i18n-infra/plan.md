<!-- forge-slug: korean-i18n-infra -->
<!-- task: 1 -->
<!-- tdd: off -->
# 프로젝트 인프라 한글화 (1단계: skills·지침·도구 주석)

## Goal / Non-goals
- Goal: Claude가 도구로 읽고 동작에 사용하는 **인프라 파일**의 중국어 산문을 한글로 전환한다. 대상: `skills/*.md`(18개), `CLAUDE.md`, `ai_CLAUDE.md`, `README.md`, `docs/ROADMAP.md`, `tools/*.py`(주석·docstring). CLAUDE.md의 보고 언어 정책을 한국어로 뒤집는다(ADR-0001).
- Non-goals:
  - `reports/`(2,083개), `实盘记录/`, `筛选公司/`, 루트 낱개 리포트(`RKLB-investment-research.md`, `sailis-touzi-yanjiu-baogao.md`), `docs/대모델...md` 번역 — **별도 리포트 배치 작업**으로 분리(품질 확인 후 결정).
  - `data/`(CSV·JSON), `logs/` 번역 — 구조화 데이터/로그라 값을 바꾸면 `tools/*.py` 로직이 깨지므로 **완전 제외**.
  - `origin`(github.com/gyuha/ai-berkshire) **푸시** — 요청 시에만. 기본은 로컬 커밋까지.

## Source of truth
- Glossary terms: 4대가(워런 버핏/찰리 멍거/돤융핑/리루) + 핵심 투자 용어(가치투자·경제적 해자·안전마진·능력범위·내재가치·잉여현금흐름) in `.forge/CONTEXT.md` — 모든 파일이 동일 한국어 표기 준수.
- Related ADRs: `.forge/adr/0001-reports-in-korean.md` (보고 언어 정책 한국어 전환)
- Definition of Done: 경계 내 모든 인프라 파일에서 중국어 산문이 한글로 전환되고, **슬래시 커맨드명·코드 식별자·API 파라미터(Eastmoney 토큰)·숫자·종목코드·날짜·★ 기호·실제 예시 경로(`reports/腾讯/...`)는 불변**이며, CLAUDE.md 보고 정책이 한국어로 명시됨.

## 번역 규칙 (전 슬라이스 공통)
- 번역: 중국어 산문·제목·설명 → 한글. 4대가 이름·핵심 용어는 CONTEXT.md 표기 준수. 자리표시자 `{公司名}` → `{회사명}`.
- 불변: 슬래시 커맨드명(`/investment-team` 등), `tools/*.py` 코드·식별자·함수명·변수·API 파라미터(특히 Eastmoney 토큰 `D43BF722C8E33BDC906FB84D85E326E8`)·문자열 키, 숫자·종목코드(LEU/RKLB/0700.HK)·날짜·재무 수치, ★ 평점, CLAUDE.md 명명 규범의 실제 예시 경로.

## Work slices
- [ ] S1. `CLAUDE.md` 한글 번역 + 보고 언어 정책을 한국어로 전환(ADR-0001 반영) — 완료 기준: CLAUDE.md에 중국어 산문 잔존 0(예시 경로 제외), "报告语言" 정책이 "한국어"로 명시됨.
- [ ] S2. `skills/*.md` 18개 전부 한글 번역(커맨드명·코드블록·예시경로·★ 보존, CONTEXT.md 용어 준수) — 완료 기준: 18개 파일 중국어 산문 잔존 0, `grep -ro '/[a-z-]\+'` 슬래시 커맨드 토큰 수가 번역 전후 동일.
- [ ] S3. `README.md` 한글로 제자리 교체 — 완료 기준: README.md 중국어 산문 잔존 0, `README_EN.md`는 변경 없음(diff 비어 있음).
- [ ] S4. `ai_CLAUDE.md` + `docs/ROADMAP.md` 한글 번역 — 완료 기준: 두 파일 중국어 산문 잔존 0.
- [ ] S5. `tools/*.py` 주석·docstring만 한글 번역 — 완료 기준: 각 .py가 `python -m py_compile`로 구문 통과(코드 안 깨짐), Eastmoney 토큰 문자열·식별자 불변(diff에 코드 라인 변경 없음).
