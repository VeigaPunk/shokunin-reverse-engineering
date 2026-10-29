#!/usr/bin/env python3
"""R50-C1 controls: build the committed control fixtures, then score each with the frozen counter.

Claim: `plans/round-50-claims.md` `## R50-C1` (genuine AVM-marker little-endian SquashFS v4,
`hsqs`, through REA `extract-firmware` -> Core).  Every control is a *counterfactual input
tree*: bytes planted at the C1 evidence path in a scratch `git clone --shared` of the lane,
committed after the freeze, then scored by the frozen counter (a subprocess, the argv the
plan freezes).  The lane is never written.  `git rev-parse --show-toplevel` is asserted
against the sandbox before every commit (run-6 incident).

Two phases, so the scored bytes are the committed bytes:

  gen    build each control's planted tree from its sources and write it under
         `--fixtures-root` (default `tools/round-50/control-fixtures`): one directory per
         control, a `manifest.json` (sha256 + size of every planted file, the expectation,
         the provenance) and gzip-compressed (mtime 0) planted bytes.  Planted bytes that
         already live in the lane (the round-41 BE receipts) are NOT copied: the manifest
         names `{rev, path}` and the sha256, and score re-reads them with `git show`.
  score  plant the committed fixtures and run the counter.  Nothing is rebuilt.

Controls (the plan's list; the clause each is meant to trip is in README.md next to this file)

  c0   CTL-C1-0   do-nothing: the counter at the freeze, no after-receipt.
  c1   CTL-C1-1   the round-41 big-endian AVM receipts (V3, V4), copied verbatim to the
                  round-50 slots.
  c2   CTL-C1-2   envelopes fabricated from the oracle tables, no REA run, evidence id
                  re-minted through the frozen rule: red on the counter-time rerun.
  c3   CTL-C1-3   a receipt captured with `sasquatch` absent from the child PATH.
  c4   CTL-C1-4   a STANDARD little-endian SquashFS (round-36 K1 carved to its bytes_used,
                  `mkfs_time != bytes_used`) with its genuine receipt planted in slot 0 of
                  a sandbox freeze whose carrier table pins that standard carrier there.
  pos  CTL-C1-POS real REA receipts for every slot + the landing blocks: exit 0.

Everything the driver needs to know about the counter (carrier table path, evidence dir,
handler, provenance prefix, entry path, clause names) is read from the counter's own
module-level constants (`--counter` is parsed, never imported), so the same driver scores
the real round-50 counter and a stand-in such as `tools/round-41/c1-counter.py`.

Exit codes (semantic): 0 every control behaved as the plan states; 1 a control misbehaved
(a red control reached the target, or a clause that must fire did not, or POS stayed red);
2 could not evaluate (counter absent, fixtures missing, capture/sandbox failure).

Usage
  c1-controls.py gen    --lane CLONE --freeze REV --counter PATH --pkg65 PKG \
                        --carrier-cache DIR --work DIR [--fixtures-root DIR] [--controls ..]
  c1-controls.py score  --lane CLONE --freeze REV --counter PATH --pkg65 PKG \
                        --carrier-cache DIR --work DIR --out DIR [--json-out FILE]
  c1-controls.py selftest --work DIR

stdlib only; REA 6.5.0 comes through `npx -y rea-agents@6.5.0`.  Honors TMPDIR/HYAKU_SCRATCH.
"""
import argparse
import ast
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time

SEAT = 'C1ControlsBuild'
CLAIM = 'R50-C1'
DEFAULT_BASE_REV = '7c678ae6d97aedb969fd253b52b3d2882ef1e186'
DEFAULT_FIXTURES = 'tools/round-50/control-fixtures'
REA_PIN = 'rea-agents@6.5.0'
# REA 6.5.0 schema maxima for the two budgets; a7530 has 15 150 inodes so the default
# 10 000-entry budget fails ("Staging entry budget exceeded").  Overridden by the carrier
# table's `rea_parameters` when it names them.
REA_ATTEMPTS = 5
LAST_ATTEMPTS = {}
DEFAULT_REA_PARAMS = {'max_depth': 1, 'max_output_files': 100000,
                      'max_output_bytes': 536870912}
ALL_CONTROLS = ('c0', 'c1', 'c2', 'c3', 'c4', 'pos')
NAMES = {'c0': 'CTL-C1-0', 'c1': 'CTL-C1-1', 'c2': 'CTL-C1-2', 'c3': 'CTL-C1-3',
         'c4': 'CTL-C1-4', 'pos': 'CTL-C1-POS', 'c1b': 'CTL-C1-1B',
         'c2x': 'CTL-C1-2X'}
DOC_BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
                'entry_present', 'sourced', 'coverage_map_row')
# receipt-derived per-carrier clauses: green on the do-nothing tree means a clause reads
# nothing (carrier-byte clauses are legitimately green there)
RECEIPT_CLAUSES = ('receipt_present', 'receipt_fresh', 'subject_pin_ok', 'operation_ok',
                   'handler_ok', 'chunks_ok', 'oracle_hits_ok', 'gaps_ok',
                   'nonregular_unpublished_ok', 'run_provenance_ok', 'evidence_id_ok',
                   'projection_ok')
# logical clause -> candidate names in the counter (first one the counter lists wins)
CLAUSE_ALIASES = {
    'marker': ('layout_ok', 'marker_ok', 'superblock_ok'),
    'subject': ('subject_pin_ok',),
    'handler': ('handler_ok',),
    'chunks': ('chunks_ok',),
    'hits': ('oracle_hits_ok',),
    'gaps': ('gaps_ok',),
    'provenance': ('run_provenance_ok',),
    'projection': ('projection_ok',),
    'evidence': ('evidence_id_ok',),
    'receipt': ('receipt_present',),
    'fresh': ('carrier_fresh_ok',),
    'parameters': ('parameters_ok',),
    'carve': ('carve_ok',),
    'nonreg_unpub': ('nonregular_unpublished_ok',),
}
FOREIGN_SOURCES = ('corpus/evidence/round-41/c1/V3/after.json',
                   'corpus/evidence/round-41/c1/V4/after.json')
K1_PATH = 'corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh'
TEMPLATE_RECEIPT = 'corpus/evidence/round-41/c1/V3/after.json'


class Uneval(Exception):
    """Could not evaluate (exit 2): never counts toward a target."""


# ------------------------------------------------------------------ small helpers

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


def jbytes(doc):
    return (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode()


def gz(raw):
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=9, mtime=0) as fh:
        fh.write(raw)
    return buf.getvalue()


def utc_now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


# ------------------------------------------------------------------ git

def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise Uneval('git %s: %s' % (' '.join(args[:3]),
                                     p.stderr.decode(errors='replace').strip()))
    return p


def show(root, rev, path):
    p = git(root, 'show', '%s:%s' % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


def assert_toplevel(d):
    """A fixture commit is only safe when git agrees the fixture is its own repo."""
    top = git(d, 'rev-parse', '--show-toplevel').stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit('sandbox toplevel mismatch: %r != %r' % (top, d))


def make_sandbox(root, freeze, work, name):
    """A `git clone --shared` of the lane at `freeze`, detached, in scratch."""
    dest = os.path.join(work, 'sandbox-' + name)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    p = subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--quiet',
                        os.path.abspath(root), dest], capture_output=True)
    if p.returncode != 0:
        raise Uneval('clone failed: ' + p.stderr.decode(errors='replace'))
    assert_toplevel(dest)
    for key, val in (('user.name', 'r50-c1-controls'),
                     ('user.email', 'controls@r50.invalid'),
                     ('commit.gpgsign', 'false')):
        git(dest, 'config', key, val)
    git(dest, 'checkout', '--quiet', '--detach', freeze)
    return dest


def plant_and_commit(sandbox, files, message):
    """Write `files` ({relpath: bytes}) into the sandbox and commit; return the revision."""
    assert_toplevel(sandbox)
    for rel, raw in files.items():
        full = os.path.join(sandbox, rel)
        os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(raw)
    git(sandbox, 'add', '--', *sorted(files))
    git(sandbox, 'commit', '--quiet', '-m', message)
    return git(sandbox, 'rev-parse', 'HEAD').stdout.decode().strip()


# ------------------------------------------------------------------ the counter's constants

def scrape(counter):
    """Module-level literal constants of the counter, by AST (never imported or executed)."""
    try:
        with open(counter, encoding='utf-8') as fh:
            tree = ast.parse(fh.read())
    except (OSError, SyntaxError) as e:
        raise Uneval('counter unreadable: %s' % e)
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, SyntaxError, TypeError):
                pass
    src = open(counter, encoding='utf-8').read()
    out['__supports_work__'] = "'--work'" in src
    out['__supports_cache__'] = "'--carrier-cache'" in src
    return out


def consts(counter):
    k = scrape(counter)
    carriers = k.get('CARRIERS')
    afterdir = k.get('AFTERDIR') or k.get('EVIDENCE')
    if not carriers or not afterdir:
        raise Uneval('counter names no CARRIERS/AFTERDIR constant')
    prov = k.get('PROV_BASE') or k.get('PROV_PREFIX') or k.get('PROV_SEGMENT') or ''
    prov_base = prov if prov.startswith('/fast/') else '/fast/scratch/hyaku' + prov
    opened = k.get('OPENED') or k.get('OPENED_DATES')
    if isinstance(opened, (tuple, list)):
        opened = opened[0]
    if not isinstance(opened, str):
        m = re.search(r'\d{4}-\d{2}-\d{2}', str(opened or ''))
        opened = m.group(0) if m else '2026-10-28'
    handler = k.get('HANDLER') or 'squashfs_v4_le'
    entry = k.get('ENTRY') or 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
    clauses = tuple(k.get('CLAUSES') or ())
    return {'carriers': carriers, 'afterdir': afterdir,
            'gaprule': k.get('GAPRULE'),
            'xpin': k.get('XPIN') or 'tools/round-27/xpin-attribute.mjs',
            'handler': handler,
            'extractor': 'sasquatch-v4be' if handler.endswith('_be') else 'sasquatch',
            'prov_base': prov_base.rstrip('/'),
            'entry': entry,
            'stem': k.get('STEM') or os.path.basename(entry)[:-3],
            'core_heading': k.get('CORE_HEADING') or '## Round-50 additions to Core',
            'frontier_mark': k.get('FRONTIER_MARK') or 'Round-50 frontier note',
            'opened': opened, 'clauses': clauses,
            'bindings': tuple(k.get('BINDINGS') or ()),
            'target': k.get('TARGET'),
            'supports_work': k['__supports_work__'],
            'supports_cache': k['__supports_cache__']}


def clause(c, logical):
    names = CLAUSE_ALIASES.get(logical, (logical,))
    if c['clauses']:
        for n in names:
            if n in c['clauses']:
                return n
    return names[0]


# ------------------------------------------------------------------ carrier table, bytes

def read_table(root, rev, c):
    raw = show(root, rev, c['carriers'])
    if raw is None:
        raise Uneval('carrier table %s absent at %s' % (c['carriers'], rev))
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        raise Uneval('carrier table unreadable: %s' % e)
    entries = [e for e in doc.get('carriers') or [] if isinstance(e, dict)]
    if not entries:
        raise Uneval('carrier table lists no carriers')
    for e in entries:
        if not (e.get('id') and (e.get('sha256') or '').strip()):
            raise Uneval('carrier entry without id/sha256: %r' % (e.get('id'),))
    return doc, entries


