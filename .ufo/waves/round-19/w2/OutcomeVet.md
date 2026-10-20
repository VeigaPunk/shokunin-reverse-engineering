# Outcome vet — C3 depth claim, `t1250-vet` (wave 2)

Seat: `KaidokuR19.OutcomeVet-3` (leaf, read-only). No delegation, no production edits, no
REA `analyze`/`search`/`decompile`, no Ghidra run, no carrier execution, no MCP devices, no
installs. Scratch only under `/tmp/kr19-w2-vet-*`. The only LANE write is this report.

- LANE: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Observed tip at first read: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`
  (`git rev-parse refs/heads/main`, exit 0, 2026-10-20T16:15:31-03:00 commit).
- Observed tip at last read: `279e8b19c51658bfd05b9e31a1c0894ab2e70537`
  (commit 2026-10-20T16:21:51-03:00). The tip advanced while this seat read; every live
  command below records the bytes it actually saw.
- C3 freeze commit: `a1140e76fffdc1be032d9d813dbb686157803bbc` (15:57:44-03:00), parent of
  `4f6c73f`, ancestor of both tips.

## Verdict (short)

- **Raw log, `t1250-vet` [OBSERVATION]:** one `Go analysis failure`
  (`ghidra.log:186`), one `Invalid index: 13902080` (`:229`), **zero** `Unable to read past
  EOF` reads, route `info` at `1.25.0` (`:181-182`), zero WARN/fallback/untested/bootstrap
  lines. Exactly the D-label failure the frozen prediction expected in kind.
- **Frozen prediction compare [OBSERVATION]:** **7/8 fields match, 1 mismatch.** The only
  mismatch is `extra.invalid_index_reads`: predicted
  `[13902080, 852107777, 1801722468838924630]`, observed `[13902080]` — a proper subset
  missing `852107777` and the walk index `1801722468838924630`. `compare.py` exits **1**,
  `all_match:false`. There is **no exact full-list match**, and the integrated record says so.
- **Frozen mechanism rule, log clause [OBSERVATION + rule text]:** **holds.** Observed set
  `{13902080}` is inside the frozen H1 list, contains the H1-only value `13902080`, contains
  no index outside the frozen list, and all seven non-D logs show zero Go analysis failures.
  The observation is discriminating (not `h0_consistent`: it is not the walk index).
- **Frozen mechanism rule, binding clause [OBSERVATION]:** **red at the delivered revision.**
  `receipt-validate.py --require-mid-maps` exits 1 on the vet receipt — and on all eight —
  with exactly two findings on `receipt-validate.py`'s **own pinned bytes** (expected
  `70672eb3…`/46047 B, actual `6afb7ef6…`/52682 B at tip `279e8b1`). The carrier, retained
  log, route and mid-map checks pass (366 checks). At run time the pinned bytes were
  `70672eb3…` (`producer.json`, `pins_post`), so the pin was true at 16:06–16:07; every
  later edit of the validator invalidates the self-pin.
- **Net:** on the bound log the mechanism verdict is **confirmed**; under the frozen rule's
  literal text at the delivered revision the label is **not counted (gate red)**. Both are
  true simultaneously and must be reported separately. The integrated knowledge note is
  calibrated about the compare mismatch and the full-list falsification; it discloses the
  expected post-edit validator flag in its `recheck:` line, but the `8 valid` validation it
  cites is a **run-window** green whose restore mechanism its retained JSONs do not record.

## 1. Raw-log evidence (the authority for the outcome)

Commands run from `LANE/.ufo/waves/round-19`, exit code after each:

```
$ sha256sum runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log
a5de762231722468bcf265d5cd13ad9669f3a6d59a2746c73373e18a1a1a79c2; exit=0
$ wc -l runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log
282; exit=0        # 37,973 bytes, final byte is LF (not torn)
$ grep -c 'Go analysis failure'  …/ghidra.log        -> 1; exit=0
$ grep -c 'Invalid index:'       …/ghidra.log        -> 1; exit=0
$ grep -c 'Unable to read past EOF' …/ghidra.log     -> 0; exit=1 (grep: no match)
$ grep -c 'Falling back'         …/ghidra.log        -> 0; exit=1
$ grep -c 'Untested Go version'  …/ghidra.log        -> 0; exit=1
$ grep -c 'Using Go API snapshot for' …/ghidra.log   -> 2; exit=0
$ grep -c 'Missing Go bootstrap' …/ghidra.log        -> 0; exit=1
$ grep -c ' ERROR '              …/ghidra.log        -> 1; exit=0
$ grep -c ' WARN '               …/ghidra.log        -> 0; exit=1
```

Exact anchors (1-based lines, verbatim text):

- `:185` `INFO  (GolangSymbolAnalyzer) Go version 1.25.0`
- `:186` `ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException`
- `:206` `at …rtti.GoTypeManager.markupGoTypes(GoTypeManager.java:153)`
- `:207` `at …plugin.core.analysis.GolangSymbolAnalyzer.added(GolangSymbolAnalyzer.java:146)`
- `:229` `Caused by: java.io.EOFException: Invalid index: 13902080`
- `:230` `at …MemoryByteProvider.ensureBounds(MemoryByteProvider.java:302)`
- `:235` `at …rtti.GoName.readStructure(GoName.java:94)`
- `:241` `at …rtti.GoRttiMapper.getGoName(GoRttiMapper.java:1074)`
- `:242` `at …rtti.GoRttiMapper.resolveNameOff(GoRttiMapper.java:1063)`
- `:243` `at …rtti.GoName.getPkgPath(GoName.java:124)`
- `:276` `INFO  (HeadlessAnalyzer) REPORT: Analysis succeeded for file: file:///tmp/kr17-rea-hpk8tp2n/rea-ghidra-CSKBVG/target-9b9d776e7569.bin`

