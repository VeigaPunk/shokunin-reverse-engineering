#!/usr/bin/env python3
"""Round 26 (R26-C1) counting instrument: native reader verb evidence-id identity.

Implements the `rules` block of the frozen claim R26-C1 in
`.ufo/waves/round-26/claims.json` (round 26, attempt 1, frozen by the kaidoku
L1 before any table REA run and before any repair edit).

Usage:
    python3 -I -B tools/round-26/c1-id-identity.py --root <LANE> --rev <REV>
    python3 -I -B tools/round-26/c1-id-identity.py --selftest

Reads only Git objects at REV (`git -C ROOT show REV:path`, `git ls-tree`).
Exit 0 iff rows_complete == 8 and entry_ok == 1, exit 1 otherwise, exit 2 on
usage error or unreadable input (bad --root / unresolvable --rev).

Standard library only; runs under `python3 -I -B`.
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

# --- frozen claim constants (claims.json R26-C1) -----------------------------
FROZEN_VERBS = (
    "analyze",
    "inspect",
    "decompile",
    "xrefs",
    "read-bytes",
    "function",
    "instructions",
    "inspect-binary-layout",
)
CARRIER_SHA256 = "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"
RUNS = ("base", "repeat", "copy")
RUN_PATH = {
    "base": "/usr/bin/jq",
    "repeat": "/usr/bin/jq",
    "copy": "/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq",
}
TABLE_PATH = "corpus/evidence/round-26/c1/table.tsv"
ENVELOPE_DIR = "corpus/evidence/round-26/c1/envelopes"
ENTRY_PATH = "corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md"
SOURCES_PATH = "corpus/SOURCES.md"
LESSON_PATH = "corpus/lessons/round-26.md"
OPENED_DATE = "2026-10-22"
TABLE_COLUMNS = ("verb", "verdict", "base_id", "repeat_id", "copy_id", "subject_sha256")


# --- git plumbing (read only) ------------------------------------------------
def _git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["LC_ALL"] = "C"
    return env


def git_bytes(root, *args):
    """Run git in ROOT and return (returncode, stdout bytes, stderr bytes)."""
    proc = subprocess.run(
        ["git", "-C", root, "--no-replace-objects", *args],
        capture_output=True,
        env=_git_env(),
    )
    return proc.returncode, proc.stdout, proc.stderr


def resolve_rev(root, rev):
    """Resolve a revision to a commit sha, or (None, error text)."""
    code, out, err = git_bytes(root, "rev-parse", "--verify", "%s^{commit}" % rev)
    if code != 0:
        return None, err.decode("utf-8", "replace").strip()
    return out.decode().strip(), ""


def read_blob(root, sha, path):
    """Return blob bytes at sha:path, or None when the path is absent."""
    code, out, _ = git_bytes(root, "show", "%s:%s" % (sha, path))
    if code != 0:
        return None
    return out


def list_tree(root, sha, directory):
    """Return the set of file paths under `directory` at sha."""
    code, out, _ = git_bytes(root, "ls-tree", "-r", "-z", "--name-only", sha, "--", directory)
    if code != 0:
        return set()
    return {p for p in out.decode("utf-8", "replace").split("\0") if p}


def dig(obj, path):
    """Walk a nested dict path; return (found, value)."""
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return False, None
        cur = cur[key]
    return True, cur


# --- helpers -----------------------------------------------------------------
def parse_table(text):
    """Parse the tab separated table. Returns (header, rows)."""
    header = None
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        cells = [c.strip() for c in line.split("\t")]
        if header is None:
            header = cells
            continue
        rows.append(cells)
    return header, rows


def envelope_subject_sha(obj):
    """First present of .data.subject.digest.sha256 then .data.normalized_result.artifact.sha256.

    Returns (value, source_path). The rule says "first present of", so a key that
    exists but holds null counts as present.
    """
    found, value = dig(obj, ("data", "subject", "digest", "sha256"))
    if found:
        return value, "data.subject.digest.sha256"
    found, value = dig(obj, ("data", "normalized_result", "artifact", "sha256"))
    if found:
        return value, "data.normalized_result.artifact.sha256"
    return None, None


def derive_verdict(ids):
    """claims.json R26-C1 derived_verdict over the three raw evidence ids.

    `ids` maps run -> the raw .data.evidence_id value (None when absent).
    """
    if any(not (isinstance(ids[r], str) and ids[r].startswith("ev_")) for r in RUNS):
        return "no-id"
    if ids["base"] != ids["repeat"]:
        return "unstable"
    if ids["copy"] == ids["base"]:
        return "content-keyed"
    return "path-sensitive"


def read_gate_section(text):
    """Text of the `## Gate` section of a lesson file (heading up to the next `## `)."""
    if text is None:
        return ""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.rstrip() == "## Gate":
            start = i
            break
    if start is None:
        return ""
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def parse_sources_rows(text):
    """Map S-id -> {status, opened, used_by} from a SOURCES.md registry table.

    Column layout (frozen by the registry header):
    | id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
    """
    rows = {}
    if text is None:
        return rows
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 11:
            continue
        sid = cells[1]
        if not re.fullmatch(r"S\d{3}", sid):
            continue
        rows[sid] = {
            "status": cells[8],
            "opened": cells[9],
            "used_by": cells[11] if len(cells) > 11 else "",
        }
    return rows


def id_cell_expected(value, found):
    """The table cell that must equal an envelope's .data.evidence_id value."""
    if not found or value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


