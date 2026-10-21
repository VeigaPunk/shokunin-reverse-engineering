# ReviewSourceReuse — round 23

Review scope: inherited S051–S057 records, the R23 source/`used-by` gate, and whether signal sources are being used to claim REA-specific fields. Author-side review only.

## Findings

### High — the R23 counter does not enforce S051–S057 immutability

**Observation:** the frozen no-harm contract says “All pre-round knowledge and source rows unchanged” (`.ufo/waves/round-23/claims.json:55-61`). The current counter measures historical eligibility at the fixed R22 baseline (`.ufo/waves/round-23/tools/count-c1.py:57-60`), then parses the requested revision's `SOURCES.md` (`:61-67`). It uses current rows only in the new-source test (`:80-85`) and never compares S051–S057 (or their existing `used-by` fields) with the baseline. Therefore its count can remain unchanged while a requested revision alters inherited rows; the count alone cannot substantiate this no-harm requirement.

The `old_source` fixture rewrites an S051 `used-by` field and expects that S051 cannot qualify a new entry (`counter-fixtures.py:69-79`, expected result in `frozen/expected.json:33-36`). It does not require the counter to reject the changed inherited row. This is a missing invariant check, not an observed mutation: both `git diff --exit-code aa1450b82f9ede35aada63efe8a34e01c6e02f72..HEAD -- corpus/SOURCES.md corpus/knowledge` and the working-tree equivalent exited 0; `git status --short -- corpus/SOURCES.md corpus/knowledge` was empty.

### Medium — new-source `used-by` admission is existential, not row-complete

**Observation:** `count-c1.py:80-85` sets `eligible = True` when *any one* cited source ID has a qualifying S058+ row whose `used-by` list contains the entry; it skips the entry only when none qualify. Thus, for an entry citing two new rows, a correctly linked S058 can make the entry eligible even if the other cited S059 row omits that entry or is otherwise ineligible. The current `wrong_usedby` fixture tests one cited source with one bad `used-by` value (`counter-fixtures.py:74-75`), not a mixed valid/invalid citation set. The frozen clause requires new knowledge to cite mined S058+ with exact `used-by` (`claims.json:26-37`); absent an explicit “at least one” interpretation, the implementation does not enforce reciprocal linkage for every new source actually cited by the entry.

No S058+ registry row or round-23 knowledge entry exists in the current corpus snapshot, so this is an implementation gap, not a claim that a live row is already malformed.

## Source-scope review

- The inherited rows themselves remain intact in `corpus/SOURCES.md:57-63`: S051 is limited to Flutter release-mode documentation; S052 is narrowed by S054, whose row explicitly disclaims REA field semantics; S053/S055 are bounded own-work observations; S056 is only the CLI alias; S057 is the original Godot envelope and explicitly not authentication. `corpus/SOURCES.md:65` has already moved into `## Paths`, so S057 is the last row; no S058+ row or new knowledge entry is present.
- The round-23 candidate report `.ufo/waves/round-23/w1/SignalCarrierAlternatives.md:20-60` supports the pinned `sigrok-dumps` fixture metadata (8n1, 9600 baud, TX and sample-rate details). Its own lines 84-88 say no UART decode was performed. It cannot support REA's `normalized_result`, annotation field names, inventory completeness, or paging behavior.
- The working UART decoder source copy `.ufo/waves/round-23/w1/_uart/pd-tag.py:28-48,95-143` describes decoder packet/RX-TX semantics, channel/options, and annotation identifiers; those are signal semantics, not REA envelope fields. Its source identity/pin has not been recorded in `corpus/SOURCES.md` at this snapshot. The retained REA observation is instead `.ufo/waves/round-23/evidence/c1/decode-uart-hi.run.json:2-25` and the paired envelope: the command used `uart:rx=0:baudrate=9600`, `binary:numchannels=1:samplerate=960000`, `REA_SIGROK_COMMAND=.../tools/sigrok-cli.sh`, exited 0, and its synthetic target SHA-256 is `4a2e729f514482287c17596cff3b29f07141fae9e86353680c99b1065e861727`. That is an observed REA result, not documentation of REA's output schema. Keep any new knowledge explicit about this distinction.
- The counter itself documents that “source relevance/admission remain manual” (`count-c1.py:4-8,102-107`). Its field checks establish only row metadata/linkage; they do not prove that a source semantically supports the statement. The planned signal source must be reviewed for the precise signal-level claim before being used.

## Verification gaps and residual risk

- `lsp` is not a mounted device: `read xd://lsp` returned “No such tool” and listed the mounted devices. No LSP status/references/definition/diagnostics were available; code locations above were read directly after literal search navigation. No build, test, formatter, or REA command was run by this reviewer. Existing run records were read as data only.
- No actual S058+ registry/knowledge pair is present yet. Final source relevance, exact `used-by` closure, and any later R23 source edits therefore remain unreviewed. The current source-row diff is clean, but the counter does not enforce that inherited-row invariant.
- Installed or updated tools: none.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewSourceReuse.md` — this review. Its raw SHA-256 is supplied in the response trailer rather than embedded in the file, to avoid self-referential hashing.
