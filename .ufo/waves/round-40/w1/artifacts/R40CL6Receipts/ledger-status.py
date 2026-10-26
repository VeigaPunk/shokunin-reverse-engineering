#!/usr/bin/env python3
"""ledger-status.py — fill per-seat status into a copy of a wave results ledger.

Routed defect R39-CL6 (kaidoku round 40): both wave ledgers the orchestrator
writes carry `status: null` for every seat, so a closure cannot tell a seat that
reported from one that did not. This tool fills, per seat,

    status        "ok" | "no-report" | "empty-report"

from REPORT PRESENCE only: the seat's report file exists and holds non-whitespace
text -> ok; the file exists but is empty/whitespace-only -> empty-report; it
cannot be located -> no-report. It never reads the report's content beyond the
whitespace test and never judges a seat's work.

Report discovery per seat, in order, first existing candidate wins:
  1. every string under a `report`-style key (`report`, `report_path`,
     `report_file`, `report_md`, `reportpath`) anywhere inside the seat's
     `output` field (a JSON object, or a JSON string that parses; an already
     decoded object is accepted too), in document order, top level first;
  2. for a non-JSON output string, a `Report: <path>.md` trailer line;
  3. the lane convention `<wave-dir>/<name>.md`.

Paths are normalised before lookup: a leading `./` is dropped, a leading lane
basename (e.g. `kaidoku-shokunin/`) is dropped (the round-39 wave-2 ledger names
two reports that way), relative paths resolve against --root, and a candidate
outside --root (after realpath, so a symlink cannot smuggle it out) is rejected.

Each seat gains `status`, `report` (root-relative when inside root), `report_bytes`
(null for no-report) and `report_source` (`output` | `canonical`); a pre-existing
non-null `status` is preserved as `status_previous`. Nothing else in the ledger
is rewritten: the tool writes a COPY, the input file is read only, and key order
is kept.

    ledger-status.py RESULTS.json --root LANE [--wave-dir .ufo/waves/round-39/w1]
                       [--out PATH] [--selftest]

Without --out the filled ledger goes to stdout; a one-line count summary always
goes to stderr. --wave-dir defaults to `.ufo/waves/round-<round>/<w1|w2>` derived
from the ledger's own `round` and `wave` fields. Exit: 0 written, 2 usage/parse
error. Stdlib only; reads no files outside --root except the ledger itself.
"""

import argparse
import copy
import json
import os
import re
import sys
import tempfile

REPORT_KEYS = {
    "report", "report_path", "report_file", "report_md", "reportpath",
    "report_file_md", "report_path_md",
}
MAX_SCAN_DEPTH = 8
TEXT_REPORT_RE = re.compile(
    r"(?im)^[ \t]{0,4}(?:\*\*)?report[ \t]*(?:\*\*)?[ \t]*:[ \t]*(\S[^\n]*\.md)[ \t]*$"
)
STATUSES = ("ok", "no-report", "empty-report")


def find_report_candidates(node, depth=0):
    """Strings under report-style keys, document order, top level first."""
    found = []
    if depth > MAX_SCAN_DEPTH:
        return found
    if isinstance(node, dict):
        for key, value in node.items():
            if str(key).strip().lower() in REPORT_KEYS and isinstance(value, str) and value.strip():
                found.append(value.strip())
        for value in node.values():
            found.extend(find_report_candidates(value, depth + 1))
    elif isinstance(node, list):
        for value in node:
            found.extend(find_report_candidates(value, depth + 1))
    return found


def text_report_candidates(text):
    found = []
    for match in TEXT_REPORT_RE.finditer(text):
        candidate = match.group(1).strip().strip("`'\"<>").strip()
        if candidate:
            found.append(candidate)
    return found


def normalize(path, root):
    """Resolve a ledger path to an absolute candidate path under root."""
    path = path.strip()
    if path.startswith("./"):
        path = path[2:]
    root_name = os.path.basename(root.rstrip(os.sep))
    if root_name and (path == root_name or path.startswith(root_name + "/")):
        path = path[len(root_name):].lstrip("/")
    if os.path.isabs(path):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(root, path))


