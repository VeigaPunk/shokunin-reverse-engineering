#!/usr/bin/env python3
"""R40-C2 counter (depth: SquashFS extract-firmware outcome-triage table v2).

Predicate P40-C2 (draft; the same sentence as plans/round-40-claims.md):
  At the measured revision, the frozen interpreter
  `tools/round-40/sqfs-triage-v2.py` — materialised from the *freeze* commit —
  reading `SKILL.md` at the measured revision and therefore only the
  `<!-- sqfs-triage-table v2 -->` block, assigns every held-out envelope the
  (label, action) pair its frozen generator assigned before any REA run, for
  all N held-out envelopes (2 per class); the seed is the freeze commit hash,
  every carrier regenerates byte-identically from that seed with the frozen
  `tools/round-40/heldout-gen-v2.py`, every envelope's subject digest equals
  its carrier's sha256, the held-out manifest is first added in a commit
  descending from the freeze and no later than its envelopes, the v2 table
  block bytes at the measured revision equal the freeze bytes, the rule block
  18 (v1) table bytes equal the pre-v2 (base) bytes, and the counter reports
  the number of distinct row decisions.

Target: matched == N and every binding true.

Usage
  c2-counter.py --root LANE --rev REV --freeze FREEZE [--json-out PATH]
                 [--base COMMIT]
  c2-counter.py --selftest
Exit
  0  target met (met_target true)
  1  not met (labels/actions or a binding false), receipt still written
  2  unevaluable: freeze integrity or a structural prerequisite —
     `frozen_path_changed`, `freeze_not_ancestor_of_rev`, `unknown_revision`,
     `no_manifest_at_rev`, `manifest_unparsable`, `manifest_not_an_object`,
     `generator_absent_at_freeze`, `generator_failed`,
     `generator_wrote_no_manifest`, `regenerated_manifest_unparsable`,
     `interpreter_failed` (both the JSON and the tab interface failed),
     `met_target_inconsistent`
The JSON receipt always records the counter's own exit code (`exit_code`), so
a re-minted receipt cannot claim a result the run did not produce (R39-CL6).

Base (rule block 18 / table v1 invariance)
  `--base` pins the pre-round-40 commit.  Without it the base is derived from
  history: the newest commit at or below FREEZE whose `SKILL.md` has no v2
  marker and does carry the v1 block (else simply the newest without the v2
  marker).  Derivation keeps the check independent of any hard-coded sha.

Frozen interpreter interface (contract this counter relies on)
  `python3 -I -B sqfs-triage-v2.py --skill SKILL.md [--json] [--table-only] ENV...`
    exit 0 on success; `--json` writes one JSON object with
    `results: [{path, label, action, rule|row_index, row}]`; without `--json`
    it writes one line per envelope: `path<TAB>label<TAB>action[<TAB>row]`.
    `--table-only` prints the rule list as `INDEX. label` lines or as
    `{"rules": [{index, label}, ...]}`.  Row indices are what
    `distinct_decisions` counts; when neither interface reports them the
    `decisions_reported` binding is false (exit 1), never silently 0.

Reads git objects only (`git show`/`log`/`ls-tree`/`merge-base`); every object
is materialised into a private scratch directory under
$HYAKU_SCRATCH/kaidoku-r40 (or the system temp dir) and removed at exit.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

MANIFEST = 'corpus/evidence/round-40/c2/heldout/manifest.json'
NOMATCH_PAIR = ('unclassified', 'none')
SKILL = 'SKILL.md'
INTERP = 'tools/round-40/sqfs-triage-v2.py'
GEN = 'tools/round-40/heldout-gen-v2.py'
COUNTER = 'tools/round-40/c2-counter.py'
CLAIMS = 'plans/round-40-claims.md'
FROZEN = (INTERP, GEN, COUNTER, CLAIMS)
MARKER_V1 = '<!-- sqfs-triage-table v1 -->'
MARKER_V2 = '<!-- sqfs-triage-table v2 -->'
CRAFT = '## Queue-drain craft'
V2_COLUMNS = ('label', 'operation', 'provider', 'action')
GEN_TREE_PREFIXES = ('tools/round-40', 'tools/round-39')  # L1 freeze fix: the generator's writer is round-39's
WRITER_ENV = 'KAIDOKU_GEN_SQUASHFS'
DEFAULT_WRITER = 'tools/round-39/gen-squashfs.py'


class Unevaluable(Exception):
    def __init__(self, reason, receipt=None):
        super().__init__(reason)
        self.reason = reason
        self.receipt = receipt or {}


# ------------------------------------------------------------------ git
def show(root, rev, path):
    """Blob bytes at `rev`, or None when absent/unreadable."""
    if not rev:
        return None
    p = subprocess.run(['git', '-C', root, 'show', '%s:%s' % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def present(root, rev, path):
    if not rev:
        return False
    return subprocess.run(['git', '-C', root, 'cat-file', '-e', '%s:%s' % (rev, path)],
                          capture_output=True).returncode == 0


def full_rev(root, rev):
    p = subprocess.run(['git', '-C', root, 'rev-parse', '--verify', '%s^{commit}' % rev],
                       capture_output=True, text=True)
    if p.returncode:
        raise Unevaluable('unknown_revision:%s' % rev)
    return p.stdout.strip()


def is_ancestor(root, a, b):
    if not a or not b:
        return False
    return subprocess.run(['git', '-C', root, 'merge-base', '--is-ancestor', a, b],
                          capture_output=True).returncode == 0


def first_add(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'log', '--format=%H', '--diff-filter=A',
                        '--no-renames', '--reverse', rev, '--', path],
                       capture_output=True, text=True)
    if p.returncode:
        return None
    lines = [l for l in p.stdout.split() if l]
    return lines[0] if lines else None


def frozen_changes(root, freeze, rev):
    p = subprocess.run(['git', '-C', root, 'log', '--format=%H', '--no-renames',
                        '%s..%s' % (freeze, rev), '--', *FROZEN],
                       capture_output=True, text=True)
    return [l for l in p.stdout.split() if l]


def commits_touching(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'log', '--format=%H', rev, '--', path],
                       capture_output=True, text=True)
    if p.returncode:
        return []
    return [l for l in p.stdout.split() if l]


# ------------------------------------------------------------------ tables
def craft_span(text):
    """(first, last) line indices of the `## Queue-drain craft` section body."""
    if text is None:
        return None
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.lower().startswith(CRAFT.lower())), None)
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    return lines, start, end


def table_block(text, marker):
    """Marker line through the table's last row, inside `## Queue-drain craft`."""
    span = craft_span(text)
    if span is None:
        return None
    lines, start, end = span
    mi = next((i for i in range(start + 1, end) if marker in lines[i]), None)
    if mi is None:
        return None
    ti = next((i for i in range(mi + 1, end) if lines[i].lstrip().startswith('|')), None)
    if ti is None:
        return None
    last = ti
    for i in range(ti, end):
        if not lines[i].lstrip().startswith('|'):
            break
        last = i
    return '\n'.join(lines[mi:last + 1])


def header_cells(block):
    if not block:
        return None
    rows = [l for l in block.splitlines() if l.lstrip().startswith('|')]
    if not rows:
        return None
    return [c.strip().strip('`').strip().lower()
            for c in rows[0].strip().strip('|').split('|')]


def v2_columns_ok(block):
    cells = header_cells(block)
    return bool(cells) and all(c in cells for c in V2_COLUMNS)


