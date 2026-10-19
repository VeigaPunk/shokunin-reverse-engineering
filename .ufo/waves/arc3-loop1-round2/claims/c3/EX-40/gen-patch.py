#!/usr/bin/env python3
"""EX-40 scratch patch generator: derives the hardened copy from the landed bytes.

Reads the untouched copy at /var/tmp/ex40/patched/custody-pair.py (byte copy of
.ufo/gates/custody-pair/custody-pair.py at sha 112d01dc…), applies exact-string
replacements, writes /var/tmp/ex40/patched/custody-pair.patched.py, and the
caller diffs the two into the patch-text artifact. Fails loudly if any anchor is
not found exactly once (so a re-revision of the tool cannot silently mismatch).
"""
import sys

SRC = "/var/tmp/ex40/patched/custody-pair.py"
DST = "/var/tmp/ex40/patched/custody-pair.patched.py"

REPS = []

REPS.append((
    """    13  ABSENT            >=1 reference path missing on the candidate side
    2   USAGE             bad arguments, unreadable/unparsable receipt, refused
                          or failed write
    3   SELFTEST-FAIL     a selftest case failed

    capture exits 0 when every requested path is present (5/5 for the default
    set) and 13 when >=1 requested path is absent; the receipt is still written.

SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > ABSENT > REWRITE-DRIFT >
METADATA-DRIFT > MATCH.""",
    """    13  ABSENT            >=1 reference path missing on the candidate side
    14  UNEVALUABLE       a path exists but could not be evaluated (EACCES on
                          open, or a stat error other than ENOENT); the receipt
                          is still written, carrying STAT-ERROR/READ-ERROR
    2   USAGE             bad arguments, unreadable/unparsable receipt, refused
                          or failed write
    3   SELFTEST-FAIL     a selftest case failed

    capture exits 0 when every requested path is present (5/5 for the default
    set), 14 when >=1 path is present-but-unevaluable, else 13 when >=1
    requested path is absent; the receipt is still written.

SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > UNEVALUABLE > ABSENT >
REWRITE-DRIFT > METADATA-DRIFT > MATCH."""))

REPS.append((
    """EXIT_ABSENT = 13
EXIT_USAGE = 2""",
    """EXIT_ABSENT = 13
EXIT_UNEVALUABLE = 14
EXIT_USAGE = 2"""))

REPS.append((
    """    "ABSENT": 3,
    "CONTENT-DRIFT": 4,
}""",
    """    "ABSENT": 3,
    "UNEVALUABLE": 4,
    "CONTENT-DRIFT": 5,
}"""))

REPS.append((
    """    "ABSENT": EXIT_ABSENT,
    "CONTENT-DRIFT": EXIT_CONTENT_DRIFT,
}""",
    """    "ABSENT": EXIT_ABSENT,
    "UNEVALUABLE": EXIT_UNEVALUABLE,
    "CONTENT-DRIFT": EXIT_CONTENT_DRIFT,
}"""))

REPS.append((
    """    elif os.path.isfile(path):
        fields["type"] = "file"
        fields["sha256"] = sha256_file(path)""",
    """    elif os.path.isfile(path):
        fields["type"] = "file"
        try:
            fields["sha256"] = sha256_file(path)
        except OSError as exc:  # exists but not evaluable (e.g. EACCES)
            fields["read_error"] = "%s" % exc"""))

REPS.append((
    """        lines.append("SIZE: %s" % sec.get("size", ""))
        if "sha256" in sec:
            lines.append("SHA256: %s" % sec["sha256"])""",
    """        lines.append("SIZE: %s" % sec.get("size", ""))
        if sec.get("read_error"):
            lines.append("READ-ERROR: %s" % sec["read_error"])
        if "sha256" in sec:
            lines.append("SHA256: %s" % sec["sha256"])"""))

REPS.append((
    """    present = sum(1 for s in sections if s.get("exists") == "yes")
    exit_code = EXIT_MATCH if present == len(sections) else EXIT_ABSENT""",
    """    present = sum(1 for s in sections if s.get("exists") == "yes")
    unevaluable = sum(1 for s in sections
                      if s.get("stat_error") or s.get("read_error")
                      or (s.get("exists") == "yes" and s.get("type") == "file" and "sha256" not in s))
    if unevaluable:
        exit_code = EXIT_UNEVALUABLE
    elif present == len(sections):
        exit_code = EXIT_MATCH
    else:
        exit_code = EXIT_ABSENT"""))

