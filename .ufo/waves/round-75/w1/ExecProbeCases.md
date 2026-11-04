# ExecProbeCases — independent re-derivation of the round-74 BEFORE-WORLD survivors (round-75, w1)

Seat: ExecProbeCases · Date: 2026-11-04 · Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin

## Scope and method

Re-derived the CLAIM'S BEFORE WORLD for R75-C1 by hand, **without running
`tools/round-75/probe-mutation.py`**:

- Source: `git show 3c15a156239af06114e1ece8d1044a0d8205379b:tools/round-74/seam-probe.py`
  (71029 bytes, sha256 `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039`), extracted to a
  private scratch copy.
- Five mutants hand-applied one per fresh copy of the pristine file (per-row edits verified in place).
- Each run: `TMPDIR=<scratch> python3 -I -B <copy> --selftest` with cwd = the lane.
- `tools/round-74/seam-probe.py` untouched (read-only target); no lane file edited by this seat.
- `git status --porcelain` after all runs: only pre-existing untracked wave artifacts — the probe runs
  wrote nothing into the lane (selftest is self-contained: injected `/proc` readers, fake spawn).

## Results (receipt.json + per-run logs in `w1/ExecProbeCases/`)

| run | site (pristine line) | mutation | rc | failures | verdict |
|---|---|---|---|---|---|
| pristine | — | — | 0 | `[]` | 20 cases, green (expected 20 / `[]`) |
| row 1 | a12_verdict genuine_ok, 558 | `and s.get("home_under") is True` → `and bool(s.get("home_under"))` | 0 | `[]` | GREEN — **d-home-under-truthy survivor** |
| row 2 | a12_verdict genuine_ok, 559 | `and s.get("tmpdir_under") is True` → `and bool(s.get("tmpdir_under"))` | 0 | `[]` | GREEN — **d-tmpdir-under-truthy survivor** |
| row 3 | `_name_samples`, 651 | `out.setdefault(name or "?", sample)` → `out[name or "?"] = sample` | 0 | `[]` | GREEN — **d-name-samples-last-wins survivor** |
| row 4 | a12_verdict lie_clean, 562–563 | `sorted(s.get("keys") or []) == allow and not s.get("canary_present")` → `set(s.get("keys") or []) >= set(allow)` | 0 | `[]` | GREEN — **d-lie-clean-superset survivor** |
| row 5 | kernel_witness sample dict, 527 | deleted `"canary_present": "KAIDOKU_ENV_CANARY" in env,` | 1 | `["a12-kernel-multiple-samples", "a12-kernel-canary-field"]` | RED — **b-drop-canary-field killed, cross-binding confirmed** |

Full raw stdout of every run preserved verbatim in the row logs; failure lists above are the complete
`failures` arrays as printed by the selftest.

## Findings

1. **Four survivors independently reproduced.** Rows 1–4 each leave `--selftest` green (rc 0,
   `failures: []`, 20 cases). The survivor set matches the claim's BEFORE WORLD exactly:
   `d-home-under-truthy`, `d-tmpdir-under-truthy`, `d-name-samples-last-wins`, `d-lie-clean-superset`.
   The round-74 selftest's 20 cases genuinely do not close these classes: `bool()` accepts any truthy
   value where `is True` was checked, last-wins naming aliases are unobserved, and the lie_clean check
   weakens silently under superset semantics.
2. **Cross-binding of b-drop-canary-field confirmed.** Deleting the kernel_witness sample's
   `canary_present` line makes exactly two cases fail — `a12-kernel-multiple-samples` (its
   `any(s.get("canary_present") ...)` conjunct loses its only true sample) and
   `a12-kernel-canary-field` (`isinstance(s.get("canary_present"), bool)` sees `None`). No other case
   moved. This matches the assignment's stated cross-binding expectation: row 5 rc 1 with exactly those
   two case names.
3. **Acceptance: ALL MET** — rows 1–4 rc 0 / `failures: []`; row 5 rc 1 with exactly the two names;
   pristine 20 cases / `failures: []`.

## Evidence

- `w1/ExecProbeCases/receipt.json` — structured receipt (pristine, rows with name/mutation/rc/failures/verdict, acceptance).
- `w1/ExecProbeCases/pristine.log`, `row1-home-under-truthy.log`, `row2-tmpdir-under-truthy.log`,
  `row3-name-last-wins.log`, `row4-lie-clean-superset.log`, `row5-drop-canary-field.log` — verbatim run outputs with rc.
- Scratch copies and mutants were under `/fast/scratch/hyaku/kaidoku-r75/ExecProbeCases/` and were deleted after the run.

## Risks / notes

- None open. All six outcomes matched the assignment's expectations exactly; no alternate or ambiguous
  output was produced. Tooling installed: none. `tools/round-75/probe-mutation.py` was not executed, per scope.
- The claim sentence "(failed == exactly that case)" reads as single-case in the frozen text, while the
  assignment's row-5 spec (and the observed ground truth) is the two-name cross-binding set; the observed
  two-name list is recorded in full so the parent can reconcile wording against data.
