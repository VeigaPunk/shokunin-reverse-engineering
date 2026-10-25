# AScorecardPlan — SCORECARD draft for Round 34 (run-6 re-dispatch), plus attack on the stop record

Seat: `L1Kaidoku34-2.AScorecardPlan` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Prompt read first: `.ufo/waves/round-34/r34b/w2/prompts/AScorecardPlan.md` (first bytes `/skill:godspeed` + verbatim directive).
Mode: read-only verification on copies; the only lane file written is this report. Lane VCS read with `git rev-parse` / `git log` / `git show` / `git ls-files` / `git ls-tree` / `git merge-base` / `git cat-file` only. `python3` = `/usr/bin/python3` (3.14.8). No tool installed or upgraded (no pacman/uv/npm transaction; nothing needed). No network. No ELF carrier, fixture or reader executed as a program of interest; readers ran only as `python3` children of the pinned counters.

Run window (UTC): 2026-10-25T07:33:01Z → 07:56:47Z. All times UTC; host local −03.

**Result in one line:** the stop's decisive counterexample, its six frozen clauses, the F1/F2/F5 repairs and the base absence all reproduce byte-for-byte on copies; F3 and F4 (M3) reproduce as live holes; the stop is **sustained**, but the record carries two conflicts the landed SCORECARD text must reconcile (claim-stop's F4/F5 are substituted in the landed defect paragraph, and `l1_rerun_utc` is forward-dated against the bound receipt). The requested section is drafted below (§7) in the prompt's exact heading form.

---

## 1. Assignment checklist → evidence

| required element | where in this report |
|---|---|
| base | §7 (base `ec3125ad…`, same as attempt-1 round-34 section) |
| inherited stop | §7 (`f432c8e3`; R34-C1 retained, `54a87a51…`) |
| new claim | §7 (R34-C2, capability acquisition, depth) |
| frozen revision | §7 (`c79bbe7b0959132b9873ff3431cf5eb313b58b33`) |
| six clauses met | §4 (exit 0, `clauses_failed=-`, byte-identical recount) |
| decisive counterexample | §3 (`nameset.py`, 8/8 ×3 seeds, hash `2e8feaea…`) |
| five record defects, Landed/Open | §5 (F1–F5) |
| owned scores 10→10, delta 0 | §7 |
| `planned` for round 35 | §7 |
| explicit sentence: no capability row enters | §7 |
| match existing section style | §7; divergences flagged in §6 |

## 2. Environment and inputs

