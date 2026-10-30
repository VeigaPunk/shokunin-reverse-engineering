## Round 51 (2026-10-30) — one re-freeze: the device-accounting law (C1) and the executable ddwrt route + re-derived census (C2)

Base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab` (the round-51 claims-draft commit, pushed).
The claims file `plans/round-51-claims.md` declares its own base as
`1aa273694f4409d3432fbcd73e83a33bee0dd8e9`; the two differ only by that claims file and
`.ufo/waves/round-51/l1/sources-census-start.txt` (`git diff --name-only 1aa27369… f04b51dd…`
→ those two paths; `SKILL.md` and `tools/` are byte-identical), so the C2 before-arm may be
counted at either revision. The wave-1 amendment record (F11) has since named
`f04b51dd…` as the C2 before-arm base — the freeze commit must carry that same base into
both counting commands **[FILL:L1]**. Declared freeze: **[FILL:L1]** (one commit adding the
round-51 instruments, fixtures and the amended claims; the `## Wave-1 amendment record` in
the claims file now carries the wave-1 attack findings F1–F11). Waves: w1 build 36 seats
(`.ufo/waves/round-51/w1/`: executor 8, scribe 6, reviewer 5, critic 5, mutation-tester 3,
scout 4, connector 2, sentinel 1, revenger 1, simplifier 1 — attack 9/36 = 25%); the falsify
wave (w2) is dispatched after the landing and its totals are recorded in the round report
[FILL:L1].

