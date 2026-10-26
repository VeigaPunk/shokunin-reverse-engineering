# R38RevengerPremise — why round 37 recorded a `missing-extractor-dependency` gap on K3

Seat: `R38RevengerPremise` (leaf, wave 1). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freezes: v1 `e059ca9391642d5b71b6662cabcbdce0d9308719` (the freeze named in my dispatch), then —
while this seat was measuring — v2 `79f69347` (03:29) and v3 `f1010f67` (03:32:55). Sections 1–2
measure the bytes; §3 states which freeze each divergence applies to and re-checks v3. Controls
`efd5c47a`; base `77091b49`.
Scope: reconstruct the round-37 "missing-extractor-dependency" premise; no corpus, counter, carrier,
oracle or VCS writes. Everything below was measured on this host on 2026-10-26 between 03:19 and
03:36 -03:00. Artifacts: `.ufo/waves/round-38/w1/artifacts/R38RevengerPremise/`.

## 0. Answer

The gap is **a property of the PATH the unblob child process sees, not of the carrier bytes and not
of any change over time**. unblob 26.6.4 has no in-process SquashFS extractor: `SquashFSv4BEHandler`
is hard-wired to `SquashFSExtractor(4, 0x73717368)`, which shells out to **`sasquatch-v4be -be`**
(`squashfs.py:41,527`), and `Command.extract` turns the resulting `FileNotFoundError` into
`ExtractorDependencyNotFoundReport(dependencies=["sasquatch-v4be"])`
(`command.py:69-71,101-102`), which rea-agents 6.5.0 maps to
`extraction_gaps[].kind = "missing-extractor-dependency"` (`cli.js:14816-14823`).

Nothing in the environment changed between the round-37 probe and now: the same unblob launcher bytes
(sha256 `0ce7b624…`, identical to the `executable_sha256` stored in the round-37 receipt), the same
`26.6.4`, the same rea-agents 6.5.0 package (installed 01:12:52, before the 02:34:47 round-37 launch),
and `sasquatch` / `sasquatch-v4be` were installed at 01:22:37 — also **before** the round-37 run. The
round-37 `before` arm worked because its committed harness filters PATH by *directory contents*
(`tools/round-37/c1-run.sh:43`), which removes `~/.local/bin`; a replication that filters PATH by
*component name* (`grep -v sasquatch`) leaves `~/.local/bin` in place, the extractor still resolves,
and the run silently becomes the **after** arm — "the gap does not reproduce".

**Class: environment delta (the child process PATH) with a probe artifact on top** (an ineffective
PATH filter in the round-38 v1 replication). A **version delta is excluded** by byte identity of the
engine and the package, and by re-deriving the round-37 receipt's evidence id under the pinned
rea-agents 6.5.0 rule. This matches the direction freeze v2 (`79f69347`) took and the measurements
behind it; §4 gives the row to paste, and §3.1/§3.4 give two things v3 (`f1010f67`) still leaves open.

## 1. Evidence chain

Scratch for every command was `/fast/scratch/hyaku/kaidoku-r38/R38RevengerPremise` (plus one short
`…Premise2` for the harness/decoy check), removed at exit; every produced envelope is copied into
the artifacts directory (names below are artifact-relative).

### 1.1 The handler requires the external extractor (code, not behaviour)

| anchor | observed |
|---|---|
| `unblob/handlers/filesystem/squashfs.py:25-26` | `EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"` |
| `…squashfs.py:41` | `executable = self.V4BE_EXECUTABLE` for `(Endian.BIG, 4)`, then `-be` unless the AVM heuristic at `:48` matches |
| `…squashfs.py:513,527` | `class SquashFSv4BEHandler(SquashFSv4LEHandler)`, `EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)` |
| `unblob/extractors/command.py:52,69-71` | `subprocess.run(list)` → `except FileNotFoundError: ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` |
| `…command.py:101-102` | `Command.get_dependencies()` → `[self._executable]`, i.e. exactly `["sasquatch-v4be"]` |
| `rea-agents/dist/cli-runtime/cli.js:14443` | `hostEnvironment: context.environment` — the unblob child inherits the caller PATH |
| `cli.js:14606,14816-14823` | `ExtractorDependencyNotFoundReport` inside `extraction_reports` → `kind: "missing-extractor-dependency"` with `dependencies` verbatim |
| `cli.js:15141` | unblob `exit_code === 1` is tolerated when a diagnostic exists, so a starved run still returns a normal envelope |

