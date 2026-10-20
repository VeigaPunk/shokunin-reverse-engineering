#!/usr/bin/env python3
"""carrier-census.py -- static census of candidate Go carrier binaries.

For each PATH given on the command line this tool records, without executing
the carrier and without touching the network directly:

  * sha256 and size (bytes) of the file at the given path (read once);
  * an ELF check by magic bytes (file-style: is_elf plus class/data/machine
    when the e_ident header is parseable);
  * the Go version and REA evidence_id reported by
    `npx -y rea-agents@<VER> inspect-go-binary PATH --format json`
    (a read-only static build-info reader; the carrier is never run);
  * the pacman owner string from `pacman -Qo PATH` (a read-only database
    query; no other pacman operation is performed).

Output schema (written to --out FILE and printed to stdout, sort_keys=True,
indent=2):

  {
    "tool": "carrier-census.py",
    "generated_at_utc": <ISO8601>,
    "rea_version": <str>,
    "carriers": [
      {
        "path": <str as given>,
        "sha256": <hex|null>,
        "size": <int|null>,
        "is_elf": <bool>,
        "elf": {"class": <str|null>, "data": <str|null>,
                "machine": <str|null>} | null,
        "inspect": {
          "argv": [..], "exit": <int|null>,
          "go_version": <str|null>,
          "evidence_id": <str|null>,
          "module_path": <str|null>,
          "go_version_raw": <str|null>,
          "stderr_tail": <str>,
          "error": <str|null>
        },
        "pacman": {"argv": [..], "exit": <int|null>,
                   "owner": <str|null>, "error": <str|null>}
      }, ...
    ],
    "counts": {"total": N, "elf": N, "go_version_found": N,
               "pacman_owned": N, "errors": N}
  }

Errors are recorded per-carrier, never hidden. Exit codes:
  0  census emitted (per-carrier errors are data, not a tool failure)
  2  could-not-evaluate: bad arguments, --out directory unreadable, or
     every carrier failed to be read at all.
Carrier binaries are never executed. `--selftest` builds its own fixtures
under tempfile.mkdtemp(), stubs the npx/pacman subprocesses, and removes
everything afterwards.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

REA_VERSION = "6.5.0"

ELF_CLASSES = {1: "ELF32", 2: "ELF64"}
ELF_DATA = {1: "LSB", 2: "MSB"}
ELF_MACHINES = {
    0x03: "x86",
    0x08: "mips",
    0x28: "aarch64",
    0x3E: "x86_64",
    0xB7: "aarch64",
    0xF3: "riscv",
}


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def elf_info(header):
    """Classify a 64-byte ELF header by magic. Returns dict or None."""
    if len(header) < 20 or header[:4] != b"\x7fELF":
        return None
    ei_class = header[4]
    ei_data = header[5]
    endian = "little" if ei_data == 1 else "big"
    machine = int.from_bytes(header[18:20], endian)
    return {
        "class": ELF_CLASSES.get(ei_class, "unknown(%d)" % ei_class),
        "data": ELF_DATA.get(ei_data, "unknown(%d)" % ei_data),
        "machine": ELF_MACHINES.get(machine, "0x%02x" % machine),
    }


def run_inspect(path, rea_version, timeout=120):
    argv = [
        "npx", "-y", "rea-agents@%s" % rea_version,
        "inspect-go-binary", path, "--format", "json",
    ]
    rec = {
        "argv": argv, "exit": None, "go_version": None,
        "evidence_id": None, "module_path": None,
        "go_version_raw": None, "stderr_tail": "", "error": None,
    }
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        rec["error"] = "spawn/timeout: %s" % e
        return rec
    rec["exit"] = proc.returncode
    rec["stderr_tail"] = (proc.stderr or "")[-2000:]
    if proc.returncode != 0:
        rec["error"] = "inspect-go-binary exited %d" % proc.returncode
        return rec
    try:
        doc = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        rec["error"] = "stdout not JSON: %s" % e
        return rec
    rec["evidence_id"] = doc.get("evidence_id")
    nr = doc.get("normalized_result") or {}
    bi = nr.get("build_info") or {}
    rec["go_version"] = bi.get("go_version")
    rec["go_version_raw"] = bi.get("go_version_bytes_base64")
    modtext = bi.get("module_text") or ""
    m = re.search(r"^mod\t([^\t]+)\t", modtext, re.M)
    if m:
        rec["module_path"] = m.group(1)
    return rec


def run_pacman(path, timeout=30):
    argv = ["pacman", "-Qo", path]
    rec = {"argv": argv, "exit": None, "owner": None, "error": None}
    try:
        proc = subprocess.run(
            argv, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        rec["error"] = "spawn/timeout: %s" % e
        return rec
    rec["exit"] = proc.returncode
    out = (proc.stdout or "").strip()
    err = (proc.stderr or "").strip()
    if proc.returncode == 0 and out:
        # e.g. "/usr/bin/shfmt is owned by shfmt 3.14.1-1"
        rec["owner"] = out.splitlines()[0]
    else:
        rec["error"] = err or out or ("pacman -Qo exited %d" % proc.returncode)
    return rec


def census(path, rea_version, inspect_runner=None, pacman_runner=None):
    row = {
        "path": path, "sha256": None, "size": None, "is_elf": False,
        "elf": None, "inspect": None, "pacman": None, "error": None,
    }
    try:
        row["size"] = os.path.getsize(path)
        row["sha256"] = sha256_file(path)
        with open(path, "rb") as f:
            header = f.read(64)
        info = elf_info(header)
        row["is_elf"] = info is not None
        row["elf"] = info
    except OSError as e:
        row["error"] = "unreadable: %s" % e
        return row
    insp = (inspect_runner or run_inspect)(path, rea_version)
    pac = (pacman_runner or run_pacman)(path)
    row["inspect"] = insp
    row["pacman"] = pac
    return row


def selftest():
    cases = 0
    tmp = tempfile.mkdtemp(prefix="carrier-census-selftest-")
    try:
        # fixture 1: minimal fake ELF64 with a parseable header
        elf_path = os.path.join(tmp, "fake-elf")
        hdr = bytearray(64)
        hdr[0:4] = b"\x7fELF"
        hdr[4] = 2   # ELFCLASS64
        hdr[5] = 1   # little endian
        hdr[16:18] = (2).to_bytes(2, "little")   # ET_EXEC
        hdr[18:20] = (0x3E).to_bytes(2, "little")  # x86_64
        with open(elf_path, "wb") as f:
            f.write(hdr + b"\x00" * 128)
        # fixture 2: non-ELF file
        txt_path = os.path.join(tmp, "not-elf")
        with open(txt_path, "wb") as f:
            f.write(b"#!/bin/sh\necho hi\n")
        # fixture 3: unreadable path (nonexistent)
        missing_path = os.path.join(tmp, "missing")

        canned_stdout = json.dumps({
            "evidence_id": "ev_selftest",
            "normalized_result": {
                "build_info": {
                    "go_version": "go1.27.0-X:nodwarf5",
                    "go_version_bytes_base64": "AAAA",
                    "module_text": "mod\texample.com/m\tv1.0.0\t\n",
                }
            },
        })

        def fake_inspect(path, ver):
            return {
                "argv": ["npx", "-y", "rea-agents@%s" % ver,
                         "inspect-go-binary", path, "--format", "json"],
                "exit": 0,
                "go_version": "go1.27.0-X:nodwarf5",
                "evidence_id": "ev_selftest",
                "module_path": "example.com/m",
                "go_version_raw": "AAAA",
                "stderr_tail": "",
                "error": None,
            }

        def fake_pacman(path):
            return {"argv": ["pacman", "-Qo", path], "exit": 0,
                    "owner": "%s is owned by pkg 1.0-1" % path,
                    "error": None}

        rows = [
            census(elf_path, "selftest", fake_inspect, fake_pacman),
            census(txt_path, "selftest", fake_inspect, fake_pacman),
            census(missing_path, "selftest", fake_inspect, fake_pacman),
        ]
        checks = [
            rows[0]["is_elf"] is True,
            rows[0]["elf"]["machine"] == "x86_64",
            rows[0]["inspect"]["go_version"] == "go1.27.0-X:nodwarf5",
            rows[0]["inspect"]["evidence_id"] == "ev_selftest",
            rows[0]["inspect"]["module_path"] == "example.com/m",
            rows[0]["pacman"]["owner"].endswith("pkg 1.0-1"),
            rows[1]["is_elf"] is False,
            rows[1]["elf"] is None,
            rows[2]["error"] is not None and "unreadable" in rows[2]["error"],
            rows[0]["sha256"] == hashlib.sha256(hdr + b"\x00" * 128).hexdigest(),
        ]
        cases = len(checks)
        if all(checks):
            print("SELFTEST: CLEAN cases=%d" % cases)
            return 0
        print("SELFTEST: FAILED checks=%s" % checks)
        return 1
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Static census of Go carrier candidates: sha256/size, "
                    "ELF magic, REA inspect-go-binary go_version+evidence_id, "
                    "pacman -Qo owner. Never executes a carrier; never any "
                    "pacman operation other than the read-only -Qo query.")
    ap.add_argument("--out", help="write census JSON to FILE")
    ap.add_argument("--rea-version", default=REA_VERSION)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not args.paths:
        print("error: no carrier paths given", file=sys.stderr)
        return 2

    carriers = [census(p, args.rea_version) for p in args.paths]
    result = {
        "tool": "carrier-census.py",
        "generated_at_utc": utcnow(),
        "rea_version": args.rea_version,
        "carriers": carriers,
        "counts": {
            "total": len(carriers),
            "elf": sum(1 for c in carriers if c["is_elf"]),
            "go_version_found": sum(
                1 for c in carriers
                if c["inspect"] and c["inspect"]["go_version"]),
            "pacman_owned": sum(
                1 for c in carriers
                if c["pacman"] and c["pacman"]["owner"]),
            "errors": sum(1 for c in carriers if c["error"]),
        },
    }
    text = json.dumps(result, sort_keys=True, indent=2)

    if args.out:
        outdir = os.path.dirname(os.path.abspath(args.out))
        if not os.path.isdir(outdir):
            print("error: --out directory does not exist: %s" % outdir,
                  file=sys.stderr)
            return 2
        try:
            with open(args.out, "w") as f:
                f.write(text + "\n")
        except OSError as e:
            print("error: cannot write %s: %s" % (args.out, e),
                  file=sys.stderr)
            return 2
    print(text)
    # "could-not-evaluate" only when every carrier failed to be read at all.
    if result["counts"]["errors"] == result["counts"]["total"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
