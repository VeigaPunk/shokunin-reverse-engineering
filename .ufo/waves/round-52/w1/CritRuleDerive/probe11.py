#!/usr/bin/env python3
"""Probe 11: final verification of the shape-clause holes and the census reader."""
import importlib.util, json, os, copy, subprocess, tempfile, shutil

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('r50c1', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

LAW = {'claim':'R52-C1',
  'allowed': {'symlink':['unpublished-entry'],'char-device':[],'block-device':[],'fifo':[],'socket':[],'dir':[]},
  'required': {'symlink':True,'char-device':False,'block-device':False,'fifo':False,'socket':False,'dir':False},
  'removed': {'diagnostic':'MaliciousSymlinkRemoved','kinds':['symlink'],'disposition':'exclusive','silent':{}},
  'structural': {'depth-limited':1,'unknown-chunk-handler':0}}
DEV = ('char-device','block-device','fifo','socket')

def shape_draft(doc):
    """The r51 DRAFT's law_shape_ok, verbatim in behaviour."""
    notes = []
    silent = (doc.get('removed') or {}).get('silent') or {}
    for k in DEV:
        if (doc.get('allowed') or {}).get(k):
            notes.append('allowed[%r] not empty' % k)
        if silent.get(k):
            notes.append('silent[%r] not empty' % k)
    if (doc.get('required') or {}).get('char-device') is not False:
        notes.append("required['char-device'] is not False")
    return (not notes), notes

print('== F-A: law_shape_ok (r51 draft behaviour) on rule variants')
variants = {
    'LAW': LAW,
    'EVIL removed.kinds names device kinds':
        dict(LAW, removed=dict(LAW['removed'], kinds=['symlink','char-device','fifo','socket','block-device'])),
    "required['fifo']=True":
        dict(LAW, required=dict(LAW['required'], fifo=True)),
    "required['socket']=True":
        dict(LAW, required=dict(LAW['required'], socket=True)),
    "required['block-device']=True":
        dict(LAW, required=dict(LAW['required'], **{'block-device': True})),
    "allowed['fifo']=['unpublished-entry']":
        dict(LAW, allowed=dict(LAW['allowed'], fifo=['unpublished-entry'])),
}
for nm, d in variants.items():
    ok, notes = shape_draft(d)
    print(f'   {nm:46s} law_shape_ok={ok} {notes}')

print('\n== F-A consequence: with removed.kinds widened, does a device removal go green?')
env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/g7581/after.json'))
nonreg, _ = m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/g7581.nonregular.tsv','rb').read())
od = (env.get('parameters') or {}).get('output_directory')
root, _ = m.subject_root(env)
diags = copy.deepcopy(m.diagnostics(env))
diags.append({'input_path': '$input', 'report': {'__typename__': 'MaliciousSymlinkRemoved',
             'severity': 'WARNING', 'link': od + '/' + root + '/dev/led', 'target': '/dev/null'}})
for nm, d in (('LAW', LAW), ('EVIL', variants['EVIL removed.kinds names device kinds'])):
    mm, _ = m.gap_rule_model(json.dumps(d).encode())
    ok, why = m.disposition_check(m.gaps(env), diags, nonreg, mm, root, od)
    print(f'   {nm:8s} device removal -> ok={ok} | {why[:120]}')

print('\n== F-F: the census re-derivation reader formats disagree')
sqspec = importlib.util.spec_from_file_location('sqfsl', os.path.join(LANE, 'tools/round-41/sqfs-list.py'))
sq = importlib.util.module_from_spec(sqspec); sqspec.loader.exec_module(sq)
tree = [{'path': 'bin/ash', 'type': 'symlink', 'target': 'busybox'},
        {'path': 'dev/led', 'type': 'char-device', 'rdev': (247, 0)},
        {'path': 'run/pipe0', 'type': 'fifo'},
        {'path': 'run/sock0', 'type': 'socket'}]
work = tempfile.mkdtemp(prefix='rd-', dir=os.path.dirname(os.path.abspath(__file__)))
try:
    img = os.path.join(work, 'img.sqsh')
    with open(img, 'wb') as fh:
        fh.write(sq._build_image(tree, endian='le', comp='gzip'))
    out = os.path.join(work, 'nonregular.tsv')
    p = subprocess.run(['python3', '-I', os.path.join(LANE, 'tools/round-41/sqfs-list.py'),
                        '--layout', 'auto', '--nonregular', out, img],
                       capture_output=True, text=True)
    print('   sqfs-list.py --nonregular exit', p.returncode, p.stderr[:200])
    if os.path.exists(out):
        print('   frozen-format rows:')
        for line in open(out).read().splitlines():
            print('      ', repr(line))
    q = subprocess.run(['/usr/bin/unsquashfs', '-lln', img], capture_output=True, text=True)
    print('   unsquashfs -lln rows (the reader the R52 claims name):')
    for line in q.stdout.splitlines():
        if 'led' in line or 'pipe0' in line or 'sock0' in line:
            print('      ', repr(line))
finally:
    shutil.rmtree(work, ignore_errors=True)
print('   -> the frozen table format is rel TAB kind TAB detail ("247:0");')
print('      -lln emits a mode-char listing ("247,  0", "prw-", "srw-") with a')
print('      "squashfs-root/" prefix: no rel/kind/detail tuple to compare.')
