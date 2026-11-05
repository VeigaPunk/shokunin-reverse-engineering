# Probe-mutation closure: the six A12 selftest survivors die by declared cases

source: S278 — Linux man-pages, ptrace(2), "Use the caller's filesystem UID and GID (see credentials(7)) or effective capabilities for LSM checks." (opened 2026-11-04, https://man7.org/linux/man-pages/man2/ptrace.2.html, located anchor: section "Ptrace access mode checking", snapshot lines 1437–1439, the `PTRACE_MODE_FSCREDS` block). Row S278 landed in `corpus/SOURCES.md` after the round-74 freeze; the frozen `frontier.sources_row_opened` field of `.ufo/waves/round-74/claims.json` names it at the freeze. The channel it gates is S275 (`proc_pid_environ(5)`) and S277 (`proc_pid_cmdline(5)`), both committed rows of `corpus/SOURCES.md`.
verified-at: 2026-11-04 — measured at the round-74 declaration `b3a7e28089582ce5fb002a1b88e5295caf696b9f` (each receipt's `rev` field); receipts committed at the freeze `021914c0e638454e507087accfe41af1ab69f185`. Receipts: `.ufo/waves/round-74/pre/c1-base-arm.json` (patch set `r73probe` on the landed round-73 probe: 4 killed, 6 survivors, pristine 14 green), `.ufo/waves/round-74/pre/c1-post-at-declaration.json` (patch set `r74probe` on `tools/round-74/seam-probe.py`: 10 killed, 0 survivors, pristine 20 green, target pinned), origin `.ufo/waves/round-73/w1/MutProbe/results.json`.
recheck: re-run the two frozen R74-C1 predicate commands from `plans/round-74-claims.md` — `python3 -I -B tools/round-74/probe-mutation.py --root . --rev <measured> --tool tools/round-74/seam-probe.py --patch-set r74probe --work <scratch> --expect-survivors 0 --expect-target-sha256 81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039 --json-out <receipt>` and the same battery with `--tool tools/round-73/seam-probe.py --patch-set r73probe --expect-survivors 6` — then read `survivor_count`, `survivors` and `target_pin.matched` in the receipts.

## What round 73 found

Round 73's mutation probe (`MutProbe`) applied ten defect classes to
`tools/round-73/seam-probe.py` and reported `counts {killed 4, survived 6,
inconclusive 0}` against a green 14-case `--selftest`
(`.ufo/waves/round-73/w1/MutProbe/results.json`). Four classes died on the one
existing A12 case `a12-kernel-cases`; six left the selftest green. The frozen
base arm re-applied the same ten classes to the **landed** round-73 blob
(`target_sha256 9c286fd7187e25a8c6de5d743e21d0402ec6c9862a14aecfaed75b2006710939`,
equal to the frozen `loaded_by_counter` pin for that file in
`.ufo/waves/round-74/claims.json`) and reproduced exactly that shape — killed 4
(`a-drop-forged-detected`, `a-drop-lie-clean`, `a-drop-genuine-rc`,
`a-any-forged-sample`), `survivor_count 6`, `killed_wrong_case []`, pristine
`{cases 14, rc 0}` — in `.ufo/waves/round-74/pre/c1-base-arm.json`. The six
survivors, by their defect class (patch anchors in the frozen `R73` table of
`tools/round-74/probe-mutation.py`):

| survivor | what the deletion does |
|---|---|
| `a-drop-genuine-canary` | drops the `not s.get("canary_present")` conjunct, so a canary inside a genuine kernel sample passes |
| `b-unreadable-empty` | turns `OSError` on `/proc/<pid>/environ` into `return {}`, so an unreadable environ reads as empty |
| `b-first-sample-only` | truncates the witness with `[:1]`, keeping only the first kernel sample |
| `b-drop-canary-field` | deletes the `canary_present` line, so samples lose the field entirely |
| `c-swap-verdict-inputs` | calls the verdict with forged and genuine swapped |
| `c-skip-forged-subrun` | replaces the forged sub-run dict with the constant `{"rc": [], "shims": {}, "kernel": {}}` |

## The seams the cases needed

Round 73's selftest could not bind those conjuncts because the probe had no
place to inject a false input. The round-74 probe names three seams
(`tools/round-74/seam-probe.py`):

- **`kernel_witness`** — takes its `/proc` readers as injectable functions
  (`read_argv`, `read_env`, `read_ppid`, `list_pids`) and does one
  deterministic pass when a pid list is injected. A case feeds a fake process
  table and an unreadable environ without touching a real `/proc`.
- **`forged_subrun`** — a separate function taking its spawner and witness, so
  a case runs the forged sub-run under a recording fake spawner and witness.
- **`assemble_arm`** — the wiring that runs the genuine producer, then the
  forged one, then the verdict; its order and arguments are directly
  observable.

## What each declared case binds

The frozen `R74` table of `tools/round-74/probe-mutation.py` declares one case
per mutant; a mutant counts as killed only when the selftest fails and its
`failures` list names that case (`classify`: rc 0 → survived, declared case
absent from `failed` → `killed_wrong_case`, which is no kill).

| survivor | declared case | the case feeds / requires |
|---|---|---|
| `a-drop-forged-detected`, `a-drop-lie-clean`, `a-drop-genuine-rc`, `a-any-forged-sample` | `a12-kernel-cases` | the existing verdict case (the four killed at base) |
| `a-drop-genuine-canary` | `a12-genuine-canary-only` | a genuine git sample with `keys == allow` but `canary_present = true` must force `ok false`, while the canary-free variant stays `ok true` |
| `b-unreadable-empty` | `a12-proc-environ-unreadable` | injected `read_env` returns `None` for pid 11; the witness returns exactly one sample — the readable pid 10 — so an unreadable environ is omitted, never read as `{}`, and a nonexistent pid reads as `None` |
| `b-first-sample-only` | `a12-kernel-multiple-samples` | a deterministic two-pid scan (pids 10 and 11) retains both samples and sees `canary_present` on one |
| `b-drop-canary-field` | `a12-kernel-canary-field` | `canary_present`, `home_under` and `tmpdir_under` are real booleans on every sample |
| `c-swap-verdict-inputs` | `a12-arm-wiring` | recording stubs around `assemble_arm` require the call order `["genuine", "forged"]` and the verdict invoked with the two sides in that order |
| `c-skip-forged-subrun` | `a12-arm-forged-executed` | `forged_subrun` with an injected spawner and witness must actually launch both producers (`git`, `readelf`) and poll the kernel witness once with parents `[9001, 9002]` — the planned-(c) call-site case; a mutant returning the forged dict as a constant dies here, not at the seam-body case |

The case-internal literals (pids 10/11, one witness call, parents
`[9001, 9002]`) are text of the frozen instrument
`tools/round-74/seam-probe.py` selftest, pinned by the r74 target digest below.

## The exact counts, each re-derived

| number | value | receipt |
|---|---|---|
| pristine cases, base arm | 14, `rc 0` | `.ufo/waves/round-74/pre/c1-base-arm.json` → `pristine` |
| killed / survived, base arm | 4 / 6 (names above) | `.ufo/waves/round-74/pre/c1-base-arm.json` → `killed`, `survivors` |
| origin run | killed 4 / survived 6 / inconclusive 0, pristine 14 | `.ufo/waves/round-73/w1/MutProbe/results.json` → `counts`, baseline stdout |
| pristine cases, r74 arm | 20, `rc 0`, `failed []` | `.ufo/waves/round-74/pre/c1-post-at-declaration.json` → `pristine` |
| killed / survivors, r74 arm | 10 killed, each with its `expect_case` in `failed`; `killed_wrong_case []` / 0 survivors | `.ufo/waves/round-74/pre/c1-post-at-declaration.json` → `mutants`, `survivor_count` |
| r74 target pin | expect and measured `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039`, `matched true` | `.ufo/waves/round-74/pre/c1-post-at-declaration.json` → `target_pin`; digest equals the frozen `instruments` pin for `tools/round-74/seam-probe.py` in `.ufo/waves/round-74/claims.json` |
| live A12 (separate evidence) | 12 of 12 arms, `A12_kernel_witness` true | `.ufo/waves/round-73/l1/scores/c1-at-landing.json` |

## Why S278 sits behind `b-unreadable-empty`

The mutant makes an unreadable `/proc/<pid>/environ` behave like an empty
environment. The kernel gates reading that file behind a ptrace access-mode
check: `PTRACE_MODE_READ_FSCREDS` is `PTRACE_MODE_READ` (the level under which
`/proc/pid/environ` is read) combined with `PTRACE_MODE_FSCREDS`, "Use the
caller's filesystem UID and GID (see credentials(7)) or effective capabilities
for LSM checks." (S278, section "Ptrace access mode checking", snapshot lines
1437–1439). An unreadable environ is therefore a permission outcome, not
evidence of an empty environment: the witness must omit the process, and
`a12-proc-environ-unreadable` enforces exactly that. The file-specific binding
— that `/proc/pid/environ` reports the initial `execve(2)` environment and is
subject to that check — is S275; what argv selection can and cannot see is
S277 (the channel rows cited by
`corpus/knowledge/2026-11-04-r73-kernel-witness-record.md`).

## Limits

- **The battery scores `--selftest` only.** It mutates a scratch copy of the
  frozen probe text and reads the selftest's own stdout; it never runs a live
  A12 arm against a real route. A live A12 run is separate evidence —
  `.ufo/waves/round-73/l1/scores/c1-at-landing.json` is what the witness
  observed, and this battery adds nothing to it.
- **A mutation survivor is a test-coverage finding.** It means the selftest
  under-determines the probe code; the fix is a case, never a contract change.
  Weakening the contract to kill a mutant is not licensed by this result, and
  the kill rule in `plans/round-74-claims.md` rejects a kill by any case other
  than the declared one and requires the pristine selftest green at the
  registered case count.
- **Ten classes, not all mutants.** Zero survivors over the ten declared
  classes is a floor on the selftest's discrimination for those classes;
  undeclared defect classes are not scored by this battery.
- **The base arm's target is unpinned** (`target_pin {expect null, matched
  null, pinned false}` in `.ufo/waves/round-74/pre/c1-base-arm.json`): the
  frozen predicate demands only that the base arm name the six survivors; the
  sha256 pin requirement binds the r74 arm.

## Receipts

- `.ufo/waves/round-73/w1/MutProbe/results.json` — the origin: 4 killed,
  6 survived, pristine 14.
- `.ufo/waves/round-74/pre/c1-base-arm.json` — the frozen base arm on the
  landed round-73 probe: same 4/6, the six survivors named.
- `.ufo/waves/round-74/pre/c1-post-at-declaration.json` — the frozen r74 arm:
  10 killed, 0 survivors, pristine 20, target pinned and matched.
- `.ufo/waves/round-74/claims.json` — the frozen instrument pins (r74 probe
  `81d6a432…`, battery `156a9294…`) and the frontier field naming S278.
- `plans/round-74-claims.md` — the frozen predicate, counting command and kill
  rule this entry restates.
