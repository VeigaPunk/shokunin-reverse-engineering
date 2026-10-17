## CLAIM
K1's Tameshi citations (`tameshi-shokunin/corpus/knowledge/verification-patterns-fleet.md:35,73,102` and `tameshi-shokunin/corpus/README.md:9`) resolve at the sibling checkout to exactly the stated content — the superseded universal evidence-ID formula `f(content, path, params)` and the unresolved r9-02/U4 marker.

## METHOD
Read-only reads and `sed -n '35p;73p;102p'` / `grep -n 'f(content'` against `/home/vgpnk/Projects/shokunin/tameshi-shokunin/`; no sibling writes, no probes, no network. Checked the note's full append structure (`grep -n '^## '`) and both errata blocks for any later correction; spot-checked the kaidoku side of the "superseded" characterization. Only this file written.

## FINDINGS
- `:35` — "identity claim strength = the id's full domain `f(content, path, params)` … one r9-02 observation (renamed byte-copy minting the same id) is flagged unresolved, U4." Exact match.
- `:73` — "Evidence-id identity domain `f(content, path, params)` (corpus/QUALITY.md:24)" inside the kaidoku lane-specific bullet. Exact match.
- `:102` — U4 "unresolved this lane". Exact match.
- `README.md:9` — coverage-map row for this note repeats `f(content,path,params)` under kaidoku's lane-specific encoding. Exact match.
- No supersession: later blocks (`:109` TAMESHI-R2-4 extension, `:200` Errata round 2, `:235` Errata round 4) correct nothing at `:35/:73/:102` and never discharge U4 (round-2 V-R2-3 leaves U1/U2 open; U4 unmentioned). `grep -n 'f(content'` over tameshi corpus returns only these three corpus hits.
- Staleness direction corroborated on the kaidoku side: `corpus/QUALITY.md:24` = row 14; `:25` = row 15 "never a universal formula … r9-02 disproved the #14 universal"; `SCORECARD.md:350` "criterion 15 added superseding 14"; `:355` the remaining literal is "retained by design as the superseded row". K1's `SCORECARD.md:347-357` and `QUALITY.md:24-25` refs likewise resolve.
- State pin: both tameshi files tracked, worktree-clean (`git status --porcelain` empty for them); note last committed `b58b26f` (2026-10-14); sha256 `bbf04a5e959b68b412ac0c5f077987bf2e8c5628cb286c508b903c8a9c208c33`; `wc -l` 306 (final line unterminated; reader shows 307). No session-transcript or log hit alters the corpus findings.

## THREATS
Pointer verification ≠ adjudication: I did not re-derive whether kaidoku's #15 is itself correct, nor quantify harm from Tameshi's stale derivative — only that K1's characterization matches the bytes. Citations resolved at one checkout state; siblings may move later. Grep is text-level, so paraphrases elsewhere are not excluded (tameshi `.ufo/interactive-sessions/` transcripts also match, correctly ignored).

## VERDICT
CLEAN: K1's Tameshi citations (`:35/:73/:102`, `README.md:9`) resolve verbatim against tracked, clean files at the sibling checkout, with no later erratum superseding them; the supersession of `f(content, path, params)` is confirmed on kaidoku's own record (QUALITY #15, SCORECARD:350).
