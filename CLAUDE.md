# AI Berkshire — 프로젝트 지침

## 프로젝트 개요

Claude Code 기반 가치투자 리서치 Skill 모음. 4대 거장 프레임워크: 워런 버핏, 찰리 멍거, 돤융핑, 리루.
GitHub: xbtlin/ai-berkshire

## 프로젝트 구조

```
skills/          — 투자 리서치 Skill 정의（.md），~/.claude/commands/ 에 복사하여 사용
tools/           — 보조 도구（financial_rigor.py 정밀 계산）
reports/         — 투자 리서치 보고서 출력
assets/          — 이미지 등 정적 자산
```

## 보고서 디렉터리 구조

모든 보고서는 **회사명** 폴더를 만들어, 해당 회사 관련 보고서를 모두 그 폴더 안에 넣는다:

```
reports/
├── AI产业研究/              — AI산업 체인 전체 리서치（상단 고정）
│   ├── AI五层蛋糕-产业全景研究-20260605.md
│   └── AI五层蛋糕-公众号-20260605.md
├── 腾讯/                    — 텐센트 전체 리서치 보고서
│   ├── 腾讯-research-20260408.md
│   ├── 腾讯-earnings-2025Q4.md
│   ├── 腾讯-management-20260409.md
│   └── 腾讯-thesis.md
├── 拼多多/                  — 핀둬둬 전체 리서치 보고서
├── 泡泡玛特/                — 팝마트 전체 리서치 보고서
├── 核电-industry-20260409.md — 산업 보고서는 루트 디렉터리에 배치
├── AI算力-funnel-20260509.md  — 퍼널 선별 보고서는 루트 디렉터리에 배치
├── AI-轮动判断-20260509.md    — 테마급 종합 판단 보고서는 루트 디렉터리에 배치
├── portfolio-latest.md       — 포트폴리오 보고서는 루트 디렉터리에 배치
└── 多公司对比-checklist-20260408.md — 다중 회사 보고서는 루트 디렉터리에 배치
```

## 보고서 명명 규칙

| Skill | 파일 명명 형식 | 예시 |
|------|---------|------|
| /investment-team | `{회사명}/` 디렉터리 내 4개 관점 + 최종 보고서 | `reports/拼多多/최종보고서.md` |
| /investment-research | `{회사명}-research-{YYYYMMDD}.md` | `reports/腾讯/腾讯-research-20260408.md` |
| /investment-checklist | `{회사명}-checklist-{YYYYMMDD}.md` | `reports/腾讯/腾讯-checklist-20260408.md` |
| /industry-research | `{산업명}-industry-{YYYYMMDD}.md`（루트 디렉터리） | `reports/核电-industry-20260409.md` |
| /industry-funnel | `{산업명}-funnel-{YYYYMMDD}.md`（루트 디렉터리） | `reports/AI算力-funnel-20260509.md` |
| /private-company-research | `{회사명}-private-{YYYYMMDD}.md` | `reports/字节跳动/字节跳动-private-20260408.md` |
| /earnings-review | `{회사명}-earnings-{기간}.md` | `reports/腾讯/腾讯-earnings-2025Q4.md` |
| /earnings-team | `{회사명}/` 디렉터리 내 4개 거장 관점+리서치 원고+공개 기사+독자 평가 | `reports/腾讯/腾讯-earnings-2025Q4.md`（공개 확정본） |
| /thesis-tracker | `{회사명}-thesis.md`（장기 유지 관리） | `reports/腾讯/腾讯-thesis.md` |
| /portfolio-review | `portfolio-latest.md`（루트 디렉터리, 지속 업데이트） | `reports/portfolio-latest.md` |
| /management-deep-dive | `{회사명}-management-{YYYYMMDD}.md` | `reports/腾讯/腾讯-management-20260409.md` |

## /investment-team 파일 구조

```
reports/{회사명}/
├── README.md                         — 리서치 프레임워크 개요 + 핵심 결론
├── 01-商业模式分析-段永平视角.md
├── 02-财务估值分析-巴菲特视角.md
├── 03-行业竞争分析-芒格视角.md
├── 04-风险管理层评估-李录视角.md
└── 최종보고서.md                     — Team Lead 종합 보고서
```

## 투자 리서치 분석 핵심 원칙（최고 우선순위）

- **객관성, 객관성, 객관성** — 모든 투자 리서치 분석은 반드시 사실과 데이터에 근거하며, 주관적 추측을 엄격히 금한다
- "사실"과 "의견"을 엄격히 구분한다: 사실은 데이터로 뒷받침하고, 의견은 반드시 "의견" 또는 "추측"으로 명시한다
- **선입견 배제**: 강세 또는 약세를 미리 전제하지 않는다. 데이터를 먼저 제시하고, 논리를 전개하며, 마지막에 결론을 낸다. 결론은 반드시 데이터에서 자연스럽게 도출되어야 한다
- "나는 ~라고 생각한다", "~인 것 같다", "명백히" 등의 주관적 표현을 금지한다. 대신 "데이터에 따르면", "증거에 의하면", "XX 출처에 따르면"으로 대체한다
- **양면 제시**: 모든 핵심 판단에는 반드시 반대 논거("그러나 반면에...")를 함께 제시하여 독자가 스스로 판단할 수 있게 한다
- 불확실한 사항은 "불확실" 또는 "데이터 부족"으로 솔직하게 명시하고, 추측으로 확실성을 채우지 않는다
- 모든 skill（investment-team、investment-research、earnings-review 등）실행 시 위 원칙을 반드시 준수한다

## 보고서 언어 및 스타일

- 모든 보고서는 **한국어**로 작성한다
- 스타일: 직접적·간결·군더더기 없이
- 데이터는 반드시 출처를 명시하고, 핵심 데이터는 최소 2개 출처를 교차 검증한다
- 추정값은 반드시 "추정"으로 표기한다
- 평점은 ★ 기호 사용（★1-5），반점 없음
- 워런 버핏/찰리 멍거/돤융핑/리루의 어록을 요소요소에 인용한다

## GitHub 작업

- 로컬 클론 경로: `~/ai-berkshire/`
- 원격 저장소: `https://github.com/xbtlin/ai-berkshire.git`
- 푸시 전 먼저 `git pull --rebase origin main` 실행（원격에 새 커밋이 자주 생김）
- commit message는 한국어로 작성하며 변경 내용을 명확히 기술한다
- 중간 과정 파일（예: data_collection.md）은 푸시하지 않는다. 최종 보고서만 푸시한다

## 자주 쓰는 명령어

```bash
# 보고서를 GitHub에 푸시
cd ~/ai-berkshire
git add reports/xxx.md
git commit -m "xxx 보고서 추가"
git pull --rebase origin main
git push origin main
```

## 주의 사항

- 시가총액은 반드시 수작업으로 검증: 주가 × 발행주식수를 계산하여 보고서 시총과 대조
- 통화 단위를 명확히 표기（홍콩달러/위안화/미달러），혼동 방지
- PE/ROE 등 지표는 tools/financial_rigor.py 로 정밀 계산한다
- 보고서 완성 후 GitHub 푸시 여부를 능동적으로 확인한다
