#!/usr/bin/env python3
"""Repro harness for seat R40W2C2InterpMutants (round 40 wave 2).

Regenerates the 32 single-logic mutants of tools/round-40/sqfs-triage-v2.py in a
scratch dir, runs both detectors per mutant (selftest; 26 held-out envelopes under
SKILL.md), and reruns the survivor probes. Read-only against the lane.

Usage: python3 harness.py [LANE] [SCRATCH]      (defaults below)
"""
import json, os, shutil, subprocess, sys, hashlib, fnmatch
from concurrent.futures import ThreadPoolExecutor

LANE = sys.argv[1] if len(sys.argv) > 1 else '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = sys.argv[2] if len(sys.argv) > 2 else '/fast/scratch/hyaku/kaidoku-r40/R40W2C2InterpMutants'
os.makedirs(S, exist_ok=True)
os.environ['TMPDIR'] = S
os.environ['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'
SRC = LANE + '/tools/round-40/sqfs-triage-v2.py'
SKILL = LANE + '/SKILL.md'
HELD = LANE + '/corpus/evidence/round-40/c2/heldout'

src = open(SRC, encoding='utf-8').read()
print('lane tool sha256:', hashlib.sha256(src.encode()).hexdigest())

man = json.load(open(HELD + '/manifest.json'))
la = man['label_actions']
EXPECT = {c['id']: (c['label'], la[c['label']]) for c in man['carriers']}
envs = [os.path.join(HELD, i, 'envelope.json') for i in sorted(EXPECT)]
assert len(EXPECT) == 26

MUT = []
def m(mid, axis, desc, old, new):
    assert src.count(old) == 1, (mid, src.count(old))
    MUT.append((mid, axis, desc, old, new))

m('M01','domain-guard','operation guard compare inverted (!= -> ==)',
  "    if rule['operation'] != '*' and rule['operation'] != feat['OP']:",
  "    if rule['operation'] != '*' and rule['operation'] == feat['OP']:")
m('M02','domain-guard','provider guard compare inverted (!= -> ==)',
  "    if rule['provider'] != '*' and rule['provider'] != feat['PV']:",
  "    if rule['provider'] != '*' and rule['provider'] == feat['PV']:")
m('M03','domain-guard','operation guard dropped (compare and-ed with False)',
  "    if rule['operation'] != '*' and rule['operation'] != feat['OP']:",
  "    if rule['operation'] != '*' and False:")
m('M04','first-match-order','classify iterates reversed(rules)',
  "def classify(rules, feat):\n    for rule in rules:",
  "def classify(rules, feat):\n    for rule in reversed(rules):")
m('M05','first-match-order','marker search keeps scanning (last v2 marker wins)',
  "        if MARKER in lines[i]:\n            marker_line = i\n            break",
  "        if MARKER in lines[i]:\n            marker_line = i")
m('M06','set-equality','exact set compare weakened to subset (== -> <=)',
  "    return frozenset(values) == payload",
  "    return frozenset(values) <= payload")
m('M07','set-equality',"set cell 'none' accepts any values",
  "        return not values", "        return True")
m('M08','set-equality','exact set compare widened to superset (== -> >=)',
  "    return frozenset(values) == payload",
  "    return frozenset(values) >= payload")
m('M15','set-equality','set-cell repeated-member check disabled',
  "    if len(set(parts)) != len(parts):",
  "    if len(set(parts)) != len(parts) and False:")
m('M09','fnmatch','handler pattern match reduced to exact equality',
  "        if not any(fnmatch.fnmatchcase(value, payload) for value in feat['H']):",
  "        if not any(value == payload for value in feat['H']):")
m('M10','fnmatch','fnmatchcase -> case-insensitive fnmatch (normcase)',
  "        if not any(fnmatch.fnmatchcase(value, payload) for value in feat['H']):",
  "        if not any(fnmatch.fnmatch(value, payload) for value in feat['H']):")
m('M11','files-cell',"'published files >0' row admits P=0 (<=0 -> <0)",
  "    if files == '>0' and feat['P'] <= 0:",
  "    if files == '>0' and feat['P'] < 0:")
m('M12','files-cell',"'published files 0' row inverted (!=0 -> ==0)",
  "    if files == '0' and feat['P'] != 0:",
  "    if files == '0' and feat['P'] == 0:")
m('M13','handler-none',"'handler none' inverted (requires a handler)",
  "    if kind == 'none':\n        if feat['H']:\n            return False",
  "    if kind == 'none':\n        if not feat['H']:\n            return False")
m('M14','action-vocab','vocabulary membership check disabled',
  "        if action not in vocabulary:",
  "        if action not in vocabulary and False:")
m('M16','duplicate-label','duplicate-label check disabled',
  "        if label in labels:",
  "        if label in labels and False:")
m('M17','unclassified-default','DEFAULT_LABEL renamed',
  "DEFAULT_LABEL = 'unclassified'", "DEFAULT_LABEL = 'unknown'")
m('M18','unclassified-default','DEFAULT_ACTION renamed',
  "DEFAULT_ACTION = 'none'", "DEFAULT_ACTION = 'inspect-input'")
m('M19','unclassified-default','rule_matches final return True -> False',
  "    if files == '>0' and feat['P'] <= 0:\n        return False\n    return True",
  "    if files == '>0' and feat['P'] <= 0:\n        return False\n    return False")
m('M20','be-derivation','-be token test inverted (in -> not in)',
  "            if '-be' in (command_tokens(cmd) or []):",
  "            if '-be' not in (command_tokens(cmd) or []):")
m('M21','be-derivation','BE default when commands exist flipped no -> yes',
  "    else:\n        be = 'no'", "    else:\n        be = 'yes'")
m('M22','be-derivation',"names_sasquatch startswith -> exact 'sasquatch'",
  "        if token.rsplit('/', 1)[-1].startswith('sasquatch'):",
  "        if token.rsplit('/', 1)[-1] == 'sasquatch':")
m('M30','be-derivation','BE command sources drop normalized_result.diagnostics',
  "    for source in (nr.get('diagnostics'), data.get('diagnostics')):",
  "    for source in (data.get('diagnostics'),):")
m('M23','sr-derivation','SR diagnostics typename compare inverted (== -> !=)',
  "        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:",
  "        if isinstance(report, dict) and report.get('__typename__') != SYMLINK_TYPENAME:")
m('M24','sr-derivation','SR raw_result fallback disabled',
  "    if symlink == 'no':", "    if symlink == 'no' and False:")
m('M25','sr-derivation','SR raw_result typename compare inverted (== -> !=)',
  "            if found.get('__typename__') == SYMLINK_TYPENAME:",
  "            if found.get('__typename__') != SYMLINK_TYPENAME:")
m('M26','provider-derivation','string provider ignored (provider_id forced empty)',
  "    elif isinstance(provider, str):\n        provider_id = provider",
  "    elif isinstance(provider, str):\n        provider_id = ''")
m('M27','domain-guard',"domain '*' cell no longer accepted (** required)",
  "def _parse_domain_cell(cell, column, token_re):\n    if cell == '*':\n        return '*'",
  "def _parse_domain_cell(cell, column, token_re):\n    if cell == '**':\n        return '*'")
m('M28','actions-line','blank-line walk between vocabulary and table disabled',
  "    while actions_line > start and not lines[actions_line].strip():",
  "    while actions_line > start and not lines[actions_line].strip() and False:")
m('M29','actions-line','blank-line walk unbounded (skips prose too)',
  "    while actions_line > start and not lines[actions_line].strip():",
  "    while actions_line > start:")
m('M31','row-grammar','trailing pipe no longer stripped (extra empty cell per row)',
  "    if s.endswith('|'):\n        s = s[:-1]\n", "")
m('M32','h-derivation',"H collects only handlers exactly 'squashfs' (startswith dropped)",
  "        if isinstance(handler, str) and handler.startswith('squashfs'):",
  "        if isinstance(handler, str) and handler == 'squashfs':")

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                          env={**os.environ}, cwd=S)

