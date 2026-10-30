# ScoutDraftsInventory — round-51 draft inventory and round-52 port map

**Seat:** `ScoutDraftsInventory` (scout) · **round:** kaidoku-shokunin round 52, wave `r52-w1`
**Lane root:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
**Round base:** `c525de54a53eb3c4fee28ede2721da4527cf8ece` · **claims draft:** `ab0eafedc41402b43b41a4362084119578dfe7ce`
**Lane HEAD at survey:** `1842addcef3458515859b928b92d9bbd0a46c5d5` (round-52 wave-1 dispatch commit)

**Verdict in one line:** round 51 landed **only** `tools/round-51/census3.py` + `census3.json`;
every round-52 instrument draft is still a wave artefact, and **three of the four big drafts are
not portable as-is** (one is a syntax error, one is broken against its own counter, one regresses
a green selftest into a crash). The L1 must port from the **r50 sources** plus the r51 *specs*
(battery/derivation prose), not from the r51 *drafts*.

---

## 1. Method (read-only, no lane writes)

* Read every file under `.ufo/waves/round-51/w1/` and `.ufo/waves/round-51/l1/`
  (333 non-`__pycache__` files; full table in `receipts/draft-table.md`).
* Syntax-checked every candidate instrument in scratch
  (`python3 -m py_compile`, `bash -n`) — receipts `py_compile_*`, `bash_n_*`,
  `json_load_gap-rule-v2` in `receipts/receipts.tsv`.
* Diffed each draft against its round-50 landed source (`diff -u`) to extract the real deltas.
* **Executed** the r51 counter draft's `--controls` mode and the r51 controls driver in a
  scratch `git clone --shared` of the lane at the claims-draft commit, to test portability
  rather than assert it. No REA, no data run, no network, no lane mutation.

Scratch: `/fast/scratch/hyaku/kaidoku-r52/w1-ScoutDraftsInventory` (removed after copy-in).
Fixture clone: `git clone --shared <lane> $S/clone`, `checkout --detach ab0eafed…`;
`git rev-parse --show-toplevel` asserted == `$S/clone` before the single scratch commit
(`aa8da9e1435e82362bda89cf119d2b44cebed9a3`); `user.name`/`user.email` set **in that clone only**.

---

## 2. Ground truth: what round 51 actually landed

`git ls-tree -r HEAD tools/` at the round-52 base shows **only** `tools/round-51/census3.json`
and `tools/round-51/census3.py` under `tools/round-51/`. No counter v2, no triage v6, no
controls, no harness, no fetcher, no gap rule.

This matches the round-51 claims' own **Final disposition** (`plans/round-51-claims.md:331+`):

> "The C1 counter/harness and incomplete v6/fetch/misroot-helper drafts are preserved under
> `.ufo/waves/round-51/`, **not shipped as working production instruments**. Only the completed
> registry-inventory diagnostic `tools/round-51/census3.py` and its census are delivered…"

So **every** round-52 instrument under `tools/round-52/` is a fresh port. The round-51 drafts
are *inputs*, and the questions below are which of them are inputs worth copying.

---

## 3. Per-draft verdicts

### 3.1 `l1/drafts/c1-counter.py` — the r51 **L1-merged v2 counter** (272 105 B)

* **Syntax:** valid (`py_compile` exit 0).
* **Runtime evidence:** `.ufo/waves/round-51/l1/counter-draft-selftest-output.txt` records
  `{"selftest": "c1-counter", "cases": 184, "green_ok": 21, "red_ok": 163, "path_probes": 6, …}`
  — the draft's own selftest ran green in round 51.
