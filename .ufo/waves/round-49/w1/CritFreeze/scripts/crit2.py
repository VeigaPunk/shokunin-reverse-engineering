import json, os, sys, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crit as C
from crit import g, mkrepo, commit, write, FREEZE, BASE
res = {}
def walks(name, d, rev, freeze):
    C.FREEZE = freeze
    rec = {'rev': rev, 'freeze': freeze, 'c1_walk': C.c1_walk(d, rev), 'c2_walk': C.c2_walk(d, rev)}
    res[name] = rec; print(json.dumps({name: rec}, sort_keys=True), flush=True)

def run(name, fn):
    C.FREEZE = FREEZE
    d = mkrepo(name); rev = fn(d); walks(name, d, rev, FREEZE)

# S10 REV before freeze (base)
def s10(d):
    return g(d, 'rev-parse', 'HEAD~0', ).stdout.decode().strip() if False else g(d, 'rev-parse', 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9').stdout.decode().strip()
C.FREEZE = FREEZE
d = mkrepo('S10_rev_is_base'); rev = s10(d); walks('S10_rev_is_base', d, rev, FREEZE)

# S11 sibling branch from base re-adding identical tools in its own commit
def s11(d):
    g(d, 'checkout', '-q', '-b', 'sib', 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9')
    g(d, 'checkout', FREEZE, '--', 'tools/round-49', 'plans/round-49-claims.md'); g(d, 'add', '-A')
    return commit(d, 'sibling re-add tools')
C.FREEZE = FREEZE
d = mkrepo('S11_sibling_readd'); rev = s11(d); walks('S11_sibling_readd', d, rev, FREEZE)

# S12 freeze contains a non-ASCII file; post-freeze edit of it. Build F2 in its own clone first.
d2 = mkrepo('S12_freeze2_build')
write(d2, 'tools/round-49/ü-note.txt', 'frozen note\n'); g(d2, 'add', '-A'); F2 = commit(d2, 'dev freeze 2 with non-ascii tool file')
d = mkrepo('S12_quoted_name_edit', src=d2, at=F2)
write(d, 'tools/round-49/ü-note.txt', 'edited after freeze\n'); g(d, 'add', '-A'); rev = commit(d, 'edit non-ascii frozen file')
walks('S12_quoted_name_edit', d, rev, F2)
print('quotepath line:', g(d, 'log', '-m', '--diff-merges=first-parent', '--name-status', '--pretty=format:', F2 + '..' + rev).stdout.decode().strip())

# S13 operator-chosen freeze: a NEW commit on base with different tool bytes, passed as --freeze
d = mkrepo('S13_refreeze_build')
write(d, 'tools/round-49/c2-mismatch.py', '# attacker-chosen freeze\n'); g(d, 'add', '-A'); F3 = commit(d, 'attacker freeze')
write(d, 'notes/after.txt', 'x\n'); g(d, 'add', '-A'); rev = commit(d, 'after refreeze')
walks('S13_refreeze_operator_freeze', d, rev, F3)

# S3d side edits carriers then reverts on the side; merge resolves to freeze bytes
d = mkrepo('S3d_side_edit_revert_on_side')
g(d, 'checkout', '-q', '-b', 'side', FREEZE)
p = os.path.join(d, 'tools/round-49/carriers.json'); open(p, 'a').write('\n'); g(d, 'add', '-A'); commit(d, 'side edit')
g(d, 'checkout', FREEZE, '--', 'tools/round-49/carriers.json'); g(d, 'add', '-A'); commit(d, 'side revert')
g(d, 'checkout', '-q', '-b', 'main2', FREEZE); write(d, 'notes/main.txt', 'm\n'); g(d, 'add', '-A'); commit(d, 'main')
g(d, 'merge', '-q', '--no-ff', '-m', 'merge side (net no change)', 'side'); rev = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
walks('S3d_side_edit_revert_on_side', d, rev, FREEZE)

# S14 copy-then-delete in one commit (rename detection -> R) vs plain add (A) of same content
d = mkrepo('S14_plain_copy_add')
shutil.copy(os.path.join(d, 'corpus/README.md'), os.path.join(d, 'tools/round-49/README-copy.md'))
g(d, 'add', '-A'); rev = commit(d, 'plain copy into tools')
walks('S14_plain_copy_add', d, rev, FREEZE)

json.dump(res, open(os.path.join(C.S, 'results-walk2.json'), 'w'), indent=1, sort_keys=True)
