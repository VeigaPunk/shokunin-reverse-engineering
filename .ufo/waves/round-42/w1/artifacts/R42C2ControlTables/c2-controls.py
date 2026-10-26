#!/usr/bin/env python3
"""R42-C2 controls: build the round-42 control tables and score every one of them.

Ported from `tools/round-41/c2-controls.py` (base c4a38ea).  Two changes:

  * the grammar is the round-42 DRAFT v4 one (marker `<!-- sqfs-triage-table v4 -->`,
    same twelve columns, a `handler` cell that is an fnmatch glob over the SquashFS
    handler names in H, the round-41 `kind+` contains form kept);
  * the controls are the nine named in `plans/round-42-claims.md` `## R42-C2` plus the
    reference table, and the base document is the lane `SKILL.md` (v3 live, no v4
    marker) rather than an older revision.

Controls built into --out (all are markdown documents with a `## Queue-drain craft`
section, a v4 marker, the vocabulary line and one table):

  CTL-C2-0             byte copy of `--root SKILL.md`: the do-nothing document
  CTL-C2-0b            the live round-41 v3 table block, marker swapped to v4: the
                       do-nothing state of the SURFACE (a v3-shaped table)
  CTL-C2-1             one domain-guarded catch-all row (`clean` / `none`)
  CTL-C2-3             the reference rows, action column rotated by one row
  CTL-C2-4             the reference rows with every contains cell made exact
  CTL-C2-7             one row per named-class (label, action) over the observed DEV
                       feature tuples (the "enumerate the classes" shortcut)
  CTL-C2-7b            one row per DISTINCT observed DEV tuple, unique synthetic labels
                       (the literal exact-tuple shortcut; extra, not in the claims)
  CTL-C2-8             the reference rows without the legacy-failure row
  CTL-C2-9             the reference rows with every handler cell `squashfs_v4_*`
  CTL-C2-REF           the reference table: the positive reachability witness, NOT a
                       control (it must reach full score)

Score: for every control plus the reference, run `--interp` (the draft v4 interpreter)
on every DEV envelope and compare its (label, action) with `--eval` (the precedence
evaluator).  `--interp`/`--eval` default to this directory's DEV replicas
(`v4-check-interp.py`, `preview-precedence.py`) and are printed in the JSON so a
re-run against R42C2Interp/R42C2Eval artifacts is unambiguous.  Exit 1 when a control
reaches full score (the C2 kill rule), 0 when none does, 2 on usage/IO failure.

Honors TMPDIR; writes only --out and --json-out.
"""
import argparse
import collections
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = '<!-- sqfs-triage-table v4 -->'
V3_MARK = '<!-- sqfs-triage-table v3 -->'
ACTIONS = ('none inspect-input install-extractor-be install-extractor-le wrap-extractor-be '
           'preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent '
           'count-gap confirm-empty cross-read-legacy isolate-residue')
HEADER = ['label', 'operation', 'provider', 'handler', 'failing handler', 'gap kinds',
          'dependencies', '-be in child argv', 'symlink removed', 'published files',
          'action', 'cause', 'source']
LEGACY_GLOB = 'squashfs_v[123]*'