def selftest_detector(path):
    r = run(['python3', '-I', '-B', path, '--selftest'])
    fails = sorted({l.split()[1] for l in r.stdout.splitlines() if l.startswith('FAIL ')})
    return {'exit': r.returncode, 'fails': fails}

def heldout_detector(path, skill=SKILL):
    r = run(['python3', '-I', '-B', path, '--skill', skill, *envs])
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    wrong = []
    for e in envs:
        eid = os.path.basename(os.path.dirname(e))
        want = EXPECT[eid]; got = None
        for l in lines:
            if l.split('\t')[0] == e:
                p = l.split('\t'); got = (p[1], p[2]); break
        if got != want:
            wrong.append(eid)
    return {'exit': r.returncode, 'wrong': sorted(wrong),
            'killed': bool(wrong) or r.returncode != 0}

shutil.copyfile(SRC, S + '/pristine.py')
print('baseline selftest:', selftest_detector(S + '/pristine.py'))
print('baseline heldout:', heldout_detector(S + '/pristine.py'))

os.makedirs(S + '/mutants', exist_ok=True)
def evaluate(mut):
    mid, axis, desc, old, new = mut
    path = S + '/mutants/%s.py' % mid
    open(path, 'w', encoding='utf-8').write(src.replace(old, new, 1))
    return mid, axis, desc, selftest_detector(path), heldout_detector(path)

results = []
with ThreadPoolExecutor(max_workers=4) as ex:
    results = list(ex.map(evaluate, MUT))
for mid, axis, desc, st, ho in results:
    print('%-4s %-22s ST=%-4s HO=%-4s %s' % (
        mid, axis, 'KILL' if st['exit'] else 'surv', 'KILL' if ho['killed'] else 'surv',
        ('st:' + ','.join(st['fails'][:3]) + ' ' if st['exit'] else '')
        + ('ho:' + ','.join(ho['wrong'][:4]) if ho['killed'] else '')))
json.dump({'expect': {k: list(v) for k, v in EXPECT.items()},
           'mutants': [{'id': mid, 'axis': axis, 'desc': desc, 'selftest': st,
                        'heldout': ho} for mid, axis, desc, st, ho in results]},
          open(S + '/results.json', 'w'), indent=1)
