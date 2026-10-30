# RevSweep — pre-freeze misroot review

Recommendation: do not integrate the reviewed draft unchanged. Static review only; no helper, selftest, REA, or fixture runtime invoked.

Axes: ownership precision; mutation containment; byte-preserving recovery; read-only default; fixture isolation.

Reviewed snapshot: `.ufo/waves/round-51/w1/ExecMisrootSweep/misroot-sweep.sh`, read tag D99A, lines 1–77. Findings describe that snapshot, not future author edits.

## Numbered findings, severity first

1. **High — filename-only ownership can delete another lane's stray.** `classify()` at lines 6–11 accepts any path containing `kaidoku` OR `round-51`; line 23 passes only the path, never file content. Therefore a foreign lane's `other-round-51-note.txt` is selected for copy/delete (lines 35–41), while `random-note.txt` containing a kaidoku round-51 report is missed. This contradicts content classification and the explicit never-touch-non-kaidoku requirement. Require positive content attribution and leave ambiguous/foreign files report-only; add both inverse-name/content fixtures.

2. **High — apply has no forbidden-path or resolved containment guard.** Lines 23–25 and 35–41 have no exclusion for `.scratch/`, `.ufo/state/`, or `.ufo/watchdog.log`, nor destination-ancestor symlink checks. A selected file beneath a forbidden prefix can be touched when exposed by status; an existing symlinked destination parent can redirect `mkdir`/`cp` outside the lane. `[[ ! -e "$target" ]]` at line 37 checks only the final existing target, not its parents or dangling symlinks. Exclude forbidden prefixes before opening/classifying content and before apply, reject symlinks/nonregular files, and verify source/destination roots and containment before mutation. Add fixture coverage, not real-fleet probes.

3. **Medium — untracked-directory collapsing prevents per-file recovery.** Line 27 calls `git status --porcelain -z` without `--untracked-files=all`. Git's normal collapsed untracked-directory output can return `kaidoku-round-51/` rather than its files. Lines 38–39 then create parents and invoke nonrecursive `cp` on the directory, failing instead of recovering each stray. Enumerate untracked files individually without a pathspec; include a nested-directory fixture and explicitly propagate status failure (the process-substitution exit currently is not checked).

4. **Medium — apply performs an extra deletion on comparison failure.** Line 40 runs `rm -f -- "$target"` when `cmp` fails. The assigned operation is exactly copy byte-exact → cmp → delete the fleet copy, and nothing else; only successful comparison authorizes deletion of the fleet source. This branch instead deletes the lane destination. On comparison failure, stop with exit 2 and retain both artifacts for diagnosis; test injected comparison failure.

5. **Medium — standalone selftest has an unauthorized temporary-root fallback.** Line 47 uses bare `mktemp -d`; when TMPDIR is unset this normally writes under `/tmp`, contrary to this wave's scratch-only/no-`/tmp` rule. Require an explicit approved scratch parent (or fail closed when absent). Git identity scope itself is correct in the inspected selftest: lines 51–57 use `git -C "$fleet"`, verify the fixture toplevel before config/add/commit, and configure identity locally. However the current selftest only exercises a flat positive filename and a neutral foreign filename; it does not test default-mode zero mutation or findings 1–4.

## Contract/provenance gaps

- `plans/round-51-claims.md:178–181` currently says the helper is read-only and “never writes.” The seat's explicit `--apply` requirement necessarily writes. L1 should amend the pre-freeze declaration to distinguish default report mode from narrowly authorized apply, rather than freezing inconsistent promises.
- The specified `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` (snapshot 3BE2) has no literal misroot/stray/copy-byte-exact clause in text search. Its actual scope rules at 478–489 restrict lane writes and forbid runtime-state inclusion. The paired `PROTOCOL-APPENDIX.md` was opened too. The specific copy/cmp/delete exception is therefore grounded here in the canonical assignment, not falsely attributed to a located protocol paragraph.

## Residual risk and verification gaps

- No mounted LSP device: opening `xd://lsp` returned “No such tool.” References, definition, diagnostics and LSP status could not be requested. Text inspection is fallback evidence, not semantic proof.
- Default report branch contains no explicit file-writing commands before its line-28 return, but read-only behavior was not dynamically established. Ordinary `git status` can perform optional index refresh writes; consider `git --no-optional-locks -C ... status ...` when promising zero mutation.
- No selftest receipt existed when the draft was first reviewed; producer-reported checks are not independently exercised here. Required follow-up checks: default-mode before/after fixture hashes; opposing name/content ownership cases; forbidden-prefix and symlink containment; nested strays; comparison failure; failed-status exit 2.
- Canonical runtime, resume continuity, same-identity rerouting and saturation are not behavior surfaces of this helper and were not assessed.
- No tool installations, lane/fleet edits outside this seat's reports, scratch creation, or cleanup were needed.

Self-evaluation: accuracy 4/5 (static consequences, not runtime observations); completeness 4/5 (runtime attacks intentionally not invoked); clarity 4/5 (snapshot-specific line evidence); actionability 4/5 (each defect has a concrete correction/fixture); conciseness 4/5 (expanded evidence kept in this findings file). Overall 4.0. Primary improvement: independently run the repaired helper only in an authorized fixture pass.
