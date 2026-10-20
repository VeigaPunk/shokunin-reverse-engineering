# ConnSiblingOverlap — round-18 sibling-overlap scan

Seat: `KaidokuR18.ConnSiblingOverlap` (connector, leaf) · 2026-10-20 · read-only.
Lane rev probed: `9011581d84527ba34c675f9cf912e54d2e72d470` (`refs/heads/main`). `jj 0.45.1-7c41cdeb`.
No sibling file was edited, no sibling gate or tool was executed, no `jj` or git write ran.
**Axes named:** calibration, operability, depth. **Nothing absorbed.**

## 0. Evidence — commands and exits

All commands read-only. `[O]` observed, `[I]` inference.

| command | exit | result |
|---|---|---|
| `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/` | 0 | 21 lanes; every `PROVINCE.md` read in full |
| `grep -rniE 'swiss\|RTTI\|ghidra\|oldmaptype\|maptype' --include=PROVINCE.md .` | masked by `\| head` | only kaidoku `PROVINCE.md` (+ its arc3 scratch copies) `[O]` |
| `grep -rliE 'swiss.?map\|oldmaptype\|golang typeinfo\|go rtti\|maptype' --include='*.md' <20 sibling corpora>` | **1** | **no sibling hit** `[O]` |
| `grep -rliE 'jujutsu\|colocated workspace\|ignore-working-copy\|bookmark set\|branch tip' --include='*.md' <20 sibling corpora>` | **0** | only `mado-shokunin/corpus/lessons/round-14.md` `[O]` |
| `git -C kaidoku-shokunin rev-parse --verify refs/heads/main` | 0 | `9011581d8452…` |
| `git -C kaidoku-shokunin rev-parse --verify HEAD` | 0 | `9011581d8452…` |
| `git -C kaidoku-shokunin symbolic-ref -q HEAD` | **1** | detached `[O]` |
| `git -C kaidoku-shokunin rev-parse --abbrev-ref HEAD` | 0 | prints `HEAD` |
| `git -C kaidoku-shokunin branch --show-current` | 0 | prints nothing |
| `git -C kaidoku-shokunin for-each-ref --points-at HEAD --format='%(refname)' refs/heads` | 0 | `refs/heads/main` |
| `git grep -nE '"HEAD"\|HEAD:\|\{u\}\|abbrev-ref\|show-current\|symbolic-ref\|rev-parse' 9011581 -- .ufo/gates .ufo/rounds .ufo/waves/round-14 .ufo/waves/round-15 .ufo/waves/round-16 .ufo/waves/round-17 .ufo/waves/round-18` | 0 | site list in §4 |
| `git cat-file -e 9011581:.ufo/waves/round-17/verify.py` | 0 | tracked at baseline (so it is in the lint's scan set) |
| `test -d .jj` × {kaidoku,tameshi,mado} | 0 | all three present |
| `wc -l scripts/hyaku/{jj-lane.sh,jj-lane.sh.new,jj-lane-selftest.sh,jj-lane-selftest.sh.new}` | 0 | 268 / 645 / 294 / 634 |

Tool note for later seats: the `grep` tool's `path` does **not** expand `*-shokunin/corpus` (returns “No matches found”); explicit `;`-separated paths are required. The shell sweeps above use explicit paths.

## 1. Go RTTI / Swiss map / Ghidra-Go — uncontested ground

**Observation.** No sibling corpus or `PROVINCE.md` holds Go type-layout ground. `revenger` is the only sibling whose declared domain is artifact RE, and its Ghidra content is *provider availability*, not Go semantics: `revenger-shokunin/corpus/knowledge/seed.md:63-66` (`F08 ghidra absent`), `…/2026-10-12-rea-readiness-checklist.md:16,39`. Other Ghidra mentions are config/availability only: `kumitate-shokunin/corpus/knowledge/kimi-config-plane.md:257-258` (MCP env), `audio-shokunin/corpus/live/r74-simplifier/working-notes.md:6-7` (REA is Ghidra-session-bound), `game-dev-3d-shokunin/corpus/knowledge/rea.md:7-9,50-52,67-72` (Ghidra presence probe).

Go RTTI prose exists only in kaidoku's lane corpus (6 files) and kaidoku-authored fleet reports: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/kaidoku.md:32` (aether Swiss-map mechanism), `.ufo/waves/kaika-w1/kaidoku-art.md:208` (`GoRttiMapper.java` `SUPPORTED_VERSIONS 1.15-1.25`; GP-6528 go1.26).

**C3 verdict:** the *subject* (Ghidra 12.1.4's map-type layout read) is kaidoku's alone; no sibling could contest a C3 artifact. `[I]` No absorption risk at corpus level.

**But the parent boundary is contested** (see §2.1): `tsukuroi-shokunin/PROVINCE.md:79` — “Kaidoku and revenger both declare shipped-artifact RE. The integrator must arbitrate this shared scope”. No ruling exists in the lane or fleet text read. Consequence for C3: keep the claim about **Ghidra's read**, never about owning native RE; the carriers' semantics stay out. Under either ruling the analyzer-behaviour claim survives because it is a statement about the tool, not the artifact.

## 2. Contested scope and owners

### 2.1 Shipped-artifact RE (formal, unresolved)

| lane | declaration |
|---|---|
| kaidoku | `PROVINCE.md:3-4` “reverse engineering of shipped artifacts … native ELF through the Ghidra 12.1.4 provider” |
| revenger | `PROVINCE.md:3-7` “reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript … using the REA skill” |
| tsukuroi | `PROVINCE.md:79` unresolved; `PROVINCE.md` ADJ-06 routes driver/binary RE to “protocol integrator — kaidoku/revenger ownership unresolved” |
| kotoba | `PROVINCE.md:32` routes shipped-artifact RE to **revenger**, not kaidoku |
| game-dev-3d | `PROVINCE.md:38-41` REA as static inspection only; “reverse engineering as an end in itself” → revenger |

**Owner of the ruling:** protocol integrator. **No lane may absorb the other's ground.** C3's analyzer claim is the safe carve-out.

### 2.2 jj branch-tip tooling — the law already exists

The rule C2 implements is fleet law, taught and implemented outside kaidoku:

- `scripts/hyaku/lane-addendum.md:136-142`, esp. `:140`: “record measured/pinned revisions as the branch tip, never bare `HEAD`; Read-only jj only with `--ignore-working-copy`.”
- `scripts/hyaku/jj-lane.sh:50-63` (`detect_branch`: `symbolic-ref` → `origin/HEAD` → `master`→`main`→first local) and `:71-77` (`state` reads `refs/heads/<branch>` + `refs/remotes/origin/<branch>`, `head=attached|detached`). `scripts/hyaku/inline.sh:33-34` states the same and is what `inline.sh` consumes (`lane_tip` = `state … local`).
- `kama-shokunin/AGENTS.md:6` restates it for a lane: read `git rev-parse master` or `jj-lane.sh state`, never `@{u}`, `--abbrev-ref HEAD`, `branch --show-current`; git-writing gates run in a `/tmp` clone.
- Sibling prior art from r17: `tameshi-shokunin/.ufo/waves/round-17/w1/C01SiblingOverlap.md:99-100` (“branch-tip rule is already fleet law … already restated by kama”) and `:118-119` — “**Branch-tip semantics belong to the fleet helper**, not to a lane tool … not define a second convention.”
- `tameshi-shokunin/.ufo/waves/round-17/w1/S03RunPinDisposition.md:74-101` is a 21-lane HEAD survey: kaidoku/kama/tameshi detached, mado attached, four `.jj` repos; kaidoku's branch is `main`, kama/tameshi `master`.
- `tameshi-shokunin/.ufo/waves/round-17/w1/S11HeadSweep.md` classifies 115 HEAD-token sites and fixes one live code site (`:144`, `tools/pin-disposition.py:318`).
- `kama-shokunin/.ufo/waves/round-17/build/advice/ScoutJjLaneHygiene.md:62` records that kama's rule is uncommitted doc-only, with five old lessons still prescribing `@{u}..HEAD`.
- `mado-shokunin/corpus/lessons/round-14.md:126-129`: read-only `jj` without `--ignore-working-copy` mutates snapshot state.

**Consequence for C2:** it is the **third consumer**, not the discovery. `revpin.py` must cite `lane-addendum.md:140` + `jj-lane.sh:71-77` in its docstring and must not present itself as the fleet convention. `branch="main"` is correct **for kaidoku only** (`S03:84`); siblings use `master` (`S03:77-101`). A hardcoded fallback to `master` would be wrong here, and a silent auto-detect would diverge from the frozen contract — keep `--branch` explicit and fail closed with `branch_missing`.

**Live state is already the jj shape** `[O]`: HEAD is detached (exit 1), `--abbrev-ref` prints `HEAD`, `--show-current` prints nothing, yet `HEAD == refs/heads/main == 9011581`. So the three C2 sites are *live but currently benign*; the behavioural red exists only in a jj mutation sandbox, which is exactly what `jj-red-before.py` is for. Do not claim the live lane currently demonstrates the failure.

### 2.3 Durable jj knowledge — kaidoku has “no route”

`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjConnectorProvinces.md:189` (R9) lists **kaidoku** among lanes with “No route … Do not seed jj entries in product domains”; the substrate entry is routed to **kumitate** (`:181`, R1), the contract text to the **protocol lane** (R4), receipt consequences to **souji** (R2), fixture method to **tameshi** (R3). `:28` records “No province claims VCS”.

So C2's “sourced: jj documentation row opened this round” must be scoped as **citation support for a lane tool**, not a jj knowledge entry. The duplicate-of-record entry belongs to kumitate (unscheduled, next round 35), and the fleet text edit belongs to the protocol lane. Nothing in kaidoku should restate the helper contract.

### 2.4 Ownership table

| item | owner | evidence | must not absorb |
|---|---|---|---|
| C1 routed defects + `routed-defects.py` | kaidoku | `corpus/lessons/round-17-verifier-spotcheck.md` (lane) | tameshi's method; sibling gates |
| C1 QUALITY criterion wording | integrator (L1) | `contract.md` C1; `corpus/QUALITY.md` admission row | tameshi owns the verification-method text (`PROVINCE.md:3-17`) |
| C2 lane tools (`revpin`, `head-rev-lint`, 3 in-place fixes) | kaidoku | `contract.md` C2 | fleet helper semantics; `PROTOCOL.md` text |
| jj substrate knowledge | kumitate (r35, unscheduled) | `JjConnectorProvinces.md:181` | kaidoku, per `:189` R9 |
| jj contract text (`HEAD`→branch ref) | protocol lane | `JjConnectorProvinces.md` R4 | any lane-local restatement |
| branch-tip helper | operator/integrator (`scripts/hyaku/`) | `C01:118`; `lane-addendum.md:136-142` | a second convention in a lane tool |
| C3 Ghidra-Go analyzer behaviour | kaidoku | `PROVINCE.md:3-4`; zero sibling corpus | carrier semantics; RE-ownership claim |
| RE boundary ruling | protocol integrator | `tsukuroi/PROVINCE.md:79` | either lane absorbing the other |

## 3. C1 overlap

No sibling claims the six routed R17 defects. `tameshi-shokunin/PROVINCE.md:3-17` owns *verification-fixture craft*, admits a pattern only from **two independent lanes** (`:15-16`), and “Never edits a sibling's gate code” (`:16-17`). `routed-defects.py` is a kaidoku gate, so tameshi's role is method citation only. The lane's `corpus/lessons/round-17-verifier-spotcheck.md` is kaidoku's own record; tameshi's similarly named file is `round-16-verifier-spotcheck.md` — do not cross-cite them.

## 4. Calibration defect found: the lint's “before” count is not 3

`contract.md:61-67` defines the scan set and the context rule verbatim: `fixture` **iff the enclosing Python function name contains `selftest` or `fixture` (AST)**, else `live`; shell files are always `live`. `claims.json:20` claims “live HEAD-as-revision call sites **3** at 9011581 → 0”.

Under that written rule, the tracked `*.py`/`*.sh` sites at `9011581` enumerate as **8 live / 6 fixture**:

| # | path:line (at 9011581) | kind | enclosing def | context |
|---|---|---|---|---|
| 1 | `.ufo/gates/citation-drift/citation-drift-probe.py:477` | `default-HEAD` | module-level argparse | **live** |
| 2 | `.ufo/gates/custody-pair/custody-pair.py:327` | `rev-parse-HEAD` | `repo_head` | **live** |
| 3 | `.ufo/waves/round-17/controls.py:442` | `rev-parse-HEAD` | `_commit` (def `:429`) | **live** by rule, “fixture” by `JjAuditKaidoku.md:212` |
| 4 | `.ufo/waves/round-17/verify.py:59` | `rev-parse-HEAD` | `main` (def `:54`) | **live** |
| 5 | `.ufo/waves/round-17/w2/audit-attack.py:91` | `rev-parse-HEAD` | `build_repo` (def `:71`) | **live** |
| 6 | `.ufo/waves/round-17/w2/audit-attack.py:348-349` | `rev-parse-HEAD` | `main` (def `:316`) | **live** |
| 7 | `.ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh:9` | `rev-parse-HEAD` | shell | **live** (always) |
| 8 | same file `:11` | `rev-parse-HEAD` | shell | **live** (always) |
| — | `round-17/measure.py:223` | `rev-parse-HEAD` | `_git_fixture` | fixture |
| — | `round-17/tools/invocation-audit.py:424` | `rev-parse-HEAD` | `selftest` | fixture |
| — | `round-17/tools/temporal-sweep.py:261,289,308,332` | `rev-parse-HEAD` | `selftest` | fixture (4) |

`[O]` `controls.py` `_commit` is called only from `selftest` (`:452,:454,:474`), so it is semantically a fixture; the rule is syntactic. `[O]` `audit-attack.py` and `rebuild.sh` are r17 wave-2 attack fixtures, but they sit inside the contract's scan paths and are not named as excluded.

**The ladder:** 8 live under the written rule; 6 if `w2/` attack fixtures are excluded; 4 if `w2/` and shell fixtures are excluded; 3 only if `controls.py:442` is *also* reclassified `fixture` — two unstated exclusions beyond the contract text. The r17 audit itself labels `controls.py:442` “None (fixture)” (`JjAuditKaidoku.md:212`) while the contract's classifier calls it live, so the audit's “top three risks” (`:242,:244,:246`) are **not** a site count.

**Second spec gap:** the claim's three intended sites are not homogeneous — custody-pair is a literal `["git", …]` argv, citation-drift is an argparse default, and verify.py is a **wrapper** call `git("rev-parse","HEAD")`. A literal-list-only detector would miss verify.py and contradict the claim; a wrapper-aware detector necessarily also sees `controls.py`, `audit-attack.py`, `measure.py`, `invocation-audit.py`, `temporal-sweep.py`. The contract must say which.

**`[I]` Consequence:** a literal implementation will fail its own stated before-value (8 or 6, never 3), and after fixing the three routed sites it will report 5 (or 3), never 0. The claim “3 → 0” is only true if “live” means “the three routed instruments”. Recommended resolution in §6: report both numbers and gate on the routed one; do not tune the classifier.

## 5. Other sibling facts that bear on C2's tools

- **`pushed` must be fail-closed.** `souji-shokunin/corpus/lessons/round-5.md:15-19`: “no remote-tracking ref → pushed-unverifiable”; a local branch alone cannot establish pushed. `revpin` returns `remote: null` for an absent remote, so `pushed` must be `remote is not None and source == remote`, never `head == remote`, and `require_pushed` must raise `branch_not_pushed` on `null`. `[I]` This is the one substantive tightening the sibling evidence supports.
- **`--ignore-working-copy` is a sibling lesson, not an option.** `mado…/round-14.md:126-129`. `jj-red-before.py`'s read-only `jj log`/`jj st` calls should carry it; `jj-lane.sh.new` additionally wraps every snapshotting call in `--config 'snapshot.auto-track="none()"'` (`diff jj-lane.sh jj-lane.sh.new`, header rule block), which the sandbox does not inherit.
- **Do not “fix” fleet tools.** `scripts/hyaku/fleet-commit.sh:54,64` and `scripts/hyaku/append-closure.py:119` read `git rev-parse HEAD` against the **fleet** repo, which stays on git (`lane-addendum.md:145-146`; `PHASE2.md:64-65` “Fleet-root commits stay on git”). Those are legitimate and outside `head-rev-lint` (LANE-only).
- **Lint scope is load-bearing.** If `head-rev-lint` ever scanned `scripts/hyaku/`, it would flag the canonical helper's `git symbolic-ref` (`jj-lane.sh:55,57,77`) under kind `upstream`. Keep the contract's LANE-only scan and do not add the helper to an allowlist.
- **Fixture HEAD is not always wrong.** `S11HeadSweep.md` §1 note (b): fixture `git init` without `init.defaultBranch` should keep `HEAD`, not a literal branch. `revpin`'s own selftest fixtures should pass `--branch` (or `git init -b main`) explicitly rather than relying on the host default.

## 6. Proposed move — one bounded change

**Evidence.** (i) The pin law is already canonical at `lane-addendum.md:140` and implemented at `jj-lane.sh:71-77`; (ii) `tameshi/C01:118` forbids a lane tool defining a second convention; (iii) `souji/round-5:15-19` requires fail-closed pushed; (iv) the contract's own site rule gives 8 live/6 fixture at baseline, not 3/0. All four are already-observed bytes; none needs a new instrument.

**Move.** Keep C2's interfaces exactly as contracted, but make two *reported* facts honest, and cite rather than re-derive:

1. `revpin.resolve_source`: define `pushed := (remote is not None) and (source == remote)`. `remote: null` ⇒ `pushed: false`. With `require_pushed=True` ⇒ `branch_not_pushed` (exit 2). Never compare `head`. Docstring cites `lane-addendum.md:140` + `jj-lane.sh:71-77` and states “lane-local resolver, not the fleet convention; `branch` is explicit (kaidoku = `main`)”.
2. `head-rev-lint` output adds `routed_live_count` (sites in `verify.py`, `citation-drift-probe.py`, `custody-pair.py`) alongside `live_count`; `--strict` gates on `routed_live_count`; the claim text and `measure.py` use the routed number, with the mechanical total reported as diagnostic.
3. No branch auto-detection and no `master` fallback: on a non-`main` lane the tool fails `branch_missing`, which is the honest result for a lane-scoped tool.

**Affected axes.** Calibration — removes two false greens (untraceable “3→0”, `pushed` true on a missing remote). Operability — a named `routed_live_count` plus the existing exit-2 findings lets the L1 gate on what it fixed. Depth — reuses vetted helper semantics instead of minting a competitor. **No axis harmed:** `--branch` explicit keeps current behaviour; the scan paths and exit codes are unchanged.

**Risks.** (1) Editing the claim's numbers can read as scope shrink — it is a correctness correction, and the mechanical total still moves 8→5. (2) If `pushed` is implemented from `head`, the “tip ahead of origin” selftest passes for the wrong reason; derive from `source`. (3) Two counts invite “which is real”; state that routed is gated and total is diagnostic. (4) Reclassifying fixtures by call-graph instead would still leave `controls.py` live (called from `selftest`) and `w2/rebuild.sh` live — it does **not** reach 0; the dual-count route avoids classifier churn.

**Verification** (to be run by the owning executor, not this seat):
- `python3 -I -B .ufo/waves/round-18/tools/revpin.py --root <mkdtemp repo with no origin> --no-require-pushed` → exit 0, `remote: null`, `pushed: false`; without `--no-require-pushed` → exit 2, finding `branch_not_pushed`.
- `head-rev-lint.py --root LANE --rev 9011581` → `routed_live_count: 3`, `live_count: 8` (this enumeration; a different total is a finding, not a failure). At the delivered rev → `routed_live_count: 0`, `live_count: 5`.
- `grep -n 'lane-addendum\|jj-lane.sh\|fleet convention' .ufo/waves/round-18/tools/revpin.py` resolves the citation; `grep -n 'master' revpin.py` shows no fallback.

## 7. Limits

- No gate, selftest, lint, `revpin`, or `jj` command was executed; everything is static reading of bytes at `9011581` and live `git` plumbing.
- The §4 counts are **my** reading of the written rule, not a tool output; the lint does not exist yet.
- Sibling tips move: `tameshi/S03` sampled at `2026-10-20T15:21Z`, my probes later; both agree on kaidoku (`DETACHED`, `main`, `9011581`).
- Corpus sweeps via the `grep` tool have no process exit; the two definitive sweeps quoted with exits were shell `grep -rliE` over explicit paths.
- No installs or upgrades were needed. No sibling file, gate, corpus, or ledger was modified; the only write is this report.
