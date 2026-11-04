#!/usr/bin/env python3
"""seam-probe.py - round-70 instrument (R70-C2 operability, capability).

The safe packer seam, proven black-box against the instrument's committed
bytes (round-69 routed defects M69-9/S-1, M69-10, M69-11; QUALITY #113):

  A1 hash_before_exec       the caller-supplied --upx is hashed and pin-compared
                            BEFORE its first execution: an impostor script that
                            prints the pinned version but hashes differently is
                            refused (exit 2, packer sha256 clause) and provably
                            never executed (its execution log stays absent)
  A2 threaded_path          the validated packer path is the one the carrier
                            loop executes: in the producer-bound measured
                            receipt every upx argv[0] equals the pinned-copy
                            path the run was given (--expect-upx), never the
                            module default
  A3 child_env_allowlist    the packer's children receive exactly the frozen
                            allowlist (build_child_env): the committed case
                            inventory names the child-env cases and the blob's
                            own --selftest is green at that case count
  A4 broken_node_typed      a node that exists but cannot run is a typed
                            `broken_tool: node` exit 2, never a traceback or a
                            misleading inventory clause
  A5 packer_exec_format     an exec-format-less --upx is a typed packer refusal
                            (exit 2, no traceback)
  A6 home_no_tmp            with HOME unset the instrument still never falls
                            back to /tmp: the receipt's child_env HOME lives
                            inside --work, and the blob carries no /tmp HOME
                            fallback
  A7 per_run_work           two battery runs sharing one --work each record
                            their own distinct mkdtemp work_dir

The instrument under test is read from git (`--root`/`--rev`) into per-run
scratch and invoked as a black box; the measured receipt read by A2 is bound to
its producer (its recorded revision and instrument hash must equal the ones
this probe was invoked with) before its argv records are trusted.

Exit: 0 all seven arms pass; 1 arms failed, each named with its observation;
2 could-not-evaluate (unknown revision, missing host tool, bad argv).
`--validate <receipt>` checks a probe receipt's structural honesty.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
UPX_VERSION_PIN = "upx 5.2.0"
TMP_FALLBACK_PATTERN = 'os.environ.get("HOME", "/tmp")'
CHILD_ENV_CASES = ("child-env-allowlist", "child-env-home-in-work", "child-env-no-tmp")


class Unevaluable(Exception):
    """Exit-2 class: the probe cannot score, so it claims nothing."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(blob_path: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location("r70_seam_probe_target", blob_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blob_to(root: str, rev: str, tool: str, scratch: str) -> tuple[str, str]:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed rc={proc.returncode}")
    path = os.path.join(scratch, os.path.basename(tool))
    with open(path, "wb") as fh:
        fh.write(proc.stdout)
    os.chmod(path, 0o755)
    return path, sha256_bytes(proc.stdout)


def parse_unevaluable(stdout: str, stderr: str) -> dict | None:
    for text in (stdout, stderr):
        for chunk in [text.strip()] + text.splitlines()[::-1]:
            chunk = chunk.strip()
            if not chunk.startswith("{"):
                continue
            try:
                payload = json.loads(chunk)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and "unevaluable" in payload:
                return payload
    return None


def parse_json_out(stdout: str) -> dict | None:
    stripped = stdout.strip()
    if stripped.startswith("{"):
        try:
            payload = json.loads(stripped)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            pass
    for chunk in stdout.splitlines()[::-1]:
        chunk = chunk.strip()
        if not chunk.startswith("{"):
            continue
        try:
            payload = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return None


