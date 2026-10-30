# R51-C2 — triage v6 mutation battery (spec + measured expectations)

Seat `MutTriV6`, round 51 wave 1 (build). All numbers in this file are **measured**
offline from committed lane bytes by the four probes in `probe/` (receipts:
`receipts/probe-receipts.tsv`; probe JSON: `probe/probe-v6-*.json`). No REA, no data
run, no lane write outside this seat directory.

Sources read (read-only): `tools/round-50-c3/sqfs-triage-v5.py` (2,311 lines),
`plans/round-51-claims.md` (R51-C2), `.ufo/waves/round-50/c3/ctl-*.json` (the round-50
control receipts), `.ufo/waves/round-50/w3/ExecTriageControls/` (the control surfaces
and their builder), `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`
(the frozen 126-envelope corpus), `tools/round-48/census2.json` + `census2.py`,
`SKILL.md` at `1aa27369…` and `f04b51dd…` (read via `git show`).

---

## 0. The three detectors v6 has, and the exit map

| id | detector | what it compares | v6 value at the freeze |
|---|---|---|---|
| **D1** | `pair_mismatches` | the SKILL.md table's (label, action) against the fixed v6 evaluator, over the frozen 126 envelopes | `0` |
| **D2** | `executability_violations` | every FAILED-body envelope's **prescribed action** against the frozen reader census: a cross-read prescribed where the census says the body has no reader | `0` |
| **D3** | `census_outside` | registered instrument paths (SKILL.md `instrument-registry v2` region) absent from the active census artifact | `0` |

