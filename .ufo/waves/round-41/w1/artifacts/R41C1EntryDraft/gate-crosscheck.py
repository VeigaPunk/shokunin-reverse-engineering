#!/usr/bin/env python3
"""Evaluate the R41-C1 drafts with the GATE's own code, not a mirror of it.

The in-wave ports carry the round-41 constants and matchers:
  .ufo/waves/round-41/w1/artifacts/R41C1Counter/c1-counter.py   (main counter)
  .ufo/waves/round-41/w1/artifacts/R41C1Extra/c1-extra.py       (supplementary gate)
This script imports them by path (read-only), feeds the draft text into their own
helpers, and prints the resulting booleans. It cannot run the whole counters (they need
git revisions and a frozen carriers.json), so it evaluates exactly the text bindings:

  province_section   counter.section(prov, counter.CORE_HEADING) is not None
  province_row       counter: a row whose first cell matches HANDLER_RE, line matches
                     AVM_LAYOUT_RE and contains ENTRY
  counter_frontier   counter: a line with FRONTIER_MARK, STEM and AVM_LAYOUT_RE
  extra_frontier     extra.note_verdict(the note line)['ok']  (four clauses)
  entry_sids         extra/counter SID regexes over the entry's `source:` lines
  sources_row        counter: 11 cells, opened == OPENED, ENTRY or STEM in used-by
  coverage_row       counter.section() over a synthesized `## Coverage map` holding the row

Usage: gate-crosscheck.py [--dir DIR] [--ports DIR] [--json-out F]
Exit 0 every binding true, 1 any false, 2 a port or draft is missing.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORTS = os.path.join(HERE, '..')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(path):
    with open(path, 'rb') as f:
        return f.read().decode('utf-8', 'replace')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default=HERE)
    ap.add_argument('--ports', default=DEFAULT_PORTS)
    ap.add_argument('--json-out')
    a = ap.parse_args(argv)
    counter_p = os.path.join(a.ports, 'R41C1Counter', 'c1-counter.py')
    extra_p = os.path.join(a.ports, 'R41C1Extra', 'c1-extra.py')
    for p in (counter_p, extra_p):
        if not os.path.exists(p):
            print(json.dumps({'error': 'port missing: %s' % p}), file=sys.stderr)
            return 2
    counter = load(counter_p, 'r41counter')
    extra = load(extra_p, 'r41extra')

    entry = read(os.path.join(a.dir, 'entry-corpus-knowledge-2026-10-26-r41-avm-be-squashfs-core.md'))
    prov = read(os.path.join(a.dir, 'province-round41-additions.md'))
    readme = read(os.path.join(a.dir, 'readme-r41-rows.md'))
    sources = read(os.path.join(a.dir, 'sources-r41-rows.md'))

    res, detail = {}, {}

    sec = counter.section(prov, counter.CORE_HEADING)
    res['province_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    hit = [r for r in rows if counter.HANDLER_RE.search(counter.cells(r)[0])
           and counter.AVM_LAYOUT_RE.search(r) and counter.ENTRY in r]
    res['province_row'] = bool(hit)
    detail['province_row'] = hit[0][:220] if hit else None

    res['counter_frontier'] = any(counter.FRONTIER_MARK in l and counter.STEM in l
                                  and counter.AVM_LAYOUT_RE.search(l)
                                  for l in prov.splitlines())
    notes = [l for l in prov.splitlines() if l.startswith(extra.NOTE)]
    verd = [extra.note_verdict(l) for l in notes]
    res['extra_frontier'] = len(notes) == 1 and verd[0]['ok']
    detail['extra_frontier'] = verd

    src_ids = [l for l in entry.splitlines() if l.lower().startswith('source')]
    ids = set()
    for l in src_ids:
        ids |= counter.sid_tokens(l)
    res['entry_sids'] = bool(ids)
    detail['entry_sids'] = sorted(ids)

    reg_rows = {}
    for l in sources.splitlines():
        if not (len(l) >= 4 and l.lstrip().startswith('|') and l.lstrip()[1:].strip().startswith('S')):
            continue
        c = counter.cells(l)
        if len(c) == 11 and c[0].startswith('S'):
            reg_rows[c[0]] = c
    ok_rows = [k for k, c in reg_rows.items()
               if c[0] in ids and c[8] == counter.OPENED
               and (counter.ENTRY in c[10] or counter.STEM in c[10])]
    res['sources_row'] = bool(ok_rows)
    detail['sources_row'] = {'rows': sorted(reg_rows), 'ok': ok_rows,
                             'cells': {k: len(c) for k, c in reg_rows.items()}}

    cov_rows = [l for l in readme.splitlines()
                if l.lstrip().startswith('|') and counter.STEM in l]
    synth = '## Coverage map\n' + (cov_rows[0] if cov_rows else '') + '\n## Knowledge\n'
    cs = counter.section(synth, '## Coverage map')
    res['coverage_row'] = bool(cs) and any(counter.STEM in l for l in cs if l.lstrip().startswith('|'))

    out = {'ports': {os.path.basename(p): sha(p) for p in (counter_p, extra_p)},
           'bindings': res, 'detail': detail,
           'met': all(res.values())}
    print(json.dumps(out, indent=1, sort_keys=True))
    if a.json_out:
        with open(a.json_out, 'w') as f:
            f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
    return 0 if out['met'] else 1


if __name__ == '__main__':
    sys.exit(main())
