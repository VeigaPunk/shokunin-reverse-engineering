# R42C2TableDraft — SKILL rule block 21 (table v4), its knowledge entry, block 20's supersession sentence, and a pre-freeze check of the draft

**DONE (with three findings the L1 must adjudicate before the freeze: the failing-handler seam, `squashfs_v4_broadcom`, and the claims' R41-CL4 wording).** Block 21, the one-sentence supersession for block
20 and `corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md` are drafted; the block parses in situ (13 rules,
exit 0), its reference reader passes 11/11 selftests, and it agrees with an independent implementation of the
draft's steps 1-13 on 45 424 of 46 656 grid points with **0** unexplained disagreements (the other 1 232 are the
one seam a table without a failing-handler column cannot close). On the 52 committed round-41 held-out
envelopes it is 52/52 with the precedence and 52/52 with the frozen v3 interpreter's pairs.

**Amended for A1.** After the first pass the L1 issued amendment A1 (15 steps) and a grammar decision (a thirteenth column, `failing handler`). The artifacts listed here are the **A1** versions; `## A1 delta` at the end of this report states exactly what changed and carries the current numbers, and it supersedes the step counts and grid figures in §2-§6 where they differ. The A1 draft agrees with the A1 precedence on **38 664 of 38 664** reachable grid points and on **8 of 8** real dev envelopes.

Seat `R42C2TableDraft` (leaf: no subagent, no background job, never `agent://all`). Base
`c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`, read-only; nothing committed, no VCS mutation, no write outside
this report and `artifacts/R42C2TableDraft/`. Scratch `/fast/scratch/hyaku/kaidoku-r42/R42C2TableDraft`
removed at the end.

## 1. Deliverables

