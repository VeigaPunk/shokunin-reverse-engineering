#!/usr/bin/env python3
"""EX-33 attack driver, deterministic variants of "the executed image is not the disk file".

mode=revise : exec source from memory, revise the disk file, then run capture
              -> pin should name the revised disk bytes, not the executed bytes (A1)
mode=vanish : exec source from memory with __file__ pointing at a path that was
              read then removed -> render_receipt's TOOL_PATH.exists() is false
              -> pin becomes "(unavailable)" (A6)
"""
import argparse
import contextlib
import hashlib
import io
import sys
import types
from pathlib import Path


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--mode", choices=("revise", "vanish"), required=True)
    a = ap.parse_args()

    tool = Path(a.tool)
    src = tool.read_bytes()
    s_exec = sha256_bytes(src)

    mod = types.ModuleType("custody_pair_exec")
    mod.__dict__["__name__"] = "__main__"
    mod.__dict__["__file__"] = str(tool)
    code = compile(src, str(tool), "exec")

    s_disk = None
    if a.mode == "revise":
        tool.write_bytes(src + b"\n# variant: revised on disk after exec image fixed\n")
        s_disk = sha256_bytes(tool.read_bytes())
    else:  # vanish
        tool.unlink()

    sys.argv = ["custody-pair.py", "capture", "--out", a.out,
                "--paths", a.fixture, "--label", "attack-%s" % a.mode]
    buf = io.StringIO()
    rc = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(code, mod.__dict__)
        except SystemExit as exc:
            rc = exc.code
    sys.stdout.write(buf.getvalue())

    text = Path(a.out).read_text(encoding="utf-8")
    pin = next((l for l in text.splitlines() if l.startswith("# tool: ")), None)
    print("mode=%s executed-image sha=%s" % (a.mode, s_exec))
    if s_disk:
        print("mode=%s disk sha at render time=%s" % (a.mode, s_disk))
    print("mode=%s receipt pin line: %s" % (a.mode, pin))
    if a.mode == "revise":
        ok = pin and pin.endswith(s_disk) and s_disk != s_exec
        print("A1 VERDICT: %s" % ("TOCTOU-CONFIRMED" if ok else "UNEXPECTED"))
        return 0 if ok else 1
    ok = pin is not None and "(unavailable)" in pin
    print("A6 VERDICT: %s" % ("PIN-UNAVAILABLE-SHAPE" if ok else "UNEXPECTED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())