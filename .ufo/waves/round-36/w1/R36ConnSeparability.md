# R36ConnSeparability — cross-claim causal separability of R36-C1 and R36-C2

Seat: `R36ConnSeparability` (leaf connector; no subagents, no background jobs, no `agent://all` broadcast).
Round: kaidoku-shokunin round 36, wave 1. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
L1/integration owner: `KaidokuR36`. All lane git access read-only (`git log/show/ls-tree/cat-file/rev-parse/status` only; no add/commit/checkout/reset/stash/pull/push, no jj). Fixture work ran in a throwaway clone under scratch, now removed; every cited output is reproduced verbatim below.

## Verdict up front

R36-C1 and R36-C2 **are causally separable as frozen**, with an asymmetric coupling:

- **C1 → C2: exactly one forced edit** — C1's knowledge entry + README coverage-map row move C2's command-A coverage count from 122/122 to 123/123, forcing a re-statement of the first `N/N knowledge files mapped` figure in the SCORECARD `owned:coverage` row before the final-tip C2 measurement. Demonstrated on a fixture: the C2 counter then fails with exactly this one mismatch and nothing else.
- **C1 → C2: two placement constraints (not edits)** — C1's PROVINCE edit must not touch lines 1–120 (the SHONEN box-4 asserted `PROVINCE.md:97-118` Adjacent span, plus the asserted `:8-14` and `:24` version-pin lines precede it), and C1's README Firmware-row edit (which sits *inside* the coverage-map section) must not add/drop any `2026-10-NN-…` stem token.
- **C2 → C1: zero coupling.** C2's landing commit `d2e46ef5` changed only `SCORECARD.md` and `SHONEN.md`; C1's counter reads neither file (nor `SKILL.md`, nor `evidence/round-1-2026-10-15/result.json`). Nothing C2 has landed or will land (the SCORECARD re-state) intersects C1's read set. Verified by counter source inspection and by re-running C1 at a fixture tip that included the simulated C2 re-state.

The frozen plan text already anticipates the one forced edit ("the row is re-stated then"); this report adds the verified mechanism, the exact line-level constraints, and a landing order that keeps both measurements legal without touching any frozen rule.

## 1. Read-set inventory (from counter source, `git show 790561d4:tools/round-36/{c1,c2}-counter.py`)

### c1-counter.py — every repo path read (all via `git show REV:path` / `git cat-file`)

| Path | Rev argument | Purpose |
|---|---|---|
| `corpus/evidence/round-36/c1/carriers.json` | freeze **and** rev | carrier spec; byte-compared (`carriers_unchanged`) |
| `tools/round-27/xpin-attribute.mjs` | freeze | frozen evidence-id recomputation tool bytes |
| `corpus/evidence/round-36/c1/K{1..4}/oracle.tsv` | freeze **and** rev | frozen independent oracle; byte-compared per carrier |
| `corpus/evidence/round-36/c1/K{1..4}/before.json` | rev | no-sasquatch envelope (subject/op/gap/hits/evidence-id) |
| `corpus/evidence/round-36/c1/K{1..4}/after.json` | rev | sasquatch envelope (subject/op/gap/hits/evidence-id) |
| `PROVINCE.md` | rev | `## Round-36 additions to Core` section, first-cell `sasquatch` row citing the entry |
| `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` | rev | entry present; `source: S…` ids |
| `corpus/SOURCES.md` | rev | registry row: 11 cells, opened `2026-10-26`, used-by lists the entry |
| `corpus/README.md` | rev | `## Coverage map` section contains a `\|`-row with the entry stem |

Plus a subprocess: `node <frozen xpin> --pkg65 <rea-agents 6.5.0 pkg> --pkg67 <same>` over the 8 envelopes (reads the 6.5.0 package files from disk, not git). It never reads `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `evidence/round-1-2026-10-15/result.json`, or the `corpus/knowledge/` tree (only the single entry path above).

### c2-counter.py — every repo path read

| Path | Rev argument | Purpose |
|---|---|---|
| `SCORECARD.md` | rev **and** base | units: `## Owned axes` rows, `## Capabilities` table rows |
| `SHONEN.md` | rev **and** base | units: `- [x~] …` boxes + 2-space-indented assertion lines |
| pointer targets named in those units | rev (current) and base (guard) | `git cat-file -e` + `git show`; line-range containment |
| `corpus/knowledge/` (whole tree) | rev | command A: `git ls-tree -r --name-only` count of `*.md`; plus each `SKILL.md`-rule-referenced knowledge file read for line counts |
| `corpus/README.md` | rev | command A: `## Coverage map` section → mapped-stem regex `2026-10-\d{2}-[a-z0-9-]+` |
| `SKILL.md` | rev | command A: `## Queue-drain craft ` rule blocks; heading range `## Queue-drain craft` |
| `evidence/round-1-2026-10-15/result.json` | rev | command B: aligned/total obligations |
| `PROVINCE.md` | rev | heading range of the **first** line starting `## Adjacent` (stop = any line starting `#`) |

