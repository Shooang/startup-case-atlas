import pathlib, re, shutil, sys

src = pathlib.Path("本地内容口播/创业及故事/GITHUB精选")
dst = pathlib.Path("startup-case-atlas")


def bucket(n):
    if 1 <= n <= 4:
        return "01-personal-failure"
    if 101 <= n <= 125:
        return "02-founder-postmortems"
    if 301 <= n <= 429:
        return "03-failory"
    if (201 <= n <= 296) or (433 <= n <= 492):
        return "04-indie-hacker"
    if 601 <= n <= 696:
        return "05-china-interviews"
    if 701 <= n <= 736:
        return "06-starter-story"
    return None


cnt = {}
skip = []
done = 0
for p in sorted(src.glob("0*/G*.md")):
    m = re.match(r"G(\d+)", p.name)
    if not m:
        skip.append(p.name)
        continue
    b = bucket(int(m.group(1)))
    if not b:
        skip.append(p.name)
        continue
    target = dst / "cases" / b / p.name
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        done += 1
    cnt[b] = cnt.get(b, 0) + 1

print("新复制:", done)
for k in sorted(cnt):
    print(f"  {k}: {cnt[k]}")
print("合计:", sum(cnt.values()))
print("跳过:", skip)
