# R41C2Gen — v3 held-out generator for round-41 R41-C2 (combined classes, seeded factorial family, per-class depth, R40-CL4 pin)

**Verdict: DONE** — `heldout-gen-v3.py` carries the 13 frozen v2 classes, the five combined
classes, the two L1-amendment classes and the 12-carrier seeded factorial family `combo`
(**52 carriers**). Every carrier records the six-field **declared** tuple the counter binds as
`observed_features_match_declared`; `class_expected` is reported only (null for combos). On the dev
seed `sha256("dev41") = c9e30c10…` all 52 envelopes hit their declared tuple
(`exit 0`, `52/52 carriers reached their declared tuple`), and the checker is red when it should be
(two kept red runs: 32/36 on a wrong dependency expectation, 50/52 on a recipe regression).

Seat `R41C2Gen`, leaf. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`49096c7e6f226af0c750c4b003be58883cb6049f`. Wrote only
`.ufo/waves/round-41/w1/R41C2Gen.md` and `.ufo/waves/round-41/w1/artifacts/R41C2Gen/`. No VCS
mutation (read-only `git show`), no subagent, no `agent://all`. REA ran only through its CLI, only
on carriers this seat built with the lane's own writer; no reserved image, no vendor image, no
vendor member was opened, fetched or copied (no vendor byte exists in any artifact). No tool
installed, upgraded or moved; `pacman` untouched. Scratch
`/fast/scratch/hyaku/kaidoku-r41/R41C2Gen` removed at exit — everything cited is in the artifacts dir.

---

## 1. Deliverables

| file | sha256 / note |
|---|---|
| `artifacts/R41C2Gen/heldout-gen-v3.py` | `698db75f4204734a811a5d603fff6b985557a99f8d905f9cbae40fc67416c9d2` — stdlib only; `--seed --out --run --verify --selftest --classes --actions-set --actions-file --gen --scratch --gzip` |
| `artifacts/R41C2Gen/dev-seed-c9e30c10/manifest.json` | `3cc2565e534f894bfce392820fa27158ce581e74863d90235f7aab82aceb9f03` — 20 named classes + the `combo` family, `declared` per carrier, `declared_schema`, `rea.per_class`, `families` |
| `artifacts/R41C2Gen/dev-seed-c9e30c10/H01..H40, C01..C12/` | per carrier `carrier.sqsh`, `envelope.json`, `run.json`, `tree.json` — 52 carriers, each ≤ 134 KB (carriers 1.8 MB, whole set 3.4 MB); `rea-full.json` (the duplicate `{ok,data,meta}` wrapper) is omitted, it is `--run` output and `ok`/`duration` are in `run.json` |
| `artifacts/R41C2Gen/dev-feature-table.md` | the 52-row observed-vs-declared table |
| `artifacts/R41C2Gen/dev-combo-factors.md` | the 12 factor draws, declared tuples, and the "outside the named tuples" verdict |
| `artifacts/R41C2Gen/dev-run.log` | final `--run --verify`, exit 0, 52/52 |
| `artifacts/R41C2Gen/dev-run-first-attempt.log` | red run: 32/36, exit 1 (`dep-missing-*`: `extraction_failed` want False got True) |
| `artifacts/R41C2Gen/dev-run-clean-empty-regression.log` | red run: 50/52, exit 1 (`clean-empty` published want `zero` got `nonzero` — caught a real recipe regression, §6 F7) |
| `artifacts/R41C2Gen/selftest.log` | 12/12 checks, exit 0 |
| `artifacts/R41C2Gen/pin-check.py` + `partial-pin-red.txt` | R40-CL4 pin: refuses a 1762 B target, accepts a 77 B one |
| `artifacts/R41C2Gen/depth-control/H31-depth3.json`, `H33-depth3.json` | the depth-limited carriers re-run at `--max-depth 3` |
| `artifacts/R41C2Gen/action-vocab/` | `--actions-file` bind: exit 1 on the round-40 SKILL line, exit 0 on a v3-shaped line |
| `artifacts/R41C2Gen/lineage/` | v2 vs v3 carrier bytes on the same seed (`21/26` identical) |
| `artifacts/R41C2Gen/run-dev.sh`, `env.txt` | one-command reproduction; host/extractor versions |
| `artifacts/R41C2Gen/check-delivered.py` + `check-delivered.txt` | independent re-read of the delivered set (manifest + envelope + run only, no generator): `52/52 carriers: observed == declared`, exit 0 |

