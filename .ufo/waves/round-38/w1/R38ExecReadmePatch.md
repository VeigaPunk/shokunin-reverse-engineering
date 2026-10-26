# R38ExecReadmePatch — `corpus/README.md` patch draft (coverage-map row, knowledge-index row, Frontier bullet)

Lane `kaidoku-shokunin`, round 38 wave 1. Base `77091b492cc53f8743bd0701b1e7d5e66123dd84`;
hand-off HEAD `9c9d496b73cf066b02639dc54647934a0ba4297a`. `git diff 77091b49 9c9d496b --
corpus/README.md` is empty (exit 0, no output), so the patch applies against the frozen base and
against HEAD alike. No lane file other than this report and my own artifact directory was written;
`corpus/README.md` itself was **not** edited.

**Status: draft delivered, but on present evidence the C1 row must not be landed — P38-C1 is
unsatisfiable with the frozen K2 carrier (§5).** Everything in §2 is exactly what would land if the
L1 later rules `met_target`; it is the claim-form text, not a landed edit.

## 1. Deliverables

| path | bytes | content |
|---|---|---|
| `.ufo/waves/round-38/w1/artifacts/R38ExecReadmePatch/patch.txt` | 6027 | unified diff, 3 hunks, `-p1` from the lane root (`a/corpus/README.md` → `b/corpus/README.md`) |
| `.ufo/waves/round-38/w1/artifacts/R38ExecReadmePatch/README.patched.md` | 74263 | result of applying `patch.txt` to the committed README (258 lines) |
| `.ufo/waves/round-38/w1/artifacts/R38ExecReadmePatch/checks.txt` | 753 | apply + binding-simulation output (§3) |

## 2. The three lines, before → after

### 2.1 Coverage-map row (inserted after line 90, inside `## Coverage map`, before the blank line at 91)

Before (line 90) — unchanged, context only:

```
| unblob's sasquatch dependency (round 36, assimilated) | `2026-10-26-unblob-sasquatch-dependency` | held as producer contract — unblob README (tag 26.6.4) makes SquashFS support conditional on an external sasquatch and documents a Debian-package route; devttys0 README self-labels sasquatch "Very beta."; re-grounded from the shokuknow package with three corrections |
```

After (new line at 91):

```
| Big-endian SquashFS v4 recursion (round 38) | `2026-10-26-r38-sasquatch-be-squashfs-recursion` | held (bounded, standard big-endian SquashFS v4) — stock unblob 26.6.4 under REA `extract-firmware` (rea-agents 6.5.0) runs the `squashfs_v4_be` handler on four frozen BE v4 carriers and publishes every regular file of the frozen oracle (K1 5/5, K2 3/3 synthetic source-tree files; K3/K4 4/4 unblob 26.6.4 fixture files); the handler shells out to `sasquatch-v4be` (`~/.local/bin`, official onekey-sec deb, S107) and records `missing-extractor-dependency` with `dependencies:["sasquatch-v4be"]` when it is off PATH; K2's tree symlink is recorded as `unpublished-entry`, K1/K3/K4 record no gap; AVM-BE and vendor-mangled images not measured. Dated supersession of the round-36 note's "big-endian/AVM stays frontier" for standard BE v4 (kept as history) |
```

The row starts with `|` and carries the stem, which is the whole of the frozen counter's
`coverage_map_row` test (§4).

### 2.2 Knowledge-index row (inserted after line 196, inside `## Knowledge`)

Before (line 196) — unchanged, context only:

```
| `2026-10-26-unblob-sasquatch-dependency` | unblob's producer contract: SquashFS support needs an external sasquatch; Debian-package route; "Very beta." self-label (assimilated from shokuknow `merge/kaidoku`, re-grounded) | S110, S111 | 2026-10-26 |
```

After (new line at 197):

```
| `2026-10-26-r38-sasquatch-be-squashfs-recursion` | Standard big-endian SquashFS v4 on four frozen carriers through stock unblob 26.6.4 under REA `extract-firmware`: `squashfs_v4_be` handler, regular-file parity with the frozen oracle, the `sasquatch-v4be` extractor dependency and its `missing-extractor-dependency` gap, the symlink `unpublished-entry` boundary, AVM-BE unmeasured | S107, S108, S112, S113; receipts `corpus/evidence/round-38/c1/`; counter `tools/round-38/c1-counter.py`; carriers `corpus/evidence/round-37/c1/carriers.json` | 2026-10-26 |
```

