#!/usr/bin/env python3
"""R42-C1 supplementary bindings (round-42 port of tools/round-41/c1-extra.py at c4a38ea2).

The main counter (tools/round-42/c1-counter.py) scores receipts, reruns, carrier
superblocks and doc presence. This gate adds the three bindings the wave-1 controls
showed the counter does not enforce, ported from round 41:

  oracle_rederived   for every carrier in .ufo/waves/round-42/c1/carriers.json, the
                     oracle tool bytes AT THE FREEZE (tools/round-42/sqfs3-oracle.py,
                     the two-producer `unsquashfs` 4.7.5 + 7-Zip 7z re-derivation) run
                     on the carrier's CARVED bytes reproduce the frozen
                     corpus/evidence/round-42/c1/<id>/{oracle,nonregular}.tsv exactly
                     (as parsed row sets); a trimmed, hand-edited, malformed or
                     duplicated table fails, and so does a table whose path is outside
                     this round's evidence directory (the round-41 CTL-C1-1 relabelling
                     shape). Round-41 read its own layout reader here (`tools/round-41/
                     sqfs-list.py`); round 42 has no lane reader in the chain, so the
                     binding is exactly "the frozen oracle tool re-derives the frozen
                     tables from the frozen bytes". A carrier may not be committed in
                     the lane: round-42 carriers are published third-party images and
                     only their carved bytes live in --carrier-cache.
  sourced_new        the round-42 entry cites an S-id whose corpus/SOURCES.md row is
                     ABSENT at --base and present at --rev with the entry in its
                     used-by cell; a date string cannot satisfy it, nor can an id that
                     already exists at the base (S129 is the highest row at
                     c4a38ea2).
  frontier_content   PROVINCE.md at --rev holds a line starting `Round-42 frontier
                     note` that names `## Round-42 additions to Core`, the round-42
                     entry stem, a supersede verb, the `squashfs_v3` handler family,
                     and what stays Frontier: v1/v2 (both) and v4 Broadcom. Round-41
                     required the round-40 `measured, not promoted` record phrase
                     instead; round 42 supersedes Frontier text, not an honest-stop
                     block, and a note naming only `squashfs_v4` is not a note about
                     the family that moved.

Round-42 changes from the round-41 file
  - constants: carriers `.ufo/waves/round-42/c1/carriers.json`, oracle
    `tools/round-42/sqfs3-oracle.py`, entry stem `2026-10-26-r42-squashfs-v3-core`,
    PROVINCE heading `## Round-42 additions to Core`, note marker
    `Round-42 frontier note`, evidence root `corpus/evidence/round-42/c1/`;
  - carrier bytes come from --carrier-cache only, located by PIN, not by a hardcoded
    file name (tools/round-42/fetch-carrier.py names the cache entry; this gate must
    not depend on that spelling): the fast paths `<pin>.bin`, `<pin>.sqfs`,
    `<id>.bin`, `<id>.sqfs`, `<pin>` are hashed first, then every regular file in the
    cache root, and the first file whose sha256 equals the pin wins;
  - the oracle CLI is discovered once, on the first carrier, from an ordered list of
    argument forms (`IMG --out DIR` first), because the tool is authored in the same
    wave; the accepted form is recorded in the receipt and every attempt with its
    exit and stderr head is kept. A carrier the oracle cannot read is RED (like the
    round-41 reader exit), never unevaluable; only a missing carriers.json or a
    missing oracle tool at the freeze is unevaluable;
  - tables are compared as PARSED row sets (rel, sha256, size) / (rel, kind, detail),
    with format validation (3 fields, 64-hex sha, integer size; duplicate rows red),
    not as raw text lines: the counter parses them too, so a whitespace-only edit is
    not a finding and a malformed row is;
  - the receipt carries `counter_sha256` (closure D4): the sha256 of the counter file
    this process runs, plus `counter_at_rev_sha256` (the same path at --rev, when the
    tool is already integrated) and `oracle_tool_sha256` (the frozen oracle bytes), so
    identity does not rest on a separate diff.

Usage:
  c1-extra.py --root LANE --rev REV --freeze FREEZE --base BASE [--carrier-cache DIR]
              [--json-out F] [--work DIR]
  c1-extra.py --selftest [--work DIR]
  c1-extra.py --oracle-check --oracle FILE --dev-image FILE [--work DIR]
Exit 0 all three true; 1 any false; 2 unevaluable (missing commit, carriers.json,
oracle tool) or bad selftest environment.
Stdlib only; scratch under $HYAKU_SCRATCH/kaidoku-r42 (honours TMPDIR / --work).
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

CARRIERS = '.ufo/waves/round-42/c1/carriers.json'
ORACLE = 'tools/round-42/sqfs3-oracle.py'
ENTRY = 'corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md'
STEM = '2026-10-26-r42-squashfs-v3-core'
HEADING = '## Round-42 additions to Core'
NOTE = 'Round-42 frontier note'
EVIDENCE = 'corpus/evidence/round-42/c1/'
SELF = 'tools/round-42/c1-extra.py'
SCRATCH_SEG = 'kaidoku-r42'
CLAIM = 'R42-C1'

# the frontier note must name the family that moved and what stays behind
FAMILY_RE = re.compile(r'squashfs_v3(?![0-9])')
V1_RE = re.compile(r'(?<![A-Za-z0-9])v1(?![0-9])')
V2_RE = re.compile(r'(?<![A-Za-z0-9])v2(?![0-9])')
V4_RE = re.compile(r'(?<![A-Za-z0-9])v4(?![0-9])')
BROADCOM_RE = re.compile(r'broadcom', re.IGNORECASE)
RESIDUAL_VERB_RE = re.compile(r'\b(?:stays?|staying|remains?|remaining|'
                              r'not[ _-]claimed|outside)\b')
SID_ROW = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
URL_RE = re.compile(r'^https?://')

# ordered CLI forms for tools/round-42/sqfs3-oracle.py (image + output directory)
ORACLE_FORMS = (
    ('img--out', lambda img, out: [img, '--out', out]),
    ('img-out', lambda img, out: [img, out]),
    ('input--out', lambda img, out: ['--input', img, '--out', out]),
    ('image--out', lambda img, out: ['--image', img, '--out', out]),
)
ORACLE_FORM_MAP = dict(ORACLE_FORMS)
CACHE_FAST = ('%(pin)s.bin', '%(pin)s.sqfs', '%(id)s.bin', '%(id)s.sqfs', '%(pin)s')


class Unevaluable(Exception):
    pass


def show(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def self_bytes():
    return open(os.path.abspath(__file__), 'rb').read()


def scratch(work):
    if work:
        os.makedirs(work, exist_ok=True)
        return tempfile.mkdtemp(prefix='c1-extra.', dir=work)
    base = os.environ.get('HYAKU_SCRATCH')
    if not base:
        base = os.path.join(os.environ.get('TMPDIR') or tempfile.gettempdir(), 'hyaku')
    base = os.path.join(base, SCRATCH_SEG)
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        base = None
    return tempfile.mkdtemp(prefix='c1-extra.', dir=base)


# ---------------------------------------------------------------- oracle tables

def tsv_rows(raw, kind):
    """Parse an oracle/non-regular table into a row set.

    oracle:      relpath TAB sha256 TAB size
    nonregular:  relpath TAB kind [TAB detail]  (a two-field row and a third empty
                 field are the same row)
    Raises ValueError on a malformed or duplicated row; callers turn that into red.
    """
    rows, n = set(), 0
    for line in raw.decode('utf-8', 'replace').splitlines():
        if not line.strip():
            continue
        n += 1
        fields = line.split('\t')
        if kind == 'oracle':
            if len(fields) != 3:
                raise ValueError('oracle row has %d fields: %r' % (len(fields), line[:120]))
            rel, digest, size = fields
            if not rel:
                raise ValueError('oracle row has an empty path: %r' % line[:120])
            if not SHA_RE.match(digest):
                raise ValueError('oracle row sha256 is not 64 lowercase hex: %r'
                                 % line[:120])
            if not size.isdigit():
                raise ValueError('oracle row size is not an integer: %r' % line[:120])
            rows.add((rel, digest, int(size)))
        else:
            if len(fields) not in (2, 3):
                raise ValueError('non-regular row has %d fields: %r'
                                 % (len(fields), line[:120]))
            rel, entry_kind = fields[0], fields[1]
            detail = fields[2] if len(fields) == 3 else ''
            if not rel or not entry_kind:
                raise ValueError('non-regular row lacks path or kind: %r' % line[:120])
            rows.add((rel, entry_kind, detail))
    if len(rows) != n:
        raise ValueError('duplicate row(s): %d rows, %d distinct' % (n, len(rows)))
    return rows


def find_tables(out):
    """Locate oracle.tsv/nonregular.tsv in the oracle's output directory (depth <= 2)."""
    a, b = os.path.join(out, 'oracle.tsv'), os.path.join(out, 'nonregular.tsv')
    if os.path.isfile(a) and os.path.isfile(b):
        return a, b
    for dirpath, dirs, names in os.walk(out):
        depth = 0 if dirpath == out else os.path.relpath(dirpath, out).count(os.sep) + 1
        if depth >= 2:
            dirs[:] = []
        if 'oracle.tsv' in names and 'nonregular.tsv' in names:
            return (os.path.join(dirpath, 'oracle.tsv'),
                    os.path.join(dirpath, 'nonregular.tsv'))
    return None, None


