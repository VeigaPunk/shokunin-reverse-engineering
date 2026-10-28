import re, hashlib, os
def masked(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    t = re.sub(r'nonce="[^"]*"', 'nonce="X"', t)
    return re.sub(r'data-n-css="[^"]*"', 'data-n-css="X"', t)
rows = [("r45-live", "s150-live.html"), ("r45-refetch1", "s150-refetch-1.html"),
        ("r45-refetch2", "s150-refetch-2.html"),
        ("r44-capture", os.environ["R44"] + "/s150-zenn.html"),
        ("r39-capture", os.environ["R39"] + "/zenn-s150.html")]
for name, p in rows:
    b = open(p, "rb").read()
    print("%-14s bytes=%7d nonces=%2d raw_sha=%s masked_sha=%s"
          % (name, len(b), len(re.findall(r'nonce="', b.decode("utf-8", "replace"))),
             hashlib.sha256(b).hexdigest()[:16], hashlib.sha256(masked(p).encode()).hexdigest()[:16]))
v45 = {hashlib.sha256(masked(p).encode()).hexdigest()
       for _, p in rows[:3]}
print("r45 same-day masked hashes identical:", len(v45) == 1)
pref = [hashlib.sha256(masked(p).encode()).hexdigest() for _, p in rows]
print("all five masked hashes identical:", len(set(pref)) == 1)