* **What it already implements** (vs the r52 claims):
  | r52 clause | present in the r51 draft | evidence |
  |---|---|---|
  | `law_shape_ok` | **yes** | 7 hits; binding at L~2660-2681: `allowed[<device kind>]` must be empty, `removed.silent[<device kind>]` must be empty, `required['char-device'] is False` |
  | `census_rederived_ok` | **yes** | 8 hits; `oracle_env_error` exit-2 path at L1990 / L3874 |
  | `--controls` rule-scoped mode | **yes** | `controls_mode()` L2706-2800; CLI `--controls --gap-rule --receipts` L2827-2838 |
  | `re_scored_pins` / `prior_pin_sources` / `carrier_fresh_ok` | **yes** | L423 `PRIOR_CARRIER_TABLES`, L934-948 `prior_pins`/`re_scored_pins` grammar, L1652 `prior_pins()`, L2323-2325 |
  | REA retry on `provider_timeout` + ENOENT `execution_failure` | **yes** | `MAX_REA_ATTEMPTS` (5 hits), `provider_timeout` (7 hits) |
  | rule claim labels `{R50-C1, R51-C1}` | **yes** | L839, L922 — **needs `R52-C1`** |
  | `depth_gap_recorded` | **name mismatch** | draft emits `depth_gaps_recorded` (L2685) — r52 claim spells it `depth_gap_recorded` |
  | `--provenance-base` / `--receipt-fresh-base` | **MISSING** | not in the `add_argument` list (L2808-2838); only mentioned in the docstring |
* **Measured portability (my probe):** placed at `tools/round-51/c1-counter.py` in the scratch
  clone with a round-51 carriers table and a law rule, then run in `--controls` mode over the
  committed round-50 envelopes:
  * `--gap-rule tools/round-50/gap-rule.json` → `{"carriers_scored": 4, "dispositions_matched": 2}`, **exit 1**
  * `--gap-rule tools/round-51/gap-rule.json` (law) → `{"carriers_scored": 4, "dispositions_matched": 4}`, **exit 0**
  * per-carrier `gaps_note` for `g7581`/`g7582`: *"required entry with no disposition (no gap, no
    MaliciousSymlinkRemoved) on ['dev/pts/0', …]"* — i.e. it independently reproduces the
    round-50 miss diagnosis (the twelve unaccounted FRITZ!Box char-devices) and the law repair.
  * Receipts: `ctl_old_r50_rule` (exit 1, sha `47487d35…`), `ctl_new_law_rule` (exit 0, sha `6f00124e…`).
* **Verdict: USE-DRAFT (best source).** This is the only r51 draft that is both complete and
  *demonstrably* producing the r52 CTL-OLD/CTL-NEW numbers. Port it, then apply the r52 deltas
  in §5.

### 3.2 `w1/ExecCounterV2/c1-counter.py` — the r51 **executor** counter draft (244 329 B)

* **Syntax:** valid. But the diff against the landed `tools/round-50/c1-counter.py` is **only
  36 lines**, and every one of them is a path/round constant.
* **What it implements:** nothing new. `law_shape_ok` 0 hits, `census_rederived_ok` 0 hits,
  `depth_gaps_recorded` 0 hits, `re_scored_pins` 0 hits, `--controls` 0 hits, `R51-C1` 0 hits.
  It is the r50 counter with `tools/round-50/` → `tools/round-51/`, `round-50` → `round-51`,
  and a re-pointed frozen-path family.
* **Verdict: PORT-FROM-R50-SOURCE (evidence-only).** Do not use as a port base; it is the r50
  counter wearing an r51 label. Keep it only as the "what a naive port looks like" baseline.

### 3.3 `w1/ExecTriV6/sqfs-triage-v6.py` — the r51 **triage v6** draft (107 956 B)

* **Syntax: BROKEN.** `python3 -m py_compile` → **exit 1**,
  `SyntaxError: invalid syntax` at line 288, verbatim:

  ```
  READER_BACKED_V1V3 = (
      'squashfs_v1',
      'squashfs_v2',
      'squashfs_v3',
  CUT 1033.=1033
  )
  ```

  A literal `CUT 1033.=1033` marker sits where `'squashfs_v3_ddwrt'` was removed. The marker is
  the only such token in the file (`grep -n 'CUT \|PLACEHOLDER\|TODO\|FIXME'` → 1 hit, receipt
  `v6_draft_cut_marker`).
