# R45W2Waves receipts

All times UTC. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (call it `$L`).
Write scope: this directory only; nothing under `tools/round-45/`, `plans/`, `SKILL.md`,
`corpus/`, `LOG.md`, `SCORECARD.md` or the fleet repo was written. No git/jj mutation.
No install made this seat (tool inventory unchanged; pacman untouched).

## Primary instrument

| id | command (cwd = `$L`) | exit | stdout sha256 | utc |
|---|---|---|---|---|
| R1 | `python3 .ufo/waves/round-45/w2/R45W2Waves/check_shape.py .ufo/waves/round-45/w2/R45W2Waves/shape-checks.json > …/shape-checks.log 2>&1` | **1** (9 of 28 checks fail) | receipt body `254c2c2d3e8207b2512fafefc439435bc2be12bfe71b863b53e7e255dec9c574`; log `686acd495126eb80b588e706ea6b915f992cc130fda4cd942cd8fd2cc6969954` | 2026-10-28T16:04:53Z |

`check_shape.py` (`36b6c4b9feeadc24d4e24fcc18bb9e5c6aa741ea2b81886646270a9eadf6dd12`) is read-only:
it opens committed wave artefacts plus `scripts/hyaku/inline-dispatcher.py` and writes one JSON
receipt. Re-running it reproduces every number in `report.md`; only the `utc` field changes.

## Supporting measurements

| id | command (cwd = `$L/.ufo/waves/round-45`) | exit | result |
|---|---|---|---|
| R2 | `jq -r '.taskCall.tasks[].name' w1-dispatch.json \| sort > d; jq -r '.results[].name' r45-w1-results.json \| sort > l; diff d l` | 0 | identical: the 40 dispatched names are exactly the 40 ledger names |
| R3 | `jq -r '.counts, (.taskCall.tasks\|length)' {w1,w2}-dispatch.json` | 0 | w1 `{spawn:40,resume:0,total:40}`, 40 tasks; w2 `{spawn:36,resume:0,total:36}`, 36 tasks |
| R4 | `jq -r '[.taskCall.tasks[].agent]\|group_by(.)\|map("\(.[0])\t\(length)")' {w1,w2}-dispatch.json` | 0 | role histograms in `report.md` §2 |
| R5 | `jq -r '.members\|length' {w1,w2}/swarm-registry.json` | 0 | 40 / 36, all `kind:spawn`, all `agentId:null` |
| R6 | `ls $L/.ufo/waves/round-45/r45-w2-results.json` | 1 (ENOENT) | wave-2 ledger **absent** at run time |
| R7 | `find w1 -maxdepth 1 -name '*.md' \| wc -l` / `find w1 -mindepth 1 -maxdepth 1 -type d \| wc -l` | 0 | 25 / 25, names diff empty → 25 delivered seats on disk |
| R8 | `git log -1 --format='%H %ci %s' <rev>` for `f762b727`,`e715263c`,`1f4b27f8`,`fedd11bf`,`f59565b7`,`0ee50aa` | 0 | times in `report.md` §4 |
| R9 | `git show <rev>:…/w2-spec.json \| python3 -c '…len(d["items"])'` for `1d04c6af~1`, `1d04c6af`, `HEAD` | 0 | 36 / 36 / 36 — the w2 spec never carried 32 |
| R10 | `git show abfeda50:.ufo/waves/round-45/w2-spec.json` | 128 | absent at the commit that wrote "wave 2: 32 seats" (LOG:3273, SCORECARD:3527) |
| R11 | band census over `round-*/{w,wave}*-dispatch.json`, deduplicated (`band-census.json`) | 0 | 47 wave dispatches, rounds 16–45; bands `(64,100)`×16, `(32,64)`×30, `(32,256)`×1, `(64,128)`×0 — policy v2's band has never been used by a committed dispatch |
| R12 | ledger census over every `*-results.json` under `.ufo/waves` (`lane-ledger-census.json`) | 0 | 17 wave ledgers, rounds 35–45; dead entries only in `round-35/w1` (64, harness string) and `round-45/w1` (15) |
| R13 | `grep -rn "never spawned\|job-cap\|job cap\|partial-fill" /home/vgpnk/Projects/shokunin/scripts/` | 1 (no match) | no fleet script emits the round-45 dead-seat note |
| R14 | `git log --format=%h -- scripts/hyaku/inline-dispatcher.py` + `git show <h>:… \| grep -A2 "ready + '.dispatched'"` | 0 | every committed version writes an ISO timestamp line (+ id map from 216cfd36); none writes a bare epoch |
| R15 | `date -u -d @1793201921 +%FT%TZ` | 0 | `2026-10-28T15:38:41Z` — the bare-epoch `w1.ready.dispatched` marker |
| R16 | `python3` per-seat revision scan of `w2-dispatch.json` (`w2-revision-pointers.json`) | 0 | 12 prompts name A3 `f59565b7` (4 of those also name A1 and/or the landing), 1 names only the landing `e715263c`, 23 name no sha at all; the shared `context` names A1 `1f4b27f8` as "the measured revision" |
| R17 | `git cat-file -e HEAD:.ufo/waves/round-45/r45-w2-results.json`; `git log --oneline --all -- <same path>` | 128 / 0 (empty) | the wave-2 ledger is absent at HEAD and no commit ever carried it |

