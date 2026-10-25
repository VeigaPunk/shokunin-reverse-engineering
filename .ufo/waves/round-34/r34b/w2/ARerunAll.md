# ARerunAll — R34-C2 frozen counter + every control, rerun at the lane tip and the wave-2 tip

Seat: `L1Kaidoku34-2.ARerunAll` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/ARerunAll/`.
Measurement window: **2026-10-25T07:29:49Z … 2026-10-25T07:44:17Z**.
Runtime: `/usr/bin/python3` = Python 3.14.8; `git` 2.56.0; `rsync` 3.5.1. **No tool installed or upgraded; no pacman transaction; no network.**
No file other than this report was written in the lane. No VCS mutation in the lane (clones only). No ELF, fixture or reader was executed as a program of interest: fixtures were read as static bytes; every reader ran as `python3 -I -B` inside a counter (the counter-owned argv or my scratch probe counter).

**Verdict: `RERUN_ALL_REPRODUCED committed_receipts=6/6_byte_identical product=GATE_COUNTER_OK exit=0 controls=5/5_discriminated counterexamples=reproduced provenance=gate_channel_unpinned_reproduced move=no_stop_invalidation`.
The stop's six frozen clauses reproduce byte-for-byte at the lane tip and at the wave-2 tip; every committed control reproduces byte-for-byte; both post-stop decisive classes reproduce at the tip. The stop is not falsified by reproduction — but the counting command cannot prove **which gate** produced its receipt (independently reproduced below), and four observation-level defects remain (P2–P4 and the name-specific red clause).**

---

## 1. Axes named

| axis | question | outcome |
|---|---|---|
| reproduction fidelity | do the six committed receipts reproduce byte-identically in a fresh clone? | yes, 6/6 JSON + 6/6 verdict lines |
| tip invariance | does the wave-2 tip change any clause? | no; identical output at every observed tip |
| provenance strength | does the receipt prove the revision and the gate it names? | **no** — `--rev` is an unverified label and `--gate` is unpinned (P1/P5) |
| control discrimination | does each control fail the clause the claim predicts? | **2 of 5 predicted clause failures are wrong** (P2) |
| decisive-evidence reachability | do the stop's counterexample receipts reproduce? | yes (nameset 4 seeds; payload-keyed plain + zeroed) |

## 2. Method and containment

* **Stop tip** `cd75b92e583735729546b0ea3b250f2df6d0652a` (the commit that landed `claim-stop.json`): `git clone --no-hardlinks --quiet <LANE> <scratch>/tip-cd75b92e`; clean working tree, 0 modified files.
* **In-flight wave-2 worktree** (no wave-2 commit existed yet at 07:32:10Z): `rsync -a --exclude .git --exclude __pycache__ <LANE>/ <scratch>/wave2-inflight-20261025T073210Z/`. 26/26 instrument pins matched in the snapshot.
* **Wave-2 tip, first commit** `66b840274390d0868c913a544947f9eb40a4ffe6` — fresh clone.
* **Wave-2 tip, second commit** `5a0435ffb9a8921206144e0b61fe3c12a89b59c2` (bind the stop's decisive receipts) — fresh clone.
* **Wave-2 tip, measured** `417a8211398e4fcb05e9d311af1877a702327b20` — fresh clone, full matrix at 07:38:30–07:38:57Z. The tip kept moving while this seat ran: observed sequence `cd75b92e → 66b84027 → 5a0435ff → 417a8211 → b62b4767 → 39f433b2 → c05984e7 → debc8dad`; at report finalization (07:44:50Z) HEAD was `debc8dad18c0e962626b9165df6bd77b4302daee`. `git diff 417a8211..debc8dad -- tools .ufo/waves/round-34/r34b/{after,controls,claims.json,claim-stop.json,instruments.json}` is **empty**; the only evidence-side change is append-only text in `claim-stop-addendum.json` (it gained Y1–Y5 at `39f433b2`; unchanged since). 26/26 pins match at HEAD. The closure must re-pin the commit it closes on; the invariance argument here is the empty instrument diff plus the pin check, not an assumption.
* **Base tip** `ec3125ad3d130d92f888a4128dfaa2982f36fff7` — fresh clone, detached, to reproduce `before/c2-at-base.txt`.
* One matrix script drives identical argv at every root: `<scratch>/run-matrix.sh`. Every invocation is logged with `ARGV`, `START_UTC`, `END_UTC`, `EXIT` in `<scratch>/receipts-*/<label>.cmd` (exact argv preserved there verbatim).

## 3. Side by side: committed receipt vs fresh clone vs wave-2 tip

Production argv (all roots):
`/usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out <receipt>.json`

| check | committed receipt (line) | fresh clone @cd75b92e (exit, UTC) | wave-2 tip @417a8211 (exit, UTC) | identity |
|---|---|---|---|---|
| C2 production counter | `after/c2-at-instruments.txt`: `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` | exit **0**, 07:30:19–07:30:22Z | exit **0**, 07:38:30–07:38:32Z | **JSON byte-identical to `after/c2-at-instruments.json`; line identical** |
| production counter, `--rev cd75b92e` | (none; probe) | exit 0, 07:30:22–07:30:24Z | exit 0, 07:38:32–07:38:35Z | identical except `measured_revision` |
| C2 before receipt | `before/c2-at-base.txt`: `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad3d130d92f888a4128dfaa2982f36fff7 gate_path=tools/round-34/replay-gate.py` | exit **2**, 07:34:07Z (counter from tip-cd75b92e, `--root <base clone>`) | exit **2**, 07:35:39Z (counter from tip-66b84027, same base root); not rerun from 417a8211 because the instrument bytes are identical | **line identical** |
| control do-nothing | `controls/do-nothing.txt` | exit **2**, 07:30:24Z | exit **2**, 07:38:35Z | **JSON + line identical** |
| control always-clean | `controls/gate-always-clean.py.txt` | exit **1**, 07:30:24–07:30:27Z | exit **1**, 07:38:35–07:38:38Z | **JSON + line identical** |
| control vacuous-no-floor | `controls/gate-vacuous-no-floor.py.txt` | exit **1**, 07:30:27–07:30:29Z | exit **1**, 07:38:38–07:38:40Z | **JSON + line identical** |
| control no-positive-check | `controls/gate-no-positive-check.py.txt` | exit **1**, 07:30:29–07:30:32Z | exit **1**, 07:38:40–07:38:43Z | **JSON + line identical** |
| control junk-clean | `controls/gate-junk-clean.py.txt` | exit **1**, 07:30:32Z | exit **1**, 07:38:43Z | **JSON + line identical** |
| gate selftest (direct) | embedded `selftest_line` in `after/c2-at-instruments.json` | exit 0, 07:30:32Z | exit 0, 07:38:43Z | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}` identical |
| gate green (direct) | embedded `green.line` | exit 0, 07:30:32–33Z | exit 0, 07:38:43–44Z | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` identical |
| gate red (direct) | embedded `red.line` | exit 2, 07:30:33–34Z | exit 2, 07:38:44–45Z | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization` identical |

