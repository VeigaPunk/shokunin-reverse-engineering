#!/usr/bin/env python3
"""Validate rows.md with the FROZEN round-46 registry parser (registry.py@freeze).

Checks, per the v2 strict clauses the L1 will paste into:
  * exactly one section (markers) built around the house header + the three rows
  * header equals HOUSE
  * exactly three rows, every row exactly 7 cells
  * cell 0 is exactly the backticked census path and nothing else
  * cell 2's EXITMAP key set is exactly {0,1,2}
  * the census path is present at the freeze commit (presence clause)
  * ids are the three census ids this seat owns
"""
import json
import subprocess
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r46/R46W1RegB/frozen")
import registry  # noqa: E402

FREEZE = "31820472784284727546808acc31b3ea1e73919b"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
ROWS = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1RegB/rows.md"
WANT = ["tools/round-41/c1-extra.py", "tools/round-42/c1-run.sh",
        "tools/round-43/verify-copies-r43.py"]

body = open(ROWS, encoding="utf-8").read().rstrip("\n")
lines = body.splitlines()
fails = []


def chk(ok, msg):
    print(("PASS\t" if ok else "FAIL\t") + msg)
    if not ok:
        fails.append(msg)


chk(len(lines) == 3, "row count == 3 (got %d)" % len(lines))

mid = "\n" + "\n".join(lines) + "\n"
cells = registry.rows_in_section(mid)
hdr = ["tool", "gate or probe - purpose", "verdict map (exit codes)",
       "self-test command", "pinned-value path", "write scope", "owner"]
header, rows = registry.grid(cells)
# no header line in rows.md: the first row becomes `header`, so prepend the house header
header, rows = registry.grid([[h.strip() for h in hdr]] + cells)
chk(header == registry.HOUSE, "header equals frozen HOUSE schema")
chk(len(rows) == 3, "parsed data rows == 3 (got %d)" % len(rows))
chk(all(len(r) == 7 for r in rows),
    "every row has exactly 7 cells: %s" % [len(r) for r in rows])

by_path = {}
for r in rows:
    if not r:
        continue
    key = r[0].strip()
    if key.startswith("`") and key.endswith("`") and len(key) > 2:
        by_path.setdefault(key[1:-1], r)

for path in WANT:
    row = by_path.get(path)
    chk(row is not None, "cell 0 exact for %s" % path)
    if row is None:
        continue
    keys = set(registry.EXITMAP.findall(row[2]))
    chk(keys == {"0", "1", "2"}, "verdict map binds {0,1,2} exactly for %s: %s" % (path, sorted(keys)))
    present = subprocess.run(["git", "-C", LANE, "cat-file", "-e", "%s:%s" % (FREEZE, path)],
                             capture_output=True).returncode == 0
    chk(present, "present at freeze %s" % path)
    chk("|" not in "".join(row), "no stray pipe inside cells for %s" % path)

extra = sorted(set(by_path) - set(WANT))
chk(extra == [], "no rows outside the three assigned ids (extra=%s)" % extra)
print("VALIDATE failures=%d" % len(fails))
sys.exit(0 if not fails else 1)
