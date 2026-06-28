<!-- forge-slug: readme-kr-demo -->
# RUN — 한국 기업 버전 데모 README 작성

## 계획 대비 실제 (divergence)

### 계획대로 된 것
- **S1 데이터수집**: 한국 상장사 8곳(카카오·쿠팡·네이버·크래프톤·하이트진로·SOOP·하이브·토스) 팩트 데이터를 8개 병렬 subagent로 수집 완료 (collected 8/8).
- **S2 작성**: `README_KR_demo.md`(634행) 생성. 매핑 전면 적용(쿠팡·카카오·토스·하이브·네이버·하이트진로·SOOP·크래프톤), 상단 데모 안내, 트랙레코드·중국계좌 스크린샷·reports/ 링크 제거, 평점·권고·가격에 "형식 예시" 표기 21건, 4대가 유지, 의도치 않은 한자 잔존 0.
- **S3 검증**: 산출물 `README_KR_demo.md` 자체는 모든 항목 통과.

### 중대한 divergence (HIGH)
- **워크플로우 작성 agent가 Non-goal을 위반**: `README_KR_demo.md`만 신규 생성해야 했는데, **원본 `README.md`를 제자리(in-place)에서 덮어써 누더기로 만듦**(631줄, 한글화+부분 번역 혼재, 제거 대상·중국명 잔존). plan의 Non-goal "원본 README.md 일절 변경 안 함" 및 DoD "원본 README.md git diff 무변경" 정면 위반.
- **위험 가중**: 세션 시작 시 `README.md`는 이미 미커밋 한글화 작업물(632행, `M` 상태)이었음 → `git checkout`으로 복원했다면 그 미커밋 작업이 소실될 뻔함.

### 현장 조치
- 워크플로우가 덮어쓴 누더기 `README.md`를 scratchpad에 백업(`README.md.workflow-clobbered.bak`).
- 메인 세션이 대화 첫머리에 Read한 632행 원본 내용으로 `README.md`를 **Write 복원**(`git checkout` 대신 — 미커밋 한글화 보존). 끝 빈 줄 1개까지 맞춰 세션 시작 상태와 일치.
- 복원 후 재검증: `README.md` 한글화판 복원 확인(첫 줄 "한국어", 트랙레코드·중국명 병기 정상 존재), `README_KR_demo.md` 정상.

### 교훈 (retro 후보)
- **파일 신규 생성을 지시한 워크플로우 agent가 기존 파일을 덮어쓸 수 있음.** 프롬프트에 "기존 README.md는 Read 전용, 절대 수정 금지"를 더 강하게 못 박거나, 워크플로우 마지막에 `git diff README.md`가 비었는지 검사하는 가드를 내장하고 실패 시 자동 복원해야 함.
- fg-run의 검증 phase(plan cross-verify)가 이 부작용을 정확히 잡아낸 것은 정상 작동 — 검증 단계의 가치를 입증.
