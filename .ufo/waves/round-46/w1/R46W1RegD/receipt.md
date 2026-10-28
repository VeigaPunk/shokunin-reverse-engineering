# R46W1RegD — command receipt

Seat `R46W1RegD`, round 46 wave 1, tag `reg-d`.
Scratch root: `/fast/scratch/hyaku/kaidoku-r46/R46W1RegD` (removed after these receipts were copied).
Environment: Python 3.14.8, git 2.56.0, harness `run-probes.sh` (records UTC start/end, exit, stdout/stderr sha256).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze `31820472784284727546808acc31b3ea1e73919b`.

## Frozen bytes read (sha256 of `git show <freeze>:<path>`)

| path | sha256 |
|---|---|
| tools/round-41/c2-controls.py | e68a057e266e37195b59590e0ca7fbc409429d2a0ccfa125617c11b8c6b00ff4 |
| tools/round-42/c2-counter.py | f108916713b38d860acdd60d78dd1d1a541b9feccb1bd1979742dd8dd952cb59 |
| tools/round-44/c1-run.sh | c35d4b9bca6cd12e7ff1a89717da033841797dde5cf3f8bd3b262d3e9860b263 |
| tools/round-46/registry.py | 307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449 |
| tools/round-46/gate.py | 64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e |
| tools/round-46/attest.py | dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb |
| plans/round-46-claims.md | a09564e0a2e200c46f6c1fc56991813ad13c5b67f1b5e70721ab3ceee7afad01 |

Blob ids at the freeze: `tools/round-41/c2-controls.py` 0f123a87c06ec4380d0d7ea188e37dc419089047,
`tools/round-42/c2-counter.py` 391811037500d07dee351361c9dc69ade73d67c5, `tools/round-44/c1-run.sh`
479053ef814def55750db34deaf0ae62f9eb2440. All three are **identical at the freeze and at lane HEAD**
(`git rev-parse <rev>:<path>` compared; the row claims therefore describe the bytes that run today).
`plans/round-46-claims.md` blob f60fb631066297d7d6623b98ad055af93d0d743c at both revisions.

The frozen **directory** has moved since: `tools/round-46/registry.py` is blob 6581c1b2… at the freeze and
c95128c9… at HEAD; `gate.py` d7cd9aac… vs 9ab7e2a3…; `attest.py` 25883520… vs 936910fe… (see report F1).

## Probes

stdout sha256 `e3b0c442…b855` = empty stdout. `S` = `/fast/scratch/hyaku/kaidoku-r46/R46W1RegD`.

