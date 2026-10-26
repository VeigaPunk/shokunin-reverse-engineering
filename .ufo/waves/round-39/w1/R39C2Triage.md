**DONE** — `sqfs-triage.py` implemented to the L1 grammar, 35/35 selftest, and every draft C2 class (eight, `no-squashfs-chunk` included) separated on measured features; two **draft-claim defects** found that must be fixed before the freeze (§6): the C1/C2 symlink rule as worded is false for absolute targets, and `body-extractor-failure` is separable from `avm-marker-be-dropped` only while it stays big-endian-scoped.

# R39C2Triage — R39-C2 triage interpreter, table contract and class separability

Seat `R39C2Triage`, round 39 wave 1 (pre-freeze). Base `a2f64e1d` (lane `main`). Leaf seat: no
subagents, no background jobs, no VCS mutation, no writes outside this seat's report and artifacts,
no REA on K5/K6, no held-out carrier built or run.

Report: `.ufo/waves/round-39/w1/R39C2Triage.md`
Artifacts: `.ufo/waves/round-39/w1/artifacts/R39C2Triage/`

Digests of the two files the freeze pins (sha256): interpreter
`ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2` (1134 lines), table block
`0f14537c076f50cb4959edcb728d501bc3bfd9e0c40533c19684df0adfc84021`, selftest output
`235d201f191a94ee4ccfe35dc04a7656b6f8864e1b7d642081b88aa16da9e9eb`.

## 1. What was delivered

| artifact | role |
|---|---|
| `sqfs-triage.py` (47 KB, stdlib only) | the frozen-candidate interpreter: `--skill`, `--json`, `--table-only`, `--selftest`, `--print-table`; exit 0 ok / 2 table or envelope unevaluable / 1 only for `--selftest` failure |
| `skill-triage-block.md` | the 8-row triage table **plus its marker line**, byte-identical to the interpreter's `--print-table` output; the L1 pastes this into the `## Queue-drain craft` section |
| `selftest.out` | `SELFTEST cases=35 pass=35 fail=0`, exit 0 |
| `mutation-matrix.txt` | ten semantic mutants of the interpreter, each losing at least one case |
| `features-committed.tsv` | the six committed development envelopes, features + label + matched rule |
| `features-dev.tsv` | eleven scratch development envelopes (eight class carriers + three symlink-boundary probes) |
| `dev-build.sh`, `dev-carriers/`, `dev-envelopes/` | the exact carrier recipes, the ten carriers, the eleven envelopes and their `evidence_id`s |

Integration (the L1 owns both writes):

1. `tools/round-39/sqfs-triage.py` ← `artifacts/R39C2Triage/sqfs-triage.py` (bytes unchanged).
2. Insert `artifacts/R39C2Triage/skill-triage-block.md` inside `SKILL.md` `## Queue-drain craft`
   (line 81 to line 318 at the base; any position in that section works, the marker makes it
   addressable). Verify with
   `python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --table-only` → exit 0, `rules: 8`.

The classification path reads only the SKILL.md craft-section table and the envelope. The absolute
lane paths in `SELFTEST_ENVELOPES`/`SELFTEST_SKILL` are read by `--selftest` only, never by a scoring
run. `TABLE_BLOCK` is printed by `--print-table` and used by the selftest to build table variants; it
is **never** a fallback — an absent or malformed table exits 2. If the L1 prefers a table-free
interpreter, `--print-table`/`TABLE_BLOCK` can be deleted, but the selftest then needs the block from
another source; I recommend keeping it and disclosing it as above.

## 2. Grammar as implemented (the L1's contract, verbatim)

Marker `<!-- sqfs-triage-table v1 -->`, first markdown table after it inside the craft section
(heading line matching `## Queue-drain craft…` up to the next `## ` line). Header cells compared
after stripping spaces/backticks and case-folding against
`label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source`.
Rules top to bottom, first full match wins, no match → `unclassified`. Unevaluable (exit 2), never a
silent non-match: no craft heading, no marker in the section, no table after the marker, wrong header,
bad separator, wrong cell count, empty label, `cause -> action` without `->`, empty source, malformed
condition cell, an empty rule set, an unreadable/unparseable envelope, an invocation without
`--skill`.

