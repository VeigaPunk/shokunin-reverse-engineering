# CritCounterV2 — findings on the R52-C1 v2 counter design

Seat: CritCounterV2 (critic, leaf). Lane base read: `ab0eafed` claims draft; `1842addc` wave dispatch.
Counter attacked: `tools/round-50/c1-counter.py` (v1, sha256 `9820811b…bd813`) and the frozen
rule `tools/round-50/gap-rule.json` (sha256 `43f7c8d7…a0ef`). Probe: `probe-r52-law.py`,
output `probe-r52-law.out.txt`, stdout sha256 `7a7916d8…6b91d`, run 2026-10-30T11:15:21Z.
No REA run, no git mutation, no lane write outside this seat directory.

Verified ground (probe output, reproduced by re-run):
- CTL-OLD (round-50 rule over committed round-50 envelopes): 2 of 4 (`c6490`, `c6430`). Reproduces the miss.
- CTL-NEW (round-52 law rule over the same envelopes): 4 of 4.
- M1 all-thirteen whitelist: disposition 4 of 4 green; the ONLY thing turning it red is the shape clause.
- M2 (14th device, no gap): law green 4/4; whitelist red 0/4. Matches the claim.
- M3 (`required` true, silent `247:0` only): 2 of 4. Matches the claim.
- Fixture: `mksquashfs -pf` device rows render in `unsquashfs -lln` as `crw-`/`brw-`/`prw-`; the
  census regex in `tools/round-50/c1-run.sh` matched all four (`b 7 1`, `p`, `c 247 0`, `c 4 64`).

## Findings

**F1 — HIGH — stale rule bytes / rule override can pass unnoticed (controls mode).**
v1 binds the rule only as `gap_rule_unchanged` (rev blob == freeze blob) and records no sha256
of the rule actually scored. The v2 controls take `--gap-rule`; nothing in the claim forbids
that flag on the predicate path, and the receipt names no rule file or digest.
Demand: (a) the predicate mode refuses `--gap-rule` (exit 2 `rule_override_refused`); (b) every
receipt records `gap_rule_path`, `gap_rule_sha256` (of the bytes scored) and `gap_rule_freeze_sha256`,
and the predicate requires them equal; (c) CTL-NEW's rule must be byte-identical to frozen
`tools/round-52/gap-rule.json`, asserted from the freeze blob, not the working tree.

**F2 — HIGH — post-freeze mutation of a committed receipt is not drift.**
`receipt_fresh` uses `git log --diff-filter=A`. An `M`/`D`/`R` on `corpus/evidence/round-52/c1/<id>/after.json`
after its add passes freshness. `evidence_id_ok` is self-consistency only (an edited envelope with a
recomputed id passes it). `projection_ok` is the sole independent guard, and only for the plus-extractor
profile. Demand: each receipt path has exactly one `A` commit and zero later `M/D/R/T` commits in
`FREEZE..REV` (`git log --name-status -- <receipt>`), and `run.json`/`after.json` sha256s are listed in
the scoring receipt's `evidence_digests` and compared to the data-run receipt written at landing.

**F3 — HIGH — retry policy erases its own evidence and is not yet controlled.**
`make_real_runner` returns `('ok', data)` on success; `replayed['attempts']` lives only on the failure
payload, so a success on attempt 2 leaves no trace in the receipt. The loop overwrites `envl` each
iteration, so earlier failing diagnostics are lost. The claim's required record (attempt count and the
failing diagnostic) is therefore not produced on the success path. The ENOENT branch does not exist in
v1 at all (only `provider_timeout` is retried). Demand: (a) every outcome returns an attempts ledger
`[{attempt, outdir, error_code, diagnostic_reason}]` surfaced as a clause-level field; (b) ENOENT
retry only when the diagnostic path lies under that attempt's own extraction root (prefix test, not
substring); (c) the deterministic-ENOENT control must drive THIS loop (not a stub returning the error),
else it proves nothing about the shipped code; (d) one shared attempt budget (≤3 total across both causes).
The `g7581` projection failure is the readlink ENOENT inside `extracted/firmware.bin_extract/…luacgi` —
a retry on a fresh root may or may not reproduce it; that is what the control must show.

