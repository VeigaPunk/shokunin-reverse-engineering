#!/usr/bin/env python3
"""oracle-build.py -- DRAFT (round-50 wave 1, seat C1OracleBuild).

Independent multi-reader oracle for one carrier (a SquashFS member).  Runs
unsquashfs (extract + -lls), the lane's pure-Python tools/round-41/sqfs-list.py
(layout auto and le) and 7z (list + extract), then compares every reader on
regular-file relpath/size/sha256 and on non-regular entries.

usage: oracle-build.py ID MEMBER WORK OUTDIR [--lane-sqfs PATH]

  ID      carrier id (a7530 ...)
  MEMBER  the SquashFS member bytes (hsqs ...)
  WORK    scratch dir (extract trees are written under WORK/ex-*/<ID>)
  OUTDIR  receipts: oracle.tsv, nonregular.tsv, oracle-summary.json,
          disagreements.json, times.json

Exit codes: 0 all readers agree, 1 at least one disagreement, 2 could not evaluate.
Vendor bytes are never written under OUTDIR; only hashes / listings.
"""
import hashlib, json, os, re, shutil, stat, subprocess, sys, time

SQFS = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/sqfs-list.py'
LLS = re.compile(r'^([-dlcbps])(\S{9}) (\S+)\s+(.*?) (\d{4}-\d\d-\d\d \d\d:\d\d) (squashfs-root(?:/.*)?)$')


def b(s):
    return s.encode('utf-8', 'surrogateescape')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def timed(name, argv, times, out=None):
    t0 = time.monotonic()
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t = {'argv': argv, 'exit': p.returncode, 'wall_s': round(time.monotonic() - t0, 3),
         'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
         'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
         'stderr_tail': p.stderr.decode('utf-8', 'replace').strip().splitlines()[-3:]}
    times[name] = t
    return p


def parse_lls(text):
    """unsquashfs -lls -> {rel: (kind, size, detail)}; root skipped."""
    ents, bad = {}, []
    for line in text.split('\n'):
        if not line:
            continue
        m = LLS.match(line)
        if not m:
            bad.append(line)
            continue
        k, _, _own, sz, _date, path = m.groups()
        rel = path[len('squashfs-root'):].lstrip('/')
        if not rel:
            continue
        if k == 'l':
            name, _, tgt = rel.partition(' -> ')
            ents[name] = ('symlink', None, tgt)
        elif k == '-':
            ents[rel] = ('file', int(sz), '')
        elif k == 'd':
            ents[rel] = ('dir', None, '')
        elif k in 'cb':
            mj, mn = [x.strip() for x in sz.replace(',', ' ').split()][:2]
            ents[rel] = ('char-device' if k == 'c' else 'block-device', None, '%s:%s' % (mj, mn))
        else:
            ents[rel] = ({'p': 'fifo', 's': 'socket'}[k], None, '')
    return ents, bad


def walk_tree(root):
    """lstat walk -> {rel: (kind, size, detail, sha)}; errors list."""
    ents, errs = {}, []
    rb = b(root)
    for dp, dns, fns in os.walk(rb):
        for n in dns + fns:
            full = os.path.join(dp, n)
            rel = os.fsdecode(os.path.relpath(full, rb)) if False else os.path.relpath(full, rb).decode('utf-8', 'surrogateescape')
            st = os.lstat(full)
            m = st.st_mode
            if stat.S_ISLNK(m):
                ents[rel] = ('symlink', None, os.readlink(full).decode('utf-8', 'surrogateescape'), None)
            elif stat.S_ISDIR(m):
                ents[rel] = ('dir', None, '', None)
            elif stat.S_ISREG(m):
                try:
                    ents[rel] = ('file', st.st_size, '', sha(full))
                except OSError as e:
                    errs.append((rel, str(e)))
                    ents[rel] = ('file', st.st_size, '', None)
            elif stat.S_ISCHR(m) or stat.S_ISBLK(m):
                ents[rel] = ('char-device' if stat.S_ISCHR(m) else 'block-device', None, '%d:%d' % (os.major(st.st_rdev), os.minor(st.st_rdev)), None)
            else:
                ents[rel] = ('other', None, '', None)
    return ents, errs