The same matrix was also run at the in-flight worktree snapshot (07:32:16–07:32:38Z), at `66b84027` (07:34:54–07:35:10Z) and at `5a0435ff` (07:35:58–07:36:14Z): all five roots (those four plus `417a8211`) produce the same six receipts byte-identically. The only inter-clone delta anywhere is the absolute `config`/`root` strings embedded by `replay-gate.py` in the *uncommitted direct* `gate-green.json` / `gate-red.json`; the committed receipts do not carry those fields.

Exact argv for the five controls (same production argv as above, plus one override; run with cwd = the root under test):

```
--gate tools/round-34/absent-gate.py
--gate .ufo/waves/round-34/r34b/controls/gates/gate-always-clean.py
--gate .ufo/waves/round-34/r34b/controls/gates/gate-vacuous-no-floor.py
--gate .ufo/waves/round-34/r34b/controls/gates/gate-no-positive-check.py
--gate .ufo/waves/round-34/r34b/controls/gates/gate-junk-clean.py
```

## 4. Control exits and the clause each control fails

| control | counter exit | clauses_failed (observed) | claim's predicted failure (`claims.json.control_plan`) | match |
|---|---|---|---|---|
| do-nothing (`--gate tools/round-34/absent-gate.py`) | 2 | n/a (`finding=gate_absent`, not a MISS) | `finding=gate_absent, exit 2` | yes |
| always-clean | 1 | `red_refused,selftest_clean` | red clause fails | yes |
| vacuous-no-floor | 1 | `selftest_clean` only | **`UNEVALUABLE`, MISS** | **no — it returns MISS, not UNEVALUABLE, and the gate's own red/green runs are both normal** |
| no-positive-check | 1 | `mutants_killed,selftest_clean` | **green clause fails** | **no — `green_clean=true`, `green_positive_matched=8`; only the selftest catches it** |
| junk-clean (fixed prints) | 1 | `red_refused` only | red clause fails | yes |

