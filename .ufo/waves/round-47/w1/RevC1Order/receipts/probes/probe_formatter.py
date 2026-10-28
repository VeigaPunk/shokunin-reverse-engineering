#!/usr/bin/env python3
"""A real formatter at 80 columns: copy gate.py, format it, count clause 7's literals."""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

SCRATCH = sys.argv[1]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
T46 = os.path.join(LANE, "tools", "round-46")
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, T46)
import exact  # noqa: E402

ORDER, REVERSED = exact.ORDER, exact.REVERSED


def main():
    d = os.path.join(SCRATCH, "fmt80")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    src = os.path.join(d, "gate.py")
    shutil.copyfile(os.path.join(T46, "gate.py"), src)
    before = open(src).read()
    t0 = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fmt = subprocess.run(["ruff", "format", "--line-length", "80", src],
                         capture_output=True, text=True)
    t1 = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    after = open(src).read()
    print(json.dumps({
        "command": "ruff format --line-length 80 gate.py",
        "utc_start": t0, "utc_end": t1, "ruff_exit": fmt.returncode,
        "ruff_stdout": fmt.stdout.strip(), "ruff_stderr": fmt.stderr.strip(),
        "ruff_version": subprocess.run(["ruff", "--version"], capture_output=True,
                                       text=True).stdout.strip(),
        "bytes_changed": before != after,
        "literal_forward_before": before.count(ORDER),
        "literal_forward_after": after.count(ORDER),
        "literal_reversed_before": before.count(REVERSED),
        "literal_reversed_after": after.count(REVERSED),
        "clause7_would_reject": after.count(ORDER) != 1 or after.count(REVERSED) != 0,
        "embedded_digest_unchanged": subprocess.run(
            ["git", "hash-object", "--", src], capture_output=True, text=True).stdout.strip(),
        "fixture_path": src,
    }, indent=1))
    print(after[after.index("def history_touched"):after.index("def history_touched") + 700])
    shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
