# ConnectJscCross — r64 w1: `.jsc` / View8 / d8 cross-links, sibling overlap, one bounded move

Seat `ConnectJscCross`, kaidoku-shokunin round 64, wave w1. Read-only: no fixture, no instrument run,
no edit outside this seat's report directory. Scan cutoff 2026-11-03 ~19:52 local, two passes.

Artifacts in `.ufo/waves/round-64/w1/ConnectJscCross/`:
`overlap.md` (the three required tables + verdict), `scan-hits.py` (re-derives the scan from the lane
tree), `hits-canonical.tsv` (the 326 lane-canonical rows as `file:line`, class, sub-kind, tokens).

Verdict: **overlap-declared**. The surface is private to kaidoku's knowledge corpus (0 hits in any
sibling lane's `corpus`, `SKILL.md`, `PROVINCE.md`), and its ownership is formally unresolved *by
declaration* — revenger's `PROVINCE.md:3-5` names "Electron/JavaScript packages"; kaidoku's
`PROVINCE.md:249` and tsukuroi's `PROVINCE.md:150,152` both record the kaidoku/revenger arbitration as
open.

## Findings (evidence pointers; nothing here was changed)

**F1 — zero sibling knowledge overlap, and it is declared, not silent.**
`grep -rln -i -E 'jsc2js|view8|loadjsc|\.jsc' --include='*.md' */corpus */SKILL.md */PROVINCE.md`
from `/home/vgpnk/Projects/shokunin` → exit 0, every path `kaidoku-shokunin/…` (20 files). Per-lane
`*/corpus` counts: kaidoku 18, all 20 other lanes 0. The only sibling text that reaches the object is
revenger `PROVINCE.md:3-5` ("Electron/JavaScript packages") plus its extractor-source row
`SKILL.md:508` (Electron S277/S297–S298), and tsukuroi `PROVINCE.md:150,152` / `SKILL.md:2090`
refusing to read OUT-009 as an ownership grant. kasegi's "deployed bytecode" (`SKILL.md:110,801`) is
EVM contract bytecode — a different sense.

**F2 — the landing admits an entry that does not exist.** Three references to
`corpus/knowledge/2026-11-03-r64-jsc-route-outcome-matrix.md`:
`corpus/knowledge/jsc-mapper-cli-contract.md:6` (`ground:`), `corpus/knowledge/jsc-mapper-release-inventory.md:12`,
`corpus/lessons/round-64.md:27` ("Entries admitted: … and the lane's own …"). The file is absent
(`ls corpus/knowledge | grep 2026-11-0` → empty; neither file is in `git status`). Both entries are
untracked drafts; the lesson is an untracked draft. Blocking if the round closes as written.

**F3 — the View8 that ran is not the View8 in `SOURCES.md`.**
`corpus/SOURCES.md:23` pins `suleram/View8 @ ef39099b` (tier A, status `mined`,
`used-by = corpus/lessons/round-13.md, corpus/lessons/round-14.md`). The instrument runs the fork:
`~/.local/share/kaidoku-jsc/jsc2js-src/View8` at jsc2js commit `01fc264d` (README line 122: "based on
a customized fork of suleram/View8"). `PINS` (`tools/round-64/jsc-route-matrix.py:56-65`) covers only
`view8.py` (`b3123e4a…`); the behaviour lives in unpinned imports — `Translate/translate.py`
`0e07589374ad38541c2edaf9867e7dc8ad4636eb6dff3532ea62503a01ff9f78`,
`Parser/sfi_file_parser.py` `7ce34163cace6e818f405d0177400c0d24fab36e35644c893e8437dccae444a1`,
`Simplify/simplify.py` `9603ff0fc837720cbb39cc3b27ba1a7e707dba76d3f05203bfb623f746402cf7`. The fork's
own README lists V8 9.4/10.2/11.3 only, so `view8-ok` (exit 0 + non-empty, `:105-111`) is never
version support; S017's scope already says it "does not establish compatibility with V8 14.8", but
that disclaimer is not attached to the r64 run anywhere.

**F4 — the lane's *priced* route list is stale, and the round's own measurement falsifies it.**
`corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md:162-164` calls the jsc2js patched-d8 route "heavy
fallback … — days of work, obviated by option 1's run-as-node disasm"; `:205-208` repeats the
run-as-node disasm as "the standing cheapest-complete path". Two measured corrections: a published
`14.8.178.14` d8 exists and was downloaded (`bc70d3c0…`, `.ufo/waves/round-64/w1/ExecMatrixRun/pins-pre.txt`)
so the cost is a download, not days; and the routes split on the real artifact — the frozen matrix
predicts 134 in all six typora cells while `:119-132` records run-as-node dumping 530 KB from the same
cache. `grep -rn 'days of work|obviated'` over `corpus/ PROVINCE.md SCORECARD.md` → no later
correction exists. No tool reads this entry's bytes (`grep -rln 'r4-07' tools/` → only the frozen
control copies under `tools/round-44|49`); its sha256 is `eb18239de783748aa4aabf0ceb89a92b809cc3da0fd3bcb099f3e596f8a0c5e4`
(worktree = `a35e5141`, byte-identical).

