#!/usr/bin/env python3
"""Report no-harm controls for round 18 from immutable lane Git objects.

Usage: python3 -I .ufo/waves/round-18/controls.py <before> <after>

Generalizes .ufo/waves/round-17/controls.py. Both revisions are resolved to
commits and read only through `git show` and `git ls-tree` blobs; the
worktree is never touched and nothing under test is executed. Every field is
a bounded byte observation, not a verdict: `prefix_preserved` reports only
byte-prefix retention (append-only), `unchanged`/`byte_identical` report
full blob-SHA equality, and the craft figures replicate command A's
knowledge-file range integrity check only — never a semantic or
all-pointer audit.

Round-18 changes over the r17 script (contract: .ufo/waves/round-18/
contract.md "Shared outputs"):

* `old_prefix` now covers LOG.md and SCORECARD.md (r17 had LOG.md only).
* `prior_corpus_text` tightens corpus/lessons and corpus/knowledge from
  old-prefix to byte-identical, with exactly one contracted exception:
  corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md may retain its
  old prefix (round 18 appends R17-* discharge lines to that file only).
* `quality_admission_rows` additionally reports `rows_1_20_identical`:
  every numbered admission row 1-20 present at BEFORE is byte-identical at
  AFTER (round 18 appends row 21).
* `sources_registry` widens the mutable cell set from used-by (column 11)
  to status (8), recheck (10) and used-by (11); `opened` (9) and every
  other cell stay immutable. Per-column deltas are named.
* `prior_wave_evidence_blobs` carves out the contract-named round-17
  in-place fix files and the round-17 SHA256SUMS from the byte-identical
  requirement and reports them under `contracted_modifications`;
  `r17_sums_restored_line` checks SHA256SUMS changed by exactly the
  restored `<sha256>  predictions/carriers.tsv` line (and nothing else).
* `skill_md_diff` lists SKILL.md deleted and added lines (round 18 edits
  the SKILL registry table in place; deletions are reported, not judged).
"""
import difflib
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

APPEND_ONLY = ["LOG.md", "SCORECARD.md"]
IDENTICAL_DIRS = ["corpus/lessons", "corpus/knowledge"]
APPENDABLE_KNOWLEDGE = {
    "corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"
}
VERIFIER_GLOB = re.compile(r"^corpus/lessons/[^/]*-verifier-spotcheck\.md$")
FROZEN_PREFIXES = [".ufo/waves/", "evidence/"]
CONTRACTED_MODIFICATIONS = {
    ".ufo/waves/round-17/predictions/SHA256SUMS",
    ".ufo/waves/round-17/tools/carrier-run.py",
    ".ufo/waves/round-17/tools/compare.py",
    ".ufo/waves/round-17/tools/log-extract.py",
    ".ufo/waves/round-17/tools/receipt-validate.py",
    ".ufo/waves/round-17/verify.py",
}
R17_SUMS = ".ufo/waves/round-17/predictions/SHA256SUMS"
R17_CARRIERS_TSV = ".ufo/waves/round-17/predictions/carriers.tsv"
QUOTE_SCRIPT = ".ufo/waves/round-14/tools/quote-fidelity.py"
QUALITY_PATH = "corpus/QUALITY.md"
ADMISSION_HEADING = "## Admission criteria"
SKILL_PATH = "SKILL.md"
SOURCE_ROW = re.compile(r"^\|\s*S\d{3,}\s*\|")
QUALITY_ROW = re.compile(r"^\|\s*(\d+)\s*\|")
RULE_REF = re.compile(
    r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
)
MUTABLE_SOURCE_COLUMNS = {8: "status", 10: "recheck", 11: "used-by"}
DIFF_LINE_CAP = 64


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
    skill = rev.get(SKILL_PATH).decode("utf-8")
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


