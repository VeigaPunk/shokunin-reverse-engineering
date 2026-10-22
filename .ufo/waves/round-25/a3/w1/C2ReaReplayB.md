# C2ReaReplayB — REA 6.5.0 replay vs saved a2 envelopes (carrierb, stewardtoken, carrierv)

Verdict: **holds**. For all three carriers the REA 6.5.0 replay is byte-identical to the saved
`corpus/evidence/round-25/a2/c2/<carrier>/envelope.json`. No counterexample found.

Scope: carriers `carrierb`, `stewardtoken`, `carrierv` only. (`rv2token`, `kdxtoken`,
`vaultb-opt200` are owned by peer `KaidokuR25a3.C2ReaReplayA`; confirmed disjoint by message.)

## Commands (argv, exit codes, UTC)

Environment: `TMPDIR=/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2ReaReplayB/tmp`,
`npx -y rea-agents@6.5.0` (node v24.21.0, npx 11.19.0), `npx rea-agents@6.5.0 --version` → `6.5.0`.
Paths taken from `corpus/evidence/round-25/a2/c2/carriers.tsv` (lane-relative → absolute).

```
carrierb    exit=0 start_utc=2026-10-22T10:43:36Z end_utc=2026-10-22T10:43:37Z
  argv=npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.runtime.hex hex --format json
stewardtoken exit=0 start_utc=2026-10-22T10:43:38Z end_utc=2026-10-22T10:43:39Z
  argv=npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c1/EX-03/runtime.hex hex --format json
carrierv    exit=0 start_utc=2026-10-22T10:43:40Z end_utc=2026-10-22T10:43:40Z
  argv=npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex hex --format json
```

All three runs exited 0 with empty stderr. Reproduced a second time from a **fresh npm cache**
(`npm_config_cache=.../npmcache-fresh`, package freshly fetched from
`https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`, installed tree
`.../npmcache-fresh/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` → version `6.5.0`):
exit=0 for all three, stdout sha256 unchanged, only stderr difference is one npm deprecation
warning (`npm warn deprecated prebuild-install@7.1.3 ...`) emitted only on the fresh fetch.

## Comparison (observation)

Command: `python3` comparison of replay stdout vs saved envelope, plus `cmp` byte compare.

| carrier | evidence_id equal | functions equal | n functions | full JSON equal | bytes identical |
|---|---|---|---|---|---|
| carrierb | yes (`ev_61b29a8…ae74e`) | yes | 8 | yes | yes |
| stewardtoken | yes (`ev_94dd707…4018`) | yes | 22 | yes | yes |
| carrierv | yes (`ev_026e6cf…b817`) | yes | 15 | yes | yes |

Exact evidence ids (saved == replay, full strings):
- carrierb `ev_61b29a8609cd791df076e254616184644cf4bed78809a203647890ae9ccae74e`
- stewardtoken `ev_94dd7079222268226c3a6164ef3cd499f3c4397c28c9f845b8eaab5312b54018`
- carrierv `ev_026e6cfaf2a6719715b6df46a564ebb32a97877ad88c4b7bef1b139a5ad9b817`

Equality was checked at four levels per carrier: `evidence_id`, `raw_result.functions`,
`normalized_result`, and whole-document `==` on the parsed JSON. `cmp` shows the replay stdout is
byte-identical to the saved `envelope.json` for all three carriers (not merely parsed-equal).
`raw_result.metadata` (bytecode offsets/sha) is therefore also identical.

Replay stdout sha256 (identical in the warm-cache and fresh-cache runs, and equal to the
sha256 recorded in `a2/c2/<carrier>/rea-run.txt`):
- carrierb `95e86017fc1ee8f75b616cbe62e0d878302af1e30d367aa1bb769fc5966ec0d6` (10035 bytes)
- stewardtoken `1de20e9604885579649a6486306518a906c1aac6c4961a818e53d3cdd82b642a` (16746 bytes)
- carrierv `a2e7ba7b27a9fece86842d641462cd6ad7fffe219feffd40b583b2c4d1e8b8e4` (11442 bytes)

The replay stdout is also byte-identical to the L1's own prior replay files
`corpus/evidence/round-25/a3/c2/rea-replay/<carrier>.json` for the same three carriers
(`cmp` → identical), so two independent replay sessions agree.

