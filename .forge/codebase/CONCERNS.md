---
last_mapped_commit: 4f7aec20fe95c4de306943808c2c22ce404a8148
mapped: 2026-06-27
---

# CONCERNS — 技术债 / 已知问题 / 脆弱区

本项目是 Claude Code 投研 Skill 合集（`.md` Skill + 少量 Python 工具 + 2083 个 Markdown 报告）。
没有应用运行时、没有 CI、没有测试。因此"技术债"主要集中在三处：
(1) 数据保鲜与 git 历史噪音；(2) `tools/*.py` 的正确性与安全缺陷；(3) 报告目录命名规范的漂移。
以下每条均锚定真实文件路径与可复现事实。

---

## 0. 凭据扫描结果（机密）

对全仓（排除 `.git`）grep `sk-` / `ghp_`/`gho_` / `AKIA` / `eyJ`(JWT) / `BEGIN PRIVATE KEY` / `api_key`/`secret`/`password`/`token` 赋值：

- **未发现任何真实的 OpenAI/Anthropic key、GitHub token、AWS key、JWT 或私钥。** 这一项是干净的。
- 唯一命中是 `tools/ashare_data.py:276` 的一个硬编码 `"token": "D43BF722C8E33BDC906FB84D85E326E8"`。
  - 这是**东方财富公开搜索接口** `searchadapter.eastmoney.com/api/suggest/get` 的固定查询参数，不是个人凭据，泄露不构成账户风险。
  - 但它仍是硬编码常量：东财若更换该 token，`cmd_search` 会静默失效（且失败被吞，见 §2.3）。**[中]**
- `tools/xueqiu_scraper.py:13-16` 的处理是正面案例：雪球登录凭据通过环境变量 `XQ_PHONE`/`XQ_PASSWORD` 注入，文档明确写"**不进入代码仓库**"；`.gitignore` 第 7 行也排除了 `/tmp/xueqiu_state.json`（含 cookies 的登录态缓存）。**[高]** 这是正确做法。

结论：无真实凭据泄露。仅 1 处公开接口 token 硬编码，影响为功能脆弱性而非安全。

---

## 1. 数据保鲜风险（最高优先级，本项目最大的系统性债）

### 1.1 股价被烤进报告，过期极快

报告把实时股价直接写进 Markdown 正文，而非引用动态数据源。以 LEU（瓶颈猎手核心标的）为例，在 `reports/bottleneck-map/` 下 grep `LEU` 旁的价格字符串，得到**十余个互相冲突的历史价**散落各文件：

```
$161.78 / $162.58 / $163.35 / $163.50 / $165.47 / $165.80 / $169.81 / $176.14 / $180.20 / $183.51 / $191.39 / 目标价 $244.91
```

- 最新 commit `4f7aec2`（`第304轮`）专门"更新LEU股价至$165.80"，说明维护者**靠人工逐条刷价**来对抗过期——这本身就是债的证据，不可规模化。
- 致命点在于**无日期前缀的汇总文件**会长期挂着旧价：`reports/bottleneck-map/top-opportunities.md`、`reports/bottleneck-map/master-map.md` 内含 `$163.50` 等旧值，读者无从判断它是哪天的价。**[高]**
- 任何读取本仓报告做决策的人，若不核对报告内的日期戳，会拿到**过期数月**的价格。CLAUDE.md 已要求"估计值必须注明'估计'"，但没有要求"股价必须注明抓取时间戳"。建议：所有内联股价强制带 `(YYYY-MM-DD 抓取)` 标注，汇总文件只引用而不复制价格。

### 1.2 静态数据文件无更新机制

`data/` 下的数据是一次性快照，文件名/内容即过期标记，但无刷新流程：

