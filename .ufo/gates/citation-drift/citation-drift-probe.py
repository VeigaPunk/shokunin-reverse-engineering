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

FROZEN-RUN GUARD  expected.json pins the sha256 of the pointer table (the
`pointer_table` key). A table whose bytes differ from the pinned digest is
`pointer_table_tampered`; an absent table is `pointer_table_unreadable`; a
baseline that pins no digest is `pointer_table_unpinned`. All three are
preflight could-not-evaluate (exit 2) and run before any entry is graded, so a
tampered table can never produce silent findings. Any edit to the table must
re-pin the digest in the same commit.

REVISION PINNING (round 18, jj risk R2; round 19, R18-HEAD-ALIASES). An
omitted --rev no longer means the moving HEAD: it resolves to the tip of
--branch (default `main`, i.e. refs/heads/main). A literal `--rev HEAD` is
accepted only when HEAD equals the branch tip; otherwise the run is
could-not-evaluate with finding head_not_branch_tip (exit 2) — under jj
colocation HEAD can be an unbookmarked commit, and attesting its tree would
certify a revision that never landed. Every OTHER expression that resolves
through HEAD or mutable local state is refused before resolution with finding
rev_moving_state (exit 2): the `@` spelling and its suffixes (`@~N`, `@^`,
`@^{commit}`, `@{...}`), any HEAD-suffixed form (`HEAD~N`, `HEAD^`,
`HEAD@{...}`, `HEAD^{commit}`), reflog selectors on any ref (`main@{1}`,
`main@{upstream}`), and the pseudo-refs Git rewrites (ORIG_HEAD, FETCH_HEAD,
MERGE_HEAD, CHERRY_PICK_HEAD, REVERT_HEAD, REBASE_HEAD, BISECT_HEAD,
AUTO_MERGE). Full commit ids, branch refs (`main`, `refs/heads/main`), tags,
and their `~`/`^` ancestors still pass through and are resolved as before. The
report records rev_requested, rev_resolved, and branch.

VERDICT  exit 0 clean, 1 failed, 2 could-not-evaluate. Every finding carries a
stable id so the self-test can assert on it.

Usage:
  citation-drift-probe.py [--root DIR] [--rev REV] [--branch BRANCH]
                          [--table PATH] [--expected PATH]
                          [--snapshot-dir DIR]
  citation-drift-probe.py --selftest [--expected PATH]
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
                     "pointer_table_unreadable", "pointer_table_tampered",
                     "pointer_table_unpinned", "unpinned_legacy",
                     "root_unreadable", "revision_unresolvable", "internal_error",
                     "branch_missing", "head_not_branch_tip",
                     "rev_moving_state")
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

def git_commit(root, revspec):
    """Resolve revspec to a commit id, or None. Never raises."""
    proc = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", "--quiet", revspec],
        capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("ascii", "replace").strip() or None


