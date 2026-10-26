# R36W2ExecReproFresh — K3 reproduced from nothing (download → oracle → before → after → diff)

Seat: leaf executor, wave 2. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, lane HEAD
`01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` while I worked. I wrote only this file; no frozen
predicate, counter, carrier, oracle or receipt was changed, and no VCS mutation was performed.

**Verdict: K3 reproduces exactly from a clean download.** The frozen harness's `oracle` output is
byte-identical to the committed `oracle.tsv` (`9924ec69…beec1f0e`, 2130 rows). The `after` published
set equals the committed one as an ordered `(relative_path, sha256)` list (2147 rows, 0/0 set
difference), the `before` published set likewise (2 rows, 0/0), and both envelopes are identical to
the committed ones once 10 run-specific metadata keys (absolute paths / pid-derived blob ids /
`evidence_id`) are removed. The REA pin provenance gap R-3 is closed for these runs by an `execve`
trace: `npx -y rea-agents@6.5.0` executed
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea` →
`…/ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs`, package version **6.5.0**.
Four advisory notes (§8) — none a defect in the committed evidence.

---

## 0. Preconditions (read-only checks before any run)

| Fact | Evidence |
|---|---|
| Lane tip | `git rev-parse HEAD` → `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` |
| I ran the **frozen** harness | `sha256sum tools/round-36/c1-run.sh` = `16907dca7fc7a104acb78d97694924a52e4a87f517348ce7a10eec1c270bf4d4` = `git show HEAD:tools/round-36/c1-run.sh \| sha256sum` |
| Committed K3 evidence is the tip's evidence (worktree sha == `git show HEAD:` sha) | `oracle.tsv 9924ec69…beec1f0e`; `oracle-run.json addcee5d…c3a82bc4ef`; `before.json 6d2457a1…526379b5`; `after.json 861736c9…8b8e01`; `before-run.json 7a8f1cfc…cfcdfcbb`; `after-run.json 94049e9b…822c7d` (all six pairs equal) |
| Carrier spec | `corpus/evidence/round-36/c1/carriers.json` K3 `url` = `https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-x86_64.appimage`, `sha256` = `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb` |
| Tools (all already present; **nothing installed, upgraded or removed**) | `sasquatch` `/home/vgpnk/.local/bin/sasquatch` `unsquashfs version 4.5.1 (2022/03/17)` sha `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`; `unblob` 26.6.4 real path `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` sha `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`; `/usr/bin/unsquashfs` `4.7.5 (2026/03/01)`; node `v24.21.0`, npm `11.19.0` |
| Scratch | `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ExecReproFresh`, `TMPDIR=$S`, `HYAKU_SCRATCH=$S`, OUTDIR `$S/out/<mode>` (sibling of, never inside, the harness scratch `$S/work/<mode>`). `$S` removed before finishing (§9) |

## 1. Carrier acquisition — "from nothing"

```
TMPDIR=$S curl -fsSL -o "$S/carrier/nvim-linux-x86_64.appimage" \
  https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-x86_64.appimage   # exit 0
sha256sum … → b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb   11454968 bytes
```
Equal to `carriers.json` K3 (the file the lane does not hold; the URL is the carrier).

## 2. SquashFS offset derived independently of the harness

ELF64 LE header of the downloaded bytes: `e_shoff=942712`, `e_shentsize=64`, `e_shnum=30` →
`942712 + 64*30 = 944632`; bytes at 944632 are `hsqs` (v4.0, `inode_count=2247`,
`block_size=131072`, `comp=6` xz, `bytes_used=10507255`, payload end 11451887 ≤ file 11454968).
Identical to the harness's own computation in `out/oracle/oracle-run.json` (`squashfs_offset: 944632`).

## 3. Oracle mode — byte-identical to the committed oracle

```
HYAKU_SCRATCH=$S TMPDIR=$S bash tools/round-36/c1-run.sh oracle "$S/carrier/nvim-linux-x86_64.appimage" "$S/out/oracle" "$S/work/oracle"   # exit 0
wc -l oracle.tsv → 2130     sha256 → 9924ec69b8aec05628f43b9e18c4595fec2b993ad446f1117af68696beec1f0e
diff -q "$S/out/oracle/oracle.tsv" corpus/evidence/round-36/c1/K3/oracle.tsv  → no output, exit 0
diff <(jq -S 'del(.carrier,.utc)' out/oracle/oracle-run.json) <(… committed …) → no differences
```
`oracle-run.json` (mine): `squashfs_offset 944632`, `unsquashfs "unsquashfs version 4.7.5
(2026/03/01)"`, `regular_files 2130`, `carrier_sha256 b644d034…f29fb`.

