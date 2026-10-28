import sys, subprocess, re, json, importlib.util, os
sys.dont_write_bytecode = True
C = os.environ['C']; L = os.environ['L']; A = os.environ['A']; S = os.environ['S']
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
cc = load('c1c', C + '/tools/round-49/c1-controls.py')
cn = load('c1n', C + '/tools/round-49/c1-counter.py')
freeze = subprocess.check_output(['git', '-C', C, 'rev-parse', 'HEAD']).decode().strip()
ctx = {'root': C, 'freeze': freeze, 'doc_dir': A, 'work': S + '/pos-probe-work'}
os.makedirs(ctx['work'], exist_ok=True)
import inspect
print('_doc_landing signature:', inspect.signature(cc._doc_landing))
out, lens = cc._doc_landing(ctx)
print('planted keys:', sorted(out.keys()))
print('block lens:', lens)
sources_new = out['corpus/SOURCES.md'].decode().split('\n')
base = subprocess.check_output(['git', '-C', C, 'show', freeze + ':corpus/SOURCES.md']).decode().split('\n')
for tag, lines in (('base', base), ('pos-planted', sources_new)):
    for l in lines:
        if re.match(r'^ {0,3}\|\s*(S138|S139)\s*\|', l):
            c = cn.cells(l)
            print(tag, 'cells=%d' % len(c), 'id=%s' % c[0], 'opened=%r' % c[8], 'used-by=%r' % c[10][-160:])
ENTRY = cn.ENTRY; STEM = cn.STEM; OPENED = cn.OPENED
def sourced(lines):
    ok = []
    for line in lines:
        if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line): continue
        c = cn.cells(line)
        if len(c) != 11: continue
        if c[0] in ('S138', 'S139') and c[8] == OPENED and (ENTRY in c[10] or STEM in c[10]):
            ok.append(c[0])
    return sorted(ok)
print('counter sourced rows, base          :', sourced(base))
print('counter sourced rows, POS-planted   :', sourced(sources_new))
print('counter sourced rows, real landing w/o SOURCES edit = base :', sourced(base))
print('ENTRY=', ENTRY, 'OPENED=', OPENED)
