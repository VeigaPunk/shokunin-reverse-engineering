#!/usr/bin/env python3
"""ExecB1Impact: build a SIMULATED attempt-2 landing in a fixture clone of the lane.

Read-only w.r.t. the lane: the clone is `git clone --shared` of the lane, all writes
happen inside the clone.  The script never touches the lane tree.

Usage: mklanding.py CLONE MODE
  MODE = inside  : C3 instrument at tools/round-50/sqfs-triage-v5.py  (as the
                   attempt-2 claims name it) + full C1/C3 landing text
         outside : same landing, C3 instrument at tools/round-50-c3/sqfs-triage-v5.py
         minimal : only the knowledge entry + coverage head (no C3 instrument)
"""
import os
import re
import subprocess
import sys

ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
STEM = '2026-10-28-r50-avm-le-squashfs-core'
INSTR_IN = 'tools/round-50/sqfs-triage-v5.py'
INSTR_OUT = 'tools/round-50-c3/sqfs-triage-v5.py'


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


def entry_text():
    return (
        '# %s — AVM-marker little-endian SquashFS v4 through REA extract-firmware\n\n'
        'State: Core.  Four FRITZ!OS images, chain-pinned, carved to bytes_used.\n\n'
        '- handler: `squashfs_v4_le`\n'
        '- marker: AVM marker (mkfs_time == bytes_used)\n\n'
        'source: S243 S244 S245 S249\n\n'
        'used-by: `%s`\n' % (STEM, ENTRY))


def sources_rows():
    rows = []
    meta = [('S243', 'Freetz AVM_LE/AVM_BE patch definition',
             'https://github.com/Freetz/Freetz/blob/master/uci/luci/firmware/avm.patch'),
            ('S244', 'AVM firmware download index',
             'https://download.avm.de/fritzbox/'),
            ('S245', 'unblob 26.6.4 SquashFS little-endian handler',
             'https://github.com/onekey-sec/unblob/blob/26.6.4/unblob/handlers/filesystem/squashfs.py'),
            ('S249', 'AVM firmware licence terms',
             'https://download.avm.de/')]
    for sid, what, url in meta:
        rows.append(
            '| %s | %s — %s | docs | A | the %s claim only | "the round-50 LE AVM member census '
            'records 28 hsqs rows" (10 words); snapshot `corpus/evidence/round-50/c1/index/README.md`, '
            'sha256 `%s` | %s | mined | 2026-10-28 | 365d | `%s` |'
            % (sid, what, url, what, '0' * 64, what, ENTRY))
    return '\n'.join(rows)


def registry_row(instr):
    return (
        '| `%s` | gate — R50-C3 depth: triage table v5 of SKILL.md rule block 22 (no independent '
        'reader families clean-unverified / no-reader-failure) scored against the round-42 recon '
        'envelope corpus | 0=met, every pair matched and no evaluator was missing; 1=not met, a pair '
        'mismatch or a missing evaluator; 2=could-not-evaluate, bad arguments or a refused read | '
        'python3 -I -B %s --selftest — 12 cases, exit 0 on 2026-10-29 | SKILL.md rule block 22 and the '
        'round-42 envelope corpus | --json-out only; scratch under --work | kaidoku |'
        % (instr, instr))


def skill_block22():
    return (
        '### Rule block 22 — SquashFS triage table v5 (round 50, C3)\n\n'
        '| handler family | independent reader | label | action |\n'
        '|---|---|---|---|\n'
        '| `squashfs_v2_nonstandard` | none | clean-unverified | record-unverified |\n'
        '| `squashfs_v3_broadcom` | none | clean-unverified | record-unverified |\n'
        '| `squashfs_v3_nonstandard` | none | clean-unverified | record-unverified |\n'
        '| `squashfs_v2_nonstandard` | none | no-reader-failure | preserve-unresolved |\n')


def main():
    clone, mode = sys.argv[1], sys.argv[2]
    top = git(clone, 'rev-parse', '--show-toplevel').strip()
    assert os.path.realpath(top) == os.path.realpath(clone), top
    instr = INSTR_IN if mode == 'inside' else INSTR_OUT

    # 1. the C1 knowledge entry
    write(clone, ENTRY, entry_text())

    # 2. README coverage-map row (backticked stem)
    rd = read(clone, 'corpus/README.md')
    i = rd.find('\n## ', rd.find('## Coverage map') + 5)
    row = ('\n| AVM LE SquashFS v4 | `%s` | Core — four chain-pinned FRITZ!OS members through REA '
           'extract-firmware (`squashfs_v4_le`) |\n' % STEM)
    write(clone, 'corpus/README.md', rd[:i] + row + rd[i:])

    # 3. SCORECARD: coverage head + an attempt-2 section (appended at EOF)
    sc = read(clone, 'SCORECARD.md')
    old = '139/139 knowledge files mapped at the round-50 landing'
    new = ('140/140 knowledge files mapped at the round-50 attempt-2 landing '
           '(the round-50 attempt-1 landing read 139/139; the C1 entry `%s` made it 140)' % STEM)
    assert old in sc
    sc = sc.replace(old, new, 1)
    sc = sc.rstrip('\n') + (
        '\n\n## Round 50 attempt 2 — resumed C1 under the same frozen bytes, C3 depth added\n\n'
        'Base `f890bbead20ca2c549487167f56876ae47f1e1a4`.  The C1 freeze `435d41fd` is unchanged.\n')
    write(clone, 'SCORECARD.md', sc)

    # 4. SOURCES rows S243-S245/S249
    soc = read(clone, 'corpus/SOURCES.md').rstrip('\n')
    write(clone, 'corpus/SOURCES.md', soc + '\n' + sources_rows() + '\n')

    # 5. PROVINCE round-50 section + frontier note
    pv = read(clone, 'PROVINCE.md').rstrip('\n')
    pv += (
        '\n\n## Round-50 additions to Core\n\n'
        '| handler | marker | entry |\n'
        '|---|---|---|\n'
        '| `squashfs_v4_le` | AVM marker (mkfs_time == bytes_used) | `%s` |\n'
        '\nRound-50 frontier note — `%s`: LE AVM members of four FRITZ!OS images are Core.\n'
        % (ENTRY, STEM))
    write(clone, 'PROVINCE.md', pv)

    # 6. SKILL: rule block 22 + the instrument's registry row
    sk = read(clone, 'SKILL.md')
    sk = sk.replace('<!-- /instrument-registry -->', registry_row(instr) +
                    '\n<!-- /instrument-registry -->', 1)
    sk = sk.rstrip('\n') + '\n\n' + skill_block22()
    write(clone, 'SKILL.md', sk)

    # 7. the C3 instrument itself
    write(clone, instr, '#!/usr/bin/env python3\n"""C3 triage v5 instrument (stub for the '
                         'coupling experiment)."""\n')

    git(clone, 'add', '-A', '--', '.')
    p = subprocess.run(['git', '-C', clone, 'commit', '-q', '-m',
                        'simulated attempt-2 landing (%s)' % mode], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.decode()[:400])
    print(git(clone, 'rev-parse', 'HEAD').strip())


if __name__ == '__main__':
    main()
