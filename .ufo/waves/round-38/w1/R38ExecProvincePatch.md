# R38 wave 1 — seat R38ExecProvincePatch

Scope: draft the exact `PROVINCE.md` patch for R38-C1 (coverage: standard big-endian SquashFS v4
moves Frontier -> Core) and R38-C2 (calibration: the `evidence/doctor/` pointer). `PROVINCE.md` was
**not** edited; the patch is text only, at
`.ufo/waves/round-38/w1/artifacts/R38ExecProvincePatch/patch.txt`.

Frozen inputs read: `plans/round-38-claims.md`; `corpus/lessons/round-37-verifier-spotcheck.md`;
the two counters `tools/round-38/c1-counter.py`, `tools/round-38/c2-counter.py`; the harness
`tools/round-38/c1-run.sh`; carriers/oracles `corpus/evidence/round-37/c1/`; freeze
`e059ca9391642d5b71b6662cabcbdce0d9308719`; base `77091b492cc53f8743bd0701b1e7d5e66123dd84`.
Lane HEAD while measuring: `cb4326b2aa4c2024af0651fe6115b82d0c4de3df` ("round-38: harness fix");
`PROVINCE.md` is byte-identical at base and HEAD
(sha256 `ecfa491fa315047a6797bd660b239f29e5e1d9c548e38e943e398a9eb0a8d242`), so the patch applies at
either revision. `tools/round-38/c1-counter.py` is **modified in the worktree** relative to HEAD (see
F5); its `PROVINCE.md` bindings are unchanged, and both versions are read below.

## 1. Patch — before/after line by line

### Edit 1 of 3 — Core `REA MCP server` row (`PROVINCE.md:44`), C2 doctor pointer

Before (634 B):

```
| REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml` — config files pin `rea-agents` (Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary) with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` would inspect a running attached client; not exercised this round. CLI: `rea doctor` (6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing) | round-19 re-grepped pin/sha256 record `.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in `evidence/doctor/`; historical readiness probe 2026-10-13 |
```

After:

```
| REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml` — config files pin `rea-agents` (Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary) with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` would inspect a running attached client; not exercised this round. CLI: `rea doctor` (6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing) | round-19 re-grepped pin/sha256 record `.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in `.ufo/waves/round-19/evidence/doctor/`; historical readiness probe 2026-10-13 |
```

### Edit 2 of 3 — round-4 frontier `sasquatch` bullet continuation (`PROVINCE.md:157`), C1

Before:

```
  covers the carved-image path today. [2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to Core`; big-endian/AVM stays here.]
