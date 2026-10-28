# R44RevFreeze — completeness review of `plans/round-44-claims.md ## Frozen paths`

Seat R44RevFreeze, base `c29360e3` (HEAD at review `fc5eb54a`, the draft). Read-only. No tool/rubric/counter exists yet under
`tools/round-44/` (`ls` exit 2), so "what the predicate reads" is derived from the draft predicate text plus the round-42 counter it ports
(`tools/round-42/c1-counter.py` `FROZEN_PATHS`, `CARRIERS/GAPRULE/PRIOR_PINS/REA_PKG/XPIN`, `c1-extra.py`, `c1-run.sh`) and the round-43 plan's
`## Frozen paths and landing paths` precedent.
Probe receipt: `R44RevFreeze/probe-receipt.json` (exit 0, stdout sha256 `5de3ad7a…8b56`, 0.065 s; script `R44RevFreeze/probe.py`, output
`probe-stdout.json`). All other statements below are from `read`/`grep` of committed bytes, not scores.

## Verdict: the list is NOT complete and contains four self-contradictions. Do not freeze it as drafted.

### Blockers (the drafted freeze makes a claim unverifiable or unreachable)

**B1. `SCORECARD.md`, `SHONEN.md`, `corpus/README.md` are byte-frozen, but the round cannot close without editing them, and the "append" escape is contradictory.**
The freeze-integrity rule demands each frozen blob at FREEZE equals the blob at REV. Appending a line changes the blob, so "frozen blobs stay equal
… repair lands as appended dated notes" (`C2 landing mechanics`) is impossible; the fallback ("relax `frozen_path_changed` for rubric-named paths, diff
bound to the rubric's expected bytes") moves the freeze mid-round — exactly the loosening door CTL-C2-3 claims to close. Precedent: every closure edits
all three (probe: last commits to SCORECARD/SHONEN/README are all `round-43: … close evidence/record lesson`); the round-43 plan froze only
`SOURCES.md` and `SKILL.md` whole, never SCORECARD/SHONEN/README.
Fix: do NOT freeze these three as files. Pin the *checked statement*, not the file: each rubric entry carries `{file, base_blob_sha256 at c29360e3,
quoted_text, line_at_base}`; the counter proves the quote against `git show c29360e3:<file>` (immutable by construction) and evaluates the
repair at REV (statement re-derives true, or a row-identity-checked appended `correction:` line exists). The rubric file + counter (hash-bound) are
the frozen artifacts. Also edit the draft's `## Frozen paths` / `C2 landing mechanics` paragraphs accordingly (this plan file is itself frozen, so the
text must be right before the freeze).

**B2. `corpus/README.md` frozen contradicts R44-C1's `coverage_map_row` binding.** The map row maps the entry stem and the entry is created after the
data run, so the row lands post-freeze. Pre-committing the row would make command A report `dangling [\"…r44-…\"]` at the freeze and plant a seeded
C2 (f)-category mismatch. README.md must be unfrozen for C1 (the C2 rubric then reads the count at REV, as the draft's Separability paragraph
already intends — that paragraph contradicts the frozen list).

**B3. `corpus/SOURCES.md` whole-frozen is only coherent if S138/S139 are in the freeze commit, `used-by` already naming the final entry stem.**
Round-43 did exactly that (freeze commit `eadcbfa5` added S135–S137; counter froze SOURCES whole). The draft instead says S138/S139 are
`opened this round`, and the C1 `sourced` binding needs the entry in `used-by`; the entry does not exist until after data. Either (a) pre-land S138+S139
with the final entry path/stem in `used-by` and fix the stem now (see B5), or (b) unfreeze SOURCES.md and bind `sourced_new` (c1-extra.py shape:
row absent at BASE, present at REV, entry in used-by). Pick one; the draft says both. Also note `tools/round-42/c1-extra.py` `sourced_new` requires the
S-id absent at `--base` — with (a) the base must be `c29360e3`, not the freeze.

**B4. SHONEN/SCORECARD line pointers into files C1 edits will drift, and `PROVINCE.md` is not (and cannot be) frozen.** SHONEN cites
`PROVINCE.md:97-125,157,378-384,386-394` and SCORECARD carries 43 line-qualified pointers into `corpus/README.md`/`corpus/SOURCES.md`/`PROVINCE.md`
(probe `scorecard_line_pointers_…=43`). C1 inserts a README coverage-map row at lines 11–104 (shifts every later README line, e.g. the
`corpus/README.md:126-127` pointer) and appends to PROVINCE/SOURCES. A rubric check that re-resolves a bare `file:line` at REV will report a
*self-inflicted* mismatch the moment C1 lands. Fix: rubric entries for pointers into these three files are checked at the pointer's own revision
qualifier (or at BASE), or by content-in-range ("quoted text found within ±N lines at REV"); C1's PROVINCE edit is constrained to append after the last
line (`## Round-42 additions to Core` is last, line 410+); add a counter binding "PROVINCE.md bytes `1..400` at REV equal BASE" (prefix-preserved) so
the SHONEN pointers stay valid. Without it C1 and C2 are not separable (draft Separability claim is false for README/PROVINCE).

