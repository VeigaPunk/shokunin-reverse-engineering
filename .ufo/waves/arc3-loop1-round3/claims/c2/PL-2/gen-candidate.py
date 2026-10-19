#!/usr/bin/env python3
"""PL-2 (arc3-loop1-round3, chain c2): generate the custody-pair hardening candidate.

Every transformation asserts its anchor occurs EXACTLY ONCE in the base file, so
a moved base cannot silently mis-apply. Base: the round-2 landed revision
sha256 112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa, 889 lines.
"""
import hashlib
import sys
from pathlib import Path

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else "/var/tmp/pl2/before/custody-pair.py")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "/var/tmp/pl2/after/custody-pair.py")

T = []  # (name, anchor, replacement)


def tr(name, anchor, repl):
    T.append((name, anchor, repl))


# ---- H1 docstring: exit class 14 + precedence (EX-40's declared class) --------
tr("H1a-docstring-exit-14", """    13  ABSENT            >=1 reference path missing on the candidate side
    2   USAGE             bad arguments, unreadable/unparsable receipt, refused""",
   """    13  ABSENT            >=1 reference path missing on the candidate side
    14  UNEVALUABLE       a path exists but could not be evaluated (EACCES on
                          open, or a stat error other than ENOENT); the receipt
                          is still written, carrying STAT-ERROR/READ-ERROR
    2   USAGE             bad arguments, unreadable/unparsable receipt, refused""")

tr("H1b-docstring-capture-exit", """    capture exits 0 when every requested path is present (5/5 for the default
    set) and 13 when >=1 requested path is absent; the receipt is still written.

SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > ABSENT > REWRITE-DRIFT >
METADATA-DRIFT > MATCH.""",
   """    capture exits 0 when every requested path is present (5/5 for the default
    set), 14 when >=1 path is present-but-unevaluable, else 13 when >=1
    requested path is absent; the receipt is still written.

SEVERITY PRECEDENCE (verify): CONTENT-DRIFT > UNEVALUABLE > ABSENT >
REWRITE-DRIFT > METADATA-DRIFT > MATCH.""")

tr("H1c-docstring-require-paths", """v1 COMPATIBILITY. Three v1 receipt shapes are parsed and compared on the fields""",
   """PARTIAL-REFERENCE GATE (D3). `verify --require-paths N` exits 2 (USAGE) when
the reference receipt carries fewer than N path stanzas, printing
`REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: ...` — a
1-of-5 reference can no longer verify clean while 4 custody paths go
unexamined. Without the flag the comparison covers exactly the reference's
paths, as before (the fixture and v1 workflows are unchanged).

v1 COMPATIBILITY. Three v1 receipt shapes are parsed and compared on the fields""")

# ---- H2 constants ------------------------------------------------------------
tr("H2a-exit-constant", """EXIT_ABSENT = 13
EXIT_USAGE = 2""",
   """EXIT_ABSENT = 13
EXIT_UNEVALUABLE = 14
EXIT_USAGE = 2""")

tr("H2b-severity", """    "ABSENT": 3,
    "CONTENT-DRIFT": 4,
}""",
   """    "ABSENT": 3,
    "UNEVALUABLE": 4,
    "CONTENT-DRIFT": 5,
}""")

tr("H2c-exit-for", """    "ABSENT": EXIT_ABSENT,
    "CONTENT-DRIFT": EXIT_CONTENT_DRIFT,
}""",
   """    "ABSENT": EXIT_ABSENT,
    "UNEVALUABLE": EXIT_UNEVALUABLE,
    "CONTENT-DRIFT": EXIT_CONTENT_DRIFT,
}""")

# ---- H3 capture_path: unreadable file is recorded, never a crash -------------
tr("H3-capture-read-error", """    elif os.path.isfile(path):
        fields["type"] = "file"
        fields["sha256"] = sha256_file(path)""",
   """    elif os.path.isfile(path):
        fields["type"] = "file"
        try:
            fields["sha256"] = sha256_file(path)
        except OSError as exc:  # exists but not evaluable (e.g. EACCES)
            fields["read_error"] = "%s" % exc""")

