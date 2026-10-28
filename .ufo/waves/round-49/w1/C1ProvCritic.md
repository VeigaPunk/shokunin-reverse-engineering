# R49-C1 pre-freeze attack — receipt-provenance clause (seat C1ProvCritic, wave 1)

## Verdict

**BLOCKING. Do not freeze P49-C1 as drafted.** The provenance clause is one string edit and an evidence-id re-mint away from green. Round-44 receipts, copied to the round-49 path with `parameters.output_directory` rewritten and the id re-minted with the frozen xpin tool, score `carriers_matched 4`, `failing []`. With the wave-1 landing bytes they exit 0 with every binding true. That is the plan's own kill-rule condition ("any counterfactual control reaching `carriers_matched == 4` with every binding true stops C1 before data"). A fully oracle-computed fabrication with no REA run reaches the same state. The drafted controls stay green (kill rule not fired) only because the drafted fabricator is incomplete, and CTL-C1-4 does not test the shortcut the plan names.

Answers to the three questions:
1. **Does the plan sentence say what the code checks?** No. The plan says `output_directory` is "an absolute path inside the `/kaidoku-r49/` scratch segment", the evidence id is "minted over that provenance", the runner records `provenance.json`, and "the committed evidence path is not the output directory — that sentence is the one the counter implements". The code checks only `isabs && '/kaidoku-r49/' in path && '..' not in components`. It never reads `provenance.json`, never checks the on-disk tree, and does not implement the committed-path sentence. See F3–F5.
2. **Can a `/kaidoku-r49/` receipt from a fake or copied producer satisfy it?** Yes. A1 (copied round-44 receipts) and A6 (oracle-only, no REA run) both reach exit 0 with landing bytes. See F1, F2.
3. **Can committed round-44 receipts, re-minted over a `/kaidoku-r49/` path, pass without a real run?** Yes, exactly as in A1 (and A2 with all paths rebased). The evidence-id check and the counter-time rerun both pass, because the rerun compares a projection that excludes `output_directory` and the copied content is identical to what a re-run of the same bytes produces.

## Method

All work ran in a scratch clone (`mkclone.sh`, dev freeze per clone; `DEV_FREEZE=bf5daf695545daac720cb7b0a7e8f80f972a7f32` for the controls run). Each attack case was a separate clone with the draft tools committed as the dev freeze, plus a receipt commit under `corpus/evidence/round-49/c1/<id>/after.json` that descends from the freeze. Each case was scored by the draft counter in default mode (rerun on) with the REA 6.5.0 package at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. Evidence ids were re-minted with the same frozen `tools/round-27/xpin-attribute.mjs` that the draft controls use. Landing bytes were the wave-1 drafts, planted with the draft controls' own `_doc_landing` (`R49C1Doc/`, `R49EntryDraft/`). No data run was performed. The `c1-run.sh --data-run` command was not run.

Real envelopes for the positive arm were captured with the draft counter's own `make_real_runner` (`capture.py`, REA 6.5.0, `npx`, `--full-output`, `max_depth 3`). The counter's `--dev-arm --run-rea` mode produced `dev_matched 4`.

Command shape for every score (exit code semantic: 0 met, 1 not met, 2 unevaluable):
`python3 -I -B tools/round-49/c1-counter.py --root <clone> --rev <REV> --freeze <FREEZE> --pkg65 <rea pkg> --work <scratch> --json-out <file>`

## Findings

Score sha256 = sha256 of the `--json-out` file. "landed" = same receipts plus the wave-1 landing bytes.

