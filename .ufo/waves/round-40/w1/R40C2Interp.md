# R40C2Interp — R40-C2 table-v2 interpreter, selftest and integration block

**VERDICT: DONE.** Delivered `sqfs-triage-v2.py` (pure stdlib, `-I -B` safe) plus the 11-row
`<!-- sqfs-triage-table v2 -->` block it validates, a 45-case selftest that passes 45/45, and
26/26 correct `(label, action)` decisions on the round-39 envelope evidence. Nothing frozen was
edited; no REA/unblob/sasquatch run; no tool installed or removed.

Seat: `R40C2Interp` (leaf; no subagents, no background jobs). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`.
Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C2Interp` (removed at exit); every cited output was copied
into the artifacts dir.

## 1. Deliverables (all under `.ufo/waves/round-40/w1/artifacts/R40C2Interp/`)

| file | role | sha256 |
|---|---|---|
| `sqfs-triage-v2.py` | the interpreter the L1 integrates as `tools/round-40/sqfs-triage-v2.py` | `336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617` |
| `v2-block.md` | the exact bytes to add to `SKILL.md` `## Queue-drain craft` as rule block 19 (`--print-table` reproduces them) | `5122a03ef25145b30e9886dfc9550ed68cf9071729d40f38d56236ab82deda6c` |
| `selftest.txt` | `--selftest` output, 45 cases | — |
| `table-only.txt`, `integrated-table-only.txt` | `--table-only` on the printed block and on a real-SKILL copy with the block inserted | — |
| `integrated-run.txt` | 26 envelope decisions against the integrated-SKILL copy | — |
| `v2-new-shapes.txt` | the three outcome shapes the v1 table could not express + K5 | — |
| `json-mixed.json` | `--json` shape (features, rule index 7, row cells) | — |
| `real-skill.txt` | `SKILL.md` at this base is v1-only: exit 2 with the v2 marker named | — |
| `commands.txt` | every command, exit code and the two hashes | — |

Integration is two steps and no source elsewhere in the lane: (1) copy the `.py` to
`tools/round-40/sqfs-triage-v2.py`; (2) insert `v2-block.md` verbatim after the
`## Queue-drain craft` heading, ahead of the existing block-18 v1 table (the v2 marker is earlier in
the section, so the v2 table is the first table after it; the v1 table and its marker stay
byte-identical). If the L1 edits any row, the constant `TABLE_BLOCK` and the selftest's `VOCAB`
must be edited with it — `--print-table` is the single source for both.

## 2. Contract as implemented

Invocation `python3 -I -B sqfs-triage-v2.py [--skill SKILL.md] [--json] [--table-only] [--selftest]
[--print-table] ENVELOPE.json...`

* default output: one `path<TAB>label<TAB>action` line per envelope, path exactly as given;
* `--json`: `skill`, `marker_line`, `actions_line`, `table_line`, `rules`, `actions`, and per
  envelope `path`, `label`, `action`, `rule` (1-based matched row or `null`), `row` (raw 12 cells or
  `null`), `features` (`OP`, `PV`, `H`, `G`, `D`, `BE`, `SR`, `P`, `commands`);
* `--table-only`: validates and prints marker/actions/table lines, the rule count, the vocabulary in
  declaration order, then every parsed rule with its normalised cells, action, cause and source;
* exit `0` ok; `2` table missing/malformed — wrong header, malformed cell, duplicate label, unknown
  action token, missing/misplaced vocabulary line, marker `v1` only, table outside the craft
  section — or envelope unreadable (missing file, invalid JSON, non-object, no `normalized_result`
  and no `operation`); `1` only for a failed `--selftest`.

Grammar is exactly the L1 draft: 12 columns
`label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source`;
rows top-to-bottom, first full match gives `(label, action)`; no match gives
`(unclassified, none)`; `*` / exact / `none` / `+`-set / `yes|no|n/a` / `0|>0` cell semantics as
specified. `OP = data.operation`, `PV = data.provider.id` (verified against all 26 round-39
envelopes: `extract_firmware` / `unblob`; `provider` is always `{id,name,version}` in this evidence
set, and a bare-string provider is accepted as `PV`). `H/G/D/BE/SR/P` are the v1 extraction verbatim
including shlex tokenisation and the standalone `-be` token test.

## 3. The v2 table (11 rows, 11-token closed vocabulary)

Vocabulary: `none inspect-input install-extractor-be install-extractor-le wrap-extractor-be
preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty`.

