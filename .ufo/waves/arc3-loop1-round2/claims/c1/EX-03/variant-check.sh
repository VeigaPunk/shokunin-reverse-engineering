#!/usr/bin/env bash
# EX-03 independent re-measurement: variant scoring of candidate rule #14 texts
# against command A's real parser (SCORECARD.md:94-122 recipe). Scratch repo
# under /var/tmp only; the lane repo is never written.
set -euo pipefail
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
WORK=/var/tmp/ex03/variants
rm -rf "$WORK"; mkdir -p "$WORK/repo"
cd "$REPO"
git archive HEAD | tar -x -C "$WORK/repo"
cd "$WORK/repo"
git init -q .
git config user.email ex03@scratch; git config user.name EX-03
git add -A >/dev/null; git commit -qm "arch3-loop1r2 base" 
BASE=$(git rev-parse HEAD)
echo "BASE=$BASE"

runA() {
python3 - "$1" <<'PY'
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(['git','show',f'{rev}:{path}'], text=True)
paths = subprocess.check_output(['git','ls-tree','-r','--name-only',rev,'--','corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n',1)[1].split('\n## ',1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/'+name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    resolved += valid
print(json.dumps({'revision':rev,'mapped':len(files & mapped),'knowledge_files':len(files),
 'missing':sorted(files-mapped),'dangling':sorted(mapped-files),'citation_resolved_rules':resolved,
 'rule_blocks':len(rules),'coverage_score':round(10*len(files & mapped)/len(files),2),
 'depth_score':round(10*resolved/len(rules),2)}, sort_keys=True))
PY
}

echo "== base =="; runA "$BASE"

MARKER='## Config custody for live-probe rounds (SOP)'
insert() {  # $1 = block file
python3 - "$MARKER" "$1" <<'PY'
import pathlib, sys
marker, blockfile = sys.argv[1], sys.argv[2]
p = pathlib.Path('SKILL.md'); t = p.read_text()
block = pathlib.Path(blockfile).read_text().rstrip('\n') + '\n'
head, tail = t.split(marker, 1)
p.write_text(head.rstrip('\n') + '\n\n' + block + '\n' + marker + tail)
print('inserted', blockfile)
PY
}

mk_t1() { cat > "$WORK/t1.md" <<'EOF'
- **An artifact that records its own byte-identity must re-derive that identity after every revision; a stale self-identity voids the verification block, not the work.** The arc3-loop1-round1 entry patch churned mid-wave: its recorded identity (8,316 B, `f95c5a05…`) stopped describing the artifact it produced — an independent re-apply read 8,598 B, `d8d85949…` (`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; VZ-1 debt D9, `.ufo/waves/arc3-loop1-round1/claims/c1/VZ-1/verdict.md:149-166`), and the landed bytes were re-derived at landing (10,225 B, `dd986f56…`, `.ufo/waves/arc3-loop1-round1/claims/cross/wave-summary.md:50`). Re-derive before citing; the integrator records the fresh identity at landing.
EOF
}
mk_t2() { cat > "$WORK/t2.md" <<'EOF'
- **An artifact that records its own byte-identity must re-derive that identity after every revision; a stale self-identity voids the verification block, not the work.** The arc3-loop1-round1 entry patch churned mid-wave: its recorded identity (8,316 B, `f95c5a05…`) stopped describing the artifact it produced — an independent re-apply read 8,598 B, `d8d85949…` (`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; VZ-1 debt D9, `.ufo/waves/arc3-loop1-round1/claims/c1/VZ-1/verdict.md:149-166`), and the landed bytes were re-derived at landing (10,225 B, `dd986f56…`, `.ufo/waves/arc3-loop1-round1/claims/cross/wave-summary.md:50`). Re-derive before citing; the integrator records the fresh identity at landing. The re-derivation discipline's analogue in the evidence-id family is recorded where an id held across a day and re-derives byte-exact (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`).
EOF
}
mk_t3() { cat > "$WORK/t3.md" <<'EOF'
- **Cite the source you measured, not the one you remember.** (`corpus/knowledge/2026-10-13-r3-evm-interface.md:23-25`)
EOF
}

for V in t1 t2 t3; do
  mk_$V
  git checkout -q "$BASE" -- SKILL.md
  insert "$WORK/$V.md"
  git add -A >/dev/null; git commit -qm "$V variant" >/dev/null
  echo "== $V =="; runA HEAD
done
