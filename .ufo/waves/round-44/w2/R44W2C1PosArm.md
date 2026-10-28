# R44W2C1PosArm — the positive control arm (R44-CL3): scored falsification

Seat: `R44W2C1PosArm` (wave 2, round 44). Fleet identity `kaidoku`, lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Measured revision under test: `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`.
Freeze: `c48f8a4bfd449300c975668e59aae5b5538b6a84`.
Counter under test (bytes identical at freeze and at the measured revision):
`tools/round-44/c1-counter.py`, sha256
`9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993`
(`git show 55bcce69:tools/round-44/c1-counter.py | sha256sum` = same value).

**Verdict in one line.** The CTL-C1-POS arm reaches `carriers_matched 4`, exit 0 in its sandbox
only with receipts produced by real REA runs that the control itself captured; it does **not**
show that a self-consistent *authored* envelope is sufficient. A scored probe run at
`55bcce69` shows that the counter-time REA rerun **is** live in the scored path and stops a
census-only authored envelope, but a **projection-matched authored envelope passes every carrier
clause** — so R44-CL3 is confirmed, not closed, at the measured revision.

All paths absolute. Nothing in the lane, the fleet root, a sibling lane, `MANIFEST.json`,
`.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, `templates/` or `scripts/` was written or
mutated. Lane `HEAD` stayed `8bb1090af3fef64477c4337855e4347472db2701` throughout (read-only
`git rev-parse`/`status`/`show`/`log` only). The only git mutations were inside my own scratch
clone `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/sandbox` (asserted
`git -C … rev-parse --show-toplevel` = that directory before `add`/`commit`; inline throwaway
identity `w2-R44W2C1PosArm <posarm@example.invalid>`, no config written).

## 1. How CTL-C1-POS is actually constructed

`tools/round-44/c1-controls.py:925-999` (`control_pos`) does four things:

1. `capture_real(...)` for each scored carrier (`c1-controls.py:927-955`) — a **real** REA 6.5.0
   `extract-firmware` run in `.ufo`/scratch, captured as a receipt-shaped `data` object
   (`c1-controls.py` `capture_real`, and the captured summary in
   `.ufo/waves/round-44/controls/pos/receipt.json` `captured[]`).
2. Rewrites `parameters.output_directory` to
   `/fast/scratch/hyaku/kaidoku-r44/c1-controls-pos/<id>/extract`
   (`c1-controls.py:940-944`) and re-mints the evidence id over that rewrite
   (`c1-controls.py:956-970`).
3. Plants the wave-1 C1 landing docs (`_doc_landing`) so the five documentation bindings are true.
4. Commits all of it in a `git clone --shared` sandbox (`c1-controls.py:984-986`) and scores it.

Its own recorded run (`.ufo/waves/round-44/controls/pos/counter.json`) is
`carriers_matched 4`, `met_target true`, `exit_code 0`, every carrier `matched true` with
`projection_ok true` and `run_provenance_ok true`.

Two consequences this seat records as facts, not opinions:

- **POS proves reachability, not authorship.** Every receipt POS plants is the output of a real
  `extract-firmware` invocation; the control, not the lane, ran it. The counter cannot tell who
  ran it — `run_provenance_ok` reads one path substring (see §5).
- The POS docstring is wrong about its own plant:
  `tools/round-44/c1-controls.py:929-933` says “`parameters.output_directory` names the round-44
  evidence path, which is what the provenance binding reads”, while the observed
  `output_directory` in `.ufo/waves/round-44/controls/pos/receipt.json` is
  `/fast/scratch/hyaku/kaidoku-r44/c1-controls-pos/v1le/extract` (scratch form, exactly what
  `c1-controls.py:940-943` writes). Defect D5 below.

## 2. Probe design (one clone, one counter, baseline vs mutated)

Scratch: `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/` (`TMPDIR` set there; `--work`
dirs under it). One live clone: `git clone --shared <lane> $S/sandbox`, detached at
`55bcce69`. Baseline = the clone at `55bcce69` itself (the four committed real receipts).
Mutated = one commit on top of `55bcce69` that replaces **two** of the four receipt blobs with
envelopes I authored from the frozen oracle census and the extracted member bytes — no REA run
at authoring time, no use of `c1-run.sh`, no lane write:

- `v1le` — **variant A (census-only)**: published files/sizes/sha256 from
  `tools/round-44/carriers.json`, laid out by the frozen
  `c1-controls.envelope()` builder under `firmware.bin_extract/`, plausible scratch
  `output_directory` `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/rea-out/v1le`, evidence
  id re-minted with the frozen vendored `xpin-attribute.mjs` (the same rule the counter
  recomputes). This is the CTL-C1-2 construction, one carrier only.
- `v1be` — **variant B (projection-matched)**: variant A plus the projection-visible fields an
  author can derive without running REA — `mime_type` from the member name (all three are
  `text/plain`), `md5`/`sha1` computed from the `unsquashfs`-extracted member bytes, the
  per-file `HashReport` rows under `raw_result.report`, one derivation edge per published file
  (`$output/firmware.bin_extract` → `$output/firmware.bin_extract/<rel>`, `handler: null`),
  `coverage: complete`, `published_bytes: 20`. The envelope *schema* was read from the committed
  `after.json`; every value in it was derived from the census and the member bytes.

Builder: `.ufo/waves/round-44/w2/artifacts/R44W2C1PosArm/author.py` (sha256
`eba0294f…f6cdf2`). Authored receipts:
`authored-v1le-after.json` sha256 `181307d4…0ce3`,
`authored-v1be-after.json` sha256 `f0e2a7d7…69f4`.
Pre-commit self-check with the counter's own `projection()`/`projection_diff()` gave
`v1le projection_equal_to_real=False diff_keys=['files','derivations']` and
`v1be projection_equal_to_real=True diff_keys=[]`.

Mutating commit: `d503bc7ea6fbfe4ee78bf1375a015d42c4d02f7a` on top of `55bcce69`
(2 files changed; only `corpus/evidence/round-44/c1/{v1le,v1be}/after.json`). The other two
receipts (`v2le`, `v2be`) are the committed real ones and stay in place as an in-run control.

## 3. Scored results

### 3.1 Baseline — pristine `55bcce69`

```
/usr/bin/python3 -I -B tools/round-44/c1-counter.py \
  --root /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/sandbox \
  --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/work-base \
  --json-out /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/artifacts/score-pristine.json
