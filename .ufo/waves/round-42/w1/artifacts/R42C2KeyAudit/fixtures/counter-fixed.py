"""Fixed-pair counter fixture for key-audit.py (R41-CL1 shape).

Reads the single declared-tuple key `declared_features` -- the ONE key the
fixed generator writes.  Minimal on purpose: it exists to be GREEN under
key-audit.py.
"""


def measure(man, carriers, env_objs):
    res = {'bindings': {}}
    b = res['bindings']
    feat_missing = []
    for c in carriers:
        decl = c.get('declared_features')
        canon = dict(decl) if isinstance(decl, dict) else None
        if canon is None:
            feat_missing.append(c.get('id'))
            continue
    b['observed_features_match_declared'] = not feat_missing
    return res
