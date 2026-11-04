# ExecMutation — R88-C1 instrument mutation probe (round 88, kaidoku)

Seat: `ExecMutation` (executor). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base HEAD `01ffb9376`; instruments under test are unmodified (`git status` shows no
change under `tools/round-88/`), and their sha256 match the pins in
`.ufo/waves/round-88/claims.json`:

| instrument | sha256 (measured) | pin |
|---|---|---|
| `tools/round-88/upx-chain-repair.py` | `59ee51b0e63d3e089c23cee066b637841133412cee50748d84d717d61f8a0b46` | match |
| `tools/round-88/upx-chain-battery.py` | `a01ed6227878db2a64c7274d6ad2f37aa7c2e3462629cbb1f8619094bc037160` | match |

No tool was installed, upgraded or removed this seat (pacman paused; nothing needed
`uv tool`/`npx`/`~/.local/bin`).

## 1. What ran (exact commands)

Base selftests:

```
python3 tools/round-88/upx-chain-repair.py  --selftest     # cases=11 failures=0 rc=0
python3 tools/round-88/upx-chain-battery.py --selftest     # cases=6  failures=0 rc=0
```

Base counter run (claim predicate, REA enabled; wall 182.95 s, exit 0):

```
python3 tools/round-88/upx-chain-battery.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --repair-cmd tools/round-88/upx-chain-repair.py \
  --upx /usr/bin/upx \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r88/ExecMutation/base-work \
  --json-out /fast/scratch/hyaku/kaidoku-r88/ExecMutation/base-receipt.json \
  --evidence-dir /fast/scratch/hyaku/kaidoku-r88/ExecMutation/base-rea
# recovered 4 of 4  controls_ok={N1,N2,N3 all True}  met=True  exit=0
# regression: recovered 8 of 8, controls true, met=True
```

Mutation harness (`/fast/scratch/.../ExecMutation/mutate.py`, deleted with scratch; its
output manifest is preserved as `receipts/mutants.json`): for each declared mutant it
copies the instrument into a depth-preserving mirror (`<mut>/tools/round-88/<file>` with
`tools/round-87` symlinked to the lane), asserts the anchor occurs **exactly once**
(`anchor_count == 1` for all 13 rows and all 3 control probes), applies the single edit,
byte-compiles the mutant (`py_compile`), then runs `python3 -I -B <mutant> --selftest` and
parses `SELFTEST cases=N failures=M <names>`.

Counter probe per repair mutant (8 rows), `--no-rea` (so `rea_recover` is false by
construction and only the four byte-level arms are read):

```
python3 tools/round-88/upx-chain-battery.py --root <lane> \
  --repair-cmd /fast/scratch/hyaku/kaidoku-r88/ExecMutation/mut/<id>/tools/round-88/upx-chain-repair.py \
  --upx /usr/bin/upx --pkg <rea-agents> \
  --work /fast/scratch/hyaku/kaidoku-r88/ExecMutation/work-<id> \
  --json-out /fast/scratch/hyaku/kaidoku-r88/ExecMutation/receipt-<id>.json --no-rea
```

Control-green probes (3 rows): same battery invocation with the *mutated battery* and a
built-in do-nothing control as `--repair-cmd` (`identity`, `identity`, `naive-global`).

Candidate census: read-only re-walk of the repair's own candidate predicate over the four
pinned carriers packed with `/usr/bin/upx --best` (dereferencing `xxd`, which is a symlink),
`sz_cpr` of block 0 zeroed, `receipts/candidate-census.json`.

## 2. Measured numbers

### 2.1 Base (independent reproduction of the R88-C1 predicate)

- `recovered 4 of 4`, `controls_ok = {N1-refuse-plain: true, N2-corrupt-payload: true,
  N3-intact-idempotent: true}`, regression arm `recovered 8 of 8` with controls true,
  `met_target true`, exit 0.
- Restored bytes: `upx -d` output sha256 equals the pinned carrier sha256 for all four
  (`e815667571d0…`, `7b1e5d0c970a…`, `6c78c5e58c3b…`, `0bd49c8d4da5…`).
- REA 6.5.0 procedure counts on the restored bytes: jq 167, xxd 99, libz 184, dinit 1268 —
  equal to `DECLARED_ORIG`; `field_only`, `test_ok`, `identity` true on all four.
- Packed sha256 (deterministic across all 9 counter runs): jq `e8b6c9e76b54…`,
  xxd `1727faf91c38…`, libz `a9c544e6da4f…`, dinit `b67ce1bdda27…`.

### 2.2 The 13-row table

Kill rule applied exactly as specified: a mutant is killed **only** when its declared case
exists in the instrument's selftest and appears in the failure list.

