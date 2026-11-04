# MutSelftest — round 69 w1 counter mutation (attack the counters, not the claims)

Seat: `MutSelftest` (leaf; no subagent dispatch). Assignment: is each frozen counter able to fail?
Write only under `.ufo/waves/round-69/w1/MutSelftest/` and scratch
`/fast/scratch/hyaku/kaidoku-r69/MutSelftest/`. No tracked lane file, fleet-repo file, jj/git index,
commit or push was touched. Nothing was installed or upgraded (no tool was needed).

Report path per seat spec: `.ufo/waves/round-69/w1/MutSelftest.md` (this file). Full table:
`counters.md`. Evidence: `evidence/`.

## 1. Inputs and their state (observation)

| file | declared sha256 | measured at HEAD `3f3d20fc` | after all runs |
|---|---|---|---|
| `tools/round-69/mutation-check.py` | `51b64c56…56d33c2` | equal | equal |
| `tools/round-69/contract-probe.py` | `e609d85d…69661d` | equal | equal |
| `tools/round-69/controls.py` | `1f8f78c1…196b918` | equal | equal |
| `tools/round-69/packed-elf.py` | `4ac0d83b…8f8aebcc` | equal | equal |
| `tools/round-68/packed-elf.py` | kept byte-identical at `48ef4c68…` | equal | equal |

`git show HEAD:<tool>` equals the working-tree bytes for all four round-69 instruments and for
`tools/round-68/packed-elf.py` at the measured revision used here (`3f3d20fc`, the wave-spec commit;
the tool blobs are the frozen bytes). Frozen files were re-hashed after every mutant run; the hashes
never changed. Mutants were written only under scratch.

Host facts used by the fixtures (observation): `upx 5.2.0`, `/usr/bin/upx` sha256
`cf2f6e7c…9aa8c969`, matching `UPX_VERSION_PIN`/`UPX_SHA256_PIN`; `/usr/bin/jq`, `/usr/bin/xxd`,
`/usr/lib/libz.so.1.3.2` all present and `readelf -h`-parsable; Python 3.14.8; the C2 base replay
(`evidence/base-replay/c2-r68-0of6.json`) reproduces `arms_passed 0` of 6 naming all six arms.

## 2. Method

Ten required mutations (assignment items 2a–2c, 3a–3c, 4a–4b = eight) plus five frontier mutants
(`ok-drops-wrong`, `a5-drop-carrier-ok`, `c1-do-nothing-flip`, `control-ok-drop`,
`ceiling-075-drop`) = **13 mutants**. Each is a single-site replacement of frozen bytes; the
builder asserts the old string occurs exactly once, records the first changed line, and hashes
frozen and mutant bytes (`evidence/results.json`).

Every row runs **frozen counter** and **mutated counter** on the **same fixture**; a mutant counts as
a counter survivor only when the mutated counter returns a green consequence (ok / met / 6-of-6 /
validate 0) on a fixture the frozen counter rejects. Fixtures are scratch git repos
(`fixtures/crash`, `fixtures/m5`, `fixtures/route-a3`, `fixtures/route-ok`, `fixtures/root-C1..C3`)
plus JSON receipts built from this host's pinned sources. `evidence/harness.py` is the full driver;
`evidence/logs/` keeps every raw counter payload.

Positive controls were run so a false green cannot be blamed on the fixture: a compliant route plus
a fully formed receipt scores 6/6 (`B0`), and an in-bounds synthetic three-carrier receipt scores
`met true` (`D0`) under the frozen counter and under the mutants that should ignore a defect there.

## 3. Result in one line (observation)

