# R44W2C1ReceiptAudit — receipt-content audit of the four C1 after-receipts, plus the C1/C2 verdicts, the record, and the M44-2 gate

Seat `R44W2C1ReceiptAudit`, round 44 wave 2 (falsification). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84`,
measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`, base
`c29360e3ba5381a5ab69e372d0d9577970f85018`, lane tip at dispatch
`c86ea508188c50e2645b1f9bba65df4177cda6b1`; HEAD while auditing is `8bb1090a` (the
lesson/LOG/SCORECARD/QUALITY record commit).

**Citation discipline.** Every doc citation below is to a **committed blob**, read with
`git show <rev>:<path>`, not to the mutable worktree: `PROVINCE.md` and `corpus/README.md` at `HEAD`
(`8bb1090a`), the knowledge entry at `55bcce69`, and `corpus/lessons/round-44.md` at `HEAD`
(blob sha256 `d48af63c72b52b68be11607c1a5b9bfb812e551acf5ea59d2edeb29447837cb0`). The worktree copy of
the lesson was being rewritten by a sibling while I audited (`git status` shows it modified,
`+43/−11`, mtime `11:27:18`); its line numbers are not stable and I quote none of them.

**Scope.** I audited the four committed `after.json` receipts *as data*, independent of
`tools/round-44/c1-counter.py`
(`corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}/after.json`), against the frozen oracle
(`tools/round-44/carriers.json`, `corpus/evidence/round-44/oracle/`), then re-ran both frozen counters
and the round-45 frozen-path gate first-hand. I changed no claim, no counter, no rubric, no frozen
byte and no production doc. Everything is measured now or cited from a committed artefact;
`[INFERENCE]` marks reasoning no measurement backs.

## Verdict table

| # | attack | verdict |
|---|---|---|
| 1 | four receipts publish the oracle file set (path, sha256, size) | **CONFIRMED** — exact, no extras, all four carriers |
| 2 | handler is exactly `squashfs_v1` / `squashfs_v2`, never a prefix | **CONFIRMED** — one chunk per receipt, exact string, in `chunks[]` and in every `ChunkReport` |
| 3 | `gaps` / `unpublished_entries` empty | **CONFIRMED** — `extraction_gaps`, `unpublished_entries`, `diagnostics`, `depth_limited_paths`, `extraction_continuations` all `[]` |
| 4 | evidence id recomputes under the frozen 6.5.0 rule | **CONFIRMED** — all four, under both pins |
| 5 | `subject.digest` == carrier pin | **CONFIRMED** — all four, and `normalized_result.selection.sha256` too |
| 6 | R44-C1 verdict at `55bcce69` | **CONFIRMED** — `carriers_matched 4`, `met_target false`, exit 1 (reproduced) |
| 7 | the stop is the only *correct* reading | **CONFIRMED on the literal text**; **not** the only *passing* reading (§3.3) |
| 8 | the record says exactly that | **FALSIFIED** — no committed prose carries `met_target false` / exit 1 at the measured revision (§3.4, D4) |
| 9 | R44-C2 at `55bcce69` | **CONFIRMED** — 80/80, `mismatches []`, `unevaluable []`, `frozen_path_changed []`, exit 0 (reproduced) |
| 10 | C2 vacuity / free-pass / note-vs-value | **NOT FALSIFIED** (§4) — but C2's freeze walk is narrower than the claim (D10) |
| 11 | M44-2 honest and sufficient | **HONEST, NOT SUFFICIENT** (§5, D5, D6) |
| 12 | `tools/round-45/frozen-path-preflight.py` really catches it | **YES for the M44-2 shape and for A/D/restore; NO for a frozen path outside the supplied `--pathspec`** (§5.2) |

## 1. Receipt-content audit (the four after-receipts)

Anchored bytes (sha256 of the audited receipts):

```
eb44f3db017337dbd9aca2af800a312de343bbffd902e8fb196d030064d90abf  v1le/after.json
facc57d94d86c3e2ac9673896e3d7d8e929246a417c1ba03c48a3bc786c3b347  v1be/after.json
162e69b2931c40dc3e35fbfd0e90c604f7fd991269c008f1d246c4a7e2a9b993  v2le/after.json
18839471ce3b8494e15a0460984445f6a1e63adcbb70c9954ce7b463daa66550  v2be/after.json
```

### 1.1 Published set == oracle

The oracle member table was taken from three frozen sources and cross-checked: `carriers.json`
`carriers[].oracle.members`, `carriers[].oracle.output_tree.members`, and the committed tree under
`corpus/evidence/round-44/oracle/**`. All three agree for all four carriers (3/3/4/4 members). The
receipt's `relative_path` was then stripped of the chunk-extract-root segment (`firmware.bin_extract`)
— the normalisation `extract_rel` uses at `tools/round-44/c1-counter.py:1361-1376` — and compared as an
exact `(path, sha256, size)` triple:

| carrier | handler | published / oracle | set equal | extra | published_bytes | oracle `output_tree_digest` recomputed |
|---|---|---|---|---|---|---|
| v1le | `squashfs_v1` | 3 / 3 | yes | none | 20 (=6+7+7) | `8faae7739b14315c10683db41d63b92f511ec8e73ec94e6cc74bc414894f2a48` = frozen |
| v1be | `squashfs_v1` | 3 / 3 | yes | none | 20 | same digest = frozen |
| v2le | `squashfs_v2` | 4 / 4 | yes | none | 28 (=7·4) | `4178bb8379de3e5573eb448010d1c309fcda4dcb6bb4fd16ab11b4ab0535f947` = frozen |
| v2be | `squashfs_v2` | 4 / 4 | yes | none | 28 | same digest = frozen |

Member digests (identical in both byte orders of a version — the fixtures are built that way):

```
v1  apple.txt   303980bcb9e9e6cdec515230791af8b0ab1aaa244b58a8d99152673aa22197d0  6 B
    banana.txt  5a81483d96b0bc15ad19af7f5a662e14b275729fbc05579b18513e7f550016b1  7 B
    cherry.txt  86baf3529da550a44b0681ffa031b6b676e620e9e06dc5ac1119d0cd21cbcf55  7 B
v2  apple1.txt  6181259c6b2ca629a56920b422e9a8f212a4d0bcead923df92dbd66fbb7e1c30  7 B
    apple2.txt  919fc82d6f1031d305dbce2fc5a74a6df5ddf2da472ee4d137c681cef28d4aff  7 B
    apple3.txt  2d95014ed3f24e86ce5fc3a4529f057d7b2318d9b24b54f2e9476b154bd21ec6  7 B
    apple4.txt  08d9b05b15b998f2dbc741399fef4350c7863cc85df2305d7da4e83e8c8a959d  7 B
```

Each `files[].path` is segment-bounded under `normalized_result.output_directory`
(`…/rea-out/firmware.bin_extract/<name>`), `relative_path` is the remainder, `reported_sha256 ==
sha256`, and every `size` matches the file. `chunks[0]` is one chunk over the whole image (`offset 0`,
`length 4096`), `encrypted false`, `extraction_failed false`, `coverage complete`. Every path the
receipt normalises is a legal spelling — `files[].relative_path` is relative, the `derivations[]` edges
use the `$output/` sigil and `$input` as the format intends, and no component is empty, `.`, `..` or
trailing-slash — so `path_shape_ok` holds independently of the counter.

### 1.2 The committed copy of the produced tree

The predicate also claims "the runner binds the scratch-produced tree to the verbatim committed copy
under `corpus/evidence/round-44/c1/`". I read those trees directly: for all four carriers,
`corpus/evidence/round-44/c1/<id>/firmware.bin_extract/*` hashes **byte-identically** to the frozen
oracle members (3/3 and 4/4, zero extras, zero missing). The claim is true of these four receipts.
What is *not* true is that any instrument checks it — **D2**.

`after.json` is value-identical to `envelope.json["data"]` for all four (JSON equality, not a
re-serialisation): the runner inserted, defaulted and dropped nothing. `manifest.json`'s per-carrier
`stdout_sha256` (`54493a8c…`, `3e03c3a0…`, `b8867486…`, `99d0ef76…`) equals the sha256 of the
committed `stdout.log`, and `stdout.log` is byte-equal to `envelope.json`. `extract-tree.tsv` agrees
with `normalized_result.files` (relpath, size, sha256).

### 1.3 Handler, evidence id, subject, toolchain

- **Handler.** `normalized_result.chunks[0].handler` and every
  `raw_result.report[*].reports[ChunkReport].handler_name` is exactly the frozen string —
  `squashfs_v1` ×2, `squashfs_v2` ×2. One chunk each; no `squashfs_v2_nonstandard`, no `squashfs_v3*`,
  no prefix form anywhere.
