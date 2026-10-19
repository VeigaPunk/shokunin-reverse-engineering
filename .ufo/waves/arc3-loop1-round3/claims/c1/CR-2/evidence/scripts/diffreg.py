import hashlib,sys
def load(p): return open(p,'rb').read()
def lcp(a,b):
    n=min(len(a),len(b)); i=0
    while i<n and a[i]==b[i]: i+=1
    return i
pairs=[("rv2-off.Rv2Token","rv2-on200.Rv2Token"),("crv-off.CrVault","crv-on200.CrVault")]
for a,b in pairs:
    A=load(f"/var/tmp/cr2r3/work/{a}.runtime.bin"); B=load(f"/var/tmp/cr2r3/work/{b}.runtime.bin")
    n=lcp(A,B)
    # find first difference after the dispatcher prologue region
    print(f"{a} ({len(A)}B) vs {b} ({len(B)}B): first byte diff at offset {n} (0x{n:x})")
    print(f"  common prefix hex: {A[:n].hex()}")
    print(f"  A[{n}:{n+16}] = {A[n:n+16].hex()}   B[{n}:{n+16}] = {B[n:n+16].hex()}")
