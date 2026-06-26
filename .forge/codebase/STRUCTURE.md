---
last_mapped_commit: 4f7aec20fe95c4de306943808c2c22ce404a8148
mapped: 2026-06-27
---

# 目录结构与命名规范 — AI Berkshire

## 顶层布局

```
ai-berkshire/
├── CLAUDE.md              — 项目级最高优先级指令（结构/命名/原则/风格）
├── ai_CLAUDE.md           — AI 记忆文件（用户画像/演进史/历史教训）
├── README.md / README_EN.md — 开源项目介绍（中/英）
├── LICENSE
├── .gitignore
├── skills/                — 17 个 Skill 定义（.md），复制到 ~/.claude/commands/ 使用
├── tools/                 — 8 个 Python 工具 + 1 个 shell 钩子脚本
├── data/                  — 共享数据集（自选股/基本面/估值/相关性）
├── docs/                  — 路线图与研究随笔
├── assets/                — 架构图、收益截图、公众号配图
├── logs/                  — 命令日志（内容被 gitignore）
├── reports/               — 投研报告输出（约 111 子目录 / 2083 个 .md）
├── 实盘记录/               — 实盘操作记录与镜子测试
├── 筛选公司/               — 筛选/召回池报告（与 reports/ 平行的另一组）
├── RKLB-investment-research.md      — 顶层散落报告（未归入 reports/）
└── sailis-touzi-yanjiu-baogao.md    — 顶层散落报告（赛轮，未归入 reports/）
```

## skills/ — Skill 定义

每个 `.md` 即一个斜杠命令（命令名 = 文件名去掉 `.md`）。完整 17 个文件：

```
skills/bottleneck-hunter.md          skills/management-deep-dive.md
skills/deep-company-series.md        skills/news-pulse.md
skills/dyp-ask.md                    skills/portfolio-review.md
skills/earnings-review.md            skills/private-company-research.md
skills/earnings-team.md              skills/quality-screen.md
skills/financial-data.md             skills/thesis-tracker.md
skills/industry-funnel.md            skills/wechat-article.md
skills/industry-research.md          skills/investment-checklist.md
skills/investment-research.md        skills/investment-team.md
```

注意：`skills/financial-data.md` 是数据取数**规范文档**，被其它 Skill 引用，不作为独立命令运行。

## tools/ — 辅助工具

```
tools/financial_rigor.py       — 十进制精确计算/防造假（CLAUDE.md 强制使用）
tools/report_audit.py          — 报告数据准出抽检（extract / verdict）
tools/ashare_data.py           — A股行情与财务（quote/financials/valuation/search）
tools/xueqiu_scraper.py        — 雪球大V时间线抓取（依赖 playwright）
tools/stock_screener.py        — 动量+价值两层筛选
tools/morningstar_fair_value.py— 晨星公允价值抓取（输出 CSV 到 data/）
tools/momentum_backtest.py     — NVDA/AMD/MU 动量回测（旧版）
tools/momentum_backtest_v2.py  — 动量回测 v2（手录数据）
tools/log-command.sh           — user_prompt_submit 钩子，记录 prompt 到 logs/
```

除 `xueqiu_scraper.py`（playwright）外，核心工具仅依赖 Python 标准库。

## data/ — 共享数据集

```
data/watchlist.json                       — 分类自选股池（us_ai_chip/us_ai_app/hk_internet 等）
data/fundamentals.json                    — NVDA/AMD/MU 季度基本面（供筛选/回测）
data/morningstar_fair_value_20260519.csv  — 晨星公允价值导出（带日期）
data/correlation_3stocks_2021-2026.csv    — 腾讯/美团/PDD 周相关性
data/cross_asset_10y_2016-2026.csv        — 10 年跨资产价格序列（美股巨头+白酒）
```

## docs/ 与 assets/

```
docs/ROADMAP.md                  — P0/P1/P2 三阶段路线图
docs/大模型的下一战：多模态…md     — 研究随笔

assets/architecture.mmd          — 架构图 Mermaid 源
assets/architecture.png          — 架构图渲染
assets/2024-returns.jpg          — 收益截图
assets/2025-returns.jpg          — 收益截图
assets/kelly/                    — 凯利公式公众号配图（fig1~fig3）
assets/opd/                      — OPD 论文配图（fig1~fig6）
```

公众号配图约定（见 `wechat-article.md`）：按主题简称建子目录，文件名形如 `assets/{主题简称}/fig{N}-{描述}.png`，`assets/kelly/` 与 `assets/opd/` 即两个实例。

## reports/ — 报告输出（核心约定）

### 目录组织原则

`CLAUDE.md` 规定：所有报告**按公司名建文件夹**，该公司的所有报告都放进对应文件夹；行业/漏斗/组合/多公司对比类报告放 `reports/` 根目录。

```
reports/
├── AI产业研究/              — AI 产业链全景研究（置顶子目录）
├── 腾讯/                    — 单公司所有报告（research/earnings/management/thesis/...）
│   └── 《看懂腾讯》/         — deep-company-series 的 8 篇系列（00~08）
├── 拼多多/  泡泡玛特/  阿里巴巴/ ...  — 约 111 个公司/主题子目录
├── bottleneck-map/         — bottleneck-hunter 输出，按日期建子目录
│   └── 2026-06-26/         — 每日滚动扫描结果
├── 核电-industry-20260409.md       — 行业报告（根目录）
├── AI算力-funnel-20260509.md       — 漏斗筛选报告（根目录）
├── AI-轮动判断-20260509.md         — 主题级综合判断（根目录）
├── portfolio-latest.md             — 组合报告（根目录，持续更新）
└── 多公司对比-checklist-20260408.md — 多公司报告（根目录）
```

