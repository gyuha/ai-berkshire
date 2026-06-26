---
last_mapped_commit: 4f7aec20fe95c4de306943808c2c22ce404a8148
mapped: 2026-06-27
---

# CONVENTIONS — 编码与内容规范

本仓库不是常规软件项目，而是一套基于 Claude Code 的价值投资研究 Skill 合集。因此"规范"以**写作/报告规范**为主、辅助 Python 工具的**代码规范**为辅。所有规范的权威来源是 `CLAUDE.md`（项目根），以及 `skills/*.md` 与 `tools/*.py` 中的实际落地。

---

## 1. 投研分析核心原则（最高优先级）

权威定义在 `CLAUDE.md` 第 68-76 行（"投研分析核心原则（最高优先级）"），所有 skill 执行时强制遵守：

- **客观、客观、客观** —— 所有分析必须基于事实和数据，严禁主观臆断。
- **严格区分"事实"与"观点"** —— 事实用数据支撑；观点必须明确标注为"观点"或"推测"。
- **不预设立场** —— 不预设看多/看空，先摆数据、再推逻辑、最后得结论；结论必须从数据中自然推出。
- **禁止主观表述** —— 不用"我认为""我觉得""显然"，改用"数据显示""证据表明""根据XX来源"。
- **呈现正反两面** —— 每个核心判断都必须附带反面论据（"但另一方面…"），让读者自行权衡。落地示例见 `skills/investment-team.md` 第 161-163 行的 `🟢 看多逻辑 / 🔴 看空逻辑` 双栏，以及 `skills/earnings-review.md` 第 182 行明确禁止"基本符合然后列一堆两面话"。
- **诚实留白** —— 对不确定的事情如实说"不确定"或"数据不足"，不用推测填充确定性（见 `skills/investment-team.md` 第 214 行"信息稀缺时的诚实原则"）。

延伸的"AI 研究偏见自觉"约定（见 `skills/investment-research.md` 第 9-33 行、`skills/investment-team.md` 第 19-32 行）：
- 报告开头必须给出**信息丰富度评级**（A 信息充裕 / B 信息适中 / C 信息稀缺）与"AI 研究局限性声明"。
- 报告结尾必须区分"**AI 分析置信度**"（取决于资料量）与"**投资确定性**"（取决于生意本质）。
- C 级（信息稀缺）公司：用第一性原理提问，报告末尾列"需要一手验证的问题清单"，不用框架伪装完整性。

---

## 2. 报告语言与风格

权威定义在 `CLAUDE.md` 第 78-85 行：

- **语言**：所有报告使用**中文**。
- **风格**：直接、犀利、不说废话。
- **数据来源**：数据必须标注来源；关键数据至少 **2 个独立来源交叉验证**。
- **估计值**：必须注明"估计"（`skills/financial-data.md` 第 87 行：未上市公司单一来源数据前标记 `[估计]`，不做交叉验证）。
- **评分**：使用 ★ 符号，范围 ★1-5，**不含半星**。实际落地见 `reports/portfolio-latest.md`、`reports/AI算力产业链全景研究-20260509.md` 等。
- **语录点评**：穿插巴菲特 / 芒格 / 段永平 / 李录的语录（用 Markdown 引用块 `>`），示例见 `skills/earnings-review.md` 第 9-11、116 行。
- **表格优先**：关键数据用 Markdown 表格呈现（贯穿所有 skill 的输出要求）。

---

## 3. 数据来源与交叉验证规范

权威定义在 `skills/financial-data.md`。核心规则：**每个关键数据必须来自两个独立来源，误差 >1% 须标记。**

数据源优先级（`skills/financial-data.md` 第 9-31 行）：

| 市场 | 主来源 | 副来源 | 一手原文 |
|------|--------|--------|----------|
| 美股 | macrotrends | stockanalysis | SEC EDGAR（10-K/10-Q）|
| 港股 | aastocks | macrotrends（ADR 代码，如腾讯 TCEHY）| HKEX 披露易 |
| A股 | 东方财富 | 巨潮资讯（cninfo）| 巨潮原始年报/季报 PDF |

误差分级处理（`skills/financial-data.md` 第 46-50 行）：
- ≤ 1%：✅ 一致，取来源1数值，标注两源。
- 1%~5%：⚠️ 标记"数据存在差异"，注明两数值与可能原因（汇率/会计口径）。
- \> 5%：❌ 标记"重大差异"，必须查原始财报核实，不得直接使用。

呈现格式（`skills/financial-data.md` 第 54-69 行）：每个关键数据下列出两个来源数值 + 误差百分比。常见差异原因（GAAP vs Non-GAAP、汇率、财年定义、合并口径、更新滞后）见第 73-81 行。

---

## 4. 市值手算校验规则

权威定义在 `CLAUDE.md` 第 108 行 + `skills/investment-research.md` 第 60-72 行：