# ---- H4 render: READ-ERROR line ---------------------------------------------
tr("H4-render-read-error", """        lines.append("TYPE: %s" % sec.get("type", "other"))
        lines.append("SIZE: %s" % sec.get("size", ""))
        if "sha256" in sec:""",
   """        lines.append("TYPE: %s" % sec.get("type", "other"))
        lines.append("SIZE: %s" % sec.get("size", ""))
        if sec.get("read_error"):
            lines.append("READ-ERROR: %s" % sec["read_error"])
        if "sha256" in sec:""")

# ---- H5 parser: READ-ERROR/STAT-ERROR become load-bearing (the parsed-receipt
#      fail-open this plan closes: EX-40's patch alone leaves it open) --------
tr("H5a-key-patterns", """    "inode": re.compile(r"^INODE:\\s*(\\d+)\\s*$", re.M),""",
   """    "inode": re.compile(r"^INODE:\\s*(\\d+)\\s*$", re.M),
    "stat_error": re.compile(r"^STAT-ERROR:\\s*(.+?)\\s*$", re.M),
    "read_error": re.compile(r"^READ-ERROR:\\s*(.+?)\\s*$", re.M),""")

tr("H5b-parse-keys", """    for key in ("type", "size", "sha256", "mtime_epoch", "mtime_ns", "mtime_utc_render",
                "mtime_utc_v1", "ctime_epoch", "ctime_ns", "ctime_utc_v1", "inode"):""",
   """    for key in ("type", "size", "sha256", "mtime_epoch", "mtime_ns", "mtime_utc_render",
                "mtime_utc_v1", "ctime_epoch", "ctime_ns", "ctime_utc_v1", "inode",
                "stat_error", "read_error"):""")

# ---- H6 format tag honors the receipt-version header ------------------------
tr("H6-fmt-tag", """        fmt = "v2" if any("mtime_epoch" in s for s in sections) else "v1-stanza\"""",
   """        fmt = "v2" if (version >= 2 or any("mtime_epoch" in s for s in sections)) else "v1-stanza\"""")

# ---- H7 compare_section: UNEVALUABLE short-circuits before both-absent MATCH -
tr("H7-compare-unevaluable", """    comparable = sum(1 for k in COMPARE_KEYS if k in ref and k in cand)
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
    if not ref_exists and not cand_exists:""")

# ---- H8 cmd_capture: exit 14, summary state ---------------------------------
tr("H8-capture-exit", """    present = sum(1 for s in sections if s.get("exists") == "yes")
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
        exit_code = EXIT_ABSENT""")

tr("H8b-capture-summary", """    print("CUSTODY_PAIR_CAPTURE: %s paths=%d/%d label=%s exit=%d"
          % ("OK" if exit_code == EXIT_MATCH else "PARTIAL", present, len(sections),
             args.label or "(none)", exit_code))""",
   """    state = {EXIT_MATCH: "OK", EXIT_UNEVALUABLE: "UNEVALUABLE"}.get(exit_code, "PARTIAL")
    print("CUSTODY_PAIR_CAPTURE: %s paths=%d/%d label=%s exit=%d"
          % (state, present, len(sections), args.label or "(none)", exit_code))""")

# ---- H9 write-guard: out must not be any measured path (VZ-4 clobber) -------
tr("H9-guard-union", """        out = Path(args.out).expanduser()
        warn_if_tmp(out)
        if out.resolve() in {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}:
            print("USAGE: refusing to write a receipt over a custody path: %s" % out, file=sys.stderr)
            return EXIT_USAGE""",
   """        out = Path(args.out).expanduser()
        warn_if_tmp(out)
        guarded = {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}
        guarded |= {p.resolve() for p in paths}
        if out.resolve() in guarded:
            print("USAGE: refusing to write a receipt over a path it measures: %s" % out, file=sys.stderr)
            return EXIT_USAGE""")

