# R36W2CriticC2Verdict — rule on R36-C2 against the actual landed diff

Seat: critic (leaf, round 36 wave 2). Assigned question: the frozen `c2-counter.py` is met at
`d2e46ef5` and `ffc81341`; does the **actual** diff `cab59f22..01a44dbf` (`SCORECARD.md`,
`SHONEN.md`) contain any of the wave-1 shortcut shapes — duplicate keys, a second contradictory
statement, a decoy document, population shrink, a pointer swap — and what is the ruling under §9?

Everything below is read-only over committed git objects. Scratch
`/fast/scratch/hyaku/kaidoku-r36/R36W2CriticC2Verdict` (fixtures, reproductions, extracted trees),
`TMPDIR` set to it, removed at the end. No counter, claim, carrier, oracle, control or surface was
edited; the only file I wrote is this report. No tool installed; `pacman` untouched.

---

## 0. Ruling

**VERIFIED** — as to the conditions P36-C2 enumerates, at both revisions it names and at the
integration tip. No wave-1 shortcut shape is present in the landed diff: no duplicate unit keys, no
unamended second contradicting statement, no decoy target, no population shrink, no pointer swap.
Both committed receipts reproduce field-for-field from the frozen counter, the do-nothing control
cannot reach the target, and my own non-counter re-derivation (QUALITY 77's four requirements applied
to the landing) also passes.

**Not verified**, and this is the scope limit the ruling must carry: the *sentence's* universal lead-in
("carry zero mismatches with observed repo state") is broader than the enumerated set, and there are
three live counterexamples inside the landed surfaces that the frozen counter cannot see (§4). Two are
introduced or extended by this round; one is an evidence-custody gap at the final tip. Under §9 the
claim is judged on the counter, kill rule and predicate frozen before data, so these do not flip the
verdict — they bound what "verified" means and they are the reason QUALITY 77's successor must not be
read as satisfied by this round's green.

