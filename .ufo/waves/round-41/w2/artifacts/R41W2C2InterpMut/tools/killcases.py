#!/usr/bin/env python3
"""killcases.py -- seat R41W2C2InterpMut survivor killing cases.

For each SURVIVED mutant from mutdrive.py, build the minimal envelope that
flips its (label, action) pair, and show pristine-vs-mutant on that envelope.
Also documents three pristine interpreter/evaluator divergences on envelope
shapes the 52 held-out envelopes never exercise (K7, K8, K9).
"""
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r41/R41W2C2InterpMut'
PRIM = os.path.join(S, 'pristine')
MUT = os.path.join(S, 'mut')
KILL = os.path.join(S, 'kill')
OUT = os.path.join(S, 'out')
INTERP = 'sqfs-triage-v3.py'
EVAL = 'indep-eval-v3.py'
SKILL = os.path.join(PRIM, 'SKILL.md')


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def interp_pair(exe, path):
    r = run([sys.executable, '-I', '-B', exe, '--skill', SKILL, path])
    if r.returncode != 0:
        return 'EXIT%d' % r.returncode, (r.stderr or '').strip()[-120:]
    for line in r.stdout.splitlines():
        if line.strip():
            _p, label, action = line.split('\t')
            return label, action
    return 'EMPTY', ''


def eval_pair(exe, path):
    iso = os.path.join(KILL, 'flat', os.path.splitext(os.path.basename(path))[0])
    os.makedirs(iso, exist_ok=True)
    tmp = os.path.join(iso, 'env.json')
    with open(path, 'rb') as fh:
        data = fh.read()
    with open(tmp, 'wb') as fh:
        fh.write(data)
    r = run([sys.executable, '-I', '-B', exe, '--envelopes', iso])
    if r.returncode != 0:
        return 'EXIT%d' % r.returncode, (r.stderr or '').strip()[-120:]
    doc = json.loads(r.stdout)
    for cid, v in doc['labels'].items():
        return v['label'], v['action']
    return 'EMPTY', ''


def env(chunks, gaps, files, diags, raw=None, drop_files=False):
    nr = {'chunks': chunks, 'extraction_gaps': gaps, 'diagnostics': diags}
    if not drop_files:
        nr['files'] = files
    if raw is not None:
        return {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
                'normalized_result': nr, 'raw_result': raw}
    return {'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
            'normalized_result': nr}


def f(n):
    return [{'relative_path': 'f%02d' % i, 'size': 1} for i in range(n)]


BE_HANDLER = 'squashfs_v4_be'
CH_BE = [{'handler': BE_HANDLER}]
CH_GZIP = [{'handler': 'gzip'}]
FAIL_BE = {'kind': 'extractor-failure', 'handler': BE_HANDLER, 'dependencies': []}
CMD_OK = [{'report': {'command': 'sasquatch-v4be -no-exit-code -f -d /out /in',
                      '__typename__': 'ExtractCommandFailedReport'}}]
CMD_BESUB = [{'report': {'command': 'sasquatch-v4be -be=1 -f -d /out /in',
                         '__typename__': 'ExtractCommandFailedReport'}}]
CMD_BE = [{'report': {'command': 'sasquatch-v4be -be -f -d /out /in',
                      '__typename__': 'ExtractCommandFailedReport'}}]

