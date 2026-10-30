#!/usr/bin/env python3
"""Receipt collector for the R52-C1 knowledge-entry draft (ScribeEntryC1).

Runs each named measurement command over COMMITTED lane bytes, records
(id, UTC, exit code, stdout sha256, exact command) into a TSV, and prints the
TSV. Read-only: no command writes to the lane tree; no REA, no download, no
vendor byte. Exit codes are semantic: 0 met/clean, 1 not met/violation,
2 could-not-evaluate.

Usage: python3 -I -B receipts-collect.py --lane <LANE> --out <TSV>
"""
import argparse
import datetime
import hashlib
import os
import subprocess
import sys

SEAT = '.ufo/waves/round-52/w1/ScribeEntryC1'
COUNTER_DRAFT = '.ufo/waves/round-52/w1/ExecCounterV2/c1-counter.py'

COMMANDS = [
    ('census-char-devices',
     "for f in c6430 c6490 g7581 g7582; do n=$(awk -F'\\t' '$2==\"char-device\"' "
     "tools/round-50/oracle/$f.nonregular.tsv | wc -l); echo \"$f char-device=$n\"; done"),
    ('census-kinds',
     "for f in c6430 c6490 g7581 g7582; do echo \"== $f\"; "
     "awk -F'\\t' '{c[$2]++}END{for(k in c)printf \"  %s=%d\\n\",k,c[k]}' "
     "tools/round-50/oracle/$f.nonregular.tsv; done"),
    ('census-fritzbox-twelve',
     "for f in g7581 g7582; do n=$(awk -F'\\t' '$2==\"char-device\" && $1!=\"dev/led\"' "
     "tools/round-50/oracle/$f.nonregular.tsv | wc -l); echo \"$f other-char-device=$n\"; done"),
    ('census-g7581-devices',
     "awk -F'\\t' '$2==\"char-device\"{print $1\"\\t\"$3}' "
     "tools/round-50/oracle/g7581.nonregular.tsv"),
    ('oracle-tables-sha',
     "sha256sum tools/round-50/oracle/*.nonregular.tsv tools/round-50/oracle/*.oracle.tsv"),
    ('gap-rule-r50-sha',
     "sha256sum tools/round-50/gap-rule.json"),
    ('gap-rule-r50-shape',
     "python3 -c \"import json;d=json.load(open('tools/round-50/gap-rule.json'));"
     "print('claim',d['claim']);print('allowed',json.dumps(d['allowed'],sort_keys=True));"
     "print('required',json.dumps(d['required'],sort_keys=True));"
     "print('silent',json.dumps(d['removed']['silent'],sort_keys=True))\""),
    ('r50-miss-receipt',
     "python3 -c \"import json;d=json.load(open('.ufo/waves/round-50/l1/scores/"
     "c1-after-attempt2.json'));print('carriers_matched',d['carriers_matched']);"
     "print('exit_code',d['exit_code']);print('target',d['target'])\""),
    ('r50-miss-carriers',
     "python3 -c \"import json;d=json.load(open('.ufo/waves/round-50/l1/scores/"
     "c1-after-attempt2.json'));[print(k,'gaps_ok',v.get('gaps_ok'),'projection_ok',"
     "v.get('projection_ok'),'nonregular_unpublished_ok',v.get('nonregular_unpublished_ok')) "
     "for k,v in sorted(d['carriers'].items())]\""),
    ('r50-gap-kinds-per-carrier',
     "for id in c6430 c6490 g7581 g7582; do python3 -c \"import json;from collections "
     "import Counter;d=json.load(open('corpus/evidence/round-50/c1/$id/after.json'));"
     "n=d['normalized_result'];print('$id','files',len(n['files']),'gaps',"
     "dict(Counter(x['kind'] for x in n['extraction_gaps'])))\"; done"),
    ('law-device-disposition',
     "python3 -I -B %s/entry-probes.py --lane . | sed -n '/^## law: device-row/,/^## rule-scoped/p'"
     % SEAT),
    ('rule-scope-offline',
     "python3 -I -B %s/entry-probes.py --lane . | sed -n '/^## rule-scoped/,/^## fail-closed/p'"
     % SEAT),
    ('failclosed-probe',
     "python3 -I -B %s/entry-probes.py --lane . | sed -n '/^## fail-closed/,/^## committed/p'"
     % SEAT),
    ('depth-gap-records',
     "python3 -c \"import json;[print(cid,json.dumps([{k:v.get(k) for k in "
     "('kind','input_path','relative_path','continuation_id')} for v in "
     "(json.load(open('corpus/evidence/round-50/c1/%s/after.json'%cid))['normalized_result']"
     "['extraction_gaps']) if v.get('kind')=='depth-limited'])) for cid in "
     "('c6430','c6490','g7581','g7582')]\""),
    ('knowledge-file-count',
     "git ls-tree -r --name-only HEAD corpus/knowledge | grep -c '\\.md$'"),
    ('sources-row-count',
     "grep -c '^| S[0-9][0-9][0-9] |' corpus/SOURCES.md"),
    ('sources-cited-rows-state',
     "python3 -I -B %s/entry-probes.py --lane . | sed -n '/^## SOURCES state/,$p'" % SEAT),
    ('counter-draft-import',
     "python3 -c \"import importlib.util,sys;s=importlib.util.spec_from_file_location("
     "'c','%s');m=importlib.util.module_from_spec(s);sys.modules['c']=m;"
     "s.loader.exec_module(m);print('IMPORT OK')\"" % COUNTER_DRAFT),
    ('counter-draft-claim-label',
     "grep -n \"!= 'R50-C1'\" " + COUNTER_DRAFT),
    ('counter-draft-missing-clauses',
     "for t in law_shape_ok census_rederived_ok depth_gap_recorded re_scored_pins; do "
     "printf '%s=%s\\n' \"$t\" \"$(grep -c -- \"$t\" " + COUNTER_DRAFT + ")\"; done"),
    ('counter-draft-missing-flags',
     "for t in --gap-rule --receipts --provenance-base --receipt-fresh-base; do "
     "printf '%s=%s\\n' \"$t\" \"$(grep -c -- \"$t\" " + COUNTER_DRAFT + ")\"; done"),
    ('s252-l1-open-receipt',
     "cat .ufo/waves/round-52/l1/s252-l1-open.txt && sha256sum "
     ".ufo/waves/round-52/l1/mknod.2.html"),
    ('mknod-epperm-quote',
     "python3 -c \"import re;h=open('.ufo/waves/round-52/l1/mknod.2.html',"
     "encoding='utf-8',errors='replace').read();t=re.sub(r'<[^>]+>',' ',h);"
     "i=t.find('EPERM');print(' '.join(t[i:i+320].split()))\""),
    ('r51-no-landing',
     "ls tools/round-51/ && ls corpus/evidence/ | grep round-5 ; "
     "git log --oneline -1 --format='%H %s' HEAD"),
    ('counter-draft-undefined-names',
     "python3 -c \"import ast,builtins;src=open('.ufo/waves/round-52/w1/ExecCounterV2/"
     "c1-counter.py').read();t=ast.parse(src);load={n.id for n in ast.walk(t) "
     "if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)};"
     "st={n.id for n in ast.walk(t) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Store)}"
     "|{n.name for n in ast.walk(t) if isinstance(n,(ast.FunctionDef,ast.ClassDef))};"
     "g=[x for x in ('TARGET','IDS','PROV_BASE','RECEIPT_FRESH_BASE') if x in load and "
     "x not in st];print('module-level constants referenced but never assigned:',g)\""),
    ('carrier-pins-in-prior-set',
     "python3 -c \"import json,re;SHA=re.compile(r'^[0-9a-f]{64}$');pins=set();"
     "tbl=('.ufo/waves/round-41/c1/carriers.json','tools/round-49/carriers.json',"
     "'tools/round-50/carriers.json');"
     "[(pins.add(c['sha256'].lower()),None) for p in tbl for c in "
     "(json.load(open(p)).get('carriers') or []) if isinstance(c.get('sha256'),str) and "
     "SHA.match(c['sha256'].lower())];"
     "print('\\n'.join('%s %s' % (c['id'], 'IN_PRIOR' if c['sha256'].lower() in pins else "
     "'fresh') for c in json.load(open('tools/round-50/carriers.json'))['carriers']))\""),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    lines = ['id\tutc\texit\tstdout_sha256\tcommand']
    for rid, cmd in COMMANDS:
        p = subprocess.run(['bash', '-c', cmd], cwd=args.lane,
                           capture_output=True, text=True,
                           env=dict(os.environ, LC_ALL='C'))
        out = p.stdout.encode()
        utc = datetime.datetime.now(datetime.timezone.utc).strftime(
            '%Y-%m-%dT%H:%M:%SZ')
        digest = hashlib.sha256(out).hexdigest()
        lines.append('%s\t%s\t%d\t%s\t%s' % (rid, utc, p.returncode, digest,
                                              cmd.replace('\t', ' ')))
    body = '\n'.join(lines) + '\n'
    with open(args.out, 'w', encoding='utf-8') as fh:
        fh.write(body)
    sys.stdout.write(body)
    return 0


if __name__ == '__main__':
    sys.exit(main())
