#!/usr/bin/env python3
"""make-controls.py - build the R41-C2 control tables in the draft v3 grammar.

Inputs (read-only):
  * the base SKILL.md bytes at the lane base 49096c7e (marker v2 + 11-row table),
  * nothing else: every control is a mechanical transformation of that block or a
    hand-written row list that implements the `**Label precedence**` list of
    plans/round-41-claims.md.

Outputs: one SKILL-shaped document per control in --out, each carrying
`## Queue-drain craft`, the `<!-- sqfs-triage-table v3 -->` marker (except CTL-C2-0),
the `<!-- sqfs-triage-actions: ... -->` line and a 12-column table.

Cell grammar used here (R41C2Interp contract): exact set = bare member list (this
generator only ever emits SINGLE-member exact sets, so it is portable across a
comma-separated and a plus-separated exact form), contains = member list ending in
`+`, plus `none` and `*`.
"""

import argparse
import hashlib
import json
import os
import re
import sys

MARKER_V2 = '<!-- sqfs-triage-table v2 -->'
MARKER_V3 = '<!-- sqfs-triage-table v3 -->'
ACTIONS = ('none inspect-input install-extractor-be install-extractor-le '
           'wrap-extractor-be preserve-failure salvage-partial audit-symlinks '
           'expect-link-absent count-gap confirm-empty raise-depth')
HEADER = ['label', 'operation', 'provider', 'handler', 'gap kinds', 'dependencies',
          '-be in child argv', 'symlink removed', 'published files', 'action', 'cause',
          'source']


def sha256_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def clean(cell):
    s = cell.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        s = s[1:-1].strip()
    return s


def read_v2_block(skill_text):
    """Return (rows, raw_lines) of the v2 table block in one SKILL.md."""
    lines = skill_text.splitlines()
    try:
        at = [i for i, line in enumerate(lines) if MARKER_V2 in line][0]
    except IndexError:
        raise SystemExit('no v2 marker in the given SKILL.md')
    raw = [lines[at]]
    i = at + 1
    while i < len(lines) and (lines[i].lstrip().startswith('<!-- sqfs-triage-actions:')
                              or lines[i].lstrip().startswith('|')):
        raw.append(lines[i])
        i += 1
    table = [line for line in raw if line.lstrip().startswith('|')]
    if len(table) < 3:
        raise SystemExit('v2 block has no header/separator/rows')
    rows = []
    for line in table[2:]:
        cells = [clean(c) for c in split_row(line)]
        if len(cells) != len(HEADER):
            raise SystemExit('v2 row has %d cells: %r' % (len(cells), line[:80]))
        rows.append(cells)
    return rows, raw


def fmt_row(cells):
    out = [cells[0]]
    out.extend('`%s`' % c for c in cells[1:10])
    out.extend(cells[10:])
    return '| ' + ' | '.join(out) + ' |'


def fmt_block(rows, marker=MARKER_V3, actions=ACTIONS):
    out = [marker, '<!-- sqfs-triage-actions: %s -->' % actions,
           '| ' + ' | '.join(HEADER) + ' |',
           '| ' + ' | '.join(['---'] * len(HEADER)) + ' |']
    out.extend(fmt_row(row) for row in rows)
    return '\n'.join(out) + '\n'


def skill_doc(title, note, block):
    return ('# %s\n\n%s\n\n'
            'Control data for the R41-C2 control score. The interpreter reads only the '
            'craft section below; this page and its comments are not instructions.\n\n'
            '## Queue-drain craft\n\n%s' % (title, note, block))


def rotate_actions(rows, keep=('unclassified',)):
    """Rotate the action cell of every row by one (no fixed points for distinct ids)."""
    actions = [row[9] for row in rows]
    shifted = actions[1:] + actions[:1]
    assert all(a != b for a, b in zip(actions, shifted)), 'rotation has a fixed point'
    out = []
    for row, act in zip(rows, shifted):
        new = list(row)
        new[9] = act
        out.append(new)
    return out


