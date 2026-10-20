# SkillRegistryDraft — kaidoku round 19, w1 (read-only seat)

Seat: `KaidokuR19.SkillRegistryDraft`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Baseline observed: `git rev-parse refs/heads/main` = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (matches `.ufo/waves/round-19/contract.md:4`). Lane status (`git --no-optional-locks status --short`): only `?? .ufo/waves/round-19/w1/`. `git diff --stat 8a8da7e… -- SKILL.md corpus/lessons/round-18-verifier-spotcheck.md` is empty, so the working copies equal baseline.
Installs or updates: none. Only stdlib `python3 -I -B`, `git` (read-only), and `grep`/`sed` were used.
Lane writes: this report only. Temporary files were written under `/tmp` and removed.

## Scope

Assignment: draft SKILL.md registry text for `pins` and `go-buildinfo-probe` (R18-REGISTRY-PINNED, `corpus/lessons/round-18-verifier-spotcheck.md:198`) and new rows `routed-r18`, `province-pins`, `wave-outcomes`. Layout follows the existing rows (`SKILL.md:535`, `:584`).

## Findings

Observation (O) and inference (I) are labelled.

**F1 (O). Current rows.** The `pins` row is `SKILL.md:542`. Its pinned clause reads "Pinned values: none (no expected digests; …)" and names no path. The `go-buildinfo-probe` row is `SKILL.md:545`. Its pinned clause reads "the build-info magic and header constants of go1.25.0 …" and names no path. Neither row has a backticked `.ufo/` or `corpus/` token in its pinned clause.

**F2 (O). The gate checks the token, not the path.** `.ufo/waves/round-18/tools/routed-defects.py:62-63` sets `REGISTRY_SCOPED` to include `pins` and `go-buildinfo-probe`. `_scope_cell_ok` (`routed-defects.py:660-661`) requires only the substring `Pinned values:` in the 5th cell. It then requires at least 3 words after `Write scope:` and that each backticked `.ufo/` or `corpus/` token exists at REV. Running that function on the baseline rows returns True for `pins` (38 words) and `go-buildinfo-probe` (20 words). Command: `_eval` cell "Simulate registry gate on draft rows", which imports `routed-defects.py` from the baseline blob into `/tmp` and calls `_registry_rows` and `_scope_cell_ok`. This matches the lesson's "the gate checks only the token" (`round-18-verifier-spotcheck.md:198`).

**F3 (O). Path tokens must be bare.** `_exists` (`routed-defects.py:97-98`) runs `git cat-file -e REV:<token>`. A token such as `.ufo/…/tool.py:30-48` therefore fails. The draft keeps every line anchor outside backticks.

**F4 (O). Verified constants for the drafted rows.**
- `.ufo/waves/round-17/tools/pins.py:34` is the only module-level assignment matching `^[A-Z_]+\s*=` (`_CHUNK = 1 << 20`). No 40-hex or `sha256 =` literal exists in that file. This supports "no expected digest, path or constant" in the drafted `pins` row.
- `.ufo/waves/round-17/tools/buildinfo-probe.py:30` is `MAGIC`. Lines 32-33 are `ALIGN = 16` and `HEADER_SIZE = 32`. Lines 43-48 are the flag masks. Line 170 is the PT_LOAD `W&&!X` fallback (`(p["flags"] & 0x3) == 0x2`).
- The go1.27.3 removal is carried from the row and the round-17 lesson. `corpus/lessons/round-17-verifier-spotcheck.md:102` records the go1.27.3 `return 0, errNotGoExe` at line 411. `corpus/SOURCES.md:30` (S024) says the same lines exist in go1.27.3. I did not re-fetch upstream, so the removal is not re-verified this round.

**F5 (O). New-tool paths are absent at baseline.** `git ls-tree -r --name-only 8a8da7e… -- .ufo/waves/round-19/tools` returned nothing. `git cat-file -e` returns 128 for `routed-r18.py`, `province-pins.py` and `wave-outcomes.py`. The planned specs are `.ufo/waves/round-19/gen-wave1.py:45-63` (routed-r18), `:132-138` (province-pins) and `:173-177` (wave-outcomes). Their entry commands can only be exercised at the delivered revision.