# --- entry_ok ----------------------------------------------------------------
def evaluate_entry(root, sha):
    """The entry_ok rule of claims.json R26-C1."""
    entry_blob = read_blob(root, sha, ENTRY_PATH)
    sources_blob = read_blob(root, sha, SOURCES_PATH)
    lesson_blob = read_blob(root, sha, LESSON_PATH)

    result = {
        "path": ENTRY_PATH,
        "present": entry_blob is not None,
        "source_line": None,
        "names_table": False,
        "cited_ids": [],
        "rows_opened_today": [],
        "gate_ids": [],
        "qualifying_ids": [],
        "reasons": [],
    }
    if entry_blob is None:
        result["reasons"].append("entry_missing")
        return 0, result

    text = entry_blob.decode("utf-8", "replace")
    source_line = None
    for line in text.splitlines():
        if line.lstrip().startswith("source:"):
            source_line = line.strip()
            break
    result["source_line"] = source_line
    if source_line is None:
        result["reasons"].append("source_line_missing")
        return 0, result

    result["names_table"] = TABLE_PATH in source_line
    if not result["names_table"]:
        result["reasons"].append("source_line_does_not_name_table")

    cited = sorted(set(re.findall(r"S\d{3}", source_line)))
    result["cited_ids"] = cited

    rows = parse_sources_rows(sources_blob.decode("utf-8", "replace") if sources_blob else None)
    gate_text = read_gate_section(lesson_blob.decode("utf-8", "replace") if lesson_blob else None)
    gate_ids = sorted(set(re.findall(r"S\d{3}", gate_text)))
    result["gate_ids"] = gate_ids

    opened_today = []
    qualifying = []
    for sid in cited:
        row = rows.get(sid)
        if row is None:
            continue
        if row["opened"] == OPENED_DATE:
            opened_today.append(sid)
            if sid in gate_ids:
                qualifying.append(sid)
    result["rows_opened_today"] = opened_today
    result["qualifying_ids"] = qualifying
    if not qualifying:
        result["reasons"].append("no_cited_source_row_opened_today_and_named_in_lesson_gate")
    return (1 if result["names_table"] and qualifying else 0), result


