#!/usr/bin/env python3
"""从 frameworks/*.md 生成数据文件与索引。"""
import pathlib
import json
import csv
import re
import collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "frameworks"
DATA = ROOT / "data"
INDEX = ROOT / "index"

FIELDS = ["id", "type", "title", "title_en", "hook", "book", "author", "edition",
          "chapter", "locator", "quote", "doctrine", "tags", "applies_to",
          "related_cases", "status"]


def parse(p):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", t, re.S)
    if not m:
        return None
    fm, body = m.group(1), m.group(2)
    d = {}
    for line in fm.splitlines():
        if ": " not in line:
            continue
        k, v = line.split(": ", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        elif v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        d[k] = v
    d["_file"] = f"frameworks/{p.name}"
    d["_body_chars"] = len(re.findall(r"[\u4e00-\u9fff]", body))
    d["_sections"] = [s for s in ["这个框架在说什么", "能拿来判断什么", "出处与边界"] if f"## {s}" in body]
    return d


cards = [c for c in (parse(p) for p in sorted(SRC.glob("F*.md"))) if c]
cards.sort(key=lambda c: c["id"])
print(f"解析 {len(cards)} 张卡")

if not DATA.exists():
    DATA.mkdir(parents=True)
with (DATA / "frameworks.jsonl").open("w", encoding="utf-8") as f:
    for c in cards:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

with (DATA / "frameworks.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "title", "book", "author", "doctrine", "tags", "file"])
    for c in cards:
        w.writerow([c["id"], c["title"], c["book"], c["author"],
                    "|".join(c.get("doctrine", [])) if isinstance(c.get("doctrine"), list) else c.get("doctrine", ""),
                    "|".join(c.get("tags", [])) if isinstance(c.get("tags"), list) else c.get("tags", ""),
                    c["_file"]])

# 索引一：按书
by_book = collections.OrderedDict()
for c in cards:
    by_book.setdefault((c["book"], c["author"], c.get("edition", "")), []).append(c)
lines = ["# 按书浏览\n", f"> {len(cards)} 张框架卡，来自 {len(by_book)} 本书。\n"]
for (book, author, edition), items in sorted(by_book.items(), key=lambda x: -len(x[1])):
    lines.append(f"## {book}\n")
    lines.append(f"{author} · {edition}\n")
    lines.append("| ID | 标题 | 能用来判断什么 |")
    lines.append("| --- | --- | --- |")
    for c in items:
        ap = c.get("applies_to", [])
        first = ap[0] if isinstance(ap, list) and ap else ""
        lines.append(f"| [{c['id']}](../{c['_file']}) | {c['title']} | {first} |")
    lines.append("")
(INDEX / "frameworks-by-book.md").write_text("\n".join(lines), encoding="utf-8")

# 索引二：按领域
by_doc = collections.defaultdict(list)
for c in cards:
    docs = c.get("doctrine", [])
    if not isinstance(docs, list):
        docs = [docs]
    for d in docs:
        by_doc[d].append(c)
lines = ["# 按领域浏览\n", "| 领域 | 张数 | 卡片 |", "| --- | --- | --- |"]
for d, items in sorted(by_doc.items(), key=lambda x: -len(x[1])):
    links = " · ".join(f"[{c['id']}](../{c['_file']})" for c in items)
    lines.append(f"| `{d}` | {len(items)} | {links} |")
(INDEX / "frameworks-by-doctrine.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# 索引三：hook 汇总，方便写稿时挑开场
lines = ["# 开场句汇总\n", "> 每张卡的可念开场，写稿时直接挑。\n"]
for c in cards:
    if c.get("hook"):
        lines.append(f"- **{c['id']}** {c['hook']}  \n  `{c['title']}`")
(INDEX / "frameworks-hooks.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

stats = {
    "cards": len(cards),
    "books": len(by_book),
    "avg_chars": round(sum(c["_body_chars"] for c in cards) / max(len(cards), 1)),
    "min_chars": min(c["_body_chars"] for c in cards),
    "max_chars": max(c["_body_chars"] for c in cards),
    "doctrines": {k: len(v) for k, v in sorted(by_doc.items(), key=lambda x: -len(x[1]))},
}
(ROOT / "data" / "frameworks-stats.json").write_text(
    json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(stats, ensure_ascii=False, indent=2))
