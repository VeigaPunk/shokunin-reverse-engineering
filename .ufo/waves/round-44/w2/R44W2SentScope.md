# R44W2SentScope — write-scope discipline audit of the round-44 evidence

Seat R44W2SentScope (sentinel, wave 2). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read-only audit: **no** mutating git/jj command was run, no claim/counter/rubric/frozen byte was
touched, nothing was written outside
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w2/` and
`/fast/scratch/hyaku/kaidoku-r44/R44W2SentScope/`. No tool was installed (nothing was needed).

Measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`. All `git show <REV>:<path>` reads below are at that
revision unless a different rev is named.

## Axes

1. **Scope purity** — every path a receipt/output *writes to or cites as its evidence* lies in the
   lane or in the declared scratch segment `/fast/scratch/hyaku/kaidoku-r44/`.
2. **Record re-derivability** — every cited path still resolves, or an in-lane copy carries the
   bytes the claim rests on. A citation that no longer resolves is a defect even when it was
   produced under the declared segment, because the round's own discipline deletes that segment.
3. **Dependency ranking** — each finding is tagged with the record element that breaks if it is
   wrong (verdict, score, control, or navigation), so the L1 can triage without re-reading the tree.

## Census

Corpus: all `*.json` and `*.md` under `.ufo/waves/round-44/` (425 files at scan instant
`2026-10-28T14:25:45Z`; wave-2 peers were still writing, so counts move by the minute).
11,831 absolute-path occurrences, 8,238 of them outside the lane + declared scratch.

