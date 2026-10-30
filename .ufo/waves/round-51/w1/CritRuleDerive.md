# CritRuleDerive — round 51 wave 1 (R51-C1 pre-freeze attack on the rule design)

**Seat**: `CritRuleDerive` (critic; leaf member — no dispatch, no subagents).
**Verdict**: **the R51-C1 rule design is not freezable as written.** 2 critical + 4 high +
4 medium + 1 low findings, all derived from committed bytes only. Two of them make the claim's
own predicate/controls **unreachable**, so they must be amended in the freeze's
`## Wave-1 amendment record` — before the freeze, not after.
**Findings (full, with evidence and the exact text fix demanded)**: `.ufo/waves/round-51/w1/CritRuleDerive/findings.md`
**Verification receipts** (command, exit code, stdout sha256, UTC): `.ufo/waves/round-51/w1/CritRuleDerive/receipts.txt`

## The three that matter most

1. **F1 (critical) — the four frozen carriers are pins the round-50 C1 freeze already scored.**
   `carrier_fresh_ok` is in `CLAUSES` and is `pin not in prior` (`c1-counter.py:435`, `:2250`,
   `:1596-1618`); the lane's own discipline is documented in `tools/round-42/prior-pins.json`
   ("frozen union of the C1 carrier pins of rounds 38-41"). The round-51 freeze is the fourth
   C1 freeze to see these four pins, so an honestly ported v2 counter (adding
   `tools/round-50/carriers.json` to `PRIOR_CARRIER_TABLES`) makes `carrier_fresh_ok` false for
   all four → `carriers_matched == 0`, and the predicate `== 4` is unreachable. The only green
   path is to omit the round-50 table and keep the pins out of `prior_pins` — the exact weakening
   the clause exists to prevent. **Fix demanded**: the claims must freeze the carrier set
   explicitly — four *new* pins, or the four round-50 pins re-scored under a **named**
   `re_scored_pins` exemption with the claims stating that R51-C1 then adds *no new carrier* and
   the Frontier → Core promotion rests on the completed 4/4 measurement, not on new coverage.

2. **F2 (critical) — CTL-OLD (2/4) and CTL-NEW (4/4) cannot be produced by the frozen
   instruments.** Three per-carrier clauses are red on the committed round-50 receipts:
   `run_provenance_ok` (the envelopes carry `/fast/scratch/hyaku/kaidoku-r50/…`, the v2 base is
   `kaidoku-r51`), `receipt_fresh` (the envelopes were added at `646d29c9`, before the round-51
   freeze) and every byte-dependent clause (`carrier_present`, `carrier_pin_ok`,
   `oracle_rederived_ok`, `projection_ok` — the round-50 carrier cache no longer exists and a
   rerun is forbidden this wave). The claims also name the wrong control input: `run.json` is
   the *harness* receipt; the counter reads the envelope `after.json`. **Fix demanded**: re-scope
   the two controls to the rule-scoped disposition verdict over the committed envelopes, and
   state that the full predicate is not claimed for the controls.

3. **F3 + F4 (high) — the law's sentence and the rule are different statements, and the
   mutation set cannot tell them apart.** The law says a device row carries *no gap record*;
   the described rule (`required=false` + `allowed['char-device']=['unpublished-entry']`) *tolerates*
   one — the gap loop in `disposition_check` is unconditional, so the rule must set
   `allowed` for the device kinds to the **empty list** to forbid the state the law forbids.
   And the planned mutants (round-50 miss; strict-subset whitelist) are red under the law rule
   too, so they prove nothing; the decisive mutant — an **all-thirteen whitelist** — is *green*
   over the four carriers and would pass the battery. **Fix demanded**: add a frozen rule-shape
   clause (`law_shape_ok`: no device detail under `removed.silent`, empty `allowed` for device
   kinds) plus a census mutant with a fourteenth device (`dev/ttyS0 4:64`) that is green under
   the law and red under any whitelist.

## Also load-bearing

- **F5 (high)**: the law's fifo/socket scope is unmeasured (the four censuses hold char-devices
  only; 28/28 device rows carry no gap and no `unpublished_entries` entry — verified over the
  four envelopes), and SKILL.md's own triage rows say the opposite ("`symlink` and `special`
  both count"). R51-C2 rewrites that table in the same freeze → the two claims would land
  contradictory device-node statements. The law's grounding must also be the *measurement*; the
  unsquashfs source rows ground the census, not the extractor's silence.
- **F6 (high)**: the round-50 miss on `g7581` had **two** causes — `gaps_ok` false *and*
  `projection_ok` false (REA `execution_failure`, `retryable: false`, ENOENT on `readlink
  …/usr/www.myfritz/avme/cgi-bin/luacgi`). The v1 counter retries only `provider_timeout`, so the
  same race in the round-51 data run would miss the claim for a cause the claim does not contain.
- **F7/F8 (medium)**: the device census — the law's entire scope — is frozen but never
  re-derived at score time (the round-41 instrument re-derived both tables); and a `depth-limited`
  gap names no path, so a never-visited device-only subtree (`dev/pts/`, which holds no regular
  file) is a false green. Narrow the law to "reached" or check the path.
- **F9/F10 (medium)**: CTL-OLD's "if it reported 4, the counter or target is wrong" is a false
  inference (a permissive old rule would report 4 with counter and target both right) — it is
  the *reproducibility* control, not the do-nothing control; and the v2 rule parser must accept
  both `R50-C1` and `R51-C1` labels or one of the two arms is rejected before it is measured.
- **F11 (low)**: the claims' `Base` line is stale (`1aa27369`; the tip was `f04b51dd`, HEAD is
  `39f41d4f`); the C2 before-arm base must name the same commit.

## What I did / did not do

Read-only on the lane tree. Files written: this report, `findings.md`, `receipts.txt` — all under
`.ufo/waves/round-51/w1/CritRuleDerive/`. **No** REA run, **no** `npx rea-agents`, **no**
download, **no** git/jj mutation, **no** write into `tools/`, `plans/`, `corpus/`, `SKILL.md`,
`PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md` or the fleet repo; scratch
`/fast/scratch/hyaku/kaidoku-r51/w1-CritRuleDerive` was used only for temporary stdout capture
and removed after the receipts were copied. No counter was executed (the round-51 instruments do
not exist yet) — every finding above is derived from committed round-50 bytes. No tool was
installed or upgraded this wave (none needed).