def inside(root, candidate):
    try:
        root_real = os.path.realpath(root)
        cand_real = os.path.realpath(candidate)
        return os.path.commonpath([root_real, cand_real]) == root_real
    except ValueError:
        return False


def classify(path):
    """(status, bytes) for one candidate path; no-report when not a file."""
    try:
        if not os.path.isfile(path):
            return "no-report", None
        size = os.path.getsize(path)
    except OSError:
        return "no-report", None
    if size == 0:
        return "empty-report", 0
    try:
        with open(path, "rb") as handle:
            if size <= 1_048_576:
                data = handle.read()
            else:
                data = handle.read(65_536)
                handle.seek(-4_096, os.SEEK_END)
                data += handle.read()
    except OSError:
        return "no-report", None
    return ("empty-report" if not data.strip() else "ok"), size


def derive_wave_dir(doc):
    round_no = doc.get("round")
    wave = str(doc.get("wave") or "")
    if not round_no or not wave:
        return None
    suffix = wave.split("-")[-1]
    if not suffix:
        return None
    return ".ufo/waves/round-%s/%s" % (round_no, suffix)


def fill_seat(seat, index, root, wave_dir):
    name = seat.get("name")
    if not isinstance(name, str) or not name:
        name = "seat%d" % index
    payload = seat.get("output")
    candidates = []
    if isinstance(payload, (dict, list)):
        candidates.extend(find_report_candidates(payload))
    elif isinstance(payload, str) and payload.strip():
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            candidates.extend(text_report_candidates(payload))
        else:
            if isinstance(parsed, (dict, list)):
                candidates.extend(find_report_candidates(parsed))
    if wave_dir:
        candidates.append(os.path.join(wave_dir, name + ".md"))
    canonical_index = len(candidates) - 1 if wave_dir else None

    chosen_path = None
    source = "canonical"
    status = None
    size = None
    for index_c, candidate in enumerate(candidates):
        path = normalize(candidate, root)
        if not inside(root, path):
            continue
        candidate_source = "canonical" if index_c == canonical_index else "output"
        if chosen_path is None:
            chosen_path, source = path, candidate_source
        candidate_status, candidate_size = classify(path)
        if candidate_status != "no-report":
            chosen_path, source = path, candidate_source
            status, size = candidate_status, candidate_size
            break
    if status is None:
        status = "no-report"
        if chosen_path is None and wave_dir:
            chosen_path = normalize(os.path.join(wave_dir, name + ".md"), root)
            source = "canonical"

    previous = seat.get("status")
    if previous is not None:
        seat["status_previous"] = previous
    seat["status"] = status
    if chosen_path is not None and inside(root, chosen_path):
        seat["report"] = os.path.relpath(chosen_path, root)
    else:
        seat["report"] = chosen_path
    seat["report_bytes"] = size
    seat["report_source"] = source
    return status


def fill(doc, root, wave_dir):
    """Return (copy with statuses, counts). Raises ValueError on a bad ledger."""
    if not isinstance(doc, dict):
        raise ValueError("ledger is not a JSON object")
    seats = doc.get("results")
    if not isinstance(seats, list):
        raise ValueError("ledger has no 'results' list")
    out = copy.deepcopy(doc)
    counts = {status: 0 for status in STATUSES}
    for index, seat in enumerate(out["results"]):
        if not isinstance(seat, dict):
            raise ValueError("results[%d] is not an object" % index)
        counts[fill_seat(seat, index, root, wave_dir)] += 1
    return out, counts


