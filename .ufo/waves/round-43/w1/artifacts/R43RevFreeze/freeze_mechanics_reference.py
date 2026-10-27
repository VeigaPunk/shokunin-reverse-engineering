#!/usr/bin/env python3
"""freeze_mechanics_reference.py — R43RevFreeze reference implementation for the
round-43 freeze mechanics (seat report: .ufo/waves/round-43/w1/R43RevFreeze.md).

Two contracts are implemented here exactly as the round-43 counters should:

1. skill_v4_region_*   — the SKILL v4 table-region extraction BOTH the frozen
   interpreter (tools/round-42/sqfs-triage-v4.py `parse_skill`/`craft_bounds`)
   and the round-43 counters must share, so "byte-identical region" means the
   same bytes to both.  Canonical byte form:
   `'\n'.join(lines[marker:table_end]).encode('utf-8')`; identity is compared
   as sha256 of that form.  Caveat carried from splitlines(): a CRLF flip
   inside the region is normalised away (semantically inert for the table
   read) — disclose, don't rely on raw-byte spans.

2. freeze_drift_*      — the FREEZE..REV enumeration recipe that closes the two
   holes demonstrated in the report:
     (a) evil merge: default `git log --name-only/--name-status` suppresses
         merge diffs, so a merge whose conflict resolution writes a frozen
         path is invisible; fix: `-m --diff-merges=first-parent` plus a
         tree-level blob-hash backstop per frozen file;
     (b) rewrite/re-add: a rewritten history re-adds an altered frozen path
         with status 'A', which the round-42 c2-counter filter
         (M/D/R/T/U only) drops; fix: assert FREEZE is an ancestor of REV,
         count 'A' as a touch whenever the path exists at FREEZE, keep the
         tree backstop.

   SKILL-region drift is checked by comparing the extracted region at EVERY
   commit in FREEZE..REV (commit list without a path filter, so neither hole
   applies to the region itself) against the freeze region.

Stdlib only; read-only git; honours TMPDIR (no temp files are written).
Self-check (read-only, against the live lane):

  python3 -I -B freeze_mechanics_reference.py --selfcheck --root <LANE>
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys

MARKER = "<!-- sqfs-triage-table v4 -->"
ACTIONS_PREFIX = "<!-- sqfs-triage-actions:"
CRAFT_PREFIX = "queue-drain craft"
SKILL_REL = "SKILL.md"


# ---------------------------------------------------------- region extraction
# Byte-for-byte the rule tools/round-42/sqfs-triage-v4.py documents and implements.

def _is_h2(line: str) -> bool:
    return line.startswith("## ") and not line.startswith("### ")


def craft_bounds(lines: list[str]) -> tuple[int, int]:
    start = None
    for i, line in enumerate(lines):
        if _is_h2(line) and line[3:].strip().lower().startswith(CRAFT_PREFIX):
            start = i + 1
            break
    if start is None:
        raise ValueError('no "## Queue-drain craft" heading in the document')
    end = len(lines)
    for j in range(start, len(lines)):
        if _is_h2(lines[j]):
            end = j
            break
    return start, end


def skill_v4_region_lines(text: str) -> tuple[list[str], int, int]:
    """Return (lines, marker_idx, table_end_idx) — region is lines[marker:table_end]."""
    lines = text.splitlines()
    start, end = craft_bounds(lines)
    marker = None
    for i in range(start, end):
        if MARKER in lines[i]:
            marker = i
            break
    if marker is None:
        raise ValueError("v4 marker absent from the craft section")
    table_start = None
    for i in range(marker + 1, end):
        if lines[i].lstrip().startswith("|"):
            table_start = i
            break
    if table_start is None:
        raise ValueError("no markdown table after the v4 marker")
    actions = table_start - 1
    while actions > start and not lines[actions].strip():
        actions -= 1
    if actions < start or ACTIONS_PREFIX not in lines[actions]:
        raise ValueError("no sqfs-triage-actions vocabulary line directly above the table")
    table_end = table_start
    while table_end < end and lines[table_end].lstrip().startswith("|"):
        table_end += 1
    return lines, marker, table_end


def skill_v4_region_bytes(text: str) -> bytes:
    lines, marker, table_end = skill_v4_region_lines(text)
    return "\n".join(lines[marker:table_end]).encode("utf-8")


def skill_v4_region_sha256(text: str) -> str:
    return hashlib.sha256(skill_v4_region_bytes(text)).hexdigest()


# ------------------------------------------------------------------ git shell

def git(root: str, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    p = subprocess.run(["git", "-C", root, *args],
                       capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p


def show(root: str, rev: str, path: str) -> str | None:
    p = git(root, "show", "%s:%s" % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


# ------------------------------------------------------------- freeze-drift walk

def assert_ancestor(root: str, freeze: str, rev: str) -> None:
    """FREEZE must be an ancestor of REV, else FREEZE..REV range semantics are
    broken (rewrite/rebase) and every drift verdict is meaningless."""
    p = git(root, "merge-base", "--is-ancestor", freeze, rev, check=False)
    if p.returncode != 0:
        raise RuntimeError("freeze %s is not an ancestor of rev %s" % (freeze, rev))


def path_exists_at(root: str, rev: str, path: str) -> bool:
    return git(root, "cat-file", "-e", "%s:%s" % (rev, path), check=False).returncode == 0


def tree_blob(root: str, rev: str, path: str) -> str | None:
    p = git(root, "rev-parse", "%s:%s" % (rev, path), check=False)
    return p.stdout.strip() if p.returncode == 0 else None


def touched_frozen_paths(root: str, freeze: str, rev: str,
                         frozen_paths: list[str]) -> dict[str, list[str]]:
    """{path: [commit, ...]} for frozen paths modified in FREEZE..REV.

    - merge-safe: -m --diff-merges=first-parent surfaces a merge resolution
      that writes a frozen path (default git log suppresses merge diffs);
    - rewrite-safe: status 'A' counts as a touch whenever the path already
      exists at FREEZE (a rewrite re-adding altered content shows 'A');
    - '--no-renames' so a rename surfaces as D (+A) and cannot smuggle past.
    """
    out: dict[str, list[str]] = {}
    rng = "%s..%s" % (freeze, rev)
    for path in frozen_paths:
        p = git(root, "log", "--format=@@%H", "--name-status", "--no-renames",
                "-m", "--diff-merges=first-parent", rng, "--", path)
        cur = None
        hits: list[str] = []
        for line in p.stdout.splitlines():
            if line.startswith("@@"):
                cur = line[2:].strip()
                continue
            if not line.strip() or cur is None:
                continue
            st = line.split("\t")[0].strip()[:1]
            if st in ("M", "D", "R", "T", "U"):
                hits.append(cur)
            elif st == "A" and path_exists_at(root, freeze, path):
                hits.append(cur)  # re-add of a frozen path = rewrite signature
        if hits:
            out[path] = sorted(set(hits))
    return out


def skill_region_drift(root: str, freeze: str, rev: str) -> list[str]:
    """Commits in FREEZE..REV whose v4 region differs from the freeze's.

    The commit list has NO path filter, so an evil merge or a rewrite cannot
    hide: every commit in the range gets its region extracted and compared.
    A touch-and-restore still drifts (the intermediate commit differs).
    """
    freeze_text = show(root, freeze, SKILL_REL)
    if freeze_text is None:
        raise RuntimeError("SKILL.md absent at freeze")
    want = skill_v4_region_sha256(freeze_text)
    bad: list[str] = []
    rng = "%s..%s" % (freeze, rev)
    for commit in git(root, "log", "--format=%H", rng).stdout.split():
        text = show(root, commit, SKILL_REL)
        if text is None:
            bad.append(commit)  # SKILL.md deleted mid-range
            continue
        try:
            got = skill_v4_region_sha256(text)
        except ValueError:
            bad.append(commit)  # marker/table/actions missing mid-range
            continue
        if got != want:
            bad.append(commit)
    return bad


def tree_backstop_differs(root: str, freeze: str, rev: str,
                          frozen_files: list[str]) -> list[str]:
    """Blob-hash inequality FREEZE vs REV for frozen regular files.

    Independent of every walk option; catches anything the per-commit status
    parse could still miss (evil merges included, since the merge's own tree
    carries the write).  Inequality here must already appear in the walk
    output; a clean walk plus a differing blob means the walk has a bug.
    """
    out = []
    for path in frozen_files:
        a, b = tree_blob(root, freeze, path), tree_blob(root, rev, path)
        if a != b:
            out.append(path)
    return out


# ------------------------------------------------------------------- selfcheck

def selfcheck(root: str) -> int:
    ok = True
    shas = {}
    for rev in ("d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b",
                "6b9e64fe7e0de202d9383baad5792fbfe039a743", "HEAD"):
        text = show(root, rev, SKILL_REL)
        lines, m, e = skill_v4_region_lines(text)
        shas[rev] = skill_v4_region_sha256(text)
        print("%s  region SKILL.md:%d-%d (%d lines)  sha256 %s..."
              % (rev[:9], m + 1, e, e - m, shas[rev][:16]))
    if len(set(shas.values())) != 1:
        ok = False
        print("FAIL: v4 region differs across d1681696 / base / HEAD")
    else:
        print("OK: v4 region byte-identical at d1681696, base, HEAD")
    # frozen round-42 tools: no drift d1681696..HEAD + blob identity
    p = git(root, "log", "--pretty=format:", "--name-only", "--no-renames",
            "d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b..HEAD", "--",
            "tools/round-42/sqfs-triage-v4.py",
            "tools/round-42/indep-eval-v4.py", "tools/round-42/fixtures.json",
            check=False)
    touched = sorted({l.strip() for l in p.stdout.splitlines() if l.strip()})
    for f in ("tools/round-42/sqfs-triage-v4.py",
              "tools/round-42/indep-eval-v4.py", "tools/round-42/fixtures.json"):
        same = tree_blob(root, "d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b", f) == \
               tree_blob(root, "HEAD", f)
        print("%s d1681696..HEAD touched=%s blob_same=%s" % (f, f in touched, same))
        ok = ok and not touched and same
    print("selfcheck:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--selfcheck", action="store_true")
    args = ap.parse_args(argv[1:])
    if args.selfcheck:
        return selfcheck(args.root)
    ap.error("only --selfcheck is implemented; the drift functions are "
             "imported by the round-43 counters")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
