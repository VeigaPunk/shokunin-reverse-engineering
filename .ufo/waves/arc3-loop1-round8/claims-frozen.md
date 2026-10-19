# arc3-loop1-round8 — frozen claims, 2026-10-19

Wave: 24 seats (within the scheduled 16–32 band), scheduled zai provider —
**substituted**: the zai lane is usage-exhausted (operator directive,
end-of-session), so this round runs on `openai-codex/gpt-6-luna-max`.
Roster frozen PRE-DISPATCH; the items array carries exactly the 24 names below.
Roster enumerated mechanically: 6 + 6 + 6 + 6 = 24.

Axis set: **operability (fleet; close the `ptr_check` blind spot — the R7
adjudicated-partial, done right this time)**, **freshness (fleet; re-anchor
the drifting pin receipt in the same commit)**, **coverage (owned; a corpus
Unknown)**. Claims are causally separable: the census gate code + the
receipt, the PROVINCE pointer, corpus/knowledge.

## C1 — operability (fleet): land the `ptr_check` extension on a real anchor

The R7 adjudication (`claims/c1/C1-ADJUDICATION.md` in the r7 wave) named the
clean fix: the live `~/.kimi-code/config.toml` pin line has drifted to
**`:4126`** (re-measured this round — `:3546` is already stale again), so the
receipt anchor must be re-derived at the landing commit, not copied from a
prior round. Land the `ptr_check` extension so a `path:line` pointer in a
clause that also carries a pin/version is evaluated — using the R7-wave
candidate patches (EX-1's digest-checked form or RV-2's anchor form, both in
`arc3-loop1-round7/claims/c1/`) as the mechanism, but anchored to a
**freshly-measured live pointer**: re-derive the pin's current line at
landing, assert it against the live config (the `ptr_check` "ok" class), and
keep the receipt-stamped historical chain as adjudicated historical. The
instrument must: (a) read PASS on the current tree with the LIVE `:4126`
pointer evaluated current-ok; (b) catch a re-keyed dead pointer on a scratch
tree; (c) keep G21 + all existing counters intact. Produce the patch TEXT +
the seeded-fault measurement; never edit the gate directly in a seat.

Falsifiable before → after: `ptr_check` unreachable on pin-carrying clauses
at HEAD; after, the live `:4126` pointer evaluates current-ok on the clean
tree and a dead-pointer re-key fails — all measured on scratch.

## C2 — freshness (fleet): re-anchor the PROVINCE pin pointer (same commit)

`PROVINCE.md:18` reads `:3546` while the live pin is `:4126` — stale again.
The pointer must be re-anchored to the live line **in the same commit as C1's
instrument extension** (the receipt anchor must exist before the instrument
can grade it). Land the `:3546` → `:4126` pointer update (a same-line edit
inside the DATED row 15-26 — measured line-neutral) + record the receipt in
`.ufo/receipts/` or the existing receipts path with the live line's content
hash, so the instrument's receipt anchor is real this time.

Falsifiable before → after: `PROVINCE.md:18` cites a dead line at HEAD
(`:3546` holds a Copilot block, not the pin); after, it cites `:4126`
(measured `rea-agents@6.7.0` present), and the pointer-table / receipt records
the current line's content.

## C3 — coverage (owned): close one named corpus Unknown

Pick ONE provable Unknown not yet closed: candidates include (a) a solc
version other than 0.8.37 under viaIR (r6 Unknown), (b) the Vyper `-O
codesize`/`--no-optimize` forms the r7 wave measured but did not land as its
own entry (several seats produced verified drafts — reconcile and land the
best ONE as a corpus entry), or (c) another cited Unknown. The chosen
Unknown lands as a corpus knowledge entry + map token; command A re-measures
86 → 87.

Falsifiable before → after: command A at the work commit — knowledge_files
86 → 87, mapped 87, missing [], dangling []; the entry's evidence cited
inside it.

## Seat roster (24, one AgentSwarm items array)

c1 chain (the ptr_check extension, 6): PL-1..PL-2, EX-1..EX-2, RV-1..RV-2
c2 chain (the PROVINCE re-anchor + receipt, 6): EX-3..EX-6, CR-1..CR-2
c3 chain (the corpus Unknown, 6): EX-7..EX-9, SC-1..SC-2, RV-3
verdicts/convergence (6): VZ-1..VZ-2, CN-1..CN-2, CR-3..CR-4
