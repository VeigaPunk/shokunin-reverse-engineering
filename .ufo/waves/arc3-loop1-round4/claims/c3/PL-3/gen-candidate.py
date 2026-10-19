#!/usr/bin/env python3
"""PL-3 anchored candidate generator — custody-pair.py + README.md residual closures.

Every anchor is asserted to occur EXACTLY ONCE in the base revision; the script
refuses (exit 1) on a moved base rather than mis-applying (rule #14).

Base revision (re-derived 2026-10-19, wave arc3-loop1-round4):
  tool   .ufo/gates/custody-pair/custody-pair.py
         sha256 7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09 (1155 lines)
  README .ufo/gates/custody-pair/README.md
         sha256 f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193 (185 lines)

Usage: gen-candidate.py <tool-in> <readme-in> <outdir>
Writes <outdir>/custody-pair.py and <outdir>/README.md; prints identities.
Patch text only: the real target is C3's EX-21 write path.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

TOOL_BASE_SHA = "7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09"
README_BASE_SHA = "f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193"

# ---------------------------------------------------------------- tool patches

T_PATCHES: list[tuple[str, str, str]] = []

# P1 — docstring exit-map line for USAGE (mkdir class + distinct-path wording)
T_PATCHES.append((
    "docstring exit map (2 USAGE)",
    """    2   USAGE             bad arguments, unreadable/unparsable receipt, refused
                          or failed write, insufficient reference coverage under
                          --require-paths, unusable selftest scratch dir
""",
    """    2   USAGE             bad arguments, unreadable/unparsable receipt, refused
                          or failed write (including an uncreatable receipt
                          directory), insufficient DISTINCT-path coverage under
                          --require-paths, unusable selftest scratch dir
""",
))

# P2 — docstring MATCH line gains the both-absent declaration
T_PATCHES.append((
    "docstring exit map (0 MATCH)",
    """    0   MATCH             every compared path agrees on every comparable field
""",
    """    0   MATCH             every compared path agrees on every comparable field;
                          a stanza absent on BOTH sides is MATCH by declared
                          design (the only shared field is existence, compared=0/11
                          -- a vacuous contract state, not a content verification)
""",
))

# P3 — ROUND-4 docstring block, inserted after ROUND-3 item 6
T_PATCHES.append((
    "docstring ROUND-4 block",
    """     not a raw `FileNotFoundError` traceback at exit 1.
""",
    """     not a raw `FileNotFoundError` traceback at exit 1.

ROUND-4 RESIDUAL CLOSURES (seat EX-21, wave arc3-loop1-round4). The four
round-3 residuals, each measured before landing (patch sources in
`.ufo/waves/arc3-loop1-round4/claims/c3/`):

  a. SIDECAR SCOPE. The write guard covers the derived `<out>.sha256` sidecar as
     well as the receipt, by resolved path and by inode. `--out X --paths
     X.sha256` (and the symlinked-sidecar form) is refused exit 2 instead of
     clobbering the file being measured. The sidecar name is computed inside the
     guarded region: an empty-name `--out` ('' / '.' / '/') keeps the base
     behaviour (a USAGE write failure, not a ValueError traceback).
  b. MKDIR GUARD. `out.parent.mkdir(...)` is inside a guarded region: an `--out`
     whose parent component is a regular file is a declared USAGE exit 2 with a
     message, not a FileExistsError/NotADirectoryError traceback at exit 1.
  c. DISTINCT-PATH COVERAGE. `--require-paths N` counts distinct resolved paths,
     not stanzas (`distinct_paths`): a reference padded with duplicate stanzas of
     one path no longer passes the gate.
  d. BOTH-SIDES-ABSENT STANZAS — declared MATCH, kept, and fenced. A path absent
     on both sides is MATCH with compared=0/11: the stanza asserts agreement on
     existence only. An error-carrying stanza on either side is UNEVALUABLE (14),
     classified before this branch; existence disagreement is ABSENT (13) in both
     directions. A consumer needing content verification must require the paths
     it needs (`--require-paths 5` over the canonical set).
""",
))

# P4 — write guard: cover the sidecar; guard the mkdir
T_PATCHES.append((
    "cmd_capture guard + mkdir",
    """        guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths
        if out.resolve() in {g.resolve() for g in guarded} or any(_same_file(out, g) for g in guarded):
            print("USAGE: refusing to write a receipt over a path it measures or a custody path"
                  " (path or inode): %s" % out, file=sys.stderr)
            return EXIT_USAGE
        out.parent.mkdir(parents=True, exist_ok=True)