| # | Case | Fixture (what differs from a real run) | Exit / carriers_matched / failing | Landed exit / matched / bindings_false | sha256 (no landing → landed) | Verdict |
|---|---|---|---|---|---|---|
| F0 | P0 positive | Real REA 6.5.0 envelopes captured in scratch, output dir `/fast/scratch/hyaku/kaidoku-r49/C1ProvCritic/real49/work/rerun-<id>/out`. Only `after.json` committed; no `provenance.json`, no on-disk tree. | 1 / 4 / [] | **0 / 4 / []** | 26ee92e2… → 04caa577… | Honest positive arm passes. Counter does not read the tree or `provenance.json`. |
| F1 | A1 copied round-44 receipts | Round-44 `corpus/evidence/round-44/c1/<id>/after.json` (real REA output, round-44 scratch). Only `parameters.output_directory` and `normalized_result.output_directory` rewritten to `/fast/scratch/hyaku/kaidoku-r49/C1ProvCritic/atk/A1/<id>/rea-out`. Evidence id re-minted by frozen xpin. | 1 / 4 / [] | **0 / 4 / []** | 03ca9315… → 0e478bb5… | **Kill rule fires.** Round-44 output passes as round-49 output after a string edit. |
| F2 | A2 round-44 receipts, all paths rebased | Same as A1, plus every occurrence of the round-44 output dir and its parent (`engine.executable_path`, `files[].path`, `derivations`) rewritten to the round-49 scratch path. Re-minted. | 1 / 4 / [] | **0 / 4 / []** | 95dec860… → fb54d743… | **Kill rule fires.** Consistency rewrite adds nothing; the counter does not check the absolute paths. |
| F3 | A3 committed path + segment | Real round-49 envelopes with output dir `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-49/c1/<id>/kaidoku-r49/rea-out`, i.e. the committed evidence path with the segment appended. Re-minted. | 1 / 4 / [] | **0 / 4 / []** | 6a87f6c6… → 0c106c8e… | Plan's "committed evidence path is not the output directory — that sentence is the one the counter implements" is false. Counter only checks substring `/kaidoku-r49/`. |
| F4 | A4 control: round-44 unchanged | Round-44 receipts, outdir untouched (`kaidoku-r44`), re-minted. | 1 / 0 / `run_provenance_ok` ×4 | not run | 1ed1e4e6… | Red as expected; the plan's named shortcut without the rewrite. |
| F5 | A5 naive oracle fabrication (r49 outdir) | Round-44 receipt template, files/digests from committed oracle, `raw_result` emptied (no HashReport digests), outdir `/kaidoku-r49/`. No REA run. | 1 / 0 / `projection_ok` ×4 | not run | 65ddd9dc… | Red, but only because `raw_result.report` is empty: projection under `plus-extractor` includes md5/sha1 from `raw_result`. |
| F6 | A6 complete oracle fabrication | As A5, plus HashReport `md5`/`sha1` computed from the frozen committed oracle bytes (`corpus/evidence/round-44/oracle/**`, sha256 asserted equal to the carrier oracle). No REA run. Outdir `/kaidoku-r49/`. Re-minted. | 1 / 4 / [] | **0 / 4 / []** | a1a91c77… → 9a7f80d5… | **Kill rule fires.** The projection is constructible from committed bytes without running REA. |

### Provenance predicate probe (pure function, `provenance_ok` in the draft counter)

