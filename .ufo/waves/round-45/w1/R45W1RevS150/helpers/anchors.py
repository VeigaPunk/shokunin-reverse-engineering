import json, html
a = json.load(open("zenn-api.json"))["article"]
bh = html.unescape(open("s150-live.html", encoding="utf-8", errors="replace").read())
body = a["body_html"]
q1 = "GNU Binutils に含まれる逆アセンブラ。ほぼすべての Linux 環境に入っています。"
q2 = "strip されていても PLT のシンボルは残る場合があるので、ここが最初の手がかりになりました"
for name, q in (("row-substantive-quote-1", q1), ("row-substantive-quote-2", q2)):
    print("%-26s body_html=%d live_page=%d len=%d" % (name, body.count(q), bh.count(q), len(q)))
# replacement anchors that ARE byte-present, with counts
for cand in ("パターン認識のコツ", "実バイナリを逆アセンブルして読む", "シンボルなしの世界に踏み込む"):
    print("candidate anchor %-28s body_html=%d live_page=%d" % (cand, body.count(cand), bh.count(cand)))
