# R52-C2 — triage v6 mutation battery (spec + measured expectations)

Seat `MutTriV6`, round 52 wave 1 (build+attack). Every number in this file is **MEASURED**
offline from committed lane bytes by the probes in `probe/` (receipts: `receipts.tsv`;
evidence JSON: `evidence.json`, `design-dependence.json`, `two-scope-witness.json`).

No REA, no `--data-run`, no carrier download, no network, no lane write outside this seat
directory, no git mutation in the lane or the fleet repo.

Sources read (read-only): `tools/round-50-c3/sqfs-triage-v5.py` (2,311 lines; sha256
`f29eb92073dfff0c…`), `plans/round-52-claims.md` (R52-C2), `.ufo/waves/round-50/c3/ctl-*.json`
(the committed round-50 control receipts), `.ufo/waves/round-50/w3/ExecTriageControls/`
(the control surfaces + their builder), `.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`
(the frozen 126-envelope corpus), `tools/round-51/census3.py` + `census3.json`,
`tools/round-48/census2.json`, `SKILL.md` at `ab0eafe…`, and
`.ufo/waves/round-49/w1/C1ScribeEntry/v3-readers.out` (the ddwrt reader measurement).

---

## 0. What changed since round 51, and why this battery is not a copy of the r51 one

Round 51 landed **no instrument and ran no data** — but it *did* land
`tools/round-51/census3.py` + `census3.json` (commit `96aee1a5`). That changes two
things the r51 battery had to guess at:

1. **The census drift 13 → 0 already landed.** Measured at the claims-draft base
   `ab0eafe…`: registry = **56** paths, `census3.json` = **56** paths,
   `census_outside` = `[]`, `census3.py --check` exit **0** (receipt R04, R11).
   The r51 battery's before-arm expected `census_outside 13` against the *round-48*
   `census2.json`; with the round-51 artifact active that number is **0**, and
   `census2.json` is now the *stale* artifact (measured: `census_outside` = **14** with
   `census2.json` as the active artifact at the current registry — receipt R06; the 14th
   is `tools/round-51/census3.py`, registered by round 51 itself).
2. **R52-C2's claim text changed the census clause.** It says the v6 instrument
   **embeds** the census clause and reports `census_outside` at both before and after,
   with `census3` treated as "landed in round 51 — a no-regression binding". So the
   census guard in v6 is a **no-regression** clause, not a re-derivation.

Everything else about the battery's *shape* is unchanged from the r51 spec, because the
r51 spec's three findings all survive re-measurement. They are restated below with this
round's numbers.

---

## 1. The three detectors v6 has, and the exit map

| id | detector | what it compares | v6 value at the freeze |
|---|---|---|---|
| **D1** | `pair_mismatches` | the SKILL.md table's (label, action) against the fixed v6 evaluator, over the frozen 126 envelopes | `0` |
| **D2** | `executability_violations` | every FAILED-body envelope's **prescribed action** against the frozen reader census: a cross-read prescribed where the census says the body has no reader | `0` |
| **D3** | `census_outside` | registered instrument paths absent from the active census artifact | `0` |

