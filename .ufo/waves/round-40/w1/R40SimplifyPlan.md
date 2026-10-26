# R40SimplifyPlan — minimality review of the round-40 DRAFT claims

**Verdict: DEFECTS FOUND** — the draft carries 14 clauses that either cost a new convention or
cannot be graded, two of them fatal to the round's own purpose (an unenumerated "semantic
projection" that the round-39 fabricator already satisfies, and a "gap rule fixed from development
recon" whose development image does not exist once V1 and V2 take both known AVM-BE vendor images).
The shortest predicates below keep every kill control red with 3 carriers, not 4, and with 12
graded labels, not a 13-row action vocabulary.

Seat: simplifier (leaf). Lane tree untouched except this report and
`.ufo/waves/round-40/w1/artifacts/R40SimplifyPlan/`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40SimplifyPlan` removed at exit. No tool installed, no pacman
transaction, no REA, no unblob, no sasquatch invocation. No VCS mutation (read-only `git show`,
`git log`; no fixture repos needed). Read-only reads of `/home/vgpnk/Projects/shokuknow`: none.

## Axes named (Godspeed)

| axis | what this review moves |
|---|---|
| **coverage** | the C1 carrier set: which carriers buy new ground (vendor provenance, gzip leg, xz leg) and which is a duplicate filesystem re-stamped |
| **depth** | the C2 decision count: 12 labels that a table must produce, versus a 26-envelope score that a duplicate replicate can inflate |
| **calibration** | the gap between the predicate sentence and what the counter can enumerate: 8 phrases in the draft name a check no code can perform |

## 1. Method

For every clause I asked one question: *which frozen kill control goes green if this clause is
deleted?* A clause that kills nothing **and** costs a new convention, a new dependency, or a
scoring-time failure mode is a deletion. A clause that kills nothing but is a cheap scalar stays
(cheap redundancy is not weight). I re-read the counters and the frozen table schema, the round-39
closure defects (R39-CL1..CL6), the round-39 fabrication control `w2/R39W2C1Fabricate.md`, the AVM
critic's byte matrix, and probed AVM's live download catalogue for the V2/CD-recon question (§6).

## 2. P40-C1 clause ledger

Legend: **keep** = enumerated by a check and kills a named control; **keep-cheap** = redundant for
grading, kept for a diagnostic reason; **drop** = no control needs it and it costs something;
**rewrite** = right intent, non-enumerable wording.

| # | draft clause (abridged) | gradeable? | kills | verdict |
|---|---|---|---|---|
| 1 | "for each frozen AVM carrier" + `carriers_matched == 4` | yes (`carriers.json`, `carrier_pin_ok`) | C1-0 do-nothing | keep, N=3 (§6) |
| 2 | "committed round-40 REA 6.5.0 `extract-firmware` after-receipt" | yes | C1-0 | keep |
| 3 | "(unblob 26.6.4, sasquatch-v4be 4.5.1 on the child PATH)" | **no** — no counter field reads a version (round-39 `grep -c engine` = 0) | nothing | **rewrite**: one executable precondition (exit 2 unless the scoring host's `unblob --version` is 26.6.4), else label "not graded" |
| 4 | "first added in a commit descending from the freeze" | yes (`receipt_first_add`) | C1 "receipts added in the freeze commit" | keep |
| 5 | "names the `squashfs_v4_be` handler" | yes | relabelled non-squash receipt | keep |
| 6 | "with no failed chunk" | yes (`chunks_ok`) | partial/body-failure receipts | keep |
| 7 | "publishes every regular file of the frozen independent oracle (same relative-path suffix, same sha256)" | yes (`oracle_hits == oracle_files`) | C1-3/C1-4 | keep |
| 8 | "carries only the extraction gaps the frozen gap rule allows (rule fixed in the freeze from development recon, never from carrier runs)" | **no, as worded** — "the frozen gap rule" is a pointer to code, and the "development recon" route is unavailable (§6) | the gap controls, *if* the rule is a rule | **rewrite**: the round-39 containment rule applied to the frozen symlink table, stated in the claim |
| 9 | *(missing)* "publishes no path for an oracle escaping symlink" | yes (`escaping_ok`, exists at round 39) | "materialise the escaping link, record no gap" — **this control passes every other receipt clause** (the oracle holds only regular files, so an extra published path is invisible to `oracle_hits`) | **restore** |
| 10 | "subject digest equal to the carrier pin" | yes | C1-1 copied round-39 receipts | keep |
| 11 | "recomputes to its evidence id" | yes | nothing left after #12: the R39 fabricator re-mints the id by construction (`w2/R39W2C1Fabricate.md` §1.2: "self-consistent: it proves the receipt was hashed after writing") | **drop** — it is the only clause that needs `node` + `tools/round-27/xpin-attribute.mjs` at scoring time |
| 12 | "a fresh REA run … made by the counter itself at scoring time … yields the same semantic projection (projection fields fixed in the freeze)" | **only if enumerated** | C1-2 re-minted fabrication — *the only clause that can* | **keep + enumerate** (§C1-a) |
| 13 | "each carrier's superblock carries the AVM marker and its first metadata block length decodes as little-endian" | half: marker is exact; "decodes as little-endian" is *plausibility* on a vendor image (critic: the inode table spans more than one metadata block, so only `1380` vs `25605` separates the readings) | C1-3 marker-only body (LE identity fails there) and C1-4 marker-stripped body | **rewrite**: two-way parse test — under LE headers the inode table parses to `directory_table_start`, under BE headers the first read length is 25 605 (vendor member) / 29 696 (the 4 KiB lane-built AVM body) against `META_MAX = 8192` (`sqfs-list.py:87`), so the BE parse fails on the reader's own bound; one flag on a reader that already enforces it |
| 14 | "PROVINCE.md holds a `## Round-40 additions to Core` row naming the AVM layout that cites the round-40 knowledge entry, which cites a SOURCES row **opened this round** whose used-by lists it" | the row/entry/README/citation checks are enumerated; "opened this round" is **not** | nothing (the entry stem already forces a new entry) | **rewrite**: "a row whose id is absent from `corpus/SOURCES.md` at the freeze" — round-39 rows carry `opened 2026-10-26`, the same date as round 40, so the date cell cannot separate rounds (counter constant `OPENED = '2026-10-26'`, `c1-counter.py:97`) |
| 15 | "a round-40 frontier note supersedes the AVM part of the Frontier text" | yes (marker + stem) | duplicate authority (Frontier still claiming AVM after a Core row) | keep |
| 16 | "corpus/README.md maps the entry stem" | yes | — | keep |
| 17 | "no frozen C1 path changed after the freeze" | yes (exit 2) | freeze-drift | keep |
| 18 | "No REA run on V1/V2/L1/L2 before the freeze" | **impossible** | — | move out of the predicate into a process note: an unrun check is not a clause |
| 19 | *(missing, round-39 bindings)* xz leg, symlink coverage (≥2 in-tree, ≥2 escaping, ≥1 carrier with 2 in-tree), carriers-spec | yes | "four carriers that never exercise the gap rule or one compression leg" | **restore** (they are the non-vacuity of #1) |
| 20 | *(missing)* the new AVM-mode oracle reader is ungraded | — | — | **restore** a validation binding (§C1-a, §6.3) |

Draft clause 12 is the load-bearing one and the draft's own parenthetical already concedes the
limit ("cannot match unless it equals a real run"). Three consequences the freeze must pin:

- **C1-a (fatal as drafted).** A projection restricted to fields the oracle and symlink tables
  already determine is satisfied by the round-39 fabricator, which reads only `carriers.json`,
  `oracle.tsv` and `symlinks.tsv` (`w2/R39W2C1Fabricate.md` §1: 6/6, `met_target true`, no REA
  process). R39-CL5 would recur one level up. The field list must contain at least one value that
  is **not** a function of those two inputs. The cheap, run-stable candidates, measured on this
  extractor: `chunks[].offset`/`.size`, `normalized_result.coverage` (`partial`/`complete`),
  the `diagnostics[].report.kind` multiset and its count, `normalized_result.limitations`, and
  `normalized_result.engine.version`. Exclude everything run-identity: `output_directory`, the
  evidence id, PIDs, temp-dir suffixes, absolute paths.
- **C1-b.** Run stability is already evidenced, not assumed: K1–K4 receipts are byte-identical to
  the round-38 receipts "after normalising only run identity (paths, pids, evidence id)"
  (`w2/R39W2C1Fabricate.md` §2). A projection over the fields above is therefore reproducible by a
  fresh run; the counter will not flake.
- **C1-c.** The counter stops being a committed-bytes reader: it needs `npx` REA, `unblob`, and
  `sasquatch-v4be`, does 3–4 extractions at scoring time, and must use a fresh output dir
  (REA refuses an existing one) under `TMPDIR`/`--work`. Keep the closure's one-command property
  by committing the counter's own run as `corpus/evidence/round-40/c1/<id>/rerun.json` and having
  the receipt carry the projection equality — the closure then re-derives by comparing two
  committed JSONs, while the live extraction remains the scoring step.

## 3. P40-C2 clause ledger

| # | draft clause (abridged) | gradeable? | kills | verdict |
|---|---|---|---|---|
| 1 | "the frozen interpreter reads only the v2 table" | yes | oral-context shortcuts | keep |
| 2 | "assigns every held-out envelope the (label, action) pair its frozen generator assigned" | label yes; **action redundant** | see §4 | **drop `action`, grade labels** |
| 3 | "for all N held-out envelopes (2 per class)" | yes (`matched == N`) | — | keep, N=26 |
| 4 | "seed = the freeze commit hash" | yes (`manifest.seed`) | — | keep |
| 5 | "carriers regenerate byte-identically" | yes **only if** the counter actually regenerates in scratch | "hand-written manifest/envelopes" | keep as a graded binding, not prose |
| 6 | "subject digests equal carriers" | yes | — | keep |
| 7 | "manifest first added after the freeze and no later than its envelopes" | yes | table fitted to a pre-freeze manifest | keep |
| 8 | "the v2 table bytes equal the freeze bytes" | yes | post-hoc table edit | keep |
| 9 | "domain guard columns `operation` and `provider` (R39-CL1)" | yes, but 2 columns × 13 rows = 26 cells **and** a new "not this value" cell convention | out-of-domain envelopes | **rewrite**: one `domain: operation=extract_firmware provider.id=unblob` line under the marker — the routed defect asks for "the precondition that the prose table already states", and a precondition is one line, not 26 cells |
| 10 | "a `mixed-symlinks` row ahead of the escaping row (R39-CL2)" | yes | mixed envelopes mislabelled | keep |
| 11 | "body failure with published files, and a clean image with zero regular files (R39-CL3 D1/D2)" | yes — the draft's class list carries both but not the rows; the rows are what makes them decisions | measured outcomes excluded by `published files >0` | keep, and name the two new labels (`partial-body-failure`, `clean-empty`) |
| 12 | "a closed-vocabulary `action` column scored together with the label" | yes, but adds nothing over #2 | — | **drop** (§4) |
| 13 | "labels unique per row, so a label is a row decision" | yes (parse-level) | ambiguity between rows | keep as a table invariant |
| 14 | "held-out classes whose two replicates differ in a non-decision feature" | **no** — "non-decision feature" is not enumerated anywhere | nothing (the #15 binding already prevents inflation) | **drop** |
| 15 | "the counter reports the number of distinct row decisions" | as a *report*, nothing; as a *binding*, the anti-inflation gate R39-CL3 asked for | "26 envelopes over 12 decisions" | **rewrite** into a binding: `distinct_labels == 12` |
| 16 | "out-of-domain (a non-`extract-firmware` REA operation on a SquashFS carrier) → `unclassified`" | only if the envelope is **otherwise clean** | the v1-transcribed control | **rewrite**: two otherwise-clean envelopes (same chunks, gaps, no removal, files > 0) whose `operation` and `provider.id` are each varied away from the domain; else the interpreter's no-match fallback already prints `unclassified` and the guard is not forced |
| 17 | subject: "carriers regenerate … no later than its envelopes" | yes | — | keep |

**C2-a.** The `action` column is redundant by construction. With label cells pairwise distinct,
label ↔ matched row is a bijection, so an action cell read from that same row adds no decision —
it re-grades the label. The round-39 table's `cause -> action` column is already *documentation
only* (`sqfs-triage.py:31`), so a second, scored action column would be two conventions for the
same information inside one table. R39-CL3's real demand ("20 means 20 decisions") is met by
binding `distinct_labels`: 26 envelopes over 12 labels cannot be reported as 26 decisions.

**C2-b.** The out-of-domain envelope must be a frozen **transform** of a recorded clean envelope
(rewrite `operation`, or `provider.id`), not a second REA operation. A real `inspect_artifact` run
adds a new command path inside the frozen generator for zero discriminating power: the guard keys
on envelope fields, not on which operation really ran, and one variant class already kills the
v1-transcribed table because a clean carrier collides with the `clean` row.

**C2-c.** Two draft kill controls are not controls:
- "label-right/action-wrong" disappears with C2-a (no action column). Its role is taken by a
  **row-order** control: `mixed-symlinks` placed after the escaping row → mixed envelopes take
  `escaping-symlink-removed`.
- "best table + `*` default row" is **behaviour-preserving**: a trailing `unclassified` default
  row is semantically identical to the interpreter's fallback for every in-domain envelope (real
  rows match first). Drop it, or restate it as a *leading* `*` row, which mislabels everything.
- Add one that is cheap and real: loosen the `clean` row's `published files` cell to `*` → a
  clean-with-zero-files envelope takes `clean` instead of `clean-empty`.

**C2-d.** v1/v2 duplicate authority: leave block 18 byte-identical (round-39's frozen-bytes check
still holds at every current revision) and put one normative sentence **inside v2**: "for any
envelope the v2 table supersedes block 18; block 18 is retained as the round-39 demonstration".
One authority, no edit to a frozen surface.

## 4. Redundant pairs (delete the second)

| claim | redundant pair | keep | drop | why |
|---|---|---|---|---|
| C1 | "recomputes to its evidence id" ⊕ the scoring-time rerun | rerun | evidence id | the id proves only "hashed after writing" (`R39W2C1Fabricate` §1.2); it costs `node` + `xpin` |
| C1 | handler/`no failed chunk` receipt clauses ⊕ the same fields in the projection | receipt clauses | — | not deletable: they are diagnostics that work when REA is unavailable; state that redundancy is deliberate |
| C1 | "oracle publishes every regular file" ⊕ "gaps only as allowed" | both | — | different outcomes (missing file vs wrong gap); round-39's partial-body class shows they diverge |
| C2 | scored `action` column ⊕ distinct labels | labels | action | §C2-a |
| C2 | "replicates differ in a non-decision feature" ⊕ `distinct_labels` binding | binding | replicates clause | the binding is checkable, the clause is not |
| C2 | scored action ⊕ `cause -> action` prose column | prose (documentation) | scored action | one convention per fact |

## 5. Universal / unenumerated wording (§6 item 9)

Clauses that read like checks but that no counter field enumerates:

1. **C1** "(unblob 26.6.4, sasquatch-v4be 4.5.1 on the child PATH)" — "all" versions, none read.
2. **C1** "carries only the extraction gaps the frozen gap rule allows" — "the rule" is a pointer;
   the full set is the in-tree link set, and it is not the sentence.
3. **C1** "yields the same semantic projection (projection fields fixed in the freeze)" — a
   universal over an unspecified field set; the freeze must list the fields literally.
4. **C1** "each carrier's … first metadata block length decodes as little-endian" — "decodes"
   without a test; on vendor images only plausibility separates the readings.
5. **C1** "genuine AVM layout" — the adjective does the work of clause 13; drop the adjective once
   the test is stated.
6. **C1** "a SOURCES row opened this round" — the only enumeration is a date that round 39 shares.
7. **C1** "No REA run on V1/V2/L1/L2 before the freeze" — unobservable.
8. **C2** "the (label, action) pair" — the action vocabulary is never listed (and is redundant).
9. **C2** "held-out classes whose two replicates differ in a non-decision feature" — "non-decision
   feature" is not enumerated; no check can tell a decision from a non-decision feature.
10. **C2** "the counter reports the number of distinct row decisions" — a report is not a check.
11. **C2** "out-of-domain envelopes must be `unclassified`" — true of the fallback too, so the
    class only bites if "otherwise clean" is added.

Kept universals that *are* enumerated (allowed under §6 item 9): "every regular file of the
oracle" (one row per file), "no failed chunk" (the chunk list), "every held-out envelope" (N),
"labels unique per row" (table parse), "no frozen C1 path changed" (`FROZEN_PATHS` + carriers).

## 6. Is a 4-carrier C1 target sized to one round?

**Effort: yes. Risk allocation: no.** Two findings decide it.

### 6.1 A second AVM-BE vendor image exists (probe, this round)

`python3 -I -B probe-avm-members.py <image>` (artifact `probe-avm-members.out`, exit 0; tar member
bytes only — no extractor):

| model / version | image | image sha256 | `./var/remote/var/tmp/filesystem.image` |
|---|---|---|---|
| 6490 Cable 07.57 (V1) | 39 741 440 B | `f518ce6b…ede6d` (lane pin) | **BE** `sqsh`, comp 4, v4.0, mkfs 5 442 392 == bytes_used, member 5 443 592 B, sha `334e56df…f3d4` (round-39 scout artifact) |
| **6590 Cable 07.57** | 39 290 880 B | `0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae` | **BE** `sqsh`, comp 4, v4.0, mkfs 5 441 468 == bytes_used, member **5 443 592 B**, inode_count 1079, frag_count 112, inode_table 5 420 540, dir_table 5 429 114, sha `65e85647f0199f9dcbb3f06674557bfda2fc9a4412378448b572478d2bff832a` |
| 6591 Cable 08.25 | 61 460 480 B | `fab055fb…a32d7` | no `filesystem.image` member (`var/*` only) |
| 6660 Cable 08.25 | 61 132 800 B | `4d96c365…9fd82` | no `filesystem.image` member |
| 6430 Cable | — | — | `other/fritz.os/` → 404 |

So V2 is *available* (6590), but the candidate is the **same rescue filesystem re-stamped**: the
BE member is byte-for-byte the same size as V1's, both firmwares are FRITZ!OS 07.57 on the same
x86 platform, and only the superblock timestamp differs (924 s apart). `[INFERENCE]` the tree is
identical (busybox-applet hardlinks explain the 2 942 published paths over 1 079 inodes); the four
scalars above are the cheap check the freeze should run before calling 6590 a second carrier.

### 6.2 The draft's own de-risking clause has no image left

The draft fixes the gap rule "from development recon, never from carrier runs" and says "recon
runs on a separate development vendor image". With V1 = 6490 and V2 = 6590 there is **no third
AVM-BE image** among the probed catalogue (§6.1). The clause is unimplementable, and it is the
clause covering C1's largest unknown: a vendor rescue filesystem carries hundreds of links, in
classes round 39 never froze (absolute, directory, chained) plus non-regular entries (device
nodes, FIFOs) whose gap behaviour is untested. The round-39 rule sentence explicitly scoped
itself to "relative file targets only".

### 6.3 Recommendation

**Target 3, not 4.** `N = 3`: V1 (6490-carved AVM-BE member, vendor provenance, xz), L1
(lane-built AVM layout, gzip), L2 (lane-built AVM layout, xz). Spend 6590 as the **development
image**: it validates the AVM-mode reader on real vendor bytes and measures the vendor link
population *before* the freeze, which is exactly what the draft's "development recon" clause
wanted. A fourth carrier buys no new control kill and consumes the only development specimen.

If the lane insists on 4, the freeze must first (a) find a third AVM-BE image for recon (probe
other x86 cable models; the 08.25 line has none), and (b) state the gap rule over all four link
classes, not just the one class round 39 exercised.

## 7. Is the 13-class C2 set sized to what recon can make deterministic?

**Yes — at 12 decisions, with three conditions.** Each new class traces to a measured development
outcome, so no label is invented:

| new class (round 40) | measured outcome it rests on | generator cost |
|---|---|---|
| `clean-empty` | `w2/R39W2C2TableReview.md` D2 (`full-be-dirempty-gzip`, clean, P=0) | recipe flag `files=0` (dir-only tree) |
| `partial-body-failure` (P>0) | same report D1 (`full-be1-xz` damaged, P>0) | new `CORRUPTIONS` recipe that damages a data block only |
| `mixed-symlinks` | K5/K6 (2 of 6 round-39 Core carriers) | recipe `symlinks=('in-tree','escaping')` |
| `out-of-domain` | R39-CL1 (`w2/R39W2C2AxisFit.md` C2) | envelope transform (§C2-b), not a second REA operation |

Replicate count: 26 REA `extract-firmware` runs post-freeze on ~5 KB images (round-39 classes run
1–7 s each) — cheap. The draft correctly drops `version-minor-mismatch` (it shares
`body-extractor-failure`'s label); keep its recipe as that class's second replicate so the label
is still exercised by two damage recipes.

**12, not 13.** `clean-be` and `clean-le` share the `clean` label; the 13 classes produce 12
distinct labels. A target that says "13 decisions" is unachievable by construction; a target that
says "26 matched" is inflatable by one duplicate replicate. `distinct_labels == 12` is both
achievable and non-inflatable, and it is the exact binding R39-CL3 asked for.

## 8. Shortest predicates that keep every kill control red

### P40-C1 (proposed)

> At the measured revision, for each of the N = 3 frozen carriers in
> `.ufo/waves/round-40/c1/carriers.json` (V1 the AVM-BE member carved from the 6490 image, L1 and
> L2 lane-built AVM-layout images in gzip and xz), the carrier hashes to its frozen pin; the
> committed after-receipt, first added in a commit descended from the freeze, is an
> `operation = extract_firmware`, `provider.id = unblob` envelope whose subject sha256 is the pin,
> whose only squashfs chunk is `squashfs_v4_be` with `extraction_failed` false, whose recorded
> sasquatch command carries no `-be`, which publishes each oracle regular-file row at the same
> relative-path suffix with the same sha256, publishes no path for an oracle escaping symlink, and
> whose gaps are exactly one `unpublished-entry` per in-tree symlink of the frozen symlink table
> and none other; a REA run the counter makes at scoring time into a fresh scratch directory
> reproduces the receipt's projection over the frozen field list (chunk offset/size/handler,
> published-path set, gap (kind, path) multiset, diagnostics report kinds and count, coverage,
> engine version), and the counter commits that run as `rerun.json` beside the receipt; each
> carrier parses under little-endian metadata block-length headers and does not under big-endian,
> and each vendor carrier's superblock is `sqsh`, version 4.0, `mkfs_time == bytes_used`; the
> AVM-mode oracle reader reproduces the six round-39 oracle tables on K1–K6; PROVINCE.md holds the
> `## Round-40 additions to Core` row citing the round-40 entry, the entry cites a SOURCES row
> whose id is absent from `corpus/SOURCES.md` at the freeze and whose used-by lists the entry, a
> round-40 frontier note supersedes the AVM Frontier text, corpus/README.md maps the entry stem,
> at least one carrier exercises each of the gzip and xz legs and the frozen symlink-coverage
> minimum holds, and no frozen C1 path changed after the freeze.
>
> **Target:** `carriers_matched == 3` and the counter's frozen binding list all true.

### P40-C2 (proposed)

> At the measured revision, `tools/round-40/sqfs-triage-v2.py` reads only
> `SKILL.md`'s `<!-- sqfs-triage-table v2 -->` block — whose `domain:` line is
> `operation=extract_firmware provider.id=unblob` and whose label cells are pairwise distinct — and
> assigns every held-out envelope the label its frozen generator recipe fixed before any REA run,
> for all N = 26 envelopes (13 classes × 2: clean-be, clean-le, clean-empty,
> escaping-symlink-removed, in-tree-symlink-metadata, mixed-symlinks, dep-missing-be,
> dep-missing-le, avm-marker-be-dropped, body-extractor-failure, partial-body-failure,
> no-squashfs-chunk, out-of-domain), where each out-of-domain envelope is an otherwise-clean
> SquashFS envelope whose `operation` or `provider.id` is varied away from the domain and whose
> expected label is `unclassified`; `distinct_labels == 12`; every carrier regenerates
> byte-identically from the frozen generator with seed = the freeze commit hash; every envelope's
> subject digest is its carrier pin; the manifest is first added after the freeze and no later than
> its envelopes; and the v2 block bytes at the measured revision equal the freeze bytes.
>
> **Target:** `matched == N`, `distinct_labels == 12`, and the counter's frozen binding list all
> true.

### 8.1 Kill-control closure matrix (every control stays red)

| control | single clause that kills it |
|---|---|
| C1 do-nothing | `receipt_present` → `carriers_matched 0` |
| C1 round-39 receipts copied | `subject_pin_ok` (different carrier) and the projection's published-path set |
| C1 fabricated from the oracle, id re-minted | the projection **only if** it carries a non-oracle field (coverage / chunk offset / diagnostics kinds / limitations) — §C1-a |
| C1 marker-only standard-BE receipt relabelled | two-way parse test: the body parses under BE too, so the LE-parse-and-BE-fail binding fails; and its real extraction publishes 0 files |
| C1 genuine AVM with the marker stripped | `mkfs_time == bytes_used` fails; extraction with `-be` publishes 0 files |
| C1 receipts added in the freeze commit | `receipt_first_add != freeze` |
| C1 escaping link materialised, no gap | restored escaping clause (and the projection's path set) |
| C2 base SKILL, no v2 block | interpreter exit 2 → counter exit 2, never `met` |
| C2 v1 transcribed with `*` domain cells | out-of-domain class: expected `unclassified`, a clean carrier otherwise takes `clean` |
| C2 catch-all row | labels wrong on the 11 in-domain classes |
| C2 mixed row placed after escaping | mixed envelopes take `escaping-symlink-removed` |
| C2 `clean` row's file cell loosened to `*` | clean-empty takes `clean` instead of `clean-empty` |
| C2 missing clean-empty row | clean-empty falls through (`>0` fails on every row) to `unclassified` |
| C2 26 envelopes reported as 26 decisions | `distinct_labels == 12` |
| *(dropped)* best-table + `*` default row | behaviour-preserving — not a control (§C2-c) |
| *(dropped)* label-right/action-wrong | no action column (§C2-a) |

## 9. Defects routed to the freeze (apply before the freeze commit)

1. **C1: enumerate the rerun projection and include ≥1 non-oracle field** (D-C1-a). Without it the
   named R39-CL5 control passes and the round-39 defect recurs.
2. **C1: drop `evidence_id_ok`**; keep the rerun as the fabrication gate, commit `rerun.json`.
3. **C1: make the tool pin executable** (exit 2 unless `unblob --version` = 26.6.4) or mark it not
   graded.
4. **C1: state the gap rule** (one `unpublished-entry` per in-tree link; none other; no published
   escaping path) over all four link classes, and drop "from development recon".
5. **C1: restore the escaping-symlink clause.**
6. **C1: replace "first metadata block length decodes LE" with the two-way parse test.**
7. **C1: replace "opened this round" with "row id absent at the freeze".**
8. **C1: carrier set N = 3** (V1 + L1 + L2); 6590 becomes the development image; state the
   symlink-coverage and xz-leg bindings and the reader-validation binding on K1–K6.
9. **C1: move "no REA before the freeze" out of the predicate** into a process note.
10. **C2: drop the scored action column**; bind `distinct_labels == 12`.
11. **C2: replace the two domain columns with one `domain:` line** under the marker.
12. **C2: pin out-of-domain to otherwise-clean envelopes and a frozen field transform.**
13. **C2: drop "replicates differ in a non-decision feature"; drop the trailing-`*` default
    control; replace label-right/action-wrong with a row-order control; add the loosened-`clean`
    control.**
14. **C2: add one sentence to v2 making it the sole authority over block 18** (no edit to block
    18, which stays byte-identical for round-39's frozen check).

## 10. Tradeoffs and what I did not decide

- Dropping `evidence_id_ok` leaves the committed receipt's internal coherence ungraded. The
  rerun's committed `rerun.json` restores it at a coarser grain; the closure can spot-check the id
  once. Accepted because the id check is the only scoring-time `node` dependency.
- The one-line `domain:` guard is less visible to a reader scanning rows than two columns. It is
  also not editable per row, which is the point: the domain is a property of the operation, not of
  an outcome row.
- `N = 3` trades a second vendor image for a validated gap rule and a validated reader on real
  vendor bytes. If the operator wants vendor breadth *and* recon, a third AVM-BE image must be
  found first; the probed 08.25 line has no `filesystem.image` member at all.
- I did not evaluate whether R40-C1/R40-C2 land (no data exists); every sizing statement is about
  clause structure and availability, not about extraction.

## 11. Evidence

Artifacts (this directory):
- `probe-avm-members.py` — reproducible member probe (tar member bytes, no extractor).
- `probe-avm-members.out` — probe run `2026-10-26T18:30:06Z`, exit 0, plus the four listing
  probes; 6590 numbers as in §6.1.
- `avm-model-index.out` — 70 model slugs from `https://download.avm.de/fritzbox/` (HTTP 200,
  8 990 B).

Read-only commands whose output the report quotes:
```
python3 -I -B .ufo/waves/round-40/w1/artifacts/R40SimplifyPlan/probe-avm-members.py fw6590.image \
  fritzbox-6591-cable.image fritzbox-6660-cable.image            # exit 0
sha256sum fw6590.image   # 0c539499044a807c2dfa3ffdf5eafe6016096912fa6e13374f48afa46cd0abae
```
Lane reads (git objects only): `tools/round-39/{c1-counter,c2-counter,sqfs-triage,heldout-gen,
sqfs-list}.py`, `plans/round-39-claims.md`, `corpus/lessons/round-39-verifier-spotcheck.md`,
`.ufo/waves/round-39/w2/R39W2C1Fabricate.md`, `.ufo/waves/round-39/w1/R39AssimAvmCritic.md` and
its `matrix.tsv`, `SKILL.md:300-347`, `PROVINCE.md:370-384`, `corpus/README.md:89-93,242-245`,
`corpus/SOURCES.md:5` (column order: `opened` = cell 8, `used-by` = cell 10).

Disclosure: the 6590 member superblock and sha were read by my probe. If the lane designates 6590
as V2, that is a pre-freeze byte read of a would-be carrier (no extractor was run); under my
recommendation 6590 is the development image, which makes the read the intended recon.

Scratch `/fast/scratch/hyaku/kaidoku-r40/R40SimplifyPlan` (four downloaded images, ~200 MB) was
removed at exit; no scratch path is cited as evidence. No installs, no upgrades, no pacman.
