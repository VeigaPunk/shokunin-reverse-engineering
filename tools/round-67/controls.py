#!/usr/bin/env python3
"""Reviewer-owned transparent output mutations, not alternative parsers."""
import pathlib,sys

def main(reader,out,dev):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False)
 common='import subprocess,sys,json,pathlib\nR='+repr(str(pathlib.Path(reader).resolve()))+'\nr=subprocess.run([sys.executable,"-I","-B",R]+sys.argv[1:],capture_output=True,text=True)\nd=json.loads(r.stdout)\n'
 finish='\nprint(json.dumps(d));raise SystemExit(d["exit"])\n'
 modes={'noop':'raise SystemExit(0)\n','boolean':common+'d["schema"]=True'+finish,'duplicate_key':common+'print(json.dumps(d)[:-1]+\',"schema":1}\');raise SystemExit(r.returncode)\n',
 'deduplicate':common+'if d["exit"]==0:\n seen=set();d["needed"]=[x for x in d["needed"] if not (x["name_hex"] in seen or seen.add(x["name_hex"]))]'+finish,
 'sort_names':common+'if d["exit"]==0:d["needed"].sort(key=lambda x:x["name_hex"])'+finish,
 'omit_terminator_origin':common+'if d["exit"]==0:\n for x in d["needed"]:\n  x["origins"][-1]["length"]-=1\n  x["origins"]=[o for o in x["origins"] if o["length"]]'+finish,
 'single_delta':common+'if d["exit"]==0:\n for x in d["needed"]:\n  if len(x["origins"])>1:x["origins"]=[dict(x["origins"][0],length=sum(o["length"] for o in x["origins"]))]'+finish,
 'decode_utf8':common+'if d["exit"]==0:\n for x in d["needed"]:x["name_hex"]=bytes.fromhex(x["name_hex"]).decode("utf8","replace").encode().hex()'+finish,
 'ignore_ambiguity':common+'if d["finding"] in ("strtab_ambiguous","dynamic_ambiguous"):d={"schema":1,"exit":0,"finding":"complete"}'+finish,
 'stale_dev':'import json,sys,pathlib\np=sys.argv[sys.argv.index("--elf")+1]\ne=json.loads(pathlib.Path('+repr(str(pathlib.Path(dev).resolve()))+').read_text())[pathlib.Path(p).stem]\nprint(json.dumps(e["output"]));raise SystemExit(e["exit"])\n'}
 for k,v in modes.items():(out/(k+'.py')).write_text(v)
if __name__=='__main__':main(*sys.argv[1:])
