import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crit as C
from crit import g, FREEZE
res = {}
d = os.path.join(C.S, 'sc', 'S15b_replace_touch'); R = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
C.FREEZE = FREEZE
# (1) replace refs in force (default): both counters
res['S15b_default'] = {'c1': C.c1_walk(d, R), 'c2': C.c2_walk(d, R)}
# (2) mitigation probe: GIT_NO_REPLACE_OBJECTS=1 in the counter environment
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'; C.ENV['GIT_NO_REPLACE_OBJECTS'] = '1'
res['S15b_no_replace_env'] = {'c1': C.c1_walk(d, R), 'c2': C.c2_walk(d, R)}
del os.environ['GIT_NO_REPLACE_OBJECTS']; del C.ENV['GIT_NO_REPLACE_OBJECTS']
print(json.dumps(res, sort_keys=True, indent=1))
# (3) squash: F -> single commit with FREEZE's tree (what a rebase/squash of X+R yields)
d2 = C.mkrepo('S27_squash')
tree = g(d2, 'rev-parse', FREEZE + '^{tree}').stdout.decode().strip()
sq = g(d2, 'commit-tree', tree, '-p', FREEZE, '-m', 'squashed').stdout.decode().strip()
g(d2, 'checkout', '-q', '--detach', sq)
res['S27_squash'] = {'rev': sq, 'c1': C.c1_walk(d2, sq), 'c2': C.c2_walk(d2, sq)}
print(json.dumps({'S27': res['S27_squash']}, sort_keys=True))
json.dump(res, open(os.path.join(C.S, 'results-walk6.json'), 'w'), indent=1, sort_keys=True)
