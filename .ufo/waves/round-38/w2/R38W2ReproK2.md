# R38W2ReproK2 — independent re-run of the committed K2 C1 receipts (round 38, attempt 2, wave 2)

**Verdict: CONFIRMED** — the committed K2 `before.json` / `after.json` reproduce on an independent
re-run by a non-author: identical chunk handler, identical `(relative_path, sha256, size)` set,
identical gap kind/paths/dependencies, identical coverage, identical score-relevant exit codes,
byte-identical unblob stdout; the receipts' `evidence_id`s also self-verify under the rea-agents
6.5.0 rule. The judged honest stop reproduces exactly from the first-freeze counter
(`carriers_matched 3`, `met_target false`, exit 1, K2 `after_gaps_empty false`). Three advisory
defects are *outside* the receipts themselves (§7); none is a receipt falsification.

Seat: `R38W2ReproK2`, leaf, advisory only. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
(`HEAD e265533e`). Freeze v1 `e059ca9391642d5b71b6662cabcbdce0d9308719`; control
`efd5c47a72a50b3a434783f82268fb4a96e636a1`; base `77091b492cc53f8743bd0701b1e7d5e66123dd84`.
Claim data under test: `corpus/evidence/round-38/c1/K2/{before,after}.json` at
`3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8`. No lane file was changed except this report and
`.ufo/waves/round-38/w2/artifacts/R38W2ReproK2/`. No VCS mutation anywhere; no REA MCP device used,
REA only through `npx -y rea-agents@6.5.0`; no install or upgrade.

## 0. Axes named (godspeed)

1. **carrier integrity** — are the bytes I re-ran the frozen K2 carrier?
2. **before-arm authenticity** — does the committed `before.json` describe a real PATH-stripped run?
3. **after-arm authenticity** — does the committed `after.json` describe a real default-PATH run?
4. **oracle agreement** — do the published files equal the frozen round-37 oracle?
5. **determinism / non-fabricability** — do repeats agree, and is any field reproducible only by chance?
6. **verdict arithmetic** — does the first-freeze counter still score the receipts at 3/4?
7. **narrative accuracy** — does the author's one-line reason for the stop match the counter's own receipt?

Moves kept were those that improved at least one axis and harmed none; the cheapest (pin check,
PATH reachability) ran first and in parallel with the REA arms.

## 1. Carrier pin (axis 1) — CONFIRMED

```
$ sha256sum /fast/scratch/hyaku/kaidoku-r38/R38W2ReproK2/carrier.sqsh
403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  ./carrier.sqsh
$ git -C <lane> cat-file -p e059ca93…:corpus/evidence/round-37/c1/K2/carrier.sqsh | sha256sum
403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  -
```
Equal to the `carriers.json` pin and to the committed bytes at the freeze. 1606 bytes; chunk
`root_file_range {0,1606}` and `selection {0,1606,403cb0a8…}` in both arms.

## 2. Method (exact commands, timings, exit codes)

Full transcript: `artifacts/R38W2ReproK2/commands.txt`.

- **before-arm** (axes 2): `$HOME/.local/bin` stripped from `PATH` (node/npx keep resolving;
  `sasquatch` and `sasquatch-v4be` both absent — verified with `command -v`, rc 1), with
  `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` kept absolute:
  `env PATH="$STRIP" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0
  extract-firmware --format json carrier.sqsh out-before > before-env.json`
  → shell exit 0, envelope `raw_result.execution.exit_code 1`, extraction dir empty (0 entries),
  wall 1.77 s, stderr 0 B.
- **after-arm** (axes 3): same command, default `PATH` (`sasquatch-v4be` →
  `/home/vgpnk/.local/bin/sasquatch-v4be`), out dir `out-after` → shell exit 0, envelope
  `exit_code 0`, 3 published regular files, 4 dirs, wall 1.69 s.
- **repeats for determinism** (axis 5): `out-before2`, `out-after2`, `out-after3` — three
  independent after runs and two before runs in total, all fresh dirs.
- **identity** (axis 5): `node tools/round-27/xpin-attribute.mjs --pkg65 <pkg> --pkg67 <pkg>` on my
  two envelopes and the two committed ones, wrapped as `{"data": …}` exactly as
  `c1-counter.evidence_ids()` does.
- **verdict arithmetic** (axis 6): frozen `git show e059ca9…:tools/round-38/c1-counter.py`
  (sha256 `a7a62b09…`, 17 469 B) run from scratch bytes at `3b960fe5` and at `0fc61133`, plus the
  worktree counter for contrast.