**B5. The knowledge-entry stem is a moving name.** Draft says `corpus/knowledge/2026-10-28-r44-*`. The round-42 counter hard-codes `ENTRY`/`STEM`/`OPENED`
constants. A wildcard in a frozen counter is an unfrozen input. Fix the exact stem (and `OPENED='2026-10-28'`, S-ids S138/S139) in
`c1-counter.py` before freeze.

### Missing from the frozen list (predicate reads them; moving input ⇒ unverifiable claim)

| path | frozen? | needed? | issue |
|---|---|---|---|
| `tools/round-27/xpin-attribute.mjs` | NO | YES | R42 counter `XPIN`: evidence-id recompute tool, run with node at score time. Frozen list omits it; ports "vendor, not import" (round-43 note) — either vendor into `tools/round-44/` (then covered) or list it. |
| `tools/round-44/rea-pkg.json` (R42: `tools/round-42/rea-pkg.json`) | covered by `tools/round-44/*` only if re-minted | YES | `--pkg65` is a mutable npm-cache dir; counter must recompute `package.json`/`package-lock.json` digests (H4). Verified now: package.json `a5003023…0a6c`, lock `d42d56f0…6ca` match the r42 file at `~/.npm/_npx/ad9a3fdbcad992c6`. Mint one for r44 and freeze. |
| `tools/round-44/prior-pins.json` | covered by glob but content unspecified | YES | `tools/round-42/prior-pins.json` holds rounds 38–41 ONLY (probe `prior_pins_rounds [38,39,40,41]`). Round-42 C1 pins (4) and round-43 C1 held-out carrier pins are absent; the freshness binding as ported would not reject a relabelled round-42/43 receipt. Re-mint through round 43. |
| `tools/round-44/gap-rule.json`, per-carrier `oracle.tsv`/`nonregular.tsv`, `fetch`-free carrier table | not named | YES | Draft names `carriers.json`/`c1-run.sh`/`c2-rubric.json` only. The gap rule (R42: `.ufo/waves/round-42/c1/gap-rule.json`) and the oracle member lists (`unsquashfs -lls` census + member digests) are predicate inputs; keep them outside `corpus/evidence/round-44/c1/` (receipts dir, first-added post-freeze) e.g. `corpus/evidence/round-44/oracle/`, and say whether `tools/round-44/*` is recursive (selftest dirs). |
| `tools/round-44/c1-extra.py` equivalent, `unblob-logtee.sh` | not named | YES if ported | R42 `FROZEN_PATHS` lists both; draft says the counter is a port of c1-counter only. Decide whether the `oracle_rederived`/`sourced_new` bindings (c1-extra) survive; if yes, port + freeze. |
| external binaries: `/usr/bin/unsquashfs` (sha256 now `461e1fd9…77c`), `~/.local/bin/sasquatch` (`ad02d27a…4754`), `~/.local/share/uv/tools/unblob/bin/unblob` (`0ce7b624…1d09`), `node` (fnm v24.21.0 path in `FIXED_PATH`), `file` | NO (cannot be git-frozen) | YES | R42 pinned sasquatch+unblob digests in `carriers.json.toolchain` and recorded them in `extract-env.json`; it never pinned `unsquashfs` (the oracle). Round 44's oracle IS `unsquashfs`, so add `toolchain.unsquashfs {path, sha256, version 4.7.5}` to the frozen `carriers.json`, and bind it at score time. The superblock "verified against `file` output" must be frozen *text* in `carriers.json`, not a live `file` call (libmagic db is a moving input). |
| `corpus/evidence/round-44/oracle/` (S138 `__output__` trees) | yes (draft) | YES | OK as drafted; add that it is committed pre-freeze and distinct from the receipts dir `corpus/evidence/round-44/c1/` (`first-added after freeze`, must NOT be frozen). |
| `.ufo/waves/round-44/controls/**` (CTL-C1-0..3, CTL-C2-0..3 tables and their *development inputs*), dry-run receipts, the sasquatch-stripped receipt for CTL-C1-3 and its `extract-env.json` | NO | YES | Freeze-integrity rule says controls + dev inputs are "committed in the freeze", but `## Frozen paths` lists none of them. CTL-C1-3 needs a real REA run with sasquatch stripped, produced PRE-freeze (never `c1-run.sh`). Add the directory, with the dry-run receipts showing every binding evaluated. |
| `corpus/evidence/round-43/c1/heldout/manifest.json` + `H41/*` | NO | YES | See D1: v2-le bytes were a round-43 C1 carrier. |
| `corpus/evidence/round-42/c2/dev/` | NO | YES (if used) | Draft freezes `heldout/` but not `dev/`. Round-43 froze both. Dev has no pin matches (probe `…c2/dev {}`), so only freeze it if a CTL replays it; otherwise note "not read". |
| `corpus/evidence/round-42/c1/*/after.json` (`OW-A8092`, `OW-X86FS`, `DW-FONERA`, `DW-MEGA`) | NO | YES | CTL-C1-1 is "round-42 C1 receipts copied to the round-44 evidence paths". The draft froze `…/c2/heldout/` (v1/v2 receipts, not v3). The v3 receipts the control actually replays live at `corpus/evidence/round-42/c1/<id>/{after,extract-env,run}.json`; they are not in the list. |
| `.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json` | NO | YES if cited | Draft lists only the round-43 scores dir. C2 category (e) reads every SCORECARD round table's cited receipt: enumerate each receipt path + sha256 in the rubric `inputs[]` instead of a `scores/*.json` glob (a glob admits files added later). |
| historical record files read by C2 categories (c)/(d)/(e): `LOG.md`, `plans/round-4{1,2,3}-claims.md`, `corpus/lessons/round-4{1,2,3}*.md`, `corpus/QUALITY.md`, `PROVINCE.md` (BASE statements) | NO | YES | `LOG.md` is appended every round (last: `round-43: append npx cache provenance correction`). Read them ONLY via `git show c29360e3:<path>` (BASE-pinned in the rubric) — not frozen as files, not read at the worktree. Anything the rubric reads at REV from these must be a named, append-only-prefix check. |
| `corpus/knowledge/*.md` cited by `SKILL.md` rule blocks (`file.md:N-M` ranges; command A resolves `1<=N<=M<=len`) | NO | YES | Depth-count check (b) depends on line counts of ≥20 cited knowledge files. They are append-only by discipline but not enforced; add a prefix-preserved check (REV blob starts with BASE blob) or list them. Knowledge file count at BASE is **138** (probe), not 133/137 — pin the rubric to command A at BASE, never a quoted integer. |

