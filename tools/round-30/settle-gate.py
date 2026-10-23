#!/usr/bin/env python3
"""Seat-settlement gate (round-30; round-29 routed defect 4, lesson M29-1).

A round may be filed only after every seat it dispatched has settled, and no
tool checked that. Round 28 was filed while a seat was still running: the seat
rewrote its report (`.ufo/waves/round-28/a2w/ExecR27SelftestFix.md`) after the
filing commit `242b0d8b`, so a tree-clean check alone cannot see it (at the
round-29 start `git status --porcelain` printed ` M` on that path; on a clean
clone at `242b0d8b` the tree step passes). This gate compares the round's own
settlement ledger against the registry member lists and the report bytes on
disk:

  registries  every `.ufo/waves/round-<N>/*/swarm-registry.json` member list
              (the dispatched seats). The registry's `reportDir` names the
              wave's report directory; when absent, the registry's own
              directory is used. A member's report is `<reportDir>/<name>.md`.
  ledger      `.ufo/waves/round-<N>/settle.tsv`, one row per dispatched seat:

                name<TAB>status<TAB>utc<TAB>report_sha256[<TAB>note]

              A header line is required; columns are read by header name, so
              order is free and unknown columns are ignored. `status` is
              `returned`, `cancelled` or `dead`. `utc` is the settlement time
              (ISO-8601 Zulu). `report_sha256` is the sha256 of the member's
              report bytes as settled, `-` when the seat left no report (a
              `returned` row must carry a sha256). `note` (optional 5th
              column) records why a cancelled/dead seat left a report behind.
              A row key is the bare member name, or `<wave>/<name>` (the wave
              is the registry's directory name, e.g. `w1`) when the round
              re-used a name across waves; a bare key for a name that appears
              in more than one registry is ambiguous and refused (exit 2).
              Blank lines and lines starting with `#` are ignored.

Findings (exit 1):
  MISSING_LEDGER       the ledger file does not exist, so nothing is settled
  MISSING_ROW          a registry member has no ledger row
  REPORT_ABSENT        a returned member's report file is absent
  REPORT_SHA_MISMATCH  a returned member's report bytes differ from the
                       settled sha256 (a seat that rewrote its report after
                       settling)
  REPORT_WITHOUT_NOTE  a cancelled/dead member left a report and its row
                       carries no note

A ledger row that settles no registry member prints `WARN STRAY_ROW` and does
not fail the gate. Exit: 0 when there are no findings; 1 when there are; 2 on
usage errors or when the input cannot be evaluated (round directory absent,
no registry, unreadable/malformed registry or ledger: unknown status,
malformed sha256 or utc, duplicate row key, ambiguous bare row key).

Limits: the ledger is author-written; the gate checks that it agrees with the
bytes on disk, not that a settlement was honest, and it reads the working tree
only, so a report rewritten after the gate run is not caught - run it last,
immediately before the filing commit, like prefile-check.sh. Timestamps are
recorded, not authenticated. `--selftest` builds its fixtures under TMPDIR and
needs no lane.
"""
import argparse
import hashlib
import io
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

STATUSES = ("returned", "cancelled", "dead")
REQUIRED = ("name", "status", "utc", "report_sha256")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")
ROUND_RE = re.compile(r"^round-\d+$")


