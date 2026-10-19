#!/bin/bash
# RV-5 late-join independent battery — landed revision, read-only over custody paths.
# usage: battery.sh <outdir>
set -u
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
README=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/README.md
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c2
OUT="$1"
S=/var/tmp/rv5-late/scratch
rm -rf "$S"; mkdir -p "$S" "$OUT"
export PYTHONDONTWRITEBYTECODE=1
PY=python3
LOG="$OUT/battery.log"; : >"$LOG"

r() { local n="$1"; shift; { echo "### $n"; echo "\$ $*"; } >>"$LOG"; { "$PY" "$TOOL" "$@"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1; }
s() { local n="$1"; shift; { echo "### $n"; echo "\$ $*"; } >>"$LOG"; { bash -c "$*"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1; }

echo "== identity (re-derived by RV-5 at run time)" >>"$LOG"
sha256sum "$TOOL" "$README" >>"$LOG"
stat -c '%y %s %n' "$TOOL" "$README" >>"$LOG"
echo "date=$(date -Is)" >>"$LOG"

echo "== A. selftest at the landed revision (default scratch)" >>"$LOG"
r A1-selftest-default selftest 2>&1 | tail -1 >>"$LOG"

echo "== B. D2 closure: EACCES/stat-blocked -> declared UNEVALUABLE, no fail-open MATCH" >>"$LOG"
mkdir -p "$S/eacces-dir"; printf 'inner\n' >"$S/eacces-dir/inner.conf"; chmod 000 "$S/eacces-dir"
r B1-D2a-capture capture --out "$S/d2a.txt" --paths "$S/eacces-dir/inner.conf" --label d2a
r B2-D2a-verify-live verify "$S/d2a.txt" --live
r B3-D2a-verify-receipt-pair verify "$S/d2a.txt" "$S/d2a.txt"
chmod 755 "$S/eacces-dir"
printf 'unreadable\n' >"$S/unreadable.conf"; chmod 000 "$S/unreadable.conf"
r B4-D2b-capture capture --out "$S/d2b.txt" --paths "$S/unreadable.conf" --label d2b
chmod 644 "$S/unreadable.conf"
printf 'toggle\n' >"$S/toggle.conf"
r B5-D2c-capture capture --out "$S/d2c.txt" --paths "$S/toggle.conf" --label d2c
chmod 000 "$S/toggle.conf"
r B6-D2c-verify-live verify "$S/d2c.txt" --live
chmod 644 "$S/toggle.conf"
# negative controls
r B7-D2-negative-absent-at-capture capture --out "$S/absent.txt" --paths "$S/nope.conf" --label absent
r B8-D2-negative-both-absent-verify verify "$S/absent.txt" --live
printf 'present\n' >"$S/created.conf"
r B9-D2-negative-created-capture capture --out "$S/created-pre.txt" --paths "$S/created.conf" --label created
rm -f "$S/created.conf"
r B10-D2-negative-deleted-verify verify "$S/created-pre.txt" --live
# both directions of the EACCES class
printf 'ref-side\n' >"$S/refside.conf"; chmod 000 "$S/refside.conf"
r B11-D2-ref-side-capture capture --out "$S/refside.txt" --paths "$S/refside.conf" --label refside
chmod 644 "$S/refside.conf"
r B12-D2-ref-side-verify-live verify "$S/refside.txt" --live

echo "== C. D3 closure: coverage gate --require-paths" >>"$LOG"
printf 'one\n' >"$S/one.conf"
r C1-D3-capture-1of5 capture --out "$S/one.txt" --paths "$S/one.conf" --label one
r C2-D3-default-no-gate verify "$S/one.txt" --live
r C3-D3-require5 verify "$S/one.txt" --live --require-paths 5
r C4-D3-control-canonical5 verify "$W/receipts/config-post-pair-v2r3.txt" --live --require-paths 5
printf 'n1\n' >"$S/n1"; printf 'n2\n' >"$S/n2"; printf 'n3\n' >"$S/n3"; printf 'n4\n' >"$S/n4"; printf 'n5\n' >"$S/n5"
r C5-D3-capture-5-noncanonical capture --out "$S/five.txt" --paths "$S/n1" "$S/n2" "$S/n3" "$S/n4" "$S/n5" --label five
r C6-D3-5-noncanonical-require5 verify "$S/five.txt" --live --require-paths 5
r C7-D3-require0 verify "$S/one.txt" --live --require-paths 0
r C8-D3-require-neg1 verify "$S/one.txt" --live --require-paths -1

echo "== D. write-guard scope closure" >>"$LOG"
printf 'precious\n' >"$S/self.conf"; sha256sum "$S/self.conf" >>"$LOG"
r D1-guard-out-is-scoped capture --out "$S/self.conf" --paths "$S/self.conf" --label guard
sha256sum "$S/self.conf" >>"$LOG"
s D2-guard-relative "cd $S && $PY $TOOL capture --out ./rel.conf --paths ./rel.conf --label rel; ls rel.conf 2>&1"
printf 'scoped2\n' >"$S/scoped2.conf"; ln -s "$S/scoped2.conf" "$S/link2.conf"
r D3-guard-symlink-alias capture --out "$S/link2.conf" --paths "$S/scoped2.conf" --label sym
printf 'hl\n' >"$S/hl-a.conf"; ln "$S/hl-a.conf" "$S/hl-b.txt"
r D4-guard-hardlink-alias capture --out "$S/hl-b.txt" --paths "$S/hl-a.conf" --label hl
r D5-guard-custody-path capture --out "$HOME/.bashrc" --paths "$S/one.conf" --label cust
r D6-guard-negative-fresh-out capture --out "$S/fresh.txt" --paths "$S/one.conf" --label fresh
# precision probe: sidecar of a *measured receipt* as --out
printf 'x\n' >"$S/rec.txt"
r D7-guard-receipt-first capture --out "$S/rec.txt" --paths "$S/one.conf" --label rec
r D8-guard-sidecar-of-measured capture --out "$S/rec.txt.sha256" --paths "$S/rec.txt" --label sidecar

echo "== E. D6 closure: selftest scratch guard" >>"$LOG"
r E1-D6-missing selftest --scratch "$S/does-not-exist"
r E2-D6-file selftest --scratch "$S/one.conf"
r E3-D6-tmp selftest --scratch /tmp/rv5-must-not
ln -s "$S/nope" "$S/scr-link"
r E4-D6-symlink-to-missing selftest --scratch "$S/scr-link"
r E5-D6-negative-existing selftest --scratch "$S" 2>&1 | tail -1 >>"$LOG"
r E6-D6-tmp-message selftest --scratch /tmp/x 2>&1

echo "== F. regression spot checks (round-2 v2 behavior)" >>"$LOG"
printf 'reg\n' >"$S/reg.conf"; touch -d @1000000000 "$S/reg.conf"
r F1-reg-pre capture --out "$S/reg-pre.txt" --paths "$S/reg.conf" --label reg
s F2-reg-inplace-rewrite "touch -d @1000000000 $S/reg.conf && $PY $TOOL verify $S/reg-pre.txt --live"
printf 'reg-new\n' >"$S/reg.conf"
r F3-reg-content-drift verify "$S/reg-pre.txt" --live
printf 'rn\n' >"$S/rn.conf"; touch -d @1000000000 "$S/rn.conf"
r F4-rn-pre capture --out "$S/rn-pre.txt" --paths "$S/rn.conf" --label rn
s F5-rn-rename-rewrite "printf 'rn\n' >$S/rn.new && touch -d @1000000000 $S/rn.new && mv $S/rn.new $S/rn.conf && touch -d @1000000000 $S/rn.conf && $PY $TOOL verify $S/rn-pre.txt --live"
printf 'md\n' >"$S/md.conf"; touch -d @1000000000 "$S/md.conf"
r F6-md-pre capture --out "$S/md-pre.txt" --paths "$S/md.conf" --label md
chmod 600 "$S/md.conf"
r F7-md-verify verify "$S/md-pre.txt" --live
s F8-v1-shapes "$PY - $TOOL $S >>$LOG 2>&1 <<'PYEOF'
import sys, time
from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('cp', sys.argv[1]); cp = importlib.util.module_from_spec(spec); spec.loader.exec_module(cp)
sec = cp.capture_path(Path(sys.argv[2], 'one.conf'))
Path(sys.argv[2], 'v1-stanza.txt').write_text(
    'PATH: %s\nEXISTS: yes\nSIZE: %d\nMTIME_UTC: %s\nMODE: %s  UID: %d  GID: %d\nSHA256: %s\n' % (
        sec['path'], sec['size'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec['mtime_epoch'])),
        sec['mode'], sec['uid'], sec['gid'], sec['sha256']))
Path(sys.argv[2], 'v1-sums.txt').write_text('%s  %s\n' % (sec['sha256'], sec['path']))
Path(sys.argv[2], 'v1-pipe.txt').write_text('%s | %d | %s | %s | %d | 8 | %s\n' % (
        sec['path'], sec['inode'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec['ctime_epoch'])),
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec['mtime_epoch'])), sec['size'], sec['sha256']))
print('v1 fixtures written')
PYEOF"
r F9-v1-stanza-verify verify "$S/v1-stanza.txt" --live
r F10-v1-sums-verify verify "$S/v1-sums.txt" --live
r F11-v1-pipe-verify verify "$S/v1-pipe.txt" --live
printf 'not a receipt\n' >"$S/junk.txt"
r F12-unparsable verify "$S/junk.txt" --live

