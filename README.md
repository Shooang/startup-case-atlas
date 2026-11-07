# 创业案例图谱 Startup Case Atlas

**简体中文** ｜ [English](README.en.md) ｜ [日本語](README.ja.md) ｜ [한국어](README.ko.md) ｜ [Español](README.es.md)

**419 个创业与生意案例，全部结构化，中文写作，机器可读。**

失败复盘、独立开发者的真实收入、以及中国街头小店那本账——房租多少、几个人、一份挣几毛、钱是怎么一天天用完的。

> English readers: 419 structured startup and small-business case studies, written in Chinese and machine-readable. [Read the English README →](README.en.md)

---

## 这是什么

讲创业的东西，大多两个毛病：成功的故事把数字抹掉，失败的故事把原因缩成"经营不善"四个字。

这个库想做的正相反：拿 419 个具体的生意，一个一个记下来——**它花了多少钱，挣了多少钱，钱到底去哪了，是哪一步把它弄塌的**。

每个案例是一个 Markdown 文件，16 个字段全都一样。淘宝卖家、深圳的硬件公司、上海的一碗面，用的是同一套骨架，所以能横向比、能筛、能直接喂给模型，不用先清洗。

有两件事让这个库跟别的不太一样：

**它记了那些通常没人记的生意。** 十平米的米线店、路边摊、首月流水七十万却亏二十多万的加盟火锅。中国小生意的经济账，在这里是具体到房租和进货价的，不是"行业平均"。

**它标了每个数字的来路。** 每个文件最后都有一节「事实边界」，写清这些数字是当事人自己说的、记者采访的、法院文书的，还是估算；哪些没法核实。有争议的地方，争议本身也写进去。

## 里面有什么

| 目录 | 篇数 | 内容 | 年代 |
| --- | --- | --- | --- |
| [`cases/01-personal-failure/`](cases/01-personal-failure/) | 4 | 当事人自己写的失败自述 | 2015–2024 |
| [`cases/02-founder-postmortems/`](cases/02-founder-postmortems/) | 25 | 创始人长文复盘，多为 B2B 与开发工具 | 2006–2016 |
| [`cases/03-failory/`](cases/03-failory/) | 129 | 二十多个国家的失败创业访谈 | 2020–2023 |
| [`cases/04-indie-hacker/`](cases/04-indie-hacker/) | 156 | 单人或小团队做付费产品 | 2019–2026 |
| [`cases/05-china-interviews/`](cases/05-china-interviews/) | 69 | 中国实体生意：餐饮、加盟、小店、服务 | 2018–2026 |
| [`cases/06-starter-story/`](cases/06-starter-story/) | 36 | 带月收入、启动成本、启动耗时的小生意 | 2019–2024 |
| [`legacy/articles/`](legacy/articles/) | 95 | 早期中文网络创业故事存档，多数原链接已失效 | 2000–2012 |

**合计：** 419 个案例 · 约 57.6 万字案例正文 · 95 篇存档文章 · 31 个国家和地区 · 13 个行业 · 5 种结局 · 12 类失败机制。

**有一个数字值得停一下：** 419 个案例里，246 个（59%）的失败机制是"需求错配"，比成本结构（118 个）多，比现金流断裂（93 个）多一倍半。横跨四十年、十五个国家、从一碗面馆到一个开发工具——生意死掉最常见的原因不是没钱，是做了一件没人要的东西，然后在发现这件事的过程中把钱用完了。

## 怎么用

### 想读

别从文件开始读，从索引开始。看你想要哪个角度：

- [按行业](index/by-industry.md)——餐饮、零售、电商、软件、硬件、服务
- [按结局](index/by-outcome.md)——失败、出售、转型、仍在营
- [按失败机制](index/by-mechanism.md)——加盟陷阱、现金流断裂、平台依赖、成本结构
- [按地区](index/by-region.md)——中国、美国、英国、印度等 31 个
- [按年份](index/by-year.md)——同一个错误，十年里怎么反复出现

### 想喂给模型

三个入口，看你上下文有多大：

