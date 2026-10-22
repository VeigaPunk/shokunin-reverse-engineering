# SkillRowDraft — SKILL.md text for EVM selector naming (round 25, attempt 3, wave 1)

Scope: read-only on the lane; the only lane write is this report. Mutation experiments ran in a
sandbox clone at `/fast/scratch/hyaku/kaidoku-r25-a3/seats/SkillRowDraft/clone`; no tool was installed.
Read: `SKILL.md` (EVM row `:54`, decision table `:42-66`, error patterns `:68-79`),
`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`,
`corpus/evidence/round-25/a3/c2/analyze/tally.json`, `corpus/SOURCES.md` (S075–S077 at `:81-83`),
`PROVINCE.md:91-93`.

## Draft 1 — decision-table row

Anchor: `SKILL.md` line 54, the row
`| EVM bytecode | \`inspect-evm-interface <file> <raw|hex>\` — encoding POSITIONAL | held (selector recovery) |`.
Insert this one line immediately **after** line 54 (it becomes line 55), inside the
`## Decision table (this host, r3-verified)` table:

```
| EVM selector names | 4byte.directory + openchain (`filter=false`) lookup → Keccak + REA-argument check (`tools/round-25/a2/resolve-selectors.py`) | held r25 (offline, saved lookups) — candidates only, never verified names; 49/69 rows named, 0 wrong, 20 unnamed (`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`) |
```

Format match (observation): 3 columns `Target | First move | Status`, backticked verbs/tools,
`held …` status vocabulary as in the neighbouring rows, one inline lane-relative corpus path in
backticks — the citation form used in "Known limits" (`SKILL.md:403-419`) and the craft bullets.

## Draft 2 — error-pattern bullet

Anchor: `SKILL.md` line 79, the last row of the `## Error patterns (typed refusals)` table. Insert one
blank line, then the bullet, then one blank line, so it sits between that table and the
`## Queue-drain craft (rounds 5-12, distilled in round 13)` heading (line 81 today):

```
- **A recovered selector is not a named function.** REA's `inspect-evm-interface` returns the selector, inferred arguments and inferred mutability, never a name; a name comes from a signature database that takes public submissions, so it stays a candidate until Keccak and REA's inferred parameter list both agree. Never take the first 4byte.directory result — 26 of its 59 names were wrong on the six lane carriers — and never read "no candidate" as "no public name" (`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`).
```

Format match (observation): that section is a table of typed refusals only, so a semantic
(non-refusal) failure cannot be a row there; the bullet uses the file's other bullet style — bold
lead-in, prose, inline lane-relative path in backticks — as in `SKILL.md:407-419` and the craft
bullets at `SKILL.md:84+`. Flagged for the integrator: the bullet goes below the table, leaving the
typed-refusal table's semantics intact.

## Provenance of every number in the drafts

- 49 named / 0 wrong / 20 unnamed over 69 per-carrier rows: rule `openchain_sole_unfiltered_args_consistent`
  in the committed `corpus/evidence/round-25/a3/c2/analyze/tally.json` (`per_carrier_rows.rules`); 26 of
  59 wrong for "first 4byte.directory result": same file, rule `fourbyte_first`, also stated in the entry
  at `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md:70-71`. Six carriers:
  `corpus/evidence/round-25/a2/c2/carriers.tsv` (6 rows).
