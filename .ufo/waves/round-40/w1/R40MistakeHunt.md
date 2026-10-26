# R40MistakeHunt — mistakes mined for the round-40 lesson `## Mistakes`

**Verdict: DEFECTS FOUND** — twelve round-39 mistake classes are absent from the round-39 lesson's
`## Mistakes` table, and each now has a gate that is red on the round-39 bytes and green on a
fixture or on the repaired revision (`artifacts/R40MistakeHunt/runs.txt`: 28 runs, 14 exit 1,
13 exit 0, 1 exit 2). Three of them
(MH-4, MH-5, MH-6) are already load-bearing for the round-40 draft: the depth label R40-C2
claims, the `--endian avm` writer R40-C1's L1/L2 carriers need, and the AVM row R40-C1's kill
control would be read through. Six forward findings follow (§4), one of which blocks a carrier the
draft names.

Seat `R40MistakeHunt`, leaf. Lane `fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f`, worktree unchanged
outside `.ufo/waves/round-40/w1/` (`git status --porcelain` → `?? .ufo/waves/round-40/`,
`?? plans/round-40-claims.md`, both pre-existing). No REA call, no unblob call, no carrier built
or touched. No tool installed, upgraded, moved or removed.

## 1. Sweep: what was read, and what is already an `M39-*` row

Read in full: `corpus/lessons/round-39.md`; `corpus/lessons/round-39-verifier-spotcheck.md`
(§1 conformance defects, §5 R39-CL1..CL6); `/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/
kaidoku.md`; `w2/R39W2C2AxisFit.md`; `w2/R39W2Sentinel.md`. Read for verdict and findings:
`R39W2C2TableReview`, `R39W2C2Shortcut`, `R39W2C2Mutants`, `R39W2TriageMutants`,
`R39W2C1AxisFit` (D1), `R39W2Separability` (D2), `R39W2SrcReopen`, `R39W2C1Fabricate`.
Also read: `plans/round-39-claims.md` and
`plans/round-40-claims.md`; `SKILL.md` blocks 18 and the instrument registry; `corpus/QUALITY.md`
rows 18, 73, 75, 80; `SCORECARD.md` recipe A; `corpus/knowledge/2026-10-26-r39-sqfs-outcome-
triage.md`; `tools/round-39/{gen-squashfs.py,sqfs-triage.py,c2-counter.py,heldout-gen.py}`;
`.ufo/waves/round-39/controls/` and `l1/scores/`.

The round-39 lesson carries ten rows. What it does not carry:

```
$ grep -c '^| M39-' corpus/lessons/round-39.md
10
$ for k in formatfix 'exit code' 'cross-domain' 'block-length' 'block length' 'endian avm' \
        saturated headroom; do printf '%-14s %s\n' "$k" "$(grep -c -F "$k" corpus/lessons/round-39.md)"; done
formatfix      0
exit code      0
cross-domain   0
block-length   0
block length   0
endian avm     0
saturated      0
headroom       0
$ grep -c 'R39-CL' corpus/lessons/round-39.md
0
$ grep -c 'R39-CL' corpus/lessons/round-39-verifier-spotcheck.md
6
```

So the six routed defects live in the spot-check only, and the wave-2 depth finding (QUALITY 75)
is not an `M39-*` row at all. `M39-4` is adjacent to MH-1 but distinct: it is a control receipt
re-scored in place; MH-1 is the control *input* arriving after the freeze. `M39-7` is adjacent to
MH-5 but distinct: it is the writer's UTF-8/xz encoding; MH-5 is the writer's `avm` mode name.

