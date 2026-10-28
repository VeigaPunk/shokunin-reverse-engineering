# R49 wave 1 — C1ControlsReview (pre-freeze attack on the CTL-C1 controls)

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` · draft tools `.ufo/waves/round-49/draft/tools/round-49/` · throwaway dev freeze `5a2711a1354b147845111d12eb8c99f70e247c30` (from `mkclone.sh`; not the real freeze).
Scratch clone: `/fast/scratch/hyaku/kaidoku-r49/C1ControlsReview/clone` (removed after copying artifacts). Lane tree: read-only; `git status --porcelain` shows only the pre-existing `?? .ufo/waves/round-49/`; HEAD unchanged; no sandbox commit exists in the lane object store (`git cat-file -t` absent for all control revs).

## Verdict

**Not ready to freeze as written.** The seven controls all print the expected verdict (CTL-C1-0..5 `as_expected`, exit 1; CTL-C1-POS `as_expected`, exit 0; `kill_rule_fires false`). But the scored evidence does not support the claim's kill rule:

1. **Kill rule fires on a one-line edit (blocking).** Round-44's committed REA receipts for the four carriers, with `parameters.output_directory` and `normalized_result.output_directory` string-rewritten to a `/kaidoku-r49/` path and the evidence id re-minted with the frozen xpin tool, plus the POS landing docs, score `carriers_matched 4`, `met_target true`, exit 0. This is the exact "copy last round's run" shortcut the plan names as the thing CTL-C1-4 must refuse.
2. **CTL-C1-4 is not the control the plan names (blocking).** It plants round-42 heldout envelopes (H41/H43/H44/H45), re-serialized, not the committed round-44 receipts. Planted bytes do not equal `corpus/evidence/round-44/c1/*/after.json` for any carrier.
3. **CTL-C1-5 is vacuous.** Its mutants are written under `corpus/evidence/round-49/c1/superbyte-mutation/`, which the counter never reads. The counter scores the original fixtures. The control would be red with a probe that accepts every mutation.
4. **The driver does not enforce several expectations it writes down** (`gap_kind`, `probe_reds_every_mutation`, `evidence_ids_minted`): `judge()` checks only exit class, `carriers_matched`, `failing_any/includes`, `all_bindings_true`, `doc_bindings_all_false`.

## Checks run and results

| # | Check | Command (abridged) | Result | Evidence |
|---|---|---|---|---|
| 1 | Build dev-freeze clone | `mkclone.sh /fast/scratch/hyaku/kaidoku-r49/C1ControlsReview/clone` | exit 0, `DEV_FREEZE=5a2711a1…` | — |
| 2 | Run all controls | `run-ctl.sh <clone> <work>` (→ `c1-controls.py --root <clone> --freeze 5a2711a1… --counter tools/round-49/c1-counter.py --pkg65 …rea-agents 6.5.0`) | exit 0 (driver `failures []`, `unevaluated []`, `kill_rule_fires false`) | `controls/ctl.json` |
| 3 | Per-control verdict | `ctl.json` | see table below | `controls/*/receipt.json` |
| 4 | Lane untouched | `git -C <lane> status --porcelain`, `rev-parse HEAD`, `cat-file -t <control rev>` | only `?? .ufo/waves/round-49/`; HEAD `e4f2cfa5…`; control revs absent from lane | — |
| 5 | Sandbox-only commits | `git -C <clone> log --oneline -3`; `cat-file -t` on each control `rev` | clone = base + dev freeze; CTL-C1-0 rev = freeze (no commit); CTL-C1-1..POS revs exist only in `work/sb-*` | — |
| 6 | CTL-C1-4 provenance vs round-44 | sha256 of `corpus/evidence/round-44/c1/<id>/after.json` vs planted `relabelled[].destination` bytes | **no match** (table below) | `round44-after-sha256.txt` |
| 7 | Mutant reachability | `counter.json.carriers.*.carrier_path` for CTL-C1-5 | all four = `corpus/evidence/round-42/c2/fixtures/*.bin`; mutants never read | `controls/c5/counter.json` |
| 8 | Counter probe on mutants (direct) | `layout_probe(mutant, carrier)` from `c1-counter.py` | 12/12 arms `ok=False` (probe is correct; control does not invoke it) | — |
| 9 | Driver judge scope | read `judge()` `c1-controls.py:1029-1106` | `gap_kind`, `probe_reds_every_mutation`, `evidence_ids_minted` never read | — |
| 10 | Forgery probes A–D | `forge.py A C` then `forge.py B D` (scratch; see below) | A: reaches target; B: 1/4; C: red; D: red | `forgery/` |

### CTL verdicts (dev freeze; `counter_sha256` d6d70cb7…)

| control | verdict | exit | counter stdout sha256 | carriers_matched | what turned it red |
|---|---|---|---|---|---|
| CTL-C1-0 | as_expected | 1 | `db56bc532227d34505460a64f8f78fcc0a2570d7875b5e3d36977179f36e67ca` | 0 | no receipts; 6 doc bindings false |
| CTL-C1-1 | as_expected | 1 | `6d3840e7f281a1e408bed0098fc967cdb8d75decbe0a6c5c4f74119c9d1f1b20` | 0 | `subject_pin_ok`, `handler_ok`, `run_provenance_ok` |
| CTL-C1-2 | as_expected | 1 | `945f27a8b25fb9f06df09f54c8221b592a1816431fef4d8e2925935aaf3a3467` | 0 | `projection_ok` (all four) |
| CTL-C1-3 | as_expected | 1 | `9a53726152ff8cb3612884d25c612ee106e446ca8ac1837597c8d949a4c0adea` | 0 | `chunks_ok` (gap `missing-extractor-dependency` captured; `gap_kind` not judged) |
| CTL-C1-4 | as_expected | 1 | `c3530573e75d0b6c7fcb160f3fcefe6c622e4084d8219077f88f8157a236cac4` | 0 | `run_provenance_ok` (all four) |
| CTL-C1-5 | as_expected | 1 | `36d742d6f521f1e751c5d9bdd61c15e1b73b0df5f6033c5ac871433e2f6426be` | 0 | no receipts for any carrier (mutants never scored) |
| CTL-C1-POS | as_expected | 0 | `4547aa7fcb9f199115153978d135be21d2be79c6b7e30b1c714a87296d332e35` | 4 | none; `met_target true` |

Each red arm's exit code is 1 with `carriers_matched 0`; the POS arm is 0 with `carriers_matched 4`, `met_target true`, no per-carrier failure.

### Finding 1 (blocking) — provenance is a string edit plus a re-mint

Forgery probe A (`forgery/forge.py A`): take `corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}/after.json` (subject digests equal the carrier pins; real REA output of the same bytes), set both `output_directory` fields to `/fast/scratch/hyaku/kaidoku-r49/forge-A-r44-rewrite-remint/<id>/extract`, re-mint each `evidence_id` with `tools/round-49/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0>`, commit in a sandbox, add the POS landing docs, run the frozen-candidate counter.

- Result: exit 0, `carriers_matched 4`, `met_target true`, `bindings_false []`, `per_carrier_failing` empty for all four. Counter stdout sha256 `ca67b3e5aeb7ada1ba87416f05b0f14c4717551212fdb1dd5296ad351132f25c` (sandbox run; the counter's json-out copy is `forgery/A-counter.json`, sha256 prefix `e9742aa14ac23f56`).
- Control variants: **C** round-44 receipts verbatim (same docs): exit 1, `carriers_matched 0`, `run_provenance_ok` red on all four — so the defence is only the output-directory string. **D** rewrite without re-mint: exit 1, `evidence_id_ok` red on all four — so the re-mint is the only extra step. **B** the driver's CTL-C1-4 source (round-42 heldout H41/H43/H44/H45) rewritten and re-minted: exit 1, `carriers_matched 1` (v1le only).
- Why this matters: `run_provenance_ok` checks `PROV_SEGMENT in output_directory` (substring `/kaidoku-r49/`, `provenance_ok` at `c1-counter.py:1176`); the evidence id is minted by a public frozen tool, so it is consistency, not authorship. The POS arm itself does this rewrite post-capture (`c1-controls.py:957-958, 979-982`), so POS demonstrates that the counter accepts the edit. The plan's disclosed limit ("proves projection equality, not which process wrote the committed receipt") does not cover this: the kill-rule sentence says a copied run is refused, and it is not.
- Adjacent, minor: the substring test also accepts any path containing `/kaidoku-r49/` (for example, any seat scratch tree under `/fast/scratch/hyaku/kaidoku-r49/`).
- Artifacts: `forgery/A-forged-tree/corpus/evidence/round-49/c1/*/after.json` (sha256 in `forgery/A-forged-after-sha256.txt`), `forgery/pos-landing-docs/` (+ `.sha256`), `forgery/A-counter.json`, `forgery/results-AC.json`, `forgery/results-BD.json`, `forgery/forge.py`.
- Suggested for L1 (not patched): either state in the plan that provenance is an attested string binding that a re-minting copy defeats (and reword the kill rule and CTL-C1-4 accordingly), or add a binding a copier cannot satisfy with two edits. No counter-only check I could think of is immune: a forger who can run xpin and REA can produce a tree that satisfies any check the counter can read. The decision is the L1's.

### Finding 2 (blocking) — CTL-C1-4 is not the round-44 receipts

- Plan `## R49-C1` says: "the committed round-44 receipts of the same bytes planted at the round-49 path (the exact do-nothing shortcut: copy last round's run)". Driver docstring (`c1-controls.py:39-42`) and `control_c4` (`:755-797`) use `HELDOUT = corpus/evidence/round-42/c2/heldout` envelopes H41/H43/H44/H45 and re-serialize them with `json.dumps(indent=1, sort_keys=True)`.
- Measured:

