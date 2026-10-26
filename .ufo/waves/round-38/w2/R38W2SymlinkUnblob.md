# R38W2SymlinkUnblob — why K1's symlink leaves no gap and K2's leaves one

**DEFECTS FOUND** (mechanism reconstructed and every mechanism sentence confirmed; one universal in
the `Symlinks` paragraph — "on every run", entry line 38 — is contradicted by the entry's own before
arm, so it is over-broad as worded).

Seat `R38W2SymlinkUnblob` (leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Judged by
the first freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`; attack surface = the `Symlinks`
paragraph (lines 33-41) of
`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` at the landed revision
`3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8`, whose bytes are identical to the working tree
(`diff <(git show 3b960fe5:…) <file>` → empty). No lane writes outside this report and
`.ufo/waves/round-38/w2/artifacts/R38W2SymlinkUnblob/`; no carrier, oracle, counter, predicate or
VCS byte touched; scratch removed.

## 0. Answer in one paragraph

Both REA runs are the *same* shape and produce the same envelope until the tree is walked. The
external extractor `sasquatch-v4be` writes **both** links into the staging tree verbatim. unblob's
post-extraction sanitiser then applies one rule that reads the link's *target*: a **relative** target
is resolved against the link's own directory and, if it lands outside the extraction root, the link
is **deleted** and a `MaliciousSymlinkRemoved` report is recorded; otherwise the link is re-created
with a normalised relative target and **survives**. K1's `../hello.txt` resolves above the root
(`…/extracted/firmware.bin_extract/link-to-hello` → `…/extracted/hello.txt`) → deleted → nothing for
REA to account for. K2's `../../a/run.sh` resolves to `…/firmware.bin_extract/a/run.sh`, inside the
root → re-created with the identical string. REA 6.5.0 publishes **only** entries whose `lstat` kind
is `file`; every other kind is retained as `unpublished_entries` metadata and each one emits exactly
one `unpublished-entry` extraction gap. So the discriminator is **presence of the entry on disk after
unblob's sanitiser**, not the link's meaning: REA is target-indifferent.

## 1. Mechanism, with anchors

unblob 26.6.4 venv root `U=/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob`;
`~/.local/bin/unblob` sha256 `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`
(= `normalized_result.engine.executable_sha256` in every committed receipt).

| step | anchor | what it does |
|---|---|---|
| extract | `unblob/handlers/filesystem/squashfs.py` (BE v4 → `sasquatch-v4be -be`) | writes the image member bytes: symlink inodes become real symlinks in the staging dir, targets unchanged |
| sanitise entry | `U/extractor.py:95-113` (`fix_extracted_directory`, called from `U/processing.py:447,654,678`) | walks the extracted tree; `:102-103` `if path.is_symlink(): fix_symlink(path, outdir, task_result)` |
| loop guard | `U/extractor.py:42-47` `is_recursive_link` | `path.resolve()` raising `RuntimeError` ⇒ "loop" |
| relative target | `U/extractor.py:73-78` | `if target.is_absolute(): target = Path(target.as_posix().lstrip("/"))` **else** `target = path.resolve()` — resolves the relative target against the link's own parent, fully |
| escape test | `U/file_utils.py:34-39` `is_safe_path(basedir, path)` | `basedir.joinpath(path).resolve().relative_to(basedir.resolve())`; absolute `path` ⇒ `ValueError` ⇒ `False` |
| remove | `U/extractor.py:80-89` | `logger.error("Path traversal attempt through symlink, removing", target=target)` + `MaliciousSymlinkRemoved(link, target)` + `path.unlink()` |
| keep | `U/extractor.py:90-92` | `relative_target = os.path.relpath(outdir.joinpath(target), start=path.parent)`; unlink; `symlink_to(relative_target)` |
| report type | `U/report.py:133-137` | `class MaliciousSymlinkRemoved(ErrorReport)`, `severity = Severity.WARNING`, fields `link`, `target` |
| REA inventory | `rea-agents 6.5.0` `dist/firmware/FirmwareFiles.js:154-190` | `lstat` walk, never follows links (`:139` skips symlinked dirs); `kind = isSymbolicLink() ? "symlink" : isFile() ? "file" : "special"` (`:179-184`), `linkTarget = readlink` (`:184`) |
| REA publication | `dist/firmware/FirmwarePublication.js:69-76` | `if (entry.kind !== "file") { unpublished.push({relative_path, kind, link_target}); continue; }` |
| coverage | same file `:103` | `coverage: unpublished.length > 0 ? "partial" : normalized.coverage` |
| gap row | same file `:301-307` (+ `:212-217` for the id) | one `extraction_gap` per unpublished entry: `{kind:"unpublished-entry", input_path:"$output/<path>", handler:null, dependencies:[], continuation_id: sha256(instruction)}`; instruction text at `:18` |
| counter | `tools/round-38/c1-counter.py` @ freeze `e059ca93` `:131-133`, `:178`, `:189-192` | `gaps(env)` reads only `normalized_result.extraction_gaps`; `after_gaps_empty = gaps(env) == []` is a hard binding on `matched` |

Consequence chain for the two carriers, arithmetically (measured, §2.3):

- K1 `link-to-hello`: `readlink = ../hello.txt`; `resolve() = <parent-of-outdir>/hello.txt`;
  `is_safe_path = False` ⇒ deleted. `diagnostics[0].report.__typename__ = MaliciousSymlinkRemoved`,
  `extraction_gaps = []`.
- K2 `var/lib/run-link`: `readlink = ../../a/run.sh`; `resolve() = outdir/a/run.sh`;
  `is_safe_path = True`; `relpath(outdir/a/run.sh, start=outdir/var/lib) = ../../a/run.sh` — the
  re-created link is **string-identical** ⇒ survives ⇒ one `unpublished-entry` gap.

## 2. Evidence measured today (2026-10-26, this host)

Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2SymlinkUnblob` (`TMPDIR`/`HYAKU_SCRATCH` set there),
removed at exit. Commands in `artifacts/R38W2SymlinkUnblob/probe.sh` (the script I ran;
`bash probe.sh` exit 0, 15.5 s).

### 2.1 Direct unblob (sanitiser, on disk)

`~/.local/bin/unblob -e $S/direct/$K -f corpus/evidence/round-37/c1/$K/carrier.sqsh` → exit 0 both.

- K1: `find -type l` → **no links**; unblob's own summary `Extracted links: 0`; `--report` JSON holds
  `{"severity":"WARNING","link":"…/carrier.sqsh_extract/link-to-hello","target":"…/K1-r/hello.txt","__typename__":"MaliciousSymlinkRemoved"}` at `report[0].reports[4]`;
  `--log` holds `[error ] Path traversal attempt through symlink, removing … target=hello.txt`.
- K2: `find -type l` → `carrier.sqsh_extract/var/lib/run-link -> ../../a/run.sh`; summary
  `Extracted links: 1`; **no** `Malicious*` anywhere in the report or log.
  (unblob's own link counter is a third, independent signal of the same discriminator.)

Artifacts: `unblob-K1-report.json`, `unblob-K2-report.json`, `links-on-disk.txt`.

### 2.2 REA `extract-firmware` (reas-agents 6.5.0, stock unblob, `sasquatch-v4be` on PATH)

`npx -y rea-agents@6.5.0 extract-firmware --format json <carrier> <fresh OUTDIR>`, exit 0 for all
seven runs; `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`.

| run | carrier | evidence_id | files | unpublished | gaps | diagnostics | coverage |
|---|---|---|---|---|---|---|---|
| K1 | frozen K1 | `ev_09227b23bb4b68ee00ce57539c10ecba053dd12f0c287d2552059e861ec504b9` | 5 | `[]` | `[]` | `MaliciousSymlinkRemoved` | partial |
| K2 | frozen K2 | `ev_0b41d7847d08c195183683abb91f01b113b167fa6893b95ab7c3bf1382bd3cbb` | 3 | 1 (`symlink`, `../../a/run.sh`) | 1 `unpublished-entry` | `[]` | partial |

These reproduce the committed receipts
(`corpus/evidence/round-38/c1/K{1,2}/after.json`) field-for-field on the fields under attack: K1
`files 5 / unpublished [] / extraction_gaps [] / diagnostics [MaliciousSymlinkRemoved]`; K2
`files 3 / unpublished [{relative_path …/var/lib/run-link, kind symlink, link_target ../../a/run.sh}] /
extraction_gaps [{kind unpublished-entry, same relative_path, dependencies []}]`.

### 2.3 Boundary probes (my own carriers, `tools/round-37/gen-squashfs.py --endian be --comp gzip`)

Each tree differs only in the link shape; envelopes in `artifacts/R38W2SymlinkUnblob/rea-P{1..5}.json`.

| probe | link(s) as encoded | survives sanitiser as | REA gaps |
|---|---|---|---|
| P1 in-tree relative (K2 shape) | `var/lib/run-link -> ../../a/run.sh` | `../../a/run.sh` | 1 `unpublished-entry` |
| P2 escaping relative (K1 shape) | `link-to-hello -> ../hello.txt` | **deleted** (`MaliciousSymlinkRemoved`) | **0** |
| P3 loop, both targets in-tree | `a -> b`, `b -> a` | `a -> a`, `b -> a` (rewritten, **not** removed) | 2 `unpublished-entry` |
| P4 absolute targets | `abs-in -> /hello.txt`, `abs-out -> /etc/passwd` | `hello.txt`, `etc/passwd` (stripped + pulled inside) | 2 `unpublished-entry` |
| P5 dangling but in-tree | `dangling -> docs/nothere` | `docs/nothere` | 1 `unpublished-entry` |

Python-level arithmetic on the same structures (unblob venv interpreter, `fix_symlink`/`is_safe_path`
imported):

```
var/lib/run-link: readlink='../../a/run.sh' resolve=…/out/a/run.sh recursive=False safe=True  relpath=../../a/run.sh
link-to-hello:    readlink='../hello.txt'   resolve=…/sim/hello.txt recursive=False safe=False relpath=../hello.txt
dangling:         readlink='docs/nothere'   resolve=…/out/docs/nothere recursive=False safe=True
la: readlink='b' resolve=…/out/b ; lb: readlink='a' resolve=…/out/a   (loop: no RuntimeError on py3.13)
```

### 2.4 Determinism of "on every run"

Five independent wave-1 envelopes hold the identical gap row and the identical continuation id
`602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca`
(`.ufo/waves/round-38/w1/artifacts/R38ExecProvincePatch/determinism-K2-run{1,2}.json`,
`…/R38ExecAfterK2/after.json`, `…/R38RevengerPremise/r38harness-after-K2.json`,
`…/R38RevengerPremise/k2-after-gap-detail.json`), plus my run in §2.2 — six runs, two freezes, at
least three distinct output directories. The id is `sha256` of the static instruction
(`FirmwarePublication.js:212-217`), so it cannot vary while the instruction text is fixed.

## 3. The paragraph, sentence by sentence

Entry lines: 33 (`**Symlinks.**`), 35-36 (K1 bullet), 37-38 (K2 bullet), 40-41 (two closing
sentences).

| # | sentence (line) | verdict | evidence |
|---|---|---|---|
| S1 | "K1's `link-to-hello -> ../hello.txt` points outside the extraction root." (35) | **CONFIRMED** | link resolves to `<parent of outdir>/hello.txt`; committed receipt's diagnostic target `…/extracted/hello.txt` vs root `…/extracted/firmware.bin_extract`; my run `…/K1-r/hello.txt` vs `…/K1-r/carrier.sqsh_extract`; `is_safe_path` False |
| S2 | "unblob removes it and logs `MaliciousSymlinkRemoved`, so no gap is recorded." (35-36) | **CONFIRMED** (one wording nuance, note N2) | no link on disk after unblob; report record `MaliciousSymlinkRemoved` WARNING; unblob log `Path traversal attempt through symlink, removing`; REA `extraction_gaps []` |
| S3 | "K2's `var/lib/run-link -> ../../a/run.sh` stays inside the tree." (37) | **CONFIRMED** | resolves to `outdir/a/run.sh`; `is_safe_path` True; survives with the identical string (`find -type l`, both receipts' `link_target`) |
| S4 | "REA keeps it as metadata and records one `unpublished-entry` gap on every run." (37-38) | **DEFECT (scope)** — metadata half CONFIRMED; "on every run" false as written | `unpublished_entries[{kind:"symlink",link_target}]` + exactly one gap in 6 runs (§2.4, §2.2); **but** `corpus/evidence/round-38/c1/K2/before.json` (extractor unreachable) has `unpublished_entries []`, `files 0`, one `missing-extractor-dependency` gap — the entry's own table line 16 says the same |
| S5 | "So 'no extraction gap' is unreachable on any carrier with an in-tree symlink." (40) | **CONFIRMED**, with a precision note (N1) | the condition is sufficient: K2, P1, P3, P5 all gap, and code makes it structural (`kind !== "file"` ⇒ unpublished ⇒ gap; no publish-symlink option); round-36 K2/K3/K4 gap the same way |
| S6 | "This is the same behaviour the round-36 LE entry recorded (`unpublished-entry` for symlinks)." (41) | **CONFIRMED** | `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:117-126` states the same shape and quotes the **same** continuation id `602c674b…`; `:188` "Not gap-free extraction" |

## 4. Defect D1 — "on every run" (entry line 38)

Swap the single sentence for one of:

> … REA keeps it as metadata and records one `unpublished-entry` gap on every run in which unblob
> publishes the image (i.e. `sasquatch-v4be` reachable); in the before arm the link is never
> extracted and the only gap is `missing-extractor-dependency`.

Why it matters: the paragraph is the paragraph a future claim will lean on to pre-declare symlink
behaviour, and the entry's own table line 16 contradicts an unqualified "every run". Severity:
wording/calibration only. It changes nothing in the graded data: the C1 after receipt is the frozen
predicate's object, and its gap list is non-empty.

## 5. Precision notes (not defects; recommended for the lesson text, L1 decides)

- **N1 — the operative condition is "survives unblob", not "in-tree".** An absolute target is
  `lstrip("/")`-ed and re-created *inside* the tree, so `abs-out -> /etc/passwd` — a link pointing
  outside the real root — is **retained** and gaps (P4). The only deletion paths are (a) a *relative*
  target resolving outside `outdir`, (b) empty target, (c) `is_recursive_link`. So "in-tree symlink"
  is a sufficient condition, and the removal rule is narrower than "points outside the root".
- **N2 — "logs MaliciousSymlinkRemoved"** is shorthand for two distinct things: unblob writes an
  `[error] Path traversal attempt through symlink, removing` log line, and records a
  `MaliciousSymlinkRemoved` report whose `severity` is `WARNING`; REA surfaces that report in
  `normalized_result.diagnostics`. Neither is a textual log entry named `MaliciousSymlinkRemoved`.
- **N3 — "0 gaps" on K1 is not "clean".** K1's after envelope is `coverage: "partial"` with one
  WARNING diagnostic; K2's is `partial` for the unpublished entry. The frozen counter keys only on
  `extraction_gaps` (`c1-counter.py@e059ca93:131-133,178`), which is why K1 passes its binding and
  K2 does not — worth stating so nobody reads the table's "0 gaps" as a clean-extraction claim.
- **N4 — loop sanitiser quirk (unblob, not the entry).** `is_recursive_link`
  (`extractor.py:42-47`) catches only `RuntimeError`; on Python 3.13 `Path.resolve()` does not raise
  for a two-link cycle, so `a -> b, b -> a` is **not** removed — it is relinked into `a -> a`,
  `b -> a` (order-dependent) and yields two gaps (P3). This strengthens S5: even malformed symlinks
  survive and gap.

## 6. Effect on the round-38 verdict under attack

None of the above moves a graded byte, and none of it is a repair I make. For the record, from the
freeze counter's own bindings and the committed receipts: K1 `after_gaps_empty` True (5/5 oracle
hits), K2 False (`extraction_gaps` length 1) ⇒ `carriers_matched` 3, `met_target` false ⇒ **R38-C1
honest stop stands**. What this seat adds is the causal account the entry asserts, verified at
`file:line` in both tools and reproduced independently, plus one over-broad universal to fix.

## 7. Limits, provenance, and bounds

- Measured on this host: unblob 26.6.4 at executable sha256 `0ce7b624…` (byte-identical to every
  receipt's `engine.executable_sha256`); rea-agents 6.5.0
  (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json` version 6.5.0);
  `sasquatch-v4be` 4.5.1 present in `~/.local/bin`, untouched.
- Not measured here: K3/K4 (no symlinks), AVM-BE, vendor images, other rea-agents/unblob versions,
  behaviour of extracted programs. P1..P5 are **my** synthetic carriers built in scratch — they are
  mechanism probes, not claim data, and are cited only as artifacts.
- Inference is marked: N1's generalisation beyond K1..K4+P1..P5 rests on code
  (`FirmwarePublication.js:69-76` is entry-kind-only), not on more carriers.
- Bounds observed: no lane writes outside this report and `…/w2/artifacts/R38W2SymlinkUnblob/`; no
  `git add/commit/checkout/reset/stash/pull/push` and no jj mutation (read-only `git show`,
  `rev-parse`, `diff` only); no subshell created a repo outside `$S`; REA driven only through
  `npx -y rea-agents@6.5.0`; assimilation package untouched; scratch
  `/fast/scratch/hyaku/kaidoku-r38/R38W2SymlinkUnblob` removed.
- Tooling installs: **none**.

## 8. Artifacts

`.ufo/waves/round-38/w2/artifacts/R38W2SymlinkUnblob/`: `probe.sh` (the run I executed),
`rea-K1.json`, `rea-K2.json`, `rea-P1.json`…`rea-P5.json`, `unblob-K1-report.json`,
`unblob-K2-report.json`, `links-on-disk.txt` (unblob's link listings, summaries, and the symlink log
lines).

Report: `.ufo/waves/round-38/w2/R38W2SymlinkUnblob.md`