**F6 (O). province-pins: stated against live pins.**
- Stated, from `PROVINCE.md:16` (Devin `rea-agents@6.5.0`), `PROVINCE.md:17` (OMP `rea-agents@6.5.0`) and `PROVINCE.md:18` (Kimi `rea-agents@6.7.0`).
- Live, from `grep -o 'rea-agents@[0-9.]*'` on `~/.config/devin/mcp_config.json`, `~/.omp/agent/mcp.json` and `~/.kimi-code/config.toml`. Only the tokens were printed: 6.7.0, 6.7.0 and 6.7.0.
- Result: 2 mismatches (Devin, OMP). This matches the expectation in `.ufo/waves/round-19/claims.json:20`.

**F7 (O). wave-outcomes: the record and the seat count.**
- No round-18 outcomes file exists at baseline. The only round-18 registration files are `wave1-registration.json` and `wave2-registration.json`. Rounds 16 and 17 have outcomes files. `SCORECARD.md:2404-2405` names `wave-outcomes.json` as a record.
- Name matching the round-18 wave-2 registration (`members`: 98 keys) against `.ufo/waves/round-18/w2/*.md` (94 files, 0 extra) leaves 4 seats without a same-name report: GatePRODUCERREV, GateSUMSRUNLOG, TruthREGISTRY, ShonenLines. This matches the expectation at `gen-wave1.py:177` ("expected 4").
- Conflict (O): the lesson lists DecisionRuleApply among the seats with no report (`corpus/lessons/round-18-verifier-spotcheck.md:197`). `.ufo/waves/round-18/w2/DecisionRuleApply.md` exists (31742 bytes, first line `PARTIAL`). So a file-presence definition of `report_present` does not count it as missing (I).

**F8 (I). Kind decisions.** `claims.json:19` calls province-pins a "pin-drift probe". The draft uses `gate` because `--strict` exits 1 on mismatch, which is the gate convention in the protocol rows (`SKILL.md:542` note, "PROTOCOL row kinds are gate or probe"). wave-outcomes is `gate` for the same reason. The L1 should confirm both.

**F9 (I). invocation-audit.** Rows whose entry commands are not exercised at the baseline must be labelled as unexercised variants. The round-18 open list says `invocation-audit` counted unlabelled new rows (`corpus/lessons/round-18.md:91`). The L1 should exercise the three new entry commands at delivery or add the label.

## Draft

Placement (L1 integrates; the lane is not edited by this seat):
- `pins` replaces the whole line at `SKILL.md:542`. Only the pinned clause differs from the current row.
- `go-buildinfo-probe` replaces the whole line at `SKILL.md:545`. Only the pinned clause differs.
- The three new rows go after `SKILL.md:593` under a new heading `## Round 19 — registry rows (draft)`, with the header `| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |` (the round-18 header at `SKILL.md:584`).

```
| pins | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/pins.py compare <PRE> <POST>`; 0 equal, 1 differ (names paths), 2 unreadable or invalid snapshot; `snapshot --out <FILE> <PATH>` writes one map | same command with `--selftest` (mutated-file red case) | Pinned values: none, and no persisted baseline: `.ufo/waves/round-17/tools/pins.py` holds no expected digest, path or constant (each entry records sha256, size and mtime_ns at the instant read). Identical bytes at two instants only, never continuity. Write scope: `snapshot --out FILE` writes `FILE.tmp` then replaces FILE (no no-clobber check); `compare` writes nothing; `--selftest` writes only a removed mkdtemp tree. Kind corrected from `tool` to `probe` in round 18 (R17-REGISTRY; PROTOCOL row kinds are gate or probe) |
```

```
| go-buildinfo-probe | probe / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py <PATH>`; 0 emitted (`found:false` when no magic), 2 unreadable or malformed ELF | same command with `--selftest` | Pinned values: constants in code, no baseline file: `.ufo/waves/round-17/tools/buildinfo-probe.py` holds the go1.25.0 `debug/buildinfo` magic (line 30), header constants (lines 32-33), flag masks (lines 43-48) and the writable-segment PT_LOAD fallback (line 170) that go1.27.3 removed (S024, corpus/SOURCES.md row 30; carried from the prior row, not re-verified); cross-check with `go version -m`. Write scope: none, one read of the target, JSON on stdout, never executes it; `--selftest` writes only a removed mkdtemp fixture tree |
```