""",
    """        guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths
        candidates = [out]
        try:
            candidates.append(out.with_name(out.name + ".sha256"))
        except ValueError:  # empty name ('' / '.' / '/'): the write path maps it to USAGE
            pass
        for cand in candidates:
            if cand.resolve() in {g.resolve() for g in guarded} or any(_same_file(cand, g) for g in guarded):
                print("USAGE: refusing to write a receipt or its sidecar over a path it measures"
                      " or a custody path (path or inode): %s" % cand, file=sys.stderr)
                return EXIT_USAGE
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:  # e.g. a path component is a regular file
            print("USAGE: cannot create the receipt directory (%s): %s" % (exc, out.parent),
                  file=sys.stderr)
            return EXIT_USAGE
""",
))

# P5 — distinct-path coverage: helper + reference_coverage + call site
T_PATCHES.append((
    "reference_coverage distinct unit",
    '''def reference_coverage(ref_sections, required: int) -> tuple[bool, str]:
    """--require-paths gate (round-2 debt D3): does the reference account for
    `required` paths? Returns (ok, line); `unaccounted` lists the canonical
    custody paths absent from the reference (resolved-path comparison)."""
    have = {Path(s["path"]).expanduser().resolve() for s in ref_sections}
    unaccounted = [p for p in CUSTODY_PATHS if Path(p).expanduser().resolve() not in have]
    line = ("REFERENCE-COVERAGE: %d/%d paths present in reference; unaccounted: %s"
            % (len(ref_sections), required, " ".join(unaccounted) if unaccounted else "(none)"))
    return len(ref_sections) >= required, line
''',
    '''def distinct_paths(sections) -> int:
    """Distinct resolved path identities in a parsed receipt. Stanza multiplicity
    is not coverage (round-3 residual c: five duplicate stanzas of one path
    passed the --require-paths gate)."""
    return len({Path(s["path"]).expanduser().resolve() for s in sections})


def reference_coverage(ref_sections, required: int) -> tuple[bool, str]:
    """--require-paths gate (round-2 debt D3; unit fixed in round 4): does the
    reference account for `required` DISTINCT paths? Returns (ok, line);
    `unaccounted` lists the canonical custody paths absent from the reference
    (resolved-path comparison)."""
    have = {Path(s["path"]).expanduser().resolve() for s in ref_sections}
    unaccounted = [p for p in CUSTODY_PATHS if Path(p).expanduser().resolve() not in have]
    line = ("REFERENCE-COVERAGE: %d/%d distinct paths present in reference; unaccounted: %s"
            % (len(have), required, " ".join(unaccounted) if unaccounted else "(none)"))
    return len(have) >= required, line
''',
))

T_PATCHES.append((
    "cmd_verify gate message",
    '''            print("USAGE: reference covers %d of the required %d paths" % (len(a_sections), require),
                  file=sys.stderr)
''',
    '''            print("USAGE: reference covers %d of the required %d distinct paths"
                  % (distinct_paths(a_sections), require), file=sys.stderr)
''',
))

# P6 — four new selftest cases, inserted before the tally
NEW_CASES = '''    # 20. the write guard covers the derived sidecar path (round-3 residual a)
    def case_guard_sidecar():
        vic = root / "sidecar-vic.sha256"
        vic.write_bytes(b"sidecar victim bytes\\n")
        before = vic.read_bytes()
        out_vic = root / "sidecar-vic"
        rc = cmd_capture(argparse.Namespace(out=str(out_vic), paths=[str(vic)], label="guard-sidecar"))
        assert rc == EXIT_USAGE, "expected USAGE for a sidecar aimed at a measured path, got %d" % rc
        assert vic.read_bytes() == before, "the measured file was clobbered by the derived sidecar"
        assert not out_vic.exists(), "a refused run left a receipt behind"
        alias = root / "sidecar-alias.sha256"
        os.symlink(vic.name, alias)
        rc2 = cmd_capture(argparse.Namespace(out=str(root / "sidecar-alias"), paths=[str(vic)],
                                            label="guard-sidecar-symlink"))
        assert rc2 == EXIT_USAGE, "expected USAGE for a symlinked sidecar, got %d" % rc2
        assert vic.read_bytes() == before, "the measured file was clobbered through the symlinked sidecar"
    run_case(cases, "refuses-sidecar-clobber-of-measured-path", case_guard_sidecar)

    # 21. an --out whose parent component is a regular file is a declared USAGE (residual b)
    def case_out_parent_not_a_dir():
        pfile = root / "out-parent-file.txt"
        pfile.write_text("not a directory", encoding="utf-8")
        rc = cmd_capture(argparse.Namespace(out=str(pfile / "rec.txt"), paths=[str(fixture)],
                                            label="guard-mkdir"))
        assert rc == EXIT_USAGE, "expected USAGE for an uncreatable receipt dir, got %d" % rc
        assert pfile.read_text(encoding="utf-8") == "not a directory", "the parent file was modified"
        rc2 = cmd_capture(argparse.Namespace(out=str(pfile / "sub" / "rec.txt"), paths=[str(fixture)],
                                             label="guard-mkdir-nested"))
        assert rc2 == EXIT_USAGE, "expected USAGE for a nested uncreatable receipt dir, got %d" % rc2
        ok = root / "fresh-dir" / "deep" / "rec.txt"
        rc3 = cmd_capture(argparse.Namespace(out=str(ok), paths=[str(fixture)], label="guard-mkdir-ok"))
        assert rc3 == EXIT_MATCH, "ordinary parent creation broke: exit %d" % rc3
        assert ok.exists(), "ordinary parent creation did not write the receipt"
    run_case(cases, "out-parent-not-a-directory-usage-exit", case_out_parent_not_a_dir)

    # 22. the coverage gate counts distinct resolved paths, not stanzas (residual c)
    def case_coverage_distinct():
        single = root / "coverage-single.conf"
        single.write_bytes(b"coverage single fixture\\n")
        rec, rc0 = capture_to("coverage-single-pre.txt", [single])
        assert rc0 == EXIT_MATCH, "coverage fixture capture exit %d" % rc0
        text = rec.read_text(encoding="utf-8")
        head, first = text.split("PATH:", 1)
        padded = root / "coverage-padded.txt"
        padded.write_text(head + ("PATH:" + first) * 5, encoding="utf-8")
        out_bad = root / "coverage-padded.out"
        rc_bad = _run_verify([str(padded), "--live", "--require-paths", "5"], out_bad)
        assert rc_bad == EXIT_USAGE, "a padded reference passed the gate (exit %d)" % rc_bad
        assert "REFERENCE-COVERAGE: 1/5" in out_bad.read_text(), "coverage line lacks the distinct count"
        five = []
        for i in range(5):
            p = root / ("coverage-distinct-%d.conf" % i)
            p.write_bytes(b"distinct %d\\n" % i)
            five.append(p)
        rec5, rc5 = capture_to("coverage-five-pre.txt", five)
        assert rc5 == EXIT_MATCH, "five-path reference capture exit %d" % rc5
        out_ok = root / "coverage-five.out"
        rc_ok = _run_verify([str(rec5), "--live", "--require-paths", "5"], out_ok)
        assert rc_ok == EXIT_MATCH, "five distinct paths failed the gate (exit %d)" % rc_ok
    run_case(cases, "coverage-gate-counts-distinct-paths", case_coverage_distinct)

    # 23. both-sides-absent stanzas: the declared MATCH, fenced (ruling d)
    def case_both_absent_declared_match():
        ghost = root / "both-absent-ghost.conf"
        if ghost.exists():
            ghost.unlink()
        rec, rc0 = capture_to("both-absent-pre.txt", [ghost])
        assert rc0 == EXIT_ABSENT, "capture over a missing path should be ABSENT 13, got %d" % rc0
        assert "EXISTS: no" in rec.read_text(encoding="utf-8"), "absence not recorded"
        out_live = root / "both-absent-live.out"
        rc_live = _run_verify([str(rec), "--live"], out_live)
        assert rc_live == EXIT_MATCH, "declared both-absent MATCH changed: exit %d" % rc_live
        body = out_live.read_text()
        assert "VERDICT: MATCH" in body, "both-absent verdict changed: %r" % body
        assert "compared=0/11" in body, "both-absent comparison shape changed: %r" % body
        out_pair = root / "both-absent-pair.out"
        rc_pair = _run_verify([str(rec), str(rec)], out_pair)
        assert rc_pair == EXIT_MATCH, "receipt-vs-receipt both-absent MATCH changed: exit %d" % rc_pair
        ghost.write_bytes(b"resurrected\\n")
        out_rev = root / "both-absent-revived.out"
        rc_rev = _run_verify([str(rec), "--live"], out_rev)
        assert rc_rev == EXIT_ABSENT, "receipt-absent vs live-present should read ABSENT 13, got %d" % rc_rev
    run_case(cases, "both-absent-stanza-declared-match", case_both_absent_declared_match)

'''

T_PATCHES.append((
    "selftest new cases",
    "    passed = sum(1 for _, ok, _ in cases if ok)\n",
    NEW_CASES + "    passed = sum(1 for _, ok, _ in cases if ok)\n",
))

# -------------------------------------------------------------- README patches

R_PATCHES: list[tuple[str, str, str]] = []

R_PATCHES.append((
    "README write-scope sentence",
    """`capture` refuses to write its receipt over any path it is measuring or any of
