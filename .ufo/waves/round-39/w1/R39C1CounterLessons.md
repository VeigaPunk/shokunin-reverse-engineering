# R39C1CounterLessons — round-39 wave 1 (pre-freeze), seat report

Verdict: **DONE** — the counter-failure history is distilled into a pre-freeze checklist
(23 lesson rows + 5 C1-observable rows + 7 C2 clauses), and the round-38 counter is reviewed
against it with live mutant evidence: **7 of 9 hand-built failure classes pass the frozen
round-38 counter green**, each mapped to a clause the round-39 successor must change.

## Deliverable

- **Checklist (primary artifact):** `.ufo/waves/round-39/w1/artifacts/R39C1CounterLessons/checklist.md`
  - Section A: failure class → counter check → one-line test (L1–L23), sourced to QUALITY rows
    55–81 and the round-34…38 verifier spot-checks.
  - Section B: round-38 counter review with the mutant table.
  - Section C: R39-C2 held-out clauses, including one **design defect to resolve before the
    freeze**: `avm-marker-be-dropped` vs `body-extractor-failure` is not separable from envelope
    bytes alone (probe evidence below); the triage table must bind the input-side AVM superblock
    test (`mkfs_time == bytes_used`) or the class pair is not executable as drafted.
- Mutant harness + raw results (same dir): `r38c1-mutants.py`, `r38c1-mutant-results.json`.

## Evidence

1. **Sources read** (all read-only): `corpus/QUALITY.md` rows 55–81 (the file has **no rows
   75/76** — numbering jumps 74 → 77; `grep -n '^\| 7[456] '` hits only 74 and 77);
   `corpus/lessons/round-3{4,5,6,7,8}-verifier-spotcheck.md` in full; `plans/round-39-claims.md`;
   `tools/round-38/c1-counter.py` (395 lines, full); `.ufo/waves/round-38/c1/carriers.json`;
   `corpus/evidence/round-38/c1/K{1,2}/after.json` (gap/diagnostic/chunk fields extracted via jq
   filters); `SKILL.md:1225-1260`; `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/summary.json`.
   Base verified: `git rev-parse --verify a2f64e1d…^{commit}` → `a2f64e1d round-38 verifier
   spot-check (integrator, hyaku)`.
2. **Counter selftest baseline** (scratch, frozen bytes unmodified):
   `HYAKU_SCRATCH=$S python3 -I -B tools/round-38/c1-counter.py --selftest --pkg65
   /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` →
   `{"selftest": "c1-counter", "cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}`,
   exit 0 — matches the committed round-38 tally.
3. **Mutant harness** (`r38c1-mutants.py`): imports the frozen counter module unmodified,
   rebuilds its own green-fixture shape (carriers/oracles/PROVINCE/SOURCES/README/entry, evidence
   id minted via `tools/round-27/xpin-attribute.mjs` under node), commits a freeze then a data
   commit in a throwaway git repo per case (`-c user.name=fx -c user.email=fx@fx` inside the
   fixture; `rev-parse --show-toplevel` verified == fixture dir), and scores one lesson class per
   case. Results (want_exit is what a round-39 successor must return):
   - **Blind (exit 0, must be 1):** M-A shadow Core heading first-wins (QUALITY 77);
     M-B frontier decoy line, unscoped check (substring-anywhere); M-C after.json already present
     at the freeze (no first-added/ancestry check — the copied-round-38-receipts kill control
     would NOT be caught by the current design); M-D SOURCES row `status=rejected` (status column
     never read); M-G coverage-map stem substring (`…-recursion-v2`); M-H carrier blob bytes
     swapped under frozen pins (counter never hashes carrier binaries, QUALITY 49); M-I measured
     rev an orphan commit not descending from the freeze.
   - **Caught:** M-L used-by path suffix (list membership, not substring); M-J stub entry without
     a `source:` line (S-id boundary regex).
4. **Symlink-rule observability** (grounds checklist L24/L25, from committed round-38 receipts):
   K1 after → `diagnostics[].report.__typename__ == ["MaliciousSymlinkRemoved"]`, 0 gaps,
   5/5 oracle hits (escaping link removed, no gap); K2 after → diagnostics `[]` + one gap
   `{kind: unpublished-entry, relative_path: firmware.bin_extract/var/lib/run-link}`, 3/3 hits
   (in-tree link kept as metadata + gap). Both classes are keyed on structured fields, never
   stderr prose.
