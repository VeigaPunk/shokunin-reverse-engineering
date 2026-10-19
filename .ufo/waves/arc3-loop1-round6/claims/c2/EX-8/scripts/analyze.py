#!/usr/bin/env python3
"""EX-8 independent Vyper dispatcher-form analyzer (arc3-loop1-round6, c2)."""
import json, sys, hashlib
sys.path.insert(0,'/var/tmp/ex08-r6')
from walker import dis

forms = ['default','Ocodesize','Onone','nooptimize','paris-default','paris-codesize']
probe = {f: json.load(open(f'probe/{f}-hex-6.4.0.json')) for f in forms}

def chain_legs(code, form):
    d = dis(code); by = {o[0]:o for o in d}
    legs = []
    for pc, nm, imm, nx in d:
        if nm != 'PUSH4': continue
        j = pc+5
        tail = []
        ok = True
        # allow DUPn then XOR, or DUPn EQ ISZERO
        if j in by and by[j][1].startswith('DUP'):
            tail.append(by[j][1]); j += 1
        else: ok = False
        if ok and j in by and by[j][1] in ('XOR','EQ'):
            tail.append(by[j][1]); j += 1
        else: ok = False
        if ok and tail[-1] == 'EQ':
            if j in by and by[j][1]=='ISZERO':
                tail.append('ISZERO'); j += 1
            else: ok = False
        if ok and j in by and by[j][1]=='PUSH2':
            tail.append('PUSH2'); dst=int(by[j][2],16); j += 3
            if j in by and by[j][1]=='JUMPI':
                tail.append('JUMPI')
                legs.append(dict(sel=imm, site=pc, next=j+1,
                                 pattern=';'.join(tail), dst=dst))
    return legs, d, by

out = {}
for f in forms:
    code = open(f'out/{f}/runtime.bin','rb').read()
    legs, d, by = chain_legs(code, f)
    nr = probe[f]['normalized_result']; fns = {x['selector'][2:]: x for x in nr['functions']}
    row = dict(form=f, runtime_len=len(code), sha256=hashlib.sha256(code).hexdigest(),
               head=code[:88].hex(), probe_id=probe[f]['evidence_id'], n_fns=len(fns),
               kind=None, legs=legs, reported={s: x['bytecode_offset'] for s,x in fns.items()})
    if legs and legs[0]['pattern'].startswith('DUP2;XOR'):
        row['kind']='xor_chain_mod_table'
        # table: PUSH1 2 PUSH1 n DUP3 MOD PUSH1 1 SHL PUSH2 base ADD PUSH1 0x1e CODECOPY PUSH0 MLOAD JUMP
        i = code.find(bytes.fromhex('600260'))
        n_buckets = code[i+3]; base = int.from_bytes(code[i+10:i+12],'big')
        table = [int.from_bytes(code[base+2*i:base+2*i+2],'big') for i in range(n_buckets)]
        row.update(n_buckets=n_buckets, table_base=base,
                   table_entries=table,
                   table_all_jumpdest=all(code[t]==0x5b for t in table),
                   table_unique=len(set(table)))
        delta = {s: row['reported'][s]-next(l['site'] for l in legs if l['sel']==s) for s in row['reported'] if any(l['sel']==s for l in legs)}
        row['offset_minus_site']=delta
        row['offset_rule']='site+11' if set(delta.values())=={11} else 'MIXED'
        row['order']='desc' if [l['sel'] for l in legs]==sorted([l['sel'] for l in legs], reverse=True) else ('asc' if [l['sel'] for l in legs]==sorted([l['sel'] for l in legs]) else 'unsorted')
    elif legs and legs[0]['pattern'].startswith('DUP2;EQ;ISZERO'):
        row['kind']='linear_eq_iszero'
        delta = {s: row['reported'][s]-next(l['site'] for l in legs if l['sel']==s) for s in row['reported'] if any(l['sel']==s for l in legs)}
        row['offset_minus_site']=delta
        row['offset_rule']='site+12' if set(delta.values())=={12} else 'MIXED'
        row['order']='desc' if [l['sel'] for l in legs]==sorted([l['sel'] for l in legs], reverse=True) else ('asc' if [l['sel'] for l in legs]==sorted([l['sel'] for l in legs]) else 'unsorted')
    else:
        row['kind']='bit_trie_lookup'
        row['distinct_reported_offsets']=sorted(set(row['reported'].values()))
        row['offset_rule']='shared-entry: every selector reports pc %s' % sorted(set(row['reported'].values()))
    out[f]=row
    print('==',f,row['kind'],row['runtime_len'],'B',row['sha256'][:16],'fns',row['n_fns'])
    print('   legs',len(legs),'order',row.get('order'),'rule',row.get('offset_rule'), 'deltas', sorted(set(row.get('offset_minus_site',{}).values())))
    if row['kind']=='xor_chain_mod_table':
        print('   n_buckets',row['n_buckets'],'base',hex(row['table_base']),'all_jd',row['table_all_jumpdest'],'unique',row['table_unique'])
        print('   table',[hex(t) for t in row['table_entries']])
    if row['kind']=='bit_trie_lookup':
        print('   reported offsets',row['distinct_reported_offsets'])
json.dump(out,open('vy-forms.json','w'),indent=1)
