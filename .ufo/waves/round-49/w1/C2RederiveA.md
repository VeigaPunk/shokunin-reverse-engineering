# C2RederiveA — independent re-derivation of C2 atoms A1–A3 (2026-10-28, base e4f2cfa5)

**Verdict: numbers AGREE; counter binding is WEAK (4 green forgeries).** My script re-derives every A1/A2/A3 value from base git objects and matches the draft lesson lines in `c2-after.py` byte for byte (0 disagreements). But `c2-mismatch.py` a1/a2/a3 accept four forgeries that violate the plan sentences, so "A1–A3 green" does not bind to the closure's facts. Not run: A4–A9.

## Re-derivation (script `w1/C2RederiveA/rederive.py`, no counter import; `python3 -I -B rederive.py` exit 0, stdout sha256 of `rederive.json` = 53461ccf777b29bb…179b7)
| atom | independent value | draft lesson line (`draft-lesson-lines.txt`, sha256 b27e372b…0e00) | agree |
|---|---|---|---|
| A1 | SCORECARD `## Round 48` declares `b6f7ca2a6391964dfdedd477cd560bd42159873a` (= amendment A8, commit); lesson `round-48.md` header (line 4) names `0f06251bf6a3a6964c715f67243d4df12e854258` (= A4, commit, ancestor of declared); lesson table has rows A1..A8; its own header says "series A1–A4" | `declared=b6f7ca2a…873a stale=0f06251b…4258` | yes |
| A2 | `663f30ee7516942a0120e7de68fe88356e680822`: `git cat-file -t` rc=128 (not an object). Only commit with prefix `663f30ee` in `rev-list --all` (1706 commits) and in `rev-list base`: `663f30ee751694fb0970e7de68fe88356e680822` (commit, ancestor of base). Common prefix is 14 hex, not just 8 | `dead=…942a0120… actual=…94fb0970…` | yes |
| A3 | LOG.md at base (3450 lines): `2e785632` → 3440,3441,3445; `33f65a91` → 3440,3441,3444; `577a02a5`, `8847042a` → no line; all four are commits and ancestors of base | `log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a` | yes |

Also confirmed: the dev clone's LOG.md blob (de4985f7…) and round-48.md blob (0a5f82e2…) equal base; dev-freeze→dev-after counter run: freeze exit 1 `mismatches 9`, after exit 0 `mismatches 0`; `--battery` on dev-after exit 0 (`failing 0`, 11 mutations, do-nothing red 9). Nuance (not a disagreement): the closure cites LOG 3445 as "the commit line" for 2e785632; the full naming set the plan asks for is 3440,3441,3445, which the draft states.

## Findings (forgeries run on `mkclone.sh` + `c2-after.py` clone; fixtures: `/fast/scratch/hyaku/kaidoku-r49/C2RederiveA/clone` since removed; script `w1/C2RederiveA/forge.py`, output `forge-run.txt`, per-forgery JSON `fo-*.json`; each: `c2-mismatch.py --root <clone> --rev <forge> --freeze 6b4eb599… --json-out …` → **exit 0, mismatches 0**)
| # | forgery (lesson/SCORECARD edit on dev-after) | counter result | defect |
|---|---|---|---|
| F1 | A3 line → `log_2e785632=3440,3441,3445 unnamed=deadbeef` | exit 0, green | plan/docstring: "full set … per hash … and the hashes the round-48 entry never named". a3 checks only the hashes the lesson chooses to state; any ≥1 `log_` key plus any non-empty `unnamed` that is absent from LOG passes. The four closure hashes are not required. |
| F2 | A3 → `log_33f65a91=3440,3441,3444 unnamed=577a02a5` (drops 2e785632, 8847042a) | exit 0, green | same: partial set accepted |
| F3 | A2 → `dead=<base[:8]+32×0> actual=<base>` (unrelated real commit) | exit 0, green | docstring: dead = the hash round-48 report cited. a2 accepts any non-commit 40-hex sharing 8 hex with any ancestor commit; `663f30ee…` is never bound. |
| F4 | SCORECARD `## Round 48` Declared freeze rewritten to base hash + lesson A1 `declared=<base>` | exit 0, green | a1 reads the SCORECARD at REV, not at base (only `round-48.md` is pinned to its base blob); rewriting the SCORECARD declaration satisfies A1. |

Suggested fix (report only): pin expected constants/sets in the counter (dead hash `663f30ee…680822`, the four A3 hashes, A1 SCORECARD section blob-equal to base), and add mutations for each. Minor: `c2-after.py` docstring says it derives every number from committed bytes, but A1–A3 (and A6–A9) lines are hard-coded literals (equal to my derivation today).

## Receipts
- `python3 -I -B rederive.py > rederive.json` exit 0 (2026-10-28 UTC); sha256 rederive.py c9bd5f75…c545c, rederive.json 53461ccf…179b7, forge-run.txt ca66290f…88c2e.
- `mkclone.sh` → DEV_FREEZE 6b4eb599e1808acc9a8b887b9014ade8d5951def; `c2-after.py` → DEV_AFTER 86504a1ad5ce56157b9fe62e1001ca27c65eb08a (both rc 0). Counter @freeze rc 1, @after rc 0, battery rc 0.
- No tools installed. Scratch removed after copying receipts.
