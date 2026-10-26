# R38CrossToolK1 — cross-tool oracle reproduction for C1 carrier K1 (independent of REA)

Leaf executor, round 38 wave 1. Scope: reproduce the R38-C1 oracle comparison for the named
carrier **K1** with `~/.local/bin/sasquatch-v4be -be`, confirm 7-Zip refuses the BE image and
capture the verbatim error text for the lesson `## Gate`, and report (not repair) anything that
falsifies the cross-tool expectation. K2..K4 were measured too, because the carrier set is frozen
as a unit and a K1-only answer would hide a carrier-specific failure; K1 stays the primary.

No claim predicate, counter, carrier, oracle, control or harness was changed. No REA invocation
was made — this is the non-REA leg. No VCS mutation (read-only `git show`/`rev-parse`/`log` only).
No installs or upgrades (every tool used was already on the host).

- Worktree HEAD while working: `9c9d496b73cf066b02639dc54647934a0ba4297a`
  (`round-38: wave-1 spec/dispatch`), i.e. freeze `e059ca93` + controls `efd5c47a` below it.
- Scratch: `S=/fast/scratch/hyaku/kaidoku-r38/R38CrossToolK1`, `TMPDIR=$S`; **removed at the end**
  (`ls -d $S` → `No such file or directory`). Everything cited below was copied into
  `.ufo/waves/round-38/w1/artifacts/R38CrossToolK1/` before cleanup.
