import re, html, json
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
u = html.unescape(t)
rows = re.findall(r"<tr[^>]*>\s*<td>(\u7b2c\S+?)</td>\s*<td><a href=\"([^\"]+)\"[^>]*>([^<]*)</a>", u)
out = [{"part": p, "url": w, "title": ti} for p, w, ti in rows]
json.dump(out, open("series-rows.json", "w"), ensure_ascii=False, indent=1)
for r in out:
    print(r["part"], r["url"], r["title"])
print("rows", len(out))
for part in ("\u7b2c6\u56de", "\u7b2c4\u56de"):
    print(part, "count", u.count(part))
print("heading パターン認識のコツ count", u.count("\u30d1\u30bf\u30fc\u30f3\u8a8d\u8b58\u306e\u30b3\u30c4"))
print("llvm-objdump lines", sum(1 for l in u.splitlines() if "llvm-objdump" in l), "occ", u.count("llvm-objdump"))
