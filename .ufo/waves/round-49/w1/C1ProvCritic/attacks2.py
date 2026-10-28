# A6: oracle-only fabrication with a COMPLETE projection: the raw_result HashReport
# digests (md5/sha1) are computed from the frozen committed oracle bytes, not from a run.
# Reuses attacks.py's definitions (everything before run_case) and its run_case/landing.
import hashlib, sys, os, json
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'attacks.py')).read().split('def run_case')[0]
sys.argv = sys.argv[:3]
exec(compile(src, 'attacks.py', 'exec'))
def oracle_tree(i): return os.path.join(LANE, cars[i]['output_tree'])
def a6(i):
    e = oracle_env(i); out = f'{S}/atk/A6/{i}/rea-out'
    reports = []
    for m in cars[i]['oracle']['members']:
        if m.get('type') not in (None, 'regular'): continue
        raw = open(os.path.join(oracle_tree(i), m['path']), 'rb').read()
        assert hashlib.sha256(raw).hexdigest() == m['sha256'], (i, m['path'])
        reports.append({'task': {'path': f'{out}/firmware.bin_extract/{m["path"]}'},
                        'reports': [{'__typename__': 'HashReport', 'md5': hashlib.md5(raw).hexdigest(),
                                     'sha1': hashlib.sha1(raw).hexdigest()}]})
    e['raw_result'] = {'report': reports}
    return e
CASES = {'A6_oracle_fabrication_complete_projection_r49_path': {i: a6(i) for i in IDS}}
