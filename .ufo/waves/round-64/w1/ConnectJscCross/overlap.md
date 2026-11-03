# ConnectJscCross — cross-link and sibling-overlap scan for the `.jsc` / View8 / d8 surface

Seat `ConnectJscCross`, kaidoku-shokunin round 64, wave w1. **Read-only**: this seat created no
fixture, ran no instrument, and edited no file outside its own report directory. Scratch
(`/fast/scratch/hyaku/kaidoku-r64/ConnectJscCross`) was deleted before yield; the scan is
reproducible with `scan-hits.py` in this directory (it re-derives the whole set from the lane tree).

Scan cutoff 2026-11-03 ~19:52 local, two passes. Between the passes 37 rows appeared in
`.ufo/waves/round-64/w1/` — sibling seats were writing while this seat read. The 4283 rows below are
a strict subset of the later pass; nothing in the canonical set (§1) moved.

## Verdict

**overlap-declared** — the surface is private to kaidoku's own knowledge corpus (0 hits in any
sibling lane's `corpus`, `SKILL.md` or `PROVINCE.md`), and its ownership is formally *unresolved by
declaration*: revenger's PROVINCE names "Electron/JavaScript packages", and both kaidoku and
tsukuroi record the kaidoku/revenger arbitration as open. Declared, not silent; not free to reassign.

## 0. Method

Predicate, verbatim from the seat order:

```
grep -rn -i -E 'jsc|view8|d8 |bytenode|ignition|v8 ?bytecode|loadjsc' --include='*.md' --include='*.json' --include='*.py' .
```

