#!/usr/bin/env python3
"""Derive the round-39 C1 symlink tables for carriers K1-K4 (read-only).

Sources
  K1/K2 : committed git objects, mode 120000 blobs under
          corpus/evidence/round-37/c1/<K>/src (target bytes = blob content).
  K3/K4 : `sasquatch-v4be -be -ll` long listing of the committed carrier image.

Class rule (extraction-root, NON-clamping).  This is the rule unblob 26.6.4
actually implements (`unblob/extractor.py:fix_symlink` + `file_utils.py:is_safe_path`),
verified on live dev carriers (see evidence/dev-links-envelope.json):

  * Relative target: start the stack at the link's own directory components
    below the image root; an absolute target is first stripped of exactly one
    leading '/' and resolved from the image root (unblob's `lstrip("/")`).
  * Components are cancelled pairwise against the stack.
  * A '..' met while the stack is empty means the link resolves ABOVE the
    extraction root => class `escaping` (unblob unlinks it and emits
    `MaliciousSymlinkRemoved`; REA records no extraction gap).
  * Otherwise the link is class `in-tree` (kept as a symlink; REA records one
    `unpublished-entry` gap + one `unpublished_entries[]` row).
  * If the resolved path is itself a symlink of the same image, the same walk is
    applied to it and the chain is followed to a fixed point: escaping anywhere
    => `escaping` (unblob removes the whole chain); a cycle => `in-tree` (unblob
    keeps cycles: Path.resolve() returns the unresolved path under python >= 3.13,
    so is_recursive_link() never raises); otherwise `in-tree` at the final
    destination, whose recorded link_target is the flattened one.

  Do NOT classify with posixpath.normpath / path.posix.normalize / realpath:
  those clamp a leading '..' at '/', which turns K1's escaping link into
  `in-tree` and contradicts K1's frozen round-38 receipt.

Usage: python3 -I -B symlink-tables.py [--lane LANE] [--out DIR]
Writes symlinks-K1.tsv .. symlinks-K4.tsv (relative_path, link_target, class)
and symlinks-combined.tsv (carrier, symlink, target, class, resolved, round-38 outcome).
Exit 0 ok, 2 unexpected carrier content (assertion failure).
"""
import argparse, json, os, subprocess, sys

CARRIERS = ('K1', 'K2', 'K3', 'K4')
SRC_BASED = ('K1', 'K2')
ORADIR = 'corpus/evidence/round-37/c1'
AFTERDIR = 'corpus/evidence/round-38/c1'

# Frozen expectations: a divergence is a hard failure, not a silent rewrite.
EXPECTED = {
    'K1': [('link-to-hello', '../hello.txt', 'escaping')],
    'K2': [('var/lib/run-link', '../../a/run.sh', 'in-tree')],
    'K3': [],
    'K4': [],
}


def git(root, *args):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('git ' + ' '.join(args) + ': ' + p.stderr.decode(errors='replace').strip())
    return p.stdout


def committed_symlinks(root, path):
    """[(relative_path_inside_image, target)] from git mode 120000 blobs."""
    rows = []
    for line in git(root, 'ls-files', '-s', '--', path).decode().splitlines():
        meta, rel = line.split('\t', 1)
        mode, blob, _stage = meta.split()
        if mode != '120000':
            continue
        inside = os.path.relpath(rel, path)
        rows.append((inside, git(root, 'cat-file', 'blob', blob).decode('utf-8', 'surrogateescape')))
    return sorted(rows)


def image_symlinks(image, tool):
    """[(relative_path_inside_image, target)] from `sasquatch-v4be -be -ll`."""
    p = subprocess.run([tool, '-be', '-ll', image], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f'sasquatch-v4be failed on {image}: {p.stderr.strip()}')
    rows = []
    for line in (p.stdout + p.stderr).splitlines():
        if not line.startswith('l'):
            continue
        left, _, target = line.partition(' -> ')
        name = left.split()[-1]
        prefix = 'squashfs-root/'
        if not name.startswith(prefix):
            raise SystemExit(f'unexpected listing row: {line!r}')
        rows.append((name[len(prefix):], target))
    return sorted(rows)


