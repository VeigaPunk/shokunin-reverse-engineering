# ResidualNumerator — appendix to CriticNumerator (same seat, source-only)

Source F=9d64b95393bb7134e9fe0dfa9f68df91338a3665; previous C=2838351450ff1ee4baa620c962a1153450d53311;
baseline B=aa1450b82f9ede35aada63efe8a34e01c6e02f72. `CriticNumerator.md` (C report) is preserved
unchanged.

Read set: `git show F:` of `tools/count-c1.py`, `tools/counter-fixtures.py`,
`frozen/expected-v3.json` and `frozen/pre-v3-counter.py`.
Metadata only: `git diff --name-status C F` and `git ls-tree -r` modes at B and F.

Nothing was run: no tests, counter, selftest, producer or install. All outcomes below are
source-inferred and unverified until L1's final run.

## Findings

### N1 — Pins are consistent; pre-v3 is exactly C's counter (observed)
- `F:frozen/pre-v3-counter.py` and `C:tools/count-c1.py` are byte-identical (no-index diff
  empty). Both have sha256 `f4b8d16a…0cc2`, which equals expected-v3
  `red_regression.before_counter_sha256` and `inputs[pre-v3-counter.py]`.
- `F:frozen/expected-v3.json` has sha256 `c0701915…b75f`, which equals
  `SELFTEST_MANIFEST_SHA256` (`count-c1.py:25`).
- `F:tools/counter-fixtures.py` has sha256 `687c4074…927e`, which equals
  `inputs[counter-fixtures.py]`.
- The expected manifest has 25 cases: the old 21 plus `inherited_entry_lost`,
  `inherited_entry_changed`, `symlink_evidence` and `symlink_knowledge`.

### N2 — Inherited-knowledge loss and change: closed in v3, false accept in pre-v3 (inferred)
- v3 builds `knowledge_blobs(ref)` as path → (mode, blob) from `ls-tree -r -z`
  (`count-c1.py:74-78`).
- It raises `historical_knowledge_changed` if any B path differs or is missing at rev
  (`:79-82`). The check runs after the catalog, old-root and source-prefix guards and before
  any scan, so both new cases should give exit 2 with that exact error.
- The fixture target `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md`
  (`counter-fixtures.py:106-110`) exists at B, so the case is meaningful.
- Pre-v3 has no knowledge guard, and its round-22 witness comes from `r22.measure(root, BASELINE)`
  (`pre-v3:81`). Identify therefore stays held, plus the selected `inspect-signal-decoders` →
  exit 1, count 2, `c1_incomplete`. That mismatches expected exit 2 / `historical_knowledge_changed`
  for both cases: two named false accepts.
- This closes the counterexample from my C report's F5 (the "inherited identify lost" blind spot).

### N3 — Symlinked evidence and knowledge: false accept in pre-v3; the v3 filter depends on an unread helper (inferred, partly unverified)
- In pre-v3, `ls-tree --name-only` lists `120000` entries (`pre-v3:94`), and `git show rev:path`
  returns the symlink's target bytes. The fixture makes those bytes exactly the raw envelope
  (`counter-fixtures.py:70-72`) or the entry text (`:83-85`).
- So both cases bind exactly as the positive case does → count 2 against expected count 1: two
  more named false accepts.
- v3 restricts knowledge files and cited evidence to `dict(r20.tree_entries(root, rev))`
  (`count-c1.py:103-107,128-129`).
- Unverified: whether `tree_entries` excludes `120000` entries. That helper is outside my read
  set.
- Bounded: B already contains `120000` blobs, for example
  `.ufo/waves/round-18/verify/scratch-custody/…/symlink-loop` and
  `round-4/…/EX-25/fixtures/scratch/alias-{1,2}.conf`. Legacy `r22.measure(B)` calls
  `r20.tree_entries` and must succeed for v3 to proceed (`count-c1.py:90-92`). So the helper does
  not raise a Refusal on symlinks, and these cases cannot turn into exit 2.
- If the helper does include symlinks, the selftest would visibly fail with count 2 rather than
  falsely pass.

### N4 — The fixture's symlink construction can make the whole selftest unevaluable (concrete risk, unverified)
- `symlink_to(raw)` stores the whole serialized envelope as a symlink target (`:72`). Linux caps
  targets at `PATH_MAX` 4096 bytes, and some filesystems cap them lower.
- If the `inspect-signal-decoders` document from `frozen/fixture.json` (not in my read set)
  serializes longer than that, `OSError(ENAMETOOLONG)` escapes `fixtures.run`, which has no
  per-case guard.
- `main` then reports the entire 25-case selftest as `unevaluable`, exit 2, not as one failed case.
  This affects whether the run is evaluable, not the count; there is no false accept.
- Smallest correction: build the symlink case from a minimal synthetic envelope below 1 KiB, or
  catch `OSError` per case and record it as an observed case failure.

### N5 — Old positives preserved; exactly four false accepts expected (inferred)
- The only new `error` expectations among the old cases are `old_source`, `helper_tamper`,
  `historical_root_injection`, `inherited_lost` and `catalog_changed`.
- Each string is raised identically by pre-v3 (`pre-v3:63,65,68,73`).
- `git add -- corpus/knowledge` (widened from ENTRY) cannot change the old cases, because
  `reset --hard` plus `clean -fd` precede each case and only the new ENTRY path is added. The
  knowledge guard cannot fire on old cases either.
- Hence pre-v3 should match 21/25 and fail exactly the four named cases, while v3 should pass
  25/25.
- Caveat: this assumes `fixture.json`'s base has B's knowledge blobs and no S058 row, the same
  assumption v2 relied on; I did not re-read it here.

### N6 — Six-verb denominator and union are unchanged; ceiling is 4/6 at F (observed and inferred)
- The C→F changes to `count-c1.py` are only:
  - the knowledge guard (`:74-82`);
  - the regular-blob selection (`:103-107,128-129`);
  - the Git config/hook environment (`:169-171`);
  - `RuntimeError` handling (`:185`).
- `r22.T1`, `held`, `t1_total: 6` and `len(held)==6` are untouched (`:101-102,140-145`).
- `git diff --name-status C F` shows no change under `.ufo/waves/round-23/evidence/c1/`. The only
  added evidence is under `evidence/sources/`, which does not match `ROOTS[1]`.
- So the bindable envelopes are the C set, whose `meta.command` values cover only four verbs (C
  report F3).
- `debug-with-gdb` and `debug-with-rizin` cannot bind at F: 6/6 is impossible, and 4/6 is the
  ceiling.
- Whether exactly 4 still holds depends on the F edits to the two R23 entries and SOURCES (the
  Sources seat's scope). That is unverified here.
- At F, every `corpus/knowledge` and `evidence/c1` blob except
  `connect-dart-symbols/preflight_dart_carrier.py` (`100755`, a `.py` file that is never a JSON
  citation) is `100644`. The C→F knowledge changes touch only post-B entries, so the v3 guard
  should not fire on F itself.
- My C report's F6 minor issues are unchanged and are false negatives only: unevaluable results
  are still dropped silently, and a sentence-final `.json.` citation is still skipped.

## Writes / installs
- Wrote only `.ufo/waves/round-23/w2/ResidualNumerator.md`. No installs.
