#!/usr/bin/env python3
"""R49-C1 controls: build each counterfactual input tree and score it with the frozen counter.

The claim is `plans/round-49-claims.md` `## R49-C1`; the controls are the ones it
names (CTL-C1-0/1/2/3 plus CTL-C1-4/5 added by the freeze review, plus the K3
positive control CTL-C1-POS). Every control is a *counterfactual*: it plants
bytes at the round-49 evidence path in a scratch git clone of the lane, commits
them after the freeze, and runs the frozen counter against that clone. The
receipt records what the counter actually did (exit code, stdout sha256, wall
time) and whether that is what the claim says must happen.

Nothing here is simulated. The counter is invoked as a subprocess with the argv
frozen in the claim:

    python3 -I -B tools/round-49/c1-counter.py --root <LANE> --rev <REV> \
        --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 package root> \
        --work <SCRATCH> --json-out <OUT>

The lane is never written: every planted tree lives in a `git clone --shared`
sandbox under `--work`, which is why a control may commit receipts without
touching the lane's VCS. (`git rev-parse --show-toplevel` is asserted against
the sandbox before any commit.)

Controls
  CTL-C1-0   do-nothing: the counter at the freeze, receipts absent.
             Expect exit 1, carriers_matched 0, every documentation binding false.
  CTL-C1-1   the round-42 C1 (v3) after-receipts relabelled onto the round-49
             carrier ids. Expect non-zero: a v3 receipt cannot satisfy a v1/v2
             predicate (subject digest, handler and superblock all disagree).
  CTL-C1-2   an "oracle-only" envelope whose published-file claims are computed
             from the carriers.json oracle with NO real REA run, re-minted
             through the frozen xpin rule so only the run itself is fabricated.
             Expect non-zero on the counter-time rerun-projection binding.
             A projection-identical fabrication would reach the target and is
             the claim's kill rule, so the receipt records the failing clauses.
  CTL-C1-3   a receipt captured with `sasquatch` stripped from the child PATH.
             Expect non-zero with a `missing-extractor-dependency` gap, never a
             clean match.
  CTL-C1-4   copy last round's run: the committed round-44 after-receipts of the
             same four carriers, planted verbatim at the round-49 evidence path.
             Expect non-zero, carriers_matched 0, `run_provenance_ok` false: their
             output_directory is a round-44 scratch path. (A copy whose path was
             rewritten and whose evidence id was re-minted is NOT refused; the plan
             discloses that limit. The counter-time REA rerun is what measures REA.)
  CTL-C1-5   (retired from the default set: it planted mutated bytes where the counter
             never reads them and could not fail. The superblock probe is witnessed by
             the counter's `--selftest` cases, not by this driver.)
  CTL-C1-POS the positive control (K3): real REA 6.5.0 receipts for every scored
             carrier, captured in scratch as a dev arm, planted and committed
             under corpus/evidence/round-49/c1 in the sandbox only. Expect exit
             0 with carriers_matched == the scored-carrier count and every
             binding true. Red-only controls cannot distinguish a counter that
             works from one that always fails; this one can.

Exit codes (semantic, per the round contract)
  0  every control behaved as its claim says it must (the kill rule did not fire)
  1  a control misbehaved: a red control reached the target, or a positive
     control failed to reach it
  2  could not evaluate (counter absent, carriers.json unreadable, sandbox or
     capture failure) - never counts toward a target

Usage
  c1-controls.py --root LANE --freeze REV --counter PATH --pkg65 PKG \
      --work DIR --out DIR [--controls c0,c1,c2,c3,c4,pos] [--json-out FILE]
  c1-controls.py ... --build-only          # build input trees, do not score
  c1-controls.py --selftest                # driver machinery only, stub counter
  c1-controls.py --capture-only --root LANE --work DIR   # REA dev-arm captures

Honors TMPDIR/HYAKU_SCRATCH; writes only --out, --work and --json-out.
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
import time

SEAT = 'R49C1Controls'
CLAIM = 'R49-C1'
CARRIERS = 'tools/round-49/carriers.json'
EVIDENCE = 'corpus/evidence/round-49/c1'
CONTROLS_OUT = '.ufo/waves/round-49/controls'
# Control inputs are CONTENT-ADDRESSED and must be committable with the freeze:
# the freeze helper forbids committing `.ufo/**`, so the planted bytes live under
# `tools/round-49/control-fixtures/` and `.ufo` keeps only transcripts/receipts.
FIXTURES = 'tools/round-49/control-fixtures'


def write_fixtures(fixtures_root, key, tree, expect, extras=None):
    """Write a control's planted bytes under the committable fixtures root.

    One directory per control, the planted tree preserved under it, and a
    manifest mapping every destination to its fixture file, sha256 and size.
    A later score reads the manifest, so the scored bytes are the committed
    ones rather than a fresh rebuild."""
    base = os.path.join(fixtures_root, key)
    manifest = {'control': key, 'expect': expect, 'files': {}}
    for rel, raw in sorted(tree.items()):
        dest = os.path.join(base, rel)
        os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
        with open(dest, 'wb') as fh:
            fh.write(raw)
        manifest['files'][rel] = {'fixture': os.path.relpath(dest, fixtures_root),
                                  'sha256': sha256_bytes(raw), 'size': len(raw)}
    for k, v in (extras or {}).items():
        manifest[k] = v
    write_json(os.path.join(base, 'manifest.json'), manifest)
    return manifest


def load_fixtures(fixtures_root, key):
    """(tree, manifest) read from the committed fixtures, or (None, None)."""
    mpath = os.path.join(fixtures_root, key, 'manifest.json')
    if not os.path.isfile(mpath):
        return None, None
    try:
        manifest = read_json(mpath)
    except (OSError, json.JSONDecodeError):
        return None, None
    tree = {}
    for rel, meta in (manifest.get('files') or {}).items():
        fp = os.path.join(fixtures_root, meta['fixture'])
        try:
            with open(fp, 'rb') as fh:
                raw = fh.read()
        except OSError:
            return None, None
        if sha256_bytes(raw) != meta['sha256']:
            raise Uneval('fixture %s does not hash to its manifest pin' % fp)
        tree[rel] = raw
    return tree, manifest


XPIN = 'tools/round-27/xpin-attribute.mjs'
XPIN_VENDORED = 'tools/round-49/xpin-attribute.mjs'
R42_C1 = 'corpus/evidence/round-42/c1'
HELDOUT = 'corpus/evidence/round-42/c2/heldout'
REA_PIN = 'rea-agents@6.5.0'
PROV_SEGMENT = '/kaidoku-r49/'
CHUNK_DIR = 'firmware.bin_extract'
CHUNK_LEN = 4096

# Carrier ids whose handler is the v1/v2 family this claim promotes.
V12_HANDLERS = ('squashfs_v1', 'squashfs_v2')

# The documentation bindings the do-nothing control must find false. The
# counter owns the exact names; these are the claim's set, and a name the
# counter does not emit is reported as `absent` rather than silently passed.
DOC_BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
                'entry_present', 'sourced', 'coverage_map_row')


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path):
    try:
        with open(path, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def write_json(path, doc):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write('\n')
    os.replace(tmp, path)


def read_json(path):
    with open(path) as fh:
        return json.load(fh)


# ------------------------------------------------------------------ git

def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(args),
                                         p.stderr.decode(errors='replace').strip()))
    return p


def show(root, rev, path):
    p = git(root, 'show', '%s:%s' % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


def assert_toplevel(sandbox):
    """A sandbox commit is only safe when git agrees the sandbox is its own repo."""
    p = git(sandbox, 'rev-parse', '--show-toplevel')
    top = p.stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(sandbox):
        raise SystemExit('sandbox toplevel mismatch: %r != %r' % (top, sandbox))


def make_sandbox(root, freeze, work, name):
    """A `git clone --shared` of the lane at `freeze`, detached, in scratch."""
    dest = os.path.join(work, 'sandbox-' + name)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    p = subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--quiet',
                        os.path.abspath(root), dest], capture_output=True)
    if p.returncode != 0:
        raise SystemExit('clone failed: ' + p.stderr.decode(errors='replace'))
    assert_toplevel(dest)
    # a committer identity that is obviously not the lane's
    for key, val in (('user.name', 'r49-c1-controls'),
                     ('user.email', 'controls@r49.invalid'),
                     ('commit.gpgsign', 'false')):
        git(dest, 'config', key, val)
    git(dest, 'checkout', '--quiet', '--detach', freeze)
    return dest


def plant_and_commit(sandbox, files, message):
    """Write `files` ({relpath: bytes}) into the sandbox and commit them.

    Returns the new revision. The commit is what makes a planted receipt a
    strict descendant of the freeze, which is the counter's `receipt_fresh`
    clause; the files themselves are byte-exact, so a control that expects a
    digest to disagree does so for a stated reason."""
    assert_toplevel(sandbox)
    for rel, raw in files.items():
        full = os.path.join(sandbox, rel)
        os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(raw)
    git(sandbox, 'add', '--', *sorted(files))
    git(sandbox, 'commit', '--quiet', '-m', message)
    return git(sandbox, 'rev-parse', 'HEAD').stdout.decode().strip()


# ------------------------------------------------------------------ carriers

def carriers_at(root, rev, override=None):
    """The frozen carrier table: scored ids, their handler, pin and oracle rows.

    `scope.target_ids` and `scope.exploratory_ids` are the freeze's own statement
    of which entries are scored; when present they win over the raw list, so the
    tool follows the frozen scope instead of a hard-coded count. A table with no
    `scope` block scores every entry.

    `override` names a worktree file to read instead of the frozen blob. It exists
    only for the pre-freeze dev arm (the oracle block lands with the freeze); a
    scored run must use the frozen bytes, so the override is refused whenever
    `--counter` is actually executed."""
    if override:
        try:
            with open(override, 'rb') as fh:
                raw = fh.read()
        except OSError as e:
            raise Uneval('--carriers unreadable: %s' % e)
    else:
        raw = show(root, rev, CARRIERS)
    if raw is None:
        raise Uneval('carriers.json absent at %s' % rev)
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        raise Uneval('carriers.json unreadable: %s' % e)
    entries = [c for c in doc.get('carriers') or [] if isinstance(c, dict)]
    if not entries:
        raise Uneval('carriers.json lists no carriers')
    scope = doc.get('scope') if isinstance(doc.get('scope'), dict) else {}
    want = scope.get('target_ids') or []
    if want:
        by_fixture = {c.get('fixture_id'): c for c in entries}
        by_id = {c.get('id'): c for c in entries}
        scored = []
        for key in want:
            hit = by_id.get(key) or by_fixture.get(key)
            if hit is None:
                raise Uneval('scope.target_ids names %r, absent from carriers' % (key,))
            scored.append(hit)
    else:
        scored = entries
    for c in scored:
        if not c.get('handler'):
            raise Uneval('carrier %r has no handler' % (c.get('id'),))
        if not (c.get('sha256') or '').strip():
            raise Uneval('carrier %r has no pin' % (c.get('id'),))
    return {'doc': doc, 'all': entries, 'scored': scored,
            'exploratory': [c for c in entries if c not in scored],
            'target': len(scored)}


def oracle_members(carrier):
    orc = carrier.get('oracle') if isinstance(carrier.get('oracle'), dict) else {}
    rows = [m for m in orc.get('members') or [] if isinstance(m, dict)]
    return [m for m in rows if m.get('type') in (None, 'regular') and m.get('path')]


def receipt_path(cid):
    return '%s/%s/after.json' % (EVIDENCE, cid)


# ------------------------------------------------------------------ envelope

def mint_evidence_ids(work, pkg65, envelopes):
    """Re-mint evidence ids through the frozen rule (the package's own projection).

    The counter recomputes each receipt's id from the record it reads, so a
    fabrication that keeps a stale id reds on `evidence_id_ok` instead of on the
    clause the control is probing. Minting with the same frozen tool keeps each
    control attributable to the clause it names."""
    xpin = None
    for cand in (XPIN_VENDORED, XPIN):
        if os.path.isfile(cand):
            xpin = os.path.abspath(cand)
            break
    if xpin is None:
        raise Uneval('no xpin tool at %s or %s' % (XPIN_VENDORED, XPIN))
    if pkg65 is None or not os.path.isdir(pkg65):
        raise Uneval('--pkg65 must name the rea-agents 6.5.0 package root')
    paths = []
    for key, env in envelopes.items():
        p = os.path.join(work, 'mint-%s.json' % key)
        write_json(p, {'data': env})
        paths.append(p)
    r = subprocess.run(['node', xpin, '--pkg65', pkg65, '--pkg67', pkg65] + paths,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Uneval('xpin mint failed: ' + r.stderr.strip()[:400])
    lines = [ln for ln in r.stdout.splitlines() if ln]
    if len(lines) != len(paths):
        raise Uneval('xpin line count %d != %d' % (len(lines), len(paths)))
    out = {}
    for (key, _), line in zip(envelopes.items(), lines):
        out[key] = line.split('\t')[2]
    return out


def envelope(carrier, outdir, *, files, handler=None, gaps=(), diagnostics=(),
             chunk_failed=False, evidence_id=None, chunk_len=CHUNK_LEN,
             coverage='complete', engine_version='26.6.4'):
    """A receipt-shaped REA 6.5.0 `data` object (the shape after.json carries).

    `files` is [(rel, sha256, size)] published under the chunk extract dir, which
    is the layout a real whole-file SquashFS chunk produces on these fixtures."""
    handler = handler or carrier['handler']
    pin = carrier['sha256']
    chunk_dir = CHUNK_DIR
    published = 0
    rel_files = []
    for rel, sha, size in files:
        published += size
        rel_files.append({
            'relative_path': '%s/%s' % (chunk_dir, rel),
            'path': '%s/%s/%s' % (outdir, chunk_dir, rel),
            'size': size, 'sha256': sha, 'reported_sha256': None,
            'mime_type': None, 'analysis_depth': None, 'runtime_address': None,
            'original_file_range': None,
        })
    gap_rows = []
    for kind, rel, deps in gaps:
        gap_rows.append({
            'kind': kind,
            'input_path': '$output/%s' % chunk_dir if rel is None
                          else '$output/%s/%s' % (chunk_dir, rel),
            'relative_path': None if rel is None else '%s/%s' % (chunk_dir, rel),
            'handler': handler if kind == 'missing-extractor-dependency' else None,
            'provider_id': None, 'range': None, 'root_file_range': None,
            'dependencies': list(deps), 'continuation_id': 'control-continuation',
        })
    diag_rows = []
    for typename, missing in diagnostics:
        diag_rows.append({
            'input_path': '$input', 'stage': handler,
            'missing_dependencies': list(missing),
            'report': {'__typename__': typename, 'severity': 'ERROR',
                       'dependencies': list(missing)},
        })
    return {
        'evidence_id': evidence_id or 'ev_' + '0' * 64,
        'subject': {'name': os.path.basename(carrier.get('path') or 'fixture.bin'),
                    'digest': {'sha256': pin},
                    'local_path': '/scratch/%s' % os.path.basename(
                        carrier.get('path') or 'fixture.bin'),
                    'format': 'file', 'architecture': None},
        'provider': {'id': 'unblob', 'name': 'Unblob', 'version': engine_version},
        'analysis_profile': None,
        'predicate_type': 'rea.analysis',
        'operation': 'extract_firmware',
        'parameters': {'path': '/scratch/%s' % os.path.basename(
                           carrier.get('path') or 'fixture.bin'),
                       'output_directory': outdir,
                       'max_depth': 3,
                       'max_output_bytes': 268435456,
                       'max_output_files': 10000},
        'raw_result': {'report': [], 'execution': {}, 'version_execution': {}},
        'normalized_result': {
            'engine': {'name': 'unblob', 'version': engine_version,
                       'executable_path': '/usr/bin/unblob',
                       'executable_sha256': None, 'source_revision': None,
                       'worker_count': 1},
            'selection': {'offset': 0, 'length': chunk_len, 'sha256': pin},
            'output_directory': outdir,
            'coverage': coverage,
            'files': rel_files,
            'unpublished_entries': [],
            'chunks': [{'input_path': '$input', 'provider_id': '1:1',
                        'range': {'offset': 0, 'length': chunk_len},
                        'handler': handler, 'encrypted': False,
                        'root_file_range': {'offset': 0, 'length': chunk_len},
                        'extraction_failed': chunk_failed}],
            'derivations': [] if chunk_failed else [
                {'parent_path': '$input',
                 'child_path': '$output/%s' % chunk_dir,
                 'provider_blob_id': '1:1', 'handler': handler,
                 'parent_file_range': {'offset': 0, 'length': chunk_len}}],
            'depth_limited_paths': [],
            'diagnostics': diag_rows,
            'extraction_gaps': gap_rows,
            'extraction_continuations': [],
            'published_bytes': published,
        },
    }


# ------------------------------------------------------------------ REA dev arm

def fixed_path():
    return ':'.join(['/usr/local/bin', '/usr/bin', '/bin',
                     os.path.expanduser('~/.local/bin'),
                     os.path.expanduser('~/.local/share/fnm/node-versions/'
                                        'v24.21.0/installation/bin')])


def stripped_path(work):
    """A PATH with every executable of the fixed PATH except `sasquatch`.

    The extractor is what unblob resolves on the child PATH; removing only
    sasquatch (and nothing else) is the CTL-C1-3 condition, and it is built by
    symlinking the other names into a scratch bin so `node`/`npx`/`unblob`
    keep working."""
    bindir = os.path.join(work, 'pathbin')
    os.makedirs(bindir, exist_ok=True)
    kept = missing = 0
    for d in fixed_path().split(':'):
        if not d or not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name == 'sasquatch':
                continue
            src = os.path.join(d, name)
            dst = os.path.join(bindir, name)
            if os.path.exists(dst) or not (os.path.isfile(src) or os.path.islink(src)):
                continue
            if not os.access(src, os.X_OK):
                continue
            try:
                os.symlink(src, dst)
                kept += 1
            except OSError:
                pass
    for d in fixed_path().split(':'):
        if os.path.isfile(os.path.join(d, 'sasquatch')):
            missing += 1
    return bindir, kept, missing


def capture_real(work, carrier, root, *, strip_sasquatch=False):
    """Run REA 6.5.0 `extract-firmware` on the carrier bytes (the dev arm).

    A dev-arm capture, never the after-side data procedure: the output directory
    is under `--work`, and nothing is written into the lane. Returns the `data`
    object of the envelope. `strip_sasquatch` removes the extractor from the
    child PATH, which is what CTL-C1-3 probes."""
    src = os.path.join(root, carrier['path'])
    if not os.path.isfile(src):
        raise Uneval('carrier fixture absent: %s' % carrier['path'])
    raw = open(src, 'rb').read()
    if sha256_bytes(raw) != carrier['sha256']:
        raise Uneval('carrier %s does not hash to its frozen pin' % carrier.get('id'))
    staged = os.path.join(work, 'rea-%s.bin' % carrier['id'])
    with open(staged, 'wb') as fh:
        fh.write(raw)
    outdir = os.path.join(work, 'rea-%s-out' % carrier['id'])
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    env = dict(os.environ)
    env['PATH'] = fixed_path()
    if strip_sasquatch:
        bindir, kept, missing = stripped_path(work)
        # REPLACE the child PATH: prepending would leave ~/.local/bin (where
        # sasquatch lives) resolvable behind the shim and the capture would
        # silently succeed, which is the one thing this control must not do.
        env['PATH'] = bindir
        if missing == 0:
            raise Uneval('sasquatch is not on the fixed PATH: nothing to strip')
        if shutil.which('sasquatch', path=bindir):
            raise Uneval('sasquatch still resolves under the stripped PATH')
        if not shutil.which('npx', path=bindir):
            raise Uneval('npx does not resolve under the stripped PATH: the '
                         'capture cannot run')
    argv = ['npx', '-y', REA_PIN, 'extract-firmware', '--format', 'json',
            '--full-output', staged, outdir]
    r = subprocess.run(argv, capture_output=True, env=env, cwd=work)
    if r.returncode != 0 and not r.stdout:
        raise Uneval('REA failed: ' + r.stderr.decode(errors='replace')[:400])
    try:
        doc = json.loads(r.stdout)
    except json.JSONDecodeError as e:
        raise Uneval('REA stdout is not JSON: %s' % e)
    data = doc.get('data') if isinstance(doc, dict) else None
    if not isinstance(data, dict):
        raise Uneval('REA envelope has no data object')
    return data


# ------------------------------------------------------------------ counter

class Uneval(Exception):
    """Could not evaluate (exit 2): never counts toward a target."""


def run_counter(counter, root, rev, freeze, pkg65, work, json_out):
    """Invoke the frozen counter as a subprocess; return its measured receipt.

    The counter is run with `cwd=work`, so `--json-out` must be absolute or it
    lands relative to the scratch directory (and the counter dies on the write).
    The verdict is also recoverable from stdout, which the counter prints as the
    same document, so a lost file is not a lost measurement."""
    json_out = os.path.abspath(json_out)
    argv = [sys.executable, '-I', '-B', counter,
            '--root', root, '--rev', rev, '--freeze', freeze,
            '--pkg65', pkg65, '--work', work, '--json-out', json_out]
    t0 = time.time()
    r = subprocess.run(argv, capture_output=True, cwd=work)
    wall = round(time.time() - t0, 3)
    stdout = r.stdout
    doc = None
    if os.path.isfile(json_out):
        try:
            doc = read_json(json_out)
        except (OSError, json.JSONDecodeError):
            doc = None
    if doc is None:
        # the counter prints its receipt on stdout as well; use it only when it
        # is a JSON object, so a crash trace can never be read as a verdict
        try:
            maybe = json.loads(stdout.decode(errors='replace') or 'null')
            if isinstance(maybe, dict):
                doc = maybe
        except (json.JSONDecodeError, UnicodeDecodeError):
            doc = None
    return {'argv': argv, 'exit_code': r.returncode, 'wall_s': wall,
            'stdout_sha256': sha256_bytes(stdout),
            'stdout_tail': stdout.decode(errors='replace').strip().splitlines()[-6:],
            'stderr_tail': r.stderr.decode(errors='replace').strip().splitlines()[-6:],
            'receipt': doc,
            'receipt_source': ('json-out file' if os.path.isfile(json_out)
                               else 'stdout' if doc is not None else None)}


def receipt_summary(doc):
    """Pull the verdict shape out of a counter receipt without guessing key names.

    The counter owns its schema; these are the names the claim and the round-42
    port use, and anything absent is reported as absent rather than defaulted to
    true (a default would let a schema change read as a pass)."""
    if not isinstance(doc, dict):
        return {'present': False}
    bindings = doc.get('bindings') if isinstance(doc.get('bindings'), dict) else {}
    carriers = doc.get('carriers') if isinstance(doc.get('carriers'), dict) else {}
    # The frozen counter emits each per-carrier failure as "<id>:<clause>" and the
    # binding failures as `bindings_false`. Both spellings are kept, and the bare
    # clause name is derived so a control can name the clause it expects to fire.
    raw_failing = doc.get('failing') or doc.get('failing_clauses') or []
    failing = []
    for item in raw_failing:
        if not isinstance(item, str):
            continue
        failing.append(item)
        if ':' in item:
            failing.append(item.split(':', 1)[1])
    failing = sorted(set(failing))
    bindings_false = doc.get('bindings_false')
    if not isinstance(bindings_false, list):
        bindings_false = sorted(k for k, v in bindings.items() if v is not True)
    if not failing and carriers:
        names = ('carrier_present', 'carrier_pin_ok', 'carrier_size_ok',
                 'carrier_fresh_ok', 'layout_ok', 'carve_ok', 'oracle_ok',
                 'tree_ok', 'receipt_present', 'receipt_fresh',
                 'evidence_envelope_ok', 'subject_pin_ok', 'operation_ok',
                 'handler_ok', 'chunks_ok', 'oracle_hits_ok', 'gaps_ok',
                 'nonregular_unpublished_ok', 'path_shape_ok',
                 'run_provenance_ok', 'evidence_id_ok', 'projection_ok')
        failing = sorted({n for c in carriers.values() if isinstance(c, dict)
                          for n in names if c.get(n) is not True})
        bindings_false = sorted(k for k, v in bindings.items() if v is not True)
    out = {
        'present': True,
        'met_target': doc.get('met_target'),
        'carriers_matched': doc.get('carriers_matched'),
        'target': doc.get('target'),
        'frozen_path_changed': doc.get('frozen_path_changed'),
        'projection_profile': doc.get('projection_profile'),
        'bindings': {k: v for k, v in bindings.items()},
        'failing_clauses': failing,
        'bindings_false': bindings_false,
        'per_carrier_failing': {
            k: sorted(n for n, v in c.items()
                      if isinstance(v, bool) and v is False)
            for k, c in carriers.items() if isinstance(c, dict)
        } if carriers else {},
        'exit_code': doc.get('exit_code'),
        'counter_sha256': doc.get('counter_sha256'),
        'counter_sha256_at_freeze': doc.get('counter_sha256_at_freeze'),
    }
    return out


# ------------------------------------------------------------------ controls

def control_c0(ctx):
    """Do-nothing: the counter at the freeze with no after-receipts present."""
    sandbox = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], 'c0')
    rev = ctx['freeze']
    expect = {'exit': 'exit1', 'carriers_matched': 0,
              'doc_bindings_all_false': True}
    return {'tree': {}, 'root': sandbox, 'rev': rev, 'expect': expect,
            'title': 'do-nothing: the counter at the freeze',
            'note': 'a do-nothing round cannot reach the target; every '
                    'documentation binding must be false'}


def control_c1(ctx):
    """Round-42 C1 (v3) receipts relabelled onto the round-49 carrier ids.

    A v3 receipt has a v3 subject digest, a `squashfs_v3*` handler and a v3
    superblock: three independent disagreements with a v1/v2 predicate."""
    r42 = [d for d in sorted(os.listdir(os.path.join(ctx['root'], R42_C1)))
           if os.path.isdir(os.path.join(ctx['root'], R42_C1, d))]
    if not r42:
        raise Uneval('no round-42 C1 receipt directories to relabel')
    files, mapping = {}, []
    for i, carrier in enumerate(ctx['carriers']['scored']):
        src_id = r42[i % len(r42)]
        src = '%s/%s/after.json' % (R42_C1, src_id)
        raw = show(ctx['root'], ctx['freeze'], src)
        if raw is None:
            raise Uneval('round-42 receipt %s absent at the freeze' % src)
        dst = receipt_path(carrier['id'])
        files[dst] = raw
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            doc = {}
        mapping.append({'carrier': carrier['id'], 'source': src,
                        'source_dir': src_id,
                        'source_sha256': sha256_bytes(raw),
                        'source_subject': ((doc.get('subject') or {})
                                           .get('digest') or {}).get('sha256'),
                        'source_handlers': [c.get('handler') for c in
                                            ((doc.get('normalized_result') or {})
                                             .get('chunks') or [])],
                        'destination': dst})
    sandbox = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], 'c1')
    rev = plant_and_commit(sandbox, files,
                           'CTL-C1-1: round-42 v3 receipts at the round-49 paths')
    return {'tree': files, 'root': sandbox, 'rev': rev, 'mapping': mapping,
            'expect': {'exit': 'non-zero', 'carriers_matched': 0,
                       'failing_any': ['subject_pin_ok', 'handler_ok', 'layout_ok']},
            'title': 'round-42 v3 receipts relabelled onto the round-49 carriers',
            'note': 'v3 receipts cannot pass a v1/v2 predicate: subject digest, '
                    'handler and superblock all disagree'}


def control_c2(ctx):
    """Oracle-only fabrication: published-file claims from the oracle, no REA run.

    The published file list, sizes and digests are exactly the oracle's, so
    every oracle-visible clause can hold; what is missing is the run itself. The
    evidence id is re-minted through the frozen rule, so a red is attributable to
    the counter-time rerun projection and not to a stale id."""
    files, fabrication = {}, []
    envs = {}
    for carrier in ctx['carriers']['scored']:
        members = oracle_members(carrier)
        if not members:
            raise Uneval('carrier %s has no oracle members' % carrier['id'])
        # the counter's run_provenance_ok requires an absolute path inside its
        # /kaidoku-r49/ scratch segment (PROV_SEGMENT); c1-run.py records the same
        # shape, so the fabrication uses it and the only difference is the run.
        outdir = ('/fast/scratch/hyaku/kaidoku-r49/c1-controls-c2/%s/extract'
                  % carrier['id'])
        env = envelope(carrier, outdir,
                       files=[(m['path'], m['sha256'], int(m['size']))
                              for m in members])
        envs[carrier['id']] = env
        fabrication.append({'carrier': carrier['id'],
                            'handler': carrier['handler'],
                            'output_directory': outdir,
                            'published': [(m['path'], m['sha256'], m['size'])
                                          for m in members],
                            'real_rea_run': False})
    minted = mint_evidence_ids(ctx['work'], ctx['pkg65'], envs)
    for cid, env in envs.items():
        env['evidence_id'] = minted[cid]
        files[receipt_path(cid)] = (json.dumps(env, indent=1, sort_keys=True)
                                    + '\n').encode()
    sandbox = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], 'c2')
    rev = plant_and_commit(sandbox, files,
                           'CTL-C1-2: oracle-only fabrication, no REA run')
    return {'tree': files, 'root': sandbox, 'rev': rev,
            'fabrication': fabrication,
            'expect': {'exit': 'non-zero', 'evidence_ids_minted': True,
                       'failing_includes': ['projection_ok']},
            'title': 'oracle-only fabrication with a re-minted evidence id',
            'note': 'the published-file claims are the oracle; the run is not. '
                    'A fabrication whose projection equals a real run would '
                    'reach the target, which is the claim kill rule'}


def control_c3(ctx):
    """A receipt captured with sasquatch stripped from the child PATH."""
    carrier = ctx['carriers']['scored'][0]
    data = capture_real(ctx['work'], carrier, ctx['root'], strip_sasquatch=True)
    nr = data.get('normalized_result') or {}
    gaps = [g.get('kind') for g in nr.get('extraction_gaps') or []]
    chunk_failed = any(c.get('extraction_failed') for c in nr.get('chunks') or [])
    published = [f.get('relative_path') for f in nr.get('files') or []]
    if 'missing-extractor-dependency' not in gaps:
        raise Uneval('stripped-PATH capture produced no '
                     'missing-extractor-dependency gap (gaps=%r)' % (gaps,))
    files = {receipt_path(carrier['id']):
             (json.dumps(data, indent=1, sort_keys=True) + '\n').encode()}
    sandbox = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], 'c3')
    rev = plant_and_commit(sandbox, files,
                           'CTL-C1-3: receipt captured without sasquatch on PATH')
    return {'tree': files, 'root': sandbox, 'rev': rev,
            'capture': {'carrier': carrier['id'],
                        'extractor': 'sasquatch',
                        'extractor_on_child_path': False,
                        'gap_kinds': gaps,
                        'chunk_extraction_failed': chunk_failed,
                        'published_files': published,
                        'evidence_id': data.get('evidence_id')},
            'expect': {'exit': 'non-zero', 'carriers_matched': 0,
                       'gap_kind': 'missing-extractor-dependency'},
            'title': 'sasquatch-absent capture: a missing extractor is not a match',
            'note': 'the chunk fails for a named missing dependency; the claim '
                    'requires non-zero with that gap, never a clean carrier match'}


def control_c4(ctx):
    """CTL-C1-4: copy last round's run. The committed round-44 REA after-receipts of the
    same four carriers are planted VERBATIM at the round-49 evidence path (the cheapest
    shortcut that skips the claimed work). Their `parameters.output_directory` still names
    the round-44 scratch segment, so the provenance clause refuses them."""
    files, copied = {}, []
    for carrier in ctx['carriers']['scored']:
        src = 'corpus/evidence/round-44/c1/%s/after.json' % carrier['id']
        raw = show(ctx['root'], ctx['freeze'], src)
        if raw is None:
            raise Uneval('round-44 receipt absent at the freeze: %s' % src)
        dst = receipt_path(carrier['id'])
        files[dst] = raw
        copied.append({'carrier': carrier['id'], 'source': src,
                       'source_sha256': sha256_bytes(raw), 'destination': dst})
    sandbox = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], 'c4')
    rev = plant_and_commit(sandbox, files,
                           'CTL-C1-4: the round-44 receipts copied verbatim')
    return {'tree': files, 'root': sandbox, 'rev': rev, 'copied': copied,
            'expect': {'exit': 'non-zero', 'carriers_matched': 0,
                       'failing_any': ['run_provenance_ok']},
            'title': 'the committed round-44 receipts copied verbatim to the round-49 path',
            'note': 'run_provenance_ok refuses output_directory under /kaidoku-r44/. A '
                    'relabelled copy (output_directory rewritten, evidence id re-minted) '
                    'is NOT refused: plan P49-C1 discloses it as a limit.'}


def control_c5(ctx):
    """Mutated superbytes: the superblock probe must red every mutation.

    The probe reads the carrier bytes at REV, so the mutations are planted as
    carrier copies under the evidence tree and scored through the counter's own
    carrier resolution when the table allows it. Because a frozen table pins the
    bytes, the control also runs the probe directly here and records the byte
    deltas: a probe that accepts a flipped magic would be the finding."""
    mutations = []
    for carrier in ctx['carriers']['scored']:
        raw = show(ctx['root'], ctx['freeze'], carrier['path'])
        if raw is None:
            raise Uneval('carrier %s absent at the freeze' % carrier['path'])
        original = bytearray(raw)
        endian = carrier.get('endian') or 'le'
        s_major_at = 28
        s_minor_at = 30
        arms = []

        def flip(desc, offset, value):
            mutated = bytearray(original)
            before = bytes(mutated[offset:offset + len(value)])
            mutated[offset:offset + len(value)] = value
            arms.append({'arm': desc, 'offset': offset,
                         'before_hex': before.hex(), 'after_hex': value.hex(),
                         'sha256': sha256_bytes(bytes(mutated)),
                         'mutated_bytes': bytes(mutated)})

        flip('bad-magic', 0, b'XXXX')
        flip('swapped-s_major', s_major_at,
             (3).to_bytes(2, 'big' if endian == 'be' else 'little'))
        flip('swapped-s_minor', s_minor_at,
             (9).to_bytes(2, 'big' if endian == 'be' else 'little'))
        mutations.append({'carrier': carrier['id'], 'endian': endian,
                          'frozen_handler': carrier['handler'],
                          'arms': arms})
    # Plant the mutated carriers beside the receipts so the counter's own probe
    # reads them when its table resolution permits; the byte deltas above are
    # the control's own measured statement in every case.
    files = {}
    for m in mutations:
        for a in m['arms']:
            rel = '%s/superbyte-mutation/%s/%s.bin' % (
                CONTROLS_OUT.replace('.ufo/waves/round-49/controls', EVIDENCE),
                m['carrier'], a['arm'])
            files[rel] = a['mutated_bytes']
    for m in mutations:
        for a in m['arms']:
            del a['mutated_bytes']
    sandbox = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], 'c5')
    rev = plant_and_commit(sandbox, files,
                           'CTL-C1-5: mutated superbytes (D-11)') if files else ctx['freeze']
    return {'tree': files, 'root': sandbox, 'rev': rev, 'mutations': mutations,
            'expect': {'exit': 'non-zero', 'carriers_matched': 0,
                       'probe_reds_every_mutation': True},
            'title': 'mutated superbytes: bad magic, swapped s_major, swapped s_minor',
            'note': 'the superblock probe must red every mutation; it is also '
                    'recorded from the byte deltas so the control stands even '
                    'when the frozen table pins the original bytes'}


def _doc_landing(ctx):
    """The C1 landing bytes, read from the wave-1 doc artifacts.

    CTL-C1-POS needs the five documentation bindings to be true as well as the
    carrier evidence, otherwise the positive control cannot reach exit 0 before
    the data lands. The bytes come from the seats that authored them
    (R49C1Doc's three blocks, R49EntryDraft's entry) and are planted ONLY in the
    sandbox, as control fixtures — they are not the landing.

    The `<AFTER-DATA: …>` markers are replaced here: a fixture that plants a
    marker where a landing plants a measured headline would be claiming a result
    it did not measure, and the counter's row checks read the whole row."""
    docdir = ctx.get('doc_dir')
    if not docdir:
        raise Uneval('--doc-dir is required for CTL-C1-POS (the C1 landing blocks)')
    want = {
        'row': 'R49C1Doc/block-a-province-round-49-core-row.md',
        'frontier': 'R49C1Doc/block-b-province-frontier-note.md',
        'readme_row': 'R49C1Doc/block-c-readme-coverage-map-row.md',
        'entry': ('R49EntryDraft/corpus/knowledge/'
                  '2026-10-28-r49-squashfs-v1v2-core.md'),
    }
    got = {}
    for key, rel in want.items():
        p = os.path.join(docdir, rel)
        if not os.path.isfile(p):
            raise Uneval('CTL-C1-POS doc fixture missing: %s' % p)
        with open(p, encoding='utf-8') as fh:
            got[key] = fh.read()
    headline = ('POS control fixture — four real REA 6.5.0 `extract-firmware` receipts '
                'captured in scratch, `carriers_matched 4`, exact `squashfs_v1`/'
                '`squashfs_v2` handlers, `gaps []`, oracle members published at their '
                'exact relative paths; not the after-side data run')
    for key in ('row', 'readme_row'):
        got[key] = re.sub(r'<AFTER-DATA:[^>]*>', headline, got[key])

    province = show(ctx['root'], ctx['freeze'], 'PROVINCE.md')
    readme = show(ctx['root'], ctx['freeze'], 'corpus/README.md')
    if province is None or readme is None:
        raise Uneval('PROVINCE.md or corpus/README.md absent at the freeze')
    # PROVINCE: append only, so the prefix the claim pins is byte-preserved
    prov_new = province.decode() .rstrip('\n') + '\n\n' + got['row'].rstrip('\n') + '\n\n' \
        + got['frontier'].rstrip('\n') + '\n'
    # README: the row goes inside `## Coverage map`, which is all the counter reads
    lines = readme.decode().splitlines()
    try:
        i = lines.index('## Coverage map')
    except ValueError:
        raise Uneval('corpus/README.md has no `## Coverage map` section')
    j = len(lines)
    for n in range(i + 1, len(lines)):
        if lines[n].startswith('## '):
            j = n
            break
    while j > i + 1 and lines[j - 1].strip() == '':
        j -= 1
    new_lines = lines[:j] + [got['readme_row'].rstrip('\n')] + lines[j:]
    readme_new = '\n'.join(new_lines) + '\n'
    entry_rel = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
    # S138/S139 must list the new entry in used-by at the measured revision (the
    # counter's `sourced` binding); the landing appends it, so the POS plants the
    # same append on the registry bytes at the freeze.
    reg = show(ctx['root'], ctx['freeze'], 'corpus/SOURCES.md')
    if reg is None:
        raise Uneval('corpus/SOURCES.md absent at the freeze')
    out_lines = []
    for line in reg.decode().split('\n'):
        m = re.match(r'^ {0,3}\|\s*(S138|S139)\s*\|', line)
        if m and entry_rel not in line:
            cells_ = line.rstrip().rstrip('|').rstrip()
            line = cells_ + ', ' + entry_rel + ' |'
        out_lines.append(line)
    return {'PROVINCE.md': prov_new.encode(),
            'corpus/README.md': readme_new.encode(),
            'corpus/SOURCES.md': '\n'.join(out_lines).encode(),
            entry_rel: got['entry'].encode()}, {k: len(v) for k, v in want.items()}


def control_pos(ctx):
    """Positive control: real REA receipts for every scored carrier (K3).

    Red-only controls cannot tell a counter that works from one that always
    fails. This arm captures a real REA 6.5.0 receipt for each scored carrier in
    scratch (never through c1-run.sh, never committed into the lane) and plants
    them under corpus/evidence/round-49/c1 in the sandbox, so the frozen counter
    must reach its target. `parameters.output_directory` names a path under
    /fast/scratch/hyaku/kaidoku-r49/, which is what the provenance binding reads."""
    files, captured = {}, []
    for carrier in ctx['carriers']['scored']:
        data = capture_real(ctx['work'], carrier, ctx['root'])
        nr = data.get('normalized_result') or {}
        gaps = [g.get('kind') for g in nr.get('extraction_gaps') or []]
        handlers = [c.get('handler') for c in nr.get('chunks') or []]
        # absolute, inside /kaidoku-r49/: what the frozen provenance clause reads
        outdir = ('/fast/scratch/hyaku/kaidoku-r49/c1-controls-pos/%s/extract'
                  % carrier['id'])
        data.setdefault('parameters', {})['output_directory'] = outdir
        data.setdefault('normalized_result', {})['output_directory'] = outdir
        files[receipt_path(carrier['id'])] = (
            json.dumps(data, indent=1, sort_keys=True) + '\n').encode()
        captured.append({'carrier': carrier['id'], 'handler': handlers,
                         'frozen_handler': carrier['handler'],
                         'handler_ok': handlers == [carrier['handler']],
                         'gap_kinds': gaps,
                         'published_files': [f.get('relative_path')
                                             for f in nr.get('files') or []],
                         'published_bytes': nr.get('published_bytes'),
                         'coverage': nr.get('coverage'),
                         'evidence_id': data.get('evidence_id')})
    # the id is minted over the projection, and the projection includes
    # parameters, so rewriting output_directory invalidates the captured id.
    # Re-mint each receipt through the frozen rule before planting it.
    envs = {}
    for carrier in ctx['carriers']['scored']:
        rel = receipt_path(carrier['id'])
        envs[carrier['id']] = json.loads(files[rel])
    minted = mint_evidence_ids(ctx['work'], ctx['pkg65'], envs)
    for cid, env in envs.items():
        env['evidence_id'] = minted[cid]
        for entry in captured:
            if entry['carrier'] == cid:
                entry['evidence_id'] = minted[cid]
        files[receipt_path(cid)] = (json.dumps(env, indent=1, sort_keys=True)
                                    + '\n').encode()
    # the C1 landing bytes, so the five documentation bindings can be true and the
    # positive control can reach exit 0 rather than stalling on a pre-landing axis
    doc_tree, doc_sizes = _doc_landing(ctx)
    planted_doc = {}
    for rel, raw in doc_tree.items():
        base = show(ctx['root'], ctx['freeze'], rel)
        planted_doc[rel] = {'bytes': len(raw),
                            'sha256': sha256_bytes(raw),
                            'base_present': base is not None,
                            'append_only': (base is not None
                                            and raw.startswith(base)),
                            'base_sha256': sha256_bytes(base) if base else None}
        files[rel] = raw
    sandbox = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], 'pos')
    rev = plant_and_commit(sandbox, files,
                           'CTL-C1-POS: real REA receipts + the C1 landing blocks')
    return {'tree': files, 'root': sandbox, 'rev': rev, 'captured': captured,
            'doc_landing': planted_doc,
            'expect': {'exit': 'exit0',
                       'carriers_matched': ctx['carriers']['target'],
                       'no_carrier_clause_fails': True,
                       'all_bindings_true': True},
            'title': 'positive control: real REA receipts + the C1 landing reach exit 0',
            'note': 'K3: with four real scratch REA receipts and the C1 landing blocks '
                    'planted in the sandbox, every binding must be true and the '
                    'counter must exit 0 — otherwise the red controls could be '
                    'satisfied by an always-fail counter. The plant is a control '
                    'fixture, not the landing, and this arm is excluded from the kill '
                    'rule'}


