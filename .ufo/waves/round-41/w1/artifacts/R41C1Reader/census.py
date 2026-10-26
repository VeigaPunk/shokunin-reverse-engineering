import collections, json, os
rows = [l.rstrip('\n').split('\t') for l in open('core-reader-files.tsv', encoding='utf-8', errors='surrogateescape')]
non = [l.rstrip('\n').split('\t') for l in open('core-reader-nonreg.tsv', encoding='utf-8', errors='surrogateescape')]
reg = {r[0]: int(r[2]) for r in rows}
links = {r[0]: r[2] for r in non if r[1] == 'symlink'}
dirs = [r[0] for r in non if r[1] == 'dir']
bs = 65536
out = {}
out['files'] = len(reg); out['links'] = len(links); out['dirs'] = len(dirs)
out['multi_block_gt_bs'] = sum(1 for s in reg.values() if s > bs)
out['exact_multiple_bs'] = sum(1 for s in reg.values() if s and s % bs == 0)
out['empty_files'] = sum(1 for s in reg.values() if s == 0)
out['largest'] = sorted(reg.items(), key=lambda kv: -kv[1])[:5]
out['total_bytes'] = sum(reg.values())
# fragment-eligible: size % bs != 0 and size != 0 (tail goes to a fragment)
out['with_fragment_tail'] = sum(1 for s in reg.values() if s and s % bs)
# suffix collisions: regular file whose component path ends with a symlink's path
by_comp = {}
for p in reg: by_comp.setdefault(p.split('/')[-1], []).append(p)
suffix_pairs = []
link_paths = set(links)
for lp in links:
    tail = '/' + lp
    for rp in reg:
        if rp.endswith(tail) and rp != lp:
            suffix_pairs.append((lp, rp, 'regular-ends-with-symlink'))
# symlink whose path ends with a regular file's path
rev_pairs = []
for rp in reg:
    tail = '/' + rp
    for lp in links:
        if lp.endswith(tail) and lp != rp:
            rev_pairs.append((rp, lp, 'symlink-ends-with-regular'))
out['reg_ends_with_symlink'] = {'count': len(suffix_pairs), 'sample': suffix_pairs[:10]}
out['symlink_ends_with_reg'] = {'count': len(rev_pairs), 'sample': rev_pairs[:10]}
# R40-CL1 shape: symlink 'bin/busy' and regular 'usr/bin/busy'
out['r40cl1_shape'] = [(lp, rp) for lp, rp, _ in suffix_pairs if lp.split('/')[-1].startswith('busy') or rp.endswith('/busy')][:10]
# same basename in different dirs, one symlink one regular
base_link = collections.defaultdict(list); base_reg = collections.defaultdict(list)
for p in links: base_link[p.split('/')[-1]].append(p)
for p in reg: base_reg[p.split('/')[-1]].append(p)
shared = sorted(set(base_link) & set(base_reg))
out['same_basename_link_and_reg'] = {'names': len(shared), 'sample': [(n, base_link[n][:2], base_reg[n][:2]) for n in shared[:8]]}
# busybox shape check
out['busy'] = {'link': {p: t for p, t in links.items() if p.endswith('busy')},
               'reg': [p for p in reg if p.endswith('busy')]}
# charset
out['names_with_space'] = [p for p in list(reg) + list(links) if ' ' in p][:5]
out['names_nonascii'] = [p for p in list(reg) + list(links) if any(ord(c) > 127 for c in p)][:5]
# max depth
out['max_depth'] = max(p.count('/') for p in list(reg) + list(links) + dirs)
# symlink targets: absolute count, relative count, targets with '..'
out['abs_targets'] = sum(1 for t in links.values() if t.startswith('/'))
out['dotdot_targets'] = sum(1 for t in links.values() if '..' in t)
out['distinct_targets'] = len(set(links.values()))
print(json.dumps(out, indent=1, sort_keys=True))
