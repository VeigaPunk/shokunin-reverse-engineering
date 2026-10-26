#!/usr/bin/env python3
"""mk-controls.py — emit the R40-C2 pre-freeze shortcut controls (seat R40C2Shortcuts).

Deterministic generator: the candidate table and every control are defined once here and
written out, so a reviewer can rebuild the exact bytes with

    python3 -I -B mk-controls.py --out .

and, once a table is frozen, can regenerate the derived controls from THE FROZEN TABLE:

    python3 -I -B mk-controls.py --from /path/to/frozen-table.md --out DIR

`--from` reads the first markdown table of that file (header + rows) and the vocabulary
line above it, then writes best-table.md (the frozen rows verbatim), CTL-C2-3 (actions
rotated), CTL-C2-4 (domain guard removed), CTL-C2-5 (mixed-symlinks row dropped) and
CTL-C2-6 (a final `*` default row).  CTL-C2-1 (catch-all) and CTL-C2-2 (the v1 table
transcribed) do not depend on the frozen table and are written in both modes.

Outputs:
  best-table.md      the candidate v2 table (reference for CTL-C2-3 / CTL-C2-6)
  CTL-C2-1.md        catch-all: one row matches every envelope
  CTL-C2-2.md        the live v1 table (SKILL.md block 18) transcribed into v2 with
                     `*` operation/provider and the best action per label
  CTL-C2-3.md        best table, actions rotated by one row (label right, action wrong)
  CTL-C2-4.md        best table with the domain guard removed (`*` operation/provider)
  CTL-C2-5.md        best table without the mixed-symlinks row
  CTL-C2-6.md        best table plus a final `*` default row
  probe-shadow.md    grammar probe: a row that can never be the first match (a broader
                     row above a narrower one, unique labels) that the draft grammar still
                     accepts -> argument for a dead-row check
CTL-C2-0 is not generated: it is a byte copy of SKILL.md at the lane base commit
(`git show fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f:SKILL.md`), made in the shell.

Every cause cell carries a ` -> ` tail.  The wave-dispatch grammar does not require one,
but the R40C2Interp interpreter still rejects a cause without it (v1 fossil, reported in
.ufo/waves/round-40/w1/R40C2Shortcuts.md).  Controls stay valid under either reading.
"""

import argparse
import os
import sys

HEADER = ('| label | operation | provider | handler | gap kinds | dependencies | '
          '-be in child argv | symlink removed | published files | action | cause | '
          'source |')
SEP = '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |'

OP = '`extract_firmware`'
PV = '`unblob`'

# Imperative tail for the cause cell: the reader's next move, restated in words (the
# action column stays the machine-scored token).
IMPERATIVE = {
    'no-squashfs-chunk': 'read the magic and superblock before rerunning',
    'dep-missing-be': 'install sasquatch-v4be on the child PATH and rerun into a fresh '
                      'output directory',
    'dep-missing-le': 'install the little-endian sasquatch on the child PATH and rerun',
    'avm-marker-be-dropped': 'rerun through a PATH wrapper that appends -be, then remove '
                             'the wrapper',
    'body-extractor-failure': 'keep the failing command and stderr and diff the carrier '
                              'against a good arm',
    'partial-body-failure': 'salvage the published files and mark the run incomplete',
    'mixed-symlinks': 'expect the removed path absent and count the kept entries '
                      'separately',
    'escaping-symlink-removed': 'expect the path absent and never materialise the link',
    'in-tree-symlink-metadata': 'count one gap per kept entry and install nothing',
    'clean': 'match files to the oracle by relative-path suffix and sha256',
    'clean-empty': 'confirm the oracle tree is empty before accepting the result',
    'any-envelope': 'probe the body by hand before believing the label',
    'escalate': 'read the envelope by hand',
    'be-any': 'read the row below, which is the one that decides',
    'clean-shadow': 'read the row above, which is the one that decides',
}