- **市值必须手算校验**：`股价 × 总股本`，与报告市值对比。
- **禁止 LLM 心算**：所有涉及计算的数据必须通过 `tools/financial_rigor.py` 验算（`verify-market-cap` / `verify-valuation` / `cross-validate` / `three-scenario`）。
- 工具阈值（`tools/financial_rigor.py` 第 80-91 行）：偏差 >5% 报 ❌ 并提示排查（股本是否最新、单位是否一致、股价是否最新）；1%~5% 报 ⚠️；≤1% 报 ✅。
- 若工具报 ❌ 偏差过大，必须排查原因后才能继续分析。

---

## 5. 货币单位规则

权威定义在 `CLAUDE.md` 第 109 行：

- **货币单位要明确**（港币 / 人民币 / 美元），防止混淆。
- 常见错误（`skills/investment-research.md` 第 95-98 行）：市值单位港币亿 vs 人民币亿 vs 美元亿，容易漏写/多写一个零；FCF 口径（是否含租赁/收购）；债务口径（是否含经营租赁）；持股比例（AB 股经济权益 ≠ 投票权）。
- 工具 `financial_rigor.py` 的 `--currency` 参数贯穿 `verify-market-cap` / `verify-valuation` / `three-scenario`，用于在输出中显式标注币种。

---

## 6. 报告文件命名与目录规范

权威定义在 `CLAUDE.md` 第 17-66 行。

- **按公司名建文件夹**：公司相关的所有报告放在 `reports/{公司名}/` 下。
- 命名格式（`CLAUDE.md` 第 42-54 行命名表，逐字执行）：
  - `/investment-research` → `{公司名}-research-{YYYYMMDD}.md`
  - `/investment-checklist` → `{公司名}-checklist-{YYYYMMDD}.md`
  - `/industry-research` → `{行业名}-industry-{YYYYMMDD}.md`（根目录）
  - `/industry-funnel` → `{行业名}-funnel-{YYYYMMDD}.md`（根目录）
  - `/private-company-research` → `{公司名}-private-{YYYYMMDD}.md`
  - `/earnings-review` → `{公司名}-earnings-{期间}.md`
  - `/thesis-tracker` → `{公司名}-thesis.md`（长期维护）
  - `/portfolio-review` → `portfolio-latest.md`（根目录，持续更新）
  - `/management-deep-dive` → `{公司名}-management-{YYYYMMDD}.md`
- 行业/漏斗/主题级/组合/多公司报告放 `reports/` 根目录；公司报告放对应公司文件夹。
- `/investment-team` 目录结构固定（`CLAUDE.md` 第 56-66 行）：`README.md` + `01-商业模式分析-段永平视角.md` + `02-财务估值分析-巴菲特视角.md` + `03-行业竞争分析-芒格视角.md` + `04-风险管理层评估-李录视角.md` + `最终报告.md`。
- 日期格式统一 `YYYYMMDD`。

注意：部分 skill 内部示例把报告写到 `~/` 家目录（如 `skills/investment-research.md` 第 204 行、`skills/investment-team.md` 第 181 行），但 `CLAUDE.md` 的目录规范以 `reports/{公司名}/` 为准 —— 以 `CLAUDE.md` 优先。

---

## 7. Skill 定义（.md）的撰写规范

`skills/` 下共 18 个 skill 定义文件。复制到 `~/.claude/commands/` 后作为斜杠命令使用（`CLAUDE.md` 第 11 行）。

**结构惯例**（以 `skills/investment-research.md`、`skills/investment-team.md`、`skills/earnings-review.md` 为代表）：

1. **标题** —— 绝大多数 skill 第一行是 `# {中文标题}`（H1）。**唯一例外**：`skills/news-pulse.md` 第 1-4 行使用 YAML frontmatter（`name:` + `description:`）。新建 skill 时与目标命令体例对齐即可，两种都被接受。
2. **一句话任务** —— 紧跟标题，含占位符 `$ARGUMENTS`（用户输入），如 `对 $ARGUMENTS 进行系统化投资研究分析。`
3. **设计理念 / 适用场景**（可选）—— 说明为什么这样设计、何时用/不用（`skills/earnings-review.md` 第 12-21 行、`skills/news-pulse.md` 第 10-16 行）。
4. **执行流程** —— 编号步骤（第一步/第二步…），每步有明确动作与产出。
5. **大师追问** —— 每个分析模块末尾必须有对应大师（巴菲特/芒格/段永平/李录）的"追问"句（`skills/investment-research.md` 第 110、126、136、146、157、173 行）。
6. **工具调用块** —— 凡涉及计算/验证，内嵌 `bash` 代码块调用 `tools/financial_rigor.py` 或 `tools/report_audit.py`，并注明"禁止心算"。
7. **输出要求** —— 明列报告结构、保存路径、结论必须明确（不回避买入/观望/回避建议与价格区间）。
8. **数据抽检（准出流程）** —— 多数研究类 skill 末尾附 `report_audit.py extract → 取数核验 → verdict` 三步准出门。
9. **并行 Agent 约定** —— 团队类 skill（investment-team / earnings-team / private-company-research / news-pulse）要求"4 个 Agent 必须在同一条消息中并行启动"，通过 `SendMessage` 汇报、`shutdown_request` 关闭、`TeamDelete` 清理。