## 2. Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| MH-1 | **a kill control's input is not in the freeze** — and the freeze's own copy cannot be evaluated: the registered C2 controls CTL-C2-5/6 live in `w1/artifacts/R39C2Shortcuts` and exit 2 `cause -> action cell has no "->" separator`; the `.formatfix` tables that produced the recorded 8/20 and 12/20 first land 3m36s later (QUALITY 80) | freeze `8fcda41c` (14:12:51) has **0** files under `.ufo/waves/round-39/controls`; `git log --diff-filter=A -- .ufo/waves/round-39/controls/tables/*formatfix*` → `72359309` (14:16:27); `git cat-file -e 8fcda41c:<formatfix>` → absent. Frozen CTL-C2-5 table exit 2 (`runs.txt` MH-1 second run) | R39-CL4 (spot-check §5), `w2/R39W2C2AxisFit.md` §4 C3 | `control-freeze-gate.py`: red twice on round-39 (2 `ABSENT_AT_FREEZE`; 4 `FORMAT_INVALID` incl. CTL-C2-5/6), red on a malformed frozen table in a fixture, green (exit 0) on a fixture whose table is committed in the freeze commit |
| MH-2 | **a score receipt does not record its own exit code, and a wave ledger carries no seat status** — the report's "exit 0" and "dead seats: 0" rest on prose (QUALITY 18; the receipts retain argv but not exit) | `c1-at-6fdaf4f1.json` / `c1-at-2b0b6a29.json` have no `exit*`/`rc` key at all; `c2-*` record the *interpreter's* `interpreter_exit`, never the counter's; `r39-w{1,2}-results.json` 43/43 and 39/39 `status: null` | R39-CL6 (spot-check §5 and §1) | `receipt-fields-gate.py`: red 7 findings on round-39 (5 receipts, 2 ledgers/82 seats), green on the same files with `exit_code` and `status` added |
| MH-3 | **the report omits a PROTOCOL minimum-content line** — "cross-domain evidence encountered" is absent; the only near-match is SHONEN box 4 "No cross-domain bleed", which asserts the absence of an event, not a disposition | `PROTOCOL.md:155`; `grep -i cross-domain` on the report → only `:146` SHONEN box 4 | spot-check §1 conformance defects | `report-content-gate.py`: red (1 missing), green on the report plus one line |
| MH-4 | **an owned-axis instrument with zero headroom certifies a non-measurement** — `depth_score = 10*resolved/rules`, every block already resolves, so any added block scores 10.00; round-39's "depth improved 17→18" is a block count, and the round-40 base is already 18/18 at 10.00, so R40-C2's block 19 inherits it | `SCORECARD.md:92-124`; measured: `a2f64e1d` 17/17 = 10.00 → `52b0eb29` 18/18 = 10.00; `fa6a8a3f` 18/18 = 10.00. QUALITY 75 (`corpus/QUALITY.md:130`) says the depth surface *is* "the craft section and its counting recipe" | `w2/R39W2C2AxisFit.md` §1 (QUALITY 75 finding); round-40 base measured by this seat | `depth-delta-gate.py`: red on round-39 and on the round-40 base (no headroom), green on a two-commit fixture scoring 5.0 → 10.0 (delta 5.0) |
| MH-5 | **a fixture mode named for a layout it does not emit** — `--endian avm` writes a standard-BE body with `mkfs_time := bytes_used`; the mode name, the docstring "LE / BE / AVM-BE" and `MAGIC['avm']` all advertise the AVM layout | `tools/round-39/gen-squashfs.py:2,20,185`, `MetaWriter.meta_header` `:49-50` packs `>` for `avm`; measured `hdr=80a8` → LE 10368 (implausible) / BE 168 (plausible) = standard-BE block lengths. Critic measured byte-identity with `--endian be` + marker patch (`w1/R39AssimAvmCritic.md:108`) | `w1/R39AssimAvmCritic.md` "Round-39 consequence (C1)" (pre-freeze) | `avm-mode-gate.py`: red on the round-39 writer; green on `gen-squashfs-avm-mode-fixed.py` (block header `a880`, LE length 168). The fixed writer's images extract 2/2 files under `sasquatch-v4be` noflag and 0/2 with `-be`, gzip **and** xz (`avm-measurements.txt`) |
| MH-6 | **a rule stated from the synthetic arm of a mechanism, against a wave-1 measurement of the other arm** — v1's AVM rows key on `mkfs_time == bytes_used`; the table has no block-length field, its `avm-marker-be-dropped` action prescribes a global `sasquatch-v4be` PATH wrapper that appends `-be`, and its `body-extractor-failure` row calls the `-be` failure "damaged" and forbids the remedy that works | `SKILL.md:324` prose, `:339` (row 4), `:340` (row 5). Measured (this seat, genuine AVM body sha256 `c7f74691…d32d32`): noflag 4 files / `-be` 0 files, **both** with the marker and with the timestamp normalised to 1700000000. The marker-stripped shape is exactly the frozen `body-extractor-failure` tuple (H15: `H=be, G=extractor-failure, BE=yes, P=0` → "image body or header is damaged") | `w1/R39AssimAvmCritic.md` feed-forward §2 ("key the table row on the block-length field, not on `mkfs_time == bytes_used`") — landed pre-freeze, not carried into the table | `avm-row-guard.py`: red 4 findings on SKILL v1 (no layout column; unscoped wrapper; damage-only attribution; no without-`-be` remedy), green on `table-v2-proposed.md` |
| MH-7 | **the executable version of a rule dropped the guard its own prose states** — base prose says an envelope with another verb or provider "is not comparable … do not relabel"; the executable table has no such column, so the interpreter labels `analyze_function`/`ghidra` envelopes `no-squashfs-chunk`, and the registry row "labels REA envelopes" is over-broad | base `SKILL.md:1241` (row 10 of the Decision table), current `SKILL.md:1351` (registry row) | R39-CL1; `w2/R39W2C2AxisFit.md` §4 C2 | `check-domain-guard.py`: red on SKILL v1 (2 findings of missing columns + both envelopes labelled `no-squashfs-chunk`), green on `table-v2-proposed.md` (both `unclassified`) |
| MH-8 | **a rule that tells the reader to ignore the gaps its own envelope carries** — an image with both link kinds resolves to the escaping row by order, whose action says "expect the path absent", while the envelope carries `unpublished-entry` gaps for the links that were kept; 2 of 6 round-39 Core carriers are this shape | K5 (`G=[unpublished-entry]`, SR=yes, P=10) and K6 (P=8) both labelled `escaping-symlink-removed` rule 6 by the frozen interpreter; symlink tables in `plans/round-39-claims.md`; the knowledge entry states the collapse at `:47-48` | R39-CL2; `w2/R39W2C2AxisFit.md` §4 C1 | `check-mixed-symlinks.py`: red on SKILL v1 (3 findings), green on `table-v2-proposed.md` (both `mixed-symlinks`) |
| MH-9 | **the depth-bearing column is unscored** — `c2-counter.py` compares `label == expected_label` only; `sqfs-triage.py` declares cause/action "documentation only", so an 8-row nonsense-cause table scores the same as the shipped one | `tools/round-39/c2-counter.py:390`; measured: all 8 cause cells replaced with "deliberate nonsense cause -> do the opposite" → labels agree **20/20**, (label, cause) pairs agree **0/20** | R39-CL3 third part; `w2/R39W2C2AxisFit.md` §3(c) | `action-scoring-check.py`: the label-only view is blind 20/20 while the action-aware view separates 0/20, and the self-comparison is stable 20/20 (exit 0) |
| MH-10 | **one rule, two live copies** — the frozen interpreter embeds `TABLE_BLOCK` and builds every selftest fixture from it, but the counter scores `SKILL.md`; the copies disagree in decision cells, so the 35-case selftest certifies a table the lane does not ship | `tools/round-39/sqfs-triage.py:130` `TABLE_BLOCK`, used at `:680,779,790,798,841,870,888,899,910`. Cell diffs: `dep-missing-be`/`le` files `0` vs `*`; `escaping-symlink-removed`, `in-tree-symlink-metadata`, `clean` handler `squashfs_v4_be` vs `squashfs_v4_*`. Behaviour: embedded table 18/20 on the frozen held-out set, shipped 20/20 | this seat; independently asserted by the peer seat `R40C2AxisFit.md` (a) answer ("a second, divergent copy scoring 18/20") — the two measurements agree | `table-copies-gate.py`: red 9 findings + the 18/20 vs 20/20 delta on the shipped bytes; writes a single-source copy (`--fix-out`) and is green on it (both 20/20) |
| MH-11 | **the landing commit did not move the axis row the lane scores** — at `6fdaf4f1` the `## Owned axes` coverage row reads 126/126 while the bytes hold 128 knowledge files, and the depth row reads 17/17 while the craft section holds 18 blocks; both catch up only in the last wave-2 commit `2b0b6a29`, so the round's own scorecard lagged its evidence by three commits | `git show 6fdaf4f1:SCORECARD.md` lines 23-24 vs recipe A at that rev: coverage computed 128/128, depth 18/18; `2b0b6a29` matches. The SCORECARD round-39 record (`:3430`) itself concedes it | `w2/R39W2C1AxisFit.md` D1; repaired in `2b0b6a29`; **not** an `M39-*` row | `axis-record-gate.py`: red 2 findings at `6fdaf4f1`, green at `2b0b6a29` — the gate compares the living row's first `N/N` pair against recipe A computed from git bytes |
| MH-12 | **committed provenance records a command that was not run** — `heldout-gen.py` executes `... extract-firmware --format json ...` but records `[REA_PACKAGE, 'extract-firmware'] + cmd[3:6] + …`, so all 20 `run.json` carry the subcommand twice; a replay that follows the record fails, and the record is the one a later round is asked to reproduce | `tools/round-39/heldout-gen.py:408` (executed) vs `:416` (recorded); 20/20 `corpus/evidence/round-39/c2/heldout/H*/run.json` `rea_argv` = `rea-agents@6.5.0 extract-firmware extract-firmware --format json …`. The same records **do** carry `exit_code`, so the field existed in the lane's evidence vocabulary | `w2/R39W2Separability.md` D2; **not** an `M39-*` row, not in the spot-check | `evidence-argv-gate.py`: red 20/20 on the committed records, green on `--fix-out` copies with the duplicate token dropped |