**F4 — HIGH — `law_shape_ok` as worded does not encode the law; the discrimination rests on it.**
M1 (all-thirteen whitelist) is green on disposition (4/4) and red only through the shape clause. The
claim's shape clause checks only `removed.silent` device details and `allowed[device]==[]`. Measured
(probe):
- K1 `removed.kinds += char-device` (plus `required` true): claimed shape **True**, extended shape False.
  A device-removal limb is admitted by the claimed clause.
- K2 `structural.char-device = 0`: claimed shape **True**, extended shape False.
Demand: `law_shape_ok` additionally requires `removed.kinds ⊆ {symlink}` and no device kind among
`structural` keys. M1, K1, K2 must each be red. Add K1 and K2 to the frozen mutation battery.

**F5 — MEDIUM-HIGH — bindings and constants are dropped or left at round-50 values.**
v1 `BINDINGS` (9) and `CLAUSES` (23) are the round-50 set. Concretely for v2:
- `OPENED_DATES` = `('2026-10-28','2026-10-29')`. The round-52 entry and its SOURCES rows are dated
  2026-10-30; `sourced` cannot pass unless the constant is re-set. Name it in the freeze.
- `FRONTIER_MARK` = `'Round-50 frontier note'`, `ENTRY`/`STEM`/`CORE_HEADING` → round-52 values; `frontier_note`
  must match `Round-52 frontier note`.
- `carriers_spec` and `gap_rule_model` both hard-code `claim == 'R50-C1'`; v2 must accept `{R50-C1, R52-C1}`
  (claim F10) in both, or every rule/spec reports `claim != R50-C1` as a problem (observed in probe).
- **No binding that `hsqs` is removed from the PROVINCE `## Frontier` bullet list.** Without it a freeze can
  add the Core row and keep the Frontier bullet: two authorities. The round-50 frontier note text itself
  still says "LE AVM members (hsqs) stays Frontier", so a naive note edit leaves a contradiction a binding
  would catch.
- No binding that the entry cites `S252` (the CAP_MKNOD device-law ground) or S243/S244/S245/S249/S250/S251 —
  `sourced` only needs *some* opened SID.
- `SCORECARD.md` coverage head 141→142 and the LOG entry are not bound (the claim names them as landing bindings).
- New clauses named by the claim (`law_shape_ok`, `census_rederived_ok`, `depth_gap_recorded`,
  `carrier_fresh_ok` allow-list) are absent from `CLAUSES`; `failing_lists` iterates only `CLAUSES`, so a red
  on them would be invisible in `failing` unless added.

**F6 — MEDIUM — drift exit 2 is correct in v1 but reads as "0 matched" to a tabulator.**
`main()` on `Unevaluable` writes a receipt with `exit_code 2`, `reason`, `frozen_path_changed` — and no
`carriers_matched`, `met_target` or `verdict` key. A before/after table keyed on `carriers_matched` gets
`None`, and the claim's "before = 2" convention would tabulate exit 2 as a count of 0 if any consumer does
`.get('carriers_matched', 0)`. The v1 selftest asserts `want=2` for drift, which is correct, but nothing
checks the consumer. Demand: exit-2 receipts carry `verdict: "unevaluable"`, `carriers_matched: null`,
`met_target: null`; the landing accounting refuses to publish a count from a non-0/1 exit.
Also: `measure()` never checks `is_ancestor(FREEZE, REV)`. The claim's predicate says "REV descending from the
freeze"; v1 relies on receipt freshness to indirectly refuse a sibling. Add the explicit check (exit 2).

**F7 — MEDIUM — the walk: scope is right in v1, but the walk must not swallow the landing docs.**
- `tools/round-41/sqfs-list.py` is in `FROZEN_PATHS`, but the score path never executes it (grep: only
  FROZEN_PATHS and selftest stand-ins). It is the freeze-time producer of the oracle tables; its identity
  is not recorded anywhere a score can see. Keep it in the walk and record its sha256 in `carriers.json`
  (or the oracle table header) so a producer swap is visible, not only a table swap.
- The oracle producers (`tools/round-50/c1-run.sh`) are covered by the `tools/round-50/` prefix. The v2
  walk must add the `tools/round-52/` prefix (counter, rule, controls, triage v6, fetcher) and must NOT
  include `PROVINCE.md`, `corpus/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`: the landing bindings are
  edited after the freeze by design. Say so in the freeze text to stop a future freeze from freezing them.
