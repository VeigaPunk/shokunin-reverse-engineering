# Receipt — `tools/round-44/c1-counter.py` registry row

Seat `R45W1RegR44C1Counter`, round 45 wave 1. Every row below is a command that was run,
with its exit code, the sha256 of its stdout and the UTC second it started. Nothing is inferred.
Scratch: `/fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter`, with `TMPDIR` and
`HYAKU_SCRATCH` pointed into it (nothing under `/tmp`); removed after these receipts were
copied here. Fixture repos were `git -C "$D" init -q` and
`git -C "$D" rev-parse --show-toplevel` was asserted equal to `$D` before the first commit.

## Instrument identity

| check | value | command | exit |
|---|---|---|---|
| blob at freeze | `9695d586b3b1a792f1ad15e8dc4b4f54b8fe1569` | `git rev-parse f762b72:tools/round-44/c1-counter.py` | 0 |
| blob at HEAD | `9695d586b3b1a792f1ad15e8dc4b4f54b8fe1569` (identical) | `git rev-parse HEAD:tools/round-44/c1-counter.py` | 0 |
| bytes at freeze | sha256 `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993` | `git show f762b72:tools/round-44/c1-counter.py \| sha256sum` | 0 |
| bytes in worktree | same sha256 | `sha256sum tools/round-44/c1-counter.py` | 0 |
| last commit touching it | `c48f8a4b… round-44: freeze C1/C2 claims, carriers, counters, and controls` | `git log --format=%H %s -1 -- tools/round-44/c1-counter.py` | 0 |
| row bytes | `row.txt` (1529 bytes, one line, no trailing newline) sha256 `2f2ea910c9c6cb86ea5b5ea389dd2cfa571821d21299a91cbcc6997efed0a931` | `sha256sum row.txt` | 0 |
| row occurs verbatim in `row.md` | 1 match | `grep -c -F -x -f row.txt row.md` | 0 |

## Exit-path probes

Run from the lane root. `<rea-agents 6.5.0 root>` =
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (6.5.0, read from its
`package.json`). `stderr` tail shown; `—` means empty.

