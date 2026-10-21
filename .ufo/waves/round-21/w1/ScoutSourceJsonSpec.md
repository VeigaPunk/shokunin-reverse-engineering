# ScoutSourceJsonSpec — RFC 8259 duplicate-member support

## Finding

**C1 calibration support, narrow.** RFC 8259 §4 recommends unique object names and says software behavior for duplicate names is unpredictable. Its examples include last-name/value-only behavior, parse errors/failure, and reporting all pairs. This supports treating contradictory duplicate operation members as ambiguous rather than accepting a last-wins interpretation. The RFC does **not** mandate a particular parser response or the fixture's exit code; rejecting this evidence representation with the local `duplicate_member_ambiguity` expectation is a validator policy consistent with the RFC's interoperability warning, not an RFC-defined requirement. This is not Evidence authentication, integrity proof, or security certification.

> “When the names within an object are not unique, the behavior of software that receives such an object is unpredictable.”

**Quote length:** 20 words. **Location:** RFC 8259, §4 “Objects,” page 6. **Published:** December 2017.

**External source opened:** `https://www.rfc-editor.org/rfc/rfc8259.txt` on 2026-10-21; the RFC Editor reader identified the canonical resource as `https://www.rfc-editor.org/rfc/rfc8259` (RFC Editor JSON API). The located Section 4 text explicitly continues that some implementations report only the last pair, others report an error or fail parsing, and some report all pairs including duplicates.

## Local scope anchors

- `.ufo/waves/round-21/fixture-contract.json#/C1/11` (`duplicate_member_ambiguity`): expected exit 2; contradictory duplicate operation names must not select last-wins success. Neighboring frozen positive and negative cases remain part of the denominator.
- `.ufo/waves/round-21/claims.json#/claims/0` (`C1`): record-bound operation/id/refusal predicate with independent controls; its scope explicitly excludes cryptographic Evidence authentication and security certification.
- `corpus/lessons/round-20-verifier-spotcheck.md`, “Routed residuals” / `R20-EVIDENCE`: historical note calls for operation-mismatch/refusal negatives and comparator asymmetric-null/kind negatives; read as context only, not as RFC authority or a new test result.

## Scope and checks

Read-only source research only: opened the official RFC and the named local claim, frozen fixture contract, and R20 lesson. No row was written; no production file, test, REA tool, provider, carrier, or live target was run; no tool was installed. Parent should run the frozen C1 battery at the owned revision and verify that `duplicate_member_ambiguity` exits 2 while the declared positive control still succeeds; preserve the frozen denominator. No such check was run here.

Report: `.ufo/waves/round-21/w1/ScoutSourceJsonSpec.md`