def classify_one(link_rel, target):
    """One lexical hop. Return (class, resolved_path_inside_image_or_None).

    This is the rule for a link whose target is not itself a symlink of the image.
    """
    if target.startswith('/'):            # unblob: Path(target).as_posix().lstrip('/')
        stack, comps = [], target.split('/')[1:]
    else:
        stack, comps = [c for c in link_rel.split('/')[:-1] if c], target.split('/')
    escaped = False
    for c in comps:
        if c in ('', '.'):
            continue
        if c == '..':
            if stack:
                stack.pop()
            else:
                escaped = True
        else:
            stack.append(c)
    return ('escaping', None) if escaped else ('in-tree', '/' + '/'.join(stack) if stack else '/')


def classify(link_rel, target, links=None, hops=40):
    """Class of one link, following an in-image chain to a fixed point.

    unblob resolves the whole host chain (`path.resolve()`), so the receipt for a link
    whose target is another symlink follows the chain:
      * chain that leaves the root -> every link in it is removed (no gaps)  => escaping
      * chain that stays inside    -> links kept, targets flattened         => in-tree
      * cycle                      -> Path.resolve() returns the unresolved path under
        Python >= 3.13 (no RuntimeError), so `is_recursive_link` never fires and the links
        are kept (`a -> b` rewritten to a self-loop `a -> a`)                => in-tree
    Measured on dev3/dev4 in this seat's evidence. `links` maps in-image path -> target.
    """
    klass, resolved = classify_one(link_rel, target)
    if klass != 'in-tree' or not links:
        return klass, resolved
    seen, cur = {link_rel}, resolved.lstrip('/')
    while cur in links and hops > 0:
        hops -= 1
        if cur in seen:
            return 'in-tree', '/' + cur                     # cycle: kept, not removed
        seen.add(cur)
        klass, resolved = classify_one(cur, links[cur])
        if klass != 'in-tree':
            return 'escaping', None                          # the chain leaves the root
        cur = resolved.lstrip('/')
    return 'in-tree', resolved


def chain_report(rows):
    """Report links whose target is another symlink of the same image (diagnostic only).

    `classify()` already follows these hops; this keeps the fact visible in the tool's
    output so a K5/K6 build can be reviewed before the freeze.
    """
    links = {rel: target for rel, target, _klass in rows}
    out = []
    for rel, target, _klass in rows:
        cur = _one_step(rel, target)
        if cur is None or cur not in links:
            continue                                   # one hop, no chain
        trail, seen = [cur], {rel}
        verdict = 'chain->' + cur
        while cur in links:
            if cur in seen:
                verdict = 'cycle'
                break
            seen.add(cur)
            nxt = _one_step(cur, links[cur])
            if nxt is None:
                verdict = 'chain->outside'
                break
            trail.append(nxt)
            cur = nxt
            verdict = 'chain->' + ' -> '.join(trail)
        out.append((rel, verdict))
    return out


def _one_step(link_rel, target):
    """One lexical hop: resolved in-image path without the leading '/', None if it escapes."""
    return (classify_one(link_rel, target)[1] or '').lstrip('/') or None


def receipt_outcome(lane, carrier):
    path = os.path.join(lane, AFTERDIR, carrier, 'after.json')
    if not os.path.exists(path):
        return {'present': False}
    env = json.load(open(path))
    nr = env.get('normalized_result') or {}
    gaps = [g for g in (nr.get('extraction_gaps') or []) if g.get('kind') == 'unpublished-entry']
    return {
        'present': True,
        'evidence_id': env.get('evidence_id'),
        'coverage': nr.get('coverage'),
        'unpublished_entries': nr.get('unpublished_entries') or [],
        'unpublished_entry_gap_paths': sorted(g.get('relative_path') or g.get('input_path') or '' for g in gaps),
        'gap_kinds': sorted({g.get('kind') for g in (nr.get('extraction_gaps') or [])}),
        'diagnostics': [(d.get('report') or {}).get('__typename__') for d in (nr.get('diagnostics') or [])],
        'symlinks_removed': sorted(
            (d.get('report') or {}).get('link', '').split('/extracted/', 1)[-1]
            for d in (nr.get('diagnostics') or [])
            if (d.get('report') or {}).get('__typename__') == 'MaliciousSymlinkRemoved'),
    }


