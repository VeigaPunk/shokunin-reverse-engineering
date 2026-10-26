# R38W2C2Rederive — independent rederivation of R38-C2 at `0fc6113`

**Verdict: CONFIRMED — R38-C2's `mismatches 0 / guards_ok` survives a rederivation stricter than the frozen counter; DEFECTS FOUND in the landing record (D-1 dangling receipt, D-2 gate red at the measured revision), not in the C2 predicate.**

R38-C2's number is true and reproducible; the two claims *around* it in the landed bytes are false:
(D-1) the C2 receipt it cites does not exist at any revision and the real receipt was never committed;
(D-2) the round's own freeze-drift gate exits 1 at the measured revision, while the record pairs a drift
receipt at `077e212b` with a "clean" receipt taken *before* the drift happened.

Attacked: `R38-C2 met` (author verdict, SCORECARD.md:3406). Not trusted: `tools/round-38/c2-counter.py`,
the wave-1 reports, and the L1's receipts. Everything below is re-derived from git objects at
`REV=0fc6113376a156fddc3ec385386d71c3a4a9f690`, `BASE=77091b492cc53f8743bd0701b1e7d5e66123dd84`,
`FREEZE=e059ca9391642d5b71b6662cabcbdce0d9308719`, by scripts written for this seat
(`.ufo/waves/round-38/w2/artifacts/R38W2C2Rederive/`, listed in §9). Read-only git only; no VCS mutation.

---

## 1. Item 1 — every backticked lane pointer in the four scored surfaces (independent parse)

My unit enumeration (`indep.py`) does not import the counter. It differs from the frozen counter on
**one deliberate point**: PROVINCE `## Frontier` is a bullet list, and the predicate says "`## Core` and
`## Frontier` **rows**", so a bullet is a row. The frozen counter only collects table rows there
(`c2-counter.py:83-86`, `l.lstrip().startswith('|')`) and therefore scores **zero Frontier units**.

| | frozen counter | this seat |
|---|---|---|
| units at REV | 35 (3 Owned + 9 Caps + 19 Core + **0 Frontier** + 4 SHONEN) | **40** (same, plus **5 Frontier bullets**) |
| pointers at BASE | 48 | **53** |
| pointers at REV | 52 | **57** |
| unresolved at BASE | 1 — `prov_core:REA MCP server :: evidence/doctor/` | **1 — same unit, same token** |
| unresolved at REV | 0 | **0** |

The five extra pointers are exactly the Frontier knowledge links
(`…r25-evm-selector-name-resolution.md`, `…r28-evm-heldout-selector-naming.md`,
`…r28-openchain-filtered-flag.md`, `…r29-evm-fresh-selector-naming.md`,
`…r29-openchain-filtered-unseen.md`), all resolving. **Extending scope did not produce a mismatch.**

Also checked, since the frozen counter keys units by first cell (`u['owned:'+first_cell]`, so a shadow
row would silently overwrite):
- duplicate unit keys at BASE **and** REV: `Owned axes` 0, `Capabilities` 0, `Core` 0, `Frontier` 0,
  SHONEN boxes 0. No shadow row exists to overwrite.
- backticked tokens in the four surfaces that the counter's `PTR` regex silently drops but which look like
  lane paths (comma ranges like `X.md:1-2,4-5`, trailing anchors): **0** (`skipped.py`).

## 2. Item 2 — the repaired `evidence/doctor/` pointer names the same document

Three independent confirmations that `.ufo/waves/round-19/evidence/doctor/` is what the base pointer meant:

1. **The base path never existed as a repo-root document.** Top-level `evidence/` at BASE contains exactly
   `evidence/round-1-2026-10-15/{baseline,rea-bundle,result,rubric}` — four files, no `doctor/`.
2. **Round-19 history holds it at exactly that path.** `.ufo/waves/round-19/evidence/doctor/doctor-6.5.0.txt`
   and `doctor-6.7.0.txt` are present at BASE and in **852 commits** of history, and are the only committed
   `…/doctor/` **directory tree** in the repo (the other doctor artifacts are single files elsewhere).
3. **The row and the freeze both say so.** The same table cell's sibling pointer is
   `.ufo/waves/round-19/evidence/province-pins-integrated.json`, and the first-freeze claims doc already
   states the intended document: "the intended document is the committed
   `.ufo/waves/round-19/evidence/doctor/` tree (doctor-6.5.0.txt, doctor-6.7.0.txt)"
   (`e059ca93:plans/round-38-claims.md`, C2 "Before" bullet).