| input | path | sha256 / state |
|---|---|---|
| prompt | `.ufo/waves/round-34/r34b/w2/prompts/AScorecardPlan.md` | first bytes `/skill:godspeed` |
| stop record | `.ufo/waves/round-34/r34b/claim-stop.json` | tracked, added `cd75b92e`; `l1_rerun_utc=2026-10-25T07:28:00Z (approximate)` |
| frozen claim | `.ufo/waves/round-34/r34b/claims.json` | tracked, added `c79bbe7b`; blob `de3afbfb61d70fee…` at `c79bbe7b` |
| before receipt | `.ufo/waves/round-34/r34b/before/c2-at-base.txt` | `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad…`, exit 2 |
| after receipt | `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` | `GATE_COUNTER_OK … clauses_failed=-`; sha256 `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9` (my recount diff: byte-identical) |
| counterexample source | `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` | sha256 `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` — equals stop record `source_sha256` and equals `w1/ExecRedReproduce.md` `r_nameset.py` hash |
| enforced pin container | `.ufo/waves/round-34/r34b/instruments.json` | 26 keys, byte-identical to `claims[0].pins`; added `b917ea64` |
| predicate reconciliation | `.ufo/waves/round-34/r34b/predicate-reconciliation.json` | exists, tracked |
| addendum | `.ufo/waves/round-34/r34b/claim-stop-addendum.json` | tracked, added `5a0435ff`; appendix-only; binds decisive receipts and boundaries-pin receipt |
| wave-2 reports | `.ufo/waves/round-34/r34b/w2/` | 32 seat reports present (incl. `ARerunAll.md`, `AStopFields.md`, `AMutStopRecord.md`) |

Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/AScorecardPlan/` — copy of `tools/round-34`, `nameset.py`, `pathkey.py`, `mini-counter-fresh.py`, `claims.json`, `instruments.json`, `stored-receipt.json`, `claim-stop.json`; all copied with `cp -a`, digests re-checked equal to pins.

## 3. Decisive counterexample — reproduced (8/8, three seeds)

Command (cwd = scratch root; identical to stop-record argv plus `--seed`):

```
/usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader <scratch>/nameset.py --seed <seed>
```

| seed | UTC (start) | exit | matched / met_target |
|---|---|---|---|
| `kaidoku-r34-mini-v1` | 07:33:53Z | 0 | 8 / true |
| `alt-1` | 07:33:54Z | 0 | 8 / true |
| `alt-2` | 07:33:55Z | 0 | 8 / true |

Receipt lines: `{"finding": "records_match", "matched": 8, "met_target": true, …}` — three seeds, exit 0. The reader scans NUL-terminated SONAME-like tokens, sorts the set, keys a memorized name→(flags,value) table; it never reads the header, walks no record array, dereferences no `name_off` (source read: `nameset.py:48-57`). `nameset.py` sha256 `2e8feaea…` matches the stop record and the `ExecRedReproduce.md` artifact. The gate flips to REFUSED when the class is registered (wave-1 `ExecRedReproduce.md` §6; wave-2 `AStopJustified.md` E6: a complete registry kills the claim). Stop substance confirmed.

## 4. Frozen verdict at `c79bbe7b` — reproduced byte-for-byte

```
/usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out <scratch>/c2-recount.json
```

- UTC 07:33:57Z; exit **0**; verdict line `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`.
- Recursive leaf diff `c2-recount.json` vs stored `after/c2-at-instruments.json`: `KEYS_A_ONLY [] KEYS_B_ONLY [] DIFF []` — 30/30 leaves equal; `clauses`, `red`, `green` equal. Six clauses true (`gate_present`, `selftest_clean`, `mutants_killed`, `red_refused`, `green_clean`, `green_positive_meets_target`).
- Base absence re-verified: `git cat-file -e ec3125ad:tools/round-34/replay-gate.py` → `fatal: path … exists on disk, but not in 'ec3125ad…'`, exit 128; the before receipt's `finding=gate_absent` is a property of the revision.

## 5. Five record defects — verification and Landed/Open status

| id | defect (claim-stop) | my verification | status |
|---|---|---|---|
| F1 | claims pins live under `claims[0].pins`; `freeze-integrity.py` requires a top-level `instruments` map and exits 3 `instruments_missing`; no instrument hashes a pinned file | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/claims.json --rev HEAD` → `ERROR schema code=instruments_missing where=instruments`, **exit 3** (07:35:55Z); `instruments.json` → `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=HEAD`, **exit 0** (07:35:55Z); `pins == instruments` = True, 26/26, byte-identical | **Landed** (`b917ea64`); rider: the F1-cited integrity *receipt* (`after/freeze-integrity-instruments.txt`) did not exist at the stop commit — added `5a0435ff`, binds `b917ea64` not `c79bbe7b` (addendum `enforced_pin_receipt.note`; `w2/AMutStopRecord.md` S5) |
| F2 | predicate identity false: claims/config sentence A (31 words, `7c6c17f0…`) vs counter/receipt sentence B (46 words, `8340aea5…`); no instrument reads the predicate value | A hash `7c6c17f0cca6c680507d4eec33b4c0c82a76c4f73e9a98ceb4bde54a9a96279b`; B hash `8340aea51154fc0e4e2c00684a12893603677c5caa7769d7e63b70f5392611c8`; C (mini counter) `09988625205de2eb661235f9019afa70086a26480372c7dd9ec16dc759e9000c`; configs carry A; receipt carries B; `A == B` false | **Open** (disclosed; no post-freeze repair) |
| F3 | shortcut-class drop invisible: removing classes down to `MIN_SHORTCUTS` (3) still returns CLEAN; nothing asserts registered set == pinned set | scratch config with 3 shortcuts (green): `replay-gate.py --root . --config config-floor3.json` → `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=3 shortcuts_over_target=-`, **exit 0** (07:47:17Z) | **Open** (routed QUALITY 70 / M34-8; "assert class count == pinned count before CLEAN" per claim-stop) |
| F4 | gate mutant M3 (ignore last shortcut row) survives its own selftest and turns the red case CLEAN | mutated scratch `replay-gate.py` `for item in config["shortcuts"][:-1]:` (sha256 `9ffbb7e9df0fa6a02da98cb4b6dacef79eeecb099002b8a94805b3d738b78844` — equals `MutGateBranches.md` M3 hash): `--selftest` → `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}`, **exit 0**; frozen red config → `REPLAY_GATE_CLEAN … shortcuts_over_target=-`, **exit 0** (07:47:18Z) | **Open** (routed QUALITY 71 / M34-9; red-last selftest case + row-count assertion) |
| F5 | receipts were untracked at first audit time | `git log --diff-filter=A`: receipts added `b917ea64`; `w1/RevFreezeOrder.md` and `w1/MutGateBranches.md` tracked from `66b84027` (all cited w1 reports tracked as of HEAD `35152484`) | **Landed** (`b917ea64`) |

