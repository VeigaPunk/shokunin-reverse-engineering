# Census rekey — CensusRekey-2

## Axes
- **Calibration:** classify both round-17 records as `DATED`, not `CURRENT`; retain G16's live-anchor override.
- **Coverage:** resolve the SKILL row from a stable evidence-path anchor and fail on missing/duplicate anchors.
- **Depth:** add anti-vacuity fixture cases for shifted anchors, live-value precedence, and a new undeclared block.

## Findings and change
- **Observed:** D4 names `SCORECARD.md:2380-2382` and `SKILL.md:511-519` as the two undeclared blocks (`corpus/lessons/round-19-verifier-spotcheck.md:186-187`). The SCORECARD capability row is explicitly first-working `round-17` (`SCORECARD.md:2374`); its limitations include REA 6.5.0/6.7.0 observations (`SCORECARD.md:2380-2382`). The SKILL section is titled “Retained Go carrier diagnostics — round 17” and points to the r17 report at its start (`SKILL.md:509-519`). Both are records of past verification, so their true gate class is `DATED`.
- **Implemented:** `.ufo/gates/c1-census-v10.py:278-289` declares narrow `DATED` ranges and stable anchors. The SKILL range keys to `r17-go-carrier-diagnostics.md` rather than a fragile absolute line; `resolve_scopes` reports non-unique/missing anchors and `assert_markers` enforces the dated marker (`:413-461`). G16 remains unchanged and still promotes a value equal to any live anchor to `current-ok` (`:628-632`); undeclared loci remain failing (`:638-641`, `:801-803`).
- Added `--selftest` with a tempfile fixture shifted before the SKILL anchor; cases assert dynamic range resolution, live-value precedence, and that a new `rea-agents@99.99.99` block is classified `UNDECLARED` (`:664-719`). This is selftest implementation, not an executed result.

## Commands and retained evidence
- `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-CensusRekey-2 && git -C /tmp/kr20-CensusRekey-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-CensusRekey-2 rev-parse HEAD` — exit 0; observed base `14f0260ad319ecc26994381b2415d5a999003375`.
- `git -C /tmp/kr20-CensusRekey-2 add -A && git -C /tmp/kr20-CensusRekey-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/CensusRekey-2.patch && git -C /tmp/kr20-CensusRekey-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; `.ufo/gates/c1-census-v10.py | 176 +++++++++++++++++++++++++++++++++++---------` (1 file changed, 140 insertions(+), 36 deletions(-)). Patch retained at `.ufo/waves/round-20/w1/patches/CensusRekey-2.patch`.
- **Not run:** baseline census, patched census, and `--selftest`; this editing wave's executor rule prohibits builds/tests/checks and assigns post-integration gate execution to the parent. No exit status or verdict is claimed for them.
- **LSP:** unavailable in the exposed tool inventory; no cold/empty LSP response was treated as evidence.
- No tools installed or updated.

## Risk / handoff
The actual baseline/patched gate verdicts and selftest outcome remain unmeasured; parent should run those post-integration checks. No other blocker identified.
