# kaidoku round 51 — claims (attempt 1)

Round base `1aa273694f4409d3432fbcd73e83a33bee0dd8e9` (lane `main` tip at round start, pushed,
`jj-lane.sh state`: `ahead=0 behind=0 untracked=0`); claims-draft commit
`f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`; wave-1 dispatch commit
`39f41d4f15a87689a41c16c5c17ed885fbfb7da3`. The C2 before-arm base is the claims-draft commit
`f04b51dd…` (F11). Round 50 attempt 2 landed R50-C3 (depth, met)
and measured R50-C1 as a miss under its frozen gap rule (`carriers_matched 2` of target 4);
the round-50 closure routed the repairs and the SCORECARD `planned (round 51)` rows name this
round's work. This file is the round declaration; the **freeze** is the single later commit
that adds the round-51 instruments, fixtures and this file's amended text, recorded in `LOG.md`
and `.ufo/waves/round-51/l1/FREEZE` before any data run. Amendments after wave-1 attacks land
in the freeze commit and are listed in `## Wave-1 amendment record` (empty until then); a
counter bug found after the freeze is a miss, never a patch.

Owned axes coverage / depth / calibration sit tied at 10 in `SCORECARD.md` (none retired):
every owned axis is a lowest axis, so both claims satisfy the lowest-axis rule. **R51-C1 works
coverage; R51-C2 works depth.** They are causally separable: C1 reads the four chain-pinned
vendor carriers (never committed), the round-51 counter/controls over the committed round-50
receipts and oracle tables, and its documentation bindings; C2 reads `SKILL.md` rule block 26,
the round-42 recon envelope corpus, the registry census, and its own new instrument. The two
claims share no write surface except record sections in `SCORECARD.md` and `LOG.md` (separate
sections) — each is verifiable without the other having landed.

## R51-C1 — coverage: the char-device accounting law, re-frozen from per-carrier-class derivation

Surface moved: `PROVINCE.md` `## Frontier` entry **LE AVM members (`hsqs`)** — the round-50
measurement published every frozen-oracle regular file on all four carriers but the frozen gap
rule failed `gaps_ok` on the two FRITZ!Box-class carriers: its `removed.silent.char-device`
allowance `["247:0"]` was generalised from the Cable-carrier class (one char-device,
`dev/led 247:0`) and leaves the FRITZ!Box class's twelve other char-devices
(`dev/pts/0-7 136:0-7`, `dev/tiatm 230:0`, `dev/ttyp0-2 3:0-2`) with neither a matching gap nor
a removal (M50-7; `MutC1Counter` F10: the unaccounted set is exactly those twelve details;
only all-thirteen whitelists, `required['char-device']=false`, or counter-code mutations turn
the frozen rule green). The miss was decided, not assumed; the repair is a **new freeze**, not
an amendment (SCORECARD `planned (round 51)`).