| carrier | source (driver) | source sha256 | planted sha256 | round-44 `after.json` sha256 | planted == round-44 bytes |
|---|---|---|---|---|---|
| v1le | round-42 heldout/H41/envelope.json | `2a169092…` | `3c6f01994afd56ab…` | `eb44f3db017337db…` | no |
| v1be | round-42 heldout/H43/envelope.json | `07809042…` | `c3f675f99f4c0211…` | `facc57d94d86c3e2…` | no |
| v2be | round-42 heldout/H44/envelope.json | `dd459799…` | `41f0fefcd01bddeb…` | `18839471ce3b8494…` | no |
| v2le | round-42 heldout/H45/envelope.json | `b5fceda0…` | `6e109b68167755de…` | `162e69b2931c40dc…` | no |

(Full sha256 lists: `round44-after-sha256.txt`; planted bytes: `controls/c4/` receipt `relabelled` block.) Subject digests match the carrier pins for both sources, so the bytes are the same carrier; the receipts are different runs (`output_directory` under `/fast/scratch/hyaku/kaidoku-r42/…`). Planted v1le still goes red only on `run_provenance_ok`, so the verdict stands, but the control tests a different artifact from the one the plan names. Fix is for L1: pick one source and say it once; the round-44 receipts are the copy the plan describes.

