**Verdict: DONE** — the R39-C2 rule block and its knowledge entry are drafted, the table is evaluable
under the stated grammar, and it classifies all sixteen envelopes whose class is already known from
committed evidence (plus three deliberate non-matches) with no row matching more than its own class.

# R39C2TableDraft — SquashFS extract-firmware outcome triage (round 39, wave 1)

## Delivered

| artifact (under `.ufo/waves/round-39/w1/artifacts/R39C2TableDraft/`) | bytes | sha256 |
|---|---|---|
| `skill-craft-block.md` — the exact text to insert into `SKILL.md` `## Queue-drain craft` | 4971 | `2a44eeeac312956b144d80dc4195d534f15389ad28a515bb6a77abdd90457fbc` |
| `knowledge-entry-draft.md` — the exact bytes for `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` | 6691 | `dd9890f25489e152f9f2d2b33f352e7356cc243944688f77bd0299b839be795a` |
| `check-table.py` — draft-only grammar interpreter used for the controls (NOT the frozen `tools/round-39/sqfs-triage.py`) | 6954 | `866d4b00ac0719cc8adfb36950abe984cd329f5699b02339d13a2786ef8f1b86` |
| `dev-probe.json` — dev carriers, damage recipe, digests, envelope features | 2903 | — |
| `rea-dev-clean.envelope.json`, `rea-dev-corrupt.envelope.json` — full CLI envelopes | 16427 / 8964 | — |
| `dev-clean.sqsh`, `dev-corrupt.sqsh` — the dev carriers those envelopes describe | 1542 / 1542 | `9ac4e807…` / `c19b10de…` |
| `dev-corrupt.sasquatch-v4be.stderr` — direct `-be` failure text | 157 | — |

## The rule block

One `- **…**` bullet in the existing style, four sentences, three citations into the knowledge entry
(`…triage.md:23-34`, `:36-53`, `:54-59`), then the marker line `<!-- sqfs-triage-table v1 -->`, then
the nine-column table, then the no-match note. Marker occurs exactly once in the block
(`grep -c 'sqfs-triage-table v1' skill-craft-block.md` → `1`), and `SKILL.md`'s craft section
currently contains zero markdown tables (`awk 'NR>=81 && NR<318 && /^\|/ {c++} END{print c+0}' SKILL.md`
→ `0`), so the new table is the first one after the marker inside that section.

Insertion point: the block goes immediately before `## Config custody for live-probe rounds (SOP)`,
which is `SKILL.md:319` at the base, i.e. after the last bullet of the craft section (currently
`SKILL.md:315`), keeping one blank line before the next heading.

Row order and cells (first match wins):