### 2.3 Frontier bullet (inserted after line 233, inside `## Frontier`; the two earlier sasquatch lines stay, kept as history)

Before (line 233) — unchanged:

```
- sasquatch — 2026-10-26 dated note on the line above (kept as history): LE SquashFS v4 recursion is now Core (`2026-10-26-r36-sasquatch-squashfs-recursion`); "AUR" was one route, the producer documents a Debian package (`2026-10-26-unblob-sasquatch-dependency`). Still frontier: big-endian/AVM (`sasquatch-v4be`) and vendor-mangled images.
```

After (new line at 236 in the patched file):

```
- sasquatch — 2026-10-26 round-38 dated note on the two lines above (kept as history): standard big-endian SquashFS v4 is now Core (`2026-10-26-r38-sasquatch-be-squashfs-recursion`); the extractor unblob runs for it is its own `squashfs_v4_be` handler over `sasquatch-v4be`, so "AVM stays frontier" now means the vendor formats only — AVM-BE (the handler's `bytes_used == mkfs_time` test selects a path this round did not measure) and vendor-mangled images stay Frontier.
```

Effect on the Frontier statement the claim names: big-endian **standard v4** stops being Frontier;
**AVM-BE** and **vendor-mangled images** stay Frontier. The old bullet is not rewritten, so the
history is intact and the round-36 note is not silently reversed.

## 3. Verification actually run (in scratch, removed afterwards)

Scratch was `/fast/scratch/hyaku/kaidoku-r38/R38ExecReadmePatch{,-fresh}`; both are deleted
(`ls -d /fast/scratch/hyaku/kaidoku-r38/R38ExecReadmePatch*` → nothing). `TMPDIR` was not needed
beyond the patch copies (all < 50 MB). Recorded in `checks.txt`:

| step | command | observed | exit |
|---|---|---|---|
| dry run | `patch -p1 --dry-run < patch.txt` in a fresh copy containing only `corpus/README.md` | `checking file corpus/README.md` | 0 |
| apply | `patch -p1 < patch.txt` | `patching file corpus/README.md` | 0 |
| identity | `cmp -s corpus/README.md README.patched.md` | identical | 0 |
| heading map of result | `## Coverage map` 11, `## Knowledge` 93, `## Lessons` 200, `## Frontier` 228, `## Known gaps` 242 | as shown | 0 |
| `coverage_map_row` rule (counter line 241, working tree; 234 at HEAD) | section `## Coverage map`, lines `lstrip().startswith('|')`, containing the stem | `True` (1 row) | 0 |
| stems in the coverage map | `re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section)` | **125** (124 at the base) | 0 |
| knowledge-index row | `## Knowledge` section holds the stem as a table row's first cell (found with an `l.startswith` test) | `True` | 0 |
| Frontier | bullets containing `sasquatch` | 3 (was 2) | 0 |

The first `checks.txt` draft was overwritten: it re-ran `patch` in the tree already patched by the
verification pass, so `patch` answered `Reversed (or previously applied) patch detected!` (exit 1).
The file now holds only the fresh-copy run above. That exit 1 was a scratch-reuse artefact, not a
patch defect.

## 4. Bindings this patch satisfies, and their exact rule

Frozen counter `tools/round-38/c1-counter.py` at HEAD (`8e33ac68`):

- `b['coverage_map_row']` (line 234): `readme = show(root, rev, 'corpus/README.md')`;
  `cm = section(text, '## Coverage map')`; true iff any line of `cm` with
  `l.lstrip().startswith('|')` contains `STEM = '2026-10-26-r38-sasquatch-be-squashfs-recursion'`.
  Satisfied by §2.1; no other section, table or heading is consulted.
- `bind_ok` (lines 236-237) also needs `province_core_section`, `province_core_row`
  (`squashfs_v4_be` in the row's **first cell** and the entry path in the row, under
  `## Round-38 additions to Core`), `frontier_note` (a `PROVINCE.md` line containing both
  `big-endian` and `superseded`), `entry_present`, `sourced`. All five are outside this seat
  (`PROVINCE.md`, the entry, `corpus/SOURCES.md`); the README contributes only
  `coverage_map_row`.
- `sourced` (HEAD line 231, working tree line 238) needs ≥1 `SOURCES.md` row whose cell 0 appears
  on a line of the entry starting `source:`, whose opened date (cell 8) is `2026-10-26`, and whose
  used-by (cell 10) contains `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`.
  Existing `S107`/`S108` are opened `2026-10-26` but their used-by lists only the round-36 entry, so
  the entry's own source line must name a row that the L1 extends or opens (§6.3).

