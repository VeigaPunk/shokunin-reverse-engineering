import importlib.util, json, os, shutil, subprocess, sys, hashlib, datetime

S = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
COUNTER = os.path.join(LANE, 'tools/round-50/c1-counter.py')

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

def sha256(b):
    return hashlib.sha256(b).hexdigest()

out = {'probe': 'CritRetry retry-policy probe', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'counter_path': COUNTER, 'counter_sha256': sha256(open(COUNTER,'rb').read())}

# ---------- probe D: r51 draft predicate (verbatim 2 lines) ----------
ERR_REAL = json.load(open(os.path.join(LANE, '.ufo/waves/round-50/l1/scores/c1-after-attempt2.json')))['carriers']['g7581']['projection_error']['error']

def r51_predicate(err_obj):
    """Verbatim from .ufo/waves/round-51/l1/drafts/c1-counter.py:2135-2137"""
    err_text = json.dumps(err_obj) if err_obj else ''
    return (err_obj.get('code') == 'execution_failure'
            and 'ENOENT' in err_text and 'readlink' in err_text)

cases = {}
cases['real_g7581_error'] = (r51_predicate(ERR_REAL), 'expected True')
# ENOENT+readlink ONLY in the boilerplate message, no path at all
cases['enoent_only_in_message'] = (r51_predicate({
    'category':'execution_failure','code':'execution_failure',
    'message':'ENOENT: no such file or directory, readlink somewhere',
    'details':{'diagnostics':{'reason':'unrelated internal error'}}}), 'claims say False (needs a PATH inside the tree)')
# ENOENT+readlink naming a path OUTSIDE the extraction tree
cases['enoent_path_outside_tree'] = (r51_predicate({
    'category':'execution_failure','code':'execution_failure',
    'details':{'diagnostics':{'reason':"ENOENT: no such file or directory, readlink '/etc/ld.so.preload'"}}}), 'claims say False (path must be INSIDE the extraction tree)')
# ENOENT+readlink naming a path inside the tree (the intended case)
cases['enoent_path_inside_tree'] = (r51_predicate({
    'category':'execution_failure','code':'execution_failure',
    'details':{'diagnostics':{'reason':"ENOENT: no such file or directory, readlink '/tmp/w/rea-firmware-X/extracted/firmware.bin_extract/usr/www.myfritz/avme/cgi-bin/luacgi'"}}}), 'claims say True')
# a DIFFERENT execution_failure (no ENOENT) -> correctly False
cases['other_execution_failure'] = (r51_predicate({
    'category':'execution_failure','code':'execution_failure',
    'details':{'diagnostics':{'reason':'Extraction failed: corrupt xz stream'}}}), 'claims say False')
out['probe_B_predicate_breadth'] = {k: {'predicate_says_retryable': v[0], 'claims_expectation': v[1]} for k, v in cases.items()}

# ---------- probe C: truncation of the captured diagnostic ----------
t = json.dumps(ERR_REAL)
out['probe_C_truncation'] = {
    'full_error_json_len': len(t),
    'r51_capture_rule': "replayed['enoent_readlink_retry'] = err_text[:300]",
    'captured_300': t[:300],
    'captured_len': len(t[:300]),
    'dropped_tail': t[300:],
    'drops_retryable_false': '"retryable": false' in t[300:],
    'full_path_visible_in_capture': "/usr/www.myfritz/avme/cgi-bin/luacgi'" in t[:300],
    'full_path_visible_in_full': True,
}

# ---------- probe A: the REAL v1 counter runner, stub REA package ----------
stubdir = os.path.join(S, 'stub'); shutil.rmtree(stubdir, ignore_errors=True); os.makedirs(stubdir)
pkg = os.path.join(stubdir, 'pkg'); os.makedirs(os.path.join(pkg, 'scripts'))
json.dump({'name':'rea-agents','version':'6.5.0','type':'module','bin':{'rea-agents':'scripts/rea.mjs'}},
          open(os.path.join(pkg,'package.json'),'w'))
