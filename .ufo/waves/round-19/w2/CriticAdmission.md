# CriticAdmission — wave-2 falsification of admission (all three claims + no-harm + lesson gate + scorecard + pending outside sample)

Scope: attack admission of C1 (routed r18 discharge), C2 (province freshness), C3 (go1.25.0 held-out replay), the no-harm surface, the lesson gate, the scorecard, and anything a pending outside sample cannot reproduce. Observed tip `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (`git rev-parse refs/heads/main`, exit 0). Baseline `8a8da7e…` per `claims.json:4`. My clone `/tmp/kr19-w2-criticadmission` was checked out detached at `d0690fd` for mutation tests only; no lane files were touched except this report.

## Verdict summary

C1/C2/C3 predicates all reproduce at the tip (observation). Two defects, one of them a must-fix for admission-grade reproducibility, plus one stale committed evidence file.

## F1 — MUST-FIX: C1's counting command is not spelling-stable; `--root .` yields a false FAIL (calibration, admission)

`routed-r18.py` accepts `--root` verbatim and passes it as `--root` to the `citation-drift-probe.py` copy it extracts into a `mkdtemp`, which it then runs with `cwd=tmp` (`tools/routed-r18.py:195-208`). A relative root is therefore resolved inside the mkdtemp, the probe's `git -C .` fails → exit 2 → `s_head_aliases` reports `refs/heads/main also refused (always-red)` → `open_count 1`.

Observed, same revision `d0690fd`, same tree:

- `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root . --rev refs/heads/main --strict` → `open_count 1`, R18-HEAD-ALIASES `substance: false`, exit 1.
- `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev refs/heads/main --strict` → `open_count 0`, exit 0.

The falsifiable command claims `--root LANE`; an outside verifier running the identical command with `.` or a relative lane path from the lane root sees the claim FAIL. Worse, the alias-refusal half of that check is vacuous under the broken root (every probe exits 2 regardless), yet the tool surfaces it only as the second half failing — the emitted "why" names the wrong cause.

Smallest safe correction: `g.root = os.path.abspath(root)` in `Git.__init__` (or a refusal of relative `--root` with a named cause). Fails-closed, so no false-green risk; blocks admission only for outside reproducibility of C1's headline command.

## F2 — counterexample: the `historical` clause exemption lets a stale, current-tense pin evade BOTH freshness authorities (freshness)

`province-pins.py` rule (`evidence/province-pins-integrated.json`, `rules.historical`): a clause containing `historical` is omitted as non-current. Mutation in my clone (commit `6ae9be0` then `mut4`): change PROVINCE.md:9's surface summary to `rea-agents@6.5.0` — caught, `mismatch_count 3` (Devin/Kimi/OMP) exit 1. Same stale pin with the single word `historical` inserted in the same clause while still asserting `register` present tense → `mismatch_count 0`, exit 0. `c1-census-v10.py` on the mutated clone marks the same locus `historical (inline marker)`; VERDICT FAIL only on the 2 pre-existing undeclared blocks (`/tmp/census-mut.txt:115`). So one authorial word turns off both gates on a live-pin assertion.

This did not happen in the round (observation: all live pins stated 6.7.0, `province-pins` exit 0 at tip). It is a documented rule working as written, but it is an admission surface for C2's "stale statements rewritten" wording — the claim is discharged for the *detected* stale statements; the gate cannot see evasions. Impacted axis: freshness. Correction if desired in a future gate: exempt `historical` only when the clause carries no present-tense pin verb. I do not mark this must-fix for round-19 admission (claim wording is about rewriting detected stale statements, and S037 grounds the identity); I do mark it a registered evasion class.

## C1 — reproduces, with reservations

- Baseline red (observation): `--rev 8a8da7e --strict` → `named_open 7, substance_open 7, open_count 7`, exit 1.
- Tip green (observation): `--rev refs/heads/main --strict` (absolute root) → `open_count 0`, exit 0.
- Discrimination (mutation in clone): deleting all `- R18-INSTALL-RECORD:` lines from `corpus/lessons/round-19.md` (commit `986aed2`) → `open_count 1`, `named:false`, substance stays true — named-check authority works. Reverting the `_is_analyze_step` list-branch fix in `receipt-validate.py` (commit atop `mut2`) → MIDMAP-LISTSTEP substance red, `open_count 2` (includes the still-mutated named defect).
- Reservation (inference): `named()` requires the correction line in BOTH `SCORECARD.md` and `corpus/lessons/round-19.md` (`routed-r18.py:304-309`) — duplicate authority by design, consistent with "append-only named correction."
- Reservation (observation): the committed "integrated" measurement `evidence/routed-r18-integrated.json` records `open_count 1` at `4f6c73f` — it was produced by a *tool* revision older than the evidence revision (the anchored `## Installs` parser landed in `5e364bd`, the same commit that wrote the file; the run used the unanchored parser, self-admitted in `corpus/lessons/round-19.md:122-123`). At the delivered revision no committed file contradicts the claim, but this stale record is mislabeled "integrated" and should be superseded by the verify pass output; an outside reader could mistake it for the current measurement. Should-fix bookkeeping, not a blocker.

