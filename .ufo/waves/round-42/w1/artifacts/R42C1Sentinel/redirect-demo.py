#!/usr/bin/env python3
"""Reproduce the redirect-following measurement for tools/round-41/fetch-vendor.py.

Loads the lane fetcher unchanged, serves a fixed body from two loopback HTTP
servers, and shows that a pinned URL may redirect to another host while
`fetch()` still returns the bytes and records only the final hop's status.

No network access, no writes outside tempfile.mkdtemp(). Usage:
    python3 -I -B redirect-demo.py [--lane PATH]
"""
import argparse
import hashlib
import http.server
import importlib.util
import os
import socketserver
import tempfile
import threading


def serve(handler):
    srv = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', default='/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
    a = ap.parse_args()
    body = b'HSQS-FAKE-CARRIER-BODY' * 100
    pin = hashlib.sha256(body).hexdigest()
    seen = []

    class Redirect(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            seen.append((self.server.server_address[1], self.path))
            if self.path == '/start':
                self.send_response(302)
                self.send_header('Location', '/final')
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        def log_message(self, *args):
            pass

    class Cross(Redirect):
        def do_GET(self):
            seen.append((self.server.server_address[1], self.path,
                         self.headers.get('Host')))
            self.send_response(302)
            self.send_header('Location', 'http://localhost:%d/final' % other.server_address[1])
            self.end_headers()

    spec = importlib.util.spec_from_file_location(
        'fetch_vendor', os.path.join(a.lane, 'tools/round-41/fetch-vendor.py'))
    fetcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fetcher)

    first, other = serve(Redirect), serve(Redirect)
    cache = tempfile.mkdtemp(prefix='redirect-demo.')
    data, how = fetcher.fetch('http://127.0.0.1:%d/start' % first.server_address[1], cache, pin)
    print('same-host redirect  bytes_ok=%s how=%s requests=%s'
          % (hashlib.sha256(data).hexdigest() == pin, how, seen))
    seen.clear()
    cross = serve(Cross)
    data, how = fetcher.fetch('http://127.0.0.1:%d/start' % cross.server_address[1], None, pin)
    print('cross-host redirect bytes_ok=%s how=%s hosts=%s'
          % (hashlib.sha256(data).hexdigest() == pin, how, seen))
    print('cache files:', sorted(os.listdir(cache)))
    for s in (first, other, cross):
        s.shutdown()


if __name__ == '__main__':
    main()
