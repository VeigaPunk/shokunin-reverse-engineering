# R40C2ReconMixed — mixed-symlink class and interplay (round 40 wave 1, development recon)

**Verdict: CONFIRMED.** A `mixed-symlinks` row is separable on the frozen feature set and must precede the
escaping row; six fresh BE/LE mixed carriers, the two round-39 mixed Core carriers (K5/K6), and twelve
interplay probes all resolve under one row order. Five draft constraints must be written into the freeze,
and eight vector combinations must be excluded from the held-out set as ambiguous or already owned by
another row.

Seat: `R40C2ReconMixed` (leaf). Item: C2 recon for the mixed-symlinks class and interplay. Nothing here is
frozen; the L1 integrates. No carrier, held-out envelope, or C1 input was run with REA/unblob: all REA runs
are on fresh trees authored in scratch by `mkdev.py` (BE/LE `gen-squashfs.py` builds), on damaged copies of
those trees, and on read-only round-39 development envelopes. No `V1`/`V2`/`L1`/`L2` C1 carrier and no C2
held-out carrier was built, opened with REA, or touched.

## 1. Method and exact invocation

Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40C2ReconMixed` (`TMPDIR`, `WORK`), removed at yield. Artifacts
`A=.ufo/waves/round-40/w1/artifacts/R40C2ReconMixed`. Every REA run:

```
export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
cd "$WORK/<name>-<arm>" && npx -y rea-agents@6.5.0 extract-firmware --format json \
  --full-output <carrier> "$WORK/<name>-<arm>/out"
