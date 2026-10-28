# C2GoldForgery — gold-forgery attack on R49-C2 (calibration), pre-freeze draft

Seat: C2GoldForgery (leaf, no dispatch). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Scratch clones only (`mkclone.sh` + `c2-after.py` + in-clone forgery commits); lane tree read-only (lane `git status` shows only the untracked `?? .ufo/waves/round-49/` wave tree). Scratch removed; receipts in `w1/C2GoldForgery/`.

## Verdict

**NOT gold-proof. Fold before the freeze.** Fourteen single-edit repository states are green in plain mode (exit 0, `mismatches 0`); twelve of them are also green with `--battery` (`battery.failing []`), and the freeze spoof F14 is green with `--battery`: 13 green in battery mode. The battery proves that each atom *can* go red under its own mutation; it does not prove that a forged-but-consistent state cannot go green. The draft honest fixture (dev-after) is green and the freeze reads `mismatches 9` as the plan says, so the instrument works on the honest path and fails open on the forged path.

Live re-open today (not a forgery finding, a fact): the draft snapshots are byte-equal to the live sources (SEP `popper/` HTTP 200, 118,135 B, sha256 `2c2d48c6…` = draft `popper.html`; man7 `sysexits.h.3head.html` HTTP 200, 12,725 B, sha256 `d9db4b96…` = draft `sysexits.html`, body contains `EX_USAGE 64`). The counter cannot see this; it is consistency-only.

## Method and reproduction

- Baseline: `mkclone.sh` → `DEV_FREEZE=dd40bdd4bcc9c9787208188f23d47f58964be790`; `c2-after.py` → `DEV_AFTER=df61876694a6fea234faf65d7c6ef9e05b8e6691`.
- Counter (draft, sha256 `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f`, recorded in every receipt as `counter_sha256`):
  `python3 -I -B .ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py --root <clone> --rev <REV> --freeze dd40bdd4bcc9c9787208188f23d47f58964be790 [--battery] --json-out <out>`
- Each forgery: `git checkout -f --detach DEV_AFTER`, `git clean -fdq`, assert `git rev-parse --show-toplevel` = clone, apply edit, commit in the clone (identity `r49-dev` set by mkclone), run plain and `--battery`. Harness `forge.py` and every JSON receipt are in `w1/C2GoldForgery/`.
- Baseline (honest dev-after, `--battery`): exit 0, `mismatches 0`, `battery.failing []`, 11/11 mutations flip exactly their atom, do-nothing red 9/9 (5 paths). Freeze `--rev dd40bdd4 --freeze dd40bdd4`: exit 1, `mismatches 9` (matches the plan).

## Findings (green = exit 0 with `mismatches 0`; battery column = `--battery` exit and `battery.failing`)