# The reference row set = the 13 draft steps 2..12 encoded first-match.  Step 1 (domain
# guard) and step 13 (default) are the interpreter's, not rows.  Order is load-bearing:
# dependencies before failures, failures before depth, depth before symlinks, mixed
# before escaping, escaping before in-tree, clean-empty last.
REF_ROWS = [
    dict(label='container-depth-limited', handler='none', gaps='depth-limited+', deps='*',
         be='*', sr='*', files='*', action='raise-depth',
         cause="F is empty and the run was depth-capped: no SquashFS handler was carved at "
               "this depth, but the image may sit inside a container below the budget -> "
               "raise max_depth or rerun with path on the container child; absence of a "
               "squashfs handler is not evidence of no SquashFS image",
         source='A1 step 2; measured on dev-legacy/L21 (tar at --max-depth 1; fixtures.json)'),
    dict(label='no-squashfs-chunk', handler='none', gaps='*', deps='*', be='*', sr='*',
         files='*', action='inspect-input',
         cause="F is empty and the run was not depth-capped: no squashfs handler of any "
               "version was carved -> check the magic and superblock before rerunning; an "
               "empty envelope is not an empty filesystem",
         source='A1 step 3; R41-CL4 repair; S112 :102,:159,:245,:463,:522'),
    dict(label='dep-missing-be', handler='squashfs_*', gaps='missing-extractor-dependency+',
         deps='sasquatch-v4be+', be='*', sr='*', files='*',
         action='install-extractor-be',
         cause="a chunk resolved its extractor to sasquatch-v4be and that binary was not "
               "on the child PATH, so no argv exists -> install it and rerun into a fresh "
               "output directory; the dependency name decides, not the handler version",
         source='A1 step 4; S112 :24,:68-69; S120 command.py:70-77'),
    dict(label='dep-missing-le', handler='squashfs_*', gaps='missing-extractor-dependency+',
         deps='sasquatch+', be='*', sr='*', files='*',
         action='install-extractor-le',
         cause="a chunk resolved its extractor to plain sasquatch and that binary was not "
               "on the child PATH -> install the little-endian sasquatch 4.5.1 binary and "
               "rerun; every v1-v3 chunk resolves plain sasquatch, not sasquatch-v4be",
         source='A1 step 4; unblob squashfs.py:25-26,:40-41; command.py:69-71,:101-102; measured on L12'),
    dict(label='partial-body-failure', handler='squashfs_*', gaps='extractor-failure+',
         deps='*', be='*', sr='*', files='>0', action='salvage-partial',
         cause="the extractor failed after publishing at least one regular file, on any "
               "handler -> keep the published subset, match it to the oracle by exact "
               "relative path and sha256, mark the run incomplete",
         source='A1 step 5; S119 FirmwarePublication.js:288-293; measured on L20'),
    dict(label='avm-marker-be-dropped', handler='squashfs_*', failing='squashfs_v4_be',
         gaps='extractor-failure+', deps='*', be='no', sr='*', files='0',
         action='wrap-extractor-be',
         cause="the AVM marker mkfs_time == bytes_used was read and -be was omitted from "
               "a v4 BE extraction that then failed with zero files -> rerun through a "
               "PATH executable named sasquatch-v4be that appends -be, then remove it",
         source='A1 step 6 (reads HF); S112 :44-50; S121 -DFIX_BE build'),
    dict(label='legacy-body-failure', handler='squashfs_*', failing=LEGACY_GLOB,
         gaps='extractor-failure+', deps='*', be='*', sr='*', files='0',
         action='cross-read-legacy',
         cause="the extractor ran on a v1-v3 chunk and published zero regular files; the "
               "AVM layout pre-check does not apply to a v1-v3 superblock -> cross-read "
               "the chunk with unsquashfs to separate body damage from an extractor build "
               "fault before touching the carrier",
         source='A1 step 7 (reads HF); unblob squashfs.py:40-54; measured on L13-L18'),
    dict(label='body-extractor-failure', handler='squashfs_*', gaps='extractor-failure+',
         deps='*', be='*', sr='*', files='0', action='preserve-failure',
         cause="the extractor ran and published zero regular files on a v4 chunk and the "
               "envelope cannot say why -> run the layout pre-check, keep the failing "
               "command and stderr, diff the carrier against a known-good arm",
         source='A1 step 8; S120 report.py:91-98'),
    dict(label='unknown-residue', handler='squashfs_*', gaps='unknown-chunk-handler+',
         deps='*', be='*', sr='*', files='*', action='isolate-residue',
         cause="bytes beside the SquashFS chunk were claimed by no handler and REA "
               "published them as a .unknown file -> re-carve to unblob's chunk end and "
               "never match the residue file against a filesystem oracle",
         source='A1 step 9; measured on dev-legacy/L22 (random tail); w1/R42CritC2Draft.md'),
    dict(label='depth-limited', handler='squashfs_*', gaps='depth-limited+', deps='*', be='*',
         sr='*', files='*', action='raise-depth',
         cause="REA stopped at max_depth for at least one path -> rerun with a higher "
               "max_depth into a fresh output directory, or with path set to one published "
               "child; never report the region as empty",
         source='A1 step 10; S119 FirmwarePublication.js:23-29,:294-299'),
    dict(label='mixed-symlinks', handler='squashfs_*', gaps='unpublished-entry+', deps='*',
         be='*', sr='yes', files='*', action='audit-symlinks',
         cause="both link kinds are present: at least one link was removed with a "
               "MaliciousSymlinkRemoved report and at least one stayed in-tree as an "
               "unpublished-entry gap -> expect the escaped paths absent, count the kept "
               "links",
         source='A1 step 11; S118 :50-92; S119 FirmwarePublication.js:301-307'),
    dict(label='escaping-symlink-removed', handler='squashfs_*', gaps='none', deps='*',
         be='*', sr='yes', files='*', action='expect-link-absent',
         cause="a link target resolved outside the extraction root or looped and unblob "
               "removed it with a report while REA records no gap -> expect the path "
               "absent and never materialise the link",
         source='A1 step 12; S118 :58-65,:79-90'),
    dict(label='in-tree-symlink-metadata', handler='squashfs_*', gaps='unpublished-entry',
         deps='*', be='*', sr='*', files='*', action='count-gap',
         cause="the gap set is exactly one kind: every non-file entry resolved inside the "
               "extraction root and is kept as metadata, one gap per entry -> count "
               "gaps, install nothing",
         source='A1 step 13; S119 FirmwarePublication.js:301-307'),
    dict(label='clean', handler='squashfs_*', gaps='none', deps='*', be='*', sr='*',
         files='>0', action='none',
         cause="every regular file was published on a chunk of any version and the gap "
               "set is empty -> nothing to install or fix",
         source='A1 step 14; S119 FirmwarePublication.js:301-307'),
    dict(label='clean-empty', handler='squashfs_*', gaps='none', deps='*', be='*', sr='*',
         files='0', action='confirm-empty',
         cause="the extractor completed with no gap and published zero regular files "
               "because the tree holds none -> confirm the independent oracle tree is "
               "empty before calling it clean",
         source='A1 step 14; S119 FirmwarePublication.js:301-307'),
]


