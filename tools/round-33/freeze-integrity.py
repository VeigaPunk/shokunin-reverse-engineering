#!/usr/bin/env python3
"""Round-33 selftest extension of the preserved Round-32 freeze-integrity gate: tools/round-31/freeze-integrity.py (mistake M31-2) plus a
`--claims` option, because round 32 holds two freeze files: claims.json (R32-C1 and the
superseded C2 v1, freeze 9a73680a) and claims-v2.json (R32-C2 v2, which supersedes C2 v1
before any seat or data scored it).

This gate reads Git objects only.  It finds the freeze commit (the first commit reachable
from --rev that adds the claims file), reads the `instruments` and `frozen_inputs` digests
from the claims file AT THE FREEZE COMMIT, and requires every pinned path at --rev to hash to
that digest and to have no commit touching it in freeze..rev.

  python3 -I -B tools/round-33/freeze-integrity.py --root <LANE> --round <N> [--claims <rel>] [--rev <REV>]
  python3 -I -B tools/round-33/freeze-integrity.py --selftest

Prints one line per pin and `freeze-integrity: CLEAN pins=K` (exit 0) or
`freeze-integrity: FAIL ...` (exit 1); exit 2 when the freeze commit is absent.

--selftest builds five disposable Git fixtures only under
/fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest, runs this file as a subprocess against
each, and checks the gate's exit codes and predicate lines: clean pinned tree 0; committed
tamper 1; tamper-then-restore 1; absent claims 2; missing pinned file 1.  --selftest takes no
--root/--round and never writes to the lane.
"""

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

SELFTEST_BASE = "/fast/scratch/hyaku/kaidoku-r33/R33FreezeSelftest"
_SELFTEST_ROUND = "99"
_SELFTEST_CLAIMS = ".ufo/waves/round-%s/claims.json" % _SELFTEST_ROUND
_SELFTEST_ID = (
    "-c", "user.name=freeze-selftest",
    "-c", "user.email=freeze-selftest@example.invalid",
    "-c", "commit.gpgsign=false",
    "-c", "core.hooksPath=/nonexistent-freeze-selftest-hooks",
)
_SELFTEST_ENV_DROP = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")


def git(root, *args, binary=False):
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
    p = subprocess.run(["git", "-C", root] + list(args), capture_output=True, env=env)
    return p.returncode, (p.stdout if binary else p.stdout.decode())


def _selftest_git(root, *args):
    rc, out = git(root, *args)
    if rc != 0:
        raise RuntimeError("fixture git failed rc=%d args=%r out=%r" % (rc, args, out.strip()[:300]))
    return out


def _selftest_commit(root, message):
    _selftest_git(root, "add", "-A")
    _selftest_git(root, *_SELFTEST_ID, "commit", "-q", "--no-gpg-sign", "-m", message)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _write(root, rel, data):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def _claims(instruments, frozen_inputs):
    return json.dumps({"instruments": instruments, "frozen_inputs": frozen_inputs}, sort_keys=True).encode()


def _fixture(base, name):
    root = tempfile.mkdtemp(prefix="fixture-%s-" % name, dir=base)
    try:
        _selftest_git(root, "init", "-q")
    except Exception:
        shutil.rmtree(root, ignore_errors=True)
        raise
    return root


def _drop(root):
    shutil.rmtree(root, ignore_errors=True)


def _check(cond, message):
    if not cond:
        raise RuntimeError(message)


def _run_gate(root, timeout=120):
    argv = [sys.executable, "-I", "-B", os.path.abspath(__file__), "--root", root, "--round", _SELFTEST_ROUND]
    env = {k: v for k, v in os.environ.items() if k not in _SELFTEST_ENV_DROP}
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            env=env, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, err = proc.communicate()
        raise RuntimeError("gate timed out after %ss root=%s" % (timeout, root))
    return proc.returncode, out, err