def run_oracle(tool, form, img, out, work):
    os.makedirs(out, exist_ok=True)
    p = subprocess.run([sys.executable, '-I', '-B', tool]
                       + ORACLE_FORM_MAP[form](img, out), capture_output=True, cwd=work)
    a, b = find_tables(out)
    return p, a, b


def discover_form(tool, img, work):
    """Find the frozen oracle's CLI on the first carrier; keep every attempt."""
    attempts = []
    for name, argv in ORACLE_FORMS:
        out = tempfile.mkdtemp(prefix='form-' + name + '.', dir=work)
        p, a, b = run_oracle(tool, name, img, out, work)
        attempts.append({
            'form': name,
            'argv': [os.path.basename(tool)] + [x if x not in (img, out) else
                                                ('<img>' if x == img else '<out>')
                                                for x in argv(img, out)],
            'exit': p.returncode,
            'tables': bool(a and b),
            'stderr': [l[:200] for l in
                       p.stderr.decode('utf-8', 'replace').strip().splitlines()[:2]],
        })
        if p.returncode == 0 and a and b:
            return name, out, attempts, p
        shutil.rmtree(out, ignore_errors=True)
    return None, None, attempts, None


def oracle_run_meta(out):
    """Best-effort read of the oracle's own oracle-run.json (two-producer record)."""
    path = os.path.join(out, 'oracle-run.json')
    if not os.path.isfile(path):
        return None
    try:
        doc = json.loads(open(path, 'rb').read())
    except (ValueError, OSError) as e:
        return {'error': str(e)[:120]}
    if not isinstance(doc, dict):
        return {'keys': None}
    meta = {'keys': sorted(doc)[:12]}
    for key in ('cross_check', 'verdict', 'agreement', 'crosscheck'):
        if key in doc:
            meta['cross_check'] = doc[key]
            break
    for key in ('producers', 'tools', 'readers'):
        if key in doc:
            meta['producers'] = doc[key]
            break
    return meta


def cache_candidates(cache, pin, cid):
    seen, out = set(), []
    for pat in CACHE_FAST:
        p = os.path.join(cache, pat % {'pin': pin, 'id': cid or ''})
        if p in seen:
            continue
        seen.add(p)
        if os.path.isfile(p) and not os.path.islink(p):
            out.append(p)
    if os.path.isdir(cache):
        for name in sorted(os.listdir(cache)):
            p = os.path.join(cache, name)
            if p not in seen and os.path.isfile(p) and not os.path.islink(p):
                seen.add(p)
                out.append(p)
    return out


