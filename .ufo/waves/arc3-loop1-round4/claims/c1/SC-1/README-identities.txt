# SC-1 artifact identities — arc3-loop1-round4, c1 scribe

Re-derived by this seat after its final writes (rule #14), 2026-10-19T14:28Z —
**revision 3**, after RV-2's grade (ACCEPT-WITH-FIXES) required six changes and CR-1's report added two scope notes:
F1 (the inventory citation path), F2 (the EX-09 `0xhex` brace over-claim),
F3 (the same-path-determinism wording), F4 (the QUALITY row-15 citation),
A1 (the id-domain sentence ordering), A2 (the ledger's stale
`custody-stat-readonly.txt` pin) — plus **revision 3**, which scopes two
citations on CR-1's report: EX-08's reconciler is Form-A-only (0/8 on the
`--no-optimize` and `-O codesize` forms while the probe recovers 8/8), and the
comparison discipline is stated as set-equality (CR-1's count-only trap: a
tampered carrier keeps n = K while its set changes). Revision-1 and revision-2
hashes are superseded and are not quoted here; the cross-check below records
which snapshot matched which revision.
All hashes `sha256sum`, recomputed — not transcribed. HEAD at all reads:
`015e1bab914713568f339fd53999bc180459cc40`.

| artifact | bytes | sha256 (rev 2) |
|---|---|---|
| `records-drafts/chain-ledger.draft.md` | 19,986 | `7e2d56a6198d5dc3911d1bc254cfbd3d1962cb2bc52c98e92e0841c6d8d0fc1e` |
| `records-drafts/knowledge-entry-draft.md` | 23,325 | `cf24559c5f0425e44a9b3a29ba4e5496db7acc4b4965ca9fd2a55f054d36f15a` |
| `records-drafts/map-token-patch.md` | 7,416 | `aa6b1ad61660ae8a9eda11b392bb7055678f3e967fbcf579e5b9927bdd80f16b` |
| `records-drafts/records-drafts.md` | 17,054 | `a93ed42de147cc82cc123a54345b78bc336d95213b6d9d6d5b7dc5706a52cd97` |
| `SC-1/c1-inventory.txt` (tree snapshot, 78 rows) | 7,848 | `1cdeb1f7a1a6c4a0e2c7d8fd7e41693ad68b48fb698b384c705e3ca93f80180c` |
| `seats/SC-1.md` (this seat's report) | 18,272 | `435c429607196af2b986afe7e71d437a50624788abe65c2813a7505d0ddaf7f3` |

## Literal blocks (what the parent lands)

| block | lines | bytes | sha256 (rev 2) |
|---|---|---|---|
| entry literal (between the entry draft's BEGIN/END markers) | 32 | 20,325 | `17320917e6b39b2518e308b2659aa628ac8da69bf1f0faef2a9664d569383f6e` |
| records literal (between the records draft's BEGIN/END markers) | 178 | 13,269 | `1bcf2306688f59e38b38444fbc713970393b89b26071c7e8f1f74ebead37bd01` |

## This seat's own evidence (first-hand runs)

| artifact | bytes | sha256 |
|---|---|---|
| `SC-1/evidence/command-A-before.json` | 220 | `2155c2d48bc4aaa0a41c377e0365bef7a007c82eb927e82edae248d1b734c379` |
| `SC-1/evidence/probe-carrierv-hex-6.4.0.json` | 10,701 | `68415a3de767d58ee176bf6bfdd1ffb1719173041997a5d3fa49ce6f614a99ec` |
| `SC-1/evidence/probe-carrierv-raw-6.4.0.json` | 10,701 | `e5b8f0eb8e08b629ef8417948c911cda70bab6cb6703b01bf602dbc5b36c5b73` |
| `SC-1/evidence/probe-carrierv-hex-6.7.0.json` | 11,442 | `0d7171ed8a0ea0beca90fb3d32c54ac20a9bfbf1f7b89ce275999fe3a1ea7c75` |
| `SC-1/evidence/probe-smoke-hex-6.4.0.json` | 5,249 | `5b2dab53117ed4371d514c0dff9407ca10588eaf15e9056dbe451e8974428245` |
| `SC-1/evidence/probe-carrierv-creation-6.4.0.json` | 7,246 | `0da3f5cd235699cc99e5634bb723ae6d9529a3086ae36ed935f54d67276721a1` |

## Cross-checks (not self-claims; the other party's value quoted)

- **VZ-1's snapshots match revision 1, not revision 2.** VZ-1 captured
  `claims/c1/VZ-1/evidence/entry-draft-snapshot.md` `df9582ac…` and
  `…/map-token-patch-snapshot.md` `8e3f91e3…` at 14:10:48Z (the token patch
  was later corrected to rev 2 — the rehearsal table now quotes the rev-2
  entry hash — so its snapshot is also superseded). At that moment the
  entry draft was byte-identical to its rev-1 form and the token patch was
  already final; **RV-2's grade then required six changes, and the entry draft
  and ledger were revised to rev 2 (14:28Z), so the entry snapshot is now
  stale by construction** (`cmp` exit 1 on the entry draft, exit 0 on the token
  patch). The rev-1 snapshot's value as evidence is that it **proves the rev-1
  text was what VZ-1 re-derived K/K against** — it is not a claim about rev 2.
  The parent must re-derive rev 2's identity at landing; this seat's rev-2
  rows above are the current ones.
- **CN-2's merge fold** (`claims/cross/CN-2/merged-SCORECARD-section.md`
  `f3cea8d0…`, `merged-LOG-entry.md` `0621d660…`, folded 14:11:26Z) carries this
  seat's C1 bullet and C1 axis row **as of rev 1 of `records-drafts.md`** — that
  file was not revised (its hash is unchanged), so the fold remains faithful.
  Its projection of the merged section reads census **PASS 0/0/0/0** with a
  planted-pin control FAILing `undeclared=1`.
- **RV-2's baseline pins** (`claims/c1/RV-2/evidence/baseline-pins.txt`) quote the
  same README sha256 this seat measured: `a451ad16…`.
- **RV-2's grade is the authority on the fixes**: `claims/c1/RV-2/quality-grade.md`
  — hard gates all PASS, verdict ACCEPT-WITH-FIXES, and the fixes above are this
  seat's application of them. The parent should re-grade rev 2 against the same
  gate list rather than trusting this seat's own application.
- **Command A before-state** agrees across three seats: this seat
  (`2155c2d4…`), RV-2 (`evidence/commandA-before.txt`), VZ-1
  (`evidence/baseline-commandA.json`).

## Pin-free check (this seat's own run)

`python3 claims/cross/CN-2/pin-free-check.py <file>`:

| file | verdict |
|---|---|
| `records-drafts/records-drafts.md` (the census-scanned side) | **CLEAN** — 0 pin/version/pointer tokens |
| `records-drafts/map-token-patch.md` | **CLEAN** — 0 tokens |
| `records-drafts/chain-ledger.draft.md` | 40 locus tokens — **not a landing surface** (a ledger must quote the exact reproducing calls; the r3 predecessor ledger reads the same way) |
| `records-drafts/knowledge-entry-draft.md` | 47 locus tokens — **not a landing surface** (`corpus/knowledge/` is outside the census's declared scope; QUALITY #6 requires the entry's `recheck:` line to carry the exact reproducing call, and the r1/r3 landed entries carry that same form) |

## Census projection (this seat's own run)

| tree | SCORECARD lines | verdict | exit |
|---|---|---|---|
| `base` (HEAD files) | 1580 | PASS 0/0/0/0 | 0 |
| `merged` (+ this seat's 178-line records literal) | 1759 | **PASS 0/0/0/0** | 0 |
| `control` (+ one planted pin literal) | 1761 | FAIL `undeclared=1` | 1 |

The drafted section adds **zero loci** and the detector is live on the same
appended region — the pin-free property is measured, not asserted.
