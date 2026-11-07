import pathlib, re

ROOT = pathlib.Path("startup-case-atlas/cases")

COUNTRIES = {
    "中国": "CN", "美国": "US", "英国": "UK", "日本": "JP", "德国": "DE",
    "法国": "FR", "印度": "IN", "加拿大": "CA", "澳大利亚": "AU", "以色列": "IL",
    "巴西": "BR", "荷兰": "NL", "新加坡": "SG", "韩国": "KR", "西班牙": "ES",
    "瑞典": "SE", "意大利": "IT", "俄罗斯": "RU", "墨西哥": "MX", "印尼": "ID",
    "越南": "VN", "泰国": "TH", "波兰": "PL", "瑞士": "CH", "爱尔兰": "IE",
    "丹麦": "DK", "挪威": "NO", "芬兰": "FI", "新西兰": "NZ", "南非": "ZA",
    "土耳其": "TR", "阿联酋": "AE", "乌克兰": "UA", "葡萄牙": "PT", "奥地利": "AT",
    "比利时": "BE", "阿根廷": "AR", "智利": "CL", "哥伦比亚": "CO", "尼日利亚": "NG",
    "肯尼亚": "KE", "埃及": "EG", "巴基斯坦": "PK", "菲律宾": "PH", "马来西亚": "MY",
}

CITIES = {
    "CN": "青岛 上海 北京 成都 杭州 深圳 广州 武汉 长沙 西安 昆明 合肥 天津 常州 曲靖 临沂 济南 南京 苏州 宁波 重庆 郑州 沈阳 大连 厦门 福州 无锡 东莞 佛山 泉州 温州 台州 绍兴 嘉兴 金华 南昌 贵阳 南宁 石家庄 太原 兰州 哈尔滨 长春 珠海 中山 惠州 汕头 保定 唐山",
    "US": "纽约 旧金山 硅谷 西雅图 波士顿 奥斯汀 洛杉矶 芝加哥 迈阿密 丹佛 亚特兰大 圣地亚哥 波特兰 费城 休斯顿 达拉斯",
    "UK": "伦敦 曼彻斯特 爱丁堡 伯明翰",
    "DE": "柏林 慕尼黑 汉堡",
    "IN": "班加罗尔 孟买 新德里 海得拉巴",
    "JP": "东京 大阪 京都",
    "CA": "多伦多 温哥华 蒙特利尔",
    "AU": "悉尼 墨尔本",
    "IL": "特拉维夫",
    "BR": "圣保罗 里约",
    "NL": "阿姆斯特丹",
    "SG": "新加坡",
    "KR": "首尔",
    "ES": "巴塞罗那 马德里",
    "SE": "斯德哥尔摩",
    "FR": "巴黎",
}
CITY2C = {}
for code, names in CITIES.items():
    for n in names.split():
        CITY2C[n] = code

ORDER = ["id", "title", "title_en", "type", "source", "era", "source_language",
         "region", "year", "outcome", "industry", "tags", "key_numbers",
         "timeline", "causal_chain", "angles", "status"]


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return None, text
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip()
    return d, m.group(2)


def render(d, body):
    out = ["---"]
    for k in ORDER:
        v = d.get(k, "")
        if isinstance(v, list):
            v = "[" + ", ".join(v) + "]" if v else "[]"
        out.append(f"{k}: {v}".rstrip())
    out.append("---")
    return "\n".join(out) + "\n" + body


def language_of(era):
    if "英文" in era:
        return "en"
    if "中文" in era:
        return "zh"
    return "unknown"


def region_of(era):
    # 明确写了"国别未标注"的，绝不猜
    if "未标注" in era or "未标" in era:
        return "unknown"
    for name, code in COUNTRIES.items():
        if name in era:
            return code
    for name, code in CITY2C.items():
        if name in era:
            return code
    # 纯"中文译本""英文访谈中文翻译"这类，只有语言信息没有国别
    return "unknown"


changed = 0
stat = {}
for p in sorted(ROOT.glob("*/*.md")):
    t = p.read_text(encoding="utf-8")
    d, body = parse(t)
    if not d:
        continue
    era = d.get("era", "")
    d["source_language"] = language_of(era)
    d["region"] = region_of(era)
    p.write_text(render(d, body), encoding="utf-8")
    stat[d["region"]] = stat.get(d["region"], 0) + 1
    changed += 1

print("处理:", changed)
print("地区分布:", dict(sorted(stat.items(), key=lambda x: -x[1])))