def carrier_bytes(c, cache):
    """Return (bytes, source) for a carrier, resolving cached bytes by PIN."""
    pin = (c.get('sha256') or '').lower()
    if not SHA_RE.match(pin):
        return None, 'carrier pin is not 64 lowercase hex'
    if not cache:
        return None, 'no --carrier-cache given'
    if not os.path.isdir(cache):
        return None, 'carrier cache directory absent'
    for path in cache_candidates(cache, pin, c.get('id')):
        with open(path, 'rb') as fh:
            raw = fh.read()
        if sha256(raw) == pin:
            return raw, 'cache:' + os.path.basename(path)
    return None, 'no file in the carrier cache hashes to the pin'


def compare_tables(frozen_oracle, frozen_nonreg, new_oracle, new_nonreg):
    try:
        fo = tsv_rows(open(frozen_oracle, 'rb').read(), 'oracle')
        fn = tsv_rows(open(frozen_nonreg, 'rb').read(), 'nonregular')
        no = tsv_rows(open(new_oracle, 'rb').read(), 'oracle')
        nn = tsv_rows(open(new_nonreg, 'rb').read(), 'nonregular')
    except (ValueError, OSError) as e:
        return False, {'note': 'table unreadable: %s' % str(e)[:200]}
    detail = {'frozen_oracle_rows': len(fo), 'oracle_rows': len(no),
              'frozen_nonregular_rows': len(fn), 'nonregular_rows': len(nn)}
    if not fo or not no:
        detail['note'] = 'empty oracle table'
        return False, detail
    lost, extra = sorted(fo - no)[:5], sorted(no - fo)[:5]
    nlost, nextra = sorted(fn - nn)[:5], sorted(nn - fn)[:5]
    detail['oracle_missing'] = [list(r) for r in lost]
    detail['oracle_extra'] = [list(r) for r in extra]
    detail['nonregular_missing'] = [list(r) for r in nlost]
    detail['nonregular_extra'] = [list(r) for r in nextra]
    return (not lost and not extra and not nlost and not nextra), detail


def oracle_rederived(root, rev, freeze, cache, work):
    spec_raw = show(root, freeze, CARRIERS)
    oracle_src = show(root, freeze, ORACLE)
    if spec_raw is None or oracle_src is None:
        missing = [p for p, r in ((CARRIERS, spec_raw), (ORACLE, oracle_src)) if r is None]
        raise Unevaluable('absent at freeze: %s' % ', '.join(missing))
    tool = os.path.join(work, 'sqfs3-oracle.py')
    with open(tool, 'wb') as fh:
        fh.write(oracle_src)
    os.chmod(tool, 0o755)
    carriers = json.loads(spec_raw).get('carriers') or []
    detail = {'oracle_tool': ORACLE, 'oracle_tool_sha256': sha256(oracle_src),
              'carrier_count': len(carriers),
              'evidence_root': EVIDENCE}
    if not carriers:
        detail['error'] = 'carriers.json lists no carriers'
        return False, detail
    form, form_out = None, None
    for c in carriers:
        cid = str(c.get('id'))
        d = {}
        detail[cid] = d
        ext = c.get('external') if isinstance(c.get('external'), dict) else {}
        url = (ext.get('url') if ext else None) or c.get('url')
        d['external_url'] = url
        if c.get('path'):
            d['fatal'] = ('carrier has a lane path (%s): round-42 carriers are '
                          'published images, never committed' % c['path'])
            continue
        if not (isinstance(url, str) and URL_RE.match(url)):
            d['fatal'] = 'carrier names no http(s) external.url'
            continue
        for key in ('oracle', 'nonregular'):
            p = c.get(key) or ''
            if not p.startswith(EVIDENCE):
                d['fatal'] = ('%s path %r is outside %s (round-41 relabelling shape)'
                              % (key, p, EVIDENCE))
                break
        if d.get('fatal'):
            continue
        raw, source = carrier_bytes(c, cache)
        d['bytes_source'] = source
        if raw is None:
            d['fatal'] = source
            continue
        d['bytes'] = len(raw)
        img = os.path.join(work, '%s.img' % cid)
        with open(img, 'wb') as fh:
            fh.write(raw)
        if form is None:
            form, form_out, attempts, p = discover_form(tool, img, work)
            detail['form_attempts'] = attempts
            detail['oracle_form'] = form
            if form is None:
                first = attempts[0]
                d['fatal'] = ('oracle produced no tables in any of %d argv forms '
                              '(canonical %s exit %d)' % (len(attempts), first['form'],
                                                          first['exit']))
                d['stderr'] = first['stderr']
                continue
            out = form_out
        else:
            out = os.path.join(work, 'oracle-' + cid)
            p, a, b = run_oracle(tool, form, img, out, work)
        d['oracle_exit'] = p.returncode
        a, b = find_tables(out)
        if p.returncode != 0 or not (a and b):
            d['fatal'] = 'oracle exit %d%s' % (p.returncode,
                                               '' if a and b else ' with no tables')
            d['stderr'] = [l[:200] for l in
                           p.stderr.decode('utf-8', 'replace').strip().splitlines()[:3]]
            continue
        meta = oracle_run_meta(out)
        if meta:
            d['oracle_run'] = meta
        frozen_o = show(root, rev, c['oracle'])
        frozen_n = show(root, rev, c['nonregular'])
        if frozen_o is None or frozen_n is None:
            d['fatal'] = 'frozen oracle/nonregular absent at rev'
            continue
        fo = os.path.join(work, cid + '-frozen-oracle.tsv')
        fn = os.path.join(work, cid + '-frozen-nonregular.tsv')
        with open(fo, 'wb') as fh:
            fh.write(frozen_o)
        with open(fn, 'wb') as fh:
            fh.write(frozen_n)
        ok, cd = compare_tables(fo, fn, a, b)
        d.update(cd)
        d['match'] = ok
        if not ok:
            d['fatal'] = cd.get('note') or 'tables differ'
    good = bool(carriers) and all(v.get('match') is True
                                  for v in detail.values() if isinstance(v, dict))
    return good, detail


