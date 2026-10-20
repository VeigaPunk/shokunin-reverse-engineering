# Round 16 — Mistakes rows for the four round-15 outside routes (DRAFT)

status: draft for L1 integration; not appended to any lesson, LOG, SKILL, SHONEN or QUALITY file.
source: `corpus/lessons/round-15-verifier-spotcheck.md:181-188` (routed defects 1-4, status-neutral, assigned to kaidoku round 16).
red-before: no check was executed by this seat. Every "predicted" value below is inferred from bytes read in the repo; L1 must capture each red-before output once, before any edit lands.

## Mistakes rows

| class | evidence | captured-by | fix |
|---|---|---|---|
| invocation drift (reference-drift) | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` `recheck:` runs `python3 .ufo/waves/round-15/snapshot-inventory.py --ghidra … --select 1.24.7 1.25.7 1.26.8` (no `-I`, cwd-relative script). Recorded execution `.ufo/waves/round-15/verification.json` commands `snapshot-inventory` and `inventory-determinism` use `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py …`, exit 0. The same no-`-I` form also appears in `SKILL.md:487` (go-snapshot-inventory registry row). | Authored review: not caught; the recheck line and registry row were authored without an argv-equivalence check, and the row has no selftest or gate. Independent closure: `round-15-verifier-spotcheck.md:185` (routed defect 1). `SKILL.md:487` was found by this round-16 source read and is NOT yet adjudicated by closure. | Align both guidance lines to the exercised argv (`python3 -I <absolute script path> …`), or explicitly label the relative form as an intended recheck distinct from recorded argv. Land as a named append-only correction in the knowledge entry, not a silent rewrite. Red-before: R1. |
| registry pin omission (reference-drift / discoverability) | `SKILL.md:450` quote-fidelity row pins only `.ufo/waves/round-14/fixtures/expected.json`. The supplemental frozen baseline `.ufo/waves/round-15/boundary-fixtures/expected.json` (exists; run as `boundary-frozen` in `verification.json`, exit 0) is not referenced anywhere in SKILL.md. | Authored review: not caught; the round-15 lesson cites the boundary controls, but the registry pinned-values cell was not updated. Independent closure: `round-15-verifier-spotcheck.md:186` (routed defect 2). | Add `.ufo/waves/round-15/boundary-fixtures/expected.json` to the quote-fidelity row's pinned-values cell, leaving the original round-14 pin and command A/frozen command unchanged. No new gate or classifier. Red-before: R2. |
| provenance gap (number-drift / survivor adjacency) | `.ufo/waves/round-15/no-harm-controls.json` holds SHA-256 craft tallies (17/17), `unchanged_inputs`, `append_only`, `pins_match` booleans with no producing command, no `producer` key, and no generator anywhere in `.ufo/waves/round-15/` (grep for `no-harm-controls` hits only `LOG.md` and the round-15 lesson). The closure's count core (`round-15-verifier-spotcheck.md:44-78`, `:141-143`) is in its own session, not retained in the repo. | Authored review: not caught; the file was written without its command. Independent closure: `round-15-verifier-spotcheck.md:187` (routed defect 3); closure reproduced the values from Git objects itself. This closure reproduction does not establish that the author's original count was a retained invocation. | Commit the stdlib producer that regenerates `no-harm-controls.json` (or record its argv, exit and stdout in `verification.json`), and name it from the file or its registry row; re-run for byte equality. Do not hand-edit the booleans. Red-before: R3. |
| temporal reference drift (historical wording) | `SHONEN.md:10` (box 3, "Instructions executable by an agent without oral context") says "this round executed the bounded native recipe and the scorecard counting recipes" and cites `corpus/lessons/2026-10-15-round-1.md`. The executed round is the historical round-1 (2026-10-15), not the current round. | Authored review: the box 3 wording was authored in the round-14/15 canonicalization. Independent closure: `round-15-verifier-spotcheck.md:188` (routed defect 4), adjudicated as wording-only; no mark change. | When SHONEN's evidence line is next updated, replace "this round" with the explicit historical round (round-1, 2026-10-15). SHONEN is a canonical seed, not append-only; keep every mark `[~]` and do not change pointer text. Red-before: R4. |

## Authored review vs independent closure (per row)

| row | authored review result | independent closure result | not claimed |
|---|---|---|---|
| invocation drift | missed; no argv-equivalence check exists | routed defect 1 | that `SKILL.md:487` was closure-reviewed |
| registry pin omission | missed; pinned cell not updated | routed defect 2 | that the supplemental baseline is a new gate |
| provenance gap | missed; no producing command retained | routed defect 3, recount reproduced in closure session | that the original author count was a retained invocation |
| temporal reference drift | author wording stands; "this round" unqualified | routed defect 4 | any SHONEN promotion or mark change |

Closure seats are not the author's L2 seats and are not counted as outside sampling here. No row claims a resolved state: C2's "resolved with reproducible command evidence" holds only after L1 captures the red-before and the post-fix outputs.

## Red-before commands (run by L1 once, before any edit; predicted values are inferred, not observed)

R1 — invocation consistency
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
grep -n '^recheck:' corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md
grep -n 'round-15/snapshot-inventory.py' SKILL.md
python3 -c "import json;[print(c['label'], c['argv'][:3]) for c in json.load(open('.ufo/waves/round-15/verification.json'))['commands'] if c['label'].startswith(('snapshot','inventory'))]"
```
Predicted red: both grep hits lack `python3 -I`; the recorded argv shows `python3 -I <absolute path>`. Pass after fix: both grep hits contain `python3 -I` plus the absolute script path, or an explicit "intended recheck, not recorded argv" label.

R2 — supplemental baseline discoverability
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
grep -c 'boundary-fixtures' SKILL.md
test -f .ufo/waves/round-15/boundary-fixtures/expected.json && echo present
```
Observed by this seat with read-only grep: `0` (no reference). Predicted red: `0`. Pass after fix: count ≥ 1, the reference sits in the quote-fidelity row's pinned-values cell, and `present` prints.

R3 — producing command for no-harm controls
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
grep -rl 'no-harm-controls' .ufo/waves/round-15
python3 -c "import json;print(sorted(json.load(open('.ufo/waves/round-15/no-harm-controls.json'))))"
```
Observed by this seat: first command has no hit; the second lists only the two commit-hash keys, `unchanged_inputs`, `row16_unchanged`, `append_only`, `pins_match` (no producer/command key). Predicted red. Pass after fix: a committed producer or recorded argv/exit appears, and a re-run reproduces the file byte-for-byte.

R4 — historical SHONEN wording
```sh
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
grep -n 'this round' SHONEN.md
```
Observed by this seat: only line 10. Predicted red. Pass after fix (at the next evidence-line update, by the integrator): no bare "this round" in box 3; the historical round is named as round-1, 2026-10-15; every box remains `[~]`.

## Constraints for L1

- Fix R1 and R2 as named append-only corrections where the target is a lesson/knowledge entry; SKILL registry rows are edited in place only where the row's own discipline permits (the quote-fidelity pinned cell is in scope).
- Do not run any red-before command from this draft as evidence of a pass; capture the outputs in the wave record with exit codes.
- No tool installs or updates are involved.
