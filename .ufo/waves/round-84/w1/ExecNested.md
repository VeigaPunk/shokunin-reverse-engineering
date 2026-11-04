# ExecNested — independent reproduction of R84-C3 (coverage, nested container chain)

Seat: `ExecNested` (executor, round-84 wave `r84-w1`) · Lane `kaidoku-shokunin` · L1 `KaidokuR84`
Base: `043b89a25241710a68b45526c3287fb3c8d907c3` · Claim: **R84-C3** (coverage — nested sub-images below depth 1)
Runner: `w1/ExecNested/repro_c3.py` — written from scratch for this seat; it shares no code with the frozen counter `tools/round-84/nested-sqfs.py` (flat procedural driver, `pathlib` + `hashlib.file_digest`, named check list E1–E14). The frozen counter was read only to fix the observable interface (REA envelope field names), never copied. Receipt schema: `execnested-r84-c3-repro-v1`.

## Verdict

**Confirmed.** The R84-C3 predicate reproduces end to end at BASE with an independent runner: 14/14 checks true, file-count control fires, `met true`, runner exit 0. Every measured value matches the L1 pilot receipt (`.ufo/waves/round-84/pre/c3-pilot.json`), including byte-identical fixture image digests and the same gap `continuation_id`. At BASE, `git show 043b89a2:tools/round-84/nested-sqfs.py` fails (tool absent), matching the plan's before-state (class Frontier, 0/9 arms at BASE).

## Method (all under scratch `/fast/scratch/hyaku/kaidoku-r84/ExecNested/`, since removed)

