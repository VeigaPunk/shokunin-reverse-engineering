# R41W2C1Rescore — independent re-score of R41-C1

**CONFIRMED — R41-C1 is met at `e9a24d07` and still met at lane HEAD `e1c83313`; I could not
falsify it. Three calibration defects found (D1–D3 below), none outcome-changing.**

I attacked the author verdict *from outside the counter*: I rebuilt the vendor carriers myself at
the freeze, scored the claim at four revisions, reran REA 6.5.0 on all four carriers with my own
commands and compared the results to the committed receipts with my own comparison code (not
`tools/round-41/c1-counter.py`), validated the oracle against a third-party extractor
(`sasquatch-v4be` 4.5.1, no `-be`) and against a byte-level superblock probe, reproduced both
controls, and then tried to *push fabricated receipts and a frozen-path edit through the counter*
to see what it accepts. Every discrimination test failed closed in the intended binding.

Seat rule: nothing outside `.ufo/waves/round-41/w2/R41W2C1Rescore.md` and
`.ufo/waves/round-41/w2/artifacts/R41W2C1Rescore/` was written; no VCS mutation in the lane
(sandbox clones only, identity `fx`); scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Rescore`
removed at the end. No tool was installed or upgraded (npx cache for `rea-agents@6.5.0` already
present; `unblob` 26.6.4, `sasquatch-v4be` 4.5.1 used as found). Vendor bytes were never copied
into artifacts — digests and the rebuild command only (AVM licence).

## 1. Commands, exit codes, divergences

Counter argv for every run below (`L` = lane root, `C` = my cache `$S/cache`):

```
python3 -I -B $L/tools/round-41/c1-counter.py --root $L --rev <REV> \
  --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --carrier-cache $S/cache --json-out <OUT>
```

Cache filled first, independently, at the freeze:

```
python3 -I -B $L/tools/round-41/fetch-vendor.py --root $L \
  --rev d764389e9cbe61b9d1b07538ff3bff02d50bb34f --cache $S/cache      # EXIT 0, 8.6 s
```
`V3` image `770efb4e…5ab7` → member `87cc5d6b…a0f8` → carve `c4f74f54…f872a` (30 233 394 B);
`V4` image `a5a3a763…f661` → member `4cfc3016…2f6c` → nested `4d5de25c…d947` → carve
`ce27ebca…087f` (32 720 860 B). Artifact `artifacts/R41W2C1Rescore/fetch-vendor-freeze.json`.

| revision | counter exit | carriers_matched | met_target | frozen_path_changed | why |
|---|---|---|---|---|---|
| `49096c7e` (base) | **1** | 0 | false | `[]` | no round-41 receipts, no docs (`carriers_unchanged`/`gap_rule_unchanged` false: the frozen tables do not exist yet) |
| `d764389e` (freeze, CTL-C1-0) | **1** | 0 | false | `[]` | 0.126 s: no receipts to rerun; every doc binding false — the surface is unmoved, as the claim says |
| `042b8769` (landing docs) | **1** | **3** | false | `[]` | V4's `after.json` does not exist yet (`receipt_present: false`); V3/L3/L4 all matched |
| `e9a24d07` (measured rev) | **0** | **4** | **true** | `[]` | 21.4 s incl. four counter-time REA reruns, all `projection_diff: []` |
| `7a24ff74` (dispatch tip) | **0** | **4** | **true** | `[]` | same, 26 s for this and the 042b run together |
| `e1c83313` (lane HEAD, extra) | **0** | **4** | **true** | `[]` | still met one commit after dispatch |

`c1-extra.py` (same cache, `--base 49096c7e…`): **exit 0**, `met: true`,
`frontier_content/oracle_rederived/sourced_new` all true, `new_with_used_by: ["S127","S128"]`,
`oracle_rederived: {V3,V4,L3,L4} = ok` (3.2 s).

**Divergence against the L1 receipts is exactly one field per file, and it is `argv`** (L1 ran with
`--root .` from the lane and a shared cache dir; I ran absolute paths and my own cache). Field-by-field
deep diff (`rescore-summary.json`):

```
c1-at-e9a24d07.json        vs c1.json        : 1 diff -> /argv   (all 4 carriers, all bindings, all details equal)
c1-extra-at-e9a24d07.json  vs c1-extra.json  : 1 diff -> /argv   (bindings + detail equal)
c1-at-042b8769.json        vs my 042b run    : 1 diff -> /argv   (met false, 3/4, same per-carrier flags)
```

## 2. Independent re-derivation (my own REA runs, my own comparison code)

I did not trust the counter's rerun projection: I ran REA myself on all four carriers and compared
with `artifacts/R41W2C1Rescore/compare.py` (rules re-implemented from the frozen predicate text:
strip one `$output/`, root = `child_path` of the `squashfs_v4*` derivation edge, rel only under
`root + '/'`, equality — no suffix test).

```
cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
  --format json --full-output --max-depth 1 <carrier> <fresh outdir>        # exit 0 each