over `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, excluding `.git/`, `.jj/`, `.ruff_cache/` and
`.ufo/waves/round-6[0-3]` (r60–r63). Classes are the six ordered names, path-assigned mechanically so
the table can be re-derived:

| class | paths | sub-kind |
|---|---|---|
| own-lane-knowledge | `corpus/knowledge/**` / `corpus/lessons/**` / `corpus/{SOURCES,README,QUALITY}.md` | entry / lesson / registry-index |
| own-lane-skill | `SKILL.md` | skill |
| own-lane-scorecard | `SCORECARD.md` | scorecard |
| own-lane-tooling | `tools/**` | tool (the `tools/round-44{,49}/control-fixtures/**` trees are frozen control *copies* classed `tool` here, see §4) |
| staged-elsewhere | `.ufo/waves/**` artifacts and `corpus/evidence/**` copied control trees | wave-artifact / copied-control-tree |
| other | `PROVINCE.md`, `LOG.md`, `plans/**`, lane-root docs | province / lane-log / frozen-plan |

`PROVINCE.md` and `LOG.md` are lane-canonical but have no slot in the ordered enum; they are classed
`other` and reported in full rather than dropped.

Totals: **4283 rows in 652 files**. 3957 of them are `staged-elsewhere` (3928 wave artifacts, 29 copied
control trees); **326 rows in 46 files** are the lane-canonical set in §1. Per class:
own-lane-knowledge 167, own-lane-tooling 92, own-lane-scorecard 9, own-lane-skill 3, other 55.

**Predicate noise, measured (a finding for the next scan).** 612 of the 4283 rows match *only* the
`d8 ` alternative, and they are dominated by tokens that merely end in `d8` — `round8 ` and the lane's
defect labels `D1–D8` — not the d8 binary (measured split: 156 contain `round8`, 83 carry a `D8`
token, 373 are residue).
A boundary-anchored form `(?<![A-Za-z0-9_])d8(?![A-Za-z0-9_])` matches 752 rows and is the count to use
for "mentions the d8 binary". `jsc` also matches `jsc2js` and `.jsc`, both intended.

## 1. Table 1 — own-lane hits (every file:line, classed)

| # | file | class | sub-kind | hits | lines |
|---|---|---|---|---|---|
| 1 | `plans/round-35-claims.md` | other | frozen-plan | 6 | 10,11,16,19,21,32 |
| 2 | `plans/round-54-claims.md` | other | frozen-plan | 1 | 88 |
| 3 | `plans/round-57-claims.md` | other | frozen-plan | 1 | 5 |
| 4 | `plans/round-64-claims.md` | other | frozen-plan | 28 | 11,13,14,15,20,23,27,28,29,30,34,36,38,39,40,41,42,43,45,48,49,57,61,65,69,70,71,73 |
| 5 | `LOG.md` | other | lane-log | 17 | 60,61,105,116,251,1300,1595,1754,3107,3109,3548,3556,3564,3571,3678,3708,3986 |
| 6 | `PROVINCE.md` | other | province | 2 | 136,154 |
| 7 | `corpus/knowledge/2026-10-13-r2-libjq-engine.md` | own-lane-knowledge | entry | 1 | 72 |
| 8 | `corpus/knowledge/2026-10-13-r3-typora-signal.md` | own-lane-knowledge | entry | 12 | 15,17,18,33,39,41,45,69,70,73,79,83 |
| 9 | `corpus/knowledge/2026-10-13-r3-verb-coverage.md` | own-lane-knowledge | entry | 1 | 117 |
| 10 | `corpus/knowledge/2026-10-13-r4-05-signal-asar.md` | own-lane-knowledge | entry | 2 | 17,73 |
| 11 | `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` | own-lane-knowledge | entry | 61 | 1,3,7,11,13,20,30,33,34,35,36,42,45,53,73,77,78,90,93,95,98,100,102,103,104,105,106,107,108,109,114,117,127,128,141,145,146,148,151,152,154,155,158,159,162,163,168,175,181,182,183,186,187,188,191,195,204,205,206,208,209 |
| 12 | `corpus/knowledge/2026-10-13-r4-15-appimage-inner.md` | own-lane-knowledge | entry | 1 | 46 |
| 13 | `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md` | own-lane-knowledge | entry | 3 | 173,382,384 |
| 14 | `corpus/knowledge/2026-10-13-r4u-02-jadx-decode.md` | own-lane-knowledge | entry | 1 | 88 |
| 15 | `corpus/knowledge/2026-10-13-r7-01-queue-a-ops.md` | own-lane-knowledge | entry | 3 | 44,221,261 |
| 16 | `corpus/knowledge/2026-10-13-r8-02-queue-a-ops-2.md` | own-lane-knowledge | entry | 7 | 24,168,172,184,187,233,263 |
| 17 | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` | own-lane-knowledge | entry | 1 | 23 |
| 18 | `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` | own-lane-knowledge | entry | 1 | 137 |
| 19 | `corpus/knowledge/jsc-mapper-cli-contract.md` | own-lane-knowledge | entry | 12 | 1,3,5,6,8,10,11,13,15,17,19,21 |
| 20 | `corpus/knowledge/jsc-mapper-release-inventory.md` | own-lane-knowledge | entry | 7 | 1,3,5,6,8,12,14 |
| 21 | `corpus/lessons/2026-10-13-round-4.md` | own-lane-knowledge | lesson | 2 | 25,28 |
| 22 | `corpus/lessons/round-13-verifier-spotcheck.md` | own-lane-knowledge | lesson | 1 | 11 |
| 23 | `corpus/lessons/round-13.md` | own-lane-knowledge | lesson | 4 | 44,45,49,65 |
| 24 | `corpus/lessons/round-14-verifier-spotcheck.md` | own-lane-knowledge | lesson | 1 | 134 |
| 25 | `corpus/lessons/round-14.md` | own-lane-knowledge | lesson | 2 | 37,38 |
| 26 | `corpus/lessons/round-16-verifier-spotcheck.md` | own-lane-knowledge | lesson | 1 | 54 |
| 27 | `corpus/lessons/round-34-verifier-spotcheck.md` | own-lane-knowledge | lesson | 1 | 34 |
| 28 | `corpus/lessons/round-35-verifier-spotcheck.md` | own-lane-knowledge | lesson | 6 | 7,31,46,91,92,110 |
| 29 | `corpus/lessons/round-35.md` | own-lane-knowledge | lesson | 4 | 18,19,74,76 |
| 30 | `corpus/lessons/round-36.md` | own-lane-knowledge | lesson | 1 | 55 |
| 31 | `corpus/lessons/round-45-verifier-spotcheck.md` | own-lane-knowledge | lesson | 1 | 209 |
| 32 | `corpus/lessons/round-56-verifier-spotcheck.md` | own-lane-knowledge | lesson | 2 | 272,295 |
| 33 | `corpus/lessons/round-57-verifier-spotcheck.md` | own-lane-knowledge | lesson | 1 | 80 |
| 34 | `corpus/lessons/round-64.md` | own-lane-knowledge | lesson | 13 | 1,16,17,18,24,25,26,27,28,36,44,45,50 |
| 35 | `corpus/QUALITY.md` | own-lane-knowledge | registry-index | 1 | 21 |
| 36 | `corpus/README.md` | own-lane-knowledge | registry-index | 8 | 23,24,51,150,152,166,244,268 |
| 37 | `corpus/SOURCES.md` | own-lane-knowledge | registry-index | 5 | 23,24,28,194,280 |
| 38 | `SCORECARD.md` | own-lane-scorecard | scorecard | 9 | 82,1174,1829,3126,3387,3403,4303,4311,4334 |
| 39 | `SKILL.md` | own-lane-skill | skill | 3 | 56,1703,1853 |
| 40 | `tools/round-35/c1-coverage-counter.py` | own-lane-tooling | tool | 12 | 7,8,9,10,17,18,52,53,72,73,77,87 |
| 41 | `tools/round-44/control-fixtures/pos/PROVINCE.md` | own-lane-tooling | tool | 2 | 136,154 |
| 42 | `tools/round-44/control-fixtures/pos/corpus/README.md` | own-lane-tooling | tool | 8 | 23,24,51,146,148,162,236,259 |
| 43 | `tools/round-49/control-fixtures/pos/PROVINCE.md` | own-lane-tooling | tool | 2 | 136,154 |
| 44 | `tools/round-49/control-fixtures/pos/corpus/README.md` | own-lane-tooling | tool | 8 | 23,24,51,147,149,163,238,261 |
| 45 | `tools/round-49/control-fixtures/pos/corpus/SOURCES.md` | own-lane-tooling | tool | 5 | 23,24,28,170,245 |
| 46 | `tools/round-64/jsc-route-matrix.py` | own-lane-tooling | tool | 55 | 2,4,7,8,11,15,17,18,19,23,26,48,51,64,70,71,72,73,74,75,105,108,110,111,118,119,153,155,157,163,164,165,171,186,200,205,207,209,210,214,218,248,249,250,253,254,256,262,265,275,279,281,284,309,321 |

Reading notes on the rows that carry the surface:

- `PROVINCE.md:136` is the Core row (`electron --print-bytecode` under `ELECTRON_RUN_AS_NODE=1`) and
  `PROVINCE.md:154-155` the Frontier bullet (`Ignition disassembly held; a View8/jsc2js-style …
  mapper is the next frontier`). Together they are the lane's whole `.jsc` capability statement.
- `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` holds 61 of the 326 canonical rows — the densest
  `.jsc` document in the lane, and the entry every pointer chain from `PROVINCE.md:136` /
  `corpus/README.md:24,152` terminates at. Its `## Frontier verdict` (:148-168) is the lane's *priced*
  route list, not just a finding.
- `corpus/SOURCES.md:23` (S017, View8) and `:24` (S018, Check Point) are the only View8/`.jsc` source
  rows; `:194` is the source path line and `:280` the open-gap line that r64 answers.
- `SCORECARD.md:3387` is the r35 C1 "unprovable" row; `:3403` the round-37 planned item that names the
  `.jsc` lead as its "second choice"; `:82` the self-assessment line that still lists `.jsc` source
  mapping among the open domain frontier.
- `SKILL.md:1703` is the instrument-registry row for `tools/round-35/c1-coverage-counter.py`, the
  falsified r35 gate; `SKILL.md:1853` is the r64 instrument row already added in the working tree.
- The two `corpus/knowledge/jsc-mapper-*.md` entries are **untracked at the cutoff** (`git status`)
  and cite `source: S264` / `S265`, which did not exist in `corpus/SOURCES.md` at the cutoff (highest row
  then: S263; both rows landed at `:181-182` after the scan, `git diff --numstat` → 2 insertions).

## 2. Table 2 — sibling overlap

Spec command over the fleet root: `grep -rln -i -E 'jsc2js|view8|loadjsc|\.jsc' --include='*.md'
*/corpus */SKILL.md */PROVINCE.md 2>/dev/null` → **exit 0, and every returned path is
`kaidoku-shokunin/…`** (20 files: 18 under `kaidoku-shokunin/corpus`, plus its `SKILL.md` and
`PROVINCE.md`). Per-lane `*/corpus` hit counts: kaidoku 18, and **0** for audio, chousa, game-dev-2d,
game-dev-3d, kagi, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger,
souji, tabi, tameshi, tsukuroi.

| lane | file that touches the same surface | owning / adjacent text | one-line ruling |
|---|---|---|---|
| revenger | `PROVINCE.md:3-5` | "Owns: reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence" (lines 3-5, line breaks normalised, no emphasis added) | the only sibling *declaration* that reaches packaged Electron JS; it names no `.jsc`, View8, jsc2js or d8 text anywhere (0 hits), so it is a scope claim over the package, not over this route |
| revenger | `SKILL.md:508` | extractor table row: "an extractor for a packaged app … Electron S277/S297–S298" | revenger holds *packaging-extractor* sources for Electron; not bytecode/code-cache work |
| tsukuroi | `PROVINCE.md:150,152` | "It is not a tsukuroi grant of ownership. Kaidoku/Revenger arbitration remains unresolved" (:150); "“Electron/JavaScript packages” is the precise package scope, not arbitrary packages" (:152) | records OUT-009 as attributed text, explicitly refuses to read it as a grant |
| tsukuroi | `SKILL.md:2090` | "Revenger's precise declaration names Electron/JavaScript packages, not arbitrary packages; it is attributed sibling text, not an ownership grant. Kaidoku/Revenger arbitration remains unresolved." | same ruling, restated as an operating instruction |
| kaidoku | `PROVINCE.md:136,154,249` | Core row + Frontier bullet + "kaidoku/revenger arbitration is still open" | holds the surface and records the arbitration as open; does not claim exclusive ownership |
| kasegi | `SKILL.md:110,801` | "deployed bytecode ↔ repo commit", "beanstalk deployed-bytecode" | different sense of "bytecode" (EVM contract bytecode); no overlap |
| souji | `tests/vault/fixture-src-*/atlas-dir-*/Frontier-Queue.md` | quotes kaidoku's r4-16 frontier sentence ("`kaidoku (from r4-16 rescan + r5 lanes)` … `.jsc` → source mapping") as synthetic vault text | test fixture that *echoes* the lane's frontier; not a claim and not editable (§4) |
| the other 16 lanes | — | no hit under the spec predicate | — |

## 3. Table 3 — proposed cross-links (exact file + anchor; nothing here was edited)

| # | file:anchor | what to add | axis / why | state at the cutoff | cost / risk |
|---|---|---|---|---|---|
| C1 | `corpus/SOURCES.md` after `:180` (last row S263 at the cutoff) | rows **S264** (jsc2js README @ 01fc264d) and **S265** (jsc2js releases) | calibration — two admitted entries already cite these ids and the registry has no such rows, so the working tree carries dangling source ids | **landed after the cutoff**: a sibling seat added `:181` S264 and `:182` S265 (`git diff --numstat corpus/SOURCES.md` → 2 insertions, 0 deletions) | done; ids were next-free (`assimilation/reg-ids` max S263; `assimilation/collisions` S106–S149) |
| C2 | `corpus/SOURCES.md:23` (S017, View8) | append `corpus/lessons/round-64.md` (+ the matrix entry if it lands) to `used-by`; state in the scope cell that the executed tool is jsc2js's **customized fork** at `01fc264d`, not this row's `suleram/View8 @ ef39099b` | calibration/provenance — the row's object is not the bytes that ran | `used-by = corpus/lessons/round-13.md, corpus/lessons/round-14.md`; fork text at `~/.local/share/kaidoku-jsc/jsc2js-src/README.md:122` | low: `used-by` is an append-only list (S003 carries 12 entries) |
| C3 | `corpus/knowledge/jsc-mapper-cli-contract.md:6`, `corpus/knowledge/jsc-mapper-release-inventory.md:12`, `corpus/lessons/round-64.md:27` | resolve the pointer to `2026-11-03-r64-jsc-route-outcome-matrix.md` — land that entry from the matrix receipt, or delete the three references | calibration — the landing's own "Entries admitted" list names a file that does not exist | **file absent**: `ls corpus/knowledge \| grep 2026-11-0` → empty | low if done after the receipt exists; **blocking** if the round closes as written |
| C4 | `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` after `:219` | append-only `## Errata (round 64)` (the bounded move in the report) | depth — the lane's priced route list is stale; see the report §Move | `## Errata (round 5 audit)` at `:212` is the existing append point; sha256 `eb18239d…c5e4` | low: additions only, no tool reads the entry's bytes |
| C5 | `PROVINCE.md:154-155` | receipt-bound measured clause: instrument path, claim id, `N/18` from the receipt, and the label class (outcome triage; output is pseudo-Ignition, `node --check` fails) | depth — the frontier statement is the capability map; without the clause a verified matrix changes nothing visible | bullet unchanged since r4u (`git log -L 154,155` → one commit, `999ce123`) | medium: **same sentence echoed at `corpus/README.md:268`** — move both or split the echo |
| C6 | `corpus/README.md:268` | the frontier echo (same clause as C5) | calibration — a second copy of the frontier state | identical sentence to `PROVINCE.md:154-155` | low |
| C7 | `PROVINCE.md:136` and `SKILL.md:56` | add the d8 route to the Core `.jsc` row as a *second port* with its measured outcome class, never as a held capability before the receipt | depth — a reader of the Core table currently sees only the electron route | both rows name `electron --print-bytecode` only | medium: overclaim risk; phrase after the receipt |
| C8 | `SCORECARD.md:3403` | dispose of the round-37 "planned" item that names the `.jsc` lead as its "second choice": deferred to r64 under R64-C1 (or dropped) | calibration — rounds 38–63 record no disposition for a planned row | `planned (round 37)` row, "second choice: the `.jsc` frontier lead recorded in the round-36 lesson" | low |
| C9 | `SCORECARD.md:81-84` | the self-assessment line lists `.jsc` source mapping among the open domain frontier; reconcile with C5's measured statement | calibration — the lane's own summary contradicts a hold | "`.jsc` source mapping and runtime-capture limits remain as documented" | low |
| C10 | `SKILL.md:1703` | mark the r35 counter row superseded by `tools/round-64/jsc-route-matrix.py`; its description scores entries "cites S125/S129", and S125 is now AVM FRITZ!Box (`corpus/SOURCES.md:131`), S129 binwalk v3 (`:135`) | calibration — a live instrument-registry row describes a falsified gate in terms of ids that no longer mean what it says | row present, no supersede note | low |
| C11 | `corpus/README.md:23-24`, `:150-152` | index rows for the two `jsc-mapper-*` entries (and the matrix entry if it lands); the Electron/ASAR/JS row currently ends at r4-07 | coverage — the corpus index is the map entrants read | rows end at `2026-10-13-r4-07-jsc-bytecode` | low |
| C12 | `SCORECARD.md` after `:4986`, `LOG.md:3987` | the round-64 section and log entry (landing-owned; listed for completeness) | calibration | r63 section is the last (`SCORECARD.md:4876`); LOG's r64 scope line is `:3986` | landing owns it |

