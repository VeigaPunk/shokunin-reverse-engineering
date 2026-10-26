# SquashFS `extract-firmware` outcome triage v2: a verb/provider guard, eleven labels, and an action scored with the label (round 40)

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 24-70 (AVM branch 44-50, `get_dependencies` 68-69) — as read 2026-10-26
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `fix_symlink` lines 50-92 — as read 2026-10-26
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `dist/domain/firmware/firmwareAnalysis.js:84-101`, `dist/firmware/FirmwarePublication.js:68-75,241,286-308`, `dist/firmware/FirmwareReports.js:254-255,284` — as read 2026-10-26
source: S120 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py — `report.py:91-98,118-122,133-138`, `extractors/command.py:59-77,101-102` — as read 2026-10-26
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — `-be` handling and `debian/rules` lines 15-18 (`-DFIX_BE` build) — as read 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-40/sqfs-triage-v2.py --skill SKILL.md --table-only` -> `rules: 11`, exit 0, and the ten tokens on the `sqfs-triage-actions` line are exactly the ten distinct tokens the table's action column uses (until the v2 interpreter lands, count the v2 table's `| label |` rows: 11)

**Features.** Version 2 of the triage table reads two fields more than version 1, and they come
first: `OP` = `data.operation` and `PV` = `data.provider.id`. Both are present in every round-39
REA 6.5.0 `extract-firmware` receipt — `corpus/evidence/round-39/c1/K{1..6}/after.json` carry
`"operation": "extract_firmware"` and `"provider": {"id": "unblob", "name": "Unblob", "version":
"26.6.4"}` — and in every round-39 held-out envelope, so `unblob` is the string to key on; the
provider *name* (`Unblob`, capital U) is a different field and never equals it. The six version-1
fields are unchanged: `H` = the `squashfs*` chunk handlers, `G` = the set of
`extraction_gaps[].kind`, `D` = the union of their `dependencies`, `BE` = a standalone `-be`
token in a recorded sasquatch command (`n/a` when no command is recorded), `SR` = a
`MaliciousSymlinkRemoved` report, `P` = `len(normalized_result.files)`. An envelope is accepted
either as a bare `data` object or as the full `{ok, data, meta}` CLI envelope.

**The domain guard (R39-CL1).** Version 1 had none, so it labelled
`corpus/evidence/round-26/c1/envelopes/function-base.json` — `operation` `analyze_function`,
`provider.id` `ghidra` — as `no-squashfs-chunk`, a SquashFS verdict on a Ghidra function analysis
(`.ufo/waves/round-39/w2/R39W2C2AxisFit.md` C2, lines 143-150). In version 2 every row carries
`operation` = `extract_firmware` and `provider` = `unblob`, so a receipt from another verb or
another provider matches no row and reads `unclassified`. An envelope with no `operation` or no
`provider.id` therefore reads as an empty string and falls through to `unclassified` as well; an
absent domain field is a non-match, never an unreadable envelope.

**Eleven labels, one per row, pairwise disjoint on the eight features.** The eleven decision
vectors are distinct, so "first match wins" cannot leak and the label is a function of the
envelope, not of row order:

| label | OP/PV | H | G | BE | SR | P |
| --- | --- | --- | --- | --- | --- | --- |
| no-squashfs-chunk | `extract_firmware`/`unblob` | none | ∅ | n/a | no | 0 |
| dep-missing-be | `extract_firmware`/`unblob` | `squashfs_v4_*` | {missing-extractor-dependency} | n/a | no | 0 |
| dep-missing-le | `extract_firmware`/`unblob` | `squashfs_v4_*` | {missing-extractor-dependency} | n/a | no | 0 |
| avm-marker-be-dropped | `extract_firmware`/`unblob` | `squashfs_v4_be` | {extractor-failure} | no | no | 0 |
| body-extractor-failure | `extract_firmware`/`unblob` | `squashfs_v4_be` | {extractor-failure} | yes | no | 0 |
| partial-body-failure | `extract_firmware`/`unblob` | `squashfs_v4_be` | {extractor-failure} | yes | no | >0 |
| mixed-symlinks | `extract_firmware`/`unblob` | `squashfs_v4_*` | {unpublished-entry} | n/a | yes | >0 |
| escaping-symlink-removed | `extract_firmware`/`unblob` | `squashfs_v4_*` | ∅ | n/a | yes | >0 |
| in-tree-symlink-metadata | `extract_firmware`/`unblob` | `squashfs_v4_*` | {unpublished-entry} | n/a | no | >0 |
| clean | `extract_firmware`/`unblob` | `squashfs_v4_*` | ∅ | n/a | no | >0 |
| clean-empty | `extract_firmware`/`unblob` | `squashfs_v4_*` | ∅ | n/a | no | 0 |

The rounds-39 classes `clean-be` and `clean-le` collapse into the one label `clean` (`H` is an
fnmatch cell, `squashfs_v4_*`); `version-minor-mismatch` reads `body-extractor-failure`, which is
what the version-1 held-out set expected for it (`H19`/`H20` in
`corpus/evidence/round-39/c2/heldout/manifest.json`).

**Every condition column decides at least one case.** Replacing one condition column at a time
with `*`, over thirty-three vectors (the twenty round-39 held-out envelopes, six round-39 Core
receipts, the two measured `w2` shapes, and five out-of-domain mutations), costs: `operation` 2,
`provider` 2, `handler` 1, `gap kinds` 9, `dependencies` 2, `-be in child argv` 4,
`symlink removed` 9, `published files` 2 — eight of eight columns, seat check
`check-draft.py` in `.ufo/waves/round-40/w1/artifacts/R40C2TableDraft/` (exit 0). Version 1's
`-be` and `symlink removed` cells could both be set to `*` and still reach 20/20 on the round-39
set, which is what the wave-2 attack measured (`.ufo/waves/round-39/w2/R39W2C2AxisFit.md`); in
version 2 the `-be` column is what separates the four body-failure vectors from the marker row,
and `symlink removed` decides nine. The two dependency rows deliberately share the
`squashfs_v4_*` handler pattern so that endianness is decided by the missing binary's name —
`sasquatch-v4be` against `sasquatch`, the only value unblob's `Command.get_dependencies()` reports
(S120 `command.py:101-102`) — instead of the dependency restating the handler.

**The marker row, worded for the genuine layout.** Version 1's `avm-marker-be-dropped` row read
"`-be` was dropped -> rerun through a `PATH` wrapper that appends `-be`". That action is right for
a standard-BE body whose `mkfs_time` happens to equal `bytes_used`, and wrong for a genuine
AVM-layout body, whose only distinguishing field is the little-endian metadata block-length header
(lane S114 / Freetz): unblob drops `-be` there too and the extractor **succeeds** — the AVM 07.57
BE member publishes 2 942 files with no `-be` in its argv
(`.ufo/waves/round-39/w1/R39AssimAvmCritic.md`). The mirror case is a genuine layout with the
marker stripped: unblob then adds `-be` and the run fails with zero files. Version 2 therefore
keys the marker row on `BE` = `no` **and** a recorded `extractor-failure` **and** `P` = 0 — a body
that fails without `-be` is the marker artefact — while a genuine layout that publishes files is
`clean` and a genuine layout with the marker stripped lands in `body-extractor-failure`, whose
cause sends the reader to the block-length header before keeping `-be`. The timestamp is the
trigger; the block-length field is the format test (S112 lines 44-50).

**Mixed symlinks (R39-CL2).** A carrier can hold both link kinds. Measured: round-39 `K5` and `K6`
each carry `G` = {`unpublished-entry`} **and** a `MaliciousSymlinkRemoved` report with `P` = 10 and
8 (`corpus/evidence/round-39/c1/K5/after.json`, `K6/after.json`) — two in-tree links and one
escaping on K5, the reverse on K6. Version 1 labelled them `escaping-symlink-removed` and told the
reader to ignore their in-tree gaps, which contradicts their own gaps. Version 2 places
`mixed-symlinks` above the escaping row; its action `expect-removed-and-unpublished` names both
halves, so the escaping path stays absent *and* the kept links are counted as metadata. Gap
multiplicity is erased (a set): the row cannot count how many links of either kind an image holds.

**Zero and partial publication (R39-CL3 D1/D2).** Two measured outcomes had no row in version 1
and were labelled `unclassified`: a damaged body that still publishes files — `full-be1-xz`,
`G` = {`extractor-failure`}, `BE` = yes, `SR` = no, `P` = 6 — and a clean extraction of a tree
that holds no regular file — `full-be-dirempty-gzip`, `G` = ∅, `BE` = `n/a`, `P` = 0
(`.ufo/waves/round-39/w2/artifacts/R39W2C2TableReview/xz-shape.json`,
`dirempty-shape.json`). Version 2 gives them `partial-body-failure` (`accept-partial-published`:
match the published subset against the oracle and keep the failing command) and `clean-empty`
(`accept`: an extraction that published nothing is only `clean` when the carrier's own oracle is
empty — an empty envelope with no squashfs chunk is still `no-squashfs-chunk`).

**Actions are scored with the label.** The table's `action` column is one token from a closed
vocabulary of ten, declared in the SKILL block; a token outside it, or a row with two tokens, is a
malformed table (exit 2), never a non-match. The pairs are: `clean`/`clean-empty` -> `accept`;
`in-tree-symlink-metadata` -> `resolve-unpublished`; `escaping-symlink-removed` ->
`expect-removed`; `mixed-symlinks` -> `expect-removed-and-unpublished`; `dep-missing-be` ->
`install-sasquatch-v4be`; `dep-missing-le` -> `install-sasquatch`; `avm-marker-be-dropped` ->
`rerun-with-be-wrapper`; `body-extractor-failure` -> `keep-failure-evidence`;
`partial-body-failure` -> `accept-partial-published`; `no-squashfs-chunk` -> `check-superblock`.
The `cause` column is documentation, adjacent to but not inside the action token, so a counter can
score the action without parsing prose.

**Status and limits.** Development evidence only: the claim is scored on a held-out set generated
after the freeze with the freeze commit hash as seed, and the interpreter reads only this table and
the envelope. No cell of the version-2 table is a bare `*`, so the "best table plus `*` default
row" control has nothing to feed on and a default row can only damage the score. Out-of-set is
`unclassified` by design: a marker-dropped run that still publishes files, a genuine AVM layout
whose marker was stripped (`BE` = yes, 0 files — indistinguishable from body damage on these
features), a mixed-symlink image that also fails extraction, `unknown-chunk-handler`,
`encrypted-chunk` and `depth-limited` gaps, non-SquashFS or non-`extract_firmware` receipts, and
anything at all about extracted programs. Version 1 (`SKILL.md` rule block 18) is unchanged and
still carries its round-39 demonstration.
