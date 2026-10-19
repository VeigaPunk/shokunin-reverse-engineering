# SEAT VZ-4 — chain cross — role wave-integrator — LATE JOIN (devin backfill)

Wave `arc3-loop1-round3` · seat VZ-4 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (immobile at every sample; no seat
commits; parent integrates).

Seat line: LATE JOIN. A wave summary may exist at `claims/cross/wave-summary.md`
— read first; verify or rewrite it with the FULL wave story: 64-seat roster; the
token-plan quota interruption at 43/64 reports (44 files incl. one sidecar); the
operator-directed devin substitution for the remaining seats; per-chain
verdicts; custody outcome (incl. the revised-tool pair); parent-facing
admission inputs. Poll the seats dir (60 s, max 25 checks). Final:
`claims/cross/wave-summary.md` + this seat report last.

**Status: COMPLETED the missing work (the late-join rewrite of the wave
summary + this report + the late-join receipts) and VERIFIED existing work
(every identity and claim quoted by the original draft and by the chains,
re-derived first-hand per rule #14).** The real-path writes (custody pair,
pointer table + expected) were read-only for this seat: hash/stat/`git show`
and scratch-copy execution only.

## 1. Work performed (evidence pointers)

**Inputs read first:** `claims-frozen.md` (frozen claims + 64-seat roster);
the pre-existing `claims/cross/wave-summary.md` (the interrupted token-plan
seat's mid-flight draft, 284 lines — archived verbatim by me at
`claims/cross/VZ-4/wave-summary-tokenplan-seat-13z22.md`, sha256
`e7bf9eb2102afcbfd515500c77c05e8e986a360b30dc4d2c2efbdffb06e93b32`); the
three chain verdicts; the seats dir (61 reports + the `EX-28.md.sha256`
sidecar at poll close); the chains' key artifacts.

**Artifacts written by this seat (all under the wave tree, no real target):**

| artifact | what |
|---|---|
| `claims/cross/wave-summary.md` | the late-join rewrite (439 lines; full wave story incl. §9 closing census) |
| `claims/cross/VZ-4/wave-summary-tokenplan-seat-13z22.md` | the archived original draft (byte-preserving copy) |
| `claims/cross/VZ-4/poll-log-late.txt` | my 25 × 60 s poller log (seats census + four real-target hashes per check; closed 13:47:31Z) |
| `claims/cross/VZ-4/late/RECEIPTS-INDEX.txt` | index of the receipts below |
| `claims/cross/VZ-4/late/selftest-22.out` | tool selftest at the landed revision (CLEAN 22/22) |
| `claims/cross/VZ-4/late/c2-injections-late.txt` | the four named holes at `7cd19c3c…` (2/14/14/2 + guard intact) |
| `claims/cross/VZ-4/late/c2-injections-before-base.txt` | the same holes at the base blob `112d01dc…` (traceback 1/1, clobber YES, gate unrecognised) |
| `claims/cross/VZ-4/late/c2-after-suite-late.txt` | after-state suite: selftest, live capture, self-pin, verify, v1 legs |
| `claims/cross/VZ-4/late/instruments.out` | command A (git mode) + probe both modes + pin-check + census at HEAD |
| `claims/cross/VZ-4/late/collision.out` | the C2↔C3 collision end-to-end on a scratch clone (1 → 0 findings) |
| `claims/cross/VZ-4/late/table-reanchored.json` + `expected-reanchored.json` | EX-32's re-anchor re-derived byte-exactly (`a810bd17…` / `e33f0e2d…`) |
| `claims/cross/VZ-4/late/restore-config-pre-pair.txt` | the exact HEAD bytes used to repair my accident (§6) |
| `claims/cross/VZ-4/late/closing-capture.txt` | closing identity capture (real targets + custody 5 paths + git status) |
| `seats/VZ-4.md` | this report |

Scratch: `/var/tmp/vz4r3-late` (mirrors, scratch clone, fixtures, TMPDIRs).
`/tmp` breach disclosed in §6. No git mutation of the real repo; custody paths
read-only; no LOG/SCORECARD/SHONEN/corpus/SKILL/README writes; no install (the
round-1 solc prefix was re-hashed, never re-installed).

