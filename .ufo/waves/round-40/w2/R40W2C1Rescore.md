# R40W2C1Rescore — reproduce the R40-C1 score at `42c10a58`

**CONFIRMED** — the R40-C1 score reproduces with **zero divergence**: `carriers_matched = 3`, `target = 4`,
`met_target = false`, exit **1**, `projection_diff = []` on all four carriers, every binding identical to
`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`. `c1-extra.py` reproduces at exit **0** / `met = true`.
The L1's read of the single miss is correct and is the **sole** blocker: `L2` fails only
`nonregular_unpublished_ok`, and that clause is a counter false positive (regular file `usr/bin/busy` read as
the symlink `bin/busy`). I additionally proved attribution with a mutant of the frozen counter: with that one
clause's comparison corrected, the same frozen bytes and the same real REA reruns give **4/4, `met_target`
true, exit 0**. The honest stop is therefore faithful to the frozen rule and the demotion at the tip is
faithfully recorded; the defect is in `tools/round-40/c1-counter.py`, frozen before the carriers ever had a
receipt.

Seat scope only: reproduction, divergence, and attribution. No lane writes outside this report and
`.ufo/waves/round-40/w2/artifacts/R40W2C1Rescore/`.

## Environment

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (revs `42c10a58`, freeze `7fce3086`, tip `4d62ee5a`).
- Scratch: `/fast/scratch/hyaku/kaidoku-r40/R40W2C1Rescore` (carrier cache + all outputs; removed at seat
  close — everything cited is copied into the artifacts dir). Every counter REA rerun went to a private
  `mkdtemp` under `/fast/scratch/hyaku/kaidoku-r40/counter`, deleted by the counter's own `finally`.
- Vendor bytes fetched, never copied into the lane: `fetch-vendor.py` at the freeze, exit 0, both carriers
  `http 200` and pin-equal (`ac4098bd…8e95`, `5ccc76…089b`; `artifacts/…/fetch-vendor.json`).
- Tooling: **nothing installed or upgraded** (all tools already present: unblob 26.6.4, sasquatch-v4be 4.5.1,
  rea-agents 6.5.0 package root, node/npx). No pacman transaction; no VCS mutation (read-only `git show/log` only).
- Timings (wall): full counter 9.4 s / 9.4 s / 10.2 s (three revs), c1-extra 0.6 s, selftest 7.0 s, mutant 8.5 s.

## 1. Reproduction at the measured revision

```
python3 -I -B <LANE>/tools/round-40/c1-counter.py --root <LANE> --rev 42c10a58cb2cae3a4a0122af35a0cf95ac718043 \
  --freeze 7fce308631a8b457d6b7c5a4b39a923c4e9a49de \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --carrier-cache /fast/scratch/hyaku/kaidoku-r40/R40W2C1Rescore/cache --json-out …/c1.json
```

| Field | L1 receipt (`c1-at-42c10a58.json`) | My run | Δ |
|---|---|---|---|
| exit code | 1 | **1** | 0 |
| `carriers_matched` / `target` | 3 / 4 | **3 / 4** | 0 |
| `met_target` | false | **false** | 0 |
| `frozen_path_changed` | `[]` | **`[]`** | 0 |
| `carriers_unchanged`, `gap_rule_unchanged`, `frozen_tables_valid` | true | true | 0 |
| `projection_profile` | `plus-extractor` | `plus-extractor` | 0 |
| `projection_diff` V1/V2/L1/L2 | `[] [] [] []` | **`[] [] [] []`** | 0 |
| 10 `bindings` | all true | all true | 0 |
| per-carrier clause dicts (17 clauses each) | — | identical | **0** |

A recursive compare of the two JSON documents (all keys; only `argv` skipped) reports **0 divergences**
(`artifacts/…/divergence-vs-l1.txt`). The per-carrier `output_directory` is byte-equal too — it is the
*committed receipt's* recorded path (`/fast/scratch/hyaku/kaidoku-r40/run-<id>/extract`), not my rerun's, so
the L1's stated values are reproducible rather than seat-local. Only `argv` differs (`--carrier-cache`,
`--json-out`), which is environment.