Content also matches the row's probe claim: `doctor-6.5.0.txt` lines 91-95 (`registration:devin`) and
111-115 (`registration:omp`) say the registration "requests rea-agents@6.7.0, while the current REA CLI
package is 6.5.0"; `doctor-6.7.0.txt` contains no `registration:devin`/`registration:omp` entry at all.
So the repair is a genuine same-document repair, **not** the "any same-basename document" decoy QUALITY 77
forbids — even though the counter's own test (`p2.endswith('/'+path)`, `c2-counter.py:229-230`) would accept
any such suffix.

## 3. Item 3 — the stated counts and ranges equal fresh observations

| stated | where | re-derived (`counts.py`, `depth.py`) |
|---|---|---|
| coverage 126/126 | SCORECARD.md:23 | knowledge `.md` = **126**, distinct basenames 126 (no collision); README `## Coverage map` (single heading, line 11) maps **126 distinct** stems; stems-without-file **0**; files-not-mapped **0** |
| depth 17/17 | SCORECARD.md:24 | `## Queue-drain craft` heading line **81**, last non-blank **314**, rule blocks **17**, resolvable **17/17** |
| calibration 9/9 | SCORECARD.md:25 | `evidence/round-1-2026-10-15/result.json`: 9 obligations, **9 aligned**, `measured_revision c265db9b…` (matches the row) |
| SHONEN box1 17/17 | SHONEN.md:5-6 | 17/17; the box's `SKILL.md:81-314` anchor is also true **at its own named commit** `3e99fbd6…` (81-314, 17 blocks) |
| craft range | SCORECARD.md:24, SHONEN.md:6 | 81-314 ✔ |
| Adjacent range 97-125 | SHONEN.md:11-12 | 97-125 ✔, and the box's sub-claims hold at those lines: safety refusal 116-118, tooling bullet 119-125, installer 110-115 |
| `PROVINCE.md:8-14` pins 6.7.0 / 207-153 | SHONEN.md:12 | ✔ (lines 8-12) |
| `PROVINCE.md:24` shared skill v42 | SHONEN.md:12 | ✔ |

Because the counter's `stated()` uses `re.search` (**first** occurrence) where the lane's own QUALITY 77
(QUALITY.md:85) demands `findall`, the *historical* counts inside the same rows are unscored. I scored them
by hand; **all are true**: 122/122 at `cab59f22`; 116/116 and 17/17 at `c369242f`; 109/109 and 17/17 at
`ebe2cb4a`; 78/78 and 9/9 at `3395b6d`; 107/107 at `7ef837a4`; 108/108 at `08c7a729`; 70/72 mapped at
baseline `a79945c4`.

Counter rerun (frozen bytes, my invocation): `exit 0`, `mismatches 0`, `guards_ok true`, 7 assertions,
`pointers 52`, selftest `14 cases, 1 green, 13 red, 0 failures`.

## 4. Item 4 — shadow rows, second statements, decoys

- **No duplicate unit keys**, no second `## Owned axes` / `## Capabilities` / `## Core` / `## Frontier`
  heading at REV; SHONEN has 4 boxes, none duplicated.
- **4 stems appear in two README coverage-map rows each** (`arc2-r7-pe-wall`,
  `arc3-r7-evm-evidence-id-domain`, `arc3-r10-rust-evidence-id-domain`, `r36-sasquatch-squashfs-recursion`).
  Checked the pairs: each is a cross-listing under a different theme row with a different, non-conflicting
  description. Not a contradictory duplicate; every map stem still resolves to one real file.
- The two new entries (`…r38-sasquatch-be-squashfs-recursion.md`, `…unblob-format-matrix.md`) resolve
  cleanly (1 lane pointer each; 126/126 mapping confirmed).
- **One decoy found: see D-1.**

## 5. Defects (FALSIFIED signals in the landed bytes)

### D-1 — the C2 receipt named in the landing does not exist; the real receipt is untracked

- `SCORECARD.md:3406` (`## Round 38`, R38-C2 row): "0 mismatches, `guards_ok`, exit 0
  (`.ufo/waves/round-38/l1/scores/c2-final.json`, revision in its `revision` field)".
- `corpus/lessons/round-38.md:11`: "measured at the landing commit
  (`.ufo/waves/round-38/l1/scores/c2-final.json`)".
