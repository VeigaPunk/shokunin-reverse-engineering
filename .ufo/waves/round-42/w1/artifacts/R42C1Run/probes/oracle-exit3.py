#!/usr/bin/env python3
import argparse, json, os
p = argparse.ArgumentParser()
for f in ('--work','--files','--nonregular','--json','--offset'):
    p.add_argument(f)
a, _ = p.parse_known_args()
os.makedirs(a.work, exist_ok=True)
open(a.files,'w').write('a.txt\t' + '0'*64 + '\t1\n')
open(a.nonregular,'w').write('')
json.dump({'cross_check': {'verdict':'disagree','mismatch_count':1,'first_20':[{'relpath':'a.txt'}]}}, open(a.json,'w'))
raise SystemExit(3)
