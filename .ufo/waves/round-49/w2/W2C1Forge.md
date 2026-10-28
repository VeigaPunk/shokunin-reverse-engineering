# W2C1Forge — round 49 wave 2, R49-C1 (coverage) post-landing falsification

Lane `KaidokuR49`, landing revision `29883d4ec35a31a8393c4ffb220888c44c0bb022`, freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`.
Frozen counter copy sha256 `ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f` = FREEZE blob of `tools/round-49/c1-counter.py` (checked). Lane was read only through git objects; every mutation is a scratch clone under `/fast/scratch/hyaku/kaidoku-r49/W2C1Forge/` (removed after copying receipts). No tool installed or upgraded.

## Verdict

**The landed C1 claim reproduces, and both plan-disclosed forgeries reproduce exactly; the counter is not a sound measurement of "REA 6.5.0 on the frozen bytes" as the plan words it.** At the landing revision the frozen counter exits 0 with `carriers_matched 4`, every binding true, `frozen_path_changed []`. The relabelled replay and the oracle-built envelope both also exit 0 with `carriers_matched 4`, as the plan discloses. Undisclosed, verified greens:

1. **F3 (plan sentence violated):** a pre-freeze receipt add hidden by `git log -- path` history simplification (a merged side branch whose path matches its first parent) makes `receipt_fresh` true for all four carriers. The plan requires "first added in a commit that descends from the freeze". Exit 0, carriers 4.
2. **F4 (measurement not bound to the hashed package):** the counter-time rerun executes `npx -y rea-agents@6.5.0`, which resolves through the npm cache, not `--pkg65` (the package the counter hashes). Pointing `npm_config_cache` at a scratch copy with a tampered `rea.mjs` yields exit 0, carriers 4. Control: the same tamper with one map entry swapped turns v1le red, so the tampered code is what ran.
3. **F5:** non-projected `depth_limited_paths` and `extraction_continuations` on a committed receipt leave it green (exit 0, carriers 4). The counter reads only `extraction_gaps`.
4. **F6:** `provider.version` `26.6.3` (plan predicate names unblob 26.6.4) green; no clause reads the sasquatch 4.5.1 named in the predicate.
5. **F7:** a symlink replacing a committed extracted file, an extra file, and a junk `extract-tree.tsv` under `corpus/evidence/round-49/c1/` are all green (exit 0, carriers 4). The counter never opens them; `provenance.json` says "unmodified" and `extract-tree.tsv` "records digests", neither checked.
6. **F8 (within the disclosed class, not named):** the v2be genuine receipt, copied to v2le with `subject.digest` and `parameters.path` rewritten, is green on v2le (exit 0, carriers 4).
7. **F9 (note, plan-literal):** freshness checks only the first add. Receipts edited after the data run (`und1`, `und2`: content changed in a later commit) still show `receipt_fresh true`.

Controls behave as the plan says: do-nothing at freeze, handler swap, unpublished entry, subject-only change, and freeze drift all red or exit 2.

## Findings table

Stdout sha256 is of the counter's stdout; `counter_sha256` is `ac83715b…` in every run. Times are UTC, 2026-10-28, 22:37–22:51Z. Exit 0 = met; 1 = not met; 2 = unevaluable.

| ID | Attack (plan clause attacked) | Fixture / command | Exit | carriers_matched | stdout sha256 | Verdict |
|---|---|---|---|---|---|---|
| base | Landing revision, counting command as written | `--root <lane> --rev 29883d4 --freeze decc5697 --pkg65 …/ad9a3fdb…/rea-agents` | 0 | 4 | `ae830b210a799c2b5ec6a67dd629562f0b170e46574f3b70646003f6b6b64657` | Reproduces the target |
| freeze | Do-nothing at FREEZE (`--rev decc5697`) | same, `--rev decc5697` | 1 | 0 | `976af57f9395202fe82a70d5d0e632d4cc3776d74034c2711b3e3e2eeacfa17c` | Red as expected; 6 documentation bindings false |
| **rel** | Disclosed (1): round-44 receipts, `parameters` and `normalized_result.output_directory` rewritten to `/fast/scratch/hyaku/kaidoku-r49/relabel/<id>/rea-out`, evidence id re-minted (xpin, 6.5.0) | scratch commit `62d3a360b4fe0e0066ac4f2c57f281865a9517b6` on the landing revision | 0 | 4 | `5795b084c0e82932a039ad55786f3c0b45834698e80895c220b6ab77f029e003` | **Confirmed exactly as disclosed** (exit 0, carriers 4, landing blocks untouched) |
| **fab** | Disclosed (1), oracle-built: `files` regenerated from the frozen census (`carriers.json` oracle members: path, sha256, size; mime copied), template = round-44 receipts, id re-minted | scratch commit `02856e582f6d5af86831997ba784e47d98d34e4b` | 0 | 4 | `8aa12cb4c8ac9e84a2ded467cff249c89d7843faee7a09f28bce93f79d8e2bed` | **Confirmed** (exit 0, carriers 4). Caveat: `raw_result` hash reports, `engine`, `derivations`, `coverage` copied from the round-44 template, not regenerated from oracle bytes. The disclosed form is at least this strong |
| mint | Sanity: re-minting the genuine landed receipts | xpin 6.5.0 on each landed `after.json` | — | — | — | stored = recomputed for all 4 (`ev_ae61568c…`, `ev_fcae87ce…`, `ev_1b395d04…`, `ev_2d839c52…`) |
| **und4o** (F3 control) | Pre-freeze add on a side branch, merged into REV; side committer date 2000-01-01 | side `68ce4ef846c39719a2f5dd654009d83394783db3` (parent `14936cb9` = decc5697^, adds the 4 after.json blobs identical to REV); merge `ec70b648b7acedcc4632596c31e985b169e78302` | 0 | 4 | `fd31645c4914a4eefa06a25c5afbc02da67e2cae87e0b86aef42496be805e6d6` | **Unexpected green.** `receipt_first_add` = `4aabb0b4` for all four |
| **und4f** (F3) | Same, side committer date 2031-01-01 | merge `3d90b626229401ee5cabc1d51d7eb91ebb6ee99e` | 0 | 4 | `1e37edef4301a49503a996d0605b9dfc5e1047f554f7da5026aadae25c461bce` | **Green.** Date is irrelevant: history simplification drops the side parent |
| F3 evidence | `git log --diff-filter=A -- <path>` (default) vs `--full-history` on the und4o merge | `git-simplification-evidence.txt` | — | — | — | Default: only `4aabb0b4`. Full history adds `68ce4ef8` (committer 2000); `merge-base --is-ancestor decc5697 68ce4ef8` fails. Merge tree == REV tree, path blob identical to first parent (TREESAME) |
| **und5** (F4) | Rerun binding: `npm_config_cache=<scratch copy of _npx/ad9a3fdb>`, copy's `scripts/rea.mjs` prepended with a block that prints the committed envelope for `extract-firmware`; `--pkg65` = untouched host package (its package.json and lock sha match `rea-pkg.json`) | `TAMPER_MAP=tamper/map.json` | 0 | 4 | `ae830b210a799c2b5ec6a67dd629562f0b170e46574f3b70646003f6b6b64657` (= base) | **Green with tampered REA.** Host cache and host `rea.mjs` untouched (sha `526105418604…` before and after) |
| **und5b** (F4 control) | Same, but the v1le pin maps to the v1be receipt | `TAMPER_MAP=tamper/map-swap.json` | 1 | 3 | `c82e7f97c9667fb7a52a658590db26209bea43884a25a3065fe2f8811848d3d6` | Red on `v1le:projection_ok` (`subject_sha256`). Proves the rerun ran the scratch copy, not `--pkg65` |
| **und2** (F5) | Committed v2le receipt adds `normalized_result.depth_limited_paths=[apple1.txt]` and `extraction_continuations=[…apple2.txt]`, re-minted | `842386bcd4f239e90c80938e9841d26b37ca3a7f` | 0 | 4 | `a08c162209e83214be1c1ea1ec43973d094e54f827a0707906ec7656a87e4db3` | **Green.** Neither field is read or projected. Plan: "gaps == []", and depth-limited allowance 0 |
| **und1** (F6) | Committed v1le `provider.version` = `26.6.3` (engine.version stays 26.6.4), re-minted | `f66724b18cc28c16155b6533d1b612a49ff25ce8` | 0 | 4 | `2e92b92cc42f94d5c7f0aa244f525f552a70aba53376c2a2d1ce1432c4487a98` | **Green.** `provider.version` unread; `engine.version` projected, so the live unblob is compared, the committed provider claim is not. Sasquatch: no clause reads it at all (grep: no `4.5.1` in counter) |
| **und3** (F7) | (a) `corpus/evidence/round-49/c1/v1le/firmware.bin_extract/apple.txt` replaced by symlink → `/etc/hostname`; (b) extra file `v2le/firmware.bin_extract/evil.txt`; (c) `v1be/extract-tree.tsv` = `junk` | `4a2ea3a082018f8d2d9edde55e3ed2e06eda4d60` | 0 | 4 | `8488eed812cea46f68bdbebe7bd161adb2a7888975fb509cd3fe034279107df0` | **Green.** Committed evidence beyond `after.json` is not bound |
| **ctlsubj** (F8) | v2be genuine receipt copied to v2le; `subject.digest` and `parameters.path` set to v2le; re-minted | `ae2c67ee65f53713695eecd92d4dfed0b9fa1f82` | 0 | 4 | `523799cd42568fb6e5d0bc26811fdf40d1d4eb06d85925498bb66115887e1749` | **Green.** `parameters.path`, `subject.local_path`, `subject.name`, `normalized_result.output_directory` unread. v2le and v2be REA projections coincide |
| ctlh | v2le: chunk and root-derivation handler → `squashfs_v1`, re-minted | `b3f4b70a8ab4eff28163511255df1e9574f4c640` | 1 | 3 | `67af0187952b7b26eb84cecc8300080113edc8fe016aa5be2f860fe61b017256` | Red: `handler_ok`, `oracle_hits_ok`, `gaps_ok`, `nonregular_unpublished_ok`, `projection_ok` on v2le |
| ctlg | v2le: `unpublished_entries` non-empty, re-minted | `93196b5127fd170336b70e4374f8a28df3466a79` | 1 | 3 | `ab90805dedce375a35931402e1eafeec586085366b4ec4fe7073decc72a10b31` | Red: `nonregular_unpublished_ok`, `projection_ok` on v2le |
| ctls | v2le: `subject.digest` = v1le pin only | `c9e3d7b81949c4cdc3d292923ee3bc84fdad201a` | 1 | 3 | `1fa37ef49156d675e2991b7eef0db5cfa1dc5ef985a7f31c712695388eab5239` | Red: `subject_pin_ok`, `projection_ok` on v2le |
| fz1 | Freeze drift: new file `tools/round-49/zz-extra.txt` in a post-freeze commit | `2b390a4f5255dfadf200a2389ac072b0a3e16a1e` | 2 | — | `fb351e5ac1fa010caab22349ffcb6dd68ee408b8dee7179f48cec6cb166bcf4c` | `frozen_path_changed ['tools/round-49/zz-extra.txt']` (as designed) |
| fz2 | Freeze drift: modify `tools/round-49/c1-run.sh`, then restore in the next commit | restore commit `a8e80a45b746853145140303fe157a1114e75031` | 2 | — | `8feef1bf71a83e24a6a0d7adbc955da2d700f60eae16b5c6c2f1cd154c20ad26` | `frozen_path_changed ['tools/round-49/c1-run.sh']`; a later restore does not un-block (as designed) |

## Detail on each undisclosed green

### F3 — `receipt_fresh` is defeated by history simplification (highest priority; plan sentence violated)

- Plan: "first added in a commit that descends from the freeze". Counter: `first_add()` = `git log --diff-filter=A --format=%H <rev> -- <path>`, then `lines[-1]`, then `is_ancestor(freeze, add)`.
- `git log -- <path>` without `--full-history` applies default history simplification: a merge whose path content equals one parent's is followed only through that parent. A side branch that adds the same blobs before the freeze and is merged afterwards is therefore invisible.
- Reproduced: `und4o` and `und4f` (side commit parent `14936cb9` = decc5697^, its adds identical to REV's blobs, merged with `-p REV -p side`). Both exit 0, `carriers_matched 4`, `receipt_first_add` = `4aabb0b4` for every carrier. Full-history listing adds `68ce4ef8…` with `merge-base --is-ancestor decc5697 68ce4ef8` failing.
- Also: `lines[-1]` is last in commit-date order, not in ancestry order, so the choice of "first" is by timestamp. The date does not matter here (2000 and 2031 both green), but the ordering is still not ancestry.
- Verified by: `W2C1Forge/git-simplification-evidence.txt`.
- Suggested repair (L1, counter is frozen so report as a miss): enumerate with `--full-history` (or `--topo-order --reverse --full-history`), require every add to descend from the freeze, and red on any pre-freeze add.

### F4 — The counter-time rerun is not bound to `--pkg65`

- Plan: the counter runs "REA 6.5.0 `extract-firmware` itself" and the counting command passes `--pkg65 <rea-agents 6.5.0 package root>`. The counter hashes that package (`rea-pkg.json`: package.json and lock sha) but only for the evidence-id recompute.
- `make_real_runner` runs `npx -y rea-agents@6.5.0 extract-firmware …` with `env = dict(os.environ)`, `PATH = FIXED_PATH`. npx resolves through the npm cache (`npm_config_cache`, inherited). `--pkg65` is not the executed package.
- Reproduced: a scratch copy of `~/.npm/_npx/ad9a3fdb…` (host untouched) with `scripts/rea.mjs` prepended by a block that prints the committed envelope for `extract-firmware`; run with `npm_config_cache=<scratch>` and `--pkg65` = host package. `und5`: exit 0, carriers 4, stdout identical to base. `und5b` (map swapped): exit 1, carriers 3, red on `v1le:projection_ok`. So the executed code was the scratch copy.
- Also unpinned: `REA_UNBLOB_COMMAND` = `~/.local/bin/unblob` (version not checked against the committed engine except through projection); the committed receipts were produced through a `unblob-tee.sh` wrapper (`engine.executable_sha256` 28956884…, not projected).
- Suggested repair: run `node <pkg65>/scripts/rea.mjs` directly after asserting its package.json and lock sha; scrub `npm_config_*`; record the executed bin's sha in the receipt.

### F5 — `depth_limited_paths` / `extraction_continuations` are not gaps for the counter

- Counter reads `normalized_result.extraction_gaps` and `unpublished_entries`, `files`, `chunks`, `diagnostics`, `derivations`, `engine`, `published_bytes`, `coverage`. `depth_limited_paths` and `extraction_continuations` are neither read nor in `PROJECTION_KEYS`.
- Reproduced: `und2` (v2le) exit 0, carriers 4, with both fields non-empty.
- Plan: "gaps == []", structural `depth-limited` allowance 0. A receipt that declares depth-limited paths passes.

### F6 — Predicate names `unblob 26.6.4, sasquatch 4.5.1`; the counter enforces neither against the receipt

- `provider.version` is not read (`provider.id` only). `engine.version` is projected, so the live unblob is compared with the committed value via the rerun (a real check, but of the engine, not of the provider claim).
- Sasquatch 4.5.1 appears in the predicate and in `FIXED_PATH` discipline only (CTL-C1-3 tests absence, not version). No clause reads a sasquatch version.
- Reproduced: `und1` (`provider.version` 26.6.3) exit 0, carriers 4.

### F7 — Committed evidence outside `after.json` is unbound

- Counter opens only `corpus/evidence/round-49/c1/<id>/after.json` (blob). `firmware.bin_extract/*`, `extract-tree.tsv`, `provenance.json`, `run.json`, `stdout.log`, `unblob.log`, `manifest.json` are never read.
- Reproduced (`und3`): a symlink where the committed extracted `apple.txt` is, an extra file, and junk `extract-tree.tsv`: exit 0, carriers 4.
- Landed text relies on these as the record (`provenance.json`: "unmodified"; `extract-tree.tsv` "records digests"). Not checked by any clause.

### F8 — Cross-carrier copy (within disclosed class (1); not named)

- `ctlsubj`: the v2be genuine receipt with `subject.digest.sha256` set to v2le's pin, `parameters.path` set to v2le's fixture path, id re-minted: exit 0, carriers 4. The rerun compares content only; v2le and v2be REA output coincide, so the projection matches.
- Disclosed class (1) says a relabelled genuine receipt scores as a fresh run. The receipt does not bind to its own carrier file (`parameters.path`, `subject.local_path`, `subject.name` unread). Low severity; the correction the plan would need is `parameters.path` equals the carrier path.

### F9 — Freshness is first-add only (plan-literal, but changes what "fresh" means)

- `und1` and `und2` edited the landed receipt at a later commit; both report `receipt_fresh true` with `receipt_first_add` = `4aabb0b4`. The clause does not bind the content to the data-run commit. The projection and the rerun do bind content to REA's output, so this only affects the "produced after the freeze" reading. L1 should either disclose or repair it (blob at REV equals blob at first add).

## Not run (honest)

- CTL-C1-1 (round-42 v3 relabel), CTL-C1-3 (sasquatch absent), CTL-C1-4 (round-44 receipts copied verbatim to round-49 path) at the landing revision: not run by me.
- `--selftest`, `--dev-arm`, `--verify-receipt`: not run.
- Documentation bindings (PROVINCE/README/SOURCES/entry text): not attacked here (plan discloses they are presence checks; left to the text seats).
- Oracle-complete fabrication was built from the round-44 template with files regenerated; `raw_result` HashReports were not regenerated from oracle bytes.

## Commands (exact form)

Counter (frozen copy, `TMPDIR=<S> HYAKU_SCRATCH=/fast/scratch/hyaku GIT_NO_REPLACE_OBJECTS=1`):

```
python3 -I -B <S>/c1-counter.py --root <R> --rev <REV> --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <S>/work/<tag> --json-out <S>/scores/<tag>.json
```

- base: `R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `REV=29883d4ec35a31a8393c4ffb220888c44c0bb022` → exit 0.
- Scratch clones: `git clone --shared --no-checkout <lane> <D>`; index-built commits (`read-tree`, `update-index --cacheinfo`, `write-tree`, `commit-tree`); identity set in each clone only; `rev-parse --show-toplevel` asserted equal to `<D>` before commits.

## Artifacts (`.ufo/waves/round-49/w2/W2C1Forge/`)

- `drv.py` (fixture builder and scorer), `c1-counter.copy.py` (frozen counter bytes), `xpin-attribute.mjs` (from `tools/round-27` at REV), `v2le-after.json`
- `scores/<tag>.json|.print|.stdout|.exit` for every scenario above; `base/` (landing score); `freeze-atfreeze.stdout|json`
- `tamper/` (map, map-swap, prologue, original `rea.mjs` sha `526105418604cc6e5a202a6275b700814e27450bfaffd45e7510530ba669de8d`), `fz.txt` (freeze-drift commit ids), `git-simplification-evidence.txt`, `commands.txt`, `sha256sums.txt` (all files)
- Scratch removed (including the tampered npm cache copy).

## Routing for L1

- Non-frozen text: nothing in the landed bytes was edited by this seat; the findings are counter defects (misses under the frozen counter, not patched).
- Recommended disclosures if the counter stays frozen: F3 (freshness blind to merged pre-freeze adds), F4 (rerun resolves through npm cache, not `--pkg65`), F5 (depth-limited/continuation fields unread), F6 (provider and sasquatch versions unread), F7 (evidence outside `after.json` unbound), F8 (cross-carrier copy passes), F9 (first-add-only freshness). These should move from "plan says X" to a stated limit, or be repaired in a successor claim with a new freeze.