CONTROLS = {
    'c0': ('CTL-C1-0', control_c0),
    'c1': ('CTL-C1-1', control_c1),
    'c2': ('CTL-C1-2', control_c2),
    'c3': ('CTL-C1-3', control_c3),
    'c4': ('CTL-C1-4', control_c4),
    'c5': ('CTL-C1-5', control_c5),
    'pos': ('CTL-C1-POS', control_pos),
}


# ------------------------------------------------------------------ verdict

def judge(control, expect, measured):
    """Compare a control's expectation with what the counter did.

    Returns (ok, why). Exit-code classes are compared as classes ('exit1',
    'exit0', 'non-zero') so a counter that renumbers its codes is still judged on
    the claim's statement; a clause the counter does not emit is recorded as
    absent and fails closed, never open."""
    if measured['exit_code'] == 2:
        return False, 'counter reported could-not-evaluate (exit 2)'
    doc = measured['receipt']
    want_exit = expect.get('exit')
    got = measured['exit_code']
    if want_exit == 'exit1' and got != 1:
        return False, 'expected exit 1, got %r' % (got,)
    if want_exit == 'exit0' and got != 0:
        return False, 'expected exit 0, got %r' % (got,)
    if want_exit == 'non-zero' and got == 0:
        return False, 'expected non-zero, got 0 (the control reached the target)'
    if want_exit == 'carriers_green':
        # not an exit-code class: the assertion is that every per-carrier clause
        # holds, which is what a positive control can prove before the docs land
        summary0 = receipt_summary(doc)
        if not summary0.get('present'):
            return False, 'the counter wrote no readable receipt'
        per = summary0.get('per_carrier_failing') or {}
        bad = {k: [c for c in v if c != 'matched'] for k, v in per.items()}
        bad = {k: v for k, v in bad.items() if v}
        if bad:
            return False, 'carrier clauses still failing: %r' % bad
        if summary0.get('carriers_matched') != expect.get('carriers_matched'):
            return False, 'carriers_matched %r != %r' % (
                summary0.get('carriers_matched'), expect.get('carriers_matched'))
        return True, ('every per-carrier clause true on %r carriers; exit %r is '
                      'driven by the landing bindings %r'
                      % (summary0.get('carriers_matched'), got,
                         summary0.get('bindings_false')))
    summary = receipt_summary(doc)
    if not summary.get('present'):
        # A red exit with no receipt is still a red, but the clause attribution
        # is unproven; say so rather than claim the clause fired.
        return (want_exit != 'exit0',
                'red as expected, but the counter wrote no readable receipt')
    if 'carriers_matched' in expect and expect['carriers_matched'] is not None:
        if summary['carriers_matched'] != expect['carriers_matched']:
            return False, 'carriers_matched %r != %r' % (
                summary['carriers_matched'], expect['carriers_matched'])
    if expect.get('doc_bindings_all_false'):
        known = {k: summary['bindings'].get(k) for k in DOC_BINDINGS}
        true_ones = sorted(k for k, v in known.items() if v is True)
        if true_ones:
            return False, 'documentation bindings true at the do-nothing freeze: %r' % true_ones
        absent = sorted(k for k, v in known.items() if v is None)
        if absent:
            return False, ('documentation bindings absent from the receipt, so '
                           '"false" is unproven: %r' % absent)
    if expect.get('failing_includes'):
        missing = [c for c in expect['failing_includes']
                   if c not in summary['failing_clauses']]
        if missing:
            return False, 'failing clauses %r do not include %r' % (
                summary['failing_clauses'], missing)
    if expect.get('failing_any'):
        if not (set(expect['failing_any']) & set(summary['failing_clauses'])):
            return False, ('none of %r fired (failing=%r)'
                           % (expect['failing_any'], summary['failing_clauses']))
    if expect.get('all_bindings_true'):
        # the bindings map also carries *_detail rows (lists/dicts); only booleans
        # are claims, and only a boolean that is not True is a failure
        # only booleans are claims; the map also carries *_detail rows and the
        # counter's own bindings_false list is not boolean-filtered. A key that is
        # absent from the map entirely is still a failure.
        bmap = summary['bindings']
        false_ones = sorted(
            {k for k, v in bmap.items() if isinstance(v, bool) and v is not True}
            | {k for k in (summary.get('bindings_false') or []) if k not in bmap})
        if false_ones:
            return False, 'bindings not true under the positive control: %r' % false_ones
    return True, 'behaved as the claim states'


