# R39 minimality table — clause × kill control × risk

Seat R39SimplifyPlan, 2026-10-26. Draft reviewed: `plans/round-39-claims.md` (unfrozen).
Base `a2f64e1da78afcf8cc39287106604dbcc270844c`. No round-39 tool, counter or carrier exists yet
(`ls tools/round-39/` → absent; `.ufo/waves/round-39/c1/` → absent), so "discriminating power" is
judged against (a) the draft's own frozen kill list, (b) the shape the round-38 counter actually
implemented (`tools/round-38/c1-counter.py`), and (c) the producer code the signals come from.

Evidence files beside this one: `evidence-code.txt` (exact source lines), `evidence-envelopes.txt`
(committed receipt fields), `determinism.txt` (generator byte-determinism).

Abbreviations: **CUT** = drop, no listed control lost; **KEEP** = a listed control depends on it;
**KEEP+** = keep only with the stated rewording or guard; **ADD** = a guard the draft lacks that a
do-nothing or degenerate control would otherwise reach.

---

## P39-C1 — clause by clause

| # | clause (draft) | what can make it red | listed control that needs it | risk | verdict |
|---|---|---|---|---|---|
| c1 | "for each of the six frozen … carriers" / `carriers_matched == 6` | 5 of 6 matched | CTL do-nothing (0≠6); CTL round-38 receipts copied for K1–K4 with K5/K6 absent (4≠6) | none — enumerated by the frozen `carriers.json` | **KEEP** (this is the whole target) |
| c2 | "(rea-agents 6.5.0, …)" as a named version | a 6.7.0-run receipt | none | none, but it duplicates the rule already stated later ("recomputes … under the rea-agents 6.5.0 rule") — the second mention is the enforceable one | **CUT** the version words at this position |
| c3 | "(unblob 26.6.4, …)" | `provider.version` ≠ 26.6.4 | none directly | ~zero: one receipt field, and the same carrier bytes under a different unblob change the sanitiser rule the oracle derives from | **KEEP** (free field compare) |
| c4 | "`sasquatch-v4be` 4.5.1 reachable on the child PATH" | nothing checkable | none | **high**: `environment` is `null` in every committed receipt (`evidence-envelopes.txt`), so the receipt cannot show PATH or the binary version; and every failure it could catch already surfaces as `extraction_failed: true` **plus** a non-`unpublished-entry` gap — proven on the round-36 before-arm (`extraction_failed: True` + `missing-extractor-dependency`, `dependencies: ["sasquatch"]`) | **CUT** (or move to a harness sidecar *and* give it its own control — strictly more machinery for zero discrimination) |
| c5 | "first added in a commit that descends from the freeze" | receipt bytes committed at or before the freeze | the *pre-freeze* variant of the copy control; it is the only structural discriminator for a K1–K4 receipt whose bytes were carried over | medium: needs `git log --ancestry-path`; but the machinery is already in-tree (`tools/round-38/freeze-drift.py`, same `git log FREEZE..REV -- path` shape) | **KEEP+** merged with immutability: "is the single commit that added it after the freeze" (one `git log` count, not two clauses) |
| c6 | "names the `squashfs_v4_be` handler" | LE handler, or no handler | CTL wrong-handler | none | **KEEP** |
| c7 | "with no failed chunk" | a chunk with `extraction_failed: true` | none — fully **redundant** | proven by producer code: `chunkGaps("extractor-failure", (chunk) => chunk.extraction_failed === true && chunk.handler !== null && chunk.encrypted !== true && !dependencyChunkKeys…)` (`cli.js:14271`). Every failed squashfs chunk yields `extractor-failure` — or `missing-extractor-dependency`, or `encrypted-chunk` — i.e. a gap that is not `unpublished-entry`, which c9 already reds | **CUT** |
| c8 | "publishes every regular file of the frozen independent oracle (same relative-path suffix, same sha256)" | one oracle row missing or hashed differently | every control (this is the extraction result) | none — enumerated by `oracle.tsv`; suffix matching is already the round-38 rule | **KEEP** |
| c9 | "carries extraction gaps of kind `unpublished-entry` exactly on the frozen oracle's in-tree symlinks" | missing gap (link materialised or dropped), extra gap, wrong kind | CTL materialise-the-symlink-with-no-gap; CTL wrong gap kind; CTL escaping-symlink-kept-as-a-gap | **defect D1**: the envelope's gap path carries the output prefix — K2's committed gap is `firmware.bin_extract/var/lib/run-link` while the oracle row is `var/lib/run-link`; without the suffix rule the clause is red by construction on its one currently-known in-tree carrier. **D2**: REA's `unpublished_entries[].kind` is `symlink` **or `special`** (`firmwareAnalysis.js:139`), so the clause's subject set is in-tree *non-regular* entries, not symlinks only | **KEEP+** state the suffix rule for gap paths exactly as for files, and name the subject "in-tree non-regular entry" |
| c10 | "and no other gap" | any gap outside the table | none new — "exactly on X" is already set equality in both directions | redundant three words that invite a second, weaker implementation of the same condition (subset-only) | **CUT** |
| c11 | "publishes no path for the oracle's escaping symlinks" | an escaping link published as a regular file | **none in the draft's kill list** | without it the rule is half-enforced: materialising an *escaping* link leaves the gap set exact, so every other clause greens on a wrong rule. Cost of enforcing: one set difference over a table C1 already needs | **KEEP + ADD** one control: "escaping link published as a file in `files[]`" → red |
| c12 | "has a subject digest equal to the frozen carrier pin" | receipt for another input | wrong-input variant of the copy control | none — one receipt field, already checked by round-38's `after_subject_ok` | **KEEP** |
| c13 | "recomputes to its stored evidence id under the rea-agents 6.5.0 rule" | hand-edited or naively patched envelope | CTL fabricated receipt | medium in the *kill rule*, not the clause: round-36 limit 9 records that an envelope fabricated from the oracle and re-hashed with REA's own digest code still recomputes. The control must therefore name the fabrication class ("patched `files`/`extraction_gaps` without recomputing"), and the re-hashed class is a disclosed limit caught only by c5 | **KEEP** + specify the control's class |
| c14 | PROVINCE Core row → entry → SOURCES row opened 2026-10-26 → used-by lists the entry | missing row/entry/citation | CTL do-nothing (no landed bytes) | low, except the literal date: a round that slips a day fails on the calendar, not on the work | **KEEP+** replace the literal with "opened on the freeze commit's date" (derived, not typed) |
| c15 | "a round-39 frontier note supersedes the big-endian part of the Frontier bullet" | — | none | **high relative to its power**: round-38's implementation is `'big-endian' in line and 'superseded' in line` (`tools/round-38/c1-counter.py`, `frontier_note`), which a do-nothing lane satisfies with one prose line. It cannot be made discriminating by a counter | **CUT from the predicate**; keep as a work requirement verified by the closure's spot-check (PROVINCE must not contradict itself), not as a scored binding |
| c16 | "`corpus/README.md` holds a coverage-map row naming the entry stem" | missing row | CTL do-nothing | low: structural row test, cheap, and it is the lane's existing coverage-accounting convention (round-38 row) | **KEEP** (note: it asserts the same move as c14 in a second document — convention, not a second convention) |
| c17 | "no frozen C1 path changed after the freeze" | post-freeze edit of carriers/oracle/tables | CTL do-nothing post-freeze amendment; QUALITY 79 | **defect D3**: an unenumerated universal — "frozen C1 path" names no set, and §6 item 9 forbids universals the command does not enumerate. The machinery already exists (`freeze-drift.py` DEFAULT list) | **KEEP+** name the set: "no path of the freeze-drift set (claims doc, both counters, carriers manifest, oracle and symlink tables, held-out generator) has a commit in freeze..rev" |
| c18 | "`carriers_matched == 6` and every binding true (`met_target`)" | — | — | tautology over the counter's own flag; round-36 limit 9 records receipts where `met_target` and `matched` diverged | **KEEP** only `carriers_matched == 6` as the stated target |

