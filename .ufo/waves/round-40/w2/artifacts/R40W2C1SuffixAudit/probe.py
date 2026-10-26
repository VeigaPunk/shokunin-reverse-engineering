import importlib.util, json, sys
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('cc',LANE+'/tools/round-40/c1-counter.py')
cc=importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)

def T(p):
    out=[]
    for l in open(LANE+'/'+p):
        c=l.rstrip('\n').split('\t')
        if len(c)>=2 and c[0]: out.append(tuple(c[:2]))
    return out
O={c:T(f'corpus/evidence/round-40/c1/{c}/oracle.tsv') for c in ('V1','V2','L1','L2')}
N={c:T(f'corpus/evidence/round-40/c1/{c}/nonregular.tsv') for c in ('V1','V2','L1','L2')}
model=json.load(open(LANE+'/.ufo/waves/round-40/c1/gap-rule.json'))
le2=json.load(open(LANE+'/corpus/evidence/round-40/c1/L2/after.json'))['normalized_result']
pub=lambda nr:[(f['relative_path'],f.get('sha256',''),f.get('size')) for f in nr['files']]

print('== S1 same_rel FP (L2 live) ==')
print(' same_rel(firmware.bin_extract/usr/bin/busy, bin/busy) =', cc.same_rel('firmware.bin_extract/usr/bin/busy','bin/busy'))
print(' nonregular_published(L2 files, L2 nonreg) =', cc.nonregular_published(pub(le2), N['L2']))

print('== S2 oracle_hits FP: real path missing, deeper copy present ==')
files=[('firmware.bin_extract/mnt/usr/bin/busy','e28f81fc567688106f45609aff0c967cc24f707bf299fe7ab5b3c876ef148e70',40000)]
print(' hits for oracle [(usr/bin/busy,...)] =', cc.oracle_hits([('usr/bin/busy','e28f81fc567688106f45609aff0c967cc24f707bf299fe7ab5b3c876ef148e70')], files),'/1')

print('== S3 oracle_hits FP via empty digest, wrong name ==')
print(' oracle row zero(empty) hit by tmp/zero =', cc.oracle_hits([('zero','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')],[('firmware.bin_extract/tmp/zero','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',0)]))

print('== S4 gap_check: gap put on the REGULAR file satisfies the symlink requirement ==')
g=[{'kind':'depth-limited','relative_path':None},
   {'kind':'unpublished-entry','relative_path':'firmware.bin_extract/usr/bin/busy'},
   {'kind':'unpublished-entry','relative_path':'firmware.bin_extract/usr/bin/ls'}]
print(' honest-gap-set   :', cc.gap_check([g[0],{'kind':'unpublished-entry','relative_path':'firmware.bin_extract/bin/busy'},g[2]],N['L2'],model))
print(' misplaced-gap-set:', cc.gap_check(g,N['L2'],model))

print('== S5 gap ambiguity: nested non-regular rels ==')
nonreg=[('bin','dir'),('bin/busy','symlink'),('busy','symlink')]
print(' one gap on bin/busy ->', cc.gap_check([{'kind':'unpublished-entry','relative_path':'bin/busy'},{'kind':'unpublished-entry','relative_path':'busy'}],nonreg,model))

print('== S6 gap trailing slash ==')
print(' path bin/busy/ ->', cc.same_rel('bin/busy/','bin/busy'), '| gap_check:', cc.gap_check([{'kind':'unpublished-entry','relative_path':'bin/busy/'},{'kind':'unpublished-entry','relative_path':'usr/bin/ls'}],N['L2'],model))

print('== S7 rel_suffix root-only / no-root / collision / traversal ==')
for p in ['firmware.bin_extract','carrier.bin_extract','$output/a_extract/','firmware.bin_extract/usr/bin/busy','usr/bin/busy','a_extract/x','b_extract/x','$output/a_extract/../../etc/passwd','$output/firmware.bin_extract/opt/x_extract/y']:
    print('  %-45r -> %r' % (p, cc.rel_suffix(p)))
