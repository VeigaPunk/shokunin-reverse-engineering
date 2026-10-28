# R46W1RegK — receipts (round-46 C2 census, tag reg-k)

Commands actually run on 2026-10-28 UTC from scratch root `/fast/scratch/hyaku/kaidoku-r46/R46W1RegK` (removed before yield). `stdout sha256` and `stderr sha256` hash the exact streams of that run; an empty stream hashes to `e3b0c442...`. Frozen bytes were copied out with `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 31820472784284727546808acc31b3ea1e73919b:<path>` — the lane tree was only read.

| # | command (as run) | exit | stdout sha256 | stderr sha256 | UTC |
|---|---|---|---|---|---|
| 1 | `git -C "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" show "31820472784284727546808acc31b3ea1e73919b:tools/round-41/mk-l-carriers.py" > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py"` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 2 | `git -C "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" show "31820472784284727546808acc31b3ea1e73919b:tools/round-42/unblob-logtee.sh" > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh"` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 3 | `git -C "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" show "31820472784284727546808acc31b3ea1e73919b:tools/round-46/gate.py" > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/gate.py"` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 4 | `git -C "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" show "31820472784284727546808acc31b3ea1e73919b:tools/round-46/registry.py" > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/registry.py"` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 5 | `sha256sum "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/gate.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/registry.py"` | 0 | b0aa7c3ba3159decf64e39a96951922f025e7cf6e569c80b92d2aa1a3ad96437 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 6 | `git -C "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" rev-parse "31820472784284727546808acc31b3ea1e73919b"` | 0 | 9757eb4b209616da445117438ef0eca8989765d9b70c7f61764efe954dd925d7 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 7 | `git -C "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" log --format=%H -1 -- plans/round-46-claims.md` | 0 | 9757eb4b209616da445117438ef0eca8989765d9b70c7f61764efe954dd925d7 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 8 | `python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" --help` | 0 | 636702ba99790581afbc22649ec46168f43b143677e2c7a9975383d078e603f2 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:20Z |
| 9 | `python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py"` | 2 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | d08c7f03407fc1b92f0674fdb6ac415ee58a9cedeae86e2aa4dd3aadc1757b98 | 2026-10-28T17:01:21Z |
| 10 | `python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/no-such-out"` | 2 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | d4c99feba0a89927e93c502c927948079b40adc07278254405e24e3accba5c1a | 2026-10-28T17:01:21Z |
| 11 | `rm -rf "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p5" && mkdir -p "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p5" && : > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p5/keep" && python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p5" --lane "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"` | 2 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 066238443386c51366080c70cc444162ac0931245efed1b01d930fb433b0ae26 | 2026-10-28T17:01:21Z |
| 12 | `rm -rf "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p6" && mkdir -p "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p6" && python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p6" --writer /no/such/writer` | 2 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 1ba69f293ef864ce569eaeff1306a68e4a41b879ccb33bd783168f94ad79f2ab | 2026-10-28T17:01:21Z |
| 13 | `rm -rf "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7" && mkdir -p "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7" && python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7" --lane "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" --builds 2 --json "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7.json"` | 0 | 9f7db30665f029e1ef91f0927d13127e5d8109360d008ccb036fd5aa9f8c06d5 | fe72c76eb62f08ebe103534cf399ded7a8132856a26b13b8798e1e3f91f4c3fd | 2026-10-28T17:01:21Z |
| 14 | `printf 'import sys\nsys.exit(3)\n' > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w3.py" && chmod +x "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w3.py" && rm -rf "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p8" && mkdir -p "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p8" && python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p8" --writer "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w3.py"` | 3 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070 | 2026-10-28T17:01:21Z |
| 15 | `printf 'import os,sys\nopen(sys.argv[2],"wb").write(os.urandom(64))\n' > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w4.py" && chmod +x "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w4.py" && rm -rf "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p9" && mkdir -p "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p9" && python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p9" --writer "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w4.py" --builds 2` | 4 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 6c3048e3b4bfe25dd4c9ded67ac5787e42dbc55e24f0554b7965db8a393f2bfe | 2026-10-28T17:01:21Z |
| 16 | `printf 'import sys\nsys.exit(0)\n' > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w0.py" && chmod +x "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w0.py" && rm -rf "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p10" && mkdir -p "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p10" && python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p10" --writer "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/w0.py"` | 1 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 0b4af779b90a47b74c48cb7edf1621045c92c09fd99a01f0903814c6cf0697fd | 2026-10-28T17:01:21Z |
| 17 | `C1_REAL_UNBLOB=relative/path bash "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" --log "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p11.log"` | 2 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 047ea8574cb56520cbc83db0bb592228e23d8215f2a2d66a0ceee9bc3adc500e | 2026-10-28T17:01:21Z |
| 18 | `sha256sum "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/stub-unblob.sh"` | 0 | 1c679357d15c83326d6c066b3705142a98c267917e68b667894cb150f2ee2380 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:21Z |
| 19 | `C1_REAL_UNBLOB="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/stub-unblob.sh" C1_LOG_COPY="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12-copy.log" bash "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" -e "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/in.bin" --log "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12.log"` | 5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:21Z |
| 20 | `cat "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/logtee.argv"` | 0 | 08d86351c23456f706549dcbd250b6d8dc60c6288863e973ed1411ae34bfbff0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:21Z |
| 21 | `cat "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12-copy.log"` | 0 | f411172f3aeaf2c2c84ce0428de41b332d179ecd70397f47b34fa729a1085d80 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:21Z |
| 22 | `C1_REAL_UNBLOB="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/stub-unblob.sh" bash "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" --log "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p13.log"` | 5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:21Z |
| 23 | `ls "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12-copy.log"` | 0 | eb1ce1806699ef3ff966f739fbfb37ff76c477f8e6e75b1359ac0af04979828d | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:21Z |
| 24 | `printf '#!/bin/sh\nexit 0\n' > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/quiet-unblob.sh" && chmod +x "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/quiet-unblob.sh" && rm -f "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16-copy.log" && C1_REAL_UNBLOB="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/quiet-unblob.sh" C1_LOG_COPY="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16-copy.log" bash "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" --log "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16.log" && test ! -e "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16-copy.log"` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 25 | `C1_REAL_UNBLOB=/nonexistent/unblob bash "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" --log "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p15.log"` | 127 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 6059f41e5f47b84b85e0859d765982ee2d7e7ac5b06011695b546528e02f777b | 2026-10-28T17:01:22Z |
| 26 | `python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/gate.py"` | 1 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 27c2bd0fd69eba0c64275602e4c2c1e8f333807638e038cd6dac08419f4244e1 | 2026-10-28T17:01:22Z |
| 27 | `python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_freeze_state.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "31820472784284727546808acc31b3ea1e73919b" "31820472784284727546808acc31b3ea1e73919b"` | 0 | d7f973f8ff479e602fd3bc779b4d37161eb54fd496ebe6bda8ce0aaffdf0a42f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 28 | `python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_freeze_state.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "31820472784284727546808acc31b3ea1e73919b" deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` | 2 | 499093ceef254591344955fe08c93391bf939c62c64f11ce0c231cecc5f984af | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 29 | `python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_freeze_state.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "31820472784284727546808acc31b3ea1e73919b" 5382acc85f9d8617fe242fc116819b8055dfc4c7` | 2 | ca18a1157512d0211820e02e0f2c02e88b1b0999e7f1ba883181e7c0323fe67f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 30 | `python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_guards.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"` | 0 | c0dbf06eee043c88f53f0f715e9a1bba9470321ea566163255df2f8feed253f0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 31 | `HYAKU_SCRATCH=/tmp python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_guards.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"` | 0 | e581866e5c0f8c9b7599c27a47c902656e12c0cb0ff9033d6dbc10f64637c114 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 32 | `python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_mainguard.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz"` | 2 | 53c97a5e091456c251fbf0531a1b85c6a6a6a6b8ecd9a6c4c83788a7a2e14fb1 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 33 | `python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/registry.py" --selftest` | 2 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 39b32007f23adb6cd77580f85875a84b170c437aeaeecf85b74fe63389ac4009 | 2026-10-28T17:01:22Z |
| 34 | `python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/registry.py" --root "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" --freeze "31820472784284727546808acc31b3ea1e73919b" --rev "31820472784284727546808acc31b3ea1e73919b" --selftest > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/selftest.out" 2> "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/selftest.err"` | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 35 | `head -1 "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/selftest.out"` | 0 | 401ed7b33ffd5786d833217c85426b299f791aafb5b6dfab7fe302b7b727b8f3 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 36 | `sha256sum "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/selftest.out"` | 0 | f23bdd73d8538f03050b10e56dadf299cb69080bd74eeebadb6dbbfb3adfa662 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 37 | `python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_rows_shape.py" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1RegK/rows.md"` | 0 | 7cbcce69de89a3d51971aa0892416da0505ecd971226c530f2460c5d9aa10575 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |
| 38 | `python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_parse_rows.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1RegK/rows.md" "31820472784284727546808acc31b3ea1e73919b"` | 0 | b9363cb58452fad64d902531245d94a83b135a81d1c621d3c5bd5f64a6cbc94f | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2026-10-28T17:01:22Z |