Environment: Linux 7.2.11-arch1-1, Python 3.14.8, node v24.21.0, unblob 26.6.4,
sasquatch/sasquatch-v4be 4.5.1, REA `rea-agents@6.5.0` via `npx -y`; writer
`tools/round-40/gen-squashfs.py` sha256 `309c502d…29042e` (pinned in the manifest).

## 2. What the manifest declares (the binding the counter reads)

```
manifest.carriers[i].declared =
  {handler_set, gap_kinds, gap_dependencies, be_argv, symlink_removed, published}
manifest.carriers[i].declared_extras = {extraction_failed, max_depth}      # not part of the binding
manifest.carriers[i].class_expected  = {label, action, reported_only: true, features}
manifest.declared_schema              # field names, types, and where they live
```

* `be_argv` is `yes`/`no`/`n/a`, never a boolean: `n/a` means **no extractor child argv was
  recorded** (a successful run records none). unblob 26.6.4
  `handlers/filesystem/squashfs.py:30-42` appends `-be` for a big-endian v4 image **unless**
  `mkfs_time == bytes_used`, and `-le` for little-endian.
* `published` is `nonzero` / `zero` (the P-class), not a count.
* `handler_set` is empty when no chunk carries a handler (`no-squashfs-chunk`, `out-of-domain`).
* `gap_kinds` / `gap_dependencies` are sorted sets.
* For `combo` carriers `class_expected` is **null** by design: the evaluator alone names the label.

Every `run.json` repeats `declared`, `declared_extras`, `factors` and `class_expected`, so the
counter can bind from either the manifest or a single receipt.

## 3. The named classes (20 × 2 replicates = 40 carriers)

