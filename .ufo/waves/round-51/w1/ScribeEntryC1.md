# ScribeEntryC1 — R51-C1 knowledge entry draft (kaidoku round 51, attempt 1, wave 1)

Seat artifacts: `.ufo/waves/round-51/w1/ScribeEntryC1/` — `entry.md` (the draft knowledge entry, 38 473 B, sha256 `1ea47d4368b0d526809a37f66aadc2bbfda9ce2b7b3b028febc4b826df1a66cc`), `receipts.tsv` (the receipt ledger), and five read-only probes (`law-device-disposition.py`, `rule-scope-offline.py`, `rule-variants-offline.py`, `failclosed-probe.py`, `entry-binding-check.py`, `receipts-collect.py`). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab` (claims-draft commit); lane HEAD at drafting `39f41d4f15a87689a41c16c5c17ed885fbfb7da3`. Scratch `/fast/scratch/hyaku/kaidoku-r51/w1-ScribeEntryC1`, removed after the receipts were copied into the seat directory. Times UTC 2026-10-30 05:04–05:20Z.

**Verdict: the entry draft is complete and internally consistent, and it carries 28 explicit `<PLACEHOLDER>` markers for the L1 to fill from receipts. Every number in it is either a measured triple (`<number> — <command> <date>`) or a placeholder; nothing is invented.** Three findings below are blockers for the freeze, and one of them would have made the frozen rule silently wrong.

---

## F1 (BLOCKER) — the wave-1 derivation draft's rule shape is **not fail-closed**; the claims' F3 amendment fixes it, and the draft does not

`ExecRuleDerive/gap-rule-v2.json` (the wave-1 derivation draft) keeps `"char-device": ["unpublished-entry"]` in `allowed`. That makes a device gap **tolerated**, not a violation — the opposite of the amended law sentence ("the frozen rule admits **no** gap kind for those kinds … a gap landing on a device row is a violation of the law, not a tolerated state").

Measured with the counter's own `disposition_check` on the committed `g7581` envelope, with one synthetic `unpublished-entry` gap injected on `dev/led` in the real gap shape (`relative_path` = chunk-root-prefixed, `input_path` = `$output/…`):

| rule shape | clean envelope | with an injected device gap |
|---|---|---|
| round-50 frozen rule | red (twelve undisposed rows) | red |
| **F3 shape** (`allowed` for device kinds = `[]`, `required.char-device` = false, `removed.silent` empty) | **green** | **red** — "gap kind 'unpublished-entry' not allowed for 'char-device' entry 'dev/led' (allowed [])" |
| wave-1 draft `ExecRuleDerive/gap-rule-v2.json` (`allowed.char-device` = `["unpublished-entry"]`) | green | **green** — 638 gaps, the device gap accepted |

Receipt `failclosed-probe`, 2026-10-30, exit 0, stdout sha256 `6abe18f3e98c2d94…`; command `python3 -I -B .ufo/waves/round-51/w1/ScribeEntryC1/failclosed-probe.py --lane .`.

**Action for the L1:** freeze `tools/round-51/gap-rule.json` with `allowed[char-device] = allowed[block-device] = allowed[fifo] = allowed[socket] = []`, `required.char-device = false`, `removed.silent = {}` — the F3 shape, **not** the wave-1 draft's file. If the draft's `allowed` list is carried into the freeze, the frozen rule will accept a device gap and the law's fail-closed clause is void.

## F2 (BLOCKER) — the claims' F3 amendment is internally contradictory: "`required` unchanged from round 50" makes the law rule red on **all four** carriers

F3 reads: "`allowed[char-device] = allowed[block-device] = allowed[fifo] = allowed[socket] = []` (a gap on a device row is a violation, fail closed); **`required` unchanged from round 50**". The round-50 rule has `required.char-device = true` and a silent list of `["247:0"]`. With `allowed` emptied but `required.char-device` left `true` and `removed.silent` empty, every device row is a required row with no allowed disposition — red everywhere.

Measured over the committed round-50 envelopes (receipt `rule-shape-variants-offline`, 2026-10-30, exit 0, stdout sha256 `bb3ba036cc5c2f21…`; command `python3 -I -B .ufo/waves/round-51/w1/ScribeEntryC1/rule-variants-offline.py --lane .`):

| rule variant | 13-row census | 14-row census |
|---|---|---|
| round-50 frozen rule | **2 of 4** | 2 of 4 |
| F3 shape (`allowed` device kinds = `[]`, `required.char-device` = **false**, no silent list) | **4 of 4** | **4 of 4** |
| F3 shape but `required.char-device` = **true** (the literal F3 text) | **0 of 4** | 0 of 4 |
| all-thirteen whitelist (`required` true, silent = all thirteen) | 4 of 4 | **3 of 4** |
| strict subset whitelist (twelve, `230:0` omitted) | **2 of 4** | 2 of 4 |

**Action for the L1:** amend F3 in the freeze commit to say "`required.char-device` **false** (the device kinds are exempt from the required-disposition check), `removed.silent` empty" — not "unchanged from round 50". As written, F3 freezes a rule that matches 0 of 4 and the claim is missed as frozen.

## F3 (BLOCKER) — the drafted v2 counter does not accept the claims' own predicate command, and is missing every clause the amended predicate names

The claims' predicate (R51-C1) is `python3 -I -B tools/round-51/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --receipts corpus/evidence/round-51/c1 --json-out <OUT>`. Run against the wave-1 v2 counter draft (`ExecCounterV2/c1-counter.py`), it **exits 2** with `error: unrecognized arguments: --receipts corpus/evidence/round-51/c1` (receipt `predicate-cli-vs-draft`, 2026-10-30, exit 2, stdout sha256 `e3b0c44298fc1c14…` — empty; the error is on stderr).

A literal grep of the draft for the amended predicate's surfaces gives **zero hits each** for `--receipts`, `--gap-rule`, `--provenance-base`, `--receipt-fresh-base`, `--controls`, `law_shape_ok`, `census_rederived_ok`, `depth_gap_recorded`, `re_scored_pins` — the exact set the amended claims name (F1, F2, F4, F7, F8). The draft's own `ExecCounterV2.md` report already concedes most of these as unimplemented; my check extends that list to the *predicate command itself*.

Two further divergences, both mine to report and the L1's to fix:

- **The rule-label check is still the v1 one.** `c1-counter.py:786` (and `:869` for the carrier spec) reject any `claim` other than `R50-C1`, so a frozen `tools/round-51/gap-rule.json` carrying `"claim": "R51-C1"` is unparseable by the counter that scores it. F10 requires the parser to accept `{R50-C1, R51-C1}`; the draft has not done it. The draft-time probes recorded this as the problem string on every round-51 rule variant they scored.
- **`carriers.json` and `gap-rule.json` are still the round-50 paths** in the draft's constants (`CARRIERS = 'tools/round-50/carriers.json'`, `FROZEN_PATHS` naming `tools/round-50/gap-rule.json`), while the amended claims require the round-51 rule at `tools/round-51/gap-rule.json` and the round-50 tables at `tools/round-50/oracle/`.

## F4 (BLOCKER for the `sourced` binding, not a defect in the draft) — the entry's `source:` lines must name the round-51 row, not only S243/S244/S245/S249

The counter's `sourced` binding is: an S-id named on one of the entry's `source:` lines must (a) exist in `corpus/SOURCES.md`, (b) have `opened` inside the counter's window, and (c) list this entry (path or stem) in its `used-by` cell. Measured with the counter's own parsing (`entry-binding-check.py`, and a direct re-implementation of the check over the registry):

- S243/S244/S245/S249 are `opened: 2026-10-28` and their `used-by` cell names only `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`.
- The v2 counter draft's `OPENED_DATES = ('2026-10-30',)`. Under that window **no** S243/S244/S245/S249 row can satisfy `sourced`, and none satisfies it under the widened `('2026-10-28','2026-10-29','2026-10-30')` window either, because their `used-by` cell does not name the round-51 entry.
- The `used-by` column **is** mutable under `tools/round-38/registry-immutable.sh` (only `status`, `recheck`, `used-by` may differ from the base), so the L1 can add the round-51 entry to those cells; but the `opened` date is immutable, so under `OPENED_DATES = ('2026-10-30',)` the **new** round-51 row is the one that can satisfy the binding.

**Action for the L1:** the draft's `source:` lines already carry two explicit placeholders for exactly this — the `ScoutUnsquashfs` device-node row and (conditionally, if C2 shares it) the `ScoutMksquashfs` padding row. Replace them with the real S-ids, register those rows with `opened: 2026-10-30` and this entry in `used-by`, and — if the L1 wants the widened window to count — add the round-51 entry to S243/S244/S245/S249's `used-by` cells too.

## F5 (correction to a round-50 sentence, no action on the counter) — the round-50 entry overstates what its own receipts establish, and the new entry supersedes rather than inherits it

`ConnSources/findings.md` §2 located an epistemic contradiction **inside** the round-50 entry: its :35 says "the retained receipts do not establish a universal rewrite rule" and carries the removed-symlink readdir-order dependence as **inference**, while its :48 and limit 7 label the same dependence an **observation**. It also says (:52) that the receipts cannot establish whether the `247:0` whitelist "was derived from the Cable class or was simply wrong", while the round-51 claims text asserts the former as the cause.

The draft handles this the way the lane's append-only contract requires: it does **not** rewrite the round-50 entry, it states the supersession in the draft's own "What moved, and only what moved" section, and it claims only what is measured — that the round-50 rule's silent list contains exactly the one detail the Cable class carries (`247:0`, `dev/led`) and that the FRITZ!Box class's other twelve details carry no disposition. The causal history of the old rule is not claimed.

## What the draft measured (committed bytes only, no REA, no downloads, no lane writes)

| id | UTC | exit | stdout sha256 (16) | what it establishes |
|---|---|---|---|---|
| `census-char-devices` | 05:18:57 | 0 | `2558bbc72d3412a1` | char-devices per carrier: c6430 1, c6490 1, g7581 13, g7582 13 |
| `census-kinds` | 05:18:57 | 0 | `7a666895d951d373` | kinds present: `symlink`, `dir`, `char-device` only — no fifo/socket/block-device row exists in any table |
| `census-fritzbox-twelve` | 05:18:57 | 0 | `26df0f304634fa2f` | 12 non-`dev/led` char-devices on each FRITZ!Box carrier |
| `census-g7581-devices` | 05:18:57 | 0 | `a4a718f37e4f8d6a` | the thirteen paths and their major/minor details |
| `oracle-tables-sha` | 05:18:57 | 0 | `5c07d99c5b2fd19d` | the four frozen oracle/non-regular tables' bytes |
| `gap-rule-r50` / `gap-rule-r50-silent` | 05:18:57 | 0 | `43f7c8d7…` / `d1f93947…` | the frozen round-50 rule: `required.char-device` true, `removed.silent.char-device` = `["247:0"]` |
| `r50-miss-receipt` / `r50-miss-carriers` | 05:18:57 | 0 | `7b0c500b…` / `b395d4c1…` | the committed miss: `carriers_matched 2` of 4, exit 1, `gaps_ok` false on g7581/g7582, and `g7581`'s `projection_ok` false (ENOENT rerun) |
| `r50-unpublished-kinds` | 05:18:57 | 0 | `3cb7bcd3…` | published files 3955/4709/4556/4564; unpublished kinds symlink only |
| `law-device-disposition` | 05:18:57 | 0 | `47485481…` | **28 of 28** device rows across the four envelopes carry no gap and no published path |
| `rule-scope-offline` | 05:18:57 | 0 | `f19fa145…` | CTL-OLD 2 of 4 (reproduces the miss), CTL-NEW 4 of 4 over the committed envelopes |
| `rule-shape-variants-offline` | 05:18:57 | 0 | `bb3ba036…` | the mutation table in F2, including the 14-device fixture |
| `failclosed-probe` | 05:12:31 | 0 | `6abe18f3…` | F1's fail-closed table |
| `entry-binding-check` | 05:18:57 | **1** | `6da9a85e…` | the draft's own shape is good; `sourced` unreachable and 28 placeholders outstanding → `needs-l1-fill` (exit 1 is the gate's "not ready", not an error) |
| `predicate-cli-vs-draft` | 05:19:09 | **2** | `e3b0c442…` | F3: the claims' predicate command is rejected by the v2 counter draft's CLI |
| `knowledge-file-count` / `sources-row-count` | 05:18:57 | 0 | `251afbc1…` / `bffd0dd9…` | 140 knowledge files today (141 with this entry), 156 SOURCES rows today |

The rule-scoped re-scoring is the claims' own CTL-OLD / CTL-NEW arms computed over the committed round-50 **envelopes** (`after.json`) plus the frozen oracle / non-regular tables, with the round-50 counter's own `gap_rule_model` / `disposition_check` — no live rerun, no carrier bytes, no REA. It is **not** the L1's control run and does not replace it; the L1's control receipts over its own frozen rule bytes are the authoritative ones. The full predicate is deliberately not claimed for either arm: the committed round-50 receipts fail `run_provenance_ok` (round-50 provenance prefix), `receipt_fresh` (added at `646d29c9`, before the round-51 freeze) and every byte-dependent clause.

## The entry draft's structure (what the L1 fills)

Provenance trio first, in the house order: `status:` → six `source:` lines (S243/S244/S245/S249 verbatim from the round-50 entry, plus two explicit placeholders for the round-51 rows the scouts open) → `verified-at: 2026-10-30` → `recheck:` (the predicate command + the two offline probes + the on-refetch chain). Then: what moved (and the two round-50 sentences this entry supersedes), the device-accounting law (its grounding, its measured width, its reached scope, the cross-claim obligation), the per-class census (Cable 1 / FRITZ!Box 13, every cell a triple), the miss it repairs (the before-arm, the rule-scoped CTL-OLD/CTL-NEW re-scoring, the mutation arms, the fail-closed table, the `claim`-label constraint), the carriers (the chain pins table, unchanged from round 50), the fresh data-run placeholders (four rows, all cells placeholders), the Core promotion (conditional, with the exact PROVINCE / README / SOURCES / SCORECARD / LOG obligations), Still Frontier, eleven limits (including the three the seat spec named — vendor bytes never committed, the extraction tree never committed, availability not holding — plus the law's width and reached scope), What was NOT examined, the instruments named, and the receipt ledger.

The 28 placeholders are: 1 in `status:`, 2 in the `source:` lines, 1 in `verified-at:`, 15 in the fresh-data-run table and its two notes, 1 in the promotion outcome, 2 in the "not examined" and "receipts" notes, and the rest in the results/PROVINCE obligations. `entry-binding-check.py` lists them by line number.

## Scope and limits of this seat's own work

- **Read-only on the lane tree.** I wrote only inside `.ufo/waves/round-51/w1/ScribeEntryC1/` and this report. No git/jj mutation, no commit, no push, no staging. The lane's pre-existing working-tree state (`plans/round-51-claims.md` modified, `tools/round-51/` untracked) is the L1's and other seats', not mine; `git status --porcelain` shows no change from my seat.
- **No REA, no downloads, no vendor bytes.** Every probe runs on committed lane bytes. The five probe scripts are **not** proposed as lane instruments; they are draft-time probes under the seat directory and the L1's own instruments must reproduce their results.
- **Nothing measured that was not measured.** The four-carrier data run, the round-51 controls, the landing counter receipts and the Core promotion are all `<PLACEHOLDER>` — none of them has happened.
- **Tools installed: none.** No pacman / uv / npx / cargo transaction was run; the operator's tooling directive was not exercised.
- **Disk guard:** `scripts/hyaku/disk-guard.sh status` was read before the pass; the scratch lived on `/fast/scratch/hyaku/kaidoku-r51/w1-ScribeEntryC1` and was removed after the receipts were copied into the seat directory. Nothing was written under `/tmp`.
- **One unrun check is named as unrun:** the deleted-guard fixture proof of `fetch-vendor.py` (routed defect 4) — `ExecFetchSelftest.md` records it as not run; my seat does not own it and did not run it.

## Files

- `.ufo/waves/round-51/w1/ScribeEntryC1/entry.md` — the draft entry (38 473 B, sha256 `1ea47d4368b0d526809a37f66aadc2bbfda9ce2b7b3b028febc4b826df1a66cc`).
- `.ufo/waves/round-51/w1/ScribeEntryC1/receipts.tsv` — the receipt ledger (id, UTC, exit, stdout sha256, command), one row per receipt above.
- `.ufo/waves/round-51/w1/ScribeEntryC1/law-device-disposition.py` — the 28-of-28 device-row disposition census.
- `.ufo/waves/round-51/w1/ScribeEntryC1/rule-scope-offline.py` — the CTL-OLD / CTL-NEW rule-scoped re-scoring.
- `.ufo/waves/round-51/w1/ScribeEntryC1/rule-variants-offline.py` — the rule-shape / mutation variants, incl. the 14-device fixture.
- `.ufo/waves/round-51/w1/ScribeEntryC1/failclosed-probe.py` — the fail-closed probe.
- `.ufo/waves/round-51/w1/ScribeEntryC1/entry-binding-check.py` — the entry-shape / `sourced`-reachability gate.
- `.ufo/waves/round-51/w1/ScribeEntryC1/receipts-collect.py` — the ledger collector.