* **Further defects beyond the syntax error** (all confirmed by diffing against
  `tools/round-50-c3/sqfs-triage-v5.py`, 23 changed lines):
  1. **Shebang lost** (`#!/usr/bin/env python3` removed).
  2. **Duplicate table row** — `['no-reader-failure', …]` appears at both line 1033 and 1034
     (identical), a v6 table defect the v5 table did not have.
  3. **The v5 `legacy-body-failure` row's text was mangled**: its `source` field and its
     explanatory paragraph were replaced with `'R51-C2; retained v5 rule'`, losing the
     `SKILL.md table v4 row 7 narrowed by R50-C3` citation chain.
  4. **The evaluator was never updated**: `evaluate()` still returns
     `'legacy-body-failure', 'cross-read-legacy'` for the ddwrt body (L952). The new
     `legacy-body-unreadable` row was added to the *table* but not wired into the *evaluator*.
  5. **The executability audit is absent**: `executability_violations` 0 hits,
     `census_outside` 0 hits. r52 requires both as first-class receipt keys with fail-closed
     gates.
  6. **No `--table` flag.** r52's C2 before-arm requires
     `--table tools/round-50-c3` (the v5 table bytes) to score `executability_violations 1`
     at the claims-draft base. v5 has no `--table` flag at all
     (v5 flags: `--root --rev --freeze --envelopes --json-out --skill --work --selftest
     --print-v5-block --emit-mutant --controls`).
* **Verdict: PORT-FROM-R50-SOURCE (v5) + SPEC-ONLY for v6.** Use
  `.ufo/waves/round-51/w1/MutTriV6/battery.md` as the **spec** (it defines detectors D1/D2/D3,
  the precedence rule, the fail-closed gate and 15 mutants) and
  `.ufo/waves/round-51/w1/CritTriV6/findings.md` as the attack record. Do **not** copy the
  draft's bytes.

### 3.4 `w1/ExecControls/c1-controls.py` — the r51 **controls driver** (5 204 B)

* **Syntax:** valid (112 lines, complete — no elision markers).
* **Design:** a *new, small* offline driver (not a port of the 90 KB `tools/round-50/c1-controls.py`).
  It synthesises named rule variants (`old`, `new`, `junk`, `require-char-device`, `only-247-0`,
  `strict-subset-01..12`) into `--out/rules/`, then shells out to the counter's `--controls`
  mode once per variant and scores exit code + `carriers_matched`.
* **Measured against the r51 counter draft: BROKEN.** Receipt `r51_controls_driver` → **exit 1**;
  all 18 controls came back `exit_code: 2` with an *identical* `stdout_sha256`, and CTL-OLD,
  CTL-NEW and CTL-JUNK were all `"verdict": "misbehaved"`. Two independent defects:
  1. **Missing `--rev`.** The driver builds
     `[… counter, --root, R, --controls, --gap-rule, G, --receipts, D]` — no `--rev`. The
     counter's `--controls` branch refuses without it (`usage: --controls requires --root --rev`,
     exit 2), so *every* control fails identically.
  2. **Wrong receipt key.** `observed_count()` reads `doc.get('carriers_matched')`, but the
     counter emits **`dispositions_matched`** (plus `carriers_scored`). Even with `--rev`
     supplied, the observed count would be `None` for every control.
  3. **Its `new` rule variant is a whitelist, not the law.** `rule_fixtures()` sets
     `new['removed']['silent']['char-device'] = list(DETAILS_13)` — the thirteen-detail
     whitelist. Under r52's `law_shape_ok` that rule is **red**, and r52's CTL-NEW must score
     the *law* rule (device kinds' `allowed` empty, `removed.silent` empty,
     `required['char-device'] false`).
