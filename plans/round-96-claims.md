# Round 96 — claims declaration (frozen before candidate scoring)

Lane `kaidoku`, round 96, attempt 1. Base `0ea695e826f2dca53dd55ac0bafead93de26b173`
(lane tip at round start, `jj-lane.sh state` `ahead=0 behind=0`). Machine-readable twin:
`.ufo/waves/round-96/claims.json`. Before-state receipts are committed in this declaration
under `.ufo/waves/round-96/pre/`, measured at the base with the frozen round-95
instruments. Pins: `.ufo/waves/round-96/pins.sha256`.

## Owned axes and lowest-axis obligation

All four owned axes (coverage, depth, calibration, freshness) sit at 10.0 on their finite
proxies (SCORECARD `## Owned axes`); saturation 10.0, stagnation window 10. A capability
entered in round 95 (`world-bound receipt battery with a symlink-safe writer`), so the
stagnation window has not closed and no waiver is invoked. Calibration and depth are
tied-lowest; both claims sit on them. Two claims, distinct axes, causally separable: C1's
measurement reads `tools/round-96/*`, the committed mutant table, the forged fixtures and
the round-95 fixture/pins bytes only; C2's measurement reads `SKILL.md`,
`corpus/QUALITY.md` and `corpus/knowledge/` bytes only.

## Routed defects this round carries (round-95 lesson and spot-check)

- M95-g / named limit 2 (unbound fields: unlabelled counts, HEAD vs measured tree,
  `repair_sha256`, the imported battery pins, `public_met`; self-verification skipped
  without `--json-out`): carried as R96-C1's v6 bindings and the mandatory-receipt rule.
- M95-h / named limit 3 (five writer and probe gates outside the frozen kill rule: M2,
  M3, M4, M6, M10): carried as R96-C1's kill rule v2 with the four named checks plus the
  no-json-out refusal.
