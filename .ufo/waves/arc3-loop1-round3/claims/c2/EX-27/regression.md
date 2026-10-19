# EX-27 — regression: the round-2 attack matrix re-run on the revised custody tool

Seat EX-27 · chain c2 · role executor · wave `arc3-loop1-round3` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No git mutation; custody
paths read-only (sha256/stat/capture-to-scratch only); scratch under
`/var/tmp/ex27-r3` (never `/tmp`). Writes inside the repo: this artifact tree and
`seats/EX-27.md` only.

Task (seat line): *regression — re-run the round-2 attack matrix on the revised
tool (rewrite forms 13/13, v1 shapes, label-defect reproduction) — every prior
behavior must hold.*

## 0. Verdict

**All prior behaviors hold, and the four named round-2 holes now close as their
declared classes — measured, not asserted.** 41 regression rows per phase:

| phase | tool pin | rows | HOLD | FAIL | before-state observations |
|---|---|---|---|---|---|
| before (round-2 landed) | `112d01dc…` | 41 | 37 | 0 | 4 (the four hole before-states) |
| after (EX-21 revision) | `7cd19c3c…` | 41 | 41 | 0 | 0 |

- The 13 CR-4 rewrite forms reproduce **13/13 caught** on the real revised tool
  with the same verdict classes as round 2 (`REWRITE-DRIFT` 11 / `CONTENT-DRIFT`
  10), and the sha256-only view is still blind on exactly the same-content
  subset (8 of the 13). Five extra forms (same-content truncate-restore +
  touch-forgery + hardlink variants, chmod-only, delete-after-capture) hold
  their classes too → 18/18.
- v1 shapes and the label-defect reproduction are **field-for-field unchanged**:
  round-1 canonical stanza and pipe sidecar still read
  `LABEL-DEFECT` (4/4 evaluable paths + exit class per drift) with
  `SHA256-CONTRACT` intact; sums-v1, the EX-35 fixtures, and drift-free synthetic
  anchors are byte-identical across phases. The only v1-lane change is the new
  opt-in `--require-paths` flag (default exit 0 unchanged).
- Selftest 15 → 22 cases, CLEAN; the four holes: EACCES capture traceback-exit-1
  → `14` + `READ-ERROR` stanza (`verify` `UNEVALUABLE`, never `MATCH`), the
  both-sides-absent fail-open `MATCH 0` → `UNEVALUABLE 14`, live-unreadable
  traceback → `14`, write-guard clobber → refuse `USAGE 2` bytes intact,
  `selftest --scratch <missing>` traceback → `USAGE 2`.
- Live pair (fresh capture vs fresh capture of the 5 custody paths) `MATCH 5/5
  exit 0` in both phases; every receipt self-pins the tool sha that matches the
  bytes under test.

## 1. Tool pins, churn record, identity discipline

| | sha256 | bytes | note |
|---|---|---|---|
| before-state tool | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` | 39157 | round-2 landed revision; extracted read-only from `git show HEAD:…` into `tools/tool-base-112d01dc.py` (identity re-verified) |
| after-state tool | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` | 52436 | EX-21's revision; snapshot taken after 4×20 s sha stability (`churn-settle-watch.log`), re-derived equal to the live working-tree path at battery time and at write time |

