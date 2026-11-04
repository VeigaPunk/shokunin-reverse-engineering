2026-11-03
# ConnectorCross — sibling-overlap scan, round 67 wave w1 (read-only)

Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin (head read only). 19 sibling lanes scanned
in the working tree; sibling HEADs pinned in §0 so every citation below is attributable.
R67 base a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92, operative freeze 3663e6b21dccf4c4957f459301156664d8b151d6.

Method limits, stated up front:
- Working-tree greps plus `git -C <lane> rev-parse HEAD`. No sibling gate, counter, selftest or
  battery was executed. Nothing was written outside this seat directory and
  `/fast/scratch/hyaku/kaidoku-r67/ConnectorCross` (deleted before yield).
- The two "also mentions selftest" columns in §2 are a candidate-pool size, not a classification:
  `grep -l 'selftest'` over files that mention mutation proves only co-occurrence. Only the files
  actually read are classified; every unread candidate is left unclassified and uncounted as a match.
- No sibling HEAD was compared across time (single read each).

## 0. Sibling HEADs (`git -C <dir> rev-parse HEAD`, rc 0 for all)

| sibling | HEAD |
|---|---|
| audio-shokunin | f9da7ee97e0ba95da1803c2afe9c616c519bae18 |
| chousa-shokunin | f748abbb6bf58388e732facd4ecec5612419c457 |
| game-dev-2d-shokunin | 1e033ef053beedf9a201daa21fbeb9c8b2f72dc3 |
| game-dev-3d-shokunin | 39ca3973c7865456d97fae18033f3f460c6cf8c1 |
| kagi-shokunin | 6191805a47f54dc2e922080129e1dd2b89390df2 |
| kake-shokunin | 783c7c13db1289ce86653c367d5904593f3a01cf |
| kama-shokunin | e2b860c8907a4ba122dbbf5f2b2188695fb7c5f5 |
| kasegi-shokunin | c81eef717ee72f6911b0155992e52299403a56da |
| kengaku-shokunin | 0ef40526d1855c152df188e0f4421914664d5f40 |
| kotoba-shokunin | 1c8f37edf2e5ac0fb3c2be1c88e32406313fe47b |
| kotodama-shokunin | c285b2afb19d4b64320e18df1f55e426bf2d0b0c |
| kumitate-shokunin | 3c369336218329e30248b5d69c41348c02658169 |
| lore-shokunin | 0f044aa7c7e4e17cfd5b6278179709b60db45d61 |
| mado-shokunin | 92151a50cc79b40700cafab98488012089f67e34 |
| mori-shokunin | 84c6cbc3b47c536a504aaee329c77897d389935e |
| revenger-shokunin | 5915ad8d71c19ad377829d130ba1c35445eb32a4 |
| souji-shokunin | 83d3813257648e99fb4ab2ddef217124f39cf324 |
| tabi-shokunin | 57b29bade4b05b03cdb8fa151daec90ac9b1a29c |
| tameshi-shokunin | a3dd35742eee608d1205843dacebc461b4242b9e |
| tsukuroi-shokunin | 0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e |

## 1. Question (a) — SquashFS gap/class-accounting rule; device-node publication rule

### Commands

```
# C1 per-lane breadth (prose included), used only to find candidate lanes
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do case "$d" in *kaidoku*) continue;; esac;
  n=$(grep -rIl --exclude-dir=.git --exclude-dir=.jj --exclude-dir=reports --exclude-dir=considerthese \
      -E 'char-device|block-device|nonregular|squashfs' "$d" 2>/dev/null | wc -l); echo "$(basename $d) $n"; done

# C2 squashfs in the surfaces where a rule could live
grep -rIl --exclude-dir=.git --exclude-dir=.jj -E 'squashfs' \
  /home/vgpnk/Projects/shokunin/*-shokunin/tools \
  /home/vgpnk/Projects/shokunin/*-shokunin/*.md \
  /home/vgpnk/Projects/shokunin/*-shokunin/plans 2>/dev/null | grep -v kaidoku        # -> no output

# C3 squashfs anywhere in any sibling tools/ (case-insensitive)
grep -rIl --exclude-dir=.git --exclude-dir=.jj -i 'squashfs' \
  /home/vgpnk/Projects/shokunin/*-shokunin/tools 2>/dev/null | grep -vc kaidoku        # -> 0

# C4 device-node vocabulary in any sibling tools/
for d in ...; grep -rIl -E 'S_IFCHR|mknod|device node|char device|character device' "$d/tools"; done

# C5 full-tree squashfs, counted by surface (to explain the breadth hits)
grep -rIl --exclude-dir=.git --exclude-dir=.jj -i 'squashfs' *-shokunin | grep -v kaidoku
```

