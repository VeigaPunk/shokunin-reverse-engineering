"""Edge-case probes for fetch-vendor.py: non-tar image, image-cache logic."""
import importlib.util
import json
import os
import tempfile

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r40/R40W2C1PatchReview'
c = importlib.util.spec_from_file_location('fv', L + '/tools/round-40/fetch-vendor.py')
m = importlib.util.module_from_spec(c)
c.loader.exec_module(m)

# 1. materialise with a fetcher returning non-tar bytes -> uncaught?
entry = {'id': 'X', 'sha256': '0' * 64,
         'external': {'url': 'x://', 'image_sha256': '0' * 64,
                      'member': './m', 'length': 5}}
try:
    rec = m.materialise(entry, tempfile.mkdtemp(dir=S), None,
                        fetcher=lambda url, ic, want: (b'not a tar at all', 'fake'))
    print('non-tar image: returned rec ok=%s link=%s' % (rec.get('ok'), rec.get('link')))
except Exception as e:
    print('non-tar image: UNCAUGHT %s: %s' % (type(e).__name__, e))

# 2. materialise with external missing url -> uncaught KeyError?
entry2 = {'id': 'Y', 'sha256': '0' * 64, 'external': {'image_sha256': '0' * 64}}
try:
    rec = m.materialise(entry2, tempfile.mkdtemp(dir=S), None, fetcher=m.fetch)
    print('missing url: returned rec ok=%s link=%s' % (rec.get('ok'), rec.get('link')))
except Exception as e:
    print('missing url: UNCAUGHT %s: %s' % (type(e).__name__, e))

# 3. fetch() positive image-cache hit (no network): real V2 image already cached
V2_SHA = '3948449d89708589cde05e8495a34cb7ed1efeb880d1ed4539b07d4594069450'
V2_URL = ('https://download.avm.de/fritzbox/fritzbox-6820-lte/other/fritz.os/'
          'FRITZ.Box_6820v1_LTE-07.30.image')
b, how = m.fetch(V2_URL, os.path.join(S, 'images'), V2_SHA)
print('cache hit: how=%r bytes=%d sha_ok=%s' % (how, len(b), m.sha256(b) == V2_SHA))

# 4. stale image-cache file (wrong bytes under the wanted name) must not be trusted
stale = tempfile.mkdtemp(dir=S)
open(os.path.join(stale, V2_SHA + '.image'), 'wb').write(b'wrong bytes')
try:
    b2, how2 = m.fetch('bad://unreachable', stale, V2_SHA)
    print('stale cache: how=%r' % (how2,))
except Exception as e:
    print('stale cache: fell through to network, %s: %s (stale file NOT trusted)'
          % (type(e).__name__, e))