**F5 — a live instrument-registry row describes a falsified gate with ids that changed meaning.**
`SKILL.md:1703` (r35 counter) scores entries that "cite S125/S129". `corpus/SOURCES.md:131` is S125 =
AVM FRITZ!Box 6490 download directory; `:135` is S129 = binwalk v3 README. The r64 renumbering (S264,
S265) is exactly this collision (`assimilation/staged-ids`, `reg-ids`, `collisions`: staged S106–S149
all collide, registry max S263).

**F6 — the frontier sentence is duplicated, including in frozen fixtures.** Identical text at
`PROVINCE.md:154-155` and `corpus/README.md:268`, and byte-frozen copies at
`tools/round-44/control-fixtures/pos/PROVINCE.md:136,154`, `tools/round-49/control-fixtures/pos/PROVINCE.md:136,154`,
both `…/corpus/README.md`, and souji's `tests/vault/fixture-src-*/atlas-dir-*/Frontier-Queue.md`.
`tools/round-44/c1-controls.py:897-920` reads `PROVINCE.md` at the *freeze* rev, so editing the live
file does not break it — but editing the fixture copies would move a control's expected bytes. The
precedent for a same-line annotation exists: `PROVINCE.md:157` (sasquatch) carries bracketed round-38/39
notes, and `SCORECARD.md:438` records "two PROVINCE same-physical-line additions".

**F7 — a planned item was never dispositioned.** `SCORECARD.md:3403` (round 37) lists "second choice:
the `.jsc` frontier lead recorded in the round-36 lesson"; rounds 38–63 record no disposition of it.
`SCORECARD.md:81-84` still lists `.jsc` source mapping among the open domain frontier.

**F8 — dangling source ids in the working tree (resolved after the cutoff).** Both `jsc-mapper-*`
entries cite `source: S264` / `S265`; at the cutoff `corpus/SOURCES.md` had no such rows (max S263,
line 180). A sibling seat added them after the scan — `:181` S264, `:182` S265
(`git diff --numstat corpus/SOURCES.md` → 2 insertions, 0 deletions). Ids verified free: registry ids
`S001–S149, S243–S263`; staged ids that collide `S106–S149`; so `S264`/`S265` were next-free and the
renumber is by document, as the plan states. S017's `used-by` (`:23`) is still r13/r14 only.

**F9 — the persistent toolchain is not write-free.** `View8/{Parser,Simplify,Translate}/__pycache__`
holds `cpython-314` and `cpython-315` `.pyc` (all mtime 2026-11-03 19:36); the frozen instrument passes
no `PYTHONDONTWRITEBYTECODE` and runs `python view8.py` with `cwd=view8_dir` (`:205-207`), so a run can
write into `~/.local/share/kaidoku-jsc/jsc2js-src/View8`. No pin covers it. Same object as
`ReviewerC2-4`'s pycache check — the connector records only that no source row or pin covers the View8
subtree.

**F10 — the seat's own predicate is noisy in a predictable way.** 612 of 4283 rows match only the
`d8 ` alternative, dominated by `round8 ` and defect labels `D1–D8` (156 `round8`, 83 `D8`, 373
residue). Boundary-anchored `(?<![A-Za-z0-9_])d8(?![A-Za-z0-9_])` → 752 rows; use that for "the d8
binary".