The working tree currently holds an **uncommitted** edit of this counter (§6.1). Its
`coverage_map_row` rule is unchanged in substance (now line 241, same predicate over the same
section), so `patch.txt` satisfies both the committed and the in-flight version.

## 5. Blocker: K2's `unpublished-entry` gap makes P38-C1 unsatisfiable

The frozen predicate requires each carrier's after-receipt to carry **no extraction gap**
(`plans/round-38-claims.md`, P38-C1), and the counter enforces it literally:
`after_gaps_empty = gaps(env) == []` (HEAD line 186; working tree line 195) and `ok` requires it
(line 196). K2's carrier was frozen with a symlink whose target stays inside the tree
(`carriers.json`: "tree2, symlink + unicode name"), and both independent draft receipts record it as
a gap:

| carrier | draft receipt | evidence id | handler | gaps | regular files | oracle hits |
|---|---|---|---|---|---|---|
| K1 | `artifacts/R38ExecProvincePatch/after-K1.json` | `ev_eccca7337fd…` | `squashfs_v4_be` | `[]` | 5 | 5/5 |
| K2 | `artifacts/R38ExecProvincePatch/after-K2.json` | `ev_66d89e96ca4…` | `squashfs_v4_be` | 1 | 3 | 3/3 |
| K3 | `artifacts/R38ExecProvincePatch/after-K3.json` | `ev_05731564198…` | `squashfs_v4_be` | `[]` | 4 | 4/4 |
| K4 | `artifacts/R38ExecProvincePatch/after-K4.json` | `ev_b62e21b8c51…` | `squashfs_v4_be` | `[]` | 4 | 4/4 |
| K2 | `artifacts/R38ExecAfterK2/after.json` (second, independent run) | `ev_4d478254a54…` | `squashfs_v4_be` | 1 | 3 | 3/3 |
| K3 | `artifacts/R38ExecAfterK3/after.json` (sasquatch-v4be off PATH) | `ev_bb5d941f43f…` | `squashfs_v4_be` | 1 | 0 | 0/4 |

The K2 gap is identical in both runs:

```json
{"kind": "unpublished-entry", "relative_path": "firmware.bin_extract/var/lib/run-link",
 "handler": null, "dependencies": []}
```

(`normalized_result.unpublished_entries[0]` additionally records
`{"relative_path": "firmware.bin_extract/var/lib/run-link", "kind": "symlink", "link_target": "../../a/run.sh"}`.)

Consequence: K2 can never satisfy `after_gaps_empty` on the frozen carrier bytes, so
`carriers_matched ≤ 3`, `met_target` is false, and P38-C1 is an **honest stop** on present
evidence. `plans/round-38-claims.md` forbids changing the counter, predicate, carriers or oracle
after the freeze. Therefore §2.1 and §2.2 must not be landed as a "held" coverage-map/knowledge
pair; they are the draft that shows what would land, and what the row has to say truthfully
(the gap is disclosed in the row itself rather than hidden).

Why K1 shows no gap while K2 does is **measured, not inferred**: K1's symlink `link-to-hello`
targets `../hello.txt`, which escapes the extraction root, so unblob answers
`normalized_result.diagnostics[0].report.__typename__ = "MaliciousSymlinkRemoved"`
(severity `WARNING`) and records no gap; K2's `run-link` resolves inside the tree and lands in
both `unpublished_entries` and `extraction_gaps`. `sasquatch-v4be -l -be` lists a symlink entry in
both carriers, so neither image lacks it.

## 6. Further findings and risks for the L1

### 6.1 The extractor-dependency premise, and an uncommitted counter edit

unblob 26.6.4's handler shells out to `sasquatch-v4be`; there is no built-in BE extractor:

```
~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py
  26:    V4BE_EXECUTABLE = "sasquatch-v4be"
  41:                executable = self.V4BE_EXECUTABLE      # Endian.BIG, 4
  49:                        if not is_avm: commands_args.append("-be")
  68:    def get_dependencies(self) -> list[str]:
  69:        return [self.EXECUTABLE, self.V4BE_EXECUTABLE]
sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287  (== S108's pinned digest)
```

