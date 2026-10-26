# R40W2C1AxisFit — the R40-C1 honest-stop handling: demotion, coverage read, S126 lineage

**Verdict: DEFECTS FOUND** — the demotion itself is correct and complete; the *record of why* is not:
the single clause that produced `exit 1` is absent from the frozen predicate P40-C1, and that clause
is implemented with a suffix test that flags a symlink's own in-tree target. One residual identity
defect survives the demotion (the `-core` entry stem, now hard-coded in two frozen counters) and the
lineage paragraph has two precision defects.

**Attacked:** (a) the claim that nothing at `4d62ee5a86b4692a13f682b29ed7975e8d7e5326` still asserts
AVM-BE is Core; (b) whether demotion is the right call under prompt §6 item 9 and the `## Round 38`
precedent; (c) whether C1 was a coverage move had it passed; (d) the entry's assimilated lineage
against S126. Leaf seat: no subagents, no mutation, no REA/unblob/sasquatch run, no vendor bytes
fetched. Evidence: committed receipts, committed bytes and read-only git; probe log and copies in
`.ufo/waves/round-40/w2/artifacts/R40W2C1AxisFit/` (`probes.md`, `c1-score-at-42c10a58.json`,
`c1-receipt-at-42c10a58.json`, `claims-at-freeze.md`, `claims-at-4d62ee5a.md`).

## (a) Does anything at 4d62ee5a still assert AVM-BE is Core?

**No prose site does; one identity artifact does.** Full non-`.ufo` sweep (`git grep … 4d62ee5a --
':!.ufo'`) returns 13 sites: PROVINCE heading/row/note (386, 392, 394), corpus/README 96, 208, 250,
six SOURCES `used-by` rows (S112, S114, S121, S124-126), and the r39 correction line (41). Every
PROVINCE/README site says `measured, not promoted`; the SOURCES rows are registry cells that make no
status claim. `SCORECARD.md` has no round-40 record yet, `corpus/QUALITY.md` has no AVM/SquashFS line,
`SHONEN.md` has no round-40 AVM line, and `## Round-40 additions to Core` exists nowhere outside
`.ufo/` wave evidence — so the counter's own `province_core_section`/`province_core_row`/
`frontier_note` bindings are false at the tip, which is the intended post-score state. The demotion
touched no C1 frozen path (`FROZEN_PATHS` at `c1-counter.py:208-219` plus carriers.json's
path/oracle/nonregular values; `git show --stat 4d62ee5a` = PROVINCE, README, entry), so it cannot
trip `frozen_path_changed`.

Residual defect **D3 (identity, minor).** The entry stem is
`2026-10-26-r40-avm-be-squashfs-core`. `-core` is this corpus's promotion marker — the round-39 Core
entry is `…-r39-be-squashfs-v4-core`, the round-38 unpromoted entry is
`…-r38-sasquatch-be-squashfs-recursion` with no suffix, and only two entries in `corpus/knowledge/`
end in `-core.md`. So the one identifier that still reads "core" is the filename, cited 13 times.
It cannot be renamed inside this round: `c1-counter.py:191-192` and `c1-extra.py:36-37` hard-code
`ENTRY`/`STEM`, and both are frozen paths — a rename would make any future score fail `entry_present`
/ `sourced` / `coverage_map_row` against a rule that can no longer be edited. The honest-stop record
does not disclose this. Smallest safe correction: one clause in the round-40 record — "the entry stem
keeps the `-core` form the frozen counters hard-code; it is renamed in the round that re-freezes the
counter" — and a lesson line (see D1) so the re-freeze carries both changes.

## (b) Is the demotion the right call?

