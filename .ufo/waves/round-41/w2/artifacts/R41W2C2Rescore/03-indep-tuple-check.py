"""C2 re-score: independent observed-tuple check.

Computes (H, G, D, BE, SR, P) from each held-out envelope.json per the frozen
precedence text's FEATURE definitions (claims.md R41-C2 "Label precedence"),
without importing tools/round-41/c2-counter.py, then compares against the
manifest's `declared` field and against `class_expected.features`.
"""
import json
import os
import sys

ROOT = sys.argv[1]
HELD = os.path.join(ROOT, 'corpus', 'evidence', 'round-41', 'c2', 'heldout')
SYMLINK = 'MaliciousSymlinkRemoved'


def as_list(v):
    return v if isinstance(v, list) else []


def iter_dicts(obj):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def argv_tokens(cmd):
    if isinstance(cmd, str):
        return cmd.split()
    if isinstance(cmd, list):
        out = []
        for x in cmd:
            out.extend(argv_tokens(x) if isinstance(x, (str, list)) else [str(x)])
        return out
    return []


def producer_argv_strings(data):
    """Every argv recorded on diagnostics[].report.command (the frozen BE source)."""
    out = []
    nr = data.get('normalized_result') if isinstance(data.get('normalized_result'), dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in as_list(source):
            rep = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(rep, dict) and 'command' in rep:
                out.append(rep['command'])
    return out


def observed(data):
    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    H = set()
    for chunk in as_list(nr.get('chunks')):
        if isinstance(chunk, dict):
            h = chunk.get('handler')
            if isinstance(h, str):
                H.add(h)
    G = set()
    D = set()
    for gap in as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        h = gap.get('handler')
        if isinstance(h, str):
            H.add(h)
        k = gap.get('kind')
        if isinstance(k, str):
            G.add(k)
        for dep in as_list(gap.get('dependencies')):
            if isinstance(dep, str):
                D.add(dep)
    argv = producer_argv_strings(data)
    if not argv:
        be = 'n/a'
    else:
        toks = [t for c in argv for t in argv_tokens(c)]
        be = 'yes' if '-be' in toks else 'no'
    SR = False
    for diag in as_list(nr.get('diagnostics')):
        rep = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(rep, dict) and rep.get('__typename__') == SYMLINK:
            SR = True
            break
    if not SR:
        for found in iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK:
                SR = True
                break
            if found.get('type') == SYMLINK or found.get('report_type') == SYMLINK:
                SR = True
                break
    P = len(as_list(nr.get('files')))
    return {'handler_set': sorted(H), 'gap_kinds': sorted(G),
            'gap_dependencies': sorted(D), 'be_argv': be,
            'symlink_removed': SR, 'published': 'nonzero' if P else 'zero',
            'P': P, 'n_argv': len(argv),
            'argv_sample': toks[:12] if argv else []}


def norm_declared(d):
    """Normalise a manifest tuple to comparable shape."""
    if not isinstance(d, dict):
        return None
    out = {}
    for k in ('handler_set', 'gap_kinds', 'gap_dependencies'):
        v = d.get(k)
        out[k] = sorted(v) if isinstance(v, list) else []
    be = d.get('be_argv')
    out['be_argv'] = str(be).lower() if isinstance(be, str) else be
    sr = d.get('symlink_removed')
    out['symlink_removed'] = sr if isinstance(sr, bool) else str(sr).lower() in ('yes', 'true')
    p = d.get('published')
    if isinstance(p, str):
        out['published'] = 'nonzero' if p.strip().lower() in ('nonzero', 'non-zero', '>0', 'some') else 'zero'
    else:
        out['published'] = 'nonzero' if p else 'zero'
    return out


def main():
    man = json.load(open(os.path.join(HELD, 'manifest.json')))
    rows = []
    for c in man['carriers']:
        cid = c['id']
        envp = os.path.join(HELD, cid, 'envelope.json')
        data = json.load(open(envp)) if os.path.isfile(envp) else None
        obs = observed(data) if data is not None else None
        decl = norm_declared(c.get('declared'))
        cex = c.get('class_expected') if isinstance(c.get('class_expected'), dict) else None
        cexf = norm_declared(cex.get('features')) if cex else None
        keys = ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
                'symlink_removed', 'published')
        diff_decl = [k for k in keys if obs and decl and obs[k] != decl[k]] if decl else None
        diff_cex = [k for k in keys if obs and cexf and obs[k] != cexf[k]] if cexf else None
        diff_dc = [k for k in keys if decl and cexf and decl[k] != cexf[k]] if (decl and cexf) else None
        rows.append({
            'id': cid, 'class': c['class'],
            'has_declared': decl is not None,
            'has_class_expected_features': cexf is not None,
            'observed': obs, 'declared': decl, 'class_expected_features': cexf,
            'differ_observed_vs_declared': diff_decl,
            'differ_observed_vs_class_expected': diff_cex,
            'differ_declared_vs_class_expected': diff_dc,
        })
    n = len(rows)
    summary = {
        'n': n,
        'carriers_with_declared_key': sum(r['has_declared'] for r in rows),
        'carriers_with_class_expected_features': sum(r['has_class_expected_features'] for r in rows),
        'combo_ids': sorted(r['id'] for r in rows if r['class'] == 'combo'),
        'combo_ids_with_declared': sorted(r['id'] for r in rows if r['class'] == 'combo' and r['has_declared']),
        'combo_ids_with_class_expected': sorted(r['id'] for r in rows if r['class'] == 'combo' and r['has_class_expected_features']),
        'observed_eq_declared_all': [r['id'] for r in rows if r['differ_observed_vs_declared'] == []],
        'observed_neq_declared': {r['id']: r['differ_observed_vs_declared'] for r in rows
                                  if r['has_declared'] and r['differ_observed_vs_declared']},
        'observed_neq_class_expected': {r['id']: r['differ_observed_vs_class_expected'] for r in rows
                                        if r['has_class_expected_features'] and r['differ_observed_vs_class_expected']},
        'declared_neq_class_expected': {r['id']: r['differ_declared_vs_class_expected'] for r in rows
                                        if r['differ_declared_vs_class_expected']},
        'no_declared_key': [r['id'] for r in rows if not r['has_declared']],
        'handler_vocabulary': sorted({h for r in rows for h in (r['observed']['handler_set'] if r['observed'] else [])}),
        'gap_vocabulary': sorted({g for r in rows for g in (r['observed']['gap_kinds'] if r['observed'] else [])}),
        'dep_vocabulary': sorted({d for r in rows for d in (r['observed']['gap_dependencies'] if r['observed'] else [])}),
        'be_counts': {},
        'observation_mismatch_total': sum(len(v) for v in
                                          ({r['id']: r['differ_observed_vs_declared'] for r in rows
                                            if r['has_declared'] and r['differ_observed_vs_declared']}).values()),
    }
    for r in rows:
        if r['observed']:
            b = r['observed']['be_argv']
            summary['be_counts'][b] = summary['be_counts'].get(b, 0) + 1
    json.dump({'summary': summary, 'rows': rows}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')


main()
