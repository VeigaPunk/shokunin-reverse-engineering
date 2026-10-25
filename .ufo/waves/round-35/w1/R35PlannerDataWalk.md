# R35PlannerDataWalk — data-walk of the SCORECARD planned row and the r34 spot-check (kaidoku round 35, wave 1)

Seat: `R35PlannerDataWalk` (scout) | Wave: `r35-build` | Milestone: Build evidence and first falsifications
Date: 2026-10-25 | Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Role: **leaf member — no subagent dispatch, no nested delegation, no background work.**

Scope of this seat: read-only data-walk of (a) the SCORECARD *planned* row that round 34 left for round 35,
(b) `corpus/lessons/round-34-verifier-spotcheck.md` (the r34 routed defects D-1..D-5), and (c) the frozen
round-35 claim surface (`plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`,
`tools/round-35/c1-coverage-counter.py`, `tools/round-35/c2-calibration-counter.py`), producing cited evidence
and first falsifications. **No claim data was authored. No predicate, counter, or scope was altered. No lane
production file, corpus file, counter, plan, claims file, SCORECARD, LOG, report, VCS/index/jj state, fleet or
sibling repo, or `/home/vgpnk/Projects/shokuknow` was written.** The only lane write is this report.

---

## 0. Revisions under examination

| rev | what it is | note |
|---|---|---|
| `aa04633a686d49756763b1feed4be6830d5bb479` | round-34 verifier spot-check (`base` in the frozen claims) | committer time `2026-10-25T05:08:51-03:00`; confirmed ancestor of HEAD |
| `d2729cba895b8664f3ccb27196091494f3cda83b` | round-35 instruments-first prep; **adds** `census-start.txt` | committer time `2026-10-25T16:05:46-03:00` |
| `2323d197456f1328459d9420aff025cffbcb3e27` | **canonical freeze** — first add of `claims-canonical.json` | `2026-10-25T16:13:40-03:00`; this is the `--freeze` both counters read |
| `3ecf42981a0b63414de90ade643040d609dbb8a5` | do-nothing control receipts committed | `2026-10-25T16:13:53-03:00`; = lane `HEAD` at my read time |
| `ee0c865c878492c26fb43aa1c0beaee7b6388f63` | `refs/heads/main` — **one commit ahead of HEAD** | adds `corpus/lessons/round-35.md`, `SCORECARD.md` (+11), `LOG.md` (+11), `census-end.txt`, and 50 seat reports |

`git merge-base --is-ancestor 3ecf4298 ee0c865c` → true; `git rev-list --count 3ecf4298..ee0c865c` → 1.
So `ee0c865c` is the newest committed lane state; `HEAD` is its parent. Both are scored below.

---

## 1. The SCORECARD planned row (r34 → r35) — cited, and where r35 diverged

`SCORECARD.md:3369` (round-34 run-6 section, last line) reads verbatim:

> - **planned (round 35, after a steer):** depth or coverage — the fresh-content replay counter
>   (`w1/CtlMultiset-files/mini-counter-fresh.py`: 8/8 structural, 0/8 for all nine structure-blind classes)
>   plus the forced-payload-perturbation surface demonstrated by `w1/MutShortcutClasses.md`, frozen with the class
>   set asserted against the pinned set, `met_target == (matched == target)`, digest-bound class entries and a
>   reserved positive-control label; the green surface must vary size, order, payload and name vocabulary
>   together, and the class set must include one class per keyable invariant. **Second choice: calibration over
>   the six record defects, counted as mismatches against observed repo state.**

**Divergence 1 — the coverage axis was taken on a different surface.** The planned coverage surface was the
*fresh-content replay counter* (`mini-counter-fresh.py`), i.e. a depth-shaped structural counter. The round-35
coverage claim C1 is instead an **assimilation/admission** claim on the `.jsc -> source mapping` frontier
(`plans/round-35-claims.md` §Claim C1; `claims-canonical.json` C1 `type: "assimilation/admission"`). The r34
plan named no assimilation duty at all. The r35 plan's §10 says the theme was taken from `merge/kaidoku/`, and
adds that `considerthese/` does not exist in this lane.