## 3. Red/green evidence

`artifacts/R40MistakeHunt/runs.txt` is one run of `run-all-gates.sh` on this host (Linux
7.2.11-arch1-1, python 3.14.8, lane HEAD `fa6a8a3f`). Every block prints `$ command`, its output
and `exit=`. Totals: **28 runs: 14 exit 1 (red), 13 exit 0 (green), 1 exit 2 (a shape check, §4 D6)**. The green fixtures are
built by `green-fixtures.py` from lane files into `$TMPDIR/mistake-green` (two git fixture repos
are created there with `git -C "$D" -c user.name=fx -c user.email=fx@fx`; the lane is not
touched).

| check | red input | red rc | green input | green rc |
|---|---|---|---|---|
| `control-freeze-gate.py` (a) | `controls/tables` at `8fcda41c` | 1 | fixture repo, table in the freeze commit | 0 |
| `control-freeze-gate.py` (b) | `w1/artifacts/R39C2Shortcuts` at `8fcda41c` | 1 | fixture repo, `cause -> action` intact | 0 |
| `control-freeze-gate.py` format half | fixture, `cause = action` | 1 | — | — |
| `receipt-fields-gate.py` | round-39 scores + ledgers | 1 | same files + `exit_code`, `status` | 0 |
| `report-content-gate.py` | fleet round-39 report | 1 | report + cross-domain line | 0 |
| `depth-delta-gate.py` | `a2f64e1d→52b0eb29`; `fa6a8a3f` | 1, 1 | fixture 5.0 → 10.0 | 0 |
| `avm-mode-gate.py` | `tools/round-39/gen-squashfs.py` | 1 | `gen-squashfs-avm-mode-fixed.py` | 0 |
| `avm-row-guard.py` | `SKILL.md` v1 | 1 | `table-v2-proposed.md` | 0 |
| `check-domain-guard.py` | `SKILL.md` v1 | 1 | `table-v2-proposed.md` | 0 |
| `check-mixed-symlinks.py` | `SKILL.md` v1 | 1 | `table-v2-proposed.md` | 0 |
| `action-scoring-check.py` | (label-only view: 20/20 blind) | 0 | (action-aware view: 0/20) | 0 |
| `table-copies-gate.py` | shipped interpreter | 1 | single-source copy | 0 |
| `axis-record-gate.py` | `6fdaf4f1` (coverage 126/126 vs 128/128; depth 17/17 vs 18/18) | 1 | `2b0b6a29` | 0 |
| `evidence-argv-gate.py` | 20 committed `run.json` | 1 | `--fix-out` copies | 0 |
| D6 shape: v2 table under the frozen interpreter | `table-v2-proposed.md` | 2 (v1 marker required) | — | — |

