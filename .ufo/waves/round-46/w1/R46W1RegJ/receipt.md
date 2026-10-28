# R46W1RegJ receipts

Lane `kaidoku`, round 46, wave 1, seat `R46W1RegJ` (registry rows, tag `reg-j`).

Rev ladder used, because the lane tip moved three times while this seat ran:

- `3182047…` — the freeze this seat was given.
- `87578656…` — HEAD when the first measurements were taken.
- `50862e4a…` — the freeze every control receipt cites; last commit before the first repair.
- `0425224…` — the post-repair bytes (F3/F4 commits); the freeze under which both counters now score green.
- `49e6cac4…` — HEAD when the final measurements were taken.

Instrument bytes were copied out of a rev with `git show <rev>:<path>` into scratch and executed from there; no original was mutated. sha256 of the copies run:

| path | sha256 |
|---|---|
| tools/round-41/local-source-gate.py | cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7 |
| tools/round-42/sqfs3-oracle.py | 9e03f9349db21c6a92a82ba96321401746df6fc7deb47fc739d1d99311547bdb |
| tools/round-46/census.py | 960c516d3b5cb1bb0306bf7f44f848a76b9c795c5319328954b5021b234c1fd5 |
| tools/round-46/registry.py @3182047 | 307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449 |
| tools/round-46/gate.py @3182047 | 64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e |
| tools/round-46/registry.py @50862e4a | db5adc02b64a4ad481211857c4263cff38d18935befad0956838619a6e50c38c |
| tools/round-46/gate.py @50862e4a | 847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223 |
| tools/round-46/attest.py @50862e4a | eba599582bb32eab3c47d7c15cbd53852e257070ae756136e3cee059e37311fd |
| tools/round-46/registry.py @0425224 | 5e16e4af69ebf714f0ee48b5a714aa682592f0ce5e32cdeec699b963d3f2da73 |
| tools/round-46/gate.py @0425224 | 847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223 |
| tools/round-46/attest.py @0425224 | e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346 |

Environment for every run: `TMPDIR=/fast/scratch/hyaku/kaidoku-r46/R46W1RegJ`, `HYAKU_SCRATCH` the same, cwd the same, `python3 -I -B`. Nothing was written under `/tmp`.

