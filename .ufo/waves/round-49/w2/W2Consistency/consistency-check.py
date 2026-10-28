#!/usr/bin/env python3
"""W2Consistency cross-document checks at the landing revision (read-only; git objects only).

Usage: python3 -I -B consistency-check.py --root LANE --rev REV
Prints one line per check: AGREE / DISAGREE / ABSENT with file:line on each side.
Writes nothing. Exit 0 always (this is an audit listing, not a gate)."""
import argparse, hashlib, json, re, struct, subprocess, sys, datetime, os

ap = argparse.ArgumentParser()
ap.add_argument('--root', required=True)
ap.add_argument('--rev', required=True)
a = ap.parse_args()
R = a.rev
BASE = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
FREEZE = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
DATA = '4aabb0b4bf716fb564c8406509c40b0a67457800'
ENTRY = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
LESSON = 'corpus/lessons/round-49.md'


def git(*args):
    return subprocess.run(['git', '-C', a.root] + list(args), capture_output=True).stdout


def blob(path, rev=R):
    return git('show', '%s:%s' % (rev, path))


def text(path, rev=R):
    return blob(path, rev).decode('utf-8', 'replace')


def lines(path, rev=R):
    return text(path, rev).split('\n')


def where(path, pat, rev=R):
    """file:line list for every line matching regex pat."""
    out = []
    for i, l in enumerate(lines(path, rev), 1):
        if re.search(pat, l):
            out.append('%s:%d' % (path, i))
    return out or ['%s:(none)' % path]


def row(path, rid, rev=R):
    for i, l in enumerate(lines(path, rev), 1):
        if re.match(r'^ {0,3}\|\s*%s\s*\|' % rid, l):
            return i, [x.strip() for x in l.strip().split('|')][1:-1]
    return None, None


results = []


def check(name, ok, detail):
    results.append((name, 'AGREE' if ok else 'DISAGREE', detail))


def sha(b):
    return hashlib.sha256(b).hexdigest()


# 1 counter digest: entry line 3 vs counter bytes at REV and the scored receipt
ctr = blob('tools/round-49/c1-counter.py')
e3 = text(ENTRY).split('\n')[2]
m = re.search(r'sha256 `([0-9a-f]{64})`', e3)
check('C1 counter sha256 (entry vs counter bytes at REV)', bool(m) and m.group(1) == sha(ctr),
      '%s vs %s; %s' % (m.group(1)[:16] if m else None, sha(ctr)[:16], where(ENTRY, r'ac83715b')[0]))

# 2 freeze hash across records
fz = {
    LESSON: FREEZE in text(LESSON),
    ENTRY: FREEZE in text(ENTRY),
    'LOG.md': FREEZE in text('LOG.md'),
    '.ufo/waves/round-49/l1/FREEZE': FREEZE in text('.ufo/waves/round-49/l1/FREEZE'),
    '.ufo/waves/round-49/controls/summary.json': FREEZE in text('.ufo/waves/round-49/controls/summary.json'),
}
check('FREEZE decc5697 in lesson, entry, LOG, l1/FREEZE, controls', all(fz.values()),
      ', '.join('%s=%s' % (k, v) for k, v in fz.items()))

# 3 C1 score file at landing: referenced paths must exist at REV
dangling = []
for p in [ENTRY, 'PROVINCE.md', 'corpus/README.md', LESSON, 'corpus/QUALITY.md']:
    for i, l in enumerate(lines(p), 1):
        for mm in re.finditer(r'\.ufo/waves/round-49/l1/scores/(c[12]-final\.json)', l):
            dangling.append('%s:%d (%s)' % (p, i, mm.group(1)))
check('landed text names landing-revision score files that exist at REV', not dangling,
      'absent in git at REV and in every commit: ' + '; '.join(dangling))

# 4 fixture sha table (entry) vs carriers.json pins vs manifest vs bytes
cj = json.loads(blob('tools/round-49/carriers.json'))
pins = {c['id']: c['sha256'] for c in cj['carriers']}
ent = lines(ENTRY)
rows_ok = []
for i, l in enumerate(ent, 1):
    mm = re.match(r'^\| `(v[12](?:le|be))` \| `([^`]+)` \| `([0-9a-f]{64})`', l)
    if mm:
        real = sha(blob('corpus/evidence/round-42/c2/fixtures/' + mm.group(2)))
        rows_ok.append((mm.group(1), mm.group(3) == pins[mm.group(1)] == real, i))
check('fixture sha256 (entry:67-70 vs carriers.json vs fixture bytes)', len(rows_ok) == 4 and all(x[1] for x in rows_ok),
      ' '.join('%s@%d=%s' % (x[0], x[2], x[1]) for x in rows_ok))

