# C2ReaReplayA — REA 6.5.0 replay vs saved a2 envelopes (rv2token, kdxtoken, vaultb-opt200)

Verdict: **holds** for all three carriers. The REA 6.5.0 replay is byte-identical to the saved
`corpus/evidence/round-25/a2/c2/<carrier>/envelope.json`. No counterexample found.

Scope: carriers `rv2token`, `kdxtoken`, `vaultb-opt200` only. (`carrierb`, `stewardtoken`, `carrierv` belong to peer `KaidokuR25a3.C2ReaReplayB`; disjointness confirmed by message.)

## Commands (argv, exit codes, UTC)

Environment: `TMPDIR=/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2ReaReplayA/tmp`, `npx -y rea-agents@6.5.0` (node v24.21.0, npm 11.19.0). Version check `npx -y rea-agents@6.5.0 --version` → `6.5.0` (exit 0, 2026-10-22T10:40Z). Carrier paths from `corpus/evidence/round-25/a2/c2/carriers.tsv`, lane-relative → absolute. Driver: `replay.sh` in this seat; it records argv, exit code, UTC start/end, byte counts and sha256 of both streams.

```
rv2token       exit=0 start_utc=2026-10-22T10:44:11Z end_utc=2026-10-22T10:44:12Z
  argv=npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json
kdxtoken       exit=0 start_utc=2026-10-22T10:44:12Z end_utc=2026-10-22T10:44:13Z
  argv=npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/EX-05/kdx-runtime.hex hex --format json
vaultb-opt200  exit=0 start_utc=2026-10-22T10:44:13Z end_utc=2026-10-22T10:44:13Z
  argv=npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.runtime.hex hex --format json
```

