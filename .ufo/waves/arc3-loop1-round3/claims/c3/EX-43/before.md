# EX-43 before-state — citation-drift pointer table: arc3-era coverage census

Seat EX-43 · chain c3 · role executor (before-state) · wave `arc3-loop1-round3` · 2026-10-19
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`.
The real pointer table was **read-only** for this seat; every mutation ran on marked copies under
`/var/tmp/ex43-scratch/` (never `/tmp`) or in a throwaway shared clone. No git mutation in the repo.

## 1. Table before-state (measured)

| item | value |
|---|---|
| `pointer-table.json` | 14,694 bytes, sha256 `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` |
| `entries` | **31** |
| `quoted` | 4 |
| `exempt` | 3 |
| `expected.json` pin | in force: `pointer_table.sha256` == the table digest above (F3 coupling; any edit must re-pin in the same commit) |
| probe at HEAD, default | `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` (`probe-before-default.txt`) |
| probe at HEAD, `--strict` | `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` (`probe-before-strict.txt`) |
| probe `--selftest` | `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0` (`probe-before-selftest.txt`) |

## 2. Existing coverage of the arc3-era citations: **0**

Mechanical, not asserted:

- `0` of the 31 entries + 4 quoted mention `arc3` at all
  (`census.out`: `table entries/quoted mentioning 'arc3': 0 []`).
- Target-file overlap between the existing table (15 target files) and the candidates (12 files) is only
  `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md` — different lines/needles in every case.
- One substantive near-overlap, for honesty: the SHONEN.md:6 → SKILL.md range pointer itself was entered by
  arc2-r10 (`shonen-skill-range`); what arc3-r2 added is a **new citing sentence** at `SCORECARD.md:1435`
  that is itself uncovered → candidate `sc1435-shonen-refresh-record`.

**Blindness proof (drift injection, scratch clone rev `19944eff7252517367ccc27a11175d143709ef94`).**
Two live arc3 pointers were corrupted in the clone (r1-entry `:17` range `149-155` → `140-146`;
`SKILL.md:246` range `86-89` → `90-93`):

- real 31-entry table at the drifted rev → `clean findings=0 exit=0` (**blind**) — `drift-blind.txt`
- 17-candidate extension at the same rev → `2× citation_dead exit=1` (**caught**) — `drift-caught.txt`

## 3. Gap census — 17 entry candidates + 1 quoted candidate (all resolve at HEAD)

Scope = the four classes the frozen claim names (r1 knowledge entry; arc3 SCORECARD sections' needles;
round-2 registry rows; custody receipt conventions), plus SKILL.md's rule-#14 block, which is the arc3-r2
landing that cites arc3-r1 artifacts. Every candidate below was validated in a scratch extension of the
table (`scratch-table-ext.json`, 48 entries, sha256 `0b01f52142924ce96e2cdddb84c15102f005dac17f07852ff0e6eb2f3d3a388f`)
→ probe `--strict` **clean findings=0 exit=0**; a needle-flip teeth control → **1 finding exit=1**
(`census.out`). Full objects, landing-ready: `candidate-entries.json`.

### Class A — the r1 knowledge entry (`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`, arc3-r1)

| # | id | citing | states | needle (verified hit) |
|---|---|---|---|---|
| 1 | `r1evm-cites-r307-erratum-offset` | entry:17 | `…r3-evm-interface.md:149-155` | `JUMPDEST dispatch-target position` |
| 2 | `r1evm-cites-r307-stub-inference` | entry:18 | `…r3-evm-interface.md:59-70` | `inferred_state_mutability` |
| 3 | `r1evm-cites-quality-id-domain` | entry:21 | `corpus/QUALITY.md:24-25` | `full domain` |
| 4 | `r1evm-cites-quality-parsed-empty` | entry:24 | `corpus/QUALITY.md:21` | `parsed-and-empty` |
| 5 | `r1evm-cites-r307-kind-hypothesis` | entry:25 | `…r3-evm-interface.md:44-45` | `richer bytecode` |
| 6 | `r1evm-cites-r307-positional-encoding` | entry:26 | `…r3-evm-interface.md:93-96` | `POSITIONAL arg` |
| 7 | `readme38-arc3-r1-map-token` | `corpus/README.md` (anchor, line unpinned) | — | `2026-10-19-arc3-r1-evm-real-solc` (hit at :38) |

### Class B — arc3 SCORECARD sections (`SCORECARD.md:1338` arc3-r1, `:1419` arc3-r2)

| # | id | citing | states | needle |
|---|---|---|---|---|
| 8 | `sc1435-shonen-refresh-record` | `SCORECARD.md:1435` | `SHONEN.md:6` | `14/14` |

The arc3-r1 section is pin-free **by design** (its own statement, `SCORECARD.md:1392`); measured zero
`path:line` citations in the whole range → adjudication, not a gap.

### Class C — round-2 landing in SKILL.md (rule #14 text, arc3-r2)

| # | id | citing | states | needle |
|---|---|---|---|---|
| 9 | `skill-rule14-cr2-stale-identity` | `SKILL.md:246` | `…/arc3-loop1-round1/seats/CR-2.md:86-89` | `stale against the` |
| 10 | `skill-rule14-verdict-d9` | `SKILL.md:248` | `…/arc3-loop1-round1/claims/c1/verdict.md:149-153` | `Three different applied identities` |
| 11 | `skill-rule14-r1evm-recheck-line` | `SKILL.md:252` | `…arc3-r1-evm-real-solc.md:7` | `recheck:` |
| 12 | `log1412-landing-identity-quoted` (quoted) | `SKILL.md:254` | `LOG.md:1411-1412` | `dd986f56` — **on :1412, not :1411** (the digest wraps; a `:1411` pin fails, measured) |

### Class D — round-2 registry rows (`SKILL.md:389`, `:390`)

Both rows were scanned: **zero `path:line` citations** (commands and paths only). Covered as row-existence
anchors (the same class as the existing `skill-registry-row`):

| # | id | file | needle (hit line) |
|---|---|---|---|
| 13 | `skill-registry-row-citation-drift` | `SKILL.md` | `\| citation-drift \| probe / kaidoku \|` (:389) |
| 14 | `skill-registry-row-custody-pair` | `SKILL.md` | `\| custody-pair \| tool / kaidoku \|` (:390) |

### Class E — custody receipt conventions (`.ufo/gates/custody-pair/README.md`)

The README's v1-compat table names three in-tree example receipts; the round-evidence section names the
EX-31 pair; the round's convention is that every v2 receipt self-pins the instrument's sha256. File-level
(the README uses paths, never line numbers) → anchor entries:

| # | id | file (target) | needle (hit line) |
|---|---|---|---|
| 15 | `custody-readme-v1-stanza-example` | `…round1/claims/cross/receipts/config-pre-pair.txt` | `capture-utc: 2026-10-19T09:57:18Z` (:3) |
| 16 | `custody-readme-v1-sums-example` | `…round1/claims/c3/EX-26/custody-sha256.txt` | `16f496e6` (:3) |
| 17 | `custody-readme-v1-pipe-example` | `…round1/claims/cross/receipts/config-pre-pair-metadata.txt` | `format: path \| inode \| ctime` (:4) |
| 18 | `custody-receipt-v2-tool-self-pin` | `…round2/claims/c3/EX-31/capture-pre.txt` | `tool: custody-pair\.py  sha256 112d01dc` (:3) |

## 4. Adjudication candidates (NO-ENTRY + cause)

1. **SCORECARD arc3-r1 section :1338-1400** — pin-free by design (its own record, `:1392`); measured zero
   `path:line` → nothing to pin.
2. **`SCORECARD.md:1415`, `:1494` `.ufo/waves/arc2-loop1-round10/C3.md`** — file-level mention of a
   pre-existing dirty path; a defect record, not a pointer → NO-ENTRY.
3. **`.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/` (README:129 directory ref)** — a directory cannot
   carry a line pin; its load-bearing file is covered by candidate 18 → NO-ENTRY.
4. **Self-identity records** (`8,316 B`/`f95c5a05…`, `8,598 B`/`d8d85949…`, `10,225 B`/`dd986f56…`,
   `SKILL.md` 390 lines/`c134afcb…`) — bind a revision, not a live line; rule #14 requires re-derivation
   after every revision, so a static pin would manufacture a false-failure class → NO-ENTRY by default
   (optional: `exact` pins if the chain wants the words frozen).
5. **R1-entry evidence-inventory path lists** (`:5`, `:11-16`, `:33`; ~30 wave paths, no line numbers) —
   evidence inventory, not live pointers; the r7 entry's own source list is likewise unpinned → NO-ENTRY.
6. **LOG.md internal arc3 citations** (e.g. `LOG.md:1449`) — append-only history; the standing `exempt`
   clause → NO-ENTRY.

## 5. After-count projection (the chain's before → after)

- entries **31 → 48** (17 added) and quoted **4 → 5** if all candidates land green; the scratch extension
  proves that exact object is probe-clean at HEAD, and that each candidate is individually separable
  (order-independent append; no existing entry's `line` moves).
- The final N is EX-41's adjudication call; whatever lands, `expected.json` must re-pin the new table's
  digest in the same commit (F3), and the whole-table sha256 above is the before-value to compare against.

## 6. Scope boundary (stated, not silent)

- Covered: every `path:line` citation inside the four named classes + the SKILL.md rule-#14 block.
- **Not** census'd: round-1/round-2 wave-tree-internal citations (hundreds of historical artifacts) —
  no scope widening (r4 precedent). Residual gap is named here for the chain to accept or adjudicate.

## 7. Evidence index (all under `claims/c3/EX-43/`)

| file | content |
|---|---|
| `census.out` | the full census transcript (counts, sim table, scratch validation, teeth, adjudications) |
| `candidate-entries.json` | the 17 + 1 candidate objects, landing-ready, with scratch validation hashes |
| `census.py` | the re-runnable census + validation script (writes only scratch + this dir) |
| `scratch-table-ext.json` | the validated 48-entry extension (scratch copy; NOT the real target) |
| `probe-before-{default,strict,selftest}.txt` | before-state probe runs at HEAD |
| `drift-blind.txt` / `drift-caught.txt` | the drift-injection blindness proof / catch |

Re-run: `TMPDIR=/var/tmp/ex43-scratch python3 .ufo/waves/arc3-loop1-round3/claims/c3/EX-43/census.py`
(exit 0 = all candidates resolve, extension clean, teeth fire).