**Divergence 2 — "the six record defects" is not D-1..D-4.** The six numbered record defects in r34's own
record (`SCORECARD.md:3359`) are: (1) pins were declarative in a container the freeze gate rejects;
(2) frozen `predicate_identity` is false (31 words vs 46 words); (3) dropping classes to the `MIN_SHORTCUTS`
floor still prints CLEAN; (4) a shortcut relabelled `structural` prints CLEAN; (5) a gate running no reader
satisfies all six clauses and `met_target` is never cross-checked with `matched`; (6) `--rev` is an echo and
receipts carried no argv. Round-35 C2 instead closes **four** defects — the *verifier-routed* D-1..D-4 from
`corpus/lessons/round-34-verifier-spotcheck.md` §"Routed defects", a different set (D-5 was routed to the
protocol lane, not to kaidoku). So the round-35 plan re-scoped the calibration claim from the six r34
*record* defects to the four r34 *verifier* defects. This is a legitimate re-scope, but it is not what the
planned row said, and it is the source of the D-4 collision in §4 below.

**Divergence 3 — planned "counted as mismatches against observed repo state" became four binary predicates.**
C2 is four boolean checks, not a mismatch count. Notably the planned row's phrase would have caught exactly
the D-1 defect class that the frozen predicate misses (§3).

**Divergence 4 — the planned row says "after a steer"; the claims were frozen with no steer recorded.**
`plans/round-35-claims.md` opens "Frozen claims: C1 … C2 …" and `freeze-status.md` records only a setup-order
defect. No artifact in the lane records the steer the planned row conditions on. Recorded as an observation, not
a fault.

**Axis-table consistency (no divergence).** `plans/round-35-claims.md` header: "Owned axes at base: coverage 10,
depth 10, calibration 10 (finite proxies, none retired) — a tie makes every owned axis a lowest axis; no
stagnation waiver needed." The r34 spot-check's axis verdicts table reads coverage / depth / calibration
"unchanged" at `10 → 10`. Consistent. Note the r35 plan claims **no depth axis at all** — coverage (C1) and
calibration (C2) only — so the third tied-lowest axis is left unclaimed, which is what the plan says.

**`considerthese/` — the one line the plan owes.** Verified absent from the lane and the fleet root:
`ls -d considerthese kaidoku/considerthese kaidoku-shokunin/considerthese` → all "No such file or directory"
(searched `/home/vgpnk/Projects/shokunin`; `merge/kaidoku/` is likewise not present at that root — the only
`merge` directory found is `/home/vgpnk/Projects/shokuknow/merge`, outside this lane).

---

## 2. The r34 spot-check, re-derived independently (not read from the round-35 lesson)

`corpus/lessons/round-34-verifier-spotcheck.md` §"Routed defects — kaidoku must fix next round" lists D-1..D-5.
I re-derived D-1..D-4 from committed bytes rather than trusting the r35 lesson's summary.

### D-1 (frontier census receipt) — r34's defect CONFIRMED; r35's remedy landed in content
- r34: `cmp <(git show aa04633a:.ufo/waves/round-34/r34b/census-start.txt) <(git show aa04633a:.ufo/waves/round-34/r34b/census-end.txt)`
  → **identical** (cmp exit 0). And `git show aa04633a:.ufo/waves/round-34/r34b/census-start.txt | grep -c "rows="`
  → **0** — the r34 start receipt carried no row count at all, so r34's report row "105 rows … 8 × W04" described
  an artifact that did not exist. Defect confirmed on the bytes.
- r35 remedy: `.ufo/waves/round-35/assimilation/census-start.txt` (committed `d2729cba`, 16:05:46) carries a
  header, the census command, the 9 `W04` lines, `EXIT=0`, and a "Manual frozen census" block with
  `rows=106 / malformed=0 / tiers A=100 B=5 C=1 / status mined=102 rejected=4 / duplicate_ids=0`.
  `grep -c 'W04'` → **9**. `cmp` against r35's own `census-end.txt` → **differ** (start ≠ end, the r34 defect
  class is fixed).
- Independent re-census of the base blob: I re-parsed `git show HEAD:corpus/SOURCES.md` with the counter's own
  11-column regex → **106 rows parsed, 0 unparsed**; tier `A=100 B=5 C=1`; status `mined=102 rejected=4`.
  The receipt's numbers are **true against the base blob**, not asserted.
- Commit ordering: the census receipt is committed in `d2729cba` (16:05:46), which is **before** the canonical
  freeze `2323d197` (16:13:40) and before any post-base `corpus/SOURCES.md` change. That part of D-1 holds.