# ---- H9b OPTIONAL (RV-11 F2/D7): inode-arm for hardlink aliases -------------
tr("H9b-guard-inode", """        if out.resolve() in guarded:
            print("USAGE: refusing to write a receipt over a path it measures: %s" % out, file=sys.stderr)
            return EXIT_USAGE""",
   """        def _same_file(a: Path, b: Path) -> bool:
            try:
                sa, sb = os.stat(a), os.stat(b)  # os.stat: a write lands on the symlink target's inode
            except OSError:
                return False
            return (sa.st_dev, sa.st_ino) == (sb.st_dev, sb.st_ino)
        if out.resolve() in guarded or any(_same_file(out, Path(p).expanduser()) for p in paths):
            print("USAGE: refusing to write a receipt over a path it measures (path or inode): %s" % out,
                  file=sys.stderr)
            return EXIT_USAGE""")

# ---- H10 verify: --require-paths coverage gate ------------------------------
tr("H10-cmd-verify-coverage", """    if args.live:
        b_fmt, b_name = "live", "live filesystem"
        b_sections = [capture_path(Path(s["path"]).expanduser()) for s in a_sections]""",
   """    require_paths = getattr(args, "require_paths", None)
    if require_paths:
        have = len(a_sections)
        if have < require_paths:
            a_paths = {Path(s["path"]).expanduser().resolve() for s in a_sections}
            unaccounted = [p for p in CUSTODY_PATHS if Path(p).expanduser().resolve() not in a_paths]
            print("REFERENCE-COVERAGE: %d/%d paths present in reference; unaccounted: %s"
                  % (have, require_paths, ", ".join(unaccounted) if unaccounted else "(none in canonical set)"))
            print("USAGE: reference covers %d of %d required paths" % (have, require_paths), file=sys.stderr)
            return EXIT_USAGE

    if args.live:
        b_fmt, b_name = "live", "live filesystem"
        b_sections = [capture_path(Path(s["path"]).expanduser()) for s in a_sections]""")

# ---- H11 argparse + in-process harness --------------------------------------
tr("H11a-argparse", """    p_ver.add_argument("--live", action="store_true", help="compare receipt_a against the live filesystem")""",
   """    p_ver.add_argument("--live", action="store_true", help="compare receipt_a against the live filesystem")
    p_ver.add_argument("--require-paths", type=int, metavar="N", default=None,
                       help="USAGE exit 2 unless receipt_a carries at least N path stanzas (coverage gate)")""")

tr("H11b-run-verify", """    ns = argparse.Namespace(receipt_a=argv[0], receipt_b=None, live=False)
    for item in argv[1:]:
        if item == "--live":
            ns.live = True
        else:
            ns.receipt_b = item""",
   """    ns = argparse.Namespace(receipt_a=argv[0], receipt_b=None, live=False, require_paths=None)
    rest = [a for a in argv[1:] if a != "--live"]
    if any(a == "--live" for a in argv[1:]):
        ns.live = True
    if "--require-paths" in rest:
        i = rest.index("--require-paths")
        ns.require_paths = int(rest[i + 1])
        del rest[i:i + 2]
    if rest:
        ns.receipt_b = rest[0]""")

# ---- H12 selftest scratch base must pre-exist (D6) --------------------------
tr("H12-scratch-guard", """    if str(base).startswith("/tmp") and not args.scratch:
        print("USAGE: /tmp is excluded scratch (EDQUOT hazard)", file=sys.stderr)
        return EXIT_USAGE
    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))""",
   """    if str(base).startswith("/tmp") and not args.scratch:
        print("USAGE: /tmp is excluded scratch (EDQUOT hazard)", file=sys.stderr)
        return EXIT_USAGE
    if not base.is_dir():
        print("USAGE: scratch base is not a directory: %s" % base, file=sys.stderr)
        return EXIT_USAGE
    root = Path(tempfile.mkdtemp(prefix="custody-pair-selftest-", dir=str(base)))""")

