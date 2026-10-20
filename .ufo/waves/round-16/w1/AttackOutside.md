# AttackOutside — author-side review is not outside verification

**Axes:** calibration (verification identity/provenance); depth (attribution of technical evidence, not selector correctness). Advisory source-reading review only.

## Concrete counterexample

Counting `KaidokuR16.ReviewCanonical` as a named independent verifier would be false even if its review were technically correct. It is a spawned reviewer in the same author-side wave as `KaidokuR16.SelectorModel`, not a separately dispatched non-author:

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/wave1-dispatch.json:676-682,905-907`: both assignments belong to the same `taskCall`; the common context at line 677 expressly says “seats advise, not outside reviewers,” and ReviewCanonical's target says “no [x] authority.”
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/swarm-registry.json:8-16,458-466`: distinct agent IDs and the `reviewer` role establish seat identity, not independence. This critic is likewise an author-side spawn at lines 538-546.
- Canonical shokunin `LEARNING.md:42-46` requires a non-author sample of at least one admit and one reject, with agree/disagree reasons, and explicitly states that a subagent the lane dispatched is still the lane. `PROTOCOL.md:63-68` applies the same distinction to promotion marks.

**Exact missing evidence:** these inspected W1 dispatch/registry records do not supply a separately dispatched non-author's current-round admit/reject judgments and reasons against the delivered revision. A different seat name, role, source reconstruction, or agreement does not supply that record. This is a bounded evidence gap in this packet, not a claim that no outside review can exist elsewhere.

## Calibration limits

No actual false independence claim was found in the inspected claims or current checklist. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/claims.json:10-14` claims closure of four **previously outside-routed obligations**, not that W1 seats constitute a new outside spot-check. Those are different facts. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SHONEN.md:5-12` retains `[~]` throughout and explicitly distinguishes historical execution from current outside verification at line 10.

The precedent is already explicit: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-15-verifier-spotcheck.md:179` excludes author-seat agreement from outside evidence; lines 181-188 route the four corrections, and line 192 leaves complete independent checklist verification outside that bounded closure. Completing those corrections does not change reviewer identity or independently establish every checklist box.

## Smallest safe correction

Keep all W1 seats, including this report, labelled **author-side advisory**. Do not use their agreement as current independent discernment, promotion authority, or evidence that no further outside check is needed. Preserve `[~]` marks. If outside verification is claimed at closure, attach the actual separately dispatched non-author record: verifier identity/provenance, delivered revision, sampled admit and reject, and reasons recorded in the round lesson. Otherwise state that this evidence is not yet established.

This is a fixable attribution/evidence defect if the conflation is proposed, not a demonstrated technical regression or an unavoidable axis tradeoff. Source/model correctness of C1 and completion of C2 still require their own evidence; this review neither admits nor rejects either claim.

**Limits:** no builds, tests, linters, formatters, smoke checks, target/source execution, runtime invocation, installs, or updates. No artifact other than this report was written.
