#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
설구(雪球) 범용 스크레이퍼: 지정 사용자의 전체 타임라인을 순회하며 키워드로 본인 원글만 필터링한다.

특징:
  - Playwright 로그인 상태 재사용: 최초 headful 수동 로그인 후 state를 로컬에 저장
  - 이중 채널 fetch: 페이지 내 JS fetch 우선, 실패 시 context.request(APIRequestContext)로 폴백
  - 체크포인트 재개: 10페이지마다 진행 상태 저장; 중단 후 재실행 시 자동으로 이어서 진행
  - 속도 제한 대응: 2-4초 랜덤 지연 + 50페이지마다 30초 장휴식 + 연속 5회 타임아웃 시 자동 종료하여 진행 상태 보전
  - 순수 리트윗 필터링: 수집 대상 사용자 본인이 작성한 내용만 수록(text 비어있지 않음, "转发微博" 아님)

자격증명은 환경 변수로 전달, **코드 저장소에 포함하지 않는다**:
  export XQ_PHONE=13xxxxxxxxx
  export XQ_PASSWORD=xxx
설정하지 않아도 되며, 최초 실행 시 headful 브라우저가 열려 수동 로그인 가능(QR코드/문자/비밀번호 모두 가능).

사용 예시:
  # 돤융핑의 핀둬둬 관련 발언
  python3 xueqiu_scraper.py \\
      --user-id 1247347556 \\
      --keywords 拼多多,PDD,Temu,黄峥 \\
      --output ../reports/拼多多/段永平雪球发言-PDD相关.md

  # 다른 사용자 + 다른 키워드
  python3 xueqiu_scraper.py --user-id 6784593966 --keywords 茅台 --output /tmp/out.md

