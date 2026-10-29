#!/usr/bin/env python3
"""redirect_request probe with a REAL urllib Request (not a stub)."""
import importlib.util, json, os, urllib.error, urllib.request
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('fv', LANE + '/tools/round-50/fetch-vendor.py')
fv = importlib.util.module_from_spec(spec); spec.loader.exec_module(fv)
h = fv._AvmOnlyRedirect()
out = {}
for url in ('https://download.avm.de/ok',
            'https://download.avm.de:8443/ok',
            'https://download.avm.de/other/path',
            'https://evil.example/x',
            'http://download.avm.de/plain',
            'https://download.avm.de.evil.example/x',
            'https://u:p@evil.example/x'):
    req = urllib.request.Request(url)
    try:
        r = h.redirect_request(req, None, 302, 'Found', {'Location': url}, url)
        out[url] = {'result': 'ALLOWED', 'newurl': r.full_url}
    except urllib.error.HTTPError as e:
        out[url] = {'result': 'REFUSED', 'code': e.code, 'reason': e.reason}
    except Exception as e:
        out[url] = {'result': 'ERR', 'exc': type(e).__name__, 'msg': str(e)[:120]}
print(json.dumps(out, indent=1, sort_keys=True))