| file | sha256 | what |
|---|---|---|
| `block21.md` | `ac0d2beaaa64dcd615c79161a65808f0a255e822964d63fa8ef16bc63bc98ccb` | the paste-ready block (A1): bullet prose (family, container, residue, legacy repair, the 13-column grammar, three deltas), the scoped layout pre-check, `<!-- sqfs-triage-table v4 -->`, the 14-token action line, 15 rows |
| `block20-supersession.md` | `2cd1e9c1b145dd355a83e8d5c5fa44e134ca54141510922cc40e618e62571552` | the one sentence appended to block 20's bullet, with the exact old/new tail and the placement note |
| `entry.md` | `31eadeb8c20d148c78d1471dac9982967c95594f433acd6b182058201e82949f` | `corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md` draft in the v3 entry shape (7 `source:` rows, `verified-at`, `recheck`; A1 content, 12 limits) |
| `rationale.md` | `db268a0792da6fbb79f289e69567e495196a35be3b02efce2b879b2bd448701e` | clause → row map (15 steps), the 13-column grammar and its three deltas, the two new rows from sources and measured envelopes, the legacy-row justification, measurements, fallbacks |
| `v4-refparse.py` | `cf47c167792d2243d0a66a7a92fc5c19afac10cc96b45d71bc286ba74f73ab9c` | reference reader for the v4 A1 grammar (marker v4, 13 columns, `handler` over `F`, `failing handler` over `HF`, dependencies contains form); `--selftest` 12/12 |
| `precedence.py` | `393c6244882e00be183681386f7e890a0b42b2ae3bc0a213792aad2a95caa22a` | the A1 steps 1-15 as executable text, for self-checking only (never the frozen evaluator) |
| `check.py` | `84fa9560324a96ef753d2ddc9f279a722ce2075c86d9d222cd39e1791fb6a3c1` | grid + held-out + dev comparison over the reachable shapes, TSV writers |
| `make-fixture.sh` | `850578d0e7bd95174ce396f2180a2c52c2789972eee1ddd74b6a8648379aabbe` | rebuilds `fixture-SKILL.md` from the lane base + `block21.md` + the supersession sentence (asserts each anchor occurs once) |
| `make-measurements.sh` | `d849abf11a310044534797bd7226d9e43b62b7ebe42fac026d3393ab3900c224` | regenerates `measurements.md` (pins, fixtures, readers, argv, residue mint sites, damage arms, parse, checks) |
| `fixture-SKILL.md` | `10adf6784c6150c007e13ac51f1870c760f74eec8f7e4410642b55cbce0e0569` | the base `SKILL.md` with block 21 and the sentence applied — 1 570 lines, block at line 525 |
| `measurements.md` | `ca400a7bb9728083a33cf4d54adaf1886ef05d95977d0bcd9212149e26adc7b0` | every command with its verbatim output and exit code |
| `c-grid.tsv.gz` | `074659d9dd97d2fd09c0a1fa66551c875761b1193972f604edcb1a35cbc02844` | 38 664 reachable grid points with a `class` column; `gunzip` to read |
| `c-heldout.tsv` | `b4a6be00c663f41e24b037afadeddbb23de3a4141f13fb8065f899f1778073ba` | the 52 round-41 held-out envelopes: v4 pair, precedence pair, step, v3 pair, equality flags |
| `c-dev.tsv` | `bbc83b4bd6d620991259f169e3ceaff72ed311126d79170e32263fbfa6b44cd2` | the decisions on the 8 real dev envelopes |
| `c-v3pairs.tsv` | `ab80506ad797b2e8f55525b52e771aaa50091ef46cb03e71c117bf82d52caead` | the frozen v3 interpreter's 52 pairs on the round-41 held-out set |
| `block21-ctl-srno.md` | `44376a4339e267c99e817f3d40c7ca9e097537d1a516bfae516641f4b4540fc0` | control: rows 13-15 with `sr no` instead of `sr *` (decides 0 of 38 664 points differently) |
| `dev-v3le-d1.json` | `feba02a3188182f6b4d20c7389a355a65249b7c1c04d0df6d69f28125eb9deea` | real `squashfs_v3` REA 6.5.0 envelope, `--max-depth 1` |
| `dev-v3le-d3.json` | `ffe6d8db3f0fa6623975e0bf1120f33b8ecfa8c91c60ca2ffeb26e7f68e2dbb8` | real `squashfs_v3` REA 6.5.0 envelope, `--max-depth 3` |
| `squashfs_v1.0_be.bin` | `529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6` | unblob 26.6.4 MIT fixture (4 096 B) |
| `squashfs_v2.0_be.bin` | `79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0` | unblob 26.6.4 MIT fixture (4 096 B) |
| `squashfs_v3_be.bin` | `4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c` | unblob 26.6.4 MIT fixture (4 096 B) |
| `squashfs_v3_le.bin` | `0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7` | unblob 26.6.4 MIT fixture (4 096 B) |

## 2. What block 21 said before A1, in one paragraph (superseded by `## A1 delta`)

Thirteen rows in clause order — `no-squashfs-chunk`, `dep-missing-be`, `dep-missing-le`,
`partial-body-failure`, `avm-marker-be-dropped`, `legacy-body-failure`, `body-extractor-failure`,
`depth-limited`, `mixed-symlinks`, `escaping-symlink-removed`, `in-tree-symlink-metadata`, `clean`,
`clean-empty` — thirteen labels, thirteen action tokens (`cross-read-legacy` is the one new token). Every row
pins `extract_firmware`/`unblob`, so steps 1 and 13 are the no-match pair. Handler cells are fnmatch patterns
over `F` (the `squashfs_`-prefixed members of `H`, with `H` read from `chunks[].handler` ∪
`extraction_gaps[].handler` per the precedence text): `none` for `F = ∅`, `squashfs_*` for the family,
`squashfs_v[123]*` for the seven legacy names, `squashfs_v4_be` for the AVM-marker handler. Two grammar
deltas: the v4 marker (an older-only craft section is refused) and the `+` contains form in `dependencies`,
because clause 3 is membership and an exact-set cell lost a dependency set naming both binaries.

## 3. R41-CL4 repaired in prose, and executed

The repair is structural, not a cell edit: v3's row 1 already read `handler none`, but its other eleven rows
read `squashfs_v4_*`, so a carved v1–v3 chunk matched **no row**. v4 makes every non-AVM row family-wide and
keeps `none` for the true no-chunk case. The block's own words: a v1–v3 chunk is not `no-squashfs-chunk`
because unblob carves it with one of seven handlers (S112 :102,:159,:200,:245,:319,:364,:410) and runs plain
`sasquatch` on it (S112 :37,:51-54) — an extraction outcome about a filesystem the finder did see, not a
missing input, and `inspect-input` would send the reader to inspect the wrong thing.