# ------------------------------------------------------------------ selftest

STUB = '''#!/usr/bin/env python3
"""A stub counter: proves the control driver's machinery, never a real verdict.

It honours the frozen argv, refuses to be mistaken for the real counter, and
returns the exit code the control expects so the driver's judging path is
exercised end to end."""
import argparse, json, os, sys
ap = argparse.ArgumentParser()
ap.add_argument('--root'); ap.add_argument('--rev'); ap.add_argument('--freeze')
ap.add_argument('--pkg65'); ap.add_argument('--work'); ap.add_argument('--json-out')
a = ap.parse_args()
mode = os.environ.get('STUB_MODE', 'red')
bindings = {k: False for k in ('province_core_section', 'province_core_row',
                               'frontier_note', 'entry_present', 'sourced',
                               'coverage_map_row')}
if mode == 'green':
    bindings = {k: True for k in bindings}
    doc = {'met_target': True, 'carriers_matched': int(os.environ.get('STUB_N', '4')),
           'target': int(os.environ.get('STUB_N', '4')), 'bindings': bindings,
           'failing': [], 'frozen_path_changed': [], 'exit_code': 0,
           'counter_sha256': 'stub', 'counter_sha256_at_freeze': 'stub'}
    code = 0
elif mode == 'red':
    doc = {'met_target': False, 'carriers_matched': 0, 'target': 4,
           'bindings': bindings,
           'failing': ['subject_pin_ok', 'handler_ok', 'projection_ok'],
           'frozen_path_changed': [], 'exit_code': 1,
           'counter_sha256': 'stub', 'counter_sha256_at_freeze': 'stub'}
    code = 1
else:
    doc = {'reason': 'stub_unevaluable'}
    code = 2
if a.json_out:
    with open(a.json_out, 'w') as fh:
        json.dump(doc, fh)
print(json.dumps({'stub': True, 'mode': mode}))
sys.exit(code)
'''