| class | occurrences | distinct | write target? | verdict |
|---|---|---|---|---|
| lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` | 1,068 | 158 | yes | in scope |
| declared scratch `/fast/scratch/hyaku/kaidoku-r44/` | 2,525 | 440 | yes | in scope (but many now deleted → F1/F2) |
| foreign scratch `/fast/scratch/hyaku/kaidoku-r42/…` | 3,950 | 1,889 | read/cite | **F7** (inherited; tree now gone) |
| `/tmp` | 622 | 68 | yes | **F3, F5, F6** |
| fleet root `/home/vgpnk/Projects/shokunin/<other>` | 33 | 13 | read only | non-violation (F9) |
| home outside lane (`~/.local/bin`, `~/.npm/_npx`, `~/.omp`) | 284 | 24 | read/host tool | non-violation (toolchain digests are bound by design) |
| host system (`/usr/bin/unsquashfs`, `7z`, `python3`) | 810 | 29 | read | non-violation |
| other / non-host fragments (`/len`, `/skill`, `/scratch/…` fixtures) | 2,539 | 259 | — | non-violation (F8) |

A second, stricter pass walked **JSON values only** (359 files), keying on write-shaped fields
(`output_directory`, `work`, `root`, `sandbox`, `cwd`, `local_path`, `json_out`, `path`, `…`):
4,008 outside rows — **0 target the fleet root**, 3,830 are the inherited round-42 fixture bytes
(F7), 64 are `/tmp` (F3/F5/F6), 67 are host binaries, 27 are toolchain binaries / the bare fleet
root string, 20 are the four synthetic `/scratch/…` values (F8).
Artifacts: `artifacts/R44W2SentScope/summary.json`, `paths.tsv` (9,449 rows at the 14:24 pass),
`outside-values.txt`.

**No seat wrote an artifact under the fleet root.** The fleet-root hits are read citations:
`AXES.md` (`w1/R44ScoutCalib.json:766`), `scripts/sources-census.sh` (round-end census),
`.ufo/watchdog.log` (dispatch/spec prompt text), `.tower/worktrees/kaika` (`w1/R44C2SentReview.md:25,54`),
`.ufo/prompts/tsukuroi-round-48.md`, `considerthese` (absence probe). All are legitimate reads.

## Findings, ranked by record dependence

### F1 — HARD — the whole C1 control set cites deleted sandboxes and unresolvable revisions

*Record element at risk:* the frozen claim's control block and its kill rule
(`plans/round-44-claims.md`, R44-C1 "Controls scored at the freeze"), i.e. the evidence that the
counter can go red at all.

*Path:line.* `corpus/evidence/round-44/controls/pos/receipt.json:102` (command),
`:243` (sandbox), `:251` (tree); `corpus/evidence/round-44/controls/c1/receipt.json:30` and `:259`;
same shape in `.ufo/waves/round-44/controls/{c0..c5,pos}/receipt.json`.

*Commands and observed values.*

```
$ git cat-file -e df4aa381f397a525979ef353657265c9a51db975     # CTL-C1-1 --rev
exit=1        (fatal: Not a valid object name)
$ test -e /fast/scratch/hyaku/kaidoku-r44/l1-c1-controls-evidence/run.gyt5aox_/sandbox-c1
exit=1
```

*Systematic result* — 14 control receipts carry `--rev`; **12 of 14 name a commit absent from the
lane object database**, and **all 14** name a `sandbox`/`--work` root that no longer exists
(`l1-c1-controls-final/run.x3vs44r6` and `l1-c1-controls-evidence/run.gyt5aox_`, both under the
declared segment, both deleted). Only `CTL-C1-0` resolves, because its `--rev` is the freeze commit
`c48f8a4`.

*Two divergent runs of the same controls.* The wave record and the lane record are **different
scoring runs**, not copies:

| control | wave record `--rev` | lane record `--rev` | wave sandbox | lane sandbox |
|---|---|---|---|---|
| CTL-C1-1 | `fdab6b7e…` | `df4aa381…` | `…/l1-c1-controls-final/run.x3vs44r6` | `…/l1-c1-controls-evidence/run.gyt5aox_` |
| CTL-C1-POS | `e094db11…` | `d73d0806…` | `…/run.x3vs44r6/sandbox-pos` | `…/run.gyt5aox_/sandbox-pos` |

*Impact.* Every control in the frozen claim is now an authored JSON file plus a digest table. A
reader cannot re-run, or even resolve, the revision each was scored against; the kill-rule argument
("no counterfactual red control reached 4/4") rests entirely on self-reported `exit_code` values.
This is the same class the round's own R44-REAP notice named (`/tmp` and `$HYAKU_SCRATCH` not
citable) applied to the declared segment: deleting scratch at yield removes the only thing that
makes a control receipt checkable.

*Smallest remediation.* Add a `sandbox_tree` digest block to each control receipt (per-file sha256
of the planted tree, including the two docs) and cite the *launch rev* (a committed lane rev, or the
freeze for pre-data arms) instead of the throwaway sandbox commit; or keep a read-only
`corpus/evidence/round-44/controls/<ctl>/sandbox/` copy of the planted files. The receipt already
carries a `tree` digest map — the defect is that for `pos` and `c3` it does not match the frozen
fixture (F4).

### F2 — HARD — the C1 honest-stop record rests on a `parameters.output_directory` whose tree is gone

*Record element at risk:* the R44-C1 verdict itself (`carriers_matched 4`, `met_target false`,
exit 1 at `55bcce69`) and R44-CL2's "internally unsatisfiable" reading, both of which are stated
over the scratch form of that field.

*The four receipts* (values verified at `55bcce69`; unchanged at `HEAD`):

| id | `parameters.output_directory` | exists? | after.json sha256 |
|---|---|---|---|
| v1le | `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out` | **MISSING** | `eb44f3db017337dbd9aca2af800a312de343bbffd902e8fb196d030064d90abf` |
| v1be | `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1be.1342995/rea-out` | **MISSING** | `facc57d94d86c3e2ac9673896e3d7d8e929246a417c1ba03c48a3bc786c3b347` |
| v2le | `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v2le.1342995/rea-out` | **MISSING** | `162e69b2931c40dc3e35fbfd0e90c604f7fd991269c008f1d246c4a7e2a9b993` |
| v2be | `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v2be.1342995/rea-out` | **MISSING** | `18839471ce3b8494e15a0460984445f6a1e63adcbb70c9954ce7b463daa66550` |

*Commands and observed values.*

```
$ test -e /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out
exit=1
$ grep -o '/fast/scratch/hyaku/[A-Za-z0-9._/-]*' corpus/evidence/round-44/c1/manifest.json | sort -u
/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out
/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/unblob-tee.sh
   … (all four carriers, rea-out + unblob-tee.sh)