- `considerthese/`: not used (absent in this lane; noted once, per the plan's single-line rule).

## 1. Tool inventory (operator tooling directive)

| tool | version | channel | digest / note |
|---|---|---|---|
| `sasquatch-v4be` | `unsquashfs version 4.5.1 (2022/03/17)` (onekey-sec BE build) | pre-installed by the L1 at `~/.local/bin` (official onekey-sec deb); **not** installed/upgraded by this seat | sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` |
| `sasquatch` (LE) | `4.5.1 (2022/03/17)` | same | sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`; negative control only |
| `unsquashfs` | `4.7.5 (2026/03/01)` | distro `/usr/bin` | negative control only |
| `mksquashfs` | `4.7.5 (2026/03/01)` | distro `/usr/bin` | built the LE positive control |
| `7z` | `7-Zip 26.04 (x64) 2026-10-05` | distro `/usr/bin` | refusal evidence |
| `unblob` | `26.6.4` | `~/.local/bin/unblob` (uv tool) | direct CLI probes (not REA) |
| `rea-agents` | `6.5.0` (`package.json`) | npx cache | read only, never executed here |

`dpkg -S` on the `sasquatch*` paths: not dpkg-owned (manual deb extract by the L1), so the deb's
own provenance is the L1's to register; digests above pin the bytes this seat used.

## 2. Frozen inputs verified before measuring

Carrier bytes at `corpus/evidence/round-37/c1/K*/carrier.*` recomputed and compared with the
frozen manifest `.ufo/waves/round-38/c1/carriers.json` — 4/4 agree, and the same digests are
present at base `77091b49`, freeze `e059ca93`, controls `efd5c47a` and HEAD `9c9d496b`
(`git show <rev>:path | sha256sum`; `oracle.tsv` digests likewise unchanged at all four):

```
K1 1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e  carrier.sqsh  9780 B
K2 403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  carrier.sqsh  1606 B
K3 9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0  carrier.bin   4096 B
K4 a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed  carrier.bin    307 B
```

`file -b` on each: `Squashfs filesystem, big endian, version 4.0, zlib compressed` (K1 11 inodes /
blocksize 4096; K2 10 inodes / 4096; K3/K4 5 inodes / 131072). K3 padding confirmed at byte level:
`len=4096`, `K3[:307] == K4` exactly, and all 3789 tail bytes are `0x00` — so `offset=0` is the
filesystem start and no `-offset` is needed for the cross-tool read.

Oracle integrity (so a cross-tool "match" cannot be an oracle-vs-source drift artefact):

| check | command | result |
|---|---|---|
| K1 oracle == committed source tree | `sha256sum` over `K1/src` regular files vs `K1/oracle.tsv` | `diff` rc=0 (5 rows) |
| K2 oracle == committed source tree | same over `K2/src` | `diff` rc=0 (3 rows) |
| K3/K4 oracle == committed `apple{1..4}.txt` | same over the committed expected files | `diff` rc=0 (4 rows each) |

## 3. K1 cross-tool reproduction — pass

Exact commands (from the lane root; `C=corpus/evidence/round-37/c1`):

```
~/.local/bin/sasquatch-v4be -be -d "$S/K1/out" "$C/K1/carrier.sqsh"          # exit 0
cd "$S/K1/out" && find . -type f -print0 | LC_ALL=C sort -z \
  | while IFS= read -r -d '' f; do printf '%s\t%s\t%s\n' "${f#./}" \
      "$(sha256sum "$f"|cut -d' ' -f1)" "$(stat -c%s "$f")"; done | LC_ALL=C sort
diff -u <(LC_ALL=C sort "$C/K1/oracle.tsv") "$S/K1/observed.sorted.tsv"      # exit 0
```

Result: **exit 0, 5/5 oracle rows identical on relative path, sha256 *and* size**; `diff` was
bidirectional, so no extra and no missing regular file. Paths compared by exact relative path,
which is stricter than the predicate's "same relative-path suffix".

```
bin/run         299001868fb8c02fd431c336c6d058f5558c5dff5b5af5e6fe04b870a6a9cbba  18
docs/deep/nested/file.dat b7e769c3ad3cb09448d2e517b491ac6d949eb0b508cc0dde0035a4994cddfa21 9000
docs/readme.md  98f8c3bfbe995a851e73f06598216243ce5b282d970fff82932a65dafdbdb742  609
empty           e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855    0
hello.txt       0da249108ff14fde04d11119e2d86dabc20aa18a95f0411164294674d62951ff   29
```

Extractor self-report (`stdout`): `created 5 files / 5 directories / 1 symlink / 0 devices /
0 fifos / 0 sockets / 0 hardlinks`, 12/12 blocks; `stderr`: `Reading a different endian SQUASHFS
filesystem` then `Successfully decompressed with default gzip decompressor` — i.e. the BE path was
taken, not an accidental LE read.

- **Determinism:** a second run from `cwd=/` with the absolute carrier path produced a
  byte-identical listing (`diff` rc=0).
- **`-be` is load-bearing:** `sasquatch-v4be` *without* `-be` on the same carrier → exit 1,
  `SquashFS version [1024.0] / inode count [184549376] suggests a SquashFS image of a different
  endianess` + `read_id_table: failed to read id table block` + `FATAL ERROR: File system
  corruption detected`, 0 files created. The harness passes `-be` explicitly, so this is correct.
- **`-lls` cross-check:** inode sizes `18 / 9000 / 609 / 0 / 29` and the symlink
  `link-to-hello -> ../hello.txt` match `K1/src` exactly. (The symlink resolves outside the
  extraction root — `../hello.txt` from the root — so it dangles in both trees; it is not an
  oracle row because the oracle is regular-files-only.)

## 4. K2..K4 corroboration — pass (independent measurement by this seat)

Same command shape per carrier. `diff` vs each committed `oracle.tsv`, all bidirectional:

| carrier | extract exit | oracle rows | extracted rows | path+sha+size diff | extractor self-report |
|---|---|---|---|---|---|
| K1 | 0 | 5 | 5 | **identical** | 5 files / 5 dirs / 1 symlink |
| K2 | 0 | 3 | 3 | **identical** | 3 files / 6 dirs / 1 symlink |
| K3 | 0 | 4 | 4 | **identical** | 4 files / 1 dir |
| K4 | 0 | 4 | 4 | **identical** | 4 files / 1 dir |

16/16 rows match. **No carrier failed to open with `sasquatch-v4be -be`**, so nothing here
falsifies the "cross-tool extraction works" expectation.

Lane-harness agreement (`tools/round-38/c1-run.sh oracle`, `HYAKU_SCRATCH=$S`):
K1 rc=0 and K3 rc=0, stdout `diff`-identical to the committed `oracle.tsv`, empty stderr — the
harness `oracle` leg reproduces the same bytes this seat measured by hand.

## 5. 7-Zip refusal — verbatim text for the `## Gate`

`7z l <carrier>` on all four: **exit code 2**, `Errors: 1`, and on `stderr`

```
ERROR: corpus/evidence/round-37/c1/K1/carrier.sqsh : Cannot open the file as archive
```

(K2/K3/K4: identical line with their own paths. K3 is the 4096 B padded fixture — padding does not
help.) Variants on K1, same verdict:

- `7z l -tSquashFS <carrier>` → exit 2, `ERROR: … : …` / `Open ERROR: Cannot open the file as
  [SquashFS] archive` (so the handler is chosen and still refuses — not an auto-detect artefact).
- `7z x -o<dir> <carrier>` → exit 2, `ERROR: … Cannot open the file as archive`; extraction dir
  empty afterwards.
- `7z t <carrier>` → exit 2, `ERROR: … Cannot open the file as archive`, `Can't open as archive: 1`.

**Positive control (new, and the reason the Gate decision is sound):** the refusal is
big-endian-specific, not a general "7-Zip can't read SquashFS". `mksquashfs` 4.7.5 built an LE v4
gzip image from a two-entry tree; `7z l` on it → **exit 0**, `Type = SquashFS`,
`File System = SquashFS 4.0`, `Method = ZLIB`, `Big-endian = -`, listing `docs/` + `hello.txt`.
So 7-Zip 26.04 ships a working SquashFS reader that exposes a `Big-endian` field yet cannot open a
BE v4 image. The lesson `## Gate` wording should therefore say "7-Zip 26.04 refuses **big-endian**
SquashFS v4 (`Cannot open the file as archive`, exit 2) while opening little-endian v4", not
"7-Zip cannot read SquashFS".

Additional negative controls (all exit 1, no files written):

| reader | K1 result |
|---|---|
| `unsquashfs` 4.7.5 | `Reading a different endian SQUASHFS filesystem` + `FATAL ERROR: Can't find a valid SQUASHFS superblock on …` |
| `sasquatch` (LE 4.5.1) | `SquashFS version [1024.0] / inode count [184549376] suggests … different endianess` + `FATAL ERROR: Block size too small. File system is corrupt.` |

## 6. Finding (reported, not repaired): the C1 parenthetical "no external extractor dependency" is false, and I measured it

**(a) [FACT] unblob 26.6.4's `squashfs_v4_be` handler always shells out to the external
`sasquatch-v4be` binary.** Installed source,
`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`:

- `:25 EXECUTABLE = "sasquatch"`, `:26 V4BE_EXECUTABLE = "sasquatch-v4be"`
- `:40-41 case Endian.BIG, 4: executable = self.V4BE_EXECUTABLE`
- `:48-50 is_avm = header.bytes_used == header.mkfs_time` / `if not is_avm:` / `commands_args.append("-be")`
- `:65 extractor = Command(executable, *commands_args)`, `:68-69 get_dependencies → [sasquatch, sasquatch-v4be]`

`unblob --help` states it outright: "You also need these extractor commands … : 7z, …, `sasquatch`,
`sasquatch-v4be`, …", and `unblob --show-external-dependencies` lists both (✗ when absent from
`PATH`).

