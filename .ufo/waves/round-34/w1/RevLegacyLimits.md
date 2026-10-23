# RevLegacyLimits — R34LegacyGaps prep report review

- **Seat:** `KaidokuR34.RevLegacyLimits` (UFO-FSD reviewer, leaf; no subagents, no execution of target/production scripts, no fixture authoring, no git/jj writes in lane or fleet).
- **Reviewed artifact:** `.ufo/waves/round-34/prep/R34LegacyGaps.md` + `R34LegacyGaps-files/` (successors, receipts, run-receipt.json, legacy-gap-matrix.json, fixtures).
- **Canonical frozen revision checked:** `54a87a51a865ab931fd355e767303337b05cccf4` (sandbox HEAD) — the sandbox is a sparse checkout (`tools/round-32/` absent from the worktree), so all frozen bytes were verified read-only from the Git object store via `git cat-file blob HEAD:<path> | sha256sum`.
- **UTC:** 2026-10-23 (~10:50Z).
- **Scope:** all five r32 wrapper survivors and the three archived secondary gates; fixed-vs-excluded disposition consistency; stale frozen-byte check. No production file was modified.

## Findings (by severity)

No high or medium findings. All items below are LOW/informational; none changes the disposition set or the evidence validity.

### LOW-1 — run-receipt.json `source_sha256` map omits the third archived gate
`run-receipt.json` `source_sha256` covers `wrapper_successor.py`, `quote_support_successor.py`,
`replay/indep_pe_replay.py`, archived `compare.py`, archived `pe_own_compare.py` — but not
archived `.ufo/waves/round-32/source-reopen/verify_quotes.py` (its pin `a41689cc...` is
asserted only in the prose report, not in the receipt's before/after hashing). Because the
harness never opens that file, `source_sha256_unchanged: true` still holds for everything it
touched; this is a completeness nit, not a broken invariant. Recommend the harness add the
third archived gate to its before/after set so the "unchanged" claim is machine-asserted for
all three gates.

### LOW-2 — C1-3 mutant text differs from the A2-recorded mutant
`run_checks.py` applies `if not isinstance(text, str) or eid not in text:` → `if not isinstance(text, str):`, whereas A2SelftestHoles recorded the C1-3 mutant as `if not eid:`. Semantically equivalent for the discriminator (removes the entry-presence half), and the harness correctly frames mutants as applied to successor copies, not to the frozen instrument. The receipt name ("C1-3 kill: live evidence_id omitted from the entry") is accurate. Purely textual-precision note.

### LOW-3 — red independent-pe run fails two checks, report names one
The tampered-run receipt shows `FAIL` for both `label_sha256` (…980 vs …989) and `oracle_sha256` (…989 vs …980), both consequences of the single tamper. The report says "label_sha256 fails, exit 1" — true but undercounts the failing rows. Informational.

### LOW-4 — section numbering skew between report and matrix
`R34LegacyGaps.md` §6 lists 8 residual limits; `legacy-gap-matrix.json` `residual_limits_of_the_repairs` lists 7. Content is consistent (the matrix merges the frozen-instruments gap and C2-1-bound-only items into the others); no contradiction.

## Verified ledger (claims → method → observed)

| Claim (report/matrix) | Verification method | Observed |
|---|---|---|
| Frozen C1 hash `7a534be6...` | `git cat-file blob HEAD:tools/round-32/c1-arm64x-positive.py \| sha256sum` | exactly `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a` |
| Frozen C2v3 hash `5955e8ac...` | same | exactly `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` |
| Archived compare.py hash `b955f908...` | same | exactly `b955f90849192ceeeee26b2849f2ec8dc1d4032e9fd05bf02e9e039cf9ed4209` |
| Archived pe_own_compare.py hash `587dadc6...` | same | exactly `587dadc65d756ccc25d9b05cbbdec0b61fb38b742ee651ebe278e06e1b023251` |
| Archived verify_quotes.py hash `a41689cc...` | same | exactly `a41689cc875ca28ea5bd3566bcf5c93eba3c6c54ce532b977960c07f0bc20e73` |
| C1 clause locations & mutant strings | `git show` + `grep -n` on frozen file | line 115 (`added <= freeze_ct`), 121 (`strip_meta(committed) != strip_meta(live)`), 124 (`if not eid or eid not in entry_text:`), 132 (`if CLAIM_ROW not in text:`) — all match A2SelftestHoles and the matrix |
| C2 threshold clause | `git show` + `grep -n` | line 168 `if len(shared) < MIN_DESC_WORDS:`; no successor file exists anywhere in the seat tree (grep for C2/calibration markers) |
| Frozen C1 selftest never exercises entry_ok/committed_check | read frozen `selftest()` body | only `judge` (11 cases) + `province_ok` (7 cases) = 18 cases; `entry_ok`/`committed_check` appear only at measure-time call sites 200/219 |
| Successor semantics for C1-1..C1-4 | read `wrapper_successor.py` | `entry_cite` (claim_row substring), `envelope_equal` (strip_meta full compare, dict guard), `evidence_id` (nonempty eid substring), `post_freeze` (`added > freeze_ct`, rejects bool); 20 selftest cases incl. the four discriminators; fail-closed `evaluate` |
| Repaired disposition for C1-1/2/3, predicate-only for C1-4 | report table vs matrix rows | identical dispositions; C1-4 limits explicitly name unexercised git acquisition + A2FreezeBytes finding 3 (verified: finding 3 exists, committer-timestamp comparison) |
| C2-1 open/excluded disposition | matrix row | `successor: null`, boundary spec retained (exactly 5 = match, 4 = mismatch), QUALITY-58/spotcheck-defect-4 rationale; no threshold code shipped |
| compare.py selftest added | read archived compare.py + shim + receipts | compare.py has `if __name__ == "__main__"` guard, hardcoded `TSV`/`BASE`, no argv use, calls `llvm-readobj --version`; shim imports read-only and rebinds only TSV/BASE; green receipt `carriers=1 checks=31 passed=31 failed=0` exit 0; red receipt exit 1 |
| verify_quotes successor-only, archived excluded | read frozen file + successor | frozen file executes at import (no `__main__` guard; module-level `sys.exit`), hardcodes SNAP/C1IN//fast RE; literal-True diagnostic rows confirmed (`drift:html:changed-lines`, `drift:html:timestamp-class`, `drift:html:sample`); successor runs 9 selftest cases, 7 support/2 informational rows, diagnostics print as INFO and are excluded from count |
| pe_own_compare excluded/not-run | read frozen file + run-receipt.json | `own_parse` opens carrier DLLs `rb`; no selftest; `not_run` record (open-bounded-limit) with archived sha and reason present |
| Fixtures are text-only copies with provenance | read provenance.json; hash/compare against archived originals | carriers k01 row verbatim-equal to `corpus/evidence/round-32/c1/carriers.tsv`; readobj-k01.txt byte-identical (`aa1ee360...`); oracle k01 = exactly 1 line; indep.json has only results[label=k01]; provenance declares `binary_content: false` and source sha256s; no binary-magic file found anywhere in the seat dir (scan of all 40 files) |
| Run receipt integrity | read run-receipt.json | `checks_run=19 checks_failed=0 not_run=1`, `source_sha256_unchanged=true`, 19 check records A..G with passes, mutant argv paths under `tmp/run-280559/mut-*` (private successor copies), E tampered red exit 1 with 2 failures, F Q-1/Q-2 killed, G red exit 1 |
| No stale frozen byte revision | grep seat dir for frozen markers; read successors | no copy of any frozen instrument; only textual references (docstring/matrix); `tmp/` empty; successor code is new re-statement, not an old revision |
| Authored-file hashes in report §4 | `sha256sum` | all five match (`eefaa3c9`, `e280d7b7`, `3a4ab63c`, `f51572aa`, `336dac96`) |

## Residual risk and verification gaps

- **Read-only review:** I did not execute `run_checks.py` or any successor (and did not rerun any binary script or create fixtures). Green/red behavior is attested by the receipts' argv/exit/stdout and is internally coherent with the code I read; I did not independently re-observe a live run.
- The harness's same-second blind edge for `post_freeze` remains disclosed and unexercised; no git writes were made.
- `verify_quotes` archived verdict map stays unselftested; the report recommends excluding it from admission — consistent with "not conformance evidence".
- I cannot verify what happened outside the seat's artifact tree; production lane is read-only and untouched.

## Tooling record

- Installed/updated: none (pacman paused host-wide; nothing else needed).
- Used read-only: `git cat-file`/`git show`/`git ls-tree` (object store), `sha256sum`, `grep`, `sed`, `find` on the production wave dir + seat dir (not `/fast/scratch`), and `python3` only to print JSON label lists (no script execution).
- Successful answering model: not visible to this seat; not recorded.

Report: `.ufo/waves/round-34/w1/RevLegacyLimits.md`
