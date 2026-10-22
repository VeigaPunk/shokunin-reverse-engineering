# W2 FalsifySuffixMapping — suffix mapping rule (`^\.[A-Za-z0-9]{1,12}$` else `.bin`)

Seat KaidokuR27.FalsifySuffixMapping, round 27 wave 2, 2026-10-22. Attack: REA 6.5.0 `analyze` run live on two byte-identical copies of `/usr/bin/tinyxxd` whose extensions straddle the rule, ids compared against the committed ids. **Verdict: the rule HOLDS — falsification attempt failed; both predictions matched.**

## Prediction (from code, before any run)

`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/ghidra/GhidraTargetSnapshot.js` (6.5.0): `const suffix = safeExtension(sourcePath)` then `` snapshotPath = join(runtimeRoot, `target-${expectedSha256.slice(0, 12)}${suffix}`) ``; `safeExtension` returns the extension only if it matches `/^\.[A-Za-z0-9]{1,12}$/u`, else `.bin` (observation, read 15:36 UTC). `abcdefghijkm`... is 13 characters (`.abcdefghijklm`), so it must be rejected → snapshot `target-7b1e5d0c970a.bin`, predicted id = tinyxxd base id `ev_89338dd2…479b`. `.dat` is kept → snapshot `target-7b1e5d0c970a.dat`, predicted id = committed renamed id `ev_65e0dbfb…7efb` (inference from code).

## Copies (observation, `sha256sum`, 15:36:40Z)

| file | sha256 | size |
|---|---|---|
| `/usr/bin/tinyxxd` (carrier) | `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` | 38928 |
| `…/FalsifySuffixMapping/x.abcdefghijklm` | `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` | 38928 |
| `…/FalsifySuffixMapping/x.dat` | `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` | 38928 |

Both copies byte-identical to the carrier; digest matches the frozen carriers table in `.ufo/waves/round-27/claims.json`.

## Runs (each `TMPDIR=…/FalsifySuffixMapping/tmp npx -y rea-agents@6.5.0 analyze <path> --format json --full-output`, observation)

1. `x.abcdefghijklm`: start 2026-10-22T15:36:59Z, end 15:37:06Z, exit 0. Stdout saved to `out/analyze-x-abcdefghijklm.json`.
2. `x.dat`: start 2026-10-22T15:37:10Z, end 15:37:17Z, exit 0. Stdout saved to `out/analyze-x-dat.json`.

Package pin read after both runs (observation): version `6.5.0`, `package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` — equals the frozen pin.

## Results (observation, jq on saved envelopes, 15:37:30Z)

| copy | `normalized_result.document` | `evidence_id` | prediction | matched | envelope sha256 (stdout bytes) |
|---|---|---|---|---|---|
| `x.abcdefghijklm` | `target-7b1e5d0c970a.bin` | `ev_89338dd2a952f73ad6a3f6d9cea71aacfb2dc3916380fa5691b853d6c164479b` | base id `ev_89338dd2…479b` | yes | `32b5316a5b85dd9a7f679ad9959e5667d241c45be91210a2af028efd746e1d5f` |
| `x.dat` | `target-7b1e5d0c970a.dat` | `ev_65e0dbfb6cca1cce703a51a18ab821b984e5344b4f6377ef51ffd510a0a17efb` | committed renamed id `ev_65e0dbfb…7efb` | yes | `8421b3fda6be709ed08f18ac741d36b2995b08ab68d4a6b8592e1aa216419cb4` |

`subject.digest.sha256` is `7b1e5d0c…ae65` in both; `subject.name` is `x.abcdefghijklm` / `x.dat`.

## Envelope-level check (observation, 15:38:02Z)

`diff` of the two saved envelopes after `delpaths` of `subject.name`, `subject.local_path`, `meta.duration`, `normalized_result.document`: the only remaining difference is `evidence_id` itself. The sole hashed-leaf difference between the runs is `document`, exactly what the rule predicts. (An earlier diff attempt at 15:37:30Z that also deleted a nonexistent `data.meta.duration` path errored in jq and proved nothing; it was redone as above.)

## What this adds beyond the committed table (observation)

- Same id `ev_89338dd2…479b` for `/usr/bin/tinyxxd` (no extension, wave-1 base) and `x.abcdefghijklm` (different directory, different base name, 13-char extension): neither directory, base name nor an over-long extension enters the id; the 13-char extension is demoted to `.bin` as the rule says.
- Same id `ev_65e0dbfb…7efb` for wave-1's `tinyxxd-r27-renamed.dat` and my `x.dat` (different directory and base name, same extension class): extension-only determination of the `analyze` id is confirmed live, closing the committed entry's noted gap ("rests on the code path … not on a separate extension-only run") for the `.dat` side.

## Residual risk and verification gaps

- Only two extensions probed live (`.abcdefghijklm` 13 chars, `.dat`). The 12-char boundary, uppercase, non-alnum and multi-dot cases rest on code reading, not live runs (unknown).
- Envelope bytes differ from the committed wave-1 renamed envelope (`9da2571d92af…` in `runs.tsv`) because envelope bytes carry duration/name/path; only the id is stable. Expected, not a mismatch.
- One pin: rea-agents@6.5.0 only; nothing here speaks to 6.7.0 or MCP sessions.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r27/seats/w2/FalsifySuffixMapping/`, sha256)

- `x.abcdefghijklm` — `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65`
- `x.dat` — `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65`
- `out/analyze-x-abcdefghijklm.json` — `32b5316a5b85dd9a7f679ad9959e5667d241c45be91210a2af028efd746e1d5f`
- `out/analyze-x-dat.json` — `8421b3fda6be709ed08f18ac741d36b2995b08ab68d4a6b8592e1aa216419cb4`

No tools were installed or upgraded (existing npx cache used); no lane files other than this report were touched.
