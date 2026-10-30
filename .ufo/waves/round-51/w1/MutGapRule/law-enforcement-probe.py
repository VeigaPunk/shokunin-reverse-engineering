#!/usr/bin/env python3
"""R51-C1 attack probes against the round-51 gap-rule draft (offline, no REA).

Seat: MutGapRule (kaidoku round 51, wave 1).  Two falsifiable probes against the
law-derived rule family, computed from the committed round-50 receipts and the
frozen oracle tables.

PROBE A (law enforcement): the law says a char-device oracle entry carries NO
disposition at all.  A rule therefore must be RED when a receipt DOES report a
gap for a device row (that is the producer behaving against the law).  Probe:
synthetically add one `unpublished-entry` gap for `dev/led` (the one char-device
every carrier has) to each carrier's gap list and score the rule family.

PROBE B (claim-string binding): the counter's `gap_rule_ok` binding is
`not plan_probs and not uncovered`, and `gap_rule_model` rejects any rule whose
`claim` field is not the round-50 claim string.  A round-51 rule that carries
`"claim": "R51-C1"` therefore makes the binding FALSE (a counter exit 1 with
four carriers matched).  Probe: score `gap_rule_ok` for the round-51 rule under
the v1 and v2-draft counters' own `gap_rule_model` and `carriers_spec`.

Exit codes: 0 every probe behaved as declared; 1 a probe misbehaved; 2 could
not evaluate.
"""
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab'
IDS = ('c6430', 'c6490', 'g7581', 'g7582')
V1 = os.path.join(LANE, 'tools/round-50/c1-counter.py')
V2DRAFT = os.path.join(LANE, '.ufo/waves/round-51/w1/ExecCounterV2/c1-counter.py')
DRAFT_RULE = os.path.join(LANE, '.ufo/waves/round-51/w1/ExecRuleDerive/gap-rule-v2.json')

STRICT = {
    'claim': 'R51-C1',
    'allowed': {
        'symlink': ['unpublished-entry'],
        'char-device': [],
        'block-device': [],
        'fifo': [],
        'socket': [],
        'dir': [],
    },
    'required': {
        'symlink': True,
        'char-device': False,
        'block-device': False,
        'fifo': False,
        'socket': False,
        'dir': False,
    },
    'removed': {
        'diagnostic': 'MaliciousSymlinkRemoved',
        'kinds': ['symlink'],
        'disposition': 'exclusive',
        'silent': {},
    },
    'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},
}


def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (rev, path)],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit('git show failed: ' + path)
    return p.stdout


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_nonregular(raw):
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = line.split('\t')
        if (f[0], f[1]) == ('relative_path', 'kind'):
            continue
        rows.append((f[0], f[1], f[2] if len(f) > 2 else None))
    return rows


def load_carrier(cid):
    env = json.loads(git_show(BASE, 'corpus/evidence/round-50/c1/%s/after.json' % cid))
    rows = parse_nonregular(git_show(BASE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid))
    nr = env.get('normalized_result') or {}
    root = None
    for d in (nr.get('derivations') or []):
        if isinstance(d, dict) and d.get('handler') == 'squashfs_v4_le':
            cp = d.get('child_path') or ''
            if cp.startswith('$output/'):
                cp = cp[len('$output/'):]
            root = cp.rstrip('/')
    params = env.get('parameters') or {}
    return {
        'id': cid,
        'gaps': [g for g in (nr.get('extraction_gaps') or []) if isinstance(g, dict)],
        'diags': [d for d in (nr.get('diagnostics') or []) if isinstance(d, dict)],
        'rows': rows,
        'root': root,
        'output_directory': params.get('output_directory'),
    }


def inject_device_gap(carrier):
    """A synthetic `unpublished-entry` gap for `dev/led` (a char-device row)."""
    c = copy.deepcopy(carrier)
    c['gaps'] = list(c['gaps']) + [{
        'kind': 'unpublished-entry',
        'input_path': '$output/firmware.bin_extract/dev/led',
        'relative_path': 'firmware.bin_extract/dev/led',
        'handler': None, 'provider_id': None, 'range': None,
        'root_file_range': None, 'dependencies': [], 'continuation_id': None,
    }]
    return c


