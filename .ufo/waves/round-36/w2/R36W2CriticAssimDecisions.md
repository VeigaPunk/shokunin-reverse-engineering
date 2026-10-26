# R36W2CriticAssimDecisions — attacking the round-36 assimilation decisions

Seat: critic, leaf, round 36 wave 2. Attacks the four `## Gate` assimilation decisions in
`corpus/lessons/round-36.md` (lines 41–44) and the expansion credit booked for the two new entries.
No counter, predicate, carrier, oracle, receipt, SOURCES row or knowledge entry was edited; no
subagent was dispatched; no VCS mutation; nothing installed or upgraded.

Tree state while reporting (`git rev-parse HEAD`): `6f2ba761bb5bcd6482d45523379376dcb6a386f6`.
`git diff --stat 01a44dbf..HEAD` touches only six `.ufo/` files; the lesson blob is identical at
`01a44dbf` and `HEAD` (`366daace55a3709abe5023aa9b9169c6896d521d`), so the decisions are read at the
assigned integration tip. **One caveat carried through this report:** the working tree carries an
uncommitted sibling edit to the admitted entry —
`git status --porcelain` → ` M corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`,
`git diff` header `index aa476af8..939a0839` — which repairs two defects found below. Findings judge
the **committed blob `aa476af8`** (what the Gate decided); the in-flight repair is cited as evidence
that the landed text did not meet the Gate's own bar, not as a fix.

## 0. Verdicts on the three assigned questions

