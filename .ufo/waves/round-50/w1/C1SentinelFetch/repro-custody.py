#!/usr/bin/env python3
"""C1SentinelFetch custody repros (round 50, wave 1). Scratch-only; never writes the lane.

Run:  python3 -I -B repro-custody.py <SCRATCH>   (SCRATCH under /fast/scratch/hyaku/kaidoku-r50/)
Needs: a lane clone at <SCRATCH>/clone checked out at 7c678ae6d97aedb969fd253b52b3d2882ef1e186
       (git clone --shared <lane> <SCRATCH>/clone; git -C <SCRATCH>/clone checkout --detach <base>).
Prints one line per check: CHECK <id> <verdict> <detail>. Values of cookies are never printed.
"""
import hashlib, importlib.util, json, os, shutil, ssl, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer

S = os.path.abspath(sys.argv[1])
CL = os.path.join(S, 'clone')
LANE_RUN_PY = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-49/c1-run.py'
FV = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/fetch-vendor.py'
SQ = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/sqfs-list.py'
ENV = {'PATH': '/usr/bin:/bin', 'HOME': os.environ['HOME'], 'TMPDIR': S}
assert subprocess.run(['git', '-C', CL, 'rev-parse', '--show-toplevel'], capture_output=True,
                      text=True).stdout.strip() == CL, 'clone toplevel mismatch'
os.makedirs(os.path.join(S, 'fx'), exist_ok=True)
os.makedirs(os.path.join(S, 'scr'), exist_ok=True)

def check(cid, verdict, detail):
    print('CHECK %s %s %s' % (cid, verdict, detail), flush=True)

# --- fixtures: a stand-in carrier (no vendor bytes) and a pinned carriers.json
payload = b'hsqs-stand-in' * 200
fx = os.path.join(S, 'fx', 'stand-in.image')
open(fx, 'wb').write(payload)
carriers = os.path.join(S, 'carriers.json')
json.dump({'carriers': [{'id': 'avmx', 'sha256': hashlib.sha256(payload).hexdigest(), 'fixture': fx}]},
          open(carriers, 'w'))

# --- fake REA: publishes a rootfs-like tree plus a symlink pair (stand-ins)
fake = os.path.join(S, 'fakerea.py')
open(fake, 'w').write('''#!/usr/bin/env python3
import os, sys, json
out = sys.argv[-1]
os.makedirs(os.path.join(out, "firmware.bin_extract/bin"), exist_ok=True)
open(os.path.join(out, "firmware.bin_extract/bin/busybox"), "wb").write(b"STAND-IN-BYTES")
os.makedirs(os.path.join(out, "firmware.bin_extract/lib"), exist_ok=True)
os.symlink("/home/operator/.ssh", os.path.join(out, "firmware.bin_extract/lib/host-link"))
print(json.dumps({"ok": True, "data": {"evidence_id": "fake", "parameters": {"output_directory": out}}}))
''')
os.chmod(fake, 0o755)

# C1 copy-into-evidence + gitignore gap
ev = os.path.join(CL, 'corpus', 'evidence', 'round-49', 'c1', 'repro-copy')
shutil.rmtree(ev, ignore_errors=True)
p = subprocess.run(['python3', '-I', '-B', LANE_RUN_PY, '--lane-root', CL, '--carriers', carriers,
                    '--evidence-root', ev, '--scratch', os.path.join(S, 'scr'), '--fake-rea', fake,
                    '--freeze', 'repro', '--no-unblob-log-tee'], capture_output=True, text=True, env=ENV, cwd=S)
bb = os.path.join(ev, 'avmx', 'firmware.bin_extract', 'bin', 'busybox')
lk = os.path.join(ev, 'avmx', 'firmware.bin_extract', 'lib', 'host-link')
check('C1-COPY', 'VIOLATION' if os.path.isfile(bb) else 'clean',
      'runner exit %d; REA-published file copied into evidence: %s; symlink copied: %s'
      % (p.returncode, os.path.isfile(bb), os.path.islink(lk)))
ad = subprocess.run(['git', '-C', CL, 'add', '--dry-run', '-A', 'corpus/evidence/round-49/c1/repro-copy'],
                    capture_output=True, text=True)
staged = [l for l in ad.stdout.splitlines() if 'firmware.bin_extract' in l]
check('C1-GITIGNORE', 'VIOLATION' if staged else 'clean',
      'git add --dry-run exit %d; firmware paths that would be staged: %d' % (ad.returncode, len(staged)))
ci = subprocess.run(['git', '-C', CL, 'check-ignore', '--no-index', 'x.image', 'filesystem.image', 'y.bin',
                     'z.part', 'corpus/evidence/round-50/c1/a/firmware.bin_extract/bin/busybox'],
                    capture_output=True, text=True)
