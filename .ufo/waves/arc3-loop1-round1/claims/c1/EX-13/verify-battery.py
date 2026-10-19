# NOTE (EX-13, kept after cleanup): run from the repo root. It expects a scratch
# bare clone at <this-dir>/_scratch/repo.git; recreate with:
#   mkdir -p <this-dir>/_scratch && git clone --bare --local . <this-dir>/_scratch/repo.git
# The scratch clone was removed at seat close (host /tmp was quota-blocked).
#!/usr/bin/env python3
"""EX-13 verification harness (transient scratch; transcript kept as artifact).

Verifies each candidate hunk for the corpus/README.md EVM-row map-token append:
  V1 line-neutrality   190 -> 190 lines, only line 38 differs, others byte-identical
  V2 token multiset    unique 81 -> 82; added == {new token}; removed []; prior counts equal
  V3 token-insert identity on line 38 (plus whether the state-cell prose changed)
  V4 apply             git apply --check + apply in a scratch tree -> byte-identical result
  V5 probe             citation-drift probe at the patched scratch commit -> findings=0
  V6 command A         with EX-12's landed entry stem -> 82/82, missing [], dangling []
  V7 command A         stem-mismatch attack -> dangling [token]
"""
import hashlib, json, os, pathlib, re, subprocess
from collections import Counter

REPO = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
SC = REPO/'.ufo/waves/arc3-loop1-round1/claims/c1/EX-13/_scratch'
GITDIR = SC/'repo.git'
BEFORE = (REPO/'corpus/README.md').read_text(encoding='utf-8')
ENTRY = '2026-10-19-arc3-r1-evm-real-solc'      # EX-12 landed stem (claims/c1/EX-12/knowledge-entry.patch.md)
PLAN = '2026-10-19-arc3-r1-evm-solc'            # PL-1 plan name (superseded by the landed entry)
TOKEN_RE = re.compile(r'2026-10-\d{2}-[a-z0-9-]+')


