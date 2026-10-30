# ScoutCensusRecheck — second-reader census no-regression recheck (r52-w1)

Scope: independent re-check of the census no-regression state at the round-52 claims draft
`ab0eafedc41402b43b41a4362084119578dfe7ce`. ExecCensusCheck outputs were not read. Work done in a
fresh `git clone --shared` checked out detached at `ab0eafed`, scratch `/fast/scratch/hyaku/kaidoku-r52/w1-ScoutCensusRecheck`
(removed before yield). Receipts: `.ufo/waves/round-52/w1/ScoutCensusRecheck/` (index `receipts-index.json`).
No tools installed or updated. No REA run. Nothing committed, staged or mutated in the lane.

## Verdict

Part (1) and part (2) hold as asked: census3 `--check` exits 0 at the claims base; `census2.json` is byte-identical to its
round-48 landing. Part (3): no round-50 calibration surface reads `census2.json`, so landing `census3.json` broke none of them.
Three findings the L1 must act on are outside the literal three asks and are listed first below.

## Findings for the L1 (ordered by impact)

1. **The round-52 landing will turn `census3 --check` red unless `census3.json` is regenerated.** Probe: at a fixture commit
   on `ab0eafed` adding the seven round-52 instrument rows the claims name (`gap-rule.json`, `c1-counter.py`, `c1-controls.py`,
   `c1-run.sh`, `fetch-vendor.py`, `sqfs-triage-v6.py`, `misroot-sweep.sh`), `census3 --check` exits 1 with
   `registry_paths 63, census_paths 56, census_outside` = those seven. Regenerating (`census3.py --generate --rev <fixture>
   --out tools/round-51/census3.json`) restores exit 0 at 63/63. The claims text does not name this regeneration step;
   the freeze or landing must include it, or the v6 `census_outside 0` binding cannot hold.

2. **The frozen round-48 `meanings.py` (R48-C1) is red at the round-52 base, and the round-51 landing made it red on a
   new row.** At `ab0eafed` (declared freeze `b6f7ca2a`, `--no-battery`) it exits 1 with `registry rows outside the census: 14`
   and `verdict maps not bound to meanings: 1`. The unbound row is `tools/round-51/census3.py`; its exit-0 cell
   `0=exact inventory equality or generation/selftest success` has no token from the frozen SUCCESS set
   (`met|clean|ok|green|pass|passed|verified|succeeded|wrote`; `success` is not in it). Measured `meaning_rows_failed`:
   0 at `f04b51dd` (round-51 claims draft), 1 at `02d667cb`, `96aee1a5`, `c525de54`, `ab0eafed`. The round-51 closure does
   not record this (its receipts show `meaning_rows_failed 0` only at `f04b51dd`). R48-C1 was already red at `f04b51dd`
   (`registry_extra 13`), so this is an added failing clause, not a new breakage class.

3. **The frozen round-50 C2 counter (`c2-record.py`, freeze `435d41fd`) exits 1 at every rev from `02d667cb` on, with
   all eleven atoms passing.** Its battery's `duplicate line` mutations for B3, B4, B5, B10, B11 are no-ops
   (`red [] noop []`), so the battery is not green. At `f04b51dd` the same command exits 0 with an empty battery failure
   list. Causal probe: fixture = `f04b51dd` + one appended trailing SCORECARD section (`## Probe section`) → exit 1, the same five
   battery failures. Mechanism (code reading, consistent with the probe): `c2-record.py:1132` appends the duplicate correction line
   at end-of-file, and `corr()` only scans the `## Record corrections — round 50` section; once any section trails it, the
   mutation falls outside the scanned span and is a no-op. Round 51 appended `## Round 51` at `02d667cb`, which is the first
   bad rev. **The round-52 SCORECARD round section, appended at EOF, will reproduce this.** Atoms (exit 0 semantics) are
   unaffected; only the battery verdict is red.

4. **`census2.json`'s per-claims-file naming map is stale against its own rule.** Paths match a fresh derivation at
   `7fe11332` (landing), `dc73587a` (A1 freeze), and `ab0eafed` (paths 42 = 42, `named_but_absent []`), and the full document
   matches at `7fe11332` and `dc73587a`. At `b6f7ca2a` (declared freeze, after amendments A2–A8) and at `ab0eafed` the
   `plans/round-48-claims.md` entry names `tools/round-47/exact.py` in addition to the four committed names. The frozen
   `meanings.py` compares `paths` only (`census_rederived_equal`), so it stays silent on this. Frozen bytes stay untouched (per
   the freeze); this is a latent naming-map drift, not a census-count regression. The L1 should record it, not fix it in-round.

