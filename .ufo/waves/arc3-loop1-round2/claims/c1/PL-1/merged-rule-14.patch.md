# Merged rule #14 payload — EX-01's text + two ranked deltas (PATCH TEXT, NOT APPLIED)

Seat PL-1 (planner, chain c1), wave `arc3-loop1-round2`, 2026-10-19. **Variant**,
not the chain's candidate: this is EX-01's peer-measured payload
(`claims/c1/EX-01/rule14.patch.md`, payload sha256 `6cc388cb…`) with the two
deltas plan §11 ranks highest, nothing else changed. Land it **only** if the
chain accepts the deltas; otherwise land EX-01's payload unmodified and re-derive
the numbers below from the bytes that actually land.

## Deltas vs EX-01's payload

1. **Rule-#11-form citations**: `SCORECARD.md:1366-1368` / `LOG.md:1411-1412` →
   `SCORECARD.md`'s `arc3-loop1-round1` section / `LOG.md`'s arc3-round-1 entry
   (section/entry keys; no instrument grades these refs — probe 0 findings either
   way — so this is fidelity, per rule #11's own discipline).
2. **Laundering closure + cost**: appends "Re-deriving costs one `wc -c -l` +
   `sha256sum`, and deleting the identity claim does not discharge the rule."
   (the only anchor CR-1's "norm with no instrument" objection can be answered
   with).

Not merged: this seat's cross-file clause (redundant with EX-01's "claim binds
the bytes it describes").

## Payload (verbatim; block sha256 `5a235f18b6ae9a74807752fe6e2cb3e5afee6376da246ae9b4dc45276bea4a55`)

```
- **An artifact that records its own byte-identity must re-derive its
  identity after every revision; a stale self-identity voids the verification
  block, not the work.** Size/hash/line-count claims bind the bytes they
  describe, not an earlier revision of the same patch: after the C1 entry
  patch was revised, its step-4 claim still read 8,316 B / `f95c5a05…` while
  the applied bytes hashed 8,598 B / `d8d85949…`
  (`.ufo/waves/arc3-loop1-round1/seats/CR-2.md:86-89`), and the chain measured
  three applied identities inside ~20 minutes, the fix being the fresh landing
  hash (`.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md:149-153`). The
  voided block is re-established by re-running its checks against the current
  bytes; the integrator records the fresh identity of the landed revision —
  10,225 B / `dd986f56…` for the landed entry
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:7`, whose recheck line
  records the mid-wave revision (`SCORECARD.md`'s `arc3-loop1-round1` section;
  `LOG.md`'s arc3-round-1 entry) — never a revert, never a carried-over
  number. Re-deriving costs one `wc -c -l` + `sha256sum`, and deleting the
  identity claim does not discharge the rule.
```

Machine copy: `merged-rule-14-block.txt` (1,320 B / 20 lines / sha256
`05bbdbfb9a087d56344a15f7c16cc73110aa60a522fea353f1d874315c4adfd3`).

## Apply recipe

Insert the block plus one blank line immediately after the unique line
containing ``kernel-OOM-killed (` `` ``corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37` `` ``).``
— i.e. after `SKILL.md:239` at HEAD `14b1682` (the base blob is unchanged from
EX-01's pre-image: 371 lines / `483b0eba…`).

## Measured (PL-1, scratch `/var/tmp/pl1r7/repo-merged2`; full battery re-run)

| Check | Result |
|---|---|
| patched `SKILL.md` | 392 lines / 28,711 B / sha256 `0cf18464787cf0dbfe227c776e9062e948244dfc148f6e557980aefaa243d1b7` |
| command A | `rule_blocks 14`, `citation_resolved_rules 14`, 82/82, 10.0/10.0, missing/dangling [] |
| prior rules | prefix 1–239 byte-identical; pure insertion (0 deletions, same contract as plan §4) |
| rule #14 geometry | `:240-259`; next heading `:263` → **SHONEN end = 259** for this variant |
| citation-drift probe | `reported findings=0 exit=0` |
| census (instrument sha `d0772ce892223690…` at read) | `PASS 0/0/0/0`, `SKILL.md lines=392 loci=2` |
| needle classes in the block | 0 `rea-agents@`, 0 `x.y.z`, 0 `json:N`, 0 operator-path line refs, 0 mutable-file bare line refs |
| rule block identity | 1,319 B / 20 lines / sha256 `5a235f18b6ae9a74807752fe6e2cb3e5afee6376da246ae9b4dc45276bea4a55` |

## Landing obligations (either variant)

1. Re-derive the anchor and the geometry at the wave's HEAD before applying; the
   SHONEN end is the rule's last line for the payload that lands (259 here; 254
   for EX-01's payload; 252 belongs to EX-04's 385-line variant, which is *not*
   EX-01's payload — plan §11).
2. Land the `SHONEN.md:6` refresh in the same commit (`13/13` → `14/14`, range
   end as above).
3. Re-run command A at the work commit (expect 14/14) and record the fresh
   `SKILL.md` identity + the census reading **with the instrument's sha256 at
   read time** — the census moved three times during this session
   (`df9ffdf9…` → `a4c16763…` → `d0772ce8…`).
4. No pointer-table, `expected.json`, or census-scope change is required; do not
   widen any of them (r4 laundering precedent).
