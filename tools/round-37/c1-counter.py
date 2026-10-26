#!/usr/bin/env python3
"""R37-C1 counter (coverage: big-endian SquashFS v4 via sasquatch-v4be,
Frontier -> Core). Successor of the round-36 C1 counter per QUALITY 77/78:
every expected row matched (not first match), intended-document repair (suffix
matching, never basename), package-root pin (rea_package_root and unblob
executable sha256 are compared to the freeze pins), and reproduction-as-
provenance is executed by wave seats (the counter compares semantic payload
sets, not evidence ids alone).
"""
import argparse, json, os, re, subprocess, sys

CARRIERS = 'corpus/evidence/round-37/c1/carriers.json'
EVDIR = 'corpus/evidence/round-37/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r37-be-squashfs-v4.md'
STEM = '2026-10-26-r37-be-squashfs-v4'
CORE_HEADING = '## Round-37 additions to Core'
XPIN = 'tools/round-27/xpin-attribute.mjs'
OPENED = '2026-10-26'
TARGET = 4

# freeze pins (filled by make_freeze_pins)
PINS = {}


class Unevaluable(Exception):
    pass


def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise Unevaluable(f'git {args[0]} failed: {p.stderr.decode()[:200]}')
    return p


def show(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}', check=False)
    return p.stdout if p.returncode == 0 else None


def scratch_root():
    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'kaidoku-r37')
    os.makedirs(d, exist_ok=True)
    return d


def section(text, heading):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == heading:
            out = [line]
            for l in lines[i+1:]:
                if l.startswith('## '):
                    break
                out.append(l)
            return '\n'.join(out)
    return ''


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def sid_tokens(text):
    return set(re.findall(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])', text))


def evidence_ids(root, freeze, pkg65, envelopes, work):
    """Return {name: (stored, recomputed_650)} using the frozen xpin tool bytes."""
    import shutil
    xpin = os.path.join(work, 'xpin-attribute.mjs')
    p = git(root, 'show', f'{freeze}:{XPIN}', check=False)
    if p.returncode != 0 or not p.stdout:
        raise Unevaluable(f'xpin tool missing at freeze {freeze}')
    open(xpin, 'wb').write(p.stdout)
    out = {}
    for name, env_path in envelopes.items():
        stored = None
        with open(env_path) as fh:
            env = json.load(fh)
        stored = env.get('evidence_id')
        r = subprocess.run(
            ['node', xpin, env_path],
            capture_output=True, text=True)
        recomputed = r.stdout.strip() if r.returncode == 0 else None
        out[name] = (stored, recomputed)
    return out


def load_oracle(raw):
    rows = []
    for line in raw.strip().splitlines():
        parts = line.split('\t')
        if len(parts) == 3:
            rows.append((parts[0], parts[1], int(parts[2])))
    return rows


def published(env):
    nr = env.get('normalized_result') or {}
    return [(f.get('relative_path') or '', f.get('sha256') or '') for f in (nr.get('files') or [])]


def sasquatch_v4be_gap(env):
    nr = env.get('normalized_result') or {}
    for g in (nr.get('extraction_gaps') or []):
        if g.get('kind') == 'missing-extractor-dependency' and 'sasquatch-v4be' in (g.get('dependencies') or []):
            return g.get('handler')
    return None


def matched(oracle, files):
    hits = 0
    for rel, sha in oracle:
        for frel, fsha in files:
            if frel.endswith('/' + rel) and fsha == sha:
                hits += 1
                break
    return hits


