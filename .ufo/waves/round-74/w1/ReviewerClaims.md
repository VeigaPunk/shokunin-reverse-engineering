# ReviewerClaims — committed-byte review

Axes: predicate fidelity, independent re-derivation, provenance, non-mutation.

Scope: base `04fdc2c4dbedbe5ee50a069af14310068393233e` (B), declaration `b3a7e28089582ce5fb002a1b88e5295caf696b9f` (D), freeze `021914c0e638454e507087accfe41af1ab69f185` (F). Evidence below comes from `git show`, read-only git diff/log/tree enumeration, and independent JSON/byte inspection. No lane instrument was executed. Verdicts are recommendations, not admissions.

## Findings, by severity

### High — verification blocker, not a claim of failed future landing: R74-C2 is not zero at the freeze

Seven of the nine new atoms remain false at F; D14 and D15 become true. The record files `SCORECARD.md`, `corpus/SOURCES.md`, and `corpus/README.md` are byte-identical between B and F. D3 and D6 also remain false because the ledger has no round-74 row and the scorecard has no round-74 section. Together this independently implies **9 mismatches at F**, not zero. The frozen predicate requires zero at the eventual landing, not at the freeze, so this does not refute that future predicate. It does prohibit treating the freeze as its passing landing.

There is **no committed round-74 landing audit receipt at F**. Tree enumeration finds only `pre/c2-at-base.json` and the base-world audit summary inside `pre/controls-at-declaration.json`. Both say 11 at B and agree with my base inspection. Therefore the requested comparison against two committed C2 receipts cannot honestly be described as a base/landing comparison. A later landing receipt and committed repaired bytes are required before recommending C2 verified.

## R74-C1: clause-by-clause

Receipts below are the blobs at F, not mutable working-tree reports.

| Clause | Verdict | Evidence |
|---|---|---|
| r73probe has exactly six survivors | Confirmed | `pre/c1-base-arm.json` has ten mutant rows: four `killed`, six `survived`; deriving the list from the rows exactly reproduces `survivors` and `survivor_count: 6`. |
| The six names equal round-73 MutProbe's names | Confirmed | Independently selecting `results[].verdict == "survived"` in `.ufo/waves/round-73/w1/MutProbe/results.json` yields the six names below, in the same order. |
| Base arm uses the landed round-73 target | Confirmed by bytes | Base receipt `tool` is `tools/round-73/seam-probe.py`, `target_sha256` is `9c286fd7187e25a8c6de5d743e21d0402ec6c9862a14aecfaed75b2006710939`; independent SHA256 of that blob at both B and F equals it. Receipt measurement revision is D, not B, but the target is unchanged. |
| r74probe survivor_count is zero over ten mutants | Confirmed | `pre/c1-post-at-declaration.json` contains ten rows, all `killed`; row-derived survivors and stored survivors are both empty; `killed_wrong_case` is empty. |
| Every kill contains its declared case | Confirmed | Every `expect_case` is present in its row's `failed`; full mapping below. |
| Pristine selftest has 20 green cases | Confirmed | Post receipt `pristine: {cases:20, failed:[], rc:0, stderr_tail:""}`; all mutant runs also report 20 cases. Base pristine is 14 cases, green, not 20. The 20-case requirement applies to the post arm. |
| Post target is pinned | Confirmed | `target_pin.expect == target_sha256 == 81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039`, `matched:true`, `pinned:true`; independent SHA256 of the r74 probe at D and F agrees. |
| Frozen battery is the receipt's runner | Confirmed | Both receipts bind `tools/round-74/probe-mutation.py` SHA256 `156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b`, matching its committed blob. |
| Battery exits zero | Supported by recorded data and canonical exit logic, not independently observed execution | Both receipts have `ok:true`; frozen battery `main` ends `return 0 if receipt["ok"] else 1` (`tools/round-74/probe-mutation.py:397`). The parent process exit code itself is not stored in these receipts. |

