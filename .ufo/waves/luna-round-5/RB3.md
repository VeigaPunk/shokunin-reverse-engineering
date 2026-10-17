## CLAIM
Fidelity sweep of debt items 5-7: r9-02 four-status tension; r5-02 "~283" wording; r12-01 L197 main-vs-erratum. All three real, anchors exact at HEAD cfc84c2; item-6's census independently re-verified on the pinned binary; drafted errata faithful; integration gate gaps and stale echoes pinned.

## METHOD
Primaries first (no probes). Line-pinned `git show HEAD:` reads; `objdump -d /usr/bin/jq` recount (sha e8156675…7806 == pin) → 284 `call *0x…(%rip)` + 2 `jmp` = 286; pins: sha1 a5f2f7d…, sha256 7387e01…, tail-12 cc9beb31…, r9-02 0e602155…; C4:10-19 / X1:7-49 token checks simulated on DB5/DB6; dist spot-check (`FirmwarePublication.js:46,59`, `FirmwareReports.js:157,198`, unblob `identifiers.py:17`). Lane seats read only after the primary pass.

## FINDINGS
Item 5 — real, exact: overclaims :7-8/:215-216/:326 vs :82-84 `inferred:0`; 3 of 4 variants evidenced (runs 8-13); `inferred` strings :53/:83/:206/:244/:345 (:345 summary shorthand, not an envelope label). V5/D5/DB5 drafts faithful ("three of four", "does not establish"). Gap: DB5 as filed lacks C4 tokens 'single queued-pairing', 'across separate runs', and contiguous '0 verified'/'0 inferred'/'39 unresolved'/'0 contradicted' (:83's `{verified:0,…}` field order cannot satisfy them); heading must be top-level `## Errata (round 5 freshness…`. README:122 + LOG:286-289 stale echoes remain unowned by any item.

Item 6 — real, exact: :153 sole "283"; 284−3=281 calls + 2 jmp = 283 sites; census re-derives from the pinned binary, so the fix need not rest on deleted scratch. DB6 pins verified (a5f2f7d…/7387e01…/194 lines/12634 B). DB6 passes X1's regex but fails C4's tokens (only '2 jmp' present) → dual-phrase wording needed. Confirmed prior flags: R2:9 cites V2.md (firmware seat) not V10a; SB2:20 truncates the last-line quote.

Item 7 — real but pre-corrected: two-value account :13/:38/:40/:42 (weaker :67) vs erratum :99-104 ("two classes across FOUR sites — 7 values"); four sites spot-verified in pinned dist. "7 values" unre-derivable (envelopes gone) — keep attributed. C4/X1 gates presuppose an r12-01 append ('supersedes main text','FOUR sites','7 values'), so D7's no-append verdict self-fails the census; parent decision. P0:16's "four variance classes" and C5:11's "four classes" misstate the erratum; rescan :750-754 still carries the two-value account.

## THREATS
Text-only; /tmp receipts gone (probe outputs and held==lane byte-diffs unverifiable); gates lexical, not semantic; anchors valid at cfc84c2 only; not every wave file read.

## VERDICT
FINDING: debts 5-7 and anchors hold (census re-verified on the pinned binary); land items 5/6 with gate-compatible wording, settle item 7's append vs gates, keep "7 values" attributed.
