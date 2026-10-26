#!/usr/bin/env python3
"""R42C2EntryReview probe: re-execute the R41-CL4 / F1 divergences at the c4a38ea bytes.

Synthetic envelopes only (stdlib; the envelope builder is the frozen v3
interpreter's own ``_env``).  No REA, no unblob, no carrier, no lane write
outside this artifacts dir.  Usage:

    python3 -I -B probe-entry.py INTERPRETER.py SKILL.md OUT.json
"""
import importlib.util
import json
import os
import sys
import tempfile


def load(path):
    spec = importlib.util.spec_from_file_location('triage_v3', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    interp_path, skill_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    tri = load(interp_path)
    results = {}

    tab = tri._cli(['--skill', skill_path, '--table-only'])
    results['table-only'] = {
        'rc': tab.returncode,
        'stdout': tab.stdout.strip(),
        'stderr': tab.stderr.strip()[:400],
    }

    work = tempfile.mkdtemp(prefix='probe-entry.')
    cases = {
        'legacy-clean': (
            dict(handler='squashfs_v3', files=2),
            'v3 precedence step 2 (no squashfs_v4_* in H) -> '
            '(no-squashfs-chunk, inspect-input); v4 draft step 2 (F=∅ over the '
            'whole family) proceeds to step 11 -> (clean, none)'),
        'legacy-dep-sasquatch': (
            dict(handler='squashfs_v3', files=2,
                 gaps=[('missing-extractor-dependency', ['sasquatch'])]),
            'v3/v4 precedence step 3 arm 2 (D holds sasquatch) -> '
            '(dep-missing-le, install-extractor-le)'),
        'legacy-dep-both': (
            dict(handler='squashfs_v3', files=2,
                 gaps=[('missing-extractor-dependency', ['sasquatch', 'sasquatch-v4be'])]),
            'v3/v4 precedence step 3 arm 1 (D holds sasquatch-v4be) -> '
            '(dep-missing-be, install-extractor-be)'),
        'v4be-dep-both': (
            dict(handler='squashfs_v4_be', files=2,
                 gaps=[('missing-extractor-dependency', ['sasquatch', 'sasquatch-v4be'])]),
            'precedence step 3 arm 1 -> (dep-missing-be, install-extractor-be); '
            'isolates the exact-deps-cell grammar limit (R41W2 F1) from the '
            'handler-family restriction'),
        'v4be-clean': (
            dict(handler='squashfs_v4_be', files=2),
            'precedence step 11 -> (clean, none); harness control'),
        'legacy-ddwrt-failure': (
            dict(handler='squashfs_v3_ddwrt', files=0, gaps=['extractor-failure']),
            'v3 precedence step 6 -> (body-extractor-failure, preserve-failure); '
            'v4 draft step 6 -> (legacy-body-failure, cross-read-legacy)'),
    }
    for name, (kw, expect) in cases.items():
        path = os.path.join(work, name + '.json')
        with open(path, 'w') as fh:
            json.dump(tri._env(**kw), fh)
        res = tri._cli(['--skill', skill_path, path])
        results[name] = {
            'rc': res.returncode,
            'stdout': res.stdout.strip(),
            'stderr': res.stderr.strip()[:400],
            'expected_of_v3_precedence': expect,
        }

    with open(out_path, 'w') as fh:
        json.dump(results, fh, indent=2, sort_keys=True)
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
