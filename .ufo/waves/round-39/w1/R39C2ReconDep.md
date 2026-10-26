# R39C2ReconDep — C2 dependency-outcome recon (round 39, wave 1, pre-freeze)

**Verdict: DONE — the dependency-missing outcome is fully characterised (BE names exactly
`sasquatch-v4be`, LE names exactly `sasquatch`, gap kind `missing-extractor-dependency`, 0 files,
`-be`/symlink features unavailable), the masking question is answered (yes, the dependency gap
masks both the symlink gap and the AVM-marker gap), and the candidate triage rule block dev-scores
23/23 with 3 freeze-blocking defects reported below (`gen-squashfs.py` silently drops
directory-target symlinks; `--comp xz` carriers are undecodable by sasquatch 4.5.1; two cells of
the triage grammar are ambiguous and one class condition changes under measured data).**

Seat `R39C2ReconDep`, leaf. Base `a2f64e1da78afcf8cc39287106604dbcc270844c` (not touched). No
write outside `.ufo/waves/round-39/w1/artifacts/R39C2ReconDep/` and this file. No VCS mutation, no
commit, no `PROVINCE/SKILL/SCORECARD/LOG/plans/tools/corpus` write, no REA on K5/K6, no held-out
carrier built or run, no `xd://mcp__rea_*` device. Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39C2ReconDep` removed at the end; every cited envelope, log and
carrier is copied into the artifacts dir.

Tooling used as installed (no installs or upgrades this wave, so no authorization entry needed):
rea-agents **6.5.0** (npx resolution `/run/user/1000/fnm_multishells/5071_1793027685454/bin/npx`,
package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, `package.json`
version 6.5.0), unblob **26.6.4** (`unblob --version`), `sasquatch` and `sasquatch-v4be`
**4.5.1 (2022/03/17)** (`-version`, "unsquashfs version 4.5.1"). pacman untouched.

---

## 1. What was run

Carriers were built only from fresh trees I authored in scratch, with
`tools/round-37/gen-squashfs.py` (`python3 "$GEN" TREE OUT --endian le|be|avm --comp gzip|xz`).
14 carriers (all in `artifacts/R39C2ReconDep/carriers/`), 23 REA `extract-firmware` runs
(23 envelopes in `artifacts/R39C2ReconDep/envelopes/`, 15 pre-existing round-38 receipts read
separately). `artifacts/R39C2ReconDep/build.sh` is the exact reproduction (syntax-checked with
`sh -n`, exit 0).

Dependency-missing runs strip `$HOME/.local/bin` from the child PATH and keep the unblob command
absolute:

```
cd "$S" && env PATH=/usr/local/bin:/usr/bin:/bin REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  $(command -v npx) -y rea-agents@6.5.0 extract-firmware --format json --full-output \
  img/<carrier>.sqsh out/stripped/<carrier>
