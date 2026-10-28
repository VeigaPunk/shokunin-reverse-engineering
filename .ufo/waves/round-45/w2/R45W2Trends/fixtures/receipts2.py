#!/usr/bin/env python3
"""R45W2Trends: records for the expansion / command-A / gate-coverage attacks."""
import hashlib, json, os, subprocess, sys, datetime

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2Trends"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REC = os.path.join(S, "receipts")
os.makedirs(REC, exist_ok=True)
BASE = "149133d47aa7e90796f96047afe6d251a3e65b2c"
A3 = "f59565b782c18b0eb691bec12f52d2f80d9f5032"

def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def run(cmd, cwd=LANE):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p

def rec(tag, cmd, p, extra=None):
    out = p.stdout or ""
    d = {"tag": tag, "utc": utc(), "cmd": cmd, "exit": p.returncode,
         "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
         "stdout": out[:6000], "stderr": (p.stderr or "")[:2000]}
    if extra:
        d.update(extra)
    json.dump(d, open(os.path.join(REC, tag + ".json"), "w"), indent=1)
    return d

# 1. expansion: knowledge diff over the whole round
cmd = ["git", "-C", LANE, "diff", "--name-status", BASE + ".." + A3, "--", "corpus/knowledge"]
p = run(cmd)
rec("expansion-knowledge-diff", " ".join(cmd), p, {"attack": "expansion unchanged"})

# 2. command A at base / landing / A1 / A3 (the recipe verbatim)
A = r'''
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
unresolved = []
for i, rule in enumerate(rules):
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    if not valid:
        unresolved.append(i + 1)
    resolved += valid
print(json.dumps({'revision': rev, 'mapped': len(files & mapped),
 'knowledge_files': len(files), 'missing': sorted(files - mapped),
 'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
 'rule_blocks': len(rules), 'unresolved_rule_indexes': unresolved,
 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
'''
open(os.path.join(S, "commandA.py"), "w").write(A)
for rev, tag in (("149133d4", "commandA-base"), ("e715263c", "commandA-landing"),
                 ("1f4b27f8", "commandA-A1"), (A3, "commandA-A3")):
    p = run([sys.executable, os.path.join(S, "commandA.py"), rev])
    rec(tag, "command A (SCORECARD ## Measurement recipes) at " + rev, p, {"attack": "expansion/quality"})

# 3. source-registry growth (the competing expansion proxy)
for rev, tag in ((BASE, "sources-rows-base"), (A3, "sources-rows-A3")):
    p = run(["bash", "-c", "git show %s:corpus/SOURCES.md | grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}'" % rev])
    rec(tag, "grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' on corpus/SOURCES.md@" + rev, p, {"attack": "expansion"})

# 4. S138 append-only: the S138 row line is not in the round's SOURCES diff
p = run(["bash", "-c", "git -C %s diff %s..%s -- corpus/SOURCES.md | grep -c '^-| S138'" % (LANE, BASE, A3)])
rec("s138-row-untouched", "git diff BASE..A3 -- corpus/SOURCES.md | grep -c '^-| S138'", p, {"attack": "discernment S138"})

# 5. S138 receipt existence at the measured revision
for rev, tag in (("f59565b7", "s138-receipt-at-A3"), ("HEAD", "s138-receipt-at-HEAD")):
    p = run(["git", "cat-file", "-e", rev + ":.ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md"])
    rec(tag, "git cat-file -e %s:.ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md" % rev, p,
        {"attack": "discernment S138"})

# 6. gate wiring: hooks + which revisions the gate receipts certify
p = run(["bash", "-c", "ls .git/hooks | grep -v sample; echo hookspath=$(git config --get core.hooksPath)"])
rec("gate-wiring", "ls .git/hooks | grep -v sample; git config --get core.hooksPath", p, {"attack": "discernment R44-CL1"})
p = run(["bash", "-c", "git log --format='%%h %%s' f762b727.." + A3])
rec("round45-commits", "git log --format='%h %s' f762b727.." + A3, p, {"attack": "discernment R44-CL1"})
p = run(["bash", "-c", "for f in .ufo/waves/round-45/l1/preflight*.json; do python3 -c \"import json;d=json.load(open('$f'));print('$f',d.get('rev'),d.get('verdict'),d.get('pathspec'))\"; done"])
rec("gate-receipt-revs", "python3 -c ... over .ufo/waves/round-45/l1/preflight*.json", p, {"attack": "discernment R44-CL1"})

# 7. four-red-arms claim: count the arm names in block 22's table
p = run(["bash", "-c", "git show %s:SKILL.md | awk '/<!-- freeze-integrity-table v1 -->/{f=1} f' | sed -n '3,13p'" % A3])
rec("block22-table", "git show A3:SKILL.md, table rows 3-13", p, {"attack": "quality improved"})

print("done")