### Finding 3 (blocking for the controls' value) — CTL-C1-5 never reaches the probe

- The mutants are written to `corpus/evidence/round-49/c1/superbyte-mutation/<id>/<arm>.bin` (`control_c5`, `:839-845`). The counter resolves carriers only from the frozen table (`corpus/evidence/round-42/c2/fixtures/…`), so the mutant files are inert. `controls/c5/counter.json` shows `carrier_path` = the original fixtures and `layout.magic = hsqs, magic_ok true` for v1le.
- The superblock probe itself is correct: `layout_probe(mutant, carrier)` returns `ok=False` for 12/12 arms with the expected reasons (bad magic `XXXX`; `s_major 3`; `s_minor 9`). So the defect is the control, not the probe.
- `judge()` does not read `probe_reds_every_mutation`, so the C5 "as_expected" verdict rests on `carriers_matched 0` and exit 1, which any counter with no receipts yields. Fix: score the mutants through the counter's own probe (e.g., a `--carriers` override in a dev arm, or call `layout_probe` on the planted bytes and record its verdicts as the control's measured statement), and judge the per-arm reds.

### Finding 4 — expectations written but not judged

- CTL-C1-3 `gap_kind: missing-extractor-dependency` (`:749`): not read by `judge()`. Capture receipt does carry the gap (`controls/c3/receipt.json` `capture.gap_kinds`).
- CTL-C1-2 `evidence_ids_minted: True` (`:716`): not read by `judge()`.
- CTL-C1-5 `probe_reds_every_mutation` (`:854`): not read (Finding 3).
- Kill-rule code (`:1538-1548`) keys on `measured.met_target is True` and `verdict == misbehaved`. It works for a non-zero control that exits 0, but was not exercised by any control here; forgery A was not run through the driver's kill accounting (its exit 0 and `met_target true` are what that code reads).

