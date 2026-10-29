# MutC1Counter — round 50, attempt 2, wave 4 (falsify): the C1 miss is the RULE's, not the extraction's

**Seat:** `MutC1Counter` (mutation-tester). **Lane:** `kaidoku-shokunin` @ `c67b741e8f6bd8d64adbdb15e059d47fde004c77`
(the landing measured is rev `646d29c9df4ef77499248f95589cb9526c6dea19`; freeze `435d41fd4ad9211d1579fc447936fb33d2b74467`).

## VERDICT

**The kill-rule framing is CONFIRMED: the frozen gap rule's `char-device` clause is exactly what decides
the miss. The extraction is NOT at fault. Three independent single-point mutations of that one clause
each take the score from 2/4 to 4/4 carriers, and the fourth arm (same rule mutation + the promotion
block the honest stop withheld) reaches exit 0.**

**But the prompt's stated expectation is only half right, and the correction matters for the L1:
mutating the gaps clause alone gets `carriers_matched 4` — NOT exit 0.** The counter's `met_target`
also requires the **documentation bindings**, and at the landing rev `PROVINCE.md` carries
`## Round-50 measured, not promoted (R50-C1 honest stop)` instead of `## Round-50 additions to Core`.
So `province_core_section` and `province_core_row` are false, `met_target` stays false and the exit
code stays 1 even at 4/4 carriers. The second red axis is **independent of the rule** and is the
consequence of the honest stop itself.

Two further corrections to the framing, both load-bearing:

1. **The prescribed command cannot score.** `c1-counter.py --no-rerun` exits **2** with
   `reason: rerun_disabled` ("P50-C1 binds a fresh REA run of each carrier; --no-rerun cannot be
   scored") for the pristine counter **and** for both mutants, with **byte-identical stdout**
   (sha256 `02ecc8d5d42e398e0528a44e72b36d5fe46448f6c0334f72ae232dca23193c45`). `--no-rerun` is a
   refusal, not a scoring mode; the expected `carriers_matched 4` is unreachable through it. The
   counterfactual therefore has to be run through the counter's own `measure()` with the rerun clause
   supplied by the counter's **own sanctioned replay technique** (below).
2. **A mutated counter cannot be scored against the real freeze at all.** `measure()` compares the
   running counter's sha256 to `tools/round-50/c1-counter.py` at the freeze and raises
   `CounterNotFrozen` otherwise. Arm A5 (M1 bytes against a pristine freeze) exits **2**,
   `reason: counter_not_frozen`. So each mutant needs a synthetic freeze carrying the mutant bytes.

## Ground truth (measured, not assumed)

The frozen rule (`tools/round-50/gap-rule.json` @ freeze) is the whole story:

```
"allowed":   {"symlink":["unpublished-entry"], "char-device":["unpublished-entry"], "block-device":[], ...}
"required":  {"symlink":true, "char-device":true, "block-device":false, "fifo":false, "socket":false, "dir":false}
"removed":   {"diagnostic":"MaliciousSymlinkRemoved","kinds":["symlink"],"disposition":"exclusive",
              "silent":{"char-device":["247:0"]}}
```

The oracle tables give **13** `char-device` rows on `g7581`/`g7582` (details `247:0`, `136:0`–`136:7`,
`230:0`, `3:0`–`3:2`) against **1** on each Cable carrier (`247:0` at `dev/led`). The receipts carry
**no gap and no removal for any of them** (`unpublished_entries` kinds = `['symlink']` only; no
published file under `dev/`). The rule admits `247:0` silently and requires the other twelve to carry
a disposition — so `gaps_ok` is false on exactly the two carriers with 13 devices.

**No coverage was lost.** For `g7581`/`g7582`: 13 char-device oracle rows, **0** of them published at
their own path (`published dev/* = 0`), and the counter's separate materialisation clause
`nonregular_unpublished_ok` is **true** on all four carriers. Every frozen-oracle **regular** file is
published (`oracle_hits == oracle_files`: 4556/4564/4709/3955, `extra_published []` everywhere). The
extraction is complete; the rule is what rejects it.

**The extractor's behaviour is IDENTICAL on the passing and the failing carriers** — this is the
strongest form of the exoneration, because it leaves no room for a carrier-specific extraction
defect:

| carrier | gaps reported | unpublished_entries | diagnostics | oracle char-device rows | `gaps_ok` |
|---|---|---|---|---|---|
| c6490 (passes) | `depth-limited:1`, `unpublished-entry:612` | `symlink:612` | `MaliciousSymlinkRemoved:1` | 1 | true |
| c6430 (passes) | `depth-limited:1`, `unpublished-entry:567` | `symlink:567` | `MaliciousSymlinkRemoved:1` | 1 | true |
| g7581 (fails) | `depth-limited:1`, `unpublished-entry:636` | `symlink:636` | `MaliciousSymlinkRemoved:3` | 13 | false |
| g7582 (fails) | `depth-limited:1`, `unpublished-entry:636` | `symlink:636` | `MaliciousSymlinkRemoved:3` | 13 | false |

All four report **only** symlink gaps / symlink unpublished entries and **only**
`MaliciousSymlinkRemoved` diagnostics; **no carrier** reports a device entry of any kind. The two
passing carriers pass **only** because their single device detail (`247:0`) happens to be in the rule's
silent whitelist — the extractor does not treat them differently. The only variable that differs is
the **rule**, and the only other difference is the **oracle's device count** (1 vs 13).

**The rule is a generalisation that does not generalise.** The predecessor rule
(`.ufo/waves/round-41/c1/gap-rule.json` @ freeze) has `required.char-device: false` and `silent: {}`.
Round 50 flipped `required.char-device` to `true` and added the `silent` whitelist `["247:0"]` — a
whitelist of exactly the one detail the **Cable** carriers carry. The two Fritz!Box carriers carry 12
more device details; the whitelist does not cover them, and the rule's `required` demand is then
unsatisfiable. The entry itself already states this ("generalised at the freeze from one carrier
class"); this seat measured that it is the sole decider of the carrier score.

## The counterfactual, and how it was run

The rerun clause was replaced by the counter's **own** sanctioned technique, not by a weakening of it:
the frozen counter's selftest helper is documented as *"a real run whose output is the given envelope
(projection-equal by construction): used to isolate a rule clause from the rerun clause"*, and the
frozen counter's own `rehost()` builds that second-run shape. The harness calls the frozen
`measure()` unchanged and injects `rerun=<rehost replay of the committed receipt>`. **No REA run
happens** (the contract forbids one here); every other clause — all 23 per carrier, all 9 bindings,
the evidence-id recompute, the frozen-table and drift checks — is the frozen counter's own code.
The oracle re-derivation uses the counter's own `rederive_oracle` (`/usr/bin/unsquashfs` 4.7.5),
memoised on disk across arms.

Each arm gets a synthetic two-commit repo whose trees are the **real lane trees** (A0's rev tree is
byte-identical to `646d29c9^{tree}`, sha `a41e12e561af228e44c0e4adcfdfb6892e60d5eb`), with one
mutation applied identically at both commits so `frozen_path_changed` stays `[]` in every arm.

| arm | mutation (one behaviour-bearing point) | counter sha256 | matched | failing | exit | met_target |
|---|---|---|---|---|---|---|
| **A0** | none (baseline: the landed state) | `9820811b…` | **2**/4 | `g7581:gaps_ok`, `g7582:gaps_ok` | 1 | false |
| **A1** | M1: `need = False` for `char-device` in `disposition_check` | `a0adbdf6…` | **4**/4 | `[]` | 1 | false |
| **A2** | M2: any `char-device` admitted **silently** | `85547228…` | **4**/4 | `[]` | 1 | false |
| **A3** | M3: the frozen **rule** `required.char-device → false` | `9820811b…` (pristine counter) | **4**/4 | `[]` | 1 | false |
| **A4** | A3 + `PROVINCE.md` gains `## Round-50 additions to Core` | `9820811b…` | **4**/4 | `[]` | **0** | **true** |
| **A5** | M1 bytes scored against a **pristine** freeze | `a0adbdf6…` | — | — | **2** `counter_not_frozen` | — |

**A0 reproduces the L1's score exactly** (`carriers_matched 2`, the same two failing clauses) — the
harness is faithful to the real measurement. A1/A2/A3 are three *independent* single-point mutations
(one in the counter's code, one in the counter's code via a different mechanism, one in the frozen rule
**data** with the counter untouched) and all three land on **4/4 with `failing: []`**. A4 shows the
same 4/4 carriers plus the promotion block the honest stop withheld ⇒ **exit 0, `met_target true`**.

So: **the frozen `char-device` clause is the sole decider of the carrier-level miss** — mutating it
in the counter or in the rule alone yields 4/4, and the extraction is exonerated (all oracle regular
files published, nothing materialised, no extra file).

## Findings

| # | finding | evidence | severity |
|---|---|---|---|
| F1 | The frozen `required.char-device` clause (with its one-detail `silent` whitelist `["247:0"]`) is exactly what decides the 2/4. Mutating that clause alone — in the counter (A1, A2) or in the rule file (A3) — yields `carriers_matched 4`, `failing: []`. | A1/A2/A3 receipts above; `probe.json` (frozen `disposition_check` on the landed receipts: frozen model → `gaps_ok` false on g7581/g7582; `required.char-device=false` → true on all four; widened silent → true on all four) | **high** — confirms the kill-rule framing |
| F2 | **The mutation does not make the score green.** `met_target` also requires the documentation bindings, and at the landing rev `PROVINCE.md` has `## Round-50 measured, not promoted (R50-C1 honest stop)`, not `## Round-50 additions to Core`. `province_core_section` and `province_core_row` are false ⇒ exit stays **1** at 4/4 carriers (A1–A3). Only A4 (rule + promotion block) reaches exit 0. | `arm-A1/A2/A3.json` `bindings_false: ["province_core_section","province_core_row"]`; `arm-A4.json` `bindings_false: []`, exit 0 | **high** — the L1 must not read "4/4" as "green"; the second red axis is independent of the rule and is the honest stop's own doing |
| F3 | **The prescribed command cannot score.** `--no-rerun` exits 2 (`rerun_disabled`) with byte-identical stdout for pristine and both mutants. The counter's own routing text says so: *"`--no-rerun` is not a mode of the predicate: it exits 2 (`rerun_disabled`) and never reports met."* | `pres-{pristine,M1,M2}.stdout`, all sha256 `02ecc8d5…` | **medium** — the seat prompt's expectation is unreachable as written |
| F4 | **A mutated counter cannot be scored against the real freeze**: `measure()` requires the running bytes to equal `tools/round-50/c1-counter.py` at the freeze. M1 against a pristine freeze → exit 2, `counter_not_frozen`. Any counterfactual must re-freeze. | `arm-A5.json`: `"the running counter (a0adbdf6…) is not tools/round-50/c1-counter.py at the freeze (9820811b…)"` | **medium** — structural constraint on any round-51 repair |
| F5 | **The landed narrative overstates its own receipt.** The entry and `PROVINCE.md` both say *"the counter's own REA rerun reproduced the projection on all four carriers"*, but the landing receipt records `g7581:projection_ok = **false**` with `code: execution_failure`, `ENOENT … readlink '…/usr/www.myfritz/avme/cgi-bin/luacgi'` — the rerun **died**, it did not reproduce. The receipt's own `failing` list has three entries, not two: `['g7581:gaps_ok','g7581:projection_ok','g7582:gaps_ok']`. | `c1-after-attempt2.json` `carriers.g7581.projection_ok=false`, `projection_error.error.code=execution_failure`; `failing` has 3 entries; entry + PROVINCE.md:442 carry the "reproduced … on all four carriers" sentence | **high** — a landed claim contradicted by its own receipt; the prompt repeats it ("the counter's own REA rerun reproduced every projection") |
| F6 | The g7581 `projection_ok` failure is an **environment flake, not a semantic difference**: REA's own `readlink` hit ENOENT on a file its extractor had already removed. The counter only retries `provider_timeout` (round 50, `MAX_REA_ATTEMPTS=3`), so this flake is scored as a clause failure rather than exit 2 `rerun_env_error`. That is why the landing's carrier count is 2/4 for **two** independent reasons on g7581. | `arm-A0.json` / L1 receipt `projection_error` (ENOENT readlink under the rerun outdir) vs `MAX_REA_ATTEMPTS` retry limited to `provider_timeout` | **medium** — the rerun clause is fragile to a non-timeout REA error |
| F7 | The counter's own **selftest cannot detect this defect — proven by source analysis, not inferred.** The kinds appearing in the selftest's fixture rows are exactly `{'device', 'symlink'}`; `'char-device'` appears in **no** fixture row. So M1/M2's mutated branch `if kind == 'char-device'` (a 2-line / 3-line addition) is **never evaluated true in any selftest case** — the frozen battery cannot bite on the exact clause that decided the round's miss. The only two `'char-device'` occurrences in the file (4718, 4721) sit in the `--selftest-rea` fixture, not the disposition battery. | fixture-kind enumeration: `{'device','symlink'}`, `'char-device'` absent; `c1-counter.py:2915,2919,4062` use kind `'device'`; `4718,4721` are the only `'char-device'` and sit in `selftest_rea`; true diffs: M1 = 2 added lines, M2 = 3 added lines | **medium** — instrument coverage gap; the repair must add a `char-device` fixture case, not just a rule change |
| F8 | The pre-data **POS control was already red** on the frozen fixtures (`carriers_matched 2`, `exit 1`, `verdict: misbehaved`, "expected exit 0, got 1") — the same defect, measured before the data run, with the same two failing carriers and the same char-device clause. The kill rule did not fire (`kill_rule_fires: false`). | `.ufo/waves/round-50/controls-attempt2/summary.json` `CTL-C1-POS: {carriers_matched: 2, exit_code: 1, verdict: "misbehaved"}`, `failures: ["CTL-C1-POS"]`; `pos/counter.json` `failing: ['g7581:gaps_ok','g7582:gaps_ok']`, `bindings_false: []` | **high** — the misbehaviour was pre-existing and available before the data run; the POS fixture itself is the counterfactual that this seat reproduced (A4 ≡ POS + fixed rule) |
| F9 | The rule's `required` map is **not self-consistent**: `gap_rule_model`'s own default is "a kind with a non-empty `allowed` list is required", so `allowed['fifo']=['unpublished-entry']` would make `fifo` required by default — the rule overrides it to `false`, while `allowed['char-device']` non-empty plus `required['char-device']=true` makes it required. The same `allowed` list therefore yields opposite verdicts for `fifo` and `char-device` purely by the `required` override. | `c1-counter.py:776-778` (default rule) vs `gap-rule.json` `allowed`/`required`; `dir` (empty allowed) is not required and passes with 349 unaccounted rows | **low** — a latent inconsistency a round-51 rule rewrite should settle |
| F10 | **Calibration of any proposed repair: a partial widening does NOT fix the miss.** The frozen rule already admits `247:0` silently, so the unaccounted set is **twelve** details (`136:0`–`136:7`, `230:0`, `3:0`–`3:2`), not eleven. Measured with the frozen `disposition_check`: widening `removed.silent['char-device']` to `247:0` + **five** details leaves `gaps_ok` false on g7581/g7582 (7 still unaccounted) — **identical to the frozen rule**; only all **thirteen** details, or `required['char-device']=false`, or the counter-code mutations (A1/A2) turn it green. A repair that widens the whitelist partially will look like it worked and silently not. | `probe.json` + the four-model probe run (F / M4 five-detail / M5 five-detail+required=false / M6 all-thirteen): M4 → `{g7581:False,g7582:False,c6490:True,c6430:True}` = frozen; M5, M6 → all true | **medium** — a trap for the round-51 repair; a widened whitelist must be carrier-class complete |

**On the prompt's framing "the extraction is not at fault": confirmed**, with one qualifier — the
extraction is complete **for regular files** (every frozen-oracle regular file published on all four
carriers, no extra file, nothing materialised), and it is *silent* about device entries on all four
carriers including the two Cable ones that pass. The rule, not the extraction, is what differs between
"pass" and "fail": the same extractor behaviour is accepted on the Cable carriers (whose only device
detail `247:0` is whitelisted) and rejected on the Fritz!Box carriers.

## Commands, exit codes, hashes

All under scratch `S=/fast/scratch/hyaku/kaidoku-r50/w4-MutC1Counter` (`TMPDIR=$S`), `python3 -I -B`.

**Prescribed command (per the prompt), for pristine and both mutants — exits 2, no score:**
```
python3 -I -B $S/c1-counter-<v>.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 646d29c9df4ef77499248f95589cb9526c6dea19 --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work $S/w-pres-<v> \
  --carrier-cache /fast/scratch/hyaku/kaidoku-r50/carrier-cache --json-out $S/pres-<v>.json --no-rerun
```
| v | exit | stdout sha256 | stdout |
|---|---|---|---|
| pristine | 2 | `02ecc8d5d42e398e0528a44e72b36d5fe46448f6c0334f72ae232dca23193c45` | `{"detail": "P50-C1 binds a fresh REA run of each carrier; --no-rerun cannot be scored", "reason": "rerun_disabled"}` |
| M1 | 2 | `02ecc8d5…` (identical) | identical |
| M2 | 2 | `02ecc8d5…` (identical) | identical |

**Counterfactual arms** (harness `harness.py` = frozen `measure()` + the counter's own `rehost` replay;
`--derived-cache` shared so `unsquashfs` runs once per carrier):
```
python3 -I -B $S/harness.py --counter $S/c1-counter-<v>.py --root $S/repo-<A> --rev <rev> --freeze <freeze> \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --carrier-cache /fast/scratch/hyaku/kaidoku-r50/carrier-cache --work $S/w-<A> \
  --derived-cache $S/derived --out $S/arm-<A>.json --label <A>
```
| arm | counter bytes | freeze | rev | exit | matched | failing | receipt sha256 (file) |
|---|---|---|---|---|---|---|---|
| A0 | `9820811b…` | `56eec8a6…` | `056dc42d…` | 1 | 2/4 | `g7581:gaps_ok`,`g7582:gaps_ok` | `cf6d94ca253328b189be3d6176bc3736bde18b4415dffa5f0acd46b4cf9e58e4` |
| A1 | `a0adbdf6…` | `388f0f3c…` | `5f756070…` | 1 | 4/4 | `[]` | `5f5682706b5bb63e959ad9d06f67d3ff36942ba93a384851fd32d5fc07919df3` |
| A2 | `85547228…` | `310e90d3…` | `3a58dc05…` | 1 | 4/4 | `[]` | `f221f3391a2bc42b72924bc727d7074fa33f24076c7f29104565b75b6139d369` |
| A3 | `9820811b…` | `e34577f2…` | `2eda395b…` | 1 | 4/4 | `[]` | `764d8bcf0250bda20a4c50e26159f1419156ba95934c3d8cac40036f5b4d8272` |
| A4 | `9820811b…` | `6239f751…` | `51781a74…` | **0** | 4/4 | `[]` | `0955b27b8894d505701130b62f8c4250f7c2975de43ef2a7e3019ec82f72316d` |
| A5 | `a0adbdf6…` | `799b688a…` | `a9b76f2e…` | **2** | — | — | `96b98523d1e9428f9f6fbcf67920758b773f6562f49fb89fbaf8ba7ee56fa80d` |

All arms: `frozen_path_changed []`, `carriers_unchanged true`, `gap_rule_unchanged true`,
`frozen_tables_valid true`, `gap_rule_problems []`.

**Minimal decisive probe** (`probe.py`, no git write, frozen counter imported read-only):
`python3 -I -B probe.py` → exit 1 (frozen model has `gaps_ok` false on g7581/g7582);
`probe.json` sha256 `797cc09bf9f0516391bf0289a844f285536397de3543891d67abf8c9578b7f7a`.
Frozen model: `g7581/gaps_note = "required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0' … 'dev/pts/7']"`.
`required.char-device=false` → `gaps_ok` true on all four; widened silent → true on all four.

**Mutant diffs** (`mutants.json`; full diffs in the artifact dir):
- M1 `c1-counter-M1.py` sha256 `a0adbdf6764132bc99a4e953dea6e92990bbaf48a79effe88d409f5ccb826c50`
  (frozen `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`):
  `+        if kind == 'char-device':` / `+            need = False` in the required loop.
- M2 `c1-counter-M2.py` sha256 `855472283443883c63c8aa18f818751c101dc4511d3343f5f552f3598336e74e`:
  `+        if kind == 'char-device':` / `+            silent_admitted.append(rel)` / `+            continue`.
- M3 `gap-rule-M3.json` sha256 `2d8182a7bd51beaa7b7c062a577ed82d87695e15d693491a3ca64745241c80c3`:
  `-  "char-device": true,` / `+  "char-device": false,`.

**Restoration / non-mutation evidence.** The lane tree was never written: `git status --porcelain` in
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` shows only sibling seats' untracked `.ufo/waves/round-50/w4/*`
artifacts (not mine — mine are listed below), and the frozen files are byte-unchanged:
`tools/round-50/c1-counter.py` = `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`,
`tools/round-50/gap-rule.json` = `43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef`.
Every mutant lives only in the scratch dir and in this seat's artifact dir. No git commit/push/stash
was run in the lane or the fleet repo; all synthetic commits are in `$S/repo-A*`, whose rev tree for
A0 is byte-identical to the real `646d29c9^{tree}` (`a41e12e561af228e44c0e4adcfdfb6892e60d5eb`).

## What the L1 should take from this

1. **The kill-rule framing survives the attack**: the frozen `char-device` clause is the sole decider of
   the carrier-level 2/4, and the extraction is exonerated. A1/A2/A3 are three independent
   single-point counterfactuals, all 4/4.
2. **Do not read "4/4" as "green"** (F2). At the landing rev the documentation bindings
   (`province_core_section`, `province_core_row`) are independently false because the honest stop wrote
   `## Round-50 measured, not promoted` instead of `## Round-50 additions to Core`. Exit 0 needs the
   promotion block too (A4). Any round-51 repair that re-freezes the rule must also land the Core
   section, or the counter still exits 1 for a different reason.
3. **F5 is a correction to the landed record, not a new defect.** The entry and `PROVINCE.md` claim the
   REA rerun "reproduced the projection on all four carriers"; the landing receipt says
   `g7581:projection_ok = false` (REA `readlink` ENOENT — a flake, F6) and its `failing` list has
   three entries. The prompt repeats the same sentence. Whatever the next round writes, it should not
   repeat it.
4. **F7/F8 tell you where the detection gap was**: the frozen selftest's fixtures spell the device kind
   `'device'`, so it never exercises the `'char-device'` clause that decided this round's miss; the
   pre-data POS control was red (2/4) and the kill rule did not fire on it.

## Not run / limits (honest scope)

- **No REA run** (contract: the C1 counter's full predicate command is L1-owned; `--no-rerun` is a
  refusal). The rerun clause was neutralised by the counter's own replay technique, so
  `projection_ok` is true by construction in every arm. The L1's own receipt shows the *real* rerun
  failed on g7581 for an unrelated reason (F6), so a real rerun of the mutant may score **3/4**
  (`g7581:projection_ok` false again) even with the rule fixed — the mutation result above is the
  rule clause in isolation, which is what the seat asked for.
- The counter's `--selftest` **mutant-kill run did not complete in this seat's window** and is **not
  reported as a result**. Three facts about it are recorded honestly because they matter for anyone
  repeating it:
  - **My first attempt was contaminated and is discarded.** Two runs shared one
    `tools/round-50/c1-counter.py` path, and the battery builds each fixture freeze from the
    **working-tree** counter bytes (`c1-counter.py:3006`), so the second variant's bytes made the first
    run's fixtures report `counter_not_frozen` (91 failures, all `counter_not_frozen`). The discarded
    output is **not** reported as a result. The re-run used one isolated tree per variant
    (`$S/st-<variant>/tools/round-50/c1-counter.py`), sequentially.
  - The **pristine** battery **did** complete on its own isolated tree: 169 cases (17 green,
    152 red), `failures []`, **zero** `counter_not_frozen` — i.e. the frozen battery is green over the
    frozen rule, uncontaminated. The M1 and M2 mutant batteries did not finish inside the window (host
    contention: ~90 sibling node processes) and are **not** claimed.
  - **F7 does not depend on any selftest run**: it is a static reachability fact over the selftest's
    own fixture rows (the kinds present are `{'device','symlink'}`; `'char-device'` appears in none),
    which makes the mutated branch unreachable in every case regardless of how a run ends.
- The **A-arm verdict does not depend on the selftest at all** — the harness calls the frozen
  `measure()` directly (`harness.py:149`); the selftest appears only as the documented source of the
  replay technique.
- `--selftest-rea` (real REA selftest) not run — needs REA and a dev image.
- `git log`/`git show` on the lane were read-only; no lane write, no commit, no push.

## Artifacts

`.ufo/waves/round-50/w4/MutC1Counter/` — `arm-A0..A5.json` (per-arm receipts),
`probe.json` + `probe.py` (minimal decisive probe), `probe-models.json` (the five rule models of F10:
sha256 `a936e4e5bdedfcd16867ef60b736556c314c3f1c1a9848a6e863b19cbe18d5c1`),
`mutants.json` + `mutate.py` (mutant builder and diffs), `harness.py` (counterfactual harness),
`build_trees.py` + `arms.json` (synthetic repo builder),
`c1-counter-frozen.py`, `c1-counter-M1.py`, `c1-counter-M2.py`, `gap-rule-frozen.json`,
`gap-rule-M3.json`, `pres-*.stdout` / `pres-*.json` (prescribed-command receipts).

Tooling: no install or upgrade was needed (no `uv tool`/`npm`/`pacman` action in this seat).