def derive_base(root, freeze):
    """Newest commit at or below FREEZE whose SKILL.md predates the v2 marker."""
    commits = commits_touching(root, freeze, SKILL)
    first_without = None
    for c in commits:                       # newest first
        b = show(root, c, SKILL)
        if b is None:
            continue
        text = b.decode('utf-8', 'replace')
        if MARKER_V2 in text:
            continue
        if first_without is None:
            first_without = c
        if MARKER_V1 in text:
            return c, 'derived'
    return first_without, 'derived'


# ------------------------------------------------------------------ scratch
def scratch_root():
    base = os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
    root = os.path.join(base, 'kaidoku-r40')
    os.makedirs(root, exist_ok=True)
    return root


def scratch_dir():
    return tempfile.mkdtemp(prefix='c2-counter.', dir=scratch_root())


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def as_text(b):
    return b.decode('utf-8', 'replace') if b is not None else None


# ------------------------------------------------------------------ envelopes
def envelope_data(obj):
    if isinstance(obj, dict) and 'subject' not in obj and isinstance(obj.get('data'), dict):
        return obj['data']
    return obj


def subject_sha(obj):
    try:
        return str(obj['subject']['digest']['sha256']).lower()
    except Exception:
        return None


def provider_name(obj):
    p = obj.get('provider')
    if isinstance(p, dict):
        return p.get('id') or p.get('name')
    return p if isinstance(p, str) else None


# ------------------------------------------------------------------ interpreter
def run_interp(exe, skill, envs, extra=()):
    return subprocess.run([sys.executable, '-I', '-B', exe, '--skill', skill]
                          + list(extra) + list(envs),
                          capture_output=True, text=True, timeout=1800)


def _row_of(entry):
    for key in ('rule', 'row_index', 'index'):
        v = entry.get(key)
        if isinstance(v, bool):
            continue
        if isinstance(v, int):
            return v
        if isinstance(v, str) and v.strip().lstrip('-').isdigit():
            return int(v)
    row = entry.get('row')
    if isinstance(row, dict):
        return _row_of(row)
    return None


def parse_json_results(stdout):
    """{path: {label, action, row, cells}} from the interpreter's `--json` document."""
    doc = json.loads(stdout)
    results = doc.get('results') if isinstance(doc, dict) else None
    if not isinstance(results, list):
        return None
    out = {}
    for r in results:
        if not isinstance(r, dict) or not isinstance(r.get('path'), str):
            return None
        action = r.get('action')
        for key in ('row_action', 'decision_action'):
            if action is None:
                action = r.get(key)
        cells = r.get('row') if isinstance(r.get('row'), list) else None
        out[r['path']] = {'label': r.get('label'), 'action': action,
                          'row': _row_of(r), 'cells': cells}
    return out


def parse_v2_rows(block):
    """(header cells lowercased, body rows) of the v2 table block."""
    if not block:
        return None, []
    rows = [[c.strip().strip('`').strip() for c in l.strip().strip('|').split('|')]
            for l in block.splitlines() if l.lstrip().startswith('|')]
    if len(rows) < 2:
        return None, []
    return [c.lower() for c in rows[0]], rows[2:]


def parse_tab_results(stdout):
    out = {}
    for line in stdout.splitlines():
        if '\t' not in line:
            continue
        f = line.split('\t')
        path = f[0].strip()
        row = None
        if len(f) > 3 and f[3].strip().lstrip('-').isdigit():
            row = int(f[3].strip())
        out[path] = {'label': (f[1].strip() or None) if len(f) > 1 else None,
                     'action': (f[2].strip() or None) if len(f) > 2 else None,
                     'row': row, 'cells': None}
    return out


TABLE_ONLY_LINE = re.compile(r'^\s*(\d+)\.\s+`?([^`\s]+)`?\s*$')


def infer_index_base(entries, tpos, label_rows):
    """0 or 1: how the interpreter numbers the table rows it reports.

    Votes come from entries that name both a label and an index, and from the
    interpreter's own `--table-only` listing; ties and silence fall back to 0.
    """
    votes = []
    for val in entries:
        lab, row = val.get('label'), val.get('row')
        if lab in tpos and isinstance(row, int):
            votes.append(row - tpos[lab])
    for lab, idx in (label_rows or {}).items():
        if lab in tpos and isinstance(idx, int):
            votes.append(idx - tpos[lab])
    if not votes:
        return 0
    return max(set(votes), key=votes.count)


def parse_table_only(stdout):
    """{label: row} from the interpreter's `--table-only` output."""
    try:
        doc = json.loads(stdout)
        rules = doc.get('rules') if isinstance(doc, dict) else None
        if isinstance(rules, list):
            out = {}
            for r in rules:
                if isinstance(r, dict) and r.get('label') is not None:
                    out[str(r['label'])] = _row_of(r)
            return out or None
    except Exception:
        pass
    out = {}
    for line in stdout.splitlines():
        m = TABLE_ONLY_LINE.match(line)
        if m:
            out[m.group(2)] = int(m.group(1))
    return out or None