```
| routed-r18 | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/routed-r18.py --root <LANE> --rev <REV> --strict`; 0 all seven R18 routed defects closed (named correction and substance both pass), 1 any open, 2 could-not-evaluate; without `--strict` 0 reported | same command with `--selftest` (open fixture, closed fixture, token-only red case) | Pinned values: the seven defect definitions in the script and the routed list at corpus/lessons/round-18-verifier-spotcheck.md lines 193-199; the round-18 receipt and validator-digest inputs under `.ufo/waves/round-18/runs` and `.ufo/waves/round-18/evidence/validate16/summary.json`. Write scope: none in the lane; Git objects at REV only; REV tools and receipts extracted into removed mkdtemp trees; `--selftest` writes only removed mkdtemp repos |
```

```
| province-pins | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/province-pins.py --root <LANE> --rev <REV> --strict`; 0 no mismatch between PROVINCE.md stated client REA pins and live client configs, 1 any mismatch (client, stated and live version named), 2 could-not-evaluate | same command with `--selftest` (fixture configs via env overrides) | Pinned values: none persisted; stated pins are parsed from PROVINCE.md at REV (Git object), live pins from ~/.config/devin/mcp_config.json, ~/.omp/agent/mcp.json and ~/.kimi-code/config.toml, printing only the rea-agents@X.Y.Z token, file sha256 and mtime. Write scope: none; reads the three client configs and Git objects at REV, never writes a config; `--selftest` writes only a removed mkdtemp tree |
```