# --- row measurement ---------------------------------------------------------
def evaluate_row(root, sha, tree_files, verb, candidates):
    """Measure one table row against the frozen row_complete rule."""
    entry = {
        "verb": verb,
        "complete": False,
        "reasons": [],
        "warnings": [],
        "table_row": None,
        "derived_verdict": None,
        "envelopes": {},
    }
    if len(candidates) > 1:
        entry["reasons"].append("duplicate_verb_row")
        return entry
    row = candidates[0]
    entry["table_row"] = row
    ids = {}
    for run in RUNS:
        env_path = None
        for suffix in (".json", ".json.gz"):
            candidate = "%s/%s-%s%s" % (ENVELOPE_DIR, verb, run, suffix)
            if candidate in tree_files:
                env_path = candidate
                break
        info = {"path": env_path, "present": env_path is not None}
        entry["envelopes"][run] = info
        if env_path is None:
            entry["reasons"].append("envelope_missing:%s" % run)
            ids[run] = None
            continue
        blob = read_blob(root, sha, env_path)
        if blob is None:
            entry["reasons"].append("envelope_unreadable:%s" % run)
            ids[run] = None
            continue
        info["bytes"] = len(blob)
        if env_path.endswith(".gz"):
            try:
                blob = gzip.decompress(blob)
            except Exception as exc:  # noqa: BLE001 - surfaced as a row reason
                entry["reasons"].append("envelope_gzip_error:%s:%s" % (run, exc))
                ids[run] = None
                continue
        text = blob.decode("utf-8", "replace")
        info["text_contains_path"] = RUN_PATH[run] in text
        try:
            obj = json.loads(text)
        except ValueError as exc:
            entry["reasons"].append("envelope_parse_error:%s:%s" % (run, exc))
            ids[run] = None
            continue
        if not isinstance(obj, dict):
            entry["reasons"].append("envelope_not_an_object:%s" % run)
            ids[run] = None
            continue
        info["ok"] = obj.get("ok")
        if obj.get("ok") is not True:
            entry["reasons"].append("envelope_ok_not_true:%s" % run)
        sha_value, sha_source = envelope_subject_sha(obj)
        info["subject_sha256"] = sha_value
        info["subject_sha256_source"] = sha_source
        if sha_value != CARRIER_SHA256:
            entry["reasons"].append("subject_sha256_mismatch:%s" % run)
        found, id_value = dig(obj, ("data", "evidence_id"))
        info["evidence_id"] = id_value if found else None
        ids[run] = id_value
        if not (isinstance(id_value, str) and id_value.startswith("ev_")):
            entry["warnings"].append("evidence_id_not_ev_prefixed:%s" % run)
        expected = id_cell_expected(id_value, found)
        cell = row.get("%s_id" % run, "")
        if cell != expected:
            entry["reasons"].append("id_cell_mismatch:%s" % run)
    derived = derive_verdict(ids)
    entry["derived_verdict"] = derived
    entry["envelope_ids"] = {r: ids[r] for r in RUNS}
    if row.get("verdict") != derived:
        entry["reasons"].append(
            "verdict_mismatch:%s:table=%s:derived=%s" % (verb, row.get("verdict"), derived)
        )
    table_subject = row.get("subject_sha256", "")
    entry["table_subject_sha256"] = table_subject
    if table_subject and table_subject != CARRIER_SHA256:
        entry["reasons"].append("table_subject_sha256_mismatch:%s:table=%s" % (verb, table_subject))
    return entry