- `git cat-file -e REV:.ufo/waves/round-38/l1/scores/c2-final.json` → **absent**; absent at BASE, absent at
  HEAD, and `git log --all --name-only` shows the name never existed under `round-38/`.
  The committed `.ufo/waves/round-38/l1/scores/` tree at REV holds **only** `c1-v1-at-3b960fe5.json` and
  `c1-v3-at-3b960fe5-NOT-THE-RULE.json`.
- The receipt that exists is **untracked**: `.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json`
  (`git status --porcelain` → `??`, mtime 03:50, i.e. written *after* the 03:49:59 commit). Its content is
  the green measurement (`mismatches 0`, `guards_ok true`, `revision 0fc61133…`, `pointers 52`), and I
  reproduced that result myself — so the *number* is true and the *citation* is false.
- This is the exact class the same round routed as a defect (claims doc: "R37-CL1 (commit every receipt the
  report cites; cite only what is committed)"). The landing commits no C2 receipt and cites one that never
  existed.
- Blind spot: the frozen predicate scopes pointers to the four surfaces only, so a dangling pointer in the
  `## Round 38` row and the lesson is invisible to `c2-counter.py` (whole-document scan of the landed docs
  finds 3 distinct new unresolved tokens: this one, plus `evidence/doctor/` in the round row and LOG and
  `considerthese/` in the lesson — the latter two are *quotations* of an absent path, not pointers, and I
  excluded them).

### D-2 — the round's own QUALITY 79 gate is not clean at the measured revision, and the record hides it behind a pre-drift receipt