def rea_params(doc):
    p = dict(DEFAULT_REA_PARAMS)
    given = doc.get('rea_parameters')
    if isinstance(given, dict):
        p.update({k: v for k, v in given.items() if isinstance(v, int)})
    return p


def carrier_bytes(root, rev, entry, cache):
    """The carrier's bytes: committed at `path`, else `<cache>/<sha256>.bin`; None if absent."""
    pin = entry['sha256']
    raw = None
    if entry.get('path'):
        raw = show(root, rev, entry['path'])
    if raw is None and cache:
        fp = os.path.join(cache, pin + '.bin')
        if os.path.isfile(fp):
            with open(fp, 'rb') as fh:
                raw = fh.read()
    if raw is not None and sha256_bytes(raw) != pin:
        raise Uneval('carrier %s bytes do not hash to the frozen pin' % entry['id'])
    return raw


def parse_oracle_tsv(raw):
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        f = line.split('\t')
        if len(f) >= 2 and f[0].strip():
            rows.append((f[0].strip(), f[1].strip(), int(f[2]) if len(f) > 2 and f[2].strip().isdigit() else None))
    return rows


def parse_nonreg_tsv(raw):
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        f = line.split('\t')
        if len(f) >= 2 and f[0].strip():
            rows.append((f[0].strip(), f[1].strip(), f[2].strip() if len(f) > 2 else ''))
    return rows


def oracle_rows(root, rev, entry):
    """([(rel, sha, size)], [(rel, kind, detail)]) from the table entry's oracle."""
    orc = entry.get('oracle')
    if isinstance(orc, str):
        raw = show(root, rev, orc)
        if raw is None:
            raise Uneval('oracle %s absent at %s' % (orc, rev))
        reg = parse_oracle_tsv(raw)
        npath = entry.get('nonregular')
        nraw = show(root, rev, npath) if isinstance(npath, str) else None
        non = parse_nonreg_tsv(nraw) if nraw else []
        return reg, non
    if isinstance(orc, dict):
        members = [m for m in orc.get('members') or [] if isinstance(m, dict) and m.get('path')]
        reg = [(m['path'], m['sha256'], int(m['size'])) for m in members
               if m.get('type') in (None, 'regular')]
        non = [(m['path'], m['type'], m.get('detail') or '') for m in members
               if m.get('type') not in (None, 'regular')]
        return reg, non
    raise Uneval('carrier %s has no usable oracle' % entry['id'])


def gap_model(root, rev, c):
    if not c.get('gaprule'):
        return {}
    raw = show(root, rev, c['gaprule'])
    try:
        return json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return {}


# ------------------------------------------------------------------ REA dev arm, evidence ids

def unblob_path():
    return os.environ.get('REA_UNBLOB_COMMAND') or os.path.expanduser('~/.local/bin/unblob')


def path_dirs():
    dirs = [d for d in os.environ.get('PATH', '').split(':') if d]
    for d in ('/usr/local/bin', '/usr/bin', '/bin', os.path.expanduser('~/.local/bin')):
        if d not in dirs:
            dirs.append(d)
    return [d for d in dirs if os.path.isdir(d)]


def stripped_path(work, extractor):
    """A PATH holding every executable of the live PATH except `extractor`.

    The PATH is REPLACED (prepending would leave ~/.local/bin, where sasquatch lives,
    resolvable behind the shim and the capture would silently succeed)."""
    bindir = os.path.join(work, 'pathbin-no-' + extractor)
    if os.path.isdir(bindir):
        shutil.rmtree(bindir)
    os.makedirs(bindir)
    had = False
    for d in path_dirs():
        if os.path.isfile(os.path.join(d, extractor)):
            had = True
        for name in sorted(os.listdir(d)):
            if name == extractor:
                continue
            src, dst = os.path.join(d, name), os.path.join(bindir, name)
            if os.path.lexists(dst) or not os.path.isfile(src) or not os.access(src, os.X_OK):
                continue
            try:
                os.symlink(src, dst)
            except OSError:
                pass
    if not had:
        raise Uneval('%s is not on the live PATH: nothing to strip' % extractor)
    if shutil.which(extractor, path=bindir):
        raise Uneval('%s still resolves under the stripped PATH' % extractor)
    for need in ('npx', 'node'):
        if not shutil.which(need, path=bindir):
            raise Uneval('%s does not resolve under the stripped PATH' % need)
    return bindir


def capture_real(work, tag, raw, params, *, strip=None):
    """Run REA 6.5.0 `extract-firmware` on `raw` in scratch (the dev arm); return `data`.

    Returns (data, staging_dir): every absolute path the receipt records lives under the
    staging dir, which `rehome` rewrites to a stable provenance path."""
    d = os.path.join(work, 'rea-' + tag)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    inp, outdir = os.path.join(d, 'carrier.bin'), os.path.join(d, 'out')
    with open(inp, 'wb') as fh:
        fh.write(raw)
    env = dict(os.environ)
    env['REA_UNBLOB_COMMAND'] = unblob_path()
    env['TMPDIR'] = d
    if strip:
        env['PATH'] = stripped_path(work, strip)
    else:
        env['PATH'] = ':'.join(path_dirs())
    argv = ['npx', '-y', REA_PIN, 'extract-firmware', '--format', 'json', '--full-output']
    for flag, key in (('--max-depth', 'max_depth'), ('--max-output-bytes', 'max_output_bytes'),
                      ('--max-output-files', 'max_output_files')):
        if key in params:
            argv += [flag, str(params[key])]
    argv += [inp, outdir]
    attempts = []
    for attempt in range(1, REA_ATTEMPTS + 1):
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        t0 = time.time()
        r = subprocess.run(argv, cwd=d, capture_output=True, env=env)
        try:
            doc = json.loads(r.stdout)
        except json.JSONDecodeError:
            raise Uneval('REA stdout is not JSON (exit %d): %s'
                         % (r.returncode, r.stderr.decode(errors='replace')[:300]))
        data = doc.get('data') if isinstance(doc, dict) else None
        err = (doc.get('error') or {}) if isinstance(doc, dict) else {}
        attempts.append({'attempt': attempt, 'wall_s': round(time.time() - t0, 1),
                         'ok': isinstance(data, dict), 'error_code': err.get('code')})
        if isinstance(data, dict):
            break
        # REA 6.5.0 has a fixed 120 s deadline; a loaded host trips it. Only that error
        # is retried (a budget or validation error is not a flake); every attempt is kept.
        if err.get('code') != 'provider_timeout' or attempt == REA_ATTEMPTS:
            raise Uneval('REA returned no data object after %d attempt(s) %s: %s'
                         % (attempt, json.dumps(attempts), json.dumps(err)[:300]))
        time.sleep(15)
    LAST_ATTEMPTS[tag] = attempts
    return data, d


def rehome(data, staging, new_root):
    """Rewrite every absolute path under `staging` to `new_root` (consistent, so the
    receipt stays internally coherent and carries no seat-private scratch path)."""
    text = json.dumps(data, sort_keys=True).replace(staging, new_root)
    return json.loads(text)


