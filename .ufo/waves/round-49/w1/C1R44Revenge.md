# C1R44Revenge — R49-C1 pre-freeze attack (wave 1, seat C1R44Revenge)

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`.
Read-only on the lane; scratch `/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge` (removed at yield after copying
receipts here). Receipts: `.ufo/waves/round-49/w1/C1R44Revenge/` (`SHA256SUMS.txt` lists every file).
No tool installed or upgraded; existing `unblob`, `sasquatch`, `/usr/bin/unsquashfs`, `npx`
(`rea-agents@6.5.0` from the npx cache at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`) were used as found.

## 1. Verdict

**DO NOT FREEZE the R49-C1 draft as written.** The draft counter is the round-44 counter with its
strings renamed and nothing else (`diff` of the two files differs only on 15 round-number lines (one hunk per line);
both 3374 lines). It inherits the round-44 provenance defect, and that defect is not hypothetical:
a real REA 6.5.0 run's receipt, relabelled, passes every carrier clause and the claim exits 0.

- **Satisfiable by forgery (decisive).** Take the committed round-44 `after.json` of each carrier,
  rewrite `parameters.output_directory` to a `/fast/scratch/hyaku/kaidoku-r49/…` path, re-mint
  `evidence_id` with the frozen xpin tool (public), commit after the freeze, and add the three
  landing blocks. The counter with the **real** `npx rea-agents@6.5.0` rerun returns
  `carriers_matched 4`, every carrier clause true, `met_target true`, exit 0 (receipt
  `receipts/C-met-forged-real-rerun.json`, `exit` file `EXIT=0`). The plan's own do-nothing control
  CTL-C1-4 ("copy last round's run") is red only because the copy keeps `/kaidoku-r44/`; the one-field
  edit is green.
- **Plan/counter disagreements repeated from round 44:** the committed-path-is-not-the-output-directory
  sentence is not implemented (scratch paths containing `corpus/evidence/round-49/c1/<id>` pass);
  `provenance_ok` is substring containment, not "inside the segment" (`/tmp/kaidoku-r49/x` and
  `/home/…/kaidoku-r49/x` pass); `gaps == []` / `unpublished_entries == []` / "any diagnostic is a
  failed carrier" are not enforced (a non-removal diagnostic and a fifo `unpublished_entries` row
  pass whenever the rerun reproduces them); the runner-binding clause (`provenance.json`,
  verbatim tree copy) is unread by the counter; the freeze walk ignores **added** files under the
  frozen directory `tools/round-49/`, against the sentence "no commit touches `tools/round-49`".
- Counter-level controls I ran behaved as the plan says: do-nothing at the freeze gives
  `carriers_matched 0` with all six documentation bindings false; the plain round-44 copy gives
  `carriers_matched 0` with only `run_provenance_ok` false (CTL-C1-4 red for the shortcut as written).

Kill-rule note for L1: the forged variant is a counterfactual that reaches `carriers_matched == 4`
with every binding true (exit 0). I did not run a CTL-C1-4 *variant* in the lane's own control
driver; by the plan's kill rule ("any counterfactual red control reaching 4 with every binding true
stops C1") this result must be adjudicated before the freeze. My recommendation is that it fires.

## 2. Why round 44 stopped, from bytes (clause table)

Method: each plan fragment mapped to the counter function and line in `tools/round-44/c1-counter.py`
(R44) and `.ufo/waves/round-49/draft/tools/round-49/c1-counter.py` (R49). Both files are 3374 lines;
the function/line numbers below are identical in both (verified by `grep -n`). Verdicts: **agrees**,
**disagrees**, **unchecked** (plan says it; no code reads it). Round-49 defects are the rows marked
disagrees/unchecked in the R49 column.