# ------------------------------------------------------------- documentation

def sids(raw):
    out = {}
    for line in (raw or b'').decode('utf-8', 'replace').splitlines():
        m = SID_ROW.match(line)
        if m:
            out[m.group(1)] = line
    return out


def sourced_new(root, rev, base):
    entry = show(root, rev, ENTRY)
    if entry is None:
        return False, {'error': 'entry absent'}
    cited = sorted({m.group(1) for line in entry.decode('utf-8', 'replace').splitlines()
                    if line.strip().lower().startswith('source')
                    for m in [SID_RE.search(line)] if m})
    at_base = sids(show(root, base, 'corpus/SOURCES.md'))
    at_rev = sids(show(root, rev, 'corpus/SOURCES.md'))
    new = [s for s in cited if s not in at_base and s in at_rev
           and (ENTRY in at_rev[s] or STEM in at_rev[s])]
    return bool(new), {'cited': cited,
                       'at_base': [s for s in cited if s in at_base],
                       'absent_at_rev': [s for s in cited if s not in at_rev],
                       'new_with_used_by': new}


def note_verdict(line):
    flat = line.replace('*', '').lower()
    v = {'line': line[:240],
         'names_heading': HEADING in line,
         'names_stem': STEM in line,
         'supersedes': 'supersede' in flat,
         'names_v3_family': bool(FAMILY_RE.search(line)),
         'frontier_v1': bool(V1_RE.search(line)),
         'frontier_v2': bool(V2_RE.search(line)),
         'frontier_v4_broadcom': bool(V4_RE.search(line) and BROADCOM_RE.search(line)),
         'residual_verb': bool(RESIDUAL_VERB_RE.search(flat))}
    v['ok'] = all(v[k] for k in ('names_heading', 'names_stem', 'supersedes',
                                 'names_v3_family', 'frontier_v1', 'frontier_v2',
                                 'frontier_v4_broadcom', 'residual_verb'))
    return v


def frontier_content(root, rev):
    prov = show(root, rev, 'PROVINCE.md')
    if prov is None:
        return False, {'error': 'PROVINCE.md absent'}
    near = []
    for line in prov.decode('utf-8', 'replace').splitlines():
        if not line.startswith(NOTE):
            continue
        v = note_verdict(line)
        if v['ok']:
            return True, v
        near.append(v)
    return False, (near[0] if near else {'error': 'no line starting %r' % NOTE})