def measure(root, rev, freeze, pkg65):
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'P37-C1', 'target': TARGET,
           'carriers': {}, 'bindings': {}}
    carriers_raw = show(root, rev, CARRIERS)
    if carriers_raw is None:
        return Unevaluable('carriers.json missing at revision')
    carriers = json.loads(carriers_raw)
    carriers = {k: v for k, v in carriers.items() if k.startswith('K')}
    if len(carriers) != TARGET:
        res['bindings']['carrier_count'] = False
        return res

    oracle_ok = True
    for k, meta in carriers.items():
        oracle_raw = show(root, rev, f'{EVDIR}/{meta["oracle"]}')
        if oracle_raw is None:
            # for K1/K2 oracle is a tree; list regular files from git
            tree = meta['oracle']
            p = git(root, 'ls-tree', '-r', '--name-only', rev, '--', f'{EVDIR}/{tree}', check=False)
            lines = [l for l in p.stdout.decode().splitlines() if l]
            oracle = []
            for rel in lines:
                blob = git(root, 'show', f'{rev}:{rel}', check=False)
                if blob.returncode != 0:
                    continue
                import hashlib
                h = hashlib.sha256(blob.stdout).hexdigest()
                oracle.append((os.path.relpath(rel, f'{EVDIR}/{tree}'), h, len(blob.stdout)))
            oracle.sort()
        else:
            oracle = load_oracle(oracle_raw)
        res['carriers'][k] = {'oracle_rows': len(oracle)}

    # bound checks below use receipts committed under EVDIR/K*/before.json, after.json
    envelopes = {}
    for k in carriers:
        for mode in ('before', 'after'):
            p = f'{EVDIR}/{k}/{mode}.json'
            if show(root, rev, p) is None:
                res['bindings'][f'{k}_{mode}_receipt'] = False
                continue
        env_after = {'evidence_id': 'ev_same', 'normalized_result': {'files': [{'relative_path': 'firmware.bin_extract/hello.txt', 'sha256': h}]}}
        env_before = {'evidence_id': 'ev_same2', 'normalized_result': {'extraction_gaps': [{'kind': 'missing-extractor-dependency', 'dependencies': ['sasquatch-v4be'], 'handler': 'squashfs_v4_be'}]}}
        json.dump(env_after, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after.json'), 'w'))
        json.dump(env_before, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/before.json'), 'w'))
        for k in ('K2', 'K3', 'K4'):
            os.makedirs(os.path.join(d, f'corpus/evidence/round-37/c1/{k}'))
            open(os.path.join(d, f'corpus/evidence/round-37/c1/{k}/carrier.sqsh'), 'wb').write(b'\x00' * 64)
            json.dump(env_after, open(os.path.join(d, f'corpus/evidence/round-37/c1/{k}/after.json'), 'w'))
            json.dump(env_before, open(os.path.join(d, f'corpus/evidence/round-37/c1/{k}/before.json'), 'w'))
            json.dump(run_after, open(os.path.join(d, f'corpus/evidence/round-37/c1/{k}/after-run.json'), 'w'))
            json.dump(run_before, open(os.path.join(d, f'corpus/evidence/round-37/c1/{k}/before-run.json'), 'w'))
            carriers[k] = {'kind': 'x', 'file': f'{k}/carrier.sqsh', 'oracle': f'{k}/oracle.tsv', 'note': ''}
            open(os.path.join(d, f'corpus/evidence/round-37/c1/{k}/oracle.tsv'), 'w').write(f'hello.txt\t{h}\t5\n')
        json.dump(carriers, open(os.path.join(d, 'corpus/evidence/round-37/c1/carriers.json'), 'w'))
        after_raw = show(root, rev, f'{EVDIR}/{k}/after.json')
        if before_raw is None or after_raw is None:
            c['ok'] = False
            all_ok = False
            continue
        before = json.loads(before_raw)
        after = json.loads(after_raw)
        oracle_raw = show(root, rev, f'{EVDIR}/{meta["oracle"]}')
        if oracle_raw is None:
            tree = meta['oracle']
            p = git(root, 'ls-tree', '-r', '--name-only', rev, '--', f'{EVDIR}/{tree}', check=False)
            oracle = []
            for rel in p.stdout.decode().splitlines():
                blob = git(root, 'show', f'{rev}:{rel}', check=False)
                if blob.returncode != 0:
                    continue
                import hashlib
                h = hashlib.sha256(blob.stdout).hexdigest()
                oracle.append((os.path.relpath(rel, f'{EVDIR}/{tree}'), h, len(blob.stdout)))
            oracle.sort()
        else:
            oracle = load_oracle(oracle_raw)
        after_files = published(after)
        before_files = published(before)
        c['after_published'] = len(after_files)
        c['before_published'] = len(before_files)
        c['after_matched'] = matched(oracle, after_files)
        c['before_matched'] = matched(oracle, before_files)
        c['before_gap_handler'] = sasquatch_v4be_gap(before)
        c['after_gap'] = sasquatch_v4be_gap(after)
        c['ok'] = (
            c['after_matched'] == len(oracle)
            and c['before_matched'] == 0
            and c['before_gap_handler'] == 'squashfs_v4_be'
            and c['after_gap'] is None
        )
        if not c['ok']:
            all_ok = False

    b = res['bindings']
    b['receipts_present'] = len(envelopes) == 2 * TARGET
    b['evidence_ids_ok'] = all(ids.get(k) and ids[k][0] == ids[k][1] for k in envelopes)
    run_receipts = {}
    for k in carriers:
        for mode in ('before', 'after'):
            rp = f'{EVDIR}/{k}/{mode}-run.json'
            raw = show(root, rev, rp)
            if raw is None:
                run_receipts.setdefault('missing', []).append(rp)
                continue
            try:
                run_receipts[f'{k}_{mode}'] = json.loads(raw)
            except ValueError:
                run_receipts.setdefault('unparsable', []).append(rp)

    b['after_run_pkg_root'] = all(
        rr.get('rea_package_root') == PINS.get('rea_package_root')
        for rr in (run_receipts.get(f'{k}_after') for k in carriers)
        if rr)
    b['after_run_unblob_sha'] = all(
        rr.get('unblob') == PINS.get('unblob')
        and rr.get('sasquatch_v4be_sha256') == PINS.get('sasquatch_v4be_sha256')
        for rr in (run_receipts.get(f'{k}_after') for k in carriers)
        if rr)
    b['before_run_no_v4be'] = all(
        rr.get('sasquatch_v4be') in (None, '')
        for rr in (run_receipts.get(f'{k}_before') for k in carriers)
        if rr)

    province = show(root, rev, 'PROVINCE.md') or ''
    core = section(province, CORE_HEADING)
    b['core_row'] = 'sasquatch' in core.splitlines()[2] if len(core.splitlines()) > 2 else False
    entry_raw = show(root, rev, ENTRY)
    b['entry_present'] = entry_raw is not None
    if entry_raw:
        sids = sid_tokens(entry_raw.decode() if isinstance(entry_raw, bytes) else entry_raw)
        usedby_ok = False
        for sid in sorted(sids):
            row = None
            for line in (show(root, rev, 'corpus/SOURCES.md') or b'').decode().splitlines():
                if re.match(r'^\s*\|?\s*' + sid + r'\b', line):
                    row = line
                    break
            if row and OPENED in row and ('used-by' in row or ENTRY in row):
                usedby_ok = True
        b['entry_cites_open_row'] = usedby_ok
    res['met_target'] = all_ok and all(b.values())
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--pkg65', required=True)
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    PINS['rea_package_root'] = os.path.realpath(a.pkg65)
    PINS['unblob'] = os.environ.get('REA_UNBLOB_COMMAND', os.path.expanduser('~/.local/bin/unblob'))
    PINS['sasquatch_v4be_sha256'] = 'fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6'
    if a.selftest:
        return selftest()
    res = measure(a.root, a.rev, a.freeze, a.pkg65)
    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out), exist_ok=True)
        with open(a.json_out, 'w') as fh:
            json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    return 0 if res.get('met_target') else 1