Route lines `:181-182` are both INFO from the two components, no WARN:

```
2026-10-20 16:06:19 INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0
2026-10-20 16:06:19 INFO  (GoRttiMapper) Using Go API snapshot for version 1.25.0
```

Independent re-parse (raw log, not `compare.json`):

```
$ python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log
exit=0
invalid_index_reads=[13902080]  eof_reads=[]  snapshot_labels=["1.25.0"]
snapshot_route="info"  untested_versions=[]  missing_bootstrap=false
analyzer_errors=["Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException"]
classification="snapshot_loaded"  log_sha256=a5de7622…
```

All 14 parser-owned fields compared equal to `runs/t1250-vet/observation.json`
(`invalid_index_reads`, `eof_reads`, `snapshot_labels`, `snapshot_route`,
`untested_versions`, `missing_bootstrap`, `analyzer_errors`, `symbol_analysis_failures`,
`classification`, `log_sha256`, `go_version_logged`, `invalid_version_strings`,
`mapper_errors`, `bootstrap_attempts`; script exit 0). The observation is a faithful parse
of these bytes.

Binding of the retained log to the run and carrier [OBSERVATION]:

- `:46` `INFO  (HeadlessAnalyzer) IMPORTING: file:///tmp/kr17-rea-hpk8tp2n/rea-ghidra-CSKBVG/target-9b9d776e7569.bin`
- `:59` `Loading file:///tmp/kr17-rea-hpk8tp2n/rea-ghidra-CSKBVG/target-9b9d776e7569.bin?MD5=26b91e58c33520c18d25f300ebb82f72...`
- `sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet` →
  `9b9d776e7569c910de714790a1b9bab1287b49fdc210973158f3076cee683bf7` (exit 0), the
  prediction's carrier sha256 and the receipt's `sha256_pre`/`sha256_post`; md5
  `26b91e58c33520c18d25f300ebb82f72` equals the log's `Loading …?MD5=` value.