def selftest(work):
    """Exercise the driver's own machinery against a stub counter.

    Nothing here says anything about the real counter; it proves that a control
    tree is built byte-exactly, that a sandbox commit is a strict descendant of
    the freeze, that the counter is invoked with the frozen argv, that the
    receipt carries seat/command/exit/stdout-sha256/wall, and that the judging
    path passes a correct control and rejects a wrong one."""
    checks = []

    def add(name, ok, detail):
        checks.append({'check': name, 'ok': bool(ok), 'detail': detail})

    bindir = os.path.join(work, 'stubbin')
    os.makedirs(bindir, exist_ok=True)
    stub = os.path.join(bindir, 'stub-counter.py')
    with open(stub, 'w') as fh:
        fh.write(STUB)
    os.chmod(stub, 0o755)

    # a two-commit fixture repo so the sandbox/commit machinery is real
    repo = os.path.join(work, 'fixture-lane')
    os.makedirs(repo, exist_ok=True)
    git(repo, 'init', '--quiet')
    for key, val in (('user.name', 'fx'), ('user.email', 'fx@fx')):
        git(repo, 'config', key, val)
    base = os.path.join(repo, 'base.txt')
    with open(base, 'w') as fh:
        fh.write('base\n')
    git(repo, 'add', 'base.txt')
    git(repo, 'commit', '--quiet', '-m', 'base')
    freeze = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()

    sb = make_sandbox(repo, freeze, work, 'selftest')
    add('sandbox is its own git repo', True, sb)
    planted = {'corpus/evidence/round-49/c1/X/after.json': b'{"planted": true}\n'}
    rev = plant_and_commit(sb, planted, 'selftest plant')
    add('plant byte-exact', open(os.path.join(
        sb, 'corpus/evidence/round-49/c1/X/after.json'), 'rb').read()
        == planted['corpus/evidence/round-49/c1/X/after.json'],
        'sha256=%s' % sha256_bytes(planted['corpus/evidence/round-49/c1/X/after.json']))
    # ancestry is asked of the sandbox: the planted commit exists only there
    anc = git(sb, 'merge-base', '--is-ancestor', freeze, rev, check=False).returncode
    add('planted commit descends from the freeze', anc == 0,
        'freeze=%s rev=%s (asked in the sandbox)' % (freeze[:8], rev[:8]))

    # red mode: expect a red control to pass and a green expectation to fail
    jout = os.path.join(work, 'stub-red.json')
    m = run_counter(stub, sb, rev, freeze, work, work, jout)
    add('counter argv carries the frozen flags',
        all(f in m['argv'] for f in ('--root', '--rev', '--freeze', '--pkg65',
                                     '--work', '--json-out')),
        ' '.join(m['argv'][2:]))
    add('receipt records exit/stdout-sha/wall',
        isinstance(m['exit_code'], int) and isinstance(m['stdout_sha256'], str)
        and len(m['stdout_sha256']) == 64 and isinstance(m['wall_s'], float),
        'exit=%r sha=%s wall=%r' % (m['exit_code'], m['stdout_sha256'][:12], m['wall_s']))
    ok, why = judge('CTL-C1-X', {'exit': 'exit1', 'carriers_matched': 0}, m)
    add('a red stub satisfies a red expectation', ok, why)
    ok, why = judge('CTL-C1-X', {'exit': 'exit0'}, m)
    add('a red stub fails a green expectation', not ok, why)

    # green mode: the positive path
    os.environ['STUB_MODE'] = 'green'
    os.environ['STUB_N'] = '4'
    jout2 = os.path.join(work, 'stub-green.json')
    m2 = run_counter(stub, sb, rev, freeze, work, work, jout2)
    ok, why = judge('CTL-C1-POS', {'exit': 'exit0', 'carriers_matched': 4,
                                   'all_bindings_true': True}, m2)
    add('a green stub satisfies the positive control', ok, why)
    ok, why = judge('CTL-C1-POS', {'exit': 'exit0', 'carriers_matched': 5}, m2)
    add('a wrong carrier count fails closed', not ok, why)
    del os.environ['STUB_MODE']
    del os.environ['STUB_N']

    # unevaluable mode never counts as a pass
    os.environ['STUB_MODE'] = 'unevaluable'
    m3 = run_counter(stub, sb, rev, freeze, work, work,
                     os.path.join(work, 'stub-u.json'))
    ok, why = judge('CTL-C1-X', {'exit': 'non-zero'}, m3)
    add('exit 2 from the counter never passes a red control', not ok, why)
    del os.environ['STUB_MODE']

    # the judge must not read an absent binding as true
    ok, why = judge('CTL-C1-X',
                    {'exit': 'non-zero', 'failing_includes': ['projection_ok']},
                    {'exit_code': 1, 'receipt': None, 'stdout_sha256': 'x',
                     'wall_s': 0.0, 'argv': [], 'stdout_tail': [], 'stderr_tail': []})
    add('a missing receipt is reported, not assumed', ok is True and 'no readable' in why, why)

    doc = {'schema': 'kaidoku-r49-c1-controls-selftest-v1', 'seat': SEAT,
           'cases': len(checks), 'passed': sum(1 for c in checks if c['ok']),
           'checks': checks}
    print(json.dumps({'selftest': 'c1-controls', 'cases': doc['cases'],
                      'passed': doc['passed'],
                      'failed': [c['check'] for c in checks if not c['ok']]},
                     sort_keys=True))
    return 0 if doc['passed'] == doc['cases'] else 1, doc


