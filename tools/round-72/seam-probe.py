#!/usr/bin/env python3
"""seam-probe.py - round-72 instrument (R72-C1 coverage, R72-C2 calibration).

Round-71 arms are retained.

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

Round 71 adds the three runtime arms the round-70 wave routed (M70-6), moving
the frontier line "runtime env-capture/concurrent-scratch coverage of the seam
arms" into Core: A8 observes the child environment from the raw per-child log
(the packer, node and readelf children, exact allowlist, HOME/TMPDIR under that
run's own run_root, an exported canary absent); A9 starts three battery runs and
three route preflights concurrently on one --work parent and requires distinct
work_dirs and distinct run_roots with each env log under its own root; A10
checks the pre-committed run binding (nonce hash against the caller's
commitment, a re-derived run_binding, the genuine receipt accepted and a
transplanted round-70 receipt, a wrong-nonce copy and a broken-binding copy each
rejected with their clause).

Round 72 (R72-C1/C2).  A10's binding verdict is read from the CHECKER's own
JSON clauses (`clauses.run_nonce`, `clauses.run_binding`), never re-derived
from the receipt's fields: the round-71 wave's mutation survivor i forced a
probe-side `binding_ok = True` and survived the probe's own test.  A11 closes
the checker-mode child-environment gap the round-71 note left Frontier: the
checker is run with a `git` and a `readelf` shim first on PATH that record the
exact bytes of their exec environment, with an exported canary in the caller's
environment; the arm requires both shims to observe exactly
HOME/LANG/PATH/TMPDIR, the canary absent, HOME and TMPDIR under the checker's
run root, and the checker's own `checker_child_env` block to record at least
the `git` and `readelf` classes cleanly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
UPX_VERSION_PIN = "upx 5.2.0"
TMP_FALLBACK_PATTERN = 'os.environ.get("HOME", "/tmp")'
CHILD_ENV_KEYS = ("HOME", "LANG", "PATH", "TMPDIR")


def under(root, path) -> bool:
    """Descendant test without the sibling-prefix false green (QUALITY #120)."""
    try:
        root_abs = os.path.abspath(str(root))
        return os.path.commonpath([root_abs, os.path.abspath(str(path))]) == root_abs
    except (TypeError, ValueError):
        return False
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
    # A blob can import a sibling module from its own directory (round-72's
    # packed-elf imports capsule_audit.py); the scratch copy must carry it, or
    # every black-box invocation dies at import.  Only lane modules are copied.
    srcdir = os.path.join(os.path.abspath(root), os.path.dirname(tool))
    for mod in ("capsule_audit.py",):
        src = os.path.join(srcdir, mod)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(scratch, mod))
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


def binding_verdict(checker: dict | None) -> dict:
    """A10's binding verdict comes from the checker's JSON, never the probe.

    The round-71 wave's MutReaders survivor i forced a probe-side
    `binding_ok = True`; it survived the probe's own test because the arm's
    boolean was re-derived from the receipt's own fields.  The verdict is now
    the checker's emitted clause; a missing clauses object is fail-closed
    (R72-C2).
    """
    clauses = (checker or {}).get("clauses")
    present = isinstance(clauses, dict)
    clauses = clauses if present else {}
    nonce_ok = clauses.get("run_nonce") is True and present
    binding_ok = clauses.get("run_binding") is True and present
    return {"present": present, "nonce_ok": bool(nonce_ok),
            "binding_ok": bool(binding_ok)}


def checker_met(checker: dict | None) -> bool:
    """The checker's own `met` and its clause block's `met` must agree (true).

    A checker that returns rc 0 with `met false` while its clauses read true is
    self-contradictory; A10 must not accept that (round-72 CriticClaims C2).
    """
    checker = checker if isinstance(checker, dict) else {}
    clauses = checker.get("clauses")
    return (checker.get("met") is True
            and isinstance(clauses, dict) and clauses.get("met") is True)