def _case_clean(base):
    root = _fixture(base, "clean")
    try:
        payload = b"instrument-v1\n"
        pinned = b"pinned-data-v1\n"
        _write(root, "bin/tool.py", payload)
        _write(root, "data/pins.json", pinned)
        _write(root, _SELFTEST_CLAIMS, _claims({"bin/tool.py": _sha(payload)}, {"data/pins.json": _sha(pinned)}))
        _selftest_commit(root, "freeze: add claims")
        freeze = _selftest_git(root, "rev-parse", "HEAD").strip()
        _write(root, "notes.txt", b"unrelated\n")
        _selftest_commit(root, "unrelated note")
        rc, out, err = _run_gate(root)
        _check(rc == 0, "expected exit 0, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        _check("freeze-integrity: CLEAN pins=2" in out, "missing CLEAN pins=2: %r" % out)
        _check("ok\tbin/tool.py\tsha=%s\tcommits_after_freeze=0" % _sha(payload)[:12] in out,
               "tool pin not clean: %r" % out)
        _check("ok\tdata/pins.json\tsha=%s\tcommits_after_freeze=0" % _sha(pinned)[:12] in out,
               "data pin not clean: %r" % out)
        return "freeze=%s pins=2 exit=0" % freeze[:12]
    finally:
        _drop(root)


def _case_tampered(base):
    root = _fixture(base, "tampered")
    try:
        payload = b"instrument-v1\n"
        tampered = b"instrument-TAMPERED\n"
        _write(root, "bin/tool.py", payload)
        _write(root, _SELFTEST_CLAIMS, _claims({"bin/tool.py": _sha(payload)}, {}))
        _selftest_commit(root, "freeze: add claims")
        _write(root, "bin/tool.py", tampered)
        _selftest_commit(root, "tamper: rewrite pinned instrument")
        rc, out, err = _run_gate(root)
        _check(rc == 1, "expected exit 1, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        _check("freeze-integrity: FAIL pins=1 changed=1" in out, "missing FAIL summary: %r" % out)
        _check("FAIL\tbin/tool.py\tsha=%s" % _sha(tampered)[:12] in out, "missing tampered digest line: %r" % out)
        return "exit=1 changed=1 sha=%s" % _sha(tampered)[:12]
    finally:
        _drop(root)


def _case_restored(base):
    root = _fixture(base, "restored")
    try:
        payload = b"instrument-v1\n"
        tampered = b"instrument-TAMPERED\n"
        _write(root, "bin/tool.py", payload)
        _write(root, _SELFTEST_CLAIMS, _claims({"bin/tool.py": _sha(payload)}, {}))
        _selftest_commit(root, "freeze: add claims")
        _write(root, "bin/tool.py", tampered)
        _selftest_commit(root, "tamper: rewrite pinned instrument")
        _write(root, "bin/tool.py", payload)
        _selftest_commit(root, "restore: put original bytes back")
        rc, out, err = _run_gate(root)
        _check(rc == 1, "expected exit 1, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        lines = [line for line in out.splitlines() if line.startswith("FAIL\tbin/tool.py")]
        _check(len(lines) == 1, "expected one FAIL line for bin/tool.py: %r" % out)
        _check("sha=%s" % _sha(payload)[:12] in lines[0], "restored bytes must match pin: %r" % lines[0])
        _check("commits_after_freeze=0" not in lines[0], "restore commit must still fail: %r" % lines[0])
        _check("freeze-integrity: FAIL pins=1 changed=1" in out, "missing FAIL summary: %r" % out)
        return "exit=1 digest_matches history_flagged %s" % lines[0].split("\t")[-1]
    finally:
        _drop(root)


def _case_absent_claims(base):
    root = _fixture(base, "absent-claims")
    try:
        _write(root, "README.txt", b"no claims committed here\n")
        _selftest_commit(root, "initial without claims")
        rc, out, err = _run_gate(root)
        _check(rc == 2, "expected exit 2, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        _check("ERROR no commit adds %s at HEAD" % _SELFTEST_CLAIMS in out,
               "missing absent-claims error: %r" % out)
        return "exit=2 claims=%s absent" % _SELFTEST_CLAIMS
    finally:
        _drop(root)


def _case_missing_pin(base):
    root = _fixture(base, "missing-pin")
    try:
        _write(root, _SELFTEST_CLAIMS, _claims({"bin/missing.py": "0" * 64}, {}))
        _selftest_commit(root, "freeze: claims pin a path that never existed")
        rc, out, err = _run_gate(root)
        _check(rc == 1, "expected exit 1, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        _check("FAIL\tbin/missing.py\tsha=absent" in out, "missing absent-pin line: %r" % out)
        _check("freeze-integrity: FAIL pins=1 changed=1" in out, "missing FAIL summary: %r" % out)
        return "exit=1 sha=absent changed=1"
    finally:
        _drop(root)


def selftest():
    os.makedirs(SELFTEST_BASE, exist_ok=True)
    cases = (
        ("clean", _case_clean),
        ("tampered_pin", _case_tampered),
        ("restored_after_change", _case_restored),
        ("absent_claims", _case_absent_claims),
        ("missing_pinned_file", _case_missing_pin),
    )
    failures = []
    started = time.monotonic()
    for name, fn in cases:
        try:
            detail = fn(SELFTEST_BASE)
        except Exception as exc:
            failures.append(name)
            print("case %s: FAIL %s" % (name, exc))
        else:
            print("case %s: PASS %s" % (name, detail))
    elapsed = time.monotonic() - started
    if failures:
        print("freeze-integrity-selftest: FAIL cases=%d failed=%s elapsed_s=%.2f"
              % (len(cases), ",".join(failures), elapsed))
        return 1
    print("freeze-integrity-selftest: PASS cases=%d elapsed_s=%.2f base=%s"
          % (len(cases), elapsed, SELFTEST_BASE))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--round")
    ap.add_argument("--claims", default=None)
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--selftest", action="store_true",
                    help="run disposable-fixture self-tests and exit; no --root/--round needed")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.root or not a.round:
        ap.error("--root and --round are required unless --selftest is given")
    claims = a.claims or ".ufo/waves/round-%s/claims.json" % a.round
    rc, out = git(a.root, "log", "--format=%H", "--diff-filter=A", a.rev, "--", claims)
    commits = out.split()
    if rc != 0 or not commits:
        print("freeze-integrity: ERROR no commit adds %s at %s" % (claims, a.rev))
        return 2
    freeze = commits[-1]
    rc, text = git(a.root, "show", "%s:%s" % (freeze, claims))
    pins = {}
    for key in ("instruments", "frozen_inputs"):
        pins.update(json.loads(text).get(key, {}))
    bad = 0
    for path, digest in sorted(pins.items()):
        rc, blob = git(a.root, "show", "%s:%s" % (a.rev, path), binary=True)
        got = hashlib.sha256(blob).hexdigest() if rc == 0 else "absent"
        rc2, touched = git(a.root, "log", "--format=%h", "%s..%s" % (freeze, a.rev), "--", path)
        touched = touched.split()
        ok = got == digest and not touched
        bad += not ok
        print("%s\t%s\tsha=%s\tcommits_after_freeze=%s" % ("ok" if ok else "FAIL", path, got[:12],
                                                          ",".join(touched) or "0"))
    if bad:
        print("freeze-integrity: FAIL pins=%d changed=%d freeze=%s rev=%s" % (len(pins), bad, freeze[:12], a.rev))
        return 1
    print("freeze-integrity: CLEAN pins=%d freeze=%s rev=%s" % (len(pins), freeze[:12], a.rev))
    return 0


if __name__ == "__main__":
    sys.exit(main())