| Input `output_directory` | `provenance_ok` | Plan says |
|---|---|---|
| `/tmp/kaidoku-r49/x` | True | "inside the scratch segment"; plan forbids `/tmp` |
| `/home/u/kaidoku-r49/` | True | not inside scratch |
| `kaidoku-r49/x` | False | — |
| `/fast/scratch/hyaku/kaidoku-r49x/x` | False | — |
| `/fast/scratch/hyaku/kaidoku-r49/` | True | — |
| `/fast/scratch/hyaku/kaidoku-r49/a/../../kaidoku-r42/x` | False | — |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-49/c1/v1le/kaidoku-r49/rea-out` | True | "the committed evidence path is not the output directory" |
| `/fast/scratch/hyaku/kaidoku-r42/x/kaidoku-r49/y` | True | cross-round path accepted |

### Plan sentence vs code

| Plan sentence (P49-C1) | Code | Result |
|---|---|---|
| `parameters.output_directory` is absolute and "inside the `/kaidoku-r49/` scratch segment" | `provenance_ok`: abs + substring + no `..` | **Mismatch.** Substring, not segment inside the scratch base. Accepts `/tmp`, lane paths, cross-round paths (table above). |
| "the evidence id is minted over that provenance" | Stored id vs xpin recompute, `evidence_id_ok` | **True** by construction: REA's `semanticProjection` in `rea-agents/dist/domain/evidence.js` lines 156–180 includes `parameters` and `normalized_result`. But anyone with the frozen xpin tool can re-mint (F1/F2/F3/F6), so this is an integrity check, not authentication. |
| "the runner copies the produced tree verbatim under `corpus/evidence/round-49/c1/<id>/` and records `provenance.json`" | `grep -n provenance.json tools/round-49/c1-counter.py` → no hits; counter reads only `after.json`, never the tree on disk | **Not implemented.** F0 passes with no tree and no provenance file. |
| "the committed evidence path is not the output directory — that sentence is the one the counter implements" | No such check | **Not implemented.** F3 passes. |
| Round-44 receipts "re-minted over a `/kaidoku-r49/` path ... pass without a real run" (plan's CTL-C1-4 description) | Counter accepts | **Confirmed pass** (F1, F2, F6). |
| `control_c4` note: "the provenance binding refuses an output_directory outside corpus/evidence/round-49/c1" | Counter refuses only paths lacking the substring | **Mismatch.** The note describes a rule the counter does not contain; F3 contradicts it. |

## Controls and battery (calibration)

- **Draft controls at dev freeze** (`run-ctl.sh`, `ctl.json`): 7 of 7 `as_expected`, `failures []`, `kill_rule_fires false`. CTL-C1-POS exit 0; CTL-C1-0 to 5 exit 1. Green only because the fabricators are weak (see F7, F8).
- **F7 CTL-C1-2 is red for incidental reasons.** `control_c2` → `envelope()` sets `raw_result: {'report': []}` and `mime_type None`. The projection differs on md5/sha1 and mime, not on the run. F6 shows a complete fabrication passes. The plan's own kill-rule text ("a projection-identical fabrication would reach the target and is the claim's kill rule") therefore applies, and the control battery does not test it.
- **F8 CTL-C1-4 is not the plan's shortcut.** `control_c4` relabels round-42 pre-freeze envelopes with their round-42 output dir unchanged. The plan describes round-44 receipts "planted at the round-49 path" as the do-nothing shortcut. With the rewrite (F1), the shortcut is green. Without it (F4), it is red.
- **Battery** (`counter` lines 3128–3136): only the `..` escape and a `/kaidoku-r42/` path are tested. None of F1, F2, F3 is in the battery, so the battery stays green while the kill-rule counterfactuals pass.
- **Counter not always red**: F0 landed exit 0, so the positive arm is not vacuous.

## Smallest safe correction (for L1 to decide pre-freeze; not applied, drafts untouched)

1. **Re-scope the provenance language to what is measured.** The counter can bind committed receipt *content* to the frozen oracle, pins and rerun projection. It cannot bind the *writer* or the *round*: F1 and F6 show that copies and oracle-computed envelopes with rewritten path strings pass, and no committed-bytes check distinguishes them from a re-run of identical inputs. Remove "fresh run"/"round-49 run" from P49-C1 and from the landing headline ("four real REA 6.5.0 receipts captured in scratch"), which would be false for F1. Put F1/F6 in disclosed limits as expected-green.
2. **Or keep run provenance and accept it is undecidable in-tree.** An independent re-execution in wave 2 proves content reproducibility, not writer identity, so it supports option 1.
3. **If the wording stays**, the minimum code change is: `output_directory` must start with the frozen prefix `/fast/scratch/hyaku/kaidoku-r49/` (prefix, not substring; no `/tmp`); require `provenance.json` with output dir equal to the receipt's; add F1/F3 as battery overlays. The change still goes green under forgery, so the freeze must not describe the result as run provenance.
4. **Replace CTL-C1-2 with a complete fabricator** (F6 shape) and CTL-C1-4 with the rebased variant (F1). Under option 1 their expected result becomes "green, disclosed limit".

## Not verified / limits

- No data run. Receipts are scratch captures or re-minted round-44 receipts. F6 uses the round-44 receipt as a structural template (derivations, chunks, engine block), labelled as such; its digests are computed from the committed oracle bytes.
- The landing bytes are the wave-1 drafts used as-is; I did not assess their prose beyond the headline issue in option 1.
- The counter's other clauses (gaps, oracle hits, superblock, freeze-integrity) were not attacked in this seat.
- Tools installed/updated: none. No pacman, no `uv`, no `npm -g`.
- Scratch `$S` removed after copying. Receipts and artifacts are under `w1/C1ProvCritic/` (`receipts/`, `scores/`, `runs/`, `manifest.sha256`, scripts `capture.py`, `attacks.py`, `attacks2.py`, `landing.py`).

## Artifacts (`w1/C1ProvCritic/`)

- `scripts`: `capture.py`, `attacks.py`, `attacks2.py`, `attacks2_full.py`, `landing.py`
- `runs/`: `do-nothing.json`/`.out` (exit 1, `carriers_matched 0`, sha 4c46e734…), `dev-arm.json` (exit 0, `dev_matched 4`, sha 5fbe4ef7…), `ctl.json` (7/7 as expected, sha c3034bec…), `attacks.json` (sha 14abb747…), `attacks2.json` (sha 30d93b74…), `landing.out`, `landing2.out`
- `scores/`: per-case `.score.json` and `.score-landed.json`
- `receipts/`: the committed `after.json` set for P0, A1, A3, A6, plus `git-log.txt` per case
- `manifest.sha256`: sha256 of every file above

Landed revs in scratch (not retained after cleanup): P0 `588a0feb…`, A1 `0e411e3f…`, A2 `47cf3e7a…`, A3 `3c73dbc0…`, A6 `23f0a21b…`.

Draft counter sha256 (`tools/round-49/c1-counter.py`): `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`. Draft plan sha256 (`plans/round-49-claims.md`): `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492`.

Report: `.ufo/waves/round-49/w1/C1ProvCritic.md`
