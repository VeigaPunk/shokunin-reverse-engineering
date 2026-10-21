#!/usr/bin/env python3
"""Independently declared finite counter controls; mutations only in temporary Git.

Expected counts/statuses below are fixed, not derived from counter decisions.
The candidate counter is invoked as a subprocess for every case.
"""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import os

T1 = ['identify-flutter-build', 'inspect-dart-aot', 'debug-with-gdb',
      'debug-with-rizin', 'inspect-signal-decoders', 'decode-signal-recording']
T2 = ['inspect-packet-fields','inspect-packet-capture','inspect-pcap-client',
      'inspect-pcap-capture','list-cutter-sessions','cutter-command',
      'list-frida-devices','list-frida-processes','instrument-with-frida',
      'inspect-adb-package','list-adb-services','inspect-adb-window',
      'start-adb-activity','stop-adb-app']
PREFIX = '.ufo/waves/round-22/evidence/'
DEPS = ['.ufo/waves/round-20/tools/verb-coverage.py',
        '.ufo/waves/round-21/tools/verb-coverage.py',
        '.ufo/waves/round-20/verify/round20/verb-coverage.json']


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def put(root, rel, content):
    target = root / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        target.write_bytes(content)
    else:
        target.write_text(content, encoding='utf-8')


def c1_files():
    files = {}
    path = 'corpus/knowledge/fixture.md'
    text = 'source: S051\nverified-at: 2026-10-21\nrecheck: fixture\n'
    operations = ['identify_flutter_build', 'inspect_dart_aot', 'gdb_console',
                  'rizin_debug_command', 'inspect_signal_decoders', 'decode_signal_recording']
    for i, verb in enumerate(T1):
        evidence_id = 'ev_' + format(i + 1, '064x')
        rel = PREFIX + 'c1/' + verb + '.json'
        files[rel] = json.dumps({'ok':True,
                                'data':{'evidence_id':evidence_id,'operation':operations[i]},
                                'meta':{'command':verb}})
        text += f'\n{verb} {evidence_id} {rel}\n'
    files[path] = text
    files['corpus/SOURCES.md'] = ('# SOURCES\n## Registry\n'
        '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
        '|---|---|---|---|---|---|---|---|---|---|---|\n'
        '| S051 | fixture | own-work | A | fixture | exact | fixture | mined | 2026-10-21 | on-release | corpus/knowledge/fixture.md |\n')
    return files


def c2_files():
    files = {}
    rows = ['### Round-22 catalog dispositions',
            '| verb | placement | probe | observed | receipt | reason |',
            '|---|---|---|---|---|---|']
    for verb in T2:
        rel = PREFIX + 'c2/' + verb + '.json'
        files[rel] = json.dumps({'ok':False, 'error':{'code':'capability_unavailable'},
                                'meta':{'command':verb}})
        rows.append(f'| {verb} | frontier-blocked | {verb} | error:capability_unavailable | {rel} | explicit fixture |')
    files['PROVINCE.md'] = '\n'.join(rows) + '\n'
    return files


