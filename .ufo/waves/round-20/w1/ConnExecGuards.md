# ConnExecGuards

written_at: 2026-10-20T17:53:33-03:00 (`date -Iseconds`, exit 0, clock read immediately before this write)
seat: KaidokuR20.ConnExecGuards-2
installs: none
scope: read-only fleet sweep. No Go binary was executed. Modes come from `stat` only.

## Axes

calibration, coverage, depth

## Proposed move

Point the D3 substance check at two sets, and keep them separate in the guard record and in the QUALITY admission.

1. Armed set (already witnessed): the 20 `go-1.24.6` paths in `manual-arm.json`. Live mode matches `mode_after` `0o644` on every path (missing 0, mismatch 0). The file records `exec_probe` PermissionError errno 13 for `bin/go`. This seat did not re-run that probe.
2. Unarmed remainder, still named by the prohibition: `go-1.25.0` and `go-1.27.3`. Both trees are mode `0o755` on every regular file in `bin/` and `pkg/tool/linux_amd64/`. `go-1.25.0` is the round-19 carrier set, and `InstallRecordDraft.md:26` executed `bin/go version` on both `go-1.24.6` and `go-1.25.0`.

L1 choice, either branch: add the still-`0o755` paths to the carrier-guard manifest, or write them in the same admission as an explicit unarmed remainder. Replaying only `manual-arm.json` leaves `go-1.25.0/bin/go` able to repeat the routed breach. Sibling phrase hits are the wrong mechanism to import (classes below).

## Affected axes

- Calibration. C1 is falsified by a token-only closure (`claims.json` C1 `falsified_if`). `manual-arm.json` closes executability for `go-1.24.6` only. The routed defect is lesson row 5 (`corpus/lessons/round-19.md:90`): execution happened, and SHA-256 does not detect it. The four-phrase grep also cannot see the prohibition that failed.
- Coverage. No sibling corpus or contract holds a carrier exec-bit guard to cross-cite. The only sibling mention of these three trees is a footprint note marked unrelated (`kama-shokunin/.ufo/waves/round-17/build/advice/ScoutInstallFootprint.md:36`).
- Depth. Unharmed if the remainder stays visible. Byte reads still work at mode `0644`. The contract's loader-mapped bypass (`ld-linux … <file>`, round-20 `contract.md:51-52`) stays a limit on the armed set too. This move does not call `0o644` a complete execution ban.

## Evidence

### Assigned commands

Working directory `/home/vgpnk/Projects/shokunin`. Pattern `noexec\|chmod a-x\|carrier execution\|do not execute`.

- `grep -ril '…' */corpus` at 2026-10-20T17:47:48-03:00, exit 2. Hits were printed, and the shell glob `*` also expands to files and to a directory whose name is `'bash: '` (trailing space, `os.listdir` repr). Grep then reports `AXES.md/corpus`, `CORPUS.md/corpus`, `LEARNING.md/corpus`, `LOG.md/corpus`, `MANIFEST.json/corpus`, `MISSION.md/corpus`, `PROTOCOL-APPENDIX.md/corpus`, `PROTOCOL.md/corpus`, `README.md/corpus`, `ROADMAP.md/corpus`, `SCORECARD.md/corpus`, `shokunin.conf/corpus` as "Not a directory", and `bash: /corpus`, `local/corpus`, `reports/corpus`, `research/corpus`, `scripts/corpus`, `tameshi-shokukin/corpus`, `templates/corpus` as missing. `ls -d */corpus` in the same command also exited 2.
- `grep -ril '…' */.ufo/waves/*/contract*.md`, same clock, exit 1. The glob is 5 files (`ls` exit 0): kaidoku round-17, round-18, round-19, round-20, and `mori-shokunin/.ufo/waves/round-17/contract.md`.
- Case-insensitive line sweep on real `*-shokunin/corpus` directories, `--exclude-dir=node_modules`, at 2026-10-20T17:49:30-03:00, exit 0. Tokens and per-lane file counts below.
- `grep -n -i` of the same pattern on the 5 contract files, same clock, exit 1.

### Corpus hits (observation)

Per-lane file counts, `-i`, node_modules excluded: audio 1, chousa 1, kaidoku 4, mado 2, mori 2, souji 1, tsukuroi 1. Zero files: game-dev-2d, game-dev-3d, kagi, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, revenger, tabi, tameshi. 21 corpus dirs. The literal `*/corpus` run also listed two tabi playwright files under `node_modules` (excluded from these counts).