Extra conflict (not a stop-falsification): claim-stop's `decisive_counterexample.l1_rerun_utc` is `07:28:00Z (approximate)` — 4 m 28 s after the stop commit `cd75b92e` (07:23:47Z) and contradicted by the bound receipt `nameset-green-receipt.json` (stamped `07:34:01Z`; `w2/AStopFields.md` rows 14–15). The addendum binds the receipt but does not rewrite the record's clock.

## 6. What the L1 landed vs this draft

The L1 landed a `## Round 34, run-6 re-dispatch (2026-10-25) — R34-C2 frozen, six clauses met, stopped on an unregistered class` section at `66b84027` (later corrected through `35152484`). It satisfies the assigned elements (base, inherited C1 stop, new claim, frozen revision, six clauses, counterexample, scores 10→10, planned, "no row enters the capabilities table"). Two divergences from the assignment's five-defect contract:

1. The landed defect paragraph lists **six** items and substitutes the relabel/M34-9, no-reader + `met_target`/M34-10, and `--rev`-echo/argv/M34-11 findings for claim-stop's F4 (M3 survivor) and F5 (receipts untracked). Claim-stop's F4 never appears in the landed paragraph (the M3 result is routed under M34-9/QUALITY 71 elsewhere). F5 is absorbed into item (6).
2. The landed paragraph does not mark F1–F5 as Landed/Open as the assignment requests; my draft below does.

Both are disclosed fixes for the L1, not claim changes.

## 7. DRAFT — SCORECARD section (assignment form; append after the attempt-1 Round-34 section)

```markdown
## Round 34 (run-6 re-dispatch)

Base `ec3125ad3d130d92f888a4128dfaa2982f36fff7`; the attempt-1 work and its C1 stop above are inherited through `f432c8e3` and are not rewritten. Outside decision on C1 remains rejected-honest-stop; R34-C1 stays frozen and stopped at `54a87a51a865ab931fd355e767303337b05cccf4` — not re-opened, not re-scored, its production reader and twelve carriers not executed.

One planned claim, **R34-C2 / depth** (capability acquisition): a pre-freeze, config-driven structure-blind shortcut-replay gate for finite structural-decoding counters, making QUALITY 67 executable. Frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33` before any seat or production run (`.ufo/waves/round-34/r34b/claims.json`, blob `de3afbfb…`). Axis basis as frozen: three owned numeric proxies tied at 10, none retired; depth is lowest non-retired; the surface moved is the lane's structural-counter admission instrument, not a numeric proxy score.

P34-shortcut-replay (frozen sentence A, verbatim): "P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a registered structural reader does." The counter's `PREDICATE` constant and receipts carry a longer paraphrase B (46 words, `8340aea5…`); the two sentences are not byte-identical (`predicate-reconciliation.json`), so no identity is claimed here.

| claim / surface | before at base `ec3125ad` | after at the frozen `c79bbe7b` | counting command | verdict / score delta |
|---|---|---|---|---|
| R34-C2 / depth — pre-freeze structure-blind shortcut-replay gate | `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad…`, exit 2 (`r34b/before/c2-at-base.txt`); `git cat-file -e ec3125ad:tools/round-34/replay-gate.py` fails (exit 128), so absence is a property of the revision | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`, exit 0 (`r34b/after/c2-at-instruments.json`, sha256 `da78f444…`); all six clauses true; five controls MISS (max 5 of 6 clauses) | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> --json-out <RECEIPT>` | **falsified measure / honest stop** — the green surface does not force record traversal; owned scores 10→10, delta 0; no capability row enters |

