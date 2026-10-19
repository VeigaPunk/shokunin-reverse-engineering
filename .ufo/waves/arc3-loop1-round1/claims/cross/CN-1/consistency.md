# Cross-chain consistency sweep — arc3-loop1-round1 (SEAT CN-1, chain cross, connector)

Scope (frozen seat line): the three chains' before/after measurements must not
contradict — (i) command A readings, (ii) custody pre-pair claims, (iii)
instrument states (citation-drift probe, census v10). Reconcile or flag.

Method: every shared instrument was re-run **independently by CN-1 at HEAD
`e845c2b524ad2e59871e004c51a1386e192a74ab`** *before* reading any seat
artifact, then diffed against each chain's recorded readings; then the
post-integration surface was projected against the census instrument in an
isolated root (`/dev/shm/cn1/root`, scratch outside the repo). Nothing in the
repo was written except this artifact and the seat report. All tool runs are
read-only over the repo/operator paths (no git mutations, no installs, no
custody writes).

- HEAD pin: `git rev-parse HEAD` → `e845c2b524ad2e59871e004c51a1386e192a74ab`.
- Scratch: `/dev/shm/cn1` (not `/tmp` — `/tmp` is tmpfs+usrquota and the user
  quota is exhausted, EDQUOT on plain writes; corroborated by EX-02 §8,
  EX-26 §5, EX-30 §5, EX-11 §5; the standing hazard already at `SCORECARD.md:990`).

## 1. Independent CN-1 baseline at HEAD (before reading seat artifacts)

