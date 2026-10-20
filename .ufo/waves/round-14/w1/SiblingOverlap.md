# Sibling Province Scope Overlap & Boundary Synthesis — Round 14

**Lane:** `kaidoku-shokunin`  
**Seat:** `KaidokuR14.SiblingOverlap` (connector)  
**Date:** 2026-10-20  
**Target:** Scan sibling province names under `/home/vgpnk/Projects/shokunin` for scope overlap of Go parser diagnosis (C1) and local REA source-quote gate (C2).  
**Declared Round Axes:** `coverage`, `calibration`

---

## 1. Fleet Province Inventory & Adjacent Domain Mapping

A full scan of sibling provinces defined in `/home/vgpnk/Projects/shokunin/MANIFEST.json`, `shokunin.conf`, and on-disk directories identified 21 active `*-shokunin` child repositories plus 2 fleet-root provinces (`protocol` and `aggregator`):

| Province | Domain / Declared Scope | Boundary Relation to `kaidoku` C1 / C2 | Overlap Finding |
|---|---|---|---|
| `revenger-shokunin` | Reverse engineering of shipped artifacts under evidence-ledger discipline | Adjacent RE lane. Seeded from PE32+ multi-icon state ledgers (`verify_named_multi_icon_states.py`). Refuses harness auditing and DRM. | **Zero Go overlap.** Contains 0 mentions of `golang`, `GoVerRange`, `pclntab`, or `GoRttiMapper`. `kaidoku` uniquely owns Linux ELF via Ghidra 12.1.4 provider on this host. |
| `chousa-shokunin` | Deep-research method (調査) — source hierarchy, citation chaining, claim verification | Owns general source research method and fleet claim verification via `tools/research-gate.sh` (`verify-claims`, `verify-chain`). Refuses target reverse engineering. | **Distinct boundary.** `chousa` owns general citation-chaining craft. `kaidoku`'s C2 local quote gate is bounded to local captured excerpts for REA evidence without absorbing `chousa`'s method. |
| `tameshi-shokunin` | Verification-fixture craft — hermetic suites, fail-closed arms, verdict-line discipline | Governs reusable verification method. Explicitly refuses product domains: *"every lane's gate remains its own"* (`PROVINCE.md:13`). | **Zero gate conflict.** Confirms `kaidoku` must own its local `quote-fidelity.py` gate. Provides pattern (isolated `--selftest`, 0/1/2 exit codes) without shared code. |
| `tsukuroi-shokunin` | Host operability & system repair — OS packages, systemd, boot health | Monitors pacman package health; refuses binary RE of packages/drivers (defers to `kaidoku`/`revenger` per `PROVINCE.md:27,80`). | **Zero overlap.** Tracks OS package state, not Go binary moduledata or Ghidra parser RTTI internals. |
| `kotoba-shokunin` | Prompt & skill craft — `SKILL.md` frontmatter, trigger fidelity, anatomy | Governs general skill craft; explicitly notes no overlap with RE (`PROVINCE.md:32`). | **Zero overlap.** `kaidoku` owns its domain Go decision table addendum; `kotoba` owns meta-skill craft. |
| `protocol` / `aggregator` | Fleet-meta, gate integrity, cross-lane quality, sources census | Governs `scripts/sources-census.sh validate` (checks 11-column header, valid tiers/statuses, disk existence of `used-by`). | **Complementary gap.** Fleet census checks table formatting but cannot check quote contiguity or section matching. C2 fills this exact local gap. |
| `kumitate-shokunin` | Orchestration & tooling — OMP task/hub, ufo-fsd scripts & runtime | Governs runtime/dispatch scripts (`ufo-fsd-alpha/scripts/`); refuses domain RE or research method. | **Zero overlap.** |
| `kasegi-shokunin` | Bounty & security research | Scopes bounty rules and submission packages; refuses binary RE or local host gates. | **Zero overlap.** |
| `kengaku-shokunin` | LLM/model evaluation & research | Benchmark batteries, route telemetry; routes RE and host state outward. | **Zero overlap.** |
| `kake-shokunin` | Web properties & publishing | Web fronts, Pages deploys, crawl scope; refuses local binary RE. | **Zero overlap.** |
| `kagi-shokunin` | Secrets & vault ops | Credential custody, 1Password/Vault rotation; refuses target analysis. | **Zero overlap.** |
| `kama-shokunin` | Local model serving & endpoint health | Endpoint drift (`:8080`, `:34113`); refuses model eval or binary RE. | **Zero overlap.** |
| `lore-shokunin` | Fictional-world records & bible consistency | Lore canon consistency; refuses technical binary RE. | **Zero overlap.** |
| `kotodama-shokunin` | Linguistic-cultural worldbuilding | Conlang and mythic systems; hands off to lore. | **Zero overlap.** |
| `mado-shokunin` | Desktop & compositor craft | Hyprland/waybar/walker configurations. | **Zero overlap.** |
| `mori-shokunin` | Fleet & host observability | Watchdog liveness, wave settlement, memory/journal pressure. | **Zero overlap.** |
| `souji-shokunin` | Repo & workspace hygiene | Artifact cleanup, stale receipts; refuses modifying live lane products. | **Zero overlap.** |
| `tabi-shokunin` | Browser & web-interaction craft | CDP session discipline; refuses reverse engineering as forensics (`PROVINCE.md:15`). | **Zero overlap.** |
| `audio-shokunin` | Game audio production | Headless audio analysis (ffmpeg, sox). | **Zero overlap.** |
| `game-dev-2d-shokunin` | 2D game production | Godot 4.7.2 2D headless fixtures. | **Zero overlap.** |
| `game-dev-3d-shokunin` | 3D game production | Headless 3D fixtures; uses REA strictly for 3D static format inspection. | **Zero overlap.** |

