## CLAIM
RB1 final gate, item 1: certify Z1’s pointer text and Q1’s source gate against raw bytes, and deliver the final item-1 text. No round-9 `VB1.md` exists anywhere under `.ufo/` (`grep -rln VB1`), so byte-level verification ran in-seat.

## METHOD
HEAD `a280e07`. `sha256sum` worktree vs `git show HEAD:` — identical for both sources (`622e3661…` r4-16; `fb2cd812…` r12-01); `git diff --quiet HEAD --` exit 0. Command A (`SCORECARD.md:93-123`, `REV=a280e07`) → `knowledge_files 79, mapped 79, missing [], citation_resolved_rules 9, coverage 10.0, depth 10.0`. Read `r4-16:728,750-754,798,875,925`; `r12-01:97-104,110-120`. Static only.

## FINDINGS
- Bytes: `r4-16:751-752` names exactly two sites (`files[].path`; `chunks[].provider_id`); `r12-01:99-104` records four sites plus “7 values”; `:110-120` is the round-5 erratum; `:112-114` supersedes r12-01’s own loci only; `:115-118` attributes the numeral, `/tmp` receipts gone. All four Q1 PASS clauses reproduce.
- Placement defect (gate correction): Z1 (`Z1.md:8`) and Q1 (`Q1.md:8`) target “the r12-01 erratum block” (:728-797), but that block is now mid-file — r12-02 at :798, r14-01 at :875, EOF :925. Inserting there renumbers :798-925 and breaks wave anchors (e.g. `Y3.md:5` :875/:925). Convention plus `BB1.md:14` (EOF, prefix-preserving) → land as a new EOF block. Clauses unchanged (Z1’s path pointer absorbs both ranges).
- Command-A-neutral: no new file; SKILL’s 9 rules cite no r4-16 range.

Final item-1 text (append after `:925`; file 64,080 B, ends LF):

```text
## Errata (round 9 freshness, 2026-10-16, append-only)

- **L197 normalization cross-reference:** the two-site summary above
  (`:751-752`) is historical; see r12-01's round-12 audit and round-5
  freshness erratum
  (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:99-104`,
  `:110-120`). The corrected account is two variance classes across
  `files[].path`, `output_directory`, `chunks[].provider_id`, and
  `derivations[].provider_blob_id`; "7 values" is attributed, not
  re-derived because the `/tmp` receipts are gone (`:115-118`).
```

## THREATS
“7 values” is not re-derivable (receipts gone); the text attributes, never re-derives. No live re-run — prose byte-identity only. Without a VB1 seat, verification is not independent of Z1/Q1 authorship.

## VERDICT
FINDING: content verified clause-by-clause at raw bytes; placement corrected to a new EOF erratum block — land the text above verbatim after `:925`.