- The `/tmp/kr17-rea-…` root is `carrier-run.py`'s `tempfile.mkdtemp(prefix="kr17-rea-")`
  (`.ufo/waves/round-17/tools/carrier-run.py:301`), not a round-17 log: timestamps
  16:06:16–16:07:06 -03 bracket the vet run window in `runs/run-log.txt`
  (`t1250-vet start 16:06:14`, `end 16:07:07`), and the target name embeds vet's sha prefix.
- Receipt recorded retained-log digest `a5de7622…`, 37973 B — equal to the bytes hashed here.
  Receipt sha256 `6e9ad99e641942e0187131a596b973482afce42ddda3ef38b99d3a33c8098403`;
  observation sha256 `071f1ba891a3ea1fafbc9315676d51302fb9e461e1db9cb4c107bc774ba40a57`.

## 2. Frozen prediction: exact comparison

Prediction integrity [OBSERVATION]:

```
$ git log --oneline --diff-filter=A -- .ufo/waves/round-19/predictions/t1250-vet.prediction.json
a1140e7 round-19: frozen C3 predictions and decision rule …
$ git show a1140e7:.ufo/waves/round-19/predictions/t1250-vet.prediction.json | sha256sum
b49702371a57bf97746669b3cda26b1a642ae04bf99604bc8f656d0b73fbf38a
$ sha256sum .ufo/waves/round-19/predictions/t1250-vet.prediction.json
b49702371a57bf97746669b3cda26b1a642ae04bf99604bc8f656d0b73fbf38a
$ git diff --stat a1140e7 279e8b1 -- .ufo/waves/round-19/predictions/   # empty, exit 0
```

`predictions/SHA256SUMS` carries the same `b4970237…`; `decision-rule.json` hashes
`3d94a7c0fc92d9af71fd3d670349acd18ce4b9ad6ccfa161b406a23d6620c8f8` both at `a1140e7` and in
the worktree. The freeze (15:57:44) precedes the first run (15:57:51) and vet's analyze step
(16:06:14) [OBSERVATION, `runs/run-log.txt`].

Replay of the comparison tool from raw-parsed observation:

```
$ python3 -I -B .ufo/waves/round-17/tools/compare.py \
    --prediction predictions/t1250-vet.prediction.json \
    --observation runs/t1250-vet/observation.json
all_match=false … extra.invalid_index_reads match=false; exit=1
```

| Field | Predicted | Observed | Match |
|---|---|---|---|
| `untested_version` | `null` | `[]` | yes (contains-or-both-empty) |
| `snapshot_label` | `"1.25.0"` | `["1.25.0"]` | yes (request echo, non-discriminating) |
| `missing_bootstrap` | `false` | `false` | yes |
| `snapshot_route` | `"info"` | `"info"` | yes (GoApiSnapshot component only) |
| `fallback_to` | `null` | `[]` | yes |
| `extra.analyzer_errors_contain` | `"Go analysis failure"` | `"Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException"` | yes |
| `extra.eof_reads` | `[]` | `[]` | yes |
| `extra.invalid_index_reads` | `[13902080, 852107777, 1801722468838924630]` | `[13902080]` | **no** |

**Exact match: no.** The mismatch is set-level: observed is a proper subset of two of the
three predicted values; nothing observed lies outside the prediction. The run aggregate is
`aggregate exit=1` in `runs/run-log.txt`, never a clean 8/8 full-match pass [OBSERVATION].

Snapshot identity binding [OBSERVATION]: the receipt pins
`…/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json` at
`54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`/10081618 B, exactly the
prediction's `selection.base.sha256`/`size`. The log prints the label (`1.25.0`), not the
file digest; the file identity link is the pin, not log text.

## 3. Frozen mechanism rule: both clauses

Rule keys from `predictions/decision-rule.json` [OBSERVATION of the file]:

- `confirmed`: "every D label's bound ghidra.log reports a Go analysis failure whose Invalid
  index value(s) include at least one `h1_only_invalid_indexes` value and no index outside
  the frozen H1 list, AND every non-D label shows no Go analysis failure".