def measure(root, rev, freeze, base, cache, work=None):
    for r in (rev, freeze, base):
        if subprocess.run(['git', '-C', root, 'cat-file', '-e', f'{r}^{{commit}}'],
                          capture_output=True).returncode:
            raise Unevaluable('not a commit: %s' % r)
    w = scratch(work)
    try:
        o, od = oracle_rederived(root, rev, freeze, cache, w)
    finally:
        shutil.rmtree(w, ignore_errors=True)
    s, sd = sourced_new(root, rev, base)
    f, fd = frontier_content(root, rev)
    at_rev = show(root, rev, SELF)
    mine = sha256(self_bytes())
    pin_ok = at_rev is None or sha256(at_rev) == mine
    res = {'claim': CLAIM, 'revision': rev, 'freeze': freeze, 'base': base,
           'bindings': {'oracle_rederived': o, 'sourced_new': s, 'frontier_content': f},
           'detail': {'oracle_rederived': od, 'sourced_new': sd,
                      'frontier_content': fd},
           'counter_sha256': mine,
           'counter_path': SELF,
           'counter_bytes': len(self_bytes()),
           'counter_at_rev_sha256': None if at_rev is None else sha256(at_rev),
           'counter_matches_rev': None if at_rev is None else sha256(at_rev) == mine,
           'counter_pin_ok': pin_ok,
           'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    # closure D4: a receipt produced by bytes other than the counter frozen at REV is
    # not a receipt of the frozen tool, so it cannot be met (before integration the
    # path is absent and the clause is vacuous)
    res['met'] = o and s and f and pin_ok
    return res


# -------------------------------------------------------------------- selftest

STUB_ORACLE = '''#!/usr/bin/env python3
"""Selftest stub for tools/round-42/sqfs3-oracle.py (offline; NOT the real oracle).

Image format: b"SQF3" + body; a body starting b"BAD!" is a damaged carrier.
Writes the round-41/42 table formats from the image bytes, plus oracle-run.json."""
import hashlib, json, os, sys


def main(argv):
    args = argv[1:]
%(parse)s
    if img is None or out is None:
        sys.stderr.write("usage: sqfs3-oracle.py IMG --out DIR\\n")
        return 2
    data = open(img, "rb").read()
    if data[:4] != b"SQF3":
        sys.stderr.write("unsquashfs: not a squashfs v1-v3 image\\n")
        return 2
    body = data[4:]
    if body[:4] == b"BAD!":
        sys.stderr.write("unsquashfs: unable to read superblock\\n")
        return 3
    os.makedirs(out, exist_ok=True)
    rows = [("etc/version", hashlib.sha256(body).hexdigest(), len(body)),
            ("bin/busybox", hashlib.sha256(b"busybox").hexdigest(), 7)]
    with open(os.path.join(out, "oracle.tsv"), "w") as fh:
        fh.write("".join("%%s\\t%%s\\t%%d\\n" %% r for r in rows))
    nonreg = [("etc", "dir", ""), ("bin", "dir", ""),
              ("bin/sh", "symlink", "../bin/busybox"),
              ("dev/console", "char-device", "5:1")]
    with open(os.path.join(out, "nonregular.tsv"), "w") as fh:
        fh.write("".join("%%s\\t%%s\\t%%s\\n" %% r for r in nonreg))
    with open(os.path.join(out, "oracle-run.json"), "w") as fh:
        json.dump({"producers": [{"name": "unsquashfs", "version": "stub"},
                                 {"name": "7z", "version": "stub"}],
                   "cross_check": "agree", "files": len(rows)}, fh)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
'''

PARSE_FLAG = ('    out = None\n'
              '    if "--out" in args:\n'
              '        i = args.index("--out")\n'
              '        out = args[i + 1]\n'
              '        del args[i:i + 2]\n'
              '    img = args[0] if args else None')
PARSE_POSITIONAL = ('    img = args[0] if args else None\n'
                    '    out = args[1] if len(args) > 1 else None')


def stub_oracle(cli='flag'):
    return STUB_ORACLE % {'parse': PARSE_POSITIONAL if cli == 'positional'
                          else PARSE_FLAG}


GREEN_NOTE = ('# p\n%s\nRound-42 frontier note, 2026-10-26: SquashFS v1-v3 chunks now '
              'extract through the `squashfs_v3` handler family; the Frontier text for '
              'v1/v2 images is superseded for v3 only, and v1/v2 images plus '
              'v4 Broadcom stay Frontier — see %s (`%s`).\n'
              % (HEADING, HEADING, STEM))


class Fixture(object):
    def __init__(self, tmp):
        self.dir = os.path.join(tmp, 'repo')
        os.makedirs(self.dir)
        self.revs = {}
        self.git('init', '-q')

    def git(self, *args):
        return subprocess.run(['git', '-C', self.dir] + list(args), check=True,
                              capture_output=True, text=True).stdout.strip()

    def put(self, rel, data):
        full = os.path.join(self.dir, rel)
        if data is None:
            if os.path.exists(full):
                os.remove(full)
            return
        os.makedirs(os.path.dirname(full) or self.dir, exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())

    def commit(self, name):
        self.git('add', '-A')
        self.git('-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-q', '-m',
                 name, '--allow-empty')
        self.revs[name] = self.git('rev-parse', 'HEAD')
        return self.revs[name]


def make_carriers(ids):
    return {'claim': CLAIM, 'target': len(ids),
            'carriers': [{'id': cid, 'sha256': 'e' * 64, 'kind': 'distribution',
                          'external': {'url': 'https://example.invalid/%s.bin' % cid,
                                       'image_sha256': 'f' * 64,
                                       'carve': {'offset': 0, 'length': 1},
                                       'product': 'selftest %s' % cid},
                          'oracle': EVIDENCE + '%s/oracle.tsv' % cid,
                          'nonregular': EVIDENCE + '%s/nonregular.tsv' % cid}
                         for cid in ids]}


def selftest(work=None):
    parent = work or os.environ.get('TMPDIR') or os.environ.get('HYAKU_SCRATCH')
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='c1-extra-selftest.', dir=parent)
    cases, extra = [], {}
    try:
        fx = Fixture(tmp)
        assert os.path.realpath(fx.git('rev-parse', '--show-toplevel')) == \
            os.path.realpath(fx.dir)
        cache = os.path.join(tmp, 'cache')
        os.makedirs(cache)
        tool = os.path.join(tmp, 'stub.py')
        open(tool, 'w').write(stub_oracle('flag'))

        def oracle_tables(img_path):
            out = tempfile.mkdtemp(prefix='stub-', dir=tmp)
            p = subprocess.run([sys.executable, '-I', '-B', tool, img_path, '--out', out],
                               capture_output=True)
            if p.returncode:
                raise SystemExit('stub oracle failed: %r' % p.stderr)
            return (open(os.path.join(out, 'oracle.tsv'), 'rb').read(),
                    open(os.path.join(out, 'nonregular.tsv'), 'rb').read())

        car_a = b'SQF3' + b'alpha-rootfs' * 40
        car_b = b'SQF3' + b'beta-rootfs' * 25
        img_a, img_b = os.path.join(tmp, 'A.img'), os.path.join(tmp, 'B.img')
        open(img_a, 'wb').write(car_a)
        open(img_b, 'wb').write(car_b)
        pin_a, pin_b = sha256(car_a), sha256(car_b)
        tab_a, tab_b = oracle_tables(img_a), oracle_tables(img_b)
        for pin, raw in ((pin_a, car_a), (pin_b, car_b)):
            open(os.path.join(cache, pin + '.bin'), 'wb').write(raw)

        spec = make_carriers(['A', 'B'])
        for c, pin, length in zip(spec['carriers'], (pin_a, pin_b),
                                  (len(car_a), len(car_b))):
            c['sha256'] = pin
            c['external']['carve']['length'] = length

        fx.put('corpus/SOURCES.md',
               '| id | x |\n|---|---|\n| S001 | old |\n| S129 | highest at base |\n')
        fx.put('PROVINCE.md', '# p\n')
        fx.commit('base')
        fx.put(CARRIERS, json.dumps(spec, indent=1))
        for cid, (o, n) in (('A', tab_a), ('B', tab_b)):
            fx.put(EVIDENCE + cid + '/oracle.tsv', o)
            fx.put(EVIDENCE + cid + '/nonregular.tsv', n)
        fx.commit('carriers-no-oracle')
        fx.put(ORACLE, stub_oracle('flag'))
        fx.commit('freeze')
        fx.put(ORACLE, stub_oracle('positional'))
        fx.commit('freeze-positional')
        fx.put(ORACLE, stub_oracle('flag'))
        fx.put(ENTRY, 'source: S130\n')
        fx.put('corpus/SOURCES.md',
               '| id | x |\n|---|---|\n| S001 | old |\n| S129 | highest at base |\n'
               '| S130 | new %s |\n' % ENTRY)
        fx.put('PROVINCE.md', GREEN_NOTE)
        green = fx.commit('landing')
        base, freeze = fx.revs['base'], fx.revs['freeze']

        def case(name, rev, want, binding=None, fz=None):
            try:
                r = measure(fx.dir, rev, fz or freeze, base, cache, work=tmp)
            except Unevaluable as e:
                cases.append((name, want == 'unevaluable'))
                if want != 'unevaluable':
                    extra[name] = 'unevaluable: %s' % e
                return None
            got = r['met'] if binding is None else r['bindings'][binding]
            ok = got == want
            if not ok:
                extra[name] = json.dumps(r['detail'])[:1200]
            cases.append((name, ok))
            return r

        case('green', green, True)
        r = case('receipt-carries-counter-sha256', green, True)
        s = (r or {}).get('counter_sha256')
        cases.append(('counter_sha256-is-self-hash',
                      isinstance(s, str) and SHA_RE.match(s) is not None
                      and s == sha256(self_bytes())))
        cases.append(('counter_matches_rev-null-before-integration',
                      (r or {}).get('counter_matches_rev') is None))
        case('base-has-nothing', base, False)
        case('oracle-absent-at-freeze', green, 'unevaluable',
             fz=fx.revs['carriers-no-oracle'])
        case('oracle-positional-cli-discovered', green, True,
             fz=fx.revs['freeze-positional'])

        # ---- table tampering (tables are read at REV)
        fx.put(EVIDENCE + 'A/oracle.tsv', b''.join(tab_a[0].splitlines(True)[:-1]))
        case('trimmed-oracle', fx.commit('trim oracle'), False, 'oracle_rederived')
        rows = tab_a[0].decode().splitlines()
        rel, digest, size = rows[0].split('\t')
        rows[0] = '\t'.join((rel, ('0' if digest[0] != '0' else '1') + digest[1:], size))
        fx.put(EVIDENCE + 'A/oracle.tsv', '\n'.join(rows) + '\n')
        case('edited-oracle-same-count', fx.commit('oracle sha edited'),
             False, 'oracle_rederived')
        fx.put(EVIDENCE + 'A/oracle.tsv', tab_a[0])
        fx.put(EVIDENCE + 'A/nonregular.tsv',
               tab_a[1] + b'fabricated/link\tsymlink\telsewhere\n')
        case('extra-nonregular-row', fx.commit('fabricated non-regular row'),
             False, 'oracle_rederived')
        # an empty third field and a two-field row are the same row; a dropped
        # non-empty detail is not
        two_field = b''.join((b'\t'.join(line.split(b'\t')[:2]) if
                              line.split(b'\t')[2:] == [b''] else line) + b'\n'
                             for line in tab_a[1].splitlines())
        fx.put(EVIDENCE + 'A/nonregular.tsv', two_field)
        case('empty-detail-two-field-row-parse-equal', fx.commit('two-field rows'),
             True, 'oracle_rederived')
        fx.put(EVIDENCE + 'A/nonregular.tsv', tab_a[1])
        fx.put(EVIDENCE + 'A/oracle.tsv', tab_a[0].replace(b'\t', b'  ', 1))
        case('oracle-row-wrong-field-count', fx.commit('space-separated oracle row'),
             False, 'oracle_rederived')
        fx.put(EVIDENCE + 'A/oracle.tsv', tab_a[0] + tab_a[0].splitlines(True)[0])
        case('duplicate-oracle-row', fx.commit('duplicated oracle row'),
             False, 'oracle_rederived')
        fx.put(EVIDENCE + 'A/oracle.tsv', tab_a[0])
        fx.put(EVIDENCE + 'A/nonregular.tsv',
               b''.join(b'\t'.join(line.split(b'\t')[:2]) + b'\n'
                        for line in tab_a[1].splitlines()))
        case('nonregular-detail-dropped-is-red',
             fx.commit('details dropped'), False, 'oracle_rederived')
        fx.put(EVIDENCE + 'A/nonregular.tsv', tab_a[1])
        fx.put(EVIDENCE + 'B/oracle.tsv', tab_a[0])
        case('table-from-the-other-carrier', fx.commit('B carries A table'),
             False, 'oracle_rederived')
        fx.put(EVIDENCE + 'B/oracle.tsv', tab_b[0])
        fx.commit('tables restored')

        # ---- carrier/spec shape (carriers.json is read at FREEZE)
        bad = make_carriers(['A'])
        bad['carriers'][0]['sha256'] = pin_a
        bad['carriers'][0]['external']['carve']['length'] = len(car_a)
        bad['carriers'][0]['oracle'] = 'corpus/evidence/round-41/c1/A/oracle.tsv'
        fx.put(CARRIERS, json.dumps(bad, indent=1))
        c = fx.commit('relabelled round-41 path')
        case('oracle-outside-round-42-evidence', c, False, 'oracle_rederived', fz=c)
        bad['carriers'][0]['oracle'] = EVIDENCE + 'A/oracle.tsv'
        bad['carriers'][0]['path'] = 'corpus/evidence/round-42/c1/A/carrier.sqsh'
        fx.put(CARRIERS, json.dumps(bad, indent=1))
        c = fx.commit('lane path carrier')
        case('carrier-committed-in-lane', c, False, 'oracle_rederived', fz=c)
        del bad['carriers'][0]['path']
        bad['carriers'][0].pop('external')
        fx.put(CARRIERS, json.dumps(bad, indent=1))
        c = fx.commit('no external block')
        case('carrier-without-external-url', c, False, 'oracle_rederived', fz=c)
        fx.put(CARRIERS, json.dumps(spec, indent=1))
        fx.commit('spec restored')

        # ---- cache resolution by pin
        saved = open(os.path.join(cache, pin_a + '.bin'), 'rb').read()
        open(os.path.join(cache, pin_a + '.bin'), 'wb').write(b'SQF3' + b'gamma' * 30)
        case('external-carrier-pin-mismatch', green, False, 'oracle_rederived')
        os.remove(os.path.join(cache, pin_a + '.bin'))
        case('external-carrier-missing-cache', green, False, 'oracle_rederived')
        open(os.path.join(cache, 'arbitrary-name.bin'), 'wb').write(saved)
        case('cache-entry-named-by-hand', green, True)
        os.remove(os.path.join(cache, 'arbitrary-name.bin'))
        open(os.path.join(cache, pin_a + '.bin'), 'wb').write(saved)

        # ---- oracle behaviour on the carrier bytes
        spec2 = json.loads(json.dumps(spec))
        junk = b'NOTASQSH' + b'x' * 64
        open(os.path.join(cache, pin_b + '.bin'), 'wb').write(junk)
        spec2['carriers'][1]['sha256'] = sha256(junk)
        fx.put(CARRIERS, json.dumps(spec2, indent=1))
        c = fx.commit('carrier bytes replaced by a non-image')
        case('oracle-cannot-read-carrier', c, False, 'oracle_rederived', fz=c)
        damaged = b'SQF3' + b'BAD!' + b'junk'
        open(os.path.join(cache, pin_b + '.bin'), 'wb').write(damaged)
        spec2['carriers'][1]['sha256'] = sha256(damaged)
        fx.put(CARRIERS, json.dumps(spec2, indent=1))
        c = fx.commit('damaged carrier body')
        case('oracle-extractor-failure-exit3', c, False, 'oracle_rederived', fz=c)
        open(os.path.join(cache, pin_b + '.bin'), 'wb').write(car_b)
        fx.put(CARRIERS, json.dumps(spec, indent=1))
        fx.commit('carriers restored')

        # ---- SOURCES binding
        fx.put(ENTRY, 'source: S001\n')
        fx.put('corpus/SOURCES.md',
               '| id | x |\n|---|---|\n| S001 | old %s |\n| S129 | highest at base |\n'
               '| S130 | new %s |\n' % (ENTRY, ENTRY))
        case('old-sid-with-used-by', fx.commit('old id re-used'),
             False, 'sourced_new')
        fx.put(ENTRY, 'source: S129\n')
        case('base-sid-s129-with-used-by', fx.commit('base-highest sid reused'),
             False, 'sourced_new')
        fx.put(ENTRY, 'source: S130\n')
        fx.put('corpus/SOURCES.md',
               '| id | x |\n|---|---|\n| S001 | old |\n| S129 | highest at base |\n'
               '| S130 | new no use |\n')
        case('new-sid-no-used-by', fx.commit('new id without used-by'),
             False, 'sourced_new')
        fx.put('corpus/SOURCES.md',
               '| id | x |\n|---|---|\n| S001 | old |\n| S129 | highest at base |\n'
               '| S130 | new %s |\n' % STEM)
        case('new-sid-used-by-stem', fx.commit('used-by names the stem'),
             True, 'sourced_new')
        fx.put(ENTRY, 'source: S1120\n')
        case('sid-adjacent-digits-are-not-a-row', fx.commit('S1120 is not S112'),
             False, 'sourced_new')
        fx.put(ENTRY, 'source: S130\n')
        fx.commit('entry restored')

        # ---- frontier note
        notes = {
            'presence-only-frontier-note':
                '# p\n%s\nRound-42 frontier note: see %s, %s; v1/v2 and v4 Broadcom '
                'stay Frontier.\n' % (HEADING, HEADING, STEM),
            'round-41-note-names-r42-heading':
                '# p\nRound-41 frontier note: `squashfs_v3` is Core, v1/v2 and v4 '
                'Broadcom stay Frontier; see %s, %s (supersedes).\n'
                % (HEADING, STEM),
            'note-miscases-heading':
                '# p\nRound-42 frontier note: `squashfs_v3` supersedes; v1/v2 and '
                'v4 Broadcom stay Frontier; see ## round-42 additions to core, %s.\n'
                % STEM,
            'note-names-v4-only':
                '# p\nRound-42 frontier note: `squashfs_v4` supersedes the frontier '
                'text; v1/v2 and v4 Broadcom stay Frontier — see %s, %s.\n'
                % (HEADING, STEM),
            'note-omits-v1v2-residual':
                '# p\nRound-42 frontier note: the `squashfs_v3` family supersedes the '
                'frontier text; v4 Broadcom stays Frontier — see %s, %s.\n'
                % (HEADING, STEM),
            'note-omits-v4-broadcom-residual':
                '# p\nRound-42 frontier note: the `squashfs_v3` family supersedes the '
                'frontier text; v1/v2 stay Frontier — see %s, %s.\n'
                % (HEADING, STEM),
            'note-without-supersede-verb':
                '# p\nRound-42 frontier note: `squashfs_v3`, %s, %s; v1/v2 and '
                'v4 Broadcom stay Frontier.\n' % (HEADING, STEM),
            'note-names-squashfs_v30':
                '# p\nRound-42 frontier note: `squashfs_v30` is Core; v1/v2 and '
                'v4 Broadcom stay Frontier; supersedes %s, %s.\n' % (HEADING, STEM),
        }
        for name, text in notes.items():
            fx.put('PROVINCE.md', text)
            case(name, fx.commit(name), False, 'frontier_content')
        fx.put('PROVINCE.md', GREEN_NOTE)
        case('green-after-restore', fx.commit('green note restored'), True)

        # ---- receipt identity (closure D4): the frozen counter's own bytes
        fx.put(SELF, self_bytes())
        case('counter-installed-at-rev-matches', fx.commit('counter installed'),
             True)
        r = measure(fx.dir, fx.revs['counter installed'], freeze, base, cache, work=tmp)
        cases.append(('counter_matches_rev-true-when-installed',
                      r.get('counter_matches_rev') is True and r.get('met') is True))
        fx.put(SELF, self_bytes() + b'\n# drift\n')
        r = measure(fx.dir, fx.commit('counter drifted'), freeze, base, cache, work=tmp)
        cases.append(('counter-drift-at-rev-is-not-met',
                      r.get('counter_matches_rev') is False
                      and r.get('counter_pin_ok') is False
                      and r.get('met') is False
                      and all(r['bindings'].values())))
        fx.put(SELF, None)
        fx.commit('counter removed')

        # ---- unevaluable
        try:
            measure(fx.dir, 'deadbeef', freeze, base, cache, work=tmp)
            cases.append(('bad-rev-unevaluable', False))
        except Unevaluable:
            cases.append(('bad-rev-unevaluable', True))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, ok in cases:
        print('%s\t%s' % ('PASS' if ok else 'FAIL', name))
    for name, why in extra.items():
        print('DETAIL\t%s\t%s' % (name, why))
    p = sum(1 for _, ok in cases if ok)
    print('SELFTEST cases=%d pass=%d fail=%d' % (len(cases), p, len(cases) - p))
    return 0 if p == len(cases) else 1


