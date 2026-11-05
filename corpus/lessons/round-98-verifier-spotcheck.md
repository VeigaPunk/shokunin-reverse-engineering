# Round 98 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: kaidoku round 98. Base `d0aebc288621b0072ac3eb2a79a62ad26bfa837a` → final `f6cdcabc1e53bee7c22a6161da5facb818103b54` (branch `main`).
Report: fleet `.ufo/reports/round-98/kaidoku.md`. Prompt: fleet `.ufo/prompts/kaidoku-round-98.md`.
Driver digest (copied from the mutable `.ufo/watchdog.log`):
`2026-11-05T17:49:07-03:00 launch kaidoku round=98 pgid=2897017 driver=hyaku-inline attempt=1`;
`2026-11-05T18:29:57-03:00 complete kaidoku round=98; hyaku-inline attempt=1`.
All commands below were run by this verifier on 2026-11-05, with the outputs observed in that session.

## 1. Conformance (PROTOCOL §Round-robin closure step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H %ci' -- .ufo/reports/round-98/kaidoku.md` | `kaidoku-shokunin 9028b80ea812f51296c059eeb47efabd9e869974 2026-11-05 18:29:13 -0300` (the final lane commit is 18:27:45, so the report was filed after its commits) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines (boxes 1–3 `[~]`, box 4 `[ ]`) | pass |
| cited commits exist and are ancestors of `refs/heads/main` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> refs/heads/main` for d0aebc28, 69c581c7, 72346895, 9cb93001, f6cdcabc | `commit` ×5; ancestor ok ×5 | pass |
| lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …/kaidoku-shokunin`; `git status --porcelain` | `branch=main local=f6cdcabc… remote=f6cdcabc… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/main` → `f6cdcabc…` | pass |
| prompt carries template contract | line-by-line comparison of `kimi-shokunin/templates/round-prompt.md` (140 lines, with `{{FLEET_ROOT}}/{{LANE}}/{{ROUND}}` substituted) against prompt lines 1–140 | 2 differing lines only: line 1 (`<{{LANE}}-repo>` → `kaidoku-shokunin`) and line 6 (`{{AXES}}` → `coverage + depth + calibration (reverse engineering with REA)`, which equals `shokunin.conf:45`); §6 hyaku addendum follows from line 141 | pass |

Conformance defects (status-neutral):
- **D1 · new gates are not registered at the registry home.** `tools/round-98/pe-upx-tamper-battery.py`, `tools/round-98/allowlist-check.py` and `tools/round-98/stop-boundary-repair-battery-v8.py` have no row in `SKILL.md` `## Local round-evidence gate registry` (line 940). `awk 'NR>=940' SKILL.md | grep -o 'tools/round-9[0-9]/[a-z0-9.-]*' | sort -u` lists round-90 to round-96 tools only, so the round-97 and round-98 counters are also missing. Under PROTOCOL §Gate standard (Delivery), no gate is graded conformant until its row exists. Claims were evidence-verified regardless (§2).
- **D2 · the v8 selftest tally is seat prose, not a committed raw output.** `SELFTEST cases=24 failures=0` appears only in `w1/ExecReproC2.md:13` and `w1/ScribeEntry.md:29`. No committed `--selftest` output file exists for v8, in contrast to `pre/c1-v4-selftest.txt` in round 94.
- **D3 · a dead seat.** ReviewerRepair ended without a report (M98-f), and the lane recorded this itself.

## 2. Claims

### R98-C1 — coverage (frontier → core; capability)

The claim rests on a lane-owned gate, so it was **evidence-verified** under §Gate standard (Closure consequence) and **independently re-measured** on carriers the lane never used. The sibling gate was not executed.

- Frozen counter integrity: `git show <r>:tools/round-98/pe-upx-tamper-battery.py | sha256sum` at 69c581c7, 72346895 and f6cdcabc gives `a34d1253e75e98d4fbb66abe139d2c374a8332f8b6ca1bc8e4afea8dbf4feee8` all three times. This equals `counter_sha256` in all three receipts.
- Receipts (`jq` over committed bytes):
  - `pre/c1-identity-control.json`: rev d0aebc28, exit 1, `recovered 0 of 18; intact 6 of 6; refused 0 of 2; effective 18 of 18`. Its `repair_sha256 d8b7d4de…` equals `sha256(controls/identity-copy.py)`.
  - `pre/c1-r87-control.json`: exit 1, `recovered 0 of 18; intact 0 of 6; refused 2 of 2; effective 18 of 18`. Its `repair_sha256 96da7d8e…` equals `sha256(tools/round-87/upx-magic-repair.py)`.
  - `l1/scores/c1-at-72346895….json`: rev `72346895a35a74af18151b125934fa0c09fe1e3c`, exit 0, `met true`, `recovered 18 of 18; intact 6 of 6; refused 2 of 2; effective 18 of 18`. Its `repair_sha256 2fa1102d…` equals `sha256` of `upx-pe-repair.py` at 72346895 and at f6cdcabc.
  - All three match the report.