- `h0_consistent`: only the walk index (both-hypotheses value).
- binding gate: `receipt-validate.py --require-mid-maps` exits 0, log's carrier sha256 equals
  the prediction's, prediction blob unchanged from the freeze commit.
- `diagnostic_set_D = ["t1250-vet"]`; `h1_only_invalid_indexes["t1250-vet"] =
  [13902080, 852107777]`; `walk_invalid_indexes_both_hypotheses = [1801722468838924630]`.

Set arithmetic on the raw log (`python3` over `ghidra.log`, exit 0):

```
observed       = {13902080}
frozen_all     = {13902080, 852107777, 1801722468838924630}
observed ⊆ frozen_all            -> True
observed ∩ h1_only               -> {13902080}   (non-empty)
observed − frozen_all            -> {}           (no unpredicted index)
missing vs predicted             -> {852107777, 1801722468838924630}
h0_consistent (only walk index?) -> False
```

Non-D census over the other seven raw logs (`for d in runs/t1250-*`, per-log grep, exit 0):

| Label | `Go analysis failure` | `Invalid index:` | `Unable to read past EOF` | snapshot INFO lines | `Falling back` / `Untested` |
|---|---|---|---|---|---|
| asm | 0 | 0 | 0 | 2 | 0 / 0 |
| cgo | 0 | 0 | 0 | 2 | 0 / 0 |
| compile | 0 | 0 | 0 | 2 | 0 / 0 |
| cover | 0 | 0 | 0 | 2 | 0 / 0 |
| go | 0 | 0 | 0 | 2 | 0 / 0 |
| gofmt | 0 | 0 | 0 | 2 | 0 / 0 |
| preprofile | 0 | 0 | 0 | 2 | 0 / 0 |
| **vet** | **1** | **1** | **0** | 2 | 0 / 0 |

So the rule's **log clause is satisfied**: the D label fails with an H1-only index and no
outside index; all seven non-D labels are silent in the frozen predicate's terms.

**Binding clause [OBSERVATION]** — live validator, two byte states observed while the tip
advanced:

```
# at tip d0690fd (validator = blob c24c3dc, 9276b198…/51075 B)
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-19/runs/t1250-vet/receipt.json; exit=1
# at tip 279e8b1 (validator = blob cae3ec8, 6afb7ef6…/52682 B)
$ sha256sum .ufo/waves/round-17/tools/receipt-validate.py
6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762; exit=0
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
    .ufo/waves/round-19/runs/t1250-vet/receipt.json; exit=1
counts={'invalid':1,'receipts':1,'unreadable':0,'valid':0}; checks_performed=366
findings: sha256_mismatch / size_mismatch on
  /…/.ufo/waves/round-17/tools/receipt-validate.py
  expected 70672eb3bd0c… / 46047 B; actual 6afb7ef6600c… / 52682 B
```

Restricting to the freeze-revision validator does not rescue it, because the check rehashes
the path as it exists now:

```
$ mktemp -d; git show a1140e7:…/receipt-validate.py > $d/receipt-validate.py
$ git show a1140e7:…/pins.py > $d/pins.py
$ sha256sum $d/receipt-validate.py   -> 70672eb3… (producer bytes)
$ python3 -I -B $d/receipt-validate.py --require-mid-maps …/t1250-vet/receipt.json
exit=1, same two findings (actual then 9276b198…, i.e. the tip bytes at that moment)
```

All eight receipts fail identically (`for r in runs/t1250-*/receipt.json`, exit 0 collector;
each validator call exit 1): one `sha256_mismatch` + one `size_mismatch`, same path. The
validator's own docstring states the limitation: it "proves only that the recorded digests
match the bytes present NOW". The only pinned path that no longer matches is the validator
itself; carrier, log, mid-map and pin-compare checks produce no findings.

