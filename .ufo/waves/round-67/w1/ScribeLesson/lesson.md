# Round 67 — the class rule and the two survivors

Base `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`; the operative freeze is the commit that first
adds `.ufo/waves/round-67/claims.json`; the carry-in is the appended entry `## 2026-11-03 — round
67, KaidokuR67 — carry-in` (`LOG.md:4083`). The carry-in entry records its own ordering — committed
before the instruments and before the declaration — which the round's A0 atom measures. Two claims on
distinct axes: **R67-C1** (coverage, frontier → core) re-freezes the
round-50 LE-AVM measurement under a gap rule that classes char-device entries as not-publishable
rather than per-row required, and **R67-C2** (depth, counter repair) adds the selftest battery that
binds the two round-66 mutation survivors. Neither verdict is taken here: the after-arms belong to
the L1's data run and the closure belongs to the non-author judge. This lesson records the grounds,
the before-arms and the two criteria the round mines.

## Gate

Access date for the new source: **2026-11-03**. Fetch, locator and quote evidence:
`.ufo/waves/round-67/w1/ScribeLesson/gate-fetch.json`. The row is drafted as **S268** (the
registry's highest id is S267 and S268 is free; the L1 assigns the final id at the landing).

| candidate | locator / evidence | measured value | decision | flip condition |
|---|---|---|---|---|
| (a) Linux kernel SquashFS documentation, §3.2 Inodes — the on-disk device inode class | https://docs.kernel.org/filesystems/squashfs.html, opened 2026-11-03: HTTP 200, 26,045 bytes, sha256 `10767bbf…d33685`, `Last-Modified: Sun, 01 Nov 2026 22:46:23 GMT`; heading `3.2 Inodes` (`<section id="inodes">` raw line 401); Gate quote raw lines 412-414, 22 words: "there are different inodes for each file type (regular file, directory, device, etc.), the inode contents and length varying with the type" | the page states that the file type selects a distinct inode whose contents and length vary, so a device entry is its own on-disk class and not a regular file with a mode bit — the class ground the round-50 rule lacked. It states **no** extraction privilege (that is S250) and **no** carrier fact (the envelopes carry those) | **admit** as S268; scope: the SquashFS on-disk inode class per file type; not extractor privilege, not a marker or layout definition, not a carrier claim | — |
| (b) the same page's §1 inode-size sentence as a second row | same locator; raw lines 264-266: "compressed inode is on average 8 bytes in length (the exact length varies on file type, i.e. regular file, directory, symbolic link, and block/char device inodes have different sizes)" | a duplicate locator and a scope S268 already carries; one row carries one located quote, and the class claim needs §3.2's type/contents sentence, not the size parenthetical | **reject as a second row**: duplicate locator and scope | admissible if the row's subject becomes the inode *size* claim (§1) instead of the class claim (§3.2) — then it is a different row with a different anchor |
| (c) the source text `Documentation/filesystems/squashfs.rst` on `torvalds/linux.git` plain | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/squashfs.rst, opened 2026-11-03: HTTP 200, 14,201 bytes, sha256 `e709573a…3ba5f9`; the same three sentences at raw lines 184-186 | the same text and scope as (a) under a locator that names no revision (the repository's default branch), so the bytes are not pinned by the location at all | **reject**: same subject and scope as S268 and no revision identity in the locator; the rendered page is pinned by its fetch sha256 and `Last-Modified`, the plain URL by nothing | flip: adopt the `.rst` at a tagged tree (e.g. `v6.18`) if the entry needs a release-pinned text identity; the locator then carries a revision |
| (d) `l1/pre/control-dryrun.json` `per_carrier.g7581.gaps_note_round50` as the ground that no extractor record can exist | the receipt names 8 of that carrier's `dev/pts/*` char devices as required-with-no-disposition; the round-67 note on the same carrier reports 637 gaps (1 structural), 3 removals, 0 silent over 1,001 non-regular entries | a receipt measures the rule's effect on one carrier; it cannot ground why a class is not publishable | **reject as a source**: a receipt demonstrates a red arm, never a rule's ground; the ground is S268 (the inode class) with S250 (the `mknod` privilege gate) | never — a receipt does not become a SOURCES row |

Re-opened round-50 rows — all four, because the re-freeze re-uses their subjects, not because a
recheck fell due (S243 and S245 carry a 180-day recheck, due 2027-04; S244 and S249 a 90-day
one, due 2027-01): **S243** (Freetz patch 101) HTTP 200,
1,153 bytes, sha256 `e28b3341…84c707`, byte-identical to the registered pin; **S244** (AVM download
index) root listing HTTP 200 and the 6490-cable `fritz.os/` row reads
`FRITZ.Box_6490_Cable-07.57.image 04-Sep-2023 17:07 39741440`, matching the registered size and
date; **S245** (unblob 26.6.4 LE handler) HTTP 200, 19,842 bytes, sha256 `2d7b901b…599287`;
**S249** (AVM licence `info_en.txt`) HTTP 200, 67,591 bytes, sha256 `6c601b34…070a7`. None needs a
new row: each scope is exactly the subject this round re-used — a symbol definition and byte order
(S243), the publisher's own listing (S244), the little-endian handler's `-le` argv (S245), the
one-backup-copy licence (S249) — and none of them states the on-disk device inode class, which is
why (a) is a new row rather than an extension of a standing one.

Assimilation: none this round, measured rather than asserted — `ls merge/kaidoku/` and
`ls considerthese` both exit 2 (no such file or directory) at the lane's base tree, so there is no
staged theme to screen against a SquashFS class rule. No row was bulk-appended.

Outside spot-check: the round's non-author closure supplies it; this lesson does not self-certify
admit/reject agreement.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M67-1 | scope / over-generalisation from one carrier family (survivor, round 50) | `tools/round-50/gap-rule.json` (`required.char-device: true`, `removed.silent.char-device: ["247:0"]`); `corpus/lessons/round-50.md` M50-7 (`captured-by none`); `.ufo/waves/round-67/l1/pre/control-dryrun.json` — g7581 and g7582 fail under the round-50 rule with `required entry with no disposition … on ['dev/pts/0' … 'dev/pts/7']` and pass under the round-67 rule | `none` until this round: M50-7 was filed with no criterion, and QUALITY #94 states the derivation requirement without the contrast the class rule needs — the criterion drafted below as **#107** is the first to bind it | the class rule `tools/round-67/gap-rule-v2.json` (`required.char-device false` plus a `class_disposition` block naming the class, the reason and the two checks that still account for it) with the count kept: `gaps_ok_round50 2` of 4 against `gaps_ok_round67 4` of 4 in one receipt, and three red fixtures keeping the waiver scoped (`round67_rule_still_fails`, `publication_check_names_it`, `junk_rule_would_pass`) |
| M67-2 | accounting / witness (this round's own, pre-freeze) | `.ufo/waves/round-67/l1/pre/control-dryrun.json`: c6430 and c6490 report `1 silent` under the round-50 rule and `0 silent` under the round-67 rule, because `tools/round-67/gap-rule-v2.json` drops `removed.silent.char-device: ["247:0"]`; the engine counts a silent admission only from `removed.silent` (`tools/round-50/c1-counter.py:1458`, `disposition_check`) | `none` — no criterion requires a dropped per-row admission to be re-expressed at class level, and the `class_disposition` block names the re-derived oracle table and the `nonregular_unpublished` check, neither of which records a *missing* record | disclosed, not repaired: the round-67 rule stops claiming the Cable carriers' one char-device removal as a silent admission. The predicate reads `carriers_matched`/`met_target`, not the silent count, so no verdict moves; if the class rule is to keep that count it must be re-expressed as a class-level count in the next rule revision |
| M67-3 | receipt / witness (round 66, closed this round) | the round-66 non-author closure's routed defect 2: `.ufo/waves/round-66/w1/ExecClosure/verify.json` and `.ufo/waves/round-66/l1/scores/c1-after-verify-at-record.json` name no measured revision | the round-66 spot-check (routed item, no QUALITY criterion) | every round-67 receipt carries `rev`: `l1/pre/control-dryrun.json` `rev a7a4ce69…`, `l1/pre/control-dryrun-c2.json` `rev a7a4ce69…`, `l1/pre/score-dryrun-at-base.json` `rev a7a4ce69…`. The field is present in the three pre-freeze receipts; binding it into the verdict is the counter's clause, not this receipt's |

## Outcome

**R67-C1 — before-arm committed, after-arm pending.** The do-nothing control at the base
(`.ufo/waves/round-67/l1/pre/control-dryrun.json`, `rev a7a4ce69…`, exit 0, `control_ok true`) scores
the same four frozen round-50 envelopes under both rules: `gaps_ok_round50 2` of 4 (g7581 and g7582
each fail on eight named `dev/pts/*` char devices) and `gaps_ok_round67 4` of 4, with the three red
fixtures as designed (`round67_rule_still_fails true` — one removed symlink gap still fails;
`publication_check_names_it true` — `firmware.bin_extract/dev/led` is named when a char-device path
is published as a regular file; `junk_rule_would_pass true` — a junk rule that also waives symlinks
would pass, so the waiver must stay scoped). The engine is pinned by sha256 `9820811b…` and its own
selftest is 169 cases green (`.ufo/waves/round-67/l1/pre/selftest-r50.txt`); the round-67 rule is
sha256 `e66ba022…`. What this receipt does **not** establish: that the four carriers, re-measured by
the pinned engine under the round-67 rule and the round-67 documentation bindings at the recorded
revision, report `carriers_matched 4` with `met_target true` — that is the `--score` after-arm, and
the four carrier data runs (`tools/round-67/c1-run.sh`) are the L1's, not this wave's. Two
timeline facts from the lane while this draft was being written, recorded because they move the
receipts and not the claim: the C1 counter was corrected **after** the freeze (`1e7fe7b7` — the
patched gap-rule name must be lane-relative, since the engine reads its rule through
`git show <rev>:<path>` and the absolute name made `measure()` exit 2), the correction is disclosed
in `claims.json` `instrument_supersessions` with the new pin `55decb51…`, and the before record was
re-taken under it with the same numbers (`gaps_ok_round50 2`, `gaps_ok_round67 4`, `control_ok true`,
`rev a7a4ce69…`); and the L1's data run has committed four `run.json` receipts (`a4c1d0fc`) with the
four `after.json` untracked in the working tree and `l1/scores/c1-data-stage.json` the only score
receipt. This seat neither wrote nor read the carrier evidence.

**R67-C2 — before-arm and a pre-freeze score dry run, after-arm pending.** The control
(`.ufo/waves/round-67/l1/pre/control-dryrun-c2.json`, `rev a7a4ce69…`, exit 0, `control_ok true`)
scores the two round-66 mutants with the round-66 selftests alone: `killed_before 0`,
`survived_before 2`, both r66 selftests `SELFTEST CLEAN` at 30 and 26 cases, mutant pins
`5e84208a…` and `2b98a7f7…`. The battery's own selftest is 9 cases green
(`.ufo/waves/round-67/l1/pre/selftest-c2.json`), including `arm-false-bound` (the mutated `arm()`
called with a false condition, wanted `false`) and `equiv-doctored-bound` / `equiv-doctored-diffs`
(the doctored recipe-A block, wanted `false` and a non-empty diff list; the observed diffs are
`coverage_score` and `mapped`). A pre-freeze dry run of the score mode at the base
(`.ufo/waves/round-67/l1/pre/score-dryrun-at-base.json`, `verified true`) reads `survived_before 2`,
`killed_before 0`, `killed_after 2`, with the killed cases `['arm-false-bound']` and
`['equiv-doctored-bound','equiv-doctored-diffs']`. That is a dry run, not the after-arm: the
record's `--score`, and the two pristine counters' green at the record, are re-checked by the L1; no
C2 score receipt exists in `l1/scores/` at this reading (`c1-data-stage.json` is the only file there).

**Outside closure — pending.** The round's non-author closure has not run. This lesson certifies
neither verdict, and no seat in this wave may.

## QUALITY rows (drafted; the L1 lands them)

- **Row 107 (a rule generalised from one carrier family names the family it came from and the class it cannot see).** A gap, removal or disposition rule that makes an entry kind a per-row requirement is admitted only when the rule file names the carrier family it was derived from and the class that family cannot exercise; where a class cannot be exercised, the rule disposes of the class — with its reason and with the checks that still account for it — and a control measures both dispositions over the same frozen envelopes, so the class is accounted for by contrast rather than by assertion. A rule that generalised from one family and names neither the family nor the invisible class is a claim-falsifying defect the moment another class reaches the data. Evidence: `corpus/lessons/round-50.md` M50-7 (the `char-device` requirement derived from the Cable class, where exactly one device `247:0` exists, falsified by the FRITZ!Box class with 13 devices each; `tools/round-50/gap-rule.json` `required.char-device: true`), and the repair with its contrast in one receipt — `tools/round-67/gap-rule-v2.json` and `.ufo/waves/round-67/l1/pre/control-dryrun.json` (`gaps_ok_round50 2` vs `gaps_ok_round67 4`, three red fixtures). Sharpens 94.
- **Row 108 (a mutation survivor is closed only by a case that exercises the mutated function on a false input).** A survivor — a mutant that no case kills — is closed only by a selftest case that calls the mutated function with an input on which the correct implementation must return false (or a non-empty difference), so the mutant and the pristine counter produce different outcomes on that case. A case that never calls the function, or calls it only where the correct answer is true, leaves the survivor alive whatever the case count. Evidence: `.ufo/waves/round-66/w1/MutClosure/mutants.md` M5 (`arm()` returns `passed: true`; `SELFTEST CLEAN cases=30` and 5 of 5 arms, `SURVIVED`) and `.ufo/waves/round-66/w1/MutCoverage/mutants/M2/` (`recipe_a_equivalence()` returns equivalent without running the block; survived 26 green cases); the round-67 battery kills both with `arm-false-bound` and `equiv-doctored-bound` / `equiv-doctored-diffs` (`.ufo/waves/round-67/l1/pre/control-dryrun-c2.json` 0 of 2 killed; `.ufo/waves/round-67/l1/pre/score-dryrun-at-base.json` 2 of 2). Sharpens 78.
