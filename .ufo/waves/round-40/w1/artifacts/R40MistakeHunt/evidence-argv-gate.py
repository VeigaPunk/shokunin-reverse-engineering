#!/usr/bin/env python3
"""evidence-argv-gate -- a committed provenance record must name the command that ran.

Round-39 wave 2 (`w2/R39W2Separability.md` D2): `heldout-gen.py:408` executes
`npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <carrier> <outdir>` but
`:416` records `[REA_PACKAGE, 'extract-firmware'] + cmd[3:6] + [carrier, '$out']`, which repeats
the subcommand: `rea-agents@6.5.0 extract-firmware extract-firmware --format json …`. All 20
committed `corpus/evidence/round-39/c2/heldout/H*/run.json` carry the duplicated token. The score
is unaffected (the counter reads `envelope.json`), so the damage is to the provenance record only
— but that record is the one a later replay would follow.

Rule: in every `run.json`, the subcommand token appears exactly once, and the argument after it is
a flag (not the same token again).

Usage: evidence-argv-gate.py --heldout DIR [--fix-out DIR]
Exit 0 clean; 1 findings; 2 usage. Red on the round-39 held-out set; green on the `--fix-out`
copies (duplicate token dropped and the argv re-serialised).
"""
import argparse
import glob
import json
import os
import sys

SUBCOMMAND = 'extract-firmware'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--heldout', required=True)
    ap.add_argument('--fix-out')
    args = ap.parse_args(argv)

    paths = sorted(glob.glob(os.path.join(args.heldout, 'H*', 'run.json')))
    if not paths:
        print(f'USAGE no run.json under {args.heldout}', file=sys.stderr)
        return 2

    findings = []
    fixed = 0
    for path in paths:
        with open(path, encoding='utf-8') as fh:
            record = json.load(fh)
        record_argv = record.get('rea_argv') or record.get('argv')
        if isinstance(record_argv, str):
            record_argv = record_argv.split()
        if not isinstance(record_argv, list):
            findings.append(f'{path}: no argv record')
            continue
        count = record_argv.count(SUBCOMMAND)
        if count != 1:
            findings.append(f'{os.path.basename(os.path.dirname(path))}: {SUBCOMMAND!r} appears '
                            f'{count}x in rea_argv: {" ".join(record_argv)}')
        if args.fix_out and count > 1:
            out_dir = os.path.join(args.fix_out, os.path.basename(os.path.dirname(path)))
            os.makedirs(out_dir, exist_ok=True)
            repaired = list(record_argv)
            seen = False
            deduped = []
            for token in repaired:
                if token == SUBCOMMAND:
                    if seen:
                        continue
                    seen = True
                deduped.append(token)
            record['rea_argv'] = deduped
            with open(os.path.join(out_dir, 'run.json'), 'w', encoding='utf-8') as fh:
                json.dump(record, fh, indent=1)
                fh.write('\n')
            fixed += 1

    if args.fix_out:
        print(f'wrote {fixed} corrected run.json under {args.fix_out}')
    print(f'records={len(paths)} findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