| # | Forgery (edit committed in clone on top of DEV_AFTER) | REV | plain exit / mismatches | battery exit / failing | Why it passes | Fix before freeze |
|---|---|---|---|---|---|---|
| F01 | A4: three zero-byte stubs `.ufo/waves/round-48/w1/{C1Meaning,C1Battery,ScribeReportNumbers}.md`; lesson `reports=75 missing=` | `6f63d35e…` | 0 / 0 | 0 / [] | A4 `has` = path exists in `ls-tree` at REV; content not read. Plan sentence "a `.md` at `w1/<seat>.md`" permits an empty file. | Require non-empty blob; pin `.ufo/waves/round-48/**` tree to base (no added/removed files). |
| F02 | A4: `r48-w1-results.json` at REV with three seats removed; lesson `seats=72 … missing=` | `86afe169…` | 0 / 0 | 0 / [] | A4 reads results from REV, not from the base blob (`RESULTS48` via `r.show(rev,…)`). | Read results at `LANE_BASE` (equal to tip `8847042a`); assert blob equality. |
| F03 | A1: SCORECARD `## Round 48` `**Declared freeze:**` re-pointed `b6f7ca2a…` → `8847042a…`; lesson correction restated `declared=8847042a…` | `81101375…` | 0 / 0 | 0 / [] | A1 checks the correction line against the *edited* SCORECARD and the lesson header; nothing binds either to history (LOG, base SCORECARD). The "record" is judged against itself. | Read SCORECARD round-48 section from `LANE_BASE` blob and require equal to base value `b6f7ca2a…` (the A8 freeze). |
| F04 | A5: round-48 receipt `c1-final-33f65a91.json` edited at REV (one inserted space before first newline), `c1_raw`/`c1_stripped`/`report_c1` re-derived | `b592783b…` | 0 / 0 | 0 / [] | A5 derives digests from REV bytes; no comparison with base blob. Plan says "committed round-48 receipts", i.e. the round-48 bytes. | Require `show REV:<receipt> == show LANE_BASE:<receipt>` for both receipts before comparing digests. |
| F05 | A3: pointer `log_33f65a91=3440,3441,3444` deleted from the correction line (the pointer the closure called wrong) | `880ddccf…` | 0 / 0 | 0 / [] | A3 iterates only the keys the lesson states; plan says "states … the full set" but nothing enforces completeness. Cheapest forgery: one token. | Derive the set of hashes named in the round-48 entry/LOG and require `keys == set`. |
| F06 | A6: `popper.html` snapshot replaced with a synthetic page; fabricated quote "falsifiability is the criterion that the 2026 review board certified for all empirical sciences" put in S147's row; sha pin in row updated | `271325f2…` | 0 / 0 | 0 / [] (all 11 mutations still flip) | A6 checks snapshot ↔ row consistency and the snapshot's sha pin; no fetch receipt, no live re-derivation (network forbidden by design). Battery is blind to it. | Add a committed fetch receipt (URL, HTTP status, Date, bytes sha256) and disclose that snapshot authenticity is a non-counter limit; or re-fetch in wave 2 by a networked seat. Plan currently says "re-opened sources with committed sha256-pinned snapshots"; the counter cannot verify "re-opened". |
| F07 | A8: round-49 entry `identified 400, screened 2, …`; round-48 entry `identified 999, …` | `dc68caa7…` | 0 / 0 | 0 / [] | Counter checks only `idn >= scr`; `identified`/`screened` are never derived. **Counter docstring says "every number is re-derived from the registry"; the plan's disclosed limit says only rows and the included/excluded split are derived. Plan/docstring disagreement.** | Fix the docstring to the plan's limit, or state `identified` as an undeclared input. Do not claim it as checked. |
| F08 | A9: `corpus/lessons/round-48-verifier-spotcheck.md` admission flipped to `**admitted**`, `**Admitted** because`, plus a sentence containing the substring `rejected-harmed`; SCORECARD line unchanged | `bf60307a…` | 0 / 0 | 0 / [] | A9 tests substring presence of `rejected-harmed` anywhere in the REV source file, not the admission verdict; the source is read at REV, not base. | Pin the closure file to `LANE_BASE`; parse the `Admission:` verdict token and require it equal the SCORECARD verdict. |
| F09 | A4 shadowing: a false `- A4 seats=75 reports=75 missing=` line inserted above the correct A4 line | `b05c9838…` | 0 / 0 | **1** / `A4 reports count off by one -> red [] noop []` | Parser is a dict, last line wins; the counter never sees the false line. The battery fails only because its A4 mutation hits the shadowed line (no-op) — caught by accident, not by design. | Reject duplicate atom keys in every lesson/SCORECARD parser. |
| F10 | A2: `dead=663f30ee` + 32×`0` (non-commit, same 8-hex prefix) | `52155d1a…` | 0 / 0 | 0 / [] | Counter checks only that `dead` is not a commit; the cited dead hash lives in the fleet report, outside the lane, and is never compared. | Disclose; or cite the dead hash from a lane artifact. Low severity. |
| F11 | A3: `unnamed=577a02a5` (8847042a dropped) | `f88b22cf…` | 0 / 0 | 0 / [] | Only listed hashes are checked for "named at base"; no completeness check. | Same fix as F05 (derive the set). |
| F12 | A7: S148 teaches `EX_USAGE is 2, not 64` (inverts the convention) | `5d3d7a2c…` | 0 / 0 | **1** / `mutation set incomplete: 10 of 11` | A7 checks only that `EX_USAGE` and the token `64` occur in the cell; the claim is not semantic. Battery goes red only because its mutation text vanished. | Require the literal `EX_USAGE is 64` (or a structured field); make the battery fail on mutation-set incompleteness (it already does — keep it). |
| F13 | control: `popper.html` edited without re-pin | `8f7c8b32…` | **1** / A6 red | 1 / 11 | Correct: unpinned edit is caught. | none — shows the pin works as designed. |
| F14 | **freeze spoof**: counter tampered by one comment line (sha256 `3b1e8fec…` ≠ frozen `90fa4722…`), committed at X=`f246a6ce…` (a fork of DEV_FREEZE; first add of `tools/round-49` is `dd40bdd4…`); REV = AFTER tree + X's tools + F01 stubs; run with `--freeze X` | `6e993fc3…` | 0 / 0 (plain run with `--freeze X` exit 0) | **0** / [] | `freeze_check` trusts the operator's `--freeze`; no frozen byte names the freeze hash, and no check asserts FREEZE is the first commit adding `tools/round-49` or that the counter sha equals a pinned value. With `--freeze X` the do-nothing overlay restores the lesson to absent (all nine red), so battery passes. The same REV with the real freeze `dd40bdd4…` → exit 2 `frozen_path_changed` (correct). | Counter asserts `FREEZE == git log --diff-filter=A --reverse --format=%H -- tools/round-49 \| head -1` **and** the frozen plan states the counter's sha256 (the plan is inside the freeze, so the sha is fixed when the plan is written). The receipt must print the freeze hash it used and the plan must state it. |
| F15 | round-49 lesson header `Declared freeze \`0f06251b…\` (series A1–A4)` — the same defect class as M49-1 | `78888ccb…` | 0 / 0 | 0 / [] | No atom reads the round-49 lesson's own header; A1 covers only round-48. The plan says the M49-1 "fix is A1 plus its mutation" but A1 cannot see this file. | Extend A1 (pre-freeze) to: every "Declared freeze" line in `corpus/lessons/round-49.md` must equal FREEZE. |
| F16 | prose in round-49 lesson "the round-48 declared freeze is 0f06251b (A4)" | `9b379038…` | 0 / 0 | 0 / [] | Plan says the counter does not judge prose. Disclosed limit; listed for completeness. | Accept; keep the disclosure in the lesson. |

