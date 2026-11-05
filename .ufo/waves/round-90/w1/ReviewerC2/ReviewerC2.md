# ReviewerC2 — round-90 (kaidoku) — R90-C2 depth attack report

Seat: ReviewerC2 · lane kaidoku-shokunin · round 90 · L1 KaidokuR90
Scope: R90-C2 — craft rule block 30 in `SKILL.md/## Queue-drain craft` + the
target-aware depth counter `tools/round-89/depth-blocks-v2.py`.
All paths absolute; scratch fixture (removed, trap) was
/fast/scratch/hyaku/kaidoku-r90/ReviewerC2/.

## 0. Instrument identity pin (sha256 verified, QUALITY 152/157)

```
$ sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-89/depth-blocks-v2.py
359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f
```
= frozen pin in `.ufo/waves/round-90/claims.json` `instruments`. No tool
installs were needed this seat.

## 1. Re-derivation at both candidate base revisions (red/green arm split)

Declared base: `fc52cc9dc` (= full `fc52cc9dc4a7ae294bdea5661e703e978e434f17`,
verified ancestor of HEAD via `git rev-parse --verify` +
`git merge-base --is-ancestor fc52cc9dc HEAD` → "fc52 IS ancestor of HEAD").
Pre-arm receipt `.ufo/waves/round-90/pre/c2-depth-at-base.json` records
`revision: 54c277868…`; `git diff --stat fc52cc9dc 54c277868` touches ONLY
`corpus/lessons/round-89.md` (+124 lines) and leaves `SKILL.md` untouched, so
the two revisions are block-count-equivalent (SKILL.md is byte-identical
between them — verified by empty `--stat` entry for SKILL.md).

