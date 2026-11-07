import pathlib, re, json, collections

ROOT = pathlib.Path("startup-case-atlas/cases")
META = pathlib.Path("startup-case-atlas/data/meta")

meta = {}
dup = []
for f in sorted(META.glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    for k, v in d.items():
        if k in meta:
            dup.append(k)
        meta[k] = v

print("合并元数据:", len(meta), "| 重复键:", dup)

ORDER = ["id", "title", "title_en", "type", "source", "era", "region", "year",
         "outcome", "industry", "tags", "key_numbers", "timeline",
         "causal_chain", "angles", "status"]


def parse_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return None, text
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip()
    return d, text[m.end():]


def render(d, body):
    out = ["---"]
    for k in ORDER:
        v = d.get(k, "")
        if isinstance(v, list):
            v = "[" + ", ".join(v) + "]" if v else "[]"
        out.append(f"{k}: {v}".rstrip())
    out.append("---")
    return "\n".join(out) + "\n" + body


written = 0
missing = []
valid_ind = {"food-beverage", "retail", "ecommerce", "content-media", "software-saas",
             "hardware", "services", "education", "gaming", "fintech", "healthcare",
             "logistics", "other"}
valid_out = {"failure", "success", "exit", "pivoted", "ongoing"}
valid_tag = {"franchise", "low-price-trap", "traffic-dependency", "platform-risk",
             "cashflow-crunch", "supply-chain", "partnership-dispute",
             "product-market-fit", "retention", "cost-structure", "scaling", "pivot"}
bad = collections.Counter()

for p in sorted(ROOT.glob("*/*.md")):
    t = p.read_text(encoding="utf-8")
    d, body = parse_fm(t)
    if d is None:
        continue
    gid = d.get("id", "")
    m = meta.get(gid)
    if not m:
        missing.append(p.name)
        continue
    d["title_en"] = m.get("title_en", "")
    d["industry"] = m.get("industry", "")
    d["outcome"] = m.get("outcome", "")
    d["tags"] = m.get("tags", [])
    if d["industry"] not in valid_ind:
        bad["industry"] += 1
    if d["outcome"] not in valid_out:
        bad["outcome"] += 1
    if any(x not in valid_tag for x in d["tags"]):
        bad["tags"] += 1
    p.write_text(render(d, body), encoding="utf-8")
    written += 1

print("写入卡片:", written)
print("未匹配到元数据:", len(missing), missing[:8])
print("越界字段:", dict(bad))
