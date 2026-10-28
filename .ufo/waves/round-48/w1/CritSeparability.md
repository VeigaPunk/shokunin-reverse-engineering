# CritSeparability — Round 48 causal-separability review

Axes: **depth** (C1) and **calibration** (C2). The causal question is whether scoring either claim requires the other's landing surface.

## Result: the declared claim surfaces are separable; the instruments share infrastructure

C1 `meanings.py` reads the committed `SKILL.md`, the `tools/round-48/census2.json` and its derivation inputs, the frozen round-48 tools, plus cited files needed for reference validation. Its `score()` path has no `SCORECARD.md` read. The freeze integrity gate also checks frozen paths and revision history, not the C2 record surface.

C2 `record2.py` receives the committed `SCORECARD.md`; it executes `tools/round-47/record.py` by fetching its body with `gate.show(root, rev, ORACLE)` and `exec`-compiling it. It also reads cited receipt files and dispatch files via the oracle's collection/correction logic. It does not read `SKILL.md` or the C1 craft block. The frozen tools and claims-file bytes are used by the common freeze gate, but are not the other's landing artefact.

Thus a revision containing only a valid C1 craft/registry landing can be scored by C1 without a SCORECARD landing, and a revision containing only a valid C2 record landing can be scored by C2 without a craft-block landing, subject to the independent freeze contract and other clause prerequisites. This is a source-level dependency proof, **not** a measured two-revision counter experiment: no valid landing fixtures were present in my assigned evidence, and I did not modify or run against a fabricated landing. Do not report the requested “score each at a revision where only the other's artefact exists” as measured.

## Shared inputs (explicit)

- `tools/round-46/gate.py`: imported by both counters; supplies revision reads, freeze derivation/integrity, scratch and CLI guard helpers.
- `plans/round-48-claims.md` and `tools/round-48/` frozen bytes: both use the same freeze identity/path contract. C1 additionally reads `census2.json`/`census2.py`; C2 executes the round-47 oracle and examines scorecard evidence.
- Git repository state/revisions, including committed tree/history, are common environmental inputs to both.

There is no evidence that either counter reads the other's claimed surface (`SKILL.md` craft block vs `SCORECARD.md`). Shared frozen infrastructure is not a shared claim surface and should not be mistaken for causal coupling.

## Counterexample/evidence and correction

The existing review `w1/CritAxis.md` identifies a separate C1 false-green: `registry_rows()` recognizes only lines whose stripped form starts `| \``. A Markdown row beginning `|  ` + backtick is skipped, while path-set and meaning checks only inspect parsed rows. An extra forged registry row can therefore avoid the claimed per-row meaning check without changing the extracted census path set. This is a depth issue, not evidence of cross-counter coupling. Smallest safe correction: parse all data rows in the bounded registry table (allowing optional horizontal whitespace after `|`) and fail closed on malformed row shape; include this variant in battery/selftest.

C2 source evidence: `record2.py` lines 62–72 loads the oracle from `gate.show(root, rev, ORACLE)`; lines 207–243 impose the round completeness/axes floor; lines 245–315 re-derive corrections, bind quoted values to cited receipts, and check score cells. C1 source evidence: `meanings.py` lines 303–418 reads skill block and semantics; lines 418–453 check the registry/census; `evaluate()` lines 533–552 reads committed skill at `rev` and invokes the freeze gate.

No counter commands were run, so there are no command receipts, exit codes, stdout hashes, or measurement-based ratings to claim. No installs. Only this scoped report was written.
