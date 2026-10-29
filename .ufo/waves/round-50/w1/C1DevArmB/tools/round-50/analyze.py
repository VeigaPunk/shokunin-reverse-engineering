#!/usr/bin/env python3
"""C1DevArmB analysis: semantic projection of REA envelope + oracle comparison. Stdlib only."""
import json, os, sys, hashlib, subprocess
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def proj(env):
    d=env['data']; n=d['normalized_result']
    return {
      'coverage': n['coverage'],
      'handlers': sorted({c['handler'] for c in n['chunks'] if c['handler']}),
      'chunks': [(c['handler'],c['range'],c['root_file_range'],c['encrypted'],c['extraction_failed']) for c in n['chunks']],
      'gaps': sorted((g['kind'],g['relative_path'],g['handler'],tuple(g['dependencies'])) for g in n['extraction_gaps']),
      'gap_kinds': sorted({g['kind'] for g in n['extraction_gaps']}),
      'unpublished': sorted((u['relative_path'],u['kind'],u['link_target']) for u in n['unpublished_entries']),
      'files': sorted((f['relative_path'],f['sha256'],f['size']) for f in n['files']),
      'published_bytes': n['published_bytes'],
      'diagnostics': n['diagnostics'],
      'depth_limited_paths': n['depth_limited_paths'],
      'subject_sha256': d['subject']['digest']['sha256'],
      'evidence_id': d['evidence_id'],
    }
def sem(p):  # projection without the evidence id/paths
    q=dict(p); q.pop('evidence_id'); return q
def main():
    out={}
    for name,path in [a.split('=',1) for a in sys.argv[1:]]:
        out[name]=proj(json.load(open(path)))
    json.dump(out,sys.stdout,indent=1,default=list)
if __name__=='__main__': main()
