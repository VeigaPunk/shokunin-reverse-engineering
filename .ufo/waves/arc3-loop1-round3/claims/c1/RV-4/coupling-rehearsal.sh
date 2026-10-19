#!/usr/bin/env bash
# RV-4 coupling rehearsal: command A 82 -> 83 on a scratch clone of the lane repo.
# Uses real Git objects (recipe A reads `git show <rev>:<path>`), never the lane worktree.
set -euo pipefail
SRC=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=/dev/shm/rv4r3/coupling
rm -rf "$W"; mkdir -p "$W"
cd "$W"
git init -q .
mkdir -p corpus
git config user.email rv4@local; git config user.name rv4
# seed from HEAD objects (immutable), not the moving worktree
git --git-dir="$SRC/.git" archive HEAD corpus/README.md SKILL.md corpus/knowledge | tar -x -C "$W"
git add -A && git commit -qm "before: HEAD state"
BEFORE=$(git rev-parse HEAD)
echo "before_rev=$BEFORE"
echo "before_readme_sha=$(sha256sum corpus/README.md | cut -d' ' -f1)"

# apply the extracted PRIMARY after-state (built mechanically from the artifact bytes)
cp /dev/shm/rv4r3/built/primary.README.md corpus/README.md
# stub the new entry file with the token stem (content-shaped, not the real entry)
cat > corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md <<'MD'
# STUB (RV-4 coupling rehearsal) — token stem coupling only
placeholder body; the real entry lands with the round.
MD
git add -A && git commit -qm "after: primary map token + stub entry (coupled)"
AFTER=$(git rev-parse HEAD)
echo "after_rev=$AFTER"
echo "after_readme_sha=$(sha256sum corpus/README.md | cut -d' ' -f1)"

# uncoupled control: same README, entry file removed
git rm -q corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md
git commit -qm "control: map token without entry file"
UNCOUPLED=$(git rev-parse HEAD)

echo "--- probe helper ---"
cat > /dev/shm/rv4r3/coupling/a.py <<'PY'
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev,
                                 '--', 'corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    resolved += valid
print(json.dumps({'revision': rev, 'mapped': len(files & mapped),
 'knowledge_files': len(files), 'missing': sorted(files - mapped),
 'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
 'rule_blocks': len(rules), 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
PY
echo "--- command A at three revisions ---"
for r in "$BEFORE" "$AFTER" "$UNCOUPLED"; do python3 /dev/shm/rv4r3/coupling/a.py "$r"; done
echo "--- worktree guard: lane repo README untouched? ---"
echo "lane_readme_sha=$(sha256sum "$SRC/corpus/README.md" | cut -d' ' -f1) (expect 6ac43e838bca7d08cc7ac3c24cff60042cb174d92b08363db0798fa844163577)"