```

After:

```
  covers the carved-image path today. [2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to Core`; big-endian standard SquashFS v4 superseded for Core — see `## Round-38 additions to Core`; AVM-BE and vendor-mangled images stay here.]
```

### Edit 3 of 3 — append at EOF (after `PROVINCE.md:374`), C1

```

## Round-38 additions to Core

Addition to Core for standard big-endian SquashFS v4 (the Core table above is not rewritten; the Frontier list is bounded by the round-38 note below).

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| Standard big-endian SquashFS v4 via the `squashfs_v4_be` handler | no new REA key — unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py` selects `squashfs_v4_be` and runs `sasquatch-v4be` from `PATH` with `-be` (`~/.local/bin/sasquatch-v4be`, official onekey-sec deb, sha256 `fac88740…`); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `rea-agents@6.5.0` | `extract-firmware --format json` on the four frozen carriers — K1/K2 synthetic standard-BE v4 gzip images (`tools/round-37/gen-squashfs.py`), K3/K4 the unblob 26.6.4 `squashfs_v4_be` integration fixtures — against the frozen regular-file oracle `corpus/evidence/round-37/c1/K*/oracle.tsv` | carriers `corpus/evidence/round-37/c1/carriers.json`; receipts `corpus/evidence/round-38/c1/K*/after.json`; handler `squashfs_v4_be` named on all four; every oracle file published with matching sha256 (K1 5/5, K2 3/3, K3 4/4, K4 4/4); zero extraction gaps on K1/K3/K4, one `unpublished-entry` gap on K2 (`var/lib/run-link` symlink); entry `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` |

Limits (measured 2026-10-26, round 38 wave 1): standard big-endian SquashFS v4 only — AVM-BE (the `bytes_used == mkfs_time` variant) and vendor-mangled images are not covered and stay Frontier. Coverage reads `complete` only on K3/K4; K1 and K2 read `partial` (K2's `partial` comes from its one unpublished symlink entry). The handler shells out to `sasquatch-v4be` on `PATH`, so a run without that dependency records `missing-extractor-dependency` and publishes no files (`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/after.json`).

Frontier note, 2026-10-26 (round 38): the big-endian half of the `- **sasquatch** — …` bullet under `### Round-4 frontier (post-unlock)` (`PROVINCE.md:156-157`) is superseded for standard big-endian SquashFS v4 as measured above, and so is the closing clause of the round-36 frontier note; AVM-BE and vendor-mangled images stay Frontier (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`).
```

`patch.txt` carries the same three edits plus a header stating that edits 2-3 are provisional (see §4
F1). The append is 13 physical lines: blank line, `## Round-38 additions to Core`, intro, table
header/separator/row, limits paragraph, frontier note, trailing blank line.

## 2. Why these bytes meet the frozen bindings (static reading of the counters)

`tools/round-38/c1-counter.py` (bindings identical at HEAD and in the worktree's modified copy, F5):

- `CORE_HEADING = '## Round-38 additions to Core'`; `section()` slices `lines.index(heading) + 1`
  until the next line starting `## `. The appended heading is the only whole line equal to it; the
  second textual mention lives inside backticks on line 157 and cannot match `lines.index`.
- `province_core_row`: for every line in that section starting `|`, `cells(r)[0]` must match
  `(?<![A-Za-z0-9-])squashfs_v4_be(?![A-Za-z0-9])` and the row must contain
  `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`. The drafted row's first cell
  is `Standard big-endian SquashFS v4 via the `` `squashfs_v4_be` `` handler` (backticks satisfy both
  lookarounds) and its evidence cell carries the entry path verbatim.
- `frontier_note`: any line of `PROVINCE.md` containing both `big-endian` and `superseded`. The draft
  leaves line 157 carrying both and adds the round-38 note line carrying both.

`tools/round-38/c2-counter.py`:

- `units()` takes `## Core` rows only (the new `## Round-38` section is not scanned, so its pointers
  cannot create a mismatch), and `pointers()` collects lane-prefixed backticked tokens from each row.
- Edit 1 is a 1:1 token replacement inside the `prov_core:REA MCP server` row: the pointer total stays
  48 (the base receipt `.ufo/waves/round-38/w1/artifacts/R38ExecRecountBase/c2-at-base.json` records
  `pointers: 48`), so `pointers_not_fewer` holds.
- `resolves()` requires `git cat-file -e <rev>:<path>`; `.ufo/waves/round-19/evidence/doctor` is a tree
  at base (`git cat-file -t` -> `tree`) containing `doctor-6.5.0.txt` and `doctor-6.7.0.txt`, whereas
  `evidence/doctor` is absent (`git cat-file -t ...:evidence/doctor` -> exit 128,
  `fatal: path 'evidence/doctor' does not exist`).
- The `unrepaired` guard needs a resolving pointer in the same unit whose path ends with
  `/evidence/doctor`; `.ufo/waves/round-19/evidence/doctor` satisfies the `endswith('/' + path)` test.

Static checks executed over the patched text (no counter run, see §6): heading count 1 as a whole
line; exactly one handler row and it contains the entry path; two lines carry both keywords;
`` `evidence/doctor/` `` occurs 0 times and `` `.ufo/waves/round-19/evidence/doctor/` `` twice (line 23
already had the resolved form).

## 3. Observed evidence behind the C1 row

Exact call per carrier (the harness `after` mode is usable since `cb4326b2`; my four 03:18 runs used
the same REA call directly because the freeze-time harness refused to run, see F2):

```
npx -y rea-agents@6.5.0 extract-firmware --format json \
  corpus/evidence/round-37/c1/<K>/<carrier> <fresh-outdir>
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob   # unblob 26.6.4 (uv tool)
PATH carries ~/.local/bin/sasquatch-v4be      # sha256 fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6
```

| carrier | exit | handler | published files / oracle rows | oracle sha256 hits | extraction gaps | coverage | evidence_id (one run) |
|---|---|---|---|---|---|---|---|
| K1 `1cfb6c33…` | 0 | `squashfs_v4_be` | 5 / 5 | 5 | 0 | `partial` | `ev_eccca7337fd7dfe589a67aa33474400ce0001f51e35d70270e1d910e931ca8d6` |
| K2 `403cb0a8…` | 0 | `squashfs_v4_be` | 3 / 3 | 3 | **1 `unpublished-entry`** (`firmware.bin_extract/var/lib/run-link`) | `partial` | `ev_66d89e96ca47811e881af56f81048eec56c306099715a9bcf18e23ff6a83a3e4` |
| K3 `9c7c523c…` | 0 | `squashfs_v4_be` | 4 / 4 | 4 | 0 | `complete` | `ev_05731564198b2377cc76e5dccc12d85fe764dc86fb733f408dba383c69984176` |
| K4 `a29ddc15…` | 0 | `squashfs_v4_be` | 4 / 4 | 4 | 0 | `complete` | `ev_b62e21b8c51c73aac83b9be8435afac1ae103f6ea1b5ef8fb260764738128d58` |

Carrier sha256 values equal the frozen `carriers.json` pins; every published file's sha256 equals its
`oracle.tsv` row under the counter's suffix rule. Full envelopes: `after-K1..K4.json` in the artifact
directory; `probe-summary.txt` carries the same table plus findings.

## 4. Findings for the L1 (reported, not repaired)

**F1 — K2 carries a frozen-relevant extraction gap; P38-C1 cannot reach its target as frozen.**
K2's envelope holds
`extraction_gaps=[{kind:"unpublished-entry", relative_path:"firmware.bin_extract/var/lib/run-link", dependencies:[], continuation_id:"602c674b…"}]`
and `unpublished_entries=[{kind:"symlink", relative_path:…, link_target:"../../a/run.sh"}]`, with
`coverage:"partial"`. The counter's per-carrier `ok` requires `gaps(env) == []`, so K2 is unmatched and
`carriers_matched` would be **3** of 4 (`met_target` false, exit 1). Reproduced four times here
(two output directories, then the same output-directory path twice); `normalized_result` identical.
Independent peer artifact with the same gap:
`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK2/after.json`. K1 carries a *dangling* symlink
(`link-to-hello -> ../hello.txt`) and reports no unpublished entries and 0 gaps — so the gap tracks the
resolvable link, not symlinks as such [INFERENCE]. Counters, carriers and oracle were not touched.

**F2 — the freeze-time `c1-run.sh after` mode could not produce a receipt.**
Freeze blob `96666472dd3b036bec38cf14a026267d352b8f2a` line 26 ran `mkdir -p "$OUT"` before `npx`; REA
then refuses with `{"code":"execution_failure", … "diagnostics":{"reason":"Extraction output root already exists"}}`,
exit 1. Observed four times (K1..K4) at 03:18; peer artifact
`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/harness-after-mode-failure.txt` records the same. HEAD
`cb4326b2` replaces it with `rm -rf "$OUT"` (blob `a95a1a9e…`, line 27); a post-fix harness run on K1
exited 0 with handler `squashfs_v4_be`, 0 gaps, 5 files. Governance note: the harness is named in the
freeze commit, so the fix lands above the freeze; `PROVINCE.md` bytes are unaffected.

**F3 — `evidence_id` is not determined by the recorded request identity (R36-CL6 calibration premise).**
Two identical K2 runs with the same `subject.local_path` **and** the same `parameters.output_directory`
produced `ev_6e8500aaffc1eca9b9ea93e21be251269240ecce99f109a565ef5e36d2a601e9` and
`ev_58fba4864fc8460d4ea8e91a8fabea2bbeb37e3ea5c164e0dc7de5004018791c`. 69 envelope paths differ, all
inside `raw_result`: unblob scratch paths (`rea-firmware-<rand>/…`) and `blob_id` values;
`normalized_result` is identical. So "receipt identity = subject digest" (R36-CL6) is not what the
platform id computes, and byte-identical repeat receipts are unobtainable. Whether the frozen counter's
`xpin` recomputation still passes for such envelopes was **not** exercised here (no counter run).

**F4 — the row's dependency reading.** unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py` has
`EXECUTABLE="sasquatch"`, `V4BE_EXECUTABLE="sasquatch-v4be"`, `class SquashFSv4BEHandler NAME="squashfs_v4_be"`,
and `SquashFSExtractor.extract` selects `sasquatch-v4be` plus `-be` unless `header.bytes_used ==
header.mkfs_time` (AVM-BE). A peer receipt produced with a shim-only PATH records
`missing-extractor-dependency` and 0 files (`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/after.json`),
so the "no external extractor dependency" phrasing in `plans/round-38-claims.md` means "no REA-side
wiring": the BE handler still needs `sasquatch-v4be` on `PATH`. The row states that.

**F5 — `tools/round-38/c1-counter.py` is modified in the worktree, above the freeze, and now asks for a
before-arm the frozen predicate does not describe.** `git status --porcelain` -> `M
tools/round-38/c1-counter.py`; `git diff --stat` -> 43 insertions, 21 deletions. The worktree copy (a)
rewrites the docstring predicate from "stock unblob 26.6.4; no external extractor dependency" to
"sasquatch-v4be available, as unblob 26.6.4's SquashFSExtractor requires", and (b) requires a paired
`before.json` per carrier (`before_missing_extractor_gap` with `missing-extractor-dependency` naming
`sasquatch-v4be`, `before_oracle_hits == 0`) in addition to the unchanged `after` conditions. Its
`PROVINCE.md` bindings (`province_core_section`, `province_core_row`, `frontier_note`, `entry_present`,
`sourced`, `coverage_map_row`) and `after_gaps_empty` are byte-for-byte the same logic, so §2 holds for
both versions, and F1 still blocks K2 either way. The selftest grows from the frozen 15 cases to 19
(`K2 before receipt missing`, `before carries no gap`, `before := after`, `after carries dependency
gap`). Two consequences the L1 has to rule on: the frozen predicate text in `plans/round-38-claims.md`
and the working counter now describe different predicates; and the `before` receipts named there do not
exist yet under `corpus/evidence/round-38/c1/`. I changed neither file.

**F6 — untracked `unblob.log` at the lane root.** `git status --porcelain` lists `?? unblob.log` (3,617 B,
2026-10-26 03:24). unblob writes `unblob.log` into its CWD, and REA was invoked with the lane root as
CWD, so the file is a byproduct of wave-1 extraction runs (its sandbox rule list shows
`ReadWrite("unblob.log")`). It is not evidence and is not cited anywhere in this report; I left it in
place because peers may still be appending to it.

## 5. Deliberate deviation from the assignment wording

The assignment asked the row to carry the observed evidence "(4 carriers, handler, 0 gaps)". The row
names all four carriers and the handler, and records zero gaps on K1/K3/K4 — but it also names K2's one
gap, because an unqualified "0 gaps across four carriers" is contradicted by four reproduced runs and
one independent peer receipt. The frozen target remains what it is; the measurement simply does not
meet it.

## 6. Limits / not done

- **No counter run.** The parent owns the post-integration gate; I did not modify `PROVINCE.md` or
  commit anything, so the counters cannot be measured on the patched tree from here. Suggested checks
  once the patch is applied: `python3 -I -B tools/round-38/c2-counter.py --root … --rev <integration>
  --base 77091b49… --json-out …` (expect `mismatches: 0`, `guards_ok: true`, `pointers: 48`);
  `c1-counter.py` on the same revision — with only `after.json` receipts the worktree version scores 0
  carriers (the `before` arm is missing), and with both arms K2 still fails `after_gaps_empty`, so
  `carriers_matched` cannot reach 4 while F1 stands (the HEAD version, no before-arm, would score 3).
- One pin (`rea-agents@6.5.0`), unblob 26.6.4, Linux host. No AVM-BE, no vendor-mangled image, no
  statement about the extracted programs. K1/K2 are synthetic carriers; K3/K4 are unblob fixtures.
- No tool was installed or upgraded; the existing npx cache, `~/.local/bin/unblob` and
  `~/.local/bin/sasquatch-v4be` were used as installed by the L1. No VCS mutation. No direct file
  write outside this report and the seat artifact directory; the untracked `unblob.log` at the lane
  root (F6) is a tool byproduct of runs whose CWD was the lane root, left in place. Scratch
  `/fast/scratch/hyaku/kaidoku-r38/R38ExecProvincePatch` was removed (`rm -rf`).

## 7. Artifacts

`.ufo/waves/round-38/w1/artifacts/R38ExecProvincePatch/`: `patch.txt` (the three edits, before/after),
`probe-summary.txt` (per-carrier table + F1..F4; F5/F6 are report-only), `after-K1..K4.json` (REA envelopes), `after-K1..K4.err`
(empty), `extract-K1..K4/` (published trees), `harness-after-K1.json` + `harness-after-K1/` (post-fix
harness run and its tree), `determinism-K2-run1.json` + `determinism-K2-run2.json` (the two F3
envelopes, copied out of scratch before it was removed).
