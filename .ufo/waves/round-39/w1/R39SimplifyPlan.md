# R39SimplifyPlan — minimality review of the round-39 DRAFT predicates

**Verdict: DEFECTS FOUND** — 6 predicate-level defects (2 of them make a clause false-by-construction or
unenforceable), 7 clauses droppable without letting a listed control through, 4 guards missing against
degenerate greens, and 3 kill controls missing for clauses the draft keeps or for degenerate tables.

Seat: leaf simplifier, round 39 wave 1 (pre-freeze). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `a2f64e1da78afcf8cc39287106604dbcc270844c`. I wrote no lane file outside this report and
`.ufo/waves/round-39/w1/artifacts/R39SimplifyPlan/`, ran no REA, built no carrier, edited nothing.

## 1. Method and its limits

The draft's counters do not exist (`ls tools/round-39/` → `No such file or directory`;
`.ufo/waves/round-39/c1/` → absent), so "could be dropped without letting a control through" cannot be
executed. I judged each clause against three things instead:

1. the draft's own frozen kill list (the controls the predicate must keep red);
2. the shape round 38 actually implemented (`tools/round-38/c1-counter.py`: 12 per-carrier flags,
   6 registry bindings, `met_target = carriers_unchanged and carriers_matched == TARGET and bind_ok`);
3. the producer code the signals come from — unblob 26.6.4 handler/sanitiser and rea-agents 6.5.0 gap
   derivation — plus the committed receipts those producers wrote.

**Limit, stated plainly:** (3) proves what a clause *can* observe, not what a not-yet-written counter
*does* observe. Under §6 item 9 the predicate sentence and the counter condition must be the same thing;
every "KEEP+" below is therefore a demand on the counter, not an established fact about it. No claim here
rests on a run of a round-39 instrument.

Evidence files (all generated this seat, from committed bytes and installed packages):

- `artifacts/R39SimplifyPlan/evidence-code.txt` — exact lines from unblob + rea-agents.
- `artifacts/R39SimplifyPlan/evidence-envelopes.txt` — receipt fields for K1–K4, the round-36 LE
  before-arm, and the round-38 AVM probe.
- `artifacts/R39SimplifyPlan/determinism.txt` — generator byte-determinism transcript.
- `artifacts/R39SimplifyPlan/minimality-table.md` — clause × control × risk table (the working document;
  this report carries the findings and the freeze-ready sentences).

## 2. Defects

### D1 — the gap clause is false by construction on any carrier with an in-tree link

Draft text: "carries extraction gaps of kind `unpublished-entry` exactly on the frozen oracle's in-tree
symlinks". The envelope does not print image-root-relative paths. K2's committed round-38 receipt:

```
extraction_gaps: [('unpublished-entry', 'firmware.bin_extract/var/lib/run-link', None, [])]
files:           ['firmware.bin_extract/a/run.sh', 'firmware.bin_extract/space name.txt', ...]
oracle.tsv:      a/run.sh <sha> 22 | space name.txt <sha> 21 | var/lib/data.bin <sha> 10240
```

The regular-file clause already carries the fix ("same relative-path suffix"); the gap clause does not, and
"exactly on" against image-root-relative rows would be red on the one carrier in the set that has an
in-tree link. Fix: give the gap clause the same suffix rule as the file clause.

### D2 — the gap subject set is in-tree *non-regular entries*, not symlinks

rea-agents 6.5.0 `unpublished_entries[].kind` is `z.enum(["symlink", "special"])`
(`dist/domain/firmware/firmwareAnalysis.js:139`) and every such entry becomes an `unpublished-entry` gap.
A carrier that carries a FIFO or device node is "correct" under the rule and red under the draft's
wording. Fix: name the subject "in-tree non-regular entry", and freeze the K5/K6 trees free of special
files (a generator constraint, guard g3).

### D3 — "no frozen C1 path changed after the freeze" is an unenumerated universal

§6 item 9: no "all/every/no" unless the counting command enumerates the full set. "Frozen C1 path" names
no set; the counter therefore cannot be the same condition as the sentence. The machinery already exists
and must simply be named: `tools/round-38/freeze-drift.py` takes explicit paths or a default set and
returns the commits in `FREEZE..REV` (`freeze-drift.py:1-27`). Fix: name the set in the predicate.

### D4 — C2's class list carries a conditional into the freeze

