# R38ExecBeforeArmRecheck — R37 before-arm re-check on K1–K4

Seat: executor (leaf), round 38 wave 1. Lane `kaidoku-shokunin`.
Lane HEAD during measurement: `cb4326b2aa4c2024af0651fe6115b82d0c4de3df`; frozen claims
`e059ca9391642d5b71b6662cabcbdce0d9308719`; carriers/oracles at base `77091b49…`.
Nothing was installed, nothing was mutated in VCS, no frozen file was touched.

## Verdict

**The R37 promised before-arm reproduces on all four carriers.** With every PATH component
holding a `sasquatch`/`sasquatch-v4be` executable removed, REA `extract-firmware`
(rea-agents 6.5.0, unblob 26.6.4) on K1/K2/K3/K4 returns
`extraction_gaps[].kind = missing-extractor-dependency`, `dependencies = ["sasquatch-v4be"]`,
`handler = squashfs_v4_be`, `coverage = partial`, `published_bytes = 0`, **0 files published**
— byte-for-byte the shape recorded at `plans/round-37-claims.md:43-45`.

Therefore the R38-C1 corrected premise is **refuted**: `sasquatch-v4be` is a hard external
dependency of unblob 26.6.4's `squashfs_v4_be` extractor, and unblob does not handle standard
BE v4 without it. The `Not claimed` paragraph (freeze-commit lines 61-65) and the
predicate parenthetical ("run with stock unblob 26.6.4; no external extractor dependency",
freeze-commit lines 26-27) both state the opposite of what is measured.

**Second, independent falsifier (orthogonal to PATH).** With the extractor installed, K2 still
reports a non-empty `extraction_gaps`: one `unpublished-entry` for
`firmware.bin_extract/var/lib/run-link`, a *live* in-image symlink
(`K2/src/var/lib/run-link` mode 120000 → `../../a/run.sh`, target inside the image). P38-C1
binds `after_gaps_empty`, so K2 cannot match even in the after arm; the projection is
K1/K3/K4 matched, K2 unmatched → `carriers_matched == 3`, target `== 4` unreachable.

## Method

- **Strip rule.** For each `$PATH` component `d`: drop `d` iff `-x "$d/sasquatch"` or
  `-x "$d/sasquatch-v4be"`. Exactly one component qualified:
  `/home/vgpnk/.local/bin` (also holds `unblob`, which is why `REA_UNBLOB_COMMAND` is
  absolute). Under the stripped PATH `command -v sasquatch`, `… sasquatch-v4be` and
  `… unblob` all print `ABSENT`; `node`/`npx` still resolve to the fnm dir, `python3` to
  `/usr/bin`. Full text: `artifacts/R38ExecBeforeArmRecheck/path-strip.txt`.
- **Treatment / control.** Treatment = stripped PATH; control = stock PATH, same command, same
  carrier, fresh output root. Both arms ran the harness
  `tools/round-38/c1-run.sh after CARRIER OUTDIR SCRATCH` (HEAD bytes) and, as a second
  independent reproduction, the identical `npx -y rea-agents@6.5.0 extract-firmware --format
  json` argv that the harness executes. 4 carriers × 2 arms × 2 reproductions = 16 cells.
- **Outcome is read from the envelope, not the exit code** (see F4).
- `HYAKU_SCRATCH=/fast/scratch/hyaku`, seat scratch
  `/fast/scratch/hyaku/kaidoku-r38/R38ExecBeforeArmRecheck`, `TMPDIR` inside it; removed at the
  end after copying the cited envelopes into the artifact dir.

## Measurements (16/16 cells agree between the two reproductions)