| question | answer |
|---|---|
| frozen counter met at `d2e46ef5` | **yes** — reproduced identical to `.ufo/waves/round-36/c2/after-at-d2e46ef5.json`, exit 0 |
| frozen counter met at `ffc81341` | **yes** — reproduced identical to `.ufo/waves/round-36/after/c2-at-ffc81341.json`, exit 0 |
| frozen counter met at the integration tip `01a44dbf` | **yes** — exit 0, 0 mismatches, `guards_ok`, 41 pointers (no committed receipt at this revision) |
| do-nothing reaches the target | **no** — rev=base gives 3 mismatches, exit 1 |
| any of the six wave-1 shortcut classes present | **no** (A4 has no live instance because the repaired documents are unique in the tree; the freeze's silence on intended documents remains a pre-freeze defect, now named in QUALITY 77) |
| honest-stop or unprovable | **no** — the target is met and it is re-derivable with one command over committed bytes |

---

## 1. Frozen inputs and reproducibility

| item | value |
|---|---|
| base | `cab59f221fe19726b5692bfa4d9a9679e96b8a73` |
| freeze | `790561d4e3aca732a434081aa9573ec2fa5fd7d0` |
| controls | `6a870b9290e9566468d7d9e6d1b8308daf025b12` (7 receipts, all `met_target: false`) |
| C2 measured revisions | `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`, `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` |
| integration tip | `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` |
| lane HEAD when read | `6f2ba761bb5bcd6482d45523379376dcb6a386f6` — adds only `.ufo/waves/round-36/{w1-results.json,w1/R36ReviewerQualityBar.md,w2-*,w2.ready}`; `git diff --stat 01a44dbf 6f2ba761 -- SCORECARD.md SHONEN.md` is empty, so the scored surfaces at HEAD equal the tip |
| counter | `tools/round-36/c2-counter.py` sha256 `f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f` at freeze `790561d4`, control `6a870b92`, `d2e46ef5`, `ffc81341`, `6f2ba761` and in the worktree — unchanged from freeze to tip |

```
$ for r in 790561d4 6a870b92 d2e46ef5 ffc81341 6f2ba761; do git show $r:tools/round-36/c2-counter.py | sha256sum; done
f079aff1…  (all five identical)
```

Reproduction of the two named receipts (JSON compared on every key except `argv`/`revision`):

```
$ python3 -I -B tools/round-36/c2-counter.py --root . --rev d2e46ef5… --base cab59f22… --json-out $S/repro-d2e46ef5.json
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "unresolved": []}   EXIT=0
$ python3 -I -B tools/round-36/c2-counter.py --root . --rev ffc81341… --base cab59f22… --json-out $S/repro-ffc81341.json
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "unresolved": []}   EXIT=0
repro-d2e46ef5.json IDENTICAL   repro-ffc81341.json IDENTICAL   (vs the committed receipts)
```

At the tip (no committed receipt exists for this revision — see L1):

```
$ python3 -I -B tools/round-36/c2-counter.py --root . --rev 01a44dbf… --base cab59f22… --json-out $S/tip.json
{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0,
 "revision": "01a44dbf…", "unresolved": []}                                                            EXIT=0
```

Unit/pointer counts by revision (counter's own `units()`/`pointers()`, imported unmodified):

| rev | units | owned | cap | shonen | pointers |
|---|---|---|---|---|---|
| `cab59f22` (base) | 15 | 3 | 8 | 4 | 34 |
| `d2e46ef5` | 15 | 3 | 8 | 4 | 36 |
| `ffc81341` | 15 | 3 | 8 | 4 | 38 |
| `01a44dbf` (tip) | **16** | 3 | **9** | 4 | **41** |

Do-nothing (`--rev cab59f22 --base cab59f22`): `mismatches 3`, unresolved
`[["cap:pre-registered two-lane live battery on REA 6.5.0","receipts-B/"],["shonen:No cross-domain bleed (PROVINCE.md still accurate)","ScoutSkillPlacement.md"]]`,
`O1 stated [116,116] vs observed [122,122]`, exit 1 — the frozen target is not reachable by doing
nothing (§9 last bullet). Selftest: `{"cases": 13, "green_ok": 1, "red_ok": 12, "failures": []}`, exit 0.

---

## 2. Shortcut-shape audit of the actual diff

`git diff cab59f22 01a44dbf -- SCORECARD.md SHONEN.md` is the scored change: SCORECARD `+`1 capability
row (`:627`), 3 rewritten Owned-axes cells (`:23` coverage, and its evidence/last-change cells), the
`receipts-B/` capability pointer, and SHONEN box 4's assertion line (`:12`, title at `:11` unchanged); plus a new `## Round 36` section
(`:3385-3397`) appended by the tip commit. SHONEN is 12 lines; there is no second surface.

| shape | how I tested it | result |
|---|---|---|
| **A1 duplicate unit key / shadow row** | enumerated every `\|` row in `## Owned axes` and every `\|` row in the whole `## Capabilities` section (`:615-633`, one contiguous block, 9 rows) and every `^- \[[^]]\]` box, keeping duplicates | **absent** — 3 owned / 9 cap / 4 boxes, zero duplicate first cells or box titles at base and tip. The new capability row has a distinct key. No row was appended with an existing key |
| **A3 second contradictory statement** | `findall`-style enumeration of every occurrence of each statement shape in the three surfaces, not just the first `re.search` | **absent for current-tense statements.** Each of the four counted phrases occurs exactly **once** and equals observed: `124/124 knowledge files mapped` (SCORECARD:23), `17/17 queue-drain rule blocks` (:24), `9/9 preselected reconciliation obligations` (:25), `17/17 rule blocks` (SHONEN:6). The additional `N/M` values in the coverage row are revision-anchored history (`122/122 at cab59f22`, `116/116 at c369242`, `109/109 at ebe2cb4a`, `78/78 at 3395b6d`, `107/107 at 7ef837a4`) — a different sentence shape, and I verified each at its own anchor (§3) |
| **A2 statement validated under a different key** | looked for any count/range statement in the scored sections that the counter's four+three hardcoded shapes do not read | **no live false instance** — the remaining `N/M` values are box 4's `207/153` and `0/207` (REA tool/command counts, not repo counts) and the history values above; the remaining ranges are `SKILL.md:77-191` (anchored to `a79945c4`, verified §3) and `PROVINCE.md:8-14` (the version paragraph, content checked §3) |
| **A4 decoy document** | searched the whole tip tree for every file whose basename is `ScoutSkillPlacement.md` or whose path segment is `receipts-B`, and listed files added in the range with either name | **absent** — exactly one of each exists (`git ls-tree -r --name-only 01a44dbf \| grep -E 'ScoutSkillPlacement\.md$\|/receipts-B/'`): `.ufo/waves/round-30/w1/ScoutSkillPlacement.md` (its own title: "where the round-30 SKILL.md section and PROVINCE.md Core addition go … and the SHONEN.md box-4 pointer check") and `.ufo/waves/luna-round-6/receipts-B/` (`MANIFEST.txt` + `leg-1..10.md`, the 10-leg B lane). Zero files with either name were added in `cab59f22..01a44dbf`. Each repair cites the only document with that basename, and each is the document the base sentence's own context names (`"… + `receipts-B/`"` beside `…/receipts/`; `"(w1 `ScoutSkillPlacement.md`)"` under a round-30 sentence) |
| **A5 population shrink** | `git diff --diff-filter=D --name-only cab59f22 01a44dbf`; plus independent recount of every population | **absent** — zero deletions under `corpus/`; knowledge files 122 → 124 (exactly the two added entries: `2026-10-26-r36-sasquatch-squashfs-recursion.md`, `2026-10-26-unblob-sasquatch-dependency.md`); mapped 122 → 124; rule blocks 17 → 17; resolved rules 17 → 17; pointers 34 → 41; no unit removed (`missing_units: []`) |
| **A6 pointer swap** (count, not identity) | per-unit backticked-token set delta base → tip, keeping every unit | **absent** — the only drops are the two repaired pointers (`receipts-B/` → `.ufo/waves/luna-round-6/receipts-B/`; `ScoutSkillPlacement.md` → `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`). The coverage row drops nothing: `.ufo/waves/round-31/w1/ScribeScorecardRows.md` is still cited at tip, and the added tokens (`plans/round-36-claims.md`, both entry paths, `tools/round-36/c2-counter.py`) all resolve. `pointers_not_fewer: true`, `unrepaired: []` |

---

## 3. Independent re-derivation (the stricter non-counter check the round says it rests on)

SCORECARD:3392 states the C2 verdict "also rests on a stricter non-counter re-derivation in wave 2".
I applied QUALITY 77's four requirements to the landing directly (`SCORECARD` rows + `SHONEN` boxes
extracted by my own parser; counts from the documented recipes run verbatim, not from the counter):

1. **Every occurrence of each statement shape.** Done in §2 (A3 row). Pass.
2. **Duplicate units kept as separate units.** 16 units at tip, no duplicates. Pass.
3. **Populations bounded below at the base.** knowledge 122→124, mapped 122→124, rules 17→17,
   pointers 34→41. Pass.
4. **Repaired pointer against the intended document.** The freeze does not name intended documents
   (pre-freeze defect); identity established two ways: (a) each basename is unique in the tree, (b) the
   base sentence's own context names the document (`receipts-B/` as the sibling of `…/receipts/`;
   `w1` of the round-30 sentence, whose note is about exactly that box-4 pointer). Pass on identity.