### Hit counts

| search | hits outside kaidoku |
|---|---|
| `squashfs` in sibling `tools/` (C2, C3) | **0** |
| `squashfs` in sibling root `*.md` and `plans/` (C2) | **0** |
| `squashfs` full tree (C5) | 134 files: 90 under `.ufo/`, 48 under `tests/`, 20 under `census/`, 5 under `corpus/`, 3 under `reports/`, **0** in `tools/` or root docs |
| `S_IFCHR\|mknod\|device node\|char device\|character device` in sibling `tools/` (C4) | **1 file** |

C1 breadth (all surface, prose included), per lane: audio 0, chousa 5, game-dev-2d 0, game-dev-3d 0,
kagi 0, kake 41, kama 176, kasegi 4, kengaku 3, kotoba 0, kotodama 0, kumitate 6, lore 0, mado 68,
mori 138, revenger 5, souji 228, tabi 27, tameshi 149, tsukuroi 51. The high counts are the word
"disposition" in prose and wave records; none is a filesystem entry-class rule (see §1b).

### Classification

| id | lane | path | class | basis |
|---|---|---|---|---|
| A-1 | — | — | **NO OWNER** | No sibling `tools/`, root doc or `plans/` file mentions SquashFS at all. The four corpus/report hits are source snapshots and prose: mori `corpus/evidence/sources-r55/statfs.2.man-pages-6.19` (man page), souji `census/round-27/sources/glocalfile.c` (GLib source snapshot), revenger `reports/round-73/bf-source-pack/format-obscura.md` and `reports/round-73/source-id-map.tsv` (RE format atlas entries). None is a rule, gate or counter. |
| A-2 | tsukuroi | `tools/score-census-handoff-r32.py:336` | different scope (measurement, not policy) | The single device-node hit in all 19 lanes: a comment `# root metadata arm, pci inventory, device nodes`. It inventories device nodes for a root-metadata census arm; it does not decide whether a device node is publishable. No sibling rules on publication by entry class. |
| A-3 | kama | `tools/census-waiver-boundary.py` | same *shape*, different surface — cite as precedent | A frozen 7-case boundary over the host census: per-class disposition where an evaluated failure is not waivable ("a failure is not waivable", case 4) and a not-evaluated member is (case 3), with `--json`, an exit-2 could-not-evaluate, and a specificity case (case 7: "the landed census bytes stay green"). This is a class-disposition rule over *census members*; R67-C1's class disposition is over *filesystem entry classes*. Same reasoning pattern, different subject. |
| A-4 | tameshi | `tools/evidence-disposition.py`, `tools/pin-disposition.py` | different scope | `evidence-disposition.py`: "does one dispositions document account for every frozen round-13 expected check exactly once". `pin-disposition.py`: pin/content byte identity with `result_reuse=not_established`. Both are dispositions over *evidence expectations and pins*, not over entry classes. Not a gap-rule precedent. |

Verdict for (a): **no sibling lane owns a SquashFS gap/class-accounting rule and none owns a
device-node publication rule.** R67-C1's `class_disposition` block has no competing owner. The nearest
same-shape precedent is kama's waiver boundary (A-3) and it must be cited as a precedent for
"per-class disposition stated in a docstring-frozen predicate", not claimed as novel.

