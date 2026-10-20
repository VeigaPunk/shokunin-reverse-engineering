#!/usr/bin/env python3
"""wave-outcomes.py — per-seat wave outcome record (fixes R18-DEADSEAT-RECORD).

Reads a wave registration in the `ufo-swarm-registry-v1` shape (model:
.ufo/waves/round-18/wave2-registration.json), a report directory, and a causes
file, then writes one row per registered seat:

    {"name": <seat>, "role": <role>, "report_present": <bool>,
     "cause": <text|null>}

and exits 1 when any seat with no report has no non-empty cause. A dead seat
therefore cannot be recorded without retained failure text: the field is part
of the record, not prose in a later report.

Rules (each count is printed together with its rule):
  report  — a seat's report is present iff <report-dir>/<name>.md is a regular
            file with size > 0. A zero-byte file, a directory, or a dangling
            symlink counts as absence.
  cause   — a seat's cause is causes[<name>] or causes[<agentId>]; it counts
            only when non-empty after .strip().
  exit    — 1 iff any seat with report_present=false has cause null; 0 otherwise.

Causes file shapes accepted (every key is resolved against the registration,
so a typo cannot silently mark a seat dead):
  flat map          {"Seat": "text" | {"cause": "text", "source": "..."}, ...}
  wrapped map       {"wave": "...", "causes": {<flat map>}}
  list of rows      {"wave": "...", "seats": [{"name"|"seat"|"agentId": ...,
                                               "cause"|"reason"|"error"|"text": ...,
                                               "source": ...}, ...]}
Registration metadata keys in the flat-map shape (schema, wave, path,
createdAt, updatedAt, generatedAt, note, source, registration, reportDir,
report_dir) are ignored and counted as `causes_ignored_meta`.

Refusals exit 2 and write nothing; each names its cause:
  argv_missing, registration_unreadable, registration_invalid, members_empty,
  member_invalid, seat_name_unsafe, report_dir_missing, causes_unreadable,
  causes_invalid, cause_value_invalid, causes_unknown_seat, causes_ambiguous,
  out_unwritable.

Determinism: the record carries no timestamp and no computed paths — inputs
are bound by sha256 (registration, causes) and seats are emitted in byte order
of their names — so two runs over identical inputs are byte-identical. Path
arguments are recorded verbatim as given on argv (a clone-relative and an
absolute invocation of the same tree differ only in those strings), while the
input *content* is bound by `registration_sha256`/`causes_sha256`: compare two
records by those digests, not by their path strings. The out file is replaced
atomically (tmp + os.replace) and may overwrite.

CLI:
    wave-outcomes.py --registration REG --report-dir DIR --causes CAUSES
                     --out OUT [--selftest]

--selftest builds fixtures only under tempfile.mkdtemp() and prints
`SELFTEST: CLEAN cases=N` (exit 0) or `SELFTEST: FAILED ...; cases=N fails=M`
(exit 1).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

SCHEMA = "ufo-wave-outcomes-v1"
CAUSE_KEYS = ("cause", "reason", "error", "text")
NAME_KEYS = ("name", "seat", "agentId", "agent")
META_KEYS = frozenset({
    "schema", "wave", "path", "createdAt", "updatedAt", "generatedAt",
    "note", "source", "registration", "reportDir", "report_dir",
})
RULE = {
    "report": "report_present=<report-dir>/<name>.md exists as a regular "
              "file with size>0",
    "cause": "cause=causes[<name>| <agentId>], non-empty after strip",
    "exit": "1 iff any seat with report_present=false has cause null",
}


class Refusal(RuntimeError):
    """An unusable input, carrying a named finding and its cause."""

    def __init__(self, finding: str, detail: str):
        super().__init__(f"{finding}: {detail}")
        self.finding = finding
        self.detail = detail


def _read_json(path: str, what: str):
    """Read one JSON input; a missing/unreadable/invalid file is a refusal."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except FileNotFoundError:
        raise Refusal(f"{what}_unreadable", f"{path}: no such file")
    except IsADirectoryError:
        raise Refusal(f"{what}_unreadable", f"{path}: is a directory")
    except OSError as exc:
        raise Refusal(f"{what}_unreadable",
                      f"{path}: {exc.strerror or exc}")
    try:
        doc = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise Refusal(f"{what}_invalid",
                      f"{path}: not UTF-8 ({exc.reason} at byte {exc.start})")
    except json.JSONDecodeError as exc:
        raise Refusal(f"{what}_invalid",
                      f"{path}: {exc.msg} at line {exc.lineno} "
                      f"column {exc.colno}")
    return doc, hashlib.sha256(raw).hexdigest()