Probe scripts (in scratch, hashed above where they are inputs): `probe_freeze_state.py`, `probe_guards.py`, `probe_mainguard.py`, `probe_rows_shape.py`, `probe_parse_rows.py`, `stub-unblob.sh`. `probe_parse_rows.py` scores `rows.md` with the frozen `registry.score` and a census replaced by exactly these three paths, so a red verdict there would be a format defect in my own rows.

No install was made for this seat; python3 3.14.0 and git were already present. Nothing under /tmp was written or cited.

## Observed output of the decisive probes

Each block replays the command string recorded in that receipt row verbatim;
the stdout sha256 is compared with the value recorded for the same row.

### probe 13 — exit 0

`rm -rf "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7" && mkdir -p "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7" && python3 -I -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/mk-l-carriers.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7" --lane "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" --builds 2 --json "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7.json"`

```
L3	xz	04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3	187892	13	3	20	/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7/L3/carrier.sqsh
L4	gzip	4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc	169545	14	3	17	/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p7/L4/carrier.sqsh
```

```
L3	build2-equal	sha256=04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3
L4	build2-equal	sha256=4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc
```

stdout sha256 `9f7db30665f029e1ef91f0927d13127e5d8109360d008ccb036fd5aa9f8c06d5` == recorded `9f7db30665f029e1ef91f0927d13127e5d8109360d008ccb036fd5aa9f8c06d5`
recorded exit 0, replay exit 0