- `PRIOR_CARRIER_TABLES` (`.ufo/waves/round-41/c1/carriers.json`, `tools/round-49/carriers.json`) are read at
  the freeze commit, so later edits cannot bless a pin. Correct as is.

**F8 — MEDIUM — the prior-pin waiver is self-inflicted and unnecessary.**
Verified on the committed round-50 receipt: none of the four round-50 carrier pins
(`968d997d…`, `a119b644…`, `880370e7…`, `da1c8049…`) is in `prior_pins`. Joining `tools/round-50/carriers.json`
to `PRIOR_CARRIER_TABLES` is what would make them "prior" and force the `re_scored_pins` allow-list. Not
joining it removes the waiver surface entirely. If the join stays, the allow-list must be exactly these four
pins, read from the freeze blob, and a waived pin must still pass `carrier_pin_ok` (the allow-list waives
freshness, never the byte pin).

**F9 — MEDIUM — `depth_gap_recorded` as worded cannot fail.**
"The receipt records the `depth-limited` gap's `input_path` and `continuation_id`" is true for every
receipt that has the gap. All four committed receipts carry `input_path "$output/firmware.bin_extract"` and
the same `continuation_id 3b54e297…b442ab`. Demand red cases: zero or two `depth-limited` gaps; a
`depth-limited` gap whose `input_path` is not the subject chunk's `<root>/...` form; a `continuation_id`
that is not 64-hex. Without them the claim's "every clause can fail" standard is unmet for this clause.

**F10 — LOW (verified GOOD, recorded so it is not re-litigated) — census re-derivation.**
The `unsquashfs -lln` regex in `c1-run.sh` parses char, block and fifo rows correctly on a mksquashfs
fixture (probe above). Sockets (`s`) use the same branch. A parse failure yields missing rows, which the
two-direction equality turns red, so the failure mode is red, not green. Residual: the regex `(.*)` name
capture cannot represent a path containing a newline; the claim already limits width to the measured
corpus. Note the `squashfs-root/` prefix strip must be asserted (not assumed) in v2.

**F11 — LOW — retry budget wording is ambiguous.**
"up to 3 attempts on provider_timeout" and "up to 2 on ENOENT" reads as 5 total. Pin one shared budget
(≤3 attempts per carrier across both causes) so the worst case is written down.

**F12 — LOW — `carrier_fresh_ok` allow-list needs an exact-equality clause.**
With F8 unresolved, the allow-list is a set; demand equality with the four pins (not subset), so a fifth
pin added later cannot ride the waiver.

## Counter-check of the claimed design
- The law itself holds on the corpus: the frozen device rows (28 of 28 across the four carriers) carry no
  gap and no published path (probe: `dev/pts/*`, `dev/tiatm`, `dev/ttyp*`, `dev/led` absent from every
  `nonregular_published`, round-50 receipts `nonregular_published []`).
- Fail-closed on a future device gap holds for the LAW rule (verified: an `unpublished-entry` gap on
  `dev/led` → `gap kind 'unpublished-entry' not allowed for 'char-device'`, 4/4 red). The round-50 rule
  does NOT fail closed there (it admits device gaps by listing `unpublished-entry`). So the claim's
  fail-closed argument is real and the shape clause (F4) is what keeps the claim honest.

## Minimal correction set (for the L1 freeze)
1. Predicate refuses `--gap-rule`; receipts record and equate gap-rule sha256 (F1).
2. Receipt freshness = exactly one add and no later M/D/R/T (F2).
3. Attempts ledger on every outcome; ENOENT retry prefix-bounded; control drives the real loop; shared budget (F3, F11).
4. `law_shape_ok` extended with removed.kinds and structural device checks; K1, K2 added to the battery (F4).
5. Re-set `OPENED_DATES`, `FRONTIER_MARK`, claim labels; add Frontier-removal, S252 and SCORECARD/LOG bindings; extend CLAUSES (F5).
6. Exit-2 receipts carry null counts and `verdict: unevaluable`; explicit `is_ancestor(FREEZE, REV)` (F6).
7. Walk: keep sqfs-list + record its sha; add `tools/round-52/`; exclude landing docs (F7).
8. Do not join `tools/round-50/carriers.json` to PRIOR tables; if joined, exact four-pin allow-list (F8, F12).
9. `depth_gap_recorded` gets red cases (F9).
