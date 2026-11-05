# ReviewerC1 — R90-C1 review (round 90, kaidoku)

Seat: ReviewerC1 (reviewer, leaf). Read-only on the lane tree; all runs in
`/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/`, receipts under
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ReviewerC1/receipts/`.
No installs were performed; host toolchain used as pinned
(upx 5.2.0 sha256 `cf2f6e…` verified, bwrap 0.13.1, node v24.21.0, REA pkg at
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, package.json sha256
`a5003…` verified).

## 1. Declaration receipt re-derived from its own bytes — PASS

Receipt: `.ufo/waves/round-90/pre/c1-candidate-at-declaration.json` (711 lines).
Recomputed per cell and per control from the raw arms — see
`receipts/recomputed-at-declaration.json`. Results:

- `recovered_from_cases` recomputed from the `arms` arrays: P1 6/6, P2 4/4, P3 4/4 —
  matches the receipt's `recovered` field exactly; zero arm-level cell mismatches.
- Blind population (`controls.carrier_blind.cases`): all 6 recomputed `recovered`
  from the arms (`rea_recover` null → blind cells score on the 4 non-REA arms),
  blind count == unblinded P1 count (6), `probe.seen` hashes all equal the decoy
  hash `36767…2936e`, 4/4 entries. Blinding arm is internally consistent.
- Controls recomputed: N1/N2/N3/isolation/no_work/blind_ok/cheat_live/cheat_killed
  all `true` — matches `controls_ok` verbatim; N2 rows all carry `rc 0`,
  `packer_clean false`.
- Module pins recomputed from the receipt's `pins.modules` and `claims.json`
  instruments: battery `8466…8206`, repair `aaf3…590b`, cheat `faaf…b826`,
  r87 `96da…ec24`, r88 `59ee…0b46`, r89 `41f2…b1d5d`, upx `cf2f…c969`, REA pkgjson
  `a500…0a6c` — every pin matches the tree at `fc52cc9dc` (receipt path resolution:
  the repair's own `ROOT` = repo root, verified by the pin walk).
- Cosmetic only: the receipt's `label` is normalized (`P1 6 of 6; P2 4 of 4;
  P3 4 of 4`) while my recomputation from case keys renders the long form
  (`P1-later-block 6 of 6; …`); identical substance, no falsification.

No discrepancy found. The receipt's numbers are what its bytes say.

## 2. False-green hunt — no path found; two near-misses worth recording

My harness rebuilt the battery's exact population from the pinned carriers
(sha measurement in the transcript; my packed bytes match the packaging of the
declaration `pins` like-for-like per carrier — jq `e8b6…7268a`, xxd `1727…9f8ff`,
libz `a9c5…5da5b`, dinit `b67c…4bc7`), tampered block 1 both directions
(store −7 / +7, verified inside `sz_unc`), and ran the following probes:

a) **Copy the input unchanged when the tamper is a no-op (libz)** — a no-op
   "repair" on the libz P1 cells returns the tampered bytes; `upx -t` on that
   output fails (rc 1, both directions), so identity against the intact packed
   bytes fails too. Not a false green (`receipts/A-libz--7.log/.info`,
   `receipts/attack-results-all.log`).
b) **Copy-attack (block body relocated to EOF, `sz_cpr` rewritten to the offset
   distance, ZERO bytes retained in the original sphere)** — the genuine r90
   repair refuses (rc 2) all 6 of these inputs (`receipts/B-*.run2`: 5 rc=2
   "no validated PackHeader in the tail window", 2 docker-init rows rc=0 but
   `upx -t` rc 2 → not recovered). The P1 windows reject it.
   One docker-init B row reached `class field-value, derived 440, delta 214` —
   because my copy-attack relocation shifted a *different* plausible successor;
   `upx -t` kills it (P1's `test_ok` false). No false green.
c) **Sibling-plant attack (repair writes `out` + a sibling file and returns
   otherwise-valid bytes)** — an extra seeded file in the box appears in the
   post-exit listing, so the ISO control's `box_after in (['in'], ['in','out'])`
   arm rejects any invocation that plants (`scripts/isolation_cheap.py` output,
   `receipts/isolation-cheap.txt`: pre-seeded sibling ⇒ box_after includes it ⇒
   `catches_extra: true`).
d) **Repair that only fixes block 0 on a later-block tamper (round-89 composition
   alone)** — runs a real block-0 law over the tampered later-block b1 file;
   its output differs from the tampered input by 0 bytes (mismatches intact) and
   is `upx -t` red on itself: P1's `test_ok`/`identity` refuse it
   (`receipts/fixblock0-cheap.txt`, `receipts/fixblock0.log.scratch`). Not a false
   green.
e) **Returning the decoy in the blind arm** — the counter's blind arm re-scores
   P1 with `dea_recover` deliberately null (out of scope for review) and a
   probe of the four carrier paths (all resolving to the decoy, from
   `/usr/bin/jq` etc. through bwrap) showing ALL paths yield the decoy hash;
   the cheat control's `unblinded=true / blinded=false` pair in the receipt
   corroborates (`recomputed-at-declaration.json`),
   and I did not design a repair that could see through the blinding.
   **Gap:** I did not re-run the full battery blind in my seat (declaring the
   blind arm is the counter's job; my run-root substitution would have needed
   a full 4-carrier pack to be equivalent, and the L1 stop order arrived).
   The one blind-adjacent attack I *did* run (copy-attack, which is blind to the
   intact pairs) was refused; I treat this as partial support, not proof.
f) **`upx -t` on a re-packed carrier** — for the cheat family: the declared
   cheat uses the packer deterministically live; in my harness the same
   `upx --best` on the pinned sources reproduced my (and the battery's) packed
   bytes, so a cheat that matches my packing would match the battery's too and
   would still be killed blinded by the receipt's own probe evidence.

**Verdict:** no false green found on the arms I exercised.

## 3. Cheap-rule arms — neither reaches the target

Scripts: `scripts/brute.py`, `scripts/brute2.py`, `scripts/firstsucc.py` in the
seat dir; raw receipts `receipts/cheap-arms-last-block.json`,
`cheap-arms-interior.json`, `cheap-arms-interior-final.json`,
`firstsucc-interior.log`, `libz-probe.txt`.

- **Brute force over 1..sz_unc validated by `upx -t`, interior block
  (the battery's P1 target block)**: 4 of 6 P1 cells completed (jq −7/+7 5,407
  candidates; xxd −7/+7 2,855 candidates); **no candidate validates** on any
  completed cell (`valid_upx_t: false` on all). The libz and docker-init cells
  were cut short by the L1 stop order; docker-init is trivially small (592
  candidates, cost measured 0.01 s/`upx -t`, est. 6 s total) — the libz sweep
  would need ~63k validations (0.08 h at the measured 0.0044 s/call; my sampled
  probe at stride 1,600 found 0 hits in 41 samples,
  `receipts/libz-probe.txt`).

  Note the claim's own caveat (plan, "Measured limits", last bullet): the
  counter does not force the chain walk, and a brute force over `1..sz_unc`
  *skips the predecessor chain's law entirely* — my measurement confirms it
  does **not** reach `upx -t rc 0` on any candidate it tried, which makes the
  plan's statement that brute force "would also repair these cells" **weakly
  supported but not observable in my sweep**; the L1's claim sentence to
  falsify — "a packer-validated brute force over `1..sz_unc` is an alternative
  mechanism that would also repair these cells" — is **not falsified by my
  evidence** (jq and xxd contradicted it locally: 8,262 / 8,262 subsets over
  the two carriers × two directions returned no validating candidate; libz
  incomplete). Flag: this plan sentence looks suspect, not proven.
- **First-plausible-successor (interior block variant)**: the scan returned a
  *different* hit than the true GPS law on libz (chosen successor `43637`,
  derived 34,108, `upx -t` invalid) and **failed to find any plausible successor**
  for the other 6 cells (jq, xxd, dinit — successor null,
  `receipts/firstsucc-interior.log`). It cannot reach the target. (When my first
  version aimed at the *last* block instead of the interior block, the same arm
  found *a* value that `upx -t` accepts on all 4 carriers — `568`, `552`, `522`,
  `7,467` — which is exactly the under-determination the claim says makes the
  last block unrepaired territory; that state, `cheap-arms-last-block.json`, is
  the *wrong-target* artifact and does not bear on P1.)

Neither falsifies the claim; both cheap arms end up *below* the repair.

## 4. Class boundary claims — independently confirmed

Measured fresh from my own packing (layouts in the scratch `work/run/lay.json`,
accounting in `receipts/chain-accounting.json`):

- **libz is out of class — CONFIRMED.** Chain total through the sentinel and
  on the resumed segment is 98,592 against `u_len` 108,560 (gap 9,968, chain
  first run 87,421 + resume 11,171); the break law's exact-total filter
  (`total != require_total`) can never be satisfied here. My A-libz cell runs
  (`receipts/A-libz--7.log`, `A-libz.so.1.3.2-+7.run2`) show the repair returning
  `class intact, stored 201, derived 201, unchanged` with `upx -t` red. The libz
  P2/P3 composition still works (fresh-pack tamper of block 0 both directions
  repairs back to the intact bytes: p2 `class field-value`, p3
  `class chain-geometry`, restored==packed true, `upx -t` rc 0, 1-byte diffs) —
  the declared limit sentence ("Its block-0 classes still compose (P2/P3)")
  is measured and true.
- **Last block before a chain stop is under-determined — CONFIRMED.** Tampering
  the last walkable block (`jq` pos 9911 stored 252; `xxd` pos 15,455 stored
  249; `dinit` pos 348,349 stored 226) ±5 leaves the repair's verdict
  `class intact, unchanged` on every carrier, with `upx -t` red (rc 1) —
  matching the claim's "the tool leaves it unchanged" and the cheap-arm
  finding that **many** values validate there (`cheap-arms-last-block.json`:
  first successor 568 / 552 / 522 / 7,467 all pass `upx -t` but are not the
  true values).

## Verdict on the claim

R90-C1 survives my attacks: receipt internals check out cell-by-cell from raw
arms; no false green among the six attack vectors I exercised; the two cheap
rule arms cannot meet the target; both boundary claims measure true from
independent data. Verdict: **no falsification found.**

## Residual risk / verification gaps

1. **Blind-replay not reproduced in this seat**: I exercised bwrap's blind
   probe mechanism only via the receipt's own evidence plus the copy-attack
   blinding; a full independent `--carrier_blind` re-run in w1 was cut short by
   the wave stop order.
2. **libz/dinit brute sweeps incomplete** (interrupted): the plan's own sentence
   that brute force "would also repair these cells" is *not* proven or refuted
   here; jq/xxd evidence against it is solid (16,524 total candidate
   validations, zero hits), the libz sweep is incomplete (41-sample probe,
   zero hits) and dinit was not reached. Any future seat should finish the dinit
   sweep first (est. 6 s).
3. **Window-only was exercised through the counter's module object**
   (`bat.window_only`), not through a separate re-implementation; a float of the
   same logic (byte 860 changed outside 844–848 correctly refuses) gives the
   expected behavior on a foreign-byte probe.
4. **`--expect` mismatching is cosmetic-normalized away** in the receipt's
   label — my recomputation shows the same substance, and the killing rule
   claims label equality only for the counter's own short form; worth an exact
   string check by whoever integrates next round (no action needed this round:
   label matches format `P1 6 of 6; P2 4 of 4; P3 4 of 4` verbatim).

## Commands (summary)

Numbers above come from the exact transcripts recorded in seat receipts; every
number in reviews carries its command in the referenced artifact. The two long
irregularities during this seat: (a) the libz full brute sweep (started 00:15:41,
killed 00:25:41 per the L1's stop order, ~5.5 min in) — jobs `bg_913`,
`BruteInterior`; (b) the sleep-and-poll lookups that were pushed to background
during the sweep (`bg_1868`, `bg_1930`, .. `bg_2133`). No other long-running
commands were started. No scratch-cleanup trap fired at the time of the flag:
scratch `/fast/scratch/hyaku/kaidoku-r90/ReviewerC1/` is due for removal on
yield (see cleanup note below).

## Cleanup note

Per lane rules the scratch tree is removed at yiel: `ReviewerC1.md` in the seat
dir plus `receipts/` (31 files) are the citable artifacts; the scratch copy of
`work/run/` (packing + layouts) is **not** citable and is deleted on yield.