## 4. `after` mode (sasquatch on PATH) — published set equals the committed one

```
HYAKU_SCRATCH=$S TMPDIR=$S bash tools/round-36/c1-run.sh after  … "$S/out/after"  "$S/work/after"    # exit 0, 8.9 s
```
`after-run.json`: `exit 0`, `sasquatch /home/vgpnk/.local/bin/sasquatch`,
`sasquatch_sha256 ad02d27a…c774754`, `sasquatch_version "unsquashfs version 4.5.1 (2022/03/17)"`,
`unblob /home/vgpnk/.local/bin/unblob`, `stderr_head ""`.

| quantity | committed `K3/after.json` | mine (`out/after/after.json`) |
|---|---|---|
| `normalized_result.files` | 2147 | **2147** |
| `(relative_path, sha256)` set | — | **equal**, only-mine 0, only-committed 0 |
| same list, order-sensitive | — | **identical** (`pm == pc` true) |
| row-level oracle suffix+sha match (counter rule) | 2130/2130 | **2130/2130** |
| oracle row size cross-check (`files[].size`) | — | 0 mismatches |
| `published_bytes` | 51122564 | 51122564 (= recomputed sum of `size`) |
| `coverage` / `chunks` / `derivations` / `unpublished_entries` / `diagnostics` | partial / 27 / 2265 / 2 / 0 | **same** |
| `extraction_gaps` (kind, dependencies, handler, relative_path) | 2 × `unpublished-entry`, deps `[]`, handler `null` (`…/.DirIcon`, `…/nvim.png`) | **identical list and order** |
| `subject.digest.sha256` | `b644d034…f29fb` | same |
| `operation` / `provider.id` | `extract_firmware` / `unblob` | same |
| unblob `raw_result.execution.exit_code` | 0 | **0** |
| `engine` | unblob 26.6.4, sha `0ce7b624…bc1d09` | same |
| stored `evidence_id` | `ev_b83bd305…f5419b` | `ev_903b25da…daa6387` (see §6) |
| unblob stdout | — | `Extracted files: 2140`, no ERROR rows |

Non-oracle published files, enumerated (17 = 2147 − 2130): 1 outer carve
`firmware.bin_extract/0-944632.elf64_extract/carved.elf` (sha `dee51346…`), and 8 × {`…_extract/0-N.elf64_extract/carved.elf`, `…_extract/N-(N+1).padding`} for `usr/bin/nvim`, `usr/lib/nvim/parser/{c,lua,markdown,markdown_inline,query,vim,vimdoc}.so`;
each `.padding` is 1 byte, sha `6e340b9c…` (sha256 of `\0`), `reported_sha256` empty (§8 F2). No
duplicate `relative_path`.

## 5. `before` mode (sasquatch filtered off PATH) — published set equals the committed one

```
HYAKU_SCRATCH=$S TMPDIR=$S bash tools/round-36/c1-run.sh before … "$S/out/before" "$S/work/before"   # exit 0, 1.9 s
```
`before-run.json`: `exit 0`, `sasquatch ""`, `sasquatch_sha256 ""`, `sasquatch_version ""`.

| quantity | committed `K3/before.json` | mine (`out/before/before.json`) |
|---|---|---|
| `files` | 2 | **2** — `firmware.bin_extract/0-944632.elf64_extract/carved.elf` `dee51346…`, `firmware.bin_extract/944632-11454968.squashfs_v4_le` `6398c783…` |
| `(relative_path, sha256)` set / order | — | **equal**, 0/0, order-identical |
| oracle suffix+sha hits | 0 | **0/2130** |
| `published_bytes` | 11454968 | 11454968 |
| `coverage` / `chunks` / `derivations` / `unpublished_entries` / `diagnostics` | partial / 3 / 2 / 0 / 1 | **same** |
| gap | `missing-extractor-dependency`, deps `["sasquatch"]`, handler `squashfs_v4_le`, `relative_path null` | **identical** |
| unblob exit / REA exit | 1 / 0 | **1 / 0** |
| unblob stdout | — | `Extracted files: 2`, `Severity.ERROR │ ExtractorDependencyNotFoundReport` |
| stored `evidence_id` | `ev_91e4ab30…e9a44a` | `ev_e75db53b…9e8056c` (see §6) |

## 6. Deep diff of the whole envelopes

Applying a recursive leaf diff, mine vs committed:

- `after`: 15 811 differing leaf paths, classified by last key: `path` 8945, `blob_id` 4530,
  `provider_blob_id` 2265, `provider_id` 27, `id` 27, `evidence_id` 1, `args` 4, `carve_dir` 9,
  `output_directory` 2, `local_path` 1 — i.e. **only** path strings and pid-derived ids.
