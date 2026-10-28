# R46W1RegI — receipts

Seat `R46W1RegI`, round 46 wave 1, tag `reg-i`. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegI` (exported as `TMPDIR` and `HYAKU_SCRATCH`),
removed after these receipts were copied here. All reads of the frozen instruments are
`git -C <lane> show 31820472784284727546808acc31b3ea1e73919b:<path>` (exit 0 for every
path below); no frozen file was modified, and no mutating git command was run.

Source bytes at the freeze (sha256 of the `git show` output):

| path | blob at 3182047 | sha256 at 3182047 | sha256 at 50862e4a |
|---|---|---|---|
| `tools/round-41/indep-eval-v3.py` | `f4b22f8a22b6cec0e55871b2c28247ca429b12dd` | `26178d71c0f7634c3f1371ad5c4c7de3b59c49636cdf1b61bf8b2e461c75dce1` | same |
| `tools/round-42/sqfs-triage-v4.py` | `79265904ff0234ed505d9daedf4cfe570c5cf12f` | `497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9` | same |
| `tools/round-46/attest.py` | `25883520b42562915f829e977a3290e0971ad503` | `dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb` | `eba599582bb32eab3c47d7c15cbd53852e257070ae756136e3cee059e37311fd` |

`eba59958…` is the sha256 pinned in `SKILL.md` rule block 23 (line 612 at `87578656`),
i.e. the pin names the **50862e4a** bytes, not the 3182047 bytes.

## Selftests (the command quoted in each row)

| UTC | command | exit | stdout sha256 | observed |
|---|---|---|---|---|
| 2026-10-28T16:55:45Z | `python3 -I -B tools/round-41/indep-eval-v3.py --selftest` | 0 | `a82b2978a06676345ef7b799b51a419d969e281cc3ca25bbb75967418acd1f70` | `"cases": 46`, `"ok": true`, `"failures": []`, steps 1–12 and all 13 labels covered |
| 2026-10-28T16:55:45Z | `python3 -I -B tools/round-42/sqfs-triage-v4.py --selftest` | 0 | `a290741c5c90297d0c40e58ab14142a1ec599af092114967973bdd6497dec8f2` | `SELFTEST cases=123 pass=123 fail=0` |
| 2026-10-28T16:56:00Z | `python3 -I -B tools/round-46/attest.py --selftest --root . --freeze HEAD --rev HEAD` (lane worktree) | 0 | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | `ATTEST_SELFTEST: cases=16 failures=0` — 16 because the worktree copy carries an uncommitted edit; the frozen and pinned bytes print `cases=15 failures=0` (next two rows) |
| 2026-10-28T16:54:xxZ (frozen copy) | `python3 -I -B attest.py --selftest --root "$S" --freeze HEAD --rev HEAD` at 3182047 bytes | 0 | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | `ATTEST_SELFTEST: cases=15 failures=0` |
| 2026-10-28T16:54:xxZ (pinned copy) | same, at 50862e4a bytes | 0 | (same shape) | `ATTEST_SELFTEST: cases=15 failures=0` |
| 2026-10-28T16:56:18Z | `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --table-only` (lane root) | 0 | `f0bc0a9bc54c3ae1db3b3369c7964631f3f7ef8943f6813edf9b87fcdcb04508` | `marker line: 525  actions line: 526  table line: 527  rules: 15` — confirms the 0 arm of that row's verdict map |
| 2026-10-28T16:57:18Z | `python3 -I -B registry.py --selftest --root "$S" --freeze HEAD --rev HEAD` (pinned 50862e4a bytes) | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | `REGISTRY_SELFTEST: cases=12 failures=0` — the claims file's preflight says 11 |
| 2026-10-28T16:57:23Z | same (3182047 bytes) | 0 | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | `REGISTRY_SELFTEST: cases=12 failures=0` |

## Bad-argument / boundary probes (the second verification per row)

| UTC | command | exit | stdout sha256 | observed |
|---|---|---|---|---|
| 2026-10-28T16:57:36Z | `python3 -I -B indep-eval-v3.py` | 2 | `9e0ac367c2f5553171a8bb854683ec79581ef318de58868a9ccf727f4ec3212b` | `error: one of --envelopes or --selftest is required` (argparse) |
| 2026-10-28T16:57:36Z | `python3 -I -B indep-eval-v3.py --envelopes /nonexistent` | 2 | `c8c3c0643a25b0401fc20cbb304d01ea93cd51d266c14ffd6962924a60c8970d` | `error: --envelopes '/nonexistent' is not a directory` |
| 2026-10-28T16:57:36Z | `python3 -I -B indep-eval-v3.py --envelopes ie-bad` (a directory holding one invalid JSON) | 0 | `08cdef5b94002a2ded39ad8eac269359bc99eef63eec80ad9c95b6c1806e054c` | `envelope_count: 0` and `errors: {broken: … Expecting property name …}` — **an unreadable envelope is exit 0**, so this tool has no could-not-evaluate exit |
| 2026-10-28T16:57:36Z | `python3 -I -B sqfs-triage-v4.py` | 2 | `f06372037ea2ec9d7a8cbc31ef0b8168a77dce279dea50d67e6d48de2da8c91a` | `sqfs-triage-v4: --skill is required with envelopes or --table-only` |
| 2026-10-28T16:57:36Z | `python3 -I -B sqfs-triage-v4.py --table-only` | 2 | `f06372037ea2ec9d7a8cbc31ef0b8168a77dce279dea50d67e6d48de2da8c91a` | same message; confirms the 2 arm |
| 2026-10-28T16:57:36Z | `python3 -I -B attest.py --selftest` (no path flags) | 2 | `3ed94b41f2837c05d27b9c05e94e8b82de953e398d3936edf35a3550079069e9` | `error: the following arguments are required: --root, --freeze, --rev` — the claims file's preflight form does not run |
| 2026-10-28T16:57:36Z | `python3 -I -B registry.py --selftest` (no path flags) | 2 | `39b32007f23adb6cd77580f85875a84b170c437aeaeecf85b74fe63389ac4009` | same required-argument error |

## The frozen C1 instrument scored against the lane

Commands run with the **pinned** `attest.py` bytes (50862e4a, sha `eba59958…`), from the
lane root; `--json-out` landed in `run/` inside this seat directory (allowed: `.ufo/` is not
a graded head).

| UTC | command | exit | receipt sha256 | observed |
|---|---|---|---|---|
| 2026-10-28T16:54:28Z | `python3 -I -B attest.py --root <LANE> --freeze 31820472784284727546808acc31b3ea1e73919b --rev 8757865679e62dac1f50efb33f583de0be884bf3 --json-out run/attest-freeze-3182047.json` | 2 | `896d7ea6a92cd22072eb00bc7ae9cdf968a0623c103e6cc53bf31d30d734dcfa` | `"reason": "frozen_path_changed"`, `frozen_path_changed: ["tools/round-46/", "tools/round-46/attest.py", "tools/round-46/gate.py", "tools/round-46/registry.py"]`, `blob_changed: ["tools/round-46/"]` |
| 2026-10-28T16:54:28Z | same with `--freeze 50862e4a041499dd2ce0da68d10301b765bb9997` | 2 | `a8067ef63f99d1d7c44424502fc188a64bdfe9df90cdadbc3f96098241496e7f` | `{"reason": "unhandled NameError: name 'REF' is not defined"}` — 64 bytes, no `met_target` |
| 2026-10-28T16:54:48Z | same with `--no-battery` | 0 | `ec2392a85007f24d9006b7e4c932421684208a270b095961f9d53535c3642a89` | `met_target: true`, `failing: []`, `frozen_path_changed: []`, `rows` ≥ 13, `header_ok: true`, `marker_occurrences: 1`, `pin == pin_expected == eba59958…` |
| 2026-10-28T16:56:12Z | `python3 -I -B -c "import attest; attest.m_self_refs(...)"` on the pinned bytes | 3 (probe's own code) | `3e984bbeb0d0c02fe013602e23151774553954f59026bbdc8f79cb7c7e12f5ae` | `NameError: name 'REF' is not defined`; `REF` is absent from both byte sets, which define `HARD_REF`/`LOOSE_REF` — the defect is `attest.py:322` in `m_self_refs` |

## The rows, scored by the frozen registry parser

`registry.score(skill, files, "r46", "v2", "deadbeef", battery=None)` from the frozen
`tools/round-46/registry.py`, with `rows.md` pasted under the house header between the two
v2 markers, and `census.json` served from the freeze:

- three rows parsed, `registry_rows: 3`, header equals `HOUSE` exactly;
- `registered` contains all three of my paths; `thin == []`; `absent_at_rev == []`;
- `unregistered: 35 of 38` and exit 1 — expected, the fixture held only my three rows;
- `EXITMAP` keys in each verdict-map cell are exactly `{0,1,2}` (the frozen
  `\b([012])\s*[=:]` regex, not the looser digit-presence test).

## Exit codes outside {0,1,2}

None observed from any of the three instruments: argparse and the tools' own paths produce
only 0, 1 and 2. Not observed but worth knowing: `indep-eval-v3.py` and
`sqfs-triage-v4.py` have no top-level exception guard, so an uncaught traceback would exit
1 with a traceback — that would be indistinguishable from "selftest failed" in whose map
1 means a failed selftest. `attest.py` guards every entry point and returns 2 instead
(`gate.main_guard`). No probe produced such a traceback.

## The lane moved during this seat: reconciled measurements

The lane advanced `87578656` → `17a72375` → `781e19ae` → `04252247` → `1e32827b` between
16:55Z and 17:01Z. Every measurement below names its `rev` (read from the receipt's own
`rev` field) so nothing here is a claim about "HEAD".

| UTC | command | exit | receipt sha256 | observed |
|---|---|---|---|---|
| 2026-10-28T16:59:08Z | `python3 -I -B tools/round-46/attest.py --selftest --root . --freeze HEAD --rev HEAD` (worktree = `65678df0` bytes) | 0 | `0bf8f4c6…` | `ATTEST_SELFTEST: cases=16 failures=0` — the F3 repair added `green-with-battery` |
| 2026-10-28T16:59:10Z | `attest.py --root <LANE> --freeze 65678df0f1666e83cdeea7233bfb31ffe73ec709 --rev 17a72375…` | 0 | `b8febffd…` | `met_target: true`, `failing: []`, `frozen_path_changed: []`, battery `9/9/0/1`, `rows 13`, `refs 9`, pin matches |
| 2026-10-28T16:59:24Z | `attest.py --root <LANE> --freeze 50862e4a0414… --rev 17a72375…` | 2 | `83c37805…` | `reason: frozen_path_changed`, `[tools/round-46/, tools/round-46/attest.py]` |
| 2026-10-28T16:59:38Z | `registry.py --root <LANE> --freeze 65678df0… --rev 781e19ae…` | 1 | `ba30eeef…` | `met_target: false`, `failing: ['battery v1_green 0 != 7']`, battery `7/0/0/1`, `registry_rows 38`, `unregistered []`, `thin []`, `absent_at_rev []` |
| same, direct module probe | `registry.score(skill, files, 'r46', 'v1', '781e19ae…')` | — | — | genuine artefact under v1: exit 1, `unregistered: 32 of 38`, `rows 45` — the v1 port was red on the honest section itself |
| 2026-10-28T17:01:05Z | `attest.py --root <LANE> --freeze 04252247… --rev 04252247…` | 0 | `5811bfe0…` | `met_target: true`, `failing: []`, battery `9/9/0/1` |
| 2026-10-28T17:01:06Z | `registry.py --root <LANE> --freeze 04252247… --rev 04252247…` | 0 | `d3869553…` | `met_target: true`, `failing: []`, battery `7/7/0/1`, `registry_rows 38`, `unregistered []`, `thin []`, `absent_at_rev []`, `frozen_path_changed []` |
| 2026-10-28T17:01:25Z | `attest.py --root <LANE> --freeze 65678df0… --rev 1e32827b…` | 2 | `a5a89058…` | `reason: frozen_path_changed`, `[tools/round-46/, tools/round-46/registry.py]` |

Row-vs-landed diff at `781e19ae` (checked by parsing both texts): rows 1 and 2 are
byte-identical to the landed rows; row 3 differs in cell 4 only — the landed cell says
"15 cases", the repaired instrument prints 16 from `65678df0` onward. My `rows.md` now
carries both counts with the revision each belongs to. Nothing else in the three rows
changed.