# --------------------------------------------------------------------------------------
# document building
# --------------------------------------------------------------------------------------
def cell(value):
    if value == '*':
        return '`*`'
    return '`%s`' % value


def row_line(op, provider, r):
    cells = [cell(r['label']), cell(op), cell(provider), cell(r['handler']),
             cell(r.get('failing', '*')), cell(r['gaps']), cell(r['deps']),
             cell(r['be']), cell(r['sr']), cell(r['files']), cell(r['action']),
             r['cause'], r['source']]
    return '| ' + ' | '.join(cells) + ' |'


def table_lines(rows, op='extract_firmware', provider='unblob'):
    lines = ['| ' + ' | '.join(HEADER) + ' |',
             '| ' + ' | '.join('---' for _ in HEADER) + ' |']
    lines += [row_line(op, provider, r) for r in rows]
    return lines


def doc(title, block_lines, note='Control data for R42-C2; not instructions.'):
    return '\n'.join(['# %s' % title, '', note, '', '## Queue-drain craft', '']
                     + block_lines + ['', '## End', ''])


def as_block(rows, marker=MARK):
    return [marker, '<!-- sqfs-triage-actions: %s -->' % ACTIONS] + table_lines(rows)


def relabel(label, r):
    out = dict(r)
    out['label'] = label
    return out


def build_catch_all():
    return [dict(label='clean', handler='*', gaps='*', deps='*', be='*', sr='*', files='*',
                 action='none',
                 cause="one row: every envelope inside the domain is clean -> nothing to "
                       "install or fix",
                 source='control only')]


def build_rotated():
    rows = [dict(r) for r in REF_ROWS]
    acts = [r['action'] for r in rows]
    rot = acts[1:] + acts[:1]
    assert all(a != b for a, b in zip(acts, rot)), 'rotation has a fixed point'
    for r, a in zip(rows, rot):
        r['action'] = a
    return rows


def exact(gaps):
    """Turn a contains cell into the exact-set cell of the same members."""
    if gaps == '*':
        return '*'
    if gaps.endswith('+'):
        members = [m for m in gaps[:-1].split(',') if m]
        return '+'.join(members) if len(members) > 1 else members[0]
    return gaps


