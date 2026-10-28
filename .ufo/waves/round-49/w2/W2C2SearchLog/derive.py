import re,sys,collections
ROW=re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
def load(p):
    rows={}; dups=[]; order=[]
    for l in open(p,encoding='utf-8'):
        l=l.rstrip('\n')
        m=ROW.match(l)
        if m:
            i=m.group(1)
            if i in rows: dups.append(i)
            rows[i]=l; order.append(i)
    return rows,dups,order
def cells(l):
    c=[x.strip() for x in l.strip().split('|')]
    return c[1:-1]
def tally(rows):
    t=collections.Counter()
    for i,l in rows.items():
        c=cells(l); t[c[7] if len(c)>7 else '?']+=1
    return t
for a,b in [('SOURCES-61b87d74.md','SOURCES-8847042a.md'),('SOURCES-e4f2cfa5.md','SOURCES-29883d4e.md')]:
    ra,da,oa=load(a); rb,db,ob=load(b)
    new=[i for i in ob if i not in ra]
    gone=[i for i in oa if i not in rb]
    inc=[i for i in new if cells(rb[i])[7]!='rejected']
    exc=[i for i in new if cells(rb[i])[7]=='rejected']
    print(f"== {a} -> {b}: rows {len(ra)} -> {len(rb)} (dups a={da} b={db}); new={new}; gone={gone}")
    print(f"   new included(non-rejected)={inc} excluded(rejected)={exc}")
    print(f"   statuses a={dict(tally(ra))} b={dict(tally(rb))}")
    # changed rows among common ids
    ch=[i for i in ra if i in rb and ra[i]!=rb[i]]
    print(f"   common ids whose row bytes changed: {ch}")
    for i in ch:
        ca,cb=cells(ra[i]),cells(rb[i])
        print("     ",i,[ (k,ca[k],cb[k]) for k in range(min(len(ca),len(cb))) if ca[k]!=cb[k]][:3] if len(ca)==len(cb) else ('NF',len(ca),len(cb)))
print("== e4f2 -> 29883 full status tallies")
