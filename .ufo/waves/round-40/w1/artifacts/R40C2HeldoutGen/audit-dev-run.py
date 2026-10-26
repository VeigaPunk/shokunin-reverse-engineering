#!/usr/bin/env python3
"""audit-dev-run.py -- re-derive the R40-C2 dev-run feature table from the envelopes.

Reads a generator output directory (``manifest.json``, ``<id>/tree.json`` and
``<id>/envelope.json`` or ``<id>/envelope.json.gz``) and, for every carrier:

  * extracts the six table features -- handler set H, gap-kind set G, gap
    dependency set D, the ``-be`` token in a recorded sasquatch argv (BE),
    MaliciousSymlinkRemoved (SR), published file count P -- plus the domain
    guard fields ``operation`` and ``provider.id``;
  * compares (label, action) against the class predicate below, so a
    generator class whose measured shape drifted fails loudly instead of
    silently scoring against a wrong row;
  * for the classes that publish regular files, compares every oracle regular
    file against a published path with the same relative-path suffix and the
    same sha256, and asserts no escaping-symlink path was published and that
    the in-tree link count equals the ``unpublished-entry`` gap count.

It never invokes REA, unblob or sasquatch and never reads a carrier image.

Usage:
  python3 -I -B audit-dev-run.py DIR [--json FEATURES.json] [--md TABLE.md]
Exit: 0 every carrier matches, 1 at least one mismatch, 2 unusable input.
"""
import argparse
import gzip
import hashlib
import json
import os
import shlex
import sys

sys.dont_write_bytecode = True

# class -> (label, handler mode, gap kinds, gap dependencies, BE, SR, P, operation, provider)
#   handler mode: 'sqfs' (a squashfs handler matched) | 'none'
#   G/D are exact sets; the empty set is written {'none'} (round-39 grammar)
#   BE/SR: yes|no|n/a ; P: '0' | '>0'
# The action half of the pair is not pinned here: it is whatever the manifest's
# label_actions map binds for that label, so the same audit serves every
# candidate vocabulary (--actions-set).
PREDICATES = {
    'clean-be': ('clean', 'sqfs', {'none'}, set(), 'n/a', 'no', '>0',
                 'extract_firmware', 'unblob'),
    'clean-le': ('clean', 'sqfs', {'none'}, set(), 'n/a', 'no', '>0',
                 'extract_firmware', 'unblob'),
    'clean-empty': ('clean-empty', 'sqfs', {'none'}, set(), 'n/a', 'no', '0',
                    'extract_firmware', 'unblob'),
    'escaping-symlink-removed': (
        'escaping-symlink-removed', 'sqfs', {'none'}, set(),
        'n/a', 'yes', '>0', 'extract_firmware', 'unblob'),
    'in-tree-symlink-metadata': (
        'in-tree-symlink-metadata', 'sqfs', {'unpublished-entry'}, set(),
        'n/a', 'no', '>0', 'extract_firmware', 'unblob'),
    'mixed-symlinks': (
        'mixed-symlinks', 'sqfs', {'unpublished-entry'}, set(),
        'n/a', 'yes', '>0', 'extract_firmware', 'unblob'),
    'dep-missing-be': (
        'dep-missing-be', 'sqfs', {'missing-extractor-dependency'},
        {'sasquatch-v4be'}, 'n/a', 'no', '0', 'extract_firmware', 'unblob'),
    'dep-missing-le': (
        'dep-missing-le', 'sqfs', {'missing-extractor-dependency'},
        {'sasquatch'}, 'n/a', 'no', '0', 'extract_firmware', 'unblob'),
    'avm-marker-be-dropped': (
        'avm-marker-be-dropped', 'sqfs', {'extractor-failure'}, set(),
        'no', 'no', '0', 'extract_firmware', 'unblob'),
    'body-extractor-failure': (
        'body-extractor-failure', 'sqfs', {'extractor-failure'}, set(),
        'yes', 'no', '0', 'extract_firmware', 'unblob'),
    'partial-body-failure': (
        'partial-body-failure', 'sqfs', {'extractor-failure'}, set(),
        'yes', 'no', '>0', 'extract_firmware', 'unblob'),
    'no-squashfs-chunk': (
        'no-squashfs-chunk', 'none', {'none'}, set(), 'n/a', 'no', '0',
        'extract_firmware', 'unblob'),
    'out-of-domain': (
        'unclassified', 'none', {'none'}, set(), 'n/a', 'no', '0',
        'inspect_firmware_regions', 'binwalk'),
}
PUBLISHING = ('clean-be', 'clean-le', 'escaping-symlink-removed',
              'in-tree-symlink-metadata', 'mixed-symlinks')


