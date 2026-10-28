#!/usr/bin/env python3
"""Round-47 C2 WINDOW-class attack harness (frozen tools/round-47/record.py @5017e1f).

One deterministic fixture repo; other atom classes held green (depth cites a path that
exists at every card rev). Each case runs the frozen counter TWICE:

  A  no window correction  -> exit 0 means the forged window claim alone is accepted
  B  a window correction over the SAME pair with a DEAD pathspec
     -> exit 0 means a false claim is laundered by a correction that is itself empty
        for a reason the atom never stated (clause 4 binds the pair only)

Receipt per run: exact command, exit, stdout sha256, UTC, receipt slice, independent
git ground truth.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

S = os.environ["HYAKU_SCRATCH"]
RECORD = os.environ.get("RECORD_OVERRIDE") or os.path.join(S, "inst/tools/round-47/record.py")
MATRIX_OUT = os.environ.get("MATRIX_OUT") or os.path.join(S, "matrix.json")
DATE = "2026-10-01T00:00:00+0000"
CORR_HEAD = "## Record corrections \u2014 round 47"
DEAD = "tools/none/"

SKILL = ("## Queue-drain craft \n\n"
         "- **rule one.** see `tools/z/keep.md:1`.\n\n"
         "## After craft\n")
README = "# readme\n\n## Coverage map\n\n- 2026-10-01-x \u2014 x\n\n## Gaps\n\ntail\n"
PATH9 = ".ufo/waves/round-9/w1-dispatch.json"

CARD_HEAD = """# card

## Owned axes

| Axis | Baseline - current score, 0-10 | Observable and limitation | Evidence | Round |
|---|---|---|---|---|
| coverage | 0 - 10 | 1/1 knowledge files mapped | x | r1 |
| depth | 0 - 10 | 1/1 rule blocks cited | x | r1 |

## Round 8

An earlier round with no atoms.

## Round 9

