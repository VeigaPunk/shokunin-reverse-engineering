#!/usr/bin/env python3
"""R30-C2 counter: REA 6.5.0 `inspect-rust-binary` refusal signatures predicted from code.

Each mutant is a deterministic edit of the frozen base carrier `elf-x86_64-uvx`
(round-30 C1 carrier list). The predicted outcome of every mutant was written
from the opened REA 6.5.0 source (round-30 SOURCES row S090) before any REA run
on any mutant, and is frozen in corpus/evidence/round-30/c2/predictions.tsv.

Frozen predicate P2 (the same sentence is in .ufo/waves/round-30/claims.json):
  "A mutant matches when its live REA 6.5.0 inspect-rust-binary run agrees with
   its frozen prediction: for a predicted refusal, the envelope is not ok and the
   frozen message appears verbatim in the run's stdout or stderr; for a predicted
   acceptance, the run exits 0 with an ok inspect_rust_binary envelope whose
   subject sha256 is the mutant's sha256 and whose package multiset, file_offset
   and compressed_bytes equal the oracle's reading of the mutant; and its
   committed envelope, first added after the freeze commit, agrees with the live
   run on ok and evidence_id."

Exit 0 only when matches == TARGET (19 of 19 frozen mutants), entry_ok and
skill_ok; exit 1 when measured but not met; exit 2 when a pinned input is absent
or altered.

Usage:
  c2-rust-refusals.py --build --root <LANE>       # (re)build mutants; checks frozen sha256 when predictions exist
  c2-rust-refusals.py --root <LANE> [--rev main] [--write-evidence]
  c2-rust-refusals.py --selftest
"""

import argparse
import csv
import datetime
import hashlib
import importlib.util
import json
import os
import re
import struct
import subprocess
import sys
import zlib

REA = ["npx", "-y", "rea-agents@6.5.0"]
TARGET = 19
PKG_JSON = os.path.expanduser("~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json")
BASE_ID = "elf-x86_64-uvx"
BASE_SHA = "2e9105ad94813196"  # prefix check; full sha comes from the C1 carrier list
MUT_DIR = "/fast/scratch/hyaku/kaidoku-r30/mutants"
PRED = "corpus/evidence/round-30/c2/predictions.tsv"
CARRIERS = "corpus/evidence/round-30/c1/carriers.tsv"
ENTRY = "corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md"
CLAIM_ROW = "S090"
BASE = "d210fb8fa62d2af04d009cfa0c65a4e8137dc742"
HERE = os.path.dirname(os.path.abspath(__file__))
MATCH = "P2-match"
MISS = "P2-miss"


