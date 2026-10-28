import re, html, unicodedata, hashlib
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
u = html.unescape(t)
q = "\u30b7\u30f3\u30dc\u30eb\u304c\u306a\u3044\u5834\u5408\u306e\u30d2\u30f3\u30c8"
print("bytes", len(t.encode()), "sha256", hashlib.sha256(t.encode()).hexdigest())
for name, body in (("raw", t), ("html-unescaped", u), ("NFKC", unicodedata.normalize("NFKC", u))):
    print("%-15s quote=%d hint=%d shinboru_ga_nai=%d shinboru=%d"
          % (name, body.count(q), body.count("\u30d2\u30f3\u30c8"),
             body.count("\u30b7\u30f3\u30dc\u30eb\u304c\u306a\u3044"), body.count("\u30b7\u30f3\u30dc\u30eb")))
for v in ("\u30b7\u30f3\u30dc\u30eb\u304c\u7121\u3044\u5834\u5408\u306e\u30d2\u30f3\u30c8",
          "\u30b7\u30f3\u30dc\u30eb\u306e\u306a\u3044\u5834\u5408\u306e\u30d2\u30f3\u30c8",
          "\u5834\u5408\u306e\u30d2\u30f3\u30c8", "\u30b3\u30c4"):
    print("variant", v, "->", u.count(v))