`artifacts/R40MistakeHunt/avm-measurements.txt` holds the MH-5/MH-6 grounding: the genuine
AVM-BE probe (shokuknow `round11/work/avm-be.squashfs`, sha256 `c7f74691…d32d32`, copied to
scratch; marker-stripped derivative sha256 `abfd7ec9…512ac`), the `sasquatch-v4be` 4.5.1 matrix,
the stock-vs-fixed writer matrix (stock `--endian avm`: noflag exit 1 / `-be` exit 0; fixed:
noflag exit 0 2 files / `-be` exit 1), and the frozen interpreter's labels for H13/H15/H01 with
their matched row causes. No REA and no unblob run; the only extractor invoked is
`sasquatch-v4be` on probe fixtures (the 4096 B round-11 AVM fixture, its marker-stripped
derivative, and the 392 B writer outputs), none of which is a frozen C1 carrier.

## 4. Attack on the round-40 draft (`plans/round-40-claims.md`)

Nothing here changes a claim byte; these are pre-freeze findings for the L1.

- **D1 (depth label, `:69-99`).** R40-C2 is labelled a depth claim, but the owned depth recipe
  cannot move: measured `depth_score 10.0` with `18/18` blocks at the round-40 base `fa6a8a3f`.
  QUALITY 75 says a claim that leaves the counted surface unmoved is not a depth claim and
  relabelling after data is forbidden — so the label must be settled **before** the freeze, or
  the measured surface must change (the draft's own "counter reports the number of distinct row
  decisions" and the scored action column are the only candidates that can move).
- **D2 (carrier plan, `:52-56`).** L1/L2 are "lane-built genuine AVM-layout carriers … from a
  writer that emits little-endian block lengths". No such writer exists on this host:
  `--endian avm` emits BE block lengths (MH-5), and `heldout-gen.py:67` names the same marker
  transform. Without a writer, L1/L2 cannot be built and the target `carriers_matched == 4`
  collapses to the two vendor members. `artifacts/R40MistakeHunt/gen-squashfs-avm-mode-fixed.py`
  is a one-hunk fix of the round-39 writer (metadata block headers LE when the mode is `avm`)
  whose gzip and xz images extract under `sasquatch-v4be` noflag and fail under `-be` — the
  layout signature, measured. It inherits the round-39 writer's limits (no fragments, no xattrs,
  no export table). [INFERENCE] It has not been run through REA (carrier discipline), so
  "REA publishes it as `squashfs_v4_be` without `-be`" is untested.