### probe 20 — exit 0

`cat "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/logtee.argv"`

precondition reset: `C1_REAL_UNBLOB="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/stub-unblob.sh" C1_LOG_COPY="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12-copy.log" bash "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" -e "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/in.bin" --log "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12.log"` (exit 5, a precondition and not a verdict)

```
-e
/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/in.bin
--log
/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12.log
```

stdout sha256 `08d86351c23456f706549dcbd250b6d8dc60c6288863e973ed1411ae34bfbff0` == recorded `08d86351c23456f706549dcbd250b6d8dc60c6288863e973ed1411ae34bfbff0`
recorded exit 0, replay exit 0

### probe 21 — exit 0

`cat "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p12-copy.log"`

```
extractor: sasquatch -le
```

stdout sha256 `f411172f3aeaf2c2c84ce0428de41b332d179ecd70397f47b34fa729a1085d80` == recorded `f411172f3aeaf2c2c84ce0428de41b332d179ecd70397f47b34fa729a1085d80`
recorded exit 0, replay exit 0

### probe 24 — exit 0

`printf '#!/bin/sh\nexit 0\n' > "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/quiet-unblob.sh" && chmod +x "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/quiet-unblob.sh" && rm -f "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16-copy.log" && C1_REAL_UNBLOB="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/quiet-unblob.sh" C1_LOG_COPY="/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16-copy.log" bash "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz/unblob-logtee.sh" --log "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16.log" && test ! -e "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/p16-copy.log"`

```
(no stdout)
```

stdout sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` == recorded `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
recorded exit 0, replay exit 0

### probe 27 — exit 0

`python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_freeze_state.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "31820472784284727546808acc31b3ea1e73919b" "31820472784284727546808acc31b3ea1e73919b"`

```
exit 0
{"blob_changed": [], "frozen_derived": ["tools/round-46/", "plans/round-46-claims.md"], "frozen_path_changed": [], "restored": []}
```

stdout sha256 `d7f973f8ff479e602fd3bc779b4d37161eb54fd496ebe6bda8ce0aaffdf0a42f` == recorded `d7f973f8ff479e602fd3bc779b4d37161eb54fd496ebe6bda8ce0aaffdf0a42f`
recorded exit 0, replay exit 0

### probe 28 — exit 2

`python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_freeze_state.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "31820472784284727546808acc31b3ea1e73919b" deadbeefdeadbeefdeadbeefdeadbeefdeadbeef`

```
exit 2
{"reason": "unknown rev revision"}
```

stdout sha256 `499093ceef254591344955fe08c93391bf939c62c64f11ce0c231cecc5f984af` == recorded `499093ceef254591344955fe08c93391bf939c62c64f11ce0c231cecc5f984af`
recorded exit 2, replay exit 2

### probe 29 — exit 2

`python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_freeze_state.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "31820472784284727546808acc31b3ea1e73919b" 5382acc85f9d8617fe242fc116819b8055dfc4c7`

```
exit 2
{"reason": "freeze is not an ancestor of rev"}
```

