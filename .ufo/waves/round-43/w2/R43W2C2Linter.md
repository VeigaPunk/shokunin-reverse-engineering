# R43W2C2Linter — committed-byte review

## Scope and measured revisions

Read frozen plan `plans/round-43-claims.md` first. Freeze: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`. The evaluated current lane tip was `5856614ac4bf7f2363bbcd1956644474a82108e5`, with freeze as its merge-base/ancestor. The committed C2 receipt available for review is `c2-at-77d196c66f4fea00d7d543728b190ebdfaf6d0f0.json`; it evaluates that earlier revision, not the current tip. C2 control receipts are in `.ufo/waves/round-43/controls/c2/`.

No installation, extractor, test, linter, formatter, or production edit was performed. `xd://lsp` was attempted first for the semantic-check requirement but returned “No such tool”; no LSP-backed references/definition/diagnostics were available. The review is therefore code/receipt inspection, not semantic LSP proof. No scratch clone was created; scratch cleanup is not applicable.

## Re-derived committed facts

Commands run read-only from fleet shell, with `R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

```sh
git -C "$R" show "$F:$p" | sha256sum
git -C "$R" show "$V:$p" | sha256sum
git -C "$R" diff --numstat "$B..$V" -- corpus/SOURCES.md
git -C "$R" show "$B:corpus/evidence/local-sources.json" | jq -cS --arg s "$S" '.sources[$s]' | sha256sum
git -C "$R" show "$V:corpus/evidence/local-sources.json" | jq -cS --arg s "$S" '.sources[$s]' | sha256sum
```

- Imported source `.ufo/waves/round-42/w1/artifacts/R42LocalSrc/build/verify-copies.py`: freeze and tip SHA-256 both `1f790e102be74fbab2a4e24c4235cd59c7a0b91e8bb0fa821259279af4256ded`. This independently agrees with the committed linter stdout's `expect-source-frozen` work/freeze/rev values.
- `corpus/evidence/local-sources.json`: freeze digest `d0d562df9e1e97d872a7ad81a0911284852a490951d3b416693875cc6ad289dd`; tip digest `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e` (expected pinned map digest).
- S126: canonicalized entry SHA-256 at BASE and tip both `3185a528c57055fcb27a494b8c9fc5e6c437f3e2bc1c1e04c6e051d86999353d`; both canonical JSON entries are identical, with copy `corpus/evidence/round-41/s126/lead1-avm-image.tsv` and content digest `f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0`.
- The committed C2 score receipt at `77d196c66f4fea00d7d543728b190ebdfaf6d0f0` reports `rows_checked=19`, `rows_total=137`, `rows_failed=[]`, `copy_audit_checks=136`, `copy_audit_failures=0`, audit exit 0, and map digest as expected. These values are directly present in committed JSON; the embedded linter output also reports `expect-source-frozen` OK. Its score itself is **not green**: `sources_numstat` is `4\t0\tcorpus/SOURCES.md`, so `sources_numstat_three_additions` is false and receipt `exit_code=1`.
- The same numstat recomputed at current tip is `4\t0\tcorpus/SOURCES.md`, not the frozen predicate's required `3\t0`. Thus the available score receipt is honest about a C2 stop at its measured rev, and a current-tip C2 green is not evidenced by this receipt. The later tip landing does not alter the earlier receipt's measured revision.
- Receipt records `freeze_is_ancestor=true`, `clone_clean=true`; gate exit 0, `rows_failed=[]`. This is evidence for those recorded run outputs, not an independent rerun of upstream-backed copy provenance.

Relevant code evidence: `verify-copies-r43.py` lines 194–211 (freeze/rev/work blob comparison and emitted `expect-source-frozen`), 285–317 (EXPECT drives member-pin loop), and `c2-score-r43.py` lines 164–199 (map digest, S126 JSON-value equality, numstat, count/check bindings). In particular, score checks require exact `sources_numstat == "3\t0\tcorpus/SOURCES.md"` and `EXPECT_LINT_CHECKS == 136`.

## Changed imported EXPECT table attack

The import is `_expect_table(args.pack_build)` (`verify-copies-r43.py` lines 35–43); the scored member checks use its result at lines 287–317. Before import, the linter computes the expected source path relative to root and emits success only when working file bytes, `git show FREEZE:path`, and `git show REV:path` all exist and are equal (lines 194–211). Therefore a post-freeze modification to the imported EXPECT file in the clean scored clone cannot silently change the member pins and remain green: the freeze-binding check fails. If `--pack-build` points outside root, `expect_rel` is outside and `git_blob` returns `None`, also making that binding fail. The scorer additionally requires the linter process exit 0.

No mutation was made to committed or scratch bytes, so this conclusion is based on the concrete control flow, not a claimed mutation-test execution. Limitation: the binding proves identity to the freeze blob, not an independent semantic correctness oracle for that frozen EXPECT table; the plan's frozen-source model defines that identity as the contract. The present committed bytes meet the identity binding.

## Findings / residual risk

**Actionable score gap (C2 target not met):** the latest measured C2 evidence is exit 1 due to four appended SOURCES rows where the frozen target demands three. At current tip the numstat remains four additions. The map digest, S126, gate rows and audit counts are otherwise reported/re-derived as above. Do not promote the C2 claim as green from these artifacts; a fresh C2 receipt at the final revision is needed to establish the complete frozen target, and its numstat clause must be reconciled within the frozen contract (not waived).

No linter escape from a changed post-freeze imported EXPECT table was identified in the inspected implementation. Unverified here: clean-clone provenance/linter re-execution, external upstream source comparisons, and all C2 negative-control runtime arms; this seat intentionally did not rerun the scorer or mutate bytes.

## Evidence paths and hashes

- `plans/round-43-claims.md` (read; frozen contract)
- `tools/round-43/verify-copies-r43.py`: SHA-256 `00b3f7a4c7a2ee7f5a6654f12211cbf2a12e0fe10e9de7fc35ff088ce8f3b020` at freeze and tip.
- `tools/round-43/c2-score-r43.py`: SHA-256 `459cbccbb2bf172376357b7e72549add1d99c5d9ed70fecc8acec1ea93432faa` at freeze and tip.
- `.ufo/waves/round-43/l1/scores/c2-at-77d196c6.json`: committed receipt; embedded audit receipt SHA-256 `50b5dbe7686507f51402120d73dce7e3ba11136019823fbcfedf45b4d1884cde`; embedded gate receipt SHA-256 `705b41ae96ffacf0561895ba782ef6f70ba38e1475b28ab0262b654ba3ba08ad`.
- C2 control files listed under `.ufo/waves/round-43/controls/c2/` were enumerated; no runtime control was repeated.

Commands/results: `rev-parse HEAD` → `5856614ac4bf7f2363bbcd1956644474a82108e5`; `merge-base FREEZE TIP` → freeze hash; `git diff --numstat BASE..TIP -- corpus/SOURCES.md` → `4\t0\tcorpus/SOURCES.md`; hash and canonicalization commands above returned the stated values. `df -h /fast/scratch/hyaku/kaidoku-r43/w2 /home/vgpnk/Projects/shokunin/kaidoku-shokunin` reported 594G and 590G available respectively. No tool was installed.

Report: `.ufo/waves/round-43/w2/R43W2C2Linter.md`
