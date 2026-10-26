#!/usr/bin/env python3
"""absence-sweep.py -- certify a *negative* existence claim the way R38-CL1 needed.

The round-38 false-green was a `find` rooted at /home/vgpnk/Projects/shokunin for the staged path
`lanes/kaidoku/round7/work/r7-local-measurements.tsv`, which printed nothing -- while `lanes/...` is
relative to the shokuknow base and the file was there all along. A negative existence claim is only
as good as the roots it was swept from, so this tool makes the roots an explicit, repeated,
mandatory argument and refuses to certify absence it could not fully observe.

Usage:
  python3 -I -B absence-sweep.py --claim RELPATH --root R1 [--root R2 ...] [--json] [--max-hits N]
  python3 -I -B absence-sweep.py --selftest

Verdict / exit codes (none other are produced):
  0 ABSENT    no file under any root whose path ends with RELPATH (all roots fully readable)
  1 PRESENT   at least one hit; every hit is printed to stdout, one per line
  2 EXIT_ERROR  usage error, unreadable/missing root, or ABSENT with unreadable subtrees
                (absence that could not be fully observed is reported, never certified)

Match rule: component-aligned suffix. RELPATH must be relative, `..`-free and literal (glob
metacharacters are a usage error, because a glob would match nothing and certify a false ABSENT). A
candidate path matches
when its trailing components equal RELPATH's components, so `xr7-local-measurements.tsv` and
`r7-local-measurements.tsv.bak` never match `r7-local-measurements.tsv`. Directory symlinks are not
followed; a symlink whose own path matches is reported as a hit with kind `symlink`.

Duplicate roots, and any root nested inside another root, are dropped before the walk (roots are
compared by real path), so one file is never walked or listed twice.

Anchoring note: an ABSENT verdict from roots that hold no directory named after the claim's first
component cannot be the base the staged path was written against (`lanes/...` is relative to the
shokuknow root, not the fleet root). That case still exits 0 as specified, and adds a stderr
`NOTE claim is unanchored ...`; the `--json` form carries `anchored_roots`.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

ABSENT, PRESENT, EXIT_ERROR = 0, 1, 2
VCS_DIRS = {".git"}  # still walked: a hit inside .git is a hit


class UsageError(Exception):
    pass


def norm_claim(claim):
    if not claim:
        raise UsageError("--claim is empty")
    if os.path.isabs(claim):
        raise UsageError("--claim must be relative, got absolute path %r" % claim)
    parts = [p for p in claim.replace(os.sep, "/").split("/") if p not in ("", ".")]
    if not parts:
        raise UsageError("--claim has no path components: %r" % claim)
    if ".." in parts:
        raise UsageError("--claim must not contain '..': %r" % claim)
    # A glob in the claim would silently match nothing and certify a false ABSENT.
    if any(ch in claim for ch in "*?["):
        raise UsageError("--claim must be a literal path, not a glob: %r" % claim)
    return parts


def root_of(path):
    """Real path used for nesting/dedup decisions; never raises."""
    try:
        return os.path.realpath(path)
    except OSError:
        return path


def prepare_roots(roots):
    if not roots:
        raise UsageError("at least one --root is required")
    prepared, errors = [], []
    for r in roots:
        if not os.path.isdir(r):
            errors.append("root is missing or not a directory: %s" % r)
            continue
        try:
            with os.scandir(r):
                pass
        except OSError as exc:
            errors.append("root is unreadable: %s (%s)" % (r, exc.strerror or exc))
            continue
        prepared.append(os.path.abspath(r))
    if errors:
        raise UsageError("; ".join(errors))
    # Drop exact duplicate roots and any root nested inside another root, so one file is
    # never walked (or listed) twice.
    kept, kept_real = [], []
    for r in sorted(prepared, key=lambda p: (len(root_of(p)), p)):
        rp = root_of(r)
        if any(rp == k or rp.startswith(k.rstrip(os.sep) + os.sep) for k in kept_real):
            continue
        kept.append(r)
        kept_real.append(rp)
    return kept


def sweep(claim_parts, roots, max_hits):
    n = len(claim_parts)
    hits = []
    stats = {"dirs_walked": 0, "entries_seen": 0, "skipped_dirs": 0, "truncated": False}
    for root in roots:
        stack = [root]
        while stack:
            cur = stack.pop()
            stats["dirs_walked"] += 1
            try:
                entries = list(os.scandir(cur))
            except OSError:
                stats["skipped_dirs"] += 1
                continue
            for ent in entries:
                stats["entries_seen"] += 1
                try:
                    is_dir = ent.is_dir(follow_symlinks=False)
                except OSError:
                    is_dir = False
                if is_dir:
                    stack.append(ent.path)
                    continue
                parts = ent.path.split(os.sep)
                if parts[-n:] != claim_parts:
                    continue
                try:
                    kind = "symlink" if ent.is_symlink() else "file"
                except OSError:
                    kind = "file"
                try:
                    size = ent.stat(follow_symlinks=False).st_size
                except OSError:
                    size = -1
                if len(hits) >= max_hits:
                    stats["truncated"] = True
                    continue
                hits.append({"path": ent.path, "kind": kind, "size": size, "root": root})
    hits.sort(key=lambda h: h["path"])
    return hits, stats


def run(claim, roots, max_hits=100, json_out=False):
    claim_parts = norm_claim(claim)
    if max_hits < 1:
        raise UsageError("--max-hits must be >= 1")
    usable = prepare_roots(roots)
    t0 = time.time()
    hits, stats = sweep(claim_parts, usable, max_hits)
    elapsed = time.time() - t0

    if hits:
        verdict, code = "PRESENT", PRESENT
    elif stats["skipped_dirs"]:
        verdict, code = "INCOMPLETE", EXIT_ERROR
    else:
        verdict, code = "ABSENT", ABSENT

    # Anchoring note: `lanes/kaidoku/...` is relative to a base that actually holds `lanes/`.
    # A sweep whose roots hold no such leading directory cannot be the base the staged path was
    # written against (the R38-CL1 mistake), so say so -- as a note, never as an exit change.
    anchored = []
    if len(claim_parts) > 1:
        anchored = [r for r in usable if os.path.isdir(os.path.join(r, claim_parts[0]))]
    note = None
    if verdict == "ABSENT" and len(claim_parts) > 1 and not anchored:
        note = ("NOTE claim is unanchored: no root holds a %r directory, so ABSENT only covers "
                "these roots and not the base the staged path is relative to" % claim_parts[0])

    if json_out:
        print(json.dumps({
            "claim": claim,
            "roots": usable,
            "anchored_roots": anchored,
            "verdict": verdict,
            "exit_code": code,
            "hits": hits,
            "skipped_dirs": stats["skipped_dirs"],
            "dirs_walked": stats["dirs_walked"],
            "entries_seen": stats["entries_seen"],
            "truncated": stats["truncated"],
            "elapsed_s": round(elapsed, 3),
        }, indent=1, sort_keys=True))
    else:
        for h in hits:
            print("HIT %s kind=%s size=%d root=%s" % (h["path"], h["kind"], h["size"], h["root"]))
        print("VERDICT %s claim=%s roots=%d hits=%d dirs_walked=%d skipped_dirs=%d elapsed=%.3fs"
              % (verdict, claim, len(usable), len(hits), stats["dirs_walked"],
                 stats["skipped_dirs"], elapsed))
    if note:
        sys.stderr.write(note + "\n")
    if stats["skipped_dirs"]:
        sys.stderr.write("WARNING unreadable_subtrees=%d: %s\n" % (
            stats["skipped_dirs"],
            "absence not certified" if verdict == "INCOMPLETE" else "presence shown anyway"))
    if stats["truncated"]:
        sys.stderr.write("WARNING hit list truncated at --max-hits %d\n" % max_hits)
    return code


# --------------------------------------------------------------------------- selftest

def _mk(root, rel, data=b"x"):
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def selftest():
    script = os.path.abspath(__file__)
    base = tempfile.mkdtemp(prefix="absence-sweep-selftest-")
    claim = "lanes/kaidoku/round7/work/r7-local-measurements.tsv"
    cases = []

    def case(name, argv, want_code, want_substrs=(), want_absent_substrs=(), cwd=None,
             setup=None, teardown=None):
        cases.append({"name": name, "argv": argv, "want_code": want_code,
                      "want": want_substrs, "reject": want_absent_substrs, "cwd": cwd or base,
                      "setup": setup, "teardown": teardown})

    # 1. nothing anywhere -> ABSENT
    empty = os.path.join(base, "c1-empty")
    os.makedirs(empty, exist_ok=True)
    case("absent-empty-root", ["--claim", claim, "--root", empty], ABSENT, ["VERDICT ABSENT"])

    # 2. exact hit deep under a root -> PRESENT, one hit
    hitroot = os.path.join(base, "c2-hit")
    _mk(hitroot, claim)
    case("present-exact", ["--claim", claim, "--root", hitroot], PRESENT,
         ["VERDICT PRESENT", "hits=1", claim])

    # 3. the R38-CL1 shape: clean root first, real file under the second root
    clean = os.path.join(base, "c3-clean")
    other = os.path.join(base, "c3-other")
    os.makedirs(clean, exist_ok=True)
    _mk(other, claim)
    case("present-second-root", ["--claim", claim, "--root", clean, "--root", other], PRESENT,
         ["VERDICT PRESENT", "hits=1", "c3-other"])
    # ... and the false green it replaces: sweeping only the clean root
    case("multi-root-only-clean-is-absent", ["--claim", claim, "--root", clean], ABSENT,
         ["VERDICT ABSENT"])

    # 4. suffix look-alikes must not match (component boundary)
    decoy = os.path.join(base, "c4-decoy")
    _mk(decoy, "lanes/kaidoku/round7/work/xr7-local-measurements.tsv")
    _mk(decoy, "lanes/kaidoku/round7/work/r7-local-measurements.tsv.bak")
    # string-tail decoy: endswith(claim) is true here, component match is not
    _mk(decoy, "xlanes/kaidoku/round7/work/r7-local-measurements.tsv")
    case("substring-decoy", ["--claim", claim, "--root", decoy], ABSENT,
         ["VERDICT ABSENT"], ["HIT "])

    # 5. missing root -> 2 (never a silent ABSENT)
    case("missing-root", ["--claim", claim, "--root", os.path.join(base, "c5-nope")], EXIT_ERROR,
         [], ["VERDICT"])

    # 6. root that is a regular file -> 2
    file_root = _mk(os.path.join(base, "c6"), "one.txt")
    case("file-root", ["--claim", claim, "--root", file_root], EXIT_ERROR, [], ["VERDICT"])

    # 7. no --claim -> 2 (usage)
    case("missing-claim", ["--root", empty], EXIT_ERROR, [], ["VERDICT"])

    # 8. absolute / dotdot claims -> 2
    case("absolute-claim", ["--claim", "/" + claim, "--root", empty], EXIT_ERROR, [], ["VERDICT"])
    case("dotdot-claim", ["--claim", "../work/r7-local-measurements.tsv", "--root", empty],
         EXIT_ERROR, [], ["VERDICT"])

    # 9. nested roots must not double-count
    outer = os.path.join(base, "c9-outer")
    _mk(outer, claim)
    case("nested-roots-dedup", ["--claim", claim, "--root", outer,
                                "--root", os.path.join(outer, "lanes")], PRESENT,
         ["VERDICT PRESENT", "hits=1"])
    case("duplicate-roots-dedup", ["--claim", claim, "--root", outer, "--root", outer], PRESENT,
         ["VERDICT PRESENT", "hits=1"])

    # 10. symlink whose own path matches is a hit, reported as such
    linkroot = os.path.join(base, "c10-link")
    target = _mk(os.path.join(base, "c10-target"), "real.tsv")
    link = os.path.join(linkroot, *claim.split("/"))
    os.makedirs(os.path.dirname(link), exist_ok=True)
    os.symlink(target, link)
    case("symlink-hit", ["--claim", claim, "--root", linkroot], PRESENT,
         ["VERDICT PRESENT", "kind=symlink"])

    # 12. an unreadable subtree makes absence unobservable: INCOMPLETE, exit 2, never ABSENT.
    # The mode is applied at run time (setup) and restored after (teardown), so the case really
    # observes a live EACCES; 12b re-runs the same tree once it is readable and gets ABSENT.
    dark = os.path.join(base, "c12-dark")
    _mk(dark, "keep/present.txt")
    hidden = os.path.join(dark, "hidden")
    os.makedirs(hidden, exist_ok=True)
    _mk(hidden, "shadowed.txt")
    case("unreadable-subtree-incomplete", ["--claim", claim, "--root", dark], EXIT_ERROR,
         ["VERDICT INCOMPLETE", "unreadable_subtrees=1"], ["VERDICT ABSENT"],
         setup=lambda: os.chmod(hidden, 0o000), teardown=lambda: os.chmod(hidden, 0o755))
    case("same-tree-readable-absent", ["--claim", claim, "--root", dark], ABSENT,
         ["VERDICT ABSENT"], ["INCOMPLETE"])

    # 11b. a glob in the claim is a usage error, not a silent ABSENT
    case("glob-claim", ["--claim", "lanes/kaidoku/*/work/r7-local-measurements.tsv",
                        "--root", hitroot], EXIT_ERROR, [], ["VERDICT"])

    # 12c. ABSENT from a root that cannot be the claim's base carries the anchoring note
    case("unanchored-note", ["--claim", claim, "--root", clean], ABSENT,
         ["VERDICT ABSENT", "NOTE claim is unanchored"], ["WARNING"])

    # 13. --json shape carries the verdict and the exit code
    case("json-shape", ["--claim", claim, "--root", clean, "--json"], ABSENT,
         ['"verdict": "ABSENT"', '"exit_code": 0'])

    passed = 0
    for c in cases:
        if c["setup"]:
            c["setup"]()
        try:
            proc = subprocess.run([sys.executable, "-I", "-B", script] + c["argv"],
                                  cwd=c["cwd"], capture_output=True, text=True)
        finally:
            if c["teardown"]:
                c["teardown"]()
        out = proc.stdout + proc.stderr
        ok = proc.returncode == c["want_code"]
        ok = ok and all(s in out for s in c["want"])
        ok = ok and all(s not in out for s in c["reject"])
        passed += 1 if ok else 0
        status = "pass" if ok else "FAIL"
        print("%s %-32s exit=%d want=%d" % (status, c["name"], proc.returncode, c["want_code"]))
        if not ok:
            print("  stdout=%r\n  stderr=%r" % (proc.stdout[-400:], proc.stderr[-400:]))
    print("SELFTEST cases=%d pass=%d fail=%d" % (len(cases), passed, len(cases) - passed))
    shutil.rmtree(base, ignore_errors=True)
    return ABSENT if passed == len(cases) else PRESENT


def main(argv):
    ap = argparse.ArgumentParser(description="absence sweep for negative existence claims")
    ap.add_argument("--claim", help="relative path whose absence is claimed")
    ap.add_argument("--root", action="append", default=[], help="base root (repeatable)")
    ap.add_argument("--max-hits", type=int, default=100)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        return run(args.claim, args.root, args.max_hits, args.json)
    except UsageError as exc:
        sys.stderr.write("ERROR %s\n" % exc)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