```

(`/usr/local/bin:/usr/bin:/bin` contains no `sasquatch*`: verified with
`env -i PATH=/usr/local/bin:/usr/bin:/bin sh -c 'command -v sasquatch sasquatch-v4be'` → nothing,
while `npx`/`node` still resolve because REA itself is launched by absolute path and `/usr/bin/node`
exists.) Controls use the interactive PATH with both sasquatch builds reachable. **Every REA run
exited 0** (`ok: true` in all 23 envelopes); `--full-output` envelopes are all 5–17 KB, so none
needed gzipping.

## 2. Feature table (all values read from the envelope, not from prose)

Files are `artifacts/R39C2ReconDep/feature-table.md` (same data, table form) and `features.json`
(machine form). `H/G/D/BE/SR/P` are exactly the L1 grammar's features; `bytes` is
`normalized_result.published_bytes`.

| run | carrier | H | G | D | -be | SR | P | bytes | coverage | chunk `extraction_failed` |
|---|---|---|---|---|---|---|---|---|---|---|
| full-be1-gzip | be1-gzip (BE gzip) | squashfs_v4_be | (none) | (none) | n/a | no | 6 | 9055 | complete | false |
| full-be2-gzip | be2-gzip (BE gzip #2) | squashfs_v4_be | (none) | (none) | n/a | no | 3 | 5018 | complete | false |
| full-le1-gzip | le1-gzip (LE gzip) | squashfs_v4_le | (none) | (none) | n/a | no | 3 | 6017 | complete | false |
| full-le2-gzip | le2-gzip (LE gzip #2) | squashfs_v4_le | (none) | (none) | n/a | no | 3 | 15 | complete | false |
| full-be-dirempty-gzip | be-dirempty-gzip (image = one empty dir) | squashfs_v4_be | (none) | (none) | n/a | no | **0** | 0 | complete | false |
| full-be-linkonly-gzip | be-linkonly-gzip (intended dir-target link — see D1) | squashfs_v4_be | (none) | (none) | n/a | no | 0 | 0 | complete | false |
| full-be-sym-gzip | be-sym-gzip (2 in-tree links) | squashfs_v4_be | unpublished-entry | (none) | n/a | no | 3 | 38 | partial | false |
| full-be-esc-gzip | be-esc-gzip (1 escaping link) | squashfs_v4_be | (none) | (none) | n/a | **yes** | 3 | 34 | partial | false |
| full-be1-avm | be1-avm (patched AVM marker) | squashfs_v4_be | extractor-failure | (none) | **no** | no | 0 | 0 | partial | true |
| full-be1-avm-native | be1-avm-native (`--endian avm`) | squashfs_v4_be | extractor-failure | (none) | **no** | no | 0 | 0 | partial | true |
| full-be1-corrupt | be1-corrupt (damaged metadata tail) | squashfs_v4_be | extractor-failure | (none) | **yes** | no | 0 | 0 | partial | true |
| full-le1-corrupt | le1-corrupt (LE, damaged tail) | squashfs_v4_le | extractor-failure | (none) | **no** | no | 0 | 0 | partial | true |
| full-be1-xz | be1-xz (`--comp xz`) | squashfs_v4_be | extractor-failure | (none) | yes | no | **6** | **19** | partial | true |
| full-le1-xz | le1-xz (`--comp xz`) | squashfs_v4_le | extractor-failure | (none) | no | no | **3** | **0** | partial | true |
| full-not-squashfs | not-squashfs.bin (1 KiB random) | **(none)** | (none) | (none) | n/a | no | 0 | 0 | complete | — (no chunk) |
| **stripped-be1-gzip** | be1-gzip | squashfs_v4_be | missing-extractor-dependency | **sasquatch-v4be** | n/a | no | 0 | 0 | partial | true |
| **stripped-be2-gzip** | be2-gzip | squashfs_v4_be | missing-extractor-dependency | **sasquatch-v4be** | n/a | no | 0 | 0 | partial | true |
| **stripped-be1-gzip-repeat** | be1-gzip (determinism repeat) | squashfs_v4_be | missing-extractor-dependency | **sasquatch-v4be** | n/a | no | 0 | 0 | partial | true |
| **stripped-le1-gzip** | le1-gzip | squashfs_v4_le | missing-extractor-dependency | **sasquatch** | n/a | no | 0 | 0 | partial | true |
| **stripped-le2-gzip** | le2-gzip | squashfs_v4_le | missing-extractor-dependency | **sasquatch** | n/a | no | 0 | 0 | partial | true |
| stripped-be-sym-gzip | be-sym-gzip (in-tree links) | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | **no** | 0 | 0 | partial | true |
| stripped-be-esc-gzip | be-esc-gzip (escaping link) | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | **no** | 0 | 0 | partial | true |
| stripped-be1-avm | be1-avm (AVM marker) | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | **n/a** | no | 0 | 0 | partial | true |

Two more carriers were built and run but are **not** representative evidence for the triage
classes; both are recorded in the table above / below: `be-linkonly-gzip` (intended as an in-tree
dir-target symlink — the generator dropped the link, see defect D1; envelope `full-be-linkonly-gzip`
is therefore indistinguishable from a clean zero-file image) and the two `xz` carriers (defect D2).

Corroboration from pre-existing lane evidence, read-only (`artifacts/round38-receipts-scored.json`):
`corpus/evidence/round-38/c1/K{1..4}/before.json` (bare `data` objects, no `ok` key) are **all**
`H={squashfs_v4_be}`, `G={missing-extractor-dependency}`, `D={sasquatch-v4be}`, `P=0` — the
round-38 "before" runs had no `sasquatch-v4be` on the child PATH. `K1/after.json` is
`G=∅, SR=yes, P=5` (escaping link, `MaliciousSymlinkRemoved`), `K2/after.json` is
`G={unpublished-entry}, P=3`, `K3/K4 after` are clean. Raw fields, e.g. `K1/before.json`:

```json
"extraction_gaps": [{"kind":"missing-extractor-dependency","input_path":"$input","relative_path":null,
  "handler":"squashfs_v4_be","provider_id":"3093997:1","range":{"offset":0,"length":9780},
  "root_file_range":{"offset":0,"length":9780},"dependencies":["sasquatch-v4be"],
  "continuation_id":"4ca863d04cc06d61e7be38d0811847a15f55c70f028fdf45e8fefdf75957a07a"}]
