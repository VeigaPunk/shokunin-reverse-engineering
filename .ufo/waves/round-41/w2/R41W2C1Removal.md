# R41W2C1Removal — attack on the removal disposition (gap-rule.json `removed`, P41-C1)

**Verdict: CONFIRMED.** I attacked the C1 removal disposition on sandbox receipts for V4 and L3. All six mandated mutations (a)–(f), plus two bonus mutations (g)/(h), are refused by the frozen counter (with its REA rerun projection); the only accepted disposition is the genuine one (baseline 4/4, exit 0). No falsification found: the counter's removal checks behave exactly as the claim describes.

## What I attacked

The `removed` block of `.ufo/waves/round-41/c1/gap-rule.json`:

```json
"removed": { "diagnostic": "MaliciousSymlinkRemoved", "kinds": ["symlink"],
             "disposition": "exclusive", "silent": {} }
```

Question: can a receipt whose removal disposition is manipulated (a) remove a symlink that also has a gap, (b) remove a regular-file path, (c) remove a directory, (d) drop one removal, (e) add a removal for a non-existent row, (f) swap which 4 links are removed while keeping the count — pass the frozen counter? Score each with the counter at a sandbox revision that contains only the receipt mutation, rerun projection enabled.

## Method

- Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; base receipt revision `e9a24d07256d1606f01aa4d2d65f74e649c5f3d4` (the measured revision, `c1-at-e9a24d07.json` baseline reproduced 4/4, `met_target` true, exit 0).
- Per mutation: fresh sandbox clone `D=$(mktemp -d "$S/fx.XXXX") && git clone -q --shared <LANE> "$D/lane"`, `git -C "$D/lane" checkout -q e9a24d07…`, asserted `git rev-parse --show-toplevel == "$D/lane"`, mutated only `corpus/evidence/round-41/c1/<CAR>/after.json`, committed with `-c user.name=fx -c user.email=fx@fx`, then ran:

```
python3 -I -B <LANE>/tools/round-41/c1-counter.py --root "$D/lane" --rev <HEAD> \
  --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --carrier-cache "$S/cache" --json-out "$S/out/<CAR>-<ATT>.json"
```

- Vendor bytes for V3/V4 rebuilt into `$S/cache` by `tools/round-41/fetch-vendor.py --root <LANE> --rev d764389e… --cache "$S/cache"` (exit 0; V3 pin `c4f74f54…`, V4 pin `ce27ebca…`, nested `filesystem_core.squashfs` sha256 `4d5de25c…` — vendor bytes not committed, hashes only).
- Environment: `cd "$S"`, `TMPDIR="$S"`, `HYAKU_SCRATCH=/fast/scratch/hyaku`; REA 6.5.0 via `npx -y`, unblob 26.6.4 at `~/.local/bin/unblob` (default), sasquatch-v4be 4.5.1. No tools installed (channel/reason: none — everything pre-existing; nothing new to record).

## Results (score JSONs in `artifacts/R41W2C1Removal/`)

Baseline (genuine disposition, unmutated, revision e9a24d07): `carriers_matched 4`, `met_target true`, exit 0. V4 note: `612 gaps (1 structural), 4 removals, 0 silent, on 1017 non-regular entries`; L3: `4 gaps (1 structural), 0 removals`.

