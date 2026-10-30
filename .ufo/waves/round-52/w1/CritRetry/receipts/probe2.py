import importlib.util, json, os, shutil, sys, hashlib, datetime

S = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DRAFT = os.path.join(LANE, '.ufo/waves/round-51/l1/drafts/c1-counter.py')

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

def sha256(b): return hashlib.sha256(b).hexdigest()

stubdir = os.path.join(S, 'stub'); pkg = os.path.join(stubdir,'pkg')
m = load(DRAFT, 'r51draft')
out = {'probe':'CritRetry probe2 against the r51 L1 DRAFT counter (the closest ancestor of the v2 counter)',
       'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'draft_path': DRAFT, 'draft_sha256': sha256(open(DRAFT,'rb').read()),
       'MAX_REA_ATTEMPTS': m.MAX_REA_ATTEMPTS}

unblob = os.path.join(stubdir,'unblob-26.6.4')

def run(mode, label):
    cf = os.path.join(S,'c_%s' % label)
    if os.path.exists(cf): os.remove(cf)
    os.environ['STUB_COUNT_FILE'] = cf
    os.environ['STUB_MODE'] = mode
    work = os.path.join(S,'w_%s' % label); shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
    r = m.make_real_runner(work, unblob, 30, pkg)
    status, payload = r(b'carrier-bytes', 'g7581', dict(m.FIXTURE_REA_PARAMETERS))
    return status, payload, open(cf).read()

# 1. ENOENT then OK  -> does a retry happen? is the attempt recorded on SUCCESS?
st, pl, n = run('enoent_then_ok','ok')
out['r51_draft_ENOENT_then_success'] = {
  'stub_invocations': n, 'runner_status': st,
  'payload_keys': sorted(pl.keys()) if isinstance(pl,dict) else None,
  'attempts_in_payload': (pl.get('replayed') or {}).get('attempts') if isinstance(pl,dict) else None,
  'enoent_readlink_retry_recorded': (pl.get('replayed') or {}).get('enoent_readlink_retry') is not None if isinstance(pl,dict) and isinstance(pl.get('replayed'),dict) else False,
  'VERDICT': 'retry happened and the diagnostic+count SURVIVED' if isinstance(pl,dict) and isinstance(pl.get('replayed'),dict) and pl['replayed'].get('attempts',0)>1 else 'DIAGNOSTIC LOST: success path returns (ok, data) and DROPS `replayed` (draft:2145-2155)'}

# 2. always ENOENT -> how many invocations, what does measure() do?
st2, pl2, n2 = run('always_enoent','bad')
perr = pl2.get('error') if isinstance(pl2,dict) else None
perr_text = json.dumps(perr) if isinstance(perr,dict) else ''
enoent_flake = (perr.get('code')=='execution_failure' and 'ENOENT' in perr_text and 'readlink' in perr_text) if isinstance(perr,dict) else False
measure_branch = ('RerunEnvError -> exit 2 (could-not-evaluate, NOT red)'
                  if (isinstance(perr,dict) and (perr.get('code')=='provider_timeout' or enoent_flake))
                  else "projection_ok=False -> exit 1 RED")
out['r51_draft_always_ENOENT'] = {
  'stub_invocations': n2, 'runner_status': st2,
  'attempts_recorded': (pl2.get('replayed') or {}).get('attempts') if isinstance(pl2,dict) else None,
  'enoent_readlink_retry_captured': (pl2.get('replayed') or {}).get('enoent_readlink_retry') if isinstance(pl2,dict) and isinstance(pl2.get('replayed'),dict) else None,
  'measure_stage_branch': measure_branch,
  'CONFLICT': ('the r52 claims demand the deterministic-ENOENT control score RED; this inherited branch yields exit 2' if measure_branch.startswith('RerunEnvError') else None)}

# 3. how many invocations would the r52-claims budget (2 attempts) need vs the inherited 3?
out['budget'] = {'inherited_MAX_REA_ATTEMPTS': m.MAX_REA_ATTEMPTS,
  'r52_claims_enoent_budget_text': 'up to 2 attempts on an execution_failure whose failing diagnostic is an ENOENT naming a path inside the extraction tree',
  'inherited_semantics': 'attempts < MAX_REA_ATTEMPTS -> 3 TOTAL invocations for BOTH classes (one shared counter); the claims need 3 for timeout but 2 for ENOENT -> a SECOND constant, not a port'}

# 4. predicate breadth, verbatim from draft:2135-2137
def pred(err):
    t = json.dumps(err) if err else ''
    return (err.get('code')=='execution_failure' and 'ENOENT' in t and 'readlink' in t)
out['predicate_breadth'] = {
  'enoent_outside_extraction_tree_is_retried': pred({'code':'execution_failure','details':{'diagnostics':{'reason':"ENOENT: no such file or directory, readlink '/etc/ld.so.preload'"}}}),
  'enoent_in_boilerplate_message_only_is_retried': pred({'code':'execution_failure','message':'ENOENT: no such file or directory, readlink x','details':{'diagnostics':{'reason':'unrelated'}}}),
  'claims_require': "an ENOENT NAMING A PATH INSIDE THE EXTRACTION TREE - the inherited predicate checks neither the path nor the tree"}
print(json.dumps(out, indent=1, sort_keys=True))
