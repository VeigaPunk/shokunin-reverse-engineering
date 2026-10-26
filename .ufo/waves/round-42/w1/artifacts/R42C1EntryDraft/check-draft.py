#!/usr/bin/env python3
"""R42-C1 landing-document checker (round 42, seat R42C1EntryDraft).

Re-implements the round-42 shape of the round-41 C1 gate's text matchers and applies them to the
draft documents in --dir, on SYNTHETIC PROVINCE.md / corpus/README.md built from the base commit plus
the draft fragments. It does not touch the lane, does not need a freeze, and never runs REA.

Bindings checked (mirroring tools/round-41/c1-counter.py :1685-1726 and c1-extra.py note_verdict):
  province_core_section  PROVINCE.md has the exact `## Round-42 additions to Core` line
  province_core_row      a row in that section whose FIRST cell carries a bare `squashfs_v3` token,
                         whose line carries a SquashFS-v3 format token, and which names the entry path
  frontier_note          ONE physical line carries `Round-42 frontier note`, the entry stem, a
                         Supersede verb, a SquashFS-v3 format token and the superseded phrase
  entry_present          the entry draft exists and is non-trivial
  entry_source_ids       the entry's `source:` lines cite at least one S-id
  sourced_new            at least one cited S-id is absent at --base and present in the SOURCES draft
                         with opened 2026-10-26 and the entry in used-by
  coverage_map_row       a `## Coverage map` row of the synthetic README maps the entry stem
  sources_rows_valid     every drafted row has 11 cells, opened 2026-10-26, entry in used-by
  fill_tokens_closed     no empty `<<L1:>>`, every token has a ledger row, every ledger row a token

Usage: check-draft.py --dir ARTIFACTS --lane LANE [--base REV] [--work DIR] [--json-out F]
       check-draft.py --selftest
Exit 0 all true; 1 any false; 2 unevaluable (missing base blob, missing draft, bad selftest env).
Stdlib only; scratch under $TMPDIR (or --work).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

ENTRY = 'corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md'
STEM = '2026-10-26-r42-squashfs-v3-core'
CORE_HEADING = '## Round-42 additions to Core'
FRONTIER_MARK = 'Round-42 frontier note'
HANDLER = 'squashfs_v3'
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
# the round-41 port gated the row and the note on one case-insensitive FORMAT regex (its analogue was
# `AVM[ _-]layout`); the round-42 spelling is unknown, so the draft must satisfy at least three of the
# plausible spellings in BOTH the row and the note.
FORMAT_PATTERNS = (r'little-endian SquashFS v3', r'SquashFS v3', r'v3 family',
                   r'SquashFS version 3', r'squashfs_v3 family')
FORMAT_MIN = 3


def format_hits(text):
    return sorted({p for p in FORMAT_PATTERNS if re.search(p, text)})
SUPERSEDED_PHRASE = 'coverage claim only'
OPENED = '2026-10-26'
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
TOKEN_RE = re.compile(r'<<L1:[^>]*>>')

PROVINCE_DRAFT = 'province-round42-additions.md'
README_DRAFT = 'readme-r42-rows.md'
SOURCES_DRAFT = 'sources-r42-rows.md'
LEDGER = 'fill-ledger.tsv'
LOG_DRAFT = 'log-r42-entry.md'


class Unevaluable(Exception):
    pass


def show(lane, rev, path):
    p = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return p.stdout.decode('utf-8', 'replace') if p.returncode == 0 else None


def fences(text):
    """[(header_line, body)] for every ```markdown fence, header = nearest preceding non-blank line."""
    out, body, header, last = [], None, '', ''
    for line in text.splitlines():
        if line.startswith('```'):
            if body is None:
                body, header = [], last
            else:
                out.append((header, '\n'.join(body)))
                body = None
            continue
        if body is not None:
            body.append(line)
        elif line.strip():
            last = line
    return out


def pick(fences_list, needle):
    for header, block in fences_list:
        if needle in block:
            return block
    raise Unevaluable('no fenced block containing %r' % needle)


def section(text, heading):
    lines = text.splitlines()
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


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def sid_tokens(text):
    return set(SID_RE.findall(text))


def insert_after_last(lines, startswith, new_lines):
    idx = [i for i, l in enumerate(lines) if l.startswith(startswith)]
    if not idx:
        raise Unevaluable('no line starts %r' % startswith)
    at = idx[-1] + 1
    return lines[:at] + list(new_lines) + lines[at:]


