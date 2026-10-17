## CLAIM
Adjudicate r5-02's "~283" (PB0 item 6). From the file's own counts: remaining scope is 281 calls + 2 jmp (= 283 GOT-indirect sites). ":152-153's remaining ~283 call sites" is not a call count. Disposition: append-only erratum; exact append below.

## METHOD
Static read at HEAD cfc84c2 of `corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md` (sha256 `7387e01cc9cde9f06df0e9c1370d348d83b0d45667181ba77de3848c34138689`, 194 lines; identical to `git show HEAD:` — tracked file untouched). Counted from :18-19, :53-70, :152-155, :163-165, :173, :194; cross-checked harness `.ufo/waves/luna-round-5/receipts/census-pre.txt:44-45`. No live probes; /tmp scratch gone — no artifact-level recount possible.

## FINDINGS
1. Census :18 (restated :173): 286 GOT-indirect sites = 284 call + 2 jmp; 284+2=286, consistent.
2. Probed call sites = 3 (:63-70: 0x1020a3→jq_init, 0x10207b→jv_array, 0x10206a→setlocale; run log :163-165). Row 7 (:167) probed 0x102020, non-call (main entry, not one of the 286) — nothing further to subtract.
3. Remaining calls = 284 − 3 = **281**; remaining jmp = 2 (:154-155 "not-probed"; :194 "untested residue"). 281 + 2 = 283 = 286 − 3 = remaining sites.
4. So "~283" is the remaining-site total mislabeled "call sites"; no reading makes 283 a call count (remaining 281; total 284). Tilde unjustified — counts are exact `grep -cE`.
5. Harness gate `census-pre.txt:44-45` (tail needs '283', `281 calls|281 call sites`, `2|two jumps`, `unprobed|untested`): block below complies.

Proposed exact append (at EOF after :194's trailing newline; prior bytes untouched):

```text
## Erratum — luna-round-5 (2026-10-16, append-only)

From this file's own counts: census :18 (284 call + 2 jmp = 286 GOT-indirect
sites) minus the three call sites probed at :63-70 (0x1020a3, 0x10207b,
0x10206a) leaves **281 calls + 2 jmp** = 283 GOT-indirect sites. So :152-153's
"the remaining ~283 call sites" mislabels: 283 is the remaining site total,
not a call count. Remaining call sites are 281; the 2 jumps (:154-155) were
not probed — unprobed, and not sweepable by the call-reference-scoped two-arg
form. Read :152-153 as "the remaining 281 calls".
```

## THREATS
Recount impossible (/tmp gone): the 286/284/2 census is taken on trust from :18 — erratum only as sound as that census (sum-consistent). Harness regex needs literal "jumps" (not "jmp") plus unprobed/untested — block complies. Lane-A reports unopened (independence kept).

## VERDICT
FINDING: r5-02:152-153 "the remaining ~283 call sites" mislabels 283 (remaining sites = 281 call + 2 jmp) as a call count; append-only erratum block above is the disposition.