with open(os.path.join(pkg,'scripts','rea.mjs'),'w') as fh:
    fh.write('''import fs from "node:fs";
const cf = process.env.STUB_COUNT_FILE;
const mode = process.env.STUB_MODE; // "enoent_then_ok" | "always_enoent"
let n = 0;
try { n = parseInt(fs.readFileSync(cf, "utf8"), 10); } catch {}
n += 1; fs.writeFileSync(cf, String(n));
const outdir = process.argv[process.argv.length - 1];
fs.mkdirSync(outdir, {recursive: true});
if (mode === "always_enoent" || n <= 1) {
  console.log(JSON.stringify({ok:false, error:{
    category:"execution_failure", code:"execution_failure",
    details:{diagnostics:{reason:"ENOENT: no such file or directory, readlink '" + outdir + "/firmware.bin_extract/usr/www.myfritz/avme/cgi-bin/luacgi'"},
             operation:"extract_firmware", provider_id:"unblob"},
    message:"Analysis could not complete. Run `rea doctor` and review the reported details; repeating the unchanged request is not expected to succeed.",
    remediation:{action:"Analysis could not complete. Run `rea doctor` and review the reported details; repeating the unchanged request is not expected to succeed."},
    retryable:false}}));
} else {
  console.log(JSON.stringify({ok:true, data:{stub_success:true, subject:{digest:{sha256:"0"*64}}, normalized_result:{}}}));
}
''')
unblob = os.path.join(stubdir, 'unblob-26.6.4')
open(unblob,'w').write('#!/bin/sh\necho 26.6.4\n'); os.chmod(unblob, 0o755)

m = load(COUNTER, 'r50counter')
work = os.path.join(S, 'work'); shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
os.environ['STUB_COUNT_FILE'] = os.path.join(S, 'count')
os.environ['STUB_MODE'] = 'enoent_then_ok'
runner = m.make_real_runner(work, unblob, 30, pkg)
status, payload = runner(b'carrier-bytes', 'g7581', dict(m.FIXTURE_REA_PARAMETERS))
out['probe_A_retry_then_success'] = {
    'mode': 'attempt1 raises the exact ENOENT, attempt2 succeeds',
    'runner_status': status,
    'payload_top_level_keys': sorted(payload.keys()) if isinstance(payload, dict) else None,
    'replayed_present_in_success_payload': isinstance(payload, dict) and 'replayed' in payload,
    'attempts_present_in_success_payload': isinstance(payload, dict) and 'replayed' in payload and 'attempts' in payload['replayed'],
    'invocations_of_stub_REA': open(os.environ['STUB_COUNT_FILE']).read(),
    'note': 'the v1 runner returns (ok, data) on success and DISCARDS `replayed` (which holds attempts) - see c1-counter.py:2078-2088',
}
# now: attempt count actually performed
os.environ['STUB_COUNT_FILE'] = os.path.join(S, 'count2')
os.environ['STUB_MODE'] = 'always_enoent'
shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
runner2 = m.make_real_runner(work, unblob, 30, pkg)
status2, payload2 = runner2(b'carrier-bytes', 'g7581', dict(m.FIXTURE_REA_PARAMETERS))
out['probe_A_always_enoent'] = {
    'mode': 'every attempt raises the ENOENT',
    'runner_status': status2,
    'invocations_of_stub_REA': open(os.environ['STUB_COUNT_FILE']).read(),
    'MAX_REA_ATTEMPTS_in_v1': m.MAX_REA_ATTEMPTS,
    'attempts_recorded_in_failure_payload': payload2.get('replayed', {}).get('attempts') if isinstance(payload2, dict) else None,
    'failure_payload_keys': sorted(payload2.keys()) if isinstance(payload2, dict) else None,
    'error_retryable_flag': (payload2.get('error') or {}).get('retryable') if isinstance(payload2, dict) else None,
    'err_text_len_if_serialised': len(json.dumps(payload2.get('error'))) if isinstance(payload2, dict) and payload2.get('error') else 0,
}
# what the v1 MEASURE stage would do with each of those two payloads
out['probe_A_measure_verdict'] = {}
for label, p in (('success_after_retry', payload), ('always_enoent', payload2)):
    perr = p.get('error') if isinstance(p, dict) else None
    if isinstance(perr, dict) and perr.get('code') == 'provider_timeout':
        verdict = 'RerunEnvError -> exit 2 (could-not-evaluate)'
    else:
        verdict = "projection_ok=False -> exit 1 RED (the claim misses)"
    out['probe_A_measure_verdict'][label] = verdict

out['probe_A_note_no_REA_invoked'] = 'the stub package is a local 3-line .mjs; the real rea-agents package was NEVER executed'
print(json.dumps(out, indent=1, sort_keys=True))
