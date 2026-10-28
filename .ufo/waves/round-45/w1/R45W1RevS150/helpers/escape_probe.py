import re
t = open("s150-live.html", encoding="utf-8", errors="replace").read()
q = "\u30b7\u30f3\u30dc\u30eb\u304c\u306a\u3044\u5834\u5408\u306e\u30d2\u30f3\u30c8"
low = "".join("\\u%04x" % ord(c) for c in q)
up = "".join("\\u%04X" % ord(c) for c in q)
print("lowercase-escape present:", low in t)
print("uppercase-escape present:", up in t)
print("escaped CJK sequences in page:", len(re.findall(r"\\u3[0-9a-fA-F]{3}", t)))
for k in ('"bodyMarkdown"', '"bodyHtml"', '"body_updated_at"', '"taggingsCount"', '"bodyLettersCount"'):
    print("field", k, "count", t.count(k))
