# R21Attack57 — RFC 8259 source check

Axes: calibration; depth.

- **Reopened:** [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) on 2026-10-21, from RFC Editor text.
- **Located quote (8 words):** “The names within an object SHOULD be unique.” Location: §4, “Objects,” page 6.
- **Observed context:** §4 defines an object as name/value pairs and a member as `string name-separator value`. It says unique-name objects are interoperable in that software agrees on name/value mappings; duplicate-name receiver behavior is unpredictable, with implementations variously retaining only the last pair, rejecting/failing to parse, or reporting all pairs.
- **S049 row:** `corpus/SOURCES.md`, row S049. Its location/date and duplicate-name interoperability scope match the reopened source. Its limitation—this does not establish Evidence authenticity or require every application to accept every JSON value—is appropriate.
- **Gate:** `corpus/lessons/round-21.md`, §Gate, S049 row. **Agree, within the stated scope.** The quote is contiguous, correctly located, and short. RFC 8259 supports JSON object member uniqueness as interoperability guidance and explains the consequences of duplicate names. It does not specify REA Evidence fields, authenticate records, or establish that an operation identifier and verb are semantically bound. That latter same-record/application-field rule is a lane contract, not a result supplied by this RFC; the Gate explicitly makes that distinction.
- **Remaining unknown:** None for this source/quote/scope check. No claim is made here about whether the lane's application-specific predicate is correctly implemented or whether other evidence satisfies it.

No source edits or tool installs.