echo "== G. live pair + cross-revision (round claim evidence, re-run)" >>"$LOG"
R="$W/receipts"
r G1-revised-pair verify "$R/config-pre-pair-v2r3-revised.txt" "$R/config-post-pair-v2r3.txt"
r G2-revised-pair-require5 verify "$R/config-pre-pair-v2r3-revised.txt" "$R/config-post-pair-v2r3.txt" --require-paths 5
r G3-revised-pre-vs-live verify "$R/config-pre-pair-v2r3-revised.txt" --live
r G4-roundstart-pre-vs-post verify "$R/config-pre-pair-v2r3.txt" "$R/config-post-pair-v2r3.txt"
r G5-round2-pre-vs-r3post verify "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/capture-pre.txt" "$R/config-post-pair-v2r3.txt"
s G6-selfpin "grep -m1 '^# tool:' $R/config-pre-pair-v2r3-revised.txt $R/config-post-pair-v2r3.txt $R/config-pre-pair-v2r3.txt; sha256sum $R/config-pre-pair-v2r3-revised.txt $R/config-post-pair-v2r3.txt $R/config-pre-pair-v2r3.txt"
s G7-r1-v1-receipts "ls -la /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/ /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c3/EX-26/ 2>&1 | head -30"
r G8-r1-stanza-vs-live verify "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt" --live
r G9-r1-pipe-vs-live verify "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt" --live

echo "== H. command A at HEAD" >>"$LOG"
s H1-commandA "cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 - HEAD <<'PY'
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
 'citation_resolved_rules': resolved, 'rule_blocks': len(rules)}, sort_keys=True))
PY"
echo "== I. custody read-only check" >>"$LOG"
s I1-custody-shas "sha256sum $HOME/.config/devin/mcp_config.json $HOME/.omp/agent/mcp.json $HOME/.kimi-code/config.toml $HOME/.bashrc $HOME/.profile"
echo BATTERY-END >>"$LOG"
exit 0
