## Record corrections — round 47

Append-only repair of the self-assessment atoms `tools/round-47/record.py` re-derives. The
original sentences stay where they were written; each `- corrects` line below supersedes the
atom it names and is itself re-derived by the counter at the measured revision. Only `seats`,
`window`, `path` and `rev` are parseable correction classes (`CORR` at
`tools/round-47/record.py:50`); `axes` is not, so the two `## Owned axes` heads are repaired in
place and recorded as a note below rather than as a `corrects` line.

- corrects seats round-45: 2 waves, 76 seats total — the superseded original is "Wave 1: 40 seats; wave 2: 32 seats (counts from `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`)". The two files it cites report `counts.spawn 40` and `counts.spawn 36` (`.ufo/waves/round-45/w1-dispatch.json`, `.ufo/waves/round-45/w2-dispatch.json`), and `r45-w2-results.json` itself records `seats 36`, so the 32 understates the dispatched wave by four and matches no committed count.
- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md — the superseded original is "`git log --name-status 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above". It carries two defects: `<tip>` is a placeholder no command resolves, and its literal base `0425224` does **not** give an empty window — `git log --name-status --format= 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md` lists `332f4884` (`M tools/round-46/attest.py`, `M tools/round-46/gate.py`, the F5 amendment). The frozen paths are unchanged only from the measured freeze `332f4884` to the measured revision `58eb04b6`, which is the window stated here and the one the counter reproduces as empty.

**`## Owned axes` heads, updated in place (deliberately not a `corrects` line).** Both rows are
current-state rows, so each head is rewritten to today's observable and the superseded value stays
in that row's history sentence. A `- corrects axes …` bullet cannot carry this repair: `CORR` does
not admit `axes`, so such a bullet is dropped before re-derivation and a false one still scores
green (measured: replacing both with `999/999`, and once with a nonexistent key, leaves the counter
at exit 0, `corrections 2`, `corrections_bad []`).

- coverage: the head read `133/133` after the round-41 landing; it now reads `138/138` —
  `git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` → 138, command A
  `mapped 138`, `missing []`, `dangling []`.
- depth: the head read `20/20` at `e1c83313`; it now reads `24/24` — command A at the round-47
  landing, `rule_blocks 24`, `citation_resolved_rules 24`. The head and block 24 must land in the
  same commit: at a revision where the craft section still has 23 blocks the `24/24` head is a
  mismatch (measured, exit 1, `mismatches 1`).