### D-2 (seat accounting) — r34's defect CONFIRMED
- `git show aa04633a:.ufo/waves/round-34/r34b/w2-seat-map.json` → a **list of 32** seat entries.
- `git ls-tree -r --name-only aa04633a | grep -E "round-34/r34b/w2/[^/]+\.md$" | wc -l` → **31** reports.
- The missing seat: `git ls-tree -r --name-only aa04633a | grep AAdjacencyCite` → exactly one hit,
  `.ufo/waves/round-34/r34b/w2/prompts/AAdjacencyCite.md` — a **prompt only, no report**. Confirmed: 31/32, and
  `AAdjacencyCite` is the unreported seat.
- r35 must record that correction plus a wave-seat line identical to the settle receipts.

### D-3 (knowledge entry provenance trio) — r34's defect CONFIRMED
`git show HEAD:corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md | head -15` shows the
entry opening `author: / status: / sources: S106 (…) / revisions:`. `grep -c '^source:'` = 0,
`^verified-at:` = 0, `^recheck:` = 0. Note the near-miss: the entry has a **plural** `sources:` line, which the
frozen D-3 regex does not match (`^source\s*:`). The spot-check's instruction stands: append a block, do not
rewrite the entry.

### D-4 (instrument registry row fields) — r34's defect CONFIRMED, and r34's own spot-check named the exact
gap it would create
The r34 spot-check's D-4 text: PROTOCOL §Gate standard requires per row `gate|probe`, verdict map, self-test
command and spelling, **pinned-value path**, **write scope** and **owner`; "the round followed the lane's
five-column habit". Confirmed in the bytes: `SKILL.md:1213-1219` (round-34 run-6 registry) is a **5-column**
table (`tool | purpose | command | exit codes | selftest`), while `SKILL.md:1066-1073` (round-32 registry) is
already the **8-column** form the frozen predicate demands. So the two tables the predicate names are in
*different* shapes, and the round-32 one is already compliant.

---

## 3. Frozen-counter behaviour, measured (counters unmodified; `--selftest` and scoring runs only)

Both counters are byte-identical between the worktree and `HEAD`:
`e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220` (C1),
`576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94` (C2) — both equal the
`claims-canonical.json` `instruments` pins and the `plans/round-35-claims.md` pin.

Predicate byte-identity **holds** where it is claimed to hold:
`P35-c1` counter constant ≡ canonical ≡ frozen (478 chars, sha `f2e27b8ba62c…`);
`P35-c2` counter constant ≡ canonical ≡ frozen (684 chars, sha `356487003f85…`).
The plan's "byte-identical in this plan" wording is *not* literal — the plan file contains neither `P35-c1`
nor `P35-c2` as a literal string, and neither full predicate sentence appears in `plans/round-35-claims.md`.
The plan states the predicate in prose under §Claim C1/C2; the counter and both claims files agree exactly.
Non-literal but unambiguous.

### 3.1 Baseline scores at the three revisions

| run | rev | C1 | C2 |
|---|---|---|---|
| base control (committed receipt) | `aa04633a` | exit 1, 8 named failures | exit 1, 9 named failures |
| lane HEAD | `3ecf4298` | exit 1, 8 named failures (identical to control) | exit 1, 9 failures, now `D1_no_sources_change_after_base` |
| `refs/heads/main` | `ee0c865c` | exit 1, 8 named failures (unchanged) | exit 1, **11** failures (lesson now present but incomplete) |

C2 at `ee0c865c` — `D1_no_sources_change_after_base; D2_r34w2_correction_missing; D2_settle_missing:.ufo/waves/round-35/w1-settle.json; D2_settle_missing:.ufo/waves/round-35/w2-settle.json; D2_lesson_seat_line_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry`

Counter exit-2 path confirmed reachable and correct: `--freeze 13d7a815…` (the *earlier* claims-frozen file)
→ `C1: claims file absent at freeze revision`, exit 2. This is the same discovery defect
`freeze-status.md` already records for the round-34 gate.

### 3.2 The D-1 ← C1 causal coupling (the round's own M35-1, independently confirmed)

`c2-calibration-counter.py` computes `first_change_time(root, base, rev, "corpus/SOURCES.md")` and, if there is
**no** post-base change to that path, emits `D1_no_sources_change_after_base` and fails — *regardless of the
census receipt's content*. `git log aa04633a..ee0c865c -- corpus/SOURCES.md` → **empty**: only C1's S125/S129
append can create that change. So **C2 cannot be scored CLEAN unless C1 lands.** The two "independent" claims
are not independent. Confirmed by direct measurement, not inference: with `corpus/SOURCES.md` untouched after
base, C2 fails `D1_no_sources_change_after_base` while D-2/D-3/D-4 could all be green.

### 3.3 D-1 accepts a fabricated census receipt (falsification, reproduced)

The predicate says the receipt "carries the base count (106 rows, exit 0, **9 W04 warnings**)". The frozen check
is three substring tests (`c2-calibration-counter.py:68`):

```python
if "rows=106" not in census or "EXIT=0" not in census or "W04" not in census:
    fails.append("D1_census_content_missing")
