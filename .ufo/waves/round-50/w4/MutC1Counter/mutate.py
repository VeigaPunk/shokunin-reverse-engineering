#!/usr/bin/env python3
"""Build the C1 gap-rule mutants from the frozen counter bytes.

Three independent mutants, each changing exactly ONE behaviour-bearing point:

  M1  code: a `char-device` non-regular entry is not REQUIRED to carry a
      disposition (the frozen `required` map's char-device:true is ignored for
      this kind).
  M2  code: a `char-device` entry with no disposition is admitted SILENTLY
      (the frozen `removed.silent.char-device` list is widened to any detail).
  M3  data: the frozen `tools/round-50/gap-rule.json` sets
      `required.char-device = false` (the rule file, not the counter).

M1/M2 mutate the counter bytes; M3 mutates the frozen rule document.
Nothing here writes to the lane tree.
"""
import difflib
import hashlib
import json
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(S, 'c1-counter-frozen.py')

# ---- M1: char-device entries are not required --------------------------
M1_OLD = """    for rel, kind, detail in nonreg:
        need = required.get(kind, bool(allowed.get(kind)))
        if not need:
            continue
"""
M1_NEW = """    for rel, kind, detail in nonreg:
        need = required.get(kind, bool(allowed.get(kind)))
        if kind == 'char-device':
            need = False
        if not need:
            continue
"""

# ---- M2: any char-device detail is admitted silently ------------------
M2_OLD = """        allowed_details = (removed.get('silent') or {}).get(kind)
        if allowed_details and silent_detail_matches(detail, allowed_details):
"""
M2_NEW = """        allowed_details = (removed.get('silent') or {}).get(kind)
        if kind == 'char-device':
            silent_admitted.append(rel)
            continue
        if allowed_details and silent_detail_matches(detail, allowed_details):
"""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    base = open(FROZEN, 'rb').read()
    out = {}

    m1 = base.decode().replace(M1_OLD, M1_NEW)
    assert m1.count(M1_NEW) == 1, 'M1 anchor not unique'
    m1b = m1.encode()
    open(os.path.join(S, 'c1-counter-M1.py'), 'wb').write(m1b)
    out['M1'] = {
        'file': 'c1-counter-M1.py',
        'sha256': sha(m1b),
        'frozen_sha256': sha(base),
        'diff': ''.join(difflib.unified_diff(
            base.decode().splitlines(True), m1.splitlines(True),
            fromfile='c1-counter.py@435d41fd', tofile='c1-counter-M1.py')),
    }

    m2 = base.decode().replace(M2_OLD, M2_NEW)
    assert m2.count(M2_NEW) == 1, 'M2 anchor not unique'
    m2b = m2.encode()
    open(os.path.join(S, 'c1-counter-M2.py'), 'wb').write(m2b)
    out['M2'] = {
        'file': 'c1-counter-M2.py',
        'sha256': sha(m2b),
        'frozen_sha256': sha(base),
        'diff': ''.join(difflib.unified_diff(
            base.decode().splitlines(True), m2.splitlines(True),
            fromfile='c1-counter.py@435d41fd', tofile='c1-counter-M2.py')),
    }

    # ---- M3: the frozen rule document, required.char-device -> false ----
    rule = json.load(open(os.path.join(S, 'gap-rule-frozen.json')))
    rule['required']['char-device'] = False
    m3 = json.dumps(rule, indent=1) + '\n'
    m3b = m3.encode()
    open(os.path.join(S, 'gap-rule-M3.json'), 'wb').write(m3b)
    out['M3'] = {
        'file': 'gap-rule-M3.json',
        'sha256': sha(m3b),
        'diff': ''.join(difflib.unified_diff(
            (json.dumps(json.load(open(os.path.join(S, 'gap-rule-frozen.json'))),
                        indent=1) + '\n').splitlines(True),
            m3.splitlines(True),
            fromfile='gap-rule.json@435d41fd', tofile='gap-rule-M3.json')),
    }

    # the pristine copy: byte-identical to the frozen counter
    open(os.path.join(S, 'c1-counter-pristine.py'), 'wb').write(base)
    out['pristine'] = {'file': 'c1-counter-pristine.py', 'sha256': sha(base),
                       'frozen_sha256': sha(base), 'diff': ''}

    open(os.path.join(S, 'mutants.json'), 'w').write(json.dumps(out, indent=1))
    for k, v in out.items():
        print('%-9s %s  %s' % (k, v['sha256'], v['file']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
