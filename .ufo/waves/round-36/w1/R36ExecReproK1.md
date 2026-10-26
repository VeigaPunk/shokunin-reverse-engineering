# R36ExecReproK1 — independent reproduction of R36-C1 carrier K1

Seat: `R36ExecReproK1` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Measured revision: lane `HEAD` = `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`,
freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`; freeze commit and `tools/round-27/xpin-attribute.mjs` present at freeze,
`git diff --stat 790561d4 -- tools/round-27/xpin-attribute.mjs tools/round-36/c1-counter.py corpus/evidence/round-36/c1/`
shows only the four `K*/after*` evidence files added). Read-only git only; no VCS mutation, no `pacman`, nothing installed.

Scope: reproduce the K1 receipt pair only (K2–K4, PROVINCE/entry/SOURCES bindings, and the C2 claim are other seats).

**Verdict: K1 reproduces exactly.** Both of my fresh runs equal the committed `K1/after.json` and `K1/before.json`
field-for-field once run-local directory names and the unblob blob-store id are normalised; the oracle is byte-identical.
The evidence ids differ, and the difference is proven to be caused only by those run-local fields (per the REA 6.5.0
rule, recomputed with the frozen `xpin` tool) — not counted, as instructed.

## 1. Carrier

| item | value |
|---|---|
| source | lane fixture `corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh` (no download needed) |
| size | 73728 B |
| sha256 | `93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589` |
| frozen digest in `c1/carriers.json` | `93802938486d952abe0f06a83b55ca882e2272805ea11dcc3c35b9b9c9b8a589` (match) |
| header | magic `hsqs` at offset 0 (squashfs offset 0) |
| unblob file-magic (from the receipts) | `Squashfs filesystem, little endian, version 4.0, xz compressed, 70482 bytes, 5 inodes, blocksize: 131072 bytes, created: Thu Jan 1 00:00:00 1970` |
| committed K1 receipts vs `HEAD` blobs | `after.json`, `before.json`, `oracle.tsv`, `after-run.json`, `before-run.json`, `oracle-run.json` all byte-identical to `d2e46ef5:corpus/evidence/round-36/c1/K1/*` (`git show … \| cmp`) |

## 2. Environment (all measured, not assumed)

| tool | version / identity |
|---|---|
| REA | `rea-agents` 6.5.0 from `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` (`name=rea-agents`, `version=6.5.0`); run through `npx -y rea-agents@6.5.0`, i.e. the frozen `--pkg65` root, no new install |
| node / npx | v24.21.0 / 11.19.0 |
| unblob | 26.6.4; `~/.local/bin/unblob -> /home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`; receipt `engine.executable_sha256 = 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`, `worker_count = 1` |
| sasquatch | `~/.local/bin/sasquatch`, 382824 B, sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` (equals committed `after-run.json`'s `sasquatch_sha256`), `sasquatch -version` → `unsquashfs version 4.5.1 (2022/03/17)` |
| oracle extractor | `/usr/bin/unsquashfs` 4.7.5 (2026/03/01) |
| PATH | 20 directories; exactly one contains an executable named `sasquatch` (`/home/vgpnk/.local/bin`); filtered PATH = 19 directories |
| `REA_UNBLOB_COMMAND` | `$HOME/.local/bin/unblob` |

`find`-style PATH audit (`os.access(join(dir,'sasquatch'), X_OK)`) printed only `/home/vgpnk/.local/bin -> /home/vgpnk/.local/bin/sasquatch`;
the stripped PATH was verified by `PATH=<filtered> command -v sasquatch` returning empty.

## 3. Commands run (exact) and exit codes

Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK1`, `TMPDIR` set per run, `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`.
Output directories were absent before each run (`<path> <fresh out dir>`), carrier given as the lane fixture.

```bash
# run A — sasquatch on PATH  ("after")
TMPDIR=$S/tmp-after npx -y rea-agents@6.5.0 extract-firmware --format json \
  <lane>/corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh  $S/after-out   > $S/after.json   # exit 0, 2 s
# run B — every PATH dir containing an executable `sasquatch` removed  ("before")
P=$(python3 -I -c '…filter dirs holding sasquatch…' "$PATH")
PATH=$P TMPDIR=$S/tmp-before npx -y rea-agents@6.5.0 extract-firmware --format json \
  <lane>/corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh $S/before-out  > $S/before.json  # exit 0, 2 s
# run A2 — repeat of run A for determinism                                            # exit 0, 2 s
# oracle — independent unsquashfs at offset 0 (same snippet as c1-run.sh oracle)
/usr/bin/unsquashfs -no-progress -o 0 -d "$S/root" <carrier>                          # exit 0, 3 inodes written
# oracle again with the sasquatch-free PATH                                           # exit 0
# evidence-id recomputation with the frozen tool
node <lane>/tools/round-27/xpin-attribute.mjs --pkg65 <pkg> --pkg67 <pkg> <4 wrapped envelopes>  # exit 0
# frozen counter at HEAD (context only)
HYAKU_SCRATCH=$S/counter-scratch python3 -I -B tools/round-36/c1-counter.py \
  --root <lane> --rev d2e46ef5… --freeze 790561d4… --pkg65 <pkg> --json-out $S/counter-head.json   # exit 1 (see §8)
```

All stderr from the two REA runs was empty after `npm warn` filtering; no retries were needed.

## 4. Run A ("after", sasquatch on PATH) vs committed `K1/after.json`

`normalized_result.files` — 3 entries, set equality **true** (relative_path, sha256, size identical):

| relative_path | sha256 | size |
|---|---|---|
| `firmware.bin_extract/README.txt` | `88dc952ab79570963415341ba52c7e2a948aa69e0200987140a933c64d595961` | 59 |
| `firmware.bin_extract/etc/config.ini` | `bf53724aca93538b630cf8742260b38426a317d5593ca1653e404710a48d9fef` | 27 |
| `firmware.bin_extract/payload.bin` | `5b61b3262ca03ec21a79929502a9182d60a055e06fabe9f990ee2182fe11824f` | 70000 |

Hashing the three published files on disk reproduces the same three sha256 values (independent of the receipt fields).
`extraction_gaps` = `[]` in both (0 vs 0). Normalised result: `coverage = complete`, `published_bytes = 70086`
(= 59+27+70000), `unpublished_entries = []`, `depth_limited_paths = []`,
`chunks = [{handler: squashfs_v4_le, range 0..73728, root_file_range 0..73728, encrypted false, extraction_failed false}]`.
Engine exit: unblob `exit_code 0`; REA exit 0. Evidence id (mine): `ev_84ce512667f0179691dd7f63260c2834b69c4792d204467f60c07f9ac6aa0bea`.

## 5. Run B ("before", no sasquatch on PATH) vs committed `K1/before.json`

`normalized_result.files` = `[]` in both (0 vs 0). `coverage = partial`, `published_bytes = 0`,
`chunks[0].extraction_failed = true`, `diagnostics = [{stage: squashfs_v4_le, missing_dependencies: ["sasquatch"],
report: {severity: ERROR, dependencies: ["sasquatch"], __typename__: ExtractorDependencyNotFoundReport}}]`.
unblob `exit_code 1`; REA exit 0 (the receipt still describes the miss — as in the committed receipt).

One `extraction_gaps` entry, all 9 fields compared against the committed gap:

| field | mine | committed | equal |
|---|---|---|---|
| kind | `missing-extractor-dependency` | same | ✔ |
| dependencies | `["sasquatch"]` | same | ✔ |
| handler | `squashfs_v4_le` | same | ✔ |
| input_path | `$input` | same | ✔ |
| relative_path | `null` | same | ✔ |
| range | `{offset:0, length:73728}` | same | ✔ |
| root_file_range | `{offset:0, length:73728}` | same | ✔ |
| continuation_id | `4ca863d04cc06d61e7be38d0811847a15f55c70f028fdf45e8fefdf75957a07a` | same | ✔ |
| provider_id | `528937:1` | `245252:1` | ✘ — run-local blob-store id (same role as the file `blob_id`s; see §7) |

Evidence id (mine): `ev_4afc395f26c9a58bc86dd7c0642a015e528cab6ba46fcc9fe72a489f52ef3a47`.

## 6. Oracle (`/usr/bin/unsquashfs`, offset 0) vs committed `K1/oracle.tsv`

3 regular files; `diff -u` of committed vs my regenerated TSV (same python normaliser as `tools/round-36/c1-run.sh`,
`regular files only, symlinks skipped, sorted`) → **no differences, exit 0**; log tail `created 0 symlinks` and
`3 inodes (3 blocks) to write`. Rows: `README.txt` 88dc952a… (59 B), `etc/config.ini` bf53724a… (27 B),
`payload.bin` 5b61b326… (70000 B) — the same three digests the "after" run publishes.

Oracle independence: re-ran unsquashfs with the sasquatch-free PATH → exit 0, same three rows. (The first comparison of
that second run showed a *reordering only*, because I sorted with locale collation — `etc/`, `payload.bin`, `README.txt`;
re-sorting with `LC_ALL=C` gave byte-identical content. Content equal, ordering artifact not a difference in data.)

## 7. Evidence ids: differ only through run-local fields (not counted)

Observations: my ids (`ev_84ce51…`, `ev_4afc39…`) differ from the committed ids (`ev_b5bd2e…`, `ev_df7bef…`).
Two independent checks show the delta is entirely run-local:

1. Frozen `xpin-attribute.mjs` (`--pkg65/--pkg67` both = rea-agents 6.5.0) recomputes **stored == 6.5.0 == 6.7.0** for
   my two envelopes *and* for the two committed envelopes (exit 0). So each receipt is internally consistent under the
   pinned rule; only the inputs differ.
2. Substituting my run-local values into the **committed** envelope makes it byte-identical to my envelope apart from
   `evidence_id`, and `xpin` then recomputes **my** id from that substituted committed envelope
   (after: `ev_84ce5126…`, before: `ev_4afc395f…`, exit 0).
   Substituted fields: `parameters.output_directory`, the REA work dir (`…/c1-run.dcmJTg/rea-firmware-ris5IG` ↔
   `…/R36ExecReproK1/tmp-after/rea-firmware-JTOmbl`; before: `…/c1-run.ktJiZv/rea-firmware-X5JDA1` ↔
   `…/tmp-before/rea-firmware-6BKpQZ`), `subject.local_path` / `parameters.path`
   (`…/L1/carriers/k1-le-xz.sqsh` ↔ the lane fixture path — same sha256), and the unblob blob-store ids
   (`348733:`/`245252:` ↔ `528938:`/`528937:`).
After substituting those, the leaf-by-leaf comparison yields the same 258 leaf keys on both sides for `after` (no key
only-mine, none only-committed; exactly one key differs — `evidence_id`), and the same 131 keys for `before` (again only
`evidence_id` differs). A coarser first pass that scrubbed only the output directory and blob ids left 21 `raw_result`
path leaves differing solely by the `rea-firmware-XXXX` work-dir component; adding that component closes all of them. Everything the predicate reads — files, gaps, provider, operation,
subject digest, coverage, diagnostics, continuation id, limitations, relationship_coverage, confidence/authority — is equal.

Determinism: run A2 (second "after") published the identical file set and gaps as run A and as the committed receipt
(its own id `ev_7c07abe297fabce4c75ebe228db836ad50ad399729c993cd41c29b6fab11f735`, from its own work dir).

## 8. Mechanism corroboration (why the dependency list is exactly `["sasquatch"]`)

- unblob `…/site-packages/unblob/handlers/filesystem/squashfs.py:25-26` declares
  `EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"`; the LE branch sets `executable = self.EXECUTABLE` (:42)
  and builds `Command(executable, "-le", "-no-exit-code", "-f", "-d", "{outdir}", "{inpath}")` (:56-64).
- `…/unblob/extractors/command.py:70-75` raises `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())`
  only on `FileNotFoundError`; `Command.get_dependencies()` (:101-102) returns `[self._executable]`. Hence the report names
  the one executable that was actually missing/tried — `["sasquatch"]` — and the after run's unblob `exit_code 0`
  means that command ran and succeeded.
- REA does not hard-code the name: `grep -rn sasquatch …/rea-agents/dist` returns nothing, while
  `dist/domain/firmware/firmwareAnalysis.js:85` lists `missing-extractor-dependency` in the gap enum and the
  `extractionGap` schema documents `dependencies` as “Extractor executables named by the producer; empty when it named none.”
  My before run's raw task report carries exactly `ExtractorDependencyNotFoundReport` with `dependencies:["sasquatch"]`
  on the `squashfs_v4_le` chunk (`provider_id 528937:1`, 0..73728).
- Cross-check of the after receipt: `sasquatch` appears **0** times in my `after.json` (grep count) and **0** times in the
  committed `after.json`; 4 times in my `before.json` (gap + diagnostics + continuation text). The after receipt proves the
  result by publishing the oracle files with no gap, not by naming the tool — matching the frozen predicate wording.

Frozen counter at HEAD (`d2e46ef5`), context only, not my claim: exit **1**, `carriers_matched = 4`, `K1.matched = true`
with every K1 sub-binding true (`oracle_frozen`, 3 oracle files, both receipts present/subject/operation/evidence-id-ok,
before gap true + 0 hits, after gap false + 3/3 hits). `met_target = false` only through the wave-1-absent document
bindings (`entry_present`, `sourced`, `province_core_section`, `province_core_row`, `coverage_map_row` all false) — i.e.
the C1 carrier half is already green and the missing half is outside this seat.

## 9. Limits / not tested (advisory)

- K2–K4 were not reproduced here; only K1. Big-endian / AVM SquashFS, vendor-mangled images, loader behaviour and the
  7z fallback were not touched (also excluded by the claim).
- I did not run `c1-counter.py --selftest` (its 14 cases are about `tools/round-36/selftest/dev-*` fixtures, not carriers)
  and did not verify any of the C1 non-carrier conjuncts (PROVINCE Core row, knowledge entry, SOURCES row / `S1070` rules).
- I did not treat evidence-id inequality as a finding, per instruction; §7 shows it is run-local. The unblob blob-store
  ids (`528937:1`, `528938:1`, …) are per-run and cannot reproduce.
- Single host, single kernel (`linux 7.2.11-arch1-1`), single PATH layout; `npx -y` resolved 6.5.0 from the existing
  cache root `ad9a3fdbcad992c6` (no new install), so no version drift was exercised.
- Tooling: nothing installed or upgraded (pacman paused host-wide, not used). Scratch
  `/fast/scratch/hyaku/kaidoku-r36/R36ExecReproK1` (≈ run outputs, oracle trees, xpin wrappers, counter json-out) was
  removed after this report; none of the cited numbers depend on files that remain there, and no path under `/tmp` or
  scratch is used as evidence above.

## 10. Files written

- This report only. No lane file, carrier, counter, harness, oracle or receipt was modified; no VCS operation was performed.