| claim | axis / surface | before | after | counting command | measured at |
|---|---|---|---|---|---|
| R51-C1 | coverage — the AVM LE SquashFS `hsqs` members of four pinned vendor carriers, Frontier → Core, under the re-frozen gap-accounting rule (`tools/round-51/gap-rule.json` + `tools/round-51/c1-counter.py` v2) | at the round-50 freeze exit 1, `carriers_matched 2` of `target 4`, `gaps_ok` false on `g7581`/`g7582` (twelve `char-device` oracle entries each with no gap and no removal against the frozen rule's single silent allowance `247:0`), `failing ["g7581:gaps_ok","g7581:projection_ok","g7582:gaps_ok"]`, `bindings_false ["province_core_section","province_core_row"]` (`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`; measured at `646d29c9df4ef77499248f95589cb9526c6dea19`, freeze `435d41fd4ad9211d1579fc447936fb33d2b74467`, counter sha256 `9820811b…`; the round-50 before-arm at the freeze read `carriers_matched 0`, `.ufo/waves/round-50/l1/scores/c1-before-attempt2.json`). The per-carrier-class derivation the re-freeze rests on is re-derivable from the frozen oracle tables: the Cable class (`c6430`, `c6490`) carries **exactly one** char-device (`dev/led 247:0`) and the FRITZ!Box class (`g7581`, `g7582`) carries **thirteen** (`dev/led 247:0`, `dev/pts/0-7 136:0-7`, `dev/tiatm 230:0`, `dev/ttyp0-2 3:0-2`) — counted from `tools/round-50/oracle/<id>.nonregular.tsv`, so the round-50 rule's `247:0`-only allowance is the Cable-class census generalised to a second class | **[FILL:L1]** — expected exit 0, `carriers_matched 4`, `gaps_ok` true on every carrier, every binding true, `frozen_path_changed []`; if the fresh data run reports `< 4` the claim is missed as frozen (honest stop, no narrowing) | `python3 -I -B tools/round-51/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --receipts corpus/evidence/round-51/c1 --json-out <OUT>` | **[FILL:L1]** (the `rev` field of `.ufo/waves/round-51/l1/scores/c1-after.json`; the before-arm is the committed round-50 receipt named in the previous cell) |
| R51-C2 | depth — `SKILL.md` rule block 27 (triage table v6: the ddwrt FAILED-body route `legacy-body-unreadable`/`preserve-unresolved`, no cross-read) + the scoring instrument `tools/round-51/sqfs-triage-v6.py` (new frozen executability audit) + the re-derived registry census `tools/round-51/census3.json` | the **committed** before-state: v5 routes the FAILED no-pad ddwrt body `dmg_Z3_v3ddwrt_inode_table` to `legacy-body-failure`/`cross-read-legacy` — a cross-read prescribed on a body whose readers refuse (v5 labels in `.ufo/waves/round-50/c3/c3-after.json`: `table_label legacy-body-failure`, `table_action cross-read-legacy`, `G ["extractor-failure"]`, `F ["squashfs_v3_ddwrt"]`; the row itself is committed at `SKILL.md` rule block 26) — and the registry census drifts by **13** registered paths (55 registered paths inside the `<!-- instrument-registry v2 -->` markers of `SKILL.md`, 42 in `tools/round-48/census2.json` → 13 absent: the six `tools/round-49/*` rows, the six `tools/round-50/*` rows, `tools/round-50-c3/sqfs-triage-v5.py`); the **declared** before-arm (the claim's `executability_violations 1` / `census_outside 13` at the base, exit 1) is not yet measured — the audit is a round-51 instrument, so the before-arm receipt `.ufo/waves/round-51/l1/scores/c2-before.json` is **[FILL:L1]** | **[FILL:L1]** — expected exit 0, `pair_mismatches 0`, `evaluator_missing 0`, `executability_violations 0`, `census_outside 0`, green selftest, over the same frozen 126-envelope corpus (`.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`); every v5 label unchanged except the one ddwrt FAILED-body pair | `python3 -I -B tools/round-51/sqfs-triage-v6.py --root <LANE> --rev <REV> --freeze <FREEZE> --envelopes <DIR> --json-out <OUT>` | **[FILL:L1]** (the `rev` field of `.ufo/waves/round-51/l1/scores/c2-after.json`; the before-arm is run once at the declared base and lands at `.ufo/waves/round-51/l1/scores/c2-before.json`) |

**C1 pre-freeze controls** (scored with the v2 counter over the committed round-50 envelopes
plus the frozen oracle/non-regular tables — wave-1 amendment F2: the controls evaluate the
**rule-scoped disposition verdict**, not the full predicate, because the committed round-50
receipts fail the byte-dependent and round-sensitive clauses):
CTL-OLD (the **reproducibility** control, wave-1 F9: the round-50 gap rule over those
envelopes → **2 of 4**, exit 1 — reproducing the committed miss; 4 of 4 would mean the
round-50 miss is not reproducible → stop and report that),
CTL-NEW (the law-derived rule over the same envelopes → **4 of 4**, exit 0),
CTL-DN (do-nothing fixture tree → exit 1 or 2, never 0),
CTL-JUNK (syntactically valid junk rule → 0 of 4, exit 1),
plus the frozen rule mutations (wave-1 F4): M1 all-thirteen whitelist → **RED by the
`law_shape_ok` clause**; M2 a fixture carrier carrying a fourteenth unlisted device → **GREEN
under the law rule, RED under any detail whitelist**; M3 `required["char-device"]=true` with
only `247:0` silent → red (the round-50 miss); M4 a strict-subset whitelist → red (the M50
partial-widening trap). Kill rule: CTL-NEW red, CTL-OLD yielding 4, or any mutant green that
should be red → stop before the data run and report a miss. Control receipts: **[FILL:L1]**.

**C2 pre-freeze controls** (scored with the frozen instrument before the table lands): the
v5 table at base → audit red; junk table → `pair_mismatches > 0`, exit 1; audit-guard-deleted,
swapped-new-row-action and census-guard-deleted mutants → red. Kill rule: any green → stop,
report a miss. Control receipts: **[FILL:L1]**.

**Freeze-drift gating** (routed defect 3): both round-51 instruments fail closed — a modified
frozen path at REV yields exit 2 with `frozen_path_changed` naming the path (the v1 counter
only reported drift). Selftest case receipts: **[FILL:L1]**.

**Four facts the L1 must carry into the freeze (measured at `f04b51dd…`, not inferred).**

0. **CRITICAL — the amended F3 rule shape makes the law rule RED on all four carriers.**
   The wave-1 amendment F3 sets `allowed[char-device] = allowed[block-device] =
   allowed[fifo] = allowed[socket] = []` and says "`required` unchanged from round 50";
   round 50's `required["char-device"]` is **`true`**. Under the frozen counter's own
   `disposition_check` semantics (`need = required.get(kind, bool(allowed.get(kind)))`; a
   required entry must carry exactly one disposition — an allowed gap, a removal, or a
   `removed.silent` detail), a device row with **no** gap and **no** removal is `missing` →
   `gaps_ok false`. With `allowed[char-device] = []` there is no admissible gap kind, and
   with the law admitting no device detail under `removed.silent` there is no silent
   admission either: **every** device row is unaccounted, not just the twelve. Measured
   against the four committed round-50 envelopes and the frozen oracle tables with the
   **unmodified** `tools/round-50/c1-counter.py` (receipt
   `.ufo/waves/round-51/w1/ScribeScorecard/probe-full.out`, sha256 `fc2c7637…`):

   | rule shape | c6430 | c6490 | g7581 | g7582 |
   |---|---|---|---|---|
   | round-50 frozen | `gaps_ok` true | true | **false** | **false** (the committed miss) |
   | F3 as amended (`required["char-device"]` = true) | **false** | **false** | **false** | **false** |
   | F3 with `required["char-device"] = false` | true | true | **true** | **true** |

   So the amended shape scores **0 of 4**, not the claim's 4 of 4: CTL-NEW would be RED and
   the kill rule ("CTL-NEW red → stop before the data run") would fire. The same probe over
   the claim's own mutation set confirms it: under the amended shape M1 (all-thirteen
   whitelist) is disposition-**green** and M2 (a fourteenth unlisted device) is **red**
   under the law rule — the opposite of what the claim states (`.ufo/waves/round-51/w1/
   ScribeScorecard/probe-mutations.out`, sha256 `788cb95a…`). Under
   `required["char-device"] = false` every mutation lands as the claim declares: CTL-NEW
   4 of 4, M1 red by the `law_shape_ok` clause (which the v2 counter must implement — it is
   **absent** from the current `ExecCounterV2` draft, together with `census_rederived_ok` and
   `depth_gap_recorded`), M2 green under the law and red under any whitelist, M3 and M4 red.
   **The freeze's rule must set `required["char-device"] = false`** (the law's statement is
   "a device entry carries no disposition at all", so the entry is not *required* to carry
   one), or the disposition semantics must change — which would be a counter change, not a
   rule change, and is the L1's call to make explicitly before the freeze.
   **RESOLVED pre-freeze (L1):** the L1 accepted this finding and amended F3 in the
   claims file to state `required['char-device'] = false` as a deliberate change from round
   50's `true`, citing these probe receipts; the amended v2 counter now carries the
   `law_shape_ok` binding (empty `allowed` and empty `removed.silent` per device kind, and
   `required["char-device"] is False`). Verified after the fix against the four committed
   envelopes with the amended v2 counter itself (receipt
   `.ufo/waves/round-51/w1/ScribeScorecard/probe-v2.out`, sha256 `62ddb35c…`): the
   required-true shape scores 0 of 4 and `law_shape_ok` false; the required-false shape
   scores **4 of 4** and `law_shape_ok` true. The kill-rule fire is avoided.

