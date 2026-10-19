# Proposed entry-text fixes — CR-2 critic, arc3-loop1-round3 (C1 chain)

Seat CR-2. Target of these fixes: `.ufo/waves/arc3-loop1-round3/claims/c1/records-drafts/knowledge-entry-draft.md`
(SC-2 scribe draft; revisions read: rev 2, 106 lines, sha256 `b9ca0310ca7ef099…`
at 13:14Z, and **rev 3, 108 lines, sha256 `9b0cb5b8459313f7…` at 13:20Z** — the
draft is under active revision; **all findings below still present at rev 3**,
apply by content match, not by line number).
and `records-drafts/map-token-patch.md` (sha256 `333ca590716b2712…`). **Not applied
by this seat** — no corpus file touched. Apply by content match, not by line
number (the draft is under active revision). Where the draft's own line numbers
are named below they are from the revision I attacked.

All receipts re-derived first-hand by CR-2: this seat's carriers and probes under
`claims/c1/CR-2/evidence/` (see `attack-notes.md` for the full battery), plus
re-derivations against the draft's own artifacts (EX-04/05/07/10 files read
read-only; sha256 recomputation and byte-level census).

## F1 (sustained — internal contradiction, draft line 42, final sentence)

**Before:**
> All were recovered K/K. r1's `60003560e01c`-class and non-binary prologues remain unvisited this round.

**Problem.** The round *did* visit both classes, by the entry's own evidence:
- r1's `60003560e01c`-class control carrier-A was re-probed **this round** —
  draft lines 32/45 say so, and `EX-07/legA-hex-6.4.0.json`'s
  `normalized_result.bytecode.hex` begins `60003560e01c8063a9059cbb1460265780…`
  (84 B, sha256 `a92ba152…`, 3/3 recovered at 3 pins × hex/raw).
- The non-binary (linear `EQ`-only) compare tree was visited this round:
  Rv2TokenOpt's runtime `ed6c8a76…` contains 5 `8063<sel>146` EQ compares and
  **0** `8063<sel>116` GT compares — a linear chain, recovered 5/5 (draft line 39).
- Draft line 47's Unknowns also assigns `60003560e01c` to r1 as a *known* class,
  reading against line 42's "unvisited this round".

**After (proposed text):**
> All were recovered K/K. The round also re-probed r1's `60003560e01c`-class
> control (carrier-A, `60003560e01c8063a9059cbb146026…`, 3/3, below) and the
> linear `EQ`-only compare tree (Rv2TokenOpt, 5 selectors, 5/5). Prologue
> classes other than `5f3560e01c` and `60003560e01c` remain unvisited.

**Receipt:** byte counts from this seat's census (`CR-2/evidence/shape-analysis.txt`),
quote of carrier-A's head from `EX-07/legA-hex-6.4.0.json`.

## F2 (sustained — citation overclaim, draft lines 20 and 51)

**Before (both lines):** `` `optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}{,-rerun}.json` ``
expands to 12 files of which 6 are `*-rerun`; only **one** rerun exists
(`EX-07/optB-hex-6.7.0-rerun.json`; `ls EX-07 | grep rerun` →
`legA-hex-6.4.0-rerun.json`, `legA-hex-6.7.0-rerun.json`, `legC-*`, `optB-hex-6.7.0-rerun.json`).
Five cited files do not resolve (QUALITY.md row 1 risk at landing).

**After:** `` `optB-{hex,raw}-{6.4.0,6.5.0,6.7.0}.json`, `optB-hex-6.7.0-rerun.json` ``

## F3 (sustained — wrong path, draft lines 28 and 51)

**Before:** `` `EX-04/evidence/planted-B.txt` sha256 `f32393c0…` ``
**After:** `` `EX-04/planted-B.txt` sha256 `f32393c0…` ``
**Receipt:** the file with that hash lives at `claims/c1/EX-04/planted-B.txt`
(467 B, sha256 `f32393c0…` re-derived by this seat); there is no
`EX-04/evidence/planted-B.txt`.

## F4 (sustained — wrong path, draft lines 36 and 51)

**Before:** `evidence/offset-check-*.json` (line 36, EX-04 context) and
`` `EX-04/evidence/offset-check-{opt200,noopt}.json` `` (line 51)
**After:** `evidence/probe/offset-check-*.json` and
`` `EX-04/evidence/probe/offset-check-{opt200,noopt}.json` ``
**Receipt:** both files exist under `EX-04/evidence/probe/` (`ls` output in this
seat's session; `EX-04/evidence/offset-check.js` is the only offset-check under
`evidence/` itself — the script, not the outputs).

## F5 (advisory — state the creation-identity convention)

