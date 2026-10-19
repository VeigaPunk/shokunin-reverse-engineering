#!/usr/bin/env python3
"""derive-siglist.py — seat EX-05 (chain c1, arc3-loop1-round4).

Mechanically derive the canonical ABI signature list from a Vyper source
file, so the planted set is not hand-typed:

  * `name: public(TYPE)` public-variable declarations become getters:
      - value type          -> `name()`
      - HashMap[K, V]       -> `name(<K as ABI type>)`
  * `@external` `def name(args)` functions become `name(<args as ABI types>)`
  * `__init__` (constructor) and `__default__` (fallback) carry no selector
    and are excluded, with a note printed.

Vyper type -> ABI canonical type mapping covers the shapes used by this
round's carrier (uint256/int128/address/bool/Bytes[N]/String[N]/DynArray).
Unmapped types abort with an error rather than guessing.

usage: python3 derive-siglist.py <file.vy> [out.txt]
"""
import re
import sys

VALUE_TYPES = {
    "uint256", "int128", "address", "bool", "decimal", "uint8", "int256",
    "bytes32", "uint128", "uint16", "uint64", "uint32",
}


def abi_type(t: str) -> str:
    t = t.strip()
    if t in VALUE_TYPES:
        return t
    m = re.fullmatch(r"Bytes\[(\d+)\]", t)
    if m:
        return f"bytes{m.group(1)}"
    m = re.fullmatch(r"String\[(\d+)\]", t)
    if m:
        return "string"
    m = re.fullmatch(r"DynArray\[(.+),\s*\d+\]", t)
    if m:
        return abi_type(m.group(1)) + "[]"
    raise SystemExit(f"derive-siglist: unmapped Vyper type: {t!r}")


def split_args(s: str) -> list:
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def main():
    src_path = sys.argv[1]
    src = open(src_path).read()
    lines = src.splitlines()

    sigs, notes = [], []

    # public variable getters
    for ln in lines:
        m = re.match(r"\s*(\w+)\s*:\s*public\((.+)\)\s*$", ln)
        if not m:
            continue
        name, typ = m.group(1), m.group(2).strip()
        hm = re.fullmatch(r"HashMap\[(.+),\s*(.+)\]", typ)
        if hm:
            key_t = abi_type(hm.group(1).strip())
            sigs.append(f"{name}({key_t})")
        else:
            sigs.append(f"{name}()")

    # @external functions
    in_external = False
    for ln in lines:
        stripped = ln.strip()
        if stripped.startswith("@"):
            if stripped == "@external":
                in_external = True
            elif stripped.startswith("@"):
                pass
            continue
        m = re.match(r"\s*def\s+(\w+)\s*\((.*?)\)\s*(->\s*[^:]+)?\s*:\s*$", ln)
        if m and in_external:
            fname, args = m.group(1), m.group(2)
            if fname in ("__init__", "__default__"):
                notes.append(f"excluded (no selector): {fname}")
                in_external = False
                continue
            argtypes = []
            for a in split_args(args):
                at = a.split(":")[-1].strip()
                argtypes.append(abi_type(at))
            sigs.append(f"{fname}({','.join(argtypes)})")
        if m or stripped:
            in_external = False

    if not sigs:
        raise SystemExit("derive-siglist: no signatures derived")

    out = [f"# canonical signature list derived mechanically from {src_path}",
           f"# K={len(sigs)}"]
    out += sorted(set(sigs))
    out += [f"# note: {n}" for n in notes]
    text = "\n".join(out) + "\n"
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
