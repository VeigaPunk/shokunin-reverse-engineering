# R51-C1 pre-freeze attack — findings (CritRuleDerive, round 51 wave 1)

Seat: `CritRuleDerive` (critic, leaf member — no dispatch). Scope: attack the R51-C1 rule
design **before** it is built: the device-accounting law, the v2 gap rule, the v2 counter's
rule-sensitive clauses, the pre-freeze controls, and the mutation set.

Read: `plans/round-51-claims.md` (R51-C1), `tools/round-50/gap-rule.json`,
`tools/round-50/c1-counter.py` (disposition check, `gap_rule_model`, `prior_pins`,
`carrier_fresh_ok`, `run_provenance_ok`, `receipt_fresh`), the four
`tools/round-50/oracle/*.nonregular.tsv`, the four committed envelopes
`corpus/evidence/round-50/c1/<id>/after.json` + `run.json`, and the committed round-50 miss
receipt `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`.

Verification receipts for every command quoted below: `receipts.txt` (same directory).
Nothing was written outside this seat directory; no REA run; no download; no git mutation.

Severity scale: **critical** = the claim as frozen cannot pass / must not be asserted;
**high** = the claim as written is false or unfalsifiable as stated; **medium** = a disclosed
limit or a clause that will bite the L1; **low** = hygiene.

---

## F1 — CRITICAL — the four frozen carriers are pins a previous C1 freeze already scored: `carrier_fresh_ok` makes `carriers_matched == 4` unreachable, or forces a silent weakening of the anti-replay clause.

**Evidence.**

* `tools/round-50/c1-counter.py:435` puts `carrier_fresh_ok` in `CLAUSES`; `:2250` computes it
  as `pin is not None and pin not in prior`; `:1596-1618` (`prior_pins`) builds `prior` from
  three sources read **at the freeze commit**: the carrier table's own `prior_pins` list,
  `PRIOR_CARRIER_TABLES = ('.ufo/waves/round-41/c1/carriers.json', 'tools/round-49/carriers.json')`,
  and `PRIOR_PIN_CANDIDATES = ('tools/round-50/prior-pins.json', 'tools/round-49/prior-pins.json',
  'tools/round-42/prior-pins.json')`. `tools/round-50/prior-pins.json` **does not exist**
  (verified). The clause is documented at `:119-122`: *"the pin is not one a previous C1 freeze
  already scored"*, with the selftest case at `:4140` *"relabelled previous-round pins
  (prior_pins) → want_fail='carrier_fresh_ok'"*.
* The discipline is documented in the lane itself: `tools/round-42/prior-pins.json` — *"frozen
  union of the C1 carrier pins of rounds 38-41"* (18 pins, rounds {38,39,40,41}). Every C1
  freeze has scored carriers no earlier C1 freeze scored: round-41 scored V3/V4/L3/L4
  (`.ufo/waves/round-41/c1/carriers.json`), round-49 scored the lane-built v1/v2 fixtures,
  round-50 scored four vendor members — and the round-50 miss receipt's own
  `prior_pin_sources` are exactly `['.ufo/waves/round-41/c1/carriers.json',
  'tools/round-49/carriers.json', 'tools/round-42/prior-pins.json']`, with the four round-50
  pins absent from all three (hence `carrier_fresh_ok: true` for all four at the round-50 freeze).
* R51-C1 as written re-runs **the same four carriers** ("re-run the four pinned carriers",
  "the four chain-pinned vendor carriers"): the four pins are exactly the round-50 pins.

**Consequence.** The round-51 freeze is the fourth C1 freeze to see these pins. The v2 counter,
ported honestly, must add `tools/round-50/carriers.json` to `PRIOR_CARRIER_TABLES` (the same
rule the round-50 counter applied to rounds 41 and 49). Then `carrier_fresh_ok` is **false for
all four carriers**, `matched` is false for all four, and `carriers_matched == 0` — the claim's
predicate is unreachable. The other way to a green number is to *not* add the round-50 table
and to keep the round-50 pins out of `prior_pins`: that is precisely the weakening the clause
exists to prevent (a relabelled previous-round carrier sold as new coverage), it would be
invisible in the receipt unless the reader checks `prior_pin_sources`, and the claims' own
sentence *"the class distinction is a property of the carriers' device census, not of the rule"*
does not cover it.