```

In a throwaway `/tmp` repo I wrote a **one-line** census receipt containing exactly `rows=106 EXIT=0 W04` — no
census was ever run, no 9 warnings, no row count — plus a satisfied D-2 (lesson line + both settle receipts),
an appended D-3 trio, and a widened D-4 round-32 section. Result: `C2_FAIL: D4_section_missing:### Round-34
run-6 instrument registry` — **D-1 passed on the fabricated receipt**. `rows=1060` or a single `W04` would also
pass. The counter never re-hashes the pinned census input: `grep -c "hashlib\|sha256"` → C1: 1 (an unused
import), **C2: 0**. `claims-canonical.json` carries `frozen_inputs` for `census-start.txt`
(`b6ce2b1773c60af4e3f5b14b7a63ba9743cae1eeec121b1ada50178a3d7af10a`) and neither counter reads `frozen_inputs`
at all (`grep -c frozen_inputs` → 0 in both). **The frozen pin on the census receipt is decorative.**

### 3.4 D-3 matches `S1060`, not the token `S106` (falsification, reproduced)

`c2-calibration-counter.py:126` — `re.search(r"(?m)^source\s*:.*S106", body)`. The `.*S106` is an unanchored
substring. In the same `/tmp` fixture I set the r34b entry's trio to `source: S1060 — a different row`; **D-3
passed** (the only remaining failure was the D-4 section name). A citation of a *different, non-existent* row
satisfies the frozen D-3 check.

### 3.5 C1 is content-blind — passes with entries containing zero jsc2js content (falsification, reproduced)

This is the sharpest finding. C1's entire entry check is four regexes on the file body
(`c1-coverage-counter.py:105-112`): `^source\s*:`, `^verified-at\s*:`, `^recheck\s*:`, and
`^source\s*:.*<row>`. Nothing reads the entry's **substance**. In a `/tmp` fixture I created both knowledge
entries containing **only**:

```
source: S125
verified-at: 2026-10-25
recheck: 180d
```

— no `.jsc` mapping, no jsc2js, no V8 version, no d8, no View8, nothing — plus the S125/S129 registry rows and
the PROVINCE/README mentions. **Result: `C1_CLEAN revision=HEAD`, exit 0.** The C1 predicate's own words are
"the two shokuknow-package jsc2js knowledge entries … land on the `.jsc -> source mapping` frontier"; the frozen
counter cannot distinguish that from two three-line files.

### 3.6 C1's registry row parse is not anchored to `## Registry` (falsification, reproduced)

`ROW_RE` is applied to the whole `corpus/SOURCES.md` blob with no section awareness (`grep -n "Registry"` in the
counter → no match outside its own selftest fixture). I moved the S125/S129 rows **out** of `## Registry` into
`## Leads (unopened)` — a state the lane's own census rejects with **E12 "row outside Registry section"**
(`scripts/sources-census.sh:621`, exit 1). **Result: `C1_CLEAN`, exit 0.** C1 can pass on a `SOURCES.md` that
the lane's census script rejects.

### 3.7 C1's PROVINCE / README checks are unscoped substring probes (falsification, reproduced)

- PROVINCE: `stem not in province` where `stem` is the filename minus `.md`. My `/tmp` fixture mentioned both
  stems **only in an unrelated prose paragraph**, with no Core-addition table at all → C1 passed. The predicate
  requires "PROVINCE.md carries a **Round-35 Core-addition table row** naming both entry stems"; the counter
  requires the stem to appear **anywhere** in the file.
- README: the predicate requires "the README **coverage map** holds both entry filenames"; the counter requires
  the string to appear **anywhere** in `corpus/README.md`.