def build_exact_only():
    rows = []
    for r in REF_ROWS:
        out = dict(r)
        out['gaps'] = exact(r['gaps'])
        rows.append(out)
    return rows


def build_no_legacy():
    return [dict(r) for r in REF_ROWS if r['label'] != 'legacy-body-failure']


def build_no_container_residue():
    drop = {'container-depth-limited', 'unknown-residue'}
    return [dict(r) for r in REF_ROWS if r['label'] not in drop]


def build_v4_handler():
    rows = []
    for r in REF_ROWS:
        out = dict(r)
        out['handler'] = 'squashfs_v4_*'
        rows.append(out)
    return rows


# --------------------------------------------------------------------------------------
# the lookup controls: observed DEV tuples, exact
# --------------------------------------------------------------------------------------
def merge_handler(handlers):
    hs = [tuple(sorted(h)) for h in handlers]
    if not hs:
        return 'none'
    if len(set(hs)) == 1:
        if not hs[0]:
            return 'none'
        return hs[0][0] if len(hs[0]) == 1 else 'squashfs_*'
    flat = {h for t in hs for h in t}
    if not flat:
        return 'none'
    if all(h.startswith('squashfs_v4_') for h in flat):
        return 'squashfs_v4_*'
    return 'squashfs_*'


def merge_files(published):
    vals = set(published)
    return vals.pop() if len(vals) == 1 else '*'


def gaps_cell(kinds):
    vals = {tuple(sorted(k)) for k in kinds}
    if len(vals) != 1:
        return '*'
    members = vals.pop()
    if not members:
        return 'none'
    return '+'.join(members)


def lookup_row(label, action, feats, used_labels, synthetic_prefix):
    name = label
    if name in used_labels:
        n = 1
        while '%s-%d' % (synthetic_prefix, n) in used_labels:
            n += 1
        name = '%s-%d' % (synthetic_prefix, n)
    used_labels.add(name)
    return dict(
        label=name,
        handler=merge_handler([f['H'] for f in feats]),
        gaps=gaps_cell([f['G'] for f in feats]),
        deps=('none' if all(not f['D'] for f in feats)
              else (sorted(feats[0]['D'])[0] if all(sorted(f['D']) == sorted(feats[0]['D'])
                                                     for f in feats) else '*')),
        be=(feats[0]['BE'] if len({f['BE'] for f in feats}) == 1 else '*'),
        sr=(feats[0]['SR'] if len({f['SR'] for f in feats}) == 1 else '*'),
        files=merge_files([('>0' if f['P'] else '0') for f in feats]),
        action=action,
        cause='a declared class tuple -> %s' % action,
        source='control only; observed DEV tuple')


def build_lookup(named, per_class):
    """One row per (label, action); differing columns across the class become `*`."""
    rows, used = [], set()
    for key in named:
        rows.append(lookup_row(key[0], key[1], per_class[key], used, 'lookup'))
    return sort_specific(rows)


def build_lookup_exact(per_tuple):
    """One row per distinct observed tuple; labels unique, synthesized after the first."""
    rows, used = [], set()
    for label, action, feats in per_tuple:
        rows.append(lookup_row(label, action, feats, used, 'lookup'))
    return sort_specific(rows)


def sort_specific(rows):
    """Most specific row first: a lookup table is normally built specific-first, and the
    first-match grammar makes the order load-bearing.  Stability keeps tuple order inside
    one specificity level."""
    return sorted(rows, key=lambda r: sum(1 for k in ('handler', 'gaps', 'deps', 'be',
                                                     'sr', 'files') if r[k] == '*'))


def build_lookup_fallback(named, per_class):
    """CTL-C2-7b: the lookup rows with the MAJORITY (label, action) pair's own row
    replaced by one all-`*` fallback row at the bottom, so anything the specific rows miss
    is guessed as the most common outcome.  A duplicate label is refused by the
    interpreter, so the majority row must move, not be added."""
    counts = collections.Counter()
    for key in named:
        counts[key] += len(per_class[key])
    majority = counts.most_common(1)[0][0]
    rows = [r for r in build_lookup(named, per_class) if r['label'] != majority[0]]
    rows.append(dict(label=majority[0], handler='*', gaps='*', deps='*', be='*', sr='*',
                     files='*', action=majority[1],
                     cause='unseen tuple -> the dev arm majority label (%s)' % majority[0],
                     source='control only; majority fallback'))
    return rows, [majority[0], majority[1], counts[majority]]


