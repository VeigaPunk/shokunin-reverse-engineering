#!/usr/bin/env python3
"""RV-7v canonical-scope arm — executable but non-destructive.

The canonical custody paths are READ-ONLY for this seat, so a reverted guard
aimed at `~/.bashrc` cannot be exercised for real. Instead: import each tool
revision as a module, monkeypatch `Path.write_text`/`Path.mkdir` to raise, then
invoke `capture --paths <scratch> --out ~/.bashrc`.

  * guard intact  -> returns EXIT_USAGE, write_text never called  (SAFE-REFUSED)
  * guard absent  -> the harness intercepts the write            (WOULD-CLOBBER)

`WOULD-CLOBBER` is a proof of the write attempt, not a write: the monkeypatch
raises before any bytes reach the real file, and the file's sha256 is compared
before/after as a second belt.
"""
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import sys
import contextlib

CANON = os.path.expanduser("~/.bashrc")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def probe(tool_path, tag, scratch):
    real_write = pathlib.Path.write_text
    real_mkdir = pathlib.Path.mkdir
    calls = []

    def fake_write(self, *a, **k):
        calls.append(("write_text", str(self)))
        raise RuntimeError("HARNESS-INTERCEPT")

    def fake_mkdir(self, *a, **k):
        calls.append(("mkdir", str(self)))
        return None

    pathlib.Path.write_text = fake_write
    pathlib.Path.mkdir = fake_mkdir
    before = sha(CANON)
    try:
        mod = load(tool_path, "rv7v_probe_" + tag)
        ns = mod.argparse.Namespace(paths=[str(scratch / "scoped.conf")],
                                    out=CANON, label="rv7v-canonical")
        buf, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
                rc = mod.cmd_capture(ns)
        except RuntimeError as exc:
            rc = "RAISED:" + str(exc)
        except SystemExit as exc:
            rc = "SYSEXIT:%s" % exc
    finally:
        pathlib.Path.write_text = real_write
        pathlib.Path.mkdir = real_mkdir
    after = sha(CANON)
    wrote = any(c[0] == "write_text" for c in calls)
    if isinstance(rc, int) and rc == 2 and not wrote:
        verdict = "SAFE-REFUSED"
    elif wrote:
        verdict = "WOULD-CLOBBER"
    else:
        verdict = "OTHER"
    return {"tag": tag, "tool": tool_path, "tool_sha256": sha(tool_path),
            "exit": rc, "write_attempted": wrote, "intercepted_calls": calls,
            "canon_sha_before": before, "canon_sha_after": after,
            "canon_untouched": before == after, "verdict": verdict,
            "stderr": err.getvalue().strip()[:200]}


def main():
    out = pathlib.Path(sys.argv[1])
    scratch = pathlib.Path(sys.argv[2])
    scratch.mkdir(parents=True, exist_ok=True)
    (scratch / "scoped.conf").write_bytes(b"rv7v-scoped-payload\n")
    arms = [
        ("pre-112d01dc", "/var/tmp/rv7v/tools/pre-112d01dc.py"),
        ("landed-7cd19c3c", "/var/tmp/rv7v/tools/landed-7cd19c3c.py"),
        ("M1-guard-revert", "/var/tmp/rv7v/mutants/M1-guard-revert.py"),
        ("M1a-scoped-arm-revert", "/var/tmp/rv7v/mutants/M1a-scoped-arm-revert.py"),
        ("M1b-inode-arm-revert", "/var/tmp/rv7v/mutants/M1b-inode-arm-revert.py"),
    ]
    res = [probe(p, t, scratch) for t, p in arms]
    out.write_text(json.dumps(res, indent=2) + "\n")
    for r in res:
        print("%-24s %-14s exit=%-12s write=%s canon_untouched=%s" %
              (r["tag"], r["verdict"], r["exit"], r["write_attempted"], r["canon_untouched"]))


if __name__ == "__main__":
    main()