def sha(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def git_blob_sha(data):
    b = data.encode('utf-8')
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def map_tokens(readme):
    sec = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    return TOKEN_RE.findall(sec)


def git(*args, check=True):
    p = subprocess.run(['git', '--git-dir', str(GITDIR)] + list(args),
                       capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError('git %s: %s' % (args, p.stderr))
    return p


def commit_readme(text, message):
    blob = subprocess.run(['git', '--git-dir', str(GITDIR), 'hash-object', '-w', '--stdin'],
                          input=text.encode('utf-8'), capture_output=True).stdout.decode().strip()
    idx = SC/'idx.tmp'
    if idx.exists():
        idx.unlink()
    e = dict(os.environ, GIT_INDEX_FILE=str(idx))
    subprocess.run(['git', '--git-dir', str(GITDIR), 'read-tree', 'HEAD'], env=e, check=True)
    subprocess.run(['git', '--git-dir', str(GITDIR), 'update-index', '--cacheinfo',
                    '100644,%s,corpus/README.md' % blob], env=e, check=True)
    tree = subprocess.run(['git', '--git-dir', str(GITDIR), 'write-tree'],
                          env=e, capture_output=True, text=True).stdout.strip()
    return subprocess.run(['git', '--git-dir', str(GITDIR), '-c', 'user.name=ex13',
                           '-c', 'user.email=ex13@local', 'commit-tree', tree, '-p', 'HEAD',
                           '-m', message], capture_output=True, text=True).stdout.strip()


def command_a(readme_text, landed_stems):
    paths = git('ls-tree', '-r', '--name-only', 'HEAD', '--', 'corpus/knowledge').stdout.splitlines()
    files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
    files |= set(landed_stems)
    mapped = set(map_tokens(readme_text))
    craft = git('show', 'HEAD:SKILL.md').stdout.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            p = git('show', 'HEAD:corpus/knowledge/' + name, check=False)
            if p.returncode != 0:
                valid = False
                continue
            count = len(p.stdout.splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        resolved += valid
    return {'knowledge_files': len(files), 'mapped': len(files & mapped),
            'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
            'citation_resolved_rules': resolved, 'rule_blocks': len(rules)}


def build_patch(newline):
    lines = BEFORE.splitlines()
    ctx = lines[34:41]
    patched = BEFORE.replace(lines[37] + '\n', newline + '\n')
    return '\n'.join([
        'diff --git a/corpus/README.md b/corpus/README.md',
        'index %s..%s 100644' % (git_blob_sha(BEFORE)[:7], git_blob_sha(patched)[:7]),
        '--- a/corpus/README.md',
        '+++ b/corpus/README.md',
        '@@ -35,7 +35,7 @@ A row is written when its file exists, never before.',
        ' ' + ctx[0], ' ' + ctx[1], ' ' + ctx[2],
        '-' + ctx[3], '+' + newline,
        ' ' + ctx[4], ' ' + ctx[5], ' ' + ctx[6]]) + '\n'


def verify(name, stem, prose):
    old_lines = BEFORE.splitlines()
    old_line = old_lines[37]
    k = old_line.index(' | held')
    insert = ', `%s`' % stem
    tail = ('EVMole selectors recovered from synthetic dispatcher (r3-07) and real '
            'solc-compiled runtime (arc3-r1); positional encoding quirk' if prose else
            'EVMole selectors recovered from synthetic dispatcher; positional encoding quirk')
    newline = '| EVM | `2026-10-13-r3-evm-interface`%s | held — %s |' % (insert, tail)
    print('=' * 74)
    print('VARIANT %s (stem %s, prose %s)  new-line sha256 %s'
          % (name, stem, 'changed' if prose else 'untouched', sha(newline + '\n')))
    assert BEFORE.count(old_line + '\n') == 1
    patched = BEFORE.replace(old_line + '\n', newline + '\n')
    new_lines = patched.splitlines()
    tok_ident = new_lines[37][:k + len(insert)] == old_line[:k] + insert
    prose_changed = new_lines[37][k + len(insert):] != old_line[k:]
    print('V3 token-insert identity: %s | state-cell prose changed: %s   (old line sha256 %s)'
          % (tok_ident, prose_changed, sha(old_line + '\n')))
    assert tok_ident and prose_changed == prose
    diffs = [i + 1 for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
    print('V1 line-neutrality: lines %d -> %d, differing %s, other lines byte-identical: %s, pipes %d -> %d'
          % (len(old_lines), len(new_lines), diffs,
             all(a == b for i, (a, b) in enumerate(zip(old_lines, new_lines)) if i + 1 not in diffs),
             old_line.count('|'), new_lines[37].count('|')))
    assert len(old_lines) == len(new_lines) == 190 and diffs == [38]
    tb, ta = Counter(map_tokens(BEFORE)), Counter(map_tokens(patched))
    print('V2 tokens: unique %d -> %d, occurrences %d -> %d, added %s, removed %s, prior counts equal: %s'
          % (len(tb), len(ta), sum(tb.values()), sum(ta.values()),
             sorted((ta - tb).elements()), sorted((tb - ta).elements()),
             all(ta[t] == tb[t] for t in tb)))
    assert len(tb) == 81 and len(ta) == 82 and list((ta - tb).elements()) == [stem] and not (tb - ta)
    print('    result sha256:', sha(patched))
    (SC/('README.%s' % name)).write_text(patched, encoding='utf-8')
    patch = build_patch(newline)
    (SC/('patch.%s' % name)).write_text(patch, encoding='utf-8')
    print('    patch sha256:', sha(patch))
    ad = SC/('applytest-%s' % name)
    subprocess.run(['rm', '-rf', str(ad)])
    (ad/'corpus').mkdir(parents=True)
    (ad/'corpus/README.md').write_text(BEFORE, encoding='utf-8')
    subprocess.run(['git', 'init', '-q'], cwd=ad, check=True)
    p = subprocess.run(['git', 'apply', '--check', str(SC/('patch.%s' % name))], cwd=ad,
                       capture_output=True, text=True)
    print('V4 git apply --check: exit %d %s' % (p.returncode, p.stderr.strip()))
    assert p.returncode == 0
    subprocess.run(['git', 'apply', str(SC/('patch.%s' % name))], cwd=ad, check=True)
    applied = (ad/'corpus/README.md').read_text(encoding='utf-8')
    print('    applied sha256: %s  byte-identical: %s' % (sha(applied), applied == patched))
    assert applied == patched
    rev = commit_readme(patched, 'EX-13 %s' % name)
    p = subprocess.run(['python3', str(REPO/'.ufo/gates/citation-drift/citation-drift-probe.py'),
                        '--root', str(GITDIR), '--rev', rev,
                        '--table', str(REPO/'.ufo/gates/citation-drift/pointer-table.json'),
                        '--expected', str(REPO/'.ufo/gates/citation-drift/expected.json')],
                       capture_output=True, text=True)
    verdict = [l for l in p.stdout.splitlines() if 'VERDICT' in l]
    print('V5 citation-drift probe @ %s: exit %d | %s' % (rev, p.returncode, verdict))
    assert p.returncode == 0 and any('findings=0' in v for v in verdict)
    print('V6 command A (EX-12 entry landed):', json.dumps(command_a(patched, [ENTRY]), sort_keys=True))
    print('V7 command A (no entry landed):  ', json.dumps(command_a(patched, []), sort_keys=True))
    print('    patched commit: %s' % rev)
    return rev


print('REPO HEAD:', subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'HEAD'],
                                   capture_output=True, text=True).stdout.strip())
print('README before sha256:', sha(BEFORE), '| lines', len(BEFORE.splitlines()))
print('EX-12 landed entry stem: %s | plan stem (superseded): %s' % (ENTRY, PLAN))
v1 = verify('v1', ENTRY, prose=False)   # primary: token-only, landed stem (== RV-4 frozen bytes)
v2 = verify('v2', ENTRY, prose=True)    # alternate: same-line state-cell prose also updated
v3 = verify('v3', PLAN, prose=False)    # attack: plan-name stem against the landed entry
print('=' * 74)
print('SUMMARY  v1 %s | v2 %s | v3 %s' % (v1, v2, v3))
