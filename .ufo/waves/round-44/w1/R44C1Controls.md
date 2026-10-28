# R44C1Controls — R44-C1 controls: driver, committed input fixtures, scored receipts

Seat `R44C1Controls` (executor, wave 1). Claim: `plans/round-44-claims.md` `## R44-C1`.
Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch:
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Controls/`. No lane file was modified except the two
paths this seat installs (`tools/round-44/c1-controls.py`, `tools/round-44/control-fixtures/`);
no commit, no push, no `c1-run.sh`.

## 0. Verdict

**All seven controls were built, scored against the frozen counter, and behaved exactly as the claim
states. `kill_rule_fires: false`.** The counter is not always-fail: **CTL-C1-POS reaches exit 0,
`met_target` true, `carriers_matched 4/4`, every boolean binding true and zero failing carrier
clauses** — four real REA 6.5.0 receipts plus the C1 landing blocks planted as control fixtures.

Two riders, both measured, both the L1's to close before the freeze:

1. **The frozen `tools/round-44/carriers.json` blob at HEAD is not the corrected table.** It still
   lists six carriers (the two `v21le`/`v21be` exploratory rows) and carries no per-carrier `oracle`
   block and no `toolchain`. Scored against those bytes, `carriers_spec_ok` is false (the counter
   refuses `v21*` as "not part of R44-C1") and `oracle_ok`/`tree_ok`/`oracle_hits_ok` are false on
   every carrier, so `met_target` can never be true. The scored run below therefore uses a
   **rehearsal freeze**: a scratch clone whose freeze commit carries the working-tree table. The
   lane freeze is untouched and every receipt is stamped `rehearsal: true`.
2. **CTL-C1-POS now reaches exit 0** because its sandbox also plants the C1 landing blocks
   (`R44C1Doc`'s PROVINCE Core row + frontier note + README map row, and `R44EntryDraft`'s entry)
   as *control fixtures* under `tools/round-44/control-fixtures/pos/`. Those are fixtures, not the
   landing, and the arm is excluded from the kill rule: reaching the target is what it is for.
   PROVINCE is **appended only** (prefix byte-preserved, as the claim requires); the README row is
   inserted inside `## Coverage map`; the `<AFTER-DATA: …>` markers are replaced with a stated
   control headline rather than planted.

## 1. Deliverables

| path | kind | note |
|---|---|---|
| `tools/round-44/c1-controls.py` | **installed tool** | sha256 `b8c55f9b9d8af47e56f6bc8c11b21018b7fb1997c4fd399355c045a16aafa402`; same bytes as the artifact |
| `.ufo/waves/round-44/w1/artifacts/R44C1Controls/c1-controls.py` | authored tool | same bytes |
| `tools/round-44/control-fixtures/<ctl>/**` | **committable control inputs** | the planted bytes per control, preserved at their destination paths, plus `manifest.json` (destination → fixture file, sha256, size) and the control's expectation |
| `.ufo/waves/round-44/w1/artifacts/R44C1Controls/controls/<ctl>/receipt.json` | scored receipt | seat, command (full argv), exit code, stdout sha256, wall, expected, measured failing clauses, tree manifest |
| `.../receipts/CTL-C1-{0,1,2,3,4,5,POS}.json` | flat receipts | same documents, one per control |
| `.../receipts/selftest.json` | driver selftest | 11 cases, 11 passed |
| `.../controls/summary.json` | run summary | carrier scope, per-control verdict, kill-rule flag |

Per the freeze helper's rule (`.ufo/**` is not committable), the **content-addressed control inputs
live under `tools/round-44/control-fixtures/`** and `.ufo` keeps only transcripts and receipts.
`tools/round-44/` is already frozen as a directory pathspec, so the fixtures are covered by the
existing freeze list; no new frozen path is needed.

## 2. The seven controls, scored