"`+ no-squashfs-chunk` if recon shows it distinct" is a predicate that cannot be frozen as written, and
the class itself is out of scope: an envelope with no squashfs chunk is not "an REA `extract-firmware`
outcome on a SquashFS v4 input" — the input is not SquashFS. Fix: freeze the class list literally and
drop `no-squashfs-chunk`; the six producer gap kinds plus "no gap" already enumerate the in-scope space.

### D5 — C2's "assigned before any REA run" is unobservable, and it is the claim's deepest hole

No committed byte can show that the label set was written before the envelopes were read. Every listed C2
control (catch-all, gap-count-only, gap-kind-only, round-36 transcription) can be greened by a label set
edited after inspection. The ordering clause and the manifest-ancestry clause are both proxies for the
same unobservable. Fix: replace the proxy with a re-derivation — the counter runs the frozen
`heldout-gen.py` at the seed and requires *its* emitted labels to equal the manifest's. Then the label set
is a function of frozen bytes plus the freeze hash, and "before any REA run" stops being load-bearing.

### D6 — both targets end in a tautology, and C2's `N` is unbound

- C1: "`carriers_matched == 6` and every binding true (`met_target`)". `met_target` is the counter's own
  conjunction over its own flags; round-36 limit 9 already records receipts where `met_target` and
  `matched` disagreed. State the count, let the receipt enumerate bindings.
- C2: "`matched == N`" with `N` introduced only as "for all N held-out carriers (2 per class)". A
  predicate must be self-contained; the count comes from the manifest.

## 3. Droppable clauses (no listed control is lost)

| cut | text removed | why it adds risk without discrimination |
|---|---|---|
| 1 | "rea-agents 6.5.0" at the parenthetical | the later clause "recomputes to its stored evidence id under the rea-agents 6.5.0 rule" *is* that version binding; naming it twice adds a second place to keep in sync |
| 2 | "`sasquatch-v4be` 4.5.1 reachable on the child PATH" | unobservable: `environment` is `null` in all four committed receipts; and every failure it could catch already surfaces as `extraction_failed: true` **plus** a non-`unpublished-entry` gap — measured on the round-36 before-arm (`extraction_failed: True`, `missing-extractor-dependency`, `dependencies: ["sasquatch"]`) |
| 3 | "with no failed chunk" | fully redundant with the exact-gap clause, by producer code: `chunkGaps("extractor-failure", (chunk) => chunk.extraction_failed === true && chunk.handler !== null && chunk.encrypted !== true && !dependencyChunkKeys…)` (`dist/cli-runtime/cli.js:14271`). A failed squashfs chunk always yields `extractor-failure`, `missing-extractor-dependency`, `encrypted-chunk` or `unknown-chunk-handler` — never silence |
| 4 | "and no other gap" | "exactly on X" is already set equality in both directions; the tail invites a counter that implements the weaker subset reading |
| 5 | "a round-39 frontier note supersedes the big-endian part of the Frontier bullet" (as a scored binding) | round-38's implementation is `'big-endian' in l and 'superseded' in l` (`tools/round-38/c1-counter.py:208-209`) — a do-nothing lane satisfies it with one prose line. It cannot be made discriminating; keep it as a work requirement the closure spot-checks, not as a receipt binding |
| 6 | "`+ no-squashfs-chunk` if recon shows it distinct" | see D4 |
| 7 | "each row source-cited" (C2 surface text) | to score it C2 must read `corpus/SOURCES.md`, which breaks C2's own separability clause; C1 already carries the round's sourced claim (§2b item 4) |

Not cut, though they read like padding — each has a listed control behind it:

- "first added in a commit that descends from the freeze": the only structural discriminator for a K1–K4
  receipt whose bytes were carried over from before the freeze. Note the control as drafted (K1–K4 copies,
  K5/K6 absent) is already red on the count; keep the clause for the *pre-freeze* variant and say so.
- "publishes no path for the oracle's escaping symlinks": no listed control, but without it the symlink
  rule is half-enforced — materialising an *escaping* link leaves the gap set exact, so every other clause
  greens on a wrong rule. Keep it and add its control (K6 below).
- "`corpus/README.md` holds a coverage-map row": cheap structural row test, and the lane's existing
  coverage-accounting convention. It duplicates the Core row's assertion in a second document, but the two
  documents have different authority (PROVINCE = province, README = corpus index) — convention, not a
  second convention.

## 4. Guards the draft lacks (degenerate passes)

