# Round 95 — claims declaration (frozen before candidate scoring)

Lane `kaidoku`, round 95, attempt 1. Base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`
(lane tip at round start, `jj-lane.sh state` `ahead=0 behind=0`). Machine-readable twin:
`.ufo/waves/round-95/claims.json`. Before-state receipts are committed in this declaration
under `.ufo/waves/round-95/pre/`, measured at the base with the frozen round-94 instruments.

## Owned axes and lowest-axis obligation

All four owned axes (coverage, depth, calibration, freshness) sit at 10.0 on their finite
proxies (SCORECARD `## Owned axes`); saturation 10.0, stagnation window 10. A capability
entered in round 94, so the stagnation window has not closed and no waiver is invoked.
Calibration and depth are tied-lowest; both claims sit on them. Two claims, distinct axes,
causally separable: C1's measurement reads `tools/round-95/*`, the committed fixtures and the
captured honest triple only; C2's measurement reads `SKILL.md`, `corpus/QUALITY.md` and
`corpus/knowledge/` bytes only.

## Routed defects this round carries (round-94 spot-check and lesson, `## Mistakes`)

- M94-e (the frozen agreement counter is narrower than its natural reading: consistent label
  rewrites and fabricated triples pass it): carried as R95-C1's strengthened instrument.
- SentinelWrite F1 (the `.tmp` write follows a pre-planted symlink; O_NOFOLLOW/mkstemp
  remediation routed): carried as R95-C1's hardened writer and the frozen symlink probe.
- M94-f (short `--rev` in base receipts; nothing validates `--rev` against `git rev-parse`):
  carried as R95-C1's revision binding.
- D-94-A (the r94 unchanged-bytes receipt is a 0-byte file, not self-describing): fixed in
  this round's bookkeeping by a self-describing sibling receipt; the 0-byte file is kept as
  evidence, not rewritten.
- Round-94 planned (a)+(b) (counter-strengthening declaration and receipt-writer hardening
  landing together): this declaration is that landing. v4 and the round-94 agreement counter
  stay pinned, unedited.

## R95-C1 — calibration (measured): the receipt is bound to the world it claims

- **Surface.** The frozen round-94 instrument `tools/round-94/c1-receipt-agreement.py`
  checks only receipt↔stdout↔rc agreement and the predicted met/exit per run name; the
  round-94 critic showed it admits a consistently rewritten label pair and a wholly
  fabricated triple (M94-e), the base receipts carried a short `--rev` with nothing
  validating it (M94-f), and the v4 writer follows a planted `<json-out>.tmp` symlink
  (SentinelWrite F1). Calibration here = a receipt that exits 0 is bound to the world it
  claims: the frozen label, the receipt's own counts, the measured tree and the pinned bytes.
- **Candidate instruments (new declaration; the frozen r94 files are unedited).**
  1. `tools/round-95/stop-boundary-repair-battery-v5.py` — imports the v3 verdict code by
     path (sha pinned below) and changes only the receipt writer: mkstemp unique temp name
     in the receipt's own directory (a planted `<json-out>.tmp` symlink is neither read nor
     followed), plus receipt self-verification before a met-True exit 0 (re-read the
     receipt; recompute the label from counts; bind label==`--expect` when met; bind
     revision to the full `git rev-parse` resolution of `--rev`; fail closed to exit 1 on
     any failed binding).
  2. `tools/round-95/c1-agreement-v2.py` — the strengthened instrument: every round-94 atom
     plus four typed bindings (`label-not-frozen`, `label-not-recomputed`,
     `revision-not-bound`, `pins-not-bound` via `git show REV:` re-derivation).
  3. `tools/round-95/c1-forgery-refusal.py` — the frozen counting command over the four
     committed forged triples (before: the pinned r94 counter admits; after: v2 refuses
     each with exactly its intended single reason; honest triple accepted).
  4. `tools/round-95/symlink-probe.py` — the public-path write-escape probe (plant victim +
     `<json-out>.tmp` symlink; run the writer's public CLI with a non-repairing repair
     command; hardened = victim intact AND receipt valid).
