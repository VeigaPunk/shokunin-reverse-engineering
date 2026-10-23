# R31-C1 — axis ruling AFTER data: coverage, narrow fit, or misfit

Seat: `KaidokuR31.CriticAxisC1After` (critic, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `c369242fee9f559f895e3f7956b1242076c7b1be`, freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`, data
`f368a101`, docs `0007731e`, tip `1288285eed81395e6af7c279a173b117b2c2eaa3`. I read the frozen
`.ufo/waves/round-31/claims.json`, the two knowledge entries, `AXES.md`, the wave-1
`CriticAxisFitC1.md`, the round-31 lesson, the round-29 and round-30 verifier spot-checks, and the
fleet rule in `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-31.md:361-364`. All
measurements are read-only against Git objects; the only lane write is this report. No REA run, no
clone, no install, no Git/jj write.

## Verdict

**narrow fit — coverage, narrow.** The round moved a real coverage artifact (the operation's first
PROVINCE row, from 0 mentions under every spelling, plus database-scope and virtual/shadow-table edge
classes that l7-04's own text disclaims), under a bar that can fail and that no control met. It is
*narrow* because the operation itself was already run, named and coverage-credited as knowledge; the
12 files are three schema families; and the lane's numeric coverage proxy is saturated, so no
numbered coverage improvement can be claimed. It is **not misfit**: the r29 misfit condition (no
surface entered governance, PROVINCE explicitly unchanged) does not hold, and the r30 outside ruling
admits exactly this shape one round earlier.

## The question, answered directly

*Is moving a once-run operation (inventory scope, one carrier, not in PROVINCE) into PROVINCE Core
with database-scope reading on 12 published files coverage?* **Yes, narrowly.** AXES.md defines the
coverage signal as "PROVINCE.md lists every surface; none unexplored without reason", and names
PROVINCE as the artifact. At the base the artifact was empty for this surface: 0 hits in `PROVINCE.md`
and 0 in `SKILL.md` for `sqlite`, `inspect[_-]sqlite[_-]database` or `.db` (both grep exits 1), and
no Core row owns SQLite reading under another name (the `Archive/package inventory` and
`host fallback readers` rows do not cover `.db` schema). The lane's knowledge entry l7-04 is
evidence, not province: the row committed at `0007731e` says so in words — "The lane's one earlier
run of this operation … had not entered PROVINCE" (`PROVINCE.md:345`).

The objects the round actually governs are new relative to that entry, on the entry's own testimony:
l7-04 records "column details not requested" and "does not establish behavior for changing
databases, WAL inputs, encrypted/corrupt files, or other schemas". C1's report exercises the opposite
side: complete columns (2,352 across the carriers), `virtual` and `shadow` kinds (five GeoPackages,
one virtual + three shadow tables each), 82 auto-index rows with `sql: null`, and overflow-chain
trigger SQL up to 128,117 characters. That is a previously ungoverned input class, not a re-run of a
held rule — the r29 shape (same rule, new fixtures, same output, PROVINCE untouched) does not apply.

The bar can fail and was shown able to fail before data: do-nothing, junk-row, all-false, no-reader
and id-rotated shortcut 0 of 12, Core-placement shortcut `province_ok=0`
(`SCORECARD.md:3263`, receipts at `7474d269`).

## Why narrow, not full fit

1. **The operation is not new.** The base tree holds `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`,
   which names the tool form, records a live `rea-agents@6.5.0` call with Evidence
   `ev_7572e622…`, and is mapped at `corpus/README.md:65,163`. The frozen sentence is false (M31-1).
2. **The surface already took a coverage verdict once.** `SCORECARD.md:521` at the base:
   `coverage | 10.0 → 10.0 … | improved (six RESULT-class verbs became admitted, quality-gated
   knowledge)`, and `LOG.md:811-821` (luna-round-7) records entry 4 as the SQLite result. That credit
   was for the knowledge artifact, not the province; the same operation is now counted a second
   time for a different artifact. The lane never said so in one place before this ruling.
3. **12 is not breadth.** Three producers, 12 distinct schema hashes, but three schema families
   (five PROJ files share a line; five GeoPackages share a layout). The entry's Limits and the
   PROVINCE row's Limits both say "three schema families", and `SCORECARD.md:3258` says the same —
   no overstatement survives in the data documents.
4. **The numeric proxy cannot move.** Command A measured now: base `116/116 → coverage_score 10.0`;
   `0007731e` and tip `118/118 → 10.0`; `missing: []`, `dangling: []` at all three. The proxy was
   already saturated, and its own row says "index integrity only, **not** fraction of the REA domain
   held" (`SCORECARD.md:23`, the owned-axes coverage row, at base and at tip). So C1 must not be presented as a scored coverage gain; the gain is the
   governance row plus the new classes.
5. **The Core row is an appendix row.** It sits under `## Round-31 additions to Core` and the section
   states "the Core table above is not rewritten" (`PROVINCE.md:345`). That is the lane's convention
   (rounds 4, 20, 30) and it passes `province_ok` plus the placement control, but a reader of the
   `## Core` table alone still will not see SQLite.

## Does M31-1 (frozen sentence false) change the verdict?

**No.** Reasons:

- It is a base-state fact, not a data outcome. It was true before the freeze and before any counter
  ran; the data neither creates nor removes it.
- The measured predicate contains no novelty clause: 12 live envelopes equal to the oracle, one
  committed full-envelope match each, entry citing S096, PROVINCE row under a Core heading. The fleet
  rule judges the claim on the predicate declared before data, and that predicate is unchanged
  (`SCORECARD.md:3251`).
- It was already priced in before data. Wave-1 `CriticAxisFitC1.md` ruled narrow fit and routed the
  correction; the round then recorded it in four places — lesson M31-1 (`corpus/lessons/round-31.md`),
  `SCORECARD.md:3254`, the entry's Claim section, and `PROVINCE.md:345` — and made the defect class
  testable (`corpus/QUALITY.md:66`, row 56: every spelling of the surface). The lane did not let the
  false sentence stand as its own record.
- What it changes is the **credit**, not the axis: not "a new operation enters Core" (overclaim), but
  "the operation's first Core row and the database-scope/virtual-shadow edge classes enter
  governance" (defensible). That sentence *is* the narrow qualifier. If one instead stipulates the
  claim's surface to be "a never-run operation", the false premise voids that description, but the
  remaining increment is still the round-30 admitted shape, so the axis label survives narrower —
  the verdict does not flip.
- One residual: the durable round log does not carry the correction. `LOG.md:3028` (tip) states the
  C1 receipt and "PROVINCE `## Round-31 additions to Core`" with no M31-1 line, so a reader of the
  LOG alone can still take "PROVINCE gains the operation" as the round's claim. See correction 1.

## Strongest argument against this ruling (the misfit case)

**The double-credit / unfalsifiability argument, at full strength:**

> l7-04 was already the coverage move of luna-round-7 — the lane's own scorecard says so, and says
> the numeric proxy is index completeness, not domain fraction. In practice the lane's notion of
> coverage is "an admitted, quality-gated knowledge entry from a real carrier with stated limits",
> which l7-04 is. Round 31 then re-reads the same operation at a wider scope and adds a one-line
> appendix row that the Core table itself does not absorb; the row's content is a restatement of the
> entry plus the SKILL table. Under the fleet rule, re-stating held ground is quality work, never
> coverage. If a signpost row converts held ground into coverage, coverage becomes unfalsifiable:
> every held surface can be re-credited by adding a row, and this operation is counted twice
> (luna-round-7 and round 31). The false frozen sentence is the tell — the claim sold "discovery"
> while delivering "bookkeeping"; the real gains are depth (oracle equality on new edge classes) and
> operability (a runnable counter). Therefore: misfit, a re-score of held ground.

**Why it fails, and what it still wins:**

- It substitutes the proxy for the axis definition. AXES.md names PROVINCE.md as the coverage
  artifact, and `SCORECARD.md:23` explicitly disclaims the proxy as domain fraction. The entry is the
  evidence the lane's own PROVINCE convention requires *before* promotion ("ground moves to Core only
  after an end-to-end probe lands a LOG entry citing its `evidence_id` and subject sha256"); it is not
  the promotion. l7-04's own limits show the database scope was not governed by it.
- The controlling precedent is one round old, decided by the same outside closure, on the same l7
  batch: R30-C1 claimed "PROVINCE Core gains the positive input class of REA operation
  `inspect_rust_binary`" while "the lane holds only null-metadata runs of this verb (l7-02)", and the
  verifier ruled **fit**: "A previously ungoverned input class … enters PROVINCE Core from 0 mentions
  under a bar that can fail and that no trivial control met"
  (`corpus/lessons/round-30-verifier-spotcheck.md:64-65`), then admitted the round
  (`SCORECARD.md:3245`). The double-credit argument, if right, would have rejected round 30.
- r29 is distinguished, not ignored: there "No surface, tool, operation or edge class entered
  governance this round" and PROVINCE said "Frontier status unchanged"
  (`corpus/lessons/round-29-verifier-spotcheck.md:50-51`). Here PROVINCE moved from 0 rows to one and
  new edge classes were measured under a failing bar.
- **What the argument wins:** the four narrow qualifiers above (no new verb; 3 families; flat proxy;
  appendix row). It is a correct attack on any wording that calls this "coverage improved" without
  them — not on the axis label itself.

## Evidence (produced 2026-10-23; commands run in the lane, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset)

| # | Command | Output excerpt | Exit | UTC | Label |
|---|---|---|---|---|---|
| F1 | `git show c369242f:PROVINCE.md \| grep -c -i -E 'sqlite\|inspect[_-]sqlite[_-]database\|[.]db\b'` | `0` | 1 | 04:34:52 | observation |
| F2 | same for `SKILL.md` | `0` | 1 | 04:34:52 | observation |
| F3 | `git grep -l -E 'inspect[_-]sqlite[_-]database' c369242f -- corpus/knowledge` | `…l7-04-inspect-sqlite-database.md`; `…l8-01-6p4-symmetry-battery.md` | 0 | 04:34:52 | observation |
| F3b | `git show c369242f:corpus/README.md \| grep -c '2026-10-16-l7-04'` | `2` (lines 65, 163) | 0 | 04:34:52 | observation |
| F4 | `python3 /fast/scratch/hyaku/kaidoku-r31/seats/w2/CriticAxisC1After/commandA.py <REV>` (SCORECARD recipe A, verbatim) | base `knowledge_files 116, mapped 116, coverage_score 10.0`; `0007731e` `118, 118, 10.0`; tip `118, 118, 10.0`; `missing []`, `dangling []` at all three | 0 | 04:34:52 | observation |
| F5 | `cat .ufo/waves/round-31/after/c1-sqlite-positive-at-0007731e.txt \| tail -2` | `carriers=12 pass=12 target=12 entry_ok=1 (ok) province_ok=1 (ok)` / `exit=0` | 0 | 04:34:52 | observation (committed receipt; not re-run by this seat) |
| F6 | `git show 0007731e:PROVINCE.md \| sed -n '343p;345p'` | `## Round-31 additions to Core (verified 2026-10-23)`; `Addition to Core for REA's SQLite reader (the Core table above is not rewritten; …)` | 0 | 04:34:52 | observation |
| F7 | `git show 0007731e:corpus/README.md \| grep -c '2026-10-23-r31'` | `4` (coverage-map 83-84; knowledge rows 183-184) | 0 | 04:34:52 | observation |
| F8 | base `SCORECARD.md:521`; base `LOG.md:811-821` | `coverage … improved (six RESULT-class verbs became admitted, quality-gated knowledge)`; `### luna-round-7 — coverage: six 6.5.0-verb knowledge entries (72 → 78)` | 0 | read 04:2x | observation |
| F9 | `corpus/lessons/round-30-verifier-spotcheck.md:64-65`; `round-29-verifier-spotcheck.md:50-51` | fit: "A previously ungoverned input class … enters PROVINCE Core from 0 mentions under a bar that can fail"; misfit: "No surface, tool, operation or edge class entered governance this round" | — | read 04:2x | observation (quoted) |
| F10 | `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-31.md:361-364` | "Name the axis by the surface the round changes … Re-scoring a rule the lane already holds on new inputs … is quality work, never coverage or depth." | — | read 04:2x | observation (quoted) |
| F11 | `corpus/QUALITY.md:66` (row 56) at tip | every-spelling rule for novelty sentences, citing M31-1 | 0 | 04:34:52 | observation |

Textual facts F8-F10 are citations, not measurements; the outputs are quoted verbatim from the files
and the reading times are approximate within this session (all before the 04:34:52Z measurement pass).

## Impacted axes

| Axis | Verdict | Why |
|---|---|---|
| coverage | **narrow positive; no numeric movement possible** | first PROVINCE Core row for the operation (0 mentions under every spelling at base) plus database-scope/edge classes; proxy saturated at 10.0 (116/116 → 118/118), so the gain is not and cannot be a score change |
| depth | supports, not claimed | oracle equality on 2,352 columns, 740 schema rows; C2 owns the depth claim |
| calibration | **at risk without the qualifiers; currently mitigated** | the frozen sentence is false (M31-1) but corrected in lesson, SCORECARD:3254, the entry and PROVINCE:345, and QUALITY row 56 makes it testable; residual: LOG.md does not carry it |
| freshness | minor gap | provider SQLite version differs between the two entries under the same 6.5.0 pin (3.53.4 CLI envelope vs 3.54.0 in the l7-04 MCP receipt); see below |
| operability / adjacency | no harm | the counter runs and the doc gates have receipts; C2's SKILL table is the adjacent artifact |

## Secondary finding — a duplicate authority on the reader's engine version (freshness)

The committed C1 envelope records `engine: {"name": "SQLite", "version": "3.53.4"}`
(`corpus/evidence/round-31/c1/envelopes/chinook-autoinc.json`; observed 04:34:52Z), while l7-04's own
cited MCP receipt records `"provider":{…,"name":"REA SQLite database inspector","version":"SQLite
3.54.0"}` (`.ufo/waves/luna-round-6/receipts-B/leg-6.md:35`) — the same `rea-agents@6.5.0` pin. On
this host node v24.21.0 bundles SQLite 3.53.4 and libsqlite3 is 3.54.0 (observed 04:34:52Z:
`node -p "process.versions.sqlite"` → `3.53.4`; `python3 -c "import sqlite3; print(sqlite3.sqlite_version)"`
→ `3.54.0`). So the provider version follows
the runtime path (MCP vs CLI, node build), not the pin. The new entry states "REA runs SQLite 3.53.4
bundled in node v24.21.0" and limits itself to "one pin, one host" without reconciling the 3.54.0
already in the corpus; `PROVINCE.md:349` correctly attributes 3.53.4 to the node:sqlite worker, so
the row is defensible, but the two corpus entries now disagree on their face with no cross-reference.
This is a freshness/calibration nit, not a coverage one, and it does not touch the predicate — which
deliberately excludes `engine.version` from the oracle comparison because it is runtime-dependent.
Recommended: one Limits clause in the C1 entry; no score change.

## Smallest safe corrections (for the L1; none is an instrument, claim or target edit)

1. **LOG.md, round-31 block, one line** next to the R31-C1 receipt: the M31-1 correction pointer
   (frozen novelty sentence false; increment = first Core row + database-scope reading;
   `SCORECARD.md:3254`, lesson M31-1). The durable round log is the only record that still reads as
   if the frozen sentence were true. Do not edit `claims.json`.
2. **C1 entry, Limits, one clause**: the engine version belongs to the CLI's node-bundled SQLite
   (node v24.21.0 → 3.53.4); the l7-04 MCP run of the same pin reported 3.54.0
   (`luna-round-6/receipts-B/leg-6.md:35`), so the provider version is a runtime-path property.
3. **Word the closure verdict as "coverage, narrow"**, not "coverage improved" unqualified. The
   SCORECARD row already says "target met as measured; pre-data axis ruling narrow fit"
   (`SCORECARD.md:3251`); this is a wording lock. Do not raise the coverage score: it is saturated at
   10.0 and its own observable disclaims domain fraction.

Explicit non-corrections: do not amend `.ufo/waves/round-31/claims.json`, the target line, the
carriers, the predictions or the counters; do not add a second unqualified coverage credit for this
operation; do not claim 12 carriers as breadth.

## Artifacts

All under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/CriticAxisC1After/`:

| file | sha256 | what |
|---|---|---|
| `commandA.py` | `73fc158ecc016590ef871cac944afaa27344be06b9cc93418859a54eea3da1d9` | verbatim SCORECARD recipe A, run at three revisions (F4) |
| `evidence.txt` | `a2b3003ff9979ec852f17c83c4496b0c63df82c31e86abe4057609d5bfc87116` | untimed evidence log (document reads, excerpts) |
| `evidence-timed.txt` | `ba4df767dbddb4b0ff9c6e3d73434bcefd3955942222e387167b90c4be670d1d` | the 04:34:52Z pass: 12 commands, each with UTC time, output and exit code |

No installs or updates. No REA invocation. No lane, fleet, Git or jj state mutated; the only lane
write is this report. Counter receipt F5 is the L1's committed run, quoted, not re-executed by this
seat.
