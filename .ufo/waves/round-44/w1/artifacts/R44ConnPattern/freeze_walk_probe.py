import os, subprocess, shutil
BASE = '/fast/scratch/hyaku/kaidoku-r44/probe-ConnPattern/cases'

def sh(root, *a, check=True):
    p = subprocess.run(['git', '-C', root, *a], capture_output=True, text=True)
    if check and p.returncode: raise SystemExit(f'{a} rc={p.returncode} {p.stderr}')
    return p.stdout.strip()

def w(root, path, text):
    with open(os.path.join(root, path), 'w') as f: f.write(text)
    sh(root, 'add', path)

def commit(root, msg):
    subprocess.run(['git','-C',root,'-c','user.name=p','-c','user.email=p@x','commit','-q','--allow-empty','-m',msg],check=True)
    return sh(root,'rev-parse','HEAD')

def fresh(name):
    root = os.path.join(BASE, name)
    shutil.rmtree(root, ignore_errors=True); os.makedirs(root)
    sh(root, 'init', '-q', '-b', 'main')
    w(root, 'F', 'orig\n'); w(root, 'base.txt', 'b\n')
    return root, commit(root, 'freeze')

def walk_r42(root, freeze, rev, path):
    # round-42 c1-counter.py frozen_drift: plain git log --name-only, exact-path set intersection
    out = sh(root, 'log', '--pretty=format:', '--name-only', '--no-renames', f'{freeze}..{rev}')
    return path in {l.strip() for l in out.splitlines() if l.strip()}

def walk_r43(root, freeze, rev, path, full=False):
    # round-43 c1-counter.py frozen_drift: merge-aware, status filter, tree backstop
    fb = sh(root, 'cat-file', '-t', f'{freeze}:{path}', check=False) == 'blob'
    args = ['log', '--format=@@%H', '--name-status', '--no-renames', '-m', '--diff-merges=first-parent']
    if full: args.append('--full-history')
    out = sh(root, *args, f'{freeze}..{rev}', '--', path)
    hits = set(); cur = None
    for line in out.splitlines():
        if line.startswith('@@'): cur = line[2:]; continue
        if not line.strip() or cur is None: continue
        st = line.split('\t')[0].strip()[:1]
        if st in ('M','D','R','T','U') or (st == 'A' and fb): hits.add(cur)
    if fb and sh(root,'rev-parse',f'{freeze}:{path}') != sh(root,'rev-parse',f'{rev}:{path}'):
        hits.add(rev)
    return bool(hits)

def run(name, build):
    root, freeze = fresh(name)
    rev = build(root)
    res = {'r42': walk_r42(root, freeze, rev, 'F'),
           'r43': walk_r43(root, freeze, rev, 'F'),
           'r43_full': walk_r43(root, freeze, rev, 'F', full=True),
           'bytes_differ': sh(root,'rev-parse',f'{freeze}:F') != sh(root,'rev-parse',f'{rev}:F')}
    print(f'{name:28s} touched(r42)={res["r42"]!s:5} touched(r43)={res["r43"]!s:5} touched(r43+full)={res["r43_full"]!s:5} endpoint_bytes_differ={res["bytes_differ"]}')

def linear_edit_restore(root):
    w(root,'F','x\n'); commit(root,'edit'); w(root,'F','orig\n'); return commit(root,'restore')

def merge_resolution_edit(root):
    # side adds unrelated file; main adds unrelated file; merge commit itself edits F
    sh(root,'checkout','-q','-b','side'); w(root,'s.txt','s\n'); commit(root,'side')
    sh(root,'checkout','-q','main'); w(root,'m.txt','m\n'); commit(root,'main')
    subprocess.run(['git','-C',root,'-c','user.name=p','-c','user.email=p@x','merge','-q','--no-ff','--no-commit','side'],check=True)
    w(root,'F','merge-edit\n')
    return commit(root,'merge with F edit')

def side_edit_then_restore_merged(root):
    # side edits F and restores it; merge brings a tree where F == freeze bytes
    sh(root,'checkout','-q','-b','side2'); w(root,'F','x\n'); commit(root,'side edit'); w(root,'F','orig\n'); commit(root,'side restore')
    sh(root,'checkout','-q','main'); w(root,'m2.txt','m\n'); commit(root,'main 2')
    subprocess.run(['git','-C',root,'-c','user.name=p','-c','user.email=p@x','merge','-q','--no-ff','side2','-m','merge side2'],check=True)
    return sh(root,'rev-parse','HEAD')

def side_edit_restore_then_delete_readd(root):
    # sanity: delete then re-add
    w(root,'F','x\n'); commit(root,'edit'); subprocess.run(['git','-C',root,'rm','-q','F'],check=True); commit(root,'rm'); w(root,'F','orig\n'); return commit(root,'readd')

def side_edit_restore_no_merge(root):
    # same as merged case but no merge: linear side edit+restore on main
    w(root,'F','x\n'); commit(root,'edit'); w(root,'F','orig\n'); return commit(root,'restore')

run('linear_edit_restore', linear_edit_restore)
run('merge_resolution_edit', merge_resolution_edit)
run('side_edit_restore_merged', side_edit_then_restore_merged)
run('delete_readd', side_edit_restore_then_delete_readd)
