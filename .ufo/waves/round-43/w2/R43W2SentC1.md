# R43W2SentC1 — C1 generator + score-receipt security/provenance review

Seat: R43W2SentC1 (wave 2, sentinel). Read-only attack seat; no lane production edits, no commits,
no VCS mutation. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## 0. Measured revisions (every attack below names its rev)

| item | value |
|---|---|
| round freeze | `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c` (`round-43: freeze explicit counterfactual kill rules for C1/C2`) |
| C1 measured rev | `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` (`round-43: add seed-bound held-out carriers and post-run tuple receipt`) |
| lane tip at review | `5856614ac4bf7f2363bbcd1956644474a82108e5` |
| ancestors | `git cat-file -t f3f8db3` → `commit`; `git rev-list --count f3f8db3..77d196c6` → 3; `git rev-list --merges f3f8db3..77d196c6` → 0 (no merges in the scored range) |
| anchor (`P43-C1`) | `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b` |
| lane worktree | dirty before and after the review, **byte-identical snapshots**; the only entries are peer/other seats' wave files (`M .ufo/waves/round-43/w2.ready`, `M SCORECARD.md`, `M SHONEN.md`, `?? .ufo/waves/round-43/w2.ready.dispatched`, `?? .ufo/waves/round-43/w2/`) — see `artifacts/R43W2SentC1/status-{before,after}.txt` (`diff` empty) |

Read first, then attacked: `plans/round-43-claims.md` (frozen, `0326dff9…`), the C1 score receipt
`.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json`, `tools/round-43/heldout-gen-v4r43.py`,
`tools/round-43/c1-counter.py`, `.ufo/waves/round-43/controls/c1/{summary.json,receipts/CTL-C1-*.json}`,
`corpus/evidence/round-43/c1/heldout/` (manifest + 78 carriers/envelopes/`run.json`, 391 files, all
`100644` — no symlink blobs).

## 1. What I re-derived from committed bytes (not from receipt fields)

All reads are `git cat-file`/`git show` blobs at `77d196c6` (never the worktree), plus one full
re-score by the frozen counter. Scripts: `artifacts/R43W2SentC1/verify.py`, logs `verify.log`.

| check | result |
|---|---|
| 78 carrier blobs: `sha256` of committed `carrier.sqsh` == manifest `sha256` | 78/78 equal, 0 mismatches |
| 78 envelopes: `data.subject.digest.sha256` == true carrier sha256 | 78/78 equal, 0 mismatches (no fabricated subject digest in the landing) |
| 78 `run.json`: `subject_sha256` == true carrier sha, `digest_matches_carrier` true | 78/78, 0 mismatches |
| six-field declared tuple vs my independent re-extraction from each envelope | 78/78 equal, 0 mismatches |
| OOD pair H25/H26 (`out-of-domain`) | declared == observed == all-empty tuple, `published: zero` (the disclosed vacuous carriers) |
| manifest `seed` == freeze hash | true |
| `generator.tuple_check.all_equal` and per-carrier `measured` records vs my extraction | equal (re-verified, 78 entries) |
| frozen blobs, freeze vs rev (SKILL.md, SOURCES.md, claims, both round-42 tools, fixtures.json, C1 counter/generator, CTL-C2-7/7b, round-42 dev+heldout manifest, C02 envelope/rea-full, c2-at-eb8215ac, local-source-gate, gen-squashfs) | all EQUAL; 0 commits in `FREEZE..REV` touch `SKILL.md`/`tools/round-43`/`tools/round-42` |
| v4 table region (`rule_block` semantics) at `d1681696`, freeze, rev | 13 856 B, sha256 `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` at all three |
| pinned interpreter/evaluator touch `d1681696..77d196c6` | 0 commits |
| counter bytes at freeze vs rev | both `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79` (matches receipt `counter_sha256` **and** `counter_sha256_at_freeze`) |
| **full re-score** `python3 -I -B tools/round-43/c1-counter.py --root <lane> --rev 77d196c6 --freeze f3f8db3 --scratch /fast/scratch/hyaku/kaidoku-r43/w2/R43W2SentC1/count --json-out …/receipt-rerun.json` | **exit 0**, `met_target true`, `matched 78`, `bindings_false []`; receipt byte-identical to the committed receipt except `argv[8]`, `argv[10]`, `regen_argv[4]` (scratch paths only) — `artifacts/R43W2SentC1/receipt-rerun.json` |
| CTL-C1-2 **red** arm re-run: committed generator copy `--tuple-check <lane>/corpus/evidence/round-42/c2/heldout` | **exit 3**, stdout `declared_tuple_unobserved: 1 of 78 … C02 … gap_kinds: declared ['extractor-failure','unpublished-entry'] != observed ['depth-limited','extractor-failure','unpublished-entry']`; manifest sha `656c22d5…` before **and** after (write-nothing holds); no worktree change — `artifacts/R43W2SentC1/ctl-c1-2-red.log` |
| r42 control rows in the receipt | 14 controls, all `reproduced: true`; max counterfactual 75/78, reference witness 78/78 (witness is excluded from the kill rule by the frozen plan) |