- **Committed forged fixtures** (`.ufo/waves/round-95/forgery/forge-{pos,F1,F2,F3}.{json,stdout,rc}`,
  world revision = base; each violates exactly one binding):
  `forge-pos` (G1) internally consistent label rewrite, met true → intended reason
  `label-not-frozen`; `forge-F1` (G2) label claims `repaired 12 of 12` while counts record
  10 → `label-not-recomputed`; `forge-F2` (G3) consistent but a 9-char short revision (the
  M94-f shape) → `revision-not-bound`; `forge-F3` (G4) consistent but fabricated pins
  (`verdict_sha256` 64 zeros, `counter_sha256` 64 f's) → `pins-not-bound`.
- **Frozen counting commands.**
  1. `python3 -I -B tools/round-95/c1-forgery-refusal.py --root . --fixtures .ufo/waves/round-95/forgery --old-prefix forge --old-counter tools/round-94/c1-receipt-agreement.py --honest-dir .ufo/waves/round-95/l1/scores --honest-prefix honest --world-rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 --instrument-rev <decl> --expect '<FROZEN_LABEL>' --json-out .ufo/waves/round-95/l1/scores/c1-forgery-at-<decl>.json` → exit 0.
  2. The honest positive control: the real v5 public run at the declaration revision —
     `python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --root . --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work <scratch> --rev <decl> --expect '<FROZEN_LABEL>' --json-out .ufo/waves/round-95/l1/scores/honest-pos.json > .ufo/waves/round-95/l1/scores/honest-pos.stdout 2> .ufo/waves/round-95/l1/scores/honest-pos.stderr; echo $? > .ufo/waves/round-95/l1/scores/honest-pos.rc` → exit 0, `selfverify ok=True reasons=0` line present.
  3. `python3 -I -B tools/round-95/symlink-probe.py --root . --writer tools/round-95/stop-boundary-repair-battery-v5.py --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work <scratch> --rev <decl> --expect '<FROZEN_LABEL>' --json-out .ufo/waves/round-95/l1/scores/c1-symlink-v5-at-<decl>.json` → exit 0 (`victim_intact true`, `receipt_valid true`).
- **Frozen label (the same string as rounds 93/94):**
  `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`.
- **Before (do-nothing controls, committed in this declaration, measured at base with the
  frozen round-94 instruments):**
  1. `.ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json`: the pinned r94 agreement
     counter over the forged fixtures prints `counts_of_4` valid 4, agree 4, predicted 4,
     `met true`, exit 0 — it admits all four forgeries.
  2. `.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json`: the probe against the pinned v4
     writer reports `victim_intact false`, `receipt_valid true`, verdict
     `followed-symlink` (the F1 mechanism reproduced on the public path).
  The unchanged r94 instruments are the do-nothing control: they cannot reach the target
  because they admit the forgeries and follow the symlink. A blanket-refusal instrument is
  excluded by the honest positive control (command 2; the forgery battery's honest leg).
- **Frozen target (after):** the forgery battery exits 0 with `forgeries refused 4 of 4`,
  each forgery carrying exactly its intended single typed reason, `before admits true`,
  and the honest leg accepted; the honest v5 run exits 0 with a valid self-verified
  receipt; the v5 probe leg exits 0 with the victim intact.
- **Kill rule:** the before-side not met (premise fails); any forgery accepted or carrying
  a reason other than exactly its intended one; the honest leg refused or not met;
  the honest run's receipt not valid JSON or `selfverify` not ok; the v5 probe leg victim
  changed or receipt invalid; any pinned sha256 below differing; `git diff --stat <decl>
  <landing> -- tools/round-95 tools/round-94 tools/round-93` nonempty (counter-read bytes
  changed after the freeze).
- **Pins (sha256).** Every pin is listed with its path in `.ufo/waves/round-95/pins.sha256`
  (committed expected output of `sha256sum`, the freeze precheck's source). The load-bearing
  pins: v5 `6fc81208c9b151f35c9768bc1f481a1bdd0bcc0854d9732879e38e6b87194b7f`;
  v2 `ca7d213a598fb79fd944886d480863d6464cb2217c8d2d4b9f11c7981c539291`;
  battery `8e43d7cff4d8f7eb9f4afe8e2ebdcfb3edfe6a53f019f21d0cd415457de0ff22`;
  probe `e07ff669eb6f0f8ed8b00afab2edb4b34ed81d20ad061db3be60626b659090ee`;
  frozen r94 counter `c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272`;
  frozen r94 agreement `dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9`;
  frozen v3 verdict `60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3`;
  frozen r92 repair `ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1`;
  frozen r93 `identity_noop.py` `518422b560156da6d16396e69439cfa5012b393d896408939c042dca3b719337`.
- **Measured revision.** The declaration commit (this file's commit); counter-read bytes
  (`tools/round-95/`, `tools/round-94/`, `tools/round-93/`) must be unchanged at the
  landing commit (checked by the kill rule's diff clause and recorded in a receipt).
- **Named limits (stated before data).** The strengthened bindings bind the receipt to the
  world it claims; they do not authenticate provenance — a wholly re-authored triple whose
  stdout/rc/pins/revision/label all consistently describe the honest world at the honest
  revision is indistinguishable from an honest capture at the byte level, and catching it
  needs independent stdout/rc custody, not another receipt field. The symlink probe covers
  the `<json-out>.tmp` name; it does not model a hostile `--json-out` directory symlink
  (parent-dir swap is out of scope this round). The honest world's `--expect` binding runs
  only when `met_target` is true; refusal labels are legitimately free-form. The fixture
  set is the four committed forgeries, not a claim about unlisted forgery classes.

## R95-C2 — depth: a craft decision table for the receipt-world-binding failure class

- **Surface.** Round 94 recorded that the agreement counter admits label rewrites and
  fabricated triples, that a short `--rev` went unvalidated, and that the `.tmp` write
  follows a planted symlink. No craft row names that class. Candidate: craft block 34
  (append-only; blocks 1-33 unchanged) with a decision table, corpus criteria QUALITY 191
  and 192 that state the rules the rows assert, and a knowledge entry citing the
  `open(2)` `O_NOFOLLOW` documentation (S320, opened this round).
- **Before (do-nothing control, committed here, measured at base):**
  `.ufo/waves/round-95/pre/c2-base-block34-after-manifest.json` exit 1, `block 34 missing
  (craft has 33 blocks)`; `pre/c2-base-depth-v2.txt` exit 1 `blocks 33 resolved 33 expect
  34`; `pre/c2-base-depth-v3.txt` exit 1 (`blocks 33 ... expect 34`).
- **Frozen counting commands (after, at the landing revision `<landing>`):**
  1. `python3 -I -B tools/round-93/craft-citation-semantic.py --root . --manifest .ufo/waves/round-95/manifests/block34-after.json --block 34 --rev <landing> --json-out .ufo/waves/round-95/l1/scores/c2-after-block34.json` → exit 0, `ok`.
  2. `python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev <landing> --expect-blocks 34` → exit 0, `blocks 34 resolved 34`.
  3. `python3 -I -B tools/round-91/depth-blocks-v3.py --root . --rev <landing> --expect-blocks 34 --shape-from 34` → exit 0, `required-shaped 1/1`.
  4. The rubber-stamp control at `<landing>`: `python3 -I -B tools/round-93/craft-citation-semantic.py --root . --manifest .ufo/waves/round-95/manifests/block34-junk.json --block 34 --rev <landing> --json-out .ufo/waves/round-95/l1/scores/c2-junk-at-landing.json` → exit 1 (the junk manifest carries keywords the cited criteria lack, so a checker that passed it would be a rubber stamp).
- **Frozen predicate (the keyword sets are in the manifest, frozen here):** block 34 carries
  the marker `receipt-world-binding v1` and a decision table with at least three body rows
  of at least four cells; each row's criterion cites exactly one QUALITY row whose text
  contains the row's frozen keywords: row `consistent label rewrite` → QUALITY 191 contains
  `bound to the frozen expect label` and `when met_target is true`; row `counts that do not
  recompute the label` → QUALITY 191 contains `recompute the label from its own counts`;
  row `revision field not the measured tree` → QUALITY 192 contains `full measured
  revision` and `git rev-parse`; row `temp-file symlink escape` → QUALITY 192 contains
  `unique temporary name` and `planted`.
- **Frozen target (after):** commands 1-3 exit 0 at the landing revision; command 4 exits 1;
  block 34 absent at base (done above); no depth regression: blocks 1-33 intact (v2 counts
  34 of 34 resolved).
- **Kill rule:** any of commands 1-3 unmet at the landing revision; command 4 exit 0 (rubber
  stamp); block 34 present at base; the checker `craft-citation-semantic.py` sha256
  (`34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`), the depth counters'
  sha256s (`depth-blocks-v2.py` `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f`,
  `depth-blocks-v3.py` `bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f`)
  or the manifest sha256 (`cf5f265f7500d1315f7b141332fff1dd9c60c74f189c53bdad1b1ac91fd03ba8`)
  differing from the pins.
- **Named limit (stated before data).** The keyword atom is a vocabulary check (QUALITY 188
  residual): a criterion that carries the keywords passes whether or not it states the rule.
  C2 does not claim more than the vocabulary check plus the junk-manifest control.

## Sourced claim (frontier step)

R95-C1's and R95-C2's knowledge entry cites `S320` (`open(2)` man page, man-pages 6.19,
`O_NOFOLLOW` flag description, located quote ≤25 words: "If the trailing component (i.e.,
basename) of path is a symbolic link, then the open fails, with the error ELOOP"), opened
2026-11-05 at `https://man7.org/linux/man-pages/man2/open.2.html`; two byte-identical
fetches (HTTP 200, 76506 bytes, sha256
`d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`) are committed at
`.ufo/waves/round-95/l1/scores/s320-open2-fetch{1,2}.html`, and the Gate record lands in
`corpus/lessons/round-95.md` `## Gate`.

## Exploratory claims

None. Two counting claims.

## Honest stop

Both claims are single-commit byte-level predicates a closure can re-derive with one
command. Neither target is narrowed after landing: a miss is reported as a miss.