## 2. Question (b) — a mutation-score battery that binds a counter's own selftest

### Commands

```
# D1 candidate pool per lane: files in tools/ mentioning mutation, and of those, how many also say selftest
for d in ...; hit=$(grep -rIl -E 'mutant|mutation' "$d/tools"); sel=$(echo "$hit" | xargs grep -l -E 'selftest');
  echo "$(basename $d) mutant-files:$(echo "$hit" | wc -l) also-selftest:..."; done

# D2 inventory of instrument-shaped names
ls /home/vgpnk/Projects/shokunin/*-shokunin/tools/*receipt* \
   /home/vgpnk/Projects/shokunin/*-shokunin/tools/*revision*
```

### Hit counts (D1 candidate pool; co-occurrence only)

| lane | tools/ files mentioning mutant\|mutation | of those also containing "selftest" |
|---|---|---|
| souji | 43 | 41 |
| tsukuroi | 32 | 26 |
| kama | 21 | 12 |
| kotodama | 13 | 11 |
| tameshi | 13 | 13 |
| mori | 13 | 12 |
| mado | 9 | 9 |
| chousa | 5 | 3 |
| audio, game-dev-2d, game-dev-3d, kagi, kake, kasegi, kengaku, kotoba, kumitate, lore, revenger, tabi | 0 | 0 |

### Classification (files actually read)

| id | lane | path | class | basis |
|---|---|---|---|---|
| B-1 | kama | `tools/release-recheck-selftest-extra.py` | **SAME CLASS** | Docstring: "Additional selftest cases for tools/release-recheck.py … Each case kills one mutant that the built-in selftest (`release-recheck.py selftest`, 5 cases) fails to kill. Mutation-testing evidence is in mutants.tsv beside this file. … Against the pristine tool all 15 cases pass; against each survivor at least its target case fails (several cases also kill neighbours, which is fine)." It carries an explicit case→survivor map (15 cases, named survivors such as `R1-first-match`, `D1-keep-dates`) and a pristine-stays-green requirement. This is the same instrument class as R67-C2: a separate case set bound to the frozen tool's own selftest, killing survivors the built-in selftest cannot see. |
| B-2 | kama | `tools/census-waiver-boundary.py` | same family, different target | Separate harness that loads the frozen census in-process, adds 7 cases the census's own selftest cannot express, requires the landed bytes to stay green (case 7) and refuses to report a silent 0 (exit 2 could-not-evaluate). Mutation-adjacent boundary work; targets waiver classes, not mutants. |
| B-3 | tsukuroi | `tools/score-counter-cheats-r51.py` | adjacent, different mechanism | Builds five cheat censuses (liar, braced-spell, echo-spell, neutered, self-checking liar) and scores a matcher counter against them, with `r50_cheats_rejected` as a sensitivity control. It tests the counter against *adversarial substitutes*, not against byte mutations re-scored by a new selftest. |
| B-4 | tameshi | `tools/pin-disposition.py` | different scope | Governs pin/content identity for recorded mutation legs and explicitly refuses to transfer results: "Every row carries result_reuse=not_established." Not a mutant-kill battery. |

### Contradiction recorded, not absorbed

