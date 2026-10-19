# C1 quality check — `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`

Checked against every row of `corpus/QUALITY.md` (15 admission criteria, 6 weak signals). Line numbers refer to the new corpus entry.

## Admission criteria

| # | criterion | verdict | evidence |
|---|---|---|---|
| 1 | Resolvable source | PASS | `source:` line names repo-relative evidence paths + absolute package paths; every claim cites `path:line` |
| 2 | Falsifiable | PASS | formula + IDs re-derivable via recorded `recheck:` commands and `recompute-ids.py` |
| 3 | Domain-specific | PASS | REA `ev_` Evidence-ID projection mechanics on this host's pinned package |
| 4 | Artifact named by absolute path + SHA-256 | PASS | `/usr/bin/docker` + `70f68a77…f45c9`, 29,327,600 B; both copy paths named absolutely |
| 5 | Every conclusion labeled observation / inference / unknown | PASS | bullets tagged `OBSERVATION`/`REPRODUCED`/`INFERENCE`/`UNKNOWN`; decompiler-free, source-line citations kept as facts about code, not behavior |
| 6 | REA claims cite Evidence ID or exact reproducing call | PASS | six `ev_` IDs inline; exact CLI invocation in `calls.txt` + `recheck:` line |
| 7 | Names what was NOT examined | PASS | "Scope and limitations": no other formats/operations/releases, no missing-metadata or error envelopes, no path-free projection, no target execution |
| 8 | Capability claims pin tool/provider versions | PASS | `rea-agents@6.7.0` pinned by absolute path and five source SHA-256s (`package-source-hashes.txt`); scope bound to that release |
| 9 | Runtime-behavior claims only with runtime provenance | PASS | none made; explicitly states target not executed, metadata is not runtime evidence |
| 10 | "Held" only for verbs run this round on a real carrier | PASS | `inspect_go_binary` run 4× stored + 4× live rerun on real `/usr/bin/docker` bytes |
| 11 | Empty/zero findings state parsed-vs-excluded | PASS | no empty/zero findings asserted; limitations record unexamined surfaces explicitly |
| 12 | Synthesized carriers retain bytes/recipe | PASS | copies are `cp` of `/usr/bin/docker`; recipe in `recheck:`; byte-exactness claimed only via measured SHA-256 |
| 13 | Verify commands reproduce | PASS | recheck uses `sha256sum`/`stat`/`python3` commands as recorded; no grep-count pattern used |
| 14 | Evidence-id domain stated as f(content, path, params) | PASS | Result section: path sensitivity attributed to three named semantic fields; cross-path identity cites `subject.digest.sha256` |
| 15 | Per-verb-family domain, never universal | PASS | formula bound to `inspect_go_binary`/6.7.0/this call shape; "not a universal rule" stated twice |

## Weak signals

| # | signal | verdict | evidence |
|---|---|---|---|
| 1 | Layout/strings narrated as behavior without Evidence ID | ABSENT | no behavior claims; all claims carry envelopes or source-line cites |
| 2 | Negative/"all" claims without search command | ABSENT | none asserted |
| 3 | Findings on unnamed artifact | ABSENT | path+SHA-256 throughout |
| 4 | Capability asserted from docs without live check | ABSENT | all claims from live CLI calls this round + stored envelopes |
| 5 | Dynamic claims from static artifacts | ABSENT | static-only; explicit "does not execute" notes |
| 6 | "Tool broken/missing" without spawn-wrapper check | ABSENT | no such claim |

Verdict: 15/15 PASS, 0/6 weak signals present.
