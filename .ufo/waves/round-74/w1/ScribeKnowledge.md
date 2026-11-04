# ScribeKnowledge — round-74 wave 1 report

Seat: ScribeKnowledge (scribe) · Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin · 2026-11-04
Frozen state: base `04fdc2c4dbedbe5ee50a069af14310068393233e`, declaration
`b3a7e28089582ce5fb002a1b88e5295caf696b9f`, freeze `021914c0e638454e507087accfe41af1ab69f185`.

## Behavior (what was produced)

New file, owned this round, no other seat edits it:

- `corpus/knowledge/2026-11-04-r74-probe-mutation-closure.md` (10 616 B, 130 lines)

The entry records R74-C1: what the round-73 MutProbe found (six A12 selftest
survivors on the landed round-73 probe), what each round-74 case binds and
which seam it needs, the exact counts, and the limits. Provenance trio
`source:` / `verified-at:` / `recheck:` are line-start fields at lines 3–5
(QUALITY row 131 position check).

## Acceptance evidence (all exercised, not assumed)

1. **Trio position.** Title line 1; `source:` line 3, `verified-at:` line 4,
   `recheck:` line 5 — all line-start inside the first 12 lines (verified by
   re-reading the written file).
2. **Cited paths resolve at the freeze.** Checked every lane path the entry
   cites against `git show 021914c0:<path>`: claims.json, plans/round-74-claims.md,
   the five pre receipts, MutProbe results.json, c1-at-landing.json,
   probe-mutation.py, both seam-probe.py blobs, corpus/SOURCES.md, corpus/QUALITY.md,
   and the round-73 knowledge entry all exist at the freeze; all except
   corpus/SOURCES.md are byte-identical to the working tree (SOURCES.md differs
   only because ScribeRows' rows S278–S282 landed after the freeze — disclosed
   as such in the entry; the S278 row is anchored at the freeze by the frozen
   `frontier.sources_row_opened` field of claims.json).
3. **Numbers re-derive from committed receipts** (each named in the entry's
   counts table): pristine 14 / killed 4 / survivors 6 →
   `.ufo/waves/round-74/pre/c1-base-arm.json`; origin 4/6/0 with pristine 14 →
   `.ufo/waves/round-73/w1/MutProbe/results.json`; pristine 20 / killed 10 /
   killed_wrong_case [] / survivors 0 / pin matched →
   `.ufo/waves/round-74/pre/c1-post-at-declaration.json`; the two target
   digests `81d6a432…` (r74 probe) and `9c286fd7…` (r73 probe) equal the
   frozen `instruments` and `loaded_by_counter` pins in
   `.ufo/waves/round-74/claims.json`; live-A12 12 of 12 →
   `.ufo/waves/round-73/l1/scores/c1-at-landing.json` (cited as separate
   evidence). Case-internal literals (pids 10/11, parents [9001, 9002]) are
   attributed to the frozen instrument text, not presented as measurements.
4. **S278 citation.** Quote: "Use the caller's filesystem UID and GID (see
   credentials(7)) or effective capabilities for LSM checks." — 15 words
   (≤25), verified byte-for-byte against the ScribeRows snapshot
   `.ufo/waves/round-74/w1/ScribeRows/ptrace.2.html` lines 1437–1439 (read
   directly; not copied from the row). Located anchor named: section
   "Ptrace access mode checking" (heading verified at snapshot line 1404).
   S275/S277 cited for the channel, matching the round-73 entry's usage.
5. **Limits name the selftest-only scope** as the first Limits bullet, plus:
   survivor = coverage finding, never permission to weaken the contract;
   ten declared classes only (a floor, not completeness); base-arm target
   unpinned per the frozen predicate.

## Provenance

- Read-only git only (`git show <rev>:<path>`, `git rev-parse --show-toplevel`
  printed the lane root before any command). No git/jj writes anywhere; no
  commits; no fleet-root writes; no sibling-lane or state-dir writes.
- Tools installed: none. Scratch dir: none created (all reads in-lane; both
  writes are lane files named by the seat spec), so there is nothing to clean.
- Per-mutant `expect_case` mapping and the seam names
  (`kernel_witness` injectable readers + one deterministic pass,
  `forged_subrun`, `assemble_arm`) were read from the frozen instruments
  `tools/round-74/probe-mutation.py` (R73/R74 tables, `classify`) and
  `tools/round-74/seam-probe.py` (defs at 482/655/668; selftest cases
  `a12-genuine-canary-only`, `a12-proc-environ-unreadable`,
  `a12-kernel-multiple-samples`, `a12-kernel-canary-field`, `a12-arm-wiring`,
  `a12-arm-forged-executed`).

## Coordination

- ScribeRows-3 asked twice over IRC whether I own the S278 `used-by` target
  (their census exits 1 on E11 until the file exists). Answered: yes, path
  confirmed; pinged after the write succeeded so their final census runs once,
  after the dependency exists.

## Conflicts / findings

- None blocking. One nuance recorded in the entry: the MutProbe origin run
  hashed the round-73 probe as `7264d0c8…` (its state during the round-73 w1
  run, `source_unchanged true`), while the landed round-73 blob is `9c286fd7…`;
  the frozen base arm re-applied the same ten classes to the landed blob and
  reproduced the identical 4-killed/6-survivor shape, so the claim's operative
  statement rests on `c1-base-arm.json` and MutProbe is cited as the origin.

## Out of scope (not mine)

- SOURCES.md rows (ScribeRows), the lesson (ScribeLesson), the SCORECARD
  round-74 section (L1), any instrument or receipt edit, any live re-run of
  the battery (the receipts are frozen; I re-derived, never re-measured).