## C2 — reproduces; PASS correctly no longer claimed

- `province-pins.py --root <LANE> --rev refs/heads/main --strict` → exit 0, `mismatch_count 0`, all 9 stated loci 6.7.0 (lines 9,16,17,18,44). Baseline `--rev 8a8da7e --strict` → exit 1, `mismatch_count 2` (Devin, OMP; 3 lines each) — matches the amended predicate exactly.
- `c1-census-v10.py --root .` → real exit 1, `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=2 unresolved=0)` — matches the amended expectation; original claim's "→ PASS" was correctly withdrawn in the amendment. Retained before-receipt `evidence/c1-census-v10-before.txt` shows `stale=4 … undeclared=2` at baseline.
- The G11 warning `current-ok without receipt language: PROVINCE.md:44` persists at tip — declared in output, non-fatal. Observation, not a defect.
- Caveat (inference): the after-state is reproducible only while live configs pin 6.7.0 (`~/.omp/agent/mcp.json` etc. are operator-owned and were rewritten twice on 2026-10-20). The tool records `file_sha256`/`mtime_utc` per config, so an outside verifier re-running later may see different live values without the artifact being wrong.

## C3 — reproduces; mechanism confirmed under the frozen rule; compare count matches

- Freeze provenance (observation): `git show -s --format=%cI a1140e7` → `2026-10-20T15:57:44-03:00`; first carrier run starts `15:57:51` (`runs/run-log.txt:2`). `git diff a1140e7 refs/heads/main -- .ufo/waves/round-19/predictions/` → empty (exit 0). Predictions and `decision-rule.json` were frozen in Git before any REA analyze. (Stray commit `2bbbf2c` touches predictions paths but is a selftest artifact tree, not on `refs/heads/main` — `git branch --contains` empty.)
- Bindings (observation): all 8 run dirs have `receipt.json`, `observation.json`, `compare.json`; `receipt.carrier.sha256_pre == sha256_post == prediction.carrier.sha256` for all 8; every prediction's `c3.emulator_sha256` = `14924bd6…` = live sha256 of `.ufo/waves/round-18/tools/swiss-misread.py`; `predictions/SHA256SUMS -c` all OK; live `go`/`vet` binaries still hash to `carriers.tsv` values.
- Mechanism (observation): vet `ghidra.log:229` `Caused by: java.io.EOFException: Invalid index: 13902080` — 13902080 ∈ `h1_only_invalid_indexes.t1250-vet {13902080, 852107777}` and ∉ `walk_invalid_indexes_both_hypotheses {1801722468838924630}`. All 7 non-D logs: zero `Go analysis failure` lines. Under `decision-rule.json`'s `confirmed` clause this is CONFIRMED, not h0_consistent.
- Count (observation): `compare.json` exists for all 8 labels → claim's 0→8 met. vet `compare=1` is the frozen full `extra.invalid_index_reads` list ([13902080, 852107777, 1801722468838924630] vs observed [13902080]); honestly reported in `SCORECARD.md:2495` and the lesson as a falsified full-list forecast, not an exact success. The amendment naming this rule restatement is timestamped 16:20 — after the 16:07 run end — but it restates the rule *as frozen in Git at 15:57:44*, so the decision authority is pre-run even though its prose re-entry is post-run. Observation + inference: no retro-fitting of the artifact, though the amendment ordering is worth an outside verifier's attention.
- Reservation (observation): `receipt-validate.py --require-mid-maps` on the retained vet receipt exits 1 — but the only findings are `sha256_mismatch`/`size_mismatch` on the validator's own path (the forward-edited tool; `verify.py:110` expects exactly this and constrains it in `receipt-current-drift-only-<lab>`). Source-bound retained validations `evidence/receipt-validation/*.json` all `valid:1`. The binding_gate's three conditions are met.

