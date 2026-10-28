#!/usr/bin/env python3
"""CritC2Calibration attack on R47-C2 (tools/round-47/record.py, as landed at 2e4ae434).

Every case is built in a throwaway git repo under $TMPDIR. The counter is imported
read-only from the lane tools directory; nothing under the lane is written.

  TMPDIR=<scratch> python3 -I -B \
    .ufo/waves/round-47/w1/CritC2Calibration/fixtures/c2-attack.py \
    --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin

Each case reports expect / got (0 met, 1 not met) and the counter's `failing` list.
`defect` names why a green there is calibration-blindness rather than calibration.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

CRAFT = "## Queue-drain craft "
CORR_HEAD = "## Record corrections — round 47"

AXES = ("## Owned axes\n\n"
        "| Axis | Baseline → current score, 0–10 | Observable | Evidence | Round |\n"
        "|---|---|---|---|---|\n"
        "| coverage | 9.0 → 10.0 | 1/1 knowledge files mapped | x | r9 |\n"
        "| depth | 9.0 → 10.0 | 1/1 craft rules resolved | x | r9 |\n\n")
CRAFTED = CRAFT + "\n\n- **r1** cites `tools/x/keep.md:1`\n\n"
AXES_LINES = ["- corrects axes coverage: 1/1", "- corrects axes depth: 1/1"]
CORR_BASE = ["- corrects path .ufo/waves/round-9/w1-dispatch.json: present",
             "- corrects rev BASE: the base commit"]


def git(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)


def write(root, path, body):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(body)


def commit(d, msg):
    git(d, "add", "-A")
    r = git(d, "commit", "-q", "-m", msg)
    if r.returncode != 0:
        raise SystemExit("commit failed: " + r.stderr)
    return git(d, "rev-parse", "HEAD").stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    args = ap.parse_args()
    sys.path.insert(0, os.path.join(args.lane, "tools", "round-47"))
    import record  # noqa: E402  (read-only import of the frozen counter)

    scratch = os.environ.get("TMPDIR") or tempfile.gettempdir()
    d = tempfile.mkdtemp(dir=scratch, prefix="c2attack-")
    try:
        assert git(d, "init", "-q").returncode == 0
        git(d, "config", "user.email", "crit@r47")
        git(d, "config", "user.name", "crit c2")
        top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), (top, d)

        write(d, "corpus/README.md",
              "# readme\n\n## Coverage map\n\n- 2026-10-01-x — x\n\n## Gaps\n\ntail\n")
        write(d, "corpus/knowledge/2026-10-01-x.md", "x\n")
        write(d, "corpus/lessons/kept.md", "kept\n")
        write(d, "tools/x/keep.md", "a\n")
        write(d, "SKILL.md", "# skill\n\n" + CRAFTED)
        write(d, ".ufo/waves/round-9/w1-dispatch.json",
              json.dumps({"counts": {"spawn": 30, "resume": 0, "total": 30}}))
        write(d, ".ufo/waves/round-9/w2-dispatch.json",
              json.dumps({"counts": {"spawn": 10, "resume": 0, "total": 10}}))
        write(d, ".ufo/waves/round-3/w1-dispatch.json",
              json.dumps({"counts": {"spawn": 20, "resume": 0, "total": 20}}))
        write(d, ".ufo/waves/round-3/w2-dispatch.json",
              json.dumps({"counts": {"spawn": 30, "resume": 0, "total": 30}}))
        base = commit(d, "base")

        git(d, "checkout", "-q", "-b", "side")
        write(d, "tools/x/side.md", "side\n")
        side = commit(d, "side")
        git(d, "checkout", "-q", "-")

        write(d, "tools/x/keep.md", "a\nb\n")          # base..tip touches tools/x
        tip = commit(d, "tip")
        b8, t8, s8 = base[:8], tip[:8], side[:8]

        # honest body: all five classes present, every atom true at `tip`
        HONEST = ("Waves: 30 + 10 = 40 seats. The window `git log %s..%s -- corpus/` is "
                  "empty at every measurement. Base `%s`. Per-seat output in "
                  "`.ufo/waves/round-9/w1-dispatch.json`.\n" % (b8, t8, b8))

        def card(body, corrections, axes=AXES, base_sha=b8):
            return ("# card\n\n" + axes + "## Round 8\n\nAn earlier round with no atoms.\n\n"
                    "## Round 9\n\n" + body + "\n" + CORR_HEAD + "\n\n"
                    + "\n".join(corrections) + "\n")

        def run(name, expect, body, corrections, defect=None, extra=None):
            code, rec = record.evaluate_text(card(body, corrections),
                                             lambda p: None, d, tip, battery=None)
            # files() -> None would break axes; supply the real blobs through git show
            return code, rec

        # the counter needs a files() that reads the fixture repo at `tip`
        def files_at_rev(p):
            r = git(d, "show", f"{tip}:{p}")
            return r.stdout if r.returncode == 0 else None

        def command_a(rev):
            """The depth reader the card itself names: corpus/knowledge refs only,
            every ref in a rule must resolve. Verbatim from SCORECARD's command A."""
            craft = (git(d, "show", f"{rev}:SKILL.md").stdout or "")
            craft = craft.split(CRAFT, 1)[1].split("\n## ", 1)[0]
            rules = __import__("re").split(r"(?m)^- \*\*", craft)[1:]
            pat = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
            resolved = 0
            for rule in rules:
                refs = __import__("re").findall(pat, rule)
                valid = bool(refs)
                for name, first, last in refs:
                    body = (git(d, "show", f"{rev}:corpus/knowledge/{name}").stdout or "")
                    count = len(body.splitlines())
                    start, end = int(first or 1), int(last or first or 1)
                    valid = valid and 1 <= start <= end <= count
                resolved += valid
            return resolved, len(rules)

        results = []

        def files_at(rev):
            def reader(p):
                r = git(d, "show", f"{rev}:{p}")
                return r.stdout if r.returncode == 0 else None
            return reader

        def case(name, expect, body, corrections, defect=None, extra=None, axes=None,
                 rev=None):
            base_sha = b8
            rev = rev or tip
            corr = [c.replace("BASE", base_sha) for c in corrections]
            body = body.replace("BASE", base_sha)
            code, rec = record.evaluate_text(card(body, corr, axes or AXES), files_at(rev),
                                             d, rev, battery=None)
            out = {"case": name, "expect": expect, "got": code, "ok": code == expect,
                   "defect": defect, "failing": rec.get("failing"),
                   "mismatches": [m["class"] + ":" + m["key"]
                                  for m in rec.get("mismatches", [])],
                   "exempted": [e["class"] + ":" + e["key"]
                                for e in rec.get("exempted", [])],
                   "corrections": rec.get("corrections"),
                   "atoms_by_class": rec.get("atoms_by_class")}
            if extra:
                out["extra"] = extra
            results.append(out)
            return out

        # ---- 0. control: an honest card with two re-deriving corrections is GREEN ---
        ca = command_a(tip)
        dp = record.depth_pair(files_at_rev)
        case("control-honest-card", 0, HONEST, list(CORR_BASE),
             extra={"record_depth_pair": list(dp), "command_a_depth_pair": list(ca),
                    "same_predicate": dp == ca},
             defect=None)

        # ---- 1. a per-wave FALSE split is exempted by a TOTAL-only correction ------
        case("seats-split-false-totals-true", 0,
             "Wave 1: 20 seats; wave 2: 20 seats. The window `git log %s..%s -- corpus/` "
             "is empty. Base `%s`. See `.ufo/waves/round-9/w1-dispatch.json`.\n" % (b8, t8, b8),
             CORR_BASE + ["- corrects seats round-9: 2 waves, 40 seats total"],
             defect="corrects() binds (n_waves, sum) only; the exempted atom's per-wave "
                    "numbers (claimed 20/20, dispatched 30/10) are never re-derived")

        # ---- 2. a dispatch SPEC nobody dispatched verifies the seat claim ----------
        case("seats-spec-not-dispatched", 0, HONEST, list(CORR_BASE),
             defect="dispatch_counts() reads counts.spawn from w<N>-dispatch.json alone; "
                    "the fixture has no *.ready, no *.ready.dispatched and no "
                    "*-results.json -- the round-46 wave-2 shape routed as R46-V1",
             extra={"round9_dir": sorted(os.listdir(os.path.join(d, ".ufo/waves/round-9"))),
                    "ready_anywhere": [p for p in
                                       subprocess.run(["find", d, "-name", "*.ready*"],
                                                      capture_output=True, text=True
                                                      ).stdout.split()]})

        # ---- 3a. an unverifiable <tip> window is exempted by a DEGENERATE window ---
        case("window-placeholder-exempted-degenerately", 0,
             "Waves: 30 + 10 = 40 seats. `git log %s..<tip> -- tools/x/` is empty at "
             "every measurement. Base `%s`. See `.ufo/waves/round-9/w1-dispatch.json`.\n" % (b8, b8),
             CORR_BASE + ["- corrects window round-9: empty in %s..%s -- tools/x/"
                          % (b8, b8)],
             defect="exempt() returns True for any window atom whose pair is None; the "
                    "correction then only has to be empty itself and A..A is empty by "
                    "construction, so the sentence's own window is never tested")

        # ---- 3b. the honest window for that same sentence is REJECTED --------------
        case("window-placeholder-honest-pair-rejected", 1,
             "Waves: 30 + 10 = 40 seats. `git log %s..<tip> -- tools/x/` is empty at "
             "every measurement. Base `%s`. See `.ufo/waves/round-9/w1-dispatch.json`.\n" % (b8, b8),
             CORR_BASE + ["- corrects window round-9: empty in %s..%s -- tools/x/"
                          % (b8, t8)],
             defect="base..tip touches tools/x, so the true window is non-empty; the "
                    "predicate prefers the vacuous correction to the honest one")

        # ---- 4. a non-ancestor revision is exempted (corrects() drops ancestry) ----
        case("rev-non-ancestor-exempted", 0,
             "Waves: 30 + 10 = 40 seats. The window `git log %s..%s -- corpus/` is empty. "
             "Base `BASE`. Measured tip `%s`. See `.ufo/waves/round-9/w1-dispatch.json`.\n"
             % (b8, t8, s8),
             CORR_BASE + ["- corrects rev %s: landed on a side branch" % s8],
             defect="derive() requires resolve AND merge-base --is-ancestor; corrects() "
                    "for rev checks rev-parse only, so the exemption is strictly weaker "
                    "than the atom it exempts",
             extra={"side_is_ancestor_of_tip":
                    git(d, "merge-base", "--is-ancestor", side, tip).returncode == 0})

        # ---- 5. path atoms exist only for `.ufo/waves/round-N/...` ------------------
        case("path-citation-outside-wave-dir-ignored", 0,
             HONEST + "Receipts `controls/ctl-c1-1-v1-profile.json`, `plans/nope.md` and "
             "`corpus/lessons/nope.md` are cited.\n",
             list(CORR_BASE),
             defect="WAVE_DIR matches only .ufo/waves/round-<N>/...; every other cited "
                    "path in the sections is not an atom, so R46-V7's four missing "
                    "receipt paths cannot fail this counter",
             extra={"exist": {p: os.path.exists(os.path.join(d, p)) for p in
                              ("controls/ctl-c1-1-v1-profile.json", "plans/nope.md",
                               "corpus/lessons/nope.md")}})

        # ---- 6. prose about LOG.md / a report is not an atom at all ----------------
        case("log-and-report-claims-not-atoms", 0,
             HONEST + "`LOG.md` says wave 2 dispatched 40 seats; the report says 32 of "
             "40 seats produced a report and no `*-results.json` exists.\n",
             list(CORR_BASE),
             defect="no class reads LOG.md, PROVINCE.md, a round report or a self-test "
                    "count; only SCORECARD's last two round sections and two axis rows "
                    "are in scope (R46-V1's LOG half, V4, V5, V6 are all outside)")

        # ---- 7. an exemption-free historical correction satisfies CORR_MIN ---------
        case("corrections-can-be-exemption-free", 0, HONEST,
             CORR_BASE + ["- corrects seats round-3: 2 waves, 50 seats total"],
             defect="A3's `historical` escape accepts a seats/window correction for any "
                    "round older than the window; it exempts nothing (exempted is empty) "
                    "yet counts toward CORR_MIN, so 'at least two re-derived corrections' "
                    "does not mean 'two defects repaired'")

        # ---- 8. doctor the ground-truth file, drop the correction -> GREEN ---------
        write(d, ".ufo/waves/round-9/w1-dispatch.json",
              json.dumps({"counts": {"spawn": 20, "resume": 0, "total": 20}}))
        write(d, ".ufo/waves/round-9/w2-dispatch.json",
              json.dumps({"counts": {"spawn": 20, "resume": 0, "total": 20}}))
        tip2 = commit(d, "r47: dispatch counts edited to match the claim")
        case("doctored-dispatch-dropped-correction", 0,
             "Wave 1: 20 seats; wave 2: 20 seats. The window `git log %s..%s -- corpus/` "
             "is empty. Base `%s`. See `.ufo/waves/round-9/w1-dispatch.json`.\n" % (b8, t8, b8),
             list(CORR_BASE),
             defect="seats ground truth is an unfrozen .ufo/waves/*-dispatch.json the "
                    "same round may commit; with the correction dropped the false split "
                    "is verified against the edited file (the claims file's kill rule "
                    "covers only the retained-correction case)",
             rev=tip2,
             extra={"dispatch_diff": git(d, "diff", "--stat", base, tip2, "--",
                                         ".ufo/waves/round-9/").stdout.strip()})
        write(d, ".ufo/waves/round-9/w1-dispatch.json",
              json.dumps({"counts": {"spawn": 30, "resume": 0, "total": 30}}))
        write(d, ".ufo/waves/round-9/w2-dispatch.json",
              json.dumps({"counts": {"spawn": 10, "resume": 0, "total": 10}}))

        # ---- 9. control: the same false split with no correction is RED ------------
        case("control-false-split-uncorrected", 1,
             "Wave 1: 20 seats; wave 2: 20 seats. The window `git log %s..%s -- corpus/` "
             "is empty. Base `%s`. See `.ufo/waves/round-9/w1-dispatch.json`.\n" % (b8, t8, b8),
             list(CORR_BASE), defect=None)

        # ---- 10. control: an honest card with no corrections is RED (CORR_MIN) -----
        case("control-honest-card-no-corrections", 1, HONEST, [], defect=None)

        # ---- 11. an `axes` correction line is NOT a correction at all -------------
        # CORR = r"^- corrects (seats|window|path|rev) (\S+):"  -- `axes` never matches,
        # so the axes branch of corrects() (record.py:280-291) is dead code and the
        # frozen clause "an `axes` correction must state <resolved>/<total>" cannot fire.
        case("axes-correction-false-line-ignored", 0, HONEST,
             list(CORR_BASE) + ["- corrects axes coverage: 999/999"],
             defect="CORR's class alternation omits `axes`, so the line is neither "
                    "counted, re-derived, nor flagged: a false axes correction passes "
                    "silently and the frozen clause 3 axes arm is unreachable")

        # ---- 12. an `axes` correction cannot repair a false axis head -------------
        case("axes-head-false-unrepairable", 1,
             HONEST, list(CORR_BASE) + ["- corrects axes coverage: 1/1"],
             defect="the counter's only path for a wrong axis head is an exemption that "
                    "cannot be parsed, so the documented repair mechanism is dead; the "
                    "landed card fixes the heads by editing them instead",
             axes=AXES.replace("1/1 knowledge files mapped", "2/2 knowledge files mapped"))

        summary = {"fixture_repo": d, "base": base, "tip": tip, "side": side,
                   "cases": results,
                   "reproduced": sum(1 for r in results if r["ok"]),
                   "total": len(results),
                   "green_by_defect": sum(1 for r in results
                                          if r["ok"] and r["got"] == 0 and r["defect"])}
        print(json.dumps(summary, indent=1))
        return 0 if summary["reproduced"] == summary["total"] else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
