# AI 반도체 가치사슬 ─「AI 칩 설계 + EDA + IP」고리 전수 스캔

**작성 기준일: 2026-06-28 | 담당 고리: 칩 설계(GPU/ASIC) + EDA + IP**

> **방법론·면책**
> - 분석가 지식 컷오프는 2026-01. **2026년 데이터는 전부 WebSearch/WebFetch로 검증**했으며 출처 URL·시점을 명기한다.
> - 신뢰 수준: [높음]=1차 자료/직접계산, [중간]=불완전 데이터의 합리적 추론, [낮음]=정황 추정, [데이터 부족]=확인 불가.
> - 시가총액·주가는 일일 변동하므로 인용 시점(2026-06-23~28)을 함께 표기한다.
> - **객관성 원칙**: 사실을 먼저 제시하고, 모든 핵심 판단에 반대 논거를 병기한다.
> - **단위 주의**: 본 보고서의 "$1.74조" = 1.74 trillion USD, "$108억" 류 표기는 가급적 "억 달러" 또는 "billion"으로 명시. 영문 billion과 한국식 "억"의 혼동에 유의.

---

## 0. 가장 중요한 검증 사실 5가지 (Executive Summary)

| # | 검증 사실 | 결론 | 신뢰 |
|---|-----------|------|------|
| 1 | **엔비디아 데이터센터 매출·점유율** | FY2026(2026-01-25 종료) 데이터센터 매출 **$193.7B**(전사 매출 $215.9B). 최신 분기 FY2027 Q1(2026-04-26 종료) 데이터센터 **$75.2B**(+92% YoY). AI 가속기 **매출 기준 점유율 약 75~80%**(2024년 ~86% 정점에서 하락 중) | 압도적 지배 유지, 단 정점 통과 가능성 | [높음] |
| 2 | **CUDA 해자 강도** | 등록 개발자 **2백만 명+**, GPU 가속 앱 3,500개+, 라이브러리 600개+, 15년 누적 SW IP. 전환비용은 칩이 아니라 "스택 전체 교체" 비용 | 현존 최강 SW 해자 | [높음] |
| 3 | **커스텀 ASIC의 엔비디아 잠식** | **절대 점유율은 아직 엔비디아 우위**이나 **성장률 역전**: 2026년 ASIC 출하 +44.6% vs 머천트 GPU +16.1%(TrendForce). 하이퍼스케일러 자체칩 합산 점유율 **15~20%**로 확대. 브로드컴+마벨이 ASIC 공동설계 **~95%** 양분 | 잠식 진행 중, 단 "파이 확대 속 비중 상승" | [중간] |
| 4 | **2026 차세대 로드맵** | 엔비디아 **Vera Rubin** 풀 프로덕션 진입, 공급 **2026 H2**(Q3 출하 시작). AMD **MI400/MI455X + Helios 랙** **2026 H2/Q3**. 양사 모두 연간 신제품 사이클 | 군비경쟁 가속 | [높음] |
| 5 | **밸류에이션 거품 여부** | 엔비디아 Forward PER ~19배(의외로 낮음). 그러나 **AMD(Fwd PER ~60), 마벨(~59), Cadence(~46), ARM(~154), 캄브리콘(PE 200~3,800배), 중국 GPU IPO(상장 첫날 +425~700%)** 등 주변부로 갈수록 극단적 거품 | 엔비디아는 "E의 지속성"이 리스크, 주변부는 "P 자체"가 리스크 | [중간] |

---

## 1. 가치사슬 전체 지도 (Tier 분류 종합표)

> Tier 정의: **1**=대형 순수 선두 / **2**=중형 / **3**=소형·개발단계(주로 비상장) / **4**=다각화 대기업(AI칩이 투자 논리의 핵심이 아님)

### 1-A. AI 가속기·GPU (머천트 칩)

| 기업 | 티커·거래소 | 시총(2026-06) | 한 줄 역할 | 순수도 | Tier |
|------|------------|---------------|-----------|--------|------|
| 엔비디아 NVIDIA | NVDA·NASDAQ | **$4.66조** (6/26) | AI 가속기 사실상 독점 + 풀스택(칩+네트워킹+CUDA) | 순수 근접(DC 매출 ~90%) | **1** |
| AMD | AMD·NASDAQ | **$847~868B** (6/23~25) | 엔비디아의 유일한 실질 머천트 GPU 경쟁자(Instinct) + 서버 CPU(EPYC) | 다각화(DC가 성장축) | **2** |
| 인텔 Intel | INTC·NASDAQ | **~$642B** (6월, 주가 $127.62) | 가우디(Gaudi) 사실상 철수, Jaguar Shores로 피벗 | 다각화·AI칩 실패(가속기 시장 1% 미만) | **4** |

### 1-B. 커스텀 ASIC·네트워킹 칩

| 기업 | 티커·거래소 | 시총(2026-06) | 한 줄 역할 | 순수도 | Tier |
|------|------------|---------------|-----------|--------|------|
| 브로드컴 Broadcom | AVGO·NASDAQ | **$1.74조** (6/25~28) | 커스텀 AI 가속기(XPU) 공동설계 **1위** + AI 네트워킹(Tomahawk/Jericho) | 다각화(AI 반도체 ~49%, VMware 포함) | **1** |
| 마벨 Marvell | MRVL·NASDAQ | **$233~245B** (6/26) | 커스텀 실리콘 공동설계 **2위** + 광통신/인터커넥트 | 다각화(DC 76%) | **2** |

### 1-C. 하이퍼스케일러 자체칩 (모회사 = 다각화 대기업, 전부 Tier 4)

| 모회사 | 티커 | 모회사 시총(2026-06) | 자체칩 | 설계 파트너 | Tier |
|--------|------|---------------------|--------|------------|------|
| 알파벳 Alphabet | GOOGL·NASDAQ | **$4.1~4.6조** (6/25) | **TPU**(Ironwood v7) — 외부 판매 개시 | Broadcom | **4** |
| 아마존 Amazon | AMZN·NASDAQ | **$2.50조** (6/26) | **Trainium**(3세대)/Inferentia | Marvell(Trn2)→Alchip(Trn3) | **4** |
| 마이크로소프트 Microsoft | MSFT·NASDAQ | **$3.11조** (6월) | **Maia 200**(2026-01 배포) | (Marvell 협력 보도) | **4** |
| 메타 Meta | META·NASDAQ | **$1.39조** (6/26) | **MTIA**(300 양산, 400 시험) | Broadcom | **4** |