def dump(doc):
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def run_selftest():
    failures = []
    checks = [0]

    def check(label, condition, detail=""):
        checks[0] += 1
        if not condition:
            failures.append("%s%s" % (label, (": " + detail) if detail else ""))

    with tempfile.TemporaryDirectory(prefix="ledger-status-selftest.") as tmp:
        root = os.path.join(tmp, "kaidoku-shokunin")
        wave = "w1"
        wave_dir = os.path.join(root, wave)
        os.makedirs(wave_dir)

        def report(name, body):
            path = os.path.join(wave_dir, name)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(body)
            return path

        report("SeatTop.md", "top\n")
        report("SeatPrefixed.md", "prefixed\n")
        report("SeatEmpty.md", "")
        report("SeatWhitespace.md", "\n\t \n")
        report("SeatCanonical.md", "canonical\n")
        report("SeatText.md", "text trailer\n")
        report("SeatNoOutput.md", "no output\n")
        report("SeatPrevStatus.md", "previous status\n")
        os.makedirs(os.path.join(wave_dir, "nested"))
        report(os.path.join("nested", "SeatNestedOk.md"), "nested\n")

        def out(**fields):
            return json.dumps(fields)

        seats = [
            {"name": "SeatTop", "agent": "executor",
             "output": out(report="./%s/SeatTop.md" % wave, verdict="ok")},
            {"name": "SeatNested", "agent": "executor",
             "output": out(deliverables={"report": "%s/SeatNestedMissing.md" % wave})},
            {"name": "SeatPrefixed", "agent": "executor",
             "output": out(report="kaidoku-shokunin/%s/SeatPrefixed.md" % wave)},
            {"name": "SeatEmpty", "agent": "executor",
             "output": out(report="%s/SeatEmpty.md" % wave)},
            {"name": "SeatWhitespace", "agent": "executor",
             "output": out(report="%s/SeatWhitespace.md" % wave)},
            {"name": "SeatCanonical", "agent": "executor",
             "output": out(verdict="canonical only")},
            {"name": "SeatAbsOutside", "agent": "executor",
             "output": out(report="/etc/hostname")},
            {"name": "SeatText", "agent": "executor",
             "output": "verdict: CONFIRMED\nReport: %s/SeatText.md\n" % wave},
            {"name": "SeatNoOutput", "agent": "executor", "output": ""},
            {"name": "SeatNoOutput2", "agent": "executor", "output": None},
            {"name": "SeatNullStatus", "agent": "executor", "status": None,
             "output": out(deliverables={"report_path": "%s/nested/SeatNestedOk.md" % wave})},
            {"name": "SeatPrevStatus", "agent": "executor", "status": "stale",
             "output": out(verdict="recomputed")},
        ]
        ledger = {"lane": "kaidoku", "round": 39, "wave": "r39-w1",
                  "seats": len(seats), "results": seats}
        ledger_path = os.path.join(root, "results.json")
        with open(ledger_path, "w", encoding="utf-8") as handle:
            handle.write(dump(ledger))
        before = open(ledger_path, "rb").read()

        filled, counts = fill(json.loads(before.decode("utf-8")), root, wave)
        got = {seat["name"]: seat for seat in filled["results"]}

        expected = {
            "SeatTop": ("ok", "output"),
            "SeatNested": ("no-report", "output"),
            "SeatPrefixed": ("ok", "output"),
            "SeatEmpty": ("empty-report", "output"),
            "SeatWhitespace": ("empty-report", "output"),
            "SeatCanonical": ("ok", "canonical"),
            "SeatAbsOutside": ("no-report", "canonical"),
            "SeatText": ("ok", "output"),
            "SeatNoOutput": ("ok", "canonical"),
            "SeatNoOutput2": ("no-report", "canonical"),
            "SeatNullStatus": ("ok", "output"),
            "SeatPrevStatus": ("ok", "canonical"),
        }
        for name, (status, source) in expected.items():
            seat = got[name]
            check("%s:status" % name, seat["status"] == status, repr(seat["status"]))
            check("%s:source" % name, seat["report_source"] == source, repr(seat["report_source"]))
        check("counts", counts == {"ok": 7, "no-report": 3, "empty-report": 2}, repr(counts))
        check("empty bytes", got["SeatEmpty"]["report_bytes"] == 0)
        check("ok bytes", got["SeatTop"]["report_bytes"] == 4)
        check("no-report bytes", got["SeatNested"]["report_bytes"] is None)
        check("nested report key", got["SeatNullStatus"]["report"] == "w1/nested/SeatNestedOk.md",
              repr(got["SeatNullStatus"]["report"]))
        check("canonical path", got["SeatNoOutput"]["report"] == "w1/SeatNoOutput.md")
        check("outside path not adopted",
              not str(got["SeatAbsOutside"]["report"]).startswith("/etc/"), repr(got["SeatAbsOutside"]["report"]))
        check("null status no previous", "status_previous" not in got["SeatNullStatus"])
        check("previous preserved", got["SeatPrevStatus"].get("status_previous") == "stale")
        check("input untouched", open(ledger_path, "rb").read() == before)
        check("copy keeps fields",
              all(k in got["SeatTop"] for k in ("name", "agent", "output", "status")))
        check("no seats mutated in source doc",
              all("status" not in seat or seat["status"] is None for seat in json.loads(before.decode())["results"]
                  if seat["name"] != "SeatPrevStatus"))

        # Bad-ledger and missing-wave-dir behaviour.
        try:
            fill({"results": "nope"}, root, wave)
        except ValueError:
            check("bad ledger raises", True)
        else:
            check("bad ledger raises", False)
        no_wave, no_wave_counts = fill(json.loads(before.decode()), root, None)
        check("no wave dir: canonical fallback gone",
              {s['name']: s['status'] for s in no_wave["results"]}["SeatCanonical"] == "no-report")

        # CLI arm: writes a copy, leaves the input alone, summary on stderr.
        out_path = os.path.join(tmp, "filled.json")
        import subprocess
        proc = subprocess.run(
            [sys.executable, "-B", os.path.abspath(__file__), ledger_path,
             "--root", root, "--wave-dir", wave, "--out", out_path],
            capture_output=True, text=True)
        check("cli exit", proc.returncode == 0, proc.stderr)
        check("cli summary", "ok=7" in proc.stderr and "no-report=3" in proc.stderr
              and "empty-report=2" in proc.stderr, repr(proc.stderr))
        check("cli wrote file", os.path.isfile(out_path))
        cli_doc = json.load(open(out_path, encoding="utf-8"))
        check("cli statuses", {s["name"]: s["status"] for s in cli_doc["results"]}["SeatEmpty"] == "empty-report")
        check("cli input untouched", open(ledger_path, "rb").read() == before)

    total = checks[0]
    print("ledger-status selftest: %d/%d checks pass" % (total - len(failures), total))
    for failure in failures:
        print("FAIL " + failure)
    return 1 if failures else 0


