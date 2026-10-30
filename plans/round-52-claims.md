# kaidoku round 52 — claims (attempt 1)

Round base `c525de54a53eb3c4fee28ede2721da4527cf8ece` (lane `main` tip at round start, pushed,
`jj-lane.sh state`: `ahead=0 behind=0 tracked=0 untracked=0`). This file is the round
declaration; the **freeze** is the single later commit that adds the round-52 instruments,
fixtures and this file's amended text, recorded in `LOG.md` and
`.ufo/waves/round-52/l1/FREEZE` before any data run. Amendments after wave-1 attacks land in
the freeze commit and are listed in `## Wave-1 amendment record` (empty until then); a counter
bug found after the freeze is a miss, never a patch.

Provenance: this round ports the round-51 declaration (`plans/round-51-claims.md`, claims draft
`f04b51dd`, honest stop) with its wave-1 amendments F1–F11 **baked in as the starting text**.
Round 51 landed no instrument and ran no data; the round-50 C1 miss (`carriers_matched 2`,
`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`) remains the committed before-state both
claims repair or supersede. The round-50 carrier cache was removed by the run-11 wrap-up sweep;
the data run re-fetches all four carriers through the pinned vendor chain.

Owned axes coverage / depth / calibration sit tied at 10 in `SCORECARD.md` (none retired):
every owned axis is a lowest axis, so both claims satisfy the lowest-axis rule. **R52-C1 works
coverage; R52-C2 works depth.** They are causally separable: C1 reads the four chain-pinned
vendor carriers (never committed), the round-52 counter/controls over the committed round-50
receipts and oracle tables, and its documentation bindings; C2 reads `SKILL.md` rule blocks 26
and 27, the round-42 recon envelope corpus, the registry census, and its own new instrument.
The two claims share no write surface except record sections in `SCORECARD.md` and `LOG.md`
(separate sections) — each is verifiable without the other having landed.

## R52-C1 — coverage: the char-device accounting law, re-frozen from per-carrier-class derivation

Surface moved: `PROVINCE.md` `## Frontier` entry **LE AVM members (`hsqs`)** — the round-50
measurement published every frozen-oracle regular file on all four carriers but the frozen gap
rule failed `gaps_ok` on the two FRITZ!Box-class carriers: its `removed.silent.char-device`
allowance `["247:0"]` was generalised from the Cable-carrier class (one char-device,
`dev/led 247:0`) and leaves the FRITZ!Box class's twelve other char-devices
(`dev/pts/0-7 136:0-7`, `dev/tiatm 230:0`, `dev/ttyp0-2 3:0-2`) with neither a matching gap nor
a removal (M50-7; `MutC1Counter` F10: the unaccounted set is exactly those twelve details).
The miss was decided, not assumed; the repair is a **new freeze**, not an amendment.