## 4. Do not touch — frozen copies of the same sentences

The frontier sentence and the Core row also live, byte-frozen, in:

- `tools/round-44/control-fixtures/pos/PROVINCE.md:136,154` and `…/pos/corpus/README.md:23,24,51,146,148,162,236,259`
- `tools/round-49/control-fixtures/pos/PROVINCE.md:136,154`, `…/pos/corpus/README.md:23,24,51,147,149,163,238,261`, `…/pos/corpus/SOURCES.md:23,24,28,170,245`
- `souji-shokunin/tests/vault/fixture-src-*/atlas-dir-*/Frontier-Queue.md` and the same paths under
  `souji-shokunin/census/round-26/…` (sibling lane, read-only)

These are copies pinned at their own round's rev and read by their own gates and tests
(`tools/round-44/c1-controls.py:897-920` reads `PROVINCE.md` at the *freeze* rev, not the worktree).
Editing them would move a control's expected bytes; a C5/C6 edit must leave all of them alone.

## 5. Second-order effects observed (state, not proposals)

- **The r64 measurement falsifies a *price*, not just a finding.** `2026-10-13-r4-07-jsc-bytecode.md:162-164`
  calls the jsc2js patched-d8 route "heavy fallback … — days of work, obviated by option 1's
  run-as-node disasm"; `:205-208` repeats that the standing cheapest-complete path is the run-as-node
  disasm "feeding a View8/jsc2js-style text mapper". A published `14.8.178.14` d8 exists (this round
  downloaded it; sha256 `bc70d3c0…` in `pins-pre.txt`), so the cost is a download. And the two routes
  split on the real artifact: the d8 path is predicted to die 134 on typora in all six typora cells,
  while `:119-132` records the run-as-node route dumping 530 KB from the same cache. No later document
  corrects either sentence.