- **Evidence id.** Recomputed with the counter's own recipe — `node <freeze>:tools/round-27/xpin-attribute.mjs
  --pkg65 <6.5.0 root> --pkg67 <same> <{'data': after.json}…>`, i.e. the frozen tool
  (`XPIN`, `tools/round-44/c1-counter.py:261`, frozen at `:282`) and the pinned package root
  (`tools/round-42/rea-pkg.json`: `package.json` sha256 `a500302319c1214a…0a6c` = live,
  `package-lock.json` `d42d56f0f4f8baf3…c6ca` = live). All four store the id the 6.5.0 rule mints; the
  6.7.0 attribution is `both` because the counter passes `--pkg67 pkg65` by design:

  ```
  v1le  ev_26c313fc4e9964583f21af3d85b3e51f8cdddbb5f501b251d7cdf2e28e8144e2  both
  v1be  ev_e7e3a71fc622b962a0b9c6c5a17f663416f7e7de9917eb6f2b35f3dc5cdcdc44  both
  v2le  ev_603145b213b57f57a2c25cfd3661deb9a449af110f11f1c622e18b085192fed2  both
  v2be  ev_89b83ee76bbc55a588d00493b432dc5d87c2e92e31d01fcb5a034b00f9e9ee5e  both
  ```

- **Subject.** `subject.digest.sha256` and `normalized_result.selection.sha256` both equal the carrier
  pin (`b45925fa…3e71`, `529e1077…31e6`, `7c62dbe3…f124`, `79c0f388…fcc0`) in all four receipts.
- **Honest producer text.** The BE receipts preserve `file(1)`'s wrong token verbatim
  (`"Squashfs filesystem, big endian, version 2.0, uncompressed"` on v2be) instead of laundering it
  into `compressed` — the R44-CL5 hazard recorded correctly; the counter binds compression from the
  inode-table metadata block, never from that text.
- **Toolchain identity**, re-measured live against `carriers.json.toolchain`: `/usr/bin/unsquashfs`
  `461e1fd9…b1677c` (4.7.5), `/usr/bin/7z` `f802383f…3ad4` (26.04), `sasquatch` `ad02d27a…4754`
  (4.5.1), `sasquatch-v4be` `fac88740…14c6`, unblob `0ce7b624…1d09` (26.6.4). All five match.
  Each `unblob.log` shows the real `sasquatch -le|-be -no-exit-code -f -d …` invocation, no warning,
  no error, no skipped-chunk line — consistent with `diagnostics == []`.

### 1.4 Extras at the receipts root (D1)

`corpus/evidence/round-44/c1/` also carries two counter outputs, neither an REA receipt, neither
marked as belonging to a stopped claim:

- `corpus/evidence/round-44/c1/counter-at-4cc1.json` — the C1 counter score at `4cc1ac11` with
  `met_target: true`, `exit_code: 0`.
- `corpus/evidence/round-44/c1/c2-score-9d3d.json` (753,998 B) — the **C2** counter score at
  `9d3d1862` with `met_target: true`, `exit_code: 0`.

A reader who opens the C1 evidence directory finds a green C1 score for the claim the round declares
stopped. No counter reads the directory, so no score is affected.

**No carrier-level defect found: no extra published file, no missing oracle file, no digest or size
mismatch, no handler prefix, no gap, no diagnostic, on any of the four receipts.**

## 2. What the counter says — reproduced from this seat

| revision | exit | `carriers_matched` | `met_target` | `bindings_false` | `failing` | `frozen_path_changed` |
|---|---|---|---|---|---|---|
| `55bcce69` (measured) | **1** | 4 / 4 | **false** | `province_core_section`, `province_core_row`, `frontier_note` | `[]` | `[]` |
| `4cc1ac11` (C1 landing) | **0** | 4 / 4 | **true** | `[]` | `[]` | `[]` |

Every per-carrier clause is `true` for all four carriers at `55bcce69`: `handler_ok`,
`oracle_hits_ok`, `gaps_ok`, `evidence_id_ok`, `projection_ok` (a live REA 6.5.0 re-run whose semantic
projection equals the committed receipt), `path_shape_ok`, `run_provenance_ok`, `subject_pin_ok`,
`receipt_fresh`, `tree_ok`. This reproduces `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`
(same exit code, same three bindings).

**The red at `55bcce69` is not the provenance clause.** The only failing bindings are the three
*documentation* bindings: the `## Round-44 additions to Core` section and row were withdrawn
(`province_core_rows_seen: []`), and the honest-stop frontier note at `PROVINCE.md:430` omits the entry
stem the binding requires. There is no receipt-side clause that could fail on provenance —
`run_provenance_ok` is `true` precisely because the receipts carry the scratch form.

## 3. R44-C1: is the honest stop the right reading, and does the record say so?

### 3.1 The contradiction is real and is unsatisfiable as written

- `plans/round-44-claims.md:34-35`: "the receipt's `parameters.output_directory` **must name a
  `corpus/evidence/round-44/c1/` path** and the evidence id must be minted over that path".
- `plans/round-44-claims.md:138`: "the receipt's `parameters.output_directory` **names this round's
  `/kaidoku-r44/` scratch segment** and the evidence id is minted over that provenance".

Measured against the counter's own predicate, `provenance_ok` (`tools/round-44/c1-counter.py:1176-1184`):

```
'/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out'         -> True
'/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/c1/v1le'    -> False
'corpus/evidence/round-44/c1/v1le'                                                   -> False
```