Decisive counterexample: `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` (sha256 `2e8feaea…`), a content-multiset memorization (SONAME-set key + stored name→flags/value table) scoring **8/8 at three seeds** (`kaidoku-r34-mini-v1`, `alt-1`, `alt-2`, exit 0 each) on the frozen `mini-counter.py` without reading a header, a record entry or a `name_off`; independent seats reached the green target by payload-keyed (8/8 with every name byte zeroed), value/offset, record-signature and transform/digest identity-leak readers (`w2/ACounterexample2.md`, `w1/MutShortcutClasses.md`, `w1/LabratSeedSensitivity.md`). Registering any flips the same gate to `REFUSED`, so the refusal mechanism is sound and the registered set was unfaithful to the class space it names. Source: `w1/CtlMultiset-files/nameset.py` (hash equals the `w1/ExecRedReproduce.md` artifact `r_nameset.py`); stop record `.ufo/waves/round-34/r34b/claim-stop.json` (landed `cd75b92e`); receipts `.ufo/waves/round-34/r34b/{before,after,controls}/` (landed `b917ea64`).

Record defects (disclosed; frozen bytes not repaired; F1/F5 landed, F2/F3/F4 open, each routed to a QUALITY row):

| id | defect | status / repair |
|---|---|---|
| F1 | pins live under `claims[0].pins`; `freeze-integrity.py` requires a top-level `instruments` map and exits 3 `instruments_missing`; no instrument hashes a pinned file | **Landed** `b917ea64` (instruments.json, 26 byte-identical pins) + integrity receipt later (`5a0435ff`, binds `b917ea64`); QUALITY 68 |
| F2 | predicate identity false: claims/config A (31 words, `7c6c17f0…`) vs counter/receipt B (46 words, `8340aea5…`); no instrument reads the predicate value | **Open** — disclose only; instruments frozen; QUALITY 68 |
| F3 | shortcut-class drop invisible: dropping classes to the `MIN_SHORTCUTS` floor still returns CLEAN; nothing asserts registered set == pinned set | **Open** — route: assert class count == pinned count before CLEAN (next instrument); QUALITY 70 |
| F4 | gate mutant M3 (ignore last shortcut row) survives its own selftest and turns the red case CLEAN | **Open** — route: red-last selftest case + row-count assertion; QUALITY 71 |
| F5 | receipts were untracked at first audit time | **Landed** `b917ea64`; QUALITY 73 |

Counting command and exact exercised control/argv/UTC/seeds are bound by `claim-stop.json` and the addendum `claim-stop-addendum.json` (decisive receipts `nameset-green-receipt.json`, `payload-keyed-receipt.json`). Independent reproduction this round: nameset 8/8 ×3 seeds (exit 0, 07:33:53Z); frozen counter recount byte-identical to the after receipt (30/30 leaves, exit 0, 07:33:57Z); `freeze-integrity.py` exit 3 on claims, CLEAN pins=26 on instruments (07:35:55Z); F3 floor probe CLEAN exit 0 and M3 selftest 12/12 + red CLEAN exit 0 (07:47:17–18Z). Wave-2 seats independently reran the full matrix (6/6 receipts byte-identical; `w2/ARerunAll.md`).

Owned scores: coverage 10→10, depth 10→10, calibration 10→10, delta 0; **no capability row enters** — a capability needs a passing demonstration in the round that enters it, and this round's demonstration failed. No target/counter/predicate/label change, re-freeze or exploratory relabel is made.

- **planned (round 35, after a steer):** depth or coverage — fresh-content replay counter (`w1/CtlMultiset-files/mini-counter-fresh.py`: 8/8 structural, 0/8 for all nine structure-blind classes) plus the forced-payload-perturbation surface demonstrated by `w1/MutShortcutClasses.md`, frozen with the class set asserted against the pinned set, `met_target == (matched == target)`, digest-bound class entries and a reserved positive-control label; the green surface must vary size, order, payload and name vocabulary together, one class per keyable invariant. Second choice: calibration over the six record defects, counted as mismatches against observed repo state.
```

## 8. Attack verdicts

- **Stop substance: SUSTAINED.** The decisive counterexample (8/8 ×3 seeds), the six frozen clauses (byte-identical recount), the base absence, F1/F2/F5 and both proposed repairs reproduce as claimed. No finding here reopens the claim, changes a clause/target/class/label, or implies any score.
- **Record defects: CONFIRMED and extended.** F3/F4 remain live (reproduced above). The landed SCORECARD paragraph substitutes M34-9/10/11 findings for claim-stop's F4/F5; `l1_rerun_utc` is forward-dated 4 m 28 s past the stop commit and contradicted by the bound receipt (`07:34:01Z`). The addendum binds receipts but does not rewrite the record's clock.
- **No capability or score credit** is awarded; owned scores stay 10→10.

**Verdict: `SCORECARD_DRAFT_READY` — section drafted in the assignment form (§7); all five claim-stop defects verified with Landed/Open status; stop sustained; two record conflicts reported §6/§8 for the L1.**