**The device-accounting law (derived round 51 from per-carrier-class enumeration of
`tools/round-50/oracle/<id>.nonregular.tsv`, stated before the freeze; r51 amendments
F1–F11 baked in):** the extraction producer (REA 6.5.0 `extract-firmware`, handler
`squashfs_v4_le`, unblob 26.6.4 → sasquatch `-le`) materialises regular files and directories
and re-creates symlinks (with a `MaliciousSymlinkRemoved` diagnostic when it refuses one), but
it creates **no device nodes, fifos or sockets** — an unprivileged extraction cannot `mknod` a
device — and it emits **no gap record for them**: a char-device/fifo/socket oracle entry
carries **no disposition at all**, and because the law is that no gap record exists for such an
entry, the frozen rule admits **no** gap kind for those kinds (`allowed` for a device kind is
the empty list; `required['char-device'] = false` — r51 amendment F3, measured by
ScribeScorecard: the required-true variant scores 0/4 over the committed round-50 envelopes,
the required-false variant 4/4), so a gap landing on a device row is a violation of the law,
not a tolerated state — a future extractor that starts emitting a device gap turns the rule
**red** (fail closed). Source ground: unsquashfs 4.7.5 gates char/block `mknod` behind
`if(root_process)` while FIFO/socket creation calls sit outside that gate (S250, tag
4.7.5 `:1287/:1296/:1328/:1349`); the kernel-side gate is CAP_MKNOD on device files
(S252, opened this round). **Width:** for the four measured LE AVM carriers, every char-device
row of the independent census carries no extraction gap and no published path (28 of 28 rows);
the generalisation to fifo/socket/block rests on the source ground and the corpus does not yet
exercise it — no fifo, socket or block-device row exists in any measured carrier (F5 width
statement, unchanged). The law claims only entries the extractor **reached**: the receipts do
not name the path a `depth-limited` gap stopped at (`relative_path` is null), and a device-only
subtree never descended into cannot be distinguished from one reached and correctly produced no
gap; the v2 counter records the `depth-limited` gap's `input_path` and `continuation_id` in its
receipt so the limit stays visible (F8). **Cross-claim obligation:** the per-carrier-class
derivation enumerates each class's non-regular census from its own committed oracle table
(`tools/round-50/oracle/<id>.nonregular.tsv`): Cable class (c6430, c6490) carries exactly one
char-device; FRITZ!Box class (g7581, g7582) carries thirteen. The law, not a detail whitelist,
is what the v2 rule encodes; the class distinction is a property of the carriers' device
census, not of the rule. R52-C2's block 27 supersedes or scopes SKILL.md's
*"`symlink` and `special` both count"* phrasing (rule block 26 rows) so the two claims land no
contradiction about device nodes; the correction is listed in `## Wave-1 amendment record`.

Claim: land the re-frozen package — `tools/round-52/gap-rule.json` (the law-derived rule),
`tools/round-52/c1-counter.py` (v2 counter, ports `tools/round-50/c1-counter.py` semantics to
the round-52 freeze), `tools/round-52/c1-controls.py`, `tools/round-52/c1-run.sh`,
`tools/round-52/fetch-vendor.py` (with the network-guard selftests the routed defect demands) —
and promote LE AVM members (`hsqs`) Frontier → Core, such that:

- **Carrier set (F1, option b):** R52-C1 adds **no new carrier**; it re-measures the four
  carriers the round-50 freeze already scored, under the corrected device-accounting law.
  `tools/round-50/carriers.json` joins the v2 counter's `PRIOR_CARRIER_TABLES`; the four pins
  are listed in the round-52 carrier table's `prior_pins`; the v2 counter honours an explicit,
  frozen `re_scored_pins` allow-list for exactly those four pins (`carrier_fresh_ok` = pin
  fresh OR pin on the frozen allow-list; the receipt names `prior_pin_sources` and the
  allow-list so the waiver is visible, never silent). The anti-replay clause is waived for
  these four pins by that explicit list, and the Frontier → Core promotion rests on the
  completed 4/4 measurement under the corrected law, not on new carrier coverage.
- **Predicate** (the same sentence in this file, the counter docstring, and the receipt
  label): at a REV descending from the R52 freeze, with every frozen path unchanged
  (`frozen_path_changed []`), running
  `python3 -I -B tools/round-52/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>
  --receipts corpus/evidence/round-52/c1 --json-out <OUT>` exits **0** with
  `carriers_matched == 4`, `gaps_ok true` on every carrier, `law_shape_ok true` (the frozen
  rule lists no char-device/fifo/socket/block detail under `removed.silent` and `allowed` for
  those kinds is the empty list — the rule-shape clause that separates the law from a detail
  whitelist; F3/F4), `census_rederived_ok true` (the v2 counter re-derives the **non-regular**
  census at score time with the frozen reader/`unsquashfs -lln` and requires the frozen
  `*.nonregular.tsv` row sets in both directions, exit 2 `oracle_env_error` when the reader
  cannot run — F7), `depth_gap_recorded true` (the receipt records the `depth-limited` gap's
  `input_path` and `continuation_id` — F8), and every binding true.
