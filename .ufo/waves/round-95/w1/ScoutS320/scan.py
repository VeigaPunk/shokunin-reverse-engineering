import re, html, sys, hashlib
p = sys.argv[1]
raw = open(p,'rb').read()
t = raw.decode('utf-8', 'replace')
# tag strip
s = re.sub(r'(?s)<script.*?</script>', ' ', t)
s = re.sub(r'(?s)<style.*?</style>', ' ', s)
s = re.sub(r'(?s)<[^>]+>', ' ', s)
s = html.unescape(s)
# whitespace normalise
n = re.sub(r'\s+', ' ', s).strip()
print("NORMALIZED_LEN", len(n))
print("NORMALIZED_SHA256", hashlib.sha256(n.encode()).hexdigest())
quote = "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP"
print("QUOTE_EXACT_COUNT", n.count(quote))
if n.count(quote) == 0:
    # find near variants
    for m in re.finditer(r'If the trailing component', n):
        print("VARIANT:", repr(n[m.start():m.start()+220]))
else:
    for i, m in enumerate(re.finditer(re.escape(quote), n), 1):
        st = max(0, m.start()-400)
        print(f"--- OCCURRENCE {i} at offset {m.start()} context before ---")
        print(repr(n[st:m.start()]))
        print(f"--- OCCURRENCE {i} context after ---")
        print(repr(n[m.end():m.end()+400]))
# version string
for m in re.finditer(r'Linux man-pages[^<]{0,40}', t):
    print("VERSION_RAW:", repr(m.group(0)))
print("--- headings ---")
for m in re.finditer(r'(?s)<h([1-4])[^>]*>(.*?)</h\1>', t):
    txt = re.sub(r'(?s)<[^>]+>','', m.group(2))
    txt = re.sub(r'\s+',' ', html.unescape(txt)).strip()
    print(f"H{m.group(1)} @{m.start()}: {txt}")
