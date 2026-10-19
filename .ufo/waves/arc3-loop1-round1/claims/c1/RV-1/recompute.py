#!/usr/bin/env python3
"""RV-1 independent selector recomputation.

Path: pure-Python Keccak-256 (keccak_ref.py, written from the Keccak reference
spec) validated against node/OpenSSL SHA3-256 by padding-swap, plus published
vectors. No third-party library, no `rea` probe, no solc call.

Modes:
  sol <file.sol>          extract candidate external/public function signatures
                          from Solidity source text and print keccak(sig)[:4]
  abi <file.abi.json>     derive canonical signatures from a compiler ABI JSON
  scan <file> <sel.txt>   check each selector's 4 bytes appear in raw bytecode
  cmp <a.txt> <b.txt>     set comparison of selector lists (bare hex)
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import keccak_ref as K

BASIC = {"uint": "uint256", "int": "int256", "byte": "bytes1"}


def canonical_type(t):
    t = t.strip()
    if t in BASIC:
        return BASIC[t]
    if t.endswith("]"):
        # array: canonicalize the base type, keep dimensions
        i = t.index("[")
        return canonical_type(t[:i]) + t[i:]
    return t


def canonicalize_sig(name, params):
    return f"{name}({','.join(canonical_type(p) for p in params)})"


def sel(sig):
    return K.keccak_256(sig.encode("ascii")).hex()[:8]


def strip_comments(src):
    src = re.sub(r"//[^\n]*", "", src)
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return src


def extract_from_sol(path):
    """Regex extraction of function signatures from source text."""
    src = strip_comments(open(path).read())
    out = []
    # function name(params) <modifiers> returns(...) ;  -- capture visibility/modifiers tail
    for m in re.finditer(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(([^)]*)\)([^{;]*)", src):
        name, params, tail = m.group(1), m.group(2), m.group(3)
        vis = re.search(r"\b(external|public|internal|private)\b", tail)
        if not vis or vis.group(1) not in ("external", "public"):
            continue
        ptypes = []
        for p in [p.strip() for p in params.split(",") if p.strip()]:
            p = re.sub(r"\b(indexed|memory|storage|calldata|payable)\b", " ", p)
            toks = p.split()
            if not toks:
                continue
            # first token that looks like a type
            ptypes.append(toks[0])
        out.append(canonicalize_sig(name, ptypes))
    # public state vars get auto-generated getters (Solidity >=0.5: `Type public name;`)
    for m in re.finditer(r"^\s*([A-Za-z_$][\w$\.\[\]()\s=>,]*?)\s+public\s+([A-Za-z_$][\w$]*)\s*(?:=[^;]*)?;", src, re.M):
        ty, nm = m.group(1).strip(), m.group(2)
        if ty.startswith("function") or "(" in ty and not ty.startswith("mapping"):
            continue
        mm = re.match(r"mapping\s*\(\s*([^=]+?)\s*=>", ty)
        if mm:  # mapping(K => V) public m; -> getter m(K)
            out.append(canonicalize_sig(nm, [mm.group(1).strip()]))
            continue
        if ty.endswith("]"):  # T[] / T[N] public a; -> getter a(uint256)
            out.append(canonicalize_sig(nm, ["uint256"]))
            continue
        # scalar public var -> getter takes NO arguments (`uint8 public decimals` -> decimals())
        out.append(canonicalize_sig(nm, []))
    return sorted(set(out))


def extract_from_abi(path):
    abi = json.load(open(path))
    sigs = []
    for e in abi:
        if e.get("type") == "function":
            params = []
            for i in e.get("inputs", []):
                t = i["type"]
                if t.startswith("tuple"):
                    inner = ",".join(x["type"] for x in i.get("components", []))
                    t = f"({inner})" + t[len("tuple"):]
                params.append(t)
            sigs.append(canonicalize_sig(e["name"], params))
    return sorted(set(sigs))


def main():
    cmd = sys.argv[1]
    if cmd == "sol":
        sigs = extract_from_sol(sys.argv[2])
        for s in sigs:
            print(f"{sel(s)} {s}")
        print(f"K={len(sigs)}")
        return 0
    if cmd == "abi":
        sigs = extract_from_abi(sys.argv[2])
        for s in sigs:
            print(f"{sel(s)} {s}")
        print(f"K={len(sigs)}")
        return 0
    if cmd == "scan":
        code = open(sys.argv[2], "rb").read()
        if code[:1] not in (b"\x00", b"\x60", b"\x61", b"\x80"):
            try:
                code = bytes.fromhex(code.decode().strip().removeprefix("0x"))
            except Exception:
                pass
        lines = [l.strip() for l in open(sys.argv[3]) if l.strip()]
        n = 0
        for l in lines:
            s = l.split()[0].lower().removeprefix("0x")
            if len(s) != 8:
                continue
            offs = [i for i in range(len(code) - 3) if code[i:i + 4].hex() == s]
            n += bool(offs)
            print(f"{'present' if offs else 'ABSENT '} {s} offsets={offs} ({len(code)} bytes)")
        print(f"present {n}/{len(lines)}")
        return 0
    if cmd == "cmp":
        def load(p):
            vals = set()
            for l in open(p):
                l = l.strip()
                if not l or l.startswith("#") or l.startswith("K="):
                    continue
                vals.add(l.split()[0].lower().removeprefix("0x"))
            return vals
        a, b = load(sys.argv[2]), load(sys.argv[3])
        print(f"ref {sys.argv[2]}: {len(a)} selectors")
        print(f"cmp {sys.argv[3]}: {len(b)} selectors")
        print(f"missing_vs_ref={sorted(a - b)}")
        print(f"extra_vs_ref={sorted(b - a)}")
        print("VERDICT:", "MATCH" if a == b else "MISMATCH")
        return 0 if a == b else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
