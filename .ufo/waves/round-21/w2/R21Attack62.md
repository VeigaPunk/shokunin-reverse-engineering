# R21Attack62 — R20 input immutability

## Axes
- **C1 — calibration**
- **C2 — depth**

## Findings by severity
- **Critical:** none.
- **High:** none.
- **Medium:** none.
- **Low:** none.

No actionable falsifier was found in the assigned integrity scope. This is an author-side recommendation, not an admission or a claim that the R20 results are correct.

## Evidence
Baseline: `2dd430cb6bcad60ff4db720c052074f1f75eecbc`. Measured `HEAD`: `e8df81801805336dbefd33b0001a2d4dd661f498`.

The independent Git tree recount command was:

```sh
for rev in 2dd430cb6bcad60ff4db720c052074f1f75eecbc HEAD; do printf '%s path_entries=' "$rev"; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only "$rev" -- .ufo/waves/round-20/tools .ufo/waves/round-20/runs .ufo/waves/round-20/predictions | wc -l; printf '%s unique_blob_oids=' "$rev"; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --format='%(objectname)' "$rev" -- .ufo/waves/round-20/tools .ufo/waves/round-20/runs .ufo/waves/round-20/predictions | sort -u | wc -l; printf '%s object_types=' "$rev"; git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --format='%(objecttype)' "$rev" -- .ufo/waves/round-20/tools .ufo/waves/round-20/runs .ufo/waves/round-20/predictions | sort | uniq -c; done
```

Captured stdout:

```text
2dd430cb6bcad60ff4db720c052074f1f75eecbc path_entries=357
2dd430cb6bcad60ff4db720c052074f1f75eecbc unique_blob_oids=246
2dd430cb6bcad60ff4db720c052074f1f75eecbc object_types=    357 blob
HEAD path_entries=357
HEAD unique_blob_oids=246
HEAD object_types=    357 blob
```

Separate `git ls-tree -r --name-only` counts (same command shape at baseline and `HEAD`) were **10** `.ufo/waves/round-20/tools` paths and **306** `.ufo/waves/round-20/runs` paths. For `.ufo/waves/round-20/predictions` the count was **41** at both revisions; `.ufo/waves/round-20/knowledge` had **0** at both. The R20 knowledge inputs live in `corpus/knowledge`: five `2026-10-20-r20-*.md` blobs. Their per-path OIDs, as returned by `git ls-tree -r --format='%(objectname) %(path)'` at both revisions, match exactly:

```text
24ce123af7adee5375025a1910063d422e46e945 corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md
48d278e571bcfac5e9e55196fc737dabe224a031 corpus/knowledge/2026-10-20-r20-harmony-application-graph.md
72bda1587427e601b1572025d348c1f39c27d9f9 corpus/knowledge/2026-10-20-r20-objdump-architecture-list.md
f98110f37af8acf838c1d2ca5c56876725cd692b corpus/knowledge/2026-10-20-r20-rizin-command-observation.md
99980c37b3ee567335c892a9165f460d95fdc0f8 corpus/knowledge/2026-10-20-r20-wasm-interfaces.md
a8165c831cd6cc80d499b83f70d8796c878ab92c corpus/lessons/round-20.md
```

`git rev-parse <rev>:.ufo/waves/round-20/<subtree>` returned identical baseline/HEAD tree OIDs: `tools` = `32e79096aaa7f71170558b1d4dc3dc90e198fb4d`; `runs` = `bcff008c7077f5edc1090e0e3a82c87e675b9b50`; `predictions` = `f0570030ddacaa7ac44a29dbd0e79f4dfe82b367`. The worktree comparison `git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --no-textconv --exit-code 2dd430cb6bcad60ff4db720c052074f1f75eecbc -- .ufo/waves/round-20 corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md corpus/knowledge/2026-10-20-r20-harmony-application-graph.md corpus/knowledge/2026-10-20-r20-objdump-architecture-list.md corpus/knowledge/2026-10-20-r20-rizin-command-observation.md corpus/knowledge/2026-10-20-r20-wasm-interfaces.md corpus/lessons/round-20.md` produced no diff; captured `git_diff_exit=0`.

`corpus/QUALITY.md` is **not** byte-identical to baseline: its blob changed from `a9dae16df80f37fddf372aa82197ae6ab820f8ca` to `6500b0135779790a7ed687aad367e4ef1108fd99`. The exact `git diff --numstat <baseline> -- corpus/QUALITY.md` output was `2\t0\tcorpus/QUALITY.md`; its unified-zero diff reports one file, two insertions, zero deletions, at `@@ -35,0 +36,2 @@`. These are new criteria **#26 and #27**. There is no changed/deleted prior criterion: existing admission rows **#1–25** are retained unchanged. The narrow falsifier here would be any deletion/replacement/edit of one of those prior rows, not the expected addition of #26/#27.

## Residual risk and verification gaps
This checks Git-tracked blob/tree identity against the named baseline and the relevant worktree diff; it does not revalidate historical runtime observations, forecast correctness, or R21 C1/C2 behavior. No lane gates, tests, runtime, carrier, or provider were invoked. The `lsp` device is unavailable (`read xd://lsp` returned “No such tool”), so no LSP references/definition/diagnostics were available; no grep output was used as semantic evidence. Canonical-runtime, rerouting-identity, and saturation behavior were outside this narrow immutable-input check.

Report: `.ufo/waves/round-21/w2/R21Attack62.md`