```
llms.txt             # 结构说明 + 索引，约 2 KB，先读这个
data/cases.jsonl     # 419 条记录，每行一个 JSON，字段齐全
llms-full.txt        # 全部案例正文拼接，约 1.7 MB
data/cases.csv       # 表格用，标签已拍平
```

`llms.txt` 遵循 [llmstxt.org](https://llmstxt.org) 的约定。如果你的管道要切块，直接指向 `cases/**/*.md`——每个文件都是自包含的，单独拿出来也讲得通。

### 想查

```python
import json

cases = [json.loads(l) for l in open("data/cases.jsonl", encoding="utf-8")]

# 加盟 + 一年内现金流断裂的失败案例
hits = [c for c in cases
        if "franchise" in c["tags"]
        and "cashflow-crunch" in c["tags"]
        and c["outcome"] == "failure"]
```

## 字段规范

16 个字段，完整定义在 [`docs/schema.md`](docs/schema.md)。简版：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | `G001`–`G736`，空号是预留段 |
| `title` | string | 中文原标题，陈述事实，带关键数字 |
| `title_en` | string | 英文标题，8–14 词 |
| `type` | string | 来源类型：自述、访谈、报道、数据库 |
| `source` | url | 原文或原始访谈链接 |
| `era` | string | `语言·国别·年份`，按来源所写 |
| `source_language` | enum | `zh` \| `en` \| `unknown` |
| `region` | enum | 国家代码，未知写 `unknown`，**从不猜** |
| `year` | int | 事件起始年份 |
| `outcome` | enum | `failure` \| `success` \| `exit` \| `pivoted` \| `ongoing` |
| `industry` | enum | 13 个值，见分类说明 |
| `tags` | list | 2–5 个失败机制，取自 12 个闭合词 |
| `key_numbers` | string | 撑起这个故事的数字，用 `｜` 分隔 |
| `timeline` | string | 起点 → 转折 → 结局，各一句 |
| `causal_chain` | string | 一条主线因果，不是理由罗列 |
| `angles` | string | 这个案例能拿来论证什么 |
| `status` | string | 编务状态，不属于数据本身 |

每个案例正文固定三节：`## 故事正文`、`## 可用观点`、`## 事实边界`。

## 来源与许可

这是一个**衍生作品，不是镜像站**。这里没有一篇是把别人的文章复制粘贴过来的——每个案例都是基于已公开发表的内容重新写的中文记述，原文链接就在文件里。

- **案例正文**（419 篇）：[CC BY-SA 4.0](LICENSE)。可转载、可改编，需署名，衍生作品沿用同一许可。
- **其中 4 篇源自 [`byoungd/up`](https://github.com/byoungd/up)**：该项目正文为 **CC BY-NC 4.0**，这 4 篇同样**不可商用**。详见 [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md)。
- **存档文章**（`legacy/`）：版权归原作者与原发布方所有，仅为研究与索引目的收录，采用通知—删除机制。详见 [`DISCLAIMER.md`](DISCLAIMER.md)。

上游许可证原样保留在 [`third-party/`](third-party/)。每个来源的署名、抓取日期、具体用了什么，都列在 [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md)。

**如果你是权利人**，希望某篇内容下架，提 issue 或发邮件到 `DISCLAIMER.md` 里的地址，我们不争辩，直接删。

## 参与

**纠错比新增更值钱。** 如果这里的某个数字与原始出处矛盾，那是个 bug，请附上链接报过来。见 [`docs/contributing.md`](docs/contributing.md)。

新增案例欢迎，但要过三条：有能打开的原始链接、至少两个具体数字、失败机制具体到不是一个"经营不善"就能概括。没出处、靠推测写的，故事再好也退。

## 一点说明

这不是投资建议，也不是在给谁排聪明与否。一个案例出现在这里，只代表这门生意被记录过，不代表它被评判过。这里有些失败者，是在大部分事情上都做对了，只是没赶上时间。

---

*作为公开数据集维护。用于研究或产品时，附个回链会很高兴，但不必需。*
