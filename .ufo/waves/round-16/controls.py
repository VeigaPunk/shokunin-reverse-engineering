#!/usr/bin/env python3
"""Report no-harm controls for a round from immutable lane Git objects.

Usage: python3 -I .ufo/waves/round-16/controls.py <before> <after>

Both revisions are resolved to commits and read only through `git show` and
`git ls-tree` blobs; the worktree is never touched and nothing is executed.
Every field is a bounded byte observation, not a verdict: `prefix_preserved`
reports only byte-prefix retention (append-only), `unchanged`/`byte_identical`
report full blob-SHA equality, and the craft figures replicate command A's
knowledge-file range integrity check only — never a semantic or
all-pointer audit. The report pins the resolved BEFORE/AFTER commits and the
verbatim producing argv (`sys.argv`) and full original command line
(`sys.orig_argv`, interpreter flags included) so an outer receipt can carry
the exact subprocess argv unmodified. This script computes no conformance
gate: exit 0 means the report completed; exit 2 means usage error,
unresolvable revision, or missing structural anchor. Git inherits the
caller's environment (GIT_* variables could in principle redirect object
reads); constraining that surface is outside this report's narrow round and
is recorded here as a limitation, not hardened.
"""
import hashlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

APPEND_ONLY = ["LOG.md"]
OLD_PREFIX_DIRS = ["corpus/lessons", "corpus/knowledge"]
VERIFIER_GLOB = re.compile(r"^corpus/lessons/[^/]*-verifier-spotcheck\.md$")
FROZEN_PREFIXES = [
    ".ufo/waves/round-14/",
    ".ufo/waves/round-15/",
    "evidence/round-1-2026-10-15/",
]
QUOTE_SCRIPT = ".ufo/waves/round-14/tools/quote-fidelity.py"
SOURCE_ROW = re.compile(r"^\|\s*S\d{3,}\s*\|")
RULE_REF = re.compile(
    r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
)
USED_BY_COLUMN = 11  # `line.split('|')` keeps leading ''; used-by is index 11


def git(*args, text=True):
    command = ["git", "-C", str(ROOT), *args]
    if text:
        return subprocess.check_output(command, text=True, encoding="utf-8")
    return subprocess.check_output(command)


