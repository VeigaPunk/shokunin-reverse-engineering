#!/usr/bin/env python3
"""Audit which files the CtlHashReplay control reader opens.

Runs the control reader under a sys.addaudithook that records every file
opened for reading, so the claim "the control reads the input solely to hash
it" is backed by an observed syscall-level file list rather than by reading
the source. The reader is executed with the same isolation flags the counter
uses (-I -B) but through this wrapper, so this is an audit probe and is not
the scored run.

Usage: audit_reader_access.py <reader.py> <input-file>
"""
import json
import runpy
import sys

opened = []


def hook(event, args):
    if event == "open":
        try:
            opened.append({"path": str(args[0]), "mode": str(args[1]), "flags": str(args[2])})
        except Exception:
            opened.append({"path": repr(args[0])})


sys.addaudithook(hook)
reader, target = sys.argv[1], sys.argv[2]
sys.argv = [reader, target]
try:
    runpy.run_path(reader, run_name="__main__")
except SystemExit as exit_error:
    code = exit_error.code
else:
    code = 0
sys.stderr.write(json.dumps({"kind": "reader_file_access_audit", "opened": opened,
                              "distinct_paths": sorted({o["path"] for o in opened}),
                              "exit": code}, sort_keys=True))
sys.exit(code if isinstance(code, int) else 0)
