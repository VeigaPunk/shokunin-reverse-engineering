import os, shutil, sys
REPO="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S="/var/tmp/pl3-arc3r6"
FILES=["PROVINCE.md","SKILL.md","SCORECARD.md"]
raw={f:open(os.path.join(REPO,f),"rb").read() for f in FILES}
def tree(name, mutate=None):
    d=os.path.join(S,"trees",name); os.makedirs(d,exist_ok=True)
    for f,b in raw.items():
        if f=="PROVINCE.md" and mutate is not None:
            lines=b.decode().splitlines()
            lines=mutate(lines)
            b=("\n".join(lines)+"\n").encode()
        open(os.path.join(d,f),"wb").write(b)
    return d
def frozen(L):
    L[91]="  (Core, r3-07); real solc/vyper-compiled bytecode untested; selectors stay"
    L[92]="  bare hashes (no signature DB \u2192 no name resolution)."
    return L
def forbidden_only(L):
    L[92]=L[92].replace("selectors stay bare hashes","selectors stay untested bare hashes")
    return L
def req_evm(L):
    L[91]=L[91].replace("real solc-0.8.37 carriers","real carriers").replace("and a vyper-0.4.3","and a vyper")
    return L
def trunc161(L): return L[:161]
def pin88(L):
    L[87]=L[87]+" rea-agents@6.3.0"
    return L
def ins(L,idx): L.insert(idx,""); return L
tree("clean")
tree("frozen",frozen)
tree("forbidden-only",forbidden_only)
tree("req-evm",req_evm)
tree("trunc161",trunc161)
tree("pin88",pin88)
tree("ins75",lambda L: ins(L,74))
tree("ins82",lambda L: ins(L,81))
tree("ins134",lambda L: ins(L,133))
print("built")
