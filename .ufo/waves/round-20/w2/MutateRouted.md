PARTIAL — all 11 assigned mutants were committed and probed; pristine/restored strict runs already fail (5 open), so no full-detector kill is claimed. Five initially-closed rows open; the effective D6d adjacency mutant survives its row.
# MutateRouted — author-side FALSIFY
- Clock: 2026-10-21T07:17:30+00:00; run window 2026-10-21T07:11:13.686999+00:00–2026-10-21T07:15:18.712390+00:00.
- Axes: **calibration** (pre-open ≠ kill), **coverage** (D1–D6f, 11/11 probes), **depth** (prove the surviving predicate actually changes behavior).
- Measured source S / observed clone base: `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`; baseline B `14f0260ad319ecc26994381b2415d5a999003375`. No C3/freeze code was changed.
- Isolated clone: `/tmp/kr20w2-MutateRouted-3-00io9uft/clone` (parent created by `tempfile.mkdtemp(prefix="kr20w2-MutateRouted-3-")`; `git clone -q --no-hardlinks`, checkout `--detach S`). All source bytes were fetched by `git -C LANE show S:<path>` and matched clone bytes before mutation.
- Unmodified detector SHA-256: `548b8ac791245cf69cc8b93e89ffca3b90b4b37db51674de722c319a7a133bd2`. Each mutant is an independent, one-file commit with parent S: private-index `read-tree S`, `add -- <path>`, `write-tree`, `commit-tree <tree> -p S -m <mutation>`, `update-ref refs/heads/mutation-probe/<ID> <commit>`; all exited 0. No source-lane Git write occurred.
## Exact bounded detector

For pristine, every mutant revision below, and restored S (13 invocations):

```sh
ROOT=/tmp/kr20w2-MutateRouted-3-00io9uft/clone
python3 -I -B "$ROOT/.ufo/waves/round-20/tools/routed-r19.py" --root "$ROOT" --rev "$R" --strict
```

Subprocess timeout 1200 s per invocation; measured tool retains its own smaller per-check bounds. Mutant runs used at most three concurrent processes. Every invocation returned **1**; every stderr was empty. Detector source never changed. No Go binary, REA analysis, Ghidra, or omp runtime was invoked. No jj command ran in LANE; jj selftests ran only through the detector’s extracted temporary fixtures. No installs or upgrades.
## Pristine and restored observations

Both: `named_open=0`, `substance_open=5`, `open_count=5`, strict exit **1**. Closed rows: D3, D4, D6b, D6d, D6e, D6f. Open rows, exact `why`:

- **D1:** `in-worktree scratch did not refuse exit 2 with scratch_inside_worktree`
- **D2:** `baseline claims.json:36 was not reported future_dated (exit 1)`
- **D5:** `final-census.json absent or invalid at REV`
- **D6a:** `head-rev-lint exit was not 0`
- **D6c:** `citation slug '../x' did not refuse exit 2 with slug_unsafe`

Restored stdout is byte-identical to pristine: SHA-256 `4a85e091811e925046b452b6779ebef00c771219bdddeb7bac695f9560684ebb`.

**Calibration:** an already-red full detector cannot yield a valid full-run killed/survived score. The table distinguishes response of the selected row from that formal inconclusiveness; other pre-existing failures are not counted as kills. D5’s record is truly absent at S (`git show S:.ufo/waves/round-20/verify/final-census.json` exited 128), not a working-tree inference. The D5 mutation consequently targets its recorder; the named counter does not run that recorder and cannot test stale-rev output without a record.

**[INFERENCE] requested clone-domain limitation:** custody-pair’s `/tmp` refusal at `.ufo/gates/custody-pair/custody-pair.py:903–905` precedes worktree recognition. Also `revexec.py:142` privatizes `/tmp`, while these checks pass the `/tmp` clone root to extracted tools. This explains why D1/D2/D6a/D6c cannot supply clean row baselines here; this report does not turn those baseline failures into regressions of their underlying fixes. No sandbox weakening or synthetic D5 closure was added to manufacture green.
## Mutant → expected → observed