- **Before (measured, already committed):** the round-50 frozen counter at its freeze exits 1
  with `carriers_matched 2` (`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`). The
  round-50 miss on `g7581` had **two** independent causes, both recorded in that receipt:
  `gaps_ok` false (the twelve unaccounted device rows) **and** `projection_ok` false (the
  counter's own REA rerun failed with `execution_failure`, ENOENT on
  `readlink …/usr/www.myfritz/avme/cgi-bin/luacgi`, `retryable: false`); `g7582` failed only
  `gaps_ok`. The re-freeze repairs the first cause. The second is handled by the **projection
  retry policy, claimed and controlled this round** (r51 disposition: no retry policy is
  admitted without proof able to fail): the v2 counter's REA rerun allows up to 3 attempts on
  REA's own `provider_timeout` (the proven flake class) and up to 2 attempts on an
  `execution_failure` whose failing diagnostic is an ENOENT naming a path inside the extraction
  tree, each rerun on a fresh extraction root with attempt count and failing diagnostic
  recorded; a frozen control (deterministic-ENOENT fixture tree) demonstrates the same failure
  surviving all attempts still scores **red**, so the policy is shown able to fail; a rerun
  failing with any other error is a red. If `g7581`'s projection still fails after the policy
  exhausts, the claim is missed as frozen — honest stop, no narrowing, no amendment.
- **Pre-freeze controls (rule-scoped, over committed bytes, no live rerun — F2):** the two
  rule controls evaluate the frozen **disposition verdict** (`gaps_ok` ∧
  `nonregular_unpublished_ok`) of a named gap rule over the committed round-50 **envelopes**
  `corpus/evidence/round-50/c1/<id>/after.json` plus the committed round-50 oracle /
  non-regular tables (NOT the `run.json` harness receipts):
  - CTL-OLD (the **reproducibility control** — F9): the round-50 gap rule over those envelopes
    yields **2 of 4** dispositions (Cable passes, FRITZ!Box fails `gaps_ok`), exit 1 —
    reproducing the committed miss receipt. If it yielded 4, the round-50 miss is not
    reproducible and the round-50 closure's diagnosis is wrong — stop and report that.
  - CTL-NEW (the derivation consistency control): the round-52 law rule over the same
    envelopes yields **4 of 4**, exit 0.
  - The full predicate is **not** claimed for the controls: the committed round-50 receipts
    fail `run_provenance_ok` (round-50 provenance prefix), `receipt_fresh` and every
    byte-dependent clause (`carrier_present`, `carrier_pin_ok`, `oracle_rederived_ok`,
    `projection_ok` — the round-50 carrier cache no longer exists and a rerun is forbidden
    pre-freeze). The v2 counter therefore exposes the round-sensitive constants as explicit
    flags (`--gap-rule`, `--receipts`, `--provenance-base`, `--receipt-fresh-base`) and the
    control driver pins the round-50 values; the rule-scoped verdict is recomputed by the v2
    counter from the frozen receipt bytes and the frozen rule.
  - CTL-DN (semantic red): the v2 counter against a do-nothing fixture tree (no receipts)
    exits 1 or 2, never 0; CTL-JUNK: a syntactically valid junk rule (every kind required with
    an impossible allowance) scores 0 of 4, exit 1.
  - **Rule mutations (frozen; F4):** (M1) the **all-thirteen whitelist**
    (`required.char-device=true`, `removed.silent.char-device` naming all thirteen observed
    details) must be **RED** — red by the frozen rule-shape clause `law_shape_ok`, because no
    carrier in the corpus carries a fourteenth device and the law and that whitelist are
    extensionally identical over the measured data; (M2) a fixture carrier whose non-regular
    census carries a **fourteenth, unlisted device** (e.g. `dev/ttyS0 4:64`) must be **GREEN
    under the law rule and RED under any detail whitelist**; (M3, regression)
    `required.char-device=true` with only `247:0` silent reproduces the round-50 miss;
    (M4, regression) a strict-subset whitelist stays red (the M50 partial-widening trap).
  - Kill rule: CTL-NEW red, CTL-OLD yielding 4, or any mutant green that should be red → stop
    before the data run; report as a miss.
