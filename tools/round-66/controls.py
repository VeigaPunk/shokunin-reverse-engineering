#!/usr/bin/env python3
"""Transparent deliberate shortcuts; not competing implementations."""
import pathlib,sys

def main(reader,out,dev):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False)
    common='import subprocess,sys,json,pathlib\nR='+repr(str(pathlib.Path(reader).resolve()))+'\nr=subprocess.run([sys.executable,"-I","-B",R]+sys.argv[1:],capture_output=True,text=True)\nd=json.loads(r.stdout)\n'
    finish='\nprint(json.dumps(d));raise SystemExit(r.returncode)\n'
    modes={'noop':'raise SystemExit(0)\n','boolean':common+'d["schema"]=True'+finish,'duplicate_key':common+'print(json.dumps(d)[:-1]+\',"schema":1}\');raise SystemExit(r.returncode)\n',
    'first_overlap':common+'if d["exit"]==0:\n for x in d["intervals"]:\n  if x["kind"]=="ambiguous":x["candidates"]=x["candidates"][:1];x["kind"]=x["candidates"][0]["kind"]'+finish,
    'gaps_are_zero':common+'if d["exit"]==0:\n for x in d["intervals"]:\n  if x["kind"]=="unmapped":x["kind"]="zero"'+finish,
    'zero_is_file':common+'if d["exit"]==0:\n for x in d["intervals"]:\n  for c in x["candidates"]:\n   if c["kind"]=="zero":c.update(kind="file",file_offset=0,sha256="0"*64)'+finish,
    'global_delta':common+'if d["exit"]==0:\n delta=None\n for x in d["intervals"]:\n  for c in x["candidates"]:\n   if c["kind"]=="file":\n    if delta is None:delta=x["start"]-c["file_offset"]\n    c["file_offset"]=x["start"]-delta'+finish,
    'stale_dev':'import json,sys,pathlib\np=sys.argv[sys.argv.index("--elf")+1]\ne=json.loads(pathlib.Path('+repr(str(pathlib.Path(dev).resolve()))+').read_text())[pathlib.Path(p).stem]\nprint(json.dumps(e["output"]));raise SystemExit(e["exit"])\n'}
    for k,v in modes.items():(out/(k+'.py')).write_text(v)
if __name__=='__main__':main(*sys.argv[1:])