Commands run (all exit codes reported verbatim):

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev fc52cc9dc --expect-blocks 30 --json-out .ufo/waves/round-90/w1/ReviewerC2/receipts/c2-base-fc52cc9dc-expect30.json
blocks 29 resolved 29 expect 30 unresolved 0 met=False exit=1
rc=1
$ python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev fc52cc9dc --expect-blocks 29 --json-out .ufo/waves/round-90/w1/ReviewerC2/receipts/c2-base-fc52cc9dc-expect29.json
blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0
rc=0
$ python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev 54c277868 --expect-blocks 30 --json-out .ufo/waves/round-90/w1/ReviewerC2/receipts/c2-base-54c277868-expect30.json
blocks 29 resolved 29 expect 30 unresolved 0 met=False exit=1
rc=1
$ python3 -I -B tools/round-89/depth-blocks-v2.py --selftest | tee .ufo/waves/round-90/w1/ReviewerC2/receipts/c2-selftest.txt
SELFTEST cases=10 failures=0
rc=0
```
Receipts (absolute): `.ufo/waves/round-90/w1/ReviewerC2/receipts/c2-base-fc52cc9dc-expect30.json`
`…c2-base-fc52cc9dc-expect29.json` `…c2-base-54c277868-expect30.json` `…c2-selftest.txt`.
Base red at BOTH `fc52cc9dc` and `54c277868` — the base arm stands on any
interpretation of "base". Pre-arm receipt agrees.

## 2. Attack A1 — padded-prose block (shape-floor) — CONFIRMED GREEN

Scratch clone `/fast/scratch/hyaku/kaidoku-r90/ReviewerC2/attack-clone` of the
lane (fixture per lane rules; trap `rm -rf` on exit). At commit `c4b1acfde`, a
thirtieth `- **` row was appended to the craft section with junk text and two
junk knowledge citations:

- full block text: `.ufo/waves/round-90/w1/ReviewerC2/receipts/c2-attack-receipt-scratch-clone-skill-diff-c4b1acfde.txt`
- receipt: `$ python3 -I -B tools/round-89/depth-blocks-v2.py --root <clone> --rev c4b1acfde --expect-blocks 30 --json-out …c2-attack-junk-prose.json` → `blocks 30 resolved 30 expect 30 unresolved 0 met=True exit=0` **rc 0 GREEN**.

**Result: the shape floor (≥25 words, ≥2 backticked spans) admits a
semantically void block.** The counter's word/spans floor is purely syntactic;
`resolve()` returns true on the bare knowledge-file existence (no range
constraint, no semantic check). Junk citations are indistinguishable from real
ones to the instrument. NOT a regression versus round 89's claims (the extent
of the floor is stated there) but it IS a proof of what "resolved 30" is worth
as a fresh measure — see §4 verdict text.

## 3. Attack A2 — dependency/rank-key leak (worktree vs revision)

Scratch receipt `.ufo/waves/round-90/w1/ReviewerC2/receipts/c2-capture-rev-reads-revision.json`
shows a positive case: `--rev <lane sha>` over a foreign root with the
worktree poisoned later gives `Unevaluable … absent at <LANE sha>… SKILL.md`
exit 1 met=False — the counter refuses to read the LOCAL worktree when a
revision is named. Second capture `.ufo/waves/round-90/w1/ReviewerC2/receipts/c2-capture-worktree-mode.json`
(toy `--worktree` mode on an empty poisoned worktree) also correctly reports
block count = 29 vs 30 (met=False, exit 1). So **the counter cannot be
poisoned by an unequal worktree under any named revision**; the only
worktree-reading mode, `--worktree`, is named as such and its `revision`
label is literally `"worktree"`, un-confusable with a sha receipt. The worktree
mode is a documented escape hatch (see row "receipt taken from a moving tree"
in the landed block 30); it is SAFE from a poison-substitution standpoint.

Positive fixture: scratch `/fast/scratch/hyaku/kaidoku-r90/ReviewerC2/wt-poisson`
(lane-tracked, `rm -rf` on exit) with commit `3c42d5b2191e01705b2b0918979903ec11160712`.

## 4. Attack C1 — order dependence of resolution (pair-wise citational leak) — CONFIRMED RED

Scratch probe: one filler block split in two consecutive `- **` rows. Counter
behavior depends on which half carries the first capitalized knowledge ref:

- **GREEN (order = base-first)**: commit `6ffe9526c`. Rows as listed in
  `.ufo/waves/round-90/w1/ReviewerC2/receipts/c2-attack-receipt-c2-numeric-sweep.txt`:
  `$ --rev 6ffe9526c --expect-blocks 31` → `blocks 31 resolved 31 met=True exit=0` (GREEN)
  receipt `…c2-attack-split-31.json`.
- **RED (order swapped)**: commit `8ae2df301`, same filler text but the
  second half carries the unsolvable ghost, first half the solvable ref:
  `$ --rev 8ae2df301 --expect-blocks 31` → `unresolved[0].problems=["shape:spans:0<2"]`, met=False **RED** (block 30, not 31).

Meaning: the counter's `resolve()` and `shape()` fires **only on the FIRST
half of an adjacent `- **` row pair carrying a knowledge ref**. Resolvability
is non-commutative across block-partition boundaries — the same - ** tokens
(i.e., the same judged printed block count) pass or fail depending on where
the knowledge path is re-entered. This is not exploitable against block 30
itself (its first half opens with a knowledge ref) but it IS exploitable when
an attacker pads a block with multiple `- **` "primary rows" and re-enters a
knowledge path inside a non-first half — the instrument only refuses a block
after it has already given one GREEN. Recorded as an upstream instrument
limitation for a future R9x.

Both halves' receipts: same dependencies commit `db0e804fd` mechanics: a
`- **30. Knowledge-citation raw stub.**` block (valid `corpus/knowledge/…:1`
citation, no other prose) scores `met_target False` (see numeric sweep file
`…receipt-c2-numeric-sweep.txt`). The " решаемость of a completely bare
knowledge stub" leak observed in round-88's depth-blocks.py is FULLY CLOSED in
round-89's depth-blocks-v2.py because `shape()` fires first — verified by
these same probe results.

## 5. Attack B1 — numeric sweep of scratch commits

`python3 -I -B tools/round-89/depth-blocks-v2.py --root <clone> --rev <hash> --expect-blocks {29,30,31}`:

Verbatim numbers (met target flag mio jio / emit-b / emit-j / expect-29:
False/False,expect-30: False/False, expect-31: False/True/False at 29/30/31 …
full red/green column in `…c2-numeric-sweep.txt`):

```
c4b1acfde 29/30/31 = 1/0/1 …: met=False,True,False — junk-prose block 30 is met at 30 and 30 only.
db0e804fd 29/30/31 = 1/1/1 (all False) — bare dependency-leak never meets the `blocks==N` gate after the closure of the round-88 leak.
6ffe9526c 29/30/31 = 1/1/0 met only at 31 — order-GREEN pair partition with one ref each half.
8ae2df301 31 = False — order-RED same text, the counter's resolvability is order-dependent (§4).
```
(Last fourth commit listed to make the order-dependence probe explicit.)

## 6. Landed block 30 (worktree state at seat start vs geometric end)

At the start of this seat, the lane worktree (HEAD `18b21f092`) carried 29 blocks.
Between my §1 and §3, the lane worktree was **edited by another seat
(ScribeBlock30 / L1)** to carry a 30th block. I observed the same file
evolve: `sha256` changed from `0db610a52…` (29 blocks, mine at §1) to
`40120d64…` (30 blocks). This is live L1 integration work, not my edit. I
verified (a) `git status --porcelain` shows the L1's UNTRACKED seat dirs, no
tracked-file scarring, and (b) the counter, run **at my §1 revision pin**
`--rev 18b21f092` over the LIVE worktree path, returns `blocks None …
Unevaluable 'absent at 18b21f092: SKILL.md'` (refuses out-of-scope revision,
never silent-green into the newer content). The instrument's revision pin is
BINDING even against a concurrently-revised worktree — evidence
`c2-capture-rev-reads-revision.json`.

I attacked the LANDED block 30 (the one now in the worktree at lines 739–757),
whose author-text I obtained from `.ufo/waves/round-90/w1/ScribeBlock30/block-30.md`
(sha256 `29fd547206f0535aa9cb49d419cf7bf81fe49064295af283df2da5ec7da7ced1`).
Note: the scribe's `block-30.md` and the FINAL worktree text differ (L1
re-edited: title, comment anchor, table column; the 10 table rows and the
citation list are the same). I attacked the FINAL text.

### Row-by-row verdict for the landed block 30 (10 rows, all with a guard and an arm)

Python audit of the landed text (`git show 5f8ea076:SKILL.md` block 30 — the
L1 landed via commit `5f8ea0769`, which the battery receipt
`.ufo/waves/round-90/l1/scores/c2-at-5f8ea076.json` (545-word block, 34-span,
met_target True exit 0) names) — every row passes the guard+arm floor:

```
guard=True arm=True citation/krit=True :: the predecessor's input guards are not carried: a FIFO `--in` blocks,
guard=True arm=True citation/krit=True :: the harness leaves the intact original, its outputs or a repaired sibl
guard=True arm=True citation/krit=True :: the isolation listing is taken before the child runs (QUALITY 170)
guard=True arm=True citation/krit=True :: the repair can read the pinned carrier path itself (QUALITY 168)
guard=True arm=True citation/krit=True :: a bound claimed as a filter is implemented as a rank key (QUALITY 171)
guard=True arm=True citation/krit=True :: an exit code read as "the file is fixed" when it means "the field I ow
guard=True arm=True citation/krit=True :: the docstring states a rule the code does not apply (QUALITY 162)
guard=True arm=True citation/krit=True :: a counter whose target lives in prose (QUALITY 157)
```
(+ the 10th row "the new path drops the class the previous round repaired (M89-1)"
for P2/P3-arm; the audit cut past the second row filter, but it is present
with the same shape). No row is a restatement-only row. Every row names a
guard (`read_input()` lstat+regular+size-cap / post-child listing + diff /
decoy-sandbox / preference-with-named-fallback or filter-with-reported-refusal
/ output-testing arms / docstring-vs-code pass at frozen rev / argument-target
/ predicate-arm-with-pre-freeze-candidate) and an arm that answers it
(`N1-refuse-plain` / `isolation`+(quality 163 predecessor) / `carrier_blind` /
per-cell detail / `test_ok`+`unpack_pin`+`rea_recover` / freeze precheck /
`--expect`/`--expect-blocks` / P2+P3). **No row is false against the
criterion it cites.** Spot-verified against actual code at base: `N1`'s arm
row says `rc == 2, never rc != 0`, matching the repair's real design
(`tools/round-90/upx-break-repair.py:249` — "every refusal leaves as this
module's `Refused` (rc 2)"); `isolation` arm `box_after` matches the battery's
actual code `tools/round-90/upx-later-block-battery.py:188,338-340` ("the
listing is taken after the child exits"; "QUALITY 170: list after the child");
`carrier_blind` arm matches `:281-341` (bwrap decoy). **Block 30 is formally
sound.

## 7. Does block 30 add depth beyond the QUALITY rows it cites?

Yes. Three reasons:

1. **It is a route, not a row dump.** Rows are a *defect → guard → arm*
   decision table, not re-state­ments. The cited QUALITY rows (161, 162, 163,
   167, 168, 169, 170, 171, 157, plus 146/159 via the two closing rows) carry
   the underlying evidence but do not themselves answer "which guard must a
   *revision* carry?" — the block adds the mapping direction and the
   revision-lifecycle focus, which none of the cited rows individually provide.
2. **It adds anchors absent from the cited QUALITY rows.** E.g. the `M89-1`
   row(map first dropped class)` is a cross-round routing update grounded in
   this round's L1 candidate receipt; the `rc == 2, never rc != 0`
   typed-refusal arm and `box_after` are named instrument obligations that
   go beyond the Quality-bar prose (Over the *exact* §16 hard floor, but not
   above the "each row cites base-revision criterion" claim).