5. **The historical census_outside at the claims base is 14, not 13.** `census3 --historical` at `ab0eafed` exits 1 with
   `census_outside` 14 (`registry_paths 56`, `census_paths 42`). The fourteenth is `tools/round-51/census3.py`, registered at
   `96aee1a5`. At the round-51 claims draft `f04b51dd` the value is 13 (matches the round-51 claim text). The round-52 claims
   text (`census_outside 0 both sides`, and "13" in the R52-C2 before-state narrative) should read 14 for the historical arm.
   `--check` (the no-regression binding) is 0 and is the binding that matters.

## Part-by-part results

### (1) census3 at `ab0eafed` (second reader; the same command the claims name)

| command | exit | key fields | receipt |
|---|---|---|---|
| `python3 -I -B tools/round-51/census3.py --root . --rev ab0eafedc41402b43b41a4362084119578dfe7ce --check` | 0 | registry 56, census 56, outside [], unregistered [], duplicates [] | `census3-check-base.json` (stdout sha256 `6b2484fc…07bff`) |
| `… --historical` (same rev) | 1 (expected) | registry 56, census 42, census_outside 14 (see finding 5) | `census3-historical-base.json` (sha `92d0a75b…2ca912`) |
| `… --selftest` | 0 | 20 cases, failures [] | `census3-selftest.json` (sha `d2f8664f…229e3`) |

Also at the round-51 claims draft `f04b51dd`: `--historical` exit 1, outside 13 (matches the round-51 claim); at the round-51 landing
`96aee1a5`: `--check` exit 0; `--historical` exit 1, outside 14.

### (2) `tools/round-48/census2.json` frozen state

- `sha256` at worktree, `7fe11332` (round-48 landing, the only commit touching the file), and `ab0eafed`:
  `403b4c143b020f1a30905258543758b11992dbd2235358575fb09f63473d7b59`, identical. `git log -1 --format=%H -- tools/round-48/census2.json`
  = `7fe11332781356ec3d5b0b314698de27dd25b50d`. **Not changed since the round-48 landing.** Receipts in `receipts-index.json`.
- Re-derivation with the frozen `census2.py` (`census_text`) at `7fe11332` and `dc73587a`: full document equal to committed.
  At `b6f7ca2a` and `ab0eafed`: paths equal, `per_claims_file` not equal (finding 4). Re-derive at `ab0eafed` exits 0 (`census2.py`
  itself), `census2-rederive-at-base.json`.

### (3) consumers of `census2.json` and the round-50 calibration surfaces

Grep over tracked files (`git grep -ln census2\.json`, excluding wave dirs): `SCORECARD.md`, `SKILL.md`, a knowledge entry, several
lesson and plan files (text only), `tools/round-48/census2.py` (generator), `tools/round-48/meanings.py` (R48-C1 counter, loads
`tools/round-48/census2.json` by path), and `tools/round-51/census3.py` (historical mode only). Named calibration surfaces
checked:

- `tools/round-50/c2-record.py`: 0 occurrences of `census2`. Its registry check (B9) reads only `SKILL.md`'s instrument-registry
  rows and `tools/round-49|50/**` at base/rev. Does not read `census2.json` or `census3.json`.
- `tools/round-50/selftest-r49-c2.py` and `selftest-r49-c2.expected.json`: 0 occurrences. Counter pin
  `9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d` matches `tools/round-49/c2-mismatch.py`. Run at
  `ab0eafed`: `exit_code 0`, `passed 40`, `failed []` (`selftest-r49-c2-at-ab0eafed-harness.json`).

Conclusion: landing `census3.json` broke none of the round-50 calibration surfaces; they do not read it, and `census2.json` is
untouched. The only consumer of `census2.json` that is still live is the frozen R48-C1 `meanings.py` (finding 2).

## Receipts (scratch removed after copy)

- `ScoutCensusRecheck/receipts-index.json`: per-command argv, cwd, UTC, exit code, stdout sha256 and stdout tail.
- `ScoutCensusRecheck/census3-*.json`, `meanings/*.json` (R48-C1 at `b6f7ca2a` freeze over `f04b51dd`, `96aee1a5`, `02d667cb`,
  `ab0eafed`), `c2/*.json` (`c2-record` at `ab0eafed`, `c525de54`, `f04b51dd`, `02d667cb`, `96aee1a5`, the SCORECARD-append probe; the
  selftest harness run).
- Not captured as receipts (terminal-only, reported as observed): the `c2-record.py` run at its own freeze rev `435d41fd` gave
  `atoms_ok False` with "genuine REV is not green" and "no mutation realized" for B2, B6–B9, B11. Not investigated (out of this
  seat's question); the L1 should not cite `c2-record` at the freeze rev.

## Scope notes

- `ExecCensusCheck` outputs were not read. Only the repo, the frozen tools and my own fixtures were used.
- Fixtures were in `git clone --shared` copies only; every git call named `-C`; identity set in the fixture clones only;
  the toplevel was asserted before each commit.
- Lane untouched; `git status` at the lane showed other seats' untracked wave dirs (`.ufo/waves/round-52/l1/`, `w1/`) and a modified
  round-50 wave file from others. Not mine; not touched.
