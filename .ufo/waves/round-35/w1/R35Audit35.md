# R35Audit35 — D4 table-boundary review

Seat: read-only audit; only this report is written. Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Frozen scope

`plans/round-35-claims.md` declares C2 D-4 as exactly eight cells in every data row of the Round-32 and Round-34 run-6 instrument-registry tables. Canonical C2 predicate says the same; counter headings are hardcoded as `### Round-32 instrument registry` and `### Round-34 run-6 instrument registry`. No predicate or scope change is proposed.

## Evidence and first falsification

Read `tools/round-35/c2-calibration-counter.py` lines 129–153. For each heading, it scans from the first exact `rstrip()` match until the next line beginning `##` or `###`, and checks each `|` line via `count('|') - 1 == 8`; first bad row per section fails. This checks all pipe lines in the heading's entire section span, not only rows semantically belonging to a registry table. It also does not distinguish header/separator from data, though the stated target is every data row.

`SKILL.md` shows the Round-32 heading at line 1064; its next heading boundary is not until the Round-33 status section at line 1086. Within that span is a separate “Residual witness registry” table (lines 1081–1084), whose displayed header/separator/data rows have four cells, plus another unrelated table (round-33 decisions; see earlier audit R35Audit42 for its observed location). Thus D4's Round-32 scan will reject on unrelated rows even if all Round-32 registry rows are eight-cell. This is a boundary/scope mismatch, not a merely incorrect cell count in the target table.

The live Round-34 run-6 heading is `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)` (SKILL.md line 1209), not the exact frozen literal. The counter therefore reports `D4_section_missing:### Round-34 run-6 instrument registry` until that heading is changed to the exact expected line. If renamed, its scan continues through the next `##`/`###` heading; the current section contains a five-cell table by construction, so all its pipe rows are implicated. Confirm the intended section extent before attempting any layout-only repair. (The distinct `## Round-34 instrument registry` at line 1182 is not the run-6 target.)

## Commands and outcomes

- Read only: plan, canonical claims JSON, C2 counter, `SKILL.md`, and round-34 spotcheck lesson; inspected specification item and sibling `R35Audit42.md` as prior boundary evidence.
- `git show aa04633a686d49756763b1feed4be6830d5bb479:SKILL.md > /tmp/skill-base.md && wc -l /tmp/skill-base.md` → `1221 /tmp/skill-base.md` (private temporary file).
- `git log --format='%h %cI %s' aa04633a686d49756763b1feed4be6830d5bb479..HEAD -- SKILL.md` → no output, so no committed SKILL.md changes since base were observed.
- `git rev-parse HEAD` → `3ecf42981a0b63414de90ade643040d609dbb8a5`; `git status --porcelain | head -20` showed only orchestrator-created untracked round-35 wave artifacts, including `w1/`; no SKILL.md change was shown.
- Attempted counter at base-as-freeze: `python3 -I -B tools/round-35/c2-calibration-counter.py --root <lane> --base aa04633a686d49756763b1feed4be6830d5bb479 --freeze aa04633a686d49756763b1feed4be6830d5bb479 --rev HEAD` → exit 2, `C2: claims file absent at freeze revision`. This is expected from the freeze input absence and is not a measured D4 verdict; no counter result is claimed.

## Advisory and limits

D4 has two independent boundary hazards: exact-heading mismatch for Round-34 run-6, and Round-32 overreach into other tables. The frozen predicate/scope cannot be narrowed by this seat. Any repair must preserve the frozen check's literal heading and ensure its scanned section contains only rows that legitimately must satisfy eight cells, or otherwise convert all scanned pipe rows to eight cells without silently changing semantics. No lane code, corpus, counter, plan, claims, VCS, or source tree was modified; no counter selftest or claim score was run. The report is advisory evidence only.

Report: `.ufo/waves/round-35/w1/R35Audit35.md`
