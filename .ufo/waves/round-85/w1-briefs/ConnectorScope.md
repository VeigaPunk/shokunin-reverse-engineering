Seat: ConnectorScope (connector, read-only). Sibling-overlap scan for this round's two claims.

# Do
1. Search the other lanes' repos (read-only) for existing claim-container gates, predicate-binding checks, or mutant-table closure counters that duplicate C1 or C2: `grep -rl --include=*.py -E 'CLAIM_NO_COUNTER_PATH|mutation-closure|declared_case|predicate-bind|PB_NO_PREDICATE' /home/vgpnk/Projects/shokunin --exclude-dir=.git --exclude-dir=.jj` restricted to `*-shokunin/tools`, plus `/home/vgpnk/Projects/shokunin/scripts`. Report each hit with path:line and whether it is a sibling-owned duplicate (name the owning lane from the directory name).
2. Check `PROVINCE.md` of this lane (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md`) for the Adjacent section and say whether the claim surfaces (claim-container gates; mutation-testing of the lane's own instruments) are in the lane's core, frontier, or adjacent scope. Quote the exact line.
3. Check whether any sibling lane's round-84/85 wave writes into `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/` (only read; grep the `.ufo/waves` dirs of other lanes for `kaidoku-shokunin/tools`). Report any hit.
4. Give the L1 a one-line recommendation for each claim: proceed, or route to owner.

# Deliverables (wave dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/w1/ConnectorScope/)
`report.md` (≤ 40 lines: hits table, PROVINCE quotes, recommendations); `DONE` marker last.