```

`corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}/after.json` each carry 26–30 references into
that one deleted root; the manifest additionally binds `REA_UNBLOB_COMMAND=…/unblob-tee.sh` inside
it (`manifest.json`, `carriers.*.command`). Neither file exists.

*Mitigation present in the record.* The lane copy is otherwise self-contained:
`corpus/evidence/round-44/c1/<id>/{after.json,envelope.json,extract-env.json,extract-tree.tsv,run.json,provenance.json,firmware.bin_extract/}`
all exist, so the *file digests and sizes* the claim binds are checkable from lane bytes.

*Impact.* The verdict is not falsified — the counter re-derives from the committed bytes — but the
one field the stop is *about* cannot be inspected at its source, and the claim simultaneously
requires the field to name `/kaidoku-r44/` (predicate) while the scratch rule forbids relying on a
scratch citation (addendum §7.5 / R44-REAP). The record should state which rule governs; today it
states neither.

*Smallest remediation.* In `corpus/evidence/round-44/c1/<id>/provenance.json` record the deletion
as expected (`scratch_reaped: true`, plus the `run.json`/`manifest.json` in-lane copies that hold
the same `output_directory` string) and have the counter bind provenance to the in-lane copy, not
to the scratch path's existence. Do not silently keep citing the reaped path as if it were live.

### F3 — HARD — the C2 measured score embeds a deleted `/tmp` clone in all 80 entry commands

*Record element at risk:* the R44-C2 MET record — `entries_evaluated 80`, `mismatches []`, exit 0
at `55bcce69` (`.ufo/waves/round-44/l1/c2-score-at-55bcce69.json`).

*Path:line.* `l1/c2-score-at-55bcce69.json:76` and 79 further lines — every
`entries[*].command[7]` is the string `/tmp/c2-counter.p_yfx2x5/repo`.

*Commands and observed values.*

```
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-44/l1/c2-score-at-55bcce69.json'));\
print(d['entries'][0]['command'][7]); \
print(len([e for e in d['entries'] if e['command'][7]==d['entries'][0]['command'][7]]))"
/tmp/c2-counter.p_yfx2x5/repo
80
$ test -e /tmp/c2-counter.p_yfx2x5/repo
exit=1
```

Root cause is in the frozen instrument, not only in the invocation. `tools/round-44/c2-counter.py:1205-1207`:

```python
base = work or os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
workdir = tempfile.mkdtemp(prefix='c2-counter.', dir=base) if os.path.isdir(base) \
    else tempfile.mkdtemp(prefix='c2-counter.')