| Mutant | Base verdict | Post declared case | Post failed list |
|---|---|---|---|
| a-drop-forged-detected | killed | a12-kernel-cases | [a12-kernel-cases] |
| a-drop-lie-clean | killed | a12-kernel-cases | [a12-kernel-cases] |
| a-drop-genuine-canary | survived | a12-genuine-canary-only | [a12-genuine-canary-only] |
| a-drop-genuine-rc | killed | a12-kernel-cases | [a12-kernel-cases] |
| a-any-forged-sample | killed | a12-kernel-cases | [a12-kernel-cases] |
| b-unreadable-empty | survived | a12-proc-environ-unreadable | [a12-proc-environ-unreadable] |
| b-first-sample-only | survived | a12-kernel-multiple-samples | [a12-kernel-multiple-samples] |
| b-drop-canary-field | survived | a12-kernel-canary-field | [a12-kernel-multiple-samples, a12-kernel-canary-field] |
| c-swap-verdict-inputs | survived | a12-arm-wiring | [a12-arm-wiring] |
| c-skip-forged-subrun | survived | a12-arm-forged-executed | [a12-arm-forged-executed] |

The base receipt is explicitly **unpinned** (`expect:null, matched:null, pinned:false`); its target identity is independently recovered above. This is not a violation of the plan's command, which supplies the explicit pin on the post arm only. `expected.survivor_names` is null in both receipts, so the exact base-name clause is established by this review, not enforced by that invocation's name option.

Provenance nuance: the historical MutProbe receipt names source SHA256 `7264d0c861d5d0f5344a4009dba738579a10952d27a207dd0d8530cf434b48ed`, not the landed `9c286fd7…` target. That historical digest independently matches the r73 probe at `da6c17c1`. Thus the historical report was not measured on the final hardened r73 blob. The new base battery does establish the same six survivor names on the actual landed blob, so the frozen measurable predicate is supported; avoid saying the original historical measurement itself used the landed bytes.

## R74-C2: independent new-atom re-derivation

These observations use actual record blobs, not the audit receipt's evidence rows. All nine new atoms were checked, exceeding the six-atom minimum.

| Atom / clause | B | F | Independent bytes and comparison |
|---|---|---|---|
| D7b: ambiguous before arms selected explicitly | false | false | `SCORECARD.md:5740` names both `pre/c1-at-base-r72probe.json` and `pre/c1-at-base.json`; no `**Before-arm selection (round 74 correction)**` marker exists in the round-73 section. Agrees with base receipt. |
| D8: three r73 and two r74 capability rows | false | false | `SCORECARD.md` capabilities section begins at line 615; first-working-round cells end with three `round 72` entries, and contain zero round-73/74 entries. Agrees with base receipt. |
| D9: S275 used-by names the r73 entry | false | false | `corpus/SOURCES.md:192` last cell is exactly `corpus/knowledge/2026-11-04-r72-checker-env-capsule.md, .ufo/waves/round-72/w1/ScoutSource.md`. Missing the required r73 path. Agrees with base receipt. |
| D10: round-73 and round-74 search notes | false | false | `corpus/SOURCES.md:221` opens `## Search log`; its newest note at line 223 starts `- 2026-11-04 round 72`. Neither `round 73` nor `round 74` occurs in this section. Agrees with base receipt. |
| D11: four opened/rejected pages registered | false | false | Independently parsed registry rows whose status cell is `rejected`: title-cell matches for `proc.5.html`, `proc_cmdline.5.html`, `proc_pid.5.html`, and `index.html#_section_5` are each zero. Mere mentions in mined rows are not counted. Agrees with base receipt. |
| D12: 24-versus-23 W04 census erratum | false | false | No `## 2026-11-04 — round 74:` section exists in SCORECARD, so its required erratum cannot exist there. Agrees with base receipt. |
| D13: README ends with newline | false | false | Exact final eight bytes of `corpus/README.md` are `b'quality.'`; final byte is hex `2e`, not `0a`. Agrees with base receipt. |
| D14: before receipt binds runner bytes | false | true | At B, `.ufo/waves/round-74/pre/c1-base-arm.json` is absent. At F, its runner path and SHA256 are exactly the battery path/digest listed above; independently hashing the battery blob reproduces the digest. Base receipt correctly says false; its base verdict must not be reused for F. |
| D15: all freeze-container producer pins match freeze blobs | false | true | Claims container absent at B. First-addition history identifies F. At F, independent SHA256 comparison passes all five `instruments` and four `loaded_by_counter` entries, nine of nine. Base receipt correctly says false; F now differs. |

