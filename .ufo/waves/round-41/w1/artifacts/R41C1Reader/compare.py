#!/usr/bin/env python3
"""Compare sqfs-list.py TSVs against a sasquatch-v4be extracted tree + -lls."""
import hashlib, json, os, sys

def sha(p):
    h = hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda: f.read(1<<20), b''):
            h.update(c)
    return h.hexdigest()

def parse_lls(path):
    reg, link, dev, ipc, dirs = {}, {}, {}, {}, set()
    other = []
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line: continue
            t = line[0]; tok = line.split()
            if t == 'l':
                # mode owner size date time PATH -> TARGET   (path may have spaces)
                head, tgt = line.split(' -> ', 1)
                p = head.split(None, 5)[5]
                link[p] = tgt
            elif t in 'cb':
                p = line.split(None, 6)[6]
                dev[p] = (int(tok[2].rstrip(',')), int(tok[3]))   # major, minor
            elif t in 'ps':
                p = line.split(None, 5)[5]; ipc[p] = 'fifo' if t=='p' else 'socket'
            elif t == 'd':
                dirs.add(line.split(None, 5)[5])
            elif t == '-':
                reg[line.split(None, 5)[5]] = (int(tok[2]),)
            else:
                other.append(line)
    strip = lambda p: p[len('squashfs-root'):].lstrip('/')
    return ({strip(k): v for k,v in reg.items()},
            {strip(k): v for k,v in link.items()},
            {strip(k): v for k,v in dev.items()},
            {strip(k): v for k,v in ipc.items()},
            {strip(k) for k in dirs}, other)

def read_tsv(path):
    out = {}
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        for line in fh:
            a = line.rstrip('\n').split('\t')
            out[a[0]] = tuple(a[1:])
    return out

root, lls, files_tsv, nonreg_tsv = sys.argv[1:5]
lls_reg, lls_link, lls_dev, lls_ipc, lls_dirs, other = parse_lls(lls)

# tree walk
tree_reg = {}
for dp, dns, fns in os.walk(root):
    for fn in fns:
        full = os.path.join(dp, fn)
        rel = os.path.relpath(full, root)
        if os.path.islink(full):
            continue
        st = os.lstat(full)
        if not os.path.isfile(full):
            continue
        tree_reg[rel] = sha(full)
tree_links = {}
tree_special = {}
for dp, dns, fns in os.walk(root):
    for n in dns + fns:
        full = os.path.join(dp, n); rel = os.path.relpath(full, root)
        if os.path.islink(full):
            tree_links[rel] = os.readlink(full)
        elif not os.path.isdir(full) and not os.path.isfile(full):
            tree_special[rel] = os.lstat(full).st_mode

r_files = read_tsv(files_tsv)          # path -> (sha256, size)
r_non = read_tsv(nonreg_tsv)           # path -> (kind, detail)

rep = {}
rep['lls_counts'] = {'reg': len(lls_reg), 'dir': len(lls_dirs), 'link': len(lls_link),
                     'dev': len(lls_dev), 'ipc': len(lls_ipc), 'unparsed': len(other)}
rep['tree_counts'] = {'reg': len(tree_reg), 'link': len(tree_links), 'special': len(tree_special)}
rep['reader_counts'] = {'reg': len(r_files), 'nonreg': len(r_non)}

# 1. regular files: set + digest, tree vs reader
only_tree = sorted(set(tree_reg) - set(r_files))
only_reader = sorted(set(r_files) - set(tree_reg))
bad = [(p, tree_reg[p], r_files[p][0]) for p in sorted(set(tree_reg) & set(r_files))
       if tree_reg[p] != r_files[p][0]]
rep['reg_only_in_tree'] = only_tree
rep['reg_only_in_reader'] = only_reader
rep['reg_digest_mismatch'] = bad
# lls size vs reader size
size_bad = [(p, r_files[p][1], lls_reg[p][0]) for p in sorted(set(r_files) & set(lls_reg))
            if int(r_files[p][1]) != lls_reg[p][0]]
rep['size_mismatch_vs_lls'] = size_bad

# 2. lls regular set vs reader regular set (authoritative image metadata)
rep['reg_only_in_lls'] = sorted(set(lls_reg) - set(r_files))
rep['reg_only_in_reader_vs_lls'] = sorted(set(r_files) - set(lls_reg))

# 3. symlinks
r_links = {p: v[1] for p, v in r_non.items() if v[0] == 'symlink'}
rep['link_only_in_lls'] = sorted(set(lls_link) - set(r_links))
rep['link_only_in_reader'] = sorted(set(r_links) - set(lls_link))
rep['link_target_mismatch'] = [(p, lls_link[p], r_links[p]) for p in sorted(set(lls_link) & set(r_links))
                               if lls_link[p] != r_links[p]]
rep['link_extracted_set_diff'] = {'only_lls': sorted(set(lls_link) - set(tree_links)),
                                 'only_tree': sorted(set(tree_links) - set(lls_link)),
                                 'target_mismatch': [(p, lls_link[p], tree_links[p])
                                                     for p in sorted(set(lls_link) & set(tree_links))
                                                     if lls_link[p] != tree_links[p]]}

# 4. devices / ipc
r_dev = {p: tuple(int(x) for x in v[1].split(':')) for p, v in r_non.items()
         if v[0] in ('block-device', 'char-device')}
r_ipc = {p: v[0] for p, v in r_non.items() if v[0] in ('fifo', 'socket')}
rep['dev_reader'] = {p: list(v) for p, v in r_dev.items()}
rep['dev_lls'] = {p: list(v) for p, v in lls_dev.items()}
rep['dev_mismatch'] = [(p, lls_dev[p], r_dev.get(p)) for p in sorted(set(lls_dev) | set(r_dev))
                       if lls_dev.get(p) != r_dev.get(p)]
rep['ipc_reader'] = r_ipc
rep['ipc_lls'] = lls_ipc
rep['ipc_mismatch'] = sorted(set(r_ipc.items()) ^ set(lls_ipc.items()))
rep['special_not_materialised'] = sorted(tree_special)

# 5. directories: reader dirs vs lls dirs (lls includes root '' )
r_dirs = {p for p, v in r_non.items() if v[0] == 'dir'}
rep['dir_counts'] = {'lls_nonroot': len(lls_dirs - {''}), 'reader': len(r_dirs)}
rep['dir_only_in_lls'] = sorted(lls_dirs - {''} - r_dirs)
rep['dir_only_in_reader'] = sorted(r_dirs - lls_dirs)

# 6. symlink class counts from the reader's kind column
print(json.dumps(rep, indent=1, sort_keys=True))