* **Verdict: USE-DRAFT (structure) + FIX (three defects).** The driver *shape* (named variants,
  one subprocess per control, per-control JSON receipt with command/exit/stdout sha256/UTC) is
  exactly what r52's CTL-OLD/CTL-NEW/CTL-DN/CTL-JUNK/M1-M4 arms want. Port the shape; fix the
  three defects above and add the r52 arms (M2 fourteenth-device fixture).

### 3.5 `l1/drafts/c1-run.sh` — the r51 **run harness** (46 142 B)

* **Syntax:** valid (`bash -n` exit 0).
* **Diff vs the landed `tools/round-50/c1-run.sh`: 39 changed lines**, all round constants:
  `ROUND_SEGMENT=kaidoku-r51`, `SCRATCH_PREFIX=/fast/scratch/hyaku/kaidoku-r51/`,
  `EVIDENCE_SEGMENT=/corpus/evidence/round-51/`, schema `kaidoku-r51-c1-run-v1`,
  claim `R51-C1`, and the prose. No semantic change.
* **Verdict: PORT-FROM-R50-SOURCE.** The draft adds zero behaviour over the landed harness; a
  pure constant substitution is less error-prone than copying 46 KB of text.

### 3.6 `w1/ExecFetchSelftest/fetch-vendor.py` — the r51 **fetcher with guard selftests** (20 459 B)

* **Syntax:** valid.
* **What it adds** over the landed `tools/round-50/fetch-vendor.py` (19 157 B): a
  `guard_selftests(cases)` function with three offline cases — `initial-non-https`,
  `initial-wrong-host`, `redirect-off-host` — wired into `selftest()` at L441. That is exactly
  the routed defect 4 obligation ("offline selftests proving each guard fails closed").
* **Measured: the added selftest CRASHES — a regression.** With the draft placed at its
  intended location (`tools/round-51/fetch-vendor.py` in the scratch clone, so its
  `../..` lane-root resolution works) the selftest exits **1** with:

  ```
  File ".../fetch-vendor.py", line 293, in guard_selftests
      opener.handle_error(
  TypeError: 'dict' object is not callable
  ```

  Mechanism (confirmed): `urllib.request.build_opener(...).handle_error` is the
  **handler-dispatch dict** `{'http': {'default': [...], 301: [...], …}}`, not a method. The
  draft calls it as a method. The landed r50 fetcher's own selftest is **green 16/16**
  (receipt `r50_fetch_vendor_selftest`, exit 0), so this draft turns a green selftest into a
  traceback.
* **Correct call, measured:** calling the handler's own method refuses as intended —
  `m._AvmOnlyRedirect().redirect_request(req, None, 302, 'Found', {'Location': 'http://example.invalid/redirect'}, 'http://example.invalid/redirect')`
  raises `HTTPError('redirect off download.avm.de refused')` → receipt
  `redirect_guard_corrected`, exit 0, sha `2a40d5a1…`.
* **Verdict: USE-DRAFT (the guard-test intent) + FIX the redirect probe.** The two URL guards
  (`fetch()` raising `ValueError('url outside https://download.avm.de: …')`) are already correct
  in the r50 source; only the redirect-guard probe needs rewriting. Note the draft also assumes
  it lives at `tools/<round>/fetch-vendor.py` — run from a wave directory it resolves
  `../..` to the wave dir and dies with `FileNotFoundError: …/w1/round-41/sqfs-list.py`
  (measured), which is a placement artifact, not a defect.

### 3.7 `w1/ExecRuleDerive/gap-rule-v2.json` — the r51 **law rule draft** (604 B)

* **Syntax:** valid JSON (`json.load` exit 0).
* **Delta vs the landed `tools/round-50/gap-rule.json`:** `claim` → `R51-C1`;
  `required['char-device']` → `false`; `removed.silent` → `{}` (the per-detail whitelist
  removed). Everything else (including `allowed`) is **unchanged**:
  `allowed['char-device'] = ['unpublished-entry']`, `allowed['fifo'] = ['unpublished-entry']`,
  `allowed['socket'] = ['unpublished-entry']`.
