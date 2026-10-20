# ConnDefectCriteria — six R17 routed defects → QUALITY captured-by

Seat: `KaidokuR18.ConnDefectCriteria` (author-side advisory). Read-only lane work; no REA/Ghidra/carrier execution.
Baseline: `9011581d84527ba34c675f9cf912e54d2e72d470` (`git rev-parse refs/heads/main`, exit 0). `corpus/QUALITY.md` is unchanged vs. baseline (`git diff --stat 9011581 -- corpus/QUALITY.md` empty, exit 0); its admission rows are `:11-:30` (rows 1–20).
Target: `corpus/lessons/round-17-verifier-spotcheck.md:137-147` (six defects). Legend: **[obs]** = observed by a command pasted in §Repro; **[inf]** = inference from those observations.

## Verdict

**[obs]** Four of the six defects are fully governed by existing admission rows (`#19` on PINMAP; `#18` on VALIDATE16 and PRODUCER-REV; `#4/#1` on S032-DIGEST); one is partially governed (SUMS-RUNLOG: `#18` for the run-log facet, `none` for manifest coverage); one has no QUALITY row (REGISTRY; `PROTOCOL.md:414-416`).
**[inf]** Exactly one new admission criterion is warranted: **#21, sharpening #19** — a retention claim names each retained field, and a comparator verdict is never described as the compared object. This matches `claims.json` C1's declared `QUALITY data rows 20 -> 21`. Minting one row per defect would overfit six prose incidents into four duplicate #18 rows and break the declared 20→21 budget.

**[obs]** The load-bearing recurrence is visible at `d0ab299:.ufo/waves/round-17/tools/carrier-run.py:475` — the writer's own comment says "Every check is retained with its instant (QUALITY #19), not only drift", then `:481-487` appends only `{taken_at_utc, equal, entries, changed, missing}`. The criterion was read and still satisfied by a verdict record. That is the argument for #21: #19 states *what* must be retained, not *which field names* the claim may use.

## Table — directly usable as `## Mistakes` rows

Columns match `corpus/lessons/round-17.md:79` (`class | evidence | captured-by | fix`); the new-criterion verdict is carried in the captured-by cell.
Abbreviations: `spotcheck:N` = `corpus/lessons/round-17-verifier-spotcheck.md:N`; `d0ab299:.../X` and `da64646:.../X` = `git show <rev>:.ufo/waves/round-17/X`; `9011581:.../X` = `git show 9011581:.ufo/waves/round-17/X`. Full commands in §Repro.

| class | evidence | captured-by | fix |
|---|---|---|---|
| vacuous — R17-PINMAP | `round-17-verifier-spotcheck.md:137`; `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:29-32` says each pin map is retained pre/mid/post; `d0ab299:.../carrier-run.py:481-487` appends only `{taken_at_utc, equal, entries, changed, missing}`; `d0ab299:.../runs/pro-aether/receipt.json` has 3 such entries, no map/digest [obs] | **#19** (`corpus/QUALITY.md:29`: the map at every named instant that the sentence asserts; the outside reviewer names #19 at spotcheck `:108`); **new #21 warranted** (`sharpens 19`) | retain `mid-<n>.json` + `map_sha256` (`contract.md:128-129`), append the named correction (knowledge/SCORECARD), and have `receipt-validate.py` recompute the digest; red case: tampered mid map |
| number-drift — R17-VALIDATE16 | `round-17-verifier-spotcheck.md:138`; `SCORECARD.md:2364` "all 16 receipts … exit 0" and `corpus/lessons/round-17.md:122` "All 16 receipts pass the final validator"; `9011581:.../verification.json` retains 8 per-label `receipt-validate-*` stdout triples, i.e. 8 retained validator executions against 16 claimed [obs] | **#18** (`corpus/QUALITY.md:28`: each claimed execution retains its producing argv/stdout/exit); **no new row** | retain the validator summary over `da64646:.../runs/*/receipt.json` (`contract.md:33-35`) and state `retained/total`, not a bare "all 16" |
| attribution — R17-PRODUCER-REV | `round-17-verifier-spotcheck.md:139` reports the second-pass producer as `95e34db` (commit time 11:27:35 -0300 = 14:27:35Z, six seconds before the first retained receipt at 14:27:41Z), before S `d0ab299` (11:47:24 -0300 = 14:47:24Z); `d0ab299:.../pro-aether/receipt.json` has no `carrier.md5_pre`/`binding.md5_ok` [obs: timestamps and field absence; producer hash from the spotcheck] | **#18** (`corpus/QUALITY.md:28`, "producing argv/snippet, measured revision"; #8's version-pinning principle is a secondary touch, not the governing row); **no new row** | append the producer revision per pass (`contract.md:36-37`) and add `producer_rev` + tool sha256 to the receipt so prose cannot misattribute; a new criterion would only restate #18 |
| number-drift / reference-drift — R17-SUMS-RUNLOG | `round-17-verifier-spotcheck.md:140-143`; `9011581:.../predictions/SHA256SUMS` has no `predictions/carriers.tsv` line (present at `2711674:.../SHA256SUMS:5`); pass-1 `da64646:.../runs/run-log.txt` has 7 `start` lines for 8 `carriers.tsv` rows and no final exit line [obs] | **#18** for the run-log facet (`corpus/QUALITY.md:28`, stdout/exit); **none** for manifest coverage — no row requires a frozen manifest's covered set to equal the set it was made for; **no new row** | restore the line, append `R17-SUMS-RUNLOG` with `7/8` (`contract.md:38-40`), and assert manifest set == `carriers.tsv` set in controls (tooling, not a row) |
| reference-drift / scope — R17-REGISTRY | `round-17-verifier-spotcheck.md:144-146`; `SKILL.md:540-542,545` rows omit pinned-value path/write scope; `SKILL.md:448` registers citation-drift as `probe` while its registered `--strict` entry exits 1 [obs] | **none** (no QUALITY row); the governing rule is `PROTOCOL.md:414-416` (required row fields: name; `gate\|probe`; entry command; verdict map; self-test command and spelling; pinned-value path; write scope; owner); **no new QUALITY row** | fill the 5th cell on the four rows; register citation-drift as `gate`; add a registry lint (required fields; kind vs reachable exit 1) |
| reference-drift — R17-S032-DIGEST | `round-17-verifier-spotcheck.md:147`; `corpus/SOURCES.md:38` anchor carries page sha256 `436c0f63…`; two fetches gave `028dbb7d…` and `f3841de0…` [obs from the spotcheck; not re-fetched here] | **#4** (`corpus/QUALITY.md:14`, "stable identity") with **#1** (`:11`, resolvable external document) as the source-row base; **no new row** | anchor on title+state and qualify the digest as fetch-time only; append the `supersedes S032 —` row (`contract.md:44-45`) |

