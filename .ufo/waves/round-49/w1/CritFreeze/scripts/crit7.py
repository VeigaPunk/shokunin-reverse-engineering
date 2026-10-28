import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crit as C
from crit import g, FREEZE
out = {}
sc = os.path.join(C.S, 'sc')
for name in sorted(os.listdir(sc)):
    d = os.path.join(sc, name)
    if not os.path.isdir(d): continue
    rev = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
    if name.startswith('S15b') or name.startswith('S3d') or name.startswith('S27'):
        pass
    C.FREEZE = FREEZE
    cli = C.c1_cli(d, rev)
    out[name] = {'rev': rev, 'c1_cli': {k: cli[k] for k in ('exit', 'reason', 'frozen_path_changed')},
                 'c1_walk': C.c1_walk(d, rev), 'c2_walk': {k: C.c2_walk(d, rev)[k] for k in ('exit', 'reason', 'mismatches')}}
    print(name, json.dumps(out[name], sort_keys=True), flush=True)
json.dump(out, open(os.path.join(C.S, 'matrix.json'), 'w'), indent=1, sort_keys=True)
