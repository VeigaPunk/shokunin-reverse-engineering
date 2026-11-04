#!/usr/bin/env python3
"""ExecC2's OWN harness for R69-C2 (never runs tools/round-69/contract-probe.py).

Builds fixtures (a)-(e) from the seat spec plus unnamed shapes, invokes the
frozen instrument with a controlled environment, and records rc, the full
stderr/stdout and the typed class.  Classification:

  typed       rc == 2, a JSON envelope with "unevaluable" on stderr, no traceback
  leak        a Python traceback reached the caller (the preflight docstring
              promises "a named class, never a crash")
  verdict     0/1 with a receipt (a scoring run, not a refusal)
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "f15998102f1ce3569e61faa2ac6f286bc414538e"
PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
S = "/fast/scratch/hyaku/kaidoku-r69/ExecC2"
R69 = os.path.join(ROOT, "tools/round-69/packed-elf.py")
R68 = os.path.join(ROOT, "tools/round-68/packed-elf.py")
UPX = "/usr/bin/upx"
PY = sys.executable


def sh(path, body, mode=0o755):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    os.chmod(path, mode)
    return path


def build():
    fx = os.path.join(S, "fixtures")
    shutil.rmtree(fx, ignore_errors=True)
    os.makedirs(fx)
    pb = os.path.join(fx, "pathbin_no_node")
    os.makedirs(pb)
    for t in ("git", "readelf", "upx"):
        os.symlink(shutil.which(t), os.path.join(pb, t))
    pbx = os.path.join(fx, "pathbin_node_nonexec")
    shutil.copytree(pb, pbx, symlinks=True)
    sh(pbx + "/node", "#!/bin/sh\necho v24\n", 0o644)
    pbb = os.path.join(fx, "pathbin_node_broken")
    shutil.copytree(pb, pbb, symlinks=True)
    os.symlink("/nonexistent/node", pbb + "/node")

    ro = os.path.join(fx, "ro0500")
    os.makedirs(ro)
    os.chmod(ro, 0o500)

    upx510 = sh(os.path.join(fx, "upx-5.1.0"),
                "#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then echo 'upx 5.1.0'; exit 0; fi\n"
                "exit 3\n")
    upx520 = sh(os.path.join(fx, "upx-5.2.0"),
                "#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then echo 'upx 5.2.0'; exit 0; fi\n"
                "exit 3\n")
    bumped = os.path.join(fx, "upx-bumped")
    with open(UPX, "rb") as src, open(bumped, "wb") as dst:
        shutil.copyfileobj(src, dst)
        dst.write(b"\0")
    os.chmod(bumped, 0o755)

    # unnamed shape 1: executable bit, no valid executable format (ENOEXEC)
    garbage = os.path.join(fx, "upx-enoexec")
    with open(garbage, "wb") as fh:
        fh.write(b"\x00\x01\x02not-an-executable\n")
    os.chmod(garbage, 0o755)

    # unnamed shape 2: byte-identical packer that is executable but not readable
    noread = os.path.join(fx, "upx-unreadable")
    with open(UPX, "rb") as src, open(noread, "wb") as dst:
        shutil.copyfileobj(src, dst)
    os.chmod(noread, 0o111)

    # unnamed shape 3: --upx names a directory
    updir = os.path.join(fx, "upx-dir")
    os.makedirs(updir)

    # unnamed shape 4: a byte-identical copy elsewhere (passes the pin, used to
    # prove whether the seam value is the binary that actually packs)
    ident = os.path.join(fx, "upx-pinned-copy")
    shutil.copyfile(UPX, ident)
    os.chmod(ident, 0o755)

    # unnamed shape 5: --rev that git cannot resolve (no validation?)
    return {"pathbin_no_node": pb, "pathbin_node_nonexec": pbx,
            "pathbin_node_broken": pbb, "ro0500": ro, "upx510": upx510,
            "upx520": upx520, "bumped": bumped, "enoexec": garbage,
            "unreadable": noread, "updir": updir, "ident": ident}


def invoke(tool, work, extra, path, out):
    env = {"PATH": path or os.environ.get("PATH", "/usr/bin"),
           "HOME": os.environ.get("HOME", "/tmp"), "LANG": "C",
           "TMPDIR": os.path.join(S, "work")}
    proc = subprocess.run([PY, "-I", "-B", tool, "--root", ROOT, "--rev", REV,
                           "--pkg", PKG, "--work", work, *extra],
                          capture_output=True, text=True, timeout=1800,
                          env=env, cwd=S)
    with open(out + ".stdout", "w", encoding="utf-8") as fh:
        fh.write(proc.stdout)
    with open(out + ".stderr", "w", encoding="utf-8") as fh:
        fh.write(proc.stderr)
    unev, cls = None, None
    for line in proc.stderr.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and "unevaluable" in payload:
                unev = payload["unevaluable"]
                cls = unev.split(":", 1)[0]
    tb = "Traceback (most recent call last)" in proc.stderr
    if unev is not None and proc.returncode == 2 and not tb:
        kind = "typed"
    elif tb:
        kind = "leak"
    else:
        kind = "other"
    return {"rc": proc.returncode, "kind": kind, "class": cls,
            "unevaluable": unev, "traceback": tb,
            "stderr_tail": proc.stderr[-500:], "stdout_tail": proc.stdout[-300:],
            "stderr_file": out + ".stderr"}


def main():
    fx = build()
    work = os.path.join(S, "work")
    os.makedirs(work, exist_ok=True)
    res = []

    def case(aid, label, tool, workdir, extra, path, expect):
        out = os.path.join(S, "runs", aid)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        r = invoke(tool, workdir, extra, path, out)
        r.update({"id": aid, "label": label, "tool": os.path.basename(os.path.dirname(tool))
                  + "/" + os.path.basename(tool), "extra": extra,
                  "pathbin": None if path is None else os.path.basename(path),
                  "expected": expect})
        res.append(r)
        print(f"{aid:22s} rc={r['rc']} kind={r['kind']:6s} class={r['class']} "
              f"expect={expect}", flush=True)

    os.makedirs(os.path.join(S, "runs"), exist_ok=True)
    # --- the five spec fixtures, against the round-69 instrument ---
    case("A1_missing_node", "PATH dir with git/readelf/upx, no node", R69, work, [],
         fx["pathbin_no_node"], "node")
    case("A2_work_unusable", "0500 work dir", R69, fx["ro0500"], [], None, "work")
    case("A3_packer_version", "upx script printing 'upx 5.1.0'", R69, work,
         ["--upx", fx["upx510"]], None, "version")
    case("A4_packer_sha256", "real upx + one appended byte", R69, work,
         ["--upx", fx["bumped"]], None, "sha256")
    case("A5_packer_sha256_script", "upx script printing 'upx 5.2.0' (different bytes shape)",
         R69, work, ["--upx", fx["upx520"]], None, "sha256")

    # --- unnamed shapes ---
    case("U1_enoexec", "exec bit, no valid exec format (ENOEXEC)", R69, work,
         ["--upx", fx["enoexec"]], None, "typed class, no traceback")
    case("U2_unreadable", "byte-identical packer, mode 0111 (unreadable)", R69, work,
         ["--upx", fx["unreadable"]], None, "typed class, no traceback")
    case("U3_upx_is_dir", "--upx names a directory", R69, work,
         ["--upx", fx["updir"]], None, "missing_tool")
    case("U4_node_nonexec", "PATH node is a non-executable file", R69, work, [],
         fx["pathbin_node_nonexec"], "missing_tool")
    case("U5_node_broken", "PATH node is a broken symlink", R69, work, [],
         fx["pathbin_node_broken"], "missing_tool")
    case("U6_pkg_absent", "--pkg names a directory without package.json", R69, work,
         ["--pkg", fx["updir"]], None, "missing_tool")
    case("U7_work_absent", "--work does not exist", R69,
         os.path.join(work, "nope-not-here"), [], None, "work_unusable")
    case("U8_root_absent", "--root does not exist, --skip-run", R69, work,
         ["--root", "/nonexistent-lane", "--skip-run"], None, "typed git failure")
    case("U9_bogus_rev", "--rev is not a commit, --skip-run", R69, work,
         ["--rev", "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef", "--skip-run"], None,
         "unknown revision")
    case("U10_seam_identical", "--upx a byte-identical copy (pin holds), --skip-run",
         R69, work, ["--upx", fx["ident"], "--skip-run"], None, "accepts the seam value")

    # --- before arm: same five fixtures against the round-68 instrument ---
    for aid, label, wd, extra in (
            ("B1_missing_node", "round-68: PATH without node", work, []),
            ("B2_work_unusable", "round-68: 0500 work dir", fx["ro0500"], []),
            ("B3_packer_version", "round-68: --upx seam absent", work,
             ["--upx", fx["upx510"]]),
            ("B4_packer_sha256", "round-68: --upx seam absent", work,
             ["--upx", fx["bumped"]])):
        case(aid, label, R68, wd, extra, fx["pathbin_no_node"] if aid == "B1_missing_node" else None,
             "no typed contract (base)")

    with open(os.path.join(S, "arm-receipt.json"), "w", encoding="utf-8") as fh:
        json.dump({"harness": "ExecC2/attack.py", "rev": REV, "instrument": R69,
                   "instrument_sha256": __import__("hashlib").sha256(
                       open(R69, "rb").read()).hexdigest(),
                   "arms": res}, fh, indent=1, sort_keys=True)
    print("wrote", os.path.join(S, "arm-receipt.json"))


if __name__ == "__main__":
    main()