Exit map (semantic, the lane's convention): **0** = D1=0 ∧ D2=0 ∧ D3=0 ∧ selftest green;
**1** = at least one violation (D1>0 ∨ D2>0 ∨ D3>0 ∨ a selftest case failed); **2** =
could-not-evaluate (a detector could not run: audit absent, census artifact
absent/unreadable, registry region malformed, frozen-path drift, a parse refusal).

**D2 is the only detector that does not trust the table.** D1 compares the table to the
evaluator, so a *coordinated* mutation (table and evaluator changed together) is blind to
D1; D2 compares the table to an independent census and catches that class. D3 is
independent of both. The battery below is built so that **every mutant is caught by at
least one detector, and the audit-visible mutants are caught by two.**

---

## 2. The v6 table shape the battery assumes (required of the port)

The measurements below pin the table shape; the port must match it or the named mutants
change meaning. This is the same shape the r51 battery required, and the port must not
drift from it.

1. The `legacy-body-failure` row's **failing-handler cell drops `squashfs_v3_ddwrt`**
   (v5 cell `squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt` → v6 cell
   `squashfs_v1,squashfs_v2,squashfs_v3`).
2. A new row `legacy-body-unreadable` is inserted **immediately below**
   `legacy-body-failure`: handler `squashfs_*`, failing handler `squashfs_v3_ddwrt`,
   gap kinds `extractor-failure+`, published files `0`, action **`preserve-unresolved`**
   (no cross-read), plus the v5 cause/source prose style (the v5 parser requires the
   `… -> …` arrow in the cause cell).
3. The v6 evaluator implements the same precedence: a FAILED body whose failing handler
   is `squashfs_v3_ddwrt` → `('legacy-body-unreadable','preserve-unresolved')`.
4. Every other v5 label and action is unchanged; `preserve-unresolved` is already in the
   v5 vocabulary, so the actions line does not change.

### 2.1 Precedence constraint — MEASURED, and it splits the battery in two

`design-dependence.json` measures both candidate placements against the same six
mutants. **The placement decides whether a required control has a corpus witness.**

| mutant | **A**: legacy cell drops ddwrt, new row **BELOW** legacy | **B**: legacy cell keeps ddwrt, new row **ABOVE** legacy |
|---|---|---|
| base (pristine) | D1=0 D2=0 | D1=0 D2=0 |
| `legacy-body-unreadable` row **deleted** | D1=**1** D2=**0** | D1=**1** D2=**1** |
| new row's action → `cross-read-legacy` | D1=1 D2=1 | D1=1 D2=1 |
| legacy failing-handler cell → `squashfs_v[123]*` | D1=**1** D2=**1** | D1=**0** D2=**0** |
| new row's failing-handler cell → `squashfs_v[123]*` | D1=**0** D2=**0** | D1=**6** D2=**0** |
| new row moved **below** `body-extractor-failure` | D1=1 D2=0 | D1=1 D2=1 |
| new row's gap-kind cell `extractor-failure+` → `extractor-failure` | D1=0 D2=0 | D1=0 D2=0 |

Reading of the table:

* **Design A is required for the claim's own named control.** R52-C2 names "the ddwrt
  glob broadened back into `legacy-body-failure`" as a required mutant that must be
  red. Under **B** that mutant is a **complete no-op** (0/0): the new row sits above the
  legacy row, so widening the legacy row's cell changes nothing the corpus can see — the
  guard around it is dead. Under **A** it flips **both** detectors (1/1). **Freeze
  design A: legacy cell drops ddwrt, new row below the legacy row.**
* **Design A has the weaker witness for M1** (row deleted): D1 fires, D2 does not. Under
  B, deleting the row leaves the ddwrt body on the legacy row, so the audit *does* fire.
  This is the price of A and it is acceptable **only because D1 fires** — see the no-op
  risk on M1 (§4).
* **The gap-kind `+` suffix is invisible on the corpus in BOTH designs** (D1=0 D2=0
  either way). Reason, measured: the corpus holds **exactly one** envelope with
  `extractor-failure` *plus* another gap kind (`dmg_V4d1_data_tail`, gaps
  `[depth-limited, extractor-failure, unpublished-entry]`, **P=155**), and that one is
  routed by `partial-body-failure` (P>0), never reaching the new row's `P=0` condition.
  The corpus therefore cannot distinguish `extractor-failure+` from `extractor-failure`
  for the new row. **A selftest case must witness it from the fixture scope** (a
  synthetic zero-file ddwrt FAILED envelope carrying a second gap kind), or the `+`
  suffix is an unverified part of the table.

---

## 3. The battery — corpus scope (D1/D2 over the frozen 126 envelopes)

All expectations measured (`evidence.json`, `two-scope-witness.json`). Design A is the
assumed shape.

### 3.1 The four round-50 carryover controls (re-used surfaces)

The round-50 control **surfaces** are the committed documents
`.ufo/waves/round-50/w3/ExecTriageControls/ctl-{do-nothing,guard-deleted,action-swapped}.skill.md`
and `.ufo/waves/round-50/c3/ctl-junk.skill.md` (unique labels). Measured by scoring
each surface with the v6 evaluator over the corpus (receipt R07):

| control | committed receipt (v5 evaluator) | **under the v6 evaluator (measured)** | D2 | must be |
|---|---|---|---|---|
| CTL-DN (do-nothing, v4 table at base) | `ctl-do-nothing.json` → `pair_mismatch_count 19` | **20** | **1** (`dmg_Z3_v3ddwrt_inode_table`) | exit 1 |
| CTL-GUARD (`legacy-body-failure` row deleted) | `ctl-guard-deleted.json` → `26` | **26** ✅ holds | 0 | exit 1 |
| CTL-ACT (`clean` row action `none`→`inspect-input`) | `ctl-action-swapped.json` → `51` | **52** | **1** (`dmg_Z3_v3ddwrt_inode_table`) | exit 1 |
| CTL-JUNK (every row label `clean`) | `ctl-junk.json` → `126` | **126** ✅ holds | 0 | exit 1 |

**The v5 carryovers do NOT all keep their round-50 numbers under v6.** Exactly two
change, each by **+1**, and the +1 *is* the ddwrt route change itself
(`dmg_Z3_v3ddwrt_inode_table`): the v4/v5 tables prescribe
`legacy-body-failure`/`cross-read-legacy` for it, the v6 evaluator says
`legacy-body-unreadable`/`preserve-unresolved`.

* **Freeze 20, not 19, for CTL-DN** and **52, not 51, for CTL-ACT.**
* CTL-GUARD (26) and CTL-JUNK (126) are unchanged. CTL-GUARD because the ddwrt body was
  already a mismatch there (both sides moved off the legacy row: 19 + 6 reader-backed
  legacy bodies + 1 ddwrt = 26, same total, different split).
* **The v5 evaluator reproduces the committed receipts exactly** (19/26/51/126 measured
  on the same surfaces) — the baseline is confirmed, not assumed.
* If the L1 re-uses the round-50 receipt numbers verbatim as the v6 expectations, **two
  controls read as misses and the kill rule fires spuriously.** This is the single most
  likely mis-freeze in the claim, and it is the r51 finding re-confirmed by measurement.

> **A second, new hazard the L1 must not walk into:** `ctl-junk.skill.md` as committed
> in `.ufo/waves/round-50/c3/` is a **v4-marker document with duplicate `clean` labels**
> — the frozen v5 parser **refuses** it (`duplicate label 'clean'`, exit 2). It parses
> only because the *round-50* scoring used the v4-era instrument's weaker duplicate
> check. Under v6 the junk control must be **regenerated with unique labels** (as v5's
> own `_junk_table()` does), or the control is unscoreable as a mismatch red and becomes
> an exit-2 refusal — which is a *refusal*, not the required `pair_mismatches > 0`.

### 3.2 The v6-native table mutants (design A)

**The `class` column is measured**, per mutant, in `mutant-classification.json`:
`RED-CORPUS` = the corpus scope fires; `CORPUS-VACUOUS` = the corpus is green and the
**fixture** scope is the only witness; `NO-OP` = neither scope fires; `PARSE-REFUSED` =
the parser refuses (exit 2) and the refusal is the witness.

**The fixture scope below is the base set (11 fixtures).** One extra synthetic fixture
(`v3ddwrt-multigap`, §5) promotes **M7** from `NO-OP` to `CORPUS-VACUOUS` — measured,
and it is the only mutant that extra fixture changes.

| id | mutation (applied to the v6 table) | D1 | D2 | class | detector that must fire | no-op risk |
|---|---|---|---|---|---|---|
| **M0** | pristine v6 | **0** | **0** | green | — (must be green) | — |
| **M1** | `legacy-body-unreadable` row **deleted** | **1** (`dmg_Z3_v3ddwrt_inode_table`) | **0** | RED-CORPUS | **D1 only** | **HIGH — the audit does NOT see this** (measured). The body falls to `body-extractor-failure`/`preserve-failure`, which prescribes no cross-read, so D2 stays 0. A *coordinated* mutation (table + evaluator both reverted) is invisible to D1 **and** D2. **Consequence: the claim must NOT claim the audit covers this row, and the battery must keep a pair witness for it.** Under design B D2 would fire — the only argument for B, and it loses on M3 (§2.1). |
| **M2** | the new row's action swapped back to `cross-read-legacy` | **1** | **1** | RED-CORPUS | D1 **and** D2 | LOW — double-witnessed |
| **M3** | ddwrt glob broadened back into `legacy-body-failure` (legacy failing-handler cell → `squashfs_v[123]*`) | **1** | **1** | RED-CORPUS | D1 **and** D2 | LOW **only if** design A is frozen (§2.1) — under design B this is a **complete no-op** |
| **M4** | new row's **failing-handler** cell broadened to `squashfs_v[123]*` (the new row swallows the reader-backed v1/v2/v3 families) | **0** | **0** | CORPUS-VACUOUS | **fixtures only** (flips `v2ns-failed`) | **MEDIUM.** Under design A the new row sits *below* the legacy row, so a widened new-row cell never reaches v1/v2/v3 (the legacy row wins them first) and the corpus sees nothing. Under design B it fires D1=6. **The battery must report this mutant's corpus scope as VACUOUS and witness it from the fixture scope** — a corpus-only selftest scores it GREEN. |
| **M5** | new row moved **below** `body-extractor-failure` (precedence lost) | **1** | **0** | RED-CORPUS | D1 | LOW — the corpus witness holds; the audit is blind (the body lands on `preserve-failure`). Same shape as M1. |
| **M6** | new row moved **above** `legacy-body-failure` | **0** | **0** | **NO-OP** | **nothing** | **EXPECTED NO-OP in design A — and it is a witness, not a defect.** In design A the legacy row's cell no longer names ddwrt, so the two rows cannot compete for the ddwrt body and their relative order is immaterial. **Under design B this mutation is the whole design** (§2.1) — which is exactly why design A is the safer freeze: the ordering is not load-bearing, the *cell content* is. |
| **M7** | new row's gap-kind cell `extractor-failure+` → `extractor-failure` | **0** | **0** | **NO-OP** with the base fixture set; **CORPUS-VACUOUS** with the extra `v3ddwrt-multigap` fixture (flips exactly that fixture) | the extra synthetic fixture | **MEDIUM — the `+` suffix is UNVERIFIED by the corpus.** Measured: the only multi-gap `extractor-failure` envelope in the corpus (`dmg_V4d1_data_tail`, gaps `[depth-limited, extractor-failure, unpublished-entry]`) has **P=155** and is routed by `partial-body-failure`, never reaching the new row's `P=0` condition. **The selftest MUST carry the multi-gap fixture or it must not claim the `+` suffix is verified.** |
| **M8** | `legacy-body-failure` row deleted (v5 carryover) | **6** (`dmg_V1`, `dmg_V2`, `dmg_V3`, `dmg_V6`, `dmg_Z1`, `dmg_Z2`) | 0 | RED-CORPUS | D1 | LOW — note the count is **6, not 7**: the ddwrt body no longer sits on the legacy route |
| **M9** | `clean-unverified` row deleted (v5 carryover) | **19** | 0 | RED-CORPUS | D1 | LOW |
| **M10** | `clean-unverified`/`no-reader-failure` actions swapped (v5 carryover) | **19** | 0 | RED-CORPUS | D1 | LOW |
| **M11** | one no-reader family moved out of `clean-unverified` (`squashfs_v3_broadcom`) | **7** | 0 | RED-CORPUS | D1 | LOW |
| **M12** | `no-reader-failure` row deleted (v5 carryover) | **0** | 0 | CORPUS-VACUOUS | **fixtures only** (flips `v2ns-failed`) | **MEDIUM.** Measured: the 126-envelope corpus holds **zero** no-reader FAILED-body envelopes (its 38 no-reader rows are 19 clean + 19 depth-limited), so the fixture scope is this mutant's *only* witness. A corpus-only v6 selftest scores it GREEN. v5's `corpus_control` already reports a `vacuous` flag per scope — **keep it.** |
| **M13** | the new row's action swapped with the `legacy-body-failure` row's action | **7** | **1** | RED-CORPUS | D1 **and** D2 | LOW — double-witnessed; the strongest single-row mutant |
| **M14** | the new row's action swapped with the `no-reader-failure` row's action (both are `preserve-unresolved`) | **0** | **0** | **NO-OP** | **nothing** | **EXPECTED NO-OP, by construction** — the two actions are equal, so the swap changes no cell. **Not a battery defect: it is a witness that the action vocabulary is doing work.** It must be *excluded* from the "every mutation must flip" assertion, or the selftest must expect a zero flip for it explicitly (and say why). |
| **M15** | new row's failing-handler cell widened to the **whole no-reader set** (`squashfs_v3_ddwrt,squashfs_v2_nonstandard,squashfs_v3_broadcom,squashfs_v3_nonstandard`) | **0** | **0** | CORPUS-VACUOUS | **fixtures only** (flips `v2ns-failed`) | **MEDIUM — and this is the width probe.** The corpus holds **zero** no-reader FAILED bodies, so widening the new row to swallow the whole no-reader set is **invisible on the corpus**. A fixture witness is mandatory, or the v6 row may over-capture without any signal. |
| **M16** | new row's failing-handler cell widened to `squashfs_v*` | **0** | **0** | CORPUS-VACUOUS | **fixtures only** (flips `v2ns-failed`) | MEDIUM — same reason as M15 |
| **M17** | new row's failing-handler cell widened to `squashfs_v3*` | **0** | **0** | **NO-OP** | **nothing** | **EXPECTED NO-OP, and it is the one that matters.** `squashfs_v3*` matches the ddwrt FAILED body exactly as `squashfs_v3_ddwrt` does, and the corpus's four `squashfs_v3` FAILED bodies are claimed by the **legacy row, which sits above** — so the widened cell is never consulted for them. Invisible on the corpus **and** on the fixtures: a genuinely everywhere-vacuous mutation. It must be **excluded from the "every mutation must flip" assertion with its reason stated**, or the selftest fails on a mutation that changes nothing observable. |
| **M18** | the new row's **label** renamed (`legacy-body-unreadable-v2`) | **1** | 0 | RED-CORPUS | D1 | LOW — a rename must not survive; this pins the label the claim names |
| **M19** | the new row's action → `none` | **1** | 0 | RED-CORPUS | D1 | LOW — `none` is a silent "nothing to do" on a body whose readers refuse; the corpus catches it |
| **M20** | the new row's **handler** cell blanked | parse refusal: `handler cell '' has an empty alternative` | — | PARSE-REFUSED | the **parser** (exit 2) | LOW — the refusal is the witness; never a silent non-match |
| **M21** | the new row's **action** cell blanked | parse refusal: `line 18: empty action cell` | — | PARSE-REFUSED | the **parser** (exit 2) | LOW — same |

### 3.3 The width defect in the v6 new row's key — measured, and it is the claim's own limit

**The v6 new row keys on the FAMILY `squashfs_v3_ddwrt`, but the reader census it rests
on is FIXTURE-level and says `squashfs_v3_ddwrt` is 6/7 NO-READER — one of the seven
measured ddwrt fixtures IS reader-backed.** Measured, from the frozen v5 instrument's own
census statement (`tools/round-50-c3/sqfs-triage-v5.py:150-156`):

> "``squashfs_v3_ddwrt`` 6/7 NO-READER. A reader is therefore only trusted for the
> **BODY VARIANT** it was measured on, and the handler name cannot carry that distinction
> — the scored features do not expose a body variant."

Consequences, all measured (`census-width.json`):

* The corpus carries **15** ddwrt envelopes but exactly **one** ddwrt **FAILED** body
  (`dmg_Z3_v3ddwrt_inode_table`) — the no-reader variant. **The corpus cannot witness
  the width question at all.**
* On a **synthetic ddwrt FAILED body standing for the reader-backed 1/7 variant**, the
  v6 table prescribes `legacy-body-unreadable`/`preserve-unresolved` where the v5 table
  prescribed `legacy-body-failure`/`cross-read-legacy`. So the v6 family key **suppresses
  a cross-read that the census says is executable** on 1 of the 7 measured ddwrt
  fixtures — the mirror image of the defect v6 fixes.
* **The audit's reader census has the same width** (it is family-level too), so D2 would
  **not** flag a cross-read on the reader-backed variant either. The audit and the table
  share the assumption, so they cannot cross-check it.

**This is the same class of defect the round-50 closure routed on the C1 side** — a
family-level key standing on a fixture-level measurement, with no witness in the corpus.
**R52-C2's own text says the new row applies to "a FAILED-body envelope of a family
with **no validated independent reader**"** — but ddwrt **has** a validated reader on one
of its seven measured fixtures, so the claim's own wording does not support a
family-level ddwrt key either.

The battery therefore carries a **width mutant** (M18/M19 above): widening the new row's
failing-handler cell to the whole no-reader set is **corpus-vacuous** (0/0, fixture-only).
The selftest must carry a synthetic reader-backed-ddwrt FAILED fixture and assert the
new row does **not** swallow it — otherwise the v6 rule silently widens the very defect
it was written to close. **The L1 should decide this before the freeze**: either the
row's key is narrowed to what the census supports (and the claim says so), or the width
is stated as a disclosed limit with the fixture that shows it.

### 3.4 The three code-level guards the claim names

These delete a **guard**, i.e. a piece of the *instrument*, so they cannot be expressed
as a table mutation. They carry the highest no-op risk in the whole battery.

| id | mutation | what it must flip | how the selftest witnesses it | no-op risk and the required mitigation |
|---|---|---|---|---|
| **G1** | **audit guard deleted** (the D2 computation/call removed from the instrument) | **must not exit 0.** The receipt must carry `executability_violations`; a missing audit is exit **2** (`audit_missing`, could-not-evaluate) or exit **1** — never a green run | a selftest case copies the instrument into the work dir, deletes the audit call textually, runs the clone on the fixture envelopes, and asserts `returncode != 0` **and** that the receipt lacks/flags the key | **HIGH.** Without a fail-closed gate this is a pure no-op: the run reports D2=0 (nothing found) and exits 0 — a *deleted* audit reads as a *passing* audit. Required mitigation: (a) the receipt key is **required**; (b) the verdict is **refused** when the key is absent; (c) the clone-and-delete selftest case. All three, or the guard is dead. |
| **G2** | **census guard deleted** (the D3 comparison removed from the instrument) | **must not exit 0.** Same shape: exit 2 (`census_missing`) or exit 1; the receipt must carry `census_outside` and the number of registry paths read | the same clone-and-delete selftest case, deleting the census comparison | **HIGH.** Identical no-op shape: a deleted census check reports "0 outside" and the run goes green. Same three-part mitigation. |
| **G3** | **the audit's reader-census entry flipped** (ddwrt marked reader-backed / removed from the no-reader set) | D2 goes blind: measured, with `squashfs_v3_ddwrt` removed from the audit's census, the **v5 table's** audit findings drop from **1** to **0** — the before-arm's D2=1 would read 0 and the before-arm would go green | a selftest case asserts the audit's reader-census entry equals the frozen round-49 measurement: `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:104` — "squashfs_v3_nonstandard and **squashfs_v3_ddwrt's no-pad fixture: both readers refuse** (unsquashfs exit 1, 7z exit 2; receipt `v3-readers`)" | **MEDIUM-HIGH — the audit's census is a NEW trust boundary.** A wrong census silently disables D2 while every *table* mutant still fires D1, so the census error itself is **unobserved**. The census must be a **frozen artifact with its own receipt**, bound to the source row. **The receipt `v3-readers` is reproduced byte-exact here** — my read of `.ufo/waves/round-49/w1/C1ScribeEntry/v3-readers.out` has stdout sha256 `a921b0fec3eb8b66…`, identical to the sha256 recorded in `.ufo/waves/round-49/w1/C1ScribeEntry/receipts.tsv:53` (receipt R13) — so the binding is verifiable, not asserted. **Measured over-broad case:** adding `squashfs_v1` to the no-reader census produces a **false positive** on `dmg_Z1_v1_inode_table` (measured, 2 findings instead of 1). The census must be an exact set, and the selftest should assert the finding count is exactly 1 on the v5 table. |

---

## 4. The before-arm, measured

The v5 table bytes at the claims-draft base `ab0eafedc41402b43b41a4362084119578dfe7ce`
(`SKILL.md` carries the **v5** table; marker at line 550, 17 rules), scored with the v6
evaluator over the frozen 126-envelope corpus:

| quantity | measured |
|---|---|
| D1 under the **v5** evaluator | **0** (the round-50 landed state is green) |
| D1 under the **v6** evaluator | **1** — `dmg_Z3_v3ddwrt_inode_table` (table `legacy-body-failure`/`cross-read-legacy` vs v6 `legacy-body-unreadable`/`preserve-unresolved`) |
| D2 (executability audit) | **1** — `dmg_Z3_v3ddwrt_inode_table`, action `cross-read-legacy` |
| D3 (`census_outside`) with `census3.json` active | **0** (registry 56 = census 56, `census3.py --check` exit 0) |
| D3 with `census2.json` active (the stale artifact) | **14** → exit 1 |
| verdict | **exit 1** — the claim's before-arm (`executability_violations 1` naming `dmg_Z3_v3ddwrt_inode_table`) is reproducible |

**Two operational landmines this measurement exposes**

1. **The claim's before-arm names a table path that does not contain table bytes.**
   `plans/round-52-claims.md:209` says the before-arm runs "with `--table
   tools/round-50-c3` (the v5 table bytes)". Measured: `tools/round-50-c3/` contains
   **only** `sqfs-triage-v5.py` and `__pycache__` (receipt R12) — **no table file**. The
   v5 table bytes live in `SKILL.md` at the base revision (marker `<!-- sqfs-triage-table
   v5 -->`, line 550). The `--table` argument must therefore name a *file* holding the
   v5 block (e.g. the base `SKILL.md`, or an extracted v5 block file under the round-50
   control surfaces), not a directory. **As written the before-arm command cannot
   resolve its own table.** The L1 must fix the command or name a real file.
2. **The census artifact is self-referential to the freeze.** The registry at the r52
   freeze will carry the round-52 rows (7 named instruments: `gap-rule.json`,
   `c1-counter.py`, `c1-controls.py`, `c1-run.sh`, `fetch-vendor.py`,
   `sqfs-triage-v6.py`, `misroot-sweep.sh`; the claims' registry rule says every new
   `.py`/`.sh`/`.json` instrument under `tools/round-52/` gets exactly one row), so the
   active census artifact must list **56 + those rows**. **Measured: with
   `tools/round-51/census3.json` unchanged, `census_outside` at the r52 freeze = 7**
   (the 7 round-52 paths). Measured remedy: regenerating the census from the **staged
   freeze** `SKILL.md` yields 62 paths and `census_outside` = `[]`, exit 0 (the census
   artifact may list itself — the census lists *registered* paths, and the artifact's own
   path is registered). **The L1 must derive the census artifact from the staged freeze
   `SKILL.md`, not from the pre-freeze HEAD** — otherwise C2's own `census_outside 0`
   predicate fails at the landing REV by exactly the number of new registry rows.

---

## 5. The fixture scope — the v6 selftest's expected flip sets

The v5 selftest asserts, per mutation, the *exact* set of fixture pairs it flips
(`c_mutations_each_flip_their_own_pairs`). Under v6 those sets change.

**v6 fixture set — 12 fixtures: v5's ten, plus TWO new synthetic ones:**

| fixture | v5 expectation | **v6 expectation** | why |
|---|---|---|---|
| `v3ddwrt-legacy` | `legacy-body-failure`/`cross-read-legacy` | **`legacy-body-unreadable`/`preserve-unresolved`** | the claim's own route change |
| `v3ddwrt-failed` (new) | — | **`legacy-body-unreadable`/`preserve-unresolved`** | a second synthetic ddwrt FAILED pair, so a mutant that touches only one ddwrt fixture is still caught |
| `v3ddwrt-multigap` (new) | — | **`legacy-body-unreadable`/`preserve-unresolved`** | a zero-file ddwrt FAILED envelope carrying a **second gap kind** — the **only** witness for the `extractor-failure+` contains-semantics of the new row's gap-kind cell (M7). Measured: adding this fixture moves M7 from `NO-OP` to `CORPUS-VACUOUS`, flipping **exactly** this fixture and nothing else. |
| `v3ddwrt-reader-backed` (new, **conditional**) | — | see below | a zero-file ddwrt FAILED envelope standing for the **reader-backed 1/7** ddwrt variant. It witnesses the **width defect of §3.3**: the selftest must assert the new row does **NOT** swallow it, or the family key over-widens silently. **If the L1 keeps the family key, this fixture is the disclosure's only mechanical witness.** |
| all other nine | unchanged | unchanged | — |

**v6 mutation → flipped fixture set (measured, design A; `mutant-classification.json`):**

| mutation | v5 expected | **v6 expected** | changed? |
|---|---|---|---|
| `guard-row-deleted` (`clean-unverified` deleted) | `{v2ns-clean-le, v2ns-clean-be, v3bc-clean}` | **same** | no |
| `legacy-glob-widened` (cell → `squashfs_v[123]*`) | `{v2ns-failed}` | **`{v2ns-failed, v3ddwrt-failed, v3ddwrt-legacy}`** | **yes** |
| `new-row-actions-swapped` | `{v2ns-clean-le, v2ns-clean-be, v3bc-clean, v2ns-failed}` | **same** | no |
| `no-reader-family-moved-to-clean` | `{v3bc-clean}` | **same** | no |
| `precedence-order-swapped` | `{v2ns-clean-le, v2ns-clean-be, v3bc-clean}` | **same** | no |
| `no-reader-failure-row-deleted` | `{v2ns-failed}` | **same** | no |
| `legacy-row-deleted` | `{v3-legacy, v3ddwrt-legacy}` | **`{v3-legacy}`** | **yes** |
| `unreadable-row-deleted` (new) | — | **`{v3ddwrt-failed, v3ddwrt-legacy}`** (+ `v3ddwrt-multigap` with the 12th fixture) | new |
| `unreadable-action-swapped` (new) | — | **`{v3ddwrt-failed, v3ddwrt-legacy}`** (+ `v3ddwrt-multigap`) | new |
| `unreadable-failing-cell-broadened` (new) | — | **`{v2ns-failed}`** | new |
| `unreadable-row-above-legacy-row` (new) | — | **`{}` — NO-OP** (M6) | new |
| `unreadable-gap-kind-exact` (new) | — | **`{v3ddwrt-multigap}`** with the 12th fixture, else `{}` | new |
| `swap-with-no-reader-failure` (new) | — | **`{}` — NO-OP** (M14) | new |

**Five vacuity facts the v6 selftest must keep reporting** (v5's `corpus_control`
already reports a `vacuous` flag per scope — **keep it, and extend it to D2**):

* `no-reader-failure-row-deleted` (M12) flips **0 corpus pairs** — the 126-envelope corpus
  holds no no-reader FAILED envelope, so the **fixture scope is its only witness**.
* `unreadable-row-deleted` (M1) flips **1 corpus pair and 0 audit violations** — the corpus
  witness and the audit **do not overlap**; both scopes must be reported, and the claim
  must not say the audit covers this row.
* the new row's failing-handler cell broadened (M4), widened to the whole no-reader set
  (M15) and widened to `squashfs_v*` (M16) flip **0 corpus pairs** under design A —
  **fixtures only**.
* the new row's gap-kind cell narrowed to exact (M7) flips **0 pairs in the base fixture
  set** — the **12th fixture** (`v3ddwrt-multigap`) is its only witness.
* the equal-action swap (M14) and the `squashfs_v3*` widening (M17) flip **nothing in
  either scope** — expected no-ops (§7).

---

## 6. The kill rule for the L1 (proposed wording)

> Every control below must be **red** at the freeze: exit ≠ 0 **and** the named detector
> non-zero. A control that is green, or that is red only because the instrument refused
> to parse it (exit 2) when a detector was expected to fire, stops the claim (report a
> miss, do not narrow).
>
> | control | expected at the freeze |
> |---|---|
> | CTL-DN (the v4 table at base) | exit 1, D1 = **20**, D2 = **1** (`dmg_Z3_v3ddwrt_inode_table`), D3 = 0 |
> | CTL-JUNK (unique labels, every row clean) | exit 1, D1 = **126** |
> | CTL-GUARD (round-50 v4 surface, `legacy-body-failure` row deleted) | exit 1, D1 = **26** |
> | CTL-ACT (round-50 v4 surface, `clean` action swapped) | exit 1, D1 = **52**, D2 = 1 |
> | CTL-AUDIT-GUARD (the audit deleted from the instrument) | exit ≠ 0, `audit_missing` named |
> | CTL-CENSUS-GUARD (the census check deleted) | exit ≠ 0, `census_missing` named |
> | CTL-CENSUS-STALE (active artifact = `census2.json`) | exit 1, D3 = **14** |
> | CTL-CENSUS-ONE (one registered path dropped from the active census) | exit 1, D3 = **1** |
> | the table mutants M1–M5, M8–M13, M15, M16, M18, M19 | each flips ≥1 detector in ≥1 scope, none a no-op in **both** scopes (§7) |
> | M6 (new row above legacy), M14 (equal-action swap), M17 (`squashfs_v3*` widening) | **expected zero flip** — excluded from the assertion, each with its reason stated |
> | M7 (gap-kind narrowed to exact) | flips **only** the `v3ddwrt-multigap` fixture — the 12th fixture is **mandatory**, else M7 is a no-op |
> | M20, M21 (blanked cells) | **parse refusal** (exit 2) is the witness |

---

## 7. The no-op rule, stated so it can be applied mechanically

> A mutant is a **no-op** iff it flips **no pair, no audit finding, and no census count**
> in **both** scopes (corpus **and** fixtures). A mutant that flips nothing in the
> corpus but flips in the fixtures is **corpus-vacuous, not passed** — the selftest must
> report it as such (v5's `vacuous` flag), and the freeze must carry a fixture witness
> for it. The selftest must additionally assert, per scope, that no mutant is vacuous
> **everywhere** — the v5 `corpus_control` already computes `any_control_vacuous_everywhere`
>; keep that field.

Applying that rule to the measured table (`mutant-classification.json`, design A):

| class | count | mutants |
|---|---|---|
| RED-CORPUS | **11** | M1, M2, M3, M5, M8, M9, M10, M11, M13, M18, M19 |
| CORPUS-VACUOUS | **4** | M4, M12, M15, M16 |
| NO-OP | **4** | M6, M7, M14, M17 |
| PARSE-REFUSED | **2** | M20, M21 |

**With the 12th fixture (`v3ddwrt-multigap`) added, M7 moves from NO-OP to
CORPUS-VACUOUS** — the counts become 11 RED-CORPUS / 5 CORPUS-VACUOUS / 3 NO-OP / 2
PARSE-REFUSED (measured, both scopes in `mutant-classification.json`).

The three everywhere-no-ops are each expected **by construction**, with a stated reason:
**M6** (the new row moved above the legacy row is immaterial in design A, because the
legacy cell no longer names ddwrt — the *cell content* is load-bearing, not the order),
**M14** (the two swapped actions are the same string) and **M17** (`squashfs_v3*` is never
consulted, because the legacy row above claims the v3 FAILED bodies). Each must be
**excluded from the "every mutation must flip" assertion with its reason stated**, or the
selftest fails on a mutation that changes nothing observable.

**Five mutants are corpus-vacuous** (M4, M12, M15, M16, and M7 once the 12th fixture
lands) — **a corpus-only selftest would score all five GREEN**, and the claim's own
predicate ("every committed mutation flips ≥1 pair or ≥1 audit finding") would then be
satisfied by a battery that witnesses nothing.

> **The v6 selftest must therefore assert, per mutant, the scope in which it is
> witnessed** — not merely "≥1 pair flipped". v5's `corpus_control` already reports
> `corpus` and `fixtures` separately with a `vacuous` flag and an
> `any_control_vacuous_everywhere` roll-up; the v6 selftest must **keep both scopes and
> extend the roll-up to D2**, so a mutant that flips nothing in either scope is a
> **no-op** and a mutant that flips only in the fixtures is **corpus-vacuous** — a
> different thing, and the claim must not conflate them.

---

## 8. What was NOT run (honest limits)

* **No v6 instrument exists yet**, so G1/G2/G3 (the code-level guards) are **specified,
  not executed**. The r51 draft at `.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py`
  is **not** a v6 implementation: its docstring still reads the **v5** marker
  (`MARKER_V5 = '<!-- sqfs-triage-table v5 -->'`) and it carries **no** `legacy-body-unreadable`
  row, no executability audit and no census clause (verified by grep + sha256: it is
  *not* a byte copy of v5 — sha256 `b79ff216…` vs `f29eb920…` — but its v6-relevant
  content is the v5 content). Every other expectation here is measured against a
  **probe** that ports the frozen v5 parser/evaluator and layers the v6 row + evaluator +
  audit on top; the port must reproduce these numbers with its own code.
* No REA run, no `--data-run`, no carrier download, no network, no `npx rea-agents`.
* The probe imports the frozen v5 instrument by `importlib` from the lane **read-only**.
* No lane file was modified; no git mutation was run in the lane or the fleet repo. The
  only writes are this seat directory and `$S` (scratch).
* **Not run:** the round-52 `gap-rule.json` / counter / controls / fetcher (C1's
  instruments) — out of this seat's scope; and the round-50 `ctl-do-nothing.skill.md`
  **under the v6 parser** was measured only as a surface parse + score, not as a
  committed receipt.
* The fleet repo shows `M .scratch/goal-20261029-hyaku-run12.md` and
  `M .ufo/l0-questions.md`; **both predate this seat's session** (mtimes 05:56 and
  08:00 vs. 11:03 at the check) and are other seats'/operator's work, not mine. The
  lane shows `M .ufo/waves/round-50/w3/ScribeEntryC1.md` (mtime 07:53, likewise
  pre-existing). This seat wrote **only** under
  `.ufo/waves/round-52/w1/MutTriV6/` (receipt R14, R15).
