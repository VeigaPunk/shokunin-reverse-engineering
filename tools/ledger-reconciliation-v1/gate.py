#!/usr/bin/env python3
"""Prospective disclosure reconciliation; NOT historical filing or round admission.

Runs unchanged pinned v1 audit. Live claims retain exact v1 findings. Only the
pinned, deliberately retired round35 declaration is classified as historical.
All original ledger bytes remain a prefix; appended rows must still agree with
v1. The old gate remains independently available and its actual exit is shown.
This candidate has no authority until independent review and explicit adoption.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

CONTRACT_SHA = 'a3e9ae358266f570f52cd9b644015893de7d82bcc1642df837ec900d205ede6d'
CONTRACT_PATH = 'tools/ledger-reconciliation-v1/contract.json'

def git(root,*args,ok=(0,)):
    p=subprocess.run(['git','-C',str(root),*args],capture_output=True)
    if p.returncode not in ok: raise ValueError('git_failed: '+ ' '.join(args[:3]))
    return p

def blob(root,rev,path): return git(root,'show',f'{rev}:{path}').stdout

def digest(b): return hashlib.sha256(b).hexdigest()

def absent(root,rev,path):
    # Tree listing, not arbitrary git failure interpreted as absence.
    return not git(root,'ls-tree',rev,'--',path).stdout.strip()

def audit(root,rev,require_clean=()):
    root=Path(root).resolve()
    measured=git(root,'rev-parse','--verify','--end-of-options',rev+'^{commit}').stdout.decode().strip()
    cfgbytes=blob(root,measured,CONTRACT_PATH)
    if digest(cfgbytes)!=CONTRACT_SHA: raise ValueError('contract_changed')
    c=json.loads(cfgbytes)
    for commit in (c['baseline'],c['retirement_commit'],c['row_added_commit']):
        if git(root,'merge-base','--is-ancestor',commit,measured,ok=(0,1)).returncode:
            raise ValueError('historical_source_not_ancestor')
    original=blob(root,c['baseline'],c['ledger'])
    if digest(original)!=c['original_ledger_sha256']: raise ValueError('original_ledger_changed')
    if not blob(root,measured,c['ledger']).startswith(original): raise ValueError('original_ledger_not_preserved')
    original_row=c['original_row'].encode()
    source_rows=blob(root,c['row_added_commit'],c['ledger']).splitlines(keepends=True)
    if source_rows.count(original_row)!=1: raise ValueError('historical_declaration_not_exact')
    if not absent(root,c['retirement_commit'],c['retired_path']): raise ValueError('retirement_not_proven')
    if not absent(root,measured,c['retired_path']): raise ValueError('retired_authority_revived')
    for commit,path,sha in c['proofs']:
        if digest(blob(root,commit,path))!=sha: raise ValueError('retirement_evidence_changed')
    old=root/c['old_gate']
    if digest(blob(root,measured,c['old_gate']))!=c['old_sha256'] or digest(old.read_bytes())!=c['old_sha256']:
        raise ValueError('legacy_gate_changed')
    spec=importlib.util.spec_from_file_location('kaidoku_legacy_v1',old)
    legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
    raw,rawcode=legacy.audit(root,measured,list(require_clean),c['ledger'])
    d=raw['disclosures']
    # No arbitrary exceptions: all extant records must agree, required-clean
    # failures remain failures, and the only absent path is the proven draft.
    valid=(not raw['required_failed'] and d['present'] and not d['missing']
           and not d['mismatched'] and d['exact']==d['of']
           and d['stray']==[c['retired_round']])
    return {'schema':c['schema'],'measured':measured,'current_reconciliation': 'PASS' if valid else 'FAIL',
        'historical_filing_repaired':False,'round_admission':False,
        'legacy_exit':rawcode,'legacy_audit':raw,
        'historical_declaration':{'round':c['retired_round'],'original_row':c['original_row'].rstrip('\n'),
        'state':'retired-declaration-preserved-NOT-current-claim','retirement_commit':c['retirement_commit'],
        'row_added_commit':c['row_added_commit'],'original_row_is_not_recomputed_verdict':True}},0 if valid else 1

def main():
    for k in tuple(os.environ):
        if k.startswith('GIT_'): del os.environ[k]
    os.environ.update(GIT_NO_REPLACE_OBJECTS='1',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',
        GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='core.hooksPath',GIT_CONFIG_VALUE_0='/dev/null',
        GIT_CONFIG_KEY_1='core.attributesFile',GIT_CONFIG_VALUE_1='/dev/null')
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',required=True);ap.add_argument('--rev',required=True)
    ap.add_argument('--require-clean',action='append',default=[]);a=ap.parse_args()
    try:r,rc=audit(a.root,a.rev,a.require_clean)
    except (ValueError,OSError,KeyError,UnicodeError,TypeError) as e:r,rc={'current_reconciliation':'UNEVALUABLE','error':str(e)},2
    print(json.dumps(r,sort_keys=True));return rc
if __name__=='__main__': raise SystemExit(main())