def _safe_seat_name(name) -> bool:
    """A seat name must be one bare file name: it becomes <dir>/<name>.md."""
    return (isinstance(name, str) and bool(name) and name not in (".", "..")
            and "/" not in name and "\\" not in name and "\0" not in name
            and os.path.basename(name) == name)


def load_registration(path: str):
    """Return ({seat: {role, agentId}}, sha256, schema-token-or-None)."""
    doc, sha = _read_json(path, "registration")
    if not isinstance(doc, dict):
        raise Refusal("registration_invalid",
                      f"{path}: top level is {type(doc).__name__}, "
                      f"expected an object with 'members'")
    raw_members = doc.get("members")
    if raw_members is None:
        raise Refusal("registration_invalid", f"{path}: no 'members' object")
    if not isinstance(raw_members, dict):
        raise Refusal("registration_invalid",
                      f"{path}: members is {type(raw_members).__name__}, "
                      f"expected an object keyed by seat name")
    if not raw_members:
        raise Refusal("members_empty",
                      f"{path}: members is empty; no seat to record")
    seats = {}
    for name, member in raw_members.items():
        if not _safe_seat_name(name):
            raise Refusal("seat_name_unsafe",
                          f"{path}: seat {name!r} is not a bare file name; "
                          f"<report-dir>/<name>.md would escape the dir")
        if not isinstance(member, dict):
            raise Refusal("member_invalid",
                          f"{path}: seat {name} is {type(member).__name__}, "
                          f"expected an object")
        role = member.get("role")
        if not isinstance(role, str) or not role.strip():
            raise Refusal("member_invalid",
                          f"{path}: seat {name} has no non-empty string role")
        agent = member.get("agentId")
        if agent is not None and not isinstance(agent, str):
            raise Refusal("member_invalid",
                          f"{path}: seat {name} agentId is "
                          f"{type(agent).__name__}, expected a string")
        seats[name] = {
            "role": role.strip(),
            "agentId": agent.strip() if isinstance(agent, str) and agent.strip()
            else None,
        }
    schema = doc.get("schema")
    return seats, sha, schema if isinstance(schema, str) else None


def _report_present(path: str) -> bool:
    """Rule `report`: a regular file with size > 0; symlink targets count."""
    try:
        st = os.stat(path)
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and st.st_size > 0


def _normalize_entry(raw_name: str, value, where: str):
    """Return (cause-text-or-None, source-or-None) for one causes value."""
    if isinstance(value, str):
        return value.strip() or None, None
    if not isinstance(value, dict):
        raise Refusal("cause_value_invalid",
                      f"{where}: {raw_name} value is "
                      f"{type(value).__name__}, expected string or object")
    text = None
    for key in CAUSE_KEYS:
        if key not in value:
            continue
        field = value[key]
        if not isinstance(field, str):
            raise Refusal("cause_value_invalid",
                          f"{where}: {raw_name} field {key!r} is "
                          f"{type(field).__name__}, expected a string")
        text = field.strip() or None
        break
    source = value.get("source")
    if source is not None and not isinstance(source, str):
        raise Refusal("cause_value_invalid",
                      f"{where}: {raw_name} source is "
                      f"{type(source).__name__}, expected a string")
    return text, (source.strip() or None) if isinstance(source, str) else None