| Reading | CN-1 command (cwd = repo root) | CN-1 result | Output sha256 |
|---|---|---|---|
| command A (recipe `SCORECARD.md:92-124`, REV=`e845c2b…`) | inline recipe, verbatim | `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [], "revision": "e845c2b524ad2e59871e004c51a1386e192a74ab", "rule_blocks": 13}` | (one-line JSON, 194 B) |
| probe selftest | `python3 <copy>/citation-drift-probe.py --selftest` (copy in /dev/shm) | `CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0` | — |
| probe at HEAD | `… --root <repo> --rev e845c2b… --snapshot-dir /var/tmp/arc2-l10r10-C2/frozen --strict` | `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` | — |
| census v10 at HEAD | `python3 <copy>/c1-census-v10.py --root <repo>` | `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; counts PROVINCE 162/6, SCORECARD 1336/9, SKILL 371/2; live anchors `{'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}` | — |
| custody 5-path | `sha256sum` over the 5 paths | devin `16f496e6…263a4`, omp `38d2a1d0…926b`, kimi `8cbacd48…c38d`, bashrc `7d2ca28a…6598`, profile `6c6be761…4f30` | — |
| snapshot digest | `sha256sum /var/tmp/arc2-l10r10-C2/frozen/config-toml-landmarks` | `387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154` = `expected.json` `snapshots.config-toml-landmarks` | — |
| baseline pins | `git show HEAD:<path> \| sha256sum` | PROVINCE `d075a3c6…`, SKILL `5c93c7c1…`, SCORECARD `30129a98…`, census `36e96cd5…`, probe `3067621a…`, expected `4e28ba90…`, table `738b3a56…` | knowledge-sha256 list: `d4416283…` (81 .md + .gitkeep) |
| non-vacuity (own `classify()`) | imported the instrument's `classify`+`SCOPE` from a /dev/shm copy | `total_loci: 17  scope-None asserts: 0` | — |

Command A before-state also pinned for later diffing: per-file sha256 of all 81
`corpus/knowledge/*.md` at HEAD (`/dev/shm/cn1/baseline/knowledge-sha256.txt`,
sha256 `d4416283…`), coverage-map section sha256 `0c67285c…` (81 unique tokens),
`corpus/README.md` `7c0cf671…`, `SKILL.md` `5c93c7c1…`.

## 2. Agreement matrix — chain records vs CN-1 re-reads

| Shared reading | Chain record (seat) | CN-1 independent | Verdict |
|---|---|---|---|
| command A before (81/81, 13/13, 10.0/10.0) | C1 `claims/c1/EX-11/command-A-before.txt`; C3 `claims/c3/EX-30/recipeA-t0.txt`; SC-3 draft notes | identical JSON (after dropping the `revision` echo) | **consistent** |
| probe selftest before (11/11 exit 0) | C2 `claims/c2/EX-25/logs/before-selftest.txt` | identical | **consistent** |
| probe findings at HEAD (0, exit 0) | C2 `claims/c2/EX-25/logs/before-probe.txt` (non-strict) | identical (strict run also clean) | **consistent** |
| probe file digests before | C2 `claims/c2/EX-25/logs/before-sha256.txt`, `claims/c2/RV-6/pre-state-hashes.txt` (expected `4e28ba90…`, table `738b3a56…`, probe `3067621a…`, SKILL `5c93c7c1…`) | identical; worktree == HEAD blob for all four | **consistent** |
| census before (PASS 0/0/0/0, exit 0) | C3 `claims/c3/EX-26/census-at-HEAD.txt` (+ .exit, .json, rerun, quiet; 4-way capture agreement EX-26/EX-29/SC-6/RV-11, sha `3b677b8e…`) | identical verdict + counts; independent non-vacuity `scope-None asserts: 0` | **consistent** |
| custody pre-pair 5/5 | CU-1 `claims/cross/receipts/config-pre-pair.txt` (+metadata); EX-01 `claims/c1/receipts/config-pre-pair.txt` (3 independent hash impls); EX-02 `claims/c1/EX-02/custody-pre-pair.txt`; EX-15 `custody-T0.txt`/`custody-T1.txt`; EX-26 `custody-sha256.txt` | identical 5/5 | **consistent** |
| custody post-install zero drift | EX-02 `custody-post-pair.txt` (`CUSTODY DIFF: EMPTY`); EX-01 recompute 09:59:53Z; EX-15 T1 | identical 5/5 at CN-1 capture time | **consistent** |
| census instrument unchanged | EX-30 poll T0 marker `36e96cd5…` | `sha256sum .ufo/gates/c1-census-v10.py` = `36e96cd5…` (EX-28 not yet landed) | **consistent (pending EX-28)** |
| real-bytecode probe K/K | C1 primary carrier EX-06 `claims/c1/EX-06/evidence/{planted-K.json,run-hex-6.7.0.json,run-raw-6.7.0.json}` (KdxToken, K=6); replication RV-2 `claims/c1/RV-2/probe-runtime-{hex,raw}-6.4.0.json`, `probe-runtime-hex-6.7.0.json` (Rv2Token, K=5); EX-07 `ex07-reconcile-rv2.txt` | extracted independently by CN-1: KdxToken 6/6 (planted == hex == raw == probe, `dispatch: abi`, bytecode sha `9c40940e…`, artifact sha `69a15782…`); Rv2Token 5/5 on raw+hex, bytecode sha `c1081a56…`; EX-07's independent M1 dispatcher parse + M2 pure-Python keccak agree with all probe offsets | **consistent** |

## 3. Cross-chain interaction checks (projections run by CN-1)

**(a) Census scope vs C2's SKILL.md registry-row edit — PASS, no scope impact
(verified with the real patch text).**
Applied C2's actual patched file (`claims/c2/SC-4/scratch/patchtest/SKILL.md`,
sha256 `fa94a4696ce68f96c8cdf717ac6d270ca7f0df5a4b590585bdedec95ff1628c5` —
matches SC-4's claimed whole-file hash; 371 lines, line-neutral) plus C1's
SCORECARD draft block into an isolated root copy (`/dev/shm/cn1/root`): census
`VERDICT: PASS (0/0/0/0)`, `SKILL.md lines=371 loci=2` — the SKILL.md locus set
is unchanged. Reason: the registry is at `SKILL.md:361+` and the census's
SKILL.md scope is lines 10-16/18-20; the patched row carries no gated token (no
`6.x.y`, no `rea-agents@`, no `path.json:line` pointer). A CN-1 simulation of the
same edit earlier gave the identical result.

**(b) Census scope vs C1's records-commit SCORECARD section — PASS as drafted,
but a demonstrated FAIL hazard for the final fill.**
Appending the SC-3 draft's pasteable block
(`claims/c1/records-drafts/SCORECARD-section-draft.md`, 59 lines, `[[FILL]]`
placeholders) to a projected SCORECARD: `VERDICT: PASS (0/0/0/0)` — the draft
carries no gated token. Injection test (variant C): a realistic final-form
sentence *"the probe was executed through the npx cache of `rea-agents@6.4.0`
on this host"* appended to the new section flips the census to
`VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)` with
`SCORECARD.md block 1397-1398 [scope None]  :1398 [pin] None=6.4.0 -> AMBIGUOUS`.
Control: the same sentence with an inline `historical` marker is labelled
historical and escapes (variant B, PASS) — that is the instrument's declared
escape hatch (`c1-census-v10.py:344-345`), not a repair.
**Rule for the parent at integration: any `6.x.y` token or `rea-agents@` pin in
the new SCORECARD section must be absent, explicitly marked historical, or the
census scope re-keyed to cover the section — otherwise the records-commit census
FAILs undeclared.** (This is exactly the C3-after / C1-integration coupling.)

**(c) Command A is a shared instrument; "unchanged" must be revision-scoped.**
C1 moves command A 81→82 (new knowledge entry + map token, after-state owned by
parent integration). C2's edit surface is `.ufo/gates/citation-drift/*` +
`SKILL.md` registry row (line 361+), C3's is `.ufo/gates/c1-census-v10.py` — both
outside recipe A's read surfaces (recipe A reads `corpus/knowledge/`,
`corpus/README.md` coverage-map section, `SKILL.md` **queue-drain craft section**,
lines 81-241 at HEAD). So C2/C3 "command A unchanged" is consistent **only if
read as "no change attributable to C2/C3"**; at the records commit the shared
reading is expected to be 82/82 with 13/13 rules. Any C2/C3 record that states
81/81 as the records-commit reading, or any C1 record that states 82/82 before
the knowledge entry lands, is a contradiction — none exists as of this writing.

