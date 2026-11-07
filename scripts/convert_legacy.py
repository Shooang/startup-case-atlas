import pathlib, re, subprocess, unicodedata

SRC = pathlib.Path("本地内容口播/创业及故事")
DST = pathlib.Path("startup-case-atlas/legacy/articles")

EXCLUDE = {
    "18位英语大师为你归纳英语学习方法.doc",
    "2010最佳商业模式.doc",
    "2011最新淘宝推广方案.doc",
    "6 淘宝网店网络推广方案.doc",
    "支持淘宝客链接的论坛大全.doc",
    "淘宝客推广从入门到精通.doc",
    "淘宝店铺网络推广策略.doc",
    "淘宝网店的网络营销方案.doc",
    "淘宝网店运营方案.doc",
    "淘宝网开店创业经营指导方案.doc",
    "王石简历.doc",
    "马云语录.doc",
    "16 郭台铭语录.doc",
    "22 市场与多样性(1).doc",
}

URL_RE = re.compile(r'https?://[^\s"\'<>()\u4e00-\u9fff]+')


def clean(txt: str):
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    # 去掉 Word 的 HYPERLINK 域残留
    txt = re.sub(r'\s*HYPERLINK\s+"([^"]*)"', "", txt)
    txt = re.sub(r'\s*\\t\s*"_blank"\s*', " ", txt)
    txt = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", txt)
    txt = unicodedata.normalize("NFKC", txt)
    lines = [ln.strip() for ln in txt.split("\n")]
    txt = "\n".join(lines)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


rows = []
idx = 0
for p in sorted(SRC.glob("*.doc")):
    if p.name in EXCLUDE:
        continue
    raw = subprocess.run(
        ["textutil", "-convert", "txt", "-stdout", str(p)],
        capture_output=True,
    )
    txt = raw.stdout.decode("utf-8", errors="ignore")
    if not txt.strip():
        print("空内容:", p.name)
        continue
    urls = URL_RE.findall(txt)
    txt = clean(txt)
    if len(txt) < 150:
        print("过短跳过:", p.name, len(txt))
        continue
    idx += 1
    cid = f"L{idx:03d}"
    title = re.sub(r"^\d+\s*[-－]?\s*", "", p.stem).strip()
    title = re.sub(r"\(\d+\)$", "", title).strip()
    src_url = urls[0].rstrip("/") if urls else ""
    body = "\n".join(f"> {ln}" if ln else "" for ln in [])
    fm = [
        "---",
        f"id: {cid}",
        f"title: {title}",
        "type: legacy-article",
        f"source_url: {src_url}",
        "source_type: 早期公开网页转载（原站多数已无法访问）",
        "language: zh",
        "license: third-party-unknown",
        "rights_note: 版权归原作者及原发布方，本库仅作研究与索引存档",
        "---",
        "",
        f"# {title}",
        "",
        "> 本文件为早期搜集的公开文章存档，原始出处见文末。版权不归本库所有，",
        "> 如权利人提出异议，将第一时间删除。",
        "",
        txt,
        "",
        "---",
        "",
        "**原始链接**：" + (src_url if src_url else "链接已在多次转存中丢失"),
    ]
    DST.mkdir(parents=True, exist_ok=True)
    (DST / f"{cid}-{title[:40]}.md").write_text("\n".join(fm), encoding="utf-8")
    rows.append((cid, title, src_url, len(txt)))

print("转换成功:", len(rows))
with_url = sum(1 for r in rows if r[2])
print("有原始链接:", with_url, "｜无链接:", len(rows) - with_url)
print("总字数:", sum(r[3] for r in rows))
print("最短三篇:", sorted(rows, key=lambda r: r[3])[:3])
