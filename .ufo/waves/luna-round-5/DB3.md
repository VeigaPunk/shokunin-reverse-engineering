## CLAIM
2nd-opinion draft of the PROVINCE text for the module-identity request-byte pin (debt 3). My assigned input `VB3.md` does not exist anywhere in the repo; per the 2nd-opinion rule I drafted from primary sources only, then compared against Lane A's item-3 seats. `PROVINCE.md:28-33` is the only surface still missing the pin — `corpus/README.md:170` already carries it.

## METHOD
Read-only: `PROVINCE.md:28-35,58`, authority `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`, grep for "request byte"/"module identity"/"authenticate module"; byte offsets recomputed in python on the worktree (`git show HEAD:PROVINCE.md | cmp - PROVINCE.md` → identical). Lane A comparison (V3/D3/F3/G3/R4) made only after my draft. No probes, MCP, or network.

## FINDINGS
Drafted sentence, to sit in the conventions paragraph after `subject sha256.` (`PROVINCE.md:32`):

> When module identity matters, pin the exact request bytes (or re-derive the dossier): an `evidence_id` and subject sha256 alone do not authenticate the module attribution carried in `subject` (founding case: `analyze_function`; `corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md:146-169`).

Insertion mechanics: my offsets reproduce F3 exactly — after `subject sha256.` = byte 2885; after line 33's LF = 2961. Preferred: inline at byte 2960 (line 33's LF), giving zero line-number drift. A new-line insert at 2961 shifts all PROVINCE lines ≥34 and stales recorded citations: `2026-10-14-r14-02-final-sweep.md` (:44, :46, :57, :117-119, :148-153), `2026-10-13-asar-surface.md:87` (:46), `SCORECARD.md:45,79` (:68-73, :107-109, :144-153), `LOG.md:369` (:117), `SHONEN.md:12` (:88-109), lessons `2026-10-15-round-1.md:152` (:107-109). Line 33 grows 42→~190 chars; line 49 is already 865 chars, so long lines are in-family.

Agreement: V3/G3 match this disposition. Divergence: D3/R4 restrict wording to `analyze_function`; I keep the conditional trigger with `analyze_function` as founding case — r9-02:166-169's own inference is conditional-general and the PROVINCE rule it qualifies is family-neutral, without asserting a universal id formula. Recommend leaving `PROVINCE.md:58` untouched (probe-output cell, not a citation duty).

## THREATS
`VB3.md` absent, so this is not a VB3 review. No live reprobe; the pin rests on r9-02's recorded runs. Inline insert breaks the paragraph's ~76-col wrap (accepted to avoid citation drift); F3's 2961 path accepts drift instead.

## VERDICT
FINDING: insert the conditional pin at byte 2960 (inline, zero citation drift); VB3.md absent — draft built from primary sources plus Lane A comparison.