| class | anchor | token |
|---|---|---|
| parse-not-import comment | `audio-shokunin/corpus/live/r89-simplifier/proofs/callsite-dump.py:55` | do not execute the module |
| broken markdown-table command | `chousa-shokunin/corpus/knowledge/archived-export-intake.md:197` | do not execute it literally |
| REA inspect-verb claim | `kaidoku-shokunin/corpus/knowledge/2026-10-13-rea-cli-surface.md:94` | do not execute/load the target |
| static-inspection recheck | `kaidoku-shokunin/corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md:7` | do not execute the inspected image |
| measurement limit | `kaidoku-shokunin/corpus/lessons/2026-10-15-round-1.md:37` | fresh carrier execution |
| routed defect | `kaidoku-shokunin/corpus/lessons/round-19-verifier-spotcheck.md:184-185` | carrier execution (no enforcement) |
| round-scoped tool ban | `mado-shokunin/corpus/knowledge/input-debugging-boundaries-r15.md:74` | do not execute here (`libinput`) |
| round-scoped tool ban | `mado-shokunin/corpus/knowledge/waybar-observation-boundaries-r16.md:61` | Do not execute `exec` / `exec-if` |
| cgroup2 mount flag | `mori-shokunin/corpus/knowledge/oom-kill-counter-kernel-only-r12.md:15` | `noexec` inside mount options |
| same mount flag, repeated | `mori-shokunin/corpus/evidence/drift-r12-20261019T2204Z-classification.md:55` | `noexec` |
| quoted bash `set -n` | `souji-shokunin/corpus/lessons/round-16.md:26` | do not execute them |
| systemd.exec(5) section name in a citation | `tsukuroi-shokunin/corpus/SOURCES.md:102` | `NoExecPaths=` |
| vendor dry-run help | `tabi-shokunin/corpus/evidence/round-13/aria/node_modules/playwright-core/lib/coreBundle.js` and `…/cli-client/help.json` | "do not execute installation" |

`NoExecPaths=` is a systemd unit sandbox directive cited as a man-page heading. It is adjacent to the sandbox-pattern seat, and it does not clear mode bits on a toolchain tree. The mori `noexec` flag is on `cgroup2` at `/sys/fs/cgroup`, which is a different filesystem from `~/.local/opt`.

### What the phrase sweep misses (observation)

The prohibition that round 19 violated is a different sentence, present only in kaidoku contracts:

- `kaidoku-shokunin/.ufo/waves/round-17/contract.md:6` — "Never execute a carrier binary."
- `kaidoku-shokunin/.ufo/waves/round-18/contract.md:10` and `:102` — the same sentence; carriers "never executed".
- `kaidoku-shokunin/.ufo/waves/round-19/contract.md:39` — "Never execute a carrier binary." Carriers named at `:41-42`: `go-1.25.0/bin/{go,gofmt}` and `pkg/tool/linux_amd64/{asm,cgo,compile,cover,link,preprofile,vet}`.

`grep -rI -n -H 'Never execute a carrier'` across `*-shokunin/corpus` and `*-shokunin/.ufo/waves/*/contract*.md` at 2026-10-20T17:51:50-03:00, exit 0, printed only those three kaidoku lines.

Round-20's mechanical words are also outside the four phrases (`grep -n -i -E 'exec bit|exec-free|never execute|…'` on round-20 `contract.md`, exit 0):

- `:47-48` arm "clears every exec bit"; check requires modes "still exec-free".
- `:50-52` selftest `exec_refused` expects PermissionError on execve; declared limit is loader-mapped execution.
- `:88-89` exec bits cleared applies to the `go-1.24.6` tree, record `W20/evidence/carrier-guard/manual-arm.json`.
- `:90` "NEVER execute any Go toolchain binary (1.24.6, 1.25.0, 1.27.3)".

The only sibling contract in the assigned glob, `mori-shokunin/.ufo/waves/round-17/contract.md:154`, says the L1 "executes final checks" and assignments "forbid test execution." That is seat-test prose. It matched neither the four phrases nor `Never execute a carrier`.

### Live modes (observation)

Script at 2026-10-20T17:51:50-03:00, exit 0. `manual-arm.json`: `action` manual-arm, `taken_at_utc` 2026-10-20T20:37:00+00:00, 20 carriers, every `mode_before` `0o755`, every `mode_after` `0o644`. Prefix check at 2026-10-20T17:53:33-03:00, exit 0: 0 paths outside `go-1.24.6`; 2 under `bin/`, 18 under `pkg/`. `exec_probe` at `manual-arm.json:166-170`: path `…/go-1.24.6/bin/go`, result PermissionError, errno 13.

