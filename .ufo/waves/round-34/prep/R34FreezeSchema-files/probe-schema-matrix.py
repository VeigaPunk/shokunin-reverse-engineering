#!/usr/bin/env python3
"""Bounded old-red/new-green matrix for the round-34 freeze-integrity schema successor.

For each claims shape it runs, as a subprocess, the untouched round-33 instrument
(tools/round-33/freeze-integrity.py) and the round-34 successor copy against the same
single-commit fixture repository:

  * the seven WFreezeMalformed survivors (empty/malformed pin maps) -- old must be
    falsely CLEAN (red), new must exit 3 with the frozen schema code (green);
  * four valid historical shapes (single pin, instruments-only as in rounds 24-29,
    empty frozen_inputs as in round-32 v2/v3, 4/4 as in round-32 claims.json) -- old and
    new must both be CLEAN with the same pin count.

It then runs the successor's --selftest and requires its frozen PASS line.

Bounds: 60 s per command, 300 s overall alarm, child RLIMIT_AS 256 MiB, RLIMIT_CPU 60 s,
RLIMIT_FSIZE 1 MiB, RLIMIT_CORE 0, RLIMIT_NOFILE 128; process groups are SIGKILLed on
timeout.  Fixtures live under /fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaProbe.* and
are removed before exit.  Writes only the --out directory and that scratch tree.
"""

import argparse
import datetime
import hashlib
import json
import os
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OLD_GATE = os.path.join(LANE, "tools/round-33/freeze-integrity.py")
NEW_GATE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "freeze-integrity.py"))
SCRATCH_ROOT = "/fast/scratch/hyaku/kaidoku-r34"
ROUND = "99"
CLAIMS_REL = ".ufo/waves/round-%s/claims.json" % ROUND
ENV_DROP = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")
GIT_ID = (
    "-c", "user.name=freeze-probe",
    "-c", "user.email=freeze-probe@example.invalid",
    "-c", "commit.gpgsign=false",
    "-c", "core.hooksPath=/nonexistent-freeze-probe-hooks",
)
COMMAND_TIMEOUT = 60.0
OVERALL_ALARM = 300


class ProbeFailure(RuntimeError):
    pass


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _env():
    env = {k: v for k, v in os.environ.items() if k not in ENV_DROP}
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env


def _limits():
    resource.setrlimit(resource.RLIMIT_AS, (256 << 20, 256 << 20))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1 << 20, 1 << 20))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))


def _run(argv, timeout=COMMAND_TIMEOUT):
    record = {"argv": argv, "start_utc": _utc()}
    started = time.monotonic()
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            env=_env(), start_new_session=True, preexec_fn=_limits)
    timed_out = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, err = proc.communicate()
    finally:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    record.update({"end_utc": _utc(), "duration_s": round(time.monotonic() - started, 6),
                   "exit": proc.returncode, "timed_out": timed_out,
                   "stdout": out, "stderr": err})
    return record


def _git(root, *args):
    proc = subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True,
                          env=_env(), timeout=30)
    if proc.returncode != 0:
        raise ProbeFailure("fixture git failed rc=%d args=%r stderr=%r"
                           % (proc.returncode, args, proc.stderr.strip()[:300]))
    return proc.stdout


def payload(rel):
    return b"probe-payload:" + rel.encode() + b"\n"


def digest(rel):
    return hashlib.sha256(payload(rel)).hexdigest()


def claims_bytes(doc):
    if isinstance(doc, bytes):
        return doc
    return json.dumps(doc, sort_keys=True).encode()


def _fixture(base, name, doc, files):
    root = tempfile.mkdtemp(prefix="fixture-%s-" % name, dir=base)
    try:
        _git(root, "init", "-q")
        for rel in files:
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(payload(rel))
        with open(os.path.join(root, "README.txt"), "wb") as fh:
            fh.write(b"inert readme\n")
        claims_path = os.path.join(root, CLAIMS_REL)
        os.makedirs(os.path.dirname(claims_path), exist_ok=True)
        with open(claims_path, "wb") as fh:
            fh.write(claims_bytes(doc))
        _git(root, "add", "-A")
        _git(root, *GIT_ID, "commit", "-q", "--no-gpg-sign", "-m", "freeze: add claims")
        return root
    except Exception:
        shutil.rmtree(root, ignore_errors=True)
        raise