def invoke(instrument: str, root: str, rev: str, pkg: str, work: str,
           extra: list[str], path: str | None = None,
           keep_home: bool = True, with_pkg: bool = True) -> dict:
    env = {"PATH": path or os.environ.get("PATH", "/usr/bin"),
           "LANG": os.environ.get("LANG", "C")}
    if keep_home and os.environ.get("HOME"):
        env["HOME"] = os.environ["HOME"]
    argv = [sys.executable, "-I", "-B", instrument,
            "--root", root, "--rev", rev]
    if with_pkg:
        argv += ["--pkg", pkg]
    argv += ["--work", work, *extra]
    proc = subprocess.run(argv,
                          capture_output=True, text=True, timeout=1800, env=env)
    return {"rc": proc.returncode, "env_keys": sorted(env),
            "unevaluable": (parse_unevaluable(proc.stdout, proc.stderr) or {}).get("unevaluable"),
            "stdout": proc.stdout[-60000:], "stderr_tail": proc.stderr[-2000:],
            "traceback": "Traceback" in proc.stderr}


def arm(aid: str, ok: bool, observed: dict) -> dict:
    return {"id": aid, "ok": bool(ok), "observed": observed}


def bind_producer(receipt_path: str, root: str, rev: str, tool: str,
                  blob_sha: str) -> tuple[dict | None, list[str]]:
    """QUALITY #114: bind the measured receipt to its producer before reading it."""
    defects = []
    try:
        with open(receipt_path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"receipt unreadable: {exc}"]
    instrument = receipt.get("instrument")
    if not isinstance(instrument, dict) or not instrument:
        defects.append("receipt.instrument absent")
    else:
        if instrument.get("path") != tool:
            defects.append(f"instrument.path {instrument.get('path')} != {tool}")
        if instrument.get("sha256") != blob_sha:
            defects.append(f"instrument.sha256 {instrument.get('sha256')} != blob at {rev}")
    if receipt.get("rev") != rev:
        defects.append(f"receipt.rev {receipt.get('rev')} != {rev}")
    return receipt, defects