All three runs exited 0 with empty stderr (sha256 of empty stream `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

## Comparison (observation)

Command: `python3 -I -B compare.py` (this seat) — byte compare plus parsed-JSON compare of the replay stdout against the saved envelope, at four levels: `evidence_id`, `raw_result.functions`, `normalized_result.functions`, and whole-document `==`.

| carrier | evidence_id equal | functions equal | n functions | full JSON equal | bytes identical |
|---|---|---|---|---|---|
| rv2token | yes (`ev_78769b9…ba51`) | yes | 5 | yes | yes |
| kdxtoken | yes (`ev_dbccef49…d89`) | yes | 6 | yes | yes |
| vaultb-opt200 | yes (`ev_b58d82e0…3d0bb`) | yes | 13 | yes | yes |

Full evidence ids (saved == replay): rv2token `ev_78769b9b5a7b901b45f914e99f2feea5e4e7bcf1775da40e50406bdbd786ba51`; kdxtoken `ev_dbccef49e8903f3a42739afe0bf18848121a5e3e1179b271cae3fb93d5adad89`; vaultb-opt200 `ev_b58d82e0f563a5fe06ba4f5211379a9b94aa49644aff9fc6372a471a2103d0bb`. `compare.py` also reports `leaf_diff_count = 0` for all three (every scalar leaf in the parsed tree compared equal) and `key_paths_only_in_new = []`, `key_paths_only_in_env = []`.

Replay stdout sha256 (equals the sha256 recorded in `a2/c2/<carrier>/rea-run.txt`): rv2token `ed4a1118dfc7a180fac794541371019ce8bc2272908860bc1fd4bf99ad2cbf50` (10307 bytes); kdxtoken `1bc65b6f3f396f9efea242a2ca25317c90c1c85e9c79798a16bba43ee8274462` (10248 bytes); vaultb-opt200 `506c9101ab85e2c45d221054b923d850923a740792789de378b8fb1ce5d4aeba` (11528 bytes). The sha256 of each runtime hex at replay time equals the `subject.digest.sha256` and the `normalized_result.artifact.sha256` in the saved envelope and the `carrier_sha256` recorded in `a2/c2/<carrier>/rea-run.txt` (lane carrier digests below). Recovered selectors (`raw_result.functions`, bare 4-byte, saved order) are listed verbatim in the replay stdout artifacts: rv2token and kdxtoken carry the five ERC-20 selectors (kdxtoken adds `40c10f19`), vaultb-opt200 carries 13.

## Reproducibility beyond the first run (observation)

1. Second run, warm npm cache, 2026-10-22T10:45:03Z–10:45:06Z, exit 0 for all three: stdout sha256 unchanged, `cmp` identical to the first run.
2. Third run from a **fresh npm cache** (`npm_config_cache=<seat>/npmcache-fresh`, package fetched from the npm registry; installed tree `rea-agents/package.json` → version `6.5.0`), 2026-10-22T10:47:04Z–10:47:09Z, exit 0 for all three: stdout sha256 unchanged, `cmp` identical. The only stderr content anywhere was one npm deprecation warning (`npm warn deprecated prebuild-install@7.1.3 …`) on the fresh fetch for rv2token; stderr does not enter stdout.
3. Independent session: the replay stdout is byte-identical (`cmp`) to the L1's earlier replay files `corpus/evidence/round-25/a3/c2/rea-replay/{rv2token,kdxtoken,vaultb-opt200}.json` (written 2026-10-22T09:25:30Z–09:25:31Z per `runs.txt`).

## Attacked: what the replay does and does not pin (observation)

The claim under test is reproducibility of the saved envelope under REA 6.5.0. Two probes bound what "reproducible" means here; both qualify the C2 claim.

1. **`evidence_id` is path-dependent, not content-dependent.** The same bytes copied to `<seat>/probe/Renamed.runtime.hex` gave id `ev_ee2f0611…b2508`; the same bytes under their original name in `<seat>/probe/sub/` gave `ev_9c62b6e2…c815b`. Both differ from `ev_78769b9…ba51` while `raw_result` stayed equal, so the saved `evidence_id` is a function of the absolute lane path and file name, not of the bytecode alone.
2. **`evidence_id` is REA-version-dependent.** `npx -y rea-agents@6.7.0` on the same rv2token path (2026-10-22T10:48Z, exit 0) produced id `ev_19d7d3cb…0b3f38`. A leaf-by-leaf diff of 6.5.0 vs 6.7.0 shows `/evidence_id` as the **only** differing path; `raw_result` and all recovered functions are identical.

Consequence for C2: the a2 envelope's `evidence_id` is reproducible only for the same carrier at the same absolute path under REA 6.5.0. The selector content the knowledge entry relies on is stable across both the path change and the 6.5.0→6.7.0 version bump, so the learning claim itself is not disturbed; but the id is not a content address and must not be cited as one.

## Labels, bounds and tooling

- observation: exit codes, UTC times, argv, sha256 digests, byte and parsed equality, selector lists, and the path/version probes above.
- inference: the a2 envelopes for these three carriers are reproducible from the same REA 6.5.0 build at the same lane paths with unchanged inputs; `evidence_id` is deterministic under that fixed triple (path, filename, REA version), not under the bytecode alone.
- unknown: whether REA 6.5.0 output stays stable on other hosts. The saved envelope has `environment: null`, `analysis_profile: null` and `relationship_coverage: null`, so it carries no node/OS/native-toolchain provenance; cross-host stability cannot be evaluated from this lane. Residual risk for C2, not a defect of the replay.
- lane bounds: read-only on the lane. Only `git rev-parse HEAD` and `git status --porcelain` ran in the lane; HEAD read as `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` at seat start and has since moved to `dc31f9c441528cfff1070c0574eea9669fd47e64` by another seat. The only lane file I wrote is this report. No `jj` command, no git write, no commit, no stash. No network source was opened and no signature-database lookup was made, so no request budget was consumed.
- tooling: `rea-agents` 6.5.0 via `npx` (npm registry, official channel) — required by the card; no system install, no pacman transaction, no host service restart, no downgrade. `rea-agents` 6.7.0 was fetched once for the version-sensitivity probe only; not used for any claim.

## Artifacts (sha256)

Under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2ReaReplayA/`: `replay.sh` `c10894d34793ce04c3d95db3ab20ae902025e6ab0cceca947d780da3acddd8f2`; `compare.py` `951fbb1f1e0f099a572e36612693b93747293d51812883ce4097fa3f7f68c1c0`; `compare.json` `797d53263ac879cd4f94376086830ba7c91c186622eebe1abc63e47d833370c7`; `fresh-cache-version.txt` `f5e1cb79459702db8fb6ffe23d5ae92b5496b4379c2aa8c2470b2f9b51e34e4a`; stdout copies for each carrier in `runs/`, `runs2/` and `fresh/` (identical bytes; sha256 as listed above); `runs/*.meta` rv2token `7980eee93214549f54d67a32b8fd045710706cf422e57e8b4b36f52e737b91f4`, kdxtoken `56fa2109047e7d806291f2404dc5dc946c7b64bfbc0e854f29201439d0a9a26c`, vaultb-opt200 `a8c51e11a0a5844adeca0ec9619b61912f4b50cb38a96a920f5c789d4033db6c`; all empty stderr files `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; `fresh/rv2token.err` `fe49a93af7f6a5072c3a3ef65019009ce521808d6b5a32810ad9a6a433f4524d` (npm deprecation warning only); `probe/v670.json` `12e5d171396354065979df8a0f109beb41598e5fe33cf6490a4e46f6e85076fb`; `probe/renamed.json` `cda87e4743c655283bf1e8b71094e4d8314600ab75bc955b2afe177d0c4e160d`; `probe/subdir.json` `28edbc816af8245213c695f6f861adf837ccd2c9fe522a56aee629ce3d2319c8`; `probe/Renamed.runtime.hex` and `probe/sub/Rv2Token.runtime.hex` `d7f73058e2d9fb2563bf96b2f26902f233530de027a7943185e15bfdc4e1048f`. The fresh npm cache tree was deleted after the run; its installed `rea-agents` version (6.5.0) is in `fresh-cache-version.txt`. Lane carrier digests: rv2token `d7f73058e2d9fb2563bf96b2f26902f233530de027a7943185e15bfdc4e1048f`, kdxtoken `69a15782678dccdd4d43b2f0af566c2f030fe9dee4de4ef8365bc4b6d1b29ad6`, vaultb-opt200 `9a1fbfaba9e3a89c1ce8bc12291c305500beef48a73ee270e6116cd5febb1d88`.

Report: .ufo/waves/round-25/a3/w1/C2ReaReplayA.md
