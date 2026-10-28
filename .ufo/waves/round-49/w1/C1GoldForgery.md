# R49-C1 gold-forgery attack (wave 1, pre-freeze) — seat C1GoldForgery

## Verdict

**KILL RULE FIRES.** The draft counter `tools/round-49/c1-counter.py` reaches `carriers_matched 4`, every binding true, `frozen_path_changed []`, exit 0 on inputs that involve **no REA run by the seat**:

1. **A13 (cheapest):** four *lean* envelopes computed from the committed carriers.json oracle and the committed unblob `__output__` tree bytes (no REA invocation by the seat), each re-minted through the frozen `xpin-attribute.mjs` (the package's own digest code), planted at `corpus/evidence/round-49/c1/<id>/after.json`, plus the draft landing text. **exit 0, matched 4, met True.**
2. **A5:** the four committed round-44 `after.json` receipts (genuine REA 6.5.0 output for the same bytes), `parameters.output_directory` rewritten to a path inside `/kaidoku-r49/` that does not exist, evidence id re-minted, plus four hollow doc edits. **exit 0, matched 4, met True.**
3. **A11 / A12:** the same two constructions with the draft landing text (`w1/artifacts/R49C1Doc` + `R49EntryDraft`) instead of hollow text. **exit 0, matched 4, met True.**

The counter's only run-binding is the counter-time rerun `projection_ok`. The rerun is genuine (it is the counter's own REA 6.5.0 call; `projection_error` absent), and the forged projections equal it because the plus-extractor projection is a function of committed oracle bytes plus receipt shape. Equality with a real run therefore does not distinguish a fabrication from a run. This contradicts the docstring/claim sentence "a receipt fabricated from the oracle, however its evidence id is minted, cannot equal a real run" and the plan's disclosed limit understates it.

Do-nothing is still red (T0: exit 1, matched 0). Each single-clause attack is red on the clause it names (table below), so the claim is not met by a do-nothing; it is met by an oracle-derived fabrication. Per the plan's kill rule, C1 stops before data.

## Attempts and stopping clauses

All runs: `python3 -I -B tools/round-49/c1-counter.py --root <clone> --rev <REV> --freeze c88ec38a57e5858e40632209abf66a96f63f9453 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <W> --json-out <W>/out.json` in a scratch `git clone --shared` of the lane at base `e4f2cfa5` with the draft tools committed as a throwaway dev freeze `c88ec38a57e5858e40632209abf66a96f63f9453` (in the scratch clone only). "docs" = hollow landing text (attack.py `docs_files`) unless stated. `false bindings` lists boolean bindings only.

| id | input | exit | matched | false bindings | clause(s) that stopped it | stdout sha256 (first 16) |
|---|---|---|---|---|---|---|
| T0 do-nothing | freeze only | 1 | 0 | all doc bindings | receipt_present, all receipt clauses | e460c5e75da3b8a5 |
| A1 docs only | hollow docs, no receipts | 1 | 0 | none | receipt_present/fresh, evidence, projection (all four) | 3055a9537c09b68e |
| A2 r44 verbatim | round-44 `after.json` copied to r49 path, no docs | 1 | 0 | 6 doc | run_provenance_ok (only clause) | 6b886a2cf825386b |
| A3 r44 + outdir rewritten, stale id | | 1 | 0 | 6 doc | evidence_id_ok (only clause) | 4786c42cbb18011e |
| A4 r44 + outdir rewritten + re-minted | no docs | 1 | **4** | 6 doc | none on receipts; doc bindings | 987191886de88e91 |
| **A5 A4 + hollow docs** | | **0** | **4** | none | — **KILL** | d750e4a868f3863b |
| A6 oracle-only (full shape) + re-minted + hollow docs | no REA by seat | **0** | **4** | none | — **KILL** | 2da3e0504e949453 |
| A7 A6 without HashReports | | 1 | 0 | none | projection_ok (`files`) | f406defe7f51010d |
| A8 A6 `published_bytes`+1 | | 1 | 0 | none | projection_ok (`published_bytes`) | 9b266639227246bb |
| A9 A4 outdir outside segment (`/fast/scratch/hyaku/kaidoku-r44/x/rea-out`) | | 1 | 0 | 6 doc | run_provenance_ok | 27bffec2c76b90b9 |
| A10 A6 stale (not re-minted) id | | 1 | 0 | none | evidence_id_ok | 51f489364678851d |
| A11 A6 + **draft landing text** | no REA by seat | **0** | **4** | none | — **KILL** | 2d971f703c114bf5 |
| A12 A5 + **draft landing text** | | **0** | **4** | none | — **KILL** | d27d9762c7543d42 |
| **A13 lean oracle envelopes + draft landing** | no REA by seat | **0** | **4** | none | — **KILL** | 8073a06afb6237f5cb9e12384f8e609c5b3ab0a673828fa1d0f59f39cbc4d9e5 |
| D-C2 draft CTL-C1-2 (as drafted) | | 1 | 0 | none | projection_ok (`files`, `derivations`) | a42398a3f6e50be2 (ctl) |
| D-C4 draft CTL-C1-4 (as drafted) | | 1 | 0 | none | run_provenance_ok, chunks/gaps/oracle_hits/nonregular (round-42 heldout source), projection | 7e848f665b54ab9f (ctl) |

