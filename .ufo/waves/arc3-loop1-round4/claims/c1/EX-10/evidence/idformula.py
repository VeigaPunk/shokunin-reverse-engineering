#!/usr/bin/env python3
"""EX-10 — bounded falsification attempt: is the ev_ id a sha256 over request fields?"""
import hashlib, itertools, json, sys

TARGET = "45849c8b11794ea0b007bd01ea3241aa9b385ca7543e514a16e82c795a106eaf"
TARGET67 = "19d7d3cb291835233fece9c457935680eea0e1ddb0695035ac1097f66d0b3f38"

PATH = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex"
REL = ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex"
BYTES = "d7f73058e2d9fb2563bf96b2f26902f233530de027a7943185e15bfdc4e1048f"
BC = "c1081a565869b50387211b25afaf3768294aa774c35845bc3a8c0b12cfe15e74"
SIZE = "3886"

fields = {
    "path": PATH, "rel": REL, "bytes": BYTES, "bytecode": BC, "size": SIZE,
    "enc": "hex", "op": "inspect_evm_interface",
    "verb": "inspect-evm-interface", "pin": "6.4.0", "tool": "rea-agents",
    "provider": "evmole-interface", "subject": "Rv2Token.runtime.hex",
}

algos = {"sha256": hashlib.sha256, "sha512": hashlib.sha512, "sha1": hashlib.sha1,
         "md5": hashlib.md5, "blake2b": hashlib.blake2b, "blake2s": hashlib.blake2s,
         "sha3_256": hashlib.sha3_256}
seps = ["", "|", ":", "\n", " ", "\x00", ","]
keys = list(fields)

hits = []
tested = 0
# single fields, and ordered tuples up to length 4 over a focused subset
subsets = [("path","enc"), ("path","enc","pin"), ("path","bytes","enc"),
           ("bytes","enc"), ("path","enc","pin","bytes"),
           ("path","enc","op"), ("path","enc","verb","pin"),
           ("path","enc","bytes","pin"), ("path","bytes"),
           ("path",), ("bytes",), ("bytecode",), ("subject","enc"),
           ("path","enc","size"), ("path","enc","provider")]
for ks in subsets:
    for sep in seps:
        for suffix in ("", "\n"):
            s = sep.join(fields[k] for k in ks) + suffix
            for an, fn in algos.items():
                tested += 1
                h = fn(s.encode()).hexdigest()
                if h == TARGET or h[:32] == TARGET[:32] or h[:16] == TARGET[:16]:
                    hits.append((an, sep, ks, suffix, h))
                if h == TARGET67:
                    hits.append((an, sep, ks, suffix, h, "6.7.0"))
# json canonical forms
for ks in subsets:
    for sort in (True, False):
        s = json.dumps({k: fields[k] for k in ks}, sort_keys=sort, separators=(",", ":"))
        for an, fn in algos.items():
            tested += 1
            h = fn(s.encode()).hexdigest()
            if h == TARGET:
                hits.append((an, "json", ks, sort, h))

print(f"candidate forms tested: {tested}")
print(f"exact hits: {len(hits)}")
for h in hits:
    print("  HIT:", h)
print("verdict:", "FORMULA FOUND" if hits else "no formula among tested forms")
