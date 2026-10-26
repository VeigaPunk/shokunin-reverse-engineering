# R41C1Counter — round-41 C1 counter port (pre-freeze)

**Verdict: DONE — the port is delivered and green (`--selftest` 97/97 cases exit 0,
`--selftest-rea` ok), and it now refuses the claim's own relabel control: the four round-40
receipts relabelled as V3/V4/L3/L4 score **0/4** (`carrier_fresh_ok`, every other clause true),
while one fresh AVM-genuine dev carrier scores green end-to-end (3/3 oracle rows, real REA rerun).
The refreeze prototype's "drop one `_extract` component" rule is FALSIFIED by measurement (0/7
oracle rows on a carrier whose chunk is not the whole input, 7/7 under the derivation-rooted rule);
the round-40 suffix rule's L2 false positive is unchanged (1/4 carriers) and is fixed by the same
exact rule. The port implements `R41C1Revenger` §1 (root from `derivations[]`, whole-segment prefix)
plus the L1's binding amendments.**

Base `49096c7e6f226af0c750c4b003be58883cb6049f`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Leaf seat: no subagents, no background jobs, no `agent://all`, no VCS mutation in the lane (all git in
scratch clones, `git -C` explicit, toplevel asserted). No reserved carrier or reserved image was read,
run, carved or copied: every REA/unblob run here is on the round-40 lane-built carriers V1/V2/L1/L2
(rebuilt/fetched as development inputs), on fresh trees built from them, or on a fresh AVM-genuine
image this seat wrote with the lane writer.

## 1. What was delivered

| artifact | sha256 | what it is |
|---|---|---|
| `c1-counter.py` | `9a3dcf4b1303bc1ecd45aa39d2277fff2e55b69109ffdb76f7c59d213524ed28` | the round-41 counter, 3447 lines (L1 installs it at `tools/round-41/c1-counter.py`) |
| `c1-counter-vs-r40.diff` | `2dbe765eda69f93e57644f9fa417b3f37a9f86becd2066c16868387a37347e54` | `diff -u` base → port: **1407 added / 263 removed** |
| `dryrun-dev.py` | `7defae10a1c6678d61c27b332dd5c35796d0b92c2388d67b9072a1af61c17afd` | builds a round-41-shaped fixture in a clone (carrier/receipt/oracle overrides) |
| `mk-fresh-dev.py` | `5de464a536d755aa8cb8e11fb36d33950cadf56d58377cb5ebdf84ab0819d1fb` | writes one fresh AVM-genuine dev image + its sasquatch oracle |
| `chunk-naming.py` / `chunk-naming.json` | `65541789…` / `388e3e22…` | the four measured chunk shapes behind the root rule (§3) |
| `legacy-demo.py` / `legacy-vs-exact.json` | `a64fa980…` / `9fd4c7f8…` | round-40 matcher vs exact matcher on the four committed receipts |
| `fresh-oracle.tsv`, `fresh-nonregular.tsv`, `fresh-receipt-envelope.json` | `c41694a1…`, `7fa39950…`, `10d89f32…` | the fresh carrier's independent oracle and its real REA receipt |
| `dryrun-fresh-counter.json` / `dryrun-adapted-counter.json` / `dryrun-verbatim-counter.json` / `dryrun-trail512-counter.json` | `c830f8a5…` / `b129d2ed…` / `5ee26ad6…` / `95bc753a…` | the four dry runs of §6 |
| `selftest.log` (+`-detail.log`), `selftest-rea.log` | `34c4f06e…`, `…`, `975166cd…` | exit 0 (re-run on the final file) |

Full diff = the artifact (command `diff -u $S/base.py <artifacts>/c1-counter.py`); its load-bearing
hunks are the extract-root block (§2), `disposition_check` (§4), `projection()` (§4), the freshness
clause (§4) and the new selftest families (§5). No tool was installed or upgraded.

## 2. The exact-path rule as implemented

1. `strip_output()` removes **one** optional `$output/` prefix (files / unpublished entries / gap
   `relative_path` are bare; gap `input_path`, `derivations[].parent_path/child_path` and
   `depth_limited_paths[]` are prefixed).
2. `squashfs_roots()` = `strip_output(child_path)` over `derivations[]` edges whose handler starts
   `squashfs_v4`. Never from path text.
3. `subject_root(env, hint)`: one root → that root; several → the freeze's `oracle_root`
   (new optional per-carrier key) or `None` → the three path clauses fail closed with
   `extract_root: null`; a hint naming no root is a frozen-table fault.
