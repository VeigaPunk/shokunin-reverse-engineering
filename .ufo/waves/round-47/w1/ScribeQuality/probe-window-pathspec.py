#!/usr/bin/env python3
"""ScribeQuality probe — does a free-text pathspec turn formatting into a verdict?

`tools/round-47/record.py` derives a `window` atom's pathspec with
    paths = re.findall(r"--\\s+([A-Za-z0-9._/ -]+)", tail)
and scores the atom with `git log --name-status --format= <A>..<B> -- <paths>`. Three
consequences, measured here at atom level (`record.collect` + `record.derive`, the exact
functions `evaluate_text` uses):

  * a path set that names no tracked path makes `git log` print nothing and exit 0, so the
    atom is scored `empty` (verified) although the window is not empty over the real path;
  * a path set written inside backticks (the spelling `corpus/lessons/round-46.md` uses)
    fails the regex entirely, leaving `pathspec []`, so `git log` runs over the whole tree —
    the correct claim turns red;
  * trailing prose after a bare path joins the pathspec.

Nothing on the lane is written.
"""
import argparse
import json
import os
import sys

LANE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
import record  # noqa: E402
import gate  # noqa: E402

VARIANTS = {
    "backticked-path": "- The window {w} -- `{p}` is empty at the measured revision.",
    "bare-path": "- The window {w} -- {p} is empty at the measured revision.",
    "bogus-path": "- The window {w} -- tools/round-95 does not exist is empty at the measured revision.",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--window", required=True, help="A..B that is NOT empty over --paths")
    ap.add_argument("--paths", required=True)
    ap.add_argument("--json-out")
    a = ap.parse_args()
    files = lambda p: gate.show(LANE, a.rev, p)  # noqa: E731
    cache = lambda rnd: record.dispatch_counts(files, rnd)  # noqa: E731
    out = {"rev": a.rev, "window": a.window, "paths": a.paths, "variants": {}}
    for name, tpl in VARIANTS.items():
        line = tpl.format(w=a.window, p=a.paths)
        atoms = [x for x in record.collect(line, "47", files, LANE, a.rev)
                 if x["class"] == "window"]
        ok, detail = record.derive(atoms[0], files, LANE, a.rev, cache)
        out["variants"][name] = {"line": line, "atom_ok": ok, "derived": detail}
    print(json.dumps(out, indent=1))
    if a.json_out:
        with open(a.json_out, "w") as fh:
            json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
