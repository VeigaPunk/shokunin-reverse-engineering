import re,sys,hashlib
# Quote check for the round-49 Gate rows S147/S148/S149 against the committed snapshots (read from git objects at REV).
def norm(p):
    import html
    s=open(p,encoding='utf-8',errors='replace').read()
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S|re.I)
    s=re.sub(r'<br\s*/?>|</p>|</div>|</h\d>|</li>|</pre>|</tr>',' \n ',s,flags=re.I)
    s=re.sub(r'<[^>]+>','',s)
    return re.sub(r'\s+',' ',html.unescape(s))
cases=[
 ('S147','popper.html','falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific'),
 ('S147b','popper.html','it is consistent with all possible observations, is unscientific'),
 ('S145','popper.html','if a theory is incompatible with possible empirical observations it is scientific; conversely, a theory which is compatible with all such observations'),
 ('S148','sysexits.html','#define EX_USAGE 64 /* command line usage error */'),
 ('S149','freebsd-sysexits.html','EX_USAGE (64) The command was used incorrectly'),
]
for rid,f,q in cases:
    t=norm(f); i=t.find(q)
    words=len(q.split())
    print(f"{rid}: words={words} (<=25: {words<=25}) present={i>=0} offset={i}")
t=norm('popper.html')
h2=[m.start() for m in re.finditer(re.escape('2. Backdrop to Popper'),t)][-1]
h3=[m.start() for m in re.finditer(re.escape('3. The Problem of Demarcation'),t)][-1]
q=t.find('falsifiability as his criterion')
print(f"S147 location: heading2@{h2} quote@{q} heading3@{h3} -> quote under section 2: {h2<q<h3}")
print("S145 locator literal '2. The Problem of Demarcation' present in body:", '2. The Problem of Demarcation' in t)
