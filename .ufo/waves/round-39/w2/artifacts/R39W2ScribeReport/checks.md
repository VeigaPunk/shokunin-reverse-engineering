# R39W2ScribeReport — checks actually run

All commands ran in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only git + local Python
over committed bytes). No REA run, no counter run, no unblob run, no scratch tree, no tool install,
no VCS mutation. `TMPDIR` was not used; the three throwaway files written to `/tmp` (`s_base.md`,
`s_6f.md`, `s_head.md`, all < 20 KB) were removed after use.

## C0 — commit shapes

```
git log --oneline -12
git show --stat --format='%H%n%an <%ae>%n%ad%n%s' <sha>        # 5 shas + e40a25df
git show --stat --format='' <sha> | tail -1                    # totals
```

Totals as recorded in `report-body.md` (`## Landed changes`): 8fcda41c 1277/98390+; 72359309
22/1430+; 3c07eed7 101/16613+; 6fdaf4f1 16/841+; 52b0eb29 18/1355+ 5-; e40a25df 3/1116+.
`git show --stat --format='' 8fcda41c -- SKILL.md` → `SKILL.md | 29 +`. Freeze name list (minus
`w1/`) confirms: claims doc, 8 tools + `c1-run.sh`, selftest fixtures, `carriers.json`, census,
K1–K4 symlink tables, K5/K6 carriers+oracles+src, triage entry, `SKILL.md`, `corpus/README.md`,
`corpus/SOURCES.md`.

## C0b — worktree state (read-only observation)

`git status --porcelain` at 14:41 with HEAD `e40a25df`: four modified/deleted wave-1 paths
(`w1/R39C1IndepReader.md`, `w1/R39C1SymlinkK1K4.md`, `w1/artifacts/R39C1SymlinkK1K4/{evidence/carrier.sqsh (deleted),symlink-tables.py}`)
plus untracked wave-2 dispatch files and `w2/`. Not mine; recorded also by
`w2/artifacts/R39W2Sentinel/08-w1-drift-diff.txt`. Every check below reads `git show <rev>:<path>`,
so none of it depends on the worktree.

## C1 — SOURCES rows by tier/status

```
git show a2f64e1d:corpus/SOURCES.md > /tmp/s_base.md
git show 6fdaf4f1:corpus/SOURCES.md > /tmp/s_6f.md
git show HEAD:corpus/SOURCES.md     > /tmp/s_head.md
grep -c '^| S[0-9]' /tmp/s_{base,6f,head}.md
awk -F'|' '/^\| S[0-9]/{tier=$5; status=$9; gsub(/ +$/,"",tier); gsub(/ +$/,"",status); ...}'
git diff --stat a2f64e1d:corpus/SOURCES.md HEAD:corpus/SOURCES.md
```

Rows: base 117, 6fdaf4f1 122, HEAD 122. Tier: A 109→114, B 7→7, C 1→1. Status: mined 112→117,
rejected 5→5. Kind `code`: 31→36. Diff: `1 file changed, 5 insertions(+)`; the five added lines are
S118–S122, each `| S1xx | ... | code | A | ... | mined | 2026-10-26 | ...`. `git show
8fcda41c:corpus/SOURCES.md | grep -c '^| S[0-9]'` → 121 (S118–S121 landed at the freeze; S122 at
6fdaf4f1).

## C2 — frozen paths and the triage block

```
git diff --stat 8fcda41c 6fdaf4f1 -- plans/round-39-claims.md tools/round-39/c1-counter.py \
  tools/round-39/c1-run.sh tools/round-39/c2-counter.py tools/round-39/sqfs-triage.py \
  tools/round-39/heldout-gen.py .ufo/waves/round-39/c1/carriers.json SKILL.md
```
→ empty output, rc 0. (A wider pathspec that included `corpus/evidence/round-39/c1/K{1..6}` lists only
the 12 *added* `after.json`/`run.json` receipts, which are claim data, not frozen inputs.)

```
git show 8fcda41c:SKILL.md | awk '/sqfs-triage-table v1/{f=1} f&&/^\s*\| clean \|/{print;exit} f' | sha256sum
git show HEAD:SKILL.md     | (same)
```
→ `735595030e11584835551095d76e94eca90d4b24ae1ba214646d3dfd273d3438` both times.

## C3 — carrier pins (my own recomputation)

Python: read `.ufo/waves/round-39/c1/carriers.json`, and for each of 6 carriers take
`path`/`sha256`, `oracle`/`oracle_sha256`, `symlinks`/`symlinks_sha256`; `git show <rev>:<path>` and
sha256 the bytes; compare. Revisions `8fcda41c` and `6fdaf4f1`.

→ 18 pinned files × 2 revisions = 36 comparisons, **0 mismatches**.

## C4 — C1 receipts

Python over `corpus/evidence/round-39/c1/K{1..6}/after.json`: `subject.digest.sha256` equals the
carrier pin for all six; `parameters.output_directory` contains `/kaidoku-r39/` for all six;
`operation == extract_firmware`; `provider == Unblob 26.6.4`. Handler string per receipt:
`squashfs_v4_be` only. Gap kinds present: K2/K5/K6 `unpublished-entry` (1/2/1 — equal to in-tree
link counts), K1/K3/K4 none; no gap of any kind for the escaping links (K1 1, K5 1, K6 2).
`unpublished_entries` rows (kind `symlink` + `link_target`) exist only for the in-tree links:
K5 `firmware.bin_extract/usr/share/demo/link-{blob,notes}`, K6
`firmware.bin_extract/a/b/link-in`; K1/K3/K4 have none. `"kind": "file-offset-range"` occurrences are
`evidence[].locations[]` entries, not gaps.

## C5 — held-out set