| # | command | exit | stdout sha256 | UTC | establishes |
|---|---|---|---|---|---|
| 1 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-41/local-source-gate.py --selftest` | 0 | `f93c7ae0fb5f5b17b300c258015cb7fc29743c72b0ccd22f661d2db5b7fa6fb6` | 2026-10-28T16:59:22Z | row1: selftest exists, 23/23 |
| 2 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-41/local-source-gate.py --root /nonexistent-xyz` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:59:24Z | row1: exit 2 on bad root |
| 3 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-41/local-source-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 31820472784284727546808acc31b3ea1e73919b` | 0 | `3038094749ef54bde1e57262b592bebe5360e32e617d01666318defdd9134603` | 2026-10-28T16:59:24Z | row1: exit 0, every out-of-lane row resolved |
| 4 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-41/local-source-gate.py --root /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fx1` | 1 | `ac35c10c28abc97e130c2a0b5093e4f2369133001e3eeb4e640dd3e2b52dc7c3` | 2026-10-28T16:59:24Z | row1: exit 1 on an unresolved row |
| 5 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-42/sqfs3-oracle.py --selftest --work /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/st-fresh` | 0 | `79b2b8e7f84ced512efd9b8f992b1d79d2564d36a8f019e1ffb936ccf673789a` | 2026-10-28T16:59:53Z | row2: selftest in a fresh --work, exit 0 |
| 6 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-42/sqfs3-oracle.py --work /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/st4 /nonexistent-xyz.img` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:59:24Z | row2: exit 2 unreadable |
| 7 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-42/sqfs3-oracle.py --dev-allow-v4 --work /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/t3/w2 --out /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/t3/o2 /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/t3/img.sqfs` | 3 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:59:25Z | row2: exit 3 path_not_representable |
| 8 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-42/sqfs3-oracle.py --selftest --work /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/st2` | 1 | `d58a4eae54a2dfb01466ef9b954a345c680fcf01976ab865ca3fa01449c2677c` | 2026-10-28T16:59:24Z | row2: selftest exists, 0 failure(s) |
| 9 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-46/census.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 31820472784284727546808acc31b3ea1e73919b --out /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/c5/census.json` | 0 | `0107c47c7f574e657390b157d3eb58aa360241899a98a20ccbe4aa5d5fdb838e` | 2026-10-28T16:59:53Z | row3: exit 0, census re-derived at the freeze |
| 10 | `sha256(produced)==sha256(committed census.json at freeze)` | 0 | `573ec008fc3f9173da04589c013484485758e9cf1c901a254bf1d6286d62133e` | 2026-10-28T16:59:53Z | byte-identical: True (sha 573ec008fc3f9173da04589c013484485758e9cf1c901a254bf1d6286d62133e) |
| 11 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-46/census.py` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:59:25Z | row3: exit 2 usage |
| 12 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-46/census.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --selftest` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:59:25Z | row3: no selftest flag |
| 13 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-46/census.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 31820472784284727546808acc31b3ea1e73919b --out /nonexistent-dir-xyz/out.json` | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:59:25Z | row3: exit 1 unhandled traceback |
| 14 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-46/registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 31820472784284727546808acc31b3ea1e73919b --rev 31820472784284727546808acc31b3ea1e73919b --no-battery` | 1 | `d89e522fc10b4cc87f71b096f47ff25de52d7c2d071e7e75600172695505d95d` | 2026-10-28T16:59:25Z | pre-landing 38 unregistered |
| 15 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fz/tools/round-46/registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 31820472784284727546808acc31b3ea1e73919b --rev 8757865679e62dac1f50efb33f583de0be884bf3 --no-battery` | 2 | `6f1a2dc360043c9d70aeb949339bdd6c544affea37b85e1aaa8aeeb360ed8caf` | 2026-10-28T16:59:25Z | FREEZE FINDING exit 2 frozen_path_changed |
| 16 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 50862e4a041499dd2ce0da68d10301b765bb9997 --rev 8757865679e62dac1f50efb33f583de0be884bf3 --no-battery` | 1 | `d48b2c3fee93b28df9687d972532c114c144074f4429ebea57a9fbb90886e79c` | 2026-10-28T16:59:25Z | authoritative freeze clean range |
| 17 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 50862e4a041499dd2ce0da68d10301b765bb9997 --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390 --no-battery` | 2 | `83f896bdbc5c03eddc70ec9a62f4baf696aeadf5ee157fc1a752563b674806bb` | 2026-10-28T17:02:13Z | declared freeze vs moved tip: exit 2 frozen_path_changed |
| 18 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 0425224756791b414454df28a9abf93dcdf154ce --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390 --no-battery` | 0 | `0cae44185193cd0384c983445f1a4ffb3e2b70a8c94565a9e3ca05cdbdae0e84` | 2026-10-28T17:02:13Z | structural clauses green; clause 6 not run (--no-battery) |
| 19 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzA/tools/round-46/registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 0425224756791b414454df28a9abf93dcdf154ce --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390` | 0 | `67b4dac13f00b0a7f77292f31146155143c7c3527cb4762fc77f2b8a21411665` | 2026-10-28T17:02:14Z | post-F4 bytes: full battery at freeze=0425224 |
| 20 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzA/tools/round-46/registry.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 50862e4a041499dd2ce0da68d10301b765bb9997 --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390 --no-battery` | 2 | `83f896bdbc5c03eddc70ec9a62f4baf696aeadf5ee157fc1a752563b674806bb` | 2026-10-28T17:02:15Z | post-F4 bytes still refuse the older freeze |
| 21 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/attest.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 50862e4a041499dd2ce0da68d10301b765bb9997 --rev 8757865679e62dac1f50efb33f583de0be884bf3` | 2 | `a8067ef63f99d1d7c44424502fc188a64bdfe9df90cdadbc3f96098241496e7f` | 2026-10-28T16:59:26Z | observation NameError REF |
| 22 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzA/tools/round-46/attest.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze 0425224756791b414454df28a9abf93dcdf154ce --rev 49e6cac4f6604986b1a7e9cfcbd9d46704dff390` | 0 | `4fca83c63d4b3ca64d70be6ea95c777d3823c88264906d769d7b8e148c78e0b2` | 2026-10-28T17:02:41Z | C1 at the moved tip, post-F3 attest bytes |
| 23 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fxreg --freeze 329440dcca73a1a95251dc37c90d920a2693d3bf --rev 329440dcca73a1a95251dc37c90d920a2693d3bf --no-battery` | 0 | `d9f58c686aa4715a35dd7b2cbe389c257672771ff4e1afb3578cb611e6a697f2` | 2026-10-28T16:59:26Z | rows register, structural clauses |
| 24 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fxreg --freeze 329440dcca73a1a95251dc37c90d920a2693d3bf --rev 329440dcca73a1a95251dc37c90d920a2693d3bf` | 1 | `0260235922a2e7dda107bc0c2b633155c30da3eb445e8eabf6526c74e32313aa` | 2026-10-28T16:59:26Z | clause 6 battery, v1_green measured |
| 25 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fxclean38 --freeze 9d0382f984039ea661d4286dd6c7c0ca4a86b0ac --rev 9d0382f984039ea661d4286dd6c7c0ca4a86b0ac --no-battery` | 0 | `9e754ba60563de747c9d8d70298f000d16df3b7f5881c6534e8b172faec45a89` | 2026-10-28T16:59:27Z | rows register, structural clauses |
| 26 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fxclean38 --freeze 9d0382f984039ea661d4286dd6c7c0ca4a86b0ac --rev 9d0382f984039ea661d4286dd6c7c0ca4a86b0ac` | 1 | `1b41b313809f23f9931e5be744d9de311b9aaeb255e4cf9eceebb6ce0dbe6992` | 2026-10-28T16:59:27Z | clause 6 battery, v1_green measured |
| 27 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fxhouse --freeze 5a1eef7d95da3bc84812c69d56d2cdddf0f7d21d --rev 5a1eef7d95da3bc84812c69d56d2cdddf0f7d21d --no-battery` | 0 | `224c881c546e7f2915f7542d1630996968bd434f342bc72627fee9b2bdf0220f` | 2026-10-28T16:59:30Z | rows register, structural clauses |
| 28 | `python3 -I -B /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fzG/tools/round-46/registry.py --root /fast/scratch/hyaku/kaidoku-r46/R46W1RegJ/fxhouse --freeze 5a1eef7d95da3bc84812c69d56d2cdddf0f7d21d --rev 5a1eef7d95da3bc84812c69d56d2cdddf0f7d21d` | 1 | `1e08966c735f55dfa02541a052825033884c28a3b7cdfbd9bf0ddbb5acf5c346` | 2026-10-28T16:59:30Z | clause 6 battery, v1_green measured |

Raw stdout and stderr per run: `receipts/<name>.log`; machine table `receipts/runs.json`.

Three receipts record a failure on purpose:

- `r2-selftest` (exit 1) reused a `--work` directory and crashed in `os.symlink` (`FileExistsError`); `r2-selftest-freshwork` is the same command on a fresh `--work` and exits 0 with `0 failure(s)`.
- `r3-badout` (exit 1) is `--out` into a missing parent directory; the frozen `census.py` does not create it. `r3-freeze-run` is the same command with the parent created (exit 0).
- `attest-freezeG-revHEAD` (exit 2) is the post-freeze `attest.py` before its repair: `unhandled NameError: name 'REF' is not defined`. `attestA-freezeA-revHEAD` is the repaired instrument at the moved freeze, exit 0.