## The move (one, bounded)

**Append `## Errata (round 64)` to `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` (after line 219),
carrying three measured sentences and one receipt pointer, in the lane's existing append-only errata
form (`## Errata (round 5 audit)` at `:212`).**

Contents, fixed in advance:

1. the "days of work / obviated" price at `:162-164` is superseded — the `14.8.178.14` patched-d8
   release exists, is sha-pinned (`bc70d3c0…`) and was run;
2. the two routes are complementary, not substitutes — the patched d8 aborts (134) on Typora's cache
   while the run-as-node route at `:119-132` dumps it; each is the other's control;
3. the text mapper's output is not JavaScript — `node --check` exit 1 on the 213-byte View8 output
   (`SyntaxError: Unexpected token ':'`, `.ufo/waves/round-64/l1/prefreeze-probe/view8-probe.log`,
   `probe-view8.js`), so `:152`'s "approximate JS" is the tool's README description, not the measured
   text;
4. `receipt:` the `ExecMatrixRun` receipt path plus `N/18 matched`, **filled from the receipt**.

**Why this and not the frontier bullet.** Every pointer chain for this surface terminates here:
`PROVINCE.md:136` (Core probe cell) → `corpus/README.md:24,152` → r4-07; the Frontier bullet's
"Ignition disassembly held" is this entry's finding. The bullet (`:154-155`) states a status; r4-07
`:148-168` states the *price* of each route, which is what a future round acts on. Landing the
measurement only in `PROVINCE.md`/`SCORECARD.md` leaves the lane's own entry telling the next round
that the capability it just acquired is not worth acquiring. That is the non-obvious cost: the round
buys a capability and the map keeps pricing it at "days of work, obviated".

**Affected axes.** Primary: **depth** (capability acquisition) — the acquired capability becomes
findable and correctly priced at the document the pointer chain resolves to, without changing the
claim, the instrument, or any count. Secondary: **calibration** — a 2026-10-13 price is corrected by
document, with the correction's evidence named. Not touched: coverage (no entry, no registry row, no
new map node), quality, discernment, expansion. No axis is harmed; no score moves.

**Cost.** One append-only block, ~6 lines. No instrument edit, no claims edit, no freeze re-pin, no
counter re-run.

## Risks

- **R1 — unverified matrix.** The errata must be written *after* the receipt and *from* it: if the
  matrix mismatches, sentence 4 reads the failing cell count and the errata records a measured
  failure, never a hold. It must never contain the words "capability held".
- **R2 — overclaim on the Typora outcome.** 134 is an artifact-level observation, not a defect
  diagnosis of Typora; `plans/round-64-claims.md:57` disclaims it and `PROVINCE.md:102-104` refuses
  safety/trust verdicts. Copy the "outcome, not diagnosis" clause into the errata.
- **R3 — line drift.** Append at the end only; cite the entry by anchor text, never by line number, in
  any later receipt.
- **R4 — re-ranking temptation.** Three facts plus a receipt pointer; no new ranked list, so the
  errata cannot become an unpriced claim of its own.
- **R5 — echo cascade.** Do not propagate the errata to `tools/round-44|49/control-fixtures/**` or
  souji's vault (F6); those copies are frozen at their own rev.

## Verification (for the main agent; not run here)

```
# 1. additions only, no deletion
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --numstat -- corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md
# 2. the pre-edit bytes are intact at the freeze
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show a35e5141:corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md | sha256sum
#    expected eb18239de783748aa4aabf0ceb89a92b809cc3da0fd3bcb099f3e596f8a0c5e4
# 3. the errata's N/18 equals the receipt's own numbers (read the receipt, never the claim)
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("matched"), d.get("total"), d.get("exit"))' <receipt.json>
# 4. no live gate depends on the entry's bytes
grep -rln 'r4-07' tools/
# 5. the frontier echo was not touched in frozen copies
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain -- tools/
```

## Not done

No file outside `.ufo/waves/round-64/w1/ConnectJscCross/` and this report was written. No instrument
run, no pin check, no claim or scorecard edit, no git mutation. Scratch
`/fast/scratch/hyaku/kaidoku-r64/ConnectJscCross` deleted before yield.