- M95-i / named limit 4 (the probe's own `--json-out` follows a planted symlink): carried
  as R96-C1's symlink-probe-v2 hardened writer.
- R95-VD-1 (no receipt names the landing revision): this declaration defines both claims'
  after-sides AT THE LANDING REVISION, and the landing receipts name it.
- R95-VD-2 (a numeric claim without a command in the r95 lesson Gate prose): corrected by
  an appended correction entry in `corpus/lessons/round-96.md` with its counting command.
- R95-VD-3 (the four round-95 instruments carry no registry rows): carried as R96-C2's
  registry work — rows for the round-95 instruments and the round-96 instruments land in
  `SKILL.md` at the landing.
- Round-95 planned (a)+(b) (closing limits 2 and 3 with the named kills; the probe's
  receipt through the hardened writer): this declaration is that landing. The round-95
  instruments stay pinned, unedited.

## R96-C1 — calibration (measured): the kill rule covers the gates it asserts, and every unbound field is bound

- **Surface.** The round-95 frozen kill rule killed only 5 of 10 mutants (M95-h): its
  checks never called the counter's `main()` and never ran the probe, so the writer
  fsync (M2), the forced self-verify (M3), the removed fail-closed exit (M4), the removed
  revision binding (M6) and the probe's hard-coded verdict (M10) survived. The same
  round's critic showed six receipt fields unbound (M95-g) — five accepted by the r95
  counter's `verify_receipt` and one crashing on a bare `KeyError` — and that a run
  without `--json-out` exited 0 on a met-True verdict without writing or verifying any
  receipt. The probe's own `--json-out` followed a planted symlink (M95-i). Calibration
  here = the counter's green exits are earned through a receipt whose every asserted gate
  survives its own kill rule, and every field the receipt claims is bound.
- **Candidate instruments (new declaration; the frozen r95 and r94 files are unedited).**
  1. `tools/round-96/stop-boundary-repair-battery-v6.py` — the verdict code is still the
     v3 counter by path (pinned). v6 changes only the receipt writer and its
     self-verification: `--json-out` is mandatory (refuse before scoring, exit 2,
     `receipt-required`); the receipt records and binds `head` (must equal the
     revision), `repair_sha256`/`repair_cmd` (bound to the bytes at `--repair-cmd`),
     `counter_sha256` and `verdict_sha256` (now checked by `verify_receipt`, not merely
     recorded), the downward met direction (`met-not-recomputed`), and schema-valid
     counts (`counts-missing-key:<k>` / `counts-type:<k>` — typed, never a `KeyError`).
     Selftest 13 cases including the wrong-revision case (the r95 M6 kill) and the
     no-json-out refusal.
  2. `tools/round-96/kill-rule-v2.py` — the frozen counting command. Check set:
     K-selftest (counter/agreement selftests), K-forgeries (`verify_receipt` refuses the
     six round-96 forgeries with exactly their intended single reason and refuses the
     four round-95 forgeries), K-agreement (the r95 agreement instrument refuses its four
     forgeries exactly and accepts the honest triple), K-dmain (main()-level negative
     control with a faked met-True verdict: honest scenario exits 0, shortrev / rewrite /
     notrecomp exit non-zero, no `--json-out` exits 2), K-fsync (instrumented
     `os.fsync` count ≥ 1 during `write_receipt`), K-probe (probe receipt
     self-consistency: `verdict == "hardened"` iff `victim_intact and receipt_valid`,
     `met` stating the same), plus the r95 forgery battery re-run (regression, exit 0).
     Mutants are applied to scratch copies; the lane tree is never mutated.
  3. `tools/round-96/symlink-probe-v2.py` — the probe with the hardened writer for its
     own receipt (mkstemp + `os.replace`), closing M95-i.
  4. `tools/round-96/legacy-kill-rule.py` — the r95 rule formalized (checks (i)-(iv)
     only) for the before arm; `tools/round-96/r95-unbound-at-base.py` and
     `tools/round-96/probe-writer-legs.py` are the other before-arm drivers;
     `tools/round-96/gen-forgery-fixtures.py` generated the committed fixtures;
     `tools/round-96/fresh-source2-check.py` measures the held-out arm's second fresh
     source (S321) through the round-92 helpers.
- **Mutant table** `.ufo/waves/round-96/mutants.json`: M0 identity control (must NOT be
  killed) plus M1-M10 — the r95 survivor set adapted to the v6 counter bytes (M1 fixed
  temp name, M2 fsync removal, M3 forced self-verify, M4 fail-closed removal, M5
  label-not-frozen removal, M6 revision-binding removal), the frozen r95 agreement bytes
  (M7 pins, M8 label-not-recomputed, M9 label-not-frozen — the same edits as r95), and
  the v2 probe verdict hard-code (M10). Each `find` string occurs exactly once in its
  target bytes; every replaced file still compiles.
- **Committed forged fixtures** (`.ufo/waves/round-96/forgery/forge-<name>.{json,stdout,rc}`,
  world revision = base; each violates exactly one binding of the v6 `verify_receipt`):
  `unlabelled` → `counts-missing-key:fresh_scored`; `met-lying` → `met-not-recomputed`;
  `head-mismatch` → `head-not-bound`; `counter-pin` → `counter-pin-not-bound`;
  `verdict-pin` → `verdict-pin-not-bound`; `repair-pin` → `repair-pin-not-bound`.
- **Frozen counting commands (after, at the landing revision `<landing>`):**
  1. `python3 -I -B tools/round-96/kill-rule-v2.py --root . --work <scratch> --mutants .ufo/waves/round-96/mutants.json --fixtures .ufo/waves/round-96/forgery --prefix forge --expect '<FROZEN_LABEL>' --json-out .ufo/waves/round-96/l1/scores/c1-at-<landing>.json` → exit 0 (the tool's defaults carry the counter/agreement/probe/writer/no-op paths and the r95 regression args).
  2. The honest v6 public run at the declaration revision (the real battery, upx
     5.2.0): `python3 -I -B tools/round-96/stop-boundary-repair-battery-v6.py --root . --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work <scratch> --rev <decl> --expect '<FROZEN_LABEL>' --json-out .ufo/waves/round-96/l1/scores/honest-pos.json` → exit 0 with `selfverify ok=True reasons=0`.
  3. `python3 -I -B tools/round-96/symlink-probe-v2.py --root . --writer tools/round-96/stop-boundary-repair-battery-v6.py --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work <scratch> --rev <decl> --expect '<FROZEN_LABEL>' --json-out .ufo/waves/round-96/l1/scores/c1-symlink-v6-at-<decl>.json` → exit 0 (`victim_intact true`, `receipt_valid true`).
- **Frozen label (the same string as rounds 93/94/95):**
  `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`.
- **Before (committed in this declaration, measured at the base):**
  1. `.ufo/waves/round-96/pre/c1-legacy-rule-at-base.json` — the formalized r95 rule
     kills **5 of 10**; survivors exactly M2, M3, M4, M6, M10 (matches the round-95
     MutationC1 finding, re-measured with a receipt).
  2. `.ufo/waves/round-96/pre/c1-v5-admits-unbound-at-base.json` — the pinned r95
     counter accepts **5 of 6** unbound-field forgeries, crashes on `forge-unlabelled`
     with a bare `KeyError: 'fresh_scored'`, and its no-json-out scenario **exits 0**
     without a receipt.
  3. `.ufo/waves/round-96/pre/c1-probe-writer-unbound-at-base.json` — the r95 probe's
     own receipt write follows a symlink planted at its `--json-out` (`victim_intact
     false`); the v2 probe's write leaves the victim intact.
  The unchanged r95 instrument set is the do-nothing control: it cannot reach the target
  because five mutants survive its rule and its counter admits the unbound fields.
- **Positive controls (blanket refusal is not a gain):** the identity mutant M0 must NOT
  be killed; K-agreement's honest triple is accepted; K-dmain's honest scenario exits 0;
  the r95 forgery battery regression exits 0; the honest v6 public run exits 0 with a
  self-verified receipt; the v6 probe leg exits 0 with the victim intact.
- **Frozen target (after):** command 1 exits 0 with `mutants killed 10 of 10; forgeries
  refused 10 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of
  1` and `identity_not_killed true`; commands 2 and 3 exit 0.
- **Kill rule:** the before side met (premise fails); any forged receipt accepted or
  carrying a reason other than exactly its intended one; any honest-arm check red; the
  identity mutant killed; any pinned sha256 in `.ufo/waves/round-96/pins.sha256`
  differing; `git diff --stat <decl> <landing> -- tools/round-96 tools/round-95
  tools/round-94 tools/round-93 tools/round-92` nonempty (counter-read bytes changed
  after the freeze).
- **Named limits (stated before data).** The v6 bindings bind a receipt to the world it
  claims; they still do not authenticate provenance (a wholly consistent re-authored
  triple whose every field describes the honest world is byte-indistinguishable — r95
  limit carried). K-probe reads only the probe's receipt: a probe that lies consistently
  with a manipulated victim state is not caught by consistency alone. The mutant table
  is the declared ten plus the identity control, not all possible mutants. K-dmain fakes
  `v3.score` in-process; the real battery path is exercised by the honest public run and
  the probe legs, not by the negctl scenarios. The fsync count is instrumented at the
  Python level, not `strace`. The `head` binding forces `--rev == HEAD` on every green
  run; a landing receipt re-run passes `--rev <landing>`.

## R96-C2 — depth: a craft decision table for the kill-rule gate-coverage failure class

- **Surface.** No craft row names the class where a counter's gates live outside its
  counting commands (M95-h) or the rule that a green verdict exists only through a
  verified receipt (M95-g's no-json-out arm). Candidate: craft block 35 (append-only;
  blocks 1-34 unchanged) with a decision table, corpus criteria QUALITY 193 and 194 that
  state the rules the rows assert, and the SKILL.md registry rows the round-95 spot-check
  routed (R95-VD-3) for the round-95 instruments plus this round's instruments.
- **Before (do-nothing controls, committed here, measured at the base):**
  `pre/c2-base-block35-after-manifest.json` exit 1 (`block 35 missing`);
  `pre/c2-base-depth-v2.txt` exit 1 (`blocks 34 resolved 34 expect 35`);
  `pre/c2-base-depth-v3.txt` exit 1 (`blocks 34 ... expect 35`).
- **Frozen counting commands (after, at the landing revision `<landing>`):**
  1. `python3 -I -B tools/round-93/craft-citation-semantic.py --root . --manifest .ufo/waves/round-96/manifests/block35-after.json --block 35 --rev <landing> --json-out .ufo/waves/round-96/l1/scores/c2-after-block35.json` → exit 0, `ok`.
  2. `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev <landing> --expect-blocks 35` → exit 0, `blocks 35 resolved 35`.
  3. `python3 -I -B tools/round-91/depth-blocks-v3.py --root . --rev <landing> --expect-blocks 35 --shape-from 35` → exit 0, `required-shaped 1/1`.
  4. The rubber-stamp control at `<landing>`: `python3 -I -B tools/round-93/craft-citation-semantic.py --root . --manifest .ufo/waves/round-96/manifests/block35-junk.json --block 35 --rev <landing> --json-out .ufo/waves/round-96/l1/scores/c2-junk-at-landing.json` → exit 1 on the keyword atoms (the junk manifest carries keywords the cited criteria lack).
- **Frozen predicate (the keyword sets are in the manifest, frozen here):** block 35
  carries the marker `kill-rule-gate-coverage v1` and a decision table with at least
  three body rows of at least four cells; each row's criterion cites exactly one QUALITY
  row whose text contains the row's frozen keywords: row `writer durability gate` →
  QUALITY 193 contains `instrumented count` and `survives every exit-code diff`; row
  `fail-closed exit and forced verdict` → QUALITY 193 contains `main()-level negative
  control`; row `probe receipt verdict` → QUALITY 193 contains `receipt-content
  consistency check`; row `green without a receipt` → QUALITY 194 contains `--json-out
  is mandatory` and `skipped self-verification`.
- **Frozen target (after):** commands 1-3 exit 0 at the landing revision; command 4
  exits 1; block 35 absent at base (done above); no depth regression: blocks 1-34 intact
  (v2 counts 35 of 35 resolved).
- **Kill rule:** any of commands 1-3 unmet at the landing revision; command 4 exit 0
  (rubber stamp); block 35 present at base; the checker `craft-citation-semantic.py`
  sha256 (`34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`), the depth
  counters' sha256s (`depth-blocks-v2.py`
  `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f`,
  `depth-blocks-v3.py`
  `bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f`) or either
  manifest's sha256 differing from the pins.
- **Named limit (stated before data).** The keyword atom is a vocabulary check (QUALITY
  188 residual, carried since round 93): a criterion that carries the keywords passes
  whether or not it states the rule. The non-author check of block 34's criteria
  (round-95 planned (c)) and this block's criteria are discernment work the wave attacks;
  C2 claims the vocabulary-plus-junk-control land only.

## Sourced claim (frontier step)

R96-C1's knowledge entry cites `S321` — the held-out arm's second fresh source,
`/usr/bin/printf` (sha256
`b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`, little-endian x86-64
ELF, packable by upx 5.2.0 on this host), opened this round by measurement:
`tools/round-96/fresh-source2-check.py --root . --work <scratch> --rev <base> --json-out
.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json` → exit 0, `fresh-source2
repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True` (pack determinism, no
public-carrier collision, near cells repaired, far cells refused). This closes the
round-93 carried limit "the fresh-pack arm has one source". The S321 registry row, the
knowledge entry and the lesson Gate record land at the round's integration commit.

## Exploratory claims

None. Two counting claims.

## Honest stop

Both claims are single-commit byte-level predicates a closure can re-derive with one
command (C2's after-side at the landing revision per R95-VD-1). Neither target is
narrowed after landing: a miss is reported as a miss.
