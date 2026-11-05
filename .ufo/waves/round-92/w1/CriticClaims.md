# CriticClaims — round 92, kaidoku (attempt 1, seat critic, leaf)

Scope: adversarial fairness review of R92-C1 (coverage, repair inside a ±16 window) and R92-C2
(calibration, refusal label vs counterfeits). Not a bug audit of the counters. Lane frozen at
declaration `11f8606178dfd9e72001b31daf412c5463106a63` (base `73a882712`), verified by
`git -C <clone> rev-parse HEAD`. All work in a clone under scratch; lane read-only. Scratch deleted
before yield; receipts and cheat sources copied to `.ufo/waves/round-92/w1/CriticClaims/receipts/`.

Pins re-hashed at the declaration clone (match `claims.json`):
`stop-boundary-repair-battery.py` `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`;
`stop-boundary-battery-v2.py` `f6ddb48b4d9cbd460002…`; `tools/round-91/upx-stop-boundary-repair.py`
`3779d35fc8f57bc9f573…`. Packer `upx 5.2.0` (`/usr/bin/upx`) as pinned.

Note on the candidate: `tools/round-92/upx-stop-boundary-search-repair.py` does not exist in the lane
or the declaration clone. Attacks on (a) therefore test the round-91 tool and the packer verdict on the
inputs the candidate would see, not candidate code. The candidate's own ELF gate and search ordering
are unverified here (named limit).

## Summary