| # | label | discriminant | action |
|---|---|---|---|
| 1 | `no-squashfs-chunk` | handler `none` | `inspect-input` |
| 2 | `dep-missing-be` | `squashfs_v4_be` + `missing-extractor-dependency` + dep `sasquatch-v4be`, P `*` | `install-extractor-be` |
| 3 | `dep-missing-le` | `squashfs_v4_le` + same gap + dep `sasquatch`, P `*` | `install-extractor-le` |
| 4 | `avm-marker-be-dropped` | `squashfs_v4_be` + `extractor-failure` + BE `no`, P `*` | `wrap-extractor-be` |
| 5 | `body-extractor-failure` | `squashfs_v4_*` + `extractor-failure`, P `0` | `preserve-failure` |
| 6 | `partial-body-failure` | `squashfs_v4_*` + `extractor-failure`, P `>0` | `salvage-partial` |
| 7 | `mixed-symlinks` | `squashfs_v4_*` + `unpublished-entry` + SR `yes` | `audit-symlinks` |
| 8 | `escaping-symlink-removed` | `squashfs_v4_*` + SR `yes`, any gap | `expect-link-absent` |
| 9 | `in-tree-symlink-metadata` | `squashfs_v4_*` + `unpublished-entry` + SR `no` | `count-gap` |
| 10 | `clean` | `squashfs_v4_*`, no gap, SR `no`, P `>0` | `none` |
| 11 | `clean-empty` | `squashfs_v4_*`, no gap, SR `no`, P `0` | `confirm-empty` |

Every row carries `operation = extract_firmware` and `provider = unblob` exactly — that pair is the
R39-CL1 domain guard, and the table declares no `*` domain cell. Row 7 sits ahead of row 8 (R39-CL2),
row 6 ahead of nothing but is split from row 5 by the `published files` cell, and row 11 splits the
`clean` row on `P = 0` (R39-CL3 D1/D2). Causes name the mechanism and the remedy in one `->`
sentence; sources cite S112/S118/S119/S120/S121 with line ranges plus the lane evidence
(`c1/K1..K6`, `c2/H01..H04`, `R39-CL2`, `R39-CL3`).

## 4. Selftest — 45 cases, 45 pass (`selftest.txt`)

All SKILL variants are written under `$TMPDIR`; every envelope is a lane fixture
(`corpus/evidence/round-39/c2/heldout/H*/envelope.json`, `.../c1/K*/after.json`) or a deep copy of
one mutated in scratch. Coverage of the required matrix:

* table parse/validate — green block; `--table-only` (11 rules, vocabulary order); `--print-table`
  round-trip; first table after the marker wins; marker absent; marker without table; table outside
  the craft section; marker `v1` only (real v1 block extracted from `SKILL.md`); wrong header;
  malformed `operation` cell; malformed set cell (`unpublished-entry+`); malformed `published files`
  cell; empty action cell; short row; duplicate label; unknown action token; missing vocabulary
  line; vocabulary line separated from the table by prose;
* cell types — exact operation/provider, `*` operation/provider; handler `none`/pattern/`*`; gap and
  dependency `none`/exact/`*`; two-kind exact-set miss; dependency superset; BE `yes`/`no`/`n/a`;
  SR `yes`/`no`; P `0`/`>0`/`*`; actions from the vocabulary;
