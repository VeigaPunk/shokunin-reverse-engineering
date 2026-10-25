# R34b w2 — AMutStopRecord: can the lane's own bytes catch a mutated stop record?

**Seat:** `L1Kaidoku34-2.AMutStopRecord` (mutation-tester). **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Subject:** `.ufo/waves/round-34/r34b/claim-stop.json` (blob `544209aa32f6f38e3152bdf16c8e563621538a75`, sha256 `e6303d061da219bb100f3a9acfc7492c9880acc177c4b98f5b695392b5cbcbfc`), landed `cd75b92e583735729546b0ea3b250f2df6d0652a`.
**Scratch:** `/fast/scratch/hyaku/kaidoku-r34b/w2/AMutStopRecord/` (clone, pristine capture, mutants, receipts, `probe-summary.json`).
**UTC window:** 2026-10-25T07:27Z–07:35Z. **Lane writes:** this file only; the lane VCS, instruments, receipts and docs were read-only.

## 1. Axes
1. **Record checkability by committed instruments** — does any executable in the tree assert a fact in `claim-stop.json`?
2. **Doc-anchor coverage** — which mutated field has a committed document that contradicts it, at which revision?
3. **Containment / restoration** — exact bytes before and after, no lane mutation.
4. **Evidence reproducibility** — do the record's own numbers and its frozen-verdict line reproduce?

## 2. Method
A `git clone` of the lane was taken into scratch (`git clone --no-hardlinks …/kaidoku-shokunin lane`; clone HEAD was then `cd75b92e`, i.e. the stop commit; `git status` clean). Pristine bytes were captured and verified. Five mutants were written one at a time as minimal structural edits (`json.dumps(indent=1, sort_keys=True)+"\n"` reproduces the original file byte-for-byte, verified: round-trip sha = `e6303d06…`), each state run through every committed detector, then restored.

Exact detector argv (cwd = scratch clone):

| id | argv | pristine exit / output |
|---|---|---|
| D1 | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/instruments.json --rev cd75b92e583735729546b0ea3b250f2df6d0652a` | **0** — `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=cd75b92e…` (07:31:54Z) |
| D2 | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev cd75b92e583735729546b0ea3b250f2df6d0652a --json-out <scratch>/gate-S0_pristine.json` | **0** — `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` (07:31:54Z) |
| D3 | pin-map scan: `instruments.json` keys, `claims.json` `claims[0].pins` keys, `grep -rn claim-stop tools/` | 26 pins / 26 pins / **0** stop keys / **empty** grep |
| D4 | outside-reader comparator (not committed anywhere; `probe.py:d4_outside`): source existence, `sha256(source)` vs `source_sha256`, rerun of the record's own argv at its three seeds vs `observed` | see §4 |
| D5 | doc cross-read (not committed; `doc-anchor` grep over `SCORECARD.md`, `LOG.md`, `SKILL.md`, `corpus/lessons/round-34.md`) | see §5 |

Baseline reproduction of the record's evidence (same clone):

- Three separate invocations, one per seed (`--seed kaidoku-r34-mini-v1`, `--seed alt-1`, `--seed alt-2`): `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py --seed <SEED>` → **exit 0**, `"matched": 8, "met_target": true, "finding": "records_match"` for all three (log `baseline-nameset.txt`).
- `frozen_counter_verdict.line` equals `after/c2-at-instruments.json`'s fields exactly (checked programmatically: `record.line == receipt.line: True`; receipt exit 0, `measured_revision: c79bbe7b…`).

So the record's empirical core is real and reproduces; this probe tests custody, not truth.

## 3. Mutants and committed-detector results

| state | mutation | file sha256 | D1 | D2 | D3 | committed instrument noticed? |
|---|---|---|---|---|---|---|
| S0 pristine | — | `e6303d06…b5cbfc` | CLEAN 0 | OK 0 | no anchor | — |
| M_a | `"verdict": "falsified measure; honest stop …"` → `"verifies"` | `ce60602446e5a2183739afd80db2a15cc1ee3d1e2c9f082caea1a0404b4fb6ca` | CLEAN 0 | OK 0 | no anchor | **no** |
| M_b | `observed.matched 8→0`, `met_target true→false`, all three seed counts 8→0 | `d490845ad4b90ee40b58d5dec5d573b96a6c6145b2eb8412c8a66dc58aa82eb1` | CLEAN 0 | OK 0 | no anchor | **no** |
| M_c | `source` nameset.py → `tools/round-34/mini-fix/readers/structural.py` (sha/argv untouched) | `36664964fccfa49006a36f7b7f469285595de18df4dbcd5514a1d19a790c285b` | CLEAN 0 | OK 0 | no anchor | **no** |
| M_c2 | source **+ argv reader element + `source_sha256`** coherently re-pointed at `structural.py` | `1903fc50fbf76eaf0d62a33e44fbf171abc8c4753a12aede5ce51557be75d543` | CLEAN 0 | OK 0 | no anchor | **no** |
| M_d | `record_defects_disclosed` loses `F4` (5→4 entries, ids F1,F2,F3,F5) | `702c1d41ae972f307d144b8c9af1730c3f7f68397c19f7120fbe33834d084d7a` | CLEAN 0 | OK 0 | no anchor | **no** |
| S6 restored | pristine bytes restored | `e6303d06…b5cbfc` | CLEAN 0 | OK 0 | no anchor | — |