### Guards C1 lacks (degenerate passes the draft does not close)

| id | degenerate pass | guard |
|---|---|---|
| g1 | empty symlink tables + carriers with no symlinks → c9/c11 green vacuously | **ADD**: across the six frozen tables there is ≥1 `in-tree` and ≥1 `escaping` link. (Round-38's counter already carries the sibling guard `oracle_files > 0`.) |
| g2 | an oracle table with zero rows on a carrier → c8 trivially true | **ADD**: every frozen `oracle.tsv` is non-empty (round-38 shape, keep it) |
| g3 | escaping links whose target passes *through* another symlink, or an empty target: unblob resolves with the real filesystem (`extractor.py:50-92`) and silently unlinks an empty target (`extractor.py:67-70`) with **no** report, while the oracle classifies by POSIX path arithmetic | **ADD** as a frozen generator constraint on K5/K6: no symlink chain, no empty target, no special file. Otherwise the rule can false-red on a carrier that is "correct" under both implementations |

---

## P39-C2 — clause by clause

| # | clause (draft) | what can make it red | listed control that needs it | risk | verdict |
|---|---|---|---|---|---|
| d1 | "the frozen triage interpreter `tools/round-39/sqfs-triage.py`" | — | all controls | none | **KEEP** |
| d2 | "reading only the SKILL.md craft-section triage table" | interpreter keyed on its own hardcoded table | CTL round-36 table transcribed into the interpreter grammar | **unprovable as written** — "reading only" is a property of the interpreter's internals, not of the run | **KEEP+** as an invocation contract: the counter calls it with exactly two inputs (the craft-section table bytes, the envelope) and the interpreter's source references no other repo path |
| d3 | "the class label its frozen generator assigned before any REA run" | a label chosen after looking at the envelope | CTL catch-all / gap-count / gap-kind tables (their redness needs labels that are not eyeballed) | **the deepest hole in the draft**: "before any REA run" is unobservable from any committed byte; every listed control can be made green by a label set edited after the envelopes were read | **KEEP+** replace with a re-derivation: the counter runs the frozen generator with the seed and requires the labels it emits to equal the manifest's |
| d4 | "for all N held-out carriers (2 per class)" | — | — | N is unbound in the sentence; "2 per class" is a manifest spec, not a per-envelope condition — a universal whose enumeration the predicate never names | **KEEP+** "every envelope in the frozen manifest"; move "≥2 envelopes per class" into the manifest guard (g4) |
| d5 | "generated by the frozen `heldout-gen.py` with seed = the freeze commit hash" | — | anti-tuning (nothing else) | none; note the ordering consequence: the freeze hash exists only after the freeze commit, so generation is post-freeze by construction | **KEEP** |
| d6 | "every carrier regenerates byte-identically from that seed" | a hand-assembled carrier | none — it is the fairness proof | **was the top freeze-killer candidate** (wall-clock mtimes); measured false: `gen-squashfs.py` writes `MKFS_TIME = 1700000000` into every inode (`:14`), and identical bytes reproduce across a 3 s gap and across separate trees (`determinism.txt`) | **KEEP** — now grounded; the constraint is that heldout-gen.py writes the trees itself, never via `tar`/`cp` |
| d7 | "every envelope's subject digest equals its carrier" | wrong input | round-36 CL6 | none, one field | **KEEP** |
| d8 | "the manifest is first added in a commit descending from the freeze and no later than its envelopes" | manifest authored after the envelopes | ordering control | low once d3 is re-derived by the generator: the ordering clause stops being load-bearing | **KEEP+** one ancestry check: the manifest's adding commit is a descendant of the freeze and an ancestor-or-equal of every envelope's adding commit |
| d9 | "the triage table bytes at the measured revision equal those at the freeze" | a table edited after the envelopes were read | tuning class | none; `freeze-drift.py` already does it | **KEEP** |
| d10 | "`matched == N` and every binding true" | — | — | same tautology as c18 | **KEEP+** "`matched` equals the manifest's envelope count" |
| d11 | class list carrying "`+ no-squashfs-chunk` if recon shows it distinct" | — | — | **defect D4**: a predicate may not carry a conditional into the freeze; and an envelope with no squashfs chunk is not "an REA `extract-firmware` outcome on a SquashFS v4 input" — the input is not SquashFS | **CUT** the conditional; freeze the class list literally |
| d12 | "each row source-cited" (surface description) | — | none | it would make C2 read `corpus/SOURCES.md`, which breaks the claim's own separability clause; C1 already carries the round's sourced claim | **CUT from the scored text**; keep as a writing requirement |
| d13 | classes `avm-marker-be-dropped` vs `body-extractor-failure` | — | CTL gap-kind-only; CTL catch-all | **risk to the target, not surplus**: both land on `extraction_failed: true` + `extractor-failure`, same dependency list, 0 files (`evidence-envelopes.txt`, AVM probe). They are separable only through `diagnostics[].report.stderr` (the AVM drop's text is "suggests a SquashFS image of a different endianess"). If the generator's body-damage case emits a stderr the AVM row also matches, both labels collapse and the two classes score as one — a gap-kind-only table then meets the target on them | **KEEP** the class pair + **require** both stderr texts committed as recon evidence before the freeze |

### Guards C2 lacks

| id | degenerate pass | guard |
|---|---|---|
| g4 | a manifest with 1 envelope per class → a lucky or label-echoing table greens | **ADD**: ≥2 envelopes per frozen class |
| g5 | an interpreter that returns one constant string per *file* (not per table row) | covered by the held-out set only if ≥2 classes share a gap shape — they do (d13); no extra guard needed |

---

## Producers' observable vocabulary (what a class label may key on)

From `evidence-envelopes.txt` + `evidence-code.txt`, the fields a triage row can legitimately use:

| field | values observed | separates |
|---|---|---|
| `normalized_result.chunks[].handler` | `squashfs_v4_be` (all six C1 carriers) | squashfs vs not |
| `chunks[].extraction_failed` | `false` clean / `true` on the AVM drop and on the dep-missing before-arm | success vs failure |
| `extraction_gaps[].kind` (six kinds, `firmwareAnalysis.js:85-90`) | `missing-extractor-dependency`, `unknown-chunk-handler`, `encrypted-chunk`, `depth-limited`, `extractor-failure`, `unpublished-entry` | failure classes |
| `extraction_gaps[].dependencies` | `["sasquatch"]` (LE) / the BE binary (single name — `Command.get_dependencies` returns `[self._executable]`, `command.py:101-102`, which is why the round-36 LE arm reports one name even though the CLI preflight table lists both, `squashfs.py:68-69`) | `dep-missing-be` vs `dep-missing-le` |
| `unpublished_entries[].kind` | `symlink` (also `special`, never observed) | in-tree metadata vs nothing |
| `diagnostics[].report.__typename__` | `MaliciousSymlinkRemoved` on K1 (escaping link) / `ExtractCommandFailedReport` on the AVM drop | `clean` vs `escaping-symlink-removed`; AVM vs body |
| `diagnostics[].report.stderr` | "…suggests a SquashFS image of a different endianess… FATAL ERROR: File system corruption detected" | AVM vs generic body damage |
| `coverage`, `files[]`, `published_bytes` | `partial`/0 on both failure shapes — **no** separation | — |

Note the diagnostic `link`/`target` fields hold absolute scratch paths (`/fast/scratch/…`), so a table
or counter must never key on them: round-36 limit 4 already rules `subject.local_path` non-durable,
and the same applies here.