- **Naming asymmetry (a landmine for the executor seat).** PROVINCE is checked against the stem **without** `.md`;
  README is checked against the filename **with** `.md` (`c1-coverage-counter.py`, `readme_missing:{p}` where `p`
  ends `.md`). But the README's own house convention is stem-style, extensionless: of the **216** backticked
  tokens in the coverage-map region, **0** end in `.md` and **173** are bare `2026-10-13-…` stems. A seat that
  writes the README row in house style **fails** C1's `readme_missing` — reproduced: `C1_FAIL: readme_missing:
  corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md; readme_missing: corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md`
  while PROVINCE was accepted from prose. Passing requires *deviating* from the README convention on the README
  side while PROVINCE accepts either form (the stem is a substring of the `.md` name).

### 3.8 C1's row-citation is also a substring match (falsification, reproduced)

Same class as §3.4: `re.search(r"(?m)^source\s*:.*" + row, body)` with `row = "S125"`. I set the entries'
citations to `source: S1250` and `source: S1290` — **wrong row ids** — and C1 returned **`C1_CLEAN`, exit 0**.

### 3.9 The C1 receipt's `checks` sub-map is vacuous

`c1-coverage-counter.py`'s receipt builds `checks` from `f not in fails` over a **fixed label list**
(`entry_exist`, `trio`, `row_citation`, `registry_rows`, `province`, `readme`) — labels that never appear in the
`fails` strings, which use different names (`entry_missing:…`, `trio_missing_source:…`, …). So every check is
`True` unconditionally: with **nine** real failures the map is still
`{'c1_0': True, 'c1_1': True, 'c1_2': True, 'c1_3': True, 'c1_4': True, 'c1_5': True}`. The committed
do-nothing receipt `.ufo/waves/round-35/controls/c1-do-nothing.json` therefore shows `checks` all-true beside a
non-empty `failing` list and `"pass": false`. **`checks` carries no information; only `failing` and the exit code
do.** (Sibling seat `R35ExecC1` independently observed the same artefact.)

### 3.10 D-4: the frozen section names do not match the historical tables

`EIGHT_CELL_SECTIONS = ["### Round-32 instrument registry", "### Round-34 run-6 instrument registry"]`, matched
by **exact** line equality (`l.rstrip() == sec`).
- Round-32: the heading matches (line 1064) and its own table (1066-1073) is **already 8 cells** — but the scan
  runs to the next `##`-prefixed line, which is `## Round-33 instrument status…` at 1086, so it also swallows the
  **separate 4-column "Residual witness registry" table at 1081-1084** → `D4_not_eight_cells:…line1081:cells=4`.
  The failure is in a table the predicate does not name.
- Round-34: the heading is `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)`
  (line 1209). It never equals the required string → `D4_section_missing`, permanently. Even if renamed, its
  rows are **5 cells** (1213-1219) and would then fail `D4_not_eight_cells`.

So closing D-4 under the frozen predicate requires (a) renaming a historical heading and (b) rewriting a
historical 5-column table and a historical 4-column table to 8 cells — i.e. rewriting committed r32/r34 record.
That is the r34 spot-check's own D-4 point inverted: r34 asked for *more* columns as a forward standard, and the
frozen predicate now demands retrofitting history to it. **D-4 is not closable without rewriting history**, which
is a design fault in the frozen predicate, not a work deficit. (The same collision is recorded as M35-3 in the
round's own lesson; I reached it from the counter's scan semantics.)

### 3.11 D-2: the settle receipts are not yet committed, and the on-disk one is malformed

- `git ls-tree -r --name-only ee0c865c | grep -E "w[12]-settle"` → **nothing**. Neither settle receipt is tracked
  at any revision, so the counter's `show(root, rev, sf)` returns `None` → `D2_settle_missing` ×2.
- The untracked worktree file `.ufo/waves/round-35/w1-settle.json` contains a **duplicate JSON key**:
  `{"spawned": 2, "settled": 2, "dead": 0, "spawned": 7}` — `json.loads` takes the last, yielding
  `spawned=7`. Two mutually inconsistent numbers in one receipt.
- `w2-settle.json` **does not exist** in the worktree at all.
- `w1-dispatch.json` records `counts.spawn = 64`, and `w1-spec.json` has 64 items, while 56 seat report files
  are on disk — so the eventual `spawned=` value is itself unsettled.
