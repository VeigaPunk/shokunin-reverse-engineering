"""M4 detector, second direction: the engine's own provenance_ok under each wrapper's PROV_BASE."""
import importlib.util
from pathlib import Path
L = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
eng = load(L/'tools/round-50/c1-counter.py', 'eng')
base = load('/fast/scratch/hyaku/kaidoku-r67/MutCounter/fix/head3-blob.py', 'base')
m4 = load('/fast/scratch/hyaku/kaidoku-r67/MutCounter/mut/M4-v3/counter.py', 'm4')
for label, p in (('r67 real run (c1-run.sh shape)', '/fast/scratch/hyaku/kaidoku-r67/c1-run.ABC123/extract'),
                 ('r67 counter scratch', '/fast/scratch/hyaku/kaidoku-r67/counter/x'),
                 ('r50 frozen envelope g7581', '/fast/scratch/hyaku/kaidoku-r50/c1-run.uVY6Hs/extract')):
    row = []
    for mod in (base, m4):
        eng.PROV_BASE = mod.PROV_BASE; row.append(eng.provenance_ok(p))
    print('%-32s base=%-5s M4=%-5s' % (label, row[0], row[1]))