def head_commit(root):
    """The commit HEAD currently points at, or None, read only to compare it
    with the branch tip. rev-list keeps the literal HEAD out of any rev-parse
    argv (head-rev-lint site kind rev-parse-HEAD)."""
    proc = subprocess.run(
        ["git", "-C", root, "rev-list", "--max-count=1", "HEAD"],  # head-rev-lint: compare-only
        capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("ascii", "replace").strip() or None


# Rev expressions that read mutable local repository state. Git rewrites these
# on checkout/fetch/merge, so one argv string can attest different trees on
# different runs; a pinned measurement must name a commit identity instead.
# The literal `HEAD` keeps its own tip comparison in resolve_rev; everything
# derived from it is refused before resolution (R18-HEAD-ALIASES), so no run
# can certify an unbookmarked or off-branch tree through an alias.
_PSEUDO_REFS = ("ORIG_HEAD", "FETCH_HEAD", "MERGE_HEAD", "CHERRY_PICK_HEAD",
                "REVERT_HEAD", "REBASE_HEAD", "BISECT_HEAD", "AUTO_MERGE")
_REV_SUFFIX = ("~", "^", "@", ":", "{")


def moving_rev_cause(rev):
    """Named cause when `rev` resolves through HEAD or mutable local state,
    else None. Purely lexical: the expression is never resolved, so an alias
    cannot pass merely because it happens to name the branch tip today."""
    if rev == "@":
        return "'@' is Git's shorthand for HEAD (a moving revision)"
    if rev.startswith("@") and rev[1:2] in _REV_SUFFIX:
        return "'%s' is HEAD-derived (the '@' spelling of HEAD)" % rev
    if rev.startswith("HEAD") and rev[4:5] in _REV_SUFFIX:
        return "'%s' is HEAD-derived; a pinned revision must not read HEAD" % rev
    for name in _PSEUDO_REFS:
        if rev == name:
            return "'%s' is a mutable pseudo-ref rewritten by Git" % name
        if rev.startswith(name) and rev[len(name):len(name) + 1] in _REV_SUFFIX:
            return "'%s' is derived from the mutable pseudo-ref %s" % (rev, name)
    if "@{" in rev:
        return "'%s' is a reflog selector (local, mutable history)" % rev
    return None


def resolve_rev(root, rev, branch, findings):
    """Pin the revision to evaluate (round 18, jj risk R2).

    Omitted --rev resolves to refs/heads/<branch>; a literal `--rev HEAD` is
    accepted only when HEAD equals that tip, else could-not-evaluate with
    head_not_branch_tip. Every other expression that resolves through HEAD or
    mutable local state — the `@` spelling, HEAD-suffixed forms, reflog
    selectors, and pseudo-refs such as ORIG_HEAD/FETCH_HEAD — is refused
    before resolution with rev_moving_state (round 19). Stable revs (full
    commit ids, refs/heads/<branch>, <branch>, tags) and their `~`/`^`
    ancestors pass through unchanged.
    Returns (rev_to_evaluate, blocking_findings_or_None).
    """
    findings.rev_requested = rev if rev is not None else "(default)"
    findings.branch = branch
    if rev is None:
        tip = git_commit(root, "refs/heads/%s^{commit}" % branch)
        if tip is None:
            findings.add("branch_missing", branch,
                         "refs/heads/%s does not resolve to a commit" % branch)
            return None, findings
        findings.rev_resolved = tip
        return tip, None
    if rev == "HEAD":
        tip = git_commit(root, "refs/heads/%s^{commit}" % branch)
        head = head_commit(root)
        if tip is None or head != tip:
            detail = ("HEAD %s != refs/heads/%s %s"
                      % (head or "(unresolvable)", branch, tip or "(missing)"))
            findings.add("head_not_branch_tip", branch, detail)
            return None, findings
        findings.rev_resolved = tip
        return tip, None
    cause = moving_rev_cause(rev)
    if cause is not None:
        findings.add("rev_moving_state", rev,
                     "%s; pass a full commit id, refs/heads/%s, or an ancestor"
                     % (cause, branch))
        return None, findings
    # explicit stable rev: evaluate exactly what was asked, as before; record
    # the normalized commit id when it resolves
    findings.rev_resolved = git_commit(root, "%s^{commit}" % rev) or rev
    return rev, None


def run_check(root, rev, table_path, expected_path, snapshot_dir, branch="main"):
    findings = Findings()
    findings.rev_requested = rev if rev is not None else "(default)"
    findings.rev_resolved = rev
    findings.branch = branch
    if not root_ok(root):
        findings.add("root_unreadable", root,
                     "not a readable Git work tree (git rev-parse --git-dir failed)")
        return findings
    rev, blocked = resolve_rev(root, rev, branch, findings)
    if blocked is not None:
        return blocked
    if not rev_ok(root, rev):
        findings.add("revision_unresolvable", rev,
                     "not a commit object (git rev-parse --verify %s^{commit} failed)" % rev)
        return findings
    try:
        expected = json.load(open(expected_path))
    except (OSError, ValueError) as exc:
        findings.add("pointer_table_unreadable", os.path.basename(expected_path), str(exc))
        return findings
    pin = expected.get("pointer_table")
    pin = pin.get("sha256") if isinstance(pin, dict) else None
    if pin is None:
        findings.add("pointer_table_unpinned", os.path.basename(expected_path),
                     "no pointer-table digest pinned in expected.json")
        return findings
    try:
        table_bytes = open(table_path, "rb").read()
    except OSError as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
    if sha256_bytes(table_bytes) != pin:
        findings.add("pointer_table_tampered", os.path.basename(table_path),
                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes), pin))
        return findings
    try:
        table = json.loads(table_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path), str(exc))
        return findings
    tree = Tree(root, rev, snapshot_dir, expected, findings)
    for entry in table.get("entries", []):
        check_entry(entry, tree, findings)
    for entry in table.get("quoted", []):
        entry = dict(entry, kind="quoted")
        check_entry(entry, tree, findings)
    return findings


