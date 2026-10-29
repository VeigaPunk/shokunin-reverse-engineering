# C1MutLayout — mutation probe of the round-41 counter's layout clauses (wave 1, pre-freeze)

**Verdict: the round-41 selftest kills 37 of 48 single-point mutants; the control is green (exit 0, 97 cases). 11 mutants survive. Of those, 6 are real selftest gaps the port must close (M03, M06, M10, M12, M21, M34), 1 is a selftest gap on a load-bearing flag (M28, rename hole verified in git), 1 is a redundant guard (M31), 1 is clause-level only and conjunction-safe (M43), and 2 are equivalent mutants (M25, M37). No drafts of the port were touched; nothing in the lane was modified.**

Scope met: every family in the seat spec has at least two mutants (magic M01/M02; s_major/s_minor M03/M04; compression id M05/M06/M07; mkfs_time==bytes_used M08/M09; metadata-length endianness M12/M13/M14 plus cap M11; handler-name M15/M16; extract-root mapping M17/M18; removal disposition M19/M20/M21; rerun projection M22/M23; evidence-id recompute M24/M25; target constant M26/M27; freeze walk M28/M29/M30/M31). Extra clause mutants M32–M48 cover pin freshness, carve, chunks, oracle hits, provenance, the CLAUSES tuple and first-add.

## Findings for the port (ordered by weight)

1. **Compression id is not gated by the round-41 counter (M06).** `layout_probe` (counter lines ~682–761) decodes `compression` but no reason branch tests it; it only feeds the binding `compression_coverage` (`any == GZIP_ID` and `any in XZ_IDS`, so ids 2 *or* 4 pass). Widening `XZ_IDS` to `(2,3,4,5)` leaves every selftest case green. The plan's predicate requires compression id **4** exactly. The port must add a `compression == 4` reason branch in `layout_probe` and selftest cases with ids 2, 3 and 5 expecting `layout_ok` red. Note the round-41 selftest L4 fixture uses id 2, so a port that gates `== 4` must change that fixture or its expected value.
2. **Rename hole in the freeze walk is untested (M28).** Verified on a throwaway fixture repo (`git mv oracle.tsv moved.tsv` then `git log --pretty=format: --name-only HEAD~1..HEAD`): default rename detection lists only `moved.tsv`; `--no-renames` lists `moved.tsv` and `oracle.tsv`. The round-41 code correctly passes `--no-renames`; the selftest does not lock it. Without the flag, a post-freeze rename of a frozen path that the counter does not read (e.g. `tools/round-41/sqfs-list.py`, a FROZEN_PATHS entry the counter never opens) would score exit 0. Suggested case: post-freeze `git mv tools/round-41/sqfs-list.py` expecting exit 2 `frozen_path_changed`. Keep `--no-renames` in the port.
3. **Version minor is untested (M03).** Only (4,0) fixtures exist. Suggested case: superblock with minor 1 expecting `layout_ok` red (`version 4.1 is not 4.0`).
4. **bytes_used beyond EOF only tested at 0xFFFFFFF0 (M10).** A `bytes_used = len(raw)+1` probe is not exercised at `layout_probe` level; in measure() the `carve_ok` clause catches it, so the selftest's `want_fail='layout_ok'` would have caught a regression only by accident. Suggested: a direct `layout_probe` case with `bytes_used = len(raw)+1` expecting reason `bytes_used … outside`.
5. **Metadata-length identity branch: the both-identity case is missing (M12).** `if d['le_identity'] and not d['be_identity']` can be weakened to `if d['le_identity']` with no red case. Suggested: a header plausible both ways where both `le_identity` and `be_identity` are true; must be `ambiguous` (layout red).
6. **Silent-allowance row without a third column is untested (M21).** `silent_detail_matches(None)` returning True admits a row like `bin/x<TAB>symlink` under `silent: {symlink: [empty-target]}`. Suggested: that row with `gaps_ok` expected red.
7. **External-carrier carve equality is untested (M34).** Only the committed branch's `bu == size` is covered (the 'sloppy carve' case). Suggested: an external carrier whose frozen `length == bytes_used` but whose raw bytes carry trailing data; `carve_ok` must be red.
8. **Selftest exit code for a missing xpin is 1, not 2 (observed, not a mutant).** Running `c1-counter.py --selftest` from a directory with no `tools/round-27/` sibling printed `xpin-attribute.mjs not found from …` and exited **1** (`find_xpin` raises `SystemExit(<str>)`). The header contract says 2 = unevaluable. The port should raise `Unevaluable` (exit 2) there.
9. **Redundant guard (M31).** `res['carriers_unchanged'] = cur == frozen` adds nothing while `frozen_drift` catches every carriers.json edit (it is in FROZEN_PATHS); it only matters if the rename hole (finding 2) is open. No separate case is needed once finding 2 is closed.
10. **Clause-level false positive, conjunction-safe (M43).** With `root_value` None, `nonregular_unpublished_ok` reads True because `esc` is empty. `met_target` stays false through `oracle_hits_ok`. If the port adds per-clause assertions, make the root-None case assert that every root-dependent clause is False.