Exit map (semantic, per the lane's convention): **0** = D1=0 ∧ D2=0 ∧ D3=0 ∧ selftest
green; **1** = at least one violation (D1>0 ∨ D2>0 ∨ D3>0 ∨ a selftest case failed);
**2** = could-not-evaluate (a detector could not run: audit absent, census artifact
absent/unreadable, registry region malformed, frozen-path drift, a parse refusal).

**D2 is the only detector that does not trust the table.** D1 compares the table to the
evaluator, so a *coordinated* mutation (table and evaluator changed together) is blind
to D1; D2 compares the table to an independent census and catches that class. D3 is
independent of both. The battery below is built so that **every mutant is caught by at
least one detector, and the two "audit-only" mutants are caught by both.**

---

## 1. The v6 table shape the battery assumes (required of the port)

The measurements below pin the table shape; the port must match it or the named
mutants change meaning.

1. The `legacy-body-failure` row's **failing-handler cell drops `squashfs_v3_ddwrt`**
   (v5 cell: `squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt` → v6 cell:
   `squashfs_v1,squashfs_v2,squashfs_v3`).
2. A new row `legacy-body-unreadable` is inserted **immediately below**
   `legacy-body-failure`: handler `squashfs_*`, failing handler `squashfs_v3_ddwrt`,
   gap kinds `extractor-failure+`, published files `0`, action **`preserve-unresolved`**
   (no cross-read), plus the v5 cause/source prose style (`… -> …` in the cause cell,
   which the v5 parser requires).
3. The v6 evaluator implements the same precedence: a FAILED body whose failing handler
   is in the ddwrt family → `('legacy-body-unreadable','preserve-unresolved')`.
4. Every other v5 label and action is unchanged; the v5 vocabulary already contains
   `preserve-unresolved`, so the actions line does not change.

**Precedence constraint — MEASURED, not asserted** (`probe/probe-v6-precedence.json`):

| placement of the new row | legacy glob broadened to `squashfs_v[123]*` | D1 | D2 | verdict |
|---|---|---|---|---|
| **below** `legacy-body-failure` (required) | yes | 1 | 1 | **RED — detected** |
| below | no (pristine) | 0 | 0 | green |
| above `legacy-body-failure` | yes | 0 | 0 | **GREEN — NO-OP** |
| above | no (pristine) | 0 | 0 | green |

If the port puts the new row *above* the legacy row, the required
"ddwrt glob broadened back into `legacy-body-failure`" control is a **no-op**: nothing
observes it, so the guard around it is dead. **Freeze the new row below the legacy
row.** (The legacy cell must also drop ddwrt; keeping ddwrt in the legacy cell with the
new row below it would leave the ddwrt body unroutable to the new row.)

---

## 2. The battery — corpus scope (D1/D2 over the frozen 126 envelopes)

Every expectation in this table is measured (`probe/probe-v6-battery.json`,
`probe/probe-v6-before-arm.json`, `probe/probe-v6-precedence.json`).

### 2.1 The four round-50 carryover controls (re-used surfaces)

The round-50 control **surfaces** are the committed documents
`.ufo/waves/round-50/w3/ExecTriageControls/ctl-{do-nothing,guard-deleted,action-swapped}.skill.md`
(v4 marker) and `.ufo/waves/round-50/c3/ctl-junk.skill.md` (unique labels).

| control | surface sha256 (head) | D1 under the **v5** evaluator (round-50 receipt) | D1 under the **v6** evaluator | D2 | must be |
|---|---|---|---|---|---|
| CTL-DN (do-nothing, v4 table at base) | `19046cf2…` | **19** — reproduces `.ufo/waves/round-50/c3/ctl-do-nothing.json` (`pair_mismatch_count 19`) | **20** | 1 | exit 1 |
| CTL-GUARD (v4 table minus the `legacy-body-failure` row) | `16c4b8a2…` | **26** — reproduces `ctl-guard-deleted.json` (`26`) | **26** ✅ holds | 0 | exit 1 |
| CTL-ACT (v4 table, `clean` row action `none`→`inspect-input`) | `721c99e1…` | **51** — reproduces `ctl-action-swapped.json` (`51`) | **52** | 1 | exit 1 |
| CTL-JUNK (every row label `junk-clean`) | `e563aebd…` | **126** — reproduces `ctl-junk.json` (`126`) | **126** ✅ holds | 0 | exit 1 |

**The v5 carryovers do NOT all keep their round-50 numbers under v6.** Exactly two
change, each by **+1**, and the +1 is the ddwrt route change itself
(`dmg_Z3_v3ddwrt_inode_table`): the v4/v5 tables prescribe
`legacy-body-failure`/`cross-read-legacy` for it, the v6 evaluator says
`legacy-body-unreadable`/`preserve-unresolved`, so that envelope becomes a mismatch.

* **Freeze 20, not 19, for CTL-DN** and **52, not 51, for CTL-ACT** — *if* the L1 re-uses
  the round-50 v4-marker surfaces.
* **CTL-GUARD (26) and CTL-JUNK (126) are unchanged** — CTL-GUARD because the ddwrt body
  was already a mismatch there (both sides moved off the legacy row: 19 + 6 reader-backed
  legacy bodies + 1 ddwrt = 26, the same total with a different split).
* If the L1 instead re-uses the round-50 receipt numbers verbatim as the v6
  expectations, **two controls will read as misses** and the kill rule will fire
  spuriously. This is the single most likely mis-freeze in this claim.

### 2.2 The v6-native table mutants

| id | mutation (applied to the v6 table) | D1 (measured) | D2 (measured) | detector that must fire | no-op risk |
|---|---|---|---|---|---|
| **M0** | pristine v6 | **0** | **0** | — (must be green) | — |
| **M1** | `legacy-body-unreadable` row **deleted** | **1** (`dmg_Z3_v3ddwrt_inode_table`) | **0** | **D1 only** | **MEDIUM — the audit does NOT see this.** The body falls to `body-extractor-failure`/`preserve-failure`, which prescribes no cross-read, so D2 stays 0. A coordinated mutation (table + evaluator both reverted) is invisible to D1 *and* D2. The battery must therefore keep a *pair* witness for this mutant and the claim must not claim the audit covers it. |
| **M2** | the new row's action swapped back to `cross-read-legacy` | **1** | **1** | D1 **and** D2 | LOW — double-witnessed |
| **M3** | ddwrt glob broadened back into `legacy-body-failure` (legacy failing-handler cell → `squashfs_v[123]*`) | **1** | **1** | D1 **and** D2 | LOW **only if** the new row stays below the legacy row (§1, measured) — otherwise NO-OP |
| **M4** | `legacy-body-failure` row deleted (v5 carryover) | **6** (`dmg_V1`, `dmg_V2`, `dmg_V3`, `dmg_V6`, `dmg_Z1`, `dmg_Z2`) | 0 | D1 | LOW — note the count is **6, not 7**: the ddwrt body no longer sits on the legacy route |
| **M5** | `clean-unverified` row deleted (v5 carryover) | **19** | 0 | D1 | LOW |
| **M6** | `clean` row action `none`→`inspect-input` (v5 carryover) | **32** | 0 | D1 | LOW — action-half only; a label-only comparison would score it GREEN (the round-50 builder flagged this: "red only if the instrument compares (label, action) PAIRS") |
| **M7** | `clean-unverified`/`no-reader-failure` actions swapped (v5 carryover) | **19** | 0 | D1 | LOW |
| **M8** | one no-reader family moved out of `clean-unverified` (`squashfs_v3_broadcom`) | **7** | 0 | D1 | LOW |
| **M9** | `clean-unverified` row moved below the `clean` row (v5 carryover) | **19** | 0 | D1 | LOW |
| **M10** | a handler cell blanked (v5 carryover) | parse refusal: `handler cell '' has an empty alternative` | — | the **parser** (exit 2) | LOW — the refusal is the witness; never a silent non-match |

### 2.3 The three new mutants the claim names (code-level, not table-level)

These are the claim's "audit-guard-deleted mutant → red" and "census-guard-deleted
mutant → red". They delete a **guard**, i.e. a piece of the instrument, so they cannot
be expressed as a table mutation. They carry the highest no-op risk in the whole
battery, and the mitigation is structural.

| id | mutation | what it must flip | how the selftest witnesses it | no-op risk and the required mitigation |
|---|---|---|---|---|
| **M11** | **audit guard deleted** (the D2 computation/call removed from the instrument) | **must not exit 0.** The receipt must carry `executability_violations`; a missing audit is exit **2** (`audit_missing`, could-not-evaluate) or exit **1** (`executability_violations` reported as unknown) — never a green run | a selftest case copies the instrument into the work dir, deletes the audit call textually, runs the clone on the fixture envelopes, and asserts `returncode != 0` **and** that the receipt lacks/flags the key | **HIGH.** Without a fail-closed gate this is a pure no-op: the run would report D2=0 (nothing found) and exit 0 — a *deleted* audit reads as a *passing* audit. Required: (a) the receipt gate (v5 already has one: the receipt must exist, parse and carry the required keys — extend the key list with `executability_violations` and `census_outside`); (b) the run path computes the audit **before** the verdict and refuses to emit a verdict without it; (c) the selftest case above. |
| **M12** | **census guard deleted** (the D3 comparison removed from the instrument) | **must not exit 0.** Same shape: exit 2 (`census_missing`) or exit 1; the receipt must carry `census_outside` and the number of registry paths read | the same clone-and-delete selftest case, deleting the census comparison | **HIGH.** Identical no-op shape: a deleted census check reports "0 outside" and the run goes green. Required: the same three-part mitigation (receipt key, pre-verdict computation, selftest clone case). |
| **M13** | **the active census artifact reverted to the stale `tools/round-48/census2.json`** | **D3 = 13** → exit 1 | the census re-derive runs against the frozen artifact at `--rev`; the receipt names the artifact path and its sha256 | LOW — a direct numeric witness, and it is the **before-arm value** (measured: 13 at `1aa27369…` and at `f04b51dd…`) |
| **M14** | **one registered path dropped from `census3.json`** | **D3 = 1** → exit 1 (exact-path comparison, not basename/substring) | the same command with a mutated census artifact | LOW |
| **M15** | **the audit's reader census entry flipped** (the ddwrt no-pad body marked reader-backed) | D2 goes blind (audit stays 0) while D1 still fires for M2/M3 → the *table* mutants are still caught, but the **census error itself is unobserved** | the selftest must assert the audit's reader-census entry equals the frozen round-49 measurement (`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:104` — "squashfs_v3_ddwrt's no-pad fixture: both readers refuse (unsquashfs exit 1, 7z exit 2; receipt `v3-readers`)") | **MEDIUM-HIGH — the audit's census is a NEW trust boundary.** A wrong census silently disables D2. The census must be a frozen artifact with its own receipt, and a selftest case must bind it to its source row. Do not let the census live as an unexplained constant. |

---

## 3. The before-arm, measured

`SKILL.md` at `1aa273694f4409d3432fbcd73e83a33bee0dd8e9` (the claim's declared base)
and at `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab` (the assignment base) are the **same
bytes** (`sha256 2e6db23aabd1bc026497d62925d212ea7bbff9e4759127cee5695bcf884fa8ce`),
both carrying the **v5** table (17 rules).

| quantity | measured at both bases |
|---|---|
| D1 under the **v5** evaluator | **0** (the round-50 landed state is green) |
| D1 under the **v6** evaluator | **1** — `dmg_Z3_v3ddwrt_inode_table` (table `legacy-body-failure`/`cross-read-legacy` vs v6 `legacy-body-unreadable`/`preserve-unresolved`) |
| D2 (executability audit) | **1** — `dmg_Z3_v3ddwrt_inode_table` |
| D3 (`census_outside`) | **13** — 55 registered paths, 42 in `census2.json`, 0 duplicates |
| verdict | **exit 1** — matches the claim's before-arm (`executability_violations 1` naming `dmg_Z3_v3ddwrt_inode_table`, `census_outside 13`) |

The 13 outside paths (measured, identical at both bases):
`tools/round-49/c1-controls.py`, `tools/round-49/c1-counter.py`,
`tools/round-49/c1-oracle.py`, `tools/round-49/c1-run.py`, `tools/round-49/c1-run.sh`,
`tools/round-49/c2-mismatch.py`, `tools/round-50-c3/sqfs-triage-v5.py`,
`tools/round-50/c1-controls.py`, `tools/round-50/c1-counter.py`,
`tools/round-50/c1-run.sh`, `tools/round-50/c2-record.py`,
`tools/round-50/fetch-vendor.py`, `tools/round-50/selftest-r49-c2.py`.

**Two operational landmines this measurement exposes**

1. **The before-arm cannot carry the freeze argument.** The v5 instrument refuses a
   freeze that is not an ancestor of `--rev` (`sqfs-triage-v5.py:1257-1263` → exit 2),
   so a before-arm run at `1aa27369…` with the round-51 freeze cannot use `--freeze`.
   The before-arm needs its own bound invocation (e.g. no `--freeze`, or
   `--freeze 1aa27369…`). (Same finding as `RevTriPort` F1; it is a hard blocker for the
   claim's before-arm sentence.)
2. **`census3.json` is self-referential to the freeze.** The registry at the freeze will
   carry the round-51 rows (≈6–7 new `.py`/`.sh`: `c1-counter.py`, `c1-controls.py`,
   `c1-run.sh`, `fetch-vendor.py`, `sqfs-triage-v6.py`, the census re-derive tool,
   `misroot-sweep.sh`), so the census artifact must list **55 + the new rows**. If
   `census3.json` is derived from the pre-freeze HEAD (55 paths), the freeze scores
   **D3 = the number of new rows (≠0)** and the claim's own predicate fails. Derive
   it from the **staged** SKILL.md of the freeze commit.

---

## 4. The fixture scope — the v6 selftest's expected flip sets

The v5 selftest asserts, per mutation, the *exact* set of fixture pairs it flips
(`c_mutations_each_flip_their_own_pairs`). Under v6 those sets change. Measured
(`probe/probe-v6-fixtures.json`):

**v6 fixture set (10 fixtures, one expectation changed):**

| fixture | v5 expectation | **v6 expectation** |
|---|---|---|
| `v3ddwrt-legacy` | `legacy-body-failure`/`cross-read-legacy` | **`legacy-body-unreadable`/`preserve-unresolved`** |
| all other nine | unchanged | unchanged |

The v6 table reproduces all ten expectations (0 wrong).

**v6 mutation → flipped fixture set (measured):**

| mutation | v5 expected | **v6 expected** | changed? |
|---|---|---|---|
| `guard-row-deleted` (`clean-unverified` deleted) | `{v2ns-clean-le, v2ns-clean-be, v3bc-clean}` | **same** | no |
| `legacy-glob-widened` (cell → `squashfs_v[123]*`) | `{v2ns-failed}` | **`{v2ns-failed, v3ddwrt-legacy}`** | **yes** |
| `new-row-actions-swapped` | `{v2ns-clean-le, v2ns-clean-be, v3bc-clean, v2ns-failed}` | **same** | no |
| `no-reader-family-moved-to-clean` | `{v3bc-clean}` | **same** | no |
| `precedence-order-swapped` | `{v2ns-clean-le, v2ns-clean-be, v3bc-clean}` | **same** | no |
| `no-reader-failure-row-deleted` | `{v2ns-failed}` | **same** | no |
| `legacy-row-deleted` | `{v3-legacy, v3ddwrt-legacy}` | **`{v3-legacy}`** | **yes** |
| `unreadable-row-deleted` (new) | — | **`{v3ddwrt-legacy}`** | new |
| `unreadable-action-swapped` (new) | — | **`{v3ddwrt-legacy}`** | new |

**Two vacuity facts the v6 selftest must keep reporting** (v5's `corpus_control`
already reports `vacuous` per scope — keep that):

* `no-reader-failure-row-deleted` flips **0 corpus pairs** (measured) — the 126-envelope
  corpus holds no no-reader FAILED envelope, so the **fixture scope is its only
  witness**. A corpus-only v6 selftest would score this mutant GREEN.
* `unreadable-row-deleted` flips **1 corpus pair and 0 audit violations** (measured) —
  the corpus witness and the audit do not overlap; both scopes must be reported.

---

## 5. The kill rule for the L1 (proposed wording)

> Every control below must be **red** at the freeze: exit ≠ 0 **and** the named
> detector non-zero. A control that is green, or that is red only because the instrument
> refused to parse it (exit 2) when a detector was expected to fire, stops the claim
> (report a miss, do not narrow).
>
> | control | expected at the freeze |
> |---|---|
> | CTL-DN (the v5 table at base) | exit 1, D1 ≥ 1, D2 = 1 (`dmg_Z3_v3ddwrt_inode_table`), D3 = 13 |
> | CTL-JUNK (unique labels, every row clean) | exit 1, D1 = 126 |
> | CTL-GUARD (round-50 v4 surface, `legacy-body-failure` row deleted) | exit 1, D1 = **26** |
> | CTL-ACT (round-50 v4 surface, `clean` action swapped) | exit 1, D1 = **52** |
> | CTL-AUDIT-GUARD (the audit deleted from the instrument) | exit ≠ 0, `audit_missing` named |
> | CTL-CENSUS-GUARD (the census check deleted) | exit ≠ 0, `census_missing` named |
> | CTL-CENSUS-STALE (active artifact = `census2.json`) | exit 1, D3 = 13 |
> | CTL-CENSUS-ONE (one registered path dropped from `census3.json`) | exit 1, D3 = 1 |
> | the nine table mutants M1–M10 | each flips ≥1 detector, none a no-op (§2.2) |

---

## 6. What was NOT run (honest limits)

* No v6 instrument exists yet: `ExecTriV6`'s draft is a byte-copy of v5 (its own report
  says so), so M11/M12/M15 are specified, not executed. Every other expectation is
  measured against a *probe* evaluator (v5's evaluator with the v6 branch, in
  `probe/probe_v6*.py`) — the port must reproduce those numbers with its own code.
* No REA run, no `--data-run`, no carrier download, no network.
* The probe reads the v5 instrument by `importlib` from the lane (read-only); the
  probe scripts and their receipts are copied into this seat directory.
* No lane file was modified, no git mutation was run in the lane or the fleet repo.
* **Disclosed mistake (repaired):** the probe artifacts were first written to a
  hand-built path that dropped the `kaidoku-shokunin/` component and landed in the
  **FLEET** repo (`/home/vgpnk/Projects/shokunin/kaidoku-r51/w1/MutTriV6/`, 17 files).
  All 17 were copied byte-exact into this seat dir and `cmp`-verified, then the fleet
  copy was deleted (the one permitted fleet deletion); the fleet repo is clean again
  (`git -C /home/vgpnk/Projects/shokunin status --porcelain` empty). The L1 should
  append the matching `corpus/lessons/round-51.md` `## Mistakes` row.