- **Consequence:** the counter requires **both** `w1-settle.json` and `w2-settle.json` to exist at the measured
  revision and sums their `spawned/settled/dead`, requiring one lesson line
  `Seat accounting (round 35): spawned=N settled=M dead=K` equal to that sum. Since `w2-settle.json` can only
  exist after wave 2 settles, **C2 is not measurable at any wave-1 revision** — its measured revision is
  necessarily post-wave-2. This is a wave-ordering constraint on the round that no artifact states.
- `corpus/lessons/round-35.md` at `ee0c865c` contains **0** occurrences of `AAdjacencyCite`, **0** of `31/32`,
  and **0** of `Seat accounting` → `D2_r34w2_correction_missing` and `D2_lesson_seat_line_missing`. The r34
  correction D-2 asks r35 to record has **not** been recorded.

### 3.12 What is genuinely correct in the round-35 prep (credit where due, stated against interest)

- Predicate byte-identity across counter constants and both claims files: exact (§3 header).
- Instrument pins in `claims-canonical.json` match the committed counter bytes exactly (§3 header) — the
  `INSTRUMENT_REVISED` debt in `freeze-status.md` is a *gate-discovery* artifact, not a byte mismatch.
- The census receipt's numbers are **true** against the base blob (§2 D-1): 106 rows, A=100 B=5 C=1,
  mined=102 rejected=4, duplicate_ids=0, 9 W04 — independently re-derived.
- r35's `census-start.txt` ≠ `census-end.txt`, unlike r34's identical pair — the r34 D-1 defect class is fixed.
- The id-guard proof is real and reproducible: `id-guard-proof/fixture-registry.md` holds an **indented**
  `  | S002 |` row and `staged-ids` holds `S002`; `run-proof.log` records `comm -12` → nonempty. On the real
  package, `reg-ids` = S001..S106 (106), `staged-ids` = S106..S237 (132), `collisions` = **S106** — one real
  collision, correctly the pre-existing r34 row, and S125/S129 do not collide.
- `considerthese/` is confirmed absent (§1).
- The quarantine dispositions are hand-checked with live bytes and are not stubbed (S150 REFUSE on a
  payload-absent quote, S113 reachable-now, S117 unreachable-not-fabricated, S136/S147 locatable).

---

## 4. First falsifications — summary table

| # | falsification | class | reproduced? | evidence |
|---|---|---|---|---|
| F1 | C1 passes with **content-free** entries (3 lines each, zero jsc2js/`.jsc` content) | vacuous semantic predicate | **yes**, `/tmp` fixture → `C1_CLEAN` exit 0 | §3.5 |
| F2 | C1 passes when S125/S129 sit **outside `## Registry`** (lane census → E12 exit 1) | scope leak | **yes** → `C1_CLEAN` exit 0 | §3.6 |
| F3 | C1 accepts `source: S1250` / `S1290` — wrong row ids | substring vs token | **yes** → `C1_CLEAN` exit 0 | §3.8 |
| F4 | C1 PROVINCE satisfied by **prose**, not a Core-addition table row | scope leak | **yes** | §3.7 |
| F5 | C1 README needs `.md` filename but house style is extensionless (0/216 map tokens carry `.md`) | counter-vs-convention conflict | **yes** → `C1_FAIL readme_missing` | §3.7 |
| F6 | C1 receipt `checks` map all-`True` with nine real failures | receipt shape | **yes**, computed | §3.9 |
| F7 | C2 D-1 accepts a **one-line fabricated** census `rows=106 EXIT=0 W04`; warning count and pinned hash never checked | vacuous + unpinned input | **yes** → D-1 passed | §3.3 |
| F8 | C2 D-3 accepts `source: S1060` | substring vs token | **yes** → D-3 passed | §3.4 |
| F9 | C2 D-4 cannot close without **rewriting r32/r34 history**; its two named surfaces are already-compliant / 5-column | predicate-vs-layout mismatch | **yes**, exact scan semantics | §3.10 |
| F10 | C2 D-1 **requires C1's SOURCES.md append** to be evaluable at all | claim coupling (no causal separability) | **yes**, direct runs | §3.2 |
| F11 | C2 D-2 needs a committed `w2-settle.json` that only exists **after wave 2**; the worktree `w1-settle.json` has a duplicate `spawned` key (2 vs 7) | wave ordering + malformed receipt | **yes** | §3.11 |
| F12 | `corpus/lessons/round-35.md` at `ee0c865c` records **none** of the r34 D-2 correction (0× `AAdjacencyCite`, 0× `31/32`, 0× `Seat accounting`) | defect not closed | **yes** | §3.11 |