Base `{rev8}`. Waves: 1 + 1 = 2 seats. Wave 1: 1 seats; wave 2: 1 seats.
{window}
See `{path}`.
"""


def run(args, env=None):
    e = dict(os.environ, GIT_AUTHOR_DATE=DATE, GIT_COMMITTER_DATE=DATE,
             GIT_AUTHOR_NAME="r47 fixture", GIT_AUTHOR_EMAIL="fx@r47.invalid",
             GIT_COMMITTER_NAME="r47 fixture", GIT_COMMITTER_EMAIL="fx@r47.invalid")
    if env:
        e.update(env)
    return subprocess.run(args, capture_output=True, text=True, env=e)


def g(d, *args):
    return run(["git", "-C", d, *args])


def must(d, *args):
    r = g(d, *args)
    if r.returncode != 0:
        raise SystemExit("git %s failed: %s %s" % (" ".join(args), r.returncode,
                                                   r.stderr.strip()))
    return r.stdout.strip()


def w(d, path, body):
    full = os.path.join(d, path)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(body)


def commit(d, msg):
    must(d, "add", "-A")
    must(d, "commit", "-q", "-m", msg)
    return must(d, "rev-parse", "HEAD")


def sha(t):
    return hashlib.sha256(t.encode()).hexdigest()


def main():
    d = tempfile.mkdtemp(dir=S, prefix="fx-")
    try:
        assert run(["git", "-C", d, "init", "-q"]).returncode == 0
        top = must(d, "rev-parse", "--show-toplevel")
        assert os.path.realpath(top) == os.path.realpath(d), (top, d)
        must(d, "config", "user.email", "fx@r47.invalid")
        must(d, "config", "user.name", "r47 fixture")
        must(d, "checkout", "-q", "-b", "main")

        w(d, "tools/y/keep.md", "k1\n")
        w(d, "tools/other/a.md", "a1\n")
        w(d, "corpus/knowledge/2026-10-01-x.md", "x\n")
        w(d, "corpus/README.md", README)
        w(d, "SKILL.md", SKILL)
        w(d, ".ufo/waves/round-9/w1-dispatch.json", '{"counts": {"spawn": 1}}')
        w(d, ".ufo/waves/round-9/w2-dispatch.json", '{"counts": {"spawn": 1}}')
        c1 = commit(d, "c1 base")

        w(d, "tools/other/a.md", "a2\n")
        c2 = commit(d, "c2 touches tools/other only")

        w(d, "tools/y/keep.md", "k2\n")
        c3 = commit(d, "c3 touches tools/y/keep.md")

        os.makedirs(os.path.join(d, "tools/z"), exist_ok=True)
        must(d, "mv", "tools/y/keep.md", "tools/z/keep.md")
        c4 = commit(d, "c4 rename tools/y -> tools/z (rename only)")

        w(d, "tools/other/a.md", "a3\n")
        c5 = commit(d, "c5 tools/other again; tools/y/ is gone")

        must(d, "checkout", "-q", "-b", "side")
        w(d, "tools/q/q.md", "q\n")
        s1 = commit(d, "s1 side touches tools/q")
        must(d, "checkout", "-q", "main")
        run(["git", "-C", d, "merge", "--no-ff", "--no-commit", "side"])
        w(d, "tools/z/keep.md", "kmerged\n")
        merge = commit(d, "merge side; resolution edits tools/z/keep.md")

        must(d, "checkout", "-q", "--orphan", "orphan-br")
        run(["git", "-C", d, "rm", "-rq", "--cached", "."])
        for name in ("tools", "corpus", "SKILL.md", ".ufo"):
            p = os.path.join(d, name)
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.exists(p):
                os.remove(p)
        w(d, "tools/other/o.md", "o\n")
        orphan = commit(d, "orphan root: tools/other/o.md only")
        must(d, "checkout", "-q", "main")

        def truth(*args):
            r = g(d, *args)
            return {"cmd": "git -C $FIX " + " ".join(args), "exit": r.returncode,
                    "stdout_sha256": sha(r.stdout), "stdout_bytes": len(r.stdout),
                    "stdout_head": r.stdout[:160]}

        gt = {
            "c2_c3_tools_y_forward": truth("log", "--name-status", "--format=",
                                           "%s..%s" % (c2, c3), "--", "tools/y/"),
            "c3_c2_tools_y_reversed": truth("log", "--name-status", "--format=",
                                            "%s..%s" % (c3, c2), "--", "tools/y/"),
            "c3_c4_rename_oldpath": truth("log", "--name-status", "--format=",
                                          "%s..%s" % (c3, c4), "--", "tools/y/keep.md"),
            "c3_c4_rename_newpath": truth("log", "--name-status", "--format=",
                                          "%s..%s" % (c3, c4), "--", "tools/z/keep.md"),
            "c5_merge_plain_name_status": truth("log", "--name-status", "--format=",
                                                "%s..%s" % (c5, merge), "--",
                                                "tools/z/keep.md"),
            "c5_merge_first_parent": truth("log", "-m", "--diff-merges=first-parent",
                                           "--name-status", "-z", "--format=",
                                           "%s..%s" % (c5, merge), "--",
                                           "tools/z/keep.md"),
            "c5_merge_diff": truth("diff", "--name-status", c5, merge, "--",
                                   "tools/z/keep.md"),
        }

        def card(window, rev8, corrections):
            return CARD_HEAD.format(rev8=rev8, window=window, path=PATH9) + "\n" + \
                corrections

        CASES = [
            ("k00-baseline-honest-empty", c1, c2, "tools/y/", None,
             "genuinely empty window; control"),
            ("k01-abbrev7", c1[:7], c2[:7], "tools/y/", None,
             "7-hex abbreviations (git's default short form)"),
            ("k02-abbrev6", c1[:6], c2[:6], "tools/y/", None,
             "6-hex abbreviation: below the {7,40} floor, never resolved"),
            ("k03-abbrev-blob-base", "BLOBC3", c1[:8], "tools/y/", None,
             "base is a BLOB object id, not a commit"),
            ("k04-path-does-not-exist", c1, c2, "tools/y/nope/", None,
             "pathspec names no path at any revision"),
            ("k05-pathspec-empty-nondegenerate", c1, c2, "", None,
             "empty pathspec, range has one commit"),
            ("k06-pathspec-empty-degenerate", c2, c2, "", None,
             "empty pathspec AND degenerate range: nothing verified"),
            ("k07-reversed-pair", c3, c2, "tools/y/", None,
             "reversed pair; the forward c2..c3 changes tools/y/"),
            ("k08-degenerate-pair", c3, c3, "tools/y/", None,
             "X..X is empty for every pathspec"),
            ("k09-tip-not-ancestor-of-rev", c1, "ORPHAN", "tools/y/", None,
             "window tip is an orphan commit unreachable from --rev"),
            ("k10-glob-rewritten-to-dir", c2, c3, "tools/y/*.txt", None,
             "stated glob *.txt matches nothing; extraction stops at '*'"),
            ("k11-prose-without-pair", None, None, None, "The dangling list is empty.",
             "ordinary prose becomes an unverifiable window atom"),
            ("k12-two-pairs-one-line", c1, c2, "tools/y/", None,
             "first pair on the line is empty, second (c2..c3) is not"),
            ("k13-rename-old-path", c3, c4, "tools/y/keep.md", None,
             "rename-only range, pathspec is the OLD path"),
            ("k14-rename-new-path", c3, c4, "tools/z/keep.md", None,
             "rename-only range, pathspec is the NEW path"),
            ("k15-dead-dir-after-rename", c4, c5, "tools/y/", None,
             "pathspec directory was removed by a rename before the window"),
            ("k16-merge-only-change", c5, merge, "tools/z/keep.md", None,
             "the only commit in range touching the path is a merge resolution"),
            ("k18-merge-plus-nonmerge-control", c3, merge, "tools/z/keep.md", None,
             "control: c4 (a non-merge rename) also touches tools/z/keep.md in range"),
            ("k20-launder-red-atom", c2, c3, "tools/y/keep.md", None,
             "atom is RED (non-empty); correction over the same pair + dead path"),
        ]

        rows = []

        def measure(name, window_line, corrections, tag):
            w(d, "SCORECARD.md", card(window_line, c1[:8], corrections))
            rev = commit(d, "card %s/%s" % (name, tag))
            cmd = [sys.executable, "-I", "-B", RECORD, "--root", d, "--rev", rev,
                   "--no-battery"]
            utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            r = run(cmd)
            try:
                rec = json.loads(r.stdout)
            except ValueError:
                rec = {"unparsable": r.stdout[:300], "stderr": r.stderr[:300]}
            mm = rec.get("mismatches") or []
            return {"arm": tag, "rev": rev, "card_commit": rev,
                    "command": "python3 -I -B $S/inst/tools/round-47/record.py "
                               "--root $FIX --rev " + rev + " --no-battery",
                    "utc": utc, "exit": r.returncode,
                    "stdout_sha256": sha(r.stdout),
                    "failing": rec.get("failing"),
                    "window_mismatches": [m for m in mm if m["class"] == "window"],
                    "all_mismatches": [(m["class"], str(m["key"]),
                                        json.dumps(m["derived"])[:160]) for m in mm],
                    "corrections": rec.get("corrections"),
                    "corrections_bad": rec.get("corrections_bad"),
                    "exempted": [e["class"] for e in (rec.get("exempted") or [])],
                    "battery": {k: rec.get("battery", {}).get(k)
                                for k in ("correction_forgeries", "forgeries_green")},
                    "receipt_atoms_by_class": rec.get("atoms_by_class")}

        def resolve(tok):
            if tok == "ORPHAN":
                return orphan
            if tok == "BLOBC3":
                return must(d, "rev-parse", c3 + ":tools/y/keep.md")[:8]
            return tok

        for name, lo, hi, paths, literal, note in CASES:
            if literal is not None:
                line = literal
                pair = None
            elif name == "k12-two-pairs-one-line":
                line = ("`git log %s..%s -- %s` is empty and `git log %s..%s -- %s` is empty."
                        % (c1, c2, paths, c2, c3, paths))
                pair = (c1, c2)
            else:
                lo, hi = resolve(lo), resolve(hi)
                sep = " -- " + paths if paths else " -- "
                line = "`git log %s..%s%s` is empty." % (lo, hi, sep)
                pair = (lo, hi) if len(lo) >= 7 else None
            base_corr = (CORR_HEAD + "\n\n"
                         "- corrects seats round-9: 2 waves, 2 seats total\n"
                         "- corrects path %s: landed\n" % PATH9)
            arms = [("A-no-window-correction", base_corr)]
            if pair:
                arms.append(("B-dead-path-window-correction",
                             base_corr + "- corrects window round-9: empty in %s..%s -- %s\n"
                             % (pair[0], pair[1], DEAD)))
            for tag, corr in arms:
                rows.append(dict(name=name, window_sentence=line, note=note,
                                 **measure(name, line, corr, tag)))

        out = {"fixture_root_template": "$S/fx-*", "record_py": RECORD,
               "record_py_sha256": sha(open(RECORD).read()),
               "revs": {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5,
                        "side": s1, "merge": merge, "orphan": orphan},
               "ground_truth": gt, "runs": rows}
        text = json.dumps(out, indent=1, sort_keys=True)
        open(MATRIX_OUT, "w").write(text + "\n")
        print(text)
    finally:
        shutil.rmtree(d, ignore_errors=True)


main()
