# SourcesOverlap — prior SOURCES rows and leads that overlap EVM selector naming

Seat `KaidokuR25a3.SourcesOverlap`, leaf, lane read-only. Measured at lane tip
`08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` (`git rev-parse HEAD`, exit 0, 2026-10-22T10:48:23Z),
baseline `18e7eb6d`. Each cited command is in `verification-log.txt` (run
2026-10-22T10:38Z–10:48:23Z; exit 0 unless stated) or its output is in `sources-hits.txt` /
`knowledge-hits.txt`. No web page opened, no REA call, no tool installed.
The working tree is dirty from other seats (`SCORECARD.md`, `corpus/lessons/round-25.md`) and one
began rewriting the entry after my read, so entry line pointers are from the committed tip blob.

## Census of the assigned terms

- `corpus/SOURCES.md`: 10 matching lines; 6 are EVM-subject (27, 81, 82, 83, 98, 142); lines 89,
  111, 113, 115 are the Go "selector" (version selector), incidental. [observation]
- `corpus/knowledge/`: 24 files match any term; 11 are EVM-subject, 13 match incidentally
  (`selector` as a CSS/ASAR/API parameter, `4-byte` as a size). [observation]

## What already exists

**F1 — No earlier SOURCES row covers selector-to-name resolution.** [observation, confidence high]
S021 (`SOURCES.md:27`) is the only pre-round-25 row in this space. Scope cell:
`Solidity ABI selector and canonical signature rules, not selector-name resolution`. Teaches cell:
`it does not supply a selector-signature database`. No row before S075 names 4byte, openchain,
Sourcify or EVMole (grep, exit 0). S075–S077 (`:81-83`) are therefore the first signature-database
rows, not a duplicate of anything. Verdict: holds.

**F2 — No earlier knowledge entry claims naming; only premise statements.** [observation, high]
The only pre-existing statement of the gap is
`corpus/knowledge/2026-10-13-r3-evm-interface.md:142` — `selectors stay as bare hashes (no signature
DB → no name resolution),`. Its "Remaining EVM frontier" (`:144-147`) lists solc/vyper contrast,
larger tables and Vyper layouts, and does not carry naming as an open lead. The arc3 family states
the same premise and inference caveat: `arc3-r1:28`, `arc3-r3:32`, `arc3-r4:27`, `arc3-r6:29`,
`arc3-r8:15`, `arc3-r9:15` ("… remain upstream inferences"; "not verified … names"). These agree
with the new entry's labelled-candidate rule and conflict with nothing. Verdict: holds.

## Defects found

**F3 — The old naming-limit stamp has no backward pointer.** [observation, high; fix is integration]
`2026-10-13-r3-evm-interface.md:142` still reads as above at tip, and the file never mentions the
new entry (`grep -c '2026-10-22-r25'` → 0, exit 1). `git diff --name-status 18e7eb6d..08c7a729 --
corpus/knowledge` shows the entry as the only knowledge change, so the earlier entry is unannotated
by design of the no-harm rule. The only link is forward: `PROVINCE.md:91-93` at tip names the entry.
Verdict: fails (stale, unpointed limitation); cheapest close is one line in the r3 Errata section
(`:149`) naming the entry, or an explicit decision that PROVINCE is the sole pointer.