the five custody paths — by resolved path *or* by inode (a hardlink alias is
refused too). `selftest --scratch` requires an existing, non-`/tmp` directory;
anything else is a declared USAGE exit 2.
""",
    """`capture` refuses to write its receipt **or its derived `<receipt>.sha256`
sidecar** over any path it is measuring or any of the five custody paths — by
resolved path *or* by inode (a hardlink alias is refused too; a symlink aimed at
a measured file is caught by the resolved-path arm). `selftest --scratch`
requires an existing, non-`/tmp` directory; anything else is a declared USAGE
exit 2, as is an `--out` whose parent directory cannot be created.
""",
))

R_PATCHES.append((
    "README exit row 2",
    "| 2 | `USAGE` | bad arguments, unreadable/unparsable receipt, a refused/failed write, fewer reference paths than `--require-paths N` demands, or an unusable `selftest --scratch` base |",
    "| 2 | `USAGE` | bad arguments, unreadable/unparsable receipt, a refused/failed write (including an uncreatable receipt directory), fewer **distinct** reference paths than `--require-paths N` demands, or an unusable `selftest --scratch` base |",
))

R_PATCHES.append((
    "README D3 bullet",
    """- **D3 → `--require-paths N` (USAGE 2).** A reference carrying fewer than N
  stanzas is a USAGE exit with a `REFERENCE-COVERAGE: n/N … unaccounted: …`
  line. Opt-in: without the flag the comparison is exactly the reference's
  paths, unchanged.
