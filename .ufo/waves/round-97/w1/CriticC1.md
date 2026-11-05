# CriticC1 - adversarial attack on R97-C1 (verify_receipt v7 at L 867ed98d)

Seat: CriticC1 (critic, leaf). Scope: forged receipts against `verify_receipt` (v7) imported with
`python3 -I -B` from a scratch clone at 867ed98d. No lane write, no frozen file touched.
Receipts: `.ufo/waves/round-97/w1/CriticC1/*.json` (JSON only; `real-public-run-*.json` are the
two genuine public-CLI runs). Driver: `$HYAKU_SCRATCH/kaidoku-r97/CriticC1/attack.py`, `attack2.py`.

## Modes
- **spec**: `verify_receipt(p, FROZEN_LABEL, L, 6, pins, pins_at_rev=blob pins at L, repair_cmd=frozen)`.
  Pins and pins_at_rev are both `git cat-file blob` digests at L (the item's blob_sha256 path).
- **main**: `main()`'s self-verify replica. `rev_full` = named rev; `pins_at_rev` = blob digests
  at that rev, **None when any named file is absent there**; `pins` = live worktree digests.

## Table

| candidate | ok | reasons | finding |
|---|---|---|---|
| L-honest (control, spec and main) | yes | - | positive control |
| A base-pins-at-L (spec): counter/verdict/repair = base blobs | no | byte-pin-not-bound:counter | refused |
| B met True, label + " " (spec) | no | label-shape-unparsable, label-not-frozen | refused |
| B2 met True, label + "\n" (spec) | no | label-not-frozen | refused by the frozen-label compare only; LABEL_RE `$` accepts a trailing newline (nit, not admitted) |
| C counts.wrong = true (spec) | no | counts-type:wrong | refused |
| C2 counts.unsafe = 0.0 (spec) | no | counts-type:unsafe | refused |
| D revision = head = 39-hex prefix (spec) | no | revision-not-bound, head-not-bound | refused |
| D2 same, rev_full from receipt (frozen-harness style) | no | head-not-bound | refused, but only by head; the harness cannot fire revision-not-bound |
| E repair_sha256 of altered bytes, repair_cmd frozen (spec) | no | byte-pin-not-bound:repair | refused |
| E' repair file dirty in worktree (main) | no | byte-pin-not-bound:repair | refused |
| F imported_v2 = frozen pin, imported_r92 = '1'*64 (spec) | no | imported-pin-not-bound:imported_r92_battery_sha256 | refused |
| G revision = head = base 2a54af07, receipt pins = live L bytes (main) | **yes** | - | **F3** |
| G2 as G, counter = v6 base blob (main) | no | counter-pin-not-bound | refused (fail-open needs live pins to match) |
| H exit = 1 with met_target True (spec) | **yes** | - | **F4** |
| I tool/verdict_counter swapped (spec) | **yes** | - | **F4** |
| J duplicate "public_met" key, false then true (spec) | **yes** | - | **F5** |
| K hand-copied honest receipt, no run (spec) | **yes** | - | **F6** |
| M imported_v2 file dirty, receipt names clean L (spec) | no | imported-pin-not-bound:imported_v2_sha256 | refused under blob pins |
| M imported_v2 file dirty, receipt names clean L (main) | **yes** | - | **F2** |
| N repair file dirty (main) | no | byte-pin-not-bound:repair | refused |
| O counter file dirty (main) | no | byte-pin-not-bound:counter | refused |
| P1 real public-run receipt, five extra count keys removed, clean (main) | yes | - | control: the honest shape passes once the counts gate admits it |
| P2 as P1, imported_v2 dirty (main) | **yes** | - | **F2** |
| P3 as P1, revision = head = 2a54af07 base (main) | **yes** | - | **F3** |
| real public run at L, clean tree (CLI, `exit 1`) | no | counts-extra-key x5 | **F1** |
| real public run, imported_v2 dirty (CLI, `exit 1`) | no | counts-extra-key x5 (dirty imported not reported) | **F1** (F2 masked by F1) |

## Findings

**F1 [high] The public CLI cannot reach exit 0 on the real battery; the honest leg is stubbed.**
Real run at L (5 s): `stop-boundary-repair-battery-v7.py --rev 867ed98d ... --json-out` gives
`selfverify ok=False reasons=5`, `met True exit 1`, reasons `counts-extra-key:{fresh_far,
fresh_far_refused, fresh_repaired, refused, silent}`. Cause: `v3.score` builds 14 count keys
(`tools/round-93/stop-boundary-repair-battery-v3.py` lines 291-305); v7 allows only 9
(`COUNT_KEYS`, line 55; `count_problems`, lines 140-155). Every real run is refused. The kill-rule's
"honest accepted" and `K-dmain pos`, `K-wlink`, `K-bytes` legs replace `v3.score` with 9-key
literals (`kill-rule-v3.py` lines 240-267, 314-326, 422-430), so command A's exit 0 never passes
through the real verdict counts. The v7 docstring's "claim's evidence is the public CLI run" is
therefore not what command A measures. Consequence: the R97-C1 calibration "honest accepted 1 of 1"
is evidence of the stub, not of the battery.

**F2 [high] Imported instrument pins are not bound to revision bytes; a dirty measurement under a clean name is admitted by `main()`.**
`main()` builds `pins["imported_*"]` from the live worktree (lines 515-526), `pins_at_rev` covers only
counter/verdict/repair (lines 498-507), and `verify_receipt` compares imported pins only against
`pins` (lines 224-230). The verdict loads `stop-boundary-repair-battery.py` from its own directory
(v3 line 53/77) and `stop-boundary-battery-v2.py` from the worktree root (v3 line 328), so a dirty
imported file changes the scoring while the receipt names L. Refused under blob pins (spec, M); admitted
under main() self-verify (M, P2). This is the M96-a class the v7 docstring says it closed.

**F3 [high] The byte binding fails open when any named file is absent at the revision.**
`main()` sets `pins_at_rev = None` when `git cat-file blob <rev>:<path>` fails for any of the three
files (lines 502-505). `verify_receipt` then uses live pins (line 208) and skips the dirty-tree check
(lines 216-221). `tools/round-97/...v7.py` is absent at base 2a54af07, so a receipt naming the base
with live L bytes passes (G, P3). A hand-written receipt that names an older revision therefore
escapes the byte binding entirely. Secondary: `want is None` skips the check (line 211) when a key
is missing from a caller-supplied `pins_at_rev`; unreachable from `main()`, latent for other callers.

**F4 [medium] Fields outside the bindings are unchecked.** `exit` (inconsistent with `met_target`),
`tool`, `verdict_counter` (names swapped, digests unchanged), `fresh_cells` and the other extras are
never verified (H, I admitted).

**F5 [medium] Duplicate JSON keys are silently last-wins.** `json.load` keeps the final value (J
admitted with `public_met` false then true). A first-wins reader of the same bytes disagrees; the
verifier neither refuses nor reports duplicates.

**F6 [medium, design] A hand-written receipt that satisfies every binding is admitted (K).** The
verifier re-derives nothing: counts, label and met are self-asserted and checked only for internal
consistency. The forgery battery therefore shows that listed defects are refused, not that a receipt
reflects a run. Related: the frozen battery's `c_verify_forgeries` passes `rev_full = rec["revision"]`
(kill-rule-v3.py line 180), so `revision-not-bound` can never fire there; only `head-not-bound` covers
revision in the battery.

## Notes for the integrator
- Once F1 is fixed by widening `COUNT_KEYS` to the 14 real keys, P2 and P3 become exit-0 paths unless F2/F3 are fixed first (they were not executed end to end as exit 0; the CLI currently stops at F1).
- Candidates D, E, F, M, N, O, G2 overlap the frozen battery's classes (head, repair-pin, imported-pin, dirty tree); D, B, C and A are new combinations and all refuse.
- Clone restored to clean after every mutation (`git status --short` empty). Scratch removed at exit.
- Tooling: none installed. Reads and python3 3.14.8 (`-I -B`) only.

## Verdict
6 findings (F1-F6): 3 high (public CLI never reaches green on the real counts; imported pins unbound to revision bytes; byte binding fails open on an absent pinned file), 3 medium (unbound fields, duplicate keys, self-authored receipts admitted).
