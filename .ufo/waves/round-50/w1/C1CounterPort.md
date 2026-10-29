# C1CounterPort — report (round 50, wave 1, pre-freeze draft)

## Verdict

**Ported and green offline; not run on any vendor carrier or against real REA.** `tools/round-50/c1-counter.py` (draft, in
`.ufo/waves/round-50/w1/C1CounterPort/tools/round-50/`, sha256 `716287fe77b30daa2d67b57b57e129196d20d6f7e328fa8d7667d6fcd974c305`,
4807 lines) is the round-41 counter on the little-endian layout, with the non-v1/v2 round-49 hardening carried over and
the six L1 folds (shortcut critique S1-S11) added. `--selftest` exits 0: **168 cases (17 green / 151 red), 6 path probes,
8 root probes, 43 spec/layout/runner/oracle probes, 0 failures.** 24 single-line mutants of the counter (M1-M23 plus the
equivalence probe M14a) were run through the selftest: **23 killed, 1 provably equivalent** (M14a, below); M1-M14 ran on an
earlier build of the same file, M15-M23 on the final one. Every delta against round 41 is in
`PORT-DELTA.md`. Not done, and why: see "Not done" (the real REA run, the real-image `unsquashfs` re-derivation, `--selftest-rea`,
a sasquatch hash freeze).

## Top findings (what the L1 should act on)

1. **L1 items (1)-(6) are all implemented and each has selftest cases and a killing mutant** (table below). The
   counter now runs REA as `node <--pkg65>/<bin>`, binds `unblob --version == 26.6.4`, resolves `sasquatch`/`node` on
   `FIXED_PATH` only and records their paths/sha256 in `res['rerun_toolchain']`; exits 2 `counter_not_frozen` when the running counter
   differs from FREEZE; reads the full git history for receipt freshness; re-derives the oracle with `/usr/bin/unsquashfs`
   4.7.5 at scoring time; requires `projection: plus-extractor` frozen; and words the marker as a constant of the pinned bytes.
2. **Round 41 never read carriers.json `rea_parameters`**: the rerun replayed the *committed receipt's own* `parameters`, so a
   receipt made at any depth/budget matched its own rerun. The port freezes `rea_parameters` (`max_depth 1`, `max_output_bytes`,
   `max_output_files`; mandatory), adds clause `parameters_ok` (receipt == frozen) and replays the frozen values. The L1's measured
   a7530 flags (`--max-output-files 100000 --max-output-bytes 536870912`) belong in `rea_parameters`.
3. **Real-data checks on the four real round-41 receipts** (`receipts/differential-check.json`, the shared machinery only, HANDLER
   patched to the BE handler for that check): the port's root, `oracle_hits`, disposition (612 gaps / 4 removals / 1017 non-regular entries on V4),
   `nonregular_published` and projection are **identical** to round 41's; the hardened clauses hold on real bytes: extra published files
   0 on all four, all 4 real `MaliciousSymlinkRemoved` links resolve under the new trusted-run-root rule, `path_shape_ok` true. The
   selftest also found a vacuity in my own first draft: the stem `…-avm-le-…` itself spells the LE-AVM token, so the frontier-note binding
   was satisfied by the stem alone; the token is now searched with the stem removed (mutant M8 killed).

## Decisions / alignments the L1 must make (all are one-line constants at the top of the counter)

* **Where carriers.json / gap-rule.json live.** The plan (`## Frozen carriers`) says `tools/round-50/carriers.json`; the spawn text said
  `.ufo/waves/round-50/c1/`. I followed the plan (`CARRIERS`, `GAPRULE`).
* **Entry stem** is my placeholder `2026-10-28-r50-avm-le-squashfs-core` (`ENTRY`, `STEM`): the plan names none.
* **carriers.json required keys**: `claim R50-C1`, `target 4`, `projection "plus-extractor"`, `rea_parameters {max_depth 1, max_output_bytes, max_output_files}`,
  four carriers a7530/a7590/c6490/c6430 each with `id`, `sha256`, `oracle`, `nonregular` and either `path` or `external {url, image_sha256, member, member_sha256, length}`.
  `oracle` tables are **3 columns `rel TAB sha256 TAB size`** and every listed oracle/nonregular table must already exist at the freeze (`frozen_tables_valid`).
* **`tools/round-50/rea-pkg.json`** is not required: the counter takes the first of `tools/round-50|49|42/rea-pkg.json` present at the freeze; `tools/round-42/rea-pkg.json`
  matches the present package (`package.json` a5003023…, lock d42d56f0…, measured here). Absent at the freeze → exit 2.
