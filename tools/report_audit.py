#!/usr/bin/env python3
"""Report Audit Tool for AI Berkshire.

데이터 표본검사 도구: 연구 보고서에서 재무 데이터 포인트의 15%를 추출하여
신뢰할 수 있는 출처와 대조한다. 통과하면 발행 승인, 미통과 시 반려하고 사유를 명시한다.

Zero external dependencies — uses only Python stdlib.
Requires Python >= 3.7.

작업 흐름 (3단계):
  Step 1 — 데이터 포인트 추출, 15% 무작위 표본추출:
    python3 tools/report_audit.py extract --report reports/xxx.md

  Step 2 — Claude가 표본검사 목록의 각 데이터 포인트에 대해 신뢰할 수 있는 출처
            (macrotrends/stockanalysis/aastocks/eastmoney)에서 값을 가져와
            fetched_value에 입력

  Step 3 — 검증 결과 입력 후 발행 승인/반려 판정 출력:
    python3 tools/report_audit.py verdict --results '[...]'

  한 번에 완료 (추출+표본검사 목록 출력만, 네트워크 검증 없음):
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run
"""

import argparse
import json
import math
import os
import re
import sys
from decimal import Decimal, Context, ROUND_HALF_EVEN
from random import Random

_CTX = Context(prec=28, rounding=ROUND_HALF_EVEN)

# ---------------------------------------------------------------------------
# 데이터 포인트 추출: Markdown 보고서에서 재무 수치 인식
# ---------------------------------------------------------------------------

# 매칭 패턴: 숫자 + 단위, 앞에 컨텍스트 레이블 포함
# 예: 收入：1,239亿元、PE 18.8x、毛利率 56%、市值 ~$5,670亿
_PATTERNS = [
    # 백분율
    (r'([\d,，\.]+)\s*%',                        '%',    'percent'),
    # 억 위안/억 달러/억 홍콩달러
    (r'([\d,，\.]+)\s*亿(元|美元|港元|RMB|USD|HKD)?', '亿',    'hundred_million'),
    # 배수 PE/PB/PS
    (r'([\d,，\.]+)\s*[xX倍]',                   'x',    'multiple'),
    # 조(만억)
    (r'([\d,，\.]+)\s*万亿',                      '万亿', 'trillion'),
    # 달러 절대값 (B/T)
    (r'\$\s*([\d,，\.]+)\s*([BMT亿])',             '$',    'usd_abs'),
    # 순수 정수 (시가총액, 매출, 사용자 수 등, 표 | 안에 나타남)
    (r'\|\s*[~约]?\$?([\d,，\.]+)\s*\|',          '',     'table_num'),
]