Cell semantics: `handler` = `*` | `none` (H empty) | fnmatch pattern matching ≥1 member of H;
`gap kinds`/`dependencies` = `*` | `none` | exact set `a+b` (single name = that singleton, order and
repetition erased); `-be in child argv`/`symlink removed` = `yes` | `no` | `n/a` | `*` (`n/a`
accepted in both columns — the contract sentence groups them); `published files` = `0` | `>0` | `*`.
Features: H from `normalized_result.chunks[].handler` starting with `squashfs`; G/D from
`normalized_result.extraction_gaps[]`; BE from every recorded command that names a `sasquatch*`
basename (`normalized_result.diagnostics[].report`, `data.diagnostics[].report`, and any `command`
member under `raw_result`; string commands shlex-split, argv lists used as given; only a standalone
`-be` token counts); SR from `normalized_result.diagnostics[].report.__typename__` or that typename
anywhere under `raw_result`; P = `len(normalized_result.files)`. Both a bare `data` object and a full
`{ok,data,meta}` envelope are accepted and give identical features.

## 3. The table (`--print-table`)

| # | label | handler | gap kinds | dependencies | -be | symlink removed | files |
|---|---|---|---|---|---|---|---|
| 1 | `no-squashfs-chunk` | `none` | `*` | `*` | `n/a` | `*` | `*` |
| 2 | `dep-missing-be` | `squashfs_v4_be` | `missing-extractor-dependency` | `sasquatch-v4be` | `n/a` | `no` | `0` |
| 3 | `dep-missing-le` | `squashfs_v4_le` | `missing-extractor-dependency` | `sasquatch` | `n/a` | `no` | `0` |
| 4 | `avm-marker-be-dropped` | `squashfs_v4_be` | `extractor-failure` | `none` | `no` | `no` | `0` |
| 5 | `body-extractor-failure` | `squashfs_v4_be` | `extractor-failure` | `none` | `yes` | `no` | `0` |
| 6 | `escaping-symlink-removed` | `squashfs_v4_be` | `*` | `*` | `n/a` | `yes` | `>0` |
| 7 | `in-tree-symlink-metadata` | `squashfs_v4_be` | `unpublished-entry` | `none` | `n/a` | `no` | `>0` |
| 8 | `clean` | `squashfs_v4_be` | `none` | `none` | `n/a` | `no` | `>0` |

No catch-all row: the kill rule registers a catch-all table, a gap-count-only table, a gap-kind-only
table and a transcription of the round-36 table as shortcuts. This table is none of those — rows 4/5
are separated only by the `-be` column, rows 6/7/8 only by `symlink removed` and the gap set, and
rows 2/3 only by handler + dependency name. Every row carries its own cause→action and a source
citing `unblob 26.6.4` / `rea-agents 6.5.0` line numbers or a named carrier.

## 4. Measured evidence

### 4.1 The six committed development envelopes

`features-committed.tsv` (canonical table, exit 0):

| envelope | H | G | D | BE | SR | P | label |
|---|---|---|---|---|---|---|---|
| `round-38/c1/K1/after.json` | `squashfs_v4_be` | — | — | `n/a` | `yes` | 5 | `escaping-symlink-removed` |
| `round-38/c1/K2/after.json` | `squashfs_v4_be` | `unpublished-entry` | — | `n/a` | `no` | 3 | `in-tree-symlink-metadata` |
| `round-38/c1/K3/after.json` | `squashfs_v4_be` | — | — | `n/a` | `no` | 4 | `clean` |
| `round-38/c1/K4/after.json` | `squashfs_v4_be` | — | — | `n/a` | `no` | 4 | `clean` |
| `R38W2AvmProbe/rea-k1-avm.json` | `squashfs_v4_be` | `extractor-failure` | — | `no` | `no` | 0 | `avm-marker-be-dropped` |
| `R38W2AvmProbe/rea-k1-orig.json` | `squashfs_v4_be` | — | — | `n/a` | `yes` | 5 | `escaping-symlink-removed` |

