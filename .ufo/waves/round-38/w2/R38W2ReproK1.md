# R38W2ReproK1 — independent re-run of the C1 receipts for carrier K1

**Verdict: CONFIRMED — the committed K1 receipts reproduce exactly (zero semantic residual in
both arms, all 5 oracle files, identical evidence ids). Secondary finding: DEFECTS FOUND — the
frozen predicate's "no external extractor dependency" clause is false for K1 and the frozen
counter cannot test it.**

Seat: leaf, advisory only. No VCS mutation, no corpus writes, no counter/predicate/carrier/oracle
change. Everything below is from my own runs in `/fast/scratch/hyaku/kaidoku-r38/R38W2ReproK1`
(removed at the end) or from read-only `git show` / file reads at the named revisions.
Instrument detail, verbatim commands and hashes:
`artifacts/R38W2ReproK1/RECEIPT.txt`.

## 1. What I attacked

- Receipts: `corpus/evidence/round-38/c1/K1/{before,after}.json` at
  `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8`.
- They are the frozen bytes: working-tree sha256 `85055c92…c72f` (before) and `3dab103b…1d4e`
  (after) equal `git show 3b960fe…:…` of the same paths. Not edited after landing.
- At the first freeze `e059ca9…`, `git ls-tree -r --name-only e059ca9 -- corpus/evidence/round-38/c1/K1/`
  is **empty** — expected, the round-38 receipts are claim data produced after the freeze.
- Carrier: `corpus/evidence/round-37/c1/K1/carrier.sqsh`, manifest pin `1cfb6c33…117e`. The
  bytes reproduce that pin from the working tree **and** from `git show` at the base
  `77091b49`, at the landing `3b960fe`, and at the freeze `e059ca9` (four independent reads).

## 2. Method

Two arms as specified, both with `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` (absolute):

| arm | PATH | fresh out dir | exit | stderr |
|---|---|---|---|---|
| before | `$PATH` with every `$HOME/.local/bin` entry removed | `out-before-1` | 0 | 0 B |
| after | default `$PATH` | `out-after-1` | 0 | 0 B |

In the before arm, `command -v sasquatch`, `sasquatch-v4be` and `unblob` all returned `NONE`
under that PATH; in the after arm both `sasquatch` and `sasquatch-v4be` resolved to
`/home/vgpnk/.local/bin/`. REA refused nothing and created both output dirs itself.

Comparison was by canonicalising each envelope (`canon.jq`) to the semantic payload — engine
(without `worker_count`), coverage, selection, `published_bytes`, chunks, files
(`relative_path`, `size`, `sha256`, `reported_sha256`, `mime_type`, `analysis_depth`,
`runtime_address`, `original_file_range`), `extraction_gaps`, `depth_limited_paths`,
`unpublished_entries`, `extraction_continuations`, `derivations`, diagnostics, the whole
`raw_result.report` tree, both execution blocks, subject, provider, operation, limitations,
locations, evidence links — then diffing committed vs re-run. Scratch roots were scrubbed to
`<SCRATCH>` and the lane path to `<LANE>` so path noise cannot mask or fake a difference.

## 3. Result — payload is identical

| observed | committed before | re-run before | committed after | re-run after |
|---|---|---|---|---|
| chunk handler / range | `squashfs_v4_be` 0..9780 | same | `squashfs_v4_be` 0..9780 | same |
| `chunks[0].extraction_failed` | true | true | false | false |
| files | 0 | 0 | 5 | 5 |
| oracle hits (path suffix + sha256) | 0 | 0 | 5/5 | 5/5 |
| gaps | 1 × `missing-extractor-dependency` [`sasquatch-v4be`] | same | `[]` | `[]` |
| coverage / published_bytes | partial / 0 | same | partial / 9656 | same |
| evidence id recomputes (6.5.0 rule) | yes (`ev_555b79…`) | yes (`ev_1631a1…`) | yes (`ev_400465…`) | yes (`ev_ea3817…`) |

Residual diff after dropping **only** volatile fields:
`diff-before-residual.txt` = **0 B**, `diff-after-residual.txt` = **0 B**.

The only differences anywhere are:

1. `provider_id` / `provider_blob_id` / `blob_id` — values `3093997:1` and `3101425:1`
   (committed) vs `2793428:1` and `2793083:1` (re-run). PID-derived, not payload.