Observed state, computed without the counter:

```
$ documented recipe A verbatim at tip (SCORECARD.md:86-124)
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 124, "mapped": 124, "missing": [], "revision": "01a44dbf…", "rule_blocks": 17}

$ documented recipe B verbatim at tip
[{"stage":"baseline","revision":"66455858…","aligned":0,"total":9,"score":0},
 {"stage":"after","revision":"c265db9b…","aligned":9,"total":9,"score":10}]
```

| stated (tip) | observed (my run) | verdict |
|---|---|---|
| `124/124 knowledge files mapped` (SCORECARD:23) | 124/124, `missing []`, `dangling []` | ✓ |
| `17/17 queue-drain rule blocks … resolvable` (:24) | 17 blocks, 17 resolved, 0 bad refs | ✓ |
| `9/9 preselected reconciliation obligations` (:25) | recipe B after-stage 9/9 | ✓ |
| SHONEN box 1 `17/17 rule blocks` (:6) | 17/17 | ✓ |
| craft `SKILL.md:81-314` (:24, SHONEN:6) | heading line 81 `## Queue-drain craft …`, last non-blank 314, 315-317 blank | ✓ |
| Adjacent `PROVINCE.md:97-125` (SHONEN:12) | heading 97, last non-blank 125, next heading `### Round-4 additions to Core` 128 | ✓ |
| box 4 `PROVINCE.md:8-14` | lines 8-14 carry the `rea-agents@6.7.0` (207/153) surface summary | ✓ |
| box 4 `:116-118` safety refusal / `:119-125` round-36 tooling bullet / `:110-115` installer line | 116-118 Quality/safety verdicts; 119-125 `- **Tooling, dated 2026-10-26**`; 110-115 `- **Installing engines, Python packages …**` | ✓ (as ranges; see L2 for the content) |
| history: `122/122 at cab59f22`, `116/116 at c369242`, `109/109 at ebe2cb4a`, `78/78 at 3395b6d`, `107/107 at 7ef837a4` | 122/122, 116/116, 109/109, 78/78, 107/107 — each at its own revision | ✓ |
| history: baseline craft range `SKILL.md:77-191` at `a79945c4` | `[77,191]` at `a79945c4` | ✓ |
| coverage last-change cell `count refreshed rounds 25, 26, 31 and 36` (SCORECARD:23) | count cells rewritten at `d2e46ef5` (116→122) and `ffc81341` (122→124); round 31 recounted | ✓ |

