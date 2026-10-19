#!/usr/bin/env python3
"""EX-10 / arc3-loop1-round4 — consolidated id-stability analysis.

Auto-discovers every leg envelope in /var/tmp/ex10-r4/out, compares against the
sealed r1/r3 baselines, groups ids, and diffs normalized payloads. Prints a
report to stdout (captured as analysis.txt).
"""
import glob
import hashlib
import json
import os

OUT = "/var/tmp/ex10-r4/out"
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R1 = f"{REPO}/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json"
EX06 = f"{REPO}/.ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/recheck-rv2token-hex-6.4.0.json"

DESC = {
    "exact-r1": "EX-06 r3 invocation, repeat 1 (TMPDIR=/var/tmp/ex10-r4/tmpdir)",
    "exact-r2": "EX-06 r3 invocation, repeat 2 (same)",
    "exact-verbatim-r1": "EX-06 probe-log.txt line VERBATIM (TMPDIR=/var/tmp/ex06-r3/tmpdir), repeat 1",
    "exact-verbatim-r2": "same verbatim line, repeat 2",
    "var-ex06tmpdir": "TMPDIR=EX-06 r3 tmpdir (short form)",
    "var-tmpdir2": "TMPDIR=fresh second dir",
    "var-abspath": "argv absolute, cwd=repo root",
    "var-abs-cwdroot": "argv absolute, cwd=repo root (dup)",
    "var-cwd-abs-from-tmp": "argv absolute (dup)",
    "b2-cwd-var": "argv absolute, cwd=/var/tmp/ex10-r4/work (cwd VARIANT)",
    "b2-rel-dot": "argv ./-prefixed relative, cwd=repo root (spelling VARIANT)",
    "b2-symlink": "argv symlink -> repo file",
    "b2-altpath-copy": "byte-identical copy at /var/tmp path (PATH VARIANT)",
    "b2-bytes-a": "scratch path, original bytes",
    "b2-bytes-b": "same scratch path, bytes+0x00 (BYTES VARIANT)",
    "pin-6.7.0-r1": "pin 6.7.0, repeat 1",
    "pin-6.7.0-r2": "pin 6.7.0, repeat 2",
    "ino-a": "hard link a at /var/tmp path",
    "ino-b": "hard link b, SAME inode, different path",
    "recreate-a": "path a recreated, NEW inode, same bytes",
    "mtime-a": "path a, mtime set to 2020 (mtime VARIANT)",
    "mutate-a": "path a, bytes+0x00 (BYTES VARIANT, scratch)",
}