**(b) [FACT] the round-37 "missing-extractor-dependency" before-arm reproduces exactly.** Direct
unblob CLI, K1 carrier, `PATH` deliberately without `~/.local/bin`:

```
env -i HOME=$HOME PATH=/usr/bin:/bin TERM=dumb ~/.local/bin/unblob -e out \
    --report report.json --log log.txt -f corpus/evidence/round-37/c1/K1/carrier.sqsh
exit=1
```

- chunk report: `handler_name = squashfs_v4_be`, `start_offset=0`, `end_offset=9780`,
  `extraction_reports = [{"severity":"ERROR","dependencies":["sasquatch-v4be"],
  "__typename__":"ExtractorDependencyNotFoundReport"}]`
- log: `Running extract command command='sasquatch-v4be -be -no-exit-code -f -d <out>/carrier.sqsh_extract <carrier>'`
  then `Can't run extract command. Is the extractor installed? … dependencies=['sasquatch-v4be']`
- published files in `out/`: **none** (directory exists and is empty)

**(c) [FACT] with the binary on `PATH` the same command exits 0**, publishes the 5 K1 regular
files, and the published tree is `diff`-identical to `oracle.tsv`; the chunk report's
`extraction_reports` is `[]`. The argv unblob issued is the same `sasquatch-v4be -be …` this seat
ran by hand — i.e. the REA leg and this seat use the *same* executable and the same flag.