# ------------------------------------------------------------------ main

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--freeze')
    ap.add_argument('--counter', default='tools/round-49/c1-counter.py')
    ap.add_argument('--pkg65')
    ap.add_argument('--work')
    ap.add_argument('--out')
    ap.add_argument('--controls', default='c0,c1,c2,c3,c4,pos')
    ap.add_argument('--carriers', default=None,
                    help='read this worktree carriers.json instead of the frozen '
                         'blob (build/capture only)')
    ap.add_argument('--dev-arm-carriers', default=None,
                    help='read this worktree carriers.json when BUILDING control '
                         'trees (the counter still reads the frozen blob itself)')
    ap.add_argument('--doc-dir', default='.ufo/waves/round-49/w1/artifacts',
                    help='where the R49C1Doc blocks and the R49EntryDraft entry live '
                         '(CTL-C1-POS plants them as control fixtures)')
    ap.add_argument('--fixtures-root', default=FIXTURES,
                    help='committable root for content-addressed control inputs '
                         '(default %s)' % FIXTURES)
    ap.add_argument('--from-fixtures', action='store_true',
                    help='plant the trees read from --fixtures-root instead of '
                         'rebuilding them (what the freeze score does)')
    ap.add_argument('--rehearsal-table-freeze', default=None, metavar='PATH',
                    help='pre-freeze dev arm only: build a rehearsal freeze commit in a '
                         'scratch clone that carries this carriers.json, and score '
                         'against it. Every receipt is stamped `rehearsal: true`. The '
                         'counter reads the table from the freeze tree, so this is the '
                         'only way to show what a corrected frozen table would score')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--build-only', action='store_true',
                    help='build the control input trees, do not score')
    ap.add_argument('--capture-only', action='store_true',
                    help='capture the REA dev arm only (no counter)')
    a = ap.parse_args(argv)

    base = a.work or os.path.join(os.environ.get('HYAKU_SCRATCH',
                                                 '/fast/scratch/hyaku'),
                                  'kaidoku-r49', 'c1-controls')
    os.makedirs(base, exist_ok=True)
    work = tempfile.mkdtemp(prefix='run.', dir=base)
    out = a.out or os.path.join(base, 'out')
    os.makedirs(out, exist_ok=True)

    if a.selftest:
        code, doc = selftest(work)
        write_json(os.path.join(out, 'selftest.json'), doc)
        return code

    if not a.root:
        print('--root is required', file=sys.stderr)
        return 2
    lane_root = os.path.abspath(a.root)
    if not os.path.isdir(os.path.join(lane_root, '.git')):
        print('--root is not a git checkout', file=sys.stderr)
        return 2
    root = lane_root
    freeze = a.freeze or git(root, 'rev-parse', 'HEAD').stdout.decode().strip()

    if a.carriers and not (a.build_only or a.capture_only):
        print('--carriers is a dev-arm input and cannot be used when scoring '
              '(use --dev-arm-carriers to stamp a rehearsal)', file=sys.stderr)
        return 2
    rehearsal_table = a.rehearsal_table_freeze
    if rehearsal_table:
        # A rehearsal freeze: a scratch clone whose freeze commit carries the
        # candidate table, so the counter reads a corrected carriers.json out of
        # the tree it scores. Nothing here touches the lane.
        if a.build_only or a.capture_only:
            print('--rehearsal-table-freeze needs a scored run', file=sys.stderr)
            return 2
        rl = os.path.join(work, 'rehearsal-lane')
        if os.path.isdir(rl):
            shutil.rmtree(rl)
        pr = subprocess.run(['git', 'clone', '--shared', '--quiet',
                             os.path.abspath(root), rl], capture_output=True)
        if pr.returncode != 0:
            raise Uneval('rehearsal clone failed: ' + pr.stderr.decode()[:300])
        assert_toplevel(rl)
        for key, val in (('user.name', 'r49-c1-controls'),
                         ('user.email', 'controls@r49.invalid'),
                         ('commit.gpgsign', 'false')):
            git(rl, 'config', key, val)
        git(rl, 'checkout', '--quiet', '--detach', freeze)
        with open(rehearsal_table, 'rb') as fh:
            table = fh.read()
        try:
            json.loads(table)
        except json.JSONDecodeError as e:
            raise Uneval('--rehearsal-table-freeze is not JSON: %s' % e)
        rehearsal_freeze = plant_and_commit(
            rl, {CARRIERS: table},
            'rehearsal freeze: corrected carriers.json (dev arm, not the lane)')
        root = rl
        freeze = rehearsal_freeze
    try:
        carriers = carriers_at(root, freeze, a.carriers)
    except Uneval as e:
        print('could not evaluate: %s' % e, file=sys.stderr)
        return 2

    try:
        if a.capture_only:
            caps = []
            for c in carriers['scored']:
                data = capture_real(work, c, root)
                nr = data.get('normalized_result') or {}
                caps.append({'carrier': c['id'],
                             'handler': [x.get('handler') for x in nr.get('chunks') or []],
                             'gap_kinds': [g.get('kind')
                                           for g in nr.get('extraction_gaps') or []],
                             'files': [f.get('relative_path')
                                       for f in nr.get('files') or []],
                             'published_bytes': nr.get('published_bytes'),
                             'coverage': nr.get('coverage'),
                             'evidence_id': data.get('evidence_id')})
            doc = {'seat': SEAT, 'phase': 'capture', 'carriers': caps,
                   'target': carriers['target']}
            write_json(os.path.join(out, 'capture.json'), doc)
            print(json.dumps({'captures': len(caps),
                              'target': carriers['target']}, sort_keys=True))
            return 0

        counter = a.counter
        if not os.path.isabs(counter):
            # the counter is a tool, not part of the scored tree: resolve it
            # against the lane even when a rehearsal clone is being scored
            counter = os.path.join(lane_root, counter)
        counter_present = os.path.isfile(counter)
        selected = [s.strip() for s in a.controls.split(',') if s.strip()]
        unknown = [s for s in selected if s not in CONTROLS]
        if unknown:
            print('unknown controls: %r' % unknown, file=sys.stderr)
            return 2

        receipts = {}
        failures, unevaluated = [], []
        for key in selected:
            name, fn = CONTROLS[key]
            ctx = {'root': root, 'freeze': freeze, 'work': work,
                   'pkg65': a.pkg65, 'carriers': carriers,
                   'doc_dir': a.doc_dir if os.path.isdir(a.doc_dir)
                              else os.path.join(lane_root, a.doc_dir)}
            try:
                pre_tree, pre_manifest = (load_fixtures(a.fixtures_root, key)
                                          if a.from_fixtures else (None, None))
                if pre_tree is not None:
                    built = {'tree': pre_tree,
                             'root': make_sandbox(root, freeze, work, key),
                             'expect': pre_manifest.get('expect') or {},
                             'title': pre_manifest.get('title'),
                             'note': 'planted from %s (committed fixtures)'
                                     % a.fixtures_root}
                    for extra in ('mapping', 'fabrication', 'capture',
                                  'relabelled', 'mutations', 'captured',
                                  'doc_landing'):
                        if extra in pre_manifest:
                            built[extra] = pre_manifest[extra]
                    built['rev'] = plant_and_commit(
                        built['root'], pre_tree,
                        'control %s: planted committed fixtures' % name)
                else:
                    built = fn(ctx)
                    if built.get('tree'):
                        write_fixtures(
                            a.fixtures_root, key, built['tree'],
                            built.get('expect') or {},
                            extras={k: built[k] for k in
                                    ('mapping', 'fabrication', 'capture',
                                     'relabelled', 'mutations', 'captured',
                                     'doc_landing', 'title', 'note')
                                    if k in built})
            except Uneval as e:
                receipts[name] = {'control': name, 'seat': SEAT, 'claim': CLAIM,
                                  'status': 'could_not_evaluate', 'reason': str(e),
                                  'expected': 'non-zero'}
                os.makedirs(os.path.join(out, key), exist_ok=True)
                write_json(os.path.join(out, key, 'receipt.json'), receipts[name])
                unevaluated.append(name)
                continue
            control_dir = os.path.join(out, key)
            os.makedirs(control_dir, exist_ok=True)
            tree_manifest = {}
            for rel, raw in (built.get('tree') or {}).items():
                tree_manifest[rel] = {'sha256': sha256_bytes(raw), 'size': len(raw)}
                full = os.path.join(control_dir, 'tree', rel)
                os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
                with open(full, 'wb') as fh:
                    fh.write(raw)
            (built.get('tree') or {})
            receipt = {
                'control': name, 'seat': SEAT, 'claim': CLAIM,
                'title': built.get('title'), 'note': built.get('note'),
                'expect': built.get('expect'),
                'expected': ('exit1' if built.get('expect', {}).get('exit') == 'exit1'
                             else 'exit0' if built.get('expect', {}).get('exit') == 'exit0'
                             else 'non-zero'),
                'tree': tree_manifest,
                'tree_root': control_dir,
                'fixtures_root': a.fixtures_root,
                'fixtures_manifest': os.path.join(a.fixtures_root, key,
                                                  'manifest.json'),
                'planted_from_committed_fixtures': bool(a.from_fixtures),
                'sandbox': built.get('root'),
                'rev': built.get('rev'),
                'freeze': freeze,
                'rehearsal': bool(rehearsal_table),
                'carriers_source': (
                    '%s committed into the REHEARSAL freeze %s (dev arm; the lane '
                    'freeze is untouched)' % (rehearsal_table, freeze[:10])
                    if rehearsal_table else CARRIERS + ' at freeze'),
                'carriers_target': carriers['target'],
                'carriers_scored': [c['id'] for c in carriers['scored']],
                'carriers_exploratory': [c['id'] for c in carriers.get('exploratory') or []],
            }
            for extra in ('mapping', 'fabrication', 'capture', 'relabelled',
                          'mutations', 'captured', 'doc_landing'):
                if extra in built:
                    receipt[extra] = built[extra]
            if a.build_only:
                receipt['status'] = 'built_only'
                write_json(os.path.join(control_dir, 'receipt.json'), receipt)
                receipts[name] = receipt
                continue
            if not counter_present:
                receipt['status'] = 'could_not_evaluate'
                receipt['reason'] = 'counter absent at %s' % os.path.relpath(counter, root)
                write_json(os.path.join(control_dir, 'receipt.json'), receipt)
                receipts[name] = receipt
                unevaluated.append(name)
                continue
            jout = os.path.join(control_dir, 'counter.json')
            measured = run_counter(counter, built['root'], built['rev'], freeze,
                                   a.pkg65, work, jout)
            ok, why = judge(name, built.get('expect') or {}, measured)
            # the claim names `command`; the receipt carries the whole argv plus
            # the seat, exit code, stdout sha256 and wall time the contract wants
            receipt.update({
                'command': ' '.join(measured['argv']),
                'argv': measured['argv'],
                'exit_code': measured['exit_code'],
                'stdout_sha256': measured['stdout_sha256'],
                'wall_s': measured['wall_s'],
                'stdout_tail': measured['stdout_tail'],
                'stderr_tail': measured['stderr_tail'],
                'counter': os.path.relpath(counter, lane_root),
                'counter_sha256': sha256_file(counter),
                'verdict': 'as_expected' if ok else 'misbehaved',
                'why': why,
                'receipt_source': measured.get('receipt_source'),
                'measured': receipt_summary(measured.get('receipt')),
                'measured_bindings_boolean': {
                    k: v for k, v in
                    ((receipt_summary(measured.get('receipt')) or {})
                     .get('bindings') or {}).items() if isinstance(v, bool)},
            })
            write_json(os.path.join(control_dir, 'receipt.json'), receipt)
            receipts[name] = receipt
            if not ok:
                failures.append(name)

        summary = {'seat': SEAT, 'claim': CLAIM, 'freeze': freeze,
                   'rehearsal': bool(rehearsal_table),
                   'carriers_source': (
                       '%s committed into the REHEARSAL freeze %s (dev arm; the lane '
                       'freeze is untouched)' % (rehearsal_table, freeze[:10])
                       if rehearsal_table else CARRIERS + ' at freeze'),
                   'root': root, 'lane_root': lane_root,
                   'counter': os.path.relpath(counter, lane_root),
                   'counter_present': counter_present,
                   'counter_sha256': sha256_file(counter) if counter_present else None,
                   'carriers': {'target': carriers['target'],
                                'scored': [c['id'] for c in carriers['scored']],
                                'exploratory': [c['id'] for c in carriers['exploratory']]},
                   'controls': {k: {'verdict': v.get('verdict', v.get('status')),
                                    'exit_code': v.get('exit_code'),
                                    'expected': v.get('expected'),
                                    'why': v.get('why', v.get('reason')),
                                    'stdout_sha256': v.get('stdout_sha256'),
                                    'wall_s': v.get('wall_s')}
                                for k, v in receipts.items()},
                   'failures': failures, 'unevaluated': unevaluated,
                   'kill_rule_fires': False}
        # the kill rule: a counterfactual control reaching the target stops the claim
        for name, rec in receipts.items():
            if name == 'CTL-C1-POS':
                # the positive arm is not a counterfactual: reaching the target is
                # what it is for, so it can never fire the kill rule
                continue
            m = rec.get('measured') or {}
            if rec.get('verdict') == 'misbehaved':
                want = (rec.get('expect') or {}).get('exit')
                if want in ('non-zero', 'exit1') and m.get('met_target') is True:
                    summary['kill_rule_fires'] = True
        write_json(os.path.join(out, 'summary.json'), summary)
        if a.json_out:
            write_json(a.json_out, summary)
        print(json.dumps({'controls': len(receipts), 'failures': failures,
                          'unevaluated': unevaluated,
                          'kill_rule_fires': summary['kill_rule_fires']},
                         sort_keys=True))
        if unevaluated:
            return 2
        return 1 if failures else 0
    except Uneval as e:
        print('could not evaluate: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
