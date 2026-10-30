#!/usr/bin/env python3
"""Mutation probe: inject one plausible defect into the frozen round-50
counter's disposition semantics (in a SCRATCH COPY only) and observe which of
the round-52 claimed controls would fire.

The defect (M-DEFECT-1): the counter treats an EMPTY `allowed` list for a kind as
"kind not present" and falls back to the round-50 default
`required.get(kind, bool(allowed.get(kind)))` -> False.  A v2 counter that
copies this default instead of honouring an explicit `required['char-device']=false`
would silently DISABLE the law's fail-closed clause: a gap landing on a device
row would no longer be a violation of `allowed[char-device] == []`.

We mutate the scratch copy so that the empty-list case is treated as
"allowed for every gap kind", and we compare pristine vs mutated vs restored.

Detector: the round-52 claimed control set, each arm scored with the SAME
offline disposition probe.
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCRATCH = os.path.dirname(os.path.abspath(__file__))
IDS = ('c6430', 'c6490', 'g7581', 'g7582')
PRISTINE = os.path.join(LANE, 'tools/round-50/c1-counter.py')
MUTANT = os.path.join(SCRATCH, 'mutant-counter.py')

LAW = {
    'claim': 'R52-C1',
    'allowed': {'symlink': ['unpublished-entry'], 'char-device': [],
                'block-device': [], 'fifo': [], 'socket': [], 'dir': []},
    'required': {'symlink': True, 'char-device': False, 'block-device': False,
                 'fifo': False, 'socket': False, 'dir': False},
    'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                'disposition': 'exclusive', 'silent': {}},
    'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},
}


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def build_state():
    raw = {cid: open(os.path.join(
        LANE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid), 'rb').read()
        for cid in IDS}
    env = {cid: json.load(open(os.path.join(
        LANE, 'corpus/evidence/round-50/c1/%s/after.json' % cid)))
        for cid in IDS}
    return raw, env


def run_all(counter_path, tag):
    M = load(counter_path, 'm_' + tag)
    raw, env = build_state()
    nonreg = {}
    for cid in IDS:
        rows, err = M.parse_nonregular(raw[cid])
        assert err is None, err
        nonreg[cid] = rows
    R50 = json.load(open(os.path.join(LANE, 'tools/round-50/gap-rule.json')))
    dev_details = sorted({r[2] for r in nonreg['g7581'] if r[1] == 'char-device'})
    m1 = copy.deepcopy(LAW)
    m1['removed']['silent'] = {'char-device': dev_details}
    m1['required']['char-device'] = True
    m1['allowed']['char-device'] = ['unpublished-entry']
    fourteenth = [('dev/ttyS0', 'char-device', '4:64')]

    def score(rule, over=None, gaps_extra=None):
        model, _ = M.gap_rule_model(json.dumps(rule).encode())
        green = 0
        for cid in IDS:
            rows = nonreg[cid] + (over or [])
            e = env[cid]
            g = list((e.get('normalized_result') or {}).get('extraction_gaps') or [])
            if gaps_extra and cid in gaps_extra:
                g = g + gaps_extra[cid]
            root, _ = M.subject_root(e, None)
            od = (e.get('parameters') or {}).get('output_directory')
            ok, _why = M.disposition_check(g, M.diagnostics(e), rows, model, root, od)
            esc = M.nonregular_published(M.published(e), rows, root)
            green += bool(ok and root is not None and not esc)
        return green

    def device_gap(cid):
        e = copy.deepcopy(env[cid])
        rel = [r[0] for r in nonreg[cid] if r[1] == 'char-device'][0]
        return [{'kind': 'unpublished-entry',
                 'input_path': '$output/firmware.bin_extract/' + rel,
                 'relative_path': 'firmware.bin_extract/' + rel,
                 'handler': None, 'provider_id': None, 'range': None,
                 'root_file_range': None, 'dependencies': [],
                 'continuation_id': 'probe-device-gap'}]

    dg = {cid: device_gap(cid) for cid in IDS}
    junk = copy.deepcopy(LAW)
    junk['allowed'] = {k: ['no-such-gap-kind'] for k in LAW['allowed']}
    junk['required'] = {k: True for k in LAW['required']}
    return {
        'CTL-OLD': score(R50),
        'CTL-NEW': score(LAW),
        'M1': score(m1),
        'CTL-JUNK': score(junk),
        'M2law': score(LAW, over=fourteenth),
        'M2white': score(m1, over=fourteenth),
        'DEVGAP': score(LAW, gaps_extra=dg),
    }


# EXPECT is the EXPECTED disposition-verdict count for each arm.
# NOTE: M1 is expected RED *by the frozen rule-shape clause law_shape_ok*
# (a rule-shape check), not by the disposition logic -- so under the
# round-50 disposition logic alone M1 is 4/4 GREEN.  That is reported as a
# separate fact, not as a survivor.
EXPECT = {'CTL-OLD': 2, 'CTL-NEW': 4, 'M1': 4, 'CTL-JUNK': 0, 'M2law': 4,
          'M2white': 0, 'DEVGAP': 0}

results = {}

print('=== pristine ===')
results['pristine'] = run_all(PRISTINE, 'pristine')
for k, v in results['pristine'].items():
    print('  %-9s %d/4  expected %d  %s'
          % (k, v, EXPECT[k], 'OK' if v == EXPECT[k] else 'MISMATCH'))

src = open(PRISTINE, 'r', encoding='utf-8').read()
NEEDLE = """        if kind not in allowed.get(entry_kind, []):
            return False, 'gap kind %r not allowed for %r entry %r (allowed %r)' % (
                kind, entry_kind, hits[0], allowed.get(entry_kind, []))"""
REPL = """        _allowed_for_kind = allowed.get(entry_kind, [])
        if not _allowed_for_kind:
            _allowed_for_kind = ['*']
        if kind not in _allowed_for_kind and '*' not in _allowed_for_kind:
            return False, 'gap kind %r not allowed for %r entry %r (allowed %r)' % (
                kind, entry_kind, hits[0], allowed.get(entry_kind, []))"""
if NEEDLE not in src:
    print('MUTATION NOT APPLIED: needle not found')
    sys.exit(2)
mut_src = src.replace(NEEDLE, REPL, 1)
open(MUTANT, 'w', encoding='utf-8').write(mut_src)
os.chmod(MUTANT, 0o755)

print('\n=== mutant (M-DEFECT-1: empty allowed[] treated as allow-all) ===')
results['mutant'] = run_all(MUTANT, 'mutant')
for k, v in results['mutant'].items():
    print('  %-9s %d/4  expected %d  %s'
          % (k, v, EXPECT[k], 'OK' if v == EXPECT[k] else 'MISMATCH'))

print('\n=== restored (lane file untouched; re-read pristine) ===')
results['pristine_sha'] = sha(PRISTINE)
results['mutant_sha'] = sha(MUTANT)
print('  lane counter sha256 now      :', results['pristine_sha'])
results['restored'] = run_all(PRISTINE, 'restored')
for k, v in results['restored'].items():
    print('  %-9s %d/4  expected %d  %s'
          % (k, v, EXPECT[k], 'OK' if v == EXPECT[k] else 'MISMATCH'))

print('\n=== SURVIVOR ANALYSIS ===')
# A control FIRES on the defect iff the mutant's verdict DIFFERS from the
# pristine verdict (i.e. the defect moves the arm's answer).  An arm whose
# verdict is unchanged is a DEAD control for this defect.
changed = [k for k in EXPECT if results['mutant'][k] != results['pristine'][k]]
unchanged = [k for k in EXPECT if k not in changed]
print('  arms that FIRE on the defect (verdict changed):')
for k in changed:
    print('    %-9s pristine=%d -> mutant=%d' %
          (k, results['pristine'][k], results['mutant'][k]))
print('  arms whose verdict is UNCHANGED by the defect (DEAD for it):')
for k in unchanged:
    print('    %-9s pristine=%d -> mutant=%d' %
          (k, results['pristine'][k], results['mutant'][k]))
survivors = unchanged

json.dump({'expectations': EXPECT,
           'pristine': results['pristine'],
           'mutant': results['mutant'],
           'restored': results['restored'],
           'pristine_sha256': results['pristine_sha'],
           'mutant_sha256': results['mutant_sha'],
           'surviving_arms': survivors},
          open(os.path.join(SCRATCH, 'mutation-probe.json'), 'w'), indent=2)
print('\njson: %s' % os.path.join(SCRATCH, 'mutation-probe.json'))