class Unevaluable(Exception):
    """Input the gate cannot evaluate (exit 2)."""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_registries(root, rnd):
    """Return (round_dir, [registry dicts]); registry = wave, path, members,
    report_dir. Raises Unevaluable."""
    base = root / ".ufo" / "waves" / rnd
    if not base.is_dir():
        raise Unevaluable("round directory absent: %s" % base.relative_to(root))
    regs = []
    for path in sorted(base.glob("*/swarm-registry.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError) as e:
            raise Unevaluable("registry unreadable: %s (%s)" % (path.relative_to(root), e))
        members = data.get("members")
        if not isinstance(members, dict) or not all(isinstance(k, str) for k in members):
            raise Unevaluable("registry members is not an object of names: %s" % path.relative_to(root))
        report_dir = path.parent
        if data.get("reportDir") is not None:
            cand = (root / str(data["reportDir"])).resolve()
            try:
                cand.relative_to(root)
            except ValueError:
                raise Unevaluable("reportDir escapes the root: %s" % data["reportDir"])
            report_dir = cand
        regs.append({"wave": path.parent.name, "path": path,
                     "members": list(members), "report_dir": report_dir})
    if not regs:
        raise Unevaluable("no swarm-registry.json under %s" % base.relative_to(root))
    return base, regs


def read_ledger(root, base):
    """Return (ledger path relative to root, rows or None). Raises
    Unevaluable. rows maps key -> row dict."""
    path = base / "settle.tsv"
    rel = path.relative_to(root)
    if not path.is_file():
        return rel, None
    try:
        lines = [l for l in path.read_text().splitlines()
                 if l.strip() and not l.startswith("#")]
    except OSError as e:
        raise Unevaluable("ledger unreadable: %s (%s)" % (rel, e))
    if not lines:
        raise Unevaluable("ledger has no header: %s" % rel)
    cols = [c.strip() for c in lines[0].split("\t")]
    for want in REQUIRED:
        if want not in cols:
            raise Unevaluable("ledger header lacks %r: %s" % (want, rel))
    at = {c: i for i, c in enumerate(cols)}
    rows = {}
    for n, line in enumerate(lines[1:], start=2):
        fields = line.split("\t")
        if len(fields) > len(cols):
            raise Unevaluable("ledger row %d has %d fields, header has %d" % (n, len(fields), len(cols)))
        fields += [""] * (len(cols) - len(fields))
        row = {c: fields[i].strip() for c, i in at.items()}
        name = row["name"]
        if not name:
            raise Unevaluable("ledger row %d has no name" % n)
        if name in rows:
            raise Unevaluable("duplicate ledger row for %s" % name)
        if row["status"] not in STATUSES:
            raise Unevaluable("ledger row %d: status %r not in %s" % (n, row["status"], "|".join(STATUSES)))
        if not UTC_RE.match(row["utc"]):
            raise Unevaluable("ledger row %d: utc %r is not ISO-8601 Zulu" % (n, row["utc"]))
        sha = row["report_sha256"].lower()
        if sha in ("", "-"):
            sha = None
        elif not SHA256_RE.match(sha):
            raise Unevaluable("ledger row %d: report_sha256 %r is not a sha256" % (n, row["report_sha256"]))
        if row["status"] == "returned" and sha is None:
            raise Unevaluable("ledger row %d: returned row for %s records no report_sha256" % (n, name))
        note = row.get("note", "")
        row["sha"] = sha
        row["note_present"] = bool(note) and note != "-"
        row["line"] = n
        rows[name] = row
    return rel, rows


def check(root, rnd, out=sys.stdout):
    root = Path(root).resolve()
    if not root.is_dir():
        print("settle: ERROR root is not a directory: %s" % root, file=out)
        return 2
    try:
        base, regs = read_registries(root, rnd)
        ledger_rel, rows = read_ledger(root, base)
    except Unevaluable as e:
        print("settle: ERROR %s" % e, file=out)
        return 2
    members = []
    index = {}
    for reg in regs:
        for name in reg["members"]:
            members.append((reg["wave"], name, reg["report_dir"]))
            index.setdefault(name, []).append(reg["wave"])
    members.sort(key=lambda t: (t[0], t[1]))
    print("settle: %s root=%s registries=%d members=%d ledger=%s rows=%d" % (
        rnd, root, len(regs), len(members), ledger_rel, 0 if rows is None else len(rows)), file=out)
    findings = []
    used = set()
    if rows is None:
        findings.append(("MISSING_LEDGER", str(ledger_rel)))
    else:
        for wave, name, report_dir in members:
            qual = "%s/%s" % (wave, name)
            row = None
            if qual in rows:
                row = rows[qual]
                used.add(qual)
            elif name in rows:
                if len(index[name]) > 1:
                    print("settle: ERROR row key %r is ambiguous (%s); qualify it as %s" % (
                        name, " ".join(sorted(index[name])), qual), file=out)
                    return 2
                row = rows[name]
                used.add(name)
            if row is None:
                findings.append(("MISSING_ROW", qual))
                continue
            report = report_dir / (name + ".md")
            rel_report = report.relative_to(root)
            exists = report.is_file()
            if row["status"] == "returned":
                got = None
                if exists:
                    try:
                        got = sha256_file(report)
                    except OSError as e:
                        findings.append(("REPORT_ABSENT", "%s status=returned unreadable=%s" % (qual, e)))
                        continue
                if got is None:
                    findings.append(("REPORT_ABSENT", "%s status=returned report=%s" % (qual, rel_report)))
                elif got != row["sha"]:
                    findings.append(("REPORT_SHA_MISMATCH", "%s ledger=%s file=%s" % (qual, row["sha"], got)))
            elif exists and not row["note_present"]:
                findings.append(("REPORT_WITHOUT_NOTE", "%s status=%s report=%s" % (qual, row["status"], rel_report)))
    for key in sorted(set(rows) - used) if rows else []:
        print("settle: WARN STRAY_ROW %s" % key, file=out)
    for code, detail in findings:
        print("settle: %s %s" % (code, detail), file=out)
    if findings:
        print("settle: FAIL (%d findings)" % len(findings), file=out)
        return 1
    print("settle: PASS", file=out)
    return 0


HEADER = "name\tstatus\tutc\treport_sha256\tnote\n"


def row(key, status, utc, sha=None, note=None):
    fields = [key, status, utc, sha if sha else "-"]
    if note is not None:
        fields.append(note)
    return "\t".join(fields) + "\n"


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _fixture(base, rnd, waves, reports, ledger):
    for wave, names in waves.items():
        wd = base / ".ufo" / "waves" / rnd / wave
        wd.mkdir(parents=True, exist_ok=True)
        (wd / "swarm-registry.json").write_text(json.dumps({
            "schema": "ufo-swarm-registry-v1", "wave": "fixture-" + wave,
            "createdAt": "2026-10-22T00:00:00.000Z", "updatedAt": "2026-10-22T00:00:00.000Z",
            "reportDir": ".ufo/waves/%s/%s" % (rnd, wave),
            "members": {n: {"kind": "spawn", "agentId": None, "role": "executor", "item": None}
                        for n in names}}))
    for (wave, name), text in reports.items():
        (base / ".ufo" / "waves" / rnd / wave / (name + ".md")).write_text(text)
    if ledger is not None:
        (base / ".ufo" / "waves" / rnd / "settle.tsv").write_text(ledger)


def selftest():
    """Fixtures for every finding and error path, including the round-28 shape
    (`.ufo/waves/round-28/a2w/ExecR27SelftestFix.md` was committed in the
    filing commit `242b0d8b`, sha256 fcb8e28061bcdacae2daa7702c134bb754a6fc44
    10496705e39ee928c47705e5, and rewritten after it, sha256 7ed676593a0b3c85
    719eb6718ea454d2bae4d29422256d59b49c38c8dfa960bb; the fixture reproduces
    that shape with its own bytes)."""
    fails = 0
    root = Path(tempfile.mkdtemp(prefix="settle-gate-selftest-"))
    utc = "2026-10-22T19:25:35Z"
    report_a = "ExecA report\n"
    report_c = "CriticC late report\n"
    cases = []

    def case(name, want, want_code, rnd, waves, reports, ledger):
        cases.append((name, want, want_code, rnd, waves, reports, ledger))

    case("green-clean", 0, "settle: PASS", "round-99",
         {"w1": ["ExecA", "ScribeB", "CriticC"]},
         {("w1", "ExecA"): report_a, ("w1", "CriticC"): report_c},
         HEADER + row("ExecA", "returned", utc, _sha(report_a))
         + row("ScribeB", "cancelled", utc)
         + row("CriticC", "dead", utc, _sha(report_c), "post-stop bytes, committed as evidence"))
    case("red-missing-row", 1, "MISSING_ROW w1/ScoutD", "round-99",
         {"w1": ["ExecA", "ScoutD"]},
         {("w1", "ExecA"): report_a},
         HEADER + row("ExecA", "returned", utc, _sha(report_a)))
    case("red-returned-report-absent", 1, "REPORT_ABSENT w1/ExecA", "round-99",
         {"w1": ["ExecA"]}, {},
         HEADER + row("ExecA", "returned", utc, _sha(report_a)))
    # round-28 shape: the ledger carries the settled (filing-time) bytes; the
    # file on disk is the later rewrite.
    filed = "ExecR27SelftestFix report\nround-28 wave 1 run at 19:25:35Z\n"
    later = filed + "rerun at 19:26:31Z after the stop\n"
    crit = "CriticMistakes report\n"
    case("red-r28-report-changed-after-filing", 1, "REPORT_SHA_MISMATCH a2w/ExecR27SelftestFix", "round-28",
         {"a2w": ["ExecR27SelftestFix", "CriticMistakes"]},
         {("a2w", "ExecR27SelftestFix"): later, ("a2w", "CriticMistakes"): crit},
         HEADER + row("ExecR27SelftestFix", "returned", utc, _sha(filed))
         + row("CriticMistakes", "returned", utc, _sha(crit)))
    case("red-cancelled-report-without-note", 1, "REPORT_WITHOUT_NOTE w1/CriticC", "round-99",
         {"w1": ["CriticC"]}, {("w1", "CriticC"): report_c},
         HEADER + row("CriticC", "cancelled", utc, _sha(report_c)))
    case("green-cancelled-report-with-note", 0, "settle: PASS", "round-99",
         {"w1": ["CriticC"]}, {("w1", "CriticC"): report_c},
         HEADER + row("CriticC", "cancelled", utc, _sha(report_c), "stopped after its report landed"))
    case("red-no-ledger", 1, "MISSING_LEDGER", "round-99",
         {"w1": ["ExecA"]}, {("w1", "ExecA"): report_a}, None)
    r1, r2 = "ScribeRegistry w1 report\n", "ScribeRegistry w2 report\n"
    case("green-qualified-keys-two-waves", 0, "settle: PASS", "round-99",
         {"w1": ["ScribeRegistry"], "w2": ["ScribeRegistry"]},
         {("w1", "ScribeRegistry"): r1, ("w2", "ScribeRegistry"): r2},
         HEADER + row("w1/ScribeRegistry", "returned", utc, _sha(r1))
         + row("w2/ScribeRegistry", "returned", utc, _sha(r2)))
    case("error-ambiguous-bare-key", 2, "is ambiguous", "round-99",
         {"w1": ["ScribeRegistry"], "w2": ["ScribeRegistry"]},
         {("w1", "ScribeRegistry"): r1, ("w2", "ScribeRegistry"): r2},
         HEADER + row("ScribeRegistry", "returned", utc, _sha(r1)))
    case("error-bad-status", 2, "status", "round-99",
         {"w1": ["ExecA"]}, {("w1", "ExecA"): report_a},
         HEADER + row("ExecA", "done", utc, _sha(report_a)))
    case("error-bad-sha", 2, "not a sha256", "round-99",
         {"w1": ["ExecA"]}, {("w1", "ExecA"): report_a},
         HEADER + row("ExecA", "returned", utc, "abc123"))
    case("error-duplicate-row", 2, "duplicate ledger row", "round-99",
         {"w1": ["ExecA"]}, {("w1", "ExecA"): report_a},
         HEADER + row("ExecA", "returned", utc, _sha(report_a))
         + row("ExecA", "cancelled", utc))
    case("green-stray-row-warns", 0, "WARN STRAY_ROW Ghost", "round-99",
         {"w1": ["ExecA"]}, {("w1", "ExecA"): report_a},
         HEADER + row("ExecA", "returned", utc, _sha(report_a))
         + row("Ghost", "cancelled", utc))

    for name, want, want_code, rnd, waves, reports, ledger in cases:
        base = root / name
        base.mkdir()
        _fixture(base, rnd, waves, reports, ledger)
        buf = io.StringIO()
        got = check(base, rnd, out=buf)
        text = buf.getvalue()
        ok = got == want and want_code in text
        fails += not ok
        print("%s %s got=%d want=%d code=%r" % ("ok" if ok else "FAIL", name, got, want,
              want_code if want_code in text else "<absent>"))
        if not ok:
            print(text, end="")
    print("selftest cases=%d failures=%d" % (len(cases), fails))
    if fails == 0:
        shutil.rmtree(root)
    else:
        print("selftest fixtures kept at %s" % root)
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--round", dest="rnd")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.root:
        ap.error("--root required")
    if not a.rnd:
        ap.error("--round required")
    value = a.rnd.strip()
    if value.isdigit():
        value = "round-" + value
    if not ROUND_RE.match(value):
        ap.error("--round takes N or round-N, not %r" % a.rnd)
    sys.exit(check(a.root, value))


if __name__ == "__main__":
    main()
