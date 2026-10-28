import re, json, sys
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
a = dict(flat(nd(sys.argv[1])))
b = dict(flat(nd(sys.argv[2])))
print("A=", sys.argv[1].split("/")[-1], " B=", sys.argv[2].split("/")[-1])
print("keys only in A:", sorted(set(a) - set(b))[:5])
print("keys only in B:", sorted(set(b) - set(a))[:5])
d = [(k, a[k], b[k]) for k in set(a) & set(b) if a[k] != b[k]]
print("changed fields:", len(d))
for k, x, y in d:
    print("  %s : A=%r -> B=%r" % (k, x, y))
