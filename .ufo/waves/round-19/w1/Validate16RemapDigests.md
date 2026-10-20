# Validate16RemapDigests — r18 remapped receipts re-created and re-validated (round 19, wave 1)

Seat: `KaidokuR19.Validate16RemapDigests`. Half two of R18-VALIDATOR-DIGEST: the r18 remapped
receipt copies were written to `/tmp` and never retained (`corpus/lessons/round-18.md:55`;
`.ufo/waves/round-18/evidence/validate16/summary.json:68-78`).

Verdict: **COMPLETE — 8/8 copies re-created and retained, 8/8 re-validate exit 0, no divergence
from the r18 summary.** Every copy is byte-identical to the surviving r18 copy *and* reverse-remaps
byte-exact to its `da64646` receipt blob. Observed base: `git -C /tmp/kr19-KaidokuR19.Validate16RemapDigests
rev-parse HEAD` → `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (exit 0).

Axes named before measuring: **calibration** (do the r18 numbers re-occur from bytes, not from the
summary?), **freshness** (are those bytes still the `da64646` bytes today?), **depth** (can a third
party verify the remap without the r18 author's `/tmp` memory?).

Labels (8, from `.ufo/waves/round-18/evidence/validate16/summary.json:3-10`):
`calib-esbuild-0.25.12`, `calib-shfmt`, `pro-aether`, `pro-containerd-shim`, `pro-esbuild-0.21.5`,
`pro-esbuild-0.27.7`, `pro-notesmd-cli`, `pro-op`.

## 1. The re-creation is exact, not plausible (observation)

The recorded remap is a byte-prefix rewrite only: `from` = the lane root, `to` =
`/tmp/r17-validate16.MWZBce`, "16 occurrences per receipt" (`summary.json:71-78`). Applied to the
`da64646` receipt blob, that rule is deterministic; the only free variable is the target root.

- **[O] 16 occurrences, 0 left.** Each `da64646` receipt blob contains the lane prefix exactly 16
  times; each regenerated copy contains the target prefix exactly 16 times and the lane prefix 0
  times (measured per label).
- **[O] The r18 target still exists** (`/tmp/r17-validate16.MWZBce`, mode 700, files dated
  12:26-12:31). So exactness was checked against the r18 artifacts themselves, not only reconstructed:
  `cmp` of my 8 retained copies against `/tmp/r17-validate16.MWZBce/receipts/<label>.json` →
  **IDENTICAL ×8** (exit 0). This is stronger than r18's own reverse-remap check
  (`.ufo/waves/round-18/w2/ValidateRemapAttack.md:35`).
- **[O] Reverse-remap holds too.** Substituting the target prefix back to the lane root reproduces
  each `sha256(git show da64646:.ufo/waves/round-17/runs/<label>/receipt.json)` byte-for-byte
  (`copies[].source_receipt_sha256` in `digests.json` makes this checkable without `/tmp`).
- **[O] Nothing in the copies points into the lane.** `lane_prefix_occurrences_total 0` across all 8
  copies; the 167 distinct out-of-target absolute paths fall in exactly the four groups the r18
  summary already names (`summary.json:72-76`): `/usr/bin/…` carriers (2 paths), the
  `/home/vgpnk/.local/bin/notesmd-cli` carrier, `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/…`
  typeinfo, `/home/vgpnk/Projects/kimi-code/node_modules/…`, plus 8 `/tmp/kr17-rea-*` `session_dir`
  strings (one per receipt; 16 occurrences with the duplicated `retained_logs`/`steps` nodes) that
  are log-content binding only (never opened).

Retained file: `.ufo/waves/round-19/evidence/validate16-remap/copies/<label>.receipt.json`
(108 KB class each; digests in `digests.json`).

## 2. The payload tree is the da64646 tree (observation)

The remap only relocates path strings; validation still needs the bytes under `to`. Rebuilt from
the recorded recipe (`summary.json:78`): `git archive da64646 .ufo/waves/round-17 | tar -x` plus
`git show da64646:.ufo/waves/round-16/selection.py` (file sha256 `6917da09…`). Compared against the
surviving r18 target payload (`receipts/`, `val/`, `out/` excluded): **260 rebuilt files, 260 target
files, 0 missing, 0 extra, 0 digest differences.** Manifest digest (sorted `sha256␠␠relpath` lines,
sha256 of that text) = `87f2beb8244b983a3c2123dbf3ce4cfcd49059472eff87a464e95325a17a2834`, recorded in
`digests.json` under `remap.tree_manifest_sha256` so a rebuilt tree can be checked later.

`to` holds the 9011581 validator and pins bytes: sha256 `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`
(= `summary.json:82`) and `9e9c7250…`.

## 3. Re-run of the 9011581 validator (observation)

Two runs per label, same tool bytes (`/tmp/r17-validate16.MWZBce/val/receipt-validate.py`, sha256
`618448…`), invoked `python3 -I -B <validator> <receipt>`, cwd inside my clone, stderr empty (0 bytes,
16/16 runs):

| run | receipt argument | exits | checks | findings |
|---|---|---|---|---|
| A (replication of the r18 invocation) | `/tmp/r17-validate16.MWZBce/receipts/<label>.json` | **0 ×8** | 341 ×8 | [] ×8 |
| B (the retained copies, this ticket) | `<clone>/…/validate16-remap/copies/<label>.receipt.json` | **0 ×8** | 341 ×8 | [] ×8 |

- **[O] A reproduces the r18 evidence exactly.** sha256 of each A stdout equals
  `summary.json` `stdout_sha256` for **8/8** (e.g. `pro-aether` → `0a013505…`).
- **[O] B differs from A in one field only** — the echoed `receipt` path. Substituting the A path
  back into B's stdout yields A byte-for-byte for 8/8; hence `matches_r18_stdout_after_receipt_path_substitution:
  true` per copy. The per-copy B stdout digests are recorded as `copies[].stdout_sha256`; the r18
  values remain visible as `copies[].r18_stdout_sha256` so the one-field delta is auditable.
- **Divergence from the r18 summary: none.** Exits 0/0, `checks_performed` 341/341, `findings` [] / [],
  `valid: true`, aggregate `{"invalid":0,"receipts":1,"unreadable":0,"valid":1}` for all 16 runs.

One stdout (B, `pro-aether`) verbatim:
```
{"counts":{"invalid":0,"receipts":1,"unreadable":0,"valid":1},"exit":0,"pins_available":true,
 "pins_path":"/tmp/r17-validate16.MWZBce/val/pins.py","receipts":[{"checks_performed":341,
 "findings":[],"kind":"carrier","receipt":"…/copies/pro-aether.receipt.json","status":"valid",
 "valid":true}],"tool":"receipt-validate.py"}
