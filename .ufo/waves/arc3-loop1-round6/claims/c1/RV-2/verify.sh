#!/bin/bash
# RV-2 verification transcript generator (arc3-loop1-round6, chain c1).
# Re-runs every measurement quoted in RV-2.md from a pristine repo + scratch.
# Scratch: /var/tmp/rv2-arc3r6 (never /tmp). Repo writes: none.
R=/var/tmp/rv2-arc3r6
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SEAT=$REPO/.ufo/waves/arc3-loop1-round6/claims/c1/RV-2
mkdir -p "$SEAT"
cd "$R" || exit 1
say(){ printf '\n### %s\n' "$*"; }

say "0. custody"
date -u +%Y-%m-%dT%H:%M:%SZ
cd "$REPO" || exit 1
git rev-parse HEAD
git log --oneline -3
sha256sum .ufo/gates/c1-census-v10.py
wc -l .ufo/gates/c1-census-v10.py PROVINCE.md
git status --porcelain | head -5

say "1. SCOPE rows + blind-spot grep"
grep -n '("PROVINCE.md",' .ufo/gates/c1-census-v10.py
grep -nE '^#{1,4} ' PROVINCE.md | sed -n '1,10p'

say "2. patch application to pristine gate"
cd "$R" || exit 1
rm -f rebuilt-rv2.py; cp c1-census-v10-pristine.py rebuilt-rv2.py
patch rebuilt-rv2.py < patch.diff
echo "patch-exit=$?"
sha256sum c1-census-v10-pristine.py patch.diff rebuilt-rv2.py
sha256sum "$REPO/.ufo/waves/arc3-loop1-round6/claims/c1/PL-4/c1-census-v10-r10.py" "$REPO/.ufo/waves/arc3-loop1-round6/claims/c1/PL-4/patch-v10-to-r10.diff"
cmp -s rebuilt-rv2.py "$REPO/.ufo/waves/arc3-loop1-round6/claims/c1/PL-4/c1-census-v10-r10.py" && echo "BUILT-INSTRUMENT IDENTICAL"
wc -l rebuilt-rv2.py
# the rebuilt instrument is what the arms below run
cp rebuilt-rv2.py c1-census-v10-r10-rebuilt.py

say "3. clean-tree PASS + counter integrity (repo root, --json)"
python3 c1-census-v10-pristine.py --quiet --json > v10-repo.json; echo "v10-exit=$?"
python3 c1-census-v10-r10-rebuilt.py --quiet --json > r10-repo.json; echo "r10-exit=$?"
python3 - <<'PY'
import json
a=json.load(open('/var/tmp/rv2-arc3r6/v10-repo.json')); b=json.load(open('/var/tmp/rv2-arc3r6/r10-repo.json'))
print('verdicts:', a['verdict'], b['verdict'])
print('counts equal:', a['counts']==b['counts'], a['counts'])
print('current_ok_per_file equal:', a['current_ok_per_file']==b['current_ok_per_file'], b['current_ok_per_file'])
s=set(a)&set(b)
print('shared keys:', len(s), '| r10-only:', sorted(set(b)-set(a)), '| v10-only:', sorted(set(a)-set(b)))
print('shared mismatches:', [k for k in sorted(s) if a[k]!=b[k]])
print('frontier_rows:', b['frontier_rows'], '| frontier_errors:', b['frontier_errors'], '| declared:', b['declared_fail_classes'])
PY
python3 c1-census-v10-pristine.py --quiet > v10-repo.txt
python3 c1-census-v10-r10-rebuilt.py --quiet > r10-repo.txt
diff v10-repo.txt r10-repo.txt || true
grep -n 'VERDICT' v10-repo.txt r10-repo.txt