```

exit **1**, wall **7.117 s**, stdout sha256 `eea45d37…cac9f8d`, stderr empty.
Receipt: `score-pristine.json` sha256 `05d77794…758c74`.

`carriers_matched 4`, `met_target false`, `failing []`,
`bindings_false ["province_core_section","province_core_row","frontier_note"]`.
Per carrier `matched true`, `projection_ok true`, `run_provenance_ok true`,
`evidence_id_ok true`, `output_directory /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/…`.
This reproduces `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` clause-for-clause (same
counter sha; the difference is only the scratch `--work` path).

### 3.2 Mutated — `d503bc7e` (two authored receipts)

```
/usr/bin/python3 -I -B tools/round-44/c1-counter.py \
  --root /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/sandbox \
  --rev d503bc7ea6fbfe4ee78bf1375a015d42c4d02f7a \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/work \
  --json-out /fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/artifacts/score-authored.json
```

exit **1**, wall **7.127 s**, stdout sha256 `7e4970a8…e15516a`, stderr empty.
Receipt: `score-authored.json` sha256 `4e6f29fe…ed2176`; `--verify-receipt` on it exits **0**
(`detail: ok`).

| carrier | receipt source | `matched` | stopping clause | other clauses |
|---|---|---|---|---|
| `v1le` | **authored, census-only** | **false** | `projection_ok false`, `projection_diff ['files','derivations']` | all other 21 clauses **true** |
| `v1be` | **authored, projection-matched** | **true** | none (`projection_diff []`) | all 22 clauses **true** |
| `v2le` | committed real | true | none | all true |
| `v2be` | committed real | true | none | all true |

`carriers_matched 3`, `met_target false`, `failing ["v1le:projection_ok"]`,
`bindings_false ["province_core_section","province_core_row","frontier_note"]` (the honest-stop
doc shape, unchanged by the probe).

For `v1be` the accepted receipt sha256 is `f0e2a7d7…69f4`; the real receipt it replaced at
`55bcce69` was `facc57d9…b347`. `evidence_id_ok true` with
`evidence_id ev_82bc977d…6675`, minted from the authored bytes. The full clause vector is in
`score-authored.json` `carriers.v1be`.

The observed census-only diff is exactly the shape CTL-C1-2 records
(`.ufo/waves/round-44/controls/c2/counter.json`): `files` differ in `mime_type`/`md5`/`sha1`
columns (`committed_only [None,None,None]`, `fresh_only [text/plain, md5, sha1]`), and
`derivations` counts `[1, 4]` — the fresh run records one derivation edge per published file,
the census-only envelope records only the input→chunk edge.

## 4. Is the counter-time REA rerun in the scored path at `55bcce69`? Yes — live, not disabled

- `projection_ok` is one of the 22 `CLAUSES` (`tools/round-44/c1-counter.py:338-344`) and
  `matched` requires every clause true (`c1-counter.py:2134-2138`).
- It is evaluated by a **real** runner for every carrier whose receipt is present and whose pin
  is OK (`c1-counter.py:2099-2112`): `make_real_runner(...)` (`:1859-1915`) spawns
  `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output` on the carrier bytes,
  replaying `max_depth`/`max_output_bytes`/`max_output_files` from the receipt, then compares
  `projection(committed)` against `projection(fresh)`.
- It cannot be switched off in a scored run: `--no-rerun` short-circuits to exit **2**
  `rerun_disabled` (`c1-counter.py:2360-2363`). Observed:
  `NORERUN_EXIT=2` with
  `{"detail": "R44-C1 binds a fresh REA run of each carrier; --no-rerun cannot be scored", "reason": "rerun_disabled"}`
  (`norerun.json` sha256 `6763b099…6ab5`, stdout sha256 `cae5e464…a503`).
- The dev arm skips it (`dev_arm` sets `projection_ok None`, `c1-counter.py:2114-2115`), but the
  measured run is not a dev arm: the baseline carrier rows show `projection_ok true`, not
  `null`.

So at `55bcce69` the rerun is in the scored path and is the binding that stops variant A.

## 5. R44-CL3 answer: a self-consistent authored envelope **is** sufficient for the carrier clauses

Score, not opinion:

- **No** — an oracle-census-only authored envelope is not sufficient. `v1le` is red on
  `projection_ok` only (`files`, `derivations`), every other clause green.
- **Yes** — an authored envelope that reproduces the projection passes **all 22** carrier clauses
  (`v1be: matched true`, `projection_ok true`, `projection_diff []`, `evidence_id_ok true`),
  although no REA run produced those committed bytes. The receipt was written by my `author.py`
  and committed in `d503bc7e`; the only REA invocations in the run are the counter's own reruns,
  which merely *confirm* the authored projection.

That is R44-CL3 (`corpus/lessons/round-44.md` `## Routed defects`) at `55bcce69`, in the same
form round 43 found: the counter-time rerun narrows fabrication to “must project like a real run”
but cannot distinguish an authored receipt from a captured one. `projection_ok` proves
projection equality, not provenance — exactly debt D-13 / R40-CL2.