- "candidates only, never verified": entry title and `PROVINCE.md:91-93` ("names are labelled candidates
  from saved signature-DB lookups, never verified"), landed by L1 at `08c7a729`; public submissions and no
  result order: S075/S076 (`corpus/SOURCES.md:81-82`); REA returns no function name: S077
  (`corpus/SOURCES.md:83`). All are observations of committed artifacts; no producer was re-run here.

## Attack on the draft (what I tried to break)

Command for every F below (sandbox clone; per-revision tables extracted with `git show <rev>:<path>`,
so the table used is the one committed at that rev):
`python3 -I .ufo/gates/citation-drift/citation-drift-probe.py --root <clone> --rev <REV>
--table <table@REV> --expected <expected@REV> --strict`

F1 — the draft shifts SKILL.md line numbers and breaks four pinned citations.
**Verdict: fails as a standalone paste.** 2026-10-22T10:48:16Z, rev `08c7a729` (C2 tip, committed table
`7994eec7e764…`): `CITATION_DRIFT_VERDICT: failed findings=5 exit=1`, 0 `skill-rule14` findings. Same
second, rev `c876db75` (draft applied, same committed table): `findings=9 exit=1` with 4 new findings —
`skill-rule14-entry-recheck SKILL.md:255`, `skill-rule14-cr2-identity SKILL.md:249`,
`skill-rule14-verdict-identities SKILL.md:251`, `skill-rule14-log-fresh-identity SKILL.md:257` (all
`states no resolvable pointer`). Cause: the pointer table pins SKILL.md lines 246/248/252/254 as
`kind: extracted`; the draft adds 3 lines above them (1 table row + bullet + blank), so each pin lands on
the wrong line. Delta: exactly +4 findings (5 → 9).

F2 — co-landing the repin restores the baseline. **Verdict: holds.** Same command, rev `13e26f3e` (draft +
pointer-table lines 246→249, 248→251, 252→255, 254→257 + `expected.json` `pointer_table.sha256`
re-pinned to `439328afcb4b…` in one commit, as the frozen-run guard demands):
`CITATION_DRIFT_VERDICT: failed findings=5 exit=1`, 0 `skill-rule14` findings — the draft then contributes
zero new findings. Note (observation): the probe reads `--table`/`--expected` from the filesystem, not
from `--rev`; a table edited without a same-commit digest re-pin reports `pointer_table_tampered`.

F3 — the gate is already red before this round. **Verdict: pre-existing, not caused by the draft.** Same
command at round baseline `18e7eb6d`, instrument commit `9dcd11ec`, C1 commit `0e333eb` and C2 tip
`08c7a729`: each returns `findings=5 exit=1` with the same five ids (`sc69-readme-177`, `sc72-readme-nitrow`,
`readme175-sc1217`, `readme175-r7range`, `readme175-r8e2`) — all in SCORECARD.md / corpus/README.md, none
in SKILL.md.

F4 — shift-free anchor. **Verdict: could-not-evaluate** (not run): appending the same blocks after
`SKILL.md:832` leaves lines 246–254 untouched so F1 would not fire, but the row would leave the decision
table and the bullet the error-patterns section — contrary to the assignment.

## Out of scope / integration checklist for L1

No lane file edited beyond this report; the five inherited gate findings (F3) were not fixed; no re-run
of the C2 tally, resolver or REA replay. Integration steps for L1:
1. Paste the row after `SKILL.md:54` and the bullet after `SKILL.md:79`.
2. Co-land the pointer-table repin (SKILL.md 246→249, 248→251, 252→255, 254→257) with the
   `expected.json` `pointer_table.sha256` re-pin in the same commit, else the gate gains 4 findings (F1).
3. The drafts cite only `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` and
   `tools/round-25/a2/resolve-selectors.py`, both committed at `08c7a729`.

## Artifacts (under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/SkillRowDraft/`)

| Path | sha256 |
|---|---|
| `draft-skill-md.diff` | `7793580d43036e0a129b25670eb23fa613f3535de533d514ec75fd42fa01330d` |
| `mitigation-pointer-repin.diff` | `d43ecc2ae0fce50522d9e8ec6da01d2b8ca7f9eaae28186a0d4d9503b73a2f99` |
| `probe-base-08c7a729.txt` | `076924e93543fe2299b16d281476b35c3795e6b1a2555df1760b78d2a166e6fb` |
| `probe-draft-c876db75.txt` | `b5a47c2501e410a868720ba8e3cc093918d3b7997a0e18577959ac83aa59ea4d` |
| `probe-mitigated-13e26f3e.txt` | `792037ec47edcbf17292f1b1f01c61ce4db13f591a717a1cb7b46d35ff5b354a` |

Sandbox clone: `…/seats/SkillRowDraft/clone` (base `08c7a729`, draft commit `c876db75`, mitigation
commit `13e26f3e`).
