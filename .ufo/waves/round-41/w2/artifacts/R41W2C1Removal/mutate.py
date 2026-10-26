import json, sys, hashlib, copy

LANE = sys.argv[1]
CAR = sys.argv[2]   # V4 | L3
ATTACK = sys.argv[3]  # a b c d e f g h
OUT = sys.argv[4]

AFTER = f"{LANE}/corpus/evidence/round-41/c1/{CAR}/after.json"
NONREG = f"{LANE}/corpus/evidence/round-41/c1/{CAR}/nonregular.tsv"
ORACLE = f"{LANE}/corpus/evidence/round-41/c1/{CAR}/oracle.tsv"

env = json.load(open(AFTER))
nr = env['normalized_result']

# relative path prefix used inside receipts (root-mapped)
PREFIX = 'firmware.bin_extract/'
# absolute link prefix: derive from first existing removal diagnostic link
def link_prefix():
    for d in nr.get('diagnostics') or []:
        rep = d.get('report') or {}
        lk = rep.get('link')
        if isinstance(lk, str) and PREFIX in lk:
            return lk.split(PREFIX)[0] + PREFIX
    return '/run/REA/extracted/' + PREFIX

LP = link_prefix()

def rel_of(link):
    return link.split(PREFIX, 1)[1]

def mk_removal(rel, target='../x'):
    return {"input_path": "$input", "report": {
        "__typename__": "MaliciousSymlinkRemoved", "severity": "WARNING",
        "link": LP + rel, "target": target}}

diags = nr.get('diagnostics') or []
gaps = nr.get('extraction_gaps') or []
unpub = nr.get('unpublished_entries') or []

# nonregular rows: rel -> kind
nonreg = {}
for line in open(NONREG):
    line = line.rstrip('\n')
    if not line.strip():
        continue
    parts = line.split('\t')
    rel = parts[0]
    kind = parts[1] if len(parts) > 1 else ''
    nonreg[rel] = kind

def symlink_gap_rels():
    out = []
    for g in gaps:
        if g.get('kind') == 'unpublished-entry' and isinstance(g.get('relative_path'), str):
            rel = g['relative_path']
            if rel.startswith(PREFIX):
                rel = rel[len(PREFIX):]
            if nonreg.get(rel) == 'symlink':
                out.append(rel)
    return out

def find_regular_rel():
    for line in open(ORACLE):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        rel = line.split('\t')[0]
        if not rel.startswith('./'):
            rel = './' + rel
        rel = rel.lstrip('./')
        if rel not in nonreg:
            return rel
    return None

def find_dir_rel():
    for rel, kind in nonreg.items():
        if kind == 'dir':
            return rel
    return None

def rm_gap(rel):
    p = PREFIX + rel
    gaps[:] = [g for g in gaps if not (g.get('kind') == 'unpublished-entry' and g.get('relative_path') == p)]
    unpub[:] = [u for u in unpub if not (u.get('kind') == 'symlink' and u.get('relative_path') == p)]

gl = symlink_gap_rels()
print(CAR, ATTACK, 'gapped symlinks', len(gl), 'first', gl[:6], file=sys.stderr)
print('nonreg kinds', {k for k in nonreg.values()}, file=sys.stderr)

base_diags = [d for d in diags if (d.get('report') or {}).get('__typename__') == 'MaliciousSymlinkRemoved']
print('base removals', len(base_diags), [rel_of((d.get('report') or {}).get('link')) for d in base_diags], file=sys.stderr)

if ATTACK == 'a':
    tgt = gl[0]
    diags.append(mk_removal(tgt, target='../x'))
elif ATTACK == 'b':
    tgt = find_regular_rel()
    diags.append(mk_removal(tgt, target='../x'))
elif ATTACK == 'c':
    tgt = find_dir_rel()
    diags.append(mk_removal(tgt, target='../x'))
elif ATTACK == 'd':
    # drop the last removal diagnostic
    assert base_diags, 'no removals to drop'
    last_link = (base_diags[-1].get('report') or {}).get('link')
    diags[:] = [d for d in diags if (d.get('report') or {}).get('link') != last_link]
elif ATTACK == 'e':
    diags.append(mk_removal('nonexistent/deep/path', target='../x'))
elif ATTACK == 'f':
    # swap the 4 removals onto 4 currently-gapped symlinks, keeping the count:
    # new targets lose their gaps and gain removals; old targets gain gaps.
    assert len(base_diags) == 4, len(base_diags)
    old_tgts = [rel_of((d.get('report') or {}).get('link')) for d in base_diags]
    new_tgts = gl[:4]
    for rel in new_tgts:
        rm_gap(rel)
    for d, rel in zip(base_diags, new_tgts):
        d['report']['link'] = LP + rel
        d['report']['target'] = '../x'
    for rel in old_tgts:
        gaps.append({'kind': 'unpublished-entry', 'input_path': '$output/' + PREFIX + rel,
                     'relative_path': PREFIX + rel, 'handler': None, 'provider_id': None,
                     'range': None, 'root_file_range': None, 'dependencies': [],
                     'continuation_id': 'fx'})
        unpub.append({'relative_path': PREFIX + rel, 'kind': 'symlink',
                      'link_target': '../x'})
elif ATTACK == 'g':
    # rename the removal diagnostic typename (no longer a removal)
    d0 = base_diags[0]
    d0['report']['__typename__'] = 'NotARemoval'
elif ATTACK == 'h':
    # duplicate one removal diagnostic (two entries, same target)
    d0 = copy.deepcopy(base_diags[0])
    diags.append(d0)
else:
    sys.exit('unknown attack')

env['normalized_result']['diagnostics'] = diags
env['normalized_result']['extraction_gaps'] = gaps
env['normalized_result']['unpublished_entries'] = unpub

with open(OUT, 'w') as fh:
    json.dump(env, fh)
print('wrote', OUT, hashlib.sha256(open(OUT,'rb').read()).hexdigest())
