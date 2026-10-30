# MutC1Bindings — probe receipts

Every command below was run by this seat. Exit codes are semantic: 0 = the probe ran
and the baseline was green; a red baseline makes the battery inconclusive and the probe
exits non-zero rather than reporting vacuous results.

**Host:** linux 7.2.11-arch1-1 · **UTC:** 2026-10-30
**Scratch:** `S=/fast/scratch/hyaku/kaidoku-r52/w1-MutC1Bindings` (`TMPDIR=$S`)

---

## R-1 — battery against the frozen round-50 counter (the reference semantics)

- **command:**
  `python3 "$S/probe.py" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-50/c1-counter.py "$S/out-v1.json" "$S"`
- **cwd:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **exit code:** `0`
- **stdout sha256:** `5d1dcbaf1071ca2b5f96275e7cb3050f5a5e061603b00302e53d4c8422b3d979`
- **UTC time:** `2026-10-30T10:59:35Z`
- **counter under test sha256:** see `out-v1.json` → `counter_sha256`
- **summary (stdout line 1):**
  `{"baseline_red": 0, "cascade": 0, "covered": 0, "dead": 8, "green": 1, "killed": 33, "no_op": 2, "total": 44}`
- **injected missing names:** `[]` (the v1 counter imports as-is)

## R-2 — battery against the round-52 v2 draft

- **command:**
  `python3 "$S/probe.py" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ExecCounterV2/c1-counter.py "$S/out-v2.json" "$S"`
- **cwd:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **exit code:** `0`
- **stdout sha256:** `7c6c968e8144521995e1d627f8ff73d6d9e39e33be2fbce910e2dfd9a5c67a35`
- **UTC time:** `2026-10-30T10:59:35Z`
- **summary (stdout line 1):**
  `{"baseline_red": 0, "cascade": 0, "covered": 0, "dead": 8, "green": 1, "killed": 33, "no_op": 2, "total": 44}`
- **injected missing names:** `["TARGET", "IDS"]` — **the draft does not import** (Finding F1);
  the probe injected the two module-level names into an **in-memory copy only**. The file
  on disk was never written.

## R-3 — the two counters' binding blocks are byte-identical

- **command:**
  `python3 -c "…extract '# ---- bindings' … 'res[met_target]' from each file and compare…"`
- **exit code:** `0`
- **stdout:** `identical: True len 2614 len 2614`
- **UTC time:** 2026-10-30 (preceding the battery runs)
- **meaning:** every doc-binding verdict in R-1 applies verbatim to the v2 draft.

## R-4 — the v2 draft does not import (Finding F1, reproduced directly)

- **command:**
  `python3 -c "import importlib.util; …exec_module(…ExecCounterV2/c1-counter.py)"`
- **exit code:** `1`
- **stderr (verbatim tail):**
  `File ".../ExecCounterV2/c1-counter.py", line 2141, in <module>`
  `    def measure(root, rev, freeze, pkg65, rerun=None, target=TARGET,`
  `NameError: name 'TARGET' is not defined`
- **UTC time:** 2026-10-30 (before R-2)

## R-5 — D10 and N08 verified against the **real** lane row

- **command:**
  `python3 -c "read PROVINCE.md:446, apply the D10/N08 edits, evaluate HANDLER_RE / AVM_MARKER_RE / ENTRY-in-row exactly as the counter does"`
- **exit code:** `0`
- **stdout (verbatim):**
  ```
  real lane row passes province_core_row: True
  D10 (layout column emptied) still passes: True
  N08 (only a NEGATIVE BE-clause marker mention) still passes: True
  ```
- **UTC time:** 2026-10-30 (after R-2)

## R-6 — the v2 draft lacks the round-sensitive flags and the law predicate

- **command:** `grep -c "provenance-base\|receipt-fresh-base\|law_shape_ok\|census_rederived_ok\|depth_gap_recorded\|re_scored_pins" ExecCounterV2/c1-counter.py`
- **exit code:** `1` (no match for any of the six)
- **stdout (verbatim, per-pattern counts):**
  `gap-rule 9` · `receipts 25` · `provenance-base 0` · `receipt-fresh-base 0` ·
  `law_shape_ok|census_rederived_ok|depth_gap_recorded 0` · `re_scored_pins 0`
- **UTC time:** 2026-10-30

## R-7 — the round-50 real lane row shape

- **command:** `grep -n '^| genuine AVM-marker little-endian SquashFS v4' PROVINCE.md`
- **exit code:** `0`
- **stdout (verbatim):** `446:| genuine AVM-marker little-endian SquashFS v4 (`hsqs`, v4.0 xz, …`
- **cell count of that row:** `3` (surface / layout / entry)
- **UTC time:** 2026-10-30

---

## Not run

- **No REA run.** The contract forbids it this wave. The probe therefore exercises the
  bindings and the three receipt clauses **directly** (verbatim extracted code against
  synthetic fixture trees), and does **not** score a full carrier predicate.
- **No `--data-run`, no vendor download, no `npx rea-agents`.**
- **No lane write.** The probe wrote only into `$S`; the lane tree was read-only.
- **`law_shape_ok` / `census_rederived_ok` / `depth_gap_recorded` mutations (M1–M4):**
  not run — those clauses do not exist in either counter under test, so there is nothing
  to mutate yet. They belong to the law owner's battery (§5 of `battery.md`).
- **`carrier_fresh_ok` with a `re_scored_pins` allow-list (R10):** specified but not
  executable against either counter — no such constant exists (R-6). Recorded as NO-OP
  / an open obligation, not as a pass.