- **D3 (kill control read through v1, `:61-65`).** The draft's control "a genuine AVM body with the
  marker stripped (unblob adds `-be`, extraction fails)" is the exact tuple SKILL v1 calls
  `body-extractor-failure` → "the image body or header is damaged … never patch the envelope into
  a success". Any wave check that interprets that control with the current SKILL reads the
  intended behaviour as damage; v2 needs the block-length field (MH-6) or an explicit note.
- **D4 (freeze-integrity rule as prose, `:19-20`).** "Control tables and control receipts' inputs
  are committed and format-validated in the freeze commit itself" is a sentence; R39-CL4 is
  exactly what a sentence without a gate produces. Bind `control-freeze-gate.py` (or the peer's
  `score-receipt.sh`) into the freeze.
- **D5 (receipts, `:20`).** "Every score receipt records the counter's exit code" — the round-39
  C2 receipts record `interpreter_exit`, which is not the counter's exit; the field the gate
  looks for is a top-level integer under `exit_code|exit|rc|returncode`. `receipt-fields-gate.py`
  also refuses a measured receipt whose only provenance is `unevaluable`.
- **D6 (v2 domain guard).** The draft's out-of-domain class requires the interpreter to read
  `operation`/`provider`; the frozen interpreter requires the v1 marker and the 9-column header
  (verified: `sqfs-triage.py --skill table-v2-proposed.md --table-only` → exit 2, `marker
  '<!-- sqfs-triage-table v1 -->' absent`), so v2 needs its own interpreter version, not a table
  swap. `table-v2-proposed.md` shows a table shape the checks accept.

## 5. Not mined, and why

- **R39-CL5 (re-minted fabrication reaches 6/6).** Already disclosed in the round-39 freeze and
  bound in R40-C1's rerun clause. A fix here would need a REA run on a C1 carrier to show the
  projection comparison failing, which this wave's carrier discipline forbids — left to the
  freeze's own control.
- **Already `M39-*`:** false absence (M39-1), routed-ledger lapse (M39-2), uncommitted wave
  checkpoint (M39-3), control receipts re-scored in place (M39-4), context lapse (M39-5), the
  POSIX-clamp predicate (M39-6), writer UTF-8/xz (M39-7), two misroots (M39-8/9), post-freeze
  edits (M39-10). MH-1/2/3/5 are adjacent to M39-4/7 but not the same class (§1).
