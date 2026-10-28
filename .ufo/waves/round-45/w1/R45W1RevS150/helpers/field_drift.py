import re, json
def nd(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', t, re.S)
    return json.loads(m.group(1))
def flat(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, p + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, p + "[%d]" % i)
    else:
        yield p, o
import os
a = dict(flat(nd(os.environ["R44"] + "/s150-zenn.html")))
b = dict(flat(nd("s150-live.html")))
print("keys only in r44:", sorted(set(a) - set(b))[:5])
print("keys only in r45:", sorted(set(b) - set(a))[:5])
d = [(k, a[k], b[k]) for k in set(a) & set(b) if a[k] != b[k]]
print("changed fields:", len(d))
for k, x, y in d:
    print("  %s : r44=%r -> r45=%r" % (k, x, y))