def load_oracle():
    spec = importlib.util.spec_from_file_location("rust_dep_oracle", os.path.join(HERE, "rust_dep_oracle.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- ELF64 editing
def shdrs(data):
    shoff = struct.unpack_from("<Q", data, 0x28)[0]
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x3A)
    stro, strs = struct.unpack_from("<QQ", data, shoff + shstrndx * shentsize + 0x18)
    out = []
    for i in range(shnum):
        b = shoff + i * shentsize
        name = struct.unpack_from("<I", data, b)[0]
        end = data.find(b"\0", stro + name)
        out.append({"index": i, "base": b, "name_off": name, "name": data[stro + name:end].decode()})
    return out


def section(data, name):
    hits = [s for s in shdrs(data) if s["name"] == name]
    assert len(hits) == 1, name
    return hits[0]


def put(buf, off, fmt, *vals):
    struct.pack_into(fmt, buf, off, *vals)


def relocate(base, payload):
    """Append payload at an 16-aligned EOF offset and point .dep-v0 at it."""
    buf = bytearray(base)
    pad = (-len(buf)) % 16
    buf += b"\0" * pad
    off = len(buf)
    buf += payload
    s = section(bytes(buf), ".dep-v0")
    put(buf, s["base"] + 0x18, "<QQ", off, len(payload))
    return bytes(buf)


def original_section(base):
    s = section(base, ".dep-v0")
    off, size = struct.unpack_from("<QQ", base, s["base"] + 0x18)
    return base[off:off + size]


def build_mutants(base):
    """Return list of (id, bytes, kind, message, code_pointer). Deterministic."""
    raw = original_section(base)
    doc = json.loads(zlib.decompress(raw).decode())
    n = len(doc["packages"])
    def js(d):
        return json.dumps(d, separators=(",", ":")).encode()
    def z(b, level=9):
        return zlib.compress(b, level)
    root_i = [i for i, p in enumerate(doc["packages"]) if p.get("root")]
    other = 0 if 0 not in root_i else 1
    m = []
    m.append(("g-relocated", relocate(base, raw), "ok", "", "RustBinaryImage.js:56 readDependency"))
    m.append(("g-recompressed", relocate(base, z(js(doc))), "ok", "", "RustAuditableReader.js:76 inflateSection"))
    noroot = json.loads(json.dumps(doc))
    for p in noroot["packages"]:
        p.pop("root", None)
    m.append(("g-no-root", relocate(base, z(js(noroot))), "ok", "", "RustAuditableReader.js:159 roots[0] ?? null"))
    buf = bytearray(base)
    s = section(base, ".dep-v0")
    put(buf, s["base"] + 0x20, "<Q", 0)
    m.append(("r-empty", bytes(buf), "refuse", "Dependency section is not file-backed", "GoBinaryContainer.js:80 file_backed: size > 0n; RustBinaryImage.js:52-53"))
    buf = bytearray(base)
    put(buf, s["base"] + 4, "<I", 8)
    m.append(("r-nobits", bytes(buf), "refuse", "Dependency section is not file-backed", "GoElfImage.js:185-186 SHT_NOBITS; RustBinaryImage.js:52-53"))
    buf = bytearray(base)
    flags = struct.unpack_from("<Q", base, s["base"] + 8)[0]
    put(buf, s["base"] + 8, "<Q", flags | 0x800)
    m.append(("r-compressed-flag", bytes(buf), "refuse", "Compressed dependency sections are unsupported", "GoElfImage.js:187; RustBinaryImage.js:50-51"))
    buf = bytearray(base)
    comment = section(base, ".comment")
    put(buf, comment["base"], "<I", s["name_off"])
    m.append(("r-two-sections", bytes(buf), "refuse", "Image contains more than one dependency section", "RustBinaryImage.js:45-46"))
    junk = bytes((i * 151 + 7) % 256 for i in range(len(raw)))
    m.append(("r-not-zlib", relocate(base, junk), "refuse", "Dependency section is not a complete zlib stream", "RustAuditableReader.js:131-134 inflateFailure Z_*"))
    m.append(("r-trailing-bytes", relocate(base, raw + b"\x00\x01\x02\x03"), "refuse", "Dependency section is not a complete zlib stream", "RustAuditableReader.js:79-82,131-134 (node v24.21.0 rejects trailing junk)"))
    big = bytes((i * 31 + 3) % 256 for i in range(1024 * 1024 + 1))
    m.append(("r-over-1mib", relocate(base, big), "refuse", "Dependency section exceeds the 1 MiB compressed limit", "RustAuditableReader.js:54-58 RUST_SECTION_BYTES"))
    padded = js(doc)[:-1] + b" " * (3 * 1024 * 1024) + b"}"
    m.append(("r-inflate-ratio", relocate(base, z(padded)), "refuse", "Inflated dependency JSON exceeds the size limit", "RustAuditableReader.js:73,128-129 RUST_INFLATE_RATIO"))
    m.append(("r-not-utf8", relocate(base, z(b"\xff\xfe\xfd")), "refuse", "Dependency JSON is not valid UTF-8", "RustAuditableReader.js:151-152"))
    m.append(("r-bad-json", relocate(base, z(b'{"packages":[')), "refuse", "Dependency section JSON is invalid", "RustAuditableReader.js:159-160"))
    m.append(("r-nesting-33", relocate(base, z(b"[" * 33 + b"]" * 33)), "refuse", "Dependency JSON nesting exceeds 32 levels", "RustAuditableReader.js:285 JSON_DEPTH"))
    m.append(("r-format-negative", relocate(base, z(b'{"format":-1,"packages":[]}')), "refuse", "Dependency JSON does not match the format schema", "RustAuditableReader.js:162-164"))
    extra = json.loads(json.dumps(doc))
    extra["packages"][0]["features"] = []
    m.append(("r-extra-field", relocate(base, z(js(extra))), "refuse", "Dependency package 0 does not match the package schema", "RustAuditableReader.js:220-246"))
    badkind = json.loads(json.dumps(doc))
    badkind["packages"][0]["kind"] = "dev"
    m.append(("r-kind-dev", relocate(base, z(js(badkind))), "refuse", "Dependency package 0 does not match the package schema", "RustAuditableReader.js:251-254"))
    two = json.loads(json.dumps(doc))
    two["packages"][other]["root"] = True
    m.append(("r-two-roots", relocate(base, z(js(two))), "refuse", "Dependency JSON declares more than one root package", "RustAuditableReader.js:151-153 rootIndex"))
    idx = json.loads(json.dumps(doc))
    idx["packages"][0]["dependencies"] = idx["packages"][0].get("dependencies", []) + [n]
    m.append(("r-index-outside", relocate(base, z(js(idx))), "refuse",
              "Dependency index %d from package 0 is outside the package list" % n, "RustAuditableReader.js:154-157 rootIndex"))
    return m


# ---------------------------------------------------------------- judging
def find_metadata(node):
    found = []
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "auditable_metadata":
                    found.append(v)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(node)
    uniq = []
    for v in found:
        if v not in uniq:
            uniq.append(v)
    return uniq


def rea_tuples(meta):
    pk = meta["packages"]
    out = []
    for p in pk:
        deps = tuple(sorted((pk[i]["name"], pk[i]["version"]) for i in p.get("dependencies", [])))
        out.append((p["name"], p["version"], p["source"], p.get("kind"), bool(p.get("root", False)), deps))
    return sorted(out, key=repr)


def judge(pred, env, out_text, err_text, code, mutant_sha, oracle_reading):
    kind, message = pred["kind"], pred["message"]
    if kind == "refuse":
        if isinstance(env, dict) and env.get("ok") is True:
            return MISS, "accepted, refusal predicted"
        if not message or (message not in out_text and message not in err_text):
            return MISS, "predicted message absent"
        return MATCH, "refused with predicted message"
    if code != 0 or not isinstance(env, dict) or env.get("ok") is not True:
        return MISS, "not accepted (exit %s)" % code
    data = env.get("data") or {}
    if data.get("operation") != "inspect_rust_binary":
        return MISS, "operation %r" % data.get("operation")
    if ((data.get("subject") or {}).get("digest") or {}).get("sha256") != mutant_sha:
        return MISS, "subject sha256"
    metas = find_metadata(data)
    if len(metas) != 1 or not isinstance(metas[0], dict) or oracle_reading is None:
        return MISS, "metadata missing"
    sec, tuples = oracle_reading
    if not tuples:
        return MISS, "oracle empty"
    try:
        if rea_tuples(metas[0]) != tuples:
            return MISS, "package multiset differs"
    except (KeyError, IndexError, TypeError):
        return MISS, "metadata shape"
    if metas[0].get("file_offset") != sec["offset"] or metas[0].get("compressed_bytes") != sec["size"]:
        return MISS, "offset/size differ"
    return MATCH, "accepted, packages=%d" % len(tuples)


def git(root, *args):
    return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)