""",
    """- **D3 → `--require-paths N` (USAGE 2).** A reference carrying fewer than N
  **distinct resolved paths** is a USAGE exit with a
  `REFERENCE-COVERAGE: n/N distinct paths present in reference; unaccounted: …`
  line. Opt-in: without the flag the comparison is exactly the reference's
  paths, unchanged.
""",
))

R_PATCHES.append((
    "README round-4 section",
    """## Exit codes (declared)
""",
    """## Round-4 residual closures (arc3-loop1-round4, seat EX-21)

The four round-3 residuals, each closed with a declared class (patch sources in
`.ufo/waves/arc3-loop1-round4/claims/c3/`):

- **Sidecar scope (a).** The write guard covers the derived `<receipt>.sha256`
  sidecar as well as the receipt: `--out X --paths X.sha256` — and the symlinked
  sidecar form — is refused exit 2 instead of clobbering the file being
  measured.
- **`out.parent.mkdir` guard (b).** An `--out` whose parent component is a
  regular file is a declared USAGE exit 2 with a message, not a traceback.
- **Distinct-path coverage (c).** `--require-paths N` counts distinct resolved
  paths, not stanzas: a reference padded with duplicate stanzas of one path is
  refused.
- **Both-sides-absent stanzas (d)** — ruled below.

## Both-sides-absent stanzas: the declared MATCH (ruling, round 4)

A stanza whose path is absent on **both** sides (reference `EXISTS: no` and the
candidate side also missing, or two receipts that both record absence) is
classified `MATCH` with `compared=0/11` and exit 0. Ruling: **this is declared
design, kept, and now fenced by selftest case
`both-absent-stanza-declared-match`.**

- The class asserts exactly one thing: both sides agree the path does not exist.
  It is a **vacuous contract state** (`SHA256-CONTRACT: 0/0`), never a content
  verification.
