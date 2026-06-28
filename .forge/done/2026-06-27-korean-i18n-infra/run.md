# run.md — 프로젝트 인프라 한글화 (1단계)

slug: korean-i18n-infra · 실행일: 2026-06-27 · 워크플로우: wf_87dda8b9-e1d (30 에이전트, sonnet 병렬)

## 계획대로 된 것
- 대상 30개 파일 전부 번역 수행(에이전트 에러 0): `CLAUDE.md`, `ai_CLAUDE.md`, `README.md`, `docs/ROADMAP.md`, `skills/*.md` 18개, `tools/*.py` 8개.
- **보고 언어 정책 한국어로 전환(ADR-0001)**: CLAUDE.md "所有报告使用中文" → "모든 보고서는 **한국어**로 작성한다".
- 보존 규칙 준수(결정적 검증): `README_EN.md` diff 빔(불가침 ✓), tools 8개 전부 `python3 -m py_compile` 통과 ✓, Eastmoney 토큰 `D43BF...` 1건 그대로 ✓, 슬래시 커맨드 `/investment-team`(6) `/earnings-review`(3) 등 정상 ✓.
- 비목표 준수: `reports/`·`实盘记录/`·`筛选公司/`·루트 낱개 리포트·`data/`·`logs/` 미수정.
- 대부분 파일의 잔존 CJK는 허용 예외로 확인: 예시 경로(CLAUDE.md), 회사명+한글병기(README), 중국어 검색 키워드·플랫폼 고유명(private-company-research), 데이터 출처명(financial-data).

## 누락 → 실행 중 수정 완료 (UAT 후)
- **S2 `skills/wechat-article.md`**: 코드블록 안 프롬프트 템플릿(Author/Editor/Reader Agent)이 중국어로 남았던 결함. 원인 = "코드블록 보존" 규칙을 산문 템플릿에 과잉 적용. **UAT에서 사용자가 "한국어 출력 통일" 결정** → 템플릿 전체 한글화 + `纯中文表达`→"순수 한국어 표현"으로 출력 지시 전환. 재검증 CJK=0. (微信公众号 출력 언어 = ADR-0001 따라 한국어로 확정.)
- `management-deep-dive.md`: 보고서 구조 서수 `一二三四五六` → `1~6`로 정리(earnings-review와 일관).
- `CLAUDE.md`: 커밋 예시 메시지 `"添加xxx报告"` → `"xxx 보고서 추가"`(자체 규칙과 일관).

## 현장 관찰 (미수정, 경미)
- `financial-data.md`: 통화 단위 `元` 유지 — 단위 기호라 보존(위안 미표기), 추후 통일 여지.
- `CLAUDE.md`: /investment-team 파일 구조 예시 파일명(`01-商业模式分析-段永平视角.md` 등) 중국어 유지 — 예시 경로 보존 규칙 적용. 향후 한국어 리포트 산출물과 불일치 가능(별도 결정 여지).

## 의도된 범위 한계 (정상)
- `tools/*.py`: 딕셔너리 데이터 라벨(`"name":"英伟达"`)·print 문자열의 중국어는 S5 범위(주석/docstring만)대로 보존 → tools 콘솔 출력은 여전히 중국어. 별도 결정 필요 시 후속 작업.

## 검증 상태
- 결정적 교차 검증 + UAT 완료. wechat-article 출력 언어 결정 해소(한국어). 잔존 CJK는 전 파일 허용 예외(예시 경로·회사명 병기·검색 키워드·데이터 출처 고유명)로 감사 완료.
- verified: yes — 증거: 30개 파일 번역 / tools py_compile 8/8 통과 / README_EN diff 빔 / Eastmoney 토큰·슬래시 커맨드 보존 / wechat-article CJK→0.