say "3b. classify() enumeration: no locus line in the frontier ranges"
python3 - <<'PY'
import importlib.util
spec=importlib.util.spec_from_file_location('v10','/var/tmp/rv2-arc3r6/c1-census-v10-pristine.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
lines=open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md',encoding='utf-8').read().splitlines()
out={}; loci=m.classify('PROVINCE.md',lines,{'devin':'6.5.0','omp':'6.5.0','kimi':'6.7.0'},out)
als=[(d['line'],d['disp'],d['scope']) for rec in loci for d in rec['asserts']]
print('PROVINCE loci=%d assertion entries=%d' % (len(loci),len(als)))
print('lines:',sorted({a[0] for a in als}))
print('frontier-range assertion lines:',[a[0] for a in als if (73<=a[0]<=93) or (133<=a[0]<=162)])
PY

say "4. rebuild seeded trees (independent seeder)"
python3 seed_rv2.py
python3 - <<'PY'
import os, shutil, subprocess
REPO="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; BASE="/var/tmp/rv2-arc3r6"
FILES=["PROVINCE.md","SKILL.md","SCORECARD.md"]
def mk(name):
    d=os.path.join(BASE,'trees',name); shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    for f in FILES: shutil.copyfile(os.path.join(REPO,f),os.path.join(d,f))
def edit(name, fn):
    d=os.path.join(BASE,'trees',name); mk(name); p=os.path.join(d,'PROVINCE.md')
    ls=open(p,encoding='utf-8').read().splitlines(True); fn(ls); open(p,'w',encoding='utf-8').writelines(ls)
edit('seeded-insert-two', lambda ls: ls.__setitem__(slice(134,134), ["- **New bullet A** \u2014 inserted.\n","- **New bullet B** \u2014 inserted.\n"]))
edit('seeded-insert-one-evm', lambda ls: ls.__setitem__(slice(89,89), ["- **New bullet before EVM** \u2014 inserted at :90.\n"]))
edit('seeded-append-163', lambda ls: ls.append("- **Brand-new bullet past bound** \u2014 appended at :163.\n"))
edit('seeded-stale-new-bullet', lambda ls: ls.__setitem__(slice(134,134), ["- **Managed PE/CLI** \u2014 pre-round-4 stale bullet, real PE untested.\n"]))
edit('benign-edit', lambda ls: ls.__setitem__(136, ls[136].replace('full 29 MB EXEC','full 29 MB EXEC file')))
CROSS_OLD = [
    "- **Cross-version residuals** \u2014 `compare-application-versions` still\n",
    "  probe-refused since r2; multi-version pacman pairs beyond expac unexercised\n",
    "  [r5-audit C1: merged from the pruned Frontier bullet \u2014 its\n",
    "  `compare_javascript_export_shapes` item is now held (Core, r4-09)].\n",
]
edit('seeded-replace-crossversion-old', lambda ls: ls.__setitem__(slice(156,160), CROSS_OLD))
edit('seeded-stale-clause-crossversion', lambda ls: ls.__setitem__(slice(156,160), [
    "- **Cross-version residuals** \u2014 `compare-application-versions` EXERCISED on all\n",
    "  three input classes (r12-02: JS + managed; r14-01: runtime-reconcile, `ev_8f0ac46c\u2026`);\n",
    "  but still probe-refused since r2; multi-version pacman pairs beyond expac unexercised\n",
    "  [r5-audit C1: merged from the pruned Frontier bullet \u2014 its `compare_javascript_export_shapes` item is now held (Core, r4-09)].\n",
]))
print('extra trees built')
PY

say "4b. build the bullet-census proposal (scratch, on top of PL-4 r10)"
python3 - <<'PY'
src=open('/var/tmp/rv2-arc3r6/c1-census-v10-r10-rebuilt.py',encoding='utf-8').read()
anchor='PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)'
reg='''REGION_BULLETS = [
    ("PROVINCE.md", 73, 93, 5),
    ("PROVINCE.md", 133, 162, 8),
]

'''
src=src.replace(anchor, reg+anchor, 1)
old='''        for pat in forb:
            m = re.search(pat, seg, re.I)
            if m:
                errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                            % (f, s, e, pat, m.group(0)))
    return errs'''
new='''        for pat in forb:
            m = re.search(pat, seg, re.I)
            if m:
                errs.append("%s:%d-%d FORBIDDEN %r matched %r (FRONTIER-STALE)"
                            % (f, s, e, pat, m.group(0)))
    for (f, s, e, want) in REGION_BULLETS:
        lines = filelines.get(f)
        if not lines:
            continue
        got = sum(1 for ln in lines[s - 1:e] if re.match(r"^- ", ln))
        if got != want:
            errs.append("%s:%d-%d bullet census %d != declared %d "
                        "(FRONTIER-UNREGISTERED-BULLET)"
                        % (f, s, e, got, want))
    return errs'''
assert anchor in src and old in src
open('/var/tmp/rv2-arc3r6/c1-census-r10-bulletcount.py','w',encoding='utf-8').write(src.replace(old,new,1))
print('bullet-census proposal built')
PY
diff -u --label a/c1-census-v10-r10.py --label b/c1-census-r10-bulletcount.py c1-census-v10-r10-rebuilt.py c1-census-r10-bulletcount.py > r10-bulletcount-proposal.diff || true
wc -l r10-bulletcount-proposal.diff

say "5. arm matrix: v10 (blind) vs r10 (PL-4) vs r10+bullet-census proposal"
python3 - <<'PY'
import json, os, subprocess
base='/var/tmp/rv2-arc3r6'
print("%-26s %-6s %-6s %-6s %s" % ("tree","v10","r10","r10+bc","r10 declared classes"))
for t in sorted(os.listdir(base+'/trees')):
    def run(gate):
        p=subprocess.run(['python3',base+'/'+gate,'--root',base+'/trees/'+t,'--quiet','--json'],capture_output=True,text=True)
        return p.returncode, json.loads(p.stdout)
    ve,v=run('c1-census-v10-pristine.py'); re_,r=run('c1-census-v10-r10-rebuilt.py'); be,b=run('c1-census-r10-bulletcount.py')
    note = [e for e in r['frontier_errors'] if 'FORBIDDEN' in e][:1] or [e for e in r['frontier_errors'] if 'REQUIRED' in e][:1] or r['frontier_errors'][:1]
    bc = b['frontier_errors'][:1]
    print("%-30s %d/%-4s %d/%-4s %d/%-4s %r | %r" % (t, ve, v['verdict'], re_, r['verdict'], be, b['verdict'], r['declared_fail_classes'], note))
    if bc: print("%-30s   bc: %r" % ('', bc))
PY

say "6. bullet census of the two frontier regions (clean tree)"
python3 - <<'PY'
import re
p='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md'
ls=open(p,encoding='utf-8').read().splitlines()
for (s,e) in [(73,93),(133,162)]:
    starts=[i+1 for i in range(s-1,e) if re.match(r'^- ',ls[i])]
    print('region %d-%d bullet starts %r count=%d' % (s,e,starts,len(starts)))
PY

say "7. provenance of the FORBIDDEN literal (git, read-only)"
cd "$REPO" || exit 1
git log --oneline -1 40de383
git merge-base --is-ancestor 40de383 HEAD && echo "40de383 is ancestor of HEAD"
git show 40de383^:PROVINCE.md | nl -ba | sed -n '91,93p'
git show 40de383^:PROVINCE.md | grep -n 'untested'

say "8. peer design cross-check: RV-3 prior anchored register (from claims/c1/RV-3/prior-attempt.md)"
cd "$R" || exit 1
python3 - <<'PY'
import re
md=open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round6/claims/c1/RV-3/prior-attempt.md',encoding='utf-8').read()
b=re.findall(r'```diff\n(.*?)```',md,re.S)[-1]
open('/var/tmp/rv2-arc3r6/rv3-patch.diff','w',encoding='utf-8').write(b)
PY
cp c1-census-v10-pristine.py rv3-test.py
patch rv3-test.py < rv3-patch.diff
sha256sum rv3-test.py
for t in clean seeded-insert-one seeded-stale-new-bullet seeded-forbidden-only clean-truncated; do
  python3 rv3-test.py --root "trees/$t" --quiet --json > "rv3-$t.json"; echo "$t exit=$?"
done
python3 - <<'PY'
import json
for t in ('clean','seeded-insert-one','seeded-stale-new-bullet','seeded-forbidden-only','clean-truncated'):
    j=json.load(open(f'/var/tmp/rv2-arc3r6/rv3-{t}.json'))
    print('%-26s %-5s rows=%s errors=%r' % (t,j['verdict'],j.get('frontier_rows'),j.get('frontier_errors',[])[:2]))
PY

say "9. evidence files"
sha256sum "$SEAT"/* 2>/dev/null || true