| id | file | single edit | declared case | selftest | counter (4 byte arms) |
|---|---|---|---|---|---|
| R01 | repair | `if not (0 < derived <= sz_unc0)` → `if not (0 < derived)` | `derived-value` | survivor | not killed (all 4 carriers byte-identical to base) |
| R02 | repair | sentinel-reach `try/except` → `end, info = ph_off, {"resume": None, …}` | `chain-geometry-recovers` | survivor | not killed (identical bytes) |
| R03 | repair | `fits` computed from `total > u_len` → `fits = True` | `geometry-records-u_len` | survivor | **killed on dinit** |
| R04 | repair | `key = (fits, total, -derived)` → `key = (total, -derived)` | `geometry-records-u_len` | survivor | **killed on dinit** |
| R05 | repair | `if sz_cpr0 != 0 or sz_unc0 == 0` → `if sz_unc0 == 0` | `szcpr-nonzero-not-derived` | survivor | not killed (equivalent on this population) |
| R06 | repair | `total += sz_unc` → `total += sz_cpr` | `geometry-records-u_len` | **killed** | **killed on dinit** |
| R07 | repair | drop `or d[s1+8] not in (m0, ph["method"])` | `chain-geometry-recovers` | survivor | not killed (identical bytes) |
| R08 | repair | add `except Exception: … return 1` after the typed `except` | `exit-1-on-untyped-error` | **gap (case absent)** | n/a |
| B01 | battery | `field_only` window test disabled (`and False`) | `field-only-refuses-outside` | **killed** | n/a |
| B02 | battery | `field_only` length check disabled (`and False`) | `field-only-refuses-length` | **killed** | n/a |
| B03 | battery | `identity` builtin returns `data + b"\0"` | `identity-builtin-noop` | **killed** | n/a |
| B04 | battery | `TARGET = len(CARRIERS)` → `TARGET = 3` | `target-is-four` | **killed** | n/a |
| B05 | battery | `if r["rc"] != 0 …` → `if (r["rc"] not in (0, None)) …` (rc None = success) | `rc-none-not-refusal` | **gap (case absent)** | n/a |

Totals: **killed by selftest 5** (`R06`, `B01`, `B02`, `B03`, `B04`); **survivors 6**
(`R01`, `R02`, `R03`, `R04`, `R05`, `R07`); **absent-case gaps 2** (`R08`, `B05`).
Of the six survivors, the real counter kills **2** (`R03`, `R04`) and leaves **4**
(`R01`, `R02`, `R05`, `R07`) alive on both instruments.