def read_json(path):
    if os.path.exists(path + '.gz'):
        with gzip.open(path + '.gz', 'rt', encoding='utf-8') as handle:
            return json.load(handle)
    with open(path, encoding='utf-8') as handle:
        return json.load(handle)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def features(env):
    nr = env.get('normalized_result') or {}
    handlers = sorted({c.get('handler') for c in nr.get('chunks') or []
                       if c.get('handler')})
    gaps = nr.get('extraction_gaps') or []
    be = 'n/a'
    for diag in nr.get('diagnostics') or []:
        command = (diag.get('report') or {}).get('command')
        if not command:
            continue
        tokens = shlex.split(command) if isinstance(command, str) else list(command)
        if any(os.path.basename(tok).startswith('sasquatch') for tok in tokens):
            be = 'yes' if '-be' in tokens else 'no'
    sr = 'yes' if any(((d.get('report') or {}).get('__typename__'))
                      == 'MaliciousSymlinkRemoved'
                      for d in nr.get('diagnostics') or []) else 'no'
    return {
        'operation': env.get('operation'),
        'provider': (env.get('provider') or {}).get('id'),
        'handlers': handlers,
        'gap_kinds': sorted({g.get('kind') for g in gaps if g.get('kind')}),
        'gap_counts': {kind: sum(1 for g in gaps if g.get('kind') == kind)
                       for kind in sorted({g.get('kind') for g in gaps
                                           if g.get('kind')})},
        'gap_dependencies': sorted({dep for g in gaps
                                    for dep in (g.get('dependencies') or [])}),
        'be_token': be,
        'symlink_removed': sr,
        'files': len(nr.get('files') or []),
        'published_files': [(f.get('relative_path'), f.get('sha256'))
                            for f in nr.get('files') or []],
        'unpublished_entries': [(u.get('kind'), u.get('relative_path'))
                                for u in nr.get('unpublished_entries') or []],
    }


