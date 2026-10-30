# ConnDocs — bounded documentation connector proposal

Axes: coverage, depth, calibration. Artifact: `ConnDocs/matrix.md` (72 constant rows across eight named draft slots).

## Evidence and findings
Only `ScribeProvince/province-r52-core-section.md` was available in the named directories at the snapshot. Five directories were absent; ScribeSources was empty; ScribeLesson had only an empty receipts directory. Missing drafts are explicitly unavailable, not matching. No cross-draft consistency pass is claimed.

1. Province line 34 correctly names `.ufo/waves/round-52/l1/scores/c1-after.json`; line 134 incorrectly names `corpus/evidence/round-52/l1/scores/c1-after.json`. Claims line 174 fixes the former. Carrier receipts are separately `corpus/evidence/round-52/c1/<id>/`.
2. Province lines 5–6 require exit-0 evidence for every fill, contradicting its honest-stop branch's requirement to quote a real nonzero exit and failure clauses (108–110). Preserve red evidence as red.
3. Province lines 79–82 reject source-grounding the FIFO/socket no-creation generalization from the root-process gate; claims lines 43 and 56–57 still generalize it. This is an explicit source/claim contradiction, not a cosmetic difference. Measured width remains 28/28 char-device rows and no measured FIFO/socket/block rows.

## One proposed move
Use the matrix as one freeze-time documentation constant ledger under L1 ownership. Normalize only current-round landing pointers and unresolved data markers, preserving historical references and actual failure semantics. Proposed marker: `[PLACEHOLDER: <field>; source=<receipt-path>#<field>]`. Available Province instead uses `<PLACEHOLDER — L1: …>`; neither RECEIPT-PLACEHOLDER nor bare [PLACEHOLDER] was observed elsewhere because the other drafts were absent. Do not invent an assimilation S-ID. Resolve source/claim differences through an explicit claim amendment decision, never silent replacement.

Expected effect: better coverage binding fidelity and calibration without touching depth routing, runtime behavior, registry or vendor bytes. Risks: indiscriminate replacement damages history; late drafts remain unaudited; instructional copies can duplicate headings. Matrix includes bounded L1 verification steps. No admission, integration, shipping or judgment performed.

Verification: not run. Read-only inspection via read/glob; no REA, shell commands, downloads, fixtures, installations, scratch use or external runtime. No executable receipt is claimed. All writes stayed in the assigned report and seat directory.