# ---- H13 identity arm: case 7 must exercise the bytes under test -------------
tr("H13-case7-tool-path", """    def case_label():
        src = (Path(__file__).resolve().parent / "custody-pair.py")""",
   """    def case_label():
        src = TOOL_PATH  # the running script, not a same-named neighbour (rule-#14 identity arm)""")

# ---- H14 new selftest cases -------------------------------------------------
NEW_CASES = '''
    # 13. exists-but-unreadable file: declared UNEVALUABLE, receipt kept, no crash
    def case_unreadable():
        if os.geteuid() == 0:
            return  # mode 000 does not block root; the case is not meaningful
        bad = root / "unreadable.conf"
        bad.write_bytes(b"x\\n")
        os.chmod(bad, 0)
        try:
            out = root / "unreadable.txt"
            rc = cmd_capture(argparse.Namespace(out=str(out), paths=[str(bad)], label="selftest"))
        finally:
            os.chmod(bad, 0o644)
        assert rc == EXIT_UNEVALUABLE, "expected UNEVALUABLE exit %d, got %d" % (EXIT_UNEVALUABLE, rc)
        text = out.read_text()
        assert "READ-ERROR:" in text, "read error not recorded in the receipt"
        assert "EXISTS: yes" in text, "unevaluable path recorded as absent"
    run_case(cases, "unreadable-path-is-unevaluable", case_unreadable)

    # 14. an unevaluable path must never verify as MATCH (live fail-open class)
    def case_unevaluable_not_match():
        if os.geteuid() == 0:
            return
        d = root / "blocked"
        d.mkdir()
        inner = d / "inner.conf"
        inner.write_bytes(b"y\\n")
        os.chmod(d, 0)
        try:
            out = root / "blocked-receipt.txt"
            rc_cap = cmd_capture(argparse.Namespace(out=str(out), paths=[str(inner)], label="selftest"))
            outv = root / "blocked-verify.out"
            rc_ver = _run_verify([str(out), "--live"], outv)
        finally:
            os.chmod(d, 0o755)
        assert rc_cap == EXIT_UNEVALUABLE, "expected capture UNEVALUABLE, got %d" % rc_cap
        assert rc_ver == EXIT_UNEVALUABLE, "expected verify UNEVALUABLE (fail-closed), got %d" % rc_ver
        text = outv.read_text()
        assert "UNEVALUABLE" in text, "no UNEVALUABLE class printed"
        assert "VERDICT: MATCH" not in text, "unevaluable path read as MATCH (fail-open)"
    run_case(cases, "unevaluable-never-matches", case_unevaluable_not_match)

    # 15. a PARSED receipt carrying an unreadable stanza must never verify MATCH
    #     (EX-40's patch alone leaves this open: the parser never reads READ-ERROR)
    def case_parsed_unevaluable():
        if os.geteuid() == 0:
            return
        f = root / "parsed-uneval.conf"
        f.write_bytes(b"parsed unevaluable fixture\\n")
        os.chmod(f, 0)
        try:
            hidden, rc_h = capture_to("parsed-hidden.txt", [f])
        finally:
            os.chmod(f, 0o644)
        assert rc_h == EXIT_UNEVALUABLE, "expected capture UNEVALUABLE, got %d" % rc_h
        assert "READ-ERROR:" in hidden.read_text(), "READ-ERROR not rendered into the receipt"
        opened, rc_o = capture_to("parsed-open.txt", [f])
        assert rc_o == EXIT_MATCH, "control capture exit %d" % rc_o
        out = root / "parsed-uneval.out"
        rc = _run_verify([str(hidden), str(opened)], out)
        assert rc == EXIT_UNEVALUABLE, "expected UNEVALUABLE exit %d on a parsed receipt, got %d" % (
            EXIT_UNEVALUABLE, rc)
        assert "VERDICT: MATCH" not in out.read_text(), "parsed unevaluable stanza read as MATCH (fail-open)"
    run_case(cases, "parsed-unevaluable-reference-never-matches", case_parsed_unevaluable)

    # 16. partial reference: declared gate --require-paths N (D3)
    def case_require_paths():
        single = root / "single.conf"
        single.write_bytes(payload)
        os.utime(single, (1000000000, 1000000000))
        rec, rc0 = capture_to("single-pre.txt", [single])
        assert rc0 == EXIT_MATCH, "reference capture exit %d" % rc0
        out_plain = root / "coverage-plain.out"
        rc_plain = _run_verify([str(rec), "--live"], out_plain)
        assert rc_plain == EXIT_MATCH, "declared default (no gate without the flag) broke: exit %d" % rc_plain
        out_gated = root / "coverage-gated.out"
        rc_gated = _run_verify([str(rec), "--live", "--require-paths", "5"], out_gated)
        assert rc_gated == EXIT_USAGE, "expected USAGE exit %d under --require-paths 5, got %d" % (
            EXIT_USAGE, rc_gated)
        text = out_gated.read_text()
        assert "REFERENCE-COVERAGE: 1/5" in text, "REFERENCE-COVERAGE line missing or wrong: %r" % text
    run_case(cases, "partial-reference-require-paths-gate", case_require_paths)

    # 17. write guard covers the scoped paths it measures (the --paths X --out X clobber)
    def case_guard_scope():
        scoped = root / "scoped.conf"
        scoped.write_bytes(b"scoped fixture bytes\\n")
        before = capture_path(scoped)
        rc = cmd_capture(argparse.Namespace(out=str(scoped), paths=[str(scoped)], label="guard-scope"))
        after = capture_path(scoped)
        assert rc == EXIT_USAGE, "expected USAGE refusing --out over a measured path, got %d" % rc
        assert before == after, "the scoped file was clobbered by the receipt it measured"
        assert scoped.read_text() == "scoped fixture bytes\\n", "scoped file bytes changed"
    run_case(cases, "refuses-to-write-over-scoped-path", case_guard_scope)

    # 18. selftest scratch base must pre-exist; missing base is USAGE, not a traceback (D6)
    def case_missing_scratch():
        missing = root / "does-not-exist"
        rc = cmd_selftest(argparse.Namespace(scratch=str(missing)))
        assert rc == EXIT_USAGE, "expected USAGE exit %d for a missing scratch base, got %d" % (EXIT_USAGE, rc)
    run_case(cases, "selftest-missing-scratch-usage-exit", case_missing_scratch)

    # 19. write guard must also refuse a hardlink alias of a measured path (D7/RV-11)
    def case_guard_hardlink():
        a = root / "guard-hardlink-a.conf"
        a.write_bytes(b"guard hardlink fixture\\n")
        b = root / "guard-hardlink-alias.txt"
        os.link(a, b)
        before = capture_path(a)
        rc = cmd_capture(argparse.Namespace(out=str(b), paths=[str(a)], label="guard-inode"))
        after = capture_path(a)
        assert rc == EXIT_USAGE, "expected USAGE for a hardlink alias, got %d" % rc
        assert before == after, "hardlinked alias was written through the guard"
    run_case(cases, "refuses-write-through-hardlink-alias", case_guard_hardlink)

'''

tr("H14-new-cases", """    passed = sum(1 for _, ok, _ in cases if ok)""",
   NEW_CASES.lstrip("\n") + """    passed = sum(1 for _, ok, _ in cases if ok)""")


def main() -> int:
    text = BASE.read_text(encoding="utf-8")
    base_sha = hashlib.sha256(text.encode()).hexdigest()
    print("base: %s sha256=%s lines=%d" % (BASE, base_sha, text.count("\n")))
    for name, anchor, repl in T:
        n = text.count(anchor)
        if n != 1:
            print("ANCHOR-FAIL %-32s count=%d" % (name, n))
            return 1
        text = text.replace(anchor, repl)
        print("  ok %-32s" % name)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    out_sha = hashlib.sha256(text.encode()).hexdigest()
    print("candidate: %s sha256=%s lines=%d" % (OUT, out_sha, text.count("\n")))
    return 0


if __name__ == "__main__":
    sys.exit(main())