Python over `corpus/evidence/round-39/c2/heldout/manifest.json`: 20 carriers, 2 per each of 10
classes; `seed == 8fcda41c…`; generator `heldout-gen.py` v`r39-c2-v1` sha `8b3eddf8…`. For each
carrier: sha256 of the committed `carrier.sqsh` equals the manifest pin; the manifest pin appears in
`Hxx/envelope.json`; `label` equals the frozen class→label map. → 20 carriers, **0 anomalies**.

## C6 — scores

`python3 -c` over `.ufo/waves/round-39/l1/scores/*.json`:
`c1-at-6fdaf4f1`: `carriers_matched 6`, `target 6`, `met_target true`, `carriers_unchanged true`,
`frozen_path_changed []`, `bindings_false []`.
`c2-at-6fdaf4f1`: `n 20`, `matched 20`, `bindings_ok true`, `bindings_false []`,
`frozen_paths_changed []`, `triage_table_identical true`, `seed_matches_freeze true`,
`regenerated_seed_matches_freeze true`, `generator_sha_matches_freeze true`.
`c1-at-base`: `unevaluable "carriers.json absent at freeze"`. `c2-at-freeze`:
`unevaluable "no_manifest_at_rev"`.

Exit-code map read from source: `tools/round-39/c1-counter.py:586` → `0 if met_target else 1`;
`tools/round-39/c2-counter.py:165` raises `Unevaluable('no_manifest_at_rev')`,
`:425-435` returns 2, and `:443` is the normal map (`0 if met_target else 1`).

## C7 — controls

```
ls .ufo/waves/round-39/controls/          # 9 ctl-c1-*.json + 9 .log, ctl-c2-dev-scores.json, tables/
python3 -c ... ctl-c1-*.json ...          # control/rev/freeze/counter_exit/expected_exit/verdict/matched
python3 -c ... .ufo/waves/round-39/w1/artifacts/R39C1Controls/evidence/suite.json ...
git cat-file -e <each control rev>        # all absent from the lane
```

Landed C1 receipts: CTL-C1-0 (raw counter JSON, no control/exit fields), CTL-C1-1/2/4/6/7/8/9
(counter_exit 1, as-expected), CTL-C1-3 (counter_exit 1, expected 0, `unexpected-exit`, matched 6,
`frontier_note false`). No `ctl-c1-5.json`.
Wave-1 suite: 10 keys `CTL-C1-0..9`; CTL-C1-5 at `rev == freeze == bc533dda51015ae13fb11c8177e8d2f1a45fbd0a`,
`mode in-freeze`, counter_exit 1, matched 0; CTL-C1-3 counter_exit 0, expected 0, matched 6.
`git cat-file -e` on `bc533dda…`, `aa7a7a03…`, `8e1aea55…`, `26d0841a…` → all ABSENT (fixture clones,
not lane history).
`ctl-c2-dev-scores.json` `controls` keys: CTL-C2-0-base-SKILL (exit 2, 0), FREEZE-table-informational
(exit 0, 20, `met_target true`), CTL-C2-1..4 (exit 0; 4/6/10/6), CTL-C2-5 and CTL-C2-6 (exit 2, 0),
CTL-C2-5.formatfix (8), CTL-C2-6.formatfix (12).

## C8 — census, frontier, wave records

```
cat .ufo/waves/round-39/census-start.txt          # 13 lines: 11 W04 + ok line + exit 0
grep -n 'Round-39' PROVINCE.md                    # :378 section, :384 frontier note
grep -n 'r39-be-squashfs-v4-core' corpus/README.md  # :93, :203, :245
git ls-tree -r --name-only <rev> corpus/knowledge | wc -l   # 127 / 128 / 129 at base/freeze/HEAD
grep -c '^| `2026-' corpus/README.md              # 113 base, 115 HEAD
grep -n 'Round 39\|round-39' LOG.md SCORECARD.md  # only SCORECARD.md:3410 (round-38 "planned (round 39)")
python3 -c ... w1-spec/w2-spec/r39-w1-results.json  # 43 / 39 items; 43 results
```

`r39-w1-results.json`: 43 seats, 43 results; verdict strings 20 `DONE`, 14 `DEFECTS FOUND`,
4 `CONFIRMED`, 5 non-scalar (`R39C1SymlinkK1K4` "DEFECTS FOUND — …", `R39SrcUnblobSymlink` "DONE. …",
`R39C2ReconDep` "DONE — …", `R39C2LabDeterminism` dict-valued verdict, `R39Quarantine` "CONFIRMED for
the slice. DEFECTS FOUND …").

```
git ls-tree --name-only 8fcda41c -- .ufo/waves/round-39/w1/ | grep -c '\.md$'   # 43
```
Set comparison of the 43 `w1-spec.json` item names against the 43 top-level report stems in the freeze
tree → no missing seat. (93 `*.md` under `w1/` once artifact markdown is counted.)

## C9 — registry / self-tests / QUALITY

```
grep -n 'c2-counter\|absence-sweep\|round-39' SKILL.md      # :331; :1292 (round-36); :1328-:1354 registry
sed -n '1328,1354p' SKILL.md | grep -c '^| `tools/'         # 22 rows, last row :1354, none after
grep -n '^| 82 |' corpus/QUALITY.md                         # :90
grep -n 'selftest' tools/round-38/{freeze-drift.py,intended-doc.py,registry-immutable.sh}
```
Registry rows include `tools/round-39/c2-counter.py` (`SKILL.md:1353`) and
`tools/round-39/absence-sweep.py` (`:1354`). `--selftest` entry points exist at
`tools/round-38/freeze-drift.py:49`, `intended-doc.py:45`, `registry-immutable.sh:22`.