Concrete unit pointers at HEAD that touch C1-writable files (extracted with the counter's own regexes): `OWNED: corpus/README.md` (no range), `SHONEN: PROVINCE.md:97-118`, `SHONEN: PROVINCE.md:8-14`, `SHONEN: PROVINCE.md:24`, `CAPS: corpus/SOURCES.md` (no range), `CAPS: corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md`, `CAPS: corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`, `OWNED: SKILL.md:81-314`, `OWNED: result.json`, `OWNED: evidence/round-1-2026-10-15/rubric.json`.

### Shared inputs (read by both counters at rev)

Exactly three mutable surfaces:

1. **`PROVINCE.md`** — C1 writes (remove sasquatch bullet at :149–150; add `## Round-36 additions to Core`); C2 measures the first `## Adjacent` heading-to-last-non-blank range (currently `[97,118]`, asserted in SHONEN box 4) and resolves `PROVINCE.md:{8-14,24,97-118}`.
2. **`corpus/README.md`** — C1 writes (new coverage-map row with the stem; Firmware-row prose at :44); C2 command A parses the whole `## Coverage map` section (lines 11–89, which **includes** the Firmware row) for stem tokens.
3. **`corpus/knowledge/` tree** — C1 adds one file (`2026-10-26-r36-sasquatch-squashfs-recursion.md`); C2 command A counts every `corpus/knowledge/*.md`.

No shared frozen surface: C1's evidence dir/carriers/xpin are unread by C2; C2's SCORECARD/SHONEN/SKILL/result.json are unread by C1. Both counters only read git objects; the only shared environment is the lane repo itself.

## 2. Coupling analysis

### Forward: C1's landing forces on C2 (verified by fixture simulation)

I cloned the lane to scratch (`git clone -q . $S/lane-clone`), committed a **simulated C1 doc landing** on top of `d2e46ef5` (added the entry file, one coverage-map row carrying the stem, removed the PROVINCE frontier bullet, appended the round-36 Core section at the tail — the conventional spot, after `## Round-32 additions to Core` at PROVINCE:353), and ran the **frozen** C2 counter against it. Verbatim results:

- After the simulated C1 landing (fixture commit `45371afa…`):

```json
{"assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [123, 123], "stated": [122, 122]}], "guards_ok": true, "met_target": false, "mismatches": 1, "revision": "45371afa01f460f2a878ea90d434b27dbd3139fe", "unresolved": []}
```

exit **1**. Full receipt (`--json-out`): `observed.adjacent_range = [97,118]`, `observed.craft_range = [81,314]`, `observed.command_a = {"knowledge_files": 123, "mapped": 123, "resolved_rules": 17, "rule_blocks": 17}`, `observed.command_b = [9,9]`, `guards = {missing_units: [], pointers_not_fewer: true, unrepaired: [], base_pointers: 34}`.

  Conclusions: **exactly one** mismatch, O1 only; the Adjacent range, craft range, depth rules, command B, every pointer resolution, and all guards are untouched by C1's edits. The counter's stated-value regex reads the **first** `(\d+)/(\d+) knowledge files mapped` in the row, so the re-statement must replace the leading `122/122`, not merely append a newer figure (the sibling scribe `R36ScribeReadme.md` independently flags the same regex behavior).

- After a **simulated C2 re-state** (SCORECARD row leading figure 122/122 → 123/123; fixture commit `27d47c1b…`), same frozen counter:

```json
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "27d47c1b5355b588f53ea4b5755429d5ac769016", "unresolved": []}
```

exit **0**. The two-commit sequence (C1 docs → C2 re-state) is sufficient and minimal.

### Reverse: C2's landing forces on C1 — none

- `git show --stat d2e46ef5` touches only `SCORECARD.md` (+4/−2 lines: coverage-row restatement, capabilities `receipts-B/` → `.ufo/waves/luna-round-6/receipts-B/`) and `SHONEN.md` (1 line: `ScoutSkillPlacement.md` → `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`). C1 reads neither file.
- Re-ran the frozen C1 counter at the fixture final tip (C1 docs + simulated C2 re-state): `carriers_matched = 4`, `carriers_unchanged = true`, doc bindings all true except `sourced` (my fixture used a placeholder `source: S1nn` with no real SOURCES row — the real landing supplies it). I.e. the C2 re-state commit changes nothing C1 measures; **C1 may be measured at its own doc commit or at the final tip with identical results**, provided no third party edits PROVINCE/README/knowledge in between.
- The future C2 re-state is likewise SCORECARD-only by construction (the O1 check reads one SCORECARD cell; nothing else in C2's units needs C1-triggered text).

### Second-order surfaces checked

- **SOURCES.md appends** (C1's registry row; the r36 assimilation `merge/kaidoku/` theme): C2 never reads `corpus/SOURCES.md`; the Capabilities pointer to it is range-free (existence only), so appends are invisible to C2. C1's `sourced` binding needs its row's opened date = `2026-10-26` and used-by listing the entry — an assimilation collision/rename of that S-id would break C1, not C2 (the assimilation `staged-ids`/`reg-ids` collision guard is the right fence; observation only).
- **r34b hygiene entries** (routed defect D-3, `2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop`, named in `w1-dispatch.json`): each added `corpus/knowledge/*.md` moves C2's denominator; if a matching coverage-map row lands, the numerator moves too. The SCORECARD re-state must equal the **final** tree, so the re-state commit must follow all such landings. (The README `## Knowledge` table row for r34b is parity hygiene, not counter-visible.)
- **Kill rules / controls**: all seven frozen controls exit 1 (`.ufo/waves/round-36/controls/*.out`, verbatim tails below); both kill rules are already satisfied pre-data, so neither landing can trip the other's kill rule. The C2 controls' base is `cab59f22` in all cases; the C1 controls pin freeze `790561d4`.

## 3. Proposed landing order and measurement revisions (no frozen rule changes)

1. **(landed) `d2e46ef5`** — C2 repairs; **first C2 measurement pinned here**, before C1's entry. Already green: `.ufo/waves/round-36/c2/after-at-d2e46ef5.json` (`mismatches: 0, guards_ok: true, met_target: true`); independently reproduced by this seat at HEAD (§4).
2. **C1 doc commit** — entry (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`), SOURCES row, PROVINCE `## Round-36 additions to Core` row, README coverage-map row (+ Firmware-row supersession). **C1 measured at this commit** (`--rev <doc commit> --freeze 790561d4 --pkg65 <rea-agents 6.5.0>`); after-receipts already frozen at `3310d8fa`.
   - *Placement constraint for the builder:* PROVINCE edits confined to lines > 120 — do not insert before or inside the `## Adjacent` span (heading :97, asserted range 97–118) and do not shift lines :8–14/:24. Removing the frontier bullet (:149–150) and tail-appending the new section (the convention since `## Round-31/32 additions to Core`) satisfies this. A violation would flip C2's R3 (`SHONEN box4 Adjacent range`) and force a SHONEN re-assertion — an avoidable second edit on C2's surface.
   - *README constraint:* the Firmware row (:44) sits **inside** the `## Coverage map` section (11–89); any prose edit there must preserve every existing stem token (`2026-10-13-r2-firmware-probe`, `-r4u-01-firmware-deep`, `-r4u-03-unblob-extract`) or `mapped` drops. (The sibling scribe's draft B supersedes by date without touching the row — compliant.)
3. **All other `corpus/knowledge/` landings of the round** (r34b D-3 trio; any assimilation-produced knowledge entries), each ideally with a one-row coverage-map append so the count stays N/N.
4. **C2 re-state commit — last knowledge-tree-touching commit of the round.** SCORECARD `owned:coverage` row's leading figure → the exact observed pair (123/123 if only C1's entry lands with a map row; N/M if r34b entries land without map rows — the counter accepts any stated==observed pair, but N<M is a visible quality regression, so map rows are preferred). **Second C2 measurement at this final tip** (`--rev <tip> --base cab59f22`), expect exit 0.
5. Optional cross-check: re-run C1 at the final tip; expect byte-identical verdict to step 2 (proved equivalent on the fixture). Not required — C1's measurement rev may stay its doc commit.

This is exactly the schedule the frozen plan text states ("measured at its own landing commit before C1's entry lands, then again at the final tip"); the revisions above only pin *which* commit is C2's landing commit (`d2e46ef5`) and add line-level placement guardrails. **No counter, predicate, carrier, oracle, or kill-rule change is proposed or needed.**

## 4. Verification log (all exercised by this seat)

Lane state at run time: HEAD `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` on top of `3310d8fa` → `6a870b92` → `790561d4` → base `cab59f22`; `git status --porcelain` shows only untracked `.ufo/waves/round-36/` wave artifacts.

- C2 at HEAD (first measurement revision):
  `python3 -I -B tools/round-36/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD --base cab59f221fe19726b5692bfa4d9a9679e96b8a73` →
  `{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "HEAD", "unresolved": []}` exit **0**. Matches committed receipt `.ufo/waves/round-36/c2/after-at-d2e46ef5.json` (`guards.base_pointers: 34`, `base_unresolved: [receipts-B/, ScoutSkillPlacement.md]`, both now repaired; `unrepaired: []`).
- C1 at HEAD (docs not yet landed):
  `HYAKU_SCRATCH=$S python3 -I -B tools/round-36/c1-counter.py --root <lane> --rev HEAD --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` →
  `{"bindings": {"coverage_map_row": false, "entry_present": false, "entry_source_ids": [], "opened_source_rows": [], "province_core_row": false, "province_core_section": false, "sourced": false}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": false, "revision": "HEAD"}` exit **1** (carrier leg fully green; only the unlanded doc bindings are red). Matches interim receipt `.ufo/waves/round-36/interim/c1-after-receipts-only.json` at `3310d8fa`.
- Fixture (clone under scratch, since removed): simulated C1 doc landing → frozen C2 counter exit 1 with the single O1 mismatch `[123,123]` vs `[122,122]`, `adjacent_range [97,118]` unchanged; + simulated SCORECARD re-state → exit 0; frozen C1 counter at that tip still `carriers_matched 4` with doc bindings true. Exact commands: `git clone -q . $S/lane-clone`, three `git -C $S/lane-clone commit` fixture commits (`45371afa…`, `27d47c1b…`), then the two frozen counter commands with `--root $S/lane-clone` (full argv and outputs reproduced in §2; scratch deleted after).
- Read-set inventory: `git show 790561d4:tools/round-36/c1-counter.py` and `:c2-counter.py` (paths enumerated in §1; counters byte-identical at freeze and worktree per seat `R36ExecRecountC2`'s sha256 check).
- `d2e46ef5` diff scope: `git show --stat d2e46ef5` → `SCORECARD.md | 4 ++--`, `SHONEN.md | 2 +-` only.
- Controls (kill rules already satisfied, verbatim from `.ufo/waves/round-36/controls/*.out`): `CTL-C1-0 exit=1`, `CTL-C1-1 exit=1`, `CTL-C1-2 exit=1`, `ctl-c2-0-do-nothing exit=1`, `ctl-c2-1-junk-count exit=1`, `ctl-c2-2-delete-bad-pointers exit=1`, `ctl-c2-3-substitute-other-document exit=1`.
- Census: `.ufo/waves/round-36/census-start.txt` exit 0, 9 W04 duplicate-url rows (S033, S047, S054, S062, S069, S083, S090, S092, S102), registry `ok`.
- No frozen predicate/counter/carrier/oracle was modified; no lane file other than this report was written.

## 5. Risks and open flags

1. **Adjacent-span drift (avoidable):** if C1's PROVINCE builder inserts the round-36 Core section before `## Adjacent` (:97) or inside it, R3 flips and C2 needs a SHONEN box-4 re-assertion — a second C1-forced edit on C2's surface. Guard: tail-append only (matches every prior round section).
2. **Re-state ordering:** any `corpus/knowledge/` landing (r34b trio, assimilation entries) or coverage-map edit after the C2 re-state re-breaks O1. Guard: re-state commit is the last tree-touching commit; final-tip measurement follows it.
3. **Stem loss in the Firmware row:** its edit is inside the parsed coverage-map section; dropping a stem token lowers `mapped` and can never be honestly re-stated as N/N. Guard: prose-only change or date-superscript outside the section.
4. **Mapped<files quality regression:** knowledge entries landed without coverage-map rows (r34b is currently unmapped per the sibling scribe) make the honest restatement N<M; the frozen counter still passes (stated==observed), but the row's "index integrity" claim weakens. Flagged for L1, not repaired by this seat.
5. **C1 measurement rev freedom is conditional:** "C1 at doc commit == C1 at final tip" holds only if no third party edits PROVINCE/README/knowledge between them; the order in §3 makes that true by construction.
6. Limit of this seat: fixture simulation proves the mechanism on the frozen counters but is not the production landing; the production re-statement value must be recomputed from the real final tree (one `c2-counter.py --rev <tip>` run).

## Bounds and tooling compliance

- Wrote only `.ufo/waves/round-36/w1/R36ConnSeparability.md`. No writes elsewhere in the lane, the fleet repo, sibling lanes, or `/home/vgpnk/Projects/shokuknow` (not touched, no campaign tool).
- No VCS mutation; read-only git only. Fixture clone lived in `/fast/scratch/hyaku/kaidoku-r36/R36ConnSeparability` and was removed after use (`TMPDIR` pointed there during runs).
- REA was not invoked by this seat (counter's internal `xpin` node call is part of the frozen counter, using the pinned 6.5.0 package already installed at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`).
- **Tooling record (operator directive 2026-10-19):** no installs/upgrades performed; nothing to record — all tools used (`git`, `python3 3.x`, `node` via the frozen xpin call) were already present. `sasquatch` was not installed/removed/touched by this seat.
- Coordination: scope overlaps sibling `R36ScribeReadme.md` (README count coupling — cited, consistent) and `R36ConnSiblingOverlap.md` (cross-lane surface — different question, no conflict). No peer messages were required for a read-only pattern check.