**(d) C2's pointer-table digest pin vs integration order (hazard, not yet
falsifiable).** `expected.json` currently pins a digest for
`snapshots.config-toml-landmarks` — and **0 entries in `pointer-table.json`
reference an `@` target** (`grep -c '"target": "@'` → 0), so that pin is inert
metadata (matches arc2-loop1-round10 `R2.md:183-187`). C2's new pin on
`pointer-table.json` will be the first **live** digest pin. Consequence: if
`pointer-table.json` is modified after the pin is computed (e.g. new entries for
C1's landed knowledge entry, or a re-pin), the pinned digest must be recomputed
in the same landing, else the declared preflight class (exit 2) fires at the
records commit. Flagged for the parent's integration order.

**(e) C3's claim framing is PASS→PASS, not FAIL→PASS (discrepancy in the frozen
text, already flagged by EX-26; CN-1 corroborates).** The frozen C3 "before"
(`claims-frozen.md:69-70`, "FAIL undeclared=2 …") is a round-3-era reading
(`SCORECARD.md:850-852`: "FAIL undeclared=2 at 766-line HEAD vs PASS at 701-line
`b21c0da`"); the round-4 v10 re-key closed it (`SCORECARD.md:908`, `:990`,
`:1096`). At current HEAD the census is PASS 0/0/0/0 (CN-1 + EX-26/SC-6/RV-11/
EX-30). So the E22 disposition is "measured at HEAD: already resolved by the r8
re-key; no re-key needed", and the claim's discriminating power rests on the
disposition record in the instrument header, not on a verdict flip. The parent
should not manufacture a re-key to force a flip.

**(f) Instrument-state facts that must not be misread.** (i) `expected.json`'s
`frozen_run` block (rev `679af5d`, verdict `failed`, finding `citation_dead`) is
**unread metadata** — the probe script contains zero occurrences of `frozen`
(arc2-loop1-round10 `Z1.md:95-101`; re-verified by CN-1 `grep -n frozen
citation-drift-probe.py` → no output). It must not be cited as a live instrument
state. (ii) The committed snapshot pin is inert (§3d). (iii) The probe's default
semantics are "reported" (exit 0); `--strict` restores 0/1/2 — before/after
claims that mix the two modes must say which mode produced the exit code.