def _resolve_seat(raw_name: str, seats: dict, by_agent: dict, where: str,
                  registration: str) -> str:
    if raw_name in seats:
        return raw_name
    if raw_name in by_agent:
        return by_agent[raw_name]
    raise Refusal("causes_unknown_seat",
                  f"{where}: {raw_name!r} is neither a seat nor an agentId "
                  f"of {registration} ({len(seats)} seats)")


def _merge(resolved: dict, seat: str, text, source, where: str) -> None:
    prev = resolved.get(seat)
    if prev is None:
        resolved[seat] = {"cause": text, "source": source}
        return
    if prev["cause"] != text:
        raise Refusal("causes_ambiguous",
                      f"{where}: seat {seat} carries two different causes")
    if source and prev["source"] and source != prev["source"]:
        raise Refusal("causes_ambiguous",
                      f"{where}: seat {seat} carries two different sources")
    if source and not prev["source"]:
        prev["source"] = source


def load_causes(path: str, seats: dict, by_agent: dict, registration: str):
    """Return ({seat: {cause, source}}, sha256, wave-or-None, ignored-meta)."""
    doc, sha = _read_json(path, "causes")
    wave = None
    raw = doc
    if (isinstance(doc, dict) and isinstance(doc.get("causes"), dict)
            and "wave" in doc):
        wave = doc.get("wave") if isinstance(doc.get("wave"), str) else None
        raw = doc["causes"]
        if not isinstance(raw, dict):
            raise Refusal("causes_invalid",
                          f"{path}: 'causes' is {type(raw).__name__}, "
                          f"expected an object keyed by seat")
    elif isinstance(doc, dict) and "seats" in doc:
        wave = doc.get("wave") if isinstance(doc.get("wave"), str) else None
        raw = doc["seats"]
        if not isinstance(raw, list):
            raise Refusal("causes_invalid",
                          f"{path}: 'seats' is {type(raw).__name__}, "
                          f"expected a list of rows")
    resolved: dict = {}
    ignored = []
    if isinstance(raw, dict):
        for key, value in raw.items():
            if not isinstance(key, str) or not key.strip():
                raise Refusal("causes_invalid",
                              f"{path}: cause key {key!r} is not a "
                              f"non-empty string")
            if key in META_KEYS and key not in seats:
                ignored.append(key)
                continue
            text, source = _normalize_entry(key, value, path)
            seat = _resolve_seat(key.strip(), seats, by_agent, path,
                                 registration)
            _merge(resolved, seat, text, source, path)
    elif isinstance(raw, list):
        for idx, entry in enumerate(raw):
            where = f"{path} seats[{idx}]"
            if not isinstance(entry, dict):
                raise Refusal("cause_value_invalid",
                              f"{where} is {type(entry).__name__}, "
                              f"expected an object row")
            name = None
            for key in NAME_KEYS:
                field = entry.get(key)
                if isinstance(field, str) and field.strip():
                    name = field.strip()
                    break
            if name is None:
                raise Refusal("causes_invalid",
                              f"{where} has no non-empty name/seat/agentId")
            text, source = _normalize_entry(name, entry, where)
            seat = _resolve_seat(name, seats, by_agent, where, registration)
            _merge(resolved, seat, text, source, where)
    else:
        raise Refusal("causes_invalid",
                      f"{path}: top level is {type(raw).__name__}, "
                      f"expected an object or a list")
    return resolved, sha, wave, ignored