# (label, operation, provider, handler, gap kinds, dependencies, -be, symlink removed,
#  published files, action, cause prose, source)
BEST_RAW = [
    ('no-squashfs-chunk', OP, PV, '`none`', '`*`', '`*`', '`n/a`', '`*`', '`*`',
     'probe-superblock',
     'no chunk carries a squashfs handler, so no sasquatch of either flavour ran and the '
     'envelope says nothing about endianness, the body or the file set',
     'S112 handler selection; knowledge 2026-10-26-r39-sqfs-outcome-triage.md:50-54; '
     'dev env-magic/env-trunc/env-bytesused (round-39 w1)'),
    ('dep-missing-be', OP, PV, '`squashfs_v4_be`', '`missing-extractor-dependency`',
     '`sasquatch-v4be`', '`n/a`', '`no`', '`*`', 'install-sasquatch-v4be',
     'the big-endian v4 handler resolved its extractor to sasquatch-v4be and that binary '
     'was not resolvable on the child PATH, so no command ran and no -be argument exists '
     'to inspect; the image is unmeasured, not unreadable',
     'S112 lines 68-69; S120 command.py:101-102; dev env-depbe (round-39 w1)'),
    ('dep-missing-le', OP, PV, '`squashfs_v4_le`', '`missing-extractor-dependency`',
     '`sasquatch`', '`n/a`', '`no`', '`*`', 'install-sasquatch',
     'the little-endian v4 handler resolved its extractor to sasquatch and that binary was '
     'not resolvable on the child PATH, so no command ran; the BE binary alone does not '
     'satisfy this gap',
     'S112 lines 68-69; S120 command.py:101-102'),
    ('avm-marker-be-dropped', OP, PV, '`squashfs_v4_be`', '`extractor-failure`', '`none`',
     '`no`', '`no`', '`0`', 'rerun-with-be',
     'mkfs_time equals bytes_used, unblob read the AVM marker and deliberately omitted -be, '
     'so sasquatch-v4be read the body in little-endian mode and failed with nothing '
     'published; this is a marker artefact, not body damage',
     'S112 lines 44-50; dev env-avm (round-39 w1)'),
    ('body-extractor-failure', OP, PV, '`squashfs_v4_*`', '`extractor-failure`', '`none`',
     '`*`', '`no`', '`0`', 'preserve-failing-arm',
     'the extractor ran, published nothing and recorded an extractor-failure gap, and the '
     'marker row above did not explain it (no -be was dropped on a BE body), so the fault '
     'reached the image body or the extractor build in either byte order',
     'S120 report.py:91-98; dev env-inodeptr/env-rootino (round-39 w1)'),
    ('partial-body-failure', OP, PV, '`squashfs_v4_*`', '`extractor-failure`', '`none`',
     '`*`', '`no`', '`>0`', 'salvage-published-files',
     'the extractor recorded an extractor-failure gap only after publishing at least one '
     'regular file, so the envelope is a partial result: the published paths are real '
     'evidence and the absent paths are unexplained, never a clean extraction',
     'R39-CL3 D1; .ufo/waves/round-39/w2/R39W2C2TableReview.md D1 (full-be1-xz, P>0)'),
    ('mixed-symlinks', OP, PV, '`squashfs_v4_*`', '`unpublished-entry`', '`none`',
     '`*`', '`yes`', '`>0`', 'split-mixed-links',
     'one symlink resolved outside the extraction root and was removed with '
     'MaliciousSymlinkRemoved while another stayed in tree as exactly one '
     'unpublished-entry gap; both facts are true at once, so read the removed link as '
     'absent metadata and the kept one as counted metadata',
     'R39-CL2; corpus/evidence/round-39/c1/K5/after.json and K6/after.json; '
     'S118 extractor.py:79-91; S119 FirmwarePublication.js:68-75'),
    ('escaping-symlink-removed', OP, PV, '`squashfs_v4_*`', '`none`', '`*`',
     '`*`', '`yes`', '`>0`', 'verify-link-absence',
     'at least one symlink resolved outside the extraction root and was removed with a '
     'MaliciousSymlinkRemoved report and no gap, and no other in-tree link was kept; expect '
     'the path to be absent and never read the report as body damage',
     'S118 extractor.py:79-91; corpus/evidence/round-39/c1/K1/after.json'),
    ('in-tree-symlink-metadata', OP, PV, '`squashfs_v4_*`', '`unpublished-entry`', '`none`',
     '`*`', '`no`', '`>0`', 'count-metadata-gaps',
     'every symlink resolved inside the extraction root and is retained as metadata, one '
     'unpublished-entry gap per link, with no removed link reported; the gap count is the '
     'link count, not a failure',
     'S119 FirmwarePublication.js:68-75,301-308; corpus/evidence/round-39/c1/K2/after.json'),
    ('clean', OP, PV, '`squashfs_v4_*`', '`none`', '`none`', '`*`', '`no`', '`>0`',
     'match-oracle',
     'every regular file was published, no gap was recorded and no link was removed, so the '
     'envelope carries nothing to fix; match files to the independent oracle by '
     'relative-path suffix and sha256',
     'corpus/evidence/round-39/c1/K3/after.json and K4/after.json; S119'),
    ('clean-empty', OP, PV, '`squashfs_v4_*`', '`none`', '`none`', '`*`', '`no`', '`0`',
     'accept-empty-root',
     'a chunk was handed to the extractor, no gap was recorded and no file was published, so '
     'the image is a clean filesystem whose tree holds no regular file; that is a measured '
     'empty result, not a failed extraction and not an absent chunk',
     'R39-CL3 D2; .ufo/waves/round-39/w2/R39W2C2TableReview.md D2 (full-be-dirempty-gzip)'),
]