All anchors below are **S** coordinates. `routed:<N>` means `.ufo/waves/round-20/tools/routed-r19.py:<N>`. All rows remain `named=true`. `C` = target substance closed, `O` = open; sequence is pristine → mutant → restored.

| Item / mutation anchor | Expected detector | Observed target output (excerpt), strict exit / total open | Verdict |
|---|---|---|---|
| D1: `.ufo/gates/custody-pair/custody-pair.py:1541` — delete shutil.rmtree(root) | `routed:352`: outside scratch selftest rejects leaked residue / cleanup_after_run | **O → O → O**; `… outside-workdir scratch selftest failed: exit=1 case cleanup_after_run … FAIL … SELFTEST: FAILED cases=33 fails=1`; **1 / 5** | INCONCLUSIVE (pre-open; cleanup response observed) |
| D2: `.ufo/waves/round-20/tools/evidence-timestamps.py:243` — timestamp > committer_time → timestamp < committer_time | `routed:413`: baseline claims.json:36 must be future_dated, strict exit 1 | **O → O → O**; `baseline claims.json:36 was not reported future_dated (exit 1)`; **1 / 5** | INCONCLUSIVE (pre-open) |
| D3: `.ufo/waves/round-20/tools/carrier-guard.py:323` — os.fchmod(fd, mode_after) → os.fchmod(fd, mode_before) | `routed:485`: carrier-guard selftest must fail when arm leaves exec bits set | **C → O → C**; `carrier-guard selftest was not CLEAN exit 0`; **1 / 6** | Target opened; full run INCONCLUSIVE (not a kill) |
| D4: `.ufo/gates/c1-census-v10.py:278` — delete SCORECARD.md:2374–2382 DATED scope row (leave SKILL row) | `routed:609`: archive census must fail after its round-17 scope row is removed | **C → O → C**; `c1-census archive run failed: exit=1 `; **1 / 6** | Target opened; full run INCONCLUSIVE (not a kill) |
| D5: `.ufo/waves/round-20/tools/final-census.py:148` — recorder rev-parse refs/heads/main → refs/heads/main^ | `routed:644`: record must name delivered tree; stale rev must be rejected | **O → O → O**; `final-census.json absent or invalid at REV`; **1 / 5** | INCONCLUSIVE (pre-open) |
| D6a: `.ufo/waves/round-18/tools/head-rev-lint.py:1006` — py_nested = scan_nested(source, tree) → py_nested = [] | `routed:695`: missing nested verify.py/revpin.py findings must open D6a | **O → O → O**; `head-rev-lint exit was not 0`; **1 / 5** | INCONCLUSIVE (pre-open) |
| D6b: `.ufo/waves/round-20/tools/revexec.py:138` — PrivateNetwork=yes → PrivateNetwork=no | `routed:821`: revexec net_refused selftest/preflight must fail | **C → O → C**; `revexec sandbox selftest failed its clean/refusal gate`; **1 / 11** | Target opened; full run INCONCLUSIVE (not a kill) |
| D6c: `.ufo/gates/citation-drift/citation-drift-probe.py:163` — delete slug lexical guard at :163–168; retain realpath containment | `routed:864`: a/b must refuse with slug_unsafe, not snapshot_missing | **O → O → O**; `citation slug '../x' did not refuse exit 2 with slug_unsafe`; **1 / 5** | INCONCLUSIVE (pre-open) |
| D6d: `.ufo/waves/round-17/tools/receipt-validate.py:153` — argv[i + 1] == "analyze" → "analyze" in argv | `routed:878`: weakened argv adjacency must open D6d | **C → C → C**; `both name and substance checks passed`; **1 / 5** | SURVIVED target row; full run INCONCLUSIVE |
| D6e: `.ufo/waves/round-19/tools/wave-outcomes.py:237` — typed causes + wave test → isinstance(doc, dict) and "causes" in doc | `routed:918`: seat_named_causes selftest must fail | **C → O → C**; `wave-outcomes selftest was not CLEAN exit 0`; **1 / 6** | Target opened; full run INCONCLUSIVE (not a kill) |
| D6f: `.ufo/waves/round-18/tools/jj-red-before.py:1191` — delete jj_relative_traversal_refused case at :1191–1197 | `routed:953`: fewer than two additional jj_ ids must open D6f | **C → O → C**; `jj_ source case ids at REV=1 baseline=0; need at least two more`; **1 / 6** | Target opened; full run INCONCLUSIVE (not a kill) |