So the multi-value coverage cell is **not** an unamended second contradiction: every number in it is
true at the revision it names. This is a stronger result than wave 1 could state and it is why A3 is
absent rather than merely unmeasured.

---

## 4. Live counterexamples (limits of the verified claim)

### L1 — the final tip adds a scored unit; no receipt covers it (evidence custody)

`01a44dbf` itself adds the capability row that the predicate scores
(`SCORECARD:627`, "REA SquashFS recursion through sasquatch (LE v4)", 3 pointers). `grep -c` of that
row's text: **0** at `d2e46ef5` and at `ffc81341`, **2** at `01a44dbf`. Unit count therefore goes
15 → 16 units and 34 → 36 → 38 → **41** pointers, while

```
$ grep -rl '"predicate": "P36-C2"' .ufo/waves/round-36 --include=*.json
.ufo/waves/round-36/controls/ctl-c2-{0..3}*.json
.ufo/waves/round-36/c2/after-at-d2e46ef5.json
.ufo/waves/round-36/after/c2-at-ffc81341.json
```

— no C2 receipt exists at `01a44dbf` or later, and `SCORECARD:3392` lists the two older revisions.
The frozen plan promised exactly this second measurement ("measured at its own landing commit … then
again at the final tip"), and the integration commit is the tip where the scored set grows. I
re-ran the frozen counter at the tip: exit 0, 0 mismatches, `guards_ok`, 41 pointers — so the
predicate is **met**, but the lane did not run it there. Under §9 ("An unrun check has not passed")
the tip check passes only because a non-author seat ran it. This is the M36-2 shape (a present-tense
surface measured at a pinned revision and left behind) recurring one commit after the lesson names it.
Severity: moderate. Axes: calibration, coverage (unit population).

### L2 — box 4's cited boundary now contains two contradictory install rules

SHONEN box 4 (`:11-12`) asserts "No cross-domain bleed (PROVINCE.md still accurate)" and cites
`PROVINCE.md:97-125`, calling `:119-125` a "round-36 dated tooling bullet **reconciling** the installer
line :110-115". But PROVINCE gained **0 deletions** in `ffc81341` (`git diff --stat ffc81341^ ffc81341 -- PROVINCE.md`
→ `15 +++++++++++++++`), so `:110-115` stands unamended:

```
PROVINCE.md:110  - **Installing engines, Python packages, or editing client configs** — … installing
PROVINCE.md:113  Hopper/IDA/JADX/Binwalk/Unblob/pwntools/ilspycmd/.NET SDK — all **operator-owned**.
PROVINCE.md:114  The lane documents the gap and the exact env key; it never runs the installer.
PROVINCE.md:119  - **Tooling, dated 2026-10-26** — the 2026-10-19 operator directive
PROVINCE.md:120  (`/home/vgpnk/.omp/agent/RULES.md`) lets an agent install or upgrade the
PROVINCE.md:121  tooling its task needs through official channels only, with tool, version,
PROVINCE.md:122  channel and reason recorded (round 36: sasquatch 4.5.1, official onekey-sec
PROVINCE.md:123  deb, into `~/.local/bin`); `rea setup` runs and client-config edits …
PROVINCE.md:125  `pi`) stay **operator-owned** and lane-untouched.
```