로그인 상태 캐시 기본 경로: /tmp/xueqiu_state.json, --state-path 로 변경 가능.
"""

import argparse
import asyncio
import json
import os
import random
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


def is_match(text, keywords):
    t = (text or '').lower()
    return any(k.lower() in t for k in keywords)


def parse_ts(ts):
    try:
        return datetime.fromtimestamp(int(ts) / 1000).strftime('%Y-%m-%d %H:%M')
    except Exception:
        return str(ts)


def clean(s):
    if not s: return ''
    s = re.sub(r'<[^>]+>', '', s)
    for ent, rep in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&nbsp;', ' ')]:
        s = s.replace(ent, rep)
    return re.sub(r'&#\d+;', '', s).strip()


async def browser_fetch_json(page, url, timeout_s=15):
    """페이지 JS fetch 우선; 실패 시 context.request로 폴백."""
    js = f"""
        async () => {{
            const ctl = new AbortController();
            const to = setTimeout(() => ctl.abort(), {int(timeout_s*1000)});
            try {{
                const r = await fetch({json.dumps(url)}, {{
                    headers: {{'Accept':'application/json','X-Requested-With':'XMLHttpRequest'}},
                    credentials: 'include', signal: ctl.signal
                }});
                const text = await r.text();
                clearTimeout(to);
                try {{ return JSON.parse(text); }}
                catch(e) {{ return {{_raw: text.substring(0, 300)}}; }}
            }} catch(e) {{
                clearTimeout(to);
                return {{_error: e.toString()}};
            }}
        }}
    """
    try:
        result = await asyncio.wait_for(page.evaluate(js), timeout=timeout_s + 5)
        if result and not result.get('_error') and not result.get('_raw'):
            return result
    except Exception:
        pass
    try:
        resp = await page.context.request.get(url, headers={
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://xueqiu.com/',
        }, timeout=timeout_s * 1000)
        if resp.ok:
            return await resp.json()
    except Exception:
        return None
    return None


async def verify_login(page, user_id):
    test = await browser_fetch_json(
        page,
        f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page=2&count=1'
    )
    return bool(test and test.get('statuses') is not None)


async def interactive_login(pw, state_path, user_id):
    phone = os.environ.get('XQ_PHONE', '')
    print("\n[로그인 필요] headful 브라우저를 열겠습니다. 그 안에서 설구 로그인을 완료하세요")
    if phone:
        print(f"        환경 변수 XQ_PHONE = {phone}   （비밀번호는 XQ_PASSWORD）")
    else:
        print("        XQ_PHONE/XQ_PASSWORD 미설정 — 브라우저에서 QR코드 스캔 또는 직접 입력하세요")
    browser = await pw.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled'],
    )
    context = await browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='zh-CN',
        viewport={'width': 1280, 'height': 800},
    )
    await context.add_init_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    page = await context.new_page()
    await page.goto('https://xueqiu.com/', wait_until='domcontentloaded')
    print(">>> 브라우저에서 로그인을 완료하세요. 스크립트가 5초마다 폴링하며 성공 시 자동 진행합니다（최대 10분）")
    ok = False
    for i in range(120):
        await asyncio.sleep(5)
        try:
            if await verify_login(page, user_id):
                ok = True
                print(f"  ✓ 로그인 성공（{i+1}번째 폴링）")
                break
        except Exception as e:
            print(f"  폴링 예외(무시): {e}")
        if (i + 1) % 6 == 0:
            print(f"  ...로그인 대기 중（{(i+1)*5}초 경과）")
    if not ok:
        print("10분 내 로그인 감지 실패, 종료")
        await browser.close()
        return None
    await context.storage_state(path=state_path)
    print(f"로그인 상태 저장 완료 → {state_path}")
    return browser, context, page


async def load_with_state(pw, state_path, user_id):
    if not os.path.exists(state_path):
        return None
    browser = await pw.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled'],
    )
    context = await browser.new_context(
        storage_state=state_path,
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='zh-CN',
        viewport={'width': 1280, 'height': 800},
    )
    await context.add_init_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    page = await context.new_page()
    loaded = False
    for attempt in range(3):
        try:
            await page.goto('https://xueqiu.com/', wait_until='domcontentloaded', timeout=15000)
            loaded = True
            break
        except Exception as e:
            print(f"  홈페이지 로드 실패({attempt+1}번째): {e}")
            await asyncio.sleep(5)
    if not loaded:
        try:
            await page.goto('about:blank')
        except Exception:
            pass
    await asyncio.sleep(2)
    if await verify_login(page, user_id):
        print("✓ 저장된 로그인 상태 재사용 성공")
        return browser, context, page
    print("저장된 state가 만료되었습니다")
    await browser.close()
    return None


async def fetch_all_timeline(page, user_id, keywords, progress_path, dump_all_path=''):
    collected = {}
    # all_posts: 해당 사용자의 모든 원글 저장（키워드 필터 없음）, 오프라인 다중 주제 분석용
    all_posts = {}
    if dump_all_path and os.path.exists(dump_all_path):
        try:
            for e in json.load(open(dump_all_path)):
                all_posts[e['id']] = e
            print(f"  ↪ 기존 전량 캐시 로드: {len(all_posts)} 건")
        except Exception as e:
            print(f"  전량 캐시 읽기 실패: {e}")
    print("\n=== 전체 타임라인 순회 ===")
    data = await browser_fetch_json(
        page,
        f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page=1&count=20'
    )
    if not data or data.get('error_code'):
        print(f"  1페이지 실패: {data}")
        return collected
    max_page = data.get('maxPage', 600)
    total = data.get('total', '?')
    print(f"  사용자ID: {user_id} | 총 게시물 수: {total} | 총 페이지: {max_page}")

    total_posts = 0
    found = 0

    def process(d):
        nonlocal total_posts, found
        for post in d.get('statuses', []):
            total_posts += 1
            text = clean(post.get('text', '') or post.get('description', ''))
            title = clean(post.get('title', ''))
            rt = post.get('retweeted_status') or {}
            rt_text = clean(rt.get('text', ''))
            own_text = (text or '').strip()
            if own_text in ('', '转发微博', '轉發微博', 'Repost'):
                continue
            pid = str(post.get('id', ''))
            date = parse_ts(post.get('created_at', 0))
            entry = {'id': pid, 'date': date, 'title': title, 'text': own_text,
                     'url': f'https://xueqiu.com/{user_id}/{pid}'}
            if rt:
                rt_user = (rt.get('user') or {}).get('screen_name', '')
                entry['retweet_of'] = f'@{rt_user}: {rt_text}'
            # 전량 캐시（필터 없음）
            if dump_all_path and pid not in all_posts:
                all_posts[pid] = entry
            # 키워드로 필터링하여 수집
            if keywords and is_match(title + ' ' + own_text, keywords):
                if pid not in collected:
                    collected[pid] = entry
                    found += 1
                    preview = own_text[:80] if own_text else (rt_text[:80] if rt_text else title[:80])
                    print(f"  ✓ [{date}] {preview}...")

    process(data)
    start_page = 2
    if os.path.exists(progress_path):
        try:
            with open(progress_path) as f:
                prev = json.load(f)
            start_page = max(2, prev.get('next_page', 2))
            for e in prev.get('collected', []):
                collected[e['id']] = e
                found += 1
            print(f"  ↪ 이어서 진행: {start_page}페이지부터, 기존 {found}건")
        except Exception as e:
            print(f"  진행 상태 파일 읽기 실패: {e}")

    def save_progress(next_page):
        with open(progress_path, 'w', encoding='utf-8') as f:
            json.dump({'next_page': next_page, 'collected': list(collected.values())},
                      f, ensure_ascii=False)
        if dump_all_path:
            with open(dump_all_path, 'w', encoding='utf-8') as f:
                json.dump(list(all_posts.values()), f, ensure_ascii=False)

    consec_fail = 0
    for p in range(start_page, max_page + 1):
        try:
            data = await browser_fetch_json(
                page,
                f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page={p}&count=20',
                timeout_s=15,
            )
        except Exception as e:
            print(f"  {p}페이지 예외: {e}")
            data = None
        if not data:
            consec_fail += 1
            print(f"  {p}페이지 응답 없음/타임아웃（연속 {consec_fail}회）")
            if consec_fail >= 5:
                print("  연속 5회 실패, 진행 상태 저장 후 종료（재실행 시 자동으로 이어서 진행）")
                save_progress(p)
                break
            await asyncio.sleep(5 * consec_fail)
            continue
        consec_fail = 0
        if data.get('error_code'):
            print(f"  {p}페이지 오류: {data.get('error_code')} {data.get('error_description')}")
            save_progress(p)
            break
        statuses = data.get('statuses', [])
        if not statuses:
            print(f"  {p}페이지 비어있음, 종료")
            break
        prev_found = found
        process(data)
        if p % 10 == 0 or found > prev_found:
            print(f"  {p}/{max_page}페이지 | 스캔 {total_posts}건 | 명중 {found}건")
        if p % 10 == 0:
            save_progress(p + 1)
        if p % 50 == 0:
            print(f"  ⏸ {p}페이지 후 30초 휴식")
            await asyncio.sleep(30)
        else:
            await asyncio.sleep(random.uniform(2.0, 4.0))
    else:
        if os.path.exists(progress_path):
            os.remove(progress_path)

    # 마지막으로 전량 캐시 디스크에 기록
    if dump_all_path:
        with open(dump_all_path, 'w', encoding='utf-8') as f:
            json.dump(list(all_posts.values()), f, ensure_ascii=False)
        print(f"  전량 캐시 → {dump_all_path}（{len(all_posts)}건）")
    print(f"\n완료: 스캔 {total_posts}건, 명중 {found}건")
    return collected


def format_md(collected, user_id, keywords):
    posts = sorted(collected.values(), key=lambda x: x.get('date', ''))
    lines = [
        f"# 雪球发言整理：用户 {user_id}",
        "",
        f"> **信息来源**：雪球 https://xueqiu.com/u/{user_id}",
        f"> **整理时间**：{datetime.now().strftime('%Y-%m-%d')}",
        f"> **收录条数**：{len(posts)} 条",
        f"> **关键词筛选**：{', '.join(keywords)}",
        f"> **采集方式**：Playwright 登录态 + user_timeline.json 全量遍历（仅本人原发言）",
        "",
        "---",
        "",
    ]
    for i, p in enumerate(posts, 1):
        lines.append(f"## {i}. {p.get('date','?')}")
        lines.append("")
        if p.get('title'):
            lines += [f"**【{p['title']}】**", ""]
        if p.get('retweet_of'):
            lines += [f"> 转发原文：{p['retweet_of']}", ""]
        if p.get('text'):
            lines.append(p['text'])
            lines.append("")
        lines += [f"来源：{p.get('url','')}", "", "---", ""]
    return '\n'.join(lines)


def parse_args():
    ap = argparse.ArgumentParser(description="설구 사용자 타임라인 스크레이퍼（키워드로 본인 원글 필터링）")
    ap.add_argument('--user-id', type=int, help='설구 사용자ID（프로필 URL의 숫자）')
    ap.add_argument('--keywords', type=str, default='',
                    help='키워드 목록, 쉼표로 구분. 예: 拼多多,PDD,黄峥,Temu')
    ap.add_argument('--output', type=str, default='', help='markdown 출력 경로')
    ap.add_argument('--raw-json', type=str, default='', help='（선택）명중 항목 원본 JSON 출력 경로')
    ap.add_argument('--state-path', type=str, default='/tmp/xueqiu_state.json',
                    help='로그인 상태 캐시 파일（기본값: /tmp/xueqiu_state.json）')
    ap.add_argument('--dump-all', type=str, default='',
                    help='전량 캐시 경로: 수집 시 해당 사용자의 모든 원글을 여기에도 저장, 이후 오프라인 다중 주제 분석용')
    ap.add_argument('--from-cache', type=str, default='',
                    help='수집 건너뛰고 기존 전량 캐시 JSON에서 필터링하여 markdown 생성（--keywords 와 --output 필요）')
    return ap.parse_args()


def filter_from_cache(cache_path, keywords, user_id):
    posts = json.load(open(cache_path))
    out = []
    for p in posts:
        if is_match((p.get('title','') + ' ' + p.get('text','')), keywords):
            out.append(p)
    return {p['id']: p for p in out}


async def main():
    args = parse_args()
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]

    # 오프라인 필터 모드
    if args.from_cache:
        if not (keywords and args.output):
            print("--from-cache 사용 시 --keywords 와 --output 을 함께 지정해야 합니다")
            return
        user_id = args.user_id or 0
        collected = filter_from_cache(args.from_cache, keywords, user_id)
        print(f"캐시 {args.from_cache} 에서 {len(collected)}건 필터링（키워드: {keywords}）")
        if not collected:
            return
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(format_md(collected, user_id, keywords))
        print(f"Markdown → {args.output}")
        return

    if not args.user_id:
        print("--user-id 가 필요합니다")
        return

    progress_path = args.state_path + f'.progress.{args.user_id}'
    raw_json = args.raw_json or f'/tmp/xueqiu_{args.user_id}_raw.json'

    print("=" * 60)
    print(f"설구 스크레이퍼 | user_id={args.user_id} | keywords={keywords} | dump_all={args.dump_all}")
    print("=" * 60)

    async with async_playwright() as pw:
        session = await load_with_state(pw, args.state_path, args.user_id)
        if not session:
            session = await interactive_login(pw, args.state_path, args.user_id)
        if not session:
            print("로그인 불가, 종료")
            return
        browser, _, page = session
        collected = await fetch_all_timeline(page, args.user_id, keywords, progress_path, args.dump_all)
        await browser.close()

    print(f"\n=== 최종: {len(collected)}건 명중 ===")
    if not collected:
        return
    with open(raw_json, 'w', encoding='utf-8') as f:
        json.dump(list(collected.values()), f, ensure_ascii=False, indent=2)
    print(f"원본 JSON → {raw_json}")
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(format_md(collected, args.user_id, keywords))
        print(f"Markdown  → {args.output}")


if __name__ == '__main__':
    asyncio.run(main())