Round-44 root cause (from `corpus/lessons/round-44-verifier-spotcheck.md` §2): the R44 plan wrote the
output-directory clause twice. `plans/round-44-claims.md:34-35` says `output_directory` must name a
`corpus/evidence/round-44/c1/` path; `:137-139` says it must be inside the `/kaidoku-r44/` scratch segment.
`provenance_ok` (line 1176-1182) implements only the second. The round-44 red was the three withdrawn
promotion-document bindings, not the counter's provenance check; the stop was a policy choice made
after two readings disagreed. Round 49 deleted the first sentence, which is correct, but kept the
second with an added claim ("the committed evidence path is not the output directory — that sentence
is the one the counter implements") that the counter does not implement.

| # | plan fragment (R44 / R49) | R44 counter (fn, line) | R44 verdict | R49 counter (fn, line) | R49 verdict | evidence |
|---|---|---|---|---|---|---|
| 1 | carrier bytes hash to pin | `measure` carrier_pin_ok 2035 | agrees | same 2035 | agrees | — |
| 2 | superblock reads frozen magic / s_major / s_minor / endianness | `layout_probe` 1070; `layout_ok` 2043 | agrees | same; R49 adds compression class | agrees (superset) | `SHA256SUMS` carriers.json re-read: magic `hsqs`/`sqsh` matches |
| 3 | carrier is a regular file | `carrier_present` 2034 (mode 100644) | agrees | same | agrees | — |
| 4 | names frozen handler, no failed chunk | `handler_ok` 1928-1929; `chunks_ok` 1930 | agrees | same | agrees | — |
| 5 | publishes every oracle file at exact path, same sha256 and size | `oracle_hits` 1430-1446 (rel, sha, size); `oracle_hits_ok` 1944-1947 | agrees | same | agrees | — |
| 6 | no extra regular file under the root (R49 sentence) | `extra_published` 1458; in `oracle_hits_ok` 1947 | agrees | same | agrees | — |
| 7 | `gaps == []` (R49: "ANY gap … is a failed carrier") | `disposition_check` 1490-1569; `GAP_RULE` 350-365 allows `unpublished-entry` on symlink/fifo/socket and removals; docstring lines 16-18 still say "one unpublished-entry gap … at most one structural depth-limited" while code allows 0 | disagrees (docstring vs code vs plan) | same 1490; `GAP_RULE` 352-364 | **disagrees** (gap allowance table is looser than plan; docstring stale). On the four carriers there are no non-regular rows, so every gap fails — effectively `== []` today | `E4c` depth-limited control red (`structural gaps over allowance {'depth-limited': [1, 0]}`) |
| 8 | `diagnostics` — "any diagnostic is a failed carrier" | `diagnostics` 1351; counted only, line 1949; only the removal typename is consumed (1526-1547) | disagrees | same 1948-1949 | **disagrees** — no clause rejects a non-removal diagnostic | `E4a`: `ChunkSkipped` diagnostic reproduced by REA ⇒ `gaps_ok true`, `projection_ok true`, `matched true`, 4/4 |
| 9 | `unpublished_entries == []` | read only by `projection` 1776/1801 (equality to the rerun); no gate | **unchecked** literal emptiness | same | **unchecked** literal emptiness | `E4a`: fifo `unpublished_entries` row reproduced ⇒ 4/4 green |
| 10 | subject digest equals pin | `subject_pin_ok` 1967-1970 | agrees | same | agrees | — |
| 11 | recomputes evidence id | `evidence_ids` 596-632; `evidence_id_ok` 2128 | agrees as a hash check; **not a provenance barrier** (anyone can re-mint with the public xpin tool) | same | agrees as hash; **satisfiable by forgery** | `E1`: ids re-minted for relabelled envelopes ⇒ `evidence_id_ok true` |
| 12 | first added in a commit descending from FREEZE | `receipt_fresh` 2082-2083 (`is_ancestor(freeze, add)`) | agrees | same | agrees | — |
| 13 | after-receipt at `corpus/evidence/round-49/c1/<id>/after.json` | `AFTERDIR` 246 | agrees | same | agrees | — |
| 14 | counter-time REA rerun has same semantic projection | `make_real_runner` 1859-1915 (`npx -y rea-agents@6.5.0`, line 1882); projection compare 2099-2112; `projection` 1707-1818 (excludes `parameters`, `output_directory`, evidence id) | agrees for content; **unchecked**: rerun binary is whatever `npx` resolves, not the `--pkg65` root the freeze pins (`evidence_ids` checks only `--pkg65`) | same | same | `E1-real` rerun ran through npx; `pkg65` never bound to the rerun |
| 15 | `parameters.output_directory` absolute, "inside" `/kaidoku-r4x/` | `provenance_ok` 1176-1182: `PROV_SEGMENT in od` (substring), isabs, no `..` | agrees for the round-44 claim text; R49 text says "inside" | same 1176-1182 | **disagrees** — `/tmp/kaidoku-r49/x` and `/home/…/kaidoku-r49/x` pass (`E5_provenance_direct`) | `results2.json` `E5_provenance_direct` |
| 16 | "the committed evidence path is **not** the output directory — that sentence is the one the counter implements" (R49) / "output_directory must name `corpus/evidence/round-44/c1/`" (R44 controls) | R44: no clause; R49: no clause | R44 **disagrees** (unimplemented; this is the round-44 dual clause) | **disagrees** (counter does not implement it; scratch path that contains `corpus/evidence/round-49/c1/v1le` passes) | `E5`: `…/kaidoku-r49/C1R44Revenge/x/corpus/evidence/round-49/c1/<id>` ⇒ carriers 4/4 (injected rerun) |
| 17 | runner copies tree verbatim and records `provenance.json` (R49 parenthetical); R44-CL8 runner binding | no reader of `provenance.json`, `extract-tree.tsv`, `run.json` (grep: none in either counter); `c1-run.py` writes them (698) | **unchecked** | same | **unchecked** | `E1` commit holds only `after.json` per carrier ⇒ green |
| 18 | "the rerun proves projection, not which process wrote the receipt" (R49 disclosed limit) | — | disclosed | — | disclosed, but the forgery in row 11/15/16 is a provenance forgery beyond the disclosed limit: the forger does not need a different process, only a renamed path and a re-minted id | `C-met-forged-real-rerun.json` |
| 19 | FREEZE ancestor of REV | not checked explicitly; implied by row 12 only when receipts exist | unchecked explicitly | same | unchecked explicitly (implied; no fixture reaches green without receipts) | — |
| 20 | frozen set = plan + `tools/round-49/` directory + listed round-42/39/27 files + oracle tree | `FROZEN_PATHS` 272-283; `FROZEN_PREFIXES` 286 | agrees on the listed files | same | agrees on files; see row 21 for directory | — |
| 21 | "no commit in FREEZE..REV touches `tools/round-49` (directory)" (R49) / "a file added under it after the freeze is a change" (R44) | `frozen_drift` 1629-1683; A branch 1662-1666 counts `A` only if the path existed at FREEZE | **disagrees** (R44 text explicitly says added files are changes; the counter does not do it) | same | **disagrees** — added file under `tools/round-49/` is not drift | `E3_frozen_drift_added_file` = `[]` for commit `af5b0698…`; `E3_frozen_drift_edited_counter` = `['tools/round-49/c1-counter.py']` |
| 22 | each frozen blob at FREEZE equals blob at REV | `frozen_drift` 1671-1682 (explicit paths only; prefixes covered by the log walk) | agrees | same | agrees | — |
| 23 | `## Round-49 additions to Core` row names squashfs_v1/v2 and cites entry | `province_core_section` 2153-2154; `province_core_row` 2156-2159 | agrees | same | agrees | green in `C-met` run |
| 24 | one line carries "Round-49 frontier note", the stem and a SquashFS v1/v2 token | `frontier_note` 2161-2163 | agrees | same | agrees | green in `C-met` run |
| 25 | entry exists; `source:` cites S138+S139; both rows opened 2026-10-28 and list the entry in used-by | `entry_present` 2164-2165; `sourced` 2166-2185 (opened = SOURCES column 8 date cell, used-by = column 10) | agrees literally; "opened" is the date cell only (R44-CL-over-claim persists) | same | agrees literally | `C-met` green |
| 26 | `corpus/README.md ## Coverage map` maps entry stem | `coverage_map_row` 2186-2189 | agrees | same | agrees | — |
| 27 | `carriers_spec_ok`, endianness/family coverage, frozen tables, oracle tool | 2190-2209 | agrees | same | agrees | — |
| 28 | target `carriers_matched == 4`, bindings, frozen clean, exit 0 | `met_target` 2216-2218; exit 2390 | agrees | same | agrees (and is satisfied by row 11/15/16 forgery) | `C-met-forged-real-rerun.json` |
| 29 | oracle = `unsquashfs -lls` census + unblob `__output__` tree digest | `oracle_rows` 735; `tree_check` 2254 | agrees with my re-derivation (section 4) | same | agrees with re-derivation | section 4 |
| 30 | PROVINCE "append after last line", prefix-preserved (R44 plan) | not implemented in either counter | R44 unchecked | R49 plan dropped the prefix sentence; counter does not check PROVINCE prefix | unchecked (plan removed the requirement; SHONEN line pointers can drift) | — |
| 31 | CTL-C1-0 do-nothing at freeze ⇒ exit 1, carriers 0, doc bindings false | `main` 2369-2403 | — | same | agrees (measured, `receipts/dn.json`: `carriers_matched 0`, six doc bindings false) | `dn.json` |
| 32 | CTL-C1-4 copy last round's run ⇒ red | `provenance_ok` | — | same | agrees as written (red via `run_provenance_ok` only); **defeated** by a one-field relabel (row 11/15) | `B_plain_copy_clauses` red; `E1` green |

Round-44 repeat count: rows 7, 8, 9, 11, 14, 15, 16, 17, 21 are the same defects R44 named (R44-CL2, CL3,
CL7, CL8, and the cited "no freeze-set" class) and remain open in the draft. Row 11/15/16 together are
R44-CL2 and R44-CL3 (projection-matched authored envelope), unrepaired.

## 3. Findings (defects that would repeat round 44)

| id | severity | finding | exact command / fixture | exit | differing value |
|---|---|---|---|---|---|
| F1 | blocking | Relabelled real-run receipts + re-minted id + landing blocks ⇒ `met_target true`, exit 0 with the **real** REA rerun | `python3 -I -B <clone>/tools/round-49/c1-counter.py --root <clone> --rev 05c049d019fde22f5def3ff457b0c3686a012b43 --freeze 5a71eaf0d23c6f2d43fa8262bda526ab157490c0 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work … --json-out …` ; fixture commit `05c049d0` (parent `9eb3b8d7`, the re-minted relabel commit; the plain-copy control is `418434d7`, the stale-id relabel `1b8af5f4`) | **0** (`receipts/C-met-forged-real-rerun.exit`) | `carriers_matched 4`, `failing []`, `bindings_false []`, `met_target true`; forged receipts `forged-receipts/*-after.json` (`parameters.output_directory` = `/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/relabel/<id>/rea-out`) vs round-44 `…/probe-R44C1Run/…` |
| F2 | blocking | `provenance_ok` is substring containment; the claim's "committed path is not the output directory" is unimplemented; `E5` scratch path containing `corpus/evidence/round-49/c1/<id>` passes | `provenance_ok(...)` direct calls, `receipts/results2.json` `E5_provenance_direct`; `E5_committed_path_in_scratch` (injected rerun) | n/a (function) / 0 for measure | `/tmp/kaidoku-r49/x: true`, `/home/…/kaidoku-r49/x: true`, `…/kaidoku-r49/x/corpus/evidence/round-49/c1/v1le: true` |
| F3 | blocking | Freeze walk ignores added files under the frozen directory `tools/round-49/` | branch `e3add` commit `af5b0698ce2e402cacf968f38a1d53f387dc275d` adds `tools/round-49/zz-added-after-freeze.txt`; `M.frozen_drift(clone, F, e3add, spec_at_F)` | `[]` (plan requires a touch of the directory ⇒ drift) | `frozen_drift == []`; control edit of `c1-counter.py` ⇒ `['tools/round-49/c1-counter.py']` |
| F4 | major | Non-removal `diagnostics` and `unpublished_entries` rows are accepted when REA reproduces them (plan: "ANY gap or diagnostic is a failed carrier"; `unpublished_entries == []`) | harness2 `E4a` / harness3 `A_diag_fifo_reproduced`: `diagnostics=[{'report':{'__typename__':'ChunkSkipped'}}]`, `unpublished_entries=[{'kind':'fifo',…}]`, provenance fixed, rerun = same | counter `carriers_matched 4` (A) | `gaps_ok true`, `projection_ok true`, `matched true` ×4. Not-reproduced variant is red (`projection_ok false`, `A_diag_fifo_not_reproduced`) so only a real-REA-produced diagnostic passes |
| F5 | major | Runner binding unchecked: committed receipts need only `after.json`; `provenance.json`/`extract-tree.tsv`/`run.json` unread | `E1` commit contains only `corpus/evidence/round-49/c1/<id>/after.json` (`git show --stat`) | green (F1) | — |
| F6 | major | Rerun is `npx -y rea-agents@6.5.0` (line 1882), not the `--pkg65` root that `evidence_ids` verifies against the freeze; the rerun's binary identity is unbound | code read `make_real_runner` 1859-1915; rerun used npx cache `ad9a3fdbcad992c6` (the same path, not verified) | n/a | — |
| F7 | minor | Gap rule docstring (lines 16-18: "at most one structural depth-limited") contradicts `GAP_RULE` 364 (`0`) and the plan (`gaps == []`); `GAP_RULE` 352-355 allows gap kinds that the plan forbids | code read | n/a | `depth-limited: 1` vs `0` |
| F8 | minor | FREEZE-is-ancestor-of-REV is not checked explicitly (only implied via receipt_fresh) | code read `measure` 2082-2083 only | n/a | — |
| F9 | minor | Landing draft `block-c` (`R49C1Doc/block-c-readme-coverage-map-row.md`) carries a literal `<AFTER-DATA: …>` marker; the marker must not land (the counter does not reject it) | file read | n/a | — |
| F10 | minor | PROVINCE prefix-preservation (R44 plan) is dropped in the R49 plan and unchecked by the counter; SHONEN pointers can drift | plan diff vs `plans/round-44-claims.md:143-144` | n/a | — |

Not run (stated, not passed): the lane's `c1-controls.py` / `run-ctl.sh` driver (CTL-C1-1, -2, -3, -5, POS) and
the counter's `--selftest`; the R49C1 data run (forbidden for seats); the C2 counter.

## 4. Oracle re-open (independent of the counter)

`/usr/bin/unsquashfs` (4.7.5, sha256 `461e1fd9…1677c`) re-run on the four committed fixtures
(`unsquashfs -d <scratch>/unsq/<id> <carrier>`, exit 0 for all four): live regular-file census equals
the frozen census (path, size) for every carrier; live member sha256 digests reproduce the frozen
`output_tree_digest` (v1le/v1be `8faae7739b14315c…2a48`, v2le/v2be `4178bb8379de3e55…f947`, matching
`carriers.json` `oracle.output_tree_digest`); carrier sha256 equals the pin; magic `hsqs` (le) / `sqsh`
(be) matches. The frozen oracle is correct; the defects above are in the receipt-side predicate, not in the oracle.

## 5. Plan sentences that disagree with each other (for the L1 to resolve before the freeze)

1. `P49-C1` "the committed evidence path is **not** the output directory — that sentence is the one the
   counter implements" vs the counter (row 16). Either implement (exact-path rules, reject
   `corpus/evidence` inside the output path) or delete the sentence and disclose that output-directory
   provenance is a label, not a witness.
