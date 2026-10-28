import json
a = json.load(open("zenn-api.json"))["article"]
bh = a["body_html"]
toc = [e.get("text", "") for e in a.get("toc", [])]
q = "\u30b7\u30f3\u30dc\u30eb\u304c\u306a\u3044\u5834\u5408\u306e\u30d2\u30f3\u30c8"
print("title", a["title"])
print("published_at", a["published_at"], "body_updated_at", a["body_updated_at"])
print("body_letters_count", a["body_letters_count"], "body_html_len", len(bh))
print("body_html quote", bh.count(q), "hint", bh.count("\u30d2\u30f3\u30c8"),
      "shinboru_ga_nai", bh.count("\u30b7\u30f3\u30dc\u30eb\u304c\u306a\u3044"))
print("toc entries", len(toc))
for x in toc:
    print("  TOC:", x)
print("toc contains quote:", any(q in x for x in toc),
      "toc contains hint:", any("\u30d2\u30f3\u30c8" in x for x in toc))