4. `extract_rel(P, root)`: `''` if equal, `P[len(root)+1:]` if `P.startswith(root + '/')`, else
   `None`. `same_rel()` = that `==` `strip_rel(row)`. Entries outside the root are **another
   namespace**: not compared, not reported as published. Regular files `rel ==` + `sha256 ==` +
   `size ==`; non-regular work never uses a link target; receipt absolute `path` is unused, and a
   diagnostic's absolute `report.link` is only used with the root as an anchored segment run.
5. The prototype helper (drop the first `_extract` component) is **not** ported. `legacy_same_rel()`
   (round-40's suffix rule) survives only so the selftest can assert it still mis-scores the fixtures
   (3 of 6 path probes discriminate). **The L1 must port this derivation rule, not the refreeze
   diff** - the diff fixes R40-CL1's suffix direction and breaks the root direction.

## 3. Measured: the root is not a fixed number of `_extract` components

Four real runs (`cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0
extract-firmware --format json --full-output --max-depth 1 <input> <fresh outdir>`), inputs built from
`corpus/evidence/round-40/c1/L1/carrier.sqsh` (230884 B); `chunk-naming.json`:

| shape | input | receipt's derivation root | rows: derivation rule / round-40 suffix / refreeze helper | gaps |
|---|---|---|---|---|
| whole file | `2521ded6…`, 230884 B | `firmware.bin_extract` | **7/7** / 7/7 / 7/7 | 1 depth-limited + 2 unpublished |
| `bytes_used` + 512 B | `a6827a83…`, 231396 B | `firmware.bin_extract/0-230884.squashfs_v4_be_extract` | **7/7** / 7/7 / **0/7** | 1 + 2 |
| 8192 B zero prefix | `10200e64…`, 239076 B | `firmware.bin_extract/8192-239076.squashfs_v4_be_extract` | **7/7** / 7/7 / **0/7** | 1 + 2 |
| L1‖L2, two filesystems | `1fe3d283…`, 472274 B | ambiguous (two roots) | 0 (fail closed) / 7/7 / 0/7 | **2** + 4 |

This independently reproduces `R41CritC1Draft` §(c) (their `carve-score.json`: helper 0/6 on an
offset-8192 carve; mine 0/7 against L1's 7-row oracle) and adds the **trailing-byte** shape, which is
the one a legal carrier can hit: superblock at offset 0, so `layout_ok` passes, but one byte past
`bytes_used` flips the root one level deeper. Every measured carrier also has
`geometry_agrees: true` - the derivation root equals the root implied by `chunks[].range` + handler +
the receipt's leading extract dir - reported per carrier (`chunk_summary`, `geometry_agrees`) so a
disagreement is visible without a clause no reserved carrier can be measured against yet.

## 4. The other bindings the L1 required

* **`carrier_fresh_ok` (new clause, 19 clauses total).** A carrier pin a previous C1 freeze already
  scored cannot be counted as new coverage: the prior set is the union of `carriers.json`'s new
  optional `prior_pins` (validated 64-hex, part of `carriers_spec_ok`) and the previous round's
  carrier table `PRIOR_CARRIERS = .ufo/waves/round-40/c1/carriers.json`, both read **at the freeze
  commit** (a table added later cannot bless an old pin). This is the claim's "relabelled round-40
  receipts" kill rule expressed as a clause; without it a rename is indistinguishable from coverage,
  and my own 4/4 dry run was its counterexample (§6).
* **Removal dispositions** (`R41C1DevCore` §7.1–7.3): `gap_check` → `disposition_check(gaps,
  diagnostics, nonreg, model, root)`; `gap-rule.json` may carry `removed: {diagnostic, kinds,
  disposition: "exclusive", silent?: {kind: [detail]}}`. A gap must resolve at its exact path to one
  entry whose kind allows that gap kind; every named removal diagnostic must resolve to an entry of a
  listed kind; no entry may be both gapped and removed; every required entry needs exactly one
  disposition (gap, removal, or - only when listed under `silent` - nothing). `empty-target` is the
  rule's label for an empty third column. **Deviation to note:** §7.1.3 phrases the silent allowance
  as a count equality; I implemented the per-row form (kind + detail must match a listed silent
  detail), which admits the same faithful extractions and is strictly stronger against camouflage.
  The freeze text should be re-worded to match.
* **Projection carries the removal identity:** diagnostics project as `[__typename__, rel]`
  (root-mapped `report.link`), and the projection's path normaliser is the subject root (falling back
  to the round-40 suffix form only outside it), so a carve directory present in one run cannot leak
  into the comparison. A rerun that removed a different link fails `projection_ok` (selftest case,
  isolated with `required.symlink: false`).
* **Vendor spec chain:** `carriers_spec` requires `external.member_sha256` (64 hex), a positive
  `external.length`, `nested.sha256` whenever a `nested` block exists, and a relative `oracle_root`
  when present. New clause **`carve_ok`:** external `length == bytes_used == size`, committed carrier
  `size == bytes_used` (bytes_used always from `layout_probe`, never from the spec).
* Constants: all round-41 paths, `IDS = (V3, V4, L3, L4)`, `PROV_SEGMENT = /kaidoku-r41/`, scratch
  `$HYAKU_SCRATCH/kaidoku-r41/counter`, `FROZEN_PATHS` = `plans/round-41-claims.md`, the seven
  `tools/round-41/*` tools and both frozen tables; `--carrier-cache <sha256>.bin` unchanged.

## 5. Selftest

`--selftest` (offline, simulated runner): **97 cases, exit 0** — 12 green, 85 red, 0 failures; plus
**6 path probes** (3 discriminating), **8 root probes**, **7 spec probes**. Round-40's base had 70
cases, so the port adds 27; every round-40 case survives renamed.

New families, each pinning one verdict: both collision directions (regular `usr/bin/busy` vs symlink
`bin/busy`, regular `sbin/tool` vs symlink `usr/sbin/tool`) and the published-symlink-path case still
caught; a gap on the deeper path not resolving to the shallow entry; a deeper file not publishing an
oracle row; two chunks with a nested file in another namespace (green with `oracle_root`, red without,
red for a bogus `oracle_root`, red for the nested file satisfying an outer row); the measured shapes
(padded carrier green, shallow publish red, two AVM chunks fail closed); dispositions (removal
admitted / gap+removal / none / unresolvable / unlisted kind / silent empty target admitted / silent
camouflage refused / rerun removing a different link breaks the projection); the spec and carve chain
(missing `member_sha256`, missing length, `nested` without `nested.sha256`, absolute `oracle_root`,
carrier longer than `bytes_used` → `carve_ok` red); freshness (relabelled `prior_pins`, previous-round
table in the lane, malformed `prior_pins`); and a receipt with no `squashfs_v4` derivation edge
(fail closed).

`--selftest-rea` (real REA, pkg root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`):
**exit 0, `selftest_rea: ok`**. The retained dev image is a 4096 B dump with `bytes_used = 365`, so the
fixture carrier is the image truncated to `bytes_used` (whole-input chunk, `carve_ok` true): green
carrier `carriers_matched 1`, failing clauses `[]`, `bindings_false ["compression_coverage"]`
(one-carrier fixture, documented); the oracle-only fabrication fails `projection_ok` (+`handler_ok`).

## 6. Dry runs (QUALITY 83) — and the relabel control

Fixture: `git clone -q --shared <lane> $D/lane`, `git -C $D/lane checkout -q 49096c7e…`, toplevel
asserted; `dryrun-dev.py` writes a round-41-shaped `.ufo/waves/round-41/c1/{carriers,gap-rule}.json`
plus `corpus/evidence/round-41/c1/<id>/` tables whose ids name the round-40 carriers V1→V3, V2→V4,
L1→L3, L2→L4, commits the tables as the freeze and the receipts as a descendant, and (with
`--adapt-provenance`) moves `output_directory`/`normalized_result.output_directory` to
`/kaidoku-r41/` and re-mints the evidence id with the frozen `tools/round-27/xpin-attribute.mjs`.

| run | freeze / rev | result | why |
|---|---|---|---|
| **fresh carrier** | `6a779172` / `9213cbba` | **1/4 matched**, `geometry_agrees` true ×4 | L3 is a fresh AVM-genuine xz image (`cb500eb7…`, 1734 B, `bytes_used == size`) with a real REA receipt and a sasquatch oracle: all clauses true, 3/3 rows, 2 gaps (1 structural), `projection_ok` true on a fresh rerun. V3/V4/L4 fail **only** `carrier_fresh_ok` |
| **relabel control** | `842bdc4b` / `81cf929f` | **0/4**, failing `carrier_fresh_ok` on all four | the round-40 receipts relabelled as round-41 carriers; every other clause true, so the refusal is attributable to freshness alone. This is CTL-C1-relabel, enforced |
| verbatim | `142c257f` / `8c17d7be` | 0/4, `carrier_fresh_ok` + `run_provenance_ok` | provenance clause still bites (`/kaidoku-r40/…`), freshness independently |
| carve past `bytes_used` | `e82f4b94` / `1d30b1cb` | 0/4: L3 `carve_ok`, others stale | L3 = L1 + 512 zero bytes (`a6827a83…`) with its real receipt: root `firmware.bin_extract/0-230884.squashfs_v4_be_extract`, 7/7 rows, `projection_ok` true, `carve_ok` **false** |

Prior pins in the fixtures: 4, source `.ufo/waves/round-40/c1/carriers.json` (the lane's own table at
the freeze commit). The 4/4 the item asked for is reachable only by disabling freshness - that is
exactly what CTL-C1-relabel is, so it is reported as the control rather than as evidence.

## 7. Risks / findings for the L1

1. **Relabel is now a clause, not a hope.** Keep `carrier_fresh_ok` in the freeze text and keep
   `prior_pins`/the round-40 table at the freeze commit; the freeze's own V3/V4 (5490/5491 members)
   and L3/L4 (new images) are fresh against round-40's four pins, so a correct freeze passes.
2. **`carve_ok` + `layout_ok` imply the whole-input shape.** A carrier that is exactly `bytes_used` of
   AVM SquashFS starting at offset 0 yields the single chunk `[0, bytes_used)` and the root
   `firmware.bin_extract`. The deeper-root support (portion, nested, `oracle_root`) is defence in
   depth; if the freeze ever wants a portion or nested carrier, both clauses need an explicit carve
   offset - say so in the freeze text.
3. **V4's fallback branch is not scorable as drafted.** "fallback the 5491 wrapper member" cannot
   pass `layout_ok` (no `sqsh` at offset 0). Either V4 is the carved rootfs (single squashfs at
   offset 0) or the claim needs a wrapper-specific layout/carve binding.
4. **Derivation edges can be weaker than the chunks.** If REA ever emits a `squashfs_v4` chunk whose
   derivation edge has `handler: null` (reported by the reviewer for an 8192 carve), the root is not
   found and the carrier fails closed with `extract_root_source: "no squashfs_v4 derivation edge"`.
   I did **not** add a geometry fallback (the reviewer's alternative) because it would turn "no
   derivation edge" into a silent success; instead every carrier records `chunk_summary` /
   `geometry_agrees` so the reviewer can see the geometry-derived root next to the chosen one. If the
   freeze wants a hard cross-check, that is a clause the L1 can add once V3/V4 receipts exist.
5. **Several `squashfs_v4` roots need `oracle_root`** (a wrapper that also extracts a nested image);
   without it the carrier fails closed rather than guessing.
6. **Entry budget (`R41C1DevCore` §7.4).** `max_output_files` is a hard 10 000-entry ceiling. Round-40's
   largest carrier stages 697 files + 381 non-regular = 1 078 entries, far inside it; the freeze
   should record V4's file+dir count from `sqfs-list` before trusting the rootfs branch (>9 500 is the
   practical stop). The counter does not pre-check this (no frozen constant for it yet).
7. **REA rerun flake observed once.** On one run of the carve-past-`bytes_used` fixture, REA returned
   `ok: false, exit 1` with empty stderr for the 5 446 392 B vendor carrier, so `projection_ok` went
   false; the identical command re-run seconds later passed (the retained JSON is the passing run).
   The runner now records REA's own `error` object in `projection_error` so a recurrence is
   diagnosable. A transient CLI failure fails the claim (exit 1), it does not become `unevaluable`.
8. **Silent-removal wording** (§4): implemented per-row; the freeze text should say so.
9. `--selftest-rea`'s green verdict carries `bindings_false ["compression_coverage"]` by design.

## 8. Tooling / scratch

No install or upgrade. Vendor bytes for the dev runs were rebuilt with the sanctioned command and kept
in scratch only (AVM licence - never copied into the lane):

```
python3 -I -B <lane>/tools/round-40/fetch-vendor.py --root <lane> \
  --rev 7fce308631a8b457d6b7c5a4b39a923c4e9a49de --cache $S/cache --image-cache $S/img
  -> V1 ac4098bd…8e95.bin (5442392 B), V2 5ccc7614…089b.bin (26013550 B)
```

Fresh dev carrier: `python3 -I -B artifacts/R41C1Counter/mk-fresh-dev.py --gen
<lane>/tools/round-40/gen-squashfs.py --out $S/fresh --comp xz` → `cb500eb7…`, 1734 B, oracle 3 rows
(sasquatch-v4be, rc 0) + 1 symlink row; receipt `npx -y rea-agents@6.5.0 extract-firmware --format
json --full-output --max-depth 1` (handler `squashfs_v4_be`, chunk `[0,1734)`, one depth-limited gap).

Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C1Counter` (clones, probe receipts, caches) was removed
after the artifacts above were copied; every number here is in this directory or reproducible with the
commands quoted above.