2. "gaps == []" and "unpublished_entries == []" and "any diagnostic is a failed carrier" vs the counter's
   gap allowance table and absent diagnostic/unpublished clauses (rows 7-9, F4).
3. "no commit in FREEZE..REV touches `tools/round-49` (directory)" vs `frozen_drift` A-branch (row 21, F3).
4. "absolute path inside the `/kaidoku-r49/` scratch segment" vs `PROV_SEGMENT in od` (row 15, F2).
5. The runner clause (`provenance.json`, verbatim copy) is described but not bound (row 17, F5).

## 6. Recommendations (for the L1 — not patches)

- Before the freeze, either (a) bind the receipt to runner-written artifacts (`run.json` stdout sha256,
  `provenance.json`, `extract-tree.tsv` with the committed tree equal to the scratch tree) and require
  `output_directory` to match the runner's pattern exactly, or (b) state in the claim and the lesson that
  C1 proves carrier **content** equal to a fresh REA run, not that the committed receipt was produced by
  the L1's runner; the relabel shows (b) is the only honest reading of the current counter.
- Make `diagnostics == []` and `unpublished_entries == []` explicit clauses; reject any `A` under the frozen
  directory in `frozen_drift`; pin the rerun to the `--pkg65` root; add an explicit FREEZE-ancestor check.