- **Freeze-drift gating (routed defect 3):** a modified frozen path at REV yields exit 2 with
  `frozen_path_changed` naming the path; a selftest case demonstrates exit 2 on a fixture
  clone with one mutated frozen byte.
- **Rule grammar (F10):** the v2 `gap_rule_model` accepts the claim labels `{R50-C1, R52-C1}`
  (the CTL-OLD arm scores the round-50 rule; CTL-NEW the round-52 rule); the frozen round-52
  rule carries `"claim": "R52-C1"`.
- **Data run (post-freeze, L1 only, quiet window):** `tools/round-52/fetch-vendor.py` re-fetches
  each carrier through the pinned chain (vendor image URL → member extraction → member pin
  verification) into `/fast/scratch/hyaku/kaidoku-r52/carrier-cache/` (vendor bytes never
  committed; the round-50 cache no longer exists and no cached byte is trusted without its
  pin), then `tools/round-52/c1-run.sh after --id <id> --carrier <CACHE>/<pin>.bin --data-run`
  per carrier, and `c1-run.sh oracle --id <id>` for the independent oracle arms. Receipts under
  `corpus/evidence/round-52/c1/<id>/`. If the fresh run reports `carriers_matched < 4`, the
  claim is missed as frozen — honest stop, no narrowing, no amendment.