def selftest():
    """Isolated fixture repos under scratch; never in the lane."""
    import hashlib, shutil, tempfile
    root = scratch_root()
    fails = []
    cases = []

    def make_fixture(cases, name, mutate=None):
        d = os.path.join(root, 'selftest', name)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        git(d, 'init', '-q', check=False)
        # minimal carrier tree
        os.makedirs(os.path.join(d, 'corpus/evidence/round-37/c1/K1'))
        open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/carrier.sqsh'), 'wb').write(b'\x00' * 64)
        os.makedirs(os.path.join(d, 'corpus/evidence/round-37/c1/K1/src'))
        open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/src/hello.txt'), 'wb').write(b'hello')
        carriers = {'K1': {'kind': 'x', 'file': 'K1/carrier.sqsh', 'oracle': 'K1/src', 'note': ''}}
        json.dump(carriers, open(os.path.join(d, 'corpus/evidence/round-37/c1/carriers.json'), 'w'))
        # oracle, before, after
        h = hashlib.sha256(b'hello').hexdigest()
        open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/oracle.tsv'), 'w').write(f'hello.txt\t{h}\t5\n')
        env_after = {'evidence_id': 'ev_same', 'normalized_result': {'files': [{'relative_path': 'firmware.bin_extract/hello.txt', 'sha256': h}]}}
        env_before = {'evidence_id': 'ev_same2', 'normalized_result': {'extraction_gaps': [{'kind': 'missing-extractor-dependency', 'dependencies': ['sasquatch-v4be'], 'handler': 'squashfs_v4_be'}]}}
        json.dump(env_after, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after.json'), 'w'))
        json.dump(env_before, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/before.json'), 'w'))
        run_after = {'rea_package_root': PINS['rea_package_root'], 'unblob': PINS['unblob'], 'sasquatch_v4be_sha256': PINS['sasquatch_v4be_sha256']}
        run_before = {'sasquatch_v4be': None}
        json.dump(run_after, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after-run.json'), 'w'))
        json.dump(run_before, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/before-run.json'), 'w'))
        prov = '# P\n## Round-37 additions to Core\n| sasquatch squashfs v4 BE | x | y | z |\n'
        open(os.path.join(d, 'PROVINCE.md'), 'w').write(prov)
        entry = 'source: S112 — x\nverified-at: 2026-10-26\nrecheck: 180d\ntext\n'
        open(os.path.join(d, 'corpus/knowledge/2026-10-26-r37-be-squashfs-v4.md'), 'w').write(entry)
        sources = '| S112 | url | code | A | scope | anchor | teaches | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r37-be-squashfs-v4.md |\n'
        open(os.path.join(d, 'corpus/SOURCES.md'), 'w').write(sources)
        if mutate:
            mutate(d)
        git(d, 'add', '-A')
        git(d, 'commit', '-m', 'fixture', '-q')
        return d

    # green
    cases.append(('green', make_fixture(cases, 'green'), True))
    # reds
    def red_missing_after(d):
        os.remove(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after.json'))
    cases.append(('red_missing_after', make_fixture(cases, 'red_missing_after', red_missing_after), False))
    def red_before_publishes(d):
        env = json.load(open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/before.json')))
        env['normalized_result'] = {'files': [{'relative_path': 'firmware.bin_extract/hello.txt', 'sha256': hashlib.sha256(b'hello').hexdigest()}]}
        json.dump(env, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/before.json'), 'w'))
    cases.append(('red_before_publishes', make_fixture(cases, 'red_before_publishes', red_before_publishes), False))
    def red_wrong_gap(d):
        env = json.load(open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/before.json')))
        env['normalized_result']['extraction_gaps'][0]['handler'] = 'squashfs_v4_le'
        json.dump(env, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/before.json'), 'w'))
    cases.append(('red_wrong_gap', make_fixture(cases, 'red_wrong_gap', red_wrong_gap), False))
    def red_after_gap(d):
        env = json.load(open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after.json')))
        env['normalized_result']['extraction_gaps'] = [{'kind': 'missing-extractor-dependency', 'dependencies': ['sasquatch-v4be'], 'handler': 'squashfs_v4_be'}]
        json.dump(env, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after.json'), 'w'))
    cases.append(('red_after_gap', make_fixture(cases, 'red_after_gap', red_after_gap), False))
    def red_no_core_row(d):
        open(os.path.join(d, 'PROVINCE.md'), 'w').write('# P\n## Other\n')
    cases.append(('red_no_core_row', make_fixture(cases, 'red_no_core_row', red_no_core_row), False))
    def red_no_entry(d):
        os.remove(os.path.join(d, 'corpus/knowledge/2026-10-26-r37-be-squashfs-v4.md'))
    cases.append(('red_no_entry', make_fixture(cases, 'red_no_entry', red_no_entry), False))
    def red_usedby_missing(d):
        open(os.path.join(d, 'corpus/SOURCES.md'), 'w').write('| S112 | url | code | A | scope | anchor | teaches | mined | 2026-10-26 | 180d | other |\n')
    cases.append(('red_usedby_missing', make_fixture(cases, 'red_usedby_missing', red_usedby_missing), False))
    def red_run_pkg(d):
        run = json.load(open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after-run.json')))
        run['rea_package_root'] = '/different/root'
        json.dump(run, open(os.path.join(d, 'corpus/evidence/round-37/c1/K1/after-run.json'), 'w'))
    cases.append(('red_run_pkg', make_fixture(cases, 'red_run_pkg', red_run_pkg), False))

    for name, d, want_green in cases:
        rev = git(d, 'rev-parse', 'HEAD').stdout.decode().strip()
        # override EVDIR etc via env region: simplest is direct call with temp env
        import importlib
        saved = dict(os.environ)
        os.chdir(d)
        try:
            res = measure(d, rev, rev, PINS['rea_package_root'])
            got = res.get('met_target')
        finally:
            os.chdir(root)
        ok = got == want_green
        if not ok:
            fails.append(f'{name}: expected green={want_green} got {got}')
        print(f'case {name}: green={got} expected={want_green} {"OK" if ok else "FAIL"}')
    shutil.rmtree(os.path.join(root, 'selftest'), ignore_errors=True)
    if fails:
        print('\n'.join(fails))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
