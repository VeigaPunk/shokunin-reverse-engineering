# ReviewR16Verification — what `pins_unchanged_during_run` is backed by (route R16-PROVENANCE)

Seat: author-side advisory reviewer, round 17 W1. Read-only; no REA analyze/search/decompile, no Ghidra,
no carrier execution, no tool installs. No `lsp` device is mounted in this seat, so caller/definition
checks were done by exact Git-blob reads and Python recomputation, not by text grep alone.

Objects reviewed: `.ufo/waves/round-16/verification.json` at lane HEAD `b563c79`
(worktree blob = HEAD blob, sha256 `4808b2665d073bdaaf35be93c85b8e351dd2052de36014281f4ba006e3fa5279`),
its recorded `source_revision` A = `27b8fc13156230981312c44380cddab1f2bd318d`, `baseline` B =
`6235498b4112350eebce0812a74af1781fc0ee88`, and the commits that carry the file:
A (source, 2026-10-20T08:35:55Z) → `2fc1d6f` (bookkeeping; adds `verification.json`, 08:40:52Z) →
`b563c79` (outside spot-check, 08:55:02Z).

## 1. Backing inventory — this is the entire support for the boolean

| Anchor | Content | Backs temporal stability? |
|---|---|---|
| `verification.json:2` | `source_revision` string | No; names one revision, no worktree assertion |
| `verification.json:3` | `baseline` string | No |
| `verification.json:4` | single `executed_at_utc: 2026-10-20T08:36:33Z` (second precision) | No; one file-level instant, not declared start/end, not tied to the map |
| `verification.json:5-396` | 22 command records; key union exactly `argv, cwd, exit, label, stderr, stdout` | No; zero per-command timestamps and zero per-command pin checks |
| `verification.json:397-418` | 20 entries, each `path → bare 64-hex digest` | No; no size, no `mtime_ns`, no capture time, no revision tag |
| `verification.json:419` | `"pins_unchanged_during_run": true` | The claim itself |
| `verification.json:420` | `evidence_scope` prose | No; does not mention pins or any snapshot |

Observed, exhaustively: a recursive key walk over the parsed file yields **one** key matching
`pins_|mtime|size|before|after|pre_|post_|taken_at` — `pins_unchanged_during_run` itself. There is no
second observation of the 20 files anywhere in the receipt, and none of the 22 command stdouts contains
the map key name or any of the 20 map digests (all 20 checked: 0 present).

Observed: the key is **not produced by any tool**. `git grep` at `2fc1d6f` and `git log -S
'pins_unchanged_during_run'` across all refs find the literal only in `verification.json` (the add at
`2fc1d6f`) and in the spot-check's quotation of it (`corpus/lessons/round-16-verifier-spotcheck.md:183`).
No committed script writes `verification.json`, and the two earlier receipts carry no pin field at all
(`.ufo/waves/round-14/verification.json` keys: `revision, commands`; round-15 adds inventory keys only).
The boolean is an L1-authored assertion; there is no measurement path to it.

## 2. What the map does certify (observed, recomputed here)

- **20/20 digest match with A.** For every map path, `sha256(git show A:<path>)` equals the recorded
  value; 0 mismatches. The spot-check's own computation says the same at
  `corpus/lessons/round-16-verifier-spotcheck.md:108` ("identity comparisons … not … proof of temporal
  stability").
- **14/20 paths did not exist at B.** `.ufo/waves/round-16/{selection,selfcheck,measure,controls}.py`,
  `selection-fixtures.json`, `negative-fixtures.json`, and the eight `w2/*-cases.json` were created in A;
  no baseline identity exists for them, so no B→A comparison can bound them.
- **6/20 pre-existing paths are byte-identical B→A** (recomputed): `.ufo/waves/round-14/tools/
  quote-fidelity.py`, `.ufo/waves/round-14/fixtures/expected.json`, `.ufo/waves/round-15/
  boundary-fixtures/expected.json`, and the three `.ufo/gates/citation-drift/*` files. That is a
  two-revision comparison, not an interval observation.
- **Partial independent cover.** `controls.py`'s `frozen_baselines` (`controls.py:35-39` prefixes,
  `:169-177` `unchanged_report`, `:201-207`) reports 126/126 pre-existing frozen/evidence blobs
  byte-identical B→A. It covers only 3 of the 6 pre-existing pinned paths; the citation-drift files are
  outside its prefixes.
- **The carrying commit does not touch them.** `git diff --name-only A 2fc1d6f -- <20 paths>` is empty,
  so the digests also equal the blobs at the commit that publishes the receipt.

[INFERENCE] A was committed 38 s before `executed_at_utc` and the receipt was committed 4 m 19 s after it;
the run most plausibly started from a clean worktree at A. No retained command records `git status` or
`rev-parse`, and nothing records when the map was taken, so even "worktree was A at run start" is
inference, and the map's capture instant is unknown (pre-run, post-run, or interleaved).

## 3. What it cannot certify

1. **No bracket.** With one map there is no pair of instants to compare, so the record is compatible both
   with unchanged bytes and with a file changed and restored between any two observations. It cannot
   distinguish the claim from its negation.
