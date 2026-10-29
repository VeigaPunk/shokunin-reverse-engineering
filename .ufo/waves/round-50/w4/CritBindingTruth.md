# FALSIFIED — two binding statements are literally false

**Verdict:** The round’s C1 outcome is otherwise documented as an honest 2/4 miss, with no Core promotion. But the knowledge-entry status and PROVINCE evidence row each say **“documentation bindings true”**. The landed receipt contradicts that: `bindings_false` is exactly `province_core_section`, `province_core_row`; both are `false`. This is a fixable wording defect, not evidence that C1 passed or that a Core promotion occurred. No reviewed text hides that extraction matched all four carriers.

Axes: **coverage** — two inaccurate binding summaries; **depth** — checked every named outcome surface against the receipt; **calibration** — separated this narrow contradiction from the correctly reported miss and no-promotion decision.

## Findings

| Surface | Exact landed quote | Verdict / basis |
|---|---|---|
| Knowledge entry, status (`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md:3`) | “every documentation binding true” | **FAIL — overstates.** Receipt says `province_core_section: false`, `province_core_row: false`, and lists both in `bindings_false` (receipt lines 45–53). The adjacent “No Core promotion is claimed; LE AVM members (`hsqs`) stay Frontier” is **PASS**. Capture `ENTRY`, `RECEIPT`. |
| Knowledge entry, What moved (`…core.md:14`) | “the claim measured as a miss, so nothing moved to Core”; “The publication half of that sentence held on all four carriers; the frozen accounting rule decided the verdict.” | **PASS.** Clearly separates extraction success from the frozen accounting miss; no promoted/verified claim. Capture `ENTRY`. |
| Knowledge entry, results / measured outcome (`…core.md:46,52`) | “the extraction side of the claim holds everywhere”; “matched **2 of 4** carriers”; `gaps_ok` false on g7581/g7582 and true on the two Cable carriers | **PASS.** Explicitly reports 4/4 extraction and 2/4 overall counter outcome. Capture `ENTRY`. |
| PROVINCE round-50 narrative (`PROVINCE.md:442`) | “matched **2 of 4** carriers (exit 1)”; “published every frozen-oracle regular file on all four carriers”; “the miss is the frozen gap-accounting rule” | **PASS.** Accurate extraction and miss. Capture `PROVINCE`. |
| PROVINCE evidence row (`PROVINCE.md:446`) | “carriers_matched 2 of 4, `frozen_path_changed []`, documentation bindings true” | **FAIL — overstates the same two false Core-promotion bindings.** Section heading/body otherwise mark a measurement, not a Core promotion. Capture `PROVINCE`, `RECEIPT`. |
| PROVINCE frontier note (`PROVINCE.md:448`) | “stays Frontier after the measured attempt”; “2/4 under the frozen gap-accounting rule” | **PASS.** No promotion asserted. Capture `PROVINCE`. |
| README coverage-map row (`corpus/README.md:106`) | “measured, not promoted”; “REA published every oracle regular file on all four”; “matched only the two Cable carriers (2/4…)”; “stay Frontier” | **PASS.** No binding overclaim and no extraction understatement. Capture `README`. |
| README knowledge-index row (`corpus/README.md:228`) | “measured, not promoted (R50-C1 miss: the frozen gap rule’s char-device accounting)” | **PASS.** Capture `README`. |
| README frontier note (`corpus/README.md:300`) | “REA published every oracle regular file on all four” and “stay Frontier — R50-C1 measured 2 of 4” | **PASS.** Capture `README`. |
| SCORECARD attempt-2 row (`SCORECARD.md:3796`) | “**exit 1, `carriers_matched 2` of `target 4` — an honest miss**”; “published every frozen-oracle regular file on all four”; “No Core promotion”; receipt `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` | **PASS.** “Frontier → Core” is the claim’s target column, not an achieved result; result text explicitly rejects promotion. Cited receipt exists (path check exit 0) and is present at target revision. Capture `SCORECARD`, `RECEIPT`, `EXISTS`. |
| SCORECARD attempt-2 summary (`SCORECARD.md:3799-3801`) | “the entry records the miss — no promotion”; “expansion **unchanged**”; “no frontier ground entered Core”; “the entry’s extraction statements are receipt-backed per carrier” | **PASS.** Does not claim C1 verification. Capture `SCORECARD`. |
| LOG attempt-2 entry (`LOG.md:3480-3481`) | “every frozen-oracle regular file published on all four”; “matched 2 of 4”; “No Core promotion” | **PASS.** Capture `LOG`. |
| Lesson attempt-2 C1 section (`corpus/lessons/round-50.md:77`) | “every frozen-oracle regular file published on all four”; “**2 of 4, exit 1**”; “documentation bindings true except the two Core-promotion bindings (`province_core_section`, `province_core_row` — intentionally absent: nothing was promoted)” | **PASS.** This is the accurate wording the two faulty lines should match. Capture `LESSON`, `RECEIPT`. |
| Entry/title and README key containing `…-core` | The filename/key is `2026-10-28-r50-avm-le-squashfs-core`; entry title says “measured — not promoted” and the rows say “measured, not promoted.” | **No false promotion claim.** The `-core` stem is potentially confusing in isolation, but explicit status and measured outcome disambiguate it; the counter pins this stem. Capture `ENTRY`, `README`. |

**Understatement check:** none found. The entry, PROVINCE narrative, README map/frontier, SCORECARD, LOG, and lesson all say that REA published every frozen-oracle regular file on all four carriers (or give the per-carrier counts); they preserve the separate 2/4 gap-accounting miss.

**Smallest safe correction:** in only the entry status and PROVINCE row, replace blanket “documentation bindings true” with “all non-Core-promotion bindings are true; `province_core_section` and `province_core_row` are false because nothing was promoted.” No claim, counter, score, frontier status, or extraction result needs changing.

## Exact command evidence

Full paired worktree/pinned byte-hash captures, exit codes, timestamps and stdout SHA-256 values are in [`CritBindingTruth/captures.md`](CritBindingTruth/captures.md). For each file, both the current worktree `cat '<absolute path>' | sha256sum` stream and `git -C '<lane>' show 'c67b741e8f6bd8d64adbdb15e059d47fde004c77:<path>' | sha256sum` stream exited **0** and produced identical file-byte hashes. Those exact commands and values are listed per file in the capture receipt.

The cited SCORECARD receipt check was exactly `test -f '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/l1/scores/c1-after-attempt2.json' > '/fast/scratch/hyaku/kaidoku-r50/w4-CritBindingTruth/receipt-exists.stdout'`; exit **0**; stdout SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; UTC `2026-10-29T21:31:44Z`.

At inspection, `HEAD` was `db61a90752657588817e78327c78106d486291d1`, later than supplied `c67b741e`; all reviewed document and receipt byte hashes match the supplied revision. Receipt field values were inspected directly; C1 full predicate/REA rerun was **not run** (seat contract prohibits it). No tool installed or updated.