def audit(root):
    manifest = json.load(open(os.path.join(root, 'manifest.json'), encoding='utf-8'))
    rows, problems = [], []
    for entry in manifest['carriers']:
        cid, cls = entry['id'], entry['class']
        env = read_json(os.path.join(root, cid, 'envelope.json'))
        tree = json.load(open(os.path.join(root, cid, 'tree.json'), encoding='utf-8'))
        feat = features(env)
        label, hmode, gset, dset, be, sr, pclass, op, provider = PREDICATES[cls]
        actions = manifest.get('label_actions') or {}
        action = actions.get(label)
        # The predicate tables spell the empty set as {'none'} (round-39 grammar).
        gset = set() if gset == {'none'} else gset
        dset = set() if dset == {'none'} else dset
        measured = {
            'id': cid, 'class': cls, 'label': label, 'action': action,
            'expected_label': entry['label'], 'expected_action': entry['action'],
            'endian': entry['endian'], 'compression': entry['compression'],
            'handlers': feat['handlers'], 'gap_kinds': feat['gap_kinds'],
            'gap_counts': feat['gap_counts'],
            'gap_dependencies': feat['gap_dependencies'], 'be_token': feat['be_token'],
            'symlink_removed': feat['symlink_removed'], 'files': feat['files'],
            'operation': feat['operation'], 'provider': feat['provider'],
            'checks': [],
        }

        def want(name, ok, detail=''):
            measured['checks'].append({'check': name, 'ok': bool(ok), 'detail': detail})
            if not ok:
                problems.append(f'{cid} {cls}: {name} {detail}')

        want('manifest label', entry['label'] == label,
             f"{entry['label']} != {label}")
        want('manifest action bound to label', action is not None
             and entry['action'] == action,
             f"{entry['action']} != {action}")
        want('action in declared vocabulary', entry['action'] in
             (manifest.get('action_vocabulary') or []), str(entry['action']))
        want('domain operation', feat['operation'] == op, str(feat['operation']))
        want('domain provider', feat['provider'] == provider, str(feat['provider']))
        has_sqfs = any(h.startswith('squashfs') for h in feat['handlers'])
        want('handler class', has_sqfs if hmode == 'sqfs' else not feat['handlers'],
             ','.join(feat['handlers']) or 'none')
        want('gap kinds', set(feat['gap_kinds']) == gset,
             f"{sorted(feat['gap_kinds'])} != {sorted(gset)}")
        want('gap dependencies', set(feat['gap_dependencies']) == dset,
             f"{sorted(feat['gap_dependencies'])} != {sorted(dset)}")
        want('-be token', feat['be_token'] == be, feat['be_token'])
        want('symlink removed', feat['symlink_removed'] == sr, feat['symlink_removed'])
        p_ok = (feat['files'] == 0) if pclass == '0' else (feat['files'] > 0)
        want('published files', p_ok, str(feat['files']))

        oracle_files = tree['oracle']['files']
        links = tree['oracle']['symlinks']
        in_tree = [link for link in links if link['kind'] == 'in-tree']
        escaping = [link for link in links if link['kind'] == 'escaping']
        if cls in PUBLISHING:
            published = feat['published_files']
            for row in oracle_files:
                hits = [sha for path, sha in published
                        if path.endswith('/' + row['path']) or path == row['path']]
                want(f"oracle file published {row['path']}", row['sha256'] in hits,
                     f"{row['sha256'][:12]} vs {[h[:12] for h in hits]}")
            for link in escaping:
                want(f"escaping path absent {link['path']}",
                     not any(path.endswith('/' + link['path']) or path == link['path']
                             for path, _sha in published))
            unpub = len(feat['unpublished_entries'])
            want('in-tree gap count one per link',
                 (feat['gap_counts'].get('unpublished-entry', 0) == len(in_tree)
                  and unpub == len(in_tree)) if in_tree
                 else (unpub == 0 and not feat['gap_counts']),
                 f"counts={feat['gap_counts']} unpublished={unpub} in_tree={len(in_tree)}")
        else:
            # Failure and out-of-domain classes publish nothing the oracle can
            # be matched against (partial publishes a truncated set), so the
            # class row is the whole check.
            want('no oracle comparison required', True, cls)
        rows.append(measured)
    return manifest, rows, problems


def table(rows):
    out = ['| carrier | class | endian/comp | H | G | D | -be | SR | P | operation/provider | pair |',
           '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for row in rows:
        out.append('| {id} | {class} | {endian}/{compression} | {H} | {G} | {D} | {be} | {sr} | {p} | {op}/{prov} | {label} / {action} |'.format(
            id=row['id'], **{'class': row['class']}, endian=row['endian'],
            compression=row['compression'],
            H=','.join(row['handlers']) or 'none',
            G=','.join(row['gap_kinds']) or 'none',
            D=','.join(row['gap_dependencies']) or 'none',
            be=row['be_token'], sr=row['symlink_removed'], p=row['files'],
            op=row['operation'], prov=row['provider'],
            label=row['label'], action=row['action']))
    return '\n'.join(out) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description='Audit an R40-C2 dev-run directory.')
    parser.add_argument('root')
    parser.add_argument('--json')
    parser.add_argument('--md')
    args = parser.parse_args(argv)
    if not os.path.isfile(os.path.join(args.root, 'manifest.json')):
        print(f'no manifest.json in {args.root}', file=sys.stderr)
        return 2
    manifest, rows, problems = audit(args.root)
    decisions = {(row['label'], row['action']) for row in rows}
    summary = {
        'root': os.path.abspath(args.root),
        'seed': manifest['seed'],
        'generator': manifest['generator'],
        'carriers': len(rows),
        'labels': sorted({row['label'] for row in rows}),
        'decisions': sorted([list(pair) for pair in decisions]),
        'distinct_row_decisions': len(decisions),
        'checks': sum(len(row['checks']) for row in rows),
        'failed_checks': problems,
        'rows': rows,
    }
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as handle:
            json.dump(summary, handle, indent=2)
            handle.write('\n')
    if args.md:
        with open(args.md, 'w', encoding='utf-8') as handle:
            handle.write(table(rows))
    print(f"carriers {summary['carriers']}  labels {len(summary['labels'])}  "
          f"decisions {summary['distinct_row_decisions']}  checks {summary['checks']}  "
          f"failed {len(problems)}")
    for problem in problems:
        print('  ' + problem)
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main())