Independent identity evidence for unchanged records (SHA256 at both B and F):

- `SCORECARD.md`: `b7575e1a389be250c5199f7ee6c77915c0a9d39f73731e4f87ee1353faa26724` (599718 bytes).
- `corpus/SOURCES.md`: `e9f82ec4708e70d5a1efd772f6d846df2e100710d3e73761dbb01e40f3fcab99` (213714 bytes).
- `corpus/README.md`: `e983caff321fab6dd1c033803d2b247717db5115571eb5b935b5b87bcaddf0fc` (101323 bytes).

| Remaining C2 predicate clause | Verdict | Evidence |
|---|---|---|
| Base receipt has exactly eleven specified mismatches across sixteen atoms | Confirmed as receipt content; nine new atoms independently checked | `pre/c2-at-base.json` names D3, D6, D7b, D8–D15; 16 rows, eleven false. Its historical process exit is inferred from canonical `main` (`return 0 if receipt["ok"] else 1`), not newly executed. |
| Second committed audit observation agrees at base | Confirmed | `pre/controls-at-declaration.json`, arm `c2_do_nothing`, independently records the identical eleven-name list and count 11. This is another base observation, not a landing observation. |
| Landing has sixteen true atoms, mismatch_count zero | Not established at assigned freeze | No committed landing receipt exists at F; independently derived F state still has nine false atoms. |
| Landing receipt passes --validate | Not evaluated | No committed landing receipt at F to validate. No validator or primary instrument was run. |

## Instrument immutability

`git diff D F -- tools/round-74` emits zero bytes. All five declared instrument blobs therefore remain unchanged between the supplied declaration and freeze. Their independent SHA256s at F equal every `claims.json.instruments` value. The same verification also passes all four loaded producer pins. The historical first declaration was `541d574e`; the assignment explicitly designates the revised declaration D, and this comparison uses D.

## Residual risks and verification gaps

- R74-C1 is supported by committed receipt data and target/runner identity, not a new execution. R74-C2 requires later committed repairs and a passing landing receipt; this review intentionally does not inspect a moving working tree or claim admission.
- Static predicate-strength caveats: D7b's implementation checks path mentions after a marker, not semantic role assignment; D10 checks round tokens and `Identified`, not all promised counts; D11 checks rejected status/title matches, not actual reason/flip content. These do not contradict the currently false record rows, but independently inspecting repaired prose remains important even if a future audit is green.
- `xd://lsp` is unavailable (`No such tool`); no semantic server, references, definitions, or diagnostics were available. This is a committed-data review; textual/byte evidence is not presented as semantic caller proof. Resume continuity, runtime rerouting, and saturation were not changed by the assigned frozen-data comparison.
- No tools installed or updated. No fixture repositories, runtime launches, git writes, raw environment dumps, or edits to production files. Only this report is written. Scratch is removed before handoff.

Self-evaluation: accuracy 4 (historical process exits not independently observed); completeness 4 (landing receipt absent at F, explicitly distinguished from two base observations); clarity 4 (detailed matrices are longer than the final summary); actionability 5 (exact unrepaired paths and atom states provided); conciseness 4 (all nine atoms retained for independent coverage). Overall 4.2. Would the user agree? The requested scope is covered without silently converting a future landing promise into a freeze success.