## Input integrity (observation)

sha256 of each runtime hex at replay time equals the `subject.digest.sha256` stored in the saved
envelope, so the input files did not change between the a2 capture and this replay:
- carrierb `247e09f3650aab9010b72b21c68af874b08dbc8d16bab54032d0c4a0017149cd`
- stewardtoken `cf13c82fb5b0bc73c7c27f1b2217997edda028c6f13b5ee577b9de09ae10b1eb`
- carrierv `e0b1021c68f8de8c3f049f4242769548b6f8271a00986f2ab20f049f8748a192`

Selectors observed per carrier (from `raw_result.functions`, bare 4-byte selectors, in saved order):
- carrierb (8): 3efdef66, 410673e5, 51f91066, 6ea056a9, 8da5cb5b, ca1d209d, d5d44d80, e7ee6ad6
- stewardtoken (22): 06fdde03, 095ea7b3, 0c751377, 18160ddd, 1aa02d59, 23b872dd, 24a9d853,
  313ce567, 3f4ba83a, 40c10f19, 5c975abb, 637eea19, 70a08231, 8456cb59, 875194ac, 95d89b41,
  a9059cbb, cee38a15, d0e30db0, d869f754, db006a75, dd62ed3e
- carrierv (15): 0776076f, 0c751377, 1aa02d59, 27e235e3, 2e1a7d4d, 3f4ba83a, 4643c56b, 48a3ef5c,
  5c975abb, 6e8efde2, 8456cb59, 8da5cb5b, b144adfb, d0e30db0, e0749a6a

## Labels

- observation: exit codes, UTC times, sha256 digests, byte/parsed equality, selector lists above.
- inference: the a2 envelopes are reproducible from the same REA 6.5.0 build and unchanged inputs;
  `evidence_id` is therefore a deterministic function of the carrier bytecode under REA 6.5.0.
- unknown: whether REA 6.5.0 output stays stable on other hosts (node/OS/EVM toolchain not pinned
  by the envelope — `environment` is `null` in the saved envelopes, so the envelope itself carries
  no host provenance). Cannot be evaluated from this lane; noted as a residual risk for the
  C2 claim, not a defect of the replay.

## Lane bounds

Read-only on the lane: only `git status --porcelain`, `git rev-parse HEAD` (read-only) were run in
the lane; HEAD is `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`. `SCORECARD.md`,
`corpus/lessons/round-25.md` and untracked `corpus/evidence/round-25/a3/after/` were already
modified/untracked before this seat ran and were not touched by me. No lane file was written
except this report. No `jj` command was run. No git write, no commit. No network source was opened;
no signature-database lookup was needed (selectors were read from the local envelope).

## Tooling

- `rea-agents` 6.5.0 via `npx` (npm registry, official channel) — already required by the card;
  no install into the system, no pacman transaction, no host service restart.
- node v24.21.0, npx 11.19.0 (pre-existing).

## Artifacts (sha256)

All under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2ReaReplayB/`:

| file | sha256 |
|---|---|
| carrierb.json, run-carrierb.json, fresh-carrierb.json | 95e86017fc1ee8f75b616cbe62e0d878302af1e30d367aa1bb769fc5966ec0d6 |
| stewardtoken.json, run-stewardtoken.json, fresh-stewardtoken.json | 1de20e9604885579649a6486306518a906c1aac6c4961a818e53d3cdd82b642a |
| carrierv.json, run-carrierv.json, fresh-carrierv.json | a2e7ba7b27a9fece86842d641462cd6ad7fffe219feffd40b583b2c4d1e8b8e4 |
| compare.json | 03a2079266e2f750f73e155340c66d4131e3eeba211dc24d474d1fbfd568747d |
| runs.txt | 943a67b6f417208dc4ac8c35e42adaa29e7cf57cd3726cc0b0d14096eb250b9f |
| carrierb.err / stewardtoken.err / carrierv.err (and run-*.err) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty, 0 bytes) |
| fresh-carrierb.err | npm deprecation warning only (not part of stdout) |

Report: .ufo/waves/round-25/a3/w1/C2ReaReplayB.md
