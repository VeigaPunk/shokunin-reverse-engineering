import json, subprocess, time
series = json.load(open("series-rows.json"))
q = "\u30b7\u30f3\u30dc\u30eb\u304c\u306a\u3044\u5834\u5408\u306e\u30d2\u30f3\u30c8"
tot = 0
for r in series:
    aid = r["url"].rstrip("/").split("/")[-1]
    out = "api-" + aid + ".json"
    p = subprocess.run(["curl", "-sS", "--max-time", "45", "-o", out, "-w",
                        "%{http_code} %{size_download}",
                        "https://zenn.dev/api/articles/" + aid],
                       capture_output=True, text=True)
    a = json.load(open(out))["article"]
    bh = a["body_html"]
    print("%s %s http=%s quote=%d hint=%d title=%s"
          % (r["part"], aid, p.stdout.strip(), bh.count(q),
             bh.count("\u30d2\u30f3\u30c8"), a["title"][:44]))
    tot += bh.count(q) + bh.count("\u30d2\u30f3\u30c8")
    time.sleep(1)
print("SERIES TOTAL quote+hint =", tot)
