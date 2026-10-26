#!/usr/bin/env python3
"""R41C2Mutants phase 2b: run the six survivor-killing selftest cases against
pristine and each mutant interpreter (scratch copies). Cases are built with the
tool's own fixture helpers so the v3 interpreter can adopt them verbatim
(v2 marker swapped for the v3 marker)."""
import importlib.util
import json
import os
import sys
import tempfile

S = '/fast/scratch/hyaku/kaidoku-r41/R41C2Mutants'

ENV_WITH_GAPS = {
    'operation': 'extract_firmware',
    'provider': {'id': 'unblob'},
    'normalized_result': {
        'extraction_gaps': [{'kind': 'unpublished-entry', 'dependencies': []}],
        'files': [{'relative_path': 'x.bin_extract/a.txt'}],
        'chunks': [{'handler': 'squashfs_v4_le'}],
        'diagnostics': [],
    },
}

ENV_STRING_PROVIDER = {
    'operation': 'extract_firmware',
    'provider': 'unblob',
    'normalized_result': {
        'extraction_gaps': [], 'files': [{'relative_path': 'a.txt'}],
        'chunks': [{'handler': 'squashfs_v4_le'}], 'diagnostics': [],
    },
}

ENV_NR_DIAG_COMMAND = {
    'operation': 'extract_firmware',
    'provider': {'id': 'unblob'},
    'normalized_result': {
        'extraction_gaps': [{'kind': 'extractor-failure', 'dependencies': []}],
        'files': [],
        'chunks': [{'handler': 'squashfs_v4_be'}],
        'diagnostics': [{'report': {'command': '/opt/sasquatch-v4be 4 /tmp/c.sqsh /out'}}],
    },
}


def load(path):
    spec = importlib.util.spec_from_file_location('triage_%d' % abs(hash(path)), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_cases(mod, work):
    """name -> {skill, env, expected_exit, expected_pair}"""
    cases = {}

    def reg(name, skill, env, exitc, pair):
        cases[name] = {'skill': skill, 'env': env, 'expected_exit': exitc,
                       'expected_pair': pair}

    # K-M05: two markers, each followed by a table; the first must win.
    first = mod._block([mod._row('first-table')])
    second = mod._block([mod._row('second-table', action='inspect-input')])
    skill = mod._write(work, 'sk-two-markers.md',
                       mod._skel(first + '\nprose between the two tables\n\n' + second))
    reg('K-M05-two-markers-first-wins', skill, mod._fixture('H', 'H01'), 0,
        ['first-table', 'none'])

    # K-M07: a gaps=none row before the correct row must not match a gapped envelope.
    rows = [mod._row('trap', handler='squashfs_v4_le', gaps='none', deps='*',
                     be='*', sr='no', files='>0', action='inspect-input'),
            mod._row('right', handler='squashfs_v4_le', gaps='unpublished-entry',
                     deps='none', be='n/a', sr='no', files='>0', action='count-gap')]
    skill = mod._write(work, 'sk-none-trap.md', mod._skel(mod._block(rows)))
    reg('K-M07-none-set-cell-rejects-nonempty', skill,
        mod._dump(work, 'env-gapped.json', ENV_WITH_GAPS), 0, ['right', 'count-gap'])

    # K-M15: a repeated member in a set cell is malformed (exit 2).
    rows = [mod._row('dup', gaps='unpublished-entry+unpublished-entry')]
    skill = mod._write(work, 'sk-repeated-member.md', mod._skel(mod._block(rows)))
    reg('K-M15-repeated-set-member-rejected', skill, mod._fixture('H', 'H01'), 2, None)

    # K-M26: a provider recorded as a bare string is used as is.
    rows = [mod._row('strprov', provider='unblob')]
    skill = mod._write(work, 'sk-strprov.md', mod._skel(mod._block(rows)))
    reg('K-M26-string-provider-used', skill,
        mod._dump(work, 'env-strprov.json', ENV_STRING_PROVIDER), 0,
        ['strprov', 'none'])

    # K-M28: blank lines between the vocabulary line and the header are allowed.
    blk = mod._block([mod._row('x')])
    blk = blk.replace(mod._vocab_line() + '\n| ', mod._vocab_line() + '\n\n\n| ', 1)
    skill = mod._write(work, 'sk-blank-lines.md', mod._skel(blk))
    reg('K-M28-blank-lines-tolerated', skill, mod._fixture('H', 'H01'), 0,
        ['x', 'none'])

    # K-M30: a sasquatch command recorded only under normalized_result.diagnostics
    # still sets BE=no, so the AVM row (not the body row) matches.
    rows = [mod._row('avmR', handler='squashfs_v4_be', gaps='extractor-failure',
                     deps='none', be='no', sr='*', files='0',
                     action='preserve-failure')]
    skill = mod._write(work, 'sk-nrdiag.md', mod._skel(mod._block(rows)))
    reg('K-M30-nr-diagnostics-be-source', skill,
        mod._dump(work, 'env-nrdiag.json', ENV_NR_DIAG_COMMAND), 0,
        ['avmR', 'preserve-failure'])

    return cases


def run_variant(name, path, work):
    mod = load(path)
    cases = build_cases(mod, work)
    row = {}
    for cname, c in cases.items():
        res = mod._cli(['--skill', c['skill'], c['env']])
        pair = None
        if res.returncode == 0:
            lines = [l for l in res.stdout.splitlines() if l.strip()]
            if len(lines) == 1 and '\t' in lines[0]:
                parts = lines[0].split('\t')
                pair = parts[1:3] if len(parts) >= 3 else None
        passed = res.returncode == c['expected_exit'] and (
            pair == c['expected_pair'] if c['expected_pair'] is not None else True)
        row[cname] = {'exit': res.returncode, 'pair': pair,
                      'expected_exit': c['expected_exit'],
                      'expected_pair': c['expected_pair'], 'pass': passed,
                      'stderr_tail': (res.stderr or '').strip()[-160:]}
    return row


def main():
    variants = [('pristine', S + '/interp-pristine.py')]
    for mid in ('M05-last-marker-wins', 'M07-none-set-cell-accepts-any',
                'M15-repeated-set-member-accepted', 'M26-string-provider-ignored',
                'M28-blank-line-walk-disabled', 'M30-nr-diagnostics-be-source-dropped',
                'M10-fnmatch-normcase'):
        variants.append((mid, S + '/mutants/interp-%s.py' % mid))
    work = tempfile.mkdtemp(prefix='interp-cases.', dir=os.environ.get('TMPDIR') or None)
    results = {}
    for name, path in variants:
        results[name] = run_variant(name, path, work)
        summary = {k: ('PASS' if v['pass'] else 'FAIL(exit=%s pair=%s)'
                       % (v['exit'], v['pair'])) for k, v in results[name].items()}
        print('%-40s %s' % (name, json.dumps(summary)), flush=True)
    with open(S + '/interp-case-results.json', 'w') as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print('WROTE interp-case-results.json', flush=True)


if __name__ == '__main__':
    main()