def check(root: str, rev: str, tool: str, pkg: str, work: str,
          battery_tool: str, receipt_path: str | None,
          expect_upx: str | None) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    scratch = tempfile.mkdtemp(prefix="seam-probe-", dir=work)
    instrument, blob_sha = blob_to(root, rev, tool, scratch)
    battery, battery_sha = blob_to(root, rev, battery_tool, scratch)
    mod = load_module(instrument)
    arms = []

    # A1 - hash before execution: impostor prints the pinned version, hashes
    # differently, and logs its own execution if it is ever run.
    a1_dir = tempfile.mkdtemp(prefix="a1-", dir=work)
    log = os.path.join(a1_dir, "executed.log")
    impostor = os.path.join(a1_dir, "upx-impostor")
    with open(impostor, "w", encoding="utf-8") as fh:
        fh.write(f"#!/bin/sh\necho '{UPX_VERSION_PIN}'\n"
                 f"touch {log}\nexit 0\n")
    os.chmod(impostor, 0o755)
    a1 = invoke(instrument, root, rev, pkg, a1_dir, ["--upx", impostor])
    executed = os.path.exists(log)
    arms.append(arm("A1_hash_before_exec",
                    a1["rc"] == 2 and "packer" in str(a1["unevaluable"] or "")
                    and "sha256" in str(a1["unevaluable"] or "") and not executed,
                    {**a1, "impostor_executed": executed}))

    # A2 - the threaded path: the producer-bound receipt's upx argv all name the
    # pinned copy the run was given, never the module default.
    if receipt_path and expect_upx:
        receipt, defects = bind_producer(receipt_path, root, rev, tool, blob_sha)
        argv0s, missing = [], []
        if receipt is not None:
            if not os.path.exists(expect_upx) or sha256_bytes(
                    open(expect_upx, "rb").read()) != UPX_SHA256_PIN:
                defects.append("--expect-upx is not the pinned packer bytes")
            if os.path.abspath(expect_upx) == os.path.abspath(mod.UPX):
                defects.append("--expect-upx equals the module default path")
            for c in receipt.get("carriers") or []:
                for name in ("pack", "unpack"):
                    argv = ((c.get("runs") or {}).get(name) or {}).get("argv") or []
                    if argv:
                        argv0s.append(argv[0])
                    else:
                        missing.append(f"{c.get('id')}:{name}")
            threaded = not defects and not missing and argv0s \
                and all(a == expect_upx for a in argv0s)
        else:
            threaded = False
        arms.append(arm("A2_threaded_path", threaded,
                        {"defects": defects, "argv0s": argv0s, "missing": missing,
                         "expect_upx": expect_upx, "module_default": mod.UPX}))
    else:
        arms.append(arm("A2_threaded_path", False,
                        {"missing": "no --receipt or no --expect-upx"}))

    # A3 - the child-env cases exist in the committed case inventory and the
    # blob's own selftest is green at that case count.
    selftest = invoke(instrument, root, rev, pkg, work, ["--selftest"])
    st = parse_json_out(selftest["stdout"]) or {}
    names_in_registry = all(n in getattr(mod, "REGISTERED_CASES", []) for n in CHILD_ENV_CASES)
    a3_ok = (selftest["rc"] == 0 and st.get("ok") is True and st.get("failed") == []
             and names_in_registry
             and st.get("cases") == len(getattr(mod, "REGISTERED_CASES", [])))
    arms.append(arm("A3_child_env_allowlist", a3_ok,
                    {"selftest_rc": selftest["rc"], "cases": st.get("cases"),
                     "failed": st.get("failed"),
                     "cases_in_registry": names_in_registry,
                     "registry_cases": len(getattr(mod, "REGISTERED_CASES", []))}))

    # A4 - a node that exists but cannot run is a typed broken_tool.
    a4_dir = tempfile.mkdtemp(prefix="a4-", dir=work)
    bin4 = os.path.join(a4_dir, "bin")
    os.makedirs(bin4)
    for name in ("git", "readelf", "upx"):
        found = shutil.which(name)
        if not found:
            raise Unevaluable(f"host tool absent: {name}")
        os.symlink(found, os.path.join(bin4, name))
    broken_node = os.path.join(bin4, "node")
    with open(broken_node, "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\nexit 7\n")
    os.chmod(broken_node, 0o755)
    a4 = invoke(instrument, root, rev, pkg, a4_dir, [], path=bin4)
    a4_clause = str(a4["unevaluable"] or "")
    arms.append(arm("A4_broken_node_typed",
                    a4["rc"] == 2 and "broken_tool" in a4_clause
                    and "node" in a4_clause and not a4["traceback"],
                    {**a4, "stderr_tail": a4["stderr_tail"][-400:]}))

    # A5 - an exec-format-less packer is a typed refusal, never a traceback.
    a5_dir = tempfile.mkdtemp(prefix="a5-", dir=work)
    notelf = os.path.join(a5_dir, "not-an-elf")
    with open(notelf, "wb") as fh:
        fh.write(b"DEFINITELY-NOT-AN-ELF-OR-SCRIPT\x00\x01\x02\x03garbage")
    os.chmod(notelf, 0o755)
    a5 = invoke(instrument, root, rev, pkg, a5_dir, ["--upx", notelf])
    arms.append(arm("A5_packer_exec_format",
                    a5["rc"] == 2 and "packer" in str(a5["unevaluable"] or "")
                    and not a5["traceback"],
                    {**a5, "stderr_tail": a5["stderr_tail"][-400:]}))

    # A6 - with HOME unset the child env still never falls back to /tmp.
    a6_dir = tempfile.mkdtemp(prefix="a6-", dir=work)
    a6 = invoke(instrument, root, rev, pkg, a6_dir, ["--skip-run"], keep_home=False)
    payload = parse_json_out(a6["stdout"]) or {}
    cenv = payload.get("child_env") or {}
    home_ok = bool(cenv) and str(cenv.get("home", "")).startswith(os.path.abspath(a6_dir)) \
        and str(cenv.get("home", "")) != "/tmp"
    blob_text = open(instrument, encoding="utf-8", errors="replace").read()
    no_tmp_fallback = TMP_FALLBACK_PATTERN not in blob_text
    arms.append(arm("A6_home_no_tmp", a6["rc"] == 1 and home_ok and no_tmp_fallback,
                    {"rc": a6["rc"], "child_env": cenv,
                     "tmp_fallback_in_source": not no_tmp_fallback,
                     "work": os.path.abspath(a6_dir)}))

    # A7 - per-run work: two battery runs sharing --work record distinct dirs.
    run_a = invoke(battery, root, rev, pkg, work,
                   ["--patch-set", "r70", "--tool", tool,
                    "--min-pristine-cases", "0"], with_pkg=False)
    run_b = invoke(battery, root, rev, pkg, work,
                   ["--patch-set", "r70", "--tool", tool,
                    "--min-pristine-cases", "0"], with_pkg=False)
    ra = parse_json_out(run_a["stdout"]) or {}
    rb = parse_json_out(run_b["stdout"]) or {}
    wa, wb = ra.get("work_dir"), rb.get("work_dir")
    a7_ok = (run_a["rc"] == 0 and run_b["rc"] == 0
             and isinstance(wa, str) and isinstance(wb, str)
             and wa != wb and wa.startswith(os.path.abspath(work))
             and wb.startswith(os.path.abspath(work)))
    arms.append(arm("A7_per_run_work", a7_ok,
                    {"rc_a": run_a["rc"], "rc_b": run_b["rc"],
                     "work_dir_a": wa, "work_dir_b": wb,
                     "distinct": isinstance(wa, str) and wa != wb}))

    failed = [a["id"] for a in arms if not a["ok"]]
    return {"instrument": tool, "rev": rev, "battery": battery_tool,
            "receipt": receipt_path, "expect_upx": expect_upx,
            "instrument_sha256": blob_sha, "battery_sha256": battery_sha,
            "arms": arms, "arms_passed": len(arms) - len(failed),
            "target": len(arms), "failed": failed, "ok": not failed,
            "scratch": scratch}


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": "seam-probe-receipt", "unevaluable": str(exc)}))
        return 2
    defects = []
    arms = receipt.get("arms")
    if not isinstance(arms, list) or not arms:
        defects.append("arms absent or empty")
        arms = []
    for a in arms:
        if not isinstance(a.get("id"), str):
            defects.append("an arm has no id")
        if not isinstance(a.get("ok"), bool):
            defects.append(f"{a.get('id')}: ok not a bool")
        if not isinstance(a.get("observed"), dict) or not a.get("observed"):
            defects.append(f"{a.get('id')}: no observation")
    derived = [a.get("id") for a in arms if a.get("ok") is True]
    if receipt.get("arms_passed") != len(derived):
        defects.append("arms_passed disagrees with the arm rows")
    if receipt.get("target") != len(arms):
        defects.append(f"target {receipt.get('target')} != arm rows {len(arms)}")
    if sorted(receipt.get("failed") or []) != sorted(
            a.get("id") for a in arms if a.get("ok") is not True):
        defects.append("failed disagrees with the arm rows")
    out = {"validate": "seam-probe-receipt", "path": path, "ok": not defects,
           "defects": defects, "arms": len(arms)}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not defects else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--tool")
    ap.add_argument("--battery")
    ap.add_argument("--pkg")
    ap.add_argument("--work")
    ap.add_argument("--receipt")
    ap.add_argument("--expect-upx")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.validate:
        return validate(args.validate)
    if not (args.root and args.rev and args.tool and args.battery
            and args.pkg and args.work):
        print("seam-probe: --root, --rev, --tool, --battery, --pkg and --work "
              "are required", file=sys.stderr)
        return 2
    try:
        receipt = check(args.root, args.rev, args.tool, args.pkg, args.work,
                        args.battery, args.receipt, args.expect_upx)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r70-seam-probe-v1",
                          "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
