#!/usr/bin/env python3
"""Transparent faulty-reader controls on construction fixtures, not independent parsers.
--reader PATH --fixtures DIR --output PATH; 0 all controls reject,1 survivor,2 setup.
Writes only requested receipt and private temporary own scripts. Never executes subjects.
"""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile
H=lambda b:hashlib.sha256(b).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--reader',required=True);p.add_argument('--fixtures',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    src=pathlib.Path(a.reader).read_text();compare=pathlib.Path(__file__).with_name('compare.py');fixtures=pathlib.Path(a.fixtures);oracle=fixtures/'expected.json';rows=[]
    changes={
      'wrong-rva-unit':("cursor=pointer;end=pointer+length;records=[]","pointer += 1024\n    cursor=pointer;end=pointer+length;records=[]"),
      'always-pe32plus':("fixed,fmt=(96,'pe32') if magic==0x10b else (112,'pe32plus')","fixed,fmt=(112,'pe32plus')"),
      'ignore-directory-count':('if count<5:return absent','if False:return absent'),
      'ignore-optional-bounds':('need(fixed+count*8<=size)','need(True)'),
      'unrounded-stride':('stride=(n+7)//8*8','stride=n'),
      'padding-in-content':('sha(b[cursor+8:cursor+n])','sha(b[cursor+8:cursor+stride])'),
      'ignore-record-cap':('need(len(records)<64 and cursor+8<=end)','need(cursor+8<=end)'),
      'sort-records':("need(cursor==end)","need(cursor==end)\n    records.sort(key=lambda x:x['type'])"),
      'deduplicate-content':("need(cursor==end)","need(cursor==end)\n    records=list({(x['length'],x['revision'],x['type'],x['declared_content_sha256'],x['alignment_padding_sha256']):x for x in records}.values())"),
    }
    programs={}
    for name,(old,new) in changes.items():
      if src.count(old)!=1:raise ValueError('mutation anchor not unique: '+name)
      programs[name]=src.replace(old,new)
    programs['no-output']='pass\n'
    programs['boolean-status']="import json\nprint(json.dumps({'status':True}))\n"
    programs['duplicate-json-key']="print('{\"status\":\"refused\",\"status\":\"refused\"}')\nraise SystemExit(1)\n"
    with tempfile.TemporaryDirectory(prefix='kaidoku68-controls-') as t:
      for name,code in programs.items():
        reader=pathlib.Path(t)/(name+'.py');reader.write_text(code)
        cmd=[sys.executable,'-I','-B',str(compare),'--reader',str(reader),'--fixtures',str(fixtures),'--reader-sha256',H(reader.read_bytes()),'--oracle-sha256',H(oracle.read_bytes())]
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);b=json.loads(r.stdout)
        rows.append({'name':name,'reader_sha256':H(reader.read_bytes()),'exit':r.returncode,'matched':b['matched'],'cases':b['cases'],'rejected':r.returncode==1 and b['matched']<b['cases'],'comparison':b})
    out={'reader_sha256':H(pathlib.Path(a.reader).read_bytes()),'oracle_sha256':H(oracle.read_bytes()),'controls':rows,'all_rejected':all(x['rejected'] for x in rows)}
    pathlib.Path(a.output).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'controls':len(rows),'all_rejected':out['all_rejected'],'outcomes':[{k:x[k] for k in ['name','matched','cases','rejected']} for x in rows]}));return 0 if out['all_rejected'] else 1
if __name__=='__main__':raise SystemExit(main())