| attack | verdict | one-line reason | disposition |
|---|---|---|---|
| (a1) outside-window single-field last-block tamper | SURVIVES | round-91 refuses 16/16 probes; packer green set is `{pristine}` over the full `sz_cpr` range on all five carriers, so no in-window wrong write exists | none |
| (a2) non-ELF input (EI_DATA=2, magic-broken) | SURVIVES (measured) | round-91 refuses rc 2 at its ELF gate; `upx -t` is never green on either variant over the full range | keep the ELF gate ahead of any search (candidate unverified) |
| (a3) non-ELF UPX formats (PE/Mach-O) | NOT MEASURED | host UPX refuses the only PE tried (`CantPackException: unsupported machine 0xfd1d`) | named limit |
| (b) window ±16 chosen after data | SURVIVES as "not fitted to a cliff"; FALSIFIES "far-refused is packer evidence" | sweep data existed (07:47) before declaration (09:10); the data has no cliff, so ±16 is a cap placed in the counter's gap (7, 40). The far arm measures the cap, not the packer | amend the reading (named limit) |
| (c1) named counterfeits A/B/C under v2 | SURVIVES | v2 refuses all three (A, B: intact 4 of 5; C: typed 0), reproduced | none |
| (c2) counterfeit v2 admits: five-carrier carrier-read (D) and five-hash table (E) | NOT-IN-SCOPE (by the claim's own carve-out); headline overreaches | both admitted (met True); both are "unseen-carrier table" class the claim declares not claimed | narrow headline text (named limit) |
| (c3) the A/B kill is by construction of xz | SURVIVES as a mechanism test; FALSIFIES any reading that it is a general calibration | without xz, A/B pass v2's intact arm; xz kills tables that omit it, and a table that includes it passes | named limit |
| (C1-cheat) five-carrier table repair passes the frozen C1 label | NOT-IN-SCOPE (declared), FALSIFIES "repaired 10 of 10 = general capability" | `table-repair-5` met True; four-carrier version fails only on xz | named limit: credit coverage as "five pinned carriers" |
| (d) do-nothing control measures "no work"? | SURVIVES (measures no repair); wording overstates | the control is the round-91 refusal, not a no-op; the identity no-op also fails (repaired 0, far-refused 0) under the same counter | relabel as "predecessor refusal control" in the record |

## (a) Does the window change harm the refusal guarantee elsewhere?

**Measured setup.** For each of the five carriers (jq, xxd, libz, docker-init, unseen xz) I packed
with `upx --best -q` and took the last block from `v2.layout` (the counter's own layout).
Single-field tamper: `sz_cpr` moved to every value `v` in `[1, sz_unc]` (full sweep), and `upx -t` run on
each. Receipt `receipts/p1b-full-green-sweep.json`:

| carrier | sz_unc | tried | packer-green values |
|---|---|---|---|
| jq | 1184 | 1184 | {174} = pristine |
| xxd | 784 | 784 | {163} = pristine |
| libz | 23584 | 23584 | {17012} = pristine |
| docker-init | 27304 | 27304 | {4313} = pristine |
| xz-unseen | 5024 | 5024 | {852} = pristine |

So on every carrier the packer verdict is a unique decision procedure over the whole range, not only
in ±56. Consequence derived from that set (not assumed): for a tamper at `t = p + d`, a window of radius
`R` contains a green value iff `|d| <= R`, and then the only green is `p`. Any window radius below
`|d|` refuses. The ±16 window therefore sets which tampers are repaired; it is not what protects
against wrong writes on these carriers.

**Outside-window input class: last-block tamper, `|d|` in 17..56.** Receipt
`receipts/p1-window-aliasing.json`: for each carrier and each `d` in ±1..±56, the window decision was
`write-pristine` for `|d| <= 16` (32 cells per carrier) and `refuse` for `|d| 17..56` (80 cells per carrier);
`WRONG-WRITE` count 0 and `silent` count 0 on all five carriers.
Against the round-91 tool (not the candidate), run from the clone, `receipts/p2-r91-refusal-probes.json`:
jq and xz at `d = +17, -17, +24, -24, +40, -40, +56, -56` (16 probes) → rc 2, no output file, typed
`stop-boundary ... this class is refused` JSON. Verdict **SURVIVES**: the refusal guarantee outside the
window holds on the measured class.

**Non-ELF input class: EI_DATA=2 (big-endian marker) and magic byte 0 = 0x00 variants, of packed jq and
packed xz with a `+7` tamper.** Round-91 tool: rc 2, no output, `refused: "not a little-endian ELF"`
(`receipts/p2-r91-refusal-probes.json`). Packer verdict over the full `sz_cpr` range on both variants of
both carriers: the pristine variant itself is not green (`upx -t` rejects it) and the greens set is empty
(`receipts/p2b-nonelf-variant-sweep.json`). So the ELF gate is not what the packer enforces here, and a
search without that gate would also refuse on these two variants. Verdict **SURVIVES** on the
measured variants; the candidate still must keep the round-91 ELF check ahead of the search (not verified
— the candidate is not in the lane).

**Not measured (named limit).** A UPX-packed non-ELF file (PE or Mach-O) with a last-block tamper. I tried
`upx --best` on `/usr/share/dotnet/shared/Microsoft.NETCore.App/10.0.13/Microsoft.CSharp.dll`: rc 1,
`CantPackException: pefile: unsupported machine 0xfd1d`. No other UPX-packable non-ELF sample was built.
The only guarantee for that class is the round-91 ELF gate, which the frozen C1 counter does not test.

## (b) Was ±16 chosen after seeing data?

- Timeline (file mtimes, not authorship): ReviewerFalsify results `falsify-search-results.json` 07:47:41;
  ReviewerFalsify.md 07:47:59; `round-92/claims.json` 09:10:14. The sweep data existed before the window
  was declared.
- The round-91 sweep (`w1/ReviewerFalsify/falsify-search.py`, lines 168-174) covered every value in
  `[1, sz_unc]` for jq and xxd and `stored ± 256` for libz and docker-init. It found the same
  structure as the full sweep above. No data point in it has a cliff at 16.
- So ±16 is **not** fitted to a data cliff. It sits in the counter's own gap between the near cells (±7)
  and the far cells (±40). By the derivation in (a), any window radius `R` in `[7, 39]` passes the frozen
  near arm and the far arm; the far arm `far-refused 10 of 10` is satisfied by any `R < 40` and says
  nothing about the packer. A candidate with `R >= 40` would write pristine bytes on the far cells
  (correctly) and fail the far arm.
- Verdict: **SURVIVES** the claim that ±16 is not fitted to data; **FALSIFIES** the reading that the
  far-refused arm is evidence of packer-verified refusal. Disposition: state in the record that the
  window is a coverage cap and that the far arm measures the cap.

## (c) Are the R92-C2 counterfeits the claim's own description?

Reproduced v2 receipts (all at the declaration clone with `--expect "refused 10 of 10; typed 10; unsafe 0; intact 5 of 5"`):

| receipt | label | met |
|---|---|---|
| `receipts/v2-positive-round91.json` | refused 10 of 10; typed 10; unsafe 0; intact 5 of 5 | True (exit 0) |
| `receipts/v2-cheatA-lane.json` | refused 10 of 10; typed 10; unsafe 0; intact 4 of 5 | False (exit 1) |
| `receipts/v2-cheatB-lane.json` | refused 10 of 10; typed 10; unsafe 0; intact 4 of 5 | False (exit 1) |
| `receipts/v2-cheatC-lane.json` | refused 10 of 10; typed 0; unsafe 0; intact 5 of 5 | False (exit 1) |
| `receipts/v2-cheatD-carrierread5.json` | refused 10 of 10; typed 10; unsafe 0; intact 5 of 5 | **True** (exit 0) |
| `receipts/v2-cheatE-table5.json` | refused 10 of 10; typed 10; unsafe 0; intact 5 of 5 | **True** (exit 0) |

Checks:
- CHEAT-B's hash table (4 entries) matches today's fresh pack of jq, xxd, libz, docker-init
  (`e8b6c9e7…`, `1727faf9…`, `a9c544e6…`, `b67ce1bd…`), so the claim's "recomputed from freshly packed
  carriers" statement holds.

**(c1) The named three are refused by v2 — SURVIVES, but the kill is by coverage.** A and B fail only on the
xz intact arm. Without xz, A and B pass v2's intact arm (the same behaviour as under v1). Their tables
are built from the four round-91 carriers and the L1 chose xz as the unseen fifth; xz therefore
defeats the table cheats by construction. That is a fair mechanism test (a table cannot know a carrier it
does not contain), but it is one carrier deep.

**(c2) A counterfeit v2 admits — NOT-IN-SCOPE by the claim's carve-out.** CHEAT-D (carrier-read over all
five carriers including xz) and CHEAT-E (sha256 table of the five freshly packed carriers) both pass v2
(met True). Both are "an unseen-carrier table" in the claim's own Declared limits. Their mechanism is a
table, not `upx -t`, and the claim says these are not claimed. The claim's headline "the refusal label stops
admitting counterfeit refusals" is broader than the measured set; the honest headline is "stops admitting
the three named round-91 counterfeits".

Files: `cheats/cheat_D_carrier_read_5.py`, `cheats/cheat_E_hash_table_5.py`.

## (d) Does the do-nothing control measure "no work"?

- The control receipt (`pre/c1-control-do-nothing-round91-repair.json`) and my re-run
  (`receipts/c1-do-nothing-round91.json`) both give `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5;
  far-refused 10 of 10`, met False, exit 1. Both record counter sha256 `63e9df431f5d…` (the pin) and repair
  sha256 `3779d35fc8f5…` (the round-91 tool). It is the frozen counter, not a different one.
- But the control's repair is the round-91 **refusal**, not a no-op. A true no-op (identity: copy input
  to output, rc 0) under the same counter (`receipts/c1-identity-noop.json`): `repaired 0 of 10; wrong 0;
  unsafe 0; intact 5 of 5; far-refused 0 of 10`, met False, exit 1. The far arm is what separates the two.