### Frozen in the draft — verdicts

| path | frozen? | needed? | issue |
|---|---|---|---|
| `plans/round-44-claims.md` | yes | yes | `## Changes from the draft` is empty and the B1–B4 text must be corrected before freeze (frozen file ⇒ no later edit). |
| `tools/round-44/*` (all tools, `carriers.json`, `c1-run.sh`, `c2-rubric.json`) | yes | yes | Needs "recursive" stated; must also contain `gap-rule.json`, `prior-pins.json`, `rea-pkg.json`, ported `c1-extra`, `c2-counter.py`, selftest fixtures. `c1-run.sh` frozen but never run by seats — correct. |
| four carrier `*.bin` under `corpus/evidence/round-42/c2/fixtures/` | yes | yes | Freeze exactly these four; the other 10 fixture files (v2ns, v3*) are not predicate inputs (round-43 froze the whole dir; harmless, not required). Verified: all four sha256 equal `tools/round-42/fixtures.json` pins (v1-be `529e1077…`, v1-le `b45925fa…`, v2-be `79c0f388…`, v2-le `7c62dbe3…`), gzip, `expected_files` 3/3/4/4. |
| `tools/round-42/fixtures.json` | yes | provenance only | Not read by the counter if pins live in `carriers.json`; freezing is harmless and keeps the licence/URL chain. |
| `tools/round-42/c1-counter.py` | yes | NO (for runtime) | Port source only; round-43 note: "No round-43 tool imports a `tools/round-42` module at runtime (ports vendor, not import)." Freezing keeps the port diff auditable — keep, but label "audit only" so no seat later treats it as a runtime input. |
| `corpus/evidence/round-42/c2/heldout/` | yes | partly | The whole dir is not read; the predicate-relevant parts are `manifest.json` and `H41/H43/H44/H45` (D1). Narrow to those (or keep whole; harmless). It is NOT where CTL-C1-1's v3 receipts live (see list above). |
| `corpus/evidence/round-44/oracle/` | yes | yes | OK; see above. |
| `tools/round-39/gen-squashfs.py` | yes | NO unless a synthetic arm exists | Draft says "if a synthetic arm is needed". Freeze only if CTL-C1-2's fabricated arm calls it; the round-43 plan froze it already, so low cost. |
| `.ufo/waves/round-43/l1/scores/*.json` | yes | partly | Glob → enumerate (C2 e). Which of the three files C2 reads is unspecified. |
| `SKILL.md` (whole) | yes | yes | Correct and consistent with round-43 (`eadcbfa5` last touch). Consequence to state: any SKILL status/instrument-row edit the round wants MUST be in the freeze commit. C1 needs none; confirm. |
| `SCORECARD.md`, `SHONEN.md` | yes | NO (as files) | See B1: freezing them forbids the Round-44 section, Capabilities row, SHONEN note. |
| `corpus/README.md` | yes | NO | See B2. |
| `corpus/SOURCES.md` | yes | conditional | See B3. |