---

## 2. Scope Overlap Analysis

### A. Go Parser Diagnosis (Claim C1)
- **Domain Ownership:** `kaidoku-shokunin` is the sole owner of the on-host Ghidra 12.1.4 provider (`GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC`) and historical ELF analysis (`op` 2.34.1 vs 2.40.0).
- **Sibling Survey:** A text sweep across all 21 sibling repositories for `GoRttiMapper`, `GoApiSnapshot`, `GoVerRange`, `pclntab`, and `GoReSym` returned **zero hits outside `kaidoku-shokunin`**. Neither `revenger-shokunin` nor `tsukuroi-shokunin` claims or touches Go binary recovery mechanisms.
- **Boundaries to Preserve:**
  1. *Versus `revenger-shokunin`:* C1 must not claim a general binary forensics ledger for Go binaries; it is strictly a static source diagnosis of why installed Ghidra 12.1.4 fails on Go 1.26 binaries.
  2. *Versus `tsukuroi-shokunin`:* Must not misattribute Go 1.26 failure to a host package or toolchain defect; it is an internal parser version-gate limit.
  3. *Versus prior mistake (r4-10):* Must not infer that Go 1.26 mutated the moduledata/pclntab binary layout; S003 source proves failure occurs at `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` and missing bootstrap snapshot `go1.26.0.json`.

### B. Local REA Source-Quote Gate (Claim C2)
- **Domain Ownership:** `kaidoku-shokunin` owns its own source registry (`corpus/SOURCES.md`) and the local excerpts cited by its lessons and knowledge entries.
- **Sibling Survey:**
  - `chousa-shokunin` operates `tools/research-gate.sh` (5,290 lines) for multi-hop citation chains (`verify-chain`) and general verbatim spans (`verify-claims`) across research corpora.
  - `tameshi-shokunin` owns verification-fixture patterns but explicitly rejects owning product-level gates for other lanes.
  - `protocol` operates `scripts/sources-census.sh validate`, which enforces the 11-column tabular structure, tier enums, and on-disk paths, but cannot detect quotation splices or heading mismatches.
- **Boundaries to Preserve:**
  1. *Versus `chousa-shokunin`:* `quote-fidelity.py` must remain strictly local to `kaidoku-shokunin`, evaluating frozen, locally captured Markdown excerpts (`fixtures/`) against exact headings. It must NOT attempt to become a general web scraper or claim fleet-wide citation-chain authority.
  2. *Versus `protocol` / `sources-census.sh`:* `quote-fidelity.py` must not mutate or replace `sources-census.sh validate`. It acts as an internal quality filter catching S017/S018-class errors before non-author review.

---

## 3. Connector Synthesis: One Bounded Non-Obvious Move

### The Proposed Move
**Hermetic Local Excerpt Fidelity Gate Partitioned from Fleet Research Method and Target Runtime Claims**

Synthesize the round's twin deliverables (C1 Go version diagnosis and C2 quote-location fidelity gate) by establishing an explicit **contractual separation of surfaces**:
1. **Scope Restriction of C2 to Captured Markdown Excerpts:**
   Formally limit `quote-fidelity.py` to local UTF-8 Markdown fixtures under `.ufo/waves/round-14/fixtures/` with exact `#` section headings and contiguous $\le 25$-word whitespace sequences. Explicitly document that non-Markdown sources (such as Java source inside S003 `Base-src.zip`, Git commits like S004, or compiled binaries) are outside C2's gate scope and must not be fed to `--manifest`.
2. **Strict Attribution Boundary for C1:**
   Formally bound C1's knowledge entry (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`) to **installed parser source analysis** (Ghidra 12.1.4 `GoRttiMapper.java` line 79 range `"1.15-1.25"` and `GoApiSnapshot.java` returning `EMPTY`), explicitly refuting the historical r4-10 inference of moduledata/pclntab layout changes without asserting active Go 1.26 REA execution capability.

