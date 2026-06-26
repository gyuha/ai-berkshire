---
last_mapped_commit: 4f7aec20fe95c4de306943808c2c22ce404a8148
mapped: 2026-06-27
---

# TESTING — 测试与验证

## 结论先行：本仓库无自动化测试套件

**实测确认：仓库中不存在任何自动化测试。** 具体证据：

- 无 `test_*.py` / `*_test.py` 文件，无 `conftest.py`。
- 无任何 Python 文件包含 `import pytest`、`import unittest`、`def test_`、`class Test`（全仓库 grep 0 命中）。
- 无 `pytest.ini` / `tox.ini` / `pyproject.toml` / `setup.py` / `setup.cfg` / `requirements*.txt` / `Makefile`。
- 无 `.github/workflows/`（无 CI/CD）。
- `tools/momentum_backtest.py` 与 `tools/momentum_backtest_v2.py` 文件名含 "test" 仅因 backtest 一词，**不含任何测试函数**，它们是回测脚本而非测试。

因此本项目**不靠单元测试保证质量**。质量由下述"程序化数据校验 + 人工准出门 + 多源交叉验证"三层机制承担——这是本项目实际意义上的"测试体系"。

---

## 第一层：程序化数据校验 —— `tools/financial_rigor.py`

报告生成过程中，所有涉及计算的数据点必须通过该工具验算，杜绝 LLM 心算误差。它是 stdlib-only、用 `Decimal`（`Context(prec=28, rounding=ROUND_HALF_EVEN)`）做精确十进制运算，**无浮点漂移**。

提供的校验子命令（`tools/financial_rigor.py` 第 380-423 行的子解析器）：

| 子命令 | 验证内容 | 判定阈值 |
|--------|---------|---------|
| `verify-market-cap` | 市值 = 股价 × 总股本，对比报告市值 | 偏差 >5% → ❌；1-5% → ⚠️；≤1% → ✅（第 80-91 行）|
| `verify-valuation` | PE / PB / ROE / FCF Yield / 股息率 / PS 精确验算 | 仅计算并输出，无 pass/fail |
| `cross-validate` | 多源数据取中位数，逐源算偏差 | 默认容差 `tolerance_pct=2.0`，超出标 ❌（第 167、189 行）|
| `benford` | Benford 定律首位数字分布（造假快筛）| MAD <0.015 视为符合；样本 <50 判不可靠（第 231、248-255、274 行）|
| `calc` | 安全四则运算精确计算器 | 白名单字符集 + 受限 `eval`（第 298-305 行）|
| `three-scenario` | 三情景（乐观/中性/悲观）目标价精确推算 | 仅计算输出 |

调用约定（见 `skills/investment-research.md` 第 66-92 行、`skills/investment-team.md` 第 64-69 行、`skills/earnings-review.md` 第 78-92 行）：
- **强制用 Bash 调用，禁止 LLM 心算**（"所有涉及计算的数据必须通过工具验算"）。
- 工具输出直接嵌入报告附录"关键数据交叉验证记录"。
- 若工具报 ❌ 偏差过大，必须排查原因后才能继续分析。

注意：各 skill 文档中 `verify-valuation` / `cross-validate` 的示例参数写法略有出入（如 `skills/earnings-review.md` 第 82-83 行用 `--metric/--values/--sources`，而实际工具 `cross-validate` 的参数是 `--field/--values/--unit/--tolerance`，见 `tools/financial_rigor.py` 第 399-403 行）。**以工具的 argparse 定义为准**——文档示例存在小幅漂移。

---

## 第二层：报告数据抽检（准出/打回门）—— `tools/report_audit.py`

报告写入文件后，**必须**执行数据抽检，通过方可发布（"准出流程"，见 `skills/investment-research.md` 第 211-236 行、`skills/investment-team.md` 第 183-198 行、`skills/earnings-review.md` 第 193-210 行）。这是项目里最接近"集成测试/验收门"的机制。

三步流程：

1. **extract** —— 从 Markdown 报告中正则提取所有财务数据点（多列表格 / KV 冒号行 / 加粗数字，见 `report_audit.py` 第 155-226 行），随机抽样 **15%**（`sample_points`，第 229-236 行：最少 3 个、最多 30 个）。
   ```bash
   python3 tools/report_audit.py extract --report reports/xxx.md
   ```
