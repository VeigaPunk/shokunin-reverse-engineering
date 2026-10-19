#!/usr/bin/env python3
"""EX-27 round-4 adversarial probes against the (a) sidecar-scope closure.

Purpose: try to DEFEAT the revised guard, not to confirm it. Every probe aims a
`capture --out` at a scratch path derived from a measured scratch file, in spellings
the round-3 patch texts did not enumerate. Nothing here touches a custody path: the
five canonical paths are read-only inputs to the tool's own default set, never
outputs; every fixture and every `--out` lives under the scratch root.

usage: adversarial-sidecar.py <tool> <scratch-root> <label>
"""
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
ROOT = Path(sys.argv[2]).resolve()
LABEL = sys.argv[3] if len(sys.argv) > 3 else "adv"
ROOT.mkdir(parents=True, exist_ok=True)
TOOL_SHA = hashlib.sha256(TOOL.read_bytes()).hexdigest()


def run(*args):
    r = subprocess.run([sys.executable, str(TOOL)] + [str(a) for a in args],
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else None


def fresh(name):
    d = ROOT / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    return d


results = []


def probe(name, fn, expect_closed, expect_clobber_free=True):
    """Record one probe.

    `expect_closed`  — True/False assert the guard's behaviour; None records the
                        probe as observed-only (a named residual, not a pass/fail).
    `expect_clobber_free` — should the measured file survive regardless of exit code?
    """
    d = fresh(name)
    rc, clobbered, note = fn(d)
    closed = (rc == 2 and not clobbered)
    if expect_closed is None:
        hold = None
    else:
        hold = (closed == expect_closed and (not clobbered or not expect_clobber_free))
    results.append({"probe": name, "exit": rc, "clobbered": clobbered, "closed": closed,
                    "expect_closed": expect_closed, "expect_clobber_free": expect_clobber_free,
                    "hold": hold, "note": note})


# P1: --out X --paths X.sha256 (the r3 direct clobber)
def p1(d):
    vic = d / "vic.sha256"; payload = b"victim\n"; vic.write_bytes(payload)
    rc, out = run("capture", "--out", d / "vic", "--paths", vic)
    return rc, vic.read_bytes() != payload, "direct: sidecar lands on the measured file"


# P2: --out X.sha256 --paths X (neighbour of the measured file)
def p2(d):
    vic = d / "vic"; payload = b"victim\n"; vic.write_bytes(payload)
    rc, out = run("capture", "--out", d / "vic.sha256", "--paths", vic)
    return rc, vic.read_bytes() != payload, "neighbour: --out is <measured>.sha256"


# P3: sidecar path is a hardlink alias of the measured file
def p3(d):
    m = d / "measured"; payload = b"measured\n"; m.write_bytes(payload)
    os.link(m, d / "fresh.txt.sha256")
    rc, out = run("capture", "--out", d / "fresh.txt", "--paths", m)
    return rc, m.read_bytes() != payload, "alias: sidecar path hardlinked to the measured file"


# P4: --out inside a symlinked directory whose target holds the measured file
def p4(d):
    real = d / "real"; real.mkdir()
    m = real / "vic.sha256"; payload = b"victim\n"; m.write_bytes(payload)
    link = d / "link"
    link.symlink_to(real)
    rc, out = run("capture", "--out", link / "vic", "--paths", m)
    return rc, m.read_bytes() != payload, "symlinked dir spelling of the same target"


# P5: measured path reached through a symlink; --out is its neighbour. The guard's
# neighbour arm is built from the SPELLED measured path, so this spelling evades the
# refusal — but the same run measures the alias, so the harm is a PRE-EXISTING
# neighbour file, which this probe creates. Classified as a persisting residual
# (same class measured on the r3 bytes), not as a new regression.
def p5(d):
    real = d / "real"; real.mkdir()
    m = real / "vic"; payload = b"victim\n"; m.write_bytes(payload)
    neighbour = real / "vic.sha256"
    precious = b"PRE-EXISTING NEIGHBOUR CONTENT\n"
    neighbour.write_bytes(precious)
    alias = d / "alias"
    alias.symlink_to(m)
    rc, out = run("capture", "--out", neighbour, "--paths", alias)
    return rc, neighbour.read_bytes() != precious, "symlink-alias measured path, neighbour --out"


# P6: relative spelling of the scoped file (the CR-4 half-fix trap)
def p6(d):
    m = d / "vic.sha256"; payload = b"victim\n"; m.write_bytes(payload)
    rc, out = run("capture", "--out", "vic", "--paths", "vic.sha256")  # cwd = d
    return rc, m.read_bytes() != payload, "relative --out/--paths in the fixture dir"


# P7: --out X.sha256.sha256 --paths X — a DOUBLE extension. No measured file is
# harmed by construction (the run's own measured path is X, and X.sha256 is a
# *neighbour* the tool never claims to protect at the second level); this probe
# records the boundary of the neighbour arm rather than asserting a refusal.
def p7(d):
    m = d / "vic"; payload = b"victim\n"; m.write_bytes(payload)
    neighbour = d / "vic.sha256"
    precious = b"PRE-EXISTING NEIGHBOUR CONTENT\n"
    neighbour.write_bytes(precious)
    rc, out = run("capture", "--out", d / "vic.sha256.sha256", "--paths", m)
    return rc, neighbour.read_bytes() != precious, "double-extension --out; first-level neighbour must survive"


# P8: control — ordinary fresh capture beside a measured .sha256 file
def p8(d):
    m = d / "vic.sha256"; payload = b"victim\n"; m.write_bytes(payload)
    rc, out = run("capture", "--out", d / "fresh-receipt.txt", "--paths", m)
    return rc, m.read_bytes() != payload, "control: legitimate capture must still work"


probe("P1-direct-sidecar", p1, True)
probe("P2-neighbour-sidecar", p2, True)
probe("P3-hardlink-alias-sidecar", p3, True)
probe("P4-symlinked-dir-spelling", p4, True)
# P5 observed-only: the neighbour arm keys off the SPELLED measured path, so an alias
# spelling evades it and a pre-existing neighbour file is destroyed. Measured as the
# SAME class on the r3 bytes (no regression), but it is a real residual of the arm's
# construction, so it is named here rather than asserted away.
probe("P5-symlink-alias-measured", p5, None)
probe("P6-relative-spelling", p6, True)
probe("P7-double-extension", p7, False, expect_clobber_free=True)
probe("P8-control-legitimate", p8, False, expect_clobber_free=True)

print("EX-27 adversarial sidecar probes  label=%s" % LABEL)
print("tool=%s sha256=%s" % (TOOL, TOOL_SHA))
print("=" * 96)
for r in results:
    st = {True: "HOLD", False: "FAIL", None: "obs "}[r["hold"]]
    print("%-32s exit=%-3s clobbered=%-5s closed=%-5s expect_closed=%-5s %s  %s" % (
        r["probe"], r["exit"], r["clobbered"], r["closed"], r["expect_closed"], st, r["note"]))
n_hold = sum(1 for r in results if r["hold"] is True)
n_fail = sum(1 for r in results if r["hold"] is False)
n_obs = sum(1 for r in results if r["hold"] is None)
n_clob = sum(1 for r in results if r["clobbered"])
print("=" * 96)
print("SUMMARY label=%s probes=%d hold=%d fail=%d observed=%d clobbered=%d" % (
    LABEL, len(results), n_hold, n_fail, n_obs, n_clob))
