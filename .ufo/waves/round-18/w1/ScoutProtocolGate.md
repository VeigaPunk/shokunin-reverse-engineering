# ScoutProtocolGate — R18 evidence rules in PROTOCOL.md:300-544

Read-only scout. Question: which rules in `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:300-544`
bind a child lane's round evidence (gate standard, two evidences, frozen re-run, registry rows,
red-before), and which does round 18 risk violating? Labels: **OBS** = observed in this read;
**INF** = inference from the quoted rule. No REA/Ghidra run, no carrier execution, no lane write
beyond this report.

## Commands run (all read-only)

| # | Command (cwd = LANE unless noted) | Exit | Observed |
|---|---|---|---|
| 1 | `awk 'NR>=300 && NR<=400 {printf "%d\|%s\n", NR, $0}' PROTOCOL.md` | 0 | numbered source; used for every quote below |
| 2 | `awk 'NR>=401 && NR<=544 {…}' PROTOCOL.md` | 0 | ditto |
| 3 | `grep -nE '^## |^### ' PROTOCOL.md` | 0 | headings at 356, 388, 439, 467, 515, 543 |
| 4 | `git rev-parse refs/heads/main HEAD refs/remotes/origin/main` | 0 | all three = `9011581d84527ba34c675f9cf912e54d2e72d470` (matches claims baseline) |
| 5 | `git status --porcelain --untracked-files=no \| wc -l` | 0 | **0** on first read, **2** on a later read (`M .ufo/waves/round-17/tools/compare.py`, `M .ufo/waves/round-17/verify.py`) — the worktree is moving |
| 6 | `awk` admission-table row count on `corpus/QUALITY.md` | 0 | `admission_rows=20` (the 26 from a raw numbered-row grep includes the 6 weak-signal rows) |
| 7 | `ls .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` | **2** | absent under LANE |
| 8 | `git ls-files --error-unmatch .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` | **1** | not tracked in LANE |
| 9 | `git -C /home/vgpnk/Projects/shokunin ls-files --error-unmatch .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` | 0 | tracked in the fleet repo; last commit `7d0c7605b66b6e7fa2d998fc66534586d660bd26` (2026-10-20 11:39:58 -0300) |
| 10 | `grep -cE '^\| *S0[0-9]{2}' corpus/SOURCES.md` | 0 | 32 (S001–S032; S033 absent, draft exists at `w1/DraftS033Row.md`) |
| 11 | `git ls-files .ufo/waves/round-18 \| wc -l` | 0 | 0 — every round-18 wave file is untracked |
| 12 | HEAD-site survey: `grep -rnE 'rev-parse…HEAD\|default…HEAD\|HEAD:\|@\{u\}\|--abbrev-ref\|--show-current\|symbolic-ref'` over `.ufo/{gates,rounds,waves/round-14..18}/**/*.{py,sh}` | 0 | 12 hits; scopes checked one by one (below) |
| 13 | `ls /home/vgpnk/.local/share/kaidoku-r18/carriers/` | 0 | 8 carriers + `SHA256SUMS` exist **outside** the repo |
| 14 | `python3 -` JSON walk of `wave1-spec.json` for registry items | 0 | `DraftRegistryCells` names only the four existing rows + citation-drift |

---

## 1. Rules extracted (verbatim, with line numbers)

### 1.1 Evidence standard — PROTOCOL.md:356-386

- **:358-360** "Everywhere the protocol says *evidence*, it means a resolvable pointer: a repo path, a
  command and its output, a commit, or an external document — never a naked assertion. A `LOG.md` entry
  without a pointer is not evidence; an unreachable claim in a lane report does not exist."
- **:361-364** "An **end-to-end domain task** is one real work item executed against the domain's actual
  surfaces, logged as trigger → action → outcome → pointer. Where the domain's terminal action is
  operator-owned (§Invariants, local-first), executed means *prepared + verified + handed off*: the
  handoff artifact is the outcome pointer, and a documented negative result at that gate still counts."
- **:365-367** "A numeric claim carries its counting command, an absence claim its search sweep, and a
  quote its location (frontmatter/body, file, line) — the `CORPUS.md` rules bind `LOG.md` entries and
  lane reports too, not only `corpus/`."
- **:367-368** "A status command printing configured values is not evidence of capability:
  endpoint/ability claims need a probe against the real surface."