Non-doc bindings were all true in A5/A6/A11/A12/A13. Full per-variant JSON is in `results/out-<variant>.json`; the matrix is `results/table.json`.

Minimal kill-shape (A13) per carrier: one envelope with `operation`, `provider.id`, `subject.digest.sha256` (= carriers.json pin), `parameters.output_directory`, `normalized_result` {`files` (oracle census sha256/size, `mime_type` from `file -b --mime-type` on committed tree bytes), `chunks` (offset 0, length 4096), `derivations` (oracle member edges + root edge), empty `diagnostics`/`extraction_gaps`/`unpublished_entries`, `engine` (unblob 26.6.4), `published_bytes` (sum of sizes), `coverage` "complete"}, and `raw_result.report` HashReports with md5/sha1 computed by `hashlib` over the committed tree bytes. Shape was copied from the committed round-44 envelope of the same carrier; no value came from a REA run. Lean envelope size: 5024 B (v1), 6275 B (v2). Re-minted with the frozen xpin tool.

## Findings (with exact commands, exit codes, sha256s)

**F1 — kill rule (C1 stops before data).** Reproduce:
```
S=/fast/scratch/hyaku/kaidoku-r49/C1GoldForgery; export TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku; mkdir -p $S
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/mkclone.sh $S/clone   # DEV_FREEZE=c88ec38a57e5858e40632209abf66a96f63f9453
cd $S && python3 -I -B attack3.py     # A13 -> "exit 0 matched 4 met True" (stdout sha256 8073a06a…)
python3 -I -B attack.py               # A1..A10 table above; A5/A6 exit 0
python3 -I -B attack2.py              # A11/A12 with the draft landing text, both exit 0
```
Scripts: `scripts/attack.py`, `scripts/attack2.py`, `scripts/attack3.py`. Counter-time REA rerun: `projection_ok True`, no `projection_error`, wall ~20 s for four carriers. The seat ran `npx`/`unblob`/`sasquatch` zero times; all REA invocations are the counter's own. Fixtures (planted receipts): `fixtures/A13-lean-oracle-envelope-plus-DRAFT-landing/<id>/after.json`, `fixtures/A5-copy-plus-hollow-docs/<id>/after.json`, `fixtures/A6-oracle-only-reminted-docs/<id>/after.json`. sha256 of planted `after.json` (v1le / v2be):
- A13: b3bc7963c2934c4d2e5b1db211d3d29f31034e523b9f43c2c38932fe7af009f8 / b5d41edacc258fd4b371b6b74862f12952e4c6594e0793ea14bcf6a0bb2ad0c2
- A5: b383211a8b72b3bcb705af797dc211a6e43324b12db6ae7c14b8cefe24dca9fa / 8e7dac26e91bb22ffadeb0a906f693844088581d45275286547d64dd1ce36e97
- A6: 79790f3e8ea992ad426bce2de4ae57d08d991ed7a9ab67a2b4fcf512e90fdcab / 32a6a144bf05c110819c30ae9b7e50c9220f97b0262117ba64005a4fa400de35

Scratch clone commits (throwaway, not lane): A5 `a9ceb97c82c0a95ee376488278d023d133683c2a`, A6 `b09c2792a24ce24209e99de73e9cf969d7a7f084`, A13 `1f3352ff5f4abd01975dff61527d34473cc63ccf`. Lane HEAD still `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`; lane status shows only the pre-existing untracked `.ufo/waves/round-49/`.

**F2 — the projection clause does not bind a run.** The plus-extractor projection reads: subject sha, file path/sha256/size/mime, md5/sha1 (from `raw_result` HashReports), chunk offset/length, derivation edges, engine name/version, `published_bytes`, `coverage`. Every one is a function of committed oracle bytes or of receipt shape (A7 and A8 show each field is live, and A6 shows that once it is computed correctly it is satisfied). So `projection_ok` adds no information beyond the oracle clauses. The disclosed limit "proves projection equality, not which process wrote the committed receipt" is too weak: here equality is achievable without any process writing REA output.

**F3 — `run_provenance_ok` is a substring test.** `provenance_ok` accepts any absolute path containing `/kaidoku-r49/`; A4/A5/A12 use `/fast/scratch/hyaku/kaidoku-r49/C1GoldForgery/never-created/<id>/rea-out` (verified: directory does not exist) and pass. The counter reads only `parameters.output_directory`, so `normalized_result.output_directory` may disagree. A9 (`/kaidoku-r44/`) is the only red. The plan's "scratch segment that is a directory name only" is accepted.

**F4 — `evidence id` is a re-mint check.** `evidence_id_ok` equals the package's digest of the envelope, so any forger re-mints via `tools/round-27/xpin-attribute.mjs` (A4 shows the clause is green after re-mint). It is not a provenance binding.

**F5 — documentation bindings are substring checks.** A5 uses hollow text (PROVINCE section + row + frontier line, entry with two `source:` lines, two SOURCES cells rewritten, one README coverage row) and exits 0. The doc bindings are required for exit 0 (A4 without them is exit 1), but four-line hollow text satisfies every one of them, so they do not evidence measurement.