Consequences for the frozen wording (advisory):

1. The predicate parenthetical "run with stock unblob 26.6.4; **no external extractor
   dependency**", and the `Not claimed` sentence "stock unblob handles standard BE v4 … without any
   external extractor — the round-37 'missing-extractor-dependency' before-arm does not reproduce",
   are both contradicted by the measured behaviour. The accurate statement is: stock unblob names
   and drives the BE handler, and **cannot** extract BE v4 without `sasquatch-v4be` on `PATH`. The
   before-arm was correct; its non-reproduction in round-37 is explained by
   `~/.local/bin/sasquatch-v4be` already being installed (mtime `Oct 26 01:22`, L1-installed).
2. `[INFERENCE]` At the REA layer this inheritance is direct: rea-agents 6.5.0 contains no
   squashfs reader of its own (`grep -rl 'squashfs\|sasquatch'` over `dist/` → 0 files) and drives
   unblob (`dist/firmware/*.js` references `unblob`, `--report`, `REA_UNBLOB_COMMAND`), so the
   after-receipt's BE extraction runs through the same `sasquatch-v4be`. The receipt has no field
   that records this: the committed round-37 `probes/rea-k3.json` shows `extraction_gaps: []` and
   `parameters` = `{path, output_directory, max_depth, max_output_bytes, max_output_files}` — no
   extractor/dependency key. **The after-receipt therefore cannot evidence the parenthetical, and
   the counter cannot catch it**: `tools/round-38/c1-counter.py:328-329` models the gap as
   `{'kind':'missing-extractor-dependency','dependencies':['sasquatch-v4be']}` and only tests
   `after_gaps_empty` (`:177-178`), which passes when the binary is present.
3. `tools/round-38/c1-run.sh`'s header comment "with stock unblob (no external extractor needed for
   standard BE v4) … never runs sasquatch" is wrong at the subprocess level: the `after` leg reaches
   `sasquatch-v4be` *through* the handler. Harness behaviour itself is correct; only the comment and
   the claim wording need fixing by the owner.
4. **Independence caveat for this seat's evidence:** because unblob delegates to the same binary,
   `sasquatch-v4be -be` is *not* a second decoder relative to the REA→unblob path — it is the same
   executable and flag. What this seat independently establishes is: (i) the extractor reproduces
   the committed oracle byte-for-byte, (ii) the carriers really are standard BE v4 (superblock,
   `file(1)`, LE readers and 7-Zip refuse), (iii) K1/K2 oracles are reproduced from an independent
   generator source tree, not from unblob output. For K3/K4 the oracle is unblob's own expected
   `__output__` lineage, so those rows are expected-output evidence, not a second decoder.

## 7. Finding (advisory): the oracle is blind to symlink loss