def corpus_text_report(before, after, prefix):
    """corpus/lessons|knowledge .md blobs: byte-identical at AFTER.

    The one contracted exception (APPENDABLE_KNOWLEDGE) may retain its old
    prefix instead; mode names which rule applied to each file.
    """
    paths = sorted(
        p
        for p in before.blobs
        if p.startswith(prefix + "/") and p.endswith(".md")
    )
    rows = {}
    for path in paths:
        if path in APPENDABLE_KNOWLEDGE:
            row = prefix_report(before, after, path)
            row["mode"] = "appendable_knowledge"
            row["ok"] = row["prefix_preserved"]
        else:
            if not after.exists(path):
                row = {"byte_identical": False, "missing_at_after": True}
            else:
                row = {"byte_identical": before.sha(path) == after.sha(path)}
            row["mode"] = "identical"
            row["ok"] = row["byte_identical"]
        rows[path] = row
    return {
        "checked": len(rows),
        "ok": sum(1 for row in rows.values() if row["ok"]),
        "violations": sorted(p for p, row in rows.items() if not row["ok"]),
        "files": rows,
    }


def r17_sums_report(before, after):
    """The one permitted SHA256SUMS change: restoring the carriers.tsv line.

    `restored_ok` holds iff the AFTER blob is byte-identical to BEFORE, or
    differs by exactly one added line of the form
    `<sha256(carriers.tsv blob at AFTER)>  predictions/carriers.tsv` with no
    removed lines. Any other delta is a violation.
    """
    report = {
        "path": R17_SUMS,
        "missing_at_before": not before.exists(R17_SUMS),
        "missing_at_after": not after.exists(R17_SUMS),
    }
    if report["missing_at_before"] or report["missing_at_after"]:
        report["restored_ok"] = False
        return report
    if before.sha(R17_SUMS) == after.sha(R17_SUMS):
        report.update(
            {"byte_identical": True, "restored_ok": True, "lines_added": []}
        )
        return report
    old_lines = set(before.get(R17_SUMS).decode("utf-8").splitlines())
    new_lines = set(after.get(R17_SUMS).decode("utf-8").splitlines())
    added = sorted(new_lines - old_lines)
    removed = sorted(old_lines - new_lines)
    expected = None
    if after.exists(R17_CARRIERS_TSV):
        digest = hashlib.sha256(after.get(R17_CARRIERS_TSV)).hexdigest()
        expected = f"{digest}  predictions/carriers.tsv"
    report.update(
        {
            "byte_identical": False,
            "lines_added": added,
            "lines_removed": removed,
            "expected_restored_line": expected,
            "restored_ok": (
                not removed
                and added == [expected]
                and expected is not None
            ),
        }
    )
    return report


def frozen_report(before, after):
    """Every `.ufo/waves/` and `evidence/` blob at BEFORE, byte-identical.

    Contract-named round-18 in-place fix files and the restored SHA256SUMS
    line are carved out of `files` and reported separately under
    `contracted_modifications` and `r17_sums_restored_line`.
    """
    paths = [
        p
        for p in before.blobs
        if any(p.startswith(prefix) for prefix in FROZEN_PREFIXES)
        and p not in CONTRACTED_MODIFICATIONS
    ]
    files = unchanged_report(before, after, paths)
    contracted = {}
    for path in sorted(CONTRACTED_MODIFICATIONS):
        if before.exists(path) or after.exists(path):
            contracted[path] = {
                "absent_at_before": not before.exists(path),
                "missing_at_after": not after.exists(path),
                "byte_identical": (
                    before.exists(path)
                    and after.exists(path)
                    and before.sha(path) == after.sha(path)
                ),
            }
    return {
        "checked": len(files),
        "unchanged": sum(1 for row in files.values() if row["unchanged"]),
        "quote_script_unchanged": (
            before.exists(QUOTE_SCRIPT)
            and after.exists(QUOTE_SCRIPT)
            and before.sha(QUOTE_SCRIPT) == after.sha(QUOTE_SCRIPT)
        ),
        "scope": sorted(FROZEN_PREFIXES),
        "contracted_modifications": contracted,
        "r17_sums_restored_line": r17_sums_report(before, after),
        "files": files,
    }


