#!/usr/bin/env python3
"""Claude Code 세션 기록(JSONL)에서 토큰 사용량을 집계한다.

사용법:
  python3 measure-tokens.py <session.jsonl> [<session.jsonl> ...]
  python3 measure-tokens.py --dir ~/.claude/projects/<프로젝트폴더>      # 폴더 안 모든 세션
  python3 measure-tokens.py A.jsonl --from "결제 알림" --to "완료"       # 특정 사용자 프롬프트 구간만
  python3 measure-tokens.py A.jsonl B.jsonl --label 하네스없음 --label 하네스있음

집계 규칙:
  - type == "assistant" 줄의 message.usage 를 합산한다.
  - 같은 requestId 가 여러 줄로 나뉘어 있으면 마지막 줄만 센다(스트리밍 중복 방지).
  - isSidechain == true 줄은 서브에이전트 사용량으로 따로 집계한다.
  - --from / --to 는 사용자 프롬프트 본문에 해당 문구가 처음 나타나는 지점부터
    다음 문구가 나타나기 직전까지를 구간으로 잡는다. --to 를 생략하면 파일 끝까지.

출력 열:
  input        캐시에 없던 새 입력 토큰
  cache_write  캐시에 새로 올린 토큰 (요금이 input 보다 높음)
  cache_read   캐시에서 읽은 토큰 (요금이 input 보다 훨씬 낮음)
  output       출력 토큰 (thinking 포함)
  calls        API 호출 수
  billable*    input + cache_write + cache_read + output 의 단순 합. 요금 비교가 아니라 규모 비교용.
"""
import argparse
import glob
import json
import os
import sys


def user_text(obj):
    m = obj.get("message") or {}
    c = m.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(
            b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def read_usage(path, start=None, end=None, ts_lo=None, ts_hi=None):
    """JSONL 하나를 읽어 requestId 별 usage 와 활성 구간의 timestamp 범위를 돌려준다.

    start/end: 사용자 프롬프트 문구로 구간을 자른다 (메인 세션용).
    ts_lo/ts_hi: ISO timestamp 로 구간을 자른다 (서브에이전트 파일용).
    """
    by_req = {}
    order = []
    active = start is None
    lo = hi = None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = o.get("type")
            ts = o.get("timestamp")
            if t == "user" and not o.get("isSidechain"):
                txt = user_text(o)
                if not active and start and start in txt:
                    active = True
                elif active and end and end in txt:
                    break
            if not active or t != "assistant":
                continue
            if ts and ((ts_lo and ts < ts_lo) or (ts_hi and ts > ts_hi)):
                continue
            m = o.get("message") or {}
            u = m.get("usage")
            if not isinstance(u, dict):
                continue
            rid = o.get("requestId") or o.get("uuid")
            if rid not in by_req:
                order.append(rid)
            by_req[rid] = (bool(o.get("isSidechain")), u)
            if ts:
                lo = ts if lo is None or ts < lo else lo
                hi = ts if hi is None or ts > hi else hi
    return [by_req[r] for r in order], lo, hi


def subagent_files(session_path):
    """<dir>/<sessionId>/subagents/agent-*.jsonl 를 찾는다."""
    base, name = os.path.split(session_path)
    sid = name[:-6] if name.endswith(".jsonl") else name
    return sorted(glob.glob(os.path.join(base, sid, "subagents", "*.jsonl")))


def collect(path, start=None, end=None):
    """세션 파일 + 그 서브에이전트 파일들을 읽어 {main: {...}, sub: {...}} 를 돌려준다."""
    zero = lambda: {"input": 0, "cache_write": 0, "cache_read": 0, "output": 0, "calls": 0}
    tot = {"main": zero(), "sub": zero()}

    def add(k, u):
        tot[k]["input"] += u.get("input_tokens", 0) or 0
        tot[k]["cache_write"] += u.get("cache_creation_input_tokens", 0) or 0
        tot[k]["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
        tot[k]["output"] += u.get("output_tokens", 0) or 0
        tot[k]["calls"] += 1

    main_rows, lo, hi = read_usage(path, start, end)
    for side, u in main_rows:
        add("sub" if side else "main", u)

    # 서브에이전트 파일: 구간을 잘랐다면 메인 구간의 timestamp 범위 안의 호출만 센다.
    ts_lo = lo if (start or end) else None
    ts_hi = hi if (start or end) else None
    for sf in subagent_files(path):
        rows, _, _ = read_usage(sf, None, None, ts_lo, ts_hi)
        for _, u in rows:
            add("sub", u)
    return tot


def total_row(t):
    r = {k: t["main"][k] + t["sub"][k] for k in t["main"]}
    r["billable"] = r["input"] + r["cache_write"] + r["cache_read"] + r["output"]
    return r


def fmt(n):
    return f"{n:,}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="세션 JSONL 파일")
    ap.add_argument("--dir", help="이 폴더의 *.jsonl 전부")
    ap.add_argument("--from", dest="start", help="구간 시작: 이 문구가 든 사용자 프롬프트부터")
    ap.add_argument("--to", dest="end", help="구간 끝: 이 문구가 든 사용자 프롬프트 직전까지")
    ap.add_argument("--label", action="append", default=[], help="파일 순서대로 붙일 이름")
    ap.add_argument("--json", action="store_true", help="JSON 으로 출력")
    a = ap.parse_args()

    files = list(a.files)
    if a.dir:
        files += sorted(glob.glob(os.path.join(os.path.expanduser(a.dir), "*.jsonl")))
    if not files:
        ap.error("세션 파일이나 --dir 을 지정하세요")

    rows = []
    for i, f in enumerate(files):
        label = a.label[i] if i < len(a.label) else os.path.basename(f)[:12]
        t = collect(os.path.expanduser(f), a.start, a.end)
        rows.append((label, t, total_row(t)))

    if a.json:
        print(json.dumps([{"label": l, "main": t["main"], "sub": t["sub"], "total": r} for l, t, r in rows],
                         ensure_ascii=False, indent=1))
        return

    hdr = f"{'label':<14}{'scope':<6}{'input':>12}{'cache_write':>13}{'cache_read':>13}{'output':>10}{'calls':>7}{'billable*':>14}"
    print(hdr)
    print("-" * len(hdr))
    for label, t, r in rows:
        for scope in ("main", "sub"):
            m = t[scope]
            print(f"{label:<14}{scope:<6}{fmt(m['input']):>12}{fmt(m['cache_write']):>13}{fmt(m['cache_read']):>13}{fmt(m['output']):>10}{m['calls']:>7}{'':>14}")
        print(f"{label:<14}{'total':<6}{fmt(r['input']):>12}{fmt(r['cache_write']):>13}{fmt(r['cache_read']):>13}{fmt(r['output']):>10}{r['calls']:>7}{fmt(r['billable']):>14}")
        print()
    if len(rows) == 2:
        a_, b_ = rows[0][2], rows[1][2]
        for k in ("input", "cache_write", "cache_read", "output", "billable"):
            if a_[k]:
                d = (b_[k] - a_[k]) / a_[k] * 100
                print(f"{k:<12} {rows[0][0]} → {rows[1][0]}: {d:+.1f}%")
    print("\n* billable 은 단순 합. 실제 요금은 cache_write > input > cache_read 순으로 다르니 요금 비교는 모델 단가를 곱해 따로 계산.")


if __name__ == "__main__":
    main()
