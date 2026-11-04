# ScoutSurfaces — round83 bounded compatibility reconnaissance

Axes: attribution precision, historical compatibility, frozen-scope preservation. Author-side source evidence only; no admission, integration or production changes.

## Observed source evidence

- `corpus/lessons/round-82-verifier-spotcheck.md:74-78` explicitly routes the distinction between lexical S299 presence and positive attribution. It retains round82 C2's failed target and rejection. Other obligations remain: seven mutation survivors, old round81 outer-selftest, receipt-auth/gate-exits, r63 sweep, concurrent replacement race, substantive-report evidence and planner/protocol wording debt. Round83's finite attribution claim does not discharge them or require retrying the old new-S299 target. Outside review also asks for document/anchor/proposition novelty selection; this round explicitly claims no novel authority.
- `tools/round-82/printed-command.py:257-261`, `entry_cites`, returns membership among all `\bS[0-9]+\b` tokens on the first line starting exactly `source:` anywhere in the text. It does not require three digits, a leading list, an em-dash delimiter or a twelve-line window. It does not inspect subsequent source fields. Caller `sourced_arm:264-289` stores that boolean as `entry_cites_row` and independently checks mined/date/base/plan conditions. Hence correcting attribution alone cannot turn round82's rejected source row into a valid mined row.
- Read-only `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 650344bc37ca303fb9487c1174192057af499b9b:corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md` exited 0. Its first line positively names S286 and later says `duplicate S299 withdrawn in-round`. This is committed real-entry evidence, not a synthetic substitute.
- `tools/round-83/attribution-audit.py:32-60` loads that real entry from its fixed BASE, fixture bytes from the freeze, and the target function from the requested commit. It checks exact bool outputs, eight unique cases and two real cases. The eight frozen cases include list/commentary/withdrawn-head/absent/embedded-id boundaries, but no duplicate-field, malformed-list, digit-width or twelve-line-boundary case. This is a coverage limit, not permission to edit the frozen fixtures.

## Four-entry bounded historical sample

This is a deliberately selected compatibility sample, not a corpus census. Only the real round82 entry was independently fetched from the committed BASE; other sample headers are observed worktree source text.

| Entry and anchors | Observed convention | Consequence under declared round83 grammar (static inference) |
|---|---|---|
| `corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md:1` | `source: S286 — ...; duplicate S299 withdrawn in-round` | S286 true; S299 false; the required real correction. |
| `corpus/knowledge/2026-11-04-r81-registry-and-record-boundary.md:1` | `source: S258 — ...; S255 — ...` | S258 binds; S255 is commentary, not a second positive id. Semicolon-separated historical attribution is not migrated by this grammar. |
| `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:1` | `source: S001, S003, S004, S007 in ...` | No immediate ` — ` after the id list: entire header is unbound, despite meaningful historical provenance. |
| `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12-14` | Three separate `source:` fields; first is line12, others line13/14 | Concrete window/duplicate boundary. A whole-entry duplicate prohibition rejects it; counting fields only inside the twelve-line window would instead see one. Do not claim universal historical compatibility. |

## Actionable grammar boundaries (inferences, not executed parser results)

Keep the frozen predicate, counter and fixtures unchanged. Candidate compatibility should be stated narrowly:

1. Exact lowercase, column-zero `source:` and an inclusive first-twelve-lines header location are house syntax; body references, uppercase/indented labels and line13-only headers are not positive attribution.
2. Require the complete leading comma-separated list and `space-em-dash-space` separator. Empty ids, empty/trailing/doubled commas, non-S tokens, fewer than three ASCII digits, Unicode digits and replacement hyphen/en-dash delimiters are malformed rather than partially salvageable. S299 must not match S2999. Commentary after the separator is never additional attribution, including a later `S255 —` fragment.
3. Duplicate source fields must not use first-wins/last-wins behavior. The plan says duplicated source fields are unbound, while its twelve-line wording leaves detection scope insufficiently explicit. The R44 header is a concrete witness distinguishing whole-entry duplicate detection from window-only detection. L1 should disclose that boundary rather than imply the eight frozen cases decide it. This report does not alter the declaration.
4. Exact acceptance of tabs, multiple spaces, repeated ids inside one list, and additional source fields after line12 is not fully settled by the eight cases. No runtime behavior for the round83 candidate is asserted here. Prefer fail-closed documented house syntax over prose inference; do not silently broaden scope to historical migration.
5. Retain the round82 receipt bytes and qualify its old `entry_cites_row:true` as lexical presence. Do not relabel the old rejected claim as successful or imply all historical provenance becomes invalid merely because it is outside the new local grammar.

## Directory and optional report checks

Directory-tool glob `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/**/considerthese/` with hidden paths enabled and gitignore disabled returned no matches. A broader `**/considerthese*` search found only six historical R44 artifact files named `considerthese-*`, not a directory. Thus no lane `considerthese` directory was observed; this does not assert anything about external paths.

No `/home/vgpnk/Projects/shokunin/merge/` directory was found. Read-only targeted inspection of the discovered fleet report `.ufo/reports/round-82/kaidoku.md:8-10,56-64,155` corroborates the withdrawn S299 admission, C2 honest stop, seven survivors, old debt and no assimilation. No material was assimilated, no fleet file written, and no external admission authority exercised.

## Method, confidence and remaining gaps

High confidence in literal source/header facts and committed real-entry bytes; moderate confidence in compatibility predictions because these are static deductions, not candidate executions. `xd://lsp` returned `No such tool`; semantic definition/reference lookup was unavailable. Definition/caller discovery used literal targeted grep followed by exact source reads, not semantic reference proof. No cold semantic result was treated as absence.

No builds, linters, formatters, scoring/selftest gates, fixture probes, clones, Git/JJ mutations, production changes or installations/updates were performed. No scratch directory or scratch files were created, so none remain to remove. No tool/version/channel install record applies. Own report is the only written artifact. Initial exploratory reads were broader than necessary; final findings are anchored to the bounded sections above.

Self-assessment (not an expertise/admission score): accuracy 4/5 (committed real bytes and exact source anchors; candidate behavior unexecuted); completeness 4/5 (assigned sample, debt and directory checks covered; whitespace/duplicate-scope contract remains unresolved by fixtures); clarity 4/5 (observations separated from inference; several boundary cases necessarily grouped); actionability 4/5 (specific compatibility caveats; frozen fixture coverage cannot establish broader behavior); conciseness 4/5 (bounded report, but method disclosures add length). Overall 4.0. Highest-impact improvement: L1 should make the duplicate-detection scope explicit in its compatibility disclosure, without rewriting the frozen case population. A user can reasonably agree because the limitations are named rather than presented as passes.
