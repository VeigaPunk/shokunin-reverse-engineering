# FreshnessR26 — re-verification of two round-26 rows on /usr/bin/jq at rea-agents@6.5.0

Seat: `KaidokuR27.FreshnessR26`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Round 27, attempt 1, wave 1. Date of runs: 2026-10-22 UTC.
Scope: freshness only. These two runs are **not** R27-C1 table rows and are not proposed as such.
Lane files touched: only this report. Lane corpus, tools, `.ufo` counters and the Git index were read-only.

## Question (from the card)

Does the round-26 `base_id` of the verbs `analyze` and `inspect-binary-layout` on `/usr/bin/jq` still
hold when the same command is run today at the same pin `rea-agents@6.5.0`? Round-26 reference read
with `git show main:corpus/evidence/round-26/c1/table.tsv` (read at 2026-10-22T14:54Z; exit 0); the two
`base_id` values are in the table below, and the round-26 verdicts for these rows were `analyze` =
`content-keyed` and `inspect-binary-layout` = `path-sensitive`.

## Result (observation)

Both ids are unchanged. No difference was found, so there is no freshness finding to report.

| verb | round-26 base id | today id (2026-10-22) | equal | today envelope sha256 | utc_start | utc_end | exit |
|---|---|---|---|---|---|---|---|
| analyze | ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328 | ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328 | yes | 66e7b3fac414132c2f16cbad1249371eb22eb30beead399ab9673f67228f9920 | 2026-10-22T14:54:59Z | 2026-10-22T14:55:05Z | 0 |
| inspect-binary-layout | ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd | ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd | yes | 98a1a229f20ed41867b8ea13a5d8812f158a589c99fb3798e631c13a72b30ebf | 2026-10-22T14:55:07Z | 2026-10-22T14:55:08Z | 0 |

Round-26 envelope sha256 for the same two runs, from `git show main:corpus/evidence/round-26/c1/runs.tsv`:
`analyze` base `3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb`;
`inspect-binary-layout` base `4a256cc73b54529b3eae4b9bafa6724a358be55bf5056867c4557f5357dfbb8f`.
The envelope **bytes** differ from round 26 for both verbs, but only in the recorded wall-clock duration:
a per-key diff of the fresh envelopes against the round-26 base envelopes shows exactly one changed
line in each file, `/meta/duration` (`5912ms` to `4943ms` for `analyze`, `194ms` to `159ms` for
`inspect-binary-layout`). The `inspect-binary-layout` envelope bytes are byte-identical to the round-26
`repeat` envelope of the same verb (`98a1a229f20ed41867b8ea13a5d8812f158a589c99fb3798e631c13a72b30ebf`),
which is a duration coincidence, not a new identity.

## Commands run (observation)

Both calls were run one after another, never in parallel, on the carrier only, with the pinned form:

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r27/seats/FreshnessR26/tmp npx -y rea-agents@6.5.0 analyze /usr/bin/jq --format json --full-output
TMPDIR=/fast/scratch/hyaku/kaidoku-r27/seats/FreshnessR26/tmp npx -y rea-agents@6.5.0 inspect-binary-layout /usr/bin/jq --format json --full-output
```

Both exited 0 with empty stderr (two 0-byte files, sha256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`) and non-empty JSON on stdout
(7559 and 80065 bytes). No retry was needed; each verb was called exactly once.

## Pin check (observation)

`package.json` of the resolved package root
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`:

- read before the first call (2026-10-22T14:53Z) and after the second call (2026-10-22T14:55:34Z),
  identical both times: version `6.5.0`, sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`.
- that sha256 equals the value frozen in `.ufo/waves/round-27/claims.json` (`R27-C1.invocation`).
- the file mtime is 2026-10-22T08:22:00Z, which is before both calls, so the pin did not change
  inside the run window; no second read between the two calls was taken, and the before/after reads
  bracket them.
