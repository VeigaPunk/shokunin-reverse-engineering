# W2 CensusEnd — fleet census at lane tip (kaidoku, round 27, attempt 1)

Seat: KaidokuR27.CensusEnd · 2026-10-22 · attacks: "Run the fleet census at the lane tip" plus
row counts at cd32264f and main. No installs performed (tools used: bash, git 2.x, GNU grep
3.12-modified, gawk via census script — all pre-existing). No lane mutation: only read-only
`git rev-parse` / `cat-file -t` / `show` / `cmp`; no jj commands; no refs touched.

## Check 1 — fleet census validate at tip
- Command: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
- Time: start 2026-10-22T15:37:04Z, end 2026-10-22T15:37:04Z · exit code: 0
- Output excerpt (full transcript in census-validate.out):
  ```
  kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
  kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
  kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
  kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
  kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
  ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
  ```
- Observation: zero E-codes; only W04 (warning class; script header: "W04 … warnings do not
  affect clean lanes"), and exit 0 which per the header means clean or warnings.
- Provenance (observation): `git -C <lane> rev-parse main` → `4084d8975b684a8837b1c858eea0008ce9ab49e0`
  (exit 0), exactly the tip under attack; `cmp` of working-copy `corpus/SOURCES.md` against
  `git show main:corpus/SOURCES.md` → IDENTICAL (exit 0), so the validated file is the tip content.
- Verdict: **holds** — census validates clean (exit 0) at the lane tip; W04 warnings are recorded,
  non-failing, and already-covered round behavior (duplicate URLs across scopes).

## Check 2 — SOURCES row counts at cd32264f and main
- Command (exact, as assigned): `git -C <lane> show <REV>:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'`
- Time: 2026-10-22T15:37:04Z · exit code: 0 both
- Output: cd32264f7ee356a9c0f48bd8e3fcdac222db22a0 → **80**; main → **82**; tip 4084d897 → **82**.
- Observation: `git -C <lane> show main:corpus/SOURCES.md | cmp - <lane>/corpus/SOURCES.md` exit 0
  (main blob == validated working copy), so 82 is also the row count of the file the census validated.
- Delta check (observation): row-id scan of both blobs — 80 unique ids at base, 82 at main, no
  duplicates, added exactly `S081`, `S082`, removed none; all row lines start at column 0.
- Verdict: **holds** — counts reproduce at base and tip; delta is exactly the two round-27
  SOURCES rows (S081 rea-agents tarball, S082 tinyxxd pacman desc) claimed as landed.

## Escape-hazard note (reporting integrity, observation)
An initial scripted run printed 159/165 for check 2. Root cause was my harness, not the command:
a Python f-string doubled the backslashes (`\\|`), turning the ERE into alternation whose empty
branch matches every line (159/165 are the blobs' total line counts, confirmed by `grep -cE '^'`).
The canonical single-backslash command gives 80/82, corroborated by a bracket-pipe variant
`^[|] S[0-9]{3} [|]` (80/82) and by row-id scans. Counts of record: 80 and 82.

## Residual risk and verification gaps
- W04 duplicate-URL warnings (S033, S047, S054, S062, S069) are unresolved by design (warning
  class, per-round policy); I did not re-judge them — out of my item's scope.
- Census content accuracy (URLs reachable, teaches text quality) is not what validate checks;
  not evaluated here. [INFERENCE on scope, flagged for the round, not a defect.]
- `git rev-parse main` reflects the local ref; I did not consult jj state (bounds discourage it;
  rev-parse exit 0 matching the named tip is sufficient identity here). Unknown beyond that.

## Artifacts (under /fast/scratch/hyaku/kaidoku-r27/seats/w2/CensusEnd/)
- `census-validate.out` — full census transcript, command, timestamps, exit · sha256
  ec5dced5c39c4881a40ac2d96bc9b200547b7498d64c1969610041263428e28b
- `counts.md` — canonical counts, control variants, id delta, escape note · sha256
  bfea8aae5f3bba4ffdf50a2cf36ded4e789fca459d34d9d9df84434ec8a360ae
- `summary.json` — machine summary of all checks · sha256
  6713e9483d2158ba63f6d6c1ebb64891bfa9bbcac8b49d50bf442e636393098e

Overall: **holds** — census exit 0 at the tip (W04 warnings only), row counts 80 (cd32264f) → 82
(main == 4084d897), delta exactly S081+S082.
