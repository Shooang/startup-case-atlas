import pathlib, re, json, csv, collections

BASE = pathlib.Path("startup-case-atlas")
CASES = BASE / "cases"
LEGACY = BASE / "legacy" / "articles"
DATA = BASE / "data"
INDEX = BASE / "index"

INDUSTRY_ZH = {
    "food-beverage": "餐饮", "retail": "零售", "ecommerce": "电商",
    "content-media": "内容媒体", "software-saas": "软件与 SaaS", "hardware": "硬件制造",
    "services": "本地服务", "education": "教育", "gaming": "游戏",
    "fintech": "金融", "healthcare": "医疗健康", "logistics": "物流", "other": "其他",
}
OUTCOME_ZH = {"failure": "失败关停", "success": "成功在营", "exit": "出售退出",
              "pivoted": "转型存活", "ongoing": "结果未定"}
TAG_ZH = {
    "franchise": "加盟授权", "low-price-trap": "低价陷阱", "traffic-dependency": "流量依赖",
    "platform-risk": "平台风险", "cashflow-crunch": "现金流断裂", "supply-chain": "供应链",
    "partnership-dispute": "合伙纠纷", "product-market-fit": "需求错配",
    "retention": "复购留存", "cost-structure": "成本结构", "scaling": "扩张过快",
    "pivot": "转型",
    # 司法判决案例新增
    "contract-dispute": "合同纠纷", "false-advertising": "虚假宣传",
    "qualification": "资质门槛",
    "labor-dispute": "劳动纠纷", "ip-infringement": "知识产权侵权",
    "equity-dispute": "股权代持与出资",
    "prepaid-card": "预付卡跑路",
}


