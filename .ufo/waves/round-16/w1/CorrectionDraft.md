# Round-16 w1 — CorrectionDraft report

Status: draft only. Source reading only; no check, build, test, or probe was executed. No installs or updates.

## Deliverable

- Draft correction: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/CorrectionDraft.candidate.md`. It is intended to be appended, unchanged, to the end of `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`. L1 integrates.
- No existing doc, knowledge entry, lesson, LOG, SCORECARD, QUALITY, SKILL, SHONEN, SOURCES, README, or retained round-15 artifact was edited.

## Finding (what the record shows)

| Item | Location | Observed |
|---|---|---|
| r15 entry `recheck:` | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` | `python3 .ufo/waves/round-15/snapshot-inventory.py --ghidra … --select 1.24.7 1.25.7 1.26.8`: relative path, no `-I` |
| Exact recorded argv, `snapshot-inventory` | `.ufo/waves/round-15/verification.json:28-44` | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py --ghidra … --select …`; exit 0 |
| Exact recorded argv, `inventory-determinism` | `verification.json:45-61` | Same argv; exit 0 |
| Equality and digest | `verification.json:159,180` | `inventory_equal: true`; SHA-256 `ad06fadc…bb2fe` |
| Earlier failed run, same `-I` absolute argv | `verification-initial.json:28-44,45-61` | Revision `856d193…`; exit 1, traceback at the `scan_directory` sort; stderr truncated before the exception type |
| Entry claim "the `recheck:` command ran twice" | entry lines 52-53 | Literal string is not what ran; the `-I` absolute form is |
| Routed defect 1 | `corpus/lessons/round-15-verifier-spotcheck.md:185-186` | Names this exact discrepancy and asks for alignment or explicit distinction |
| Probe CLI | `.ufo/waves/round-15/snapshot-inventory.py:406-417` (argparse), `:55-61` (stdlib-only imports) | `-I` is an interpreter flag, not in the probe's argparse |

Interpretation used in the draft:

- **Exact recorded invocation**: the `-I` absolute-path argv in `verification.json`. Only this supports the entry's inventory result.
- **Source-only preview**: the `recheck:` string. It is derived from the probe's CLI surface and was not run in any retained record.

## Correction approach

- Append-only, named (`## Round-16 correction — r15 snapshot-inventory recheck invocation (append-only)`), following the existing round-14 and round-15 correction pattern in the lessons.
- Does not rewrite `recheck:` or the executed-inventory paragraph. It qualifies them by pointer.
- Recommends that future rechecks run the recorded argv verbatim.
- Does not claim the relative-path spelling is wrong, nor that `-I` is output-neutral.

## Calibration: what is observed vs inferred

- Observed: argv, exit codes, `inventory_equal`, and digest, all from committed bytes read in this session.
- `[INFERENCE]`: the `-I` flag does not change output. The probe imports only standard-library modules, and its output is `sort_keys=True` with absolute paths. This is expected, not measured. The draft labels it so.
- `[INFERENCE]`: the semantics of `-I` (ignores `PYTHON*` environment variables; omits the script directory from `sys.path`) come from general Python knowledge, not from a retained document or run.
- Not claimed: the cause of the initial failure beyond "sort in `scan_directory`"; the exception type (truncated in the record).
- Not claimed: any target capability, provider behavior, historical cause, or numeric score.

## Out of scope for this draft (other round-16 routed items)

Items 2 (supplemental baseline discoverability), 3 (producing commands for controls), and 4 (historical SHONEN wording) are not addressed here. Only routed defect 1 is in scope for this w1 slice.

## Checks for L1 to run once after integration (not run by this seat)

1. Confirm the draft is appended only at end of `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`: the pre-append bytes (74 lines, as read in this session) must be unchanged, and the `recheck:` line 3 must be byte-identical to its pre-correction value (append-only check). The baseline `6235498b4112350eebce0812a74af1781fc0ee88` was not checked for this file by this seat.
2. Confirm the argv string in the draft matches `verification.json` lines 30-40 exactly. A stdlib one-liner: parse `verification.json`, select `label == "snapshot-inventory"`, `' '.join(argv)`, and compare against the draft's code block.
3. Run the knowledge-entry citation probe over the appended correction if it is registered; check that `:185-186`, `:406-417`, `:55-61`, `:159`, `:180`, `:41`, `:58` resolve at the integration revision.
4. The `recheck:` line itself is unchanged, so no citation-drift pin on line 3 should move. Confirm this against any pointer table that names it.

## Limits

- The verification sequence above was not executed. Its success is not claimed.
- The retained stderr of the failed run does not name the exception type, so the failure cause is recorded only as "sort in `scan_directory`".
- The draft does not establish that `-I` is necessary. It only establishes that the recorded argv used it.