The 13 v2 recipes are unchanged except where R40-CL4 requires it. New axes: `rea={'max_depth': n}`
(3 for v2 classes, 1 for the depth-limited ones; passed explicitly and re-appearing as the
envelope's `parameters.max_depth`), `nested=True` (a real LE SquashFS image written into the tree),
`layout='two-chunk'`, `link_placement='root-first'`.

| class | build | declared tuple (both replicas unless stated) | label under the precedence text | the trap |
|---|---|---|---|---|
| `clean-be` | BE, stream | H `{…_be}`, G ∅, BE n/a, P>0 | clean | — |
| `clean-le` | LE, stream | H `{…_le}`, G ∅, P>0 | clean | — |
| `clean-empty` | empty tree (P must stay 0) | H per endian, G ∅, P **zero** | clean-empty | a fill rule must not touch it (§6 F7) |
| `escaping-symlink-removed` | + escaping link | G ∅, **SR yes**, P>0 | escaping-symlink-removed | v2's row matched `G=*`, so it swallowed everything (§6 F5) |
| `in-tree-symlink-metadata` | + in-tree link | G `{unpublished-entry}`, SR no | in-tree-symlink-metadata | — |
| `mixed-symlinks` | both links | G `{unpublished-entry}`, SR yes | mixed-symlinks | SR alone must not decide |
| `dep-missing-be` | `before` arm (no ~/.local/bin) | G `{missing-extractor-dependency}`, D `{sasquatch-v4be}`, P 0, **failed** | dep-missing-be | a dependency gap also marks the chunk failed (§6 F1) |
| `dep-missing-le` | same, LE | D `{sasquatch}`, P 0, failed | dep-missing-le | — |
| `avm-marker-be-dropped` | BE + `mkfs_time==bytes_used` | G `{extractor-failure}`, P 0, **BE no** | avm-marker-be-dropped | only the argv separates it from the next row |
| `body-extractor-failure` | BE, id table zeroed | G `{extractor-failure}`, P 0, **BE yes** | body-extractor-failure | see above |
| `partial-body-failure` | BE, pattern, `partial` | G `{extractor-failure}`, P>0, BE yes | partial-body-failure | R40-CL4 pin |
| `no-squashfs-chunk` | `s_major` 4→9 | H ∅, G ∅, P 0 | no-squashfs-chunk | — |
| `out-of-domain` | `inspect-firmware-regions` | OP ≠ extract_firmware | unclassified | domain guard |
| **`partial-in-tree`** | above + root-first in-tree link | G `{extractor-failure, unpublished-entry}`, SR no, P>0, BE yes | partial-body-failure (rule 4) | a table matching the symlink row loses |
| **`partial-mixed`** | above + escaping link | same G, **SR yes**, P>0 | partial-body-failure (rule 4 before 8) | as above, and SR is not decisive |
| **`depth-limited-alone`** | nested image, depth 1 | G `{depth-limited}`, P>0, BE n/a | depth-limited (rule 7) | a table with no depth row says clean |
| **`depth-limited-in-tree`** | + in-tree link | G `{depth-limited, unpublished-entry}`, SR no | depth-limited (rule 7 before 10) | — |
| **`depth-limited-mixed`** | + both links | G `{depth-limited, unpublished-entry}`, SR yes | depth-limited (rule 7 before 8) | — |
| **`body-extractor-failure-le`** *(amendment)* | LE, id table zeroed | H `{…_le}`, G `{extractor-failure}`, P 0, **BE no** | body-extractor-failure (rule 6) | rule 5 names `squashfs_v4_be`: a table that drops the handler column labels this avm-marker-be-dropped |
| **`failure-depth-limited`** *(amendment)* | two chunks: empty image at 0 (depth ceiling) + id-table-zeroed image at 4096, depth 1 | G `{depth-limited, extractor-failure}`, P **nonzero**, BE yes/no | partial-body-failure (rule 4) | a table with the depth step before the failure steps says depth-limited |

The label `depth-limited-nested` is renamed to `depth-limited` everywhere (L1 amendment).

## 4. The seeded factorial family `combo` (12 carriers)

Factors are drawn from `random.Random(int(sha256('<seed>:combo:<k>').hexdigest()[:16],16))`,
independently, in this order: `endian {le,be}`, `in_tree {0,1}`, `escaping {0,1}`, `partial {0,1}`,
`comp` (`gzip` when partial, else `gzip|xz`), `max_depth {1,3}`. The declared tuple is **computed
from the factors** (`G = {extractor-failure if partial} ∪ {unpublished-entry if in-tree} ∪
{depth-limited if depth==1}`, `SR = escaping`, `BE = n/a unless damaged`, `P = nonzero`), and
`class_expected` is null. Partial combos use `link_placement='root-first'` so a damaged block can
never pre-empt the links the declaration counts on. Full table in `dev-combo-factors.md`:

| id | endian | in-tree | escaping | partial | comp | depth | declared G | BE | SR | P | vs named tuples |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C01 | be | 0 | 1 | 1 | gzip | 3 | extractor-failure | yes | yes | nonzero | **outside** |
| C02 | le | 0 | 1 | 0 | gzip | 3 | — | n/a | yes | nonzero | in set |
| C03 | be | 0 | 1 | 1 | gzip | 3 | extractor-failure | yes | yes | nonzero | **outside** |
| C04 | le | 1 | 1 | 1 | gzip | 1 | depth-limited, extractor-failure, unpublished-entry | no | yes | nonzero | **outside** |
| C05 | le | 0 | 1 | 1 | gzip | 1 | depth-limited, extractor-failure | no | yes | nonzero | **outside** |
| C06 | le | 0 | 0 | 1 | gzip | 1 | depth-limited, extractor-failure | no | no | nonzero | in set |
| C07 | be | 0 | 1 | 0 | gzip | 1 | depth-limited | n/a | yes | nonzero | **outside** |
| C08 | be | 0 | 0 | 0 | xz | 1 | depth-limited | n/a | no | nonzero | in set |
| C09 | be | 1 | 1 | 1 | gzip | 3 | extractor-failure, unpublished-entry | yes | yes | nonzero | in set |
| C10 | le | 1 | 0 | 0 | gzip | 3 | unpublished-entry | n/a | no | nonzero | in set |
| C11 | le | 0 | 0 | 1 | gzip | 3 | extractor-failure | no | no | nonzero | **outside** |
| C12 | be | 1 | 1 | 0 | gzip | 3 | unpublished-entry | n/a | yes | nonzero | in set |

**6 of 12 dev combos fall outside the 18 named class tuples** (C01, C03, C04, C05, C07, C11);
11 distinct tuples among 12 (C01 and C03 draw the same tuple). C04 is a three-way combined set no
named class carries. All 12 matched their declared tuple on the dev seed.

## 5. Dev proof — 52/52 observed == declared

```
python3 -I -B .ufo/waves/round-41/w1/artifacts/R41C2Gen/heldout-gen-v3.py \
  --seed c9e30c103fab83c4a703aec5927cb26187cf67f18f6bc6ec29352f09097fe31b \
  --out "$S/dev" --run --verify --scratch "$S" \
  --gen /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-40/gen-squashfs.py
# exit 0, 52 carriers, 1m31s, "52/52 carriers reached their declared tuple"
```

Per-carrier rows (H01–H40, C01–C12) are in `dev-feature-table.md`; the class-level tuples are the
"declared tuple" column of §3 and the table of §4. Digest binding: `subject.digest.sha256` equals
the carrier sha256 on all 52 runs (`digest-ok`). 50 runs are `extract-firmware` (37 at depth 3, 13 at
depth 1), 2 are `inspect-firmware-regions`.

Two red runs are kept, because a checker that never fails proves nothing:

* `dev-run-first-attempt.log` — 32/36, exit 1. My first expectation said the dependency-gap chunks
  were not extraction failures; the envelopes (and round-40's committed H13/H15) say they are.
* `dev-run-clean-empty-regression.log` — 50/52, exit 1. Adding the empty-directory fill (§6 F7)
  silently turned `clean-empty` into P>0; `--verify` caught it by name (`published: want 'zero' got
  'nonzero'`) and the fill is now skipped for the intentionally empty class.

## 6. Findings for the freeze

* **F1 — a dependency gap also marks the chunk failed.** `dep-missing-be/le` carry
  `extraction_failed: true` *and* `G={missing-extractor-dependency}` (H13–H16; round-40's committed
  H13/H15 agree). The precedence text is safe (rule 3 precedes 4–6), but any table or evaluator that
  matches a bare "failed" column before the gap kind labels these `body-extractor-failure`.
* **F2 — BE is observable only on the failure branch.** `body-extractor-failure` records
  `sasquatch-v4be -be …` (BE yes) and `avm-marker-be-dropped` records `sasquatch-v4be -no-exit-code …`
  (BE no) — that token is the *only* thing separating the two v2 classes. A successful run records no
  argv at all and `MaliciousSymlinkRemoved` reports carry `command: null`, so BE must be
  `yes/no/n/a` with `n/a` for "no argv", never `no`.
* **F3 — `depth-limited` moves with the parameter, not with the carrier.** It is minted from
  `normalized.depth_limited_paths` (REA `dist/cli-runtime/cli.js:14271-14276`); at `--max-depth 1`
  every successful extraction directory is marked, nested image or not, and the same bytes read
  `depth-limited` at depth 1 and `clean` / `unpublished-entry` at depth 3
  (`depth-control/H31-depth3.json`, `H33-depth3.json`: handlers become
  `{squashfs_v4_be, squashfs_v4_le}` and the depth gap disappears — the nested chunk really is
  extracted). This is why v3 passes `--max-depth` explicitly and records it per class.
* **F4 — the 13th label still has no action token in the frozen line.** The current `SKILL.md` line
  declares 12 tokens; `--actions-file` exits 1 naming `extract-nested` as undeclared, and exits 0
  against a v3-shaped line that adds it (`action-vocab/`). The freeze must add one token for
  `depth-limited` and select the matching `--actions-set`; the generator then records
  `action_source{file, sha256, tokens}`. Carriers do not depend on tokens.
* **F5 — R40-CL4 is now a length pin, not a compressor pin.** `MAX_DAMAGED_BLOCK = 512 B`, fill
  `0x00`, `pin_check.py` red/green: a `hex3100` target is REFUSED at **1762 B** compressed (MH-4's
  absorbed regime), a `pat1500` target is ACCEPTED at **77 B**. Dev partial block lengths:
  21, 24, 31, 33, 35, 36, 37, 84, 92, 93, 132 B. `partial-body-failure` is back to `comp='k'`; its
  gzip replicate is byte-identical to v2's, its xz replicate is the only carrier the repair moved.
* **F6 — `P > 0` means "published", not "analysed"** on a depth-limited envelope: files under the
  ceiling carry `reported_sha256=null` (R41C2ReconDepth §5; consistent with my H31/H33 runs). Any v3
  cause/action prose that equates publication with a walked tree is wrong for this class.
* **F7 — the lane writer collapses two directories when one has no children** (defect in
  `tools/round-40/gen-squashfs.py`, inherited by every round that used it). A directory record with
  no children writes **nothing**, so `dir_ref` is `(block, 0, 3)` — the same offset the next record
  receives. Measured (seed `b13ef790…`, combo C08): `78hgf8qhm` and its empty child
  `78hgf8qhm/_2bjv9low` both claim dir-table offset 0. Effects: `sqfs-list.py` still parses the
  image; `sasquatch` extracts the files but **silently skips the empty directory**; a reader that
  follows the shared record loops (my reader did, hence the new cycle guard in `_Sqfs.walk`).
  v3's `fill_empty_dirs()` gives every directory one child so **no v3 image carries a collapsed
  record**; `clean-empty` is exempt because its empty directory is the class (and that exemption is
  exactly what the 50/52 red run proved necessary). Round-40's frozen held-out set may contain such
  images — no label is affected (directories are neither published nor gapped), but a C1-style
  oracle that lists an empty directory will disagree with extraction.
* **F8 — the amendment's `failure-depth-limited` cannot have P = 0; the shipped class declares the
  measured P-class.** Measured, in order:
  1. id-table-zeroed carrier at `--max-depth 1` → `G={extractor-failure}`, P=0, `depth_limited_paths`
     **empty** (a failed root extraction mints no depth gap);
  2. the same broken image *inside* a valid image at depth 2 → `G={extractor-failure}`, P=1, no depth
     gap (a failing child task never becomes a ceiling task);
  3. a valid **empty** image at depth 1 → `G={depth-limited}`, P=0;
  4. `[empty image][4096 zero pad][broken image]` at depth 1 → `G={depth-limited, extractor-failure}`,
     P=2 (`padding` + carve);
  5. `[empty image][zeros to 4096][broken image]` at depth 1 → same gaps, **P=1**, handler set
     `{squashfs_v4_be}` / `{squashfs_v4_le}` only — **this is the shipped two-chunk layout**
     (`H39/H40`, `layout='two-chunk'`, both chunks' offsets/sha256/roles in the manifest).
  Any chunk that is not the root is carved into a published file, and a root-chunk failure mints no
  depth gap, so `{extractor-failure, depth-limited}` with P=0 is unreachable with unblob 26.6.4 +
  REA 6.5.0. With P>0 rule 4 owns the label (`partial-body-failure`) — the precedence-order trap the
  class exists for — and the declared tuple says `published: nonzero` rather than claiming a P=0 the
  toolchain cannot produce.
* **F9 — the combined classes are the only discriminating part of the held-out set** (independently
  cross-checked by R41C2Interp: the committed round-40 26-carrier set scores identically under the
  v2 table and a transcribed v3 table). The 10 combined carriers plus the 12 factor combos are what
  separate tables that hard-code the named tuples.

## 7. Controls

1. **Depth control** — `H31`/`H33` at `--max-depth 3`: handlers `{squashfs_v4_be, squashfs_v4_le}`,
   gaps `[]` / `[unpublished-entry]`, `depth_limited_paths` 0, P 8/9, exit 0. Label changes with the
   parameter alone.
2. **Lineage** — the 13 v2 classes rebuilt with the round-40 v2 generator on the same seed:
   **21 of 26 byte-identical**; the five that differ are four trees that contained a childless
   directory (the F7 fill) plus `partial-body-failure`'s xz replicate (the R40-CL4 repair). H21, the
   gzip replicate of the partial class, is byte-identical.
3. **Determinism** — selftest 12/12: same seed → identical manifest bytes and all 52 carrier sha256;
   other seed → all 52 differ; no two carriers equal; the pin holds on all 13 partial carriers; the
   depth-limited classes carry `max_depth 1` + a nested image; every carrier declares the six fields;
   named carriers keep `class_expected`, combos keep `null` + a well-formed factor vector.
4. **Action binding** — exit 1 on the round-40 SKILL line, exit 0 on a v3-shaped line, with
   `action_source` recorded in the manifest.
5. **Digest binding** — 52/52 `subject.digest.sha256 == carrier sha256`.

## 8. Limits

* I did not read the round-40 independent evaluator or `R41C2Eval`, and I ran no scorer: every label
  discussion here is derived from `plans/round-41-claims.md` §R41-C2 plus the L1 amendments. The
  scored labels must come from the frozen evaluator.
* `class_expected` for the named classes assumes the round-40 v2 rows survive into v3; a renamed row
  changes only `manifest.label_actions`.
* Combos declare `published: nonzero` from construction (3–8 files, the damaged target never the first
  file). A future factor set that emptied a tree would need the declaration recomputed, not patched.
* Severity of F4 is the table author's call; the generator cannot validate a token the frozen line
  does not declare, which is the intended loud failure.