def cases(claim):
    if claim == 'C1':
        base = c1_files()
        output = [('all_six', base, 0, 6, None)]
        for name in ['missing_source','refusal','split_record','uncited_path','duplicate_json',
                     'wrong_command','extraction_only','refused_with_extraction',
                     'forged_debug_operation','helper_drift','source_queued','source_old_date',
                     'source_old_id','source_wrong_used_by','tier_c_only','missing_registry',
                     'invalid_revision','nested_refusal','record_refusal','normalized_refusal',
                     'overflow_metadata','directory_citation','meta_error','meta_exit',
                     'duplicate_source_id','source_not_header','array_refusal',
                     'non_utf8_evidence','committed_helper_change']:
            mutant = copy.deepcopy(base)
            if name == 'missing_source':
                mutant['corpus/knowledge/fixture.md'] = mutant['corpus/knowledge/fixture.md'].replace('source: S051', 'source: none')
            elif name=='source_not_header':
                mutant['corpus/knowledge/fixture.md']='# body first\n'+mutant['corpus/knowledge/fixture.md']
            elif name=='duplicate_source_id':
                mutant['corpus/SOURCES.md']+=mutant['corpus/SOURCES.md'].splitlines()[-1]+'\n'
            elif name.startswith('source_') or name=='tier_c_only':
                row=mutant['corpus/SOURCES.md']
                if name=='source_queued': row=row.replace('| mined |','| queued |')
                if name=='source_old_date': row=row.replace('2026-10-21','2026-10-20')
                if name=='source_old_id':
                    row=row.replace('S051','S050')
                    mutant['corpus/knowledge/fixture.md']=mutant['corpus/knowledge/fixture.md'].replace('S051','S050')
                if name=='source_wrong_used_by': row=row.replace('corpus/knowledge/fixture.md |','corpus/knowledge/other.md |')
                if name=='tier_c_only': row=row.replace('| own-work | A |','| own-work | C |')
                mutant['corpus/SOURCES.md']=row
            elif name=='missing_registry':
                del mutant['corpus/SOURCES.md']
            else:
                for verb in T1:
                    rel = PREFIX + 'c1/' + verb + '.json'
                    record = json.loads(mutant[rel])
                    if name in ('refusal','refused_with_extraction'):
                        record['ok'] = False
                        record['error'] = {'code':'capability_unavailable'}
                    if name == 'split_record':
                        data = record['data']
                        record['data'] = [dict(data,operation='other'),dict(data,evidence_id='ev_'+'f'*64)]
                    if name == 'wrong_command':
                        record['meta']['command'] = 'other'
                    if name=='nested_refusal':
                        record['data']={'result':{'ok':False,'evidence':record['data']}}
                    if name=='record_refusal':
                        record['data']['ok']=False
                    if name=='normalized_refusal':
                        record['data']['normalized_result']={'ok':False}
                    if name=='array_refusal':
                        record['data']['raw_result']=[{'ok':False,'error':{'code':'capability_unavailable'}}]
                    if name=='overflow_metadata':
                        record['meta']['overflow']=float('inf')
                    if name=='meta_error':
                        record['meta']['error']={'code':'execution_failure'}
                    if name=='meta_exit':
                        record['meta']['exit_code']=1
                    if name=='directory_citation':
                        mutant['corpus/knowledge/fixture.md']=mutant['corpus/knowledge/fixture.md'].replace(rel,PREFIX+'c1/')
                    if name == 'forged_debug_operation' and verb in ('debug-with-gdb','debug-with-rizin'):
                        record['data']['operation'] = verb.replace('-','_')
                    if name == 'refused_with_extraction':
                        derived = PREFIX+'c1/'+verb+'.derived.json'
                        mutant[derived] = json.dumps(record['data'])
                        mutant['corpus/knowledge/fixture.md'] += '\n'+derived+'\n'
                    if name == 'extraction_only':
                        record = record['data']
                    if name == 'uncited_path':
                        mutant['corpus/knowledge/fixture.md'] = mutant['corpus/knowledge/fixture.md'].replace(rel,'not-cited')
                    mutant[rel] = (json.dumps(record)[:-1] + ',"ok":true}') if name == 'duplicate_json' else json.dumps(record)
                    if name=='overflow_metadata':
                        mutant[rel]=mutant[rel].replace('Infinity','1e999')
                    if name=='non_utf8_evidence':
                        mutant[rel]=mutant[rel].encode()[:-1]+b',"extra":"\xff"}'
            expected_count = None if name in ('missing_registry','invalid_revision','duplicate_source_id','non_utf8_evidence','committed_helper_change') else 6 if name=='helper_drift' else 4 if name=='forged_debug_operation' else 0
            expected_exit = 2 if expected_count is None else 0 if name=='helper_drift' else 1
            output.append((name, mutant, expected_exit, expected_count, None))
        return output
    base = c2_files()
    output = [('all_fourteen', base, 0, 14, None)]
    for name, status in [('probe_alias','probe_mismatch'),('wrong_code','observed_mismatch'),
                         ('duplicate_row','duplicate_rows'),('outside_path','receipt_outside_prefix'),
                         ('duplicate_json','receipt_unevaluable'),('empty_section','unaccounted'),
                         ('receipt_absent','receipt_absent'),('bad_placement','bad_placement'),
                         ('missing_reason','missing_reason'),('foreign_row','matched'),
                         ('ok_empty_positive','matched'),('ok_empty_nonempty','observed_mismatch'),
                         ('ok_field_positive','matched'),('ok_field_wrong','observed_mismatch'),
                         ('boolean_number','observed_mismatch'),('nested_boolean_number','observed_mismatch'),
                         ('overflow_number','receipt_unevaluable'),('tiny_number','observed_mismatch'),
                         ('recursive_receipt','receipt_not_envelope'),('heading_spoof','unaccounted'),
                         ('duplicate_section',None),('malformed_row',None),('invalid_revision',None),
                         ('non_utf8','receipt_unevaluable'),('fenced_example','matched'),
                         ('fenced_only','unaccounted'),('empty_error','bad_observed_grammar'),
                         ('comment_duplicate','duplicate_rows')]:
        mutant = copy.deepcopy(base)
        verb = T2[0]
        rel = PREFIX + 'c2/' + verb + '.json'
        if name == 'probe_alias':
            mutant['PROVINCE.md'] = mutant['PROVINCE.md'].replace(f'| {verb} | error:', '| inspect-pcap-client | error:')
            record = json.loads(mutant[rel]); record['meta']['command'] = 'inspect-pcap-client'; mutant[rel] = json.dumps(record)
        if name == 'wrong_code': mutant[rel] = mutant[rel].replace('capability_unavailable','invalid_request')
        if name == 'duplicate_row': mutant['PROVINCE.md'] += mutant['PROVINCE.md'].splitlines()[3] + '\n'
        if name == 'outside_path': mutant['PROVINCE.md'] = mutant['PROVINCE.md'].replace(rel, 'outside.json')
        if name == 'duplicate_json': mutant[rel] = mutant[rel][:-1] + ',"ok":false}'
        if name == 'empty_section': mutant['PROVINCE.md'] = '# Province\n'
        if name=='receipt_absent': del mutant[rel]
        if name=='bad_placement': mutant['PROVINCE.md']=mutant['PROVINCE.md'].replace('| frontier-blocked |','| bogus |',1)
        if name=='missing_reason': mutant['PROVINCE.md']=mutant['PROVINCE.md'].replace('| explicit fixture |','| |',1)
        if name=='foreign_row': mutant['PROVINCE.md']+='| foreign | adjacent | foreign | error:x | absent.json | fixture |\n'
        if name.startswith('ok_empty'):
            mutant['PROVINCE.md']=mutant['PROVINCE.md'].replace('error:capability_unavailable','ok-empty:items',1)
            mutant[rel]=json.dumps({'ok':True,'data':{'items':[] if name=='ok_empty_positive' else [1]},'meta':{'command':verb}})
        if name.startswith('ok_field') or name in ('boolean_number','nested_boolean_number','tiny_number'):
            literal='null' if name.startswith('ok_field') else '[false]' if name=='nested_boolean_number' else '0' if name=='tiny_number' else 'false'
            value=None if name=='ok_field_positive' else False if name=='ok_field_wrong' else [0] if name=='nested_boolean_number' else 0
            mutant['PROVINCE.md']=mutant['PROVINCE.md'].replace('error:capability_unavailable','ok-field:value='+literal,1)
            mutant[rel]=json.dumps({'ok':True,'data':{'value':value},'meta':{'command':verb}})
            if name=='tiny_number': mutant[rel]=mutant[rel].replace('\"value\": 0','\"value\": 1e-999')
        if name=='overflow_number':
            mutant[rel]='{\"ok\":false,\"error\":{\"code\":\"capability_unavailable\"},\"meta\":{\"command\":\"'+verb+'\"},\"extra\":1e999}'
        if name=='recursive_receipt': mutant[rel]='['*2000+'0'+']'*2000
        if name=='heading_spoof': mutant['PROVINCE.md']=mutant['PROVINCE.md'].replace('### Round-22 catalog dispositions','### Round-22 catalog dispositions decoy')
        if name=='duplicate_section': mutant['PROVINCE.md']+=mutant['PROVINCE.md']
        if name=='malformed_row': mutant['PROVINCE.md']+='| unknown | adjacent | rogue |\n'
        if name=='non_utf8': mutant[rel]=b'\xff'
        if name=='fenced_example': mutant['PROVINCE.md']='```\n'+base['PROVINCE.md']+'```\n'+base['PROVINCE.md']
        if name=='fenced_only': mutant['PROVINCE.md']='~~~\n'+base['PROVINCE.md']+'~~~\n'
        if name=='empty_error':
            mutant['PROVINCE.md']=mutant['PROVINCE.md'].replace('error:capability_unavailable','error:',1)
            mutant[rel]=mutant[rel].replace('capability_unavailable','')
        if name=='comment_duplicate':
            mutant['PROVINCE.md']+='<!--\n# hidden heading\n-->\n'+base['PROVINCE.md'].splitlines()[3]+'\n'
        expected_exit=0 if name in ('ok_empty_positive','ok_field_positive','fenced_example') else 2 if name in ('duplicate_section','malformed_row','invalid_revision') else 1
        expected_count=None if expected_exit==2 else 14 if expected_exit==0 or name=='foreign_row' else 0 if name in ('empty_section','heading_spoof','fenced_only') else 13
        output.append((name, mutant, expected_exit, expected_count, status))
    return output