### Design findings that affect whether the C1 predicate can discriminate (D = discriminator)

**D1. The four frozen carriers already have committed REA receipts of identical bytes.** Probe: round-42 `c2/heldout` H43=v1-be, H41=v1-le, H44=v2-be,
H45=v2-le carriers all hash to the frozen pins (REA 6.5.0 envelopes in the same dirs); round-43 `c1/heldout/H41` is v2-le again (a round-43 C1 carrier,
so the draft's "never a C1 carrier" is true only for round 42). Consequences: (i) the "Frontier" status is not the absence of an envelope but the absence
of a mapped Core row — the disclosed limit should say so; (ii) a *copy* of a heldout envelope placed at a round-44 path has the correct subject
digest, handler and published files, and a counter-time rerun of the same bytes has the same projection, so CTL-C1-2 ("fabricated from the oracle")
tests the wrong forgery. Add a control CTL-C1-4: pre-freeze real receipts of the same bytes (round-42 H41/43/44/45, round-43 H41) relabelled into the
round-44 receipt paths and first-added after the freeze — the counter must refuse it (e.g. reject any after-receipt whose bytes or
`parameters`/stage identity equal a pre-freeze committed envelope, or require evidence id minted at a `/kaidoku-r44/` provenance segment as the r42
`PROV_SEGMENT='/kaidoku-r42/'` does). Without it, the "first added in a descendant of the freeze" clause is satisfiable by `cp`. The frozen list must then
include those five heldout envelope sets (`corpus/evidence/round-42/c2/heldout/{manifest.json,H41,H43,H44,H45}` and
`corpus/evidence/round-43/c1/heldout/{manifest.json,H41}`) — the first is in the draft only as a whole-dir entry, the second is missing.

**D2. Freshness table stops at round 41** (`prior_pins_rounds [38..41]`, `prior_pins_has_c1_pins_for_v1v2 []`): see missing-list row; re-mint through
round 43, and decide explicitly whether the round-42 C2/round-43 C1 uses of these bytes count as "already scored" (they were calibration/depth
claims, not coverage). State the ruling in the plan.

**D3. Do-nothing control for C2 can only be scored against an enumerated rubric** — fine — but the counter reads `SCORECARD`/`SHONEN`/README at
`--rev <BASE>` for CTL-C2-0 while they are blob-frozen at FREEZE; once B1 is applied (BASE-pinned `git show`), CTL-C2-0 and the REV score use one
mechanism and CTL-C2-3 ("rubric is itself a frozen path") stays true.

## Corrected frozen set (proposal)

Byte-frozen (change ⇒ `frozen_path_changed`, exit 2): `plans/round-44-claims.md`; `tools/round-44/**` (counters, selftests, `carriers.json`
(with `toolchain.{sasquatch,unblob,unsquashfs}` digests and frozen superblock text), `gap-rule.json`, `prior-pins.json` through round 43,
`rea-pkg.json`, `c1-run.sh`, ported `c1-extra.py`, `c2-rubric.json`); `tools/round-27/xpin-attribute.mjs` (if not vendored); the four carriers;
`tools/round-42/fixtures.json`; `tools/round-42/c1-counter.py` (audit-only); `corpus/evidence/round-44/oracle/**`;
`.ufo/waves/round-44/controls/**` (+dry-run receipts, sasquatch-stripped receipt); `corpus/evidence/round-42/c1/**` (CTL-C1-1 inputs);
`corpus/evidence/round-42/c2/heldout/{manifest.json,H41,H43,H44,H45}`; `corpus/evidence/round-43/c1/heldout/{manifest.json,H41}`;
the cited score receipts enumerated by path+sha in the rubric (`.ufo/waves/round-4{2,3}/l1/scores/*.json` as named); `SKILL.md` (whole);
`corpus/SOURCES.md` (whole) **only if** S138/S139 land in the freeze commit with the final `used-by`.

Not frozen (landing paths, BASE-pinned in the rubric instead): `SCORECARD.md`, `SHONEN.md`, `corpus/README.md`, `PROVINCE.md` (append-after-line-410
only, prefix-preserved check), `LOG.md`, `corpus/knowledge/*` (new entry only; existing files prefix-preserved), `corpus/evidence/round-44/c1/**`
(first-added after the freeze).

Open items for the L1 before the freeze commit: B1–B5, D1 control CTL-C1-4, D2 pin re-mint, `unsquashfs` toolchain digest, `## Changes from the
draft` filled.