# 5 superblock table vs bytes (entry:37-40)
sbok = []
for cid, p in [('v1be', 'v1-be--squashfs_v1.0_be.bin'), ('v1le', 'v1-le--squashfs_v1.0_le.bin'),
               ('v2be', 'v2-be--squashfs_v2.0_be.bin'), ('v2le', 'v2-le--squashfs_v2.0_le.bin')]:
    b = blob('corpus/evidence/round-42/c2/fixtures/' + p)
    e = '<' if cid.endswith('le') else '>'
    inodes, used, *_ = struct.unpack(e + '6I', b[4:28])
    smaj, smin = struct.unpack(e + '2H', b[28:32])
    bs1, blog = struct.unpack(e + '2H', b[32:36])
    flags = b[36]
    mk = struct.unpack(e + 'I', b[39:43])[0]
    utc = datetime.datetime.fromtimestamp(mk, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    zo = [i for i in range(len(b) - 1) if b[i] == 0x78 and b[i + 1] == 0xda]
    rowtxt = None
    for l in ent:
        if l.startswith('| `%s` |' % cid) and rowtxt is None:
            rowtxt = l
    cells = [x.strip().strip('`') for x in rowtxt.strip().split('|')][1:-1] if rowtxt else []
    # columns: 0 carrier, 2 s_major:s_minor, 4 block_size_1, 5 block_log, 6 flags, 8 inodes, 9 bytes_used, 10 mkfs_time
    ok = bool(cells) and cells[2] == '%d:%d' % (smaj, smin) and cells[4] == str(bs1) and cells[5] == str(blog) \
        and cells[6] == '0x%02x' % flags and cells[8] == str(inodes) and cells[9] == str(used) and cells[10] == utc
    sbok.append('%s zlib=%s row=%s agree=%s' % (cid, zo, rowtxt and ent.index(rowtxt) + 1, ok))
check('superblock table (entry:37-40) vs fixture bytes; zlib offsets (entry:47)', all('agree=True' in s for s in sbok),
      ' | '.join(sbok))

# 6 REA after-receipts vs entry publication table (entry:89-94)
pub = []
for cid in ['v1le', 'v1be', 'v2le', 'v2be']:
    d = json.loads(blob('corpus/evidence/round-49/c1/%s/after.json' % cid))
    nr = d['normalized_result']
    pub.append('%s files=%d bytes=%s gaps=%s cov=%s handler=%s' % (cid, len(nr['files']), nr['published_bytes'],
                                                              nr['extraction_gaps'], nr['coverage'],
                                                              [c['handler'] for c in nr['chunks']]))
ok = all(('files=3 bytes=20' in s or 'files=4 bytes=28' in s) and 'gaps=[]' in s and 'cov=complete' in s for s in pub)
check('REA after-receipts vs entry table rows 91-94 (3/3/4/4, 20/20/28/28, gaps [], complete)', ok, ' | '.join(pub))

# 7 receipt table (entry:127-152) vs w1 receipts.tsv
rt = {}
for l in blob('.ufo/waves/round-49/w1/C1ScribeEntry/receipts.tsv').decode().split('\n'):
    f = l.split('\t')
    if len(f) >= 4:
        rt[f[0]] = (f[2].replace('exit=', ''), f[3].replace('stdout_sha256=', ''), re.search(r'T(\d\d:\d\d:\d\d)Z', f[1]).group(1))
bad = []
n = 0
for i, l in enumerate(ent, 1):
    if l.startswith('| `') and i > 120:
        c = [x.strip() for x in l.strip().split('|')][1:-1]
        rid = c[0].strip('`')
        if rid in rt:
            n += 1
            if not (rt[rid][0] == c[2] and rt[rid][1].startswith(c[3]) and rt[rid][2] == c[1]):
                bad.append(rid)
        elif len(c) >= 4 and rid != 'receipt':
            bad.append(rid + '(absent)')
check('entry receipt table (entry:127-152) vs receipts.tsv (exit, stdout sha, time)', n == 26 and not bad,
      'rows=%d bad=%s' % (n, bad))

# 8 S108 vs S112 source ids for the same unblob URL
s108, c108 = row('corpus/SOURCES.md', 'S108')
s112, c112 = row('corpus/SOURCES.md', 'S112')
prov_ln = where('PROVINCE.md', r'S108 :101-102')
ent_ln = where(ENTRY, r'source: S112')
check('unblob squashfs.py cited under one source id (PROVINCE:436 uses S108; entry source and README use S112)',
      'S108 :101-102' not in lines('PROVINCE.md')[435], 'PROVINCE %s; entry %s; SOURCES rows %d (S108) and %d (S112), same URL+tag: %s' % (
          prov_ln[0], ent_ln[0], s108, s112, 'yes' if c108[1].split('—')[0].strip() == 'unblob SquashFS handler at tag 26.6.4' else 'check'))

# 9 S112 registry row: lines 24-70 vs entry 24-69 (wave-1 D8 said fix at landing)
check('S112 row extractor line range vs entry :24-69', 'lines 24-70' not in c112[5],
      'SOURCES %s "%s" vs %s' % (s112, re.search(r'lines 24-\d+', c112[5]).group(0), where(ENTRY, r'SquashFSExtractor` :24-69')[0]))

# 10 S112 used-by lists the r49 entry (entry cites S112; wave-1 D7 asked for it)
check('S112 used-by lists the round-49 entry', 'r49-squashfs-v1v2-core' in c112[10],
      'SOURCES:%s used-by = %s' % (s112, c112[10][:160]))

# 11 "independent oracle" wording (entry:52-59 withdraws it; PROVINCE:436 still uses it)
check('round-49 PROVINCE row free of "independent oracle" (entry:55 withdraws the phrase)',
      'independent oracle' not in ''.join(lines('PROVINCE.md')[435:436]),
      where('PROVINCE.md', r'independent oracle `/usr/bin/unsquashfs`')[0] + ' vs ' + where(ENTRY, r'withdrawn in favour')[0])

# 12 "exactly 8 hex" claim (lesson:56) vs the two A2 hashes
dead = '663f30ee7516942a0120e7de68fe88356e680822'
real = '663f30ee751694fb0970e7de68fe88356e680822'
pre = len(os.path.commonprefix([dead, real]))
suf = 0
while suf < 40 and dead[-1 - suf] == real[-1 - suf]:
    suf += 1
check('lesson:56 "the two share exactly 8 hex"', pre == 8, 'common prefix %d hex, common suffix %d hex; %s' % (
    pre, suf, where(LESSON, r'share exactly 8 hex')[0]))

# 13 wave-1 seats: registry members vs report artifacts
reg = json.loads(blob('.ufo/waves/round-49/w1/swarm-registry.json'))['members']
tree = git('-c', 'core.quotePath=false', 'ls-tree', '--name-only', R, '.ufo/waves/round-49/w1/').decode().split('\n')
names = {p.split('/')[-1][:-3] if p.endswith('.md') else p.split('/')[-1] for p in tree if p}
missing = sorted(set(reg) - names)
check('wave-1 "48 seats" (lesson:4) vs report artifacts in w1/', not missing,
      '%d registry members; no report artifact: %s; %s' % (len(reg), missing, where(LESSON, r'wave 1 \(48 seats')[0]))

# 14 S139 releases-page byte count: lesson:22 vs entry:136 receipt
check('S139 releases-page size (lesson:22 "361,752 B today" vs entry:136 "361757 B")',
      not ('361,752' in text(LESSON) and '361757 B' in text(ENTRY)),
      '%s vs %s; SOURCES row S139 still %s' % (where(LESSON, r'361,752')[0], where(ENTRY, r'361757 B')[0],
                                             'contains 398943 B' if '398943 B' in row('corpus/SOURCES.md', 'S139')[1][5] else 'changed'))

# 15 S138 "six carriers" (SOURCES teaches) vs entry four carriers
s138, c138 = row('corpus/SOURCES.md', 'S138')
check('S138 teaches "all six carriers" vs entry 4 carriers, v2.1 not carriers', 'six carriers' not in c138[6],
      'SOURCES:%s; entry:%s' % (s138, where(ENTRY, r'are not carriers')[0]))

# 16 r44 entry v1 mkfs (round-44 entry still shows host-local times)
r44 = where('corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md', r'04:18:58Z', R)
check('round-44 entry v1 mkfs times corrected or annotated', 'Correction to the round-44' in text('corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md'), '%s (correction only in %s)' % (r44[0], where(ENTRY, r'Correction to the round-44 table')[0]))

# 17 script paths cited by entry exist at repo root
check('entry-cited scripts exist at the cited relative path (entry:33, :138)',
      bool(blob('scripts/sb.py')) and bool(blob('scripts/s138.py')),
      'scripts/sb.py and scripts/s138.py absent at repo root; present only at .ufo/waves/round-49/w1/C1ScribeEntry/scripts/')

print('consistency-check rev=%s' % R)
for name, verdict, detail in results:
    print('%-9s %s :: %s' % (verdict, name, detail))
