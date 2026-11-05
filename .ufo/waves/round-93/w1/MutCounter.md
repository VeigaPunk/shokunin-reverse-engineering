# MutCounter — mutation-kill of the round-93 counters (seat report)

Lane `kaidoku`, round 93, attempt 1. Declaration commit `92a240521bd1bf2213b75d18d9b176a8dafdc67c`.
Counter pins verified before any run: `tools/round-93/stop-boundary-repair-battery-v3.py`
`60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3` (matches claims.json), `tools/round-93/craft-citation-semantic.py`
`34cf6579…ffedf05340` (matches). Round-92 imports (`stop-boundary-repair-battery.py` `63e9df43…`,
`stop-boundary-battery-v2.py` `f6ddb48b…`) and the honest repair `upx-stop-boundary-search-repair.py`
(`ce1b1769…`) match. Machine-readable record: `mutants.json`.

## Headline

1. **Frozen-counter defect (blocks the R93-C1 positive receipt).** `stop-boundary-repair-battery-v3.py --json-out`
   crashes with `TypeError: Object of type bytes is not JSON serializable` at `fresh_cells[].output` whenever a
   fresh cell is **repaired**, which is the honest positive control. The receipt is left truncated
   (`…"output": ` then EOF) and exit is 1. The label line still prints (met True, exit 0) without `--json-out`.
   The frozen positive command includes `--json-out`, so its receipt cannot land and the claim's kill rule
   "any receipt missing" fires. Forgery receipts are unaffected (no repaired bytes, so the dump succeeds).
   The probe receipt `pre/probe-v3-F1-unscored.json` did not hit this only because F1 refuses both fresh near cells.
   Named need: a successor counter (a new declaration, not a re-edit of the frozen one) whose receipt serialises the repaired bytes (hex or length plus digest).
   Not fixed here.
2. **The fresh-roundtrip clause is redundant on this host.** `repaired` in `fresh_arm` means `out == packed1`
   exactly, and the roundtrip is computed on that same `packed1`. Under the pinned packer the roundtrip is therefore
   true by construction (fresh-roundtrip 2 of 2 in every honest run). It only detects a broken `upx -d`. The
   held-out power of the arm comes from the nonce-marked fresh bytes, not from the roundtrip.
3. **Nonce secrecy is the whole held-out property, and no atom measures it.** With a constant nonce (M2) the
   honest-repair label still reaches the frozen expect; only a forger that pins the constant-nonce fresh image
   (F4) distinguishes the two (see M2). Provenance atoms (marker present/absent, determinism, collision) do not
   check nonce freshness.
4. **Depth counter gaps.** The frozen 10-case selftest has no zero-citation case (C2 survives the selftest), and
   the two shape clauses in C3 are redundant (`len(body) >= 3` is implied by `len(rows) >= 4`).

The R93-C2 candidate (block 32 + QUALITY row 188 applied to a scratch copy) passes the frozen after-manifest.

## Results

### v3 (R93-C1) — frozen expect `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`

Controls (frozen counter, unmutated):

| control | command | observed | exit |
|---|---|---|---|
| positive (honest repair) | `python3 -I -B tools/round-93/stop-boundary-repair-battery-v3.py --root <clone> --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work <s>/work/honest2 --rev 92a24052 --expect '<FROZ>'` | `repaired 12 of 12; … fresh-roundtrip 2 of 2 met True` | 0 |
| positive with `--json-out` | same + `--json-out <f>` | **TypeError bytes not JSON serializable**; truncated receipt | 1 |
| F1 table5-window | `--repair-cmd <controls>/table5-window.py` | `repaired 10 of 12; … intact 5 of 6; … fresh-roundtrip 0 of 2 met False`; both fresh near cells `refused` (json receipt written) | 1 |
| F2 carrierread5 | `--repair-cmd <controls>/carrierread5.py` | `repaired 10 of 12; … intact 6 of 6; … fresh-roundtrip 0 of 2 met False`; both fresh near `refused` (json receipt written) | 1 |
| F3 identity_noop | `--repair-cmd <controls>/identity_noop.py` | `repaired 0 of 12; … met False` | 1 |