def unsorted_lookup(named, per_class):
    """The same rows as build_lookup, kept in class-discovery order: the order sensitivity
    witness that shows how much of the control's score is the enumeration and how much is
    the sort."""
    rows, used = [], set()
    for key in named:
        rows.append(lookup_row(key[0], key[1], per_class[key], used, 'lookup'))
    return rows


def combo_ids(devdirs):
    """Envelope ids the dev manifest declares as `combo`: a lookup must not learn them."""
    out = set()
    for d in devdirs:
        path = os.path.join(d, 'manifest.json')
        if not os.path.isfile(path):
            continue
        for c in json.load(open(path)).get('carriers') or []:
            if c.get('class') == 'combo':
                out.add(c.get('id'))
    return out


# --------------------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------------------
def envelope_id(path):
    base = os.path.basename(path)
    parent = os.path.basename(os.path.dirname(path))
    if base in ('envelope.json', 'rea-full.json'):
        return parent
    return os.path.splitext(base)[0]


def run_interp(interp, skill, envs):
    r = subprocess.run([sys.executable, '-I', '-B', interp, '--skill', skill] + envs,
                       capture_output=True, text=True)
    out = collections.OrderedDict()
    if r.returncode == 0:
        for line in r.stdout.splitlines():
            parts = line.split('\t')
            if len(parts) == 3:
                out[envelope_id(parts[0])] = (parts[1], parts[2])
    return r.returncode, out, r.stderr.strip()[-400:]


