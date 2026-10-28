#!/usr/bin/env python3
"""kaidoku round 49 - R49-C1 after-freeze data procedure (the runner).

DATA side of the R49-C1 claim: for every carrier id frozen in
`tools/round-49/carriers.json` it runs REA 6.5.0 `extract-firmware` on the
carrier bytes and records the receipt tree under
`corpus/evidence/round-49/c1/<id>/`.

The L1 runs this AFTER the freeze. Seats never run it: a pre-freeze receipt's
first-add commit would not be a strict descendant of the freeze, so the
counter's `receipt_fresh` binding could never hold (round-42 counter,
`receipt_fresh`). The tool therefore refuses to write into the default
(committed) evidence root unless the caller states that the freeze is in place:

    KAIDOKU_C1_DATA_RUN=1 tools/round-49/c1-run.sh
    tools/round-49/c1-run.sh --data-run

`--dry-run` prints every command it WOULD run and writes nothing at all.

Where the run writes
--------------------
REA's `output_directory` is a fresh root inside the round's private scratch
segment (`$HYAKU_SCRATCH`/kaidoku-r49, default /fast/scratch/hyaku/kaidoku-r49),
and the receipt's `parameters.output_directory` names that `/kaidoku-r49/` path -
the binding the frozen claims text states

    "the receipt's `parameters.output_directory` names this round's
     `/kaidoku-r49/` scratch segment and the evidence id is minted over that
     provenance; the runner records `provenance.json` binding the
     scratch-produced tree to the verbatim committed copy under
     `corpus/evidence/round-49/c1/`"

(plans/round-49-claims.md, R49-C1 predicate). The tree REA produced is copied
VERBATIM into `<lane>/corpus/evidence/round-49/c1/<id>/` - bytes, symlinks,
modes and mtimes preserved - and `provenance.json` binds the two, so the
committed evidence carries the produced bytes exactly.

`--rea-outdir-mode evidence` instead points REA at the evidence directory
itself (the receipt then names that path); it is the alternative binding, kept
so the two artifacts can be reconciled without editing either.

REA 6.5.0 refuses an output root that already exists ("Extraction output root
already exists"), so the runner never pre-creates it. An existing evidence
directory fails closed (exit 2) unless --force replaces it.

REA's own task directory (`rea-firmware-<uuid>`) goes under TMPDIR, which the
runner points at the same private scratch directory, so nothing but the
pin table, the receipt and this runner's own files reaches the evidence
directory.

The extractor
-------------
REA runs `unblob` with `--log <task dir>/unblob.log` and deletes the task
directory when the run ends, so a successful envelope never shows which
extractor ran. The runner therefore sets `REA_UNBLOB_COMMAND` to a transparent
tee generated into the scratch: it runs the real unblob
(`$HOME/.local/bin/unblob`) with REA's arguments unchanged, copies the log out
of the task directory and exits with unblob's own exit code. The receipt's
`extract-env.json` records the real unblob's digest, the sasquatch digest on
the fixed PATH, the PATH itself and the extract command line the log names
(`sasquatch -le|-be ...`) - the binding the round-42 counter's `extract_env_ok`
clause reads. `--no-unblob-log-tee` (or C1_UNBLOB_LOG_TEE=0) runs unblob
directly; the log line is then recorded as absent, honestly.

Per carrier the outdir holds, after a run:

    <id>/firmware.bin_extract/...   the tree REA published (committed verbatim)
    <id>/envelope.json              stdout captured BYTE-FOR-BYTE (the receipt)
    <id>/after.json                 the envelope's `data` object (the shape the
                                    round-42 counter reads as the after-receipt)
    <id>/stdout.log                 the same stdout bytes (explicit capture)
    <id>/stderr.log                 stderr captured byte-for-byte
    <id>/unblob.log                 unblob's log, copied out of REA's task dir
    <id>/extract-env.json           the toolchain that actually ran
    <id>/extract-tree.tsv           relpath/kind/size/sha256 of every entry REA
                                    produced, snapshotted before the receipts
                                    were written (the verbatim-copy record)
    <id>/provenance.json            output_directory <-> committed tree
    <id>/run.json                   command, exit_code, stdout_sha256, wall_s,
                                    carrier, rev_at_run (+ argv, pins, digests)

and, once, `<evidence-root>/manifest.json` mapping every carrier id to its
outdir and its run.json path.

Exit codes (semantic, per the round contract):
    0  every carrier ran and produced a receipt
    1  at least one carrier failed (REA exit != 0, no receipt, or a pin
       mismatch between the frozen carrier bytes and the fixture on disk)
    2  could not evaluate (bad arguments, carriers.json missing/unparsable,
       a fixture that does not resolve, an occupied outdir)
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

SEAT = 'R49C1Run'
SCHEMA_RUN = 'kaidoku-r49-c1-run-v1'
SCHEMA_MANIFEST = 'kaidoku-r49-c1-manifest-v1'
SCHEMA_ENV = 'kaidoku-r49-c1-extract-env-v1'
SCHEMA_PROV = 'kaidoku-r49-c1-provenance-v1'

REA_PIN = 'rea-agents@6.5.0'
DEFAULT_CARRIERS = 'tools/round-49/carriers.json'
DEFAULT_EVIDENCE = 'corpus/evidence/round-49/c1'
ROUND_SEGMENT = 'kaidoku-r49'
SCRATCH_PREFIX = 'probe-R49C1Run'
# Fixture directories searched when a carrier entry does not name a path.
FIXTURE_DIRS = (
    'corpus/evidence/round-42/c2/fixtures',
    'corpus/evidence/round-44/carriers',
    'corpus/evidence/round-44/fixtures',
)
# The child PATH of every run: identical to the round-42 counter's FIXED_PATH
# so the extractor that resolves (`sasquatch`) is the same binary in the run
# and in the counter's own rerun.
FIXED_PATH = ':'.join([
    '/usr/local/bin', '/usr/bin', '/bin',
    os.path.expanduser('~/.local/bin'),
    os.path.expanduser('~/.local/share/fnm/node-versions/v24.21.0/installation/bin'),
])
HEX64 = re.compile(r'\A[0-9a-f]{64}\Z')
# Files this runner writes into an evidence directory. They are the ones the
# occupancy guard protects; REA's own published tree is never in this list.
RECEIPT_FILES = ('envelope.json', 'after.json', 'stdout.log', 'stderr.log',
                 'unblob.log', 'extract-env.json', 'extract-tree.tsv',
                 'provenance.json', 'run.json')

# A transparent unblob tee: run the real unblob with REA's arguments
# unchanged, copy the `--log` file out of the REA task directory, exit with
# unblob's own exit code. It never edits an argument, the input or the log.
TEE_SOURCE = """#!/usr/bin/env bash
set -u
real=${C1_REAL_UNBLOB:?C1_REAL_UNBLOB must be set}
case "$real" in /*) ;; *) echo "unblob-tee: C1_REAL_UNBLOB must be absolute" >&2; exit 2 ;; esac
log=
prev=
for a in "$@"; do
  if [[ $prev == --log ]]; then log=$a; fi
  prev=$a
done
"$real" "$@"
rc=$?
if [[ -n ${C1_LOG_COPY:-} && -n $log && -f $log ]]; then
  cp -- "$log" "$C1_LOG_COPY" || echo "unblob-tee: copy of $log failed" >&2
fi
exit "$rc"
"""


class Unevaluable(Exception):
    """Could not evaluate: exit 2."""


# ----------------------------------------------------------------- helpers

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for block in iter(lambda: fh.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def lane_root(start):
    """Nearest ancestor of `start` holding corpus/evidence and plans/."""
    d = os.path.abspath(start)
    for _ in range(6):
        if os.path.isdir(os.path.join(d, 'corpus', 'evidence')) and \
                os.path.isdir(os.path.join(d, 'plans')):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def git_rev(root):
    try:
        p = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'],
                           capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if p.returncode != 0:
        return None
    return p.stdout.decode('utf-8', 'replace').strip() or None


def norm_key(text):
    """Lowercase, drop every non-alphanumeric character (id/file matching)."""
    return re.sub(r'[^a-z0-9]+', '', str(text).lower())


def unblob_path():
    return os.path.join(os.path.expanduser('~'), '.local', 'bin', 'unblob')


# --------------------------------------------------------------- carriers

def load_carriers(path):
    if not os.path.isfile(path):
        raise Unevaluable('carriers.json not found: %s' % path)
    try:
        with open(path, 'rb') as fh:
            raw = fh.read()
    except OSError as e:
        raise Unevaluable('carriers.json unreadable: %s' % e)
    try:
        doc = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise Unevaluable('carriers.json is not JSON: %s' % e)
    entries = doc.get('carriers') if isinstance(doc, dict) else doc
    if not isinstance(entries, list) or not entries:
        raise Unevaluable('carriers.json carries no carrier list')
    out = []
    seen = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise Unevaluable('carriers[%d] is not an object' % i)
        cid = entry.get('id')
        if not isinstance(cid, str) or not cid.strip():
            raise Unevaluable('carriers[%d] has no id' % i)
        cid = cid.strip()
        if cid in seen:
            raise Unevaluable('carriers.json repeats id %r' % cid)
        seen.add(cid)
        out.append((cid, entry))
    return doc, out


PATH_KEYS = ('fixture', 'fixture_path', 'carrier_path', 'carrier_file', 'path',
             'file', 'local_path', 'input', 'bytes', 'source_path')


def fixture_listing(lane):
    listing = []
    for d in FIXTURE_DIRS:
        base = os.path.join(lane, d)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if name.endswith('.bin'):
                listing.append(os.path.join(base, name))
    return listing


def resolve_fixture(lane, cid, entry):
    """(absolute path, how) of the carrier bytes for one carrier entry.

    Resolution order:
      1. an explicit path-ish field of the entry (absolute, lane-relative, or
         a bare file name searched in the fixture directories);
      2. the fixture directories' own listing, matched against the entry id
         with case and separators ignored, so an id written `V1LE` finds
         `v1-le--squashfs_v1.0_le.bin` and an id written `v1-le` finds the
         same file. The match is on the file's stem (the part before `--`), so
         `v2-le` never resolves to `v2ns-le--...`.
    """
    notes = []
    for key in PATH_KEYS:
        val = entry.get(key)
        if not isinstance(val, str) or not val.strip():
            continue
        val = val.strip()
        cands = []
        if os.path.isabs(val):
            cands.append(val)
        else:
            cands.append(os.path.join(lane, val))
            for d in FIXTURE_DIRS:
                cands.append(os.path.join(lane, d, val))
        for cand in cands:
            if os.path.isfile(cand):
                return os.path.realpath(cand), 'entry field %r' % key
        notes.append('entry field %r=%r did not resolve' % (key, val))

    want = norm_key(cid)
    # the fixture_id field is the file stem as published by unblob
    fids = [entry.get('fixture_id')] if isinstance(entry.get('fixture_id'), str) else []
    matches = []
    for path in fixture_listing(lane):
        stem = os.path.basename(path).split('--', 1)[0]
        keys = {norm_key(stem), norm_key(os.path.basename(path))}
        keys |= {norm_key(f) for f in fids if f}
        if want in keys:
            matches.append(path)
    if len(matches) == 1:
        return os.path.realpath(matches[0]), 'fixture listing, id match'
    if len(matches) > 1:
        raise Unevaluable('carrier %r matches %d fixture files: %s'
                          % (cid, len(matches),
                             ', '.join(os.path.basename(m) for m in matches)))
    raise Unevaluable('carrier %r: no fixture file resolves (%s)'
                      % (cid, '; '.join(notes) if notes
                         else 'no path field and no id match'))


def carrier_pin(entry):
    for key in ('sha256', 'pin', 'digest', 'image_sha256'):
        val = entry.get(key)
        if isinstance(val, str) and HEX64.match(val.lower()):
            return val.lower()
    image = entry.get('image')
    if isinstance(image, dict):
        val = image.get('sha256')
        if isinstance(val, str) and HEX64.match(val.lower()):
            return val.lower()
    return None


# ------------------------------------------------------------- the runner

def build_plan(lane, evidence_root, cid, entry, scratch_root, rea_command,
               outdir_mode='evidence'):
    fixture, how = resolve_fixture(lane, cid, entry)
    pin = carrier_pin(entry)
    digest = sha256_file(fixture)
    run_dir = os.path.join(scratch_root, SCRATCH_PREFIX, 'c1-run.%s.%d'
                           % (cid, os.getpid()))
    outdir = os.path.join(evidence_root, cid)
    # Where REA's `output_directory` points. `evidence` (default) makes the
    # receipt's parameters.output_directory name the committed evidence path -
    # the binding the frozen claims text states (plans/round-49-claims.md: "the
    # receipt's parameters.output_directory names a corpus/evidence/round-49/c1/
    # path"). `scratch` points it at this round's scratch segment instead, for a
    # counter that binds the round through the /kaidoku-r49/ segment; the
    # produced tree is then copied verbatim into the evidence directory.
    rea_outdir = outdir if outdir_mode == 'evidence' else os.path.join(
        run_dir, 'rea-out')
    argv = list(rea_command) + [
        'extract-firmware', '--format', 'json', '--full-output',
        fixture, rea_outdir,
    ]
    return {
        'id': cid,
        'entry': entry,
        'fixture': fixture,
        'fixture_how': how,
        'fixture_sha256': digest,
        'fixture_size': os.path.getsize(fixture),
        'fixture_pin': pin,
        'pin_ok': (pin is None) or (digest == pin),
        'outdir': outdir,
        'rea_outdir': rea_outdir,
        'outdir_mode': outdir_mode,
        'run_dir': run_dir,
        'argv': argv,
        'unblob': unblob_path(),
        'rea_command': list(rea_command),
    }


def command_string(plan, unblob_command=None):
    env = 'REA_UNBLOB_COMMAND=%s' % (unblob_command or plan['unblob'])
    return '%s %s' % (env, ' '.join(plan['argv']))


def tool_pins():
    """(pins, notes) for the binaries the run uses, resolved on the fixed PATH.

    The shape mirrors the round-42 runner's `extract-env.json`: `unblob` and
    `sasquatch` carry `path`/`sha256`/`version` plus the first version line, so
    the counter's `extract_env_ok` clause reads the same keys it read there.
    """
    pins = {}
    notes = []
    env = dict(os.environ)
    env['PATH'] = FIXED_PATH
    for name in ('unblob', 'sasquatch', 'sasquatch-v4be', 'npx', 'node'):
        path = shutil.which(name, path=FIXED_PATH)
        if not path:
            if name in ('unblob', 'sasquatch'):
                notes.append('%s not found on the fixed PATH' % name)
            continue
        real = os.path.realpath(path)
        info = {'path': real, 'sha256': sha256_file(real)}
        if name in ('unblob', 'sasquatch'):
            try:
                args = [real, '--version'] if name == 'unblob' else [real, '-version']
                p = subprocess.run(args, capture_output=True, timeout=60, env=env)
                lines = (p.stdout or p.stderr).decode('utf-8', 'replace').splitlines()
                info['version_line'] = lines[0].strip() if lines else None
                m = re.search(r'[Vv]ersion ([0-9][0-9A-Za-z.]*)',
                              info['version_line'] or '')
                info['version'] = m.group(1) if m else None
            except (OSError, subprocess.SubprocessError) as e:
                info['version_line'] = None
                info['version'] = None
                notes.append('%s --version failed: %s' % (name, e))
        pins[name] = info
    return pins, notes


def rea_package_root():
    """The installed rea-agents 6.5.0 package root (the npx cache entry)."""
    cache = os.environ.get('npm_config_cache') or os.path.join(
        os.path.expanduser('~'), '.npm')
    root = os.path.join(cache, '_npx')
    if not os.path.isdir(root):
        return None
    best = None
    for dirpath, dirnames, filenames in os.walk(root):
        if 'package.json' in filenames and os.path.basename(dirpath) == 'rea-agents':
            try:
                with open(os.path.join(dirpath, 'package.json'), 'rb') as fh:
                    ver = json.load(fh).get('version')
            except (OSError, json.JSONDecodeError):
                continue
            if ver == REA_PIN.split('@', 1)[1]:
                best = dirpath
    return best


def copy_tree_verbatim(src, dst):
    """Copy `src` into `dst` preserving bytes, symlinks, modes and mtimes."""
    if not os.path.isdir(src):
        return
    shutil.copytree(src, dst, symlinks=True, dirs_exist_ok=True)


def snapshot_tree(root, skip=()):
    """[(relpath, kind, size, sha256)] for every entry under `root`.

    Symlinks are recorded as symlinks (never followed); names in `skip` at the
    top level are ignored, so the receipt files this runner writes are not
    mistaken for produced bytes.
    """
    entries = []
    if not os.path.isdir(root):
        return entries
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(dirnames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if rel.split(os.sep)[0] in skip:
                dirnames.remove(name)
                continue
            if os.path.islink(full):
                entries.append((rel, 'symlink', None, None))
                dirnames.remove(name)
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if rel.split(os.sep)[0] in skip:
                continue
            if os.path.islink(full):
                entries.append((rel, 'symlink', None, None))
            elif os.path.isfile(full):
                st = os.stat(full)
                entries.append((rel, 'file', st.st_size, sha256_file(full)))
            else:
                entries.append((rel, 'other', None, None))
    entries.sort()
    return entries


def write_tree_tsv(path, entries):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('# relpath\tkind\tsize\tsha256\n')
        for rel, kind, size, digest in entries:
            fh.write('%s\t%s\t%s\t%s\n' % (
                rel.replace(os.sep, '/'), kind,
                '-' if size is None else size, digest or '-'))


def write_json(path, doc):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, sort_keys=True, indent=2, ensure_ascii=False)
        fh.write('\n')


def write_tee(path):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(TEE_SOURCE)
    os.chmod(path, 0o755)
    return path


def extract_command_line(log_path):
    """The extract command line unblob's log names, or None."""
    try:
        with open(log_path, 'r', encoding='utf-8', errors='replace') as fh:
            text = fh.read()
    except OSError:
        return None
    m = re.search(r"Running extract command\s*command='([^']*)'", text)
    if m:
        return m.group(1)
    for line in text.splitlines():
        if 'sasquatch' in line:
            return line.strip()
    return None


def clear_outdir(path, force):
    """Ensure `path` does not exist (REA refuses an existing output root)."""
    if not os.path.exists(path):
        return 'absent'
    if not force:
        raise Unevaluable(
            'output directory %s already exists. REA 6.5.0 refuses an existing '
            'extraction root, so this runner never reuses an evidence directory '
            '(a second run would also overwrite committed receipts). Re-run with '
            '--force to replace it, or delete it first.' % path)
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
    return 'removed'


def run_carrier(plan, lane, evidence_root, scratch_root, timeout, keep_scratch,
                fake, use_tee, force):
    """Execute one carrier and write its receipt tree. Returns the run.json doc."""
    outdir = plan['outdir']
    run_dir = plan['run_dir']
    rea_outdir = plan['rea_outdir']
    os.makedirs(os.path.dirname(outdir), exist_ok=True)
    cleared = clear_outdir(outdir, force)
    os.makedirs(run_dir, exist_ok=True)
    # In `scratch` mode REA's output root is fresh inside the run dir; in
    # `evidence` mode it IS the evidence dir (already cleared above).
    if rea_outdir != outdir:
        cleared_rea = clear_outdir(rea_outdir, True)
    else:
        cleared_rea = cleared

    env = dict(os.environ)
    env['PATH'] = FIXED_PATH
    env['TMPDIR'] = run_dir
    env.pop('PYTHONPATH', None)

    unblob = plan['unblob']
    unblob_command = unblob
    tee_path = None
    log_copy = os.path.join(run_dir, 'unblob.log')
    if use_tee and os.path.exists(unblob):
        tee_path = write_tee(os.path.join(run_dir, 'unblob-tee.sh'))
        env['C1_REAL_UNBLOB'] = unblob
        env['C1_LOG_COPY'] = log_copy
        env['REA_UNBLOB_COMMAND'] = tee_path
        unblob_command = tee_path
    else:
        env['REA_UNBLOB_COMMAND'] = unblob
        if use_tee:
            sys.stderr.write('c1-run: no unblob at %s; running without the log tee\n'
                             % unblob)

    started = utc_now()
    t0 = time.monotonic()
    timed_out = False
    try:
        proc = subprocess.run(plan['argv'], cwd=run_dir, env=env,
                              capture_output=True, timeout=timeout)
        rc = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
    except subprocess.TimeoutExpired as e:
        rc = 124
        stdout = e.stdout or b''
        stderr = e.stderr or b''
        timed_out = True
    except OSError as e:
        rc = 127
        stdout = b''
        stderr = str(e).encode('utf-8', 'replace')
    wall = round(time.monotonic() - t0, 3)
    ended = utc_now()

    os.makedirs(outdir, exist_ok=True)

    # In `scratch` mode the produced tree lives in the run dir; copy it
    # verbatim into the evidence directory before snapshotting, so the
    # committed evidence carries the produced bytes either way.
    copy_note = None
    if rea_outdir != outdir:
        if os.path.isdir(rea_outdir):
            try:
                copy_tree_verbatim(rea_outdir, outdir)
                copy_note = ('copied verbatim from the REA output root %s'
                             % rea_outdir)
            except (OSError, shutil.Error) as e:
                copy_note = 'copy failed: %s' % e
        else:
            copy_note = 'REA produced no output root at %s' % rea_outdir

    # The tree REA produced, snapshotted BEFORE this runner's receipts are
    # written, so extract-tree.tsv describes exactly the produced bytes.
    tree_entries = snapshot_tree(outdir, skip=set(RECEIPT_FILES))

    # stdout is copied byte-for-byte: the same bytes become envelope.json and
    # stdout.log, and stdout_sha256 in run.json describes them.
    with open(os.path.join(outdir, 'envelope.json'), 'wb') as fh:
        fh.write(stdout)
    with open(os.path.join(outdir, 'stdout.log'), 'wb') as fh:
        fh.write(stdout)
    with open(os.path.join(outdir, 'stderr.log'), 'wb') as fh:
        fh.write(stderr)

    envelope = None
    parse_error = None
    try:
        envelope = json.loads(stdout.decode('utf-8', 'replace'))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        parse_error = str(e)
    if not isinstance(envelope, dict):
        if parse_error is None:
            parse_error = 'stdout is not a JSON object'
        envelope = None

    data = envelope.get('data') if envelope else None
    receipt_ok = isinstance(data, dict)
    if receipt_ok:
        # the round-42 counter reads after.json as the envelope's `data` object
        write_json(os.path.join(outdir, 'after.json'), data)

    # unblob's own log, copied out of the REA task directory by the tee
    unblob_log = {'path': None, 'sha256': None, 'command_line': None}
    if os.path.isfile(log_copy):
        shutil.copyfile(log_copy, os.path.join(outdir, 'unblob.log'))
        unblob_log = {
            'path': 'unblob.log',
            'sha256': sha256_file(os.path.join(outdir, 'unblob.log')),
            'command_line': extract_command_line(log_copy),
        }

    pins, pin_notes = tool_pins()
    log_tee = None
    if tee_path is not None:
        log_tee = {'path': tee_path, 'sha256': sha256_file(tee_path)}
    env_doc = {
        'schema': SCHEMA_ENV,
        'seat': SEAT,
        'carrier': plan['id'],
        'path': FIXED_PATH,
        'unblob': pins.get('unblob'),
        'sasquatch': pins.get('sasquatch'),
        'sasquatch-v4be': pins.get('sasquatch-v4be'),
        'npx': pins.get('npx'),
        'log_tee': log_tee,
        'unblob_log': unblob_log,
        'notes': pin_notes + ([
            'REA_UNBLOB_COMMAND was a transparent tee generated in the scratch; '
            'it ran the real unblob ($HOME/.local/bin/unblob) with REA\'s '
            'arguments unchanged and copied the --log file out of the REA task '
            'directory. The tee never edits an argument, the input, the output '
            'or the log, and exits with unblob\'s own exit code.',
        ] if tee_path else [
            'no log tee was used: REA deletes the unblob --log file with its '
            'task directory, so the extract command line was not captured.',
        ]),
    }
    write_json(os.path.join(outdir, 'extract-env.json'), env_doc)

    if tree_entries or os.path.isdir(outdir):
        write_tree_tsv(os.path.join(outdir, 'extract-tree.tsv'), tree_entries)

    prov_doc = {
        'schema': SCHEMA_PROV,
        'seat': SEAT,
        'carrier': plan['id'],
        'rea_output_directory': rea_outdir,
        'rea_output_directory_mode': plan['outdir_mode'],
        'evidence_outdir': outdir,
        'evidence_outdir_under_evidence_root': True,
        'evidence_root': evidence_root,
        'round_evidence_segment': 'corpus/evidence/round-49/c1/',
        'produced_tree': {'entries': len(tree_entries),
                          'files': sum(1 for e in tree_entries if e[1] == 'file'),
                          'bytes': sum(e[2] for e in tree_entries
                                       if e[2] is not None),
                          'tsv': 'extract-tree.tsv'},
        'rewritten': False,
        'copied_verbatim': copy_note,
        'note': ('REA 6.5.0 named %r as its output_directory; the published '
                 'tree in this directory is the produced tree, unmodified '
                 '(extract-tree.tsv records its digests).' % rea_outdir),
        'outdir_state_before_run': cleared,
        'rea_outdir_state_before_run': cleared_rea,
    }
    write_json(os.path.join(outdir, 'provenance.json'), prov_doc)

    run_doc = {
        'schema': SCHEMA_RUN,
        'seat': SEAT,
        'carrier': plan['id'],
        'command': command_string(plan, unblob_command),
        'argv': plan['argv'],
        'cwd': run_dir,
        'exit_code': rc,
        'stdout_sha256': sha256_bytes(stdout),
        'stdout_bytes': len(stdout),
        'stderr_sha256': sha256_bytes(stderr),
        'stderr_bytes': len(stderr),
        'wall_s': wall,
        'timed_out': timed_out,
        'started_utc': started,
        'ended_utc': ended,
        'rev_at_run': git_rev(lane),
        'freeze_arg': plan.get('freeze_arg'),
        'evidence_root': evidence_root,
        'outdir': outdir,
        'scratch_root': scratch_root,
        'carrier_fixture': {
            'path': plan['fixture'],
            'resolved_by': plan['fixture_how'],
            'sha256': plan['fixture_sha256'],
            'size': plan['fixture_size'],
            'frozen_pin': plan['fixture_pin'],
            'pin_ok': plan['pin_ok'],
        },
        'rea': {
            'pin': REA_PIN,
            'package_root': None if fake else rea_package_root(),
            'command_override': list(plan['rea_command']) if fake else None,
        },
        'unblob': pins.get('unblob'),
        'unblob_command_env': unblob_command,
        'unblob_log_tee': tee_path,
        'sasquatch': pins.get('sasquatch'),
        'child_path': FIXED_PATH,
        'receipt_written': receipt_ok,
        'envelope_parse_error': parse_error,
        'extract_tree': {
            'entries': len(tree_entries),
            'files': sum(1 for e in tree_entries if e[1] == 'file'),
            'symlinks': sum(1 for e in tree_entries if e[1] == 'symlink'),
            'bytes': sum(e[2] for e in tree_entries if e[2] is not None),
            'tsv': 'extract-tree.tsv',
        },
        'handler': plan['entry'].get('handler'),
        'endian': plan['entry'].get('endian'),
        'output_directory': (data or {}).get('parameters', {}).get(
            'output_directory') if isinstance(data, dict) else None,
    }
    write_json(os.path.join(outdir, 'run.json'), run_doc)

    if not keep_scratch:
        shutil.rmtree(run_dir, ignore_errors=True)

    return run_doc


# ------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(
        prog='c1-run.py',
        description='kaidoku round 49 R49-C1 after-freeze data procedure.')
    ap.add_argument('--lane-root', default=None,
                    help='lane root (default: nearest ancestor with corpus/evidence '
                         'and plans/)')
    ap.add_argument('--carriers', default=None,
                    help='carriers.json (default: <lane>/tools/round-49/carriers.json)')
    ap.add_argument('--evidence-root', default=None,
                    help='evidence root (default: <lane>/corpus/evidence/round-49/c1)')
    ap.add_argument('--scratch', default=None,
                    help='scratch base (default: $HYAKU_SCRATCH or '
                         '/fast/scratch/hyaku; the runner appends /kaidoku-r49)')
    ap.add_argument('--carrier', action='append', default=None,
                    help='run only this carrier id (repeatable)')
    ap.add_argument('--include-exploratory', action='store_true',
                    help='also run carriers.json ids listed under scope.'
                         'exploratory_ids (the claim does not score them)')
    ap.add_argument('--timeout', type=int, default=900,
                    help='per-carrier REA timeout in seconds (default 900)')
    ap.add_argument('--freeze', default=None,
                    help='freeze revision recorded in the receipts')
    ap.add_argument('--dry-run', action='store_true',
                    help='print the commands that would run; write nothing')
    ap.add_argument('--data-run', action='store_true',
                    help='assert that the freeze is in place (required to write '
                         'into the default evidence root)')
    ap.add_argument('--keep-scratch', action='store_true',
                    help='keep the per-carrier scratch directory')
    ap.add_argument('--force', action='store_true',
                    help='replace an existing evidence directory (REA refuses an '
                         'existing output root, so a re-run must replace it)')
    ap.add_argument('--no-unblob-log-tee', action='store_true',
                    help='run unblob directly (no log tee): the extract command '
                         'line is then not captured')
    ap.add_argument('--rea-outdir-mode', choices=('scratch', 'evidence'),
                    default='scratch',
                    help='where REA\'s output_directory points (default scratch = '
                         'this round\'s /kaidoku-r49/ scratch segment, the binding '
                         'the frozen claims text states: the produced tree is '
                         'copied verbatim into the evidence dir and provenance.json '
                         'binds the two; evidence = REA writes into the evidence '
                         'dir itself, so the receipt names that path)')
    ap.add_argument('--fake-rea', default=None,
                    help='DEVELOPMENT ONLY: replace the REA command with this '
                         'argv prefix (a stand-in that prints a synthetic '
                         'envelope). The receipt records the override, and a '
                         'synthetic receipt fails the counter\'s evidence-id and '
                         'rerun-projection bindings.')
    args = ap.parse_args(argv)

    here = os.path.dirname(os.path.abspath(__file__))
    lane = os.path.abspath(args.lane_root) if args.lane_root else lane_root(here)
    if not lane or not os.path.isdir(lane):
        sys.stderr.write('c1-run: lane root not found (pass --lane-root)\n')
        return 2
    carriers_path = args.carriers or os.path.join(lane, DEFAULT_CARRIERS)
    evidence_root = os.path.abspath(
        args.evidence_root or os.path.join(lane, DEFAULT_EVIDENCE))
    default_evidence = os.path.join(lane, DEFAULT_EVIDENCE)
    writing_committed = (os.path.realpath(evidence_root)
                         == os.path.realpath(default_evidence))
    if writing_committed and not args.dry_run \
            and not args.data_run and os.environ.get('KAIDOKU_C1_DATA_RUN') != '1':
        sys.stderr.write(
            'c1-run: refusing to write into the committed evidence root %s.\n'
            '        This procedure runs AFTER the freeze: a pre-freeze receipt\n'
            '        breaks the counter\'s receipt_fresh binding. Run it with\n'
            '          KAIDOKU_C1_DATA_RUN=1 c1-run.sh\n'
            '        or --data-run, or use --dry-run / --evidence-root <other>.\n'
            % default_evidence)
        return 2

    base_scratch = (args.scratch or os.environ.get('HYAKU_SCRATCH')
                    or '/fast/scratch/hyaku')
    scratch_root = os.path.join(base_scratch, ROUND_SEGMENT)
    if not args.dry_run:
        os.makedirs(scratch_root, exist_ok=True)

    try:
        spec, carriers = load_carriers(carriers_path)
    except Unevaluable as e:
        sys.stderr.write('c1-run: %s\n' % e)
        return 2
    if args.carrier:
        wanted = set(args.carrier)
        carriers = [c for c in carriers if c[0] in wanted]
        if not carriers:
            sys.stderr.write('c1-run: no carrier matches %s\n' % ','.join(sorted(wanted)))
            return 2

    # carriers.json may declare which ids are SCORED (`scope.target_ids`) and
    # which are retained exploratory data the claim explicitly does not score
    # (`scope.exploratory_ids`). The data procedure runs the scored set by
    # default: writing receipts for the exploratory carriers would put
    # unscoreable evidence in the receipts directory. `--include-exploratory`
    # opts them in, and the manifest marks them as exploratory either way.
    scope = spec.get('scope') if isinstance(spec, dict) else None
    target_ids = []
    exploratory_ids = []
    if isinstance(scope, dict):
        target_ids = [x for x in (scope.get('target_ids') or [])
                      if isinstance(x, str) and x]
        exploratory_ids = [x for x in (scope.get('exploratory_ids') or [])
                           if isinstance(x, str) and x]
    skipped = []
    if target_ids and not args.carrier:
        all_ids = [c[0] for c in carriers]
        keep = set(target_ids)
        if args.include_exploratory:
            keep |= set(exploratory_ids)
        unknown = sorted(keep - set(all_ids))
        if unknown:
            sys.stderr.write('c1-run: carriers.json scope names ids with no carrier '
                             'entry: %s\n' % ','.join(unknown))
            return 2
        skipped = [x for x in all_ids if x not in keep]
        carriers = [c for c in carriers if c[0] in keep]

    rea_command = args.fake_rea.split() if args.fake_rea else ['npx', '-y', REA_PIN]
    fake = bool(args.fake_rea)
    use_tee = (not args.no_unblob_log_tee
               and os.environ.get('C1_UNBLOB_LOG_TEE', '1') != '0')

    target = spec.get('target') if isinstance(spec, dict) else None
    plans = []
    for cid, entry in carriers:
        try:
            plan = build_plan(lane, evidence_root, cid, entry, scratch_root,
                              rea_command, args.rea_outdir_mode)
        except Unevaluable as e:
            sys.stderr.write('c1-run: %s\n' % e)
            return 2
        plan['freeze_arg'] = args.freeze
        plans.append(plan)

    rev = git_rev(lane)
    if args.dry_run:
        out = {
            'schema': SCHEMA_MANIFEST,
            'mode': 'dry-run',
            'seat': SEAT,
            'lane_root': lane,
            'carriers_file': carriers_path,
            'evidence_root': evidence_root,
            'scratch_root': scratch_root,
            'target': target,
            'rev_at_plan': rev,
            'fixed_path': FIXED_PATH,
            'unblob': unblob_path(),
            'rea_command': rea_command,
            'unblob_log_tee': use_tee,
            'scope': {'target_ids': target_ids,
                      'exploratory_ids': exploratory_ids,
                      'skipped_ids': skipped},
            'manifest_path': os.path.join(evidence_root, 'manifest.json'),
            'carriers': [],
        }
        for plan in plans:
            cmd = command_string(plan, '<tee>' if use_tee else unblob_path())
            produces = os.path.join(plan['outdir'], 'firmware.bin_extract/')
            out['carriers'].append({
                'id': plan['id'],
                'command': cmd,
                'argv': plan['argv'],
                'fixture': plan['fixture'],
                'fixture_sha256': plan['fixture_sha256'],
                'outdir': plan['outdir'],
                'run_dir': plan['run_dir'],
                'produces': produces,
            })
            sys.stdout.write('# carrier %s\n' % plan['id'])
            sys.stdout.write('cd %s && REA_UNBLOB_COMMAND=%s %s\n'
                             % (plan['run_dir'],
                                '<tee>' if use_tee else unblob_path(),
                                ' '.join(plan['argv'])))
            sys.stdout.write('#   REA output_directory %s (must not exist; REA '
                             'creates it)\n' % plan['rea_outdir'])
            if plan['rea_outdir'] != plan['outdir']:
                sys.stdout.write('#   produced tree copied verbatim -> %s\n'
                                 % os.path.join(plan['outdir'], ''))
            sys.stdout.write('#   receipts -> %s{firmware.bin_extract/..., '
                             'envelope.json,after.json,stdout.log,stderr.log,'
                             'unblob.log,extract-env.json,extract-tree.tsv,'
                             'provenance.json,run.json}\n'
                             % os.path.join(plan['outdir'], ''))
        sys.stdout.write('# manifest -> %s\n' % out['manifest_path'])
        sys.stdout.write('# DRY RUN: nothing was written.\n')
        return 0

    manifest = {
        'schema': SCHEMA_MANIFEST,
        'mode': 'data-run',
        'seat': SEAT,
        'claim': 'R49-C1',
        'lane_root': lane,
        'carriers_file': carriers_path,
        'evidence_root': evidence_root,
        'scratch_root': scratch_root,
        'target': target,
        'rev_at_run': rev,
        'freeze': args.freeze,
        'generated_utc': utc_now(),
        'fixed_path': FIXED_PATH,
        'rea_pin': REA_PIN,
        'rea_command': rea_command,
        'unblob_log_tee': use_tee,
        'scope': {'target_ids': target_ids,
                  'exploratory_ids': exploratory_ids,
                  'skipped_ids': skipped},
        'carriers': {},
        'summary': {},
    }
    failures = []
    for plan in plans:
        if not plan['pin_ok']:
            sys.stderr.write(
                'c1-run: carrier %s: fixture %s hashes to %s but the frozen pin '
                'is %s (not running REA on unverified bytes)\n'
                % (plan['id'], plan['fixture'], plan['fixture_sha256'],
                   plan['fixture_pin']))
            manifest['carriers'][plan['id']] = {
                'outdir': os.path.relpath(plan['outdir'], lane),
                'run_json': os.path.relpath(os.path.join(plan['outdir'], 'run.json'), lane),
                'fixture': os.path.relpath(plan['fixture'], lane),
                'fixture_sha256': plan['fixture_sha256'],
                'exit_code': None,
                'stdout_sha256': None,
                'wall_s': None,
                'receipt_written': False,
                'status': 'failed',
                'failure': 'pin mismatch: fixture %s != frozen pin %s'
                           % (plan['fixture_sha256'], plan['fixture_pin']),
            }
            failures.append(plan['id'])
            continue
        sys.stdout.write('# running %s\n' % plan['id'])
        sys.stdout.flush()
        try:
            doc = run_carrier(plan, lane, evidence_root, scratch_root,
                              args.timeout, args.keep_scratch, fake, use_tee,
                              args.force)
        except Unevaluable as e:
            sys.stderr.write('c1-run: %s\n' % e)
            return 2
        ok = doc['exit_code'] == 0 and doc['receipt_written']
        manifest['carriers'][plan['id']] = {
            'outdir': os.path.relpath(plan['outdir'], lane),
            'run_json': os.path.relpath(os.path.join(plan['outdir'], 'run.json'), lane),
            'receipt': os.path.relpath(os.path.join(plan['outdir'], 'after.json'), lane),
            'extract_env': os.path.relpath(
                os.path.join(plan['outdir'], 'extract-env.json'), lane),
            'extract_tree': os.path.relpath(
                os.path.join(plan['outdir'], 'extract-tree.tsv'), lane),
            'fixture': os.path.relpath(plan['fixture'], lane),
            'fixture_sha256': plan['fixture_sha256'],
            'command': doc['command'],
            'exit_code': doc['exit_code'],
            'stdout_sha256': doc['stdout_sha256'],
            'wall_s': doc['wall_s'],
            'receipt_written': doc['receipt_written'],
            'output_directory': doc.get('output_directory'),
            'status': 'ok' if ok else 'failed',
        }
        if not ok:
            failures.append(plan['id'])
        sys.stdout.write('# %s: exit %d, receipt %s\n'
                         % (plan['id'], doc['exit_code'], doc['receipt_written']))
        sys.stdout.flush()

    os.makedirs(evidence_root, exist_ok=True)
    manifest['summary'] = {
        'carriers': len(plans),
        'ok': sum(1 for c in manifest['carriers'].values() if c['status'] == 'ok'),
        'failed': failures,
    }
    write_json(os.path.join(evidence_root, 'manifest.json'), manifest)
    sys.stdout.write('# manifest -> %s\n' % os.path.join(evidence_root, 'manifest.json'))
    if failures:
        sys.stderr.write('c1-run: %d carrier(s) failed: %s\n'
                         % (len(failures), ', '.join(failures)))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