Per-carrier at `42c10a58` (my run, equal to the L1's):

| id | pin | handler | oracle hits | gaps | projection | clauses failing |
|---|---|---|---|---|---|---|
| V1 | ok | `squashfs_v4_be`, no failed chunk | 697/697 | 264 (1 structural) | ok | none |
| V2 | ok | `squashfs_v4_be`, no failed chunk | 8/8 | 86 (1 structural) | ok | none |
| L1 | ok | `squashfs_v4_be`, no failed chunk | 7/7 | 3 (1 structural) | ok | none |
| L2 | ok | `squashfs_v4_be`, no failed chunk | 6/6 | 3 (1 structural) | ok | **`nonregular_unpublished_ok`** |

`matched = all(17 CLAUSES)` (`c1-counter.py:1125`; `CLAUSES` at `:228-233`), so one false clause is
enough — this is exactly the observed 3/4.

## 2. Supplementary gate `c1-extra.py`

Exit **0**, `met: true`, bindings `frontier_content`, `oracle_rederived` (`V1/V2/L1/L2 = ok`), `sourced_new`
(`S124,S125,S126` new-with-used-by) — file-level identical to
`c1-extra-at-42c10a58.json` modulo `argv`/`--json-out`
(`artifacts/…/c1-extra-at-42c10a58-local.json`). So the L1's "supplementary gate met" is exact.

## 3. Controls either side of the landing

| rev | role | exit | matched | failing bindings / carriers |
|---|---|---|---|---|
| `7fce3086…` | freeze = do-nothing (CTL-C1-0) | **1** | **0** | every carrier `receipt_present: false`; bindings `province_core_section`, `province_core_row`, `frontier_note`, `entry_present`, `sourced`, `coverage_map_row` false |
| `42c10a58…` | measured / landing | **1** | 3 | L2 `nonregular_unpublished_ok` |
| `4d62ee5a…` | tip after demotion | **1** | 3 | L2 `nonregular_unpublished_ok` **plus** `province_core_row: false`, `province_core_section: false` (`province_core_rows_seen: []`) |

Both expected exit 1s confirmed. The tip is red for the two intended reasons at once: no `## Round-40
additions to Core` heading survived the demotion (`git show 4d62ee5a -- PROVINCE.md` renames it to
`## Round-40 measured, not promoted (R40-C1 honest stop)`), and the L2 clause still fails. `frozen_path_changed`
is `[]` on all three revs, so no frozen C1 path moved after the freeze — the counter, carriers, oracles and
tables are the freeze bytes (counter authored only in the freeze commit `7fce3086`; `git log -- tools/round-40/c1-counter.py`
lists that commit alone).

## 4. The L2 miss: false positive confirmed, and it is the only blocker

### 4.1 Trace

Frozen data (`corpus/evidence/round-40/c1/L2/`):

- `nonregular.tsv`: `bin/busy  symlink  /usr/bin/busy`, `usr/bin/ls  symlink  busy`, plus 8 directories.
- `oracle.tsv`: 6 regular files, including `usr/bin/busy  40000 bytes  e28f81fc…8e70`.
- `after.json`: 6 published files; `unpublished_entries` = both symlinks
  (`firmware.bin_extract/bin/busy` target `../usr/bin/busy`; `firmware.bin_extract/usr/bin/ls` target `busy`);
  gaps = 2 × `unpublished-entry` (one per symlink) + 1 × `depth-limited`.
  **No published path is a symlink path.**

The clause:

```python
def same_rel(candidate, rel):                     # :606-607
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))

def nonregular_published(files, nonreg):          # :643-649
    for fp, _, _ in files:                        # fp = raw receipt path, e.g. firmware.bin_extract/usr/bin/busy
        for rel, _kind in nonreg:                 # rel = bare relative path, e.g. bin/busy
            if same_rel(fp, rel): hits.append(fp)
```

Direct probe against the frozen module (loaded from `git show 42c10a58:tools/round-40/c1-counter.py`, no lane
edit; `artifacts/…/suffix-exposure.txt`):

```
same_rel('firmware.bin_extract/usr/bin/busy', 'bin/busy')          -> True
rel_suffix('firmware.bin_extract/usr/bin/busy')                    -> 'usr/bin/busy'
rel_suffix(...) == 'bin/busy'                                      -> False
nonregular_published(L2 files, L2 nonreg)                          -> ['firmware.bin_extract/usr/bin/busy']
hits under exact strip-then-compare rule                           -> []
```

Exposure across all four carriers: **only L2** has a non-regular path that is a proper path-suffix of a
published regular path (`bin/busy` ⊂ `usr/bin/busy`); V1 (381 non-regular entries), V2 (95), L1 (13) return
`[]`. No carrier has an *exact* file/symlink path collision.

### 4.2 Attribution mutant — the one clause is the whole gap

Driver `artifacts/…/mutant-strict-rule.py` loads the frozen counter unmodified, replaces only
`nonregular_published` with "strip the `*_extract/` chunk directory (`rel_suffix`), then compare exactly", and
calls the frozen `measure()` at `42c10a58` with the real REA reruns:

```
carriers_matched 4   met_target True   exit_if_cli 0
L1/L2/V1/V2: matched true, nonregular_published [], nonregular_unpublished_ok true, projection_ok true,
             oracle_hits == oracle_files (697, 8, 7, 6), gaps_ok true
all 10 documentation bindings true
```

So with the false positive removed, the **same frozen bytes, receipts, carriers and reruns** meet P40-C1.
This mutant is **not** an admissible score (the counter is a frozen path; editing it post-freeze is
`frozen_path_changed`, exit 2 — the counter's own red case "counter edited after freeze" is one of the 65).
It is attribution evidence only: the claim failed on this clause and on nothing else at `42c10a58`.

### 4.3 Why it is a defect, not a fixture artefact

1. **Internal inconsistency.** `projection()` already normalises every receipt path with `rel_suffix` before
   comparing (`:808` files rows, `:835` gaps, `:842` unpublished rows). `nonregular_published` is the
   only consumer of `same_rel` that compares a *raw prefixed receipt path* against a *bare relative table
   path*, so it is the only place where a segment-boundary suffix is ambiguous.
2. **Redundant with the rerun.** `files` and `unpublished_entries` are in the projection for every profile,
   so a receipt that really published a symlink as a regular file would differ from the counter's fresh run
   and fail `projection_ok`. The clause is defence in depth; it bought no coverage the projection lacks, and
   it cost the promotion.
3. **The 70-case selftest cannot see the class.** `--selftest` → `{"cases": 70, "green_ok": 5, "red_ok": 65,
   "failures": []}`, exit 0. Its `nonregular_unpublished_ok` red case (`:1783-1787`) appends a file at an
   *exactly equal* symlink path (`firmware.bin_extract/usr/share/demo/escape`). No case publishes a file whose
   path merely *contains* a shorter non-regular relative path.
4. **The risk class was named in wave 1 and not carried.** `w1/R40MutR39.md:152` (N-C1): "the equality branch
   of `same_rel` is load-bearing for green but unpinned … (or the contract declares suffix-only and drops the
   branch)"; `w1/R40C1Controls.md:138` (defect 2): "'same relative-path suffix' (CTL-C1-14) accepts
   publication under any root. Require the exact `<extract_root>/<relpath>` …". Round 40 kept `same_rel` in the
   unpublished clause with neither the exact-path form nor a collision case. The control that could have
   caught it pre-freeze did not exist: CTL-C1-0 at the freeze has no receipts at all (0/4), and the first L2
   receipt appears only at `73c7bf9c`, after the freeze.

## 5. Independent checks of the substantive core (so "3/4" is not the only thing verified)

- **Carrier pins**: `sha256sum` of the committed L1/L2 carriers = `2521ded6…1a0d` / `fec0f72d…5928` =
  `carriers.json`; fetched V1/V2 = `ac4098bd…8e95` / `5ccc7614…089b` = pins; `carrier_pin_ok` true on all four.
- **L2 layout, read by hand** (`xxd -l 96` + `xxd -s 240269 -l 8`): magic `sqsh`, `s_major/minor = 4.0`,
  `mkfs_time = 0x0003aeee = 241390 = bytes_used` (AVM marker), `block_size 4096`, compression id 1 (gzip),
  `inode_table_start 0x3aa8d`, and the metadata header at that offset is `1d 83` → little-endian `0x831d`,
  length `0x031d = 797` (the big-endian reading would be 7555). That is the genuine AVM layout the claim
  states (BE fields, LE 2-byte block lengths), independent of the counter's probe.
- **Oracles**: `c1-extra` re-derives all four from the frozen reader (`oracle_rederived: V1/V2/L1/L2 = ok`).
- **Receipts**: `operation = extract_firmware`, `provider.id = unblob`, one `squashfs_v4_be` chunk with
  `extraction_failed: false`, `evidence_id_ok` true on all four, `receipt_fresh` true (first add `73c7bf9c`,
  descendant of the freeze), `run_provenance_ok` true, `--max-depth 1` recorded in `run.json`
  (unblob 26.6.4 `0ce7b6…1d09`, sasquatch-v4be 4.5.1 `fac887…14c6`).

## 6. Calibration notes on the author verdict

- "L2 failed **only** `nonregular_unpublished_ok`" — correct (the other 16 of 17 clauses true, 0 divergences).
- "a path-suffix false positive" — correct in the alarm sense; the counter wrongly *fires*. The commit
  subject (`4d62ee5a`, "counter suffix false negative on L2") and the README line ("on a counter suffix false
  negative") use the opposite name for the same event; `PROVINCE.md`'s own paragraph in the same commit says
  "a suffix false positive". Terminology only — no factual overclaim, but the lane now carries both words for
  one defect.
- "the supplementary gate met" — correct (§2).
- "the Core row was then demoted to a measured-not-promoted record" — correct and conservative: the demoted
  row is labelled "measured, not promoted", the frontier note says "promotion waits for a re-frozen counter",
  `corpus/README.md` says "**measured, not promoted** (R40-C1 honest stop, 3/4 on a counter false negative)",
  and the entry body says "**Measured; R40-C1 stopped, not promoted.**" No document claims MET. The demotion
  touched no frozen C1 path (tip `frozen_path_changed: []`).
- "an honest stop" — compliant with the claim's kill rule ("A miss at the measured revision is an honest
  stop") and with freeze integrity. Under the frozen bytes no in-round action could have made the counter
  exit 0; the stage at which it was fixable was wave 1, before the freeze.

## 7. Limits

- The mutant (§4.2) changes a copy of the frozen counter and calls `measure()` directly; it is attribution,
  not a score, and is explicitly not offered as evidence that P40-C1 was met.
- I verified one direction of the over-broad suffix (a published file whose path contains a shorter non-regular
  path). I did not exhaustively search for a *lax* direction that would let a wrong receipt pass this clause;
  `projection_ok` covers the fabricated-receipt class (red case in the 70-case selftest).
- Counter reruns were executed with the seat's carrier cache, which is byte-equal to the pins; the rerun itself
  cannot prove which process wrote the committed receipts (the claim's disclosed limit, unchanged).
- I did not re-score C2, did not re-derive the gap rule, and did not audit every wave-1 artefact; the only
  wave-1 material I used is the two `same_rel`/suffix findings cited in §4.3.

## 8. Artifacts (`…/.ufo/waves/round-40/w2/artifacts/R40W2C1Rescore/`)

| file | sha256 | content |
|---|---|---|
| `c1-at-42c10a58-local.json` | `8bb864ea68f617ecb3b908280fa8e9a962bd8bbda3adbff8afe3b3496bfc1e33` | my counter run at the measured rev |
| `c1-extra-at-42c10a58-local.json` | `b8641269d11cef6365e4d29545781dc74f88a270e04b68bb9a070b500f408da6` | c1-extra at the measured rev |
| `c1-at-freeze.json` | `1e460d8aa797ffa074023c00f3b4a11c708fe01d6981e488ed3efe1e76ec2905` | do-nothing at `7fce3086` |
| `c1-at-tip.json` | `1b422dd72daccc5701190a06d4d0ead9c7d0cb128db778d8760dad6419c9af96` | tip `4d62ee5a` |
| `divergence-vs-l1.txt` | `c376385f8b8bbd6d927585bcaf226c4068d51a8b37b6d923abe4e32c3b45c430` | 0-divergence report vs the L1 receipt |
| `mutant-strict-rule.py` / `.json` | `85e60aba…b576` / `d03c69b9…535e` | attribution mutant + result (4/4, met) |
| `suffix-exposure.txt` | `03df3af8f40f38b1aac4bdb10a45e0e1a8e2b6a9587bfcfe497b5d3ea05d2db6` | per-carrier `same_rel` exposure |
| `fetch-vendor.json` | `f7839c18567b0863fc7af177c1ba53aee8d55bf8941e47961a728c60076e6df0` | vendor fetch, both pins ok |
| `c1.stdout` | `0fed1e487eccf441ac98eb59109e8c8f3dff2b9c6e3da7678ecf932a42379bb5` | summary line of the measured run |

Reference receipts compared against (lane, read-only):
`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` `881a66230925367ac01fe57a9ecf14f8322ead787f81084839bc966ca8e13216`,
`.ufo/waves/round-40/l1/scores/c1-extra-at-42c10a58.json` `ffe8ebe2fec14dc78a359bf8532f889f8585811bd109ddf9c9dee7076d2afab6`.
No vendor firmware bytes and no extracted vendor files are in this directory.
