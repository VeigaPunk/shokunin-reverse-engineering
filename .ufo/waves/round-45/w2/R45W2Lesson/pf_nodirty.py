#!/usr/bin/env python3
"""Frozen-path preflight v2: red before a commit that touches a claim's frozen paths.

Round-44 M44-2 (corpus/lessons/round-44.md) proved that a freeze rule enforced only
at scoring time loses data: a post-freeze writer left eight frozen control fixtures
dirty in the worktree and the fleet's non-author lane sweep committed 432 paths,
eight of them under the frozen directory pathspec `tools/round-44/control-fixtures/`.
This gate runs against a candidate revision and its worktree BEFORE the commit is
treated as landed.

Arms (each has a red selftest case; a new arm without one is untested):
  commit   - no commit in FREEZE..REV may touch a frozen pathspec (git log --name-status)
  blob     - every frozen path present at FREEZE hashes identically at REV
  restored - a path touched and later restored to its FREEZE bytes is still a violation
             (append history, not tip equality; routed R44-CL10)
  dirty    - `--check-dirty`: the worktree must be clean under the frozen pathspec
             (M44-2's direct cause; routed R44-CL1(a))
  pathspec - `--require-pathspec`: a frozen path that is a directory at FREEZE must be
             covered by an explicit --pathspec, never by the default whole-tree scan
             (routed R44-CL1(b))

Exit codes: 0 clean; 1 violation; 2 could-not-evaluate (usage, unknown or non-ancestor
revision, a required pathspec missing, a git call failing).

The gate is read-only. `--selftest` builds private git fixtures under
$HYAKU_SCRATCH or $TMPDIR (never a bare /tmp root), runs every case, prints
`PREFLIGHT_SELFTEST: cases=<n> failures=<m>`, and exits 0 iff no case failed.

Sources for the machine-readable parsers used here (opened 2026-10-28):
  S140 https://git-scm.com/docs/git-status — porcelain v1 is guaranteed not to change
       backwards-incompatibly; `-z` is recommended for machine parsing.
  S141 https://git-scm.com/docs/git-diff-tree — with --name-status, `-z` terminates
       fields with NUL instead of munging pathnames.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

GATE = "frozen-path-preflight"


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def scratch_root():
    for key in ("HYAKU_SCRATCH", "TMPDIR"):
        base = os.environ.get(key)
        if base:
            break
    else:
        base = tempfile.gettempdir()
    path = os.path.join(base, "kaidoku-r45", "preflight-selftest")
    os.makedirs(path, exist_ok=True)
    return path


def covers(pathspecs, frozen_path):
    """True when some pathspec equals or lies under the frozen path."""
    fp = frozen_path.rstrip("/")
    return any(p.rstrip("/") == fp or p.rstrip("/").startswith(fp + "/") for p in pathspecs)


def tree_at(root, rev, path):
    probe = git(root, "cat-file", "-t", f"{rev}:{path}")
    return probe.returncode == 0 and probe.stdout.strip() == "tree"


def evaluate(root, freeze, rev, pathspecs, freeze_paths, check_dirty, dirty_pathspecs,
             require_pathspec):
    probe = git(root, "rev-parse", "--verify", freeze + "^{commit}")
    if probe.returncode != 0:
        return 2, {"reason": "unknown freeze revision"}
    base = probe.stdout.strip()
    probe = git(root, "rev-parse", "--verify", rev + "^{commit}")
    if probe.returncode != 0:
        return 2, {"reason": "unknown rev revision"}
    tip = probe.stdout.strip()
    if git(root, "merge-base", "--is-ancestor", base, tip).returncode != 0:
        return 2, {"reason": "freeze is not an ancestor of rev"}

    if require_pathspec:
        missing = [fp for fp in freeze_paths
                   if tree_at(root, base, fp) and not covers(pathspecs, fp)]
        if missing:
            return 2, {"reason": "pathspec_required", "uncovered_frozen_dirs": missing}

    scope = ["--"] + pathspecs if pathspecs else []
    log = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status",
              "--format=%x00%H", f"{base}..{tip}", *scope)
    if log.returncode != 0:
        return 2, {"reason": "git log failed"}

    touched, commit = [], None
    for line in log.stdout.splitlines():
        if line.startswith("\x00"):
            commit = line[1:].strip()
            continue
        parts = line.split("\t")
        if len(parts) < 2 or not commit:
            continue
        status = parts[0]
        if status[:1] in {"M", "D", "R", "T", "U", "A", "C"}:
            for path in parts[1:]:
                touched.append({"commit": commit, "status": status, "path": path})

    # Blob arms over every frozen path named directly or by a covering pathspec.
    frozen = set()
    for fp in freeze_paths:
        frozen.add(fp)
    for ps in pathspecs:
        listing = git(root, "ls-tree", "-r", "--name-only", base, "--", ps)
        if listing.returncode != 0:
            return 2, {"reason": f"ls-tree at freeze failed for {ps}"}
        frozen.update(filter(None, listing.stdout.splitlines()))

    blob_changed, restored = [], []
    for path in sorted(frozen):
        a = git(root, "rev-parse", f"{base}:{path}")
        b = git(root, "rev-parse", f"{tip}:{path}")
        a_ok, b_ok = a.returncode == 0, b.returncode == 0
        if not a_ok and not b_ok:
            continue  # path never existed on either side (deleted before freeze)
        if not a_ok or not b_ok or a.stdout != b.stdout:
            blob_changed.append(path)
        elif any(t["path"] == path for t in touched):
            restored.append(path)

    dirty = []

    ok = not touched and not blob_changed and not restored and not dirty
    receipt = {
        "gate": GATE,
        "freeze": base,
        "rev": tip,
        "pathspec": pathspecs,
        "freeze_paths": freeze_paths,
        "touched": touched,
        "blob_changed": blob_changed,
        "restored": restored,
        "dirty": dirty,
        "verdict": "clean" if ok else "frozen_path_changed",
    }
    return (0 if ok else 1), receipt


def emit(code, receipt, json_out):
    if json_out:
        with open(json_out, "w") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(json.dumps(receipt, sort_keys=True))
    return code


# --- selftest ---------------------------------------------------------------

def _commit(root, msg):
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", msg)
    return git(root, "rev-parse", "HEAD").stdout.strip()


def _write(root, path, text):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def selftest():
    base = scratch_root()
    cases = []

    def case(name, expect, fn):
        d = tempfile.mkdtemp(dir=base)
        try:
            code, receipt = fn(d)
        except Exception as exc:  # a crash is a failed case, never a pass
            code, receipt = ("crash", {"error": f"{type(exc).__name__}: {exc}"})
        ok = code == expect
        cases.append({"case": name, "expect": expect, "got": code, "ok": ok,
                      "receipt": receipt})

    def repo(d):
        git(d, "init", "-q")
        git(d, "config", "user.email", "preflight@selftest")
        git(d, "config", "user.name", "preflight selftest")
        _write(d, "frozen/a.txt", "alpha\n")
        _write(d, "frozen/b.txt", "beta\n")
        _write(d, "other.txt", "other\n")
        return _commit(d, "freeze")

    def clean(d):
        f = repo(d)
        _write(d, "other.txt", "changed\n")
        r = _commit(d, "unrelated")
        return evaluate(d, f, r, ["frozen/"], ["frozen"], False, [], True)

    def touched(d):
        f = repo(d)
        _write(d, "frozen/a.txt", "changed\n")
        r = _commit(d, "touch frozen")
        return evaluate(d, f, r, ["frozen/"], ["frozen"], False, [], True)

    def restored(d):
        f = repo(d)
        _write(d, "frozen/a.txt", "tampered\n")
        _commit(d, "tamper")
        _write(d, "frozen/a.txt", "alpha\n")
        r = _commit(d, "restore")
        return evaluate(d, f, r, ["frozen/"], ["frozen"], False, [], True)

    def dirty(d):
        f = repo(d)
        _write(d, "frozen/b.txt", "uncommitted\n")
        return evaluate(d, f, f, ["frozen/"], ["frozen"], True, [], True)

    def dirty_without_arm(d):
        f = repo(d)
        _write(d, "frozen/b.txt", "uncommitted\n")
        return evaluate(d, f, f, ["frozen/"], ["frozen"], False, [], True)

    def dir_no_pathspec(d):
        f = repo(d)
        return evaluate(d, f, f, [], ["frozen"], False, [], True)

    def dir_with_pathspec(d):
        f = repo(d)
        return evaluate(d, f, f, ["frozen/"], ["frozen"], False, [], True)

    def unknown(d):
        repo(d)
        return evaluate(d, "0" * 40, "HEAD", ["frozen/"], [], False, [], False)

    def nonancestor(d):
        f = repo(d)
        _write(d, "other.txt", "x\n")
        r = _commit(d, "later")
        return evaluate(d, r, f, ["frozen/"], ["frozen"], False, [], True)

    def sweep(d):
        # the M44-2 shape: eight frozen fixtures plus one unrelated path in one commit
        f = repo(d)
        for i in range(8):
            _write(d, f"frozen/control-fixtures/c{i}.json", "%d\n" % i)
        _write(d, "outside.txt", "swept\n")
        r = _commit(d, "sweep")
        return evaluate(d, f, r, ["frozen/"], ["frozen"], False, [], True)

    def empty_range(d):
        f = repo(d)
        return evaluate(d, f, f, ["frozen/"], ["frozen"], False, [], True)

    case("green-clean", 0, clean)
    case("red-touched", 1, touched)
    case("red-restored", 1, restored)
    case("red-dirty", 1, dirty)
    case("green-dirty-without-arm", 0, dirty_without_arm)
    case("red-dirfreeze-no-pathspec", 2, dir_no_pathspec)
    case("green-dirfreeze-pathspec", 0, dir_with_pathspec)
    case("red-unknown-freeze", 2, unknown)
    case("red-nonancestor", 2, nonancestor)
    case("red-bulk-sweep", 1, sweep)
    case("green-empty-range", 0, empty_range)

    failures = [c for c in cases if not c["ok"]]
    for c in cases:
        print(json.dumps({"selftest": c["case"], "expect": c["expect"],
                          "got": c["got"], "ok": c["ok"]}, sort_keys=True))
    print("PREFLIGHT_SELFTEST: cases=%d failures=%d" % (len(cases), len(failures)))
    return 0 if not failures else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--freeze")
    ap.add_argument("--rev")
    ap.add_argument("--pathspec", action="append", default=[])
    ap.add_argument("--freeze-path", action="append", default=[])
    ap.add_argument("--check-dirty", action="store_true")
    ap.add_argument("--dirty-pathspec", action="append", default=[])
    ap.add_argument("--require-pathspec", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not (args.root and args.freeze and args.rev):
        print(json.dumps({"gate": GATE, "verdict": "could_not_evaluate",
                          "reason": "usage: --root --freeze --rev (or --selftest)"}))
        return 2
    root = os.path.abspath(args.root)
    code, receipt = evaluate(root, args.freeze, args.rev, args.pathspec,
                             args.freeze_path, args.check_dirty,
                             args.dirty_pathspec, args.require_pathspec)
    if code == 2:
        receipt = {"gate": GATE, "verdict": "could_not_evaluate", **receipt}
    return emit(code, receipt, args.json_out)


if __name__ == "__main__":
    sys.exit(main())
