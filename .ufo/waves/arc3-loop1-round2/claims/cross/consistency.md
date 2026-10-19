# Cross-chain consistency sweep — arc3-loop1-round2 (SEAT CN-1, chain cross, connector)

Scope (frozen seat line): the three chains' instrument readings must not
contradict — (i) census PASS baseline identical across chains, (ii) custody pair
digests match the 5 paths, (iii) command A readings consistent. Reconcile or
flag at `claims/cross/consistency.md`.

Method: every shared instrument was re-run **independently by CN-1 before
reading any round-2 seat artifact** (first capture 12:00:06Z at HEAD
`14b1682b1128d2e41085ebc79c9addeb8786d420`), then re-measured on the landed
targets as they appeared. All CN-1 work is read-only over the repo and the
operator paths; scratch under `/dev/shm/cn1r2`; no git mutations; the two
authorized real-target writers this round are EX-16 (C2, the census file) and
EX-31 (C3, new files under `.ufo/gates/custody-pair/`) — CN-1 wrote neither, and
touched no custody path except hash/stat reads.

Baseline artifact: `claims/cross/CN-1/baseline.md` (+ `baseline/`,
`receipts/`).

## 1. Baseline — the shared numbers every chain is checked against

| Reading | CN-1 command (cwd = repo root) | CN-1 result |
|---|---|---|
| HEAD | `git rev-parse HEAD` | `14b1682b1128d2e41085ebc79c9addeb8786d420` (round-1 records commit) |
| command A (recipe `SCORECARD.md:92-124`, REV=`14b1682…`) | inline recipe, verbatim | `{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "14b1682…", "rule_blocks": 13}` → **82/82, 13/13, 10.0/10.0** |
| census (instrument `6f1d19ff…`, 490 L) | copy of the committed gate, `--root .` | `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0; counts **PROVINCE 162/6 · SCORECARD 1417/9 · SKILL 371/2**; `current_ok` blocks 5 |
| citation-drift probe (`e2665074…`, table `738b3a56…`) | copy, `--selftest` / `--root . --rev HEAD [--strict]` | `SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`; `reported findings=0 exit=0`; `clean findings=0 exit=0` |
| custody 5-path | `sha256sum` + `stat` + C3 v2 capture | devin `16f496e6…263a4`, omp `38d2a1d0…926b`, kimi `8cbacd48…c38d`, bashrc `7d2ca28a…6598`, profile `6c6be761…4f30` — **byte-identical to every round-1 capture** (round-1 `cross/consistency.md` §1) |
| instrument identities | worktree == `git show HEAD:` blob | census `6f1d19ff…`, probe `e2665074…`, expected `ff47bfd6…`, table `738b3a56…`, PROVINCE `d075a3c6…`, SCORECARD `a7c72950…`, SKILL `483b0eba…`, README `6ac43e83…` |

## 2. Agreement matrix — chain records vs CN-1 re-reads

| Shared reading | Chain record | CN-1 independent | Verdict |
|---|---|---|---|
| command A before (82/82, 13/13, 10.0/10.0 at `14b1682`) | C1 `SC-1/command-A-before.txt`, `CR-1/command-a-head.txt`, `EX-04/receipts/t0-commandA.json`; C2 `records-drafts/LOG-entry-draft.md:137`; C3 `EX-18` (B0 ≡ S0) | identical JSON (modulo the `revision` echo and `HEAD` spelling) | **consistent** |
| census before (PASS 0/0/0/0, exit 0, counts 162/6 · 1417/9 · 371/2) | C2 `RV-8.md` §3 (`6f1d19ff…`), C3 `VZ-3/live-baseline-1201Z.txt`, `RV-12/independent-pre.txt` | identical verdict + counts; instrument sha matches | **consistent** |
| probe before (13/13; findings=0) | C3 `EX-38/base-probe-*.txt`; C1 `CR-1/citation-drift-head.txt`; C2 `EX-19` | identical | **consistent** |
| custody pre-pair 5/5 | CU-1 `capture-1201Z.txt` (+3 hash engines), VZ-4 `custody-pre.txt`, EX-33 `custody-live.v2.json`, EX-31 `capture-pre.txt`, RV-12 `independent-pre.txt` | identical 5/5 **and** identical inode/ctime/mtime_epoch per path | **consistent** |
| census after (landed `82fb807e…`, later `df9ffdf9…`) | C2 `EX-23` §5+addendum, `RV-4`, `EX-18`; C3 `EX-35`, `EX-36`; C1 `EX-04/receipts/t2-commandA.json` | ordinary run PASS 0/0/0/0 on both landed revisions; counts unchanged | **consistent (revision-stamped — §3a)** |
| custody after (v2 tool live) | EX-31 `capture-post.txt` (`MATCH 5/5 drift=0 exit=0`, tool `112d01dc…`), EX-33 pair audit, CU-1 §3b | CN-1's own pair at the settled tool: `capture` 5/5 exit 0; `verify <EX-31 pre> --live` MATCH 5/5 exit 0; `verify T0 T1` MATCH 5/5 | **consistent** |
| command A after (C1 slice) | EX-01 `rule14.patch.md` §3 (14/14), EX-04 t1/t2 (`14/14`) | reproduced byte-exact — §3b | **consistent** |

No contradiction found in any shared reading. Every discrepancy found is a
**scope/revision/wording** issue, listed in §4.

## 3. Cross-chain interaction checks (run by CN-1)

### 3a. The census instrument is a moving target inside this wave — revision-stamp every reading

The C2 real target was rewritten at least six times during the wave. CN-1's
60 s poller and direct hashes measured:

| time (UTC) | census sha256 (prefix) | lines | observed behavior on the **healthy** root |
|---|---|---|---|
| ≤12:01:56 | `6f1d19ff…` | 490 | PASS 0/0/0/0 (round-1 close, the baseline) |
| 12:05:56 | `2a89793a…` | — | mid-edit state (EX-33/EX-23 saw siblings `1431620f`, `9373964c`, `59975ae0`; `9373964c` crashed with a TypeError per `seats/EX-23.md:89-92`) |
| 12:06:56 | `82fb807e…` | 560 | PASS; tree-level floor (`current-ok loci=5, floor=1`); H1/H3 classes present |
| 12:10:56 | `c95a5cf3…` | — | per-file floor on **blocks**; CN-1 measured a healthy tree (and the real rule-#14 tree) reading `G2 … SUSPECT (SKILL.md=0)` → `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` → **FAIL exit 1** |
| 12:11:50 | `df9ffdf9…` | 601 | PASS; per-file floor on **asserts** (`PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; floor=1/file`); H1/H3 hold |
| 12:15:39 | `a4c16763…` | 603 | text-only delta from `df9ffdf9` (docstring + Usage line renamed v9 → v10-r9); battery byte-identical |
| 12:18:14 | `d0772ce8…` | 610 | still churning (header polish); battery byte-identical again |

The C2 chain's own reports enumerate the full set seen from inside the chain:
`6f1d19ff` → `1431620f` → `2a89793a` → `7b5a0e88` → `9373964c` → `a4553911` →
`59975ae0` → `82fb807e` → `076bd621` → `c95a5cf3` → `df9ffdf9` → `a4c16763` →
`d0772ce8` (`seats/EX-23.md:23-25,115-116`, `RV-4.md:19-23`, `RV-8.md`,
`CR-3.md`). Two of the transient revisions were genuine defects, both caught
in-chain: `9373964c` crashed (TypeError), and **`c95a5cf3` read a claim-blocking
`VERDICT: FAIL` on the *unmodified* HEAD tree** (per-file floor measured in
*blocks*; SKILL.md has 0 current-ok blocks because its live-matching dets sit in
an `info`-aggregate block) — CN-1 measured the same failure independently at
12:10Z before reading any C2 report, and `CR-3`/`EX-23` recorded it from inside
the chain. The landed det-level (assert) floor at `df9ffdf9`+ fixes it. CR-3
also measured that **four of the twenty SCOPE rows are legitimately zero-locus
(DATED rows)**, so a per-*row* floor false-positives forever — the granularity
question is now chain knowledge, not a guess.

**Behavior was stable across `df9ffdf9…` / `a4c16763…` / `d0772ce8…`** (the
last three revisions observed through 12:20Z): ordinary HEAD PASS 0/0/0/0, H1
absent-file FAIL `['UNREADABLE']`, H3 blind FAIL `['BLIND-INSTRUMENT']`, rule-#14
tree PASS, records tree PASS, scope-diff 0 flags. The instrument is being
*polished*, not re-semanticked — but the sha is the only way to say which
reading is which.

CN-1's own measurements on `82fb807e…` (12:07Z), `df9ffdf9…` (12:12Z) and
`a4c16763…` (12:17Z) are all green and behaviorally identical on the battery
below, but **they are different instruments**: the floor's counting basis
changed (blocks → asserts) between `82fb807e` and `df9ffdf9`, and on the
intermediate `c95a5cf3` basis the same healthy tree FAILed. Consequences for the
records:

1. Every census reading in every chain record must name the instrument sha that
   produced it. Readings taken at different revisions are **not comparable
   evidence** — this is the round-1 "revision-scoped command A" lesson (F5 in
   round 1) applied to the census.
2. The C2 after-leg is only complete if the final settled revision carries the
   H1/H3 classes and PASS on HEAD. The C2 chain is aware and re-ran on the final
   digest (`seats/EX-23.md:113-120`, `RV-4.md` §1) — the parent must re-run once
   more against the committed bytes (any later write is a new instrument).
3. **Measured at 12:17Z — the drafts and the worktree already disagree.** The C2
   records drafts declare the landed revision as `df9ffdf9…` (601 lines)
   (`c2/records-drafts/SCORECARD-section-draft.md:42,121`;
   `LOG-entry-draft.md:54,157`), while the worktree file is now `a4c16763…`
   (603 lines, mtime 09:15:39 −0300). The delta is text-only (first docstring
   line + Usage line renamed v9 → v10-r9; battery behavior identical), but a
   records commit that lands the `a4c16763` bytes while stating `df9ffdf9` is a
   stale self-identity claim — precisely the defect C1's rule #14 distills.
   Fix: re-derive the sha/line-count on the bytes actually committed and update
   the two draft lines (the drafts' own parent checklist at
   `LOG-entry-draft.md:185` already demands this).
4. A per-file floor is **fragile on this tree**: on the block-counting basis
   SKILL.md has 0 current-ok blocks (its loci sit in blocks whose disposition is
   `info`/historical), so "floor per file" can fail a healthy root. The landed
   basis counts asserts. Any future touch must keep the floor's *basis* in its
   own header, or the next reader will re-derive a different verdict from the
   same bytes. (The landed header itself records this: "a block-count floor
   false-FAILs the ordinary run".)

CN-1 battery on the measured landed revisions:

| injection | `82fb807e…` (12:07Z) | `df9ffdf9…` (12:12Z) | `a4c16763…` (12:17Z, current) |
|---|---|---|---|
| ordinary HEAD run | PASS 0/0/0/0 exit 0; counts 162/6 · 1417/9 · 371/2 | same | PASS 0/0/0/0 exit 0; same counts |
| SKILL.md absent | FAIL exit 1, `UNREADABLE: ['SKILL.md: FileNotFoundError']`, `['UNREADABLE']` | identical class/exit | identical class/exit |
| SKILL.md truncated (10 L) | FAIL exit 1, `['UNREADABLE']` | same class family | — |
| SKILL.md is-a-directory | FAIL exit 1, `['UNREADABLE']` | — | — |
| all needles neutered (PIN+VER+PTR) | FAIL exit 1, `G2 … SUSPECT (current-ok loci=0)`, `['BLIND-INSTRUMENT']` | same class | FAIL exit 1, `['BLIND-INSTRUMENT']` |
| PIN alone neutered (partial blindness) | PASS exit 0 — **the named H4 residual** | PASS exit 0 | — |
| rule-#14 tree (C1's real payload) | — | PASS, SKILL 385/2 loci | PASS, no declared class |
| records tree (all three drafts appended) | — | PASS 0/0/0/0 | PASS 0/0/0/0 |
| scope-diff vs baseline `6f1d19ff…` | rows 20/20, 0 added/removed/changed, `CREEP FLAGS: []`, exit 0 | identical | identical |

### 3b. C1's rule #14 — verified byte-exact, and the one way it can still break the claim

EX-01's patch text (`claims/c1/EX-01/rule14.patch.md`) was applied by CN-1 to
fresh scratch trees from `git show HEAD:` bytes — **both payload generations**,
because the artifact was revised mid-wave (v1 superseded in-seat; its own
`identity-final.txt` marks v1 history-only):

| generation | artifact sha256 | payload | patched SKILL.md | command A |
|---|---|---|---|---|
| v1 (superseded) | `7cd9e950…` (8,833 B) | 896 B, `a47dc38d…`, 13 lines | 385 L, `19057c13…` | 14/14 |
| **v2 (current)** | **`885fa537…` (11,084 B)** | **1,071 B, `6cc388cb…`, 15 lines** | **387 L, `a8170b96…`** | **14/14** |

All six identities **reproduced exactly** at CN-1's hand (payload bytes from the
markers, applied after `SKILL.md:239` per the anchor form), and for both
generations: lines 1-239 byte-identical, tail byte-identical, pure insertion;
command A `{"citation_resolved_rules": 14, "knowledge_files": 82, "mapped": 82,
"missing": [], "dangling": [], "rule_blocks": 14, "coverage_score": 10.0,
"depth_score": 10.0}`; census PASS with `SKILL.md lines=385/387, loci=2` (no new
locus); probe `clean findings=0` with SHONEN unrefreshed and refreshed. The
v1→v2 revision is documented in-artifact with the supersession marked — rule #14
practising itself. **Land v2** (`885fa537…` artifact; its `identity-final.txt`
carries the same three identities and instructs re-derivation at landing).

The count is not free: CR-1's incident-only candidate text (the honest form of
the frozen claim, citing only wave-tree paths) measures **13/14, `depth_score`
9.29** at CN-1's hand; adding one resolvable `corpus/knowledge/…` citation
restores 14/14. **The parent must land a rule text carrying a resolvable corpus
citation** (v2 does: `…-evm-real-solc.md:7`; the `EX-05/` fallback does;
CR-1's T1 does not). A rising denominator with a falling numerator is the one
way this chain's claim fails.

Exact post-append geometry (measured, both generations, for the SHONEN refresh):
at HEAD the craft content ends at line 239 with the `## Config custody` heading
at 242; under **v2** the payload occupies 240-254, blanks 255-257, heading moves
to **258** — so the craft content ends at **254** (v1: 252, heading 256).
EX-01's own report proposes exactly that refresh (`seats/EX-01.md:111`:
"`SHONEN.md:6` refresh (`81-254`, 14/14)") — independent agreement with CN-1's
measurement. SHONEN's existing `81-243` is a loose containing range; any refresh
value (`81-252`, `81-254`, EX-04's `81-249` from a shorter draft) keeps the probe
needle green while rule #13 stays inside it — but the landed value must match
the landed bytes.

### 3c. C1's append vs C2's probe needle — the SHONEN coupling, with teeth

`pointer-table.json` `shonen-skill-range` pins `SHONEN.md:6`'s extracted
`SKILL.md:(\d+)-(\d+)` and requires the range to contain rule #13's title
("A mitigation claim carries its natural control").

- After EX-01's append (rule #14 at 242-249, craft body to 252): the probe stays
  **clean findings=0** — rule #13 (233-241) is still inside `81-243`. Measured in
  CN-1's projection repo (`/dev/shm/cn1r2/proj`), with SHONEN unrefreshed **and**
  refreshed.
- Teeth test: a 12-line insert *before* rule #13 pushes it out of the stated
  range → `CITATION_DRIFT: citation_dead entry=shonen-skill-range … exit=1`. The
  needle is real, and this is the r10-class coupling (one instrument's edit
  staling another's needle) in its benign direction.
- **Text staleness is real even while the needle is green**: `SHONEN.md:6` says
  `SKILL.md:81-243` and "13/13". After the append the craft body ends at 252 and
  the count is 14. EX-04 rehearsed the same-commit refresh (`t2-refresh.txt`:
  `81-243`→`81-249`, `13/13`→`14/14`, "rules #11-14"); EX-01 proposes `81-252`
  (its patch's own geometry). Both keep the needle green; the parent must land
  one — **and the range must match the landed bytes, not the rehearsal** (the
  two rehearsals disagree by 3 lines because their payload lengths differ; a
  wrong end line reads as a stale self-identity claim under rule #14 itself).

### 3d. Records-commit pre-flight — all three chains' drafts, both instruments

CN-1 extracted the three chains' **literal** SCORECARD sections
(c1 `records-drafts/scorecard-section-draft.md` 84 L · c2 … 86 L · c3 … 106 L,
+279 lines total, SCORECARD 1417 → 1696) into a scratch root and ran:

- token scan with the census's own vocabulary (PIN / VER / PTR / CACHE /
  REA_GATE, `c1-census-v10.py:163-167`): **0 hits in all three sections** — the
  pin-free discipline holds in the appended text;
- census (`df9ffdf9…`) on the records tree: `VERDICT: PASS (0/0/0/0)`,
  `SCOPE-ERRORS: []`, `UNREADABLE: []`, `DECLARED FAIL CLASSES: []` — the
  append lands past the declared bound without creating an undeclared locus;
- the **combined** projection (records tree + EX-01's rule-#14 SKILL.md +
  EX-04's SHONEN refresh) in a scratch git repo: census PASS (SKILL 385/2,
  SCORECARD 1696/9) and the citation-drift probe `clean findings=0 exit=0` in
  both modes. This is the strongest seat-time evidence that the records commit
  will not break either instrument — and it covers the one coupling (C1's
  SKILL append) that round 1's equivalent pre-flight did not have to carry.

### 3e. C3's custody-pair — verified at the settled revision, attacks reproduce

- Gate dir ships exactly two files (tool `112d01dc…`, 889 L;
  `README.md` `fa484d57…`) — the mid-round `__pycache__` was removed;
  `.ufo/gates/__pycache__/` (other seats' imports, mtime 09:06:58) remains
  untracked and must be excluded from the commit.
- selftest `CLEAN cases=15 passed=15 failed=0 exit=0` (CN-1, fresh scratch).
- CN-1's own capture 5/5, exit 0; `verify --live` MATCH 5/5; EX-31's
  `capture-pre.txt` re-verified by CN-1 at the settled tool → MATCH 5/5 exit 0.
- **Same-content rewrite**: CN-1's clean form (same bytes, same inode, mtime
  restored exactly) is caught as `REWRITE-DRIFT … moved=ctime_ns`, exit 11 —
  the attack sha256-only custody cannot see. Temp+rename (inode moves) caught as
  `moved=inode,mtime_ns`. Both match EX-33's six-form matrix.
- **v1 compatibility**: the round-1 canonical receipt verified against live →
  `SHA256-CONTRACT: 5/5 paths agree`, five `LABEL-DEFECT` lines naming each
  path's local-time-as-`MTIME_UTC`, `VERDICT: METADATA-DRIFT … exit=12`. So
  "v1 receipts remain verifiable against the tool's sha256 fields" is true via
  the sha contract channel — **not** via exit 0; any record that reads a v1
  verification as "MATCH/exit 0" misstates the instrument (CU-1 A6 and EX-33 §
  both flag the same).
- Label fix confirmed on live bytes: devin/omp epoch `1792011200` renders
  `2026-10-14T20:53:20Z` under `MTIME_UTC_RENDER` with the local render recorded
  separately as `2026-10-14T17:53:20-03:00` (the v1 defect is gone, and
  reproduced as a *detected* defect on v1 input).

## 4. Discrepancies / flags (ranked)

- **F1 (revision churn, C2 — the round's central hazard, now concrete).** Six
  census revisions in ~10 minutes (§3a); readings are only comparable within one
  revision; one intermediate revision (`c95a5cf3`) FAILed a healthy tree on a
  per-file floor over blocks. **Measured at 12:17Z: the C2 records drafts pin
  `df9ffdf9…` (601 L) as "the landed revision" while the worktree file is
  `a4c16763…` (603 L)** — landing the current bytes with those records would
  state a stale instrument identity (the rule-#14 defect class, in the records
  of the chain that lands the census). Mitigation: the parent re-runs the full
  battery on the committed bytes and the records state the instrument sha they
  were taken with; the C2 after-leg must cite the revision that is actually
  committed. The C2 chain's own reports already name their revisions — this is a
  records-discipline flag, not a claim defect.
- **F2 (claim-vs-text, C1).** The frozen claim's incident-only citation form
  measures **13/14 (depth 9.29)**; only a text carrying a resolvable
  `corpus/knowledge/…` citation reaches 14/14 (§3b). Land EX-01's **v2** payload
  (or an equivalent with a corpus citation), or the depth claim fails on its own
  instrument. Note v1 was superseded mid-wave — do not land the v1 bytes with
  the v1 identity numbers.
- **F3 (same-commit coupling, C1↔C2↔SHONEN).** The SKILL.md append must land
  with the SHONEN.md:6 refresh in one commit, and the refresh's range end must
  match the landed craft geometry (rehearsals disagree: 249 / 252 / **254** —
  254 is the measured end for the v2 payload, §3b). The probe needle tolerates
  any of them while rule #13 stays inside the range — the risk is a *stale
  promotion-checklist text* (and a stale it-would-be range under rule #14), not
  a probe failure (§3c).
- **F4 (wording, C3).** v1-receipt verification exits 12 (METADATA-DRIFT) by
  design; "v1 receipts remain verifiable" must be read through the
  `SHA256-CONTRACT` line, not as exit 0 (§3e). Also: the chain-level
  `claims/c3/receipts/config-pre-pair-v2.txt` embeds tool sha `4862f642…` — a
  superseded mid-round revision; its digests still agree 5/5 with live under the
  settled tool, but the pair the claim means is EX-31's (`capture-pre.txt` /
  `capture-post.txt`, both `112d01dc…`). Name the pair by path in the records.
- **F5 (naming).** The claim and several drafts say "v11"; the shipped path is
  still `.ufo/gates/c1-census-v10.py` and the header dates its work "r9". Minor,
  but the records should either say "the round-2 revision of
  `c1-census-v10.py`" or the parent should rename in a later round — never
  silently mix.
- **F6 (hygiene).** `.ufo/gates/__pycache__/` is untracked residue (mtime
  09:06:58, not EX-31's); `custody-pair/__pycache__/` appeared mid-round and was
  removed by EX-31. The wave commit must exclude `__pycache__`/`*.pyc`.
- **F7 (instrument-state caution, re-stated from round 1).** The probe's
  `shonen-skill-range` needle passes by *content-anywhere-in-range*; it does not
  check the count ("13/13") or that the newest rule is inside the range's end.
  A green probe is not a fresh SHONEN — §3c.
- **F8 (claim scope, C2 — bound the universal quantifier).** The frozen claim
  says "every round-1 silent-PASS injection now reproduces as a declared FAIL".
  Read universally that is **false**, and CN-1 reproduced the two counterexamples
  on the landed census (`df9ffdf9…`):
  (i) **H2 — inline-marker excusal.** SKILL.md:20's live `rea-agents@6.7.0`
  changed to a fabricated `rea-agents@9.9.9`, nothing else: the pin reads
  `historical (inline marker)`, `STALE (0)`, `DECLARED FAIL CLASSES: []`,
  `VERDICT: PASS` exit 0 — silence unchanged.
  (ii) **H5 — gate-free version statement.** "The build shipped 6.7.0 last
  week." appended at SCORECARD EOF: no gate token → not a locus → PASS exit 0.
  Both are exactly what EX-16's landed header names as still open
  ("H2 same-line inline-marker excusal; t5 DATED-shelter …; H4
  self-certification"), so the header is honest — the **records text** is what
  must not inherit the universal form. Honest form: "the two named round-1
  injections (H1 absent-file, H3 blind) reproduce as declared FAILs; H2/H4/H5
  remain open, named by the landed header." The round-1 tree's other items were
  H4 (external audit — the certificate the claim itself names) and H6 (a
  comment-rationale item, not a silent PASS).

## 5. Open items / what CN-1 could not close

- **C1's landed text** — parent-side (SKILL.md is patch-text-only this round).
  CN-1 verified the candidate byte-exactly; the landed bytes must be re-derived
  at landing and the SHONEN range re-derived from *those* bytes.
- **Final census revision** — `df9ffdf9…` was stable from 12:11:50Z through CN-1's
  last check; if the parent's landing touches it again, the battery in §3a must
  be re-run (it is scripted: `/dev/shm/cn1r2/sim-h1h3.py` + the injections in
  §3a's table).
- **Their own after-readings at the records commit** — structurally parent-side
  (the commit does not exist during the wave); §3d is the seat-time pre-flight.
- **Custody zero-drift into the close** — CN-1's T0/T1 are 12:04/12:13Z; a
  final capture at close is the parent's (the round-1 pattern).
- **The 17.7MB/91.6MB PE threads** are not this round's claims and were not
  re-run; no seat artifact contradicts them.

## 6. Reproduction (CN-1 commands)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
git rev-parse HEAD                        # 14b1682b1128d2e41085ebc79c9addeb8786d420
# command A: inline recipe from SCORECARD.md:92-124 with REV=14b1682…
python3 /dev/shm/cn1r2/gates/c1-census-v10.py --root .            # baseline v10 copy
python3 .ufo/gates/c1-census-v10.py --root .                      # landed revision
python3 /dev/shm/cn1r2/gates/citation-drift/citation-drift-probe.py --selftest
python3 /dev/shm/cn1r2/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict
python3 .ufo/gates/custody-pair/custody-pair.py capture --out /dev/shm/x.txt --label re
python3 .ufo/gates/custody-pair/custody-pair.py verify /dev/shm/x.txt --live
# projections: /dev/shm/cn1r2/{simrepo,simrepo3,simrepo4,proj,records,cases/}
```

CN-1 is a connector seat: no repo file change is proposed by this sweep. All
findings are flags for the parent's integration and for the chains' records.