---

## 5. Advisory conclusions (no data authored, nothing scored on my behalf)

1. **Do not author C1 data against the frozen counter.** F1–F6 mean a passing C1 would not evidence the
   predicate's own words ("land on the `.jsc -> source mapping` frontier"): the counter cannot see jsc2js
   content, cannot see whether the PROVINCE/README mention is a table row, and accepts wrong row ids. Admitting
   S125/S129 now would buy a green receipt whose subject matter the predicate never measured — the same
   shape of failure the round-34 stop recorded ("a registry-relative CLEAN").
2. **C2 is not closable in wave 1, on the frozen predicate, without rewriting history.** F9 (D-4) is a design
   fault; F10 (D-1 coupling) means C2's score depends on C1 landing, which F1–F6 argue against; F11 (D-2's
   `w2-settle.json`) means the measured revision is necessarily post-wave-2; and the r34 correction D-2 asks
   r35 to record is still unrecorded (F12). The r35 plan's own kill rule — "any of the four frozen checks
   failing at the measured revision stops the claim (honest stop)" — points at a stop, which is the recorded
   verdict at `ee0c865c`.
3. **The SCORECARD planned row and the round-35 plan are on different surfaces** (§1, divergences 1–2). The
   planned calibration — "counted as mismatches against observed repo state" over six defects — is a stronger
   instrument than the four boolean checks that were frozen, and the planned coverage surface (fresh-content
   replay counter) was not used at all. A future round should reconcile the plan with the row it inherits.
4. **Two defects in the plan's own discipline text** are worth recording for the next freeze: the plan says
   the predicate is "byte-identical in this plan" while the plan carries no literal predicate; and
   `claims-canonical.json` `frozen_inputs`/`instruments` pins are read by **neither** counter (F7), so the
   round-35 pins are documentary only — the round-34 lesson already recorded that same class ("pins were
   declarative").
5. **Wave-2 precondition**: whoever closes D-2 must reconcile the duplicate `spawned` key in
   `w1-settle.json`, publish `w2-settle.json`, and decide the seat total against `w1-dispatch.json`'s
   `spawn=64` versus the 56 report files on disk before the lesson line is written.

---

## 6. Limits of this data-walk

- Every measurement above is over **committed bytes** (`git show`, `git ls-tree`, `git log`), plus the two
  unmodified counters executed read-only in the lane and in throwaway `/tmp` repositories. No lane worktree
  file, corpus file, counter, plan, claims file, SCORECARD, LOG, or report was written; no `jj`/git state was
  mutated; no source tree was modified; no fetch was performed; nothing was installed.
- The `/tmp` fixtures are **instruments-under-test demonstrations, not claim data**. They show what the frozen
  counters do and do not discriminate; they are not, and must not be read as, a claim score.
- I did **not** re-run the fleet census (`scripts/sources-census.sh`) against the lane — it writes outside the
  lane. The registry figures in §2 D-1 were re-derived independently from the committed `corpus/SOURCES.md`
  blob with the counter's own 11-column regex and agree with the committed receipt.
- `find`/`du` were not used under `/fast/scratch`; no path under it was opened. No `find` was run anywhere.
- Sibling-lane and fleet content (`/home/vgpnk/Projects/shokuknow`) was **not** read into this report beyond
  the path-existence checks already noted; the quarantine verdicts' substance is taken from the lane's own
  committed `quarantine-verdicts.md`, not re-derived.
- I did not open `w1/R35CriticClaims.md` before forming my own falsification list; M35-1..M35-4 in
  `corpus/lessons/round-35.md` were encountered afterwards and my findings F1–F12 agree with them where they
  overlap (F7↔M35-2, F9↔M35-3, F10↔M35-1) and extend them where they do not (F1–F6 on C1 are **not** in the
  round's own mistake list).
- The `ee0c865c` tip was mid-flight when I read it; a later commit may change C2's failure list. The
  `3ecf4298` and `aa04633a` figures are stable.

## 7. Files changed

- `.ufo/waves/round-35/w1/R35PlannerDataWalk.md` (this report) — the only lane write.
- `/tmp` fixtures (`r35-c1-contentfree`, `r35-c1-section`, `r35-c1-name`, `r35-c1-substr`, `r35-d1-fake`) —
  scratch, outside the lane, disposable.