| id | degenerate pass it closes |
|---|---|
| g1 | empty `symlinks.tsv` on all six carriers + carriers built without links → the gap clause greens vacuously. Require ≥1 in-tree and ≥1 escaping link across the frozen tables. (Round-38 carried the sibling guard `oracle_files > 0`, `c1-counter.py:186`.) |
| g2 | an empty oracle table on a carrier → the file clause is trivially true. Keep round-38's `oracle_files > 0`. |
| g3 | K5/K6 trees containing a symlink chain, an empty-target link, or a special file. unblob resolves with the real filesystem (`extractor.py:50-92`), unlinks an empty target **silently** (`extractor.py:67-70` — no report, so no diagnostic and no gap), and REA records `special` entries as gaps; the oracle classifies by POSIX path arithmetic. Any of the three makes a correct run red. Freeze the constraint. |
| g4 | a C2 manifest with 1 envelope per class → a lucky or label-echoing table greens. Require ≥2 per frozen class. |

## 5. Kill-rule additions

| id | control | must be red because |
|---|---|---|
| K6 (C1) | the escaping link published as a file in `files[]`, gap set left exact | only the escaping-publication clause sees it (see §3) |
| K7 (C1) | empty symlink tables on all six carriers | guard g1 |
| K8 (C2) | a table keying on `diagnostics[].report.__typename__` alone | the two dependency classes share one report class: `Command.extract` raises `ExtractorDependencyNotFoundReport` for *any* missing executable (`extractors/command.py:69-72`), so the typename cannot split `dep-missing-be` from `dep-missing-le` |

K7 and K8 are cheap: K7 is one fixture manifest; K8 is a two-row table.

## 6. Proposed predicate sentences (freeze-ready)

Both are single sentences in the draft's register. Word counts measured on the extracted draft text
(`plans/round-39-claims.md`, 169 and 102 words) versus these (161 and 101) — the reduction is small on
purpose: C1's surplus was five clauses worth ~40 words (§3 cuts 1–5), spent back on two guards, and its
real problem was correctness, not length. A guard against a degenerate green buys more than eight words
cost, so the shortest sentence that keeps every control red is not the shortest sentence that parses.

### P39-C1

> At the measured revision, for each carrier in the frozen `.ufo/waves/round-39/c1/carriers.json` (six
> standard big-endian SquashFS v4 images), the round-39 after-receipt it names (unblob 26.6.4) is the
> single commit that added it after the freeze, and carries the frozen carrier's subject sha256, the
> `squashfs_v4_be` handler, every frozen oracle row (relative-path suffix and sha256), and
> `unpublished-entry` gaps whose relative-path suffixes are exactly the frozen table's in-tree non-regular
> entries, publishing no path for its escaping ones; and it recomputes to its stored evidence id under the
> rea-agents 6.5.0 rule. `PROVINCE.md` holds a `## Round-39 additions to Core` row naming `squashfs_v4_be`
> and citing the round-39 knowledge entry, which cites a `SOURCES.md` row opened on the freeze commit's
> date whose used-by lists that entry; `corpus/README.md` holds a coverage-map row naming the entry stem;
> and no freeze-drift path has a commit in freeze..rev. Target: `carriers_matched == 6`; guards: every
> oracle table is non-empty, and the six symlink tables carry at least one in-tree and one escaping link.

Changes from the draft: dropped the `rea-agents 6.5.0` mention at the parenthetical, the
`sasquatch-v4be`/PATH clause, "with no failed chunk", "and no other gap", and the frontier-note binding;
added the suffix rule to the gap clause, "non-regular entries", the derived `opened` date, the
enumerated freeze-drift set, and two guards. "Every"/"exactly"/"no frozen path" now each name an
enumerated set (oracle rows per carrier; the frozen symlink table; the freeze-drift path list).

Two fields the frozen `carriers.json` must carry for this sentence to be checkable: the `after` receipt
path per carrier and the `symlinks` table path per carrier (round-38's manifest already carries `path`
and `oracle`; `symlinks` is new in round 39). Without them "the after-receipt it names" is undefined.

### P39-C2

> At the measured revision, for every envelope in the frozen held-out manifest, the frozen
> `tools/round-39/sqfs-triage.py`, given only the `SKILL.md` `## Queue-drain craft` table bytes and the
> envelope, returns the manifest's label; the frozen `tools/round-39/heldout-gen.py` at seed = the freeze
> commit hash re-emits those carriers byte-for-byte and those labels; each envelope's subject sha256
> equals its carrier's; the manifest's adding commit is a descendant of the freeze and an ancestor-or-equal
> of every envelope's adding commit; and the table bytes at the measured revision equal those at the
> freeze. Target: `matched == the manifest's envelope count`; guard: at least 2 envelopes per frozen class.

