#!/usr/bin/env python3
"""Independent recomputation of combo_unseen_majority for round 43.

Re-derived from the frozen plan text (P43-C1):
  UNSEEN = the combo's OBSERVED six-field tuple (handler_set, gap_kinds,
  gap_dependencies, be_argv, symlink_removed, published) is outside the union
  of the NAMED-class DECLARED tuples in the frozen round-42 dev-arm manifest.
  Binding: len(unseen) >= ceil(n_combos/2).

Primary recomputation is standalone; a later reference cross-check imports the counter's helpers. All bytes read from the committed worktree.
"""
import json, re, shlex, hashlib, sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FEATS = ('handler_set', 'gap_kinds', 'gap_dependencies',
         'be_argv', 'symlink_removed', 'published')

ALIASES = {
    'h': 'handler_set', 'handlers': 'handler_set', 'handler': 'handler_set',
    'handler_set': 'handler_set',
    'g': 'gap_kinds', 'gaps': 'gap_kinds', 'gap_kinds': 'gap_kinds',
    'gap kinds': 'gap_kinds',
    'd': 'gap_dependencies', 'deps': 'gap_dependencies',
    'dependencies': 'gap_dependencies', 'gap_dependencies': 'gap_dependencies',
    'be': 'be_argv', 'be_argv': 'be_argv', '-be in child argv': 'be_argv',
    'sr': 'symlink_removed', 'symlink_removed': 'symlink_removed',
    'symlink removed': 'symlink_removed',
    'p': 'published', 'published': 'published', 'published files': 'published',
    'files': 'published',
}
SYMLINK_TN = 'MaliciousSymlinkRemoved'

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

def toks(value):
    if isinstance(value, str):
        return sorted(t.strip() for t in re.split(r'[,+]', value)
                      if t.strip() and t.strip().lower() != 'none')
    if isinstance(value, (list, tuple, set)):
        return sorted(str(t) for t in value if str(t).strip())
    return []

def tri(value):
    if value is None:
        return 'n/a'
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ('yes', 'true', 'y', 'removed', '1'):
            return 'yes'
        if v in ('no', 'false', 'n', 'kept', '0'):
            return 'no'
        if v in ('n/a', 'na', 'n-a', 'none', '-', ''):
            return 'n/a'
    return 'n/a'

def pub(value):
    if isinstance(value, bool):
        return 'nonzero' if value else 'zero'
    if isinstance(value, int):
        return 'nonzero' if value > 0 else 'zero'
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ('>0', 'nonzero', 'non-zero', 'some', 'positive', 'yes', 'true'):
            return 'nonzero'
        if v in ('0', 'zero', 'none', 'empty', 'no', 'false'):
            return 'zero'
    return 'zero'

def canon_declared(obj):
    """Canonical six-field tuple from a manifest declared_features dict."""
    if not isinstance(obj, dict):
        return None
    out = {}
    for key, value in obj.items():
        k = ALIASES.get(str(key).strip().lower())
        if k is None:
            continue
        if k in ('handler_set', 'gap_kinds', 'gap_dependencies'):
            out[k] = toks(value)
        elif k == 'be_argv':
            out[k] = tri(value)
        elif k == 'symlink_removed':
            out[k] = tri(value) == 'yes'
        elif k == 'published':
            out[k] = pub(value)
    return out or None

def names_sasquatch(tokens):
    return any(t.rsplit('/', 1)[-1].startswith('sasquatch') for t in tokens)

def cmd_tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None

def extractor_commands(data):
    cmds = []
    def take(cmd):
        t = cmd_tokens(cmd)
        if t and names_sasquatch(t) and cmd not in cmds:
            cmds.append(cmd)
    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in as_list(source):
            rep = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(rep, dict) and 'command' in rep:
                take(rep['command'])
    for found in iter_dicts(data.get('raw_result')):
        if 'command' in found:
            take(found['command'])
    return cmds

def observed(data):
    """Six-field observed tuple from an envelope data object."""
    if not isinstance(data, dict):
        return None
    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    handlers = set()
    gap_kinds = set()
    deps = set()
    for chunk in as_list(nr.get('chunks')):
        if isinstance(chunk, dict):
            h = chunk.get('handler')
            if isinstance(h, str) and h:
                handlers.add(h)
    for gap in as_list(nr.get('extraction_gaps')):
        if isinstance(gap, dict):
            k = gap.get('kind')
            if isinstance(k, str):
                gap_kinds.add(k)
            gh = gap.get('handler')
            if isinstance(gh, str) and gh:
                handlers.add(gh)
            for dep in as_list(gap.get('dependencies')):
                if isinstance(dep, str):
                    deps.add(dep)
    cmds = extractor_commands(data)
    if not cmds:
        be = 'n/a'
    else:
        be = 'no'
        for cmd in cmds:
            if '-be' in (cmd_tokens(cmd) or []):
                be = 'yes'
                break
    symlink = 'no'
    for diag in as_list(nr.get('diagnostics')):
        rep = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(rep, dict) and rep.get('__typename__') == SYMLINK_TN:
            symlink = 'yes'
            break
    if symlink == 'no':
        for found in iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK_TN:
                symlink = 'yes'
                break
    return {
        'handler_set': sorted(handlers),
        'gap_kinds': sorted(gap_kinds),
        'gap_dependencies': sorted(deps),
        'be_argv': be,
        'symlink_removed': symlink == 'yes',
        'published': 'nonzero' if as_list(nr.get('files')) else 'zero',
    }