5. **AVM/body class separability** (grounds checklist C5): `summary.json` — AVM-marker run:
   `chunk_extraction_failed: true`, `gap_kind: extractor-failure`, `files: 0`, stderr "SquashFS
   version [1024.0] … suggests a SquashFS image of a different endianess / read_id_table:
   failed…"; patch rule `mkfs_time := bytes_used` (offsets 8 w4 / 40 w8, BE). A damaged body
   presents the same envelope shape, so the C2 table must bind the superblock discriminator.

## Clause changes a round-39 successor must make (short form; full table in checklist §B)

1. Commit-history checks: receipts (and the knowledge entry) absent at the freeze and first added
   in a commit descending from it; `merge-base --is-ancestor freeze rev`; zero freeze-drift over
   kill-rule paths (M-C, M-I; QUALITY 44/55/79).
2. Re-hash frozen inputs at the measured rev: carrier blobs vs pins, oracles, symlinks.tsv (M-H;
   QUALITY 49).
3. Replace `gaps == []` with symlink-rule semantics: `unpublished-entry` exactly on in-tree
   links (recompute in-tree/escaping from `(dir, target)`, disagreeing tsv → unevaluable);
   escaping links unpublished + `MaliciousSymlinkRemoved`; no `extractor-failure` gap / failed
   chunk.
4. Section- and cell-scoped, token-boundary matching for the Frontier note, Core row, SOURCES
   row, coverage-map stem (M-A, M-B, M-G); shadow/duplicate headings enumerated, first-wins
   banned, contradictory rows fail (QUALITY 77).
5. SOURCES binding adds `status == mined` + row new since the base blob (M-D; QUALITY 45/74).
6. Receipt provenance fields: argv, xpin digest, commit bytes, UTC instant, `caller_asserted`,
   provider version pin (`26.6.4` observed in committed receipts) (QUALITY 73/78).
7. Selftest gains the seven blind classes as red cases, plus escaping/in-tree gap cases, a
   no-reader case, and the existing `S1120` red case kept.

## Residual risk and verification gaps

- Mutant fixtures use the counter's own selftest fixture shapes (dev-after.json), not real REA
  envelopes over real carriers; the blind classes shown are binding-logic classes, so the
  simplification does not affect the verdicts. Per HELD-OUT discipline no REA run was made on any
  K5/K6 or held-out material, and none is needed for this item.
- The r39 predicate's "no failed chunk" wording is mapped to observed fields
  (`chunk_extraction_failed`, `gap_kind: extractor-failure`) from the probe and committed
  receipts; the actual envelope schema for a *partially* failed multi-chunk run was not observed
  (no such committed receipt) — flagged in checklist L26 as a recon item, not assumed.
- Whether `rea-agents` version is machine-checkable inside a committed envelope (vs
  `caller_asserted`) was not established; checklist L27/L28 pin provider `version` (observed) and
  leave the agents version as receipt provenance.
- QUALITY rows 75/76 are absent from the current file; the assignment's "rows 55–81" is
  interpreted as the rows numbered 55–81 that exist (55–74, 77–81).

## Bounds and hygiene

- Wrote only: this report, and `checklist.md`, `r38c1-mutants.py`, `r38c1-mutant-results.json`
  under `.ufo/waves/round-39/w1/artifacts/R39C1CounterLessons/`. No VCS-mutating command anywhere
  (only `rev-parse`, and fixture commits inside throwaway `$S` repos). No subagents, no
  background jobs, no `agent://all`.
- Scratch: `S=/fast/scratch/hyaku/kaidoku-r39/R39C1CounterLessons` (also `HYAKU_SCRATCH=$S` for
  the counter's internal scratch); removed before finishing; cited outputs copied into the
  artifacts dir first. `/tmp` unused.
- Tooling: nothing installed or updated (pacman untouched; sasquatch/sasquatch-v4be/unblob
  untouched; used existing node via fnm, python3, git).
