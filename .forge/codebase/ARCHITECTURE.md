---
last_mapped_commit: 4f7aec20fe95c4de306943808c2c22ce404a8148
mapped: 2026-06-27
---

# 架构总览 — AI Berkshire

## 项目本质

这不是传统软件项目，而是一套**基于 Claude Code 的价值投资研究 Skill 合集**。没有可运行的应用主程序、没有服务器、没有构建系统。核心制品是一批 Markdown 格式的 Skill 定义和一批辅助 Python 工具脚本。「执行」发生在 Claude Code 会话内：用户输入斜杠命令（如 `/investment-team 拼多多`），Claude 读取对应 Skill 的 `.md` 流程定义并按其指令编排子 Agent、调用工具、产出报告。

四大师方法论框架是贯穿全项目的组织主线：**巴菲特**（财务估值/护城河/资本配置）、**芒格**（行业竞争/逆向思维）、**段永平**（商业模式/好生意标准）、**李录**（风险/管理层/长期确定性）。

## 三层架构

数据流向：用户斜杠命令 → Skill 编排逻辑 → 多 Agent 并行 + 工具/数据层 → 结构化报告写入 `reports/`。

```
用户(一个人 + Claude)
        │  斜杠命令 /investment-team ...
        ▼
┌─────────────────────────────────────────────┐
│ 第1层  Skill 入口层  (skills/*.md)            │  ← 流程定义/提示词
└─────────────────────────────────────────────┘
        │  Skill 编排：TeamCreate / TaskCreate / Task(并行)
        ▼
┌─────────────────────────────────────────────┐
│ 第2层  多Agent 并行核心  (四大师视角对抗)      │  ← Claude 子Agent运行时
│   Team Lead ──┬── 段永平视角(商业模式)          │
│               ├── 巴菲特视角(财务估值)          │
│               ├── 芒格视角(行业竞争)            │
│               └── 李录视角(风险管理层)          │
└─────────────────────────────────────────────┘
        │  调用
        ▼
┌─────────────────────────────────────────────┐
│ 第3层  工具与数据层  (tools/*.py, data/*)      │  ← 确定性计算/检索/抽检
│   financial_rigor.py · report_audit.py        │
│   WebSearch/WebFetch · xueqiu_scraper.py 等    │
└─────────────────────────────────────────────┘
        │  写入
        ▼
   结构化研究报告  reports/{公司}/*.md
```

该图的权威来源是 `assets/architecture.mmd`（Mermaid 源）与渲染图 `assets/architecture.png`。

## 第1层：Skill 入口层

- 位置：`skills/`，共 17 个 `.md` 文件，每个文件即一个斜杠命令（`/` + 去掉 `.md` 的文件名）。
- 使用方式（见 `CLAUDE.md`）：这些 `.md` 复制到 `~/.claude/commands/` 后由 Claude Code 识别为命令。仓库内的 `skills/` 是源，`~/.claude/commands/` 是运行副本。
- Skill 文件内容 = 给 Claude 的执行流程说明：分步骤的中文指令，规定要创建哪些 Agent、每个 Agent 的 prompt 模板、要调用哪些 `tools/*.py`、最终报告结构、输出文件路径与命名。
- `skills/financial-data.md` 是**规范文档而非可执行 Skill**：定义各市场（美股/港股/A股）的财务数据取数来源与两源交叉验证规则，被其它 Skill 的 Agent prompt 引用。

### 17 个 Skill 的分类与运行模态

