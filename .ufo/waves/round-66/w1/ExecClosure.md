# ExecClosure — R66-C1 frozen counter run (w1)

Executed the frozen `tools/round-66/closure-boundary.py` once end to end in all three
requested modes, read-only, with `TMPDIR=/fast/scratch/hyaku/kaidoku-r66/ExecClosure`
(scratch deleted before yield). Instrument not edited; no re-runs.

## Files changed (written only)
- `.ufo/waves/round-66/w1/ExecClosure/findings.md` (scoped findings)
- `.ufo/waves/round-66/w1/ExecClosure/{verify.json,verify.stdout,verify.stderr,manifest.json,manifest.stdout,skiprun.json,instrument-before.txt,instrument-after.txt,toolchain-cache-after.txt}` (receipts)
- `.ufo/waves/round-66/w1/ExecClosure.md` (this report)
No repository source, fleet root, MANIFEST, `.ufo/state/`, toolchain root, or sibling lane touched.

## Behavior measured
- `--verify`: exit **0**, `ok true`, **5/5** arms passed (`arms_total 5`, `passed 5`, `count 30`).
  - a1 `ok true`, `cache_present []`
  - a2 `ok false`, `cache_present ["__pycache__", "__pycache__/fixture_mod.cpython-315.pyc"]`, finding names the `.pyc`; probe itself `ok true` → the post-probe cache scan, not probe failure, drives the red
  - a3 `count_ok true`, `entries 30`
  - a4 `count_ok false`, `entries 29`, finding `"count 29 != 30"`, `dropped_entry "d8-14.7.173/d8"`
  - a5 `closure null`, `closure_claimed false`
- `--manifest`: exit **0**; `closure.ok true`, `entries 30`, `expected_count 30`, `count_ok true`, `missing []`, `pin_mismatch []`, `cache_present []`, probe `{"ok": true, "message": "ok"}`.
- `--skip-run`: exit **1** by design; `closure null`, `closure_claimed false`, `verified false`, `runs_total 0`. Instrument contract: exit 1 = not verified; `skip_run_receipt` sets `"exit": 1` and `--selftest` asserts it (line 421). Not an error.
- No exit-2; `verify.stderr` empty.

## Retained evidence
- Instrument sha256 before **and** after: `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b` (equal, `diff -u` clean).
- Frozen r65 pin on disk equals receipt `v1_pin`: `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`.
- Receipt sha256: verify `7d2188b5ef2e73dd5978faa1afc936c96a188dc62ef189bf5ce21ac25243ea0a`; manifest `305a340e91c9b70743c0a298c3686379da6e182b9cb4a5726e9d9001bc17b91f`; skiprun `1fe4d6be39f9f77730d883fe661ac049ecd0fd49fbe3b4b956763be56390ef73`.
- Toolchain cache scan: **0** lines (`toolchain-cache-after.txt`, sha256 `e3b0c442…7852b855`).

## Risks / caveats
- `--skip-run` exit 1 could be misread as failure by a later aggregator; it is the mode's documented "not verified" exit and is selftest-asserted.
- a1's arm detail omits a `probe` key (a2 carries it); arm pass/fail is decided on `ok`/`cache_present`/`findings`, so no decision is lost.
- The counter is self-contained; I did not exercise `--selftest` (not in my assignment).

## Blockers
None.

Report: .ufo/waves/round-66/w1/ExecClosure.md