**Exact text fix demanded** (claims file, R51-C1, "Claim:" bullet — one of the two):

> **Carrier set (decided at this freeze).** R51-C1 freezes the carrier set explicitly as
> either **(a) four new carrier pins** — LE AVM members whose sha256 is in no earlier C1
> freeze's pin union (`tools/round-42/prior-pins.json` + `tools/round-50/carriers.json`), with
> their oracle and non-regular tables derived and committed before the freeze; or **(b) the
> four round-50 carriers, re-scored** — in which case `tools/round-50/carriers.json` is added
> to the v2 counter's `PRIOR_CARRIER_TABLES`, the four pins are listed in the round-51
> carrier table's `prior_pins`, and the v2 counter honours an explicit, named
> `re_scored_pins` allow-list for exactly those four. Under (b) the claims state verbatim:
> *"R51-C1 adds no new carrier; it re-measures the four carriers the round-50 freeze already
> scored, under the corrected device-accounting law. The anti-replay clause is waived for
> these four pins by an explicit list, and the Frontier → Core promotion of LE AVM members
> (`hsqs`) rests on the completed 4/4 measurement, not on new carrier coverage."*

Under (a) the promotion's coverage reading is unaffected; under (b) the claims must not let
"re-run the four pinned carriers" stand as if it were new coverage.

---

## F2 — CRITICAL — the pre-freeze controls cannot produce the numbers the claims demand: three per-carrier clauses are pinned to round-51 constants, the control input file is the wrong file, and the carrier bytes are gone.

**Evidence.**

