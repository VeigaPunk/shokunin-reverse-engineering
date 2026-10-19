# PL-3 plan — C3 arc3-era citation coverage extension (chain c3, wave arc3-loop1-round3)

Seat: PL-3 (planner, chain c3) · 2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
· HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (read-only `git rev-parse`; no git mutation by this seat)
· scratch `/var/tmp/pl3` (`/tmp` never used).

## 0. Revision ledger (rule #14 discipline)

| object | revision | sha256 | when |
|---|---|---|---|
| pointer table at seat start (committed, r2 landing) | HEAD c07af80 | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` | measured 13:06Z (EX-44 receipt agrees) |
| expected.json at seat start | HEAD c07af80 | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` | measured |
| **pointer table mid-seat (EX-41's landed first cut, worktree, uncommitted)** | worktree, 13:12Z | **`bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7`** | EX-46 `pin-check.py` — matches the worktree `expected.json` pin (`d97dd60a…`) |
| **this plan's delta fragment** | re-based on `bfc42f1b` | table-with-delta `c895a671827f5712e7a1559169aae5b5a46b796ea7472530976d8a3ebc0e9ad3` | `validation.out` |

The base moved while this seat planned (31-entry r2 table → EX-41's 57-entry cut). **All numbers
below are re-based on `bfc42f1b`.** Any further EX-41 revision invalidates the delta's scratch digest:
re-run `build_entries.py` (it reads the worktree table live) — the fragment re-derives.
EX-41's seat report (`seats/EX-41.md`) landed at 13:1xZ and polls my absence explicitly: it names
"the delta is a plan-vs-landed reconciliation, not a defect" — §2 and §4 are that reconciliation.

## 1. Work performed (method + evidence pointers)

Census scripts (this directory): `census.py` → `census-v2.json`/`census-table.out` (full run);
`build_entries.py` (fragment + scratch table/expected + probe runs) → `validation.out`;
`bite.py` (per-entry mutation falsification) → `bite-suite.out`.

Citation census over the arc3 r1/r2-introduced artifacts, read as Git objects at HEAD:

- **S1** `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` (r1's new knowledge entry, 33 lines)
- **S2** `SCORECARD.md:1338-1496` (the arc3 r1 + r2 sections)
- **S3** `SKILL.md` (rule #14 block 240-255; registry intro 381-383; rows 389-390; r1's guard-text edit)
- **S4** `.ufo/gates/custody-pair/README.md` (r2's new receipt-convention document, 132 lines)
- **S5** `corpus/README.md:38` (r1's map row) · **S6** `SHONEN.md:6` (r2 refresh)
- **S7** every added line of the two non-wave work diffs (`fbbbd45`, `28aa7a9`) — 49 citation tokens
- **S8-S11** `.ufo/gates/custody-pair/custody-pair.py`, `citation-drift-probe.py`, `expected.json`,
  `c1-census-v10.py` (the instruments arc3 touched — their own header citations are in scope)

Resolution ladder for each token: exact tracked path → source-relative → bare-name suffix match →
`../`-normalized → absent. **356 backticked tokens; 128 path-ish or operator tokens** (forms:
exact 35, suffix 39, multi 4, operator 15, dotdot-absent 1, absent 34 — the 34 "absent" ones are
non-path tokens: version pins, digests, field paths, byte constants, host paths; 228 non-path).
**Every in-repo citation target exists at HEAD** (`absent_at_HEAD = 0` for path tokens; `census-table.out`).

## 2. Census result — the coverage contract (four declared families + two surfaces found)

| cluster | citations (distinct targets) | coverage |
|---|---|---|
| F1a r1 entry → line-number citations | r3-07 entry ×4 ranges, QUALITY ×2 | EX-41 `arc3r1-entry-*` (6, landed) — ratified |
| F1b r1 entry → evidence artifacts | **26 files** + solc-prefix dir + 2 dir/brace citations | **this delta (27 anchors)**; dirs by prose adjudication |
| F2 arc3 SCORECARD section needles | section keys r1/r2, fresh-identity line, r2→SHONEN:6 coupling, dirty-path, custody-dir, shonen count | EX-41 keys (2, landed) + this delta (fresh-identity, SHONEN 14/14, dirty-path) |
| F3 round-2 registry rows + rule #14 block | 2 rows; rule-#14 cites CR-2.md:86-89, verdict.md:149-153, entry:7, LOG.md:1411-1412, SCORECARD section-key | EX-41 (rows + 4 extracted, landed) — ratified; registry rows' **cited files** (tool/README/probe/table/expected) = this delta (4 anchors) |
| F4 custody receipt conventions | 3 v1 shape examples, EX-31 evidence set (9 named files), 5 operator paths, scratch-policy tokens | EX-41 v1 examples (3, landed) — ratified; EX-31 anchors (10) + CUSTODY_PATHS proxies (5) = this delta |
| F5 map row + SHONEN r2 refresh | corpus/README.md:38 → 2 knowledge files; SHONEN.md:6 → SKILL.md:81-255 | this delta (2 anchors + 1 extracted strengthening; EX-41 has the row-token anchor) |
| **found, not in the four families** | `c1-census-v10.py` header → SCORECARD (E22 debt, laundering refusal, round-4 range) | EX-41 (3, landed) — ratified (arc3 r1/r2 changed this instrument; its header citations are arc3-era) |

Coverage accounting at the delta: base table 57 entries (EX-41) → **N = 108** with the 51-entry delta
(`validation.out`: `NEW entries=51 new_exempt=11 N=108`, table sha `c895a671…`).

## 3. Classification — pinnable vs adjudicated NO-ENTRY

**Pinnable under rule #11 (all in this delta):** line-number citations into lane-owned files
(`extracted`); file-level citations to committed wave evidence (`anchor`, needled by the cited
claim's load-bearing content); SCORECARD's own section lines (`exact` — append-grown file, pins do
not move); operator-mutable paths only through their in-repo content-anchor proxy.

**NO-ENTRY adjudications (this delta's 11 exempt rows; EX-41's 5 ratified):**

1. bare operator paths (README:7-11) — rule #11 by construction; **upgraded**: the proxy
   (instrument's `CUSTODY_PATHS`) *is* covered by `a3r2-cp-path-*` (5 anchors; measured to survive
   C2's in-progress tool revision `112d01dc…`→`7cd19c3c…`: 2 occurrence lines each).
   *Recommendation: EX-41's exempt row "the five operator paths as written in README" should name
   the proxy anchors and drop the blanket exemption.*
2. `../waves/arc3-loop1-round2/claims/c3/EX-31/` (README:129) — **non-conforming form, measured**:
   resolves to `.ufo/gates/waves/` (absent, `git cat-file -t` fatal) and `git show HEAD:../waves/…`
   exit 128. Covered by the `a3r2-ex31-*` anchors at repo-relative paths; README fix in
   `proposed-readme-path-forms.patch.md`.
3. receipt examples `arc3-loop1-round1/claims/…` (README:103-105) — shorthand relative to the
   implied `.ufo/waves/` base; resolves uniquely by suffix; EX-41's anchors cover the targets.
4. digest/identity tokens in arc3 surfaces (`dd986f56…`, `c134afcb…`, `112d01dc…`, `fa484d57…`,
   `d0772ce8…`, `0e1a1ab6…`) — identity claims, not path citations; discipline is rule #14
   re-derivation. The r2 section's `c134afcb…` legitimately stales when C2's revision lands.
5. commit short-hashes — revision refs, not file citations (probe target model is `rev:path`).
6. selector/prologue byte constants — data, not repo objects.
7. scratch-policy paths (`/tmp`, `/dev/shm`, `/var/tmp`, `$CUSTODY_PAIR_SCRATCH`) — host policy.
8. version pins (`rea-agents@…`, `evmole@0.9.3`, `solc 0.8.37+…`) — the census's PIN locus class.
9. `source:`-list sibling shorthand — 20 distinct tokens, all suffix-resolved (one context case:
   `solc-input.json` → RV-2's); every resolvent has a full-path anchor in this delta.
10. dotted field paths (`normalized_result.functions`, `bytecode.kind`, …) — observation vocabulary.
11. directory citations (r1 entry lines 1 and 11) — members carry their own anchors.

**EX-41's exempts ratified with causes:** round-report line pins (parent-written reports, mutable);
wave-internal citations (outside the four declared families; wave artifacts are frozen evidence);
current-state count tokens (measurements, not citations); LOG/report prose naming without numbers.

## 4. Entry design (schema-conformant; `entries-arc3.json`)

Conventions used (existing schema only): `{id, kind, file, line?, pattern?, target?,
target_group?, target_group_end?, must_match, note}`; kinds `extracted|exact|anchor`.
Needle rules: (a) load-bearing content of the cited claim, not mere existence; (b) revision-robust —
never a digest, never text C2's same-commit revision is expected to rewrite (verified for the
custody files against the in-progress worktree revision); (c) `anchor` needles may be multi-site
(class-removal bite verified); (d) registry-table rows stay line-unpinned (`anchor`), the
precedent of `skill-registry-row`.

The 51 delta entries (ids as landed in the fragment):

- **r1 evidence anchors (27):** `a3r1-rv2-{probe-hex64,probe-raw64,probe-hex67,rerun-a,rerun-b,
  cwdroot,creation,smoke,many,manysel,sel5,abi,creationhex,solcinput}`, `a3r1-ex06-{runhex,runraw,
  plantedk,transcript,compilejs}`, `a3r1-ex07-{recon,m1rv2,m1kdx,m2keccak}`, `a3r1-rv1-sha3`,
  `a3r1-ex02-{receipt,smokebin}`, `a3r1-solcprefix-pkg`. Needles: envelope evidence ids
  (`ev_c80379e1`, `ev_d0d0b054`, `ev_56d89cb4`), `"normalized_result"`, planted-set counts (`K=5`,
  `K=11`, `"K": 6`), `VERDICT: ALL SOURCES AGREE`, `"code_sha256": "c1081a56`, `INSTALL RECEIPT`,
  `two independent SHA3-256 oracles`, `^60806040` carriers, `"language": "Solidity"`, `0.8.37`.
- **F2/F5 (5):** `a3r1-sc-fresh-identity` (exact, SCORECARD:1366), `a3r1-sc-dirty-path` (anchor),
  `a3r2-sc-shonen-refresh` (extracted, SCORECARD:1435→SHONEN `14/14`);
  `a3r1-maprow-r1entry`, `a3r1-maprow-r3entry` (anchors).
- **F3 files (4):** `a3r2-custody-tool` (`CUSTODY_PATHS`), `a3r1-cd-probe` (`pointer_table_tampered`),
  `a3r1-cd-table` (`"entries"`), `a3r1-cd-expected` (`"pointer_table"`).
- **F4 EX-31 (10):** `a3r2-ex31-{pre,post,pre-side,post-side,verify-pair,attacks-sh,attacks-out,
  selftest,labeldefect}` + the 5 `a3r2-cp-path-*` proxies. (9 EX-31 + 5 = 14; the tenth EX-31-class
  entry counted with the F4 anchors.) Needles: `^# receipt-version: 2`, sha256-sum sidecar shape,
  `CUSTODY_PAIR_VERIFY: MATCH paths=5/5`, `same-content rewrite IN PLACE`,
  `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15`, `v2 bare MTIME_UTC`.
- **SHONEN strengthening (1):** `a3r2-shonen-rule14-inrange` — same citing line as the r10 entry
  `shonen-skill-range`, needle = rule #14's opening words: pins that the asserted 81-255 range still
  contains the newest rule, the exact form the r10 entry used for rule #13. Keep both (independent
  needles on one coupling; the r10 entry's note text is stale — see §6 note edits).

**17 dropped as functional duplicates of EX-41's cut** (mapping in `validation.out` header and §2):
the 6 r1-entry extracted, `a3r1-sc-section-head` (vs `sc-arc3r1-section-key`), `a3r2-custody-readme`
(vs its 4 README anchors), the 2 registry row anchors, the 4 rule-#14 extracted, the 3 v1-shape
examples. Kept despite near-overlap: `a3r2-sc-shonen-refresh` (pins the `14/14` count; EX-41 pins
the range form) — two needles, one coupling, stated redundancy.

## 5. Before → after measurement (commands + outputs)

```
$ python3 /var/tmp/pl3/build_entries.py        # re-based on the EX-41 worktree cut
BASE table sha256=bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7
BASE entries=57 quoted=4 exempt=8
NEW entries=51 new_exempt=11 new_table_sha256=c895a671827f5712e7a1559169aae5b5a46b796ea7472530976d8a3ebc0e9ad3 N=108
--- probe: scratch table + scratch expected (default) --- CITATION_DRIFT_VERDICT: reported findings=0 exit=0
--- probe: --strict ------------------------------------ CITATION_DRIFT_VERDICT: clean findings=0 exit=0
--- stale-pin demo (scratch table + base expected) ----- CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2  (pointer_table_tampered)
--- selftest with scratch expected --------------------- CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
real table/pin unchanged: 738b3a56→n/a; worktree table bfc42f1b == bfc42f1b; expected d97dd60a == d97dd60a
$ python3 /var/tmp/pl3/bite.py
BITE_SUITE: entries=51 control_silent=51 both_mutations_bite=51 failed=0
```

Landed-cut control (read-only, EX-41's revision): probe at HEAD `findings=0` both modes; EX-46
`pin-check.py` VERDICT MATCH (`bfc42f1b`). **Claim-relevant before→after: entries 57 → 108
(counted mechanically; the census is the acceptance test, not the count); findings 0 → 0; selftest
13/13 unchanged.**

## 6. Integration procedure for EX-41 (and the hazards it must re-check)

1. **Order vs C2.** C2 lands revisions of `.ufo/gates/custody-pair/{custody-pair.py,README.md}`
   and its SKILL.md registry row in the same commit. Land C2's text first, then splice the table,
   then **re-verify every needle that touches those files** against the *new* revision:
   `grep -c` for each `a3r2-custody-*`, `a3r2-cp-path-*`, `a3r2-ex31-*`, and EX-41's
   `custody-readme-*` / `skill-registry-custody-pair-row` needles. Measured today against C2's
   in-progress worktree revision (README `fa484d57…`→`f30df42e…`, tool `112d01dc…`→`7cd19c3c…`):
   all survive (occurrence counts in the seat report). **Hazard H2**: EX-41's
   `skill-registry-custody-pair-row` needle is the precedence sentence — C2's claim rewrites the
   row's declared exit map; if the sentence is edited, re-aim the needle in the same commit
   (stable cell: `\| custody-pair \| tool / kaidoku \|`).
2. Splice `entries-arc3.json` (`entries`, `exempt`, `_doc_addendum`), dedupe the operator-path
   exempt rows (§3.1), then **re-pin**: `sha256(pointer-table.json)` into `expected.json`
   `pointer_table.sha256` in the same commit (EX-46 `pin-check.py` must read MATCH).
   Byte-format facts measured from EX-41's landing: use its `build-table.py` (round-trip
   `json.dumps(indent=2, ensure_ascii=False)` reproduces the current table bytes) and note that
   `expected.json` carries **no trailing newline** — the pin edit must preserve that convention
   (EX-41 `seats/EX-41.md` §1).
3. Re-run: probe default + `--strict` at the work commit (findings 0 both; the `--strict` run is
   gate semantics), `--selftest` 13/13, and the census (command A) unchanged.
4. Optional same-commit note edits (table-internal, no schema change):
   - `shonen-skill-range` note: append "; arc3 r2 refreshed the count to 14/14 — rule #14's presence
     in the range is pinned by `a3r2-shonen-rule14-inrange`". (Its stored note still says 13/13.)
   - EX-41's operator-paths exempt row: name the proxy anchors (see §3.1).
5. Do not pin: truncated digests, commit hashes, count tokens, wave-internal citations (ratified
   exemptions). Do not widen the census scope rows (r4 precedent — untouched by this delta).

## 7. Attacks attempted, with verdicts

| attack | method | verdict |
|---|---|---|
| vacuous needles / no bite | per-entry mutation suite (`bite.py`): wrong-number mutation on extracted citing lines, all-occurrence needle removal elsewhere, isolation asserted | **51/51 bite, 68/68 at the pre-dedupe design**; the first run caught 13 non-biting entries — 12 multi-site needles (fixed semantics: class removal) and 1 in-range number mutation too mild (fixed: EOF+7) |
| two wrong needles in the first design | probe scratch run | caught: `8,316 B / `f95c5a05`` mis-matched an ellipsis; map-row needle guessed wrong (`# 07 — EVM interface inspection (round 3)` is the true H1) — both fixed and re-verified |
| landing the table without the expected re-pin | stale-pin demo | exit 2 `pointer_table_tampered`, no silent findings (frozen-run guard holds) |
| needles broken by C2's same-commit revision | grep of every custody-file needle against the in-progress worktree revision | survive (measured); H2 flagged for the one row-text needle |
| census under-scoping (missed citation sources) | S7 diff scan + S8-S11 instrument scans | found the census instrument's own SCORECARD citations (EX-41 covered 3, ratified); no other uncensused source |
| operator-path citation smuggled in as pinnable | classification | NO-ENTRY with cause; proxy coverage instead (§3.1) |
| relative-path citation conforms | `git show` `..` + `git cat-file -t` | refused (exit 128; `.ufo/gates/waves` absent) — NO-ENTRY as written + patch text |

## 8. Blockers, gaps, out-of-scope

- **H1 (handled):** the base table moved mid-seat; all scratch numbers re-based on `bfc42f1b`; the
  builder is re-runnable against any later revision.
- **H2 (open, named):** EX-41's custody-row/precedence needles must be re-verified after C2's
  landing revision; procedure in §6.1.
- **H3 (patch text):** README path forms (`.ufo/gates/custody-pair/README.md:103-105,129`) —
  `proposed-readme-path-forms.patch.md`; C2's file, so patch text only.
- **Out of scope, ratified:** wave-internal citations; round-report line pins; count/identity tokens.
- EX-41's seat report has landed (13:1xZ) and names this delta as the expected reconciliation; its
  `build-table.py` is the splice tool of record, so a missing PL-3 plan no longer blocks anything.

## 9. Proposed changes (patch-text paths)

- `proposed-readme-path-forms.patch.md` (this directory) — README:129 `../waves/` → `../../waves/`;
  README:103-105 receipt examples prefixed `.ufo/waves/`.
- Table-internal note edits (EX-41's file, same commit; §6.4) — no separate patch file.
- No other repo file is proposed for change by this seat.