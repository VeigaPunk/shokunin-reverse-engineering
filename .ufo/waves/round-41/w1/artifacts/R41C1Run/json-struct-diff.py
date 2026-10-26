#!/usr/bin/env python3
"""Structure diff for two JSON documents (stdout report, exit 0/1).

Reports, for A (reference) vs B (candidate):
  * key paths only in A, key paths only in B (with their type)
  * key paths present in both with a different JSON type
  * leaf values that differ (path, A value, B value), truncated to 160 chars
  * list lengths that differ

Exit 0 when A and B have the same key-path set and every common key path has
the same type (value differences are reported but are not a failure); exit 1
otherwise. A list is compared element-wise by index (homogeneous envelopes);
extra list elements are reported as list-length differences only.

Pure stdlib; no /tmp use.
"""
import json
import sys

MAX = 160


def walk(node, prefix, out):
    if isinstance(node, dict):
        for key, value in node.items():
            walk(value, '%s.%s' % (prefix, key), out)
    elif isinstance(node, list):
        out[prefix] = ('list', len(node))
        for i, value in enumerate(node):
            walk(value, '%s[%d]' % (prefix, i), out)
    else:
        kind = 'null' if node is None else type(node).__name__
        out[prefix] = (kind, node)


def short(value):
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= MAX else text[:MAX] + '...'


def main(argv):
    if len(argv) != 3:
        sys.stderr.write('usage: json-struct-diff.py A.json B.json\n')
        return 2
    with open(argv[1], encoding='utf-8') as fh:
        a = json.load(fh)
    with open(argv[2], encoding='utf-8') as fh:
        b = json.load(fh)
    amap, bmap = {}, {}
    walk(a, '$', amap)
    walk(b, '$', bmap)

    only_a = sorted(set(amap) - set(bmap))
    only_b = sorted(set(bmap) - set(amap))
    common = sorted(set(amap) & set(bmap))
    type_mismatch = [(p, amap[p][0], bmap[p][0]) for p in common if amap[p][0] != bmap[p][0]]
    value_diff = [
        (p, amap[p][1], bmap[p][1])
        for p in common
        if amap[p][0] != 'list' and amap[p][0] == bmap[p][0] and amap[p][1] != bmap[p][1]
    ]
    len_diff = [
        (p, amap[p][1], bmap[p][1])
        for p in common
        if amap[p][0] == 'list' and amap[p][1] != bmap[p][1]
    ]

    print('A: %s' % argv[1])
    print('B: %s' % argv[2])
    print('key_paths: A=%d B=%d common=%d' % (len(amap), len(bmap), len(common)))
    print('only_in_A: %d' % len(only_a))
    for p in only_a:
        print('  - %s (%s)' % (p, amap[p][0]))
    print('only_in_B: %d' % len(only_b))
    for p in only_b:
        print('  + %s (%s)' % (p, bmap[p][0]))
    print('type_mismatch: %d' % len(type_mismatch))
    for p, ka, kb in type_mismatch:
        print('  ! %s: %s vs %s' % (p, ka, kb))
    print('list_length_mismatch: %d' % len(len_diff))
    for p, la, lb in len_diff:
        print('  ~ %s: %d vs %d' % (p, la, lb))
    print('leaf_value_diff: %d' % len(value_diff))
    for p, va, vb in value_diff:
        print('  * %s\n      A=%s\n      B=%s' % (p, short(va), short(vb)))

    structural = not only_a and not only_b and not type_mismatch
    print('STRUCTURE_%s' % ('EQUAL' if structural else 'DIFFERS'))
    return 0 if structural else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