Changes from the draft: "reading only" → an invocation contract; "assigned before any REA run" → a
re-derivation by the frozen generator; "for all N (2 per class)" → "every envelope in the manifest" plus a
manifest guard; the conditional class dropped; `matched == N` → `matched == the manifest's envelope count`.
Every universal now names an enumerated set (the manifest's envelopes, the generator's emitted labels, the
table bytes).

### §6 item 9 audit — every universal word in the draft, and what enumerates it

| draft words | enumerated by | §6 status |
|---|---|---|
| C1 "publishes every regular file of the frozen independent oracle" | the frozen `oracle.tsv` rows, per carrier | compliant |
| C1 "exactly on … in-tree symlinks and no other gap" | the frozen `symlinks.tsv` rows (both directions) **plus** every gap in the envelope | compliant only with guard g1 (an empty table makes the universal vacuous) |
| C1 "publishes no path for the oracle's escaping symlinks" | the table's `escaping` rows | compliant only with guard g1 |
| C1 "no frozen C1 path changed after the freeze" | **nothing named** | **violation — D3** |
| C1 "every binding true" | the counter's own flag | tautology, not a set — D6 |
| C2 "every held-out envelope … for all N held-out carriers" | the manifest, but `N` is never bound to it in the sentence | **violation — D6** |
| C2 "every carrier regenerates byte-identically" | the manifest's carriers | compliant |
| C2 "every envelope's subject digest" | the manifest's envelopes | compliant |
| C2 "each row source-cited" (surface text, not predicate) | the table's rows — but scoring it would make C2 read `SOURCES.md` | cut (§3 cut 7) |

## 7. Every listed control stays red under the proposed sentences

C1 — with the receipt fields above, not by argument:

| control | red because |
|---|---|
| CTL do-nothing at base | 0 ≠ 6; no Core row, no entry, no README row |
| CTL round-38 receipts copied to the round-39 paths, K5/K6 absent | 4 ≠ 6 |
| CTL fabricated receipt | the evidence-id recompute (`xpin-attribute.mjs`, the rea-agents 6.5.0 rule). **Scope it to the patched-without-recompute class**: round-36 limit 9 records that a fabrication rebuilt from the oracle and re-hashed with REA's own digest code still recomputes — that class is caught only by the added-once-after-freeze clause, and must be disclosed as a limit, not listed as a kill |
| CTL materialise the symlink, no gap | set equality: an in-tree entry with no gap |
| CTL wrong gap kind | the kind clause |
| CTL escaping symlink kept as a gap | set equality: a gap that is not in the table |
| K6 escaping link published as a file | the escaping-publication clause |
| K7 empty symlink tables | guard g1 |

C2:

| control | red because |
|---|---|
| do-nothing at base | no table, no interpreter |
| catch-all table | ≥2 classes, ≥2 envelopes each |
| gap-count-only table | `clean` and `escaping-symlink-removed` both have 0 gaps (K1 is the committed witness: `gaps: []`, `diagnostics: ['MaliciousSymlinkRemoved']`); the two dependency classes both have 1 |
| gap-kind-only table | `dep-missing-be`/`dep-missing-le` share `missing-extractor-dependency` and differ only in `dependencies` |
| round-36 table transcribed | no BE row, no dependency-name split, no AVM row |
| K8 typename-only table | both dependency classes share `ExtractorDependencyNotFoundReport` |

The held-out classes are separable in the fields the producer actually writes — evidence, not inference:

| class | distinctive field |
|---|---|
| `clean` | 1 chunk, `extraction_failed: false`, gaps `[]`, diagnostics `[]` (K3/K4 receipts) |
| `escaping-symlink-removed` | gaps `[]` **and** `diagnostics[].report.__typename__ == MaliciousSymlinkRemoved` (K1 receipt; its `target` resolves one level above the image root) |
| `in-tree-symlink-metadata` | exactly one `unpublished-entry` gap, path suffix = the table's in-tree entry, `unpublished_entries[].kind == symlink` (K2 receipt) |
| `dep-missing-be` / `dep-missing-le` | one `missing-extractor-dependency` gap whose `dependencies` names the endianness-appropriate executable |
| `avm-marker-be-dropped` | `extraction_failed: true` + one `extractor-failure` gap + `ExtractCommandFailedReport` stderr "…suggests a SquashFS image of a different endianess… FATAL ERROR: File system corruption detected" (round-38 AVM probe) |
| `body-extractor-failure` | same chunk/gap shape as the AVM row — separable **only** by stderr |

