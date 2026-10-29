# Sweep: every tools/round-4[1-9]/**.py|.sh at BASE vs cell-0 paths of the marker-bound instrument-registry section in SKILL.md at BASE.
# Read-only: git show / git ls-tree only. Exit 0 = all registered, 1 = unregistered paths exist, 2 = could not evaluate.
import re, subprocess, sys
rev = sys.argv[1]; root = sys.argv[2] if len(sys.argv) > 2 else '.'
def git(*a):
    return subprocess.run(['git', '-C', root, *a], capture_output=True, text=True)
skill = git('show', f'{rev}:SKILL.md')
if skill.returncode: print('could-not-evaluate: SKILL.md absent at rev'); sys.exit(2)
s = skill.stdout
opens = [m.start() for m in re.finditer(r'<!-- instrument-registry v2 -->', s)]
closes = [m.start() for m in re.finditer(r'<!-- /instrument-registry -->', s)]
print(f'markers open={len(opens)} close={len(closes)}')
if len(opens) != 1 or len(closes) != 1: sys.exit(2)
sec = s[opens[0]:closes[0]]
registered = set()
for line in sec.splitlines():
    if line.startswith('| `tools/'):
        cell0 = line.split('|')[1].strip()
        registered.add(cell0.strip('`'))
print(f'registered_rows_in_marker_section={len(registered)}')
ls = git('ls-tree', '-r', '--name-only', rev, '--', 'tools')
files = [f for f in ls.stdout.splitlines() if re.match(r'tools/round-4[1-9]/.*\.(py|sh)$', f)]
missing = []
for f in files:
    tag = 'REG' if f in registered else 'UNREG'
    print(f'{tag}\t{f}')
    if tag == 'UNREG': missing.append(f)
print(f'files_total={len(files)} unregistered={len(missing)}')
sys.exit(1 if missing else 0)