D6b’s preflight failure opens every runtime-gated row (11 total open); that is one sandbox-preflight response, not eleven independent kills. D6f is caught by the source-ID floor before its selftest executes. D1 adds the real cleanup diagnostic despite its pre-existing scratch-domain failure.
## D6d survivor is behavior-bearing, not an equivalent mutant

Observed by extracting and evaluating only the revision’s `_is_analyze_step` AST function (stdlib `ast` + `re`, no receipt execution or external command):

```text
argv = ["npx", "-y", "rea-agents@6.5.0", "inspect-go-binary", "--", "analyze"]
step shape                         pristine  mutant  restored
{"step":"inspect-go-binary", ...} False     False   False
{"argv": argv}                     False     True    False
{"step":"analyze", "argv": argv}   False     True    False
```

The named routed detector uses the first shape (`routed-r19.py:891–894`), which the independent declared-label check rejects before reaching argv (`receipt-validate.py:143–145`). Therefore removing package/analyze adjacency can remain invisible to D6d even though unlabelled or analyze-labelled decoys become authenticated. **FALSIFIED: this fixture alone establishes argv-adjacency enforcement.** This is an author-side coverage finding, not permission to change the contract.
## Commit / output ledger

Commit IDs belong only to the disposable scratch clone, not the lane. Stdout digests bind the actual full JSON; excerpts above preserve the relevant observed findings.

| Item | Mutant commit (parent S) | stdout SHA-256 |
|---|---|---|
| D1 | `8bb1e9eaa2446ce79ee3f2510f812d0279917208` | `c1b7d7e9761f492e19be448513bc72dca97ba185181e330e247990bff9e12687` |
| D2 | `e293a562351a4e005c3e18120d31c788b45543d4` | `097f8e5272a374245505d1edf38ab444c8ef3bd3244063f9983730ea1c59bac3` |
| D3 | `f5b5b757eca94b430040b9bfddfec92fc4044e2b` | `7831ff797b87b09bc3b057a16094298f023b1abfc217416174dc3c209520237a` |
| D4 | `a2036f8875e0b5f2dbe557ef1f2a5af2a892d8af` | `6cea5e21f5440522c61ee1f3e6fed0ca73100cd0758623e0a797402438db5e38` |
| D5 | `22d8654b0d24b792230f759b1f9afe114775d4a0` | `e09073bbd68457b8d03be28bbfa14aec28f4fdc3c0bd01a942b787cfb4da8ab8` |
| D6a | `0b2bd0754ee2a521c9982be43721e01239819a19` | `990e9204ee6dd829cd1dd119b456b49f80c4f5cb2400ced2166d62f0d5752075` |
| D6b | `8d2a74c1c6e0ddee360ddde09670ed4dc26d4fd0` | `8411a4f2e7d5006ebd213fb4b48481f61dad677d805aa4e03631fd9afd9a52eb` |
| D6c | `a85711d17ebd63e022fe06d6f2c65b056e7361dc` | `4d812fc70e4cb3fc5cfef3823d47b9e10ee926afbdd0be39646de6bd076ad06b` |
| D6d | `310077e1246081bf113bbd52209dacc777bc8df1` | `fe51715093b3188eaeeed974dcd800d68ac2a4bbd188164dca15225760ddbb9a` |
| D6e | `f629e9b3c76ab421c91fe6745e7f59a2d044f265` | `a664aca64fbb925a1e4e5fabf3caecb3d3cadd7a0175ab0298fe319bf5afb3a3` |
| D6f | `9d5b46009f8f5594567ee251d2b80efa293116e4` | `a7a60de41a9810f471eec8182a5c5463afbd081bf88a667b78c63d4911716ed2` |

