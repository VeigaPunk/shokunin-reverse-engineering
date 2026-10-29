#!/usr/bin/env python3
"""ExecB1Impact: build the FULL simulated attempt-2 landing (capstone fixture).

Everything the L1's landing order says:
  1. C3 instrument at tools/round-50-c3/sqfs-triage-v5.py + its instrument-registry v2 row
  2. SKILL.md rule block 22 (triage table v5)
  3. C1 entry corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md
     PROVINCE.md '## Round-50 additions to Core' + frontier note
     corpus/README.md coverage-map row
     SOURCES rows S243/S244/S245/S249 (11 cells, opened 2026-10-28)
     SCORECARD Owned-axes coverage head 140/140 + attempt-2 section BEFORE the corrections section
  4. corrections section stays LAST in SCORECARD.md
"""
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
STEM = '2026-10-28-r50-avm-le-squashfs-core'
INSTR = 'tools/round-50-c3/sqfs-triage-v5.py'
CORR_HEAD = '## Record corrections — round 50'


def git(clone, *args, check=True):
    p = subprocess.run(['git', '-C', clone] + list(args), capture_output=True)
    if check and p.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(args), p.stderr.decode()[:400]))
    return p.stdout.decode('utf-8', 'replace')


def write(clone, path, text):
    fp = os.path.join(clone, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w') as fh:
        fh.write(text)


def read(clone, path):
    return git(clone, 'show', 'HEAD:' + path)


def commit(clone, msg):
    git(clone, 'add', '-A', '--', '.')
    p = subprocess.run(['git', '-C', clone, 'commit', '-q', '-m', msg], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.decode()[:400])
    return git(clone, 'rev-parse', 'HEAD').strip()


def registry_row():
    return (
        '| `%s` | gate — R50-C3 depth: the SKILL rule block 22 triage table v5 scored against the '
        'frozen independent evaluator over the round-42 recon envelope corpus (table label and '
        'action against evaluator label and action, pair_mismatches, evaluator_missing, the '
        'committed mutation battery), run as `python3 -I -B %s --root LANE --rev REV --freeze '
        'FREEZE --envelopes DIR --json-out OUT` | 0=met, every envelope\'s table label and action '
        'equal the evaluator\'s, pair_mismatches 0 and evaluator_missing 0 at --rev, and the '
        'committed mutation battery green; 1=not met, a named envelope pair mismatch or a false '
        'binding, the receipt still written; 2=could-not-evaluate, bad arguments, unknown revision, '
        'frozen_path_changed, a refused read or an unhandled exception | python3 -I -B %s --selftest '
        '— the case count and the exit code are recorded in the freeze receipt | '
        '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ | --json-out only; scratch '
        'under --work | kaidoku |' % (INSTR, INSTR, INSTR))


def sources_rows():
    meta = [('S243', 'Freetz AVM_LE/AVM_BE patch definition',
             'https://github.com/Freetz/Freetz/blob/master/uci/luci/firmware/avm.patch',
             'the AVM_LE/AVM_BE layout definition'),
            ('S244', 'AVM firmware download index', 'https://download.avm.de/fritzbox/',
             'the four FRITZ!OS image URLs'),
            ('S245', 'unblob 26.6.4 SquashFS little-endian handler',
             'https://github.com/onekey-sec/unblob/blob/26.6.4/unblob/handlers/filesystem/squashfs.py',
             'the squashfs_v4_le handler'),
            ('S249', 'AVM firmware licence terms', 'https://download.avm.de/',
             'the non-redistribution condition')]
    out = []
    for sid, what, url, scope in meta:
        out.append(
            '| %s | %s — %s | docs | A | %s only | "the round-50 census records 28 hsqs LE AVM member '
            'rows across 16 models" (12 words); snapshot `corpus/evidence/round-50/c1/index/README.md`, '
            'sha256 `%s` | the round-50 LE AVM member census and the frozen handler family | mined | '
            '2026-10-28 | 365d | `%s` |'
            % (sid, what, url, scope, '0' * 64, ENTRY))
    return '\n'.join(out)


def entry_text():
    return (
        '# %s — AVM-marker little-endian SquashFS v4 through REA extract-firmware\n\n'
        'State: Core.  Four FRITZ!OS images, chain-pinned, each carved to its superblock '
        '`bytes_used`.\n\n'
        '- handler: `squashfs_v4_le`\n'
        '- marker: the AVM marker (`mkfs_time == bytes_used`) — an empirical constant of these '
        'four pinned members, not an origin proof\n\n'
        'source: S243 S244 S245 S249\n\n'
        'used-by: `%s`\n' % (STEM, ENTRY))


def main():
    work = sys.argv[1]
    clone = os.path.join(work, 'final-landing')
    subprocess.run(['git', 'clone', '--shared', '-q', LANE, clone], check=True)
    git(clone, 'checkout', '-q', '--detach', BASE)
    git(clone, 'config', 'user.name', 'c2-impact-seat')
    git(clone, 'config', 'user.email', 'c2-impact-seat@invalid')
    git(clone, 'config', 'commit.gpgsign', 'false')

    # 1. the C3 instrument + its registry row + SKILL rule block 22
    write(clone, INSTR, '#!/usr/bin/env python3\n"""C3 triage v5 instrument (simulated)."""\n')
    sk = read(clone, 'SKILL.md')
    sk = sk.replace('<!-- /instrument-registry -->', registry_row() + '\n<!-- /instrument-registry -->', 1)
    sk = sk.rstrip('\n') + (
        '\n\n### Rule block 22 — SquashFS triage table v5 (round 50, C3)\n\n'
        '| handler family | independent reader | label | action |\n'
        '|---|---|---|---|\n'
        '| `squashfs_v2_nonstandard` | none | clean-unverified | record-unverified |\n'
        '| `squashfs_v3_broadcom` | none | clean-unverified | record-unverified |\n'
        '| `squashfs_v3_nonstandard` | none | clean-unverified | record-unverified |\n')
    write(clone, 'SKILL.md', sk)

    # 2. the C1 entry
    write(clone, ENTRY, entry_text())

    # 3. README coverage-map row (backticked stem)
    rd = read(clone, 'corpus/README.md')
    i = rd.find('\n## ', rd.find('## Coverage map') + 5)
    row = ('\n| AVM LE SquashFS v4 | `%s` | Core — four chain-pinned FRITZ!OS members through REA '
           'extract-firmware (`squashfs_v4_le`) |\n' % STEM)
    write(clone, 'corpus/README.md', rd[:i] + row + rd[i:])

    # 4. SOURCES rows
    soc = read(clone, 'corpus/SOURCES.md').rstrip('\n')
    write(clone, 'corpus/SOURCES.md', soc + '\n' + sources_rows() + '\n')

    # 5. PROVINCE
    pv = read(clone, 'PROVINCE.md').rstrip('\n')
    pv += (
        '\n\n## Round-50 additions to Core\n\n'
        '| handler | marker | entry |\n|---|---|---|\n'
        '| `squashfs_v4_le` | AVM marker (mkfs_time == bytes_used) | `%s` |\n'
        '\nRound-50 frontier note — `%s`: LE AVM members of four FRITZ!OS images are Core.\n'
        % (ENTRY, STEM))
    write(clone, 'PROVINCE.md', pv)

    # 6. SCORECARD: coverage head + attempt-2 section BEFORE the corrections section
    sc = read(clone, 'SCORECARD.md')
    old = '139/139 knowledge files mapped at the round-50 landing'
    new = ('140/140 knowledge files mapped at the round-50 attempt-2 landing (the round-50 attempt-1 '
           'landing read 139/139; the attempt-2 C1 entry `%s` made it 140)' % STEM)
    assert old in sc
    sc = sc.replace(old, new, 1)
    att2 = ('## Round 50 attempt 2 — resumed C1 under the same frozen bytes, C3 depth added\n\n'
            'Base `f890bbead20ca2c549487167f56876ae47f1e1a4`.  The C1 freeze `435d41fd` is unchanged.\n')
    i = sc.find(CORR_HEAD)
    assert i > 0
    sc = sc[:i] + att2 + '\n' + sc[i:]
    write(clone, 'SCORECARD.md', sc)

    print(commit(clone, 'simulated attempt-2 landing (final shape)'))


if __name__ == '__main__':
    main()
