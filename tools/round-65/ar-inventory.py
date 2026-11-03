#!/usr/bin/env python3
"""Bounded inert ar inventory. No extraction, linking or external-reference reads."""
import argparse, hashlib, json, os, re, stat, sys, tempfile, subprocess
LIMIT=1048576
class Refusal(Exception):
    def __init__(self, code, reason): self.code,self.reason=code,reason

def fail(code, reason): raise Refusal(code,reason)
def printable(b):
    if not b or any(c<32 or c>126 for c in b): fail(2,'unsupported_name')
    return b.decode('ascii')
def parse(b):
    if len(b)>LIMIT: fail(2,'archive_budget')
    if b[:8]==b'!<thin>\n': fail(2,'thin_archive')
    if b[:8]!=b'!<arch>\n': fail(1,'bad_magic')
    pos=8; out=[]; table=None
    while pos<len(b):
        if len(out)>=128: fail(2,'count_budget')
        if len(b)-pos<60: fail(1,'truncated_header')
        h=b[pos:pos+60]
        if h[58:60]!=b'`\n': fail(1,'bad_terminator')
        if not re.fullmatch(rb'[0-9]+ *',h[48:58]): fail(1,'bad_size')
        n=int(h[48:58])
        if n>65536: fail(2,'member_budget')
        start=pos+60; end=start+n
        if end>len(b): fail(1,'truncated_payload')
        if n%2 and (end>=len(b) or b[end]!=10): fail(1,'bad_padding')
        raw=h[:16].rstrip(b' '); data=b[start:end]; payload=data; kind='member'
        if raw==b'//':
            if table is not None: fail(1,'bad_name_table')
            table={}; off=0
            while off<len(data):
                stop=data.find(b'/\n',off)
                if stop<0: fail(1,'bad_name_table')
                try: name=printable(data[off:stop])
                except Refusal: fail(1,'bad_name_table')
                table[off]=name; off=stop+2
            name='//';kind='name_table'
        elif raw==b'/': name='/';kind='symbol_table'
        elif raw.startswith(b'#1/'):
            if not re.fullmatch(rb'[0-9]+',raw[3:]): fail(1,'bad_bsd_length')
            k=int(raw[3:])
            if not 0<k<=n: fail(1,'bad_bsd_length')
            name=printable(data[:k]);payload=data[k:]
        elif raw.startswith(b'/'):
            if not re.fullmatch(rb'[0-9]+',raw[1:]): fail(2,'unsupported_variant')
            k=int(raw[1:])
            if table is None or k not in table: fail(1,'bad_name_reference')
            name=table[k]
        else: name=printable(raw[:-1] if raw.endswith(b'/') else raw)
        out.append(dict(ordinal=len(out),header_offset=pos,kind=kind,name=name,stored_size=n,payload_size=len(payload),payload_sha256=hashlib.sha256(payload).hexdigest()))
        pos=end+n%2
    return dict(schema=1,exit=0,finding='complete',archive_sha256=hashlib.sha256(b).hexdigest(),archive_size=len(b),occurrences=out)
def read(path):
    try:
        if not stat.S_ISREG(os.lstat(path).st_mode): fail(2,'input_refused')
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        with os.fdopen(fd,'rb') as f:
            if not stat.S_ISREG(os.fstat(f.fileno()).st_mode): fail(2,'input_refused')
            if os.fstat(f.fileno()).st_size>LIMIT: fail(2,'archive_budget')
            b=f.read(LIMIT+1)
        return parse(b)
    except OSError: fail(2,'input_refused')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive');ap.add_argument('--selftest',action='store_true');a=ap.parse_args()
    if a.selftest:
        rows=[]
        with tempfile.TemporaryDirectory() as d:
            for name,b,code,finding in [('empty',b'!<arch>\n',0,'complete'),('bad',b'bad',1,'bad_magic'),('thin',b'!<thin>\n',2,'thin_archive')]:
                p=os.path.join(d,name);open(p,'wb').write(b)
                r=subprocess.run([sys.executable,'-I','-B',__file__,'--archive',p],capture_output=True,text=True)
                body=json.loads(r.stdout); rows.append(dict(case=name,exit=r.returncode,finding=body['finding'],ok=r.returncode==code and body['finding']==finding))
        print(json.dumps(dict(cases=rows,passed=all(x['ok'] for x in rows))))
        return 0 if all(x['ok'] for x in rows) else 1
    if not a.archive: ap.error('--archive required')
    try: result=read(a.archive)
    except Refusal as e: result=dict(schema=1,exit=e.code,finding=e.reason)
    print(json.dumps(result,sort_keys=True));return result['exit']
if __name__=='__main__':sys.exit(main())
