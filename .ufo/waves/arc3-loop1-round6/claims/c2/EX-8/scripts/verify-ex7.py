import json, hashlib, glob, os
from walker import dis

EX7 = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round6/claims/c2/EX-7'
MY = '/var/tmp/ex08-r6'
probe_of = {
 'viair-opt200': f'{MY}/probe/viair-opt200.hex-hex-6.4.0.json',
 'viair-noopt':  f'{MY}/probe/viair-noopt.hex-hex-6.4.0.json',
 'std-opt200':   f'{MY}/probe/std-opt200.hex-hex-6.4.0.json',
}
report = {}
for tag, pj in probe_of.items():
    code = open(f'{EX7}/out/{tag}/runtime.bin','rb').read()
    d = dis(code); by = {o[0]:o for o in d}
    jd = {pc for pc,b in enumerate(code) if b == 0x5b}
    push2_targets = {int(o[2],16) for o in d if o[1]=='PUSH2'}
    probe = json.load(open(pj)); nr = probe['normalized_result']
    fns = {f['selector'][2:]: f for f in nr['functions']}
    eq = {}
    for pc,imm in [(o[0],o[2]) for o in d if o[1]=='PUSH4']:
        j = pc+5
        if j in by and by[j][1] in ('DUP1','DUP2','DUP3'): j += 1
        if j in by and by[j][1]=='EQ' and (j+1) in by and by[j+1][1]=='PUSH2' and (j+4) in by and by[j+4][1]=='JUMPI':
            eq[imm] = dict(site=pc, dst=int(by[j+1][2],16))
    gt = {}
    for pc,imm in [(o[0],o[2]) for o in d if o[1]=='PUSH4']:
        j = pc+5
        if j in by and by[j][1] in ('DUP1','DUP2','DUP3'): j += 1
        if j in by and by[j][1]=='GT' and (j+1) in by and by[j+1][1]=='PUSH2' and (j+4) in by and by[j+4][1]=='JUMPI':
            gt.setdefault(imm, []).append(dict(site=pc, dst=int(by[j+1][2],16)))
    sub = []
    for pc,imm in [(o[0],o[2]) for o in d if o[1]=='PUSH4']:
        j = pc+5
        if j in by and by[j][1]=='SUB' and (j+1) in by and by[j+1][1]=='PUSH2' and (j+4) in by and by[j+4][1]=='JUMPI':
            sub.append(dict(site=pc, imm=imm, dst=int(by[j+1][2],16), jumpi=j+4, fallthrough=j+5))
    rows = []
    for sel, f in sorted(fns.items()):
        off = f['bytecode_offset']
        e = eq.get(sel)
        rows.append(dict(selector=sel, offset=off, is_jumpdest=off in jd, is_push2_target=off in push2_targets,
                         eq_site=(e['site'] if e else None), eq_dst=(e['dst'] if e else None),
                         offset_minus_eq_dst=(off-e['dst'] if e else None),
                         off_minus_sub_site=(off-sub[0]['site'] if (not e and sub) else None),
                         off_minus_sub_fallthrough=(off-sub[0]['fallthrough'] if (not e and sub) else None),
                         byte_at_offset=code[off:off+1].hex() if off < len(code) else None,
                         inferred=f['inferred_state_mutability']))
    abi = json.load(open(f'{EX7}/out/{tag}/abi.json'))
    abi_mut = {a['name']: a['stateMutability'] for a in abi if a['type']=='function'}
    mi = json.load(open(f'{EX7}/out/{tag}/method-identifiers.json'))
    sig_of = {v[2:]: k for k,v in mi.items()}
    delta = [dict(selector=r['selector'], sig=sig_of.get(r['selector']), inferred=r['inferred'], abi=abi_mut.get(sig_of.get(r['selector'],'').split('(')[0]))
             for r in rows if r['inferred'] != abi_mut.get(sig_of.get(r['selector'],'').split('(')[0])]
    report[tag] = dict(runtime_len=len(code), sha256=hashlib.sha256(code).hexdigest(),
        head=code[:48].hex(), eq_count=len(eq), gt_count=sum(len(v) for v in gt.values()),
        gt_sites=gt, sub=sub, rows=rows, abi_entries=len(abi_mut),
        probe_evidence_id=probe['evidence_id'], probe_fns=len(fns),
        mutability_delta=delta)
json.dump(report, open(f'{MY}/verify-ex7.json','w'), indent=1)

for tag,r in report.items():
    print('==',tag, r['runtime_len'], r['sha256'][:16], 'eq:',r['eq_count'],'gt:',r['gt_count'],'sub:',[(s['imm'],s['site'],s['dst'],s['fallthrough']) for s in r['sub']])
    print('  probe id',r['probe_evidence_id'][:20],'fns',r['probe_fns'],'abi',r['abi_entries'])
    print('  rows: offset==eq_dst count', sum(1 for x in r['rows'] if x['eq_dst'] is not None and x['offset_minus_eq_dst']==0), '| jumpdest', sum(x['is_jumpdest'] for x in r['rows']), '| push2tgt', sum(x['is_push2_target'] for x in r['rows']))
    for x in r['rows']:
        if x['eq_dst'] is None or x['offset_minus_eq_dst'] != 0:
            print('   NON-EQ row:', x)
    print('  mutability delta:', r['mutability_delta'])
