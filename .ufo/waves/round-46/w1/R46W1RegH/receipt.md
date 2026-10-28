# R46W1RegH — receipts (round 46, wave 1)

Seat `R46W1RegH`, tag `reg-h`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch `S=/fast/scratch/hyaku/kaidoku-r46/R46W1RegH` (`TMPDIR=HYAKU_SCRATCH=$S`), removed at exit.
Lane tree read-only: no write outside `.ufo/waves/round-46/w1/R46W1RegH/` and `$S`; no git mutation.

Provenance of every row: the three instruments byte-read at
`31820472784284727546808acc31b3ea1e73919b`, at `50862e4a…` and at the HEAD current when the rows were
verified. Content sha256 is equal at all three revisions (so the rows cannot be stale against a later HEAD):

| path | sha256 at 31820472 | at 50862e4a | at e3dfdbad / 7bf33e31 |
|---|---|---|---|
| `tools/round-41/heldout-gen-v3.py` | `652d71afe464856caf04286fb653cbc3914373f76f9f5cae9fb22cd577d97e00` | same | same |
| `tools/round-42/prefile-gate.py` | `c3f8abf984fa4f2c247b3b3629721429fc212cb51fe80eeb7aaea0946a2688b6` | same | same |
| `tools/round-45/frozen-path-preflight.py` | `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b` | same | same |

Each command below ran through `$S/receipts/runner.sh <label> <argv…>`, which writes
`receipts/<label>.out` and `.err` and prints `UTC`, `ARGV`, `EXIT`, `STDOUT_SHA256`, `STDERR_SHA256`.
The hashes in the table are the sha256 of those stored files (recomputed after the run).

## Row 1 — `tools/round-41/heldout-gen-v3.py`

| label | argv | exit | stdout sha256 | utc |
|---|---|---|---|---|
| hg-help | `python3 -I -B tools/round-41/heldout-gen-v3.py --help` | 0 | `58d655c6e90b68a9559436ef7c3aab79449d72187f7638fa5e2718983e3ce3a7` | 2026-10-28T16:57:24Z |
| hg-selftest | `python3 -I -B tools/round-41/heldout-gen-v3.py --seed 31820472784284727546808acc31b3ea1e73919b --selftest --scratch $S/hg` | 0 | `8090b455ed5fb3c3c4c2b0d6f0a10c149e20d73e53f934e3a597c9c4c99df814` | 2026-10-28T16:53:20Z |
| hg-noseed | `python3 -I -B tools/round-41/heldout-gen-v3.py --out $S/nope` | 2 | empty (`e3b0c442…`) | 2026-10-28T16:53:52Z |
| hg-badseed | `python3 -I -B tools/round-41/heldout-gen-v3.py --seed zz --selftest --scratch $S/hg` | 1 | empty | 2026-10-28T16:53:52Z |
| hg-verify-norun | `python3 -I -B tools/round-41/heldout-gen-v3.py --seed 31820472… --out $S/hgv --verify --scratch $S/hg` | 1 | `49b1fd8e87c66d1d5462b48345ff47e8dab632057a59eccd272f1be63915de67` | 2026-10-28T16:53:52Z |

Selftest body: `all 12 selftest checks passed`; 52 carriers, 26 classes, 40 named + 12 combos.
Evidence for the row: 0 = build/selftest green (hg-selftest 0, `all 12 selftest checks passed`);
1 = red outcome and also every guard (hg-badseed 1 stderr `--seed must be at least 16 hex characters, got 'zz'`;
hg-verify-norun 1 stderr `--verify needs --run …`); 2 = argparse only (hg-noseed 2 stderr
`heldout-gen-v3.py: error: the following arguments are required: --seed`).
`--help` shows `--actions-set {actionreview,interp,tabledraft}`, so an out-of-choice value is argparse exit 2.

## Row 2 — `tools/round-42/prefile-gate.py`

