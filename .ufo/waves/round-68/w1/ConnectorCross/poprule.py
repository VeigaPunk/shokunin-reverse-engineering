import re, subprocess, sys, json
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
KAMA_RE = re.compile(r"^(?:\.ufo/waves/round-[^/]+/count-[^/]+|tools/round[0-9]+-[A-Za-z0-9._-]+)\.py$")  # kama gate-registry-check.py:79
TOOL_RE = re.compile(r"tools/round-\d+[A-Za-z0-9._/-]*?\.(?:py|sh|mjs)(?![A-Za-z0-9._-])")
PLAN_RE = re.compile(r"^plans/round-(\d+)-claims\.md$")

def git(*a):
    return subprocess.run(["git","-C",LANE,*a],capture_output=True,text=True,check=True).stdout

def scope(rev):
    names = git("ls-tree","-r","--name-only",rev).splitlines()
    blobs = set(names)
    plans = [n for n in names if PLAN_RE.match(n)]
    out=set()
    for p in plans:
        n=int(PLAN_RE.match(p).group(1))
        if n < 41: continue
        body = git("show", f"{rev}:{p}")
        for tok in TOOL_RE.findall(body):
            m = re.match(r"tools/round-(\d+)/", tok)
            if not m or int(m.group(1)) != n: continue
            if tok in blobs: out.add(tok)
    return sorted(out)

for rev,label in [(sys.argv[1],"BASE"),(sys.argv[2],"FREEZE")]:
    sc = scope(rev)
    kama = [p for p in sc if KAMA_RE.match(p)]
    missed = [p for p in sc if not KAMA_RE.match(p)]
    print(f"{label} rev={rev}")
    print(f"  plan_keyed_scope={len(sc)}")
    print(f"  kama_layout_rule_matches={len(kama)}")
    print(f"  kama_layout_rule_misses={len(missed)}")
    print(f"  round67_in_scope={[p for p in sc if p.startswith('tools/round-67/')]}")
    print(f"  round67_matched_by_kama={[p for p in kama if p.startswith('tools/round-67/')]}")