Related mechanism evidence (not needed for the verdict, but it bounds what “fresh” means):
`receipt_fresh` is a property of the **path's first add**, not the current blob
(`c1-counter.py:2080-2084` `first_add(...)`). In the probe, both mutated receipts report
`receipt_fresh true` with `receipt_first_add fee6e98a454859ba2d12cda8d45de833fb0950a5` while
their bytes were written by `d503bc7e`. `corpus/evidence/round-44/c1/` is not in the counter's
frozen paths (`c1-counter.py:272-283` `FROZEN_PATHS`/`FROZEN_PREFIXES`), so a post-freeze receipt
rewrite is invisible to the freeze walk; only projection equality constrains it. Defect D4.

## 6. Claim-text vs instrument (supports R44-CL2; recorded because the arm depends on it)

`plans/round-44-claims.md:34-35` (the controls amendment) requires
“the receipt's `parameters.output_directory` must name a `corpus/evidence/round-44/c1/` path and
the evidence id must be minted over that path”, while the predicate
(`plans/round-44-claims.md:137-139`) requires the same field to name the `/kaidoku-r44/` scratch
segment. The counter implements only the second: `provenance_ok` (`c1-counter.py:1176-1182`)
checks “absolute” + literal `PROV_SEGMENT = '/kaidoku-r44/'` (`:258`) + no `..`.

