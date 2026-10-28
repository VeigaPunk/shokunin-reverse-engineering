import json
a = json.load(open("zenn-api.json"))["article"]
bh, title = a["body_html"], a["title"]
print("title:", title)
print("body_html シンボルなし:", bh.count("シンボルなし"))
print("body_html シンボルがない:", bh.count("シンボルがない"))
print("title シンボルなし:", title.count("シンボルなし"))
print("body_html ヒント:", bh.count("ヒント"))
print("nearest real tips heading パターン認識のコツ:", bh.count("パターン認識のコツ"))