| # | UTC (start→end) | command (cwd lane root) | exit | stdout sha256 | stderr sha256 | observation |
|---|---|---|---|---|---|---|
| 1 | 16:58:07→16:58:08 | `python3 -I -B $S/frozen/c2-controls.py --help` | 0 | c47135949cb47ddfd00321470a373c5a91125839f6ced2f5f7bc017ac8bb77e5 | empty | options: --root --dev --out --json-out --build, `-h` |
| 2 | 16:58:08→16:58:08 | `python3 -I -B $S/frozen/c2-controls.py --bogus` | 2 | empty | 7cf00da23b332cb4911110b2d5945149fb80a6d40a56167c7f237204f422ec65 | argparse usage error |
| 3 | 16:58:08→16:58:08 | `python3 -I -B $S/frozen/c2-controls.py --selftest` | 2 | empty | 7cf00da23b332cb4911110b2d5945149fb80a6d40a56167c7f237204f422ec65 | **no selftest option exists**; error names the four required args |
| 4 | 16:58:08→16:58:08 | `python3 -I -B tools/round-41/c2-controls.py --root . --dev .ufo/waves/round-41/controls/c2/dev --out $S/ctl --json-out $S/ctl-a.json --build` | 0 | 13e69669d83d0e447bf967836372185bfc0ae44598ded9172e802d519febe941 | empty | `kill_rule_fires False`; receipt `$S/ctl-a.json` sha 739137e6… |
| 5 | 16:58:08→16:58:09 | `cp SKILL.md $S/ctl/CTL-C2-9-skill-copy.md && python3 -I -B tools/round-41/c2-controls.py --root . --dev .ufo/waves/round-41/controls/c2/dev --out $S/ctl --json-out $S/ctl-b.json` | 1 | 6f9ac7089c03faf641f47718989209ebad26552d3db5a28297d655677538681e | empty | `kill_rule_fires True`, `controls_at_full ['CTL-C2-9-skill-copy.md']`; receipt `$S/ctl-b.json` sha b6fb8949… |
| 6 | 16:58:09→16:58:09 | `python3 -I -B $S/frozen/c2-counter.py --help` | 0 | 491aae867c4de0e65c851d54b38215b1734d3850c75d726076fb3420cf722a4b | empty | options: --root --rev --freeze --json-out --selftest |
| 7 | 16:58:09→16:58:09 | `python3 -I -B $S/frozen/c2-counter.py --bogus` | 2 | empty | 6a96c2f56e8fadfb8f1133e25735274dc68ea1a0cce5016d7d90b0a86e6f2ba3 | argparse: unrecognized arguments |
| 8 | 16:58:09→16:58:09 | `python3 -I -B $S/frozen/c2-counter.py` | 2 | empty | 5b4ad767fd08477938e5708c21e02d2473caddfa73ebb98a45eba737e92994b8 | `usage: --root --rev --freeze required (or --selftest)` |
| 9 | 16:58:09→16:58:09 | `bash tools/round-44/c1-run.sh --help` | 0 | d0c9f37edd5e8434dff8d64a2b8dca63d14a7700a33c2499305df4fc70d9d26f | empty | wrapper execs c1-run.py; full argparse help printed |
| 10 | 16:58:09→16:58:09 | `bash tools/round-44/c1-run.sh --bogus` | 2 | empty | 20a477c4eba46322191cbcdf91a547f8c89c131d3adf687cee3d7c2729e4b16d | argparse via wrapper |
| 11 | 16:58:09→16:58:09 | `bash tools/round-44/c1-run.sh` | 2 | empty | bb1842d3b1f886264312f8db657ec7f38b0c6a777e8ef035a9bfad53a9c8f7c3 | guard: refuses committed evidence root without --data-run/KAIDOKU_C1_DATA_RUN=1 |
| 12 | 16:58:09→16:58:10 | `bash tools/round-44/c1-run.sh --dry-run` | 0 | c2aefcbcd18faa3a8579cc8c941d1b02b25f23f3d9abbdaf6b5d29002d7d3771 | empty | 22 lines of planned commands; no write |
| 13 | 16:58:10→16:58:10 | `bash $S/solo/c1-run.sh --dry-run` (frozen copy alone) | 2 | empty | d1171417f15347261ab0efc0c71de9becfd7a9a52a770c25951f347b34ee14b9 | `c1-run.py not found next to this script` → exit 2 |
| 14 | 16:58:10→16:58:11 | `bash tools/round-44/c1-run.sh --carrier v1le --evidence-root $S/ev --scratch $S --fake-rea /bin/false` | 1 | a8ffe39b18dd957062fd05c5ede5ca2d24c55280d3f80e660159c431a1b0af8a | e1ed9673ca97fa20a39d08c9f529e7a91abacde00211e9c8c88ed8be7f0dc80e | `# v1le: exit 1, receipt False` → one carrier failed, exit 1; wrote only `$S/ev` |
| 15 | 16:58:11→16:58:11 | `python3 -I -B $S/frozen46/registry.py --selftest` | 2 | empty | 39b32007f23adb6cd77580f85875a84b170c437aeaeecf85b74fe63389ac4009 | **claims' preflight command is unrunnable**: --root/--freeze/--rev are `required=True` |
| 16 | 16:58:11→16:58:12 | `python3 -I -B $S/frozen46/registry.py --root $S/fx --freeze HEAD --rev HEAD --selftest` | 0 | 0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e | empty | `REGISTRY_SELFTEST: cases=12 failures=0` (claims say cases=11) |
| 17 | 16:58:12→16:58:13 | `python3 -I -B $S/frozen46/attest.py --root $S/fx --freeze HEAD --rev HEAD --selftest` | 0 | ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb | empty | `ATTEST_SELFTEST: cases=15 failures=0` (matches claims) |
| 18 | 16:58:13→16:58:13 | `python3 -I -B $S/frozen46/registry.py --root $S/fx3 --freeze a02b5d37 --rev a02b5d37 --spec r46 --profile v2 --no-battery --json-out $S/fx3/.out/reg.json` | 1 | 9a494c2f8785bf25fd7e3d44bbc3df063f34b0a27c9342590b5b484a0691e556 | empty | real 38-path census: `registered` = my 3, `thin []`, `absent_at_rev []`, `unregistered` 35 (other seats), one failing clause |
| 19 | 16:58:13→16:58:14 | `python3 -I -B $S/frozen46/registry.py --root $S/fx --freeze a4e2bee8 --rev a4e2bee8 --spec r46 --profile v2 --json-out $S/fx/.out/reg-frozen3.json` | 1 | 780b3976a68af3560ffe71d92e206595f12715021f2dceae9aaf482538da0fbf | empty | 3-path census: `unregistered []`, `thin []`, `absent []`; battery `forgeries_total 7, v1_green 5, v2_green 0, genuine_green 1`; failing `battery v1_green 5 != 7` |
| 20 | 16:58:14→16:58:17 | `python3 -I -B $S/frozen46/registry.py --root $S/fx4 --freeze 92f7d77b --rev 92f7d77b --spec r46 --profile v2 --json-out $S/fx4/.out/reg.json` | 1 | 78787918a703149d067318a0ab287d556bb2d5580a0523526cf01c5a49cc0ab6 | empty | 38 **canonical** rows (frozen `house_row`), same battery values, failing `battery v1_green 5 != 7` |
| 21 | finished 16:54:24 | `python3 -I -B $S/frozen/c2-counter.py --selftest` (run before the harness; 123.3 s) | 0 | fef2f5cc74531cafaeb31c192e1262e4c37eaf7787f38992f7e7169572a48bac | e3b0c442…b855 (0 bytes) | `cases=79 green=18 red=61 pass=79 fail=0` |
| 22 | 16:59:01→16:59:01 | `h0=$(git status --porcelain | sha256sum); bash tools/round-44/c1-run.sh --dry-run; h1=$(git status --porcelain | sha256sum)` | 0 | d3838033741b3df145276f5869a76cbcae259ad90ef3c83bf12801eaf901da2e | empty | `before=after=c2d28487…7c4f`: dry-run wrote nothing into the lane |
| 23 | start 16:58:41 | `python3 -I -B` loading `$S/frozen46/gate.py`: `freeze_state(lane, 3182047…, "HEAD", plans/round-46-claims.md)` | 2 | 17fb1f8e49e8cd324575411e1f2fd0cdd3870a3f99c680aaf30826e5376d7935 | empty | `frozen_path_changed` = tools/round-46/ + attest.py + gate.py + registry.py; rev 17a72375 (same verdict measured at rev e3dfdbad) |
| 24 | 16:59:33→16:59:33 | `python3 -I -B $S/check_rows.py` (re-reads `rows.md`) | 0 | 0dbd46bb2d6ef15d032d46e6b540bca0be68d1bea40dfcd7dfd9137e2749c47f | empty | `rows 3 paths [3 correct] failures 0`; rows.md sha cf4c12bd… |