### Criterion verdict, one line each

- **R17-PINMAP** — captured-by #19; **new #21 yes** (`sharpens 19`). #19 was read and misapplied (`carrier-run.py:475`); #21 adds the field-vocabulary clause.
- **R17-VALIDATE16** — captured-by #18; **no**. The sentence is an execution tally missing 8 records; #18 already requires them.
- **R17-PRODUCER-REV** — captured-by #18; **no**. The durable fix is a receipt field (`producer_rev`), not more prose.
- **R17-SUMS-RUNLOG** — captured-by #18 (run-log) / none (manifest coverage); **no**. The manifest facet is a controls assertion, not an admission criterion.
- **R17-REGISTRY** — captured-by none; **no QUALITY row**. This is operability substrate (`PROTOCOL.md:414-416`); a registry lint is the right instrument, and a second new row would break C1's 20→21.
- **R17-S032-DIGEST** — captured-by #4/#1; **no**. A dynamic-page digest is not a stable identity; qualifying it fetch-time restores #4 compliance.

## Notes that affect integration

1. **PINMAP is a documentation-time defect, not a run-time failure.** [obs] #19 at `da64646` required only pre/post maps; the mid-run clause and the knowledge sentence both landed at `d0ab299` (S, 14:47:24Z), after the second-pass runs. `git log -S 'each pin map is retained'` points at `d0ab299`; `git show da64646:corpus/QUALITY.md | grep -c 'including mid-run checks'` → 0 (exit 1), at `d0ab299` → 1 (exit 0). [inf] The Mistakes row should say the sentence was written about the runs without reading `pin_checks`, not that the runs measured incorrectly.
2. **#19 is the correct captured-by even though it was amended in the same commit as the claim.** The outside reviewer's partial disagreement itself says "not the per-path map QUALITY #19 itself requires" (`round-17-verifier-spotcheck.md:108`). #21 should not supersede #19; it narrows what a retention claim may assert.
3. **#18 is overworked but correctly so.** Three defects are execution-evidence-retention failures on three surfaces (validator runs, receipt producer, run-log stdout/exit). That is one row doing one job; the fix is enforcement, not new vocabulary.
4. **S032's #4 mapping is the only inferred extension.** [inf] #4's subject is "the artifact under analysis"; applying its stable-identity clause to a SOURCES anchor is an extension. #1 (resolvable source) is the fallback. The repair (title+state + fetch-time qualifier) holds under either reading.
5. **Do not add a Signals row for S032 in this round.** [inf] It would not change admission rows 1–20, but if `controls.py` counts every numbered QUALITY row, it would contradict the "rows 1–20 identical / 20→21" control. Keep the round at one appended admission row.

## Frontier move (one bounded proposal)

