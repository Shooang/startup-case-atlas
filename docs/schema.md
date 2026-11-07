# 字段规范 / Schema

每个案例是一个 Markdown 文件，由 YAML front matter 与三段固定正文构成。字段名固定为英文，值以中文为主，便于人和机器同时读。

Every case is one Markdown file: YAML front matter plus three fixed sections. Field names are English, values are mostly Chinese.

```yaml
---
id: G623
title: 卖房凑150万加盟火锅自助，首月流水70万反而亏20多万，四个月闭店
title_en: Sold his house for 1.5M RMB to join a buffet chain, closed in four months
type: 中文小生意
source: https://cbgc.scol.com.cn/news/7946483
era: 中文·青岛·2025-2026
source_language: zh
region: CN
year: 2025
outcome: failure
industry: food-beverage
tags: [franchise, low-price-trap, cashflow-crunch, cost-structure]
key_numbers: 总投入150多万（加盟费十几万＋装修40多万＋备货七八十万）｜首月流水六七十万、净亏20多万｜59.9元引流套餐预售近80万｜4个月闭店
timeline: 2025年11月刷到招商信息 → 到青岛开店、卖房凑钱 → 首月流水六七十万却亏20多万 → 第二个月自主采购调价、亏损收窄到三四万 → 第四个月付不出工资房租闭店 → 去总部发现办公室已搬空
causal_chain: 招商话术承诺"一年盈利200多万"，总部靠指定采购和装修抽利；59.9元引流套餐卖得越多亏得越多，流水做了起来、成本结构是坏的；低毛利撑不住高固定成本，现金流四个月断裂
angles: 加盟总部的利润在供货不在你的店／引流套餐是负毛利陷阱／"流水好看"和"成本结构健康"是两回事
status: 未使用
---
```

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | string | 是 | `G` + 三位数字。编号分段预留，空号属正常 |
| `title` | string | 是 | 中文标题。陈述事实，带上最能说明问题的数字。不用问句，不用感叹号 |
| `title_en` | string | 是 | 英文标题，8–14 词。同样是陈述句，保留关键数字。人民币按 `RMB` 写 |
| `type` | string | 是 | 来源类型，见下表 |
| `source` | url | 是 | 原文链接。无法定位到具体文章时写站点首页，并在 `type` 中说明 |
| `era` | string | 是 | `语言·国别·年份`，保留来源的原始表述。国别不明就写「国别未标注」 |
| `source_language` | enum | 是 | `zh` / `en` / `unknown`。指**原始素材**的语言，不是本卡语言 |
| `region` | enum | 是 | ISO 3166-1 alpha-2 国家代码，或 `unknown`。**不允许猜测**，来源没写就填 `unknown` |
| `year` | int | 是 | 事件起始年份。跨年的取起点 |
| `outcome` | enum | 是 | 见 `taxonomy.md` |
| `industry` | enum | 是 | 见 `taxonomy.md`，13 选 1 |
| `tags` | list | 是 | 2–5 个，取自 12 个闭合词。不允许自造 |
| `key_numbers` | string | 是 | 撑起这个故事的数字，用 `｜` 分隔。原币种，不换算，不四舍五入 |
| `timeline` | string | 是 | `起点 → 转折 → 结局`，用 ` → ` 连接，每段一句 |
| `causal_chain` | string | 是 | **一条**主线因果，不是理由罗列。用分号串联，不超过四句 |
| `angles` | string | 是 | 这个案例能用来论证什么，用 `／` 分隔，3 条以内 |
| `status` | string | 是 | 编务状态（未使用 / 已用于第 N 期），不属于数据本身 |

## `type` 取值

| 值 | 含义 |
| --- | --- |
| `中文自述` | 当事人自己写的第一人称长文 |
| `中文小生意` | 记者实地采访的实体小生意 |
| `中文创业报道` | 媒体对公司/创始人的深度报道 |
| `中文失败复盘` | 关店、倒闭、清算的复盘 |
| `中文访谈` | 创业者深度访谈逐字稿 |
| `独立开发变现` | 单人/小团队产品的收入复盘 |
| `失败访谈` | 第三方平台做的失败创始人问答 |
| `创始人文` | 创始人自己写的长文 post-mortem |
| `真实生意案例` | 带收入/成本字段的标准化案例 |
| `legacy-article` | 早期网页文章存档 |

## 正文三节

```markdown
## 故事正文
600–900 字。有场景、有数字、有转折。不是摘要罗列，是把账一笔一笔摆出来。

## 可用观点
3 条以内。落在具体商业机制上（房租占比、翻台率、毛利、回本周期、平台抽佣），
不写"这告诉我们坚持很重要"这类。

## 事实边界
写清：出处媒体与标题、发布日期、是当事人自述还是记者转述、
哪些数字是当事人回忆、哪些无法核实、有无争议。
```

## 校验

```bash
python3 scripts/validate.py      # 字段完整性、枚举合法性、正文长度
python3 scripts/build_data.py    # 重新生成 jsonl / csv / 索引 / llms.txt
```

## English summary

Sixteen fields, fixed names, Chinese values. The two rules that matter most:

**`region` is never guessed.** If the source does not state a country, the field is `unknown`. A dataset that infers geography from language is worse than one that admits a gap.

**`key_numbers` is never converted.** Currencies stay as published. A 2021 figure in pounds is not translated into today's dollars, because the point of the number is what the founder faced, not what it equals now.