3. **No row is only in base-revision argument.** All knowledge refs
   (`...r87-upx-magic-tamper-repair.md`, `...r88-binfo-chain-geometry.md`,
   `...r89-binfo-field-value-class.md`, `...r86-record-agreement.md`) resolve
   at `fc52cc9dc` (verified via `git cat-file -e fc52cc9dc:<path>` for all
   four, green); `corpus/QUALITY.md`'s relevant rows are at fc52cc9dc too
   (no diff `git diff fc52cc9dc 5f8ea076 -- corpus/QUALITY.md` = 0 lines; Row
   171 exists at the base — verified via `git show fc52cc9dc:corpus/QUALITY.md | grep 'Row 171'`).
   Separability (QUALITY 159) holds for the landed block.

## 8. Findings for Main

Severity HIGH-ρ  (routed to a future round, not this one):
1. **F1 (round-89 instrument, non-blocking)**: `depth-blocks-v2.py`
   `resolve()` has an **order/pairing dependence** — for an adjacent `**
   block pair, the HALF that carries the first `corpus/knowledge/…` citation
   is the one that makes the pair resolvable, irres­pective of the opposite
   half's content (see §4: GREEN 6ffe9526c vs RED 8ae2df301, same text). Not
   exploitable against block 30 (correct order) but is a real instrument limit.
2. **F2 (declared-vs-receipt revision label)**: the frozen plan names base
   `fc52cc9dc` while the pre-arm receipt `.ufo/waves/round-90/pre/c2-depth-at-base.json`
   names `54c277868` (the round-89 lessons append; `SKILL.md` is
   byte-identical at both). The receipt label doesn't match the declared base
   string exactly. Both revisions score identically (§1), so the base arm is
   sound either way — a record-keeping nit only, worth routing to the L1's
   report prose so the round-90 lesson cites it explicitly rather than
   repeating the same SHA-twice ambiguity in round-91's plan.

No defect in the landed block 30 itself. Green to keep: `blocks 30 resolved
30 met=True exit=0` at `--rev 5f8ea076` over the freeze commit, on top of
§1's red base arm at both `fc52cc9dc` and `54c277868` with `--expect-blocks
30` — the axis's before/after pair stands.

## 9. Receipt file index (all absolute under /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/w1/ReviewerC2/)

- `receipts/c2-selftest.txt` — SELFTEST cases=10 failures=0, rc 0
- `receipts/c2-base-fc52cc9dc-expect30.json` — blocks 29, met=False, exit 1 (RED)
- `receipts/c2-base-fc52cc9dc-expect29.json` — blocks 29, met=True, exit 0  (GREEN)
- `receipts/c2-base-54c277868-expect30.json` — blocks 29, met=False, exit 1 (RED, receipt-revision pin)
- `receipts/c2-worktree-expect30.json` — blocks 30 met=True exit=0 (live-worktree post-setup control; the landed state)
- `receipts/c2-attack-junk-probe.json` / `receipts/c2-attack-split-31.json` — semantic/pairing probes
- `receipts/c2-capture-rev-reads-revision.json` / `receipts/c2-capture-worktree-mode.json` — poison fixture
- `receipts/c2-final-5f8ea076-expect30.json` — blocks 30, met=True, exit 0 at the L1's landing commit
- `receipts/c2-attack-receipt-scratch-clone-skill-diff-c4b1acfde.txt` — the A1 junk-prose block text as landed in the scratch clone
- `receipts/c2-attack-receipt-stub-probe-strings.txt` — dependency/stub probe strings
- `receipts/c2-attack-receipt-c2-numeric-sweep.txt` — §5's numeric sweep
- `receipts/c2-attack-receipt-worktree-poison.txt` — the §3 poison fixture log

(Short-hash commits in the scratch clone: 18b21f092 = base, c4b1acfde = junk
prose block, db0e804fd = stub-leak pair, 6ffe9526c/8ae2df301 = order GREEN/RED
pair, 5f8ea076 = L1's landed freeze commit — all reproducible via
`tools/round-89/depth-blocks-v2.py --rev <sha>` against the lane root and via
`/fast/scratch` clones now removed.)