| # | Carrier | Mutation (on the committed receipt) | sandbox head | gaps_ok | disposition note (c1-counter.py) | proj_ok | proj_diff | matched | exit |
|---|---|---|---|---|---|---|---|---|---|---|
| a | V4 | add `MaliciousSymlinkRemoved` for gapped symlink `bin/ash` (gap kept) | de0ba05d | FALSE | `entry 'bin/ash' is both gapped and removed` (:1116-1117) | FALSE | diagnostics | 3 | 1 |
| b | V4 | add removal for regular file `bin/aicmd` | 3532d2ea | FALSE | `removal resolves to 0 non-regular entries at 'bin/aicmd'` (:1109-1111) | FALSE | diagnostics | 3 | 1 |
| c | V4 | add removal for directory `bin` | 417cd1e7 | FALSE | `removal at 'bin' names a 'dir' entry; removed.kinds is ['symlink']` (:1113-1115) | FALSE | diagnostics | 3 | 1 |
| d | V4 | drop removal `usr/www/avme/cgi-bin/system_status` | cf099d60 | FALSE | `required entry with no disposition … on ['usr/www/avme/cgi-bin/system_status']` (:1134-1136) | FALSE | diagnostics | 3 | 1 |
| e | V4 | add removal for non-existent row `nonexistent/deep/path` | ae17551c | FALSE | `removal resolves to 0 non-regular entries at 'nonexistent/deep/path'` | FALSE | diagnostics | 3 | 1 |
| f | V4 | swap the 4 removals onto `bin/ash, bin/base64, bin/cat, bin/chgrp`; the old 4 gain gaps (count kept, internally consistent) | c3f65080 | TRUE | `612 gaps (1 structural), 4 removals, 0 silent` | **FALSE** | `extraction_gaps, unpublished_entries, diagnostics` | 3 | 1 |
| g | V4 | rename diagnostic typename `MaliciousSymlinkRemoved` → `NotARemoval` | df1b9b07 | FALSE | `required entry with no disposition … on ['lib/libbroadbandcfg.so']` | FALSE | diagnostics | 3 | 1 |
| h | V4 | duplicate one removal diagnostic (same target twice) | cf0c2a5b | TRUE | `612 gaps (1 structural), 5 removals` (duplicate tolerated) | **FALSE** | diagnostics | 3 | 1 |
| a | L3 | add removal for gapped symlink `bin/busy` | c2553c7d | FALSE | `entry 'bin/busy' is both gapped and removed` | FALSE | diagnostics | 3 | 1 |
| b | L3 | add removal for regular file `etc/conf` | 8d4090f8 | FALSE | `removal resolves to 0 non-regular entries at 'etc/conf'` | FALSE | diagnostics | 3 | 1 |
| c | L3 | add removal for directory `bin` | ee38f0d7 | FALSE | `removal at 'bin' names a 'dir' entry; removed.kinds is ['symlink']` | FALSE | diagnostics | 3 | 1 |
| e | L3 | add removal for non-existent row | e14d825f | FALSE | `removal resolves to 0 non-regular entries at 'nonexistent/deep/path'` | FALSE | diagnostics | 3 | 1 |

In every refused run the other three carriers stay `matched=true`, so the refusal is isolated to the mutated carrier. Mutated receipt sha256s are recorded in the run transcript and the artifacts' `mutate.py`; every score JSON includes the full per-carrier detail.

## Disposition code read (c1-counter.py, frozen)

- `disposition_check` (lines 1040-1141). Removal family: typename gate `diagnostic_typename(d) != removal_name → skip` (:1101-1103); path resolution `diagnostic_rel(d, root)` and exact match to exactly one non-regular row (:1104-1111); kind gate `entry_kind not in removal_kinds` → refuse (:1112-1115); exclusivity `gapped.get(hits[0])` → refuse "both gapped and removed" (:1116-1117). Required-disposition loop: every `required` entry must carry a gap, a removal, or a silent admission; else "required entry with no disposition" (:1121-1136).
- Model validation: `gap_rule_model` parses `removed` and rejects a non-`"exclusive"` disposition (:547-580).
- Wiring: per-carrier `d['gaps_ok']` from `disposition_check` (:1634-1637); `matched` requires all `CLAUSES` including `gaps_ok` and `projection_ok` (:321-326, 1674-1676).
- Rerun projection: `make_real_runner` replays `--max-depth 1` etc. (:1418-1463); a diagnostic projects as `[typename, path-relative-to-root]` (:1328-1343); `projection_diff` compares `extraction_gaps`, `unpublished_entries`, `diagnostics` etc. (:1383-1398).

## Findings

1. **Every mandated mutation is refused.** (a) exclusivity, (b)/(e) exact-row resolution, (c) kind gate, (d) required-disposition completeness — each refuses at the disposition check itself (and additionally at the projection). No falsification of the removal disposition.
2. **Case (f) is the load-bearing one:** a fully consistent swap (4 removals relocated, gaps rebalanced, count kept) *passes the disposition check* (`gaps_ok=true`) and is refused **only** by the rerun projection (`projection_ok=false`, diff on `extraction_gaps/unpublished_entries/diagnostics`). The claim's removal-path binding is enforced at projection level, not disposition level — consistent with `R41C1DevCore 7.3` and the disclosed "rerun projection carries removal paths".
3. **Duplicate-removal tolerance (bonus h):** the disposition model counts but does not cap removals per entry (a duplicated diagnostic for the same link passes `disposition_check`, `5 removals`), and the projection is what refuses the duplicate. Minor robustness observation, not a claim violation: the rule admits "each symlink row exactly once … one diagnostic", and the projection binding enforces it in practice.
4. **Genuine disposition passes:** baseline 4/4 at e9a24d07 (and every untouched carrier stays matched in every run).
5. **Disclosed boundary (not a defect):** because unblob's symlink-removal set is iteration-order-dependent (claim §Disclosed limits), the projection binding is per-machine; a genuine receipt produced on another host could be refused here if its removal set differs. The claim already discloses this.

## Conclusion

Expected outcome confirmed: every manipulated removal disposition is refused; only the genuine disposition is accepted. No counterexample found. The `removed` block is implemented and enforced as claimed in P41-C1.
