# SentWaves: r52-w1 spec write-scope audit

Verdict: **settled with findings.** No item grants lane-tree, fleet, `.scratch/`, `.ufo/state/`,
sibling-lane, REA, `--data-run`, `corpus/evidence/`, or git-mutation writes in its deliverable.
Eight findings (F1-F10 in the audit; F9 and F10 are notes) need spec edits before dispatch or
before the L1 relies on the item. Full item-by-item table: `SentWaves/audit.md`.

## Most important findings

1. **F1 (medium), item 06 ExecMisrootSweep.** The item authorises a fleet-repo deletion
   ("the one permitted fleet deletion") and asks for an `--apply` that performs it. The contract
   forbids fleet-repo touches. Remove the fleet clause; keep the helper read-only plus lane copy.
2. **F2 (medium), items 03 and 15 (harness dry-runs).** The round-50 harness defaults to
   scratch `/fast/scratch/hyaku/kaidoku-r50` and to OUTDIR `corpus/evidence/round-50/c1/<id>`
   (verified by dry-run). Guards currently refuse a write (exit 2), but the items do not pin
   `--outdir`/`--scratch` or forbid `--data-run`. Pin both.
3. **F4 (medium, routed defect 2).** 61 of 64 prompts omit the status.json instruction; only
   `context` carries it. The L1 must confirm the rendered dispatch includes the context in every seat.
4. **F3 (medium), item 01 ExecControls.** Receipt directory unnamed. Pin to `w1/ExecControls/receipts/`.
5. **F5 (low-medium), item 00 ExecCounterV2.** "Offline `--selftest`" is not tied to REA. The v1
   selftest resolves rea-agents via `find_rea_pkg()` (`c1-counter.py:595`); whether it reaches the
   node recompute at `:686` is [INFERENCE], not run. Prohibit `--selftest-rea`, `--dev-image`, and
   counter runs without `--no-rerun`.

## Other findings (low)

- F6: vendor HEAD requests reached by reference (items 10, 27); justified, name the URLs literally.
- F7: sibling-lane reads (item 60) are read-only but ambiguous under "never touch a sibling lane".
- F8: item 53 names a `--file`-style mode that `census3.py` does not have; the exact command is
  `--root <scratch> --rev WORKTREE --check --census <relpath>`.
- F9: item 11 does not name a `--json-out` directory (v5 requires one).
- F10 (note): py_compile writes `__pycache__` beside source even without `-B`; items 29 and 37 say "in your scratch".

## Checks (receipts in `w1/SentWaves/receipts/receipts.txt`)

- Credentials: none in spec or context (regex scans, 0 hits). `cookie`/`token` appear only as nouns.
- URLs: three literals (`man7` mknod(2) x2, capabilities(7)), all justified by their tasks. Vendor
  carriers by reference; all four hosts `download.avm.de`. No unjustified URL.
- Placeholders: 0 unresolved `{...}` markers.
- Spawn: none instructed.
- Attack share: 24/64 (37.5%) by role label; 28/64 (43.8%) if LB1-LB4 are counted. Both clear 25%.
- Harness guards (verified): after-arm without `--data-run` exits 2; default-OUTDIR in a scratch copy
  exits 2; `--dry-run` writes nothing.
- Census base: `census3.py --check` at `ab0eafed` exits 0 (56 registry paths, outside [], unregistered [], duplicates []).
- Lane git status: unchanged by this seat (only `w1/` and `round-52/l1/` untracked, pre-existing).

## Tooling

No installs. Used the host's `python3`, `bash`, `git`, `sha256sum`, `grep`. Nothing installed or
upgraded; no pacman use. Read-only lane access; no git mutations; no REA; no network beyond the
spec's named reads (none performed by this seat).

## Scope of my writes

Only `.ufo/waves/round-52/w1/SentWaves/` (audit.md, status.json, receipts/) and
`.ufo/waves/round-52/w1/SentWaves.md`. Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-SentWaves`
removed before yield.