**Method.** Late poller (25 × 60 s; seats census + tool/README/table/expected
hashes per check); re-runs of every round instrument at HEAD; the C2 injection
suite on scratch copies of BOTH the base blob and the landed tool + the
after-state suite; the C1 landing projection on a scratch mirror (cross-checked
against RV-4's independent patch application and the c1 verdict rev 3); a
scratch git clone for the collision (local-only git, never the real repo); a
fresh REA probe of EX-04's carrierB; read-only custody capture; the CN-2 v7
fold gates re-run via their own script.

## 2. Proposed changes (patch text / proposed artifacts)

**None authored by this seat.** The wave's proposed changes live in the chains'
trees (indexed in the summary §6): C1 entry-text fixes
(`CR-2/proposed-entry-text-fixes.patch.md` `953b53f2…`,
`CR-1/proposed-entry-corrections.patch.md` `60180c9a…`,
`RV-3/proposed-entry-fixes-rev4.patch.md` `1e191bd8…`), the C1 map token
(`records-drafts/map-token-patch.md`, PRIMARY additive), C2's registry-row
voices (`EX-21/proposed-skill-registry-row.patch`,
`EX-30/registry-row.patch.md` — both rewrite the precedence clause identically),
C3's re-anchor (`EX-32/pointer-table-reanchor.patch.md` `c0b0d2b4…`) and R1 fix
(EX-42 §5.4), the CN-2 records package (`claims/cross/records-outline.md` v1.4
+ merged texts), and the assorted residuals' patch texts. This seat's summary
is the parent-facing index; no additional patch text is proposed here.

## 3. Before → after measurement for this chain's claim (cross: wave
integration)

The cross chain owns no corpus/gate edit target; its "before → after" is the
wave's integration state:

| reading | before (the draft's close, ~13:22Z) | after (this seat, poll close 13:47:31Z) |
|---|---|---|
| seat reports delivered | 43/64 (44 files incl. sidecar; frozen checks 10–16 of the original poller) | **61/64** (EX-14, SC-3 pending; VZ-4 last) |
| chain verdicts | c1 draft only | c1 rev 3 (13:28:26Z), c2 (13:28:08Z), c3 (13:26:15Z) — all VERIFIED |
| custody tool | `7cd19c3c…` (1155 L) | identical — frozen through checks 01–25 |
| README | `f30df42e…` (185 L) | identical |
| table / expected | `bfc42f1b…` / `d97dd60a…` (pin MATCH) | identical |
| command A at HEAD | 82/82, 14/14 | identical |
| probe | 0/0 both modes, selftest 13/13 | identical |
| census | PASS 0/0/0/0 | identical |
| collision | predicted (CN-1 §3g), not yet reproduced by VZ-4 | reproduced + fix verified (§4 A4/A5) |
| CN-2 fold | v5 (`4db10215…` / `103c57da…` per outline v1.3) | v7 (213 L `83772cc4…` / 207 L `6e20b662…`), gates PASS |
| C1 projection | draft-rev-3 pins (`189ac2a2…` / `016b632e…`) | current rev-4 pins (`3b5f371e…` / `a451ad16…`), 83/83, prior-82 identical |

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the draft's C1 projection pins are still current" | **REFUTED** — the draft projected the 13:12Z draft revision; the literal moved to rev 4 (13:17:51Z mtime). My re-run: literal `3b5f371e…` (17,708 B), README after `a451ad16…`, 83/83, prior-82 byte-identical; RV-4's independent application lands the same README; c1 verdict rev 3 and RV-3's rehearsal reproduce the same triple — five independent applications converge |
| A2 | "the D2/D3/write-guard/D6 holes are only claimed closed" | **REFUTED** — I re-ran the injection suite on a scratch copy at `7cd19c3c…`: D6 → 2, D2a/D2b → 14, D3 gate → 2 with `REFERENCE-COVERAGE: 1/5`, write-guard → 2 with victim bytes intact; all declared classes, zero tracebacks. The before side measured by me on the base blob (`112d01dc…`): traceback 1/1, clobber YES, gate unrecognised |
| A3 | "the live pair is stale / one-sided" | **REFUTED** — revised-tool pre `553fe82d…` + post `4969133b…` (both self-pin `7cd19c3c…`): MATCH 5/5 drift=0; both vs live MATCH; sidecars `sha256sum -c` OK; EX-21's own pair additionally verified (MATCH 5/5 cross-verify) |
| A4 | "the C2↔C3 collision is hypothetical" | **CONFIRMED as real, then fixed** — scratch clone at `c07af80` + EX-30 row committed (SKILL.md `03832723…`, scratch commit `f4c520a2`): `citation_dead entry=skill-registry-custody-pair-row`, findings=1 / strict exit 1; with the re-anchor (`a810bd17…` + `e33f0e2d…`): 0 both modes |
| A5 | "the re-anchor neuters the needle" | **REFUTED** — both real rows match the optional-group regex (True/True, my run); CN-2's teeth test (reordered-precedence mutant → citation_dead) reproduced |
| A6 | "the custody paths drifted this wave" | **REFUTED for 4/5; CONFIRMED pre-window for `config.toml`** — mtime 12:57:45Z precedes every wave sample; CU-1/CN-1 independently record the same moved fields |
| A7 | "the CN-2 fold is stale after C2's late revisions" | **REFUTED** — my re-run of their fold script (their §8 step 0) produced v7 texts `83772cc4…`/`6e20b662…`; their refreshed `identity.txt` (13:32:28Z) carries the same digests — two independent invocations agree |
| A8 | "the probe's `findings=0` at HEAD is vacuous" | **REFUTED** — selftest 13/13 (each class fires on fixtures); the collision run fires exactly the pinned entry; tamper/teeth tests across seats |
| A9 | "the instruments moved under the wave" | **REFUTED** — tool/README/table/expected/SKILL/corpus-README hashes identical in every poll sample (checks 01–25 and the original poller to its close); probe and census bytes untouched |
| A10 | "the C1 prior-82 slice moved" | **REFUTED** — 0/82 mismatches vs HEAD blobs in my mirror; 190 → 190 README lines, one line changed |
| A11 | "the table extension clobbers existing entries" | **REFUTED** — object-level diff re-derived by me: 26 added / 0 removed / 0 modified / 0 duplicate ids; `quoted` 4 == 4; exempt prefix-equal; `_doc` prefix preserved |
| A12 | "planted-K was recorded after the probes" | **REFUTED** — mtimes (my stats): EX-10 planted 13:07:24Z < probe 13:08:10Z; EX-05 planted 13:08:11Z < probe 13:08:21Z; EX-04 both 13:08:25.41Z (same-second, documented in its seat report) |
| A13 | "EX-04's carrierB selectors are claimed, not measured" | **REFUTED** — my fresh REA probe: 11/11, zero extras, `dispatch:"abi"`, decoded sha `aaf85cea…` == on-disk runtime digest; set-equal to `planted-B.txt` (`f32393c0…`) |

## 5. Blockers

None for this seat's deliverable. Named gaps carried for the parent (summary
§7): both-sides-absent MATCH ruling; C1 entry-text fixes F1/F2/F4 still open at
rev 4; C3 R1 (`LOG.md:1442`); the §3 collision landing order; sidecar-path /
mkdir residuals; EX-14 + SC-3 reports pending at close (artifacts complete).