**Q1 — should `unblob-sasquatch-dependency` have been refused?** Refusal was **not required on
QUALITY grounds** (after c1–c3 the entry meets #1/#2/#3), but the Gate's stated ground — producer
contract the lane did not hold — is **over-broad**: the entry's headline claim ("Unblob's SquashFS
support is a declared dependency on an external sasquatch extractor") was already in the corpus
since 2026-10-13 with the typed report verbatim (`corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md:18-19,105-108,130-131`),
and again in the C1 entry landed in the same commit
(`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:144-147`). Two facts are genuinely
new: the README's **pip-route** install instruction (S110 lines 43/49/52-53) and devttys0's
**self-description/build base** (S111 lines 12/17/26). So: **admit-on-correction was defensible only
if scoped to those two facts**; the version admitted (and the credit booked) presents a
third restatement of held ground as new knowledge. The connector recommended exactly `defer`
(`w1/R36ConnAssimilationTheme.md:101`); the Gate overrode it without recording a novelty sweep.

**Q2 — are the three refusals right?**

| decision | stated reason reproduced? | verdict |
|---|---|---|
| D2 `sasquatch-prebuilt-package-inventory` | **yes, both reasons** (first-hand: v4.5.1-6 body contains no `1.0`; v1.0 page shows 2 release files against 6 — "Assets 4" vs "Assets 8" — amd64-only per `R36ScoutPrebuiltInventory.md`'s API table) | refusal **right**; flip **incomplete**, and the treatment is **inconsistent** with D1 (F3) |
| D3 `sasquatch-unblob-compatibility` | reason 1 **yes** (rows S184–S186 are campaign-local; lane has no `lanes/`); reason 2 **false** — C1 measured LE v4 only and does **not** supersede the entry's `sasquatch-v4be`/big-endian exercise | refusal **right on reason 1 alone**; reason 2 must be struck (F4) |
| D4 `sasquatch-unblob-compatibility-precondition` | **yes** (both binaries present and digest-matching on this host) | refusal **right**; the lesson records **no flip** and the cited flip is itself insufficient (F5) |

**Q3 — is any expansion credit double-counted between the two new entries?** **No score or registry
credit is double-counted** (no SOURCES row lists both entries; the capability row cites the C1 entry
only; the coverage axis is `10 → 10` either way). One **fact** is booked twice: the dependency
contract is asserted in the admitted entry and was already held by `2026-10-13-r4u-03` and the C1
entry. Under fleet `CORPUS.md:123` rule 4 ("expansion … counts admitted `knowledge/` entries whose
`source:` cites a `mined` row on uncovered coverage-map ground") the admitted entry is a second unit
on ground that was already covered, so the round's "two entries added" (`SCORECARD.md:23,3394`)
overstates expansion units by one (F6).

## 1. Findings

### F1 — Decision 1's novelty premise is refuted by a lane entry a one-line sweep would have found

Strongest counterexample available locally. At the pre-landing tree (`d2e46ef5`, the revision the
gate seat itself read), before either new entry existed:

```
git grep -c -iE 'sasquatch' d2e46ef5 -- corpus/knowledge PROVINCE.md SKILL.md corpus/README.md
d2e46ef5:PROVINCE.md:1
d2e46ef5:corpus/README.md:3
d2e46ef5:corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md:14
git grep -c -iE 'ExtractorDependencyNotFoundReport|missing-extractor-dependency' d2e46ef5 -- corpus skills
… corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md:4
… corpus/evidence/round-36/c1/K{1,2,3,4}/before.json:1   (four lines)
```

What that entry already held, verbatim:

- `:18-19` — unblob's external-extractor matrix names `sasquatch` **and** `sasquatch-v4be`;
- `:105` — `{"severity": "ERROR", "dependencies": ["sasquatch"], "__typename__": "ExtractorDependencyNotFoundReport"}`;
- `:107-108` — "Command still returns ok:true — the refusal is per-chunk, typed, and non-fatal";
- `:130-131` — "`extract-firmware` will not recurse into squashfs in-process until `sasquatch` is installed";
- `:16-26` — the `unblob --show-external-dependencies` table itself (the verify command the S110
  scout recommends adding is already recorded as source on 2026-10-13).

The C1 entry landed in the same commit adds the handler declaration and the measured gap/continuation
(`…r36-sasquatch-squashfs-recursion.md:38-58,144-147`) plus the deb install provenance (`:130-138`).
The admitted entry's H1 (blob `aa476af8`, line 6) and its "Consequence 1" (lines 26-29) restate this.
Neither the lesson's Gate nor `w1/R36ScribeAssimilationGate.md` records a corpus sweep for the spelling
variants, although `corpus/QUALITY.md:67` (row 57) requires exactly that for a novelty claim
("every spelling … in PROVINCE.md, SKILL.md, corpus/README.md and corpus/knowledge contents").

Impacted axes: **coverage** (what the admission is credited with adding), **calibration** (the Gate's
novelty judgment). Smallest safe correction: one clause in the lesson's Decision 1 (or the entry's
intro) naming the two novel facts and cross-referencing `2026-10-13-r4u-03-unblob-extract.md:105-108`
as the ground already held — the entry then reads as a packaging/self-description note, not a second
dependency claim. No counter, source row or claim predicate is affected.

### F2 — Decision 1's corrections did not cover scope, and c1 was not fully applied to S111

Admitted text (blob `aa476af8`) vs its own source, first-hand on 2026-10-26:

| landed text | source bytes | verdict |
|---|---|---|
| H1: "unblob's SquashFS support is a declared dependency …" (unqualified, line 6) | README `:62-64` "### Docker (batteries included)" / "The Docker image bundles all extractors — no extra setup needed"; `:77-79` Kali is `sudo apt install unblob`; the external-tool step is pip-only (`:37-60`) | route overgeneralised — reproduced independently by `w2/R36W2ScoutS110.md` D1 |
| Consequence 2: "Because the producer calls its own extractor 'Very beta'" (line 30) | "Very beta." is devttys0's (S111 `:12`); the onekey-sec repo the lane runs serves `README` = 133 B, 9 lines, `grep -c -i 'very beta'` → **0** | attribution transferred across builds — `w2/R36W2ScoutS111.md` item 7 |
| Intro: "pinned by tag/commit and sha256" (line 8) | S110 is pinned by tag+commit; **S111 is pinned by branch `master` + sha256 only**, no commit | c1 ("pin by document") delivered for one of two sources — `w2/R36W2ScoutS111.md` item 1 |

`w1/R36ScribeAssimilationGate.md:161` states the flip as "any of c1–c3 not applied at landing … or the
re-opened README hashes differ". None of c1–c3 required a route qualifier, and the S111 pin gap was not
tested — so the flip could not fire on two of the three defects above.

Impacted axes: **calibration**. Smallest safe correction: extend the flip test in the lesson's Decision 1
beyond c1–c3 to "any claim not carried by the cited route/section", and fold the two wave-2 scouts'
D1/D2/D3 and item 1 into the decision record (the working-tree repair is already doing this — cite it
from the lesson so the correction is durable). Note the only SOURCES-side consequence I found is the
tier question on S111 (`w2/R36W2ScoutS111.md` §3, B vs A); `sources-census.sh validate` is unaffected
either way.

### F3 — Decision 2's reasons hold; its flip is incomplete, and its refusal line is not the one Decision 1 used

Reasons, reproduced first-hand today (GitHub REST was rate-limited: `curl …/releases?per_page=100` →
`API rate limit exceeded`; the tag pages were used instead):

- `https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6` — body is the three PR
  bullets plus contributors; it contains **no** `1.0`, and `4.5.1` appears only inside tag names
  (`sasquatch-v4.5.1-5...sasquatch-v4.5.1-6`). The staged claim "the release body shows the packaged
  upstream version (4.5.1) against the package version (1.0)" is therefore not sourced → reason (ii) holds.
- `…/tag/sasquatch-v1.0` — "**Assets 4**" (= 2 files + 2 source archives) against "Assets 8" on
  v4.5.1-6 (= 6 + 2), consistent with `R36ScoutPrebuiltInventory.md`'s API table (v1.0: amd64 deb +
  amd64 dbgsym only). The universal "each [release] carrying a Debian package per architecture" is
  false → reason (i) holds.

Two defects in the decision record:

1. **Flip incomplete.** The gate report records a third, independent defect the lesson omits — the
   row's own recheck does not reproduce (`w1/R36ScribeAssimilationGate.md:172`, `:297`: stored
   `grep -c` → 12, re-run → 13, `grep -o … | wc -l` → 18). The lesson's flip ("both corrected and
   re-opened") would admit the entry with the two corrected claims and the same irreproducible verify
   cell. Add "recheck replaced by an API form (`jq length`, per-tag asset counts) at a stated date".