Detector UTCs: S0 07:31:54Z, M_a 07:31:57Z, M_b 07:32:00Z, M_c 07:32:03Z, M_c2 07:32:06Z, M_d 07:32:10Z, S6 07:32:17Z (all 2026-10-25). D1 and D2 outputs were byte-identical in all seven states; D2's receipt per state is `gate-<state>.json` in scratch.

**Committed instruments: 0 of 5 mutants killed.** Nothing in `tools/` reads, hashes or validates `claim-stop.json` (`grep -rln "claim-stop|claim_stop|stop.json" tools/` → empty; no hook, no `.github/workflows`, no repo-level validator; `tools/` holds only round directories).

## 4. Outside-reader comparator (D4)

| state | source exists | sha256 match | 3-seed rerun vs `observed` | D4 verdict |
|---|---|---|---|---|
| S0 | yes | yes | 8/8 = 8/8 each seed | agrees |
| M_a | yes | yes | agrees | **not caught** (verdict is uncomputable free text) |
| M_b | yes | yes | record 0 vs rerun 8 at all three seeds | **caught** |
| M_c | yes | **no** (`2e8feaea92ee` vs `2f399cab3645`) | rerun 8 = 8 | **caught by hash only** |
| M_c2 | yes | yes | agrees (structural.py also scores 8/8) | **not caught** by existence/hash/count; caught only by prose (class says "reads no header, walks no record array") and by doc paths |
| M_d | yes | yes | agrees | **not caught** |

## 5. Doc anchors — and the revision they appear in

Crucial: at the stop commit `cd75b92e`, **no** doc mentions `R34-C2` at all (`git show cd75b92e:{SCORECARD.md,LOG.md,SKILL.md,corpus/lessons/round-34.md} | grep -c R34-C2` → `0,0,0,0`). The doc surface exists only from the later landing commit `66b84027` ("round-34: land the stopped claim's record — SCORECARD section, LOG entry, lesson M34-5..M34-11, …", parent `cd75b92e`, now `refs/heads/main`), where it is 2 (SCORECARD), 1 (LOG), 1 (SKILL), 2 (lessons) hits. The knowledge entry `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` is likewise absent from `cd75b92e` and tracked from `66b84027`.

Anchors in the current tip (`66b84027`; `SCORECARD.md:3353`, `:3355`; `LOG.md:3094/3098`; `corpus/lessons/round-34.md:41/49/57`; `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:4/38/42`, tracked):

| mutant | contradicting text exists | effect |
|---|---|---|
| M_a | yes — `SCORECARD.md:3353` "**falsified measure / honest stop**"; `LOG.md:3094`; `lessons:41`; record's own `why_this_falsifies_the_surface` + `observed.met_target=true` | a **human** diff notices; no program does |
| M_b | yes — `SCORECARD.md:3353` "five unregistered structure-blind classes reach the green 8/8"; `lessons:49` "8/8 … at three seeds"; knowledge entry `:42` | human diff + D4 rerun |
| M_c / M_c2 | yes — path + 12-hex prefix `2e8feaea92ee` at `lessons:49/57`, `SCORECARD.md:3355`, `LOG.md:3098`, knowledge entry `:42` | human diff only for M_c2 |
| M_d | **no** | nothing |

Counting anchor for the defect list is self-conflicting: the stop commit message says "disclose **five** record defects", `SCORECARD.md` prose enumerates **six** numbered items, and the file holds **five** entries whose membership is not the SCORECARD list. `claim-stop.json` F4 = "gate mutant M3 (ignore last shortcut row) survives its own selftest" while SCORECARD item (4) = "a shortcut relabelled `structural` prints CLEAN even on the red config" (`lessons` M34-9 covers both). The record therefore omits at least three classes SCORECARD flags (relabelled-structural; gate-runs-no-reader **and** `met_target` cross-check; `--rev` echo) and includes one SCORECARD's numbered list omits. Dropping F4 leaves a record that is still *more* than the doc's count minus one, and no byte anywhere states the intended F-set.

## 6. What happens if the mutant is committed (the realistic landing path)

In the probe clone (not the lane):

- **P1** — commit M_a (`git commit -m "probe: land a mutated stop record"`), then `git status --porcelain` → 0 lines; `freeze-integrity … --rev HEAD` → **exit 0**, `CLEAN pins=26`; `c2-shortcut-gate-counter.py --root . --rev HEAD` → **exit 0**, `GATE_COUNTER_OK …` (07:34Z). A landed mutant is indistinguishable from the stop.
- **P2** — append `# probe` to the pinned `tools/round-34/replay-gate.py` **without committing** → `freeze-integrity` → **exit 0**, `CLEAN pins=26`: `freeze-integrity.py` hashes `git show <rev>:<path>` blobs, never the worktree (blob read at `tools/round-34/freeze-integrity.py:456`, `git(a.root, "show", "<rev>:<path>")`).
- **P3** — commit the same appended-bytes change → **exit 1**, `FAIL tools/round-34/replay-gate.py sha=774032b59d03 commits_after_freeze=<sha>`, `freeze-integrity: FAIL pins=26 changed=1`.