def synthetic(base_province, base_readme, prov_block, cov_row, idx_row, frontier_line):
    prov = base_province.rstrip('\n') + '\n\n' + prov_block.strip('\n') + '\n'
    # coverage-map row: append inside the section, after its last table row
    lines = base_readme.splitlines()
    sec = section(base_readme, '## Coverage map')
    if sec is None:
        raise Unevaluable('base README has no ## Coverage map section')
    last_row = [l for l in sec if l.lstrip().startswith('|')][-1]
    readme = insert_after_last(lines, last_row, [cov_row.strip()])
    # knowledge index row: inside ## Knowledge, after its last table row
    km = section('\n'.join(readme), '## Knowledge')
    if km is not None:
        krow = [l for l in km if l.lstrip().startswith('|')][-1]
        readme = insert_after_last(readme, krow, [idx_row.strip()])
    # frontier line: after the last sasquatch-v4be bullet
    readme = insert_after_last(readme, '- sasquatch-v4be', [frontier_line.strip()])
    return prov, '\n'.join(readme) + '\n'


# ------------------------------------------------------------------ bindings

def check_province(prov_text):
    b = {}
    sec = section(prov_text, CORE_HEADING)
    b['province_core_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(
        HANDLER_RE.search(cells(r)[0]) and len(format_hits(r)) >= FORMAT_MIN and ENTRY in r
        for r in rows)
    b['province_core_row_format_hits'] = [format_hits(r) for r in rows]
    b['province_core_rows_seen'] = [cells(r)[0][:60] for r in rows if HANDLER_RE.search(cells(r)[0])]
    note = [l for l in prov_text.splitlines() if FRONTIER_MARK in l]
    b['frontier_note_lines'] = len(note)
    b['frontier_note'] = any(
        l.startswith(FRONTIER_MARK) and STEM in l and 'supersede' in l.lower()
        and len(format_hits(l)) >= FORMAT_MIN and SUPERSEDED_PHRASE in l
        for l in note)
    b['frontier_note_format_hits'] = [format_hits(l) for l in note]
    return b


def check_entry(text, base_sids, draft_sids):
    b = {}
    b['entry_present'] = bool(text) and len(text) > 4000
    cited = set()
    for line in (text or '').splitlines():
        if line.startswith('source:'):
            cited |= sid_tokens(line)
    b['entry_source_ids'] = sorted(cited)
    b['sourced_new'] = any(s not in base_sids and s in draft_sids for s in cited)
    b['entry_names_stem'] = False  # the entry file name is the stem; kept for symmetry
    return b


def check_readme(text):
    cm = section(text, '## Coverage map')
    return {'coverage_map_row': bool(cm) and any(STEM in l for l in cm if l.lstrip().startswith('|'))}


def check_sources(block, entry=ENTRY):
    rows = [l for l in block.splitlines() if re.match(r'^\s*\|\s*S\d{3,}\s*\|', l)]
    bad = []
    ids = []
    for r in rows:
        c = cells(r)
        ids.append(c[0] if c else '?')
        if len(c) != 11 or c[8] != OPENED or (entry not in c[10] and STEM not in c[10]):
            bad.append({'id': c[0] if c else '?', 'cells': len(c),
                        'opened': c[8] if len(c) > 8 else None,
                        'used_by': (c[10][:60] if len(c) > 10 else None)})
    good_ids = [c[0] for r in rows for c in [cells(r)]
                if len(c) == 11 and c[8] == OPENED and (entry in c[10] or STEM in c[10])]
    return {'sources_rows_valid': bool(rows) and not bad, 'sources_ids': ids,
            'sources_valid_ids': good_ids, 'sources_bad': bad}


def check_fills(texts, ledger_text):
    toks = {}
    for name, t in texts.items():
        empty = t.count('<<L1:>>')
        for m in TOKEN_RE.findall(t):
            toks.setdefault(m, set()).add(name)
        if empty:
            return {'fill_tokens_closed': False, 'reason': 'empty token in %s' % name}
    ledger = set()
    for line in ledger_text.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        ledger.add(line.split('\t')[0].strip())
    missing = sorted(t for t in toks if t not in ledger)
    orphan = sorted(t for t in ledger if t not in toks and '{N}' not in t and '<N>' not in t)
    return {'fill_tokens_closed': not missing and not orphan,
            'fill_missing': missing, 'fill_orphan': orphan,
            'fill_tokens': len(toks)}