### 1-D. EDA (전자설계자동화)

| 기업 | 티커·거래소 | 시총(2026-06) | 한 줄 역할 | 순수도 | Tier |
|------|------------|---------------|-----------|--------|------|
| 시놉시스 Synopsys | SNPS·NASDAQ | **$87.0B** (6/26) | EDA·설계IP 1위 + Ansys(시뮬레이션) 인수 | 부분 다각화(EDA+IP ~71%) | **1** |
| 케이던스 Cadence | CDNS·NASDAQ | **$104B** (6/26) | EDA 양강 + 에뮬레이션·시스템설계 | 순수 근접 | **1** |
| 지멘스 EDA Siemens EDA | (Siemens AG·ETR:SIE) | 모회사 ~$213~240B | EDA 빅3 3위(Calibre 물리검증 85%+) | 거대복합기업 일부 | **4** |

### 1-E. IP (설계 자산)

| 기업 | 티커·거래소 | 시총/밸류(2026) | 한 줄 역할 | 순수도 | Tier |
|------|------------|-----------------|-----------|--------|------|
| Arm Holdings | ARM·NASDAQ | **$357~383B** (6/24~26) | CPU 명령어셋(ISA) IP 표준, 라이선스+로열티 | 순수 IP | **1** |
| SiFive | 비상장 | **$3.65B** (Series G, 2026-04) | RISC-V CPU IP 1위(Arm의 오픈 대안) | 순수 IP | **3** |

### 1-F. AI 칩 스타트업 (미국·한국)

| 기업 | 상태 | 시총/밸류(2026) | 한 줄 역할 | Tier |
|------|------|-----------------|-----------|------|
| 세레브라스 Cerebras | **상장**(CBRS·NASDAQ, 2026-05-14 IPO) | **~$86~95B**(상장 첫날) | 웨이퍼스케일 엔진(WSE), 추론 특화 | **2** |
| 그록 Groq | 비상장 | **$6.9B**(2025-09) | LPU 추론 칩, GroqCloud | **3** |
| 텐스토렌트 Tenstorrent | 비상장(Qualcomm 인수설 $8~10B) | $2B(2024-12 prev-money) | RISC-V AI 칩, Jim Keller | **3** |
| 삼바노바 SambaNova | 비상장 | **~$2.2B**(2026-02, **다운라운드**) | 추론으로 피벗, 구조조정 | **3** |
| 리벨리온 Rebellions | 비상장(한국, IPO 예정 2026말) | **~$2.34B**(2025) | 한국 1호 AI칩 유니콘(사피온 합병) | **3** |
| 퓨리오사AI FuriosaAI | 비상장(한국) | ~$550M+(증액 중) | RNGD 추론칩, Meta 인수 거부·LG 협력 | **3** |
| 사피온 Sapeon | **소멸**(2024-12 리벨리온에 합병) | — | (구 SKT 자회사, 리벨리온에 통합) | — |

### 1-G. 중국 AI 칩

| 기업 | 티커·거래소 | 시총/밸류(2026) | 한 줄 역할 | Tier |
|------|------------|-----------------|-----------|------|
| 캄브리콘 Cambricon 寒武纪 | 688256·상하이 STAR | **¥8,877억/~$123~135B** (6/24) | 중국 상장 순수 AI칩 1위("중국판 엔비디아") | **1**(상장 순수 기준) |
| 하이실리콘 HiSilicon 海思 | 비상장(화웨이 자회사) | (화웨이 비상장) | **Ascend 昇腾 910C** — 중국 AI칩 실질 1강 | **3**(투자 불가) |
| 무어스레드 Moore Threads 摩尔线程 | **상장**(STAR, 2026, +425% 첫날) | ~$1.1B 조달 | 범용 GPU(전 엔비디아 중국대표 창업) | **2~3** |
| MetaX 沐曦 | **상장**(STAR, 2025-12, +~700% 첫날) | ~$540M 조달 | GPGPU(전 AMD 임원 창업) | **2~3** |
| 비런 Biren 壁仞 | **상장**(홍콩, 2026-01-02, ~$717M) | ~$717M 조달 | 고성능 GPGPU | **2~3** |

---

## 2. Tier 1·2 기업 심층 분석 (4대 거장 프레임워크)

---

### 2-1. 엔비디아 NVIDIA (NVDA) ─ Tier 1