- Version pins observed inside my envelopes: provider unblob **26.6.4**, engine
  `executable_sha256 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`,
  `worker_count 1`, rea-agents package `6.5.0` (`package.json`), node v24.21.0, npx 11.19.0.
  Parameters identical to the committed receipts (`max_depth 3`, `max_output_bytes 268435456`,
  `max_output_files 10000`).

## 3. Before-arm payload vs committed `before.json` (axis 2) — CONFIRMED

| graded field | mine | committed |
|---|---|---|
| chunk handlers | `["squashfs_v4_be"]` | same |
| chunk extraction_failed | `[true]` | same |
| `normalized_result.files` | `[]` (0) | same |
| `unpublished_entries` | `[]` | same |
| `extraction_gaps` | `[("missing-extractor-dependency", null, ["sasquatch-v4be"])]` | same |
| diagnostics | `[("squashfs_v4_be", ["sasquatch-v4be"], "ExtractorDependencyNotFoundReport", "ERROR")]` | same |
| `coverage` | `partial` | same |
| `published_bytes` | 0 | same |
| continuation id | `4ca863d04cc06d61e7be38d0811847a15f55c70f028fdf45e8fefdf75957a07a` | same |
| `derivations` / `depth_limited_paths` | 0 / 0 | same |
| score-relevant exit code | 1 | 1 |
| unblob stdout | 2089 B, **text identical** to the committed envelope's | 2089 B |
| stderr | 0 B | 0 B |
| argv (unblob) | `--process-num 1 --depth 3 --randomness-depth 0 --report … --log … --extract-dir … firmware.bin` | same shape, different scratch dir |

The committed before-arm is therefore a real PATH-stripped run: it fails for the *declared*
dependency `sasquatch-v4be` (not the LE `sasquatch`), which is exactly what my stripped-PATH run
reproduces, and exactly what the landed entry states.

## 4. After-arm payload vs committed `after.json` (axis 3) — CONFIRMED

| graded field | mine | committed |
|---|---|---|
| chunk handlers | `["squashfs_v4_be"]`, `extraction_failed false` | same |
| files (relative_path, sha256, size, mime) | `firmware.bin_extract/a/run.sh` `ca9988b8…` 22 `text/x-shellscript`; `firmware.bin_extract/space name.txt` `72d0bbc9…` 21 `text/plain`; `firmware.bin_extract/var/lib/data.bin` `e96760a8…` 10240 `image/x-tga` (all `analysis_depth 1`) | **identical, same order** |
| `published_bytes` | 10283 | 10283 |
| `coverage` | `partial` | `partial` |
| `unpublished_entries` | `[("firmware.bin_extract/var/lib/run-link","symlink","../../a/run.sh")]` | same |
| `extraction_gaps` | `[("unpublished-entry","firmware.bin_extract/var/lib/run-link",())]` | same |
| continuation | `602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca`, "retained as metadata; only regular files are published…" | same |
| diagnostics | `[]` | `[]` |
| `derivations` | 10 | 10 |
| score-relevant exit code | 0 | 0 |
| unblob stdout | 1423 B, **text identical** | 1423 B |
| dirs/links counted by unblob | "Extracted files: 4 / directories: 6 / links: 1" | same text |

The `var/lib/run-link` stat report (index 6 of `raw_result.report`) is `is_link true`,
`link_target "../../a/run.sh"`, `size 14` in both, while the final extraction tree contains no
symlink entry (`find -printf '%y %p -> %l'` lists only 4 dirs + 3 regular files; extraction size
10283 B). So the gap is REA's symlink publication policy, not a failed extraction — the chunk is
`extraction_failed false`, exit 0, and all three regular files are present and hashed.

## 5. Oracle agreement (axis 4) — CONFIRMED

Rule from the frozen counter: suffix match on `relative_path` + sha256 equality.

| oracle row (`round-37/c1/K2/oracle.tsv`) | mine | committed |
|---|---|---|
| `a/run.sh` `ca9988b8…` 22 | 1 hit, sha ✓, size ✓ | 1 hit, sha ✓ |
| `space name.txt` `72d0bbc9…` 21 | 1 hit, sha ✓, size ✓ | 1 hit, sha ✓ |
| `var/lib/data.bin` `e96760a8…` 10240 | 1 hit, sha ✓, size ✓ | 1 hit, sha ✓ |

No extra published files, no missing ones. `10283 = 22 + 21 + 10240` matches `published_bytes`.

## 6. Determinism, identity, verdict arithmetic (axes 5–6)

