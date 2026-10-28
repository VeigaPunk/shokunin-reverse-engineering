#!/usr/bin/env python3
"""R45W2SweepAudit: classify every changed path in FREEZE..main against the
seat-declared commit scope, read-only."""
import json
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"
MAIN = "main"

EXACT = {
    "plans/round-45-claims.md",
    "SKILL.md",
    "corpus/SOURCES.md",
    "corpus/lessons/round-45.md",
    "LOG.md",
    "SCORECARD.md",
}
PREFIX = ("tools/round-45/", ".ufo/waves/round-45/")


def git(*args):
    return subprocess.run(
        ["git", "-C", ROOT, *args], capture_output=True, text=True, check=True
    ).stdout


def in_scope(path):
    return path in EXACT or path.startswith(PREFIX)


def main():
    revs = git("rev-list", "--reverse", f"{FREEZE}..{MAIN}").split()
    commits = []
    violations = []
    fleet_ish = []
    top_components = {}
    for rev in revs:
        subject = git("log", "-1", "--format=%s", rev).strip()
        parents = git("log", "-1", "--format=%P", rev).split()
        raw = subprocess.run(
            ["git", "-C", ROOT, "diff-tree", "--no-commit-id", "--name-status", "-r", rev],
            capture_output=True, text=True, check=True,
        ).stdout
        rows = []
        for line in raw.splitlines():
            if not line.strip():
                continue
            status, path = line.split("\t", 1)
            rows.append((status, path))
            top = path.split("/", 1)[0]
            top_components[top] = top_components.get(top, 0) + 1
            if not in_scope(path):
                violations.append({"commit": rev, "status": status, "path": path})
            # fleet-repo path shapes: the lane repo is a nested git repo; a
            # fleet-relative path would have to name a fleet-root entry.
            if top in {"scripts", "docs", "agents", "harnesses", "ufo", "bin", "kaidoku"} and not path.startswith("kaidoku-shokunin/"):
                fleet_ish.append({"commit": rev, "path": path})
        commits.append({
            "rev": rev,
            "subject": subject,
            "parents": parents,
            "n_paths": len(rows),
            "paths": rows,
            "violations": [p for s, p in rows if not in_scope(p)],
        })
    out = {
        "freeze": FREEZE,
        "main": git("rev-parse", MAIN).strip(),
        "n_commits": len(commits),
        "commits": commits,
        "violations": violations,
        "fleet_path_candidates": fleet_ish,
        "top_components": top_components,
        "verdict": "clean" if not violations else "sweep_finding",
    }
    print(json.dumps(out, indent=2))
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
