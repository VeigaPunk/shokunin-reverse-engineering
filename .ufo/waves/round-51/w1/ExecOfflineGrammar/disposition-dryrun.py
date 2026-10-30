#!/usr/bin/env python3
"""Offline three-family disposition proof over committed R50 receipts."""
import csv, json, pathlib, sys
ROOT = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
IDS = ('c6430', 'c6490', 'g7581', 'g7582')

def table(cid):
    p = ROOT / f'tools/round-50/oracle/{cid}.nonregular.tsv'
    with p.open(newline='') as f:
        return [r for r in csv.reader(f, delimiter='\t') if r and not r[0].startswith('#')]

def disposition(cid, rule):
    d = json.loads((ROOT / f'corpus/evidence/round-50/c1/{cid}/after.json').read_text())
    nr = d['normalized_result']; rows = table(cid)
    entries = {r[0].removeprefix('./').lstrip('/'): (r[1], r[2] if len(r)>2 else None) for r in rows}
    root = 'firmware.bin_extract/'
    gapmap = {}
    structural = 0
    for g in nr['extraction_gaps']:
        if g['relative_path'] is None:
            if g['kind'] not in rule.get('structural', {}): return False, 'unallowed structural '+g['kind']
            structural += 1
            continue
        rel = g['relative_path'].removeprefix('$output/').removeprefix(root).removeprefix('./').lstrip('/')
        if rel not in entries: return False, 'unmatched gap '+rel
        ek = entries[rel][0]
        if g['kind'] not in rule.get('allowed', {}).get(ek, []): return False, 'disallowed gap '+rel
        gapmap.setdefault(rel, []).append(g['kind'])
    removed = set()
    for diag in nr['diagnostics']:
        report = diag.get('report') or {}
        ip = diag.get('input_path','')
        rel = ip.removeprefix('$output/').removeprefix(root).removeprefix('./').lstrip('/')
        if rel not in entries:
            link = report.get('link', '')
            rel = link.split('/firmware.bin_extract/', 1)[-1] if '/firmware.bin_extract/' in link else ''
            # Symlink diagnostics identify the link but the receipt gap carries its path.
            rel = next((p for p in entries if p == rel or p.endswith('/' + rel)), rel)
        if rel not in entries or entries[rel][0] not in rule.get('removed',{}).get('kinds',[]): return False, 'bad removal '+rel
        if gapmap.get(rel): return False, 'gap and removal '+rel
        removed.add(rel)
    missing=[]; silent=[]
    for rel,(kind,detail) in entries.items():
        if not rule.get('required',{}).get(kind, bool(rule.get('allowed',{}).get(kind))): continue
        if gapmap.get(rel) or rel in removed: continue
        if detail in (rule.get('removed',{}).get('silent',{}).get(kind) or []): silent.append(rel); continue
        missing.append(rel)
    return not missing, f'entries={len(rows)} gaps={len(nr["extraction_gaps"])} structural={structural} removals={len(removed)} silent={len(silent)} missing={len(missing)}'+(' first='+','.join(missing[:3]) if missing else '')

old=json.loads((ROOT/'tools/round-50/gap-rule.json').read_text())
new=json.loads(json.dumps(old)); new['claim']='R51-C1'; new['required']['char-device']=False; new['allowed']['char-device']=[]; new['removed']['silent'].pop('char-device',None)
print('carrier | R50 | R50 counts | R51 law | R51 counts')
matched={0:0,1:0}
for cid in IDS:
    a,ad=disposition(cid,old); b,bd=disposition(cid,new); matched[0]+=a; matched[1]+=b
    print(f'{cid} | {"PASS" if a else "FAIL"} | {ad} | {"PASS" if b else "FAIL"} | {bd}')
print(f'carriers_matched | R50 {matched[0]}/4 | R51 {matched[1]}/4')
if matched != {0:2,1:4}: sys.exit(1)