**Determinism.** Payload equality (`compare.txt` §DETERMINISM):
before run1 = run2 → `True`; after run1 = run2 = run3 → `True`, `published_bytes` `[10283, 10283, 10283]`.

**Identity.** `xpin-attribute.mjs` (6.5.0 rule, package's own `semanticProjection`) reports stored id
== recomputed id for **all four** envelopes (`xpin.txt`):
mine-before `ev_554c887e…`, mine-after `ev_daafb11b…`, ref-before `ev_f28115c9…`, ref-after
`ev_e9386786…`. The committed ids are therefore self-verifying; they differ from mine only because
the projection hashes `parameters`, `raw_result` and `normalized_result` (paths + per-run blob ids),
not because anything semantic differs — see §7b.

**First-freeze counter (the judged rule), run from frozen bytes in my own scratch** — reproduces the
author's numbers exactly:

```
python3 -I -B c1-counter-v1.py --root <lane> --rev 3b960fe5… --freeze e059ca93… --pkg65 <6.5.0>
→ exit 1 · carriers_matched 3 · met_target false
  K1 matched true  (5/5, gaps empty)
  K2 matched FALSE (3/3 oracle hits, after_gaps_empty FALSE)
  K3 matched true  (4/4)
  K4 matched true  (4/4)
  bindings: coverage_map_row true, entry_present true, entry_source_ids [S112,S113,S114],
            frontier_note true, opened_source_rows [S112,S113,S114], sourced true,
            province_core_row FALSE, province_core_section FALSE
```
Identical result at `0fc61133` (exit 1, `carriers_matched 3`). `c1-v1-3b960fe5.json`,
`c1-v1-0fc61133.json`. The frozen counter's per-carrier `ok` requires `after_gaps_empty`
(`grep`-read at lines 178–200 of the frozen bytes), so K2's single `unpublished-entry` gap is
mechanically the deciding clause — as the author verdict states.

**Contrast (not the judged rule):** the in-tree counter at `HEAD` (sha256 `d9aa8b62…`, = the
attempt-1 `f1010f67` amendment) reads a `before_*` leg and a narrowed gap binding; on the *same*
receipts it returns `carriers_matched 4` with `K2 after_no_missing_extractor_gap true`, stopped only
by `province_core_row false` (`c1-counter-3b960fe5.json`). Recorded because a future re-run that uses
the in-tree counter instead of the first freeze turns K2's carrier clause green.

## 7. Advisory defects (outside the receipts; reported, not repaired)

**a. The stop has a second, independent red that the one-line reason omits.** The counter's own
receipt shows `province_core_row false` and `province_core_section false` at *both* `3b960fe5` and
`0fc61133`. Read-only confirmation: `PROVINCE.md` at base, `3b960fe5`, `0fc61133` and `HEAD`
contains **no** `## Round-38 additions to Core` heading and **zero** occurrences of
`squashfs_v4_be` (`git show <rev>:PROVINCE.md | grep -n …` → empty; the round-38 PROVINCE change is
2 lines: the C2 `evidence/doctor/` pointer repair and a 1-line append inside the existing Frontier
`sasquatch` bullet). So C1 stays red on the Core-row binding even if K2's gap clause were satisfied.
The landing's prose is at least *self-consistent*: that Frontier bullet says "not promoted — R38-C1
honest stop, K2's in-tree symlink leaves an `unpublished-entry` gap", and the landed entry's table
row for K2 (`3/3 oracle files, 1 gap`) matches my measurement. The defect is in the verdict's
attribution, not the claim data.
→ `[INFERENCE]` (bounded by the receipts): any C1 verdict sentence citing K2 alone under-describes
the failure set.

**b. `evidence_id` is not path-independent, so it cannot be reproduced from the carrier alone.**
`semanticProjection` in `rea-agents@6.5.0 dist/domain/evidence.js:156` hashes `parameters`,
`raw_result` and `normalized_result` — which contain `parameters.path`, `output_directory`, every
`task.path` and every per-run `provider_blob_id` — while excluding only `subject.local_path` /
`subject.name`. Measured: three identical-input after runs produced three different ids
(`ev_daafb11b…`, `ev_5edb2892…`, `ev_96c67b65…`) with identical payloads. R36-CL6's phrasing
("receipt identity = subject digest, not local_path") is therefore only half true at the envelope
level: the *subject* is digest-addressed, the *evidence id* is not. Consequence for verification:
an auditor must adopt the committed parameter strings to recompute a committed id; adopting the
carrier alone cannot. Both committed K2 ids do self-verify (§6), so this is a portability
calibration note, not a falsification.

**c. `carriers.json` mislabels K2's tree.** The frozen manifest calls K2
`synthetic standard-BE v4 gzip (tree2, symlink + unicode name)`. The bytes are ASCII: the
distinctive entry is `space name.txt` (`73 70 61 63 65 20 6e 61 6d 65 2e 74 78 74` — a U+0020
space, no non-ASCII byte) plus the symlink `var/lib/run-link -> ../../a/run.sh`. The carrier, oracle
and every counter binding are unaffected (no binding reads the `kind` string), so this is a stale
description only — but it is frozen and cannot be edited after the freeze.

**d. Fixed-consequence note (supporting a, not a defect):** the frozen P38-C1 clause "carries no
extraction gap" is unsatisfiable on any carrier containing an in-tree symlink, because REA never
publishes symlinks and always records one `unpublished-entry` gap (K2). Measured here on three
independent runs for K2. K1's receipt shows `after_gaps_empty true` (frozen counter receipt) — the
reason K1's dangling symlink produces no gap (the landed entry's `MaliciousSymlinkRemoved`
explanation) is the entry's claim and was **not** re-measured by this seat. The landed entry states
the same consequence ("'no extraction gap' is unreachable on any carrier with an in-tree symlink").