Forgery F1/F2 are therefore **rejected** by v3 (the calibration claim's target holds). The F3 control is rejected.
The positive control is met (label, stdout), but not as a receipt file (see headline 1).

Mutants (full pipeline unless noted; `<mut-tree>` = scratch tree whose `tools/round-93/` holds the mutant and
whose round-87/88/91/92 entries symlink the clone):

| id | mutation (exact old→new in mutants.json) | observed | verdict |
|---|---|---|---|
| M1 | fresh arm replaced by an empty stub | `repaired 10 of 10; … intact 5 of 6; … fresh-roundtrip 0 of 0` met False exit 1 | **killed** (label) |
| M2 | `secrets.token_hex(8)` → `"0"*16` | plain: met True exit 0 (**survives the frozen label**). F4 forger (pinned to the constant-nonce fresh image): orig exit 1 (`repaired 10 of 12; intact 5 of 6; fresh-roundtrip 0 of 2`), M2 exit 0 (`repaired 12 of 12; intact 6 of 6; fresh-roundtrip 2 of 2`) | **killed by F4 only** — not an accepted survivor: the constant nonce makes the held-out source public and forgeable |
| M3 | `prov["deterministic"] = packed1 == packed2` → `True` | plain survives (host packer deterministic; `/usr/bin/upx` is sha-pinned, so a non-deterministic packer is not craftable). Injected second pack differs by one byte: orig `unevaluable='fresh provenance atoms failed'`, M3 proceeds (4 cells) | **killed by injection** (fresh_arm() call, monkeypatched `v2.pack`) |
| M4 | `collides_public_packed` → `False` | plain survives (no real collision craftable: nonce random, carriers pinned). Injected public set = fresh digest: orig `unevaluable` (collides=True), M4 proceeds (4 cells) | **killed by injection** |
| M5a | failed roundtrip not reclassified (`class = class`) | plain: met True (roundtrip always true on host). Injected `roundtrip_sha → None`: orig `repaired 10 of 12; fresh-roundtrip 0 of 2` exit 1; M5a `repaired 12 of 12; fresh-roundtrip 0 of 2` exit 1 | **killed** (label differs: 12 vs 10) |
| M5b | M5a + `roundtrip_ok` counts `class == "repaired"` | plain: met True. Injected `roundtrip → None`: orig exit 1, M5b `repaired 12 of 12; fresh-roundtrip 2 of 2` met True exit 0 | **killed by injection**; near-equivalent on this host (the injected state is unreachable under the pinned packer, see headline 2) |
| M6 | `label == expect` → `expect in label` | forged expect = frozen label minus the roundtrip clause, honest repair: orig met False exit 1; M6 met True exit 0 | **killed** (forged expect) |
| M7 | `fresh_intact_ok = 1` | plain: met True (identity true on honest). Injected fresh intact answered with altered bytes: orig `intact 5 of 6` met False exit 1; M7 `intact 6 of 6` met True exit 0 | **killed by injection** (wrapper alters only the sha-matched fresh intact input; everything else delegated to the honest repair) |

Mutant-tree receipts are in `receipts/v3/` (`plain-*.out/.err/.rc`, `inj-*`, `forged-*`, `f4-*`).

Rerun notes for M2 and the F4 forger: the F4 control is `harness/f4.py` (five public pinned images plus the
fresh image for nonce `"0"*16`, window-matched like `table5-window.py`). Its orig run and M2 run use the same
harness (`harness/inject.py --mode f4`).

### craft-citation-semantic (R93-C2)

Frozen controls (unmutated):

| check | command | observed | exit |
|---|---|---|---|
| before, base | `craft-citation-semantic.py --root <clone> --manifest manifests/block31-before.json --block 31 --worktree` | `QUALITY 169 lacks ['never refuse an intact input', "packer's verdict"]` | 1 |
| after, candidate | `… --root <cand> --manifest manifests/block32-after.json --block 32 --worktree` | `ok` | 0 |
| after, base clone (kill-rule check) | `… --root <clone> --manifest manifests/block32-after.json --block 32` | `block 32 missing (craft has 31 blocks)` | 1 |
| before, candidate (history kept) | `… --root <cand> --manifest manifests/block31-before.json --block 31` | same atom as base | 1 |
| wrong-citation fixture (block 32 row 3 cites 169) | `… --root <fix-wrong> --manifest manifests/block32-after.json --block 32` | `QUALITY 169 lacks ['exactly one candidate', "packer's own verdict"]` | 1 |
| selftest | `--selftest --work <s>/work/st-frozen` | `SELFTEST cases=10 failures=0` | 0 |

Candidate = `git archive` of the declaration commit plus the drafts applied in scratch: `block32-draft.md`
inserted after SKILL.md line 766 (before `## Config custody for live-probe rounds (SOP)`, now line 778), and
`row188-draft.md` appended to `corpus/QUALITY.md` (line 318). Diffs: `candidate/draft-apply-*.diff`. Both drafts
validate: block 32 is ok on the candidate (4 rows, all keyword atoms), and the criterion column resolves to 176,
178, 184 and 188, each containing its keyword.

Mutants (each checked against the frozen-expected behaviour):

| id | mutation | frozen behaviour | mutant behaviour | verdict |
|---|---|---|---|---|
| C1 | `missing = []` (keyword atom dropped) | block31-before exit 1; fix-wrong exit 1; kwless manifest exit 1 | block31 exit 0; fix-wrong exit 0; kwless exit 0. C1 selftest FAILS (keyword-miss want 1 got 0; cited-row-missing) — so it is **not runnable as the frozen counter** | **killed** |
| C2 | zero QUALITY citations accepted (`if not m: … continue`) | fix-nocite (no `QUALITY N` in row 3) exit 1 (`names 0 QUALITY citations, expected 1`) | exit 0 | **killed by the real fixture only**; C2 passes the frozen 10-case selftest (gap) |
| C3 | shape floor 4→3 rows, 3→2 body rows | selftest shape case (gamma, 2 body rows) exit 1 | selftest FAIL shape want 1 got 0 (1 failure). Real block32 (4 body rows) exit 0 for both | **killed by selftest** |
| C4 | marker atom dropped | badmarker manifest exit 1 | exit 0; selftest FAIL marker-missing | **killed** |

Checker receipts: `receipts/chk/`.

## Accepted survivors

None. Every mutant is killed; the four that the honest-repair path does not reach (M3, M4, M5b, M7) are killed by
injection and are labelled as such in `mutants.json`. The frozen-checker selftest does not kill C2 (killed only by
the real fixture), which is recorded as a gap rather than an accepted survivor.

## Recommendations for the L1 (no counter was edited)

- Do not land the v3 positive receipt through `--json-out` under the frozen counter; it cannot produce a file for
  a repaired fresh cell. Needs a successor counter (new declaration) or the L1 must record the label line only and
  state that the receipt is absent.
- Consider stating in the claim that the fresh-roundtrip clause is redundant under the pinned packer, so the
  "fresh-roundtrip 2 of 2" label is not counted as independent evidence.
- Add a zero-citation case to the C2 selftest; drop one of the two redundant shape clauses in C3.

## Method and bounds

- Clone: `git clone --shared -q <lane> <S>/clone && git -C <S>/clone checkout -q 92a24052`. The clone was not
  edited; all shas unchanged after the runs (`34cf6579…`, `60026511…`).
- Scratch trees (not the lane): `mut-tree/` (round-93 files plus symlinks to the clone's round-87/88/91/92 tools),
  `cand-tree/` (archive plus drafts), `fix-wrong/`, `fix-nocite/`, `controls/` (copies of the three forgery
  controls with `ROOT` pointed at the clone; the lane originals are unchanged).
- The first mutant batch was discarded: my `mut-tree` linked round-87/88/92 but not round-91, which the round-92
  repair imports, so every repair call exited 1 and all results were refusals. Fixed by linking all sibling
  tool dirs; the batch was rerun in full. Results above are from the rerun only.
- Fast path: none needed. The full v3 pipeline runs in about 5 s, so every mutant was run with the frozen expect
  and the honest repair. Injection harness used only where the frozen path cannot reach the mutant
  (`harness/inject.py`).
- Tools: no installs. `/usr/bin/upx` 5.2.0 (existing, sha-pinned by the counter), python3 3.14. No pacman, no
  sysctl, no ~/.local/bin changes, no lane writes (read-only git and reads only).
- Scratch `$HYAKU_SCRATCH/kaidoku-r93/MutCounter` is removed after the copy below.

## Files written (seat `.ufo/waves/round-93/w1/MutCounter/`)

- `MutCounter.md` (this report), `mutants.json` (12 records with exact old/new strings, commands, expected, observed, verdict, reason, controls, and the json-out defect)
- `mutants/` — v3 mutants `M1.py`…`M7.py`, `orig-v3.py`; checker mutants `C1.py`…`C4.py`, `orig-craft-citation-semantic.py`
- `harness/` — `run-v3.sh` (batch), `inject.py` (in-process injections, same harness for honest and mutant), `f4.py` (constant-nonce forger)
- `receipts/` — `v3/` (stdout/stderr/rc for every v3 run), `chk/` (checker runs and selftests), `crash-json-out/` (the `--json-out` TypeError trace and truncated receipt), top-level control and candidate outputs
- `candidate/` — `draft-apply-SKILL.diff`, `draft-apply-QUALITY.diff`
- `controls/` — `table5-window.py`, `carrierread5.py`, `identity_noop.py` (ROOT set to the scratch clone)
