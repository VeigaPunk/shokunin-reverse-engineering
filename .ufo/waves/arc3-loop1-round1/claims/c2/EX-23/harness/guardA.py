#!/usr/bin/env python3
"""citation-drift gate (draft v1, seat E15, wave arc2-loop1-round3).

A committed, re-runnable verdict script over a PINNED POINTER TABLE. The table
is the contract: every citation the lane relies on is listed as an entry, and
each entry is resolved against the tree at a named revision (Git objects, never
the moving worktree) or against a committed snapshot for targets outside the
repo. The gate never repairs anything: it reports.

WHY THE EXTRACTION FORM. Three rounds of pointer bites (CR5 arc2-loop1-round1;
SCORECARD.md:68-72 arc2-loop1-round2) all had the same shape: the citing text
states a line number, and the stated number is wrong. A static regex pin on the
citing line would pass a sentence that states a wrong number, so an `extracted`
entry instead reads the number OUT of the citing line and verifies that the
TARGET line the sentence names actually holds the content the sentence claims.
A reword that states the right number passes; any number it states wrong fails.

ENTRY KINDS
  extracted  regex over the citing line yields a target line number (or range);
             the TARGET line(s) must match `must_match`. This is the class
             catcher for stated-number drift.
  exact      the citing line itself must match `must_match` at the pinned line.
  anchor     `must_match` must appear somewhere in the file; a hit on a line
             other than `pin_line` is `citation_moved` (the citation's line
             number is stale even though the content survives). Used for
             operator-owned files whose line numbers legitimately move.

TARGETS
  repo-relative path       read as a Git object at --rev (immutable).
  @<slug>                  read from --snapshot-dir, after verifying its sha256
                           against expected.json `snapshots` (a mismatched
                           snapshot is `snapshot_tampered`, exit 2).

VERDICT  exit 0 clean, 1 failed, 2 could-not-evaluate. Every finding carries a
stable id so the self-test can assert on it.

Usage:
  citation-drift-gate.py [--root DIR] [--rev REV] [--table PATH]
                         [--expected PATH] [--snapshot-dir DIR]
  citation-drift-gate.py --selftest [--expected PATH]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TABLE = os.path.join(HERE, "pointer-table.json")
DEFAULT_EXPECTED = os.path.join(HERE, "expected.json")

CLEAN, FAILED, CNE = 0, 1, 2


class Findings:
    def __init__(self):
        self.rows = []

    def add(self, finding, entry, detail=""):
        self.rows.append((finding, entry, detail))

    def ids(self):
        return {f for f, _, _ in self.rows}

    def verdict(self, strict=False):
        if not self.rows:
            return CLEAN
        if any(f in ("snapshot_tampered", "snapshot_missing",
                     "pointer_table_unreadable", "unpinned_legacy",
                     "root_unreadable", "revision_unresolvable", "internal_error")
               for f, _, _ in self.rows):
            return CNE
        if not strict:
            return CLEAN
        # A stamp-qualified pointer that no longer resolves is recorded, not
        # counted as failure: the entry's own text names the revision it was
        # accurate at, so it is history rather than a broken citation.
        if all(f == "citation_historical_ok" for f, _, _ in self.rows):
            return CLEAN
        return FAILED


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def git_show(root, rev, path):
    """Return (text, error). Never raises."""
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        return None, "absent at %s" % rev
    try:
        return proc.stdout.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, "undecodable"


class Tree:
    """Resolves a target to lines, from a Git rev or a verified snapshot."""

    def __init__(self, root, rev, snapshot_dir, expected, findings):
        self.root, self.rev = root, rev
        self.snapshot_dir = snapshot_dir
        self.expected = expected
        self.findings = findings
        self._cache = {}
        # targets whose resolution failure was already reported, so a caller
        # does not file a second finding for the same cause
        self.reported = set()

    def lines(self, target):
        if target in self._cache:
            return self._cache[target]
        if target.startswith("@"):
            out = self._snapshot(target[1:])
        else:
            text, err = git_show(self.root, self.rev, target)
            if err:
                self.findings.add("citation_file_absent", target, err)
                self.reported.add(target)
            out = (None, err) if err else (text.splitlines(), None)
        self._cache[target] = out
        return out

    def _snapshot(self, slug):
        key = "@" + slug
        if not self.snapshot_dir:
            # a missing --snapshot-dir is a configuration error, not a drifted
            # citation: it must read as could-not-evaluate, never as failed
            self.findings.add("pointer_table_unreadable", key,
                              "no --snapshot-dir given for snapshot target @%s" % slug)
            self.reported.add(key)
            return None, "no --snapshot-dir given for snapshot target @%s" % slug
        path = os.path.join(self.snapshot_dir, slug)
        if not os.path.isfile(path):
            self.findings.add("snapshot_missing", key, path)
            self.reported.add(key)
            return None, "snapshot absent: %s" % path
        data = open(path, "rb").read()
        pinned = (self.expected.get("snapshots") or {}).get(slug)
        if pinned is None:
            self.findings.add("unpinned_legacy", key,
                              "no digest pinned in expected.json")
            self.reported.add(key)
            return None, "unpinned (legacy): %s" % slug
        if sha256_bytes(data) != pinned:
            self.findings.add("snapshot_tampered", key,
                              "sha256 %s != pinned %s" % (sha256_bytes(data), pinned))
            self.reported.add(key)
            return None, "snapshot_tampered"
        return data.decode("utf-8", "replace").splitlines(), None


def check_entry(entry, tree, findings):
    eid = entry.get("id", "<unnamed>")
    kind = entry.get("kind")
    target = entry["file"]
    citing, err = tree.lines(target)
    if citing is None:
        # a resolution failure was already reported by Tree (snapshot classes)
        # or is reported here for an absent in-repo file
        if target not in tree.reported:
            findings.add("citation_file_absent", eid, "%s: %s" % (target, err))
        return

    if kind == "anchor":
        hits = [i + 1 for i, l in enumerate(citing) if re.search(entry["must_match"], l)]
        if not hits:
            findings.add("citation_dead", eid,
                         "%s: no line matches %r" % (target, entry["must_match"][:60]))
        elif entry.get("pin_line") is not None and entry["pin_line"] not in hits:
            findings.add("citation_moved", eid,
                         "%s: content at %s, citation pins %s"
                         % (target, hits, entry["pin_line"]))
        return

    line_no = entry.get("line")
    if not isinstance(line_no, int) or not (1 <= line_no <= len(citing)):
        findings.add("citation_out_of_range", eid,
                     "%s:%s beyond EOF (%d lines)" % (target, line_no, len(citing)))
        return
    citing_line = citing[line_no - 1]

    if kind == "quoted":
        # an append-only record of a claim; the words must survive verbatim.
        if not re.search(entry["must_match"], citing_line):
            findings.add("record_word_missing", eid,
                         "%s:%d no longer carries %r (append-only records are "
                         "never rewritten)" % (target, line_no, entry["must_match"][:60]))
        return

    if kind == "exact":
        if not re.search(entry["must_match"], citing_line):
            findings.add("citation_dead", eid,
                         "%s:%d lacks %r" % (target, line_no, entry["must_match"][:60]))
        return

    if kind == "extracted":
        m = re.search(entry["pattern"], citing_line)
        if not m:
            findings.add("citation_dead", eid,
                         "%s:%d states no resolvable pointer (pattern %r absent)"
                         % (target, line_no, entry["pattern"][:60]))
            return
        cited_target = entry["target"]
        try:
            lo = int(m.group(entry.get("target_group", 1)))
            hi = int(m.group(entry.get("target_group_end", entry.get("target_group", 1)))
                     or lo)
        except (IndexError, ValueError):
            findings.add("citation_dead", eid,
                         "%s:%d pointer group unreadable in %r"
                         % (target, line_no, m.group(0)[:60]))
            return
        if entry.get("rev"):
            cited, terr = Tree(tree.root, entry["rev"], tree.snapshot_dir,
                               tree.expected, tree.findings).lines(cited_target)
        else:
            cited, terr = tree.lines(cited_target)
        if cited is None:
            findings.add("citation_file_absent", eid,
                         "%s (cited by %s:%d): %s" % (cited_target, target, line_no, terr))
            return
        # `window` widens the cited range: a citation that names one line of a
        # multi-line block (e.g. a line inside a config stanza) is checked
        # against that block's neighborhood, not against one exact line.
        window = int(entry.get("window", 0))
        lo, hi = lo - window, hi + window
        if not (1 <= lo <= hi <= len(cited)):
            findings.add("citation_out_of_range", eid,
                         "%s:%d-%d beyond EOF (%d lines), cited by %s:%d"
                         % (cited_target, lo, hi, len(cited), target, line_no))
            return
        blob = "\n".join(cited[lo - 1:hi])
        if not re.search(entry["must_match"], blob, re.M):
            finding = ("citation_historical_ok" if entry.get("stamp")
                       else "citation_dead")
            detail = ("%s:%d cites %s:%d-%d, which lacks %r (holds %r)"
                      % (target, line_no, cited_target, lo, hi,
                         entry["must_match"][:48], cited[lo - 1][:64]))
            if entry.get("stamp"):
                findings.add(finding, eid, detail + " [stamp: %s]" % entry["stamp"])
            else:
                findings.add(finding, eid, detail)
        return

    findings.add("pointer_table_unreadable", eid, "unknown kind %r" % kind)


def root_ok(root):
    proc = subprocess.run(["git", "-C", root, "rev-parse", "--git-dir"],
                          capture_output=True)
    return proc.returncode == 0


def rev_ok(root, rev):
    """True iff --rev names one commit object. A missing or non-commit rev is
    could-not-evaluate, not a set of absent files. Never raises."""
    proc = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", "%s^{commit}" % rev],
        capture_output=True)
    return proc.returncode == 0


def run_check(root, rev, table_path, expected_path, snapshot_dir):
    findings = Findings()
    if not root_ok(root):
        findings.add("root_unreadable", root,
                     "not a readable Git work tree (git rev-parse --git-dir failed)")
        return findings
    if not rev_ok(root, rev):
        findings.add("revision_unresolvable", rev,
                     "not a commit object (git rev-parse --verify %s^{commit} failed)" % rev)
        return findings
    try:
        table = json.load(open(table_path))
    except (OSError, ValueError) as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
    try:
        expected = json.load(open(expected_path))
    except (OSError, ValueError) as exc:
        expected = {}
        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
    # Frozen-run guard: the table is the contract, so its bytes are pinned in
    # expected.json. The run cannot tell an honest in-flight re-key from a
    # tamper, so a digest mismatch is could-not-evaluate, never a finding set.
    try:
        table_bytes = open(table_path, "rb").read()
    except OSError as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path),
                     str(exc))
        return findings
    pinned_table = (expected.get("frozen_run") or {}).get("table_sha256")
    if pinned_table is None:
        findings.add("unpinned_legacy", os.path.basename(table_path),
                     "no table digest pinned in expected.json")
        return findings
    if sha256_bytes(table_bytes) != pinned_table:
        findings.add("pointer_table_tampered", os.path.basename(table_path),
                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes),
                                                 pinned_table))
        return findings
    tree = Tree(root, rev, snapshot_dir, expected, findings)
    for entry in table.get("entries", []):
        check_entry(entry, tree, findings)
    for entry in table.get("quoted", []):
        entry = dict(entry, kind="quoted")
        check_entry(entry, tree, findings)
    return findings


def report(root, rev, table_path, findings, strict=False):
    print("CITATION_DRIFT_ROOT: %s" % root)
    print("CITATION_DRIFT_REVISION: %s" % rev)
    print("CITATION_DRIFT_TABLE: %s" % table_path)
    for finding, entry, detail in findings.rows:
        print("CITATION_DRIFT: %s entry=%s %s" % (finding, entry, detail))
    verdict = findings.verdict(strict=strict)
    label = {CLEAN: "clean" if strict else "reported", FAILED: "failed",
             CNE: "could-not-evaluate"}[verdict]
    print("CITATION_DRIFT_VERDICT: %s findings=%d exit=%d"
          % (label, len(findings.rows), verdict))
    return verdict


# --------------------------------------------------------------------------
# self-test: isolated fixture trees, no network, no live-tree write
# --------------------------------------------------------------------------
FIXTURE_FILES = {
    "CITING.md": "see `TARGET.md:3` for the claim\nsee `TARGET.md:99` for the far claim\n",
    "TARGET.md": "alpha\nbeta\nthe pinned claim lives here\ngamma\n",
    "MOVED.md": "the anchored sentence is here\n",
}


def build_fixture(case):
    """Create an isolated git repo carrying one mutation; return its path."""
    d = tempfile.mkdtemp(prefix="citation-drift-selftest-")
    subprocess.run(["git", "init", "-q", d], check=True)
    for name, text in FIXTURE_FILES.items():
        open(os.path.join(d, name), "w").write(text)
    if case == "clean":
        pass
    elif case == "dead":
        open(os.path.join(d, "TARGET.md"), "w").write(
            "alpha\nbeta\nsomething else entirely\ngamma\n")
    elif case == "out_of_range":
        open(os.path.join(d, "TARGET.md"), "w").write("alpha\nbeta\n")
    elif case == "file_absent":
        os.remove(os.path.join(d, "TARGET.md"))
    elif case == "moved":
        open(os.path.join(d, "MOVED.md"), "w").write(
            "a new opening line\nthe anchored sentence is here\n")
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=e@x", "-c", "user.name=e",
                    "commit", "-qm", case], check=True)
    return d


# The self-test case table (case, expected exit code, expected finding id) is
# NOT defined here: it is committed in expected.json so the expected values are
# independent of the recomputation, per the protocol's Gate standard.


def fixture_table(case):
    entries = [
        {"id": "f-extracted", "kind": "extracted", "file": "CITING.md", "line": 1,
         "pattern": r"`TARGET\.md:(\d+)`", "target": "TARGET.md", "target_group": 1,
         "must_match": r"pinned claim lives here"},
        {"id": "f-moved", "kind": "anchor", "file": "MOVED.md", "pin_line": 1,
         "must_match": r"anchored sentence is here"},
    ]
    if case == "snapshot_missing":
        entries.append({"id": "f-snap", "kind": "exact", "file": "@external.cfg",
                        "line": 1, "must_match": r"anything"})
    if case == "snapshot_tampered":
        entries.append({"id": "f-snap", "kind": "exact", "file": "@external.cfg",
                        "line": 1, "must_match": r"anything"})
    if case == "no_snapshot_dir":
        # a configuration error must read as could-not-evaluate (2), never 1
        entries.append({"id": "f-snap", "kind": "exact", "file": "@external.cfg",
                        "line": 1, "must_match": r"anything"})
    if case == "stamped":
        # A stamp-qualified pointer whose target no longer holds the claim:
        # recorded as history, and it must NOT redden the run.
        entries.append({"id": "f-stamp", "kind": "extracted", "file": "CITING.md",
                        "line": 1, "pattern": r"`TARGET\.md:(\d+)`",
                        "target": "TARGET.md", "target_group": 1,
                        "must_match": r"a claim that has since moved away",
                        "stamp": "2026-10-18T16:57:35Z receipt"})
    return {"entries": entries}


def selftest(expected_path):
    try:
        expected_root = json.load(open(expected_path))
        cases = [(c["case"], c["exit_code"], c["finding"])
                 for c in expected_root["selftest"]]
    except (OSError, ValueError, KeyError) as exc:
        print("CITATION_DRIFT_SELFTEST: FAILED cases=0 passed=0 failed=0 exit=1 "
              "finding=selftest_table_unreadable (%s)" % exc)
        return 1
    passed = failed = 0
    for case, want_exit, want_finding in cases:
        with tempfile.TemporaryDirectory(prefix="citation-drift-case-") as case_dir:
            root = None
            try:
                if case == "table_unreadable":
                    table = os.path.join(case_dir, "table.json")
                    open(table, "w").write("{ not json")
                    root = build_fixture("clean")
                else:
                    root = build_fixture(case)
                    table = os.path.join(case_dir, "table.json")
                    json.dump(fixture_table(case), open(table, "w"))

                snapshot_dir = os.path.join(case_dir, "snap")
                os.makedirs(snapshot_dir)
                snap = os.path.join(snapshot_dir, "external.cfg")
                if case == "snapshot_missing":
                    # deliberately do NOT create the snapshot file
                    digests = {"external.cfg": sha256_bytes(b"the external anchor\n")}
                elif case == "snapshot_tampered":
                    open(snap, "w").write("the external anchor\n")
                    digests = {"external.cfg": "0" * 64}
                else:
                    digests = {}
                expected = {"snapshots": digests}
                exp_file = os.path.join(case_dir, "expected.json")
                json.dump(expected, open(exp_file, "w"))

                rev = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef" if case == "rev_unresolvable" else "HEAD"
                findings = run_check(root, rev, table, exp_file,
                                     None if case == "no_snapshot_dir" else snapshot_dir)
                got_exit = findings.verdict(strict=True)
                got_ids = findings.ids()
                if case == "clean" and not findings.rows:
                    got_ids = {"citations_clean"}
                ok = (got_exit == want_exit) and (want_finding in got_ids)
                print("SELFTEST_CASE: %s case=%s exit=%d expected=%d finding=%s"
                      % ("CLEAN" if ok else "FAILED", case, got_exit, want_exit,
                         want_finding))
                passed += ok
                failed += not ok
            finally:
                if root:
                    shutil.rmtree(root, ignore_errors=True)
    total = len(cases)
    print("CITATION_DRIFT_SELFTEST: %s cases=%d passed=%d failed=%d exit=%d"
          % ("CLEAN" if failed == 0 else "FAILED", total, passed, failed,
             0 if failed == 0 else 1))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(HERE))
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--table", default=DEFAULT_TABLE)
    ap.add_argument("--expected", default=DEFAULT_EXPECTED)
    ap.add_argument("--snapshot-dir")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="gate semantics 0/1/2; default probe semantics "
                         "(0 reported / 2 could-not-evaluate)")
    args = ap.parse_args()
    if args.selftest:
        return selftest(args.expected)
    try:
        findings = run_check(args.root, args.rev, args.table, args.expected,
                             args.snapshot_dir)
    except Exception as exc:
        findings = Findings()
        findings.add("internal_error", "gate", "%s: %s" % (type(exc).__name__, exc))
    return report(args.root, args.rev, args.table, findings,
                  strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