# ------------------------------------------------------------------ measure
def measure(root, rev_arg, freeze_arg, base_arg=None):
    rev = full_rev(root, rev_arg)
    freeze = full_rev(root, freeze_arg)
    res = {'predicate': 'P40-C2', 'revision': rev, 'freeze': freeze,
           'freeze_arg': freeze_arg, 'revision_arg': rev_arg, 'base_arg': base_arg,
           'manifest_path': MANIFEST, 'argv': sys.argv,
           'bindings': {}, 'bindings_false': [], 'carriers': [],
           'frozen_paths_changed': []}
    if not is_ancestor(root, freeze, rev):
        raise Unevaluable('freeze_not_ancestor_of_rev', res)
    changed = frozen_changes(root, freeze, rev)
    if changed:
        res['frozen_paths_changed'] = changed
        raise Unevaluable('frozen_path_changed', res)

    # ---- base (rule block 18 / table v1 invariance)
    if base_arg:
        base = full_rev(root, base_arg)
        base_src = 'arg'
    else:
        base, base_src = derive_base(root, freeze)
    res['base_commit'] = base
    res['base_source'] = base_src

    man_b = show(root, rev, MANIFEST)
    if man_b is None:
        raise Unevaluable('no_manifest_at_rev', res)
    try:
        man = json.loads(man_b.decode())
    except Exception:
        raise Unevaluable('manifest_unparsable', res)
    if not isinstance(man, dict):
        raise Unevaluable('manifest_not_an_object', res)

    classes = man.get('classes') if isinstance(man.get('classes'), list) else []
    carriers = man.get('carriers') if isinstance(man.get('carriers'), list) else []
    carriers = [c for c in carriers if isinstance(c, dict)]
    N = len(carriers)
    ids = [str(c.get('id', '')) for c in carriers]
    per = {}
    for c in carriers:
        per[c.get('class')] = per.get(c.get('class'), 0) + 1

    b = res['bindings']
    b['seed_matches_freeze'] = str(man.get('seed', '')).lower() == freeze

    gen_b = show(root, freeze, GEN)
    gen_sha = sha256_bytes(gen_b) if gen_b is not None else None
    g = man.get('generator')
    declared_gen_sha = None
    if isinstance(g, dict):
        b['manifest_generator_path'] = str(g.get('name', '')).lower() in (
            'heldout-gen-v2.py', GEN)
        declared_gen_sha = g.get('sha256')
        b['generator_sha_matches_freeze'] = declared_gen_sha is None or declared_gen_sha == gen_sha
    else:
        b['manifest_generator_path'] = str(g) == GEN
        b['generator_sha_matches_freeze'] = True
    res['generator'] = {'declared': g, 'declared_sha256': declared_gen_sha,
                        'freeze_sha256': gen_sha, 'path': GEN,
                        'present_at_freeze': gen_b is not None}

    b['classes_unique'] = bool(classes) and len(classes) == len(set(classes)) \
        and all(isinstance(x, str) and x for x in classes)
    b['classes_two_each'] = bool(classes) and all(per.get(k) == 2 for k in classes) \
        and set(per) <= set(classes)
    b['n_equals_twice_classes'] = N > 0 and N == 2 * len(classes)
    b['ids_unique'] = bool(ids) and len(set(ids)) == len(ids) and all(ids)
    b['arms_valid'] = bool(carriers) and all(c.get('arm') in ('after', 'before', 'ood')
                                             for c in carriers)

    # ---- tables
    skill_rev = show(root, rev, SKILL)
    skill_fz = show(root, freeze, SKILL)
    skill_base = show(root, base, SKILL) if base else None
    v2_rev = table_block(as_text(skill_rev), MARKER_V2)
    v2_fz = table_block(as_text(skill_fz), MARKER_V2)
    v1_rev = table_block(as_text(skill_rev), MARKER_V1)
    v1_base = table_block(as_text(skill_base), MARKER_V1)
    b['v2_table_present'] = v2_rev is not None
    b['v2_table_identical'] = v2_rev is not None and v2_fz is not None and v2_rev == v2_fz
    b['v2_table_columns'] = v2_columns_ok(v2_rev)
    b['v1_table_present'] = v1_base is not None
    b['v1_table_identical'] = v1_base is not None and v1_rev is not None and v1_base == v1_rev
    res['table'] = {
        'v2': {'present_at_rev': v2_rev is not None, 'present_at_freeze': v2_fz is not None,
               'identical': b['v2_table_identical'], 'columns_ok': b['v2_table_columns'],
               'bytes': len(v2_rev.encode()) if v2_rev is not None else 0},
        'v1': {'present_at_base': v1_base is not None, 'present_at_rev': v1_rev is not None,
               'identical': b['v1_table_identical'],
               'bytes_base': len(v1_base.encode()) if v1_base is not None else 0,
               'bytes_rev': len(v1_rev.encode()) if v1_rev is not None else 0},
    }

    interp_b = show(root, freeze, INTERP)
    b['interpreter_present_at_freeze'] = interp_b is not None
    res['interpreter'] = {'path': INTERP,
                          'freeze_sha256': sha256_bytes(interp_b) if interp_b is not None else None}

    mdir = os.path.dirname(MANIFEST)

    def resolve(p):
        if not isinstance(p, str) or not p or p.startswith('/') or '..' in p.split('/'):
            return None
        for cand in (p, mdir.rstrip('/') + '/' + p):
            if cand.startswith('./'):
                cand = cand[2:]
            if present(root, rev, cand):
                return cand
        return None

    scratch = scratch_dir()
    try:
        # ---- regeneration from the frozen generator
        regen = {}
        if gen_b is None:
            raise Unevaluable('generator_absent_at_freeze', res)
        tree = os.path.join(scratch, 'lane')
        os.makedirs(tree)
        p = subprocess.run(['git', '-C', root, 'ls-tree', '-r', '--name-only', freeze,
                            '--', *GEN_TREE_PREFIXES], capture_output=True, text=True)
        materialised = []
        for rel in [l for l in p.stdout.split() if l]:
            blob = show(root, freeze, rel)
            if blob is None:
                continue
            dest = os.path.join(tree, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'wb') as fh:
                fh.write(blob)
            materialised.append(rel)
        gpath = os.path.join(tree, GEN)
        if not os.path.isfile(gpath):
            raise Unevaluable('generator_absent_at_freeze', res)
        wlocal = os.path.join(tree, DEFAULT_WRITER)
        wb = show(root, freeze, DEFAULT_WRITER)
        w_sha = sha256_bytes(wb) if wb is not None else None
        gw = g.get('writer') if isinstance(g, dict) else None
        declared_w_sha = gw.get('sha256') if isinstance(gw, dict) else None
        b['writer_matches_manifest'] = True
        res['writer'] = {'path': DEFAULT_WRITER, 'materialised': os.path.isfile(wlocal),
                         'sha256': w_sha, 'declared_sha256': declared_w_sha,
                         'declared_path': gw.get('path') if isinstance(gw, dict) else None,
                         'materialised_files': materialised}
        env = dict(os.environ)
        env['TMPDIR'] = os.path.join(scratch, 'tmp')
        os.makedirs(env['TMPDIR'], exist_ok=True)
        if os.path.isfile(wlocal):
            env[WRITER_ENV] = wlocal
        outdir = os.path.join(scratch, 'regen')
        pr = subprocess.run([sys.executable, '-I', '-B', gpath, '--seed', freeze,
                             '--out', outdir],
                            cwd=tree, capture_output=True, text=True, timeout=3600, env=env)
        if pr.returncode != 0:
            res['generator_stderr'] = (pr.stderr or '')[-2000:]
            raise Unevaluable('generator_failed', res)
        rman_path = os.path.join(outdir, 'manifest.json')
        if not os.path.exists(rman_path):
            raise Unevaluable('generator_wrote_no_manifest', res)
        try:
            with open(rman_path) as fh:
                rman = json.load(fh)
        except Exception:
            raise Unevaluable('regenerated_manifest_unparsable', res)
        for rc in (rman.get('carriers') or []):
            if not isinstance(rc, dict):
                continue
            rel = rc.get('carrier')
            fp = os.path.join(outdir, rel) if isinstance(rel, str) else None
            data = open(fp, 'rb').read() if fp and os.path.isfile(fp) else None
            regen[str(rc.get('id', ''))] = {
                'sha256': sha256_bytes(data) if data is not None else None,
                'class': rc.get('class'), 'arm': rc.get('arm'),
                'carrier': rel, 'manifest_sha': rc.get('sha256'),
                'expected_label': rc.get('expected_label', rc.get('label')),
                'expected_action': rc.get('expected_action', rc.get('action'))}
        b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze

        # ---- per-carrier checks
        env_rows = []
        for c in carriers:
            cid = str(c.get('id', ''))
            msha = str(c.get('sha256', '')).lower()
            exp_label = c.get('expected_label', c.get('label'))
            exp_action = c.get('expected_action', c.get('action'))
            cpath = resolve(c.get('carrier'))
            cbytes = show(root, rev, cpath) if cpath else None
            committed_sha = sha256_bytes(cbytes) if cbytes is not None else None
            r = regen.get(cid) or {}
            regen_sha = r.get('sha256')
            regen_ok = bool(regen_sha) and regen_sha == msha \
                and r.get('class') == c.get('class') and r.get('arm') == c.get('arm') \
                and r.get('expected_label') == exp_label \
                and r.get('expected_action') == exp_action
            commit_ok = committed_sha is not None and committed_sha == msha
            epath = c.get('envelope')
            inferred = False
            if not isinstance(epath, str) or not epath:
                car = c.get('carrier')
                if isinstance(car, str) and '/' in car:
                    epath = car.rsplit('/', 1)[0] + '/envelope.json'
                    inferred = True
                else:
                    epath = None
            epath = resolve(epath) if epath else None
            ebytes = show(root, rev, epath) if epath else None
            digest_ok = False
            op = prov = None
            if ebytes is not None:
                try:
                    eo = envelope_data(json.loads(ebytes.decode()))
                    digest_ok = bool(msha) and subject_sha(eo) == msha
                    op = eo.get('operation') if isinstance(eo, dict) else None
                    prov = provider_name(eo) if isinstance(eo, dict) else None
                    env_rows.append({'id': cid, 'path': epath, 'bytes': ebytes})
                except Exception:
                    digest_ok = False
            res['carriers'].append({
                'id': cid, 'class': c.get('class'), 'arm': c.get('arm'),
                'expected_label': exp_label, 'expected_action': exp_action,
                '_carrier_path': cpath,
                'manifest_sha256': msha, 'committed_sha256': committed_sha,
                'regenerated_sha256': regen_sha, 'regen_ok': regen_ok,
                'commit_ok': commit_ok, 'envelope': epath,
                'envelope_inferred': inferred, 'digest_ok': digest_ok,
                'operation': op, 'provider': prov})
        cp = [r.get('_carrier_path') for r in res['carriers']]
        ep = [r.get('envelope') for r in res['carriers']]
        b['carrier_paths_unique'] = N > 0 and all(cp) and len(set(cp)) == len(cp)
        b['envelope_paths_unique'] = N > 0 and all(ep) and len(set(ep)) == len(ep)
        for r in res['carriers']:
            r.pop('_carrier_path', None)
        b['carriers_regenerated'] = N > 0 and all(r['regen_ok'] for r in res['carriers'])
        b['carriers_committed'] = N > 0 and all(r['commit_ok'] for r in res['carriers'])
        b['envelopes_valid'] = N > 0 and all(r['digest_ok'] for r in res['carriers'])

        # ---- first-add ordering
        ma = first_add(root, rev, MANIFEST)
        b['manifest_after_freeze'] = bool(ma) and ma != freeze and is_ancestor(root, freeze, ma)
        env_firsts = []
        for row in res['carriers']:
            fa = first_add(root, rev, row['envelope']) if row['envelope'] else None
            row['envelope_first_add'] = fa
            env_firsts.append(fa)
        b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) \
            and all(fa is not None and is_ancestor(root, ma, fa) for fa in env_firsts)
        res['manifest_first_add'] = ma

        # ---- (label, action, row) from the frozen interpreter on SKILL.md at REV
        got = {}
        row_source = None
        if v2_rev is not None and interp_b is not None:
            idir = os.path.join(scratch, 'triage')
            os.makedirs(idir)
            ipath = os.path.join(idir, 'sqfs-triage-v2.py')
            with open(ipath, 'wb') as fh:
                fh.write(interp_b)
            spath = os.path.join(idir, 'SKILL.md')
            with open(spath, 'wb') as fh:
                fh.write(skill_rev)
            edir = os.path.join(idir, 'env')
            os.makedirs(edir)
            argmap = {}
            for row in env_rows:
                fp = os.path.join(edir, row['id'] + '.json')
                with open(fp, 'wb') as fh:
                    fh.write(row['bytes'])
                argmap[os.path.normpath(fp)] = row['id']
            args = sorted(argmap)

            def collect(parsed):
                out = {}
                for path, val in (parsed or {}).items():
                    cid = argmap.get(os.path.normpath(path))
                    if cid:
                        out[cid] = val
                return out

            pr = run_interp(ipath, spath, args, ['--json'])
            res['interpreter_json_exit'] = pr.returncode
            got = {}
            if pr.returncode == 0:
                try:
                    parsed = parse_json_results(pr.stdout)
                except Exception:
                    parsed = None
                if parsed is not None:
                    got = collect(parsed)
                    row_source = 'json' if all(v.get('row') is not None
                                               for v in got.values()) else None
            if not got:
                pr = run_interp(ipath, spath, args)
                res['interpreter_tab_exit'] = pr.returncode
                res['interpreter_stderr_tail'] = (pr.stderr or '')[-1000:]
                if pr.returncode != 0:
                    raise Unevaluable('interpreter_failed', res)
                got = collect(parse_tab_results(pr.stdout))
                row_source = 'tab' if got and all(v.get('row') is not None
                                                  for v in got.values()) else None
            label_rows = None
            if got and any(v.get('row') is None for v in got.values()):
                pt = run_interp(ipath, spath, [], ['--table-only'])
                res['interpreter_table_only_exit'] = pt.returncode
                label_rows = parse_table_only(pt.stdout) if pt.returncode == 0 else None
                if label_rows:
                    for val in got.values():
                        if val.get('row') is None:
                            val['row'] = label_rows.get(val.get('label'))
                    if all(v.get('row') is not None for v in got.values()):
                        row_source = 'table_only'
            res['row_source'] = row_source

            # The table row the interpreter chose is itself a decision: when it
            # names only an index (or only the row cells), read the pair off the
            # frozen v2 header, so the executable's row is what gets compared
            # with the generator's expectation.  Row numbering is the
            # interpreter's own (v1 numbers from 1), so the index base is
            # inferred from the rows the interpreter does name, never assumed.
            header, trows = parse_v2_rows(v2_rev)
            if header is not None:
                lidx = header.index('label') if 'label' in header else None
                aidx = header.index('action') if 'action' in header else None
                tpos = {}
                if lidx is not None:
                    for i, cells in enumerate(trows):
                        if lidx < len(cells) and cells[lidx] not in tpos:
                            tpos[cells[lidx]] = i
                need = [v for v in got.values()
                        if (v.get('label') is None or v.get('action') is None)
                        and v.get('cells') is None]
                if need and tpos and label_rows is None:
                    pt = run_interp(ipath, spath, [], ['--table-only'])
                    res['interpreter_table_only_exit'] = pt.returncode
                    if pt.returncode == 0:
                        label_rows = parse_table_only(pt.stdout)
                base = infer_index_base(list(got.values()), tpos, label_rows)
                res['row_index_base'] = base
                derived = 0
                for val in got.values():
                    cells = val.get('cells')
                    if cells is None and isinstance(val.get('row'), int):
                        pos = val['row'] - base
                        if 0 <= pos < len(trows):
                            cells = trows[pos]
                    if cells is None:
                        continue
                    if val.get('label') is None and lidx is not None and lidx < len(cells):
                        val['label'] = cells[lidx]
                        derived += 1
                    if val.get('action') is None and aidx is not None and aidx < len(cells):
                        val['action'] = cells[aidx]
                        derived += 1
                res['pair_fields_derived_from_row'] = derived
            for row in res['carriers']:
                v = got.get(row['id']) or {}
                row['label'] = v.get('label')
                row['action'] = v.get('action')
                row['row'] = v.get('row')
                row['pair_match'] = (row['label'] == row['expected_label']
                                     and row['action'] == row['expected_action'])
        else:
            res['row_source'] = None
            for row in res['carriers']:
                row['label'] = None
                row['action'] = None
                row['row'] = None
                row['pair_match'] = False

        matched = sum(1 for row in res['carriers'] if row['pair_match'])
        matched_rows = [row['row'] for row in res['carriers'] if row['pair_match']]
        # L1 freeze fix (dry run): the no-match pair (unclassified, none) has no row by design
        reported = bool(got) and all(r.get('row') is not None or r.get('label') == NOMATCH_PAIR[0]
                                     for r in res['carriers'])
        b['decisions_reported'] = reported
        distinct = len(set(matched_rows)) if matched_rows else 0
        res['distinct_decisions'] = distinct
        res['distinct_row_list'] = sorted(set(matched_rows),
                                          key=lambda x: (x is None, str(x)))

        # same expected pair <=> same row, and different pairs <=> different rows
        pairs = {}
        for row in res['carriers']:
            pairs.setdefault((row['expected_label'], row['expected_action']), set()).add(row['row'])
        consistent = reported and all(len(v) == 1 and (None not in v or k == NOMATCH_PAIR)
                                      for k, v in pairs.items()) \
            and len(set(next(iter(v)) for v in pairs.values())) == len(pairs)
        b['row_decisions_consistent'] = bool(consistent)
        res['decision_pairs'] = {'%s/%s' % k: sorted(v, key=lambda x: (x is None, str(x)))
                                 for k, v in pairs.items()}

        # ---- reported (non-binding) shape of the held-out set
        per_class = {}
        for row in res['carriers']:
            per_class.setdefault(str(row['class']), []).append({
                'id': row['id'], 'carrier_sha256': row['manifest_sha256'],
                'expected_label': row['expected_label'],
                'expected_action': row['expected_action'],
                'label': row['label'], 'action': row['action'], 'row': row['row']})
        res['per_class'] = {k: sorted(v, key=lambda r: r['id'])
                            for k, v in sorted(per_class.items())}
        res['replicates_identical_in_class'] = sorted(
            k for k, v in per_class.items()
            if len({r['carrier_sha256'] for r in v}) != len(v))
        res['label_action_vocabulary'] = sorted(
            {'%s/%s' % (r['expected_label'], r['expected_action']) for r in res['carriers']})
        res['unclassified_expected'] = sum(
            1 for r in res['carriers'] if r['expected_label'] == 'unclassified')
        res['unclassified_observed'] = sum(
            1 for r in res['carriers'] if r['label'] == 'unclassified')

        # ---- target
        bindings_ok = all(v is True for v in b.values())
        met = bool(matched == N and bindings_ok)
        recomputed = bool(matched == N and all(v is True for k, v in b.items()))
        res.update({'n': N, 'matched': matched, 'bindings_ok': bindings_ok,
                    'bindings_false': sorted(k for k, v in b.items() if v is not True),
                    'met_target': met,
                    'met_target_formula': {'matched_equals_n': matched == N,
                                           'all_bindings_true': bindings_ok},
                    'met_target_consistent': met == recomputed})
        if not res['met_target_consistent']:
            raise Unevaluable('met_target_inconsistent', res)
        res['exit_code'] = 0 if met else 1
        return res
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--base')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.rev and a.freeze):
        print('usage: --root --rev --freeze required (or --selftest)', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze, a.base)
    except Unevaluable as e:
        out = dict(e.receipt)
        out['unevaluable'] = e.reason
        out['exit_code'] = 2
        out['argv'] = sys.argv
        print(json.dumps({'unevaluable': e.reason,
                          'revision': out.get('revision'),
                          'freeze': out.get('freeze'),
                          'frozen_paths_changed': out.get('frozen_paths_changed', []),
                          'exit_code': 2}, sort_keys=True))
        if a.json_out:
            d = os.path.dirname(os.path.abspath(a.json_out))
            os.makedirs(d, exist_ok=True)
            with open(a.json_out, 'w') as f:
                json.dump(out, f, indent=1, sort_keys=True)
        return 2
    print(json.dumps({'revision': res['revision'], 'freeze': res['freeze'], 'n': res['n'],
                      'matched': res['matched'], 'distinct_decisions': res['distinct_decisions'],
                      'bindings_false': res['bindings_false'],
                      'met_target': res['met_target'],
                      'met_target_consistent': res['met_target_consistent'],
                      'exit_code': res['exit_code']}, sort_keys=True))
    if a.json_out:
        d = os.path.dirname(os.path.abspath(a.json_out))
        os.makedirs(d, exist_ok=True)
        with open(a.json_out, 'w') as f:
            json.dump(res, f, indent=1, sort_keys=True)
    return res['exit_code']


