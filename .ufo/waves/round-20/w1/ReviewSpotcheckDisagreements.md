# Round-20 spotcheck disagreement cross-check

**Axes:** calibration, coverage, depth.

**Finding — no sampled discernment disagreement remains without a QUALITY row.**

- **R16 → QUALITY #19:** Round-17’s discernment summary says both R16 outside disagreements became QUALITY #19 plus fixes (`corpus/lessons/round-17-verifier-spotcheck.md:131`). The row is at `corpus/QUALITY.md:29`; its rationale points to the R16 provenance spotcheck and R17 lesson.
- **R17 pin-map partial disagreement → QUALITY #21:** The sole partial disagreement in the R17 outside sample is the claim that each mid-run pin map was retained (`corpus/lessons/round-17-verifier-spotcheck.md:108`). Round 18 independently confirms the correction and explicitly says QUALITY #21 was added (`corpus/lessons/round-18-verifier-spotcheck.md:85`), summarizes that #21 is grounded in that partial disagreement (`:178, :187`), and the row is present at `corpus/QUALITY.md:31`.
- **R18 sample:** the outside decisions shown at `corpus/lessons/round-18-verifier-spotcheck.md:153-161` all say “agree”; the summary records 7/7 agreement and says no disagreement was left unlearned (`:187`).
- **R19 sample:** all five decisions at `corpus/lessons/round-19-verifier-spotcheck.md:156-160` say “agree”; the summary confirms all five (`:175-176`). Separately, the R18 dead-seat discrepancy (`round-18-verifier-spotcheck.md:146,197`) is a routed defect, not a sampled discernment disagreement; R19 says it became QUALITY #22 (`round-19-verifier-spotcheck.md:175-176`), whose row is `corpus/QUALITY.md:32`.

**Verification / commands:** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --exit-code refs/heads/main -- corpus/QUALITY.md` — exit 0 (QUALITY.md has no working-tree diff against `refs/heads/main`). Source conclusions above are from the cited lesson and QUALITY text. No other shell commands were run. LSP checks were unavailable: no `lsp` device is exposed in the mounted tool inventory; this is a document cross-reference, not a caller/definition review.
