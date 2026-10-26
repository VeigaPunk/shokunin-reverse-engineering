#!/usr/bin/env python3
"""R41C2ReconDepth -- does the frozen v2 table grammar express the draft v3 rules?

The DRAFT round-41 precedence states its gap tests as membership (`depth-limited`
in G, `extractor-failure` in G, ...).  The committed v2 interpreter's gap-kinds
cell is `*`, `none`, or an EXACT set (`match_set`: frozenset(values) == payload;
tools/round-40/sqfs-triage-v2.py:599-605), and its action column is closed over
the `<!-- sqfs-triage-actions: ... -->` line (`_parse_enum_cell`).

This probe writes four variant SKILL tables into a scratch dir and labels five
dev envelopes with them:

  novocab        v2 table + a depth-limited row whose action token is NOT on the
                 actions line                     -> expect exit 2 (TableError)
  vocab          same row, token appended to the actions line  -> expect exit 0
  order-late     the depth row placed before `clean`, i.e. AFTER the symlink rows
  order-early    the depth row placed before `mixed-symlinks`, i.e. the draft's
                 precedence (rule 7 before rules 8/9/10)

Usage
    python3 -I -B table-probe.py --lane LANE --envelopes DIR --work DIR
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True

ROW = (
    "  | depth-limited-nested | `extract_firmware` | `unblob` | `squashfs_v4_*` | "
    "`depth-limited` | `*` | `*` | `*` | `*` | raise-depth | a task sat at the "
    "max_depth ceiling so its extract directory was inventoried but never analysed "
    "-> rerun with a higher max_depth (up to 10) into a fresh output directory | "
    "recon R41C2ReconDepth; FirmwareReports.js :229-230 |\n")
CASES = ('sh-alone-le-d1', 'sh-intree-le-d1', 'sh-escaping-le-d1',
         'sh-both-le-d1', 'pf-partial-le-d3')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--envelopes', required=True)
    ap.add_argument('--work', required=True)
    ns = ap.parse_args(argv)
    os.makedirs(ns.work, exist_ok=True)
    skill = os.path.join(ns.lane, 'SKILL.md')
    interp = os.path.join(ns.lane, 'tools/round-40/sqfs-triage-v2.py')
    text = open(skill, encoding='utf-8').read()
    vocab = re.search(r'<!-- sqfs-triage-actions: ([^>]*)-->', text).group(1)
    anchor_clean = "  | clean | `extract_firmware`"
    anchor_mixed = "  | mixed-symlinks |"
    assert anchor_clean in text and anchor_mixed in text
    with_vocab = text.replace(
        '<!-- sqfs-triage-actions: %s-->' % vocab,
        '<!-- sqfs-triage-actions: %s raise-depth-->' % vocab, 1)
    variants = {
        'novocab': text.replace(anchor_clean, ROW + anchor_clean, 1),
        'vocab': with_vocab.replace(anchor_clean, ROW + anchor_clean, 1),
        'order-late': with_vocab.replace(anchor_clean, ROW + anchor_clean, 1),
        'order-early': with_vocab.replace(anchor_mixed, ROW + anchor_mixed, 1),
    }
    envelopes = [os.path.join(ns.envelopes, case, 'envelope.json')
                 for case in CASES]
    for name, body in variants.items():
        path = os.path.join(ns.work, 'skill-%s.md' % name)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(body)
        proc = subprocess.run([sys.executable, '-I', '-B', interp,
                               '--skill', path, '--json', *envelopes],
                              capture_output=True, text=True)
        print('== %s: exit %d' % (name, proc.returncode))
        if proc.returncode == 0:
            for result in json.loads(proc.stdout)['results']:
                print('   %-22s %-26s %s'
                      % (os.path.basename(os.path.dirname(result['path'])),
                         result['label'], result['action']))
        else:
            print('   ' + proc.stderr.strip().splitlines()[-1])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