# ---------------------------------------------------------------- selftest
STUB_GEN = r'''#!/usr/bin/env python3
import argparse, hashlib, json, os
ap = argparse.ArgumentParser()
ap.add_argument('--seed', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--classes')
ap.add_argument('--gen')
ap.add_argument('--scratch')
a = ap.parse_args()
DEC = {
    'clean-be': ('clean', 'inspect', 'clean'),
    'clean-le': ('clean', 'inspect', 'clean'),
    'dep-missing-be': ('dep-missing-be', 'install-extractor', 'dep-missing-be'),
    'dep-missing-le': ('dep-missing-le', 'install-extractor', 'dep-missing-le'),
    'out-of-domain': ('unclassified', 'report-only', 'out-of-domain'),
}
classes = [c for c in a.classes.split(',') if c] if a.classes else list(DEC)
os.makedirs(a.out, exist_ok=True)
out = []
for ci, c in enumerate(classes):
    lab, act, key = DEC.get(c, ('unclassified', 'report-only', c))
    for k in range(2):
        h = hashlib.sha256(('%s:%s:%d' % (a.seed, c, k)).encode()).hexdigest()
        ident = 'H%02d' % (ci * 2 + k + 1)
        dpath = os.path.join(a.out, ident)
        os.makedirs(dpath, exist_ok=True)
        body = h.encode() + b':' + c.encode() + b'\n' + bytes.fromhex(h) * 8
        with open(os.path.join(dpath, 'carrier.sqsh'), 'wb') as fh:
            fh.write(body)
        out.append({'id': ident, 'class': c, 'decision_key': key,
                    'expected_label': lab, 'expected_action': act,
                    'arm': 'after' if lab != 'unclassified' else 'before',
                    'carrier': ident + '/carrier.sqsh',
                    'sha256': hashlib.sha256(body).hexdigest()})
man = {'seed': a.seed,
       'generator': {'name': 'heldout-gen-v2.py', 'version': 'r40-c2-stub',
                     'sha256': hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest()},
       'classes': classes, 'carriers': out}
with open(os.path.join(a.out, 'manifest.json'), 'w') as fh:
    json.dump(man, fh, indent=1, sort_keys=True)
'''