```

`after` arm = PATH unchanged; `before` arm = `$HOME/.local/bin` removed from the child PATH with
`REA_UNBLOB_COMMAND` kept absolute (`run.json: home_bin_on_path false`). All 21 runs exited 0 and printed a
parseable `{ok,data,meta}` envelope. Tools (no installs; nothing upgraded): `rea-agents@6.5.0` from the npx
cache, `unblob` 26.6.4, `sasquatch`/`sasquatch-v4be` 4.5.1, Python 3.14 stdlib. Commands: `commands.md`.
Feature reads: `feat.py` (independent re-implementation of v1 `features()` plus v2 extras). Row-order
counterfactuals: `ordercheck.py --table A|B|C`. Feature table: `feature-table.md`; digests: `hashes.txt`.

Carriers were validated byte-level with the lane's independent reader (`tools/round-39/sqfs-list.py`) before
any REA run; `dev-carriers/*/symlinks.tsv` are its classifications.

## 2. Item (1) — mixed carriers: G={unpublished-entry}, SR=yes, P>0, on BE and LE

Six authored trees, three shapes × two endiannesses. Shapes vary the escaping link position (root vs
subdirectory), the in-tree target (same dir, sibling dir, file in another subtree), and the link count
(1+1, 1+1, 2+2). `mx1`/`mx4` share a tree shape across endian, `mx2`/`mx5` and `mx3`/`mx6` likewise; each is a
separate build of a freshly created tree.

| run | carrier | endian/comp | tree links (sqfs-list) | H | G | D | BE | SR | P |
|---|---|---|---|---|---|---|---|---|---|
| `mx1-after` | sha `33de8689…` | be/gzip | `esc`→`../outside-target` (escaping), `d1/ini`→`../a.txt` (in-tree) | `squashfs_v4_be` | `unpublished-entry` | ∅ | `n/a` | `yes` | 3 |
| `mx2-after` | sha `40317258…` | be/xz | `d1/up`→`../../outside2` (escaping), `d2/i1`→`../d1/c.txt` (in-tree) | `squashfs_v4_be` | `unpublished-entry` | ∅ | `n/a` | `yes` | 3 |
| `mx3-after` | sha `8638e7e1…` | be/gzip | `e1`→`../x`, `e2`→`../y` (escaping), `d2/i1`→`../b.txt`, `d2/i2`→`../d1/c.txt` (in-tree) | `squashfs_v4_be` | `unpublished-entry` | ∅ | `n/a` | `yes` | 4 |
| `mx4-after` | sha `719c78a3…` | le/gzip | same shape as mx1 | `squashfs_v4_le` | `unpublished-entry` | ∅ | `n/a` | `yes` | 3 |
| `mx5-after` | sha `090290eb…` | le/xz | same shape as mx2 | `squashfs_v4_le` | `unpublished-entry` | ∅ | `n/a` | `yes` | 3 |
| `mx6-after` | sha `f9c77752…` | le/gzip | same shape as mx3 | `squashfs_v4_le` | `unpublished-entry` | ∅ | `n/a` | `yes` | 4 |

Observations that the row must encode:

- **One gap kind regardless of link count.** Two in-tree links produce two `extraction_gaps` entries but the
  set `G` stays `{unpublished-entry}`; the per-link count is not in the frozen feature set (`mx3`, `mx6`).
- **The escaping link leaves no gap.** `G` is exactly `{unpublished-entry}`, never `{unpublished-entry, …}`;
  the removal appears only as `diagnostics[].report.__typename__ == MaliciousSymlinkRemoved` (`SR=yes`).
- **`D` is empty and `BE` is `n/a`.** A successful extraction records no sasquatch command at all
  (`feat.py: commands []`), so `-be in child argv` is `n/a`, not `yes`. A row that required `BE=yes` would never
  match a mixed envelope.
- **`unpublished_entries[].kind` is `symlink`** for every gap, one entry per in-tree link.
- Endian is not a decision feature for the label: only `H` changes (`_be`/`_le`), so the mixed row needs the
  endian-agnostic handler pattern the v1 symlink rows already use (`squashfs_v4_*`).

Round-39 confirms the same signature on real mixed Core carriers: `corpus/evidence/round-39/c1/K5/after.json`
(`G={unpublished-entry}`, `SR=yes`, `P=10`, one diagnostic, two unpublished symlinks) and `K6/after.json`
(`G={unpublished-entry}`, `SR=yes`, `P=8`, two diagnostics, one unpublished symlink). Their oracles name
one escaping and two in-tree links (K5) and two escaping and one in-tree link (K6).

## 3. Item (2) — mixed + sasquatch unreachable: the dependency gap masks every symlink feature

| run | arm | H | G | D | BE | SR | P | chunk `extraction_failed` | diagnostics |
|---|---|---|---|---|---|---|---|---|---|
| `mx1-before` | PATH minus `~/.local/bin` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | 0 | true | `ExtractorDependencyNotFoundReport` |
| `mx4-before` | same | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | 0 | true | `ExtractorDependencyNotFoundReport` |

Yes: the mask is total. No extractor ran, so unblob never walked the tree: no `unpublished-entry` gap, no
`MaliciousSymlinkRemoved`, no published file. The envelope is feature-identical to a symlink-free dep-missing
carrier, down to the gap dependency token (`sasquatch-v4be` for BE, `sasquatch` for LE). A mixed tree can
therefore never be scored as `mixed-symlinks` in the before arm; it scores `dep-missing-*`, which is the
correct row for the envelope but the wrong class for a held-out replicate. Exclude this cross (§7).

## 4. Item (3) — mixed + body damage: full failure masks, partial failure does not

Five damages applied to mixed carriers:

| run | damage | H | G | D | BE | SR | P | chunk failed | resulting row |
|---|---|---|---|---|---|---|---|---|---|
| `mx1-idtable-after` | zero id-table metadata block | `squashfs_v4_be` | `extractor-failure` | ∅ | `yes` | `no` | 0 | true | `body-extractor-failure` |
| `mx1-badminor-after` | `s_minor` 4→5 (handler still matches) | `squashfs_v4_be` | `extractor-failure` | ∅ | `yes` | `no` | 0 | true | `body-extractor-failure` |
| `mx8-flip-after` | XOR 16 B of the last data block | `squashfs_v4_be` | `extractor-failure` | ∅ | `yes` | `no` | 0 | true | `body-extractor-failure` |
| `mx1-avm-after` | `--endian avm` (marker-only standard BE) | `squashfs_v4_be` | `extractor-failure` | ∅ | `no` | `no` | 0 | true | `avm-marker-be-dropped` |
| `mx8-zerofirst-after` | zero first 16 B of the first compressed data block | `squashfs_v4_be` | `extractor-failure`+`unpublished-entry` | ∅ | `yes` | `yes` | 3 | true | **no row** (`unclassified`) |
| `mx7-zerofirst-after` | same damage on a raw (uncompressed) first block | `squashfs_v4_be` | `unpublished-entry` | ∅ | `n/a` | `yes` | 3 | false | `mixed-symlinks` (damage was inert) |
| `mx7-trunc-after` | truncate 18 466 B image to 9 000 B | ∅ | ∅ | ∅ | `n/a` | `no` | 0 | – | `no-squashfs-chunk` |
| `mx7-trunc2-after` | truncate to 18 400 B | ∅ | ∅ | ∅ | `n/a` | `no` | 0 | – | `no-squashfs-chunk` |

What survives:

- **Full failure destroys all symlink evidence.** sasquatch exits before unblob fixes symlinks, so `SR=no` and
  the in-tree gap is absent. The envelope collapses onto the existing body-failure (or AVM-marker) row; the
  damage, not the tree, decides the label. This is safe for scoring and wrong for a mixed held-out replicate.
- **Partial failure keeps both symlink features.** `mx8-zerofirst` publishes 3 files (`P=3`) *after*
  `zero-first-data` breaks one compressed data block, and unblob still processes the tree: `G` becomes the
  two-kind set `{extractor-failure, unpublished-entry}`, `SR=yes`, and one unpublished symlink is listed. The
  exact-set row grammar then matches **no** row (the body rows require `G={extractor-failure}`, the mixed row
  requires `G={unpublished-entry}`). This is the one mixed-plus-damage combination that must be excluded, not
  relied on.
- **The damage recipe, not just the damage kind, decides `P`.** Zeroing the last data block (`mx8-flip`) and
  zeroing the id table (`mx1-idtable`) both abort with `P=0`; zeroing the first compressed block
  (`mx8-zerofirst`) publishes files. Round-39 development evidence shows the same split on symlink-free trees:
  `ta-v5-corrupt-block-length` and `tc-v2-zero-first-data-block` (`P=3`, `SR=no`) versus
  `full-be1-xz` (`P=6`) — all `G={extractor-failure}`. `rea-TA-be-xz` (round-39) is the symlink-free-tree
  analogue of partial damage with in-tree links only: `G={extractor-failure, unpublished-entry}`, `SR=no`,
  `P=5`, also with no matching row.
- **Raw data blocks are unchecksummed.** `mx7-zerofirst` zeroed the first data block of an incompressible
  tree and extraction still succeeded (`chunk extraction_failed=false`); the same bytes in a zlib-compressed
  block fail. A "partial body failure" held-out recipe must corrupt a *compressed* block, otherwise it
  silently produces the clean/mixed row.
- **Truncation is not body damage here.** Both truncated images lose the chunk entirely (`H=∅`), so they land
  on `no-squashfs-chunk`; unblob does not run a handler whose computed range exceeds the file.

## 5. Item (4) — escaping-only and in-tree-only on LE

| run | tree links | H | G | D | BE | SR | P | diagnostics |
|---|---|---|---|---|---|---|---|---|
| `esc-le-after` | `esc`→`../outside-target` only | `squashfs_v4_le` | ∅ | ∅ | `n/a` | `yes` | 2 | `MaliciousSymlinkRemoved` |
| `intree-le-after` | `d1/ini`→`../a.txt` only | `squashfs_v4_le` | `unpublished-entry` | ∅ | `n/a` | `no` | 2 | — |

Both match the v1 symlink rows, which already use `squashfs_v4_*` (verified by reading the committed table,
`SKILL.md:333-343`, and by labelling them with `tools/round-39/sqfs-triage.py --skill SKILL.md`: exit 0,
`escaping-symlink-removed` and `in-tree-symlink-metadata`). The escaping row's v1 cells are `gap kinds=*`,
`dependencies=*`; that is exactly why v1 mislabels mixed envelopes (§6).

## 6. v1 mislabels mixed envelopes — R39-CL2 reproduced

```
python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md \
  rea/mx1-after/envelope.json … rea/mx6-after/envelope.json \
  corpus/evidence/round-39/c1/K5/after.json corpus/evidence/round-39/c1/K6/after.json
→ escaping-symlink-removed   (all eight; exit 0)
```

Cause: the v1 escaping row matches `handler squashfs_v4_*`, `gap kinds *`, `dependencies *`, `SR=yes`, `P>0`,
so a mixed envelope stops there and its `unpublished-entry` gap is never read. `ordercheck.py --table C`
reproduces the same mislabel with a v2 table that keeps v1's `*` gap/dependency cells *and* puts escaping
before mixed (`mx1`, `mx4`, `K5` → `escaping-symlink-removed`, rule 7). Two consequences for the freeze:

1. Mixed must be its own row **and** ahead of the escaping row (draft wording is right);
2. the escaping row must be tightened to `gap kinds=none`, `dependencies=none`. With exact sets, row order
   between mixed and escaping stops mattering for correctness (verified: table A with exact cells still
   resolves every mixed and escaping envelope), but a `*` escaping row placed first breaks mixed — so keep
   both the order and the exact cells. Keeping the exact cells also prevents an escaping row from swallowing
   any future envelope that carries an unrelated gap.

## 7. Proposed v2 row order that resolves every measured combination

Actions vocabulary (one token per row; declared above the table):

```
<!-- sqfs-triage-actions: install-extractor rerun-fresh rerun-fresh-partial expect-absent expect-absent-metadata repin-marker inspect-chunk ignore-benign -->
```

Every row pins the domain columns; verified that REA really emits `data.operation="extract_firmware"`,
`data.provider.id="unblob"`, `data.provider.name="Unblob"`, `data.provider.version="26.6.4"` on all 21 runs.
Use `provider.id`, not the display name.

| # | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `no-squashfs-chunk` | `extract_firmware` | `unblob` | `none` | `*` | `*` | `n/a` | `*` | `*` | `inspect-chunk` |
| 2 | `dep-missing-be` | `extract_firmware` | `unblob` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` | `install-extractor` |
| 3 | `dep-missing-le` | `extract_firmware` | `unblob` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` | `install-extractor` |
| 4 | `avm-marker-be-dropped` | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` | `repin-marker` |
| 5 | `body-extractor-failure` | `extract_firmware` | `unblob` | `squashfs_v4_be` | `extractor-failure` | `none` | `yes` | `no` | `0` | `rerun-fresh` |
| 6 | `partial-body-failure` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `extractor-failure` | `none` | `yes` | `no` | `>0` | `rerun-fresh-partial` |
| 7 | `mixed-symlinks` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `yes` | `>0` | `expect-absent-metadata` |
| 8 | `escaping-symlink-removed` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `yes` | `>0` | `expect-absent` |
| 9 | `in-tree-symlink-metadata` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` | `ignore-benign` |
| 10 | `clean` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `>0` | `ignore-benign` |
| 11 | `clean-empty` | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `0` | `ignore-benign` |

`cause`/`source` columns omitted here only for width; the implementer transcribes them per row.

Resolutions measured with `ordercheck.py --table A` (35 envelopes: 21 dev runs, K1–K6, six round-39 dev
envelopes, two synthetic domain violations; 7 are `unclassified`, exactly the excluded combinations
plus the two domain violations):

| combination | measured evidence | row | correct? |
|---|---|---|---|
| mixed, undamaged, after arm, BE gzip/xz, 1–2 links each | mx1/mx2/mx3, K5/K6 | 7 `mixed-symlinks` | yes |
| mixed, undamaged, after arm, LE gzip/xz | mx4/mx5/mx6 | 7 `mixed-symlinks` | yes |
| escaping only, BE and LE | K1, `esc-le` | 8 `escaping-symlink-removed` | yes |
| in-tree only, BE and LE | K2, `intree-le` | 9 `in-tree-symlink-metadata` | yes |
| clean, P>0 | K3/K4 | 10 `clean` | yes |
| clean, P=0 (empty directory) | `dironly`; round-39 `full-be-dirempty-gzip` | 11 `clean-empty` | yes |
| mixed + dependency missing | `mx1-before`, `mx4-before` | 2/3 `dep-missing-*` | yes (masked) |
| mixed + AVM marker | `mx1-avm` | 4 `avm-marker-be-dropped` | yes (masked) |
| mixed + full body failure (id-table, bad-minor, last-block) | `mx1-idtable`, `mx1-badminor`, `mx8-flip` | 5 `body-extractor-failure` | yes (masked) |
| partial body failure, symlink-free tree | round-39 `ta-v5`, `tc-v2`, `full-be1-xz` | 6 `partial-body-failure` | yes |
| truncated image | `mx7-trunc`, `mx7-trunc2` | 1 `no-squashfs-chunk` | yes |
| non-`extract_firmware` operation | `synth/op-changed.json` | none | `unclassified` (domain guard) |
| non-`unblob` provider | `synth/prov-changed.json` | none | `unclassified` (domain guard) |
| mixed + partial body failure | `mx8-zerofirst` | none | **unclassified** — exclude |
| mixed with zero regular files | `mx-nofiles` | none | **unclassified** — exclude |
| partial body failure + in-tree only | round-39 `rea-TA-be-xz` | none | **unclassified** — exclude |
| LE body failure, full **or** partial | `mx4-idtable`, round-39 `full-le1-xz` | none | **unclassified** — decide (§8) |

Ordering constraints and why:

- Row 1 first: it has `handler=none` and `published=*`; with every later row pinning a handler pattern an
  `H=∅` envelope cannot reach them, so this is not strictly required today — it is required the moment any
  later row uses a `*` handler, and it is v1's demonstrated order. Keep it first.
- Rows 2–3 before 4–6 is conventional, not forced: the dependency gap kinds are unique sets.
- Row 4 before 5–6: forced only if 5–6 used `-be=*`; with `yes` they are disjoint from the AVM row's `no`,
  but keeping the AVM row first is the safe invariant.
- Row 7 before 8: **required while row 8 keeps v1's `*` gap/dependency cells** (table C mislabels), harmless
  once row 8 is `none/none` (table A still resolves). Both changes together are the robust form.
- Rows 10/11 last; their `0`/`>0` cells are disjoint.

## 8. What the freeze must state (concrete draft changes)

1. **Mixed row cells.** `handler=squashfs_v4_*`, `gap kinds=unpublished-entry`, `dependencies=none`,
   `-be=n/a`, `symlink removed=yes`, `published=>0`. Not `squashfs_v4_be` (would lose LE) and not
   `-be=yes` (a successful extraction records no sasquatch command, so `BE` is `n/a`).
2. **Replicate variation for `mixed-symlinks`.** Use two replicates that differ in a non-decision feature:
   endian and/or compression. Measured pairs that both resolve to row 7: `mx1` (be/gzip) vs `mx4` (le/gzip),
   `mx2` (be/xz) vs `mx5` (le/xz), `mx3` vs `mx6` (link counts). Endian-differing replicates are only safe
   because the row's handler is `squashfs_v4_*` — state that dependency in the claims.
3. **Held-out generation constraints** (bound the generator recipes, not the table):
   mixed class = undamaged body, after arm, ≥1 escaping **relative** link that climbs above the root, ≥1
   in-tree link, ≥1 regular file. Escaping targets must be relative with `..` — an absolute target is
   stripped of its leading `/` by unblob and kept as in-tree metadata [INFERENCE from
   `S118 extractor.py:79-91`, not measured here].
4. **`partial-body-failure` recipe.** Its tree must contain **no symlinks** (otherwise `G` gains
   `unpublished-entry` and the envelope is unclassified), and the corruption must break a *compressed*
   block after some files are publishable (`zero-first-data`-style). `zero-id-table`, `bad-minor` and last-block
   damage all yield `P=0` and belong to `body-extractor-failure`.
5. **Decide LE damage.** `mx4-idtable` (LE zero-id-table) and round-39 `full-le1-xz` (LE partial) are
   measured, in-domain envelopes that the draft's rows leave `unclassified`: LE failures record
   `sasquatch -le …`, so `-be=no` and the row-5/6 `-be=yes` cell cannot match. Either add
   `body-extractor-failure-le` / `partial-body-failure-le` rows (`handler=squashfs_v4_le`, `-be=no`,
   `symlink removed=no`) — which changes the label count — or declare LE damage out of the held-out set and
   accept `unclassified`. Do not leave this implicit in the class list.

## 9. Exclusions from the held-out set (ambiguous or already owned)

| combination | why exclude |
|---|---|
| mixed × dependency missing (before arm) | gap masks both symlink features; scores `dep-missing-*`; indistinguishable from a symlink-free carrier |
| mixed × AVM marker | `-be` dropped, sasquatch fails endianness; scores `avm-marker-be-dropped`, no symlink signal |
| mixed × full body failure (`P=0`) | scores `body-extractor-failure`; no symlink signal (safe for scoring, wrong for the class) |
| mixed × partial body failure | two-kind `G` matches no row → `unclassified`; `mx8-zerofirst` measured |
| escaping/in-tree × partial body failure | same two-kind `G`; round-39 `rea-TA-be-xz` measured `G={extractor-failure, unpublished-entry}`, `SR=no` |
| LE full or partial body failure | no matching row (draft), measured unclassified unless §8.5 adds rows |
| mixed with zero regular files | `P=0` fails the mixed row's `>0` and row 9's `>0`; measured `mx-nofiles`: `G={unpublished-entry}`, `SR=yes`, `P=0` → `unclassified` |
| carriers with non-symlink `unpublished-entry` kinds (hardlink/special) | `G` alone cannot distinguish them from symlink metadata; the frozen grammar has no unpublished-kind column. No round-40 class needs them — keep the held-out entries symlink-only [INFERENCE: no such carrier measured] |

## 10. Writer and vector hazards found while building the probes

- **`tools/round-39/gen-squashfs.py` silently drops symlinks to directories.** `os.walk` puts a
  directory-target symlink in `dirnames`, and the writer serialises only `fnames`. Measured: a tree with
  `a.txt`, `d1/`, `inlink→d1` produced a 255 B image with 3 inodes (root + `d1` + `a.txt`) and **0** symlinks,
  no warning (`dev-carriers/dirlink/`). The first `mx2`/`mx5` builds authored `inlink→d1` and came out with
  only the escaping link (the independent reader showed `in_tree_symlinks: 0`); they were rebuilt with a
  file-target in-tree link before any REA run. `heldout-gen.py`'s `build_tree` only targets regular files, so
  today's recipes are safe, but any future mixed recipe that picks a directory target degenerates to an
  escaping-only carrier (`G=∅`, `SR=yes`), which scores `escaping-symlink-removed` and would silently break a
  frozen `mixed-symlinks` label rather than fail loudly. State the constraint in the held-out generator
  notes; do not change frozen bytes.
- **A bare-empty root is not writable as a valid image.** `gen-squashfs.py` on an empty root emits a 146 B
  image whose zero-length metadata block the independent reader rejects (`sqfs-list: zero-length metadata block
  at 130`, exit 2). A tree holding one empty directory (`dironly`) is valid and is the clean-empty vector used
  here (`P=0`). The round-39 `be-dirempty` recipe uses exactly that shape.
- **Raw data blocks carry no checksum.** Damage applied to an uncompressed block is a no-op (`mx7-zerofirst`
  succeeded). Damage recipes must target compressed blocks to force a failure.

## 11. Evidence inventory

All under `A=.ufo/waves/round-40/w1/artifacts/R40C2ReconMixed/`; sha256 for every file in `hashes.txt`.

- `dev-carriers/<name>/`: `carrier.sqsh`, `build.json` (endian, compression, exact argv, tree listing,
  symlink kinds), `files.tsv`, `symlinks.tsv`, `inspect.txt` (independent reader).
- `envelopes/<run>/`: `envelope.json` (full `{ok,data,meta}`) + `run.json` (arm, exit code, argv,
  `home_bin_on_path`). 21 runs, all exit 0, all parsed.
- `synth/op-changed.json`, `synth/prov-changed.json`: domain-guard envelopes derived from `mx1-after`.
- `feature-table.md` (per-run features + v2A decision), `order-A.txt`, `order-B.txt`, `order-C.txt`.
- Tools: `feat.py`, `mkdev.py`, `corrupt.py`, `runrea.sh`, `ordercheck.py`.
- `commands.md`: exact build/damage/run/read commands.

Carrier digests cited above (`sha256[:8]`): mx1 `33de8689`, mx2 `40317258`, mx3 `8638e7e1`, mx4 `719c78a3`,
mx5 `090290eb`, mx6 `f9c77752`, mx1-avm `855b4702`, mx1-idtable `89feba7b`, mx1-badminor `bf43b581`,
mx4-idtable `b37be52a`, mx8-zerofirst `d74badae`, mx-nofiles `1374042b`, mx7-trunc `add06b84`,
dironly `65886123`, dirlink `c47dcf92`. Envelopes: e.g. `mx8-zerofirst-after` `30532abc`,
`mx1-avm-after` `5c0fe36c`, `mx-nofiles-after` `67f06217`.

## 12. Limits and inference

- All numbers are development carriers built by the lane writer; they characterise the frozen features, not
  any vendor image. No V1/V2 member and no C1 carrier was opened.
- `[INFERENCE]` absolute symlink targets are in-tree under unblob's `fix_symlink` (from the `sqfs-list.py`
  doc and S118 lines): used only to constrain held-out generation; not measured here.
- `[INFERENCE]` non-symlink `unpublished-entry` kinds would alias the mixed/in-tree rows; no such envelope was
  built.
- The v2 interpreter's table parsing, exit-2 behaviour, and its own selftest are not exercised here; this
  report fixes the row order and the feature semantics the interpreter must reproduce (`ordercheck.py` is a
  recon prototype with hard-coded rows, not the frozen interpreter).
- The round-39 `heldout-gen.py` `corruption_bad_minor` docstring erratum noted in the round-39 closure is
  consistent with my measurement (it yields a matching handler plus `extractor-failure`, not a missing
  chunk); my `corrupt.py` docstring states the measured behaviour.