def evaluate(root, sha):
    """Full R26-C1 measurement at revision sha. Returns the JSON-ready report."""
    tree_files = list_tree(root, sha, ENVELOPE_DIR)

    table_blob = read_blob(root, sha, TABLE_PATH)
    header = None
    data_rows = []
    table_present = table_blob is not None
    if table_present:
        header, data_rows = parse_table(table_blob.decode("utf-8", "replace"))

    col = {}
    header_ok = False
    if header is not None:
        for name in TABLE_COLUMNS:
            if name in header:
                col[name] = header.index(name)
        header_ok = all(name in col for name in TABLE_COLUMNS)

    by_verb = {}
    extra_rows = []
    for number, cells in enumerate(data_rows, start=2):
        if not header_ok:
            break
        verb = cells[col["verb"]] if col["verb"] < len(cells) else ""
        row = {name: (cells[col[name]] if col[name] < len(cells) else "") for name in TABLE_COLUMNS}
        row["_line"] = number
        if verb in FROZEN_VERBS:
            by_verb.setdefault(verb, []).append(row)
        else:
            extra_rows.append(row)

    rows = []
    rows_complete = 0
    path_text = {}
    table_reasons = []
    for verb in FROZEN_VERBS:
        if not table_present:
            entry = {
                "verb": verb,
                "complete": False,
                "reasons": ["table_missing"],
                "warnings": [],
                "table_row": None,
                "derived_verdict": None,
                "envelopes": {},
            }
        elif not header_ok:
            entry = {
                "verb": verb,
                "complete": False,
                "reasons": ["table_header_invalid"],
                "warnings": [],
                "table_row": None,
                "derived_verdict": None,
                "envelopes": {},
            }
        elif verb not in by_verb:
            entry = {
                "verb": verb,
                "complete": False,
                "reasons": ["row_missing"],
                "warnings": [],
                "table_row": None,
                "derived_verdict": None,
                "envelopes": {},
            }
        else:
            entry = evaluate_row(root, sha, tree_files, verb, by_verb[verb])
            for run, info in entry["envelopes"].items():
                if "text_contains_path" in info:
                    path_text.setdefault(verb, {})[run] = {
                        "path": RUN_PATH[run],
                        "text_contains_path": info["text_contains_path"],
                    }
        entry["complete"] = not entry["reasons"]
        if entry["complete"]:
            rows_complete += 1
        rows.append(entry)

    # A table row whose verb is not one of the 8 frozen verbs is not a row of this
    # claim: row_complete requires "the verb is one of the 8 frozen verbs", and
    # the claim's own statement is that the table "has one row for each of the 8
    # frozen verbs". rows_total is the constant 8 (held even where the table is
    # absent), so a surplus row is a table-shape defect: it is reported and it
    # caps rows_complete, keeping the frozen exit rule (rows_complete == 8 and
    # entry_ok == 1) as the only gate. Disclosed in the seat report.
    if extra_rows:
        table_reasons.append("unknown_verb_row:%s" % ",".join(r.get("verb", "") for r in extra_rows))
        rows_complete = max(0, min(rows_complete, 8 - len(extra_rows)))

    entry_ok, entry_detail = evaluate_entry(root, sha)

    report = {
        "instrument": "tools/round-26/c1-id-identity.py",
        "claim": "R26-C1",
        "rev": sha,
        "carrier_sha256": CARRIER_SHA256,
        "rows_total": 8,
        "rows_complete": rows_complete,
        "rows": rows,
        "table": {
            "path": TABLE_PATH,
            "present": table_present,
            "data_rows": len(data_rows),
            "header": header,
            "header_ok": header_ok,
            "extra_rows": extra_rows,
            "reasons": table_reasons,
        },
        "entry_ok": entry_ok,
        "entry": entry_detail,
        "diagnostics_not_gating": {
            "description": "whether each envelope's text contains the path it was run on",
            "envelope_path_text": path_text,
            "tree_path_text": tree_path_diagnostics(root, sha, tree_files),
        },
        "exit": 0 if (rows_complete == 8 and entry_ok == 1) else 1,
    }
    return report


# --- selftest ----------------------------------------------------------------
def _fixture_envelope(evidence_id, path, sha_value=None, ok=True, sha_source="subject"):
    if sha_value is None:
        sha_value = CARRIER_SHA256
    data = {
        "evidence_id": evidence_id,
        "subject": {"name": "jq", "local_path": path, "format": "elf"},
        "provider": {"id": "rea-workflow", "name": "REA composed investigation workflow", "version": "1"},
    }
    if sha_source == "subject":
        data["subject"]["digest"] = {"sha256": sha_value}
    else:
        data["normalized_result"] = {"artifact": {"sha256": sha_value}}
    return json.dumps({"ok": ok, "data": data, "meta": {"fixture": True}}, indent=1) + "\n"


def _fixture_id(verb, run):
    return "ev_" + hashlib.sha256(("%s:%s" % (verb, run)).encode()).hexdigest()


# verb -> (verdict, repeat_differs, copy_differs)
_FIXTURE_PLAN = {
    "analyze": ("content-keyed", False, False),
    "inspect": ("content-keyed", False, False),
    "decompile": ("unstable", True, False),
    "xrefs": ("content-keyed", False, False),
    "read-bytes": ("content-keyed", False, False),
    "function": ("path-sensitive", False, True),
    "instructions": ("content-keyed", False, False),
    "inspect-binary-layout": ("path-sensitive", False, True),
}


