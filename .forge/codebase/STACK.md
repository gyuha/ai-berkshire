---
last_mapped_commit: 4f7aec20fe95c4de306943808c2c22ce404a8148
mapped: 2026-06-27
---

# 技术栈（STACK）

本项目是一套基于 **Claude Code** 的价值投资研究 Skill 合集。它不是传统的 Web/服务端应用，没有构建系统、没有依赖清单、没有服务进程。代码主体是 `skills/` 下的 Markdown Skill 定义（供 Claude Code 作为 slash command 加载执行），辅以 `tools/` 下的若干独立 Python/Shell 脚本，以及 `reports/`、`data/`、`assets/` 等内容/数据目录。

## 语言构成

| 语言 | 位置 | 用途 |
|------|------|------|
| **Markdown** | `skills/*.md`（18 个 Skill 定义）、`reports/`（大量研究报告）、`docs/`、根目录 `README.md` / `README_EN.md` / `CLAUDE.md` / `ai_CLAUDE.md` | 项目主体。Skill 定义是给 Claude Code 执行的"程序"，报告是产物 |
| **Python 3** | `tools/*.py`（7 个脚本） | 财务计算、数据抓取、选股、报告抽检等辅助工具 |
| **Bash** | `tools/log-command.sh` | Claude Code hook 脚本，记录用户指令到日志 |

没有 JavaScript/TypeScript、没有前端框架、没有数据库、没有任何编译型语言。`assets/architecture.mmd` 是一个 Mermaid 图源文件（架构图）。

## 运行时与解释器版本

- Python 脚本均以 `#!/usr/bin/env python3` 为 shebang（`tools/` 下 8 处）。
- `tools/financial_rigor.py`、`tools/report_audit.py` 文档注明 **要求 Python >= 3.7**。
- `tools/ashare_data.py` 文档注明 **要求 Python >= 3.8**，且其用法示例中显式调用 `python3.11`（4 处 `python3.11` 引用集中在此脚本与相关 Skill 中）。
- Bash 脚本 `tools/log-command.sh` 为 `#!/bin/bash`。

## 框架与第三方库

**核心特征：绝大多数工具零外部依赖，仅用 Python 标准库。** `financial_rigor.py` 与 `ashare_data.py` 的文件头明确写"Zero external dependencies / 零外部依赖"。

`tools/*.py` 全量 import 统计（来自源码扫描）：

| 库 | 类型 | 使用脚本 |
|----|------|---------|
| `json`, `sys`, `os`, `argparse`, `re`, `math`, `time`, `csv`, `random`, `asyncio` | Python 标准库 | 各脚本 |
| `datetime`, `decimal`, `collections`, `pathlib`, `urllib.request`, `random.Random` | Python 标准库 | 各脚本 |
| `subprocess` | 标准库（用于调用 `curl`，见下） | `ashare_data.py`、`stock_screener.py`、`morningstar_fair_value.py` |
| **`playwright`**（`from playwright.async_api import async_playwright`） | **唯一的第三方依赖** | `tools/xueqiu_scraper.py` |

唯一的外部依赖是 **Playwright**（无头 Chromium 浏览器自动化），仅 `xueqiu_scraper.py` 使用，用于雪球登录态复用与时间线抓取。项目无 `requirements.txt` / `pyproject.toml`，Playwright 需用户自行安装（含 `playwright install chromium` 一类的浏览器下载，未在仓库中脚本化）。

注意：部分脚本不直接用 Python 的 HTTP 库，而是通过 `subprocess` 调用系统 **`curl`** 发请求（`ashare_data.py` 用 `/usr/bin/curl --noproxy '*'` 绕过系统代理；`stock_screener.py`、`morningstar_fair_value.py` 用 `curl -s -H "User-Agent: ..."`）。`momentum_backtest.py` 则用标准库 `urllib.request`。

## 配置与运行方式

**没有项目级配置文件**（仓库内无 `settings.json`、`.mcp.json`、`requirements.txt`、`pyproject.toml`、`Makefile`、`package.json` 等；`find` 全仓确认）。

