import json,sys,subprocess,os
cmd=sys.argv[1]; args=sys.argv[2:]
p=subprocess.run(["npx","-y","rea-agents@6.5.0",cmd,*args,"--format","json"],capture_output=True,text=True,timeout=170)
o=p.stdout
try: d=json.loads(o)
except Exception: print(f"{cmd}\texit={p.returncode}\tNONJSON\t{(o or p.stderr)[:160]!r}"); sys.exit()
if isinstance(d,dict) and "operation" in d:
    print(f"{cmd}\texit={p.returncode}\tOK\top={d['operation']}\tprov={d['provider']['id']}")
else:
    det=d.get("details") or {}
    print(f"{cmd}\texit={p.returncode}\tERR\tcode={d.get('code')}\tmsg={str(d.get('message'))[:100]!r}\treason={str(det.get('reason') or det.get('issues') or '')[:140]!r}")
