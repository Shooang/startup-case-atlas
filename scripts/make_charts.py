#!/usr/bin/env python3
"""Generate README charts as standalone SVG from data/cases.jsonl.

Output: assets/failure-mechanisms.svg
Run: python3 scripts/make_charts.py
Charts embed prefers-color-scheme styles so GitHub renders them correctly
in both light and dark mode.
"""
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABELS = {
    "product-market-fit": "需求错配",
    "scaling": "扩张过快",
    "cost-structure": "成本结构过重",
    "traffic-dependency": "依赖单一流量",
    "cashflow-crunch": "现金流断裂",
    "retention": "复购不足",
    "platform-risk": "平台规则变化",
    "pivot": "转型未成",
    "supply-chain": "供应链",
    "franchise": "加盟",
    "partnership-dispute": "合伙纠纷",
    "low-price-trap": "低价引流反噬",
}

W, ROW, PAD_TOP, PAD_BOTTOM = 900, 34, 92, 56
LABEL_X, BAR_X, BAR_MAX = 160, 176, 580


def main():
    rows = [json.loads(l) for l in open(ROOT / "data/cases.jsonl", encoding="utf-8")]
    counts = Counter()
    for r in rows:
        counts.update(r["tags"])
    total_cases = len(rows)
    total_tags = sum(counts.values())
    items = counts.most_common()
    top = items[0][1]
    height = PAD_TOP + ROW * len(items) + PAD_BOTTOM

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" role="img" aria-label="{total_cases} 个创业案例的失败机制分布">',
        f"<title>{total_cases} 个创业案例的失败机制分布</title>",
        "<style>",
        "  .bg{fill:#ffffff} .ttl{fill:#111827} .sub{fill:#6b7280}",
        "  .lbl{fill:#374151} .val{fill:#6b7280} .bar{fill:#c7d2e4} .hot{fill:#d85a30}",
        "  .note{fill:#9ca3af} .rule{stroke:#e5e7eb}",
        "  text{font-family:system-ui,-apple-system,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif}",
        "  @media (prefers-color-scheme: dark){",
        "    .bg{fill:#0d1117} .ttl{fill:#e6edf3} .sub{fill:#8b949e}",
        "    .lbl{fill:#c9d1d9} .val{fill:#8b949e} .bar{fill:#30363d} .hot{fill:#e8734a}",
        "    .note{fill:#6e7681} .rule{stroke:#21262d}",
        "  }",
        "</style>",
        f'<rect class="bg" width="{W}" height="{height}" rx="12"/>',
        f'<text class="ttl" x="40" y="46" font-size="21" font-weight="600">{total_cases} 个生意，都是怎么死的</text>',
        f'<text class="sub" x="40" y="72" font-size="14">每个案例 2–5 个标签，共 {total_tags} 次计数。最多的一项占 {top / total_cases:.0%}。</text>',
    ]

    for i, (key, n) in enumerate(items):
        y = PAD_TOP + i * ROW
        bw = max(3, round(BAR_MAX * n / top))
        cls = "hot" if i == 0 else "bar"
        parts.append(f'<text class="lbl" x="{LABEL_X}" y="{y + 15}" font-size="13.5" text-anchor="end">{LABELS.get(key, key)}</text>')
        parts.append(f'<rect class="{cls}" x="{BAR_X}" y="{y + 3}" width="{bw}" height="17" rx="4"/>')
        parts.append(f'<text class="val" x="{BAR_X + bw + 9}" y="{y + 16}" font-size="12.5">{n}</text>')

    y_note = PAD_TOP + ROW * len(items) + 14
    parts.append(f'<line class="rule" x1="40" y1="{y_note - 6}" x2="{W - 40}" y2="{y_note - 6}" stroke-width="1"/>')
    parts.append(f'<text class="note" x="40" y="{y_note + 18}" font-size="12">数据：本仓库 data/cases.jsonl　·　标签为闭合词表，一个案例可命中多个机制</text>')
    parts.append("</svg>")

    out = ROOT / "assets" / "failure-mechanisms.svg"
    if not out.parent.exists():
        out.parent.mkdir()
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"written {out.relative_to(ROOT)}  {out.stat().st_size} bytes  {height}px")


if __name__ == "__main__":
    main()
