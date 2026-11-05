# binwalk v3 is a Rust rewrite whose unit of work is embedded-data identification

source: S129 — https://raw.githubusercontent.com/ReFirmLabs/binwalk/26713972e3f9f52dc37d4a421c4554b0bd9e82ef/README.md — lines 1-3 (`# Binwalk v3` lead) and line 9 (`## What does it do?`), commit-pinned, sha256 `87b8277efbbbdcdfcaa6518c1d3efed071617214432c81400b9e67ee093a11d4`
verified-at: 2026-10-26
recheck: 180d — `curl -fsSL <S129 URL> | sha256sum` equals the pin above (ran 2026-10-26T21:17Z, HTTP 200)
lineage: assimilated in round 41 from the shokuknow `corpus-expansion-1` package (`merge/kaidoku/knowledge/.../firmware-region-vocabulary.md`, staged S109 → lane S129 by document; review `.ufo/waves/round-41/w1/R41Assim.md`)

**Claim.** binwalk v3 is "an updated version of the Binwalk firmware analysis tool, re-written in Rust
for speed and accuracy" (README line 3, the document lead under `# Binwalk v3`), and its stated job is
that it "can identify, and optionally extract, files and data that have been embedded inside of other
files" (line 9, under `## What does it do?`); the per-signature catalogue is delegated to the project
Wiki, which this entry did not open and does not claim.

**Why this matters for the lane.** REA's `inspect_firmware_regions` operation runs the `binwalk` engine
(S123, `FirmwareProvider.js:141`), and the round-40/41 triage tables treat an envelope from that
operation/provider pair as out of domain (`unclassified`, `SKILL.md` rule blocks 19-20). This entry
states the upstream half of why: binwalk's unit of work is identification of embedded data, so a
region it reports is a producer-local label, not a filesystem fact; a SquashFS verdict needs the
`extract_firmware`/`unblob` path.

**Caveats.** README only; the Wiki signature list and binwalk's extractor behaviour are not evidence
here. Nothing asserts that a given image holds a given filesystem.