| label | argv | exit | stdout sha256 | utc |
|---|---|---|---|---|
| pg-help | `python3 -I -B tools/round-42/prefile-gate.py --help` | 0 | `8c8de9a16b4a7aad8e7db491e5f026a9820873dba86b77b5d563d88c4b2320c1` | 2026-10-28T16:53:20Z |
| pg-selftest | `env TMPDIR=$S python3 -I -B tools/round-42/prefile-gate.py --selftest --work $S/pg` (`$S/pg` pre-created) | 0 | `4f07e178262574f5868648c93154ef61da37ca4bad67ce7acd81d46132922465` | 2026-10-28T16:53:29Z |
| pg-noargs | `python3 -I -B tools/round-42/prefile-gate.py` | 2 | empty | 2026-10-28T16:53:20Z |
| pg-fixture-red | `python3 -I -B tools/round-42/prefile-gate.py --root $S/tmp.y3UavdLOvC --round 46` (fresh `git init`) | 1 | `fa9160e3ee3cd2bb2cf306dfe9c8f4199086b1bcff01f1337ad076511fa82aea` | 2026-10-28T16:53:38Z |
| pg-nongit | `python3 -I -B tools/round-42/prefile-gate.py --root $S/notgit --round 46` | 1 | empty | 2026-10-28T16:53:38Z |
| pg-selftest-missing-work | `python3 -I -B tools/round-42/prefile-gate.py --selftest --work $S/no-such-dir` | 1 | empty | 2026-10-28T16:57:24Z |

