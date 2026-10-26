# SquashFS `extract-firmware` outcome triage v3: combined gap sets, a `depth-limited` row and one layout pre-check (round 41)

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 24-70 (AVM branch 44-50), handler names and magic patterns 102-522 — re-read 2026-10-26 from the installed unblob 26.6.4 tree (`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`), not re-fetched from the URL
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `is_recursive_link` lines 42-47 and `fix_symlink` lines 50-92 (loop 58-65, empty target 67-69, containment 79-90) — re-read 2026-10-26 from the installed tree
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `dist/firmware/FirmwarePublication.js` (`MAX_EXTRACTION_DEPTH` :23, depth continuation :24-29, `emptyGap` :39-46, dependency gaps :161-201, `extractor-failure` :288-293, `depth-limited` :294-299, `unpublished-entry` :301-307), `dist/domain/firmware/firmwareAnalysis.js:85-90,139`, `dist/firmware/FirmwareRelease.js:27-32` — re-read 2026-10-26 from the installed 6.5.0 package
source: S120 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py — `ExtractCommandFailedReport` :91-98, `ExtractorDependencyNotFoundReport` :118-122, `ExtractorTimedOut` :125-138; `extractors/command.py:60-72` raise sites — re-read 2026-10-26 from the installed tree
source: S122 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/file_utils.py — `is_safe_path`, the containment test `fix_symlink` applies — registry row only, not re-fetched this wave
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-41/sqfs-triage-v3.py --skill SKILL.md --table-only` -> 12 rules, exit 0 (until that interpreter exists: `.ufo/waves/round-41/w1/artifacts/R41C2TableDraft/v3-refparse.py --table-only` on the same block)

**What v3 adds.** Rule block 20 in `SKILL.md` `## Queue-drain craft` holds table v3 after the marker
`<!-- sqfs-triage-table v3 -->`, read by `tools/round-41/sqfs-triage-v3.py`. The eight features, the
(label, action) pair and the no-match pair `(unclassified, none)` are v2's: `OP` = `data.operation`,
`PV` = `data.provider.id`, `H` the `squashfs*` chunk handlers, `G` the gap kinds, `D` the gap
`dependencies`, `BE` a recorded standalone `-be`, `SR` a `MaliciousSymlinkRemoved` report, `P` the
published file count. Twelve rows carry twelve labels and twelve action tokens. Three grammar deltas,
all stated in the block and required of the interpreter: (1) a cell ending in `+` in `gap kinds` or
`dependencies` is a **contains** test — the envelope's set holds that name — while every other non-`*`
cell in those columns stays exact-set equality, `none` is the empty set, and `a+b+` is malformed;
(2) a handler cell `none-v4` matches when **no** handler starts with `squashfs_v4_`, so an image whose
only SquashFS chunk is v1-v3 is clause 2, not a no-match; (3) the reader parses this block out of
`SKILL.md` and carries **no embedded copy** of the table, so a table edit cannot leave a second, stale
text behind (round-40 defect M1).

**The label precedence is the authority (round-40 closure D3).** The expected labels for the held-out
set come from the numbered precedence list in `plans/round-41-claims.md` § R41-C2, applied by an
evaluator written from that text that never reads this table, the interpreter, or the generator's class
map. The table is that list in executable form and nothing else: row order is clause order (no-chunk,
dep, partial, AVM marker, body, depth, mixed, escaping, in-tree, clean, clean-empty), each cell carries
exactly the constraints its clause names and `*` for every feature the clause leaves open, and the
row-by-row map with the composition argument is `.ufo/waves/round-41/w1/artifacts/R41C2TableDraft/rationale.md`.
Where the precedence and the table could drift, the table follows the text: clause 9's `G = ∅` is why
`escaping-symlink-removed` pins its gap cell to `none` instead of v2's `*`, and clause 10's set equality
is why `in-tree-symlink-metadata` keeps the exact singleton while its neighbours are contains cells.