CASES = [
    dict(id='K1-be-substring-token',
         kills=['E01', 'I06'],
         e=env(CH_BE, [FAIL_BE], [], CMD_BESUB),
         why='argv token `-be=1` contains -be as a substring but is not the token; '
             'token equality says BE=no (avm-marker-be-dropped), substring says BE=yes '
             '(body-extractor-failure)'),
    dict(id='K2-files-absent',
         kills=['I11', 'E06'],
         e=env(CH_BE, [], [], [], drop_files=True),
         why='normalized_result carries no `files` key at all; the text reads absent as '
             'P=0 (clean-empty), the mutants read absent as P=1 (clean)'),
    dict(id='K3-non-squashfs-handler',
         kills=['I14'],
         e=env(CH_GZIP, [], [], []),
         why='chunks[].handler=gzip only: the interpreter filters H to squashfs* so the '
             '`none` handler row matches (no-squashfs-chunk); accepting every handler '
             'string makes H nonempty and the envelope falls off the table (unclassified)'),
    dict(id='K4-no-argv-na',
         kills=['I19', 'E02'],
         e=env(CH_BE, [FAIL_BE], [], []),
         why='extractor-failure, P=0, handler squashfs_v4_be, but no child argv recorded: '
             'BE=n/a never satisfies step 5 (body-extractor-failure); n/a read as no '
             'reaches step 5 (avm-marker-be-dropped)'),
    dict(id='K5-dep-plus-failure',
         kills=['E08'],
         e=env(CH_BE, [{'kind': 'missing-extractor-dependency',
                        'dependencies': ['sasquatch-v4be']}, FAIL_BE], f(3), CMD_BE),
         why='missing-extractor-dependency AND extractor-failure with P>0: step 3 runs '
             'before step 4, so the pair is dep-missing-be; the swapped order gives '
             'partial-body-failure'),
    dict(id='K6-both-dependencies',
         kills=['E13'],
         e=env(CH_BE, [{'kind': 'missing-extractor-dependency',
                        'dependencies': ['sasquatch', 'sasquatch-v4be']}], [], []),
         why='dependency list names both executables: BE is tested first (dep-missing-be); '
             'LE-first order gives dep-missing-le'),
    dict(id='K7-superset-D-at-exact-row',
         kills=['I02', 'E13b'],
         e=env(CH_BE, [{'kind': 'missing-extractor-dependency',
                        'dependencies': ['sasquatch-v4be', 'unsquashfs']}], [], []),
         why='D is a superset of sasquatch-v4be: the exact dependency cell rejects it '
             '(falls through to unclassified); contains-form dependency matching or a '
             'substring LE test accepts it (dep-missing-be / dep-missing-le)'),
    dict(id='K8-stdout-only-sr',
         kills=['E04'],
         e=env(CH_BE, [], f(3), [],
               raw={'execution': {'stdout': {'text':
                    'WARNING MaliciousSymlinkRemoved link=$output/a target=../b'}}}),
         why='the removal token appears only in raw_result.execution.stdout.text: the '
             'evaluator\'s stdout defence decides SR=yes (escaping-symlink-removed); '
             'without it SR=no (clean)'),
    dict(id='K9-diag-level-typename',
         kills=['E05'],
         e=env(CH_BE, [], f(3), [{'__typename__': 'MaliciousSymlinkRemoved'}]),
         why='the removal typename sits directly on diagnostics[] with no nested report '
             'object: the diag-level holder sees it (escaping-symlink-removed); '
             'report-only holders do not (clean)'),
    dict(id='K10-rawdict-typename',
         kills=['I09'],
         e=env(CH_BE, [], f(3), [],
               raw={'report': [{'reports': [{'__typename__': 'MaliciousSymlinkRemoved'}]}]}),
         why='the removal typename sits in a raw_result dict: the interpreter\'s '
             'raw_result dict scan decides SR=yes (escaping-symlink-removed); without '
             'that scan SR=no (clean).  NOTE: the pristine evaluator does NOT scan '
             'raw_result dicts, so pristine interp and pristine eval DISAGREE here'),
    dict(id='K12-diagnostics-only-sr',
         kills=['I08'],
         e=env(CH_BE, [], f(3), [{'report': {'__typename__': 'MaliciousSymlinkRemoved'}}]),
         why='the removal typename is recorded ONLY in normalized_result.diagnostics[].report '
             'and the envelope carries no raw_result at all (a trimmed envelope): the '
             'diagnostics-report path decides SR=yes (escaping-symlink-removed); a mutant '
             'that misses the __typename__ key falls back on nothing (clean).  All 52 '
             'held-out envelopes carry raw_result with the same token, which is why the '
             'held-out kill check cannot see this path alone'),
    dict(id='K11-p-collapse-demo',
         kills=[],
         e=env(CH_BE, [], f(5), []),
         why='P magnitude demo: I10/E07 collapse P to 0/1; the table grammar and the '
             'counter\'s declared `published` (nonzero/zero) cannot see the difference, '
             'so no pair flips -- unkillable by the frozen kill check'),
]


def main():
    os.makedirs(KILL, exist_ok=True)
    mutant = {}
    for mid in ('I02', 'I06', 'I08', 'I09', 'I11', 'I14', 'I19',
                'E01', 'E02', 'E04', 'E05', 'E06', 'E07', 'E08', 'E13', 'E13b'):
        p = os.path.join(MUT, '%s-%s' % (INTERP, mid))
        if os.path.isfile(p):
            mutant[mid] = (INTERP, p)
        p = os.path.join(MUT, '%s-%s' % (EVAL, mid))
        if os.path.isfile(p):
            mutant[mid] = (EVAL, p)
    rows = []
    for case in CASES:
        path = os.path.join(KILL, case['id'] + '.json')
        with open(path, 'w') as fh:
            json.dump(case['e'], fh, indent=1, sort_keys=True)
        rec = {'id': case['id'], 'why': case['why'], 'envelope': path, 'runs': {}}
        for tool, exe, tag in ((INTERP, os.path.join(PRIM, INTERP), 'interp-pristine'),
                               (EVAL, os.path.join(PRIM, EVAL), 'eval-pristine')):
            pair = interp_pair(exe, path) if tool == INTERP else eval_pair(exe, path)
            rec['runs'][tag] = pair
        for mid in case['kills']:
            tool, exe = mutant[mid]
            tag = '%s-%s' % ('interp' if tool == INTERP else 'eval', mid)
            pair = interp_pair(exe, path) if tool == INTERP else eval_pair(exe, path)
            rec['runs'][tag] = pair
        rows.append(rec)
        print(case['id'])
        for tag, pair in rec['runs'].items():
            print('   %-18s %s' % (tag, pair))
    with open(os.path.join(OUT, 'killcases-out.json'), 'w') as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