2. `subject.local_path` — the committed receipts name the repository carrier path, my run names
   the scratch copy. The digest, which is the identity that matters, is identical in all four.

Nothing in file set, hashes, sizes, mime types, handler naming, gap kinds/relative_paths/
dependencies, coverage or diagnostics differs. The after diagnostic
(`MaliciousSymlinkRemoved`, `link-to-hello -> …/extracted/hello.txt`) is the same event, only
under the other scratch root; the before diagnostic (`ExtractorDependencyNotFoundReport`,
`missing_dependencies: ["sasquatch-v4be"]`) is byte-identical with no scrubbing at all.

Oracle and on-disk checks:

- `oracle.tsv` (5 rows) vs committed-after files, re-run-after files and arm-B files, with the
  `firmware.bin_extract/` prefix stripped: **MATCH** in all three.
- On-disk `sha256sum` of my extracted tree: **MATCH** to `oracle.tsv` (`disk.tsv`).
- `sum(oracle size) = 9656` equals `normalized_result.published_bytes` in both after envelopes.
- `xpin-attribute.mjs` recomputes each envelope's stored `evidence_id` to itself under the
  rea-agents 6.5.0 rule (and 6.7.0), and `--parse` accepts all four envelopes. The predicate
  clause "recomputes to its stored evidence id" holds for K1.

**So the receipt payload is CONFIRMED. No difference worth reporting as a payload divergence
exists.**

## 4. Defects found (the part that does not confirm)

### D1 — the frozen predicate's "no external extractor dependency" clause is false for K1

`plans/round-38-claims.md` at the freeze, predicate P38-C1, lines 26-28:

> the committed REA extract-firmware after-receipt (run with stock unblob 26.6.4; **no external
> extractor dependency**) publishes every regular file of the frozen independent oracle …

and lines 61-65:

> Not claimed: … or that sasquatch-v4be is required (stock unblob handles standard BE v4;
> measured probes at the base show the `squashfs_v4_be` handler publishing all oracle files
> without any external extractor — the round-37 "missing-extractor-dependency" before-arm
> **does not reproduce** on these carriers …).

Two discriminating arms I ran settle it (both exit 0, fresh output dirs):

| arm | PATH contents | files | gaps | handler |
|---|---|---|---|---|
| A: only **LE** `sasquatch` reachable | `bin-le/sasquatch` + base PATH | 0 | `missing-extractor-dependency` [`sasquatch-v4be`] | `squashfs_v4_be`, `extraction_failed: true` |
| B: only **BE** `sasquatch-v4be` reachable | `bin-be/sasquatch-v4be` + base PATH | 5 (5/5 oracle) | none | `squashfs_v4_be`, `extraction_failed: false` |

Arm A is canonically **identical to the committed before receipt** (`diff-armA-vs-before.txt`
= 0 B); arm B is canonically **identical to the committed after receipt**
(`diff-armB-vs-after.txt` = 0 B). The load-bearing dependency is exactly `sasquatch-v4be`, and
it is resolved only through PATH: `unblob/dependencies.py:30` uses `shutil.which(command)`, and
`squashfs.py:25-26` sets `EXECUTABLE = "sasquatch"` / `V4BE_EXECUTABLE = "sasquatch-v4be"` with
`SquashFSv4BEHandler.EXTRACTOR = SquashFSExtractor(4, 0x73717368)`. The uv unblob install ships
no squashfs reader and no sasquatch binary.

Consequences:

- The after receipt is reproducible **only** while an external `sasquatch-v4be` is on PATH.
  Remove it and the run degrades to the before arm. So the receipt that exists was not produced
  "without any external extractor dependency"; under the literal predicate text it does not
  satisfy that clause.
- The same freeze's "does not reproduce" premise is contradicted **by the freeze's own claim
  data**: `corpus/evidence/round-38/c1/K1/before.json`, committed with the claim, contains
  exactly that gap. I reproduced it twice (stripped PATH, and LE-only PATH).
- The landed knowledge entry already says so:
  `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` — "unblob 26.6.4 has no
  in-process SquashFS reader … Why the dependency is structural", and "Round 38's first freeze
  said the gap 'does not reproduce' because its probes filtered PATH entries by directory name
  and never removed `~/.local/bin`." The receipt and the entry are honest; the frozen predicate
  sentence is not.

