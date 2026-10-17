# PB2 — records drafts: luna-round-8 LOG + SCORECARD (operability)

## CLAIM
Draft the luna-round-8 LOG entry and SCORECARD section for the 6.4.0
operability symmetry battery, including the 78→79 denominator consequence if
the consolidated knowledge entry lands. Read-only elsewhere; only this file
written.

## METHOD
Read-only at HEAD `6e2ee8f`. Re-hashed all ten canonical receipts and
`leg-2-tools.txt` against `receipts/MANIFEST.txt`; re-extracted and hashed the
fenced stdout blocks of `leg-3.md`/`leg-10.md` (LF-terminated) in Python and
matched `/tmp` raw captures; read `census-pre.txt`, `P0.md`, `CA5/CA6/CA7`,
`RE1`, `VB1/VB5/VB6/VB7`, `FB2`, `CB4/CB6`, `HB2`, `TB1`, `ZB2`. No probes, no
edits.

## FINDINGS
- Hash audit: legs 1–9 match MANIFEST exactly; **leg-10.md does not** —
  current bytes `6cd389e9…` (40,401 B; mtime 21:14) vs MANIFEST/CA6
  `c89eea7a…`, whose bytes equal `head -n 59`; the append is the disclosed
  EX10 fallback section. Concurs with `VB5.md:13`, `VB6.md:21`.