### Finding 5 — CTL-C1-POS rewrites the evidence it claims to capture

POS captures real REA receipts for the four carriers, then overwrites `parameters.output_directory` and `normalized_result.output_directory` to a `/kaidoku-r49/` path and re-mints the ids (`c1-controls.py:957-958, 979-982`). This is what makes POS green, and it is the same edit as forgery A. POS is therefore evidence that the counter accepts rewritten provenance, not evidence that the provenance binding fires on real runs. Recommend: POS should plant the captured receipts without rewriting, with the provenance rule satisfied by the capture's own `--work` path inside the segment, or the plan should say the rewrite is a dev-arm device.

## Sources re-read
- `plans/round-49-claims.md` `## R49-C1` (controls list, kill rule, disclosed limits; `EA7A` in the read).
- `tools/round-49/c1-controls.py` (controls, judge, main, POS, fixture helpers) and `c1-counter.py` (`provenance_ok`, `layout_probe`, `projection`, `run_counter` callers).
- Round-44 receipts `corpus/evidence/round-44/c1/{v1le,v1be,v2le,v2be}/after.json`; round-42 heldout `corpus/evidence/round-42/c2/heldout/H41,H43,H44,H45/envelope.json`.

## Verification gaps
- Dev arm only: freeze `5a2711a1…` is a throwaway; controls' `freeze`, `counter_sha256` and `rev`s are dev-arm values, not the real freeze.
- Did not run `c1-run.sh` or any data run (per contract); did not run `c2-mismatch.py`.
- Did not drive forgery A through the driver's own control loop; the counter run is the same counter at the same argv shape as `run_counter`.
- Did not verify the counter's full projection/rerun logic beyond the clauses named above.

## Tooling
No tools installed or updated. All work used `python3`, `git` (read-only on the lane; clone-only mutations), `sha256sum`, and the draft tools as committed. Host guard: no writes to `~/.local/bin`, no pacman, no fleet-root files.

## Artifacts (this seat)
- `w1/C1ControlsReview/controls/` — `ctl.json`, `summary.json`, per-control `receipt.json` and `counter.json` (c0..c5, pos).
- `w1/C1ControlsReview/forgery/` — `forge.py` (scratch-path driver; reproduce via `mkclone.sh`), `A-counter.json`, `B-counter.json`, `C-counter.json`, `D-counter.json`, `results-AC.json`, `results-BD.json`, `A-forged-tree/`, `A-forged-after-sha256.txt`, `pos-landing-docs/` + `.sha256`.
- `w1/C1ControlsReview/draft-input-sha256.txt` — sha256 of the draft inputs read (`c1-controls.py` `209f0f4a…`, `c1-counter.py` `d6d70cb7…`, `carriers.json` `829e3392…`, `c1-run.py` `f9161ff3…`, `c1-oracle.py` `80f8212d…`, `run-ctl.sh` `f74939ec…`, `mkclone.sh` `d7d2cd71…`, plan `984e1026…`).
- `w1/C1ControlsReview/round44-after-sha256.txt` — round-44 and round-42 heldout sha256s.

## Recommended folds before the freeze
1. Decide the provenance binding (Finding 1) and reword the kill rule and CTL-C1-4 text to match what the counter can refuse.
2. Make CTL-C1-4 the round-44 receipts, planted without re-serialization, or reword the plan to name the round-42 heldout source (Finding 2).
3. Score CTL-C1-5 mutants through the counter's probe, not beside it (Finding 3).
4. Judge `gap_kind`, `probe_reds_every_mutation`, `evidence_ids_minted` in `judge()` (Finding 4).
5. Stop POS from rewriting captured provenance, or label the rewrite as a dev-arm device (Finding 5).