The single-name dependency list is a **signature**: a static dependency check would name all missing
tools (`unblob --show-external-dependencies` exits 1 and lists 15 commands, 8 of them ✗ —
`env-snapshot.txt`). A one-name list can only come from the extractor instance that actually ran and
failed to `execvp`.

### 1.2 The round-37 record is genuine but uncommitted (R37-CL1)

- `git show 77091b49:.ufo/waves/round-37/probes/rea-k3.json | sha256sum` →
  `c6fdc0d06ea8056fb03752f94c93504f901d8ced50efd316172c61017e746085` (identical to the working file).
- Recomputing it: `node tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0>` →
  `ev_3c3bf52c…` = its stored `evidence_id` (both pins). The receipt is authentic rea-agents 6.5.0
  output for K3: `coverage: complete`, `extraction_gaps: []`, four `apple1..4.txt`, chunk handler
  `SQUASHFS_V4_BE` in the unblob stdout, `engine.executable_sha256 = 0ce7b624…`.
- `git rev-list --all --objects | grep -i before` → **no** round-37 before-arm receipt on any ref.
  The before-arm exists only as prose in `plans/round-37-claims.md` ("Before-arm shape verified on
  K3 … `dependencies = ["sasquatch-v4be"]`, `coverage partial`, `published_bytes 0`").
- The receipt's `environment` field is `null`, so no receipt in the corpus attests a PATH. That is
  precisely why the premise could not be settled from committed bytes.

### 1.3 The committed round-37 instrument still produces both arms today

`bash tools/round-37/c1-run.sh before K <dir>` (its filter at `:43` drops every PATH dir containing
`sasquatch`/`sasquatch-v4be`, guard at `:44`), four carriers, all exit 0:

| carrier | gaps | coverage | published bytes | files | run record |
|---|---|---|---|---|---|
| K1 | `[missing-extractor-dependency, ["sasquatch-v4be"], squashfs_v4_be]` | partial | 0 | 0 | `sasquatch_v4be=""` |
| K2 | same | partial | 0 | 0 | `""` |
| K3 | same | partial | 0 | 0 | `""` |
| K4 | same | partial | 0 | 0 | `""` |

`bash tools/round-37/c1-run.sh after K3 <dir>` → exit 0, `gaps: []`, `coverage: complete`, four
apples with the oracle sha256 (`r37harness-after-K3.json`). So the identical instrument reproduces
the round-37 prose exactly, on all four carriers, with today's binaries.

### 1.4 The after arm through the frozen counting harness (fresh runs)

`bash tools/round-38/c1-run.sh after <carrier> <out> <scratch>` at `cb4326b2`, `REA_UNBLOB_COMMAND=~/.local/bin/unblob`:

| carrier | coverage | files | gaps | oracle hits |
|---|---|---|---|---|
| K1 | partial (one `MaliciousSymlinkRemoved` diagnostic; `link-to-hello` is a dangling/escaping symlink) | 5 | `[]` | 5/5 |
| K2 | partial (one `unpublished-entry` gap, see §3.1) | 3 | `[unpublished-entry]` | 3/3 |
| K3 | complete | 4 | `[]` | 4/4 |
| K4 | complete | 4 | `[]` | 4/4 |

All eight envelopes (`r38harness-{before,after}-K*.json`) recompute to their stored `ev_` ids under
the 6.5.0 rule, exactly like the committed round-37 receipt.

### 1.5 The environment did not change (version delta excluded)

| fact | observation | source |
|---|---|---|
| unblob engine | `26.6.4`; launcher `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` | `env-snapshot.txt`; equals the receipt's `engine.executable_sha256` |
| unblob install clock | 2026-10-25 18:10:59 -03:00 | mtime |
| rea-agents | `rea-agents 6.5.0`, npx package mtime 2026-10-26 01:12:52 -03:00 (unchanged after this seat's `npx -y` runs) | `env-snapshot.txt` |
| sasquatch binaries | `~/.local/bin/sasquatch`, `~/.local/bin/sasquatch-v4be`, both 2026-10-26 01:22:37 -03:00, `unsquashfs version 4.5.1`; no other copies in `/usr/local/bin`, `/usr/bin`, `~/.local/bin` | `env-snapshot.txt` |
| round-37 launch | `2026-10-26T02:34:47-03:00` (driver digest in `corpus/lessons/round-37-verifier-spotcheck.md`) | — |
| PATH sources | `~/.bashrc` (2026-10-24) exports `~/.local/bin` first and sets `REA_UNBLOB_COMMAND`; `~/.profile`/`~/.bash_profile` (2026-10-22) do the same | `env-snapshot.txt` |

Every input that could constitute a "then vs now" delta predates the round-37 run. There is no time
axis on which the gap could have appeared or disappeared.

### 1.6 The two filters that explain "fresh runs now show none"

`path-filter-demo.txt` (K3, sha256 `9c7c523c…`, verbatim output):

| filter | `~/.local/bin` present | `sasquatch-v4be` resolves | unblob run |
|---|---|---|---|
| A. `PATH=$(… \| tr ':' '\n' \| grep -v sasquatch \| paste -sd:)` | 1 | `/home/vgpnk/.local/bin/sasquatch-v4be` | exit 0, 4 files, no `ExtractorDependencyNotFoundReport` |
| B. `tools/round-37/c1-run.sh:43` (drop dirs that hold the binaries) | 0 | `NONE` | exit 1, 0 files, `ExtractorDependencyNotFoundReport ["sasquatch-v4be"]` |

Filter A is a no-op for the only directory that matters: its *name* (`~/.local/bin`) contains no
"`sasquatch`". A run with filter A is the after arm, and its "no gap" is the expected after result,
not evidence about the before arm.

Secondary trap found while building the demo (`path-filter-demo.txt` §C): in a persistent bash, the
command hash table keeps `sasquatch-v4be` after PATH changes —
`PATH=$P_B command -v sasquatch-v4be` printed the path while `env -i PATH=$P_B bash -c 'command -v …'`
and `hash -r` both printed `NONE`. Any guard built on `command -v` inside a long-lived shell must
`hash -r` first (the committed round-37 harness runs one mode per fresh `bash`, so its guard at `:44`
is sound).

### 1.7 Reproduction commands

At v1 the harness had only `after|oracle`, so the before arm required a starved PATH:
`env PATH="$STARVED" bash tools/round-38/c1-run.sh after <carrier> <out> <scratch>` with a
`$STARVED` built from a shim dir for node/npx plus the system dirs (and no `~/.local/bin`).
Freeze v2 (`79f69347`) added a `before` mode that strips `$HOME/.local/bin` from the child PATH and
keeps `REA_UNBLOB_COMMAND` absolute; measured today on K3 it yields
`coverage: partial, bytes: 0, gaps: [missing-extractor-dependency ["sasquatch-v4be"] squashfs_v4_be]`
(`v2harness-before-K3.json`). §3.4 records the one weakness of that mode.

```bash
export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
bash tools/round-38/c1-run.sh before <carrier> <out> <scratch>   # v2+
bash tools/round-38/c1-run.sh after  <carrier> <out> <scratch>
bash tools/round-37/c1-run.sh before <K> <out> <scratch>         # v1-era, self-guarding (exits 2 if the extractor resolves)
```

Both arms exit 0 at the harness level; the arm is visible only inside the envelope (`gaps`,
`published_bytes`, `coverage`) and in the round-37 harness's `<mode>-run.json` extractor fields.
All 13 envelopes in the artifacts directory (8 round-38-harness, 5 round-37-harness) recompute to
their stored `ev_` ids under `tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0>`.

## 2. Falsifier that would overturn this report

Run K3 with a PATH from which `sasquatch-v4be` genuinely cannot be resolved (`env -i HOME=$HOME
PATH=<dirs without it> unblob … K3/carrier.bin`) and observe four published apples. Measured result:
exit 1, zero files, `["sasquatch-v4be"]` gap (repeatable, §1.3/§1.6-B). Conversely, run with only
`sasquatch-v4be` on PATH (no `sasquatch`): exit 0, four apples, no gaps — the LE/GNU `sasquatch`
binary is irrelevant for BE v4.

## 3. Divergences found (reported, not repaired)

### 3.1 K2's `unpublished-entry` gap — real blocker for v1/v2, counter-fixed in v3, predicate text still open

K2's frozen bytes contain the symlink `var/lib/run-link -> ../../a/run.sh`. REA publishes only
regular files, so the entry lands in `unpublished_entries` **and** becomes a gap
(`k2-after-gap-detail.json`, reproducible with the counting harness):

```
coverage: partial, published_bytes: 10283, files: 3/3 oracle hits
unpublished_entries: [{relative_path: "firmware.bin_extract/var/lib/run-link", kind: "symlink", link_target: "../../a/run.sh"}]
extraction_gaps: [{kind: "unpublished-entry", relative_path: ".../var/lib/run-link", dependencies: []}]
```

Under **v1** (`after_gaps_empty = gaps(env) == []`) and under the **v2** draft of the counter (same
clause) this caps `carriers_matched` at 3/4 no matter how the BE extraction behaves — measured
`v2-as-written: 3/4`, `v2-with-narrowed-gap-binding: 4/4` (`v2-draft-binding-check.json`).

**v3 `f1010f67` (03:32:55) resolves it in the counter**: the binding became
`after_no_missing_extractor_gap` (any gap of kind `missing-extractor-dependency` fails; the
`unpublished-entry` symlink gap is admitted), and the three C1 controls were re-scored. Scoring my
eight drafts with v3's own helpers gives **4/4**
(`v3-binding-check.json`): all four have `after_no_missing_extractor_gap`, the `squashfs_v4_be`
handler, every oracle file, a before-arm `["sasquatch-v4be"]` gap and zero before-arm publications;
v3's selftest is green (`{"cases": 18, "green_ok": 1, "red_ok": 17, "failures": []}`).

**Residual divergence v3 did not close:** the *predicate sentence* still says "carries no extraction
gap" (`plans/round-38-claims.md:38`; v3 touched only the counter and the controls — `git diff
79f69347 f1010f67 --stat`). The counter now passes K2 with a gap present, so instrument and frozen
text disagree by exactly one `unpublished-entry` gap. A non-author verifier reading the predicate
will score K2 as violating it. Either the sentence must say "carries no missing-extractor-dependency
gap" (the v3 binding, and what the round-37 counter draft tested via `sasquatch_v4be_gap()`), or the
claim report must state the exclusion explicitly and cite the counter line. Re-freezing the text is
the L1's call; I only report the mismatch.

Related, not blocking: K1's after envelope is `coverage: partial` (diagnostic `MaliciousSymlinkRemoved`
for the dangling `link-to-hello`, no gap). If a later predicate asks for `coverage == complete` on all
four, K1 fails too; the current wording does not ask for it.

### 3.2 The committed v1 harness could not generate the after arm (fixed in v2)

`tools/round-38/c1-run.sh` at `e059ca93` does `mkdir -p "$OUT"`; REA refuses an existing extraction
root, so `after` always failed:
`{"code":"execution_failure", … "diagnostics":{"reason":"Extraction output root already exists"}}`
(`frozen-v1-harness-after-K2-error.json`). Fixed at `cb4326b2` (`rm -rf "$OUT"`); v2 also replaced the
wrong header line "stock unblob (no external extractor needed for standard BE v4)" and added the
`before` mode. The current header matches `squashfs.py:527`. No residual issue in the text.

### 3.3 Freeze churn observed while measuring (history, now committed)

While this seat ran (03:19–03:36) the freeze moved twice: v2 `79f69347` (03:29) and v3 `f1010f67`
(03:32:55). At 03:27 the tree held a half-applied v2 counter copy (duplicated `published`/`gaps`
definitions, no `per[k] = d`, no `n = 0`) that crashed with `AttributeError: 'NoneType'` at `gaps()`;
that state was transient and is gone. Committed instruments, selftests re-run by this seat:
v1 → `{"cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}` (blob `a7a62b09…`, copied into
scratch because the tree copy had moved on); v2/v3 → `{"cases": 18, "green_ok": 1, "red_ok": 17,
"failures": []}`. Both instruments are green; the v3 counter scores my drafts 4/4.

### 3.4 The v2/v3 harness `before` mode has no post-condition guard

The v2 `before` mode builds the child PATH with
`grep -v -F "$HOME/.local/bin"` and does **not** verify that the extractor is actually gone
(`grep -c 'command -v sasquatch-v4be' tools/round-38/c1-run.sh` → `0`, unlike `tools/round-37/c1-run.sh:44`).
Demonstration (`v2harness-before-K3-with-decoy-extractor-dir.json`): put a second copy of
`sasquatch-v4be` in an earlier PATH dir (simulating any future install outside `~/.local/bin`),
run the v2 `before` mode on K3 → exit 0, `coverage: complete`, 4 published files, `gaps: []`.
The "before" receipt is then an after receipt in disguise.

Mitigation already present: the frozen counter's `before_missing_extractor_gap` binding rejects such
a receipt (my decoy envelope would fail it), so the score is protected. But the harness itself
silently produces the wrong artifact, which is exactly the failure family behind this round's
premise confusion. One-line fix for whoever owns the harness post-v3: restore the round-37 guard —
`PATH="$STRIP" command -v sasquatch-v4be >/dev/null && { echo "still on PATH" >&2; exit 2; }` — or
derive the strip from `os.access` over dir contents as `tools/round-37/c1-run.sh:43` does.

For the record, the committed v1 counter is after-only (no before arm) and its docstring still carries
the v1 premise sentence ("no external extractor dependency"); running it at `cb4326b2` gives
`carriers_matched 0`, `met_target false`, exit 1 (`frozen-v1-counter-measure-at-cb4326b2.json`) —
expected, since no receipts exist yet.

## 4. Corrected-premise row (for the lesson's corrected-premise row)

> **Corrected premise (R37 missing-extractor-dependency).** The round-37 gap is an environment
> control, not a property of the carriers or of the toolchain version: unblob 26.6.4's
> `SquashFSv4BEHandler` extracts BE v4 only through the external `sasquatch-v4be -be`
> (`squashfs.py:41,527`), and `Command.extract` maps `FileNotFoundError` to
> `ExtractorDependencyNotFoundReport(dependencies=["sasquatch-v4be"])` (`command.py:69-71,101-102`),
> which REA renders as `kind: missing-extractor-dependency` with `published_bytes: 0`. Measured:
> with `sasquatch-v4be` resolvable, all four carriers publish every oracle file with no gap (K3/K4
> `coverage: complete`, K1 5/5, K2 3/3); with it unresolvable, all four emit the identical
> single-name gap. `sasquatch-v4be` 4.5.1 and rea-agents 6.5.0 were installed (01:22:37 / 01:12:52)
> before the round-37 launch (02:34:47) and the unblob launcher bytes are unchanged
> (`0ce7b624…` = the receipt's `executable_sha256`), so no version or time delta exists. "It does not
> reproduce" was a replication artifact: filtering PATH *component names* (`grep -v sasquatch`) never
> removes `~/.local/bin`, so the run stayed on the after arm. `sasquatch` (GNU/LE) is not needed; only
> `sasquatch-v4be` is.

## 5. Confidence

- **High**: the mechanism (PATH → `execvp` failure → single-name dependency report → gap), the
  byte-identity of engine/package, the authenticity of the round-37 receipt, both-arm reproducibility
  through the committed round-37 harness on all four carriers, and the K2 `unpublished-entry` gap.
- **Medium**: the exact round-38 v1 command that failed to reproduce. It is not committed anywhere
  (checked `git rev-list --all --objects`); the `grep -v sasquatch` shape is reported by the now-committed
  v2 note (`79f69347`) and is [INFERENCE] as to what actually ran, though §1.6 shows it produces exactly the observed
  "no gap" outcome.
- **Not claimed**: anything about AVM-BE, vendor-mangled images, or the extracted programs; anything
  about which arm the round-37 L1 believed it was running.

## 6. Tooling, scratch, limits

- No installs, no upgrades, no `pacman`. `npx -y rea-agents@6.5.0` reused the existing npx cache
  (package mtime unchanged). unblob 26.6.4 and sasquatch 4.5.1 were left untouched.
- All scratch under `/fast/scratch/hyaku/kaidoku-r38/R38RevengerPremise` and one short-lived
  `…Premise2` (harness/decoy check); both removed (`rm -rf`). Everything cited is copied into the
  artifacts directory. No file was written outside
  this report and that directory; nothing was written to `corpus/`, `PROVINCE.md`, `SCORECARD.md`,
  `SHONEN.md`, `LOG.md`, or VCS.
- Draft envelopes here are **not** claim data: they were produced under this seat's scratch paths and
  must be regenerated by the seat that lands them (their `parameters.output_directory` is
  scratch-local).

## 7. Artifacts

`code-anchors.md`, `env-snapshot.txt`, `path-filter-demo.txt`, `premise-verdict.json`,
`v2-draft-binding-check.json`, `v3-binding-check.json`, `k2-after-gap-detail.json`,
`frozen-v1-counter-selftest-and-measure.txt`, `frozen-v1-counter-measure-at-cb4326b2.json`,
`frozen-v1-harness-after-K2-error.json`,
`r37harness-{before-K1..K4}.json`, `r37harness-{before-K1..K4}-run.json`, `r37harness-after-K3.json`,
`r38harness-before-K1..K4.json`, `r38harness-after-K1..K4.json`,
`v2harness-before-K3.json`, `v2harness-before-K3-with-decoy-extractor-dir.json`.
