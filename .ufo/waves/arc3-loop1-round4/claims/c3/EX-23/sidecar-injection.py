#!/usr/bin/env python3
"""EX-23 after-state probe: the sidecar-scope injection (C3 residual (a)).

The residual (r3 c2 verdict item 3 / CR-4 item 1): the write guard examines
`--out` only, while the derived sidecar path `out.name + ".sha256"` is written
unguarded.  Two spellings of the same defect:

  variant A  `--out X --paths X.sha256`  -> the sidecar IS the measured file
  variant B  `--out X.sha256 --paths X`  -> the sidecar is the measured file's
                                            neighbour (a file derived from it)

This driver runs the same probes against any revision of the tool and prints a
stable, diffable report: exit code, the refusal line, and the byte/inode/mtime
state of every fixture before and after.  Run it on the frozen base revision for
the before-state, then on the landed revision for the after-state; the declared
class is whatever the landed revision's own declaration says, checked against
what this probe measures.

usage: python3 sidecar-injection.py <path/to/custody-pair.py> <scratch-root> <label>
"""

import hashlib
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
ROOT = Path(sys.argv[2]).resolve()
LABEL = sys.argv[3] if len(sys.argv) > 3 else "run"


def sha256(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError as exc:
        return "ERR:%s" % type(exc).__name__


def state(p: Path) -> str:
    try:
        st = p.stat()
    except OSError:
        return "ABSENT"
    return "sha=%s ino=%d mtime_ns=%d" % (sha256(p)[:16], st.st_ino, st.st_mtime_ns)


def run(argv, cwd):
    proc = subprocess.run([sys.executable, str(TOOL)] + argv, cwd=str(cwd),
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def probe(name, fixtures, out, paths, expect_receipt):
    """fixtures: {relpath: bytes}.  out/paths: strings relative to the sandbox."""
    box = ROOT / LABEL / name
    shutil.rmtree(box, ignore_errors=True)
    box.mkdir(parents=True)
    for rel, blob in fixtures.items():
        (box / rel).write_bytes(blob)
    watched = sorted(set(list(fixtures) + [out, out + ".sha256", paths,
                                           paths + ".sha256"]))
    before = {w: state(box / w) for w in watched}

    argv = ["capture", "--out", out, "--paths", paths, "--label", "ex23-" + name]
    rc, so, se = run(argv, box)

    after = {w: state(box / w) for w in watched}
    touched = [w for w in watched if before[w] != after[w]]
    # landed = created or changed by THIS run (a pre-existing --out is not a landing)
    receipt_landed = before[out] != after[out]
    sidecar_landed = before[out + ".sha256"] != after[out + ".sha256"]

    print("=" * 78)
    print("PROBE %s  label=%s" % (name, LABEL))
    print("  tool-sha256=%s" % sha256(TOOL))
    print("  argv: capture --out %s --paths %s" % (out, paths))
    print("  exit=%d" % rc)
    for stream, text in (("stdout", so), ("stderr", se)):
        for line in text.strip().splitlines():
            print("  %s| %s" % (stream, line))
    print("  fixture watch (before -> after):")
    for w in watched:
        mark = "TOUCHED" if before[w] != after[w] else "untouched"
        print("    %-28s %-14s %s" % (w, mark, before[w]))
        if before[w] != after[w]:
            print("    %-28s %-14s %s" % ("", "  after", after[w]))
    print("  receipt-landed=%s sidecar-landed=%s expected-receipt=%s"
          % (receipt_landed, sidecar_landed, expect_receipt))
    print("  TOUCHED-FILES: %s" % (", ".join(touched) if touched else "(none)"))
    return {"exit": rc, "touched": touched, "receipt": receipt_landed,
            "sidecar": sidecar_landed, "stderr": se.strip()}


def control(name):
    """The fix must not break the legitimate write path."""
    box = ROOT / LABEL / name
    shutil.rmtree(box, ignore_errors=True)
    box.mkdir(parents=True)
    (box / "vic.sha256").write_bytes(b"measured fixture bytes\n")
    rc, so, se = run(["capture", "--out", "fresh.txt", "--paths", "vic.sha256",
                      "--label", "ex23-control"], box)
    sidecar = box / "fresh.txt.sha256"
    pinned = None
    if sidecar.is_file():
        recorded = sidecar.read_text().split()[0]
        pinned = (recorded == sha256(box / "fresh.txt"))
    print("=" * 78)
    print("CONTROL %s (legitimate fresh --out beside a measured .sha256 file)" % name)
    print("  tool-sha256=%s" % sha256(TOOL))
    print("  exit=%d" % rc)
    for stream, text in (("stdout", so), ("stderr", se)):
        for line in text.strip().splitlines():
            print("  %s| %s" % (stream, line))
    print("  receipt-landed=%s sidecar-landed=%s sidecar-pins-receipt=%s"
          % ((box / "fresh.txt").is_file(), sidecar.is_file(), pinned))
    if (box / "fresh.txt").is_file():
        vrc, vso, vse = run(["verify", "fresh.txt", "--live", "--require-paths", "1"], box)
        line = [l for l in vso.splitlines() if l.startswith("CUSTODY_PAIR_VERIFY")]
        print("  verify --live --require-paths 1: exit=%d %s" % (vrc, line[0] if line else "(no verdict line)"))
    return {"exit": rc, "receipt": (box / "fresh.txt").is_file(),
            "sidecar": sidecar.is_file(), "pins": pinned}


def consequence(name):
    """Why the residual matters: measure the injection through the tool's own
    verify.  Capture a legitimate receipt of the measured file, run the
    injection, then ask verify whether the measured file still matches its
    receipt.  Base revision: the sidecar overwrote it -> CONTENT-DRIFT."""
    box = ROOT / LABEL / name
    shutil.rmtree(box, ignore_errors=True)
    box.mkdir(parents=True)
    (box / "vic.sha256").write_bytes(b"measured bytes, will be overwritten by a sidecar\n")
    rc0, so0, _ = run(["capture", "--out", "pre.txt", "--paths", "vic.sha256",
                       "--label", "ex23-pre"], box)
    pre_digest = sha256(box / "vic.sha256")
    rc1, so1, se1 = run(["capture", "--out", "vic", "--paths", "vic.sha256",
                         "--label", "ex23-consequence"], box)
    rc2, so2, se2 = run(["verify", "pre.txt", "--live", "--require-paths", "1"], box)
    verdict = [l for l in so2.splitlines() if l.startswith("CUSTODY_PAIR_VERIFY")]
    print("=" * 78)
    print("CONSEQUENCE %s (injection observed through the tool's own verify)" % name)
    print("  tool-sha256=%s" % sha256(TOOL))
    print("  step1 capture pre-receipt of vic.sha256: exit=%d" % rc0)
    print("  step2 injection capture --out vic --paths vic.sha256: exit=%d" % rc1)
    for line in (so1 + se1).strip().splitlines():
        print("  step2| %s" % line)
    print("  step3 verify pre.txt --live --require-paths 1: exit=%d" % rc2)
    for line in (so2 + se2).strip().splitlines():
        if line.startswith(("PATH", "CUSTODY_PAIR_VERIFY", "SHA256-CONTRACT", "USAGE")):
            print("  step3| %s" % line)
    print("  measured-file digest: before=%s after=%s"
          % (pre_digest[:16], sha256(box / "vic.sha256")[:16]))
    print("  VERDICT-CLASS: %s" % (verdict[0] if verdict else "(no verdict line)"))
    return {"injection_exit": rc1, "verify_exit": rc2,
            "verdict": verdict[0] if verdict else None,
            "digest_held": pre_digest == sha256(box / "vic.sha256")}


def hardlink_probe(name):
    """Third spelling (EX-27's g1b): `--out` is FRESH (so the out-only guard cannot
    fire), while the derived sidecar path is a hardlink of the measured file — the
    sidecar write reaches the measured inode without ever naming it."""
    box = ROOT / LABEL / name
    shutil.rmtree(box, ignore_errors=True)
    box.mkdir(parents=True)
    measured = box / "measured.sha256"
    payload = b"measured-through-sidecar-alias\n"
    measured.write_bytes(payload)
    out = box / "out.txt"
    out.write_bytes(b"fresh out\n")
    os.link(measured, box / "out.txt.sha256")
    before = state(measured)
    rc, so, se = run(["capture", "--out", "out.txt", "--paths", "measured.sha256",
                      "--label", "ex23-hardlink"], box)
    after = state(measured)
    clobbered = before != after
    print("=" * 78)
    print("PROBE %s  label=%s" % (name, LABEL))
    print("  tool-sha256=%s" % sha256(TOOL))
    print("  argv: capture --out out.txt --paths measured.sha256   (out.txt.sha256 is a hardlink of measured.sha256)")
    print("  exit=%d" % rc)
    for stream, text in (("stdout", so), ("stderr", se)):
        for line in text.strip().splitlines():
            print("  %s| %s" % (stream, line))
    print("  measured inode: before=%s" % before)
    if clobbered:
        print("  measured inode: after =%s  CLOBBERED" % after)
    else:
        print("  measured inode: unchanged")
    print("  CLOSED=%s (rc==2 and not clobbered)" % (rc == 2 and not clobbered))
    return {"exit": rc, "clobbered": clobbered, "closed": rc == 2 and not clobbered}


def main():
    print("EX-23 sidecar-scope after-state probe")
    print("tool=%s" % TOOL)
    print("scratch-root=%s label=%s" % (ROOT, LABEL))
    print("utc=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    a = probe("A-sidecar-lands-on-measured-file",
              {"vic.sha256": b"measured file whose name is X.sha256\n",
               "vic": b"receipt target\n"},
              out="vic", paths="vic.sha256", expect_receipt=False)
    b = probe("B-sidecar-lands-on-neighbour-of-measured",
              {"vic": b"measured file X\n"},
              out="vic.sha256", paths="vic", expect_receipt=False)
    # B2 is the residual's literal wording: the neighbour ALREADY exists, so the
    # clobber is an overwrite of a bystander file rather than a fresh create.
    b2 = probe("B2-sidecar-overwrites-existing-neighbour",
               {"vic": b"measured file X\n",
                "vic.sha256": b"bystander neighbour bytes\n"},
               out="vic.sha256", paths="vic", expect_receipt=False)
    c = control("C-legitimate-write-still-works")
    d = consequence("D-injection-observed-by-tool-verify")
    e = hardlink_probe("E-sidecar-hardlink-of-measured-inode")

    print("=" * 78)
    print("SUMMARY label=%s tool-sha256=%s" % (LABEL, sha256(TOOL)))
    print("  A: exit=%d touched=%s" % (a["exit"], a["touched"]))
    print("  B: exit=%d touched=%s" % (b["exit"], b["touched"]))
    print("  B2: exit=%d touched=%s" % (b2["exit"], b2["touched"]))
    print("  C: exit=%d receipt=%s sidecar=%s pins=%s"
          % (c["exit"], c["receipt"], c["sidecar"], c["pins"]))
    print("  D: injection-exit=%d verify-exit=%d digest-held=%s class=%s"
          % (d["injection_exit"], d["verify_exit"], d["digest_held"], d["verdict"]))
    print("  E: exit=%d clobbered=%s closed=%s" % (e["exit"], e["clobbered"], e["closed"]))


if __name__ == "__main__":
    main()
