# 재무 데이터 수집 및 교차 검증 규범

본 규범은 기업 재무 데이터를 다루는 모든 리서치에 적용된다. **핵심 데이터는 반드시 두 개의 독립 출처에서 확보해야 하며, 오차 >1%이면 표시한다.**

---

## 데이터 출처 우선순위

### 미국주식（PDD、腾讯ADR、网易ADR 등）

| 우선순위 | 출처 | URL | 접근 방법 |
|--------|------|-----|---------|
| 1（주） | **macrotrends** | macrotrends.net/stocks/charts/{ticker} | 직접 접근, 회원가입 불필요 |
| 2（부） | **stockanalysis** | stockanalysis.com/stocks/{ticker}/financials | 직접 접근, 회원가입 불필요 |
| 원본 1차 | SEC EDGAR | sec.gov/cgi-bin/browse-edgar | 10-K / 10-Q 원문 |

### 홍콩주식（腾讯0700、网易9999、美团3690 등）

| 우선순위 | 출처 | URL | 접근 방법 |
|--------|------|-----|---------|
| 1（주） | **aastocks** | aastocks.com/tc/stocks/analysis/company-fundamental | 직접 접근 |
| 2（부） | **macrotrends**（ADR 코드） | 腾讯은 TCEHY, 网易은 NTES | 직접 접근 |
| 원본 1차 | HKEX 披露易 | hkexnews.hk | 연간보고서 PDF |

### A주（三七互娱、吉比特 등）

| 우선순위 | 출처 | URL | 접근 방법 |
|--------|------|-----|---------|
| 1（주） | **东方财富** | eastmoney.com → 종목코드 검색 → 재무제표 | 직접 접근 |
| 2（부） | **巨潮资讯** | cninfo.com.cn | 원본 연간보고서/분기보고서 PDF |

---

## 실행 규범

### 1단계: 데이터 수집

각 재무지표（매출, 순이익, 매출총이익률, 영업현금흐름, 부채비율 등）를 **출처 1**과 **출처 2**에서 각각 수집한다.

### 2단계: 오차 계산 및 표시

```
오차율 = |출처1 수치 - 출처2 수치| / 출처1 수치 × 100%
```

| 오차 | 처리 방법 |
|------|---------|
| ≤ 1% | ✅ 일치, 출처1 수치 사용, 두 출처 모두 표기 |
| 1% ~ 5% | ⚠️ "데이터 차이 존재" 표시, 두 수치 모두 기재, 가능한 원인 설명（환율/회계 기준） |
| > 5% | ❌ "데이터 중대 차이 존재" 표시, 원본 재무제표 반드시 확인, 직접 사용 불가 |

### 3단계: 데이터 표기 형식

핵심 데이터는 반드시 아래 형식으로 표기한다:

```
수익：1,239억元 ✅
  - macrotrends: 1,241억元
  - stockanalysis: 1,237억元
  - 오차: 0.3%
```

차이 예시:
```
순이익：245억元 ⚠️ 데이터 차이 존재
  - macrotrends: 245억元（GAAP）
  - stockanalysis: 278억元（Non-GAAP）
  - 오차: 13.5% — 원인：회계 기준 상이（GAAP vs Non-GAAP）
```

---

## 흔한 차이 원인（반드시 데이터 오류는 아님）

| 원인 | 설명 |
|------|------|
| GAAP vs Non-GAAP | 가장 흔함, 특히 이익 계열 데이터 |
| 환율 환산 | 홍콩달러/위안화/달러 환산 시점 상이 |
| 회계연도 정의 | 역년 vs 회계연도（예: 애플 회계연도는 10월 마감） |
| 연결 범위 | 비지배지분 포함 여부 |
| 데이터 업데이트 지연 | 특정 플랫폼이 최신 재무제표 미반영 |

---

## 특별 규칙

1. **비상장 기업**（米哈游、莉莉丝 등）: 1차 데이터 출처만 있을 때는 수치 앞에 `[추정]` 표시, 교차 검증 미실시
2. **분기 데이터 vs 연간 데이터**: 연간 데이터를 우선으로 교차 검증, 분기 데이터는 일부 출처 지연 가능
3. **원본 재무제표 우선**: 두 출처 모두 원본 재무제표（10-K/연간보고서 PDF）와 불일치하면 원본 재무제표 기준, 출처 오류 표기

---

## 빠른 색인

| 상황 | 주 출처 | 보조 출처 |
|------|---------|---------|
| PDD / 拼多多 | macrotrends.net/stocks/charts/PDD | stockanalysis.com/stocks/pdd |
| 腾讯 | macrotrends.net/stocks/charts/TCEHY | aastocks（0700.HK） |
| 网易 | macrotrends.net/stocks/charts/NTES | aastocks（9999.HK） |
| 三七互娱 | eastmoney.com（002555） | cninfo.com.cn |
| 吉比特 | eastmoney.com（603444） | cninfo.com.cn |
| Nintendo | macrotrends.net/stocks/charts/NTDOY | stockanalysis.com/stocks/ntdoy |
| Capcom | macrotrends（CCOEY） | stockanalysis（CCOEY） |
