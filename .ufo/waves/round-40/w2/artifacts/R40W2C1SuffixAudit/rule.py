"""Round-41 proposal: root-anchored entry matching (R40W2C1SuffixAudit)."""
def path_parts(path):
    if not isinstance(path, str):
        return None
    while path.startswith('$output/'):
        path = path[len('$output/'):]
    return [p for p in path.split('/') if p not in ('', '.')]

def chunk_root(env):
    """(root, why): the single chunk extract directory the receipt names."""
    nr = env.get('normalized_result') or {}
    roots = []
    for d in nr.get('derivations') or []:
        if not isinstance(d, dict):
            continue
        ps = path_parts(d.get('child_path'))
        if ps and len(ps) == 1 and ps[0].endswith('_extract'):
            roots.append(ps[0])
    if not roots:                                  # fixtures / older receipts
        cand = set()
        for key in ('files', 'extraction_gaps', 'unpublished_entries'):
            for e in nr.get(key) or []:
                ps = path_parts((e or {}).get('relative_path'))
                if ps and ps[0].endswith('_extract'):
                    cand.add(ps[0])
        roots = sorted(cand)
    roots = sorted(set(roots))
    if len(roots) != 1:
        return None, ('no_root' if not roots else 'mult_root:%r' % (roots,))
    return roots[0], None

def entry_rel(path, root):
    ps = path_parts(path)
    if not ps or root is None or '..' in ps:
        return None
    if ps[0] == root:
        payload = ps[1:]
    else:
        try:
            i = ps.index(root)
        except ValueError:
            return None
        payload = ps[i + 1:]
    return '/'.join(payload)

def same_entry(path, rel, root):
    return rel is not None and entry_rel(path, root) == rel