The committed-path form cannot pass the counter's clause, and the scratch form cannot satisfy line 34's
"must name". **No receipt can satisfy both frozen sentences.** That is `R44-CL2`
(`git show HEAD:corpus/lessons/round-44.md`, line 57). The stop is therefore correct, and no Core row is
claimed at the measured revision: `PROVINCE.md:424` at `55bcce69` is
`## Round-44 measured, not promoted (R44-C1 honest stop)`, and `## Round-44 additions to Core` is
present only at the withdrawn landing commit `4cc1ac11` (1 occurrence) and absent at `55bcce69` and at
HEAD (0 occurrences each).

### 3.2 The counter cannot see the contradiction

`BINDINGS` (`tools/round-44/c1-counter.py:334-337`) has no clause for the committed-path form, and
`failing_lists` only reports `CLAUSES`/`BINDINGS`. Consequence, measured: **the same four receipts score
exit 0 / `met_target true` at `4cc1ac11` and exit 1 / `met_target false` at `55bcce69`**, and the
difference is entirely whether the Core-row prose is present. The green at `4cc1ac11` is a *check-pass
that violates the frozen text*, not evidence that the claim was met — debt D-16 ("check-pass ≠ truth")
and D-23 ("receipt-derived verdicts not re-executed").

### 3.3 The stop is the only *honest* reading, not the only *passing* one

`provenance_ok` is a **substring** test (`PROV_SEGMENT in output_directory`, `:1180`). Measured:

```
'/fast/scratch/hyaku/kaidoku-r44/corpus/evidence/round-44/c1/v1le/rea-out'           -> True
```

That one path satisfies both frozen sentences to the letter — absolute, contains `/kaidoku-r44/`, and
names a `corpus/evidence/round-44/c1/` path — while being a scratch path, not the committed one.
Nothing in either instrument would notice, and the "runner binds the copy" clause is unchecked anyway
(D2). So the stop holds **because the L1 refused a legalistic dodge**, not because the instruments
forced it. The record should say that; as written it implies the instruments forced the stop.

*(A sibling has reached the same conclusion and the uncommitted lesson text now carries it as a
qualifier to R44-CL2 — "a substring-shaped scratch path … passes both prose clauses and the counter —
a loophole, not a legitimate route". My measurement is independent confirmation, not a competing
claim.)*

### 3.4 The record does not say exactly that (D4)

Measured on the committed lesson blob (`git show HEAD:corpus/lessons/round-44.md`,
sha256 `d48af63c…7cb0`):

```
grep -c "met_target\|carriers_matched\|4cc1" → 0
```

`exit 1` occurs once, inside `M44-2`'s phrase "instead of `0/1`", i.e. as the code that was *expected*
at the tip — never as the C1 verdict at the measured revision.

- `corpus/lessons/round-44.md` (HEAD, line 16) states the tip's exit 2 for the freeze violation and the
  title states "measured 4/4 but not promoted", but **nowhere states that the C1 counter exits 1 with
  `met_target false` at the measured revision**, and nowhere names the three red bindings.
- `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:3-9` (at `55bcce69`) reads: "The counter
  returned `carriers_matched 4/4`, **exit 0** at revision `4cc1ac11…` … However, the frozen claim
  required `parameters.output_directory` under `corpus/evidence/round-44/c1/`, while the frozen
  counter requires the `/kaidoku-r44/` scratch provenance segment." Substantively correct about
  *why*, but it cites a **different revision from the round's measured one** and the only exit code in
  the record is **0**.
- `PROVINCE.md:428` and `corpus/README.md:104,224` say "counter matched 4/4 … not promoted", again with
  no exit code.

The qualitative record is right everywhere; the quantitative record shows a `0` for a claim that
stopped. Under the semantic exit codes (0 met / 1 red / 2 could-not-evaluate) the measured-revision
code is `1`. Fix: one sentence in the entry and the lesson — "at `55bcce69` the frozen counter exits
**1**, `carriers_matched 4`, `met_target false`, red bindings
`province_core_section`/`province_core_row`/`frontier_note` (the withdrawn landing), **not** the
provenance clause; the provenance contradiction is documentary and no instrument evaluates it." The
second half matters: attributing the exit 1 to provenance would be a fresh error.

## 4. R44-C2 — confirmed, and the three attacks fail

**Confirmed first-hand** (R3/R4 in §7): exit **0** at `55bcce69`, `entries_count 80`,
`entries_evaluated 80`, `mismatches []`, `unevaluable []`, `frozen_path_changed []`, `met_target true`,
`wall_seconds 4.65`; `counter_sha256 == counter_sha256_at_freeze == 085192ea…c277`,
`rubric_sha256 == rubric_sha256_at_rev == e8cc0ded…e755e`.