**(g) C1 carrier scope note (not a contradiction).** EX-02's smoke `.bin`
(creation code, 1370 hex chars) probes to **0 selectors**
(`claims/c1/RV-2/probe-EX02-smoke-bin-6.4.0.json`), while the real leg's runtime
objects probe K/K: primary carrier EX-06's KdxToken (K=6/6, `dispatch: abi`,
bytecode sha `9c40940e…`, planted == hex == raw == probe) and replication
RV-2's Rv2Token (5/5, decoded-bytecode sha `c1081a56…` identical across raw/hex
and client versions 6.4.0/6.7.0). EX-07's independent dispatcher-parse (own
disassembler; solc 0.8.37 emits the PUSH0 prologue `5f3560e01c`) and pure-Python
keccak methods agree with all probe offsets, and solc's own js-sha3 agrees with
the independent keccak on 7/7 full hashes. The claim's "K/K planted selectors"
must cite the **runtime** carrier, never the creation code (a creation-code
probe returns empty — real, recorded, and not a probe defect).

**(h) Before-state correction carried by C1 (EX-02 §6).** The host already had
an ambient global `solc` 0.8.37 (fnm node v24 tree) before the wave; the new
artefact is the receipted isolated prefix install (`solc@0.8.37`, tarball sha256
`0e1a1ab6…`, exit 0, `added 8 packages`). Consistency consequence: the corpus
entry and receipts should cite the prefix path (EX-02's recommendation; CN-1
concurs — otherwise the claim's provenance rests on an unpinned ambient binary).

**(i) Projected C1 landing end-to-end — command A arithmetic verified by
rehearsal.** CN-1 built a scratch git repo (`/dev/shm/cn1/simrepo`, base commit
`d58c829e…` = HEAD's `corpus/knowledge` + `corpus/README.md` + `SKILL.md`), applied
EX-13's real map patch (`claims/c1/EX-13/_scratch/README.patched`, one line at
`:38`) and added the entry under EX-13's landed token name, then ran recipe A at
the projected rev `5090fc8d…`:
`{"citation_resolved_rules": 13, …, "knowledge_files": 82, "mapped": 82, "missing": [], "dangling": [], "rule_blocks": 13, "coverage_score": 10.0, "depth_score": 10.0}`.
`git diff --name-status` base→projected: exactly one `A` (the new entry), 0
modified/deleted → **prior-81 byte-identical**; `README.md` 1 insertion/1
deletion, 190 → 190 lines → **line-neutral**. So the C1 after-shape is
arithmetically and mechanically reachable; what remains for the parent is the
real entry content + acceptance per `corpus/QUALITY.md`.

**(j) Entry-name coupling (must be one name).** EX-13's landed map token is
`2026-10-19-arc3-r1-evm-real-solc` (the "h3" variant; EX-13 rehearsed h1/h2/h3 +
v1/v2/v3 in `claims/c1/EX-13/_scratch/`, and the applied `README.patched` =
`b74b8d34…` carries h3). CN-2's records outline (`claims/cross/CN-2/records-outline.md` R5)
still carries the placeholder `2026-10-19-arc3-r1-evm-real-bytecode.md`, and the
C1 records drafts mention a third variant `2026-10-19-arc3-r1-evm-solc` in their
SC-3 notes (documenting the variant set, not a landed token). If the parent
lands a file whose stem differs from the map token, command A reads `missing` +
`dangling` (one each — demonstrated by RV-4's patch-only preview `295cd30a`).
Use EX-13's h3 token (the one already rehearsed in §3i) or update the map row
and the file together.

**(k) Probe vs the combined C1+C2 text edits — clean (projection).** CN-1 built
a faithful subset projection repo (`/dev/shm/cn1/proj`, all 20 surfaces the
pointer table cites, `git show HEAD:<f>` verbatim; base `ff96ce5f…` → probe
`clean findings=0 exit=0`), then applied **C1's real README map patch** (EX-13,
sha `b74b8d34…`) **and C2's real patched SKILL.md** (SC-4 patchtest, sha
`fa94a469…`) and re-ran the HEAD probe against the byte-stable table at the
projected rev `32456843…`: `clean findings=0 exit=0` (strict) and `reported
findings=0 exit=0` (default). The table's README entries pin lines 22/175 and
the SKILL.md entry is an anchor — neither is touched by the two line-neutral
edits, so no citation breaks. Residual: this projection uses the HEAD probe;
EX-16's landed probe must reproduce the same 0-findings result at the records
commit (C2's after-leg).

**(l) Alignment with the sibling connector's contract (CN-2).** CN-2's records
outline (`claims/cross/CN-2/records-outline.md` §6) states the same single-source
numbers this sweep measured, names the same line-shift couplings (§6.2 —
`readme22/readme175` pins vs the line-neutral map-row edit; `skill-registry-row`
anchor unaffected by the citation-drift row edit), and §6.4 asserts the records
append does not introduce an undeclared census locus "per precedent (rounds
4-10)". CN-1's §3b gives the **condition under which that precedent fails** (an
unmarked `6.x.y`/`rea-agents@` token in the new SCORECARD section → FAIL
undeclared=1, reproduced) — so the parent should treat §6.4 as conditional and
run the census after the append, not before. CN-2 §6.3's digest coupling
(EX-16 lands probe + expected + byte-stable table) matches CN-1's F3. VZ-4's
roster census (`claims/cross/VZ-4/poll-log.txt`, `roster-census.sh`) is the
independent seat-delivery count; CN-1's §5 EX-03 gap note agrees with VZ-4's
draft ("EX-03 NEVER LANDED").