Counter `tools/round-44/c1-counter.py` sha256 `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`.
Every control is planted in a `git clone --shared` sandbox at the freeze, committed after it (the
counter's `receipt_fresh` clause), and scored with the frozen argv
`--root <sandbox> --rev <planted> --freeze <FREEZE> --pkg65 <rea-agents 6.5.0> --work <scratch> --json-out <abs>`.

| control | exit | carriers | what the counter refused it on | verdict |
|---|---|---|---|---|
| **CTL-C1-0** do-nothing | 1 | 0/4 | every carrier `receipt_present` false; all six documentation bindings false | as expected |
| **CTL-C1-1** v3 receipts relabelled | 1 | 0/4 | `subject_pin_ok`, `handler_ok`, `gaps_ok`, `oracle_hits_ok`, `projection_ok`, `run_provenance_ok`, `extract_root_confirmed`, `nonregular_unpublished_ok` | as expected |
| **CTL-C1-2** oracle-only fabrication | 1 | 0/4 | **`projection_ok` only**, on all four carriers | as expected |
| **CTL-C1-3** sasquatch absent | 1 | 0/4 | on the stripped carrier: `chunks_ok`, `gaps_ok`, `oracle_hits_ok`, `projection_ok`, `extract_root_confirmed`, `nonregular_unpublished_ok` | as expected |
| **CTL-C1-4** pre-freeze envelopes relabelled | 1 | 0/4 | `run_provenance_ok` on all four (`…/kaidoku-r42/…` output dirs); three also `chunks_ok`/`oracle_hits_ok`/`projection_ok` | as expected |
| **CTL-C1-5** mutated superbytes | 1 | 0/4 | no receipt planted; the 12 mutations are byte-delta-recorded (see §4.6) | as expected |
| **CTL-C1-POS** positive control | **0** | **4/4** | **nothing — `met_target` true, every boolean binding true, zero failing carrier clauses** | as expected |

`summary.json`: `failures: []`, `unevaluated: []`, `kill_rule_fires: false`, driver exit **0**. Only
CTL-C1-POS is excluded from the kill rule, because it is a positive arm: reaching the target is its
purpose, so it can never fire a kill.

### 2.1 CTL-C1-2 — the sharpest result in the set

The oracle-only fabrication publishes the oracle's members at their oracle sha256/size, names the
frozen handler, carries the one chunk and one derivation edge, sets `gaps == []`, and has its
evidence id re-minted through the frozen xpin rule **after** the output directory rewrite. It passes
`subject_pin_ok`, `handler_ok`, `chunks_ok`, `oracle_ok`, `tree_ok`, `oracle_hits_ok`, `gaps_ok`,
`run_provenance_ok`, `evidence_id_ok` and `path_shape_ok` — and is caught by **`projection_ok`
alone** on all four carriers. That is exactly the R40-CL2 / R43-CL-witness class the claim names,
and it is the strongest available evidence that the counter's discrimination is the counter-time
REA rerun and not a lucky field mismatch.

### 2.2 CTL-C1-POS — what "green" means here

Real REA 6.5.0 captures, one per scored carrier, in scratch (never `c1-run.sh`, never written into
the lane's `corpus/evidence/round-44/c1/`):

| carrier | handler | gaps | published bytes | coverage |
|---|---|---|---|---|
| `v1le` | `squashfs_v1` | `[]` | 20 | complete |
| `v1be` | `squashfs_v1` | `[]` | 20 | complete |
| `v2le` | `squashfs_v2` | `[]` | 28 | complete |
| `v2be` | `squashfs_v2` | `[]` | 28 | complete |

`parameters.output_directory` and `normalized_result.output_directory` are absolute paths inside
`/kaidoku-r44/` (what the counter's `run_provenance_ok` reads), and each id is **re-minted after**
that rewrite. The same sandbox plants the C1 landing blocks as control fixtures:

| planted | bytes | shape | why it is safe |
|---|---|---|---|
| `PROVINCE.md` | base + Core row + frontier note | **append-only** (`append_only: true`, base sha `e385f119…` → new `1aab8d0d…`) | the claim pins the PROVINCE prefix byte-preserved, and appending cannot move it |
| `corpus/README.md` | base + one `## Coverage map` row | row inserted inside the section | the counter reads the section, and the row names the entry stem |
| `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` | the entry | new file, `source:` cites S112/S138/S139 | `sourced` needs S138 and S139, both already in the freeze with `used-by` naming the entry |

Result: **exit 0**, `met_target` true, `carriers_matched 4/4`, per-carrier failing set empty, every
boolean binding true, `oracle_tool_ok` true.

## 3. What the L1 runs at the freeze

```
python3 -I -B tools/round-44/c1-controls.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --freeze <FREEZE> --pkg65 <rea-agents 6.5.0 package root> \
    --counter tools/round-44/c1-counter.py --from-fixtures \
    --work <SCRATCH> --out <RECEIPTS_DIR>
```

Exit codes are semantic: **0** every control behaved as the claim states, **1** a control
misbehaved (`summary.json` then sets `kill_rule_fires: true` if a counterfactual red control reached
`met_target`), **2** could-not-evaluate — never a pass. `--from-fixtures` plants the committed
`tools/round-44/control-fixtures/**` bytes instead of rebuilding them, so the scored inputs are the
frozen ones. `--build-only` rebuilds fixtures, `--selftest` exercises the driver alone,
`--capture-only` re-runs the REA dev arm, `--rehearsal-table-freeze PATH` scores against a scratch
freeze that carries a candidate `carriers.json` (dev arm only; refuses on the real freeze).

## 4. Findings the L1 must close before the freeze

### 4.1 The frozen carriers table is not the corrected one — blocking

Measured against the frozen blob at HEAD: six carriers (`v21le`/`v21be` extra) → `carriers_spec_ok`
false, and the counter iterates those ids and reds them; no per-carrier `oracle` block and no
`toolchain` → `oracle_ok`/`tree_ok`/`oracle_hits_ok` false on **every** carrier. With the
working-tree table (four carriers, oracle blocks, toolchain) the same controls score 4/4 with no
carrier clause false. **The worktree `tools/round-44/carriers.json` must be the frozen bytes**, and
`oracle.tool` must stay the absolute `/usr/bin/unsquashfs` (a bare `unsquashfs` makes
`oracle_tool_ok` false — that was real until the L1 fixed it mid-seat).

### 4.2 Provenance: the counter's rule, and the claim text that contradicts it

`provenance_ok()` requires an **absolute** path containing `/kaidoku-r44/` (`PROV_SEGMENT`), no `..`
component. `tools/round-44/c1-run.py` records exactly that shape and copies the produced tree into
`corpus/evidence/round-44/c1/`. The claim sentence that says the receipt's `output_directory` must
name a `corpus/evidence/round-44/c1/` path is therefore wrong and should read "absolute, inside the
`/kaidoku-r44/` scratch segment; the runner copies the produced tree/receipt into
`corpus/evidence/round-44/c1`". CTL-C1-POS and CTL-C1-2 both use the scratch-segment shape;
CTL-C1-4 depends on the refusal of the `/kaidoku-r42/` shape.

### 4.3 `gaps == []` is coupled to `parameters.max_depth`, which the counter replays

The counter replays the receipt's own `parameters.max_depth` on its rerun. A receipt captured at the
default (3) replays at 3 and yields `gaps == []`; a receipt captured with `--max-depth 1` replays at
1 and carries a `depth-limited` gap, which the counter's zero structural allowance reds. `c1-run.py`
passes no `--max-depth`. **Do not introduce one.**

### 4.4 CTL-C1-2 is only as sharp as the projection profile

The fabrication is caught because the profile is `plus-extractor` (measured `projection_profile:
plus-extractor`): the file rows carry no `mime_type`/`md5`/`sha1` and there is no `raw_result`, so
the rerun projection differs. Under a `core` profile the six compared fields are all oracle-visible
and a projection-identical fabrication would pass — the round-42 counter records that exact limit. If
the profile is ever narrowed, treat a CTL-C1-2 pass as the claim's disclosed limit, not as a
weakened control.

### 4.5 CTL-C1-4 reds on provenance, not on the D1 byte-identity arm the claim names

The claim says the counter "rejects any after-receipt byte-identical to a pre-freeze committed
envelope". **No such arm exists in `tools/round-44/c1-counter.py`** — there is no comparison of a
planted receipt against the round-42 `c2/heldout` or round-43 `c1/heldout` envelope bytes (the only
`evidence_digests` field records the digests the counter *read*, and the only relabel-shaped
selftest case is `score receipt relabelled as REA evidence`). CTL-C1-4 still reds, but on
`run_provenance_ok` (the `…/kaidoku-r42/…` output directory), which is the weaker of the two
guards. Either implement the byte-identity arm or drop that clause from the claim; do not cite
CTL-C1-4 as evidence for a guard that is not there. (This also means committing the POS fixtures
cannot trip that clause, since it does not exist.)

### 4.6 CTL-C1-5 cannot be driven through the counter's public CLI

`carriers.json` pins each carrier's `path` **and** `sha256`; planting mutated carrier bytes trips
`carrier_pin_ok` before the superblock probe, and rewriting the table trips
`carriers_unchanged`/`frozen_path_changed`. The control therefore records the twelve mutation byte
deltas and digests — per carrier, per byte order: magic `hsqs`/`sqsh` → `XXXX`; `s_major` 1/2 → 3;
`s_minor` 0 → 9 — and plants the mutated copies under
`corpus/evidence/round-44/c1/superbyte-mutation/`. **Recommendation: the ported counter's
`--selftest` must carry these three mutations per byte order**, which is the only surface where a
pinned carrier can be mutated *and* scored.

## 5. Defects found and fixed inside this seat

Each was caught by running the tool, not by reading it.

1. **Stripped-PATH capture silently succeeded.** The draft *prepended* the shim directory, leaving
   `~/.local/bin` (and `sasquatch`) resolvable behind it. Fixed by **replacing** the child PATH with
   a scratch bin of symlinks to every executable of the fixed PATH except `sasquatch`, plus
   preconditions that refuse to continue if `sasquatch` still resolves or `npx` does not.
2. **Sandbox ancestry asked the wrong repository.** `merge-base --is-ancestor` ran in the source
   lane, where the planted commit does not exist; the selftest case failed and the driver's own
   claim was unproven. Fixed by asking the sandbox.
3. **CTL-C1-POS reds `evidence_id_ok` on every carrier.** Rewriting `parameters.output_directory`
   invalidates the captured evidence id (the id is minted over the projection, which includes
   `parameters`). Fixed by re-minting after the rewrite.
4. **Relative `--json-out` killed the counter's receipt write.** The counter runs with `cwd=work`,
   so a relative `--json-out` resolved under scratch and the counter died in `write_receipt` (the
   verdict was still true — the judge correctly failed closed with "no readable receipt"). Fixed by
   absolutising the path and falling back to the counter's stdout document.
5. **The binding check counted `*_detail` rows as claims.** The `bindings` map also carries
   `compression_detail`, `handler_detail`, … (lists/dicts); only booleans are claims. Fixed.

## 6. Driver selftest

`receipts/selftest.json` — **11 cases, 11 passed**, against a stub counter that cannot be mistaken
for the real one: sandbox is its own git repo; a planted file is byte-exact; a planted commit
descends from the freeze; the counter is invoked with the frozen flags; the receipt records exit
code, stdout sha256 and wall time; a red stub satisfies a red expectation and fails a green one; a
wrong `carriers_matched` fails closed; the positive path passes; **exit 2 never passes a red
control**; a missing receipt is reported as unreadable, never assumed true.

## 7. Residual gap

| surface | state |
|---|---|
| `tools/round-44/c1-controls.py` | installed, sha256 `32003f28…`, selftest 11/11 |
| `tools/round-44/control-fixtures/**` | written, content-addressed, committable |
| seven scored receipts | present, all as expected, `kill_rule_fires: false` |
| scored against the **frozen** table | blocked by §4.1 — six carriers, no oracle block, at HEAD |
| CTL-C1-POS exit 0 | **reached**: real receipts + the C1 landing blocks planted as control fixtures; excluded from the kill rule |
| CTL-C1-5 probe assertion | not CLI-drivable; belongs to the counter's `--selftest` (§4.6) |
| claim provenance sentence | contradicts the counter; correct it per §4.2 |