- **:369-373** "An evidence pointer must resolve at *closure* time, not only at write time: paths under
  `tmpfs` (`/tmp`, `/dev/shm`), session-scoped `local://` artifacts, and any pointer a fresh session
  cannot reach are not evidence — commit the artifact or cite a reproducible command. A timestamp on
  evidence must be at or before the commit that ships it — future-dated evidence is a conformance
  defect (§Appendix, "Evidence standard")."
- **:374-375** "**Claimed ≠ re-executed.** A command offered as evidence is a re-run performed at write
  time with its observed output — never an output quoted from memory or a prior session."
- **:376-378** "**Corrections sweep every mention.** Before a round's commit, grep every file the lane
  touches (`corpus/README.md`, `SKILL.md`, `knowledge/`) for the superseded claim — a corrected fact left
  standing in a sibling file is still a defect."
- **:379-380** "**A falsified claim in an append-only file gets a named correction entry in the lane's
  next round** — appended, never rewritten; it stays on the routed-defect queue until it lands."
- **:381-382** "**Commits are cited by hash, never by subject or tag** — `git rev-parse round-4` fails
  wherever the tag doesn't exist."
- **:383-386** "**Drift pins.** A pin counts only if its expected values are **persisted inside the
  repo** (a recorded sha/mode/lines baseline, or a committed expected-output file the script diffs
  against); a fingerprint *printer* with no stored baseline cannot detect drift; a pin is `RECOMMENDED`
  where the cited surface is outside the lane's control."

### 1.2 Gate standard — PROTOCOL.md:388-437

- **Gate vs probe, :390-392** "A **gate** is a committed, re-runnable verdict script a lane owns: it reads
  surfaces, compares them against expected values persisted in its own repo, and returns a verdict. A
  tool that cannot fail is a **probe**, and is registered as one."
- **Verdict map, :393-397** "`0` = `clean` and `1` = `failed` fleet-wide; every other code a gate exits
  (`2`, `3`, `64`, …) is declared in its registry entry and mapped onto `clean | failed |
  could-not-evaluate`, and an undeclared nonzero code reads as `could-not-evaluate`."
- **Self-test, :398-402** "Every gate exposes a self-invocation mode over isolated fixtures (temp trees,
  no network, no live-tree write) asserting both the exit code and a stable expected finding-id, with the
  expected values committed in the owning repo and independent of the recomputation. … a helper-only or
  model-only self-check does not satisfy this clause."
- **Two evidences / frozen re-run, :403-410** "Self-test green is capability, not a measurement. A gate
  whose verdict depends on a mutable fleet artifact also ships a run over a committed input snapshot with
  its committed expected verdict, so a later hand-edit of that artifact contradicts the frozen run. A
  verdict names the revision it was measured against: a gate grades the tree it runs on, so a run over a
  moving worktree is not comparable to one over the cited commit. A frozen baseline's `expected.json`
  MUST pin the digest of every snapshot input file, and the gate verifies those digests before comparing
  verdicts: an edited snapshot is `snapshot_tampered` (could-not-evaluate), not a compared verdict, and a
  baseline without digests is reported `unpinned (legacy)`."
- **Registry rows, :411-419** "The schema is this section's; a child lane's *registry home* is its own
  `SKILL.md`. … Row fields: name, `gate|probe`, entry command, verdict map (code → class), self-test
  command and spelling, pinned-value path, write scope, owner. … Frozen baseline names resolve under any
  `.ufo/waves/*/frozen` root; a bare name matching more than one root fails closed."
- **Scope, :420-424** "Read-only over surfaces it does not own, and it never acts on an external surface —
  publishing, vault approval, claim submission and driver mutation stay operator-owned. A verdict is
  lane-local evidence: it never defines the host runtime's stop conditions (`loop_stop`/`mission_goal`)
  and never stands in for the native judge."
- **Closure consequence, :425-430** "A red gate is a conformance defect recorded in the round notes and
  routed to its owner — status-neutral unless the round's rules already prescribe `failed`; gate redness
  is never the marker predicate, since step 1 grades marker-versus-real-report first and only a marker
  invokes `failed`. The integrator verifies a gate's *committed evidence* (self-test tally, frozen-run
  verdict, the revision measured); it does not execute a sibling's gate."
- **Delivery, :431-437** "… closure grades no gate conformant until its registry row exists at the lane's
  *registry home* defined under **Registry** above. The closure gate verifies the history pin
  (§Round-robin step 4) as committed evidence; a pin failure is a conformance defect routed under
  Closure consequence."

