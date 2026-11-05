import json,os,subprocess,sys
S="/fast/scratch/hyaku/kaidoku-r90/SentinelScope"
W=os.path.join(S,"bwrap","procwork"); hide=os.path.join(W,"runroot")
decoy=os.path.join(W,"decoy")
paths=[os.path.realpath(p) for p in ("/usr/bin/jq","/usr/bin/xxd","/usr/lib/libz.so.1.3.2","/usr/bin/docker-init")]
lane="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
payload=(
 "import json,os,sys\n"
 "lane=sys.argv[1]\n"
 "probe={'lane_writable':os.access(lane,os.W_OK),\n"
 " 'lane_receipts_writable':os.access(os.path.join(lane,'.ufo/waves/round-90'),os.W_OK),\n"
 " 'home':os.environ.get('HOME'),\n"
 " 'home_writable':os.access(os.environ.get('HOME') or '/',os.W_OK),\n"
 " 'root_bind_rw':[l.split()[0:6] for l in open('/proc/self/mountinfo') if l.split()[4]=='/'][:2],\n"
 " 'jq_size':os.path.getsize('/usr/bin/jq') if os.path.exists('/usr/bin/jq') else None,\n"
 " 'jq_is_decoy':open('/usr/bin/jq','rb').read(21)==b'decoy-not-a-carrier\\n'}\n"
 "print(json.dumps(probe))\n")
argv=["bwrap","--dev-bind","/","/","--tmpfs",hide]
for p in paths: argv+=["--bind",decoy,p]
argv+=["--",sys.executable,"-c",payload,lane]
pr=subprocess.run(argv,capture_output=True,text=True,timeout=120)
print("rc",pr.returncode); print(pr.stdout.strip()); print((pr.stderr or "")[-300:])
json.dump({"rc":pr.returncode,"stdout":pr.stdout.strip()},open(os.path.join(S,"rwprobe.json"),"w"),indent=1)