* **Why that is wrong for r52:** r52's `law_shape_ok` clause requires
  "`allowed` for those kinds is the empty list" (r52 claims §R52-C1, predicate bullet).
  The r51 draft's rule **fails** `law_shape_ok` — as does the r51 draft's own `ExecControls`
  "new" variant, and as does the law rule I had to write by hand to get CTL-NEW 4/4 in §3.1.
  The law rule that actually passes is:
  `allowed = {symlink:['unpublished-entry'], char-device:[], block-device:[], fifo:[], socket:[], dir:[]}`,
  `required = {symlink:true, char-device:false, block-device:false, fifo:false, socket:false, dir:false}`,
  `removed.silent = {}`.
  **This is exactly the shape the r51 L1 counter draft's own selftest `law_rule()` helper
  builds (L4522-4530)** — use that as the canonical r52 `gap-rule.json` starting point.
* **Verdict: PORT-FROM-R50-SOURCE + apply F3/F4.** The r51 draft is a whitelist-era artefact;
  take `tools/round-50/gap-rule.json` and apply the law shape above.

### 3.8 `w1/ExecOfflineGrammar/` — the r51 **offline receipt-ingestion grammar**

* `grammar.md` (4 380 B) — the authoritative description of the envelope fields the counter
  reads (`after.json` is the payload; `run.json` is harness metadata). **Verdict: USE as prose.**
  It is the single best statement of *which* bytes the controls must ingest.
* `disposition-dryrun.py` (58 lines, `py_compile` exit 0) — a **standalone re-implementation**
  of the three-family disposition check over the four committed round-50 envelopes. Its own
  recorded run: **R50 2/4, law 4/4** — the same numbers I independently measured with the
  counter draft's `--controls` mode. **Verdict: USE as an independent cross-check oracle**
  (it is the cheapest possible proof that CTL-OLD/CTL-NEW are the right expectations), but it
  is *not* the r52 control driver — it reads a hard-coded lane path, not `--root/--rev`.

### 3.9 Everything else in the wave

| draft | what it is | r52 use |
|---|---|---|
| `w1/MutGapRule/` (battery, amended-battery, amended-law-battery, law-enforcement-probe, `amended-expected-verdicts.md`) | the r51 gap-rule mutation battery + expected-verdict table | **SPEC** — the M1–M4 arms r52 inherits |
| `w1/MutTriV6/battery.md` + `probe/` | the r51 triage-v6 mutation battery (D1/D2/D3 detectors, precedence, 15 mutants) | **SPEC** — this, not the v6 draft, is the v6 port source |
| `w1/MutControlsV2/` | attack on the r51 controls designs (dead-control hunting) | evidence; read before freezing the r52 controls |
| `w1/CritCounterV2/findings.md` (48 KB), `w1/CritRuleDerive/findings.md` (30 KB) | the two big critic attacks | the r51 amendment record F1–F11 is already baked into the r52 claims — read for re-derivations |
| `w1/SimpV1Audit/audit.md` | "dead weight the v2 port must drop" | read before porting the counter; it is the trim list |
| `w1/RevCounterPort/checklist.md` (66 KB), `w1/RevTriPort/checklist.md` (14 KB) | port-fidelity checklists | **SPEC** — the port audit trail |
| `w1/ScribeEntryC1/entry.md` (38 KB), `w1/ScribeProvince/*`, `w1/ScribeReadme/*`, `w1/ScribeScorecard/section.md`, `w1/ScribeLesson/lesson.md`, `w1/ScribeSources/rows.md` | the r51 documentation drafts | evidence for the r52 doc/source/assimilation seats; **not** a port source (they name the r50/r51 entry stems) |
| `w1/CritCensus/`, `w1/ScoutCensusRecheck/`, `w1/ExecCensusDrift/census3.py` | the census3 work | census3 **landed**; the r52 v6 audit must use `tools/round-51/census3.json` |
| `w1/ScoutMksquashfs/` | the mksquashfs padding source (R51-C2 grounding) | already in `corpus/SOURCES.md` (S250/S251) |
| `w1/ExecMisrootSweep/misroot-sweep.sh` (3 517 B, `bash -n` exit 0) | the r51 stray-sweep helper | **USE-DRAFT + FIX — see §4.6** |
| `w1/RevFetchGuards/`, `w1/RevExtractor/`, `w1/RevSweep/`, `w1/SentCreds/`, `w1/ConnSiblings/`, `w1/ConnSources/` | reviews / scans | evidence only |
| `l1/census3-*.json`, `l1/integrity*.json`, `l1/registry-*.json`, `l1/wave-accounting.json` | the r51 L1's own bookkeeping | evidence only |