### 1.3 Invariants that bind the same evidence — PROTOCOL.md:439-513

- **:445** "`LOG.md` | Append-only iteration log: round entries, accepted changes, falsifiable
  next-iterations".
- **:476-477** "Rounds are evidence-driven: every `LOG.md` entry cites the work that motivated it." /
  "`LOG.md` is append-only: entries are never rewritten or deleted; corrections land as new entries."
- **:482-489** "Lanes write only inside their own child repo and their lane report at
  `.ufo/reports/round-<N>/<id>.md` … `.ufo/reports/`, `.ufo/waves/`, and the round's
  `.ufo/prompts/*.md` are committed with the round's integration commit — an untracked prompt is
  non-durable dispatch evidence. `.ufo/state/` and `.ufo/watchdog.log` … no lane commit may include
  them".
- **:492-502** local-first / push scope; "A lane's main-repo commit is pathspec-limited to its own report
  file … never `commit -a` / `add -A`".
- **:503-509** lane identity; main-repo commits use `git -c user.name=<lane>-shokunin …`.
- **:510-513** "`corpus/` inherits the evidence standard: every `knowledge/` entry cites a resolvable
  source; `corpus/lessons/` entries cite the round and its LOG.md entry or lane report. Corpus
  corrections are new entries, never in-place rewrites".

### 1.4 Fleet-2 claim rules — PROTOCOL.md:515-529

- **:517-520** "each lane owns a named subset and works 1–3 declared claims per round (each an axis-move
  on a distinct axis with its own falsifiable before→after; at least one on the lane's lowest non-retired
  axis; a claim may be a capability acquisition or an exploratory taste-bound claim per `AXES.md`, section
  *Capabilities*), measured in `SCORECARD.md`."
- **:521-523** exploratory claims verify only as `unprovable-but-better` with a named non-author reviewer.
- **:523-525** "An axis-move inherits the evidence standard: before and after numbers each carry the
  counting command and the commit they were measured against, and a score no reader can re-derive is an
  opinion, not a measurement."
- **:525-529** an axis name not defined in `AXES.md` is worked only if its row carries the mapping to one
  of the six axes in the same row; axis work does not displace the file contract.

### 1.5 Closure-row rules that touch evidence — PROTOCOL.md:300-338

- **:301-307** `in-flight` is debt answered by the next protocol round via an appended
  `closure-correction`.
- **:311-320** row identity: `lane_rounds` annotates, never re-keys; an `ok` row's report path is
  derivable and "its absence falsifies the row".
- **:321-326** retroactive closure is typed and "is not a pass".
- **:327-334** `rounds` is append-only; corrections carry `supersedes`.
- **:335-338** "`.ufo/history-pin.json` pins `sha256(rounds[0:k])` for the closed prefix plus the commit
  whose `MANIFEST.json` bytes hash to it; the closure gate reports `history_pin_mismatch` … Appends never
  invalidate it."

### 1.6 "red-before" — not a PROTOCOL term in 300-544

- **OBS:** the only occurrence of "red" in the range is **:425-427** — "A red gate is a conformance
  defect … gate redness is never the marker predicate". Nearby binding rules are **:390-392** (a tool
  that cannot fail is a probe) and **:398-402** (self-test asserts the red case's exit and finding-id).
- **INF:** the round's "red-before" duty (claims.json:13 "whose red state is the baseline";
  claims.json:20 `jj-red-before.py`) comes from the lane's own QUALITY/lessons practice
  (`corpus/lessons/round-16.md:58-61` uses the phrase), not from PROTOCOL. Cite it as lane doctrine, not
  as a PROTOCOL requirement.

---

## 2. Flags against the round-18 plan

Severity: **H** = closure/claim verification would fail as written; **M** = evidence weakened, cheap fix;
**L** = wording/durability.

### F1 (H, calibration) C2 works a fleet axis the lane does not own — type it capability acquisition
- Plan: `claims.json:17-21` declares C2 on axis `operability`; `claims.json:7` itself lists only
  coverage/depth/calibration as the lane's axes.
- OBS: `SCORECARD.md:23-25` Owned axes = coverage, depth, calibration; every operability row is labelled
  "operability (fleet axis, unowned proxy; capability acquisition)" (`SCORECARD.md:682`, also `:490`,
  `:549`, `:744`).