def evaluate(registration: str, report_dir: str, causes: str):
    """Build the outcome record; return (doc, exit-code 0|1)."""
    seats, reg_sha, reg_schema = load_registration(registration)
    if not os.path.isdir(report_dir):
        raise Refusal("report_dir_missing",
                      f"{report_dir}: not a directory; refusing to score "
                      f"every seat as dead")
    by_agent: dict = {}
    for name in sorted(seats):
        agent = seats[name]["agentId"]
        if not agent:
            continue
        if agent in by_agent:
            raise Refusal("registration_invalid",
                          f"{registration}: agentId {agent!r} is shared by "
                          f"{by_agent[agent]} and {name}")
        by_agent[agent] = name
    resolved, causes_sha, wave, ignored = load_causes(
        causes, seats, by_agent, registration)

    rows = []
    for name in sorted(seats):
        entry = resolved.get(name) or {}
        rows.append({
            "name": name,
            "role": seats[name]["role"],
            "report_present": _report_present(
                os.path.join(report_dir, name + ".md")),
            "cause": entry.get("cause"),
        })

    missing = [r["name"] for r in rows if not r["report_present"]]
    uncaused = [r["name"] for r in rows
                if not r["report_present"] and not r["cause"]]
    unneeded = [r["name"] for r in rows
                if r["report_present"] and r["cause"]]
    sources = {name: resolved[name]["source"] for name in sorted(resolved)
               if resolved[name]["source"]}

    doc = {
        "schema": SCHEMA,
        "registration": registration,
        "registration_sha256": reg_sha,
        "registration_schema": reg_schema,
        "report_dir": report_dir,
        "causes": causes,
        "causes_sha256": causes_sha,
        "wave": wave,
        "rule": dict(RULE),
        "seat_count": len(rows),
        "report_present_count": len(rows) - len(missing),
        "missing_count": len(missing),
        "uncaused_count": len(uncaused),
        "causes_recorded": sum(1 for r in rows if r["cause"]),
        "missing": missing,
        "uncaused": uncaused,
        "causes_unneeded": unneeded,
        "causes_ignored_meta": ignored,
        "cause_sources": sources,
        "seats": rows,
    }
    return doc, (1 if uncaused else 0)


def _write_json_atomic(path: str, doc) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    try:
        os.makedirs(parent, exist_ok=True)
        payload = json.dumps(doc, indent=2, ensure_ascii=True,
                             sort_keys=False) + "\n"
        fd, tmp = tempfile.mkstemp(prefix=".wave-outcomes-", suffix=".tmp", dir=parent)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload)
        os.replace(tmp, path)
    except OSError as exc:
        try:
            os.unlink(tmp)
        except (OSError, UnboundLocalError):
            pass
        raise Refusal("out_unwritable",
                      f"{path}: {exc.strerror or exc}")


def _print_summary(doc: dict, out: str) -> None:
    print(f"OUTCOMES seats={doc['seat_count']} "
          f"reports={doc['report_present_count']} "
          f"missing={doc['missing_count']} "
          f"uncaused={doc['uncaused_count']} "
          f"(rule: report={RULE['report']}; cause={RULE['cause']})")
    print(f"MISSING n={doc['missing_count']} {json.dumps(doc['missing'])} "
          f"(rule: seat has no report file)")
    print(f"CAUSES recorded={doc['causes_recorded']} "
          f"unneeded={len(doc['causes_unneeded'])} "
          f"ignored_meta={len(doc['causes_ignored_meta'])} "
          f"(rule: one non-empty cause per seat, from "
          f"causes[<name>|<agentId>])")
    if doc["uncaused"]:
        print(f"UNCAUSED n={doc['uncaused_count']} "
              f"{json.dumps(doc['uncaused'])} "
              f"(rule: {RULE['exit']}) -> exit 1")
    print(f"OUT {out}")


