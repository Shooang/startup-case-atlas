# 分类词表 / Taxonomy

三个闭合词表：行业、结局、失败机制。**只能从这里取值，不允许自造。**

Closed vocabularies. Values must come from these lists — no free-form tags.

---

## 一、行业 `industry`（13 选 1）

| 值 | 中文 | 判断标准 | 典型例子 |
| --- | --- | --- | --- |
| `food-beverage` | 餐饮 | 卖吃的喝的，堂食或外卖 | 火锅自助、奶茶、面馆、烘焙 |
| `retail` | 零售 | 卖实物，有店面，非线上为主 | 便利店、社区超市、水果店 |
| `ecommerce` | 电商 | 线上成交为主 | 独立站、跨境、平台店铺 |
| `content-media` | 内容媒体 | 卖内容、流量、知识 | newsletter、课程、播客、社群 |
| `software-saas` | 软件与 SaaS | 卖软件使用权或订阅 | 工具站、API、插件、App |
| `hardware` | 硬件制造 | 有实物生产、模具、供应链 | 设备、消费电子、配件 |
| `services` | 本地服务 | 卖人力与时间，服务半径有限 | 民宿、美容、维修、宠物、家政 |
| `education` | 教育 | 教培、训练营、考试 | 学科培训、技能培训 |
| `gaming` | 游戏 | 游戏或游戏周边工具 | 独立游戏、游戏资产 |
| `fintech` | 金融 | 支付、借贷、理财、保险 | 支付工具、记账、保险科技 |
| `healthcare` | 医疗健康 | 医疗、康复、健康管理 | 诊所、康复、健康硬件 |
| `logistics` | 物流 | 运输、仓储、配送 | 同城配送、跨境物流 |
| `other` | 其他 | 确实无法归入以上 | 综合集团、跨界项目 |

**边界规则：**
- 一家店既卖餐又卖零售 → 看主营收入占比，多数选 `food-beverage`
- 软件公司卖硬件 → 看收入主体，硬件占比高选 `hardware`
- 内容创作者卖课 → `content-media`；正规教育机构 → `education`

---

## 二、结局 `outcome`（5 选 1）

| 值 | 中文 | 判断标准 |
| --- | --- | --- |
| `failure` | 失败关停 | 已停止运营，或明确退出、破产、清算 |
| `success` | 成功在营 | 仍在运营且有明确盈利或增长证据 |
| `exit` | 出售退出 | 被收购、并购、上市，创始人套现离场 |
| `pivoted` | 转型存活 | 原方向失败，换品类/换模式后活下来 |
| `ongoing` | 结果未定 | 仍在运营，但成败尚无定论；或报道停在中间 |

**注意：**
- 「亏钱但还在开」→ `ongoing`，不是 `failure`
- 「关掉 A 店开了 B 店，B 店赚钱」→ `pivoted`
- 「卖掉了但价格很低」→ `exit`，在 `causal_chain` 里写明价格

---

## 三、失败机制 `tags`（12 选 2–5）

这是本库最有价值的一层：把「经营不善」拆成可复用的判断点。

| 标签 | 中文 | 机制 | 识别信号 |
| --- | --- | --- | --- |
| `franchise` | 加盟授权 | 总部利润在供货、装修、抽成，不在门店销量 | 加盟费+强制采购+区域保护条款 |
| `low-price-trap` | 低价陷阱 | 引流价低于单份变动成本，卖越多亏越多 | 预售套餐、9.9 引流、爆单却亏损 |
| `traffic-dependency` | 流量依赖 | 收入押在单一渠道，渠道规则一变就断 | 全靠一个平台/一个爆款/一个网红 |
| `platform-risk` | 平台风险 | 平台政策、算法、抽佣变化直接致命 | 账号被封、规则调整、佣金翻倍 |
| `cashflow-crunch` | 现金流断裂 | 账面有收入但收不回、撑不到回本 | 备货压款、账期错配、扩张烧钱 |
| `supply-chain` | 供应链 | 进货价、履约、品质波动吃掉毛利 | 单一供应商、食材涨价、次品率 |
| `partnership-dispute` | 合伙纠纷 | 股权、分工、退出机制没谈清 | 兄弟创业、对赌、创始人内斗 |
| `product-market-fit` | 需求错配 | 做出来的东西没人真的需要 | 自嗨型产品、把爱好当市场 |
| `retention` | 复购留存 | 拉新成本收不回，客户只来一次 | 复购率低、靠不断买流量 |
| `cost-structure` | 成本结构 | 固定成本过重，客流一波动就亏 | 大店、高房租、重人力 |
| `scaling` | 扩张过快 | 单店模型没跑通就复制 | 一年开几十家、跨城扩张 |
| `pivot` | 转型 | 主动换方向，多为被迫 | 关店改品类、换赛道 |

**用法：**
- 一个案例通常命中 2–4 个。命中 5 个说明写得散，回去收敛
- `franchise` 与 `low-price-trap` 常同时出现——加盟总部的引流套餐是负毛利装置
- `cost-structure` 与 `cashflow-crunch` 是因果不是并列：前者是病灶，后者是死因

---

## 四、怎么用这套词表找选题

单一标签太宽，两个标签交叉才出选题：

| 交叉 | 能讲什么 |
| --- | --- |
| `franchise` + `cashflow-crunch` | 加盟商的钱是怎么在四个月里烧完的 |
| `low-price-trap` + `retention` | 爆单为什么不等于赚钱 |
| `traffic-dependency` + `platform-risk` | 平台一封号，生意归零 |
| `cost-structure` + `scaling` | 单店没跑通就复制，越开越亏 |
| `partnership-dispute` + `exit` | 股权没谈清，卖公司时撕破脸 |

```python
import json
cases = [json.loads(l) for l in open("data/cases.jsonl", encoding="utf-8")]

def cross(a, b, outcome=None):
    return [c for c in cases
            if a in c["tags"] and b in c["tags"]
            and (outcome is None or c["outcome"] == outcome)]
```