2. **取数核验** —— Claude 对抽检清单每项按 `skills/financial-data.md` 规范从可靠信源（macrotrends / stockanalysis / aastocks / 东方财富 / 巨潮）取数，填入 `fetched_value` / `fetched_source`（及可选第二源 `fetched_value2`）。
3. **verdict** —— 输出准出/打回判决：
   ```bash
   python3 tools/report_audit.py verdict --results '<填好的JSON>' --report <报告文件名>
   ```

判定逻辑（`report_audit.py` 第 243-386 行）：
- 容差 `_TOLERANCE = 0.01`（**1%**，第 243 行）。
- **【准出 PASS】** 所有抽检点偏差 ≤ 1% → 报告可发布。
- **【打回 FAIL】** 任意点偏差 > 1% → 列出打回原因，报告需修正后重审（直到准出）。
- 两来源彼此不一致（>1%）会单独标 ⚠️ 警告（可能 GAAP/Non-GAAP 或汇率口径差异，需人工复核）。
- **退出码即门禁信号**：PASS 返回 0、FAIL 返回非 0（第 514 行 `sys.exit(0 if outcome['verdict'] == 'PASS' else 1)`，注释明确"方便 CI/脚本判断"）。

---

## 第三层：多源人工交叉验证 —— `skills/financial-data.md`

最底层、贯穿全程的验证纪律（非工具，是写作规范，但实际承担"数据正确性测试"的角色）：

- **每个关键财务数据必须来自两个独立来源**，误差 >1% 须标记（`skills/financial-data.md` 第 3 行）。
- 误差分级：≤1% ✅ 取主源；1-5% ⚠️ 标差异；>5% ❌ 查原始财报，不得直接使用（第 46-50 行）。
- 必须人工验证的高风险数据点（`skills/investment-research.md` 第 59-65 行）：总股本、股价/市值（手算 `股价×总股本` 防单位错误）、最近财年收入/净利润、现金储备/净现金、管理层持股（区分经济权益 vs 投票权、AB 股结构）。
- 未上市公司单一来源时，数据前标 `[估计]`，不做交叉验证（第 87 行）。

---

## 测试相关的"框架/工具/Mock/覆盖率"实情

| 维度 | 实情 |
|------|------|
| 测试框架 | **无**（无 pytest/unittest）|
| 测试目录结构 | **无**（无 `tests/` 目录、无 test 文件）|
| Mock | **无**（无 mocking 库、无 fixture）|
| 覆盖率工具 | **无**（无 coverage / `.coveragerc`）|
| CI | **无**（无 `.github/workflows/`）|
| 工具自检 | 工具内置**校验阈值**作为运行期断言（`financial_rigor.py` 偏差 1%/5% 档；`report_audit.py` 1% 容差 + 非零退出码），但**这些是数据正确性门，不是代码单元测试** |
| 手动运行入口 | 各工具 `if __name__ == "__main__": main()`，靠人/skill 用 CLI 子命令手动调用验证；无自动化触发 |

---

## 如何"验证"一次改动（实践指引）

由于无测试套件，验证一次工具或 skill 改动只能手动跑：

- 改了 `tools/financial_rigor.py`：用 docstring 里的示例（第 10-15 行）手动跑各子命令，肉眼核对输出与已知正确值。例：
  ```bash
  python3 tools/financial_rigor.py verify-market-cap --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD
  python3 tools/financial_rigor.py calc --expr '510 * 9.11e9'
  ```
- 改了 `tools/report_audit.py`：对一份既有报告跑 `extract`（可加 `--dry-run` 仅提取不验证，见 docstring 第 20-21 行），确认数据点识别正确，再造一组 `results` JSON 跑 `verdict`，确认准出/打回判决与退出码符合预期。
- 改了某个 `skills/*.md`：无自动校验，靠跑一遍该 skill 流程、人工对照 `CLAUDE.md` 的核心原则与命名/目录规范确认。
- 改了报告本身：必走第二层准出门（`report_audit.py extract → 取数 → verdict`），偏差 >1% 即打回。

**底线**：本项目把"测试"前移成了"数据校验 + 准出门"。没有红/绿测试灯——绿灯等价于 `verdict` 返回 PASS（退出码 0）且双来源误差 ≤1%。