def tkey(can):
    return tuple((k, json.dumps(can.get(k), sort_keys=True)) for k in FEATS)

def envelope_data(obj):
    if isinstance(obj, dict) and 'subject' not in obj \
            and isinstance(obj.get('data'), dict):
        return obj['data']
    return obj

# ---- 1. dev-arm named-class declared union (round-42 dev manifest)
with open(LANE + '/corpus/evidence/round-42/c2/dev/manifest.json', 'rb') as fh:
    dev_bytes = fh.read()
dev = json.loads(dev_bytes.decode())
dev_sha = hashlib.sha256(dev_bytes).hexdigest()

dev_named, dev_combo, dev_none_class, dev_ood_empty = [], [], [], []
for c in dev.get('carriers') or []:
    if not isinstance(c, dict):
        continue
    cls = c.get('class')
    if str(cls) == 'combo':
        dev_combo.append(c.get('id'))
        continue
    can = canon_declared(c.get('declared_features'))
    if can is None:
        if str(cls) == 'out-of-domain':
            dev_ood_empty.append(c.get('id'))
        else:
            dev_none_class.append(c.get('id'))
        continue
    dev_named.append((c.get('id'), can))

dev_tuples = {tkey(can) for _, can in dev_named}
print('== dev arm ==')
print('dev manifest sha256:', dev_sha)
print('n carriers:', len(dev.get('carriers') or []),
      'named-class carriers:', len(dev_named),
      'combos skipped:', len(dev_combo),
      'canon-None non-combo:', dev_none_class,
      'ood empty (canon None):', dev_ood_empty)
print('distinct named union tuples:', len(dev_tuples))

# ---- 2. round-43 held-out combo observed tuples from envelope bytes
with open(LANE + '/corpus/evidence/round-43/c1/heldout/manifest.json', 'rb') as fh:
    h43_bytes = fh.read()
h43 = json.loads(h43_bytes.decode())
combos = [c for c in h43['carriers'] if c.get('class') == 'combo']
print('\n== round-43 heldout ==')
print('heldout manifest sha256:', hashlib.sha256(h43_bytes).hexdigest())
print('seed:', h43.get('seed'))
print('n combos:', len(combos))

unseen, seen, skipped = [], [], []
per_combo = {}
for c in combos:
    cid = c['id']
    with open(LANE + '/corpus/evidence/round-43/c1/heldout/%s/envelope.json' % cid,
              'rb') as fh:
        env = json.loads(fh.read().decode())
    obs = observed(envelope_data(env))
    if obs is None:
        skipped.append(cid)
        continue
    per_combo[cid] = obs
    (seen if tkey(obs) in dev_tuples else unseen).append(cid)

need = (len(combos) + 1) // 2
binding = bool(dev_tuples) and len(unseen) >= need
print('unseen n=%d:' % len(unseen), unseen)
print('seen   n=%d:' % len(seen), seen)
print('skipped (obs None):', skipped)
print('need (ceil(n/2)):', need, ' binding len(unseen)>=need:', binding)

# ---- 3. cross-check vs the counter's own functions (reference only)
sys.path.insert(0, LANE + '/tools/round-43')
import importlib.util
spec = importlib.util.spec_from_file_location(
    'c1counter', LANE + '/tools/round-43/c1-counter.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

dev_tuples_ref = set()
for c in dev['carriers']:
    if not isinstance(c, dict) or str(c.get('class')) == 'combo':
        continue
    can = mod.declared_features(c)
    if can is not None:
        dev_tuples_ref.add(mod_tuple := tuple(
            (k, json.dumps(can.get(k), sort_keys=True)) for k in mod.REQUIRED_FEATURES))
print('\n== reference cross-check (counter functions) ==')
print('ref distinct named union:', len(dev_tuples_ref),
      ' equal to independent:', dev_tuples_ref == dev_tuples)

unseen_ref, seen_ref = [], []
for c in combos:
    with open(LANE + '/corpus/evidence/round-43/c1/heldout/%s/envelope.json' % c['id'],
              'rb') as fh:
        env = json.loads(fh.read().decode())
    obs = mod.observed_features(mod.envelope_data(env))
    k = tuple((kk, json.dumps(obs.get(kk), sort_keys=True)) for kk in mod.REQUIRED_FEATURES)
    (seen_ref if k in dev_tuples_ref else unseen_ref).append(c['id'])
print('ref unseen == independent unseen:', unseen_ref == unseen)
print('ref seen   == independent seen  :', seen_ref == seen)

# ---- 4. union-hash attempt (manifest carries a named_tuple_union_sha256)
candidates = {
    'sorted-json-tuples': json.dumps(sorted(json.dumps(list(t), sort_keys=True) for t in dev_tuples), sort_keys=True).encode(),
    'json-list-tuples': json.dumps([list(t) for t in sorted(dev_tuples)], sort_keys=True).encode(),
}
for name, blob in candidates.items():
    print('union-hash try %s: %s' % (name, hashlib.sha256(blob).hexdigest()))
print('manifest claims union sha256: da11f0ef5bcaa9aa10c707c1c171ef106960df3afb03520b001b261755c31da6')