REPS.append((
    """    print("CUSTODY_PAIR_CAPTURE: %s paths=%d/%d label=%s exit=%d"
          % ("OK" if exit_code == EXIT_MATCH else "PARTIAL", present, len(sections),
             args.label or "(none)", exit_code))""",
    """    state = {EXIT_MATCH: "OK", EXIT_UNEVALUABLE: "UNEVALUABLE"}.get(exit_code, "PARTIAL")
    print("CUSTODY_PAIR_CAPTURE: %s paths=%d/%d label=%s exit=%d"
          % (state, present, len(sections), args.label or "(none)", exit_code))"""))

REPS.append((
    """    comparable = sum(1 for k in COMPARE_KEYS if k in ref and k in cand)
    if not ref_exists and not cand_exists:""",
    """    comparable = sum(1 for k in COMPARE_KEYS if k in ref and k in cand)
    ref_uneval = bool(ref.get("stat_error") or ref.get("read_error"))
    cand_uneval = bool(cand.get("stat_error") or cand.get("read_error"))
    if ref_uneval or cand_uneval:
        sides = "+".join(n for n, u in (("reference", ref_uneval), ("candidate", cand_uneval)) if u)
        return {"finding": "UNEVALUABLE", "moved": ["unevaluable"], "compared": 0,
                "comparable": comparable,
                "notes": notes + ["exists but not evaluable on %s side" % sides],
                "label_findings": label_findings}
    if not ref_exists and not cand_exists:"""))

REPS.append((
    """        fmt = "v2" if any("mtime_epoch" in s for s in sections) else "v1-stanza\"""",
    """        fmt = "v2" if (version >= 2 or any("mtime_epoch" in s for s in sections)) else "v1-stanza\""""))

REPS.append((
    """    run_case(cases, "refuses-to-write-over-custody-path", case_guard)

    passed = sum(1 for _, ok, _ in cases if ok)""",
    """    run_case(cases, "refuses-to-write-over-custody-path", case_guard)

    # 13. exists-but-unreadable path: declared UNEVALUABLE, receipt kept, no crash
    def case_unreadable():
        if os.geteuid() == 0:
            return  # mode 000 does not block root; the case is not meaningful
        bad = root / "unreadable.conf"
        bad.write_bytes(b"x\\n")
        os.chmod(bad, 0)
        out = root / "unreadable.txt"
        rc = cmd_capture(argparse.Namespace(out=str(out), paths=[str(bad)], label="selftest"))
        os.chmod(bad, 0o644)
        assert rc == EXIT_UNEVALUABLE, "expected UNEVALUABLE exit %d, got %d" % (EXIT_UNEVALUABLE, rc)
        text = out.read_text()
        assert "READ-ERROR:" in text, "read error not recorded in the receipt"
        assert "EXISTS: yes" in text, "unevaluable path recorded as absent"
    run_case(cases, "unreadable-path-is-unevaluable", case_unreadable)

    # 14. an unevaluable path must never verify as MATCH (fail-open class)
    def case_unevaluable_not_match():
        if os.geteuid() == 0:
            return
        d = root / "blocked"
        d.mkdir()
        inner = d / "inner.conf"
        inner.write_bytes(b"y\\n")
        os.chmod(d, 0)
        out = root / "blocked-receipt.txt"
        rc_cap = cmd_capture(argparse.Namespace(out=str(out), paths=[str(inner)], label="selftest"))
        outv = root / "blocked-verify.out"
        rc_ver = _run_verify([str(out), "--live"], outv)
        os.chmod(d, 0o755)
        assert rc_cap == EXIT_UNEVALUABLE, "expected capture UNEVALUABLE, got %d" % rc_cap
        assert rc_ver == EXIT_UNEVALUABLE, "expected verify UNEVALUABLE (fail-closed), got %d" % rc_ver
        assert "UNEVALUABLE" in outv.read_text(), "no UNEVALUABLE class printed"
    run_case(cases, "unevaluable-never-matches", case_unevaluable_not_match)

    passed = sum(1 for _, ok, _ in cases if ok)"""))


def main():
    src = open(SRC, encoding="utf-8").read()
    for i, (old, new) in enumerate(REPS, 1):
        n = src.count(old)
        if n != 1:
            print("ANCHOR %d not unique: %d occurrences\n---\n%s\n---" % (i, n, old[:200]), file=sys.stderr)
            return 1
        src = src.replace(old, new)
    with open(DST, "w", encoding="utf-8") as fh:
        fh.write(src)
    print("patched copy written: %s (%d replacements applied)" % (DST, len(REPS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
