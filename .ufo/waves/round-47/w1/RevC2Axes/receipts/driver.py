"""RevC2Axes fixture driver — axes-class attacks on tools/round-47/record.py.

Every fixture is its own repo under $S, cloned --shared from the lane so the
frozen objects are the same bytes.  Mutations are committed with plumbing
(read-tree / hash-object / update-index / write-tree / commit-tree) so no
worktree checkout of the 500MB tree is ever needed.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time

S = "/fast/scratch/hyaku/kaidoku-r47/RevC2Axes"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)


def run(args, cwd=None, stdin=None):
    r = subprocess.run(args, cwd=cwd, input=stdin, capture_output=True, text=True)
    return r


def git(d, *args, stdin=None):
    return run(["git", "-C", d, *args], stdin=stdin)


def show(rev, path):
    r = run(["git", "-C", LANE, "show", f"{rev}:{path}"])
    if r.returncode != 0:
        raise SystemExit(f"cannot read {rev}:{path}: {r.stderr}")
    return r.stdout


class Fixture:
    def __init__(self, name):
        self.name = name
        self.d = tempfile.mkdtemp(dir=S, prefix="fx-" + name + "-")
        r = run(["git", "clone", "-q", "--shared", "--no-checkout", LANE, self.d])
        if r.returncode != 0:
            raise SystemExit("clone failed: " + r.stderr)
        top = git(self.d, "rev-parse", "--show-toplevel").stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(self.d), (top, self.d)
        self.rev = FREEZE
        self.idx = os.path.join(self.d, ".git", "r47-index")
        self.env = dict(ENV, GIT_INDEX_FILE=self.idx)

    def _g(self, *args, stdin=None):
        r = subprocess.run(["git", "-C", self.d, *args], input=stdin,
                           capture_output=True, text=True, env=self.env)
        if r.returncode != 0:
            raise SystemExit(f"git {' '.join(args)} failed: {r.stderr}")
        return r.stdout

    def commit(self, files, msg, remove=()):
        """files: {path: text}; remove: paths to drop.  Returns the new commit oid."""
        self._g("read-tree", self.rev)
        for path in remove:
            self._g("update-index", "--force-remove", path)
        for path, text in files.items():
            blob = self._g("hash-object", "-w", "--stdin", stdin=text).strip()
            self._g("update-index", "--add", "--cacheinfo", f"100644,{blob},{path}")
        tree = self._g("write-tree").strip()
        env = dict(self.env, GIT_AUTHOR_NAME="r47 fx", GIT_AUTHOR_EMAIL="fx@r47",
                   GIT_COMMITTER_NAME="r47 fx", GIT_COMMITTER_EMAIL="fx@r47")
        r = subprocess.run(["git", "-C", self.d, "commit-tree", tree, "-p", self.rev,
                            "-m", msg], capture_output=True, text=True, env=env)
        if r.returncode != 0:
            raise SystemExit("commit-tree failed: " + r.stderr)
        self.rev = r.stdout.strip()
        return self.rev

    def read(self, path):
        r = git(self.d, "show", f"{self.rev}:{path}")
        return r.stdout if r.returncode == 0 else None

    def counter(self, tag):
        out = os.path.join(self.d, f"r-{tag}.json")
        r = subprocess.run([sys.executable, "-I", "-B",
                            os.environ.get("R47_COUNTER", os.path.join(LANE, "tools/round-47/record.py")),
                            "--root", self.d, "--rev", self.rev,
                            "--json-out", out],
                           capture_output=True, text=True, env=ENV, cwd=self.d)
        rec = json.load(open(out)) if os.path.exists(out) else {}
        return r.returncode, rec, r.stdout, r.stderr

    def recipe_a(self):
        r = subprocess.run([sys.executable, os.path.join(S, "recipeA.py"), self.rev],
                           capture_output=True, text=True, cwd=self.d)
        try:
            return json.loads(r.stdout)
        except ValueError:
            return {"error": r.stdout + r.stderr}


AXIS_ROW = re.compile(r"(?m)^\|\s*(coverage|depth)\s*\|.*$")


def card_at(rev=FREEZE):
    return show(rev, "SCORECARD.md")


def axis_row(card, axis):
    m = re.search(r"(?m)^\|\s*" + axis + r"\s*\|.*$", card)
    return m


def set_axis_row(card, axis, new):
    m = axis_row(card, axis)
    assert m, axis
    return card[:m.start()] + new + card[m.end():]


def drop_axis_row(card, axis):
    m = axis_row(card, axis)
    assert m, axis
    return card[:m.start()] + card[m.end() + 1:]


def set_frac(card, axis, frac):
    """Rewrite the first N/M of an axis row (its 'headline') in place."""
    m = axis_row(card, axis)
    row = m.group(0)
    f = re.search(r"\b\d+/\d+\b", row)
    assert f, axis
    return card[:m.start()] + row[:f.start()] + frac + row[f.end():] + card[m.end():]


CORR_HEAD = "## Record corrections — round 47"


def corrections(*lines):
    return "\n\n" + CORR_HEAD + "\n\n" + "\n".join(lines) + "\n"


def green_card(rev_placeholder=FREEZE):
    """The frozen card with its two axes rows repaired in place and two genuine
    corrections appended — the minimum a landing needs.  Used as the baseline."""
    card = card_at()
    card = set_frac(card, "coverage", "138/138")
    card = set_frac(card, "depth", "23/23")
    card += corrections(
        "- corrects seats round-45: 2 waves, 76 seats total",
        "- corrects window 46: empty in %s..%s -- corpus/lessons/round-46.md"
        % (BASE, FREEZE),
    )
    return card


def brief(rec):
    return {
        "exit_classes": rec.get("atoms_by_class"),
        "mismatches": [(m["class"], m["key"]) for m in rec.get("mismatches", [])],
        "corrections": rec.get("corrections"),
        "corrections_bad": rec.get("corrections_bad"),
        "exempted": [(e["class"], e["key"]) for e in rec.get("exempted", [])],
        "failing": rec.get("failing"),
        "battery": rec.get("battery"),
    }


RESULTS = []


def record(name, fixture, tag, expect, extra=None):
    code, rec, out, err = fixture.counter(tag)
    entry = {"fixture": name, "tag": tag, "rev": fixture.rev,
             "dir": fixture.d, "exit": code, "expect_exit": expect,
             "ok": code == expect, "receipt": brief(rec),
             "stdout_sha256": __import__("hashlib").sha256(out.encode()).hexdigest(),
             "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if extra:
        entry["extra"] = extra
    RESULTS.append(entry)
    print(json.dumps(entry, sort_keys=True))
    return code, rec
