# HB2 — receipts re-counter / C2 inventory recompute

## CLAIM
C2's 43-artifact receipt inventory recomputes exactly: counts 14+12+17=43 and all 43 SHA-256 values; every in-bundle anchor (MANIFESTs, censuses) agrees with current bytes, the sole MANIFEST delta being the arc-known round-8 leg-10 append-supersession.

## METHOD
Read-only at HEAD c343939. `git ls-files -- <3 dirs> | wc -l`; `git ls-files -z -- <3 dirs> | xargs -0 sha256sum` (whitespace-normalized, sorted) diffed against `.ufo/waves/luna-round-10/C2.md:11-53`; `git diff --quiet HEAD -- <3 dirs>`; `git status --porcelain -- <3 dirs>`; `git ls-files --stage` mode tally. MANIFEST row loops (`sha256sum`, `stat -c%s`). `python3 -B` parse of `census-final.txt` / `census-laneB-final.txt` CENSUS_JSON `receipts_sha256` vs live files. `head -n 59 leg-10.md | sha256sum`. HB2-lineage: `wc -l`, `sort -u | wc -l`, `grep -cE '^[a-z0-9_]+$'`, `grep -cwE` on the six 6.5-only names in `leg-2-tools.txt`. No probes, no network.

## FINDINGS
1. Counts: round-6 `receipts` 14 (10 legs + 3 census + MANIFEST), `receipts-B` 12 (10 legs + census + MANIFEST) = 26; round-8 17 (10 legs + leg-2-tools + 3 RV3 replays + 2 census + MANIFEST); combined 43; all index mode 100644; `git diff --quiet HEAD` exit 0; `git status --porcelain` empty (no untracked files inside the three dirs).
2. Hash recompute: sorted normalized diff against C2.md:11-53 empty (exit 0) — 43/43 identical, including leg-10 `6cd389e9…`.
3. Anchor cross-checks beyond C2: `receipts-B/MANIFEST.txt` 10/10 hash+size exact; round-6 `census-final.txt` `receipts_sha256` A1-10/B1-10 20/20 live-match; `census-laneB-final.txt` likewise 20/20.
4. Round-8 MANIFEST 9/10 exact; leg-10 row `c89eea7a…` = `head -n 59` (27,655 B) of current 40,401 B `6cd389e9…` — disclosed post-census append (round-8 PB0/HB1; `census-laneB-pre.txt:266` "APPEND-SUPERSEDED"), not a false hash; C2's row cites current bytes.
5. Round-6 lane-A MANIFEST holds 1 row (leg-1 `24bfd90f…`, matches) — known defect (`.ufo/reports/luna-round-6/kaidoku.md:53`), not a count error; the census carries the other hashes.
6. `leg-2-tools.txt` recount: 170/170 unique/strict; 0 hits for the six names — round-8 HB2's recount reproduces.

## THREATS
SHA-256 authenticates bytes, not authorship or semantics. Tracked-scope only; none untracked under the three dirs at my snapshot, but parallel writers could add. HEAD advanced past the briefing (6e83a20 → c343939, LOG.md + SCORECARD.md only; receipts untouched). `MANIFEST.txt:10` stays stale-by-append — citation hazard, bytes intact.

## VERDICT
CLEAN — 43/43 counts and hashes reproduce C2 exactly; all bundle anchors consistent; sole MANIFEST mismatch is the disclosed round-8 leg-10 prefix-supersession.
