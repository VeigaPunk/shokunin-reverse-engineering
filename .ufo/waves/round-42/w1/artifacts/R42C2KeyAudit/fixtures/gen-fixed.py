"""Fixed-pair generator fixture for key-audit.py (R41-CL1 shape).

One declared-tuple key (`declared_features`) written by BOTH entry shapes --
class carriers and combo carriers -- as the round-42 draft requires
(plans/round-42-claims.md, R41-CL1: "read by the counter under exactly that
key").  Minimal on purpose: it exists to be GREEN under key-audit.py.
"""


def declared_features(handler_set, gap_kinds, gap_dependencies, be_argv,
                      symlink_removed, published):
    return {'handler_set': handler_set, 'gap_kinds': gap_kinds,
            'gap_dependencies': gap_dependencies, 'be_argv': be_argv,
            'symlink_removed': symlink_removed, 'published': published}


def build_class(seed, k):
    return {'id': 'H%02d' % k, 'sha256': 'x', 'arm': 'after',
            'declared_features': declared_features([], [], [], 'n/a',
                                                   False, 'nonzero')}


def build_combo(seed, k):
    return {'id': 'C%02d' % k, 'sha256': 'y', 'arm': 'after',
            'class_expected': None,
            'declared_features': declared_features([], [], [], 'no',
                                                   False, 'zero')}


def build_set(seed):
    manifest = {'seed': seed, 'carriers': [], 'classes': []}
    return manifest