**F4 — S021 back-reference is incomplete.** [observation, high; severity low]
The entry's `source:` line (`:1`) cites S021: `… S077 EVMole interpretation reference; S021 Solidity
ABI specification (Function Selector, opened 2026-10-19)`. S021's used-by cell is only
`corpus/lessons/round-13.md`. QUALITY row 29 and `SKILL.md:689` require at least one qualifying row,
not an exhaustive list, so no gate fails; the registry cell just under-enumerates a consumer.
Close by appending the entry to S021 used-by or dropping S021 from the entry's source line.

**F5 — S075–S077 used-by cites a lesson text that is not committed at tip.** [observation, high]
Each used-by cell reads `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md,
corpus/lessons/round-25.md`. At tip that lesson blob is 356 lines and contains no S075
(`git show 08c7a729:corpus/lessons/round-25.md | grep -c 'S075'` → `0`, exit 1; `wc -l` → `356`).
The attempt-3 gate table citing S075–S077 exists only as uncommitted worktree content:
`git diff --stat -- corpus/lessons/round-25.md` → `33 insertions(+)`, author not determined here.
If that append does not land, the lesson half of used-by overstates. Verdict: fails at the measured
revision; state-dependent, so re-check after the lesson commit.

**F6 — S076's "now answers openchain lookups" claim is contradicted by the lane's own manifests.**
[observation, high] `SOURCES.md:82` scope: `the service that now answers openchain lookups`; entry
`:28`: `The openchain lookup, now served by Sourcify (S076)`. Host census over the six
`db/manifest.json` files: `rows 138`, `api.openchain.xyz 69`, `www.4byte.directory 69`; first
openchain row `https://api.openchain.xyz/signature-database/v1/lookup?function=0x095ea7b3&filter=false`,
`"status": 200`, `"utc": "2026-10-22T08:28:11Z"`. `api.4byte.sourcify.dev` was never contacted.
The saved swagger copy (`corpus/evidence/round-25/a3/sources/sourcify-4byte-swagger.json`) lists its
own servers (`api.4byte.sourcify.dev`, staging, localhost) and says only
`This API maintains compatibility with openchain.xyz behavior`. The cited document therefore
supports the `filter`/`filtered` vocabulary by compatibility, not as the responder. Verdict: fails
(counterexample = the manifest URL); close by narrowing both wordings to "an openchain-compatible
service", or add a row for api.openchain.xyz's own documentation.

**F7 — The paths section is stale and incomplete.** [observation, high]
`SOURCES.md:98`: `EVM selector boundary — S021: … selector-to-name resolution remains outside that
specification and is not newly claimed.` Round 25 now claims a naming procedure (entry `:5`, rule at
`:60-75`), and no path line covers S075 → S076 → S077. Read strictly against "that specification"
the clause is still true, so the defect is ambiguity plus the missing successor path. Verdict: fails
as a current path statement; close by appending a signature-database path line.

**F8 — Leads list has no selector item.** [observation, high]
`SOURCES.md:144` `## Leads (unopened)` holds only the binary-lifter SoK and LLM4Decompile
(`:146-147`). Nothing there to close. The one lead this audit proposes: api.openchain.xyz itself is
opened nowhere and has no row, while its responses are 69 of the 138 saved lookups. Close by row or
by an explicit reject note. Verdict: holds (no stale lead), with that addition.

**F9 — Wave-internal census items are now false, but frozen.** [observation, high]
`.ufo/waves/arc3-loop1-round4/claims/c2/verdict.md:198` (`no corpus entry claims a signature DB`)
and `.../claims/c2/EX-17/before.md:225` (`no corpus signature-DB claim`) no longer describe the lane.
They are historical wave records; do not edit and do not cite as current.

## Attack verdicts

- Earlier row already covers naming → holds: none; S021 excludes it.
- Earlier entry already covers it → holds: none; only premise and caveat statements.
- Earlier entries conflict with the new rule → holds: they match its labelled-candidate framing.
- Registry back-references consistent → fails: F4, F5.
- S076 documents the responding service → fails: F6.
- Paths and leads current → path fails (F7), leads hold (F8).
- The old naming limit is closed → fails (F3) unless the PROVINCE forward pointer is accepted.

## Unknowns

- Whether api.openchain.xyz and the Sourcify clone agree on `filtered`/`hasVerifiedContract`
  semantics beyond the documented compatibility. Not measured; no openchain.xyz page opened.
- Whether the uncommitted 33-line lesson append lands; at tip it has not.
- Whether the lane treats `used-by` as exhaustive or existence-only; only a single qualifying row is
  required by QUALITY row 29 and `SKILL.md:689`.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r25-a3/seats/SourcesOverlap/)

- `verification-log.txt` sha256 `ca7f8be08231315c5aecd7fb4bf0cb0faec9c5f73d72f7a7e81ac2f3385ef75a`
  (all commands, timestamped, with exit codes)
- `sources-hits.txt` sha256 `d4aef29e4aee04b203b3c52886b9537234018f2b20b5869692b9ec103b91cb8d`
- `knowledge-hits.txt` sha256 `974bd57d0f742f59ed3e51efa00add9f2ec328edcb161dc01aaeb300ed81f2d7`
- `hosts.txt` sha256 `e44890b3e742c976672f2659102cc738145bd5370463e6e601c49daf3e350956`
- `lessons-round-25-at-tip.md` sha256 `b88399f24d8dd27d9b8e30781b6a64630febb1cfec3d04418b1132d68e53399d`
