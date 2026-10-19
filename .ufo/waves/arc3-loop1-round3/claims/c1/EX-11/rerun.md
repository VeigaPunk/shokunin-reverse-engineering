# SEAT EX-11 — rerun id-stability: carrier A's exact probe invocation, byte-wise (chain c1)

Wave `arc3-loop1-round3` | 2026-10-19 | repo HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`
(`git rev-parse HEAD`, read at 10:10 -03). Writes: this artifact set under
`.ufo/waves/arc3-loop1-round3/claims/c1/EX-11/` + `seats/EX-11.md` only. No git
mutation, no custody-path access, no other repo file touched. Scratch:
`/var/tmp/ex11r3/` and the reconstructed carrier path `/dev/shm/cr1/` (both
outside the repo; `/tmp` never used).

## 0. Task and what "carrier A" resolves to

Seat task (frozen): *rerun id-stability: repeat carrier A's exact probe
invocation twice; compare envelopes byte-wise; record whether ids re-derive
(per the r1 entry's id-domain caveat).*

- **Primary reading — measured.** The only artifact in the repo literally named
  "carrier A" is CR-1's hand-assembled control from arc3-loop1-round1:
  `.ufo/waves/arc3-loop1-round1/claims/c1/CR-1/evidence/carrier-A.hex`
  (168 B hex text, sha256 `36dc82468c5846a93273970483253e63f5b0bef673f0bd355d3c41db01b9b3d2`;
  decoded bytecode 84 B `a92ba15225aaddccff5c0c67fff18c6c13b86be3bc91c07527681fbf500f6f7b`;
  3 dispatched selectors `095ea7b3`/`70a08231`/`a9059cbb` + decoy PUSH4 `deadbeef`
  and `ffffffff`). Referenced as "carrier A" in
  `.ufo/waves/arc3-loop1-round1/seats/CR-1.md:58`; a repo-wide grep for
  "carrier A" returns that seat report as the only hit.
- **Alternate reading — also measured (cheap, ambiguity closed).** The r1
  knowledge entry's primary carrier is `Rv2Token` (hex leg, sealed id
  `ev_45849c8b…`) — see `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:12,17`.
  Its invocation was repeated too, so the seat verdict holds under either
  reading of "carrier A".

The r1 caveat being tested (entry line 7 and its Unknowns line 29): *"the `ev_`
id domain for this verb family was not measured, so if a fresh run mints a
different id, compare by `subject.digest.sha256` + function payload instead."*

## 1. The exact invocation (recovered, then repeated)

CR-1's own agent wire log survives:
`~/.kimi-code/sessions/wd_shokunin_8c4a99c6228c/session_f33b1f06-8ec4-4bf9-9726-28a5a61545d1/agents/agent-23/wire.jsonl`
(agent carries `SEAT CR-1 | CHAIN c1 | ROLE critic`). Recovered form:

```
REA=~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/scripts/rea.mjs   # package.json version 6.4.0
cd /dev/shm/cr1
node $REA inspect-evm-interface /dev/shm/cr1/carrier-A.hex hex --format json --full-output > out-A-hex.json 2>err-A-hex.txt
TMPDIR=/dev/shm/cr1 node $REA inspect-evm-interface /dev/shm/cr1/carrier-A.hex hex --format json --full-output > ok-full.json 2>&1
```

- The pin is **6.4.0**, identified by measurement, not prose: the 6.4.0 envelope
  byte-matches CR-1's committed `out-A-hex.json`/`ok-full.json` (4,497 env bytes);
  6.5.0/6.7.0 produce 5,238 env bytes (see §3).
- Executable pinned: `scripts/rea.mjs` sha256
  `3554288a08c455fa419dad662d73710fb17debe94b9e71dd1282761117c5981e`, `node v26.12.0`.
- CR-1's scratch dir was gone at rerun time; `/dev/shm/cr1/carrier-A.hex` was
  rebuilt byte-identically from the committed evidence file (hash re-verified,
  and the rerun envelopes' path-keyed fields match CR-1's exactly — §3).
- TMPDIR is outside the envelope (CR-1's two committed files differ in no
  envelope byte although only the `ok-full` line carried `TMPDIR=/dev/shm/cr1`;
  my npx-form pair ran with `TMPDIR=/var/tmp/ex11r3/tmpdir` and is byte-identical
  as well — an independent re-confirmation of r1 EX-09 attack E).

**Repeated invocations** — `commands.txt` (this dir) holds every command verbatim.
Fresh pair 1 (the "exact" form, cwd/TMPDIR `/dev/shm/cr1`):
`rerun-exact-1.json`, `rerun-exact-2.json` (raw `--full-output` stdout, exit 0).
Fresh pair 2 (npx form, `TMPDIR=/var/tmp/ex11r3/tmpdir`) — raw stdout stayed in
scratch; the landed `env-a-6.4.0-1.json`/`env-a-6.4.0-2.json` are the extracted
envelopes. Envelopes were extracted as the exact `"data":…,"meta":` byte
substring (no re-serialization) by `extract2.py`; extraction is lossless
(`rerun-exact-*.json` = wrapper + envelope).

## 2. Verdict

**The ids re-derive, byte-exactly, on both carriers.** For carrier A @6.4.0:
six independent runs (CR-1's two committed ones + my four fresh ones, across two
invocation forms, two TMPDIRs, cwd `/dev/shm/cr1`) produced a **byte-identical
envelope** and the same sealed id `ev_2d55ac04dee5f3a4b3b35f8550f21810b3691d5450ce44f1a745e732dcdf1a8c`.
The id was additionally re-derived independently from the envelope bytes under
the 6.4.0 projection (`reid-ext11.py`, §4) — MATCH, not merely observed twice.
For Rv2Token hex @6.4.0: five lanes (RV-2's committed probe + reruns a/b + my two
fresh runs) are envelope byte-identical, id `ev_45849c8b11794ea0b007bd01ea3241aa9b385ca7543e514a16e82c795a106eaf`
re-derived — closing the r1 caveat for that leg too.

## 3. Byte-wise comparison (evidence: `compare-carrierA.txt`, `compare-rv2.txt`)

Carrier A lanes (envelope = exact bytes between the `--full-output` wrapper's
`"data":` and its trailing `,"meta":`):

| lane | stdout B | envelope B | envelope sha256 | evidence_id |
|---|---|---|---|---|
| CR-1 `out-A-hex.json` (committed, 6.4.0) | 4,579 | 4,497 | `c6d85aed0ccafaa265e79f030b27aade10eefd30932e4ff76d45cf2226467f90` | `ev_2d55ac04…` |
| CR-1 `ok-full.json` (committed, 6.4.0) | 4,579 | 4,497 | `c6d85aed…67f90` | `ev_2d55ac04…` |
| `rerun-exact-1.json` (fresh, exact form) | 4,579 | 4,497 | `c6d85aed…67f90` | `ev_2d55ac04…` |
| `rerun-exact-2.json` (fresh, exact form) | 4,579 | 4,497 | `c6d85aed…67f90` | `ev_2d55ac04…` |
| `env-a-6.4.0-1.json` (fresh, npx form, other TMPDIR) | 4,579 | 4,497 | `c6d85aed…67f90` | `ev_2d55ac04…` |
| `env-a-6.4.0-2.json` (fresh, npx form, other TMPDIR) | 4,579 | 4,497 | `c6d85aed…67f90` | `ev_2d55ac04…` |

All six envelopes pairwise IDENTICAL. Whole stdout differs only inside
`meta.duration` (143/119/108/107/102/102 ms — outside the envelope); after
normalizing that field the whole-stdout sha256 is
`bf1e8518ac13e85283e732e3cf39668b35e8a497dfd100d8d6020c8e1cd362e6` for all six.
Function payload identical everywhere: 3/3 selectors, offsets 58/48/38,
`dispatch:"abi"`, `stateMutability:"payable"`, decoded bytecode sha `a92ba152…`
(= carrier `carrier-A.bin` sha, r1), artifact sha `36dc8246…` = the carrier file
I reconstructed.

Rv2Token lanes (bare envelopes): rv2 fresh-1, fresh-2, RV-2's
`probe-runtime-hex-6.4.0.json` + `probe-rerun-a.json` + `probe-rerun-b.json` —
all 9,398 env bytes, sha256 `04cd4adebf70dab08867ddaa95aa3df91fa113870a8da64298a9543dc26f73b7`,
id `ev_45849c8b…`; 5/5 selectors, decoded sha `c1081a56…` everywhere
(committed files are bare envelopes + trailing newline, 9,399 B).

Version sweep at the same carrier A path (two runs each; pins are the npx cache
dirs `dea9475797100b20`=6.4.0, `ad9a3fdbcad992c6`=6.5.0, `a1722018f28f9df2`=6.7.0,
versions read from each `package.json`):

| pin | envelope B | envelope sha256 | id |
|---|---|---|---|
| 6.4.0 (×2, identical) | 4,497 | `c6d85aed…` | `ev_2d55ac04…` |
| 6.5.0 (×2, identical) | 5,238 | `58431c07d18f395fb423a761e63f4b1089ab75fd839c78877c69f834276a1879` | `ev_7c82fe2abd2591ba24b616462a9e0513bfa814101143ab61a07b8bef57f45f46` |
| 6.7.0 (×2, identical) | 5,238 | `468395d553766bc1f8debac9c39a58ea06c7c856a768c70d6dbaf851677aadf3` | `ev_c0ef54bf267e17bfe74a69155e03551e4a4693132cddaa5a763f1d06991fc751` |

Field-level walk: the 6.5.0 and 6.7.0 envelopes differ **only in `evidence_id`**
(every other byte equal; both carry `relationship_coverage: null`). The id split
is the projection rule, measured against the pinned sources:
6.4.0 `dist/domain/evidence.js:129-151` has no rc field; 6.5.0 `:175-177` omits
rc when it is null; 6.7.0 `:178` hashes rc unconditionally. Hence: a differing id
across pins is a schema difference, not rerun instability (r1 EX-09 attack G,
re-confirmed here with the exact inclusion rule).

## 4. Independent id re-derivation (evidence: `reid-results.txt`)

`reid-ext11.py` (this dir) re-implements RFC 8785 canonical JSON + sha256 over
the per-pin semantic projection (subject display fields `name`/`local_path`
excluded), modeled on r1 EX-09's `reid.py` and switchable `norc|rc` to match
each pin's rule. Results, verbatim (all run, all exit 0 unless stated):

- `env-exact-1/2`, `env-cr1-out-A-hex`, `env-cr1-ok-full`, `env-a-6.4.0-1` under
  `norc` (canonical 4,348 B): **MATCH** `ev_2d55ac04…` (four lanes + sweep).
- `env-rv2-1/2`, `env-rv2-r1-6.4.0`, `-rerun-a`, `-rerun-b` under `norc`
  (canonical 9,157 B): **MATCH** `ev_45849c8b…` (five lanes).
- `env-a-6.5.0-1` `norc`: **MATCH** `ev_7c82fe2a…`; `rc`: MISMATCH
  (derives `ev_c0ef54bf…`).
- `env-a-6.7.0-1` `rc`: **MATCH** `ev_c0ef54bf…`; `norc`: MISMATCH.

## 5. Attacks / refutations attempted (all run, verdicts)

1. **Path-keying attack** — same carrier bytes at a different path
   (`/var/tmp/ex11r3/pathctl/carrier-A.hex`): id `ev_d8ee1364256b6b71d8449127721ab4604ab8ecbe770e0788831d79cb42ba2200`
   (envelope `env-pathctl-path.json`), re-derives MATCH. Verdict: **CONFIRMED
   path-keyed** — "repeat the exact invocation" must mean the same path
   (re-confirms r1 EX-09 attack F; the id is not a pure content hash).
2. **Content-keying attack** — same control path, content + one trailing newline
   (sha256 `95eca04dc5aebc164b34b578442e58925a3cecaaa47360b25cf9263dca86ef0e`):
   id `ev_130b6d787d8e06b6dc667e2e4ae90fabdf63a400bfdca34279bd3e726d322838`
   (`env-pathctl-content.json`), re-derives MATCH. Verdict: **CONFIRMED
   content-keyed**. Together 1+2 show the rerun identity in §2 is a deterministic
   function of (path, content, pin projection), not a coincidence or a constant.
3. **"Different id = instability" attack** — 6.5.0 vs 6.7.0 mint different ids
   for the same input: REFUTED as instability; difference is the null-rc
   projection rule (§3), and each pin's id re-derives under its own rule.
4. **TMPDIR/cwd confound** — CONFIRMED neutral (two TMPDIRs, same envelope).
5. **Same-envelope/hidden-different-argv** — the envelope pins
   `operation`, `parameters` (path + `encoding:"hex"`), provider and decoded
   bytecode; `--format`/`--full-output` affect only the wrapper. The comparison
   is defined at the envelope level by the seat task; the wrapper differs only in
   `meta.duration` (measured §3).
6. **Not run (stated, not hidden):** the r1 host hazard that a `/tmp`-defaulted
   run fails EDQUOT is unchanged; every run here used a disk-backed TMPDIR. Raw
   encoding of this carrier and the wrong-artifact (creation) leg were covered by
   CR-1 and are out of this seat's scope.

## 6. Chain before→after measurement (c1)

Recipe A (SCORECARD.md:86-124, body copied unmodified; `REV=HEAD`) at HEAD
`c07af80f` → `command-A-before.txt`:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "HEAD", "rule_blocks": 14}
```