- `data/morningstar_fair_value_20260519.csv`（75 KB，日期烤进文件名，已过期 1 个月+）。
- `data/fundamentals.json`（NVDA 等财报季度数据，最新条目需逐条核对是否停更）。
- `data/correlation_3stocks_2021-2026.csv` / `cross_asset_10y_2016-2026.csv`（区间烤进文件名，到期后无人提醒重算）。
- `data/watchlist.json` 的 `a_share` 分类为空数组 `[]`——疑似占位未填，待验证是否有下游工具假设它非空（`stock_screener.py` 读取 watchlist 时可能空跑）。**[中]**

---

## 2. `tools/*.py` 正确性与安全缺陷

仓内 8 个 Python 工具（共 3052 行），**零测试、零 CI**。逐一审计后发现以下真实缺陷。

### 2.1 `financial_rigor.py` —— "currency" 参数是装饰性的，不做币种校验 **[高]**

`verify_market_cap(price, shares, reported_cap, currency="")`（`tools/financial_rigor.py:61-91`）：

- `--currency` 仅在第 73/75/76 行被**打印进标签**，从不参与计算。
- 偏差计算（第 68 行）`abs(calculated - r)/r` 直接比较两个裸数字，**完全不检查 price 与 reported_cap 是否同币种**。
- 讽刺的是，偏差 >5% 时它自己打印的告警（第 83 行）"`单位是否一致（港币 vs 人民币 vs 美元）?`"恰恰是它无法检测的失败模式——它把"港币股价 × 股本 vs 人民币市值"这种混币错误当普通数值偏差处理，可能误判为通过。
- 这与 CLAUDE.md "货币单位要明确（港币/人民币/美元），防止混淆""市值必须手算校验"的核心规则正面冲突：**号称做市值严谨性校验的工具，恰恰不校验最容易出错的币种维度。**
- 同样问题存在于 `three_scenario_valuation`（`:320`）的 `currency` 参数。

### 2.2 `financial_rigor.py:288-313` —— `exact_calc` 的"安全 eval"名不副实 **[中]**

```python
allowed = set("0123456789.+-*/() eE")
if not all(c in allowed for c in expr.replace(" ", "")):
    ...
result = eval(expr, {"__builtins__": {}}, {})
```

实测（仅测字符过滤，未执行 eval）：

| 表达式 | 通过过滤? |
|--------|-----------|
| `2**10` | True |
| `9**9**9` | True |
| `1e1000` | True |
| `(1).__class__` | False（下划线被挡） |

- **DoS 风险**：`*` 在白名单内 → `**`（幂）合法 → `9**9**9` 会让进程长时间占满 CPU/内存直至挂死。
- **溢出**：`1e1000` → `eval` 得 `inf` → `exact(inf)` 走 `Decimal(str(inf))` 抛 `InvalidOperation`，被 `except Exception`（第 311 行）吞掉只打印错误。
- RCE 概率低（`__builtins__` 已清空、下划线被白名单挡掉，`__class__` 这类逃逸进不来），所以**不是远程代码执行级别的洞**，但注释"Safe evaluation"高估了安全性。这是本地工具，攻击面有限，故评 [中] 而非 [高]。

### 2.3 静默吞异常，校验可"假通过" **[高]**

多处 `except Exception: pass` / `except Exception:` 把失败藏起来，违反"客观、数据必须可核验"原则：

- `tools/ashare_data.py:185` `shares = cap / p`（推算总股本做市值验算）整段包在 `try: ... except Exception: pass`（`:181-192`）里。一旦 `p` 解析失败或为 0，**整个市值验算静默跳过**，调用方却以为校验过了——这正是 CLAUDE.md "市值必须手算校验"想防的事，却被静默吞掉。
- `tools/ashare_data.py:222`、`:231` 同样裸吞。
- 全仓 `except Exception` 计 16 处（`ashare_data` 3、`xueqiu_scraper` 8、`momentum_backtest`/`stock_screener`/`morningstar_fair_value`/`financial_rigor` 各若干）。爬虫场景吞网络异常尚可理解，但**财务校验路径吞异常会制造"假阴性安全感"**。

### 2.4 `momentum_backtest.py:315` —— 除零 + 可能未绑定变量 **[中]**

