import re, sys
a = open(sys.argv[1], encoding="utf-8", errors="replace").read()
b = open("s113-adb.html", encoding="utf-8", errors="replace").read()
def mask(t):
    t = re.sub(r'nonce="[^"]*"', 'nonce="X"', t)
    return re.sub(r'data-n-css="[^"]*"', 'data-n-css="X"', t)
ma, mb = mask(a), mask(b)
print("r44 bytes", len(a), "r45 bytes", len(b), "delta", len(b) - len(a))
print("masked lens", len(ma), len(mb), "masked identical", ma == mb)
i = next((k for k in range(min(len(ma), len(mb))) if ma[k] != mb[k]), None)
if i is not None:
    print("first masked diff at", i)
    print("r44:", repr(ma[max(0, i - 100):i + 100]))
    print("r45:", repr(mb[max(0, i - 100):i + 100]))