Measured end to end on a fresh dev input (unblob's own MIT v3 fixture, allowed as development by the
reservation):

```
$ REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json \
    --full-output --max-depth 1 fx/squashfs_v3_le.bin out/rea-v3le            # exit 0
  envelope: H=['squashfs_v3'] G=['depth-limited'] P=2 BE=n/a SR=no
$ python3 -I -B tools/round-41/sqfs-triage-v3.py --skill base-SKILL.md dev-v3le-d1.json dev-v3le-d3.json
dev-v3le-d1.json        unclassified    none
dev-v3le-d3.json        unclassified    none
$ python3 -I -B v4-refparse.py --skill fixture-SKILL.md --json dev-v3le-d1.json dev-v3le-d3.json
dev-v3le-d1.json        depth-limited   raise-depth     8
dev-v3le-d3.json        clean           none            12
```

The second envelope is the same fixture at `--max-depth 3` (`G = ∅`). So the two fates v4 distinguishes — a
depth ceiling and a clean legacy extraction — both fall out of real REA 6.5.0 envelopes, and the frozen v3
table answers neither.

## 4. The `legacy-body-failure` row's action, justified from sources and measurement

Action `cross-read-legacy` (never the `-be` wrapper):

1. **The AVM pre-check cannot apply.** unblob parses the marker (`is_avm = header.bytes_used ==
   header.mkfs_time`) and appends `-be` only inside `case Endian.BIG, 4:` (S112 :40-50); every other version
   takes `case Endian.BIG, _` → `-be` or `case Endian.LITTLE, _` → `-le` and parses no header (S112 :51-54).
   v1/v2 inherit the base extractor and v3's family only overrides the magic (S112 :75,:323,:368,:414).
   Measured on the wire with unblob 26.6.4: `handler=squashfs_v3 … command='sasquatch -le -no-exit-code -f -d
   …'` for the LE fixture and `sasquatch -be …` for the BE one.
2. **`unsquashfs` is a genuine second reader of 1:0-3:0.** 4.7.5 prints `Found a valid … SQUASHFS 1:0 / 2:0 /
   3:0 superblock` and lists the trees of all four fixtures (both endiannesses, exit 0); 7-Zip 26.04 lists the
   same v3 trees and marks the BE one `Big-endian = +`. On six damaged copies the superblock still parses
   (`unsquashfs -s` exit 0) while both readers fail with the message sasquatch itself prints
   (`read_fragment_table: failed to read fragment table block` / `FATAL ERROR: File system corruption
   detected`; on other regions `read_ids`/`parse_exports_table: Bad inode count`). Agreement = damage;
   a listing independent reader beside a failing sasquatch = extractor build or argv fault. That is exactly
   the separation the action prescribes, and the intact control (`unsquashfs -lls` exit 0, `sasquatch` exit 0,
   `apple.txt` + `cherry.txt`) is the other end of it.

The row does not carry the wrapper because `-be` is a v4-BE reading fix; a v1–v3 body has no marker field to
mis-read.

## 5. Block-20 prose repairs carried (and two re-scoped)

Carried verbatim where still true: M1 (no embedded copy), M2/M3 (body row scoped to its own population, the
pre-check overrides the cell), L3 (both dependency rows cite S119 as the minter), L4 (partial row cites the
measured 4-of-5 oracle match), L6 (clean row: `SR = no` never proves no link was dropped — S118 :67-69), L7
(`none` double duty disclosed), F4 (`dependencies` redundant with handler on every measured class). Two are
re-scoped in the v4 text: the pre-check now says **BE-structural** body before it says AVM layout (round-41 w2
F6), and the drop-`-be` wrapper's PATH delivery is marked `[INFERENCE]` because only its body-side effect is
measured (round-41 w2 F3; MH-6: four files without the flag, zero with it). L3's defect is also *repaired*
rather than carried: v3's claim that "a dependency list naming both resolves to the BE row above" was false
under exact-set cells (round-41 w2 F1, MEDIUM); v4's contains cells make it true — measured below.

