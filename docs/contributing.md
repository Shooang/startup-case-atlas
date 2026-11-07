# 贡献指南 / Contributing

## 最欢迎的贡献：纠错

**这里的错误比缺失更有害。** 一个数字错了，整个库的可信度都要打折。

如果你发现某个案例与原始出处不符，请提 issue，附上：

- 案例 ID（如 `G623`）
- 错的字段（`key_numbers` / `timeline` / `causal_chain`）
- 原文链接与截图（如果原页面还在）
- 正确的内容

核实后我们会更正，并在文件末尾的「事实边界」里注明修订记录。

## 次欢迎的贡献：补链接

`legacy/articles/` 里有 90 篇保留了原始 URL，但多数已失效。如果你知道某篇文章的存档地址（Wayback Machine、archive.today、其他转载），欢迎补充。

有 5 篇的链接彻底丢失了，如果你能认出来源，那也有价值。

## 新增案例的门槛

新增案例要过四条，缺一条就不收：

1. **有能打开的原始链接。** 不接受「听朋友说」「网上看到的」
2. **至少两个具体数字。** 启动资金、月流水、亏损额、单价、房租、毛利率，任意两个。只是「投入不少」「挣得还行」这种，不收
3. **有具体的地点或时间。** 哪个城市、哪一年。匿名到无法定位的，不收
4. **失败机制具体。** 能落到 12 个标签里的至少一个，不是「经营不善」

**明确不收的：**

- AI 生成的内容农场文章（特征：段落工整对仗、每段以金句收尾、数字全是整数没有来源）
- 匿名软文（「某先生」「一位创业者」，无城市无时间）
- 加盟招商导流稿（结尾留微信、留电话、导向加盟）
- 只有融资快讯没有故事的（「XX 宣布完成 A 轮」）
- 只有观点没有账的目的论文章
- 短视频平台的口播笔记（只有结论没有过程）

## 提交格式

1. Fork 本仓库
2. 新建文件 `cases/<分类>/G<编号>-<短标题>.md`
3. 按 [`docs/schema.md`](schema.md) 填 16 个字段，正文三节
4. `industry`、`outcome`、`tags` 必须从 [`docs/taxonomy.md`](taxonomy.md) 的词表取值
5. 跑一遍 `python3 scripts/validate.py`，确保通过
6. 提 PR，说明：素材来源、为什么这个案例值得收录

**编号规则**：新案例从 `G801` 起顺延，不要占用现有号段（`G001–G736`）。如果有人同时在提，以合并顺序为准。

## 写作纪律

这几条是这个库能看的原因，请遵守：

**只用原文出现过的数字。** 一个都不许补。不确定就不写。原文说「六七十万」，不要写成「约 65 万」。

**不换算货币。** 美元就是美元，日元就是日元。不折人民币，不折今天购买力。

**不写「这告诉我们」。** 可用观点落在机制上——房租占营收多少、翻台率要几轮、毛利被谁吃掉——不落在「坚持很重要」。

**第三人称。** 原始访谈是第一人称的，转成第三人称叙述，关键引语可以保留。

**涉及具体个人与公司只写公开内容。** 破产、债务、诉讼、裁员这些，只陈述报道中的说法，不加评判，不做道德总结。

**化名受访者不可指认。** 文中的「王先生」「李女士」如果原文就是化名，卡内要标注「不可指认真实身份」。

## 修订流程

| 类型 | 处理 |
| --- | --- |
| 数字错误 | 直接改，在事实边界注明 |
| 链接失效 | 找存档替换；找不到就标「原链接已失效」 |
| 分类争议 | 以 taxonom 定义为准，可以提 issue 讨论改定义 |
| 权利人要求下架 | 72 小时内删除，不问理由 |

## English

The most valuable contribution is a **correction**, not an addition. If a figure here contradicts its source, that is a bug — report it with the link.

New cases must have: a working source link, at least two specific figures, a real place and year, and a failure mechanism more specific than "it failed." AI-generated content farms, anonymous advertorials, franchise recruitment posts and funding-round press releases are rejected on sight.

Field names and vocabularies are fixed. Run `scripts/validate.py` before opening a PR.
