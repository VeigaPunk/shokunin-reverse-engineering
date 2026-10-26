#!/usr/bin/env python3
"""Proposed correction to QUALITY 79's gate (artifact; not lane code).

tools/round-38/freeze-drift.py answers "did any commit, in an interval the
caller chose, touch a path the caller listed?"  Four cheap bypasses survive
that question.  This gate closes them and is shown able to fail on the
R38W2CritGateBypass fixture and on the round-38 lane bytes:

 1. IDENTITY.  The freeze is derived: the earliest commit that touched the
    claims doc.  An asserted --freeze that is not that commit is refused.
    freeze-drift.py accepts any ancestor -- including the amendment commit
    the lane itself titled "freeze v2"/"freeze v3".
 2. BYTES.  git diff --quiet FREEZE REV over a CLOSED path set must exit 0:
    the measured revision must SHIP the freeze's bytes.  freeze-drift.py only
    lists commits; it never requires the shipped bytes to equal the freeze's,
    so an amendment is "reported" and then adopted in the landing tree.
 3. RECEIPT.  A receipt is required, and it must name the measured revision
    and the derived freeze.  freeze-drift.py never reads the receipt, so
    --rev can be the freeze while the score comes from the tip.
 5. TYPE.  A kill-rule path must be a regular blob at both revisions: a
    symlink's blob is its target text, so editing the target changes the rule
    while every path-addressed check still compares identical link text.
 4. COUNTER.  The counter named in the receipt's argv must be, byte for byte,
    a counter the freeze held -- whether read from the repo or copied out of
    it.  freeze-drift.py's path set is a fixed list, so a counter at a NEW
    path is invisible even when the receipt names it.

Closed set = freeze-drift's DEFAULT plus the surfaces that change the rule in
effect: control generator, receipt-producing harness, carrier bytes, digest
helper.  Claim data (after/before receipts) is exempt from byte-equality and
reported separately; its provenance is QUALITY 78's independent re-run.

Exit 0 clean, 1 any check fails, 2 unevaluable.
"""
import argparse, hashlib, json, os, subprocess, sys

CLAIM_DOC_DEFAULT = 'plans/round-38-claims.md'
CLOSED = [
    'plans/round-38-claims.md',
    'tools/round-38/c1-counter.py',
    'tools/round-38/c2-counter.py',
    '.ufo/waves/round-38/c1/carriers.json',
    'corpus/evidence/round-37/c1/*/oracle.tsv',
    'corpus/evidence/round-37/c1/*/carrier.*',
    'tools/round-38/gen-controls.py',
    'tools/round-38/c1-run.sh',
    'tools/round-27/xpin-attribute.mjs',
]
# Claim DATA is exempt from byte-equality by design: after/before receipts are
# produced after the freeze.  Their provenance is QUALITY 78's independent
# re-run, not this gate.  What must not move is the surface that decides what
# the data means.
DATA = [
    'corpus/evidence/round-38/c1/*/after.json',
    'corpus/evidence/round-38/c1/*/before.json',
]
COUNTERS = ['tools/round-38/c1-counter.py', 'tools/round-38/c2-counter.py']


def git(root, *args):
    return subprocess.run(['git', '-C', root, *args], capture_output=True)