- Add CTL-C1-4 variants as controls: (i) the one-field relabel (`E1`/`C-met`) must be red; (ii) a
  reproduced non-removal diagnostic must be red. Both are red under the fixes above; neither is red today.
- Under the plan's own kill rule, F1 is a counterfactual reaching 4/4 with every binding true. Decide before
  any data run.

## 7. Tools, provenance and reproduction

- Clone: `bash .ufo/waves/round-49/draft/mkclone.sh /fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/clone` →
  `DEV_FREEZE=5a71eaf0d23c6f2d43fa8262bda526ab157490c0` (draft tools + plan committed in the clone only,
  identity `r49-dev`; `git rev-parse --show-toplevel` asserted equal to the clone path before every commit).
- Branches in the clone: `plainE2` `418434d7…`, `relabelE1` `1b8af5f4…` (stale ids), `9eb3b8d7…` (re-minted),
  `e3add` `af5b0698…`, `e3mod`, `e4b`, `e4c`, `e5`, `met` `05c049d0…` (= `C-met`).
- Harness: `harness.py` (E1/E2), `harness2.py` (E3, E4, E4c, E5, provenance, oracle re-open), `harness3.py`
  (A-fixed, B, C). Counter loaded in-process with `importlib` from the clone's `tools/round-49/c1-counter.py`
  (`sha256 d6d70cb7…779`). In-process `measure(..., rerun=…)` injects a rerun returning the committed round-44
  envelope (a genuine REA output; its projection was counter-verified in round 44); every claim that depends on
  the rerun is also checked with the real `npx` rerun (`receipts/E1-relabel-real-rerun.*`,
  `receipts/C-met-forged-real-rerun.*`).
- Exit codes: CLI runs (`real`, `real2`) recorded exit 1 (E1: docs absent) and 0 (C-met). In-process
  `measure` results are booleans (`met_target`), mapped to 0/1; no `2` (could-not-evaluate) occurred.
- `forged-receipts/met-landing.patch` is my quick landing (PROVINCE/README/SOURCES/entry from the round-49
  landing drafts); the L1's landing will differ in text but bind the same way.
- Receipts and hashes: `SHA256SUMS.txt` (27 entries, including the draft counter `d6d70cb7…`, round-44 counter
  `9f2cc140…`, draft plan `984e1026…`, round-44 plan `369a6201…`, carriers.json `829e3392…`, c1-run.py
  `f9161ff3…`, c1-run.sh `5ebb453f…`, round-44 spot-check `eb075d01…`, round-44 lesson `d09e415e…`).
- Disk guard: `/fast/scratch/hyaku` 516 G free before the heavy pass.
- Scratch `$S` removed at yield after copying receipts.

Confidence: high on F1-F3 (reproduced by the real rerun and by function calls on committed fixtures);
medium on F6 (npx resolution not inspected beyond the cache directory); high on the clause table (every
row cites a function line verified by grep in both counters).
