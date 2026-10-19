# VZ-1 — arc3-loop1-round7 reconciliation verdict

Seat VZ-1, verdicts/convergence chain, 2026-10-19. Direct checks used repository HEAD `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804` and frozen work revision `2fba56fe7d54cfb94ca9332c11cea81667b3b289`. The census gate is SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca` (713 lines). Git was read-only. This seat writes only this verdict artifact; no gate, corpus, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, or `LOG.md` was changed. Scratch execution was under existing `/var/tmp` trees, never `/tmp`.

## Per-claim rulings

- **C1 operability — REPRODUCED, with a locator correction.** The `ptr_check` blind spot is present at HEAD. The RV-2 scratch candidate preserves the clean PASS and catches a dead pointer; it is not landed. PL-2's broader patch variant also passes and catches seeded faults, but produces different counts and scope behavior. Do not combine the variants' counters.
- **C2 coverage — BOUNDED RESULT REPRODUCED; LANDING HOLD.** EX-6 supports the selected finite path/canonicalization Unknown for one `inspect_evm_interface` request shape, not the complete Evidence-ID formula. Its in-memory coverage projection is 86/86, but the entry is still a draft and misses the required opening `recheck:` field; the projection is not a post-landing Command A run.
- **C3 calibration — LIVE COUNT REPRODUCED; DISCREPANCY against a current reading of the receipt.** The live cache contains 1,350 archives, 206 below the dated 1,556 receipt. I select the frozen claim's recorded no-edit adjudication for the historical corpus receipt, while flagging the still-unqualified summary at `PROVINCE.md:50` as a residual if read as current.

## C1 — pointer census blind spot

The current gate collects `PTR` occurrences only inside `if not occ` (`.ufo/gates/c1-census-v10.py:511-514`), after pins and bare versions have already populated `occ`. Direct classification of work-revision `PROVINCE.md:18` with pointer/cache calls observed:

```text
work_line18_PIN= ['6.7.0']
work_line18_PTR= ['~/.kimi-code/config.toml:3546']
work_line18_classify= [('pin', 18, '6.7.0', 'current-ok')]
work_line18_ptr_check_calls= []
```

Correction to the frozen locator: the full current path-and-line on `PROVINCE.md:18` is `~/.kimi-code/config.toml:3546`, dated “2026-10-19 re-read”; `:3298` is named there as a historical receipt pointer. The gate's path-bearing `PTR` expression matches `:3546`; the abbreviated `:3298` is not itself a `PTR` regex match. The blind spot still reproduces on the actual current pointer.

At the unmodified gate, `python3 .ufo/gates/c1-census-v10.py --json` returned exit 0 / PASS, with `current_ok_per_file={"PROVINCE.md":17,"SCORECARD.md":14,"SKILL.md":3}`, `frontier_rows=14`, and `frontier_errors=[]`. I independently ran RV-2's final scratch candidate (SHA-256 `1e7ee0d9b7c89074de9eef37c0da4f8684848f59450219192b329e81c6822f8c`) and confirmed:

- Candidate JSON key set equals the baseline's 19 keys; clean-tree exit 0 / PASS, `current_ok_per_file={"PROVINCE.md":20,"SCORECARD.md":14,"SKILL.md":3}`, `frontier_rows=14`, `frontier_errors=[]`. The three additional Province current-ok loci are the current Devin, OMP, and Kimi pointers.
- `python3 -m py_compile` on the scratch candidate exited 0.
- On the seeded tree changing only `config.toml:3546` to `config.toml:999999`, the candidate exited 1 / FAIL and reported `PROVINCE.md` block `15-26`, pointer line 18, `UNRESOLVED (line 999999 beyond EOF (4150 lines))`; G21 remained 14 rows with no frontier errors and G2 remained true.

Peer reconciliation: PL-2's different scratch patch also returned clean PASS and caught its `:999999` and `:3298` fault fixtures. Its clean `current_ok_per_file` was 21/16/3, versus RV-2's 20/14/3; the PL-2 patch collects all path matches and explicitly synthesizes receipt loci, so it tests a broader surface (including dated/receipt references). Both are scratch-only patch texts. RV-2 is the narrower direct test of the frozen current-pointer blind spot; the broader PL-2 counter changes and receipt-scope policy should be resolved before adopting that variant. The frozen claim is supported; no gate edit is authorized here.

## C2 — bounded Evidence-ID characterization

I parsed all six retained envelopes under `claims/c2/EX-6/evidence/` and independently recomputed the envelope and canonical-function-payload hashes. All six describe the same 1,517-byte carrier (`2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`), 15 normalized functions, and function-payload SHA-256 `3394626e1e49bdb2714faf1fbc942f20dfcbd2a35547a2de18e3c2005adbe1ce`. The first four envelopes are byte-identical (SHA-256 `9b333d1595188f96328dd0a0effaeeb3e17ea90419cce18dc13c1210c33dbc50`) and share ID `ev_a84a565969defaa739ab2567e8da826a284b4a8c4ee1564ec472ab1703b6a09c`; the basename change yields `ev_a19a232f0589027e2b528a7fc5ad68ad95034faee95e3ff7ec98281d130f4912`, and the parent-directory change yields `ev_4634efd77db0fc4d9df111ea38e333651a992c004ccb6a5b5f0361de43843b79`. Thus the bounded path sensitivity, same-resolved-path canonicalization, and `TMPDIR` invariance are supported; the complete hash formula remains **UNVERIFIABLE**. See the retained matrix at `claims/c2/EX-6/evidence/matrix-summary.txt:8-19` and the stated boundary at `claims/c2/EX-6/entry-draft/2026-10-19-arc3-r7-evm-evidence-id-domain.md:28-34`.

Command A was re-run at frozen work revision `2fba56f` using `SCORECARD.md:88-124`:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":85,"mapped":85,"missing":[],"revision":"2fba56f","rule_blocks":15}
```

