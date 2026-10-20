PARTIAL

# LogAudit — LOG.md round-18 entry at REV (wave 2, falsify)

Seat `KaidokuR18.LogAudit` (author-side advisory reviewer). I worked read-only, and this file is the only lane write.
REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline B `9011581d84527ba34c675f9cf912e54d2e72d470`, freeze F `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
Target: `LOG.md:2125-2167` at REV. Every anchor below is `git show REV:<path>` unless marked otherwise.
Axes: calibration (do the numbers and wording match the evidence?), operability (can a reader rerun each claim?), depth (does the substance reproduce, beyond the citation?).
I ran no REA, Ghidra, or carrier execution, no jj, and no git writes. I installed nothing. I removed my scratch files under `/tmp` (`kr18-logaudit-*`).

## Verdict by acceptance item

| Item | Verdict | Basis (observation) |
|---|---|---|
| Append-only vs B | **HOLDS** | `44 0 LOG.md`. B's 139,886 bytes (2,123 lines) are a byte prefix of REV. F did not touch LOG; F→REV is `44 0`. |
| Seat counts and role mix | **HOLDS** | 89 spawn / 89 registry / 89 tasks / 89 `.md` reports, with names 1:1. The role mix equals `LOG.md:2133-2134` exactly. |
| Every claim cites evidence | **PARTIAL** | Every claim I checked reproduces. But M1 is an undisclosed instrument change, and L1–L6 are uncited, misanchored, or overreaching lines. |

## Findings (by severity)

### M1 — An undisclosed post-freeze edit to the C1 counter flips R17-PINMAP from open to closed (calibration)
- **Observation.** `routed-defects.py` changed in REV, after F, with `9 4` lines. The substance check went from `"mid_map_mismatch" in code` (F `.ufo/waves/round-18/tools/routed-defects.py:278`) to requiring both `mid_map_sha256_mismatch` and `mid_map_compare_mismatch` (REV `:277-283`; the check itself is at `:282-283`).
- **Observation (reproduced).** Run at REV, the F-version tool gives `open_count 1`, with R17-PINMAP open on `receipt-validate-mid-finding`. The REV tool gives `open_count 0`. At B, the REV tool gives `open_count 6`.
- **Observation.** The entry never mentions the edit:
  - The "Tool changes" bullet (`LOG.md:2140-2149`) lists only r17 tools and gates.
  - "Landed in this commit" (`LOG.md:2162-2167`) omits it.
  - `git grep routed-defects REV -- LOG.md SCORECARD.md` finds nothing. `corpus/lessons/round-18.md` mentions the tool but not this edit.
- **Observation.** The in-code justification points at "contract.md's placeholder `mid_map_mismatch`". But `contract.md` at REV contains no `mid_map` at all (grep exit 1), and `wave1-dispatch.json` contains it 0 times. The token originated in the tool itself, at F `:278`.
- **Inference.** The edit is a plausible correction: it aligns the check to the validator's real ids, and it is arguably stricter. But the next entry's C1 "6 → 0" depends on an instrument change made in the same delivering commit. The audit trail has to say so.

### L1 — `LOG.md:2148-2149` "All old outputs reproduce (16 / 8 / 8)" cites no evidence, and nothing is retained at REV (citation)
- **Observation.** The line gives no path. The tree under `.ufo/waves/round-18/evidence/` holds no log-extract, compare, or receipt-replay record. The only support is wave-1 seat prose from `/tmp` runs (`w1/LogExtractEof.md:70,100,103`, `w1/CompareEofFields.md:52`, `w1/CarrierRunMidMaps.md:165`). This is the same class as R17-VALIDATE16, which the entry discharges at `:2159`.
- **Observation (independent reproduction).** The substance **holds** at REV:
  - Logs: 16/16 have old fields equal between B and REV `log-extract.py`, with every exit 0/0. The new keys are exactly `eof_reads`, `invalid_index_reads` and `symbol_analysis_failures`.
  - Compare: 8/8 REV `compare.py` outputs are byte-identical to the retained `runs/*/compare.json`.
  - Receipts: 8/8 r17 receipts exit 0 under the REV validator without `--require-mid-maps`.

### L2 — `LOG.md:2161` "`d0ab299` verified them" overstates for pass 1 and cites no evidence (calibration)
- **Observation.** r17 `verification.json` has `source_revision` d0ab299. Its 8 `receipt-validate-*` runs target working-tree `runs/<label>/receipt.json`. All 8 pass-1 receipts at `da64646` differ from the d0ab299 bytes (`git diff --quiet` loop: 8/8 differ). So d0ab299 validated pass 2 only.
- The pass-1 receipts were validated only in round 18 (`:2159`). The appended r17 correction states this precisely: "d0ab299 … is the verification revision, not a producer" (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:206`). The LOG line neither matches nor cites it.
- **Observation.** The producer attribution itself holds by bracketing:
  - 2711674 at 10:46:45-03:00 is followed by pass 1 at 10:47:42–11:00:05, with no commit in between.
  - 95e34db at 11:27:35 is followed by pass 2 at 11:27:41–11:40:02. Only d0ab299, at 11:47:24, follows.
  - The blobs are `bc964ac` and `c536e3e` respectively.

### L3 — `LOG.md:2164` "README Go row token (in place, line 35)" names the wrong file (anchor)
- **Observation.** The root `README.md` at REV has 24 lines, and B→REV leaves it unchanged. The edited file is `corpus/README.md` (`1 1`). `corpus/README.md:35` contains `2026-10-20-r18-swiss-map-replay`.

### L4 — `LOG.md:2162-2167` "Landed in this commit" is incomplete (completeness)
- **Observation.** F→REV non-run files include four that the list omits:
  - `corpus/lessons/round-18.md` (`75 0`);
  - `SCORECARD.md` (`14 0`);
  - `routed-defects.py` (M1);
  - an **in-place** edit at `corpus/SOURCES.md:48` (hunk `@@ -44 +48,3 @@`), where S032 was dropped from the "Go carrier route diagnosis" path.
- "SOURCES S033–S036" reads as append-only, but SOURCES is `11 1`.

### L5 — `LOG.md:2128-2129` range `:137-147` does not contain "one partial outside disagreement" (anchor)
- **Observation.** `round-17-verifier-spotcheck.md` mentions "partial" only at `:108` (the "partial disagree" row) and `:131`. Range `:137-147` holds just the six routed defects. R17-PINMAP at `:137` covers the same substance, but not the disagreement record.

### L6 — `LOG.md:2135,2138` "before any measurement" and "a scope rule written before measuring" overreach, and the cited timestamp contradicts itself (calibration)
- **Observation.** The critics measured before the amendments, and their measurements were the reason for them:
  - `w1/CriticC2.md:18` (A1): the prototype lint gives 8 live, or 6, at B.
  - `w1/CriticC1.md:33`: a token-only commit gives `open_count 0`.
  - The amended rule's seat-dir exclusion is what moves 5 to 3 (`w1/HeadRevLintTool.md:123-124`).
- **Observation.** The cited `claims.json` amendment says `"at": "2026-10-20T13:25:00-03:00 (after wave 1, before any round-18 REA run)"` (`claims.json:35`). But:
  - F, which already contains that amendment, was committed at 13:23:55-03:00 and pushed at 13:23:57 (origin/main reflog);
  - the first REA run started at 13:24:07 (`runs/run-log.txt:2`);
  - `contract.md:148` dates the same amendments "~12:40 -03:00".
- **Inference.** The Git commit and push order supports "before any round-18 REA run". The stated `at` value does not support it, and "before any measurement" is too broad.

### Info
- **Phrasing:** `:2156` "the noswiss sibling and all 11 non-diagnostic synthetic carriers" double-counts. `s1246-noswiss-nethttp` is one of the 11 (`decision-rule.json` table, `diagnostic: false`).
- **Uncited in-line but verified:**
  - the wave-1 counts (`:2133-2134`; evidence `wave1-dispatch.json:17,19`, `wave1-result.txt:1` "attempt1", `w1/`);
  - the tool changes (`:2140-2147`; e.g. `citation-drift-probe.py:43-46,314-329`, `custody-pair.py:109-121,410-412`, `round-17/verify.py:11-12,73-83`, `carrier-run.py:7-8,371-372`, `receipt-validate.py:6,33,453-465`, `log-extract.py:14-15,24-32`, `compare.py:192-197`);
  - the `Invalid index` lines (`runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log:451`, `runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:206`, WARN `:68`);
  - "C2's declared 3 came from audit prose" (`corpus/lessons/round-18.md:68`).

## Claim ledger (LOG.md at REV)

| Line(s) | Claim | Evidence checked | Status |
|---|---|---|---|
| 2127 | Baseline 9011581 | commit exists; parent of F | verified |
| 2128-2129 | spotcheck `:137-147`: six defects + one partial disagreement | six at `:137-147`; partial at `:108,131` | misanchored (L5) |
| 2129-2131 | jj audit §5: three HEAD-keyed live pins | `JjAuditKaidoku.md` §5 R1–R3 (verify.py:59, citation-drift L477, custody-pair:327) | verified |
| 2133-2134 | 89 seats, one call, role mix, 89/89 reports | see Seat table | verified, uncited |
| 2135-2139 | critics changed the round; fixes | CriticC1:33, CriticC2:18, CriticC3:9; contract.md:148-151; decision-rule.json | substance verified; ordering wording overreaches (L6) |
| 2140-2147 | tool changes | anchors in Info | verified, uncited |
| 2148-2149 | old outputs reproduce 16/8/8 | my reruns 16/16, 8/8, 8/8 | true; uncited and unretained (L1) |
| 2150-2153 | frozen and pushed at F 16:23:55Z; pass 16:24:07–16:32:10Z; 15× 0/0 | commit 13:23:55-03:00, push 13:23:57; run-log 15× `carrier-run=0 compare=0`, `run-carriers exit=0` | verified |
| 2153-2156 | D results exact; non-D did not fail | compare.json `all_match` 15/15; `Go analysis failure` only in calib-aether, s1246-swiss-nethttp, real-kimi-webbridge; predictions unchanged F→REV | verified |
| 2157 | verdict confirmed under the frozen rule | all `confirmed` clauses (`decision-rule.json:7`) plus the binding gate (`:2`): `--require-mid-maps` 15/15 exit 0, carrier sha256 15/15 equal, prediction blobs unchanged | verified (re-run by me; not retained at REV) |
| 2157-2158 | first intermediate patch fallback | every retained r17 fallback (16 logs) is `→ 1.25.0`; kimi is `1.24.13 → 1.24.6` | verified within retained logs ([INFERENCE] r≤16 retained no Ghidra logs) |
| 2159 | R17-VALIDATE16 | summary.json: 8× exit 0; `validator_sha256` = sha256(B validator); stdout digests match (4/4 sampled); SCORECARD:2364, round-17.md:88,122 contain "all 16" | verified |
| 2160 | R17-SUMS-RUNLOG | da64646 run-log has 7 carriers, no calib-shfmt; shfmt receipt present; line dropped at 95e34db and restored with sha `8ac38afe…` = blob = 2711674 line | verified |
| 2161 | R17-PRODUCER-REV | bracketing commits and blobs | producers verified; "verified them" overstated (L2) |
| 2162-2167 | landed list | numstat F→REV; QUALITY.md:31 (#21); SOURCES.md:39-42; SKILL in-place 448, 528, 540-542, 545 and appended 548, 567 (EOF; B had 546 lines) | partly verified; wrong README path (L3); incomplete (L4, M1) |

## Seat-count reconciliation (observation)

| Source | Count / mix |
|---|---|
| `wave1-dispatch.json:17,19` counts | spawn 89, total 89 |
| dispatch `registry.members` / `taskCall.tasks` | 89 / 89. Roles: executor 19, scout 23, reviewer 15, scribe 10, connector 8, critic 6, revenger 4, sentinel 2, simplifier 2 |
| `wave1-registry.json`, `w1/swarm-registry.json` | 89 each, roles identical to the dispatch |
| `w1/` at REV | 90 entries = 89 `.md` + `swarm-registry.json`. Names 1:1 with the registry (both diffs empty). Smallest report 3,925 B. `w1/` unchanged F→REV |
| registry vs task `agent` roles | 0 mismatches |

## Commands (exit is from the trailing `echo exit=$?`, i.e. the last command of each chain; lane cwd)

```
git rev-parse b2aad08… 9011581… eb6c266…                                   # exit 0
git diff --numstat 9011581… b2aad08… -- LOG.md                             # "44 0 LOG.md", exit 0
n=$(git show B:LOG.md|wc -c); cmp <(git show B:LOG.md) <(git show R:LOG.md|head -c $n)   # PREFIX-IDENTICAL, exit 0
git diff --numstat B eb6c266 -- LOG.md; git diff --numstat eb6c266 R -- LOG.md          # "" / "44 0", exit 0
python3 -I -B -c '<Counter of dispatch registry roles; len(tasks)>'                      # 89 + mix above, exit 0
python3 -I -B -c '<registry names vs w1/*.md stems; registry role vs task agent>'          # [] [] [], exit 0
git ls-tree --name-only R .ufo/waves/round-18/w1/ | wc -l   # 90 (89 .md), exit 0
git show R:.ufo/waves/round-18/runs/run-log.txt             # 32 lines, 15× carrier-run=0 compare=0, exit 0
git reflog show --date=iso refs/remotes/origin/main         # eb6c266 @ 13:23:57 -0300 "update by push", exit 0
git diff --stat eb6c266 R -- .ufo/waves/round-18/predictions/   # empty, exit 0
for L in <15>; do python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $L/receipt.json; done   # 15× exit 0
for L in <15>; do <prediction carrier.sha256 == receipt carrier.sha256_pre == sha256_post>; done   # 15/15, exit 0
for L in <8 r17>; do python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py $L/receipt.json; done   # 8× exit 0
# eval cell: git show {B,R}:.ufo/waves/round-17/tools/log-extract.py to mkdtemp; run both with -I -B --log on
# 8 da64646 + 8 REV r17 ghidra.log blobs; compare old keys -> 16/16 equal, every per-run exit 0/0
(cd .ufo/waves/round-17 && for L in <8>; do python3 -I -B tools/compare.py --prediction predictions/$L.prediction.json \
   --observation runs/$L/observation.json | cmp -s - <(git show R:.ufo/waves/round-17/runs/$L/compare.json); done)   # 8/8, exit 0
git show {R,da64646}:<16 r17 ghidra.log> | grep -o 'Falling back from … to …'   # only 1.25.14→1.25.0, 1.25.8→1.25.0, exit 0
git show B:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum            # 618448829ba6…, equals summary.json:82, exit 0
git log --format='%h %cI %s' -- .ufo/waves/round-17/predictions/SHA256SUMS      # 2711674, 95e34db, b2aad08, exit 0
git log --format='%h %cI %s' 2711674~1..d0ab299                                  # 2711674 10:46:45, da64646 11:06:06, 95e34db 11:27:35, d0ab299 11:47:24, exit 0
for L in <8>; do git diff --quiet da64646 d0ab299 -- .ufo/waves/round-17/runs/$L/receipt.json || n=$((n+1)); done   # 8/8 differ, exit 0
python3 -I -B <F routed-defects.py in mkdtemp> --root . --rev R    # open_count 1 (R17-PINMAP), exit 0
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev R   # open_count 0, exit 0
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev B   # open_count 6, exit 0
git show R:.ufo/waves/round-18/contract.md | grep -n "mid_map"     # no output, exit 1
grep -c "mid_map_mismatch" .ufo/waves/round-18/wave1-dispatch.json # 0
git grep -n routed-defects R -- LOG.md SCORECARD.md corpus/lessons/round-18.md corpus/knowledge/2026-10-20-r18-swiss-map-replay.md   # lesson lines only, exit 0
git show R:README.md | wc -l; git diff --numstat B R -- README.md corpus/README.md   # 24; "1 1 corpus/README.md", exit 0
git diff -U0 B R -- corpus/SOURCES.md | grep '^@@'                 # includes "@@ -44 +48,3 @@", exit 0
git show R:corpus/lessons/round-17-verifier-spotcheck.md | grep -n -i partial   # 108, 131 printed; the chain's trailing exit 128 came from a malformed two-arg `git rev-parse --short` in the same chain, re-run per revision -> bc964ac / c536e3e, exit 0
```

## Residual risk and verification gaps
- **Operability, outside LOG scope (observation).** `.ufo/waves/round-18/tools/__pycache__/routed-defects.cpython-314.pyc` exists, gitignored, with mtime 13:46:17-03:00. `round-18/verify.py:269,281,295` exits 1 when any `__pycache__` exists under `.ufo`, so the L1 verification pass will fail unless it is removed first.
  - **Inference: not mine.** It comes from the selftest's in-process `spec_from_file_location` import (`routed-defects.py:1053-1057`) run without `-B`. All of my invocations used `-I -B`, and none used `--selftest`.
- **Not retained at REV.** The binding-gate runs and the 16/8/8 replays exist only as my reruns and wave-1 prose. The verdict at `:2157` and the line at `:2148-2149` rely on the "next entry" for retained proof.
- **Not checked:** C2 lint numbers, jj-red-before content beyond `all_held: true` and 14/14 expectations, the SKILL row bodies, and the r17 knowledge pass-1 window "13:47:05Z" (`:206`) against the receipts. These fall outside LOG claims or belong to sibling seats.
- **Installs:** none.