- Rule: PROTOCOL.md:517-519 (lane works its named subset) + :519-520 (a claim may be a capability
  acquisition) and :523-525 (per-axis verdict). AXES.md:57-64: a capability row enters only through a
  round that demonstrates it running.
- Fix: label C2 `capability acquisition` in claims and the round report, add the capability row only
  after the jj-red-before receipt is green, and record the operability verdict with its counting command;
  otherwise a reader sees an axis-move on an unowned axis.

### F2 (H, calibration) C2's before-number "3" contradicts the contract's own lint definition
- Plan: `claims.json:20` "live HEAD-as-revision call sites 3 at 9011581 -> 0"; contract.md:61-70 defines
  `live` as *any* `rev-parse`/`HEAD`/upstream site whose enclosing function name lacks
  `selftest`/`fixture`, scanned under `.ufo/{gates,rounds,waves/round-14../round-18}`.
- OBS extra live sites at baseline 9011581 (same tree as HEAD):
  `.ufo/waves/round-17/controls.py:429` `def _commit`, site `:442` `git(root, "rev-parse", "HEAD")`;
  `.ufo/waves/round-17/w2/audit-attack.py:71` `def build_repo`, site `:91`.
  Fixture-classified (names match): `temporal-sweep.py:233` `selftest` → sites :261,:289,:308,:332;
  `measure.py:198` `_git_fixture` → site :223; `invocation-audit.py:369` `selftest` → nested `put` at
  :379, site :424. The three audited sites are `verify.py:59`, `citation-drift-probe.py:477`,
  `custody-pair.py:327` (also `:349` uses the same `repo_head`).
