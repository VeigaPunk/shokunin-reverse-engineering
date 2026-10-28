# R46W1RegL — receipts

Raw stdout/stderr for every run below, plus the counter receipts as JSON, are in
`.ufo/waves/round-46/w1/R46W1RegL/evidence/` (`receipt.tsv` is the machine-readable index;
`fixture-*.json` are the counter's own receipts, byte-identical to the captured stdout).

All times UTC unless labelled. Scratch root `S=/fast/scratch/hyaku/kaidoku-r46/R46W1RegL`,
`TMPDIR=$S HYAKU_SCRATCH=$S` for every run; `S` removed after the report files were copied.
Lane root for every git call: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only git).

## Source identity (read at the freeze, never mutated)

Freeze `31820472784284727546808acc31b3ea1e73919b`.

| path | `git show <freeze>:<path>` blob | sha256 of extracted bytes | lines |
|---|---|---|---|
| `tools/round-41/sqfs-list.py` | `a5623aadc8aa48373a5a80159c248658bc93cc77` | `a8e633f5fe34ad9495ef1cf8d4dd43a718e25352b0f5ae13c760655b8664969d` | 1585 |
| `tools/round-43/c1-counter.py` | `e9335c03c6ad5bb7487be7197c0e6ce31c9c9803` | `3a23e93ee95f4b0d69a2f4d03ed2592c9f0b81dbb6188cb6818a18a8f4f33c79` | 4112 |
| `tools/round-46/registry.py` | `6581c1b2acb805a13e50a05ba5992c489a0917fb` | `307506d51f04bb1212aedc34619b675adc378ec8cfeb1ea5d15ac53582b7a449` | 534 |

The whole frozen `tools/round-46/` directory was extracted with
`git archive 3182047 tools/round-46 | tar -x -C $S/frozen` (registry.py imports sibling
`gate.py`; a bare file copy dies `ModuleNotFoundError: No module named 'gate'`, exit 1).
A second copy of the final instrument revision was extracted from
`0425224756791b414454df28a9abf93df154ce` (F4) into `$S/f4`.

## Commands run, exit codes, stdout sha256

Columns: receipt name · exit · sha256(stdout) · UTC · exact command
(`bin/` = the extracted freeze copy, `frozen/` = the extracted freeze directory).

| name | exit | stdout sha256 | UTC | command |
|---|---|---|---|---|
| `sqfs-selftest` | 0 | `5cd3f0602aa41c35cac53a0317292806045e9d130ca2bffb54a876d9e7ad2411` | 2026-10-28T17:03:12Z | `python3 -I -B bin/sqfs-list.py --selftest` |
| `sqfs-noargs` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 2026-10-28T17:03:13Z | `python3 -I -B bin/sqfs-list.py` |
| `sqfs-badimage` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty; reason on stderr) | 2026-10-28T17:03:13Z | `python3 -I -B bin/sqfs-list.py /nonexistent.sqfs --files cap/o.tsv` |
| `sqfs-mut-exit1` | 1 | `7f2ea919daf21c1f3c72a60a12c7f768bbc1f71279a498f9a8776ce0eb891d35` | 2026-10-28T17:03:35Z | `python3 -I -B mut/sqfs-list-mut.py --selftest` (copy with `228: b'hsqs'` → `b'Hsqs'`; prints `13/16 passed`) |
| `c1-selftest` | 0 | `81e2110d5b35de4bec317387297adb96f668b42e36d24ad41608c7824f374b4a` | 2026-10-28T17:00:22Z | `python3 -I -B bin/c1-counter.py --selftest` (prints `SELFTEST cases=91 pass=91 fail=0`, 263 s wall) |
| `c1-noargs` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 2026-10-28T17:03:13Z | `python3 -I -B bin/c1-counter.py` (stderr `usage: --root --rev --freeze required (or --selftest)`) |
| `reg-selftest-bare` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 2026-10-28T17:03:13Z | `python3 -I -B frozen/tools/round-46/registry.py --selftest` (argparse: `--root --freeze --rev` required) |
| `reg-selftest-args` | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | 2026-10-28T17:03:13Z | `python3 -I -B frozen/tools/round-46/registry.py --selftest --root . --freeze 0 --rev 0` (prints `REGISTRY_SELFTEST: cases=12 failures=0`) |
| `reg-noargs` | 2 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 2026-10-28T17:03:13Z | `python3 -I -B frozen/tools/round-46/registry.py` |

## Row validation (the decisive check)