Selftest-case census: repair 11 cases (matches the plan's "11"), battery 6 (matches "6").

### 2.3 Why R03/R04 die on dinit only

The dinit failure is `upx: …/chain.repaired: Exception: compressed data violation` with
`test_ok` and `identity` false and `repaired_equals_packed` false; jq, xxd and libz still
pass all four arms. Derived values measured directly:

| carrier | base derived `sz_cpr` | R03/R04 derived | base accounted / `u_len` | R03/R04 accounted |
|---|---|---|---|---|
| dinit | **226** (next block 814) | **136** (next block 724) | 851,288 / 851,288 (fits) | 123,942,159 (does not fit) |
| libz | 201 | 201 | 98,592 / 108,560 (fits) | 98,592 |
| jq | 252 | 252 | 30,800 / 30,800 | 30,800 |
| xxd | 249 | 249 | 38,928 / 38,928 | 38,928 |

### 2.4 Candidate census (why the selftest cannot see the selection law)

Admissible candidates under the instrument's own predicate, per carrier:

- jq: **1** — s1 840, derived 252, accounted 30,800.
- xxd: **1** — s1 837, derived 249, accounted 38,928.
- libz: **1** — s1 9517, derived 201, accounted 98,592 of u_len 108,560 (shared object).
- dinit: **3** —
  (s1 724, derived 136, accounted 123,942,159, **does not fit**),
  (s1 814, derived 226, accounted 851,288, fits, **selected**),
  (s1 1028, derived 440, accounted 850,696, fits).

So the `fits_u_len` preference rejects candidate 724, and the accounted-total tiebreak
chooses 814 over 1028 (by 592 bytes of accounting) — both only on dinit.
The selftest fixture has exactly **one** admissible candidate (s1 140, derived 40,
accounted 200 against `u_len` 64), so no selection rule is observable there.

### 2.5 Control-green probes

| id | mechanism | `--repair-cmd` | controls_ok | recovered | met_target | exit |
|---|---|---|---|---|---|---|
| G1 | `identity` builtin refuses an unpacked ELF (contains no `UPX!`) | `identity` | **all true** | 0 of 4 | false | 1 |
| G2 | N1 recorded as `"refused": True` unconditionally | `identity` | **all true** | 0 of 4 | false | 1 |
| G3 | `naive-global` builtin refuses an unpacked ELF | `naive-global` | **all true** | 0 of 4 | false | 1 |

All three turn every control green; none turns the claim green (`met_target` false in all
three, regression arm `met=False`). At base, the only control any do-nothing control fails
is N1 (frozen receipts: `identity` and `naive-global` fail N1 only, `r87-anchor` passes all
three), so N1 is the whole of the do-nothing signal and it is satisfiable by refusal shape
alone.

## 3. Findings that limit or contradict the plan/claim

1. **The repair selftest does not exercise the selection law.** The zeroed-fixture case has
   one admissible candidate; 6 of 8 repair mutants survive `--selftest`. The `fits_u_len`
   preference, the accounted-total tiebreak, the `derived <= sz_unc0` bound, the
   sentinel-reach test and the method gate are all invisible to it. The plan's named limit 1
   ("the repair derives sz_cpr from geometry and bounds it by u_len accounting") is enforced
   by the counter on dinit only.
2. **`szcpr-nonzero-not-derived` does not test the `sz_cpr0 != 0` gate.** For the
   `_fixture(7)` image the upstream round-87 repair answers `intact=True` and returns the
   input unchanged, so `geometry()` is never entered; the case passes for that reason.
   R05 (gate removed) therefore survives both instruments — an equivalent mutant on this
   population. The declared limit "a non-zero but wrong sz_cpr is left alone" is upheld by
   the upstream intact verdict, not by this instrument's guard.
3. **Three guards are killed by nothing** (`R01` bound, `R02` sentinel test, `R07` method
   gate): their mutants produce byte-identical output on all four carriers and pass the
   selftest. The direction is conservative (dropping them changes no measured output here),
   but no instrument distinguishes them.
4. **N1 is gameable.** Three independent mutants make all controls green with a do-nothing
   repair (recovered 0 of 4). N1 is a refusal-shape check, not a capability control; the
   claim's own green depends on `recovered`, `N2`, `N3` and the regression arm, which did not
   turn.
5. **No selftest covers exit-code or stderr semantics.** `R08` (catch `Exception`, print one
   line, `return 1`) is *exit-code equivalent* to base — an uncaught exception already makes
   CPython exit 1 — so the mutant only replaces the traceback with a single-line message; no
   case can distinguish it, and none exists. `B05` (`rc is None` from a crashed child treated
   as success) has no case at all; by source reading (not measured), the builtin path would
   then `open()` a missing output and raise out of `score()`, i.e. the counter would die
   instead of recording `could-not-evaluate`. The documented contract "0 repaired/intact;
   2 refused; 1 unexpected" is enforced only by reading the source.
6. **Population fragility.** The u_len accounting law is load-bearing on exactly one of four
   carriers (dinit). A three-carrier population without dinit would let `R03`, `R04` and
   `R06` survive the counter as well.

## 4. Risks / caveats

- Mutants lived in scratch and scratch was deleted; they are reproducible from
  `table.json` (anchor, replacement, unified diff, mutant sha256) and
  `receipts/mutants.json`. Counter probes were `--no-rea`, so `rea_recover` is false in every
  probe receipt by construction and only the four byte arms are interpreted; the base run
  (REA on) is the claim-level check.
- `B05` was not counter-probed: triggering `rc is None` needs a child that dies without a
  status (timeout/OSError), which the pinned repair cannot be made to do without editing it.
  Declared gap.
- Wall times measured: base (REA on) 182.95 s; repair-mutant counter probes 84–114 s each;
  control-green probes 1.16 s (G1, G2) and 51.25 s (G3). The 84–114 s per repair probe is
  the geometry scan on real carriers (16 repair invocations per run), consistent with the
  plan's named limit 4 (O(window) per candidate).
- Sibling seats had uncommitted edits in the lane (`PROVINCE.md`, `SKILL.md`,
  `corpus/QUALITY.md`, `corpus/README.md`, an untracked knowledge entry); I touched none of
  them and made no git/jj mutation.

## 5. Suggested follow-ups (not performed here)

- Add a multi-candidate selftest fixture shaped like dinit (≥2 admissible candidates, one
  accounting more than `u_len`, two fitting with different totals) so `R03`/`R04`/`R06` are
  killed without the packer.
- Add a fixture where the upstream repair refuses on a *non-zero* `sz_cpr` so the gate is
  reachable, and assert `derived_sz_cpr`/`fits_u_len` explicitly.
- Add `main()`-level cases for exit 2 (refused, bad argv) and exit 1 (untyped error), and a
  battery case for a child that returns `rc is None`.
- Either strengthen N1 to a capability-shaped check (typed refusal on the *tampered* file
  plus refusal on the plain original) or state in the claim that N1 is a shape check.

## Artifacts

- `.ufo/waves/round-88/w1/ExecMutation/table.json` — full table (rows, diffs, shas, counter
  probes, control probes, candidate census, base receipt numbers).
- `.ufo/waves/round-88/w1/ExecMutation/report.md` — this file.
- `.ufo/waves/round-88/w1/ExecMutation/receipts/` — `base-receipt.json`,
  `receipt-R01…R07.json`, `receipt-G1…G3.json`, `mutants.json`, `candidate-census.json`,
  `geometry-probe.json`.
- `.ufo/waves/round-88/w1/ExecMutation/harness/` — `mutate.py` (mutant build/run harness)
  and `build_table.py` (table assembler), preserved so the probe is reproducible.
- `.ufo/waves/round-88/w1/ExecMutation.md` — scoped seat report.