* `run_provenance_ok` → `provenance_ok(output_directory)` requires
  `parameters.output_directory.startswith(PROV_BASE)`; the v2 counter's `PROV_BASE` is
  `/fast/scratch/hyaku/kaidoku-r51/` (the claims' own `prov_base`), while every committed
  round-50 envelope carries `parameters.output_directory =
  /fast/scratch/hyaku/kaidoku-r50/c1-run.<rand>/extract` (verified on `g7581` and `c6430`;
  `run.json` `extraction_root` agrees). → the clause is **false for all four** under the v2
  counter, so `carriers_matched` is 0 regardless of the rule.
* `receipt_fresh` (`:2315-2317`) requires every commit that adds the receipt path to be a
  strict descendant of `--freeze`. The round-50 envelopes were added at **`646d29c9`**
  ("round-50: C1 after-receipts as named files"), which is *before* the round-51 freeze and
  *after* the round-50 freeze `435d41fd` (the envelope is **absent** at `435d41fd`, verified).
  → `receipt_fresh` is **false for all four** under the round-51 freeze.
* `carrier_present`, `carrier_pin_ok`, `oracle_rederived_ok` and `projection_ok` need the
  carrier bytes. The round-50 cache `/fast/scratch/hyaku/kaidoku-r50/carrier-cache` **no longer
  exists** (verified: "No such file or directory"); `projection_ok` additionally demands a
  live REA rerun of the bytes — forbidden in this wave ("No REA runs this wave") and impossible
  without the bytes.
* The claims name the control input as `corpus/evidence/round-50/c1/<id>/run.json`. That file
  is the **harness** receipt (`schema: kaidoku-r50-c1-run-v1`: argv, timings, carrier
  superblock), not the REA envelope. The counter's `receipt_present` / `evidence_envelope_ok`
  read the envelope `after.json` (`run_provenance_ok`, `parameters_ok`, `evidence_id_ok`,
  `gaps_ok` are all computed from the envelope). Feeding `run.json` fails
  `evidence_envelope_ok` (it carries `exit`/`argv`, not `normalized_result`).

**Consequence.** CTL-NEW ("the new law-derived rule over the same receipts reports
`carriers_matched 4`, exit 0") and CTL-OLD ("the old round-50 gap rule over the same receipts
reports `carriers_matched 2`, exit 1") are **not producible** by the frozen instruments as
specified: both would report 0/4 (four clauses red on the round-50 receipts), not 4/4 and 2/4.
The kill rule "CTL-NEW red → stop" would therefore fire on the *correct* rule and abort the
round for the wrong reason.

**Exact text fix demanded** (claims file, R51-C1, "Pre-freeze controls" bullet — replace the
CTL-NEW / CTL-OLD sentences):

> The two rule controls are **rule-scoped**, not predicate-scoped: they evaluate the frozen
> disposition verdict (`gaps_ok` ∧ `nonregular_unpublished_ok`) of a named gap rule over the
> committed round-50 **envelopes** `corpus/evidence/round-50/c1/<id>/after.json` and the
> committed round-50 oracle / non-regular tables. CTL-OLD (the round-50 rule) → 2 of 4
> dispositions (the Cable class passes, the FRITZ!Box class fails `gaps_ok`), exit 1;
> CTL-NEW (the round-51 law rule) → 4 of 4 dispositions, exit 0. The full predicate
> (`carriers_matched == 4`, every clause) is **not** claimed for the controls: the committed
> round-50 receipts fail `run_provenance_ok` (they carry the round-50 provenance prefix),
> `receipt_fresh` (added at `646d29c9`, before the round-51 freeze) and every byte-dependent
> clause (`carrier_present`, `carrier_pin_ok`, `oracle_rederived_ok`, `projection_ok` — the
> round-50 carrier cache no longer exists, and a rerun is forbidden before the freeze). The
> v2 counter therefore exposes the round-sensitive constants as explicit flags
> (`--gap-rule`, `--receipts`, `--provenance-base`, `--receipt-fresh-base`) and the control
> driver pins the round-50 values; the rule-scoped verdict is recomputed by the v2 counter from
> the frozen receipt bytes and the frozen rule.

---

## F3 — HIGH — the law's sentence and the rule the claims describe are different statements; keeping `allowed["char-device"] -> ["unpublished-entry"]` with `required=false` is incoherent.

**Evidence.**

* The law (claims, R51-C1): *"it creates no device nodes, fifos or sockets — an unprivileged
  extraction cannot `mknod` — and it emits **no gap record for them**: a char-device/fifo/socket
  oracle entry is expected to carry **no disposition at all**."*
* The rule the claims describe: `required['char-device'] = false` with
  `allowed['char-device'] = ['unpublished-entry']` retained. But `disposition_check`
  (`tools/round-50/c1-counter.py:1458+`) evaluates the **gap loop unconditionally**, for every
  gap, regardless of `required`: a gap whose path resolves to exactly one census row is
  accepted iff its kind is in `allowed[that row's kind]`. With
  `allowed['char-device'] = ['unpublished-entry']` a device row that **does** carry an
  `unpublished-entry` gap is accepted. The rule therefore says *"a device row may carry an
  `unpublished-entry` gap"*; the law says *"no gap record at all"*.
* Answer to the seat's question ("does dropping `required` silently weaken future coverage?"):
  **for gaps, no** — a gap is never bypassed: it must resolve to exactly one non-regular row
  and its kind must be allowed for that row's kind; **for rows, yes, and that is the point** —
  with `required=false` a device row that is neither gapped, nor published, nor removed is
  silently acceptable, which is exactly the law's claim. The hole is that the *rule* does not
  forbid the very state the law forbids; only the *text* forbids it.

**Exact text fix demanded** (the round-51 rule file and the claims' law sentence):

* rule: `"allowed": {"symlink": ["unpublished-entry"], "char-device": [], "block-device": [],
  "fifo": [], "socket": [], "dir": []}` — empty lists for the device kinds, so that **any**
  extraction gap landing on a device / fifo / socket / block row is a hard `gaps_ok` failure
  (the round-50 rule already uses the legal `"block-device": []` form, and `gap_rule_ok`
  still holds: every kind that appears in a frozen non-regular table — `symlink`, `dir`,
  `char-device` — is a key of `allowed`, an empty list is a legal value);
  `"required": {"symlink": true, "char-device": false, "block-device": false, "fifo": false,
  "socket": false, "dir": false}` unchanged from round 50.
* claims: replace *"and it emits **no gap record for them**: a char-device/fifo/socket oracle
  entry is expected to carry **no disposition at all**"* with

  > it emits **no gap record for them**: a char-device/fifo/socket oracle entry carries **no
  > disposition at all** — and, because the law is that no gap record exists for such an entry,
  > the frozen rule admits **no** gap kind for those kinds (`allowed` for a device kind is the
  > empty list), so a gap landing on a device row is a violation of the law, not a tolerated
  > state. A future extractor that starts emitting a device gap turns the rule **red**
  > (fail closed), which is the intended behaviour and not a false green.

---

## F4 — HIGH — the planned mutation set cannot distinguish "the law" from a per-detail whitelist: the decisive mutant is missing and would pass the battery.

**Evidence.**

* The claims' mutation list: *"requiring char-device dispositions (`required.char-device=true`)
  and whitelisting only `247:0` reproduces the round-50 miss (red); whitelisting a strict
  subset of the thirteen stays red (the M50 partial-widening trap, `MutC1Counter` F10)."*
  Both of those mutants are **red under the law rule too** (with `required.char-device=true`
  the twelve unlisted device rows have no disposition). Neither mutant therefore tests the
  property the claim asserts.
* The mutant that matters is the one M50-7 named: an **all-thirteen whitelist** —
  `required.char-device=true` with `removed.silent.char-device = [136:0..7, 230:0, 247:0,
  3:0..2]`. Over the four measured carriers it is **green** (every device row's detail is in
  the list: verified — `dev/led 247:0`, `dev/pts/0-7 136:0-7`, `dev/tiatm 230:0`,
  `dev/ttyp0-2 3:0-2` in `g7581.nonregular.tsv` and `g7582.nonregular.tsv`; `dev/led 247:0` in
  `c6430`/`c6490`). So the battery as planned **passes a rule that is precisely the smuggled
  per-detail whitelisting** the claims say the v2 rule is not.
* The claims' sentence *"the law, not a detail whitelist, is what the v2 rule encodes; the class
  distinction is a property of the carriers' device census, not of the rule"* is therefore
  **unfalsifiable at the freeze** under the planned battery: over the four carriers the law rule
  and the thirteen-detail whitelist are extensionally identical, and the only difference (a
  fourteenth device) is not in the corpus.

**Exact text fix demanded** (claims, R51-C1, "Rule mutations" paragraph — replace):

> The rule mutation set is frozen with the two mutants that actually separate the law from a
> detail whitelist:
> **(M1) all-thirteen whitelist** — `required.char-device=true` with
> `removed.silent.char-device` naming all thirteen observed details — **must be RED**, and it is
> red by a frozen **rule-shape** clause in the v2 counter (`law_shape_ok`: the frozen rule must
> list no char-device / fifo / socket / block detail under `removed.silent`, and `allowed` for
> those kinds must be the empty list). A rule-shape clause is required because no carrier in
> the corpus carries a fourteenth device, so the difference between the law and a whitelist is
> otherwise unobservable in the data.
> **(M2) a census with an unlisted device** — a fixture carrier whose non-regular table carries
> a device row whose detail is not in the thirteen (e.g. `dev/ttyS0 4:64`) — **must be GREEN
> under the law rule and RED under any detail whitelist**. The v1 counter's fixture builder
> already supports this (`nonreg_over={'g7582': ...}`, `tools/round-50/c1-counter.py:4031`),
> so the v2 control driver plants it.
> The existing two mutants (round-50 miss reproduced; strict-subset whitelist) are retained as
> regression arms.

---

## F5 — HIGH — the law's scope is stated wider than the measurement, and the wider part is contradicted by the lane's own SKILL.md — which R51-C2 rewrites in the same freeze.

**Evidence (measured over the four committed envelopes).**

* The non-regular census of the four carriers contains **char-devices only**: `c6430` 1,
  `c6490` 1, `g7581` 13, `g7582` 13 = 28 device rows. There is **no fifo, socket or
  block-device row anywhere** in the four tables.
* In every envelope, **none** of the 28 device rows carries a gap and none appears in
  `unpublished_entries`: gap kinds are `unpublished-entry` (567 / 612 / 636 / 636 — one per
  symlink) plus one structural `depth-limited`; `unpublished_entries` kinds are `symlink` only
  (567 / 612 / 636 / 636). No gap lands on a device row (checked by resolving every gap's
  `relative_path` against the census).
* The lane's own SKILL.md says the **opposite**: the triage rows (rule block 26 / table v5,
  "in-tree-symlink-metadata" and "mixed-symlinks") read *"every non-file entry resolved inside
  the extraction root and is kept as metadata, one `unpublished-entry` gap per entry … `symlink`
  and `special` both count (S119 FirmwarePublication.js:301-307; firmwareAnalysis.js:139)"* —
  i.e. device/special entries **do** get a gap. R51-C2 lands triage table v6 (a dated
  supersession of block 26) in the **same freeze**, so the two claims would land contradictory
  statements about device nodes.
* The claims' grounding is also on the wrong side: *"C1's entry cites the unsquashfs/squashfs-tools
  device-node source row(s) registered this round (the law's primary grounding)"*. The **reader**
  source explains why the independent *oracle* sees device nodes; it does not explain why the
  *extractor* emits no gap. The extractor-side evidence is the measurement above (28/28 rows).

**Exact text fix demanded** (claims, R51-C1, law paragraph):

> The law is stated to the width of the measurement and generalised only where it is marked:
> *"For the four measured LE AVM carriers, every char-device row of the independent census
> carries no extraction gap and no published path (28 of 28 rows). We generalise this to the
> device-node kinds (char/block device, fifo, socket) on the ground that an unprivileged
> extraction cannot create such nodes — a generalisation the corpus does not yet exercise: no
> fifo, socket or block-device row exists in any measured carrier. The law's primary grounding
> is the measurement (the four committed envelopes); the unsquashfs/squashfs-tools source rows
> ground the **census**, not the extractor's silence."*
> **Cross-claim obligation:** R51-C2's v6 table must not contradict this law. The SKILL.md
> phrase *"`symlink` and `special` both count"* is superseded (or scoped to the kinds actually
> observed) in block 27, and the correction is listed in this round's `## Wave-1 amendment
> record`.

---

## F6 — HIGH — the round-50 miss had a **second, independent cause** on g7581 (`projection_ok`), which R51-C1 does not mention and the re-freeze does not repair.

**Evidence.** The committed miss receipt
`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`: `carriers_matched 2`, `exit_code 1`;
`c6430` and `c6490` matched (`gaps_ok true`); **`g7581`: `gaps_ok false` *and*
`projection_ok false`**, with `projection_error` = REA `execution_failure`, `retryable: false`,
`diagnostics.reason` = *"ENOENT: no such file or directory, readlink
'…/firmware.bin_extract/usr/www.myfritz/avme/cgi-bin/luacgi'"*; `g7582`: `gaps_ok false`,
`projection_ok true`.

**Consequence.** The claims' narrative ("the round-50 measurement published every frozen-oracle
regular file on all four carriers but the frozen gap rule failed `gaps_ok` on the two
FRITZ!Box-class carriers") and the "Before (measured, already committed)" bullet attribute the
miss to the gap rule alone. The v1 counter retries **only** `provider_timeout`
(`MAX_REA_ATTEMPTS = 3`); a `retryable: false` `execution_failure` is a hard red. If the same
ENOENT readlink recurs for g7581 in the round-51 data run, `projection_ok` is false and the
claim misses for a cause the claim does not contain — and the claims' own kill rule ("honest
stop, no narrowing") turns that into a miss of a claim that was never about the projection.

**Exact text fix demanded** (claims, R51-C1, "Before (measured, already committed)" bullet —
append):

> The round-50 miss on `g7581` had **two** independent causes, both recorded in
> `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`: the frozen gap rule's `gaps_ok`
> false (the twelve unaccounted device rows) **and** `projection_ok` false (the counter's own
> REA rerun of the carrier bytes failed with `execution_failure`, `retryable: false`, ENOENT on
> `readlink …/usr/www.myfritz/avme/cgi-bin/luacgi`); `g7582` failed only `gaps_ok`. The
> re-freeze repairs the first cause. The second cause is a REA/unblob filesystem race and is
> handled by treating a REA `execution_failure` whose diagnostic is an ENOENT on a path inside
> the extraction tree as a **retryable environment error** (as `provider_timeout` already is),
> with the attempt count and the failing diagnostic recorded in the receipt; a carrier whose
> rerun fails with any other error is a red.

---

## F7 — MEDIUM — the non-regular census — the law's entire scope — is frozen but never re-derived at score time.

**Evidence.** The counter's own docstring (`tools/round-50/c1-counter.py`, `oracle_rederived_ok`):
*"the counter runs `/usr/bin/unsquashfs` … and requires the set of regular files `(rel, sha256,
size)` to EQUAL the frozen oracle table in both directions … **Non-regular entries are not
re-derived** (an unprivileged extraction cannot make device nodes)."* Only the regular-file
oracle is re-derived. The lane already had the stronger instrument: the SKILL.md registry row
for `tools/round-41/c1-extra.py` — *"oracle_rederived re-runs the frozen `sqfs-list.py` reader on
every pinned carrier and reproduces `oracle.tsv` **and `nonregular.tsv`** as row sets"*.

**Consequence.** A device node missing from the frozen census is invisible to every clause:
`gaps_ok` has no row to fail on, `nonregular_unpublished_ok` has no path to compare, and the
*census itself* is never checked against the carrier bytes. Under F1(b) (re-scored carriers) the
census is a committed round-50 artifact and this limit is a disclosed one; under F1(a) (new
carriers) the census is brand new and unverified, which is where it bites hardest — the law
would be stated over a census nobody re-derived.

**Exact text fix demanded** (claims, R51-C1, add to the predicate/limit list):

> **Census re-derivation.** The v2 counter re-derives the **non-regular** census at score time
> (the frozen reader of the round-41 instrument or `unsquashfs -ll`), compares it with the
> frozen `*.nonregular.tsv` in both directions, and fails closed (exit 2, `oracle_env_error`)
> when the reader cannot run — the round-50 counter re-derived only the regular-file oracle, so
> the device census on which the whole law rests was frozen but never verified against the
> carrier bytes. If the v2 counter keeps the round-50 behaviour instead, the claims carry the
> limit verbatim: *"the device census is frozen, not re-derived at score time; a device node
> absent from the frozen table is invisible to every clause."*

---

## F8 — MEDIUM — the law cannot distinguish "the extractor creates no device nodes" from "the extractor never reached the device's directory".

**Evidence.** `tools/round-50/gap-rule.json` allows one path-less structural gap per carrier
(`"structural": {"depth-limited": 1, "unknown-chunk-handler": 0}`). The `depth-limited` gap in
the committed envelopes carries `"relative_path": null` and `"input_path":
"$output/firmware.bin_extract"` — it does **not** name the directory that was not descended into
(verified on g7581 and g7582; the continuation text only says *"descend into this path"*).
The census shows the device rows under `dev/pts/` have **no regular-file sibling** (`dev/pts` is
a `dir` row; only `dev/pts/0..7` are char-devices), so an extraction truncated above `dev/pts/`
would still satisfy `oracle_hits_ok` (no oracle regular file is missed), still satisfy the law
rule (device rows need no disposition), and still satisfy `nonregular_unpublished_ok` — while
eight device rows were never visited at all.

**Exact text fix demanded** (claims, R51-C1, law paragraph — append):

> The law is a statement about the entries the extractor **reached**: the receipts do not name
> the path a `depth-limited` gap stopped at (`relative_path` is null), and a device-only subtree
> (e.g. `dev/pts/`, which holds no regular file) that was never descended into cannot be
> distinguished from one that was reached and correctly produced no gap. The v2 counter records
> the `depth-limited` gap's `input_path` and `continuation_id` in the receipt so that this limit
> is visible in the evidence; the claim does not assert more than "reached".

---

## F9 — MEDIUM — CTL-OLD's stated inference is false, and CTL-OLD is a reproducibility control, not a do-nothing control.

**Evidence.** Claims: *"CTL-OLD … reports `carriers_matched 2`, exit 1 — the target is NOT
reachable without the claimed re-freeze; if it reported 4, the counter or target is wrong and
nothing proceeds."* `carriers_matched` is the conjunction of the per-carrier clauses and
`gaps_ok` is a function of the rule and the committed receipt alone; the receipts are already
committed. A permissive old rule (e.g. one with `required.char-device=false`) would report 4
while both the counter and the target are right — CTL-OLD reporting 4 would prove only that the
old rule happened to be permissive. And the claims' own list has a *separate* do-nothing control
(CTL-DN, a do-nothing fixture tree); CTL-OLD is the before-arm reproduction.

**Exact text fix demanded** (claims, R51-C1, CTL-OLD bullet — replace the inference clause):

> CTL-OLD is the **reproducibility control** for the committed round-50 miss: the round-50 gap
> rule over the same committed envelopes yields 2 of 4 dispositions (the Cable class passes,
> the FRITZ!Box class fails `gaps_ok`) and exit 1, reproducing
> `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`. If it yielded 4, the round-50 miss is
> not reproducible and the round-50 closure's diagnosis is wrong — stop and report that, not
> "the counter or target is wrong". The do-nothing control (CTL-DN) is the separate arm that
> shows the counter cannot be green on an empty tree.

---

## F10 — MEDIUM — the v2 rule's `claim` label is rejected by the v2 counter's own rule parser unless the parser is widened — and the CTL-OLD arm needs the *old* label.

**Evidence.** `gap_rule_model` (`tools/round-50/c1-counter.py:771+`): `claim = doc.get('claim')`;
`if claim is not None and claim != 'R50-C1': probs.append("claim %r != R50-C1")` → the rule
fails `gap_rule_ok` → `frozen_tables_valid`/`gap_rule_ok` false. The round-51 rule will carry
`"claim": "R51-C1"`; the CTL-OLD arm carries `"claim": "R50-C1"`. With the ported parser, one of
the two arms is rejected before it is measured.

**Exact text fix demanded** (v2 counter + claims):

> The v2 rule parser accepts the claim labels `{"R50-C1", "R51-C1"}` (the CTL-OLD arm scores
> the round-50 rule, the CTL-NEW arm the round-51 rule) and the frozen round-51 rule's own
> `claim` label is named in the claims, because the label is part of the frozen rule's identity
> and is compared, not ignored.

---

## F11 — LOW — the claims' `Base` line is stale, and the C2 before-arm base is named inconsistently.

**Evidence.** The claims open with *"Base `1aa273694f4409d3432fbcd73e83a33bee0dd8e9` (lane `main`
tip, pushed …)"* — that commit is `1aa27369 round-50 verifier spot-check`; the tip at round
start was `f04b51dd round-51: claims draft` and the lane HEAD is now `39f41d4f round-51: wave-1
spec`. R51-C2's predicate names *"the declared base `1aa27369…`"* as the before-arm base.

**Fix.** Name the round-51 base explicitly as the claims-draft commit `f04b51dd` (or the
wave-1 dispatch commit) in the header, and use the same string in the C2 before-arm clause, so
the before-arm is not anchored to a commit that predates the claims file.

---

## Summary table

| # | severity | one line |
|---|---|---|
| F1 | critical | the four frozen carriers are prior-scored pins → `carrier_fresh_ok` makes `carriers_matched == 4` unreachable, or the anti-replay clause must be waived explicitly |
| F2 | critical | CTL-OLD / CTL-NEW cannot produce 2/4 and 4/4: `run_provenance_ok`, `receipt_fresh` and every byte clause are red on the round-50 receipts, the carrier cache is gone, and the control names the wrong input file (`run.json`, not `after.json`) |
| F3 | high | the law says "no gap record for device rows", the rule as described says "a device row may carry an `unpublished-entry` gap" → `allowed[device kind]` must be the empty list |
| F4 | high | the planned mutants cannot separate the law from a whitelist; the all-thirteen whitelist mutant is green and passes the battery → add a rule-shape clause and a fourteenth-device census mutant |
| F5 | high | the law's fifo/socket scope is unmeasured and contradicts SKILL.md's "`special` both count" — which C2 rewrites in the same freeze; the law's grounding is the reader, not the extractor |
| F6 | high | g7581's round-50 miss had a second cause (`projection_ok` false, REA ENOENT readlink, `retryable: false`) that the re-freeze does not repair and the claim does not mention |
| F7 | medium | the device census is never re-derived at score time (the round-41 instrument re-derived both tables) → re-derive it or disclose the limit |
| F8 | medium | a `depth-limited` gap names no path, so a never-visited device-only subtree is a false green → narrow the law to "reached" and record the gap's `input_path` |
| F9 | medium | CTL-OLD's "if it reported 4, the counter or target is wrong" is a false inference → re-label it the reproducibility control |
| F10 | medium | the rule parser rejects any label but `R50-C1` → the v2 parser must accept both labels |
| F11 | low | the claims' `Base` line is stale; the C2 before-arm base must match |

**Not run** (deliberately, this wave): any REA run, any vendor download, any `npx rea-agents`
invocation, any git mutation, any write into the lane tree outside
`.ufo/waves/round-51/w1/CritRuleDerive/`. No counter was executed: the round-51 instruments do
not exist yet, so every claim above is derived from the **committed** round-50 bytes
(`gap-rule.json`, `c1-counter.py`, the four census tables, the four envelopes, the miss receipt),
which is what the pre-freeze attack is for.
