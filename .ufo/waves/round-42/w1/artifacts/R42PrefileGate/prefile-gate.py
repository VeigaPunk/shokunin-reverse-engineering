#!/usr/bin/env python3
"""kaidoku pre-file gate for round N (stdlib only, read-only).

Exit 0 only if all four conditions hold:

  (a) every .ufo/waves/round-N/<wave>.ready has a <wave>.ready.dispatched marker
      AND a results file (<wave>-results.json or rN-<wave>-results.json beside the
      dispatch json).  -> no wave is still running.
  (b) `git status --porcelain` lists nothing under .ufo/waves/round-N/,
      corpus/evidence/round-N/, plans/ or tools/round-N/ (untracked or modified).
  (c) no stray *.err file in the lane root.
  (d) every w*/<Name>.md path cited in corpus/lessons/round-N.md exists in the
      committed tree (HEAD), not merely on disk (round-41 closure D2).

Advisory checks (reported, exit-neutral): ignored residue under the same scopes,
committed .err under the round's evidence/wave dirs, nested w*/.../*.md citations,
bare R<N>*.md wave-report names, uncommitted edits to the lesson.

Usage:
  prefile-gate.py --root LANE --round N [--json]
  prefile-gate.py --selftest [--work DIR]

The gate never writes: no temp files, no git mutation.  Selftest fixtures are
created under TMPDIR (or --work) and removed afterwards.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FAIL = "FAIL"
WARN = "WARN"
PASS = "PASS"

CONDITIONS = (
    ("a", "waves settled"),
    ("b", "tree clean under round scopes"),
    ("c", "no stray .err in lane root"),
    ("d", "lesson wave-report pointers resolve in HEAD"),
)

WAVE_MD_RE = re.compile(r"(?<![\w./-])w(\d+)/([A-Za-z0-9_][A-Za-z0-9_./-]*?\.md)(?![\w./-])")


def _git(root, *args):
    """Run git against *root* with an explicit -C.  Returns (rc, stdout, stderr)."""
    p = subprocess.run(
        ["git", "-C", root, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (
        p.returncode,
        p.stdout.decode("utf-8", "surrogateescape"),
        p.stderr.decode("utf-8", "surrogateescape"),
    )


def _norm_root(root):
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        raise SystemExit("prefile-gate: --root is not a directory: %s" % root)
    rc, out, err = _git(root, "rev-parse", "--show-toplevel")
    if rc != 0:
        raise SystemExit("prefile-gate: not a git work tree: %s\n%s" % (root, err.strip()))
    top = out.strip()
    if os.path.realpath(top) != os.path.realpath(root):
        raise SystemExit(
            "prefile-gate: --root %s is inside work tree %s; pass the toplevel" % (root, top)
        )
    return top


def _x(p):
    return os.path.join(*p.split("/")) if "/" in p else p


def _in_head(root, relpath):
    """True if relpath is a blob (or tree) in HEAD."""
    rc, _out, _err = _git(root, "cat-file", "-e", "HEAD:" + relpath)
    return rc == 0


def _read_head(root, relpath):
    rc, out, err = _git(root, "show", "HEAD:" + relpath)
    if rc != 0:
        return None, err
    return out, None


def _json_at(path):
    try:
        with open(path, "rb") as fh:
            return json.load(fh)
    except (ValueError, OSError):
        return None


def _status_z(root, extra):
    """Parse `git status --porcelain=v1 -z -uall` into [(xy, path, src_or_None)]."""
    args = ["status", "--porcelain=v1", "-z", "-uall"]
    args.extend(extra)
    rc, out, err = _git(root, *args)
    if rc != 0:
        raise SystemExit("prefile-gate: git status failed: %s" % err.strip())
    toks = out.split("\0")
    entries = []
    i = 0
    while i < len(toks):
        tok = toks[i]
        i += 1
        if not tok:
            continue
        xy, path = tok[:2], tok[3:]
        src = None
        if ("R" in xy or "C" in xy) and i < len(toks):
            src = toks[i]
            i += 1
        entries.append((xy, path, src))
    return entries


def _under(path, scope):
    return path == scope or path.startswith(scope)


class Gate:
    def __init__(self, root, round_no):
        self.root = root
        self.n = round_no
        self.findings = {key: [] for key, _ in CONDITIONS}
        self.notes = {key: [] for key, _ in CONDITIONS}

    def fail(self, cond, msg, detail=None):
        self.findings[cond].append((FAIL, msg, detail))

    def warn(self, cond, msg, detail=None):
        self.findings[cond].append((WARN, msg, detail))

    def ok(self, cond, msg, detail=None):
        self.findings[cond].append((PASS, msg, detail))

    def note(self, cond, msg):
        self.notes[cond].append(msg)

    def _ledger_advisory(self, wave, relpath, ledger, dispatch):
        """Advisory: a settled wave whose ledger is short of its dispatch count."""
        cond = "a"
        if not isinstance(ledger, dict):
            self.warn(cond, "wave %s results file is not a JSON object: %s" % (wave, relpath))
            return
        rn = ledger.get("round")
        if isinstance(rn, int) and rn != self.n:
            self.warn(
                cond,
                "wave %s results ledger says round=%d (gate round=%d)" % (wave, rn, self.n),
            )
        entries = ledger.get("results")
        n_entries = len(entries) if isinstance(entries, (list, dict)) else None
        if isinstance(ledger.get("seats"), int) and n_entries is not None:
            if n_entries != ledger["seats"]:
                self.warn(
                    cond,
                    "wave %s results ledger has %d entries but declares seats=%d"
                    % (wave, n_entries, ledger["seats"]),
                )
        declared = None
        if isinstance(dispatch, dict) and isinstance(dispatch.get("counts"), dict):
            counts = dispatch["counts"]
            declared = counts.get("total", counts.get("spawn"))
        if n_entries is not None and isinstance(declared, int) and declared > n_entries:
            self.warn(
                cond,
                "wave %s results ledger has %d entries vs dispatch total %d (partial)"
                % (wave, n_entries, declared),
            )

    # ---- (a) waves settled -------------------------------------------------
    def check_waves(self):
        cond = "a"
        wdir = ".ufo/waves/round-%d" % self.n
        adir = _x(wdir)
        if not os.path.isdir(os.path.join(self.root, adir)):
            self.fail(cond, "no wave directory %s/" % wdir)
            return
        waves = sorted(
            os.path.basename(p)[: -len(".ready")]
            for p in glob.glob(os.path.join(self.root, adir, "*.ready"))
            if os.path.isfile(p)
        )
        if not waves:
            self.fail(cond, "no %s/*.ready wave marker: round has no dispatched wave" % wdir)
            return
        settled = 0
        for wave in waves:
            ready = os.path.join(adir, wave + ".ready")
            dispatched = os.path.join(adir, wave + ".ready.dispatched")
            if not os.path.isfile(os.path.join(self.root, dispatched)):
                self.fail(
                    cond,
                    "wave %s is still running: %s/ has no %s.ready.dispatched"
                    % (wave, wdir, wave),
                )
            dispatch_json = "%s/%s-dispatch.json" % (wdir, wave)
            base = wdir
            if _in_head(self.root, dispatch_json) or os.path.isfile(
                os.path.join(self.root, _x(dispatch_json))
            ):
                base = os.path.dirname(dispatch_json)
            cands = ["%s/%s-results.json" % (base, wave), "%s/r%d-%s-results.json" % (base, self.n, wave)]
            found = [
                c
                for c in cands
                if os.path.isfile(os.path.join(self.root, _x(c)))
                or _in_head(self.root, c)
            ]
            if not found:
                self.fail(
                    cond,
                    "wave %s has no results file (looked for %s)"
                    % (wave, " and ".join(os.path.basename(c) for c in cands)),
                )
            else:
                settled += 1
                hit = _x(found[0])
                p = os.path.join(self.root, hit)
                size = os.path.getsize(p) if os.path.isfile(p) else None
                self.note(
                    cond,
                    "wave %s settled: %s%s"
                    % (wave, found[0], "" if size is None else " (%d bytes)" % size),
                )
                if os.path.isfile(p):
                    ledger = _json_at(p)
                    if ledger is None:
                        self.warn(
                            cond,
                            "wave %s results file does not parse as JSON: %s" % (wave, found[0]),
                        )
                    else:
                        self._ledger_advisory(wave, found[0], ledger, _json_at(
                            os.path.join(self.root, _x(dispatch_json))
                        ))
            if not os.path.isfile(os.path.join(self.root, ready)):
                self.note(cond, "list-only marker %s.ready" % wave)
        orphans = sorted(
            os.path.basename(p) for p in glob.glob(os.path.join(self.root, adir, "*.ready.dispatched"))
        )
        known = {w + ".ready.dispatched" for w in waves}
        for name in orphans:
            if name not in known:
                self.warn(cond, "orphan dispatch marker %s/%s without a .ready" % (wdir, name))
        if settled == len(waves):
            self.ok(cond, "%d/%d waves settled (%s)" % (settled, len(waves), ", ".join(waves)))

    # ---- (b) tree clean under scopes --------------------------------------
    def check_status(self):
        cond = "b"
        scopes = [
            ".ufo/waves/round-%d/" % self.n,
            "corpus/evidence/round-%d/" % self.n,
            "plans/",
            "tools/round-%d/" % self.n,
        ]
        entries = _status_z(self.root, ["--", *scopes])
        dirty = []
        for xy, path, src in entries:
            hits = [p for p in (path, src) if p and any(_under(p, s) for s in scopes)]
            if hits:
                dirty.append((xy, path, src))
        if dirty:
            for xy, path, src in dirty:
                shown = "%s %s" % (xy, path)
                if src:
                    shown += " <- " + src
                self.fail(cond, "uncommitted under round scope: " + shown)
        else:
            self.ok(cond, "git status clean under %s" % ", ".join(s[:-1] for s in scopes))

        ign = _status_z(self.root, ["--ignored=matching", "--", *scopes])
        ignored = [e for e in ign if e[0] == "!!" and any(_under(e[1], s) for s in scopes)]
        if ignored:
            sample = ", ".join(p for _xy, p, _src in ignored[:5])
            self.warn(
                cond,
                "%d ignored path(s) under round scope (build/scratch residue): %s%s"
                % (len(ignored), sample, " ..." if len(ignored) > 5 else ""),
            )

    # ---- (c) stray .err in lane root --------------------------------------
    def check_stray_err(self):
        cond = "c"
        stray = sorted(
            os.path.basename(p) for p in glob.glob(os.path.join(self.root, "*.err")) if os.path.isfile(p)
        )
        if stray:
            for name in stray:
                self.fail(cond, "stray stderr file in lane root: %s" % name)
        else:
            self.ok(cond, "no *.err in lane root")

        rc, out, _err = _git(
            self.root,
            "ls-files",
            "-z",
            "--",
            ".ufo/waves/round-%d/*.err" % self.n,
            "corpus/evidence/round-%d/*.err" % self.n,
        )
        tracked = [p for p in out.split("\0") if p]
        rc2, out2, _err2 = _git(
            self.root,
            "ls-files",
            "-z",
            "--others",
            "--",
            ".ufo/waves/round-%d/*.err" % self.n,
            "corpus/evidence/round-%d/*.err" % self.n,
        )
        untracked = [p for p in out2.split("\0") if p]
        if tracked or untracked:
            self.warn(
                cond,
                "%d tracked + %d untracked .err under round evidence/wave dirs (outside the "
                "lane-root rule; e.g. %s)"
                % (
                    len(tracked),
                    len(untracked),
                    (tracked + untracked)[0],
                ),
            )

    # ---- (d) lesson pointers resolve in HEAD ------------------------------
    def check_pointers(self):
        cond = "d"
        lesson = "corpus/lessons/round-%d.md" % self.n
        text, err = _read_head(self.root, lesson)
        if text is None:
            on_disk = os.path.isfile(os.path.join(self.root, _x(lesson)))
            self.fail(
                cond,
                "%s is not in the committed tree (HEAD)%s"
                % (lesson, "; it exists on disk only" if on_disk else ""),
            )
            return
        rc, dirty, _e = _git(self.root, "status", "--porcelain", "--", lesson)
        if rc == 0 and dirty.strip():
            self.warn(cond, "%s has uncommitted edits; gate read the HEAD bytes" % lesson)

        seen = set()
        nested = set()
        binding_missing = 0
        for m in WAVE_MD_RE.finditer(text):
            wave, name = m.group(1), m.group(2)
            rel = ".ufo/waves/round-%d/w%s/%s" % (self.n, wave, name)
            key = "%s/%s" % (wave, name)
            if key in seen:
                continue
            seen.add(key)
            if "/" in name:
                nested.add((rel, key))
                continue
            if _in_head(self.root, rel):
                continue
            binding_missing += 1
            on_disk = os.path.isfile(os.path.join(self.root, _x(rel)))
            self.fail(
                cond,
                "cited wave report missing from HEAD: w%s/%s (%s)%s"
                % (wave, name, rel, "; present on disk only" if on_disk else ""),
            )
        for rel, key in sorted(nested):
            if not _in_head(self.root, rel):
                self.warn(cond, "cited nested path not in HEAD: w%s" % key)

        rc, out, _e = _git(self.root, "ls-tree", "-r", "--name-only", "HEAD", "--", ".ufo/waves/round-%d" % self.n)
        committed = [p for p in out.splitlines() if p.endswith(".md")]
        basenames = {os.path.basename(p) for p in committed}
        bare_re = re.compile(r"(?<![\w./-])(R%d[A-Za-z0-9_-]*\.md)(?![\w./-])" % self.n)
        bare = sorted(set(bare_re.findall(text)))
        for name in bare:
            if name not in basenames:
                self.warn(
                    cond,
                    "bare wave-report name cited but absent from every wave dir in HEAD: %s" % name,
                )

        if binding_missing == 0:
            self.ok(
                cond,
                "%d w*/<Name>.md citation(s) resolve in HEAD (%d nested advisory, %d bare name(s) checked)"
                % (len(seen) - len(nested), len(nested), len(bare)),
            )

    def run(self):
        rc, head, _err = _git(self.root, "rev-parse", "--short", "HEAD")
        self.head = head.strip() if rc == 0 else "?"
        self.check_waves()
        self.check_status()
        self.check_stray_err()
        self.check_pointers()
        failed = [k for k, _ in CONDITIONS if any(sev == FAIL for sev, _m, _d in self.findings[k])]
        self.exit_code = 0 if not failed else 1
        self.failed_conditions = failed
        return self.exit_code

    def as_dict(self):
        return {
            "tool": "prefile-gate",
            "root": self.root,
            "round": self.n,
            "head": self.head,
            "exit_code": self.exit_code,
            "verdict": "GREEN" if self.exit_code == 0 else "RED",
            "failed_conditions": self.failed_conditions,
            "conditions": [
                {
                    "key": key,
                    "title": title,
                    "status": "FAIL"
                    if any(s == FAIL for s, _m, _d in self.findings[key])
                    else ("WARN" if any(s == WARN for s, _m, _d in self.findings[key]) else "PASS"),
                    "findings": [
                        {"severity": s, "message": m, "detail": d}
                        for s, m, d in self.findings[key]
                    ],
                    "notes": self.notes[key],
                }
                for key, title in CONDITIONS
            ],
        }

    def render(self):
        lines = [
            "prefile-gate: root=%s round=%d head=%s" % (self.root, self.n, self.head),
        ]
        for key, title in CONDITIONS:
            fails = [m for s, m, _d in self.findings[key] if s == FAIL]
            warns = [m for s, m, _d in self.findings[key] if s == WARN]
            status = "FAIL" if fails else ("WARN" if warns else "PASS")
            lines.append("(%s) %-52s %s" % (key, title, status))
            for s, m, _d in self.findings[key]:
                if s == PASS:
                    lines.append("    PASS  " + m)
                elif s == WARN:
                    lines.append("    WARN  " + m)
                else:
                    lines.append("    FAIL  " + m)
            for n in self.notes[key]:
                lines.append("    note  " + n)
        verdict = "GREEN" if self.exit_code == 0 else "RED"
        lines.append(
            "GATE %s%s  (exit %d)"
            % (
                verdict,
                ""
                if not self.failed_conditions
                else " — failing: " + ", ".join(self.failed_conditions),
                self.exit_code,
            )
        )
        return "\n".join(lines)


# --------------------------------------------------------------------------
# selftest: sandbox git fixtures, red for every condition, green when clean
# --------------------------------------------------------------------------

BASE_FILES = {
    "plans/round-41-claims.md": "# claims\n",
    ".ufo/waves/round-41/w1.ready": '{"wave":"r41-w1"}\n',
    ".ufo/waves/round-41/w1.ready.dispatched": '{"seats":2}\n',
    ".ufo/waves/round-41/w1-dispatch.json": '{"wave":"r41-w1"}\n',
    ".ufo/waves/round-41/r41-w1-results.json": '{"wave":"r41-w1","results":[]}\n',
    ".ufo/waves/round-41/w2.ready": '{"wave":"r41-w2"}\n',
    ".ufo/waves/round-41/w2.ready.dispatched": '{"seats":2}\n',
    ".ufo/waves/round-41/w2-dispatch.json": '{"wave":"r41-w2"}\n',
    ".ufo/waves/round-41/w2-results.json": '{"wave":"r41-w2","results":[]}\n',
    ".ufo/waves/round-41/w1/R41Alpha.md": "# alpha\n",
    ".ufo/waves/round-41/w2/R41Beta.md": "# beta\n",
    ".ufo/waves/round-41/w2/R41W2Gamma.md": "# gamma\n",
    "corpus/lessons/round-41.md": (
        "# Round 41\n\nSee `w1/R41Alpha.md` and `w2/R41Beta.md`; "
        "wave-2 review `w2/R41W2Gamma.md`.\n"
    ),
    "tools/round-41/stub.py": "# stub\n",
    "corpus/evidence/round-41/c1/stub.txt": "stub\n",
}


def _write(root, rel, content):
    path = os.path.join(root, _x(rel))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _rm(root, rel):
    path = os.path.join(root, _x(rel))
    if os.path.isfile(path):
        os.unlink(path)


def _fx_git(fx, *args):
    p = subprocess.run(["git", "-C", fx, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("fixture git %s failed: %s" % (args[0], p.stderr.decode()))
    return p.stdout.decode()


def make_fixture(work, name, mutate=None, commit=True, post=None):
    fx = os.path.join(work, name)
    os.makedirs(fx)
    subprocess.run(
        ["git", "-c", "init.defaultBranch=main", "-C", fx, "init", "-q"], check=True
    )
    top = _fx_git(fx, "rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(fx):
        raise RuntimeError("fixture toplevel %s != %s" % (top, fx))
    files = dict(BASE_FILES)
    if mutate:
        mutate(files)
    for rel, content in files.items():
        if content is None:
            continue
        _write(fx, rel, content)
    if commit:
        _fx_git(fx, "add", "-A")
        _fx_git(
            fx,
            "-c",
            "user.name=fx",
            "-c",
            "user.email=fx@fx",
            "commit",
            "-q",
            "-m",
            "fixture",
        )
    if post:
        post(fx)
    return fx


def _run_gate(root, round_no=41):
    g = Gate(_norm_root(root), round_no)
    code = g.run()
    return code, g.render(), g.as_dict()


SELFTEST_CASES = [
    # name, mutate, commit, post, expect_exit, must_contain
    ("green-clean", None, True, None, 0, ["GATE GREEN"]),
    (
        "red-wave-running-no-dispatched",
        lambda f: f.pop(".ufo/waves/round-41/w1.ready.dispatched"),
        True,
        None,
        1,
        ["FAIL", "no w1.ready.dispatched", "GATE RED"],
    ),
    (
        "red-wave-no-results",
        lambda f: (f.pop(".ufo/waves/round-41/r41-w1-results.json"), f.pop(".ufo/waves/round-41/w2-results.json")),
        True,
        None,
        1,
        ["no results file", "looked for w1-results.json and r41-w1-results.json"],
    ),
    (
        "green-results-both-naming-variants",
        lambda f: (
            f.pop(".ufo/waves/round-41/r41-w1-results.json"),
            f.update({".ufo/waves/round-41/w1-results.json": '{"wave":"r41-w1"}\n'}),
        ),
        True,
        None,
        0,
        ["w1 settled: .ufo/waves/round-41/w1-results.json", "w2 settled"],
    ),
    (
        "red-tracked-modification",
        None,
        True,
        lambda fx: _write(fx, "plans/round-41-claims.md", "# claims edited\n"),
        1,
        ["M plans/round-41-claims.md"],
    ),
    (
        "red-untracked-in-every-scope",
        None,
        True,
        lambda fx: [
            _write(fx, ".ufo/waves/round-41/w1/stray.txt", "x\n"),
            _write(fx, "corpus/evidence/round-41/c1/stray.txt", "x\n"),
            _write(fx, "plans/round-99-claims.md", "x\n"),
            _write(fx, "tools/round-41/stray.py", "x\n"),
        ],
        1,
        [
            "?? .ufo/waves/round-41/w1/stray.txt",
            "?? corpus/evidence/round-41/c1/stray.txt",
            "?? plans/round-99-claims.md",
            "?? tools/round-41/stray.py",
        ],
    ),
    (
        "red-stray-err-in-lane-root",
        None,
        True,
        lambda fx: _write(fx, "green.err", "boom\n"),
        1,
        ["stray stderr file in lane root: green.err"],
    ),
    (
        "red-dead-pointer",
        lambda f: f.update(
            {"corpus/lessons/round-41.md": "# Round 41\n\nSee `w1/R41Alpha.md` and `w2/R41Missing.md`.\n"}
        ),
        True,
        None,
        1,
        ["cited wave report missing from HEAD: w2/R41Missing.md", "GATE RED"],
    ),
    (
        "red-lesson-not-committed",
        lambda f: f.pop("corpus/lessons/round-41.md"),
        True,
        lambda fx: _write(fx, "corpus/lessons/round-41.md", "# Round 41\n\nSee `w1/R41Alpha.md`.\n"),
        1,
        ["is not in the committed tree", "it exists on disk only", "GATE RED"],
    ),
    (
        "green-dirty-lesson-reads-head-bytes",
        None,
        True,
        lambda fx: _write(
            fx,
            "corpus/lessons/round-41.md",
            "# Round 41\n\nSee `w2/R41Dead.md`.\n",
        ),
        0,
        ["has uncommitted edits; gate read the HEAD bytes", "GATE GREEN"],
    ),
    (
        "advisory-partial-ledger",
        lambda f: f.update(
            {
                ".ufo/waves/round-41/w1-dispatch.json": '{"wave":"r41-w1","counts":{"spawn":3,"total":3}}\n',
                ".ufo/waves/round-41/r41-w1-results.json": (
                    '{"round":41,"seats":2,"results":[{},{}]}\n'
                ),
            }
        ),
        True,
        None,
        0,
        ["results ledger has 2 entries vs dispatch total 3 (partial)", "GATE GREEN"],
    ),
    (
        "advisory-only-ignored-residue-and-bare-name",
        lambda f: f.update(
            {
                ".gitignore": "tools/round-41/__pycache__/\n",
                "corpus/lessons/round-41.md": (
                    "# Round 41\n\nSee `w1/R41Alpha.md`; also `R41W2Nonexistent.md` "
                    "and `w2/Nested/Deep.md`.\n"
                ),
            }
        ),
        True,
        lambda fx: _write(fx, "tools/round-41/__pycache__/x.pyc", "x\n"),
        0,
        ["WARN  ", "ignored path(s) under round scope", "bare wave-report name cited but absent"],
    ),
]


def selftest(work_root):
    work = tempfile.mkdtemp(prefix="prefile-gate-selftest.", dir=work_root)
    pass_n = fail_n = 0
    rows = []
    try:
        for name, mutate, commit, post, expect, needles in SELFTEST_CASES:
            fx = make_fixture(work, name, mutate=mutate, commit=commit, post=post)
            code, out, _data = _run_gate(fx, 41)
            problems = []
            if code != expect:
                problems.append("exit %d != expected %d" % (code, expect))
            for needle in needles:
                if needle not in out:
                    problems.append("missing output: %r" % needle)
            verdict = "pass" if not problems else "fail"
            if problems:
                fail_n += 1
            else:
                pass_n += 1
            rows.append((name, verdict, expect, code, problems))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    for name, verdict, expect, code, problems in rows:
        print("SELFTEST %-4s %-44s expect=%d got=%d" % (verdict.upper(), name, expect, code))
        for p in problems:
            print("         " + p)
    print("SELFTEST cases=%d pass=%d fail=%d" % (len(rows), pass_n, fail_n))
    return 0 if fail_n == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="kaidoku pre-file gate (read-only)")
    ap.add_argument("--root", help="lane work-tree toplevel")
    ap.add_argument("--round", type=int, help="round number, e.g. 41")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--selftest", action="store_true", help="run sandbox fixture selftest")
    ap.add_argument(
        "--work",
        help="scratch parent for selftest fixtures (default: $TMPDIR or system temp)",
    )
    args = ap.parse_args(argv)

    if args.selftest:
        work_root = args.work or os.environ.get("TMPDIR") or None
        return selftest(work_root)

    if not args.root or args.round is None:
        ap.error("--root and --round are required (or use --selftest)")

    gate = Gate(_norm_root(args.root), args.round)
    code = gate.run()
    if args.json:
        print(json.dumps(gate.as_dict(), indent=2, sort_keys=True))
    else:
        print(gate.render())
    return code


if __name__ == "__main__":
    sys.exit(main())
