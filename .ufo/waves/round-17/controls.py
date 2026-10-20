#!/usr/bin/env python3
"""Report no-harm controls for round 17 from immutable lane Git objects.

Usage: python3 -I .ufo/waves/round-17/controls.py <before> <after>

Generalizes .ufo/waves/round-16/controls.py. Both revisions are resolved to
commits and read only through `git show` and `git ls-tree` blobs; the
worktree is never touched and nothing under test is executed. Every field is
a bounded byte observation, not a verdict: `prefix_preserved` reports only
byte-prefix retention (append-only), `unchanged`/`byte_identical` report
full blob-SHA equality, and the craft figures replicate command A's
knowledge-file range integrity check only — never a semantic or
all-pointer audit.

Round-17 generalizations over the r16 script:

* `prior_wave_evidence_blobs` replaces the hardcoded FROZEN_PREFIXES list
  (round-14/round-15 + one evidence dir): every blob under `.ufo/waves/` or
  `evidence/` present at BEFORE must be byte-identical at AFTER. This covers
  every prior wave and evidence subtree without enumeration.
* `quality_admission_rows` parses the numbered admission-criteria table in
  corpus/QUALITY.md and requires every row present at BEFORE to survive at
  AFTER byte-identical (r17 fixes rows 1-18 and appends row 19); new row
  numbers are reported, never rejected.
* LOG.md stays append-only (old prefix retained); every corpus/lessons and
  corpus/knowledge .md blob at BEFORE keeps its old prefix; every
  `*-verifier-spotcheck.md` at BEFORE is byte-identical; the SOURCES
  registry immutability check is unchanged (all cells frozen except the
  used-by column).

The report pins the resolved BEFORE/AFTER commits and the verbatim producing
argv (`sys.argv`) and full original command line (`sys.orig_argv`,
interpreter flags included) so an outer receipt can carry the exact
subprocess argv unmodified. This script computes no conformance gate:
exit 0 means the report completed; exit 2 means usage error, unresolvable
revision, or missing structural anchor. Git inherits the caller's
environment (GIT_* variables could in principle redirect object reads);
constraining that surface is outside this report's narrow round and is
recorded here as a limitation, not hardened.
"""
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

APPEND_ONLY = ["LOG.md"]
OLD_PREFIX_DIRS = ["corpus/lessons", "corpus/knowledge"]
VERIFIER_GLOB = re.compile(r"^corpus/lessons/[^/]*-verifier-spotcheck\.md$")
FROZEN_PREFIXES = [".ufo/waves/", "evidence/"]
QUOTE_SCRIPT = ".ufo/waves/round-14/tools/quote-fidelity.py"
QUALITY_PATH = "corpus/QUALITY.md"
ADMISSION_HEADING = "## Admission criteria"
SOURCE_ROW = re.compile(r"^\|\s*S\d{3,}\s*\|")
QUALITY_ROW = re.compile(r"^\|\s*(\d+)\s*\|")
RULE_REF = re.compile(
    r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
)
USED_BY_COLUMN = 11  # `line.split('|')` keeps leading ''; used-by is index 11


def git(root, *args, text=True):
    command = ["git", "-C", str(root), *args]
    if text:
        return subprocess.check_output(command, text=True, encoding="utf-8")
    return subprocess.check_output(command)


def fail(message):
    print(f"controls.py: {message}", file=sys.stderr)
    raise SystemExit(2)


def resolve(root, name):
    try:
        return git(root, "rev-parse", "--verify", f"{name}^{{commit}}").strip()
    except (subprocess.CalledProcessError, OSError) as error:
        fail(f"cannot resolve commit {name!r}: {error}")


class Rev:
    def __init__(self, root, revision):
        self.root = root
        self.revision = revision
        try:
            entries = git(root, "ls-tree", "-r", "-z", revision).split("\x00")
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
                    self.root, "show", f"{self.revision}:{path}", text=False
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


