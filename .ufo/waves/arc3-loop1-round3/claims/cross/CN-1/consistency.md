# Cross-chain consistency sweep — arc3-loop1-round3 (SEAT CN-1, chain cross, connector)

Scope (frozen seat line): the three chains' instrument readings must not
contradict — (i) command A before-state identical across chains, (ii) custody
digests vs the 5 paths, (iii) probe/census states. Reconcile or flag here.

Method: every shared reading below was re-derived **by CN-1 from the instrument
itself, before reading any round-3 seat artifact** (first capture 13:07Z at HEAD
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`). CN-1 wrote only under
`claims/cross/CN-1/**`; scratch `/dev/shm/cn1-scratch` (never `/tmp`); custody
paths touched with sha256/stat reads only; no git mutations; no LOG/SCORECARD/
SHONEN/corpus/SKILL/README writes by this seat (a README line-shift variant was
emulated **in memory** — no file was edited).

Receipts: `claims/cross/CN-1/receipts/` — `baseline-pins.txt`,
`commandA-t0.txt`, `census-t0.txt`, `probe-t0.txt`, `custody-t0.txt`,
`custody-watch.txt`, `knowledge-digests-t0.txt`, `craft-map-t0.txt`,
`readme-line-shift-emulation.out`.

## 1. Baseline — the shared numbers every chain is checked against

| Reading | CN-1 command (cwd = repo root) | CN-1 result |
|---|---|---|
| HEAD | `git rev-parse HEAD` | `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`; worktree clean except ` M .ufo/waves/arc2-loop1-round10/C3.md` (pre-existing, carried) + untracked `arc3-loop1-round3/`, `.ufo/gates/__pycache__/` |
| command A (recipe `SCORECARD.md:92-123`, REV=`c07af80…`) | inline recipe, verbatim | `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "c07af80…", "rule_blocks": 14}` → **82/82, missing [], dangling [], 14/14, 10.0/10.0** |
| census (`c1-census-v10.py`, `d0772ce8…`, 610 L) | `python3 .ufo/gates/c1-census-v10.py` | `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, `DECLARED FAIL CLASSES: []`, G2 ok (current-ok loci PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; floor=1/file), G7 [], G11 [], exit 0 |
| citation-drift probe (`citation-drift-probe.py` `e2665074…`, table `738b3a56…`, expected `ff47bfd6…`) | `--rev HEAD` / `--rev HEAD --strict` / `--selftest` | `reported findings=0 exit=0`; `clean findings=0 exit=0`; `SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0` |
| pointer table shape | `json.load` count | entries **31** (exact 15 / extracted 11 / anchor 5), `quoted` 4, `exempt` 3; no duplicate ids; files pinned: SCORECARD.md 8, r7-pe-wall 6, corpus/README.md 5, PROVINCE.md 2, SHONEN.md 2, + 8 singles |
| custody 5-path (read-only sha256/stat) | `sha256sum` + `stat` per path | devin `16f496e6…263a4` (inode 11341318, 406 B, 600); omp `38d2a1d0…926b` (11341316, 429 B, 600); kimi `bc66d543…ddc3` (37793921, 114434 B, 644); bashrc `7d2ca28a…6598` (25991953, 3601 B, 644); profile `6c6be761…4f30` (40274, 736 B, 644) |
| custody tool selftest (`custody-pair.py` `112d01dc…`, 889 L) | `CUSTODY_PAIR_SCRATCH=/dev/shm/cn1-scratch … selftest` | `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0` — the C2 "before" count |
| instrument identities | worktree sha256 vs `HEAD:` blob | census `d0772ce8…`, probe `e2665074…`, expected `ff47bfd6…`, table `738b3a56…`, custody-pair `112d01dc…`, PROVINCE `d075a3c6…` (162 L), SCORECARD `c26f16bc…` (1496 L), SKILL `c134afcb…` (390 L), README `6ac43e83…` (190 L) — **all equal=True** |
| knowledge substrate (for C1's 82→83) | `git cat-file blob` per file, sorted | 82 files; list digest `6bcf3bad…`; per-file digests in `receipts/knowledge-digests-t0.txt` (`d74440c4…`) |
| command-A input slices (for line-neutrality checks) | python split on commit text | craft section `## Queue-drain craft` 11370 chars `173b8627…`, 178 L; README coverage-map section 57 L `875128ee…` |
| C1's reused instrument (receipt re-verified) | npm cache content file for `solc@0.8.37` | cache sha256 **`0e1a1ab6…575a51` = the receipt's pinned tarball sha256** (receipt `EX-02/install-receipt.txt` §1); prefix `node_modules/solc` runs → `0.8.37+commit.f401782d.Emscripten.clang`; prefix tree digest `f361af99…` |

## 2. Agreement matrix — chain records vs CN-1 re-reads (as they land)

| Shared reading | Chain record (round-3) | CN-1 independent | Verdict |
|---|---|---|---|
| tool revision under test `112d01dc…` | C2 `EX-22.md:15` (re-derived before+after; `transcripts/r5-tool-rehash.txt`) | identical (`baseline-pins.txt`) | **consistent** |
| HEAD `c07af80f…` | C2 `EX-22.md:16` | identical | **consistent** |
| custody-pair selftest before = 15/15 CLEAN exit 0 | C2 `EX-22.md:20,50` (`d1-selftest-happy.txt`) | identical | **consistent** |
| custody 5-path pre-state | C2 `RV-9/rv9-independent-T0.txt` (13:07:39Z); C2 `EX-29/verify-pre-roundstart-vs-live.out` (MATCH 5/5 exit 0); CU-1 `capture-pre-indep.txt` (13:07:07Z, 3 hash engines agree); CU-1 `grade-live-vs-EX29-pre.txt` (13:08:58Z, 80/80 cells) | identical digests, inodes, mtime/ctime ns on all 5 paths (CN-1 13:07:56Z) | **consistent** |
| path-3 drift vs round-2 post | C2 `EX-29/verify-roundstart-vs-r2receipt.out` → `CONTENT-DRIFT` moved=sha256; CU-1 `diff-r2post-vs-r3pre.txt` → MOVED 11/16 fields (sha, mtime, ctime, inode, mode 384→420) | CN-1 `verify capture-post.txt --live` → CONTENT-DRIFT, SHA256-CONTRACT 4/5 | **consistent** |
| probe before (findings 0 both modes, selftest 13/13, table `738b3a56…`, expected `ff47bfd6…`, entries 31/quoted 4/exempt 3) | C3 `EX-44/before-probe.txt`, `EX-44/before-selftest.txt` (13:06:47Z) | identical, byte-for-byte on every quoted number | **consistent** |
| command A before (82/82, 14/14, 10.0/10.0) | C1 `EX-04.md:80-82` (independent recipe copy, `git show`/`ls-tree` only); C2 pending; C3 pending | identical JSON field-for-field | **consistent** |
| solc prefix reuse (C1's no-install clause) | C1 `EX-04.md:12-16` (`soljson.js` `221d7a66…`, prefix `package.json` `b4205b08…`) | receipt re-verified: npm-cache tarball sha256 `0e1a1ab6…575a51` = receipt pin; `solcjs --version` → `0.8.37+commit.f401782d` | **consistent** |
| C2 revised pre-pair (landed tool) | C2 `receipts/config-pre-pair-v2r3-revised.txt` (13:15:44Z; self-pins tool `7cd19c3c…`) | CN-1 `verify` runs: revised-pre vs live → `MATCH 5/5 exit 0`; original-pre vs revised-pre → `MATCH 5/5` (no movement 13:06:57Z → 13:15:44Z across the tool-revision change); both sidecars `sha256sum -c` OK | **consistent** |
| C1 landing rehearsed against C3's landed table | C1 `records-drafts/{knowledge-entry-draft.md,map-token-patch.md}` (SC-2, line-neutral; RV-4 `coupling-rehearsal.out`: 82/82 → 83/83 → dangling control) | CN-1 rebuilt the landing in scratch (entry 17,563 B + line-neutral row patch; README 190 → 190): command A tree-mode **83/83, missing [], dangling [], 14/14**; 57-entry evaluation → **0 findings** (`readme38-arc3r1-token` hit at row 38; `readme22-*`/`readme175-*` intact) | **consistent** |
| C1 draft's self-stamp | SC-2 `knowledge-entry-draft.md:4` states "Revision 3 (~13:47Z…)" | file mtime `2026-10-19 10:15:54 -0300` = 13:15:54Z — the stated UTC is 31 min in the future of its own mtime | **inconsistent (cosmetic)** — do not quote that stamp |
| path-3 drift is pre-round, operator-side | C2 `EX-25.md:80-88` (same digests, ctime `12:57:45Z`, "not caused by this seat") | same fact from CN-1's capture + r2-post verify (CONTENT-DRIFT, 4/5) | **consistent** |
| write-guard after-state | C2 `EX-25.md:54-63` (REFUSED exit 2 at `d9be407d…`/`08fb6833…`, bytes intact; controls not over-refused) | re-derived at `03bd6242…` and `7cd19c3c…`: selftest CLEAN 21/21 then 22/22, guard arm refuses `--paths X --out X` | **consistent** |
| C3 real target landed (`pointer-table.json` 31 → 57 entries; `expected.json` re-pinned) | C3 `EX-41.md:14-24` (table `bfc42f1b…`, expected `d97dd60a…`, pin MATCH; entries +26, quoted 4, exempt 8) | re-derived: same digests; probe default/strict `findings=0`, selftest 13/13; `frozen_run` unchanged (`679af5d7…`, failed) | **consistent** |
| C3 extension green before landing | C3 `EX-43/proposed-pointer-table-extension.patch.md` (48-entry scratch table `0b01f521…`) | CN-1 ran the **real probe against the scratch table** with a re-pinned expected → `findings=0` both modes | **consistent** |
| custody README rewrite keeps C3's four convention anchors | C3 `EX-41/10-cross-seat-check.txt` (all four needles green after EX-21's rewrite) | re-derived over the landed README `f30df42e…` (185 L, `--require-paths` ×6, 22 cases declared): 4/4 anchors still match | **consistent** |
| registry row (SKILL.md) still the round-2 text | — (C2 row patch drafted, not landed: `EX-30/registry-row.patch.md`) | re-derived: SKILL.md `c134afcb…` unchanged; old precedence string still present → C3 anchor currently green — **see §3g** | **pending collision** |

No contradiction found in any shared reading so far. The two live hazards that
could *create* one are §3a (custody churn) and §3b/§3c (landing-order effects on
command A and the probe).

## 3. Cross-chain interaction checks (run by CN-1)

### 3a. Custody timeline — 4/5 paths byte-stable since round 1; path 3 was rewritten before this wave started

| capture (UTC) | devin | omp | **kimi `config.toml`** | bashrc | profile |
|---|---|---|---|---|---|
| r1 CU-1 `config-pre-pair.txt` 09:57:18Z | `16f496e6…` | `38d2a1d0…` | `8cbacd48…` (inode 34530637, mode 600) | `7d2ca28a…` | `6c6be761…` |
| r1 snapshots ×25 (10:00–10:24Z) | 0/5 drift across every check | | | | |
| r2 `EX-31/capture-pre.txt`/`capture-post.txt` 12:03/12:06Z | same | same | `8cbacd48…` (same inode) | same | same |
| r3 C2 `receipts/config-pre-pair-v2r3.txt` 13:06–13:07Z | same | same | **`bc66d543…` (inode 37793921, mode 644)** | same | same |
| r3 CN-1 `custody-t0.txt` 13:07:56Z | same | same | same as C2 | same | same |

Path 3 was rewritten at mtime/ctime epoch `1792414665` = `2026-10-19T12:57:45Z`
(9 min *before* the wave tree was created), with **same byte length 114434**,
new inode, mode 600→644, new digest — a same-length replacement, i.e. the
operator-side interactive-session churn class recorded in round 2, one rewrite
further on. Consequence for this round's frozen C2 clause "the round's live
pre/post pair verifies MATCH 5/5": it holds only while path 3 stays quiet for
the rest of the wave. Measured so far: `receipts/custody-watch.txt` — 60 s
checks from 13:08:17Z, 0/5 drift on every check to 13:10Z. The r1 precedent
(25 consecutive 0/5 checks) and the r2 precedent (one rewrite in the wave
window) bracket the risk: real, operator-owned, and not the lane's to repair.

### 3b. Command A ordering: "unchanged" must be revision-stamped, and the round's before-state is 82/82 for all three chains

The freeze gives all three chains the same before-state (82/82, 14/14) and
predicts C1's landing moves the denominator 82 → 83. Therefore:

- C2's and C3's after-clause "command A unchanged" is only well-defined
  **relative to a revision**: at a HEAD without C1's entry it is 82/82; at a
  HEAD with C1's entry it is **83/83, missing [], dangling [], 14/14**.
- A seat (or the parent's summary) that quotes "command A unchanged (82/82)" as
  the round's after-state *while* C1's entry is landed would state a number the
  recipe cannot produce — a cross-chain contradiction of exactly the class this
  seat exists to catch. Round-3 rule, pre-registered: **every command A reading
  carries its revision**; the parent's final reading at the work commit is
  authoritative, and the 82-file slice must remain byte-identical
  (`receipts/knowledge-digests-t0.txt` is the substrate for that check).
- The tree-mode harness `claims/cross/VZ-4/commandA.sh tree <ROOT>` exists for
  pre-landing projections; CN-1 verified it is the recipe body with only the
  byte-source swapped (`git show` → `open()`), regexes byte-identical.

### 3c. Probe/table coupling — C1's README edit is load-bearing for C3's "findings = 0"

The probe pins `corpus/README.md:22` (2 entries) and `:175` (3 entries), and
reads **one physical line** per entry (`probe:196` `citing_line = citing[line_no - 1]`;
no match → `citation_dead`, `probe:212-217`). C1's claim lands a new EVM token
in that same README. CN-1 emulated the two landing shapes against the probe's
own entry-checking code (`readme-line-shift-emulation.py`, faithful re-impl of
`probe:168-230`; prediction, not a probe run):

| variant | README lines | simulated findings |
|---|---|---|
| control (unmodified HEAD) | 190 | 0 |
| **A — line-neutral token add** (token appended to the EVM row, line 38) | 190 | 0 |
| **B — new physical map row** (one line inserted at 38) | 191 | **3 → `readme175-sc1217`, `readme175-r7range`, `readme175-r8e2` all `citation_dead`** |

So the freeze's "line-neutral map token" clause is not a coverage nicety: it is
the condition under which C3's frozen clause "probe findings = 0 at HEAD in both
modes" survives C1's landing. Routing rule for the parent: land C1's README edit
line-neutrally, then re-run the probe at the work commit; if C1's edit ever
needs a new row, C3's table must be re-anchored in the same commit (its digest
re-pin is already the F3 coupling).

Symmetric check on the other append points: every SCORECARD-pinned entry sits at
`:59/:60/:68/:69/:72/:270/:622/:699` and every other pinned file is untouched by
this round's target set, so the parent's SCORECARD append (records step) is
line-safe as long as it stays an append.

### 3d. Scope-disjointness of the three real targets (checked against the instruments' own inputs)

| real target (implementer only) | command A inputs | census inputs | probe inputs |
|---|---|---|---|
| `.ufo/gates/custody-pair/**` (C2/EX-21) | none (not corpus/, not README map, not SKILL craft) | none (census scopes PROVINCE/SCORECARD/SKILL) | none (no entry pins a custody tool path) |
| `SKILL.md` registry row `:390` (C2, same commit) | **outside** the craft section (`:81-259`; registry `## Local round-evidence gate registry` starts `:379`) — line 390 is a 2182-char single physical line, an in-place rewrite; craft slice sha `173b8627…` is the check | the only SKILL.md census block is `10-16` (historical) — row edit is outside it; G2 loci SKILL.md=3 to be re-measured | `shonen-skill-range` pins SHONEN.md:6's `SKILL.md:81-255` range + the natural-control needle — unaffected by a row edit at `:390` |
| `.ufo/gates/citation-drift/{pointer-table,expected}.json` (C3/EX-41) | none | none | self-target: digest re-pin is the F3 coupling; CN-1 re-runs `EX-46/pin-check.py` at landing |
| `corpus/knowledge/<new>.md` + `corpus/README.md` map row (C1) | denominator 82 → 83 (see §3b) | none (knowledge/README out of census scope) | **§3c hazard** |

Open wording note for the parent: the C2 freeze sentence "the registry row +
README are updated in the SAME commit" reads naturally as
`.ufo/gates/custody-pair/README.md` (the round-2 precedent). If it means
`corpus/README.md`, §3c's hazard applies to C2's edit too and the same
line-neutrality rule must bind it.

### 3e. C2's real target is churning inside the round — the revision map is a record requirement

Observed `custody-pair.py` revisions (UTC), from CN-1's watcher and C2's seats:

| revision | lines | selftest | observed by |
|---|---|---|---|
| `112d01dc…` | 889 | 15/15 | round-2 landed state; both round-3 pre-states (CN-1, EX-22 `:15`, EX-29 receipt `:3`) |
| `7b848eaf…` | — | — | EX-25 13:08:08Z |
| `d164d49f…` | — | — | EX-25 13:08:57Z (claim/code divergence measured, §4 there) |
| `460a01f0…` | — | — | EX-25 13:09:16Z |
| `9860149d…` | — | — | EX-25 13:09:40Z |
| `d9be407d…` | — | — | EX-25 13:10:01Z (first refusing revision) |
| `08fb6833…` | — | 15/15 | EX-25 13:10:40Z (full matrix REFUSED) |
| `03bd6242…` | 1109 | **21/21** | CN-1 13:12Z (re-derived; write-guard landed, case count in claim range) |

CU-1's watcher and EX-25's revision log cover the same window and add
`68e30768…` (selftest 15/15), `ec2b2d48…` (`--require-paths` registered; the
README still lacked it — CU-1 N1) and `57dffff1…` (selftest 21/21, `--require-paths 5`
returns the declared `USAGE` exit 2). Union observed this round: **≥11 distinct
revisions**. CN-1's timeline is `receipts/tool-revision-watch.txt`; the union is
the revision map the record needs.

Consequences, reconciled rather than flagged as defects:

1. **Receipt self-pins diverge by design.** The round's pre-pair receipt
   (`claims/c2/receipts/config-pre-pair-v2r3.txt:3`) self-pins `112d01dc…`; a
   post-pair captured by the landed tool will self-pin the landed sha. Each
   receipt pins *its own writer* — that is the v2 contract, not a
   contradiction. But the round record must carry this revision map so the
   pre-pin is not read as the landed tool (the round-2 D8 handling).
2. **The claim's "selftest 15 → ≥17"** is satisfied at `03bd6242…` (21 cases);
   it was still 15 at `08fb6833…` (EX-25 §5 measured) — the flip happened
   between those revisions. Any record sentence must name the revision it
   counted.
3. **`verify` between a pre receipt and a post receipt compares receipt
   fields, not tool versions**, so "live pre/post pair MATCH 5/5" stays
   measurable across the churn; the sentence should name both writer revisions.
4. **Rule #14 in practice**: the landed sha256, the registry-row clause
   ("15 fixture cases", the exit map) and the receipt self-pins must all be
   re-derived *after the last revision* — the row and README clauses are
   revision-pinned prose. CN-1's `receipts/tool-revision-watch.txt` is the
   timeline; the parent should re-derive at the commit revision.

### 3f. Standing-rule vs measured state: the `/tmp` EDQUOT premise does not reproduce this round

The freeze repeats the standing rule "scratch under `/var/tmp` or `/dev/shm`
(`/tmp` EDQUOT — standing)", and the r1 EVM entry's recheck line records a
`/tmp`-defaulted probe failing with EDQUOT (errno -122). Measured state at
round-3 time (CU-1 `A7`, re-checked by CN-1 read-only):
`df -h /tmp` → tmpfs 16G, **93M used (1%)**; `findmnt -no OPTIONS /tmp` →
`…,usrquota`; CU-1's 50 MiB `dd` to `/tmp` succeeded at 13:08Z.
Reconciliation: the r1 statement is dated history (and remains the reason the
recipes carry a disk-backed `TMPDIR`); the rule is a discipline, not a current
environmental fact. **No contradiction** — but any round-3 sentence asserting
"the host's `/tmp` fails this probe" as a *current* fact would contradict the
measurement and must be written as the r1-dated observation it is. CN-1 did not
write to `/tmp` under any circumstance (rule respected; read-only checks only).

Addendum (same premise, two different statements that only look contradictory):
the revised custody-pair tool now **enforces** the rule as policy — EX-21 A7
measures an explicit `--scratch /tmp/...` refused as `USAGE` exit 2 even though
the directory would accept a write. So "the host rejects `/tmp` writes" (false
at round-3 time) and "this instrument refuses `/tmp` scratch" (true, by
declaration) must both be quoted with their subject; the second is a tool
contract, not an environment measurement.

### 3g. **CONFIRMED COLLISION** — C2's drafted registry-row rewrite breaks one C3 entry

Measured, not predicted. CN-1 rebuilt C2's drafted rewrites from EX-30's own
scratch outputs (`/var/tmp/ex30/SKILL.v1.md` sha256 `8efd8a87…` and
`/var/tmp/ex30/README.v1.md` sha256 `a82d0071…` — both re-derived and equal to
EX-30's claims) and evaluated **C3's landed 57-entry table** against them with
the probe's own check semantics (`c2-vs-c3-collision.py`: replicates
`probe:168-259` including `re.M`, `window`, and `rev` target resolution;
control over unmodified HEAD reproduces the probe's clean result = **0
findings**, so the evaluator is calibrated).

| world | findings |
|---|---|
| unmodified HEAD (control) | **0** |
| C2's drafted SKILL.md row + README rewrite, C3's landed table | **1**: `skill-registry-custody-pair-row` → `citation_dead` |

The entry (`kind: anchor`, file `SKILL.md`, must_match
`precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH`)
requires the round-2 precedence chain verbatim; C2's drafted row writes the
revised chain `CONTENT-DRIFT > UNEVALUABLE > ABSENT > REWRITE-DRIFT >
METADATA-DRIFT > MATCH` (the new exit 14 class — declared by the tool itself at
the landed revision). Both texts are individually correct; together they cannot
both hold.

Consequences and reconciliation options (parent's call):

1. **C3 re-anchors that one entry** to a revision-stable form (e.g. anchor the
   map's class list or a prefix that survives added classes) and re-pins
   `expected.json` in the same commit — the F3 coupling the C3 claim already
   grants. Cheapest, keeps both chains' semantics.
2. **C2 keeps a compatible substring** in the row (e.g. naming the precedence as
   "CONTENT-DRIFT first, UNEVALUABLE before ABSENT, …" — anything that still
   contains the pinned string) — possible but writes the old chain into a row
   whose purpose is the new one.
3. **Serialize the landings**: C2 lands first, then C3 re-derives the anchor and
   digest before the commit.

The collision is **structurally forced**, not optional: the round-2 row states
"15 fixture cases" and a three-class worst-finding map with no exit 14, while
the landed tool declares 22 cases and `14 UNEVALUABLE`; leaving the row
unchanged is itself the stale-self-identity class rule #14 names (and the C2
claim requires the coupled landing). So the *anchor* is the thing that must
move, whichever chain moves it.

Pre-registered gate for the parent: if both land as currently drafted, the
probe at the work commit will read **findings = 1** (`citation_dead`,
`skill-registry-custody-pair-row`) — exactly the C3 acceptance clause's failure
mode. Re-run the probe after landing; CN-1's evaluator is the cheap predictor,
the probe is the authority.

State snapshot at 13:15Z (re-derived): table `bfc42f1b…` + expected `d97dd60a…`
(pin MATCH), probe `findings=0` both modes, selftest 13/13; custody README
`f30df42e…` (185 L) with all four convention anchors green; tool `7cd19c3c…`
(1155 L); SKILL.md `c134afcb…` with the **round-2 row still in place** — i.e.
the collision has not fired yet, and fires exactly when the row lands.

Also measured: **the four custody-README anchors survive C2's README rewrite**
(`MTIME_UTC_RENDER`, `Rewrite identity is \`INODE\` + \`CTIME\``, `Severity
precedence for the verdict of a \`verify\` run`, `never \`/tmp\``) — the
collision is confined to the SKILL.md row.

Stale-verification note (both chains): EX-30 §9 attack 1 asserts "the probe's
only `SKILL.md` entry is an unpinned sibling-row anchor" — true against the
31-entry table, false against the landed 57-entry table (six SKILL.md entries
now: 246/248/252/254 + three row anchors). Each chain's local "no interaction"
verdict is revision-stamped to the other chain's *previous* revision; the
post-landing re-run is the only valid statement.

## 4. Discrepancies, scope items, and non-contradictions

1. `expected.json` line count: CN-1's `wc -l` reads **0** (one line, no trailing
   newline); round-2's CN-1 `baseline-pins.txt` recorded `lines=1`. Method
   difference, not a file difference — the digest matches both rounds
   (`ff47bfd6…`). Recorded so nobody "repairs" a phantom.
2. Round-2's `compare N/300` TOCTOU and the D1–D7 debt taxonomy are **not**
   re-measured by CN-1; the before-states are re-measured by C2's EX-22/EX-29
   and agree with the round-2 records (see §2).
3. The custody drift (§3a) is operator-side by attribution (the file is the
   live kimi client's config; the wave neither writes nor can prevent it).
   It must be quoted in the round record as measured, not repaired.
4. No cross-chain reading has been found contradictory as of 13:1xZ.

## 5. Re-check queue (what CN-1 re-measures when each chain lands)

- C1 landing: new knowledge file digest + map-row line-neutrality (README stays
  190 physical lines; map section 57 lines) → command A 83/83 at the work
  revision; prior-82 slice byte-identical vs `knowledge-digests-t0.txt`.
- C2 landing: custody-pair.py new sha256 self-pinned in receipts; selftest
  ≥17 exit 0; the registry row's "15 fixture cases" clause re-derived in the
  same commit; SKILL craft slice unchanged (`173b8627…`); census PASS re-run;
  live pre/post pair + CN-1's own independent pair re-verify.
- C3 landing: `EX-46/pin-check.py` → MATCH; probe both modes → findings 0;
  selftest 13/13; entries 31 → N counted mechanically; `frozen_run` metadata
  unchanged; new entries' needles verified against HEAD content.
- Post-landing: all four instruments re-run at the work revision; custody
  watcher result appended.

*Written 2026-10-19T13:1xZ; §2 rows and §5 outcomes are appended as seats land.
CN-1 does not claim byte-identity of this report; it re-derives every number it
quotes.*