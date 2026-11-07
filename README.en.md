# Startup Case Atlas

[简体中文](README.md) ｜ **English** ｜ [日本語](README.ja.md) ｜ [한국어](README.ko.md) ｜ [Español](README.es.md)

**419 structured case studies of startups and small businesses — written in Chinese, queryable by machine.**

Failure post-mortems, solo-founder revenue numbers, and the actual books of Chinese street-level businesses: rents, headcount, per-unit margin, and how the cash ran out.

---

## What this is

Most startup writing is either a success story with the numbers removed, or a failure story with the cause reduced to "poor management". This atlas is an attempt to do the opposite: take 419 individual businesses, and record for each one **what it cost, what it earned, where the money actually went, and which decision broke it**.

Every case is a single Markdown file with the same 16 fields. Same shape for a Taobao seller, a Shenzhen hardware startup, and a noodle shop in Shanghai — so they can be compared, filtered, and fed to a model without cleaning.

Two things make this collection unusual:

**It includes businesses that usually go unrecorded.** A 10-square-metre rice-noodle shop. A street stall. A franchise hotpot restaurant that did 700,000 RMB in its first month and still lost 200,000. Chinese small-business economics are documented here at the level of individual rent and ingredient costs, not industry averages.

**It documents where the numbers come from.** Every file ends with a "facts and limits" section that states whether the figures are the founder's own account, a reporter's interview, a court filing, or an estimate — and what could not be verified. If a number is disputed, the dispute is written down.

## What's inside

| Directory | Cases | Coverage | Period |
| --- | --- | --- | --- |
| [`cases/01-personal-failure/`](cases/01-personal-failure/) | 4 | First-person failure accounts, written by the founders themselves | 2015–2024 |
| [`cases/02-founder-postmortems/`](cases/02-founder-postmortems/) | 25 | Long-form founder post-mortems, mostly B2B and developer tools | 2006–2016 |
| [`cases/03-failory/`](cases/03-failory/) | 129 | Founder interviews on failed startups across 20+ countries | 2020–2023 |
| [`cases/04-indie-hacker/`](cases/04-indie-hacker/) | 156 | Solo founders and small teams shipping paid products | 2019–2026 |
| [`cases/05-china-interviews/`](cases/05-china-interviews/) | 69 | Chinese physical businesses: restaurants, franchises, shops, services | 2018–2026 |
| [`cases/06-starter-story/`](cases/06-starter-story/) | 36 | Revenue, launch cost, and time-to-launch for small ventures | 2019–2024 |
| [`legacy/articles/`](legacy/articles/) | 95 | Archive of early Chinese web articles on entrepreneurs, mostly dead links | 2000–2012 |

**Totals:** 419 cases · ~576,000 Chinese characters of case text · 95 archived articles · 31 countries and regions · 13 industries · 5 outcome types · 12 failure mechanisms.

**One number worth pausing on:** 246 of 419 cases (59%) carry `product-market-fit` as a failure mechanism — more than cost structure (118), more than running out of cash (93). Across four decades, fifteen countries and everything from a noodle shop to a developer tool, the most common way a business dies is not that it ran out of money. It is that it built something nobody wanted, and the money ran out while finding that out.

## Quick start

### Reading

Start with an index, not a file. If you want a specific angle:

- [By industry](index/by-industry.md) — restaurants, retail, e-commerce, software, hardware, services
- [By outcome](index/by-outcome.md) — failure, exit, pivoted, still running
- [By failure mechanism](index/by-mechanism.md) — franchise traps, cash-flow collapse, platform dependency, cost structure
- [By region](index/by-region.md) — China, US, UK, India, and 27 more
- [By year](index/by-year.md) — how the same mistake repeats across a decade

### Feeding a model

Three entry points, depending on how much context you have:

```
llms.txt             # structure + index, ~2 KB, read this first
data/cases.jsonl     # 419 records, one JSON object per line, all fields
llms-full.txt        # every case body concatenated, ~1.7 MB
data/cases.csv       # spreadsheet-friendly, flattened tags
```

`llms.txt` follows the [llmstxt.org](https://llmstxt.org) convention. If your pipeline chunks documents, point it at `cases/**/*.md` — each file is self-contained and stands alone.

### Querying

```python
import json

cases = [json.loads(l) for l in open("data/cases.jsonl", encoding="utf-8")]

# franchise failures where the cash ran out within a year
hits = [c for c in cases
        if "franchise" in c["tags"]
        and "cashflow-crunch" in c["tags"]
        and c["outcome"] == "failure"]
```

## Schema

16 fields, defined once in [`docs/schema.md`](docs/schema.md). The short version:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | `G001`–`G736`, gaps are reserved |
| `title` | string | Original Chinese headline, factual, carries the key number |
| `title_en` | string | English rendering, 8–14 words |
| `type` | string | Provenance type: first-person, interview, reportage, database |
| `source` | url | Link to the original article or interview |
| `era` | string | `language · country · year`, as stated at source |
| `source_language` | enum | `zh` \| `en` \| `unknown` |
| `region` | enum | ISO-ish country code, or `unknown` — never guessed |
| `year` | int | Year the events began |
| `outcome` | enum | `failure` \| `success` \| `exit` \| `pivoted` \| `ongoing` |
| `industry` | enum | 13 values, see taxonomy |
| `tags` | list | 2–5 failure mechanisms from a closed list of 12 |
| `key_numbers` | string | The figures that carry the story, `｜`-separated |
| `timeline` | string | Onset → turning point → outcome, one line each |
| `causal_chain` | string | The single main causal thread, not a list of reasons |
| `angles` | string | What this case can be used to argue |
| `status` | string | Editorial state, not part of the data proper |

Every case body has three fixed sections: `## Story`, `## Usable angles`, `## Facts and limits`.

## Sources and licensing

This is a **derived work, not a mirror**. Nothing here is a copy-paste of someone else's article. Each case is an original Chinese-language write-up based on published reporting, with the source linked in the file itself.

- **Case notes** (419 files): released under [CC BY-SA 4.0](LICENSE). Share and adapt, credit required, derivatives under the same terms.
- **Four cases derived from [`byoungd/up`](https://github.com/byoungd/up)**: that project's prose is **CC BY-NC 4.0**. Those cases carry the same non-commercial restriction. See [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).
- **Archived articles** (`legacy/`): copyright remains with the original authors and publishers. Included for research and indexing only, under a notice-and-takedown arrangement. See [`DISCLAIMER.md`](DISCLAIMER.md).

Upstream licenses are preserved verbatim in [`third-party/`](third-party/). Per-source attribution, retrieval dates, and what exactly was reused are listed in [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).

**If you are a rights holder** and want something removed, open an issue or email the address in `DISCLAIMER.md`. It will be taken down without argument.

## Contributing

Corrections are more valuable than additions. If a number here contradicts the original source, that is a bug — please report it with the link. See [`docs/contributing.md`](docs/contributing.md).

New cases are welcome if they meet three conditions: a working source link, at least two specific figures, and a mechanism more specific than "it failed". Speculative or unsourced write-ups get rejected, however good the story.

## A note on what this is not

This is not investment advice, and it is not a ranking of who is smart and who is not. A case appearing here means the business was documented, not that it was judged. Several of the failures are people who did most things right and ran out of time.

---

*Maintained as a public dataset. If you use it in research or a product, a link back is appreciated but not required.*