**The device-accounting law (derived in this round, stated before the freeze; wave-1
amendments F3/F5/F8 applied):** the extraction producer (REA 6.5.0 `extract-firmware`,
handler `squashfs_v4_le`, unblob 26.6.4 → sasquatch `-le`) materialises regular files and
directories and re-creates symlinks (with a `MaliciousSymlinkRemoved` diagnostic when it
refuses one), but it creates **no device nodes, fifos or sockets** — an unprivileged
extraction cannot `mknod` — and it emits **no gap record for them**: a char-device/fifo/socket
oracle entry carries **no disposition at all**, and because the law is that no gap record
exists for such an entry, the frozen rule admits **no** gap kind for those kinds (`allowed`
for a device kind is the empty list), so a gap landing on a device row is a violation of the
law, not a tolerated state — a future extractor that starts emitting a device gap turns the
rule **red** (fail closed). **Width:** for the four measured LE AVM carriers, every
char-device row of the independent census carries no extraction gap and no published path
(28 of 28 rows); the generalisation to the device-node kinds (char/block device, fifo, socket)
rests on the unprivileged-`mknod` ground and the corpus does not yet exercise it — no fifo,
socket or block-device row exists in any measured carrier. The law's primary grounding is the
measurement (the four committed envelopes); the unsquashfs/squashfs-tools source rows ground
the **census**, not the extractor's silence. The law is a statement about the entries the
extractor **reached**: the receipts do not name the path a `depth-limited` gap stopped at
(`relative_path` is null), and a device-only subtree (e.g. `dev/pts/`, which holds no regular
file) never descended into cannot be distinguished from one reached and correctly produced no
gap; the v2 counter records the `depth-limited` gap's `input_path` and `continuation_id` in
its receipt so the limit stays visible. **Cross-claim obligation:** the per-carrier-class
derivation enumerates each class's non-regular census from its own committed oracle table
(`tools/round-50/oracle/<id>.nonregular.tsv`): Cable class (c6430, c6490) carries exactly one
char-device; FRITZ!Box class (g7581, g7582) carries thirteen. The law, not a detail whitelist,
is what the v2 rule encodes; the class distinction is a property of the carriers' device
census, not of the rule. R51-C2's block 27 supersedes or scopes SKILL.md's
*"`symlink` and `special` both count"* phrasing (rule block 26 rows) so the two claims land no
contradiction about device nodes; the correction is listed in `## Wave-1 amendment record`.

Claim: land the re-frozen package — `tools/round-51/gap-rule.json` (the law-derived rule),
`tools/round-51/c1-counter.py` (v2 counter, ports `tools/round-50/c1-counter.py` semantics to
the round-51 freeze), `tools/round-51/c1-controls.py`, `tools/round-51/c1-run.sh`,
`tools/round-51/fetch-vendor.py` (with the network-guard selftests the routed defect demands) —
and promote LE AVM members (`hsqs`) Frontier → Core, such that:

- **Carrier set (decided at this freeze; wave-1 amendment F1, option b):** R51-C1 adds **no
  new carrier**; it re-measures the four carriers the round-50 freeze already scored, under
  the corrected device-accounting law. `tools/round-50/carriers.json` joins the v2 counter's
  `PRIOR_CARRIER_TABLES`, the four pins are listed in the round-51 carrier table's
  `prior_pins`, and the v2 counter honours an explicit, frozen `re_scored_pins` allow-list for
  exactly those four pins (`carrier_fresh_ok` = pin fresh OR pin on the frozen allow-list;
  the receipt names `prior_pin_sources` and the allow-list so the waiver is visible, never
  silent). The anti-replay clause is waived for these four pins by that explicit list, and the
  Frontier → Core promotion rests on the completed 4/4 measurement under the corrected law,
  not on new carrier coverage.