2. **Inconsistent treatment [INFERENCE].** Decision 1 landed an entry with three corrections applied
   in place, including deletion of an unsupported provenance claim (c3: "fork"). Decision 2 refused an
   entry whose two defects are of the same class (a wrong quantifier; an attribution not in the
   source) and are one-line fixes. Neither the lesson nor the gate report states the line that
   distinguishes "correct at landing" from "refuse and re-open"; `CORPUS.md:123` rule 4 is silent on
   admission novelty. The plan's `≥1 admit / ≥1 reject` is satisfied without such a line, so the
   refusal stands, but an unstated rule is exactly what a later round will apply differently.

Impacted axes: **calibration** (gate consistency), **coverage** (the refused entry's surviving true
content — the three-architecture asset matrix, which `S107` records only for amd64 — stays outside the
corpus). Smallest safe corrections: add the recheck condition to the flip; state the correction-vs-
refusal test in one sentence, or land entry 3 with its corrections the way entry 1 was landed.

### F4 — Decision 3's second clause is false and contradicts three lane surfaces and the round's own connector

Lesson `:43`: "… and the lane's own R36-C1 receipts supersede it." Evidence against:

- C1 entry `:175` "Little-endian SquashFS v4 only" and `:180` "**No big-endian or AVM result.** All four
  carriers are LE v4 … nothing here exercises it";
- `PROVINCE.md:372` "`sasquatch-v4be` is its big-endian sibling, unmeasured";
- `SCORECARD.md:3396` planned round-37 coverage: "big-endian SquashFS v4 through `sasquatch-v4be`";
- the round's own connector, on this exact entry: "Adds the BE-branch exercise (`sasquatch-v4be`) that
  C1's frozen scope excludes" (`w1/R36ConnAssimilationTheme.md:142`), with the sibling note at `:151`
  "C1 does not claim BE/AVM — frozen 'Not claimed' line";
- the staged entry's distinctive evidence is `positive_be_v4` / `sasquatch-v4be` (staged S185).

