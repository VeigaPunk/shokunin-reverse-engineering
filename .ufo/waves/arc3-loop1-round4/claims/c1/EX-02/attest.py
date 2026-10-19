#!/usr/bin/env python3
"""Re-runnable attestation for the arc3-loop1-round4 C1 vyper venv (EX-02).

Verifies, from bytes on disk:
  1. the target venv's interpreter identity and pyvenv.cfg
  2. the installed vyper tree against the wheel recorded in this directory
  3. the installed dependency .so / .py payloads against the recorded wheels
  4. vyper's operability (--version) and its own selector derivation on the smoke carrier

Exit 0 = every check passed.  Read-only with respect to the venv; writes nothing
outside stdout.  Usage:  python3 attest.py [--venv PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", ".."))
DEFAULT_VENV = os.path.join(REPO, ".ufo", "waves", "arc3-loop1-round4", "tools", "vyper-venv")

# wheel -> PyPI-attested sha256 (independently re-derived by this seat AND by EX-01)
WHEELS = {
    "vyper-0.4.3-py3-none-any.whl":
        "3b9671727c888363740dc678e60336759871487d0e4e9fdd973048fa9635c4fd",
    "immutables-0.21-cp314-cp314-linux_x86_64.whl":
        "63cc2954d6009065c543fa213f3f9541aa13e15b282ae59263a411c47e2c3c5d",
    "cbor2-5.9.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl":
        "422817286c1d0ce947fb2f7eca9212b39bddd7231e8b452e2d2cc52f15332dba",
    "asttokens-3.0.2-py3-none-any.whl":
        "9da13157f5b28becde0bd374fc677dcd3c290614264eff096f167c469cd9f933",
    "pycryptodome-3.24.1-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl":
        "93619c3117a8f14ea1267b427e465d152a66c89c3d3c643262070c05b2855aae",
    "packaging-26.3-py3-none-any.whl":
        "d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c",
    "lark-1.3.1-py3-none-any.whl":
        "c629b661023a014c37da873b4ff58a817398d12635d3bbb2c5a03be7fe5d1e12",
    "wheel-0.48.0-py3-none-any.whl":
        "3217dcc807155e45db462d7ef2431f5ddda0d7273b700d05a67b271ceb1287ab",
}

FAILURES: list[str] = []


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(label)


def site_packages(venv: str) -> str:
    for entry in sorted(os.listdir(os.path.join(venv, "lib"))):
        sp = os.path.join(venv, "lib", entry, "site-packages")
        if os.path.isdir(sp):
            return sp
    raise SystemExit("no site-packages found under " + venv)


def record_paths(record: str) -> list[str]:
    out = []
    with open(record) as fh:
        for line in fh:
            name = line.split(",")[0].strip()
            if name and not name.endswith("__pycache__"):
                out.append(name)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--venv", default=DEFAULT_VENV)
    args = ap.parse_args()
    venv = os.path.abspath(args.venv)
    sp = site_packages(venv)

    print(f"venv: {venv}")
    print(f"site-packages: {sp}")
    print()

    print("1. interpreter identity")
    real = os.path.realpath(os.path.join(venv, "bin", "python"))
    check("venv python is the 3.14 interpreter under test",
          real == "/usr/bin/python3.14", real)
    ver = subprocess.run([os.path.join(venv, "bin", "python"), "--version"],
                         capture_output=True, text=True).stdout.strip()
    check("interpreter version", ver == "Python 3.14.7", ver)
    check("interpreter sha256",
          sha256(real) == "d78f9cf7178ecff09963551399855543c297f37ac207e626228bfe43cb26a70c",
          sha256(real))
    print()

    print("2. recorded wheels present and matching their attested digests")
    for name, want in WHEELS.items():
        p = os.path.join(HERE, name)
        if not os.path.exists(p):
            check(name, False, "not found in seat artifact dir")
            continue
        got = sha256(p)
        check(name, got == want, got[:16] + "…")
    print()

    print("3. installed payload vs the pinned vyper wheel (byte-identical)")
    vyper_whl = os.path.join(HERE, "vyper-0.4.3-py3-none-any.whl")
    if not os.path.exists(vyper_whl):
        check("vyper wheel available for comparison", False)
    else:
        with zipfile.ZipFile(vyper_whl) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
            same = diff = missing = 0
            bad: list[str] = []
            for n in names:
                if n.startswith("vyper-0.4.3.data/data/"):
                    continue  # installed to the venv prefix, checked separately
                if n == "vyper-0.4.3.dist-info/RECORD":
                    continue  # pip rewrites RECORD at install time
                target = os.path.join(sp, n)
                if not os.path.exists(target):
                    missing += 1
                    bad.append(f"missing {n}")
                    continue
                data = zf.read(n)
                if hashlib.sha256(data).hexdigest() == sha256(target):
                    same += 1
                else:
                    diff += 1
                    bad.append(f"differs {n}")
            check(f"vyper payload files identical ({same} files)", diff == 0 and missing == 0,
                  f"differ={diff} missing={missing}")
            for b in bad[:5]:
                print(f"        {b}")
    # the .data/ payload relocates to the venv prefix
    prefix_file = os.path.join(venv, "vyper_git_commithash.txt")
    check("relocated .data/ payload present at venv prefix",
          os.path.exists(prefix_file) and sha256(prefix_file) ==
          "5064033b27edd58fcc174dc763d54b6501cc4e1f09f6336601ab75b0c5d1cbd1")
    print()

    print("4. installed dependency payloads vs their pinned wheels")
    deps = {
        "immutables-0.21-cp314-cp314-linux_x86_64.whl": "immutables/_map.cpython-314-x86_64-linux-gnu.so",
        "cbor2-5.9.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl": None,
        "asttokens-3.0.2-py3-none-any.whl": None,
        "pycryptodome-3.24.1-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl": None,
        "packaging-26.3-py3-none-any.whl": None,
        "lark-1.3.1-py3-none-any.whl": None,
        "wheel-0.48.0-py3-none-any.whl": None,
    }
    for whl, only in deps.items():
        p = os.path.join(HERE, whl)
        if not os.path.exists(p):
            check(whl, False, "not found in seat artifact dir")
            continue
        with zipfile.ZipFile(p) as zf:
            names = [n for n in zf.namelist()
                     if not n.endswith("/")
                     and ".dist-info/" not in n
                     and not n.endswith(".pyc")]
            if only:
                names = [n for n in names if n == only]
            same = diff = missing = 0
            for n in names:
                target = os.path.join(sp, n)
                if not os.path.exists(target):
                    missing += 1
                    continue
                if hashlib.sha256(zf.read(n)).hexdigest() == sha256(target):
                    same += 1
                else:
                    diff += 1
            check(f"{whl.split('-')[0]} ({same} payload files)", diff == 0 and missing == 0,
                  f"differ={diff} missing={missing}")
    print()

    print("5. operability")
    r = subprocess.run([os.path.join(venv, "bin", "vyper"), "--version"],
                       capture_output=True, text=True)
    check("vyper --version", r.returncode == 0 and r.stdout.strip() == "0.4.3+commit.bff19ea2",
          r.stdout.strip())
    smoke = os.path.join(HERE, "smoke", "Smoke.vy")
    r = subprocess.run([os.path.join(venv, "bin", "vyper"), "-f", "method_identifiers", smoke],
                       capture_output=True, text=True)
    import json as _json
    try:
        got = _json.loads(r.stdout)
    except Exception:
        got = {}
    want = {"increment()": "0xd09de08a", "get()": "0x6d4ce63c",
            "owner()": "0x8da5cb5b", "counter()": "0x61bc221a"}
    check("vyper derives the smoke carrier's own selector set (4/4)", got == want, str(got))
    print()

    print("VERDICT:", "ALL CHECKS PASS" if not FAILURES else f"{len(FAILURES)} FAILURE(S)")
    for f in FAILURES:
        print("   failed:", f)
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
