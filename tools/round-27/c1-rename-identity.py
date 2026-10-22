#!/usr/bin/env python3
"""R27-C1 counter: renamed-copy and second-carrier evidence-ID identity at rea-agents 6.5.0.

Committed before any R27-C1 table run. Reads Git objects at REV only (never the
working tree) and counts complete table rows (16 = 8 verbs x 2 carriers) plus
entry_ok. Gates added after the round-26 spot-check (routed defects 2-4, lesson M26-5):

  * each envelope's sha256 equals runs.tsv envelope_sha256, and all 48 differ;
  * .meta.command equals the verb; the argv equals the frozen template;
  * the envelope bytes contain the run's own path and not the row's other path;
    .data.subject.name (when present) equals the basename of that path;
  * runs.tsv records the resolved package version and package.json sha256 per call;
  * each .data.evidence_id recomputes under the 6.5.0 rule (tools/round-26/recompute-ids.py
    at REV, an independent standard-library reimplementation);
  * each run started, and each envelope file was first committed, no earlier than the
    commit that added this counter.

Usage:
  c1-rename-identity.py --root LANE --rev REV [--base BASE]
  c1-rename-identity.py --selftest
Exit 0 when rows_complete == 16 and entry_ok == 1; 1 otherwise; 2 on input error.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

COUNTER_PATH = "tools/round-27/c1-rename-identity.py"
RECOMPUTE_PATH = "tools/round-26/recompute-ids.py"
EVDIR = "corpus/evidence/round-27/c1"
ENTRY = "corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md"
LESSON = "corpus/lessons/round-27.md"
SOURCES = "corpus/SOURCES.md"
BASE = "cd32264f7ee356a9c0f48bd8e3fcdac222db22a0"
OPENED = "2026-10-22"
RENAMED_DIR = "/fast/scratch/hyaku/kaidoku-r27/carrier/renamed"
CARRIERS = {
    "jq": {
        "sha256": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806",
        "base": "/usr/bin/jq",
        "renamed": RENAMED_DIR + "/jq-r27-renamed.dat",
        "addr": "0x103fa0",
    },
    "tinyxxd": {
        "sha256": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65",
        "base": "/usr/bin/tinyxxd",
        "renamed": RENAMED_DIR + "/tinyxxd-r27-renamed.dat",
        "addr": "0x103d40",
    },
}
VERBS = {
    "analyze": "analyze <PATH> --format json --full-output",
    "inspect": "inspect <PATH> --format json --full-output",
    "decompile": "decompile <PATH> <ADDR> --format json --full-output",
    "xrefs": "xrefs <PATH> <ADDR> --format json --full-output",
    "read-bytes": "read-bytes <PATH> <ADDR> --length 64 --format json --full-output",
    "function": "function <PATH> <ADDR> --format json --full-output",
    "instructions": "instructions <PATH> <ADDR> --format json --full-output",
    "inspect-binary-layout": "inspect-binary-layout <PATH> --format json --full-output",
}
RUNS = ("base", "repeat", "renamed")
PKG_VERSION = "6.5.0"
PKG_JSON_SHA256 = "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c"
RUNS_HEADER = [
    "seat", "carrier", "verb", "run", "path", "argv", "exit", "utc_start", "utc_end",
    "envelope_sha256", "evidence_id", "subject_sha256", "pkg_version", "pkg_json_sha256",
]
TABLE_HEADER = ["carrier", "verb", "verdict", "base_id", "repeat_id", "renamed_id", "subject_sha256"]
ROWS_TOTAL = len(CARRIERS) * len(VERBS)


class InputError(Exception):
    pass


def git(root, *args, binary=False, check=True):
    proc = subprocess.run(["git", "-C", root, *args], capture_output=True)
    if check and proc.returncode != 0:
        raise InputError("git %s failed: %s" % (" ".join(args), proc.stderr.decode(errors="replace").strip()))
    return proc.stdout if binary else proc.stdout.decode()


def show(root, rev, path):
    proc = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)], capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def first_commit_time(root, rev, path):
    out = git(root, "log", "--diff-filter=A", "--format=%ct", rev, "--", path).split()
    return int(out[-1]) if out else None


def parse_utc(text):
    try:
        return int(dt.datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).timestamp())
    except ValueError:
        return None


def load_recompute(root, rev):
    raw = show(root, rev, RECOMPUTE_PATH)
    if raw is None:
        raise InputError("%s absent at %s" % (RECOMPUTE_PATH, rev))
    tmp = tempfile.mkdtemp(prefix="r27c1-")
    path = os.path.join(tmp, "recompute_ids.py")
    with open(path, "wb") as handle:
        handle.write(raw)
    spec = importlib.util.spec_from_file_location("recompute_ids", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    shutil.rmtree(tmp, ignore_errors=True)
    return module


def read_tsv(raw, header, name):
    if raw is None:
        return None
    lines = [line for line in raw.decode("utf-8").split("\n") if line != ""]
    if not lines or lines[0].split("\t") != header:
        raise InputError("%s header differs from frozen header" % name)
    rows = []
    for number, line in enumerate(lines[1:], start=2):
        cells = line.split("\t")
        if len(cells) != len(header):
            raise InputError("%s line %d has %d cells, want %d" % (name, number, len(cells), len(header)))
        rows.append(dict(zip(header, cells)))
    return rows


def argv_for(carrier, verb, path):
    return VERBS[verb].replace("<PATH>", path).replace("<ADDR>", CARRIERS[carrier]["addr"])


def section(text, heading):
    out, inside = [], False
    for line in text.split("\n"):
        if line.startswith("## "):
            if inside:
                break
            inside = line.strip() == heading
            continue
        if inside:
            out.append(line)
    return out


def sources_rows(text):
    rows = {}
    for line in text.split("\n"):
        match = re.match(r"^\| (S\d{3}) \|", line)
        if match:
            rows[match.group(1)] = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return rows


def check_entry(root, rev, base):
    reasons = []
    entry = show(root, rev, ENTRY)
    if entry is None:
        return 0, ["entry absent"]
    source_lines = [l for l in entry.decode("utf-8").split("\n") if l.startswith("source:")]
    if not source_lines:
        return 0, ["entry has no source: line"]
    source_line = source_lines[0]
    if EVDIR + "/table.tsv" not in source_line:
        reasons.append("source: line does not name %s/table.tsv" % EVDIR)
    raw_sources = show(root, rev, SOURCES)
    raw_base_sources = show(root, base, SOURCES)
    raw_lesson = show(root, rev, LESSON)
    if raw_sources is None or raw_lesson is None:
        return 0, reasons + ["SOURCES.md or round-27 lesson absent"]
    rows = sources_rows(raw_sources.decode("utf-8"))
    base_rows = sources_rows(raw_base_sources.decode("utf-8")) if raw_base_sources else {}
    gate_ids = set()
    for line in section(raw_lesson.decode("utf-8"), "## Gate"):
        match = re.match(r"^\| (S\d{3}) \|", line)
        if match:
            gate_ids.add(match.group(1))
    good = []
    for sid in sorted(set(re.findall(r"\bS\d{3}\b", source_line))):
        row = rows.get(sid)
        if row is None or len(row) < 11:
            continue
        if sid in base_rows:
            continue
        if row[7] != "mined" or row[8] != OPENED or sid not in gate_ids:
            continue
        good.append(sid)
    if not good:
        reasons.append("source: line names no S### that is new since base, mined, opened %s and in ## Gate" % OPENED)
    return (0 if reasons else 1), reasons + (["sourced by " + ",".join(good)] if good else [])


def count(root, rev, base):
    recompute = load_recompute(root, rev)
    counter_time = first_commit_time(root, rev, COUNTER_PATH)
    if counter_time is None:
        # Not committed at REV (for example the round base): no run can follow it.
        counter_time = float("inf")
    runs = read_tsv(show(root, rev, EVDIR + "/runs.tsv"), RUNS_HEADER, "runs.tsv")
    table = read_tsv(show(root, rev, EVDIR + "/table.tsv"), TABLE_HEADER, "table.tsv")
    report = {}
    if runs is None or table is None:
        for carrier in CARRIERS:
            for verb in VERBS:
                report[(carrier, verb)] = ["runs.tsv or table.tsv absent"]
        entry_ok, entry_reasons = check_entry(root, rev, base)
        return report, entry_ok, entry_reasons
    sha_count = {}
    for run in runs:
        sha_count[run["envelope_sha256"]] = sha_count.get(run["envelope_sha256"], 0) + 1
    for carrier, frozen in CARRIERS.items():
        for verb in VERBS:
            reasons = []
            trows = [t for t in table if t["carrier"] == carrier and t["verb"] == verb]
            if len(trows) != 1:
                reasons.append("table has %d rows" % len(trows))
            ids = {}
            for run_name in RUNS:
                tag = run_name
                path = frozen["base"] if run_name in ("base", "repeat") else frozen["renamed"]
                other = frozen["renamed"] if run_name in ("base", "repeat") else frozen["base"]
                rrows = [r for r in runs if r["carrier"] == carrier and r["verb"] == verb and r["run"] == run_name]
                if len(rrows) != 1:
                    reasons.append("%s: runs.tsv has %d lines" % (tag, len(rrows)))
                    continue
                r = rrows[0]
                if r["path"] != path:
                    reasons.append("%s: path %s, frozen %s" % (tag, r["path"], path))
                if r["argv"] != argv_for(carrier, verb, path):
                    reasons.append("%s: argv differs from frozen template" % tag)
                if r["exit"] != "0":
                    reasons.append("%s: exit %s" % (tag, r["exit"]))
                start = parse_utc(r["utc_start"])
                if start is None or start < counter_time:
                    reasons.append("%s: utc_start %s not after counter commit" % (tag, r["utc_start"]))
                if r["pkg_version"] != PKG_VERSION or r["pkg_json_sha256"] != PKG_JSON_SHA256:
                    reasons.append("%s: package %s/%s not the frozen 6.5.0" % (tag, r["pkg_version"], r["pkg_json_sha256"][:12]))
                if sha_count.get(r["envelope_sha256"], 0) != 1:
                    reasons.append("%s: envelope_sha256 shared with another run" % tag)
                env_path = "%s/envelopes/%s-%s-%s.json" % (EVDIR, carrier, verb, run_name)
                raw = show(root, rev, env_path)
                if raw is None:
                    reasons.append("%s: %s absent" % (tag, env_path))
                    continue
                added = first_commit_time(root, rev, env_path)
                if added is None or added < counter_time:
                    reasons.append("%s: envelope first committed before the counter" % tag)
                if hashlib.sha256(raw).hexdigest() != r["envelope_sha256"]:
                    reasons.append("%s: envelope sha256 differs from runs.tsv" % tag)
                try:
                    env = json.loads(raw.decode("utf-8"))
                except (ValueError, RecursionError):
                    reasons.append("%s: envelope does not parse" % tag)
                    continue
                if not isinstance(env, dict) or env.get("ok") is not True or not isinstance(env.get("data"), dict):
                    reasons.append("%s: not an ok envelope" % tag)
                    continue
                data = env["data"]
                meta = env.get("meta") if isinstance(env.get("meta"), dict) else {}
                if meta.get("command") != verb:
                    reasons.append("%s: meta.command %r" % (tag, meta.get("command")))
                eid = data.get("evidence_id")
                if not isinstance(eid, str) or not eid.startswith("ev_"):
                    reasons.append("%s: no evidence_id" % tag)
                    continue
                if eid != r["evidence_id"]:
                    reasons.append("%s: evidence_id differs from runs.tsv" % tag)
                try:
                    if recompute.compute_evidence_id(data) != eid:
                        reasons.append("%s: evidence_id does not recompute under the 6.5.0 rule" % tag)
                except Exception as error:  # noqa: BLE001 - any recompute failure fails the row
                    reasons.append("%s: recompute failed: %s" % (tag, type(error).__name__))
                subject = data.get("subject") if isinstance(data.get("subject"), dict) else {}
                digest = subject.get("digest") if isinstance(subject.get("digest"), dict) else {}
                sha = digest.get("sha256")
                if sha is None:
                    artifact = (data.get("normalized_result") or {}).get("artifact") if isinstance(data.get("normalized_result"), dict) else None
                    sha = artifact.get("sha256") if isinstance(artifact, dict) else None
                if sha != frozen["sha256"] or r["subject_sha256"] != frozen["sha256"]:
                    reasons.append("%s: subject sha256 not the carrier" % tag)
                text = raw.decode("utf-8")
                if path not in text:
                    reasons.append("%s: envelope does not contain its run path" % tag)
                if other in text:
                    reasons.append("%s: envelope contains the row's other path" % tag)
                if "name" in subject and subject["name"] != os.path.basename(path):
                    reasons.append("%s: subject.name %r is not the run file name" % (tag, subject["name"]))
                ids[run_name] = eid
            if len(ids) == 3:
                if ids["base"] != ids["repeat"]:
                    verdict = "unstable"
                elif ids["renamed"] == ids["base"]:
                    verdict = "content-keyed"
                else:
                    verdict = "rename-sensitive"
                if len(trows) == 1:
                    t = trows[0]
                    if (t["base_id"], t["repeat_id"], t["renamed_id"]) != (ids["base"], ids["repeat"], ids["renamed"]):
                        reasons.append("table id cells differ from envelopes")
                    if t["verdict"] != verdict:
                        reasons.append("table verdict %s, derived %s" % (t["verdict"], verdict))
                    if t["subject_sha256"] != frozen["sha256"]:
                        reasons.append("table subject_sha256 is not the carrier")
            report[(carrier, verb)] = reasons
    entry_ok, entry_reasons = check_entry(root, rev, base)
    return report, entry_ok, entry_reasons


def run_count(root, rev, base, out=sys.stdout):
    report, entry_ok, entry_reasons = count(root, rev, base)
    complete = 0
    for (carrier, verb), reasons in sorted(report.items()):
        if reasons:
            print("INCOMPLETE %s %s: %s" % (carrier, verb, "; ".join(reasons)), file=out)
        else:
            complete += 1
            print("COMPLETE %s %s" % (carrier, verb), file=out)
    print("entry: %s" % "; ".join(entry_reasons or ["ok"]), file=out)
    print("rows_complete=%d/%d entry_ok=%d rev=%s" % (complete, ROWS_TOTAL, entry_ok, rev), file=out)
    return 0 if complete == ROWS_TOTAL and entry_ok == 1 else 1


# ------------------------------------------------------------------ selftest


def _commit(repo, when, message):
    env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when,
               GIT_AUTHOR_NAME="selftest", GIT_AUTHOR_EMAIL="selftest@invalid",
               GIT_COMMITTER_NAME="selftest", GIT_COMMITTER_EMAIL="selftest@invalid")
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", message], check=True, env=env, capture_output=True)
    return git(repo, "rev-parse", "HEAD").strip()


def _write(repo, rel, content):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(content if isinstance(content, bytes) else content.encode("utf-8"))


def _envelope(recompute, carrier, verb, run_name, path, sensitive):
    data = {
        "subject": {"name": os.path.basename(path), "digest": {"sha256": CARRIERS[carrier]["sha256"]},
                    "local_path": path, "format": "elf", "architecture": "x86_64"},
        "provider": {"id": "ghidra"}, "analysis_profile": {"p": 1}, "predicate_type": "t",
        "operation": verb, "parameters": {"target": path} if sensitive else {"x": 1},
        "raw_result": {"run": "%s-%s" % (carrier, verb)}, "normalized_result": {"v": verb},
        "confidence": "high", "authority": "a", "environment": {}, "limitations": [],
        "relationship_coverage": None, "locations": [], "evidence_links": [],
        "nonce": "%s-%s-%s" % (carrier, verb, run_name),
    }
    data["evidence_id"] = recompute.compute_evidence_id(data)
    return {"ok": True, "data": data, "meta": {"command": verb, "duration": "1ms"}}


def _build_green(repo, recompute_src, counter_src):
    subprocess.run(["git", "init", "-q", repo], check=True)
    _write(repo, SOURCES, "| id |\n| S001 | old | code | A | s | a | t | mined | 2026-10-20 | r | u |\n")
    base = _commit(repo, "2026-10-22T10:00:00Z", "base")
    _write(repo, RECOMPUTE_PATH, recompute_src)
    _write(repo, COUNTER_PATH, counter_src)
    _commit(repo, "2026-10-22T11:00:00Z", "counter")
    spec = importlib.util.spec_from_file_location("rc_selftest", os.path.join(repo, RECOMPUTE_PATH))
    recompute = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recompute)
    runs = ["\t".join(RUNS_HEADER)]
    table = ["\t".join(TABLE_HEADER)]
    for carrier, frozen in CARRIERS.items():
        for verb in VERBS:
            ids = {}
            for run_name in RUNS:
                path = frozen["base"] if run_name in ("base", "repeat") else frozen["renamed"]
                env = _envelope(recompute, carrier, verb, run_name, path, verb == "inspect-binary-layout")
                raw = json.dumps(env, indent=1).encode("utf-8")
                _write(repo, "%s/envelopes/%s-%s-%s.json" % (EVDIR, carrier, verb, run_name), raw)
                eid = env["data"]["evidence_id"]
                ids[run_name] = eid
                runs.append("\t".join(["Seat", carrier, verb, run_name, path, argv_for(carrier, verb, path), "0",
                                       "2026-10-22T11:30:00Z", "2026-10-22T11:30:05Z",
                                       hashlib.sha256(raw).hexdigest(), eid, frozen["sha256"],
                                       PKG_VERSION, PKG_JSON_SHA256]))
            verdict = "content-keyed" if ids["base"] == ids["renamed"] else "rename-sensitive"
            table.append("\t".join([carrier, verb, verdict, ids["base"], ids["repeat"], ids["renamed"], frozen["sha256"]]))
    _write(repo, EVDIR + "/runs.tsv", "\n".join(runs) + "\n")
    _write(repo, EVDIR + "/table.tsv", "\n".join(table) + "\n")
    _write(repo, ENTRY, "source: `%s/table.tsv`; S900 test row\n\n# entry\n" % EVDIR)
    _write(repo, SOURCES, "| id |\n| S001 | old | code | A | s | a | t | mined | 2026-10-20 | r | u |\n"
                          "| S900 | new | code | A | s | a | t | mined | %s | r | u |\n" % OPENED)
    _write(repo, LESSON, "# lesson\n\n## Gate\n\n| row | x |\n|---|---|\n| S900 | quote |\n\n## Mistakes\n\n| S901 | no |\n")
    _commit(repo, "2026-10-22T12:00:00Z", "data")
    return base


def _tsv_edit(repo, rel, carrier, verb, run_name, column, value):
    path = os.path.join(repo, rel)
    lines = open(path, encoding="utf-8").read().split("\n")
    header = lines[0].split("\t")
    for i, line in enumerate(lines[1:], start=1):
        cells = line.split("\t")
        if len(cells) != len(header):
            continue
        row = dict(zip(header, cells))
        if row["carrier"] == carrier and row["verb"] == verb and (run_name is None or row.get("run") == run_name):
            cells[header.index(column)] = value
            lines[i] = "\t".join(cells)
            break
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def _env_path(repo, carrier, verb, run_name):
    return os.path.join(repo, "%s/envelopes/%s-%s-%s.json" % (EVDIR, carrier, verb, run_name))


def _resync(repo, carrier, verb, run_name):
    raw = open(_env_path(repo, carrier, verb, run_name), "rb").read()
    _tsv_edit(repo, EVDIR + "/runs.tsv", carrier, verb, run_name, "envelope_sha256", hashlib.sha256(raw).hexdigest())


def _mut_json(repo, carrier, verb, run_name, fn, resync=True):
    path = _env_path(repo, carrier, verb, run_name)
    env = json.load(open(path))
    fn(env)
    open(path, "w").write(json.dumps(env, indent=1))
    if resync:
        _resync(repo, carrier, verb, run_name)


def selftest():
    recompute_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "round-26", "recompute-ids.py"), "rb").read()
    counter_src = open(os.path.abspath(__file__), "rb").read()
    scratch_root = "/fast/scratch/hyaku" if os.path.isdir("/fast/scratch/hyaku") else None
    scratch = tempfile.mkdtemp(prefix="r27c1-selftest-", dir=scratch_root)
    green = os.path.join(scratch, "green")
    base = _build_green(green, recompute_src, counter_src)
    j, a = "jq", "analyze"

    def swap_copy(repo):  # renamed envelope replaced by base bytes (round-26 forgery 1)
        shutil.copy(_env_path(repo, j, a, "base"), _env_path(repo, j, a, "renamed"))

    def reuse_run(repo):  # one run used for repeat, sha resynced (forgery 2)
        shutil.copy(_env_path(repo, j, a, "base"), _env_path(repo, j, a, "repeat"))
        _resync(repo, j, a, "repeat")

    def swap_verbs(repo):  # analyze and inspect envelopes swapped (forgery 3)
        for run_name in RUNS:
            pa, pb = _env_path(repo, j, "analyze", run_name), _env_path(repo, j, "inspect", run_name)
            ta, tb = open(pa, "rb").read(), open(pb, "rb").read()
            open(pa, "wb").write(tb)
            open(pb, "wb").write(ta)
            _resync(repo, j, "analyze", run_name)
            _resync(repo, j, "inspect", run_name)

    def early_run(repo):  # pre-counter probe reused (forgery 4)
        _tsv_edit(repo, EVDIR + "/runs.tsv", j, a, "base", "utc_start", "2026-10-22T10:30:00Z")

    def wrong_pkg(repo):
        _tsv_edit(repo, EVDIR + "/runs.tsv", j, a, "base", "pkg_version", "6.7.0")

    def wrong_pkg_sha(repo):
        _tsv_edit(repo, EVDIR + "/runs.tsv", j, a, "base", "pkg_json_sha256", "0" * 64)

    def wrong_path(repo):
        _tsv_edit(repo, EVDIR + "/runs.tsv", j, a, "renamed", "path", "/usr/bin/jq")

    def wrong_argv(repo):
        _tsv_edit(repo, EVDIR + "/runs.tsv", j, a, "base", "argv", "analyze /usr/bin/jq --format json")

    def forged_id(repo):  # id edited in envelope, table and runs consistently: recompute catches it
        new = "ev_" + "1" * 64
        _mut_json(repo, j, a, "renamed", lambda e: e["data"].__setitem__("evidence_id", new))
        _tsv_edit(repo, EVDIR + "/runs.tsv", j, a, "renamed", "evidence_id", new)
        _tsv_edit(repo, EVDIR + "/table.tsv", j, a, None, "renamed_id", new)
        _tsv_edit(repo, EVDIR + "/table.tsv", j, a, None, "verdict", "rename-sensitive")

    def wrong_verdict(repo):
        _tsv_edit(repo, EVDIR + "/table.tsv", j, a, None, "verdict", "rename-sensitive")

    def table_cell(repo):
        _tsv_edit(repo, EVDIR + "/table.tsv", j, a, None, "repeat_id", "ev_" + "2" * 64)

    def meta_command(repo):
        _mut_json(repo, j, a, "base", lambda e: e["meta"].__setitem__("command", "inspect"))

    def other_path(repo):  # renamed envelope mentions the base path
        _mut_json(repo, j, a, "renamed", lambda e: e.__setitem__("note", "/usr/bin/jq"))

    def subject_name(repo):
        path = _env_path(repo, j, a, "renamed")
        env = json.load(open(path))
        env["data"]["subject"]["name"] = "jq"
        open(path, "w").write(json.dumps(env, indent=1))
        _resync(repo, j, a, "renamed")

    def subject_sha(repo):
        _tsv_edit(repo, EVDIR + "/runs.tsv", j, a, "base", "subject_sha256", "f" * 64)

    def not_ok(repo):
        _mut_json(repo, j, a, "base", lambda e: e.__setitem__("ok", False))

    def missing_env(repo):
        os.remove(_env_path(repo, "tinyxxd", "xrefs", "repeat"))

    def entry_no_table(repo):
        _write(repo, ENTRY, "source: S900 only\n")

    def entry_old_row(repo):  # cites a row that existed at base
        _write(repo, ENTRY, "source: `%s/table.tsv`; S001\n" % EVDIR)

    def gate_missing(repo):  # S row cited only outside ## Gate
        _write(repo, LESSON, "# lesson\n\n## Gate\n\nnothing\n\n## Mistakes\n\n| S900 | x |\n")

    def status_wrong(repo):
        _write(repo, SOURCES, "| id |\n| S001 | old | code | A | s | a | t | mined | 2026-10-20 | r | u |\n"
                              "| S900 | new | code | A | s | a | t | candidate | %s | r | u |\n" % OPENED)

    cases = [
        ("green", None, 0, None),
        ("swap-renamed-with-base", swap_copy, 1, "envelope sha256 differs"),
        ("reuse-one-run", reuse_run, 1, "shared with another run"),
        ("swap-verbs", swap_verbs, 1, "meta.command"),
        ("run-before-counter", early_run, 1, "not after counter commit"),
        ("package-version", wrong_pkg, 1, "not the frozen 6.5.0"),
        ("package-json-sha", wrong_pkg_sha, 1, "not the frozen 6.5.0"),
        ("run-path", wrong_path, 1, "path /usr/bin/jq, frozen"),
        ("argv", wrong_argv, 1, "argv differs"),
        ("forged-id-consistent", forged_id, 1, "does not recompute"),
        ("table-verdict", wrong_verdict, 1, "table verdict"),
        ("table-id-cell", table_cell, 1, "table id cells differ"),
        ("meta-command", meta_command, 1, "meta.command"),
        ("other-path-in-envelope", other_path, 1, "row's other path"),
        ("subject-name", subject_name, 1, "subject.name"),
        ("subject-sha", subject_sha, 1, "subject sha256 not the carrier"),
        ("not-ok", not_ok, 1, "not an ok envelope"),
        ("missing-envelope", missing_env, 1, "absent"),
        ("entry-no-table", entry_no_table, 1, "does not name"),
        ("entry-cites-base-row", entry_old_row, 1, "names no S###"),
        ("gate-missing-row", gate_missing, 1, "names no S###"),
        ("row-status", status_wrong, 1, "names no S###"),
    ]
    failures = 0
    for name, mutate, want_exit, want_text in cases:
        repo = os.path.join(scratch, "case-" + name)
        subprocess.run(["git", "clone", "-q", green, repo], check=True)
        if mutate is not None:
            mutate(repo)
            _commit(repo, "2026-10-22T12:30:00Z", "mutation " + name)
        buf = _Buffer()
        try:
            got = run_count(repo, "HEAD", base, out=buf)
        except InputError as error:
            got = 2
            buf.write("input error: %s\n" % error)
        text = buf.getvalue()
        ok = got == want_exit and (want_text is None or want_text in text)
        failures += 0 if ok else 1
        summary = [l for l in text.split("\n") if l.startswith("rows_complete")]
        print("%s %s: exit %d (want %d)%s %s" % ("PASS" if ok else "FAIL", name, got, want_exit,
              "" if want_text is None else " expects %r" % want_text, summary[0] if summary else ""))
        if not ok:
            print("  " + text.replace("\n", "\n  ")[:2000])
    shutil.rmtree(scratch, ignore_errors=True)
    print("selftest cases=%d failures=%d" % (len(cases), failures))
    return 0 if failures == 0 else 1


class _Buffer:
    def __init__(self):
        self.parts = []

    def write(self, text):
        self.parts.append(text)

    def getvalue(self):
        return "".join(self.parts)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root")
    parser.add_argument("--rev")
    parser.add_argument("--base", default=BASE)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.root or not args.rev:
        parser.error("--root and --rev are required")
    try:
        rev = git(args.root, "rev-parse", "--verify", args.rev + "^{commit}").strip()
        return run_count(args.root, rev, args.base)
    except InputError as error:
        print("input error: %s" % error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