def _definitions():
    a, b, c, d = "artifact.txt", "data/one.json", "data/two.bin", "bin/run.sh"
    inputs = ("in-1.json", "in-2.json", "in-3.txt", "in-4.bin")
    sha = {rel: digest(rel) for rel in (a, b, c, d) + tuple("data/" + rel for rel in inputs)}
    malformed = (
        ("empty_maps", {"frozen_inputs": {}, "instruments": {}}, {a: sha[a]}, "instruments_empty"),
        ("omitted_instruments", {"frozen_inputs": {}}, {a: sha[a]}, "instruments_missing"),
        ("no_pin_keys", {}, {}, "instruments_missing"),
        ("empty_list_map", {"frozen_inputs": {}, "instruments": []}, {}, "instruments_not_object"),
        ("empty_string_map", {"frozen_inputs": {}, "instruments": ""}, {}, "instruments_not_object"),
        ("pair_list_map", {"frozen_inputs": {}, "instruments": [[a, sha[a]]]}, {a: sha[a]},
         "instruments_not_object"),
        ("empty_list_frozen_inputs", {"frozen_inputs": [], "instruments": {a: sha[a]}}, {a: sha[a]},
         "frozen_inputs_not_object"),
    )
    valid = (
        ("valid_single_pin", {"instruments": {a: sha[a]}, "frozen_inputs": {}}, {a: sha[a]}, 1),
        ("valid_instruments_only", {"instruments": {a: sha[a]}}, {a: sha[a]}, 1),
        ("valid_empty_frozen_2", {"instruments": {a: sha[a], b: sha[b]}, "frozen_inputs": {}},
         {a: sha[a], b: sha[b]}, 2),
        ("valid_round32_4_4",
         {"instruments": {a: sha[a], b: sha[b], c: sha[c], d: sha[d]},
          "frozen_inputs": {"data/" + rel: sha["data/" + rel] for rel in inputs}},
         {a: sha[a], b: sha[b], c: sha[c], d: sha[d],
          **{"data/" + rel: sha["data/" + rel] for rel in inputs}},
         8),
    )
    return malformed, valid


def _check_outcome(record, shape, gate, is_malformed, expected_code, expected_pins):
    if record["timed_out"]:
        raise ProbeFailure("%s/%s timed out" % (shape, gate))
    if record["stderr"].strip():
        raise ProbeFailure("%s/%s wrote stderr: %r" % (shape, gate, record["stderr"].strip()[:300]))
    out = record["stdout"]
    if is_malformed:
        if gate == "old":
            if record["exit"] != 0 or "freeze-integrity: CLEAN" not in out:
                raise ProbeFailure("%s/old was not falsely CLEAN: exit=%d out=%r"
                                   % (shape, record["exit"], out[:300]))
            return "red"
        if record["exit"] != 3:
            raise ProbeFailure("%s/new expected exit 3 got %d out=%r" % (shape, record["exit"], out[:300]))
        if "freeze-integrity: ERROR schema code=%s" % expected_code not in out:
            raise ProbeFailure("%s/new missing code %s: %r" % (shape, expected_code, out[:300]))
        if "freeze-integrity: CLEAN" in out or "ok\t" in out:
            raise ProbeFailure("%s/new printed CLEAN/ok on schema reject: %r" % (shape, out[:300]))
        return "green"
    expected = "freeze-integrity: CLEAN pins=%d" % expected_pins
    if record["exit"] != 0 or expected not in out:
        raise ProbeFailure("%s/%s expected %r exit=0, got exit=%d out=%r"
                           % (shape, gate, expected, record["exit"], out[:300]))
    return "green"