The three "creation" hashes in the draft are sha256 over the **decoded** creation
bytes, not over the `.hex` files; for CarrierB@EX-05 no `.bin` artifact is
published, so a verifier hashing `CarrierB.creation.hex` gets `6de2e96e…`, not
`6794c3a2…`. All three reproduce as decoded-byte identities (re-derived by this
seat): VaultB opt200 decoded 1,655 B `ac614a6e…` (also `.creation.bin`),
carrierB@EX-04 decoded 2,237 B `8466da5f…`, CarrierB decoded 1,560 B `6794c3a2…`.
The r1 entry's "creation blob 3,942 B `e6517fb7…`" is the **`.hex`-file** hash
(this seat re-derived it) — so the two entries in this family use different
conventions.

**Proposed sentence (once, after the carriers block):**
> Creation identities are sha256 over the decoded creation bytes (`.bin` where
> published, else decoded from `.hex`; e.g. `VaultB.opt200.creation.hex` itself
> hashes to `aeab7960…`).

## F6 (landing condition — identity sidecar; RESOLVED)

The draft's final-identity row points at `claims/c1/SC-2/README-identities.txt`.
At 13:14Z that file was absent; **at 13:20Z it is present** — resolved, no fix
needed. The two recheck captures were already present and both re-derive:
`05f76b33…` / `f2aec424…`, verified byte-identical to this seat's own runs.

## F7 (advisory — shape-vs-optimizer wording; title/stem)

The title and stem say "optimizer-enabled … dispatch shapes". Measurement
(this seat and the draft's own pairs): the optimizer does **not** change the
dispatch shape class or selector order. First byte difference between
optimizer-off and optimizer-on runtimes: VaultB 0x31, carrierB@EX-04 0x0b,
Rv2TokenOpt-vs-r1 0x32, CrVault 0x26, MutMix 0x26, CrWide/OptVault 0x0b —
always after the prologue + leading compare(s); the linear-vs-binary split
tracks selector count (the 22-selector carrier is binary even with the
optimizer off). What held under the optimizer is selector recovery on different
bytes, at a smaller size class.

**Proposed sentence (line 42 or the Inference):**
> The optimizer left the dispatcher shape class and selector order unchanged —
> for this round's own pairs the first byte difference between optimizer-off and
> optimizer-on runtimes falls after the prologue and leading compares (VaultB
> 0x31, carrierB@EX-04 0x0b, Rv2TokenOpt vs r1 0x32); the optimizer changed
> bodies, sizes and jump targets, not the shape. The measured variable is
> selector recovery, not a new shape class.

Optional (only if done before landing, since the map token must be paired):
rename the stem/token to `2026-10-19-arc3-r3-evm-optimizer-carriers` in both
`knowledge-entry-draft.md` and `map-token-patch.md`.

## Not defects (attacked, refuted)

- **Recheck line.** Runs byte-identically: 13 functions, decoded `b24a0115…`,
  sealed `ev_d409bd50b370c55c…`, envelope sha256 `05f76b33…` — this seat's own
  run in `/var/tmp/cr2r3/recheck` (disk-backed TMPDIR), envelope sha matching the
  draft's declared and SC-2's capture. The r1 canonical recheck likewise
  (`ev_45849c8b…`, envelope `f2aec424…`).
- **Availability→holding.** No class-level holding claim from declared
  availability; per-carrier envelopes only; Scope sentence carries "no
  availability→holding claim". Both-pin usage is stated per carrier and matches
  the artifacts (EX-04's carrierB legs are 6.4.0-only, and the draft's source
  line says so by naming the files).
- **r1 Unknowns wording.** No "first optimizer-enabled compile" phrasing anywhere
  (r1's Smoke compile was `solcjs --bin --abi --optimize`); the narrow residue
  (runs≠200, viaIR, other prologue classes, size class) is carried in this
  entry's Unknowns; the parent note says the r1 bytes are not rewritten. (One
  optional strengthening: name the r1 Unknowns item explicitly as "narrowed" —
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:29` by stem — so a reader
  can connect the two entries without inferring it.)
- **Map-token row (map-token-patch.md primary variant).** "optimizer-enabled
  non-ERC-20-shaped carriers (arc3-r3)" — plural is supported by the landed legs
  (VaultB opt200, carrierB@EX-04 opt200, CarrierB opt200, CarrierBErr). Line
  neutrality re-rehearsed by this seat: 190 → 190, 1 changed line, token set
  82 → 83, no prior token removed, and a stub-stem overlay reads command-A
  83/83, 14/14, missing [], dangling [] (worktree variant self-tested equal to
  recipe A on the pristine tree).