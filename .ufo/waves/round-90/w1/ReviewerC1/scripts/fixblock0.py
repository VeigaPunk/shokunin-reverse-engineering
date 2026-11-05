#!/usr/bin/env python3
"""Reviewer probe: a repair that only patches block 0 — is it caught by P1?

Uses the round-89 block-0 law to set block 0's sz_cpr from its successor, i.e.
exactly the 'cheat that only fixes block 0'.  Run it on a later-block tamper;
P1 only recovers if every differing byte lies in the *tampered* window, which
this repair will violate when it bytes outside block 0's 4-byte window."""
import hashlib, importlib.util, json, os, struct, subprocess, sys, tempfile

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
r89 = importlib.util.module_from_spec(importlib.util.spec_from_file_location(
    "r89", ROOT + "/tools/round-89/upx-field-value-repair.py"))
import importlib.util as iu
spec = iu.spec_from_file_location("r89", ROOT + "/tools/round-89/upx-field-value-repair.py")
r89 = iu.module_from_spec(spec); spec.loader.exec_module(r89)

def fixblock0(cmd_in):
    out, info = r89.repair(open(cmd_in, "rb").read())
    return out, info

if __name__ == "__main__":
    path = "/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/work/run/t-jq--7"
    out, info = fixblock0(path)
    packed = open("/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/work/run/jq/packed", "rb").read()
    tampered = open(path, "rb").read()
    print("class:", info.get("class"))
    print("output==intact:", hashlib.sha256(out).hexdigest() == hashlib.sha256(packed).hexdigest())
    print("diff bytes vs tampered:", sum(1 for a, b in zip(tampered, out) if a != b),
          "diff bytes vs intact:", sum(1 for a, b in zip(packed, out) if a != b))