Direct probe (exit 0, printed):

```
True  /fast/scratch/hyaku/kaidoku-r44/c1-controls-pos/v1le/extract
False /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/c1/v1le
True  /fast/scratch/hyaku/kaidoku-r44/corpus/evidence/round-44/c1/v1le
False /fast/scratch/hyaku/kaidoku-r42/x
```

Consequences for the record, verified rather than inferred:

- At `55bcce69` the counter's exit **1** is produced by three *documentation* bindings
  (`province_core_section`, `province_core_row`, `frontier_note`) — the Core row that existed at
  `4cc1ac11` is absent at `55bcce69` because the honest-stop landing replaced it. It is **not**
  produced by any receipt clause: all four receipts are `matched true`, `run_provenance_ok true`.
- At `4cc1ac11` the same frozen counter reported `met_target true`, `exit_code 0`,
  `bindings_false []` (`corpus/evidence/round-44/c1/counter-at-4cc1.json`). The honest stop is
  therefore a prose decision about the frozen claim's intent, not an instrument red — which is
  what `PROVINCE.md:428` and `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:6-9,161-162`
  say. The stated reason is accurate; this seat confirms it and pins the counter-side numbers.

## 7. M44-2 / freeze defect (contract item 3) — verified

- Inherited `c86ea508188c50e2645b1f9bba65df4177cda6b1` writes the 8 control-fixture files listed
  in `.ufo/waves/round-44/l1/preflight-c86ea508.json` `blob_changed`, all under the frozen
  `tools/round-44/` directory pathspec.
- `tools/round-45/frozen-path-preflight.py` **really catches it**. Observed, read-only on the
  lane:
  - `--freeze c48f8a4… --rev c86ea508… --pathspec tools/round-44/` → exit **1**,
    `blob_changed` = the 8 files, `verdict frozen_path_changed`
    (`preflight-c86.json` sha256 `15566303…6e38`);
  - same invocation without `--pathspec` → exit **1** as well (empty pathspec makes it flag
    every touched path in `FREEZE..REV`);
  - `--rev 55bcce69…` → exit **0**, `{"blob_changed": [], "touched": [], "verdict": "clean"}`
    (`preflight-55.json` sha256 `fd301ffb…ad2e`).
- The frozen counter at the lane tip still exits **2** `frozen_path_changed` with the same 8
  paths (`tip-c1.json`, `tip_c1_exit=2`), so “the round measures at `55bcce69` and says so” is
  the admissible reading. The gate is a tool, not a hook: it works when run, and nothing in the
  repo makes it run automatically — the lesson's “wire it into the round's commit sequence”
  remains an instruction, not an enforced control.

## 8. Defects for L1 (numbered; act or explicitly accept)

**D1 — R44-CL3 is confirmed, not closed (severity: high for any provenance claim).**
Counter: `tools/round-44/c1-counter.py:2099-2112` (`projection_ok`) and `:338-344` (`CLAUSES`).
Command: the §3.2 invocation. Exit **1**; observed `carriers.v1be.matched true`,
`projection_ok true`, `projection_diff []`, `evidence_id_ok true` for
`authored-v1be-after.json` sha256 `f0e2a7d7…69f4`, authored from
`tools/round-44/carriers.json` + `unsquashfs`-extracted member bytes with no REA run.
Action: do not read `projection_ok` as “the lane ran REA”. A provenance claim needs a run
artifact the counter cannot synthesize (the claim already carries D-13; keep CL3 open).