def run(claim, counter, source):
    results=[]
    with tempfile.TemporaryDirectory(prefix='kaidoku-r22-fixtures-') as directory:
        root = Path(directory)/'main'
        foreign = Path(directory)/'foreign'
        for repo in (root,foreign):
            repo.mkdir()
            git(repo,'init','-q')
            git(repo,'config','user.name','fixture')
            git(repo,'config','user.email','fixture@invalid.local')
        put(foreign,'README','unrelated repository\n')
        git(foreign,'add','README');git(foreign,'commit','-qm','foreign')
        for dependency in DEPS:
            put(root, dependency, (Path(source)/dependency).read_text())
        prior = set()
        case_rows=cases(claim)
        for name in ('git_dir_control','replace_ref_control'):
            case_rows.append((name,c1_files() if claim=='C1' else c2_files(),0,6 if claim=='C1' else 14,None))
        for name, files, expected_exit, expected_count, expected_status in case_rows:
            for old in prior - set(files): (root/old).unlink()
            for rel, text in files.items(): put(root, rel, text)
            prior = set(files)
            if name=='committed_helper_change':
                helper_path=root/DEPS[1]
                helper_path.write_text('# unreviewed helper change\n'+helper_path.read_text())
            git(root,'add','--all'); git(root,'commit','-qm',name,'--allow-empty')
            revision=git(root,'rev-parse','HEAD')
            if name=='invalid_revision':
                revision='not-a-revision'
            helper = root / DEPS[1]
            helper_bytes = helper.read_bytes()
            if name == 'helper_drift':
                helper.write_text('raise RuntimeError("uncommitted_helper_executed")\n')
            env=dict(os.environ)
            env_overrides={}
            if name=='git_dir_control':
                env['GIT_DIR']=str(foreign/'.git')
                env_overrides['GIT_DIR']=env['GIT_DIR']
            if name=='replace_ref_control':
                empty=subprocess.run(['git','-C',str(root),'mktree'],input='',capture_output=True,text=True,check=True).stdout.strip()
                replacement=git(root,'commit-tree',empty,'-m','unrelated replacement')
                git(root,'replace',revision,replacement)
                env.pop('GIT_NO_REPLACE_OBJECTS',None)
                env_overrides['GIT_NO_REPLACE_OBJECTS']=None
            proc=subprocess.run([sys.executable,'-I','-B',str(counter),'--root',str(root),'--rev',revision],capture_output=True,text=True,env=env)
            if name=='replace_ref_control':
                git(root,'replace','-d',revision)
            if name == 'helper_drift':
                helper.write_bytes(helper_bytes)
            if name=='committed_helper_change':
                helper.write_bytes((Path(source)/DEPS[1]).read_bytes())
            try: data=json.loads(proc.stdout)
            except ValueError: data={}
            count=data.get('t1_exercised_count' if claim=='C1' else 'accounted_count')
            status=data.get('per_verb',{}).get(T2[0],{}).get('status') if claim=='C2' else None
            finding_id=data.get('finding')
            expected_finding='unevaluable' if expected_exit==2 else ('c1_complete' if expected_exit==0 else 'c1_incomplete') if claim=='C1' else ('dispositions_complete' if expected_exit==0 else 'dispositions_incomplete')
            ok=proc.returncode==expected_exit and count==expected_count and finding_id==expected_finding and (expected_status is None or status==expected_status)
            results.append({'id':name,'finding_id':finding_id,'expected_finding_id':expected_finding,'argv':proc.args,'env_overrides':env_overrides,'expected_exit':expected_exit,'expected_count':expected_count,'expected_status':expected_status,'exit':proc.returncode,'count':count,'status':status,'stdout':proc.stdout,'stderr':proc.stderr,'pass':ok})
    clean=all(row['pass'] for row in results)
    return {'finding':'counter_controls_clean' if clean else 'counter_controls_failed','claim':claim,'cases':results}, 0 if clean else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--claim',choices=['C1','C2'],required=True)
    parser.add_argument('--counter',required=True)
    parser.add_argument('--root',required=True)
    args=parser.parse_args()
    result,code=run(args.claim,Path(args.counter).resolve(),args.root)
    print(json.dumps(result,sort_keys=True))
    return code


if __name__=='__main__':
    raise SystemExit(main())