def report(root, table_path, findings, strict=False):
    print("CITATION_DRIFT_ROOT: %s" % root)
    print("CITATION_DRIFT_REV_REQUESTED: %s"
          % getattr(findings, "rev_requested", "(default)"))
    print("CITATION_DRIFT_REV_RESOLVED: %s"
          % getattr(findings, "rev_resolved", "(unresolved)"))
    print("CITATION_DRIFT_BRANCH: %s" % getattr(findings, "branch", "main"))
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


def _fixture_commit(d, message):
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=e@x", "-c", "user.name=e",
                    "commit", "-qm", message], check=True)


def _fixture_tip(root):
    proc = subprocess.run(["git", "-C", root, "rev-parse", "refs/heads/main"],
                          capture_output=True, check=True)
    return proc.stdout.decode("ascii", "replace").strip()


def _fixture_extra_commit(root):
    """A second on-branch commit, so `main~1` and `*@{1}` name real objects."""
    open(os.path.join(root, "EXTRA.md"), "w").write("extra\n")
    _fixture_commit(root, "extra")


def _plant_pseudoref(root, name):
    """Give a pseudo-ref a resolvable object, so a red case observes the
    refusal rather than an unresolved name."""
    sha = _fixture_tip(root)
    line = ("%s\t\tbranch 'main' of fixture\n" % sha if name == "FETCH_HEAD"
            else "%s\n" % sha)
    open(os.path.join(root, ".git", name), "w").write(line)


def build_fixture(case):
    """Create an isolated git repo carrying one mutation; return its path."""
    d = tempfile.mkdtemp(prefix="citation-drift-selftest-")
    subprocess.run(["git", "init", "-q", "-b", "main", d], check=True)
    for name, text in FIXTURE_FILES.items():
        open(os.path.join(d, name), "w").write(text)
    if case == "clean" or case == "detached_head":
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
    _fixture_commit(d, case)
    if case == "detached_head":
        # jj-colocation shape: HEAD is an unbookmarked commit ahead of the
        # branch tip, so "clean" lives on main while HEAD carries a broken
        # tree (TARGET.md deleted).
        subprocess.run(["git", "-C", d, "checkout", "-q", "--detach", "HEAD"],
                       check=True)
        os.remove(os.path.join(d, "TARGET.md"))
        _fixture_commit(d, "off-branch")
    return d