```python
for p in prices:
    if p["date"] >= buy_date:
        final_price = p["close"]
final_date = prices[-1]["date"]
total_return = (final_price - buy_price) / buy_price * 100
```

- `buy_price` 来自 `first_buy["close"]`，无 `!= 0` 守卫——若收盘价为 0/缺失，`ZeroDivisionError`。
- `final_price` 仅在循环命中 `p["date"] >= buy_date` 时赋值；若 `prices` 全部早于 `buy_date`（数据切片错误），`final_price` **未定义** → `NameError`。
- `momentum_backtest_v2.py:237/332` 的 `/ first_buy["close"]`、`/ buy_p` 同类除零无守卫。
- `morningstar_fair_value.py:86` `(fair_value - close_price)/close_price`、`:144` `/ len(undervalued)`（`undervalued` 为空时除零）同类风险。
- 相较之下，`financial_rigor.py`（`:68/:113/:125/:146/:188`）与 `report_audit.py:248` **有** `if x != 0 else` 守卫，处理较规范——除零防护在工具间不一致，是质量参差的信号。

### 2.5 `momentum_backtest.py` 与 `momentum_backtest_v2.py` 并存 —— 疑似遗留 **[低/待验证]**

两个版本同时在仓（360 行 vs 397 行），无文档说明 v1 是否已废弃。若 v1 已被 v2 取代却未删除，是死代码；按 CLAUDE.md "发现无关死代码应提示而非删除"，此处仅标记，不建议自行删。

---

## 3. git 历史噪音：瓶颈猎手扫描的自动化 churn **[高]**

- 全仓共 **1151** 个 commit，其中含"瓶颈猎手"字样的达 **616 个（≈53%）**——**超过一半的提交历史是自动扫描记录**。
- 其中 `reports/bottleneck-map/` 下含"无新信号"字样的扫描文件有 **162 个**，目录总文件数 **483**。最近 commit 串（`第300/301/302/303/304轮`）连续 5 条都是"无新信号"。
- 后果：
  - `git log` / `git blame` 被扫描记录淹没，**真实的报告/工具变更被埋没**，难以追溯有意义的改动。
  - 每小时一轮 × 304+ 轮的提交节奏，使 diff review、bisect、changelog 全部失去信噪比。
  - `reports/bottleneck-map/` 下每天一个日期目录（`2026-05-26` … `2026-06-21`+），每目录十余个时点文件，**文件数随时间线性膨胀且永不归档**。
- 建议（不在本任务范围内执行）：把"无新信号"轮次的产物落到**单一滚动日志文件**而非每轮新文件 + 新 commit；或将这类自动扫描移出主仓（独立分支/独立仓/`.gitignore`）。

### 3.1 `.forge/` 未被 gitignore —— 地图可能被卷入 churn **[中]**

`.gitignore` 中**没有** `.forge/` 条目（grep 确认）。本地图文档（及未来的 fg-map 产物）默认可被 `git add` 跟踪。在每小时自动 commit 的环境下，存在被"瓶颈猎手扫描"批量提交顺手带进版本库、或与人工提交混杂的风险。若不希望地图进仓，需显式加入 `.gitignore`。

---

## 4. 报告目录命名规范漂移 vs CLAUDE.md `命名规范`

CLAUDE.md 规定：所有报告按**公司名（中文）**建文件夹、放 `reports/` 下、按表格命名格式。实际存在多处违反：

### 4.1 仓库根目录的游离报告（违反"报告放 reports/"） **[高]**
- `RKLB-investment-research.md`（28 KB，应在 `reports/` 下，且应为 `{公司名}-research-{YYYYMMDD}`）
- `sailis-touzi-yanjiu-baogao.md`（30 KB，拼音命名，无日期，散在根目录）
两者都**绕过了 `reports/` 目录结构**，属于规范外产物。