| carrier | PATH | exit | chunk handlers | extraction_gaps | coverage | published bytes | files | oracle hits | P38-C1 projection |
|---|---|---|---|---|---|---|---|---|---|
| K1 | stripped | 0 | `squashfs_v4_be` | `missing-extractor-dependency` `["sasquatch-v4be"]` | partial | 0 | 0 | 0/5 | unmatched |
| K1 | stock | 0 | `squashfs_v4_be` | *(none)* | partial | 9656 | 5 | 5/5 | **would match** |
| K2 | stripped | 0 | `squashfs_v4_be` | `missing-extractor-dependency` `["sasquatch-v4be"]` | partial | 0 | 0 | 0/3 | unmatched |
| K2 | stock | 0 | `squashfs_v4_be` | `unpublished-entry` (`firmware.bin_extract/var/lib/run-link`) | partial | 10283 | 3 | 3/3 | **unmatched (gap)** |
| K3 | stripped | 0 | `squashfs_v4_be` | `missing-extractor-dependency` `["sasquatch-v4be"]` | partial | 0 | 0 | 0/4 | unmatched |
| K3 | stock | 0 | `squashfs_v4_be` | *(none)* | complete | 28 | 4 | 4/4 | **would match** |
| K4 | stripped | 0 | `squashfs_v4_be` | `missing-extractor-dependency` `["sasquatch-v4be"]` | partial | 0 | 0 | 0/4 | unmatched |
| K4 | stock | 0 | `squashfs_v4_be` | *(none)* | complete | 28 | 4 | 4/4 | **would match** |