* The harness side (`c1-run.sh`, not in my scope) must produce receipts with the frozen `rea_parameters`, scratch under `/fast/scratch/hyaku/kaidoku-r50/`, `TMPDIR` = parent of
  `output_directory` (the trusted-run-root rule reads `report.link` under it, as the real round-41 V4 receipt does), and the same node + `--pkg65` execution as the counter rerun.
* `FIXED_PATH` is host-specific (`~/.local/share/fnm/node-versions/v24.21.0/installation/bin` verified present; `sasquatch`/`unblob` in `~/.local/bin`).

## L1 fold-ins (1)-(6): status

| # | request | status | selftest evidence | killing mutant |
|---|---|---|---|---|
| 1 | rerun = node + `--pkg65` package, no npx; unblob `--version` == 26.6.4; child sasquatch path/sha256 recorded; shim PATH must not satisfy | **done** (`rea_entry`, `toolchain_record`, `make_real_runner(.., pkg65)`) | 6 stub-package probes: node runs the entry with frozen flags and `PATH == FIXED_PATH`; unblob 26.6.3 refused; package 6.4.0 / no `bin` / missing `bin` file refused; a shim `sasquatch` first on the caller PATH is not resolved; no-sasquatch PATH refused | M18, M19, M22, M23 |
| 2 | `counter_not_frozen` | **done** (`CounterNotFrozen`, exit 2) | counter differs at freeze; no counter at freeze | M16 |
| 3 | `first_add` → `--full-history` | **done** (`all_adds`: `git log -m --full-history --diff-filter=A`; fresh = *all* adds descend from the freeze) | side-branch pre-freeze add + post-freeze re-add, merged with first parent = the later add: red (default history lists only the later add, reproduced); add only after freeze: green | M15, M21 |
| 4 | `oracle_rederived_ok` via `/usr/bin/unsquashfs` 4.7.5 | **done** (`rederive_oracle`, `OracleEnvError` exit 2) | table shrunk / extended / wrong sha / wrong size / nothing: red; tool unavailable: exit 2; real host unsquashfs on a lane-built LE image equals its source tree; missing tool / wrong version raise; no scratch left behind | M17 |
| 5 | `projection: plus-extractor` frozen in `carriers_spec_ok` | **done** | frozen `core`, `plus-mime`, unknown, missing: all `b:carriers_spec_ok` red (the round-41 "core accepts the fabrication" case is inverted) | M20 |
| 6 | marker wording; CTL-C1-4 red on `carrier_pin_ok` AND `layout_ok` | **done** (docstring + two cases) | standard-LE carrier planted under the genuine pin: red `carrier_pin_ok`, red `layout_ok` | M1 (marker), M2, M3, M11 (layout) |

## Not done / could not do (honest list)

* **Nothing was run against REA, the AVM images or the vendor carriers** (wave-1 rule). Unmeasured: (a) `node <pkg65>/scripts/rea.mjs extract-firmware …` against the *real* package (the runner is proven on a stub package only; npx runs the same `bin` file but I did not execute it);
  (b) `rederive_oracle` on a real 13k-file/172 MB rootfs (mode-0 files, hardlinks, sparse files, odd names) — the code does `chmod -R u+rwX` and streams hashes, but that is untested at scale;
  (c) `--selftest-rea` (ported: builds an LE AVM-marker member with host `mksquashfs`, `unsquashfs` oracle, REA twice) — **never executed**; run it before the freeze or drop it;
  (d) the real-image gap rule (sibling seat), real `depth-limited` gaps, and the wall time of 4 reruns + 4 re-derivations.
* **sasquatch hash is recorded, not enforced** (the plan pins no hash). If the L1 wants it enforced, a frozen `toolchain.sasquatch_sha256` would be a few lines; I did not add an unrequested required key.
* **The AVM marker adds no evidence** beyond `carrier_pin_ok` (as the L1 now words it); `layout_ok` is retained unchanged in code.
* The oracle re-derivation covers **regular files only**; non-regular rows (symlinks, dirs, devices) are not re-derived (an unprivileged extraction cannot make devices; symlink targets would need `-lls`).
* `--dev-arm`, `oracle_tool_ok` and the S138 `tree_ok` of round 49 are v1/v2-shaped and **not carried** (round-49 carry-over list is in PORT-DELTA §2/§3: carried = identity/verify-receipt, `--work`, FIXED_PATH, rea-pkg pin, handler equality, `under_root`, `path_shape_ok`, `evidence_envelope_ok`, size + extra-file in `oracle_hits_ok`, trusted run root for removal links, prefix provenance, merge-aware drift + blob equality, prior-pin tables; not carried = `gaps == []` for zero-non-regular oracles, committed-carrier mode check, census/tree digest, embedded GAP_RULE, dev arm).
* Tooling: no installs, no pacman, no downloads. A bulk splice script (`port-build/build.py`, scratch-driven Python, not the `edit` tool) assembled the file from fragments over the pristine round-41 text; the mechanical regex transforms it applies are listed in PORT-DELTA §1.

