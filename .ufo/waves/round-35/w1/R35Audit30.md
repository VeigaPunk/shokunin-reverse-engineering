# R35Audit30 — locate S147 host contract fields (round 35, wave 1, advisory)

Seat: R35Audit30 (scribe, leaf). Item: "Locate S147 host contract fields." Read-only /
private-tmp only; the sole lane write is this report. No subagents, no VCS mutation, no
Pacman.

## Affirmed scope
- Frozen claims C1/C2 untouched; no predicates altered; no lane production file read/written
  other than this report.
- S147 is **not** a frozen row: it is a quarantine-candidate staged id (round-5 register row),
  explicitly **not adopted** (quarantine verdict line 21, 24). This report is advisory
  evidence only.

## Behaviour / what was located
S147 (kaidoku round-5) is a *proposed* SOURCES row whose source is the host's own REA
contract. The "host contract fields" the row claims, and where they actually live:

1. **Row definition** — `shokuknow/lanes/kaidoku/round5/SOURCES-PROPOSED.md` line 18:
   source `agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` (local artifact under
   `$HOME`), kind docs, tier A, anchor `§ "REA release" and § "Expected doctor output"`,
   teaches "this machine runs `rea-agents@6.7.0` with skill v42 and 207 tools, REA is
   CLI-first and loads nothing on session spawn, and `rea-agents setup --client …` is
   forbidden", recheck `` grep -c '207 tools' $HOME/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md `` -> 1, used-by `corpus/knowledge/rea-catalogue-version-join.md`.
2. **Gate — S147 block** — same file lines 47-52: URL local artifact, opened 2026-10-23,
   anchor `§ "REA release"`, quote `207 tools`, also `Do not run `rea-agents setup --client ...` or re-enable the plugin`.
3. **Host contract file** — `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`
   exists, 3,386 bytes (matches quarantine's 3,386 B). Verified fields:
   - line 18: CLI pin `npx -y rea-agents@6.7.0 <command> [args] --json`;
   - lines 32-33: `…@6.7.0 --llms` / `--schema` read commands;
   - line 41 (`## State as of this writing`): `- REA release: `rea-agents@6.7.0`, skill v42, 207 tools.` — carries all three row claims in one line;
   - line 53 (doctor table under `## Expected `doctor` output on this host`): `skill.installed_version` is still `42` and `installed_tool_count` is still `207`;
   - lines 23/25 (`## Do not`): `Do **not** run `rea-agents setup --client <client>`…` and `Do **not** run `mcode plugin enable rea@official`.`;
   - lines 12-16: `rea` plugin disabled in MiniMax Code runtime, session starts with zero REA MCP tools (matches "loads nothing on session spawn").
4. **Recheck reproducibility**: `grep -c '207 tools' …HOST-CONTRACT.md` -> **1** (only line 41). `rea-agents@6.7.0` occurs 5 times (18/32/33/41/60).

## Commands / output (all read-only)
- `wc -c ~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` -> 3386
- `grep -nF '207 tools' …` -> `41:- REA release: `rea-agents@6.7.0`, skill v42, 207 tools.`
- `grep -nF 'rea-agents@6.7.0' …` -> lines 18, 32, 33, 41, 60
- `grep -n 'Do .not. run' …` -> no match (file uses `Do **not** run`)
- `grep -n '^#\|^##' …` -> headings: `# Host contract — REA on this machine`, `## The rule`, `## Do not`, `## Do`, `## State as of this writing`, `## Expected `doctor` output on this host`
- `grep -nF 'Do not run `rea-agents setup --client' …` -> rc=1 (no literal)
- `ls ~/Projects/shokuknow/corpus/knowledge/rea-catalogue-version-join.md` -> No such file or directory
- `grep -c '207 tools' …` -> 1

## First falsifications (milestone)
1. **Gate `also:` quote is not verbatim.** `Do not run `rea-agents setup --client ...` or re-enable the plugin` has no literal match (grep -F rc=1); the file's actual literals are `Do **not** run `rea-agents setup --client <client>`…` (line 23) and `Do **not** run `mcode plugin enable rea@official`.` (line 25). A strict quote-lint (`grep -F`) on the `also:` cell would fail — consistent with the register's `no-locator`/ABSENT-class treatment.
2. **Anchor headings are not literal.** The row/gate anchor `§ "REA release"` is not a markdown heading; the phrase is a bullet under `## State as of this writing` (line 39/41). `§ "Expected doctor output"` is `## Expected `doctor` output on this host` (line 46). Anchor checkers requiring a literal heading fail on `§ "REA release"`.
3. **Used-by entry absent -> row never adopted.** `corpus/knowledge/rea-catalogue-version-join.md` does not exist in shokuknow; confirms quarantine verdict "still not adopted (no admitted entry cites it)". S147 is a candidate, not an admitted row.

## Limits
- The 3,386-byte size matches the capture date (2026-10-23); file mtime is 2026-10-22
  22:11 (unchanged at verification time 2026-10-25).
- No write to shokuknow or any production path; register/gate read via `read`/`grep`
  (read-only).
- S147's recheck cell itself notes `(ran 2026-10-23)`; I re-ran the identical grep today and
  reproduced count 1.
