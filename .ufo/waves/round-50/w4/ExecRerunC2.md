# ExecRerunC2 — R50 attempt 2, wave 4 (falsify)

**VERDICT: the C2 battery re-run HOLDS — no atom flip. Three falsification findings survive (F1, F2, F3), all outside C2's own reach.**

The re-run itself is clean and reproduces the landed receipt exactly. The findings are about what the *other* landed artifacts claim and whether any counter would catch them.

---

## F1 (STOP-class, landed-and-still-standing): the C3 predicate asserts "frozen paths untouched" but the instrument never enforces it

**Severity: high. Owner: C3 instrument (`tools/round-50-c3/sqfs-triage-v5.py`).**

The C3 PREDICATE constant — the sentence copied verbatim into `plans/round-50-attempt2-claims.md`, into the instrument's docstring, and into every receipt under the key `predicate` — opens:

> "at the measured revision REV, with FREEZE an ancestor of REV, **frozen paths untouched**, running `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py …` exits 0 with `pair_mismatches 0` …"

The instrument *computes* the drift and *reports* it, but never fails on it. `sqfs-triage-v5.py:1257-1281` fills `freeze_report['other_tools_round50_changed']` and `freeze_report['instrument_unchanged']`; nothing downstream reads either field. The verdict is computed at `:1365` as `'met' if not mismatches and not evaluator_missing else 'not met'` — the freeze arm has no path into it. A grep for `other_tools_round50_changed` returns exactly two hits (the initialiser at `:1256` and the assignment at `:1280`); there is no `raise` on it.

**Measured (M6, on a copy, never in the lane):** commit `1a2b0ca6` on the scratch clone edits `tools/round-50/gap-rule.json` — a path inside C3's own `FROZEN_TOOL_TREES = ('tools/round-50/', 'tools/round-50-c3/')` — *after* the freeze `435d41fd`.

```
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <clone> --rev 1a2b0ca6… \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes \
  --json-out <S>/c3-m6.json
→ EXIT=0
table: v5 (17 rules) from git:1a2b0ca6…:SKILL.md
envelopes: 126   pair_mismatches: 0   evaluator_missing: 0
verdict met
"freeze": { "other_tools_round50_changed": [ "tools/round-50/gap-rule.json" ], … }
```

The receipt's own `freeze` block names the drift, and the run still reports **`verdict: met`, exit 0**. The predicate sentence the receipt carries is therefore not satisfied by the run the receipt records. Both C1 and C2 *do* enforce their frozen sets (`c1-counter.py:449` → `reason = 'frozen_path_changed'`; `c2-record.py:1065-1069` → `frozen_path_changed`); C3 is the only one of the three whose predicate names the clause without binding it.

**Why this matters for the round's claims:** the L1's wave-4 summary states C3 "landed and scored" on the strength of this predicate. The scoring itself is sound (the table really does match the evaluator 126/126 — I re-ran it), but the *sentence* overstates what was checked. The honest fix is either to make the freeze arm raise (exit 2) when `other_tools_round50_changed` is non-empty, or to narrow the predicate's clause to match what is actually enforced. Note the fix must not be a naive one: `tools/round-50-c3/sqfs-triage-v5.py` itself is inside `FROZEN_TOOL_TREES` and the instrument's own bytes legitimately change between freeze and rev (see F2), so an arm that raises on any drift in those trees would refuse every legitimate re-run.

## F2 (STOP-class): the C3 receipts' `instrument_sha256` does not name the instrument that produced them, and no counter re-reads it

**Severity: high. Owner: C3 receipts (`.ufo/waves/round-50/c3/c3-{before,after}.json`).**

The receipts carry `instrument_sha256` alongside a `rev`. Measured at the stated tip `c67b741e`, the two disagree:

| receipt | `instrument_sha256` (the running tool's own bytes) | `git show <receipt.rev>:tools/round-50-c3/sqfs-triage-v5.py` | `receipt.freeze.instrument_sha256_at_rev` |
|---|---|---|---|
| `c3-after.json` | `f29eb920…` | `a2ebb5a4…` (at rev `1439dfe9`) | `a2ebb5a4…` |
| `c3-before.json` | `f29eb920…` | file absent at rev `f890bbea` | `null` |

So `c3-after.json` says "I scored rev `1439dfe9`" while the instrument committed at `1439dfe9` is `a2ebb5a4…` — not the `f29eb920…` that actually ran. `c3-before.json` is worse: its `rev` (`f890bbea`) has no instrument at all (`instrument_sha256_at_rev: null`, `instrument_unchanged: null`), so nothing in the receipt can tie the 19-mismatch before-state to any committed instrument bytes.

The receipt's own `freeze` block carries the disambiguating value (`instrument_sha256_at_rev`), so the information is *present* — but the top-level `instrument_sha256` key names the wrong thing, and the L1's summary quotes it as if it pinned the scoring tool. The wave-4 spec text ("receipts carry `predicate` + `instrument_sha256` and are gated on re-read") reads as though the receipt is bound to the instrument; it is not.

Compounding: the *committed* `SKILL.md` pins differ between revisions for the same reason — `c67b741e` pins `ef4633c5…` (correct for that rev), and `HEAD` pins `f29eb920…`. The pin tracks, but the C3 receipts did not re-pin when the tool changed at `1a7cc5c3`. A consumer that reads `receipt.instrument_sha256` and compares it to `git show receipt.rev:<tool>` gets a **mismatch** — the guard intended to catch tool drift instead reports one. Either the receipts must be regenerated so `instrument_sha256` names the blob at the scored rev, or the key must be renamed to something like `instrument_sha256_running` with a second key for the committed blob.

**Demonstrated directly, not just inferred.** I produced a fresh C3 receipt (M6b, receipt `c3-m6b-frozen-drift-head-instrument.json`) and the same shape falls out:

```
receipt.rev                             = d73c14c1a879f61caac2dfd565cfcf5369cbb45f
receipt.instrument_sha256               = f29eb920…   (the RUNNING tool)
blob AT receipt.rev (sha256)            = ef4633c5…   (the COMMITTED tool at that rev)
receipt.freeze.instrument_sha256_at_rev = ef4633c5…   (correct value, in the right place)
match?                                 = False
```

The receipt names two different instruments and puts the *wrong* one under the key a reader would naturally use. The correct value is present but buried under `freeze.instrument_sha256_at_rev`, and `freeze.instrument_unchanged` is `null` (the instrument did not exist at the freeze), so no field anywhere says "the tool at this rev differed from the tool that ran".

**The `instrument_unchanged` check is structurally vacuous.** The freeze arm compares `git show FREEZE:<tool>` against `git show REV:<tool>` (`sqfs-triage-v5.py:1265-1275`). But the instrument was **added after the freeze** — `git log --diff-filter=A` puts its first commit at `1439dfe9`, while the freeze is `435d41fd`, where the path does not exist at all (`fatal: path 'tools/round-50-c3/sqfs-triage-v5.py' exists on disk, but not in '435d41fd…'`). So `at_freeze` is always `None`, the `if` at `:1271` never fires, and `instrument_unchanged` is **permanently `null`** in every receipt this instrument can ever produce. The guard that was written to detect the tool having drifted since the freeze cannot detect it, by construction. The only meaningful anchor is `instrument_sha256_at_rev`, and that is the key nobody reads.

**Cross-check (the same commit also moved the lane's prose):** `SKILL.md:572` at `c67b741e` says the instrument sha256 is `ef4633c5…`, which *is* the blob at `c67b741e` — that one is correct. The defect is confined to the JSON receipts.

## F3 (calibration): C2's registry census and SOURCES coverage do not reach the round-50 landed rows

**Severity: medium. Owner: C2 counter's *scope* (the counter is frozen; the gap is in what the round landed).**

C2's B9 census is scoped to `tools/round-49/**` at base + `tools/round-50/**` at rev (`c2-record.py:143-144`, `census_paths` at `:845`). The C3 instrument was deliberately placed in `tools/round-50-c3/` to stay outside the frozen walk (the instrument's own comment at `sqfs-triage-v5.py:308-316` documents this reasoning), which means **C2's census cannot see it**, and C2 therefore never required a registry row for it. The lane did add one anyway (`SKILL.md:1800`), which is good practice — but nothing enforces it. Measured (M1): deleting the `tools/round-50-c3/sqfs-triage-v5.py` registry row from `SKILL.md` on a copy leaves C2 **green** (exit 0, `mismatches 0`, no atom red).

Likewise, C2's SOURCES atoms (B6/B7/B8) are hard-wired to the round-49 rows `S149`/`S147`/`S138`; no C2 atom reads the new round-50 rows `S243`/`S244`/`S245`/`S249`. Measured (M4): mutating the `S243` quote (`+#define AVM_LE 2` → `+#define AVM_LE 99`) leaves C2 **green** (exit 0, `mismatches 0`). M5 (deleting the `S249` row entirely) is likewise green.

The new rows *are* bound by C1 (`c1-counter.py:2464` `entry_source_ids`, `:2477` `opened_source_rows`, which require the entry's `source:` ids to be present as 11-cell rows with a valid open date and a `used-by` pointing at the entry) — so the SOURCES rows are not wholly unverified. But the *registry row* for the C3 instrument has no verifier at all, and that row is the thing that tells a reader which command to run and what its exit codes mean.

**Note on scope:** this is a gap in *coverage*, not a defect in C2's implementation. C2 is a frozen counter; widening its census would break its freeze binding. The honest remedy is a separate, later-round check, not an edit to `c2-record.py`.

---

## Survival check against the L1's later corrections

The lane moved on during this seat's run (falsify corrections 1–5 landed at `b98fd2d0`, `1bff0613`, `4db20b0b`, `98cd8ce5`, `004d5fd4`). I re-checked both STOP-class findings against the **current** HEAD `004d5fd4`:

- **F1 survives.** `git show HEAD:tools/round-50-c3/sqfs-triage-v5.py` still has exactly two references to `other_tools_round50_changed` (the initialiser and the assignment), and the verdict is still `'verdict': 'met' if not mismatches and not evaluator_missing else 'not met'` at `:1365`. The freeze arm is still report-only.
- **F2 survives.** `c3-after.json` at HEAD still carries `instrument_sha256: f29eb920…` against `rev 1439dfe9`, whose committed tool blob is `a2ebb5a4…` — still a mismatch. All six regenerated control receipts (`ctl-do-nothing`, `ctl-action-swapped`, `ctl-guard-deleted`, `ctl-junk`, `c3-before`, `c3-after`) carry the same running-tool sha while naming revs whose committed blobs are `a2ebb5a4…` or absent. `SKILL.md` at HEAD correctly pins `f29eb920…` (the current tool), so the *prose* is right and the *receipts* are wrong.
- **F3 survives.** The registry census is still `CENSUS_REV_PREFIX = 'tools/round-50'`; `tools/round-50-c3/` is still outside it.

Note that `98cd8ce5` regenerated the control receipts specifically to "bind the instrument (`predicate` + `instrument_sha256`)" — the intent is right, but the key still names the running tool rather than the committed blob, so the binding it asserts is not the one a reader would check.

---

## What held (attacked and survived)

- **C2 battery re-run at the stated tip `c67b741e`** — exit 0, `atoms_total 11`, `mismatches 0`, `battery.failing []`, `do_nothing_red` 11/11, `mutation_count 52`, zero no-op mutations, zero cross-flips. **No atom flip. Not a STOP finding.**
- **C2 battery re-run at the actual `HEAD` `db61a907`** — identical green result.
- **C2 battery re-run at the landed receipt's own rev `bff7d96c`** — byte-for-byte identical to `.ufo/waves/round-50/l1/scores/c2-final-attempt2.json` on every field, including `do_nothing_paths 1150`, `mutation_count 52`, `do_nothing_red` 11. The landed receipt is exactly reproducible.
- **C2 offline selftest** — exit 0, 29 cases, `failures []`.
- **C3 selftest** — exit 0, 18 cases, pass 18, fail 0.
- **C3 scoring itself** — re-run over the 126 frozen envelopes at the tip: `pair_mismatches 0`, `evaluator_missing 0`, `verdict met`. The *scoring* is sound; only the predicate *sentence* (F1) and the receipt's *key semantics* (F2) are wrong.
- **The `do_nothing_paths` count grows with the rev** (1150 at `bff7d96c` → 1761 at `c67b741e` → 1768 at `db61a907`) because more paths changed since the freeze. This is expected, not a regression: `do_nothing_red` stays 11/11.

## Counter-check on the "tip" the L1 named

The prompt's tip `c67b741e` was **not** the lane tip for most of this wave. The lane moved to `db61a907` → `1a7cc5c3` → `92ec6e6d` → `f73a61e5` → `b98fd2d0` → `4db20b0b` while this seat ran. The prompt's "the tip has moved only by evidence commits" is accurate for `db61a907`/`a3615f70`, but `1a7cc5c3` ("C3 guard fix applied") changed the **instrument's own bytes** (`ef4633c5…` → `f29eb920…`), and `b98fd2d0`/`4db20b0b` changed landed content (the knowledge entry, PROVINCE, the lesson, and `plans/round-50-attempt2-claims.md`). I therefore ran C2 at the stated tip, at the actual HEAD, and at the landed receipt's rev, and all three are green.

**Also observed: the lane working tree carries uncommitted drift in a tracked corpus file.** `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` is modified in the working tree relative to `HEAD` (`b98fd2d0`), 4 insertions / 4 deletions, re-wording the census and the LE-handler statements. Per the contract this is the L1's to land or discard — **reported, not touched.** Several `.ufo/waves/round-50/w3/**` files are likewise modified-but-uncommitted. No fleet-root stray was found.

**One claim already corrected by the L1 during this wave (not a finding):** the knowledge entry's status line at `c67b741e` said "every documentation binding true", while the C1 receipt at that rev reports `province_core_row: false` and `province_core_section: false`. The L1 fixed this in `b98fd2d0` ("binding overstatements fixed (entry, PROVINCE)"). The binding-overstatement defect no longer exists at the current HEAD — I record it here only because the L1's own wave-4 summary still describes the entry as carrying `every documentation binding true`.

---

## Falsification matrix (all on copies in scratch; the lane was never mutated)

| ID | Mutation | Target | Expected if covered | Measured | Verdict |
|---|---|---|---|---|---|
| M1 | delete the `tools/round-50-c3/sqfs-triage-v5.py` registry row from `SKILL.md` | C2 B9 | exit 1, B9 red | **exit 0, `mismatches 0`, no atom red** | **GAP** (F3) |
| M4 | mutate the new `S243` quote (`AVM_LE 2` → `AVM_LE 99`) | C2 | exit 1 | **exit 0, `mismatches 0`** | **GAP** (F3) |
| M5 | delete the new `S249` row from `corpus/SOURCES.md` | C2 | exit 1 | exit 0, `mismatches 0` | GAP (F3) |
| M6 | edit `tools/round-50/gap-rule.json` after the freeze, then run C3 | C3 predicate | exit 2 / not met | **exit 0, `verdict: met`**, receipt names the drift | **GAP** (F1) |
| M7 | rewrite `plans/round-50-attempt2-claims.md` after the freeze | C2 freeze walk | exit 2 `frozen_path_changed` | **exit 0, `mismatches 0`, no atom red** | **GAP** — the attempt-2 claims file is in *no* counter's frozen set (`c2-record.py:123` freezes `plans/round-50-claims.md`, the attempt-1 file; `c1-counter.py:414` likewise), so the file C3's PREDICATE is bound to can be rewritten post-freeze unchallenged. The lane already did this at `4db20b0b`. |
| M2 | unmap the new knowledge stem from `corpus/README.md` `## Coverage map` | C2 B1 | exit 1, B1 red | **exit 1, B1 red**: `knowledge files not mapped in README Coverage map: ['corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md']` | **HELD** — B1 does cover the new knowledge entry |
| M3 | change the SCORECARD coverage head `140/140` → `139/140` | C2 B1 | exit 1, B1 red | **exit 1, B1 red**: `coverage row states 139/140, derived 140 knowledge files` | **HELD** |
| M6b | the same frozen-tree edit as M6, re-run with the **current** instrument (`f29eb920…`) | C3 predicate | exit 2 / not met | **exit 0, `verdict: met`**, `freeze.other_tools_round50_changed = ["tools/round-50/gap-rule.json"]` | **GAP** (F1) — F1 is not an artifact of the older instrument |

## Commands run (exact)

All counters are the frozen bytes at the tip; `sha256sum tools/round-50/c2-record.py` = `4749bcd86c8f61bfb6994baeab3bd990b61ea0c369b87197351d0a4618e71285`, identical at the freeze `435d41fd` (the counter self-reports `counter_sha256 == counter_sha256_at_freeze`).

```
S=/fast/scratch/hyaku/kaidoku-r50/w4-ExecRerunC2 ; export TMPDIR="$S"

# 1. the assigned re-run (stated tip)
python3 -I -B tools/round-50/c2-record.py --root <lane> --rev c67b741e8f6bd8d64adbdb15e059d47fde004c77 \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --battery --work $S/w --json-out $S/c2.json
→ exit 0 ; atoms_total 11 ; mismatches 0 ; battery.failing [] ; do_nothing_red 11/11 ; mutation_count 52

# 2. same at the actual HEAD
python3 -I -B tools/round-50/c2-record.py --root <lane> --rev db61a90752657588817e78327c78106d486291d1 \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --battery --work $S/w2 --json-out $S/c2-head.json
→ exit 0 ; identical fields

# 3. reproduction of the landed receipt at its own rev
python3 -I -B tools/round-50/c2-record.py --root <lane> --rev bff7d96c59d85ca6d997fa1ced59348dcc228190 \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --battery --work $S/w3 --json-out $S/c2-landedrev.json
→ exit 0 ; identical to .ufo/waves/round-50/l1/scores/c2-final-attempt2.json on every field

# 4. C2 offline selftest
python3 -I -B tools/round-50/c2-record.py --selftest --root <lane> --work $S/ws --json-out $S/c2-selftest.json
→ exit 0 ; 29 cases ; failures []

# 5. C3 selftest at the tip
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest --work $S/c3st --json-out $S/c3-selftest.json
→ exit 0 ; 18 cases ; pass 18 ; fail 0

# 6. C3 re-scoring over the 126 frozen envelopes (M6 arm, see matrix)
python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root <clone> --rev <rev> \
  --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --envelopes .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes --json-out <out>
→ exit 0 ; pair_mismatches 0 ; evaluator_missing 0 ; verdict met
```

Fixture discipline: all mutations ran on `git clone --shared <lane> "$S/clone"`, detached at `c67b741e`, with `git -C "$S/clone" rev-parse --show-toplevel` asserted equal to `$S/clone` before the first commit, and `user.name`/`user.email` set in that clone only. **No mutating git command was run in the lane or the fleet repo.** No REA run was performed (not authorised for this seat). Scratch removed after receipts were copied into `.ufo/waves/round-50/w4/ExecRerunC2/`.

## Receipts

Under `.ufo/waves/round-50/w4/ExecRerunC2/`:

| file | what |
|---|---|
| `c2-rerun-at-tip.json` | C2 battery at `c67b741e` (exit 0) |
| `c2-rerun-at-head.json` | C2 battery at `db61a907` (exit 0) |
| `c2-landed-rev-repro.json` | C2 battery at `bff7d96c` — reproduces the landed receipt |
| `c2-selftest.json` | C2 selftest, 29 cases, exit 0 |
| `c3-selftest.txt` | C3 selftest, 18/18, exit 0 |
| `c3-m6-frozen-drift.json` | the C3 receipt written with frozen drift present (`verdict: met`) |
| `mutations.json` | the mutation matrix with per-arm exit codes and red-atom lists |
| `commands.txt` | every command above with its exit code, stdout sha256 and UTC time |

## Tooling

No tools installed, upgraded, or removed. `python3` (system, 3.x) only; `uv`, `npx`, `pacman` not used. `disk-guard.sh status` consulted before the heavy passes (idle ≥ 12.2 M on `/var/tmp`, 488 G free on `/fast`).
