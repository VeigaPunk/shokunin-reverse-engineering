# EX-34 — v2 receipt UTC-render label test (chain c3, executor)

Wave arc3-loop1-round2 · seat EX-34 · 2026-10-19 · chain c3 (custody receipt v2).
Task (seat line): *label correctness — prove the v2 receipt's UTC rendering has no
tz offset (compare `date -u`, epoch round-trip); contrast with the v1 label defect
(round-1 record).*

**Verdict: PASS for the label claim, at the pinned tool revision
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`.** Every
`*_UTC_RENDER` field of every real v2 receipt examined is a strict
`YYYY-MM-DDTHH:MM:SSZ` string equal to `date -u -d @<epoch>`, round-trips to the
same epoch, and is byte-identical across seven TZ settings (including DST and
non-whole-hour zones). The round-1 v1 defect reproduces under the same test with
a measured −10800 s (−3 h) delta. Two robustness gaps in the tool were found and
are recorded with verbatim tracebacks (§7).

## 1. Ground truth

- Host TZ at measurement: `-0300` (`date '+%z'` → `-0300`; `date -u` and local
  differ by exactly 3 h).
- The 5 custody paths and their live `mtime`/`ctime` epochs (read-only `stat` +
  `sha256sum`, `live-stat.txt`, captured 2026-10-19T12:01:48Z):
  devin `1792011200`, omp `1792011200`, kimi `1792376443`, bashrc `1792168396`,
  profile `1792044727`; sha256 values live-stat.txt:2-6 (all 5 unchanged from
  round 1: `16f496e6…`, `38d2a1d0…`, `8cbacd48…`, `7d2ca28a…`, `6c6be761…`).
- Rendering functions under test (`custody-pair.py`, pinned revision):
  `render_utc` at `:174-176` (`time.strftime(..., time.gmtime(epoch))`),
  `render_local` at `:179-186`, emitted at `:278` (`MTIME_UTC_RENDER`) and
  `:282` (`CTIME_UTC_RENDER`); the receipt's own label contract is stated at
  `:256-258`.

## 2. The v1 label defect (round-1 record, independently re-derived)

Round-1 canonical receipt
`.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
(sha256 `b8ed1936…`, copy kept here as `v1-canonical-round1-receipt.txt`) prints,
under an `MTIME_UTC` label:

```
:15  MTIME_UTC: 2026-10-14 17:53:20      (devin)     true UTC = 2026-10-14T20:53:20Z
:22  MTIME_UTC: 2026-10-14 17:53:20      (omp)
:29  MTIME_UTC: 2026-10-18 23:20:43      (kimi)      true UTC = 2026-10-19T02:20:43Z
:36  MTIME_UTC: 2026-10-16 13:33:16      (bashrc)
:43  MTIME_UTC: 2026-10-15 03:12:07      (profile)
```

The metadata sidecar `config-pre-pair-metadata.txt` (sha256 `85fa1860…`, kept as
`v1-round1-metadata.txt`) prints the same local instants in its `ctime(UTC)` and
`mtime(UTC)` columns (`:5-9`), with no epoch column at all.