- **The View8 that ran is not the View8 in `SOURCES.md`.** `corpus/SOURCES.md:23` pins
  `suleram/View8 @ ef39099b`; the instrument runs `jsc2js-src/View8` (`01fc264d`, README:122 "based on
  a customized fork"). `view8.py` sha256 `b3123e4a…` is the only View8 file in `PINS`
  (`tools/round-64/jsc-route-matrix.py:56-65`), while the behaviour lives in the unpinned imports:
  `Translate/translate.py` `0e075893…`, `Parser/sfi_file_parser.py` `7ce34163…`,
  `Simplify/simplify.py` `9603ff0f…`. The fork's own README lists V8 9.4/10.2/11.3 only, so `view8-ok`
  must never be read as version support (S017's scope already says it "does not establish
  compatibility with V8 14.8" — consistent, but that disclaimer is not attached to the r64 run).
- **The persistent toolchain is not write-free.** `View8/{Parser,Simplify,Translate}/__pycache__`
  holds `cpython-314` and `cpython-315` `.pyc` files (all mtime 2026-11-03 19:36); the frozen
  instrument passes no `PYTHONDONTWRITEBYTECODE` and runs `view8.py` with `cwd=view8_dir`. A run can
  therefore write into `~/.local/share/kaidoku-jsc/jsc2js-src/View8`, and no pin covers it. This is the
  same object as the sibling seat `ReviewerC2-4`'s pycache check; the connector records only the
  cross-link — no source row or pin covers the View8 subtree.
- **`corpus/lessons/round-64.md:36,44-50` are drafts in flight** (`git status` → untracked), as are
  both `jsc-mapper-*` entries; `SKILL.md` already carries the r64 instrument row as a modification
  (`git diff SKILL.md` → 1 insertion at `:1853`).

## 6. Verdict

overlap-declared