def default_lane():
    """Walk up from this file until corpus/evidence/round-37/c1 is a directory."""
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ORADIR)):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.abspath(__file__))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', default=default_lane())
    ap.add_argument('--out', default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--sasquatch', default=os.path.expanduser('~/.local/bin/sasquatch-v4be'))
    a = ap.parse_args(argv)
    lane, out = os.path.abspath(a.lane), os.path.abspath(a.out)
    if not os.path.isdir(os.path.join(lane, ORADIR)):
        raise SystemExit(f'not a lane root: {lane}')
    os.makedirs(out, exist_ok=True)

    tables, combined, bad = {}, [], []
    for k in CARRIERS:
        if k in SRC_BASED:
            raw = committed_symlinks(lane, f'{ORADIR}/{k}/src')
        else:
            image = os.path.join(lane, ORADIR, k, 'carrier.bin')
            raw = image_symlinks(image, a.sasquatch)
        links = dict(raw)
        rows = []
        for rel, target in raw:
            klass, resolved = classify(rel, target, links)
            rows.append((rel, target, klass))
            combined.append((k, rel, target, klass, resolved, receipt_outcome(lane, k)))
        tables[k] = rows
        got = [(r, t, c) for r, t, c in rows]
        if got != EXPECTED[k]:
            bad.append((k, got))

    for k in CARRIERS:
        with open(os.path.join(out, f'symlinks-{k}.tsv'), 'w') as fh:
            for rel, target, klass in tables[k]:
                fh.write(f'{rel}\t{target}\t{klass}\n')

    with open(os.path.join(out, 'symlinks-combined.tsv'), 'w') as fh:
        fh.write('carrier\tsymlink\tlink_target\tclass\tresolved\tround38_gap\tsymlink_removed_by_unblob\tcoverage\n')
        for k, rel, target, klass, resolved, rec in combined:
            if not rec.get('present'):
                fh.write(f'{k}\t{rel}\t{target}\t{klass}\t{resolved or "-"}\tNO-RECEIPT\t-\t-\n')
                continue
            gap = ','.join(rec['unpublished_entry_gap_paths']) or '-'
            removed = ','.join(rec['symlinks_removed']) or '-'
            fh.write(f'{k}\t{rel}\t{target}\t{klass}\t{resolved or "-"}\t{gap}\t{removed}\t{rec["coverage"]}\n')
        # carriers without any symlink still need their receipt verdict visible
        for k in CARRIERS:
            if tables[k]:
                continue
            rec = receipt_outcome(lane, k)
            fh.write(f'{k}\t(none)\t-\t-\t-\t{",".join(rec.get("gap_kinds") or []) or "-"}\t-\t{rec.get("coverage")}\n')

    for k, got in bad:
        print(f'ASSERTION FAILED {k}: {got!r} != {EXPECTED[k]!r}', file=sys.stderr)
    counts = {k: len(v) for k, v in tables.items()}
    chains = {k: chain_report(v) for k, v in tables.items() if chain_report(v)}
    for k, rows in chains.items():
        for rel, what in rows:
            print(f'CHAIN {k} {rel}: {what} — the receipt follows the chain, '
                  f'the one-step class does not; see chain_report()', file=sys.stderr)
    print(json.dumps({'rows': counts, 'assertions': 'fail' if bad else 'pass',
                      'chains': {k: len(v) for k, v in chains.items()}}, sort_keys=True))
    return 2 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
