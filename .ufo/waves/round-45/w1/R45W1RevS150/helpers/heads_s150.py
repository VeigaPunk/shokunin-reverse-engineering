import re, html
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
def clean(x):
    return re.sub(r"<[^>]+>", "", html.unescape(x)).strip()
h2 = [clean(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", t, re.S)]
h3 = [clean(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", t, re.S)]
print("h2 count", len(h2))
for x in h2:
    print("H2:", x)
print("h3 count", len(h3))
for x in h3:
    print("H3:", x)
print("any heading contains hint-chars:", any("\u30d2\u30f3\u30c8" in x for x in h2 + h3))
