# ScoutCoverageMap — "Go map type descriptor layout / Swiss maps under Ghidra"

**Verdict: mapped, NOT held; frontier-in-plan, not frontier-registered.** It is not held
ground and not unmapped. For C3 this means the entry is *depth on an unheld inference inside
an already-mapped Go surface*, not expansion into uncovered ground — and it may be written as
"held" only if the replay lands the PROVINCE held-test (LOG entry citing `evidence_id` and
subject sha256).

## Question

Is "Go map type descriptor layout / Swiss maps under Ghidra" held ground, frontier, or
unmapped — per `corpus/README.md` (coverage map + `## Frontier`) and `PROVINCE.md`?

## Evidence

### 1. Coverage map names the Go row but never the map layout

- `corpus/README.md:35` — the only README row carrying the Go entries (`r14-go-version-diagnosis`,
  `r15-go-snapshot-inventory`, `r16-go-selection-preview`, `r17-go-carrier-diagnostics`).
  Its state cell says: "r17 retains run-bound Ghidra analyzer logs for eight pinned x86-64 ELF
  carriers … 8/8 routes matched predictions … aether's post-bootstrap symbol-markup EOF was
  unpredicted." No token `Swiss`, `maptype`, `OldMapType`, or "map type descriptor" appears.
  The cell is not prefixed "held —" (the table's held marker used by most rows).
- `corpus/README.md:170-181` — `## Frontier` bullets (crash cap, RISC-V, `.jsc` mapping, >90MB
  PE, `capture-electron-scenario`, sasquatch, adb, PE reserve, runtime-obs depth, operator-gated
  providers). No Go/map-type bullet.
- `corpus/README.md:183-190` — `## Known gaps`; no Go/map-type item.

### 2. PROVINCE does not register it either, and defines the held test

- `PROVINCE.md:30-32` — "a catalog-listed tool is *available*, not *held* — ground moves to
  Core only after an end-to-end probe lands a `LOG.md` entry citing its `evidence_id` and
  subject sha256."
- `PROVINCE.md:52` — the only Go content in Core is the Cross-version-compare cell (`op`
  2.34.1→2.40.0, inventories 33,060→11,595, "pair by explicit evidence/ELF role"). No
  map-type-layout claim.
- `PROVINCE.md:73-93` — `## Frontier` bullets (PE subtypes, recorded crashes, alternate
  providers, macOS-only, EVM). No Go/map-type bullet.

### 3. The mechanism exists only as a labelled inference

- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:145-164` — "INFERENCE, aether cause":
  - `:146-148` — installed `go1.25.0.json` maps `runtime.maptype` to `internal/abi.OldMapType`
    (0x58 bytes), "Ghidra's `GoMapType` has no Swiss-map binding. aether's maps use the Swiss
    layout (0x70 bytes)."
  - `:149-152` — static byte trace reaches the logged pair `111938854` / `17645861`.
  - `:153-154` — same mechanism described by open, unmerged upstream PR #9348 (S032, tier B).
  - `:158-160` — "These are seat byte traces …, not a Ghidra replay with instrumentation. The
    exact invoking record is unresolved."
  - `:161-164` — corollary, also INFERENCE: the binding would silently misread every Swiss map
    type's size fields with no log line.
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:181-193` — "Not examined" omits
  patched-content correctness and layout proof.
- `SKILL.md:528` — decision-table limit: "INFERENCE, not replayed: Swiss maps read with the
  `OldMapType` layout from `go1.25.0.json` (S032 lead), not the patch fallback."
- `corpus/SOURCES.md:38` — S032 is tier B, "Candidate mechanism", not sole support.
- `corpus/lessons/round-17.md:37` — the binding appears as the rationale of a *reject row*
  ("aether's symbol-markup EOF is caused by the 1.25.0 patch fallback" rejected); a gate
  rationale, not a measured holding.

### 4. LOG keeps the cause open

- `LOG.md:2044-2050` — round-17 landing: eight carriers, 8/8 route compares; "Unpredicted:
  aether symbol-markup EOF after a successful fallback bootstrap (cause UNKNOWN)."
- `LOG.md:2096-2100` — second pass replicated every route and the EOF pair
  `17645861, 111938854`; no evidence id is recorded for a map-layout binding.

### 5. The lane plans it as the next depth step

- `SCORECARD.md:2408` — round-17 learning trend: "The new entry deepens held Go ground."
  (Surface-level Go ground; the Swiss mechanism inside it remained INFERENCE.)
- `SCORECARD.md:2422-2426` — "Planned: … either (a) depth on Go 1.24/1.25 Swiss-map markup,
  a replay that confirms or refutes the aether inference with a second Swiss-map carrier that
  has method-carrying map types, or (b) calibration …".

### 6. Earlier source-model rounds did not cover the layout

- `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`,
  `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`,
  `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` — zero hits for
  `maptype|swiss|map type|OldMapType` (grep exit 1). r15 pins snapshot bytes and labels, r16
  selection order; neither states a map-descriptor layout.

## Classification (three-way)

| Bucket | Fit | Basis |
|---|---|---|
| Held ground | **No** | Explicit "INFERENCE, not replayed" (`knowledge:158-160`, `SKILL.md:528`); no LOG entry with an `evidence_id` for the binding (`PROVINCE.md:30-32`; `LOG.md:2049-2050`). |
| Frontier (registered) | **No** | Absent from both canonical Frontier lists (`README.md:170-181`, `PROVINCE.md:73-93`). |
| Unmapped | **No** | Landed, indexed entry (`README.md:35`) plus `knowledge:145-164`, `SOURCES.md:38`. |

**Best single label: frontier (claimed/known, not yet held), with the qualifier
"frontier-in-plan"** — it is named as the next depth step at `SCORECARD.md:2422-2426` but is not
registered in either Frontier list. It is *mapped-unheld inference inside a held Go surface*.

## Consequence for C3

- `.ufo/waves/round-18/claims.json:24-27` — C3 is exactly the replay of this inference:
  "the aether mechanism status moves from unreplayed INFERENCE to replayed-confirmed or
  replayed-refuted on the pair."
- **Expansion vs depth:** not expansion. The surface and the specific mechanism are already
  indexed and written down; no new surface is opened. It is **depth**, and specifically the
  first measurement of ground that was *never held* — so the C3 entry must not present itself
  as deepening an already-held mechanism.
- **Held status:** only the replay's retained, run-bound logs (with `evidence_id` + subject
  sha256 per `PROVINCE.md:30-32`) can promote it. A C3 entry that only restates the r17 source
  trace and the byte trace adds no ground.