## 8. Limits

- I reproduced the *payload*, not the author's exact envelope bytes: `parameters.path`,
  `output_directory`, argv report/log/extract paths and per-run blob ids necessarily differ (§7b),
  so byte-for-byte `diff` of the JSON files cannot be expected and is not evidence either way.
  Every leaf of a full recursive diff is enumerated in `compare.txt` (14 leaves before, 76 after —
  all of them `evidence_id`, scratch path strings or per-run blob ids; zero semantic leaves).
- The committed before-receipts were produced under `/fast/scratch/hyaku/kaidoku-r38/l1-receipts/`,
  which no longer exists; I could not and did not re-run with the identical `output_directory`.
- Not exercised: K1/K3/K4 receipts (other seats), `sasquatch-v4be -be` cross-tool extraction, the
  C2 counter, and the REA MCP devices.
- Timing: each REA arm 1.7 s wall; no long-running jobs, no subagents.

## 9. Tooling record

Nothing installed, upgraded or removed. Used as-is: `npx` with the cached
`rea-agents@6.5.0` (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), unblob
26.6.4 (`~/.local/bin/unblob` → uv tool), node v24.21.0, `sasquatch` / `sasquatch-v4be` 4.5.1 left
untouched in `~/.local/bin` (present, used by the after-arm; stripped via `PATH` only, never moved).
No pacman transaction.

## 10. Retained evidence

`artifacts/R38W2ReproK2/` (lane-relative
`.ufo/waves/round-38/w2/artifacts/R38W2ReproK2/`), checksums in `artifact-sha256.txt`:

| file | what |
|---|---|
| `before-env.json`, `before-env2.json` | my two independent before-arm envelopes |
| `after-env.json`, `after-env2.json`, `after-env3.json` | my three independent after-arm envelopes |
| `compare.txt` | graded-field comparison + full recursive differing-leaf lists + oracle table + determinism + argv/stdout |
| `xpin.txt` | evidence-id recompute for my 2 envelopes and the 2 committed ones |
| `c1-counter-v1.py` | frozen counter bytes used for the judged run (sha256 `a7a62b09…`) |
| `c1-v1-3b960fe5.json`, `c1-v1-0fc61133.json` | judged-rule counter receipts (both exit 1, 3/4) |
| `c1-counter-3b960fe5.json` | in-tree (amended) counter receipt for contrast (4/4, still `met_target false`) |
| `commands.txt` | exact commands, exit codes, timings |

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2ReproK2` removed on exit; every cited byte is copied
into the artifact directory above.

## 11. Files changed by this seat

- `.ufo/waves/round-38/w2/R38W2ReproK2.md` (this report)
- `.ufo/waves/round-38/w2/artifacts/R38W2ReproK2/` (12 files listed in §10)

Nothing else in the lane was written; `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`,
`LOG.md` and `tools/` were read only (via `git show` at fixed revisions).

Disclosure, bounds: the first `write` of this report used a lane-relative path against the fleet
root cwd and therefore landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-38/w2/R38W2ReproK2.md`
(outside the lane) at 03:58. It was moved into the lane immediately (`mv`, then `rmdir` of the two
directories that write had created, which held no other file) and the stray tree no longer exists
(`ls -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-38` → "No such file or directory"). No other
file outside the lane was touched, and nothing in that stray location remains.