### 报告命名规范表（来自 CLAUDE.md）

| Skill | 文件命名格式 | 示例 |
|------|---------|------|
| `/investment-team` | `{公司名}/` 目录内含 4 视角 + 最终报告 | `reports/拼多多/最终报告.md` |
| `/investment-research` | `{公司名}-research-{YYYYMMDD}.md` | `reports/腾讯/腾讯-research-20260408.md` |
| `/investment-checklist` | `{公司名}-checklist-{YYYYMMDD}.md` | `reports/腾讯/腾讯-checklist-20260408.md` |
| `/industry-research` | `{行业名}-industry-{YYYYMMDD}.md`（根目录） | `reports/核电-industry-20260409.md` |
| `/industry-funnel` | `{行业名}-funnel-{YYYYMMDD}.md`（根目录） | `reports/AI算力-funnel-20260509.md` |
| `/private-company-research` | `{公司名}-private-{YYYYMMDD}.md` | `reports/字节跳动/字节跳动-private-20260408.md` |
| `/earnings-review` | `{公司名}-earnings-{期间}.md` | `reports/腾讯/腾讯-earnings-2025Q4.md` |
| `/earnings-team` | `{公司名}/` 目录内含 4 大师视角+研究底稿+公众号文章+读者评审 | `reports/腾讯/腾讯-earnings-2025Q4.md`（公众号定稿） |
| `/thesis-tracker` | `{公司名}-thesis.md`（长期维护） | `reports/腾讯/腾讯-thesis.md` |
| `/portfolio-review` | `portfolio-latest.md`（根目录，持续更新） | `reports/portfolio-latest.md` |
| `/management-deep-dive` | `{公司名}-management-{YYYYMMDD}.md` | `reports/腾讯/腾讯-management-20260409.md` |

### /investment-team 公司目录的标准内部结构

```
reports/{公司名}/
├── README.md                         — 研究框架概览 + 核心结论
├── 01-商业模式分析-段永平视角.md
├── 02-财务估值分析-巴菲特视角.md
├── 03-行业竞争分析-芒格视角.md
├── 04-风险管理层评估-李录视角.md
└── 最终报告.md                       — Team Lead 综合报告
```

实际编号方案可随公司扩展（例如 `reports/蚂蚁数科-team-20260417/` 含 01~07 多个分析文件 + README + 最终报告）。

### 实际落盘 vs 规范的偏差（高 / 实测）

规范是理想约定，实际 `reports/` 树更宽松，映射时需注意：

1. **`investment-team` 输出有两种落法**：既有直接 `reports/{公司名}/`（如 `reports/腾讯/`、`reports/拼多多/`），也有带 `-team-{日期}` 后缀的目录（如 `reports/蚂蚁数科-team-20260417/`、`reports/思格新能-team-20260409/`、`reports/灵境万维-team-20260512/`）。
2. **`-research-` 文件绝大多数在公司子目录内**（48 个），仅少数散在根目录（5 个）；与规范一致的占多数。
3. **`-private-` 文件落点不一致**：既有在公司目录内（`reports/蚂蚁数科/蚂蚁数科-private-20260511.md`），也有直接在根目录（`reports/思格新能-private-20260409.md`、`reports/群核科技-private-20260409.md`、`reports/长光辰芯-private-20260409.md`）。
4. **存在大量规范表未列出的报告类型**：如 `-valuation-`、`-news-`、`-team-`、对比类（`腾讯vs阿里-护城河与估值深度对比-…md`）、专题类（`贵州茅台DCF估值研究-…md`）、deepseek 分析子目录（`reports/百度-deepseek分析/`）等。命名风格不统一（中英混杂、有无日期不一）。
5. **顶层散落报告**：`RKLB-investment-research.md`、`sailis-touzi-yanjiu-baogao.md` 直接在仓库根，未归入 `reports/`。
6. **平行报告目录**：`筛选公司/`（含 `A股召回池/`、`科创板股召回池/` 等子目录及筛选报告）与 `实盘记录/`（实盘操作 + 镜子测试）与 `reports/` 平级，不在 `reports/` 内。

### 其它命名约定（散见各 Skill）

- `bottleneck-hunter`：`reports/bottleneck-map/{趋势名}-bottleneck-{YYYYMMDD}.md`，以及按日期滚动的 `reports/bottleneck-map/YYYY-MM-DD/HH-MM-{codes}.md`。
- `deep-company-series`：`reports/{公司名}/《看懂{公司名}》/0X-标题.md`（8 篇 + `00-系列说明.md`）。
- `wechat-article`：`reports/[AI产业研究/ 或 {公司名}/]公众号-{主题}-{YYYYMMDD}.md`，配图入 `assets/{主题简称}/fig{N}-…png`。
- 日期格式统一为 `YYYYMMDD`；报告内容统一中文。

## logs/ 与 .gitignore

```
logs/.gitignore          — 仅忽略 .counter（命令计数）
```

根 `.gitignore` 忽略：`logs/command-log.jsonl`、`reports/.DS_Store`、`reports/美团/command-log.jsonl`、`/tmp/xueqiu_state.json`。即命令日志与雪球登录态不入库。