I also independently overlaid the EX-6 draft stem and proposed EVM map token in memory (no repository edit): the result is `knowledge_files=86`, `mapped=86`, `missing=[]`, `dangling=[]`, `citation_resolved_rules=15`, `rule_blocks=15`, coverage/depth `10.0`. This confirms the projection only; the parent must land the corrected entry and map token, then run Command A on that commit.

**Blocking entry correction:** the Shokunin Corpus Contract requires each `knowledge/` entry to open with `source:`, `verified-at:`, and `recheck:` (`~/.kimi-code/skills/shokunin/protocol/CORPUS.md:17`). EX-6's draft has `source:` and `verified-at:` at lines 10-11, then `REA pin:`; it has no top-level `recheck:` field. A later `## Recheck recipe` section at lines 36-49 does not satisfy the opening-field contract. Before landing, add the field. The current recipe also omits the basename-renamed and relative-argument variants present in the evidence matrix; extend it to recheck those dimensions or narrow the recipe's stated coverage. This does not invalidate the retained six-run measurement.

CR-1/EX-4 independently offer a bounded Vyper optimizer-variants candidate. C2 permits one selection; retain EX-6 as the selected candidate rather than counting both drafts as closure of the same frozen claim.

## C3 — pacman archive count

Fresh read-only measurement at `2026-10-19T14:28:31-03:00`:

```text
find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' -printf 'x' | wc -c  -> 1350
Python pathlib direct-child regular-file count                                      -> 1350
1350 - 1556                                                                        -> -206
```

The receipt records 1,556 at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25`, explicitly `verified-at: 2026-10-13`; it is a historical snapshot. `PROVINCE.md:50` repeats 1,556 without an as-of date. This measurement establishes only the archive-path count, not signatures, signature coverage, bytes, or package integrity.

All six C3 peers agree on the live 1,350 count and −206 delta. EX-7/RV-3 favor an append-only erratum; EX-8/EX-9/SC-1/SC-2 favor a recorded no-edit adjudication. The frozen claim allows either. I choose **recorded adjudication/no corpus edit** for the dated receipt because cache inventory is retention-varying, not a REA capability claim; keep 1,556 as the 2026-10-13 historical observation. Residual: that adjudication does not make `PROVINCE.md:50` a current count. Treat it as discrepant if interpreted as live inventory; any correction there requires a separately authorized source change.

## Write boundary and remaining integration work

This verdict records reconciliation only. The C1 candidate remains unlanded; C2 needs its opening `recheck:` correction and a post-landing Command A run; C3 leaves the historical receipt unchanged and explicitly flags the `PROVINCE.md:50` wording residual. No source, corpus, gate, or `LOG.md` edits were made.