---

## 4. New findings the r51 wave did not catch (the L1 must not port blindly)

These are **measured**, not inferred, and they are the reason the port-from verdict above is
"port from the r50 source + the r51 spec", not "copy the r51 draft".

### 4.1 The r51 counter draft is missing two flags r52's claims name
`plans/round-52-claims.md:131` requires the v2 counter to expose
`--gap-rule`, `--receipts`, **`--provenance-base`**, **`--receipt-fresh-base`**, and the control
driver to pin the round-50 values. The r51 draft exposes the first two only. **Delta required.**

### 4.2 `depth_gap_recorded` vs `depth_gaps_recorded`
r52's predicate names `depth_gap_recorded`; the r51 draft emits `depth_gaps_recorded`
(`res['depth_gaps_recorded']`, L2685). Pick one and make the claim text, the counter docstring
and the receipt key agree — the r52 claims explicitly require "the same sentence in this file,
the counter docstring, and the receipt label".

### 4.3 The r52 C2 **before-arm cannot carry the round-52 freeze**
r52's C2 before-arm is "at the declared claims-draft base … the same command with
`--table tools/round-50-c3` … exits 1". The v5/v6 instrument's freeze gate
(`sqfs-triage-v5.py:1261`) raises `Unevaluable('freeze %r is not an ancestor of %r')` → **exit 2**
when the freeze is not an ancestor of `--rev`. The round-52 freeze is created *after* the
claims-draft commit `ab0eafed…`, so the freeze is **not** an ancestor of the before-arm rev:
the before-arm as written would exit 2, not 1. MutTriV6 already flagged this landmine for r51
("the before-arm cannot carry the round-51 `--freeze` … exit 2"); **it is still unaddressed in
the r52 claims.** The v6 instrument needs an explicit before-arm mode (e.g. `--freeze` optional
in the before-arm, or a pre-freeze base passed as the freeze) *and* that must be stated in the
amended claims.

### 4.4 `census_outside 0` at both sides requires re-deriving census3 at the r52 freeze
`tools/round-51/census3.json` was generated at rev `02d667cb` and lists 57 paths. The r52 freeze
adds five new registry rows under `tools/round-52/` (counter, controls, harness, fetcher,
triage v6) plus `misroot-sweep.sh` if registered. If the v6 audit compares the registry against
the **frozen** census3.json, `census_outside` will be **5–6, not 0**. MutTriV6 measured
`census_outside 13` against `census2.json` at the r51 base for exactly this reason. The r52
freeze must regenerate `tools/round-52/census3.json` (or a round-52 census) at the freeze commit
and the audit must read *that*. (The r52 claim's "no-regression binding" wording assumes the
census is re-derived, not that the old artefact is reused.)

### 4.5 The r51 `ExecControls` driver cannot drive the r51 counter (measured)
See §3.4 — missing `--rev` and the wrong receipt key. Any r52 controls driver copied from it
inherits both. The `dispositions_matched` key is also the name r52's CTL arms should quote, not
`carriers_matched` (the latter is the *scoring* key of the full predicate, a different thing —
conflating them is how the r51 driver would have reported "misbehaved" for a correct CTL-NEW).