- **Independent re-measure (held-out, not the lane's gate).** I took three PE32+ carriers that appear in neither the frozen six nor ExecHeldOut's set: Ghidra `lzfse.exe` (sha256 `6ea4781fee28…`, 223744 B), Ghidra `pdb.exe` (`744c4bc0a664…`, 76288 B) and orca `win32-x64/…/winpty-agent.exe` (`0c4834a0ab2a…`, 307712 B).
  - Steps per carrier: `upx --best -q -f -o packed`; ref = sha256(`upx -d` of packed); then three tampers — magic (first `UPX!` → 00000000), names (sections 0/1 → `.text`/`.data`), both.
  - For each tamper: `upx -t` of the tampered file, then `python3 -I -B tools/round-98/upx-pe-repair.py --in tam --out rep`, `upx -t rep`, and sha256(`upx -d rep`) compared with ref.
  - Observed for all 9 cells: tampered `upx -t` rc 1, repair rc 0 (`ok magic@992` / `ok name0,name1` / `ok magic@992,name0,name1`), post `upx -t` rc 0, unpack == ref. That is **9/9 recovered**.
  - The PackHeader was again at offset 992 on all three carriers, so this re-measure does **not** cover the one-layout limit CriticC1 named.
- Coverage-map and corpus re-measure. Over committed bytes, I counted the `corpus/knowledge/*.md` stems that are mentioned in `corpus/README.md` outside their own index row:
  - d0aebc28: 181 entries, 175 mapped. f6cdcabc: 182 entries, 176 mapped. Both equal the lane's 175/181 → 176/182.
  - The new entry has a coverage-map row (`corpus/README.md:134`), an index row (`:279`) and a frontier note (`:397`).
  - It opens with the provenance trio and `source: S324`. S324 is `mined`, with `used-by` = the entry.
- **Verdict: coverage `improved`** (verified; both the frozen predicate and the held-out re-measure pass).
- Named limit, carried rather than ruled against: the frozen battery admits the CriticC1 forgeries f2/f7/f1h because every carrier sits at offset 992. The capability row and frontier note are scoped to the six pinned carriers, so the claim does not overreach.

### R98-C2 — calibration (round-97 routed defect 1)

- Frozen counter integrity: `allowlist-check.py` sha256 is `c8106aff…` at 69c581c7, 72346895 and f6cdcabc. v8 sha256 is `7a983746…` at 72346895 and at f6cdcabc.
- Receipts:
  - `pre/c2-v7-control.json`: exit 1, `legs passed 1 of 4; public 0; real14 0; stub9 0; extra 1`. `public_stderr` holds `counts-extra-key:` for fresh_far, fresh_far_refused, fresh_repaired, refused and silent.
  - `l1/scores/c2-at-72346895….json`: exit 0, `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1`. `public_stdout` is `selfverify ok=True reasons=0 … met True exit 0`.
- **Independent re-measure of the substance.** I parsed the keys of v3.score's `counts = {…}` block (`tools/round-93/stop-boundary-repair-battery-v3.py` ≈ lines 291-305) and v8's `COUNT_KEYS`. Result: 14 = 14, set equality True, symmetric difference empty.
- The v7→v8 diff (`git diff --no-index` of both files at 72346895) is 28 insertions and 8 deletions. All of them fall in the docstring, `TOOL`, `COUNT_KEYS`/`NINE_LABEL_KEYS`, the selftest fixture, the new `verify-catches-nine-key-stub` case and the selftest scratch default. This matches the report.
- Round-97 routed defect 1 (`round-97-verifier-spotcheck.md:73`, "COUNT_KEYS must equal the verdict's 14-key set, with a red fixture for the nine-key stub") is satisfied: the key set is equal, the `stub9` leg is in place and the selftest case exists.
- **Verdict: calibration `improved`** (verified).
- Limit carried: the public leg trusts printed stdout (CriticC2 F2/F3/F5, MutationC2 M6).

### Harm check (owned axes coverage, depth, calibration)

- `git diff d0aebc28 f6cdcabc -- SCORECARD.md` is additions only: one capability row and the round-98 section. No axis score row was edited.
- Depth proxy: the committed `coverage-selfcheck` receipts give `recipe_a.rule_blocks 36` and `citation_resolved_rules 36` at both d0aebc28 and 9cb93001. SKILL.md is unchanged. **Depth: `unchanged`.**
- Coverage: 175/181 → 176/182 (9.67 both), not harmed. Calibration: no regression.
- Pre-existing stale coverage head (`10.0`, 168/168 vs observed 175/181): the lane found it, recorded it in the SCORECARD round-98 section and routed it. It is marked, so this round did not harm calibration.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1: receipts verified, held-out 9/9 re-measured, 175/181 → 176/182 recount |
| calibration | improved | C2: receipts verified, 14-key set equality re-measured |
| depth | unchanged | rule blocks 36 → 36 (committed receipts); SKILL.md unchanged |

## 3. Discernment spot-check (LEARNING.md)

| item | lane decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S324 UPX 5.2.0 `src/pefile.cpp` | admit, tier A | `curl -sSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/pefile.cpp` → 127340 B, sha256 `6783a926f339b8fa5051c3c0c105c078655513d96ca4bb0f94c74315911379fa` (equals the row) | agree | Lines 3167-3170 read `if (memcmp(isection[0].name, "UPX", 3) == 0) {` / `// current version` / `fi->seek(isection[1].rawdataptr - 64, SEEK_SET);` / `found_ph = readPackHeader(1024);`. The row's ≤25-word quote (whitespace collapsed) is present at the stated lines. Lines 2643-2652 confirm the pack-time `UPX0`/`UPX1`/`.rsrc`-or-`UPX2` naming. The packer's own source is tier A for this scope. |
| S325 "Unpacking Modified UPX" (hardlyprogramming) | reject, tier C | `curl -sSL https://blog.hardlyprogramming.com/posts/Unpacking-Modified-UPX/` → 45767 B, sha256 `f1b7c347472973e2f55f7818eb6fcfbbcfa6859a75aa41ee87da67d634e1e402` (equals the row) | agree | The 22-word quote is present verbatim after tag-strip. The text goes on "I decided to forego this and opted to manually unpack the sample". In the stripped text, `UPX0`, `UPX!`, `section`, `magic` and `header` each occur 0 times, while x64dbg occurs 2 times and OEP 3 times. The page therefore names no tampered field and cannot ground a structural repair. |
| ScoutSources drafts (not appended) | reject (duplicate URL / uncited) | `sources-census.sh validate` W04 list | agree | The census lists no new W04 for S324/S325. Appending same-URL rows for packhead/pefile would have added duplicates. |

New `corpus/SOURCES.md` row re-opened: S324 (quote and lines checked above; `used-by` resolves to `corpus/knowledge/2026-11-05-r98-pe-upx-tamper-repair.md`).
Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `kaidoku ok`. Only W04 duplicate-URL warnings appear, none on S324/S325.
Row count by `grep -cE '^ {0,3}\| *S[0-9]{3,}'`: 228 at d0aebc28 and 230 at f6cdcabc.
Spot-check verdict: agree on the admit and on the reject.

Side check M98-a: `test -e /home/vgpnk/Projects/shokuknow/merge/kaidoku; echo $?` → `0`. This confirms the lane's own correction of the false absence statements from rounds 93–97.

## 4. Trends

- **expansion: improved.** A new knowledge entry sits on ground that was Frontier at base: the round-92 "PE … packed inputs" note now has a coverage-map row. It cites the `mined` S324, and a capability row was added. The held-out re-measure confirms the capability runs.
- **quality: improved.** The round-97 calibration-harmed counter is superseded by v8, verified above. The new entry's limits are marked in the entry: truncated `ok intact` at line 73, offset-992 population at line 61, and the forgeries. No admitted entry failed my re-check.
- **discernment: improved.** The outside spot-check agrees with the gate on one admit and one reject. The lane also mined its own false absence statement (M98-a) into QUALITY Row 198, and that row is shown able to fail.

## 5. Routed defects (lane must fix next round)

1. D1: register `pe-upx-tamper-battery.py`, `allowlist-check.py` and `stop-boundary-repair-battery-v8.py`, plus the round-97 counters, in `SKILL.md` `## Local round-evidence gate registry`. Each row needs gate/probe class, verdict map, self-test spelling and pinned values.
2. D2: commit raw `--selftest` outputs for v8 (and v7) as files rather than citing seat prose.
3. Successor counters must carry the wave's forgeries as committed red fixtures before freeze (CriticC1 f2/f7/f1h; CriticC2 F2/F3/F5; MutationC2 M6). They also need a carrier whose PackHeader is not at offset 992. This verifier's three held-out carriers were also at 992.
4. `upx-pe-repair.py` reports `ok intact` (exit 0) on a pack truncated to ≥ c_len. There are also three rc-1 CLI crash paths. Make exit 0 imply `upx -t` would pass, or refuse.
5. The stale coverage head (`10.0`, 168/168 vs 175/181 → 176/182) and the six unmapped r93–r97 entries.
6. Round-97 defects 2–5 and 7 are still open. Defect 2 was absent from the plan's not-claimed list (ReviewerV8 F2).

## 6. Operator note (promotion is operator-owned)

- SHONEN boxes 2 and 3 look checkable by a non-author. This verifier ran an end-to-end pack → tamper → repair → `upx -d` task on held-out carriers, using only the tool's committed usage line (§2).
- Box 1 (SKILL.md) was not edited this round and was not checked. Box 4 was untouched.
- Nothing was written to SHONEN.md.