## 6. Disclosed accidents (this seat)

1. **Round-1 receipt clobber, repaired.** At 13:25:02Z I clobbered
   `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` by
   mis-ordering `c2-verify.sh` arguments (the receipt was passed as the output
   file). Restored byte-identically from the HEAD blob 53 s later (`git show`
   redirect; sha256 `b8ed1936…`; `git status` clean, re-verified at 13:30Z and
   in the closing capture at 13:36Z). Observed and exonerated by VZ-2 (§R2)
   and RV-9. The parent should confirm the file is not committed in a
   clobbered state — it is clean.
2. **`/tmp` discipline breach.** Two scratch JSONs were copied to `/tmp` during
   the collision test and removed immediately; never used for receipts.
3. **Byte-neutral rewrite of CN-2's artifacts.** While testing CN-2's
   pre-flight recipe I invoked their own fold script (`assemble-merge.py`);
   by design it rewrites `claims/cross/CN-2/merged-{LOG-entry,SCORECARD-section}.md`.
   The regenerated bytes are byte-identical to CN-2's own receipts and to
   their post-run `identity.txt` — no content altered, only mtimes moved.
   Recorded because seats should not write other seats' artifacts even
   byte-neutrally.

## 7. Identity discipline note (rule #14)

Every identity quoted in this report and in the summary was re-derived by this
seat after the last write that could have moved it, or is bound to the
timestamp+command that produced it. The four real targets were re-verified on
disk at 13:48:48Z (after the poll closed): tool `7cd19c3c…`, README
`f30df42e…`, table `bfc42f1b…`, expected `d97dd60a…` — all unchanged. This
report's own identity is deliberately not self-asserted (a fixed point cannot
hash itself; the write that prints it invalidates it) — the parent re-derives
`seats/VZ-4.md` and `claims/cross/wave-summary.md` at landing, per rule #14
and the RV-5 precedent.
