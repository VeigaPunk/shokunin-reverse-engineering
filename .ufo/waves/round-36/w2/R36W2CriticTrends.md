# R36W2CriticTrends — verdicts on the L1's proposed trends (round 36)

Seat: critic, round 36 wave 2. Target: the L1's proposed trend verdicts as dispatched in
`.ufo/waves/round-36/w2-spec.json` (prompt at line 235) against
`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md` and `CORPUS.md`.
Measured at integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` (lane HEAD is
`6f2ba761`, wave-1 results only: `git diff --stat 01a44dbf 6f2ba761 -- corpus/ SCORECARD.md
PROVINCE.md SHONEN.md SKILL.md tools/` is empty, rc 0, so committed tip and worktree agree on every
file I cite). During the wave, sibling wave-2 seats left uncommitted edits in the worktree
(`corpus/SOURCES.md` S107/S111 cells, the dependency entry's scope/attribution, the lesson's S109
quote count); this seat wrote none of them and pins every citation below to `01a44dbf`.
Judged on: coverage, calibration.

## Verdicts

| trend | L1 proposes | this seat | one-line reason |
|---|---|---|---|
| expansion | improved | **improved on the observables; `harmed` as landed at `01a44dbf`** | Two admitted entries with mined rows on ground the map did not hold, a Core row, a new capability row; but the assimilated entry fails a claim-vs-source check as landed (C-c), so the round is a trade until the wave-2 corrections commit. "Sources 106→111" is a registry count, not an observable |
| quality | improved | **harmed** (strict LEARNING clause) / `unchanged` if the supersession leg is withdrawn | `2026-10-13-r4u-03-unblob-extract.md` is untouched by the round — no mark, no trio — while the round's own record calls its statement superseded; the README Firmware row's mark lives only in a different row |
| discernment | unprovable-but-better pending the non-author closure | **unchanged** | No non-author spot-check exists on record (lesson `## Gate` has none; all w2 seats are lane-dispatched); "pending" is not an admissible verdict — LEARNING admits that label only through the gate |

