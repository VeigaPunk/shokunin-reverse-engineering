# Proposed corpus note — "carrier A" readings @ first REA pin (EX-06, arc3-loop1-round3)

Status: PROPOSAL (patch text only; no corpus file edited). For folding into the
round-3 C1 corpus entry or as an addendum to
`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`. Every claim below cites a
file in `.ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/` (E) or a sibling
seat's artifact.

## Reading note (naming) — three readings exist; all three were probed K/K

- **A/1. `carrier-A.hex`** — r1 CR-1 hand-assembled control, 84 B runtime / 168 B hex,
  sha256 `36dc8246…01b9b3d2` (`arc3-loop1-round1/claims/c1/CR-1/evidence/carrier-A.hex`);
  EX-07's wave calls it **legA**. 3 planted selectors + decoys `deadbeef`/`ffffffff`.
- **A/2. `carrierA.runtime.hex`** — EX-03's round-3 compiled carrier (optimizer-enabled),
  1426 B runtime / 2853 B hex, runtime sha256 `9f7392ac…1d23741a`, hex-text file
  `87d1bb03…`; K=9 planted (`claims/c1/EX-03/planted-selectors.txt`, mtime 13:09:10Z);
  EX-07's wave calls it **legC**, and `seats/EX-07.md` names this as the wave's carrier A.
- **A/3. `OptVault.runtime.hex`** — PL-1's plan carrier A
  (`claims/c1/PL-1/plan.md` §1A: optimizer `runs=200`, payable receive/fallback, mixed
  mutability), 776 B runtime sha256 `544469b7…95dfde7f`, K=5 planted
  (`evidence/OptVault.runtime.{hex,bin}`).

## Observations (all re-derivable from the sealed envelopes)

- **A/1 @6.4.0 (FIRST pin, bare `--format json`, positional encoding):**
  `ev_4321ec29…`; 3/3 planted (`a9059cbb`@38, `70a08231`@48, `095ea7b3`@58), zero
  missing / zero extra; decoys present as PUSH4 immediates @70/@77 and **not reported**
  (E/planted-K.json). Full envelopes in three output shapes — bare JSON,
  `--full-output` `{ok,data,meta}` wrapper, default TOON — all with the same
  evidence_id (E/probe-carrier-A-hex-6.4.0.json, E/probe-carrierA-hex-6.4.0-full.json,
  E/probe-carrierA-hex-6.4.0-default.out).
- **A/2 @6.4.0 + @6.7.0 + raw@6.4.0:** 9/9, zero missing / zero extra on all three legs;
  non-dispatch PUSH4 constants (`6508d58f`, `30cd7471` ×2, `4e487b71` Panic, terminal
  CBOR `43000825`) **not reported** (E/planted-K-ex03carrierA.json).
- **A/3 @6.4.0 + @6.7.0 + raw@6.4.0:** 5/5, zero missing / zero extra; `4e487b71@659`
  not reported (E/planted-K-pl1OptVault.json); prologue `608060405260043610610049`…
- **Cross-seat agreement, 0 diffs (normalized; id/paths/diagnostics stripped):**
  A/1: my 6.4.0 vs EX-07 `legA-hex-6.4.0` vs CR-1 r1 `out-A-hex` (wrapper); A/2: my
  legs vs EX-07 `legC` hex-6.4.0/hex-6.7.0/raw-6.4.0; A/3: my legs vs PL-1 prototype
  `OptVault-6.4.0-hex/-raw`, `OptVault-6.7.0-hex` — all 0 diffs (E/analysis.txt).
- **6.7.0 vs 6.4.0 on A/1:** same payload; delta = `bytecode.metadata`
  (`status:"unavailable"`, "No plausible terminal CBOR map was identified") + one extra
  limitation line + `relationship_coverage` — a clean negative on a hand-assembled blob.
- **raw twin:** identical payload/offsets; only form fields differ (bytes 168→84,
  encoding, file-vs-bytecode digest, subject name).
- **ev_ id domain (r1 entry Unknown), measured on this verb family:** id stable across
  reruns, output forms, TMPDIR, ~3 h, relative-vs-absolute argv spelling; changes with
  resolved path (E/probe-carrierA-hex-6.4.0-altpath.json → `ev_a964fa8c…`), **carrier
  bytes at the same path** (E/idtest-bytes-a/b.json — decoded bytecode sha identical,
  ids differ), encoding form, and pin. EX-07's `idpath-cr1path` replay reproduces CR-1's
  historical `ev_2d55ac04…` at CR-1's recorded path. ⇒ request-scoped identity; no
  content-addressed claim for `ev_` ids; compare by `subject.digest.sha256` + payload.
- **Standing `/tmp` note re-measured (not reproduced):** 2026-10-19T13:09–13:10Z both
  carriers exit 0 with `TMPDIR=/tmp` (`/tmp` 96M used of 16G; 50 MiB write test OK;
  E/trap-tmp-default-edquot.json, E/trap-tmp-edquot-rv2token-6.4.0.json). The r1 EDQUOT
  mode is environment-dependent; scratch-under-/var/tmp stays the cheap default.

## Limitations

Payload equality asserted on the normalized envelopes named above; the `ev_` id's full
domain (hash vs other derivation) was not proven, only its sensitivity axes. Only the
three named carriers were probed by this seat; per-carrier mutability/argument deltas
remain upstream-inference observations (PL-1 §5, EX-07 §1).