def strip_contains(rows):
    out = []
    for row in rows:
        new = list(row)
        for idx in (4, 5):
            cell = new[idx]
            if cell not in ('*', 'none') and cell.endswith('+'):
                new[idx] = cell[:-1]
        out.append(new)
    return out


V2_ACTIONS_LINE = ACTIONS.replace(' raise-depth', '')


def ref_rows(v2_rows):
    """Rows implementing the 12-step `**Label precedence**` list, first match wins."""
    cause = {row[0]: row[10] for row in v2_rows}
    source = {row[0]: row[11] for row in v2_rows}
    rows = [
        # step 2
        ['no-squashfs-chunk', 'extract_firmware', 'unblob', 'none', '*', '*', '*', '*', '*',
         'inspect-input', cause['no-squashfs-chunk'], source['no-squashfs-chunk']],
        # step 3, be flavour
        ['dep-missing-be', 'extract_firmware', 'unblob', 'squashfs_v4_be',
         'missing-extractor-dependency+', 'sasquatch-v4be+', '*', '*', '*',
         'install-extractor-be', cause['dep-missing-be'], source['dep-missing-be']],
        # step 3, le flavour
        ['dep-missing-le', 'extract_firmware', 'unblob', 'squashfs_v4_le',
         'missing-extractor-dependency+', 'sasquatch+', '*', '*', '*',
         'install-extractor-le', cause['dep-missing-le'], source['dep-missing-le']],
        # step 4 (before the symlink and depth steps)
        ['partial-body-failure', 'extract_firmware', 'unblob', 'squashfs_v4_*',
         'extractor-failure+', '*', '*', '*', '>0', 'salvage-partial',
         cause['partial-body-failure'] + '; a combined gap set that also holds '
         'unpublished-entry or depth-limited never leaves this row',
         source['partial-body-failure'] + '; plans/round-41-claims.md precedence step 4'],
        # step 5
        ['avm-marker-be-dropped', 'extract_firmware', 'unblob', 'squashfs_v4_be',
         'extractor-failure+', '*', 'no', '*', '0', 'wrap-extractor-be',
         cause['avm-marker-be-dropped'], source['avm-marker-be-dropped']],
        # step 6
        ['body-extractor-failure', 'extract_firmware', 'unblob', 'squashfs_v4_*',
         'extractor-failure+', '*', '*', '*', '0', 'preserve-failure',
         cause['body-extractor-failure'], source['body-extractor-failure']],
        # step 7 (before steps 8-10 on purpose)
        ['depth-limited-nested', 'extract_firmware', 'unblob', 'squashfs_v4_*',
         'depth-limited+', '*', '*', '*', '*', 'raise-depth',
         'the extraction stopped at the depth ceiling and REA recorded a depth-limited '
         'gap for a nested carved image, so the outer tree is published and the inner '
         'one is unmeasured -> raise --max-depth and rerun into a fresh output '
         'directory; in-tree and escaped symlinks ride along and do not change this '
         'label',
         'plans/round-41-claims.md precedence step 7; REA 6.5.0 '
         'dist/cli-runtime/cli.js :14273 depth-limited gap from '
         'normalized.depth_limited_paths (:14867); :14236 ceilingReached'],
        # step 8
        ['mixed-symlinks', 'extract_firmware', 'unblob', 'squashfs_v4_*',
         'unpublished-entry+', '*', '*', 'yes', '*', 'audit-symlinks',
         cause['mixed-symlinks'], source['mixed-symlinks']],
        # step 9
        ['escaping-symlink-removed', 'extract_firmware', 'unblob', 'squashfs_v4_*',
         'none', '*', '*', 'yes', '*', 'expect-link-absent',
         cause['escaping-symlink-removed'], source['escaping-symlink-removed']],
        # step 10 (exact set: precedence names G = {unpublished-entry})
        ['in-tree-symlink-metadata', 'extract_firmware', 'unblob', 'squashfs_v4_*',
         'unpublished-entry', '*', '*', '*', '*', 'count-gap',
         cause['in-tree-symlink-metadata'], source['in-tree-symlink-metadata']],
        # step 11, P > 0
        ['clean', 'extract_firmware', 'unblob', 'squashfs_v4_*', 'none', '*', '*', '*',
         '>0', 'none', cause['clean'], source['clean']],
        # step 11, P = 0
        ['clean-empty', 'extract_firmware', 'unblob', 'squashfs_v4_*', 'none', '*', '*',
         '*', '0', 'confirm-empty', cause['clean-empty'], source['clean-empty']],
    ]
    return rows


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-skill', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--manifest')
    ns = ap.parse_args(argv)
    text = open(ns.base_skill, 'r', encoding='utf-8').read()
    v2_rows, v2_raw = read_v2_block(text)
    base_sha = hashlib.sha256(open(ns.base_skill, 'rb').read()).hexdigest()
    os.makedirs(ns.out, exist_ok=True)
    written = []

    def emit(name, title, note, block):
        path = os.path.join(ns.out, name)
        doc = skill_doc(title, note, block)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(doc)
        written.append({'file': name, 'sha256': sha256_text(doc),
                        'marker': block.splitlines()[0] if block else None,
                        'rows': len([l for l in block.splitlines()
                                     if l.startswith('| `')])})
        return path

    # CTL-C2-0: the base document itself, byte for byte (no v3 marker anywhere).
    with open(os.path.join(ns.out, 'CTL-C2-0-base-SKILL.md'), 'w',
              encoding='utf-8') as handle:
        handle.write(text)
    written.append({'file': 'CTL-C2-0-base-SKILL.md', 'sha256': base_sha,
                    'marker': None, 'rows': 0})

    # CTL-C2-1: one all-star row, all twelve cells starred except label and action.
    # `clean`/`none` is the label a guessing table would most like to reach (it is the
    # largest class family), and it is the only pair a single row can pick that scores
    # more than the out-of-domain class.
    emit('CTL-C2-1-catch-all.skill.md', 'CTL-C2-1 catch-all (one `*` row)',
         'A single row with every feature cell `*`, including operation and provider: '
         'it accepts every envelope, so it cannot encode any precedence step and it '
         'also erases the domain guard of step 1.',
         fmt_block([['clean', '*', '*', '*', '*', '*', '*', '*', '*',
                     'none',
                     'every envelope is labelled clean because no cell constrains '
                     'anything -> nothing is inspected, no gap is counted and no '
                     'endianness handshake is considered',
                     'control only: no source, this row is a deliberate shortcut']]))

    # CTL-C2-2: the round-40 v2 block verbatim, marker swapped for v3.
    verbatim_block = fmt_block(v2_rows, actions=V2_ACTIONS_LINE)
    for line in v2_raw:
        if line.lstrip().startswith('<!-- sqfs-triage-actions:'):
            assert line.strip() in verbatim_block, 'actions line not preserved'
            break
    emit('CTL-C2-2-v2-verbatim.skill.md',
         'CTL-C2-2 the round-40 v2 table transcribed into the v3 marker',
         'Byte-identical rows and actions line to SKILL.md rule block 19 at '
         '49096c7e; only the marker line differs. No contains row, no depth row.',
         verbatim_block)

    ref = ref_rows(v2_rows)
    ref_block = fmt_block(ref)
    emit('CTL-C2-REF-precedence.skill.md',
         'CTL-C2-REF positive reference: the precedence list encoded in v3 grammar',
         'Not a control against the claim: the row set a correct v3 table must reach. '
         'Order follows **Label precedence** 1-12 (step 1 is structural: every row '
         'names extract_firmware/unblob, so a domain mismatch falls to the default).',
         ref_block)

    # CTL-C2-3: the reference row set with the action cells rotated by one.
    emit('CTL-C2-3-actions-rotated.skill.md',
         'CTL-C2-3 reference rows, action column rotated by one',
         'Every label and every feature cell is the reference table; only the action '
         'cells are shifted one row up, so the rotation has no fixed point.',
         fmt_block(rotate_actions(ref)))
    emit('CTL-C2-3b-v2-actions-rotated.skill.md',
         'CTL-C2-3b v2 rows, action column rotated by one',
         'The composed shortcut: v2 rows plus a rotated action column.',
         fmt_block(rotate_actions(v2_rows), actions=V2_ACTIONS_LINE))

    # CTL-C2-4: reference rows with every contains cell reduced to an exact set.
    emit('CTL-C2-4-no-contains.skill.md',
         'CTL-C2-4 reference rows with the contains form removed (exact sets only)',
         'Every `kind+` cell is rewritten as the exact set `kind`, so the rows can no '
         'longer match a gap set that carries one extra kind.',
         fmt_block(strip_contains(ref)))

    # CTL-C2-5: v2 rows plus a final `*` default row.
    default_row = ['depth-limited-nested', 'extract_firmware', 'unblob', '*', '*', '*',
                   '*', '*', '*', 'raise-depth',
                   'a final catch-all row hands every envelope that reaches the bottom '
                   'of the table the depth-limited verdict, whether or not any '
                   'depth-limited gap exists -> this is a guess, not a precedence step',
                   'control only: the depth-limited label and the raise-depth action '
                   'are the pair the most still-uncovered planned envelopes carry']
    emit('CTL-C2-5-default-row.skill.md',
         'CTL-C2-5 v2 rows plus a final `*` default row (domain cells fixed)',
         'Same eleven rows as CTL-C2-2 plus one all-star row whose operation and '
         'provider stay extract_firmware/unblob, so the domain guard survives.',
         fmt_block(v2_rows + [default_row], actions=ACTIONS))
    all_star = list(default_row)
    all_star[1] = '*'
    all_star[2] = '*'
    emit('CTL-C2-5b-all-star-default-row.skill.md',
         'CTL-C2-5b v2 rows plus a final row with all twelve cells `*`',
         'The same catch-all with the domain cells starred too: it now swallows the '
         'out-of-domain envelope as well.',
         fmt_block(v2_rows + [all_star], actions=ACTIONS))
    inert = list(default_row)
    inert[0] = 'unclassified'
    inert[1] = '*'
    inert[2] = '*'
    inert[9] = 'none'
    emit('CTL-C2-5c-inert-default-row.skill.md',
         'CTL-C2-5c v2 rows plus a final `*` default row that restates the default',
         'The degenerate reading of "a `*` default row": unclassified/none, which the '
         'interpreter already returns on no match, so the row is behaviourally inert.',
         fmt_block(v2_rows + [inert], actions=ACTIONS))

    # CTL-C2-6: v2 rows plus the depth row only, placed before the symlink rows.
    depth_row = list(ref[6])
    rows = list(v2_rows)
    at = [i for i, row in enumerate(rows) if row[0] == 'partial-body-failure'][0] + 1
    rows.insert(at, depth_row)
    emit('CTL-C2-6-depth-row-only.skill.md',
         'CTL-C2-6 v2 rows plus the depth-limited row only (partial fix)',
         'The one repair the round-40 defect list names is added (a contains row for '
         'depth-limited, ahead of the symlink rows); the partial-body row keeps its '
         'exact gap set.',
         fmt_block(rows, actions=ACTIONS))

    manifest = {
        'base_skill': os.path.basename(ns.base_skill),
        'base_skill_sha256': base_sha,
        'base_rev': '49096c7e6f226af0c750c4b003be58883cb6049f',
        'grammar': {'marker': MARKER_V3, 'actions': ACTIONS.split(),
                    'contains': 'trailing + on a comma-joined member list',
                    'exact': 'bare member (single member only in these controls)'},
        'controls': written,
    }
    if ns.manifest:
        with open(ns.manifest, 'w', encoding='utf-8') as handle:
            json.dump(manifest, handle, indent=1, sort_keys=True)
            handle.write('\n')
    print(json.dumps(manifest['controls'], indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