def main(argv):
    parser = argparse.ArgumentParser(
        description="Fill per-seat ok/no-report/empty-report status into a copy of a wave results ledger.")
    parser.add_argument("results", nargs="?", help="wave results.json to read (never modified)")
    parser.add_argument("--root", default=None, help="lane root for report lookup (default: cwd)")
    parser.add_argument("--wave-dir", default=None,
                        help="report directory relative to --root (default: derived .ufo/waves/round-<round>/<w1|w2>)")
    parser.add_argument("--out", default=None, help="write the filled copy here (default: stdout)")
    parser.add_argument("--selftest", action="store_true", help="run built-in checks")
    args = parser.parse_args(argv)

    if args.selftest:
        return run_selftest()
    if not args.results:
        parser.error("RESULTS.json is required unless --selftest")

    root = os.path.abspath(args.root or os.getcwd())
    try:
        with open(args.results, "r", encoding="utf-8") as handle:
            doc = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        print("ledger-status: cannot read ledger: %s" % error, file=sys.stderr)
        return 2
    wave_dir = args.wave_dir
    if wave_dir is None:
        wave_dir = derive_wave_dir(doc)
    if wave_dir is not None and not os.path.isdir(normalize(wave_dir, root)):
        print("ledger-status: warning: wave dir not found under root: %s" % wave_dir, file=sys.stderr)
    try:
        filled, counts = fill(doc, root, wave_dir)
    except ValueError as error:
        print("ledger-status: %s" % error, file=sys.stderr)
        return 2

    text = dump(filled)
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as handle:
                handle.write(text)
        except OSError as error:
            print("ledger-status: cannot write %s: %s" % (args.out, error), file=sys.stderr)
            return 2
    else:
        sys.stdout.write(text)
    print("ledger-status: %d seats ok=%d no-report=%d empty-report=%d (wave_dir=%s)"
          % (len(filled["results"]), counts["ok"], counts["no-report"],
             counts["empty-report"], wave_dir), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