def mint_ids(work, root, rev, c, pkg65, envs):
    """Re-mint evidence ids through the frozen rule (the package's own projection) so a
    fixture reds on the clause it names, never on a stale id."""
    if not pkg65 or not os.path.isdir(pkg65):
        raise Uneval('--pkg65 must name the rea-agents 6.5.0 package root')
    xpin = os.path.join(work, 'xpin-attribute.mjs')
    tool = show(root, rev, c['xpin'])
    if tool is None:
        tool = show(root, 'HEAD', c['xpin'])
    if tool is None:
        raise Uneval('xpin tool %s absent' % c['xpin'])
    with open(xpin, 'wb') as fh:
        fh.write(tool)
    paths = []
    for key, env in envs.items():
        p = os.path.join(work, 'mint-%s.json' % key)
        with open(p, 'w') as fh:
            json.dump({'data': env}, fh)
        paths.append(p)
    if not paths:
        return {}
    r = subprocess.run(['node', xpin, '--pkg65', pkg65, '--pkg67', pkg65] + paths,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Uneval('xpin mint failed: ' + r.stderr.strip()[:400])
    lines = [ln for ln in r.stdout.splitlines() if ln]
    if len(lines) != len(paths):
        raise Uneval('xpin line count %d != %d' % (len(lines), len(paths)))
    return {key: line.split('\t')[2] for key, line in zip(envs, lines)}


def real_receipt(ctx, key, entry, raw, strip=None):
    """A genuine REA receipt of `raw`, rehomed under the provenance prefix, id re-minted.

    Returns (receipt bytes, facts)."""
    c = ctx['c']
    tag = '%s-%s' % (key, entry['id'])
    data, staging = capture_real(ctx['work'], tag, raw, ctx['params'], strip=strip)
    home = '%s/c1-controls/%s/%s' % (c['prov_base'], key, entry['id'])
    data = rehome(data, staging, home)
    nr = data.get('normalized_result') or {}
    facts = {'carrier': entry['id'], 'pin': entry['sha256'],
             'handlers': [x.get('handler') for x in nr.get('chunks') or []],
             'gap_kinds': sorted({g.get('kind') for g in nr.get('extraction_gaps') or []}),
             'chunk_failed': any(x.get('extraction_failed') for x in nr.get('chunks') or []),
             'coverage': nr.get('coverage'), 'published_files': len(nr.get('files') or []),
             'published_bytes': nr.get('published_bytes'),
             'output_directory': (data.get('parameters') or {}).get('output_directory'),
             'rea_attempts': LAST_ATTEMPTS.get(tag)}
    minted = mint_ids(ctx['work'], ctx['root'], ctx['freeze'], c, ctx['pkg65'], {tag: data})
    data['evidence_id'] = minted[tag]
    facts['evidence_id'] = data['evidence_id']
    return jbytes(data), facts


# ------------------------------------------------------------------ oracle-only forgery

def forge_receipt(ctx, entry, length):
    """An envelope built ONLY from the oracle tables and a real receipt's public shape.

    Published files = the oracle's regular files at `firmware.bin_extract/<rel>`; one
    `unpublished-entry` gap + row per non-regular entry the frozen gap rule allows; one
    depth-limited gap; coverage partial; no diagnostics (the forger cannot know which
    links the real run removed).  No REA run.  The evidence id is re-minted afterwards, so
    the only thing missing is the run itself."""
    c = ctx['c']
    tmpl_raw = show(ctx['root'], ctx['base_rev'], TEMPLATE_RECEIPT)
    if tmpl_raw is None:
        raise Uneval('template receipt %s absent at %s' % (TEMPLATE_RECEIPT, ctx['base_rev']))
    env = json.loads(tmpl_raw)
    reg, non = oracle_rows(ctx['root'], ctx['freeze'], entry)
    if not reg:
        raise Uneval('carrier %s has no oracle files' % entry['id'])
    model = gap_model(ctx['root'], ctx['freeze'], c)
    allowed = model.get('allowed') or {}
    required = model.get('required') or {}
    silent = (model.get('removed') or {}).get('silent') or {}
    outdir = '%s/c1-controls/c2/%s/out' % (c['prov_base'], entry['id'])
    chunk_dir = 'firmware.bin_extract'
    handler = c['handler']
    pin = entry['sha256']
    files, published = [], 0
    for rel, sha, size in reg:
        size = int(size) if size is not None else 0
        published += size
        files.append({'relative_path': '%s/%s' % (chunk_dir, rel),
                      'path': '%s/%s/%s' % (outdir, chunk_dir, rel), 'size': size,
                      'sha256': sha, 'reported_sha256': None, 'mime_type': None,
                      'analysis_depth': None, 'runtime_address': None,
                      'original_file_range': None})
    gaps = [{'kind': 'depth-limited', 'input_path': '$output/' + chunk_dir,
             'relative_path': None, 'handler': None, 'provider_id': None, 'range': None,
             'root_file_range': None, 'dependencies': [],
             'continuation_id': 'forged-continuation'}]
    unpub = []
    for rel, kind, detail in non:
        if not allowed.get(kind):
            continue
        if required.get(kind) and detail in (silent.get(kind) or []):
            continue
        gaps.append({'kind': 'unpublished-entry',
                     'input_path': '$output/%s/%s' % (chunk_dir, rel),
                     'relative_path': '%s/%s' % (chunk_dir, rel), 'handler': handler,
                     'provider_id': '1:1', 'range': None, 'root_file_range': None,
                     'dependencies': [], 'continuation_id': 'forged-continuation'})
        unpub.append({'relative_path': '%s/%s' % (chunk_dir, rel), 'kind': kind,
                      'link_target': detail if kind == 'symlink' else None})
    nr = env['normalized_result']
    nr['selection'] = {'offset': 0, 'length': length, 'sha256': pin}
    nr['output_directory'] = outdir
    nr['coverage'] = 'partial'
    nr['files'] = files
    nr['unpublished_entries'] = unpub
    nr['chunks'] = [{'input_path': '$input', 'provider_id': '1:1',
                     'range': {'offset': 0, 'length': length}, 'handler': handler,
                     'encrypted': False,
                     'root_file_range': {'offset': 0, 'length': length},
                     'extraction_failed': False}]
    nr['derivations'] = [{'parent_path': '$input', 'child_path': '$output/' + chunk_dir,
                          'provider_blob_id': '1:1', 'handler': handler,
                          'parent_file_range': {'offset': 0, 'length': length}}]
    nr['depth_limited_paths'] = ['$output/' + chunk_dir]
    nr['diagnostics'] = []
    nr['extraction_gaps'] = gaps
    nr['extraction_continuations'] = []
    nr['published_bytes'] = published
    base = '%s/c1-controls/c2/%s' % (c['prov_base'], entry['id'])
    env['subject'] = {'name': 'carrier.bin', 'digest': {'sha256': pin},
                      'local_path': base + '/carrier.bin', 'format': 'file',
                      'architecture': None}
    env['parameters'] = {'path': base + '/carrier.bin', 'output_directory': outdir,
                         'max_depth': ctx['params']['max_depth'],
                         'max_output_bytes': ctx['params']['max_output_bytes'],
                         'max_output_files': ctx['params']['max_output_files']}
    return env, {'carrier': entry['id'], 'handler': handler, 'real_rea_run': False,
                 'regular_files': len(reg), 'gap_rows': len(gaps),
                 'unpublished_rows': len(unpub), 'output_directory': outdir}


# ------------------------------------------------------------------ the standard carrier (c4)

def carve_standard(ctx):
    """round-36 K1 (bare LE SquashFS v4, xz, `mkfs_time == 0`) carved to its bytes_used."""
    raw = show(ctx['root'], ctx['base_rev'], K1_PATH)
    if raw is None:
        raise Uneval('%s absent at %s' % (K1_PATH, ctx['base_rev']))
    if raw[:4] != b'hsqs':
        raise Uneval('K1 is not little-endian hsqs')
    used = int.from_bytes(raw[40:48], 'little')
    mkfs = int.from_bytes(raw[8:12], 'little')
    comp = int.from_bytes(raw[20:22], 'little')
    if mkfs == used & 0xFFFFFFFF:
        raise Uneval('K1 carries the AVM marker; it cannot be the standard control')
    if not 0 < used <= len(raw):
        raise Uneval('K1 bytes_used out of range')
    carve = raw[:used]
    return carve, {'source': K1_PATH, 'source_rev': ctx['base_rev'],
                   'source_sha256': sha256_bytes(raw), 'source_size': len(raw),
                   'carved_size': len(carve), 'carved_sha256': sha256_bytes(carve),
                   'bytes_used': used, 'mkfs_time': mkfs, 'compression_id': comp,
                   'avm_marker': False}


def oracle_from_squashfs(work, carve):
    """(oracle rows, non-regular rows) of a bare SquashFS through `unsquashfs` 4.7.x."""
    if not shutil.which('unsquashfs'):
        raise Uneval('unsquashfs is not on PATH')
    d = os.path.join(work, 'k1-oracle')
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    src = os.path.join(d, 'k1.sqsh')
    with open(src, 'wb') as fh:
        fh.write(carve)
    root = os.path.join(d, 'out')
    r = subprocess.run(['unsquashfs', '-no-xattrs', '-d', root, src], capture_output=True)
    if r.returncode != 0:
        raise Uneval('unsquashfs failed: ' + r.stderr.decode(errors='replace')[:200])
    reg, non = [], []
    for dp, dns, fns in os.walk(root):
        for n in sorted(dns + fns):
            full = os.path.join(dp, n)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                non.append((rel, 'symlink', os.readlink(full)))
            elif os.path.isdir(full):
                non.append((rel, 'dir', ''))
            elif os.path.isfile(full):
                with open(full, 'rb') as fh:
                    blob = fh.read()
                reg.append((rel, sha256_bytes(blob), len(blob)))
            else:
                non.append((rel, 'other', ''))
    return sorted(reg), sorted(non)


def tsv_bytes(rows):
    return ''.join('\t'.join(str(x) for x in row) + '\n' for row in rows).encode()


def swap_slot(table_raw, slot_id, pin, carrier_rel, reg, non):
    """The carrier table with `slot_id` pointing at the standard carrier.

    Keeps the entry's own `oracle`/`nonregular` paths (their bytes are replaced in the
    same overlay) and drops the `external` chain; the carrier bytes are committed at
    `carrier_rel` so a counter that reads committed carriers finds them, and the driver
    also drops `<pin>.bin` into the control's carrier cache for one that reads the cache."""
    doc = json.loads(table_raw)
    overlay = {}
    for e in doc['carriers']:
        if e.get('id') != slot_id:
            continue
        for k in ('external', 'nested'):
            e.pop(k, None)
        e['sha256'] = pin
        e['path'] = carrier_rel
        if 'kind' in e:
            e['kind'] = 'lane-built'
        orc = e.get('oracle')
        if isinstance(orc, str):
            overlay[orc] = tsv_bytes(reg)
            if isinstance(e.get('nonregular'), str):
                overlay[e['nonregular']] = tsv_bytes(non)
        elif isinstance(orc, dict):
            e['oracle'] = dict(orc, members=(
                [{'path': r, 'sha256': s, 'size': z, 'type': 'regular'} for r, s, z in reg]
                + [{'path': r, 'type': k, 'detail': d} for r, k, d in non]))
        break
    else:
        raise Uneval('slot %s not in the carrier table' % slot_id)
    return jbytes(doc), overlay


# ------------------------------------------------------------------ landing (POS)

def province_blocks(c):
    h = c['handler']
    le = h.endswith('_le')
    stem = c['stem']
    entry = c['entry']
    if le:
        row = ('| genuine AVM-marker little-endian SquashFS v4 (`%s`, `hsqs`, v4.0, xz, '
               '`mkfs_time == bytes_used`) | no new REA key; unblob 26.6.4 with `sasquatch` '
               '4.5.1 on the child PATH, no `-be` binary; `extract-firmware --max-depth 1` '
               'with the staging budgets raised | CONTROL-FIXTURE TEXT (CTL-C1-POS), not the '
               'landing: AVM marker, AVM layout, entry `%s` | `extract-firmware` on four '
               'frozen carriers |\n' % (h, entry))
        front = ('%s, 2026-10-28 (CONTROL FIXTURE): genuine AVM-marker little-endian members '
                 '(LE AVM, LE-AVM, AVM-LE, `hsqs`) moved Frontier -> Core with `%s`. Still '
                 'Frontier: AVM kernel images.\n' % (c['frontier_mark'], stem))
    else:
        row = ('| genuine AVM-layout big-endian SquashFS v4 (`%s`) | CONTROL-FIXTURE TEXT '
               '(CTL-C1-POS), not the landing: AVM layout, entry `%s` | probe | evidence |\n'
               % (h, entry))
        front = ('%s, 2026-10-28 (CONTROL FIXTURE): AVM layout `%s`.\n'
                 % (c['frontier_mark'], stem))
    core = ('%s\n\n| Surface | Ports / keys | Probe | Verified evidence |\n|---|---|---|---|\n%s'
            % (c['core_heading'], row))
    readme = ('| Genuine AVM %s SquashFS v4 through REA (CONTROL FIXTURE) | `%s` | **Core** '
              '(CTL-C1-POS plant; not the landing) |'
              % ('marker little-endian' if le else 'layout big-endian', stem))
    sid = 'S990'
    src_row = ('| %s | CONTROL FIXTURE source row — https://example.invalid/ctl-c1-pos | docs | A '
               '| plant for CTL-C1-POS only | none | nothing; a fixture row so the `sourced` '
               'binding can be true | mined | %s | on-release | %s |'
               % (sid, c['opened'], entry))
    entry_md = ('# CONTROL FIXTURE entry for %s (CTL-C1-POS plant, not the landing)\n\n'
                'status: control fixture\n\n'
                'source: %s — https://example.invalid/ctl-c1-pos — as read %s\n'
                'verified-at: %s\n' % (stem, sid, c['opened'], c['opened']))
    return {'province_core': core, 'province_frontier': front, 'readme_row': readme,
            'sources_row': src_row, 'entry': entry_md}


def apply_landing(root, rev, c, blocks):
    """{path: bytes} landing planted on the freeze bytes: PROVINCE.md + Core section and
    frontier line appended, README row inside `## Coverage map`, SOURCES row after the last
    registry row, the entry file."""
    out = {}
    prov = show(root, rev, 'PROVINCE.md')
    readme = show(root, rev, 'corpus/README.md')
    reg = show(root, rev, 'corpus/SOURCES.md')
    if prov is None or readme is None or reg is None:
        raise Uneval('PROVINCE.md/corpus/README.md/corpus/SOURCES.md absent at the freeze')
    out['PROVINCE.md'] = (prov.decode().rstrip('\n') + '\n\n'
                          + blocks['province_core'].rstrip('\n') + '\n\n'
                          + blocks['province_frontier'].rstrip('\n') + '\n').encode()
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
    out['corpus/README.md'] = ('\n'.join(lines[:j] + [blocks['readme_row']] + lines[j:])
                               + '\n').encode()
    rl = reg.decode().split('\n')
    last = max((n for n, ln in enumerate(rl) if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', ln)),
               default=None)
    if last is None:
        raise Uneval('corpus/SOURCES.md has no registry rows')
    rl.insert(last + 1, blocks['sources_row'])
    out['corpus/SOURCES.md'] = '\n'.join(rl).encode()
    out[c['entry']] = blocks['entry'].encode()
    return out


# ------------------------------------------------------------------ control builders
# A spec: {'files': {rel: bytes | {'from_lane': {rev, path}}}, 'overlay': {...} (committed
# as the sandbox's own freeze), 'expect': {...}, 'title', 'note', 'extras': {...}}

def spec_c0(ctx):
    c = ctx['c']
    return {'files': {}, 'overlay': {}, 'title': 'do-nothing: the counter at the freeze',
            'note': 'a do-nothing tree cannot reach the target; every documentation binding '
                    'and every receipt-derived carrier clause must be false',
            'expect': {'exit': 'exit1', 'matched': 0, 'doc_bindings_all_false': True,
                       'receipt_clauses_all_false': True},
            'extras': {}}


def spec_c1(ctx):
    c = ctx['c']
    files, mapping = {}, []
    ids = [e['id'] for e in ctx['entries']]
    shift = 1 if {'V3', 'V4'} & set(ids) else 0
    for i, e in enumerate(ctx['entries']):
        src = FOREIGN_SOURCES[(i + shift) % len(FOREIGN_SOURCES)]
        raw = show(ctx['root'], ctx['base_rev'], src)
        if raw is None:
            raise Uneval('round-41 receipt %s absent at %s' % (src, ctx['base_rev']))
        dst = '%s/%s/after.json' % (c['afterdir'], e['id'])
        files[dst] = {'from_lane': {'rev': ctx['base_rev'], 'path': src},
                      'sha256': sha256_bytes(raw), 'size': len(raw)}
        doc = json.loads(raw)
        mapping.append({'slot': e['id'], 'source': src, 'source_sha256': sha256_bytes(raw),
                        'source_subject': ((doc.get('subject') or {}).get('digest') or {})
                        .get('sha256'),
                        'source_handlers': [x.get('handler') for x in
                                            (doc.get('normalized_result') or {}).get('chunks') or []],
                        'source_output_directory': (doc.get('parameters') or {})
                        .get('output_directory')})
    fire = ['subject']
    if c['handler'] != 'squashfs_v4_be':
        fire.append('handler')
    if '/kaidoku-r41/' not in c['prov_base'] + '/':
        fire.append('provenance')
    return {'files': files, 'overlay': {},
            'title': 'round-41 big-endian AVM receipts copied verbatim to the round-50 slots',
            'note': 'a receipt that is genuine for a BE carrier cannot satisfy an LE '
                    'carrier slot: subject digest, handler and provenance prefix disagree. '
                    'The layout/marker clause reads the carrier bytes, not the receipt, so '
                    'it is NOT tripped here (see README)',
            'expect': {'exit': 'non-zero', 'matched': 0, 'every_slot_fails': fire},
            'extras': {'mapping': mapping}}


L3_DIR = 'corpus/evidence/round-41/c1/L3'


def spec_c1b(ctx):
    """EXTRA ARM (not in the default set): the BE carrier too.  The round-41 lane-built BE
    AVM carrier `L3` (committed, `sqsh`, `mkfs_time == bytes_used`) with its genuine round-41
    receipt, verbatim, in slot 0 of a sandbox freeze that pins it there.  Only this arm
    makes the marker/superblock clause read a big-endian body (CTL-C1-1 plants receipts,
    which carry no superblock): handler, marker and provenance must all fire."""
    c = ctx['c']
    if c['handler'] == 'squashfs_v4_be':
        raise Uneval('c1b is only meaningful for a little-endian counter')
    carve = show(ctx['root'], ctx['base_rev'], L3_DIR + '/carrier.sqsh')
    rcpt = show(ctx['root'], ctx['base_rev'], L3_DIR + '/after.json')
    otsv = show(ctx['root'], ctx['base_rev'], L3_DIR + '/oracle.tsv')
    ntsv = show(ctx['root'], ctx['base_rev'], L3_DIR + '/nonregular.tsv')
    if None in (carve, rcpt, otsv, ntsv):
        raise Uneval('round-41 L3 carrier/receipt/oracle absent at %s' % ctx['base_rev'])
    if carve[:4] != b'sqsh':
        raise Uneval('L3 is not a big-endian body')
    used = int.from_bytes(carve[40:48], 'big')
    mkfs = int.from_bytes(carve[8:12], 'big')
    slot = ctx['entries'][0]
    pin = sha256_bytes(carve)
    carrier_rel = '%s/%s/carrier.sqsh' % (c['afterdir'], slot['id'])
    table_raw = show(ctx['root'], ctx['freeze'], c['carriers'])
    new_table, overlay = swap_slot(table_raw, slot['id'], pin, carrier_rel,
                                   parse_oracle_tsv(otsv), parse_nonreg_tsv(ntsv))
    overlay[c['carriers']] = new_table
    overlay[carrier_rel] = {'from_lane': {'rev': ctx['base_rev'], 'path': L3_DIR + '/carrier.sqsh'},
                            'sha256': pin, 'size': len(carve)}
    after = '%s/%s/after.json' % (c['afterdir'], slot['id'])
    files = {after: {'from_lane': {'rev': ctx['base_rev'], 'path': L3_DIR + '/after.json'},
                     'sha256': sha256_bytes(rcpt), 'size': len(rcpt)}}
    fire = ['marker', 'handler']
    if '/kaidoku-r41/' not in c['prov_base'] + '/':
        fire.append('provenance')
    return {'files': files, 'overlay': overlay,
            'title': 'a genuine big-endian AVM carrier with its genuine round-41 receipt in a carrier slot',
            'note': 'receipt, oracle, carve and evidence id are genuine for the BE carrier; the '
                    'marker/superblock clause (reads `sqsh`), the handler and the provenance '
                    'prefix must fire and nothing else',
            # may also fire: the round-41 pin is a prior pin (carrier_fresh_ok); the receipt's
            # budgets are round 41's (parameters_ok); a BE body has no LE extract root, so the
            # three path clauses cannot resolve (hits/gaps/nonreg_unpub) and carve reads LE
            # round-50 draft counter: a BE body makes its independent unsquashfs oracle arm fail,
            # exit 2 `oracle_env_error` (the counter refuses it) - accepted as "not a match"
            'expect': {'exit': 'non-zero', 'slot': slot['id'], 'slot_fails': fire,
                       'slot_fails_exactly': fire + ['fresh', 'parameters', 'carve', 'hits', 'gaps',
                                             'nonreg_unpub'],
                       'matched_lt_target': True,
                       'accept_refusal': ['oracle_env_error']},
            'extras': {'slot': slot['id'], 'standard_carrier_pin': pin,
                       'be_carrier': {'source': L3_DIR + '/carrier.sqsh', 'size': len(carve),
                                      'sha256': pin, 'bytes_used': used, 'mkfs_time': mkfs}}}


def spec_c2(ctx):
    files, fab, envs = {}, [], {}
    c = ctx['c']
    for e in ctx['entries']:
        raw = carrier_bytes(ctx['root'], ctx['freeze'], e, ctx['cache'])
        length = len(raw) if raw is not None else (e.get('external') or {}).get('length')
        if not length:
            raise Uneval('carrier %s: length unknown (no bytes, no external.length)' % e['id'])
        env, facts = forge_receipt(ctx, e, int(length))
        envs[e['id']] = env
        fab.append(facts)
    minted = mint_ids(ctx['work'], ctx['root'], ctx['freeze'], c, ctx['pkg65'], envs)
    for cid, env in envs.items():
        env['evidence_id'] = minted[cid]
        files['%s/%s/after.json' % (c['afterdir'], cid)] = jbytes(env)
    for f in fab:
        f['evidence_id'] = minted[f['carrier']]
    return {'files': files, 'overlay': {},
            'title': 'oracle-only fabrication with a re-minted evidence id',
            'note': 'published-file claims, gap rows and the carrier pin are the oracle and '
                    'the public receipt shape; no REA run exists. Only the counter-time '
                    'rerun can tell it from a run. A fabrication whose rerun projection '
                    'equals a real run would reach the target: that is the kill rule',
            'expect': {'exit': 'non-zero', 'matched': 0, 'some_slot_fails': ['projection']},
            'extras': {'fabrication': fab}}


def spec_c3(ctx):
    c = ctx['c']
    slot = None
    for e in ctx['entries']:
        raw = carrier_bytes(ctx['root'], ctx['freeze'], e, ctx['cache'])
        if raw is not None:
            slot, raw0 = e, raw
            break
    if slot is None:
        raise Uneval('no carrier bytes available for the sasquatch-absent capture')
    body, facts = real_receipt(ctx, 'c3', slot, raw0, strip=c['extractor'])
    if 'missing-extractor-dependency' not in facts['gap_kinds']:
        raise Uneval('stripped-PATH capture produced no missing-extractor-dependency gap '
                     '(gaps=%r)' % (facts['gap_kinds'],))
    facts.update({'extractor': c['extractor'], 'extractor_on_child_path': False})
    return {'files': {'%s/%s/after.json' % (c['afterdir'], slot['id']): body}, 'overlay': {},
            'title': '%s-absent capture: a missing extractor is not a match' % c['extractor'],
            'note': 'the chunk fails for a named missing dependency; the counter must not '
                    'score it a match and the receipt must carry the gap kind',
            'expect': {'exit': 'non-zero', 'matched': 0,
                       'slot': slot['id'], 'slot_fails': ['chunks', 'hits'],
                       'receipt_gap_kind': 'missing-extractor-dependency'},
            'extras': {'capture': facts}}


def spec_c4(ctx):
    c = ctx['c']
    carve, cinfo = carve_standard(ctx)
    reg, non = oracle_from_squashfs(ctx['work'], carve)
    slot = ctx['entries'][0]
    pin = sha256_bytes(carve)
    carrier_rel = '%s/%s/carrier.sqsh' % (c['afterdir'], slot['id'])
    table_raw = show(ctx['root'], ctx['freeze'], c['carriers'])
    new_table, overlay = swap_slot(table_raw, slot['id'], pin, carrier_rel, reg, non)
    overlay[c['carriers']] = new_table
    overlay[carrier_rel] = carve
    # genuine receipt of the standard carrier, made by the real REA with sasquatch on PATH
    fake_entry = dict(slot, sha256=pin)
    body, facts = real_receipt(ctx, 'c4', fake_entry, carve)
    files = {'%s/%s/after.json' % (c['afterdir'], slot['id']): body}
    if facts['chunk_failed'] or c['handler'] not in facts['handlers']:
        if c['handler'] in ('squashfs_v4_le', 'squashfs_v4_be') and facts['handlers'] != [c['handler']]:
            facts['note'] = ('the standard carrier took handlers %r, not %r; the receipt is '
                             'still genuine for the standard carrier' % (facts['handlers'], c['handler']))
    le = c['handler'].endswith('_le')
    expect = {'exit': 'non-zero', 'slot': slot['id'], 'slot_fails': ['marker'],
              'slot_fails_exactly': ['marker'] if le else None,
              'matched_lt_target': True}
    return {'files': files, 'overlay': overlay,
            'title': 'a standard little-endian SquashFS with its genuine receipt in a carrier slot',
            'note': 'slot %s of the sandbox freeze pins a STANDARD LE carrier '
                    '(mkfs_time != bytes_used); everything the receipt, oracle, carve, '
                    'handler, provenance, evidence id and rerun check is genuine, so the '
                    'AVM-marker/superblock clause is the only one allowed to fail. The '
                    'other slots hold no receipt unless the pos fixtures exist at score '
                    'time (then they hold the genuine pos receipts and matched must be '
                    'target-1)' % slot['id'],
            'expect': expect,
            'extras': {'standard_carrier': cinfo, 'slot': slot['id'], 'capture': facts,
                       'oracle_rows': len(reg), 'nonregular_rows': len(non),
                       'standard_carrier_pin': pin}}


def import_receipt(ctx, key, entry, directory):
    """A genuine REA receipt produced elsewhere (a dev-arm seat on a quiet host), taken from
    `<directory>/<id>.envelope.json[.gz]` or `<id>.json[.gz]`; refused unless its subject
    digest is the carrier pin.  Rehomed under the provenance prefix, id re-minted."""
    c = ctx['c']
    path = None
    for stem in ('%s.envelope.json' % entry['id'], '%s.json' % entry['id']):
        for ext in ('', '.gz'):
            cand = os.path.join(directory, stem + ext)
            if os.path.isfile(cand):
                path = cand
                break
        if path:
            break
    if path is None:
        raise Uneval('no receipt for %s under %s' % (entry['id'], directory))
    with open(path, 'rb') as fh:
        raw = fh.read()
    blob = gzip.decompress(raw) if path.endswith('.gz') else raw
    doc = json.loads(blob)
    data = doc.get('data', doc)
    if not isinstance(data, dict) or 'normalized_result' not in data:
        raise Uneval('%s holds no REA data object' % path)
    if ((data.get('subject') or {}).get('digest') or {}).get('sha256') != entry['sha256']:
        raise Uneval('%s subject digest is not the %s carrier pin (an uncarved or other '
                     'member?)' % (path, entry['id']))
    params = data.get('parameters') or {}
    home = '%s/c1-controls/%s/%s' % (c['prov_base'], key, entry['id'])
    out_old = params.get('output_directory') or ''
    text = json.dumps(data, sort_keys=True)
    # the run's trusted root is the output directory's parent: REA's private extraction tree
    # (where `MaliciousSymlinkRemoved.link` points) lives under the run's TMPDIR, which is
    # that parent.  Rehome the parent, then pin the two named paths.
    if out_old:
        text = text.replace(os.path.dirname(out_old), home)
    data = json.loads(text)
    data['parameters']['output_directory'] = home + '/out'
    data['normalized_result']['output_directory'] = home + '/out'
    data['parameters']['path'] = home + '/carrier.bin'
    if isinstance(data.get('subject'), dict):
        data['subject']['local_path'] = home + '/carrier.bin'
    for dg in (data['normalized_result'].get('diagnostics') or []):
        link = (dg.get('report') or {}).get('link') or ''
        if link and not link.startswith(home + '/'):
            raise Uneval('%s: diagnostic link %s lies outside the run root %s; re-run with '
                         'TMPDIR set to the output directory\'s parent' % (path, link, home))
    nr = data.get('normalized_result') or {}
    facts = {'carrier': entry['id'], 'pin': entry['sha256'],
             'handlers': [x.get('handler') for x in nr.get('chunks') or []],
             'gap_kinds': sorted({g.get('kind') for g in nr.get('extraction_gaps') or []}),
             'chunk_failed': any(x.get('extraction_failed') for x in nr.get('chunks') or []),
             'coverage': nr.get('coverage'), 'published_files': len(nr.get('files') or []),
             'published_bytes': nr.get('published_bytes'),
             'output_directory': (data.get('parameters') or {}).get('output_directory'),
             'imported_from': os.path.basename(path), 'imported_sha256': sha256_bytes(raw)}
    tag = '%s-%s' % (key, entry['id'])
    data['evidence_id'] = mint_ids(ctx['work'], ctx['root'], ctx['freeze'], c, ctx['pkg65'],
                                   {tag: data})[tag]
    facts['evidence_id'] = data['evidence_id']
    return jbytes(data), facts


def spec_pos(ctx):
    c = ctx['c']
    files, caps, missing = {}, [], []
    for e in ctx['entries']:
        if ctx.get('pos_envelopes'):
            body, facts = import_receipt(ctx, 'pos', e, ctx['pos_envelopes'])
            files['%s/%s/after.json' % (c['afterdir'], e['id'])] = body
            caps.append(facts)
            continue
        raw = carrier_bytes(ctx['root'], ctx['freeze'], e, ctx['cache'])
        if raw is None:
            missing.append(e['id'])
            continue
        body, facts = real_receipt(ctx, 'pos', e, raw)
        files['%s/%s/after.json' % (c['afterdir'], e['id'])] = body
        caps.append(facts)
    if missing:
        raise Uneval('pos needs every carrier\'s bytes; absent from the cache: %r' % missing)
    blocks = province_blocks(c)
    return {'files': files, 'overlay': {}, 'blocks': blocks,
            'title': 'positive control: real REA receipts for every slot + the landing blocks',
            'note': 'K3: red-only controls cannot tell a counter that works from one that '
                    'always fails. The landing text is a fixture, not the landing',
            'expect': {'exit': 'exit0', 'matched': 'target', 'all_bindings_true': True},
            'extras': {'captured': caps}}


def spec_pos_lane(ctx):
    """Stand-in POS: the lane's own landing at `base_rev` (real receipts + real docs)."""
    c = ctx['c']
    files = {}
    for e in ctx['entries']:
        p = '%s/%s/after.json' % (c['afterdir'], e['id'])
        raw = show(ctx['root'], ctx['base_rev'], p)
        if raw is None:
            raise Uneval('lane receipt %s absent at %s' % (p, ctx['base_rev']))
        files[p] = {'from_lane': {'rev': ctx['base_rev'], 'path': p},
                    'sha256': sha256_bytes(raw), 'size': len(raw)}
    for p in ('PROVINCE.md', 'corpus/README.md', 'corpus/SOURCES.md', c['entry']):
        raw = show(ctx['root'], ctx['base_rev'], p)
        if raw is None:
            raise Uneval('lane landing file %s absent at %s' % (p, ctx['base_rev']))
        files[p] = {'from_lane': {'rev': ctx['base_rev'], 'path': p},
                    'sha256': sha256_bytes(raw), 'size': len(raw)}
    return {'files': files, 'overlay': {},
            'title': 'stand-in positive control: the lane landing at the base revision',
            'note': 'STAND-IN ONLY: plants the lane\'s own real round receipts and docs from '
                    'the base revision; it is a real positive for the stand-in counter',
            'expect': {'exit': 'any', 'doc_bindings_all_true': True},
            'extras': {}}


def spec_c2x(ctx):
    """ATTACK ARM (not in the default set): the oracle-only forgery of c2 PLUS the removal
    list a forger could learn from any published receipt (the `MaliciousSymlinkRemoved`
    diagnostics and the links they remove).  If the counter-time rerun cannot tell this
    from a real run the plan's "no REA run" claim rests on facts the oracle does not carry
    and the disclosed limits must say so.  Needs the pos fixtures (their real receipts are
    where the removal list is read from)."""
    c = ctx['c']
    pfiles, _, _ = load_fixtures(ctx['fixtures_root'], 'pos', ctx['root'])
    model = gap_model(ctx['root'], ctx['freeze'], c)
    dname = (model.get('removed') or {}).get('diagnostic') or 'MaliciousSymlinkRemoved'
    files, envs, fab = {}, {}, []
    for e in ctx['entries']:
        rel_after = '%s/%s/after.json' % (c['afterdir'], e['id'])
        if rel_after not in pfiles:
            raise Uneval('pos receipt for %s absent from the fixtures' % e['id'])
        real = json.loads(pfiles[rel_after])
        rnr = real['normalized_result']
        real_out = os.path.dirname(rnr.get('output_directory') or '')
        raw = carrier_bytes(ctx['root'], ctx['freeze'], e, ctx['cache'])
        length = len(raw) if raw is not None else (e.get('external') or {}).get('length')
        env, facts = forge_receipt(ctx, e, int(length))
        nr = env['normalized_result']
        new_out = os.path.dirname(nr['output_directory'])
        removed, diags = set(), []
        for d in rnr.get('diagnostics') or []:
            rep = d.get('report') or {}
            if rep.get('__typename__') != dname:
                continue
            link = rep.get('link') or ''
            marker = '/firmware.bin_extract/'
            if marker in link:
                removed.add(link.split(marker, 1)[1])
            d2 = json.loads(json.dumps(d).replace(real_out, new_out))
            diags.append(d2)
        nr['unpublished_entries'] = [u for u in nr['unpublished_entries']
                                     if u['relative_path'].split('/', 1)[1] not in removed]
        nr['extraction_gaps'] = [g for g in nr['extraction_gaps']
                                 if g.get('relative_path') is None
                                 or g['relative_path'].split('/', 1)[1] not in removed]
        nr['diagnostics'] = diags
        envs[e['id']] = env
        facts.update({'removed_links': len(removed), 'diagnostics': len(diags),
                      'gap_rows': len(nr['extraction_gaps']),
                      'unpublished_rows': len(nr['unpublished_entries'])})
        fab.append(facts)
    minted = mint_ids(ctx['work'], ctx['root'], ctx['freeze'], c, ctx['pkg65'], envs)
    for cid, env in envs.items():
        env['evidence_id'] = minted[cid]
        files['%s/%s/after.json' % (c['afterdir'], cid)] = jbytes(env)
    return {'files': files, 'overlay': {},
            'title': 'ATTACK ARM: oracle + removal-list forgery, no REA run',
            'note': 'informational: records whether a forgery that also carries the '
                    'removal diagnostics read off a published receipt reaches the target',
            'expect': {'exit': 'any', 'informational': True},
            'extras': {'fabrication': fab}}


SPECS = {'c0': spec_c0, 'c1': spec_c1, 'c1b': spec_c1b, 'c2': spec_c2, 'c3': spec_c3, 'c4': spec_c4,
         'pos': spec_pos, 'c2x': spec_c2x}


# ------------------------------------------------------------------ fixtures io

def write_fixtures(root_dir, key, spec):
    base = os.path.join(root_dir, key)
    if os.path.isdir(base):
        shutil.rmtree(base)
    os.makedirs(base)
    man = {'control': NAMES[key], 'key': key, 'claim': CLAIM, 'title': spec['title'],
           'note': spec['note'], 'expect': spec['expect'], 'files': {}, 'overlay': {},
           'generated_by': SEAT, 'generated_utc': utc_now()}
    man.update(spec.get('extras') or {})

    def store(group, rel, item):
        if isinstance(item, dict) and 'from_lane' in item:
            man[group][rel] = {'from_lane': item['from_lane'], 'sha256': item['sha256'],
                               'size': item['size']}
            return
        name = rel.replace('/', '__') + '.gz'
        sub = os.path.join(base, group)
        os.makedirs(sub, exist_ok=True)
        with open(os.path.join(sub, name), 'wb') as fh:
            fh.write(gz(item))
        man[group][rel] = {'fixture': '%s/%s' % (group, name), 'encoding': 'gzip',
                           'sha256': sha256_bytes(item), 'size': len(item)}

    for rel, item in sorted(spec['files'].items()):
        store('files', rel, item)
    for rel, item in sorted(spec['overlay'].items()):
        store('overlay', rel, item)
    if spec.get('blocks'):
        man['blocks'] = spec['blocks']
    write_json(os.path.join(base, 'manifest.json'), man)
    return man


def load_fixtures(root_dir, key, lane, ):
    """(planted files, overlay files, manifest) read from the committed fixtures."""
    mpath = os.path.join(root_dir, key, 'manifest.json')
    if not os.path.isfile(mpath):
        raise Uneval('fixture manifest absent: %s' % mpath)
    with open(mpath) as fh:
        man = json.load(fh)

    def fetch(meta):
        if 'from_lane' in meta:
            raw = show(lane, meta['from_lane']['rev'], meta['from_lane']['path'])
            if raw is None:
                raise Uneval('lane file %s@%s absent' % (meta['from_lane']['path'],
                                                          meta['from_lane']['rev']))
        else:
            with open(os.path.join(root_dir, key, meta['fixture']), 'rb') as fh2:
                raw = gzip.decompress(fh2.read())
        if sha256_bytes(raw) != meta['sha256'] or len(raw) != meta['size']:
            raise Uneval('fixture does not hash to its manifest pin: %s' % meta)
        return raw

    files = {rel: fetch(m) for rel, m in (man.get('files') or {}).items()}
    overlay = {rel: fetch(m) for rel, m in (man.get('overlay') or {}).items()}
    return files, overlay, man


# ------------------------------------------------------------------ counter, summary, judge

def run_counter(counter, c, root, rev, freeze, pkg65, work, cache, json_out):
    json_out = os.path.abspath(json_out)
    if os.path.exists(json_out):
        os.remove(json_out)
    argv = [sys.executable, '-I', '-B', counter, '--root', root, '--rev', rev,
            '--freeze', freeze, '--pkg65', pkg65]
    if c['supports_work']:
        argv += ['--work', work]
    if cache and c['supports_cache']:
        argv += ['--carrier-cache', cache]
    argv += ['--json-out', json_out]
    t0 = time.time()
    r = subprocess.run(argv, capture_output=True, cwd=work, env=dict(os.environ, HYAKU_SCRATCH=os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')))
    wall = round(time.time() - t0, 3)
    doc = None
    if os.path.isfile(json_out):
        try:
            with open(json_out) as fh:
                doc = json.load(fh)
        except (OSError, json.JSONDecodeError):
            doc = None
    src = 'json-out file' if doc is not None else None
    if doc is None:
        try:
            maybe = json.loads(r.stdout.decode(errors='replace') or 'null')
            if isinstance(maybe, dict):
                doc, src = maybe, 'stdout'
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    return {'argv': argv, 'exit_code': r.returncode, 'wall_s': wall,
            'stdout_sha256': sha256_bytes(r.stdout),
            'stdout_tail': r.stdout.decode(errors='replace').strip().splitlines()[-6:],
            'stderr_tail': r.stderr.decode(errors='replace').strip().splitlines()[-6:],
            'receipt': doc, 'receipt_source': src}


def summarize(doc, c):
    """The verdict shape of a counter receipt; anything absent stays absent (never true)."""
    if not isinstance(doc, dict) or 'carriers' not in doc and 'carriers_matched' not in doc:
        return {'present': False}
    carriers = doc.get('carriers') if isinstance(doc.get('carriers'), dict) else {}
    names = c['clauses'] or tuple(sorted({n for v in carriers.values() if isinstance(v, dict)
                                          for n, b in v.items() if n.endswith('_ok')
                                          or n in ('receipt_present', 'receipt_fresh',
                                                   'carrier_present')}))
    per, per_true = {}, {}
    for cid, d in carriers.items():
        if not isinstance(d, dict):
            continue
        per[cid] = sorted(n for n in names if d.get(n) is not True)
        per_true[cid] = sorted(n for n in names if d.get(n) is True)
    bindings = doc.get('bindings') if isinstance(doc.get('bindings'), dict) else {}
    rerun_errors = {}
    for cid, d in carriers.items():
        pe = d.get('projection_error') if isinstance(d, dict) else None
        if pe:
            err = pe.get('error') if isinstance(pe, dict) and isinstance(pe.get('error'), dict) else {}
            rerun_errors[cid] = err.get('code') or str(pe)[:80]
    return {'present': True, 'rerun_errors': rerun_errors, 'met_target': doc.get('met_target'),
            'carriers_matched': doc.get('carriers_matched'), 'target': doc.get('target'),
            'frozen_path_changed': doc.get('frozen_path_changed'),
            'bindings': {k: v for k, v in bindings.items() if isinstance(v, bool)},
            'per_carrier_failing': per, 'per_carrier_true': per_true,
            'per_carrier_matched': {k: d.get('matched') for k, d in carriers.items()
                                    if isinstance(d, dict)},
            'reason': doc.get('reason'), 'exit_code': doc.get('exit_code')}


def judge(key, expect, m, c, planted):
    """(ok, why, diag).  A clause the counter does not name fails closed, never open."""
    diag = {}
    got = m['exit_code']
    if got == 2:
        reason = (m['receipt'] or {}).get('reason') if isinstance(m['receipt'], dict) else None
        if reason and reason in (expect.get('accept_refusal') or []):
            diag['refused'] = reason
            return True, 'the counter refused to score it (exit 2, %s): not a match' % reason, diag
        return False, 'counter reported could-not-evaluate (exit 2)', diag
    want = expect.get('exit')
    if want == 'exit1' and got != 1:
        return False, 'expected exit 1, got %r' % (got,), diag
    if want == 'exit0' and got != 0:
        return False, 'expected exit 0, got %r' % (got,), diag
    if want == 'non-zero' and got == 0:
        return False, 'expected non-zero, got 0 (the control reached the target)', diag
    s = summarize(m['receipt'], c)
    if not s['present']:
        return False, 'the counter wrote no readable verdict, so clause attribution is unproven', diag
    target = s.get('target')
    em = expect.get('matched')
    if em == 'target':
        em = target
    if em is not None and s['carriers_matched'] != em:
        return False, 'carriers_matched %r != %r' % (s['carriers_matched'], em), diag
    if expect.get('matched_lt_target') and not (isinstance(s['carriers_matched'], int)
                                                and isinstance(target, int)
                                                and s['carriers_matched'] < target):
        return False, 'carriers_matched %r is not below target %r' % (s['carriers_matched'], target), diag
    if expect.get('doc_bindings_all_false'):
        known = {k: s['bindings'].get(k) for k in DOC_BINDINGS}
        if any(v is True for v in known.values()):
            return False, 'documentation bindings true on the do-nothing tree: %r' % [
                k for k, v in known.items() if v is True], diag
        absent = [k for k, v in known.items() if v is None]
        if absent:
            return False, 'documentation bindings absent, so "false" is unproven: %r' % absent, diag
    if expect.get('doc_bindings_all_true'):
        bad = [k for k in DOC_BINDINGS if s['bindings'].get(k) is not True]
        if bad:
            return False, 'documentation bindings not true under the positive control: %r' % bad, diag
    if expect.get('receipt_clauses_all_false'):
        green = {cid: [n for n in RECEIPT_CLAUSES if n in v]
                 for cid, v in s['per_carrier_true'].items()}
        green = {cid: v for cid, v in green.items() if v}
        diag['receipt_clauses_green'] = green
        if green:
            return False, 'receipt-derived clauses green with no receipt: %r' % green, diag
    if expect.get('all_bindings_true'):
        bad = sorted(k for k, v in s['bindings'].items() if v is not True)
        wanted = [b for b in c['bindings'] if b not in s['bindings']]
        if bad or wanted:
            return False, 'bindings not true under the positive control: %r %r' % (bad, wanted), diag
    if expect.get('every_slot_fails'):
        need = [clause(c, x) for x in expect['every_slot_fails']]
        for cid, failing in s['per_carrier_failing'].items():
            miss = [n for n in need if n not in failing]
            if miss:
                return False, 'slot %s: clauses %r did not fire (failing=%r)' % (cid, miss, failing), diag
    if expect.get('some_slot_fails'):
        need = [clause(c, x) for x in expect['some_slot_fails']]
        union = {n for v in s['per_carrier_failing'].values() for n in v}
        miss = [n for n in need if n not in union]
        if miss:
            return False, 'no slot failed %r (failing=%r)' % (miss, sorted(union)), diag
        diag['attributed_alone'] = {cid: [n for n in v if n not in need]
                                    for cid, v in s['per_carrier_failing'].items()}
    if expect.get('slot'):
        failing = s['per_carrier_failing'].get(expect['slot'])
        if failing is None:
            return False, 'slot %s absent from the counter verdict' % expect['slot'], diag
        need = [clause(c, x) for x in expect.get('slot_fails') or []]
        miss = [n for n in need if n not in failing]
        if miss:
            return False, 'slot %s: clauses %r did not fire (failing=%r)' % (expect['slot'], miss, failing), diag
        if expect.get('slot_fails_exactly'):
            allowed = set(clause(c, x) for x in expect['slot_fails_exactly'])
            extra = [n for n in failing if n not in allowed]
            diag['slot_failing'] = failing
            if extra:
                return False, ('slot %s fails %r beyond the one clause the control may trip '
                               '%r' % (expect['slot'], extra, sorted(allowed))), diag
    if expect.get('receipt_gap_kind'):
        rel = [p for p in planted if p.endswith('/after.json')]
        kinds = set()
        for p in rel:
            try:
                env = json.loads(planted[p])
            except json.JSONDecodeError:
                continue
            kinds |= {g.get('kind') for g in
                      (env.get('normalized_result') or {}).get('extraction_gaps') or []}
        diag['planted_gap_kinds'] = sorted(k for k in kinds if k)
        if expect['receipt_gap_kind'] not in kinds:
            return False, 'planted receipt lacks the %s gap' % expect['receipt_gap_kind'], diag
    return True, 'behaved as the plan states', diag


# ------------------------------------------------------------------ commands

def make_ctx(a, c, with_counter=True):
    root = os.path.abspath(a.lane)
    if not os.path.isdir(os.path.join(root, '.git')):
        raise Uneval('--lane is not a git checkout')
    freeze = a.freeze or git(root, 'rev-parse', 'HEAD').stdout.decode().strip()
    doc, entries = read_table(root, freeze, c)
    os.makedirs(a.work, exist_ok=True)
    return {'root': root, 'freeze': freeze, 'work': os.path.abspath(a.work), 'c': c,
            'doc': doc, 'entries': entries, 'params': rea_params(doc),
            'pkg65': a.pkg65, 'cache': a.carrier_cache,
            'base_rev': a.base_rev, 'fixtures_root': a.fixtures_root,
            'pos_envelopes': a.pos_envelopes}


def cmd_gen(a):
    counter = os.path.abspath(a.counter)
    c = consts(counter)
    ctx = make_ctx(a, c)
    keys = [k.strip() for k in a.controls.split(',') if k.strip()]
    results, bad = {}, []
    for key in keys:
        if key not in SPECS:
            print('unknown control %r' % key, file=sys.stderr)
            return 2
        fn = spec_pos_lane if (key == 'pos' and a.pos_from_lane) else SPECS[key]
        t0 = time.time()
        try:
            spec = fn(ctx)
        except Uneval as e:
            results[key] = {'status': 'could_not_generate', 'reason': str(e)}
            bad.append(key)
            continue
        man = write_fixtures(a.fixtures_root, key, spec)
        results[key] = {'status': 'generated', 'wall_s': round(time.time() - t0, 1),
                        'files': {r: m['sha256'] for r, m in man['files'].items()},
                        'overlay': {r: m['sha256'] for r, m in man['overlay'].items()}}
    ipath = os.path.join(a.fixtures_root, 'GEN-INDEX.json')
    prior = {}
    if os.path.isfile(ipath):
        try:
            with open(ipath) as fh:
                prior = (json.load(fh).get('results') or {})
        except (OSError, json.JSONDecodeError):
            prior = {}
    prior.update(results)
    write_json(ipath, {'seat': SEAT, 'utc': utc_now(), 'freeze': ctx['freeze'],
                       'base_rev': ctx['base_rev'], 'counter_consts': {
                           k: v for k, v in c.items() if k not in ('clauses', 'bindings')},
                       'results': prior})
    print(json.dumps({'generated': [k for k, v in results.items() if v['status'] == 'generated'],
                      'could_not_generate': bad}, sort_keys=True))
    return 2 if bad else 0


def stage_cache(work, base_cache, key, extra):
    """A per-control carrier cache: the real cache's `<pin>.bin` files + the control's own."""
    d = os.path.join(work, 'cache-' + key)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    if base_cache and os.path.isdir(base_cache):
        for n in os.listdir(base_cache):
            if n.endswith('.bin'):
                os.symlink(os.path.abspath(os.path.join(base_cache, n)), os.path.join(d, n))
    for pin, raw in extra.items():
        fp = os.path.join(d, pin + '.bin')
        if os.path.lexists(fp):
            os.remove(fp)
        with open(fp, 'wb') as fh:
            fh.write(raw)
    return d


def verify_committed(root, freeze, fixtures_root):
    """When the fixtures live inside the lane, every file under them must equal its blob at
    the freeze: the scored bytes are the committed bytes, not a dirty worktree."""
    top = os.path.realpath(root) + os.sep
    base = os.path.realpath(fixtures_root)
    if not (base + os.sep).startswith(top):
        return None
    bad = []
    n = 0
    for dp, _, fns in os.walk(base):
        for fn in fns:
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, os.path.realpath(root))
            blob = show(root, freeze, rel)
            n += 1
            if blob is None or sha256_file(full) != sha256_bytes(blob):
                bad.append(rel)
    if bad:
        raise Uneval('fixture files differ from the freeze (%d of %d): %s'
                     % (len(bad), n, bad[:3]))
    return n


def cmd_score(a):
    counter = os.path.abspath(a.counter)
    c = consts(counter)
    ctx = make_ctx(a, c)
    committed = verify_committed(ctx['root'], ctx['freeze'], a.fixtures_root)
    counter_present = os.path.isfile(counter)
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    keys = [k.strip() for k in a.controls.split(',') if k.strip()]
    receipts, failures, unevaluated = {}, [], []
    pos_files = None
    for key in keys:
        name = NAMES[key]
        cdir = os.path.join(out, key)
        os.makedirs(cdir, exist_ok=True)
        try:
            files, overlay, man = load_fixtures(a.fixtures_root, key, ctx['root'])
            if key == 'pos' and man.get('blocks'):
                files = dict(files)
                files.update(apply_landing(ctx['root'], ctx['freeze'], c, man['blocks']))
            extra_cache = {}
            if key in ('c4', 'c1b'):
                carrier_rel = '%s/%s/carrier.sqsh' % (c['afterdir'], man['slot'])
                if carrier_rel in overlay:
                    extra_cache[man['standard_carrier_pin']] = overlay[carrier_rel]
                # the other slots hold their genuine pos receipts when those fixtures exist
                if os.path.isfile(os.path.join(a.fixtures_root, 'pos', 'manifest.json')):
                    pfiles, _, pman = load_fixtures(a.fixtures_root, 'pos', ctx['root'])
                    for rel, raw in pfiles.items():
                        if rel.endswith('/after.json') and ('/%s/' % man['slot']) not in rel \
                                and rel.startswith(c['afterdir'] + '/'):
                            files.setdefault(rel, raw)
            sb = make_sandbox(ctx['root'], ctx['freeze'], ctx['work'], key)
            freeze = ctx['freeze']
            if overlay:
                freeze = plant_and_commit(sb, overlay, '%s: sandbox freeze overlay' % name)
            rev = plant_and_commit(sb, files, '%s: planted committed fixtures' % name) \
                if files else freeze
        except Uneval as e:
            receipts[name] = {'control': name, 'status': 'could_not_evaluate', 'reason': str(e)}
            write_json(os.path.join(cdir, 'receipt.json'), receipts[name])
            unevaluated.append(name)
            continue
        rec = {'control': name, 'seat': SEAT, 'claim': CLAIM, 'title': man.get('title'),
               'note': man.get('note'), 'expect': man.get('expect'),
               'sandbox': sb, 'freeze': freeze, 'rev': rev, 'lane_freeze': ctx['freeze'],
               'planted': {r: {'sha256': sha256_bytes(b), 'size': len(b)}
                           for r, b in sorted(files.items())},
               'overlay': {r: {'sha256': sha256_bytes(b), 'size': len(b)}
                           for r, b in sorted(overlay.items())},
               'fixtures_manifest': os.path.join(a.fixtures_root, key, 'manifest.json'),
               'manifest_sha256': sha256_file(os.path.join(a.fixtures_root, key, 'manifest.json'))}
        if not counter_present:
            rec.update({'status': 'could_not_evaluate',
                        'reason': 'counter absent: %s' % counter})
            write_json(os.path.join(cdir, 'receipt.json'), rec)
            receipts[name] = rec
            unevaluated.append(name)
            continue
        cache = stage_cache(ctx['work'], a.carrier_cache, key, extra_cache)
        measured = run_counter(counter, c, sb, rev, freeze, a.pkg65, ctx['work'], cache,
                               os.path.join(cdir, 'counter.json'))
        ok, why, diag = judge(key, man.get('expect') or {}, measured, c, files)
        msum = summarize(measured['receipt'], c)
        rerr = msum.get('rerun_errors') or {}
        if rerr:
            diag['rerun_errors'] = rerr
            # a counter-time REA rerun that did not run (REA 6.5.0 has a fixed 120 s deadline;
            # a loaded host trips it) turns projection_ok red for a reason that is not the
            # control's: a verdict that depends on that clause is not evaluable
            slot = (man.get('expect') or {}).get('slot')
            dependent = (key in ('c2', 'c2x', 'pos')
                         or (key in ('c4', 'c1b') and slot in rerr))
            if dependent:
                rec.update({'status': 'could_not_evaluate',
                            'reason': 'counter-time REA rerun did not run: %r' % rerr,
                            'command': ' '.join(measured['argv']),
                            'exit_code': measured['exit_code'], 'diag': diag,
                            'measured': msum, 'stdout_sha256': measured['stdout_sha256'],
                            'wall_s': measured['wall_s'], 'utc': utc_now()})
                write_json(os.path.join(cdir, 'receipt.json'), rec)
                receipts[name] = rec
                unevaluated.append(name)
                continue
        if key in ('c4', 'c1b'):
            others = [r for r in files if r.endswith('/after.json')
                      and ('/%s/' % man['slot']) not in r]
            diag['other_slots_planted'] = len(others)
            diag['matched_equals_other_slots'] = (
                (measured['receipt'] or {}).get('carriers_matched') == len(others))
        rec.update({'command': ' '.join(measured['argv']), 'exit_code': measured['exit_code'],
                    'stdout_sha256': measured['stdout_sha256'], 'wall_s': measured['wall_s'],
                    'utc': utc_now(), 'stdout_tail': measured['stdout_tail'],
                    'stderr_tail': measured['stderr_tail'],
                    'counter': counter, 'counter_sha256': sha256_file(counter),
                    'verdict': 'as_expected' if ok else 'misbehaved', 'why': why,
                    'diag': diag, 'receipt_source': measured['receipt_source'],
                    'measured': summarize(measured['receipt'], c)})
        write_json(os.path.join(cdir, 'receipt.json'), rec)
        receipts[name] = rec
        if not ok:
            failures.append(name)
    summary = {'seat': SEAT, 'claim': CLAIM, 'utc': utc_now(), 'freeze': ctx['freeze'],
               'lane': ctx['root'], 'fixtures_verified_against_freeze': committed, 'counter': counter, 'counter_present': counter_present,
               'counter_sha256': sha256_file(counter) if counter_present else None,
               'counter_consts': {k: v for k, v in c.items() if k not in ('clauses', 'bindings')},
               'controls': {k: {'verdict': v.get('verdict', v.get('status')),
                                'exit_code': v.get('exit_code'), 'why': v.get('why', v.get('reason')),
                                'stdout_sha256': v.get('stdout_sha256'),
                                'carriers_matched': (v.get('measured') or {}).get('carriers_matched'),
                                'wall_s': v.get('wall_s')} for k, v in receipts.items()},
               'failures': failures, 'unevaluated': unevaluated, 'kill_rule_fires': False,
               'kill_rule_detail': []}
    for name, rec in receipts.items():
        m = rec.get('measured') or {}
        if name in ('CTL-C1-0', 'CTL-C1-1', 'CTL-C1-4') and m.get('present'):
            full = (m.get('carriers_matched') == m.get('target')
                    and all(v is True for v in (m.get('bindings') or {}).values()))
            if full:
                summary['kill_rule_fires'] = True
                summary['kill_rule_detail'].append('%s reached the target with every binding true' % name)
        if name == 'CTL-C1-0' and (rec.get('diag') or {}).get('receipt_clauses_green'):
            summary['kill_rule_fires'] = True
            summary['kill_rule_detail'].append('do-nothing scored receipt-derived clauses green')
    if 'CTL-C1-2X' in receipts:
        m = receipts['CTL-C1-2X'].get('measured') or {}
        summary['informational_c2x'] = {
            'carriers_matched': m.get('carriers_matched'), 'target': m.get('target'),
            'reached_target': m.get('carriers_matched') == m.get('target'),
            'per_carrier_failing': m.get('per_carrier_failing'),
            'reading': 'an oracle + removal-list forgery that reaches the target is evidence '
                       'for a disclosed limit, not a kill-rule event (c2x is outside the plan)'}
    write_json(os.path.join(out, 'summary.json'), summary)
    if a.json_out:
        write_json(a.json_out, summary)
    print(json.dumps({'controls': len(receipts), 'failures': failures,
                      'unevaluated': unevaluated, 'kill_rule_fires': summary['kill_rule_fires']},
                     sort_keys=True))
    if unevaluated:
        return 2
    return 1 if failures or summary['kill_rule_fires'] else 0


# ------------------------------------------------------------------ selftest

STUB = '''#!/usr/bin/env python3
import argparse, json, os, sys
ap = argparse.ArgumentParser()
for f in ('--root', '--rev', '--freeze', '--pkg65', '--work', '--json-out', '--carrier-cache'):
    ap.add_argument(f)
a = ap.parse_args()
CARRIERS = 'tools/round-50/carriers.json'
AFTERDIR = 'corpus/evidence/round-50/c1'
HANDLER = 'squashfs_v4_le'
PROV_PREFIX = '/fast/scratch/hyaku/kaidoku-r50/'
CLAUSES = ('receipt_present', 'subject_pin_ok', 'handler_ok', 'projection_ok', 'layout_ok')
mode = os.environ.get('STUB_MODE', 'red')
b = {k: mode == 'green' for k in ('province_core_section', 'province_core_row', 'frontier_note',
                                  'entry_present', 'sourced', 'coverage_map_row')}
ok = mode == 'green'
doc = {'met_target': ok, 'carriers_matched': 4 if ok else 0, 'target': 4, 'bindings': b,
       'carriers': {'a': {n: ok for n in CLAUSES}}, 'frozen_path_changed': [],
       'exit_code': 0 if ok else 1}
json.dump(doc, open(a.json_out, 'w'))
sys.exit(0 if ok else (2 if mode == 'unevaluable' else 1))
'''


def cmd_selftest(a):
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    checks = []

    def add(name, ok, detail):
        checks.append({'check': name, 'ok': bool(ok), 'detail': detail})

    stub = os.path.join(work, 'stub-counter.py')
    with open(stub, 'w') as fh:
        fh.write(STUB)
    k = scrape(stub)
    c = consts(stub)
    add('constants are scraped from the counter, not imported',
        c['handler'] == 'squashfs_v4_le' and c['afterdir'] == 'corpus/evidence/round-50/c1'
        and c['extractor'] == 'sasquatch' and c['prov_base'] == '/fast/scratch/hyaku/kaidoku-r50',
        json.dumps({x: c[x] for x in ('handler', 'extractor', 'prov_base')}))
    add('flag support is detected from the counter source (stub declares both)',
        c['supports_work'] is True and c['supports_cache'] is True, str(k['__supports_work__']))
    repo = os.path.join(work, 'fixture-lane')
    if os.path.isdir(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)
    git(repo, 'init', '--quiet')
    assert_toplevel(repo)
    for kk, vv in (('user.name', 'fx'), ('user.email', 'fx@fx'), ('commit.gpgsign', 'false')):
        git(repo, 'config', kk, vv)
    with open(os.path.join(repo, 'base.txt'), 'w') as fh:
        fh.write('base\n')
    git(repo, 'add', 'base.txt')
    git(repo, 'commit', '--quiet', '-m', 'base')
    freeze = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
    sb = make_sandbox(repo, freeze, work, 'selftest')
    rev = plant_and_commit(sb, {'x/after.json': b'{}\n'}, 'plant')
    add('planted commit descends from the freeze',
        git(sb, 'merge-base', '--is-ancestor', freeze, rev, check=False).returncode == 0,
        '%s -> %s' % (freeze[:8], rev[:8]))
    # fixtures round-trip: gzip is deterministic, from_lane reads git
    spec = {'files': {'a/b.json': b'{"k": 1}\n',
                      'a/lane.txt': {'from_lane': {'rev': freeze, 'path': 'base.txt'},
                                     'sha256': sha256_bytes(b'base\n'), 'size': 5}},
            'overlay': {}, 'title': 't', 'note': 'n', 'expect': {'exit': 'exit1'}}
    fx = os.path.join(work, 'fx')
    write_fixtures(fx, 'c0', spec)
    files, _, man = load_fixtures(fx, 'c0', repo)
    add('fixtures round-trip byte-exact (gzip + from_lane)',
        files['a/b.json'] == b'{"k": 1}\n' and files['a/lane.txt'] == b'base\n', str(sorted(files)))
    g1, g2 = gz(b'abc'), gz(b'abc')
    add('gzip fixtures are deterministic', g1 == g2, sha256_bytes(g1)[:12])
    # tamper detection
    gp = os.path.join(fx, 'c0', 'files', 'a__b.json.gz')
    with open(gp, 'wb') as fh:
        fh.write(gz(b'{"k": 2}\n'))
    try:
        load_fixtures(fx, 'c0', repo)
        add('a tampered fixture is refused', False, 'accepted')
    except Uneval as e:
        add('a tampered fixture is refused', True, str(e)[:80])
    # fixtures inside the lane must equal the freeze blobs
    write_fixtures(os.path.join(repo, 'fx'), 'c0', {'files': {'a.json': b'{}\n'}, 'overlay': {},
                                                   'title': 't', 'note': 'n', 'expect': {}})
    git(repo, 'add', 'fx')
    git(repo, 'commit', '--quiet', '-m', 'fixtures')
    fz = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
    n = verify_committed(repo, fz, os.path.join(repo, 'fx'))
    add('committed fixtures verify against the freeze', isinstance(n, int) and n >= 2, str(n))
    with open(os.path.join(repo, 'fx', 'c0', 'files', 'a.json.gz'), 'wb') as fh:
        fh.write(gz(b'dirty\n'))
    try:
        verify_committed(repo, fz, os.path.join(repo, 'fx'))
        add('a dirty fixture worktree is refused', False, 'accepted')
    except Uneval as e:
        add('a dirty fixture worktree is refused', True, str(e)[:80])
    add('fixtures outside the lane are not verified', verify_committed(repo, fz, os.path.join(work, 'fx')) is None, '')
    # judge
    for mode, want_exit, expect, should in (
            ('red', 1, {'exit': 'exit1', 'matched': 0, 'doc_bindings_all_false': True}, True),
            ('red', 1, {'exit': 'exit0'}, False),
            ('green', 0, {'exit': 'exit0', 'matched': 'target', 'all_bindings_true': True}, True),
            ('green', 0, {'exit': 'non-zero'}, False),
            ('unevaluable', 2, {'exit': 'non-zero'}, False)):
        os.environ['STUB_MODE'] = mode
        m = run_counter(stub, c, sb, rev, freeze, work, work, None, os.path.join(work, 'j.json'))
        ok, why, _ = judge('x', expect, m, c, {})
        add('judge: %s stub vs %s -> %s' % (mode, json.dumps(expect, sort_keys=True), should),
            ok == should, why)
    m2 = {'exit_code': 2, 'receipt': {'reason': 'oracle_env_error'}, 'stdout_tail': [],
          'stderr_tail': []}
    ok, why, _ = judge('x', {'exit': 'non-zero', 'accept_refusal': ['oracle_env_error']}, m2, c, {})
    add('judge: a named refusal (exit 2) is accepted only when the control lists it', ok, why)
    ok, why, _ = judge('x', {'exit': 'non-zero', 'accept_refusal': ['other']}, m2, c, {})
    add('judge: an unlisted exit 2 is could-not-evaluate', not ok, why)
    ok, why, _ = judge('x', {'exit': 'non-zero'}, m2, c, {})
    add('judge: exit 2 with no refusal list is never a pass', not ok, why)
    os.environ['STUB_MODE'] = 'red'
    m = run_counter(stub, c, sb, rev, freeze, work, work, None, os.path.join(work, 'j.json'))
    ok, why, _ = judge('x', {'exit': 'non-zero', 'slot': 'a', 'slot_fails': ['marker'],
                             'slot_fails_exactly': ['marker']}, m, c, {})
    add('judge: slot_fails_exactly refuses extra failing clauses', not ok, why)
    ok, why, _ = judge('x', {'exit': 'non-zero', 'every_slot_fails': ['nonexistent-clause-name']}, m, c, {})
    add('judge: a clause the counter never lists fails closed (a literal name is not a pass)',
        not ok and 'did not fire' in why, why)
    del os.environ['STUB_MODE']
    # province blocks name what the plan's bindings read
    pb = province_blocks(c)
    add('landing text names the handler, the AVM marker, the entry path and the frontier mark',
        'squashfs_v4_le' in pb['province_core'] and 'AVM marker' in pb['province_core']
        and c['entry'] in pb['province_core'] and c['frontier_mark'] in pb['province_frontier']
        and c['stem'] in pb['province_frontier'], 'ok')
    passed = sum(1 for x in checks if x['ok'])
    doc = {'selftest': 'c1-controls', 'cases': len(checks), 'passed': passed,
           'failed': [x['check'] for x in checks if not x['ok']], 'checks': checks}
    write_json(os.path.join(work, 'selftest.json'), doc)
    print(json.dumps({k2: doc[k2] for k2 in ('selftest', 'cases', 'passed', 'failed')},
                     sort_keys=True))
    return 0 if passed == len(checks) else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=('gen', 'score', 'selftest'))
    ap.add_argument('--lane')
    ap.add_argument('--freeze')
    ap.add_argument('--counter', default='tools/round-50/c1-counter.py')
    ap.add_argument('--pkg65')
    ap.add_argument('--work')
    ap.add_argument('--out')
    ap.add_argument('--carrier-cache')
    ap.add_argument('--fixtures-root', default=DEFAULT_FIXTURES)
    ap.add_argument('--controls', default=','.join(ALL_CONTROLS))
    ap.add_argument('--base-rev', default=DEFAULT_BASE_REV,
                    help='lane revision the round-41/round-36 source bytes are read from')
    ap.add_argument('--pos-from-lane', action='store_true',
                    help='STAND-IN ONLY: pos = the lane\'s own landing at --base-rev')
    ap.add_argument('--pos-envelopes',
                    help='gen pos from genuine REA receipts made elsewhere '
                         '(<dir>/<id>.envelope.json[.gz]); each must carry the carrier pin')
    ap.add_argument('--json-out')
    a = ap.parse_args(argv)
    if not a.work:
        a.work = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
                              'kaidoku-r50', 'c1-controls')
    try:
        if a.mode == 'selftest':
            return cmd_selftest(a)
        if not a.lane:
            print('--lane is required', file=sys.stderr)
            return 2
        if a.mode == 'score' and not a.out:
            print('--out is required for score', file=sys.stderr)
            return 2
        if not os.path.isabs(a.counter):
            a.counter = os.path.join(os.path.abspath(a.lane), a.counter)
        if not os.path.isabs(a.fixtures_root):
            a.fixtures_root = os.path.join(os.path.abspath(a.lane), a.fixtures_root)
        if a.pos_envelopes:
            a.pos_envelopes = os.path.abspath(a.pos_envelopes)
        return cmd_gen(a) if a.mode == 'gen' else cmd_score(a)
    except Uneval as e:
        print('could not evaluate: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