## 6. Pre-freeze checks (exact commands, exit codes)

All from the artifacts directory or scratch with `TMPDIR` set; no REA/unblob/sasquatch run on any reserved
carrier (the only REA and unblob runs used unblob's own MIT v3 fixture).

| check | command | result |
|---|---|---|
| fixture builds and block parses in situ | `make-fixture.sh LANE c4a38ea2… fixture-SKILL.md`; `v4-refparse.py --table-only` | `fixture written (1555 lines)`; `marker line: 512 actions line: 513 table line: 514 rules: 13`, exit 0 |
| reader refuses a superseded marker, accepts the deltas | `v4-refparse.py --selftest` | `cases: 11, failures: 0`, exit 0 (`v3-only-refused` exit 2, `dep-contains-ok` exit 0, `handler-class-ok` exit 0) |
| **pre-A1 (13 steps)** drafted block vs drafted precedence, whole grid | `check.py --skill fixture-SKILL.md --heldout … --dev … --out-prefix c` | `grid: 46656 points, 45424 agree, 1232 seam (168 multifamily, 1064 orphan), 0 other`, exit 0 |
| regression on the round-41 held-out set | same run | `heldout: 52 envelopes, 52 agree, 0 seam, 0 other; v4==v3 on 52` |
| real AVM receipts | `v4-refparse.py --json c1/{V3,V4,L3,L4}/after.json`; same with the v3 interpreter | all four `(depth-limited, raise-depth)` under both |
| the two dev legacy envelopes | as §3 | v4 `(depth-limited, raise-depth)` / `(clean, none)`; v3 `(unclassified, none)` on both |
| dependency membership | `c-grid.tsv.gz`, `deps=both` ∧ dep gap | **2 016 / 2 016 agree** (exact-set cells labelled these `unclassified`) |
| **pre-A1** the `sr *` loosening is neutral | `block21-ctl-srno.md` fixture, same grid, row-for-row diff | **0** of 46 656 points differ |

## 7. Findings for the L1

**F1 — RESOLVED BY A1, kept as the record — steps 5/6 said "the failing handler" and the table has no such column.** A handler cell
matches *some* member of `F`. Single-family envelopes (every measured carrier, all 52 held-out, all real AVM
receipts) make the two readings coincide; a two-family envelope does not. With `F = {squashfs_v3,
squashfs_v4_be}`, `G ∋ extractor-failure`, `P = 0`, `-be` absent the table answers
`(avm-marker-be-dropped, wrap-extractor-be)` where the text says `(legacy-body-failure, cross-read-legacy)`;
with `-be` recorded the mirror image. The grid counts 168 such points out of 46 656 (`c-grid.tsv.gz`,
`class=seam-multifamily`). Two-family envelopes are REA-reachable in principle (a legacy rootfs carrying a v4
BE child) and present in nothing measured. **Decision needed:** either the round-42 held-out generator excludes
two-family envelopes (my recommendation — it keeps the text and the table equal on everything scored), or the
precedence says "a handler in `H`" instead of "the failing handler" and the draft's rows already implement it.
I drafted the table to the text and disclosed the seam in the entry's Limits and in the block's cause cells;
`rationale.md` §5 has the census and the sentence to change.

**F2 — MEDIUM — `squashfs_v4_broadcom` shares the v4-BE extractor branch but clause 5 names only
`squashfs_v4_be`.** `SquashFSv4BroadcomHandler.EXTRACTOR = SquashFSExtractor(4, 0x71687368)` (S112 :549,:553),
so its body takes the same `Endian.BIG, 4` path: `sasquatch-v4be`, AVM marker parsed, `-be` dropped only on the
marker. A broadcom BE failure with `P = 0` and `-be` absent therefore lands on the body row (`preserve-failure`)
while the pre-check would prescribe the wrap. `[INFERENCE]` — no broadcom envelope was measured, and the
precedence text is the L1's to change. Cheapest repair: clause 5 reads "failing handler `squashfs_v4_be` **or**
`squashfs_v4_broadcom`", and row 5's handler cell becomes `squashfs_v4_be` plus one more row would be needed
(one label owns one row), so the alternative is to keep the label and accept the body-row fate, disclosed.

**F3 — MEDIUM — the draft's R41-CL4 sentence is imprecise for the interpreter.** See §8.

**F4 — LOW — step 3's bracketed note is now measured and needs no wording change.** "[to be confirmed by wave 1
on real REA envelopes]" — confirmed from source and from the wire: every v1–v3 chunk resolves plain `sasquatch`
(S112 :37,:51-54; `sasquatch -le` on the LE fixture, `sasquatch -be` on the BE one). A consequence the draft did
not state and the block does: a v1–v3 **BE** chunk records `-be`, so `dep-missing-le` names the missing
**binary**, never the image endianness. No row may require `be no` for the plain-binary gap.