def show(root, rev, rel):
    p = git(root, "show", rev + ":" + rel)
    return p.stdout if p.returncode == 0 else None


def first_add(root, rev, rel):
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", rel)
    t = [int(x) for x in p.stdout.split()]
    return min(t) if t else None


def committed_agrees(committed, live, added, freeze_ct):
    if freeze_ct is None or added is None or added <= freeze_ct:
        return False, "committed envelope absent or not added after the freeze"
    c_ok = isinstance(committed, dict) and committed.get("ok") is True
    l_ok = isinstance(live, dict) and live.get("ok") is True
    if c_ok != l_ok:
        return False, "committed ok %s != live ok %s" % (c_ok, l_ok)
    if l_ok and (committed.get("data") or {}).get("evidence_id") != (live.get("data") or {}).get("evidence_id"):
        return False, "committed evidence_id differs"
    return True, "ok"


def entry_ok(root, rev):
    text = show(root, rev, ENTRY)
    if text is None:
        return False, "entry absent at rev"
    src = [l for l in text.splitlines() if l.startswith("source:")]
    if not src or CLAIM_ROW not in src[0]:
        return False, "entry source line lacks %s" % CLAIM_ROW
    srcs = show(root, rev, "corpus/SOURCES.md") or ""
    if not re.search(r"^\| %s \|" % CLAIM_ROW, srcs, re.M):
        return False, "%s not in SOURCES.md" % CLAIM_ROW
    if re.search(r"^\| %s \|" % CLAIM_ROW, show(root, BASE, "corpus/SOURCES.md") or "", re.M):
        return False, "%s already present at base" % CLAIM_ROW
    return True, "ok"