| Skill (`/命令`) | 用途 | 大师视角 | 并行模态 |
|---|---|---|---|
| `investment-team` | 单公司四角色团队深研 | 四大师全 | 4 Agent 并行 → Team Lead 汇总 |
| `investment-research` | 单公司 7 模块综合框架 | 四大师全 | Task 并行取数 → 7 模块串行 |
| `investment-checklist` | 巴菲特买入前 6 关清单 + 镜子测试 | 巴菲特/段永平 | 多公司取数并行 → 逐公司串行 |
| `earnings-review` | 单 Agent 财报精读 | 巴菲特/李录/段永平 | 单线程 |
| `earnings-team` | 四大师并行财报分析 → 公众号文章 | 四大师全 | 4 Agent 并行 → 编辑+读者评审并行 |
| `industry-research` | 产业链全景 + 全市场公司扫描 | 四大师全 | Task 并行检索 → 串行 |
| `industry-funnel` | 全市场漏斗筛选至 3 只 | 四大师全 | 1-2 层并行 → 3-4 层串行 |
| `private-company-research` | 未上市公司 6 Agent 研究 + 去偏协议 | 四大师全 | 6 Agent 并行 → 交叉验证 → 汇总 |
| `management-deep-dive` | CEO 品格与资本配置深挖 | 巴菲特/段永平/李录 | Task 并行取数 → 串行综合 |
| `news-pulse` | 股价异动 10 分钟归因 | 段永平/巴菲特 | 4 Agent 并行 → Team Lead 综合 |
| `portfolio-review` | 组合健康体检 | 巴菲特/李录/段永平 | Task 并行取数 → 串行 |
| `thesis-tracker` | 买入后投资论点季度跟踪 | 李录/巴菲特/段永平 | 单线程（读→验→追加） |
| `bottleneck-hunter` | 供应链瓶颈套利扫描 | 段永平/芒格 | 单线程 |
| `quality-screen` | 7 指标一流公司快筛 | 巴菲特 | 单线程逐公司 |
| `deep-company-series` | 单公司 8 篇深度系列（公众号） | 四大师全 | 串行写 01→08 → 并行一致性扫描 |
| `wechat-article` | 公众号文章生产流水线 | 写作为主 | 研究/编辑/读者 Agent 并行 |
| `dyp-ask` | 以段永平口吻第一人称答疑（非研究） | 段永平 | 单线程对话，无文件输出 |

## 第2层：多 Agent 并行核心（四大师对抗）

这是项目的方法论灵魂，最典型实现是 `skills/investment-team.md`：

1. **团队创建**：`TeamCreate` 建团队（`team_name` 形如 `{公司名}-research`，英文小写），agent_type 为 `team-lead`。
2. **任务创建**：`TaskCreate` 建 4 个任务，分别对应 4 个分析维度。
3. **并行启动**：在**同一条消息中**用 `Task` 工具并行启动 4 个 `general-purpose` 子 Agent（`run_in_background: true`），每个绑定到团队并命名为 `business-analyst` / `financial-analyst` / `industry-researcher` / `risk-assessor`。
4. **角色 ↔ 大师映射**（固定约定）：
   - 商业模式 & 护城河 → **段永平视角**（business-analyst）
   - 财务报表 & 估值 → **巴菲特视角**（financial-analyst）
   - 行业格局 & 竞争 → **芒格视角**（industry-researcher）
   - 风险 & 管理层 → **李录视角**（risk-assessor）
5. **汇报机制**：子 Agent 用 `SendMessage`（type `message`，recipient `team-lead`）把报告发回 Team Lead——**是消息通信，不是文件协作**。
6. **收口**：Team Lead 收齐 4 份后发 `shutdown_request` 关闭成员，综合产出最终报告，`TeamDelete` 清理团队。

`earnings-team`、`news-pulse`、`private-company-research` 采用同构模式（分别为 4/4/6 个并行 Agent）。其余 Skill 多为「并行取数 + 串行分析」或纯单线程。

### Skill 之间的关系

- **investment-team → 子视角文件 → 最终报告**：一次 `investment-team` 运行产出一个公司目录，内含 4 个分视角 `.md`（`01-商业模式分析-段永平视角.md` … `04-风险管理层评估-李录视角.md`）+ `README.md` + `最终报告.md`。最终报告由 Team Lead 综合 4 份子视角而成。
- **数据规范被复用**：`financial-data.md` 的取数/交叉验证规则被多个 Skill 的 Agent prompt 直接引用。
- **内容生产链**：`earnings-team` 与 `deep-company-series` / `wechat-article` 衔接——研究底稿经编辑 + 读者评审 Agent 处理后产出公众号定稿。
- **跟踪闭环**：`investment-team`/`investment-research`（建仓研究）→ `thesis-tracker`（买入后论点跟踪，追加式日志）→ `portfolio-review`（组合层复盘）。

## 第3层：工具与数据层

