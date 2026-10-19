#!/usr/bin/env python3
"""EX-33 attack A1 — is the receipt's self-pin a pin of the EXECUTED image?

The tool computes its pin with `sha256_file(TOOL_PATH)` inside render_receipt,
i.e. a live disk read AFTER the captures, not a hash of the code that is
running.  This driver makes that deterministic without racing:

  1. read the tool source into memory  -> these are the EXECUTED bytes (S_exec)
  2. revise the on-disk file           -> disk bytes become S_disk
  3. exec the in-memory source with __file__ pointing at the (now revised) path
  4. capture a receipt from a scratch fixture (never a custody path)
  5. classify:  pin == S_disk != S_exec  => the pin names bytes that never ran
"""
import hashlib
import io
import contextlib
import sys
import types
from pathlib import Path


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    tool = Path(sys.argv[1])
    out = Path(sys.argv[2])
    fixture = Path(sys.argv[3])

    src = tool.read_bytes()                       # executed image
    s_exec = sha256_bytes(src)

    mod = types.ModuleType("custody_pair_exec")
    mod.__dict__["__name__"] = "__main__"
    mod.__dict__["__file__"] = str(tool)          # the tool resolves TOOL_PATH from this

    code = compile(src, str(tool), "exec")

    tool.write_bytes(src + b"\n# A1: revised on disk AFTER the executed image was fixed\n")
    s_disk = sha256_bytes(tool.read_bytes())

    sys.argv = ["custody-pair.py", "capture", "--out", str(out),
                "--paths", str(fixture), "--label", "A1-executed-vs-disk"]

    buf = io.StringIO()
    rc = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(code, mod.__dict__)              # module's sys.exit(main())
        except SystemExit as exc:
            rc = exc.code
    sys.stdout.write(buf.getvalue())

    text = out.read_text(encoding="utf-8")
    pin = None
    for line in text.splitlines():
        if line.startswith("# tool: "):
            pin = line.rsplit("sha256 ", 1)[1].strip()
    print("A1 executed-image sha (source read into memory, then exec'd): %s" % s_exec)
    print("A1 on-disk sha at render time (revised mid-run):              %s" % s_disk)
    print("A1 receipt pin:                                               %s" % pin)
    if pin == s_disk and pin != s_exec:
        print("A1 VERDICT: TOCTOU-CONFIRMED — the pin names bytes that did not execute")
        return 0
    print("A1 VERDICT: UNEXPECTED — pin=%s (exec=%s disk=%s) rc=%s" % (pin, s_exec, s_disk, rc))
    return 1


if __name__ == "__main__":
    sys.exit(main())