**기본**: NVDA·NASDAQ | 주가 $192.53(6/26) | 시총 **$4.66조**(세계 1위) | 발행주식 ~242.2억 주
출처: [stockanalysis.com](https://stockanalysis.com/stocks/nvda/market-cap/), [macrotrends](https://www.macrotrends.net/stocks/charts/NVDA/nvidia/market-cap) [높음]
> **회계연도 주의**: FY는 1월 말 종료. **FY2026=2026-01-25 종료(보고완료)**, FY2027 진행 중. 최신 분기=**FY2027 Q1(2026-04-26 종료, 2026-05-20 발표)**.

**① 비즈니스**

| 지표 | FY2027 Q1(최신) | FY2026(연간) |
|------|-----------------|--------------|
| 총매출 | $81.6B (+85% YoY) | $215.9B (+65%) |
| 데이터센터 | **$75.2B** (+92% YoY) | **$193.7B** (+68%) |
| GAAP 순이익 | $58.3B(분기) | $120.1B |
| GAAP 매출총이익률 | 74.9% | 71.1% |
| 잉여현금흐름 | — | $96.6B |

- Q2 FY2027 가이던스: 매출 **$91.0B ±2%**, 마진 70%대 중반, **중국 데이터센터 매출 0 가정**. 출처: [NVIDIA 뉴스룸 Q1 FY2027](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-first-quarter-fiscal-2027), [CNBC](https://www.cnbc.com/2026/05/20/nvidia-nvda-earnings-report-q1-2027.html) [높음]
- 매출총이익률 추이: FY26 Q2 72.4% → Q3 73.4% → Q4 75.0% → FY27 Q1 74.9%. 블랙웰 초기 램프 때 눌렸다가 회복. [높음]
- **데이터 충돌 해소**: 일부 2차 매체는 FY2026 DC 매출을 $197.3B로 보도하나, 1차 보도자료 기준 **$193.7B** 채택(컴퓨팅+네트워킹 집계 차이). [높음]

**② 해자**
- **CUDA(소프트웨어 락인) — 현존 최강**: 등록 개발자 2백만 명+(1백만 도달 13년 → 2백만 추가 2년 미만, 가속), 가속 앱 3,500개+, 라이브러리 600개+. 전환비용은 커널 재작성+성능 재검증+엔지니어 재교육의 **스택 전체 교체** 비용. 출처: [NVIDIA 개발자 블로그](https://developer.nvidia.com/blog/celebrating-the-2-million-innovators-changing-the-world/) [높음]
- **네트워킹 해자**: 2019년 Mellanox 인수($6.9B) 기반. InfiniBand/NVLink(학습) + Spectrum-X 이더넷(추론) 양 패브릭 장악. 네트워킹 분기 매출 ~$10~15B. [중간]
- **규모·기술장벽**: TSMC CoWoS 우선 할당, 연간 신제품 사이클(Hopper→Blackwell→Rubin).

**③ 밸류에이션**(6/28, [stockanalysis.com](https://stockanalysis.com/stocks/nvda/statistics/) [높음])

| PER(TTM) | Fwd PER | PSR | EV/EBITDA | PEG |
|----------|---------|-----|-----------|-----|
| ~29.5 | **~19.4** | ~18.4 | ~27.9 | 0.43 |

- **핵심**: 절대 PER 29.5배는 엔비디아 과거 밴드(50~70배)보다 오히려 낮음 — 이익 성장이 주가보다 빨라 멀티플 압축. PSR 18.4배는 반도체 업종(통상 한 자릿수) 대비 압도적 프리미엄.

**④ 경영진**: CEO·공동창업자 **젠슨 황(Jensen Huang)**, 지분 약 3.3~3.6%(8.1~8.8억 주). 단일 클래스 주식(1주 1의결권). FY2026 주주환원 $41.1B, Q1 FY27 분기배당 25배 인상. [중간—정확 지분율은 DEF 14A 확인 필요]

**⑤ 핵심 리스크 / 똑똑한 투자자가 망설이는 이유**
1. **AI capex 사이클 반전(최대 거시 리스크)**: 하이퍼스케일러 capex가 매출의 45~57%(SaaS 시대 11~16%의 4~5배). ROI 미실현 시 급조정.
2. **이중 압축 위험**: PER는 합리적이나 그 E가 capex 정점 이익일 수 있음 → 사이클 정상화 시 P와 E 동시 하락.
3. **하이퍼스케일러 자체칩 + AMD**: 점유율 정점(~86%→75%) 통과 신호.
4. **중국**: FY2027 가이던스 중국 DC 매출 0. H200 양국 라이선스 승인됐으나 인도 불확실+25% 세금. Blackwell급은 여전히 "거부 추정". [중간]
5. **고객 집중**: 매출 ~40%가 소수 하이퍼스케일러.

**⑥ 로드맵**: **Vera Rubin** — GTC 2026(3/17) 발표, GTC Taipei(6/1) 풀 프로덕션 확인, 공급 **2026 H2**. VR200: FP4 50 PFLOPS, HBM4 288GB, TSMC N3, B300 대비 컴퓨트 ~3.3배. 7개 신규 칩(Vera CPU, Rubin GPU, NVLink 6, ConnectX-9, BlueField-4, Spectrum-6 등). 출처: [NVIDIA 뉴스룸 Vera Rubin](https://nvidianews.nvidia.com/news/vera-rubin-full-production-agentic-ai-factory) [중간~높음]

---

### 2-2. AMD ─ Tier 2

**기본**: AMD·NASDAQ | 시총 **$847~868B**(6/23~25) | 사상최고가 $551.63(6/22) | 30일 +41.5%, 12개월 +143%
출처: [stockanalysis.com](https://stockanalysis.com/stocks/amd/market-cap/), [macrotrends](https://www.macrotrends.net/stocks/charts/AMD/amd/market-cap) [높음]

**① 비즈니스**

| 지표 | Q1 2026(최신) | FY2025(연간) |
|------|---------------|--------------|
| 총매출 | $10.3B (+38% YoY) | $34.6B |
| 데이터센터 | **$5.8B** (+57% YoY) | $16.6B (+32%) |
| GAAP 매출총이익률 | 53% (Non-GAAP 55%) | 50% (Non-GAAP 52%) |
| GAAP 순이익 | $1.4B (Non-GAAP $2.3B) | $4.3B (Non-GAAP $6.8B) |
| 잉여현금흐름 | $2.6B (FCF 마진 ~25%) | — |

출처: [AMD Q1 2026 IR](https://www.amd.com/en/newsroom/press-releases/2026-5-5-amd-reports-first-quarter-2026-financial-results.html), [AMD FY2025 IR](https://ir.amd.com/news-events/press-releases/detail/1276/) [높음]
- **Meta 6GW 약정**: 다년 계약, 초기 1GW는 커스텀 MI450 기반. [높음]

**② 해자**: CUDA 대비 **ROCm은 여전히 후발**. AMD 경쟁축은 메모리 용량·가격대비성능·개방성. 점유율 ~6~9%(2025) → 15%+ 목표(2026말). 해자는 엔비디아보다 약하나 "유일한 실질 대안"이라는 포지션 자체가 가치. [중간]

**③ 밸류에이션**(6월, [stockanalysis](https://stockanalysis.com/stocks/amd/statistics/), [GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/AMD))

| PER(TTM) | Fwd PER | EV/EBITDA |
|----------|---------|-----------|
| **172.9** | 60~69 (출처별) | 113.3 |

- GuruFocus: 반도체 업종 중간값(Fwd PER 34.1) 대비 **79% 프리미엄, "Significantly Overvalued"**. [중간]

**④ 경영진**: CEO **리사 수(Lisa Su)**, 지분 ~0.3~0.5%(약 290~377만 주, ~$1.5~1.6B). 전문경영인이나 AMD를 부활시킨 상징. 2026년 85,000주 매도 기록. [중간]

**⑤ 리스크**: ① CUDA 락인 돌파 실패 가능 ② 밸류에이션이 엔비디아보다 비쌈(Fwd PER 60+ vs 19) — 실행 미달 시 디레이팅 폭 큼 ③ TSMC CoWoS 할당 경쟁 ④ MI308 중국 수출규제로 $440M 재고손실(FY2025).

**⑥ 로드맵**: **MI400 시리즈**(CES 2026, 1/5 공개) — MI430X/MI440X/MI455X, CDNA 5, HBM4 **432GB**(MI350 대비 +50%), 대역폭 19.6TB/s, FP4 40 PFLOPS, TSMC N2. **Helios 랙**(72× MI455X, 2.9 FP4 엑사플롭스) **2026 Q3/H2**. MI500은 2027(MI300 대비 1,000배 주장). 출처: [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/amd-touts-instinct-mi430x-mi440x-and-mi455x-ai-accelerators), [NextPlatform](https://www.nextplatform.com/compute/2026/02/23/amd-says-helios-racks-and-mi400-series-gpus-on-track-for-2h-2026/) [중간~높음]

---

### 2-3. 브로드컴 Broadcom (AVGO) ─ Tier 1

**기본**: AVGO·NASDAQ | 시총 **$1.74조**(6/25~28) | 주가 ~$378.91(6/25)
출처: [stockanalysis.com](https://stockanalysis.com/stocks/avgo/statistics/) [높음]
> 순수도: 다각화. FY2026 Q2 AI 반도체 ~49%, 나머지(비AI 반도체+VMware) 51%.

**① 비즈니스**(FY2026 Q2, 2026-06-03 발표, [Broadcom IR via StockTitan](https://www.stocktitan.net/news/AVGO/broadcom-inc-announces-second-quarter-fiscal-year-2026-financial-if4yrbje8hq6.html) [높음])
- 총매출 **$22.19B**(+48% YoY), **AI 반도체 $10.8B**(+143% YoY)
- 매출총이익률(TTM) 76.3%, 순이익률(TTM) 38.9%, **FCF $10.26B**(매출의 46%)
- **가이던스**: Q3 AI 반도체 **$16B**, **FY2026 AI 매출 ~$56B**(+~180%), **FY2027 AI $100B 초과** 재확인(월가 회의적)
> 단위: 위 "$56B/$16B/$100B"는 billion(560억/160억/1,000억 달러)

**② 해자**
- **기술장벽·설계IP [높음]**: Google TPU 7세대 공동설계(2014~), SerDes·어드밴스드 패키징·칩렛 IP.
- **전환비용·고객 lock-in [높음]**: XPU 한 세대 공동설계에 수년·수억 달러 → 중도 교체 난망. 다년 멀티-기가와트 계약.
- **고객(검증)**: Google TPU, Meta MTIA, **OpenAI(10GW)**, **Anthropic(1→3GW)**, ByteDance, Fujitsu. 출처: [IBTimes](https://www.ibtimes.com/what-broadcom-unknown-company-building-ai-chips-powering-google-anthropic-openai-meta-3802922) [중간~높음]
- ASIC 공동설계 시장 **~60~70%** 점유. [중간]

**③ 밸류에이션**(6/28): 시총 $1.74조, PER(TTM) 60.8, **Fwd PER 23~31**(출처편차), PSR 23.0, EV/EBITDA 42.3. [높음]

**④ 경영진**: CEO **혹 탄(Hock Tan)**(2006~), M&A 자본배분 달인(VMware 등). FY2025 보상 $205.3M(대부분 주식). 인센티브가 AI 매출 목표(2030 $120B)에 연동. 직접 지분 ~0.019%. [높음]

**⑤ 리스크**: ① **FY2027 $100B 가이던스 월가 회의**(Q2 후 주가 ~11% 급락) ② PSR 23·EV/EBITDA 42의 거품 우려 ③ 고객 집중(특히 Google) ④ VMware 둔화(+9%) ⑤ 하이퍼스케일러 설계 내재화.

---

### 2-4. 마벨 Marvell (MRVL) ─ Tier 2

**기본**: MRVL·NASDAQ | 시총 **$233~245B**(6/26) | 주가 $272.67
출처: [stockanalysis.com](https://stockanalysis.com/stocks/mrvl/statistics/) [높음]

**① 비즈니스**(Q1 FY2027, 2026-05-27 발표, [Marvell IR](https://investor.marvell.com/news-events/press-releases/detail/1023/) [높음])
- 순매출 **$2,417.8M**(+28% YoY), 데이터센터 $1,832.7M(76%)
- 매출총이익률 GAAP 52.1%/Non-GAAP 58.9%, 순이익 GAAP $34.5M/Non-GAAP $718.0M(괴리 큼)
- 영업현금흐름 $638.8M(사상최대). 커스텀 실리콘 매출 FY2026 **~$1.5B**(브로드컴 분기 $10.8B의 ~1/7)

**② 해자**: 광통신 DSP·SerDes·인터커넥트 IP [높음]. **엔비디아가 2026-03 $2B 투자 + NVLink Fusion 파트너십**. ASIC 점유율 **~25%**(2위). 단 브로드컴 대비 lock-in 약함. [중간]
- **고객(검증)**: Amazon Trainium2, Microsoft Maia, Meta, (Google 협상 중). [중간]

**③ 밸류에이션**(6/28): PER(TTM) 92~117, **Fwd PER 59~70**, PSR 26.8, EV/EBITDA **86.6**. **브로드컴보다 전 멀티플에서 더 비쌈**. [높음]

**④ 경영진**: CEO **매트 머피(Matt Murphy)**(2016~, 전문경영인), 지분 ~$2.1억. 최근 1년 **순매도**. [중간]

**⑤ 리스크**: ① 밸류에이션이 브로드컴보다 더 거품(Fwd PER 59~70, EV/EBITDA 87) ② **고객 내재화 위험이 더 큼**(Amazon Trn3 백엔드가 Marvell→Alchip으로 이동) ③ **2026-06-09 ByteDance-Qualcomm ASIC 딜 보도에 Marvell -10% 급락**(신규 진입자) ④ GAAP 이익의 질 낮음.

---

### 2-5. 시놉시스 Synopsys (SNPS) ─ Tier 1 (EDA)

**기본**: SNPS·NASDAQ | 주가 $454.34(6/26) | 시총 **$87.0B**(수작업 검증: $454.34×191.48M=$86.99B ✓)
출처: [stockanalysis.com](https://stockanalysis.com/stocks/snps/) [높음]

**① 비즈니스**(Q2 FY2026, 2026-04-30 종료. FY는 10월 말 종료)
- 매출 **$2,276M**(+42% YoY, **단 대부분 Ansys 연결효과**, 유기적 EDA는 +8%)
- 세그먼트: EDA $1,822M(+8%), Design IP $454M(−6%), Ansys $652M
- GAAP EPS $0.09(Ansys 상각으로 압축) vs **Non-GAAP EPS $3.35**. 백로그/RPO **~$11.0B**(매출의 ~5배)
- FY2026 가이던스: 매출 $9.665B, Non-GAAP EPS $14.76, FCF ~$2B
출처: [10-Q via StockTitan](https://www.stocktitan.net/sec-filings/SNPS/10-q-synopsys-inc-quarterly-earnings-report-7ceeee1568d4.html), [Futurum](https://futurumgroup.com/insights/synopsys-q2-fy-2026-ai-driven-chip-design-demand-lifts-outlook/) [높음]

**② 해자(EDA 듀오폴리)**: Synopsys+Cadence가 EDA **~74~85%** 장악(추정편차). 전환비용 극강(설계플로우+PDK 인증 락인), 첨단노드(2nm) 도구는 파운드리 공동인증 필요. [높음/점유율은 중간]

**③ 밸류에이션**: PER(TTM,GAAP) 107.6(Ansys 상각 왜곡), **Fwd PER 29~35**, PSR 10.0, NTM EV/EBITDA ~25배(Cadence ~34.5보다 저평가). [중간]

**④ 경영진**: CEO **Sassine Ghazi**(2024~), 공동창업자 **Aart de Geus**(1986~, 현 Executive Chair). 내부자 ~2.0%, **순매도 지속**(Ghazi 5년 9건 전부 매도). [높음]

**⑤ Ansys 인수(검증완료)**: **2025-07-17 완료**, ~$35B, Ansys 주당 $197 현금+0.345주, Ansys 주주가 합병법인 16.5%. 부채 ~$10.8B, 영업권+무형자산이 총자산 83%. 출처: [Synopsys 공식](https://news.synopsys.com/2025-07-17-Synopsys-Completes-Acquisition-of-Ansys) [높음]

**⑤ 리스크**: ① **중국 수출규제(최대)** — 2025년 가이던스 하향 시 주가 -35% 전례 ② Design IP 구조적 약세(-6~8%) ③ 밸류에이션 부담 ④ Ansys 부채·무형자산 손상 리스크 ⑤ **+42% 성장은 착시**(유기적 +8%), 하반기 Ansys 기저효과 소멸 시 헤드라인 급락.

---

### 2-6. 케이던스 Cadence (CDNS) ─ Tier 1 (EDA)

**기본**: CDNS·NASDAQ | 주가 $377.27(6/26) | 시총 **$104.06B**(수작업 검증 ✓)
출처: [stockanalysis.com](https://stockanalysis.com/stocks/cdns/) [높음]

**① 비즈니스**(Q1 2026, 2026-03-31 종료)
- 매출 **$1,474.2M**(+18.7% YoY), GAAP 순이익 $335.7M, Non-GAAP EPS $1.96(+25%)
- **매출총이익률 86.1%**(TTM), Non-GAAP 영업이익률 44.7%. 백로그 **$8.0B**(TTM매출 1.4배)
- 세그먼트: Core EDA +18%, IP +22%, **하드웨어 에뮬레이션 "역사상 최고 분기"**(AI/HPC 주도)
- FY2026 가이던스: 매출 $6.125~6.225B(+17%). **주의: Q1 OCF -27%, FCF -34% YoY**(추적 필요)
출처: [Cadence Q1 2026 IR](https://investor.cadence.com/news/news-details/2026/Cadence-Reports-First-Quarter-2026-Financial-Results/default.aspx), [Futurum](https://futurumgroup.com/insights/cadence-q1-fy-2026-earnings-driven-by-agentic-ai-expansion-and-emulation-hardware/) [높음]

**② 해자**: EDA 빅3 양강. 강점=에뮬레이션(Palladium Z3/Protium X3, NVIDIA 채택), 아날로그(Virtuoso). BETA CAE+Hexagon D&E($3.16B, 2026-02 완료) 인수로 멀티피직스 확장. [높음]

**③ 밸류에이션**: PER(TTM) **87.9**, **Fwd PER 46.4**, PSR 18.8, EV/EBITDA 52.4. **모든 멀티플에서 Synopsys보다 비쌈**(매출은 SNPS의 69%인데 시총 1.4배). [높음]

**④ 경영진**: CEO **Anirudh Devgan**(2021~). CEO 2026-06 76,827주($30.8M) 매도(10b5-1 정례 가능성). 내부자 지분율 데이터 부족. [중간]

**⑤ 리스크**: ① **밸류에이션(최대)** PER 88/Fwd 46, PSR 18.8 ② 중국 노출 ~13%+수출규제 변동성(2025 라이선스 부과→해제, $1.4억 벌금) ③ 현금흐름 둔화 신호 ④ 인수 희석(FY2026 EPS -$0.28) ⑤ AI "10배 생산성"은 자사 마케팅, Synopsys도 동일 추진(차별화 해자 아닌 공통 군비경쟁).

---

### 2-7. Arm Holdings (ARM) ─ Tier 1 (IP)

**기본**: ARM·NASDAQ | 주가 $334.27(6/26) | 시총 **$357~383B**(6/24~26) | **SoftBank ~87% 보유**
출처: [stockanalysis](https://stockanalysis.com/stocks/arm/), [TradingKey](https://www.tradingkey.com/analysis/stocks/us-stocks/261921505-arm-300b-softbank-87-stake-wins-cpu-fuels-wall-street-tradingkey) [높음]

**① 비즈니스**(FY2026, 2026-03-31 종료, 발표 2026-05-06)
- 총매출 **$4.92B**(+23%), 로열티 $2.613B(+21%), 라이선스 $2.307B(+25%)
- Q4 매출 $1.49B(+20%), 데이터센터 로열티 **2배+** YoY. Non-GAAP EPS(연) $1.77
- RPO $2,071M(-7% YoY), Arm Total Access 라이선스 56개. 순이익 $904M
- **공급 제약**: TSMC 웨이퍼 매진 + 메모리(HBM) 부족(CFO 발언)
출처: [Arm 뉴스룸 Q4 FYE26](https://newsroom.arm.com/news/arm-q4-fye26-results), [Investing.com](https://www.investing.com/news/transcripts/earnings-call-transcript-arm-holdings-reports-record-q4-fy2026-results-93CH-4665853) [높음]

**② 해자**: CPU 명령어셋(ISA) **사실상 표준** — 모바일 99%+, 하이퍼스케일 클라우드 CPU 컴퓨트 ~50%. Armv9 채택+CSS로 칩당 로열티율 상승. 생태계 락인 극강. [높음]

**③ 밸류에이션**: PER(TTM) **394.9**, **Fwd PER 153.8**. **본 보고서 전체에서 가장 극단적 멀티플 중 하나**. 출처: [stockanalysis](https://stockanalysis.com/stocks/arm/statistics/) [높음]

**④ 경영진**: CEO **Rene Haas**. SoftBank(손정의) ~87% 지배 → 유동주식 적음(멀티플 왜곡 요인). [높음]

**⑤ 리스크 / 안 사는 이유**: ① **밸류에이션(Fwd PER 154)이 압도적 부담** ② **자체 칩 진출 = 라이선시와 경쟁**: 2026-03 **AGI CPU**(136코어 Neoverse V3, TSMC 3nm, Meta가 첫 고객, OpenAI·Cerebras·Rebellions 등) 직접 판매 시작 → ③ **FTC 반독점 조사(2026-05)**: 라이선스 통제+경쟁칩 판매의 이해상충 ④ RISC-V(SiFive 등) 오픈 대안의 신규 AI 가속기 침투 ⑤ SoftBank 오버행. 출처: [CNBC](https://www.cnbc.com/2026/03/24/arm-launches-its-own-cpu-with-meta-as-first-customer.html), [TechTimes](https://www.techtimes.com/articles/318254/20260611/arm-builds-its-own-data-center-cpu-agi-chip.htm) [높음]

---

### 2-8. 캄브리콘 Cambricon 寒武纪 (688256) ─ Tier 1 (중국 상장 순수 AI칩)

**기본**: 688256·상하이 STAR | 주가 ¥1,453(6/24, 52주 ¥349~1,540) | 시총 **¥8,877억 / ~$123~135B**
출처: [companiesmarketcap](https://companiesmarketcap.com/cambricon-technologies/marketcap/), investing.com [중간—환율·시점 편차]
> 2024년 +387%, 2025-08 일시 마오타이 추월(A주 최고가주), 사상최고 ¥1,595.88. 저점 대비 ~4.5배.

**① 비즈니스(흑자전환 확인)**

| 항목 | 2024 | 2025 | 2026 Q1 |
|------|------|------|---------|
| 매출 | ¥11.74억(+65.6%) | **¥64.97억(+453%)** | ¥28.85억(+159.6%) |
| 순이익 | -¥4.52억(적자) | **+¥20.59억(흑자전환)** | +¥10.13억(+185%) |

- **2025년 = 상장(2020) 이래 첫 연간 흑자**. 매출총이익률 ~55%, 순이익률 ~31.7%. 출처: [ithome](https://www.ithome.com/0/924/333.htm) [높음]

**② 밸류에이션(거품 논란 핵심)**: 시점별 극단 변동 — 2025말 PS(TTM) **71배**·PE(TTM) **247배**(엔비디아 PS 27/PE 38의 2.6~6.5배). 2025-10 고점 PS ~120배·PE ~3,800배("극도 고평가 95분위"). 동방재부 연구보고서: "밸류에이션 동력이 펀더멘털→심리·전략 프리미엄으로 전환". [높음]

**③ 경영진**: 창업자 겸 CEO·실제지배인 **천톈스(陈天石)**(1985년생, 중과원 계산소 출신), 합산 의결권 ~35.6%. [높음/지분 중간]

**④ 리스크(전부 [높음])**: ① **고객 집중**(2024 단일최대 79.15%, 상위5 94.6%) ② **SMIC 7nm 의존**(SMIC도 Entity List) ③ **미국 Entity List 등재**(2022-12) ④ **재고 급증**(2025말 ¥49.44억 +178%, 대손충당) ⑤ 화웨이 Ascend(국산 1강)·T-Head·쿤룬 경쟁.
> **순수도 주의**: "중국 상장 순수 AI칩 1위"는 맞으나 **중국 AI칩 시장 전체 1위는 화웨이(비상장)**. 출하량은 화웨이에 크게 뒤짐.

---

### 2-9. 세레브라스 Cerebras (CBRS) ─ Tier 2 (신규 상장)

**기본**: **CBRS·NASDAQ, 2026-05-14 IPO**(2026 최대 IPO, Uber 이후 최대 미 테크 IPO) | IPO가 $185 → 첫날 +68% $311.07 → 시총 **~$95B**(완전희석 ~$86B)
- IPO 조달 **$5.55B**(3,000만 주). FY 매출 **$510M**(+76%), 순이익 **$88M**(전년 -$481.6M에서 흑전). **$10B OpenAI 딜**.
출처: [CNBC](https://www.cnbc.com/2026/05/14/cerebras-cbrs-stock-trade-nasdaq-ipo.html), [Cerebras 공식](https://www.cerebras.ai/press-release/cerebras-systems-announces-pricing-of-initial-public-offering) [높음]
- **역할**: 웨이퍼스케일 엔진(WSE) — 단일 거대 칩, 초고속 추론 특화. CEO **Andrew Feldman**(공동창업).
- **리스크**: ① **매출 대비 시총 극단적**(PS ~170~190배: $86~95B/$510M) ② OpenAI 단일 고객 집중 ③ 엔비디아 대비 niche.

---

## 3. Tier 3·4 요약 (투자 직접 노출 제한)

### 3-A. 하이퍼스케일러 자체칩 (전부 Tier 4 — 모회사 티커로만 노출)

- **공통 전략**: 엔비디아 의존도 축소 + 추론 비용 절감. 2026 하이퍼스케일러 합산 capex **$660~690B**(75%가 AI). 엔비디아 매출의 ~40%가 자체칩 만드는 4사에서 발생. 출처: [TrendForce/검색](https://www.techtimes.com/articles/317225/), [alcapitaladvisory](https://alcapitaladvisory.com/research/intelligence/ai-infrastructure.html) [중간]

| 자체칩 | 현황(2026) | 설계 파트너(=ASIC사 투자 논리 연결) |
|--------|-----------|-------------------------------------|
| **Google TPU** Ironwood v7 | **외부 판매 개시** — Anthropic에 $40B 투자+1M Ironwood, Meta 임대(2026)/구매(2027), xAI·SSI 등 | **Broadcom**(랙 직판) |
| **Amazon Trainium3** | 2026초 출하·Q2 양산, 거의 완전예약. Project Rainier=Anthropic 100만+ Trn2 가동. Anthropic 최대 $330억 투자, OpenAI 2GW. 커스텀칩 $200억 런레이트 | **Marvell**(Trn2)→**Alchip**(Trn3 백엔드) |
| **Microsoft Maia 200** | 2026-01 배포(전 "Braga", 2025서 지연). TSMC 3nm, 216GB HBM3E. GPT-5.2/Copilot 서비스 | (Marvell 협력 보도) |
| **Meta MTIA** | MTIA 300 양산(랭킹/추천), 400 시험. 로드맵 300~500(2027까지) | **Broadcom** |

출처: [Tom's Hardware 커스텀 ASIC](https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia), [SemiAnalysis Trainium3](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential), [Microsoft Maia 200](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/), [Google TPU/Anthropic](https://thenextweb.com/news/google-tpu-compute-internal-researchers-anthropic) [중간~높음]

> **투자 시사점**: 하이퍼스케일러 자체칩 붐의 **순수 수혜주는 모회사가 아니라 설계 파트너(Broadcom·Marvell·Alchip)**. 모회사는 AI칩이 투자 논리의 핵심이 아닌 Tier 4.

### 3-B. 미국·한국 스타트업 (전부 비상장, Tier 3 — Cerebras만 상장 후 Tier 2)

| 기업 | 핵심 사실 | 생존·리스크 |
|------|-----------|------------|
| **Groq** | LPU 추론, 마지막 밸류 $6.9B(2025-09), Saudi $1.5B, **NVIDIA $17B 라이선스 딜**(2025-12, $20B "not-acqui-hire"), $650M 라운드(2026-06) | NVIDIA 라이선스로 자금 확보, 추론 niche |
| **Tenstorrent** | RISC-V AI, Jim Keller CEO, **Qualcomm 인수설 $8~10B**(2026-06), prev $2B(2024-12) | 인수 성사 시 exit, 밸류 3배 점프 |
| **SambaNova** | **다운라운드** $5.1B(2021)→$2.2B(2026-02), 추론 피벗·15% 감원, **Intel $1.6B 인수 무산**(2025말) | 구조적 고전, 생존 의문 |
| **Rebellions(리벨리온)** | 사피온 합병(2024-12)=한국 1호 AI칩 유니콘, $400M pre-IPO→**~$2.34B**, **IPO 2026말 예정** | 한국 대표주자, ATOM/REBEL, Arm AGI CPU 파트너 |
| **FuriosaAI(퓨리오사)** | **Meta $800M 인수 거부**(2025), LG AI Research 협력(RNGD 2.25x 추론), **$500M pre-IPO 모집**(2026-01, 모건스탠리·미래에셋) | 독립노선 선택, IPO 추진 |
| **Sapeon(사피온)** | **소멸** — 리벨리온에 합병(2024-12) | — |

출처: [Cerebras CNBC](https://www.cnbc.com/2026/05/14/cerebras-cbrs-stock-trade-nasdaq-ipo.html), [Groq TechCrunch](https://techcrunch.com/2026/06/22/ai-chipmaker-groq-confirms-650m-raise-re-staffs-after-nvidias-20b-not-acqui-hire-deal/), [Tenstorrent Tom's](https://www.tomshardware.com/tech-industry/artificial-intelligence/qualcomm-mulls-taking-over-jim-kellers-tenstorrent-report-claims), [SambaNova TSG](https://tsginvest.com/sambanova/), [Rebellions 코리아헤럴드](https://www.koreaherald.com/article/10012110), [FuriosaAI TechCrunch](https://techcrunch.com/2025/07/21/instead-of-selling-to-meta-ai-chip-startup-furiosaai-signed-a-huge-customer/) [높음~중간]

### 3-C. 인텔 Intel (INTC) ─ Tier 4 (AI 가속기 사실상 철수)

- **시총 ~$642B**(6월, 주가 $127.62). 2026년 주가 급등(~190~500% YTD)은 **AI 가속기가 아니라 미 정부 9.9% 지분 인수($8.9B) + NVIDIA $5B 투자 + SoftBank·Silver Lake 등 $20.4B 외부자본 + 파운드리 회생 기대** 때문. [중간~높음]
- **Gaudi 결론: 경쟁력 상실** — 디스크리트 AI 가속기 시장 **1% 미만**(과거 서버 CPU 99% 점유와 대비), 2024 $500M 매출 목표 미달·폐기, Habana($2B 인수) 전략 실패. SW 생태계 미성숙(CUDA 등가물 부재). 출처: [Nasdaq](https://www.nasdaq.com/articles/intel-just-gutted-its-ai-chip-ambitions) [높음]
- **로드맵**: Falcon Shores 상용 취소(내부 플랫폼 전환) → 후속 **Jaguar Shores**(랙스케일, 18A+HBM4) 출시 **2027 하반기 추정** → NVIDIA Rubin 후속·AMD MI500 대비 2~3세대 뒤처진 진입. 추격 가능성 [낮음]
- FY2025 매출 $52.9B(2010년 이후 최약), CEO **립부 탄(Lip-Bu Tan)**(2025-03 취임). [높음]

### 3-D. 중국 (캄브리콘 외)

| 기업 | 핵심 사실 |
|------|-----------|
| **HiSilicon 海思 / 화웨이 Ascend** | **910C가 중국 AI칩 실질 1강**. 2026년 60만 개 생산(2x), 성능 H100의 ~80%(추론 ~60%), B200 BF16의 ~1/3. SMIC 7nm. 고객 알리바바·텐센트·딥시크. 정부 승인 공급사(엔비디아 제외). **비상장→투자 불가** |
| **Moore Threads 摩尔线程** | **STAR 상장(2026), 첫날 +425%**, ~$1.1B 조달. 전 엔비디아 중국대표 창업. 범용 GPU |
| **MetaX 沐曦** | **STAR 상장(2025-12), 첫날 +~700%**, ~$540M. 전 AMD 임원 창업 |
| **Biren 壁仞** | **홍콩 상장(2026-01-02), ~$717M**. 2026년 1월 홍콩 첫 신규상장 |

출처: [Huawei Ascend Tom's](https://www.tomshardware.com/tech-industry/semiconductors/huaweis-ascend-ai-chip-ecosystem-scales), [중국 GPU IPO CNBC](https://www.cnbc.com/2025/12/17/metax-moore-threads-chinese-rivals-nvidia-ai-chips.html), [Biren Tom's](https://www.tomshardware.com/tech-industry/biren-kicks-off-hong-kong-ipo) [중간]

> **중국 IPO 거품 신호**: 상장 첫날 +425~700%, 청약 수천 배 초과 — 펀더멘털보다 "국산화 테마+유동성"이 가격을 견인. 수출규제 수혜의 정책 베팅 성격.

---

## 4. 핵심 질문에 대한 종합 판단

**Q1. 엔비디아 점유율 80~90%대가 맞나? CUDA 해자 강도는?**
→ **매출 기준 ~75~80%**(2024년 ~86% 정점에서 하락 중)이 정확. "90%대"는 게이밍 포함 또는 출하량 기준일 가능성. CUDA는 개발자 2백만 명·15년 SW IP의 **현존 최강 해자**이나, 신규 AI 가속기(ASIC)는 인스트럭션 락인이 없어 추론 영역에서 침투 여지. [높음]

**Q2. 커스텀 ASIC이 엔비디아를 잠식하나?**
→ **절대 점유율은 아직 엔비디아 우위, 그러나 성장률은 ASIC이 역전**(2026 +44.6% vs +16.1%). 하이퍼스케일러 자체칩 합산 15~20%로 확대, 일부 애널리스트는 추론 영역 엔비디아 점유율이 2028년 20~30%까지 하락 전망(공격적). **순수 잠식이 아니라 "파이 확대 속 비중 상승"**. 수혜주는 Broadcom·Marvell. [중간]

**Q3. 2026 차세대 로드맵?**
→ 엔비디아 **Vera Rubin**(2026 H2 공급, Q3 출하), AMD **MI400/Helios**(2026 Q3/H2). 양사 연간 사이클로 군비경쟁 격화. [높음]

**Q4. 밸류에이션 거품?**
→ **엔비디아는 의외로 합리적**(Fwd PER 19, PEG 0.43) — 리스크는 가격이 아니라 "E의 지속성"(capex 사이클). **주변부로 갈수록 극단적**: AMD(60), 마벨(59), Cadence(46), **ARM(154)**, **캄브리콘(PE 247~3,800)**, **중국 GPU IPO(첫날 +425~700%)**, **Cerebras(PS ~170~190)**. 가치투자 관점 안전마진이 있는 종목은 사실상 없음. [중간]

---

## 5. 데이터 부족·검증 한계

- **SEC 1차 문서(8-K/10-Q 원문)는 WebFetch 403 차단** → NVIDIA/AMD/Broadcom 등은 회사 뉴스룸·StockTitan·CNBC·Futurum 교차검증으로 대체(핵심 수치 다수 출처 일치 [높음]).
- **인텔(INTC)**: 시총 ~$642B 확인(주가 $127.62, 6월). 2026 주가 급등은 정부지분·NVIDIA $5B 투자·파운드리 기대 때문이며 Gaudi와 무관.
- **시가총액·밸류에이션 멀티플은 출처·시점별 편차** 존재(특히 캄브리콘 환율, ARM/Broadcom Fwd PER) → 범위로 표기.
- **하이퍼스케일러 자체칩 vs 엔비디아 정확한 % 분할**: 비공개 → 데이터 부족.
- **비상장 스타트업 매출**: 대부분 비공개(Cerebras만 IPO로 공개) → 밸류에이션은 사모 라운드 가격(공개시장 미검증).
- **중국 GPU 3사(무어스레드/MetaX/비런) 상장 후 현재 시총**: 첫날 급등 폭만 확인, 6월말 현재 시총은 미확정 → 데이터 부족.
- **AMD/캄브리콘 등 일부 정밀 지표는 tools/financial_rigor.py 재계산 권장**.

---

*본 보고서는 사실·데이터 우선, 양면 제시, 출처 명기 원칙에 따라 작성되었다. 투자 권유가 아니며, 모든 수치는 인용 시점 기준이다.*
