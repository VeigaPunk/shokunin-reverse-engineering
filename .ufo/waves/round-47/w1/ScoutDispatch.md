# ScoutDispatch — seats-atom ground truth (round 47)

Interpreter used for both counter runs: `tools/round-47/record.py` as committed at `1e2c3102952dc636650095643c1963c833859019` (worktree clean for that path; not the freeze blob). `dispatch_counts` / the seats `derive` arm are unchanged from freeze `5017e1f7299c3a812e87e7950148f54313dd279e` (`git diff --stat` is 21 insertions / 10 deletions, none of them in `dispatch_counts` or `SEATS_*`). The code reads `git show <rev>:path`, never the worktree. No packages installed.

Scratch `/fast/scratch/hyaku/kaidoku-r47/ScoutDispatch` was removed after the fixture files below were copied. Fixture repos were `git init`'d under that scratch; `rev-parse --show-toplevel` matched the fixture before any commit.

## What the seats clause actually counts

`record.dispatch_counts` walks `.ufo/waves/round-<N>/w1-dispatch.json`, `w2-dispatch.json`, … and stops at the first missing file. It appends `counts.spawn` only. It does not read `registry.members`, `taskCall.tasks`, `*-results.json`, `wN.ready`, or `wN.ready.dispatched`. There is no file literally named `.ready` or `.ready.dispatched` under rounds 43–47; the markers are `wN.ready` and `wN.ready.dispatched`.

Last two `## Round N` headings at the freeze and at `1e2c310` are **45 then 46** (counter `sections`). Round 44 has no `## Round 44` heading, so its dispatch files are not a seats atom. Headings `## Round 25` and `## Round 34` each occur twice; that does not change the last-two pair.

| atom at freeze and at `1e2c310` | regex | claimed | `counts.spawn` sequence | counter |
|---|---|---|---|---|
| Round 45 `Wave 1: 40 seats; wave 2: 32 seats` | `SEATS_PAIR` | (40, 32) | (40, 36) | mismatch at freeze; exempted at `1e2c310` by the correction below |
| Round 46 `Waves: 40 + 40 = 80 seats` | `SEATS_SUM` | (40, 40, 80) | (40, 40) sum 80 | verified at both revs |

The round-45 parenthetical says those numbers are "counts from `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`". Those files' `seats` fields are **40 and 36**, and `results` lengths are 40 and 36. The integer 32 is in neither the dispatch nor the results file.

Correction committed at `1e2c310` (`SCORECARD.md:3669-3671`), re-derived by the counter (`corrections_bad []`):

```
- corrects seats round-45: 2 waves, 76 seats total — `w1-dispatch.json` reports `counts.spawn 40`
  and `w2-dispatch.json` reports `counts.spawn 36`, so the round-45 cell's "wave 2: 32 seats"
  understates the dispatched wave by four.
```

`2 waves, 76 seats total` equals `(len(spawns), sum(spawns))` for round 45. The original sentence is still in the section; the counter exempts it.

## Counter exits (current interpreter)

| rev | exit | `met_target` | seats detail | json-out sha256 (file, includes trailing newline) | stdout sha256 reconstructed as file minus that newline (`gate.emit` prints the text, writes `text+"\n"`) | file mtime |
|---|---|---|---|---|---|---|
| `5017e1f7299c3a812e87e7950148f54313dd279e` | **1** | false | claimed [40, 32] derived [40, 36] dispatch [40, 36]; also window `<tip>`, coverage 133/133 vs 138/138, depth 20/20 vs 23/23; `corrections 0` | `7c93ef7e37dab44c5c29ae0cf99c58df97c34ef43074104f55138fae92897218` | `10aa1a346f7585b863b583ff8d3a972b9744d251a6e319ed8c4a726ce07df6cf` | 2026-10-28T17:53:32Z |
| `HEAD` → `1e2c3102952dc636650095643c1963c833859019` | **0** | true | round-45 seats atom exempted; round-46 sum verified; `corrections 2`, `corrections_bad []`, `failing []` | `b9f528cb821cd9f8b013a0f9218206038c58740dba4a900c7e309491098b0dae` | `1cc15ca443f8821d02ece53a9bec71ba1118ae882d71c98d211d4ff156386704` | 2026-10-28T17:54:25Z |

Commands (`--no-battery`; cwd irrelevant, paths absolute):

```sh
python3 -I -B tools/round-47/record.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 5017e1f7299c3a812e87e7950148f54313dd279e --no-battery \
  --json-out .ufo/waves/round-47/w1/ScoutDispatch/receipts/record-at-freeze.json

python3 -I -B tools/round-47/record.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev HEAD --no-battery \
  --json-out .ufo/waves/round-47/w1/ScoutDispatch/receipts/record-at-HEAD.json
```

