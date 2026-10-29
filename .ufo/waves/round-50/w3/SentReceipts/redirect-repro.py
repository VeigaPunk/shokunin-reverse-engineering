#!/usr/bin/env python3
"""Offline redirect exploit repro: two loopback origins, no internet.

Server A (127.0.0.1:PORT_A) answers 302 -> http://127.0.0.1:PORT_B/evil
Server B (127.0.0.1:PORT_B) answers 200 with the payload.

We then call each fetcher's fetch() with A's URL and observe whether the
redirect is followed and the payload is accepted.
"""
import http.server, importlib.util, io, json, os, socket, sys, tarfile, threading, hashlib, urllib.parse

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PAYLOAD = b'PAYLOAD-FROM-SECOND-ORIGIN\n'


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


PA, PB = free_port(), free_port()
member = b'SECOND-ORIGIN-MEMBER\n' * 4
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w') as tf:
    ti = tarfile.TarInfo('./fw.image'); ti.size = len(member)
    tf.addfile(ti, io.BytesIO(member))
tar_b = buf.getvalue()


class A(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/image':
            self.send_response(302)
            self.send_header('Location', 'http://127.0.0.1:%d/evil' % PB)
            self.end_headers()
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, *a): pass


class B(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Length', str(len(tar_b)))
        self.end_headers()
        self.wfile.write(tar_b)
    def log_message(self, *a): pass


sa = http.server.HTTPServer(('127.0.0.1', PA), A)
sb = http.server.HTTPServer(('127.0.0.1', PB), B)
threading.Thread(target=sa.serve_forever, daemon=True).start()
threading.Thread(target=sb.serve_forever, daemon=True).start()

res = {}
for name, path in (('round-50', 'tools/round-50/fetch-vendor.py'),
                   ('round-41', 'tools/round-41/fetch-vendor.py')):
    spec = importlib.util.spec_from_file_location('fv_' + name, os.path.join(LANE, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    url = 'http://127.0.0.1:%d/image' % PA
    try:
        b, how = m.fetch(url, None, hashlib.sha256(tar_b).hexdigest())
        res[name] = {'outcome': 'ACCEPTED', 'how': how, 'bytes': len(b),
                     'sha256': hashlib.sha256(b).hexdigest(),
                     'note': 'redirect to a second origin was followed'}
    except Exception as e:
        res[name] = {'outcome': 'REFUSED', 'exc': type(e).__name__, 'msg': str(e)[:160]}

print(json.dumps(res, indent=1, sort_keys=True))