stdout sha256 `ca18a1157512d0211820e02e0f2c02e88b1b0999e7f1ba883181e7c0323fe67f` == recorded `ca18a1157512d0211820e02e0f2c02e88b1b0999e7f1ba883181e7c0323fe67f`
recorded exit 2, replay exit 2

### probe 30 — exit 0

`python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_guards.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"`

```
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md -> (None, '--json-out inside a graded or frozen surface: SKILL.md')
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46/x.json -> (None, '--json-out inside a graded or frozen surface: tools/round-46/x.json')
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/ok.json -> ('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/ok.json', None)
/tmp/x.json -> (None, '--json-out outside the lane root: /tmp/x.json')
scratch -> ('/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe-kcsajuuv', None)
```

stdout sha256 `fc6f0cb7c5cd8aab9adccf7f04774d843f8bdff5f41690aae1f13b8143a16c89` == recorded `c0dbf06eee043c88f53f0f715e9a1bba9470321ea566163255df2f8feed253f0`
recorded exit 0, replay exit 0
note: the mkdtemp suffix in the scratch line is random, so this row's hash cannot repeat; the four out_path lines are compared literally and match

### probe 31 — exit 0

`HYAKU_SCRATCH=/tmp python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_guards.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"`

env: `HYAKU_SCRATCH=/tmp`

```
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md -> (None, '--json-out inside a graded or frozen surface: SKILL.md')
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46/x.json -> (None, '--json-out inside a graded or frozen surface: tools/round-46/x.json')
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/ok.json -> ('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/ok.json', None)
/tmp/x.json -> (None, '--json-out outside the lane root: /tmp/x.json')
scratch -> (None, 'scratch root is a temporary partition: /tmp')
```

stdout sha256 `e581866e5c0f8c9b7599c27a47c902656e12c0cb0ff9033d6dbc10f64637c114` == recorded `e581866e5c0f8c9b7599c27a47c902656e12c0cb0ff9033d6dbc10f64637c114`
recorded exit 0, replay exit 0

### probe 32 — exit 2

`python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_mainguard.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz"`

```
{"reason": "unhandled RuntimeError: boom"}
```

stdout sha256 `53c97a5e091456c251fbf0531a1b85c6a6a6a6b8ecd9a6c4c83788a7a2e14fb1` == recorded `53c97a5e091456c251fbf0531a1b85c6a6a6a6b8ecd9a6c4c83788a7a2e14fb1`
recorded exit 2, replay exit 2

### probe 35 — exit 0

`head -1 "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/selftest.out"`

```
REGISTRY_SELFTEST: cases=12 failures=0
```

stdout sha256 `401ed7b33ffd5786d833217c85426b299f791aafb5b6dfab7fe302b7b727b8f3` == recorded `401ed7b33ffd5786d833217c85426b299f791aafb5b6dfab7fe302b7b727b8f3`
recorded exit 0, replay exit 0

### probe 37 — exit 0

`python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_rows_shape.py" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1RegK/rows.md"`

```
1 cells=7 backticks=2 cell0=`tools/round-41/mk-l-carriers.py` exitmap=['0', '1', '2'] OK
2 cells=7 backticks=2 cell0=`tools/round-42/unblob-logtee.sh` exitmap=['0', '1', '2'] OK
3 cells=7 backticks=2 cell0=`tools/round-46/gate.py` exitmap=['0', '1', '2'] OK
shape OK
```

stdout sha256 `7cbcce69de89a3d51971aa0892416da0505ecd971226c530f2460c5d9aa10575` == recorded `7cbcce69de89a3d51971aa0892416da0505ecd971226c530f2460c5d9aa10575`
recorded exit 0, replay exit 0

### probe 38 — exit 0

`python3 -B "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/probe_parse_rows.py" "/fast/scratch/hyaku/kaidoku-r46/R46W1RegK/fz" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin" "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1/R46W1RegK/rows.md" "31820472784284727546808acc31b3ea1e73919b"`

```
exit 0
{
 "scope_size": 3,
 "registry_rows": 3,
 "registered": [
  "tools/round-41/mk-l-carriers.py",
  "tools/round-42/unblob-logtee.sh",
  "tools/round-46/gate.py"
 ],
 "unregistered": [],
 "thin": [],
 "absent_at_rev": [],
 "failing": []
}
```

stdout sha256 `b9363cb58452fad64d902531245d94a83b135a81d1c621d3c5bd5f64a6cbc94f` == recorded `b9363cb58452fad64d902531245d94a83b135a81d1c621d3c5bd5f64a6cbc94f`
recorded exit 0, replay exit 0

replay verdict: all hashes matched