**D2 — the frozen claim's controls amendment is not implemented anywhere (severity: high;
already routed as R44-CL2, here with a scored demonstration).**
`plans/round-44-claims.md:34-35` vs `tools/round-44/c1-counter.py:1176-1182`.
Command: the §6 provenance probe (exit **0**). Observed: committed evidence path → `False`;
`/kaidoku-r44/` path → `True`; a path containing both literals → `True`. Action: either
implement the amendment as a clause (and make it satisfiable) or delete it from the claim text
before the next freeze; as written the two provenance homes cannot both be the same field for a
real run.

**D3 — the honest-stop record names the reason but not the failing bindings (severity: low).**
`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:6-9` and `PROVINCE.md:428` say the frozen
claim's output-directory clause disagreed with the counter — true — but at the measured
revision the counter's exit 1 comes from `province_core_section`/`province_core_row`/
`frontier_note` (`score-pristine`/`score-authored`, `bindings_false`), while every receipt
carrier clause is green. Command: §3.1 invocation, exit **1**. Action: add one sentence to the
entry naming the three documentation bindings that produce the red at `55bcce69`, so a reader
does not look for a receipt failure that is not there.

**D4 — `receipt_fresh` binds the path's first add, not the bytes; receipts are not frozen
(severity: medium).**
`tools/round-44/c1-counter.py:2080-2084` and `:272-283`. Command: §3.2 invocation, exit **1**.
Observed: `v1le`/`v1be` `receipt_fresh true`, `receipt_first_add fee6e98a…` although their
current blobs were written by `d503bc7e`; `corpus/evidence/round-44/c1/` is outside the frozen
path families. Action: state in the claim that committed receipts are mutable after the freeze
subject only to projection equality, or freeze the receipt paths and require the REV blob to
equal the blob at the adding commit.

**D5 — CTL-C1-POS docstring contradicts its own plant (severity: low, but it is the origin of
the “both paths” confusion).**
`tools/round-44/c1-controls.py:929-933` says the output directory “names the round-44 evidence
path, which is what the provenance binding reads”; `c1-controls.py:940-943` writes
`/fast/scratch/hyaku/kaidoku-r44/c1-controls-pos/<id>/extract`, and
`.ufo/waves/round-44/controls/pos/receipt.json` shows exactly that scratch value. Action: correct
the docstring before the next freeze so the control does not imply an evidence-path provenance
requirement the counter does not implement.

## 9. Reproduction and artifacts

- Clone: `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/sandbox` (`git clone --shared` of the
  lane, detached `55bcce69`, then probe commit `d503bc7e`).
- Builder: `author.py`; envelopes: `authored-v1le-after.json`, `authored-v1be-after.json`.
- Receipts: `score-authored.json` (+ `.stdout` sha256 `7e4970a8…`, `.stderr` empty, `.time`
  `real 0m7.127s`), `score-pristine.json` (+ `.stdout` sha256 `eea45d37…`, `.stderr` empty,
  observed `real 0m7.117s`), `norerun.json` (+ `.stdout`), `tip-c1.json` (+ `.stdout`),
  `preflight-c86.json`, `preflight-55.json`.
- All ten artifacts are under
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w2/artifacts/R44W2C1PosArm/`
  with `SHA256SUMS.txt`.
- Restoration: the mutated tree is the scratch clone, not a lane file, and the clone is
  disposable; the before-bytes are recorded in §3.2 (`v1le eb44f3db…`, `v1be facc57d9…`) and
  remain reachable at `55bcce69`. The scratch tree
  `/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm/` was deleted after the artifacts were
  copied out (seat self-check: no leftover tree).
- Tooling: none installed or upgraded (pacman is paused host-wide; nothing was needed —
  `unblob 26.6.4` at `~/.local/bin/unblob`, `sasquatch 4.5.1`, `unsquashfs 4.7.5`,
  `npx` under the frozen fixed PATH, `rea-agents@6.5.0` at the recorded npx cache root).
- Pre-existing lane worktree state, not mine: `git status` in the lane showed
  ` M corpus/lessons/round-44.md` and untracked `.ufo/waves/round-44/l1/*` files before this
  seat ran; none were touched. `HEAD` stayed `8bb1090`.
