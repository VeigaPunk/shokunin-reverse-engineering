#!/usr/bin/env python3
"""c1-receipt-agreement.py - round-94 frozen counting command for R94-C1 (calibration).

For each of the four frozen runs (positive repair, forgeries F1-F3) it reads the captured
`<prefix>-<name>.json` receipt, `.stdout` line and `.rc` file and counts three atoms:

  valid      the receipt parses as JSON (a truncated or absent receipt is not valid)
  agree      receipt label, met_target and exit equal the stdout line's label, met and exit,
             and the captured rc equals the receipt exit
  predicted  met_target and exit equal the predicted verdict: positive met True exit 0;
             F1, F2, F3 met False exit 1

Prints one JSON object with the three counts out of four and the per-run rows. Exit 0 iff
all three counts are 4 of 4; otherwise exit 1.

    python3 tools/round-94/c1-receipt-agreement.py --dir <wave dir> --prefix c1-v4
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

NAMES = ("pos", "F1", "F2", "F3")
PREDICTED = {"pos": (True, 0), "F1": (False, 1), "F2": (False, 1), "F3": (False, 1)}
LINE = re.compile(r"^(.*) met (True|False|None) exit (\d+)$")


def _read(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def row(directory: str, prefix: str, name: str) -> dict:
    base = os.path.join(directory, f"{prefix}-{name}")
    out = {"run": name, "valid": False, "agree": False, "predicted": False}
    raw = _read(base + ".json")
    if raw is not None:
        try:
            rec = json.loads(raw)
            out["valid"] = isinstance(rec, dict)
        except ValueError:
            rec = None
    else:
        rec = None
    stdout = (_read(base + ".stdout") or "").strip()
    m = LINE.match(stdout.splitlines()[-1]) if stdout else None
    rc_text = (_read(base + ".rc") or "").strip()
    if rec is not None and m is not None and rc_text.isdigit():
        s_label, s_met, s_exit = m.group(1), m.group(2) == "True", int(m.group(3))
        met = rec.get("met_target")
        exit_code = rec.get("exit")
        out["agree"] = (rec.get("label") == s_label and met is s_met
                        and exit_code == s_exit and int(rc_text) == s_exit)
        want_met, want_exit = PREDICTED[name]
        out["predicted"] = (met is want_met and exit_code == want_exit)
    out["stdout"] = stdout
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix", required=True)
    args = ap.parse_args(argv)
    rows = [row(args.dir, args.prefix, n) for n in NAMES]
    counts = {k: sum(1 for r in rows if r[k]) for k in ("valid", "agree", "predicted")}
    ok = all(v == len(NAMES) for v in counts.values())
    print(json.dumps({"prefix": args.prefix, "counts_of_4": counts, "met": ok,
                      "rows": rows}, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