**F5 — LOW — two grammar deltas are now on the v4 interpreter's contract.** The marker refusal and the
`dependencies` contains form (`name+`) must be implemented by `tools/round-42/sqfs-triage-v4.py`, and `H` must be
chunks ∪ gaps (the v3 reader used chunks only). If the contains form is rejected, round-41 F1 returns
(`D = {sasquatch, sasquatch-v4be}` → `unclassified`); fallbacks are in `rationale.md` §7.

**F6 — INFO — no row may require `be yes`.** Both dev envelopes carry `BE = n/a` on a clean REA 6.5.0 run: the
child argv is not surfaced when nothing failed, so `-be` is unrecorded. The draft's rows all use `*` for `be`
except the AVM row's `no`, which a failed command supplies (`ExtractReportFailedReport.command`, S120 :91-98).

## 8. Conflicts, verbatim (for the canonical judge)

- `plans/round-42-claims.md` § R42-C2, surface-moved paragraph: *"routed defect R41-CL4: v3 sends every v1-v3
  chunk to `no-squashfs-chunk`"*.
- `corpus/lessons/round-41.md` § Routed defects: *"R41-CL4 | the interpreter's handler `none` (no `squashfs*`
  chunk) and the precedence's step 2 (no `squashfs_v4_*` handler) diverge on a v1–v3-only chunk"*.
- `corpus/lessons/round-41-verifier-spotcheck.md` §5 and round-41 w2 `R41W2C2Table.md` F5, executed: *"interp
  `(unclassified, none)` vs eval `(no-squashfs-chunk, inspect-input)`"*.

My measurement agrees with the lesson and the w2 review, not with the claims' sentence: the frozen v3
*interpreter* sends both dev legacy envelopes to `(unclassified, none)` (the log is in `measurements.md` §7);
`no-squashfs-chunk` is the v3 *precedence's* answer. The block's prose states both fates ("v3's precedence
answered `no-squashfs-chunk` … while v3's table answered `unclassified`"), so no freeze path depends on the
disagreement — but the claims sentence should be corrected, because a reader who trusts it will look for a
defect the interpreter does not have.

A second, smaller wording conflict: `plans/round-42-claims.md` says the held-out set is *"the round-41 v4
classes, new legacy-family classes … and a widened `combo` family whose factors include the handler family"*,
and the table cannot separate the failing handler (F1). If the widened combos draw a handler-family factor
per *chunk* while the gap names another chunk, F1 becomes a mismatch on the scored set, not a disclosure. This
is the decision F1 asks for.

## 9. Out of scope, and what I did not do

- No lane tool written: `tools/round-42/*` is the L1's integration. The reference reader lives in the artifacts
  directory and is labelled as such in its docstring, so it cannot be mistaken for the frozen interpreter.
- The frozen interpreter, evaluator, generator, counter and control tables are other seats; nothing here
  scores the claim.
- I did not run REA, unblob or sasquatch on any C1 candidate or on anything carved from one. No third-party
  firmware was downloaded; the only inputs were unblob's MIT fixtures (copied, 4 KiB each) and the lane's
  committed envelopes.
- I did not edit block 19's supersession sentence (its round-41 w2 F4 defect is out of this seat's scope) or
  block 18.