**语言**：所有 skill 正文用中文；表格、引用块（大师语录）、`bash` 代码块为标准 Markdown。

---

## 8. Python 工具（tools/*.py）代码规范

`tools/` 下 8 个 Python 工具 + 1 个 shell 脚本（`log-command.sh`）。

- **零外部依赖优先**：`financial_rigor.py`（第 7 行）、`report_audit.py`（第 7 行）、`ashare_data.py` 明确"仅用 Python stdlib"，要求 Python ≥ 3.7。常用 stdlib：`argparse`、`json`、`sys`、`os`、`decimal`、`math`、`re`、`datetime`。**唯一引入第三方依赖的文件**是 `tools/xueqiu_scraper.py`（用 `playwright`，雪球爬虫）。新工具应延续"零依赖、stdlib only"惯例。
- **精确十进制，禁止浮点**：金额/估值计算统一用 `decimal.Decimal` + `Context(prec=28, rounding=ROUND_HALF_EVEN)`（`financial_rigor.py` 第 28 行的 `_CTX`、`report_audit.py` 第 33 行）。`exact()`（`financial_rigor.py` 第 31-37 行）把任意数值先转 `str` 再转 `Decimal`，规避浮点陷阱。
- **文件头**：`#!/usr/bin/env python3` + 模块级 docstring（中文说明 + Usage 示例）。`xueqiu_scraper.py` 额外有 `# -*- coding: utf-8 -*-`。
- **CLI 结构**：`argparse` + `add_subparsers(dest="command")` 子命令模式；`def main()` 末尾 `if __name__ == "__main__": main()`（6 个工具均有 `__main__` guard）。
- **退出码约定**：`report_audit.py verdict`（第 514 行）准出返回 0、打回返回非 0，"方便 CI/脚本判断"。
- **输出风格**：中文 print，分隔线 `"=" * 60`，状态符号 `✅ / ⚠️ / ❌`，与报告中的标记体系一致。
- **凭据安全**：敏感凭据通过环境变量传入，不进代码仓库（`xueqiu_scraper.py` 第 15-18 行：`XQ_PHONE` / `XQ_PASSWORD`；登录态缓存 `/tmp/xueqiu_state.json` 已在 `.gitignore` 忽略）。
- **安全求值**：`financial_rigor.py` 的 `exact_calc`（第 298-305 行）用白名单字符集 + `eval(expr, {"__builtins__": {}}, {})` 限制表达式，仅允许数字与四则运算。

---

## 9. Git / GitHub 工作流规范

权威定义在 `CLAUDE.md` 第 87-104 行：

- **commit message 用中文**，描述清楚改了什么。实际历史一致（如 `瓶颈猎手扫描 2026-06-26（第304轮）：无新信号，更新LEU股价至$165.80`）。
- **推送前先 `git pull --rebase origin main`** —— 远程经常有新提交，必须 rebase 后再 push。
- **只推最终报告**，不推中间过程文件（如 `data_collection.md`）。
- 远程：`https://github.com/xbtlin/ai-berkshire.git`，本地克隆 `~/ai-berkshire/`。
- 报告写完后**主动询问是否推送到 GitHub**（`CLAUDE.md` 第 111 行）。
- `.gitignore` 忽略：`logs/command-log.jsonl`、各公司目录下 `command-log.jsonl`、`.DS_Store`、`/tmp/xueqiu_state.json`。

---

## 10. 速查清单

| 规范 | 权威位置 |
|------|---------|
| 投研核心原则（客观/事实vs观点/不预设/正反两面）| `CLAUDE.md` 68-76 |
| 报告语言风格（中文/犀利/★1-5不含半星/语录）| `CLAUDE.md` 78-85 |
| 双来源交叉验证（误差>1%标记）| `skills/financial-data.md` |
| 市值手算 股价×总股本 | `CLAUDE.md` 108；`tools/financial_rigor.py` 61-91 |
| 货币单位明确 | `CLAUDE.md` 109；`skills/investment-research.md` 95-98 |
| 报告命名/目录 | `CLAUDE.md` 17-66 |
| commit 中文 + pull --rebase | `CLAUDE.md` 87-104 |
| Python 零依赖 + Decimal 精确计算 | `tools/financial_rigor.py`、`tools/report_audit.py` |
