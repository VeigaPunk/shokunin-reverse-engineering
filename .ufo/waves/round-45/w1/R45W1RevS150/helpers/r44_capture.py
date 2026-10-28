import html, hashlib, os
p = os.environ["R44"] + "/s150-zenn.html"
b = open(p, "rb").read()
t = b.decode("utf-8", "replace")
u = html.unescape(t)
q = "\u30b7\u30f3\u30dc\u30eb\u304c\u306a\u3044\u5834\u5408\u306e\u30d2\u30f3\u30c8"
print("bytes", len(b), "sha256", hashlib.sha256(b).hexdigest())
print("quote raw", t.count(q), "unescaped", u.count(q),
      "hint", t.count("\u30d2\u30f3\u30c8"))