`K1/after.json` and `rea-k1-orig.json` share subject `1cfb6c33f915…` and classify identically, which
is the intended equivaluation: the committed receipt and the probe envelope are two runs of one
carrier.

### 4.2 Eleven scratch development envelopes (all exit 0 from REA)

`features-dev.tsv`, each carrier rebuilt byte-identically by `dev-build.sh` (sha256 of the copy ==
sha256 rebuilt in a fresh directory, all ten carriers). Command per run:

```
cd "$S" && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
  extract-firmware --format json --full-output <carrier> <fresh outdir>     # exit 0, 11/11
```
`dep-missing-*` runs additionally `PATH=<PATH minus $HOME/.local/bin>` (verified
`command -v sasquatch` → absent).

| carrier | class | H | G | D | BE | SR | P | label |
|---|---|---|---|---|---|---|---|---|
| `C-clean-be.sqsh` | clean | `squashfs_v4_be` | — | — | `n/a` | `no` | 4 | `clean` |
| `C-intree-be.sqsh` | in-tree symlink (`var/lib/run-link -> ../../bin/run`) | `squashfs_v4_be` | `unpublished-entry` | — | `n/a` | `no` | 5 | `in-tree-symlink-metadata` |
| `C-escape-be.sqsh` | escaping symlink (`escape-link -> ../../outside/secret`) | `squashfs_v4_be` | — | — | `n/a` | `yes` | 4 | `escaping-symlink-removed` |
| `C-avm-be.sqsh` | AVM marker (`mkfs_time == bytes_used`) | `squashfs_v4_be` | `extractor-failure` | — | `no` | `no` | 0 | `avm-marker-be-dropped` |
| `C-bodyfail-be.sqsh` | inode-table head XOR 0xff | `squashfs_v4_be` | `extractor-failure` | — | **`yes`** | `no` | 0 | `body-extractor-failure` |
| `C-clean-be` + PATH stripped | BE dep missing | `squashfs_v4_be` | `missing-extractor-dependency` | **`sasquatch-v4be`** | `n/a` | `no` | 0 | `dep-missing-be` |
| `C-clean-le` + PATH stripped | LE dep missing | `squashfs_v4_le` | `missing-extractor-dependency` | **`sasquatch`** | `n/a` | `no` | 0 | `dep-missing-le` |
| `C-nochunk.bin` | ASCII prose | — | — | — | `n/a` | `no` | 0 | `no-squashfs-chunk` |
| `C-abs-escape-be.sqsh` (`-> /etc/passwd`) | boundary probe | `squashfs_v4_be` | `unpublished-entry` | — | `n/a` | `no` | 4 | `in-tree-symlink-metadata` |
| `C-abs-intree-be.sqsh` (`-> /hello.txt`) | boundary probe | `squashfs_v4_be` | `unpublished-entry` | — | `n/a` | `no` | 4 | `in-tree-symlink-metadata` |
| `C-climb-be.sqsh` (`a/b/climb-link -> ../../../hello.txt`) | boundary probe | `squashfs_v4_be` | — | — | `n/a` | `yes` | 4 | `escaping-symlink-removed` |

### 4.3 Selftest and its sensitivity

`python3 -I -B sqfs-triage.py --selftest` → exit 0, `SELFTEST cases=35 pass=35 fail=0`
(`selftest.out`). Cases: green parse; first-match order; `*`; `none` (handler, gap set, dep set);
`none` handler must **reject** an envelope that has a squashfs chunk; exact-set hit, miss, and
superset (two-kind envelope must not match a singleton row; two-dep envelope must not match a
one-dep row); fnmatch handler; malformed header → 2; malformed cell → 2; malformed set cell → 2;
table outside the craft section → 2; marker absent → 2; marker without a table → 2; bare `data` vs
full envelope identical features; BE `yes`/`no`/`n/a`; BE from an argv list; `--be=1`/`-be-check`
tokens are not `-be`; SR from `normalized_result.diagnostics`; SR from `raw_result`; P `0`/`>0`;
`unclassified`; unreadable/missing/invalid envelope → 2; `--table-only`; a real-SKILL.md copy with
the block inserted at the craft heading; first of two tables wins; `--print-table` round-trip; `--json`
carries the matched rule's raw cells (`row`), its 1-based index and the nine columns.