_LABEL_RE = re.compile(
    r'(?P<label>[^\|\n：:]{2,25})[：:\s]+[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)

_TABLE_ROW_RE = re.compile(
    r'\|\s*(?P<label>[^|]{1,40})\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?\s*\|'
)


def _clean_num(s: str) -> float:
    """쉼표 및 중문 쉼표가 포함된 숫자 문자열을 float으로 변환한다."""
    s = s.replace(',', '').replace('，', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def _is_valid_label(label: str) -> bool:
    """레이블이 의미 있는 재무 필드명인지 판단하여 노이즈를 필터링한다."""
    label = label.strip()
    # 너무 짧음
    if len(label) < 2:
        return False
    # 순수 숫자 또는 순수 연도
    if re.fullmatch(r'[\d\s年季度Q]+', label):
        return False
    # 기호/마크다운 마커로 시작
    if re.match(r'^[+\-\*#\|~\$>_`]', label):
        return False
    # 마크다운 굵게/코드 마커 포함
    if '**' in label or '`' in label or '__' in label:
        return False
    # 레이블이 순수 증가율 기호만 포함 (예: +56%, -13% 단독 레이블)
    if re.fullmatch(r'[+\-]?\d+(\.\d+)?%', label):
        return False
    # 흔한 무의미 레이블
    _SKIP = {'来源', 'sources', 'source', '说明', '注意', '备注', '数据来源',
             'n/a', '—', '-', '/', '合计', 'total', '单位', '趋势'}
    if label.lower() in _SKIP:
        return False
    return True


# 2열 표 행: | 레이블 | 수치 단위 | (재무 보고서 KV 표 전용 설계)
_KV_TABLE_RE = re.compile(
    r'^\|\s*(?P<label>[^|*\n]{2,40}?)\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*'
    r'(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT亿])?\s*[\|（\(]'
)

# 레이블이 있는 KV 행: 레이블: 수치 단위
_KV_LABEL_RE = re.compile(
    r'(?P<label>[\u4e00-\u9fa5A-Za-z][^\|\n：:*]{1,30})[：:]\s*[~约]?\$?'
    r'(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)


def _parse_md_tables(lines: list) -> list:
    """Markdown 내 모든 표를 파싱하여 (row_label, col_header, value, unit, lineno, raw) 목록을 반환한다."""
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 헤더 행 감지 (| 포함 && 구분행 아님)
        if '|' in line and not re.match(r'^\|[\-\s\|:]+\|$', line):
            headers_raw = [h.strip().strip('*_').strip() for h in line.split('|')]
            headers_raw = [h for h in headers_raw if h]
            # 다음 행은 구분행이어야 함
            if i + 1 < len(lines) and re.match(r'^\|[\-\s\|:]+\|$', lines[i+1].strip()):
                i += 2  # 구분행 건너뜀
                # 데이터 행 읽기
                while i < len(lines):
                    dline = lines[i].strip()
                    if not dline or not dline.startswith('|'):
                        break
                    cells = [c.strip().strip('*_~').strip() for c in dline.split('|')]
                    cells = [c for c in cells if c != '']
                    if len(cells) < 2:
                        i += 1
                        continue
                    row_label = cells[0]
                    for col_idx, cell in enumerate(cells[1:], start=1):
                        col_header = headers_raw[col_idx] if col_idx < len(headers_raw) else f'列{col_idx}'
                        # cell에서 숫자+단위 추출
                        m = re.search(
                            r'[~约]?\$?([\d,，\.]+)\s*(亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?',
                            cell
                        )
                        if m:
                            val = _clean_num(m.group(1))
                            unit = (m.group(2) or '').strip()
                            if val and val != 0 and val < 1e15:
                                results.append((row_label, col_header, val, unit, i + 1, dline))
                    i += 1
                continue
        i += 1
    return results


def extract_data_points(md_text: str) -> list:
    """Markdown 보고서에서 인식 가능한 모든 재무 데이터 포인트를 추출한다.

    세 가지 구조를 커버한다:
      1. 다중 열 Markdown 표 (주요 출처): (행 레이블 + 열 헤더) → 수치
      2. 콜론이 있는 KV 행: 레이블: 수치 단위
      3. 굵게 표시된 숫자 행: **수치** 단위

    반환값 list of dict:
      {id, label, reported_value, unit, raw_text, line_number}
    """
    points = []
    seen = set()

    def _add(label, val, unit, lineno, raw):
        label = re.sub(r'[\*_`]+', '', label).strip()
        if not _is_valid_label(label):
            return
        if val is None or val == 0 or val > 1e15:
            return
        # 순수 연도/분기 필터링
        if re.fullmatch(r'(20\d{2}|Q[1-4]|\d{4}\s*Q[1-4])', label.strip()):
            return
        key = f"{label}|{round(val,4)}|{unit}"
        if key in seen:
            return
        seen.add(key)
        points.append({
            'id': len(points) + 1,
            'label': label,
            'reported_value': val,
            'unit': unit,
            'raw_text': raw[:120],
            'line_number': lineno,
        })

    lines = md_text.split('\n')
    in_code = False

    # --- 1. 다중 열 표 ---
    for row_label, col_header, val, unit, lineno, raw in _parse_md_tables(lines):
        # 무의미한 행 레이블 건너뜀
        if not _is_valid_label(row_label):
            continue
        # 무의미한 열 헤더 건너뜀 (YoY 증가율 열은 별도 표기, 검증 대상에서 제외)
        if col_header.upper() in ('YOY', 'YOY增速', '增速', '同比', '变化', '趋势', '说明', '备注'):
            continue
        # label = "행 레이블 · 열 헤더" (열 헤더가 행 레이블의 보완인 경우)
        if col_header and col_header != row_label:
            label = f"{row_label} · {col_header}"
        else:
            label = row_label
        _add(label, val, unit, lineno, raw)

    # --- 2. KV 콜론 행 ---
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code or stripped.startswith('> ') or re.match(r'^#{1,6}\s', stripped):
            continue
        if '|' in stripped:
            continue  # 표 처리는 위에서 이미 완료

        for m in _KV_LABEL_RE.finditer(stripped):
            label = m.group('label')
            val = _clean_num(m.group('num'))
            unit = (m.group('unit') or '').strip()
            _add(label, val, unit, lineno, stripped)

    return points


def sample_points(points: list, ratio: float = 0.15, seed: int = None) -> list:
    """ratio 비율만큼 데이터 포인트를 무작위 추출한다. 최소 3개, 최대 30개."""
    n = max(3, min(30, math.ceil(len(points) * ratio)))
    n = min(n, len(points))
    rng = Random(seed)
    sampled = rng.sample(points, n)
    # 행 번호 순으로 정렬하여 수동 비교 용이하게
    return sorted(sampled, key=lambda p: p['line_number'])


# ---------------------------------------------------------------------------
# 발행 승인/반려 판정
# ---------------------------------------------------------------------------

_TOLERANCE = 0.01   # 1% 허용 오차


def _pct_diff(reported: float, fetched: float) -> float:
    """상대 편차 (절댓값)."""
    if reported == 0:
        return 0.0 if fetched == 0 else float('inf')
    return abs(reported - fetched) / abs(reported)


def render_verdict(results: list, report_name: str = "") -> dict:
    """
    검증 결과를 바탕으로 발행 승인/반려 판정을 출력한다.

    results: list of dict, 각 항목 포함 필드:
      - id, label, reported_value, unit, fetched_value, fetched_source
      - (선택) fetched_value2, fetched_source2   ← 2차 출처

    반환값:
      {
        'verdict': 'PASS' | 'FAIL',
        'pass_count': int,
        'fail_count': int,
        'total': int,
        'fail_items': [...],
        'summary': str,
      }
    """
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    print('=' * 70)
    print(f'{BOLD}报告数据抽检 — 准出/打回判决{RESET}')
    if report_name:
        print(f'报告：{report_name}')
    print('=' * 70)
    print()

    fail_items = []
    warn_items = []

    for item in results:
        label = item.get('label', '?')
        reported = float(item.get('reported_value', 0))
        unit = item.get('unit', '')
        fetched = item.get('fetched_value')
        source = item.get('fetched_source', '?')
        fetched2 = item.get('fetched_value2')
        source2 = item.get('fetched_source2', '')

        # --- 주요 출처 비교 ---
        if fetched is None:
            # 검증값 미제공 → 건너뜀 (통과/실패 미집계)
            print(f'  ⬜ [{item["id"]:>2}] {label[:35]:35s} {reported:>12.2f} {unit}  →  [未提供核验值，跳过]')
            continue

        fetched = float(fetched)
        diff1 = _pct_diff(reported, fetched)

        # --- 2차 출처 비교 (있는 경우) ---
        diff2 = None
        if fetched2 is not None:
            fetched2 = float(fetched2)
            diff2 = _pct_diff(reported, fetched2)

        # 판정
        pass1 = diff1 <= _TOLERANCE
        pass2 = (diff2 is None) or (diff2 <= _TOLERANCE)

        if pass1 and pass2:
            status = f'{GREEN}✅ 通过{RESET}'
            detail = f'{source}: {fetched:.2f} (偏差 {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (偏差 {diff2*100:.2f}%)'
        elif not pass1 and not pass2:
            status = f'{RED}❌ 不通过{RESET}'
            detail = f'{source}: {fetched:.2f} (偏差 {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (偏差 {diff2*100:.2f}%)'
            fail_items.append({
                'id': item['id'],
                'label': label,
                'reported': reported,
                'unit': unit,
                'fetched': fetched,
                'source': source,
                'fetched2': fetched2,
                'source2': source2,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
                'raw_text': item.get('raw_text', ''),
                'line_number': item.get('line_number', 0),
            })
        else:
            # 한 출처 통과, 한 출처 미통과 → 경고, 실패에 미집계
            status = f'{YELLOW}⚠️  警告{RESET}'
            detail = f'{source}: {fetched:.2f} (偏差 {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (偏差 {diff2*100:.2f}%)'
            warn_items.append({
                'id': item['id'], 'label': label,
                'reported': reported, 'unit': unit,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
            })

        print(f'  {status} [{item["id"]:>2}] {label[:35]:35s}  报告: {reported:>12.2f} {unit}')
        print(f'              {" " * 38}{detail}')

    print()
    print('-' * 70)

    total = len([r for r in results if r.get('fetched_value') is not None])
    fail_count = len(fail_items)
    warn_count = len(warn_items)
    pass_count = total - fail_count - warn_count

    print(f'  抽检总数: {total}  |  通过: {GREEN}{pass_count}{RESET}  |  警告: {YELLOW}{warn_count}{RESET}  |  不通过: {RED}{fail_count}{RESET}')
    print()

    if fail_count == 0:
        print(f'{BOLD}{GREEN}【准出】所有抽检数据通过，报告可发布。{RESET}')
        verdict = 'PASS'
    else:
        print(f'{BOLD}{RED}【打回】{fail_count} 个数据点核验不通过，报告需修正后重审。{RESET}')
        print()
        print(f'{BOLD}打回原因：{RESET}')
        for fi in fail_items:
            print(f'  ❌ 第 {fi["line_number"]} 行 | {fi["label"]}')
            print(f'     报告值：{fi["reported"]} {fi["unit"]}')
            print(f'     {fi["source"]}：{fi["fetched"]}  （偏差 {fi["diff1_pct"]}%）')
            if fi.get('fetched2') is not None:
                print(f'     {fi["source2"]}：{fi["fetched2"]}  （偏差 {fi["diff2_pct"]}%）')
            print(f'     原文：{fi["raw_text"][:80]}')
            print()
        verdict = 'FAIL'

    if warn_count > 0:
        print(f'{YELLOW}注意：{warn_count} 个数据点两来源结果不一致（超过1%），可能是口径差异（GAAP/Non-GAAP或汇率），请人工复核。{RESET}')
        for wi in warn_items:
            print(f'  ⚠️  {wi["label"]}  报告:{wi["reported"]} {wi["unit"]}  偏差: {wi["diff1_pct"]}% / {wi["diff2_pct"]}%')

    print('=' * 70)

    return {
        'verdict': verdict,
        'pass_count': pass_count,
        'warn_count': warn_count,
        'fail_count': fail_count,
        'total': total,
        'fail_items': fail_items,
        'warn_items': warn_items,
    }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Report Audit Tool — 연구 보고서 데이터 표본검사 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
작업 흐름:

  Step 1 — 데이터 포인트 추출 및 15% 무작위 표본추출, 표본검사 목록 출력:
    python3 tools/report_audit.py extract --report reports/腾讯/腾讯-research-20260408.md

  Step 2 — Claude가 목록의 각 데이터 포인트에 대해 신뢰할 수 있는 출처에서 값을 가져와
            fetched_value / fetched_source / fetched_value2 / fetched_source2에 입력

  Step 3 — 검증 결과 입력 후 발행 승인/반려 판정 출력:
    python3 tools/report_audit.py verdict --results '[
      {"id":1,"label":"营业收入","reported_value":7518,"unit":"亿","fetched_value":7518,"fetched_source":"macrotrends","fetched_value2":7500,"fetched_source2":"stockanalysis"},
      ...
    ]'

  한 번에 미리보기 (표본검사 목록만 출력, 검증 없음):
    python3 tools/report_audit.py extract --report reports/xxx.md --dry-run

  표본추출 비율 지정 (기본값 0.15):
    python3 tools/report_audit.py extract --report reports/xxx.md --ratio 0.20

  무작위 시드 고정 (동일 표본 재현):
    python3 tools/report_audit.py extract --report reports/xxx.md --seed 42
        """)

    sub = parser.add_subparsers(dest='command')

    # extract
    ext = sub.add_parser('extract', help='보고서에서 데이터 포인트 추출 및 무작위 표본추출')
    ext.add_argument('--report', required=True, help='보고서 파일 경로 (Markdown)')
    ext.add_argument('--ratio', type=float, default=0.15, help='표본추출 비율, 기본값 0.15')
    ext.add_argument('--seed', type=int, default=None, help='무작위 시드 (선택, 재현용)')
    ext.add_argument('--dry-run', action='store_true', help='출력만 하고 JSON 미생성')

    # verdict
    vrd = sub.add_parser('verdict', help='검증 결과를 바탕으로 발행 승인/반려 판정 출력')
    vrd.add_argument('--results', required=True, help='JSON 배열, fetched_value 등 필드 포함')
    vrd.add_argument('--report', default='', help='보고서 이름 (선택, 표시용)')
    vrd.add_argument('--output-json', action='store_true', help='판정 결과를 JSON으로 stdout에 출력')

    args = parser.parse_args()

    if args.command == 'extract':
        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(1)

        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()

        all_points = extract_data_points(text)
        sampled = sample_points(all_points, ratio=args.ratio, seed=args.seed)

        print('=' * 70)
        print(f'보고서 데이터 표본검사 목록')
        print(f'파일: {args.report}')
        print(f'총 추출 데이터 포인트: {len(all_points)}  |  표본추출 비율: {args.ratio:.0%}  |  표본검사 수: {len(sampled)}')
        if args.seed is not None:
            print(f'무작위 시드: {args.seed} (동일 표본 재현 가능)')
        print('=' * 70)
        print()
        print(f'{"ID":>3}  {"행번":>5}  {"데이터 레이블":<35}  {"보고값":>12}  {"단위"}')
        print(f'{"─"*3}  {"─"*5}  {"─"*35}  {"─"*12}  {"─"*6}')
        for p in sampled:
            print(f'{p["id"]:>3}  {p["line_number"]:>5}  {p["label"][:35]:<35}  {p["reported_value"]:>12.2f}  {p["unit"]}')
        print()
        print('↑ 위 각 데이터 포인트에 대해 아래 출처에서 값을 가져와 fetched_value에 입력하세요:')
        print('  미국주식: macrotrends.net (주) + stockanalysis.com (부)')
        print('  홍콩주식: aastocks.com (주) + macrotrends ADR (부)')
        print('  A주: eastmoney.com (주) + cninfo.com.cn (부)')
        print()

        if not args.dry_run:
            # 입력 가능한 JSON 템플릿 출력
            template = []
            for p in sampled:
                template.append({
                    'id': p['id'],
                    'label': p['label'],
                    'reported_value': p['reported_value'],
                    'unit': p['unit'],
                    'line_number': p['line_number'],
                    'raw_text': p['raw_text'],
                    'fetched_value': None,       # ← 주요 출처 검증값 입력
                    'fetched_source': '',        # ← 주요 출처명 입력
                    'fetched_value2': None,      # ← 보조 출처 검증값 입력 (선택)
                    'fetched_source2': '',       # ← 보조 출처명 입력 (선택)
                })
            print('표본검사 목록 JSON (fetched_value 입력 후 verdict 명령에 전달):')

            print()
            print(json.dumps(template, ensure_ascii=False, indent=2))

    elif args.command == 'verdict':
        try:
            results = json.loads(args.results)
        except json.JSONDecodeError as e:
            print(f'❌ JSON 解析失败: {e}', file=sys.stderr)
            sys.exit(1)

        report_name = args.report or ''
        outcome = render_verdict(results, report_name=report_name)

        if args.output_json:
            print(json.dumps(outcome, ensure_ascii=False, indent=2))

        # 비영(non-zero) 종료 코드는 반려를 의미, CI/스크립트 판단 용이
        sys.exit(0 if outcome['verdict'] == 'PASS' else 1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
