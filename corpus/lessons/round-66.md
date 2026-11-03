# Round66 — checked ELF span provenance

## Work and evidence

One depth capability acquisition, R66-C1. Basec773575091604b6508386b5f4b1510f96484c822; independent development9c8c6514, sole freeze fb62a6df26162fa6591511b872861afa44178448, first scored data8da550c1b8864ee19cf04ab5f1fc127a743069b5. Original50/50exact; capability still awaits independent terminal judgment. Command: frozen tools/round-66/compare.py over data/fixtures and pinned reader/oracle, actual argv/output percase in data/comparison.json. Numeric owned-axis proxies remain unchanged.

## Gate

Two primary sources opened2026-11-03, both candidate source admissions within stated scope:
- S269: https://gabi.xinuos.com/elf/07-pheader.html, ELF4.3DRAFT section7.2 PT_LOAD. Located rendered quotation: “[source quotation omitted in selective export; consult the cited source]” Supports the filesz/memsz guard; not arbitrary runtime policy.
- S270: https://gabi.xinuos.com/elf/02-eheader.html, ELF4.3DRAFT section2.1 e_phentsize. Located rendered quotation: “[source quotation omitted in selective export; consult the cited source]”. Supports explicitrecord width. Both checked manually in rendered source, not raw-HTML substring certification. No complete source retained.
- Reject inference “equal backing bytes settle loader precedence.” No opened source establishes that, and distinct overlapping candidate origins are retained even if hashes agree. Reject inference “unmapped gap means zero-filled memory”; zero-tail applies only inside a covering LOAD's declared memory span.
- Local no-table traversal policy permits nonzero phoff with phnum0; not an assertion that this satisfies the header spec or full ELFvalidity. Sectionmachine/OSABI/page-size concerns remain outside profile.

Source census atbase175rows(A161,B9,C5),2newA mined rows S269/S270; expected177rows(A163,B9,C5). Final counted receipt required; no old source-row edits. Search record in SOURCES and prep/source-notes.md. Independent outside spotcheck pending; no self-attested discernment.

## Mistakes

| Class | Evidence | Captured by | Fix |
|---|---|---|---|
| Instrument custody omission during prefreeze adaptation | Initial comparator only recorded actual fixturehash; independent PREPARATION-REVIEW caught it before freeze; prep/comparator-selftest-before-pin-repair.json retains old development controls | Protocol Gate standard, pinned input before verdict; QUALITY18/55/61 | Added complete oracle-to-file pin preflight before any reader, snapshot_tampered exit2 and realCLI mutation control, revised14/14. Not a scored failure or retroactive repair. |
| Overbroad first novelty query | prep/novelty-search.txt includes prior PT_LOADinventory/NOBITS and address conversion | QUALITY57 alias/index/filename sweep | Scope claim narrowed to checked interval-provenance decision procedure; prior knowledge retained. |

## Training meaning

New difficult-case judgment is that file/virtual deltas are persegment, conceptual zeros have no fileoffset, gaps are not zeros, and overlapping candidates require explicit uncertainty rather than firstmatch. Fresh50instances use known scenario recipes;28refusal answers intentionally unchanged acrosssalt. No claim of50unseen mechanisms or realworld loader coverage. No carrier loaded or executed, no provider call, no external writes.

## Independent terminal judgment

Reviewer judge_kaidoku_round66: R66-C1 verified and technically admissible. `closure/independent-assessment.md` with independent50/50rerun, exact freeze/data pins and unchanged reader/recipe confirms. Outside spotcheck agrees with admitted file-prefix/zero-tail semantics and rejects both inferred loader precedence from equal bytes and interpreting gaps as zeros. Source tiersA scoped correctly; no unrun native behavior admitted. Final ledger/census/prefile still separate filing duties.

Trend proposals supported by outside judgment: expansion improved (new checked interval-provenance repertoire), quality improved (exact typed evidence and fixture-pin refusal), discernment improved (ambiguity preserved, source vs local profile separated, independent admit/reject spotchecks agree). No axis harm identified, legacy numeric proxies unchanged. Source census executed177rows, validation0, old rows byte-preserved; receipts in closure.