VOCAB = ['accept-empty-root', 'count-metadata-gaps', 'install-sasquatch',
         'install-sasquatch-v4be', 'match-oracle', 'probe-superblock',
         'preserve-failing-arm', 'rerun-with-be', 'salvage-published-files',
         'split-mixed-links', 'verify-link-absence']


def arrow(label, cause):
    """Give the cause cell the ` -> ` tail the current interpreter insists on."""
    if '->' in cause:
        return cause
    return '%s -> %s' % (cause, IMPERATIVE.get(label, 'read the envelope by hand'))


def arrowed(rows):
    out = []
    for row in rows:
        row = list(row)
        row[10] = arrow(row[0], row[10])
        out.append(tuple(row))
    return out


BEST = arrowed(BEST_RAW)


def actions_line(tokens):
    return '<!-- sqfs-triage-actions: %s -->' % ' '.join(tokens)


def render(rows, vocab):
    return ('<!-- sqfs-triage-table v2 -->\n' + actions_line(vocab) + '\n' + HEADER + '\n'
            + SEP + '\n' + '\n'.join('| %s |' % ' | '.join(row) for row in rows) + '\n')


def doc(title, note, rows, vocab):
    return ('<!-- %s: generated by mk-controls.py — see .ufo/waves/round-40/w1/'
            'R40C2Shortcuts.md -->\n# %s\n\n%s\n\n## Queue-drain craft\n\n'
            'Control table (v2 grammar, wave-dispatch draft).\n\n%s\n## After the control\n\n'
            'Nothing below the craft section is read by the interpreter.\n'
            % (title, title, note, render(rows, vocab)))