**All 13 mutated counters produce the wrong verdict on a fixture the frozen counter rejects; none is
caught by the counter's own verdict field.** The guards split by artifact: six by a receipt-field
predicate clause (C1-A1 all-five-by-name, C1-A2 failed-names-case, C1-A3 all-five-killed, C1-A5
cases-20, C3-D1 `control_ok`, C3-D2 ratio-0.75; C1-A2 is also caught by the C1 kill rule's "a syntax
error is not a gate" and C3-D2 by the C3 kill rule), two by the C2 kill rule's carrier conditions
(C2-B2 format, C2-B3 carrier-ok), two by the declared do-nothing controls (C1-A4
`c1-constant-battery`, C2-B4 `c2-constant-probe`), one by the C2 base-instrument clause (C2-B1), and
three only by re-scoring the claim directly instead of trusting the controls suite (the three
controls flips). No mutation here falsifies R69-C1/C2/C3 as frozen — the frozen counters are correct artifacts and
reproduce their declared base states — but the matrix names exactly which clauses carry the guard.

Base reproduction (observation, this seat's runs):

- `evidence/base-replay/c1-r68-at-base.json`: r68 patch set vs round-68 at `d7d9a62c` → `ok true`,
  `survivors` the five, `killed []`, `pristine.cases 13`.
- `evidence/base-replay/c2-r68-0of6.json`: probe vs round-68 + `c2-at-landing.json` → `arms_passed 0`
  of 6, all six named, exit 1.
- `evidence/base-replay/c3-r68-receipt.json`: `--check-receipt` on the round-68 receipt → `met false`,
  `target 2`, `kinds [null]`, exit 1.
- Frozen battery vs the frozen round-69 route at HEAD: `ok true`, five `killed`, `pristine.cases 20`,
  exit 0 (`A1-row-drop--real-instrument/frozen`).

## 4. Attack on R69-C1 (`mutation-check.py`)

Mutations and exact lines (`counters.md` has the full rows):

- **C1-A1, line 69** — delete the `M5_control` row from `PATCH_SETS["r69"]`. Fixture: the frozen
  route with only the `arm-pack-control-false` case (and its `REGISTERED_CASES` entry) removed, so
  M5 survives while M1–M4 are killed. Frozen: exit 1, `survivors ["M5_control"]`. Mutated: exit 0,
  `survivors []`, four mutant rows. **False green.** The frozen `--validate` accepts the four-row
  receipt (rc 0), and on the *real* frozen route the mutated counter also exits 0 with `killed`
  listing four names instead of five — the counter's `ok` cannot distinguish "M5 killed" from
  "M5 never run".
- **C1-A2, line 145** — a kill is any non-zero rc once a case is declared; the `failed` list is no
  longer required. Fixture: an instrument whose pristine `--selftest` prints `cases 20`, `ok true`
  and whose five patched arms raise before printing JSON. Frozen: exit 1, `killed_wrong_case` all
  five. Mutated: exit 0, `killed` all five with `failed: null`. **False green**, and the frozen
  `--validate` still accepts that receipt (rc 0). The C1 predicate's "each kill's `failed` list
  naming its declared arm-false case" and the kill rule's "(a syntax error is not a gate)" are the
  only guards.
- **C1-A3, line 158** — `ok` drops `and not wrong`. Same crash fixture. Frozen: exit 1. Mutated:
  exit 0 while the receipt still lists all five as `killed_wrong_case` and `killed []`. **False
  green**; the predicate's "all five mutants killed" is the guard, not the counter.
- **C1-A4, line 184** — `--validate` accepts an empty mutant list. Fixture: the fabricated battery
  receipt used by `c1-constant-battery` (`mutants: []`, `survivors: []`). Frozen: validate rc 1,
  `"mutants absent or empty"`. Mutated: rc 0, no defects. **False accept.** The declared do-nothing
  control `c1-constant-battery` (which expects validate rc 1) is the only executable guard.
- **C1-A5, coverage gap (no mutant needed)** — the frozen battery's pristine gate checks
  `rc == 0` and `ok is true`, not `cases == 20`. Observed in C1-A1's frozen run: a 19-case
  instrument whose selftest is green passes as `pristine_ok: true, pristine.cases 19`. The
  predicate's explicit "`pristine.cases 20`" is the guard.

Verbatim clauses that stop these: predicate — "reports `survivors []` with all five mutants `killed`
and each kill's `failed` list naming its declared arm-false case … and `pristine.cases 20` with
`pristine.ok true`"; kill rule — "Any survivor, any kill whose `failed` does not name the declared
case (a syntax error is not a gate), a pristine selftest not green, a patch site that matches zero or
several times, a before-arm that does not show the five survivors". Note the kill rule does not
literalise a row inventory ("a patch site that matches zero or several times" is only checked for
sites that remain in `PATCH_SETS`), so C1-A1 hangs on the predicate's "all five mutants killed"
being evaluated *by name*; the receipt keeps the names, so a name-based reading catches it.

## 5. Attack on R69-C2 (`contract-probe.py`)

- **C2-B1, line 204** — A3 passes on any exit 2. Fixture: a route that refuses both bad packers but
  reports the fake upx as a work problem, plus a fully formed receipt. Frozen: 5/6, `A3` named, exit
  1. Mutated: 6/6, exit 0. **False 6-of-6.** The C2 before-arm clause does catch this one: the same
  mutant scores the round-68 base instrument 1 of 6 (`evidence/base-replay/c2-mutant-a3-rc-only-at-base.json`),
  so the predicate's "reports `arms_passed 0` of 6" fails. This is the one C2 mutant where the
  before-arm is load-bearing.
- **C2-B2, line 114** — A5 stops treating a missing `format` as a defect (and stops sub-scripting it
  in the `seen` record). Fixture: compliant route + receipt whose `libz` carrier has no `format`.
  Frozen: 5/6, `A5` named. Mutated: 6/6, exit 0. **False 6-of-6.** The before-arm does **not** catch
  it (base stays 0 of 6 — the round-68 carriers are also missing `name`/`packing_mode`, so the
  mutated A5 still fails there). The only guard is the kill rule "a receipt whose carrier
  pins/formats/modes do not equal the probe's own derivation from the pinned source bytes", applied
  to a receipt the probe no longer derives for. If the verifier trusts `arms_passed 6`, this
  mutation is invisible.
- **C2-B3, line 129** — A5 stops requiring carrier `ok` and arm truth. Fixture: receipt with `xxd`
  `ok:false`. Frozen 5/6; mutated 6/6. **False 6-of-6.** Same before-arm blindness (0 at base);
  guard is the kill rule's "a carrier arm false", read from the receipt.
- **C2-B4, line 236** — `--validate` accepts an arm with an empty `observed` dict. Fixture: six arm
  rows, `observed {}` everywhere. Frozen: validate rc 1 with six `no observation` defects. Mutated:
  rc 0. **False accept**; `c2-constant-probe` is the executable guard.

Also observed: the frozen probe `--validate` accepts a receipt with `ok:false`, `rev:"deadbeef"`,
`instrument:"nope.py"`, `instrument_sha256:"00…"`, `target:99` (rc 0) — it checks arm structure and
`arms_passed`/`failed` agreement only. The claim's R69-C2 predicate names only arm identities and
truth values, not what each arm must observe, so once the probe bytes are wrong the predicate alone
cannot see B2/B3: the receipt's carrier fields are the only trace, and the claim's kill rule is what
must be applied to them. This is the sharpest asymmetry found: **C1 and C3 predicates describe
receipt-level evidence; C2's predicate describes only the probe's own booleans.**

## 6. Attack on R69-C3 (both the controls driver and the checker)

Against `controls.py`:

- **C3-C1, line 146** — `c3-do-nothing` ok when `--check-receipt` returns 0. Fixture: stub root whose
  checker accepts the round-68 receipt (`met true`, rc 0) — i.e. the exact do-nothing the control
  exists to reject. Frozen suite: exit 1, `c3-do-nothing: false`. Mutated: exit 0, all seven green.
- **C3-C2, line 150** — `c3-loose-ceiling` expects 0. Fixture: stub root whose checker accepts a 0.9
  ceiling. Frozen: exit 1, `c3-loose-ceiling: false`. Mutated: exit 0, all seven green.
- **C3-C3, line 103** — `c1-do-nothing` ok when `survivors == 0`. Fixture: stub root whose battery
  reports zero survivors. Frozen: exit 1, `c1-do-nothing: false`. Mutated: exit 0, all seven green.

Each single flip certifies a do-nothing counter with the whole seven-arm suite green. The suite has
no independent re-derivation: every observed value is the counter's own output.

Against `packed-elf.py --check-receipt`:

- **C3-D1, line 285** — drop `control_ok is True`. Fixture: in-bounds three-carrier receipt with
  `control_ok:false`. Frozen: `met false`. Mutated: `met true`. **False met.** The checker's output
  does not echo `control_ok`, so the C3 predicate's "`control_ok true`" must be read from the
  receipt; that clause is the guard.
- **C3-D2, line 303** — drop the `ratio > 0.75` comparison. Fixture: receipt with `libz`
  `before_ceiling_ratio 0.9`. Frozen: `met false`. Mutated: `met true`. **False met.** Guarded by
  the predicate's "every carrier's `before_ceiling_ratio` at or below 0.75" and the kill rule's "a
  ceiling ratio above 0.75", again only if the receipt is read.

## 7. Guard-chain summary (which frozen artifact catches which counter mutant)

| claim | counter mutant | counter output | predicate sentence | kill rule | do-nothing control | base/before clause |
|---|---|---|---|---|---|---|
| C1 | A1 row drop | green | **yes**, by name | no (site never probed) | no | no |
| C1 | A2 weak verdict | green | **yes** (`failed` must name case) | **yes** ("syntax error is not a gate") | no | no |
| C1 | A3 ok-drops-wrong | green | **yes** (all five killed) | no | no | no |
| C1 | A4 validate-empty | accept | **yes** (empty receipt lacks five kills) | no | **yes** (`c1-constant-battery`) | no |
| C1 | A5 cases 19 | `pristine_ok true` | **yes** (`pristine.cases 20`) | no | no | no |
| C2 | B1 A3-any-rc | 6/6 | no | no | no | **yes** (base becomes 1 of 6) |
| C2 | B2 A5-no-format | 6/6 | no | **yes**, textual | no | no |
| C2 | B3 A5-no-carrier-ok | 6/6 | no | **yes**, textual | no | no |
| C2 | B4 validate-no-observation | accept | no | no | **yes** (`c2-constant-probe`) | no |
| C3 | D1 control_ok drop | met true | **yes** (receipt `control_ok`) | no | no | no |
| C3 | D2 ceiling drop | met true | **yes** (receipt ratio) | **yes** ("ratio above 0.75") | no | no |
| C3 | controls C1/C2/C3 flips | suite green | only if the claim is scored directly, not via controls | — | — | the C3/C1 base clause, if scored directly |

Consequence for the wave: the counting commands' exit codes are necessary but not sufficient
evidence. A verifier that consumes `ok:true` / `met:true` / `arms_passed:6` / `--validate rc 0`
without reading the receipt against the predicate is exposed to every row above. The frozen
receipts in `evidence/logs/` show exactly the fields a sentence-based reading needs
(`mutants[].failed`, `pristine.cases`, `arms[].observed`, `carriers[].format`, `carriers[].ok`,
`control_ok`, `before_ceiling_ratio`).

## 8. Gaps beyond the assigned mutations (observation / inference)

- Observation: both `--validate` implementations are structural only; neither binds `ok`, `rev`,
  `patch_set`, `instrument`, `instrument_sha256`, `target`, `expected_survivors` or `survivor_count`.
  Forged receipts passed both (rc 0). This matches their docstrings ("structural honesty"), so the
  finding is that they must not be used as the claim gate.
- Observation: the C1 battery's pristine gate accepts a 19-case green selftest; the 20-case pin is
  the predicate's, not the counter's.
- Observation: `controls.py` has no independent derivation; every arm trusts the counter's JSON.
- Inference (code read, not run): `mutation-check.run_selftest` and `contract-probe.invoke` pass
  `timeout=300`/`timeout=900` to `subprocess.run` without catching `TimeoutExpired`; a hanging
  instrument would escape as a traceback with exit 1, not the documented exit 2 ("could-not-
  evaluate"). Not exercised here (a 300 s hang was out of bounds for this seat).
- Inference (code read): A2's unwritable-work arm depends on a non-root process (`chmod 0500` still
  writable as root). Observed passing as the current non-root user; root behaviour is unknown.
- Inference (code read): A5/A6 are host-coupled — they re-derive carrier pins from
  `carriers[].source` and the packer from `/usr/bin/upx`, so a receipt measured on a different host
  fails A5/A6 even when correct. The measured run must use this host's pinned sources.
- Unknown: the L1's after-arm had not landed a measured C2 receipt at the time of this seat
  (`.ufo/waves/round-69/l1/scores/` was empty); whether the after-arm is scored by the counting
  commands alone or also against the predicate text is not something this seat can observe. The
  matrix above says what each choice buys.

## 9. Reproduction

Driver (recreates all fixtures, mutants, receipts and logs from the frozen bytes; writes only under
scratch):

```sh
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-69/w1/MutSelftest/evidence/harness.py
```

Single-mutant illustration (frozen vs mutated validator on the same fabricated receipt):

```sh
python3 -I -B tools/round-69/mutation-check.py --validate <receipt>   # rc 1, "mutants absent or empty"
python3 -I -B <mutant>/mutation-check/validate-empty.py --validate <receipt>   # rc 0
```

Base replay commands used (read-only git; scratch work dirs):

```sh
python3 -I -B tools/round-69/mutation-check.py --root . --rev d7d9a62cc70935304e600ed0dee864fc4f1751f7 \
  --tool tools/round-68/packed-elf.py --patch-set r68 --work <scratch> --json-out <receipt>
python3 -I -B tools/round-69/contract-probe.py --root . --rev d7d9a62cc70935304e600ed0dee864fc4f1751f7 \
  --tool tools/round-68/packed-elf.py --pkg <REA 6.5.0 root> --work <scratch> \
  --receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json --json-out <receipt>
python3 -I -B tools/round-69/packed-elf.py --check-receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json
```

## 10. Evidence bundle

| path | contents |
|---|---|
| `evidence/results.json` | mutant index (frozen/mutant sha256, first changed line, note) and every frozen-vs-mutant record |
| `evidence/harness.py` | the driver that built fixtures, mutants and the matrix |
| `evidence/mutants/` + `SHA256SUMS` | the 13 mutant sources, hashed |
| `evidence/logs/` | raw counter payload for every run (frozen and mutant) |
| `evidence/receipts/` | fixture receipts: complete / missing format / carrier-not-ok / no-observation probe / fabricated battery / forged validators / A1, A2, A4 receipts / C3 met, loose, control-false |
| `evidence/base-replay/` | C1 r68-at-base, C2 r68 0-of-6, C3 r68 receipt, C2 mutants at base |
| `counters.md` | the full mutation table and the survivor list for the next freeze |

Scratch lifecycle: created at `/fast/scratch/hyaku/kaidoku-r69/MutSelftest/`, all evidence copied
here first, then the scratch tree removed (`rm -rf`). Nothing outside this seat dir, the scratch
dir, and read-only `git show`/`git log` on the lane repo was written; no commit, checkout, add,
reset or jj command was issued. No tool was installed or upgraded.

Every conclusion above is marked observation, inference or unknown; an unrun check is listed as
inference, not as a pass.