### Skill 的安装与调用（项目主要"运行"方式）

`README.md`（约 226–238 行）说明：将 `skills/` 目录下的 `.md` 文件复制到 Claude Code 全局命令目录，然后在 Claude Code 中以 slash command 调用：

```bash
cp ai-berkshire/skills/*.md ~/.claude/commands/
```

Skill 在执行时会按需调用 `tools/` 下的脚本（见下）以及 Claude Code 内置工具（`WebSearch` 在 skills 中被引用约 14 次，`WebFetch` 约 2 次——这是 Skill 获取外部数据的主要途径）。Skill 定义文件多为纯标题 + 正文的 Markdown，未发现 `allowed-tools` 之类的 frontmatter 元数据。

### Python 工具的运行

工具均为命令行脚本，由 Skill 在执行过程中自动调用，也可手动运行。各脚本入口：

- `tools/financial_rigor.py` — 金融数据严谨性验证（`argparse` 子命令：`verify-market-cap` / `verify-valuation` / `cross-validate` / `benford` / `calc` / `three-scenario`）。精确十进制运算（`decimal.Decimal`，`prec=28`，`ROUND_HALF_EVEN`）。**被 Skill 引用最多（约 23 处）**。
- `tools/report_audit.py` — 研究报告数据抽检（`extract` / `verdict` 子命令，从 Markdown 报告抽样 15% 财务数据点比对，1% 容差，FAIL 时非零退出码）。被 Skill 引用约 12 处。
- `tools/ashare_data.py` — A 股行情/财务（`quote` / `financials` / `valuation` / `search` 子命令）。
- `tools/stock_screener.py` — 动量发现 + 价值验证选股筛（无 argparse，直接读 `sys.argv`；交互式 `--update` 录入基本面）。
- `tools/morningstar_fair_value.py` — 抓取 Morningstar 筛选器，输出潜在涨幅 Top 100，落盘 CSV 到 `data/`。
- `tools/momentum_backtest.py` / `tools/momentum_backtest_v2.py` — 动量+价值回测（NVDA/AMD/MU），基本面数据硬编码在脚本内（`FUNDAMENTALS` 字典）。
- `tools/xueqiu_scraper.py` — 雪球用户时间线爬虫（Playwright，`asyncio`）。

### 数据文件（脚本读写，非配置）

`data/` 目录被 `stock_screener.py` 与 `morningstar_fair_value.py` 读写：

- `data/watchlist.json` — 选股观察列表（按市场分组：`us_ai_chip` / `us_ai_app` / `us_ai_infra` / `us_crypto` / `hk_internet` / `a_share`）。`stock_screener.py` 首次运行会用内置 `DEFAULT_WATCHLIST` 生成它。
- `data/fundamentals.json` — 手工维护的季度基本面数据（营收同比、毛利率、EPS 超预期）。
- `data/morningstar_fair_value_20260519.csv`、`data/correlation_3stocks_*.csv`、`data/cross_asset_10y_*.csv` — 工具产出/数据快照。

### Hook 与日志

- `tools/log-command.sh` 由 Claude Code 的 **`user_prompt_submit` hook** 调用（脚本注释明示），从 stdin 读取用户指令，追加写入 `~/ai-berkshire/logs/command-log.jsonl`（JSONL 格式），并维护 `logs/.counter` 计数器，每 10 条提示运行 `/command-log`。**注意：实际的 hook 注册配置（settings.json）不在本仓库内**——脚本是 hook 的执行体，注册需在用户的 Claude Code 设置中完成。
- `.gitignore` 排除 `logs/command-log.jsonl`、`*/command-log.jsonl`、`.DS_Store`，以及雪球登录态缓存 `/tmp/xueqiu_state.json`（含 cookies，本地使用）。

## 编码与字符集细节

- `ashare_data.py` 处理腾讯行情 API 的 **GBK** 编码（先尝试 UTF-8，失败回退 GBK）。
- 多处脚本写文件用 `encoding="utf-8"`、`ensure_ascii=False`（中文内容）。
- 报告与文档全部为中文。