Round 36 as landed at `01a44dbf` is therefore a **trade in both directions**, not learning
(LEARNING: "expansion: improved with `quality: harmed` is a trade, reported as a trade, never
admitted"). Both harm legs are repairable inside the round without touching any frozen instrument:
the C-c corrections are already in the worktree uncommitted, and the r4u-03 mark is one append plus
one inline pointer.

---

## 1. Expansion — `improved` on the observables, `harmed` as landed (C-c)

### What checks out

1. **Two admitted entries with `mined` rows, both opened 2026-10-26.**
   `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:1-3` cites S107/S108/S109;
   `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md:1-2` cites S110/S111.
   `git show 01a44dbf:corpus/SOURCES.md | grep -E '^\| S1(07|08|09|10|11) ' | awk -F'|' …` →
   status `mined` for all five; rows at `corpus/SOURCES.md:113-117`.
2. **Registry count 106 → 111 is literally true.**
   `git show cab59f22:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '` → `106`;
   `git show 01a44dbf:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '` → `111`.
   Caveat: this is not one of LEARNING's expansion observables, and `CORPUS.md` rule 4 is explicit
   — "The expansion trend counts admitted `knowledge/` entries whose `source:` cites a `mined` row
   on uncovered coverage-map ground. There is no row quota." The count is supporting evidence only.
3. **Ground the coverage map did not hold, and the map now maps both entries.** Base
   `corpus/README.md:44` (`git show cab59f22:corpus/README.md | sed -n 44p`) holds the Firmware row
   at "held (partial) — … AppImage SquashFS carved but recursion blocked by missing sasquatch", and
   base `corpus/README.md` Frontier carries "sasquatch (AUR) — unblob squashfs recursion; 7z
   fallback covers today." New coverage rows `corpus/README.md:89-90`; knowledge-index rows
   `corpus/README.md:195-196`; round row `corpus/README.md:224`.
4. **Frontier area entered.** `PROVINCE.md:368` `## Round-36 additions to Core`, row at
   `PROVINCE.md:372`, dated Frontier note at `PROVINCE.md:374` naming the superseded bullet
   (`PROVINCE.md:156`).
5. **One capability row, on new ground.** `SCORECARD.md:615` `## Capabilities`, new row
   `SCORECARD.md:627` ("REA SquashFS recursion through sasquatch (LE v4)"). Base evidence:
   `git show cab59f22:SCORECARD.md | grep -in squashfs` → no match (rc 1), so this is not a
   restatement of an existing capability. The other two `+` rows in the capabilities region of
   `git diff cab59f22 01a44dbf -- SCORECARD.md` are the C2 repairs (coverage row, pre-registered
   battery row), not new capabilities.

### Caveats (C-a and C-b sharpen the verdict; C-c voids it until fixed)

- **C-a — credit adjacency.** Entry 2 is the producer contract of the same surface entry 1
  measures. Both qualify under CORPUS rule 4 (distinct rows, distinct claims), but the round should
  count **one province move** (Frontier → Core), not two. The expansion verdict survives on one
  entry + Core row + capability row either way.
- **C-b — the admitted dependency entry overstates its own pin.** Its line 8 reads "both sources …
  pinned by tag/commit and sha256", but S111 is anchored "branch master, 30 lines, sha256
  `f09961ee…`" (`corpus/SOURCES.md:117`) — **no tag/commit**, i.e. the floating ref the gate's own
  correction c1 (lesson `## Gate`, decision 1) was applied to remove. The bytes are pinned; the
  revision is not. Minimal fix: record `devttys0/sasquatch` master head commit in S111's `anchor`
  and narrow the entry sentence to "S110 by tag+commit, S111 by branch head + sha256".
  (Uncommitted wave-2 edits are correcting S110/S111 scope and attribution in this entry and S111's
  `anchor`/`teaches` cells; they add a line-8 quote but still no commit pin, so C-b stands.)

  [INFERENCE] This is a documentation-level overstatement, not a false measured claim: the entry's
  load-bearing statement rests on S110, which is tag- and commit-pinned.
- **C-c — the assimilated entry fails a claim-vs-source check at the landed tip** (this is the
  LEARNING expansion-harm condition, "an admitted entry fails the bar it was admitted under").
  Two independent re-openings of S110 agree (this seat: `curl -fsSL …/26.6.4/README.md` → sha256
  `6544d60f…3716`, same bytes; wave-2 `R36W2ScoutS110.md` §1-3):
  1. **Unsupported attribution.** Entry line 30: "Because the producer calls its own extractor
     'Very beta'…". "Very beta." is S111, the **devttys0** README, and the entry's own line 41 says
     "neither README says so" about a fork relation between devttys0 and the onekey-sec package —
     so "the producer" (unblob/onekey-sec) is not the text that says it. The sentence is not
     labelled as inference; the entry contradicts itself.
  2. **Over-scoped framing.** Entry title and lines 10-12 make SquashFS support unconditionally
     conditional on an external extractor; S110's Docker route says "The Docker image bundles all
     extractors — no extra setup needed" (README line 64) and its Kali route is a plain
     `sudo apt install unblob` (lines 77-79). The condition holds for the pip route only
     (`### pip` at line 37, `### Docker` at 62).
  The uncommitted worktree already carries the fix (scope/attribution rewrites citing
  `R36W2ScoutS110.md` D1-D3). **The expansion verdict is `improved` only once that commit lands**;
  at `01a44dbf` it is not. Minimal safe correction: commit the in-flight corrections, and make the
  r4u-03 mark (see §2) in the same integration commit.

### Checked and not found

No admitted entry fails the bar it was admitted under on the measured surface: the C1 entry's own
`recheck:` command runs green (see §2, evidence Q-3), and the dependency entry's recheck digests
match live bytes (Q-2). I did **not** find a coverage-map row that contradicts the Core row.

---

## 2. Quality — the claimed supersession did not land; `harmed` under the strict clause

### The L1's three legs, tested

| leg | finding |
|---|---|
| README Firmware row's "recursion blocked by missing sasquatch" superseded | **half-landed**: the row is byte-identical base→tip; the mark is a dated note inside a *different*, new row (`corpus/README.md:89` "Dated supersession of the Firmware row's … (2026-10-13 state, kept as history)"). Consistent with the lane's "kept as history" practice, so acceptable for the map — but the map is not an entry and cannot carry the quality verdict |
| r4u-03 entry's sasquatch-blocked statement superseded by a measured entry | **not landed**: the entry is untouched by the entire round and no corpus document marks it |
| r34b provenance re-verified with an appended trio | **landed**: `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:75-79`, `git log -S 'Provenance trio' -- <that file>` → `01a44dbf`; `verified-at: 2026-10-26` appended; the trio's standing check holds (see Q-4) |
| no admitted entry failing a re-check | **sampled, not established**: three entries exercised green (Q-2, Q-3), 121 not exercised. The round asserts it globally without a sweep |

### The counterexample

`corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md`:

- **Untouched.** `git diff --stat cab59f22 01a44dbf -- corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md`
  → no output, rc 0. The round's knowledge diff is exactly three files
  (`git diff --name-status cab59f22 01a44dbf -- corpus/knowledge/` → `M` r34b, `A` the two r36
  entries).
- **No provenance trio at all**, so no freshness field to move: `grep -cE '^(source|verified-at|recheck):' <entry>`
  → `0`; the only date is an inline bullet `- verified-at: 2026-10-13` (lines 28, 54, 85, 127).
  `LEARNING.md` ("Files the path writes") requires entries to open with `source:`, `verified-at:`,
  `recheck:`; this entry predates that and the round left it so.
- **Stale present tense, now contradicted by Core.** Lines 129-132: "unblob-as-carver + 7z-as-reader
  is a working pipeline **TODAY** … Either install sasquatch (`pacman -S sasquatch` / AUR) or accept
  the carve-then-7z two-step"; line 178: "a working carve-then-7z pipeline today". After R36-C1 the
  native route is Core (`PROVINCE.md:372`, `SCORECARD.md:627`) and the route that actually worked was
  the official Debian package, not `pacman -S sasquatch` / AUR (lesson M36-1).
- **No pointer in either direction.** `grep -n 'r4u\|2026-10-13' corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`
  → no match (rc 1). The README rows naming the entry are byte-identical base→tip (see Q-5). The only
  round-36 text that names the entry is wave-1 seat prose, not a corpus document.

**Why this is `harmed` and not a reading quibble.** LEARNING's quality-harm condition is "an entry is
found false or stale and left unmarked". The L1's own proposed verdict asserts the statement *was*
superseded this round; the corpus records no supersession. Either the round found it (→ harmed, left
unmarked) or it did not (→ the "superseded" leg must be deleted, and `improved` then rests on the r34b
trio alone plus a 3/124 recheck sample, which is `unchanged`, not `improved`). Both readings deny the
clean verdict.

### Minimal safe correction (inside this round)

Append one dated block to the entry — e.g. `## Supersession (round 36)` — naming
`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`, correcting the "TODAY"/route
sentences to the measured state, and giving it the `verified-at: 2026-10-26` / `recheck:` pair; plus
one inline pointer on `corpus/README.md:44` (or on index row 164). With that landed, quality is
`improved` on three legs and the trade disappears.

---

## 3. Discernment — `unchanged`; `unprovable-but-better` is inadmissible as filed

LEARNING fixes the observable: "the gate decisions vs the outside spot-check", and the exploratory
label is "admitted only through this gate: a named non-author reviewer judges the change better with
reasons on record — never through self-attestation."

1. **No spot-check on record.** The lesson's `## Gate` (lines 23-48) carries sources, assimilation and
   quarantine only. `grep -nE 'agree|disagree' corpus/lessons/round-36.md` → one hit, line 48, and it
   is the lane comparing its own register to round 35 ("S150 … agrees with round 35"), not a
   non-author's verdict. `CORPUS.md:19-20` requires the lesson's `## Gate` to carry "spot-check
   result".
2. **No seat can supply it.** `grep -c 'non-author' .ufo/waves/round-36/w2-spec.json` → `1`, and that
   one occurrence is inside the L1's own proposed verdict text (my prompt at line 235). All 36 w2
   seats are lane-dispatched; LEARNING: "A subagent the lane dispatched is still the lane."
3. **The offered evidence is not the discernment observable.** 1 assimilation admit + 3 refusals and
   5 source admits + 1 rejection are gate *outputs*; QUALITY 77-78 are mistakes mined from lane-internal
   wave-1 critiques (`corpus/QUALITY.md:85-86`, correctly citing lesson M36-3/M36-4 and the wave-1
   reports). That is the `understanding` step (LEARNING step 3), not "gate decisions vs the outside
   spot-check". Neither can move discernment, however good it is.
4. **The reject side is not curated where the protocol puts it.** The one round-36 rejection (AppImage
   Specification) has **no SOURCES row**: `grep -c 'AppImageSpec' corpus/SOURCES.md` → `0`; the only
   `AppImage` match is S109's neovim row (line 115). Prior rejections are rows with
   `REJECTED: <reason>; flip: …` (S100 `corpus/SOURCES.md:106`, S105 `:111`), and `CORPUS.md:104`
   says a rejected row is "kept — a rejection is evidence of taste". LEARNING step 1: "Opened sources
   and rejected ones are curated in `corpus/SOURCES.md`". The rejection exists only in the lesson.
5. **No search-log note for 2026-10-26.** `sed -n '145,203p' corpus/SOURCES.md | grep -oE '2026-10-[0-9]{2}' | sort -u`
   → latest `2026-10-25`; the last registry note is "round 33". `CORPUS.md` rule 5 ("one prose note
   per bounded search … identified / screened / included / excluded counts, exclusion reasons") has no
   round-36 line, so the very counts the L1 cites (5 admits, 1 rejection, 1 located-not-appended) are
   not auditable from the registry.

**Verdict: `unchanged`.** Not `unprovable-but-better`, and not "pending": LEARNING has no pending
state for that label. The route to the better verdict is concrete: an outside reviewer (operator or a
fresh reviewer, explicitly not a lane seat) records `agree`/`disagree` with reasons for at least one
admit (e.g. S107 or the assimilated entry) and one reject (the AppImageSpec row, once it exists) in
`corpus/lessons/round-36.md`, and the lesson's `## Gate` gains that line.

---

## Evidence runs (exact)

- **Q-1 sources census** — `git show cab59f22:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '` → 106;
  `git show 01a44dbf:…` → 111; statuses S107-S111 → `mined` (all five).
- **Q-2 dependency-entry rechecks** — `curl -fsSL https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md | sha256sum`
  → `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716`;
  `curl -fsSL https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md | sha256sum`
  → `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef`; exit 0. Both match the stored
  anchors.
- **Q-3 C1-entry recheck, run verbatim** — `HYAKU_SCRATCH=$S bash tools/round-36/c1-run.sh after
  corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh "$S/recheck-out"` → rc 0;
  `jq -c '.normalized_result|{files:(.files|length),gaps:(.extraction_gaps|length)}' "$S/recheck-out/after.json"`
  → `{"files":3,"gaps":0}`; `after-run.json` → `sasquatch_version "unsquashfs version 4.5.1
  (2022/03/17)"`, `rea "rea-agents@6.5.0"`. Fixture sha256 matches `carriers.json` K1
  (`93802938…a589`).
- **Q-4 r34b standing check** — `corpus/SOURCES.md:112` (S106) `used-by` ends
  `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`.
- **Q-5 README rows** — `diff <(git show cab59f22:corpus/README.md | grep 'r4u-03-unblob-extract') <(git show 01a44dbf:corpus/README.md | grep 'r4u-03-unblob-extract')`
  → identical; same for line 44 (`sed -n 44p` both revisions → IDENTICAL).
- **Q-6 round knowledge diff** — `git diff --name-status cab59f22 01a44dbf -- corpus/knowledge/`
  → `M r34b`, `A` the two r36 entries.
- **Q-7 capacity/quality rows** — `corpus/QUALITY.md:85-86` cite lesson M36-3/M36-4 and
  `w1/R36CriticC2Shortcut.md` classes A1-A6 / `w1/R36CriticC1Shortcut.md` F1/F5.

Scratch: `S=/fast/scratch/hyaku/kaidoku-r36/R36W2CriticTrends`, created and removed at exit; no
`find`/`du` under `/fast/scratch`. No VCS mutation: read-only `git show`/`diff`/`log`/`grep` only.
No tool installed or upgraded this seat. No carrier, counter, oracle, receipt or predicate touched.

## Impacted axes

- **coverage** (expansion): verdict stands, but the round's expansion statement should drop
  "sources 106→111" as an observable and count one province move, not two.
- **depth / freshness** (quality): `harmed` until the r4u-03 mark lands — the entry that the round
  calls superseded still recommends the route the round proved stale, and carries no trio.
- **calibration** (discernment): `unchanged`; the calibration score move (C2 3 → 0) is a separate
  claim, not discernment, and cannot substitute for the missing outside spot-check.