def admission_rows(rev):
    """Numbered `| n | ...` row lines inside the admission-criteria section.

    Keyed by row number so a renumbered or edited row shows as a violation
    rather than passing silently; returns raw line text for byte equality.
    """
    text = rev.get(QUALITY_PATH).decode("utf-8")
    try:
        section = text.split(ADMISSION_HEADING, 1)[1].split("\n## ", 1)[0]
    except IndexError:
        fail(
            f"{QUALITY_PATH} at {rev.revision} has no "
            f"'{ADMISSION_HEADING}' section"
        )
    rows = {}
    for line in section.splitlines():
        match = QUALITY_ROW.match(line)
        if match:
            rows[match.group(1)] = line
    if not rows:
        fail(f"{QUALITY_PATH} at {rev.revision} has no admission rows")
    return rows


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
    """Every `.ufo/waves/` and `evidence/` blob at BEFORE, byte-identical.

    Generalized from r16's fixed prefix list: the scope is derived from the
    BEFORE tree itself, so any prior wave or evidence path is covered
    without being named.
    """
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
        "scope": sorted(FROZEN_PREFIXES),
        "files": files,
    }


def quality_registry(before, after):
    """Admission-criteria rows: every BEFORE row byte-identical at AFTER."""
    old_rows = admission_rows(before)
    new_rows = admission_rows(after)
    violations = {}
    for number, line in old_rows.items():
        if number not in new_rows:
            violations[number] = "row_absent_at_after"
        elif new_rows[number] != line:
            violations[number] = "row_text_changed"
    return {
        "rows_before": len(old_rows),
        "rows_after": len(new_rows),
        "prior_rows_byte_identical": not violations,
        "violations": violations,
        "added_rows": sorted(set(new_rows) - set(old_rows), key=int),
        "removed_rows": sorted(set(old_rows) - set(new_rows), key=int),
        "note": (
            "raw line equality inside '## Admission criteria' only; the "
            "signals table and row semantics are out of scope"
        ),
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


def build_report(root, before_name, after_name):
    before = Rev(root, resolve(root, before_name))
    after = Rev(root, resolve(root, after_name))

    verifiers = sorted(p for p in before.blobs if VERIFIER_GLOB.match(p))
    return {
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
        "prior_wave_evidence_blobs": frozen_report(before, after),
        "quality_admission_rows": quality_registry(before, after),
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
            "repo_root": str(root),
            "producing_command": shlex.join(
                list(getattr(sys, "orig_argv", [sys.executable, *sys.argv]))
            ),
        },
        "conformance_gate": False,
    }


FIXTURE_BEFORE = {
    "LOG.md": "# log\nline one\n",
    "SKILL.md": (
        "# skill\n\n## Queue-drain craft (test)\n\n"
        "- **rule one** see corpus/knowledge/k-one.md:1-2\n\n"
        "## Other\n"
    ),
    "corpus/SOURCES.md": (
        "| id | a | b | c | d | e | f | g | h | i | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        "| S001 | a | b | c | d | e | f | g | h | i | r1 |\n"
    ),
    "corpus/QUALITY.md": (
        "# quality\n\n## Admission criteria\n\n"
        "| # | criterion | why | supersedes |\n|---|---|---|---|\n"
        "| 1 | first | l1 | — |\n"
        "| 2 | second | l2 | — |\n\n"
        "## Signals of weak material\n\n| # | signal |\n|---|---|\n"
        "| 1 | weak |\n"
    ),
    "corpus/lessons/round-1.md": "# l1\n",
    "corpus/lessons/round-1-verifier-spotcheck.md": "# spot\n",
    "corpus/knowledge/k-one.md": "one\ntwo\n",
    ".ufo/waves/round-1/run.json": '{"a": 1}\n',
    "evidence/round-1/x.json": '{"e": 1}\n',
}