One-commit fixture repo, per the seat contract:
`D=mktemp -d -p $S`; `git -C $D init -q`; asserted
`git -C $D rev-parse --show-toplevel` == `$D` before the first commit; local identity
`st@r46`; files `SKILL.md` (the house header plus my three rows between the two
`instrument-registry v2` markers), `tools/round-46/census.json` (my three paths),
`plans/round-46-claims.md` (`## Frozen paths (exact)`), and the three tool paths as
one-line stubs. `REV=cac00f8d469f8d544b368101fba937e14442f623`.

| check | instrument | exit | receipt |
|---|---|---|---|
| positive: my three rows | `registry.py@3182047 --profile v2 --no-battery` | 0 | `registered`=3, `unregistered`=[], `thin`=[], `absent_at_rev`=[], `failing`=[], `met_target`=true |
| positive: my three rows | `registry.py@F4 --profile v2 --no-battery` | 0 | same: scope 3, rows 3, registered 3, all four lists empty, `met_target` true |
| negative: one verdict cell rewritten `0 rows, 1 column, 2 bytes` | `registry.py@3182047 --profile v2 --no-battery` | 1 | `thin=['tools/round-43/c1-counter.py']`, `failing=['thin verdict-map cells: 1']` |

`--json-out` had to sit inside `--root` (`gate.out_path` refuses outside-lane targets, exit 2
`--json-out outside the lane root`); the fixture receipts were written at `$D/receipt.json`
and `$D/f4.json`.

## Attack on the R46-C2 predicate (same fixture, `registry.py@F4`)

| name | exit | stdout sha256 | UTC | artefact scored |
|---|---|---|---|---|
| `banana-map` | 0 | `3e9fed99cd70f51af4d00313d6ee6aac2eebadb36da640d0f73b5d4c3012246a` | 2026-10-28T17:04:25Z | the `c1-counter.py` row's verdict-map cell replaced by `0=banana; 1=banana; 2=banana`; `--profile v2 --no-battery`; `met_target` true, `thin` [] |
| `vacuous-rows` | 0 | `be630265dfad7704539d622f7ef28a30f2dbe3c4e017bdd6120e56ce6efde6c6` | 2026-10-28T17:04:37Z | all three rows written `\| \`path\` \|  \| 0=banana; 1=nope; 2=whatever \|  \|  \|  \| kaidoku \|` — purpose, self-test, pinned path and write scope all empty; `--profile v2 --no-battery`; `met_target` true, `registered` 3, `thin` [], `failing` [] |
| `vacuous-battery` | 0 | `b528b6aa719d7ad80c29d3603f121957bdd42a1424fda730c80390bb1cccff51` | 2026-10-28T17:05:00Z | the same vacuous artefact with the **battery on**: `forgeries_total` 7, `v1_green` 7, `v2_green` 0, `genuine_green` 1, `failing` [], `met_target` true |

The `\|` inside the third row is the shell-escaped pipe in this markdown table only; the
fixture row itself uses real `|` separators.

## Real-lane probes (read-only)

| check | command | exit | result |
|---|---|---|---|
| freeze arm at the declared freeze | `registry.py@3182047 --root <lane> --freeze 3182047 --rev 8757865679e6 --profile v2 --no-battery` | 2 | `reason=frozen_path_changed`, `touched=[tools/round-46/attest.py, gate.py, registry.py]`, `restored` same three, `blob_changed=[tools/round-46/]` |
| post-freeze commits touching the frozen paths | `git log --format='%h %s' --name-status 3182047..HEAD -- tools/round-46/ plans/round-46-claims.md` | 0 | `50862e4a` (attest.py, gate.py, registry.py), `65678df0` (attest.py), `04252247` (registry.py) |
| claims file unchanged since the freeze | `git diff --stat 3182047 HEAD -- plans/round-46-claims.md` | 0 | empty |
| no frozen-path commit after F4 | `git diff --stat 04252247 HEAD -- tools/round-46/ plans/round-46-claims.md` | 0 | empty |

## Read from source, not executed

- `c1-counter.py` exit 1 on a **pair miss with every binding true**: `2545`
  `met = bool(matched == N and bindings_ok)` feeding `2555` `res['exit_code'] = 0 if met else 1`.
  Reproducing it needs a complete round-43 measurement tree, so this is a source reading.
- `c1-counter.py` has **no `failing` key** in any receipt: the false-binding list is
  `bindings_false` (`2548`, printed at `2622`).
- `sqfs-list.py` exit 1 has no non-selftest producer: the only `1` is
  `return 0 if bad == 0 else 1` at the end of `run_selftest`; both other failure surfaces
  (`ap.error`, `SqfsError`) return 2 and were executed above.
