# ControlMap — scoped review

**Scope:** README coverage-map paths and format; no-harm controls for `corpus/README.md` at baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`.

**Axes reviewed:** coverage and calibration. This is an author-side review of the observed baseline-to-HEAD state, not outside admission. At inspection, `HEAD` was `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`; it is not a final revision. Do not infer a final-after result from this report.

## Findings (severity order)

### Medium — `prior-controls` calculates dangling map entries but does not gate them

`.ufo/waves/round-21/controls.py:62-75` parses the Coverage map and returns `missing` and `dangling` sets, but its acceptance predicate at line 86 checks only unchanged prior files, LOG/SCORECARD prefixes, QUALITY rows, and nondecreasing coverage/depth scores. A fabricated entry with no backing knowledge file increases `dangling` without decreasing the score when every actual knowledge file is already mapped; such a bad row can pass this control. This leaves the README's explicit rule (“A row is written when its file exists,” `corpus/README.md:9`) unenforced by the gate.

**Invariant for L1 to verify at final:** require `mapping_after.missing == []` **and** `mapping_after.dangling == []`, in addition to score non-regression; validate each Coverage-map entry path against the revision tree. At the inspected HEAD, the direct controls output had `missing: []` and `dangling: []`, so this is a control gap, not an observed bad new row.

### Low — C1-only separability omits the README that claims.json assigns to C1

`claims.json:22` lists `corpus/README.md coverage-map rows` among C1 touches. However, `.ufo/waves/round-22/verify.py:84-87` builds the `C1-only` path list from C1 evidence, round-22 knowledge, and `corpus/SOURCES.md`; it omits `corpus/README.md`. The separability matrix at lines 89-107 therefore does not apply or assess the C1 map update in the isolated C1 revision. The normal prior-controls check sees the combined revision, but that does not close this isolation gap.

**Invariant for L1 to verify at final:** the C1-only reconstruction includes the C1 README map rows (or explicitly states that map rows are outside the separability assertion and separately checks their C1-only presence/path resolution). Do not report separability as covering all listed C1 touches while README remains omitted.

## Observed map state and no-harm evidence

- `corpus/README.md` uses the existing three-column Coverage map table (`section | entries | state`, lines 11-13). Existing rows include both category rows with one or more entry basenames (for example line 69) and single-knowledge-file rows. The R22 category row at line 70 follows the former convention and is directly before `## Knowledge`.
- The README also keeps a four-column Knowledge index and a Lessons index. The R22 knowledge row is at line 156, the `round-22` Lessons row at line 173. New data rows sit at the ends of their respective tables; no existing row was edited in the baseline-to-HEAD README diff.
- Baseline-to-HEAD `git diff` showed only three README insertions: the `Static Flutter APK boundary (round 22)` map row, the `2026-10-21-r22-flutter-static-boundary` Knowledge row, and the `round-22` Lessons row. Map and index entries resolve to the extant round-22 knowledge file at inspected HEAD. A read-only parser found 55 Coverage-map and 81 Knowledge data rows at B, versus 56 and 82 at inspected worktree/HEAD; it reported no malformed four-pipe rows and no missing map/index targets. These are point-in-time observations, not final-tree assertions.
- The current README itself had no uncommitted change in the observed `git diff HEAD --stat`; the shared worktree did contain unrelated/in-flight round-22 modifications. The final tree may differ.
- An inherited out-of-map citation remains stale: `corpus/README.md:123` cites `.ufo/waves/kaidoku-r5/05-riscv-deep.md`, which `git cat-file -e` could not resolve at either B or inspected HEAD (exit 128), and which was absent from the worktree (test exit 1). It is in the Knowledge table, not a newly added Coverage-map row, and is present before this round; it is not attributed to the R22 change.

## Commands and observed results

1. Baseline C1 measurement:

   ```sh
   cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && timeout 120 python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 7787fea4d6fd718726de92ed20759d11ce7b8b48
   ```

   **Observed:** program exit `1`; `rev` was B, `t1_exercised_count` was `0/6`, and `catalog_zero_count` was `20` of 153. This agrees with the frozen before expectation; it is not a final-after measurement.

2. Existing no-harm controls B→the then-current HEAD:

   ```sh
   cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && timeout 180 python3 -I -B .ufo/waves/round-21/controls.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --before 7787fea4d6fd718726de92ed20759d11ce7b8b48 --after HEAD
   ```

   **Observed:** program exit `0`, `finding: controls_clean`; B mapping `102/102`, score `10.0`, `missing: []`, `dangling: []`; HEAD mapping `103/103`, score `10.0`, `missing: []`, `dangling: []`; `prior_files_checked: 1135`, `prior_files_changed: []`; LOG/SCORECARD prefixes true; prior QUALITY rows identical (28 before, 30 after). The tool's own limit says these are structural proxies, not a semantic audit.

3. README diff inspection:

   ```sh
   cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git diff 7787fea4d6fd718726de92ed20759d11ce7b8b48..HEAD -- corpus/README.md
   ```

   **Observed:** three added rows listed above; no deletion or modification of existing README lines. (The earlier captured invocation piped to `head -80`; its shell exit `0` was the pipe's `head` status, not a claim that `git diff` had no changes.)

4. LSP availability:

   ```text
   read xd://lsp
   ```

   **Observed:** `No such tool: xd://lsp` (tool registry listed no LSP device). Therefore no LSP references/definitions/diagnostics were available; text inspection was only a literal fallback and is not semantic proof.

## Residual risk and verification gaps

The final revision did not exist at the time of review. The complete round-22 final verifier, final C1/C2 outcome, final coverage-map path-resolution result, and final counter/separability checks remain for L1 to run against the actual final revision. In particular, the two control gaps above should be closed or explicitly scoped before treating map validity and C1 isolation as verified. No install was performed.
