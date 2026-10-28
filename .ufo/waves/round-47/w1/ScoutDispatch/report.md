# ScoutDispatch measurements

Same findings as `../ScoutDispatch.md`. This file is the measurement table. Interpreter: `tools/round-47/record.py` at `1e2c3102952dc636650095643c1963c833859019` (clean worktree; seats arithmetic unchanged since freeze `5017e1f`). Counter reads `git show <rev>:`, not the worktree. No installs. Scratch removed after fixture copy.

## Counter

| measurement | command | exit | stdout sha256 | utc |
|---|---|---|---|---|
| seats at freeze: claimed (40, 32), derived (40, 36); `met_target` false; also window `<tip>`, coverage 133/133 vs 138/138, depth 20/20 vs 23/23 | `python3 -I -B tools/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 5017e1f7299c3a812e87e7950148f54313dd279e --no-battery --json-out .ufo/waves/round-47/w1/ScoutDispatch/receipts/record-at-freeze.json` | 1 | `10aa1a346f7585b863b583ff8d3a972b9744d251a6e319ed8c4a726ce07df6cf` (reconstructed: json-out file minus the newline `gate.emit` adds; file sha `7c93ef7e37dab44c5c29ae0cf99c58df97c34ef43074104f55138fae92897218`) | file mtime 2026-10-28T17:53:32Z |
| same interpreter at `HEAD`=`1e2c3102952dc636650095643c1963c833859019`: `failing []`, round-45 seats atom exempted, round-46 sum verified, `corrections 2` | `python3 -I -B tools/round-47/record.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD --no-battery --json-out .ufo/waves/round-47/w1/ScoutDispatch/receipts/record-at-HEAD.json` | 0 | `1cc15ca443f8821d02ece53a9bec71ba1118ae882d71c98d211d4ff156386704` (same reconstruction; file sha `b9f528cb821cd9f8b013a0f9218206038c58740dba4a900c7e309491098b0dae`) | file mtime 2026-10-28T17:54:25Z |
| spawn lie: `counts.spawn` 1, members 4, tasks 4, card `1 + 1 = 2`, battery `forgeries_green 0` | `python3 -I -B …/tools/round-47/record.py --root <fixture> --rev 285f5c1a88c6ddb6e408bd2659a6d1c301a9d4a8 --json-out <fixture>/receipts/spawn-lie.json` | 0 | `ffb8033a77a4ecb7fddda7c500d1eed909db0b707f63109ef16a7c1f793d9ee5` | 2026-10-28T17:54:24Z |
| gap: no `w2-dispatch.json` (`cat-file -e` exit 128), `w3` spawn 50 ignored, card `1 + 0 = 1` | same interpreter, fixture rev `8580cc4c1aac839551c0800b5f7a0a684c90ce03` | 0 | `c51cbe82b084666edb883a288bd578b97a531ee57bb4a7b8faf056a85a09ec54` | 2026-10-28T17:54:25Z |

Fixture copies: `fixtures/spawn-lie/`, `fixtures/gap/`.

## `wN-dispatch.json` (`counts.spawn`, and `registry.members` / `taskCall.tasks` lengths)

All `resume` 0 and `total` equal to spawn. Rounds 43–46 blobs identical at freeze and at `1e2c310`. `git cat-file -e` exit 0 tracked, 128 absent (stdout empty; sha not teed).

| path | spawn = members = tasks | results seats / len | results tracked at freeze | `wN.ready` at freeze | `wN.ready.dispatched` at freeze | worktree sha256 |
|---|---|---|---|---|---|---|
| `.ufo/waves/round-43/w1-dispatch.json` | 32 | 32 / 32 | 0 | 0 | 0 (32 keys) | `5c04fb8c27b6ee8ac1f71908e86597f01e7023e30785caa71bac18fb6b647cf5` |
| `.ufo/waves/round-43/w2-dispatch.json` | 32 | 32 / 32 | 0 | 0 | 0 (32 keys) | `dabbb0582c13c023f214534312566942154672078ea6910f5dc148a86fe5dde0` |
| `.ufo/waves/round-44/w1-dispatch.json` | 37 | 37 / 37 | 0 | 0 | 0 (37 keys) | `b6f9519967968860040d4252454ebb4d2efd644e73543e145f81889eb7a7b128` |
| `.ufo/waves/round-44/w2-dispatch.json` | 42 | 42 / 42 | 0 | 0 | 0 (42 keys) | `5fb17b94e9acc76aa3c0dec5ba2001664c65f81a65d38c08a40d2946748d30dd` |
| `.ufo/waves/round-45/w1-dispatch.json` | 40 | 40 / 40 (15 of 40 notes: never spawned) | 0 | 0 | **128** (body `1793201921.739129\n`, not a roster) | `fec3d2b055d0fcbbe94fcc1ab476efb00c23d3a01fe75397ce1869705b7b4087` |
| `.ufo/waves/round-45/w2-dispatch.json` | **36** | **36 / 36** | 0 | 0 | **128** (36 keys) | `0dfade1b643085d0a8d507a886b695a21adc107134e70c847f304e0b5e0da5a8` |
| `.ufo/waves/round-46/w1-dispatch.json` | 40 | 40 / 40 | **128** (still 128 at `1e2c310`) | 0 | 0 (40 keys) | `2e6693484d1509fc6a7418b0e69f77c459bb40978afdb88812de78ce82999697` |
| `.ufo/waves/round-46/w2-dispatch.json` | 40 | no results file | — | **128 absent** | **128 absent** | `b0d334a4e2504db5a3eb27e65fa382e31e79b782d6072b0c94b8350352a0c4ba` |
| `.ufo/waves/round-47/w1-dispatch.json` | 75 | none | **128** (0 at `1e2c310`) | **128** | absent | `9542c673d1101ee14c418ccef7f081418cec326b59018069b90724ce38222573` |

Round 46 `w2/` has one file, `swarm-registry.json` (40 members), and 0 `*.md`. The sum atom `40 + 40 = 80` is verified anyway.

Other `*-results.json` (tracked at freeze, not censuses): `round-43/w1/artifacts/R43C2Pin/anchor-pin-results.json`, `round-45/w1/R45W1CritC1/attacks-results.json`, `round-45/w1/R45W1CritC1/follow-results.json`, `round-45/w2/R45W2DoNothing/skip-results.json`.

No literal `.ready` / `.ready.dispatched`. Untracked adjacent: `round-47/w1.ready.partial` (48 keys). Not read by the counter.

## Not run

`record.py` on the dirty worktree card whose last headings are Round 46 and Round 47 (`record.sections` was executed; full counter was not). Lane counter runs did not pass the battery flag.
