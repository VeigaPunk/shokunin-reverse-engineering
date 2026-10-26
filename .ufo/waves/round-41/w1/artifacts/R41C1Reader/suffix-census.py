import collections, json
rows = [l.rstrip('\n').split('\t') for l in open('core-reader-files.tsv', encoding='utf-8', errors='surrogateescape')]
non  = [l.rstrip('\n').split('\t') for l in open('core-reader-nonreg.tsv', encoding='utf-8', errors='surrogateescape')]
reg = [r[0] for r in rows]
link = [r[0] for r in non if r[1] == 'symlink']
def tail(p, k): return '/'.join(p.split('/')[-k:])
out = {}
for k in (1, 2, 3, 4):
    idx = collections.defaultdict(list)
    for lp in link: idx[tail(lp, k)].append(lp)
    pairs = [(lp, rp) for rp in reg for lp in idx.get(tail(rp, k), ()) if lp != rp]
    out['k%d' % k] = {'distinct_tails': len(idx), 'colliding_pairs': len(pairs),
                      'sample': pairs[:6]}
# also: is any regular file's *whole* path a component suffix of a symlink path /v.v.
full = []
for lp in link:
    for rp in reg:
        if lp.endswith('/' + rp) or rp.endswith('/' + lp):
            full.append((rp, lp))
out['full_path_component_suffix_pairs'] = {'count': len(full), 'sample': full[:6]}
print(json.dumps(out, indent=1, sort_keys=True))