1. **The depth head is already stale at the round base.** The Owned-axes `depth` head reads
   "25/25 queue-drain rule blocks have resolvable file/range citations at the round-48
   landing", but command A at `f04b51dd…` reads **`rule_blocks 26`,
   `citation_resolved_rules 25`, `depth_score 9.62`** — the 26th block (rule block 26, the v5
   triage table) carries **no** `corpus/knowledge/…` citation at all (its only file refs are
   `SKILL.md table v4 row N` and `S112`/`S119`/`S120`/`S121` source rows). The round-50
   attempt-2 section already notes the 25/25 figure is "a historical statement and is not
   re-run this round", but the head still states it as the current observable. **The round-51
   depth head must state the re-derived base pair (26 blocks / 25 resolved) and the landing
   pair**, and rule block 27 (v6) should carry a resolvable `corpus/knowledge/…` citation so
   the depth proxy does not regress. If the v6 block is added without one, the landing reads
   27 blocks / 25 resolved (`depth_score 9.26`) — a silent regression the head must not hide.
2. **The registry-census drift cannot reach 0 under the round-48 census rule.** The
   round-48 rule (`tools/round-48/census2.py`) derives the census from the paths **named in
   the claims files**, not from the registry rows. Widening that rule to
   `plans/round-4[1-9]`/`round-50`/`round-51` still leaves **three registered paths
   unnameable**: `tools/round-49/c1-controls.py`, `tools/round-49/c1-oracle.py`,
   `tools/round-49/c1-run.py` are named in **no** claims file (they exist only in
   `.ufo/waves/round-49/draft/` and the round-49 registry rows). A census-scoped
   re-derivation therefore lands at `census_outside 3`, not 0. The amended claims text
   (wave-1 F11 header) already says the re-derive "enumerates the registered instrument
   paths from the registry markers at REV" — that wording is the reachable one, but the
   **port must not import `census2.py`'s claims-file-naming rule**: it must enumerate the
   rows inside the `<!-- instrument-registry v2 -->` markers (the round-48 counter's own
   `registry_rows` surface), and `census3.json` must record that rule and which artifact it
   supersedes for which surface. The frozen `tools/round-48/census2.json` bytes stay
   untouched. Independent confirmation that the drift is real at the base: the round-48
   counter `tools/round-48/meanings.py` run at `f04b51dd…` exits **1** with `failing
   ["registry rows outside the census: …"]`, `registry_rows 55`, `census_paths 42`,
   `registry_extra` = exactly those 13 paths (receipt
   `.ufo/waves/round-51/w1/ScribeScorecard/meanings-at-base.json`).