def _fixture_tree():
    """Return {relpath: bytes} for a fully green synthetic repository."""
    files = {}
    table = ["\t".join(TABLE_COLUMNS)]
    for verb in FROZEN_VERBS:
        verdict, repeat_differs, copy_differs = _FIXTURE_PLAN[verb]
        base = _fixture_id(verb, "base")
        repeat = _fixture_id(verb, "repeat") if repeat_differs else base
        copy = _fixture_id(verb, "copy") if copy_differs else base
        for run, value in (("base", base), ("repeat", repeat), ("copy", copy)):
            sha_source = "normalized" if (verb == "instructions" and run == "copy") else "subject"
            files["%s/%s-%s.json" % (ENVELOPE_DIR, verb, run)] = _fixture_envelope(
                value, RUN_PATH[run], sha_source=sha_source
            ).encode()
        table.append("\t".join([verb, verdict, base, repeat, copy, CARRIER_SHA256]))
    files[TABLE_PATH] = ("\n".join(table) + "\n").encode()

    files[SOURCES_PATH] = (
        "# SOURCES — where kaidoku learns\n\n"
        "## Registry\n\n"
        "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        "| S900 | fixture source A | docs | A | fixture scope | anchor | teaches | mined | 2026-10-22 | on-release | corpus/lessons/round-26.md |\n"
        "| S901 | fixture source B | docs | A | fixture scope | anchor | teaches | mined | 2026-10-19 | on-release | corpus/lessons/round-25.md |\n"
    ).encode()

    files[LESSON_PATH] = (
        "# Round 26 — fixture lesson\n\n"
        "## Gate\n\n"
        "| Item | Decision | Located source quotation and limit |\n"
        "|---|---|---|\n"
        "| S900 | Admit, fixture | fixture text: “quoted fixture passage”. It supports the fixture scope only. |\n"
        "\n"
        "## Mistakes\n\n"
        "None recorded.\n"
    ).encode()

    files[ENTRY_PATH] = (
        "# Fixture entry\n\n"
        "source: S900 fixture source A; %s\n"
        "verified-at: 2026-10-22, round 26 fixture\n"
        "recheck: python3 -I -B tools/round-26/c1-id-identity.py --root <LANE> --rev <REV>\n"
        "\n"
        "Fixture body naming the table %s.\n" % (TABLE_PATH, TABLE_PATH)
    ).encode()
    return files