Files published, stock arm (relative to `<out>/firmware.bin_extract/`, oracle suffix match
per the counter's `matched()` rule, sha256 equality):

- K1: `bin/run`, `docs/deep/nested/file.dat`, `docs/readme.md`, `empty`, `hello.txt` (5/5, 9656 B)
- K2: `a/run.sh`, `space name.txt`, `var/lib/data.bin` (3/3, 10283 B)
- K3: `apple1.txt`, `apple2.txt`, `apple3.txt`, `apple4.txt` (4/4, 28 B)
- K4: identical to K3 (4/4, 28 B)

Subject digests equal the frozen pins for all four carriers (`1cfb6c33…`, `403cb0a8…`,
`9c7c523c…`, `a29ddc15…`), provider `unblob` / `Unblob` version `26.6.4`, operation
`extract_firmware` in every cell. All 8 harness envelopes recompute to their stored
`evidence_id` under the pinned `tools/round-27/xpin-attribute.mjs` 6.5.0 rule (8/8 `both`, see
`xpin-recompute.txt`), so the stock-arm envelopes for K1/K3/K4 are directly usable as
`after.json` drafts; K2's is not (gap).

## Mechanism (why the premise really is "external extractor required")

- `unblob/handlers/filesystem/squashfs.py:24-26` — `SquashFSExtractor.EXECUTABLE = "sasquatch"`,
  `V4BE_EXECUTABLE = "sasquatch-v4be"`; `:39-50` picks `sasquatch-v4be` for
  `Endian.BIG` + version 4 and appends `-be` when the image is not AVM
  (`is_avm = header.bytes_used == header.mkfs_time`); `:65` wraps
  `Command(executable, *commands_args)`; `:68-69` `get_dependencies()` returns both executables.
- `unblob/extractors/command.py:70-73` — a `FileNotFoundError` from the exec is converted to
  `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())`; `:101-102`
  `Command.get_dependencies()` returns `[self._executable]`, which is exactly why the reported
  dependency list is `["sasquatch-v4be"]` alone (not both).
- Runtime confirmation without REA in the loop
  (`artifacts/…/unblob-direct.txt`): `unblob --extract-dir … K3/carrier.bin` with the stripped
  PATH ends with severity `ERROR` / `ExtractorDependencyNotFoundReport` and publishes no files;
  the same command on the stock PATH publishes `apple1..4.txt`.
- The dependency table itself flips: `unblob --show-external-dependencies` prints
  `sasquatch ✗`, `sasquatch-v4be ✗` under the stripped PATH and `✓`, `✓` under the stock PATH
  (`path-strip.txt:18-53`).
- Alternative extractors do not cover it: `7z l K3/carrier.bin` → exit **2**
  ("Cannot open the file as archive", 7-Zip 26.04); `unsquashfs -l K3/carrier.bin` → exit **1**
  ("Can't find a valid SQUASHFS superblock", unsquashfs 4.7.5). Both carriers are genuinely
  big-endian (`file` magic in the unblob report: "Squashfs filesystem, big endian, version 4.0,
  zlib compressed …"), so this is the standard-BE path the claim is about.

## Findings

- **F1 (claim-fatal, calibration).** R38-C1's premise is wrong in both places it is stated
  in freeze v1 (`git show e059ca93:plans/round-38-claims.md`, lines 26-27 and 61-65). Measured:
  the before-arm reproduces on K1,
  K2, K3 and K4; no external extractor is *not* equivalent to this; `sasquatch-v4be` must be
  present on PATH for any after-receipt to exist. Whatever produced the round-37-to-38
  "corrected premise" probe did not actually remove the extractor (same class of mistake as
  R37-CL1: a receipt described but not measured/committed).
- **F2 (claim-fatal, independent of F1).** P38-C1's `after_gaps_empty` binding is unsatisfiable
  for K2 by construction: K2's frozen tree carries a *resolving* symlink
  (`var/lib/run-link → ../../a/run.sh`), REA refuses to publish link entries, so the receipt
  always carries `unpublished-entry`. `carriers_matched` can reach at most 3 even with the
  extractor installed. If K2 is to stay in the carrier set, the predicate's gap clause has to
  exempt `unpublished-entry` — and that is a pre-freeze decision, not a wave-1 one.
- **F3 (instrument, already fixed but not in the freeze).** The harness bytes at the freeze
  commit contain `mkdir -p "$OUT"` in `after` mode; REA's `SafeOutputTree.create` does an
  exclusive `mkdir` of the output root, so those bytes always fail. Measured from
  `git show e059ca93:tools/round-38/c1-run.sh` with the frozen code and a fresh run:
  exit **1**, `code=execution_failure`, `details.diagnostics.reason = "Extraction output root
  already exists"` (`envelopes/frozen-harness-bytes-failure-K3.json`). HEAD `cb4326b2`
  ("round-38: harness fix …") replaces it with `rm -rf "$OUT"` and works; all measurements here
  use HEAD bytes. Consequence for the L1: the freeze commit does not contain a runnable
  after-instrument, so the claims doc should name `cb4326b2` (or the fix should be folded into
  the freeze record) before any after-receipt is scored.
- **F4 (calibration, methodological).** Every cell — including the six zero-output before-arm
  cells — exits **0**. REA reports a missing extractor inside a successful envelope, so any
  check that gates on exit status, or a harness caller that infers success from `$?`, silently
  accepts "nothing extracted". The counter is safe (it reads the envelope), but the round-38
  wave artifacts should state this explicitly.
- **F5 (minor, narrative).** K1's stock arm has `gaps == []` yet `coverage == "partial"`: the
  image contains a dangling symlink (`K1/src/link-to-hello → ../hello.txt`, target outside the
  tree), which unblob extracts but cannot publish as a *resolving* entry and does not gap.
  Not a P38-C1 binding, but any prose asserting "complete coverage" for K1 would be false;
  K3/K4 are the only `complete` carriers.

- **F6 (operational caution).** `unblob` writes `unblob.log` into its **current working directory**.
  My step-5 no-REA reproductions were launched from the lane root, which created
  `kaidoku-shokunin/unblob.log` (3617 B); I deleted it immediately and re-verified
  `git status --porcelain` shows nothing of mine outside the wave dir. REA-launched runs
  (harness `after`) did not do this — REA gives unblob its own cwd. Anyone running unblob
  directly must `cd` into scratch or pass `--log-file`.

## Freeze drift observed while measuring (not mine to reconcile)

While this seat ran, `plans/round-38-claims.md` and `tools/round-38/c1-counter.py` were modified
in the worktree by other seats (freeze **v2**, header "the first freeze (v1) declared the
round-37 missing-extractor-dependency before-arm 'does not reproduce' … Wave-1 discovery
(R38CrossToolK1, measured) falsified that premise"). My finding is independent corroboration of
that amendment: I reached it by measuring the PATH-stripped before-arm on all four carriers
through the harness and through a no-REA unblob run, before reading the v2 diff. All citations
above are pinned to the freeze-commit bytes so they stay exact; the working-tree v2 restatement
is not something this seat scored.

## Suggested corrected-premise wording (advisory only; the frozen predicate is not mine to change)

> REA `extract-firmware` (rea-agents 6.5.0) on standard big-endian SquashFS v4 runs unblob
> 26.6.4's `squashfs_v4_be` handler, which shells out to the external `sasquatch-v4be` binary
> with `-be`; with that binary off PATH the run returns `missing-extractor-dependency`
> (`dependencies=["sasquatch-v4be"]`), `coverage partial`, zero published bytes on all four
> carriers. With it installed, K1/K3/K4 publish every oracle regular file with no gap, while K2
> publishes 3/3 regular files plus an `unpublished-entry` gap for its in-image symlink.

## Artifacts (drafts; under the wave dir, not committed — the L1 integrates)

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/w1/artifacts/R38ExecBeforeArmRecheck/`

- `matrix.json` — all 16 cells: path mode, carrier, subject sha256 + pin equality, evidence id,
  provider, handlers, gaps (kind/deps/relative_path/handler), coverage, published bytes, file
  list, oracle hits, per-binding P38-C1 projection.
- `envelopes/h-K{1..4}-{stripped,stock}.json` — harness envelopes (the specified command).
- `envelopes/direct-K{1..4}-{stripped,stock}.json` — second, independent reproduction.
- `envelopes/frozen-harness-bytes-failure-K3.json` — F3 evidence.
- `xpin-recompute.txt` — 8/8 evidence ids recompute (`both`).
- `path-strip.txt` — strip rule, PATH before/after, resolve checks, both dependency tables,
  installed extractor versions.
- `unblob-direct.txt` — unblob-only reproduction (no REA) for both PATH modes.
- `harness-freeze-vs-head.diff` — freeze `e059ca93` vs HEAD `cb4326b2` harness bytes (21 lines).
- `commands.txt` — exact commands, versions, and the read-only git checks.

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38ExecBeforeArmRecheck` was removed after the copy;
nothing cited above resolves to scratch or `/tmp`.

## Limits

- The measurement is over `corpus/evidence/round-37/c1/K{1..4}` at base `77091b49`, which the
  worktree still matches (`git status --porcelain corpus/evidence/round-37/c1` empty, and every
  subject digest equals the frozen pin).
- "No external extractor is required" was tested by removing the only PATH component that
  provides one, plus a source reading of the handler and a no-REA reproduction. I did not test
  exotic routes (e.g. a caller-injected `PATH` inside unblob's own launcher, or a patched
  sasquatch hardlinked under another name) — none exists on this host.
- `[INFERENCE]` The most likely origin of the wrong R38 premise is a "stripped" probe whose
  strip rule did not actually match (`sasquatch-v4be` lives in the same directory as `unblob`,
  so a probe that borrowed `PATH` from the REA launcher, or stripped only after the child was
  spawned, would still find it). I cannot reconstruct the round-37/38 probe shell, so this is
  offered as a hypothesis, not a finding.
- Tooling: nothing installed or upgraded this seat (all binaries — `unblob` 26.6.4,
  `sasquatch`/`sasquatch-v4be` 4.5.1, `7z` 26.04, `unsquashfs` 4.7.5, node/npx — pre-existing).