```

Two ways to land in `/tmp`, and the second is the silent one: `--work`/`HYAKU_SCRATCH` naming an
existing `/tmp/...` base, **or** `--work` naming a directory that does not exist yet — `isdir`
fails and the `else` branch calls `mkdtemp()` with no `dir`, i.e. `tempfile.gettempdir()`, instead
of erroring on the bad argument. `gettempdir()` honours `TMPDIR`/`TEMP`/`TMP` and only then falls
back to `/tmp`/`/var/tmp`/`/usr/tmp`/cwd, so the recorded `/tmp` places the L1's and wave-1
invocations in the cell "no valid `--work` **and** no valid `TMPDIR`" — the default environment.
R44W2C2Freeze probed all three cells (`<scratch>/work-missing` with and without an existing
`TMPDIR`): created `--work` → cites `--work`; uncreated `--work` + valid `TMPDIR` → cites `TMPDIR`
(exit 0, `<scratch>/tmp/c2-counter.hrtv590_/repo`); uncreated `--work` + no `TMPDIR` → `/tmp`. That
is why (b) below is load-bearing rather than belt-and-braces: an uncreated `--work` that is silently
turned into a tempdir scrape *relocates* the citation into whatever temp root the operator exported
and then serialises it into `entries[].command`. (Their earlier reproduction of the second cell is
what put `/tmp/c2-counter.gdl0i8bb/repo` in their 11:23 artifact set.)
`tools/round-44/c1-counter.py:452-461` has no such hole: `scratch_root()` does
`os.makedirs(WORK_OVERRIDE, exist_ok=True)` or
`os.makedirs(/fast/scratch/hyaku/kaidoku-r44/counter, exist_ok=True)` and its docstring says
"Deliberately never `tempfile.gettempdir()`" (R44-SCR-TMP).

*Live recurrence in wave 2 (observed, then repaired by the peer).*
`.ufo/waves/round-44/w2/artifacts/R44W2C2Freeze/base.json` (mtime 11:23) contained
`/tmp/c2-counter.gdl0i8bb/repo`: a wave-2 seat re-ran the same frozen counter and reproduced the
same class of citation while this audit was running. R44W2C2Freeze re-scored and replaced that
artifact set at ~11:31; the replacement has 0 `/tmp` citations (verified), with the verdict
unchanged (base `stdout_sha256` `b4e4a26b…f132`, 80/80). The defect therefore remains in the
frozen instrument and in the pre-existing receipts, not in that seat's final artifacts. Also present
in the four wave-1 C2 control receipts
`w1/artifacts/R44C2Rubric/receipts/{census-shipped-artifact,control-seeded-mismatch,control-repair,control-claim-mode-c1-readme-row}.json`
(`/tmp/c2-counter.{x9y7f1zo,37ii9ojf,b2biwxe0,i2vwngic}/repo`).

*Exploit path (integrity, no privilege needed).* `/tmp/c2-counter.p_yfx2x5/repo` is an unowned
path under a world-writable directory. Any local user can pre-create that exact directory with
attacker-chosen content; a verifier that trusts the recorded command — or a re-run that "reuses the
work dir" — would then read attacker bytes as the measured tree. The `0755`/`0700` mode of a fresh
`mkdtemp` does not help once the clone has been reaped, because nothing records a digest of the
clone itself.

*Impact.* The C2 score body (per-entry `stdout_sha256`, `subject_sha256_at_rev`, `match`) is
self-contained and reproducible from the lane repo, so the MET verdict survives; but the command
trail is stale everywhere and violates the round's own "never cite a `/tmp` path as evidence".

*Smallest remediation.* Three changes, all in the instrument: (a) `os.makedirs(base, exist_ok=True)`
before `mkdtemp`, mirroring `c1-counter.py:452-461`, so an uncreated `--work` no longer escapes;
(b) **load-bearing:** treat an uncreated or unusable `--work` as a caller error — exit 2, the same
class as an unknown revision — instead of scraping `gettempdir()`; exporting `TMPDIR` is not a fix,
it only relocates the citation into whatever temp root the operator happened to set, and the
default (no `--work`, no `HYAKU_SCRATCH`) should use the declared segment as `c1-counter.py` does;
(c) re-emit `l1/c2-score-at-55bcce69.json` with `--work /fast/scratch/hyaku/kaidoku-r44/<seat>` so
`entries[*].command[7]` names a re-derivable path, and record the clone's tree digest so a later
re-materialisation of that path is detectable.

### F4 — MEDIUM-HARD — the post-freeze commit rewrote scratch provenance *inside* the frozen fixtures, and the committed control evidence does not match the bytes that were scored

*Record element at risk:* M44-2 / the freeze defect, and the C1 control block (F1). Another seat
owns M44-2 itself; this finding is about **what the edit changed** and the resulting digest split.

*Commands and observed values.*

```
$ git log --oneline c48f8a4..HEAD -- tools/round-44/
c86ea508 round-44: land the post-freeze control fixtures and unsettled wave evidence
$ git show --name-status --format= c86ea508 -- tools/round-44/control-fixtures
M  tools/round-44/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json
M  tools/round-44/control-fixtures/c3/manifest.json
M  tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/{v1be,v1le,v2be,v2le}/after.json
M  tools/round-44/control-fixtures/pos/corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md
M  tools/round-44/control-fixtures/pos/manifest.json
exit=0
$ git show 55bcce69:tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json | sha256sum
12c794ada076a87dea9bf51082f38a38f9a4ababbe3ce349591b82f3a0d52fbb  -
exit=0
$ git show 55bcce69:corpus/evidence/round-44/controls/pos/tree/corpus/evidence/round-44/c1/v1le/after.json | sha256sum
51dd0688f4e8385bc473fa51efecfeff6f55e8f5fc33dd3bac13274f102a9ee4  -
exit=0
# c3 v1le: frozen adba89ea3d22de718b27b05976c9da316f6c8517a8e1bbc24ef2e09291bfe8c9
#         copy   8b15697baae7937918d185a11ebc1e216c5e04dcc5368c9fe97f652154bef43d
# the committed receipt's tree[*].sha256 for pos v1le is 51dd0688f4e8…, i.e. the copy
```

All eight are **M** (modified), not A: the fixtures already existed at the freeze. The content of
the modification is a scratch-provenance rewrite, e.g. for `pos/…/v1le/after.json`:

```
-  "path": "/tmp/rea-firmware-U2G3Cb/extracted/firmware.bin_extract/apple.txt",
+  "path": "/fast/scratch/hyaku/kaidoku-r44/probe-v21/rea-firmware-n0k0aR/extracted/firmware.bin_extract/apple.txt",
```

i.e. `/tmp/rea-firmware-*` citations were replaced with `probe-v21` paths — the round's own
"unbound exploratory v2.1 assets, explicitly EXCLUDED from R44-C1" (`plans/round-44-claims.md`,
amendment 1). The frozen v1/v2.0 control fixture now points at a v2.1 probe tree.

*Digest split at the measured revision.* The committed control receipt's `tree` block records the
**second** run's bytes; the frozen fixture the counter scored has the **first** run's bytes:

| control | `receipt.tree` sha256 (short) | frozen `tools/…` @55bcce69 | committed `corpus/…/tree` copy |
|---|---|---|---|
| pos v1le | `51dd0688f4e8…` | `12c794ada076…` **MISMATCH** | `51dd0688f4e8…` match |
| c3 v1le | `8b15697baae7…` | `adba89ea3d22…` **MISMATCH** | `8b15697baae7…` match |
| c1 v1le | `d9fc4ae76a68…` | `d9fc4ae76a68…` match | match |
| c4 v1le | `3c6f01994afd…` | `3c6f01994afd…` match | match |

At `HEAD` the two trees are identical (`pos v1le` = `51dd0688f4e8` on both sides), so `c86ea508`
retro-fitted the frozen fixtures to the lane's committed copies after the measurement.

*Impact.* At the measured revision the record publishes a control tree that is not the tree the
counter scored; the receipt's own digest proves it. M44-2's text ("added/edited 8 files under a
frozen directory pathspec") does not say the edit rewrote evidence provenance or tied v1/v2.0
fixtures to a v2.1 probe root, so the record understates what was changed.

*Smallest remediation.* Name the eight files and the nature of the edit in M44-2 (this is an
appendix to the existing entry, not a new claim), and state that the C1 control receipt `pos`/`c3`
tree digests refer to the post-freeze tree, not the scored one. Do not restore the freeze bytes.

### F5 — MEDIUM — the frozen control fixtures carried `/tmp` citations at the measured revision

*Record element at risk:* the C1 control block used in wave 1 (before `c86ea508`).

*Path:line at `55bcce69`.*
`tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json:154,156,158,159,185,205,216,236,247,267,278,287,293,299,306,317,347,354`
(18 lines, 8 distinct `/tmp/rea-firmware-U2G3Cb/*` paths);
`tools/round-44/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json:128,130,132,133,159,197`
(6 lines, 4 distinct `/tmp/rea-firmware-MNL2DH/*` paths). The same bytes are on disk at
`w1/artifacts/R44C1Controls/controls/{pos,c3}/tree/corpus/evidence/round-44/c1/v1le/after.json`
(sha256 equal to the frozen blobs — verified: `12c794ada076…`, `adba89ea3d22…`).

*Command.*

```
$ git show 55bcce69:tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json \
  | grep -o '/tmp/rea-firmware-[A-Za-z0-9]*' | sort -u
/tmp/rea-firmware-U2G3Cb
exit=0
$ git show 55bcce69:tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json \
  | grep -c '/tmp/'
18
exit=0
$ git show 55bcce69:tools/round-44/control-fixtures/c3/corpus/evidence/round-44/c1/v1le/after.json \
  | grep -c '/tmp/'
6
exit=0
```

*Impact.* The positive dev arm and the `missing-extractor-dependency` control are built from
envelopes whose `parameters.path`/`locations[].path` point at `/tmp` trees that never survived and
were never lane evidence. The record does not disclose this; it is only visible by reading the
fixture bodies. Content-wise the fixtures are synthetic dev inputs, so no claim value changes — but
the round's "planted real REA scratch receipts" description is inaccurate for these files, and the
`/tmp` citation rule is violated in frozen bytes.

*Smallest remediation.* State in the C1 control block that `pos` and `c3` dev envelopes were
composed from runs whose output roots were `/tmp/rea-firmware-*` (later rewritten by `c86ea508`),
and that neither fixture is a verbatim single-run receipt. Alternatively publish a one-run
`pos` envelope under the declared segment and freeze that.

### F6 — MEDIUM-LOW — wave-1 seats put their own scratch in `/tmp` and cite it from receipts

| receipt | line | cited path | now |
|---|---|---|---|
| `w1/R44SrcOracle/receipts/oracle-tree-inventory.json` | 7 | writes+reads `/tmp/probe-R44SrcOracle-tree.tsv` | exists (3,111 B) |
| `w1/R44SrcOracle/receipts/file-token-flip.json` | 7 | `/tmp/probe-R44SrcOracle-flip.XXXX` | gone |
| `w1/R44RevFreeze/probe-receipt.json` | 3 | `python3 -I -B /tmp/probe-r44revfreeze.py` | exists (2,258 B) |
| `w1/R44C2Sentinel.md` | 375 | `--rubric /tmp/edited.json` (exploit narration) | gone |
| `w1/R44SrcOracle.md` | — | `/tmp/probe-R44SrcOracle-tree.tsv`, `/tmp/r44_unblob_sqfs.json` | both exist (3,111 B / 11,007 B) |

`r44-w1-results.json` also carries the two `/tmp` names from `R44SrcOracle`'s output (same class).

*Impact.* These are wave-1 method receipts, not part of the C1/C2 score chain, so the verdicts do
not depend on them. The rule violated is the citation rule ("never cite a `/tmp` path as evidence"),
and `probe-r44revfreeze.py` is a *script* the receipt's command depends on: a reader cannot re-run
the probe without a file that is not in the lane. Files under 50 MB are permitted writes, so the
transgression is the citation, not the write.

*Smallest remediation.* Copy the two still-live artifacts (tree.tsv, the probe script) into
`w1/artifacts/<seat>/` and point the receipts at the lane copy; mark the `flip.XXXX` and
`edited.json` references as illustrative.

### F7 — LOW-MEDIUM — inherited round-42 scratch citations, now unresolvable

*Path:line.* `tools/round-44/control-fixtures/c1/corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}/after.json:1`
(one-line JSON, 460–582 refs each into `/fast/scratch/hyaku/kaidoku-r42/…`);
`tools/round-44/control-fixtures/c4/…/after.json:91,102,113,121,135` (`output_directory`); plus the
wave copies under `w1/artifacts/R44C1Controls/controls/{c1,c4}/tree/…` and the lane copies under
`corpus/evidence/round-44/controls/{c1,c4}/tree/…`.

*Facts.* The `c1` fixture bytes are **byte-identical** to the committed round-42 evidence
(`v1le == corpus/evidence/round-42/c1/DW-FONERA/after.json`, sha `d9fc4ae76a68…`; same for the
other three), so this is inherited, not a round-44 write. The `c4` fixture is a prior-round
envelope planted deliberately so the counter's provenance binding rejects `/kaidoku-r42/`. But
`/fast/scratch/hyaku/kaidoku-r42` **no longer exists** (checked; see F10), so the *source* of those
bytes cannot be inspected either. Lane-wide, 852 committed files under `corpus/evidence/` cite
`/fast/scratch/hyaku/` (`grep -rl … | wc -l`), up from the 789 the round's own `R44ConnRouted.md:70`
recorded.

*Impact.* No round-44 verdict depends on it (the controls are red by design; the digests are
committed). It is the pre-existing debt R44-REAP described, now with one more reaped root. Worth
one line in the lesson rather than a new defect id.

### F8 — LOW — `/scratch/…`-rooted fixture paths (not a defect)

`tools/round-44/control-fixtures/c2/…/{v1le,v1be,v2le,v2be}/after.json:1` carry
`parameters.path`/`subject.local_path` = `/scratch/v1-le--squashfs_v1.0_le.bin` etc. These are the
authored "oracle-only, no REA run" envelopes for CTL-C1-2, so a non-existent root is the point.
Listed only so the L1 does not mistake `/scratch` for a real host root.

### F9 — observation — the round-42 scratch root was deleted mid-audit

At 11:19 local `/fast/scratch/hyaku/kaidoku-r42/` existed (6 entries); by 11:23 it was gone, while
`kaidoku-r44/` grew from 14 to 39 entries. I did not delete it and ran no mutating command. Per the
seat contract this is another actor's cleanup; it changes the *inspectability* of the `c1`/`c4`
fixture sources (F7) and should be mentioned wherever the r42-backed evidence is cited.

At 11:27, `git -C <lane> status --porcelain --untracked-files=no` reports three modified tracked
files — `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-44.md` — an in-progress record landing by
the L1, not part of the measured revision `55bcce69`. My audit reads revision bytes only, so none
of the findings above depend on the worktree state; but the final record must be committed before
it is scored, or the counters will see different bytes than the ones this audit describes.

## Verification summary for the four `after.json`

All four `parameters.output_directory` values name the `/kaidoku-r44/` scratch segment (the
predicate form, not the controls-amendment `corpus/evidence/…` form) and all four named trees are
**gone**. The receipts are unchanged between `55bcce69` and `HEAD`. The lane holds complete copies
(`after.json`, `envelope.json`, `extract-env.json`, `extract-tree.tsv`, `run.json`,
`provenance.json`, `firmware.bin_extract/`), so the C1 file-digest bindings remain checkable;
only the provenance *path* is unresolvable. This is consistent with the round's honest stop and
with R44-CL2 — but the record should say the cited tree was deliberately reaped, not leave the
citation looking live (F2).

## What I did not find (so the L1 does not chase it)

- **No artifact under the fleet root.** Zero JSON write-shaped fields point at the fleet root; the
  only outside-lane write-shaped values are the toolchain binaries at `~/.local/bin` /
  `~/.local/share/uv/...`, which are digest-bound by design (`carriers.json.toolchain`,
  `w1/R44C1Oracle.md:84-86`), and the `/tmp` values in F3/F5/F6.
- **No sibling-lane write.** The only sibling path is a *read* citation of
  `.tower/worktrees/kaika` in `w1/R44C2SentReview.md:25,54`, used to argue that a SCORECARD
  evidence cell in another worktree points at an absolute path. That is data about a rejected row,
  not a round-44 write.
- **No `/tmp` use by the C1 score path.** `l1/c1-score-at-55bcce69.json` uses
  `/fast/scratch/hyaku/kaidoku-r44/l1/c1-work-55` (exists) and cites no `/tmp`. The `/tmp` problem
  is confined to C2 (F3), the frozen control fixtures (F5), and wave-1 seat scratch (F6).
- `l1/c1-score-at-tip.json` correctly reports exit 2 with the eight `c86ea508` paths in
  `frozen_path_changed`; that matches `git log --oneline c48f8a4..HEAD -- tools/round-44/`.

## Reproduce

```bash
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
# census
python3 - <<'PY'   # full version: artifacts/R44W2SentScope/summary.json
import os; print(sum(1 for d,_,fs in os.walk(L+'/.ufo/waves/round-44') for f in fs if f.endswith(('.json','.md'))))
PY
# F1
git -C $L cat-file -e df4aa381f397a525979ef353657265c9a51db975; echo $?         # 1
test -e /fast/scratch/hyaku/kaidoku-r44/l1-c1-controls-evidence/run.gyt5aox_/sandbox-c1; echo $?  # 1
# F2
test -e /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out; echo $?       # 1
# F3
python3 -c "import json;d=json.load(open('$L/.ufo/waves/round-44/l1/c2-score-at-55bcce69.json'));print(d['entries'][0]['command'][7])"
test -e /tmp/c2-counter.p_yfx2x5/repo; echo $?                                                    # 1
# F4
git -C $L show --name-status --format= c86ea508 -- tools/round-44/control-fixtures
# F5
git -C $L show 55bcce69:tools/round-44/control-fixtures/pos/corpus/evidence/round-44/c1/v1le/after.json | grep -c '/tmp/'
```

## Hygiene

Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2SentScope/` removed at exit; the census artifacts
(`summary.json`, `paths.tsv`, `outside-values.txt`) were copied to
`.ufo/waves/round-44/w2/artifacts/R44W2SentScope/` first. Only that directory and this file were
written. No mutating git/jj command, no tool installation, no change to any claim, counter, rubric,
fixture or production doc.
