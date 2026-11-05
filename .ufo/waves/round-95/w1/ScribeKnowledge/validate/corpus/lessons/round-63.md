# Round 63 — the receipt corpus's edge half becomes enumerable: the edge-numstat sweep audits every receipt with the frozen r61 gate

Lane kaidoku, round 63, fresh-start binding honored (r50/r51/r52 re-read and
spot-checked with fresh probes; seven ruled-out items receipted), L1-inline
on the Windows host (2026-11-02). Round base
`4ce1d64ed62f4dff42ceab43aba085ad0fc1fed7` (the r62 verifier spot-check
commit, which verified R62-C1 improved with NO routed defects); carry-in
`0fadbd062088590d2f8a695efc26ccbba49d72d4` (the r62 outside decision
recorded per QUALITY #34 BEFORE any claim was measured; the carried items
restated: 19 standing W04, the r53 L0 open and routed around, the two
standing bare-name findings, the host adaptations; the two cosmetic wording
nits acknowledged at receipt level); declaration
`feebe7b9a350e5f0feecc98305ab5166537c6710` (the plans + the new
instrument, the QUALITY #33 order); operative freeze
`fbc0f95034cd6b371cab8189b3b351415945524c` (the first commit adding
`.ufo/waves/round-63/claims.json`); landing
`c77c5392b6954d66bab3690289988ea9b2ba4fa5` (the SKILL row + the
capability row; the seven-cell recount covers both the new row and the
r62 neighbor — M60-1/M61-2 applied). No wave (no dispatch surface on this
host; the kaidoku round-53 L0 question stays open and unanswered). Nine
frozen instruments (eight unchanged, one new:
`tools/round-63/edge-numstat-sweep.py`, pin `0e67bd45…`), which COMPOSES
the frozen `tools/round-61/numstat-edge-audit.py` (pin `6b967e20…`,
byte-checked via `--expect-sha256` before any enumeration) instead of
duplicating it — and never passes `--name` fleet-wide, so every per-receipt
binding is the receipt's OWN. The claim is offline over committed bytes.

## Gate

| row | URL / path / command and access | located quote (at most 25 words) | decision and limits |
|---|---|---|---|
| S263 | https://docs.python.org/3/library/hashlib.html — fetched read-only with curl 2026-11-02 into the round scratch, snapshot bytes and sha256 committed at `.ufo/waves/round-63/l1/s263/` (hashlib.html `d0b45c7e32268e992981b4b05a1a2205aedfe90d961e376fda4f55c51fe47339`, 121928 bytes) | "This module implements a common interface to many different hash algorithms." (11 words; locator: the h1 module heading `hashlib — Secure hashes and message digests`, the nearest preceding h1–h6 before the intro paragraph, verified programmatically against the snapshot; **plain** — contiguous in one `<p>` after whitespace normalization, no tag crossing, not composite) | admit, tier A docs (official Python standard-library documentation — the category is the authority for the `hashlib.sha256` constructor the sweep's `--expect-sha256` pin check and every claims-container instruments map are computed with); mined: the pin is a content digest of the checker's exact bytes, not a name — "never audit with unpinned checker bytes" is mechanically enforceable because the digest is recomputable from the bytes alone. Used by `plans/round-63-claims.md`, `tools/round-63/edge-numstat-sweep.py`, this lesson. |
| R63 reject 1 | re-implementing the edge-claim grammar inside the sweep instead of composing the frozen r61 gate | reject — the r60 rule (named again by the r62 planned field): threading the frozen gate's semantics "needs the frozen single-receipt gate's option threaded through a new instrument and its own freeze"; the gate is frozen at `6b967e20…`; the sweep composes it (one argv subprocess per receipt, `--expect-sha256` pin check, exit 2 on pin mismatch before any enumeration) so the per-receipt semantics stay byte-identical to the r61 recorded runs | reject row |
| R63 reject 2 | passing caller `--name` overrides fleet-wide so more receipts' claims resolve | reject — that would import caller context into what the lane records as receipt-own state; the r61 before-arm's quote-prose resolves at DEMO time with recorded caller-supplied overrides (the gate JSON marks them `caller_supplied_names`), never in the fleet sweep; the fail-closed NUMSTAT_NAME_UNRESOLVED on every fleet run is the honest persistent state, dispositioned, never waived | reject row |
| R63 reject 3 | reading receipt bytes in the sweep to compute the inventory (the r62 mirror pattern) | reject — stricter rule adopted instead: the sweep NEVER reads receipt bytes; every inventory number comes from the gate's own JSON bodies (claims_found, bindings_used, findings, exit_reason), so there is no mirror that could drift; the only sweep-side checks are the enumeration predicate and the body-vs-enum-path consistency check (a body naming another receipt is an invocation error, fail-closed) | reject row |
| census receipts | the host-adapted census command (explicit ABSOLUTE lane dir) at round start and at the filing tip; start receipt `.ufo/waves/round-63/l1/scores/census-start.txt` (exit 0, 19 standing W04, 169 rows; the literal form exits 2 as disclosed since r53) | 19 standing W04 warnings; exit recorded in the receipt | host-adapted form (the `kaidoku-shokunin` mapped directory does not exist here; the lane arg is cwd-relative — M63-1); W04 stays debt |
| do-nothing control | `.ufo/waves/round-63/l1/scores/c1-before.txt` (instrument absent rc=128 at the base; 0 SKILL rows; 0 SCORECARD rows; 0 `records/edgesweep-` receipts; the r62 inventory's no-edge-fields behavior probe 0; the r61 demos' no-inventory probe 0 — the composed gate was present but only ever hand-aimed) | the arm is red at the base, committed at the operative freeze | measured pre-data; a do-nothing control cannot produce the instrument, the first corpus-wide inventory, the registration, or the binding statistics |

Assimilation: none — `considerthese/` does not exist in this lane (measured
at round start); the shokuknow register is unreachable from this host; the
report carries `Assimilation: none — shokuknow unreachable`.

## Mistakes

| id | class | evidence pointer | captured-by | fix / demonstrated limit |
|---|---|---|---|---|
| M63-1 | an argument form that passes only when the caller's cwd happens to make it resolve — the census script's lane argument is cwd-relative on this host, and the first host-adapted census attempt with the RELATIVE arg `fleet/shokunin-reverse-engineering` failed `ERROR: unknown lane (not a dir, not in conf or root)` because the caller's cwd was the lane repo; the same arg had exited 0 earlier from a different cwd | the first attempt's stderr, preserved in this lesson's history and in `scores/census-start.txt`'s form-correction note (the failed form is recorded as a form correction, never as a census result); captured BEFORE any census receipt landed | this round's L1, re-running the census at the freeze assembly step | the receipt records the ABSOLUTE-dir form (exit 0, 19 W04, 169 rows); rule: a relative lane arg is not a form — paste the absolute directory and re-run before recording; a green run from a lucky cwd proves nothing about the form |
| M63-2 | a path written from memory into a drafted receipt where the tree disagrees — the drafted duty-dispositions receipt named the genuine `freeze-gate-tip-90f3a9b9.json` copies as round-55/round-56 scores; the tree-wide `git ls-tree -r --name-only HEAD | grep` says round-54/round-55 | the drafted receipt's wrong sentence vs the tree (the `git ls-tree` count 2 with both true paths printed, re-run this round and pasted in `records/duty-finding-dispositions.txt`); caught BEFORE any commit of the affected bytes (the M60-2 rule: no placeholder, every path re-derived) | this round's L1, on the pre-landing re-read of the drafted receipt (the M62-3 rule: re-read receipt bytes before commit) | the landed receipt names the two true paths with the re-derivation command and its count; rule: a memory-written path in a receipt is a defect until the tree is asked; `ls-tree` is the ask |

## Claim disposition (filled at the record commit)

C1 (depth, capability acquisition): before all open at the base
(`scores/c1-before.txt` — the instrument absent rc=128; 0 rows; 0
receipts; the behavior probes 0; the composed gate present but only ever
hand-aimed), after the instrument is registered (SKILL row 7 cells
pipe-free with the neighbor recounted, capability row, container pin
`0e67bd45…`), the demonstrations stand: selftest 53/0
(`records/edgesweep-selftest.txt`); the FIRST corpus-wide numstat-edge
inventory at the base — red exit 1 with no dispositions, 258 receipts,
0 invocation errors, 3 receipts with edge claims / 7 claim instances, 2
receipts binding all edge endpoints from receipt-own bytes, 1 receipt
with unresolvable quote-prose names, 255 receipts without edge claims, 4
findings (1 NUMSTAT_EDGE_MISMATCH — the standing D60-1 — and 3
NUMSTAT_NAME_UNRESOLVED — the r61 before-arm's quote-prose)
(`records/edgesweep-inventory-red.txt`); green exit 0 with the r63
disposition TSV — inventory complete; 4 finding(s) all dispositioned,
NEVER defects erased (`records/edgesweep-green-and-only.txt`); the
`--only` arm over the three claim-bearing receipts — same 4 keys, the
r61 recorded classes; the pin fail-closed arm — a wrong `--expect-sha256`
exits 2 before any enumeration (`records/edgesweep-pin-mismatch.txt`).
The duties ran to dispositions: the TEN-container receipt-audit sweep
(EIGHT clean — the r62 container clean on first entry — plus the TWO
standing bare-name findings, dispositioned before the landing, no copy
planted, the sixth refusal), the record-audit over the r62 record section
(clean), and the two-direction orphan census (5 worktree-only with the
ordering note + 4 in-progress wave files + the 50-path aux/ class).
census3 `--generate` 68 paths at the landing rev, `--check` at the record
rev. The standing halfway sweep re-runs at the record rev with the close.
Verdicts in SCORECARD's round-63 section and LOG.

## Freeze

Operative freeze: `fbc0f95034cd6b371cab8189b3b351415945524c` — the first
commit adding `.ufo/waves/round-63/claims.json`. No amendments to the
operative freeze. The frozen instruments and pins:
`tools/round-63/edge-numstat-sweep.py` `0e67bd45…` (new, committed at the
declaration `feebe7b9…` before the claims file),
`tools/round-61/numstat-edge-audit.py` `6b967e20…`,
`tools/round-60/annotation-sweep.py` `38614088…`,
`tools/round-59/annotation-audit.py` `ba9ccbb9…`,
`tools/round-56/receipt-audit.py` `897df532…`,
`tools/round-57/record-receipt-audit.py` `3a5fff9a…`,
`tools/round-51/census3.py` `a7538e5f…`,
`tools/round-29/freeze-gate.py` `25b54339…`,
`tools/round-55/v6-block-digest.py` `22785c1e…` — bytes unchanged from the
claims commit through the tip. Disclosed shape note: the freeze gate
extracts instruments by path-naming from the container strings, which name
exactly one script path (the new sweep); the instruments MAP pins all nine;
the pin check covers every named instrument and the verdict is CLEAN
(pre-flight rc 0 at the freeze, audited 38, clean 18, round-63 CLEAN,
`required_failed []`).
