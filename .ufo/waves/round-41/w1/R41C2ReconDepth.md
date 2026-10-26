# R41C2ReconDepth — depth-limited recon (round 41 wave 1, pre-freeze development recon)

**Verdict: CONFIRMED (hypothesis holds on 40/40 dev envelopes) + DEFECTS FOUND (5 draft/grammar
defects, D1–D5 below, two of them load-bearing for R41-C2's predicate).**

Seat `R41C2ReconDepth` (leaf). Item: measure what REA 6.5.0 `extract-firmware` records when a
SquashFS tree holds a regular file that is itself a SquashFS image, at `--max-depth 1` and at the
schema default, alone and combined with the two symlink kinds; deliver recipes and envelopes.
Nothing here is frozen; the L1 integrates.

## 0. Hypothesis, as measured

| clause | result |
|---|---|
| `--max-depth 1` on a squashfs whose tree holds a squashfs file records **exactly one** `depth-limited` gap | **confirmed** — one gap, `kind=depth-limited`, `input_path` = the chunk's **extract directory** (`$output/firmware.bin_extract`), every other gap field null/empty |
| it publishes the outer files | **confirmed** — all three outer regular files published, `coverage=partial` |
| the inner image is also published as a regular file | **confirmed** — `firmware.bin_extract/inner.sqsh` published with its exact sha256, but `reported_sha256=null` and `analysis_depth=null` |
| an in-tree symlink adds `unpublished-entry` | **confirmed** — `G={depth-limited, unpublished-entry}`, `SR=no` |
| an escaping symlink adds `SR=yes` | **confirmed** — `SR=yes`, `G` unchanged (`{depth-limited}`), no gap row for the removal |
| both → combined set | **confirmed** — `G={depth-limited, unpublished-entry}`, `SR=yes` |

Not stated in the hypothesis and measured here: the label of the same bytes **changes with
`max_depth`** (a single nesting is `depth-limited-nested` at depth 1–2 and `clean` at the default
3); the gap is recorded **per ceiling task**, so two nested images at depth 2 give two gaps; and
`depth-limited` co-occurs with `extractor-failure` and `unknown-chunk-handler`, where the draft's
precedence gives up the depth label (D3, D4).

## 1. Method, bounds, tooling

Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41C2ReconDepth` (`TMPDIR`/`HYAKU_SCRATCH` exported,
removed at yield). Artifacts
`A=.ufo/waves/round-41/w1/artifacts/R41C2ReconDepth`. Every REA run:

```
cd "$S/<case>" && npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  [--max-depth N] <carrier> "$S/<case>/rea/out"
```
with `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` absolute and PATH unchanged (`after` arm only; no
`before` arm in this recon). Harness: `A/mkdev.py` (build + run + features + labels),
`A/analyze.py` (table + invariants), `A/table-probe.py` (grammar probe, §6).

Versions (unchanged, nothing installed): REA `rea-agents@6.5.0` (npx cache), unblob `26.6.4`,
`sasquatch`/`sasquatch-v4be` `4.5.1`, Python `3.14.8`, npx `11.19.0`.

Bounds observed: no reserved image (3490/5490/5491/7560, L3/L4) and no vendor bytes were read,
hashed or opened; no round-40 C1 carrier and no held-out carrier was touched. Every carrier is a
fresh tree authored by `mkdev.py` in scratch from `sha256` counter streams, squashed with the lane
writer `tools/round-40/gen-squashfs.py` (`--endian le|be --comp gzip`), and validated with the lane
reader `tools/round-40/sqfs-list.py --layout auto` before the REA run. No VCS mutation. No subagents.
Digests: `A/hashes.txt`. Rebuild determinism: three cases rebuilt from scratch to the **same**
carrier sha256 (`sh-alone-le-d1 e0124838…`, `tw-two-le-d2 a48437bb…`, `dp-alone-be-d3 2b714618…`).

## 2. The recipe (three layers, deterministic)

```
inner   := gen-squashfs(tree{payload/hello.txt (20 B), payload/deep/leaf.bin (700 B)})
middle  := gen-squashfs(tree{mid/note.txt (12 B), inner2.sqsh = inner})      # regular file, not a link
outer   := gen-squashfs(tree{etc/banner.txt (16 B), usr/share/data.bin (2048 B),
                             inner.sqsh = middle|inner,
                             [etc/link_rel -> ../usr/share/data.bin],   # in-tree variant
                             [esc_link     -> ../outside-target],       # escaping variant
                             [damaged.sqsh], [mystery.bin], [padded.sqsh]})
```

Variants: `alone` (no link), `intree`, `escaping`, `both`; chains: `shallow` (inner has no nesting),
`deep` (outer→middle→inner, ceiling reached at the default depth), `links` (the links live one level
down inside `middle`), `two` (two nested images side by side), `partial` (a `zero-id-table` damaged
squashfs beside the deep chain, recipe imported from
`tools/round-40/heldout-gen-v2.py:524-546 corruption_zero_id_table`), `tail` (a valid squashfs with
4096 trailing random bytes → unknown chunk), `mystery` (a 4096-byte random regular file — measured to
produce **no** gap at all, see §7). 40 envelopes: 20 le / 20 be, all `ok:true`, REA exit 0, subject
digest equal to the carrier sha256.

## 3. Results

`H` is `squashfs_v4_le`/`squashfs_v4_be` matching the endianness in every row, and `D` (gap
dependencies) is `∅` in all 40 envelopes — omitted below. `d` = `--max-depth` (3 = schema default).
Ceiling paths are printed without the `$output/` prefix.

### 3a. Shallow chain (single nesting) — the depth contrast

| case | d | G | BE | SR | P | ceiling | v2 label | draft-v3 label |
|---|---|---|---|---|---|---|---|---|
| `sh-alone-le-d1` | 1 | `depth-limited` | n/a | no | 3 | `firmware.bin_extract` | unclassified | depth-limited-nested |
| `sh-alone-le-d2` | 2 | `depth-limited` | n/a | no | 5 | `firmware.bin_extract/inner.sqsh_extract` | unclassified | depth-limited-nested |
| `sh-alone-le-d3` | 3 | ∅ | n/a | no | 5 | ∅ | clean | clean |
| `sh-intree-le-d1` | 1 | `depth-limited,unpublished-entry` | n/a | no | 3 | `firmware.bin_extract` | unclassified | depth-limited-nested |
| `sh-intree-le-d2` | 2 | `depth-limited,unpublished-entry` | n/a | no | 5 | `…/inner.sqsh_extract` | unclassified | depth-limited-nested |
| `sh-intree-le-d3` | 3 | `unpublished-entry` | n/a | no | 5 | ∅ | in-tree-symlink-metadata | in-tree-symlink-metadata |
| `sh-escaping-le-d1` | 1 | `depth-limited` | n/a | yes | 3 | `firmware.bin_extract` | escaping-symlink-removed | depth-limited-nested |
| `sh-escaping-le-d2` | 2 | `depth-limited` | n/a | yes | 5 | `…/inner.sqsh_extract` | escaping-symlink-removed | depth-limited-nested |
| `sh-escaping-le-d3` | 3 | ∅ | n/a | yes | 5 | ∅ | escaping-symlink-removed | escaping-symlink-removed |
| `sh-both-le-d1` | 1 | `depth-limited,unpublished-entry` | n/a | yes | 3 | `firmware.bin_extract` | escaping-symlink-removed | depth-limited-nested |
| `sh-both-le-d2` | 2 | `depth-limited,unpublished-entry` | n/a | yes | 5 | `…/inner.sqsh_extract` | escaping-symlink-removed | depth-limited-nested |
| `sh-both-le-d3` | 3 | `unpublished-entry` | n/a | yes | 5 | ∅ | mixed-symlinks | mixed-symlinks |

The six `-be-` rows are identical with `H=squashfs_v4_be` (full table: `A/table.md`). The three
`sh-*-le-d*` rows of one variant share **one** carrier sha256 (`e0124838…`, `a639f7a6…` for
`both-be`): the same bytes score `depth-limited-nested` or `clean` purely as a function of
`--max-depth`.

### 3b. Combination and multiplicity probes

| case | d | G | BE | SR | P | ceiling(s) | v2 label | draft-v3 label |
|---|---|---|---|---|---|---|---|---|
| `dp-alone-le-d2` | 2 | `depth-limited` | n/a | no | 5 | `…/inner.sqsh_extract` | unclassified | depth-limited-nested |
| `dp-alone-le-d3` | 3 | `depth-limited` | n/a | no | 7 | `…/inner2.sqsh_extract` | unclassified | depth-limited-nested |
| `tw-two-le-d1` | 1 | `depth-limited` | n/a | no | 4 | `firmware.bin_extract` | unclassified | depth-limited-nested |
| `tw-two-le-d2` | 2 | `depth-limited` | n/a | no | 8 | `…/inner_a.sqsh_extract`, `…/inner_b.sqsh_extract` | unclassified | depth-limited-nested |
| `lk-links-le-d3` | 3 | `depth-limited,unpublished-entry` | n/a | yes | 7 | `…/inner2.sqsh_extract` | escaping-symlink-removed | depth-limited-nested |
| `pf-partial-le-d3` | 3 | `depth-limited,extractor-failure` | **no** | no | 8 | `…/inner2.sqsh_extract` | unclassified | **partial-body-failure** |
| `pf-partial-be-d3` | 3 | `depth-limited,extractor-failure` | **yes** | no | 8 | `…/inner2.sqsh_extract` | unclassified | **partial-body-failure** |
| `ta-tail-le-d3` | 3 | `depth-limited,unknown-chunk-handler` | n/a | no | 11 | `…/inner2.sqsh_extract` | unclassified | depth-limited-nested |
| `my-unknown-le-d3` | 3 | `depth-limited` | n/a | no | 8 | `…/inner2.sqsh_extract` | unclassified | depth-limited-nested |

(`-be-` twins of every row are in `A/table.md`; `my-unknown` is the negative control of `ta-tail`.)

## 4. Anatomy of the `depth-limited` gap (verbatim, `sh-alone-le-d1`)

```json
{
  "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
  "dependencies": [], "handler": null, "input_path": "$output/firmware.bin_extract",
  "kind": "depth-limited", "provider_id": null, "range": null,
  "relative_path": null, "root_file_range": null
}
```

Invariants that held on **all 32 depth-limited envelopes** (`A/analyze.py`, exit 0):

1. `input_path` is always `$output/…` and always names a **directory**: every one of the 34 ceiling
   paths ends in `_extract` (the chunk extract root, `firmware.bin_extract` at depth 1 — *not* a
   nested image name).
2. `dependencies` is always `[]`; `handler`, `provider_id`, `range`, `relative_path`,
   `root_file_range` are always `null`. No locator, so a table row cannot key on a handler or range.
3. One gap per ceiling task: `tw-two-le-d2` has two ceiling tasks and two gaps, same
   `continuation_id`. `G` is a set, so multiplicity is invisible to the feature tuple.
4. `continuation_id` is constant (`3b54e29…`) for every `max_depth < 10` — the continuation prose is
   depth-independent ([INFERENCE] from `FirmwarePublication.js:24-29`; not probed at 10).
5. `depth_limited_paths` equals the depth-limited gap paths, in sorted order, and is non-empty iff a
   depth-limited gap exists (0 mismatches in 40 cases).
6. `coverage` is `partial` whenever a depth-limited gap exists (38/40 partial; the only two
   `complete` envelopes are the resolved clean controls `sh-alone-{le,be}-d3`). Note that
   publication also forces `partial` for any unpublished entry
   (`FirmwarePublication.js:103`), so `escaping`-only envelopes are `partial` too, via the
   `MaliciousSymlinkRemoved` diagnostic.
7. **`unpublished-entry` gaps inside the ceiling directory are still reported** — `sh-intree-le-d1`
   carries the gap for `firmware.bin_extract/etc/link_rel`, which sits inside the unexamined ceiling
   dir, because publication inventories the whole staged tree. Depth-limited does not mask symlink
   gaps.

## 5. Published-but-unexamined: the one feature the label set does not carry

In every depth-limited envelope the files **under** the ceiling are published with
`reported_sha256=null` and `analysis_depth=null`, while every published file **outside** the ceiling
carries `reported_sha256 == sha256` and its `analysis_depth` (1 or 2). Measured on all 40 envelopes
(the only exemption is a carved unknown-chunk file, `/^\d+-\d+\.unknown$/`, which is never a file
task). `tw-two-le-d2` shows both sides in one envelope:

```
firmware.bin_extract/inner_a.sqsh                          rep=78098cf4… depth=1
firmware.bin_extract/inner_a.sqsh_extract/payload/hello.txt rep=null      depth=null
```

Consequence for C2: `P > 0` on a depth-limited envelope does **not** mean the published set was
analysed; the provider hash binding stops at the ceiling. Any v3 cause/action prose that says
"files were published, so the tree was walked" is wrong for this class.

## 6. Labels: v2 mislabels every combined depth-limited set; the draft v3 fixes it

- **v2 (committed interpreter + committed SKILL v2 table)**: of 32 depth-limited envelopes,
  **22 `unclassified`** and **10 `escaping-symlink-removed`** (all `escaping`/`both`/`links`
  variants — the v2 escaping row has `gap kinds = *`, so it swallows any envelope with `SR=yes`).
  v2 has no row for `depth-limited`; its `mixed-symlinks`/`in-tree-symlink-metadata` rows require
  `G` to be *exactly* `{unpublished-entry}`.
- **draft v3 (my transcription of the plan's precedence text, `mkdev.py:v3_precedence`)**:
  30 `depth-limited-nested`, 2 `partial-body-failure` (the `pf-*` pair). v2 and v3 disagree on
  exactly the 32 depth-limited envelopes and agree on the 8 others — so the draft's rule 7 is the
  whole delta, and rule 7 before rules 8/9/10 is necessary (measured: with the depth row placed
  after the symlink rows, `sh-escaping-le-d1` still reads `escaping-symlink-removed`; placed before
  `mixed-symlinks` it reads `depth-limited-nested` — `A/table-probe.txt`).

**Grammar probe (`A/table-probe.py`, `A/table-probe.txt`)** — a v3-grammar table cannot be written
in the v2 grammar:

```
novocab     exit 2  action 'raise-depth' is not declared in the vocabulary line
vocab       sh-alone-le-d1 depth-limited-nested | sh-intree-le-d1 unclassified
            sh-escaping-le-d1 escaping-symlink-removed | sh-both-le-d1 escaping-symlink-removed
            pf-partial-le-d3 unclassified
order-late  identical to vocab for all five
order-early sh-escaping-le-d1 depth-limited-nested (the other four unchanged)
```

The gap-kinds cell of the frozen interpreter is `*`, `none`, or an **exact** set
(`match_set`: `frozenset(values) == payload`, `tools/round-40/sqfs-triage-v2.py:599-605`), so only
`G == {depth-limited}` can ever match a depth row: 1/5 of the probe cases. The draft's rules are
written as membership (`∈ G`) and are inexpressible.

## 7. Defects found in the draft (attack surface for the freeze)

**D1 — the v3 action token for `depth-limited-nested` is undefined (load-bearing).**
`P41-C2` scores `(label, action)` pairs, but `## Label precedence` names labels only, and the v2
vocabulary line has no depth token (`none inspect-input install-extractor-be install-extractor-le
wrap-extractor-be preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap
confirm-empty`). Measured: a row whose action is not on the line makes the frozen interpreter exit
**2** (`line 374: action 'raise-depth' is not declared in the vocabulary line`); adding the token to
the line makes the same row parse and score. The freeze must name the token and extend the
`<!-- sqfs-triage-actions: … -->` line, or the C2 counter cannot run.

**D2 — the v3 grammar needs a `contains`/superset operator on gap kinds (load-bearing).**
Draft rules 3–8 are membership tests; the frozen cell is exact-set equality. Measured: with an
exact-set depth row placed correctly, combined sets are unreachable — `intree`→`unclassified`,
`both`→`escaping-symlink-removed`, `partial+depth`→`unclassified` (§6). The draft's kill-rule
control list already names "no contains-operator", so the author intends the operator; the draft
text must specify its cell syntax and semantics, and `P41-C2`'s "the frozen v3 interpreter, reading
only the SKILL v3 table" must acknowledge a grammar change from v2.

**D3 — `depth-limited` is unreachable under any extractor failure, and the draft does not say so.**
`pf-partial-{le,be}-d3` measure `G={depth-limited, extractor-failure}`, `P=8`; draft rule 4 fires
(`partial-body-failure`) and the depth ceiling disappears from the label. Rule 7's wording
("whatever symlink gaps accompany it") understates the reach: rule 7 also loses to rules 4/5/6.
Freeze action: state the subordination explicitly and keep `depth-limited + extractor-failure` out
of the held-out set (or expect `partial-body-failure`).

**D4 — rule 7 absorbs `unknown-chunk-handler` too, which the draft's wording excludes.**
`ta-tail-{le,be}-d3` measure `G={depth-limited, unknown-chunk-handler}` → draft rule 7 →
`depth-limited-nested`. The unknown chunk's own recovery (`inspect_firmware_regions`) is not in the
label or the action. Either the cause/action prose must say the depth gap subsumes other
non-extractor gaps, or rule 7 must be restricted to `G ⊆ {depth-limited, unpublished-entry}`.

**D5 — the held-out class list is not reproducible without a per-class `max_depth` binding.**
`heldout-gen-v2.py:run_rea` passes no `--max-depth` (schema default 3), so a depth-limited class
built with the round-40 generator machinery would score `clean` on the shallow chain — measured:
identical carrier bytes `e0124838…` give `depth-limited-nested` at depth 1–2 and `clean` at 3. The
v3 generator must bind `max_depth` per class in the manifest (and the independent evaluator must read
it), and the "two replicates" of a depth-limited class must not vary `max_depth` (that flips the
label); vary endianness/compression instead, as measured (le and be agree on all 20 paired rows).

Recommended additions to the draft's held-out class list, all measured here: `depth-limited` alone
(G={depth-limited}), `depth-limited+in-tree` (G={depth-limited, unpublished-entry}), and
`depth-limited+escaping` (G={depth-limited}, SR=yes). The third is **not** in the draft's list
("partial+in-tree, partial+mixed, depth-limited+in-tree, depth-limited+mixed, depth-limited alone")
and is the only class that discriminates a *v2-transcribed-into-v3* control for the escaping row:
measured, v2 gives `escaping-symlink-removed` for exactly that shape and draft v3 gives
`depth-limited-nested`.

## 8. Limits of this recon

- Dev images only: `gen-squashfs.py` trees (single metadata block per table, uncompressed metadata
  blocks, no fragments/xattrs), standard `le`/`be` layouts. No AVM layout, no vendor carrier.
- The depth ceiling was probed only for **squashfs-in-squashfs** (and one squashfs+unknown-tail).
  Tar/`img`/multifile nesting, `is_multi_file` dir tasks and the `-be` argv under the ceiling were
  not measured. `BE` is `n/a` in 30/32 depth-limited envelopes because a successful extraction
  records no sasquatch command; the two `no`/`yes` values come from the damaged-chunk arm
  (`pf-partial-le-d3` → `no`, `pf-partial-be-d3` → `yes`, i.e. the standard-BE handler appends `-be`).
- `depth-limited + missing-extractor-dependency` was not constructed: with `$HOME/.local/bin`
  stripped the root chunk fails first, so no ceiling is reached [INFERENCE from
  `FirmwareReports.js:229-230` + `processing.py:274`].
- `max_depth=10` (the schema ceiling) was not probed; the continuation prose branches there
  (`FirmwarePublication.js:24-29`) and the `continuation_id` would change [INFERENCE].
- A 4096-byte random regular file inside the tree produces **no** chunk and **no** gap (control
  `my-unknown-*`): unblob does not report a whole-file unknown chunk here, so an
  `unknown-chunk-handler` gap needs a file that also carries a valid chunk (`ta-tail`).

## 9. Files

Artifacts `A=.ufo/waves/round-41/w1/artifacts/R41C2ReconDepth/`:

| file | content |
|---|---|
| `mkdev.py` | carrier recipes + REA driver + feature/label recording (sha256 in `hashes.txt`) |
| `analyze.py` | table renderer + the seven invariants of §4/§5 (exit 0 on all 40) |
| `table-probe.py`, `table-probe.txt` | the §6 grammar probe and its output |
| `summary.json` | 40 case records: features, gaps verbatim, published list, chunks, diagnostics, labels |
| `table.md` | full 40-row table |
| `evidence.md` | verbatim envelope excerpts for 11 representative cases |
| `envelopes/<case>/envelope.json` | the `data` object the v2 interpreter read (40 files, ~1.2 MB total) |
| `hashes.txt` | lane-tool digests, artifact digests, per-case carrier sha256 |

Lane tool digests read (unmodified): `gen-squashfs.py 309c502d…`, `sqfs-list.py 1079fa9b…`,
`sqfs-triage-v2.py 336c621c…`, `heldout-gen-v2.py 644d8f6e…`, `SKILL.md 926dac30…`.
Source lines cited: `rea-agents/dist/firmware/FirmwareProvider.js:230-232` (`--depth
max_depth`), `FirmwareReports.js:229-230` (`depth >= maxDepth` → `depths.push`), `:384`
(`depth_limited_paths`), `:419-423` (`coverage`), `FirmwarePublication.js:294-300` (the gap row),
`:264-270` (continuation id); `unblob/processing.py:274` (the stop), `:683-686` (extract-dir task at
`depth+1`), `:440-478` (directory subtasks keep the parent's depth), `extractor.py:50-113`
(`fix_symlink`/`fix_extracted_directory`).

Tooling record: **nothing installed or upgraded**; no pacman transaction, no `~/.local/bin` write.