**F6 — draft control CTL-C1-2 is red for an accidental reason.** It omits HashReports and derivations, so `projection_ok` fails on `files` and `derivations` (counter `ctl/counter-draft-CTL-C1-2.json`). Adding HashReports, mime and derivation edges (A6/A13) turns it green. The plan's expectation "red on the counter-time rerun-projection binding" holds only because the builder is incomplete, not because the binding resists.

**F7 — plan vs control mismatch on CTL-C1-4.** Plan text (`plans/round-49-claims.md` CTL-C1-4 at `## R49-C1`): "the committed round-44 receipts of the same bytes planted at the round-49 path (the exact do-nothing shortcut: copy last round's run)". Draft `c1-controls.py` `control_c4` (line ~755) reads `corpus/evidence/round-42/c2/heldout/**/envelope.json` (`HELDOUT` at line 139), not round-44 receipts, and does not rewrite `output_directory` or re-mint. So **no draft control tests the copy-last-round shortcut the plan names**; the copy that reaches 4/4 (A4/A5) is untested. This is the same claim/counter disagreement class round 44 stopped on.

**F8 — `carrier_fresh_ok` ignores round 44.** Counter docstring: "the pin is not one a previous C1 freeze already scored". `tools/round-42/prior-pins.json` (18 entries, rounds 38–41) contains none of the four round-44 pins (`b45925fa…`, `529e10…`, `7c62db…`, `79c0f3…`; grep exit 1), and there is no `tools/round-49/prior-pins.json` in the draft. The clause is true for pins round 44 already scored. Calibration only: it does not change any verdict above.

## Clause audit (what each clause actually binds)
- `receipt_fresh`: first-add commit descends from freeze. Satisfied by any commit after the freeze (every attack).
- `carrier_fresh_ok`: see F8.
- `layout_ok`, `carve_ok`, `oracle_ok`, `tree_ok`, `carrier_pin_ok`, `carrier_size_ok`: pass on frozen bytes (T0 per-carrier layout true). Not forgeable here; they bind the carriers, not the run.
- `handler_ok`, `chunks_ok`, `gaps_ok`, `oracle_hits_ok`, `nonregular_unpublished_ok`, `path_shape_ok`: satisfied by a correctly-shaped envelope (A6/A13). They are shape checks.
- `run_provenance_ok`: F3.
- `evidence_id_ok`: F4.
- `projection_ok`: F2 — the only clause that touches a real run, and it is satisfied by oracle-derived data.
- doc bindings: F5.

## Smallest safe correction (for L1 to decide; not applied)
The claim's run-binding has to rest on the counter-time REA run, not on a committed copy: count the facts from the counter's own `extract-firmware` rerun (handler, files/sha/size, gaps, chunks), require equality with the oracle, and keep the committed receipt only as a cross-check whose equality is necessary, not sufficient. A committed copy then cannot reach 4/4 without a genuine REA run at count time, and the counter's own run is the one thing a seat cannot pre-compute. Trade-off: the counter then depends on the REA/unblob/sasquatch environment at scoring time (exit 2 if absent). Separately: change the `run_provenance_ok` check to an exact prefix of an allowed scratch root that exists and was created by the run, and make the control set include A4 (copy + re-mint + relabel) and A13 (oracle-only lean) as red controls with expected exit ≠ 0.

## Scope and disclosure
- No data run, no `c1-run.sh --data-run`, no write into the lane tree (all work in `/fast/scratch/hyaku/kaidoku-r49/C1GoldForgery/`). Only `.ufo/waves/round-49/w1/C1GoldForgery/` and this report were written in the lane.
- Tools: none installed or upgraded. Used `/usr/bin/unsquashfs`, `/usr/bin/file`, `node` (fnm v24.21.0), `npx`/rea-agents 6.5.0 cache, `unblob` and `sasquatch` only through the counter's own reruns.
- Attacks with receipts ran four REA reruns each (inside the counter); T0 and A1 had no receipts and ran none.
- The scratch tree is removed after this report is written; reproduction is by the commands in F1 (recreates `clone/` and `v/`), and `results/` holds the outputs.
- Hollow doc text is in `scripts/attack.py` `docs_files()` (not copied as a file).

## Artifacts (`.ufo/waves/round-49/w1/C1GoldForgery/`)
- `scripts/attack.py`, `attack2.py`, `attack3.py` (sha256 35a38a09…, 074eaf31…, 3a3c3be4…)
- `results/` : `results-all.json` (bb481554…), `results-attack2.json` (59796bc2…), `results-attack3.json` (471cf004…), `table.json`, `run-*.log`/`.err`, `minted.json`, `out-<variant>.json` and `stdout-<variant>.txt` for each attempt, `draft-doc-tree-sizes.json`
- `fixtures/` : planted `after.json` for A5, A6, A13 (16 files)
- `ctl/` : `ctl.json`, `run.log`, `counter-draft-CTL-C1-2.json`, `counter-draft-CTL-C1-4.json`

Tool version/channel record: none installed.