B-1's docstring names `mutants.tsv` beside the tool as the mutation evidence. `ls -l
kama-shokunin/tools/mutants.tsv` → **absent** at kama HEAD e2b860c8. The tool is present and the
referenced evidence file is not in the tree. I did not resolve or repair this — it is a kama-side
doc-pointer gap, reported here because it is the one defect this scan found and because citing B-1 as
a precedent would otherwise imply its evidence is locatable. [INFERENCE] the tsv may have been
authored in a wave directory rather than `tools/`; I did not search for a renamed copy.

Verdict for (b): **a selftest-binding mutation battery of R67-C2's class already exists (B-1, kama).**
R67-C2's novelty must be scoped to its object, not its class: two nameless-by-design frozen counters
loaded by path under sha256 pins, each survivor killed by a case composed onto its own selftest
surface, with a before/after score (`killed_before 0`, `killed_after 2`) plus a `--control` arm that
runs the round-66 selftests alone. B-1 has the case-set shape but no before/after scoring and no
pin-loaded frozen bytes in its stated contract.

## 3. Question (c) — a receipt-revision convention for gate receipts

### Commands

```
ls /home/vgpnk/Projects/shokunin/*-shokunin/tools/*receipt* /home/vgpnk/Projects/shokunin/*-shokunin/tools/*revision*
grep -rIl --exclude-dir=.git --exclude-dir=.jj -E 'receipt' /home/vgpnk/Projects/shokunin/*-shokunin/tools | wc -l   # 454
```

| id | lane | path | class | basis |
|---|---|---|---|---|
| C-1 | tameshi | `tools/receipt-revision-gate.py` | **SAME CLASS, direct precedent** | "bind a receipt to the revision it certifies … a positive control was scored at the FREEZE commit, which predated the work it certified, and every gate in the lane accepted it because none compared the `rev=` a receipt names with the revision under test. A verdict, or a positive control, is evidence only for the content it was measured against." Roles `positive`/`verdict`/`control`; 11 named refusal codes (`RECEIPT_REV_ABSENT`, `RECEIPT_REV_MISMATCH`, `RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_CONTROL_NOT_ANCESTOR`, …); `GATE: receipts=N ok=N refused=N` line, exit 3 on refusal; `--selftest`. |
| C-2 | tameshi | `tools/receipt-commit-bind.py` | same family, different axis | Binds receipt *names* in a commit message to the bytes the commit carries: "an empty commit carries no content, so it can never satisfy a receipt claim made in its own message". Name→tree resolution over a range; C-1 is rev→content. Complementary conventions, both landed. |
| C-3 | tsukuroi | `tools/check-revision-binding.py` | same family, judge over gates | 1591-line read-only judge asking "are the `--revision` gates bound to a landed revision, and do they all bind the same way?", with BOUND and CONSISTENT contracts, a shared `tools/_revision.py`, and a deliberate independent implementation ("it grades the tools and must not share what it grades"). |
| C-4 | kama | `tools/round33-gate-receipts.py` | same family, gate-receipt capture | "Capture runs the gate code from a pinned lane revision against that revision … Audit reads only committed receipt blobs and replays each case from its pinned source revision; the lane repository is never mutated." Receipts are revision-pinned and replayable. |
| C-5 | kotodama, mado, mori, chousa, souji, tsukuroi | `check-receipt-seq.py`, `mado-receipt-citecheck.py`, `mori-receipt-complete.py`, `receipt-pin.py`, `souji-receipt-run.py`, `append-receipt.py` / `receipt-write.py` / `run-receipt.py` / `check-cited-receipts-r62.py` | same family | 454 tools across the fleet mention receipts; at least six lanes carry a receipt-sequence, receipt-completeness, receipt-citation or receipt-pinning gate. |

Verdict for (c): **the receipt-revision convention is established and multiply owned.** A round-67
gate receipt naming `rev=3663e6b2…` applies C-1's rule; it does not introduce a convention. Any wave
text that presents revision-binding on receipts as an R67 invention would be an overclaim.

## 4. Counts

- Lanes scanned: 19 siblings (all `*-shokunin` except kaidoku). HEAD pinned for all 19.
- Questions: 3. Answers: (a) no owner, (b) same-class precedent found, (c) established class.
- Files read in full or in part for classification: 12 (listed in §1b, §2, §3 rows).
- Same-class precedents: 2 (B-1 mutation battery; C-1 receipt-revision gate). Same-shape precedent: 1
  (A-3 class disposition). Different-scope hits: 4 (A-2, A-4, B-3, B-4). No-owner findings: 1 (A-1).
- Executed sibling instruments: **0**. Writes: this directory and scratch only.
- Installs/upgrades: none needed; none performed.