```
| wave-outcomes | gate / kaidoku | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/wave-outcomes.py --registration <WAVE_REGISTRATION> --report-dir <DIR> --causes <CAUSES_JSON> --out <OUT_JSON>`; 0 every seat has a report or a non-empty cause, 1 a seat without a report has no non-empty cause, 2 unusable input | same command with `--selftest` | Pinned values: none; the registration is read in the round-18 `wave2-registration.json` shape (`members` keyed by seat name), a seat's report is `<DIR>/<seat name>.md`, and the causes file is a per-run input. Write scope: writes only the `--out` JSON; reads the registration, `<DIR>` and the causes file; `--selftest` writes only a removed mkdtemp tree |
```

## Gate simulation (read-only, baseline)

Command: `_eval` (py) cell "Simulate registry gate on draft rows". It loads `routed-defects.py` from `8a8da7e…` into `/tmp` and runs `_registry_rows` and `_scope_cell_ok` against `LANE`, rev `8a8da7e…`.

| Row | Result |
|---|---|
| baseline `pins` (SKILL.md:542) | True, 38 words, scoped paths exist |
| baseline `go-buildinfo-probe` (SKILL.md:545) | True, 20 words, scoped paths exist |
| draft `pins` | True, 38 words, scoped paths exist |
| draft `go-buildinfo-probe` | True, 20 words, scoped paths exist |
| draft `routed-r18` | True, 24 words, scoped paths exist |
| draft `province-pins` | True, 22 words, scoped paths exist |
| draft `wave-outcomes` | True, 20 words, scoped paths exist |

The gate passes on the drafted rows at baseline. Their entry-column paths to the three round-19 tools are not gated, and they are absent at baseline (F5). The baseline gate also passes the old `pins` and `go-buildinfo-probe` rows (F2), so the substance that R18-REGISTRY-PINNED asks for is a naming check, not the token check. That naming check is for routed-r18 to implement, as its own substance step. It would fail the baseline rows because neither pinned clause names a `.ufo/` or `corpus/` path (F1) and pass the drafted ones (I).

## Sources for draft factual sentences

| Draft sentence | Source |
|---|---|
| pins pinned clause: no expected digest, path or constant | `.ufo/waves/round-17/tools/pins.py:34` is the only module-level assignment; no 40-hex or `sha256 =` literal (eval output, F4) |
| pins: each entry records sha256, size and mtime_ns | baseline row `SKILL.md:542`; `.ufo/waves/round-17/tools/pins.py:1-12` docstring |
| pins: kind corrected in round 18 | `SKILL.md:542` (carried text) |
| go-buildinfo: magic (line 30), header constants (32-33), flag masks (43-48), PT_LOAD fallback (170) | `.ufo/waves/round-17/tools/buildinfo-probe.py:30,32,33,43-48,170` (`grep -n`, eval output) |
| go-buildinfo: go1.27.3 removal | carried: `SKILL.md:545`; `corpus/SOURCES.md:30`; `corpus/lessons/round-17-verifier-spotcheck.md:102` (not re-verified upstream) |
| go-buildinfo: cross-check with `go version -m` | `SKILL.md:545` (carried) |
| routed-r18: seven defects at lines 193-199 | `corpus/lessons/round-18-verifier-spotcheck.md:193-199`; `.ufo/waves/round-19/gen-wave1.py:45-47` |
| routed-r18: validator digest input at `validate16/summary.json` | `.ufo/waves/round-18/evidence/validate16/summary.json` exists at baseline (`git cat-file -e`, rc 0); `corpus/lessons/round-18-verifier-spotcheck.md:194` |
| routed-r18: round-18 receipts under `runs` | `.ufo/waves/round-18/runs` exists at baseline (`git cat-file -e`, rc 0); `.ufo/waves/round-19/gen-wave1.py:50` |
| province-pins: stated pins | `PROVINCE.md:16,17,18` (`grep -n 'rea-agents@'`) |
| province-pins: live pins, token only | `grep -o 'rea-agents@[0-9.]*'` on the three configs; output `rea-agents@6.7.0` once per file; `.ufo/waves/round-19/gen-wave1.py:134-137` |
| province-pins: 2 mismatches expected | `.ufo/waves/round-19/claims.json:20` |
| province-pins: `--strict` exit 1 on mismatch | `.ufo/waves/round-19/gen-wave1.py:137-138` |
| wave-outcomes: registration `members` keyed by seat name | `git show 8a8da7e…:.ufo/waves/round-18/wave2-registration.json` (98 members; `python3 -I -B`) |
| wave-outcomes: 4 seats without a same-name report | same command: 94 report files at `.ufo/waves/round-18/w2/`, 0 extra; missing GatePRODUCERREV, GateSUMSRUNLOG, TruthREGISTRY, ShonenLines; `.ufo/waves/round-19/gen-wave1.py:177` |
| wave-outcomes: no round-18 outcomes file | `git ls-tree -r --name-only 8a8da7e… -- .ufo/waves` (only round-16/17 outcomes; round-18 has registration files only) |
| wave-outcomes: `wave-outcomes.json` is a named record | `SCORECARD.md:2404-2405` |
| DecisionRuleApply has a report | `.ufo/waves/round-18/w2/DecisionRuleApply.md` (`git cat-file -s`: 31742; first line `PARTIAL`) |
| routed-r18 gate convention | `.ufo/waves/round-18/tools/routed-defects.py:62-63,97-98,644,660-661` |

## Open for the L1

1. Integrate the two replacements (`SKILL.md:542`, `:545`) and the appended block after `SKILL.md:593`.
2. The R18-REGISTRY-PINNED named correction must go in `SCORECARD.md` and `corpus/lessons/round-19.md` (`routed-r18` check (a)). This seat did not write either.
3. Decide the kind of province-pins (F8). Exercise the three new entry commands at delivery, or label them as unexercised (F9).
4. The lesson's DeadSeat list includes DecisionRuleApply, which has a PARTIAL report at `.ufo/waves/round-18/w2/DecisionRuleApply.md` (F7). The R18-DEADSEAT-RECORD fix should reconcile this.
5. The go1.27.3 removal claim for PT_LOAD fallback (F4) is carried, not re-verified upstream.