def read_tsv(path):
    out = {}
    with open(path, encoding='utf-8', errors='surrogateescape') as f:
        for line in f:
            line = line.rstrip('\n')
            if line:
                out[line.split('\t')[0]] = line.split('\t')[1:]
    return out


def parse_7z(text):
    ents = {}
    for blk in text.split('\n\n'):
        d = {}
        for ln in blk.split('\n'):
            if ' = ' in ln:
                k, v = ln.split(' = ', 1)
                d[k] = v
        if 'Path' in d and 'Folder' in d:
            mode = d.get('Mode', '')
            k = mode[:1]
            kind = {'l': 'symlink', 'd': 'dir', '-': 'file', 'c': 'char-device', 'b': 'block-device', 'p': 'fifo', 's': 'socket'}.get(k, 'dir' if d['Folder'] == '+' else 'file')
            ents[d['Path']] = (kind, int(d['Size']) if d.get('Size', '').isdigit() else None, '')
    return ents


def bsort(rows):
    return sorted(rows, key=lambda r: b(r[0]))


def main():
    a = sys.argv[1:]
    if len(a) < 4:
        print(__doc__)
        return 2
    cid, member, work, outdir = a[:4]
    sqfs = SQFS
    if '--lane-sqfs' in a:
        sqfs = a[a.index('--lane-sqfs') + 1]
    os.makedirs(outdir, exist_ok=True)
    times, dis = {}, {}
    exu, ex7 = os.path.join(work, 'ex-unsq', cid), os.path.join(work, 'ex-7z', cid)
    for d in (exu, ex7):
        shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.dirname(exu), exist_ok=True)
    os.makedirs(os.path.dirname(ex7), exist_ok=True)

    member_sha = sha(member)
    p = timed('unsquashfs-extract', ['unsquashfs', '-d', exu, '-f', member], times)
    p = timed('unsquashfs-lls', ['unsquashfs', '-lls', member], times)
    lls_text = p.stdout.decode('utf-8', 'surrogateescape')
    lls, lls_bad = parse_lls(lls_text)
    sq = {}
    for lay in ('auto', 'le'):
        f, n = os.path.join(work, 'py-%s-%s.files.tsv' % (cid, lay)), os.path.join(work, 'py-%s-%s.nonreg.tsv' % (cid, lay))
        timed('sqfs-list-' + lay, [sys.executable, '-I', sqfs, '--layout', lay, '--files', f, '--nonregular', n, member], times)
        sq[lay] = (read_tsv(f), read_tsv(n))
    p = timed('7z-list', ['7z', 'l', '-slt', member], times)
    z_list = parse_7z(p.stdout.decode('utf-8', 'surrogateescape'))
    p = timed('7z-extract', ['7z', 'x', '-snl', '-y', '-o' + ex7, member], times)
    t0 = time.monotonic()
    tree_u, errs_u = walk_tree(exu)
    times['hash-unsq-tree'] = {'wall_s': round(time.monotonic() - t0, 3)}
    t0 = time.monotonic()
    tree_7, errs_7 = walk_tree(ex7) if os.path.isdir(ex7) else ({}, [])
    times['hash-7z-tree'] = {'wall_s': round(time.monotonic() - t0, 3)}

    # 7z rewrites absolute link targets under its output dir and refuses some links
    # ("Dangerous link ... was ignored", exit 2), leaving a 0-byte regular file in their place.
    # These are 7z extract artefacts, recorded as reader notes, not oracle disagreements.
    pre = ex7.rstrip('/')
    for r, v in list(tree_7.items()):
        if v[0] == 'symlink' and v[2].startswith(pre + '/'):
            tree_7[r] = (v[0], v[1], v[2][len(pre):], v[3])
    lls_syms = {r for r, v in lls.items() if v[0] == 'symlink'}
    demoted = sorted(r for r, v in tree_7.items() if v[0] == 'file' and r in lls_syms and v[1] == 0)
    for r in demoted:
        del tree_7[r]
    notes = {'7z_demoted_symlinks_to_empty_files': len(demoted), '7z_demoted_examples': demoted[:5],
             '7z_extract_exit': times['7z-extract']['exit'], '7z_extract_stderr_tail': times['7z-extract']['stderr_tail']}

    # ---- primary oracle = hashes of the unsquashfs-extracted tree
    files_u = {r: (v[3], v[1]) for r, v in tree_u.items() if v[0] == 'file'}
    files_7 = {r: (v[3], v[1]) for r, v in tree_7.items() if v[0] == 'file'}
    files_py = {r: (v[0], int(v[1])) for r, v in sq['auto'][0].items()}
    files_pyle = {r: (v[0], int(v[1])) for r, v in sq['le'][0].items()}
    files_lls = {r: (None, v[1]) for r, v in lls.items() if v[0] == 'file'}
    files_z = {r: (None, v[1]) for r, v in z_list.items() if v[0] == 'file'}

    def cmp_files(nm, ref, oth, use_sha):
        d = {'only_ref': sorted(set(ref) - set(oth)), 'only_other': sorted(set(oth) - set(ref)), 'size_mismatch': [], 'sha_mismatch': []}
        for r in set(ref) & set(oth):
            if ref[r][1] != oth[r][1]:
                d['size_mismatch'].append([r, ref[r][1], oth[r][1]])
            if use_sha and ref[r][0] != oth[r][0]:
                d['sha_mismatch'].append([r, ref[r][0], oth[r][0]])
        dis['files:' + nm] = {k: (v[:20] if isinstance(v, list) else v) for k, v in d.items()}
        dis['files:' + nm + ':counts'] = {k: len(v) for k, v in d.items()}
    cmp_files('unsq-extract-vs-unsquashfs-lls', files_u, files_lls, False)
    cmp_files('unsq-extract-vs-sqfs-list-auto', files_u, files_py, True)
    cmp_files('unsq-extract-vs-sqfs-list-le', files_u, files_pyle, True)
    cmp_files('unsq-extract-vs-7z-list', files_u, files_z, False)
    cmp_files('unsq-extract-vs-7z-extract', files_u, files_7, True)

    # ---- non-regular
    def nr_tree(tree):
        return {r: (v[0], v[2]) for r, v in tree.items() if v[0] != 'file'}
    nr_u = nr_tree(tree_u)
    nr_lls = {r: (v[0], v[2]) for r, v in lls.items() if v[0] != 'file'}
    nr_py = {r: (v[0], v[1] if len(v) > 1 else '') for r, v in sq['auto'][1].items()}
    nr_pyle = {r: (v[0], v[1] if len(v) > 1 else '') for r, v in sq['le'][1].items()}
    nr_7 = nr_tree(tree_7)
    for r in demoted:
        nr_7[r] = nr_lls[r]
    nr_z = {r: (v[0], '') for r, v in z_list.items() if v[0] != 'file'}

    def cmp_nr(nm, ref, oth, detail=True):
        miss = sorted(set(ref) - set(oth))
        extra = sorted(set(oth) - set(ref))
        diff = sorted(r for r in set(ref) & set(oth) if ref[r][0] != oth[r][0] or (detail and ref[r][1] != oth[r][1]))
        dis['nonreg:' + nm] = {'missing_in_other': miss[:20], 'extra_in_other': extra[:20], 'differ': [[r, ref[r], oth[r]] for r in diff[:20]]}
        dis['nonreg:' + nm + ':counts'] = {'missing_in_other': len(miss), 'extra_in_other': len(extra), 'differ': len(diff)}
    # ref for non-regular = unsquashfs -lls (the only reader that names devices when the
    # extract runs unprivileged); the extract tree is compared to it and may lack devices.
    cmp_nr('unsquashfs-lls-vs-extract-tree', nr_lls, nr_u)
    cmp_nr('unsquashfs-lls-vs-sqfs-list-auto', nr_lls, nr_py)
    cmp_nr('unsquashfs-lls-vs-sqfs-list-le', nr_lls, nr_pyle)
    cmp_nr('unsquashfs-lls-vs-7z-list', nr_lls, nr_z, detail=False)
    cmp_nr('unsquashfs-lls-vs-7z-extract-tree', nr_lls, nr_7)

    # ---- write oracle tables (files: unsquashfs-extract hashes; fall back flagged)
    unhashed = [r for r, v in files_u.items() if v[0] is None]
    with open(os.path.join(outdir, 'oracle.tsv'), 'w', encoding='utf-8', errors='surrogateescape', newline='') as f:
        for r, (h, s) in bsort([(r, v) for r, v in files_u.items()]):
            f.write('%s\t%s\t%s\n' % (r, h, s))
    # non-regular: union of -lls entries (authoritative for devices); detail from -lls
    nr_rows = [(r, v[0], v[1]) for r, v in nr_lls.items()]
    with open(os.path.join(outdir, 'nonregular.tsv'), 'w', encoding='utf-8', errors='surrogateescape', newline='') as f:
        for r, k, dt in bsort(nr_rows):
            f.write('%s\t%s\t%s\n' % (r, k, dt))

    # ---- structural stats
    syms = {r: v[1] for r, v in nr_lls.items() if v[0] == 'symlink'}
    abs_t = [r for r, t in syms.items() if t.startswith('/')]
    empty_t = [r for r, t in syms.items() if t == '']
    esc_rel = []
    for r, t in syms.items():
        if t and not t.startswith('/'):
            base = os.path.dirname(r)
            n = os.path.normpath(os.path.join(base, t))
            if n == '..' or n.startswith('../'):
                esc_rel.append(r)
    def resolves(r, t):
        """does the target resolve to an entry within the image (lexical, one hop)?"""
        if not t:
            return None
        n = os.path.normpath(t.lstrip('/')) if t.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(r), t))
        if n.startswith('..'):
            return False
        return n in lls or n == '.'
    dangling_abs = [r for r in abs_t if resolves(r, syms[r]) is False]
    names = list(lls)
    weird = {'tab': [n for n in names if '\t' in n], 'newline': [n for n in names if '\n' in n], 'cr': [n for n in names if '\r' in n],
             'non_utf8_surrogate': [n for n in names if any(0xDC80 <= ord(c) <= 0xDCFF for c in n)],
             'leading_dash': [n for n in names if n.rsplit('/', 1)[-1].startswith('-')],
             'backslash': [n for n in names if '\\' in n], 'space': [n for n in names if ' ' in n],
             'sym_target_space_arrow': [r for r, t in syms.items() if ' -> ' in t or ' -> ' in r]}
    low = {}
    for n in names:
        low.setdefault(n.lower(), []).append(n)
    case_coll = [v for v in low.values() if len(v) > 1]
    sizes = [v[1] for v in lls.values() if v[0] == 'file']
    modes = {'setuid_or_setgid': 0}
    for line in lls_text.split('\n'):
        m = LLS.match(line)
        if m and ('s' in m.group(2)[2] or 's' in m.group(2)[5] or 'S' in m.group(2)[2] or 'S' in m.group(2)[5]):
            modes['setuid_or_setgid'] += 1
    kinds = {}
    for v in lls.values():
        kinds[v[0]] = kinds.get(v[0], 0) + 1
    z_hdr = timed('7z-header', ['7z', 'l', '-slt', member], {}) if False else None
    summary = {
        'id': cid, 'member': {'sha256': member_sha, 'size': os.path.getsize(member)},
        'entries_by_kind_unsquashfs_lls': kinds,
        'regular_files': len(files_u), 'regular_bytes': sum(s for _, s in files_u.values() if s),
        'zero_size_files': sum(1 for s in sizes if s == 0),
        'dirs': kinds.get('dir', 0), 'symlinks': kinds.get('symlink', 0),
        'char_devices': kinds.get('char-device', 0), 'block_devices': kinds.get('block-device', 0),
        'fifos': kinds.get('fifo', 0), 'sockets': kinds.get('socket', 0),
        'symlinks_absolute_target': len(abs_t), 'symlinks_relative_escaping_root': len(esc_rel),
        'symlinks_empty_target': len(empty_t), 'symlinks_absolute_target_not_in_image': len(dangling_abs),
        'symlink_escape_examples': sorted(abs_t)[:5] + sorted(esc_rel)[:5],
        'empty_target_examples': sorted(empty_t)[:5],
        'devices': [[r, v[0], v[1]] for r, v in nr_lls.items() if v[0].endswith('device')],
        'unusual_names': {k: len(v) for k, v in weird.items()},
        'unusual_names_examples': {k: v[:3] for k, v in weird.items() if v},
        'case_collisions': len(case_coll), 'setuid_setgid_entries': modes['setuid_or_setgid'],
        'reader_notes': notes,
        'unparsed_lls_lines': len(lls_bad), 'unparsed_lls_examples': lls_bad[:3],
        'extract_unreadable_files': errs_u[:5], 'extract_unhashed_regular': len(unhashed),
        'extract_tree_counts': {'file': len(files_u), 'dir': sum(1 for v in tree_u.values() if v[0] == 'dir'),
                                'symlink': sum(1 for v in tree_u.values() if v[0] == 'symlink'),
                                'device': sum(1 for v in tree_u.values() if v[0].endswith('device'))},
        'extract_7z_counts': {'file': len(files_7), 'symlink': sum(1 for v in tree_7.values() if v[0] == 'symlink'),
                              'dir': sum(1 for v in tree_7.values() if v[0] == 'dir')},
        '7z_list_counts': {'file': len(files_z), 'nonregular': len(nr_z)},
        'sqfs_list_counts': {'auto_files': len(files_py), 'auto_nonreg': len(nr_py), 'le_files': len(files_pyle), 'le_nonreg': len(nr_pyle)},
        'unique_sha256': len({v[0] for v in files_u.values() if v[0]}),
        'wall_s': {k: v['wall_s'] for k, v in times.items()}, 'exits': {k: v.get('exit') for k, v in times.items() if 'exit' in v},
    }
    json.dump(summary, open(os.path.join(outdir, 'oracle-summary.json'), 'w'), indent=1, sort_keys=True)
    json.dump(dis, open(os.path.join(outdir, 'disagreements.json'), 'w'), indent=1, sort_keys=True)
    json.dump(times, open(os.path.join(outdir, 'times.json'), 'w'), indent=1, sort_keys=True)
    # 7z extract is advisory (rewrites link targets, demotes links/devices to 0-byte files):
    # its residue is reported, not scored.  Primary readers: unsquashfs extract + -lls,
    # sqfs-list auto/le, 7z list.
    bad = sum(v for k, d in dis.items() if k.endswith(':counts') and '7z-extract' not in k for v in d.values())
    adv = sum(v for k, d in dis.items() if k.endswith(':counts') and '7z-extract' in k for v in d.values())
    json.dump({'primary_disagreements': bad, 'advisory_7z_extract_residue': adv}, open(os.path.join(outdir, 'disagreement-totals.json'), 'w'), indent=1)
    print(json.dumps({'id': cid, 'primary_disagreements': bad, 'advisory_7z_extract_residue': adv, 'regular': len(files_u), 'nonregular': len(nr_lls)}))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