check('C1-GITIGNORE-PROBE', 'VIOLATION' if ci.returncode == 1 else 'check',
      'git check-ignore exit %d (1 = none of the probe paths is ignored)' % ci.returncode)

# --- fetch-vendor: redirect to a non-AVM host is followed; file:// accepted
class Target(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Length', str(len(payload))); self.end_headers()
        self.wfile.write(payload)
    def log_message(self, *a): pass
class Redir(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302); self.send_header('Location', 'http://127.0.0.1:%d/x.image' % TP)
        self.send_header('Content-Length', '0'); self.end_headers()
    def log_message(self, *a): pass
ts = HTTPServer(('127.0.0.1', 0), Target); TP = ts.server_address[1]
rs = HTTPServer(('127.0.0.1', 0), Redir)
for srv in (ts, rs):
    threading.Thread(target=srv.serve_forever, daemon=True).start()
spec = importlib.util.spec_from_file_location('fv', FV)
fv = importlib.util.module_from_spec(spec); spec.loader.exec_module(fv)
b, how = fv.fetch('http://127.0.0.1:%d/start.image' % rs.server_address[1], None,
                  hashlib.sha256(payload).hexdigest())
check('C1-REDIRECT', 'VIOLATION' if b == payload else 'clean',
      'redirect followed to a different host (no AVM allowlist): %s; bytes %d' % (how, len(b)))
b2, how2 = fv.fetch('file://' + fx, None, hashlib.sha256(payload).hexdigest())
check('C1-FILE-SCHEME', 'VIOLATION' if b2 == payload else 'clean', 'file:// accepted by fetch: %s' % how2)
ts.shutdown(); rs.shutdown()

# --- TLS verification: a self-signed https origin must be rejected
cert = os.path.join(S, 'tls'); os.makedirs(cert, exist_ok=True)
subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', cert + '/k.pem',
                '-out', cert + '/c.pem', '-days', '1', '-subj', '/CN=127.0.0.1'], capture_output=True, check=True)
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.send_header('Content-Length', '3'); self.end_headers(); self.wfile.write(b'abc')
    def log_message(self, *a): pass
hs = HTTPServer(('127.0.0.1', 0), H)
c = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); c.load_cert_chain(cert + '/c.pem', cert + '/k.pem')
hs.socket = c.wrap_socket(hs.socket, server_side=True)
threading.Thread(target=hs.serve_forever, daemon=True).start()
try:
    fv.fetch('https://127.0.0.1:%d/x.image' % hs.server_address[1], None, hashlib.sha256(b'abc').hexdigest())
    check('C1-TLS', 'VIOLATION', 'self-signed origin accepted')
except Exception as e:
    check('C1-TLS', 'clean', 'self-signed origin rejected: %s' % type(e).__name__)
hs.shutdown()

# --- timeout does not reap the grandchild (runner returns while the child keeps running)
orph = os.path.join(S, 'fakerea_orphan.py')
open(orph, 'w').write('#!/usr/bin/env python3\nimport subprocess,time\nsubprocess.Popen(["sleep","25"])\ntime.sleep(60)\n')
os.chmod(orph, 0o755)
ev2 = os.path.join(CL, 'corpus', 'evidence', 'round-49', 'c1', 'repro-orphan')
shutil.rmtree(ev2, ignore_errors=True)
t0 = time.time()
p = subprocess.run(['python3', '-I', '-B', LANE_RUN_PY, '--lane-root', CL, '--carriers', carriers,
                    '--evidence-root', ev2, '--scratch', os.path.join(S, 'scr'), '--fake-rea', orph,
                    '--timeout', '2', '--freeze', 'repro', '--no-unblob-log-tee'],
                   capture_output=True, text=True, env=ENV, cwd=S)
alive = subprocess.run(['pgrep', '-f', 'sleep 25'], capture_output=True, text=True).stdout.strip()
check('C1-TIMEOUT', 'VIOLATION' if alive else 'clean',
      'runner wall %.1fs (timeout 2s), exit %d, grandchild alive after return: %s'
      % (time.time() - t0, p.returncode, bool(alive)))
subprocess.run(['pkill', '-f', 'sleep 25'])

# --- hygiene: fetch-vendor selftest (must stay green on the copy)
st = subprocess.run(['python3', '-I', '-B', FV, '--selftest'], capture_output=True, text=True, env=ENV, cwd=S)
check('FV-SELFTEST', 'clean' if st.returncode == 0 else 'FAIL', 'exit %d, last line: %s'
      % (st.returncode, st.stdout.strip().splitlines()[-1] if st.stdout.strip() else ''))

for path in (FV, SQ, LANE_RUN_PY, '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c1-run.sh',
             '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.gitignore'):
    check('SRC-SHA256', 'info', '%s %s' % (hashlib.sha256(open(path, 'rb').read()).hexdigest(), path))
