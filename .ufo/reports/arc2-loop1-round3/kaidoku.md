# kaidoku arc2-loop1-round3 — freshness verified / coverage inconclusive / operability form-refuted

Date: 2026-10-18. Wave: 64 seats on `devin/deepseek-v4-1-flash-max`,
parent-integrated, no seat commits; 60 seat reports delivered (4
non-completions — named dispatch defect, second consecutive round). Work
commits: `fd30b9c` (content + receipts), `dbba2dd` (wave artifacts) — lane
identity; this report lands after and cites them.

**Round not admitted: 1 of 3 claims verified.** The other two are honest
stops with the full evidence trail — not trades, not forced passes.

## Work performed

Claims (3, distinct axes):

1. **C1 — freshness** (fleet): drain the dead-pointer class. The wave proved
   the declared form was defective — the re-point target `:2938/:2940` was
   itself dead (live stanza `:3296`, pin `:3298`; five positions today), and
   `:9`/`:80` carry pin staleness, not pointers. Landed content-anchored:
   PROVINCE.md:18 + SCORECARD.md:59 single-line re-anchors (162/766 held);
   append-only errata at mcp-registrations (88→111) and r4-16 (936→975),
   every pointer superseded by `[mcp_servers.rea]` + receipt sha256. Dated
   records (SCORECARD:270, :698) adjudicated in-section, not edited.
2. **C2 — coverage** (owned): the >90MB PE scale-wall retry. Bisect leg held
   (`ev_92dea347…`); the wall leg died at its own outer cap (typed
   `cancelled`, no evidence, 3600s deadline untested) — INCONCLUSIVE per the
   pre-declared outcome taxonomy (E11/R2/CR3/CR7 convergent). Knowledge
   accrued (recorded); no entry landed.
3. **C3 — operability** (fleet): citation-drift gate. Implementations proven
   (E14/E15, selftests green, live red→green) but the form fails the Gate
   standard on measured grounds (CR4/R3/R6/CR7) — adjudicated to a future
   probe; the durable repair (content anchors) shipped via C1.

Work items (pointers): dead-pointer census (E23 instrument, sha256
`7cd2a760…`; before at `679af5d`: unwarned 6; after at `dbba2dd`: **0**,
minted 0); PE inventory (E6: 180 .exe, target `7a2ccd68…` byte-identical to
r4-12; no ARM64 rung between 1.19MB and 91.7MB); knob verification (E7:
`REA_GHIDRA_STARTUP_TIMEOUT_MS` schema-capped 2^31−1, default 330s not 900s —
PROVINCE/README correction debt; `GHIDRA_HEADLESS_MAXMEM` unvalidated, live
`-Xmx8G` observed); bisect leg (E10) and wall leg (E11: 87,639B typed-cancelled
stdout, RSS 8.89GB, ghidra.log 277→577 lines still analyzing at kill);
resource watch (E13/CR2: systemd-containment recipe for the decisive run);
config-churn witness (E22/SC2/CR8: four states + one in-window
mutate-and-revert, writer = interactive session afa2dd53); gate engineering
(E14/E15/E16/E17 + R3's F1-F3 fixes + R6's defect list, all preserved in the
wave as the probe-round raw material).

Cross-domain evidence (routed, not absorbed): the config.toml writer is the
operator's interactive Kimi client (model-table churn: opencode-go-7,
glm-5.3-flash-max) — an operator-domain surface; the lane records, never
repairs. No sibling repo touched.

## Landed changes

- `PROVINCE.md` / `SCORECARD.md` — single-line re-anchors (:18, :59);
  dated-record adjudications live in this round's SCORECARD section. LOG: this
  entry; commit `fd30b9c`.
- `corpus/knowledge/2026-10-13-mcp-registrations.md` (88→111) and
  `2026-10-13-r4-16-frontier-rescan.md` (936→975) — append-only errata,
  prefix-identity proven. Commit `fd30b9c`.
- Receipts: 5-path pre/post-pair (endpoints 5/5; config.toml claim VOID as
  bare — witnessed in-window mutate-and-revert), bisect meta, 91.6MB cancelled
  envelope, mutate-revert drift record. Wave reports at `dbba2dd`.
- NOT landed (honest): the C2 knowledge entry (inconclusive); the C3 gate +
  registry row (form refuted); SCORECARD.md:270/:698 in-place edits (dated
  records). No config edits or restores; no pushes.

## Before → after measurements

- **C1** — E23 instrument (unit = unwarned dead loci, append-only files):
  **6 → 0** at `dbba2dd` vs `679af5d`; minted 0; current-surface wide-dead
  4 → 3 (:59 repaired; :291/:698 dated); instrument's blanket verdict stays
  FAIL by its raw-count semantics (append-only keeps dead lines; the unit is
  stated, per S1/E2 §7). Command A at `dbba2dd`: 79/79, 10/10, 10.0/10.0.
- **C2** — bisect leg: exit 0, 44.117s, 6,337 procedures, deterministic rerun
  byte-identical. Wall leg: 30m01.228s, exit 124, typed `cancelled`,
  `cleanup:complete`, zero evidence ids — the 3600s deadline never fired.
  Coverage: 79/79 both sides; no entry, no score change.
- **C3** — E15 gate: selftest 10/10; live `failed findings=10 exit=1` at HEAD;
  line-neutral-repair scratch → clean exit 0. Capability row NOT entered.
- Custody: pre 17:55:49Z / post endpoint 5/5; in-window excursion recorded
  verbatim (receipts/drift-config-toml-mutate-revert-20261018T180140Z.txt).

## SHONEN — all four boxes retained [~]

- [~] Decision tables/error patterns/checklists: craft 10/10 + custody SOP
  (5-path) + error-pattern table (provider_timeout vs cancelled now distinct,
  E11/R2); command A at `dbba2dd`; no outside verifier (`SHONEN.md:5-6`).
- [~] End-to-end task: the C2 battery (bisect held; wall leg typed-cancelled
  cleanly) and the 5-path custody pair; receipts + this LOG entry; the 2026-
  10-15 libjq smoke at `evidence/round-1-2026-10-15/rea-bundle.json`; no
  outside verifier (`SHONEN.md:7-8`).
- [~] Executable without oral context: the decisive-run recipe, the
  content-anchor erratum form, and the instrument set replay from the record;
  documentation-level only (`SHONEN.md:9-10`).
- [~] No cross-domain bleed: the config churn writer is operator-domain and
  was recorded, not touched; safety/adjacency boundary intact
  (`PROVINCE.md:88-116`); no complete outside audit (`SHONEN.md:11-12`).

Gate `../PROTOCOL.md:63-72`: lane-dispatched seats are still the lane; `[x]`
needs a named non-author verifier — none exists; all four boxes stay `[~]`.

Stale-lane duty: no mission exceeded two driver ticks (single parent session);
all seat processes closed (E13 post-state 0 JVMs, 0 session dirs); the wave's
two mid-flight worktree rehearsals (README dummy rows) were reverted by their
seats and verified byte-identical to HEAD.

## Verdicts

- freshness: **improved** — unwarned dead loci 6→0, minted 0, durable
  content-anchor form landed.
- coverage: **unprovable** (honest stop) — the wall leg is inconclusive
  (outer-cap kill; deadline untested); nothing harmed (79/79 both sides).
- operability: **not verified** (honest stop) — gate form refuted on measured
  grounds; implementations preserved; probe conversion named.
- depth / calibration / coverage-score: **unchanged** (command A at `dbba2dd`).

Stagnation window 3/10; no capability entered. Regimen continues to round 4.
