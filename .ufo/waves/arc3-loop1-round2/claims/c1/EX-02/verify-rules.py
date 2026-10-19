#!/usr/bin/env python3
"""Compare the craft section before/after a patch: rules 1-13 byte-identity + rule 14 text."""
import hashlib, pathlib, re, sys
before = pathlib.Path(sys.argv[1]).read_text()
after  = pathlib.Path(sys.argv[2]).read_text()
def craft(t):
    return t.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
def rules(t):
    return re.split(r'(?m)^- \*\*', craft(t))[1:]
rb, ra = rules(before), rules(after)
print(f"rule_blocks before={len(rb)} after={len(ra)}")
def h(s): return hashlib.sha256(('- **' + s).encode()).hexdigest()
ident = True
for i in range(min(len(rb), 13)):
    same = h(rb[i]) == h(ra[i])
    ident &= same
    print(f"rule {i+1:2d}: {'IDENTICAL' if same else 'CHANGED'}  pre={h(rb[i])[:16]} post={h(ra[i])[:16]}")
print(f"PREREQ_13_BYTE_IDENTICAL={'True' if ident else 'False'}")
if len(ra) > 13:
    print("--- rule 14 text ---")
    print('- **' + ra[13])
    print("--- end rule 14 (bytes:", len(('- **'+ra[13]).encode()), ") ---")