Sensitivity proven by mutation (`mutation-matrix.txt`, ten mutants, all killed):

| mutant | cases lost |
|---|---|
| BE feature always `n/a` | 6 |
| last match wins instead of first | 1 |
| exact-set becomes superset | 2 |
| `none` handler ignored | 10 |
| `-be` substring instead of standalone token | 1 |
| SR diagnostics-only (no `raw_result` scan) | 1 |
| `0`/`>0` inverted | 20 |
| header not validated | 1 |
| dependencies ignored | 1 |
| `--json` `row` omitted | 1 |

### 4.4 Base state

`python3 -I -B sqfs-triage.py --skill SKILL.md <K1/after.json>` at `a2f64e1d` →
`sqfs-triage: marker '<!-- sqfs-triage-table v1 -->' absent from the craft section`, exit 2. The
`--table-only` form exits 2 the same way. This is the command that shows the surface unmoved.

## 5. Recon results that decide the held-out generator

1. **The AVM marker drops `-be`, and that is the only separator of rows 4 and 5.**
   `unblob 26.6.4 handlers/filesystem/squashfs.py:40-56`: for `Endian.BIG, 4` the executable is
   `sasquatch-v4be` and `commands_args.append("-be")` happens only `if not is_avm` where
   `is_avm = header.bytes_used == header.mkfs_time`. Measured commands: AVM carrier
   `sasquatch-v4be -no-exit-code -f -d …` (no `-be`), body-damaged carrier
   `sasquatch-v4be -be -no-exit-code -f -d …`. Both record `extractor-failure`, no dependency, P=0,
   SR=no — without the `-be` column they are indistinguishable. Same in the committed
   `rea-k1-avm.json`. **The `-be` column earns its place.**
2. **The dependency name splits by endianness.** BE + stripped PATH →
   `dependencies: ["sasquatch-v4be"]`; LE + stripped PATH → `dependencies: ["sasquatch"]`
   (`squashfs.py:25-26`, `:69`). A table that keys the dep rows on `sasquatch` alone collapses the
   BE/LE distinction.
3. **Absolute symlink targets never escape.** `extractor.py:66-79`: an absolute target is rewritten
   to `Path(target.as_posix().lstrip("/"))` — a *relative* path — before `is_safe_path`, so it is
   always inside the chunk extraction directory and is **kept** as metadata. Measured:
   `-> /etc/passwd` and `-> /hello.txt` both produce `unpublished-entry`, SR=no, and no removal.
4. **The boundary is the chunk extraction directory, not the filesystem root.**
   `a/b/climb-link -> ../../../hello.txt` resolves above `firmware.bin_extract/` and is **removed**
   (`MaliciousSymlinkRemoved`, no gap). So "escapes" means "a *relative* target that resolves above
   the image root as extracted".
5. **`link_target` in `unpublished_entries` is the rewritten target, not the image's raw target**
   (`/etc/passwd` → `etc/passwd`; `/hello.txt` → `hello.txt`). An oracle that compares raw target
   text will disagree with the envelope.
6. **An empty symlink target is removed with no report and no gap** (`extractor.py:68-70`), so it is
   invisible to the table; **a symlink loop is reported and removed** (`extractor.py:57-65`), so it
   looks exactly like class 6. Neither may appear in the frozen class list.
7. `missing-extractor-dependency` records no sasquatch command at all (only
   `ExtractorDependencyNotFoundReport`), which is why rows 2/3 and 6/7/8 can honestly say `n/a` in
   the `-be` column: only a failing stage records a command.
8. `no-squashfs-chunk` is distinct on handler `none` (measured: 0 chunks, 0 gaps, P=0,
   coverage `complete`), so the draft's optional ninth class is real and is row 1.

## 6. Defects in the draft claim — fix before the freeze

