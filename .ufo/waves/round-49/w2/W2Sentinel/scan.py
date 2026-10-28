import subprocess, re, gzip, os, sys, json, hashlib, collections
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S=os.environ['TMPDIR']
rows=[l.split('\t') for l in open(S+'/rows.tsv').read().splitlines()]
rows=[r for r in rows if r[0]!='160000']
env=dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
shas=[r[2] for r in rows]; paths=[r[3] for r in rows]
p=subprocess.Popen(['git','-C',L,'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,env=env)
PAT=collections.OrderedDict([
 ('private-key-block', re.compile(rb'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY')),
 ('aws-access-key', re.compile(rb'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b')),
 ('github-token', re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})')),
 ('npm-token', re.compile(rb'\bnpm_[A-Za-z0-9]{30,}\b')),
 ('npmrc-authtoken', re.compile(rb'_authToken\s*=')),
 ('anthropic-or-openai-key', re.compile(rb'\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{20,}')),
 ('slack-token', re.compile(rb'\bxox[abposr]-[A-Za-z0-9-]{10,}')),
 ('google-api-key', re.compile(rb'\bAIza[0-9A-Za-z_\-]{30,}')),
 ('jwt', re.compile(rb'\beyJ[A-Za-z0-9_\-]{8,}\.eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}')),
 ('1password-ref', re.compile(rb'op://')),
 ('authorization-header', re.compile(rb'(?i)\bAuthorization\s*:\s*(?:Bearer|Basic|token)\b')),
 ('bearer-literal', re.compile(rb'(?i)\bBearer\s+[A-Za-z0-9._\-]{16,}')),
 ('cookie-header', re.compile(rb'(?i)\b(?:Set-)?Cookie\s*:\s*\S')),
 ('session-id-assign', re.compile(rb'(?i)\b(?:sessionid|session_id|sess_id|JSESSIONID|PHPSESSID|connect\.sid|session-token|__Secure-[A-Za-z_]+)\s*[=:]\s*[\'"]?[A-Za-z0-9%._\-]{12,}')),
 ('generic-secret-assign', re.compile(rb'(?i)\b(?:api[_-]?key|apikey|secret|client_secret|access_token|auth_token|refresh_token|private_token|password|passwd|pwd)\s*[=:]\s*[\'"]?([A-Za-z0-9/+_\-=.]{12,})')),
 ('env-token-var', re.compile(rb'\b(?:GITHUB_TOKEN|NPM_TOKEN|ANTHROPIC_API_KEY|OPENAI_API_KEY|AWS_[A-Z_]*|GH_TOKEN|SSH_AUTH_SOCK|SSH_AGENT_PID|DBUS_SESSION_BUS_ADDRESS|XDG_SESSION_ID|GPG_AGENT_INFO|SSH_CONNECTION|SSH_CLIENT|SSH_TTY|KEYRING\w*|HF_TOKEN|GOOGLE_\w*KEY)\b')),
 ('ipv4-private', re.compile(rb'\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b')),
 ('email', re.compile(rb'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')),
 ('operator-home-path', re.compile(rb'/home/[a-z][a-z0-9_\-]+')),
 ('mac-address', re.compile(rb'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b')),
 ('hex-40-64-long', re.compile(rb'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])')),
])
out=open(S+'/scan-hits.tsv','w')
counts=collections.Counter(); files_hit=collections.defaultdict(set); binary=[]; unreadable=[]
def read_blob(sha):
    p.stdin.write((sha+'\n').encode()); p.stdin.flush()
    hdr=p.stdout.readline().decode().split()
    if hdr[1]=='missing': return None
    size=int(hdr[2]); data=p.stdout.read(size); p.stdout.read(1); return data
for sha,path in zip(shas,paths):
    data=read_blob(sha)
    if data is None: unreadable.append(path); continue
    srcs=[('raw',data)]
    if path.endswith('.gz'):
        try: srcs=[('gunzip',gzip.decompress(data))]
        except Exception as e: unreadable.append(path+' gunzip-fail '+str(e))
    for tag,d in srcs:
        if b'\0' in d[:8000]: binary.append(path+' ['+tag+']')
        for name,rx in PAT.items():
            for m in rx.finditer(d):
                ln=d.count(b'\n',0,m.start())+1
                tok=m.group(0)
                red=(tok[:6]+b'...'+tok[-4:]).decode('latin1') if len(tok)>14 else tok.decode('latin1')[:20]
                line=d[d.rfind(b'\n',0,m.start())+1:d.find(b'\n',m.end()) if d.find(b'\n',m.end())!=-1 else len(d)]
                out.write(f"{path}\t{tag}:{ln}\t{name}\t{red}\n")
                counts[name]+=1; files_hit[name].add(path)
out.close(); p.stdin.close(); p.wait()
json.dump({'counts':counts,'files':{k:sorted(v) for k,v in files_hit.items()},'binary':binary,'unreadable':unreadable,'n_blobs':len(paths)},open(S+'/scan-summary.json','w'),default=list,indent=1)
print('blobs',len(paths),'binary-or-nul',len(binary),'unreadable',len(unreadable))
for k,v in counts.items(): print(f'{v:6d} {k:26s} files={len(files_hit[k])}')
