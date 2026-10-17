## CLAIM
README:163 lists process-capture, managed `verify`/`project` ops, and native call-target resolution as frontier; all three are held in the same file (:125, :53, :47) and their census queue is drained. Final replacement text drafted below; no tracked-file write (seat-only).

## METHOD
`git show HEAD:cfc84c2` (worktree clean vs HEAD for corpus/README.md); read :163 plus :47, :53, :125 and the rows they summarize (r5-02, r9-02, r11-01), the driving census + errata (r4-16:144-206, 860-925), ledgers r12-02/r14-01, r10-02:33; ran Command A on HEAD.

## FINDINGS
- Command A @cfc84c2: mapped 72/72, knowledge_files 72, missing/dangling `[]`, citations 9/9, depth 10.0 — baseline intact. Frontier is outside the `## Coverage map` token scan; edit simulated → token set identical (72).
- The three items are held: call-target resolution r5-02:53-70 (3/3 probed jq sites, one EXTERNAL thunk each); managed verify/project r9-02:50-57,106-124,240-244; process-capture pair r11-01:185-217,228-270. Queue A drained: r4-16:913-915, r11-01:375 — so the "(per r4-16 rescan: ~26 self-provisionable)" driver is spent.
- Genuine residual: r5-02:152-155,193-194 (283/286 cataloged GOT-indirect sites unprobed, both `jmp *` untested; "resolved" names an EXTERNAL import, not a body, r5-02:85-98); r9-02:82-84 (managed `inferred` variant never observed — :53 already records this); r12-02:65 (managed↔managed compares all-`unknown`, 4,114 items / 0 paired). Device/operator sets already have bullets (:161, :164); `capture-electron-scenario` keeps its own (:159).
- Replacement text (recommended): `- Runtime-obs extended — call-target resolution, managed `verify`/`project`, and the process-capture pair are held, not frontier (r5-02, r9-02, r11-01); the census's Queue A is drained (r4-16 erratum :913-915), so the "~26 self-provisionable" driver is spent. Residual depth only: 283 of 286 cataloged jq GOT-indirect sites unprobed (2 `jmp *` untested, r5-02:152-155); managed `inferred` variant has no observed example (r9-02:82-84); managed↔managed compare grades all-`unknown` (r12-02:65).`
- Terse fallback: `- Runtime-obs extended — held, not frontier: call-target resolution (r5-02), managed `verify`/`project` (r9-02), process-capture pair (r11-01); Queue A drained (r4-16 erratum :913-915). Residual: unprobed jq call sites + jump targets (r5-02:152-155), managed `inferred` variant (r9-02:82-84).`

## THREATS
Line numbers drift (locate by quoted text). PB0 item 6's 281-calls/2-jmp split is not yet corpus text, so the draft cites only r5-02's own counts. PB0 item 4b (:131 "4 nits fixed") is outside this seat. Textual reconciliation; no artifacts replayed.

## VERDICT
FINDING: README:163 stale — three held families listed as frontier; replacement text drafted above (no tracked-file write).