**Consequence, stated exactly:** the log clause yields **confirmed**; the binding gate as
written yields **red at the delivered revision**, so under the literal rule `t1250-vet` does
not "count" at the tip, while the run-window record does (see §4). This is not a defect in
the log evidence; it is a rule/tool-pin artifact.

## 4. The retained run-window validation and what it can prove

`evidence/receipt-validation/t1250-vet.json` (sha256 `eeae8a29f183…`, mtime
2026-10-20T16:07:56.465-03:00 — 49 s after the vet run ended, 81 s before commit `4f6c73f`):

```
exit=0; counts={'invalid':0,'receipts':1,'unreadable':0,'valid':1}
checks_performed=366; findings=[]; pins_path=/tmp/pins.py; require_mid_maps=true
```

`producer.json` records the run-time validator hash `70672eb3…` (same value as the receipt's
`pins_post` and the `a1140e7` blob `bf04388`). Therefore at run time the self-pin was true
and a validation would pass; at every later revision the same validation is red.

What the retained JSON does **not** carry: the validator binary's own digest, or the mechanism
by which the pinned path held producer bytes. The green does prove the pinned path matched its
recorded `70672eb3…`/46047 B at 16:07:56 — the same recompute check that fires today passed
then, and `checks_performed` is also 366, equal to today's run. The integrated note's sentence
— "with the producer's original receipt-validate.py bytes restored at its recorded path during
validation" — is consistent with the mechanics but is not confirmed or refuted by the cited
JSONs; the 16:07:56 mtime cannot distinguish "the LANE working tree still held producer bytes"
from "producer bytes were restored". The note's `recheck:` line does disclose the expected
post-edit flag and instructs reconstructing the `a1140e7` producer bytes before replay; that is
the correct limitation to state. The **frozen rule text** contains no such exception.

## 5. Why only one of three predicted indices appears (INFERENCE)

All of the following linking steps are **INFERENCE** except the quoted log lines and
emulator JSON values:

- The emulator (`predictions/swiss-misread/t1250-vet.json`, exit 0 read) predicts H1
  map-path failures at three descriptors, in the order it lists them:
  `7793536 *types.valueMap -> 13902080`, `7793792 *types.opPredicates -> 852107777`,
  `7793920 *types.nodeSet -> 852107777`; H0 has no `per_type` failure; the walk index
  `1801722468838924630` is predicted under **both** (`walk.failed.h0=h1=true`).
- The observed value `13902080` is exactly the **first** H1 failure, and the log stack shows
  the failure inside `GoTypeManager.markupGoTypes` (`:206`) reached through
  `GoName.getPkgPath` (`:243`) → `resolveNameOff` (`:242`) → `getGoName` (`:241`) →
  `GoName.readStructure` (`:235`) → `ensureBounds` (`:230`). `getPkgPath` is the field the
  emulator marks as misread (`pkg_path` under the H1 uncommon placement).
- The analyzer aborts at the first `IOException`: exactly one failure record, one ERROR line,
  no second attempt, no later `Invalid index`, and the stack escapes `markupGoTypes` into
  `GolangSymbolAnalyzer.added:146`, which is where the single failure is logged. Hence the
  later predicted reads (and the shared walk failure) are **unreachable**, which is why a
  subset is observed rather than the full list.
- Ghidra's type list is address-sorted (emulator basis cites
  `GoTypeManager.java:263-269`), and `7793536 < 7793792 < 7793920`, so `*types.valueMap` is
  the earliest H1 failure — the one an abort-on-first-failure would surface.
- The log does **not** name `*types.valueMap` or its address: `grep -c '7793536'` = 0 and
  `grep -ci '76e5c0\|0x76'` = 0. The descriptor-to-value link remains byte-decode inference
  from the frozen emulator, not an analyzer statement.

This also explains the compare mismatch without excusing it: `compare.py`'s
`extra.invalid_index_reads` is exact list equality (`compare.py:212-216`), so an abort-induced
subset is a mismatch by construction; the frozen rule's confirmation predicate is set
membership, which is why the rule can be confirmed while the full-list prediction is
falsified. Both statements are in the integrated note and both match the raw log.