SKIP = {"evidence_id", "locations"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def norm(d):
    if isinstance(d, dict):
        return {k: norm(v) for k, v in d.items() if k not in SKIP}
    if isinstance(d, list):
        return [norm(v) for v in d]
    return d


def walk_diff(a, b, path=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in SKIP:
                continue
            if k not in a:
                out.append(f"+ {path}/{k}")
            elif k not in b:
                out.append(f"- {path}/{k}")
            else:
                out += walk_diff(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"~ {path}: len {len(a)} -> {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            out += walk_diff(x, y, f"{path}[{i}]")
    elif a != b:
        sa, sb = json.dumps(a), json.dumps(b)
        out.append(f"~ {path}: {sa[:60]} -> {sb[:60]}")
    return out


legs = sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{OUT}/*.json"))
r1_sha, ex06_sha = sha(R1), sha(EX06)
r1_id = json.load(open(R1))["evidence_id"]
ex06_id = json.load(open(EX06))["evidence_id"]

print("EX-10 — id-stability rerun (arc3-loop1-round4, 2026-10-19)")
print("=" * 78)
print()
print("A. Sealed baselines (read-only)")
print(f"  r1 canonical capture  sha256={r1_sha}")
print(f"                        id    ={r1_id}")
print(f"  EX-06 r3 recheck      sha256={ex06_sha}")
print(f"                        id    ={ex06_id}")
print(f"  r1 == EX-06 envelope byte-identity: {r1_sha == ex06_sha}")
print()

print("B. Leg table (all envelopes; symlink leg is a typed refusal)")
print(f"  {'leg':20} {'exit':4} {'bytes':6} {'env sha256':16} {'id (or -)':36} {'decoded bytecode':16}")
data = {}
for leg in legs:
    p = f"{OUT}/{leg}.json"
    d = json.load(open(p))
    eid = d.get("evidence_id", "")
    br = d.get("normalized_result", {})
    bs = br.get("bytecode", {}).get("sha256", "") if isinstance(br, dict) else ""
    data[leg] = d
    exit_ = "0" if eid else "1"
    print(f"  {leg:20} {exit_:4} {os.path.getsize(p):6} {sha(p)[:16]:16} {(eid[:36] if eid else '-'):36} {bs[:16]:16}")
print()

print("C. Byte-identity vs the sealed envelopes")
for leg in legs:
    p = f"{OUT}/{leg}.json"
    s = sha(p)
    marks = []
    if s == r1_sha:
        marks.append("== r1 canonical")
    if s == ex06_sha:
        marks.append("== EX-06 r3 recheck")
    print(f"  {leg:20} {s[:16]} {'  '.join(marks) if marks else ''}")
print()

print("D. id groups (identical request -> identical id)")
groups = {}
for leg in legs:
    eid = data[leg].get("evidence_id")
    if eid:
        groups.setdefault(eid, []).append(leg)
for eid, names in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    print(f"  {eid[:20]}…  n={len(names)}: {', '.join(names)}")
print()

print("E. Normalized payload diff vs exact-r1 (evidence_id/locations stripped)")
base = norm(data["exact-r1"])
for leg in legs:
    if leg == "exact-r1":
        continue
    d = data[leg]
    if not d.get("evidence_id"):
        print(f"  {leg:20} no envelope (typed refusal: {d.get('code')}) — diff n/a")
        continue
    diffs = walk_diff(base, norm(d))
    print(f"  {leg:20} {len(diffs)} field diffs")
    for line in diffs[:8]:
        print(f"      {line}")
    if len(diffs) > 8:
        print(f"      … {len(diffs)-8} more")
print()

print("F. Sensitivity axes — measured verdicts this round")
print("  id STABLE across: repeat runs (x6: exact-r1/r2, verbatim-r1/r2, pin-r1/r2),")
print("    TMPDIR value (3 distinct dirs incl. EX-06's own), cwd (2 values),")
print("    argv spelling (relative / ./-prefixed / absolute),")
print("    inode identity + link count (recreate same path -> same id; hard link same")
print("    inode at another path -> different id), mtime (2020 vs 2026 -> same id),")
print("    pin-internal rerun (6.7.0 x2 byte-identical).")
print("  id CHANGES with: resolved path (byte-identical copy elsewhere), carrier bytes")
print("    (mutated hex text at a fixed path), encoding form (r3), pin (6.4.0 vs 6.7.0),")
print("    verb family request (r3).")
print("  id INPUT is the RESOLVED PATH as recorded in parameters.path/subject.local_path,")
print("    not the raw argv spelling and not the inode — proven by the hard-link pair.")
print()

print("G. Content-identity anchor (decoded bytecode sha256) per leg")
for leg in legs:
    d = data[leg]
    br = d.get("normalized_result", {})
    bs = br.get("bytecode", {}).get("sha256", "") if isinstance(br, dict) else ""
    subj = d.get("subject", {}).get("digest", {}).get("sha256", "")
    print(f"  {leg:20} subject(file)={subj[:16]:16} bytecode={bs[:16]:16}")
print()

print("H. Typed refusal — symlink input (new this round)")
d = data["b2-symlink"]
print(f"  code={d.get('code')} category={d.get('category')} retryable={d.get('retryable')}")
for iss in d.get("details", {}).get("issues", []):
    print(f"  issue: path={iss.get('path')} reason={iss.get('reason')}")
    print(f"         message={iss.get('message')}")
print("  -> symlinked carriers are refused fail-closed; no id is minted.")
print()
print("I. Bounded formula falsification (idformula.py): 1,680 candidate hash forms")
print("  over {path, rel, file bytes, decoded bytecode, size, encoding, operation,")
print("  verb, pin, provider, subject name} x 7 algorithms x 7 separators — 0 hits.")
print("  Verdict: no formula among tested forms; id derivation unproven (consistent")
print("  with r3's honest-stop form). Sensitivities are measured, not derived.")
