import sys
for l in sys.stdin:
    if l.startswith("@@") or l.startswith("diff") or l.startswith("---") or l.startswith("+++"):
        print(l.rstrip())