- `block21.md` is a draft: the L1 chooses placement (after block 20's table, before `## Config custody`, as the
  base's line 449-454 layout implies) and decides F1/F2.

## 10. Tooling record

Nothing installed, upgraded or removed; no pacman transaction; no write into `~/.local/bin` or any PATH
directory. Used: system `python3` (3.13), `unsquashfs` 4.7.5, 7-Zip 26.04, `sasquatch` 4.5.1,
`unblob` 26.6.4 (installed tree), `npx -y rea-agents@6.5.0`, read-only `git show`, `curl` (four fixture
fetches), `sha256sum`/`awk`/`grep` over scratch copies.

## 11. Artifact paths

All under `.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/`; the table of digests is §1. Scratch
`/fast/scratch/hyaku/kaidoku-r42/R42C2TableDraft` removed before yield; no scratch or `/tmp` path is cited as
evidence, and every cited path resolves inside the lane.

## A1 delta

**What A1 changed, and what the drafts now say.** The precedence I drafted against was re-issued as amendment
A1 (15 steps) with a grammar decision from the L1: a thirteenth column, `failing handler`, after `handler`.
Both are implemented.

- **Rows: 13 → 15.** `container-depth-limited` / `raise-depth` (step 2, `F = ∅` ∧ `depth-limited ∈ G`) and
  `unknown-residue` / `isolate-residue` (step 9, `unknown-chunk-handler ∈ G`, placed **above** the depth row).
  `legacy-body-failure` moved from a handler test to the failing-handler test (step 7). Two new action tokens;
  the vocabulary line now has 14 tokens (`raise-depth` is used twice).
- **Grammar: twelve columns → thirteen.** `handler` is a glob over `F` (`none` = `F` empty); the new
  `failing handler` column is a glob over `HF` (handlers of the `extractor-failure` gaps, `F` when none carries
  one; `*` matches anything, an empty `HF` included). Only steps 6 and 7 name it. `dependencies` keeps the `+`
  contains form. `H` is still chunks ∪ gaps. My first pass had drafted an `hf:` cell prefix; the L1's column
  replaced it, and no `hf:` text survives in `block21.md`.
- **The seam F1 is gone.** With one handler column keyed on `F`, a two-chunk envelope (`F = {squashfs_v3,
  squashfs_v4_be}`, one chunk failing) could not say which chunk failed: 168 grid points diverged from the text.
  With `failing handler` keyed on `HF` the drafted block and the executable precedence agree on **all 38 664**
  reachable points (`check.py`, `c-grid.tsv.gz`, `class` column all `agree`). **Nothing about the held-out
  generator needs to change for this**; the earlier recommendation to exclude two-family envelopes is
  withdrawn.

**Sources re-opened for the new rows** (verbatim lines in `measurements.md` §3b and the source ledger):

| claim | source | line evidence |
|---|---|---|
| `depth-limited` is minted per un-descended path, empty deps, with a rerun continuation; ceiling is 10 | S119 `FirmwarePublication.js` | `:23` `MAX_EXTRACTION_DEPTH = 10`, `:24-29` continuation, `:294-299` gap mint |
| `unknown-chunk-handler` is minted per chunk with a null handler | S119 `FirmwarePublication.js` | `:286` `chunkGaps("unknown-chunk-handler", (chunk) => chunk.handler === null)`, `chunkGaps` body `:226-238` copies `handler: chunk.handler` |
| the residue is carved as `<start>-<end>.unknown` beside the tree | S118 `extractor.py` | `:116-127`, `extension = "unknown"` `:119`, `filename = f"{chunk.start_offset}-{chunk.end_offset}.{extension}"` `:123` |
| a v1–v3 chunk runs plain `sasquatch` with an explicit `-be`/`-le` and no header parse | S112 `squashfs.py` | `:37` executable reset, `:40-41` v4-BE branch, `:42-50` AVM marker, `:51-54` `BIG,_` → `-be`, `LITTLE,_` → `-le` |
| a gap's handler is its chunk's (so `HF ⊆ F` on reachable envelopes) | S119 `FirmwarePublication.js` | `:226-238` |

**Observed envelopes** (committed by `R42C1DevRun`, read-only):

```
trx-img-with.json     H=[] (the only handler is trx_v1)  G=[depth-limited]  P=3    -> container-depth-limited / raise-depth
x86-fs-with.json      H=[squashfs_v3]  G=[depth-limited, unknown-chunk-handler, unpublished-entry]  P=138
                                                    published firmware.bin_extract/786432-851972.unknown
                                                                              -> unknown-residue / isolate-residue
```

**A1 measurements** (all reproducible: `make-fixture.sh`, `make-measurements.sh`, `check.py`):

| measurement | A1 result |
|---|---|
| block parses in situ | `marker line: 525  actions line: 526  table line: 527  rules: 15`, 14 action tokens, exit 0 |
| reader selftest | 12 cases, 0 failures (`v3-only-refused`, `twelve-cells-refused` both exit 2) |
| grid over reachable shapes (`HF ⊆ F`) | **38 664 points, 38 664 agree, 0 differ** |
| round-41 held-out, 52 envelopes | **52/52** vs the precedence and **52/52** vs the frozen v3 interpreter's pairs |
| 8 real dev envelopes | draft vs precedence **8/8**; frozen v3 interpreter **0/8** — six `unclassified`, and `no-squashfs-chunk` on the two whole-TRX runs that A1 makes `container-depth-limited` |
| four round-41 C1 receipts | both engines `(depth-limited, raise-depth)` |
| dependency membership (`D` names both binaries) | 2 016/2 016 `dep-missing-be` |
| `sr no` control (`block21-ctl-srno.md`) | 0 of 38 664 points differ |

**Findings, updated.**

- **A1-F1 — BLOCKING, unchanged in kind — `squashfs_v4_broadcom` is not step 6's handler.** `EXTRACTOR =
  SquashFSExtractor(4, 0x71687368)` (S112 :549,:553) puts a broadcom BE body on the same `Endian.BIG, 4` path
  (`sasquatch-v4be`, AVM marker parsed), but step 6 names only `squashfs_v4_be`, so a broadcom BE failure with
  `P = 0` and `-be` absent lands on the body row while the pre-check would prescribe the wrap. `[INFERENCE]`, no
  broadcom envelope measured. A1's `failing handler` column makes the repair cheap (a second name in that cell
  is still one row, since the cell is a glob: `squashfs_v4_be` could become a two-name glob only if the
  grammar allowed alternation — it does not, so this needs a second row and a second label, or the text's
  acceptance of the body-row fate).
- **A1-F2 — LOW — step 7's `HF ∩ L` is not a table predicate.** `L` is defined over `F`, so `HF ∩ L` also
  requires the failing handler to be a handler *of this envelope*. The table says "`HF` matches a legacy name".
  They coincide whenever `HF ⊆ F`, which is every envelope REA can mint (a gap's handler is its chunk's,
  S119 :226-238); the grid therefore enumerates `HF ⊆ F` and the divergence on synthetic non-subset `HF` is
  disclosed in the entry's Limits (1). No action needed unless a control table is built with a non-subset `HF`.
- **A1-F3 — INFO — step 2 and step 10 both answer `raise-depth`.** Two labels, one action; the action column
  cannot distinguish "container below the ceiling" from "SquashFS chunk below the ceiling", only the label can.
  That is deliberate in A1 (the container row's point is the *label* and the refusal to say `inspect-input`), but
  it means an actions-rotated control cannot separate them.
- **A1-F4 — INFO — `unknown-residue` is reachable only with a SquashFS chunk present.** Step 3 takes `F = ∅`
  first (unless a depth gap is there, step 2), so an envelope whose only evidence is an `unknown-chunk-handler`
  gap with no SquashFS chunk is `no-squashfs-chunk`. The entry's Limits (4) states it; the held-out generator
  must not build a residue class without a SquashFS chunk.

**Verdict for the A1 pass: DONE.** `block21.md`, `entry.md`, `rationale.md` and the reference reader are the A1
versions; the block parses as 15 rules, the reader's selftest is 12/12, and the draft equals the A1 precedence on
every reachable grid point and on all eight real envelopes, with the v3 interpreter's failures on those eight
recorded for the delta claim. Scratch removed before yield; §1 digests are the A1 bytes.