def parse(path):
    t = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", t, re.S)
    if not m:
        return None, t
    d = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            d[k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        else:
            d[k] = v
    return d, m.group(2)


rows = []
for p in sorted(CASES.glob("*/*.md")):
    d, body = parse(p)
    if not d:
        continue
    rows.append({
        "id": d.get("id", ""),
        "title": d.get("title", ""),
        "title_en": d.get("title_en", ""),
        "type": d.get("type", ""),
        "source": d.get("source", ""),
        "era": d.get("era", ""),
        "region": d.get("region", ""),
        "year": d.get("year", ""),
        "outcome": d.get("outcome", ""),
        "industry": d.get("industry", ""),
        "tags": d.get("tags", []),
        "key_numbers": d.get("key_numbers", ""),
        "timeline": d.get("timeline", ""),
        "causal_chain": d.get("causal_chain", ""),
        "angles": d.get("angles", ""),
        "status": d.get("status", ""),
        "path": str(p.relative_to(BASE)),
        "body": body.strip(),
    })

legacy = []
for p in sorted(LEGACY.glob("*.md")):
    d, body = parse(p)
    if not d:
        continue
    legacy.append({
        "id": d.get("id", ""), "title": d.get("title", ""),
        "source_url": d.get("source_url", ""), "license": d.get("license", ""),
        "path": str(p.relative_to(BASE)), "chars": len(body),
    })

DATA.mkdir(parents=True, exist_ok=True)
INDEX.mkdir(parents=True, exist_ok=True)

# 1. JSONL
with (DATA / "cases.jsonl").open("w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

# 2. CSV
cols = ["id", "title", "title_en", "type", "industry", "outcome", "region", "year",
        "tags", "source", "key_numbers", "path"]
with (DATA / "cases.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        rr = dict(r)
        rr["tags"] = "|".join(r["tags"])
        w.writerow(rr)

# 3. 索引
def table(items, extra=None):
    out = ["| ID | 标题 | 英文标题 | 行业 | 结局 | 地区·年份 | 关键数字 |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in items:
        t = r["title"] if len(r["title"]) <= 26 else r["title"][:25] + "…"
        te = r["title_en"] if len(r["title_en"]) <= 42 else r["title_en"][:41] + "…"
        kn = r["key_numbers"] if len(r["key_numbers"]) <= 46 else r["key_numbers"][:45] + "…"
        out.append(f"| [{r['id']}](../{r['path']}) | {t} | {te} | "
                   f"{INDUSTRY_ZH.get(r['industry'], r['industry'])} | "
                   f"{OUTCOME_ZH.get(r['outcome'], r['outcome'])} | "
                   f"{r['region']}·{r['year']} | {kn} |")
    return out


def write_dim(name, title, desc, keyfn, dictzh):
    groups = collections.defaultdict(list)
    for r in rows:
        v = keyfn(r)
        if isinstance(v, list):
            for x in v:
                groups[x].append(r)
        else:
            groups[v].append(r)
    lines = [f"# {title}", "", f"> {desc}", "",
             f"> 共 {len(rows)} 个案例。按此维度去重后 {len(groups)} 组。", ""]
    for k in sorted(groups, key=lambda x: -len(groups[x])):
        label = dictzh.get(k, k) if dictzh else k
        lines.append(f"## {label} ({len(groups[k])})")
        lines.append("")
        lines += table(groups[k])
        lines.append("")
    (INDEX / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")


write_dim("by-industry", "按行业索引", "同一门生意里的不同打法，横向对比用这张表。",
          lambda r: r["industry"], INDUSTRY_ZH)
write_dim("by-outcome", "按结局索引", "失败、出售、转型、在营，结局决定这案例能讲什么。",
          lambda r: r["outcome"], OUTCOME_ZH)
write_dim("by-mechanism", "按失败机制索引", "每个标签是一个可复用的判断点，写选题时按机制找案例。",
          lambda r: r["tags"] if r["tags"] else ["untagged"], TAG_ZH)
write_dim("by-region", "按地区索引", "英文案例必须交代国别，中文案例注意城市。",
          lambda r: r["region"], {"CN": "中国", "US": "美国", "UK": "英国", "JP": "日本",
                                  "DE": "德国", "IN": "印度", "CA": "加拿大", "AU": "澳大利亚",
                                  "IL": "以色列", "BR": "巴西", "NL": "荷兰", "SG": "新加坡",
                                  "KR": "韩国", "ES": "西班牙", "SE": "瑞典", "FR": "法国"})
write_dim("by-year", "按年份索引", "按案例发生年份排序，看风口起落。",
          lambda r: r["year"], None)

# 4. llms.txt
_fw_files = sorted((BASE / "frameworks").glob("F*.md"))
_fw_n = len(_fw_files)
_fw_books = set()
for _f in _fw_files:
    _m = re.search(r"^book: (.+)$", _f.read_text(encoding="utf-8"), re.M)
    if _m:
        _fw_books.add(_m.group(1).strip())
_fw_b = len(_fw_books)
_dir_n = collections.Counter(str(pathlib.Path(r["path"]).parent) for r in rows)
def _dn(d):
    return _dir_n.get(d, 0)
ll = ["# Startup Case Atlas", "",
      f"> {len(rows)} 个创业与生意案例的结构化中文库，覆盖失败复盘、独立开发变现、中国小店账本、"
      "真实生意收入数据、司法判决里的生意纠纷。每个案例字段统一：行业、结局、地区、年份、关键数字、时间线、因果链、可用角度。",
      "",
      "## 使用方式", "",
      "- 单篇：`cases/<分类>/<ID>-<标题>.md`，YAML front matter 可直接解析",
      "- 批量：`data/cases.jsonl`（每行一个案例，含全部字段）",
      "- 表格：`data/cases.csv`",
      f"- 全文：`llms-full.txt`（全部案例正文拼接，约 {sum(len(r['body']) for r in rows)//10000} 万字）",
      "",
      "## 分类目录", "",
      f"- [个人失败自述](cases/01-personal-failure/)：{_dn('cases/01-personal-failure')} 篇，当事人自己写的",
      f"- [创始人文复盘](cases/02-founder-postmortems/)：{_dn('cases/02-founder-postmortems')} 篇，2006-2016 为主",
      f"- [失败访谈 Failory](cases/03-failory/)：{_dn('cases/03-failory')} 篇，2020-2023 多国",
      f"- [独立开发变现](cases/04-indie-hacker/)：{_dn('cases/04-indie-hacker')} 篇，单人产品与订阅生意",
      f"- [中文创业访谈与小店](cases/05-china-interviews/)：{_dn('cases/05-china-interviews')} 篇，2019 年后中国实体生意账本",
      f"- [真实生意数据库](cases/06-starter-story/)：{_dn('cases/06-starter-story')} 篇，带月收入与启动成本",
      f"- [司法判决案例](cases/07-judgments/)：{_dn('cases/07-judgments')} 篇，法院生效判决与最高法案例库入库案例：加盟、合伙散伙、对赌、货款、竞业、商标、代持、预付卡、工程款、二手车、装修、直播、劳务派遣、医美、宠物、驾校、婚介、口腔正畸、助贷",
      "",
      "## 索引", "",
      "- [按行业](index/by-industry.md)", "- [按结局](index/by-outcome.md)",
      "- [按失败机制](index/by-mechanism.md)", "- [按地区](index/by-region.md)",
      "- [按年份](index/by-year.md)", "",
      "## 框架卡", "",
      f"{_fw_n} 张判断工具卡，从 {_fw_b} 本书与课程里提取，每张 2000-2700 字，含「出处与边界」一节说明方法失效的条件。", "",
      "- [按书/课程浏览](index/frameworks-by-book.md)",
      "- [按领域](index/frameworks-by-doctrine.md)",
      "- [全部开场句](index/frameworks-hooks.md)——写稿时可直接念",
      "- 批量：`data/frameworks.jsonl` / `data/frameworks.csv`", ""]
(BASE / "llms.txt").write_text("\n".join(ll), encoding="utf-8")

# 5. llms-full.txt（仅原创卡片，不含 legacy 全文）
fl = ["# Startup Case Atlas — Full Text", "",
      f"> {len(rows)} 个案例的完整正文。每条含 front matter 与三段正文。", ""]
for r in rows:
    fl.append(f"\n\n===== {r['id']} | {r['title']} | {r['title_en']} =====\n")
    fl.append(f"行业: {r['industry']} | 结局: {r['outcome']} | 地区: {r['region']} | 年份: {r['year']}")
    fl.append(f"关键数字: {r['key_numbers']}")
    fl.append(f"因果链: {r['causal_chain']}")
    fl.append(f"可用角度: {r['angles']}")
    fl.append("\n" + r["body"])
(BASE / "llms-full.txt").write_text("\n".join(fl), encoding="utf-8")

# 6. legacy 索引
lg = ["# 早期文章存档索引", "",
      f"> {len(legacy)} 篇 2010 年前后从公开网页搜集的创业故事原文，多数原站已无法访问。",
      "> **版权归原作者及原发布方**，本库仅作研究与索引存档，收到权利人通知即删除。", "",
      "| ID | 标题 | 原始链接 | 字数 | 文件 |", "| --- | --- | --- | --- | --- |"]
for r in legacy:
    u = r["source_url"] or "（原链接已丢失）"
    lg.append(f"| {r['id']} | {r['title']} | {u} | {r['chars']} | [{r['id']}](../{r['path']}) |")
(INDEX / "legacy-archive.md").write_text("\n".join(lg), encoding="utf-8")

# 7. 统计
stat = {
    "cases": len(rows),
    "legacy": len(legacy),
    "by_industry": dict(collections.Counter(r["industry"] for r in rows)),
    "by_outcome": dict(collections.Counter(r["outcome"] for r in rows)),
    "by_region": dict(collections.Counter(r["region"] for r in rows)),
    "total_body_chars": sum(len(r["body"]) for r in rows),
    "legacy_chars": sum(r["chars"] for r in legacy),
}
(DATA / "stats.json").write_text(json.dumps(stat, ensure_ascii=False, indent=2), encoding="utf-8")

print("案例:", len(rows), "| 存档:", len(legacy))
print("行业:", dict(sorted(stat["by_industry"].items(), key=lambda x: -x[1])))
print("结局:", stat["by_outcome"])
print("地区:", dict(sorted(stat["by_region"].items(), key=lambda x: -x[1])))
print("卡片正文总字数:", stat["total_body_chars"], "| 存档字数:", stat["legacy_chars"])