def main(argv=None):
    out_path = argv[0] if argv else '/dev/stdout'
    c1 = load(V1, 'c1_v1')
    c2 = load(V2DRAFT, 'c1_v2draft')
    carriers = {cid: load_carrier(cid) for cid in IDS}
    draft_bytes = open(DRAFT_RULE, 'rb').read()
    draft = json.loads(draft_bytes)
    strict_bytes = json.dumps(STRICT, indent=2, sort_keys=True).encode()

    res = {
        'seat': 'MutGapRule',
        'generated_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'base_revision': BASE,
        'probe_a': {
            'question': 'does the rule go RED when a receipt reports a gap for a char-device row?',
            'law': 'a char-device/fifo/socket oracle entry carries no disposition at all',
            'rules': {},
        },
        'probe_b': {
            'question': "does the counter's gap_rule_ok binding hold for a round-51 rule?",
            'note': "gap_rule_ok = not plan_probs and not uncovered",
        },
        'findings': [],
    }

    # -------------------------------------------------------------- PROBE A
    for label, raw in (('sibling_draft_ExecRuleDerive_gap-rule-v2.json', draft_bytes),
                       ('strict_variant_device_kinds_admit_no_gap', strict_bytes)):
        entry = {'rule_sha256': hashlib.sha256(raw).hexdigest(), 'carriers': {}}
        for cid, carrier in carriers.items():
            _model, probs = c1.gap_rule_model(raw)
            clean_ok, clean_why = c1.disposition_check(
                carrier['gaps'], carrier['diags'], carrier['rows'],
                _model, carrier['root'], carrier['output_directory'])
            mutated = inject_device_gap(carrier)
            mut_ok, mut_why = c1.disposition_check(
                mutated['gaps'], mutated['diags'], mutated['rows'],
                _model, mutated['root'], mutated['output_directory'])
            entry['carriers'][cid] = {
                'clean_verdict': 'green' if clean_ok else 'red',
                'device_gap_verdict': 'green' if mut_ok else 'red',
                'law_enforced': (not mut_ok),
                'device_gap_note': mut_why,
                'rule_model_problems': probs,
            }
        res['probe_a']['rules'][label] = entry

    for label, entry in res['probe_a']['rules'].items():
        leaks = [cid for cid, v in entry['carriers'].items() if not v['law_enforced']]
        if leaks:
            res['findings'].append({
                'id': 'A-%s' % ('device-gap-accepted' if label.startswith('sibling') else 'strict-ok'),
                'severity': 'high' if label.startswith('sibling') else 'info',
                'finding': ('the rule %s goes GREEN on a receipt that reports a gap for a '
                            'char-device row; the law says a device row carries no '
                            'disposition at all, so the rule does not enforce the law'
                            % label),
                'carriers_where_green': leaks,
                'evidence': 'probe_a.rules.%s' % label,
            })

    # -------------------------------------------------------------- PROBE B
    for label, mod, path in (('v1_round-50-counter', c1, V1),
                             ('v2_draft_ExecCounterV2', c2, V2DRAFT)):
        model, probs = mod.gap_rule_model(draft_bytes)
        kinds_seen = set()
        for carrier in carriers.values():
            kinds_seen |= {k for _r, k, _d in carrier['rows']}
        uncovered = sorted(kinds_seen - set(model.get('allowed') or {}))
        gap_rule_ok = (not probs) and (not uncovered)
        spec = json.loads(git_show(BASE, 'tools/round-50/carriers.json').decode())
        spec['claim'] = 'R51-C1'
        _ids, spec_probs = mod.carriers_spec(spec, 4, IDS)
        res['probe_b'][label] = {
            'counter_path': path,
            'counter_sha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
            'gap_rule_problems': probs,
            'gap_rule_uncovered_kinds': uncovered,
            'gap_rule_ok': gap_rule_ok,
            'carriers_spec_problems': spec_probs,
            'carriers_spec_ok': not spec_probs,
        }
        if not gap_rule_ok:
            res['findings'].append({
                'id': 'B-claim-string-binding',
                'severity': 'high',
                'finding': ("the counter's gap_rule_ok binding is FALSE for the round-51 "
                            "rule: gap_rule_model rejects the rule's `claim` field because "
                            "the counter still hardcodes the round-50 claim string, so the "
                            "predicate would exit 1 with carriers_matched 4 and every "
                            "binding but gap_rule_ok true"),
                'counter': label,
                'gap_rule_problems': probs,
                'evidence': 'probe_b.%s' % label,
            })
        if spec_probs:
            res['findings'].append({
                'id': 'B-carriers-spec-claim',
                'severity': 'high',
                'finding': ("the counter's carriers_spec_ok binding is FALSE for a round-51 "
                            "carriers.json: carriers_spec rejects a `claim` field that is "
                            "not the round-50 claim string"),
                'counter': label,
                'carriers_spec_problems': spec_probs,
                'evidence': 'probe_b.%s' % label,
            })

    res['exit_code'] = 1 if any(f.get('severity') == 'high' for f in res['findings']) else 0
    with open(out_path, 'w') as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
        fh.write('\n')
    return res['exit_code']


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
