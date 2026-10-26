#!/usr/bin/env python3
"""Check the R41-C1 landing drafts against the round-41 gate's token requirements.

Why this exists: the round-41 counter and its supplementary gate read PROVINCE.md, the knowledge
entry, corpus/SOURCES.md and corpus/README.md by exact string, and a drafts wave that lands text
which misses one token costs a freeze cycle. This script mirrors those readings on the DRAFT files
before the L1 copies them, so the failure is found on a draft, not at a score.

Checks (each mirrors a specific binding of the in-wave gate ports):

  entry_present     the entry draft exists and is not empty
  entry_sources     every `source:` line names at least one S-id
  sourced_new       one cited S-id is a NEW row (absent from --base-sources when given) opened
                    2026-10-26 whose used-by cell names the entry stem — c1-extra.py sourced_new
  province_section  PROVINCE draft has the exact heading line — c1-counter.py province_core_section
  province_row      a row inside that section: first cell names `squashfs_v4_be`, the line matches
                    AVM[ _-]layout and contains the entry path — c1-counter.py province_core_row
  frontier_note     exactly one line starts `Round-41 frontier note` and that line names the
                    heading, the stem, a supersede verb and `measured, not promoted` —
                    c1-extra.py note_verdict
  coverage_row      a table row containing the stem appears in the `## Coverage map` part of the
                    README draft — c1-counter.py coverage_map_row
  fill_tokens       every `{FILL:…}` is closed, non-empty and listed in fill-ledger.tsv
  sources_cells     every drafted S-row has exactly 11 cells, opened 2026-10-26, used-by naming
                    the entry stem — c1-counter.py cells()/sourced
  row_width         the province row has 4 cells and the coverage row 3, so a `|` inside a cell is
                    caught before it shifts a table

Usage:
  check-draft.py [--dir DIR] [--base-sources PATH] [--work DIR] [--json-out F] [--selftest]
Exit 0 all checks green (or every selftest mutation killed), 1 a check failed, 2 unusable input.
Nothing is written outside --work / --json-out; stdlib only.
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile

ENTRY = 'entry-corpus-knowledge-2026-10-26-r41-avm-be-squashfs-core.md'
PROVINCE = 'province-round41-additions.md'
README = 'readme-r41-rows.md'
SOURCES = 'sources-r41-rows.md'
LEDGER = 'fill-ledger.tsv'

ENTRY_PATH = 'corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md'
STEM = '2026-10-26-r41-avm-be-squashfs-core'
HEADING = '## Round-41 additions to Core'
MARK = 'Round-41 frontier note'
HANDLER = 'squashfs_v4_be'
OPENED = '2026-10-26'
AVM_RE = re.compile(r'AVM[ _-]layout', re.IGNORECASE)
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
R40_RECORD = re.compile(r'measured[,\s-]+not[,\s-]+promoted')
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
SID_ROW = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
FILL_RE = re.compile(r'\{FILL:([^}]*)\}')


def read(path):
    with open(path, 'rb') as f:
        return f.read().decode('utf-8', 'replace')


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def section(lines, heading):
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith('## '):
            break
        out.append(line)
    return out


def note_verdict(line):
    flat = line.replace('*', '').lower()
    v = {'names_heading': HEADING in line,
         'names_stem': STEM in line,
         'supersedes': 'supersede' in flat,
         'names_r40_record': bool(R40_RECORD.search(flat))}
    v['ok'] = all(v[k] for k in ('names_heading', 'names_stem', 'supersedes', 'names_r40_record'))
    return v


def base_sids(path):
    if not path or not os.path.exists(path):
        return set()
    return {m.group(1) for l in read(path).splitlines() for m in [SID_ROW.match(l)] if m}


def rows_by_id(text):
    out = {}
    for l in text.splitlines():
        m = SID_ROW.match(l)
        if m:
            out[m.group(1)] = l
    return out


def check(d):
    paths = {k: os.path.join(d, v) for k, v in
             (('entry', ENTRY), ('province', PROVINCE), ('readme', README),
              ('sources', SOURCES), ('ledger', LEDGER))}
    res, detail = {}, {}
    missing = [k for k, p in paths.items() if not os.path.exists(p)]
    if missing:
        return False, {'missing_files': missing}

    entry = read(paths['entry'])
    prov = read(paths['province'])
    readme = read(paths['readme'])
    src = read(paths['sources'])
    ledger = read(paths['ledger'])

    # entry_present
    res['entry_present'] = bool(entry.strip())
    detail['entry_present'] = {'bytes': len(entry)}

    # entry_sources + sourced_new
    cited = sorted({s for l in entry.splitlines() if l.lower().startswith('source')
                    for s in SID_RE.findall(l)})
    res['entry_sources'] = bool(cited)
    detail['entry_sources'] = {'cited': cited}
    base = base_sids(BASE)
    rows = rows_by_id(src)
    new_ok = []
    for s in cited:
        if s not in rows:
            continue
        c = cells(rows[s])
        if len(c) != 11:
            detail.setdefault('sources_cells_bad', []).append((s, len(c)))
            continue
        if c[8] == OPENED and (ENTRY_PATH in c[10] or STEM in c[10]) and s not in base:
            new_ok.append(s)
    res['sourced_new'] = bool(new_ok)
    detail['sourced_new'] = {'new_with_used_by': new_ok,
                             'cited_but_at_base': [s for s in cited if s in base]}

    # province_section / province_row / row_width
    plines = prov.splitlines()
    sec = section(plines, HEADING)
    res['province_section'] = sec is not None
    detail['province_section'] = {'heading': HEADING}
    hit, rows_seen = None, []
    for r in (sec or []):
        if not r.lstrip().startswith('|'):
            continue
        c = cells(r)
        rows_seen.append(c[0] if c else '')
        if HANDLER_RE.search(c[0]) and AVM_RE.search(r) and ENTRY_PATH in r:
            hit = r
            break
    res['province_row'] = hit is not None
    detail['province_row'] = {'rows_seen': rows_seen,
                              'row_cells': len(cells(hit)) if hit else None}
    res['row_width'] = bool(hit) and len(cells(hit)) == 4 and len(cells(
        next((r for r in readme.splitlines() if r.lstrip().startswith('|') and STEM in r), ''))) == 3

    # frontier_note
    notes = [l for l in plines if l.startswith(MARK)]
    verdicts = [note_verdict(l) for l in notes]
    res['frontier_note'] = len(notes) == 1 and verdicts[0]['ok']
    detail['frontier_note'] = {'count': len(notes), 'verdicts': verdicts}

    # coverage_row
    head = 'EDIT 2'
    cov = [l for l in readme.splitlines()
           if l.lstrip().startswith('|') and STEM in l and l]  # any table row naming the stem
    # the coverage row must be the one before the knowledge-index edit marker
    idx = next((i for i, l in enumerate(readme.splitlines()) if head in l), len(readme.splitlines()))
    cov_rows = [l for l in readme.splitlines()[:idx] if l.lstrip().startswith('|') and STEM in l]
    res['coverage_row'] = len(cov_rows) == 1
    detail['coverage_row'] = {'rows_before_knowledge_edit': len(cov_rows), 'any': len(cov)}

    # fill_tokens
    tokens = []
    for name, text in (('entry', entry), ('province', prov), ('readme', readme), ('sources', src)):
        for m in FILL_RE.finditer(text):
            tokens.append(m.group(1).strip())
    opens = sum(t.count('{FILL:') for t in (entry, prov, readme, src))
    bad = [t for t in tokens if not t]
    led = {l.split('\t')[0].strip() for l in ledger.splitlines() if l.strip()}
    unlisted = []
    for t in tokens:
        key = t.split('—')[0].split(' - ')[0].strip()
        if not any(key in x or x in t for x in led):
            unlisted.append(t)
    res['fill_tokens'] = opens == len(tokens) and not bad and not unlisted
    detail['fill_tokens'] = {'count': len(tokens), 'unclosed': opens - len(tokens),
                             'empty': bad, 'unlisted': unlisted}

    # sources_cells
    bad_rows = []
    for sid, l in rows.items():
        c = cells(l)
        if len(c) != 11 or c[8] != OPENED or not (ENTRY_PATH in c[10] or STEM in c[10]):
            bad_rows.append((sid, len(c), c[8] if len(c) > 8 else None))
    res['sources_cells'] = not bad_rows
    detail['sources_cells'] = {'bad': bad_rows, 'rows': sorted(rows)}

    return all(res.values()), {'checks': res, 'detail': detail}


def selftest(work):
    """Every mutation must flip exactly its intended check."""
    d = os.path.join(work, 'draft')
    os.makedirs(d, exist_ok=True)
    for f in (ENTRY, PROVINCE, README, SOURCES, LEDGER):
        shutil.copyfile(os.path.join(HERE, f), os.path.join(d, f))
    ok, det = check(d)
    cases = [('baseline green', ok)]
    if not ok:
        return False, {'baseline': det}

    def mutate(fname, old, new, want):
        p = os.path.join(d, fname)
        orig = read(p)
        assert old in orig, (fname, old)
        with open(p, 'w') as fh:
            fh.write(orig.replace(old, new, 1))
        good, dd = check(d)
        killed = (not good) and dd['checks'].get(want) is False
        with open(p, 'w') as fh:
            fh.write(orig)
        cases.append(('%s -> %s false' % (fname, want), killed))

    def mutate2(fname, pairs, want):
        p = os.path.join(d, fname)
        orig = read(p)
        new = orig
        for old, rep in pairs:
            assert old in new, (fname, old)
            new = new.replace(old, rep, 1)
        with open(p, 'w') as fh:
            fh.write(new)
        good, dd = check(d)
        killed = (not good) and dd['checks'].get(want) is False
        with open(p, 'w') as fh:
            fh.write(orig)
        cases.append(('%s x%d -> %s false' % (fname, len(pairs), want), killed))

    mutate(PROVINCE, HEADING, '## round-41 additions to core', 'province_section')
    mutate(PROVINCE, '(`' + HANDLER + '`) |', '(`squashfs_v4_le`) |', 'province_row')
    mutate2(PROVINCE, [('`## Round-40 measured, not promoted (R40-C1 honest stop)` above is superseded',
                        '`## Round-40 record` above is superseded'),
                       ('its `measured, not promoted` status', 'its status')], 'frontier_note')
    mutate(PROVINCE, 'by `## Round-41 additions to Core` (`' + STEM + '`)',
           'by `## Round-41 additions to Core`', 'frontier_note')
    mutate(SOURCES, 'corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md |', 'corpus/lessons/round-41.md |', 'sourced_new')
    mutate(README, '`' + STEM + '` | **Core**', '`2026-10-26-r41-avm-be-other` | **Core**',
           'coverage_row')
    mutate(ENTRY, '{FILL:V3 chunk = one squashfs_v4_be, not failed}', '{FILL:}', 'fill_tokens')
    bad = [c for c, k in cases if not k]
    return not bad, {'cases': cases, 'failed': bad}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default=HERE)
    ap.add_argument('--base-sources')
    ap.add_argument('--work')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    res = {'dir': a.dir}
    if a.selftest:
        w = a.work or tempfile.mkdtemp(prefix='check-draft.', dir=scratch())
        try:
            ok, det = selftest(w)
        finally:
            if not a.work:
                shutil.rmtree(w, ignore_errors=True)
        res.update(selftest=ok, detail=det)
        code = 0 if ok else 1
    else:
        ok, det = check(a.dir)
        res.update(met=ok, **det)
        code = 0 if ok else 1
    out = json.dumps(res, indent=1, sort_keys=True)
    print(out)
    if a.json_out:
        with open(a.json_out, 'w') as f:
            f.write(out + '\n')
    return code


def scratch():
    base = os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')
    p = os.path.join(base, 'kaidoku-r41')
    os.makedirs(p, exist_ok=True)
    return p


HERE = os.path.dirname(os.path.abspath(__file__))
BASE = None

if __name__ == '__main__':
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('--base-sources')
    pre, _ = ap.parse_known_args()
    BASE = pre.base_sources
    sys.exit(main())