## No-harm, lesson gate, scorecard, pending outside sample

- Production edits (baseline→tip): `receipt-validate.py` (list-step fix + new selftest cases 4k/4l), `citation-drift-probe.py` (HEAD-alias refusal, `rev_moving_state`), `custody-pair.py` (repo-root toplevel fix, receipt-version stays 2 by construction), `revpin.py` (wording), `jj-red-before.py`, `routed-defects.py` (validator-digest recompute). All in scope of carried items / routed defects; each carried fix names its red case. Observation.
- verify.py (d0690fd): expected-red safeguards are real — `receipt-validate-`→1 is content-constrained to exactly the two drift findings on the validator path (`:674-678`); `vet-full-list-only-mismatch` requires the *only* compare mismatch be `extra.invalid_index_reads` (`:688-690`); `census-only-carried-undeclared` pins `stale=0 ambiguous=0 undeclared=2` (`:686-687`). Tool-integrity table checks worktree == source blob for every executed tool. Gap (inference): `worktree_dirty_tracked_at_start` is recorded but I found no gate that fails the pass on unrelated dirty paths; two tracked wave-2 files are modified right now (`git status`: `wave2-registration.json`, `wave2-registry.json`), which is swarm bookkeeping but verify will pass or fail on it only via tool_integrity if those paths were tools — they aren't.
- Lesson gate: `corpus/lessons/round-19.md` has `## Mistakes` with 6 rows including mined R18-DEADSEAT-RECORD, `## Installs` with full sha256s/channel/date/reason (satisfies R18-INSTALL-RECORD substance at tip), Open list updated, mistakes 5/6 are this-round admissions (carrier `go version` execution breach, 42 dead wave-1 seats) — not hidden. Observation.
- Scorecard: `SCORECARD.md:2491-2499` records C1 10.0→10.0, C3 10.0→10.0, C2 fleet-axis no-proxy, honest falsified-full-list note, "no capability row enters", SHONEN `[~]` preserved, "outside sampling belongs to closure". `SCORECARD.md:2479` still says "Final measured revision and verification records are appended after integration" — `.ufo/waves/round-19/verify/` does not exist (observation); if admission is to be final the verification record is still pending. Treat C1's scorecard verdict column ("Final measured verdict appended after verification") as a placeholder until the verify pass lands; the claim itself stands on my independent reproduction above.
- Pending outside sample (inference): an outside verifier can reproduce C1 baseline/tip and C3 counts from committed objects + live carrier hashes. Two things will bite them: F1's root-spelling false FAIL, and C2's live-config dependency (documented above, mtimes 16:35:56Z on Devin/OMP configs). The `routed-r18-integrated.json` stale record is the third tripwire.

## Impacted axes

- calibration: F1 (counting command not spelling-stable; fails closed but unreproducible outside).
- freshness: F2 (dual-gate `historical` evasion class; today's statements clean).
- depth: none blocking; freeze/binding/mechanism all check out. The post-run amendment timestamp vs pre-run Git freeze is a provenance nuance, not a refutation.
- admission: verify-pass artifact absent; scorecard verdict cell still future-tense.

## Smallest safe corrections

1. `routed-r18.py`: `self.root = os.path.abspath(root)` (or refuse non-absolute root, exit 2). MUST-FIX before an outside sample.
2. Supersede/rename `evidence/routed-r18-integrated.json` or land the verify output so the committed "integrated" measurement isn't stale open_count 1.
3. Register F2 as a known evasion class in the census/pins tool docs (or tighten the clause rule); not a blocker.
4. Append the verification record the scorecard already promises, or correct the tense.

Commands cited above were run read-only in the lane or against `/tmp/kr19-w2-criticadmission` (clone of `d0690fd`); mutations were committed only in that clone. No installs were needed or performed.