def skill_ok(root, rev):
    text = show(root, rev, "SKILL.md") or ""
    base = (show(root, BASE, "SKILL.md") or "").splitlines()
    lines = [l for l in text.splitlines() if "inspect-rust-binary" in l and ENTRY in l and l not in base]
    return (True, "ok") if lines else (False, "no new SKILL.md line names inspect-rust-binary with the entry")


def base_carrier(root):
    rows = {r["id"]: r for r in csv.DictReader(open(os.path.join(root, CARRIERS)), delimiter="\t")}
    r = rows[BASE_ID]
    data = open(r["path"], "rb").read()
    if sha(data) != r["sha256"] or not r["sha256"].startswith(BASE_SHA):
        raise SystemExit("PIN base carrier altered")
    return data


def do_build(root):
    base = base_carrier(root)
    os.makedirs(MUT_DIR, exist_ok=True)
    muts = build_mutants(base)
    pred_path = os.path.join(root, PRED)
    frozen = {}
    if os.path.exists(pred_path):
        frozen = {r["id"]: r for r in csv.DictReader(open(pred_path), delimiter="\t")}
    rows = []
    bad = 0
    for mid, b, kind, msg, ptr in muts:
        p = os.path.join(MUT_DIR, mid)
        if os.path.exists(p):
            os.chmod(p, 0o644)
        open(p, "wb").write(b)
        os.chmod(p, 0o444)
        h = sha(b)
        if frozen and frozen.get(mid, {}).get("sha256") != h:
            bad += 1
            print("PIN mutant %s sha256 differs from frozen" % mid)
        rows.append((mid, kind, msg, h, len(b), p, ptr))
    if not frozen:
        os.makedirs(os.path.dirname(pred_path), exist_ok=True)
        with open(pred_path, "w") as f:
            f.write("id\tkind\tmessage\tsha256\tsize\tpath\tcode_pointer\n")
            for r in rows:
                f.write("\t".join(str(x) for x in r) + "\n")
    print("mutants=%d rebuilt pin_mismatch=%d" % (len(rows), bad))
    return 2 if bad else 0


def measure(root, rev, write_evidence):
    if do_build(root) != 0:
        return 2
    oracle = load_oracle()
    preds = list(csv.DictReader(open(os.path.join(root, PRED)), delimiter="\t"))
    frozen_text = show(root, rev, PRED)
    if frozen_text is None or frozen_text != open(os.path.join(root, PRED)).read():
        print("PIN predictions file differs from %s" % rev)
        return 2
    pkg_ver = json.load(open(PKG_JSON))["version"]
    pkg_sha = sha(open(PKG_JSON, "rb").read())
    if pkg_ver != "6.5.0":
        print("PIN package version")
        return 2
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", ".ufo/waves/round-30/claims.json")
    t = [int(x) for x in p.stdout.split()]
    freeze_ct = min(t) if t else None
    env_dir = os.path.join(root, "corpus/evidence/round-30/c2/envelopes")
    matches = 0
    runs = []
    for pr in preds:
        data = open(pr["path"], "rb").read()
        try:
            sec, doc = oracle.read_file(pr["path"])
            reading = (sec, oracle.normalize(doc))
        except Exception:
            reading = None
        start = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        argv = REA + ["inspect-rust-binary", pr["path"], "--format", "json", "--full-output"]
        r = subprocess.run(argv, capture_output=True, timeout=300, cwd="/tmp")
        end = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        out_t = r.stdout.decode("utf-8", "replace")
        err_t = r.stderr.decode("utf-8", "replace")
        try:
            env = json.loads(out_t)
        except ValueError:
            env = None
        verdict, why = judge(pr, env, out_t, err_t, r.returncode, sha(data), reading)
        if verdict == MATCH and not write_evidence:
            rel = "corpus/evidence/round-30/c2/envelopes/%s.json" % pr["id"]
            try:
                committed = json.loads(show(root, rev, rel) or "null")
            except ValueError:
                committed = None
            ok, w2 = committed_agrees(committed, env, first_add(root, rev, rel), freeze_ct)
            if not ok:
                verdict, why = MISS, w2
        matches += verdict == MATCH
        print("%s\t%s\t%s\t%s" % (pr["id"], pr["kind"], verdict, why))
        runs.append((pr["id"], start, end, r.returncode, " ".join(argv), pkg_ver, pkg_sha, verdict, why))
        if write_evidence:
            os.makedirs(env_dir, exist_ok=True)
            open(os.path.join(env_dir, pr["id"] + ".json"), "wb").write(r.stdout)
            open(os.path.join(env_dir, pr["id"] + ".stderr"), "wb").write(r.stderr)
    if write_evidence:
        with open(os.path.join(root, "corpus/evidence/round-30/c2/runs.tsv"), "w") as f:
            f.write("id\tutc_start\tutc_end\texit\targv\tpkg_version\tpkg_json_sha256\tverdict\treason\n")
            for row in runs:
                f.write("\t".join(str(x) for x in row) + "\n")
    e_ok, e_why = entry_ok(root, rev)
    s_ok, s_why = skill_ok(root, rev)
    print("mutants=%d matches=%d target=%d entry_ok=%d (%s) skill_ok=%d (%s)" % (
        len(preds), matches, TARGET, e_ok, e_why, s_ok, s_why))
    return 0 if matches == TARGET and len(preds) == TARGET and e_ok and s_ok else 1


