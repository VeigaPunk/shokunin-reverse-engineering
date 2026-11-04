# ExecC2 — seat report (round-71 w1): R71-C2 independent rederivation + frozen battery attack

Seat ExecC2-3, 2026-11-04. Scope: re-derive R71-C2 with my own shape builder (no use of
`tools/round-71/forged-receipts.py` for steps 2–3), then run the frozen battery at the freeze.
All work in `.ufo/waves/round-71/w1/ExecC2/` + scratch `/fast/scratch/hyaku/kaidoku-r71/ExecC2/`
(now removed; all receipts copied here first). No tools installed, no pacman. Read-only git
only; no commits, no pushes, no edits outside my scope.

## 1. Independent rederivation (steps 2–3) — GREEN

My own `build-lying.py` cuts six receipts from `.ufo/waves/round-70/l1/scores/c3-at-landing.json`,
relabels each to the first-cut world (`rev 4737a542…`; `instrument.sha256 = 1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880`
= sha256 of the `git show 4737a542…:tools/round-70/packed-elf.py` blob bytes; the blob's git
object id is `070010fa…`, the receipt field carries the content hash the readers re-derive), and
lies in exactly one verdict-relevant field per shape:

| shape | lie | first cut (blob 4737a542) | superseded (bytes 7c155617, argv --rev 4737a542) | declared clause found |
|---|---|---|---|---|
| L1_unpacked-counts | jq `.unpacked_counts.procedure_count` 167→168 | rc 0 met | rc 1 `jq: unpacked_counts {…168…} != orig_counts` | unpacked_counts |
| L2_packed-sha | xxd `.packed_sha256` → 0×64 | rc 0 met | rc 1 `xxd: packed_sha256 000… != declared 1727faf9…` | packed_sha256 |
| L3_section-list | libz `.section_count`→3, `.upx_list_rc`→1 | rc 0 met | rc 1 `libz: section_count 3 != 0` + `upx_list_rc 1 != 0` | section_count |
| L4_runs-argv | jq `.runs.pack.argv` drops `--best` | rc 0 met | rc 1 `jq: runs.pack.argv […] lacks --best` | runs.pack.argv |
| L5_refusal | jq `.refusal.packed_rc` 1→0 | rc 0 met | rc 1 `jq: refusal.packed_rc 0 (packed bytes must refuse)` | refusal |
| L6_format | dinit `.format.type` `EXEC (Executable file)`→`DYN (Position-Independent Executable file)` | rc 0 met | rc 1 `dinit: format … != readelf of the pinned source …` | format |

Honest relabel control (no lie): accepted by BOTH readers (rc 0 met both) — the relabel alone is
sound; only the single lie trips supersession. Evidence: `lying-rederive.json`,
`lying-receipts/` (my receipts + manifest), `build-lying.py`, `run-checks.py`.

## 2. Frozen battery (step 4) — frozen bytes FAIL, uncommitted tree edit is green

Command verbatim from the assignment (`--rev b827a8b5… --base-rev 5cc845ca… --first-cut-rev
4737a542… --superseded-rev 7c155617… --pkg ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`).

**Run B (authoritative): FROZEN bytes**, blob at `b827a8b5…`, sha256 `50bb190b3c0b91870bfcce74c9898167f961102c8381d1a2b0c70fe7df115c7f`
= the claims.json pin → **exit 1, `ok: false`, failures 4**:
`F3L_relabelled-landing` and `F9L_unknown-landing` "frozen probe did not reject it on
A5_carrier_record with A6 true (rc 1, arms {A5: False, A6: False})";
"genuine landing receipt rejected by the frozen checker" (producer clause `rev 7c155617… !=
b827a8b5…`); "genuine landing receipt rejected by the frozen probe" (4/6 arms). Its six lying
rows are still all (0, 1) + clause, its ten base-world shapes and `battery_arms` green.
Receipt: `battery-frozen.json`.

**Run A: working-tree bytes** sha256 `44b973f1…` → **exit 0, `ok: true`, failures []**: 10
base-world + **6 lying (all first_cut_rc 0 / superseded_rc 1 + clause)** + 2 landing identities
(A5 false, A6 true), genuine accepted by both frozen readers (checker 0; probe 6/6), battery
arms green. Receipt: `battery.json`; its six lying receipts in `shipped-battery-lying-receipts/`;
Run B's in `shipped-battery-lying-receipts-frozen/`.

**Root cause (defect).** The frozen `check()` anchors the three landing-world invocations (F3L/F9L
probe call ~line 326; genuine checker ~line 375; genuine probe ~line 378) to `--rev <measured>`
instead of the landing world `superseded_rev`. The landing material is bound to `7c155617…`, so
at `--rev b827a8b5…` the producer clause always fires and A6 collapses to false — "genuine
receipts still accepted by both frozen readers" and "landing identities rejected with A6 true"
are **unsatisfiable at the pinned bytes**. Round-70 tool bytes are identical at both revs
(packed-elf blob `9be15f77…`, contract-probe blob `803f6ed3…` at both `7c155617…` and
`b827a8b5…`), so only the `--rev` anchoring differs. The uncommitted working-tree edit
(` M tools/round-71/forged-receipts.py`, 7+/6−, `working-tree-drift.diff`) changes exactly those
three call sites to `superseded_rev` and yields the declared green. No commit touches the path
since the freeze (`b827a8b5..HEAD` = only `46d9e311`, wave dispatch); `claims.json` unchanged,
still pinning `50bb190b…`; no `instrument_supersessions` entry in the round-71 container.

**Do-nothing control observed:** `.ufo/waves/round-70/l1/scores/c1-at-landing.json` = shapes 10,
landing_probe_shapes 2, `lying_shapes` ABSENT, rev `7c155617…` — matches the predicate's
do-nothing clause.

## 3. Risks / handoff notes

- The green Run A state exists ONLY uncommitted. If the wave lands it as-is, the claims.json pin
  (`50bb190b…`) no longer matches the landed instrument and A1/the kill rule fire. The landing
  seat must either commit the fix WITH a re-taken pin + `instrument_supersessions` disclosure
  (predicates byte-unchanged, the r67/r70 precedent), or fix the frozen call sites in a
  supersession commit before the C2 landing receipt is measured.
- My steps 2–3 evidence is byte-independent of that decision: the six lying-field shapes
  themselves are sound against both reader generations (identical clause strings from my builder
  and both battery byte-states).
- Battery-receipt paths under `/fast/scratch/…` inside `battery.json` / `battery-frozen.json`
  are run pointers, not evidence (scratch removed per bounds); the clause strings are inline in
  those JSONs and the six+six lying receipts are copied here.
- Full derivation + tables: `rederive.md` in this directory.

VERDICT: defect named — R71-C2's six lying-field shapes re-derive green independently (own builder: 6× first_cut 0 / superseded_rc 1 with declared clause; honest relabel passes both readers), but the FROZEN forged-receipts.py (pin 50bb190b…) exits 1 at the declared argv because its genuine-receipt and F3L/F9L arms anchor to --rev <measured> instead of the landing world 7c155617… (genuine-accepted and A6-true unsatisfiable at the pinned bytes); an uncommitted working-tree edit (44b973f1…) is the minimal fix and runs the battery green (exit 0, 18 rows) — re-take the pin + disclose the supersession when it lands.