That last row is a requirement on the held-out generator, not a formality: if the body-damage carrier's
stderr also matches the AVM phrase, the two labels collapse and a gap-kind-only table meets the target on
them. Both stderr texts must be committed as recon evidence before the freeze.

## 8. Checked and found sound (no change proposed)

- **C2's regeneration clause is freezable.** `tools/round-37/gen-squashfs.py` writes the constant
  `MKFS_TIME = 1700000000` into every inode (`:14`, and at `:105,:114,:155`), and no `stat()`/`st_mtime`/
  `utime()` call exists in the file, so SquashFS inode mtimes are not wall-clock. Measured: identical bytes
  for repeated runs over one source tree, in the same second and 3 s apart, for `--comp gzip` and
  `--comp xz` (`determinism.txt`). The step from same-tree to fresh-tree rests on the constant and the
  absence of `stat()` — code, not measurement — [INFERENCE] for trees created at a different time. This
  was the draft's most likely silent freeze-killer; it is not one — provided `heldout-gen.py` writes the
  trees itself and does not shell out to `tar`/`cp`, which would reintroduce `stat()` mtimes.
- **The two dependency classes exist and are distinguishable.** unblob's CLI preflight lists both binaries
  (`handlers/filesystem/squashfs.py:68-69`), but the failure report names one: `Command.get_dependencies`
  returns `[self._executable]` (`extractors/command.py:101-102`) and is raised only on `FileNotFoundError`
  of the executable it invoked (`:69-72`). The endianness chooses it at `squashfs.py:37-44`.
- **"Escaping symlink → removed, no gap" is measured, not assumed.** K1's receipt: `extraction_gaps: []`,
  `unpublished_entries: []`, `files[]` without `link-to-hello`, diagnostics `MaliciousSymlinkRemoved` with
  `target` = `…/extracted/hello.txt` (one level above the image root `…/extracted/firmware.bin_extract`).
  The draft's rule matches the producer.
- **The AVM marker is a code fact**, not a vendor rumour: `is_avm = header.bytes_used == header.mkfs_time`
  and in that branch `-be` is omitted (`squashfs.py:46-50`); the round-38 probe's patched carrier
  reproduces the drop with exit 1 and `published_bytes: 0`.

## 9. Residual risk after the proposed changes

1. **Receipt provenance vs a re-hashed fabrication** (C1) — unsolvable inside the counter; disclosed as a
   limit, carried by the four/six independent reproductions instead.
2. **C1's symlink classification** — the oracle uses POSIX path arithmetic; unblob uses `Path.resolve()`
   plus `is_safe_path`. Guards g3 remove the known divergences (chains, empty targets); a future carrier
   with a chain would need a rule, not a reworded predicate.
3. **C2's AVM/body separation** — rests on free-text stderr; a sasquatch message change moves the class.
   The table row must cite the message it matches, and the recon must commit both texts.

## 10. Evidence index (commands run by this seat)

| command | exit | output |
|---|---|---|
| `ls tools/round-39/` / `ls .ufo/waves/round-39/c1/` | 2 | both absent — no counter exists to execute |
| `python3 …` dump of `corpus/evidence/round-38/c1/K*/after.json` fields | 0 | `artifacts/R39SimplifyPlan/evidence-envelopes.txt` |
| `grep -n` over unblob 26.6.4 + rea-agents 6.5.0 sources | 0 | `artifacts/R39SimplifyPlan/evidence-code.txt` |
| `python3 tools/round-37/gen-squashfs.py … --endian be --comp gzip\|xz` ×2 each, one pair 3 s apart | 0 | identical sha256 within each pair — `determinism.txt` |
| `find corpus/evidence/round-37/c1/K{1,2}/src -type l` | 0 | K1 `link-to-hello -> ../hello.txt` (escaping), K2 `var/lib/run-link -> ../../a/run.sh` (in-tree) |
| `grep -n 'oracle_files\|frontier_note' tools/round-38/c1-counter.py` | 0 | `:186` guard, `:208-209` prose binding |

Scratch `/fast/scratch/hyaku/kaidoku-r39/R39SimplifyPlan` removed on exit; no scratch or `/tmp` path is
cited as evidence. No tool installed, no package touched. No REA run: no dev carrier was needed, and the
held-out discipline (no REA on K5/K6, none on held-out) holds trivially.