- **Wave-2 defects that were never routed at all:** `R39W2C1AxisFit` D1 (MH-11) and
  `R39W2Separability` D2 (MH-12) are not in the spot-check's R39-CL list, so the round-39→40
  routed ledger has no state for them; they enter here with their own gates.
  `R39W2C2TableReview`'s "two cause cells narrower than the cited source" (row 6 omits the
  symlink-loop branch, row 7 claims `symlink` for a gap REA also emits for `special`) is not a
  separate row here: it is recorded in the triage knowledge entry, and its repair is a v2 table
  text change covered by MH-6's guard. `R39W2C2Shortcut`'s "7 cells reach 20/20" is the same
  saturation family as MH-4/MH-9 and is carried by the peer `R40C2AxisFit`.
- **Open items that are not mistakes:** the `heldout-gen.py` `corruption_bad_minor` docstring
  erratum, surviving interpreter/counter mutants, loose S118/S121 anchors, R36-CL5.
- **Cross-seat overlap:** MH-2 overlaps the peer deliverable `R40CL6Receipts` (a wrapper + status
  filler) — mine is a checker over committed artifacts; the two agree that the round-39 receipts
  carry no exit code and the ledgers carry null status. MH-4 and MH-10 overlap the peer
  `R40C2AxisFit`; MH-10's independent 18/20 measurement equals the peer's.

## 6. Lane observation (not this seat's file, not removed)

`detail.log` at the lane root (9535 B, mtime 2026-10-26 15:29:36) is a peer seat's C1 control-run
detail output (`DETAIL green (4 AVM carriers …)` lines) written outside that seat's artifacts
directory — the M39-8/M39-9 misroot shape, in this wave. It is named here for the wave sentinel;
this seat did not create, move or delete it.

## 7. Artifacts, tooling, bounds

`artifacts/R40MistakeHunt/` (all writes of this seat):

| file | role |
|---|---|
| `control-freeze-gate.py` | MH-1 gate (freeze presence + format of control tables) |
| `receipt-fields-gate.py` | MH-2 gate (exit code per measured receipt, status per seat) |
| `report-content-gate.py` | MH-3 gate (PROTOCOL minimum content) |
| `depth-delta-gate.py` | MH-4 gate (recipe A headroom/delta) |
| `avm-mode-gate.py` | MH-5 gate (a mode named `avm` must emit LE block lengths) |
| `avm-row-guard.py` | MH-6 guard (layout column, scoped wrapper, damage attribution, remedy) |
| `check-domain-guard.py`, `sqfs_rows.py` | MH-7 check + the independent table reader it uses |
| `check-mixed-symlinks.py` | MH-8 check |
| `action-scoring-check.py` | MH-9 check (label-only vs action-aware, through the frozen interpreter) |
| `table-copies-gate.py` | MH-10 gate (+ `--fix-out` single-source copy) |
| `axis-record-gate.py` | MH-11 gate (living axis row vs recipe A at a revision) |
| `evidence-argv-gate.py` | MH-12 gate (recorded argv must name the executed command; `--fix-out`) |
| `table-v2-proposed.md` | the green fixture table the three table checks accept (not a claim) |
| `gen-squashfs-avm-mode-fixed.py` | MH-5 fix: round-39 writer with LE metadata headers in `avm` mode |
| `green-fixtures.py` | builds the pass-side fixtures (augmented scores/ledgers, report copy, two git fixture repos, depth repo) |
| `run-all-gates.sh`, `runs.txt` | every red/green run, commands and exit codes |
| `measure-avm.sh`, `avm-measurements.txt` | AVM-layout matrix and the frozen interpreter's three labels |

Reproduce: `LANE=<lane> TMPDIR=<scratch> sh artifacts/R40MistakeHunt/run-all-gates.sh` and
`LANE=<lane> TMPDIR=<scratch> sh artifacts/R40MistakeHunt/measure-avm.sh`.

Tooling: nothing installed or upgraded (no pacman, uv, npx). Binaries used: `git` (read-only:
`show`, `log`, `ls-tree`, `cat-file`, `rev-parse`, `status`), `python3` (3.14.8),
`sasquatch-v4be` 4.5.1 (direct, probe fixtures only), `sha256sum`. VCS: no add/commit/checkout/
reset/stash/pull/push; the only git writes are two `git init` fixture repos under scratch, each
verified to resolve to itself before its first commit. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40MistakeHunt` removed at exit; shokuknow read only (one 4096 B
file hashed and copied into scratch); no `find`/`du` sweeps under `/fast/scratch`.