Independent re-derivation (`date -u -d @1792011200` → `2026-10-14 20:53:20`,
`date -d @1792011200` → `2026-10-14 17:53:20 -03`): the v1 string equals the
**local** render, not the UTC render. Round-1 seats recorded this too — EX-01's
corroboration receipt `claims/c1/EX-01/config-pre-pair.txt` ("note on CU-1 time
labels", its tail block) and the round-1 connector sweep
`claims/cross/consistency.md` §5 ("Time-label defect in the canonical custody
receipt"). Digests were never affected; the epoch values were correct.

## 3. The v2 rendering (pinned revision) — checks and results

### 3a. Epoch round-trip (`epoch-roundtrip-table.txt`)

10/10 rows exact, 0 mismatches: for every path and both time kinds,
`MTIME_UTC_RENDER == date -u -d @MTIME_EPOCH '+%Y-%m-%dT%H:%M:%SZ'` and
`date -u -d '<render>' '+%s' == MTIME_EPOCH` (delta 0 s). Example row:

```
/home/vgpnk/.kimi-code/config.toml | MTIME_EPOCH | 1792376443 | 2026-10-19T02:20:43Z | 2026-10-19T02:20:43Z | 1792376443 | YES | 0
```

### 3b. Label separation + no-offset (`label-separation-table.txt`)

10/10 rows pass all four conditions: the UTC field is a strict
`YYYY-MM-DDTHH:MM:SSZ` string **with no offset suffix**, the local field carries
an explicit `[+-]HH:MM` offset, and both parse (via `date -u -d`) to the same
epoch — i.e. the two labels denote one instant, and the separation is real
rather than two copies of one render.

### 3c. TZ invariance (`tz-sweep-112d01.txt`)

Seven captures at the pinned revision, one per TZ:

| TZ | MTIME_UTC_RENDER | independent `date -u` | MTIME_LOCAL_RENDER | independent local `date` |
|---|---|---|---|---|
| UTC | 2026-10-14T20:53:20Z | same | 2026-10-14T20:53:20+00:00 | same |
| America/Sao_Paulo | 2026-10-14T20:53:20Z | same | 2026-10-14T17:53:20-03:00 | same |
| Asia/Tokyo | 2026-10-14T20:53:20Z | same | 2026-10-15T05:53:20+09:00 | same |
| America/New_York (DST −04) | 2026-10-14T20:53:20Z | same | 2026-10-14T16:53:20-04:00 | same |
| Australia/Lord_Howe (DST +11) | 2026-10-14T20:53:20Z | same | 2026-10-15T07:53:20+11:00 | same |
| America/St_Johns (−02:30) | 2026-10-14T20:53:20Z | same | 2026-10-14T18:23:20-02:30 | same |
| host default (−03:00) | 2026-10-14T20:53:20Z | same | 2026-10-14T17:53:20-03:00 | same |

The sha256 of the receipt's UTC-render line set — the 10 `MTIME_UTC_RENDER`/
`CTIME_UTC_RENDER` lines plus the one constant `# label-contract:` header line,
which is identical in every receipt — is the same for all seven files
(`51835c37fcbb84b4e8b8d896b674431bd5bbe5c3b02697afca55cf22151f16f3`) and also
matches the same line-set hash of the mid-wave revision's (`b10ad1c8…`)
captures (`v2-real-tz*.txt`, 7 files), i.e. cross-revision stability of the
rendering. The local renders vary per TZ and each matches an independent
`date -d @1792011200` run byte-for-byte, including the DST and half-hour cases.

## 4. Non-vacuity — the same test FAILs the v1 shape and v2 mutants

`run-matrix.txt` (harness sha256 `2c3286ba…`, source here as `label-test.py`):

| target | exit | verdict |
|---|---|---|
| fixture-v2-correct / fixture-v2-pipe-correct (synthetic conformant v2) | 0 | PASS |
| 7 × v2-112d01-* real receipts (7 TZ) + 7 × v2-real-* (mid-wave revision) | 0 | PASS |
| fixture-v2-m1 — local instant under a `MTIME_UTC` label | 1 | FAIL |
| fixture-v2-m2 — UTC field with `-03:00` offset suffix | 1 | FAIL |
| fixture-v2-m3 — epoch off by one vs render | 1 | FAIL |
| fixture-v2-m4 — `CTIME_EPOCH` absent | 1 | FAIL |
| v1-canonical-round1-receipt / v1-round1-metadata | 1 | FAIL |

On the two v1 files the harness reports 5 × `LOCAL_INSTANT_UNDER_UTC_LABEL`
(one per `MTIME_UTC:` line, each `delta_vs_true_epoch = -10800`) and 10 × the
same class plus 10 × `NO_EPOCH_FIELD` for the sidecar. A check that passed on v2
while also passing v1 would be vacuous; this one discriminates, and the mutant
fixtures fence the failure modes (label, offset suffix, epoch/render
disagreement, missing epoch).

## 5. Independent cross-check by the tool's own verify

`tool-verify-v1-vs-v2.txt` (commands and full output):

- `custody-pair.py verify <v1 round-1 receipt> --live` → **5 × `LABEL-DEFECT`**,
  `VERDICT: METADATA-DRIFT … exit=12`; the sha256 contract still reports
  `5/5 paths agree on sha256` — the v1 receipts remain verifiable on the digest
  field, exactly as the C3 claim requires, while the mislabel is named.
- `custody-pair.py verify <fresh v2 receipt> --live` → `MATCH` 11/11 per path,
  `paths=5 … exit=0`.
- `verify v1-receipt v2-receipt` (cross-format, two-receipt mode) → exit 12
  (expected: the v1 side carries the label finding), digest contract 5/5.
- Tool selftest with an existing scratch dir: `CUSTODY_PAIR_SELFTEST: CLEAN
  cases=15 passed=15 failed=0 exit=0` (includes the tool's own
  `label-utc-render-tz-independent` case, `custody-pair.py:752`).
- **Post-write re-check** (2026-10-19T12:12:42Z, after this seat's artefacts were
  written, tool revision re-derived = `112d01dc…`): fresh capture
  `post-write-recheck-112d01.txt` → harness `PASS`; the receipt's self-recorded
  tool sha equals the live file's sha256.

## 6. Scope of the proof

Proven: the pinned revision's **UTC rendering** is offset-free, epoch-derived,
TZ-invariant, and the label defect of v1 is gone (§2-§5). Not assessed here
(other C3 seats own them): inode/ctime rewrite detection (EX-32/EX-33), NS
field semantics, selftest case adequacy (EX-35/EX-40), the live pre/post pair's
non-label fields (EX-31).

## 7. Robustness gaps found (both on scratch/read-only runs)

1. **`selftest --scratch <non-existent-dir>` → unhandled traceback, exit 1**
   (`robustness-scratch-missingdir.traceback.txt`; `mkdtemp` at
   `custody-pair.py:630`). The tool's declared failure code for a bad argument
   is `EXIT_USAGE = 2`; a missing scratch directory is a plausible operator
   slip. Proposed patch text: `proposed-scratch-dir-guard.patch.md` (this dir).
   Control: the same command with an existing scratch dir exits 0, 15/15 cases.
2. **Transient `KeyError: 'sha_agree'` in `verify … --live`**
   (`robustness-verify-keyerror-transient.txt`): observed while the tool was
   being rewritten mid-wave (revisions `4862f642…` → `b10ad1c8…` → `112d01dc…`
   all within ~2 min; every receipt self-records its tool sha, which makes the
   moving target auditable). Not reproducible at the pinned revision: the same
   command re-run against the same receipt and against a fresh capture gives
   `MATCH … exit=0`. Recorded, not hidden — it is evidence that a seat must pin
   the tool sha in its receipt (the receipts already do).

## 8. Reproduction

```bash
# harness (this dir), live table captured read-only from the 5 custody paths
python3 label-test.py --receipt v2-112d01-hostdefault.txt --live live-stat.txt
# TZ sweep (any subset): capture, then re-run the harness per file
TZ=America/St_Johns python3 .ufo/gates/custody-pair/custody-pair.py capture \
  --out /var/tmp/ex34/x.txt --label t
# v1 contrast, both directions
python3 label-test.py --receipt v1-canonical-round1-receipt.txt --live live-stat.txt
python3 .ufo/gates/custody-pair/custody-pair.py verify \
  v1-canonical-round1-receipt.txt --live        # -> LABEL-DEFECT x5, exit 12
```

## 9. Artefact inventory (sha256)

```
label-test.py (harness)                2c3286ba873966c994ad52513bb65021ce57cb8558f42ba49d12806cde92337a
live-stat.txt (live ground truth)      71cce7f1ace9add58f9234ae98e019d4eb0b12a1d560e54bd6705656a1a4cd20
epoch-roundtrip-table.txt              a35e90ce9abaee087efd02b5885b5883d95c292833a28f1a31e573e43aeba2c1
label-separation-table.txt             3993483b36e159dbcfd1144c9b751b31b2ec52e2f61944e741b81f9c747b51d6
tz-sweep-112d01.txt                    ca4870bf116bc2355abd260169c677b17e03ded89f3211ba803e3fd7529e20ac
run-matrix.txt                         73ac25f4a3fba6692f73f84c105b1afbbcc32816712965d325f57cecc24b1388
tool-verify-v1-vs-v2.txt               898c06475904a8f30c713abc75a224816b9b96049fa63e3e3a187bf35cf87377
robustness-scratch-missingdir…         3e1a22db3af01382d8b24c23ace75a87526519cafe943c7bf06b79d1ac1b6ee9
robustness-verify-keyerror-…           4af372535fbc396ec43a6d329dd135521e128549989157cf994a3737f255d7bc
v2-112d01-hostdefault.txt              c6ff83840931451492a479fa7404b75ce94d14a84a26f79ba23aebeb8fdde338
post-write-recheck-112d01.txt          1e80accd395b75d471172d9cb2273dd0b1ee622d8a2c2a626b750a3458cb87b1
v2-112d01-UTC.txt                      697c7b89b01a1d520fdaa944f33c8e83532b0c29debd84492fb64de361a13707
v2-112d01-America_Sao_Paulo.txt        90bc985c84c1acd17383307a5035416fcfdae7df62c1cfe40f173c2d8c2f3297
v2-112d01-Asia_Tokyo.txt               d7c9ec8fb9edf39e74c9a8e40e492a41f56873cb70e09f282957c704b795dbd4
v2-112d01-America_New_York.txt         d10772879c9539d497a434a04554a6ba946b02d6d3e571ce9f58bde523e9878f
v2-112d01-Australia_Lord_Howe.txt      e361ffae8f7b1eefe9c44311679a27beb1f21df79ed3e87309836d0e05e29714
v2-112d01-America_St_Johns.txt         921508b3f6c2299d4df012ae9291cb3516fc5746d8a33eb4e84ac93c77158032
v1-canonical-round1-receipt.txt        b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776
v1-round1-metadata.txt                 85fa1860000bda4de57ffb17219e59fa0e553d505eb76815c4bcf542f6426a90
fixture-v2-correct.txt                  3325ccfb0c47a8191165528ac572e46d44af5a1f370ce7d73100c8fcf8d7d64d
fixture-v2-pipe-correct.txt            2cad1173d5b931bdfab96598d2aa817b5c9871bfec230b72c542704478ff7e31
fixture-v2-m1-local-under-utc.txt      3c646d46996be70f5fcb32154c74ddd46ac9af4c9e20b90538b69b5958c84db8
fixture-v2-m2-offset-suffix.txt        2ba93492c668821f32e04ab4fa33100641447bc366aaaca567dcdbbfd683d671
fixture-v2-m3-epoch-offbyone.txt       898f68c6f5a3d95f447449e70e8a34ddf43f7c72a7110be6aeb229b87e495753
fixture-v2-m4-ctime-epoch-missing.txt  2b63c85d955b3eed6e048e8530c8647e3add10641054128fcb3a4ffee79398d3
```

Scratch (not committed): `/var/tmp/ex34/` — captures, fixtures, harness working
copy (per the wave rule; `/tmp` untouched, it is quota-exhausted).