Reason 1 of Decision 3 is verified and sufficient: `ls lanes` → absent in the lane, while
`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round8/work/lead3-sasquatch-compat.tsv` exists (2175 B,
read-only sibling root), i.e. the rows are not lane-retained bytes (QUALITY #1); S183 additionally cites
an unpinned `main` URL.

Impacted axes: **coverage** (a later round could read "superseded" and skip the BE exercise the
SCORECARD plans), **calibration** (a supersession claim is a provenance claim). Smallest safe
correction: replace the clause with "and the lane's own R36-C1 receipts supersede its LE v4 half only;
the entry's `sasquatch-v4be`/big-endian exercise is not held in-lane (C1 measured LE v4 only) and stays
Frontier."

### F5 — Decision 4 records no flip in the durable artifact, and its cited flip is insufficient

Lesson `:44` gives the reason and a pointer (`— R36ScribeAssimilationGate.md decision 4`) but no flip,
while Decisions 2 and 3 both state theirs. `corpus/QUALITY.md:45` (row 35) requires a rejected source
decision to keep "its stated reason **and** its flip condition". The cited flip
(`w1/R36ScribeAssimilationGate.md:205`) says the entry "becomes admissible only as an explicit
*superseded historical record*" if re-scoped to a dated snapshot — but the staged entry's own source row
is `S165 — lanes/kaidoku/round7/work/r7-local-measurements.tsv`, absent from the lane, and the gate
report does not mention it. Executing that flip as written would re-admit a row that still fails
QUALITY #1 (`corpus/QUALITY.md:11`) — the same ground Decision 3 refused.

The premise itself is verified first-hand on this host (2026-10-26):
`~/.local/bin/unblob --show-external-dependencies | grep -i sasq` → `sasquatch ✓`, `sasquatch-v4be ✓`;
`sha256sum` → `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` /
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; `sasquatch -version` →
`unsquashfs version 4.5.1 (2022/03/17)`. "Superseded premise", not "false when written", is the correct
calibration.

Impacted axes: **calibration**. Smallest safe correction: give Decision 4 the same one-line flip the
other two carry, with the missing condition: "dated 2026-10-24 snapshot **and** S165's evidence imported
into the lane, admitting row naming this refusal (QUALITY #35/#36)."

### F6 — One fact is booked twice; no score credit is double-counted

Credit channels checked one by one:

- **SOURCES.** `awk -F'|'` field 12 on `corpus/SOURCES.md:113-117`: S107–S109 carry
  `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` only; S110–S111 carry
  `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` only. No row lists both; no duplicate
  URL+scope; `sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-26` → **exit 0**,
  exactly the 9 pre-existing `W04` (the lesson's append-gate claim holds at HEAD).
- **Capability.** `SCORECARD.md:627` cites the C1 entry and the C1 receipts only.
- **Knowledge units.** `git ls-tree -r … | grep -c '\.md$'` → 122 at `cab59f22`/`d2e46ef5`, 124 at
  `ffc81341`/`HEAD`. Both new entries count, so `SCORECARD.md:23 "124/124 … two entries added"` and
  `:3394 "coverage 10 → 10 (… 122/122 → 124/124, two entries added and mapped)"` book **two units**.
- **Axis score.** `10 → 10` before and after; coverage is defined as "index integrity only, **not**
  fraction of the REA domain held", so nothing is inflated numerically.
- **The AUR-only correction** is supported independently by S107 (a Debian-package release exists) and
  by C1's own act (the lane installed from that deb, C1 entry `:130-138`), yet `M36-1`'s fix cell and
  `PROVINCE.md:374` credit the assimilated entry. That is attribution narrowing, not double credit.

The residual double count is thus **one fact, two entries**: the dependency contract is asserted in the
admitted entry (H1, Consequence 1, Consequence 3) and already held at `2026-10-13-r4u-03:105-108` and
`2026-10-26-r36-sasquatch-squashfs-recursion:144-147`. Under fleet `CORPUS.md:123` rule 4 the entry
still passes the *literal* test (its new `corpus/README.md:90` row did not exist before), but the test is
self-certifying: a coverage-map row written in the same commit makes its own ground "covered". The
material effect is on the expansion trend, not on any axis score.

Impacted axis: **coverage** (the round's expansion narrative). Smallest safe correction: one clause on
`SCORECARD.md:3394` — "(two entries added and mapped; **one** moved surface — the assimilated entry is a
packaging/self-description note on the same surface, not a second capability)", or book only the C1
entry as new coverage-map ground.

## 2. What I could not break (stated plainly)

- **Id collision and renumber map.** `106 / 132 / comm -12 → S106` reproduced from
  `.ufo/waves/round-36/assimilation/{reg-ids,staged-ids,collisions}` (`wc -l` = 106/132/1; content
  `S106`). Lane `S106` is the binutils readelf row (`corpus/SOURCES.md:112`). The by-document map in the
  lesson `:39` (staged S106 → S110 unblob README; staged S107 → S111 devttys0) matches the landed rows
  `corpus/SOURCES.md:116-117`, whose anchor cells carry "(staged as package S…, renumbered by document)".
  The gate report's earlier draft numbering (S107/S108) is stale superseded text, not a lane defect.
- **Append gate.** The lesson's claim is true at HEAD: census `validate` exits 0 with only the 9
  pre-existing `W04`; no `E01/E02/E03/E04/E09/E11` for the appended rows; `used-by` paths all resolve.
- **Decision 1's flip condition (README digests) has not fired.** Re-fetched today:
  `…/unblob/26.6.4/README.md` sha256 `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716`,
  235 lines; `…/devttys0/sasquatch/master/README.md` sha256
  `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef`, 30 lines; lines 43/49/52/53 and
  12/17/26 are exactly as the entries quote.
- **Decision 2's two stated reasons** (F3) and **Decision 4's premise** (F5) reproduce.
- **Decision 3's reason 1** reproduces.
- **Four corrections' targets** are present in the landed text (pins/commit for S110; labelled
  inference; re-scoped host-state; "fork" dropped) — except the S111 pin wording (F2).
- Nothing in the two refusal records smuggles a row append: `S130`, `S165`, `S183`–`S186`, `S189`–`S223`
  are absent from `corpus/SOURCES.md` (rows stop at S111 plus the pre-existing registry).

I found **no** evidence that the admitted entry's *facts* are false except the three scope/attribution
defects in F2, and **no** evidence that S110/S111 were fabricated, mis-hashed, or mis-renumbered.

## 3. Axes impacted

- **coverage** — F1 (novelty of the admitted entry), F3 (refused entry's held-out asset matrix), F4
  (BE supersession claim), F6 (expansion units). No axis score changes; the exposure is the round's
  narrative of what it added and what it may skip later.
- **calibration** — F1 (Gate novelty judgment without a QUALITY #57 sweep), F2 (landed text exceeding
  its source, with one correction only partly applied), F4 (false supersession), F5 (rejection without
  a flip condition).
- **depth** — untouched by this seat; no depth claim is reviewed here.

## 4. Smallest safe corrections (one line each; integration owner decides)

1. Lesson Decision 1: name the two novel facts (S110 pip-route install; S111 self-description/build
   base) and cross-reference `2026-10-13-r4u-03-unblob-extract.md:105-108` as already-held ground.
2. Lesson Decision 1: widen the flip to "any claim not carried by the cited route/section", and cite
   the committed wave-2 repairs (`w2/R36W2ScoutS110.md` D1–D3, `w2/R36W2ScoutS111.md` items 1/7) so the
   fix survives the working tree.
3. Lesson Decision 2: add "and the recheck replaced by the API form" to the flip; state the one-sentence
   correction-vs-refusal test.
4. Lesson Decision 3: strike ", and the lane's own R36-C1 receipts supersede it" — keep QUALITY #1 as the
   sole ground and record BE as unheld.
5. Lesson Decision 4: add the flip (dated snapshot **plus** S165's evidence imported), per QUALITY #35.
6. `SCORECARD.md:3394`: one clause recording that round 36 moved one surface, not two.

## 5. Commands run (exact; cwd = lane root unless stated)

| # | command | outcome |
|---|---|---|
| 1 | `git rev-parse HEAD`; `git log --oneline cab59f22..HEAD`; `git diff --stat 01a44dbf..HEAD`; `git rev-parse 01a44dbf:corpus/lessons/round-36.md HEAD:…` | `6f2ba761`; 7 commits (`790561d4`…`6f2ba761`); only `.ufo/` files differ after `01a44dbf`; lesson blob `366daace` identical |
| 2 | `git grep -c -iE 'sasquatch' d2e46ef5 -- corpus/knowledge PROVINCE.md SKILL.md corpus/README.md` | `r4u-03:14`, `PROVINCE.md:1`, `corpus/README.md:3` |
| 3 | `git grep -c -iE 'ExtractorDependencyNotFoundReport\|missing-extractor-dependency' d2e46ef5 -- corpus skills` | `r4u-03:4`; `c1/K{1,2,3,4}/before.json:1` each |
| 4 | `git diff -- corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`; `git hash-object` that file | uncommitted repair, `aa476af8 → 939a0839` |
| 5 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-26` | **exit 0**, 9 `W04`, no E-code |
| 6 | `awk -F'\|'` on rows S107–S111 (field 12 = used-by) | single entry per row, no row with both |
| 7 | `curl -fsSL …/unblob/26.6.4/README.md`, `…/devttys0/sasquatch/master/README.md`; `sha256sum`; `sed -n '43p;49p;52p;53p'`, `sed -n '12p;17p;26p'`; `sed -n '35,90p'` | digests/lines reproduce; Docker `:64`, Kali `:77-79` |
| 8 | `read` of `…/releases/tag/sasquatch-v4.5.1-6` and `…/tag/sasquatch-v1.0` | body has no `1.0`; "Assets 8" vs "Assets 4" |
| 9 | `curl -sS 'https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100'` | **403 rate limit** (fell back to #8) |
| 10 | `~/.local/bin/unblob --show-external-dependencies \| grep -i sasq`; `sasquatch -version`; `sha256sum ~/.local/bin/sasquatch{,-v4be}` | `sasquatch ✓`, `sasquatch-v4be ✓`; 4.5.1; `ad02d27a…`/`fac88740…` |
| 11 | `curl -fsSL https://raw.githubusercontent.com/onekey-sec/sasquatch/main/README` | 200, 133 B, 9 lines, `grep -c -i 'very beta'` → 0 |
| 12 | `git ls-tree -r --name-only <rev> -- corpus/knowledge \| grep -c '\.md$'` at base/d2e46ef5/ffc81341/HEAD | 122 / 122 / 124 / 124 |
| 13 | `ls -d lanes`; `ls -l /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round8/work/lead3-sasquatch-compat.tsv` | lane absent; sibling file 2175 B |

## 6. Disclosure

- **Writes:** only this file. No lane edit, no counter/predicate/carrier/oracle/receipt/SOURCES change,
  no knowledge-entry repair. The uncommitted entry diff is another seat's work; I did not touch it.
- **VCS:** read-only (`rev-parse`, `log`, `diff`, `grep`, `ls-tree`, `hash-object`, `status`). No
  add/commit/checkout/reset/stash/pull/push, no jj. No fixture repo was needed.
- **Installs/upgrades:** none; no pacman, `uv`/`npx`/`npm`, and no `~/.local/bin/sasquatch*` change.
- **Scratch:** `S=/fast/scratch/hyaku/kaidoku-r36/R36W2CriticAssimDecisions`, `TMPDIR=$S`, removed after
  each network step; no `find`/`du` under `/fast/scratch`; nothing cited here lives under `/tmp` or
  scratch.
- **Limits:** `[INFERENCE]` where marked (notably the fairness of the D1/D2 asymmetry charge and the
  self-certifying-coverage reading of `CORPUS.md:123`). GitHub REST was rate-limited, so release-inventory
  facts rest on tag pages plus the committed `R36ScoutPrebuiltInventory.md` API table; I did not re-run
  any counter, harness or REA command, and I did not read `shokuknow` beyond the two named staged entries
  and the one cited tsv.
