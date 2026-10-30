import importlib.util, urllib.request, urllib.error, urllib.parse
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
fv=load('tools/round-50/fetch-vendor.py','fv')
# PURELY OFFLINE: replicate the guard predicate exactly as written, no network.
def fetch_guard(u):
    u = urllib.parse.urlsplit(u)
    return not (u.scheme != 'https' or u.hostname != fv.ALLOWED_HOST)
cases = ['https://download.avm.de/x.image',
         'http://download.avm.de/x.image',
         'https://evil.example/x.image',
         'https://download.avm.de:8443/x.image',
         'https://download.avm.de:443/x.image',
         'https://DOWNLOAD.AVM.DE/x.image',
         'https://download.avm.de.evil.example/x.image',
         'https://user:pw@download.avm.de/x.image',
         'https://download.avm.de@evil.example/x.image',
         'file:///etc/passwd']
for c in cases:
    print('%-6s %s' % ('PASSES' if fetch_guard(c) else 'refused', c))
# redirect guard predicate, offline
def redir_guard(newurl):
    u = urllib.parse.urlsplit(newurl)
    return not (u.scheme != 'https' or u.hostname != fv.ALLOWED_HOST)
for c in ['https://download.avm.de/y','http://download.avm.de/y','https://evil.example/y','https://download.avm.de:8443/y']:
    print('%-6s redirect-> %s' % ('PASSES' if redir_guard(c) else 'refused', c))