Counts: 14 green in plain mode (F01–F12, F15, F16); F09 and F12 are plain-green and their battery red is accidental (a mutation no-op and a missing mutation target). 12 green in battery mode (F01–F08, F10, F11, F15, F16) plus the freeze spoof F14 = 13. F13 is a control and behaves (red).

## Plan-vs-counter disagreements (for L1 to decide before freeze)

1. A8 scope: counter docstring "every number is re-derived from the registry" vs plan's disclosed limit (rows and included/excluded only). `identified`/`screened` are free inputs (F07).
2. A4 "report artifact": plan's own wording ("a `.md` at …") admits a zero-byte file (F01). Plan needs "non-empty, content-bearing" or a named content check.
3. "Committed round-48 receipts" (A5) and "SCORECARD record" (A1): counter reads REV bytes, not the base blob (F02, F03, F04, F08). The plan does not say which commit is the authority; the fix is to name `LANE_BASE` (or the tip `8847042a`) explicitly.
4. FREEZE identity: the plan's counting command takes `--freeze <FREEZE>` but no frozen byte names it (F14).
5. "Re-opened sources" (A6/A7): the counter verifies internal consistency only (F06); the plan should say so in the disclosed limits, not only the counter docstring.

## Minimum set to fold before the freeze (ranked)

1. Blob-equality pin of every round-48 input (`results.json`, closure file, round-48 lesson, both receipts, SCORECARD `## Round 48` section, LOG pointer region) to `LANE_BASE`, plus tree-equality for `.ufo/waves/round-48/**` (kills F02, F03, F04, F08; F01 via tree equality).
2. A4 content check (non-empty) (F01).
3. Derived completeness for A3 and reject duplicate keys in every lesson/SCORECARD parser (F05, F09, F11).
4. Freeze identity: first-add check + counter sha in the frozen plan (F14).
5. A1 extended to the round-49 lesson header (F15).
6. A7 literal claim `EX_USAGE is 64` (F12).
7. A8 docstring corrected; `identified`/`screened` declared as disclosed inputs (F07).
8. A6/A7 fetch receipt + disclosed limit that snapshot authenticity is not counter-checked (F06).
9. A2 dead-hash disclosure (F10), F16 disclosure.

## Receipts and artifacts (`w1/C2GoldForgery/`)

- `forgery-table.tsv`: per-label rev, plain exit, mismatches, battery exit, battery failing, do-nothing red count, sha256 of battery JSON and plain JSON.
- `forge.py`: harness (`forg` dict with every edit; `python3 forge.py <label-prefix>` against a clone at `/fast/scratch/hyaku/kaidoku-r49/C2GoldForgery/c0` built by `mkclone.sh` + `c2-after.py`).
- `base-battery.json` (+ `.stdout`, sha256 `4638ec6c6b5241478a70b112dfb93647653ffea0a89a307728f76e8c4731dc3a`), `fz.json` (freeze run, exit 1, mismatches 9), `spoof.json` (sha256 `7ac5a9b0…`), `spoof-plain.json` (sha256 `87106644…`), `spoof-real.json` (exit 2, sha256 `d6efacbf…`), `out-F*.json` and `.plain` for each forgery.
- `sep-live.html`, `man3head-live.html` with `live-sha256.txt`.
- Commit hashes of forgery REVs are scratch objects in a deleted clone; they are reproducible from the recipe above, but the hashes are not (commit timestamps differ).

## Tools

None installed. No pacman, no network writes; two read-only GETs (SEP, man7) for the live-sha check.

## Not run

Wave-2-style battery on frozen counters (outside this wave); C1 counter (other seat); data runs (forbidden).