1. Two independent chain builds (`build-r1`, `build-r2`) with `mksquashfs 4.7.5`: leaf (`alpha.txt`, `beta.txt`, 200-row `gamma.bin`) → `c.sqfs`; mid (`inner-c.sqfs`, `one.txt`, `two.txt`) → `b.sqfs`; outer (`inner-b.sqfs`, `x.txt`) → `a.sqfs`; each `-noappend -comp gzip -b 4096 -quiet -repro-time 1760000000`.
2. Oracle per level with `unsquashfs 4.7.5 -d`: full recursive listing + sha256 → expected published map (8 members, levels 1–3 after stripping REA's `firmware.bin_extract/` root).
3. `npx -y rea-agents@6.5.0 extract-firmware <build-r1/a.sqfs> <absent outdir> --max-depth {3,4} --format json`; both outdirs verified absent before the run; `TMPDIR` pinned inside scratch.
4. Scoring: path-set equality and per-path sha256 equality vs the oracle at both depths, coverage, `depth_limited_paths`, `extraction_gaps`, per-file `analysis_depth`, engine identity, carrier identity vs built pins, build-to-build reproducibility.

## Toolchain (nothing installed or upgraded; no PATH-dir writes)

| tool | version | channel |
|---|---|---|
| mksquashfs / unsquashfs | 4.7.5 (2026/03/01) | pre-existing on host |
| python | 3.14.8 | pre-existing |
| node / npx | v24.21.0 | pre-existing |
| rea-agents | 6.5.0 | `npx -y rea-agents@6.5.0` (authorized npm channel; npx cache) |
| unblob (invoked by REA) | 26.6.4 | pre-existing at `~/.local/share/uv/tools/unblob/bin/unblob` |

Tooling authorization exercised: `npx` fetch of `rea-agents@6.5.0` only. No installs, no upgrades, no pacman, no host services touched.

## Fixture digests — rebuild twice, reproducible (E14 true)

| image | build-r1 sha256 | build-r2 sha256 |
|---|---|---|
| `a.sqfs` (outer) | `e82c59956789a47b7524dda30d9ac4f6139a4cf279b0e5403039df88549d06c2` | same |
| `b.sqfs` (mid) | `7d2dd0e73d1bbeffe02aef346ea45b5c3604255a598b9cb7b1daaa6ef6fc3d1a` | same |
| `c.sqfs` (leaf) | `f68b42fa16a9b1ed0fd57165f0a949e89271c09a59db680b3e39a155fbea4aa8` | same |

All three equal the pilot receipt's `fixture_pins` byte-for-byte — `-repro-time 1760000000` makes the chain deterministic across runners and sessions (S301 holds). Carrier identity (E13 true): `inner-b.sqfs` inside the outer oracle == pin b; `inner-c.sqfs` inside the mid oracle == pin c. Oracle counts: outer 2, mid 3, leaf 3 members.

## Published set vs oracle — identical at both depths (E2, E3, E8, E9 true)

REA reports extract root `firmware.bin_extract` (it renames the input) and 8 files in both runs; after stripping that single shared root, the published path set equals the unsquashfs oracle set exactly, and every published sha256 equals the oracle sha256, at `--max-depth 3` and `--max-depth 4`. `published_bytes` 9837 in both runs.

| published path (root-stripped) | level | sha256 (oracle == REA at d3 == d4) | analysis_depth d3 | d4 |
|---|---|---|---|---|
| `x.txt` | 1 | `8238740e443649fb3548aface71ec79fcbe97fdf4a168c434dec10a5df555673` | 1 | 1 |
| `inner-b.sqfs` | 1 | `7d2dd0e73d1bbeffe02aef346ea45b5c3604255a598b9cb7b1daaa6ef6fc3d1a` | 1 | 1 |
| `inner-b.sqfs_extract/one.txt` | 2 | `d0233a9a5866b5ac60c6c3fd194caace998d8bec7c8968b64838658ffc2aa9b0` | 2 | 2 |
| `inner-b.sqfs_extract/two.txt` | 2 | `110cbe584f54b21db2ce7a602ffe26b6a434bf05358d3f66f454a82455318da2` | 2 | 2 |
| `inner-b.sqfs_extract/inner-c.sqfs` | 2 | `f68b42fa16a9b1ed0fd57165f0a949e89271c09a59db680b3e39a155fbea4aa8` | 2 | 2 |
| `..._extract/inner-c.sqfs_extract/alpha.txt` | 3 | `d063a9ad96d0a5593edc7f71840eb7728cf218d611cc368ca96105f154d9695b` | **null** | 3 |
| `..._extract/inner-c.sqfs_extract/beta.txt` | 3 | `d3db6ca0a178712cecf33bf8c22433b52ada83a12049e8ecb491f01b4623d96b` | **null** | 3 |
| `..._extract/inner-c.sqfs_extract/gamma.bin` | 3 | `2e5fe29222d1cd97d6673153dcf480cea9931274a0e6bc9a386c40e5850e1aac` | **null** | 3 |

## Depth 3 vs depth 4 (E4–E7, E10, E11 true)

- **Files:** no difference — same 8 paths, same bytes at both depths.
- **coverage:** differs — `partial` at depth 3, `complete` at depth 4.
- **depth_limited_paths:** exactly one at depth 3 (`$output/firmware.bin_extract/inner-b.sqfs_extract/inner-c.sqfs_extract`), none at depth 4.
- **extraction_gaps:** exactly one at depth 3, `kind: "depth-limited"` at the deepest extract root (`continuation_id 3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab`, identical to the pilot's — envelope is deterministic); none at depth 4.
- **analysis_depth:** differs only on the three level-3 files (`null` → `3`); levels 1–2 unchanged (1 and 2).

**Published vs analyzed at depth 3 — explicitly NOT the same set.** 8 members are published; 5 are analyzed (`x.txt`, `inner-b.sqfs` at 1; `one.txt`, `two.txt`, `inner-c.sqfs` at 2). The three level-3 files are published but carry `analysis_depth null`: publication is not analysis. At depth 4 the published and analyzed sets coincide (all 8 analyzed, level-3 files at depth 3).

## Engine block — identical across both runs (E12 true)

```json
{"executable_path": "/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob",
 "executable_sha256": "0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09",
 "name": "unblob", "source_revision": null, "version": "26.6.4", "worker_count": 1}
```

`npx rea-agents --version` → `6.5.0` (pin honored). Both runs exit 0 with empty stderr — no error envelope.

## File-count control — fires

Rule `published-file-count-equals-oracle-count-therefore-complete`: at depth 3 the run publishes all 8 oracle members yet REA still reports `partial`. A count-only completeness oracle would misgrade this run as complete; the control demonstrates the necessity of the coverage/gap fields. Fires: **true**.

## Checks

E1 runs clean · E2 d3 paths · E3 d3 bytes · E4 d3 partial · E5 d3 one depth-limited path · E6 d3 single gap · E7 d3 analysis map (levels 1,2 at level; level 3 null) · E8 d4 paths · E9 d4 bytes · E10 d4 complete/no gaps/no depth-limited · E11 d4 analysis map (all levels at level) · E12 engine identity · E13 nested carrier identity · E14 fixture reproducibility — **all true**; `met: true`; runner exit 0.

## Bounds and receipts

- Writes confined to: scratch `/fast/scratch/hyaku/kaidoku-r84/ExecNested/` (removed before yield), `.ufo/waves/round-84/w1/ExecNested/`, and this report. No production, fleet, sibling-lane, LOG/SCORECARD/MANIFEST, or PATH-directory writes; read-only git only (`cat-file`, `log`, `show`); no commits, no `task`/subagent spawns, no labrat probe needed.
- Receipts in `w1/ExecNested/` (sha256 in `receipts.sha256`): `repro_c3.py` `a0b89422d5b6ca758daf96ea83d95b50b04d49cd4d44b0a737abbedbb22c257a` · `repro-receipt.json` `aaa7aa9decdb4c0941c38acd8d2e1befe031f1136e229973473062ce4898128b` · `repro-stdout.txt` `cf4eb89e560514482d9bab28324964eefcc0df335d0a49f0bf8c9cd2e7bd43e7` · `repro-stderr.txt` `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) · `rea-probe.txt` `cda8802b6c6087a9635733c1595f426d1aa19c5ed29442c7300a408bc28f2445`.
- Blockers: none. Nothing further needed from L1 for this item.