2. **No capture time.** `executed_at_utc` is not shown to apply to the map; no entry has its own timestamp.
   The receipt cannot place the observation relative to the 22 commands.
3. **No provenance for the digests.** A digest read out of Git (`git show A:path`) is byte-identical to a
   digest computed from an equal worktree file. The record cannot show which source produced the map, so
   even "a worktree file was hashed" is unrecorded. [INFERENCE] a `sha256sum`/Python pass over the worktree
   is the most plausible production, but no retained artifact selects it.
4. **Coverage is narrower than the run.** The 20 paths exclude the installed Ghidra data tree
   (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`) that labels
   `selection-*` read. Those 10 invocations do retain read-time size+SHA-256 of the selected base/diff files
   inside stdout (`selection.py:144-153` streamed hash; 9 labels have a base digest, 6 a diff digest,
   `selection-1.26.8` has neither), but that is input identity at read time, not a before/after equality,
   and it does not cover the root listing or the selfcheck/measure/controls inputs.
5. **No continuous record.** Even a true pre/post pair would support "identical at each recorded instant"
   only; "throughout" needs a change-notification record with a stated gap bound, which does not exist here.

## 4. Strongest truthful replacement sentence

Use verbatim as the R16-PROVENANCE correction lemma:

> The recorded `producer_and_fixture_sha256` values match the committed blobs of all 20 named paths at
> source_revision `27b8fc13156230981312c44380cddab1f2bd318d` (20/20, recomputed from Git objects); no
> pre/post snapshot, capture timestamp, per-file size or `mtime_ns`, or producing command was retained, so
> the record cannot distinguish "pins unchanged during execution" from a run in which a pin changed and was
> restored.

Compact admissible form for space-constrained docs (matches the route's own wording at
`round-16-verifier-spotcheck.md:183`): **"Map matches committed source-revision blobs; temporal stability
not evidenced."**

If L1 prefers a field-level replacement rather than prose, the truthful shape is
`pins_map_matches_source_revision: {matched: 20, of: 20, revision: "27b8fc13…", temporal_stability:
"not evidenced"}`. The filed bytes must not be rewritten; the append-only correction should quote one of
the sentences above and name this path.

## 5. Sites where the sentence must land (lane, at HEAD)

- `LOG.md:2012` — "Producer/fixture hashes remain unchanged across execution."
- `corpus/lessons/round-16.md:154` — "All producer/fixture pins remained unchanged during execution."
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` — "Producer and fixture pins were unchanged
  during the run."
- `.ufo/waves/round-16/verification.json:419` — the boolean (annotate only; do not rewrite bytes).
- Outside lane: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60` — "Producer/input
  hashes stayed unchanged during execution." Operator/aggregator only.

`SCORECARD.md` contains no during-run statement (its r16 section has only change-scope and two-revision
"unchanged/byte-identical" wording); the route's enumeration at `round-16-verifier-spotcheck.md:183`
naming the scorecard is imprecise, and it omits the knowledge entry, which is a real site.

## 6. Calibration notes on the route and the round-17 sweep (adjacent, confirmed independently)

1. **Sweep regex gap.** Contract `contract.md:91-93` matches `unchanged during|remained unchanged during|
   stable throughout|pins_unchanged_during_run`. Applying that regex in Python to HEAD yields exactly 2
   lane sites
   (`corpus/lessons/round-16.md:154`, `verification.json:419`). `LOG.md:2012` says "unchanged **across**
   execution" and is missed; the widened phrase scan yields 4 lane sites. Without widening, C1's
   "unqualified sites N→0" (`claims.json:12`) can go green while the LOG overstatement stands.
   `ScoutTemporalWording.md` reports the same gap; this check reproduces it directly.
2. **Sweep scope gap.** The contract scans LOG/SCORECARD/lesson-16/SKILL/`verification.json`; it does not
   scan `corpus/knowledge/`. The knowledge statement at `:95` therefore needs `--extra` or a scope
   extension, not just a correction line.
3. **"No per-command hashes" is imprecise.** `round-16-verifier-spotcheck.md:183` says there are none, but
   the 10 `selection-*` labels retain read-time size+SHA-256 for each selected base (9) and diff (6) in
   stdout. The accurate statement is
   "no per-command *equality check across instants*"; the read-time identities exist and should not be
   denied in the correction.
4. **Boolean naming.** The key asserts an interval property while the record is a single map; even renaming
   it would not make it a measurement. Only `pins.py`-style pre/post snapshots (`contract.md:12-21`) can
   support a future "unchanged" claim, and even then only "identical at each recorded instant".

## 7. Residual risk and verification gaps

- The truth of the boolean is unknowable from committed bytes; this review establishes only that the
  receipt does not evidence it. Nothing observed suggests the pins did change; nothing observed excludes it.
- The map's generating command, capture instant, and whether it read the worktree or Git are unrecorded;
  a fabricated or Git-derived map would be indistinguishable from a measured one.
- Counts and equalities above are reproducible from Git objects only:
  `sha256(git show 27b8fc1:<path>)` for the 20 paths; `git diff --name-only 27b8fc1 2fc1d6f`; recursive key
  walk of the receipt; `git log -S 'pins_unchanged_during_run'`.
- No tool installs or upgrades were made.
