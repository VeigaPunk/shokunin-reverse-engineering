import re, html, sys
p = sys.argv[1]
t = open(p, encoding='utf-8', errors='replace').read()
# find the dt/dd structure around O_NOFOLLOW
i = t.find('O_NOFOLLOW')
while i != -1 and i < len(t):
    seg = t[i:i+40].split('\n')[0]
    print("O_NOFOLLOW occurrence at", i, ":", repr(seg))
    i = t.find('O_NOFOLLOW', i+1)
print("=== raw html slice around quote ===")
q = "If the trailing component"
j = t.find(q)
print("raw idx", j)
print(t[j-700:j+700])
print("=== dl/dt structure: nearest preceding <dt> and <dl> ===")
k = j
dt = t.rfind('<dt', 0, j)
dl = t.rfind('<dl', 0, j)
h2 = t.rfind('<h2', 0, j)
print("nearest dt at", dt, repr(re.sub(r'<[^>]+>','',t[dt:dt+80])))
print("nearest dl at", dl)
print("nearest h2 at", h2, repr(re.sub(r'(?s)<[^>]+>','',t[h2:h2+200]).strip()))
