---
last_mapped_commit: 4f7aec20fe95c4de306943808c2c22ce404a8148
mapped: 2026-06-27
---

# 外部集成（INTEGRATIONS）

本项目的外部集成分两类：(1) `tools/*.py` 脚本**直接通过 HTTP/浏览器访问**的接口；(2) `skills/*.md` 在执行时**约定让 Claude（经 WebSearch/WebFetch）访问**的数据源网站。没有数据库、没有 OAuth/鉴权服务、没有消息队列、没有 webhook 接收端。

## 一、代码直接调用的 HTTP API / 服务

### 腾讯行情 API（A 股实时行情）

- 端点：`https://qt.gtimg.cn/q={code}`（如 `sh600519`）。
- 调用方：`tools/ashare_data.py`（`_curl()` → `/usr/bin/curl --noproxy '*'`）。
- 特征：无需鉴权；返回 `~` 分隔的字段串；**GBK 编码**（脚本 UTF-8 失败后回退 GBK）。`_qq_code()` 按代码前缀映射 `sh`/`sz`/`bj`。
- 用途：`quote` / `valuation` / `financials` 子命令的行情快照来源。

### 东方财富 datacenter API（A 股财务数据）

- 端点：`https://datacenter.eastmoney.com/securities/api/data/get`。
- 调用方：`tools/ashare_data.py`（`cmd_financials`）。
- 参数：`type=RPT_F10_FINANCE_MAINFINADATA`、按 `SECUCODE` 与 `REPORT_TYPE="年报"` 过滤，`source=HSF10`、`client=PC`，取近 5 期年报；无结果则去掉年报过滤重试。

### 东方财富搜索建议 API（股票代码搜索）

- 端点：`https://searchadapter.eastmoney.com/api/suggest/get`。
- 调用方：`tools/ashare_data.py`（`cmd_search`）。
- 参数：`type=14`、`count=10`，并带一个**硬编码的 `token`**（`D43BF722C8E33BDC906FB84D85E326E8`，公开 API token，非私密凭据）。
- 返回：`QuotationCodeTable.Data`（含 `MktNum` 沪/深/北市场标识）。

### Yahoo Finance Chart API（美股/港股日线行情）

- 端点：`https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1=...&period2=...&interval=1d`。
- 调用方：
  - `tools/stock_screener.py`（`fetch_prices_curl`，经 `subprocess` 调 `curl`，`User-Agent: Mozilla/5.0`，绕过 Python SSL 问题）。
  - `tools/momentum_backtest.py`（`fetch_price_data`，用标准库 `urllib.request.urlopen` + `Request` 头）。
- 注意：脚本注释明确提到 Yahoo API **会被限流/限制**（`momentum_backtest_v2.py` 因此改为对 NVDA 手工录入数据、对 AMD/MU 读本地 JSON）。

### Morningstar 筛选器 API（全市场公允价值）

- 端点：`https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener?...`。
- 调用方：`tools/morningstar_fair_value.py`（`fetch_page`，经 `curl`）。
- 参数：分页抓取（`pageSize=100`），按 `FairValueEstimate desc` 排序，universe 为纳斯达克+纽交所（`E0EXG$XNAS|E0EXG$XNYS`），取 `FairValueEstimate` / `ClosePrice` / `StarRatingM255` / `EconomicMoat` 等字段。
- 产出：计算潜在涨幅，落盘 `data/morningstar_fair_value_{YYYYMMDD}.csv`。
- URL 内含一段路径片段 `klr5zyak8x`（Morningstar 公开接口 key，非用户私密凭据）。

### 雪球（Xueqiu）—— 带登录态的网页抓取

- 站点：`https://xueqiu.com/`；数据端点 `https://xueqiu.com/v4/statuses/user_timeline.json?user_id=...&page=...&count=...`。
- 调用方：`tools/xueqiu_scraper.py`（**唯一使用 Playwright** 的工具，无头/有头 Chromium）。
- 鉴权机制：
  - 首次运行弹出有头浏览器**人工登录**（扫码/短信/密码），登录态以 `storage_state` 持久化到 `--state-path`（默认 `/tmp/xueqiu_state.json`，已在 `.gitignore` 中排除，含 cookies）。
  - 凭据**经环境变量传入、不入库**：`XQ_PHONE`、`XQ_PASSWORD`（脚本头部明示）。
  - 反检测：注入 `navigator.webdriver=undefined`、自定义 User-Agent、`zh-CN` locale。
  - 反限流：随机抖动、每 50 页长休、断点续爬（进度文件 `*.progress.{user_id}`）。