- **OBS:** the fleet audit corroborates exactly three *risks*
  (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:240-249`, R1/R2/R3),
  but those are audit risks, not the lint's site set.
- INF: under contract.md:66-67 the baseline `live_count` is at least 5, so "3 → 0" is unmeasurable
  unless `_commit`/`build_repo` are reclassified or fixed. Decide one before the tool is written: fix all
  live sites (two more `--rev`-style fixes), or narrow the site definition (and restate the before
  number). Also ensure `gen-wave1.py:374,463` prose strings are not counted as "git argv".

### F3 (H, registry rows) the four new W18 tools have no planned `SKILL.md` registry row
- Plan: `contract.md:41-43` fixes existing rows only; the only registry item is `DraftRegistryCells`
  (`wave1-spec.json`), whose prompt names the four r17 rows + citation-drift. No item adds rows for
  `routed-defects.py`, `head-rev-lint.py`, `jj-red-before.py`, `swiss-misread.py`.
- Rule: PROTOCOL.md:411-419 (row fields) and :431-435 ("closure grades no gate conformant until its
  registry row exists at the lane's *registry home*").
- Fix: add rows at `SKILL.md:539+` with name, `gate|probe`, entry (including `--strict` where the gate can
  fail), verdict map 0/1/2, `--selftest` spelling, pinned-value path, write scope, owner. `swiss-misread`
  exits 0/2 only → register as **probe** (:390-392). Also map jj-red-before's 2 = could-not-evaluate.

### F4 (H, registry content) R17-REGISTRY's check tests only half the defect
- Plan: contract.md:41-43 requires only a 5th cell containing `Write scope:` and the citation-drift kind;
  the lesson's defect is broader — "no pinned-value path or write scope"
  (`corpus/lessons/round-17-verifier-spotcheck.md:139-141`).
- Rule: PROTOCOL.md:414-416 row fields include **pinned-value path** and **write scope**.
- Fix: add a check that each of the four rows also names its pinned values (e.g. contains
  `Pinned values:` or a path), plus its self-test spelling; otherwise a gate green can coexist with a
  nonconformant row and closure defects it again. The draft item
  (`DraftRegistryCells` → "Draft replacement 5th cells (`Pinned values / write scope`)") suggests the
  content will be right — the gate still cannot see it.

### F5 (M, numeric claim) QUALITY 20→21 has no counting command
- Plan: `claims.json:13` "QUALITY data rows 20 -> 21 with rows 1-20 byte-identical".
- OBS: the counting command exists and gives 20 — `awk` admission-table count = 20 (raw
  `grep -cE '^\| *[0-9]+ *\|'` gives 26 because the weak-signal table is 1–6). `controls.py` only checks
  rows 1–20 identical; nothing reports the count.
- Rule: PROTOCOL.md:365-366; also :523-525. Fix: put the scoped counting command in the claim / SCORECARD
  verdict row and have `controls.py` report `admission_rows` as a field.

### F6 (H, evidence) C1's "6 at 9011581" must be a retained re-run, not an embedded expectation
- Rule: PROTOCOL.md:374-375 (re-run at write time with observed output) and :406-407 (a run over a moving
  worktree is not comparable).
- OBS: the worktree changed between two reads of this report (0 → 2 tracked modifications:
  `round-17/tools/compare.py`, `round-17/verify.py`), so any "delivered revision" run over the worktree
  is inadmissible.
- Fix: retain `measure.py 9011581` output (expected `open_count: 6`) and `measure.py <integration-commit>`
  output as committed files under `W18/`, and cite both commit hashes in the report. The plan's phrase
  "at the delivered revision" needs that hash named.

### F7 (H, two evidences / frozen re-run) C3's "frozen in Git before any REA run" is not yet auditable
- Plan: `claims.json:26-27`; `contract.md:15` ("the L1 runs every carrier analysis once, sequentially,
  after predictions are frozen in Git"), `contract.md:17-21` (any jj/git write only in a mkdtemp clone).
- OBS: `W18/predictions/` does not exist yet; `git ls-files .ufo/waves/round-18 | wc -l` = 0; no named
  freeze commit or mechanism appears in contract.md. A prediction merely written to disk before the run
  is not "frozen in Git", and commit-time ordering cannot be shown from an integration commit that lands
  after the runs.
- Rule: PROTOCOL.md:371-373 (timestamp ≤ shipping commit), :406-407 (verdict names its revision), :374-375.
- Fix: name who makes the freeze commit and its subject (L1, before analysis), record the freeze commit
  hash in every `compare.json`/receipt and in `run-carriers.sh`'s pin set, and ensure run-log timestamps
  sit between freeze commit time and integration-commit time.

### F8 (H, drift pins / two evidences) C3's inputs and expected values live outside the repo
- Plan: `contract.md:103` puts carriers + `SHA256SUMS` at `/home/vgpnk/.local/share/kaidoku-r18/carriers/`;
  `carriers/build.sh:6,28` defaults `OUT=$here/bin` and only *prints* `<sha256> <file>`; the eight
  carriers and `SHA256SUMS` are observed only outside the repo. Calibration binaries `/usr/bin/aether`
  and `~/.local/bin/notesmd-cli` are also external.
- Rule: PROTOCOL.md:383-386 (expected values persisted inside the repo; a printer cannot detect drift) and
  :403-410. `swiss-misread`'s verdict depends on mutable installed artifacts (Ghidra typeinfo JSON,
  Base-src.zip, external binaries), so the conditional "two evidences" clause applies.
- Fix: commit `W18/carriers/SHA256SUMS` (the build output) and a
  `.ufo/waves/round-18/frozen/expected.json` that pins the digest of every snapshot input (carrier bytes,
  selected snapshot JSON, Base-src.zip member list, aether/notesmd digests) with the expected verdicts
  (`predicted_eof_reads`, `predicted_failure`, per-label match). Give the baseline a unique name that
  matches only this root (:417-419). `build.sh` should write the sums file, not only echo it.

### F9 (M, verdict naming) `jj-red-before.py` receipt names no revision
- Plan: `contract.md:88-98` — receipt schema `{steps, expectations, all_held}`, and the fixed probe is
  run "from LANE's working tree" (`:93`); no `rev`, `branch`, or digest of the probe bytes.
- Rule: PROTOCOL.md:406-407 ("A verdict names the revision it was measured against"). The fixed-probe
  bytes are a moving-worktree input; `git show B:` baseline is pinned, the fixed side is not.
- Fix: add `rev`, `branch`, `head_equals_source`, and sha256 of both probe variants (baseline blob and
  fixed file) to the receipt; write the receipt to a repo-relative path (e.g.
  `W18/evidence/jj-red-before.json`), not a bare `RECEIPT.json`.

### F10 (M, self-test) finding-id stability is unspecified for two tools
- Plan: `contract.md:61-70` head-rev-lint selftest asserts kinds/counts and exits only; `contract.md:119-120`
  swiss-misread selftest is "small synthetic byte fixtures" with no named finding-id.
- Rule: PROTOCOL.md:398-402 requires asserting exit code **and** a stable expected finding-id, with
  expected values committed in the repo.
- Fix: assert the emitted site kind/name (e.g. `head_not_branch_tip`, `rev-parse-HEAD`) and the exact
  `predicted_eof_reads`/`predicted_failure` finding per case; `routed-defects` already does this (one
  red case per defect id) and can be the pattern.

### F11 (M, pointer) C2's source pointer does not resolve from LANE
- Plan: `claims.json:19` cites `.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` (section 5).
- OBS: that path does not exist under LANE (`ls` exit 2; `git ls-files` exit 1). It exists and is tracked
  in the fleet repo at `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md`
  (commit `7d0c760`, section 5 at :240-249).
- Rule: PROTOCOL.md:358-360 and :369-373 (a pointer a fresh session cannot reach is not evidence).
- Fix: cite the fleet-repo path explicitly (or a fleet-root-qualified path) and the commit hash; do not
  write it from the lane (write scope, :482-484).

### F12 (L, citation discipline) "red-before" is not a PROTOCOL rule
See §1.6. Attribute the red-before form to `corpus/lessons/round-16.md:58-61` / QUALITY, and cite
PROTOCOL.md:390-392 and :425-427 for what the protocol actually says about failing tools and red gates.

### F13 (L, durability) round-18 evidence is not yet committed
- OBS: `git ls-files .ufo/waves/round-18 | wc -l` = 0. Not a defect mid-round, but PROTOCOL.md:485-486
  commits `.ufo/waves/` with the integration commit, and :381-382 requires that commit cited by hash.
- Fix: name the integration commit hash in the round report's evidence table; ensure `W18/runs/`,
  rehearsed receipts, and the frozen baseline are inside it.

### F14 (L/INF, calibration honesty) aether acceptance is not independent of the emulator
- Plan: `contract.md:119` calibrates `swiss-misread` on aether's logged EOF pair and then accepts aether
  by reproducing that same pair; only the 8 synthetic carriers are out-of-sample
  (`claims.json:26-27`).
- Rule: PROTOCOL.md:367-368 and :374-375 (a probe, not a status echo, is evidence).
- Note (INF): label the aether result "calibrated-on-this-pair" in the report; the falsifiable test is
  the 8-carrier frozen-outcome table. Do not let the calibration pair be counted twice as confirmation.

---

## 3. Premises that check out (not flags)

- **OBS:** claims baseline `9011581d…` equals `refs/heads/main`, `HEAD`, and `refs/remotes/origin/main`
  (command 4) — the before numbers are measured against the branch tip, consistent with
  `contract.md:17-19`.
- **OBS:** QUALITY admission rows = 20 (command 6), so "20 -> 21" is the correct table and the new row
  is row 21 (`w1/DraftQualityRow21.md` exists as a draft).
- **OBS:** the three routed HEAD sites exist at baseline: `verify.py:59`, `citation-drift-probe.py:477`,
  `custody-pair.py:327`; the fleet audit's section 5 lists exactly those three risks.
- **OBS:** claims are 1–3, on distinct axes (calibration/operability/depth), and the "tied-lowest"
  premise matches `SCORECARD.md:23-25` + round-17 rows `:257-259` (coverage 10.0, depth 10.0,
  calibration 10) — C1 satisfies the lowest-axis duty (:517-519).
- **OBS:** SOURCES holds 32 rows (S001–S032); C1's `S033` is drafted but not yet appended — expected
  mid-round, required at closure (:365-367, :510-511).
- **OBS:** `routed-defects.py`'s planned selftest (one red case per defect id, temp-tree fixture repo,
  expected values in the tool) matches :398-402; the gap is the second evidence (F6), not the selftest.

---

## 4. Remaining unknowns

- Whether the implemented `head-rev-lint` AST rule classifies module-level fixture helpers
  (`controls.py:_commit`, `audit-attack.py:build_repo`) as `live`; that decides whether the before number
  is 3 or ≥5 (F2). The tool's own run at `9011581` is the only resolution — do not freeze "3" first.
- Whether `DraftRegistryCells` is extended to rows for the four new tools after adjudication (F3); the
  current item text covers only existing rows.
- Who owns the prediction freeze commit and when it lands relative to the L1 analysis runs (F7); the
  contract fixes ordering but not the mechanism or recorded hash.
- Whether `swiss-misread` will ship a strict/failing mode; absent one it is a probe, and registering it
  as a gate would contradict :390-392.
