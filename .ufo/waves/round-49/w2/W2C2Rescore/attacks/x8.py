import sys, importlib.util, json, re
D = '/fast/scratch/hyaku/kaidoku-r49/W2C2Rescore/clone.m6J4'
R = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('c2', D + '/tools/round-49/c2-mismatch.py')
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
g = c2.Git(D)
sx = c2.text(g.show(R, 'corpus/SOURCES.md'))
sy = g.show(R, 'corpus/evidence/round-49/c2/sysexits.html')
forged = sy + b'\n<p>EX_USAGE is 2 in some other table</p>\n'
old_pin = c2.sha(sy); new_pin = c2.sha(forged)
s148 = [l for l in sx.split('\n') if l.startswith('| S148 |')][0]
row = s148.replace(old_pin, new_pin, 1)
assert row != s148
over = {'corpus/evidence/round-49/c2/sysexits.html': forged,
        'corpus/SOURCES.md': sx.replace(s148, row, 1).encode()}
got = c2.score(c2.Overlay(g, R, over), R)
print('X8 forged snapshot + re-pinned sha (adds EX_USAGE is 2 line) -> red', sorted(k for k,v in got.items() if v), {k:v for k,v in got.items() if v})