## Receipts (exact commands, exit codes, sha256; all under the seat dir, UTC)

| what | command (from the seat dir; scratch `S=/fast/scratch/hyaku/kaidoku-r50/C1CounterPort`, `TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku`) | exit | output sha256 |
|---|---|---|---|
| the counter | `sha256sum tools/round-50/c1-counter.py` | 0 | `716287fe77b30daa2d67b57b57e129196d20d6f7e328fa8d7667d6fcd974c305` |
| selftest | `python3 -I -B tools/round-50/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work $S/work` (2026-10-29T00:36:16Z → 00:37:28Z) | **0** | stdout `receipts/selftest.stdout.json` `b4013a97bc8c57f1db71d1d64f851f6f065d3348c67068d3c0e22dd830656e28`; stderr empty |
| differential vs round 41 on the real round-41 receipts | `python3 -I -B differential-check.py tools/round-50/c1-counter.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c1-counter.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin` | 0 | `receipts/differential-check.json` `e4f350ed…ae21` |
| perf (synthetic 13,366-file / 852-link receipt) | `python3 -I -B perf-check.py tools/round-50/c1-counter.py …/tools/round-41/c1-counter.py` | 0 | `receipts/perf-check.json` `e9c2b020…3a8a` |
| mutation, new mutants M15-M23 | `python3 -I -B mutation-check.py tools/round-50/c1-counter.py $S <pkg65> M15 … M23` | 0 | `receipts/mutation-run3.txt` `40986535…0126` — 9/9 killed |
| mutation, first build M1-M14 | same, earlier build `c1b41a9b…` / `6896138…` | 0 | `receipts/mutation-run1-initial-build.txt` `e6874e15…aca6` — 13 killed, M14 survived (that build had no removal-root case) |
| M14 re-run with the removal-root case | `… mutation-check.py … M14 M14a` (build `c1b41a9b…`) | 0 | `receipts/mutation-m14-m14a.txt` `a96bed0d…c544`: **M14 killed** (both guards removed → "a removal whose link lies outside the run root cannot be mapped: want 1 got 0"); **M14a survives and is an equivalent mutant** (the `under_root` guard and the segment-prefix guard in `diagnostic_rel` are redundant with each other; removing one changes nothing; the third guard, the search window start, needs a link longer than the run root to be exercised, which the case uses) |
| receipt identity | `--no-rerun --json-out` → exit 2; `--verify-receipt` of it → 0; tampered → 1; missing file → 2; usage error → 2; base lane (`--rev=--freeze=7c678ae6…`, no carriers.json) → 2 `carriers.json absent at freeze` | as listed | (earlier build; not re-captured) |

Selftest scenario families (all in the 168): green (4 carriers, fresh receipts, docs), do-nothing, relabelled/fabricated receipts, oracle-only fabrication with re-minted id,
handler negatives (BE, v3, bare v4, mixed), layout negatives (standard LE, marker ±1, BE with marker, BE standard, `hsqs` over BE fields, gzip/lzma/zstd, v3.0/v4.1, bytes_used,
table order, truncation), extra file / size / shape / envelope / provenance / parameters, missing-extractor-dependency gap, carrier custody through `--carrier-cache`
(green / empty / absent / wrong bytes / wrong carve length), freeze walk (counter, plan, carriers, gap rule, tables, prefix additions, carried-over tools, xpin, evil merge,
side-branch merge, clean merge), prior pins (three sources), spec problems, removal disposition (adapted: links now under the run root; outside-root and root-`/` cases new), docs bindings
with window edges, plus L1 items 1-6.

## Files

`PORT-DELTA.md`; `tools/round-50/c1-counter.py`; `port-build/{build.py,frag/*}` (reproducible assembly; `build.py` writes the absolute deliverable path); `perf-check.py`, `differential-check.py`,
`mutation-check.py` (seat-local checks, not counter instruments); `receipts/*`. Scratch `S` removed after copying.