**Yes, and for the reason the prompt gives.** §6 item 9: "Never narrow a target after landing: a miss
is an honest stop" and "the claim is judged on the counter, kill rule and predicate declared before
data … whatever attacks it later passes (kumitate r42)". Keeping Core after `exit_code 1 /
met_target false` would be the violation; fixing the counter and re-scoring in the same round would
replace the claim's rule after the score. The round-38 precedent agrees on direction: R38-C1 recorded
`carriers_matched 3, met_target false, exit 1` with the Core-row bindings false, and BE stayed
Frontier with a `measured, not promoted` entry. Round 40's demotion reproduces that shape in the
opposite order (r39/r40 land the promotion text, score it, then demote on a miss).

The record's receipt discipline is sound: `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.receipt.json`
records `exit_code 1` and the verbatim argv (R39-CL6 satisfied); the score json records
`carriers_matched 3`, `target 4`, `met_target false`, `frozen_path_changed []`,
`carriers_unchanged true`, `gap_rule_unchanged true`. The claims file is byte-identical freeze→tip
(`cmp` exit 0), so no post-freeze predicate edit.

Three defects in what the demotion *says*:

**D1 (major, freeze integrity).** The only failing clause, `nonregular_unpublished_ok`, is **not in
the frozen predicate sentence**. P40-C1 (`plans/round-40-claims.md:38-51`) requires: handler + no
failed chunk; every oracle regular file published (suffix, sha256); gaps only as the gap rule allows;
subject digest = pin; evidence id recomputes; carrier pin + AVM marker + LE metadata lengths; fresh
REA rerun with the same `plus-extractor` projection; the frozen reader reproducing its tables; the
doc bindings; no frozen path changed. The counter enforces two further per-carrier clauses —
`nonregular_unpublished_ok` and `run_provenance_ok` (`c1-counter.py:227-231`). Dumping
`carriers.L2` from the score receipt, every clause is true except `nonregular_unpublished_ok`;
`run_provenance_ok` is true on all four. So the **sole** cause of the miss is a condition the frozen
rule never states. [INFERENCE, derived from the receipt's clause table, not a rerun: read as written,
P40-C1 is met on all four carriers at `42c10a58`.] §6 item 9 asks for "one predicate that is the same
sentence in the plan, the same condition in the counter's code and the same label in the receipt";
here the plan sentence is narrower than the code by one load-bearing clause. A non-author judge
reproducing the claim from the predicate alone cannot reach `exit 1`. The wave-1 counter report did
announce the clause (`.ufo/waves/round-40/w1/R40C1Counter.md:51`), but announcement is not the frozen
rule.

**D2 (major, implementation).** That clause's docstring says "no published regular file path
**equals** a non-regular entry path" (`c1-counter.py:54-56`), while the code tests a path-suffix
(`same_rel`, `:606-607`). Measured blast radius: V1 0/697, V2 0/8, L1 0/7, L2 1/6 published files hit.
L2's single hit is the symlink's own target — `nonregular.tsv` `bin/busy symlink ../usr/bin/busy`,
`oracle.tsv` `usr/bin/busy e28f81fc… 40000`, published as a regular file with the oracle's sha256 —
while both L2 symlinks are correctly unpublished and gap-carrying. This is therefore not a fixture
oddity: any carrier whose symlink points at an in-tree file that shares tail segments trips it, and
V1/V2/L1 only escaped by layout luck. The L1's one-line diagnosis ("suffix false positive") is
correct but understates it: `equals` in the docstring and `endswith` in the code are different
conditions, and "the symlink's own target" is the counterexample.

**D3 (calibration, minor — with D1/D2).** The record states only the suffix cause. It should also
state that (i) the failing condition is absent from P40-C1's frozen sentence, and (ii) at the measured
revision the promotion text was already landed and green — the score receipt records
`province_core_section true`, `province_core_row true`, `frontier_note true`, `coverage_map_row true`,
`sourced true`. Those doc bindings are self-certifying (the lane writes the heading, note, README row
and `used-by` cell that the counter then checks), so the sequence land-Core → score → demote leaves
one pinned revision whose PROVINCE table carries a "Verified evidence" cell for a surface the score at
that same revision rejects. That is a predicate-design defect, not an L1 error: the frozen predicate
requires the Core row at the measured revision, so the promotion text cannot be scored as a claim
before it is landed as fact. Disclosing it is the only in-round repair.

Smallest safe corrections (all record-level; nothing re-scored, nothing re-frozen):
1. Round-40 record / lesson: state D1 — the miss rests on a counter clause absent from P40-C1 — and
   that the re-freeze must either state the clause or drop it (state it: materialisation is a real
   failure mode).
2. Round-40 record: state D2's counterexample — symlink `bin/busy` → `../usr/bin/busy` with the target
   published and in the oracle — so the re-frozen clause tests exact path equality after the
   extraction root is stripped (equivalently: exempt paths the frozen oracle lists as regular files).
   That keeps the "materialised symlink" control red (`c1-counter.py:1775-1787`) and makes L2 green.
3. Round-40 record: D3's two sentences above.
4. Closure note: keep the demotion (no coverage credit), name the `-core` stem as frozen-counter
   baggage to rename at the re-freeze.

## (c) Was C1 a coverage move had it passed?

**Yes — the surface is a format class, not a new input set.** The frontier it would have moved is
named twice: `PROVINCE.md:156-157` ("big-endian/AVM stays here") and `PROVINCE.md:384` ("AVM-BE bodies
and vendor-mangled images stay Frontier"). The round-39 Core row explicitly *excluded* the surface —
`SCORECARD.md:628`: "AVM-marked BE bodies, vendor-mangled images and extra published files are not
claimed". The probe exercises the other handler branch: `unblob` omits `-be` when
`mkfs_time == bytes_used`, and the body's 2-byte metadata headers are little-endian while the
superblock is big-endian (`layout_ok`: the LE walk from `inode_table_start` lands on
`directory_table_start`, the BE decode does not). A different reader path and a different on-disk
invariant is an edge class, exactly the §6 item 9 sense of coverage ("a new tool, operation or edge
class").

The two vendor carriers are evidence, not the surface: they are what makes "vendor-mangled images"
real (two model families, FRITZ!OS 7.30/7.57, no REA or unblob run touched them before the freeze),
and the claim's own frontier note kept "other vendor-mangled images" Frontier rather than promoting
vendor images wholesale — the calibration-correct scope. Counterexample tested: had the surface been
"standard BE v4 on two more images", §6 item 9's "re-scoring a rule the lane already holds on new
inputs" would apply and the round would be quality work, not coverage. The layout identity test is
what separates the two, and it is stated before data and re-derived independently.

Consequence for this round: the measurement itself is intact (all four carriers publish every oracle
file with matching sha256 at `oracle_hits_ok` 6/6 for L2 and 697/8/7/6 published overall;
`projection_ok` true on the reruns), so the coverage *work* is done and the *credit* is correctly
withheld. That asymmetry is exactly why D1 must be recorded: the next round inherits a measured
surface plus a rule whose stated sentence says it passed.

## (d) Is the entry's lineage paragraph accurate to S126?

**Substantively yes; every checkable value reproduces; two precision defects.**

| entry claim | check | result |
|---|---|---|
| "a 4096-byte genuine AVM-BE image" | `sha256sum`, file size | `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`, 4096 B — matches the entry and E3's digest |
| "saw unblob run `sasquatch-v4be -no-exit-code -f -d …` with no `-be`" | `round11/work/unblob.log`, `lead1-avm-image.tsv` `unblob_be_flag` | argv verbatim, no `-be`; flag row "absent - the AVM branch passes no `-be`" |
| "publish its four files" | same log (four `Processing file` lines, sizes) + TSV `extracted_files` | four files (`apple1…4.txt`), no failure line |
| "first header `7400` → LE 116, `121 + 2 + 116 = 239 = directory_table_start`" | stdlib superblock parse of the retained image | `inode_table_start 121`, header bytes `74 00` → LE 116, BE 29696 fails; `121 + 2 + 116 = 239 == directory_table_start` |
| marker | parse | `mkfs_time 365 == bytes_used 365` |
| "the round-11 log carries no exit code, so it is lineage, not a scored receipt" | both logs | no unblob exit code in `unblob.log` or `avm-final.log` (only `make exit=0`) |
| "The lane's rounds 9-11 lead built …" | `shokuknow/merge/kaidoku/MERGE-REPORT.md:76,78,79` | r9 `sasquatch-unblob-avm-branch`, r10 `avm-image-build-blocker`, r11 `avm-image-extraction` — matches |

Defects:
- **D4 (provenance, minor).** The header/`directory_table_start` step is attributed to S126, but
  S126's row list (`SOURCES.md:132`) carries only `image_path`, magic, compression id, `mkfs_time`,
  `bytes_used`, `image_is_avm`, handler, `be_flag`, `extracted_files` and contents — no
  `inode_table_start`/`directory_table_start`, and no metadata header bytes. The number is true and
  re-derives from the retained image, but the observation belongs to this round's own re-measure
  (`.ufo/waves/round-40/w1/R40AssimE3.md` §2 measured exactly the same three numbers). Smallest fix:
  cite the retained image path or `R40AssimE3.md` for that parenthetical instead of S126.
- **D5 (precision, minor).** The workdir holds a *failed* earlier attempt — `avm-final.log`
  "Can't run extract command / dependencies=['sasquatch-v4be']" — while the successful run is
  `unblob.log`. The entry says "the round-11 log carries no exit code", which is true of both, but a
  reader who opens `avm-final.log` first finds a contradiction with "saw unblob … publish its four
  files". Smallest fix: name `unblob.log` as the log that records the successful argv and note the
  earlier dependency-miss attempt.

No false claim found: the paragraph is lineage-labelled, not receipt-labelled, and the entry's own
limits paragraph keeps "cannot prove which process wrote a committed receipt" honest.

## Observations outside the item

- Inherited uncommitted state at review time: `SKILL.md` is modified (+19 lines, a "Round-40 instrument
  registry" table) and untracked `.ufo/waves/round-40/{r40-w1-status.json,w2.ready,w2.ready.partial}`
  exist (`git status --porcelain`). Not mine, not touched; the L1 must commit or revert the SKILL diff
  before the round lands.
- No tool installed, upgraded or removed; no package manager run. Scratch
  `/fast/scratch/hyaku/kaidoku-r40/R40W2C1AxisFit` created empty and removed.

## Impacted axes

- **coverage** — the surface move is real and measured; credit correctly withheld by the honest stop.
  The demotion is the right value; D3 is the identity cost (one pinned revision carried a live Core
  assertion).
- **depth** — untouched by this seat.
- **calibration** — the real cost: D1 (stated predicate narrower than the enforced rule) and D2
  (`equals` vs suffix) mean the published `3/4` cannot be reproduced from the predicate, and the
  record's cause sentence explains only D2. Fixable at record level without touching the freeze.