- **Vacuity.** Run the same rubric at BASE without the repair (`--pre-freeze --rev c29360e…`): exit
  **1**, 80 evaluated, `unevaluable 0`, mismatches exactly `C2-a1-owned-coverage-count`,
  `C2-a2-owned-depth-count`, `C2-a4-owned-depth-craft-range`. The rubric reds on exactly the three
  statements the claim repairs, and only at BASE. Nothing is dropped into `unevaluable`; the 10
  `dropped` surfaces are outside a re-derivable value and each carries a stated reason.
- **Free pass.** Three routes, none lands. (a) `asserted` is the *derived* value, not the file's value:
  `C2-a1` asserts `137/137` where `SCORECARD.md:23` carries `133/133`; `C2-a2` asserts `21/21` where
  `:24` carries `20/20`; `C2-a4` asserts `81-543` where `:24` carries `81-449` — measured `observed`
  at REV is `137/137`, `21/21`, `81-543`, and the appended `c2-correction-value:` lines agree with the
  derivation (they are compared, not trusted: a disagreeing note yields `UNSUPPORTED:<note value>`,
  which is what CTL-C2-4 exercises). A rubric authored from the file (asserted `133/133`) would have
  red as `137/137 ≠ 133/133`, so the authorship path the sentinel guards against is closed.
  (b) `check_script_sha256` is enforced, not decorative: `tools/round-44/c2-counter.py:940-960`
  recomputes sha256 of the `-c` payload and returns `script_pin_mismatch` on drift. (c) All 80 entries
  carry a concrete `mutation_witness` with `verdict: fails-as-required` and the resulting
  `UNSUPPORTED:<mutated value>` observation (e.g. `C2-a4`: `81-449`→`81-999`).
- **Note vs value.** Real: CTL-C2-4 replaces the bound `c2-correction-value:` line with
  `81-543 [WRONG]`; the enforced arm exits 2 `frozen_path_changed` on `SCORECARD.md` and the scored arm
  leaves the entry a mismatch (`arm_A_passed false`, `arm_B_passed false`). A note is never evidence.
  Naming drift only: the claim names a diagnostic `note_value_disagrees` that is emitted nowhere
  (`grep -c` → 0 in `tools/round-44/c2-counter.py` and in `tools/round-44/c2-rubric.json`); the
  mechanism is the generic `UNSUPPORTED:` observation (D8).

Controls are committed and green: `.ufo/waves/round-44/w1/artifacts/R44C2Controls/receipts/real-base/summary.json`
→ `verdicts {CTL-C2-0…4: ok}`, with the control counter/rubric sha256 equal to the frozen files
(`085192ea…`, `e8cc0ded…`). C1's controls are likewise committed and `as_expected`
(`.ufo/waves/round-44/controls/summary.json`, CTL-C1-0…5 + POS, `kill_rule_fires false`).

**But `frozen_path_changed []` at `55bcce69` certifies far less than the claim's freeze clause (D10).**
C2's frozen set is `frozen_paths ['SCORECARD.md','SHONEN.md','SKILL.md']` + `frozen_dirs ['tools/round-44']`
(`tools/round-44/c2-rubric.json`; `C2_DEFAULT_FROZEN` at `tools/round-44/c2-counter.py:134`). Against the
claim's byte-frozen list (`plans/round-44-claims.md:303-312`) C2 never walks
`plans/round-44-claims.md`, `tools/round-42/fixtures.json`, `tools/round-42/c1-counter.py`,
`tools/round-43/c1-counter.py`, the four carrier bins, `corpus/evidence/round-44/oracle/**`,
`corpus/SOURCES.md`, or the round-42/43 heldout receipt sets. This is the in-flight `R44-CL7`
(`w2/R44W2C2Freeze.md`); I confirm it independently and extend it in D10.

## 5. M44-2 and `tools/round-45/frozen-path-preflight.py`

### 5.1 The freeze violation is real, reproduced, and disclosed

`git log --oneline c48f8a4..HEAD -- tools/round-44/` → only `c86ea508`. I re-ran the gate over the
*lane's full frozen set* (not just `tools/round-44`):

| rev | gate exit | verdict | touched | blob_changed |
|---|---|---|---|---|
| `55bcce69` | 0 | clean | 0 | 0 |
| `8bb1090a` (HEAD) | 1 | `frozen_path_changed` | 8 | 8 |

The 8 paths are byte-identical at HEAD and at `c86ea508` (unrestored), and the sorted list is identical
in `c1-score-at-tip.json` (exit 2), `c2-score-at-tip.json` (exit 2) and `preflight-c86ea508.json`
(`blob_changed`): `c1 == c2 == gate`, 8 entries each.