- The briefed leg-3 defect **no longer reproduces**: current `leg-3.md`
  (1448 B, `1be7e4f9…` = MANIFEST) has its stdout block hashing to the claim
  `5c682099…` = `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B). RE1's
  `ac7470f9…`/`prompts:{}` observation (`RE1.md:9`) matches the pre-20:59
  state; `census-pre.txt:97` records the interim bytes (`leg-3` `d641e3d3…`,
  `leg-4` `8f04ac26…`), both rewritten before MANIFEST (21:02). `FB2.md:21`
  concurs. Nothing remains to repair for leg-3.
- Measured: 10/10 vs frozen classes (`CA6.md:8`; corroborated `FB2`, `HB2`
  170 recount, `CB6` 6/6 absences, `VB7` six uniform `-32602`, `VB1`); command
  A 78/78, 9/9, 10.0/10.0, token `c6c025f3…` (`TB1.md:4`); ten stale verdicts
  superseded (`VB6`); leg-10 refresh + the 78→79 entry decision parent-owned
  (`ZB2.md:38`).
- Drafts below; `<…>` marks parent fill-ins.

## THREATS
- Wave still landing: 83 root reports at read time (52 lane-A-named, 31
  lane-B-named); the brief's "64 lane-A reports" was not independently
  verifiable from the directory (may count dispatched seats, not files).
- Point-in-time only; re-run hashes and `git status` before landing. leg-10's
  appended content was verified by VB5/VB6-adjacent seats, not replayed
  end-to-end here.
- If the entry is declined, drop every clause marked `[entry]`.

## VERDICT
FINDING: drafts delivered; the briefed leg-3 corruption is superseded by the
pre-MANIFEST rewrite (current bytes consistent); leg-10 MANIFEST/CA6 refresh
and the 78→79 entry decision remain parent-owned.

## DELIVERABLE — LOG draft (paste-ready)

### luna-round-8 — operability: pre-registered 10-leg symmetry battery on REA 6.4.0

- Motivating evidence: luna-round-6's battery exercised the six 6.5-only verbs
  on 6.5.0 only; the kimi-resolved pin is 6.4.0 (luna-round-2 receipts), so the
  same preregistered treatment was owed there (`SCORECARD.md:529-531`;
  per-client evidence asymmetry).
- Work: one axis-move on operability (fleet axis, unowned proxy). One frozen
  10-prediction battery (`P0.md:7-15`): L1 version exactly `6.4.0`, L2 count
  exactly 170, L3–L8 six 6.5-only verbs TYPED-REFUSAL in order, L9 six
  absences, L10 control RESULT; accept at ≥9/10. Two-lane wave; lane A ran the
  battery, lane B re-verified (hash custody, scope freeze, leakage,
  forgery/classification attacks). Per-leg receipts: command, full stdout,
  stderr, exit, stdout SHA-256; full tool list as `leg-2-tools.txt`.
- Landed at `<records commit>` (lane identity): the receipt bundle committed
  tracked (receipts/leg-1..10.md, leg-2-tools.txt, MANIFEST.txt,
  census-pre.txt). Measurement-only round: map/PROVINCE/SKILL untouched.
- Measured at `6e2ee8f`: 10/10 vs frozen classes (CA6 census; corroborated by
  FB2, HB2, CB6, VB7, VB1); command A 78/78, 9/9, 10.0/10.0, token
  `c6c025f3…` (CE2/TB1); tracked tree frozen (CB4); zero availability→holding
  upgrades (CA2); config sentinel matched without a round-8 pre/post pair
  (SE2; CA6: strict zero drift unproven).
- Defects recorded: ten seats (PS1, PS2, PS3, RE2, RV6, RV8, RV1, CA7, XG1,
  RE6) published absent/unscored verdicts before receipts landed — all
  superseded (VB6); leg-10.md stale-by-append — MANIFEST/CA6 cite pre-append
  bytes (VB5: `c89eea7a…` = head-59; current `6cd389e9…`); RE1's leg-3
  display-corruption finding superseded by the pre-MANIFEST rewrite (current
  block `5c682099…` = claim = /tmp raw; interim `d641e3d3…` at
  `census-pre.txt:97`); timeout bounds asserted, not reproducible (RE1);
  battery-labelled /tmp litter left (SE1).
- [entry] If the consolidated knowledge entry lands (CA5 recommendation; RB8
  landing spec): +1 knowledge file + 2 README rows; denominator 78 → 79;
  command A re-measured 79/79 at the landing commit.

## DELIVERABLE — SCORECARD draft

## luna-round-8 — operability: pre-registered 6.4.0 symmetry battery, 2026-10-16

One move on the **operability** axis (fleet axis, unowned proxy — same
recording ruling as rounds 4–6). Claim shape: the frozen 10-prediction battery
executes on the Kimi-pinned 6.4.0 surface with hashed per-leg receipts and
≥9/10 matches; command A + token set unchanged; zero config drift. Predictions
frozen parent-side before dispatch (`P0.md`).

- Wave: two-lane; lane A ran the battery and the receipt bundle, lane B
  re-verified (hash custody, scope freeze, leakage, forgery/classification
  attacks).
- Landed at `<records commit>` (lane identity): receipt bundle committed
  tracked. Measurement-only round: map/PROVINCE/SKILL untouched.
- Measured at `6e2ee8f`: 10/10 vs frozen classes (CA6; corroborations
  FB2/HB2/CB6/VB7/VB1); command A 78/78, 9/9, 10.0/10.0, token `c6c025f3…`
  (CE2, TB1); tracked tree frozen (CB4); zero availability→holding upgrades
  (CA2). Config sentinel matched without a round-8 pre/post pair (SE2/CA6), so
  strict zero drift stays unproven.
- Defects recorded: ten stale verdicts superseded (VB6); leg-10.md
  stale-by-append — "MANIFEST hash `c89eea7a…` = pre-21:14 (head-59); current
  bytes `6cd389e9…`" (VB5); RE1's leg-3 display-corruption finding does not
  reproduce on current bytes (superseded by the pre-MANIFEST rewrite;
  `5c682099…` = claim = /tmp raw); asserted-only timeout bounds (RE1); /tmp
  battery litter (SE1).

| Axis | Before → after | Verdict |
|---|---|---|
| operability (fleet axis, unowned proxy) | 6.5.0-only battery → 6.4.0 symmetry battery: 10 hashed legs, 10/10 vs frozen classes, six per-name refusals cross-lane corroborated | improved |
| coverage | 10.0 → 10.0 (measured; 78/78) [entry] (denominator 78 → 79; re-measure 79/79) | unchanged (improved if the entry lands) |
| depth | 10.0 → 10.0 (measured) | unchanged |
| calibration | 10 → 10 | unchanged |

Learning trends: expansion [entry] improved if the six 6.4.0 per-name refusal
results are admitted (else unchanged); quality improved (stale-verdict
supersession and hash-custody defects caught and recorded); discernment
improved (spoofing, forgeability, shallow-rule and scope-restraint seats —
CA1, CA3, CA10, CA9, CA2, RE4). Planned next: luna-round-9 — candidate
freshness sweep (stale SUMMARY pointers `corpus/README.md:128,160`; jq
safety-language bleed) or the entry decision. Retired: none.

## DELIVERABLE — integration notes (not paste text)

- `[entry]` clauses are conditional on the consolidated entry landing; drop if
  declined.
- If landed, update `SCORECARD.md:23` (coverage row): 78/78 → 79/79, measured
  `<landing commit>`, last-change "luna-round-1 + luna-round-7 + luna-round-8".
- Entry must pass `corpus/QUALITY.md` and carry `source:`/`verified-at:`/
  `recheck:` metadata; hyphenated filename (round-7 lessons, `LOG.md:817-820`).
- Keep the leg-3 defect out of the entry (already superseded; ZB2 disposition).
