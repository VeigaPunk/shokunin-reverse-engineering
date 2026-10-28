import sys, os, importlib.util
sys.dont_write_bytecode = True
C = os.environ['C']; S = os.environ['S']
spec = importlib.util.spec_from_file_location('c1r', C + '/tools/round-49/c1-run.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print('FIXTURE_DIRS=', m.FIXTURE_DIRS)
print('listing=', [os.path.relpath(p, C) for p in m.fixture_listing(C)])
for cid in ('v1le', 'v1be', 'v2le', 'v2be', 'v21le', 'v21be', 'v2.1le', 'V2LE'):
    try:
        r = m.resolve_fixture(C, cid, {})
        print('no-path entry', cid, '->', r)
    except Exception as e:
        print('no-path entry', cid, 'raises', type(e).__name__, str(e)[:160])