`HEAD` moved during this scout. First `rev-parse` was `9018c53b16503c8d06d398b75503406508119946`. The HEAD run resolved `1e2c3102952dc636650095643c1963c833859019`. Commits `5017e1f..1e2c310`: `3186f69` (wave-1 dispatch), `9018c53` (A1), `e856beb` (land block 24 and the record corrections), `62e33f7` (A2), `2e4ae43` (A3 historical-correction carve-out), `1e2c310` (A4). Freeze is an ancestor of `1e2c310` (`merge-base --is-ancestor` exit 0). Rounds 43–46 `wN-dispatch.json` blobs are identical from the freeze to `1e2c310` (`git diff --stat 5017e1f 1e2c310 -- .ufo/waves/round-4[3-6]` shows no dispatch paths; the only wave diff is round-47 additions).

At the freeze the claims-file "before" narrative matches the files: wave 2 spawn is 36, not 32. At `1e2c310` C2 is already exit 0, because the correction and the axis-head edits are already committed. That is not a do-nothing tree.

## Dispatch inventory

`counts` on every file is `{"spawn": N, "resume": 0, "total": N}` with `N` below. `registry.members` and `taskCall.tasks` lengths equal `N` on every file (all member `kind` values are `spawn`). Worktree sha256 equals the freeze blob for rounds 43–46 (compared by `git cat-file -p` during the inventory; `git diff --stat` freeze..`1e2c310` does not touch them). Round 47's dispatch is **not** in the freeze.

`git cat-file -e <rev>:<path>` exit **0** = tracked, **128** = absent. Stdout of `cat-file -e` is empty; stderr on 128 is `fatal: path '…' exists on disk, but not in '<rev>'` or `fatal: path '…' does not exist in '<rev>'`. Stdout sha256 was not teed.

| path | spawn = members = tasks | results `seats` / `len` | results at freeze | `wN.ready` at freeze | `wN.ready.dispatched` at freeze | dispatch sha256 (worktree) |
|---|---|---|---|---|---|---|
| `round-43/w1-dispatch.json` | 32 | 32 / 32 | tracked | tracked | tracked, 32 keys | `5c04fb8c27b6ee8ac1f71908e86597f01e7023e30785caa71bac18fb6b647cf5` |
| `round-43/w2-dispatch.json` | 32 | 32 / 32 | tracked | tracked | tracked, 32 keys | `dabbb0582c13c023f214534312566942154672078ea6910f5dc148a86fe5dde0` |
| `round-44/w1-dispatch.json` | 37 | 37 / 37 | tracked | tracked | tracked, 37 keys | `b6f9519967968860040d4252454ebb4d2efd644e73543e145f81889eb7a7b128` |
| `round-44/w2-dispatch.json` | 42 | 42 / 42 | tracked | tracked | tracked, 42 keys | `5fb17b94e9acc76aa3c0dec5ba2001664c65f81a65d38c08a40d2946748d30dd` |
| `round-45/w1-dispatch.json` | 40 | 40 / 40 | tracked | tracked | **128 untracked**. Body is `1793201921.739129\n`, not a roster | `fec3d2b055d0fcbbe94fcc1ab476efb00c23d3a01fe75397ce1869705b7b4087` |
| `round-45/w2-dispatch.json` | **36** | **36 / 36** | tracked | tracked | **128 untracked**, 36 keys | `0dfade1b643085d0a8d507a886b695a21adc107134e70c847f304e0b5e0da5a8` |
| `round-46/w1-dispatch.json` | 40 | 40 / 40 | **128 untracked** (still 128 at `1e2c310`) | tracked | tracked, 40 keys | `2e6693484d1509fc6a7418b0e69f77c459bb40978afdb88812de78ce82999697` |
| `round-46/w2-dispatch.json` | 40 | no `r46-w2-results.json` | — | **128, file absent** (still absent at `1e2c310`) | **128, file absent** | `b0d334a4e2504db5a3eb27e65fa382e31e79b782d6072b0c94b8350352a0c4ba` |
| `round-47/w1-dispatch.json` | 75 | no results file | **128** (tracked at `1e2c310`, added in `3186f69`) | **128 untracked** | absent | `9542c673d1101ee14c418ccef7f081418cec326b59018069b90724ce38222573` |

Round 45 wave 1 results: 25 notes empty, **15** notes starting `never spawned: host job-cap refusal…`. The card's 40 and `counts.spawn` 40 count those 15. The counter cannot see the note.

Round 46 wave 2 is the live witness that "dispatched" is not checked. `w2/` contains only `swarm-registry.json` (40 members). No `w2.ready`, no `w2.ready.dispatched`, no results file, 0 `*.md`. `counts.spawn` is still 40, and `Waves: 40 + 40 = 80 seats` is **verified**, not mismatched.