Live directories (regular files, any exec bit = mode `& 0o111`):

| tree | bin | linux_amd64 tools | exec-bit files |
|---|---|---|---|
| go-1.24.6 | 2, both `0o644` (`go`, `gofmt`) | 18, `any_exec_bit=0` | 0 |
| go-1.25.0 | 2, both `0o755` (`go`, `gofmt`) | 7, all `0o755`: asm, cgo, compile, cover, link, preprofile, vet | 9 |
| go-1.27.3 | 2, both `0o755` (`go`, `gofmt`) | 8, all `0o755`: asm, cgo, compile, cover, fix, link, preprofile, vet | 10 |

The `go-1.25.0` names match round-19 `contract.md:41-42`. `go-1.27.3` adds `fix` and is outside that carrier list. It is inside the round-20 `:90` prohibition and outside the arm record.

Breach record: `kaidoku-shokunin/.ufo/waves/round-19/w1/InstallRecordDraft.md:26` ran `~/.local/opt/go-{1.24.6,1.25.0}/bin/go version`, exit 0 each. `:27` records `command -v go` exit 1. Repeated at 2026-10-20T17:52:32-03:00: `command -v go` exit 1 (no PATH `go`). Spotcheck ruling at `round-19-verifier-spotcheck.md:96-99`: disclosed process defect, output stayed in the install record. Lesson fix cell at `round-19.md:90`: "No demonstrated enforcement fix."

### Worktree contracts outside the glob (observation)

At 2026-10-20T17:52:32-03:00, 10 files match `mori-shokunin/.ufo/worktrees/round-17/*/.ufo/waves/round-17/contract.md`. Primary sha256 `045a7de7217e635aed992adcc2727bddf5d70b24aedf9877194305dd3cd39621`. Three copies match it (FinalVerification, FinalVerificationFixed, FinalVerificationMetadata). Seven share prefix `3304aff7200f` and differ. Assigned `*/.ufo/waves/*/contract*.md` does not search `.ufo/worktrees`.

Phrase grep of that worktree glob at 2026-10-20T17:52:45-03:00 exited 2: `FinalChecks/.ufo/waves/round-17/contract.md` was in the expansion and missing at open. No phrase line was printed. On the differing hash class, `JjGate/…/contract.md` has no `never execute|exec bit|chmod|carrier` (exit 1) and the paired `execute` grep printed only primary `:154`.

## Risks

- Arming `go-1.25.0` or `go-1.27.3` changes a shared install. PATH has no `go` (exit 1, now and at InstallRecordDraft `:27`). One sibling file calls the three trees unrelated. This sweep did not prove that no absolute-path caller remains. [INFERENCE] chmod there can still break an unlisted caller. The unarmed-remainder branch avoids that chmod and can be misread as shrinking `:90` unless the prohibition text stays and the enforcement label is separate.
- `0o644` does not stop loader-mapped execution. The contract already states that limit (`:51-52`). Citing the arm record as a full ban overclaims depth.
- A later gate that copies `grep -ril … */corpus` from the fleet root will exit 2 on glob noise even when corpus hits exist. Directory arguments are required before that exit code means "no match" (exit 1) or "hits" (exit 0).
- Worktree churn: `FinalChecks` vanished during the phrase grep. Those copies were not re-listed after the error.
- Mori line `oom-kill-counter-kernel-only-r12.md:21` says a userspace killer "does not execute" kernel accounting calls. The four-phrase pattern does not match that word order. It is OOM accounting, not a carrier control.

## Verification

Without executing a Go binary:

- Re-stat `go-1.24.6`, `go-1.25.0`, and `go-1.27.3` `bin/` and `pkg/tool/linux_amd64/`. Expect the armed 20 paths at `0644` and the other two trees at `0755`, unless the L1 has since armed them.
- When `carrier-guard.py` exists, its manifest either lists the `go-1.25.0` round-19 names plus the named `go-1.27.3` files, or the D3 admission lists those paths as unarmed. A check JSON that only repeats `manual-arm.json` leaves the breach tree out of the finding set.
- Confirm the admission does not treat presence of `do not execute`, `noexec`, `chmod a-x`, or `carrier execution` as the guard. Those strings are absent from round-20 `contract.md` (exit 1) and present in the false-friend rows above.