STUB_INTERP = r'''#!/usr/bin/env python3
import argparse, fnmatch, json, sys
MODE = '@@MODE@@'
ap = argparse.ArgumentParser()
ap.add_argument('--skill')
ap.add_argument('--json', action='store_true')
ap.add_argument('--table-only', action='store_true')
ap.add_argument('envs', nargs='*')
a = ap.parse_args()
if MODE == 'fail':
    sys.exit(1)
lines = open(a.skill).read().splitlines()
start = next((i for i, l in enumerate(lines) if l.startswith('## Queue-drain craft')), None)
if start is None:
    sys.exit(2)
end = len(lines)
for i in range(start + 1, len(lines)):
    if lines[i].startswith('## '):
        end = i
        break
sec = lines[start + 1:end]
mi = next((i for i, l in enumerate(sec) if '<!-- sqfs-triage-table v2 -->' in l), None)
if mi is None:
    sys.exit(2)
ti = next((i for i in range(mi + 1, len(sec)) if sec[i].lstrip().startswith('|')), None)
if ti is None:
    sys.exit(2)
rows = []
for l in sec[ti:]:
    if not l.lstrip().startswith('|'):
        break
    rows.append([c.strip().strip('`').strip() for c in l.strip().strip('|').split('|')])
if len(rows) < 2:
    sys.exit(2)
head = [c.strip().strip('`').strip().lower() for c in rows[0]]
def idx(name):
    return head.index(name) if name in head else None


CY, CO, CP, CC, CA = idx('label'), idx('operation'), idx('provider'), idx('class'), idx('action')
if CY is None or CC is None:
    sys.exit(2)
body = rows[2:]
if a.table_only:
    if MODE in ('notable', 'tsv4'):
        sys.exit(2)
    off = 1 if MODE == 'rowonly1' else 0
    for i, cells in enumerate(body):
        print('%d. %s' % (i + off, cells[CY]))
    sys.exit(0)
if a.json and MODE in ('tab3', 'notable', 'tsv4'):
    sys.exit(2)
res = []
for p in a.envs:
    d = json.load(open(p))
    if isinstance(d, dict) and 'subject' not in d and isinstance(d.get('data'), dict):
        d = d['data']
    cls = d.get('stub_class')
    hit = None
    for i, cells in enumerate(body):
        pat = cells[CC] if CC < len(cells) else '*'
        if pat == '*' or (cls is not None and fnmatch.fnmatchcase(cls, pat)):
            hit = i
            break
    cells = body[hit] if hit is not None else None
    res.append({'path': p,
                'label': cells[CY] if cells else 'unclassified',
                'action': (cells[CA] if CA is not None and CA < len(cells) else 'report-only')
                if cells else 'report-only',
                'rule': hit, 'row': cells})
if MODE == 'rowonly1':
    for r in res:
        r.pop('label', None)
        r.pop('action', None)
        r.pop('row', None)
        r['rule'] = None if r['rule'] is None else r['rule'] + 1
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
if MODE == 'rowonly':
    for r in res:
        r.pop('label', None)
        r.pop('action', None)
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
if a.json or MODE == 'norow':
    if MODE == 'norow':
        for r in res:
            r.pop('rule', None)
            r.pop('row', None)
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
for r in res:
    if MODE in ('tab3', 'notable'):
        print('%s\t%s\t%s' % (r['path'], r['label'], r['action']))
    else:
        print('%s\t%s\t%s\t%s' % (r['path'], r['label'], r['action'], r['rule']))
'''