**(m) The census edit cannot trip the probe guard (peer-verified, corroborated
here).** CR-4 proved the disjointness two ways: the table's `entries`+`quoted`
resolve to exactly 14 files, none under `.ufo/gates/`, and the probe resolves
Git objects at `--rev`, never the worktree; a simulated honest census re-key
(blob `36e96cd5…` → `e39b1892…`) leaves the probe verdict invariant
(`findings=0`, strict clean) and the pinned table digest `738b3a56…`
byte-identical (`seats/CR-4.md` §1). This is the mirror image of CN-1's §3k
(C1+C2 text edits leave the probe clean) — together the two projections cover
the C1/C2/C3 edit surfaces against the C2 instrument. CR-4's ordering proposal:
`claims/c2/CR-4/proposed-ordering.md`.

**(n) C2 after-state — EX-16's real-target landing verified by CN-1 (10:16:16Z).**
The poll caught the write: `expected.json` `4e28ba90…` → **`ff47bfd6…`**, probe
`3067621a…` → **`e2665074…`**, `pointer-table.json` **byte-stable `738b3a56…`**
(all three re-hashed by CN-1; `git status` shows the two modified, table clean).
CN-1 then ran the after-battery against the landed target:

| check | command (CN-1) | result |
|---|---|---|
| selftest | `python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest` | `CLEAN cases=13 passed=13 failed=0 exit=0`; new cases `table_tampered` and `table_absent`, each exit 2 |
| probe at HEAD | `--root . --rev HEAD` (default) | `reported findings=0 exit=0` |
| probe at HEAD | `--root . --rev HEAD --strict` | `clean findings=0 exit=0` |
| pin present | `expected.json` `pointer_table.sha256` | `738b3a56…` = the live table's sha (coupling F3 satisfied at this point) |
| case table | `expected.json` `selftest` | 13 cases, ids as above |

Injection tests on /dev/shm copies of the landed files (real target untouched),
re-measuring the exact classes RV-6 found silent at HEAD:

| attack | before (RV-6) | after (landed, CN-1) |
|---|---|---|
| emptied `entries` (valid JSON) | silent `findings=0 exit=0` | `pointer_table_tampered … != pinned 738b3a56…`, exit 2 |
| every `must_match` weakened to `.*` | silent `exit=0` | `pointer_table_tampered`, exit 2 |
| one-byte table edit | silent (same class) | `pointer_table_tampered`, exit 2 |
| absent table | exit 2 `pointer_table_unreadable` | exit 2 `pointer_table_unreadable` (unchanged) |
| unpinned `expected.json` + tampered table | (new case) | exit 2 `pointer_table_unpinned` — **fail-closed**, resolving F6(i) |
| control (copies of the real pair) | — | `clean findings=0 exit=0` |

