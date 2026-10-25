# R35ExecC2 — cloned C2 green/red /tmp fixture; Git root

Item: "Run cloned C2 green/red /tmp fixture; verify Git root." (wave r35-build w1, milestone "Build evidence and first falsifications").
Instrument: `tools/round-35/c2-calibration-counter.py` (frozen). Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base `aa04633a686d49756763b1feed4be6830d5bb479`; freeze `2323d197456f1328459d9420aff025cffbcb3e27`; measured head `3ecf42981a0b63414de90ade643040d609dbb8a5`.

## Git root verification (clone)

```
$ git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r35w1-c2-fixture-20261025
$ git -C /tmp/r35w1-c2-fixture-20261025 rev-parse --show-toplevel
/tmp/r35w1-c2-fixture-20261025        # == clone root; HEAD == 3ecf42981a0b63414de90ade643040d609dbb8a5; clean
```
The counter's git calls (`git -C <root> show/log`) all ran from that root; no git writes were made to the lane (lane status unchanged apart from the wave's own pre-existing untracked dispatch/spec files).

## Runs (counter read only immutable git objects; `python3 -I -B`)

| # | fixture | revision | command | exit | C2 output / failing |
|---|---|---|---|---|---|
| 1 | real base (control) | `aa04633a` | `--root <clone> --base aa04633a... --rev aa04633a... --freeze 2323d197... --json-out /tmp/r35w1-c2-base-red-receipt.json` | 1 | `C2_FAIL: D1_census_start_missing; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry` |
| 2 | real head | `3ecf4298` | same, `--rev 3ecf4298...` | 1 | `C2_FAIL: D1_no_sources_change_after_base; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry` |
| 3 | synthetic green (all four defects satisfied in clone commits) | `2beb52ad` | same, `--rev 2beb52ad...` | 0 | `C2_CLEAN revision=2beb52ad...` (receipt `pass=true`, `failing=[]`) |
| 4 | synthetic red mutant (lesson seat line corrupted) | `58c04e40` | same, `--rev 58c04e40...` | 1 | `C2_FAIL: D2_lesson_seat_mismatch` |
| 5 | selftest (green/red built-in) | — | `--selftest` | 0 | `C2_SELFTEST: ok` / `green=0 red=1` |

Green synthetic data (clone-only, clearly not claim data): `corpus/lessons/round-35.md` (`Seat accounting (round 35): spawned=4 settled=4 dead=0` + `AAdjacencyCite 31/32 correction`), `w1-settle.json`/`w2-settle.json` (`{spawned:2,settled:2,dead:0}` each), SKILL.md registry fixes (see D-4), appended D-3 trio, and a SOURCES row so D-1's first-change ordering is evaluable. Red mutant = same tree with `spawned=99 settled=99`.

## First falsifications (measured head `3ecf4298`)

- **D-2 open** — `corpus/lessons/round-35.md` and `.ufo/waves/round-35/w1-settle.json`/`w2-settle.json` do not exist at head → `D2_lesson_missing`.
- **D-3 open** — `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` cites S106 only as `sources: S106 …` (line 5, plural) and contains no lines matching `^source\s*:`, `^verified-at\s*:`, `^recheck\s*:` → all four D3 checks fail.
- **D-4 open** — `SKILL.md` `### Round-32 instrument registry` section includes the 4-cell "Residual witness registry" table (row at line ~1081 → `cells=4`); the round-34 run-6 section heading is `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)`, which is not the exact required string `### Round-34 run-6 instrument registry` → `D4_section_missing`.
- **D-1 partial** — `assimilation/census-start.txt` exists (rows=106, EXIT=0, W04) and content passes, but no `corpus/SOURCES.md` change exists after base yet → `D1_no_sources_change_after_base` (order check activates once C1 lands S125/S129 rows).

## Limits

- Synthetic green commit is a proof-of-instrument, fabricated in the /tmp clone; it is not claim data and satisfies no production requirement.
- No lane production/corpus/counter/plan/VCS files were written; only this report. No `find`/`du` under `/fast/scratch`; no delegation; no Pacman changes; no VCS mutation of the lane.
- Receipts: `/tmp/r35w1-c2-base-red-receipt.json`, `/tmp/r35w1-c2-head-red-receipt.json`, `/tmp/r35w1-c2-green-receipt.json`, `/tmp/r35w1-c2-red-mut-receipt.json` (scratch, not lane files).