# The self-test case table (case, expected exit code, expected finding id) is
# NOT defined here: it is committed in expected.json so the expected values are
# independent of the recomputation, per the protocol's Gate standard.
#
# Round-19 additions (R18-HEAD-ALIASES): `<HEX>` is replaced at run time with
# the fixture's refs/heads/main tip. Red cases plant a resolvable ORIG_HEAD /
# FETCH_HEAD / MERGE_HEAD, so the refusal — not an unresolved name — is what
# exit 2 reports; `_detached` cases put HEAD one commit off the branch tip.
ALIAS_CASES = [
    ("alias_accept_hex", "<HEX>", 0, "citations_clean"),
    ("alias_accept_refs_heads", "refs/heads/main", 0, "citations_clean"),
    ("alias_accept_refs_heads_peel", "refs/heads/main^{commit}", 0,
     "citations_clean"),
    ("alias_accept_branch", "main", 0, "citations_clean"),
    ("alias_accept_ancestor", "main~1", 0, "citations_clean"),
    ("alias_refuse_at", "@", 2, "rev_moving_state"),
    ("alias_refuse_at_ancestor", "@~1", 2, "rev_moving_state"),
    ("alias_refuse_head_tilde", "HEAD~0", 2, "rev_moving_state"),
    ("alias_refuse_head_caret", "HEAD^", 2, "rev_moving_state"),
    ("alias_refuse_head_peel", "HEAD^{commit}", 2, "rev_moving_state"),
    ("alias_refuse_head_reflog", "HEAD@{1}", 2, "rev_moving_state"),
    ("alias_refuse_orig_head", "ORIG_HEAD", 2, "rev_moving_state"),
    ("alias_refuse_orig_head_ancestor", "ORIG_HEAD~1", 2, "rev_moving_state"),
    ("alias_refuse_fetch_head", "FETCH_HEAD", 2, "rev_moving_state"),
    ("alias_refuse_merge_head", "MERGE_HEAD", 2, "rev_moving_state"),
    ("alias_refuse_branch_reflog", "main@{1}", 2, "rev_moving_state"),
    ("alias_refuse_at_detached", "@", 2, "rev_moving_state"),
    ("alias_refuse_head_tilde_detached", "HEAD~0", 2, "rev_moving_state"),
]


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
        # round-18 additions (jj risk R2): fixtures with a detached off-branch
        # HEAD made by plain git. Green: an omitted --rev resolves the branch
        # tip, not HEAD. Red: a literal --rev HEAD is refused when HEAD is not
        # the tip (exit 2, head_not_branch_tip).
        cases.append(("detached_head_default", 0, "citations_clean"))
        cases.append(("detached_head_rev_head", 2, "head_not_branch_tip"))
        # round-19 additions (R18-HEAD-ALIASES): stable forms stay green;
        # every HEAD/working-copy expression is refused before resolution.
        cases.extend((case, exit_code, finding)
                     for case, _rev, exit_code, finding in ALIAS_CASES)
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
                    if case.startswith("alias_"):
                        fixture_case = ("detached_head"
                                        if case.endswith("_detached") else "clean")
                    else:
                        fixture_case = ("detached_head"
                                        if case.startswith("detached_head") else case)
                    root = build_fixture(fixture_case)
                    if case.startswith("alias_"):
                        _fixture_extra_commit(root)
                        for name in ("ORIG_HEAD", "FETCH_HEAD", "MERGE_HEAD"):
                            _plant_pseudoref(root, name)
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
                table_bytes = open(table, "rb").read()
                expected = {"snapshots": digests,
                            "pointer_table": {"sha256": sha256_bytes(table_bytes)}}
                exp_file = os.path.join(case_dir, "expected.json")
                json.dump(expected, open(exp_file, "w"))
                if case == "table_tampered":
                    # the silent-clean shape: a valid table with no entries
                    # grades findings=0 at rc 0 without the frozen-run guard
                    open(table, "w").write(json.dumps({"entries": []}))
                elif case == "table_absent":
                    os.remove(table)

                if case.startswith("detached_head") or case.startswith("alias_"):
                    # CLI-level path: drive the real argv surface (argparse ->
                    # resolve_rev -> run_check), not run_check directly.
                    argv = [sys.executable, os.path.abspath(__file__),
                            "--root", root, "--table", table,
                            "--expected", exp_file, "--strict"]
                    if case == "detached_head_rev_head":
                        # head-rev-lint: compare-only
                        argv += ["--rev", "HEAD"]
                    elif case.startswith("alias_"):
                        rev = next(r for c, r, _, _ in ALIAS_CASES if c == case)
                        argv += ["--rev", _fixture_tip(root) if rev == "<HEX>"
                                 else rev]
                    proc = subprocess.run(argv, capture_output=True, text=True)
                    got_exit = proc.returncode
                    got_ids = {ln.split(":", 1)[1].strip().split(" ", 1)[0]
                               for ln in proc.stdout.splitlines()
                               if ln.startswith("CITATION_DRIFT:")}
                else:
                    if case == "rev_unresolvable":
                        rev = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
                    else:
                        rev = "HEAD"
                    findings = run_check(
                        root, rev, table, exp_file,
                        None if case == "no_snapshot_dir" else snapshot_dir)
                    got_exit = findings.verdict(strict=True)
                    got_ids = findings.ids()
                if want_finding == "citations_clean" and not got_ids:
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
    ap.add_argument("--rev", default=None,
                    help="commit to evaluate; omitted resolves the tip of "
                         "--branch; literal HEAD is accepted only when HEAD "
                         "equals the branch tip; HEAD aliases, reflog "
                         "selectors, and pseudo-refs are refused as moving "
                         "revisions (exit 2)")
    ap.add_argument("--branch", default="main",
                    help="branch whose tip pins an omitted --rev")
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
                             args.snapshot_dir, branch=args.branch)
    except Exception as exc:
        findings = Findings()
        findings.add("internal_error", "gate", "%s: %s" % (type(exc).__name__, exc))
    return report(args.root, args.table, findings,
                  strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