## 6. Freshness / calibration findings (falsification targets)

1. **The binding gate is unstable by construction at any later revision.** The receipt pins
   the validator that validates it. Observed byte states: `70672eb3…`/46047 (producer,
   `a1140e7`), `9276b198…`/51075 (`4f6c73f`..`d0690fd`), `6afb7ef6…`/52682 (`279e8b1`).
   A live `--require-mid-maps` run is red at every post-run revision, on every C3 receipt,
   with only the two self-pin findings. The frozen rule's "exits 0" cannot be met at the
   delivered tip without restoring producer bytes; the rule text should name the run-window
   validation and the producer-byte reconstruction, as the knowledge note's `recheck:` line
   already does (append-only amendment, not written by this seat).
2. **The integrated note's vet statements are calibrated [OBSERVATION].** It reports compare
   exit **1**, states the only mismatch is `extra.invalid_index_reads` with the exact frozen
   and observed lists, says the mechanism verdict is confirmed *because* the index is H1-only
   and the seven non-D carriers are silent, and says the full-list prediction is falsified
   ("never call this 8/8 exact prediction success"). Each statement matches this independent
   parse. It also labels the abort explanation INFERENCE and the descriptor identity as
   inference — consistent with §5.
3. **Its `8 valid` sentence is weaker than it reads.** The retained JSONs record counts,
   `pins_path=/tmp/pins.py`, `checks_performed=366` and no tool digest; they cannot
   substantiate *which* validator bytes produced the green, and they postdate the runs by
   only ~49 s but predate the first integrated validator blob. Report it as a run-window
   green with a producer-byte dependency, not as a tip-green.
4. **Polling-copy limit [OBSERVATION, receipt-declared].** `log_capture_limit` says lines
   written after the final poll can be missing; final copy 19:07:07.283Z, analyze step ended
   19:07:07.784Z, last log line 16:07:06. The failure at 16:06:20 and its stack are far
   inside the copied window, so no outcome field depends on the missing tail; tail
   completeness after the final poll is unverified.
5. **Concurrent writers observed, unused.** While this seat read, an untracked
   `runs/pass2/t1250-go/` appeared (16:22, `analyze.json` empty, one 84 KB `ghidra.log`) and
   the tip advanced `d0690fd` → `279e8b1`. No pass2 evidence was used; this verdict rests on
   the frozen pass1 record (`a1140e7` freeze; runs 15:57:51–16:07:07). A second pass, if it
   becomes C3 evidence, is outside the frozen-prediction comparison as recorded.

## 7. Remaining unknowns

- Which validator bytes produced the retained 16:07:56 green (no digest in the JSON);
  producer-byte restoration vs pre-edit working tree is unresolved from artifacts.
- Tail completeness of the retained log after the final poll (not needed for this verdict).
- Descriptor identity `*types.valueMap` ↔ `Invalid index: 13902080` and the abort/order
  explanation are byte-decode inference, not log statements.
- No claim about recovery quality, carrier execution, other Go versions, or a full 8/8 exact
  prediction match.

## 8. Answer to the assigned question

- **Exact match against `predictions/t1250-vet.prediction.json`: no.** 7/8 fields match; the
  invalid-index list is a proper subset (`13902080` only); `compare.py` exit 1.
- **Frozen mechanism rule:** the **log-side confirmation clause holds** (H1-only index, no
  outside index, seven non-D logs silent; not `h0_consistent`); the **binding clause is red
  at the delivered revision** solely because the receipt pins the validator's own bytes and
  the validator changed after the run. Under the literal frozen rule the label counts only
  under the run-window validation (`evidence/receipt-validation/t1250-vet.json`, exit 0,
  366 checks), not at the tip. The integrated knowledge note's vet outcome is calibrated on
  all substantive points; the gap is between the frozen gate text and the post-run tool
  revisions, and it applies to all eight C3 labels, not vet alone.
