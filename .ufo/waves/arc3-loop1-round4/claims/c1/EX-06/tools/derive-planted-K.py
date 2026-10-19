#!/usr/bin/env python3
"""Derive the planted selector set K from the Vyper source, pre-probe.

Reads the .vy source, extracts:
  - public state vars  `name: public(TYPE)`            -> name(args-from-TYPE)
  - external functions `@external def name(a: T, ...)` -> name(T, ...)
and derives 4-byte selectors with the local pure-python keccak256.

Records source sha256 + derivation timestamp. Output JSON is the planted-K
record; it must be written BEFORE any probe envelope exists.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from keccak import selector  # noqa: E402

TYPES = {
    "uint256": "uint256", "int256": "int256", "address": "address",
    "bool": "bool", "bytes32": "bytes32", "String": "string",
    "Bytes": "bytes", "decimal": "decimal",
}


def canon(t: str) -> str:
    t = t.strip()
    if t.startswith("HashMap["):
        inner = t[len("HashMap["):-1]
        key = inner.split(",")[0].strip()
        return canon(key)
    if t.startswith("DynArray["):
        inner = t[len("DynArray["):-1]
        base = inner.split(",")[0].strip()
        return canon(base) + "[]"
    return TYPES.get(t, t)


def main() -> int:
    src_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    src_bytes = src_path.read_bytes()
    src_sha = hashlib.sha256(src_bytes).hexdigest()
    text = src_bytes.decode()

    sigs = []
    # public state vars — Vyper auto-getter takes NO args for scalar types;
    # for HashMap[K, V] it takes the key type only.
    for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*public\(([^)]+)\)", text, re.M):
        name, typ = m.group(1), m.group(2)
        if typ.strip().startswith("HashMap["):
            key = typ.strip()[len("HashMap["):-1].split(",")[0].strip()
            args = canon(key)
        else:
            args = ""
        sigs.append({"name": name, "signature": f"{name}({args})", "kind": "public-var", "vy_type": typ})

    # external functions (decorator block then def)
    for m in re.finditer(r"@(external|public)\b[^\n]*\n(?:\s*@[A-Za-z_]+\b[^\n]*\n)*\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", text):
        kind = m.group(1)
        name = m.group(2)
        params = m.group(3).strip()
        args = []
        if params:
            for p in params.split(","):
                p = p.strip()
                if not p:
                    continue
                if ":" not in p:
                    raise SystemExit(f"unparsable param {p!r} in {name}")
                ptype = p.split(":", 1)[1].strip()
                args.append(canon(ptype))
        sigs.append({"name": name, "signature": f"{name}({','.join(args)})", "kind": f"{kind}-fn"})

    seen = set()
    planted = []
    for s in sigs:
        if s["name"] == "__default__" or s["name"] == "__init__":
            continue
        sel = selector(s["signature"])
        if sel in seen:
            continue
        seen.add(sel)
        planted.append({"selector": sel, "signature": s["signature"], "kind": s["kind"]})

    ts = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()
    doc = {
        "carrier_source": str(src_path),
        "source_sha256": src_sha,
        "derivation": "pure-python keccak256 over source-declared external signatures (keccak.py, selftest PASS)",
        "recorded_utc": ts,
        "k": len(planted),
        "selectors": sorted(planted, key=lambda d: d["selector"]),
    }
    out_path.write_text(json.dumps(doc, indent=2) + "\n")
    print(f"recorded_utc: {ts}")
    print(f"source_sha256: {src_sha}")
    print(f"K = {len(planted)}")
    for p in doc["selectors"]:
        print(f"  {p['selector']}  {p['signature']}  [{p['kind']}]")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