def selftest():
    SAME = object()
    ABSENT = object()
    sroot = os.path.join(os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir(),
                         'kaidoku-r40')
    os.makedirs(sroot, exist_ok=True)
    fails = []

    V2_HEADER = ['label', 'operation', 'provider', 'class', 'action', 'source']
    V1_HEADER = ['label', 'handler', 'gap kinds', 'dependencies', '-be in child argv',
                 'symlink removed', 'published files', 'cause -> action', 'source']
    V1_ROWS = [
        ['`clean`', '`squashfs_v4_be`', '`*`', '`*`', '`n/a`', '`yes`', '`>0`',
         'handlers ran, gaps allowed -> publish', '`corpus/k.md:1-1`'],
        ['`dep-missing-be`', '`*`', '`missing-extractor-dependency`', '`sasquatch-v4be`',
         '`-be`', '`n/a`', '`0`', 'no extractor -> record gap', '`corpus/k.md:2-2`'],
    ]
    V2_ROWS = [
        ['`clean`', '`extract_firmware`', '`unblob`', 'clean', '`inspect`',
         '`corpus/k.md:3-3`'],
        ['`dep-missing-be`', '`extract_firmware`', '`unblob`', 'dep-missing-be',
         '`install-extractor`', '`corpus/k.md:4-4`'],
        ['`unclassified`', '`*`', '`*`', 'out-of-domain', '`report-only`',
         '`corpus/k.md:5-5`'],
    ]

    def table_text(header, rows):
        sep = '|' + '---|' * len(header)
        return '\n'.join(['| ' + ' | '.join(header) + ' |', sep]
                         + ['| ' + ' | '.join(r) + ' |' for r in rows])

    def skill_doc(v1_rows, v2_rows, v2_header=None):
        header = v2_header or V2_HEADER
        s = '# K\n\n## Queue-drain craft (x)\n\n- **rule** text\n\n'
        if v1_rows is not ABSENT:
            s += '### rule block 18 — SquashFS extract-firmware outcome triage (table v1)\n\n'
            s += '<!-- sqfs-triage-table v1 -->\n\n' + table_text(V1_HEADER, v1_rows) + '\n\n'
        if v2_rows is not ABSENT:
            s += '### rule block 19 — triage table v2\n\n'
            s += '<!-- sqfs-triage-table v2 -->\n\n' + table_text(header, v2_rows) + '\n\n'
        return s + '## Next\n\n- other\n'

    def write_tree(d, tree):
        for p, c in tree.items():
            fp = os.path.join(d, p)
            os.makedirs(os.path.dirname(fp) or d, exist_ok=True)
            with open(fp, 'wb') as f:
                f.write(c if isinstance(c, bytes) else c.encode())

    def commit(d, tree, msg='x'):
        write_tree(d, tree)
        subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                        'commit', '-qm', msg, '--allow-empty'], check=True)
        return subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip()

    CLASSES = ['clean-be', 'clean-le', 'dep-missing-be', 'out-of-domain']

    def build(params):
        d = tempfile.mkdtemp(prefix='c2-case.', dir=sroot)
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit('fixture toplevel mismatch')
        v1_base = params.get('v1_base', V1_ROWS)
        commit(d, {SKILL: skill_doc(v1_base, ABSENT),
                   CLAIMS: '# claims (draft)\n'}, 'base')
        v1_freeze = params.get('v1_freeze', v1_base)
        v2_freeze = params.get('v2_freeze', V2_ROWS)
        mode = params.get('mode', 'json')
        v2_header = params.get('v2_header')
        tool_tree = {
            SKILL: skill_doc(v1_freeze, ABSENT if v2_freeze is ABSENT else v2_freeze,
                             v2_header),
            INTERP: STUB_INTERP.replace('@@MODE@@', mode),
            GEN: STUB_GEN,
            COUNTER: '# counter\n',
            CLAIMS: '# claims (frozen)\n',
        }
        claim = params.get('claim', 'after')
        muts = params.get('muts', set())
        freeze = commit(d, tool_tree, 'freeze')
        if claim == 'none':
            return d, freeze, freeze
        seed = '0' * 64 if params.get('seed') == 'zero' else freeze
        gdir = tempfile.mkdtemp(prefix='gen.', dir=sroot)
        pr = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, GEN),
                             '--seed', seed, '--out', gdir],
                            capture_output=True, text=True)
        if pr.returncode != 0:
            raise SystemExit('stub generator failed: ' + pr.stderr)
        with open(os.path.join(gdir, 'manifest.json')) as fh:
            rman = json.load(fh)
        classes = params.get('classes', CLASSES)
        man = {'seed': seed, 'generator': GEN,
               'classes': [c for c in rman['classes'] if c in classes], 'carriers': []}
        if params.get('gen_obj'):
            man['generator'] = {
                'name': 'heldout-gen-v2.py', 'version': 'r40-c2-stub',
                'sha256': hashlib.sha256(STUB_GEN.encode()).hexdigest()
                if params.get('gen_obj') == 'good' else 'f' * 64,
                'carriers_per_class': 2}
        claim_files = {}
        sha_by_id = {c['id']: c['sha256'] for c in rman['carriers']}
        for c in rman['carriers']:
            if c['class'] not in classes:
                continue
            cid = c['id']
            body = open(os.path.join(gdir, cid, 'carrier.sqsh'), 'rb').read()
            if 'carrier_corrupt' in muts and cid == 'H01':
                body += b'X'
            base = 'corpus/evidence/round-40/c2/heldout/' + cid
            claim_files[base + '/carrier.sqsh'] = body
            env = {'subject': {'name': 'carrier.sqsh',
                               'digest': {'sha256': (
                                   '0' * 64 if ('digest_mismatch' in muts and cid == 'H01')
                                   else sha_by_id.get('H02', c['sha256'])
                                   if ('swap_digest' in muts and cid == 'H01')
                                   else c['sha256'])},
                               'format': 'file', 'architecture': None,
                               'local_path': '/fast/scratch/x'},
                   'operation': 'analyze' if ('envelope_op' in muts and cid == 'H03')
                   else 'extract_firmware',
                   'provider': {'id': 'unblob'},
                   'normalized_result': {'extraction_gaps': [], 'files': [],
                                         'chunks': [], 'diagnostics': []},
                   'stub_class': c['decision_key']}
            if 'missing_envelope' in muts and cid == 'H02':
                pass
            else:
                blob = {'ok': True, 'data': env, 'meta': {'cli': 'rea-agents@6.5.0'}} \
                    if 'full_envelope' in muts else env
                claim_files[base + '/envelope.json'] = json.dumps(blob, indent=1, sort_keys=True)
            entry = dict(c)
            for k in ('decision_key',):
                entry.pop(k, None)
            if 'lane_relative_paths' in muts:
                entry['carrier'] = base + '/carrier.sqsh'
            if 'omit_envelope' not in muts:
                entry['envelope'] = (base + '/envelope.json') if 'lane_relative_paths' in muts \
                    else (cid + '/envelope.json')
            if 'mislabel' in muts and cid == 'H01':
                entry['expected_label'] = 'dep-missing-be'
            if 'wrong_action' in muts and cid == 'H03':
                entry['expected_action'] = 'install-extractor'
            if 'share_carrier_path' in muts and cid == 'H02':
                entry['carrier'] = 'H01/carrier.sqsh'
            man['carriers'].append(entry)
        if 'class_count3' in muts:
            body = claim_files['corpus/evidence/round-40/c2/heldout/H01/carrier.sqsh']
            claim_files['corpus/evidence/round-40/c2/heldout/H09/carrier.sqsh'] = body
            claim_files['corpus/evidence/round-40/c2/heldout/H09/envelope.json'] = \
                claim_files['corpus/evidence/round-40/c2/heldout/H01/envelope.json']
            man['carriers'].append({'id': 'H09', 'class': 'clean-be',
                                    'expected_label': 'clean', 'expected_action': 'inspect',
                                    'arm': 'after', 'carrier': 'H09/carrier.sqsh',
                                    'sha256': hashlib.sha256(body).hexdigest(),
                                    'envelope': 'H09/envelope.json'})
        man_text = json.dumps(man, indent=1, sort_keys=True)
        if 'bad_manifest' in muts:
            man_text = manifest_broken(man_text)
        post = {}
        v1_rev = params.get('v1_rev', SAME)
        v2_rev = params.get('v2_rev', SAME)
        if v1_rev is not SAME or v2_rev is not SAME:
            post[SKILL] = skill_doc(
                v1_freeze if v1_rev is SAME else (ABSENT if v1_rev is ABSENT else v1_rev),
                (ABSENT if v2_freeze is ABSENT else v2_freeze) if v2_rev is SAME
                else (ABSENT if v2_rev is ABSENT else v2_rev), v2_header)
        for m, p in (('edit_interp', INTERP), ('edit_gen', GEN),
                     ('edit_claims', CLAIMS), ('edit_counter', COUNTER)):
            if m in muts:
                cur = tool_tree[p]
                post[p] = cur + ('\n# edited after freeze\n' if isinstance(cur, str) else b'#x\n')
        if claim == 'after':
            tree = dict(claim_files)
            tree[MANIFEST] = man_text
            tree.update(post)
            rev = commit(d, tree, 'claim data')
        elif claim == 'split':
            commit(d, dict(claim_files), 'carriers and envelopes')
            tree = {MANIFEST: man_text}
            tree.update(post)
            rev = commit(d, tree, 'manifest')
        elif claim == 'befreeze':
            commit(d, dict(claim_files), 'claim data before freeze')
            tree = {MANIFEST: man_text, 'plans/round-40-freeze.txt': 'freeze\n'}
            tree.update(post)
            rev = commit(d, tree, 'freeze marker')
            freeze = rev
        else:
            raise SystemExit('unknown claim mode ' + claim)
        return d, freeze, rev

    def manifest_broken(text):
        return text.rstrip()[:-3]

    def run_counter(d, rev, freeze, extra=()):
        jout = os.path.join(d, '..', os.path.basename(d) + '.receipt.json')
        cmd = [sys.executable, '-I', '-B', os.path.abspath(__file__),
               '--root', d, '--rev', rev, '--freeze', freeze,
               '--json-out', jout] + list(extra)
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        rec = None
        if os.path.exists(jout):
            try:
                with open(jout) as fh:
                    rec = json.load(fh)
            finally:
                os.unlink(jout)
        return pr, rec

    cases = [
        # name, params, want_exit, want_false bindings, want_true bindings, extra args
        ('green: all bindings, labels and actions', dict(), 0, [], ['v2_table_present',
         'v2_table_identical', 'v2_table_columns', 'v1_table_present', 'v1_table_identical',
         'decisions_reported', 'row_decisions_consistent'], ()),
        ('do-nothing: no manifest at rev', dict(claim='none', v2_freeze=ABSENT), 2, [], [], ()),
        ('v2 block removed after freeze', dict(v2_rev=ABSENT), 1,
         ['v2_table_present', 'v2_table_identical'], [], ()),
        ('v2 table edited after freeze', dict(v2_rev=V2_ROWS + [
            ['`extra`', '`*`', '`*`', 'extra', '`report-only`', '`corpus/k.md:9-9`']]), 1,
         ['v2_table_identical'], [], ()),
        ('v1 table edited after freeze', dict(v1_rev=V1_ROWS + [
            ['`x`', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`', 'other -> x', '`corpus/k.md:9-9`']]),
         1, ['v1_table_identical'], [], ()),
        ('v1 block removed at rev', dict(v1_rev=ABSENT), 1,
         ['v1_table_identical'], ['v1_table_present'], ()),
        ('seed != freeze', dict(seed='zero'), 1, ['seed_matches_freeze'], [], ()),
        ('manifest added before freeze', dict(claim='befreeze'), 1,
         ['manifest_after_freeze', 'seed_matches_freeze'], [], ()),
        ('envelope before manifest', dict(claim='split'), 1, ['manifest_before_envelopes'], [], ()),
        ('interpreter edited after freeze', dict(muts={'edit_interp'}), 2, [], [], ()),
        ('generator edited after freeze', dict(muts={'edit_gen'}), 2, [], [], ()),
        ('claims edited after freeze', dict(muts={'edit_claims'}), 2, [], [], ()),
        ('counter edited after freeze', dict(muts={'edit_counter'}), 2, [], [], ()),
        ('carrier not committed as pinned', dict(muts={'carrier_corrupt'}), 1,
         ['carriers_committed'], [], ()),
        ('subject digest mismatch', dict(muts={'digest_mismatch'}), 1, ['envelopes_valid'], [], ()),
        ('missing envelope', dict(muts={'missing_envelope'}), 1, ['envelopes_valid'], [], ()),
        ('3 carriers in one class', dict(muts={'class_count3'}), 1,
         ['classes_two_each', 'n_equals_twice_classes'], [], ()),
        ('one wrong expected label', dict(muts={'mislabel'}), 1, [], [], ()),
        ('label right, action wrong', dict(muts={'wrong_action'}), 1, [], [], ()),
        ('envelopes swapped between carriers', dict(muts={'swap_digest'}), 1,
         ['envelopes_valid'], [], ()),
        ('best table plus a `*` default row instead of the domain guard',
         dict(v2_freeze=V2_ROWS[:2] + [['`clean`', '`*`', '`*`', '*', '`inspect`',
                                       '`corpus/k.md:9-9`']]), 1, [], [], ()),
        ('catch-all table', dict(v2_freeze=[['`clean`', '`*`', '`*`', '*', '`inspect`',
                                             '`corpus/k.md:3-3`']]), 1, [], [], ()),
        ('truncated table (unclassified fallthrough)',
         dict(v2_freeze=[V2_ROWS[0]]), 1, [], [], ()),
        ('generator object with matching sha', dict(gen_obj='good'), 0,
         [], ['generator_sha_matches_freeze'], ()),
        ('generator object with wrong sha', dict(gen_obj='bad'), 1,
         ['generator_sha_matches_freeze'], [], ()),
        ('envelope path omitted, sibling inferred', dict(muts={'omit_envelope'}), 0, [], [], ()),
        ('two carriers share one carrier path', dict(muts={'share_carrier_path'}), 1,
         ['carrier_paths_unique'], [], ()),
        ('full CLI envelope ok/data/meta', dict(muts={'full_envelope'}), 0, [], [], ()),
        ('lane-root-relative carrier and envelope paths', dict(muts={'lane_relative_paths'}),
         0, [], [], ()),
        ('tab interface with row column', dict(mode='tab3row'), 0, [], ['decisions_reported'], ()),
        ('tab interface, rows from --table-only', dict(mode='tab3'), 0,
         [], ['decisions_reported'], ()),
        ('tab interface, no row and no --table-only', dict(mode='notable'), 1,
         ['decisions_reported', 'row_decisions_consistent'], [], ()),
        ('json results without row index', dict(mode='norow'), 0, [], ['decisions_reported'], ()),
        ('interpreter reports rows only, pair read off the v2 table',
         dict(mode='rowonly'), 0, [], ['decisions_reported', 'row_decisions_consistent'], ()),
        ('interpreter numbers rows from 1, pair read off the v2 table',
         dict(mode='rowonly1'), 0, [], ['decisions_reported', 'row_decisions_consistent'], ()),
        ('interpreter reports rows only and v2 header lacks action',
         dict(mode='rowonly', v2_header=['label', 'operation', 'provider', 'class', 'source'],
              v2_freeze=[['`clean`', '`extract_firmware`', '`unblob`', 'clean',
                          '`corpus/k.md:3-3`'],
                         ['`dep-missing-be`', '`extract_firmware`', '`unblob`',
                          'dep-missing-be', '`corpus/k.md:4-4`'],
                         ['`unclassified`', '`*`', '`*`', 'out-of-domain',
                          '`corpus/k.md:5-5`']]), 1, ['v2_table_columns'], [], ()),
        ('interpreter fails outright', dict(mode='fail'), 2, [], [], ()),
        ('v2 header without action column',
         dict(v2_header=['label', 'operation', 'provider', 'class', 'source'],
              v2_freeze=[['`clean`', '`extract_firmware`', '`unblob`', 'clean',
                          '`corpus/k.md:3-3`']]), 1, ['v2_table_columns'], [], ()),
        ('manifest unparsable', dict(muts={'bad_manifest'}), 2, [], [], ()),
        ('unknown revision', dict(), 2, [], [], ('--rev', 'deadbeef' * 5)),
        ('freeze not ancestor of rev', dict(), 2, [], [], ('NONANCESTOR',)),
        ('explicit --base equal to derived base', dict(), 0, [], ['v1_table_identical'], ('BASE',)),
    ]
    green = red = 0
    for name, params, want, want_false, want_true, extra in cases:
        d = None
        try:
            d, freeze, rev = build(params)
            extra_args = []
            base_commit = None
            if extra == ('NONANCESTOR',):
                extra_args = ['--rev', freeze, '--freeze', rev]
            elif extra == ('BASE',):
                base_commit = subprocess.run(
                    ['git', '-C', d, 'rev-list', '--max-parents=0', 'HEAD'],
                    capture_output=True, text=True).stdout.split()[0]
                extra_args = ['--base', base_commit]
            elif extra:
                extra_args = list(extra)
            pr, rec = run_counter(d, rev, freeze, extra_args)
            got = pr.returncode
            ok = got == want
            if rec is None:
                ok = False
                fails.append('%s: no receipt written (stderr=%r)' % (name, pr.stderr[-400:]))
            else:
                if rec.get('exit_code') != got:
                    ok = False
                    fails.append('%s: receipt exit_code %r != process exit %d'
                                 % (name, rec.get('exit_code'), got))
                if got in (0, 1):
                    if rec.get('met_target_consistent') is not True:
                        ok = False
                        fails.append('%s: met_target_consistent false' % name)
                    for k in want_false:
                        if rec.get('bindings', {}).get(k) is not False:
                            ok = False
                            fails.append('%s: binding %s not false (got %r)'
                                         % (name, k, rec.get('bindings', {}).get(k)))
                    for k in want_true:
                        if rec.get('bindings', {}).get(k) is not True:
                            ok = False
                            fails.append('%s: binding %s not true (got %r)'
                                         % (name, k, rec.get('bindings', {}).get(k)))
                    if got == 0 and not rec.get('met_target'):
                        ok = False
                        fails.append('%s: exit 0 without met_target' % name)
                    if got == 0 and rec.get('distinct_decisions') != len(
                            set(r.get('row') for r in rec.get('carriers', []))):
                        ok = False
                        fails.append('%s: distinct_decisions mismatch' % name)
            if ok:
                st = subprocess.run(['git', '-C', d, 'status', '--porcelain'],
                                    capture_output=True, text=True).stdout.strip()
                if st:
                    ok = False
                    fails.append('%s: counter dirtied the measured repo: %r' % (name, st[:300]))
            if ok:
                if want == 0:
                    green += 1
                else:
                    red += 1
            elif got != want:
                fails.append('%s: want exit %d got %d (stdout=%r)'
                             % (name, want, got, pr.stdout[-400:]))
        except SystemExit as e:
            fails.append('%s: fixture error %s' % (name, e))
        finally:
            if d:
                shutil.rmtree(d, ignore_errors=True)

    total = len(cases)
    passed = total - len(fails)
    print(json.dumps({'selftest': 'c2-counter r40', 'cases': total, 'green': green,
                      'red': red, 'pass': passed, 'fail': len(fails),
                      'failures': fails}))
    print('SELFTEST cases=%d pass=%d fail=%d' % (total, passed, len(fails)))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
