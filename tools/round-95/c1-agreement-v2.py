#!/usr/bin/env python3
"""c1-agreement-v2.py - round-95 strengthened receipt-agreement instrument (R95-C1).

The round-94 frozen instrument `tools/round-94/c1-receipt-agreement.py` checks only
receipt<->stdout<->rc agreement and the predicted met/exit per run name. The round-94
critic (CriticC1 attacks 2/3/4, M94-e) showed it admits: a receipt pair whose `label`
is rewritten consistently in both files, and a wholly fabricated triple.

v2 keeps every round-94 atom and adds four world bindings, each with a typed reason:

  label-not-frozen     met_target is true and `label` != the frozen `--expect` string
  label-not-recomputed the label's six segments do not recompute from `counts`
                       (+ `--intact-total`, default 6)
  revision-not-bound   `revision` != the full 40-hex resolution of `--rev`
  pins-not-bound       `verdict_sha256` != sha256(git show REV:tools/round-93/...v3.py)
                       or `counter_sha256` != sha256(git show REV:<receipt.tool>)

The inherited atoms keep their round-94 meaning and reasons: `not-valid`,
`stdout-disagree`, `rc-disagree`, `predicted-mismatch`.

    python3 -I -B tools/round-95/c1-agreement-v2.py --root . --dir <dir> --prefix <p> \
        --rev <full-or-short-rev> --expect '<label>' [--case NAME] [--json-out <path>]

Exit 0 iff every named run carries an empty reason list. `--selftest <dir>` runs a
hermetic fixture world (no git, no network): the world's expected pins and revision
come from `<dir>/world.json` instead of `git show`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

NAMES = ("pos", "F1", "F2", "F3")
PREDICTED = {"pos": (True, 0), "F1": (False, 1), "F2": (False, 1), "F3": (False, 1)}
LINE = re.compile(r"^(.*) met (True|False|None) exit (\d+)$")
LABEL_RE = re.compile(
    r"^repaired (\d+) of (\d+); wrong (\d+); unsafe (\d+); intact (\d+) of (\d+); "
    r"far-refused (\d+) of (\d+); fresh-roundtrip (\d+) of (\d+)$")


def _read(path: str):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_show(root: str, rev: str, path: str):
    out = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)],
                         capture_output=True, timeout=30)
    if out.returncode != 0:
        return None
    return out.stdout


def _resolve_rev(root: str, rev: str):
    if not re.fullmatch(r"[0-9a-f]{6,64}", rev or ""):
        return None
    try:
        out = subprocess.run(["git", "-C", root, "rev-parse", "--verify", rev],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    full = out.stdout.strip()
    return full if re.fullmatch(r"[0-9a-f]{40}", full) else None


def recompute_label(counts: dict, intact_total: int) -> str:
    return ("repaired %d of %d; wrong %d; unsafe %d; intact %d of %d; "
            "far-refused %d of %d; fresh-roundtrip %d of %d") % (
        counts["repaired"], counts["scored"], counts["wrong"], counts["unsafe"],
        counts["intact"], intact_total, counts["far_refused"], counts["far"],
        counts["fresh_roundtrip"], counts["fresh_scored"])


def row(directory: str, prefix: str, name: str, expect: str, rev_full,
        intact_total: int, world: dict | None, root: str = ".") -> dict:
    """world: hermetic selftest override {expected_verdict_sha256, expected_counter_sha256}."""
    base = os.path.join(directory, f"{prefix}-{name}")
    out = {"run": name, "valid": False, "agree": False, "predicted": False,
           "reasons": []}
    raw = _read(base + ".json")
    rec = None
    if raw is not None:
        try:
            rec = json.loads(raw)
            out["valid"] = isinstance(rec, dict)
        except ValueError:
            rec = None
    if not out["valid"]:
        out["reasons"].append("not-valid")
        return out
    stdout = (_read(base + ".stdout") or "").strip()
    rc_text = (_read(base + ".rc") or "").strip()

    # Inherited atom: receipt <-> stdout <-> rc agreement.
    m = None
    for line in reversed(stdout.splitlines()[-3:]):
        m = LINE.match(line)
        if m is not None:
            break
    if m is None or not rc_text.isdigit():
        out["reasons"].append("stdout-disagree")
    else:
        s_label, s_met, s_exit = m.group(1), m.group(2) == "True", int(m.group(3))
        met = rec.get("met_target")
        exit_code = rec.get("exit")
        ok = (rec.get("label") == s_label and met is s_met
              and exit_code == s_exit and int(rc_text) == s_exit)
        out["agree"] = ok
        if not ok:
            out["reasons"].append("stdout-disagree")
        want_met, want_exit = PREDICTED[name]
        out["predicted"] = (met is want_met and exit_code == want_exit)
        if not out["predicted"]:
            out["reasons"].append("predicted-mismatch")

    counts = rec.get("counts")
    label = rec.get("label")

    # Binding 1+2: the label is bound to the frozen expect when met, and must
    # recompute from the receipt's own counts.
    if not isinstance(counts, dict) or not isinstance(label, str):
        out["reasons"].append("label-not-recomputed")
    else:
        lm = LABEL_RE.match(label)
        if lm is None or lm.group(0) != recompute_label(counts, intact_total):
            out["reasons"].append("label-not-recomputed")
        elif rec.get("met_target") is True and expect is not None and label != expect:
            out["reasons"].append("label-not-frozen")

    # Binding 3: the receipt's revision is the measured tree.
    if rev_full is None or rec.get("revision") != rev_full:
        out["reasons"].append("revision-not-bound")

    # Binding 4: the receipt's pins are the pinned bytes of that tree.
    tool = rec.get("tool")
    if world is not None:
        exp_verdict = world.get("expected_verdict_sha256")
        exp_counter = world.get("expected_counter_sha256")
    else:
        exp_verdict = None
        exp_counter = None
        if rev_full is not None:
            v3_bytes = _git_show(root, rev_full,
                                 "tools/round-93/stop-boundary-repair-battery-v3.py")
            exp_verdict = _sha256_bytes(v3_bytes) if v3_bytes is not None else None
            if isinstance(tool, str) and re.fullmatch(r"[0-9A-Za-z_./-]+", tool):
                tool_bytes = _git_show(root, rev_full, tool)
                exp_counter = _sha256_bytes(tool_bytes) if tool_bytes is not None else None
    if (rec.get("verdict_sha256") != exp_verdict
            or rec.get("counter_sha256") != exp_counter):
        out["reasons"].append("pins-not-bound")
    return out


def _selftest(fixdir: str) -> int:
    """Hermetic: the selftest authors its own fixture world (world.json + five
    triples) inside `fixdir` — no git, no network, no live-tree write."""
    os.makedirs(fixdir, exist_ok=True)
    rev_full = "c" * 40
    world = {"revision": rev_full,
             "expected_verdict_sha256": hashlib.sha256(b"mini-verdict").hexdigest(),
             "expected_counter_sha256": hashlib.sha256(b"mini-counter").hexdigest(),
             "expect": ("repaired 2 of 2; wrong 0; unsafe 0; intact 1 of 1; "
                        "far-refused 1 of 1; fresh-roundtrip 1 of 1")}
    with open(os.path.join(fixdir, "world.json"), "w", encoding="utf-8") as fh:
        json.dump(world, fh, indent=1, sort_keys=True)
        fh.write("\n")
    expect = world["expect"]
    counts = {"repaired": 2, "scored": 2, "wrong": 0, "unsafe": 0, "intact": 1,
              "far": 1, "far_refused": 1, "fresh_roundtrip": 1, "fresh_scored": 1}
    label = recompute_label(counts, 1)
    base = {"class": "selftest", "counts": counts, "label": label,
            "met_target": True, "exit": 0, "revision": rev_full,
            "tool": "selftest-writer.py",
            "verdict_sha256": world["expected_verdict_sha256"],
            "counter_sha256": world["expected_counter_sha256"]}
    ok = True

    def case(name: str, cond: bool) -> None:
        nonlocal ok
        ok = ok and cond
        print(f"selftest {name}: {'ok' if cond else 'FAIL'}")

    # honest: every atom and binding green
    _write_world(fixdir, "honest", "pos", base, label, True, 0)
    r = row(fixdir, "honest", "pos", expect, rev_full, 1, world)
    case("honest-accepted", r["valid"] and r["agree"] and r["predicted"]
         and r["reasons"] == [])

    # label rewrite (consistent pair) -> label-not-frozen only
    other_counts = {**counts, "far_refused": 0}
    other = recompute_label(other_counts, 1)
    _write_world(fixdir, "rw", "pos",
                 {**base, "label": other, "counts": other_counts}, other, True, 0)
    r = row(fixdir, "rw", "pos", expect, rev_full, 1, world)
    case("rewrite-refused", r["reasons"] == ["label-not-frozen"])

    # counts that do not recompute -> label-not-recomputed only
    _write_world(fixdir, "nr", "F1", {**base, "met_target": False, "exit": 1,
                                      "counts": {**counts, "repaired": 1}},
                 label, False, 1)
    r = row(fixdir, "nr", "F1", expect, rev_full, 1, world)
    case("not-recomputed-refused", r["reasons"] == ["label-not-recomputed"])

    # short revision -> revision-not-bound only
    _write_world(fixdir, "sr", "F2", {**base, "met_target": False, "exit": 1,
                                      "revision": (rev_full or "")[:9]},
                 label, False, 1)
    r = row(fixdir, "sr", "F2", expect, rev_full, 1, world)
    case("short-revision-refused", r["reasons"] == ["revision-not-bound"])

    # fabricated pins -> pins-not-bound only
    _write_world(fixdir, "fp", "F3", {**base, "met_target": False, "exit": 1,
                                      "verdict_sha256": "0" * 64,
                                      "counter_sha256": "f" * 64},
                 label, False, 1)
    r = row(fixdir, "fp", "F3", expect, rev_full, 1, world)
    case("fabricated-pins-refused", r["reasons"] == ["pins-not-bound"])

    print(f"SELFTEST cases=5 failures={0 if ok else 1}")
    return 0 if ok else 1


def _write_world(fixdir: str, prefix: str, name: str, rec: dict, label: str,
                 met: bool, exit_code: int) -> None:
    stem = os.path.join(fixdir, f"{prefix}-{name}")
    with open(stem + ".json", "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(stem + ".stdout", "w", encoding="utf-8") as fh:
        fh.write("%s met %s exit %d\n" % (label, met, exit_code))
    with open(stem + ".rc", "w", encoding="utf-8") as fh:
        fh.write("%d\n" % exit_code)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--dir")
    ap.add_argument("--prefix")
    ap.add_argument("--names", default=",".join(NAMES))
    ap.add_argument("--case")
    ap.add_argument("--expect")
    ap.add_argument("--rev")
    ap.add_argument("--intact-total", type=int, default=6)
    ap.add_argument("--json-out")
    ap.add_argument("--selftest")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest(args.selftest)
    if not args.dir or not args.prefix or args.expect is None:
        print("usage: --dir <d> --prefix <p> --expect <label> --rev <rev> "
              "[--case NAME] [--json-out <path>]", file=sys.stderr)
        return 2
    rev_full = _resolve_rev(args.root, args.rev or "")
    names = [args.case] if args.case else [n for n in args.names.split(",") if n]
    rows = [row(args.dir, args.prefix, n, args.expect, rev_full,
                args.intact_total, None, root=os.path.abspath(args.root))
            for n in names]
    ok = all(not r["reasons"] for r in rows)
    payload = {"prefix": args.prefix, "names": names, "revision": rev_full,
               "met": ok, "rows": rows}
    rendered = json.dumps(payload, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    print(rendered)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