Under a lenient reading ("no *extra* extractor beyond the standard toolchain") the clause is
merely ambiguous rather than false — but the frozen text says "no external extractor
dependency", and K1 demonstrably has one. This is a calibration defect in the frozen artifact
that C1's verdict is derived from, not a defect in the measured bytes.

### D2 — the counter cannot see D1, and the receipt records no extractor provenance

`git show e059ca9:tools/round-38/c1-counter.py`, carrier-match body (lines ~177-191), tests only
`oracle_frozen`, `oracle_files > 0`, `after_present`, `after_subject_ok`, `after_operation_ok`,
`after_handler_ok`, `after_gaps_empty`, `after_evidence_id_ok`, `after_oracle_hits ==
oracle_files`. Nothing in the match expression consumes extractor provenance (the only
`sasquatch-v4be` occurrence in code is the selftest fixture at line 329 that injects a gap to
prove red). A run that silently needed `sasquatch-v4be` passes the counter exactly like a run
that did not.

The receipts give the counter no way to check even if it wanted to: `grep -c sasquatch
corpus/evidence/round-38/c1/K1/after.json` = **0**, and the committed
`ChunkReport.extraction_reports` is `[]`. `engine.executable_path` / `executable_sha256` cover
unblob only. So the after receipt cannot demonstrate which binary produced the published bytes.

### D3 — cosmetic, not a divergence

The after arm reports `coverage: "partial"` with zero gaps, zero depth limits, zero
unpublished entries and 5/5 oracle hits. The envelope's own limitations text explains the
policy ("Missing external extractors, unknown chunks, encrypted chunks and depth limits yield
partial coverage … only regular files are published"); the removed `link-to-hello` symlink is
the visible non-published entry. [INFERENCE] `partial` here tracks unpublished entries/bytes
(9656 of 9780) rather than a missed extraction. Identical in committed and re-run, so it is not
a receipt defect — but a reader can mistake it for failure, and the counter treats it as neutral.

## 5. What this means for the C1 verdict

- The **K1 leg of "carriers_matched 3" is independently substantiated**: handler named, no gap,
  5/5 oracle files with matching sha256, evidence id recomputes, subject digest matches the pin.
  I verified each of those conditions directly rather than trusting the author's summary.
- The **verdict "honest stop" is unaffected**: the binding clause `carriers_matched == 4` fails
  on K2 per the landed entry, and K1 did not contribute that failure. (I did **not** re-run K2.)
- What the landing *overstates* is the meaning of the three successes: they are "stock unblob
  26.6.4 **plus an external `sasquatch-v4be` on PATH**", not "stock unblob alone". The
  knowledge entry states this correctly; the frozen predicate parenthetical does not, and the
  counter is blind to the difference.

## 6. Limits

- Only K1 was re-run. K2/K3/K4, the frozen counter and the C2 counter were not executed by this
  seat (out of scope; the counter writes outside my scratch allocation).
- The 6.7.0 rule was computed with the *same* package root as 6.5.0 (`--pkg65 == --pkg67`), so
  the "both" attribution says the id is stable under the 6.5.0 rule, not that 6.7.0 was tested
  against a real 6.7.0 tree.
- No tool installs or upgrades were performed; `npx -y rea-agents@6.5.0` resolved from the
  existing npx cache.
- No `[INFERENCE]` beyond D3; every other statement is an observed command result.

## 7. Artifacts

`.ufo/waves/round-38/w2/artifacts/R38W2ReproK1/`

`RECEIPT.txt` (instrument), `env-before.json`, `env-after.json`, `env-armA.json`,
`env-armB.json` (my four envelopes, sha256 in the receipt), `canon.jq` (the canonicaliser),
`c-*` / `n-*` (canonicalised committed vs re-run), `cn2-*` / `nn2-*` (residual-stripped),
`cA.json`, `cB.json` (discriminator arms), `diff-before-raw.txt`, `diff-after-raw.txt`,
`diff-before-residual.txt` and `diff-after-residual.txt` (both 0 B),
`diff-armA-vs-before.txt` and `diff-armB-vs-after.txt` (both 0 B), `oracle.tsv`,
`env-after-files.tsv`, `committed-after-files.tsv`, `armB-files.tsv`, `disk.tsv`,
`wrap-*.json` (envelopes wrapped for `xpin-attribute.mjs`).

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2ReproK1` was deleted after staging; every cited
byte is in the artifacts directory above.