## Exact-byte restoration ledger

All eleven edited paths were restored with inverse surgical edits **before** the restored detector run. Byte equality against the original `git show S:<path>` payload was true for every row. “Before = restored” is the observed full SHA-256, not a presumed source version.

| Item | Before = restored SHA-256 | Mutated SHA-256 |
|---|---|---|
| D1 | `d81cf5c0eb9c027a3aaadeb0c0b3cc326b36d6e8556a678a4b95e03eee47c146` | `117652065f895175019bcdd9f8bfed85d453d9f996e8745229e5d24df35d9b58` |
| D2 | `2c4fe4d554a4a74b4d7c653ef1157fc91e26796fc8c36b6716abbfdb4febf3a8` | `07ac52c6d9613ccb4202153293327de70d4fe317f531ab7a261a81c77544b1e0` |
| D3 | `62ab550c433741c343cd7f0c5c5e877a01e052f6babc25d0c067895db5eace6b` | `dc41be4669b4a10cc7598ca5d596571fc03d86385690cc6332e1f2d7f477a0a8` |
| D4 | `7567e36e9206b202411e2f0a332ac220245ee3ded5ad654f140d58c0496329bc` | `8c33c4a7e7c4a41d9d92336ab380b5d41ca75c2a2fd4e6265834286a25d006e4` |
| D5 | `02a78af8ca801077393588b59b57240870bd23590f1588efb606e35ce6ac8fa9` | `2f4d2b73b45bc5663793fea808147a723860d7fa92c54c4e2e550ca697d203e7` |
| D6a | `0ae09875e579b44079421212c67930014eff5e20bed577fe65738f970cb5db1d` | `34c0e20bd1326ecba343a32604b3bcaad8dfcbda791f00c2d1efc3985d0fc096` |
| D6b | `d30c503bccf426318c01c811c8e2edae4909f6a7b834936bc1f333eea9853e2c` | `2711ba759cc8d7adcee9d3ec8c01b30609d919012355da7670c3cad009394d52` |
| D6c | `436ae13c7f50cd12061565409784977def6d039331d4687ee2b4f494cedaae68` | `6fc876eaeda4391631d3042663ec685c9044454d335b35d5b865b91835b9a706` |
| D6d | `a31c7db8fbf2f67d34b3f0aad969847794efb8712b1c717b94960652becbe22c` | `47754d170be295de849b22e805a5732f56742de3fceeda763552191046c1f612` |
| D6e | `f925083c4f42c599bdf76f5c2b22402f03feb6f58c64d2c3c254dfcde466b6c8` | `1c342d32dd04f7c4509cedf1d8e33ae16e5401599c0e2923a40ce086dc007adc` |
| D6f | `567a59be96f205faec103cef6792b977960342642a7e6261c857e3fc6944e489` | `94d7be570f19857e0e916229b85081d01298a1e48d6b25ca2de124d2e7ac3921` |

D5 hashes refer to `tools/final-census.py`, not the absent `verify/final-census.json`. The top-level routed detector also matched its original bytes after restoration. No production change or patch is offered.

Cleanup observation 2026-10-21T07:17:30+00:00: own mkdtemp tree `/tmp/kr20w2-MutateRouted-3-00io9uft` removed; `exists()` = `False`. Restored-byte hashes and observed run outputs were retained in memory for filing this report after cleanup.