def _mutate(files, kind):
    """Return a mutated copy of the green fixture tree."""
    out = dict(files)
    if kind == "missing_envelope":
        out.pop("%s/analyze-copy.json" % ENVELOPE_DIR)
    elif kind == "envelope_ok_false":
        path = "%s/analyze-base.json" % ENVELOPE_DIR
        obj = json.loads(out[path].decode())
        obj["ok"] = False
        out[path] = (json.dumps(obj, indent=1) + "\n").encode()
    elif kind == "wrong_subject_sha256":
        path = "%s/analyze-base.json" % ENVELOPE_DIR
        obj = json.loads(out[path].decode())
        obj["data"]["subject"]["digest"]["sha256"] = "0" * 64
        out[path] = (json.dumps(obj, indent=1) + "\n").encode()
    elif kind == "id_cell_mismatch":
        text = out[TABLE_PATH].decode().splitlines()
        cells = text[1].split("\t")
        cells[2] = "ev_" + "1" * 62
        text[1] = "\t".join(cells)
        out[TABLE_PATH] = ("\n".join(text) + "\n").encode()
    elif kind == "wrong_verdict":
        text = out[TABLE_PATH].decode().splitlines()
        cells = text[1].split("\t")
        cells[1] = "path-sensitive"
        text[1] = "\t".join(cells)
        out[TABLE_PATH] = ("\n".join(text) + "\n").encode()
    elif kind == "unknown_verb":
        text = out[TABLE_PATH].decode().splitlines()
        cells = text[4].split("\t")
        cells[0] = "frobnicate"
        text[4] = "\t".join(cells)
        out[TABLE_PATH] = ("\n".join(text) + "\n").encode()
    elif kind == "duplicate_verb_row":
        text = out[TABLE_PATH].decode().splitlines()
        out[TABLE_PATH] = ("\n".join(text + [text[2]]) + "\n").encode()
    elif kind == "table_subject_sha256_mismatch":
        text = out[TABLE_PATH].decode().splitlines()
        cells = text[1].split("\t")
        cells[5] = "0" * 64
        text[1] = "\t".join(cells)
        out[TABLE_PATH] = ("\n".join(text) + "\n").encode()
    elif kind == "no_id_verdict":
        # One envelope carries no .data.evidence_id: the derived verdict is then
        # "no-id" and the table row must say so with empty id cells.
        path = "%s/xrefs-base.json" % ENVELOPE_DIR
        obj = json.loads(out[path].decode())
        del obj["data"]["evidence_id"]
        out[path] = (json.dumps(obj, indent=1) + "\n").encode()
        text = out[TABLE_PATH].decode().splitlines()
        for i, line in enumerate(text):
            if line.startswith("xrefs\t"):
                cells = line.split("\t")
                cells[1] = "no-id"
                cells[2] = ""
                text[i] = "\t".join(cells)
                break
        out[TABLE_PATH] = ("\n".join(text) + "\n").encode()
    elif kind == "gzip_envelopes":
        for key in list(out):
            if key.startswith(ENVELOPE_DIR + "/") and key.endswith(".json"):
                out[key + ".gz"] = gzip.compress(out[key], mtime=0)
                del out[key]
    elif kind == "entry_missing":
        out.pop(ENTRY_PATH)
    elif kind == "entry_source_without_table":
        lines = out[ENTRY_PATH].decode().splitlines()
        for i, line in enumerate(lines):
            if line.lstrip().startswith("source:"):
                lines[i] = line.replace(TABLE_PATH, "corpus/evidence/round-26/c1/row-summary.tsv")
                break
        out[ENTRY_PATH] = ("\n".join(lines) + "\n").encode()
    elif kind == "sources_row_other_date":
        out[SOURCES_PATH] = out[SOURCES_PATH].decode().replace(
            "| mined | 2026-10-22 |", "| mined | 2026-10-19 |"
        ).encode()
    elif kind == "gate_omits_id":
        out[LESSON_PATH] = out[LESSON_PATH].decode().replace("S900", "S901").encode()
    else:
        raise ValueError("unknown mutation %r" % kind)
    return out


def _git_run(cwd, *args):
    env = _git_env()
    env.update(
        {
            "GIT_AUTHOR_NAME": "c1 selftest",
            "GIT_AUTHOR_EMAIL": "selftest@localhost",
            "GIT_COMMITTER_NAME": "c1 selftest",
            "GIT_COMMITTER_EMAIL": "selftest@localhost",
        }
    )
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, env=env)


