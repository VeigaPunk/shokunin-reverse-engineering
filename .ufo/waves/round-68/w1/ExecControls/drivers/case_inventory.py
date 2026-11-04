#!/usr/bin/env python3
"""case_inventory.py - capture the runtime executed case names of both round-68
selftests and compare them, in order, with each module's REGISTERED_CASES.

The selftests print only a count; this harness reads the selftest frame's own
`cases` local on its return event, so the comparison is a runtime observation,
not an AST re-reading of the source.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = os.path.join(LANE, ".ufo", "waves", "round-68", "w1", "ExecControls",
                   "case-inventory.json")
TOOLS = [(os.path.join(LANE, "tools/round-68/registry-conformance.py"), "r68_registry"),
         (os.path.join(LANE, "tools/round-68/packed-elf.py"), "r68_packed")]


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def capture(path: str, name: str) -> dict:
    target = os.path.abspath(path)
    mod = load(path, name)
    seen: dict = {}
    buf = io.StringIO()

    def trace(frame, event, arg):
        if frame.f_code.co_filename == target and frame.f_code.co_name == "selftest":
            if event == "return":
                seen["cases"] = [(n, bool(ok))
                                 for n, ok in frame.f_locals.get("cases", [])]
        return trace

    old = sys.stdout
    sys.stdout = buf
    try:
        sys.settrace(trace)
        rc = mod.selftest()
    finally:
        sys.settrace(None)
        sys.stdout = old
    executed = [n for n, _ in seen.get("cases", [])]
    registered = list(mod.REGISTERED_CASES)
    return {
        "tool": os.path.relpath(path, LANE),
        "registered_cases": registered,
        "registered_count": len(registered),
        "executed_names": executed,
        "executed_count": len(executed),
        "names_equal": executed == registered,
        "case_results": dict(seen.get("cases", [])),
        "all_cases_true": all(ok for _, ok in seen.get("cases", [])),
        "selftest_rc": rc,
        "selftest_stdout": buf.getvalue(),
    }


def main() -> int:
    results = [capture(path, name) for path, name in TOOLS]
    payload = {
        "schema": "kaidoku-r68-case-inventory-v1",
        "note": ("executed names captured from the selftest frame's `cases` local "
                 "on its return event; counts alone are not treated as inventory"),
        "tools": results,
        "ok": all(r["names_equal"] and r["all_cases_true"] and r["selftest_rc"] == 0
                  for r in results),
    }
    text = json.dumps(payload, indent=1, sort_keys=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