The operator directive's own channel list includes `uv tool install <pkg>` — a *Python-package*
install — so `:110-115` ("Python packages … operator-owned … never runs the installer") and
`:119-125` (agents may install task tooling) disagree for at least that class, and the new bullet
retracts neither the clause nor the tools list. The file demonstrates the convention it omits ten
lines later: `PROVINCE.md:374` explicitly marks the Frontier bullet "superseded for little-endian
SquashFS v4 … its '(AUR-only)' was wrong as a route statement". The `## Adjacent` preamble
(`:99-100`, "Ground the lane refuses or defers") also no longer describes every bullet in the range the
box cites. Impact: a box titled "No cross-domain bleed" now cites, as its evidence, a grant, and its
headline "PROVINCE.md still accurate" is an assertion P36-C2 cannot count (§9: "It cannot be an
assertion"). Severity: moderate. Axes: calibration (the scored unit), province scope (C1's surface).

### L3 — a live instance of the pointer filter hole (correcting wave 1's "latent, not live")

The predicate's first clause is universal: "**every** backticked repo pointer in them resolves at that
revision (path exists…)". The counter drops any token with no `/` that does not end `.md`. Two such
tokens are real file names, in scored rows, at the tip:

| row | token | repo-relative existence |
|---|---|---|
| `SCORECARD.md:621` (config custody capability) | `` `config-post-pair.txt` `` | absent at root; the file is `.ufo/waves/arc2-loop1-round2/receipts/config-post-pair.txt` |
| `SCORECARD.md:25` (calibration Owned axes) | `` `result.json` `` | absent at root; the file is `evidence/round-1-2026-10-15/result.json` |

```
$ git cat-file -e 01a44dbf:config-post-pair.txt ; echo $?   → nonzero (absent)
$ git cat-file -e 01a44dbf:result.json        ; echo $?   → nonzero (absent)
$ git cat-file -e 01a44dbf:.ufo/waves/arc2-loop1-round2/receipts/config-post-pair.txt → 0 (exists)
$ git cat-file -e 01a44dbf:evidence/round-1-2026-10-15/result.json                     → 0 (exists)
```

`config-post-pair.txt` is the *same sibling-basename shape* the round repaired one row below
(`receipts-B/` → full path) and left here. Both are resolvable from adjacent context, which is why a
human reads them as fine, but neither resolves as a path, and the counter returns `unresolved: []`
because of its filter. So the sentence's universal clause is **false as written** at the measured
revision while the frozen counter is green — the divergences wave-1 `R36CriticPredicateIdentity.md`
§5 C2-1 / §6 listed, now with a live instance. Severity: low (surface), high (predicate identity —
this is the §9 "universal clause without a full enumerator" defect that QUALITY 77 exists to close).
Axes: calibration.

### L4 — the repair convention was applied to one Owned row and not its sibling (pre-existing)

`SCORECARD.md:24` (depth) last-change cell: "… count refreshed rounds 25 and 26", while the same row's
observable cell says "17/17 … at `c369242…` (recount, round 31; also 17/17 at `ebe2cb4a`, round 26)".
The round repaired exactly this omission for coverage (`:23` now reads "count refreshed rounds 25, 26,
31 and 36") and left depth untouched — consistent with "C1 did not touch the depth row", but by the
lane's own convention (round 31 counted as a refresh for coverage) the depth cell is now understated.
Inherited from base; the counter's fixed statement shapes never reach a last-change cell. Severity: low.
Axes: depth, calibration.

---

## 5. Why not honest-stop, why not unprovable

- **honest-stop** requires the frozen counter to miss at the measured revision. It does not: both
  receipts recompute identical, exit 0, and the tip also exits 0. No narrow-after-landing occurred —
  the predicate, counter and kill rule are byte-identical from freeze to tip (§1).
- **unprovable** requires the evidence to be undecidable. It is not: two independent computations of
  every stated number and range agree (documented recipes A and B run verbatim, plus a third parser
  over the surfaces), and both repaired pointers land on unique documents.
- **§9 "Same sentence / same condition / same label"**: sentence ≡ docstring ≡ receipt labels was
  established in wave 1 and is unchanged (counter hash identical from freeze). The residual
  divergence is the one §4/L3 makes concrete: the sentence's universal is wider than the enumerator.
- **§9 "Name the axis by the surface the round changes"**: C2 is a calibration claim counting
  mismatches between SCORECARD/SHONEN and observed state, and it does that (`mismatches` is a real
  count, not an assertion) — pass, with the L2 boundary hazard.
- **§9 do-nothing**: unreachable (3 mismatches at base, exit 1) — pass.
- The round does **not** claim a score increase (coverage 10 → 10, depth 10 → 10, calibration 10 → 10,
  SCORECARD:3394); the move claimed is 3 → 0 mismatches, which I confirm.

---

## 6. Impacted axes

- **calibration** — the claim's own axis: met at both named revisions and at the tip, no shortcut
  shape; but L1 (tip unreceipted), L2 (a scored box's cited boundary now holds two rules), L3 (live
  filter hole), L4 (sibling row not repaired by the same convention).
- **coverage** — L1 (scored unit population 15 → 16 without a receipt); L3 (the sibling-file citation
  inside a capability row); no population regression anywhere.
- **depth** — L4 only (last-change cell understates round 31/36); depth numbers are 17/17 and true.
- **province scope (C1's surface, observed only)** — L2; I did not re-measure C1's carriers, which is
  not this seat's assignment.

## 7. Smallest safe corrections

1. **Close L1 (one command, already green).** Run the frozen counter at the integration tip and commit
   the receipt, then add the revision to `SCORECARD.md:3392`'s "measured at" cell:
   `python3 -I -B tools/round-36/c2-counter.py --root <lane> --rev 01a44dbf… --base cab59f22… --json-out .ufo/waves/round-36/after/c2-at-01a44dbf.json`
   → exit 0, `mismatches 0`, `guards_ok`, 41 pointers (verified here). Re-run after any further surface
   edit at the true final tip.
2. **Close L2 (three lines in PROVINCE).** Scope `PROVINCE.md:113-115` to what remains operator-owned
   (`rea setup`, client-config edits, the named operator engines) or append a dated supersession line
   under it exactly as `:374` already does for the Frontier bullet, so that `## Adjacent` 97-125 holds
   one rule about installs and the box's "still accurate" carries an edit behind it.
3. **Close L3 (two one-line pointer fixes, or one counter change).** Write `SCORECARD.md:621` as
   `.ufo/waves/arc2-loop1-round2/receipts/config-post-pair.txt` (same shape the round applied to
   `receipts-B/`) and `:25` as `evidence/round-1-2026-10-15/result.json`; and, for the successor
   instrument, treat any backticked token containing `/` **or** ending in a known file extension
   (`.md .json .txt .py .sh .mjs .tsv .log`) as a pointer and print the skipped tokens in the receipt,
   so the universal clause has a full enumerator (QUALITY 77).
4. **Close L4 (one cell).** `SCORECARD.md:24` → "count refreshed rounds 25, 26 and 31" (round 36
   leaves the row unchanged, per the coverage row's convention).
5. **Freeze-side, for round 37's successor (QUALITY 77 as written):** name the intended repair
   documents by full lane-relative path in the freeze. This round's freeze names none, so the "same
   document" clause is only satisfiable by tree uniqueness, not by the rule.

## 8. Limits / inference

- Scope is R36-C2 only. I did not re-measure C1's carriers, receipts or provenance; the C1 capability
  row's prose is C1's predicate business (its 3 pointers resolve, which is all P36-C2 counts).
- The worktree at read time carried uncommitted edits from other wave-2 seats
  (`corpus/SOURCES.md`, `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`,
  `corpus/lessons/round-36.md`) and untracked `.ufo/waves/round-36/w2/`. `SCORECARD.md` and
  `SHONEN.md` were clean, and every measurement above reads git objects at a named revision, so the
  worktree state cannot change a number here.
- `[INFERENCE]` — that `uv tool install` falls under "Python packages" at `PROVINCE.md:110` is my
  reading of the directive's channel list (`~/.omp/agent/RULES.md`, quoted in the round contract §7);
  the directive text itself is not repo bytes, so L2 rests on the two PROVINCE clauses plus the
  directive's channel order, not on a lane-committed copy of the directive.
- `[INFERENCE]` — severity ordering (L1 > L2 > L3 > L4) is my judgement; every quoted number, path,
  line, exit code and byte-level claim above was executed read-only against the lane and its receipts.
- No tool installed or upgraded; nothing outside this report was written.
