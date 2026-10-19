#!/bin/bash
[ -z "$3" ] && { echo "need <tool> <outdir> <tag>"; exit 9; }
# RV-5 attack battery — adversarial checks on the four landed closures.
# usage: attack.sh <tool> <outdir> <tag>
TOOL="$1"; OUT="$2"; TAG="$3"
S="/var/tmp/rv5/scratch/$TAG"; rm -rf "$S"; mkdir -p "$S" "$OUT"
export PYTHONDONTWRITEBYTECODE=1
PY=python3; LOG="$OUT/attack.log"; : >"$LOG"
r() { local n="$1"; shift; { echo "### $n"; echo "\$ $*"; } >>"$LOG"; { "$PY" "$TOOL" "$@"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1; }
s() { local n="$1"; shift; { echo "### $n"; echo "\$ $*"; } >>"$LOG"; { bash -c "$*"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1; }

sha256sum "$TOOL" >>"$LOG"
printf 'fixture\n' >"$S/f.conf"; printf 'other\n' >"$S/g.conf"
R2=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/claims/c3/EX-31

# --- guard attacks ---
s C1-hardlink "printf 'hl\n' >$S/hl-target.conf && ln $S/hl-target.conf $S/hl-alias.txt && $PY $TOOL capture --out $S/hl-alias.txt --paths $S/hl-target.conf --label hl; ls -l $S/hl-target.conf; head -c 20 $S/hl-target.conf | od -c | head -2"
s C2-symlink-to-custody "ln -s $HOME/.bashrc $S/link-to-bashrc && $PY $TOOL capture --out $S/link-to-bashrc --paths $S/f.conf --label symcust"
s C3-symlink-to-scoped "printf 'scoped\n' >$S/scoped.conf && ln -s $S/scoped.conf $S/link-to-scoped && $PY $TOOL capture --out $S/link-to-scoped --paths $S/scoped.conf --label symscoped; sha256sum $S/scoped.conf"
s C4-relative-vs-absolute "cd $S && $PY $TOOL capture --out ./f.conf --paths $S/f.conf --label relabs; head -c 20 $S/f.conf"
s C5-false-positive "$PY $TOOL capture --out $S/new-out.txt --paths $S/f.conf --label fp && echo OK-WROTE"
s C6-out-is-sidecar "printf 'x\n' >$S/rec.txt && $PY $TOOL capture --out $S/rec.txt.sha256 --paths $S/rec.txt --label sidecar || true; head -c 60 $S/rec.txt"

# --- D2 attacks ---
s A2-verify-stat-blocked-cand "mkdir -p $S/blk && printf 'p\n' >$S/blk/inner.conf && $PY $TOOL capture --out $S/blk-pre.txt --paths $S/blk/inner.conf --label blk && chmod 000 $S/blk && $PY $TOOL verify $S/blk-pre.txt --live; chmod 755 $S/blk"
s A3-ref-read-error-vs-fine "printf 'q\n' >$S/q.conf && chmod 000 $S/q.conf && $PY $TOOL capture --out $S/q-pre.txt --paths $S/q.conf --label q; chmod 644 $S/q.conf && $PY $TOOL verify $S/q-pre.txt --live"
s A4-symlink-to-unreadable "printf 'u\n' >$S/u-target && chmod 000 $S/u-target && ln -s $S/u-target $S/u-link && $PY $TOOL capture --out $S/u-link.txt --paths $S/u-link --label ulink; chmod 644 $S/u-target"
s A5-directory-path "$PY $TOOL capture --out $S/dir-rec.txt --paths $S --label dirpath; $PY $TOOL verify $S/dir-rec.txt --live"

# --- D3 attacks ---
r B1-canonical5-require5 verify "$R2/capture-pre.txt" --live --require-paths 5
s B2-five-noncanonical "printf 'n1\n' >$S/n1; printf 'n2\n' >$S/n2; printf 'n3\n' >$S/n3; printf 'n4\n' >$S/n4; printf 'n5\n' >$S/n5; $PY $TOOL capture --out $S/five.txt --paths $S/n1 $S/n2 $S/n3 $S/n4 $S/n5 --label five && $PY $TOOL verify $S/five.txt --live --require-paths 5"
r B3-absent-inside-covered verify "$R2/capture-pre.txt" --live --require-paths 5
r B4-require-zero verify "$S/f.conf" --live --require-paths 0
r B5-require-negative verify "$S/f.conf" --live --require-paths -1

# --- D6 attacks ---
s D1-symlink-missing-scratch "ln -s $S/nope $S/scr-link && $PY $TOOL selftest --scratch $S/scr-link"
s D2-symlink-valid-scratch "mkdir -p $S/real-scr && ln -s $S/real-scr $S/scr-good && $PY $TOOL selftest --scratch $S/scr-good | tail -2"
s D3-env-tmp-scratch "CUSTODY_PAIR_SCRATCH=/tmp/rv5-must-not $PY $TOOL selftest | tail -2"
r D4-explicit-tmp selftest --scratch /tmp/rv5-must-not
s D5-default-scratch "$PY $TOOL selftest | tail -2"

# --- cross-version / regression ---
r E1-cross-version verify "$R2/capture-pre.txt" "$R2/capture-post.txt"
r E2-v1-vs-r2v2 verify "$R2/capture-pre.txt" /var/tmp/rv5/scratch/after-03bd6242/live-pre.txt
s E3-empty-receipt "printf '' >$S/empty.txt && $PY $TOOL verify $S/empty.txt --live"
s E4-mixed-sums-v2 "printf '%s  %s\n' $(sha256sum $S/f.conf | cut -d' ' -f1) $S/f.conf >$S/sums.txt && $PY $TOOL verify $S/sums.txt $S/new-out.txt 2>/dev/null || true; $PY $TOOL verify $S/sums.txt --live | tail -3"

# --- command A recipe at HEAD (SCORECARD) ---
s F1-commandA "cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 - HEAD <<'PY'
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path): return subprocess.check_output(['git','show',f'{rev}:{path}'],text=True)
paths = subprocess.check_output(['git','ls-tree','-r','--name-only',rev,'--','corpus/knowledge'],text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n',1)[1].split('\n## ',1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule); valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/'+name).splitlines()); start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError: valid = False
    resolved += valid
print(json.dumps({'revision': rev, 'mapped': len(files & mapped), 'knowledge_files': len(files),
 'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
 'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
 'coverage_score': round(10*len(files & mapped)/len(files),2),
 'depth_score': round(10*resolved/len(rules),2)}, sort_keys=True))
PY"

# --- diff scope: which files did the round's C2 landing touch ---
s F2-diff-scope "cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git status --porcelain && echo '---' && git diff --stat -- .ufo/gates/custody-pair/"
echo ATTACK-END >>"$LOG"; exit 0