Round 47 is one wave. Neither seats regex matches a single wave: `SEATS_SUM` needs `A + B = C`, `SEATS_PAIR` needs `Wave 1: A seats; wave 2: B seats`. `Waves: 75 + 0 = 75 seats` would match a one-element spawn list, because the sum shape uses `spawns[1] if len>1 else 0`. A sentence `Wave 1: 75 seats` would not be an atom. The dirty worktree section `## Round 47` (not at `1e2c310`) contains **no** seats sentence, so the 75 is unchecked. `record.sections` on the worktree card returns `['46','47']`. The round-45 correction then has key `45` outside `known_keys`, but the A3 carve-out treats `seats`/`window` keys that are digits `< oldest` of the last two (45 < 46) as historical and does **not** push `corrections_bad`. Full `record.py` on that uncommitted card: **not run** (the counter never reads the worktree card).

Other `*-results.json` files, not wave censuses, all tracked at the freeze: `round-43/w1/artifacts/R43C2Pin/anchor-pin-results.json`, `round-45/w1/R45W1CritC1/attacks-results.json`, `round-45/w1/R45W1CritC1/follow-results.json`, `round-45/w2/R45W2DoNothing/skip-results.json`. No `*-dispatch.json` other than the `wN-dispatch.json` rows above, so lexical order and the `w1,w2,…` walk coincide on this tree. No `w3-dispatch.json` in rounds 43–47, so the gap-stop is not triggered here.

Adjacent, not in the requested names: untracked `round-47/w1.ready.partial` (one JSON object, 48 keys). Not read by the counter.

`git cat-file -e` commands that established the 128s (stdout empty, exit 128):

```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e \
  5017e1f7299c3a812e87e7950148f54313dd279e:.ufo/waves/round-47/w1-dispatch.json
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e \
  5017e1f7299c3a812e87e7950148f54313dd279e:.ufo/waves/round-45/w1.ready.dispatched
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e \
  5017e1f7299c3a812e87e7950148f54313dd279e:.ufo/waves/round-45/w2.ready.dispatched
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e \
  5017e1f7299c3a812e87e7950148f54313dd279e:.ufo/waves/round-46/r46-w1-results.json
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e \
  5017e1f7299c3a812e87e7950148f54313dd279e:.ufo/waves/round-46/w2.ready
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -e \
  5017e1f7299c3a812e87e7950148f54313dd279e:.ufo/waves/round-46/w2.ready.dispatched
```

The same four round-46/47 probes were repeated at `1e2c310` and stayed 128, except `round-47/w1-dispatch.json`, which is exit 0 there.

## Forgeries (current interpreter, exit 0)

Copied out of the fixture before scratch was removed. Both runs included the battery (`correction_forgeries 3`, `forgeries_green 0`).

**Spawn lie.** `counts.spawn` 1 with `registry.members` 4 and `taskCall.tasks` 4, on both waves. No `wN.ready`. Card says `Waves: 1 + 1 = 2 seats` and `corrects seats round-9: 2 waves, 2 seats total`. Exit **0**, `failing []`.

- Command UTC `2026-10-28T17:54:24Z`, exit 0, stdout sha256 `ffb8033a77a4ecb7fddda7c500d1eed909db0b707f63109ef16a7c1f793d9ee5`
- Tip `285f5c1a88c6ddb6e408bd2659a6d1c301a9d4a8` (fixture-local)
- Files: `.ufo/waves/round-47/w1/ScoutDispatch/fixtures/spawn-lie/` (`w1-dispatch.json` measured `counts.spawn 1`, members 4, tasks 4)

**Gap.** `w2-dispatch.json` deleted (`cat-file -e` at the fixture tip exit 128). `w3-dispatch.json` has spawn 50 and 50 members. Card says `Waves: 1 + 0 = 1 seats` and `corrects seats round-9: 1 wave, 1 seats total`. The walk stops at the hole and never reads w3. Exit **0**, `failing []`.

- Command UTC `2026-10-28T17:54:25Z`, exit 0, stdout sha256 `c51cbe82b084666edb883a288bd578b97a531ee57bb4a7b8faf056a85a09ec54`
- Tip `8580cc4c1aac839551c0800b5f7a0a684c90ce03`
- Files: `.ufo/waves/round-47/w1/ScoutDispatch/fixtures/gap/` (`w3-dispatch.json` spawn 50; no `w2-dispatch.json`)

On the real rounds 43–47, spawn equals members equals tasks, so the committed integers are not currently a lie. The clause is still satisfied by editing only `counts.spawn`, and by a `w3` hidden behind a missing `w2`.

## Not run

Full `record.py` against the dirty worktree `SCORECARD.md` (the `## Round 47` heading). Battery-on runs at the freeze and at `1e2c310` (the fixture runs did include the battery; the lane runs were `--no-battery`).