工具是 Skill 流程中被 `Bash` 调用的确定性组件，弥补 LLM 不擅长精确算术与事实核验的短板。全部位于 `tools/`，核心工具仅用 Python 标准库（无第三方依赖），`xueqiu_scraper.py` 例外（依赖 `playwright`）。

| 工具 | 角色 | 关键子命令 |
|---|---|---|
| `tools/financial_rigor.py` | 十进制精确计算与防造假（被 CLAUDE.md 列为强制） | `verify-market-cap` / `verify-valuation` / `cross-validate` / `benford` / `calc` / `three-scenario` |
| `tools/report_audit.py` | 报告数据准出抽检（15% 随机抽样 → 判决 PASS/FAIL） | `extract` / `verdict` |
| `tools/ashare_data.py` | A 股实时行情与财务（腾讯 API + 东方财富抓取） | `quote` / `financials` / `valuation` / `search` |
| `tools/xueqiu_scraper.py` | 雪球大 V 时间线抓取（Playwright，可持久化登录态） | `--user-id` / `--keywords` / `--output` 等 |
| `tools/stock_screener.py` | 动量发现 + 价值打分两层筛选 | 无子命令；位置参数为 ticker，`--update` |
| `tools/morningstar_fair_value.py` | 抓 Morningstar 公允价值，按低估幅度排序 | 无 CLI 参数，输出 CSV 到 `data/` |
| `tools/momentum_backtest.py` / `_v2.py` | NVDA/AMD/MU 动量+价值回测 | 无 CLI 参数，独立脚本 |
| `tools/log-command.sh` | `user_prompt_submit` 钩子，记录用户 prompt 到 `logs/command-log.jsonl` | 读 stdin → 追加 JSONL |

数据层 `data/`：`watchlist.json`（分类自选股池）、`fundamentals.json`（NVDA/AMD/MU 季度基本面，供回测/筛选）、`morningstar_fair_value_20260519.csv`（晨星公允价值导出）、`correlation_3stocks_2021-2026.csv`、`cross_asset_10y_2016-2026.csv`（相关性/跨资产价格序列）。

`financial_rigor.py` 与 `report_audit.py` 是被 Skill 流程显式编排的两个工具：前者在「财务与估值」环节强制调用（禁止心算），后者在报告产出后作为「准出流程」抽检。

## 报告产出流程（数据流终点）

Skill 执行的终点是把结构化报告写入 `reports/`：

- 单公司类（research/earnings/management/thesis/private 等）写入 `reports/{公司名}/`。
- 行业/漏斗/组合/多公司对比类写入 `reports/` 根目录。
- `investment-team` 产出一个完整公司子目录（README + 4 视角 + 最终报告）。
- `bottleneck-hunter` 写入 `reports/bottleneck-map/`，按日期建子目录（如 `reports/bottleneck-map/2026-06-26/`），用于持续滚动扫描。
- `deep-company-series` 在公司目录下建书名号子目录（如 `reports/腾讯/《看懂腾讯》/`，内含 `00-系列说明.md` 到 `08-…md`）。

实测产出规模：`reports/` 下约 111 个公司/主题子目录、2083 个 `.md` 文件。命名与落盘的实际情况与 `CLAUDE.md` 规范存在偏差，详见 `STRUCTURE.md`。

## 入口与配置文件

- `CLAUDE.md` — 项目级指令：项目结构、报告目录约定、命名规范表、投研核心原则、报告风格、GitHub 操作流程、强制手算/工具校验规则。这是约束所有 Skill 行为的最高优先级文档。
- `ai_CLAUDE.md` — AI 记忆文件：记录用户画像、偏好、项目演进历史与历史决策教训，供后续会话参考（非执行指令）。
- `README.md` / `README_EN.md` — 面向开源用户的项目介绍（中/英）。
- `docs/ROADMAP.md` — 三阶段路线图（P0 A股数据源、P1 HTML 报告/多深度模式/跨股对比、P2 测试覆盖）。
- `assets/architecture.mmd` + `architecture.png` — 架构图源与渲染。
- `LICENSE` — 开源许可。
- `.gitignore` — 忽略 `logs/command-log.jsonl`、`reports/.DS_Store`、`reports/美团/command-log.jsonl`、`/tmp/xueqiu_state.json`。
