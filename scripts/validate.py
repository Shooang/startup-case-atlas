import pathlib, re, sys, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
CASES = ROOT / "cases"

REQUIRED = ["id", "title", "title_en", "type", "source", "era", "source_language",
            "region", "year", "outcome", "industry", "tags", "key_numbers",
            "timeline", "causal_chain", "angles", "status"]
INDUSTRY = {"food-beverage", "retail", "ecommerce", "content-media", "software-saas",
            "hardware", "services", "education", "gaming", "fintech", "healthcare",
            "logistics", "other"}
OUTCOME = {"failure", "success", "exit", "pivoted", "ongoing"}
TAGS = {"franchise", "low-price-trap", "traffic-dependency", "platform-risk",
        "cashflow-crunch", "supply-chain", "partnership-dispute",
        "product-market-fit", "retention", "cost-structure", "scaling", "pivot",
        # 司法判决案例（07-judgments）新增
        "contract-dispute", "false-advertising", "qualification"}
SECTIONS = ["## 故事正文", "## 可用观点", "## 事实边界"]


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if v.startswith("[") and v.endswith("]"):
                d[k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            else:
                d[k] = v
    return d, m.group(2)


errors, warns = [], []
seen = {}
n = 0
for p in sorted(CASES.glob("*/*.md")):
    n += 1
    d, body = parse(p.read_text(encoding="utf-8"))
    rel = p.relative_to(ROOT)
    if d is None:
        errors.append(f"{rel}: 无 front matter")
        continue
    for k in REQUIRED:
        if k not in d or d[k] in ("", []):
            errors.append(f"{rel}: 字段为空 {k}")
    gid = d.get("id", "")
    if gid in seen:
        errors.append(f"{rel}: id 重复 {gid} 与 {seen[gid]}")
    seen[gid] = str(rel)
    if d.get("industry") not in INDUSTRY:
        errors.append(f"{rel}: industry 越界 {d.get('industry')}")
    if d.get("outcome") not in OUTCOME:
        errors.append(f"{rel}: outcome 越界 {d.get('outcome')}")
    tags = d.get("tags", [])
    if isinstance(tags, str):
        tags = [x.strip() for x in tags.strip("[]").split(",") if x.strip()]
    if not (2 <= len(tags) <= 5):
        warns.append(f"{rel}: tags 数量 {len(tags)}（应 2-5）")
    for t in tags:
        if t not in TAGS:
            errors.append(f"{rel}: tag 越界 {t}")
    for s in SECTIONS:
        if s not in body:
            errors.append(f"{rel}: 缺正文节 {s}")
    story = body.split("## 故事正文")[-1] if "## 故事正文" in body else ""
    story = story.split("## ")[0]
    if len(story) < 300:
        warns.append(f"{rel}: 故事正文偏短 {len(story)} 字")

print(f"检查 {n} 个案例")
print(f"错误 {len(errors)}")
for e in errors[:20]:
    print("  ✗", e)
print(f"警告 {len(warns)}")
for w in warns[:10]:
    print("  !", w)

sys.exit(1 if errors else 0)