```
V4 14.9 s, V3 2.5 s, L3+L4 4.4 s. Comparison result — **PASS on all four, zero differences**:

| carrier | files rel/sha256/size | gaps | removals | coverage / published_bytes | root |
|---|---|---|---|---|---|
| V3 | 8 = 8, 0 hash/size diffs | 85 `unpublished-entry` + 1 `depth-limited` | 0 | partial / 31 227 104 | `firmware.bin_extract` |
| V4 | 6349 = 6349, 0 | 611 + 1 | 4 (`lib/libbroadbandcfg.so`, `…so.1`, `usr/www/avm/cgi-bin/system_status`, `usr/www/avme/cgi-bin/system_status`) | partial / 110 187 475 | same |
| L3 | 13 = 13, 0 | 3 + 1 | 0 | partial / 194 049 | same |
| L4 | 14 = 14, 0 | 3 + 1 | 0 | partial / 174 930 | same |

Non-regular accounting, recomputed from the receipt alone: V3 85 symlinks = 85 gaps, 0 removals;
V4 **615 symlinks = 611 gaps + 4 removals, each exactly once**; L3/L4 3 symlinks = 3 gaps; no gap or
removal resolves to a dir/device; no non-regular row published as a file; exactly one structural
`depth-limited` each; no `unknown-chunk-handler`. Matches the frozen `gap-rule.json`
(`allowed.symlink=[unpublished-entry]`, `removed={MaliciousSymlinkRemoved, exclusive}`,
`structural={depth-limited:1, unknown-chunk-handler:0}`).

**Oracle corroboration (third party).** `sasquatch-v4be -f -no-exit-code -d …` (4.5.1, no `-be`) on
V3 and V4, hashed with `sq-vs-oracle.py`: V4 6349 files / 615 symlinks / 401 dirs — oracle_only 0,
tree_only 0, value_differ 0, symlink path sets equal, **0 symlink-target mismatches**; V3 8/85/9
same result. The char device `dev/led` is not created unprivileged, which is exactly why it is a
`char-device` row and not a publication. The oracle is therefore not an under-approximation that
REA could both satisfy and hide behind.

**Layout, from the bytes.** `probe-layout.py` reads the superblock without the lane's reader: all
four carriers `magic='sqsh'`, BE `major=4 minor=0`, `block_size == 1<<block_log`,
**`bytes_used == file size == mkfs_time`**; the LE reading is nonsense (`major=1024`), so the
structural fields are genuinely big-endian; the 2-byte header at `inode_table_start` is plausible
only little-endian (V3 724 → exact single-block identity `30231260+2+724 == 30231986`; L3 1411;
L4 1337; **V4 2024 is plausible but the single-block identity does not hold** — V4's inode table
spans multiple metadata blocks, so `layout_ok` there rests on the plausibility walk, corroborated
by two independent extractions).

**Carrier provenance.** `mk-l-carriers.py --builds 2` rebuilds L3/L4 **byte-identically** to the
committed pins (`04cfb4cd…`, `4c0e5459…`), `build2-equal`, with the claimed counts (L3 13 files /
3 links / 20 dirs, L4 14 / 3 / 17); the both-direction collisions are in the tables
(regular `usr/bin/busy` + symlink `bin/busy` → `../usr/bin/busy`; symlink `usr/sbin/tool` →
`/sbin/tool` + regular `sbin/tool`; deep pair `opt/x/etc/conf` vs `etc/conf`; empty `var/tmp/empty`
= `e3b0c442…`). L3's own receipt is the discriminator: it publishes `usr/bin/busy` and
`sbin/tool` while `bin/busy` and `usr/sbin/tool` are `unpublished-entry` gaps — the counter's
equality matcher scores that right; a suffix matcher could not. `fetch-vendor.py` with a tampered
`member_sha256` exits **1** with `link: "member_sha256"`, `ok: false`, and materialises nothing for
V3 (V4 unaffected): the R40-CL6 chain is fail-closed.

## 3. Controls and discrimination (attacked, not assumed)

Controls reproduced from scratch:
* **CTL-C1-0** at the freeze: exit 1, 0/4 (see table above).
* **CTL-C1-1** round-40 receipts relabelled into the round-41 receipt paths, in my own sandbox
  clone at the freeze, commit `f376d82c…` (`-c user.name=fx`): exit **1**, 0/4,
  `subject_pin_ok: false` and `projection_ok: false` on every carrier with
  `projection_diff = [subject_sha256, files, chunks, extraction_gaps, unpublished_entries,
  published_bytes(+diagnostics on V4)]`. 21 s ⇒ the reruns really execute.

Selftests: `c1-counter.py --selftest --pkg65 …` → exit 0, **97 cases, green_ok 12, red_ok 85**,
path_probes 6 (3 discriminating), root_probes 8, spec_probes 7; `c1-extra.py --selftest` → exit 0,
17/17.

Adversarial probes I ran through the counter (sandbox clone, own commits; artifact + `revision`
field in each JSON):

| probe | commit | counter | caught by |
|---|---|---|---|
| one hex char changed in V4 `files[0].sha256` | `819dc2c6…` | exit 1, 0/4 | `oracle_hits_ok` 6348/6349 **and** `projection_ok` **and** `evidence_id_ok` |
| fabricated file at the symlink path `bin/ash` | `b6acd2ee…` | exit 1, 0/4 | `nonregular_unpublished_ok` (`nonregular_published: 1`) + projection + evidence id |
| one file dropped from V4's receipt | `1129f7ae…` | exit 1, 0/4 | `oracle_hits_ok` 6348/6349 + projection + evidence id |
| a line appended to the frozen `V4/oracle.tsv` | — | **exit 2** | `frozen_path_changed: ["corpus/evidence/round-41/c1/V4/oracle.tsv"]` |
| the same, then **restored** (net diff vs freeze empty) | — | **exit 2** | same path still reported — a later restore does not un-block, exactly the claims-file rule |
| V3 receipt `parameters.max_depth` set to 3 | `eae64a1d…` | exit 1, V3 unmatched | `projection_ok: false` — REA's own `unreadable_output` ("Report exceeded 8388608 bytes") at depth 3 |
| V3 receipt chunk handler set to `squashfs_v4` (LE) | `9e7610fc…` | exit 1, V3 unmatched | `handler_ok: false` + `projection_diff: ["chunks"]` |

Receipts are stable artefacts, not rewritten later: blob ids are identical at first add and at tip
(V3 `b22d4b91…`, V4 `2f1d34fe…`, L3 `9dbc687b…`, L4 `6cb2bea2…`); V3/L3/L4 were first added in
`5ca6941b`, V4 in `e9a24d07` (skipped by the directory commit's 1 MiB rule, disclosed in the commit
message). The frozen tool/table bytes are identical in the working tree, at the freeze, at the
measured rev and at the tip (`c1-counter.py bbabbfec…`, `c1-extra.py 531724e1…`, `fetch-vendor.py
1cb0a346…`, `sqfs-list.py a8e633f5…`, `c1-run.sh bdb97632…`, `mk-l-carriers.py fa2debc0…`,
`gen-squashfs.py 309c502d…` (both copies), `plans/round-41-claims.md 64ec060d…`, `carriers.json
65dc5c14…`, `gap-rule.json 73acb262…`), and no commit in `d764389e..7a24ff74` touches
`tools/`, `plans/` or `.ufo/waves/round-41/c1/`. Round-40 comparators the claim cites are real:
V1 oracle 697 rows, V2 oracle 8 rows.

Documents: PROVINCE `## Round-41 additions to Core` row names `genuine AVM-layout big-endian
SquashFS v4 (squashfs_v4_be)` with the supersession paragraph and the round-41 frontier note;
`corpus/README.md` lines 97/212/258 map the stem and the Frontier line; `corpus/SOURCES.md` S127/S128
exist with vendor-listing digests and are absent at the base; the entry
`corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md` cites S112/S114/S121/S124/S125/S126/S127/S128.
Every number in the entry's carrier table matches my measurements (8/95, 6349/1017, 13/23, 14/20
regular/non-regular; inode counts 104/7367/37/35; xz 4, gzip 1; carve lengths = `bytes_used`).

## 4. Findings (none changes the verdict)

**D1 — the counter does not compare oracle file *size*, though the predicate says "same sha256 and
size".** `parse_oracle()` keeps `(rel, sha256)` and drops column 3; `oracle_hits()` compares rel and
sha only. Closed in fact, not in text: equal sha256 ⇒ identical bytes ⇒ equal size, `c1-extra.py`
re-derives the table as exact lines (size included), and my own comparison checked `(rel, sha, size)`
against both the receipt and a sasquatch extraction with 0 differences. Severity: textual.

**D2 — the predicate's "(`--max-depth 1`)" is not asserted by the counter.** It deliberately replays
the receipt's recorded depth (selftest case *"rerun takes max_depth from the receipt, not a
constant"*), so the clause is bound only indirectly. All four committed receipts record
`max_depth: 1` (verified) and a depth-3 receipt is still rejected — but here for an incidental
reason (REA's 8 MiB report cap at depth 3 on V3), not because depth 1 is required. A consistent
depth-3 receipt on a carrier where depth 3 changes nothing could pass while violating the text.
Severity: binding tightness, not landing-breaking.

**D3 — PROVINCE wording overstates the reservation.** The Core row's Probe says "four frozen
carriers no extractor touched before the freeze"; wave 1 did run `sasquatch-v4be` directly on V3
(and cross-checked V4) to build the oracle — `corpus/evidence/round-41/c1/V3/oracle-run.json`
records the `sasquatch_v4be` argv/exit 0, and `w1/R41C1VendorV3.md:206` shows the run. The precise
claim — "no seat ran REA or unblob … before the freeze" — is what holds and what the receipts'
freshness demonstrates. Severity: documentation precision.

**D4 (observation) — `run_provenance_ok` is a path-shape token test** (absolute path containing the
`kaidoku-r41` segment, no `..`), not a binding of the receipt to this lane's run. The claim does not
lean on it; the rerun is the real binding, and my independent rerun now corroborates the receipts
from outside the counter.

## 5. Residual limits (honest)

* **R40-CL2 stays open in the strong form.** Neither the counter's rerun nor mine can prove *which
  process* wrote the committed `after.json`. What is now established independently is that the
  content of all four receipts is exactly what REA 6.5.0 + unblob 26.6.4 + `sasquatch-v4be` 4.5.1
  produce today on the pinned bytes, whose whole vendor chain I re-fetched and re-hashed.
* **V4's layout binding rests on the plausibility walk**, not the single-block identity (D-probe
  above); two independent extractions and the oracle agreement carry that carrier.
* **Vendor bytes never entered the lane or my artifacts.** Rebuild with
  `python3 -I -B tools/round-41/fetch-vendor.py --root . --rev d764389e9cbe61b9d1b07538ff3bff02d50bb34f --cache <DIR>`
  (exit 0, 8.6 s); pins `c4f74f54…f872a` (V3), `ce27ebca…087f` (V4).
* Everything in this report is measured on this host on 2026-10-26; nothing is inferred except where
  tagged `[INFERENCE]` — I used that tag nowhere, because every statement above has a command and an
  artifact behind it.

## 6. Artifacts (`artifacts/R41W2C1Rescore/`, 3.2 MB)

`c1.json`, `c1-extra.json` (+stdout) — my score at `e9a24d07`; `c1-at-042b…json`,
`c1-at-7a24ff74….json`, `c1-at-head.json`, `c1-at-base.json` — the four revisions;
`ctl-c1-0.json`, `ctl-c1-1.json` (+stdout) — controls; `mut-sha1char.json`,
`mut-symlink-as-file.json`, `mut-drop-file.json`, `mut-frozen.json`, `mut-restored.json`,
`p-depth3.json`, `p-le-handler.json` — discrimination probes (each carries its sandbox `revision`);
`rea-v3/v4/L3/L4.json` — my own REA envelopes (V4 2.9 MB; metadata+digests only, no vendor bytes);
`compare.py` + `cmp-v4/v3/L3/L4.json` — receipt vs my rerun vs oracle; `sq-vs-oracle.py` +
`sq-vs-oracle.json` — sasquatch leg; `probe-layout.py` + `probe-layout.json` — byte-level layout;
`fetch-vendor-freeze.json`, `tampered.out` — vendor chain, positive and fail-closed;
`lcar.out` — L3/L4 rebuild and determinism; `selftest.out`, `extra-selftest.out`;
`rescore-summary.json` — run table + the one-field (`/argv`) divergence against every L1 receipt;
`sandbox-commits.txt` — sandbox provenance.