def parse_environ_file(path: str) -> dict | None:
    """A `/proc/self/environ` byte dump as a dict (NUL-separated, exact)."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError:
        return None
    env = {}
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        key, _, value = entry.partition(b"=")
        env[key.decode("utf-8", "replace")] = value.decode("utf-8", "replace")
    return env


def read_jsonl(path: str) -> tuple[list[dict], list[str]]:
    """Records and parse errors from a JSON Lines capsule (never a summary)."""
    records: list[dict] = []
    errors: list[str] = []
    try:
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"line {lineno}: {exc.__class__.__name__}")
                    continue
                if isinstance(payload, dict):
                    records.append(payload)
                else:
                    errors.append(f"line {lineno}: not an object")
    except OSError as exc:
        errors.append(f"unreadable: {exc.__class__.__name__}")
    return records, errors


def checker_log_verdict(records: list[dict]) -> dict:
    """A11's own reading of the checker's log: allowlist, canary, census.

    The checker's JSON summary is a claim; this derives the same facts from
    the raw records, so a checker (or a fake) that emits a clean summary
    without a matching log cannot pass (round-72 ReviewerGates).
    """
    envs = [rec.get("env") if isinstance(rec.get("env"), dict) else {}
            for rec in records]
    census: dict[str, int] = {}
    for rec in records:
        name = os.path.basename(str((rec.get("argv") or ["?"])[0]))
        census[name] = census.get(name, 0) + 1
    keys_exact = bool(envs) and all(sorted(e) == sorted(CHILD_ENV_KEYS) for e in envs)
    ok = (bool(records) and keys_exact
          and not any("KAIDOKU_ENV_CANARY" in e for e in envs)
          and census.get("git", 0) >= 1 and census.get("readelf", 0) >= 1)
    return {"ok": ok, "records": len(records), "keys_exact": keys_exact,
            "canary_present": any("KAIDOKU_ENV_CANARY" in e for e in envs),
            "children": census}


def invoke(instrument: str, root: str, rev: str, pkg: str, work: str,
           extra: list[str], path: str | None = None,
           keep_home: bool = True, with_pkg: bool = True,
           extra_env: dict | None = None) -> dict:
    env = {"PATH": path or os.environ.get("PATH", "/usr/bin"),
           "LANG": os.environ.get("LANG", "C")}
    if keep_home and os.environ.get("HOME"):
        env["HOME"] = os.environ["HOME"]
    if extra_env:
        env.update(extra_env)
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


def checker_env_arm(instrument: str, root: str, rev: str, pkg: str,
                    work: str, receipt_path: str,
                    nonce_commitment: str) -> dict:
    """A11: every checker-mode child runs under the four-key allowlist.

    Two independent witnesses: a `git` and a `readelf` shim first on PATH
    record the exact `/proc/self/environ` bytes they receive before exec'ing
    the real tool, and the checker's own capture log is read back from its
    JSON.  The caller's environment carries an exported canary; neither the
    shim bytes nor the checker log may show it.
    """
    scratch = tempfile.mkdtemp(prefix="a11-", dir=os.path.abspath(work))
    shim_dir = os.path.join(scratch, "shims")
    log_dir = os.path.join(scratch, "logs")
    os.makedirs(shim_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    canary = "KAIDOKU_ENV_CANARY"
    records = {}
    for name in ("git", "readelf"):
        # Trusted absolute host tool first; a PATH-resolved tool is the
        # fallback only (round-72 SentinelScope SS72-1: PATH is a trust
        # boundary, and the environment allowlist does not sanitize it).
        trusted = os.path.join("/usr/bin", name)
        real = trusted if os.path.exists(trusted) else shutil.which(name)
        if not real:
            return {"ok": False, "missing": f"host tool {name}"}
        record = os.path.join(log_dir, name + ".environ")
        shim = os.path.join(shim_dir, name)
        # A perl shim, not a shell: /bin/sh adds PWD/SHLVL/_ to the
        # environment it exports, so a shell shim would measure the shell, not
        # the exec boundary (verified: perl exec'd with four keys sees four).
        with open(shim, "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/perl\n"
                     "open(my $in, '<', '/proc/self/environ') or exit 127;\n"
                     "binmode $in; local $/; my $data = <$in>; close $in;\n"
                     "open(my $out, '>', '%s') or exit 127;\n"
                     "binmode $out; print $out $data; close $out;\n"
                     "exec '%s', @ARGV;\n" % (record, real))
        os.chmod(shim, 0o755)
        records[name] = record
    checker_log = os.path.join(log_dir, "checker.jsonl")
    path_env = shim_dir + os.pathsep + (os.environ.get("PATH") or "/usr/bin")
    res = invoke(instrument, root, rev, pkg, work,
                 ["--check-receipt", receipt_path,
                  "--child-env-log", checker_log,
                  "--nonce-commitment", nonce_commitment],
                 path=path_env, keep_home=True,
                 extra_env={canary: "probe-canary-r72",
                            "TMPDIR": os.path.join(log_dir, "tmp")})
    work_abs = os.path.abspath(work)
    shims = {}
    for name, record in records.items():
        env = parse_environ_file(record)
        shims[name] = {
            "recorded": env is not None,
            "values": env,
            "keys": sorted(env) if env else None,
            "keys_exact": bool(env) and sorted(env) == sorted(CHILD_ENV_KEYS),
            "canary_present": bool(env) and canary in env,
            "home_under_work": bool(env) and under(work_abs, env.get("HOME", "")),
            "tmpdir_under_work": bool(env) and under(work_abs, env.get("TMPDIR", "")),
        }
    payload = parse_json_out(res["stdout"]) or {}
    observed = payload.get("checker_child_env") or {}
    # Read the checker's log OURSELVES: the JSON summary is the checker's
    # claim, and a fake checker that emits a clean summary without a log (or
    # with a zero-count census) must fail (round-72 ReviewerGates).
    log_records, log_errors = read_jsonl(checker_log)
    log_verdict = checker_log_verdict(log_records)
    verdict = a11_verdict(res["rc"], observed, log_verdict, shims, work_abs)
    return {"ok": verdict["ok"], "rc": res["rc"], "shims": verdict["shim_rows"],
            "checker_child_env": observed, "log_derived": log_verdict,
            "log_errors": log_errors, "observed_ok": verdict["observed_ok"],
            "checker_stdout_tail": (res["stdout"] or "")[-600:],
            "work": work_abs, "contain_root": verdict["contain_root"],
            "log": checker_log}


def a11_verdict(rc: int, observed: dict, log_verdict: dict, shims: dict,
                work_abs: str) -> dict:
    """A11's decision as a pure function over the witnesses (selftest-bound).

    Every conjunct the wave's mutation probe could delete lives here, so a
    mutant that drops one fails `a11-arm-cases` in --selftest (R72-C2's rule
    applied to C1's arm).
    """
    observed = observed if isinstance(observed, dict) else {}
    run_root = observed.get("run_root")
    contain_root = run_root if isinstance(run_root, str) and run_root else work_abs
    shim_rows = {}
    for name, rec in (shims or {}).items():
        values = rec.get("values") or {}
        shim_rows[name] = {
            "recorded": bool(rec.get("recorded")),
            "keys_exact": bool(rec.get("keys_exact")),
            "canary_present": bool(rec.get("canary_present")),
            "home_under_run_root": bool(values)
            and under(contain_root, values.get("HOME", "")),
            "tmpdir_under_run_root": bool(values)
            and under(contain_root, values.get("TMPDIR", "")),
        }
    observed_ok = (log_verdict.get("ok") is True
                   and observed.get("records") == log_verdict.get("records")
                   and observed.get("all_allowlisted") is True
                   and observed.get("canary_present") is False
                   and observed.get("home_under_run") is True
                   and observed.get("tmpdir_under_run") is True
                   and observed.get("children") == log_verdict.get("children")
                   and isinstance(run_root, str) and bool(run_root)
                   and under(work_abs, run_root))
    ok = (rc == 0 and observed_ok
          and bool(shim_rows)
          and all(s["recorded"] and s["keys_exact"] and not s["canary_present"]
                  and s["home_under_run_root"] and s["tmpdir_under_run_root"]
                  for s in shim_rows.values()))
    return {"ok": ok, "observed_ok": observed_ok,
            "contain_root": contain_root, "shim_rows": shim_rows}


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
          expect_upx: str | None, nonce_commitment: str | None = None,
          legacy_receipt: str | None = None,
          receipt_rev: str | None = None) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    scratch = tempfile.mkdtemp(prefix="seam-probe-", dir=work)
    instrument, blob_sha = blob_to(root, rev, tool, scratch)
    battery, battery_sha = blob_to(root, rev, battery_tool, scratch)
    # The receipt binds its producer at the revision it was produced at, which
    # may predate the instrument's own supersession commits; the checker reads
    # carrier sources at that revision too.  Default: the measured revision.
    rrev = receipt_rev or rev
    rblob_sha = blob_sha
    if rrev != rev:
        proc = subprocess.run(["git", "-C", root, "show", f"{rrev}:{tool}"],
                              capture_output=True)
        rblob_sha = (sha256_bytes(proc.stdout) if proc.returncode == 0
                     else None)
        if rblob_sha is None:
            raise Unevaluable(f"git show {rrev}:{tool} failed")
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
        receipt, defects = bind_producer(receipt_path, root, rrev, tool, rblob_sha)
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

    # A8 - the OBSERVED child environment (round-70 M70-6): a one-carrier run
    # records each child's own environ; the probe parses the raw JSONL itself,
    # never the builder's returned dict.
    a8_dir = tempfile.mkdtemp(prefix="a8-", dir=work)
    a8_log = os.path.join(a8_dir, "env.jsonl")
    a8_out = os.path.join(a8_dir, "a8.json")
    a8 = invoke(instrument, root, rev, pkg, a8_dir,
                ["--carriers", "jq", "--child-env-log", a8_log,
                 "--json-out", a8_out],
                extra_env={"KAIDOKU_ENV_CANARY": "probe-canary"})
    a8_receipt = None
    try:
        with open(a8_out, encoding="utf-8") as fh:
            a8_receipt = json.load(fh)
    except (OSError, json.JSONDecodeError):
        a8_receipt = None
    raw_records = []
    raw_ok = False
    try:
        with open(a8_log, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    raw_records.append(json.loads(line))
        raw_ok = bool(raw_records)
    except (OSError, json.JSONDecodeError):
        raw_ok = False
    run_root = (a8_receipt or {}).get("run_root")
    obs = (a8_receipt or {}).get("child_env_observed") or {}
    envs = [r.get("env") or {} for r in raw_records]
    children = sorted({os.path.basename(str((r.get("argv") or ["?"])[0]))
                       for r in raw_records})
    raw_allow = bool(envs) and all(sorted(e) == sorted(CHILD_ENV_KEYS) for e in envs)
    raw_home = bool(envs) and all(under(run_root, e.get("HOME", "")) for e in envs)
    raw_tmp = bool(envs) and all(under(run_root, e.get("TMPDIR", "")) for e in envs)
    raw_canary = any("KAIDOKU_ENV_CANARY" in e for e in envs)
    a8_ok = (a8["rc"] == 0 and raw_ok and raw_allow and raw_home and raw_tmp
             and not raw_canary and isinstance(run_root, str) and bool(run_root)
             and obs.get("records") == len(raw_records)
             and obs.get("all_allowlisted") is True
             and obs.get("canary_present") is False
             and obs.get("keys") == sorted(CHILD_ENV_KEYS)
             and {"upx", "node", "readelf"} <= set(children))
    arms.append(arm("A8_child_env_observed", a8_ok,
                    {"rc": a8["rc"], "records": len(raw_records),
                     "children": children, "raw_allowlisted": raw_allow,
                     "raw_home_under_run": raw_home,
                     "raw_tmpdir_under_run": raw_tmp,
                     "raw_canary_present": raw_canary,
                     "receipt_observed": obs, "run_root": run_root}))

    # A9 - concurrent scratch isolation: three batteries and three route
    # preflights started together on one --work parent never collide.
    a9_dir = tempfile.mkdtemp(prefix="a9-", dir=work)
    base_env = {"PATH": os.environ.get("PATH", "/usr/bin"),
                "LANG": os.environ.get("LANG", "C"),
                "HOME": os.environ.get("HOME", "/nonexistent")}
    bat_procs = []
    for _ in range(3):
        bat_procs.append(subprocess.Popen(
            [sys.executable, "-I", "-B", battery, "--root", root, "--rev", rev,
             "--tool", tool, "--work", a9_dir, "--patch-set", "r70",
             "--min-pristine-cases", "0"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env=base_env))
    bat_results = []
    for proc in bat_procs:
        out, _err = proc.communicate(timeout=1800)
        payload = None
        for chunk in [out.strip()] + [x.strip() for x in out.splitlines()[::-1]]:
            if not chunk:
                continue
            try:
                payload = json.loads(chunk)
                break
            except json.JSONDecodeError:
                continue
        bat_results.append({"rc": proc.returncode,
                            "work_dir": (payload or {}).get("work_dir")})
    route_procs = []
    route_paths = []
    for i in range(3):
        log_name = "env-%d.jsonl" % i
        out_i = os.path.join(a9_dir, "route-%d.json" % i)
        route_paths.append((log_name, out_i))
        route_procs.append(subprocess.Popen(
            [sys.executable, "-I", "-B", instrument, "--root", root, "--rev", rev,
             "--pkg", pkg, "--work", a9_dir, "--skip-run",
             "--child-env-log", log_name, "--json-out", out_i],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            env=base_env))
    route_results = []
    for proc, (log_name, out_i) in zip(route_procs, route_paths):
        proc.communicate(timeout=1800)
        payload = None
        try:
            with open(out_i, encoding="utf-8") as fh:
                payload = json.load(fh)
        except (OSError, json.JSONDecodeError):
            payload = None
        rr = (payload or {}).get("run_root")
        obs_i = (payload or {}).get("child_env_observed") or {}
        log_path = obs_i.get("log")
        records = []
        try:
            with open(log_path, encoding="utf-8") as fh:
                records = [json.loads(line) for line in fh if line.strip()]
        except (OSError, TypeError, json.JSONDecodeError):
            records = []
        envs_i = [r.get("env") or {} for r in records]
        route_results.append({
            "rc": proc.returncode, "run_root": rr, "records": len(records),
            "log": log_path,
            "log_under_run": (isinstance(rr, str) and isinstance(log_path, str)
                              and under(rr, log_path)),
            "own_home": bool(envs_i) and isinstance(rr, str) and all(
                under(rr, e.get("HOME", "")) for e in envs_i),
            "own_tmp": bool(envs_i) and isinstance(rr, str) and all(
                under(rr, e.get("TMPDIR", "")) for e in envs_i),
            "own_keys": bool(envs_i) and all(
                sorted(e) == sorted(CHILD_ENV_KEYS) for e in envs_i),
            "verdict_claimed": (payload or {}).get("verdict_claimed")})
    bat_dirs = [r["work_dir"] for r in bat_results]
    route_roots = [r["run_root"] for r in route_results]
    a9_ok = (all(r["rc"] == 0 for r in bat_results)
             and all(isinstance(d, str) and d.startswith(os.path.abspath(a9_dir))
                     for d in bat_dirs)
             and len(set(bat_dirs)) == 3
             and all(r["rc"] == 1 and r["verdict_claimed"] is False
                     and r["records"] >= 1 and r["own_home"] and r["own_tmp"]
                     and r["own_keys"] and r["log_under_run"]
                     and isinstance(r["run_root"], str)
                     and r["run_root"].startswith(os.path.abspath(a9_dir))
                     for r in route_results)
             and len(set(route_roots)) == 3)
    arms.append(arm("A9_concurrent_collision", a9_ok,
                    {"battery": bat_results, "route": route_results,
                     "distinct_battery_dirs": len(set(bat_dirs)),
                     "distinct_run_roots": len(set(route_roots))}))

    # A10 - pre-committed run binding, verdict read from the CHECKER's JSON
    # (R72-C2: the probe no longer re-derives binding_ok from the receipt).
    if receipt_path and nonce_commitment:
        receipt, defects = bind_producer(receipt_path, root, rrev, tool, rblob_sha)
        genuine = invoke(instrument, root, rrev, pkg, work,
                         ["--check-receipt", receipt_path,
                          "--nonce-commitment", nonce_commitment])
        genuine_json = parse_json_out(genuine["stdout"])
        genuine_verdict = binding_verdict(genuine_json)
        genuine_met = checker_met(genuine_json)
        fail_modes = {}
        base_dir = tempfile.mkdtemp(prefix="a10-", dir=work)
        wrong = json.loads(json.dumps(receipt or {}))
        if isinstance(wrong.get("run_nonce"), str) and len(wrong["run_nonce"]) == 64:
            flip = "0" if wrong["run_nonce"][0] != "0" else "1"
            wrong["run_nonce"] = flip + wrong["run_nonce"][1:]
        wrong_path = os.path.join(base_dir, "wrong-nonce.json")
        with open(wrong_path, "w", encoding="utf-8") as fh:
            json.dump(wrong, fh)
        broke = json.loads(json.dumps(receipt or {}))
        broke["run_binding"] = "00" * 32
        broke_path = os.path.join(base_dir, "broken-binding.json")
        with open(broke_path, "w", encoding="utf-8") as fh:
            json.dump(broke, fh)
        for label, path in (("wrong_nonce", wrong_path),
                            ("broken_binding", broke_path)):
            res = invoke(instrument, root, rrev, pkg, work,
                         ["--check-receipt", path,
                          "--nonce-commitment", nonce_commitment])
            verdict = binding_verdict(parse_json_out(res["stdout"]))
            fail_modes[label] = {"rc": res["rc"], **verdict}
        if legacy_receipt:
            res = invoke(instrument, root, rrev, pkg, work,
                         ["--check-receipt", legacy_receipt,
                          "--nonce-commitment", nonce_commitment])
            fail_modes["legacy"] = {"rc": res["rc"],
                                    **binding_verdict(
                                        parse_json_out(res["stdout"]))}
        a10_ok = (not defects
                  and genuine_met is True
                  and genuine_verdict["present"] is True
                  and genuine_verdict["nonce_ok"] is True
                  and genuine_verdict["binding_ok"] is True
                  and genuine["rc"] == 0
                  and fail_modes.get("wrong_nonce", {}).get("rc") == 1
                  and fail_modes.get("wrong_nonce", {}).get("nonce_ok") is False
                  and fail_modes.get("broken_binding", {}).get("rc") == 1
                  and fail_modes.get("broken_binding", {}).get("binding_ok") is False
                  and (not legacy_receipt
                       or (fail_modes.get("legacy", {}).get("rc") == 1
                           and fail_modes.get("legacy", {}).get("nonce_ok") is False)))
        arms.append(arm("A10_run_binding", a10_ok,
                        {"defects": defects,
                         "genuine_met": genuine_met,
                         "genuine_verdict": genuine_verdict,
                         "genuine_rc": genuine["rc"],
                         "fail_modes": fail_modes,
                         "commitment": nonce_commitment}))
        # A11 - the checker-mode children run under the same allowlist
        # (R72-C1: this was the round-71 note's Frontier line).
        a11 = checker_env_arm(instrument, root, rrev, pkg, work,
                              receipt_path, nonce_commitment)
        arms.append(arm("A11_checker_env", a11["ok"], a11))
    else:
        arms.append(arm("A10_run_binding", False,
                        {"missing": "no --receipt or no --nonce-commitment"}))
        arms.append(arm("A11_checker_env", False,
                        {"missing": "no --receipt or no --nonce-commitment"}))

    failed = [a["id"] for a in arms if not a["ok"]]
    return {"instrument": tool, "rev": rev, "battery": battery_tool,
            "receipt": receipt_path, "expect_upx": expect_upx,
            "instrument_sha256": blob_sha, "battery_sha256": battery_sha,
            "arms": arms, "arms_passed": len(arms) - len(failed),
            "target": len(arms), "failed": failed, "ok": not failed,
            "scratch": scratch}


def validate_defects(receipt: dict) -> list[str]:
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
    return defects


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": "seam-probe-receipt", "unevaluable": str(exc)}))
        return 2
    if not isinstance(receipt, dict):
        print(json.dumps({"validate": "seam-probe-receipt",
                          "unevaluable": f"receipt root is {type(receipt).__name__}, "
                                        f"not an object"}))
        return 2
    defects = validate_defects(receipt)
    arms = receipt.get("arms") if isinstance(receipt.get("arms"), list) else []
    out = {"validate": "seam-probe-receipt", "path": path, "ok": not defects,
           "defects": defects, "arms": len(arms)}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not defects else 1


def selftest() -> int:
    cases = {}

    def receipt(ids, ok_flags, observed=True):
        return {"arms": [{"id": i, "ok": f,
                          "observed": ({"x": 1} if observed else {})}
                         for i, f in zip(ids, ok_flags)],
                "arms_passed": sum(1 for f in ok_flags if f),
                "target": len(ids),
                "failed": [i for i, f in zip(ids, ok_flags) if not f]}

    good = receipt(["A1", "A2"], [True, False])
    cases["validate-clean"] = validate_defects(good) == []
    cases["validate-no-observation"] = (
        validate_defects(receipt(["A1"], [True], observed=False))
        == ["A1: no observation"])
    bad_pass = dict(good)
    bad_pass["arms_passed"] = 2
    cases["validate-pass-mismatch"] = (
        "arms_passed disagrees with the arm rows" in validate_defects(bad_pass))
    bad_failed = dict(good)
    bad_failed["failed"] = []
    cases["validate-failed-mismatch"] = (
        "failed disagrees with the arm rows" in validate_defects(bad_failed))
    bad_target = dict(good)
    bad_target["target"] = 7
    cases["validate-target-mismatch"] = (
        "target 7 != arm rows 2" in validate_defects(bad_target))
    cases["parse-unevaluable"] = (
        parse_unevaluable("", '{"unevaluable": "missing_tool: upx"}')
        == {"unevaluable": "missing_tool: upx"})
    cases["parse-json-out"] = parse_json_out('{"ok": true}\n') == {"ok": True}
    cases["containment-descendant"] = under("/w/run", "/w/run/home") is True
    cases["containment-sibling-prefix"] = under("/w/run", "/w/run-outside/home") is False
    cases["a10-binding-from-checker"] = (
        binding_verdict({"clauses": {"run_nonce": True, "run_binding": True}})
        == {"present": True, "nonce_ok": True, "binding_ok": True}
        and binding_verdict({"clauses": {"run_nonce": True,
                                         "run_binding": False}})["binding_ok"] is False
        and binding_verdict({})["present"] is False
        and binding_verdict({"clauses": {"run_nonce": True}})["binding_ok"] is False)
    clean = {"HOME": "/r/home", "LANG": "C", "PATH": "/usr/bin", "TMPDIR": "/r/tmp"}
    git = {"argv": ["/usr/bin/git", "show"], "env": dict(clean)}
    readelf = {"argv": ["/usr/bin/readelf", "-h"], "env": dict(clean)}
    cases["a11-log-census"] = (
        checker_log_verdict([])["ok"] is False
        and checker_log_verdict([git])["ok"] is False
        and checker_log_verdict([git, readelf])["ok"] is True
        and checker_log_verdict([git, readelf])["children"] == {"git": 1, "readelf": 1}
        and checker_log_verdict(
            [git, {**readelf, "env": {**clean, "KAIDOKU_ENV_CANARY": "x"}}])["ok"] is False
        and checker_log_verdict(
            [git, {**readelf, "env": {**clean, "EXTRA": "1"}}])["ok"] is False)
    run_home = {"HOME": "/w/root/home", "LANG": "C", "PATH": "/usr/bin",
                "TMPDIR": "/w/root/tmp"}
    log_v = {"ok": True, "records": 2, "children": {"git": 1, "readelf": 1}}
    obs_v = {"records": 2, "all_allowlisted": True, "canary_present": False,
             "home_under_run": True, "tmpdir_under_run": True,
             "children": {"git": 1, "readelf": 1}, "run_root": "/w/root"}

    def shim(values, keys_exact=True, canary=False):
        return {"recorded": True, "keys_exact": keys_exact,
                "canary_present": canary, "values": values}

    good_shims = {"git": shim(run_home), "readelf": shim(run_home)}
    cases["a11-arm-cases"] = (
        a11_verdict(0, obs_v, log_v, good_shims, "/w")["ok"] is True
        and a11_verdict(1, obs_v, log_v, good_shims, "/w")["ok"] is False
        and a11_verdict(0, obs_v, {**log_v, "children": {"git": 0, "readelf": 1}},
                        good_shims, "/w")["ok"] is False
        and a11_verdict(0, {**obs_v, "children": {"git": 0, "readelf": 1}},
                        log_v, good_shims, "/w")["ok"] is False
        and a11_verdict(0, obs_v, log_v,
                        {"git": shim(run_home, keys_exact=False),
                         "readelf": shim(run_home)}, "/w")["ok"] is False
        and a11_verdict(0, obs_v, log_v,
                        {"git": shim(run_home, canary=True),
                         "readelf": shim(run_home)}, "/w")["ok"] is False
        and a11_verdict(0, obs_v, log_v,
                        {"git": shim({**run_home, "HOME": "/w/root-out/home"}),
                         "readelf": shim(run_home)}, "/w")["ok"] is False
        and a11_verdict(0, obs_v, log_v,
                        {"git": shim({**run_home, "TMPDIR": "/elsewhere"}),
                         "readelf": shim(run_home)}, "/w")["ok"] is False
        and a11_verdict(0, {}, log_v, good_shims, "/w")["ok"] is False)
    cases["a10-met-consistency"] = (
        checker_met({"met": True, "clauses": {"met": True}}) is True
        and checker_met({"met": False, "clauses": {"met": True}}) is False
        and checker_met({"met": True, "clauses": {"run_binding": True}}) is False
        and checker_met({}) is False)
    print(json.dumps({"selftest": "tools/round-72/seam-probe.py",
                      "cases": len(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


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
    ap.add_argument("--nonce-commitment")
    ap.add_argument("--legacy-receipt")
    ap.add_argument("--receipt-rev")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        return validate(args.validate)
    if not (args.root and args.rev and args.tool and args.battery
            and args.pkg and args.work):
        print("seam-probe: --root, --rev, --tool, --battery, --pkg and --work "
              "are required", file=sys.stderr)
        return 2
    try:
        receipt = check(args.root, args.rev, args.tool, args.pkg, args.work,
                        args.battery, args.receipt, args.expect_upx,
                        args.nonce_commitment, args.legacy_receipt,
                        args.receipt_rev)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r72-seam-probe-v1",
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