## Equivalent or argued-equivalent mutants (no selftest case needed)

- **M25** (drop `ev[key][0].startswith('ev_')`): the xpin tool always emits `ev_`-prefixed ids, so the prefix test cannot differ from equality. [INFERENCE: xpin output not exercised with a non-`ev_` id.]
- **M37** (drop `--diff-filter=A` in `first_add`): the oldest commit touching a path is its addition, so `lines[-1]` is the same either way. [INFERENCE from git semantics; not run on a fixture.]

## Method and receipts

- Scratch copy: `cp` of the lane's `tools/round-41/c1-counter.py` (read-only) → sha256 `bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc`, equal to `git show 7c678ae6…:tools/round-41/c1-counter.py | sha256sum` (exit 0).
- Companion: `tools/round-27/xpin-attribute.mjs` from base → sha256 `8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708`.
- Baseline command, from `<mutant>/tools/round-41/`: `HYAKU_SCRATCH=<scratch> python3 c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` → **exit 0**, 97 cases, stdout sha256 `34c4f06e9fc9ab32c75e10361fb5855b07347c08ed63d1740fcc2cd4083e3741` (`results/baseline-selftest.stdout.json`), 13 s wall.
- Mutants: `mut-driver/mutate.py` (35 mutants + control) and `mut-driver/mutate2.py` (13 mutants); each anchor must occur exactly once (none failed). Each mutant ran with its own `HYAKU_SCRATCH` and cwd, through `--selftest`. Results: `results/mutation-results.json`, `results/mutation-results-2.json`; `mut-driver/run.out`, `run2.out`. Wall time 67 s and 26 s on 8 workers.
- Exit codes are the selftest's own: 0 = all cases green (survived), 1 = a case disagrees (killed), anything else = crash. No mutant crashed or timed out. M30 is killed through an exit 2 (unevaluable) on a green case, a legitimate kill.
- SHA256 of the driver and results: `mutate.py` 4802bad5…f3dc; `mutate2.py` 788c2a1e…23f0; `results/mutation-results.json` 79fe240e…f7cd; `results/mutation-results-2.json` 5547e01a…e749. `baseline-selftest.stdout.json` 34c4f06e…3741.
- Installs or updates: none. Used host `python3` and `git` (read-only: `show`, and a throwaway `git init` in scratch for the rename check). No pacman, no lane or fleet writes, no `--data-run`, no git mutation outside a scratch fixture.
- Scratch `/fast/scratch/hyaku/kaidoku-r50/C1MutLayout` removed after copy.

## Mutant table (all 49 runs)