def run(dirpath, lane, base):
    base_prov = show(lane, base, 'PROVINCE.md')
    base_readme = show(lane, base, 'corpus/README.md')
    base_sources = show(lane, base, 'corpus/SOURCES.md')
    if base_prov is None or base_readme is None or base_sources is None:
        raise Unevaluable('base blobs missing at %s' % base)
    prov_txt = open(os.path.join(dirpath, PROVINCE_DRAFT)).read()
    readme_txt = open(os.path.join(dirpath, README_DRAFT)).read()
    src_txt = open(os.path.join(dirpath, SOURCES_DRAFT)).read()
    entry_name = 'entry-' + ENTRY.replace('/', '-')
    entry_txt = open(os.path.join(dirpath, entry_name)).read()
    ledger_txt = open(os.path.join(dirpath, LEDGER)).read()

    pf = fences(prov_txt)
    prov_block = pick(pf, CORE_HEADING)
    rf = fences(readme_txt)
    cov = pick(rf, '| SquashFS v3 handler family through REA (round 42)')
    idx = pick(rf, '| `' + STEM + '` |')
    frn = pick(rf, '- sasquatch — 2026-10-26 round 42')
    prov, readme = synthetic(base_prov, base_readme, prov_block, cov, idx, frn)

    b = {}
    b.update(check_province(prov))
    b.update(check_readme(readme))
    b.update(check_entry(entry_txt, sid_tokens(base_sources),
                         set(check_sources(pick(fences(src_txt), '| S130'))['sources_valid_ids'])))
    b.update(check_sources(pick(fences(src_txt), '| S130')))
    log_txt = open(os.path.join(dirpath, LOG_DRAFT)).read()
    b.update(check_fills({ENTRY: entry_txt, PROVINCE_DRAFT: prov_txt, README_DRAFT: readme_txt,
                          SOURCES_DRAFT: src_txt, LOG_DRAFT: log_txt}, ledger_txt))
    names = ('province_core_section', 'province_core_row', 'frontier_note', 'entry_present',
             'sourced_new', 'coverage_map_row', 'sources_rows_valid', 'fill_tokens_closed')
    res = {'bindings': b, 'order': list(names), 'met': all(b.get(n) is True for n in names)}
    return res


# ------------------------------------------------------------------ selftest