Observation (P2): on the **production** path the positive-control branch only fires when the *real* structural reader misses the target, which it does not; disabling the branch is therefore invisible to the green clause and only the selftest's `positive-below` case sees it. The `gate-no-positive-check.py` selftest also reports `no-positive-check-anchor-missing` (a pre-mutated gate cannot be re-mutated at the same needle), so its `mutants_killed=2` is produced by two mechanisms, not purely by the branch. The pristine gate's selftest is clean (0 failures, 3/3 mutants killed).

Observation (P3): the junk gate that prints fixed `{"cases":12,"failures":0,"mutants_killed":3}` passes `selftest_clean` **and** `mutants_killed`, and its fixed red payload (no `classes_over_target`) passes `green_clean`; only `red_refused` refuses it. The counter's `green.shortcuts_below_target` for that run is `0` (computed from the payload's one structural row, `c2-shortcut-gate-counter.py:109`) while the gate's printed line says `7` — the field is payload-derived and is **not a clause**.

## 5. Counterexample reproduction at the wave-2 tip (417a8211)

| reader | class | counter | seed | matched/target | exit | UTC |
|---|---|---|---|---|---|---|
| `w1/CtlMultiset-files/nameset.py` (`sha256 2e8feaea…`) | content-multiset (SONAME-set key) | mini (green) | `kaidoku-r34-mini-v1` | **8/8** | 0 | 07:38:45–46Z |
| same | same | mini | `alt-1` | **8/8** | 0 | 07:38:46Z |
| same | same | mini | `alt-2` | **8/8** | 0 | 07:38:46Z |
| same | same | mini | `alt-3` (addendum's fourth seed) | **8/8** | 0 | 07:37:48Z (tip 5a0435ff) |
| same | same | naive (red) | default | **8/8** | 0 | 07:38:46Z |
| `w1/CtlMultiset-files/pathkey.py` | path/digest identity | mini (green) | default | **0/8** | 1 | 07:38:46Z |
| same | same | naive (red) | default | **8/8** | 0 | 07:38:46Z |
| `w1/CtlMultiset-files/payload_keyed.py` (`sha256 0e125169…`) | payload signature (count + ordered (flags,value)) | mini (green) | default | **8/8** | 0 | 07:38:57Z |
| same, names zeroed | same | scratch probe counter (zeroes `names_off..EOF`, runs reader as python, compares to `expected.json`) | n/a | **8/8**, all eight `zeroed_sha256` **byte-identical to `payload-keyed-receipt.json`** | 0 | 07:38:57Z |
| `readers/structural.py` | structural (positive control) | mini (green) | `kaidoku-r34-mini-v1` | **8/8** | 0 | 07:38:46Z |
| same, names zeroed | structural | scratch probe counter | n/a | **0/8** (8 rows, reader exit 0, answers wrong) | probe 1 | 07:38:57Z |

Every transformed fixture the nameset run saw was a **permuted copy** with a different digest from the pinned fixture (`transformed_sha256` c7adf97f…, ee5b4266…, f4ad00ab…, be4be5e7…, 48c701c7…, be1f1fba…, 398e12c9…, 80078364…; all 512 bytes), so the 8/8 is not a pass-through of original fixture bytes.

Class-registration probe (scratch copy of the green config + `{"class":"content-multiset","path":"…/nameset.py"}`, 8 shortcuts; **pinned config untouched**):
`/usr/bin/python3 -I -B tools/round-34/replay-gate.py --root . --config <scratch>/gate-config-nameset-registered.json --json-out <scratch>/receipts-tip417a/gate-nameset-registered.json`
→ **`REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=content-multiset`**, exit **2**, UTC 07:44:16–07:44:17Z (`gate-nameset-registered.json`, `sha256 556ff0b0…`, 9 rows). The frozen CLEAN is a function of the registered set, as the stop says.

## 6. Provenance probes that bear on the stop's evidence

**P1 — `--rev` is a label, not a measurement (independently confirms the addendum's X4).** `c2-shortcut-gate-counter.py:73` writes `"measured_revision": args.rev`; the file makes no `git` call (only `subprocess.run` for the gate, lines 36/73–80). Probe: same root = the `ec3125ad` clone (which contains **no** `tools/round-34` at all — `git ls-tree`), run once with `--rev ec3125ad…` and once with `--rev c79bbe7b…`:
* `--rev ec3125ad…` → `…measured_revision=ec3125ad3d130d92f888a4128dfaa2982f36fff7…`, exit 2
* `--rev c79bbe7b…` → `…measured_revision=c79bbe7b0959132b9873ff3431cf5eb313b58b33…`, exit 2
Both measure the same bytes. Consequence: `measured_revision` in any C2 receipt cannot establish which tree was measured; only the byte pins can. For this round the pins do establish it: the seven inspected instrument files are byte-identical at `c79bbe7b` and `cd75b92e` (`git show <rev>:<path> | sha256sum`), and all 26 pins match at every root I cloned (cd75b92e, 66b84027, 5a0435ff, 417a8211, c05984e7, debc8dad). The verdict is not undermined; the field is decorative and the closure should not cite it as provenance.

**P5 — the counting command's `--gate` channel is unpinned and a file-opaque mock gate passes all six clauses (independently reproduces the addendum's critical finding Y1).** Scratch `mock-gate.py` (`sha256 54451ee6…`, 1.7 KB, opens no file and reads no `--root`) decides only on the config basename the counter passes:
`/usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev 0000000000000000000000000000000000000000 --gate <scratch>/mock-gate.py --json-out <scratch>/receipts-tip417a/mock-gate-probe.json`
→ **`GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`**, exit **0**, all six clauses `true`, `measured_revision=0000…`, `gate_path=<scratch>/mock-gate.py`, UTC 07:41:29Z. The receipt does record `gate_path`, so the substitution is visible — but `GATE_COUNTER_OK` does not check it, and `gate_present` only tests that the named file exists. A production-legal `--gate` override is therefore enough to synthesize the receipt shape without the pinned gate ever running.

**P6 — the enforced container does not reach the claim freeze (independently reproduces the addendum's Y3).** `freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/instruments.json --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33` → `freeze-integrity: ERROR no commit adds .ufo/waves/round-34/r34b/instruments.json at c79bbe7b…`, exit **2** (07:41:29Z). CLEAN is only obtainable from `b917ea64` onward (`freeze=b917ea64`), so the container audits the pins as they stood *after* they were restated, not the freeze commit itself.

**P2/P3** — see §4.

**P4 — the `before` receipt is a root swap.** `ec3125ad` has no `tools/round-34` (`git ls-tree ec3125ad tools/` ends at `round-33`), so the committed `before/c2-at-base.txt` was produced by a later counter with `--root <base>` (the counter is invoked from another tree). The line reproduces exactly, but it does not demonstrate that the counter existed or ran "at" `ec3125ad`.

## 7. The five disclosed record defects plus F6, adjudicated by reproduction

| id | stop's statement | my probe | verdict |
|---|---|---|---|
| F1 | frozen pins live under `claims[0].pins`; `freeze-integrity.py` wants top-level `instruments`, exits 3; repair = `instruments.json` + receipt | `freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/claims.json --rev cd75b92e` → `ERROR schema code=instruments_missing …` exit **3**; with `--claims …/instruments.json` → `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=cd75b92e…`, all 26 rows `commits_after_freeze=0`, exit **0**. The committed receipt `after/freeze-integrity-instruments.txt` (`sha256 d68e4e17…`) **did not exist at `cd75b92e`** (not in the stop commit's tree); it appears in `5a0435ff` and its digest matches `claim-stop-addendum.json`. | defect real; container repair works; the receipt was bound **after** the stop, as the addendum discloses. `freeze=b917ea64 ≠ c79bbe7b` because the container postdates the freeze. |
| F2 | predicate identity false: claims/config sentence A vs counter/receipt sentence B | sha256 of the three predicate sentences: A (claims + both gate configs, 237 chars) `7c6c17f0cca6…`; B (counter `PREDICATE`, 351 chars) `8340aea51154…`; C (`mini-counter.PREDICATE`, 214 chars) `09988625205d…`. A==config true; A==counter false. | confirmed. The counterexample is indeed scored under A and C (the mini-counter compares to `expected.json` under C). No instrument reads the predicate value. |
| F3 | dropping classes to the `MIN_SHORTCUTS` floor still returns CLEAN; nothing asserts set equality | source: `replay-gate.py:58` only enforces `len(shortcuts) >= 3`; no pinned-count comparison anywhere in `load_config`/`evaluate`; the counter's clauses (§3) contain no class-count term. My 8-class scratch run proves the converse direction (adding a class changes the verdict). | confirmed at source level; **not executed** by me (a 3-class scratch config is a one-line probe any closure can repeat). |
| F4 | gate mutant M3 (ignore last shortcut row) survives its own selftest and turns the red case CLEAN | pristine selftest reproduces 12 cases / 0 failures / 3 mutants killed. I did not build the M3 mutant; the committed wave-1 evidence `w1/MutGateBranches.md` carries it. | not reproduced by me (out of my assignment); the pristine selftest is sound. |
| F5 | receipts were untracked at first audit | at `cd75b92e` all six receipts are tracked (`git ls-files`); `git diff 66b84027..5a0435ff` touched no `after/`/`controls/` file except adding the freeze receipt. | repaired and observable. |
| F6 | deterministic public seed + published per-copy digest name ⇒ identity/digest replay reaches 8/8 without decoding | source-confirmed: `mini-counter.py` `--seed` default `kaidoku-r34-mini-v1`; target name `opaque-<sha256(transformed)[:20]>.data`; digest recorded in each row. My `pathkey.py` run still scores 0/8 because it keys on the *input* basename/digest, not on the published *output* name/digest — F6's exploit needs the reader to read the counter's own receipt, which `pathkey.py` does not do. | mechanism confirmed at source level; **not exploited** by the committed readers I reran. |

## 8. What this reproduction does and does not say about the stop

* **Supports the stop.** The six frozen clauses hold, byte-identically, at the lane tip and at every observed wave-2 tip. Every committed control reproduces. Both post-stop decisive classes reproduce at the tip, including the addendum's payload-keyed receipt with all eight zeroed digests matching. The registered-class probe refuses the unregistered class. Nothing here revives the claim or moves a clause.
* **Does not falsify the stop.** I found no reproduction in which the production counter returns `GATE_COUNTER_OK` at a root whose instrument bytes differ from the pins, and no control that turns into a pass.
* **Reproduction-visible defects, classified against the record as filed.** The stop record (`cd75b92e`) disclosed F1–F5; the append-only addendum (landed `5a0435ff`, extended at `39f433b2`) adds F6, X1–X5 and Y1–Y5. My probes independently reproduce F1's container mechanics, F2's predicate divergence, X4/P1, Y1/P5 and Y3/P6; F3 and F6 are source-confirmed only (§7). Each item below is marked *already disclosed* or *not in the addendum text read*:
  1. **X4/P1** `measured_revision` is an argv echo and no counted run reads VCS (§6). **Already disclosed (X4); independently reproduced.**
  2. **Y1/P5** the `--gate` channel is unpinned and a 1.7 KB file-opaque mock gate yields `GATE_COUNTER_OK` with all six clauses and a forged rev (§6). **Already disclosed (Y1, critical); independently reproduced with a receipt** (`mock-gate-probe.json`).
  3. **Y3/P6** the enforced container exits 2 at the claim freeze and verifies only from `b917ea64` (§6/§7). **Already disclosed (Y3); independently reproduced.**
  4. **P2** two of the five `control_plan` predictions name the wrong failing clause (no-positive-check → green; vacuous → UNEVALUABLE). The controls still produce MISS, so discrimination holds, but the claim text is wrong about *why*. Not found in the addendum text read at 07:36–07:41Z.
  5. **P3** a fixed-print gate clears `selftest_clean` + `mutants_killed` + `green_clean`; only `red_refused` refuses it, and the counter's `green.shortcuts_below_target` disagrees with the gate's printed line (0 vs 7). The clause set is not independently discriminative for a gate that fabricates its own selftest output. Not found in the addendum text.
  6. **P4** the `before` receipt is a root swap over a tree that never contained the counter (§6). Related to X4 but distinct in that the committed receipt's `finding=gate_absent` is an artefact of the root choice. Not in the addendum text.
  7. The counter's `red_refused` clause is **name-specific**: `c2-shortcut-gate-counter.py:116` requires the literal `"label-memorization"` in `classes_over_target`. A different shape-only class over target in the red config would not satisfy the red clause. With P5, the clause is also satisfiable by a gate that simply prints the name. Not exercised (the frozen red config contains exactly that class), but the red clause measures *this one reader label*, not "a shape-only counter" as predicate sentence A says. Not in the addendum text; source-level.

## 9. Unrun, limits, risks

* **Unrun:** `tools/round-34/freeze-integrity.py --selftest` (not the C2 counter); the M3/mutant reconstructions owned by wave-1 (F4); the `mini-counter-fresh.py` fresh-content sweep (the addendum explicitly does not claim it as this round's evidence); any execution of the R34-C1 production reader or its twelve carriers (forbidden).
* **F3** is source-confirmed only; **F6** is source-confirmed only (see §7).
* The wave-2 tip is a **moving target**: it advanced through `cd75b92e → 66b84027 → 5a0435ff → 417a8211 → b62b4767 → 39f433b2 → c05984e7 → debc8dad` during this seat. The measured tip is `417a8211`; every later commit I observed leaves the restricted evidence paths (`tools`, `after`, `controls`, `claims.json`, `claim-stop.json`, `instruments.json`) byte-identical (the addendum gained text at `39f433b2` only), and 26/26 pins hold at HEAD. The closure should re-pin whatever commit it closes on and can reuse `<scratch>/run-matrix.sh` unchanged.
* Scratch is 2.8 GB (five clones + one rsync snapshot) under `/fast/scratch/…`; it may be reclaimed. Every receipt and line quoted here is in the report, and the committed receipts are byte-identical, so the report stands alone.

## 10. Evidence pointers (scratch)

| path | content |
|---|---|
| `<scratch>/run-matrix.sh` | the exact matrix (argv per command) |
| `<scratch>/receipts-tip/` | fresh clone @cd75b92e, 07:30:19–07:30:35Z |
| `<scratch>/receipts-wave2/` | in-flight worktree snapshot, 07:32:16–07:32:38Z |
| `<scratch>/receipts-tip66b/` | @66b84027, 07:34:54–07:35:10Z |
| `<scratch>/receipts-tip5a04/` | @5a0435ff, 07:35:58–07:36:14Z; `extra/` = nameset alt-3, payload plain/zeroed/structural |
| `<scratch>/receipts-tip417a/` | @417a8211 (measured wave-2 tip), 07:38:30–07:38:57Z; `extra/` payload probes |
| `<scratch>/receipts-base/before-ec3125ad.{json,stdout}` | before receipt reproduction, 07:35:39Z |
| `<scratch>/payload-probe-counter.py` | scratch counter for the zeroed-name probe (reader run only as python) |
| `<scratch>/mock-gate.py` (`sha256 54451ee6…`) | file-opaque probe gate for P5/Y1 |
| `<scratch>/receipts-tip417a/mock-gate-probe.json` (`sha256 4a418e7c…`) | the forged `GATE_COUNTER_OK` receipt (all six clauses true, `measured_revision=0000…`) |
| `<scratch>/gate-config-nameset-registered.json` (`sha256 0b5f1ba2…`) | copy of the green config plus `content-multiset` (pinned config untouched) |
| `<scratch>/receipts-tip417a/gate-nameset-registered.json` (`sha256 556ff0b0…`) | REFUSED with `classes_over_target=[content-multiset]` |
| `<scratch>/wave2-inflight-20261025T073210Z/` | rsync snapshot (no `.git`, no `__pycache__`) |

Receipt digests at the measured wave-2 tip (`sha256sum` of `<scratch>/receipts-tip417a/*.json`):
`prod-rev-frozen da78f444…`, `prod-rev-tip 0cc17186…`, `ctl-do-nothing bce6aa9f…`, `ctl-always-clean 22f819c4…`, `ctl-vacuous-no-floor a12f720d…`, `ctl-no-positive-check 50516d79…`, `ctl-junk-clean 25485cb9…`. All six digests are identical to the receipts produced at `cd75b92e` (`<scratch>/receipts-tip/`) — the whole set is invariant across roots.

## 11. Final verdict line

`RERUN_ALL_REPRODUCED committed=6/6_byte_identical product=GATE_COUNTER_OK selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 controls=5/5_discriminated counterexamples=nameset_8/8_x4seeds,payload_keyed_8/8_names_zeroed_digests_identical,structural_zeroed_0/8,nameset_registered_REFUSED stop_tip=cd75b92e wave2_tip_measured=417a8211 pins=26/26 exit=0 utc=2026-10-25T07:44:17Z provenance_probes=X4/P1_reproduced,Y1/P5_forged_GATE_COUNTER_OK_reproduced,Y3/P6_reproduced defects_new=P2_control_plan_expectation,P3_fixed_print_gate,P4_before_root_swap,P_red_name_specific stop_invalidated=no`