### 4.6 `misroot-sweep.sh` must lose its `--apply` mode
r52 routed defect 5 requires "a **read-only** sweep helper `tools/round-52/misroot-sweep.sh`
(reads `git -C <fleet> status --porcelain`, classifies strays by content, **never writes**)".
The r51 draft has an `--apply` mode that **copies files out of the fleet repo into the lane**
(`copy_file` → `cp` + `cmp` + `rm`), i.e. it writes to the fleet tree. Port the classifier and
the fixture-repo selftest; **drop `--apply`**. The classifier also keys on the literal string
`round-51` → must become `round-52`.

### 4.7 The r51 triage v6 draft regressed a green instrument into a non-compiling one
See §3.3. The r52 triage v6 is a **from-scratch port of v5** plus the audit, the `--table`
flag, the census clause and the freeze-drift gating; the r51 v6 draft contributes one usable
thing: the exact shape of the new table row (`legacy-body-unreadable` /
`preserve-unresolved` / `squashfs_v3_ddwrt` / `extractor-failure+`).

---

## 5. Draft → r52 target map, with the sed-able deltas

| r52 target (path under the lane) | port from | deltas to apply |
|---|---|---|
| `tools/round-52/gap-rule.json` | `tools/round-50/gap-rule.json` + r51 `law_rule()` helper shape | `claim` → `R52-C1`; `required['char-device']` → `false`; `removed.silent` → `{}`; `allowed['char-device'\|'block-device'\|'fifo'\|'socket']` → `[]` (keep `allowed['symlink']=['unpublished-entry']`) |
| `tools/round-52/c1-counter.py` | **`l1/drafts/c1-counter.py`** (the L1-merged v2 counter) | `round-51` → `round-52`; `R51-C1` → `R52-C1` (rule-label set → `{R50-C1, R52-C1}`); `kaidoku-r51` → `kaidoku-r52`; `tools/round-51/` → `tools/round-52/` in `FROZEN_PREFIXES` (keep `tools/round-50/oracle/`); `GAPRULE`/`AFTERDIR`/`CARRIERS`/`COUNTER_PATH` paths; `ENTRY`/`STEM`/`CORE_HEADING`/`FRONTIER_MARK`/`OPENED_DATES`/`PROV_BASE`/`PROV_SEGMENT` → the r52 constants; `depth_gaps_recorded` → `depth_gap_recorded`; **add** `--provenance-base` and `--receipt-fresh-base`; `PRIOR_CARRIER_TABLES` → add `tools/round-50/carriers.json`; `PRIOR_PIN_CANDIDATES` → the r52 chain |
| `tools/round-52/c1-controls.py` | `w1/ExecControls/c1-controls.py` (shape) + `tools/round-50/c1-controls.py` (semantics of the fixture controls) | add `--rev` to the counter argv; read `dispositions_matched`; replace the "new" variant with the **law** rule; add M1 (all-thirteen whitelist), M2 (fourteenth-device fixture), M3/M4 regressions; keep CTL-OLD/CTL-NEW/CTL-DN/CTL-JUNK |
| `tools/round-52/c1-run.sh` | `tools/round-50/c1-run.sh` | `ROUND_SEGMENT=kaidoku-r52`, `SCRATCH_PREFIX=/fast/scratch/hyaku/kaidoku-r52/`, `EVIDENCE_SEGMENT=/corpus/evidence/round-52/`, schema `kaidoku-r52-c1-run-v1`, claim `R52-C1` |
| `tools/round-52/fetch-vendor.py` | `tools/round-50/fetch-vendor.py` + r51 `guard_selftests` intent | `CARRIERS` → `tools/round-52/carriers.json`; **rewrite** the redirect-guard probe to call `_AvmOnlyRedirect().redirect_request(...)`; add the "guard deleted → selftest red" clone-and-delete case |
| `tools/round-52/sqfs-triage-v6.py` | `tools/round-50-c3/sqfs-triage-v5.py` + `MutTriV6/battery.md` (spec) | add the `legacy-body-unreadable` row **below** `legacy-body-failure` and drop `squashfs_v3_ddwrt` from the legacy cell; wire the evaluator; add the D2 executability audit (reader census) and the D3 census clause against the **round-52** census; add `--table`; add freeze-drift gating; add the fail-closed gates for a missing audit/census |
| `tools/round-52/misroot-sweep.sh` | `w1/ExecMisrootSweep/misroot-sweep.sh` | **drop `--apply`** (read-only only); classifier string `round-51` → `round-52`; keep the fixture-repo selftest |

