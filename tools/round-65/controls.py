#!/usr/bin/env python3
"""Generate transparent deliberately faulty owned reader wrappers."""
import pathlib,sys,json

def main(reader,out,dev):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False)
    common='import subprocess,sys,json,pathlib,hashlib\nR='+repr(str(pathlib.Path(reader).resolve()))+'\nr=subprocess.run([sys.executable,"-I","-B",R]+sys.argv[1:],capture_output=True,text=True)\nd=json.loads(r.stdout)\n'
    modes={
      'noop':'raise SystemExit(0)\n',
      'boolean':common+'d["schema"]=True\nprint(json.dumps(d));raise SystemExit(r.returncode)\n',
      'duplicate_key':common+'s=json.dumps(d);print(s[:-1]+", \\\"schema\\\": 1}");raise SystemExit(r.returncode)\n',
      'collapse_names':common+'if d["exit"]==0: d["occurrences"]=list({x["name"]:x for x in d["occurrences"]}.values())\nprint(json.dumps(d));raise SystemExit(r.returncode)\n',
      'bsd_includes_name':common+'if d["exit"]==0:\n for x in d["occurrences"]:\n  if x["stored_size"]!=x["payload_size"]:\n   x["payload_size"]=x["stored_size"]; b=pathlib.Path(sys.argv[-1]).read_bytes(); x["payload_sha256"]=hashlib.sha256(b[x["header_offset"]+60:x["header_offset"]+60+x["stored_size"]]).hexdigest()\nprint(json.dumps(d));raise SystemExit(r.returncode)\n',
      'metadata_as_member':common+'if d["exit"]==0:\n for x in d["occurrences"]: x["kind"]="member"\nprint(json.dumps(d));raise SystemExit(r.returncode)\n',
      'ignore_offset':common+'if d["exit"]==0:\n for x in d["occurrences"]:\n  if x["name"].endswith("second-long-object.o"): x["name"]=x["name"].replace("second-long-object.o","first-long-object.o")\nprint(json.dumps(d));raise SystemExit(r.returncode)\n',
      'stale_dev': 'import json,sys,pathlib\nx=json.loads(pathlib.Path('+repr(str(pathlib.Path(dev).resolve()))+').read_text())[pathlib.Path(sys.argv[-1]).stem]\nprint(json.dumps(x["output"]));raise SystemExit(x["exit"])\n'}
    for n,s in modes.items(): (out/(n+'.py')).write_text(s)
if __name__=='__main__':main(*sys.argv[1:])
