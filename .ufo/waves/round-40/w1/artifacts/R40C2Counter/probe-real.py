#!/usr/bin/env python3
"""Read-only probe: R40C2Counter's mechanics on the real lane at HEAD.

Not a gate and not part of the counter's exit contract — it prints the facts
the report cites:
  * the base commit `derive_base` picks (newest SKILL.md without the v2 marker)
    and the rule-block-18 (v1) table bytes at that base and at HEAD;
  * the v1 interpreter's `--json`/`--tab`/`--table-only` interfaces exercised
    through the counter's own parsers, on committed round-39 held-out
    envelopes (git objects only; no REA or unblob run).

Usage: python3 -I -B probe-real.py [--root LANE]
Scratch under $HYAKU_SCRATCH/kaidoku-r40 (or TMPDIR), removed at exit.
"""
import glob
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
V1_INTERP = 'tools/round-39/sqfs-triage.py'
HELDOUT = 'corpus/evidence/round-39/c2/heldout'


def git(root, *args):
    return subprocess.run(['git', '-C', root] + list(args),
                          capture_output=True, text=True).stdout.strip()


def load_counter():
    spec = importlib.util.spec_from_file_location('c2c', os.path.join(HERE, 'c2-counter.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    root = LANE
    if argv and '--root' in argv:
        root = argv[argv.index('--root') + 1]
    m = load_counter()
    head = git(root, 'rev-parse', 'HEAD')
    base, src = m.derive_base(root, head)
    v1_head = m.table_block(m.as_text(m.show(root, head, m.SKILL)), m.MARKER_V1)
    v1_base = m.table_block(m.as_text(m.show(root, base, m.SKILL)), m.MARKER_V1)
    v2_head = m.table_block(m.as_text(m.show(root, head, m.SKILL)), m.MARKER_V2)
    out = {
        'head': head, 'derived_base': base, 'base_source': src,
        'v1_present_at_head': v1_head is not None,
        'v1_present_at_base': v1_base is not None,
        'v1_identical_base_head': v1_head == v1_base,
        'v1_sha256_head': hashlib.sha256(v1_head.encode()).hexdigest() if v1_head else None,
        'v1_sha256_base': hashlib.sha256(v1_base.encode()).hexdigest() if v1_base else None,
        'v1_bytes': len(v1_head.encode()) if v1_head else 0,
        'v1_header_cells': m.header_cells(v1_head),
        'v2_present_at_head': v2_head is not None,
    }
    scratch = tempfile.mkdtemp(
        prefix='probe-r40c2.',
        dir=os.path.join(os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir(),
                         'kaidoku-r40'))
    try:
        blob = m.show(root, head, V1_INTERP)
        if blob is None:
            out['interpreter_probe'] = 'unavailable: %s absent at HEAD' % V1_INTERP
        else:
            ipath = os.path.join(scratch, 'sqfs-triage.py')
            with open(ipath, 'wb') as fh:
                fh.write(blob)
            spath = os.path.join(scratch, 'SKILL.md')
            with open(spath, 'wb') as fh:
                fh.write(m.show(root, head, m.SKILL))
            edir = os.path.join(scratch, 'env')
            os.makedirs(edir)
            envs = []
            for p in sorted(glob.glob(os.path.join(root, HELDOUT, 'H*', 'envelope.json')))[:4]:
                dst = os.path.join(edir, os.path.basename(os.path.dirname(p)) + '.json')
                with open(p, 'rb') as src_fh, open(dst, 'wb') as dst_fh:
                    dst_fh.write(src_fh.read())
                envs.append(dst)
            jr = m.run_interp(ipath, spath, envs, ['--json'])
            parsed = m.parse_json_results(jr.stdout) if jr.returncode == 0 else None
            tr = m.run_interp(ipath, spath, envs)
            tab = m.parse_tab_results(tr.stdout) if tr.returncode == 0 else None
            pr = m.run_interp(ipath, spath, [], ['--table-only'])
            label_rows = m.parse_table_only(pr.stdout) if pr.returncode == 0 else None
            header, trows = m.parse_v2_rows(v1_head)
            tpos = {cells[header.index('label')]: i for i, cells in enumerate(trows)} \
                if header and 'label' in header else {}
            out['interpreter_probe'] = {
                'path': V1_INTERP, 'json_exit': jr.returncode, 'tab_exit': tr.returncode,
                'table_only_exit': pr.returncode,
                'json_results': {os.path.basename(k): {
                    'label': v['label'], 'action': v['action'], 'row': v['row'],
                    'cells_head': (v['cells'] or [])[:2]} for k, v in sorted((parsed or {}).items())},
                'tab_results': {os.path.basename(k): v for k, v in sorted((tab or {}).items())},
                'table_only_labels': len(label_rows or {}),
                'row_index_base_from_reported_rows':
                    m.infer_index_base(list((parsed or {}).values()), tpos, None),
                'row_index_base_from_table_only': m.infer_index_base([], tpos, label_rows),
            }
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