def interp_features(interp, skill_ref, envs):
    r = subprocess.run([sys.executable, '-I', '-B', interp, '--skill', skill_ref, '--json']
                       + envs, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('feature extraction failed (exit %d): %s'
                         % (r.returncode, r.stderr.strip()[-400:]))
    payload = json.loads(r.stdout)
    feats = {}
    for rec in payload['results']:
        f = rec['features']
        # the two interpreters disagree on whether `H` is squashfs-only or every handler
        # name; the lookup control needs F, so normalise to the squashfs prefix here
        h = [name for name in (f.get('H') or []) if str(name).startswith('squashfs_')]
        feats[envelope_id(rec['path'])] = {
            'OP': f.get('OP'), 'PV': f.get('PV'), 'H': h,
            'G': f.get('G') or [], 'D': f.get('D') or [], 'BE': f.get('BE'),
            'SR': f.get('SR'), 'P': f.get('P') or 0,
        }
    return feats


def collect_envs(dirs):
    envs = []
    for d in dirs:
        for name in sorted(os.listdir(d)):
            sub = os.path.join(d, name)
            if not os.path.isdir(sub):
                continue
            for cand in ('envelope.json', 'rea-full.json'):
                p = os.path.join(sub, cand)
                if os.path.isfile(p):
                    envs.append(p)
                    break
    return envs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='lane root (its SKILL.md is CTL-C2-0)')
    ap.add_argument('--dev', action='append', required=True,
                    help='DEV envelope directory (repeatable); first is the named-class arm')
    ap.add_argument('--out', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--interp', default=None)
    ap.add_argument('--eval', default=None)
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--extra-control', action='append', default=[],
                    help='NAME=PATH documents scored beside the generated ones')
    a = ap.parse_args(argv)
    interp = a.interp or os.path.join(HERE, 'v4-check-interp.py')
    evaluator = a.eval or os.path.join(HERE, 'preview-precedence.py')
    os.makedirs(a.out, exist_ok=True)
    skill_text = open(os.path.join(a.root, 'SKILL.md'), encoding='utf-8').read()
    envs = collect_envs(a.dev)
    if not envs:
        raise SystemExit('no envelopes under %r' % a.dev)

    info = {}
    if a.build:
        shutil.copyfile(os.path.join(a.root, 'SKILL.md'),
                        os.path.join(a.out, 'CTL-C2-0-base-SKILL.md'))
        # CTL-C2-0b: the live v3 block, bytes unchanged except the marker line
        lines = skill_text.splitlines()
        i = next(k for k, l in enumerate(lines) if V3_MARK in l)
        j = i + 1
        while j < len(lines) and not lines[j].lstrip().startswith('|'):
            j += 1
        k = j
        while k < len(lines) and lines[k].lstrip().startswith('|'):
            k += 1
        block = list(lines[i:k])
        block[0] = block[0].replace(V3_MARK, MARK)
        open(os.path.join(a.out, 'CTL-C2-0b-v3-table-v4-marker.md'), 'w').write(
            doc('CTL-C2-0b (the round-41 v3 table bytes under the v4 marker)', block))
        # CTL-C2-0c: the same rows widened to the 13-column A1 grammar (failing `*`), so
        # the do-nothing surface stays parseable after the grammar change
        wide = []
        for line in block:
            if not line.lstrip().startswith('|'):
                wide.append(line)
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells[0].lower() == 'label':
                cells.insert(4, 'failing handler')
            elif all(set(c) <= set('-: ') for c in cells):
                cells.insert(4, '---')
            else:
                cells.insert(4, '`*`')
            wide.append('| ' + ' | '.join(cells) + ' |')
        open(os.path.join(a.out, 'CTL-C2-0c-v3-rows-13col.md'), 'w').write(
            doc('CTL-C2-0c (the round-41 v3 rows widened to the A1 13-column grammar)',
                wide))
        ref_block = as_block(REF_ROWS)
        open(os.path.join(a.out, 'CTL-C2-REF-v4-precedence.md'), 'w').write(
            doc('CTL-C2-REF (reference v4 rows; the positive witness, not a control)',
                ref_block))
        for name, rows in (('CTL-C2-1-catch-all', build_catch_all()),
                           ('CTL-C2-3-actions-rotated', build_rotated()),
                           ('CTL-C2-4-exact-gap-sets', build_exact_only()),
                           ('CTL-C2-8-no-legacy-row', build_no_legacy()),
                           ('CTL-C2-9-v4-handler-glob', build_v4_handler()),
                           ('CTL-C2-10-no-container-residue', build_no_container_residue())):
            open(os.path.join(a.out, name + '.md'), 'w').write(doc(name, as_block(rows)))
        # the lookup controls read observed DEV tuples produced by the interpreter
        ref_path = os.path.join(a.out, 'CTL-C2-REF-v4-precedence.md')
        feats = interp_features(interp, ref_path, envs)
        ev = score_eval(evaluator, a.dev)
        named, per_class, per_tuple = [], collections.OrderedDict(), []
        seen_tuple = set()
        skip = combo_ids(a.dev)
        for path in envs:
            eid = envelope_id(path)
            if eid not in ev or eid in skip:
                continue
            label, action = ev[eid]['label'], ev[eid]['action']
            f = feats[eid]
            if (label, action) not in per_class:
                named.append((label, action))
                per_class[(label, action)] = []
            per_class[(label, action)].append(f)
            key = (label, action, tuple(sorted(f['H'])), tuple(sorted(f['G'])),
                   tuple(sorted(f['D'])), f['BE'], f['SR'], f['P'] > 0)
            if key not in seen_tuple:
                seen_tuple.add(key)
                per_tuple.append((label, action, [f]))
        rows7 = build_lookup(named, per_class)
        open(os.path.join(a.out, 'CTL-C2-7-lookup.md'), 'w').write(
            doc('CTL-C2-7 (one row per named-class label from the observed DEV tuples)',
                as_block(rows7)))
        rows7b, majority = build_lookup_fallback(named, per_class)
        open(os.path.join(a.out, 'CTL-C2-7b-lookup-majority-fallback.md'), 'w').write(
            doc('CTL-C2-7b (CTL-C2-7 plus one majority-label `*` fallback row; A1 control)',
                as_block(rows7b)))
        rows7x = build_lookup_exact(per_tuple)
        open(os.path.join(a.out, 'CTL-C2-7x-lookup-exact-tuples.md'), 'w').write(
            doc('CTL-C2-7x (one row per distinct observed DEV tuple; unique labels; extra)',
                as_block(rows7x)))
        rows7c = unsorted_lookup(named, per_class)
        open(os.path.join(a.out, 'CTL-C2-7c-lookup-discovery-order.md'), 'w').write(
            doc('CTL-C2-7c (CTL-C2-7 rows in class-discovery order, no specificity sort)',
                as_block(rows7c)))
        info['lookup_rows'] = len(rows7)
        info['lookup_majority'] = majority
        info['lookup_exact_rows'] = len(rows7x)

    expected = score_eval(evaluator, a.dev)
    docs = sorted(f for f in os.listdir(a.out) if f.startswith('CTL-') and f.endswith('.md'))
    extra = []
    for spec in a.extra_control:
        name, _, path = spec.partition('=')
        extra.append((name, path))
    scores = {}
    for name, path in [(None, os.path.join(a.root, 'SKILL.md'))] + \
                      [(d, os.path.join(a.out, d)) for d in docs] + extra:
        label = name or 'SKILL.md (live v3 table)'
        rc, got, err = run_interp(interp, path, envs)
        ids = [envelope_id(p) for p in envs]
        matched = [i for i in ids if i in expected and got.get(i) == (expected[i]['label'],
                                                                    expected[i]['action'])]
        missed = [i for i in ids if i not in matched]
        by_step = collections.Counter(expected[i]['step'] for i in missed if i in expected)
        combo = combo_ids(a.dev)
        combo_ids_here = [i for i in ids if i in combo]
        named_ids_here = [i for i in ids if i not in combo]
        scores[label] = {
            'interp_exit': rc, 'matched': len(matched), 'n': len(ids),
            'full': len(matched) == len(ids),
            'label_hits': sum(1 for i in ids if i in expected and got.get(i, ('', ''))[0]
                              == expected[i]['label']),
            'action_hits': sum(1 for i in ids if i in expected and got.get(i, ('', ''))[1]
                               == expected[i]['action']),
            'combo': [sum(1 for i in combo_ids_here if i in matched), len(combo_ids_here)],
            'named': [sum(1 for i in named_ids_here if i in matched), len(named_ids_here)],
            'missed': missed, 'missed_by_step': dict(sorted(by_step.items())),
            'stderr_tail': err if rc else '',
        }
    controls = [k for k in scores if k != 'SKILL.md (live v3 table)'
                and 'REF' not in k]
    full = [k for k in controls if scores[k]['full']]
    res = {
        'interp': os.path.relpath(os.path.abspath(interp), a.root)
        if os.path.abspath(interp).startswith(os.path.abspath(a.root)) else interp,
        'eval': os.path.relpath(os.path.abspath(evaluator), a.root)
        if os.path.abspath(evaluator).startswith(os.path.abspath(a.root)) else evaluator,
        'dev_slices': [os.path.relpath(d, a.root) for d in a.dev],
        'n': len(envs),
        'expected_steps': dict(sorted(collections.Counter(
            r['step'] for r in expected.values()).items())),
        'scores': scores,
        'controls_at_full': full,
        'kill_rule_fires': bool(full),
        **info,
    }
    json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    for k, v in scores.items():
        print('%-46s exit=%d matched=%d/%d  label=%d action=%d'
              % (k, v['interp_exit'], v['matched'], v['n'], v['label_hits'],
                 v['action_hits']))
    print('kill_rule_fires', res['kill_rule_fires'])
    return 1 if full else 0


def score_eval(evaluator, devdirs):
    """Expected (label, action, step) per envelope id, merged across DEV slices."""
    import tempfile
    merged = {}
    for dev in devdirs:
        with tempfile.TemporaryDirectory() as t:
            out = os.path.join(t, 'ev.json')
            r = subprocess.run([sys.executable, '-I', '-B', evaluator, '--envelopes', dev,
                                '--out', out], capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit('evaluator failed on %s (exit %d): %s'
                                 % (dev, r.returncode, r.stderr.strip()[-400:]))
            doc = json.load(open(out))
            if isinstance(doc.get('results'), list):
                # the frozen evaluator's shape: one record per envelope, with `id`
                for rec in doc['results']:
                    merged[rec['id']] = {'label': rec['label'], 'action': rec['action'],
                                         'step': rec.get('step')}
            else:
                merged.update(doc['labels'])
    return merged


if __name__ == '__main__':
    sys.exit(main())