Verdict: **C2's after-legs measure as claimed** (selftest 11→13 at exit 0;
tampered/absent table → the declared preflight exit-2 class, never silent
findings; findings = 0 at HEAD). One row-vs-code mismatch survives: the landed
finding id is `pointer_table_tampered` while EX-20's row text says
`table_tampered` (the *case* name is `table_tampered`; the *finding* id is
`pointer_table_tampered`) — see F6(ii).

**(o) C3 after-state — EX-28's real-target landing verified by CN-1 (two writes).**
The census was written twice: blob `c39beccc…` at 07:17:44 then blob
`6f1d19ff…` at 07:18:16 (sha256 + `stat` by CN-1; `36e96cd5…` before). CN-1
measured **both** states against the real root:

- **Intermediate `c39beccc…`: FAIL.** `SCOPE-ERRORS (marker assertions):
  ['PROVINCE.md:40 marker line outside its own declared range 45-62 (G18)']`,
  `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 1. The
  header already claimed the row was "re-keyed to line 45", but the SCOPE entry
  still read `("PROVINCE.md", 45, 62, "DATED", 40, r"verified on this host
  2026-10-13")` — the newly added G18 assertion fired on the very row it
  documents.
- **Final `6f1d19ff…`: PASS.** Row now `("PROVINCE.md", 45, 62, "DATED", 45,
  r"2026-10-13")` (`PROVINCE.md:45` carries "(2026-10-13 receipt)" — the row's
  own dated receipt text); run → `VERDICT: PASS (stale=0 ambiguous=0
  undeclared=0 unresolved=0)`, `SCOPE-ERRORS: []`, exit 0.

Value of the transient: the intermediate state is a **live non-vacuity proof of
G18** — the assertion caught a genuinely un-re-keyed row (the exact class the
header says it repairs), which no seat had demonstrated on the real target.
CN-1 re-ran its projection with the NEW census (C2's patched SKILL.md + C1's
current SCORECARD draft in `/dev/shm/cn1/root`) → still `PASS 0/0/0/0`.
Residual: RV-11's absent-file fail-open (an absent `SKILL.md` → vacuous PASS)
is **not** addressed by the landed header (no mention) — see F7.

**Records-commit pre-flight (all three chains' drafts, new census):** CN-1
appended the pasteable blocks of the C1, C2 and C3 SCORECARD drafts
(`claims/{c1,c2,c3}/records-drafts/*scorecard*`, C3's extracted from its
`BEGIN/END LITERAL SECTION TEXT` markers) plus C2's patched `SKILL.md` into
`/dev/shm/cn1/root` (SCORECARD 1336 → **1549 lines**; none of the three drafts
carries a gated token — verified by the same regex family the census uses) and
ran the **landed** census: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0
unresolved=0)`, `SCOPE-ERRORS: []`, `UNDECLARED (0)`. This is the strongest
seat-time evidence that the records commit will not break C3's claim, and it
shows all three scribes' pin-free discipline holds in the appended text.

## 4. Discrepancies / flags (ranked)

- **F1 (claim-text vs measurement, C3):** before is PASS, so the claim's
  before→after is PASS→PASS. Precision from the peers' reproductions: the debt's
  own reading IS reproducible at the debt's revision — PL-3 and RV-11 re-ran the
  recovered v9 (`sha256 213fe679…`, recovered byte-exact from
  `.ufo/waves/arc2-loop1-round2/E22.md:264-692`) against `679af5d` (766-line
  card) and got **FAIL undeclared=2** at blocks 731-737 / 747-766 — but at
  current HEAD the census is PASS 0/0/0/0 (round-4 v10 re-key, re-verified from
  the `6bc4c29` diff: exactly 3 DATED rows +1). So the honest landing is a
  disposition-by-measurement, not a manufactured re-key. (EX-26 §3; CN-1 §3e.)
- **F2 (integration hazard, demonstrated):** an unmarked `6.x.y`/`rea-agents@`
  token in the new SCORECARD section → records-commit census FAIL undeclared=1.
  Repro in §3b; mitigation rule stated there.
- **F3 (integration-order hazard, C2):** table-digest pin must match the final
  `pointer-table.json`; recompute after any table edit in the same commit (§3d).
- **F4 (after-readings status): CLOSED for both real targets.** **C2's
  after-half is measured and verified by CN-1 against EX-16's landed target**
  (§3n: selftest 13/13 exit 0; tampered/absent/unpinned → declared exit-2 class;
  findings=0 at HEAD). **C3's after-half is measured and verified against
  EX-28's landed census** (§3o: final blob `6f1d19ff…` → PASS 0/0/0/0 exit 0
  with the E22 disposition in the header; the intermediate blob `c39beccc…`
  FAILed on its own new G18 — live non-vacuity proof). The records-commit
  pre-flight with all three drafts also PASSes (§3o). C1's after half (knowledge entry, map token, command A
  82/82, prior-81 byte-identical) is parent-integration work — CN-1 pinned the
  before-state digests (§1) so the parent's diff can be checked mechanically.
- **F5 (revision-scope wording):** any "command A unchanged" sentence in C2/C3
  records must be read as "no change attributable to this chain"; the shared
  records-commit value is expected 82/82 (§3c).
- **F6 (C2 landing-set consistency — the couplings the parent must resolve
  together):** (i) **RESOLVED by the landing:** the landed implementation is
  fail-closed on an unpinned baseline — `pointer_table_unpinned` → exit 2
  (CN-1 §3n), matching EX-20's row clause; the prototype's skip-on-unpinned
  shape (`seats/SC-4.md:73-77`) is superseded. (ii) **CONFIRMED against the
  landed code:** the row text says a digest-mismatched table yields finding
  `table_tampered`, but the landed **finding id** is `pointer_table_tampered`
  (the *case* name is `table_tampered`; the absent case is `table_absent` with
  finding `pointer_table_unreadable`). The row must be edited to name
  `pointer_table_tampered`, or it misstates the instrument it registers.
  (iii) **D1 was closed by EX-21's regeneration, but the changeset manifest is
  stale:** SC-4 measured the then-published diff (applies rc 0 but yields
  `ea364f2d…` ≠ EX-21's `probe.py` `776cef6a…`; 9/13, exit 1). EX-21 then
  regenerated it — CN-1 verified independently: EX-21's current
  `logs/proto-probe.diff` (sha `9d346018…`) applies cleanly to the HEAD probe
  and yields `794e57bc…` = EX-21's current `tmp/proto/probe.py`
  (`claims/c2/EX-21/logs/proto-hashes.txt`). SC-4's changeset manifest
  (`claims/c2/SC-4/changeset.md:33,41,107`) still carries the OLD prototype shas
  (`776cef6a…`/`376f9fc5…`) — the parent should take EX-21's current artifact
  and refresh the changeset row. (iv) **Two overlapping patches target the same
  row:** EX-20's row patch (file `fa94a469…`, row `08be1ec2…`) and EX-21's
  cell-4 patch (file `47ad6fdb…`, row `fa1496c9…`) both rewrite `SKILL.md:371`
  with different texts — the parent must land ONE merged row, not both.
  Landing an inconsistent set would make the SKILL.md registry row state
  semantics the instrument does not have, or ship a red selftest.
- **F7 (census fail-open, C3):** an absent `SKILL.md` yields `PASS exit 0`
  (`lines=0 loci=0`; `assert_markers` never fires for CURRENT-only rows) —
  RV-11 attack 3 (`seats/RV-11.md:93-96`), fix proposed as patch text for
  EX-28. Not a contradiction in the before-readings, but an instrument-state
  fact the C3 after-edit could close; if not closed, the disposition record
  should name it as a residual.

## 5. Open items / what CN-1 could not check

- **C2's after-state — CLOSED (verified):** EX-16 landed 10:16:16Z; CN-1
  re-ran the selftest (13/13 exit 0), the HEAD probe (0 findings, both modes),
  and the tampered/absent/unpinned injections against the landed files (§3n).
  Residual row-vs-code item: F6(ii).
- **C3's after-state — CLOSED (verified):** EX-28 landed 07:17:44Z/07:18:16Z
  local (blobs `c39beccc…` then `6f1d19ff…`); CN-1 ran both, verified the
  disposition header, the re-keyed `PROVINCE.md 45-62` row, and the
  records-commit pre-flight with all three drafts (§3o). Residual: F7.
- C1's after-state (knowledge entry, map token line-neutrality, command A
  82/82, prior-81 byte-identity) — blocked on parent integration; the before
  digests are pinned in §1 for mechanical checking, and the shape is verified
  by rehearsal (§3i) against EX-13's real map patch.
- **Seat-delivery gap that the records must not paper over:** `claims/c1/EX-03/`
  is still empty (CN-1 `ls`, 07:10) — its seat line's primary target
  (`token.sol` + `planted-selectors.txt`) never landed, and RV-1 executed its
  seat line against the three planted sets that did land instead
  (`seats/RV-1.md` §1, 16 polls + a 25-check poller). The wave's delivered
  count and RV-1's verification scope must be stated as measured (RV-1 verified
  EX-02's smoke set, RV-2's set and EX-06's planted set — not an EX-03 set that
  does not exist). EX-04 later landed its own `KdxToken` compile
  (`claims/c1/EX-04/token.runtime.bin`, sha-pinned in its compile receipt).
- **Time-label defect in the canonical custody receipt (digests unaffected):**
  CU-1's `config-pre-pair.txt`/`config-pre-pair-metadata.txt` print
  `MTIME_UTC`/ctime as local (-03) renderings; CN-1 reproduced EX-01's A4
  independently — `stat` epoch `1792011200` = `2026-10-14T20:53:20Z` =
  `2026-10-14 17:53:20 -03`, while the receipt prints `2026-10-14 17:53:20`
  under an `MTIME_UTC` label (3 h). The sha256s are the contract and are
  unaffected; the parent should carry EX-01's `mtime_epoch` form into any
  record that quotes times, and pass the label fix to CU-1 (label-only, no
  re-capture).
- One pre-existing dirty path (`.ufo/waves/arc2-loop1-round10/C3.md`, ` M`) is
  outside every instrument's scope; `?? .ufo/waves/arc3-loop1-round1/` is the
  wave's own untracked tree. A transient `?? .ufo/gates/__pycache__/` appeared
  during the wave and was removed by EX-26 at 07:03 (re-verified by CN-1:
  absent; porcelain back to the two pre-existing entries).
- **Bytecode-cache residue inside the wave tree (parent should exclude or
  note):** `claims/c1/EX-07/__pycache__/selector-recon.cpython-314.pyc` still
  exists (CN-1 `find`); SC-2 measured it as the one MISSING row of EX-14's
  manifest (deleted mid-wave) and proposes a generator exclusion patch
  (`seats/SC-2.md` §2, `claims/c1/receipts/manifest-crosscheck.md`). Any
  wave-artifacts commit should exclude `__pycache__`/`*.pyc`, and the
  manifest's one MISSING + six MISMATCH rows are explained by mid-wave live
  rewrites (`ctime > generated-utc`), not tamper.

## 6. Reproduction (CN-1 commands)

The `/dev/shm/cn1` scratch tree was removed at seat close (no residue; `/tmp`
was quota-blocked all wave). Rebuild is mechanical:

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git rev-parse HEAD                                    # e845c2b524ad2e59871e004c51a1386e192a74ab
mkdir -p /dev/shm/cn1/gates && cp -r .ufo/gates/* /dev/shm/cn1/gates/
# command A: inline recipe from SCORECARD.md:92-124 with REV=e845c2b…
python3 /dev/shm/cn1/gates/citation-drift/citation-drift-probe.py --selftest
python3 /dev/shm/cn1/gates/citation-drift/citation-drift-probe.py --root . \
  --rev e845c2b524ad2e59871e004c51a1386e192a74ab \
  --snapshot-dir /var/tmp/arc2-l10r10-C2/frozen --strict
python3 /dev/shm/cn1/gates/c1-census-v10.py --json      # default --root = repo
# projection tests (§3a/§3b/§3o): /dev/shm/cn1/root/{PROVINCE,SKILL,SCORECARD}.md
#   built from `git show HEAD:<f>`; the chains' draft blocks appended;
#   census --root /dev/shm/cn1/root
# after-state battery (§3n): copies of the landed gates files + injection variants
```

CN-1 is a connector seat: no repo file change is proposed by this sweep. All
findings above are flags for the parent's integration and for the C2/C3
after-seats.