### 4.2 拼音 vs 中文命名混用（规范要求中文公司名） **[中]**
`reports/` 下混杂大量拼音文件名：
- `hengrui-yiyao-touzi-yanjiu-baogao-20260625.md`（恒瑞医药）
- `jingfang-keji-touzi-yanjiu-baogao-20260625.md`（晶方科技）
- `chunfeng-dongli-603129-investment-research-20260624.md`（春风动力）
- `zijin-mining-investment-research-20260624.md` / `Putailai-investment-research-20260624.md` / `focus-media-...` / `chemring-group-deep-dive.md`
而同类报告又有纯中文目录（`reports/恒瑞`?/`reports/晶泰科技`/`reports/腾讯`…）。**命名语言不统一**，破坏了"按公司名归档"的可检索性。

### 4.3 同名条目既是目录又是文件（结构歧义） **[中]**
`reports/长光辰芯-team-20260409`（目录）与 `reports/长光辰芯-team-20260409.md`（文件）**同名并存**。按 CLAUDE.md，`/investment-team` 产物应是目录内含 4 视角 + 最终报告；这里又多出一个同名 `.md`，疑似旧单文件版本未清理。**[待验证]**

### 4.4 多份顶层报告未归入公司文件夹
根级 `reports/*.md` 散落数十个跨公司/主题报告（`7公司10年利润对决-买哪个-20260515.md`、`蚂蚁系-5年估值全景-...` 等）。CLAUDE.md 允许"行业/漏斗/对比报告放根目录"，故这类**部分合规**；但与 4.1/4.2 的违规混在一起，使 `reports/` 根目录有 100+ 项，**人工很难分辨哪个是规范内、哪个是漏归档**。

### 4.5 v1/v2 报告并存
`reports/基础大模型训练方法论综述-2025-2026.md` 与 `...-v2.md` 并存，无标注哪个为现行版——读者可能引用过时的 v1。**[低]**

### 4.6 双 CLAUDE 记忆文件
根目录有 `CLAUDE.md`（项目指令）与 `ai_CLAUDE.md`（"AI 记忆文件"，记录用户画像/历史决策）。两者用途不同、非重复，但命名相近易混淆；`ai_CLAUDE.md` 不是 Claude Code 约定的记忆文件名（约定是 `CLAUDE.md`），故其内容**不会被自动加载**，仅作普通文档。**[低/待验证]** 是否有意为之需向维护者确认。

---

## 5. 其它观察

- `reports/腾讯-deepseek分析` / `reports/百度-deepseek分析` 等 `-deepseek分析` 后缀目录与 CLAUDE.md 命名表无对应条目——疑似规范外的临时分类。**[低/待验证]**
- 顶层既有 `reports/` 又有 `筛选公司/`、`实盘记录/`、`数据`(`data/`)、`docs/`、`logs/` 等中文/英文混合目录，**目录组织缺乏单一约定**，新人难以快速定位某类产物。**[低]**
- 无 `requirements.txt`/`pyproject.toml`：`xueqiu_scraper.py` 依赖 `playwright`，但仓内无依赖声明，**运行前提靠注释口口相传**，易踩"未装 playwright"的坑。**[中]**
- `tools/*.py` 全部依赖 `curl`/`subprocess` 抓第三方接口（东财、腾讯行情、雪球），**接口一旦改版即静默失效**（叠加 §2.3 的吞异常），数据正确性缺乏外部校验闭环。**[中]**

---

## 优先级速览

| 等级 | 条目 |
|------|------|
| 高 | §1.1 内联股价过期（无时间戳）、§2.1 市值校验不验币种、§2.3 财务校验吞异常假通过、§3 git 历史 53% 被自动扫描淹没、§4.1 根目录游离报告 |
| 中 | §0 东财 token 硬编码、§1.2 静态数据无更新机制、§2.2 eval 幂运算 DoS、§2.4 回测除零/未绑定变量、§3.1 `.forge` 未 gitignore、§4.2/§4.3 命名漂移、§5 无依赖声明 |
| 低/待验证 | §2.5 momentum v1/v2 并存、§4.5 报告 v1/v2、§4.6 双 CLAUDE 文件、§5 -deepseek分析 目录、目录组织 |