def _materialize(tree, workdir):
    for rel, data in tree.items():
        full = os.path.join(workdir, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as handle:
            handle.write(data)
    _git_run(workdir, "init", "-q")
    _git_run(workdir, "add", "-A")
    res = _git_run(workdir, "commit", "-q", "-m", "fixture")
    if res.returncode != 0:
        raise RuntimeError("fixture commit failed: %s" % res.stderr.decode("utf-8", "replace"))


def _run_cli(root, rev):
    proc = subprocess.run(
        [sys.executable, "-I", "-B", os.path.abspath(__file__), "--root", root, "--rev", rev],
        capture_output=True,
    )
    payload = None
    try:
        payload = json.loads(proc.stdout.decode("utf-8", "replace"))
    except ValueError:
        payload = None
    return proc.returncode, payload


def selftest():
    """Show that each frozen rule can fail, plus one fully green fixture."""
    cases = [
        ("green", None, {"rows_complete": 8, "entry_ok": 1, "exit": 0}),
        ("missing_envelope", "missing_envelope", {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("envelope_ok_false", "envelope_ok_false", {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("wrong_subject_sha256", "wrong_subject_sha256", {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("id_cell_mismatch", "id_cell_mismatch", {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("wrong_verdict", "wrong_verdict", {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("unknown_verb", "unknown_verb", {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("duplicate_verb_row", "duplicate_verb_row", {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("table_subject_sha256_mismatch", "table_subject_sha256_mismatch",
         {"rows_complete": 7, "entry_ok": 1, "exit": 1}),
        ("gzip_envelopes", "gzip_envelopes", {"rows_complete": 8, "entry_ok": 1, "exit": 0}),
        ("no_id_verdict", "no_id_verdict", {"rows_complete": 8, "entry_ok": 1, "exit": 0}),
        ("entry_missing", "entry_missing", {"rows_complete": 8, "entry_ok": 0, "exit": 1}),
        ("entry_source_without_table", "entry_source_without_table",
         {"rows_complete": 8, "entry_ok": 0, "exit": 1}),
        ("sources_row_other_date", "sources_row_other_date", {"rows_complete": 8, "entry_ok": 0, "exit": 1}),
        ("gate_omits_id", "gate_omits_id", {"rows_complete": 8, "entry_ok": 0, "exit": 1}),
    ]
    green = _fixture_tree()
    results = []
    failures = 0
    with tempfile.TemporaryDirectory(prefix="c1-selftest-") as tmp:
        for name, mutation, expect in cases:
            tree = green if mutation is None else _mutate(green, mutation)
            workdir = os.path.join(tmp, name)
            os.makedirs(workdir)
            _materialize(tree, workdir)
            code, payload = _run_cli(workdir, "HEAD")
            observed = {
                "rows_complete": payload["rows_complete"] if payload else None,
                "entry_ok": payload["entry_ok"] if payload else None,
                "exit": code,
            }
            ok = observed == expect
            if not ok:
                failures += 1
            reasons = []
            if payload:
                for row in payload["rows"]:
                    if row["reasons"]:
                        reasons.append("%s: %s" % (row["verb"], "; ".join(row["reasons"])))
                for reason in payload["entry"]["reasons"]:
                    reasons.append("entry: %s" % reason)
            results.append(
                {
                    "case": name,
                    "mutation": mutation or "none",
                    "expected": expect,
                    "observed": observed,
                    "pass": ok,
                    "first_reasons": reasons[:2],
                }
            )
            print(
                "%-30s exit=%s rows_complete=%s entry_ok=%s expected=%s -> %s"
                % (
                    name,
                    observed["exit"],
                    observed["rows_complete"],
                    observed["entry_ok"],
                    expect,
                    "PASS" if ok else "FAIL",
                )
            )
            for reason in reasons[:2]:
                print("    reason: %s" % reason)
        proc = subprocess.run(
            [sys.executable, "-I", "-B", os.path.abspath(__file__), "--root", tmp],
            capture_output=True,
        )
        usage_ok = proc.returncode == 2
        if not usage_ok:
            failures += 1
        results.append(
            {
                "case": "usage_error_missing_rev",
                "mutation": "none",
                "expected": {"exit": 2},
                "observed": {"exit": proc.returncode},
                "pass": usage_ok,
                "first_reasons": [],
            }
        )
        print("%-30s exit=%s expected=2 -> %s" % ("usage_error_missing_rev", proc.returncode,
                                                  "PASS" if usage_ok else "FAIL"))

    summary = {
        "selftest": "R26-C1 c1-id-identity.py",
        "cases": len(results),
        "failures": failures,
        "results": results,
    }
    print(json.dumps(summary, indent=1))
    return 0 if failures == 0 else 1


# --- mutant fixture harness --------------------------------------------------
def run_mutants(args):
    """Measure each mutant revision and compare entry_ok with the expectation file.

    The expectation file is the mutation seat's final_table.json (list of rows
    with `mutant`, `rev` and `expected_r26_entry_ok`, e.g. "entry_ok=0 CAUGHT").
    """
    if not args.root or not os.path.isdir(args.root):
        print(json.dumps({"error": "root_not_a_directory", "root": args.root}), file=sys.stderr)
        return 2
    try:
        with open(args.mutants, "r", encoding="utf-8") as handle:
            table = json.load(handle)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": "mutants_unreadable", "path": args.mutants, "detail": str(exc)}),
              file=sys.stderr)
        return 2
    rows = []
    failures = 0
    for entry in table:
        name = entry.get("mutant")
        rev = entry.get("rev")
        expect_text = entry.get("expected_r26_entry_ok") or ""
        if not rev or "entry_ok=" not in expect_text:
            continue
        expect = int(expect_text.split("entry_ok=")[1].split()[0])
        sha, err = resolve_rev(args.root, rev)
        if sha is None:
            rows.append({"mutant": name, "rev": rev, "expected_entry_ok": expect,
                         "observed_entry_ok": None, "pass": False, "error": err})
            failures += 1
            continue
        report = evaluate(args.root, sha)
        observed = report["entry_ok"]
        ok = observed == expect
        if not ok:
            failures += 1
        rows.append({
            "mutant": name,
            "rev": rev,
            "mutation": entry.get("mutation"),
            "expected_entry_ok": expect,
            "observed_entry_ok": observed,
            "rows_complete": report["rows_complete"],
            "pass": ok,
            "entry_reasons": report["entry"]["reasons"],
        })
        print("%-8s rev=%s expected entry_ok=%s observed=%s -> %s"
              % (name, rev[:12], expect, observed, "PASS" if ok else "FAIL"))
    summary = {"mutant_harness": args.mutants, "root": args.root, "cases": len(rows),
               "failures": failures, "results": rows}
    print(json.dumps(summary, indent=1))
    return 0 if failures == 0 else 1


def tree_path_diagnostics(root, sha, tree_files):
    """Non-gating diagnostic: for every envelope in the tree, does its text name the path it was run on?

    The path is derived from the run token in the file name (`<verb>-<run>.json`),
    falling back to "does the text mention either known path" for other names.
    """
    out = {}
    for path in sorted(tree_files):
        name = path[len(ENVELOPE_DIR) + 1:] if path.startswith(ENVELOPE_DIR + "/") else path
        run = None
        for candidate in RUNS:
            for suffix in (".json", ".json.gz"):
                if name.endswith("-%s%s" % (candidate, suffix)):
                    run = candidate
                    break
            if run:
                break
        blob = read_blob(root, sha, path)
        if blob is None:
            continue
        if path.endswith(".gz"):
            try:
                blob = gzip.decompress(blob)
            except Exception:  # noqa: BLE001 - diagnostic only
                continue
        text = blob.decode("utf-8", "replace")
        if run:
            expected = RUN_PATH[run]
            out[path] = {
                "run": run,
                "expected_path": expected,
                "text_contains_path": expected in text,
            }
        else:
            out[path] = {
                "run": None,
                "expected_path": None,
                "text_contains_path": any(p in text for p in RUN_PATH.values()),
                "text_contains_any_known_path": any(p in text for p in RUN_PATH.values()),
            }
    return out


# --- CLI ---------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Round 26 R26-C1 evidence-id identity counting instrument."
    )
    parser.add_argument("--root", help="lane repository root (read only)")
    parser.add_argument("--rev", help="revision to measure")
    parser.add_argument("--selftest", action="store_true", help="run the built-in synthetic selftest")
    parser.add_argument(
        "--mutants",
        metavar="FILE",
        help="optional mutant expectation file (JSON list of {mutant, rev, expected_entry_ok}); "
        "each rev is measured in --root and its entry_ok compared",
    )
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.mutants:
        return run_mutants(args)
    if not args.root or not args.rev:
        parser.error("--root and --rev are required (or use --selftest)")
    if not os.path.isdir(args.root):
        print(json.dumps({"error": "root_not_a_directory", "root": args.root}), file=sys.stderr)
        return 2
    sha, err = resolve_rev(args.root, args.rev)
    if sha is None:
        print(
            json.dumps({"error": "unresolvable_rev", "rev": args.rev, "git": err}),
            file=sys.stderr,
        )
        return 2
    report = evaluate(args.root, sha)
    print(json.dumps(report, indent=1))
    return report["exit"]


if __name__ == "__main__":
    sys.exit(main())