Contrast established: the lane *can* pin and detect a landed mutation of an instrument; it simply does not pin the artifact that carries the verdict. `instruments.json` is not itself a pin (no key names it), so the pin container's integrity rests only on git history.

## 7. Findings

- **S1 (primary).** The stop record is not checkable by the lane: 0/5 mutants noticed by any committed instrument, including a fully committed mutant (P1). Its verdict, its observed numbers and its defect list are enforced by nothing.
- **S2.** It is only partly checkable by an outside reader: the record is *self-reproducing* (`source_sha256` recomputes; the recorded argv reproduces 8/8 at all three seeds; `frozen_counter_verdict.line` equals the committed receipt), so a reader who reruns D4 catches M_b and M_c — but not M_a (free-text verdict), not M_c2 (a coherent forgery that still passes existence, hash and count), and not M_d.
- **S3.** At its own commit the record had **no doc reference at all**; every doc anchor (SCORECARD/LOG/SKILL/lesson/knowledge entry) arrived in the later landing commit `66b84027`. A reader of `cd75b92e` alone has only the wave-1 evidence reports and the commit message.
- **S4.** The five-defect inventory is already inconsistent with the landing doc: commit message "five", SCORECARD prose six numbered items, file five entries with different membership; `F4` collides with an unrelated `F4` id in `w1/MutCounterClauses.md`. Dropping a defect is undetectable because no artifact states the expected set or count.
- **S5.** F1's `repair_landed` cites "`.ufo/waves/round-34/r34b/instruments.json` … + freeze-integrity receipt over it", but that receipt is **absent at the stop commit**: `git ls-tree cd75b92e .ufo/waves/round-34/r34b/after/` lists only `c2-at-instruments.{json,txt}`; `after/freeze-integrity-instruments.txt` is tracked only from `66b84027` (mtime 2026-10-25 04:34:34 −0300). F5's class (unbound receipt) recurs inside F1's own repair claim.
- **S6.** `freeze-integrity` is commit-scoped (P2): even pinned instruments can be tampered in the worktree without a FAIL; only a commit trips it (P3). Any future pin on the stop record inherits that property.
- **S7.** The counterexample itself is sound as recorded: `nameset.py` sha256 `2e8feaea…` matches, 8/8 at `kaidoku-r34-mini-v1`, `alt-1`, `alt-2`, exit 0, `records_match`; `structural.py` positive control 8/8 (`--selftest` exit 0); `pathkey.py` 0/8. Nothing here weakens the stop's decision — only its custody.

## 8. Restoration evidence

- All seven states ended with `claim-stop.json` = `e6303d061da219bb100f3a9acfc7492c9880acc177c4b98f5b695392b5cbcbfc`; `probe-summary.json` records `restored_equals_pristine: true`.
- Probe clone reset to `cd75b92e583735729546b0ea3b250f2df6d0652a`: `git status --porcelain` → 0 lines; `claim-stop.json` `e6303d06…`, `tools/round-34/replay-gate.py` `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` (matches `instruments.json`); 07:34:50Z.
- The lane itself was never written: no `git`/`jj` write command, no edit under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` except this report. Lane `HEAD` movement (`cd75b92e` → `66b84027`) during the window was the L1 landing commit, not this seat.
- No R34-C1 production reader and no ELF carrier/fixture was executed; readers ran only as `python3 -I -B` children of `mini-counter.py` / `c2-shortcut-gate-counter.py`.

## 9. Limits

D5 is a scripted grep of doc text, not a committed checker; "doc would notice" always means "a human comparing record to doc finds a contradiction". The landing-commit doc texts may still change while wave 2 runs; the anchor lines quoted are as of `66b84027` at 07:33Z. I did not mutate `instruments.json`, `claims.json`, the frozen instruments, or any doc, and I did not evaluate the truth of the four additional unregistered classes (other seats' scope). No tool was installed or updated; measured runtimes: `python3 -V` → `Python 3.14.8`, `git --version` → `git version 2.56.0`.

## Verdict

**The stop record survives mutation only because nothing checks it.** 0/5 mutants (verdict→verifies, matched→0, source re-pointed minimally, source+argv+sha re-pointed coherently, a record defect dropped) are detected by any committed instrument; a mutant committed in-tree passes `freeze-integrity` (CLEAN pins=26, exit 0) and the C2 counter (`GATE_COUNTER_OK`, exit 0) unchanged. Detection is outside-reader-only, and even there: the rerun+hash comparator catches 2 of 5, committed docs contradict 3 of 5, and the dropped-defect mutant is caught by nothing because the record's own defect inventory already disagrees with its landing doc (five vs six, different membership). The counterexample evidence itself is true as recorded (8/8, three seeds, sha match); the gap is custody — the record is an un-pinned, un-referenced-at-stop-time free-text artifact whose only reproduction path is a reader choosing to rerun it.
