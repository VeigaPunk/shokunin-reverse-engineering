#!/usr/bin/env python3
"""R43-C1 refusal prototype: declared-tuple vs OBSERVED-envelope tuple, standalone.

This is a *reconstruction*, not lane code.  It ports, without importing anything
from the lane, the three extraction functions the frozen round-42 generator uses
(`_be_argv`, `_envelope_parts`, `observed_features` at
tools/round-42/heldout-gen-v4.py:2516,2539,2964), and adds the one function the
round-42 generator is missing: a check that every carrier's six-field declared
tuple equals the tuple its own envelope exhibits.

It reads `DIR/manifest.json` plus each `DIR/<id>/rea-full.json` (or
`.rea-full.json.gz`) and writes NOTHING.  Exit codes:
  0  every carrier's observed tuple == its declared tuple
  3  at least one differs (R42-CL1 shape); per-carrier diff on stdout
  2  unusable input (missing manifest / envelope / unparsable)
  4  a carrier declares no `declared_features`

Why `rea-full.json` and not `run.json`: `run.json` is the generator's own
summary of the same in-memory shape, so checking it re-reads the writer's
opinion.  `rea-full.json` is the whole `{ok, data, meta}` envelope, so the
observation is re-derived from the emitted bytes (the round-42 `--verify` path
reads `run.json` -- that is the weaker of the two available observations).

Usage:
  python3 -I -B tuple-check-proto.py --dir <heldout dir> [--json-out PATH]
  python3 -I -B tuple-check-proto.py --dir <heldout dir> --declared-from <json>
      (control only: replace a carrier's declared tuple from a JSON map
       {id: {six fields}} so the red/green pair can be produced without REA)
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import posixpath
import sys

DECLARED_FIELDS = ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
                   'symlink_removed', 'published')
DECLARED_KEY = 'declared_features'


# --- ported verbatim in behaviour from heldout-gen-v4.py:2516 ----------------
def _be_argv(commands):
    """'-be' in a recorded extractor child argv: 'yes' / 'no' / 'n/a'."""
    seen = False
    for command in commands:
        tokens = command.split()
        if not tokens:
            continue
        base = posixpath.basename(tokens[0])
        if base.startswith('sasquatch') or base.startswith('unsquashfs'):
            seen = True
            if '-be' in tokens[1:]:
                return 'yes'
    return 'no' if seen else 'n/a'


# --- ported verbatim in behaviour from heldout-gen-v4.py:2539 ----------------
def _envelope_parts(full):
    """(data object or None, subject sha256, shape summary) from a CLI envelope."""
    if not isinstance(full, dict) or not isinstance(full.get('data'), dict):
        return None, None, {}
    data = full['data']
    normalized = data.get('normalized_result') or {}
    reports = [diag.get('report') or {}
               for diag in normalized.get('diagnostics') or []]
    shape = {
        'operation': data.get('operation'),
        'provider': (data.get('provider') or {}).get('id'),
        'handlers': sorted({chunk.get('handler')
                            for chunk in normalized.get('chunks') or []
                            if chunk.get('handler')}),
        'failed_chunks': sorted({chunk.get('handler')
                                 for chunk in normalized.get('chunks') or []
                                 if chunk.get('extraction_failed') and chunk.get('handler')}),
        'gap_kinds': sorted({gap.get('kind')
                             for gap in normalized.get('extraction_gaps') or []
                             if gap.get('kind')}),
        'gap_dependencies': sorted({dep
                                    for gap in normalized.get('extraction_gaps') or []
                                    for dep in (gap.get('dependencies') or [])}),
        'diagnostics': sorted({report.get('__typename__')
                               for report in reports
                               if report.get('__typename__')}),
        'be_argv': _be_argv([report.get('command') for report in reports
                             if report.get('command')]),
        'symlink_removed': any(report.get('__typename__')
                               == 'MaliciousSymlinkRemoved' for report in reports),
        'depth_limited_paths': len(normalized.get('depth_limited_paths') or []),
        'parameters': {'max_depth': (data.get('parameters') or {}).get('max_depth')},
        'files': len(normalized.get('files') or []),
        'coverage': normalized.get('coverage'),
    }
    subject = (data.get('subject') or {}).get('digest') or {}
    return data, subject.get('sha256'), shape


# --- ported verbatim in behaviour from heldout-gen-v4.py:2964 ----------------
def observed_features(record):
    """The tuple the precedence text reads, as measured in one envelope."""
    return {
        'handler_set': sorted(record.get('handlers') or []),
        'gap_kinds': sorted(record.get('gap_kinds') or []),
        'gap_dependencies': sorted(record.get('gap_dependencies') or []),
        'symlink_removed': bool(record.get('symlink_removed')),
        'extraction_failed': bool(record.get('failed_chunks')),
        'published': 'nonzero' if (record.get('files') or 0) > 0 else 'zero',
        'be_argv': record.get('be_argv'),
        'max_depth': (record.get('parameters') or {}).get('max_depth'),
    }


# --- new (the refusal) ------------------------------------------------------
def read_envelope(out_dir, carrier_id):
    """The full `{ok, data, meta}` envelope for one carrier, or None."""
    dest = os.path.join(out_dir, carrier_id)
    plain = os.path.join(dest, 'rea-full.json')
    packed = plain + '.gz'
    if os.path.isfile(plain):
        with open(plain, encoding='utf-8') as handle:
            return json.load(handle)
    if os.path.isfile(packed):
        with gzip.open(packed, 'rt', encoding='utf-8') as handle:
            return json.load(handle)
    return None


def collect_observed(out_dir, carriers):
    """id -> (observed six-field tuple, shape) re-derived from each envelope."""
    observed, shapes, missing, unparsable = {}, {}, [], []
    for entry in carriers:
        cid = str(entry.get('id'))
        try:
            full = read_envelope(out_dir, cid)
        except Exception as exc:                      # unparsable bytes
            unparsable.append((cid, repr(exc)[:120]))
            continue
        if full is None:
            missing.append(cid)
            continue
        data, _sha, shape = _envelope_parts(full)
        if data is None:
            unparsable.append((cid, 'no data object'))
            continue
        observed[cid] = observed_features(shape)
        shapes[cid] = shape
    return observed, shapes, missing, unparsable


def tuple_check(carriers, observed, declared_override=None):
    """Per-carrier declared-vs-observed verdicts.  Pure; writes nothing."""
    rows, bad = [], []
    for entry in carriers:
        cid = str(entry.get('id'))
        declared = (declared_override or {}).get(cid) or entry.get(DECLARED_KEY)
        got = observed.get(cid)
        if not isinstance(declared, dict):
            rows.append({'id': cid, 'class': entry.get('class'),
                         'verdict': 'no_declared_tuple', 'diff': []})
            bad.append(cid)
            continue
        declared6 = {key: declared.get(key) for key in DECLARED_FIELDS}
        if got is None:
            rows.append({'id': cid, 'class': entry.get('class'),
                         'verdict': 'no_envelope', 'diff': []})
            bad.append(cid)
            continue
        observed6 = {key: got[key] for key in DECLARED_FIELDS}
        diff = [{'field': key, 'declared': declared6[key], 'observed': observed6[key]}
                for key in DECLARED_FIELDS if declared6[key] != observed6[key]]
        rows.append({'id': cid, 'class': entry.get('class'),
                     'verdict': 'match' if not diff else 'MISMATCH',
                     'declared': declared6, 'observed': observed6, 'diff': diff})
        if diff:
            bad.append(cid)
    return {'ok': not bad, 'carriers_checked': len(rows),
            'mismatched': bad, 'rows': rows}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dir', required=True, help='held-out directory (manifest.json + <id>/)')
    ap.add_argument('--json-out', help='write the verdict JSON here (optional)')
    ap.add_argument('--declared-from',
                    help='JSON map {id: six-field tuple} to use as the DECLARED side '
                         '(controls only; never for a claim)')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args(argv)

    manifest_path = os.path.join(args.dir, 'manifest.json')
    if not os.path.isfile(manifest_path):
        print(f'no manifest at {manifest_path}', file=sys.stderr)
        return 2
    with open(manifest_path, encoding='utf-8') as handle:
        manifest = json.load(handle)
    carriers = manifest.get('carriers') or []
    if not carriers:
        print('manifest holds no carriers', file=sys.stderr)
        return 2
    override = None
    if args.declared_from:
        with open(args.declared_from, encoding='utf-8') as handle:
            override = json.load(handle)

    observed, _shapes, missing, unparsable = collect_observed(args.dir, carriers)
    verdict = tuple_check(carriers, observed, override)
    verdict['envelope_missing'] = missing
    verdict['envelope_unparsable'] = unparsable
    verdict['dir'] = os.path.abspath(args.dir)
    verdict['seed'] = manifest.get('seed')
    if missing or unparsable:
        verdict['ok'] = False
        for cid in missing:
            if cid not in verdict['mismatched']:
                verdict['mismatched'].append(cid)

    if not args.quiet:
        for row in verdict['rows']:
            if row['verdict'] != 'match':
                print(f"{row['id']}  {row.get('class')}  {row['verdict']}")
                for d in row['diff']:
                    print(f"    {d['field']}: declared {d['declared']!r} "
                          f"observed {d['observed']!r}")
        print(f"\ntuple check: {verdict['carriers_checked'] - len(verdict['mismatched'])}"
              f"/{verdict['carriers_checked']} carriers declare what their own "
              f"envelope shows  -> {'PASS' if verdict['ok'] else 'REFUSE'}")
    if args.json_out:
        with open(args.json_out, 'w', encoding='utf-8') as handle:
            json.dump(verdict, handle, indent=2, sort_keys=True)
            handle.write('\n')
    if verdict['envelope_missing'] or verdict['envelope_unparsable']:
        return 2
    return 0 if verdict['ok'] else 3


if __name__ == '__main__':
    sys.exit(main())
