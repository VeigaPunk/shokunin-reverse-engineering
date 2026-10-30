#!/usr/bin/env python3
"""Round-52 theme scan over the shokuknow merge package (read-only)."""
import hashlib, json, os, re, subprocess, sys, time

PKG = '/home/vgpnk/Projects/shokuknow/merge/kaidoku'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
OUT = os.path.dirname(os.path.abspath(__file__))

# round-52 theme vocabulary (from plans/round-52-claims.md: C1 device-accounting law
# over LE AVM carriers; C2 triage v6 over ddwrt FAILED no-pad body)
THEME = re.compile(r'squashfs|avm|fritz|firmware|unsquashfs|sasquatch|unblob|'
                    r'device node|mknod|padding|nopad|no-pad|ddwrt|extractor', re.I)

def sha256(p):
    h = hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda: f.read(1<<16), b''):
            h.update(b)
    return h.hexdigest()

def rows(path):
    out = {}
    for line in open(path, encoding='utf-8'):
        if not line.startswith('|'): continue
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if len(c) < 3 or not re.fullmatch(r'S\d+', c[0]): continue
        out[c[0]] = c
    return out

pkg_rows = rows(f'{PKG}/SOURCES.append.md')
lane_rows = rows(f'{LANE}/corpus/SOURCES.md')

# 1. knowledge entries in the package, with theme hit
kdir = f'{PKG}/knowledge/corpus/knowledge'
entries = sorted(f for f in os.listdir(kdir) if f.endswith('.md'))
theme_hits = []
for e in entries:
    txt = open(f'{kdir}/{e}', encoding='utf-8').read()
    if THEME.search(txt):
        theme_hits.append((e, len(THEME.findall(txt)), sha256(f'{kdir}/{e}')))

# 2. which package rows are cited by which package knowledge entry (used-by col)
used_by = {}
for rid, c in pkg_rows.items():
    if len(c) >= 12:
        used_by.setdefault(c[11], []).append(rid)

# 3. lane held ground: which package documents already have a lane row (by URL tail)
lane_doc = {}
for rid, c in lane_rows.items():
    url = c[1]
    m = re.search(r'(https?://\S+?)(?:\s+—|\s+-\s|,\s|$)', url)
    u = m.group(1) if m else url
    lane_doc.setdefault(u.rstrip('/'), []).append(rid)

def doc_key(url):
    u = url.strip()
    u = re.sub(r'^`', '', u).rstrip('`')
    return u.rstrip('/')

pkg_doc_lane = {}
for rid, c in pkg_rows.items():
    key = doc_key(c[1].split(' — ')[-1] if ' — ' in c[1] else c[1])
    pkg_doc_lane[rid] = lane_doc.get(key, [])

# 4. id space
pkg_ids = sorted(pkg_rows, key=lambda s: int(s[1:]))
lane_ids = sorted(lane_rows, key=lambda s: int(s[1:]))
lane_nums = sorted(int(i[1:]) for i in lane_ids)
collisions = [i for i in pkg_ids if i in lane_rows]
next_free = max(lane_nums) + 1

report = {
 'scanned_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
 'package': PKG,
 'package_knowledge_entries_total': len(entries),
 'package_theme_hits': [{'entry': e, 'theme_mentions': n, 'sha256': s} for e,n,s in theme_hits],
 'package_rows': len(pkg_rows),
 'package_row_id_range': f"{pkg_ids[0]}..{pkg_ids[-1]}",
 'lane_rows': len(lane_rows),
 'lane_max_id': f'S{max(lane_nums)}',
 'lane_next_free_id': f'S{next_free}',
 'numeric_collisions': len(collisions),
 'numeric_collision_range': f"{collisions[0]}..{collisions[-1]}" if collisions else None,
 'rows_already_held_by_document': {k: v for k, v in pkg_doc_lane.items() if v},
 'used_by_map': used_by,
}
json.dump(report, open(f'{OUT}/scan.json','w'), indent=1)
print(json.dumps({k: report[k] for k in
      ['scanned_at_utc','package_knowledge_entries_total','package_rows','package_row_id_range',
       'lane_rows','lane_max_id','lane_next_free_id','numeric_collisions','numeric_collision_range']}, indent=1))
print('\ntheme hits:', len(theme_hits))
for e,n,s in theme_hits: print('  ', e, n, s[:12])
print('\ndocument already held by a lane row (package id -> lane ids):')
for k,v in sorted(pkg_doc_lane.items()):
    if v: print('  ', k, '->', v)