Honest: yes — the lesson records `M44-2` with the preflight receipt as the red arm, the round measures
at a pre-violation revision and says so, and no score is claimed at the tip. Sufficient: no (D5, D6).

### 5.2 The gate catches the M44-2 shape — and passes two frozen violations (D6)

Independent fixture proof (`artifacts/R44W2C1ReceiptAudit/preflight-demo.sh`: one throwaway repo per
case under `$TMPDIR`, toplevel asserted before the first commit, never the lane):

```
clean-at-freeze                    exit=0 verdict=clean               touched=0
modify-frozen-tool                 exit=1 verdict=frozen_path_changed touched=1
add-under-frozen-dir               exit=1 verdict=frozen_path_changed touched=1
delete-frozen-tool                 exit=1 verdict=frozen_path_changed touched=1
restore-endpoints-equal            exit=1 verdict=frozen_path_changed touched=2   # log-based, not endpoints
claims-only-narrow-pathspec        exit=0 verdict=clean               touched=0   # FALSE GREEN
claims-only-right-pathspec         exit=1 verdict=frozen_path_changed touched=1
oracle-only-narrow-pathspec        exit=0 verdict=clean               touched=0   # FALSE GREEN
oracle-only-right-pathspec         exit=1 verdict=frozen_path_changed touched=1
```

`M`/`A`/`D` and change-then-restore are all caught inside a pathspec (restore is caught from the
`git log` range, matching "a later restore does not un-block"). But the gate is **pathspec-driven with
no claim-aware default** (`tools/round-45/frozen-path-preflight.py:29`; the tree backstop runs only
`if pathspec`, `:69`), and the invocation on record supplied only `--pathspec tools/round-44`. A commit
that rewrites `plans/round-44-claims.md` or `corpus/evidence/round-44/oracle/**` — both frozen by
R44-C1 — passes the gate with exit 0 and is caught only later, at scoring time, by the counter's
`frozen_drift`, which does cover the full set (`FROZEN_PATHS` `:272-283` + `FROZEN_PREFIXES` `:286`).
R44-CL1's fix is therefore strictly weaker than the instrument it front-runs: it closes the discovered
hole and leaves the same class open on every other frozen path.

## 6. Defects for L1