**Mint #21 narrowly, and make #18 mechanical instead of minting four more rows.** Add one `claims-join` check (in `W18/controls.py` or `verify.py`) that reads SCORECARD/lesson prose for retention/execution claims of the form `all N`, `N/N`, `8/8`, and requires N retained labelled records, emitting `retained/total` in the finding. Red case: `SCORECARD.md:2364` at `9011581` (16 claimed, 8 retained) → exit 1; green case: the corrected sentence after `W18/evidence/validate16/summary.json` and the restored run-log.

- **Affected axes:** calibration (mapping precision; one row, not four; keeps 20→21), operability (runnable join; no REA/Ghidra dependency), depth (unchanged — no carrier analysis).
- **Risks:** (a) over-broad prose extraction produces false reds and becomes a vacuous gate (a repeat of the `da64646` validator-on-wrong-shape lesson); scope it to lines containing a retention/execution verb and require the matched sentence plus the retained label set before exit 1. (b) `146 entries` in `pin_checks` is not a run count — exclude `entries` from the tally grammar. (c) The #21 DraftQualityRow21 clause "A retention claim names each field the producing tool retains" could be read to cover counts and overlap #18; keep #21's subject = field vocabulary, and let the join check carry counts. (d) A historical count explicitly labelled as historical must be green; add that selftest case.
- **Verification:** `routed-defects.py --root LANE --rev REV --strict` (C1 check c consumes the #21 why-cell); `controls.py BEFORE AFTER` (rows 1–20 byte-identical, row 21 appended); the join check on `9011581` → exit 1 naming `SCORECARD.md:2364`; on the corrected revision → exit 0; selftest includes the historical-number green case. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution.

## Reproduction (commands and exits)

All run in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only Git objects; no writes, no `jj`, no installs.

```text
git rev-parse refs/heads/main
→ 9011581d84527ba34c675f9cf912e54d2e72d470                                  exit 0
git show d0ab299:.ufo/waves/round-17/tools/carrier-run.py | awk 'NR>=475&&NR<=487'
→ comment "Every check is retained … (QUALITY #19)"; append has 5 keys       exit 0
git show d0ab299:.ufo/waves/round-17/runs/pro-aether/receipt.json | python3 -c '…'
→ n= 3; keys= ['changed','entries','equal','missing','taken_at_utc']; has_map= False; has_md5_pre= False  exit 0
git show 9011581:.ufo/waves/round-17/verification.json | grep -oE 'receipt-validate-(calib|pro)-[a-z0-9.-]+\.stdout' | sort -u | wc -l
→ 8                                                                          exit 0
git show 9011581:.ufo/waves/round-17/predictions/SHA256SUMS | grep -c 'predictions/carriers.tsv'
→ 0                                                                          exit 1 (no match)
git show 2711674:.ufo/waves/round-17/predictions/SHA256SUMS | grep -c 'predictions/carriers.tsv'
→ 1                                                                          exit 0
git show da64646:.ufo/waves/round-17/runs/run-log.txt | grep -c ' start '
→ 7                                                                          exit 0
git show da64646:.ufo/waves/round-17/predictions/carriers.tsv | wc -l
→ 8                                                                          exit 0
git show da64646:.ufo/waves/round-17/runs/run-log.txt | grep -c -i 'exit'
→ 0                                                                          exit 1 (no match)
git show da64646:corpus/QUALITY.md | grep -c 'including mid-run checks'
→ 0                                                                          exit 1 (no match)
git show d0ab299:corpus/QUALITY.md | grep -c 'including mid-run checks'
→ 1                                                                          exit 0
git log -S 'each pin map is retained' --oneline -- corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md
→ d0ab299 round-17: w2 integration … (source revision)                       exit 0
git show -s --format='%h %ci' 95e34db d0ab299
→ 95e34db 2026-10-20 11:27:35 -0300 / d0ab299 2026-10-20 11:47:24 -0300      exit 0
git diff --stat 9011581 -- corpus/QUALITY.md
→ (empty)                                                                    exit 0
```

Other read-only observations used above: `corpus/QUALITY.md:11` (#1), `:14` (#4), `:28` (#18), `:29` (#19); `corpus/lessons/round-17.md:79` (Mistakes columns), `:122`; `SCORECARD.md:2364`, `:2374`; `SKILL.md:448`, `:540-542`, `:545`; `PROTOCOL.md:414-416`; `corpus/SOURCES.md:38`; `contract.md:30-32,33-35,36-37,38-40,44-45,128-129`; `corpus/lessons/round-17-verifier-spotcheck.md:108,137-147`.

## Limits

- [obs] Working tree showed `M .ufo/waves/round-17/tools/compare.py` and untracked `.ufo/waves/round-18/` — sibling state, not touched. `corpus/QUALITY.md` unchanged vs. baseline.
- [inf] The S032 fetch-instability is taken from the spotcheck's report (`:147`); this seat did not re-fetch (network not needed for the mapping).
- No new criterion was executed; #21's wording is the peer draft's (`w1/DraftQualityRow21.md`), assessed here, not edited.
- Tools installed or updated by this seat: **none**.