def selftest():
    fails = 0
    sec = {"offset": 10, "size": 5}
    tup = [("a", "1", "s", None, True, ())]
    good = {"ok": True, "data": {"operation": "inspect_rust_binary", "subject": {"digest": {"sha256": "h"}},
            "normalized_result": {"auditable_metadata": {"packages": [{"name": "a", "version": "1", "source": "s", "root": True}],
                                                          "file_offset": 10, "compressed_bytes": 5}}}}
    refusal = {"ok": False, "error": {"message": "Dependency section is empty"}}
    R = {"kind": "refuse", "message": "Dependency section is empty"}
    A = {"kind": "ok", "message": ""}
    cases = [
        ("green-refusal-matches", R, refusal, json.dumps(refusal), "", 1, (sec, tup), MATCH),
        ("green-acceptance-matches", A, good, "", "", 0, (sec, tup), MATCH),
        ("red-do-nothing", R, None, "", "", 0, None, MISS),
        ("red-accepted-when-refusal-predicted", R, good, json.dumps(good), "", 0, (sec, tup), MISS),
        ("red-other-message", R, {"ok": False, "error": {"message": "Dependency section JSON is invalid"}},
         '{"ok":false,"error":{"message":"Dependency section JSON is invalid"}}', "", 1, None, MISS),
        ("red-empty-predicted-message", {"kind": "refuse", "message": ""}, refusal, json.dumps(refusal), "", 1, None, MISS),
        ("red-refused-when-acceptance-predicted", A, refusal, json.dumps(refusal), "", 1, (sec, tup), MISS),
        ("red-accept-wrong-packages", A, good, "", "", 0, (sec, [("b", "1", "s", None, True, ())]), MISS),
        ("red-accept-wrong-offset", A, good, "", "", 0, ({"offset": 11, "size": 5}, tup), MISS),
        ("red-accept-wrong-subject", A, good, "", "", 0, (sec, tup), MISS),
    ]
    for name, pred, env, out_t, err_t, code, reading, want in cases:
        msha = "x" if name == "red-accept-wrong-subject" else "h"
        got, why = judge(pred, env, out_t, err_t, code, msha, reading)
        ok = got == want
        fails += not ok
        print("%s %s got=%s (%s)" % ("ok" if ok else "FAIL", name, got, why))
    live = dict(good, data=dict(good["data"], evidence_id="ev_1"))
    other = dict(good, data=dict(good["data"], evidence_id="ev_2"))
    cc = [
        ("green-committed-agrees", live, live, 200, 100, True),
        ("green-committed-refusal-agrees", refusal, refusal, 200, 100, True),
        ("red-committed-absent", None, live, None, 100, False),
        ("red-committed-before-freeze", live, live, 100, 100, False),
        ("red-committed-ok-differs", refusal, live, 200, 100, False),
        ("red-committed-id-differs", other, live, 200, 100, False),
    ]
    for name, c, l, added, frz, want in cc:
        got, why = committed_agrees(c, l, added, frz)
        ok = got == want
        fails += not ok
        print("%s %s got=%s (%s)" % ("ok" if ok else "FAIL", name, got, why))
    # builder determinism on a synthetic ELF is covered by --build pin check against the frozen sha256
    print("selftest cases=%d failures=%d" % (len(cases) + len(cc), fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--rev", default="main")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--write-evidence", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.root:
        ap.error("--root required")
    if a.build:
        sys.exit(do_build(a.root))
    sys.exit(measure(a.root, a.rev, a.write_evidence))


if __name__ == "__main__":
    main()
