"""Corrected fetch-vendor probes: reach carve() with sha-consistent non-tar bytes;
missing member/length keys."""
import importlib.util
import tempfile

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r40/R40W2C1PatchReview'
c = importlib.util.spec_from_file_location('fv', L + '/tools/round-40/fetch-vendor.py')
m = importlib.util.module_from_spec(c)
c.loader.exec_module(m)

img = b'GARBAGE-NOT-A-TAR' * 10
isha = m.sha256(img)


def mk(ext_over):
    ext = {'url': 'x://', 'image_sha256': isha, 'member': './m', 'length': 5}
    ext.update(ext_over)
    return {'id': 'X', 'sha256': '0' * 64, 'external': ext}


def run(name, entry):
    try:
        rec = m.materialise(entry, tempfile.mkdtemp(dir=S), None,
                            fetcher=lambda url, ic, want: (img, 'fake'))
        print('%s: returned ok=%s link=%s' % (name, rec.get('ok'), rec.get('link')))
    except Exception as e:
        print('%s: UNCAUGHT %s: %s' % (name, type(e).__name__, e))


run('non-tar image (sha-consistent)', mk({}))
run('external missing member', mk({'member': None}) if False else
    {k: v for k, v in mk({}).items() if k != 'external'} | {'external': {'url': 'x://', 'image_sha256': isha, 'length': 5}})
run('external missing length', {'id': 'X', 'sha256': '0' * 64,
                                'external': {'url': 'x://', 'image_sha256': isha, 'member': './m'}})
run('length as string', mk({'length': '5'}))