- **Predicate** (the same sentence in this file, the counter docstring, and the receipt
  label): at a REV descending from the R51 freeze, with every frozen path unchanged
  (`frozen_path_changed []`), running
  `python3 -I -B tools/round-51/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE>
  --receipts corpus/evidence/round-51/c1 --json-out <OUT>` exits **0** with
  `carriers_matched == 4`, `gaps_ok true` on every carrier, `law_shape_ok true` (the frozen
  rule lists no char-device/fifo/socket/block detail under `removed.silent` and `allowed` for
  those kinds is the empty list — the rule-shape clause that separates the law from a detail
  whitelist; wave-1 amendment F4), `census_rederived_ok true` (the v2 counter re-derives the
  **non-regular** census at score time with the frozen reader/`unsquashfs -lln` and requires
  the frozen `*.nonregular.tsv` row sets in both directions, exit 2 `oracle_env_error` when
  the reader cannot run — wave-1 amendment F7), `depth_gap_recorded true` (the receipt records
  the `depth-limited` gap's `input_path` and `continuation_id` — F8), and every binding true.
- **Before (measured, already committed):** the round-50 frozen counter at its freeze exits 1
  with `carriers_matched 2` (`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`); its
  before-arm re-measurement command stays the SCORECARD round-50 row's. The round-50 miss on
  `g7581` had **two** independent causes, both recorded in that receipt: `gaps_ok` false (the
  twelve unaccounted device rows) **and** `projection_ok` false (the counter's own REA rerun
  failed with `execution_failure`, `retryable: false`, ENOENT on
  `readlink …/usr/www.myfritz/avme/cgi-bin/luacgi`); `g7582` failed only `gaps_ok`. The
  re-freeze repairs the first cause. The second is handled in the v2 counter: a REA
  `execution_failure` whose diagnostic is an ENOENT on a path inside the extraction tree is
  treated as a **retryable environment error** (as `provider_timeout` already is, ≤3 attempts,
  attempt count and failing diagnostic recorded); a rerun failing with any other error is a
  red (wave-1 amendment F6).
- **Pre-freeze controls (rule-scoped, over committed bytes, no live rerun — wave-1 amendment
  F2):** the two rule controls evaluate the frozen **disposition verdict** (`gaps_ok` ∧
  `nonregular_unpublished_ok`) of a named gap rule over the committed round-50 **envelopes**
  `corpus/evidence/round-50/c1/<id>/after.json` plus the committed round-50 oracle /
  non-regular tables (NOT the `run.json` harness receipts):
  - CTL-OLD (the **reproducibility control** — wave-1 amendment F9): the round-50 gap rule
    over those envelopes yields **2 of 4** dispositions (Cable passes, FRITZ!Box fails
    `gaps_ok`), exit 1 — reproducing the committed miss receipt. If it yielded 4, the round-50
    miss is not reproducible and the round-50 closure's diagnosis is wrong — stop and report
    that. (The do-nothing arm is CTL-DN, separate below.)
  - CTL-NEW (the derivation consistency control): the round-51 law rule over the same
    envelopes yields **4 of 4**, exit 0.
  - The full predicate is **not** claimed for the controls: the committed round-50 receipts
    fail `run_provenance_ok` (round-50 provenance prefix), `receipt_fresh` (added at
    `646d29c9`, before the round-51 freeze) and every byte-dependent clause (`carrier_present`,
    `carrier_pin_ok`, `oracle_rederived_ok`, `projection_ok` — the round-50 carrier cache no
    longer exists and a rerun is forbidden pre-freeze). The v2 counter therefore exposes the
    round-sensitive constants as explicit flags (`--gap-rule`, `--receipts`,
    `--provenance-base`, `--receipt-fresh-base`) and the control driver pins the round-50
    values; the rule-scoped verdict is recomputed by the v2 counter from the frozen receipt
    bytes and the frozen rule.
  - CTL-DN (semantic red): the v2 counter against a do-nothing fixture tree (no receipts)
    exits 1 or 2, never 0; CTL-JUNK: a syntactically valid junk rule (every kind required with
    an impossible allowance) scores 0 of 4, exit 1.
  - **Rule mutations (frozen; wave-1 amendment F4):** (M1) the **all-thirteen whitelist**
    (`required.char-device=true`, `removed.silent.char-device` naming all thirteen observed
    details) must be **RED** — red by the frozen rule-shape clause `law_shape_ok`, because no
    carrier in the corpus carries a fourteenth device and the law and that whitelist are
    extensionally identical over the measured data; (M2) a fixture carrier whose non-regular
    census carries a **fourteenth, unlisted device** (e.g. `dev/ttyS0 4:64`) must be **GREEN
    under the law rule and RED under any detail whitelist** (the v1 fixture builder's
    `nonreg_over` mechanism supports this); (M3, regression) `required.char-device=true` with
    only `247:0` silent reproduces the round-50 miss; (M4, regression) a strict-subset
    whitelist stays red (the M50 partial-widening trap).
  - Kill rule: CTL-NEW red, CTL-OLD yielding 4, or any mutant green that should be red → stop
    before the data run; report as a miss.
- **Freeze-drift gating (routed defect 3; the v1 counter already exits 2 on
  `frozen_path_changed` — the v2 keeps that and adds the selftest case):** a modified frozen
  path at REV yields exit 2 with `frozen_path_changed` naming the path; a selftest case
  demonstrates exit 2 on a fixture clone with one mutated frozen byte.
- **Rule grammar (wave-1 amendment F10):** the v2 `gap_rule_model` accepts the claim labels
  `{R50-C1, R51-C1}` (the CTL-OLD arm scores the round-50 rule; CTL-NEW the round-51 rule);
  the frozen round-51 rule carries `"claim": "R51-C1"`.
- **Data run (post-freeze, L1 only, quiet window):** `tools/round-51/c1-run.sh after --id <id>
  --carrier <CACHE>/<pin>.bin --data-run` per carrier into
  `/fast/scratch/hyaku/kaidoku-r51/carrier-cache/` (chain re-pinned by
  `tools/round-51/fetch-vendor.py`; vendor bytes never committed). Receipts under
  `corpus/evidence/round-51/c1/<id>/`. If the fresh run reports `carriers_matched < 4`, the
  claim is missed as frozen — honest stop, no narrowing, no amendment.
- **Landing bindings (all true at the landing REV, each re-derivable by the counter):** the
  knowledge entry `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` (constants:
  entry stem `2026-10-30-r51-avm-le-squashfs-core`, `core_heading` `## Round-51 additions to
  Core`, `frontier_mark` `Round-51 frontier note`, `opened` `2026-10-30`, `prov_base`
  `/fast/scratch/hyaku/kaidoku-r51`) exists, cites S243/S244/S245/S249 and the round-51
  SOURCES row(s) opened this round, and names the fresh receipts; `PROVINCE.md` carries
  `## Round-51 additions to Core` with the LE members row and an updated frontier note
  (LE `hsqs` leaves the Frontier list); `corpus/README.md` coverage map row for the entry;
  `corpus/SOURCES.md` new row(s) list the entry in `used-by`; `SCORECARD.md` coverage head
  names 141/141 (the map's 141st file is this entry); LOG entry.
- **Counting command:** the predicate command, run once at the landing REV (after) with the
  committed fresh receipts; the before-arm is the committed round-50 receipt named above plus
  CTL-OLD. Receipts: `.ufo/waves/round-51/l1/scores/c1-{before,after}.json`.
- **Registry:** every new `.py`/`.sh` under `tools/round-51/` gets exactly one
  `instrument-registry v2` row; no other code files land there.

## R51-C2 — depth: the ddwrt failed-body route fix (executability audit) + the registry-census re-derivation

Surface moved: `SKILL.md` rule block 26 (triage table v5) — two disclosed residues the round-50
closure routed:

1. **Failed-body route:** the v5 comma-list keeps `squashfs_v3_ddwrt` in `legacy-body-failure`,
   so the ddwrt FAILED no-pad body `dmg_Z3_v3ddwrt_inode_table` is routed
   `legacy-body-failure`/`cross-read-legacy` — **a cross-read prescribed on a body whose
   readers refuse** (the ddwrt family has no validated second reader; 6/7 no-reader). A
   prescribed action the corpus cannot execute is a depth defect: the rule as written cannot be
   followed. The v5 disclosure left it unfixed ("needs a body-variant discriminator that does
   not exist in the scored features").
2. **Registry-census drift:** `tools/round-48/census2.json` froze 42 registered-instrument
   paths; twelve instruments registered by M50-2's fix plus the round-50 C3 instrument make
   **13** registered paths the frozen census does not list (the `meanings.py` census surface
   drifted from the registry).

Claim: land **triage table v6** as `SKILL.md` rule block 27 (dated supersession of block 26's
ddwrt rows; block 26 stays as history) plus the scoring instrument
`tools/round-51/sqfs-triage-v6.py` (ports `tools/round-50-c3/sqfs-triage-v5.py`; freeze-drift
**gating**, routed defect 3), and the re-derived registry census, such that:

- **Predicate** (the same sentence in this file, the instrument docstring, and the receipt
  label): at a REV descending from the R51 freeze, with every frozen path unchanged, running
  `python3 -I -B tools/round-51/sqfs-triage-v6.py --root <LANE> --rev <REV> --freeze <FREEZE>
  --envelopes <DIR> --json-out <OUT>` exits **0** with `pair_mismatches 0`,
  `evaluator_missing 0`, `executability_violations 0`, `census_outside 0`, and a green
  selftest (every committed mutation flips ≥1 pair or ≥1 audit finding, none a no-op, do-nothing
  red); and at the declared base `1aa27369…` the same command exits **1** with
  `executability_violations 1` naming `dmg_Z3_v3ddwrt_inode_table` and `census_outside 13`.
- **The v6 change:** for a reader-backed-family body whose readers ALL refuse, the routed label
  becomes a new row (`legacy-body-unreadable`) whose action prescribes **no cross-read**
  (`preserve-unresolved`); the evaluator implements the same precedence; the executability
  audit (new, frozen) checks every FAILED-body envelope's prescribed action against the family's
  reader census and counts violations — the audit is what makes the before-state measurable
  (v5: 1; v6: 0). The two clean ddwrt no-pad `_ddefault` envelopes keep `clean` (their readers
  succeeded; no route change).
- **Census re-derivation:** a frozen re-derive command (ported from the `meanings.py` census
  surface) enumerates the registered instrument paths from the registry markers at REV and
  reports `census_outside` = registered paths absent from the active census artifact; the
  landing adds `tools/round-51/census3.json` (the re-derived census, provenance recorded) and
  the drift drops 13 → 0. The frozen round-48 census bytes stay untouched; `census3.json`
  records which artifact it supersedes for which surface.
- **Held-out corpus:** the same frozen 126-envelope corpus (`.ufo/waves/round-42/w1/artifacts/
  R42C2ReconLegacy/envelopes/`); same disclosed limit as R50-C3 (depth, not held-out
  generalization). v6 must keep every v5 label unchanged except the one ddwrt FAILED-body pair.
- **Controls (scored with the frozen instrument BEFORE the table lands, receipts committed):**
  do-nothing (the v5 table at base → audit red), junk table (syntactically valid, wrong labels
  → `pair_mismatches > 0`, exit 1), audit-guard-deleted mutant → red, swapped-new-row-action
  mutant → red, census-guard-deleted mutant → red. Kill rule: any of these green at the freeze
  → stop, report as a miss.
- **Counting command:** the predicate command, run twice — before at the declared base
  `1aa27369…`, after at the landing REV. Receipts:
  `.ufo/waves/round-51/l1/scores/c2-{before,after}.json`.
- **Registry:** exactly one `instrument-registry v2` row for the v6 instrument and one for the
  census re-derive tool (if it is a separate file); no other code files land under
  `tools/round-51/` beyond the claims' named files.

## Routed-defect repairs (obligations from the round-50 closure — not claims)

1. **LOG correction entry naming `646d29c9`** (the R50 C1 after-receipts landing commit, never
   cited in LOG.md) — append-only entry this round.
2. **`SHONEN.md` regenerated verbatim from the canonical template**
   (`/home/vgpnk/Projects/kimi-shokunin/templates/mint/SHONEN.md`, `<name>` =
   `kaidoku-shokunin`, the only substitution); the extra note lines and trailing prose move
   into this round's report and a LOG entry.
3. **Freeze-drift gating** in both round-51 instruments (R51-C1 counter, R51-C2 instrument) —
   covered by the claims' predicates and selftests.
4. **`fetch-vendor.py` network-guard selftests:** the repaired copy at
   `tools/round-51/fetch-vendor.py` gains offline selftests proving each guard (https-scheme,
   pinned-host) fails closed: guard deleted → selftest red, guards present → green, shown able
   to fail on fixture clones.
5. **Preventive fleet-root stray control (operator-side, M50-9):** the lane lands a read-only
   sweep helper `tools/round-51/misroot-sweep.sh` (reads `git -C <fleet> status --porcelain`,
   classifies strays by content, never writes) with a fixture-repo selftest; the operator-side
   prevention stays an L0-class note in the report.
6. **Open L0 (carried):** unredacted session cookies in pushed history — `kaidoku | round-50`
   stands; not re-appended.

## Frontier step (inside the claim cap)

- **Sourced claims:** both claims rest on rows opened this round — C1's entry cites the
  unsquashfs/squashfs-tools device-node source row(s) registered this round (the law's
  primary grounding) plus S243/S244/S245/S249; C2's block cites the squashfs-tools `-no-pad`
  / padding source row registered this round. Every new row's `## Gate` record carries URL,
  access date, ≤25-word located quote; rejections stay as rows.
- **Mistakes mined:** appended to `corpus/lessons/round-51.md` `## Mistakes`
  (class · evidence · captured-by · fix), from this round or the round-50 closure/spotcheck;
  a fix counts only once shown able to fail. Found none → paste the sweep.
- **Census:** before = exit 0, 156 rows, 19 W04
  (`.ufo/waves/round-51/l1/sources-census-start.txt`); end must be exit 0 with the round's new
  rows, re-taken at the filing tip.
- **Assimilation:** ONE theme from `merge/kaidoku/` (read-only) serving this round's ground,
  1–3 entries re-grounded in-round with per-entry gates (≥1 admit, ≥1 reject recorded), or the
  report says `Assimilation: none` with the scan receipt. `considerthese/` does not exist in
  this lane (verified 2026-10-30); one report line.

## Round shape

Two v1 waves (policy `ufo-wave-policy.json`, band 32–64 each), round total 64–128:
**w1 build** (~36 seats: the law derivation, the three instrument ports, controls, source
opens, doc drafts, pre-freeze attacks) and **w2 falsify** (dispatched after the landing, ~33
seats: re-run every counting command, re-open every new source row, attack each claim, mutate
each new gate). Attack roles ≥25% round-wide; a few connector seats per wave; the §3 planner
seat is the L1 (the validator rejects `planner`). Waves dispatch through the inline spawn
handoff (`<wave>.ready`), never by the L1 calling `task`; the report files only after
WAVE-DONE for every wave.

## Wave-1 amendment record

The following are proposed amendments from wave-1 pre-freeze attacks
(CritRuleDerive findings F1–F11,
`.ufo/waves/round-51/w1/CritRuleDerive/findings.md`), not a freeze receipt.
No R51 claim freeze or carrier data run was completed; see the final disposition.

- **F1 (critical) — carrier set:** option (b). R51-C1 re-measures the four round-50 carriers;
  `tools/round-50/carriers.json` joins `PRIOR_CARRIER_TABLES`; the four pins enter the round-51
  carrier table's `prior_pins`; the v2 counter honours a frozen `re_scored_pins` allow-list for
  exactly those four; the promotion rests on the 4/4 measurement under the corrected law, not
  on new carrier coverage.
- **F2 (critical) — rule-scoped controls:** CTL-OLD/CTL-NEW evaluate the disposition verdict
  over the committed round-50 **envelopes** (`after.json`) + oracle/non-regular tables; the
  full predicate is not claimed for controls; the v2 counter exposes `--gap-rule`,
  `--receipts`, `--provenance-base`, `--receipt-fresh-base`; the control input is the envelope,
  never the `run.json` harness receipt.
- **F3 (high) — rule shape:** `allowed[char-device] = allowed[block-device] =
  allowed[fifo] = allowed[socket] = []` (a gap on a device row is a violation, fail closed);
  **`required['char-device'] = false` — a deliberate change from round 50's `true`**,
  because the law is that a device row carries no disposition at all: ScribeScorecard's
  probe (`.ufo/waves/round-51/w1/ScribeScorecard/probe-device.out`, run against the four
  committed round-50 envelopes with the unmodified round-50 counter) measured the
  required-true variant red on ALL FOUR carriers (with no admissible gap kind, every
  device row — not just the twelve — is unaccounted) and the required-false variant
  4 of 4; the law sentence updated to match.
- **F4 (high) — mutation set:** M1 all-thirteen whitelist (red via the new frozen rule-shape
  clause `law_shape_ok`), M2 fourteenth-device census fixture (green under the law, red under
  any whitelist), M3/M4 the old mutants retained as regression arms.
- **F5 (high) — law width + cross-claim:** the law is stated to the measured width (char-device
  rows measured; fifo/socket/block generalisation marked, unexercised); the grounding is the
  measurement; the reader source grounds the census; R51-C2's block 27 supersedes/scopes the
  SKILL.md *"`symlink` and `special` both count"* phrasing so the two claims do not contradict.
- **F6 (high) — second miss cause:** the before-state records `g7581`'s `projection_ok` false
  (REA `execution_failure`, ENOENT readlink, `retryable: false`); the v2 counter treats an
  ENOENT-on-extraction-tree `execution_failure` as retryable (≤3 attempts, recorded).
- **F7 (medium) — census re-derivation:** new frozen clause `census_rederived_ok` (the
  non-regular census is re-derived at score time and compared in both directions; exit 2
  `oracle_env_error` when the reader cannot run).
- **F8 (medium) — reached-scope:** the law claims only entries the extractor reached; the v2
  receipt records the `depth-limited` gap's `input_path`/`continuation_id`
  (`depth_gap_recorded`).
- **F9 (medium) — CTL-OLD relabeled** the reproducibility control; a 4-of-4 CTL-OLD stops the
  round with "the round-50 miss is not reproducible", not "the counter or target is wrong".
- **F10 (medium) — rule labels:** the v2 parser accepts `{R50-C1, R51-C1}`; the frozen round-51
  rule carries `R51-C1`.
- **F11 (low) — base lines:** the round base, claims-draft commit and wave-1 dispatch commit
  are named in the header; the C2 before-arm base is the claims-draft commit `f04b51dd…`.

## Final disposition — provider-recovery honest stop

The orchestrator's latest boundary supersedes the two-wave execution plan:
“finish current round using already-submitted wave identities only; no additional
waves or provider-replacement seats”; unmet required work must be explicitly
unverified. Wave r51-w1 settled 36/36 (WAVE-DONE received); no w2 was launched.
The 64-seat floor and independent falsify wave are consequently unmet.

Both original claims remain **unverified, not admitted**. This is not a smaller
replacement claim: C1 did not freeze/measure the fresh four-carrier predicate
or promote Core; C2 did not land/score triage v6 or its executability audit.
The independent census diagnostic alone does not satisfy C2's conjunction.
No capability is added and owned-axis scores stay unchanged.

Pre-freeze hypotheses above are not admitted doctrine. Source opening falsified
the shared char-device/FIFO/socket explanation: S250's FIFO/socket branches are
not root-gated. “no-pad” is descriptive prose; S251's actual writer flag is
`-nopad`. CritTriV6 also disproved the assertion that clean DD-WRT extraction
means its independent readers succeeded. CritCounterV2 F13–F15 identify
uncompleted controls/binding obligations; none is silently marked repaired.
The ENOENT diagnostic alone does not prove a retry-safe environmental race;
no new retry policy is admitted.

The C1 counter/harness and incomplete v6/fetch/misroot-helper drafts are preserved
under `.ufo/waves/round-51/`, not shipped as working production instruments.
Only the completed registry-inventory diagnostic `tools/round-51/census3.py`
and its census are delivered, alongside source/documentary corrections.
`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` states NOT promoted
despite occupying the originally declared filename.
