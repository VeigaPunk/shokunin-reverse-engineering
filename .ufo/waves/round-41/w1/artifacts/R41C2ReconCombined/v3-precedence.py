#!/usr/bin/env python3
"""Independent implementation of the R41-C2 draft v3 label precedence.

The rules below are transcribed from ``plans/round-41-claims.md`` (draft),
section R41-C2, "Label precedence", in the written order.  This file deliberately
imports neither the v2 interpreter nor the frozen generator: it reads only an
REA envelope and the 12 numbered sentences of the draft text, so any label it
prints is a read of the *precedence prose*, not a read of the v2 table.

Rule order (draft text, first match wins):

  1  OP != extract_firmware or PR != unblob                     -> unclassified/none
  2  no squashfs_v4_* handler in H                              -> no-squashfs-chunk
  3  missing-extractor-dependency in G                          -> dep-missing-be (D has
                                                                   sasquatch-v4be) else
                                                                   dep-missing-le (D has sasquatch)
  4  extractor-failure in G and P > 0                           -> partial-body-failure
  5  extractor-failure in G, P = 0, BE = no, handler
     squashfs_v4_be                                             -> avm-marker-be-dropped
  6  extractor-failure in G, P = 0                              -> body-extractor-failure
  7  depth-limited in G                                         -> depth-limited-nested (new)
  8  SR = yes and unpublished-entry in G                        -> mixed-symlinks
  9  SR = yes and G empty                                       -> escaping-symlink-removed
 10  G = {unpublished-entry}                                    -> in-tree-symlink-metadata
 11  G empty, P > 0 -> clean ; G empty, P = 0 -> clean-empty
 12  otherwise                                                  -> unclassified/none

Actions are the v2 action vocabulary carried by the draft's own predicate wording
("the (label, action) pair"); the draft names no action for the new label
``depth-limited-nested`` and none for the combined labels, so this implementation
prints ``UNBOUND`` for those and says so, rather than inventing one.

Usage: v3-precedence.py ENVELOPE.json [ENVELOPE.json ...]
Prints one JSON object per envelope.
"""

import json
import shlex
import sys

V2_ACTIONS = {
    'clean': 'none',
    'clean-empty': 'confirm-empty',
    'no-squashfs-chunk': 'inspect-input',
    'dep-missing-be': 'install-extractor-be',
    'dep-missing-le': 'install-extractor-le',
    'avm-marker-be-dropped': 'wrap-extractor-be',
    'body-extractor-failure': 'preserve-failure',
    'partial-body-failure': 'salvage-partial',
    'mixed-symlinks': 'audit-symlinks',
    'escaping-symlink-removed': 'expect-link-absent',
    'in-tree-symlink-metadata': 'count-gap',
    'unclassified': 'none',
    'depth-limited-nested': None,        # draft names no action (see docstring)
}


def walk_commands(node, out):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == 'command':
                if isinstance(value, str):
                    out.append(value)
                elif isinstance(value, list):
                    out.append(' '.join(str(v) for v in value))
            else:
                walk_commands(value, out)
    elif isinstance(node, list):
        for value in node:
            walk_commands(value, out)


def find_typename(node, want):
    if isinstance(node, dict):
        if node.get('__typename__') == want:
            return True
        return any(find_typename(v, want) for v in node.values())
    if isinstance(node, list):
        return any(find_typename(v, want) for v in node)
    return False


def features(full):
    if not isinstance(full, dict):
        return None
    data = full.get('data') if isinstance(full.get('data'), dict) else (
        full if ('normalized_result' in full or 'operation' in full) else None)
    if not isinstance(data, dict):
        return None
    normalized = data.get('normalized_result') or {}
    provider = data.get('provider')
    pr = provider.get('id') if isinstance(provider, dict) else (
        provider if isinstance(provider, str) else '')
    handlers = sorted({c.get('handler') for c in normalized.get('chunks') or []
                       if c.get('handler') and c['handler'].startswith('squashfs')})
    gaps = normalized.get('extraction_gaps') or []
    kinds = sorted({g.get('kind') for g in gaps if g.get('kind')})
    deps = sorted({d for g in gaps for d in (g.get('dependencies') or [])})
    commands = []
    for diag in normalized.get('diagnostics') or []:
        report = diag.get('report') or {}
        if isinstance(report.get('command'), str):
            commands.append(report['command'])
    for diag in data.get('diagnostics') or []:
        report = diag.get('report') or {}
        if isinstance(report.get('command'), str):
            commands.append(report['command'])
    walk_commands(data.get('raw_result'), commands)
    sasq = [c for c in commands if 'sasquatch' in c]
    if not sasq:
        be = 'n/a'
    elif any('-be' in shlex.split(c) for c in sasq):
        be = 'yes'
    else:
        be = 'no'
    sr = 'yes' if (find_typename(normalized.get('diagnostics'), 'MaliciousSymlinkRemoved')
                   or find_typename(data.get('raw_result'), 'MaliciousSymlinkRemoved')) else 'no'
    return {
        'OP': data.get('operation'), 'PR': pr, 'H': handlers,
        'G': kinds, 'D': deps, 'BE': be, 'SR': sr,
        'P': len(normalized.get('files') or []),
    }


def label(f):
    """The draft precedence, first match wins.  Returns (label, rule)."""
    if f['OP'] != 'extract_firmware' or f['PR'] != 'unblob':
        return 'unclassified', 1
    if not any(h.startswith('squashfs_v4_') for h in f['H']):
        return 'no-squashfs-chunk', 2
    if 'missing-extractor-dependency' in f['G']:
        if 'sasquatch-v4be' in f['D']:
            return 'dep-missing-be', 3
        if 'sasquatch' in f['D']:
            return 'dep-missing-le', 3
    if 'extractor-failure' in f['G'] and f['P'] > 0:
        return 'partial-body-failure', 4
    if ('extractor-failure' in f['G'] and f['P'] == 0 and f['BE'] == 'no'
            and 'squashfs_v4_be' in f['H']):
        return 'avm-marker-be-dropped', 5
    if 'extractor-failure' in f['G'] and f['P'] == 0:
        return 'body-extractor-failure', 6
    if 'depth-limited' in f['G']:
        return 'depth-limited-nested', 7
    if f['SR'] == 'yes' and 'unpublished-entry' in f['G']:
        return 'mixed-symlinks', 8
    if f['SR'] == 'yes' and not f['G']:
        return 'escaping-symlink-removed', 9
    if f['G'] == ['unpublished-entry']:
        return 'in-tree-symlink-metadata', 10
    if not f['G']:
        return ('clean', 11) if f['P'] > 0 else ('clean-empty', 11)
    return 'unclassified', 12


def main(argv):
    for path in argv:
        with open(path, encoding='utf-8') as handle:
            full = json.load(handle)
        feats = features(full)
        if feats is None:
            print(json.dumps({'path': path, 'error': 'no data object'}))
            continue
        name, rule = label(feats)
        action = V2_ACTIONS.get(name)
        print(json.dumps({'path': path, 'label': name, 'rule': rule,
                          'action': action if action is not None else 'UNBOUND',
                          'features': feats}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