def _selftest() -> int:
    """Fixtures live only under tempfile.mkdtemp(); nothing touches the lane."""
    here = os.path.abspath(__file__)
    failures = []
    cases = [0]

    def check(ok, label, detail):
        cases[0] += 1
        if not ok:
            failures.append(f"{label}: {detail}")

    def run_cli(*argv):
        return subprocess.run([sys.executable, "-I", "-B", here, *argv],
                              capture_output=True, text=True, check=False)

    def load_out(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return {}

    root = os.path.realpath(tempfile.mkdtemp(prefix="wave-outcomes-selftest-"))

    def fixture(tag, members, reports, causes_doc=None, reg_text=None,
                causes_text=None, make_report_dir=True):
        """Write one registration/report-dir/causes triple under root/tag.

        members: {seat: role}; reports: {seat: text|"DIR"|"EMPTY"}.
        """
        base = os.path.join(root, tag)
        os.makedirs(base, exist_ok=True)
        reg_path = os.path.join(base, "registration.json")
        if reg_text is not None:
            with open(reg_path, "w", encoding="utf-8") as fh:
                fh.write(reg_text)
        else:
            reg = {
                "path": ".ufo/waves/round-19/" + tag + "-registry.json",
                "schema": "ufo-swarm-registry-v1",
                "wave": None,
                "reportDir": "reports",
                "members": {
                    name: {"kind": "spawn",
                           "agentId": "Kaidoku19." + name,
                           "role": role,
                           "item": None,
                           "axes": ["calibration", "freshness", "depth"]}
                    for name, role in members.items()
                },
            }
            with open(reg_path, "w", encoding="utf-8") as fh:
                json.dump(reg, fh)
        rdir = os.path.join(base, "reports")
        if make_report_dir:
            os.makedirs(rdir, exist_ok=True)
        for name, payload in reports.items():
            rpath = os.path.join(rdir, name + ".md")
            if payload == "DIR":
                os.makedirs(rpath, exist_ok=True)
            else:
                with open(rpath, "w", encoding="utf-8") as fh:
                    fh.write("" if payload == "EMPTY" else payload)
        cpath = os.path.join(base, "causes.json")
        if causes_text is not None:
            with open(cpath, "w", encoding="utf-8") as fh:
                fh.write(causes_text)
        elif causes_doc is not None:
            with open(cpath, "w", encoding="utf-8") as fh:
                json.dump(causes_doc, fh)
        else:
            with open(cpath, "w", encoding="utf-8") as fh:
                fh.write("{}\n")
        return reg_path, rdir, cpath, os.path.join(base, "out.json")

    try:
        # ---- clean path: every seat reported, no cause needed -------------
        reg, rdir, cpath, out = fixture(
            "c1", {"Alpha": "executor", "Bravo": "critic"},
            {"Alpha": "a\n", "Bravo": "b\n"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0 and doc.get("missing") == []
              and doc.get("seat_count") == 2
              and doc.get("report_present_count") == 2
              and doc.get("uncaused_count") == 0,
              "all-present", f"rc={r.returncode} doc={doc}")
        check([s.get("name") for s in doc.get("seats", [])]
              == ["Alpha", "Bravo"]
              and [set(s) for s in doc.get("seats", [])]
              == [{"name", "role", "report_present", "cause"}] * 2,
              "seat-shape", f"seats={doc.get('seats')}")
        check(doc.get("rule", {}).get("exit") == RULE["exit"]
              and doc.get("registration_sha256")
              and doc.get("causes_sha256"),
              "record-binding", f"doc={doc}")

        # ---- a missing seat with no cause is the red state ---------------
        reg, rdir, cpath, out = fixture(
            "c2", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 1 and doc.get("missing") == ["Bravo"]
              and doc.get("uncaused") == ["Bravo"],
              "missing-uncaused-red", f"rc={r.returncode} doc={doc}")
        check(doc.get("seats", [{}])[1].get("report_present") is False
              and doc.get("seats", [{}])[1].get("cause") is None,
              "missing-null-cause", f"seats={doc.get('seats')}")
        check("-> exit 1" in r.stdout, "red-reason", f"out={r.stdout!r}")

        # ---- string cause clears the red state ---------------------------
        reg, rdir, cpath, out = fixture(
            "c3", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": "worker exited 1 before its first tool call"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and doc.get("seats", [{}])[1].get("cause")
              == "worker exited 1 before its first tool call"
              and doc.get("missing") == ["Bravo"],
              "string-cause", f"rc={r.returncode} doc={doc}")

        # ---- object cause keeps its source -------------------------------
        reg, rdir, cpath, out = fixture(
            "c4", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": {"cause": "exited 1", "source": "history://K19.Bravo"}})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and doc.get("cause_sources", {}).get("Bravo")
              == "history://K19.Bravo"
              and doc.get("seats", [{}])[1].get("cause") == "exited 1",
              "object-cause-source", f"rc={r.returncode} doc={doc}")

        # ---- an agentId key resolves to its seat -------------------------
        reg, rdir, cpath, out = fixture(
            "c5", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Kaidoku19.Bravo": "exited 1"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and doc.get("seats", [{}])[1].get("cause") == "exited 1",
              "agentid-key", f"rc={r.returncode} doc={doc}")

        # ---- a whitespace-only cause is not a cause ----------------------
        reg, rdir, cpath, out = fixture(
            "c6", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": "   \n\t"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 1 and doc.get("uncaused") == ["Bravo"]
              and doc.get("seats", [{}])[1].get("cause") is None,
              "blank-cause-red", f"rc={r.returncode} doc={doc}")

        # ---- zero-byte and directory "reports" are absence ---------------
        reg, rdir, cpath, out = fixture(
            "c7", {"Alpha": "executor", "Bravo": "critic"},
            {"Alpha": "EMPTY", "Bravo": "DIR"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 1
              and doc.get("missing") == ["Alpha", "Bravo"]
              and doc.get("report_present_count") == 0,
              "empty-and-dir-absent", f"rc={r.returncode} doc={doc}")

        # ---- an absent report dir is a refusal, not 98 dead seats --------
        reg, rdir, cpath, out = fixture(
            "c9", {"Alpha": "executor"}, {}, make_report_dir=False)
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "report_dir_missing" in r.stderr
              and not os.path.exists(out),
              "report-dir-missing", f"rc={r.returncode} err={r.stderr!r}")

        # ---- a causes key outside the registration is refused ------------
        reg, rdir, cpath, out = fixture(
            "c10", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Zulu": "exited 1"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "causes_unknown_seat" in r.stderr
              and "Zulu" in r.stderr and not os.path.exists(out),
              "unknown-cause-seat", f"rc={r.returncode} err={r.stderr!r}")

        # ---- malformed registration JSON ---------------------------------
        reg, rdir, cpath, out = fixture("c11", {}, {}, reg_text="{")
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "registration_invalid" in r.stderr,
              "registration-malformed", f"rc={r.returncode} err={r.stderr!r}")

        # ---- empty members ------------------------------------------------
        reg, rdir, cpath, out = fixture(
            "c12", {}, {}, reg_text='{"schema": "ufo-swarm-registry-v1", '
            '"members": {}}')
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "members_empty" in r.stderr,
              "members-empty", f"rc={r.returncode} err={r.stderr!r}")

        # ---- a member without a role -------------------------------------
        reg, rdir, cpath, out = fixture(
            "c13", {}, {}, reg_text='{"members": {"Alpha": {"kind": "spawn"}}}')
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "member_invalid" in r.stderr
              and "Alpha" in r.stderr,
              "member-no-role", f"rc={r.returncode} err={r.stderr!r}")

        # ---- a seat name that would escape the report dir ----------------
        reg, rdir, cpath, out = fixture(
            "c14", {}, {}, reg_text='{"members": {"../escape": '
            '{"role": "executor"}}}')
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "seat_name_unsafe" in r.stderr,
              "seat-name-escape", f"rc={r.returncode} err={r.stderr!r}")

        # ---- malformed causes JSON ---------------------------------------
        reg, rdir, cpath, out = fixture(
            "c15", {"Alpha": "executor"}, {"Alpha": "a\n"}, causes_text="[")
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "causes_invalid" in r.stderr,
              "causes-malformed", f"rc={r.returncode} err={r.stderr!r}")

        # ---- missing causes file -----------------------------------------
        reg, rdir, cpath, out = fixture(
            "c16", {"Alpha": "executor"}, {"Alpha": "a\n"})
        os.unlink(cpath)
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "causes_unreadable" in r.stderr,
              "causes-missing", f"rc={r.returncode} err={r.stderr!r}")

        # ---- two conflicting entries for one seat ------------------------
        reg, rdir, cpath, out = fixture(
            "c17", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": "one", "Kaidoku19.Bravo": "two"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "causes_ambiguous" in r.stderr,
              "ambiguous-cause", f"rc={r.returncode} err={r.stderr!r}")

        # ---- the same cause under both forms collapses -------------------
        reg, rdir, cpath, out = fixture(
            "c18", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": "exited 1", "Kaidoku19.Bravo": "exited 1"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and doc.get("causes_recorded") == 1
              and doc.get("seats", [{}])[1].get("cause") == "exited 1",
              "duplicate-identical", f"rc={r.returncode} doc={doc}")

        # ---- a cause on a reporting seat is retained, not required -------
        reg, rdir, cpath, out = fixture(
            "c19", {"Alpha": "executor", "Bravo": "critic"},
            {"Alpha": "a\n", "Bravo": "b\n"}, {"Alpha": "late but returned"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and doc.get("causes_unneeded") == ["Alpha"]
              and doc.get("seats", [{}])[0].get("cause")
              == "late but returned",
              "unneeded-cause", f"rc={r.returncode} doc={doc}")

        # ---- byte-identical reruns ---------------------------------------
        reg, rdir, cpath, out_a = fixture(
            "c20", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": "exited 1"})
        out_b = os.path.join(os.path.dirname(out_a), "out-b.json")
        r1 = run_cli("--registration", reg, "--report-dir", rdir,
                     "--causes", cpath, "--out", out_a)
        r2 = run_cli("--registration", reg, "--report-dir", rdir,
                     "--causes", cpath, "--out", out_b)
        with open(out_a, "rb") as fh:
            blob_a = fh.read()
        with open(out_b, "rb") as fh:
            blob_b = fh.read()
        check(r1.returncode == r2.returncode == 0 and blob_a == blob_b
              and blob_a.endswith(b"\n"),
              "deterministic-bytes", f"rc={r1.returncode}/{r2.returncode} "
              f"len={len(blob_a)}/{len(blob_b)}")

        # ---- list-shaped causes with source ------------------------------
        reg, rdir, cpath, out = fixture(
            "c21", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"wave": "selftest",
             "seats": [{"seat": "Bravo", "cause": "exited 1",
                        "source": "history://K19.Bravo"}]})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0 and doc.get("wave") == "selftest"
              and doc.get("cause_sources", {}).get("Bravo")
              == "history://K19.Bravo",
              "list-causes", f"rc={r.returncode} doc={doc}")

        # ---- wrapped map -------------------------------------------------
        reg, rdir, cpath, out = fixture(
            "c22", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"wave": "selftest", "causes": {"Bravo": "exited 1"}})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0 and doc.get("wave") == "selftest"
              and doc.get("seats", [{}])[1].get("cause") == "exited 1",
              "wrapped-causes", f"rc={r.returncode} doc={doc}")

        # ---- a seat named "causes" stays a flat-map entry ---------------
        reg, rdir, cpath, out = fixture(
            "c22b", {"causes": "executor"}, {},
            {"causes": {"cause": "worker aborted",
                        "source": "history://K19.causes"}})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and doc.get("seats") == [{
                  "name": "causes", "role": "executor",
                  "report_present": False, "cause": "worker aborted"}]
              and doc.get("cause_sources", {}).get("causes")
              == "history://K19.causes",
              "seat_named_causes", f"rc={r.returncode} doc={doc}")

        # ---- flat map with metadata keys ---------------------------------
        reg, rdir, cpath, out = fixture(
            "c23", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"schema": "x", "wave": "w", "Bravo": "exited 1"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and sorted(doc.get("causes_ignored_meta", []))
              == ["schema", "wave"],
              "flat-meta", f"rc={r.returncode} doc={doc}")

        # ---- a metadata-looking key that is also a seat still resolves ---
        reg, rdir, cpath, out = fixture(
            "c23b", {"Alpha": "executor", "source": "critic"},
            {"Alpha": "a\n"}, {"source": "exited 1"})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        doc = load_out(out)
        check(r.returncode == 0
              and doc.get("seats", [{}, {}])[1].get("cause") == "exited 1"
              and doc.get("causes_ignored_meta") == [],
              "meta-key-seat", f"rc={r.returncode} doc={doc}")

        # ---- duplicate agentId in the registration -----------------------
        reg, rdir, cpath, out = fixture(
            "c24", {}, {}, reg_text='{"members": {'
            '"A": {"role": "executor", "agentId": "K19.same"}, '
            '"B": {"role": "critic", "agentId": "K19.same"}}}')
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "registration_invalid" in r.stderr
              and "K19.same" in r.stderr,
              "duplicate-agentid", f"rc={r.returncode} err={r.stderr!r}")

        # ---- unwritable out ----------------------------------------------
        reg, rdir, cpath, out = fixture(
            "c25", {"Alpha": "executor"}, {"Alpha": "a\n"})
        blocker = os.path.join(os.path.dirname(out), "blocker")
        with open(blocker, "w", encoding="utf-8") as fh:
            fh.write("file, not a dir\n")
        bad_out = os.path.join(blocker, "out.json")
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", bad_out)
        check(r.returncode == 2 and "out_unwritable" in r.stderr,
              "out-unwritable", f"rc={r.returncode} err={r.stderr!r}")

        # ---- invalid cause value types -----------------------------------
        reg, rdir, cpath, out = fixture(
            "c26", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": 5})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "cause_value_invalid" in r.stderr,
              "cause-value-type", f"rc={r.returncode} err={r.stderr!r}")
        reg, rdir, cpath, out = fixture(
            "c27", {"Alpha": "executor", "Bravo": "critic"}, {"Alpha": "a\n"},
            {"Bravo": {"cause": 5}})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "cause_value_invalid" in r.stderr,
              "cause-field-type", f"rc={r.returncode} err={r.stderr!r}")

        # ---- a list row without a name -----------------------------------
        reg, rdir, cpath, out = fixture(
            "c28", {"Alpha": "executor"}, {"Alpha": "a\n"},
            {"seats": [{"cause": "exited 1"}]})
        r = run_cli("--registration", reg, "--report-dir", rdir,
                    "--causes", cpath, "--out", out)
        check(r.returncode == 2 and "causes_invalid" in r.stderr,
              "nameless-row", f"rc={r.returncode} err={r.stderr!r}")

        # ---- missing argv is refused, not defaulted ----------------------
        r = run_cli("--registration", reg)
        check(r.returncode == 2 and "argv_missing" in r.stderr
              and "--report-dir" in r.stderr,
              "argv-missing", f"rc={r.returncode} err={r.stderr!r}")
    except Exception as exc:  # fixture setup failure — reported as a failure
        failures.append(f"setup: {exc!r}")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    if failures:
        print(f"SELFTEST: FAILED {'; '.join(failures)}; "
              f"cases={cases[0]} fails={len(failures)}")
        return 1
    print(f"SELFTEST: CLEAN cases={cases[0]}")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(
        description="Record one row per registered wave seat "
                    "({name, role, report_present, cause}) and exit 1 when a "
                    "seat without a report has no non-empty cause.")
    ap.add_argument("--registration",
                    help="wave registration JSON (ufo-swarm-registry-v1)")
    ap.add_argument("--report-dir",
                    help="directory holding <seat>.md reports")
    ap.add_argument("--causes",
                    help="JSON mapping seat (or agentId) to failure text")
    ap.add_argument("--out", help="path of the outcome record to write")
    ap.add_argument("--selftest", action="store_true",
                    help="run fixture-based selftest outside the lane")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    absent = [flag for flag, value in (
        ("--registration", args.registration),
        ("--report-dir", args.report_dir),
        ("--causes", args.causes),
        ("--out", args.out)) if not value]
    if absent:
        sys.stderr.write(f"REFUSED argv_missing: required {', '.join(absent)}\n")
        return 2

    try:
        doc, code = evaluate(args.registration, args.report_dir, args.causes)
        _write_json_atomic(args.out, doc)
    except Refusal as exc:
        sys.stderr.write(f"REFUSED {exc.finding}: {exc.detail}\n")
        return 2
    _print_summary(doc, args.out)
    return code


if __name__ == "__main__":
    sys.exit(main())
