import io, json, os, sys, tarfile, hashlib, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_vendor_shim as fv  # loads the lane tool by path

body = b'sqsh' + bytes(range(256)) * 40 + b'TAILPAD!'
bio = io.BytesIO()
with tarfile.open(fileobj=bio, mode='w') as tf:
    ti = tarfile.TarInfo('./var/tmp/filesystem.image'); ti.size = len(body)
    tf.addfile(ti, io.BytesIO(body))
image = bio.getvalue()
length = len(body) - 8
pin = fv.sha256(body[:length])
member_true = fv.sha256(body)

def fake(url, ic, want): return image, 'fake'
d = tempfile.mkdtemp()
for label, member_pin in (('correct', member_true), ('WRONG', '0'*64), ('absent', None)):
    ext = {'url': 'x://', 'image_sha256': fv.sha256(image),
           'member': './var/tmp/filesystem.image', 'length': length}
    if member_pin is not None: ext['member_sha256'] = member_pin
    rec = fv.materialise({'id': 'V3', 'sha256': pin, 'external': ext},
                         os.path.join(d, label), None, fake)
    print('%-8s member_sha256=%-8s ok=%s link=%s detail=%s' % (
        label, (member_pin or 'ABSENT')[:8], rec['ok'], rec.get('link'),
        rec.get('member_detail')))