So on the *landed* bytes the claim's central numeric and byte clauses hold, and the receipt is
independently reproducible. The findings below are about what those bindings **do not** prove, and
about two path-handling defects in the counter itself.

## 2. Findings

### F1 — HIGH (calibration / provenance): a hand-authored envelope set scores the full target; no binding distinguishes "REA produced this" from "a forger wrote this"

**Exploit path.** Produce honest, seed-regenerating carriers (that half *is* bound), then author the
78 `envelope.json` files by hand: copy each carrier's true sha into `subject.digest.sha256`, keep the
declared six-field tuple and the table's row decisions. `run.json` need not even be touched: its
`gap_kinds`/`handlers` are written by the generator as `record.update(shape)` from the *same*
envelope parse (`heldout-gen-v4r43.py:2669-2677`, `2713-2756`), so the counter's `runjson_digests`
comparison (counter `1893-1928`) is `f(envelope) == f(envelope)`.

**Evidence (measured).** Scratch clone of the lane, landing-shaped commit
`5a2ea34d3f6afcca1e5a304c7fbdc21131e6ef99` = `09ab56b8` + the committed heldout tree with **only**
`H01/envelope.json` edited (added `"zz_fabricated_by_seat": true` and
`"environment": {"host": "hand-authored", "rea": "never ran"}`; digest and tuple untouched):

```
{"bindings_false": [], "exit_code": 0, "matched": 78, "met_target": true,
 "revision": "5a2ea34d3f6afcca1e5a304c7fbdc21131e6ef99"}
EXIT=0
```

`artifacts/R43W2SentC1/receipt-fabricated.json`. The stronger form is mechanical: round-42
held-out/dev envelopes carry the same class-driven tuples, so copying them and rewriting the digest
field (and `run.json.subject_sha256`) reproduces a green **without any REA run**; the only work is
re-hashing.