- An error-carrying stanza (`STAT-ERROR`/`READ-ERROR`) on either side is
  `UNEVALUABLE` (14), classified *before* this branch — the round-2 fail-open is
  closed and does not reopen here.
- Existence disagreement is `ABSENT` (13) in **both** directions: a receipt that
  recorded `EXISTS: no` against a resurrected path reads `ABSENT` (measured).
- `capture` over a missing path exits 13, so a live capture never silently
  produces an all-ghost receipt; and `--require-paths N` counts distinct paths,
  so padding cannot manufacture coverage.
- A consumer that needs content verification must require the paths it needs
  (`--require-paths 5` over the canonical set) — `MATCH` alone, over a
  both-absent stanza, is not that.

## Exit codes (declared)
""",
))

R_PATCHES.append((
    "README selftest count",
    """`selftest` builds all fixtures in a scratch dir (never a custody path) and runs
22 cases: the round-2 fifteen (capture shape + sidecar identity, receipt-vs-live
clean, same-content rewrite in place (ctime pin) and via rename (inode pin),
content drift, absent path, mode drift, TZ-independence of the UTC render,
v1-stanza/v1-sums/v1-pipe compatibility with mutation detection,
unparsable-receipt usage exit, refusal to write a receipt over a custody path)
plus the round-3 seven: `unreadable-path-is-unevaluable`,
`unevaluable-never-matches`, `parsed-unevaluable-reference-never-matches`,
`partial-reference-require-paths-gate`, `refuses-to-write-over-scoped-path`,
`selftest-missing-scratch-usage-exit`, `refuses-write-through-hardlink-alias`.
It ends with

```
CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0
```
""",
    """`selftest` builds all fixtures in a scratch dir (never a custody path) and runs
26 cases: the round-2 fifteen (capture shape + sidecar identity, receipt-vs-live
clean, same-content rewrite in place (ctime pin) and via rename (inode pin),
content drift, absent path, mode drift, TZ-independence of the UTC render,
v1-stanza/v1-sums/v1-pipe compatibility with mutation detection,
unparsable-receipt usage exit, refusal to write a receipt over a custody path),
the round-3 seven: `unreadable-path-is-unevaluable`,
`unevaluable-never-matches`, `parsed-unevaluable-reference-never-matches`,
`partial-reference-require-paths-gate`, `refuses-to-write-over-scoped-path`,
`selftest-missing-scratch-usage-exit`, `refuses-write-through-hardlink-alias`,
plus the round-4 four: `refuses-sidecar-clobber-of-measured-path`,
`out-parent-not-a-directory-usage-exit`,
`coverage-gate-counts-distinct-paths`, `both-absent-stanza-declared-match`.
It ends with

```
CUSTODY_PAIR_SELFTEST: CLEAN cases=26 passed=26 failed=0 exit=0
```
""",
))


def apply_patches(text: str, patches, label: str) -> str:
    for name, old, new in patches:
        n = text.count(old)
        if n != 1:
            raise SystemExit("ANCHOR FAIL (%s): %s occurs %d times (want exactly 1)" % (label, name, n))
        text = text.replace(old, new, 1)
        print("anchor ok  [%s] %s" % (label, name))
    return text


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    tool_in, readme_in, outdir = (Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
    tool = tool_in.read_text(encoding="utf-8")
    readme = readme_in.read_text(encoding="utf-8")

    t_sha, r_sha = sha(tool), sha(readme)
    print("base tool   %s  %s" % (t_sha, "OK" if t_sha == TOOL_BASE_SHA else "UNEXPECTED"))
    print("base readme %s  %s" % (r_sha, "OK" if r_sha == README_BASE_SHA else "UNEXPECTED"))
    if t_sha != TOOL_BASE_SHA or r_sha != README_BASE_SHA:
        return 1

    tool = apply_patches(tool, T_PATCHES, "tool")
    readme = apply_patches(readme, R_PATCHES, "readme")

    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "custody-pair.py").write_text(tool, encoding="utf-8")
    (outdir / "README.md").write_text(readme, encoding="utf-8")
    print("candidate tool   %s  %d lines" % (sha(tool), len(tool.splitlines())))
    print("candidate readme %s  %d lines" % (sha(readme), len(readme.splitlines())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
