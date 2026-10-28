# R45W1CritC1 — R45-C1 attacked before data (scoped findings)

Full report, attacks and every receipt:
`.ufo/waves/round-45/w1/R45W1CritC1/report.md` + `receipts.json` (command, exit, stdout sha256, UTC
per run). No installs. Lane tree read-only; `git log FREEZE..HEAD -- plans/round-45-claims.md
tools/round-45/` is empty and `git status --porcelain` on both is empty.

## Verdict

The landed artefact at HEAD is genuine (ten semantic rows, five arms, real 11-case selftest:
exit 0, `cases=11 failures=0`). **The predicate is not a discriminator: 10 forgery fixtures score
`met_target: true`.** `failing == []` certifies markup shape, not the depth work.

1. do-nothing → exit 1. **Sound.** (Real lane freeze..freeze also 1.)
2. garbage rows → **exit 0.** Eight `| lorem i | ipsum | i%3 | dolor |` rows pass.
3. `rule_blocks == 22` is a `^- \*\*` bullet count, not a rule index: a block labelled "7." plus two
   `- **scratch note.**` bullets → **exit 0**; conversely any extra unrelated bullet (or a `###`
   subheading bullet) makes a genuine block **exit 1**. Header matching is substring
   (`harm`, `no-exit-code`) → **exit 0**.
4. citations: four off-topic ranges → **exit 0**; four self-citations to `plans/round-45-claims.md`
   → **exit 0**; **bare paths with no line at all** count as "located" → **exit 0**. The claims file's
   "provenance is stated as exact path equality" is therefore false for the citation clause. One of
   the real block's seven refs is off-topic (`corpus/knowledge/2026-10-25-r34b-…:40-66`, SONAME
   multisets) and is accepted by design.
5. interpreter binding: a 4-line stub printing `PREFLIGHT_SELFTEST: cases=11 failures=0` → **exit 0**.
   The counter's own golden case scores `STUB_OK` (`c1-counter.py:251-253`, `:274-276`), so its
   selftest cannot demonstrate the binding — it proves a script printed a line.
6. extra: SKILL.md heading without the trailing space → IndexError, **empty stdout, exit 1**; a
   could-not-evaluate is reported as "claim not met".
7. extra, negative result: evil merge appending to both frozen paths → **exit 2**
   `frozen_path_changed`. The freeze arm holds; I report no defect.

**Cheapest green artefact:** `fx-a6-cheapest-green` — 44 lines total (21 plain bullets + 8 garbage
rows + 4 `:1` refs + a 4-line stub interpreter), exit 0, sha256 `34336cf7…`,
2026-10-28T15:42:01Z. Zero freeze-integrity content. The frozen-path arm does not close this: it only
forbids changing `tools/round-45/` after the freeze, so a content-free *freeze* passes forever.

## Axes

- **depth** (the claim's axis): over-credited unless the report restates the structural limit.
- **calibration**: crash reads as 1, not 2; the claim's "located citations" is not computed.
- **provenance**: four refs can be four lines of the claims file.

## Smallest safe correction (round-46 instrument, not a wave-1 edit)

Require the seven named red cases (`red-touched`, `red-restored`, `red-dirty`,
`red-dirfreeze-no-pathspec`, `red-unknown-freeze`, `red-nonancestor`, `red-bulk-sweep`) to appear in
`--selftest` output with `"ok": true` — kills the stub. Then (optional) require `0/1/2` each present
in the exit column with `arm` cells naming declared arms, and require `:line` on every counted ref.
The graded block at SKILL.md:587-589 already discloses the structural limit; cite it in the landing
instead of claiming the counter proves the depth.

## Not run

C2 (other seat), renamed frozen directories, submodules, shallow/replace histories.