Before-state 82/82, 14/14 rules, 10.0/10.0 — the c1 claim's `82 → 83` before
value. The after value lands only at the round's commit and is not mine to
measure; this seat's deliverable is the id-stability rerun above.

## 7. Provenance, identity, gaps

- All id/sha claims above are re-derived from the **landed** files in this dir
  (`SHA256SUMS` regenerated after the final revision). “SHA256SUMS” lists every
  file in this directory except itself. Landed-file hashes: carrier A envelope
  `c6d85aed…` (6 files in-dir identical), Rv2Token envelope `04cd4ade…` (5
  identical), 6.5.0 `58431c07…`, 6.7.0 `468395d5…`, controls `e3d7dcde…` /
  `c0aac104…`.
- Source trees read (read-only): CR-1 and RV-2 claim dirs (r1), the r1 knowledge
  entry, SCORECARD.md; pins in `~/.npm/_npx/` (no installs, no writes there).
- Gaps: CR-1's `/dev/shm/cr1` was gone — carrier rebuilt, hash-verified
  (§1); the wire-log line for CR-1's `out-A-hex` run does not itself show a
  `TMPDIR=` prefix (the `ok-full` line does), so the TMPDIR of that exact run is
  not claimed — it is outside the envelope either way (measured, §3).
- Interpretation risk left to the parent: if the dispatch intended some other
  "carrier A" than CR-1's hand-assembled control, the Rv2Token leg (§2/§3) is the
  nearest standing reading; both are measured.