def fail(message):
    print(f"controls.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def resolve(name):
    try:
        return git("rev-parse", "--verify", f"{name}^{{commit}}").strip()
    except (subprocess.CalledProcessError, OSError) as error:
        fail(f"cannot resolve commit {name!r}: {error}")


class Rev:
    def __init__(self, revision):
        self.revision = revision
        try:
            entries = git("ls-tree", "-r", "-z", revision).split("\x00")
        except (subprocess.CalledProcessError, OSError):
            fail(f"cannot list tree at {revision}")
        # entry form: "<mode> <type> <sha>\t<path>"
        self.blobs = {}
        for entry in entries:
            if not entry:
                continue
            meta, _, path = entry.partition("\t")
            parts = meta.split()
            if len(parts) >= 3 and parts[1] == "blob":
                self.blobs[path] = parts[2]
        self._bytes = {}

    def exists(self, path):
        return path in self.blobs

    def sha(self, path):
        return self.blobs.get(path)

    def get(self, path):
        """Raw blob bytes at this revision; never the worktree."""
        if path not in self._bytes:
            try:
                self._bytes[path] = git(
                    "show", f"{self.revision}:{path}", text=False
                )
            except (subprocess.CalledProcessError, OSError):
                fail(f"cannot read {path} at {self.revision}")
        return self._bytes[path]


def craft_section(rev):
    """Command-A craft counts at one revision (SCORECARD.md recipe A).

    `citation_resolved_rules` is only knowledge-file existence plus
    in-range line citations — the same bounded check command A runs — not a
    semantic audit, pointer audit, or evidence of correctness.
    """
    skill = rev.get("SKILL.md").decode("utf-8")
    try:
        craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        fail(f"SKILL.md at {rev.revision} has no '## Queue-drain craft' section")
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    resolved = 0
    for rule in rules:
        refs = RULE_REF.findall(rule)
        valid = bool(refs)
        for name, first, last in refs:
            path = "corpus/knowledge/" + name
            if not rev.exists(path):
                valid = False
                continue
            count = len(rev.get(path).decode("utf-8").splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        resolved += int(valid)
    return {
        "craft_sha256": hashlib.sha256(craft.encode("utf-8")).hexdigest(),
        "rule_blocks": len(rules),
        "citation_resolved_rules": resolved,
    }


def source_rows(rev):
    sources = rev.get("corpus/SOURCES.md").decode("utf-8")
    rows = [
        line.split("|") for line in sources.splitlines() if SOURCE_ROW.match(line)
    ]
    if not rows:
        fail(f"corpus/SOURCES.md at {rev.revision} has no source rows")
    return {
        row[1].strip(): [
            cell.strip() if index < len(row) else ""
            for index, cell in enumerate(row)
        ]
        for row in rows
        if len(row) > 1
    }


def prefix_report(before, after, path):
    old = before.get(path)
    if not after.exists(path):
        return {
            "prefix_preserved": False,
            "byte_identical": False,
            "missing_at_after": True,
        }
    new = after.get(path)
    return {
        "prefix_preserved": new.startswith(old),
        "appended_bytes": max(len(new) - len(old), 0),
        "byte_identical": before.sha(path) == after.sha(path),
    }


def unchanged_report(before, after, paths):
    out = {}
    for path in sorted(paths):
        if not before.exists(path):
            out[path] = {"unchanged": False, "absent_at_before": True}
        elif not after.exists(path):
            out[path] = {"unchanged": False, "missing_at_after": True}
        else:
            out[path] = {"unchanged": before.sha(path) == after.sha(path)}
    return out


def dir_prefix_report(before, after, prefix):
    paths = sorted(
        p
        for p in before.blobs
        if p.startswith(prefix + "/") and p.endswith(".md")
    )
    rows = {path: prefix_report(before, after, path) for path in paths}
    return {
        "checked": len(rows),
        "prefix_preserved": sum(
            1 for row in rows.values() if row["prefix_preserved"]
        ),
        "files": rows,
    }


def frozen_report(before, after):
    paths = [
        p
        for p in before.blobs
        if any(p.startswith(prefix) for prefix in FROZEN_PREFIXES)
    ]
    files = unchanged_report(before, after, paths)
    return {
        "checked": len(files),
        "unchanged": sum(1 for row in files.values() if row["unchanged"]),
        "quote_script_unchanged": (
            before.exists(QUOTE_SCRIPT)
            and after.exists(QUOTE_SCRIPT)
            and before.sha(QUOTE_SCRIPT) == after.sha(QUOTE_SCRIPT)
        ),
        "files": files,
    }


def sources_registry(before, after):
    old_rows = source_rows(before)
    new_rows = source_rows(after)
    immutable_violations = {}
    used_by_deltas = {}
    for sid, old_cells in old_rows.items():
        new_cells = new_rows.get(sid)
        if new_cells is None:
            immutable_violations[sid] = "row_absent_at_after"
            continue
        for index in range(max(len(old_cells), len(new_cells))):
            old = old_cells[index] if index < len(old_cells) else ""
            new = new_cells[index] if index < len(new_cells) else ""
            if old == new:
                continue
            if index == USED_BY_COLUMN:
                used_by_deltas[sid] = {"before": old, "after": new}
            else:
                immutable_violations.setdefault(sid, []).append(index)
    return {
        "rows_before": len(old_rows),
        "rows_after": len(new_rows),
        "immutable_cells_unchanged": not immutable_violations,
        "immutable_violations": immutable_violations,
        "allowed_used_by_deltas": used_by_deltas,
        "added_rows": sorted(set(new_rows) - set(old_rows)),
        "removed_rows": sorted(set(old_rows) - set(new_rows)),
    }


def main():
    if len(sys.argv) != 3:
        fail("usage: controls.py <before> <after>")
    before_name, after_name = sys.argv[1], sys.argv[2]
    before = Rev(resolve(before_name))
    after = Rev(resolve(after_name))

    verifiers = sorted(p for p in before.blobs if VERIFIER_GLOB.match(p))
    result = {
        "revisions": {
            "before_name": before_name,
            "before": before.revision,
            "after_name": after_name,
            "after": after.revision,
        },
        "log_old_prefix": {
            path: prefix_report(before, after, path) for path in APPEND_ONLY
        },
        "old_lessons_prefix": dir_prefix_report(before, after, "corpus/lessons"),
        "old_knowledge_prefix": dir_prefix_report(
            before, after, "corpus/knowledge"
        ),
        "prior_verifiers_unchanged": unchanged_report(before, after, verifiers),
        "frozen_baselines": frozen_report(before, after),
        "craft": {
            "note": (
                "command-A replication: knowledge-file existence and "
                "in-range line citations only; not a semantic or "
                "all-pointer audit"
            ),
            "before": craft_section(before),
            "after": craft_section(after),
        },
        "sources_registry": sources_registry(before, after),
        "evidence_class": "git_object_bytes",
        "invocation": {
            "argv": sys.argv,
            "orig_argv": list(getattr(sys, "orig_argv", sys.argv)),
            "argv_note": (
                "sys.argv excludes interpreter flags; sys.orig_argv retains "
                "them; outer L1 receipts should carry the exact subprocess "
                "argv unmodified"
            ),
            "executable": sys.executable,
            "isolated": bool(sys.flags.isolated),
            "repo_root": str(ROOT),
            "producing_command": shlex.join(
                list(getattr(sys, "orig_argv", [sys.executable, *sys.argv]))
            ),
        },
        "conformance_gate": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