- Full-envelope equality after removing exactly `{path, provider_id, provider_blob_id, blob_id, id,
  output_directory, carve_dir, evidence_id, local_path, args}`:
  `after → True`, `before → True`.
- `normalized_result` equality after removing `{path, provider_id, provider_blob_id, blob_id,
  output_directory}`: `after → True`, `before → True`.
- Size delta is fully explained: `after.json` mine 4 515 077 B vs committed 4 362 742 B (Δ 152 335);
  the 8945 `path` strings total 1 681 801 chars mine vs 1 529 737 committed (Δ 152 064), leaving
  271 B for the differing id strings. So the byte delta is my longer scratch root, nothing else.
- `limitations` (5), `locations` (1), `evidence_links` (0), `confidence` `observed`, `authority`
  `shipped-artifact`, `predicate_type` `rea.analysis`, `analysis_profile` `null`, `environment`
  `null` — all equal to committed.

**Why my ids differ (evidence-backed, not inferred):** the 6.5.0 rule hashes
`semanticProjection(evidence)` which includes `parameters`, `raw_result` and `normalized_result`
(`…/rea-agents/dist/domain/evidence.js:156-180`), and those carry the absolute output dir, the
carrier path and pid-derived `NNN:k` blob ids. Reproducing a committed id therefore needs the
committer's exact paths, not just their bytes.

**Both committed receipts recompute to their stored id under the 6.5.0 rule** (frozen
`tools/round-27/xpin-attribute.mjs`, `--pkg65` = the 6.5.0 root, `--pkg67` = the host's global
6.7.0 root), and so do all four of my envelopes:

```
committed-after.json   ev_b83bd305…f5419b = ev_b83bd305…f5419b (6.5.0)  ≠ 6.7.0 value   → 6.5.0
committed-before.json  ev_91e4ab30…e9a44a = ev_91e4ab30…e9a44a (6.5.0)  ≠ 6.7.0 value   → 6.5.0
after.json             ev_903b25da…daa6387 = recomputed                  → 6.5.0
before.json            ev_e75db53b…9e8056c = recomputed                  → 6.5.0
after2.json            ev_2ff0cc18…bb1dd4 = recomputed                  → 6.5.0
before2.json           ev_bb5219b6…5ef7a8 = recomputed                  → 6.5.0
```
(`xpin` exit 0. Receipts are wrapped as `{"data": <envelope>}` because the tool reads the record
from `.data`; the REA CLI writes the record at top level.)

## 7. Pin provenance — closing wave-1 harness R-3

R-3 said `*-run.json`'s `rea:"rea-agents@6.5.0"` is an echoed literal and every envelope carries
`environment: null`, so no receipt field proves which package ran. Recorded here:

| probe | observed |
|---|---|
| `readlink -f /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea` | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs` |
| that package's `package.json` | `name rea-agents`, `version 6.5.0`, `bin {rea, rea-agents} → scripts/rea.mjs` |
| other npx cache root holding rea-agents | `/home/vgpnk/.npm/_npx/dea9475797100b20/…` → **6.4.0**; two other `_npx` roots (`4c14ca9d…`, `ba38acec…`) hold no rea-agents |
| `npx -y rea-agents@6.5.0 --version` | `6.5.0`, exit 0 |
| **`execve` of my traced `after` run** | `632076 execve("/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea", ["rea","extract-firmware","--format","json", …]) = 0` |
| **`execve` of my traced `before` run** | `788570 execve("/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/.bin/rea", …) = 0` |
| global install on PATH (`command -v rea`) | `/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/rea-agents/scripts/rea.mjs` = **6.7.0** |
| unblob actually executed (both modes) | `execve("/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob", [… "--version"]) = 0` then the extraction call, exit 0 |

So for these runs the pin held at the **process-execution** level (6.5.0 cache root), not merely in
the receipt string. The traced runs (`out/after2`, `out/before2`) produced the same published sets
(2147 / 2, order-identical) and their own receipts also recompute under 6.5.0, so `strace` did not
perturb the result.

## 8. Advisory findings (reported, not repaired)

- **F1 — a global `rea` 6.7.0 sits on PATH.** `command -v rea` resolves to the fnm global
  install of **6.7.0**, while the harness correctly execs the 6.5.0 npx cache root. Any future
  harness or ad-hoc probe that calls `rea` instead of `npx -y rea-agents@6.5.0` would silently run
  6.7.0 (different `semanticProjection`, hence different `evidence_id` rule) and the receipt would
  still print 6.5.0-looking prose. R-3 is *worked around*, not fixed: neither `<mode>-run.json`
  (`rea` is echoed at `c1-run.sh:85`) nor the envelope (`environment: null`) records the executed
  package path/version.
- **F2 — `reported_sha256` is empty for the 8 padding chunks** (sha `6e340b9c…`, 1 B). All 2139 other
  published files have `reported_sha256 == sha256`. The committed receipt has the same 8 blanks, so
  this is receipt shape, not drift; a consumer that keys on `reported_sha256` alone would drop them.
- **F3 — `$HYAKU_SCRATCH/kaidoku-r36/` is left behind empty** after every run (`c1-run.sh:23`
  `mkdir -p "$root"`; the trap only removes the `c1-run.XXXXXX`/explicit scratch). Same as wave-1
  harness D-3; harmless, reproduced here.
- **F4 — measurement hazard, not a harness defect:** in a *persistent* shell,
  `PATH=$filtered command -v sasquatch` answered from bash's command hash and printed
  `/home/vgpnk/.local/bin/sasquatch` even though the filtered PATH does not contain that directory.
  `env PATH="$filtered" bash -c 'command -v sasquatch'` and `hash -r; PATH=…` both returned rc 1.
  The harness's own guard (`c1-run.sh:72`) runs in a fresh script process, so it is unaffected; any
  seat that repeats this check inline in a long-lived shell can get a false "still on PATH".
  Independent confirmation that the filter really hides the binary in my run: 27 `sasquatch`
  `execve` attempts in the `before` trace, **0 with `= 0`**, all `= -1`; `/home/vgpnk/.local/bin`
  appears in that trace only once, as the harness's own final `jq -n` receipt builder (which runs
  with the unfiltered PATH by design).

## 9. What I did *not* do

- Not executed: `c1-counter.py` (it reads receipts from git revisions, so my scratch receipts are
  not admissible to it), its `--selftest`, any control (`CTL-C1-0/1/2`), K1/K2/K4, PROVINCE/README/
  knowledge binding checks. `carriers_matched`/`met_target` are **not** claimed here. Instead I
  applied the counter's own per-carrier projection rules verbatim
  (`c1-counter.py:119-138` `load_oracle`/`published`/`sasquatch_gap`/`matched`) to my receipts:
  `before_sasquatch_gap True, before_oracle_hits 0, after_sasquatch_gap False, after_oracle_hits
  2130 == oracle_files, subject_ok True, operation_ok True` for K3.
- No fresh `npm`/`npx` download of rea-agents: the 6.5.0 package was resolved from the existing
  cache and its execution proven by `execve` (§7). No tool installed/upgraded; no pacman call.
- No `/fast/scratch` `find`/`du` outside my own scratch; no campaign tool in
  `/home/vgpnk/Projects/shokuknow`; no subagents, background jobs, or `agent://all` messages.
- No writes outside `$S` and this report: `git status --porcelain` shows only pre-existing wave-2
  dispatch files and this new report. Scratch `$S` (34 MB, including the downloaded carrier and all
  extraction trees) removed; verified absent. Nothing under `/tmp` was used.

## 10. Retained evidence (the falsifiable anchors)

- carrier: URL above, `curl` exit 0, `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb`,
  11 454 968 B; offset 944 632 (ELF end), magic `hsqs`, v4.0, inodes 2247, block 131072, comp 6 (xz).
- harness: sha `16907dca…0bf4d4`, = tip blob.
- oracle: 2130 rows, byte-identical to committed, sha `9924ec69…beec1f0e`; `oracle-run.json` equal
  to committed modulo `carrier`/`utc`.
- after: 2147 files, ordered `(relative_path, sha256)` list identical to committed, 2130/2130 oracle
  hits, `published_bytes` 51 122 564, 27 chunks, 2265 derivations, 2 `unpublished-entry` gaps
  (`.DirIcon`, `nvim.png`), unblob 26.6.4 exit 0, sasquatch 4.5.1 sha `ad02d27a…c774754`,
  `evidence_id ev_903b25da…daa6387` (recomputes under 6.5.0).
- before: 2 files (`dee51346…`, `6398c783…`), 0/2130 oracle hits, gap
  `missing-extractor-dependency`/`["sasquatch"]`/`squashfs_v4_le`, 1 diagnostic, unblob exit 1,
  `evidence_id ev_e75db53b…9e8056c` (recomputes under 6.5.0).
- full-envelope equality modulo the 10 run-specific keys: `after True, before True`.
- pin: executed `rea` = `…/ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs` (6.5.0), by
  `execve` in both traced modes; global 6.7.0 present but not used.