### Affected Axes
- **`calibration` (Improved):** Prevents gate overclaiming. Bounding `quote-fidelity.py` to captured excerpts avoids failure on heterogeneous sources (e.g. zip archives, binary carriers) while precisely detecting the historical red-before S017 splice and S018 heading mislocation.
- **`coverage` (Improved):** Expands knowledge on uncovered ground (diagnosing installed Ghidra 12.1.4 version constraints via S003–S006) without overclaiming target execution or treading on sibling provinces.
- **Harm to Other Axes:** None. Preserves `operability`, `freshness`, `depth`, and `fleet-meta`.

### Second-Order Effects & Explicit Contradictions
- *Contradiction Identified:* S003 is a zip archive (`Base-src.zip`) containing Java source (`GoRttiMapper.java`), while S004 is a commit diff. C2's candidate gate requires Markdown files with heading lines beginning with `#`. If C2 were claimed as a "whole-registry verifier" for all `SOURCES.md` rows, it would fail or require unmaintainable ad-hoc parsing of non-Markdown files.
- *Resolution:* C2's observable is strictly defined in `claims.json` as: *"limits: local captured source excerpts only; no whole-registry or semantic truth assertion"*. Bounding C2 to local Markdown fixture excerpts resolves the contradiction completely.
- *Sibling Harmony:* `chousa-shokunin` retains full authority over general research citation method; `tameshi-shokunin` retains verification-fixture craft; `revenger-shokunin` retains binary forensic ledgers; `kaidoku-shokunin` owns its host-specific Ghidra provider analysis and local citation gate.

### Risks & Mitigations
- **Risk:** C1 quotes from S005/S006 could be inadvertently evaluated by C2 without matching Markdown fixture excerpts.
  - *Mitigation:* Ensure C2 manifest fixtures are owned exclusively by `QuoteSourceFixtures` for the frozen test set (S017/S018 red/green pairs).
- **Risk:** Future rounds might treat S003 version-gate analysis as proof that Go 1.26 binaries can now be parsed.
  - *Mitigation:* Explicitly label upstream GP-6528 (S004) as unreleased/master-only and installed Ghidra 12.1.4 as strictly gated at `1.15-1.25`.

---

## 4. Verification Recipe for Main Agent

The following verification steps can be executed by the main integrator at round completion:

1. **Verify Sibling Independence (No Out-of-Scope Writes):**
   ```sh
   git status --short
   ```
   *Expected:* No modified files in sibling repositories (`revenger-shokunin`, `chousa-shokunin`, etc.) or fleet root (`MANIFEST.json`, `shokunin.conf`).
2. **Verify Census & Registry Structure:**
   ```sh
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
   ```
   *Expected:* Exit 0 (`kaidoku ok .../corpus/SOURCES.md`).
3. **Verify C2 Gate Selftest Isolation:**
   ```sh
   python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --selftest
   ```
   *Expected:* Exit 0 with deterministic case passes.

---

## 5. Sources Opened

Every source below was opened on **2026-10-20**. Excerpts are contiguous and $\le 25$ words:

1. **`chousa-shokunin/PROVINCE.md`**  
   - *Location:* Lines 5–7, `## Owns`  
   - *Quote:* “question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy;”  
   - *Limitations:* Describes chousa's research domain; does not specify REA host provider boundaries.

2. **`tameshi-shokunin/PROVINCE.md`**  
   - *Location:* Lines 13–15, `## Refuses`  
   - *Quote:* “Refuses: product domains — every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general).”  
   - *Limitations:* Defines reusable verification craft, refusing product-specific gate code.

3. **`revenger-shokunin/PROVINCE.md`**  
   - *Location:* Lines 3–7, `## Owns`  
   - *Quote:* “Owns: reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence — using the REA skill and its toolset,”  
   - *Limitations:* Reflects revenger's general RE scope; does not govern on-host Ghidra 12.1.4 provider state.

4. **`tsukuroi-shokunin/PROVINCE.md`**  
   - *Location:* Lines 27–28, `## Core` > `Refuses`  
   - *Quote:* “Refuses: endpoint/model serving health (→ kama), secrets (→ kagi), binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks state and health, not internals).”  
   - *Limitations:* Confirms driver/binary RE is out of tsukuroi's scope and deferred to kaidoku/revenger.

5. **`kaidoku-shokunin/.ufo/waves/round-14/claims.json`**  
   - *Location:* Lines 20–25, Claim C2  
   - *Quote:* “observable: quote-location fidelity gate plus grounded QUALITY criterion rejecting S017 splice and S018 mislocation while admitting corrected contiguous located quotes”  
   - *Limitations:* Bounded round 14 claim definition; limits truth claims to local captured excerpts.

---

## 6. Tooling Directive Record
- **Tools installed or updated:** None. Standard host Python 3 (`/usr/bin/python3`) and core utilities were used in read-only inspection mode.