**Combined gap sets (repairs R40-CL5, and round-40 axis-fit F6).** v2 matched gap kinds as exact sets,
so a partial failure that also carried link gaps matched no failure row and fell into
`escaping-symlink-removed` — telling the reader to expect an absent path and losing `salvage-partial`
(`.ufo/waves/round-40/w2/R40W2C2AxisFit.md` F6, measured on H11 plus one injected `extractor-failure`
gap). v3's four failure rows, the depth row and the mixed row are contains cells, which is what clause 4
("whatever other gaps or removed links accompany it") and clause 7 ("whatever symlink gaps accompany
it") say in words. Measured on this draft: the committed 26 round-40 envelopes score 26/26 unchanged,
eighteen precedence-derived combined envelopes score 18/18, and the same block with every `+` stripped
to an exact cell scores 7/18 on those combinations and 0/4 on the round-40 C1 carriers
(`artifacts/R41C2TableDraft/checks.py`, `c-combined.tsv`, `ctl-exact-c-combined.tsv`). The contains form
is load-bearing, not decorative.

**The `depth-limited` row (new).** REA records one `depth-limited` gap per path it did not descend into,
with an empty dependency list and a continuation that names the rerun: a higher `max_depth` up to
`MAX_EXTRACTION_DEPTH` = 10 into a fresh output directory, and at the ceiling `path` set to one published
child below the path, which restarts the depth budget; with no eligible child the region is
*unexamined*, never empty (`FirmwarePublication.js:23-29,294-299`). All four round-40 C1 carriers carry
exactly `{depth-limited, unpublished-entry}` and v2 refused them as `unclassified` — the inherited
ceiling v2's Limits disclosed. v3 labels them `depth-limited-nested` / `raise-depth`; that is a label for
an existing envelope, not a repair of the carrier, and C1 does not read this table (Separability).

**The layout pre-check (repairs M2 and M3).** The envelope cannot see metadata block-length endianness,
so both failure rows share one feature vector across two populations with different remedies: a
standard-BE body whose marker was doctored needs `-be` forced, while a genuine AVM-layout body needs no
change (its marker is authentic) or, when `-be` was forced on it, needs `-be` dropped — round-40 measured
the second population directly (marker-stripped genuine AVM body: four files without the flag, zero with
it, `.ufo/waves/round-40/w1/R40MistakeHunt.md` MH-6). v2 handled this inside two cause cells, which made
the avm row's cause route one branch to `preserve-failure` while its action column could only say
`wrap-extractor-be` (M3), and let the body row claim the fault was "not the endianness handshake" for a
population that is exactly the handshake (M2). v3 hoists one procedure above the table: walk the
inode-table metadata headers at `inode_table_start` as 2-byte little-endian lengths; if they land on
`directory_table_start` the body is AVM layout; then AVM + `-be` absent → damage (`preserve-failure`),
AVM + `-be` present → drop `-be`, standard BE + `-be` absent → `wrap-extractor-be`, standard BE + `-be`
present → damage. The pre-check overrides the action cell when it fires and an inconclusive walk leaves
the cell standing. Both cells are then honest about their own population, and the scored pair stays a
function of envelope fields only.

**Prose repairs riding the block (unscored, reviewed).** M1: no embedded table copy, and `--print-table`
prints the parsed block. L1: block 18's supersession sentence now separates *mislabels* (mixed links,
non-firmware envelopes) from *cannot label* (partial failures, empty trees) and stops at routing only if
block 19 says so; drafted with block 20's own supersession sentence in
`artifacts/R41C2TableDraft/block18-19-prose.md`. L2: the `wrap-extractor-be` wrapper delivery is measured this wave — a
`sasquatch-v4be` earlier on PATH is the binary unblob runs under REA 6.5.0, and appending `-be` flips
the marker-only carrier from `extractor-failure`/`P=0` to three files sha256-identical to its tree
(`.ufo/waves/round-41/w1/artifacts/R41C2TableDraft/l2-wrapper-measurement.md`) — so the cell cites a run,
not a guess. L3: both dependency rows cite S119 as the minter of
`missing-extractor-dependency`. L4: the partial row's oracle-match half is now measured — H21 publishes 5
files of which 4 match the oracle and the fifth is a 16384-byte truncation of an 19873-byte file
(`.ufo/waves/round-40/w2/R40W2C2IndepEval.md` §6) — so it is cited, not marked. L6: the clean row states
that unblob removes an empty-target link with no report at all (S118 :67-69), so `SR = no` never proves
no link was dropped. L7: `none` is both the clean row's action and the no-match action, disclosed below.
F4: the `dependencies` column is disclosed as redundant with `handler` on every measured class.

**Scoring.** The held-out set is generated from the round-41 freeze hash: v2's thirteen classes plus the
combined classes `partial+in-tree`, `partial+mixed`, `depth-limited+in-tree`, `depth-limited+mixed` and
`depth-limited` alone, two replicates each. Partition, stated because a headline count hides it: on v2's
26 held-out envelopes v3 reproduces the v2 pairs (measured on this draft, 26/26), so those pairs are
pre-seen and prove the grammar extension changed nothing for the old classes; the genuinely new decisions
are the combined classes and the depth-limited class. A disagreement between the frozen independent
evaluator and the generator's own class expectation is reported and fails the claim.

**Limits.** The `cause` and `source` columns are prose and are not scored; the action token is. The
`dependencies` column is required by clause 3 but redundant with `handler` on every measured class — a
`squashfs_v4_be` dependency gap always names `sasquatch-v4be` — so ablating it changes no decision.
Provider is never tested alone: in the out-of-domain class `operation` and `provider.id` move together.
`none` is both the `clean` action and the no-match action, so those two envelopes are distinguishable
only by label. The layout pre-check needs carrier bytes and is inconclusive on a truncated body. A
timed-out extractor records `cmd` rather than `command` (S120 :125-138), so `BE` reads `n/a` on such a
run and a timed-out BE failure lands on the body row. Clause order means a dependency gap on one chunk
masks an extractor failure on another: the reader installs the dependency before reading the failure.
Clause 2 labels an image whose only SquashFS chunk is v1-v3 `no-squashfs-chunk`; the name is the
precedence text's, the cause cell says what happened. Gap kinds with no row —
`unknown-chunk-handler`, `encrypted-chunk`, any combined set the clauses do not name — are
`unclassified`/`none`. Genuine AVM-layout extraction outcomes are the C1 surface, not this table's.
