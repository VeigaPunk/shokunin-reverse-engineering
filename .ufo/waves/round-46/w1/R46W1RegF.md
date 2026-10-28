# R46W1RegF — round-46 C2 census rows (tag `reg-f`)

Seat: `R46W1RegF` (registry scribe, leaf). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze
`31820472784284727546808acc31b3ea1e73919b`. Everything below was read and executed at that
freeze; the worktree blobs of all three instruments are byte-identical to the freeze blobs
(hashes in `w1/R46W1RegF/receipt.md`).

## Deliverable

`w1/R46W1RegF/rows.md` — exactly three rows, one line each, 7 cells, house column order,
cell 1 the backticked path and nothing else, cell 3 binding `0=`, `1=`, `2=`, no backticks
outside cell 1, no literal `|` inside a cell:

- `tools/round-41/fetch-vendor.py` — probe, carrier materialisation chain (url → image
  sha256 → member sha256 → nested file sha256 → carve → carrier pin), fails closed.
- `tools/round-42/heldout-gen-v4.py` — probe, deterministic held-out carrier generator,
  `--run` fills envelopes, `--verify` regenerates and compares.
- `tools/round-45/c1-counter.py` — gate, R45-C1 rule block 22 and its citations at `--rev`.

All three paths are in `tools/round-46/census.json` (38 paths at the freeze).

## Verification actually run

- **All three selftests green at the frozen bytes.** fetch-vendor `cases=16 pass=16 fail=0`
  (exit 0); round-45 c1-counter `cases=9 failures=0` (exit 0); heldout-gen-v4
  `all 17 selftest checks passed` (exit 0). Re-run twice; identical stdout sha256 both times.
- **Process-level exit codes measured, not inferred.** fetch-vendor: 0 selftest, 2 with no
  args, 2 with `--cache` only, 1 on a broken chain link (JSON receipt on stdout, no cache
  entry written), 0 on `--help`. c1-counter: 0 selftest, 2 with no args, 2 on an unknown
  revision, 0 scoring itself at the freeze (`rule_blocks 22`, `block22_rows 10`,
  `failing []`). heldout-gen-v4: 0 selftest, 2 on missing `--seed` (argparse), 1 on a short
  seed and 1 on an unknown class.
- **Rows scored by the frozen counter's own code**, not by eye: `registry.score(...,
  "r46", "v2", ...)` over a section built from `rows.md` returns exit 0 with
  `unregistered []`, `thin []`, `absent_at_rev []`; three mutants of those same rows
  (prose verdict map, cell-1 substring, deleted row) return exit 1 with exactly the expected
  list populated. The format is load-bearing under the frozen parser, not merely well-formed.
- No exit code outside `{0,1,2}` was observed from any of the three.

## Findings — instrument behaviour the L1 should know before it reconciles

**F1. `tools/round-42/heldout-gen-v4.py` collapses its own usage refusals into 1.** Every
self-refusal is `raise SystemExit("<text>")` (`--seed` format, unknown class, `--out` already
holding a manifest, `--verify` without `--run`, missing writer, fixture-pin mismatch), and
Python exits 1 for that. Only argparse exits 2. Measured: `--seed zz --selftest` → exit 1,
empty stdout; `--classes nope` → exit 1, empty stdout. So exit 1 currently means both "the
generated set failed a check" and "the invocation never evaluated anything". My row states
this explicitly rather than pretending the map is clean. This is a real limit of a
registry-eligible instrument; it is not repairable here (frozen bytes).

**F2. `tools/round-41/fetch-vendor.py`'s docstring exit line is false in one half.** It
claims "2 usage / unreadable spec"; an unreadable or invalid `--spec` exits **1** with a
traceback and empty stdout (measured: nonexistent file → `FileNotFoundError`, truncated JSON
→ `JSONDecodeError`, both exit 1). Only missing-argument usage returns 2. My row therefore
binds 2 to the measured meaning ("usage refusal: no `--cache`, or neither `--spec` nor
`--root` with `--rev`") and does not repeat the docstring claim.

**F3. Traceback exits are indistinguishable from measured failures.** For fetch-vendor the
same exit 1 carries a JSON receipt when a chain link fails and zero bytes when the spec cannot
be read; a caller that parses stdout to classify the verdict gets nothing in the latter case.
Same shape applies to any uncaught exception in the other two.

**F4. `tools/round-45/c1-counter.py` pins `rule_blocks == 22`, so it stops scoring once
block 23 lands.** It scores 0 at the freeze today (`failing []`), but the landing of round-46
block 23 makes `rule_blocks 23 != 22` and the counter will exit 1 at the post-landing `--rev`
by design. The registry row registers presence and the exit map at the measured revision; it
must not be read as "certified green at the post-landing REV". Its selftest, not its
`--rev` verdict, is what the row cites.

**F5. The six rows already in `### Round-44/45 instrument registry` are thin under v2.**
Scored verbatim through the frozen scorer (receipt #17), the landed
`tools/round-45/c1-counter.py` row returns exit 1, `thin ["tools/round-45/c1-counter.py"]`:
its verdict map reads `` `0` met; `1` not met … `` with no `=` or `:` binding the digits, and
`registry.EXITMAP` finds no key in it. Its section header also reads
`tool | gate or probe | verdict map (exit codes) | …`, not the house
`tool | gate or probe - purpose | …`. So the landing needs six rewritten rows plus a header
change, not just 32 appends — otherwise C2 clause 2 and clause 4 fail on the pre-existing
rows once the census covers them.

**F6. Scope fact for the census.** All three paths exist at the freeze and in
`census.json`; `named_but_absent` is empty at the freeze, so my three rows cannot fail clause
5 on presence.

## Risks

- The frozen scorer's `EXITMAP` accepts `:` as well as `=`; my rows use `=` only, so no
  accidental key can appear from a time-like token. I checked the parsed key set per row
  (`{0,1,2}` exactly).
- `heldout-gen-v4` exit 1 overloading (F1) means a future C2 consumer of that row cannot
  use the exit code alone to separate "red artefact" from "bad argv". Recorded in the row
  text and here; no silent normalisation.
- The row-level validation used a synthetic three-path census. The full C2 run still needs
  the other 35 census rows; nothing here claims the round-level target.

## Blockers

None. No install was made (stdlib python3, read-only git, sha256sum only); scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegF` holds the receipts and is removed after the copy.
