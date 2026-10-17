# DB6 — r5-02 erratum draft (2nd opinion, from VB6.md)

## CLAIM
Debt item (6) confirmed from primary sources and matches VB6.md: `corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md:153` ("sweeping the remaining ~283 call sites") labels the unprobed aggregate as call sites. Draft erratum below restates 281 call sites + 2 jumps unprobed — 283 GOT-indirect sites total.

## METHOD
Read VB6.md (wave input) plus its cited primary source at pinned HEAD cfc84c2 (`git show HEAD:corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md`, `nl -ba` excerpts :17-20, :55-71, :150-156, :192-194). Verified: working tree == HEAD blob (`git hash-object` == `git rev-parse HEAD:...` = a5f2f7d…); only "283" at :153; EOF-append citation safety (SKILL.md cites :25-51, :36-41, :55-57, :144-146 — preserved); census predicate (`receipts/census-pre.sh:30-31`) simulated in-memory on HEAD-blob + draft. No Lane A outputs; no tracked writes; no REA/MCP/network. VB6.md arrived mid-pass; reconciled after an independent derivation — no divergence.

## FINDINGS
1. Counts match VB6.md: 284−3 = 281 remaining calls (not ~283); 286−3 = 283 = 281 + the 2 unprobed jmp sites; the "~" is unnecessary.
2. Draft — append verbatim after current EOF (byte-prefix preserved; corpus errata heading convention):
```
## Errata (luna-round-5, 2026-10-16, append-only)

- `:152-155` ("sweeping the remaining ~283 call sites"): the counts recorded
  in this entry (`:18-19`: 286 GOT-indirect sites = 284 call + 2 jmp;
  `:53-70`: three probed call sites) imply **281 call sites and 2 jumps
  remain unprobed — 283 GOT-indirect sites in total**. 283 is the aggregate
  residual (286 - 3); it is not the remaining call count (284 - 3 = 281) -
  the 2 unprobed `jmp *0x…(%rip)` sites are exactly the difference.
  Restated from the recorded counts (no recount run); probe results and the
  untested-jump caveat stand unchanged.
```
3. Simulation passes: appended tail contains '283', '281 call sites', '2 jumps', 'unprobed'; simulated HEAD-blob sha256 == SB2.md's pin (7387e01…) — basis matches the wave baseline.
4. Optional: VB6 flags :59-60 ("Three call sites inside main") as better read "the three probed sites" — local recount only; parent may add/drop.

## THREATS
- VB6's :53-70 output half rests on deleted /tmp scratch; offline-unverifiable — accepted as recorded, unchanged here.
- Counts derive from the entry's own census, not a fresh recount (binary outside git; probes banned here); the optional clause would rest on unreproducible evidence — recommend omission.

## VERDICT
FINDING: r5-02:153 counts the aggregate residual as "call sites" — append-only erratum drafted (281 calls + 2 jumps unprobed; 283 sites total); census-matcher-simulated, byte-prefix safe.