def read_table(path):
    """Return (rows, vocab) of the first markdown table in a SKILL-like file."""
    with open(path, 'r', encoding='utf-8') as handle:
        lines = handle.read().splitlines()

    def cells(line):
        s = line.strip()
        if s.startswith('|'):
            s = s[1:]
        if s.endswith('|'):
            s = s[:-1]
        return [c.strip() for c in s.split('|')]

    start = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith('|') and cells(line)[0].strip('`') == 'label':
            start = i
            break
    if start is None:
        raise SystemExit('%s: no markdown table with a `label` header' % path)
    rows = []
    j = start + 2
    while j < len(lines) and lines[j].lstrip().startswith('|'):
        row = cells(lines[j])
        if len(row) != 12:
            raise SystemExit('%s:%d: %d cells, expected 12' % (path, j + 1, len(row)))
        rows.append(tuple(row))
        j += 1
    vocab = None
    for line in reversed(lines[:start]):
        if '<!-- sqfs-triage-actions:' in line:
            body = line.split('<!-- sqfs-triage-actions:', 1)[1]
            vocab = body.split('-->', 1)[0].split()
            break
    if not vocab:
        vocab = []
        for row in rows:
            if row[9] not in vocab:
                vocab.append(row[9])
    return rows, vocab


def derived_controls(rows, vocab):
    """CTL-C2-3..6 for an arbitrary table (the frozen one, at freeze time)."""
    out = {}
    rotated = []
    for i, row in enumerate(rows):
        nxt = rows[(i + 1) % len(rows)][9]
        rotated.append(tuple(list(row[:9]) + [nxt] + list(row[10:])))
    out['CTL-C2-3.md'] = doc(
        'CTL-C2-3 label-right, action-wrong',
        'The adopted table except that every row carries the action of the next row (a '
        'one-step cyclic rotation; the vocabulary is unchanged and no row is a fixed point '
        'only if no two adjacent rows share a token). Labels stay right, so a counter that '
        'scores only labels passes this control; a counter that scores the (label, action) '
        'pair must fail every in-domain class.', rotated, vocab)
    unguarded = [tuple(list(row[:1]) + ['`*`', '`*`'] + list(row[3:])) for row in rows]
    out['CTL-C2-4.md'] = doc(
        'CTL-C2-4 table without the domain guard',
        'The adopted table except that the two domain columns are `*` on every row, i.e. '
        'the R39-CL1 state with v2 rows. In-domain classes are decided exactly as in the '
        'adopted table; a non-`extract_firmware` or non-`unblob` envelope is decided by its '
        'squashfs-shaped features instead of falling through.', unguarded, vocab)
    nomixed = [row for row in rows if row[0].strip('`') != 'mixed-symlinks']
    if len(nomixed) == len(rows):
        raise SystemExit('CTL-C2-5: the source table has no `mixed-symlinks` row')
    out['CTL-C2-5.md'] = doc(
        'CTL-C2-5 table without the mixed-symlinks row',
        'The adopted table with the `mixed-symlinks` row removed and every other byte kept. '
        'A carrier holding one in-tree and one escaping link (one `unpublished-entry` gap '
        'plus `MaliciousSymlinkRemoved`) must then refuse, borrow the escaping row, or '
        'borrow the in-tree row, depending on how tightly the remaining rows are cut.',
        nomixed, vocab)
    default_row = ('escalate', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`',
                   'inspect-manually',
                   arrow('escalate', 'no earlier row decided this envelope, so a human '
                                     'reads it; the row claims nothing about the carrier'),
                   'CTL-C2-6 default row (R40-C2 kill control)')
    out['CTL-C2-6.md'] = doc(
        'CTL-C2-6 adopted table plus a `*` default row',
        'The adopted table unchanged, followed by one final row whose every condition cell '
        'is `*` and whose action has its own vocabulary token. Every in-domain class keeps '
        'the adopted decision; the row exists only to convert the honest no-match result '
        '(`unclassified`, `none`) into an answer, and it does that for any envelope the '
        'guard was supposed to reject.', list(rows) + [default_row],
        list(vocab) + ([] if 'inspect-manually' in vocab else ['inspect-manually']))
    return out


def static_controls():
    """Controls that do not depend on the adopted table (v1 transcription, catch-all)."""
    out = {}
    catch = arrowed([
        ('any-envelope', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`',
         'probe-superblock',
         'every envelope, in domain or not, resolves to this row; the table states a '
         'decision it cannot have measured',
         'CTL-C2-1 catch-all (R40-C2 kill control)')])
    out['CTL-C2-1.md'] = doc(
        'CTL-C2-1 catch-all',
        'One row whose every condition cell is `*`, a unique label and a legal action. The '
        'weakest table that still parses: it answers `any-envelope` to every class, so a '
        'counter that scores only "an answer was produced" passes it while every held-out '
        'class is wrong.', catch, ['probe-superblock'])

    v1 = [
        ('no-squashfs-chunk', '`*`', '`*`', '`none`', '`*`', '`*`', '`n/a`', '`*`', '`*`',
         'probe-superblock',
         "no chunk carries a squashfs handler: unblob's finder dropped a truncated image, a "
         "`bytes_used` past the end or a non-4 `s_major` without a report -> check the magic "
         "and superblock before rerunning; an empty envelope is not an empty filesystem",
         'knowledge entry :50-54'),
        ('dep-missing-be', '`*`', '`*`', '`squashfs_v4_be`', '`missing-extractor-dependency`',
         '`sasquatch-v4be`', '`n/a`', '`no`', '`*`', 'install-sasquatch-v4be',
         'the big-endian handler needed sasquatch-v4be and it was not on the unblob child '
         'PATH -> put the sasquatch-v4be 4.5.1 binary on that PATH and rerun into a fresh '
         'output directory; the image is unmeasured, not unreadable',
         'S112 lines 68-69; S120 command.py:101-102'),
        ('dep-missing-le', '`*`', '`*`', '`squashfs_v4_le`', '`missing-extractor-dependency`',
         '`sasquatch`', '`n/a`', '`no`', '`*`', 'install-sasquatch',
         'the little-endian handler needed plain sasquatch and it was not on the child PATH '
         '-> put sasquatch on that PATH and rerun; sasquatch-v4be alone does not satisfy '
         'this gap; an AppImage before-arm still publishes its ELF prefix and the opaque '
         'container range',
         'S112 lines 68-69; S120 command.py:101-102'),
        ('avm-marker-be-dropped', '`*`', '`*`', '`squashfs_v4_be`', '`extractor-failure`',
         '`none`', '`no`', '`no`', '`0`', 'rerun-with-be',
         'mkfs_time equals bytes_used, unblob read the AVM marker and omitted -be, so '
         'sasquatch-v4be read a standard-BE body with the wrong byte order -> do not treat '
         'it as damage; rerun through a PATH wrapper named sasquatch-v4be that appends -be '
         '(REA has no flag passthrough)',
         'S112 lines 44-50; S121'),
        ('body-extractor-failure', '`*`', '`*`', '`squashfs_v4_be`', '`extractor-failure`',
         '`none`', '`yes`', '`no`', '`0`', 'preserve-failing-arm',
         'the extractor ran with -be and still failed, so the image body or header is '
         'damaged -> keep the failing command and stderr from diagnostics, compare against '
         'a known-good carrier, never patch the envelope into a success',
         'S120 report.py:91-98; knowledge entry :29-40'),
        ('escaping-symlink-removed', '`*`', '`*`', '`squashfs_v4_*`', '`*`', '`*`',
         '`n/a`', '`yes`', '`>0`', 'verify-link-absence',
         'a symlink target resolved outside the extraction root; unblob removed it and '
         'reported MaliciousSymlinkRemoved, and REA records no gap for it -> expect the path '
         'to be absent; never materialise the link or match it against the regular-file '
         'oracle',
         'S118 extractor.py:79-91'),
        ('in-tree-symlink-metadata', '`*`', '`*`', '`squashfs_v4_*`', '`unpublished-entry`',
         '`none`', '`n/a`', '`no`', '`>0`', 'count-metadata-gaps',
         'a symlink target resolved inside the extraction root; it is kept as metadata and '
         'recorded as one unpublished-entry gap per link -> expected, not a failure; count '
         'one gap per in-tree link and publish nothing for it',
         'S119 FirmwarePublication.js:68-75,301-308'),
        ('clean', '`*`', '`*`', '`squashfs_v4_*`', '`none`', '`none`', '`n/a`', '`no`',
         '`>0`', 'match-oracle',
         'every regular file was published, no gap was recorded and no symlink was removed '
         '-> nothing to fix; match files to an oracle by relative-path suffix and sha256',
         'S119; knowledge entry :11-19'),
    ]
    out['CTL-C2-2.md'] = doc(
        'CTL-C2-2 v1 table transcribed into v2',
        'The live v1 table of `SKILL.md` block 18 (rows and cells taken verbatim from '
        'SKILL.md:333-343 at the lane base) with the two domain columns added as `*` and the '
        'decision moved into the action column. This is the "port the old table and call it '
        'v2" shortcut: every v1 row survives, none of the three routed v2 defects (R39-CL1 '
        'domain guard, R39-CL2 mixed links, R39-CL3 P>0 / P=0) is repaired.', v1,
        ['count-metadata-gaps', 'install-sasquatch', 'install-sasquatch-v4be',
         'match-oracle', 'preserve-failing-arm', 'probe-superblock', 'rerun-with-be',
         'verify-link-absence'])
    return out


