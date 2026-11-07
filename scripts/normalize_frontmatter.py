import pathlib, re, json

ROOT = pathlib.Path("startup-case-atlas/cases")
KEYMAP = {
    "id": "id",
    "标题": "title",
    "类型": "type",
    "来源": "source",
    "语言年代": "era",
    "关键数字": "key_numbers",
    "时间线": "timeline",
    "因果链": "causal_chain",
    "可用角度": "angles",
    "状态": "status",
}
ORDER = ["id", "title", "title_en", "type", "source", "era", "region", "year",
         "outcome", "industry", "tags", "key_numbers", "timeline",
         "causal_chain", "angles", "status"]

REGION_HINTS = [
    ("中国", "CN"), ("中文", "CN"), ("美国", "US"), ("英文", "US"), ("英国", "UK"),
    ("日本", "JP"), ("德国", "DE"), ("法国", "FR"), ("印度", "IN"), ("加拿大", "CA"),
    ("澳大利亚", "AU"), ("以色列", "IL"), ("巴西", "BR"), ("荷兰", "NL"),
    ("新加坡", "SG"), ("韩国", "KR"), ("西班牙", "ES"), ("瑞典", "SE"),
]


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


def guess_region(era):
    for k, code in REGION_HINTS:
        if k in era:
            return code
    return ""


def guess_year(era):
    ys = re.findall(r"(19|20)\d{2}", era)
    years = re.findall(r"(?:19|20)\d{2}", era)
    return years[0] if years else ""


def render(d, body):
    out = ["---"]
    for k in ORDER:
        v = d.get(k, "")
        if isinstance(v, list):
            v = "[" + ", ".join(v) + "]" if v else "[]"
        out.append(f"{k}: {v}".rstrip())
    out.append("---")
    return "\n".join(out) + "\n" + body


changed = 0
stats = {"region": 0, "year": 0}
for p in sorted(ROOT.glob("*/*.md")):
    t = p.read_text(encoding="utf-8")
    d, body = parse_fm(t)
    if d is None:
        print("跳过(无fm):", p.name)
        continue
    nd = {}
    for k, v in d.items():
        nd[KEYMAP.get(k, k)] = v
    era = nd.get("era", "")
    nd.setdefault("title_en", "")
    nd["region"] = nd.get("region") or guess_region(era)
    nd["year"] = nd.get("year") or guess_year(era)
    nd.setdefault("outcome", "")
    nd.setdefault("industry", "")
    nd.setdefault("tags", [])
    if nd["region"]:
        stats["region"] += 1
    if nd["year"]:
        stats["year"] += 1
    p.write_text(render(nd, body), encoding="utf-8")
    changed += 1

print("规范化:", changed)
print("可自动识别地区:", stats["region"], "/ 年份:", stats["year"])