- `python3 -I -B tools/round-38/freeze-drift.py --root <lane> --freeze e059ca93… --rev 0fc6113…` →
  **exit 1**, drift = `79f69347` (`plans/round-38-claims.md`, `tools/round-38/c1-counter.py`) and
  `f1010f67` (`tools/round-38/c1-counter.py`). Same at `3b960fe5` (C1's measured revision): exit 1.
- The record cites only "exit 1 at `077e212b`" (SCORECARD.md:3401) and a *clean* receipt
  `.ufo/waves/round-38/l1/freeze-drift-cb4326b2.json` (`drift: []`, exit 0). But `cb4326b2` is dated
  03:19:01 and is an **ancestor** of the drifting commits (`cb4326b2` → `077e212b` → `3b960fe5` →
  `0fc6113`). A clean verdict taken before the drift happened cannot certify the landing; the gate at the
  measured revision is red.
- QUALITY 79 (QUALITY.md:87, added by this round) requires zero commits over the claim's kill-rule paths
  from first freeze to **measured revision** before any score is cited. That precondition is unmet at REV.
- **Scope of the defect — C2's rule is intact.** The drift does not touch C2's rule bytes:
  C2 predicate lines are byte-identical at freeze and REV (`sha256 3c4b236d…`), `tools/round-38/c2-counter.py`
  is byte-identical (`sha256 7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7` at both).
  The claims-doc drift is C1's rewrite plus one appended 3-line C2 "Wave-1 disclosure" paragraph
  (`c2-claims-freeze.md` vs `c2-claims-rev.md` — the only diff in the C2 section). So the claim is scored
  with first-freeze rule bytes; the *reported gate status* is what is false.

## 6. Blind spots that survive but hide nothing at this revision

- **B-1 Frontier units are not scored at all** by the frozen counter (§1). Harmless here; it means the
  Frontier half of the predicate was scored vacuously, and a future unresolved Frontier bullet would pass.
- **B-2 repair identity is a path-suffix test** (`endswith('/evidence/doctor/')`), which QUALITY 77
  explicitly forbids ("checks a repaired pointer against the intended document named in the freeze — not
  any same-basename file"). The actual repair happens to be the right document (§2), and the freeze itself
  names it — but the counter, not the freeze, is doing the accepting.
- **B-3 first-match counts** (`re.search`) instead of `findall` (QUALITY 77). All historical counts happen
  to be correct (§3).
- Inherited and *not* from this landing: 11 unresolved lane pointers in SCORECARD, 11 in LOG, 1 in README
  (e.g. `tools/carrier-guard.py`, `evidence/strict-baseline/`, `.ufo/waves/kaidoku-r1/`) — all dated
  historical references, none in a C2 unit, all present at BASE.

## 7. Impacted axes

- **calibration** — the C2 verdict ("met") stands on measurement, but the landing's calibration record
  claims a receipt it does not hold and reports a gate as closed that is open at the measured revision
  (D-1, D-2). Calibration is precisely the axis that should not be self-certified.
- **coverage** — unaffected in number: 126/126, 17/17 verified independently, and both round-38 entries are
  genuinely mapped and resolvable. The `## Round 38` section's *evidence pointers* are the damaged part,
  not its counts.
- **QUALITY** — the landing violates 77 (suffix repair test, first-match counts) and 79 (gate not run to the
  measured revision) in its own artifacts while citing both as satisfied.

## 8. Smallest safe correction (one commit, no rule change)

1. Commit the green receipt as `.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json` (or move it to the cited
   `c2-final.json` name) **and** make `SCORECARD.md:3406` + `corpus/lessons/round-38.md:11` cite the path that
   exists. Do not change the counter, the predicate, or any count.
2. Commit a `freeze-drift.py` receipt at the measured revision and state it plainly: `exit 1`, commits
   `79f69347` + `f1010f67`, touching the claims doc and the **C1** counter only; C2's predicate and counter
   bytes are identical to the freeze. Either delete the "exit 0 at `cb4326b2`" pairing or label it as a
   pre-drift revision (`cb4326b2` 03:19:01 is an ancestor of both drift commits).
3. Optional, successor counter only (not needed for C2): score Frontier bullets, use `findall`, and resolve
   the repaired pointer against the document named in the freeze.

## 9. Reproduction

Artifacts: `.ufo/waves/round-38/w2/artifacts/R38W2C2Rederive/` — `indep.py` (unit + pointer rederivation,
returns 40 units / 57 REV pointers / 0 unresolved), `skipped.py` (PTR-skipped lane tokens: 0), `dups.py`
(duplicate keys + craft range), `counts.py` (coverage), `depth.py` (rule blocks), `hist.py` (historical
counts), `fullscan.py` (whole-document new-vs-inherited unresolved), `c2-rerun.json` (frozen counter at REV),
`fd-rev.json` / `fd-3b96.json` (freeze-drift at both measured revisions), `c2-claims-freeze.md` /
`c2-claims-rev.md` (the C2-section diff), `c2-at-0fc61133.UNTRACKED-snapshot.json` (the receipt that exists
but is uncommitted).

Commands (cwd = lane root, `TMPDIR` in seat scratch, read-only git):

```
python3 -I -B tools/round-38/c2-counter.py --root $PWD --rev 0fc61133… --base 77091b49…   # exit 0, mismatches 0
python3 -I -B tools/round-38/c2-counter.py --selftest                                     # 14 cases, 13 red ok
python3 -I -B tools/round-38/freeze-drift.py --root $PWD --freeze e059ca93… --rev 0fc61133…  # exit 1
python3 -I -B tools/round-38/freeze-drift.py --root $PWD --freeze e059ca93… --rev cb4326b2…  # exit 0 (pre-drift)
python3 -I -B $ART/indep.py       # BASE 53 ptr/1 unresolved · REV 57 ptr/0 unresolved · 40 units
git show e059ca93:tools/round-38/c2-counter.py | sha256sum   # 7f137b66… == REV
git show e059ca93:plans/round-38-claims.md | sed -n '/^## R38-C2/,/^## Frontier step/p' > f; \
git show 0fc61133:plans/round-38-claims.md | sed -n '/^## R38-C2/,/^## Frontier step/p' > r; diff -u f r
git ls-tree -r --name-only 0fc61133 -- .ufo/waves/round-38/l1/scores   # only the two c1 receipts
git status --porcelain -- .ufo/waves/round-38                          # ?? …/c2-at-0fc61133.json
```

## 10. Bound compliance

Wrote only this report and the artifacts directory named above. No VCS mutation (read-only `git show/log/
ls-tree/ls-files/cat-file/merge-base/status/diff/rev-parse/grep`); no `git add/commit/checkout`. No writes
to `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`, no sibling lane or fleet repo,
no campaign tool in `shokuknow`. No REA invocation was needed. No tool installed or updated (nothing was
missing: `python3`, `git`, `diff`, `sha256sum` suffice). Scratch `/fast/scratch/hyaku/kaidoku-r38/
R38W2C2Rederive/` removed at exit; every cited artifact was copied into the artifacts directory. No
subagents, no background jobs, no `agent://all`.