def shadow_probe():
    rows = arrowed([
        ('be-any', OP, PV, '`squashfs_v4_*`', '`*`', '`*`', '`*`', '`*`', '`*`',
         'match-oracle',
         'anything the big-endian-or-little-endian v4 handler produced, with or without gaps',
         'probe-shadow row 1 (broader)'),
        ('clean-shadow', OP, PV, '`squashfs_v4_*`', '`none`', '`none`', '`*`', '`no`',
         '`>0`', 'match-oracle',
         'a clean extraction; unreachable, because row 1 already matches every envelope row '
         '2 could match',
         'probe-shadow row 2 (narrower, dead)'),
    ])
    return doc(
        'probe-shadow (grammar probe, not a kill control)',
        'Two rows: row 1 is strictly broader than row 2, labels are unique, every cell and '
        'the action are legal. The draft grammar accepts this file (exit 0) even though row '
        '2 can never be the first match, so a table can carry a first-match order that its '
        'author believes is a decision order while one row is dead. Used only to argue for a '
        'dead-row check; it is not part of the kill-control set.', rows, VOCAB)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--from', dest='source',
                        help='regenerate the derived controls from this table file')
    parser.add_argument('--out', default=os.path.dirname(os.path.abspath(__file__)),
                        help='output directory (default: this artifact directory)')
    ns = parser.parse_args(argv)
    out_dir = os.path.abspath(ns.out)
    os.makedirs(out_dir, exist_ok=True)
    files = static_controls()
    if ns.source:
        rows, vocab = read_table(os.path.abspath(ns.source))
        files['best-table.md'] = doc(
            'best-table (verbatim copy of %s)' % os.path.basename(ns.source),
            'Rows and vocabulary copied byte-for-byte from the table named in this header, '
            'so the derived controls differ from the adopted table in exactly one dimension '
            'each.', rows, vocab)
        files.update(derived_controls(rows, vocab))
    else:
        files['best-table.md'] = doc(
            'best-table (candidate v2 table, not a control)',
            'The candidate table the controls are derived from. Eleven unique labels, one '
            'row per outcome the draft claims, domain guard as an exact '
            '`extract_firmware`/`unblob` prefix on every row. Row order: absent chunk, '
            'dependency misses, marker artefact, fatal body failure, partial body failure, '
            'mixed links, escaping link, in-tree link, clean, clean-empty.', BEST, VOCAB)
        files.update(derived_controls(BEST, VOCAB))
    files['probe-shadow.md'] = shadow_probe()
    for name, text in files.items():
        with open(os.path.join(out_dir, name), 'w', encoding='utf-8') as handle:
            handle.write(text)
    print('wrote %d files to %s: %s'
          % (len(files), out_dir, ' '.join(sorted(files))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