| id | mutation (clause) | mutant sha256 (16) | selftest exit | status | first failing case / note |
|---|---|---|---|---|---|
| M00 | control: unmutated round-41 counter | bbabbfecb229e899 | 0 | SURVIVED | control, unmutated copy of base blob bbabbfec |
| M01 | magic: accept hsqs as BE magic | 935e61d3c1a5a862 | 1 | KILLED | killed by: little-endian superblock magic: want 1 got 0 |
| M02 | magic: no magic test | e2025cd068c92238 | 1 | KILLED | killed by: little-endian superblock magic: want 1 got 0 |
| M03 | s_major/s_minor: version test drops minor | dc8f1f265a4354b9 | 0 | SURVIVED | SURVIVED: no fixture with minor != 0; add layout case version 4.1 -> layout red |
| M04 | s_minor: wrong superblock offset | 0963977348c4a16a | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M05 | compression id: little-endian read | 065751f3ca8e1446 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M06 | compression id: XZ set widened to 3,5 | 376c773e4f33ce1a | 0 | SURVIVED | SURVIVED: round-41 counter never gates compression id (only binding compression_coverage); port must test compression == 4 exactly; add ids 2,3,5 red cases |
| M07 | compression id: GZIP id aliased to xz 4 | 82e5efc28367e1ae | 1 | KILLED | killed by: no xz carrier (compression coverage): want 1 got 0 |
| M08 | mkfs_time==bytes_used: >= instead of == | a69aea08c4c15f1b | 1 | KILLED | killed by: marker-stripped genuine-LE-lengths carrier: want 1 got 0 |
| M09 | mkfs_time: little-endian read | 5b0593e7e4ebdbd1 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M10 | bytes_used sanity: admits 4 KiB past EOF | 9facffcf12aa5871 | 0 | SURVIVED | SURVIVED: only bytes_used=0xFFFFFFF0 tested; add bytes_used = len(raw)+1 layout probe case |
| M11 | metadata cap widened 8192->65536 | fee9fe70f9c98192 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M12 | length endianness: identity branch ignores BE identity | 26404c45281b2066 | 0 | SURVIVED | SURVIVED: no fixture with le_identity and be_identity both true; add that case -> must be ambiguous (layout red) |
| M13 | length endianness: plausibility branch ignores BE plausibility | a525ef3d259f77d9 | 1 | KILLED | killed by: metadata length plausible both ways (no identity): want 1 got 0 |
| M14 | length endianness: uncompressed flag mask wrong | 4756829f5bdd2bc0 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 1 |
| M15 | handler name: any squashfs_v4* accepted | 1e02890e6760ef85 | 1 | KILLED | killed by: chunk handler is the LE handler: want failing clause 'handler_ok', failing=['projection_ok'] |
| M16 | handler name: only first chunk inspected | cdcca69cec40b15d | 1 | KILLED | killed by: padded carrier: the oracle resolves under the portion chunk directory: want 0 got 1 |
| M17 | extract-root mapping: suffix match (R40-CL1 regression) | e32f56421756dace | 1 | KILLED | killed by: probe 'dir 1: regular usr/bin/busy vs symlink entry bin/busy': exact matcher True, want False |
| M18 | extract-root mapping: root prefix from first segment only | ee5b6aee4d7c97d3 | 1 | KILLED | killed by: padded carrier: the oracle resolves under the portion chunk directory: want 0 got 1 |
| M19 | removal disposition: entry-kind check dropped | e82fe81740c05206 | 1 | KILLED | killed by: a removal naming a row of an unlisted kind fails: want 1 got 0 |
| M20 | removal disposition: gapped-and-removed check dropped | f07d7dacfd4375be | 1 | KILLED | killed by: an entry cannot be both gapped and removed: want 1 got 0 |
| M21 | removal disposition: silent row with no detail admitted | b287e1b4eba3998a | 0 | SURVIVED | SURVIVED: no silent-rule row lacking a third column; add `bin/x\tsymlink\n` under silent empty-target -> gaps_ok red |
| M22 | rerun projection: diagnostics key dropped from core profile | 3975a6514fc70e2e | 1 | KILLED | killed by: fabrication differing only in the diagnostics multiset: want 1 got 0 |
| M23 | rerun projection: verdict forced true | 52eb39f3bf0055e3 | 1 | KILLED | killed by: oracle-only fabrication with re-minted evidence id: want failing clause 'projection_ok', failin |
| M24 | evidence id: recomputed-equality dropped | 4f9bd46812969f16 | 1 | KILLED | killed by: evidence id stale after an edit: want failing clause 'evidence_id_ok', failing=['projection_ok' |
| M25 | evidence id: ev_ prefix test dropped (expected equivalent) | b9f2d993e5e93453 | 0 | SURVIVED | SURVIVED, equivalent [INFERENCE]: xpin emits ev_-prefixed ids; prefix test redundant |
| M26 | target constant 4->3 | aa120c791047c5b5 | 1 | KILLED | killed by: spec probe 'external carrier with a member_sha256': ok=False want True (problems ['carriers has |
| M27 | target comparison loosened to >= target-1 | 0b3fb5269f67d553 | 1 | KILLED | killed by: receipt missing (V4): want 1 got 0 |
| M28 | freeze walk: rename detection not disabled | 2dd800aa898b498e | 0 | SURVIVED | SURVIVED, selftest gap (code correct): drop of --no-renames hides a rename of a frozen path; add post-freeze git mv case -> exit 2 |
| M29 | freeze walk: nonregular table not a frozen path | c0211ae364a58042 | 1 | KILLED | killed by: nonregular table changed after freeze: want 2 got 1 |
| M30 | freeze walk: range includes the freeze commit | 34c0c9847689a715 | 1 | KILLED | killed by: green (4 AVM carriers, fresh receipts, docs): want 0 got 2 (unevaluable) |
| M31 | freeze walk: carriers_unchanged forced true | 09ae1e002b9b8567 | 0 | SURVIVED | SURVIVED, redundant guard: frozen_drift already raises for carriers.json edits; still untested |
| M32 | carrier_fresh_ok: prior pins ignored | af2bb3dee781a50b | 1 | KILLED | killed by: relabelled previous-round pins (prior_pins): want 1 got 0 |
| M33 | provenance: .. climb not refused | 94b5170c5a6c14db | 1 | KILLED | killed by: provenance path climbs out with ..: want 1 got 0 |
| M34 | carve_ok: file-size equality dropped | 3738bbde1afb6257 | 0 | SURVIVED | SURVIVED: external-branch carve only; add external carrier with trailing bytes past frozen length == bytes_used |
| M35 | carrier_pin_ok: sha256 comparison dropped | 200a813a2dae7acd | 1 | KILLED | killed by: frozen pin wrong (carrier untouched): want failing clause 'carrier_pin_ok', failing=['subject_p |
| M36 | receipt_fresh: freeze itself accepted as first add | ac6212e925db9457 | 1 | KILLED | killed by: receipt added at freeze: want 1 got 0 |
| M37 | receipt_fresh: first_add without --diff-filter=A | f05c892d59e77d21 | 0 | SURVIVED | SURVIVED, equivalent [INFERENCE]: oldest commit touching a path is its add; --diff-filter=A redundant |
| M38 | chunks_ok forced true | 3e84f47847bc42b9 | 1 | KILLED | killed by: failed chunk: want failing clause 'chunks_ok', failing=['projection_ok'] |
| M39 | CLAUSES tuple drops layout_ok | 38509a39ed8e2190 | 1 | KILLED | killed by: marker-stripped genuine-LE-lengths carrier: want 1 got 0 |
| M40 | CLAUSES tuple drops projection_ok (rerun clause unconjoined) | 1d3cc8f8ca59ef7c | 1 | KILLED | killed by: oracle-only fabrication with re-minted evidence id: want failing clause 'projection_ok', failin |
| M41 | CLAUSES tuple drops evidence_id_ok | 432b75331ad8a6ac | 1 | KILLED | killed by: evidence id stale after an edit: want failing clause 'evidence_id_ok', failing=['projection_ok' |
| M42 | provenance: scratch segment test dropped | b3b2abcaefb3e0c0 | 1 | KILLED | killed by: foreign scratch provenance (/kaidoku-r39/): want 1 got 0 |
| M43 | nonregular_unpublished_ok: root-known test dropped | b001903ba04e79cf | 0 | SURVIVED | SURVIVED, clause-level only: nonregular_unpublished_ok True when root unknown; conjunction still red via oracle_hits_ok |
| M44 | oracle_hits equality loosened to one missing file | d855b7c42dc08e2e | 1 | KILLED | killed by: oracle file missing from the published set: want failing clause 'oracle_hits_ok', failing=['pro |
| M45 | operation_ok: operation/provider test dropped | 6bac7aff728fec2f | 1 | KILLED | killed by: wrong operation (extract_filesystem): want 1 got 0 |
| M46 | layout_ok ORs the BE magic (loosened gate) | af52f032f3dbe5b6 | 1 | KILLED | killed by: marker-stripped genuine-LE-lengths carrier: want 1 got 0 |
| M47 | layout probe: bytes_used sanity branch skipped | 951d16cb5c948859 | 1 | KILLED | killed by: bytes_used beyond the file: want failing clause 'layout_ok', failing=['carve_ok'] |
| M48 | carrier_present forced true | 4bda7e05d33ec91c | 1 | KILLED | killed by: carrier listed but never committed: want failing clause 'carrier_present', failing=['carrier_pi |

Per-mutant rows: `results/table.md` (same content). "Killed by" is the first failing case name the selftest printed; a failing-clause mismatch is noted in the row where it shows.

## Suggested selftest additions for the port (one line each)

- compression id 2/3/5 carrier, expect `layout_ok` red (M06; requires the port's `== 4` gate).
- superblock minor 1, expect `version 4.1 is not 4.0` (M03).
- `bytes_used = len(raw)+1` layout probe, expect reason `bytes_used outside` (M10).
- both-identity length header, expect `ambiguous` (M12).
- silent-rule row with no third column, expect `gaps_ok` red (M21).
- external carve with trailing bytes past `length == bytes_used`, expect `carve_ok` red (M34).
- post-freeze `git mv` of a frozen non-read path, expect exit 2 `frozen_path_changed` (M28).
- missing xpin in the counter's tree, expect exit 2 `Unevaluable` not 1 (finding 8).
