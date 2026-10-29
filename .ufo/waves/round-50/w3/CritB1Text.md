# Verdict

**Conditionally accept the `140/140` value, but do not merely prepend it.** It is the correct projected attempt-2 denominator if the one planned C1 knowledge entry is the only new `.md` file. B1 will read that first count and the existing history will not shadow it. However, if “lead the row” means adding the new phrase while leaving the current `139/139 … at the round-50 landing` and “round 50 added no knowledge entry” wording unchanged, B1 can pass while the row retains an unqualified stale/current-sounding claim. Reword or replace that clause (or label it explicitly as attempt 1); this is a documentation defect the counter does not catch, not a B1 predicate defect.

## Findings

| Check | Finding / evidence | Exact command; exit; stdout SHA-256; UTC |
|---|---|---|
| B1 derivation and prefix | `b1` selects the sole coverage row, `re.findall`s all matching phrases, then compares only `fr[0]` with the `.md` count at REV. Current row prefix before its first matching phrase is only `9.72 → 10.0`; it contains no earlier `N/N knowledge files mapped`. A leading `140/140` will therefore be the checked value. | `git show f890bbead20ca2c549487167f56876ae47f1e1a4:tools/round-50/c2-record.py`; exit 0; SHA-256 `4749bcd86c8f61bfb6994baeab3bd990b61ea0c369b87197351d0a4618e71285`; 2026-10-29T20:36:21Z |
| B2 / neighboring atoms | B2 selects the `calibration` row separately and checks its own verdict, closure/receipt references, and mismatch expression. Changing only coverage-row text does not alter B2. B3–B5/B11 read correction and round-48/49 sections; B6–B8 read SOURCES rows; B9 reads the registry; B10 checks the self-test/correction. No other atom reads the coverage row. | `git show f890bbead20ca2c549487167f56876ae47f1e1a4:tools/round-50/c2-record.py`; exit 0; SHA-256 `4749bcd86c8f61bfb6994baeab3bd990b61ea0c369b87197351d0a4618e71285`; 2026-10-29T20:36:21Z |
| Historical counts / counterexample | `fr[0]` means later 138/138, 133/133, etc. do not affect B1. The same first-only rule also ignores a trailing 139/139: a prepended 140 plus the untouched old “round 50 added no knowledge entry” text can score B1 green while leaving an ambiguous/conflicting assertion. | `git show f890bbead20ca2c549487167f56876ae47f1e1a4:SCORECARD.md`; exit 0; SHA-256 `b7e11602738cd167ab4b56463316566539956a9f9631ce2485d09cafd2200790`; 2026-10-29T20:36:21Z |
| Attempt-2 count | Exact requested command returned **139** `.md` files at base. Current claims name one C1 knowledge entry; C3 adds no knowledge file, so 140 is correct if that is the only added entry. This is a projection: no landing entry/count has been observed yet. | `git ls-tree -r --name-only f890bbead20ca2c549487167f56876ae47f1e1a4 -- corpus/knowledge \| grep -c '\.md$'`; exit 0; stdout `139\n`; SHA-256 `690e07064753123c967bbac0180f32da6a753a5bd8b79a47644cef58e776d9f0`; 2026-10-29T20:36:21Z |
| Current plan / landing state | Worktree delta from base lists only `plans/round-50-attempt2-claims.md` modified; no SCORECARD or `corpus/knowledge` delta was present. The plan edit corrects the entry stem to the frozen counter stem and still calls for the 140/140 head. | `git diff --name-status f890bbead20ca2c549487167f56876ae47f1e1a4 -- SCORECARD.md plans/round-50-attempt2-claims.md corpus/knowledge`; exit 0; SHA-256 `e906eae53935123eb4e77b2d2a37839308568bb517ded50866f474b31097dff8`; 2026-10-29T20:36:53Z |

## Quoted derivation

`tools/round-50/c2-record.py:501-509`:

> `rows = [l for l in sec if re.match(r'^ {0,3}\|\s*coverage\s*\|', l)]`  
> `fr = re.findall(r'(\d+)/(\d+) knowledge files mapped', rows[0])`  
> `files = [p for p in c.r.ls(c.rev, 'corpus/knowledge') if p.endswith('.md')]`  
> `elif fr[0] != (str(len(files)), str(len(files))):`

B1 then independently checks that each file stem is mapped in the README coverage map (`:510-516`). B2’s separate row selection is `rows = [l for l in sec if re.match(r'^ {0,3}\|\s*calibration\s*\|', l)]` (`:522-527`).
The B1 off-by-one battery mutant also selects the first matching phrase after `| coverage` (`:1095-1101`), so it will continue exercising the new head; it does not validate trailing historical claims.

## Smallest safe correction and impact

Keep `140/140 knowledge files mapped at the round-50 attempt-2 landing` as the first matching phrase. Replace the old 139/139 current-sounding clause, or qualify it as the **attempt-1** landing and scope “round 50 added no knowledge entry” to attempt 1; retain 138/138, 133/133, and older counts only as clearly historical. Do not change B1 or its frozen predicate.

Impacted axes: **coverage** (the asserted count) and **calibration/audit integrity** (B1 accepts the first count but does not reject contradictory later prose). B2 and its calibration-row checks are unaffected. No REA run or data run was performed. Receipt details are also saved in `CritB1Text/receipts.md`.