def selftest():
    """Mutants on in-memory text; each must die on exactly one named binding."""
    prov_ok = ('## Round-42 additions to Core\n\n| Surface | Keys | Probe | Evidence |\n|---|---|---|---|\n'
               '| little-endian SquashFS v3 — the `squashfs_v3` handler family, squashfs_v3 family, '
               'SquashFS version 3, v3 family | k | p | %s |\n\n'
               'Round-42 frontier note, 2026-10-26: it supersedes %s for the handlers; the phrase '
               '"coverage claim only" is history; little-endian SquashFS v3, squashfs_v3 family, '
               'SquashFS version 3, v3 family, `%s`.\n' % (ENTRY, STEM, STEM))
    readme_ok = ('## Coverage map\n\n| a | b | c |\n|---|---|---|\n| x | `other` | y |\n\n'
                 '## Knowledge\n\n| entry | topic | source | at |\n|---|---|---|---|\n| `z` | t | s | d |\n\n'
                 '## Frontier\n\n- sasquatch-v4be — old\n- adb — x\n')
    readme_ok = readme_ok.replace('| x | `other` | y |', '| x | `%s` | y |' % STEM)
    entry_ok = 'x' * 5000 + '\nsource: S130 — row\nsource: S112 — old row\n'
    sources_ok = ('| S130 | doc | dataset | A | scope | anchor | teaches | mined | 2026-10-26 | 180d | %s |\n'
                  '| S134 | own | own-work | A | scope | anchor | teaches | mined | 2026-10-26 | 180d | %s |\n'
                  % (ENTRY, ENTRY))
    ledger_ok = '# ledger\n'

    def score(prov=prov_ok, readme=readme_ok, entry=entry_ok, sources=sources_ok, ledger=ledger_ok):
        b = {}
        b.update(check_province(prov))
        b.update(check_readme(readme))
        b.update(check_entry(entry, set(), set(check_sources(sources)['sources_valid_ids'])))
        b.update(check_sources(sources))
        b.update(check_fills({'e': entry}, ledger))
        return b

    cases = []

    def add(name, fn, want):
        cases.append((name, fn, want))

    add('baseline green', lambda: score(), None)
    add('heading miscased',
        lambda: score(prov=prov_ok.replace('## Round-42 additions to Core', '## round-42 additions to Core')),
        'province_core_section')
    add('handler token renamed in first cell',
        lambda: score(prov=prov_ok.replace(
            '| little-endian SquashFS v3 — the `squashfs_v3` handler family, squashfs_v3 family, '
            'SquashFS version 3, v3 family |',
            '| SquashFS v3 family (`squashfs_V3`, `squashfs_v3_ddwrt`) — SquashFS v3, '
            'SquashFS version 3, v3 family |', 1)),
        'province_core_row')
    add('format tokens stripped from row',
        lambda: score(prov=prov_ok.replace(
            '| little-endian SquashFS v3 — the `squashfs_v3` handler family, squashfs_v3 family, '
            'SquashFS version 3, v3 family |',
            '| the `squashfs_v3` handler |', 1)),
        'province_core_row')
    add('entry path missing from row',
        lambda: score(prov=prov_ok.replace('| %s |\n' % ENTRY, '| other |\n', 1)),
        'province_core_row')
    add('note reflowed to two lines',
        lambda: score(prov=prov_ok.replace('it supersedes %s' % STEM, 'it supersedes\n%s' % STEM, 1)),
        'frontier_note')
    add('supersede verb dropped',
        lambda: score(prov=prov_ok.replace('it supersedes', 'it replaces', 1)),
        'frontier_note')
    add('superseded phrase dropped',
        lambda: score(prov=prov_ok.replace('"coverage claim only" is history', 'it is history', 1)),
        'frontier_note')
    add('coverage row stem removed',
        lambda: score(readme=readme_ok.replace('| x | `%s` | y |' % STEM, '| x | `nope` | y |')),
        'coverage_map_row')
    add('used-by rewritten',
        lambda: score(sources=sources_ok.replace('| %s |' % ENTRY, '| other.md |')),
        'sourced_new')
    add('sources row loses a cell',
        lambda: score(sources=sources_ok.replace('| mined | 2026-10-26 | 180d |', '| mined | 2026-10-26 |', 1)),
        'sources_rows_valid')
    add('sources row opened wrong day',
        lambda: score(sources=sources_ok.replace('2026-10-26', '2026-10-25', 1)),
        'sources_rows_valid')
    add('fill token emptied',
        lambda: score(entry=entry_ok + '<<L1:>>\n'),
        'fill_tokens_closed')
    add('fill token missing from ledger',
        lambda: score(entry=entry_ok + '<<L1:new>>\n'),
        'fill_tokens_closed')

    out = []
    ok = True
    for name, fn, want in cases:
        b = fn()
        green = all(b.get(k) is True for k in ('province_core_section', 'province_core_row', 'frontier_note',
                                               'entry_present', 'sourced_new', 'coverage_map_row',
                                               'sources_rows_valid', 'fill_tokens_closed'))
        if want is None:
            good = green
        else:
            good = (not green) and b.get(want) is False
        ok = ok and good
        out.append({'case': name, 'want_false': want, 'green': green, 'pass': good})
    return {'selftest_ok': ok, 'cases': out}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir')
    ap.add_argument('--lane', default='/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
    ap.add_argument('--base', default='c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c')
    ap.add_argument('--work')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        res = selftest()
        code = 0 if res['selftest_ok'] else 1
    else:
        if not a.dir:
            ap.error('--dir is required')
        work = tempfile.mkdtemp(prefix='r42-entry-', dir=a.work or os.environ.get('TMPDIR'))
        try:
            res = run(a.dir, a.lane, a.base)
            res['work'] = work
            code = 0 if res['met'] else 1
        except Unevaluable as e:
            res, code = {'error': str(e)}, 2
        finally:
            pass
        res.pop('work', None)
    txt = json.dumps(res, indent=1, sort_keys=True)
    if a.json_out:
        open(a.json_out, 'w').write(txt + '\n')
    print(txt)
    return code


if __name__ == '__main__':
    sys.exit(main())