So the frozen predicate's "run with stock unblob 26.6.4; **no external extractor dependency**" and
the Not-claimed note "sasquatch-v4be **not** required … the round-37 before-arm does not reproduce"
are contradicted by the before-arm receipt in the same wave: with `sasquatch-v4be` off PATH, K3
returns `{"kind": "missing-extractor-dependency", "handler": "squashfs_v4_be",
"dependencies": ["sasquatch-v4be"]}` and publishes 0 files (`ev_bb5d941f43f…`). The v4be binary is
present at `~/.local/bin/sasquatch-v4be` (436232 B, official onekey-sec deb, S107), which is why the
after-runs succeed. The §2 lines therefore state the mechanism as measured instead of repeating the
"no external extractor" premise.

Independently: `git status` shows `M tools/round-38/c1-counter.py` (mtime
2026-10-26T03:22:17-03:00, uncommitted; `git diff HEAD` non-empty). The diff rewrites the P38-C1
docstring sentence to "run with **sasquatch-v4be available**, as unblob 26.6.4's SquashFSExtractor
requires" plus "the paired committed before-receipt … names sasquatch-v4be as a missing extractor
dependency", and adds `before`-receipt handling (`before_missing_extractor_gap`). That is a change to
a frozen predicate/counter after the freeze commit; if it is to stand, the L1 must own it as an
explicit re-freeze disclosure, not as a silent wave-1 edit. I did not touch the file and report it as
found. [INFERENCE] a sibling seat produced it while probing the K3 before-arm.

### 6.2 The stated coverage count moves 124 → 125

`c2-counter.py` command A counts `len(knowledge_files ∩ stems_in_coverage_map)`. Measured at the
base (`77091b49`): 124 knowledge files, 124 stems, intersection 124, no unmapped file, no stem
without a file. Adding the round-38 entry plus §2.1 gives **125/125**. `SCORECARD.md:23` currently
states "124/124 knowledge files mapped after the round-36 landing" — the SCORECARD seat must move it
to 125/125 (with the new revision and the new entry named), or C2's stated-count check fails on a
stale number.

### 6.3 Source ids in the index row are placeholders for the SOURCES gate

`S107` (sasquatch release deb, contains `sasquatch-v4be`) and `S108` (unblob handler source) exist
and are opened `2026-10-26`. `S112`/`S113` are the next free ids (max registered is `S111`) and stand
for the two round-38 candidates named in the claims — unblob BE-fixture provenance and the Freetz
AVM-BE note (R37-CL2 requires both registered before a claim relies on them). If the lesson gate
admits them under other numbers or rejects one, §2.2's source cell must be corrected to cite exactly
the ids the entry's `source:` line names — the counter compares only the entry, so a stale README id
would be a citation defect that the counter cannot see.

## 7. Boundaries observed

- `corpus/README.md`, `PROVINCE.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`,
  `corpus/knowledge/*`, `corpus/evidence/round-38/*` and every counter/harness were left untouched.
- No VCS mutation; no commit, no push, no jj. Read-only `git show`/`diff`/`status` only.
- No subagents, no background jobs, no `agent://all`.
- No tool installs or upgrades this seat; `/home/vgpnk/.omp/agent/RULES.md` not needed.
- Scratch removed. Cited receipts live in sibling artifact directories under
  `.ufo/waves/round-38/w1/artifacts/` (drafts, not yet committed to `corpus/evidence/round-38/`);
  they are the wave's draft data and are marked as such, not as my evidence.
- Not mine, reported as found: an untracked `unblob.log` (3617 B, mtime
  2026-10-26T03:24:32-03:00) sits at the **lane root**, recording an unblob run that processed
  `corpus/evidence/round-37/c1/K3/carrier.bin` from the lane root, i.e. a sibling ran unblob with
  its cwd outside scratch. It needs removal before the wave's census/commit step.

## 8. What the L1 has to decide

1. P38-C1: accept the K2 `unpublished-entry` gap as decisive (honest stop), or re-open the
   carrier/predicate question — which the freeze forbids. On the frozen rule, `met_target` cannot
   become true.
2. If the claim stops, `patch.txt` is discarded; nothing in it should be applied piecemeal, because a
   coverage-map row without the receipt-backed claim would overstate Core.
3. Own the uncommitted `tools/round-38/c1-counter.py` edit: either revert it or land it as a
   disclosed re-freeze with the before-receipt requirement.
4. Keep `PROVINCE.md`'s `frontier_note` line and the `## Round-38 additions to Core` row consistent
   with §2.3's wording so the README and PROVINCE do not disagree about what stays Frontier.
