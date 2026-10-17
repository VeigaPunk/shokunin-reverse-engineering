## CLAIM
Fidelity sweep of debt items 3 (PROVINCE module-identity request-byte pin) and 4 (README stale frontier + nit text): both debts real, current anchors exact, integration mechanics pinned.

## METHOD
Primary sources first at HEAD cfc84c2 (worktree clean; no probes): PROVINCE.md full read + pin/module/attest greps; corpus/README.md full; r9-02:146-181; SCORECARD.md:45,68-84,346-352,414; LOG.md:388-401,746-748; drift lineage via `git show {a3f2e1b,2abd30f,HEAD}:corpus/README.md`; command A rerun. Lane outputs (P0/V3/D3/V4/G4/F4/C2/R4/Y1/ZB3/DB3/VB4/DB4) read only after drafting.

## FINDINGS
Item 3 — real, open: PROVINCE.md carries no pin wording (only version :41 / retention :55 pins). Authority verbatim: "consumers must pin request bytes (or re-derive dossiers themselves), never just ids, when module identity matters" (r9-02:168-169). Constraints: (a) same-physical-line insert — tracked cites of PROVINCE lines ≥44 (SCORECARD:45,79; SHONEN:12; lessons:152; r14-02:44-153; r12-02:141,183,297; r4-16:849; asar-surface:87; LOG:369) break under any added line; (b) wording must keep the `analyze_function` qualifier and literal "when module identity matters" + "pin request bytes" (gates C4:25/X1:32; "pin the exact request bytes" fails literal matching). D3's "the evidence ID alone does not authenticate module attribution carried in `subject`" mirrors the source; V3/C7's extra "ID + subject sha256" negation exceeds it. PROVINCE:58 needs no second edit.
Item 4 — anchors exact: :131 = lessons row ending "verify-lane VERIFIED, 4 nits fixed"; :163 = "Runtime-obs extended…" bullet; SCORECARD:68-70's :128/:160 are round-1-era positions (+3 drift, verified). Both stale: :163's three families all held (r5-02 3/3 of 286; r9-02; r11-01 exit-0 pair; README:47,53,56); :131's count corrected by LOG:395-401 to 1 pre-land self-correction + 2 integration fixes + 1 accepted. D4's row replacement is otherwise byte-faithful; at :163 prefer in-place replacement over deletion (deletion shifts ≥:164 cites: lessons:37, wave P1:12); F4's :160/sasquatch reading mis-anchors the debt. Invariant: command A → mapped 72, missing [], dangling [], 9/9, 10.0/10.0; both sites outside the parsed Coverage map.

## THREATS
Textual only; no live re-runs. Insert byte (2885 vs 2960) and delete-vs-replace are parent calls; SCORECARD:68-72 self-stales once README lands.

## VERDICT
FINDING: land item 4 as a line-preserving :163 replacement (not deletion) and item 3 as a same-line :32 insert carrying `analyze_function` + literal "when module identity matters"/"pin request bytes"; F4's :160 anchor misreads the debt.