## Fixtures (each `git -C <dir> init -q`, toplevel asserted equal before the first commit)

| dir | commits | content |
|---|---|---|
| `$S/fx` | 3b02241 (fixture, real census) → a4e2bee (reg-d 3-path census) | frozen round-46 tree, claims, my 3 rows, reduced census = my 3 paths |
| `$S/fx3` | a02b5d3 | frozen round-46 tree, claims, my 3 rows, **real 38-path census** |
| `$S/fx4` | 92f7d77b | frozen tree + claims, **38 canonical `house_row` rows**, real census |

## Not run

- `c2-controls.py` exit 1 via a real (non-synthetic) control was not produced; the kill-rule path was exercised with a control that is a byte copy of `SKILL.md` (probe 5), which is the tool's own `full` condition.
- `c1-run.sh` exit 0 with a real carrier (REA `extract-firmware`) was not run: the data procedure is L1-only after the freeze. Exit 0 was exercised through `--dry-run` (probe 12).
- No installs were made (no tool added, no package changed).

## Raw receipts (copied here before the scratch root was removed)

Directory `w1/R46W1RegD/receipts/`:

| sha256 | file |
|---|---|
| 1ee87383e335c10b03108a366fa6a2fd922bde617220b142337df744178e3db0 | probes.tsv (the 20 harness records) |
| fef2f5cc74531cafaeb31c192e1262e4c37eaf7787f38992f7e7169572a48bac | selftest.out (c2-counter, cases=79) |
| 0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e | reg-frozen-selftest.out (cases=12) |
| ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb | att-selftest.out (cases=15) |
| 739137e66603a6d401466a850fd351514cae43115d1d6e4b80f4a436fa2dfeea | ctl-a.json (c2-controls, exit 0) |
| b6fb8949a2623fd7e49469ed3935a456724782bbf0d0052fb348d75c3832ec60 | ctl-b.json (c2-controls, exit 1) |
| 17fb1f8e49e8cd324575411e1f2fd0cdd3870a3f99c680aaf30826e5376d7935 | freeze-state.out (exit 2, frozen_path_changed) |
| 9a494c2f8785bf25fd7e3d44bbc3df063f34b0a27c9342590b5b484a0691e556 | fx3_.out_reg.json (real census, my 3 rows) |
| 780b3976a68af3560ffe71d92e206595f12715021f2dceae9aaf482538da0fbf | fx_.out_reg-frozen3.json (3-path census + battery) |
| 78787918a703149d067318a0ab287d556bb2d5580a0523526cf01c5a49cc0ab6 | fx4_.out_reg.json (38 canonical rows + battery) |
| 0dbd46bb2d6ef15d032d46e6b540bca0be68d1bea40dfcd7dfd9137e2749c47f | rows-check.out |

## Addendum (after raw-receipt copy)

| # | UTC | command | gate exit | stdout sha256 | observation |
|---|---|---|---|---|---|
| 25 | 17:01:00 | frozen `gate.freeze_state(lane, 3182047…, "HEAD", plans/round-46-claims.md)` at HEAD `04252247` | 2 (driver process 0; verdict is the JSON field) | 8d3b1e81ebc4b1b9844bcffcc9a48b6f6dd5ef9f8fcaf01cc96d9bb0090585d3 | `frozen_path_changed`: tools/round-46/ + attest.py + gate.py + registry.py; file `receipts/freeze-state-2.out` |
| 26 | 16:59:56 | `python3 -I -B tools/round-41/c2-controls.py --root $S/noskill --dev … --out $S/ctl --json-out $S/ctl-c.json` | 1 | empty | `FileNotFoundError` traceback: an uncaught crash exits 1 (row A's "or an uncaught crash") |