| probe | argv | exit | stdout sha256 | UTC | stderr tail |
|---|---|---|---|---|---|
| `help` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --help` | **0** | `24864e9af3ecbcd2cb663b62864204f120b18c1624e60a0db5cdbf7efd885081` | 2026-10-28T15:42:27Z | — |
| `no-args` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py` | **2** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T15:42:28Z | usage: --root --rev --freeze --pkg65 required |
| `unknown-option` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --bogus` | **2** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T15:42:28Z | c1-counter.py: error: unrecognized arguments: --bogus |
| `selftest-good` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter/w-selftest` | **0** | `fbe23fefc21c12358232a8146947a3da39e96fc1d359fa9f61ec36178310da1c` | 2026-10-28T15:42:41Z | — |
| `selftest-no-pkg65-no-xpin` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --selftest` | **0** | `fbe23fefc21c12358232a8146947a3da39e96fc1d359fa9f61ec36178310da1c` | 2026-10-28T15:42:28Z | — |
| `selftest-from-relocated-copy` | `python3 -I -B /fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter/c1-counter.py --selftest` | **1** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T15:43:01Z | xpin-attribute.mjs not found from /fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter |
| `selftest-pkg65-undiscoverable` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --selftest` | **1** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T15:43:01Z | selftest needs --pkg65 (a rea-agents 6.5.0 package root) |
| `selftest-bad-pkg65` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --selftest --pkg65 /nonexistent-pkg` | **1** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T15:42:53Z | xpin mint failed: xpin-attribute: 6.5.0: cannot read package files under /nonexistent-pkg: Cannot find module '/nonexistent-pkg/dist/domain/canonicalD |
| `selftest-unwritable-work` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /proc/self/nope` | **1** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T15:42:53Z | FileNotFoundError: [Errno 2] No such file or directory: '/proc/self/nope' |
| `no-rerun` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --no-rerun` | **2** | `cae5e4643f417d5d6c970dc3b9a39b04cf459703761123d615b204c30a16a503` | 2026-10-28T15:42:53Z | — |
| `dev-arm-no-root` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --dev-arm` | **2** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T15:42:53Z | usage: --dev-arm needs --root |
| `dev-arm-no-arm` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --dev-arm --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` | **2** | `2e611334084aecfd6164555b6b53e6be338ba223f1dad53a4a6dddc38e2cb802` | 2026-10-28T15:42:53Z | — |
| `verify-receipt-ok` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --verify-receipt /fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter/vr-ok.json` | **0** | `80eaa5ac229b573762ea070296b21b647c57c011513eb706b4e4eed64398814d` | 2026-10-28T15:42:53Z | — |
| `verify-receipt-mismatch` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --verify-receipt /fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter/vr-bad.json` | **1** | `301ddb66a0df66a1ed905de107ff7c3e2b3908734b7323764e8fa48459e91aee` | 2026-10-28T15:42:53Z | — |
| `verify-receipt-unreadable` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --verify-receipt /fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter/nope.json` | **2** | `009ef2ee2b5472dbd503e25c5e95982274c6d6dc2dacea42e7c3422d88abe1f8` | 2026-10-28T15:42:53Z | — |
| `score-malformed-carriers` | `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-44/c1-counter.py --root /fast/scratch/hyaku/kaidoku-r45/R45W1RegR44C1Counter/fx-badjson --rev 1c1b886318747fea3c7f68f4ab943f8ab5756bcd --freeze 1c1b886318747fea3c7f68f4ab943f8ab5756bcd --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | **2** | `879a35dbe1d83ad140343736e8e412662f448d6ae222cd962375e09dc8f8d550` | 2026-10-28T15:42:53Z | — |

`selftest-good` stdout: `{"cases": 47, "failures": [], "green_ok": 1, "red_ok": 46,
"receipt_probes": 5, "prefix_probes": 6, "selftest": "c1-counter", ...}` →
`red_ok 46` means 46 of the 47 cases are negative controls; there is exactly one positive
case. Two independent runs produced byte-identical stdout (`fbe23fef…`), so the selftest is
deterministic on this host.

Exit codes observed across the 16 probes: `{0, 1, 2}`. None outside that set.

## R45-C2 landing simulation

Counter: `tools/round-45/c2-counter.py --root <fixture> --rev <HEAD> --freeze <HEAD>`.
Freeze == rev, so its frozen-path arm is empty by construction. Scope file copied verbatim
from `tools/round-45/registry-scope.json` (6 paths).

| fixture | exit | stdout sha256 | `failing` |
|---|---|---|---|
| clean | **0** | `df6b59f56e7900ba3b07c5e59a7048db173a58ec726ccbc5a7f92579bddcca0e` | `[]` |
| thin | **1** | `4a38f11abe80c68be2cdf5df7c33583faac5e9a05ef9cebfe9914df8419c6abd` | `["thin exit-code cells: ['tools/round-44/c1-counter.py']"]` |
| wrongpath | **1** | `cdacfe458aec4e81bec21cb1f0244c7227732cbb4f6d5e10bbf72bc5159697e8` | `["unregistered: ['tools/round-44/c1-counter.py']"]` |

Clean fixture stdout: `registered` = all six scope paths, `unregistered []`, `thin []`,
`scope_size 6`, `registry_rows 6`, `met_target true`.

Shadowing check: parsing the live `SKILL.md` rows (six, the incumbent first) with this row
appended gives `dup_rows_for_path: 2` and `first_match_is_existing: True` — `by_tool`
resolves to the row at `SKILL.md:1636`.

## Pinned values at the freeze

| check | command | exit | result |
|---|---|---|---|
| carrier map | `git ls-tree -r --name-only f762b72 -- tools/round-44/carriers.json` | 0 | `tools/round-44/carriers.json` |
| carrier bytes | `python3 -c "import json;print([(c['id'],c['handler'],c['path']) for c in json.load(open('tools/round-44/carriers.json'))['carriers']])"` | 0 | 4 carriers: `v1le`/`v1be` → `squashfs_v1`, `v2le`/`v2be` → `squashfs_v2`, bytes under `corpus/evidence/round-42/c2/fixtures/` |
| expected trees | `git ls-tree -r --name-only f762b72 -- corpus/evidence/round-44/c1` | 0 | 126 files, four `v*/` carrier dirs |
| frozen path families | source `FROZEN_PATHS` (10) and `FROZEN_PREFIXES` (`tools/round-44/`, `corpus/evidence/round-44/oracle/`) | — | the carrier `.bin` bytes are bound by the `carrier_pin_ok` sha clause, not by a frozen path |

## Write-scope evidence

`grep -n "open([^)]*['\"]wb\?['\"]" tools/round-44/c1-counter.py` → six sites, all rooted at
the private `work` dir: 609 (`work/xpin-attribute.mjs`), 614 (`work/<name>.wrapped.json`),
1876 (`work/rerun-<id>/carrier.bin`), 2288 (the `--json-out` path), 2732 (mint payload under
`work`), 3305 (selftest fixture repos under scratch). `scratch_root()` (line 452) reads
`--work` → `$HYAKU_SCRATCH/kaidoku-r44/counter` → `/fast/scratch/hyaku`, never
`tempfile.gettempdir()`.

## Not run

- A scoring run of the instrument against the lane (real REA rerun of four carriers). Not run.
- `--dev-arm --run-rea` on the real carrier bytes. Not run.
- `frozen_path_changed` in scoring mode against a real two-commit lane. Not run out of
  process; covered by four selftest cases wanting exit 2 (`carriers.json changed`, `carrier
  bytes changed`, `oracle tree edited`, `frozen path touched then restored`).