# --------------------------------------------------------------- oracle check

def oracle_check(oracle, dev_image, work=None):
    """End-to-end with the REAL frozen oracle on a development image.

    Builds a fixture lane whose freeze holds tools/round-42/sqfs3-oracle.py (the given
    file) and one external carrier whose cached bytes are the development image, with
    tables produced by that oracle. Asserts green, then flips one frozen oracle sha256
    and asserts the only false binding is oracle_rederived."""
    parent = work or os.environ.get('TMPDIR') or os.environ.get('HYAKU_SCRATCH')
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='c1-extra-oracle-check.', dir=parent)
    try:
        fx = Fixture(tmp)
        assert os.path.realpath(fx.git('rev-parse', '--show-toplevel')) == \
            os.path.realpath(fx.dir)
        tool_src = open(oracle, 'rb').read()
        image = open(dev_image, 'rb').read()
        pin = sha256(image)
        cache = os.path.join(tmp, 'cache')
        os.makedirs(cache)
        open(os.path.join(cache, pin + '.bin'), 'wb').write(image)
        tool = os.path.join(tmp, 'sqfs3-oracle.py')
        open(tool, 'wb').write(tool_src)
        form, out, attempts, _p = discover_form(tool, dev_image, tmp)
        result = {'oracle': os.path.abspath(oracle), 'oracle_sha256': sha256(tool_src),
                  'dev_image': os.path.abspath(dev_image),
                  'dev_image_sha256': pin, 'dev_image_bytes': len(image),
                  'oracle_form': form, 'form_attempts': attempts}
        if form is None:
            result.update({'verdict': 'FAILED', 'reason': 'no argv form produced tables'})
            print(json.dumps(result, indent=1, sort_keys=True))
            return 1
        result['oracle_run'] = oracle_run_meta(out)
        tab_o = open(os.path.join(out, 'oracle.tsv'), 'rb').read()
        tab_n = open(os.path.join(out, 'nonregular.tsv'), 'rb').read()
        result['rows'] = {'oracle': len(tsv_rows(tab_o, 'oracle')),
                          'nonregular': len(tsv_rows(tab_n, 'nonregular')),
                          'bytes': {'oracle': len(tab_o), 'nonregular': len(tab_n)}}
        spec = make_carriers(['DEV'])
        spec['carriers'][0]['sha256'] = pin
        spec['carriers'][0]['external']['carve']['length'] = len(image)
        fx.put('corpus/SOURCES.md',
               '| id | x |\n|---|---|\n| S129 | highest at base |\n')
        fx.put('PROVINCE.md', '# p\n')
        fx.commit('base')
        fx.put(CARRIERS, json.dumps(spec, indent=1))
        fx.put(EVIDENCE + 'DEV/oracle.tsv', tab_o)
        fx.put(EVIDENCE + 'DEV/nonregular.tsv', tab_n)
        fx.put(ORACLE, tool_src)
        fx.commit('freeze')
        fx.put(ENTRY, 'source: S130\n')
        fx.put('corpus/SOURCES.md',
               '| id | x |\n|---|---|\n| S129 | highest at base |\n| S130 | new %s |\n'
               % ENTRY)
        fx.put('PROVINCE.md', GREEN_NOTE)
        green = fx.commit('landing')
        base, freeze = fx.revs['base'], fx.revs['freeze']
        r = measure(fx.dir, green, freeze, base, cache, work=tmp)
        result['green'] = {'met': r['met'], 'bindings': r['bindings'],
                           'detail': r['detail']['oracle_rederived']}
        rows = tab_o.decode().splitlines()
        rel, digest, size = rows[0].split('\t')
        rows[0] = '\t'.join((rel, ('0' if digest[0] != '0' else '1') + digest[1:], size))
        fx.put(EVIDENCE + 'DEV/oracle.tsv', '\n'.join(rows) + '\n')
        red = fx.commit('oracle sha flipped')
        r2 = measure(fx.dir, red, freeze, base, cache, work=tmp)
        result['flipped_row'] = {'met': r2['met'], 'bindings': r2['bindings'],
                                 'note': r2['detail']['oracle_rederived'].get('DEV', {})}
        ok = (r['met'] is True
              and r2['bindings']['oracle_rederived'] is False
              and r2['bindings']['sourced_new'] is True
              and r2['bindings']['frontier_content'] is True
              and r2['met'] is False)
        result['verdict'] = 'ok' if ok else 'FAILED'
        print(json.dumps(result, indent=1, sort_keys=True))
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    for k in ('--root', '--rev', '--freeze', '--base', '--carrier-cache', '--json-out',
              '--work', '--oracle', '--dev-image'):
        ap.add_argument(k)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--oracle-check', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.work)
    if a.oracle_check:
        if not (a.oracle and a.dev_image):
            print('usage: --oracle-check needs --oracle FILE --dev-image FILE',
                  file=sys.stderr)
            return 2
        return oracle_check(a.oracle, a.dev_image, a.work)
    if not (a.root and a.rev and a.freeze and a.base):
        print('usage: --root --rev --freeze --base required', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze, a.base, a.carrier_cache, a.work)
        res['exit_code'] = 0 if res['met'] else 1
    except Unevaluable as e:
        res = {'claim': CLAIM, 'unevaluable': str(e), 'exit_code': 2,
               'counter_sha256': sha256(self_bytes()), 'counter_path': SELF,
               'counter_bytes': len(self_bytes()),
               'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    res['argv'] = sys.argv
    text = json.dumps(res, indent=1, sort_keys=True)
    print(text)
    if a.json_out:
        with open(a.json_out, 'w') as fh:
            fh.write(text + '\n')
    return res['exit_code']


if __name__ == '__main__':
    sys.exit(main())