Revision churn watched, not guessed: `churn-poll.log` (60 s polls) records the
tool moving `d164d49f → d9be407d → f2412aaa → 03bd6242 → 89bfebec → 7cd19c3c`
between 13:08:56Z and 13:13:31Z; `churn-settle-watch.log` shows `7cd19c3c`
stable for 4 consecutive checks from 13:14:51Z. The harness aborts if the tool
bytes move mid-run (`tool_check()`), and each phase runs against an
`outdir/tool-under-test/custody-pair.py` copy whose re-derived sha must equal the
pin (so the tool's own selftest case-7 sibling-invocation resolves).

## 2. Method

Harness: `harness/regress.py` (re-runnable; `python3 regress.py --phase
{baseline,revised} --tag <t> --tool-src <tool.py>`; ~4 s wall). Every fixture
under the phase's own scratch; every expectation derived from the round-2 record
and from live state, never hard-coded twice.

Legs and their acceptance anchors:

- **A — attack matrix** (the round-2 CR-4 `battery.py` bodies, verbatim, driven
  through the real tool): `capture → attack → capture → verify A B`. Verdict
  class expected from the content state (`sha_same` → `REWRITE-DRIFT` else
  `CONTENT-DRIFT`), plus `chmod-only → METADATA-DRIFT` and `delete →
  ABSENT` (EX-33 R-K/R-I classes). The "13/13" quantity is the CR-4 set of 13;
  5 extra forms fence the same-content class (truncate-restore, touch-forgery,
  hardlink alias) and the two boundary classes.
- **B — v1 shapes**: round-1 canonical stanza vs live, canonical-vs-fresh-v2
  (cross-format), round-1 pipe sidecar, round-1 sums, EX-35 fixtures
  (`partial-1of5`, `corrupt-sha`, `swap-sha`, `absent-path`), junk → usage, and
  three drift-free synthetic v1 anchors on a scratch fixture (stanza / sums /
  pipe) built by the harness. Real-custody expectations are **re-derived at run
  time** by `drift_reconcile()` (independent clock math + sha comparison), so
  the operator-side live drift below cannot silently move the bar.
- **C — label-defect reproduction**: v1 defect declared with the exact
  `localtime(epoch N); gmtime(epoch) is '…'` wording; v2 `MTIME_UTC_RENDER ==
  date -u -d @epoch` (no offset) and `MTIME_LOCAL_RENDER` offset-suffixed;
  TZ sweep (UTC / Asia_Tokyo / America_St_Johns) → identical UTC render.
- **D — selftest**: case count + CLEAN, and `--scratch <missing>` class.
- **E — hole probes** (before→after of the chain's named debt; scratch only):
  EACCES capture, crafted both-sides `STAT-ERROR` receipts (receipt-file
  fail-open arm), live-unreadable verify, `--paths X --out X` write-guard.
- **F — identity**: live-pair capture-vs-capture, and the receipt `# tool:`
  self-pin vs the bytes under test.

## 3. Before → after (generated by `harness/make-tables.py` from the two `regress.json`)

| row | before (112d01dc) | after (7cd19c3cfd83) | verdict |
|---|---|---|---|
| A/A1_cp_a | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A2_cp_a_remove_dest | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A3_cp_p | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A4_rsync_a_default | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A5_rsync_a_inplace | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A6_tar_restore | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A7_copy_new_then_mv | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A8_inplace_modify_no_restore | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A9_inplace_modify_then_restore | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A10_restore_bytes_plus_touch_r | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A11_hardlink_alias_restore | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A12_reflink_replace | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A13_rename_swap_pristine_hardlink | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | verdict=CONTENT-DRIFT exit=10 sha_same=no sha_only_view=caught | HOLD |
| A/A9s_truncate_restore | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A10s_truncate_restore_touch | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A11s_hardlink_truncate_restore | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | verdict=REWRITE-DRIFT exit=11 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A14_chmod_only | verdict=METADATA-DRIFT exit=12 sha_same=yes sha_only_view=BLIND | verdict=METADATA-DRIFT exit=12 sha_same=yes sha_only_view=BLIND | HOLD |
| A/A15_delete_after_capture | verdict=ABSENT exit=13 sha_same=no sha_only_view=caught | verdict=ABSENT exit=13 sha_same=no sha_only_view=caught | HOLD |
| B/r1-canonical-vs-live | exit=10 label_defect=4 sha_agree=4 | exit=10 label_defect=4 sha_agree=4 | HOLD |
| B/r1-canonical-vs-fresh-v2 | exit=10 label_defect=4 sha_agree=4 | exit=10 label_defect=4 sha_agree=4 | HOLD |
| B/r1-metadata-pipe-vs-live | exit=10 label_defect=8 sha_agree=4 | exit=10 label_defect=8 sha_agree=4 | HOLD |
| B/r1-sums-vs-live | exit=10 sha_agree=4 | exit=10 sha_agree=4 | HOLD |
| B/ex35-partial-1of5-default | exit=0 require5_supported=no | exit=0 require5_supported=yes | HOLD |
| B/ex35-corrupt-sha-vs-live | exit=10 sha_agree=3 | exit=10 sha_agree=3 | HOLD |
| B/ex35-swap-sha-vs-live | exit=10 sha_agree=2 | exit=10 sha_agree=2 | HOLD |
| B/ex35-absent-path-vs-live | exit=10 sha_agree=3 | exit=10 sha_agree=3 | HOLD |
| B/junk-receipt | exit=2 | exit=2 | HOLD |
| B/synth-v1-stanza-vs-live | exit=12 label_defect=1 | exit=12 label_defect=1 | HOLD |
| B/synth-v1-sums-vs-live | exit=0 | exit=0 | HOLD |
| B/synth-v1-pipe-vs-live | exit=12 label_defect=1 | exit=12 label_defect=1 | HOLD |
| C/v2-utc-render-correct | exit=0 | exit=0 | HOLD |
| C/v2-utc-render-tz-invariant | (3 TZ, 1 render) | (3 TZ, 1 render) | HOLD |
| C/v1-label-defect-declared | exit=10 label_defect=4 | exit=10 label_defect=4 | HOLD |
| D/selftest-existing-scratch | exit=0 cases=15 | exit=0 cases=22 | HOLD |
| D/selftest-missing-scratch | exit=1 traceback=yes | exit=2 traceback=no | HOLD |
| E/d2-eacces-capture | exit=1 read_error=no | exit=14 read_error=yes | HOLD |
| E/d2-failopen-both-absent | verdict=MATCH exit=0 | verdict=UNEVALUABLE exit=14 | HOLD |
| E/d2-live-unreadable | exit=1 traceback=yes | exit=14 traceback=no | HOLD |
| E/writeguard-paths-eq-out | exit=0 clobbered=yes | exit=2 clobbered=no | HOLD |
| F/live-pair-capture-vs-capture | verdict=MATCH exit=0 | verdict=MATCH exit=0 | HOLD |
| F/receipt-self-pin | pin=112d01dc == tool | pin=7cd19c3c == tool | HOLD |

("HOLD" on the E rows = the revised side reproduces its *declared after-class*;
the before side is the recorded hole. The four `obs` rows in the baseline
`regress.txt` are exactly those E before-states.)

### 3a. The 13/13 rewrite-form reading

Round-2's "same-content rewrite visibility 0/13 → 13/13" is the CR-4 matrix's
v2-ns column (its `attack-matrix.txt`): all 13 forms caught, `v1` (and
sha256-alone) blind on the same-content forms. On the real revised tool, with
the CR-4 attack bodies verbatim, I measure the same split:

- sha256-only **blind** (content identical, rewrite visible only via
  inode/ctime/mtime-ns): `A1 cp -a`, `A2 cp -a --remove-destination`,
  `A3 cp -p`, `A4 rsync -a`, `A5 rsync -a --inplace`, `A6 tar --overwrite`,
  `A7 cp-new+mv`, `A12 reflink=always` → all `REWRITE-DRIFT exit 11`.
- content changed (sha caught by any comparison): `A8`, `A9`, `A10`, `A11`,
  `A13` → all `CONTENT-DRIFT exit 10`.
- boundaries: `chmod-only` → `METADATA-DRIFT 12`; `delete` → `ABSENT 13`.

The same-content subset additionally re-verified via truncate-restore and
mtime-forgery variants (`A9s`/`A10s`/`A11s` → `REWRITE-DRIFT 11`,
`moved=ctime_ns` on the forged rows — the ctime pin remains load-bearing).

## 4. Evidence inventory (excerpt)

| what | where |
|---|---|
| harness + table generator | `harness/regress.py`, `harness/make-tables.py` |
| per-phase structured results | `runs/baseline/regress.{txt,json}`, `runs/revised/regress.{txt,json}` |
| per-form receipts + verify transcripts | `runs/*/logs/<form>.{A,B}.txt` (+`.sha256` sidecars), `runs/*/raw/<form>.verifyAB.txt` |
| E-hole before/after transcripts | `runs/baseline/raw/eacces-capture.txt`, `failopen-AB.txt`, `writeguard-scratch.txt`, `selftest-missing-dir.txt`; same names under `runs/revised/raw/` |
| v1-shape transcripts | `runs/*/raw/v1shape-*.txt` (incl. `v1shape-partial-require5.txt`: `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: …`) |
| live drift derivation | `runs/*/raw/drift-expectation.json`, `runs/*/raw/live-protein-shas.json`, `runs/*/raw/live-capture-drift-reconcile.txt` |
| label evidence | `runs/*/raw/label-v2-stdout.txt`, `label-tz-renders.json`, `label-v1-declared.txt` |
| identity / live pair | `runs/*/raw/live-pair-verify.txt`, `receipt-self-pin` row in `regress.json` |
| tool bytes (both pins) | `tools/tool-base-112d01dc.py`, `tools/tool-rev-7cd19c3c.py` |
| churn record | `churn-poll.log`, `churn-settle-watch.log` |
| full before→after table | `before-after-table.md` (generated) |
| hashes of everything | `MANIFEST.sha256` (re-derivable with `sha256sum -c`) |

Raw key outputs (verbatim):

```
# revised, E/d2-eacces-capture (runs/revised/raw/eacces-capture.txt)
CUSTODY_PAIR_CAPTURE: UNEVALUABLE paths=1/1 label=(none) exit=14
PATH …/eacces-file.conf: UNEVALUABLE  compared=0/11 moved=unevaluable
VERDICT: UNEVALUABLE  paths=1  UNEVALUABLE=1  exit=14
# (receipt stanza: EXISTS: yes / TYPE: file / READ-ERROR: [Errno 13] …; no SHA256)

# revised, E/d2-failopen-both-absent (crafted receipts, both sides STAT-ERROR)
VERDICT: UNEVALUABLE  paths=1  UNEVALUABLE=1  exit=14     [baseline: VERDICT: MATCH exit=0]

# revised, E/writeguard-paths-eq-out
USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode): …/guard/target.conf
(after-bytes = "guard probe original")                    [baseline: exit 0, file replaced by its own receipt]

# revised, D/selftest-missing-scratch
USAGE: scratch base is not a directory: …/no-such-dir-xyz/sub   [baseline: FileNotFoundError traceback, exit 1]

# revised, D/selftest-existing-scratch
CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0   [baseline: cases=15]

# revised, B/ex35-partial-1of5-default (--require-paths 5)
REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: ~/.omp/agent/mcp.json ~/.kimi-code/config.toml ~/.bashrc ~/.profile
[default, no flag: exit 0 (declared default unchanged)]
```

## 5. Attacks / refutations attempted (this seat)

1. **Did the revision regress any rewrite-form detection?** 18/18 identical
   classes and exit codes before→after; sha-only blindness pattern identical.
   VERDICT: no regression.
2. **Vacuousness of the 13/13**: is the "blind" claim real? Every same-content
   form carries `sha_same=True` while the tool fires `REWRITE-DRIFT` with
   `moved=` ∈ {inode, ctime_ns, mtime_ns, mtime_epoch} — the detection is the
   identification pin, and the sha-only view stays silent. VERDICT: real.
3. **Did `--require-paths` change default behavior?** Default 1-of-5 verify is
   still `exit 0` (`MATCH-V1-PARTIAL 1/1`); the flag is opt-in and yields
   `USAGE 2` + the `REFERENCE-COVERAGE` line. VERDICT: no regression, hole
   closed without a default-behavior break.
4. **Is the D2 fail-open closed for receipt files too, or only live?** Crafted
   both-sides `EXISTS: no` + `STAT-ERROR` receipts → `UNEVALUABLE 14`, no
   `MATCH`; live-unreadable candidate → `14` no traceback; EACCES capture writes
   a receipt with `READ-ERROR`. VERDICT: closed on both arms.
5. **Can the write-guard break ordinary captures?** Live pair capture exit 0
   both phases; default-path capture (`F/live-pair…`, `B/r1-canonical-vs-fresh-v2`)
   unaffected; guard fires only on `--paths X --out X`. VERDICT: scoped.
6. **Did the v1 label behavior silently change?** The harness re-derives the
   expected LABEL-DEFECT set and sha agreement independently from live state at
   run time; both phases match it exactly, and the drift-free synthetic anchor
   reproduces the round-2 numbers (1 label / exit 12 / sha 1/1). VERDICT: no.
7. **Mid-run tool churn** (the identity attack): harness aborts on tool movement;
   each phase's copy sha re-verified against its pin; receipts self-pin the same
   sha. VERDICT: run pinned; churn window recorded.
8. **Operator-side confounder hunt**: the only live change is
   `~/.kimi-code/config.toml` (`8cbacd48…` → `bc66d543…`, size-equal rewrite,
   mtime 2026-10-19 09:57:45 −0300) — the kimi CLI rewriting its own config;
   every affected expectation was re-derived (4/5 sha, 4 labels, exit 10) and
   matched. VERDICT: confounder named, not a tool behavior change.

## 6. Named gaps / caveats

- **Revision pin vs wave end.** `7cd19c3c` was EX-21's revision at 13:14:51Z
  (stable 4×20 s) and still the working-tree bytes when this artifact was
  written; EX-21's own seat report had not landed at write time. If the parent
  lands later edits, re-run the harness (≈4 s per phase):
  `python3 harness/regress.py --phase revised --tag <t> --tool-src <tool.py>`.
- **Before-pin identity.** The `before` pin is the round-2 landed blob at HEAD
  (`112d01dc`), extracted read-only; the WORKING-TREE bytes at dispatch time had
  already moved to EX-21's first in-progress revision (`d164d49f` at 13:08:56Z),
  so the before-side is the committed round-2 behavior, which is what the
  regression targets.
- **Live drift is operator-side**: the round-2-recorded `SHA256-CONTRACT: 5/5`
  for the live set can no longer be reproduced (kimi config rewritten at
  12:57:45Z by the running CLI); the harness derives the expectation from live
  state (4/5). The round-1 receipt remains verifiable on 4/5 paths, and the
  drifted path is identified by name and new sha. Recommend the parent record
  this in the rounds notes (round 2 recorded the same class of drift).
- **Chain items not covered here** (owned by other seats, named so nothing reads
  as silently skipped): command A invariance (EX-24 / PL-2), the live pre/post
  pair *as the claim's capture* (EX-21's implementer receipts; my F leg
  independently reproduces MATCH 5/5), README/registry coupled landing (EX-21 +
  parent), and the round-2 hole measurements' first-hand before files (EX-22
  baseline.md) — my before-states corroborate those.