**Impact.** `met_target: true` and the 45/45 bindings evidence *consistency of the committed
envelopes with the frozen table*, not that REA 6.5.0 produced them. P43-C1's provenance clauses
("the held-out set is … produced by … `--run`", "every envelope's subject digest equals its
carrier's sha256") are satisfiable by construction, and the plan's compensation claim ("the check is
generator-self-reported, so the counter additionally binds the per-carrier `run.json` digests") does
not compensate — `run.json` is the same generator's transcription of the same parse. Nothing pins
`provider.version` either: all 76 extract carriers say `unblob 26.6.4` and H25/H26 say
`binwalk 3.1.0`, but **no binding reads `provider.version`** (grep: `26.6.4` in the counter appears
only in the fixture-pin block and selftest) — `artifacts/R43W2SentC1/provider-inventory.log`.

**Smallest remediation.** (a) Restate the two provenance clauses as consistency clauses in
`plans/round-43-claims.md` and drop "additionally binds the run.json digests" as a provenance claim
(it is an anti-tamper transcription check); (b) add one cheap binding the evidence already carries:
`provider.id == "unblob"` and `provider.version == "26.6.4"` for the 76 extract-firmware carriers
(and `binwalk`/`3.1.0` for the OOD pair) — green today, and it rejects an envelope set lifted from a
different unblob build; (c) if real provenance is wanted, it cannot come from generator-written
files — it needs an out-of-band run record (resolved `rea-agents` version + integrity, unblob digest)
committed by the runner.

### F2 — MEDIUM (security): attacker-chosen **absolute write** during scoring, before any refusal

**Exploit path.** `c1-counter.py:1317-1327` `flat_envelopes()` does
`fp = os.path.join(d, cid + '.json')` with `cid = str(c.get('id',''))` taken straight from
`corpus/evidence/round-43/c1/heldout/manifest.json` (`1506`). An absolute id makes `os.path.join`
return the absolute path; `..` segments escape the staging dir. `ids_unique` (`1608`) checks only
non-emptiness and uniqueness. The carrier and envelope *paths* are guarded by the `resolve()` helper
(`1680-1690`: rejects `/` and `..`), but ids never pass through it. The write happens at `1943`,
i.e. before any binding is evaluated, and the run-level `shutil.rmtree(scratch)` (`2558`) cannot
remove escaped files.

**Reachability (both directions tested at `77d196c6`).**
- Post-landing edit of the manifest → **blocked**: rev `bab71e07bc49ae576b2a59b8cb39e7f35ff1cbdc`
  (clone, manifest id → absolute) gives `exit 2`, `frozen_paths_changed: ["corpus/evidence/round-43/c1/heldout"]`,
  and no file is written. `frozen_drift` (`339-382`) catches `M` inside the frozen dir regardless of
  `froze_blob`. This is a real defence and it worked.
- **First-add** landing with the poisoned id → **not blocked**: the same edit placed in the commit
  that first adds the heldout tree (rev `4a62bb002b08d11bd9d6c78aa10a23a594fd8be1`) reaches the write.
  Result: `exit 1` (`bindings_false: carriers_regenerated, decisions_reported, evaluator_covers_all,
  generator_tuple_check_all_equal, row_decisions_consistent`) **and** a 24 089-byte
  `…/POISON2.json` written outside the scratch staging tree, containing the committed
  `H01/envelope.json` bytes. Proof: `artifacts/R43W2SentC1/poison-write-proof.txt`,
  `receipt-poison2.json`. (`A` is not a change for a path that was not a blob at freeze — documented
  at `339-355` — so first-added content has no byte anchor to drift against; that is by design, and
  it is exactly the shape of every future claim landing the counter must judge.)

**Impact.** A poisoned evidence commit makes the scoring run write attacker-chosen bytes to an
attacker-chosen path with the scorer's privileges (the L1), *then* refuse. Write-then-refuse is still
arbitrary file write; on a shared host it is a persistence/overwrite primitive, and `--json-out`
targets are also reachable if the id path is aimed there. No in-repo impact was possible in this
landing: the committed manifest's 78 ids are all `^[A-Za-z0-9._-]+$` (inventory above), so F2 is a
latent defect, not a live compromise.

**Smallest remediation.** One guard at the loader: reject any id that does not match
`^[A-Za-z0-9._-]+$` (or route ids through the existing `resolve()`), and derive
`flat_envelopes`/`measure_out_dir` filenames from the index, not the id string.

### F3 — LOW/MEDIUM (dead binding): `manifest_before_envelopes` is true on a same-commit add

`is_ancestor(root, ma, fa)` (`1935-1937`, helper `296-299`) returns true when `ma == fa`
(`git merge-base --is-ancestor X X` → 0). In the landed receipt the manifest first-add and **all 78**
envelope first-adds are the same commit `77d196c6`
(`manifest_first_add`, `carriers[].envelope_first_add`). So the binding carries **zero** ordering
evidence: the exact M42-2 inversion (manifest finalised before the run) passes it if the manifest and
the envelopes land in one commit. Scratch fixture (asserted `rev-parse --show-toplevel` == fixture)
with both files added in one commit: manifest first-add == envelope first-add, binding value `True`
(`artifacts/R43W2SentC1/demos.log`, DEMO 4). The plan's "`manifest_before_envelopes` stays bound" is
therefore satisfied vacuously; the actual guard against R42-CL1 is the generator source order, which
is not what the receipt's binding name says.

**Smallest remediation.** Either rename to `manifest_committed_with_envelopes` and keep the predicate
honest (it is a co-landing check), or make it strict (`any(is_ancestor(root, ma, fa) and ma != fa …)`)
and accept that a single landing commit cannot pass it — in which case the plan should stop counting
it as an anti-inversion binding.

### F4 — LOW (read traversal, same root cause as F2): `--tuple-check` reads outside its directory

`run_tuple_check_dir` (`heldout-gen-v4r43.py:3345-3362`) → `measure_out_dir` (`3271-3281`) →
`envelope_shape_on_disk(os.path.join(out_dir, cid))` with `cid` from the checked directory's own
`manifest.json`. Absolute or `..` ids read and *print a diff of* any `<dir>/envelope.json`-shaped file
on the host (declared vs observed). Live demo inside scratch: a manifest in `demo3/checked` with
`id = <scratch>/demo3/outside/SENTINEL` produced
`… SENTINEL  combo  published: declared 'zero' != observed 'nonzero'` — proving the parse came from
outside `checked`; the checked directory was left with only `manifest.json` (no writes).
`artifacts/R43W2SentC1/demos.log` DEMO 3. Impact is disclosure of parsed field values only; the same
one-line id guard fixes it. (`--tuple-check` runs with **no** freeze/ancestor gate at all, which is
why this arm is the easiest way to hit the id join.)

### F5 — LOW (provenance hygiene of the generator's process inputs)

- `REA_PACKAGE = 'rea-agents@6.5.0'`, invoked as `npx -y …` (`heldout-gen-v4r43.py:189`, `2719-2722`)
  with no lockfile/integrity and no recorded resolved version: `rea_argv` in `run.json` is the spec
  string, the envelope records no REA version, and `npx` fetches at run time. The evidence therefore
  cannot name the bytes that produced it.
- `rea_env` (`2592-2601`) inherits the **whole** environment and only appends `REA_UNBLOB_COMMAND`
  (`$HOME/.local/bin/unblob`, host path, unpinned) plus an arm-scoped PATH edit; a hostile
  `NODE_OPTIONS`/`npm_config_*` in the operator env reaches the child unexamined. `home_bin_on_path`
  is recorded per carrier but bound by nothing.
- `subprocess.run(cmd, cwd=work, env=env, …)` (`2722`, `2780`) has no `timeout` — a hung REA blocks
  the generator indefinitely (counter-side `run_tool` uses 1800 s, the regen arm 3600 s).
- `load_writer` (`1272-1278`) `exec_module`s an arbitrary path from `--gen` /
  `KAIDOKU_GEN_SQUASHFS`. The counter overrides it with the freeze-materialised writer when its
  `writer_scope` is non-empty (it is, `writer.materialised: true`), and `writer_matches_manifest`
  binds the declared sha — but if `scope` were empty (`wlocal` falsy) the ambient env var would be
  inherited and executed. Latent only; no evidence path reaches it today.

**Remediation.** Record the resolved REA version/integrity and the unblob sha256 in `run.json` and
bind them; pass a minimal env (`PATH`, `REA_UNBLOB_COMMAND`, `HOME`, `TMPDIR`); add a timeout; clear
`KAIDOKU_GEN_SQUASHFS` before the regen child when no frozen writer was materialised.

### F6 — INFO (no action required, recorded for the integrator)

- Committed envelopes leak absolute host and scratch paths
  (`subject.local_path` = lane path, `parameters.output_directory` =
  `/fast/scratch/hyaku/kaidoku-r43/l1-data/r43-heldout-…/rea-H01`). Hygiene only — and it is
  positive evidence that the envelopes were produced by a run whose outdir was the named scratch;
  a forger would have to copy these strings too.
- Counter scratch defaults (`SCRATCH_BASE or $HYAKU_SCRATCH or $TMPDIR or gettempdir()`,
  `654-661`) can land in `/tmp`; the receipt's argv shows the L1 used
  `/fast/scratch/hyaku/kaidoku-r43/l1-c1-score` (in-spec). Generator default `--scratch` is
  `$TMPDIR` (`4030`).
- No `eval`/`exec`/`pickle`/`yaml.load`/`shell=True`/`os.system` in either tool (grep, clean); all
  subprocesses are list-form with `-I -B` for Python tools; all repository reads are `git show`
  blobs, so a dirty worktree cannot fake a C1 green (contrast C2, which the plan correctly requires
  a clean clone for).

## 3. Kill-rule check (what the controls do and do not cover)

CTL-C1-0 (exit 2 `no_manifest_at_rev`), CTL-C1-1 (round-42 manifest copied → seed/first-add/
regeneration red), CTL-C1-2 (refusal red **and** green arm — I reproduced the red arm: exit 3, C02,
write-nothing), CTL-C1-3 (14 round-42 tables re-scored, max 75/78), CTL-C1-4 (counter-side hand-edit
of `declared_features` → `observed_features_match_declared` false) are all present, committed at
`77d196c6`, and consistent with my re-reads. **Gap:** none of them covers a hand-edited **id**
(F2/F4), and none covers a hand-authored **envelope** (F1) — CTL-C1-4 edits the declaration, not the
evidence. F1 and F2 are the two arms the control set is missing.

## 4. Limitations / inference marks

- I did not run the claim's data procedure (the `--run` generator command); the plan reserves it to
  the L1 and this seat's instructions forbid it. Carrier regeneration is therefore taken from the
  counter's own regen arm inside my re-score (`regen_argv` = `--carriers-only …`, `materialised_files: 75`,
  `carriers_regenerated: true`, and 78/78 regen shas equal to the committed blobs).
- No REA was executed; no publisher firmware or carved image was opened. The only extractor-adjacent
  execution was the generator's read-only `--tuple-check` (no REA, no writer) on round-42 generated
  carriers, and `--carriers-only` inside the counter's own regen arm.
- F1's "round-42 envelopes could be re-hashed into a green" is **[INFERENCE]** from the demonstrated
  fact that a hand-authored envelope passes with only a digest/tuple match; I did not build that
  full false set (it would require touching all 78 envelopes and their `run.json` digests).
- F2's "write-then-refuse" reachability is demonstrated at first-add; whether a future round could
  also *avoid* the refusal depends on other bindings — not claimed here.
- Line numbers refer to the frozen `77d196c6` blobs of `tools/round-43/c1-counter.py` and
  `tools/round-43/heldout-gen-v4r43.py` (sha256 `3a23e93e…` / `6ab0114d…`).

## 5. Verdict on my surface

The landed C1 evidence and score receipt are honest at the byte level and reproducible: 78/78
carriers, digests, tuples, freeze-integrity and the full counter re-score all verify independently,
and the refusal control reproduces exactly. Two defects remain in the *instrument*: **F1** (the score
cannot tell a measured envelope set from an authored one, and the plan's `run.json` "additionally
binds" wording overstates what is measured) and **F2** (manifest-supplied ids reach
`os.path.join` unguarded, giving an absolute write before refusal — with F4's read-only twin). F3 is
a binding that is true by construction. None of these re-opens the claim design; all three are
fixable without touching the frozen predicates' intent.

Artifacts: `.ufo/waves/round-43/w2/artifacts/R43W2SentC1/` (verify.py/log, demos.py/log,
receipt-rerun.json, receipt-fabricated.json, receipt-poison2.json, ctl-c1-2-red.log,
poison-write-proof.txt, provider-inventory.log, status-before/after.txt). Scratch
`/fast/scratch/hyaku/kaidoku-r43/w2/R43W2SentC1/` removed after the artifacts were copied; no
tool was installed; disk free at probe time: `/fast` 592 G, `/` 590 G.

Report: .ufo/waves/round-43/w2/R43W2SentC1.md