def quality_registry(before, after):
    """Admission-criteria rows: every BEFORE row byte-identical at AFTER.

    `rows_1_20_identical` is the round-18 contract facet: every numbered row
    1-20 present at BEFORE survives byte-identical (row 21 may be added).
    """
    old_rows = admission_rows(before)
    new_rows = admission_rows(after)
    violations = {}
    for number, line in old_rows.items():
        if number not in new_rows:
            violations[number] = "row_absent_at_after"
        elif new_rows[number] != line:
            violations[number] = "row_text_changed"
    rows_1_20 = [str(n) for n in range(1, 21) if str(n) in old_rows]
    return {
        "rows_before": len(old_rows),
        "rows_after": len(new_rows),
        "prior_rows_byte_identical": not violations,
        "rows_1_20_present_at_before": len(rows_1_20),
        "rows_1_20_identical": not any(n in violations for n in rows_1_20),
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
    allowed_deltas = {}
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
            column = MUTABLE_SOURCE_COLUMNS.get(index)
            if column is not None:
                allowed_deltas.setdefault(sid, {})[column] = {
                    "before": old,
                    "after": new,
                }
            else:
                immutable_violations.setdefault(sid, []).append(index)
    return {
        "rows_before": len(old_rows),
        "rows_after": len(new_rows),
        "mutable_columns": MUTABLE_SOURCE_COLUMNS,
        "immutable_cells_unchanged": not immutable_violations,
        "immutable_violations": immutable_violations,
        "allowed_deltas": allowed_deltas,
        "added_rows": sorted(set(new_rows) - set(old_rows)),
        "removed_rows": sorted(set(old_rows) - set(new_rows)),
    }


def skill_diff(before, after):
    """SKILL.md line delta: deleted and added lines listed, not judged."""
    if not after.exists(SKILL_PATH):
        return {"missing_at_after": True}
    if before.sha(SKILL_PATH) == after.sha(SKILL_PATH):
        return {"byte_identical": True, "deleted_lines": [], "added_lines": []}
    old = before.get(SKILL_PATH).decode("utf-8").splitlines()
    new = after.get(SKILL_PATH).decode("utf-8").splitlines()
    deleted, added = [], []
    for line in difflib.unified_diff(old, new, lineterm="", n=0):
        if line.startswith("-") and not line.startswith("---"):
            deleted.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
    return {
        "byte_identical": False,
        "deleted_lines": deleted[:DIFF_LINE_CAP],
        "added_lines": added[:DIFF_LINE_CAP],
        "deleted_count": len(deleted),
        "added_count": len(added),
        "truncated": len(deleted) > DIFF_LINE_CAP
        or len(added) > DIFF_LINE_CAP,
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
        "old_prefix": {
            path: prefix_report(before, after, path) for path in APPEND_ONLY
        },
        "prior_corpus_text": {
            prefix: corpus_text_report(before, after, prefix)
            for prefix in IDENTICAL_DIRS
        },
        "prior_verifiers_unchanged": unchanged_report(before, after, verifiers),
        "prior_wave_evidence_blobs": frozen_report(before, after),
        "quality_admission_rows": quality_registry(before, after),
        "skill_md_diff": skill_diff(before, after),
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


CARRIERS_FIXTURE = "label\tpath\ns1\t/carriers/a\n"
SUMS_FIXTURE = (
    "a" * 64 + "  predictions/calib-x.prediction.json\n"
)
APPENDABLE_FIXTURE_PATH = (
    "corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"
)

FIXTURE_BEFORE = {
    "LOG.md": "# log\nline one\n",
    "SCORECARD.md": "# score\ncard one\n",
    "SKILL.md": (
        "# skill\n\n## Queue-drain craft (test)\n\n"
        "- **rule one** see corpus/knowledge/k-one.md:1-2\n\n"
        "## Other\n\nstale line\n"
    ),
    "corpus/SOURCES.md": (
        "| id | source | kind | tier | scope | anchor | teaches | status "
        "| opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        "| S001 | src1 | tool | A | sc | an | t1 | mined | 2026-01-01 "
        "| on-release | r1 |\n"
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
    APPENDABLE_FIXTURE_PATH: "# r17 diag\noriginal\n",
    ".ufo/waves/round-1/run.json": '{"a": 1}\n',
    ".ufo/waves/round-17/predictions/SHA256SUMS": SUMS_FIXTURE,
    ".ufo/waves/round-17/predictions/carriers.tsv": CARRIERS_FIXTURE,
    ".ufo/waves/round-17/tools/compare.py": "# compare v1\n",
    "evidence/round-1/x.json": '{"e": 1}\n',
}


def fixture_after_clean():
    restored = (
        f"{hashlib.sha256(CARRIERS_FIXTURE.encode()).hexdigest()}"
        "  predictions/carriers.tsv"
    )
    return {
        "LOG.md": "# log\nline one\nline two appended\n",
        "SCORECARD.md": "# score\ncard one\ncard two appended\n",
        "SKILL.md": (
            "# skill\n\n## Queue-drain craft (test)\n\n"
            "- **rule one** see corpus/knowledge/k-one.md:1-2\n\n"
            "## Other\n\nnew line\n"
        ),
        "corpus/SOURCES.md": (
            "| id | source | kind | tier | scope | anchor | teaches | status "
            "| opened | recheck | used-by |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n"
            "| S001 | src1 | tool | A | sc | an | t1 | superseded "
            "| 2026-01-01 | on-release | r1, r2 |\n"
            "| S033 | src33 | tool | A | sc | an | t33 | opened "
            "| 2026-10-20 | next | r18 |\n"
        ),
        "corpus/QUALITY.md": (
            "# quality\n\n## Admission criteria\n\n"
            "| # | criterion | why | supersedes |\n|---|---|---|---|\n"
            "| 1 | first | l1 | — |\n"
            "| 2 | second | l2 | — |\n"
            "| 3 | third appended | l3 | — |\n\n"
            "## Signals of weak material\n\n| # | signal |\n|---|---|\n"
            "| 1 | weak |\n"
        ),
        "corpus/lessons/round-2.md": "# l2\n",
        APPENDABLE_FIXTURE_PATH: "# r17 diag\noriginal\nappended\n",
        ".ufo/waves/round-2/new.json": '{"b": 2}\n',
        ".ufo/waves/round-17/predictions/SHA256SUMS": SUMS_FIXTURE + restored
        + "\n",
        ".ufo/waves/round-17/tools/compare.py": "# compare v2 edited\n",
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


def _rmtree(root):
    for base, dirs, files in os.walk(root, topdown=False):
        for name in files:
            os.remove(os.path.join(base, name))
        for name in dirs:
            os.rmdir(os.path.join(base, name))
    os.rmdir(root)


def selftest():
    """Temporary fixture repo: one clean append case, six red mutations."""
    cases = 0
    failures = []

    def check(name, ok):
        nonlocal cases
        cases += 1
        if not ok:
            failures.append(name)

    root = Path(tempfile.mkdtemp(prefix="controls18-selftest-"))
    try:
        git(root, "init", "-q")
        before = _commit(root, FIXTURE_BEFORE, "before")

        clean = _commit(root, fixture_after_clean(), "clean append")
        report = build_report(root, before, clean)
        check(
            "clean:log prefix",
            report["old_prefix"]["LOG.md"]["prefix_preserved"],
        )
        check(
            "clean:scorecard prefix",
            report["old_prefix"]["SCORECARD.md"]["prefix_preserved"],
        )
        frozen = report["prior_wave_evidence_blobs"]
        check("clean:frozen all", frozen["unchanged"] == frozen["checked"])
        check(
            "clean:contracted compare.py",
            frozen["contracted_modifications"]
            [".ufo/waves/round-17/tools/compare.py"]["byte_identical"]
            is False,
        )
        check(
            "clean:sums restored",
            frozen["r17_sums_restored_line"]["restored_ok"] is True,
        )
        corpus = report["prior_corpus_text"]
        check(
            "clean:lessons all identical",
            corpus["corpus/lessons"]["violations"] == [],
        )
        knowledge = corpus["corpus/knowledge"]
        check(
            "clean:knowledge ok",
            knowledge["violations"] == [],
        )
        check(
            "clean:appendable knowledge",
            knowledge["files"][APPENDABLE_FIXTURE_PATH]["prefix_preserved"]
            and not knowledge["files"][APPENDABLE_FIXTURE_PATH][
                "byte_identical"
            ],
        )
        check(
            "clean:verifiers",
            all(
                row["unchanged"]
                for row in report["prior_verifiers_unchanged"].values()
            ),
        )
        quality = report["quality_admission_rows"]
        check("clean:quality rows", quality["prior_rows_byte_identical"])
        check("clean:quality 1-20", quality["rows_1_20_identical"])
        check("clean:quality added", quality["added_rows"] == ["3"])
        sources = report["sources_registry"]
        check("clean:sources", sources["immutable_cells_unchanged"])
        check(
            "clean:sources deltas",
            sources["allowed_deltas"]["S001"]["status"]["after"]
            == "superseded"
            and sources["allowed_deltas"]["S001"]["used-by"]["after"]
            == "r1, r2",
        )
        skill = report["skill_md_diff"]
        check(
            "clean:skill diff",
            skill["deleted_lines"] == ["stale line"]
            and skill["added_lines"] == ["new line"],
        )
        check(
            "clean:revisions",
            report["revisions"]["before"] == before
            and report["revisions"]["after"] == clean,
        )

        red_log = _commit(
            root, {"LOG.md": "# log\nline one REWRITTEN\n"}, "red: log"
        )
        report = build_report(root, clean, red_log)
        check(
            "red:log rewritten",
            report["old_prefix"]["LOG.md"]["prefix_preserved"] is False,
        )

        red_quality = _commit(
            root,
            {
                "corpus/QUALITY.md": FIXTURE_BEFORE["corpus/QUALITY.md"].replace(
                    "| 1 | first |", "| 1 | first EDITED |"
                )
            },
            "red: quality",
        )
        report = build_report(root, clean, red_quality)
        check(
            "red:quality detects",
            not report["quality_admission_rows"]["prior_rows_byte_identical"]
            and report["quality_admission_rows"]["violations"].get("1")
            == "row_text_changed",
        )
        check(
            "red:quality 1-20",
            report["quality_admission_rows"]["rows_1_20_identical"] is False,
        )

        red_sources = _commit(
            root,
            {
                "corpus/SOURCES.md": FIXTURE_BEFORE["corpus/SOURCES.md"].replace(
                    "| t1 |", "| TEACHES-TAMPERED |"
                )
            },
            "red: sources",
        )
        report = build_report(root, clean, red_sources)
        check(
            "red:sources immutable",
            report["sources_registry"]["immutable_violations"].get("S001")
            == [7],
        )

        red_knowledge = _commit(
            root,
            {"corpus/knowledge/k-one.md": "one\ntwo\ntampered\n"},
            "red: knowledge",
        )
        report = build_report(root, clean, red_knowledge)
        check(
            "red:knowledge tamper",
            "corpus/knowledge/k-one.md"
            in report["prior_corpus_text"]["corpus/knowledge"]["violations"],
        )

        red_sums = _commit(
            root,
            {
                ".ufo/waves/round-17/predictions/SHA256SUMS": (
                    SUMS_FIXTURE + "0" * 64 + "  predictions/carriers.tsv\n"
                )
            },
            "red: sums",
        )
        report = build_report(root, clean, red_sums)
        check(
            "red:sums wrong sha",
            report["prior_wave_evidence_blobs"]["r17_sums_restored_line"][
                "restored_ok"
            ]
            is False,
        )

        red_frozen = _commit(
            root,
            {".ufo/waves/round-1/run.json": '{"a": 999}\n'},
            "red: frozen",
        )
        report = build_report(root, clean, red_frozen)
        check(
            "red:frozen names",
            report["prior_wave_evidence_blobs"]["files"][
                ".ufo/waves/round-1/run.json"
            ]["unchanged"]
            is False,
        )
    finally:
        _rmtree(root)

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
