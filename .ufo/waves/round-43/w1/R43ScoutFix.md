DONE — held-out regen recon for P43-C1 complete: layout inventoried, seed/REA byte provenance mapped, all 14 fixture pins verified, disk guard green, run.json mirror schema tabulated, and five port-time risks for the L1 identified.

# R43ScoutFix — R43-C1 held-out regeneration recon

Scope: what the round-43 data run (`tools/round-43/heldout-gen-v4r43.py --seed <FREEZE> --out corpus/evidence/round-43/c1/heldout --run --scratch …`) must reproduce, based on the committed round-42 set. All paths below are lane-relative to `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Artifacts: `.ufo/waves/round-43/w1/artifacts/R43ScoutFix/`.

## 1. Held-out layout inventory (corpus/evidence/round-42/c2/heldout/, 6.5 MB total)

78 carrier dirs + one `manifest.json` (164,827 B):

| entry | count | content |
|---|---|---|
| `H01`–`H54` | 54 | 27 named classes × 2 replicates (`carriers_per_class: 2`) |
| `C01`–`C24` | 24 | combo carriers (`families.combo.count: 24`, `min_decisions: 2`) |
| `manifest.json` | 1 | seed `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b` (= the r42 freeze), `round: 42`, `claim: R42-C2` |

Per-dir files (all 78 dirs have all five): `carrier.sqsh`, `envelope.json`, `rea-full.json`, `run.json`, `tree.json`.

| file | n | total bytes | provenance |
|---|---|---|---|
| `carrier.sqsh` | 78 | 2,559,538 | **seed-derived** — pure function of `--seed` (random.Random on `seed[:16]^(class_index*1000+k)`; SHA-256 counter stream for contents; no clock/urandom/host input — docstring §"Every byte this script emits") |
| `tree.json` | 78 | 151,390 | **seed-derived** — generator's own oracle (seed recorded inside each file) |
| `manifest.json` | 1 | 164,827 | **seed-derived** at r42 (declared tuples are factor-predicted); at r43 it also embeds `generator.tuple_check`, which is REA-derived-but-deterministic |
| `envelope.json` | 78 | 1,393,099 | **REA-derived** — `data` object of the REA CLI envelope |
| `rea-full.json` | 78 | 1,462,610 | **REA-derived** — full `{ok,data,meta}` envelope (meta.duration is wall-clock, non-deterministic) |
| `run.json` | 78 | 105,377 | **mixed** — generator record + envelope-derived shape summary (provenance per field: `runjson-fields.json` artifact) |

Arm/operation census over the 78 `run.json` (extract_schema): `arm`: after=57, before=19 (before = `$HOME/.local/bin` stripped from child PATH; all four `dep-missing*`/`legacy-dep-missing*` classes, plus 11 of 24 combos by factor draw `dep: 1`), `arm: "ood"`=2 (H25, H26, `out-of-domain` class, `inspect_firmware_regions` op). `operation`: `extract_firmware` 76, `inspect_firmware_regions` 2. `home_bin_on_path`: true=57, false=19, absent=2 (ood schema has no such key). `be_argv`: n/a=55, yes=16, no=7. `coverage`: partial=65, complete=11, signature_scan=2. `files==0` (P=zero): 24 carriers (C03, C07, H05, H06, H13–H20, H23–H26, H37, H38, H43–H48).

Digest bindings verified (all 78): `manifest.carriers[].sha256` == sha256 of committed `carrier.sqsh` (0 mismatches); `envelope.subject.digest.sha256` == manifest `sha256` (0 mismatches; `run.json.digest_matches_carrier` true throughout).

One carrier is **seed-independent**: `H43` (`legacy-dep-missing-be`, sha256 `529e10775c…` = raw `v1-be` fixture bytes) has identical carrier sha256 in dev and heldout manifests — fixture-pinned bytes need no seed regeneration to match, everything else does. (`declared_features.seed_dependent` marks which records are.)

## 2. Dev arm (corpus/evidence/round-42/c2/dev/, 2.0 MB)

78 dirs but only **two files each**: `envelope.json` (1,423,231 B total) + `run.json` (106,263 B) — no `carrier.sqsh`, `tree.json`, or `rea-full.json` committed. Its `manifest.json` (165,808 B) has identical top-key set to heldout's but `seed: e48947bb2a1542206bc6a324257b3500231946e3` (≠ r42 freeze) and `generator.sha256: a054e5cd…` (≠ the frozen generator's `c2b1641a…`) — the dev arm predates the last generator edits; that is the QUALITY-84 dry-run artifact, not a regen target. Dev arm arms: after=59, before=17, ood=2 (different seed ⇒ different factor draw). **Notable:** dev C02's observed gap_kinds == its declared ({extractor-failure, unpublished-entry}) — the R42-CL1 defect only materialized at the freeze seed's draw, which is exactly why QUALITY 85 binds the check at manifest-finalization time of the real data run.

## 3. run.json receipt schema the round-43 run should mirror

Two schemas (see `runjson-fields.json` for full provenance map):

- **extract_firmware (76/78):** `arm, be_argv, class, class_expected, coverage, declared, declared_extras, depth_limited_paths, diagnostics, digest_matches_carrier, duration, exit_code, expected_action, expected_label, factors, failed_chunks, files, gap_dependencies, gap_kinds, handlers, home_bin_on_path, id, max_depth, ok, operation, parameters, provider, rea_argv, subject_sha256, symlink_removed, unblob_command`
- **out-of-domain (2/78, H25/H26):** the same 31 keys minus `factors`, `home_bin_on_path`, `max_depth` — 28 keys. Its `rea_argv` carries no `--max-depth`; `parameters` is `{"max_depth": null}`; `provider` is `binwalk`, `coverage` `signature_scan`, `files` 0, `expected_label` `unclassified`.

Field semantics to mirror: `rea_argv` is a template (`"$out"` placeholder, package string `rea-agents@6.5.0`); `duration` is envelope `meta.duration` (non-deterministic — do not byte-compare run.json across runs); `declared` is a permanent `null` tombstone (R41-CL1: binding lives only in `carriers[].declared_features`); `handlers` = sorted **chunk** handlers only (§7 item 3).

## 4. Manifest generator block + declared_features contract

`generator` block keys (artifact `manifest-blocks.json` holds the full dump): `name` (`heldout-gen-v4.py`), `version` (`r42-c2-v4`), `sha256` (self-hash of the script — `c2b1641a…`, matches the committed file), `carriers_per_class` (2), `writer` {name `gen-squashfs.py`, path `tools/round-39/gen-squashfs.py`, sha256 `f535e60e…`, block_encoder note — still same bytes today}, `partial_pin` (R40-CL4: compressed-length pin, fill 00, max_damaged_block 136, fail_range [26,136], absorbed_from 1730), `fixtures` {pins `fixtures.json`, pins_sha256 `9f957663…` (matches), project onekey-sec/unblob, commit `1fcc7a0a…`, url_base, license MIT, count 14, resolution order `committed --fixtures-dir → --scratch cache → --fetch URL`}.

`declared_schema` (the R41-CL1 contract): binding `observed_features_match_declared`; single key `declared_features`; six fields `handler_set, gap_kinds, gap_dependencies, be_argv, symlink_removed, published`; extras `extraction_failed, max_depth` live in `declared_extras` outside the binding. Round 43 adds `generator.tuple_check` (per-carrier observed/declared verdicts) — a manifest key that did not exist at r42.

Declared-vs-observed audit across the committed r42 set (observed extracted from `run.json` shape fields): **1 mismatch — C02** only. Declared `gap_kinds: [extractor-failure, unpublished-entry]`; observed `[depth-limited, extractor-failure, unpublished-entry]`. This is routed defect R42-CL1 = M42-2, byte-verified. Its combo factor signature: `base:v4, damage:1, max_depth:1, legacy_fixture:v3adapt-be (squashfs_v3), endian:be, links:in-tree, body_v4:true` — a failing damaged chunk beside a sibling that reaches the depth ceiling.

## 5. Fixture pins vs committed copies — ALL MATCH

14 files under `corpus/evidence/round-42/c2/fixtures/` (naming: `<id>--<file>`), every sha256 equals its `tools/round-42/fixtures.json` pin (full table: `fixtures-sha256.txt`):

| id | sha256 (matches pin) | size |
|---|---|---|
| v1-be | 529e1077… | 4096 |
| v1-le | b45925fa… | 4096 |
| v2-be | 79c0f388… | 4096 |
| v2-le | 7c62dbe3… | 4096 |
| v2ns-be | 6560be64… | 4096 |
| v2ns-le | f25cf3ea… | 4096 |
| v3-be | 4e9493d9… | 4096 |
| v3-le | 0161351c… | 4096 |
| v3adapt-be | 71971c7a… | 4096 |
| v3adapt-le | 2ac15e5c… | 4096 |
| v3bc-le | 6baad438… | 4096 |
| v3ddwrt-be | daa8e72d… | 320 |
| v3ns-be | 01b2792b… | 4096 |
| v3ns-le | 3bce6ae3… | 4096 |

`fixtures.json` also carries `duplicate_bytes` notes (v3bc-be = v3-be, v3ddwrt-le = v3-le bytes; only referenced, no extra files needed) and `damage_offset/damage_len` (4-byte zero window) per pin. `--fixtures-dir` resolution: committed dir → `KAIDOKU_FIXTURES` env → `--fetch` URL. For the r43 counter's regen materialization (`GEN_TREE_PREFIXES` at c2-counter.py:124-127, env `KAIDOKU_FIXTURES`), the fixtures dir must sit under the tree prefix it materialises — keep the same relative position in round-43 (the claim freezes the r42 fixture dir itself, so a no-op if the port reuses `corpus/evidence/round-42/c2/fixtures`).

## 6. Environment + disk

- `disk-guard.sh status` (2026-10-27): `/fast/scratch/hyaku` 610.8 G free (24%), `/tmp` 125.1 G free, `/home` 590 G free. Round-42's total held-out payload was 6.5 MB; 78 REA runs at ~1 s each (~90 s CPU total) plus a small npx package cache — capacity is not a constraint.
- Host tools present: `unblob` 26.6.4 (`~/.local/bin/unblob` → uv tool), `sasquatch` + `sasquatch-v4be` in `~/.local/bin`, `unsquashfs`, `7z` in `/usr/bin`. `REA_PACKAGE = 'rea-agents@6.5.0'` (npx -y). `tools/round-39/gen-squashfs.py` sha256 `f535e60e…` == manifest writer pin.
- Frozen byte check (worktree vs `d1681696`): `heldout-gen-v4.py`, `sqfs-triage-v4.py`, `indep-eval-v4.py`, `fixtures.json`, `gen-squashfs.py` all SAME.
- Stop receipt present: `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` (146,982 B).
- Lane state: HEAD is `1ed29de` (round-43 draft commits `d22686e1`, `1ed29de2` sit atop stated base `6b9e64fe`, which is an ancestor — expected, claims doc records the draft). `tools/round-43/` and `corpus/evidence/round-43/` do not exist yet (both created post-freeze by port + data run).

## 7. Port notes / risks for the L1 (P43-C1 data-run design)
1. **Manifest-write ordering vs refusal.** r42 `build_set` writes `manifest.json` *before* `--run` (main() 3374→3379). QUALITY 85 requires refusal with *no manifest write*, so the port must defer manifest finalization until after the REA loop. But the **counter regenerates with only `--seed --out` (no `--run`) and requires a manifest** (c2-counter.py:1250-1258 raises `generator_wrote_no_manifest` / `generator_failed` otherwise). ⇒ The port must still emit a manifest in no-run mode; the natural split is: no-run → factor-predicted manifest (carriers + declared_features as today), `--run` → re-open/finalize with `tuple_check` after verifying every observed tuple, exit 3 `declared_tuple_unobserved` with nothing written on mismatch. Whether `tuple_check` appears only in `--run` manifests (then no-run manifests must still parse for the counter) is a freeze-time spec detail to pin down in the port's docstring.
2. **`--verify` regen_check byte-compares manifest.json** (lines 3070-3073) but never re-runs REA. If `tuple_check` is REA-derived inside the manifest, a naive byte-compare fails. Options: exclude `tuple_check` from the compare, or make `--verify`'s regen pass re-run the tuple check rather than byte-comparing it. Flag for the controls seat (CTL-C1-3 also re-scores r42 shortcut controls through the new counter).
3. **Extraction path for the tuple check.** `run.json.handlers` = chunk handlers only; the counter's `observed_features` unions `extraction_gaps[].handler` too (c2-counter.py:592-617). On r42 data the two agree (verified 78/78 identical), but the claim text says "extracts the observed six-field feature tuple from each envelope" — the port should extract from `envelope.json` with the counter's extraction (gap-handler union), not from run.json's summary, and keep `run.json` as a receipt.
4. **C02-shape availability is probabilistic.** In the r42 draw only **1/24** combos (C02) produced the exact observed triple `{depth-limited, extractor-failure, unpublished-entry}` (three combos carried `depth-limited`+`extractor-failure`: C02, C11, C22). The claim requires "C02's round-42 shape must appear among the new seed's combos, with the manifest declaring what was observed, including `depth-limited`." A fresh seed draw may not produce that shape; if the claim demands it verbatim, the port either forces one such combo (deterministic, e.g. fixed factors for a designated combo slot) or the claim text gets amended before freeze. [INFERENCE] — flagged for the L1, not resolved here.
5. **Envelopes bake absolute paths.** `envelope.subject.local_path` and `parameters.path` record the absolute lane path `…/kaidoku-shokunin/corpus/evidence/round-42/c2/heldout/…`, and `parameters.output_directory` the r42 scratch (`/fast/scratch/hyaku/kaidoku-r42/l1-data/gen/r42-heldout-*/rea-*/out`). The r42 data run was executed **from the real lane root** (carrier path resolved relative to `--out`); the r43 L1 data run must likewise run with cwd = lane root and `--out corpus/evidence/round-43/c1/heldout` so the committed envelope paths name the committed location, and `--scratch` under `/fast/scratch/hyaku/kaidoku-r43/`. Envelope/run.json bytes are not determinism-bound (regen_check compares carriers + tree.json + manifest only), so scratch-path entropy is benign but path-shape consistency should be preserved.

## 8. What the r43 data run must reproduce (checklist for the L1 mirror)

- Same class table: 27 named classes × 2 + 24 combos, n = 78; same `classes` list; same `rea.per_class` max_depth map (1 for `depth-limited-*`, `failure-depth-limited`, `container-depth-limited`, `combo` → per-factor; else 3; `out-of-domain` → ood op, no max_depth).
- Same file layout per dir: `carrier.sqsh, tree.json, envelope.json, rea-full.json, run.json`; `manifest.json` at top. Same arm semantics (`before` ⇒ PATH stripped of `~/.local/bin`, `REA_UNBLOB_COMMAND` absolute; `home_bin_on_path` recorded).
- `manifest.json` new/changed fields: `seed` = r43 freeze hash, `round: 43`, `claim: R43-C1` (or the claim's own tag), `generator.name/sha256/version` = the new script, `generator.tuple_check` new block; `precedence_observations`, `combo_unseen.named_tuple_union_{size,sha256}`, `declared_outside*` all seed-derived re-computed; `declared_features` tuples measured-verified.
- run.json mirror: field list in §3, same value provenance; the only non-deterministic field is `duration`.
- Fixtures: r43 carriers embed the same 14 pinned unblob 26.6.4 MIT fixtures (all pinned sha256 verified, §5); S135 backs the license basis.
- Dev-arm equivalent: r43 needs its own dry-run dev set before freeze (QUALITY 84); r42 dev arm is frozen evidence, not regenerated.

Verification exercised: directory census, sha256 of all 14 fixtures vs pins, sha256 of all 78 carriers vs manifest, subject-digest bind on all 78 envelopes, declared-vs-observed tuple audit on all 78, envelope-extraction vs run.json summary agreement on all 78, byte-identity of five frozen files at `d1681696`, `disk-guard.sh status`, `git log/ls-tree/rev-parse` reads only. No REA/unblob/sasquatch executed; no VCS mutation; nothing written outside this report and `artifacts/R43ScoutFix/`. No tools installed (none needed).

Confidence: high on layout/provenance/pins/disk; the §7 items are the remaining open design points for the port seats.
