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
    target.write_text(content, encoding='utf-8')


def c1_files():
    files = {}
    path = 'corpus/knowledge/fixture.md'
    text = 'source: S051\nverified-at: 2026-10-21\nrecheck: fixture\n'
    for i, verb in enumerate(T1):
        evidence_id = 'ev_' + format(i + 1, '064x')
        rel = PREFIX + 'c1/' + verb + '.json'
        files[rel] = json.dumps({'evidence_id': evidence_id,
                                'operation': verb.replace('-', '_')})
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
        for name in ['missing_source','refusal','split_record','uncited_path','duplicate_json']:
            mutant = copy.deepcopy(base)
            if name == 'missing_source':
                mutant['corpus/knowledge/fixture.md'] = mutant['corpus/knowledge/fixture.md'].replace('source: S051', 'source: none')
            else:
                for verb in T1:
                    rel = PREFIX + 'c1/' + verb + '.json'
                    record = json.loads(mutant[rel])
                    if name == 'refusal': record['error'] = {'code':'execution_failure'}
                    if name == 'split_record': record = [dict(record,operation='other'),dict(record,evidence_id='ev_'+'f'*64)]
                    if name == 'uncited_path':
                        mutant['corpus/knowledge/fixture.md'] = mutant['corpus/knowledge/fixture.md'].replace(rel,'not-cited')
                    mutant[rel] = (json.dumps(record)[:-1] + ',"operation":"wrong"}') if name == 'duplicate_json' else json.dumps(record)
            output.append((name, mutant, 1, 0, None))
        return output
    base = c2_files()
    output = [('all_fourteen', base, 0, 14, None)]
    for name, status in [('probe_alias','probe_mismatch'),('wrong_code','observed_mismatch'),
                         ('duplicate_row','duplicate_rows'),('outside_path','receipt_outside_prefix'),
                         ('duplicate_json','receipt_unevaluable'),('empty_section','unaccounted')]:
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
        output.append((name, mutant, 1, 0 if name=='empty_section' else 13, status))
    return output


def run(claim, counter, source):
    results=[]
    with tempfile.TemporaryDirectory(prefix='kaidoku-r22-fixtures-') as directory:
        root = Path(directory)
        git(root,'init','-q')
        git(root,'config','user.name','fixture')
        git(root,'config','user.email','fixture@invalid.local')
        for dependency in DEPS:
            put(root, dependency, (Path(source)/dependency).read_text())
        prior = set()
        for name, files, expected_exit, expected_count, expected_status in cases(claim):
            for old in prior - set(files): (root/old).unlink()
            for rel, text in files.items(): put(root, rel, text)
            prior = set(files)
            git(root,'add','--all'); git(root,'commit','-qm',name,'--allow-empty')
            revision=git(root,'rev-parse','HEAD')
            proc=subprocess.run([sys.executable,'-I','-B',str(counter),'--root',str(root),'--rev',revision],capture_output=True,text=True)
            try: data=json.loads(proc.stdout)
            except ValueError: data={}
            count=data.get('t1_exercised_count' if claim=='C1' else 'accounted_count')
            status=data.get('per_verb',{}).get(T2[0],{}).get('status') if claim=='C2' else None
            finding_id=data.get('claim')
            ok=proc.returncode==expected_exit and count==expected_count and finding_id=='R22-'+claim and (expected_status is None or status==expected_status)
            results.append({'id':name,'finding_id':finding_id,'expected_finding_id':'R22-'+claim,'argv':proc.args,'expected_exit':expected_exit,'expected_count':expected_count,'expected_status':expected_status,'exit':proc.returncode,'count':count,'status':status,'stdout':proc.stdout,'stderr':proc.stderr,'pass':ok})
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