Selftest body: `SELFTEST cases=12 pass=12 fail=0`. Live red run: `GATE RED — failing: a, d (exit 1)`
(no `.ufo/waves/round-46/`, lesson absent from HEAD). Evidence: 0 = all four conditions PASS
(pg-selftest's green cases; pg-help 0); 1 = at least one condition FAIL (pg-fixture-red 1) — and,
recorded as a quirk, an unusable `--root` also exits 1 with empty stdout (pg-nongit 1); 2 = argparse
only (pg-noargs 2, stderr `prefile-gate.py: error: --root and --round are required`).

## Row 3 — `tools/round-45/frozen-path-preflight.py`

| label | argv | exit | stdout sha256 | utc |
|---|---|---|---|---|
| pfp-selftest | `env HYAKU_SCRATCH=$S TMPDIR=$S python3 -I -B tools/round-45/frozen-path-preflight.py --selftest` | 0 | `9f03df6538de49b733ecc71415bbb192a30aa428b82953f4ea064342389ec06c` | 2026-10-28T16:53:29Z |
| pfp-usage | `python3 -I -B tools/round-45/frozen-path-preflight.py --root <lane>` | 2 | `c675302bcd30443aa992b364ab5cd673a90a0c8cfdd077d53b8d07f6398cbe38` | 2026-10-28T16:53:30Z |
| pfp-freeze-31820472 | `… --root <lane> --freeze 31820472… --rev HEAD --pathspec tools/round-46/ --pathspec plans/round-46-claims.md --freeze-path tools/round-46 --freeze-path plans/round-46-claims.md --require-pathspec` | 1 | `59fa9c4ed1fbe5338dd7ce8d61b4f38958628d172374ece0b04b1f354b2930ac` | 2026-10-28T16:53:38Z |
| pfp-freeze-authoritative | same with `--freeze 50862e4a…` | 1 | `3e037ef07edd931a1e4999f3bd561840ba87f9f5372b5e2ccda1238d31d720ae` | 2026-10-28T16:55:50Z |

Selftest body: `PREFLIGHT_SELFTEST: cases=11 failures=0` (each arm has a red case: `red-touched`,
`red-restored`, `red-dirty`, `red-dirfreeze-no-pathspec`, `red-unknown-freeze`, `red-nonancestor`,
`red-bulk-sweep`, all `ok: true`). Evidence: 0 = clean (green-clean, green-dirfreeze-pathspec,
green-empty-range in the selftest); 1 = `frozen_path_changed` (pfp-freeze-31820472 1); 2 =
could-not-evaluate (pfp-usage 2 prints `{"verdict": "could_not_evaluate", "reason": "usage: …"}`).

## Scorer of the rows — frozen `tools/round-46/registry.py`

| label | argv | exit | stdout sha256 | utc |
|---|---|---|---|---|
| reg-fixture | `env HYAKU_SCRATCH=$S python3 -I -B $S/reg_fixture.py` — builds two scratch fixture repos (rows.md pasted into a v2-bound section, census = exactly my three paths) and scores each with the FROZEN counter, `--spec r46 --profile v2 --no-battery` | 0 | `9b6252bf1c716fc4f9345e158f87903f6b19bb1cc2647d4fd984bbed4cdcf999` | 2026-10-28T16:55:42Z |
| reg-selftest | `env HYAKU_SCRATCH=$S python3 -I -B tools/round-46/registry.py --selftest` | 2 | empty | 2026-10-28T16:56:51Z |
| reg-selftest-dummy | same plus `--root /nonexistent --freeze x --rev x` | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | 2026-10-28T16:57:02Z |
| reg-freeze-brief | `env HYAKU_SCRATCH=$S python3 -I -B tools/round-46/registry.py --root <lane> --freeze 31820472… --rev 50862e4a… --spec r46 --profile v2 --no-battery` | 2 | `3197a648b5049355df2ce3eeeab3aff3d2c398ba18a834f6ea06e22f50f64466` | 2026-10-28T16:55:50Z |
| reg-freeze-50862e4a | same with `--freeze 50862e4a… --rev HEAD` | 2 | `640ab1d1c75caaec530597561b6587218396b62a857d2af452640057071a14ad` | 2026-10-28T16:56:10Z |
| reg-freeze-65678df0 | same with `--freeze 65678df0… --rev HEAD` | 1 | `887f2d206fa26f882e0ab23daaa6b1f532e7e432ebc0f448c6a2d8e45efbefeb` | 2026-10-28T16:56:28Z |
| attest-selftest | `env HYAKU_SCRATCH=$S python3 -I -B tools/round-46/attest.py --selftest` | 2 | empty | 2026-10-28T16:57:02Z |
| restored-semantics | `python3 -I -B $S/restored_semantics.py` (calls `gate.freeze_state` on two fixtures differing only in final bytes) | 0 | `20c1b4a07a3ff6735ce67a3ddd3e14724f4c1b421279a1acfd49a821d8bccc8c` | 2026-10-28T16:57:29Z |
| reg-at-head-781e19ae | `env HYAKU_SCRATCH=/fast/scratch/kaidoku-r46-regcheck python3 -I -B tools/round-46/registry.py --root <lane> --freeze 65678df0… --rev HEAD --spec r46 --profile v2 --no-battery` (HEAD `781e19ae`, section already landed by the L1) | 0 | receipt read as JSON inline, not stored (scratch and receipt file removed in the same command) | 2026-10-28T16:59:30Z |

Scoring of my rows (`reg-fixture`, variant `mine`): `exit 0`, `scope_size 3`, `registered` = all three
paths, `unregistered []`, `thin []`, `absent_at_rev []`, `met_target true`, `failing []`, header equals
the house schema exactly. Negative control (variant `prose`, row 1's verdict map replaced by
`0 rows, 1 column, 2 bytes`): `exit 1`, `thin ["tools/round-41/heldout-gen-v3.py"]`,
`failing ["thin verdict-map cells: 1"]` — so the pass is not vacuous.

Copied into this directory before the scratch was removed: `scored-rows.json` (the frozen counter's
receipt for these three rows, `met_target true`), `scored-negative-control.json` (the prose control,
exit 1 with `thin`), and `reg-fixture.stdout` (both variant summaries).

`restored-semantics`: both fixtures exit 2, and `restored` names `frozen/same.txt` in BOTH — the
tamper-kept fixture's final bytes are `tampered`, the tamper-restored fixture's are `same`. So the
receipt field `restored` does not distinguish modified-and-kept from tamper-then-restored.

Scratch discipline: every fixture and every receipt lived under `$S` and `$S` was removed. One command
(`reg-at-head-781e19ae`) pointed `HYAKU_SCRATCH` at a second temporary root,
`/fast/scratch/kaidoku-r46-regcheck`, because `$S` had already been reaped; it was created and removed
inside that same command, held no fixtures (the run was `--no-battery`, so `gate.scratch` was never
called), and nothing under `/tmp` was used at any point.