FIXTURE_AFTER_APPEND = {
    "LOG.md": "# log\nline one\nline two appended\n",
    "corpus/lessons/round-2.md": "# l2\n",
    "corpus/QUALITY.md": (
        "# quality\n\n## Admission criteria\n\n"
        "| # | criterion | why | supersedes |\n|---|---|---|---|\n"
        "| 1 | first | l1 | — |\n"
        "| 2 | second | l2 | — |\n"
        "| 3 | third appended | l3 | — |\n\n"
        "## Signals of weak material\n\n| # | signal |\n|---|---|\n"
        "| 1 | weak |\n"
    ),
    ".ufo/waves/round-2/new.json": '{"b": 2}\n',
}

FIXTURE_AFTER_RED = {
    ".ufo/waves/round-1/run.json": '{"a": 999}\n',
    "corpus/QUALITY.md": (
        "# quality\n\n## Admission criteria\n\n"
        "| # | criterion | why | supersedes |\n|---|---|---|---|\n"
        "| 1 | first EDITED | l1 | — |\n"
        "| 2 | second | l2 | — |\n\n"
        "## Signals of weak material\n\n| # | signal |\n|---|---|\n"
        "| 1 | weak |\n"
    ),
}


def _commit(root, files, message):
    for path, content in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    git(root, "add", "-A")
    git(
        root,
        "-c", "user.email=selftest@localhost",
        "-c", "user.name=selftest",
        "commit", "-qm", message,
        text=True,
    )
    return git(root, "rev-parse", "HEAD").strip()


def selftest():
    """Temporary fixture repo: one clean append case, one red mutation case."""
    cases = 0
    failures = []
    root = Path(tempfile.mkdtemp(prefix="controls17-selftest-"))
    try:
        git(root, "init", "-q")
        before = _commit(root, FIXTURE_BEFORE, "before")

        clean = _commit(root, FIXTURE_AFTER_APPEND, "clean append")
        report = build_report(root, before, clean)
        checks = [
            ("log prefix", report["log_old_prefix"]["LOG.md"]["prefix_preserved"]),
            ("frozen all", report["prior_wave_evidence_blobs"]["unchanged"]
             == report["prior_wave_evidence_blobs"]["checked"]),
            ("verifier", all(
                row["unchanged"]
                for row in report["prior_verifiers_unchanged"].values())),
            ("quality rows", report["quality_admission_rows"]["prior_rows_byte_identical"]),
            ("quality added", report["quality_admission_rows"]["added_rows"] == ["3"]),
            ("sources", report["sources_registry"]["immutable_cells_unchanged"]),
            ("revisions", report["revisions"]["before"] == before
             and report["revisions"]["after"] == clean),
        ]
        for name, ok in checks:
            cases += 1
            if not ok:
                failures.append(f"clean:{name}")

        red = _commit(root, FIXTURE_AFTER_RED, "red mutation")
        report = build_report(root, clean, red)
        checks = [
            ("frozen detects", not all(
                row["unchanged"]
                for row in report["prior_wave_evidence_blobs"]["files"].values())),
            ("frozen names", report["prior_wave_evidence_blobs"]["files"]
             [".ufo/waves/round-1/run.json"]["unchanged"] is False),
            ("quality detects", not report["quality_admission_rows"]
             ["prior_rows_byte_identical"]),
            ("quality names", report["quality_admission_rows"]["violations"]
             .get("1") == "row_text_changed"),
        ]
        for name, ok in checks:
            cases += 1
            if not ok:
                failures.append(f"red:{name}")
    finally:
        for base, dirs, files in os.walk(root, topdown=False):
            for name in files:
                os.remove(os.path.join(base, name))
            for name in dirs:
                os.rmdir(os.path.join(base, name))
        os.rmdir(root)

    if failures:
        print(f"SELFTEST: FAILED cases={cases} {failures}")
        raise SystemExit(1)
    print(f"SELFTEST: CLEAN cases={cases}")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        selftest()
        return
    if len(sys.argv) != 3:
        fail("usage: controls.py <before> <after> | controls.py --selftest")
    print(
        json.dumps(build_report(ROOT, sys.argv[1], sys.argv[2]),
                   indent=2, sort_keys=True)
    )


if __name__ == "__main__":
    main()