def run(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(SCRATCH_ROOT, exist_ok=True)
    base = tempfile.mkdtemp(prefix="R34FreezeSchemaProbe.", dir=SCRATCH_ROOT)
    malformed, valid = _definitions()
    old_before, new_before = _sha_file(OLD_GATE), _sha_file(NEW_GATE)
    receipt = {
        "driver_argv": sys.argv,
        "driver_start_utc": _utc(),
        "python": sys.version.split()[0],
        "git": subprocess.run(["git", "--version"], capture_output=True, text=True,
                              env=_env()).stdout.strip(),
        "lane": LANE,
        "old_gate": {"path": OLD_GATE, "sha256_before": old_before, "sha256_after": None},
        "new_gate": {"path": NEW_GATE, "sha256_before": new_before, "sha256_after": None},
        "scratch_base": base,
        "cases": [],
        "selftest": None,
        "errors": [],
    }
    try:
        for shape, doc, files, expected_code in malformed:
            root = _fixture(base, shape, doc, files)
            try:
                for gate, gate_path, code in (("old", OLD_GATE, expected_code), ("new", NEW_GATE, expected_code)):
                    rec = _run([sys.executable, "-I", "-B", gate_path,
                                "--root", root, "--round", ROUND])
                    verdict = _check_outcome(rec, shape, gate, True, code, 0)
                    receipt["cases"].append({"shape": shape, "class": "malformed", "gate": gate,
                                             "expected_code": code, "verdict": verdict, **rec})
            finally:
                shutil.rmtree(root, ignore_errors=True)
        for shape, doc, files, pins in valid:
            root = _fixture(base, shape, doc, files)
            try:
                for gate, gate_path in (("old", OLD_GATE), ("new", NEW_GATE)):
                    rec = _run([sys.executable, "-I", "-B", gate_path,
                                "--root", root, "--round", ROUND])
                    verdict = _check_outcome(rec, shape, gate, False, None, pins)
                    receipt["cases"].append({"shape": shape, "class": "valid", "gate": gate,
                                             "expected_pins": pins, "verdict": verdict, **rec})
            finally:
                shutil.rmtree(root, ignore_errors=True)
        st = _run([sys.executable, "-I", "-B", NEW_GATE, "--selftest"], timeout=180)
        if st["timed_out"] or st["exit"] != 0 or "freeze-integrity-selftest: PASS cases=25" not in st["stdout"]:
            raise ProbeFailure("new --selftest failed: exit=%r timed_out=%r stdout=%r stderr=%r"
                               % (st["exit"], st["timed_out"], st["stdout"][:600], st["stderr"][:600]))
        if st["stderr"].strip():
            raise ProbeFailure("new --selftest wrote stderr: %r" % st["stderr"].strip()[:300])
        receipt["selftest"] = {"gate": "new", **st}
    except Exception as exc:
        receipt["errors"].append("%s: %s" % (type(exc).__name__, exc))
    finally:
        old_after, new_after = _sha_file(OLD_GATE), _sha_file(NEW_GATE)
        receipt["old_gate"]["sha256_after"] = old_after
        receipt["new_gate"]["sha256_after"] = new_after
        receipt["driver_end_utc"] = _utc()
        receipt["scratch_removed"] = False
        shutil.rmtree(base, ignore_errors=True)
        receipt["scratch_removed"] = not os.path.exists(base)
    if old_before != receipt["old_gate"]["sha256_after"]:
        receipt["errors"].append("old gate bytes changed during probe")
    if new_before != receipt["new_gate"]["sha256_after"]:
        receipt["errors"].append("new gate bytes changed during probe")
    with open(os.path.join(out_dir, "receipt.json"), "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    lines = ["probe-schema-matrix: %s" % ("PASS" if not receipt["errors"] else "FAIL"),
             "old_gate_sha256=%s" % receipt["old_gate"]["sha256_before"],
             "new_gate_sha256=%s" % receipt["new_gate"]["sha256_before"]]
    for case in receipt["cases"]:
        lines.append("%-26s %-3s exit=%-2d %s" % (case["shape"], case["gate"], case["exit"],
                                                  case["verdict"]))
    if receipt["selftest"]:
        lines.append("selftest new exit=%d %s" % (receipt["selftest"]["exit"],
                                                  receipt["selftest"]["stdout"].strip().splitlines()[-1]))
    lines.extend("error: " + err for err in receipt["errors"])
    text = "\n".join(lines) + "\n"
    with open(os.path.join(out_dir, "receipt.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)
    return 0 if not receipt["errors"] else 1


def _alarm(signum, frame):
    raise ProbeFailure("overall alarm after %ss" % OVERALL_ALARM)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(OVERALL_ALARM)
    try:
        return run(a.out)
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    sys.exit(main())
