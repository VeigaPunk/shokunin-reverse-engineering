#!/usr/bin/env python3
"""pins-attack.py — wave-2 falsification harness for W/tools/pins.py.

Exercises the assigned attack surface (empty path list, self-compare, swapped
pre/post, missing-then-present, unreadable file, symlink swap, same-size
different content) plus calibration probes beyond the w1 selftest: fifo /
char-device hangs, forged-empty snapshot files, relative-path key
normalization vs carrier-run lookup, deep-JSON exit-code violation.

Never executes a carrier binary; never invokes REA or Ghidra. All fixtures
live under tempfile.mkdtemp(). Every subprocess is `python -I -B pins.py`
with a bounded timeout. Always exits 0; findings are printed and returned.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

TOOLS = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools"
PINS = os.path.join(TOOLS, "pins.py")
RETAIN = os.path.join(TOOLS, "retain.py")

FINDINGS = []


def run_cli(argv, timeout=30):
    """Run `python -I -B <tool> argv...`; return (rc, stdout, stderr, hung)."""
    try:
        p = subprocess.run(
            [sys.executable, "-I", "-B", *argv],
            capture_output=True, text=True, timeout=timeout, check=False)
        return p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired:
        return None, "", f"hung>{timeout}s", True


def record(label, severity, expected, observed, anchor, note=""):
    FINDINGS.append({
        "label": label, "severity": severity, "expected": expected,
        "observed": observed, "anchor": anchor, "note": note})
    print(f"[FINDING {severity}] {label}\n  expected: {expected}\n"
          f"  observed: {observed}\n  anchor: {anchor}\n  note: {note}")


def observe(label, detail):
    print(f"[ok] {label}: {detail}")


def jload(text):
    try:
        return json.loads(text)
    except Exception:
        return None


def write_snap(path, entries):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"taken_at_utc": "2026-10-20T00:00:00.000000+00:00",
                   "monotonic_ns": 1, "entries": entries}, fh)


def main():
    root = os.path.realpath(tempfile.mkdtemp(prefix="pins-attack-", dir="/tmp"))
    f_a = os.path.join(root, "a.bin")
    f_b = os.path.join(root, "b.bin")
    with open(f_a, "wb") as fh:
        fh.write(b"payload-a")
    with open(f_b, "wb") as fh:
        fh.write(b"payload-b")
    snap_dir = os.path.join(root, "snaps")
    os.mkdir(snap_dir)

    def snap(out, *paths):
        return run_cli([PINS, "snapshot", "--out", out, *paths])

    # ---- assigned case: empty path list ------------------------------------
    rc, out, err, _ = run_cli([PINS, "snapshot", "--out",
                               os.path.join(snap_dir, "e.json")])
    if rc == 2 and "required" in err:
        observe("empty-cli", "CLI refuses bare snapshot (nargs='+'), exit 2")
    else:
        record("empty-cli", "info", "exit 2 required-arg",
               f"rc={rc} err={err.strip()[:120]}", "pins.py:287")
    # Forged empty snapshots through the compare CLI: vacuous equal.
    e1 = os.path.join(snap_dir, "e1.json")
    e2 = os.path.join(snap_dir, "e2.json")
    write_snap(e1, {})
    write_snap(e2, {})
    rc, out, _, _ = run_cli([PINS, "compare", e1, e2])
    doc = jload(out) or {}
    if rc == 0 and doc.get("equal") is True:
        observe("empty-vacuous",
                "two empty-entry snapshots compare equal:true exit 0 "
                "(vacuous truth: nothing was ever hashed)")
        # Consumer impact: retain.py with zero --pin flags.
        rdir = os.path.join(root, "retain")
        rc2, out2, _, _ = run_cli([RETAIN, "--out",
                                   os.path.join(rdir, "r.json"), "--",
                                   sys.executable, "-c", "print(1)"])
        emit = jload(out2) or {}
        if rc2 == 0 and emit.get("pins_equal") is True:
            rec = jload(open(os.path.join(rdir, "r.json")).read()) or {}
            n = len((rec.get("pins_pre") or {}).get("entries") or {})
            record("empty-vacuous-retain", "minor",
                   "a run that pins nothing should not be indistinguishable "
                   "from a clean pinned run",
                   f"retain exit 0, pins_equal=true, pinned_paths={n}",
                   "pins.py:62-72 + retain.py:102,124,151-154",
                   "no --pin flags: snapshot([]) -> entries {} -> equal "
                   "-> green receipt proving nothing")
    else:
        record("empty-vacuous", "major", "equal must be false or exit!=0 "
               "for vacuous comparisons",
               f"rc={rc} out={out[:200]}", "pins.py:75-106")

    # ---- assigned case: identical snapshot compared to itself --------------
    s1 = os.path.join(snap_dir, "s1.json")
    rc, _, _, _ = snap(s1, f_a, f_b)
    rc, out, _, _ = run_cli([PINS, "compare", s1, s1])
    doc = jload(out) or {}
    if rc == 0 and doc.get("equal") is True:
        observe("self-compare", "clean snapshot vs itself: equal exit 0")
    else:
        record("self-compare", "major", "self-compare equal exit 0",
               f"rc={rc} out={out[:200]}", "pins.py:82-98")
    # Self-compare of a snapshot containing an error entry must stay red.
    ghost = os.path.join(root, "never-existed")
    se = os.path.join(snap_dir, "se.json")
    snap(se, ghost)
    rc, out, _, _ = run_cli([PINS, "compare", se, se])
    doc = jload(out) or {}
    if rc == 1 and doc.get("equal") is False and ghost in doc.get("errors", []):
        observe("self-compare-error",
                "error-entry snapshot vs itself: not equal (good, "
                "errors never prove same-bytes)")
    else:
        record("self-compare-error", "major",
               "error entry vs itself must not be equal",
               f"rc={rc} out={out[:200]}", "pins.py:87-95")

    # ---- assigned case: swapped pre/post order ------------------------------
    # Pair (a) two identical-content snapshots in both orders.
    s2 = os.path.join(snap_dir, "s2.json")
    snap(s2, f_a, f_b)
    for order in [(s1, s2), (s2, s1)]:
        rc, out, _, _ = run_cli([PINS, "compare", *order])
        doc = jload(out) or {}
        if not (rc == 0 and doc.get("equal") is True):
            record("swap-equal", "major", "equal in both orders",
                   f"{order}: rc={rc}", "pins.py:82-98")
    # Pair (b) asymmetric pair pre={a}, post={a,b}: file created in interval.
    pa = os.path.join(snap_dir, "pa.json")
    pab = os.path.join(snap_dir, "pab.json")
    snap(pa, f_a)
    snap(pab, f_a, f_b)
    for order in [(pa, pab), (pab, pa)]:
        rc, out, _, _ = run_cli([PINS, "compare", *order])
        doc = jload(out) or {}
        if not (rc == 1 and doc.get("equal") is False
                and f_b in doc.get("missing", [])):
            record("swap-asym", "major",
                   "asymmetric pair red in both orders",
                   f"{order}: rc={rc} doc={json.dumps(doc)[:200]}",
                   "pins.py:82-98")
    observe("swap",
            "equal/red outcomes symmetric under pre/post swap; "
            "equal is symmetric by construction (pins.py:82-98)")

    # ---- assigned case: missing-then-present --------------------------------
    pre_ghost = os.path.join(snap_dir, "pre-ghost.json")
    snap(pre_ghost, ghost)
    created = os.path.join(root, "created.bin")
    with open(created, "wb") as fh:
        fh.write(b"new")
    post_ghost = os.path.join(snap_dir, "post-ghost.json")
    snap(post_ghost, created)
    # Proper missing-then-present on ONE path: delete after pre, recreate.
    tgt = os.path.join(root, "flap.bin")
    with open(tgt, "wb") as fh:
        fh.write(b"flap")
    fpre = os.path.join(snap_dir, "fpre.json")
    snap(fpre, tgt)
    os.unlink(tgt)
    fmid = os.path.join(snap_dir, "fmid.json")
    snap(fmid, tgt)
    with open(tgt, "wb") as fh:
        fh.write(b"flap")
    fpost = os.path.join(snap_dir, "fpost.json")
    snap(fpost, tgt)
    rc, out, _, _ = run_cli([PINS, "compare", fpre, fmid])
    doc = jload(out) or {}
    if rc == 1 and tgt in doc.get("missing", []):
        observe("missing-then-deleted", "vanished file -> missing, exit 1")
    else:
        record("missing-then-deleted", "major",
               "deleted path in missing, exit 1",
               f"rc={rc} doc={json.dumps(doc)[:200]}", "pins.py:91-93")
    rc, out, _, _ = run_cli([PINS, "compare", fmid, fpost])
    doc = jload(out) or {}
    if rc == 1 and tgt in doc.get("missing", []):
        record("created-as-missing", "minor",
               "a file created in the interval should be named 'changed' "
               "or a dedicated 'added' list, not 'missing'",
               f"exit 1, {tgt} reported in missing",
               "pins.py:82-95",
               "set-difference only: presence asymmetry maps to 'missing' "
               "regardless of direction; 'missing' also covers created")
    else:
        record("created-as-missing", "major",
               "created path not equal",
               f"rc={rc} doc={json.dumps(doc)[:200]}", "pins.py:82-95")
    # modify+restore: identical bytes restored -> equal (documented limit)
    rc, out, _, _ = run_cli([PINS, "compare", fpre, fpost])
    doc = jload(out) or {}
    if rc == 0 and doc.get("equal") is True:
        observe("modify-restore",
                "deleted+recreated same bytes: equal (documented endpoint "
                "limit, --help epilog pins.py:280-282)")
    else:
        record("modify-restore", "info",
               "endpoint limit", f"rc={rc}", "pins.py:280-282")

    # ---- assigned case: unreadable file (chmod 000) -------------------------
    locked = os.path.join(root, "locked.bin")
    with open(locked, "wb") as fh:
        fh.write(b"locked")
    os.chmod(locked, 0)
    lpre = os.path.join(snap_dir, "lpre.json")
    lpost = os.path.join(snap_dir, "lpost.json")
    rc, out, _, _ = snap(lpre, locked)
    ent = (jload(out) or {}).get("entries", {}).get(locked, {})
    rc, out, _, _ = snap(lpost, locked)
    rc, out, _, _ = run_cli([PINS, "compare", lpre, lpost])
    doc = jload(out) or {}
    if rc == 1 and doc.get("equal") is False and locked in doc.get("errors", []):
        observe("chmod-000",
                "unreadable file pins as error entry; identical error pair "
                "still not equal, exit 1")
    else:
        record("chmod-000", "major",
               "permission pair must be errors + not equal",
               f"rc={rc} entry={json.dumps(ent)[:150]} "
               f"doc={json.dumps(doc)[:200]}", "pins.py:49,87-95")
    os.chmod(locked, 0o644)
    # unreadable vs FileNotFoundError on the same path -> errors (not missing)
    lmix = os.path.join(snap_dir, "lmix.json")
    snap(lmix, ghost)  # ghost: FileNotFoundError entry
    # reuse lpre (PermissionError-ish entry? locked now readable -> real entry)
    # proper mix: snapshot locked while unreadable already done above is gone;
    # recreate chmod 000 snapshot quickly.
    os.chmod(locked, 0)
    lerr = os.path.join(snap_dir, "lerr.json")
    snap(lerr, locked)
    os.chmod(locked, 0o644)
    lgood = os.path.join(snap_dir, "lgood.json")
    snap(lgood, locked)
    rc, out, _, _ = run_cli([PINS, "compare", lerr, lgood])
    doc = jload(out) or {}
    if rc == 1 and doc.get("equal") is False:
        if locked in doc.get("missing", []):
            observe("unreadable-vs-present",
                    "PermissionError opposite real entry -> missing "
                    "(FileNotFoundError-startswith test only treats FNF "
                    "as missing; PermissionError would land in errors)")
        elif locked in doc.get("errors", []):
            observe("unreadable-vs-present",
                    "PermissionError opposite real entry -> errors, exit 1")
    else:
        record("unreadable-vs-present", "major",
               "unreadable-vs-present must not be equal",
               f"rc={rc} doc={json.dumps(doc)[:200]}", "pins.py:87-95")

    # ---- assigned case: symlink swapped between snapshots --------------------
    real1 = os.path.join(root, "real1.bin")
    real2 = os.path.join(root, "real2.bin")
    link = os.path.join(root, "link.bin")
    with open(real1, "wb") as fh:
        fh.write(b"same-content")
    with open(real2, "wb") as fh:
        fh.write(b"same-content")  # identical bytes, different path
    os.symlink(real1, link)
    ypre = os.path.join(snap_dir, "ypre.json")
    rc, out, _, _ = snap(ypre, link)
    pre_keys = list((jload(out) or {}).get("entries", {}))
    os.unlink(link)
    os.symlink(real2, link)
    ypost = os.path.join(snap_dir, "ypost.json")
    snap(ypost, link)
    rc, out, _, _ = run_cli([PINS, "compare", ypre, ypost])
    doc = jload(out) or {}
    if rc == 1 and doc.get("equal") is False:
        named = doc.get("missing", []) + doc.get("changed", [])
        if link in named:
            observe("symlink-swap", "retargeted symlink names the link")
        else:
            record("symlink-swap-misname", "minor",
                   "retargeted symlink should name the pinned operand "
                   "(or 'changed'), not two 'missing' targets",
                   f"missing={doc.get('missing')} — names {real1}/{real2}, "
                   f"never the pinned path {link}",
                   "pins.py:66-67,82-95",
                   "realpath keys: user-pinned spelling vanished from the "
                   "diff; even identical bytes at both ends force 'missing'")
    else:
        record("symlink-swap", "major",
               "retargeted symlink must not compare equal",
               f"rc={rc} doc={json.dumps(doc)[:200]}", "pins.py:66-67")

    # ---- assigned case: same size different content --------------------------
    # Correct construction: ONE path, same-length bytes mutated in place.
    sc = os.path.join(root, "sc.bin")
    with open(sc, "wb") as fh:
        fh.write(b"A" * 4096)
    ssc1 = os.path.join(snap_dir, "ssc1.json")
    ssc2 = os.path.join(snap_dir, "ssc2.json")
    snap(ssc1, sc)
    with open(sc, "wb") as fh:
        fh.write(b"B" * 4096)   # identical size, identical length, diff bytes
    snap(ssc2, sc)
    rc, out, _, _ = run_cli([PINS, "compare", ssc1, ssc2])
    doc = jload(out) or {}
    if rc == 1 and sc in doc.get("changed", []) and not doc.get("missing"):
        observe("same-size-diff",
                "same-length in-place mutation -> changed, exit 1 "
                "(sha256 decides, not size alone)")
    else:
        record("same-size-diff", "major",
               "same-size different-content path in changed, exit 1",
               f"rc={rc} doc={json.dumps(doc)[:200]}", "pins.py:96-97")

    # ---- extra: char device pinned equal to a real empty file -----------------
    empty = os.path.join(root, "empty.bin")
    open(empty, "wb").close()
    snull = os.path.join(snap_dir, "snull.json")
    sempty = os.path.join(snap_dir, "sempty.json")
    snap(snull, "/dev/null")
    snap(sempty, empty)
    # compare across DIFFERENT paths is 'missing' by key; the equal-true hole
    # is SAME path replaced: file -> /dev/null-like device cannot be made in
    # tmp, but a real file replaced by a fifo-like empty-EOF object would
    # equal. Demonstrate with a real file truncated vs device digest instead:
    ent_null = (jload(open(snull).read()) or {}).get("entries", {}) \
        .get("/dev/null", {})
    ent_empty = (jload(open(sempty).read()) or {}).get("entries", {}) \
        .get(empty, {})
    if ent_null.get("sha256") == ent_empty.get("sha256"):
        record("devnull-empty-equal", "minor",
               "a device pin should not be byte-identical to an empty "
               "regular-file pin",
               f"both sha256={ent_null.get('sha256','')[:16]}… size=0: "
               "file type is invisible to compare() — a regular file "
               "replaced by a character device with EOF-at-open would "
               "compare equal:true",
               "pins.py:40-58,96-97",
               "no file-type field in the entry; st.st_mode recorded "
               "nowhere")
    if pre_keys == [real1]:
        observe("symlink-realpath-key",
                f"entry keyed by target {real1}, not operand {link}")
    # chain swap: link -> link2 -> real1 (same terminal target)
    link2 = os.path.join(root, "link2.bin")
    os.unlink(link)
    os.symlink(link2, link)
    os.symlink(real1, link2)
    ypost2 = os.path.join(snap_dir, "ypost2.json")
    snap(ypost2, link)
    rc, out, _, _ = run_cli([PINS, "compare", ypre, ypost2])
    doc = jload(out) or {}
    if rc == 0 and doc.get("equal") is True:
        observe("symlink-chain-swap",
                "retargeted via extra hop resolving to same file: equal — "
                "pins the resolved bytes, not the link object")
    # realpath dedupe: one operand + its symlinked spelling collapse to 1 key
    dd = os.path.join(snap_dir, "dd.json")
    rc, out, _, _ = snap(dd, real1, link2)
    ents = (jload(out) or {}).get("entries", {})
    if len(ents) == 1:
        record("realpath-dedupe", "minor",
               "two requested operands should yield two keys or a warning",
               f"pinned 2 paths ({real1}, {link2}) -> 1 entry {list(ents)}",
               "pins.py:64-67",
               "silent dedupe: pin count silently < requested count")
    else:
        observe("realpath-dedupe", f"dedupe preserved {len(ents)} keys")

    # ---- extra: fifo / char-device hang --------------------------------------
    fifo = os.path.join(root, "pipe")
    os.mkfifo(fifo)
    rc, out, err, hung = run_cli(
        [PINS, "snapshot", "--out", os.path.join(snap_dir, "fifo.json"), fifo],
        timeout=10)
    if hung:
        record("fifo-hang", "major",
               "snapshot of a fifo must return an error entry, not block",
               f"open('{fifo}','rb') blocks >10s awaiting a writer; "
               "process killed by timeout",
               "pins.py:40,45",
               "os.stat succeeds on a fifo, then open() blocks forever: "
               "no S_ISREG/fstat-type check; retain.py pins_pre would hang "
               "the whole run with no timeout on the pin step")
    else:
        observe("fifo", f"rc={rc} out={out[:160]}")
    rc, out, err, hung = run_cli(
        [PINS, "snapshot", "--out",
         os.path.join(snap_dir, "zero.json"), "/dev/zero"],
        timeout=10)
    if hung:
        record("devzero-hang", "major",
               "snapshot of an infinite char device must bound or refuse",
               "read() of /dev/zero never returns b''; hashing loops "
               ">10s unbounded",
               "pins.py:44-47",
               "iter(lambda: fh.read(_CHUNK), b'') terminates only on EOF; "
               "special files never EOF")
    else:
        observe("devzero", f"rc={rc} out={out[:160]}")
    # /dev/null: EOF instantly -> pins a device as if it were an empty file
    rc, out, _, _ = run_cli(
        [PINS, "snapshot", "--out",
         os.path.join(snap_dir, "null.json"), "/dev/null"])
    ent = (jload(out) or {}).get("entries", {}).get("/dev/null", {})
    if "sha256" in ent:
        record("devnull-pinned", "info",
               "non-regular files should be refused or flagged",
               f"/dev/null pinned as sha256={ent['sha256'][:16]}… size=0 "
               "— the empty-file digest, indistinguishable from an empty "
               "regular file", "pins.py:40-58")
    # directory operand
    rc, out, _, _ = run_cli(
        [PINS, "snapshot", "--out", os.path.join(snap_dir, "dir.json"), root])
    ent = (jload(out) or {}).get("entries", {}).get(root, {})
    if "error" in ent:
        observe("dir-operand", f"directory -> error entry ({ent['error'][:60]})")
    else:
        record("dir-operand", "minor", "directory should error",
               f"entry={json.dumps(ent)[:150]}", "pins.py:45")

    # ---- extra: relative-path key vs carrier-run lookup -----------------------
    rel_out = os.path.join(snap_dir, "rel.json")
    rc, out, _, _ = run_cli(
        [PINS, "snapshot", "--out", rel_out, "a.bin"], timeout=30)
    # that ran in CWD; instead demonstrate key form directly:
    with open(rel_out) as fh:
        rel_doc = json.load(fh)
    keys = list(rel_doc.get("entries", {}))
    observe("cli-cwd", f"bare-name operand from CWD keyed as {keys}")

    # ---- extra: malformed snapshot exit codes --------------------------------
    deep = os.path.join(snap_dir, "deep.json")
    with open(deep, "w") as fh:
        fh.write("[" * 200000 + "]" * 200000)
    rc, out, err, _ = run_cli([PINS, "compare", deep, s1])
    if rc == 2:
        observe("deep-json", "deeply nested JSON -> exit 2")
    else:
        record("deep-json-exit", "major",
               "invalid input must be exit 2 with JSON on stdout "
               "(contract: 2 could-not-evaluate)",
               f"rc={rc}; stdout has no JSON "
               f"({'traceback' if 'Traceback' in err else err.strip()[:80]})",
               "pins.py:144-150",
               "json.load raises RecursionError — outside the "
               "(OSError, ValueError) guard -> interpreter traceback, "
               "exit 1")
    # entries values must be dicts — verified validator accepts scalars? no:
    badval = os.path.join(snap_dir, "badval.json")
    with open(badval, "w") as fh:
        json.dump({"entries": {"/x": "not-a-dict"}}, fh)
    rc, out, _, _ = run_cli([PINS, "compare", badval, s1])
    if rc == 2:
        observe("bad-entry-value", "scalar entry rejected with exit 2")
    else:
        record("bad-entry-value", "minor", "exit 2",
               f"rc={rc} out={out[:160]}", "pins.py:137-140")

    print(f"\nATTACK: FINDINGS={len(FINDINGS)}")
    for f in FINDINGS:
        print(f"  - [{f['severity']}] {f['label']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