1. **Symlink rule wording (R39-C2 classes 2/3; R39-C1 symlink rule).** The claims say "a symlink
   whose target resolves inside the extraction root is kept … a symlink that escapes is removed by
   unblob". Measured, that is only true for **relative** targets: an absolute target is neutered by
   `lstrip("/")` and kept, and the removal boundary is the chunk extraction directory. An oracle that
   classifies `/etc/passwd → escaping` will disagree with the envelope (gap present, SR=no). Either
   the wording is corrected to "relative target resolving above the image root", or the frozen
   carriers must be generated with relative targets only. K5/K6 are being built **now** — I have
   messaged both carrier seats with this, and it must be settled in the freeze text. Status after
   that message [peer-reported, not re-measured by this seat]: `R39C1CarrierK5` confirms zero absolute
   targets and exactly one relative escaping link (`usr/share/demo/escape -> ../../../../etc/shadow`,
   removed, one `MaliciousSymlinkRemoved`, no gap), ledger `in_tree=2, escaping=1, expected gaps=2`;
   `R39C1CarrierK6` confirms zero absolute targets, one in-tree relative link
   (`a/b/link-in -> ../../etc/config.ini`) and two relative escaping links, carrier
   `df85c10b…df344f61`. Neither needs a rebuild. Both keep `symlinks.tsv` raw-target text: for clean
   relative in-tree links the rewrite is the identity, so raw and rewritten agree there — the
   divergence is confined to absolute targets, which neither carrier has.
2. **`body-extractor-failure` must stay big-endian-scoped.** Row 5 keys `-be == yes` on
   `squashfs_v4_be`. An LE body failure records `-le` (so `-be == no`) and would fall to
   `unclassified`. Either the frozen class list pins `body-extractor-failure` as BE-only, or a second
   row + label (`body-extractor-failure-le`, handler `squashfs_v4_le`) is added before the freeze. My
   recommendation: pin BE-only — the AVM class is BE anyway, and the claim's own examples (K1–K4,
   round-38 probe) are BE.
3. **The held-out generator must not use absolute escaping targets, symlink loops, or empty
   targets**; and the class list must contain exactly the eight labels in §3 (the interpreter prints
   `unclassified` for anything else, by design).

## 7. Limits

* Cell text is split on `|`; a literal pipe inside a cell is unsupported (documented in the
  interpreter docstring and enforced by a cell-count error).
* Handler patterns match case-sensitively (`fnmatchcase`); `dependencies` compares as a set, so
  order and repetition in an envelope are erased.
* Row 6 uses `*` for gap kinds and dependencies deliberately: an escaping target may coexist with an
  in-tree link (one `unpublished-entry` gap) and the class is still "escaping symlink removed"; the
  `symlink removed` and published-files columns carry that row.
* Rows 6/7/8 assert `-be == n/a`. This holds because only a failing stage records a command; if a
  future REA version records successful commands, those three rows must widen to `*`.
* `BE` scans `raw_result` for any dict with a `command` member; the unblob path
  (`…/bin/unblob`) does not name a sasquatch basename, so it is not mistaken for an extractor
  command. [INFERENCE] A hypothetical report whose *argument* is a path ending in `sasquatch` would
  be counted; not observed in any envelope here.
* The interpreter labels an envelope, never a carrier's usability; an envelope can be `clean` while
  the image is wrong for other reasons.
* No `<50 MB` files were left in `/tmp`; the scratch root `/fast/scratch/hyaku/kaidoku-r39/R39C2Triage`
  was used for all REA output and removed at exit. All cited envelopes and carriers are copied into
  the artifacts directory.
* No tool was installed or upgraded in this wave (unblob 26.6.4, rea-agents 6.5.0, sasquatch 4.5.1
  and sasquatch-v4be 4.5.1 were used as found); no pacman transaction; no VCS mutation; **no REA run
  on K5/K6 and no held-out carrier built or run**.

## 8. Checks the L1 should run after integration

1. `python3 -I -B tools/round-39/sqfs-triage.py --selftest` → `cases=35 pass=35 fail=0`, exit 0.
2. `python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --table-only` → exit 0, `rules: 8`,
   and the eight labels above.
3. `python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md` over the six committed envelopes
   → the labels in §4.1 (`--json` prints the features that produced them).
4. `git diff --stat` on `SKILL.md`: only the inserted block (marker + 10 lines) inside the craft
   section, no other byte of that section changed.