```
(reflowed for width; the B bytes are 521 B and hash to `76bb326b…`; the A bytes are 452 B, matching
the r18 retained file size.)

The 341 is the validator's own count (`check_required` 30 + `check_binding` 5 + pins compare 1 +
`pins_post` 146×2 + `walk_pairs` 13 — decomposition at `.ufo/waves/round-18/w2/ValidateRemapAttack.md`,
Q2). The receipts themselves carry **no `exit` key**; "exit 0" is the validator's verdict on those
bytes, not a receipt field (ground truth recorded at `.ufo/waves/round-18/w2/GateVALIDATE16.md`,
"Ground truth the gate must rest on").

## 4. Retention shape and what it closes

`digests.json` (this round) = `{source_rev, validator_rev, validator_sha256, remap, copies}` with
`copies[] = {label, sha256, validator_exit, stdout_sha256, source_receipt_sha256, checks_performed,
r18_stdout_sha256, matches_r18_stdout_after_receipt_path_substitution}` and `remap` = the recorded
remap object verbatim plus `occurrences_per_receipt`, `tree_files`, `tree_manifest_sha256` and a
`replay` block (validator/pins paths, argv, cwd).

This closes the *retention* half of R18-VALIDATOR-DIGEST — the r18 run is no longer reconstructible
only from prose (`.ufo/waves/round-18/w2/ValidateRemapAttack.md`, D3; `corpus/QUALITY.md:28` requires
argv, revision, stdout/stderr and exit). A gate can now, from Git alone:
`sha256(copy) == copies[].sha256`; `sha256(git show da64646:…/receipt.json) == copies[].source_receipt_sha256`;
and either run the 9011581 validator on the copy where the recorded `to` exists, or rebuild `to`
from `da64646` and check `tree_manifest_sha256` before running.

## 5. Limits (labelled; none affects the verdict)

- **[O/I] The payload tree is still `/tmp`-resident.** The copies are retained; the 260 payload files
  are not. This is the recorded remap target (`summary.json:77`), so it is reproduced, not changed.
  The rebuild recipe + manifest digest make the tree reconstructible and checkable, but a validator
  re-run on the retained copies needs the tree present. If the L1 wants a lane-internal replay, the
  recipe is the one in §2; nothing else in the copies depends on the target's location.
- **[O] The r18 target survived only by chance.** It is 8/8 identical today; had it been cleaned, exact
  re-creation would still have been provable from `da64646` (the reverse-remap leg), but not the
  `cmp` against the r18 artifacts. Recorded because "the tmp dir exists" is not a durable premise.
- **[O] stdout digests are argv-path sensitive by construction** (the validator echoes the receipt
  argument and its own sibling `pins.py`, `receipt-validate.py` `PINS_PATH`). `replay.argv`/`cwd`
  pin the exact invocation behind `copies[].stdout_sha256`.
- **[O] The validator proves present bytes, not run-time bytes** — its own stated limitation
  (`9011581:.ufo/waves/round-17/tools/receipt-validate.py:34-37`). What was re-established is that the
  committed `da64646` blobs, materialised at the recorded target, pass today.
- **[O] Selftest case count differs by revision.** `9011581` prints `SELFTEST: CLEAN cases=9`; the
  r18 hardening revision `b2aad08` prints `cases=18` (`.ufo/waves/round-18/w2/ReceiptValidateRerun.md`).
  This ticket names `9011581`; 9 is that revision's case count, not a regression.

## 6. Commands and exit codes (observed)

| # | Command (abridged) | Exit |
|---|---|---|
| 1 | `git clone -q --no-hardlinks LANE /tmp/kr19-KaidokuR19.Validate16RemapDigests`; `checkout --detach 8a8da7e…`; `rev-parse HEAD` | 0 / 0 / 0 |
| 2 | `git show 9011581:…/receipt-validate.py \| sha256sum` → `618448…`; same for `pins.py` → `9e9c7250…` | 0 |
| 3 | regenerate 8 copies from `da64646` blobs (16 prefix replacements each) and compare with `/tmp/r17-validate16.MWZBce/receipts/*`: `regen==surviving True` ×8, lane-prefix 0 | 0 |
| 4 | `git archive da64646 .ufo/waves/round-17 \| tar -x -C …`; `git show da64646:.ufo/waves/round-16/selection.py > …` | 0 / 0 |
| 5 | tree compare (260 files): `missing 0, extra 0, digest_diff 0`; manifest `87f2beb8…` | 0 |
| 6 | write 8 copies to `…/validate16-remap/copies/<label>.receipt.json` | 0 |
| 7 | validator run A on `$T/receipts/*` and run B on the retained copies: `exit 0` ×16, `341` checks, `0` findings, stderr 0 B; A stdout sha == r18 recorded ×8; B == A modulo receipt path ×8 | 0 |
| 8 | `cmp` retained copy vs `$T/receipts/<label>.json` → `IDENTICAL` ×8 | 0 |
| 9 | `python3 -I -B .scratch/val9011581/receipt-validate.py --selftest` (cwd = clone) → last line `SELFTEST: CLEAN cases=9` | **0** |
| 10 | write `digests.json` (generator asserts exit/checks/findings, reverse-remap and the stdout substitution) | 0 |

Selftest, exact last line and exit:
```
SELFTEST: CLEAN cases=9
SELFTEST_EXIT=0
```

Delivered patch (`.ufo/waves/round-19/w1/patches/KaidokuR19.Validate16RemapDigests.patch`,
sha256 `48f13ae436a52faf43fe590e5da1ccc093e8aceef0739021b1d5563498900dea`, 15278 lines,
`git apply --check` against a fresh baseline clone → exit 0):

```
$ git -C /tmp/kr19-KaidokuR19.Validate16RemapDigests diff --cached --stat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
 .../copies/calib-esbuild-0.25.12.receipt.json      | 1888 +++++++++++++++++++
 .../copies/calib-shfmt.receipt.json                | 1888 +++++++++++++++++++
 .../copies/pro-aether.receipt.json                 | 1888 +++++++++++++++++++
 .../copies/pro-containerd-shim.receipt.json        | 1888 +++++++++++++++++++
 .../copies/pro-esbuild-0.21.5.receipt.json         | 1888 +++++++++++++++++++
 .../copies/pro-esbuild-0.27.7.receipt.json         | 1888 +++++++++++++++++++
 .../copies/pro-notesmd-cli.receipt.json            | 1888 +++++++++++++++++++
 .../validate16-remap/copies/pro-op.receipt.json    | 1890 +++++++++++++++++++
 .../evidence/validate16-remap/digests.json         |  110 ++
 9 files changed, 15216 insertions(+)
```
(exit 0). The patch carries the evidence only; this report is written straight to the lane, per
`contract.md:17-18`.

No installs or upgrades (nothing was missing; no pacman transaction attempted). No REA or Ghidra run,
no carrier execution, no `jj` or git write in LANE, no write to the fleet repo. The only LANE writes
are this report and `w1/patches/KaidokuR19.Validate16RemapDigests.patch`; the patch carries the 8
copies and `digests.json` only.

## Anchors

- `.ufo/waves/round-19/contract.md:8-21` (Writers, clone, patch command)
- `.ufo/waves/round-18/evidence/validate16/summary.json:3-10,68-78,80-82`
- `corpus/lessons/round-18.md:55` (the `/tmp`-not-retained statement)
- `.ufo/waves/round-18/w1/RevValidatorPaths.md:103-104` (absolute-path resolution)
- `.ufo/waves/round-18/w2/ValidateRemapAttack.md:21,34-35` (stdout normalization, reverse-remap)
- `.ufo/waves/round-18/w2/GateVALIDATE16.md` (self-authored evidence; receipts carry no `exit`)
- `corpus/QUALITY.md:28` (execution evidence retention)
- `9011581:.ufo/waves/round-17/tools/receipt-validate.py:34-37` (live-bytes limitation), `:60-68` (required sets), `:206-232` (file checks), `:267-269` (pins precedence)

Report: .ufo/waves/round-19/w1/Validate16RemapDigests.md