- **Landing bindings (all true at the landing REV, each re-derivable by the counter):** the
  knowledge entry `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` (constants: entry
  stem `2026-10-30-r52-avm-le-squashfs-core`, `core_heading` `## Round-52 additions to Core`,
  `frontier_mark` `Round-52 frontier note`, `opened` `2026-10-30`, `prov_base`
  `/fast/scratch/hyaku/kaidoku-r52`) exists, cites S243/S244/S245/S249, S250/S251, the
  round-52 SOURCES row(s) opened this round, and names the fresh receipts; `PROVINCE.md`
  carries `## Round-52 additions to Core` with the LE members row and an updated frontier note
  (LE `hsqs` leaves the Frontier list); `corpus/README.md` coverage map row for the entry;
  `corpus/SOURCES.md` new row(s) list the entry in `used-by`; `SCORECARD.md` coverage head
  names 141/141 → 142/142 (the map's 142nd file is this entry); LOG entry.
- **Counting command:** the predicate command, run once at the landing REV (after) with the
  committed fresh receipts; the before-arm is the committed round-50 receipt named above plus
  CTL-OLD. Receipts: `.ufo/waves/round-52/l1/scores/c1-{before,after}.json`.
- **Registry:** every new `.py`/`.sh`/`.json` instrument under `tools/round-52/` gets exactly
  one `instrument-registry v2` row; no other code files land there.

## R52-C2 — depth: the ddwrt failed-body route fix (executability audit) over the landed census

Surface moved: `SKILL.md` rule block 26 (triage table v5) — the disclosed residue the round-50
closure routed and round 51 left unimplemented:

1. **Failed-body route:** the v5 comma-list keeps `squashfs_v3_ddwrt` in
   `legacy-body-failure`, so the ddwrt FAILED no-pad body `dmg_Z3_v3ddwrt_inode_table` is
   routed `legacy-body-failure`/`cross-read-legacy` — **a cross-read prescribed on a body
   whose readers refuse** (the ddwrt family has no validated second reader; 6/7 no-reader).
   A prescribed action the corpus cannot execute is a depth defect: the rule as written cannot
   be followed. The v5 disclosure left it unfixed ("needs a body-variant discriminator that
   does not exist in the scored features").
2. **Registry-census state (inherited, no longer a move):** round 51 landed
   `tools/round-51/census3.py` + `census3.json`; the active census equals the registry at the
   base (`--check` exit 0, receipts `.ufo/waves/round-51/l1/census3-after.json`). The census
   drift 13 → 0 already landed; this round's instrument **embeds the census clause** so the
   v6 audit cannot regress it, and reports `census_outside 0` at both before and after. It is
   a no-regression binding, not a claimed move.

Claim: land **triage table v6** as `SKILL.md` rule block 27 (dated supersession of block 26's
ddwrt rows; block 26 stays as history) plus the scoring instrument
`tools/round-52/sqfs-triage-v6.py` (ports `tools/round-50-c3/sqfs-triage-v5.py`; freeze-drift
**gating**, routed defect 3), such that:

- **Predicate** (the same sentence in this file, the instrument docstring, and the receipt
  label): at a REV descending from the R52 freeze, with every frozen path unchanged, running
  `python3 -I -B tools/round-52/sqfs-triage-v6.py --root <LANE> --rev <REV> --freeze <FREEZE>
  --envelopes <DIR> --json-out <OUT>` exits **0** with `pair_mismatches 0`,
  `evaluator_missing 0`, `executability_violations 0`, `census_outside 0`, and a green
  selftest (every committed mutation flips ≥1 pair or ≥1 audit finding, none a no-op,
  do-nothing red); and at the declared claims-draft base the same command with
  `--table tools/round-50-c3` (the v5 table bytes) exits **1** with
  `executability_violations 1` naming `dmg_Z3_v3ddwrt_inode_table`.
- **The v6 change:** for a FAILED-body envelope of a family with **no validated independent
  reader** (the frozen reader-census table from the round-49 entry, cited by block 26), the
  routed label becomes a new row (`legacy-body-unreadable`) whose action prescribes **no
  cross-read** (`preserve-unresolved`); the evaluator implements the same precedence; the
  executability audit (new, frozen) checks every FAILED-body envelope's prescribed action
  against the family's reader census and counts violations — the audit is what makes the
  before-state measurable (v5: 1; v6: 0). The two clean ddwrt no-pad `_ddefault` envelopes
  keep `clean` (their readers succeeded; no route change). Per CritTriV6 (r51): clean
  extraction is not independent-reader success; the v6 audit's reader-census table states the
  census per family with its evidence pointer, and no new reader is claimed validated.
- **Held-out corpus:** the same frozen 126-envelope corpus
  (`.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`); same disclosed limit as
  R50-C3 (depth, not held-out generalization). v6 must keep every v5 label unchanged except
  the one ddwrt FAILED-body pair.
- **Controls (scored with the frozen instrument BEFORE the table lands, receipts committed):**
  do-nothing (the v5 table at base → audit red), junk table (syntactically valid, wrong labels
  → `pair_mismatches > 0`, exit 1), audit-guard-deleted mutant → red, swapped-new-row-action
  mutant → red, census-guard-deleted mutant → red. Kill rule: any of these green at the freeze
  → stop, report as a miss.
- **Counting command:** the predicate command, run twice — before at the claims-draft base
  (this file's commit), after at the landing REV. Receipts:
  `.ufo/waves/round-52/l1/scores/c2-{before,after}.json`.
- **Registry:** exactly one `instrument-registry v2` row for the v6 instrument; no other code
  files land under `tools/round-52/` beyond the claims' named files.

## Routed-defect repairs (obligations from the round-51 closure — not claims)

1. **Round shape below band (r51):** this round sizes inside the band: one v2 wave of 64
   (build + attack, ≥25 % attack roles) and a falsify wave dispatched after the landing when
   ≥32 distinct attack items exist (32–64 seats), else one residual `task` call of ≤8
   reviewer/critic seats; round total ≤128. Recorded per wave in the report.
2. **Per-seat results fields (r51):** every wave-1 seat writes
   `.ufo/waves/round-52/w1/<SeatName>/status.json` (`seat`, `name`, `status`, `summary`,
   `artifacts[]`); the L1's wave accounting reads those files, not the results handoff text.
3. **Dispatch interpolation (M51-6):** the wave generator asserts before dispatch that no item
   string contains an unresolved `{PLACEHOLDER}` marker; the check and its output are committed
   wave evidence.
4. **`fetch-vendor.py` network-guard selftests (routed defect 4, carried):** the repaired copy
   at `tools/round-52/fetch-vendor.py` gains offline selftests proving each guard
   (https-scheme, pinned-host) fails closed: guard deleted → selftest red, guards present →
   green, shown able to fail on fixture inputs.
5. **Preventive fleet-root stray control (operator-side, M50-9/M51-1):** the lane lands a
   read-only sweep helper `tools/round-52/misroot-sweep.sh` (reads
   `git -C <fleet> status --porcelain`, classifies strays by content, never writes) with a
   fixture-repo selftest; the operator-side prevention stays an L0-class note in the report.
6. **Census hygiene:** the 19 W04 duplicate-URL warnings stand as named debt unless a seat's
   row-by-row audit lands a correction set under CORPUS.md rule 2 this round; any correction
   row supersedes old→new and is logged in the lesson.
7. **Open L0 (carried):** unredacted session cookies in pushed history — `kaidoku | round-50`
   stands; not re-appended; no credential use this round.

## Frontier step (inside the claim cap)

- **Sourced claims:** C1's entry cites the round-52 SOURCES row S252 (man7 `mknod(2)`, opened
  this round by the L1 and a scout, CAP_MKNOD ground for the device law) plus
  S243/S244/S245/S249/S250/S251; C2's block cites the round-49 reader-census entry and S251.
  Every new row's `## Gate` record carries URL, access date, ≤25-word located quote;
  rejections stay as rows.
- **Assimilation:** ONE theme from `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` (read-only)
  serving this round's ground, 1–3 entries re-grounded in-round with per-entry gates
  (≥1 admit, ≥1 reject recorded), or the report says `Assimilation: none` with the scan
  receipt. The package stages 132 rows at ids S106+ while the lane registry holds 158 rows —
  mass id drift is expected; the id-collision check runs in scratch before any append, and any
  adopted row is renumbered to continue the lane's S-space **by document** (the URL/anchor is
  the evidence), with both id lists, the collision count and the renumber map in the report.
  The scratch mirror must pass `sources-census.sh validate --file` exit 0 before the first
  append. `considerthese/` does not exist in this lane; one report line.
- **Mistakes mined:** appended to `corpus/lessons/round-52.md` `## Mistakes`
  (class · evidence · captured-by · fix), from this round or the round-51 closure/spotcheck;
  a fix counts only once shown able to fail. Found none → paste the sweep.
- **Census:** before = `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  kaidoku` receipt at round start; end = the same command re-taken at the filing tip, exit 0
  required.

## Round shape

One v2 wave (policy `ufo-wave-policy-v2.json`, band 64–128): **w1 = 64 seats**, build + attack
mixed, attack roles ≥25 % (reviewer, critic, mutation-tester, labrat, sentinel, revenger),
a few connector seats; the §3 planner seat is the L1 (the validator rejects `planner`). A
**w2 falsify** wave (32–64 seats, policy v1) is dispatched after the landing only when w1's
output yields ≥32 distinct attack items; otherwise one residual `task` call of ≤8 seats.
Round total ≤128. Waves dispatch through the inline spawn handoff (`<wave>.ready`), never by
the L1 calling `task`; the report files only after WAVE-DONE for every launched wave.

## Wave-1 amendment record

(empty until wave-1 attacks land; amendments land in the freeze commit)