- **Integration note (L1):** if the replay lands, `corpus/README.md:35`'s state cell and
  `PROVINCE.md` currently carry no Swiss-map wording and would need one. I did not edit them.

## Commands and exit codes (all run read-only from the lane root)

```
$ grep -n "## Frontier" corpus/README.md PROVINCE.md
corpus/README.md:170:## Frontier
PROVINCE.md:73:## Frontier
rc=0

$ sed -n '170,181p' corpus/README.md | grep -niE 'go\b|swiss|maptype|map type'
rc=1   # no Go/Swiss/maptype bullet in README Frontier
# (a looser pattern with bare "map" matched only README:174 "mapping")

$ sed -n '82,93p' PROVINCE.md | grep -niE 'go\b|swiss|maptype|map type'
rc=1   # no Go/Swiss/maptype bullet in PROVINCE Frontier

$ grep -n "not \*held\*\|ground moves to Core" PROVINCE.md
30:provider candidates); a catalog-listed tool is *available*, not *held* —
31:ground moves to Core only after an end-to-end probe lands a `LOG.md` entry
rc=0

$ grep -n -i -E 'go\b|Go 1|golang|maptype|map type' PROVINCE.md
52:| Cross-version compare | ...
rc=0   # only Go-bearing row; no map-layout claim

$ grep -rn -i "swiss" corpus/ SKILL.md LOG.md SCORECARD.md SOURCES.md
corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:148
corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:162
corpus/lessons/round-17.md:61
corpus/SOURCES.md:38
SKILL.md:528
SCORECARD.md:2423
SCORECARD.md:2424
rc=0   # no "swiss" in corpus/README.md, PROVINCE.md, or LOG.md

$ grep -n -iE 'maptype|swiss|map type|OldMapType' \
    corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md \
    corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md \
    corpus/knowledge/2026-10-20-r16-go-selection-preview.md
rc=1   # no layout coverage in r14-r16

$ grep -n -E 'INFERENCE, aether cause|Swiss-map binding|exact invoking record|not a Ghidra replay|silently misread' \
    corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
145:- INFERENCE, aether cause:
148:    Swiss-map binding. aether's maps use the Swiss layout (0x70 bytes).
159:    `RevAetherEOF.md`), not a Ghidra replay with instrumentation. The exact
161:  - Corollary, also INFERENCE: the same binding would silently misread the
rc=0

$ grep -n -iE 'swiss|carrier diagnostics|go carrier|maptype|OldMapType' LOG.md
2033:## 2026-10-20 — round-17 — retained Go carrier diagnostics and routed r16 defects
2044:- C2 depth + capability: eight pinned Go carriers through REA 6.5.0 analyze
rc=0

$ grep -n "deepens held Go ground" SCORECARD.md
2408:- **Expansion unchanged.** The new entry deepens held Go ground. The new
rc=0

$ grep -n -E '"id": "C3"|Replay the round-17|unreplayed INFERENCE' .ufo/waves/round-18/claims.json
24:      "id": "C3",
26:      "claim": "Replay the round-17 aether INFERENCE (...)"
27:      "falsifiable_before_after": "... moves from unreplayed INFERENCE to replayed-confirmed or replayed-refuted ..."
rc=0

$ ls corpus/knowledge/ | wc -l
95
rc=0
```

## Observation vs inference

- **OBSERVED:** every quote and line anchor above; grep exit codes; the r17 entry's own
  "INFERENCE, not a Ghidra replay" label; the two Frontier lists lacking a Go/map bullet.
- **INFERENCE:** the three-way placement (frontier-in-plan rather than registered frontier) and
  the C3 scoring consequence. Both follow from the anchors but are my reading, not a corpus
  statement.
- **Open point, not blocking:** whether `SCORECARD.md:2422-2426`'s "Planned" counts as frontier
  registration for scoring purposes. The two files named in the ticket do not register it; the
  scorecard plans it as the next depth step.

## Bounds

No REA/Ghidra command, no carrier execution, no jj/git write, no install or upgrade, no edits
to README/PROVINCE/knowledge/SKILL/SCORECARD/LOG/SOURCES. The only file written is this report.
