# ExecCoverage — R65-C2 measurements

Axes: population completeness, mapping correctness, historical discrimination, negative-control sensitivity, substrate preservation.

## Findings

The base comparison behaves as predicted: stem includes and maps all 144 entries with zero mismatches; date excludes two entries and returns exit 1. Both historical controls are clean with 142 entries. Selftest: CLEAN, 28 cases, zero failures, exit 0.

**Naming caveat:** the frozen date JSON has `population_dropped: 2` but no list naming those entries. Supplementary `c2-dropped-names.json`, computed using the frozen `read_inputs` and `DATE_TOKEN_RE` at the same base, names:
- `corpus/knowledge/jsc-mapper-cli-contract.md`
- `corpus/knowledge/jsc-mapper-release-inventory.md`

Thus the numeric portion of C2 is reproduced; a literal requirement that the superseded recipe itself output the hidden filenames is not satisfied by its JSON. No instrument edits were made.

**Red-arm blocker:** the higher-priority fleet executor instruction prohibits commits without a fixture exception. The requested shared scratch clone was created successfully, with top-level `/fast/scratch/hyaku/kaidoku-r65/ExecCoverage/lane` and tip `922ed89f42bed28173035f3faaf705e0cb70abb7`. No fixture commit or working-tree mutation was made. Therefore the requested committed-clone CLI red arm is NOT completed. As separately labelled supplementary evidence, calling the frozen `assess` and `exit_class` in memory after removing exactly one backticked `jsc-mapper-cli-contract` token yields missing `[jsc-mapper-cli-contract]`, mismatches 1, computed exit class 1. This is not a process exit or a substitute for the requested committed-clone run.

## Measured numbers

| Receipt | process exit | knowledge_files | population | mapped | population_dropped | mismatches | missing | dangling |
|---|---:|---:|---:|---:|---:|---:|---|---|
| c2-before-date.json | 1 | 144 | 142 | 142 | 2 | 2 | [] | [] |
| c2-after-stem.json | 0 | 144 | 144 | 144 | 0 | 0 | [] | [] |
| c2-ctrl-date-df727606.json | 0 | 142 | 142 | 142 | 0 | 0 | [] | [] |
| c2-ctrl-stem-df727606.json | 0 | 142 | 142 | 142 | 0 | 0 | [] | [] |
| c2-red-inmemory.json (supplementary) | not run; exit class 1 | 144 | 144 | 143 | 0 | 1 | [jsc-mapper-cli-contract] | [] |

The shell wrappers ended with `echo exit=$?`, so their outer status was 0; the table records the instrument statuses printed by that echo and present in each JSON.

## Exact measurement commands

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-65/coverage-recipe.py --selftest > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ExecCoverage/selftest.txt 2>&1; echo exit=$?
```
Exit 0, `SELFTEST CLEAN cases=28 failures=0`.

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-65/coverage-recipe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c99e907cb5576c13a7b22755d776b356fdfc1752 --recipe date --out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ExecCoverage/c2-before-date.json; echo exit=$?
```

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-65/coverage-recipe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev c99e907cb5576c13a7b22755d776b356fdfc1752 --recipe stem --out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ExecCoverage/c2-after-stem.json; echo exit=$?
```

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-65/coverage-recipe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev df727606 --recipe date --out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ExecCoverage/c2-ctrl-date-df727606.json; echo exit=$?
```

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-65/coverage-recipe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev df727606 --recipe stem --out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ExecCoverage/c2-ctrl-stem-df727606.json; echo exit=$?
```

## Preparation and cleanup evidence

Preparation used `mkdir -p` for the assigned scratch and receipt directories, `sha256sum` on both frozen instruments, disk guard `status`, and read-only `git -C` rev-parse/log calls. Disk guard completed: scratch 50% used, 404.5G free. Coverage instrument SHA256: `9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6`; closure instrument SHA256: `79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6`.

Clone preparation command (exit 0):
```sh
S=/fast/scratch/hyaku/kaidoku-r65/ExecCoverage; git clone --shared --quiet /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/lane" && T=$(git -C "$S/lane" rev-parse --show-toplevel) && echo "toplevel=$T" && TIP=$(git -C "$S/lane" rev-parse HEAD) && echo "tip=$TIP" && git -C "$S/lane" log --oneline -2 && git -C "$S/lane" show "$TIP:corpus/README.md" | sed -n '/^## Coverage map/,/^## /p' | sed -n '1,40p'
```
No author identity configured, no commit made. No tools installed or updated. No toolchain paths were written. The preflight shell commands accidentally used non-null service names; they were finite and exited, not intentionally long-lived work.

Scratch cleanup completed with exit 0:
```sh
rm -rf -- /fast/scratch/hyaku/kaidoku-r65/ExecCoverage && test ! -e /fast/scratch/hyaku/kaidoku-r65/ExecCoverage && printf 'scratch_removed=true\n'
```
Output: `scratch_removed=true`.

## Receipt SHA256

```
5e1377822a0fb820d2f43506108753dc744ff85ea9c4c2db12fd8e60f61a9af2  selftest.txt
8fcfc339a10cbd4199eb8a0278fd618d802b89466c30bcc9d6fbf838c8290108  c2-after-stem.json
fa02c97a6ca5c003ee86de8d761aada260b16f857c9267abb78cfba156acb2a8  c2-before-date.json
9088d1a8f29dbf148a97bf050c22c279479e836b21519489c9f687ab5a16631f  c2-ctrl-date-df727606.json
c7d4419fc80d9fbf4be7a32c14e0951a2b001113d5c718f10854313e0ecf5b47  c2-ctrl-stem-df727606.json
920034c939b94bff630152b93f3270eb66733ca70df48f96ce9016c30437d2e0  c2-dropped-names.json
23145936b831d416635646041abb53ec16a4facebf45989d51e9460dcfb37c30  c2-red-inmemory.json
```

## Advisory self-assessment

Accuracy 4: process exits are distinguished from the in-memory exit class; hidden-name evidence is supplemental rather than attributed to JSON. Completeness 3: committed-clone red arm remains blocked by the governing no-commit instruction. Clarity 4: exact commands and one numeric table are retained, but supplementary evidence requires care. Actionability 4: parent can decide the literal naming requirement and run the blocked arm under an authorized seat. Conciseness 4: command detail is retained for reproducibility. Average 3.8. Main improvement: obtain a governing fixture-commit exception before requesting that arm. Would the user agree: likely on the evidence, not on calling the blocked arm complete; it is explicitly incomplete.
