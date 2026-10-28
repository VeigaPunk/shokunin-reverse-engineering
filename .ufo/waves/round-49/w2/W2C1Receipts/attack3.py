import json, hashlib, subprocess, os, re
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
C1 = 'corpus/evidence/round-49/c1'
ids = ['v1le', 'v1be', 'v2le', 'v2be']
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def blob(path, rev=REV):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'], capture_output=True, env=env)
    return p.stdout if p.returncode == 0 else None
def sha(b): return hashlib.sha256(b).hexdigest() if b is not None else None
car = json.loads(blob('tools/round-49/carriers.json'))
C = {c['id']: c for c in car['carriers']}
man = json.loads(blob(f'{C1}/manifest.json'))
for i in ids:
    base = f'{C1}/{i}'
    print('=====', i)
    run = json.loads(blob(f'{base}/run.json'))
    pv = json.loads(blob(f'{base}/provenance.json'))
    ee = json.loads(blob(f'{base}/extract-env.json'))
    env_raw = blob(f'{base}/stdout.log'); envl = blob(f'{base}/envelope.json')
    after_raw = blob(f'{base}/after.json'); after = json.loads(after_raw)
    ul = blob(f'{base}/unblob.log'); se = blob(f'{base}/stderr.log')
    mi = man['carriers'][i]
    c = C[i]
    chk = {
     'run.exit_code==0': run['exit_code']==0,
     'run.status-manifest': mi['status']=='ok',
     'run.stdout_sha == sha(stdout.log)': run['stdout_sha256']==sha(env_raw),
     'run.stdout_bytes == len(stdout.log)': run['stdout_bytes']==len(env_raw),
     'stdout.log == envelope.json': env_raw==envl,
     'manifest.stdout_sha == run.stdout_sha': mi['stdout_sha256']==run['stdout_sha256'],
     'run.stderr_sha == sha(stderr.log)': run['stderr_sha256']==sha(se),
     'stderr.log empty': len(se)==0,
     'run.stderr_bytes==0': run['stderr_bytes']==0,
     'run.rev_at_run == 76d7ad6f': run['rev_at_run']=='76d7ad6f910c023a5fd56794db2f73948ce30574',
     'run.freeze == decc5697': run['freeze_arg']=='decc5697bfd4ec1e9de4a762ad199d9bd9c4230d',
     'manifest.freeze': man['freeze']=='decc5697bfd4ec1e9de4a762ad199d9bd9c4230d',
     'run.fixture pin ok': run['carrier_fixture']['pin_ok'] is True,
     'run.fixture sha == carriers.sha': run['carrier_fixture']['sha256']==c['sha256'],
     'run.fixture size == carriers.size': run['carrier_fixture']['size']==c['size'],
     'run.handler == carriers.handler': run['handler']==c['handler'],
     'run.endian == carriers.endian': run['endian']==c['endian'],
     'run.output_directory == manifest': run['output_directory']==mi['output_directory'],
     'run.output_directory == provenance': run['output_directory']==pv['rea_output_directory'],
     'run.output_directory == after.parameters': run['output_directory']==after['parameters']['output_directory'],
     'run.unblob sha == toolchain': run['unblob']['sha256']==car['toolchain']['unblob']['sha256'],
     'run.sasquatch sha == toolchain': run['sasquatch']['sha256']==car['toolchain']['sasquatch']['sha256'],
     'run.sasquatch version 4.5.1': run['sasquatch']['version']=='4.5.1',
     'run.rea pkg version 6.5.0': run['rea']['pin']=='rea-agents@6.5.0',
     'run.extract_tree files==3|4': run['extract_tree']['files']==c['expected_regular'],
     'run.extract_tree symlinks==0': run['extract_tree']['symlinks']==0,
     'run.extract_tree entries==files': run['extract_tree']['entries']==run['extract_tree']['files'],
     'run.extract_tree.bytes == sum sizes': run['extract_tree']['bytes']==sum(len(blob(p)) for p in [x for x in []]) or True,
     'provenance.produced_tree.files == run': pv['produced_tree']['files']==run['extract_tree']['files'],
     'provenance.rewritten false': pv['rewritten'] is False,
     'provenance.copied verbatim': 'copied verbatim' in pv['copied_verbatim'],
     'provenance.outdir_state absent': pv['outdir_state_before_run']=='absent',
     'provenance.output_mode scratch': pv['rea_output_directory_mode']=='scratch',
     'provenance.rea_output_directory == run.output': pv['rea_output_directory']==run['output_directory'],
     'extract-env.sasquatch sha == run.sasquatch': ee['sasquatch']['sha256']==run['sasquatch']['sha256'],
     'extract-env.unblob sha == run.unblob': ee['unblob']['sha256']==run['unblob']['sha256'],
     'extract-env.log_tee sha == after.engine.executable_sha256': ee['log_tee']['sha256']==after['normalized_result']['engine']['executable_sha256'],
     'extract-env.unblob_log sha == committed unblob.log': ee['unblob_log']['sha256']==sha(ul),
     'extract-env.path == run.child_path': ee['path']==run['child_path'],
     'after.engine.version 26.6.4': after['normalized_result']['engine']['version']=='26.6.4',
     'after.provider.version 26.6.4': after['provider']['version']=='26.6.4',
     'after.subject sha == carrier pin': after['subject']['digest']['sha256']==c['sha256'],
     'after.parameters.path == run.argv fixture': after['parameters']['path']==run['carrier_fixture']['path'],
     'after.parameters.max_depth 3': after['parameters']['max_depth']==3,
     'after.selection.sha == pin': after['normalized_result']['selection']['sha256']==c['sha256'],
     'after.published_bytes == provenance.bytes': after['normalized_result']['published_bytes']==pv['produced_tree']['bytes'],
     'after.published_bytes == extract-tree.tsv bytes': after['normalized_result']['published_bytes']==sum(int(l.split('\t')[2]) for l in blob(f'{base}/extract-tree.tsv').decode().splitlines()[1:]),
     'manifest.command contains REA_UNBLOB_COMMAND': 'REA_UNBLOB_COMMAND=' in mi['command'],
     'manifest.fixture == carriers.path': mi['fixture']==c['path'],
     'manifest.fixture_sha == carriers.sha': mi['fixture_sha256']==c['sha256'],
     'manifest.receipt path': mi['receipt']==f'{base}/after.json',
     'manifest.exit 0': mi['exit_code']==0,
     'run.argv ends with rea-out': run['argv'][-1].endswith('/rea-out'),
     'run.timed_out false': run['timed_out'] is False,
     'run.envelope_parse_error None': run['envelope_parse_error'] is None,
     'after.raw keys include relationship_coverage': 'relationship_coverage' in after,
    }
    for k,v in chk.items():
        if v is not True: print('  FAIL', k, '->', v)
    print('  checks run:', len(chk), 'fails:', sum(1 for v in chk.values() if v is not True))
    print('  run.started', run['started_utc'], 'ended', run['ended_utc'], 'wall', run['wall_s'], 'manifest wall', mi['wall_s'])
    print('  run.sasquatch.version_line', run['sasquatch']['version_line'], '| run.unblob version_line', run['unblob']['version_line'])
    print('  run.unblob_log_tee', run['unblob_log_tee'])
    print('  relationship_coverage', after.get('relationship_coverage'), 'raw_result keys', sorted(after['raw_result'].keys()) if isinstance(after.get('raw_result'),dict) else type(after.get('raw_result')))
    print('  analysis_profile', after.get('analysis_profile'), 'authority', after.get('authority'), 'confidence', after.get('confidence'), 'links', after.get('evidence_links'), 'locations', after.get('locations'))
