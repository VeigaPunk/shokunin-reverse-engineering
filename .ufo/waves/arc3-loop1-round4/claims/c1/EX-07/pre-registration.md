# EX-07 (arc3-loop1-round4, c1) — pre-registration, recorded BEFORE the id-domain legs ran

Written 2026-10-19 (before the D-series probes below were invoked; the A/B/C leg
matrix and the envelope/`relationship_coverage` measurements are already captured
and hashed in this seat dir).

## Id-domain experiment: what each leg isolates

- D1: byte-identical copy of `VaultB.opt200.runtime.hex` at a *different* absolute
  path, same pin 6.4.0, same `hex` encoding. **Isolates path** (bytes held).
- D2: byte-identical copy of `VaultB.opt200.runtime.bin` at a different absolute
  path, same pin 6.4.0, `raw`. Same isolation, raw leg.
- D3: symlink at a different absolute path resolving to the repo `.hex` file,
  `hex`, 6.4.0. Distinguishes "id minted from the path string given" from "id
  minted from the resolved target".
- D4: the *same* repo `.hex` path as A-hex-6.4.0, but requested as `raw` (the
  ASCII-decode trap). **Isolates the encoding parameter** at fixed path + pin.
- D5: the same repo file reached through a relative path from a different cwd
  (`hex`, 6.4.0). Second path-string variant.
- D6: the repo `.bin` file requested as `hex` (the mirror-image input trap).

## Predictions (falsifiable; recorded before the runs)

- P1 (D1, D2): the `ev_` id **differs** from the repo-path leg, while decoded
  `normalized_result.bytecode.sha256` and the function payload are **identical**.
  Basis: r3 measured path-sensitive ids for this verb family (carrier-A at three
  paths, `EX-07/legA-compare.txt`).
- P2 (D3): if the id follows the *given* path string, D3's id differs from
  `ev_d409bd50…`; if it follows the resolved target, D3 re-derives
  `ev_d409bd50…`. I do **not** know which; both outcomes are informative and
  neither is a defect claim. Prediction: id follows the given path string (the
  r3 envelope records `parameters.path` verbatim), so D3 differs.
- P3 (D4): the raw-on-hex-text leg exits 0, reports 0 functions, and its decoded
  `bytecode.sha256` equals the *hex file's own* sha256 (the r3 trap class). The id
  differs from A-hex-6.4.0 (same path, different request).
- P4 (D6): the `.bin` read as `hex` does **not** reproduce the raw leg's payload
  (binary-as-hex is not a valid hex text); expected parsed-empty or an error, not
  13/13. (r3 had an `attack-bin-as-hex-6.7.0` leg; its outcome is read only after
  this file is written.)
- P5: every leg that does decode the runtime bytes reports the same decoded
  `b24a0115…` and the same 13-function payload regardless of path or encoding —
  i.e. the payload is the encoding/path-invariant identity, the `ev_` id and the
  `subject.digest` are not.

## Envelope-delta prediction (already measured; recorded for the record)

The r3 entry's Unknowns line reads "whether 6.7.0-specific envelope deltas (e.g.
`relationship_coverage` present only there) generalize". Measured this round on
three carriers × hex/raw: the key is **absent at 6.4.0 and present at both 6.5.0
and 6.7.0** (value `null`), with the limitation list at 6 vs 7 lines (the 6.7.0/
6.5.0 extra line being the CBOR-metadata caveat). Prediction if this reading is
wrong: some leg in this seat's matrix contradicts the pattern; the matrix is the
arbiter.