| # | label | handler | gap kinds | deps | -be | symlink removed | files |
|---|---|---|---|---|---|---|---|
| 1 | avm-marker-be-dropped | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `*` |
| 2 | body-extractor-failure | `squashfs*` | `extractor-failure` | `none` | `yes` | `no` | `*` |
| 3 | dep-missing-be | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `*` |
| 4 | dep-missing-le | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `*` |
| 5 | in-tree-symlink-metadata | `squashfs*` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` |
| 6 | escaping-symlink-removed | `squashfs*` | `none` | `none` | `n/a` | `yes` | `>0` |
| 7 | clean | `squashfs*` | `none` | `none` | `n/a` | `no` | `>0` |

## Evidence actually observed (not inferred)

Committed and probe evidence, feature-extracted by the same code the checker uses:

| envelope | H | G | D | BE | SR | P | class |
|---|---|---|---|---|---|---|---|
| `corpus/evidence/round-38/c1/K1..K4/before.json` (4, bare `data`) | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | n/a | no | 0 | dep-missing-be |
| `corpus/evidence/round-38/c1/K1/after.json` | `squashfs_v4_be` | ∅ | ∅ | n/a | yes | 5 | escaping-symlink-removed |
| `corpus/evidence/round-38/c1/K2/after.json` | `squashfs_v4_be` | `unpublished-entry` | ∅ | n/a | no | 3 | in-tree-symlink-metadata |
| `corpus/evidence/round-38/c1/K3,K4/after.json` | `squashfs_v4_be` | ∅ | ∅ | n/a | no | 4 | clean |
| `corpus/evidence/round-36/c1/K1,K2/before.json` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a | no | 0 | dep-missing-le |
| `corpus/evidence/round-36/c1/K3,K4/before.json` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | n/a | no | **2** | dep-missing-le |
| `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json` | `squashfs_v4_be` | `extractor-failure` | ∅ | **no** | no | 0 | avm-marker-be-dropped |
| `…/R38W2AvmProbe/rea-k1-orig.json` | `squashfs_v4_be` | ∅ | ∅ | n/a | yes | 5 | escaping-symlink-removed |

Two features were not groundable from committed material and were produced here on development
carriers built from my own fresh tree in scratch (never K1–K4 copies, never K5/K6, never a held-out
carrier):

1. `mkdir -p tree/{bin,docs/deep/nested}`; four files (`hello.txt` 17 B, `bin/run.sh` 19 B,
   `docs/readme.md` 9 B, `docs/deep/nested/file.dat` 9000 B);
   `python3 -I -B tools/round-37/gen-squashfs.py tree dev-clean.sqsh --endian be --comp gzip`
   → exit 0, `wrote dev-clean.sqsh 1542 bytes, inodes 9`, sha256 `9ac4e80743e6ec66534b874d7a81c9d3b07a2bbc8dca6653e83c665ea23caefc`;
   superblock: magic `sqsh`, `bytes_used` 1542, `mkfs_time` 1700000000, AVM marker false.
2. `dev-corrupt.sqsh`: bytes 942–1342 overwritten with `0xff` (superblock and padding untouched),
   sha256 `c19b10ded866e211d7c412492c0c44af7caf502a9734d6abf99ab76ce2d47dca`.
3. `sasquatch-v4be -be -f -d … dev-clean.sqsh` → exit 0, 4 files;
   `sasquatch-v4be -be -f -d … dev-corrupt.sqsh` → exit 1, 0 files,
   `get_metadata: failed to read block` / `FATAL ERROR: read_inode: failed to read inode 1039:280`.
4. `cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware
   --format json --full-output dev-clean.sqsh rea-dev-clean` → exit 0, 16427 B envelope; the same for
   `dev-corrupt.sqsh` → exit 0, 8964 B. `$HOME/.local/bin` was **not** stripped (after-arm shape:
   `which sasquatch-v4be` → `/home/vgpnk/.local/bin/sasquatch-v4be`, `-version` reports
   `unsquashfs version 4.5.1`; `unblob --version` → `26.6.4`).

Outcomes: `dev-clean` → `H={squashfs_v4_be}`, `G=∅`, `D=∅`, `BE=n/a`, `SR=no`, `P=4`;
`dev-corrupt` → `H={squashfs_v4_be}`, `G={extractor-failure}`, `D=∅`, `BE=yes`,
`SR=no`, `P=0`, diagnostics `ExtractCommandFailedReport` with argv
`sasquatch-v4be -be -no-exit-code -f -d …` — i.e. the body-damage class really does carry `-be`
while the AVM probe's argv (`sasquatch-v4be -no-exit-code -f -d …`, round 38) does not. That is the
whole separation the table encodes. Both dev envelope subjects digest to their carrier
(`subject.digest.sha256` = the carrier sha256 above; note the digest sits at `subject.digest.sha256`,
not `subject.sha256`).

## Contract conformance and controls

`check-table.py` implements the brief's grammar (marker → first table; exact header; nine cells;
backticks stripped from condition cells; `*`, `none`, `a+b`, `yes/no/n/a`, `0/>0/*`; malformed → exit 2;
bare `data` **and** `{ok,data,meta}` accepted) and was exercised in three ways:

1. Sixteen known envelopes → `checker_exit=0`, every one classified to its expected label
   (8 round-38 receipts, 4 round-36 LE before-receipts, 2 AVM-probe envelopes, 2 dev envelopes).
2. Grammar refusal: a copy with the `clean` row's `>0` replaced by `>1` →
   `exit 2: row 9 published files malformed: '>1'`, process exit `2` — never a silent non-match.
3. Not a catch-all: per-row match counts over the sixteen envelopes are
   `avm 1/16, body 1/16, dep-be 4/16, dep-le 4/16, in-tree 1/16, escaping 2/16, clean 3/16`.
   Three synthetic non-matches also resolve to `unclassified`: no squashfs chunk (`handler=elf64`),
   `extractor-failure` with no recorded command, and a `depth-limited` gap.

## Knowledge entry

Provenance header (as in the round-38 entry) cites S112 (unblob 26.6.4 `SquashFSExtractor` lines
24-70), a **new** S118 (unblob 26.6.4 `extractor.py:34-39,42-90` and `report.py:133-139` — the
in-tree-kept / escaping-removed symlink rule), and a **new** S119 (rea-agents 6.5.0
`dist/domain/firmware/firmwareAnalysis.js:78-96` gap-`kind` enum and
`dist/firmware/FirmwarePublication.js:12-24,208-320` gap construction and the `unpublished-entry`
mapping), plus `verified-at: 2026-10-26` and a `recheck: 180d` command pair. Locally read copies:
`unblob/handlers/filesystem/squashfs.py` sha256 `2d7b901b…` (identical to S108/S112's pinned blob),
`extractor.py` `1bb49811…`, `report.py` `2329783f…`, `firmwareAnalysis.js` `2cbc1cc4…`,
`FirmwarePublication.js` `bb4f3246…`. Body: the sixteen-envelope feature matrix (lines 23-34), the
`-be`-not-file-count argument (36-53), the symlink rule (54-59), and a Status block that bounds the
claim. The citations in the SKILL bullet point at exactly those spans, so the entry must land
**verbatim**.

## Findings for the L1 (integration decisions I did not take)

1. **SOURCES rows.** S118/S119 do not exist yet; the highest used number is S117
   (`corpus/SOURCES.md:123`). Land those two rows with the entry, or renumber consistently.
   Neither is needed by the C1 predicate, so no `used-by` requirement applies.
2. **One ordering decision to confirm.** If one image holds *both* an escaping and an in-tree
   symlink, the envelope is `G={unpublished-entry}`, `SR=yes`, so it matches row 5
   (`in-tree-symlink-metadata`, `SR` wildcard) and never row 6 (whose `gap kinds` is `none`).
   That is the only place my order changes the answer. If the frozen generator can emit such a
   carrier and labels it `escaping-symlink-removed`, row 6 must move above row 5 with
   `gap kinds = *` — a freeze-time decision, not mine.
3. **`published files = *` on rows 1-4 is deliberate.** A container prefix publishes files beside a
   failed or unextracted squashfs chunk — measured, not assumed: round-36 `K3/K4/before` publish
   `P=2` while the dependency gap stands. Narrowing those cells to `0` would break on any
   AppImage-shaped held-out carrier, and it buys nothing: rows 1-4 are already separated by
   `gap kinds` + `dependencies` (+ `-be` for 1 vs 2).
4. **`-be = n/a` on rows 3-7 assumes success is silent.** Across 14 successful or
   dependency-blocked envelopes no sasquatch command appears in `diagnostics`; the only
   command-carrying report observed is `ExtractCommandFailedReport`. If REA ever records a
   successful command, those five rows need `*`.
5. **`extractor-failure` with no recorded command is `unclassified` by design** — AVM-versus-body is
   undecidable without the argv, and guessing would be the catch-all the kill rule forbids.
6. **`no-squashfs-chunk` deferred**, as the claim allows: today it falls to `unclassified`; if recon
   shows it distinct it enters above `clean` (the no-match note says so).
7. The AVM row's remedy is only half-measured: the round-38 probe shows `sasquatch-v4be -be` succeeds
   on the AVM-patched images (k1-avm 5 files, k4-avm 4 files, exit 0), so the *flag* is the fix;
   the *wrapper* mechanism (a `PATH` executable named `sasquatch-v4be` that appends `-be`) is
   [INFERENCE] — I did not build or test one. `npx rea-agents@6.5.0 extract-firmware --help` confirms
   there is no unblob-flag passthrough (only `--offset/--length/--max-depth/--max-output-*`).

## Not claimed / out of scope

No held-out carrier was built or run; no REA run touched K1–K4 copies, K5/K6, or any C1 carrier.
Nothing is claimed about AVM-BE *bodies* (only the marker's argv effect), vendor-mangled images, or
extracted programs. The dev carriers are development fixtures; the frozen held-out set is the L1's.
I did not write `tools/round-39/*`, the interpreter, the counter, or any lane file: `SKILL.md`,
`PROVINCE.md`, `SOURCES.md`, `SCORECARD.md`, `LOG.md` and `corpus/knowledge/` are untouched.

## Tooling, hygiene

No installs or upgrades (nothing was missing: `unblob` 26.6.4, `sasquatch-v4be` 4.5.1 and the cached
`rea-agents@6.5.0` at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6` were used as found); no pacman
transaction; no VCS mutation; no fixture repos. Writes: this report plus the nine files listed above,
all under `.ufo/waves/round-39/w1/`. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39C2TableDraft` was
removed at the end; the dev envelopes' internal `parameters.path` / `subject.local_path` therefore
name dead scratch paths, but both carriers were copied beside their envelopes and match
`subject.digest.sha256`, and `dev-probe.json` records the tree, generator command, damage offsets and
tool versions needed to rebuild them byte-identically.