1. **D1 (high) — a green score sits inside the stopped claim's evidence directory.**
   `corpus/evidence/round-44/c1/counter-at-4cc1.json` (`met_target: true`, `exit_code: 0`) and
   `corpus/evidence/round-44/c1/c2-score-9d3d.json` (`met_target: true`, C2's score) are committed
   among the receipts, unmarked.
   `python3 -c "import json;d=json.load(open('corpus/evidence/round-44/c1/counter-at-4cc1.json'));print(d['met_target'],d['exit_code'])"`
   → `True 0`. Fix: move both under `.ufo/waves/round-44/l1/` (where the measured-revision receipts
   already live) or add a `README` naming the claim's stop.

2. **D2 (high) — the "verbatim committed copy" clause is unevaluated by any instrument.**
   `tools/round-44/c1-counter.py`: `grep -c "extract-tree.tsv"` → **0**, `grep -c "provenance.json"` →
   **0**, `grep -c "copied_verbatim"` → **0**. The 7 hits for `firmware.bin_extract` are the
   `chunk_dir` default in the selftest helpers (`:2577`, `:2654`) and selftest fixture literals
   (`:3098-3161`) — never a read of the committed tree. `corpus/evidence/round-44/c1` appears only at
   `:135`, `:231`, `:2334`, `:2413` (docstring/prose) and `:246` (`AFTERDIR`, the `after.json` path).
   The clause list at `:117-196` has no tree-copy clause. Observed: the committed trees are correct for
   all four receipts (my audit), but a wrong tree would still score exit 0 / `met_target true`. Fix:
   bind each `corpus/evidence/round-44/c1/<id>/firmware.bin_extract/**` blob at REV to the receipt's
   `files[]` (path, sha256, size) as a counter clause.

3. **D3 (high) — the disputed provenance field is substring-guarded and one-sided.**
   `tools/round-44/c1-counter.py:1176-1184`. Measured:
   `provenance_ok('/fast/scratch/hyaku/kaidoku-r44/corpus/evidence/round-44/c1/v1le/rea-out')` → `True`.
   The frozen claim (`plans/round-44-claims.md:34-35` vs `:138`) is unsatisfiable as written; the stop
   is correct but rests on the L1's reading, not on the instrument. Round-45 fix: make the two clauses
   one (`output_directory` under the scratch segment **and** the D2 copy binding) and make the segment
   test a path-prefix test, not a substring test.

4. **D4 (medium) — the measured-revision verdict is absent from the record.**
   `grep -c "met_target\|carriers_matched\|4cc1"` on `git show HEAD:corpus/lessons/round-44.md` → `0`;
   `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:3-9` (at `55bcce69`) quotes `exit 0` at
   `4cc1ac11`. Observed at the measured revision: exit `1`, `met_target false`, `bindings_false` =
   `province_core_section`/`province_core_row`/`frontier_note`. The uncommitted worktree lesson now
   names the red qualitatively; the code is still absent. Fix: state it, and state that the red is the
   withdrawn landing, not the provenance clause.

5. **D5 (medium) — the committed M44-2 row says "added/edited"; all eight are modifications.**
   `git show --name-status --format= c86ea508 -- tools/round-44/` → 8 × `M`, no `A`; the row's own
   cited receipt (`preflight-c86ea508.json`) records `"status": "M"` for all eight. The uncommitted
   worktree copy already rewrites the row (and drops "added/edited"); the committed text at HEAD still
   carries it. Fix: land the rewrite.

6. **D6 (medium) — the new gate's coverage is caller-chosen.**
   `tools/round-45/frozen-path-preflight.py:29` (`--pathspec`, default none) and `:69` (tree backstop
   only `if pathspec`). Measured false greens in §5.2. Fix: derive the frozen set from one declared
   source (the claim file's `## Frozen paths`, or the counter's `FROZEN_PATHS`/`FROZEN_PREFIXES`), or
   refuse to run without a pathspec that covers a declared claim.

7. **D7 (low) — exit-code asymmetry between the gate and the counters.**
   Gate: `1` on a violation (`tools/round-45/frozen-path-preflight.py:93`). Counters: `2`
   `frozen_path_changed`. A wrapper that distinguishes "red score" from "could-not-evaluate" will
   mis-classify the gate. Document the mapping or align it.

8. **D8 (low) — `note_value_disagrees` is named in the claim and emitted nowhere.**
   `grep -c "note_value_disagrees" tools/round-44/c2-counter.py tools/round-44/c2-rubric.json` → `0`,
   `0`. The behaviour is enforced through `UNSUPPORTED:` (CTL-C2-4). Rename in the claim/control text or
   emit the reason string.

9. **D9 (low) — the counter's `frontier_note` binding cannot see an honest-stop frontier note.**
   `PROVINCE.md:430` at `55bcce69` *is* a `Round-44 frontier note` naming SquashFS v1/v2, but it does
   not cite the entry stem, so the binding is `false`. For a claim that stops the note exists and is
   correct; the binding conflates "a frontier note exists" with "a promotion note cites the entry".
   Harmless at `55bcce69` (the claim is red anyway) but it would mis-grade a future stopping note.

10. **D10 (medium) — the claim's byte-frozen set is wider than either counter's freeze walk.**
    Enumerated against `plans/round-44-claims.md:303-312`:

    | claim byte-frozen | C1 counter | C2 counter |
    |---|---|---|
    | `plans/round-44-claims.md` | yes (`FROZEN_PATHS`) | **no** |
    | `tools/round-44/` (incl. `control-fixtures/**`) | yes (prefix `:286`) | yes (`frozen_dirs`) |
    | `tools/round-42/fixtures.json` | yes | **no** |
    | `tools/round-42/c1-counter.py` | yes | **no** |
    | `tools/round-43/c1-counter.py` | **no** (`grep -c` → 0) | **no** |
    | four carrier bins | yes (via `carriers[].path`) | **no** |
    | `corpus/evidence/round-44/oracle/` | yes (prefix) | **no** |
    | round-42 v3 C1 receipt inputs | **no** (`grep -c "round-42/c1/"` → 0) | **no** |
    | round-42/43 heldout receipts | **no** (`grep -c "heldout"` → 0) | **no** |
    | `SKILL.md` | **no** (`grep -c` → 0) | yes |
    | `corpus/SOURCES.md` | **no** (read at the `sourced` binding, not frozen) | **no** |
    | historical score receipts pinned in C2's rubric | **no** | yes (per-entry `subject_sha256_at_*`) |

    The 80/80 at `55bcce69` is unaffected — filtered for exactly those uncovered families,
    `git log -m --diff-merges=first-parent --name-only --pretty=format: c48f8a4..55bcce69` returns
    **no match** (rc=1) — but `frozen_path_changed []` from either counter is not a certificate for
    the claim's freeze clause. Confirms and extends the in-flight `R44-CL7`; the `corpus/SOURCES.md`
    overlap between `plans/round-44-claims.md:312` (byte-frozen) and `:318` ("NOT frozen … *for C2
    only*") is the same family.

## 7. Receipts (this seat)

All commands ran with `cwd=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, scratch
`/fast/scratch/hyaku/kaidoku-r44/R44W2C1ReceiptAudit/` (deleted before yield). Artifacts copied to
`.ufo/waves/round-44/w2/artifacts/R44W2C1ReceiptAudit/`.

| # | command (abridged) | exit | stdout sha256 | wall |
|---|---|---|---|---|
| R1 | `python3 -I -B tools/round-44/c1-counter.py --root . --rev 55bcce69… --freeze c48f8a4… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <S>/c1work --json-out …/c1-rev-55bcce.json` | **1** | `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d` | 6.98 s |
| R2 | same at `--rev 4cc1ac11…` | **0** | `8742a90d9b879fbf91f77c5862273be788911ace1d2228e79cd6b9ad2d8fee6a` | 6.90 s |
| R3 | `python3 -I -B tools/round-44/c2-counter.py --root . --rev 55bcce69… --freeze c48f8a4… --work <S>/c2work-rev` | **0** | `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3` | 4.65 s |
| R4 | same with `--pre-freeze --rev c29360e…` (CTL-C2-0 replay) | **1** | see `…/c2-base-prefreeze.json` | 4.30 s |
| R5 | `python3 -I -B tools/round-45/frozen-path-preflight.py --root . --freeze c48f8a4… --rev 55bcce69… --pathspec <full frozen set>` | **0** | see `…/preflight-full-55bcce.json` | <1 s |
| R6 | same at `--rev 8bb1090a` | **1** | see `…/preflight-full-tip.json` | <1 s |
| R7 | `bash …/preflight-demo.sh tools/round-45/frozen-path-preflight.py <out> <S>` | **0** (9 cases, 2 false greens) | `91772aefc22386fd5aeb45662925ded29be91c6c2320151aca035c53fc9abaaa` | 0.58 s |
| R8 | `node <freeze>:tools/round-27/xpin-attribute.mjs --pkg65 <6.5.0> --pkg67 <6.5.0> {v1le,v1be,v2le,v2be}.wrapped.json` | **0** | `9319d7723e75e5cc06e8955caf01e13ba3b735b603c7fbcbc527f5b4d3f33f70` | <1 s |

Read-only git only (`show`, `log`, `ls-tree`, `rev-parse`, `merge-base --is-ancestor`, `cat-file`,
`grep`, `status`, `diff`); fixture-local `git init/add/commit/rm` ran only inside `mktemp -d` repos
under the seat scratch, each with `git rev-parse --show-toplevel` asserted equal to the fixture root
before the first commit. No mutating command touched the lane, the fleet repo, a sibling lane,
`MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, `templates/` or `scripts/`. No tool
was installed or upgraded this seat; pacman was not invoked.

## 8. Residual risk and verification gaps

- **The receipts' published bytes are anchored to the committed copy and the oracle, not to the
  original scratch run.** `files[].path` names a `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…`
  directory that the seat discipline deletes. What survives is the committed tree (verified
  byte-equal to the oracle) plus the counter's live REA re-run whose projection matched — strong, but
  not process-attesting (D-13, R40-CL2). I did not attempt to forge a receipt, so "a fabricated
  receipt cannot pass" remains the claim's assertion, not my measurement.
- **The oracle cannot discriminate the two byte orders of a version.** v1le and v1be have identical
  member digests *and* identical `output_tree_digest` (likewise v2le/v2be). Carrier identity rests on
  `subject.digest`, the handler string and the superblock layout, not on the published set: a receipt
  whose published set came from the sibling carrier would still match the set comparison.
- **`tree_ok` binds the S138 `__output__` tree to the unsquashfs census, not to the receipt.** The
  receipt↔committed-tree link is unaudited by any instrument (D2); my audit covers only these four.
- **C2's 80 entries are scored, but 10 surfaces are dropped by disposition** (`dropped` D1–D10) and 77
  ids are excluded from *repair*. I verified the three target entries' `asserted`/`observed` values,
  the 80/80 fitness witnesses, script pinning, the BASE negative control and the tip freeze-drift; I
  did not re-derive every one of the 80 checks by hand. "Check-pass ≠ truth" (D-16) still applies.
- **C2's controls ran against byte-identical copies of the frozen counter/rubric** under
  `.ufo/waves/round-44/w1/artifacts/` (`085192ea…`, `e8cc0ded…` = the frozen files). I verified the
  sha equality rather than re-running the five controls; the C1 controls I read only as the committed
  summary.
- **D6/D10's uncovered-frozen-path class is demonstrated on synthetic fixtures or by static
  enumeration**, never by a real lane commit that rewrites a non-`tools/round-44` frozen path (that
  would need a mutating commit in the lane).
- **The lesson was being rewritten concurrently** (uncommitted, `+43/−11`) while I audited. My
  citations are pinned to the HEAD blob; if the rewrite changes M44-2/R44-CL2 again, re-run
  `git show HEAD:corpus/lessons/round-44.md | sha256sum` and diff the anchors above.
