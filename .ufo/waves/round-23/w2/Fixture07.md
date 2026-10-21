# Fixture07 — source review: `wrong_usedby` (R23-C1 selftest)

Candidate `2838351450ff1ee4baa620c962a1153450d53311`. All bytes read with `git show <rev>:PATH`, copied into my ignored runtime dir for line-anchored reading. Suite NOT executed. No lane, index, or frozen file edited.

## Verdict

- **No wrong expectation.** `wrong_usedby = {exit 1, count 1, finding c1_incomplete}` (`frozen/expected-v2.json:38-42`) is what the candidate counter produces for this fixture (F0, static trace).
- **Positive-preserving:** `wrong_usedby` differs from `positive` only in the used-by string (`counter-fixtures.py:82`). Envelopes, evidence file, entry body, and the rest of the S058 row are identical, so an outcome change is attributable to the used-by gate.
- **Weak mutation coverage.** The case detects only a counter with no used-by check at all. Three plausible refinements of the same fault (F1–F3) survive it, and no other manifest case detects them either. The manifest has 21 cases; 13 expect count 1.

## Findings

### F0 — expectation correct (observed by static trace; not executed)

- Pins: `expected-v2.json` sha256 `458b30d5…096f` equals `count-c1.py:25` `SELFTEST_MANIFEST_SHA256`. `fixture.json` `a1f5aff8…f4b` and `counter-fixtures.py` `f2990b35…97f` equal the manifest `inputs`.
- Legacy round-22 counter `.ufo/waves/round-22/tools/count-c1.py` sha256 `c925918f…1879` at both base and candidate, equal to `count-c1.py:23` `LEGACY_SHA256`. Catalog blob (`61fc4e66…`) and `.ufo/waves/round-22/evidence/c1` tree (`b83fc459…`) identical base vs candidate. None of the `measure()` exit-2 guards fire for this fixture.
- Anchor: the only `## Paths` heading in baseline `corpus/SOURCES.md` is line 65. The last S-row is line 63 (S057); line 64 is blank. `counter-fixtures.py:84` inserts the S058 row after S057, so the historical prefix guard `count-c1.py:71-73` passes. No exit 2 from that guard.
- Gate: entry `corpus/knowledge/control-r23-synthetic.md` (`counter-fixtures.py:16`) carries `source: S058` (`:47`). Its row's used-by cell is `corpus/knowledge/not-this-entry.md` (`:82-83`). At `count-c1.py:107` the conjunct `entry in [x.strip() for x in row[11].split(',')]` is False, so `:109-110` `continue` before any bind. Held set = historical `identify-flutter-build` only, so count 1, finding `c1_incomplete`, exit 1 (`main` returns 0 only when count == 6). Matches `expected-v2.json:38-42`.
- **Inferred, not observed:** the historical measure (`count-c1.py:81-83`) returns exactly `['identify-flutter-build']` at baseline. Consistent with `claims.json` `before: 1` and `no_harm` "R22 C1=1/6", but I did not run the legacy measure.
- Independence: `counter-fixtures.py` imports only stdlib (`copy, json, os, pathlib, subprocess, sys, tempfile`), never imports count-c1 logic, and runs the counter as a subprocess. The header (`:47`) and row template (`:83`) are literals. Expectations are a separate digest-pinned file. Caveat: same author for both (F6).

### F1 — weak mutation (medium): existence substitution survives the case and the suite

- Mutant M-exist: replace the used-by membership conjunct at `count-c1.py:107` with "every used-by path exists at rev".
- Observed: `corpus/knowledge/not-this-entry.md` is absent at base (`git cat-file -e` fails). M-exist rejects it, count 1, so it passes `wrong_usedby`.
- Inferred: M-exist matches the correct counter in all 21 cases. Every other case uses ENTRY as its sole used-by (`counter-fixtures.py:82`), and ENTRY exists at rev. The suite never presents an existing, unrelated used-by path.
- M-exist is the stated fault by another route: a row whose used-by names a different existing entry is accepted.
- Discriminator: `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md` exists at base (observed: `git cat-file -e` succeeds) and does not name ENTRY. As `wrong_usedby`'s used-by, the correct counter still gives count 1. M-exist would reach the same bind path as `positive` and give count 2 (requires F5), failing the expectation.

### F2 — weak mutation (medium): row-wide mention survives

- Mutant M-row: eligibility = ENTRY appears anywhere in the S-row, not in the used-by cell.
- Inferred survival: the template (`counter-fixtures.py:83`) puts ENTRY only in cell 11, and cell 11 here is the wrong path. ENTRY appears in no cell of the fixture row. Suite-wide, ENTRY is only ever in cell 11, so M-row never differs.
- Discriminator: keep used-by as-is and place the ENTRY path in another cell (e.g., the scope cell). Correct counter: count 1 (membership fails). M-row: count 2 (requires F5). This is the frozen falsifier "mere mention counts" applied to the SOURCES side.

### F3 — weak mutation (low-medium): substring / basename collision survives

- Mutants M-sub: `entry in row[11]` (cell substring). M-base: `basename(entry) in row[11]`.
- Inferred survival: `not-this-entry.md` contains neither `corpus/knowledge/control-r23-synthetic.md` nor `control-r23-synthetic.md`. No case uses a near-collision used-by.
- Discriminator: used-by `corpus/knowledge/control-r23-synthetic.md.bak` contains ENTRY as a substring but is not a list element. Correct counter: count 1. M-sub and M-base: count 2 (requires F5).
- F1 and F3 discriminators must be separate variants. An existing sibling does not contain ENTRY as a substring, and `.bak` does not exist (so M-exist would reject it).

### F4 — coverage gap (low): list parsing untested

- No manifest case has a multi-entry used-by containing ENTRY. Inferred survival: a "first-only" mutant (`row[11].split(',')[0]`) and a `split(';')` mutant pass all 21 cases. The `split(';')` mutant rejects multi-entry lists (false negative), it does not accept them. This corrects my first draft's wording.

### F5 — unverified control dependency (info)

- Positive's expected count 2 depends on legacy `bind_cli` accepting the synthetic `inspect-signal-decoders` envelope (`counter-fixtures.py` documents, `normalized_result.control` marker). Not verified; the legacy bind path is outside this item. F0 for `wrong_usedby` does not depend on it, because that case never reaches bind. F1–F3 detection claims do depend on it.

### F6 — process (info, author-side)

- The manifest digest is pinned inside the unit under test (`count-c1.py:25`). A coordinated edit to counter plus `expected-v2.json` is undetected. Not specific to this case.

## Produced files and hashes

- Report: `.ufo/waves/round-23/w2/Fixture07.md` (overwrites my own first draft). Its own sha256 is in the final message, since a file cannot embed its own hash.
- Runtime copies, ignored `.ufo/waves/round-23/runtime/KaidokuR23.Fixture07/`:
  - `count-c1.py` `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`
  - `counter-fixtures.py` `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f`
  - `expected-v2.json` `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f`
  - `SOURCES-baseline.md` `5ae5e7ed539d092d801d1c521cb3a0cfa6d89ff82e38b8d86c0c8d5b4f777ebd`
- `/tmp/f07-sources.md` was created during an early read, outside the allowed write paths, and removed. Absence verified.

## Installs

- None.

## Open risks

- F1–F4 survival claims are static inference. Confirming them requires executing mutants in a disposable clone. This item forbids execution, so I did not.
- Baseline historical measure (F0) and F5 bind acceptance are not observed.
- F6 is structural and author-side.
