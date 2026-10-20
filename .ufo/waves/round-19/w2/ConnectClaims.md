# ConnectClaims — C1, C2, C3 causal separability

Axes attacked: calibration (does one claim's stated count require another's fix), freshness (do C2's pin and census counters move when C1 or C3 artifacts move), depth (does C3's mechanism count survive C1's validator edit).

Observed main tip: `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (`refs/heads/main`, "round-19: wave-two fixes — list identity, alias classifier coverage, strict replay, scope and source qualifications"). An earlier read of `refs/heads/main` in this seat returned `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; the tip moved before the clone. Every measurement below is at `279e8b1` or at a commit whose parent is that tip. Baseline B = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. Freeze `a1140e76fffdc1be032d9d813dbb686157803bbc` is an ancestor of integration `4f6c73f81ae8d31de18377d7ff57e4e10140ce48` (`git merge-base --is-ancestor`, exit 0).

No tools installed. No lane file was edited except this report. Mutations are commits in `/tmp/kr19-ConnectClaims-X0pHsY` only (`git rev-parse HEAD` there = `279e8b19c51658bfd05b9e31a1c0894ab2e70537` before the commits).

## Answer

The three scored counters are causally separable. Restoring C1's validator bytes reopens only `R18-MIDMAP-LISTSTEP`. Restoring C2's PROVINCE text and the two SKILL census lines reopens only the pin mismatch and the four stale census blocks. C1's checker never reads C3 run artifacts.

One reading of C3 is not separable from C1. `predictions/decision-rule.json:3` says a label counts only if `receipt-validate.py --require-mid-maps` exits 0. At the tip that command exits 1 on all eight receipts, and the only findings are the sha256 and size of `.ufo/waves/round-17/tools/receipt-validate.py`. Those receipts pin the pre-fix bytes (`70672eb3…`, 46047), which are the bytes at B and at `a1140e7`. C1's list-step fix, and the later identity edit at `279e8b1`, replace that file (tip `6afb7ef6…`, 52682). The object-shaped `steps` on these receipts never enter the list branch, so the behavioral fix is not what fails the gate. The byte replacement is. Landing C1's substance fix and satisfying that frozen sentence on one tree are mutually exclusive.

`decision-rule.json:6` also counts "a bound retained log and a compare.json". Eight `compare.json` files are in the tip tree, and eight retained validations are exit 0. Those retained files were produced by the split named in the knowledge entry: corrected code, producer bytes restored at the pinned path. The frozen sentence was not updated when the path's bytes changed.

## What each claim's checker actually reads

[OBSERVATION] `routed-r18.py` substance functions (`tools/routed-r18.py:92`, `:120`, `:167`, `:204`, `:236`, `:263`, `:285` at `279e8b1`): mid-map loads REV's `receipt-validate.py`; digest hashes the blob at `9011581`; strict-baseline replays a retained round-18 tool; head-aliases and registry read `SKILL.md` rows; install-record reads `corpus/lessons/round-19.md` `## Installs`. None read `PROVINCE.md` or `.ufo/waves/round-19/runs/`.

[OBSERVATION] `province-pins.py` reads `PROVINCE.md` at REV (`tools/province-pins.py:244-272`) and the live client configs. Historical clauses are those whose sentence contains "historical" (`:96-97`, `:187-188`). It does not read the validator or the runs.

[OBSERVATION] `c1-census-v10.py` SCOPE for the shared files is `PROVINCE.md` 8-13, 15-26, 44; `SKILL.md` 10-16 and 18-20; `SCORECARD.md` through 2122 (`.ufo/gates/c1-census-v10.py:254-263`). The gate file is not in the B..tip diff. The name is the historical gate name; round-19 C1 does not edit it. `claims.json:37-39` already separates the two undeclared blocks (SCORECARD 2380-2382, SKILL 511-519) from the freshness edit.

[OBSERVATION] B..`279e8b1` shared-text hunks: PROVINCE stays 162 lines, edits at 8-12, 15-19, 21-22, 24-26, 44, 47. SKILL census-range edit is only lines 18-19 (6.5.0 → 6.7.0). Later SKILL hunks start at 448 (registry / carried rows) and, in `279e8b1`, at 542, 579, and the insert at 601-619. SCORECARD's only hunk is an append at 2472 (+32). Those appends sit past the census end line 2122, so they do not renumber scoped rows.

## Tip measurements (clone tree = `279e8b1`)

```
python3 -I -B /tmp/kr19-ConnectClaims-X0pHsY/.ufo/waves/round-19/tools/routed-r18.py \
  --root /tmp/kr19-ConnectClaims-X0pHsY --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
```
exit 0. `open_count` 0, `named_open` 0, `substance_open` 0. All seven defects `named` true and `substance` true.

```
python3 -I -B /tmp/kr19-ConnectClaims-X0pHsY/.ufo/waves/round-19/tools/province-pins.py \
  --root /tmp/kr19-ConnectClaims-X0pHsY --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
```
exit 0. `mismatch_count` 0, `unstated_clients` []. Stated pins are Devin/OMP/Kimi 6.7.0 at PROVINCE lines 9, 16, 17, 18, 44. Line 12's `rea-agents@6.5.0` is not extracted.

```
python3 -I -B /tmp/kr19-ConnectClaims-X0pHsY/.ufo/gates/c1-census-v10.py \
  --root /tmp/kr19-ConnectClaims-X0pHsY --quiet
```
exit 1. `VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)`. Line counts PROVINCE 162, SCORECARD 2503, SKILL 619. This matches the amended C2 sentence (`claims.json:39`): stale 4 → 0, undeclared stays 2, PASS is not claimed.

```
git --no-optional-locks ls-tree -r --name-only 279e8b19c51658bfd05b9e31a1c0894ab2e70537
```
exit 0. Paths ending in `.ufo/waves/round-19/runs/<label>/compare.json`: 8.

[OBSERVATION] All eight `runs/t1250-*/receipt.json` have `"steps"` as an object with keys `analyze` and `inspect-go-binary` (vet receipt `:1919-1920`). The list branch (`receipt-validate.py:614-621`) is not taken for them. The dict branch (`:611-613`) only asks that `steps["analyze"]` carry `pin_checks`.

[OBSERVATION] Each receipt's `pins_pre` and `pins_post` record `.ufo/waves/round-17/tools/receipt-validate.py` as sha256 `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145`, size 46047 (vet `pins_post` entry at `:1103-1106`, `pins_pre` at `:1122` / `:1869-1872`). Content sha256 of that path:

| rev | content sha256 | size |
|---|---|---|
| B and `a1140e7` | `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145` | 46047 |
| `4f6c73f` and `d0690fd` | `9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45` | 51075 |
| `279e8b1` | `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762` | 52682 |

The same scan of every lane path in all eight pin maps found no other drift. `receipt-validate.py` is the only pinned lane file whose tip bytes differ from the receipt. It is also the only round-17 tool in the B..tip name list.

[OBSERVATION] Invoking the tip `receipt-validate.py --require-mid-maps` on each of the eight receipts (subprocess return codes): exit 1, 2 findings, codes `{sha256_mismatch, size_mismatch}`, path the lane `receipt-validate.py`. Vet's finding records expected `70672eb3…` / 46047 and actual `6afb7ef6…` / 52682 (`where` `pins_post.entries.…receipt-validate.py`). `validate_receipt` sets `"valid": not findings` (`receipt-validate.py:656`). `validate_paths` returns 1 when any receipt is invalid (`:689-694`).

[INFERENCE] If that path held the expected bytes, those two findings would be absent, `valid` would be true, and the exit would be 0. This seat did not write the lane path to observe that exit (lane writes are out of contract). A prefix remap onto a temp copy of the B bytes produced extra `mid_map_compare_mismatch` findings whose recomputed `missing` list was the lane path plus the temp path; that mismatch is an artifact of changing the path key, not of the B bytes.

[OBSERVATION] Retained `evidence/receipt-validation/t1250-{go,gofmt,asm,cgo,compile,cover,preprofile,vet}.json`: each `exit` 0, `counts` `{invalid:0, receipts:1, unreadable:0, valid:1}`, `require_mid_maps` true. Knowledge entry `:46` states those runs used the corrected validator from an extracted file while the producer's original bytes were restored at the recorded path, and that validation against today's file reports the sha256/size mismatch. SKILL `:615` records the same rule: recheck against producer snapshot bytes or retain the original validation; do not rewrite the receipt.

The runs and the first validator-byte change landed in one commit: `4f6c73f` (2026-10-20 16:09:17 -0300), which is the commit that adds `runs/t1250-vet/receipt.json`. At that tree the receipt already pins B bytes and the blob is already 51075. No commit contains both the receipts and a `receipt-validate.py` blob equal to the pin. `279e8b1` changed the file again (list identity: `_is_analyze_step` and `len(named) == 1`).

## Mutation M1 — undo only the validator bytes

Clone commit `ac517eb159b35ec826e3ecb09f5ddecda129eac2`, parent `279e8b1`. `git checkout 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 -- .ufo/waves/round-17/tools/receipt-validate.py` then commit. Worktree content sha256 `70672eb3…`, size 46047.

```
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-ConnectClaims-X0pHsY --rev ac517eb159b35ec826e3ecb09f5ddecda129eac2 --strict
```
exit 1. `open_count` 1, `named_open` 0, `substance_open` 1. Only `R18-MIDMAP-LISTSTEP` substance false: "list-shaped receipt with pin_checks only on a non-analyze step is accepted". The other six stay substance true, including `R18-VALIDATOR-DIGEST` (it hashes `9011581`'s blob, not the working-tree file).

```
python3 -I -B .ufo/waves/round-19/tools/province-pins.py --root /tmp/kr19-ConnectClaims-X0pHsY --rev ac517eb159b35ec826e3ecb09f5ddecda129eac2 --strict
```
exit 0. `mismatch_count` 0.

```
python3 -I -B .ufo/gates/c1-census-v10.py --root /tmp/kr19-ConnectClaims-X0pHsY --quiet
```
exit 1. `VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=2 unresolved=0)`. Census does not read the validator. C2's counters did not move.

[OBSERVATION] The same commit's `receipt-validate.py --require-mid-maps` on the vet receipt still exited 1, and the finding's `actual_sha256` was `6afb7ef6…` (the lane tip blob), not the clone's restored bytes. The receipt stores the absolute lane path (`runs/t1250-vet/receipt.json:60` and the pin entries). Restoring the clone does not restore the path the gate hashes. That exit is evidence the gate reads the lane file, not evidence that B bytes fail.

## Mutation M2 — undo only C2's text

Clone commit `e0c7085b1868b7239a657c2eb6fb1aca223c428b`, parent `279e8b1` (not stacked on M1). Whole `PROVINCE.md` restored from B (34-line equal-length rewrite). SKILL lines 18-19 restored from B; the C1 rows from line 448 down stayed. Cached stat: `PROVINCE.md | 34`, `SKILL.md | 4`.

```
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-ConnectClaims-X0pHsY --rev e0c7085b1868b7239a657c2eb6fb1aca223c428b --strict
```
exit 0. `open_count` 0. All seven substance checks true. C1 does not depend on the C2 rewrite.

```
python3 -I -B .ufo/waves/round-19/tools/province-pins.py --root /tmp/kr19-ConnectClaims-X0pHsY --rev e0c7085b1868b7239a657c2eb6fb1aca223c428b --strict
```
exit 1. `mismatch_count` 2. Mismatches: Devin stated 6.5.0 vs live 6.7.0 (lines 9, 16, 44); OMP the same pair. That is the amended before-state (`claims.json:39`).

```
python3 -I -B .ufo/gates/c1-census-v10.py --root /tmp/kr19-ConnectClaims-X0pHsY
```
exit 1. `VERDICT: FAIL  (stale=4 ambiguous=0 undeclared=2 unresolved=0)`. Stale dispositions include PROVINCE `:9` omp 6.5.0, `:16` devin 6.5.0, `:17` omp 6.5.0, `:44` devin and omp 6.5.0, and SKILL `:19` devin and omp 6.5.0. Undeclared stayed 2. Putting the C2 sentences back is what moves C2's counters; the C1 registry rows were still present and did not add an undeclared block.

## Couplings that do not invalidate the counters

[OBSERVATION] PROVINCE `:12` says round carrier runs pin the superseded client pin `rea-agents@6.5.0`. Vet `orig_argv` has `--rea-version` `6.5.0` (`runs/t1250-vet/receipt.json:37-38`). The sentence is true because the C3 runs used that pin. `province-pins` did not extract it (tip stated lines are 9, 16, 17, 18, 44). Census `INLINE_MARKER` includes `superseded` (`.ufo/gates/c1-census-v10.py:320`), and the tip census stale count is 0, so the line is not a stale block. [INFERENCE] The sentence's truth depends on the C3 run pin; the C2 numeric proxies do not. Deleting the runs would make the sentence false without a `routed-r18` or `province-pins` failure. That is prose coupling inside C2's CURRENT block, contained by the marker, not a counter dependence.

[OBSERVATION] `routed-r18.py` `GO_SHA["go1.25.0"]` is `2852af0c…b613`, the same digest `claims.json:41` scopes to S038 and the lesson `## Installs` records. `s_install` reads only the lesson section. Lesson `:87` says no C3 measurement uses the install-record `go version` execution. Duplicated digest, not a fix dependence.

[OBSERVATION] Lesson `:94` extends S037's used-by onto `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`. That "C1 entry" is the round-12 knowledge entry, not round-19 C1. It is a carried item citing C2's source row. It does not feed `routed-r18`, `province-pins`, or the compare count.

[OBSERVATION] `claims.json` has no sentence that says the three claims are separable. Separability is the shape of the three falsifiers (`:13`, `:20`, `:27`) and the amended counters (`:38-40`). Those counters survived the cross-restores above.

## Where separability fails

[OBSERVATION] Under `decision-rule.json:3`, a label counts only when the working-tree `receipt-validate.py --require-mid-maps` exits 0. At `279e8b1` it exits 1 eight times, solely because the file C1 changed is the file the receipt pins. M1 shows the inverse: putting B bytes back in git reopens MIDMAP and is exactly the byte string the receipts expect. The two greens cannot hold on one path.

[OBSERVATION] The amended C3 count (`claims.json:40`) is "labels with a bound retained log and a compare.json, 0 → 8", and it points at the frozen rule. `decision-rule.json:6` repeats that count wording. "Bound" is defined by line 3. Read literally, the tip count is 0. Read as the retained JSON plus `compare.json`, the count is 8. The file contains both sentences. `measure.py:91-94` states that it does not verify the binding gate.

This invalidates separability for that gate and for any count that inherits it. It does not invalidate separability of `routed-r18` open-count, `province-pins` mismatch-count, census stale-count, or the compare.json presence count. C3's mechanism observations (vet index 13902080, seven silent controls) are in the logs and do not call the list branch.

## Proposed move

Affected axes: calibration improves; freshness and depth stay put.

Append one qualifier beside the C3 count, outside `predictions/decision-rule.json` (that file stays the pre-analyze freeze). State that `binding_gate`'s `receipt-validate.py` means the producer blob each receipt pins — sha256 `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145`, size 46047, the blob at B and at `a1140e7` — and that a later edit of the working-tree path is a different file whose live exit 1 is the expected C1 side effect. Keep the list-step fix. Do not rewrite the eight receipts. Do not widen census SCOPE.

Risk: until a counter reads the qualifier, a literal rerun of line 3 still reports count 0. Re-pinning the receipts to `6afb7ef6…` would erase the producer snapshot the knowledge entry forbids and would make the historical binding depend on C1's latest bytes. Verification: rerun the eight `--require-mid-maps` commands and expect the same two findings; rerun `routed-r18 --strict` at the tip and expect open 0; confirm `decision-rule.json` blob sha256 is unchanged by the qualifier.