"diagnostics": [{"stage":"squashfs_v4_be","report":{"severity":"ERROR",
  "dependencies":["sasquatch-v4be"],"__typename__":"ExtractorDependencyNotFoundReport"}}]
```

The dependency-gap `continuation_id` is a hash of the static instruction, identical across
carriers and runs — it carries no per-run information.

## 3. The dependency outcome, precisely

**G (gap kinds)** — exactly one row, `{missing-extractor-dependency}`, `input_path == "$input"`,
`handler == squashfs_v4_be|squashfs_v4_le`, `relative_path == null`, `range`/`root_file_range`
equal to the whole-image chunk, `provider_id` set. Not `extractor-failure`: REA separates them by
whether the provider reported an `ExtractorDependencyNotFoundReport` (kind
`missing-extractor-dependency`) or only an `ExtractCommandFailedReport`
(kind `extractor-failure`). No second (task-level) duplicate gap appears, because the report is
nested inside the `ChunkReport` and only the chunk path is emitted — `grep` of the source confirms
`chunkGaps("extractor-failure", …)` explicitly excludes chunks covered by a dependency row
(`dist/firmware/FirmwarePublication.js`).

**D (dependencies)** — **yes, exactly one name, and it is the executable REA/unblob actually tried
to run**: `["sasquatch-v4be"]` for every BE v4 image (3 BE carriers + 3 masked variants, 6 runs;
plus 4 round-38 `before` receipts) and `["sasquatch"]` for every LE v4 image (2 LE carriers, 3
runs). It is never both, even though unblob's handler-level `get_dependencies()` returns
`[sasquatch, sasquatch-v4be]` (`unblob/handlers/filesystem/squashfs.py:68-69`): the *report* comes
from `Command.extract`, whose `FileNotFoundError` handler raises
`ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())` and
`Command.get_dependencies()` returns `[self._executable]`
(`unblob/extractors/command.py:69-71`, `:101-102`) — i.e. the single argv[0] that was missing. The full
handler-level pair only shows up in `unblob --show-external-dependencies`, never in an envelope.

**BE (`-be` in child argv)** — **`n/a` for every dependency-missing run**, on both endians. The
`command` field exists only on `ExtractCommandFailedReport`; a dependency failure records no
command (no argv was ever built), so no report names sasquatch at all and the grammar's `-be`
feature is `n/a`. Rationale from source: unblob constructs the argv inside
`SquashFSExtractor.extract` only after `get_endian(file, …)` succeeds, and `Command` only records
the joined argv on a non-zero exit. Consequence for C2: **the two dependency classes can never be
separated by the `-be` column**; they must be keyed on `handler` and/or `dependencies`.

**SR (symlink removed)** — `no` in every dependency-missing run, including the BE carrier that
holds an **in-tree** symlink (`stripped-be-sym-gzip`) and the BE carrier that holds an **escaping**
symlink (`stripped-be-esc-gzip`). No `MaliciousSymlinkRemoved` anywhere: unblob never extracted a
tree, so `fix_extracted_directory`/`fix_symlink` never ran.

**P (len(files))** — `0`, with `published_bytes == 0`, `coverage == "partial"`, `ok == true` on the
top-level envelope. Also `chunks[0].extraction_failed == true`, and
`normalized_result.diagnostics[] = [{stage: "squashfs_v4_be", report: {__typename__:
"ExtractorDependencyNotFoundReport", severity: "ERROR", dependencies: ["sasquatch-v4be"]}}]`
(`normalized_result.diagnostics[].missing_dependencies: ["sasquatch-v4be"]` is also present; that
field is not in the L1 grammar).

### Masking (the assignment's key question): yes, completely

Under a missing extractor the dependency gap **masks every other discriminator** the C2 table
would use. Measured, same carrier with and without the extractor:

| carrier (property) | full PATH | stripped PATH |
|---|---|---|
| be-sym-gzip (2 in-tree links) | G={unpublished-entry}, SR=no, P=3 | G={missing-extractor-dependency}, SR=no, P=0 — no `unpublished-entry` at all |
| be-esc-gzip (1 escaping link) | SR=yes, G=∅, P=3 | G={missing-extractor-dependency}, **SR=no**, P=0 |
| be1-avm (AVM marker) | G={extractor-failure}, **BE=no**, P=0 | G={missing-extractor-dependency}, **BE=n/a**, P=0 |

So an in-tree/escaping symlink question and an AVM-marker question are both invisible while the
extractor is absent: the envelope is byte-for-byte equivalent (modulo ids/ranges) to a plain
BE image with no links and no marker. This is exactly what makes `dep-missing-be` /
`dep-missing-le` safe as *first* rows but also means **C2 must generate its symlink/AVM classes
with the extractor present** — a stripped-PATH held-out run of those classes would silently
produce `dep-missing-*` and the class assignment would be wrong.

Determinism: `stripped-be1-gzip` and `stripped-be1-gzip-repeat` are identical on every grammar
feature (`H,G,D,BE,SR,P,ok`) — expected, since the gap is produced before any image byte is read.

## 4. Exact JSON paths (all verified against the envelopes)

Full CLI envelope (stdout of `--format json --full-output`, one line):
`{"ok": true, "data": {...data object...}, "meta": {...}}`.

| feature | path |
|---|---|
| top-level success | `ok` |
| handlers | `data.normalized_result.chunks[].handler` |
| failed chunk | `data.normalized_result.chunks[].extraction_failed` |
| gap kinds | `data.normalized_result.extraction_gaps[].kind` |
| gap dependencies | `data.normalized_result.extraction_gaps[].dependencies` (list, sorted, may be `[]`) |
| gap handler / range | `data.normalized_result.extraction_gaps[].handler`, `.input_path`, `.range`, `.root_file_range`, `.provider_id`, `.relative_path`, `.continuation_id` |
| unpublished entries | `data.normalized_result.unpublished_entries[].kind` (`"symlink"` observed), `.relative_path`, `.link_target` (raw target string, e.g. `"../../hello.txt"`) |
| diagnostics typename | `data.normalized_result.diagnostics[].report.__typename__` — observed `ExtractorDependencyNotFoundReport`, `ExtractCommandFailedReport`, `MaliciousSymlinkRemoved` |
| the failed argv | `data.normalized_result.diagnostics[].report.command` — **string** (`shlex.join`), e.g. `"sasquatch-v4be -be -no-exit-code -f -d <outdir> <inpath>"`; also `exit_code`, base64 `stderr`, `stdout` |
| diagnostic stage | `data.normalized_result.diagnostics[].stage` (handler name for extractor reports; **null** for `MaliciousSymlinkRemoved`) |
| published files / bytes | `data.normalized_result.files` (len = P), `data.normalized_result.published_bytes` |
| coverage | `data.normalized_result.coverage` (`complete` / `partial`) |
| extra normalized maps | `data.normalized_result.diagnostics[].missing_dependencies` (task-level), `…[].chunk_missing_dependencies` — internal names, not in the grammar |

The **bare `data` object** form (round-38 receipts, and what a receipt file stores) has exactly the
same paths minus the outer `ok`/`meta`: `normalized_result.*` at top level and **no `ok` key** —
the interpreter must not require `ok`. `SR` may also appear under `raw_result.report`
(`data.raw_result.report[].…__typename__`), which the grammar allows; in every envelope I measured
the same typename is present under `normalized_result.diagnostics[].report`.

## 5. The triage table contract — dev-scored, with the ambiguities pinned

I implemented the grammar literally in `artifacts/R39C2ReconDep/sqfs-triage-dev.py` (dev harness,
not the frozen tool — the L1 owns `tools/round-39/sqfs-triage.py`) and wrote the candidate rule
block as `artifacts/R39C2ReconDep/candidate-triage-rows.md` (marker `<!-- sqfs-triage-table v1 -->`,
exact 9-cell header, 8 rows, rules ordered). Dev score over my 23 envelopes: **23/23**, zero
mismatches (`dev-scored.json` vs `expectations.json`). Negative controls (`controls/`) prove the
score is not vacuous: catch-all `*|*|*|*|*|*` → 0/23 (one label for everything); gap-kind-only
table → 0/23; published-bytes-only table → 0/23. Malformed cells exit 2 as required:
`published files = 1` → exit 2 `bad published files cell '1'`; `gap kinds = a++b` → exit 2
`malformed set cell 'a++b'`; `-be = maybe` → exit 2.

Cross-check on lane evidence: the harness classifies the 8 round-38 receipts as 4×
`dep-missing-be` (`before`), 1× `escaping-symlink-removed` (K1 after), 1×
`in-tree-symlink-metadata` (K2 after), 2× `clean` (K3/K4 after) — which is exactly what those runs
did, in the bare-`data` form.

Contract gaps the freeze must pin (each changes which envelopes a row can match):

1. **`*` in the set columns.** The prose says "`*` matches anything" *before* enumerating
   `gap kinds`/`dependencies` as `none` or `a+b`, so a catch-all control table
   (`* | * | * | * | * | * | *`) is either a wildcard table (evaluable, matches everything, 0/N) or
   a malformed table (exit 2). I implemented the global reading (wildcard). Either way the
   catch-all control stops C2, but the L1 should state which, because exit 2 vs 0/N is a different
   receipt.
2. **"names sasquatch" is substring or exact token.** All measured commands are `sasquatch …` or
   `sasquatch-v4be …`. Under substring semantics (what I implemented, and what the class design
   needs) a corrupt-body BE image gives `-be yes` while an AVM-marker BE image gives `-be no`.
   Under exact-token semantics no BE command ever "names sasquatch", both become `n/a`, and
   `avm-marker-be-dropped` and `body-extractor-failure` collapse — the class list would be
   unattainable. Pin substring.
3. **`published files` for `body-extractor-failure` must allow `>0`.** Measured: the two `xz`
   carriers publish 6 files / 3 files while the chunk reports `extraction_failed: true` and the gap
   is `extractor-failure`. A `0`-only cell misses them.
4. **`published files` for `clean` must allow `0`.** Measured: an image whose tree is one empty
   directory extracts with `chunks[].extraction_failed == false`, `G=∅`, `SR=no`, `coverage
   complete`, and `P=0` (`full-be-dirempty-gzip`). A `>0` cell makes it `unclassified`, and it is
   also the shape a *real* clean carrier takes when the tree yields no regular files. `*` is the
   safe cell; `no-squashfs-chunk` is still separable because it is keyed on `handler == none`.
5. **`coverage` is not a usable proxy for "nothing happened".** `full-not-squashfs` (no chunk, no
   gap) reads `coverage: "complete"` with `P=0`, i.e. "complete" over an unexamined input. Do not
   fold coverage into a `clean` condition.

Candidate rows (full text with causes/actions/sources in the artifact):

```
no-squashfs-chunk      | none             | none                          | none          | n/a | no | 0
dep-missing-be         | squashfs_v4_be   | missing-extractor-dependency  | sasquatch-v4be| n/a | no | 0
dep-missing-le         | squashfs_v4_le   | missing-extractor-dependency  | sasquatch     | n/a | no | 0
avm-marker-be-dropped  | squashfs_v4_be   | extractor-failure             | none          | no  | no | *
body-extractor-failure | squashfs_v4_*    | extractor-failure             | none          | *   | no | *
escaping-symlink-removed | squashfs_v4_*  | none                          | none          | n/a | yes| *
in-tree-symlink-metadata | squashfs_v4_*  | unpublished-entry             | none          | n/a | no | *
clean                  | squashfs_v4_*    | none                          | none          | n/a | no | *
```

Order is load-bearing twice: `no-squashfs-chunk` must precede everything (H empty), and
`avm-marker-be-dropped` must precede `body-extractor-failure` (the AVM row is the `-be no`
specialisation of an `extractor-failure` gap on `squashfs_v4_be`; the generic row keeps `*` so it
covers LE body failures, whose argv is `sasquatch -le …` and therefore also `-be no`).
`no-squashfs-chunk` is **distinct in recon** — but as "no gap at all", not as a
`no-squashfs-chunk` kind: unblob emits nothing for an unrecognised input, and the
`unknown-chunk-handler` gap only appears when Binwalk is configured (`REA_BINWALK_COMMAND`), which
no run here had. If the L1's held-out run configures Binwalk, that class's envelope changes shape
(`G={unknown-chunk-handler}`, `H=∅`) and the row as written would no longer match.

Encrypted chunks (`encrypted-chunk`) and depth ceilings (`depth-limited`) never appeared and are
not covered by the candidate rows.

## 6. Defects and freeze risks

**D1 (high, blocks carrier correctness). `tools/round-37/gen-squashfs.py` silently drops any
symlink whose target is a directory.** Enumeration is
`for root, dnames, fnames in os.walk(tree)` + `for fn in fnames: if os.path.islink(p): links.append(...)`
(`gen-squashfs.py:59-67`); `os.walk` puts a directory-target symlink into `dnames`, so it never
reaches `links`, is never given an inode, and is never written as a directory entry. Measured on
tree `be-linkonly` (`docs/libdir-link -> ../lib`): the writer printed `inodes 3` (root+docs+lib,
no link), `sasquatch-v4be -be` printed `created 0 symlinks`, the extraction contains only the two
directories, and an REA run yields `P=0, G=∅` (`envelopes/full-be-linkonly-gzip.json`). Consequence
for the freeze: a K5/K6 `symlinks.tsv` (or a C2 held-out manifest) built from the source tree would
list a link the image does not contain — the C1 predicate "gaps exactly on the frozen oracle's
in-tree symlinks" would then be unsatisfiable, or an `in-tree-symlink-metadata` held-out carrier
would silently be a `clean` zero-file image. Mitigation available without touching `tools/`: keep
every symlink's target a **regular file** (all my in-tree/escaping dev carriers do this and behave
as designed). If directory-target links are wanted, the generator needs
`for p in list(dnames): if os.path.islink(join(root,p)): …` (did not implement — `tools/` is out of
my bounds).

**D2 (high, blocks carrier correctness). `--comp xz` produces images sasquatch 4.5.1 cannot
decode.** Both endians: `full-be1-xz` → `extractor-failure`, `-be yes`, **6 files published, 19
bytes total**; `full-le1-xz` → `extractor-failure`, `-be no`, **3 files, 0 bytes**. stderr
(sasquatch): `Trying to decompress with xz... 4096 33 ... FATAL ERROR: writer: failed to
read/uncompress file …/payload.bin` — the writer's raw-LZMA2 stream is rejected by every
decompressor. So any `xz` carrier reads as `body-extractor-failure` with partially published files,
which would break C1's "names `squashfs_v4_be` with no failed chunk". **Build every K5/K6 and
held-out C2 carrier with `--comp gzip`.** (Also the reason risk 5.3 above matters: this is the only
way I could produce a failing extraction that still publishes files.)

**D3 (medium, table semantics).** The two grammar ambiguities in §5 (`*` in set cells; "names
sasquatch"). Pin both in the freeze commit, before any held-out generation.

**D4 (low, AVM generation).** `--endian avm` needs no patcher: `gen-squashfs.py` writes
`mkfs = bytes_used if e == 'avm' else MKFS_TIME`, and the image is **byte-identical** to my
superblock patch (both `67fafa05d31d8f843290e702b2a1ab5d7cd42cf78ea526d604d2f19e9e76a966` for the
same tree). The AVM rule unblob applies is `bytes_used == mkfs_time`
(`unblob/handlers/filesystem/squashfs.py:48-50`, BE v4 only) and it *omits* `-be`; recovery per
round-38 is `sasquatch-v4be -be`. Keep `make-avm-copy.py` only as a cross-check.

**D5 (informational, C1 predicate wording).** K1's `link-to-hello -> ../hello.txt` sits at the image
root, so it resolves outside the image root and is **escaping** under the round-39 rule — matching
unblob's observed removal (`unblob/extractor.py fix_symlink` → `MaliciousSymlinkRemoved`,
`stage: null`). My independent `be-esc-gzip` (`escape-link -> ../outside.txt`) reproduces the same
outcome, and `be-sym-gzip` reproduces the in-tree metadata outcome with the link target preserved
verbatim in `unpublished_entries[].link_target`. The round-39 symlink rule is therefore stated
consistently with the tool: in-tree → one `unpublished-entry` gap and the link kept as metadata;
escaping → removed, `MaliciousSymlinkRemoved`, **no gap**.

## 7. Limits (what I did not establish)

- Not exercised: encrypted chunks, `depth-limited`, Binwalk-configured `unknown-chunk-handler`,
  multi-file (7z) nested dependency reports, nested derivations, and a real-world vendor image.
- A second missing dependency on the same chunk (both sasquatch builds absent) is unpublished
  territory: for BE only `sasquatch-v4be` is attempted, so I expect `["sasquatch-v4be"]` only
  `[INFERENCE]`; not measured separately because stripping `~/.local/bin` already removes both.
- Directory-target symlinks could not be measured (D1); absolute-target symlinks not measured
  (unblob strips the leading `/` and treats them as in-tree `[INFERENCE]` from
  `extractor.py:fix_symlink`, not observed).
- `no-squashfs-chunk` was measured only without Binwalk; with `REA_BINWALK_COMMAND` configured the
  envelope would gain an `unknown-chunk-handler` gap `[INFERENCE]` from
  `FirmwarePublication.js:chunkGaps`.
- All class labels here are **development** labels from my own trees; no held-out carrier was built
  or run, and no K5/K6 carrier was touched or extracted.

## 8. Files changed / artifacts

No lane file outside my artifact dir was written; no VCS operation.

`artifacts/R39C2ReconDep/`
- `build.sh` — exact reproduction of all 14 carriers and 23 runs (`sh -n` clean).
- `make-avm-copy.py`, `make-corrupt-copy.py` — deterministic AVM-marker and metadata-tail damage
  tooling used to build the dev carriers (D4 cross-check).
- `carriers/` — 14 dev carriers (`be1-gzip`, `be2-gzip`, `le1-gzip`, `le2-gzip`, `be-sym-gzip`,
  `be-esc-gzip`, `be-dirempty-gzip`, `be-linkonly-gzip`, `be1-avm`, `be1-avm-native`,
  `be1-corrupt`, `le1-corrupt`, `be1-xz`, `le1-xz`), sha256 in `features.json`.
- `envelopes/` — 23 full REA envelopes (`{ok,data,meta}`, 5–17 KB each, uncompressed).
- `logs/` — stderr of each REA run, plus the direct `unblob -v` / `sasquatch-v4be` runs used for D1.
- `feature-table.md`, `features.json` — the §2 table with every feature and sha256.
- `candidate-triage-rows.md` — the 8-row rule block in the L1's grammar (marker + exact header).
- `sqfs-triage-dev.py` — literal implementation of the grammar (dev harness).
- `expectations.json`, `dev-scored.json` — 23/23 dev score.
- `controls/` — catch-all / gap-kind-only / published-only / 3 malformed-cell tables and results.
- `round38-receipts-scored.json` — the 8 pre-existing round-38 receipts classified by the harness.

Report: `.ufo/waves/round-39/w1/R39C2ReconDep.md`
