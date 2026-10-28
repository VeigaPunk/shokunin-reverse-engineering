# C1RowsA — scoped findings

## Behavior and gates
The frozen claims file was read in full before any command. It requires a first-half alphabetical-path analysis of registry rows that score failing under `tools/round-48/meanings.py` at freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`. No meanings counter run was performed in this seat. Existing diagnostics at `.ufo/waves/round-48/w1/C1Struct-2/meanings-dc73587a.json` report only `marker_occurrences 0 != 1` and `marker_block_count 0 != 1`; the battery was skipped because the artefact fails structural clause first. They do not enumerate failing registry rows. Therefore no row can responsibly be represented as having scored failing from this available output.

The source tools census lists the instrument paths at `tools/round-48/census2.json:3-45`; the declared census rule is at line 2. The registry acceptance predicate, including exact equality to the census path set and meaning classes for 0/1/2, is specified at `plans/round-48-claims.md:60-65`. These rules establish the intended scope but not which registry rows actually fail.

## Draft verdict-map cells
No rows are listed: the required failing-row population was not observed. Drafting meanings for a guessed subset would misstate coverage and violate the requested evidence basis. In addition, the frozen SKILL registry content at `dc73587a...` has not been inspected for its actual old cells or tool-specific exit meanings. No new cells are asserted.

## Touched surfaces
Only this report was written. No product code, frozen bytes, sibling lane or fleet files were changed. No tools installed. No fixture repo created. No scratch created or removed.

## Findings and limits
The command `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` was run and reported `/tmp` 19% used (104.8G free), `/var/tmp` 38% used (556.5G free), and `/fast/scratch/hyaku` 32% used (549.7G free). Lane `git status --porcelain` showed extensive pre-existing unrelated changes, including `tools/round-48/meanings.py`; no changes were made to them. The freeze commit resolves successfully. No exit-contract checks, per-tool source reviews, per-row counter results, or command receipts with UTC timestamp/stdout hash were produced. Coverage, depth, and calibration for the requested cell draft are thus incomplete; this report is not a claim that any gate passed.

## Artifacts
- Report: `.ufo/waves/round-48/w1/C1RowsA.md`
- Cell table: none (failing rows not enumerated)
- Receipts: none