- Verdict: **SURVIVES** — the control correctly measures "no repair" (repaired 0 under any non-repairing tool).
  The wording "do-nothing" overstates: the control is the predecessor refusal. Disposition: record it as
  "predecessor refusal control (round-91 tool)".

## C1 counterfeit repair (not one of the four attacks; required by the declared-limit test)

The claim says a counterfeit "that embeds the pinned packed images of all five carriers would pass
`repaired` and is not excluded by this counter". I tested it:

| receipt | label | met |
|---|---|---|
| `receipts/c1-table-repair-5.json` (five pinned carriers, ±16 by value, no packer verdict) | repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10 | **True** (exit 0) |
| `receipts/c1-table-repair-4-no-xz.json` (same, four carriers) | repaired 8 of 10; wrong 0; unsafe 0; intact 4 of 5; far-refused 10 of 10 | False (exit 1) |

The five-carrier table passes the frozen C1 label. The four-carrier table fails only on xz, the same
by-construction pattern as C2. This is the declared limit, now measured. Source:
`receipts/cheats/table_repair_5.py`, `receipts/cheats/table_repair_4_no_xz.py`,
`receipts/cheats/identity_noop.py`.

## Dispositions for the L1

1. **R92-C1 — named limit; do not refuse.** The packer-verdict repair is achievable on all five carriers
   (full sweep: a unique green on each), so the capability is real. The counter cannot tell a search from
   a five-carrier table (receipt above). Record the coverage credit as "measured on five pinned carriers,
   window ±16 as a coverage cap", not as general capability. Keep the far arm described as a cap measure.
   Named limits: (i) five-carrier table passes the frozen label; (ii) non-ELF PE/Mach-O not measured;
   (iii) candidate ELF gate and search ordering not verified in this seat. A fresh-pack oracle is the
   fix, for a later round.
