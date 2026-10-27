#!/usr/bin/env bash
# Read-only measurement sweep for the R43ScribeEntry draft.
# Writes only its stdout; the caller redirects to an artifact. No network, no VCS
# mutation: `git show`, `git diff --stat`, `git log`, `sha256sum`, `stat`, `python3`.
set -u
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
FREEZE=d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b
BASE=6b9e64fe7e0de202d9383baad5792fbfe039a743
STOP=eb8215ac87860f0e52745a4f842485bf8a6fe3b8
SITEPKG=$HOME/.local/share/uv/tools/unblob/lib/python3.13/site-packages

echo "## 1. frozen interpreter --table-only (cwd: \$S, TMPDIR: \$S)"
out=$(cd "${TMPDIR:-/var/tmp}" && python3 -I -B "$L/tools/round-42/sqfs-triage-v4.py" --skill "$L/SKILL.md" --table-only); rc=$?
printf '%s\n' "$out" | sed -n '1,4p'
echo "exit=$rc (interpreter's own exit, not a pipeline's)"
echo

echo "## 2. v4 region hash at FREEZE / BASE / HEAD"
python3 - "$L" "$FREEZE" "$BASE" <<'PY'
import hashlib, re, subprocess, sys
root, freeze, base = sys.argv[1:4]
MARK = '<!-- sqfs-triage-table v4 -->'
def show(rev):
    return subprocess.run(['git','-C',root,'show','%s:SKILL.md'%rev],capture_output=True,text=True,check=True).stdout
def region(text):
    lines=text.splitlines()
    start=next(i for i,l in enumerate(lines) if l.lower().startswith('## queue-drain craft'))
    end=next((i for i in range(start+1,len(lines)) if lines[i].startswith('## ')),len(lines))
    mi=next(i for i in range(start+1,end) if lines[i].strip().startswith(MARK))
    stop=end
    for i in range(mi+1,end):
        l=lines[i]
        if re.match(r'^#{1,4} ',l) or re.match(r'^\s*-\s+\*\*',l) or l.strip().startswith('<!-- sqfs-triage-table'):
            stop=i; break
    return '\n'.join(lines[mi:stop]).rstrip('\n')
for rev in (freeze, base, 'HEAD'):
    b=region(show(rev))
    print('%s  bytes=%d  rows=%d  sha256=%s' % (rev, len(b.encode()),
          sum(1 for l in b.splitlines() if l.lstrip().startswith('|'))-2,
          hashlib.sha256(b.encode()).hexdigest()))
PY
echo

echo "## 3. frozen tools: sha256 at FREEZE vs BASE vs HEAD"
for p in tools/round-42/sqfs-triage-v4.py tools/round-42/indep-eval-v4.py tools/round-42/fixtures.json tools/round-42/heldout-gen-v4.py; do
  for rev in "$FREEZE" "$BASE" HEAD; do
    printf '%s %s ' "$p" "${rev:0:8}"
    git -C "$L" show "$rev:$p" | sha256sum | cut -d' ' -f1
  done
done
echo

echo "## 4. SKILL.md edits since the freeze"
echo "\$ git -C \$L diff --stat $FREEZE..$BASE -- SKILL.md"
git -C "$L" diff --stat "$FREEZE..$BASE" -- SKILL.md | cat
echo "\$ git -C \$L diff --stat $BASE..HEAD -- SKILL.md"
git -C "$L" diff --stat "$BASE..HEAD" -- SKILL.md | cat
echo "\$ git -C \$L log --oneline $FREEZE..HEAD -- SKILL.md"
git -C "$L" log --oneline "$FREEZE..HEAD" -- SKILL.md | cat
echo

echo "## 5. S135: unblob 26.6.4 license in the installed distribution"
stat -c '%s bytes  %n' "$SITEPKG/unblob-26.6.4.dist-info/licenses/LICENSE"
sha256sum "$SITEPKG/unblob-26.6.4.dist-info/licenses/LICENSE"
echo

echo "## 6. S112/S118 installed-file pins"
sha256sum "$SITEPKG/unblob/handlers/filesystem/squashfs.py" "$SITEPKG/unblob/extractor.py"
echo

echo "## 7. S119: re-fetched 6.5.0 tarball in \$S/rea65 (scratch), never installed, never on PATH"
if [ -f "${TMPDIR:-/var/tmp}/rea65/rea-agents-6.5.0.tgz" ]; then
  sha256sum "${TMPDIR:-/var/tmp}/rea65/rea-agents-6.5.0.tgz" "${TMPDIR:-/var/tmp}/rea65/package/dist/firmware/FirmwarePublication.js"
  python3 -c "import json,sys;print('version',json.load(open(sys.argv[1]))['version'])" "${TMPDIR:-/var/tmp}/rea65/package/package.json"
else
  echo "(scratch copy absent; pins quoted from the fetch recorded in R43ScribeEntry.md)"
fi
echo

echo "## 8. round-42 stop receipt: facts, and where its bytes are committed"
python3 - "$L" "$STOP" <<'PY'
import json, subprocess, sys
root, stop = sys.argv[1], sys.argv[2]
p = '.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json'
d = json.load(open(root + '/' + p))
print('argv        :', ' '.join(d['argv']))
print('exit_code   :', d['exit_code'])
print('freeze      :', d['freeze'])
print('matched/n   :', d.get('matched'), '/', d.get('n'), '(pair_match true:', sum(1 for c in d['carriers'] if c.get('pair_match')), ')')
print('features ok :', sum(1 for c in d['carriers'] if c.get('features_match')), 'of', len(d['carriers']))
print('bindings_false:', d['bindings_false'])
print('mismatch    :', json.dumps(d['declared_features']['mismatch'], sort_keys=True))
import collections
c = collections.Counter(x['class'] for x in d['carriers'])
print('classes     : %d distinct, combo=%d, named=%d all two-each=%s'
      % (len(c), c['combo'], len(c) - 1, set(v for k, v in c.items() if k != 'combo')))
print('rows/decisions: %s rows, %s decision pairs' % (d['distinct_rows'], len(d['decision_pairs'])))
print('combo unseen :', len(d['combo_unseen_majority']['unseen']), 'need', d['combo_unseen_majority']['need'])
print('lookup score :', d['lookup']['score'], 'of', d['lookup']['n_combos'])
print('receipt at HEAD blob:', subprocess.run(['git','-C',root,'rev-parse','HEAD:'+p],capture_output=True,text=True).stdout.strip())
print('commits touching it:', ' '.join(subprocess.run(['git','-C',root,'log','--format=%h','--',p],capture_output=True,text=True).stdout.split()))
print('present at stop rev:', subprocess.run(['git','-C',root,'cat-file','-e',stop+':'+p]).returncode == 0)
PY
echo

echo "## 9. what round-43 tool code exists at the base"
ls "$L/tools/round-43" 2>&1 | sed 's/^/  /'
git -C "$L" ls-tree -r --name-only "$BASE" tools/round-43 | sed 's/^/  tracked at base: /'
