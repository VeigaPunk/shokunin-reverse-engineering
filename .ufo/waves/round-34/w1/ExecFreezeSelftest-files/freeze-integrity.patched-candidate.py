#!/usr/bin/env python3
"""Round-34 strict-schema successor of tools/round-33/freeze-integrity.py.

The preserved Round-33 instrument (family root: tools/round-31/freeze-integrity.py,
mistake M31-2) merged the two claims pin maps with `dict.get(key, {})` and
`dict.update(...)`.  A claims file carrying zero pins -- `{}`, `{"instruments": {}}`,
an empty list/string map, or a list of key/value pairs -- therefore printed
`freeze-integrity: CLEAN pins=0` (or `pins=1` for the coerced pair list) and exited 0.
WFreezeMalformed routed that boundary: seven empty or malformed map shapes survived as
falsely CLEAN.  This file keeps the byte-identical gate behaviour for valid claims files
and adds a strict schema gate for the two relied-upon pin maps before any pin is checked:

  * the claims document at the freeze commit MUST be a JSON object;
  * `instruments` MUST be present, a JSON object, and non-empty;
  * `frozen_inputs` MAY be absent (rounds 24-29 carry only `instruments`) but, if it is
    present, MUST be a JSON object; the empty object is valid (round-32 v2/v3 pin it);
  * every pin key MUST be a non-empty repo-relative path with no `..` segment and no NUL
    byte, and MUST NOT be pinned in both maps;
  * every pin digest MUST be exactly 64 lowercase hex characters.

  python3 -I -B freeze-integrity.py --root <LANE> --round <N> [--claims <rel>] [--rev <REV>]
  python3 -I -B freeze-integrity.py --selftest

Exit codes: 0 CLEAN, 1 FAIL (digest or history), 2 absent freeze commit, 3 claims schema
error.  A schema error never prints CLEAN or an `ok<TAB>` row; it prints
`freeze-integrity: ERROR schema code=<code> claims=<path> where=<detail>`.

--selftest builds disposable Git fixtures only under
/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaSelftest and asserts frozen exits and
findings for 25 cases: the five preserved round-33 cases, seventeen schema rejects (one
per WFreezeMalformed survivor plus ten adjacent shape/digest/path rejects), and three
historical-shape compatibility cases.  --selftest takes no --root/--round and never
writes to the lane.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

SELFTEST_BASE = "/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaSelftest"
_SELFTEST_ROUND = "99"
_SELFTEST_CLAIMS = ".ufo/waves/round-%s/claims.json" % _SELFTEST_ROUND
_SELFTEST_ID = (
    "-c", "user.name=freeze-selftest",
    "-c", "user.email=freeze-selftest@example.invalid",
    "-c", "commit.gpgsign=false",
    "-c", "core.hooksPath=/nonexistent-freeze-selftest-hooks",
)
_SELFTEST_ENV_DROP = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")
_DIGEST_RE = re.compile(r"[0-9a-f]{64}")

EXIT_CLEAN = 0
EXIT_FAIL = 1
EXIT_ABSENT_FREEZE = 2
EXIT_SCHEMA = 3


class SchemaError(Exception):
    def __init__(self, code, where="-"):
        super().__init__(code)
        self.code = code
        self.where = where


def _schema_fail(code, where="-"):
    raise SchemaError(code, where)


def _check_pin_path(key, map_name):
    if not key:
        _schema_fail("pin_key_empty", map_name)
    if key.startswith("/") or "\x00" in key or ".." in key.split("/"):
        _schema_fail("pin_path_not_relative", "%s:%s" % (map_name, key))


def load_pins(text):
    """Parse claims text and return the merged pin map, or raise SchemaError."""
    try:
        doc = json.loads(text)
    except ValueError:
        _schema_fail("claims_not_json")
    if not isinstance(doc, dict):
        _schema_fail("claims_not_object")
    if "instruments" not in doc:
        _schema_fail("instruments_missing", "instruments")
    instruments = doc["instruments"]
    if not isinstance(instruments, dict):
        _schema_fail("instruments_not_object", "instruments")
    if not instruments:
        _schema_fail("instruments_empty", "instruments")
    frozen_inputs = doc.get("frozen_inputs", {})
    if not isinstance(frozen_inputs, dict):
        _schema_fail("frozen_inputs_not_object", "frozen_inputs")
    pins = {}
    for map_name, mapping in (("instruments", instruments), ("frozen_inputs", frozen_inputs)):
        for key in sorted(mapping):
            if not isinstance(key, str):
                _schema_fail("pin_key_empty", map_name)
            _check_pin_path(key, map_name)
            digest = mapping[key]
            if not isinstance(digest, str) or _DIGEST_RE.fullmatch(digest) is None:
                _schema_fail("pin_digest_format", "%s:%s" % (map_name, key))
            if key in pins:
                _schema_fail("pin_path_duplicate", key)
            pins[key] = digest
    return pins


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


def _payload(rel):
    return b"pin-payload:" + rel.encode() + b"\n"


def _write(root, rel, data):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def _claims_doc(instruments, frozen_inputs=None, include_frozen=True):
    doc = {"instruments": instruments}
    if include_frozen:
        doc["frozen_inputs"] = {} if frozen_inputs is None else frozen_inputs
    return json.dumps(doc, sort_keys=True).encode()


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


# Frozen expected exits/findings for the schema-reject cases.  Each entry is
# (case name, claims bytes, expected exit, expected finding substring, write artifact).
_ARTIFACT = "artifact.txt"
_ARTIFACT_DIGEST = _sha(_payload(_ARTIFACT))
_SCHEMA_CASES = (
    # The seven WFreezeMalformed survivors, each with its own frozen case.
    ("schema_empty_instruments", _claims_doc({}, {}), EXIT_SCHEMA, "code=instruments_empty", False),
    ("schema_omitted_instruments", json.dumps({"frozen_inputs": {}}).encode(), EXIT_SCHEMA,
     "code=instruments_missing", False),
    ("schema_no_pin_keys", b"{}", EXIT_SCHEMA, "code=instruments_missing", False),
    ("schema_empty_list_instruments", b'{"instruments": [], "frozen_inputs": {}}', EXIT_SCHEMA,
     "code=instruments_not_object", False),
    ("schema_empty_string_instruments", b'{"instruments": "", "frozen_inputs": {}}', EXIT_SCHEMA,
     "code=instruments_not_object", False),
    ("schema_pair_list_instruments",
     b'{"instruments": [["' + _ARTIFACT.encode() + b'", "' + _ARTIFACT_DIGEST.encode() + b'"]], "frozen_inputs": {}}',
     EXIT_SCHEMA, "code=instruments_not_object", True),
    ("schema_empty_list_frozen_inputs", _claims_doc({_ARTIFACT: _ARTIFACT_DIGEST}, [], True), EXIT_SCHEMA,
     "code=frozen_inputs_not_object", True),
    # Adjacent non-object, digest, path and parse rejects; formerly tracebacks or FAILs.
    ("schema_null_instruments", b'{"instruments": null, "frozen_inputs": {}}', EXIT_SCHEMA,
     "code=instruments_not_object", False),
    ("schema_null_frozen_inputs",
     json.dumps({"instruments": {_ARTIFACT: _ARTIFACT_DIGEST}, "frozen_inputs": None}).encode(),
     EXIT_SCHEMA, "code=frozen_inputs_not_object", True),
    ("schema_bad_digest", _claims_doc({"bin/tool.py": "not-a-sha256"}, {}), EXIT_SCHEMA,
     "code=pin_digest_format", False),
    ("schema_absolute_pin", _claims_doc({"/bin/tool.py": _ARTIFACT_DIGEST}, {}), EXIT_SCHEMA,
     "code=pin_path_not_relative", False),
    ("schema_parent_pin", _claims_doc({"../bin/tool.py": _ARTIFACT_DIGEST}, {}), EXIT_SCHEMA,
     "code=pin_path_not_relative", False),
    ("schema_empty_pin_key", _claims_doc({"": _ARTIFACT_DIGEST}, {}), EXIT_SCHEMA,
     "code=pin_key_empty", False),
    ("schema_duplicate_pin", _claims_doc({_ARTIFACT: _ARTIFACT_DIGEST}, {_ARTIFACT: _ARTIFACT_DIGEST}),
     EXIT_SCHEMA, "code=pin_path_duplicate", True),
    ("schema_malformed_json", b'{"instruments":', EXIT_SCHEMA, "code=claims_not_json", False),
    ("schema_top_level_array", b"[]", EXIT_SCHEMA, "code=claims_not_object", False),
    ("schema_top_level_null", b"null", EXIT_SCHEMA, "code=claims_not_object", False),
)


def _case_clean(base):
    root = _fixture(base, "clean")
    try:
        payload = b"instrument-v1\n"
        pinned = b"pinned-data-v1\n"
        _write(root, "bin/tool.py", payload)
        _write(root, "data/pins.json", pinned)
        _write(root, _SELFTEST_CLAIMS, _claims_doc({"bin/tool.py": _sha(payload)}, {"data/pins.json": _sha(pinned)}))
        _selftest_commit(root, "freeze: add claims")
        freeze = _selftest_git(root, "rev-parse", "HEAD").strip()
        _write(root, "notes.txt", b"unrelated\n")
        _selftest_commit(root, "unrelated note")
        rc, out, err = _run_gate(root)
        _check(rc == EXIT_CLEAN, "expected exit 0, got %d (stderr=%r)" % (rc, err.strip()[:300]))
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
        _write(root, _SELFTEST_CLAIMS, _claims_doc({"bin/tool.py": _sha(payload)}, {}))
        _selftest_commit(root, "freeze: add claims")
        _write(root, "bin/tool.py", tampered)
        _selftest_commit(root, "tamper: rewrite pinned instrument")
        rc, out, err = _run_gate(root)
        _check(rc == EXIT_FAIL, "expected exit 1, got %d (stderr=%r)" % (rc, err.strip()[:300]))
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
        _write(root, _SELFTEST_CLAIMS, _claims_doc({"bin/tool.py": _sha(payload)}, {}))
        _selftest_commit(root, "freeze: add claims")
        _write(root, "bin/tool.py", tampered)
        _selftest_commit(root, "tamper: rewrite pinned instrument")
        _write(root, "bin/tool.py", payload)
        _selftest_commit(root, "restore: put original bytes back")
        rc, out, err = _run_gate(root)
        _check(rc == EXIT_FAIL, "expected exit 1, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        lines = [line for line in out.splitlines() if line.startswith("FAIL\tbin/tool.py")]
        _check(len(lines) == 1, "expected one FAIL line for bin/tool.py: %r" % out)
        _check("sha=%s" % _sha(payload)[:12] in lines[0], "restored bytes must match pin: %r" % lines[0])
        _field = lines[0].split("\t")[-1]
        _check(_field != "0" and _field != "", "restore commit must still fail: %r" % lines[0])
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
        _check(rc == EXIT_ABSENT_FREEZE, "expected exit 2, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        _check("ERROR no commit adds %s at HEAD" % _SELFTEST_CLAIMS in out,
               "missing absent-claims error: %r" % out)
        return "exit=2 claims=%s absent" % _SELFTEST_CLAIMS
    finally:
        _drop(root)


def _case_missing_pin(base):
    root = _fixture(base, "missing-pin")
    try:
        _write(root, _SELFTEST_CLAIMS, _claims_doc({"bin/missing.py": "0" * 64}, {}))
        _selftest_commit(root, "freeze: claims pin a path that never existed")
        rc, out, err = _run_gate(root)
        _check(rc == EXIT_FAIL, "expected exit 1, got %d (stderr=%r)" % (rc, err.strip()[:300]))
        _check("FAIL\tbin/missing.py\tsha=absent" in out, "missing absent-pin line: %r" % out)
        _check("freeze-integrity: FAIL pins=1 changed=1" in out, "missing FAIL summary: %r" % out)
        return "exit=1 sha=absent changed=1"
    finally:
        _drop(root)


def _case_schema(base, name, claims_bytes, expected_exit, expected_finding, write_artifact):
    root = _fixture(base, name)
    try:
        _write(root, "README.txt", b"inert readme\n")
        if write_artifact:
            _write(root, _ARTIFACT, _payload(_ARTIFACT))
        _write(root, _SELFTEST_CLAIMS, claims_bytes)
        _selftest_commit(root, "freeze: add malformed claims")
        rc, out, err = _run_gate(root)
        _check(rc == expected_exit, "expected exit %d, got %d (stdout=%r stderr=%r)"
               % (expected_exit, rc, out.strip()[:300], err.strip()[:300]))
        _check("freeze-integrity: ERROR schema %s" % expected_finding in out,
               "missing schema finding %r: %r" % (expected_finding, out))
        _check("freeze-integrity: CLEAN" not in out, "schema reject must not print CLEAN: %r" % out)
        _check("ok\t" not in out, "schema reject must not print ok rows: %r" % out)
        return "exit=%d %s" % (expected_exit, expected_finding)
    finally:
        _drop(root)


def _case_compat(base, name, instruments, frozen_inputs, include_frozen, expected_pins):
    root = _fixture(base, name)
    try:
        _write(root, "README.txt", b"inert readme\n")
        for rel in instruments:
            _write(root, rel, _payload(rel))
        for rel in (frozen_inputs or {}):
            _write(root, rel, _payload(rel))
        _write(root, _SELFTEST_CLAIMS,
               _claims_doc({rel: _sha(_payload(rel)) for rel in instruments},
                           {rel: _sha(_payload(rel)) for rel in (frozen_inputs or {})},
                           include_frozen))
        _selftest_commit(root, "freeze: add historical-shape claims")
        rc, out, err = _run_gate(root)
        _check(rc == EXIT_CLEAN, "expected exit 0, got %d (stdout=%r stderr=%r)"
               % (rc, out.strip()[:300], err.strip()[:300]))
        _check("freeze-integrity: CLEAN pins=%d" % expected_pins in out,
               "missing CLEAN pins=%d: %r" % (expected_pins, out))
        return "exit=0 pins=%d" % expected_pins
    finally:
        _drop(root)


def selftest():
    os.makedirs(SELFTEST_BASE, exist_ok=True)
    cases = [
        ("clean", _case_clean),
        ("tampered_pin", _case_tampered),
        ("restored_after_change", _case_restored),
        ("absent_claims", _case_absent_claims),
        ("missing_pinned_file", _case_missing_pin),
        ("compat_absent_frozen_inputs",
         lambda b: _case_compat(b, "compat_absent_frozen_inputs", {_ARTIFACT: _ARTIFACT_DIGEST},
                                None, False, 1)),
        ("compat_empty_frozen_inputs",
         lambda b: _case_compat(b, "compat_empty_frozen_inputs",
                                {_ARTIFACT: _ARTIFACT_DIGEST, "data/second.txt": _sha(_payload("data/second.txt"))},
                                None, True, 2)),
        ("compat_round32_shape",
         lambda b: _case_compat(b, "compat_round32_shape",
                                {"tools/a.py": _sha(_payload("tools/a.py")),
                                 "tools/b.py": _sha(_payload("tools/b.py")),
                                 ".ufo/waves/round-99/pins.json": _sha(_payload(".ufo/waves/round-99/pins.json")),
                                 "bin/c.sh": _sha(_payload("bin/c.sh"))},
                                {"data/in-1.json": _sha(_payload("data/in-1.json")),
                                 "data/in-2.json": _sha(_payload("data/in-2.json")),
                                 "data/in-3.txt": _sha(_payload("data/in-3.txt")),
                                 "data/in-4.bin": _sha(_payload("data/in-4.bin"))},
                                True, 8)),
    ]
    cases.extend((name, lambda b, n=name, c=claims, e=exit_code, f=finding, w=artifact:
                  _case_schema(b, n, c, e, f, w))
                 for name, claims, exit_code, finding, artifact in _SCHEMA_CASES)
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
        return EXIT_FAIL
    print("freeze-integrity-selftest: PASS cases=%d elapsed_s=%.2f base=%s"
          % (len(cases), elapsed, SELFTEST_BASE))
    return EXIT_CLEAN


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
        return EXIT_ABSENT_FREEZE
    freeze = commits[-1]
    rc, text = git(a.root, "show", "%s:%s" % (freeze, claims))
    if rc != 0:
        print("freeze-integrity: ERROR schema code=claims_unreadable claims=%s where=-" % claims)
        return EXIT_SCHEMA
    try:
        pins = load_pins(text)
    except SchemaError as exc:
        print("freeze-integrity: ERROR schema code=%s claims=%s where=%s" % (exc.code, claims, exc.where))
        return EXIT_SCHEMA
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
        return EXIT_FAIL
    print("freeze-integrity: CLEAN pins=%d freeze=%s rev=%s" % (len(pins), freeze[:12], a.rev))
    return EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