## Receipt files (sha256)

| file | sha256 |
|---|---|
| `shape-checks.json` | `254c2c2d3e8207b2512fafefc439435bc2be12bfe71b863b53e7e255dec9c574` |
| `shape-checks.log` | `686acd495126eb80b588e706ea6b915f992cc130fda4cd942cd8fd2cc6969954` |
| `check_shape.py` | `36b6c4b9feeadc24d4e24fcc18bb9e5c6aa741ea2b81886646270a9eadf6dd12` |
| `band-census.json` | `92c056db28681b528b5978cfcc6b8fde4942986dfe8ce17e32de63945aa4ea4c` |
| `lane-ledger-census.json` | `7cbf470d02b9fd84514c77d2f09890b878b0240ac4df229ce5a927c62502e324` |
| `w1-shape.json` | `7c60b4c1099c8863bc294865916a1007a077b81a8da85e56a3b68c20386013f4` |
| `w2-revision-pointers.json` | `34ba3cc6ef9e02fb4e98a38382db66a3a7f180ed51c35194e950e1e713de7c42` |

Input hashes (read-only, whole-file sha256) recorded at 2026-10-28T16:01:47Z:

| input | sha256 |
|---|---|
| `w1-dispatch.json` | `fec3d2b055d0fcbbe94fcc1ab476efb00c23d3a01fe75397ce1869705b7b4087` |
| `w2-dispatch.json` | `0dfade1b643085d0a8d507a886b695a21adc107134e70c847f304e0b5e0da5a8` |
| `w1-spec.json` | `5c493b13a62003ea1c924e591101b349159ca6d6fe662bbcbad8333ef497afc9` |
| `w2-spec.json` | `23d059d7a7abb0abef38b8370fe2bb1aeb58658c6b9e184d4dce739e2d09d73d` |
| `r45-w1-results.json` | `6773b1777c3f377cbb752e53ab8186e88d1a899f814fcb8162e08ff8fd4649d9` |
| `w1/swarm-registry.json` | `db6bdd2ca05b2e555b340fff2f8dccbed8028593fdf6e65d0da78cce4e95e084` |
| `w2/swarm-registry.json` | `42d02252464909e2611c6bcc20e506cf8377fa2adda247a28ce3090446f81631` |
| `w2.ready.dispatched` | `7bcf718e985c3aa1ebb33a87de0f90ef7c4df6faf8e55955e45be12e65559ea4` |

Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W2Waves` removed after these receipts were copied here.

The seat's final text is also written, byte-identical, at
`.ufo/waves/round-45/w2/R45W2Waves.md` — sha256 `c3ad9f8d3350cb738def017c01d16a6a3a70f80bce19737eec0c9716438b2f24`,
the same as `.ufo/waves/round-45/w2/R45W2Waves/report.md`. Lane tracked tree untouched:
`git status --porcelain` prints no non-`??` line.