* domain guard — non-`extract_firmware` envelope (still carrying a `squashfs_v4_be` chunk) →
  `unclassified`/`none`; non-`unblob` provider → `unclassified`/`none`; a domain-mismatched envelope
  with no `normalized_result` stays readable (exit 0, `unclassified`); an `extract_firmware`
  envelope with no `normalized_result` is exit 2; the same out-of-domain envelope labels under a
  row with `*` domain cells (proves the guard is the table's doing);
* first-match order — two identical matching rows give the first; `mixed-symlinks` beats
  `escaping-symlink-removed` on K5/K6;
* v2-new outcomes — `partial-body-failure` (H15 shape with one published file),
  `clean-empty` (H01 shape with zero files), both distinct from `body-extractor-failure`/`clean`;
* evidence replay — all 20 round-39 held-out envelopes, the manifest's own labels agree with the
  selftest expectation table, and K1..K6 give escaping/in-tree/clean/clean/mixed/mixed;
* envelope forms — bare `data` and full `{ok,data,meta}` produce identical features and decisions;
  missing file, `{}`, invalid JSON, JSON scalar → exit 2 each;
* `--json` shape — rule index, 12-cell row, action cell, all eight features, top-level vocabulary.

Commit-level replay on a *real* SKILL copy (block inserted after the craft heading, v1 block left in
place) gives the same 26 decisions (`integrated-run.txt`); at this base `SKILL.md` has no v2 marker,
so the adaptive `real-skill` case asserts exit 2 and starts asserting `clean`/`none` for H01 plus a
clean `--table-only` the moment the block lands.

## 5. Deviations from the L1 contract draft (and why)

1. **Envelope readability with the domain guard.** The draft says an unreadable envelope is exit 2,
   and v1 required `normalized_result`. Taken literally, a genuine non-`extract_firmware` REA envelope
   (different `normalized_result` schema — or none) would exit 2 and the planned out-of-domain class
   could never be scored `unclassified`. Implemented rule: a bare object or full envelope is readable
   when it carries a `normalized_result` **object** or a string `operation`; an `extract_firmware`
   envelope must *also* carry `normalized_result` (exit 2 otherwise). So the domain guard remains a
   label decision and payload drift in another verb cannot fake readability.
2. **Absent `operation`/`provider` never defaults.** There is no implied `extract_firmware` domain:
   an absent field becomes `''`, which no exact cell matches → `unclassified`. A `*` domain cell is
   the only way to accept it. (`real-skill`/`--table-only` do not depend on this; every REA envelope
   records both fields.)
3. **Vocabulary line placement.** "Directly above the table" is implemented as *the last non-blank
   line before the table header* inside the craft section, containing
   `<!-- sqfs-triage-actions: … -->` with a closing `-->`; blank lines are tolerated, prose is not.
   The line may sit above or below the v2 marker. Tokens must be lowercase dashed and unique —
   duplicates are treated as malformed (exit 2) rather than silently deduped.
4. **`none` is an ordinary token.** It is in the vocabulary, `clean` uses it as its row action, and
   it is also the action of the no-match default. No row is required to declare it.
5. **Cell breadth chosen for measured outcomes, not for looseness.** Symlink rows (7–9) use
   `published files = *` because the link count and the file count are independent; dep-missing rows
   (2–3) use `*` because the AppImage before-arm publishes its ELF prefix beside the same gap (the
   round-39 SKILL table already broadened this from v1's `0`); the AVM row (4) uses `*` because the
   `-be` absence decides it regardless of what was published; body rows (5–6) use BE `*` so a
   little-endian body failure (`BE = no`, no marker involvement) is still a body fault. Rows 5/6/10
   still separate on `P`, rows 10/11 on `P`.

## 6. Risks and open items for the freeze

* **Exact-set cells are a hard edge.** An envelope with one extra gap kind (e.g.
  `extractor-failure+unpublished-entry`, or mixed links plus `depth-limited`) matches no row and is
  `unclassified`; `mixed-symlinks` requires the gap set to be exactly `{unpublished-entry}`. The
  frozen held-out generator must build each class with the gap set its row names (measure before the
  freeze), or a row must be added. `[INFERENCE]` the round-39 recipes already do this for every
  existing class; the new `mixed-symlinks`, `partial-body-failure`, `clean-empty` and `out-of-domain`
  recipes do not exist yet.
* **`clean-empty` must really carry no gap.** If the empty-tree recipe still yields an
  `unpublished-entry` (e.g. a special entry), row 11 will not match; confirm on the development
  generator before the freeze or add the measured shape.
* **`partial-body-failure` should be built on a standard-BE image.** A partial failure whose `BE` is
  `no` while `mkfs_time == bytes_used` would match row 4 (the marker row) by design; the round-39
  body-failure recipe (zeroed id-table, bad `s_minor`, `-be` present) is the safe basis.
* **`out-of-domain` must rewrite `data.operation`.** The guard reads `data.operation`, not
  `meta.command` (which is `extract-firmware`, kebab). A cloned envelope left with
  `operation = extract_firmware` is in-domain and would be labelled `clean`.
* **TABLE_BLOCK vs the committed table.** The constant is a convenience copy for
  `--print-table`/integration, never read during classification; if the L1 changes a row it must
  change the constant and the selftest `VOCAB` too, or delete `--print-table` and the constant.
* Not claimed here: no carrier, held-out generation, counter or REA behaviour was exercised; this
  seat writes only the interpreter, the block and the selftest. The counter must score the pair
  `(label, action)` and can read `rule` from `--json` for its distinct-row-decision count.

## 7. Hygiene

No REA/unblob/sasquatch invocation; no carrier read (only committed envelope JSON); no VCS command;
no writes outside this artifacts dir and scratch; no tool installed/upgraded/removed (python 3.14.8,
`/usr/bin/python3`); scratch removed before this report was finalised.
