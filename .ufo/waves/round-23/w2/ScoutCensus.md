# Round 23 SOURCES census — ScoutCensus

## Findings

- **[Observed]** Read the committed `corpus/SOURCES.md` bytes from candidate `2838351450ff1ee4baa620c962a1153450d53311` and baseline `aa1450b82f9ede35aada63efe8a34e01c6e02f72` using `git show <rev>:corpus/SOURCES.md`. Both reads succeeded (exit 0). Candidate blob SHA-256: `736857e1fb46cb81ee8bc29b79e595567a400994a83c330f0ccc47f394eb3525`; baseline blob SHA-256: `5ae5e7ed539d092d801d1c521cb3a0cfa6d89ff82e38b8d86c0c8d5b4f777ebd`.
- **[Observed]** Independently selected registry rows matching `^\| S[0-9]+ \|`, parsed pipe-delimited cells, and required 13 cells per row. The tier and status fields are columns 4 and 8 of the trimmed split-cell list (1-based after the leading empty cell). Candidate contains 61 unique rows, IDs `S001`–`S061`.
- **[Observed]** Baseline has 57 rows; its 57 raw row lines exactly equal the first 57 candidate row lines in order. Candidate therefore has the unchanged old-57 prefix plus four appended rows, `S058`–`S061`, at candidate blob lines 64–67. Each appended row is tier A / status `mined`.
- **[Observed] Candidate tier histogram:** A=55, B=5, C=1.
- **[Observed] Candidate status histogram:** `mined`=59, `rejected`=2.
- **[Observed] Candidate tier/status histogram:** A/mined=54, A/rejected=1, B/mined=5, C/rejected=1.

## Boundary and remaining unknowns

This is a structural census of the two pinned registry blobs only. It does not validate the cited sources, establish evidence eligibility/admission, or characterize a moving worktree. I did not run the shared source-census command, any gate, or tests. No other census remains unresolved within the requested row/count scope.

## Produced files and hashes

- `.ufo/waves/round-23/w2/ScoutCensus.md` — final file SHA-256 is provided in the delivery message, avoiding an embedded self-referential checksum.

## Installs

None.