- the 6.7.0 root `a1722018f28f9df2` reports version `6.7.0`, sha256
  `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`; it was not used for any call here.

## Independent recomputation (observation)

`tools/round-26/recompute-ids.py` (read from `main`, sha256
`89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b`, run from a copy in this seat with
`python3 -I -B`) reports for both fresh envelopes `MATCH`, stored id equal to recomputed id, and
`recomputed ids: 2 match of 2 total`, exit 0. It also prints the path-bearing fields of the hashed
projection: `none` for `analyze`, and for `inspect-binary-layout` `/parameters/path`,
`/normalized_result/artifact/path`, `/locations/0/path` (all `/usr/bin/jq`) plus the interpreter
display string. This is consistent with the round-26 table verdict `path-sensitive` for that verb and
says nothing about the six verbs not run here.

## Carrier custody (observation)

`sha256sum /usr/bin/jq` after the calls (2026-10-22T14:56:21Z) gave
`e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, size 30800 bytes, mtime
2026-06-20T17:10:39Z. The value equals the carrier sha256 in the claims file and the
`subject_sha256` in both fresh envelopes. The carrier was only read.

## Files written by this seat

Only this report inside the lane. All other artifacts are under
`/fast/scratch/hyaku/kaidoku-r27/seats/FreshnessR26/` (sha256 of file bytes):

- `envelopes/analyze-base.json` 66e7b3fac414132c2f16cbad1249371eb22eb30beead399ab9673f67228f9920
- `envelopes/inspect-binary-layout-base.json` 98a1a229f20ed41867b8ea13a5d8812f158a589c99fb3798e631c13a72b30ebf
- `analyze-base.stderr`, `inspect-binary-layout-base.stderr` (seat root, both 0 bytes, sha256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`)
- `runs.tsv` 4a6d23068e92966759545acd0d6a8148f4a2b77d37f4c99c108bb134718c26a6 (two data lines; the
  header follows the frozen round-27 corpus header: seat, carrier, verb, run, path, argv, exit,
  utc_start, utc_end, envelope_sha256, evidence_id, subject_sha256, pkg_version, pkg_json_sha256)
- `compare.tsv` 86b41b55b6c74f157c0cafcb5b8c19db80eefb5c51bdf2bf865601c2f14ab8ee
- `recompute-ids.py` 89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b
- `recompute-ids.txt` f183e4e860c9427cb65a6b31370678ff1b73914cc0e9feee52c662db495102a9
- `r26-table.tsv` 89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df
- `r26-runs.tsv` 250a00a8ddda82eb712def66300fdfeef185d5296afde6dfe040c8784040d6c5
- `carrier-after.sha256` c6d5446094c4733655e7a3db7784db8070ee92c346339084750813600fb13820

Nothing was written to the renamed carrier copies and nothing was written to the round-27 corpus.

## Failures, retries, risks

- Failures: none. Both calls exited 0 and both envelopes parse as JSON with `ok`, `data`, `meta`;
  `meta.command` equals the verb in each; `.data.subject.name` is `jq` and `.data.subject.digest.sha256`
  is the carrier digest in both.
- Retries: none, so there is no second-attempt record.
- Risk (inference): this is a two-row freshness check at one pin on one carrier. It shows that the
  round-26 `analyze` and `inspect-binary-layout` ids reproduce today; it does not re-derive the
  round-26 verdicts, because the round-26 verdicts also rest on the `repeat` and `copy` runs, which
  this seat did not repeat.
- Risk (observation): envelope bytes are not byte-stable across runs (`/meta/duration` changes), so any
  future check that compares envelope sha256 instead of `evidence_id` would report a false difference.
- Unknown: whether the other six round-26 verbs still reproduce their ids; this seat did not run them.

## Tooling

No package was installed, upgraded or removed by this seat. `npx -y rea-agents@6.5.0` was already
present in the local npx cache at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/` and was used as pinned.
No host service was restarted and no pacman transaction was run.