- 双通道取数：优先页面内 JS `fetch`（`credentials: 'include'`），失败回退 `context.request`（APIRequestContext）。

## 二、Skill 在执行时约定访问的数据源（经 Claude 的 WebSearch/WebFetch）

这些不是代码里的 HTTP 调用，而是 `skills/*.md`（尤其 `skills/financial-data.md`）规定 Claude 在做研究时应访问的网站。Skill 中 `WebSearch` 被引用约 14 次、`WebFetch` 约 2 次。

`skills/financial-data.md` 定义的数据源优先级（"每个关键数据须来自 2 个独立来源，误差>1% 告警"）：

| 市场 | 主来源 | 副来源 | 一手原始 |
|------|--------|--------|----------|
| 美股 | `macrotrends.net/stocks/charts/{ticker}` | `stockanalysis.com/stocks/{ticker}/financials` | SEC EDGAR `sec.gov/cgi-bin/browse-edgar`（10-K / 10-Q） |
| 港股 | `aastocks.com`（公司基本面） | `macrotrends`（ADR 代码，如腾讯 TCEHY、网易 NTES） | HKEX 披露易 `hkexnews.hk`（年报 PDF） |
| A 股 | 东方财富 `eastmoney.com`（搜代码→财务报表） | 巨潮资讯 `cninfo.com.cn`（原始年报/季报 PDF） | 同左 |

`report_audit.py` 的抽检流程同样提示 Claude 从这些信源取数核验（美股 macrotrends + stockanalysis；港股 aastocks + macrotrends ADR；A 股 eastmoney + cninfo）。

其他在 Skill 正文中作为信息渠道被提及的来源：

- **富途（futu）/ 同花顺** — 港股行业分类、持股比例口径（`skills/industry-funnel.md`、`skills/deep-company-series.md`）。
- **雪球** — 大师（如段永平 user_id=1247347556）言论整理（`xueqiu_scraper.py` 的目标，亦在多个 Skill 中作为引用源）。
- 其余在数据源名称扫描中出现的高频词：macrotrends、stockanalysis、aastocks、eastmoney、cninfo、Yahoo Finance、Morningstar、wind、SEC（10-K/10-Q）。

## 三、版本控制 / 仓库远程

- Git 远程：`https://github.com/xbtlin/ai-berkshire.git`（`CLAUDE.md` 第 90 行；`README.md` / `README_EN.md` 的 clone 指令）。
- README 嵌入 **Star History** 徽章：`https://api.star-history.com/svg?repos=xbtlin/ai-berkshire`（图片服务，非代码集成）。
- README 指向 **Claude Code** 官网 `https://claude.ai/code`（项目运行平台）。
- 推送约定（`CLAUDE.md`）：`git pull --rebase origin main` 后 `git push origin main`；本地克隆路径 `~/ai-berkshire/`。

## 四、平台集成：Claude Code

- 项目本质是 Claude Code 的 Skill 合集，依赖其 **slash command** 机制（Skill 复制到 `~/.claude/commands/`）与内置工具（WebSearch / WebFetch / Bash）。
- **Hook 集成**：`tools/log-command.sh` 设计为 Claude Code `user_prompt_submit` hook 的执行体（从 stdin 读取用户指令并记日志）。hook 的注册配置不在本仓库（需在用户的 Claude Code settings 中挂接）。

## 未涉及的集成（明确为"无"）

- 无数据库（无 SQL/NoSQL 连接、无 ORM）。
- 无认证/授权服务（除雪球的人工登录态外，无 OAuth provider、无 API key 管理体系；出现的 Morningstar key、东方财富 token 均为各接口内嵌的公开标识）。
- 无 webhook 接收端、无消息队列、无云服务 SDK、无支付/邮件/IM 等第三方 SaaS 集成。
