# MutC2Corr — R48-C2 correction grammar attack

Read the frozen claims file in full before commands. Read-only lane; no frozen files changed. Disk guard checked; no installs.

## Attack result

Targeted `record2.py`'s `_quote_correction` / quote correction application (frozen source). A quote correction obtains receipts with `receipts_at(files, text)` for the corrected section, then accepts if *any* cited receipt has the correction's stated key/value. It does not bind that receipt to the corrected round, nor require the correction to identify the particular receipt. The later quote-validation path applies a successful correction to quotes in that round, likewise without requiring the supporting receipt to be round-matched. Thus a round-47 quote can be excused by citing an unrelated section receipt whose matching numeric field is true. This is a plausible forged `quote` correction satisfying the current implementation's checks while not correcting against the receipt the section claims to use.

**Detector/status:** not executed as an isolated mutant in this seat; verdict is a source-level coverage finding, not a killed-mutant result. Expected detector: run the frozen `record2.py --root <fixture> --freeze <freeze> --rev <rev>` against a fixture card where round 47 cites receipt A with a different value, cites another-round receipt B with the correction value, and supplies a correction for round 47. Contract requires the cited receipt for the corrected section; implementation may accept the correction. Exact command/output/hash: not run. No claim of green output is made.

## Existing scoped evidence

The pre-existing `C2Corr.md` records actual correction probes against frozen bytes: correct axes pair produced `corrections_bad: []`; `999/999` was named bad; malformed seats correction was rejected by v3 and accepted by v2. Its full-counter run exited 1 because the freeze card lacks required floor/corrections and its `exempted 2` quote is unsupported. That report explicitly notes the requested well-formed conflicting seats correction and full battery were not run. I did not reuse these as my own command receipts.

## Requested attack scoring

- Correction that re-derives but changes nothing material: **not exercised** (no green evidence).
- `quote` correction whose section quote is unsupported by the receipt it cites: **coverage concern found**; there is no isolated behavioral detector output from this seat.
- `axes` correction for an axis the card does not own: parser accepts arbitrary `\S+` key, but `axis_pairs(...).get(key)` must exist for a valid correction, so such a line should be rejected; **not executed**.

No fixtures were created, so no restoration action was required. No build, test, or other runtime invoked.