---

## 6. Port-from verdict summary

| draft | verdict | one-line reason |
|---|---|---|
| `l1/drafts/c1-counter.py` | **use-draft** | only complete v2 counter; measured CTL-OLD 2/4 exit 1 and CTL-NEW 4/4 exit 0 |
| `w1/ExecControls/c1-controls.py` | **use-draft (shape) + fix** | missing `--rev`, wrong receipt key, whitelist "new" rule |
| `w1/ExecFetchSelftest/fetch-vendor.py` | **use-draft (intent) + fix** | redirect probe raises `TypeError`; r50 selftest is already green 16/16 |
| `w1/ExecMisrootSweep/misroot-sweep.sh` | **use-draft + fix** | `--apply` writes to the fleet tree; r52 requires read-only |
| `w1/ExecRuleDerive/gap-rule-v2.json` | **port-from-r50-source** | its `allowed` still admits device gaps → fails r52's `law_shape_ok` |
| `w1/ExecTriV6/sqfs-triage-v6.py` | **port-from-r50-source** | `SyntaxError` (`CUT 1033.=1033`), duplicate row, evaluator not wired, no audit, no `--table` |
| `w1/ExecCounterV2/c1-counter.py` | **port-from-r50-source** | 36-line path-constant diff over the r50 counter; implements none of F1–F10 |
| `l1/drafts/c1-run.sh` | **port-from-r50-source** | 39-line constant diff; no behavioural change |
| `w1/ExecOfflineGrammar/disposition-dryrun.py` | **cross-check oracle** | independent 2/4 → 4/4 proof, not the r52 driver |
| `w1/MutGapRule/`, `w1/MutTriV6/`, `w1/RevCounterPort/`, `w1/RevTriPort/` | **spec** | the mutation batteries and port checklists the r52 freeze should be audited against |
| `w1/Scribe*`, `w1/Scout*`, `w1/Conn*`, `w1/Crit*`, `w1/Rev*` (rest), `l1/*.json` | **evidence-only** | round-51 evidence; not a port source |

---

## 7. Open unknowns (not resolved by this seat)

1. Whether the r52 carriers table should carry `prior_pins`/`re_scored_pins` in the **r51 draft's**
   grammar (64-hex lists, L934-948) — the r52 claims require the four pins listed and the
   waiver visible in the receipt, but not the exact field names. The L1 owns the freeze.
2. Whether `tools/round-52/` gets its own `carriers.json` (the r51 draft's `CARRIERS` constant
   points at `tools/round-51/carriers.json`); r52's claim says the four pins are "listed in the
   round-52 carrier table's `prior_pins`", implying a new table. **L1 decision.**
3. The exact reader-census artefact the v6 audit freezes (MutTriV6 M15 wants it bound to
   `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:104`); the r52 claims cite the
   round-49 entry but do not name the artefact path. **L1 decision.**

---

*Receipts:* `receipts/receipts.tsv` (every command, exit code, stdout sha256, UTC) and the
per-label stdout/stderr dumps in `receipts/*.out`; the machine-generated draft table is
`receipts/draft-table.md`; the probe JSON receipts are `receipts/ctl-old.json` and
`receipts/ctl-new.json`. The recorder is `record-receipts.sh` (re-runnable; it writes only
into this seat directory and `$S`).
*No lane file outside this seat directory was written; no REA, no data run, no network, no
git mutation in the lane or the fleet repo.*