def blob_sha256(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}')
    return hashlib.sha256(p.stdout).hexdigest() if p.returncode == 0 else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--freeze', help='optional asserted freeze; refused unless it equals the derived one')
    ap.add_argument('--receipt', required=True)
    ap.add_argument('--claim-doc', default=CLAIM_DOC_DEFAULT)
    ap.add_argument('--json-out')
    a = ap.parse_args(argv)
    res = {'tool': 'pin-gate', 'rev': a.rev, 'receipt': a.receipt, 'paths': CLOSED, 'fails': []}

    def fail(kind, detail):
        res['fails'].append({'check': kind, 'detail': detail})

    for r in (a.rev,) + ((a.freeze,) if a.freeze else ()):
        if git(a.root, 'cat-file', '-e', f'{r}^{{commit}}').returncode:
            res.update(verdict='unevaluable', reason=f'unknown revision {r}')
            return finish(res, a.json_out, 2)

    firsts = [l for l in git(a.root, 'log', '--reverse', '--format=%H', '--', a.claim_doc).stdout.decode().splitlines() if l.strip()]
    if not firsts:
        res.update(verdict='unevaluable', reason='claims doc never committed')
        return finish(res, a.json_out, 2)
    derived = firsts[0]
    res['freeze_derived'] = derived
    res['freeze_asserted'] = a.freeze
    if a.freeze and a.freeze != derived:
        fail('freeze-not-first', f'asserted {a.freeze}; first commit touching {a.claim_doc} is {derived}')
    if git(a.root, 'merge-base', '--is-ancestor', derived, a.rev).returncode:
        fail('freeze-not-ancestor', f'{derived} is not an ancestor of {a.rev}')

    # 5. TYPE.  A kill-rule path must be a regular blob at both revisions: a
    # symlink's blob is the target path, so a target edited in place changes the
    # rule while every path-addressed check (log, diff) still compares identical
    # link text.
    import fnmatch
    for label, rev in (('freeze', derived), ('measured', a.rev)):
        for line in git(a.root, 'ls-tree', '-r', rev).stdout.decode().splitlines():
            meta, path = line.split('\t', 1)
            mode = meta.split()[0]
            if mode in ('100644', '100755'):
                continue
            if any(fnmatch.fnmatchcase(path, pat) for pat in CLOSED):
                fail('non-regular-kill-rule-path', f'{path} at {label} revision {rev[:12]} has mode {mode}')

    changed = [l for l in git(a.root, 'diff', '--name-only', '--no-renames', derived, a.rev, '--',
                              *[f':(glob){p}' for p in CLOSED]).stdout.decode().splitlines() if l.strip()]
    res['bytes_differ'] = changed
    if changed:
        fail('bytes-differ', f'{len(changed)} kill-rule path(s) at {a.rev[:12]} are not the freeze bytes: '
                             + ', '.join(changed[:6]) + (' …' if len(changed) > 6 else ''))

    try:
        rec = json.load(open(a.receipt))
    except Exception as e:  # noqa: BLE001
        res.update(verdict='unevaluable', reason=f'receipt unreadable: {e}')
        return finish(res, a.json_out, 2)
    res['receipt_revision'] = rec.get('revision')
    res['receipt_freeze'] = rec.get('freeze')
    if rec.get('revision') != a.rev:
        fail('receipt-rev-unbound', f"receipt names {rec.get('revision')}, gate measured {a.rev}")
    if rec.get('freeze') != derived:
        fail('receipt-freeze-unbound', f"receipt names {rec.get('freeze')}, derived {derived}")

    frozen_hashes = {p: blob_sha256(a.root, derived, p) for p in COUNTERS}
    frozen_hashes = {p: h for p, h in frozen_hashes.items() if h}
    argv_paths = [t for t in (rec.get('argv') or []) if isinstance(t, str) and t.endswith(('.py', '.mjs', '.sh'))]
    res['receipt_tool_paths'] = argv_paths
    if not argv_paths:
        fail('counter-unnamed', 'receipt argv names no counter file')
    root_real = os.path.realpath(a.root)
    for p in argv_paths:
        cand = os.path.realpath(p) if os.path.isabs(p) else os.path.realpath(os.path.join(a.root, p))
        rel = os.path.relpath(cand, root_real) if cand and cand.startswith(root_real + os.sep) else None
        if rel is not None:
            if git(a.root, 'cat-file', '-e', f'{derived}:{rel}').returncode:
                fail('counter-not-in-freeze', f'{rel} does not exist at the derived freeze (new/edited counter path)')
            elif git(a.root, 'diff', '--quiet', derived, a.rev, '--', rel).returncode:
                fail('counter-not-frozen', f'{rel} at {a.rev[:12]} differs from the freeze bytes')
        elif os.path.isfile(p):
            h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            if h not in frozen_hashes.values():
                fail('counter-not-frozen', f"{p} (copied out of the repo) is not any freeze counter's bytes")
            else:
                res.setdefault('counter_copies_ok', []).append(p)
        else:
            fail('counter-not-in-freeze', f'{p} is neither in the repo nor on disk (unverifiable counter)')

    data_changed = [l for l in git(a.root, 'diff', '--name-only', '--no-renames', derived, a.rev, '--',
                                   *[f':(glob){p}' for p in DATA]).stdout.decode().splitlines() if l.strip()]
    res['claim_data_present'] = data_changed

    res['commits'] = git(a.root, 'log', '--format=%h %s', f'{derived}..{a.rev}', '--').stdout.decode().splitlines()
    res['verdict'] = 'clean' if not res['fails'] else 'drift'
    return finish(res, a.json_out, 0 if not res['fails'] else 1)


def finish(res, out, code):
    text = json.dumps(res, indent=1)
    if out:
        open(out, 'w').write(text + '\n')
    print(json.dumps({k: res.get(k) for k in ('tool', 'freeze_derived', 'freeze_asserted', 'verdict', 'fails')}, indent=1))
    return code


if __name__ == '__main__':
    sys.exit(main())