3. **The C2 executability audit has no committed, joinable reader census.** The claims
   require the v6 audit to check each FAILED body's prescribed action against "the family's
   reader census" and to report `executability_violations 1` at the base. The only reader
   census in the lane (`.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt`,
   committed) is **fixture-level** over the 31 round-42 fixture rows; the nine FAILED-body
   envelopes are **derived** bodies whose own subject digests appear in **no** census row
   (measured: receipt `.ufo/waves/round-51/w1/ScribeScorecard/probe-census-join.out`,
   sha256 `d1331558…` — `dmg_Z3_v3ddwrt_inode_table`'s own digest is `839c17a83b70…` while
   its parent fixture's row is keyed `daa8e72d355d…`). The join runs through the round-42
   manifest's `input.parent` name, which is ambiguous without the family (the parent name
   `squashfs_v3.be.nopad.bin` appears under four families with four different verdicts), and
   seven of the nine FAILED bodies have parents in **no** census row at all (the census
   covers only the four v3 families). Further, the census's family roll-up for ddwrt is
   **6 no-reader of 7**, not "all refuse" — so a family-scoped rule does not select
   `dmg_Z3_v3ddwrt_inode_table` at all; the discriminating fact is per-body, and the scored
   features expose no body variant (v5's own disclosure). The round-50 what-if receipt
   already recorded that a fixture-correct rule moves **8** labels, not 1. **The freeze must
   land a committed, machine-readable per-body reader census (or an explicit frozen
   envelope → parent fixture → census-row binding keyed by family) as a pinned tool input**,
   and must state whether the reader verdict is the raw-fixture one (the census) or the
   magic-normalised one (the round-42 oracle runs show the ddwrt fixtures readable after
   normalisation) — otherwise the declared before-state `1` has no re-derivable mechanism and
   the after-state `0` is reachable by making the audit vacuous.

Owned scores: coverage `10 → 10` **[FILL:L1]** (coverage head **140/140 → 141/141** once
`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` lands and is mapped — the map's
141st file; the pre-round count is measured: 140 knowledge `.md` files at `f04b51dd…`, all 140
mapped, `missing []`, `dangling []`); depth `10 → 10` **[FILL:L1]** (the base re-derivation
is 26 blocks / 25 resolved — see finding 1; the landing pair is re-derived by command A at
the landing); calibration `10 → 10` **[FILL:L1]** (the record re-derives at the new tip; the
round-48/49 atoms stay as written).

Learning trends: expansion **[FILL:L1]**; quality **[FILL:L1]**; discernment **[FILL:L1]** —
each verdict names its evidence and its bound, and none is inherited from the round-50
attempt-2 trend line by default.

Limits **[FILL:L1]** — the C1 measurement is bounded to the four frozen carriers and the
frozen rule; the C2 corpus is the round-42 recon set (depth, not held-out generalisation —
the same disclosed limit as R50-C3); the executability audit is a new frozen instrument, so
its before-arm is a re-derivation against the v5 table rather than a pre-existing receipt.

- **planned (round 52):** **[FILL:L1]**
- **retired:** none.

### LOG and lesson pointers (append-only)

- `LOG.md` — the round-51 entry (`## 2026-10-30 — round 51 (KaidokuR51): …`): the freeze
  revision, the two counting commands and their receipts, the coverage-head move
  140/140 → 141/141, the `PROVINCE.md` `## Round-51 additions to Core` landing (LE `hsqs`
  leaves the Frontier list), the routed-defect repairs (the `646d29c9` correction entry, the
  `SHONEN.md` regeneration, the two freeze-drift gates, the `fetch-vendor.py` network-guard
  selftests, the `misroot-sweep.sh` sweep helper, the carried L0 cookie note) and the
  wave-2 falsify dispatch. Exact heading text: **[FILL:L1]**.
- `corpus/lessons/round-51.md` — `## Mistakes` rows (class · evidence · captured-by · fix),
  one per mistake mined this round (a fix counts only once shown able to fail). Rows:
  **[FILL:L1]**.
- `corpus/SOURCES.md` — the round-51 rows opened this round (the device-node / `no-pad`
  source rows that ground the law and the v6 change), each with its `## Gate` record (URL,
  access date, ≤25-word located quote) and its `used-by` entry naming
  `2026-10-30-r51-avm-le-squashfs-core`. Rows: **[FILL:L1]**; the census end state (exit 0,
  the round's new rows) is re-taken at the filing tip — **[FILL:L1]**.
- `corpus/README.md` — the coverage-map row for the round-51 entry **[FILL:L1]**;
  `PROVINCE.md` — `## Round-51 additions to Core` with the LE-members row and the
  Round-51 frontier note **[FILL:L1]**.