2. **R92-C2 — amend the headline text before the after-measurement; keep the predicate.** Change
   "stops admitting counterfeit refusals" to "stops admitting the three named round-91 counterfeits". Name
   CHEAT-D and CHEAT-E as admitted and out of scope. The predicate
   `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` and the counter stay frozen.
3. **Window reading (b) — amend the record sentence, not the window.** Say the far-refused arm measures
   the chosen cap, not packer refusal.

Not recommended: refusing either claim. Both are fair in their declared scope once the headline and the
window reading are narrowed as above.

## Commands and receipts

Counters (all at the declaration clone, scratch `--work`, `--rev 11f8606178`):
- v2 counter: `python3 -I -B tools/round-92/stop-boundary-battery-v2.py --root <clone> --repair-cmd <cmd> --work <scratch>/work/v2-NAME --rev 11f8606178 --expect "refused 10 of 10; typed 10; unsafe 0; intact 5 of 5" --json-out <scratch>/work/v2-NAME.json`. Exit codes: positive 0, cheat A 1, B 1, C 1, D 0, E 0.
- C1 repair counter: `python3 -I -B tools/round-92/stop-boundary-repair-battery.py --root <clone> --repair-cmd <cmd> --work <scratch>/work/c1-NAME --rev 11f8606178 --expect "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10" --json-out <scratch>/work/c1-NAME.json`. Exit codes: do-nothing 1, identity 1, table-5 0, table-4 1.
- Window and sweep probes (P1, P1b, P2, P2b, P4 table builds, P5 PE) were run from a Python kernel
  against the declaration clone; the outputs are the JSON receipts listed below. The probe code was not
  saved as a file; the receipts record each row's inputs and decision.

Receipts (`.ufo/waves/round-92/w1/CriticClaims/receipts/`):
- `p1b-full-green-sweep.json` — full-range packer-green sweep, five carriers.
- `p1-window-aliasing.json` — window decision per carrier and `d` in ±1..±56.
- `p2-r91-refusal-probes.json` — round-91 tool on outside-window and non-ELF inputs (rc 2, no output).
- `p2b-nonelf-variant-sweep.json` — packer-green sweep on EI_DATA=2 and magic-broken variants.
- `v2-*.json` (six) — v2 counter runs; `c1-*.json` (four) — C1 counter runs.
- `cheats/` — the five counterfeit and control sources used above.

Tooling: no installs or upgrades. No pacman. Host state untouched: no sysctl, namespace or service
change. Lane untouched: no git mutation; `git status` shows other seats' pending files, none written by me.
