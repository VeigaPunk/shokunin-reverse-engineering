# R38MutC2 — mutation battery on the frozen R38-C2 counter (selftest-level)

Seat R38MutC2, lane kaidoku-shokunin, 2026-10-26. Scope: mutate the frozen
`tools/round-38/c2-counter.py` **in scratch copies only**, run the counter's own
selftest against each mutant, report mutant | class | green? | killed?. The
frozen counter, predicate, carriers and oracles were not changed; findings are
coverage observations for the wave, not repair proposals.

## Method and bounds compliance

- Battery driver: scratch `mutate_c2.py` (script copied into
  `.ufo/waves/round-38/w1/artifacts/R38MutC2/driver-mutate_c2.py`). It reads the
  frozen bytes read-only, applies each mutation as an exact one-occurrence
  string replacement (asserted `count==1` per anchor), writes the mutant under
  `$SEAT_SCRATCH/mut/`, runs `python3 -I -B <mutant> --selftest` with
  `HYAKU_SCRATCH=$SEAT_SCRATCH`, records rc/stdout/stderr/sha256, deletes the
  mutant copy. Selftest fixture repos are created by the counter's own selftest
  (`mkdtemp` + `git -C <d> init -q` + toplevel check before first commit, all
  calls name `-C <d>`).
- No VCS mutation: only read-only git (`rev-parse`, `cat-file`, `status`,
  `log`) on the lane. No tools installed (stock python3 + system git; pacman
  untouched). No subagents, no background jobs, no `agent://all`.
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38MutC2` removed at the end
  (restoration section).

## Detector baseline (pristine)

| probe | result |
|---|---|
| frozen counter sha256 (disk) | `7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7` |
| blob sha256 at freeze `e059ca9:tools/round-38/c2-counter.py` | `7f137b66…` (identical — disk bytes are the frozen bytes) |
| counter at base `77091b49` | absent (`git rev-parse` fatal: not in that tree) — introduced by the freeze commit `e059ca93` "round-38: freeze (…counters + selftests…)", consistent with plans/round-38-claims.md; `git status --porcelain tools/round-38/` = 0 lines |
| pristine copy selftest | rc=0, `{"cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}` |
| pristine counter, do-nothing at base (`--rev base --base base`) | rc=1, `mismatches=1`, `unresolved=[["prov_core:REA MCP server","evidence/doctor/"]]`, `guards_ok=false` — matches the frozen 1-mismatch premise and CTL-C2-0 exit-1 expectation |

Baseline green ⇒ all 15 mutants applied cleanly and every verdict below is
conclusive (a baseline failure would have been inconclusive; none occurred).

## Battery: mutant | class | green? | killed?

"green?" = the `green: repaired by document` case still passed under the
mutant. "killed?" = selftest exited non-zero (any case verdict wrong or crash).
Full per-mutant JSON: `artifacts/R38MutC2/results.json`.

| mutant (exact change) | class | green? | killed? | evidence |
|---|---|---|---|---|
| A1 `resolves`: `return 1 <= lo <= hi <= cache[p]` → `return True` | pointer-resolver (range bound dropped) | yes | **no — SURVIVED** | no fixture passes an out-of-range range through a LANE-matching pointer: the only ranged LANE pointers (`SKILL.md:3-5`, `PROVINCE.md:15-17`) are in range, and the "range beyond file" red uses `docs/x.md:1-9`, which the LANE filter drops in `pointers()` before `resolves()` runs. Existence check is upstream of the mutated line, so `bad_base`/`unrepaired` still fire |
| A2 `resolves`: `p = path.rstrip('/')` → `p = path` | pointer-resolver | yes | **no — SURVIVED** | probed: `git cat-file -e HEAD:sub/` accepts a trailing slash on a tree (rc=0), so the repair pointer `.ufo/waves/round-19/evidence/doctor/` resolves unchanged; nothing else in the suite distinguishes |
| A3 `pointers()`: `if not LANE.match(path): continue` → `if False:` | pointer-resolver (LANE filter dropped) | yes | **no — SURVIVED** | fixture non-LANE paths (`docs/`, `d/`, `x.md`) absorb the difference: all resolve or stay guard-red; green stays green. The LANE allow-list has zero killing power in this suite |
| B1 shonen loop: first box only (`if m and not any(k.startswith('shonen:') for k in u)`) | unit-enumeration (findall→first) | **no** | **killed** | `green: repaired by document: want 0 got 1` — box4 missing ⇒ `sh4=''` ⇒ R3 stated None ⇒ mismatch in every case incl. green |
| B2 `units()`: drop `('## Frontier', 'prov_frontier:')` from the section loop | unit-enumeration | yes | **no — SURVIVED** | fixture Frontier rows carry no LANE pointer (only `` `docs/x.md` ``), so dropping the enumeration is observationally equivalent. PROVINCE Frontier enumeration is untested |
| C1 `heading_range`: `break` → `continue` on stop-line | range-bounds | yes | **no — SURVIVED** | `continue` skips the `last = i` update for the stop-line itself, and both fixtures have no non-blank content after the first stop-line (`## Next`, `### Sub` are last) ⇒ identical ranges. Post-stop content is untested |
| C2 `heading_range`: `return (start+1, last+1)` → `(start+1, last+2)` | range-bounds (upper off-by-one) | **no** | **killed** | green case: observed craft (3,6) ≠ stated (3,5) ⇒ R1/R2 fail ⇒ green fails |
| C3 `heading_range`: `last = start` → `last = start - 1` | range-bounds (empty section) | yes | **no — SURVIVED** | no fixture heading section is empty-after-heading; the first non-blank line always overwrites `last` ⇒ equivalent here |
| D1 checks loop: `tuple(s) != tuple(o)` → `==` | count-comparison (inverted) | **no** | **killed** | green case: all 7 equal checks now "fail" ⇒ mismatches=7 ⇒ green fails |
| D2 `mismatches = len(unresolved) + len(failed)` → `len(unresolved)` | count-comparison (assertions dropped from target) | yes | **no — SURVIVED** | every red case is already guard-red (`pointers_not_fewer` 4<5 and `unrepaired` non-empty), so `assertion_mismatches` is never the sole killer. A count-mismatch-only red does not exist in the suite |
| E1 `guards_ok` drops `not missing_units` | guard-missing_units | yes | **no — SURVIVED** | "box removed" co-removes the box's `PROVINCE.md:15-17` pointer, so `pointers_not_fewer` fires too; no case isolates a removed unit whose pointers survive elsewhere |
| E2 `guards_ok`: `total >= base_total` → `total > base_total` | guard-pointers_not_fewer | **no** | **killed** | green case repairs by substitution (5→5 pointers, equal, not more) ⇒ guard false ⇒ green fails |
| E3 `guards_ok` drops `not unrepaired` | guard-unrepaired | yes | **no — SURVIVED** | all 13 reds still red via `pointers_not_fewer` (4<5); no red isolates the repair guard |
| E4 `bad_base`: `resolves(root, base, …)` → `resolves(root, rev, …, cache)` | guard-bad_base (wrong revision) | yes | **no — SURVIVED** | fixture pointer-relevant trees are identical across base/rev, so resolving `bad_base` at either revision gives the same answer. The guard's revision pinning is untested |
| F1 `met_target`: `and` → `or` | target conjunction | yes | **killed** | 4 reds with `mismatches==0` but `guards_ok=false` flip to met ("unresolved pointer deleted", "substituted by other document", "range beyond file", "new unresolved pointer": want 1 got 0) — the conjunction is load-bearing exactly where guards carry the red |

**Tally: 15 applied, 5 killed (B1, C2, D1, E2, F1), 10 survived.**

## Coverage findings (survivor cluster — findings only, no counter changes)

1. **Red-case triple redundancy.** Every non-green rev fixture replaces the
   base's only prov_core LANE pointer (`evidence/doctor/`) with the
   LANE-invisible `` `docs/x.md` `` and never repairs it, so in all 13 reds
   `pointers_not_fewer` (4<5) and `unrepaired` are both false simultaneously.
   Any mutant that leaves green green and leaves the `guards_ok` conjunction
   honest is therefore invisible (A1, A3, B2, C1, C3, D2, E1, E3, E4, A2). A
   red fixture per mechanism (change exactly one thing against an otherwise
   green rev) would collapse this cluster.
2. **Range bound untested through real pointers (A1).** The only out-of-range
   pointer in the suite rides a non-LANE path and is filtered before
   `resolves()`. A LANE path with an out-of-range range (e.g. `SKILL.md:99-100`
   in a cap row) would kill A1.
3. **LANE allow-list untested (A3).** No red depends on a pointer being
   excluded because its path is off-lane.
4. **Guards mask each other (E1/E3/D2).** `missing_units`, the repair guard and
   `assertion_mismatches` each lack a case where they are the sole killer.
5. **PROVINCE Frontier enumeration untested (B2)** — fixture Frontier rows
   carry no LANE pointer.
6. **heading_range post-stop content and empty sections untested (C1/C3).**
7. **Guard revision pinning untested (E4)** — base/rev fixture trees are
   identical for pointer paths.

## Prediction calibration

13/15 predicted correctly. Misses: A1 (I overlooked that the existence check
short-circuits before the mutated line, and that the out-of-range fixture
pointer is LANE-filtered) and C1 (I overlooked that `continue` skips the
`last = i` update for the stop-line itself, making the mutant suite-equivalent).
Both misses were my derivation errors; the battery outputs above are the
ground truth and are now backed by re-read source for every function involved
(`pointers`, `resolves`, `heading_range`, `measure`).

## Restoration evidence

- Frozen counter sha256 before battery: `7f137b664984595e4d63068a7fa0be2c74a7c57fe5cd5e3a0b794918d2a7b0f7`;
  after battery: `7f137b66…` (identical; the driver never opens the frozen file
  for writing, mutants were separate scratch copies).
- Mutant copies deleted by the driver; scratch dir removed; lane writes limited
  to this report and `.ufo/waves/round-38/w1/artifacts/R38MutC2/`
  (`results.json`, `lane-base-donothing.json`, `driver-mutate_c2.py`).
- `git status --porcelain tools/round-38/` = 0 lines before and after.

SHONEN: n/a (leaf mutation probe; nothing here is claim data).