`sasquatch-v4be -be` preserves K1's `link-to-hello -> ../hello.txt`. unblob's shell-out does not:
the positive run logs `Path traversal attempt through symlink, removing` / `target=hello.txt` and
the published tree has no symlink. Both still score 5/5 because the predicate and the oracle are
regular-files-only. This is not a defect to repair — it is a coverage blind spot worth one line in
the knowledge entry: "regular-file fidelity only; symlink/dir fidelity is not pinned by the
oracle". K2 has the same shape (`var/lib/run-link -> ../../a/run.sh`).

## 8. Gate notes this seat hands to the lesson author

- **7-Zip rejection — reproduced, BE-specific.** Exit 2, `Cannot open the file as archive`
  (auto-detect) / `Cannot open the file as [SquashFS] archive` (explicit `-tSquashFS`), on all four
  frozen carriers; LE v4 positive control opens fine (exit 0, `Type = SquashFS`). Use the
  "big-endian-specific" phrasing.
- **Extractor dependency — reproduced, and it inverts the round-38 premise.** Stock unblob 26.6.4
  needs `sasquatch-v4be` for BE v4 (`ExtractorDependencyNotFoundReport`, exit 1, nothing
  published); it extracts only when that binary is on `PATH`. The claim's "no external extractor
  dependency" wording and the `Not claimed` sentence should be corrected before freeze.
- `unsquashfs` 4.7.5 refuses BE v4 (`Can't find a valid SQUASHFS superblock`, exit 1) — matches the
  claim's aside, so the harness's `oracle` leg could not have used stock unsquashfs.

## 9. Artifacts (all under `.ufo/waves/round-38/w1/artifacts/R38CrossToolK1/`)

```
K1-oracle.tsv                  frozen oracle, LC_ALL=C sorted
K1-sasquatch-v4be.tsv          this seat's extraction listing (rel path, sha256, size)
K1-diff.txt                    oracle-vs-extraction diff + determinism diff (both rc=0)
K{2,3,4}-sasquatch-v4be.tsv    same listing per carrier
oracle-compare-matrix.txt      per-carrier rows/extracted/identical verdict
carrier-pins.txt               recomputed carrier digests + revisions checked
tool-versions.txt              versions, digests, rea-agents package version
7z-refusal.txt                 full 7-Zip transcript per carrier, auto-detect + -tSquashFS + x, exit codes
7z-explicit-squashfs-K1.txt    7z l -tSquashFS on K1 (exit 2)
7z-le-positive-control.txt     7z l on an mksquashfs-built LE v4 image (exit 0, Type=SquashFS)
unblob-dependency-probe.txt    PATH-sanitized unblob run: dependency report, log, empty out dir
unblob-positive-K1.txt         PATH-with-binary run: argv, empty extraction_reports, tree==oracle
unblob-external-deps.txt       unblob --show-external-dependencies listing
unblob-handler-excerpt.txt     unblob squashfs.py:24-72 (executable selection, is_avm, -be)
```

## 10. Verdict for this seat

- **K1 cross-tool reproduction: pass.** exit 0, 5/5 rows identical (path, sha256, size), 0 extra,
  0 missing, deterministic, `-be` shown to be required.
- **All four carriers: pass** (16/16 rows), no carrier failed to open — the cross-tool expectation
  is not falsified at the extraction level.
- **7-Zip refusal: reproduced on 4/4** (exit 2) with verbatim text, plus an LE positive control
  that makes the Gate decision precise.
- **Two premise defects reported, not repaired:** (i) "no external extractor dependency" / "the
  before-arm does not reproduce" — measured false, the dependency gap reproduces exactly;
  (ii) the harness header comment repeating (i). Plus the independence caveat (§6a.4) and the
  symlink blind spot (§7).
- **Blockers:** none. `pacman` untouched; no subagents, no background jobs, no `agent://all`
  messages; files written: this report and the artifact directory only.
