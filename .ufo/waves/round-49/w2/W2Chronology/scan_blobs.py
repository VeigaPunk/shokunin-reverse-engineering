import sys, hashlib, subprocess
want = {
 "d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779": "c1-counter draft (wave-1 attacked)",
 "90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f": "c2-mismatch draft (wave-1 attacked)",
 "209f0f4ad0568a6e845b72dcd8ca5102caa13423884391dd9a92398e26d087a4": "c1-controls draft (wave-1 attacked)",
 "f9161ff3afa2ded9553ea77dc31432add67ca6f6a02e98b3eb22c74da33a46fb": "c1-run.py draft (wave-1 attacked)",
 "984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492": "plan draft (wave-1 attacked)",
}
oids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
p = subprocess.run(['git','cat-file','--batch'], input='\n'.join(oids).encode()+b'\n', capture_output=True)
data = p.stdout; i = 0; n = 0; hits = []
while i < len(data):
    nl = data.index(b'\n', i)
    hdr = data[i:nl].split()
    i = nl + 1
    if len(hdr) < 3: break
    oid, typ, size = hdr[0].decode(), hdr[1].decode(), int(hdr[2])
    body = data[i:i+size]; i += size + 1
    n += 1
    h = hashlib.sha256(body).hexdigest()
    if h in want: hits.append((want[h], oid, size))
print('blobs scanned', n)
print('HITS', hits if hits else 'none')
