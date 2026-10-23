# R30 W2 — ReRunC2 (re-run frozen C2 counter + selftest at the measured revision; C2 separability)

Seat: `KaidokuR30.ReRunC2`. The only C2 measure-mode / mutant REA runner this wave. All runs were sequential.

## Verdicts

- **C2 re-run at 92b1dd2ddc119fda89a611ba515bdf6cfe906f76: holds.** The live counter printed the frozen target line `mutants=19 matches=19 target=19 entry_ok=1 (ok) skill_ok=1 (ok)` and exited 0 (observation).
- **C2 selftest: holds.** It printed `selftest cases=16 failures=0` and exited 0 (observation).
- **C2 separability from C1: holds.** A sandbox commit that deletes the C1 envelopes, the C1 `runs.tsv`, the C1 entry and the PROVINCE round-30 section still prints the same target line and exits 0. Its stdout is byte-identical to the measured-revision run (same sha256) (observation).
- **Shared mutants: unchanged.** Before, between and after the two measure runs, all 19 files in `/fast/scratch/hyaku/kaidoku-r30/mutants` hashed identically (`diff` of the sha256 lists was empty). Each build printed `pin_mismatch=0` (observation).

No actionable finding remains in scope.

## Setup

- Clone: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/clone`, then `git checkout -q --detach 92b1dd2ddc119fda89a611ba515bdf6cfe906f76`. HEAD is `92b1dd2ddc119fda89a611ba515bdf6cfe906f76`. GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE were unset for every command. The only `GIT_*` variables in the environment were GIT_EDITOR, GIT_PAGER and GIT_TERMINAL_PROMPT.
- Pins: the counter is `clone/tools/round-30/c2-rust-refusals.py`, sha256 `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b`; the oracle is `rust_dep_oracle.py`, sha256 `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d`. Both files are identical in clone and clone2. The REA package.json version is `6.5.0`, node is `v24.21.0`, and the base carrier `elf-x86_64-uvx` has sha256 `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d` and attribute `----i-----` (immutable).
- Mutant attributes before the runs: mode 0444, no `chattr` flags, mtime `2026-10-23 00:08 -0300`. After the runs the mtime is `00:12:49 -0300`, because the counter's build step rewrote them. The bytes are identical (see below).
- REA runs went through the counter's own `subprocess.run(... cwd="/tmp")`, with `TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/tmp`. The only thing written to that directory was `node-compile-cache/`.

## Run 1 — measure mode at the measured revision

Command, from `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2`:

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/tmp timeout 900 python3 -I -B clone/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/clone --rev 92b1dd2ddc119fda89a611ba515bdf6cfe906f76
```

UTC start `2026-10-23T03:12:49Z`, end `2026-10-23T03:13:07Z`. **Exit 0.** Stderr was empty.

Full stdout:

```
mutants=19 rebuilt pin_mismatch=0
g-relocated	ok	P2-match	accepted, packages=584
g-recompressed	ok	P2-match	accepted, packages=584
g-no-root	ok	P2-match	accepted, packages=584
r-empty	refuse	P2-match	refused with predicted message
r-nobits	refuse	P2-match	refused with predicted message
r-compressed-flag	refuse	P2-match	refused with predicted message
r-two-sections	refuse	P2-match	refused with predicted message
r-not-zlib	refuse	P2-match	refused with predicted message
r-trailing-bytes	refuse	P2-match	refused with predicted message
r-over-1mib	refuse	P2-match	refused with predicted message
r-inflate-ratio	refuse	P2-match	refused with predicted message
r-not-utf8	refuse	P2-match	refused with predicted message
r-bad-json	refuse	P2-match	refused with predicted message
r-nesting-33	refuse	P2-match	refused with predicted message
r-format-negative	refuse	P2-match	refused with predicted message
r-extra-field	refuse	P2-match	refused with predicted message
r-kind-dev	refuse	P2-match	refused with predicted message
r-two-roots	refuse	P2-match	refused with predicted message
r-index-outside	refuse	P2-match	refused with predicted message
mutants=19 matches=19 target=19 entry_ok=1 (ok) skill_ok=1 (ok)
```

This matches the frozen target line `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1` with exit 0 (observation). The counter gives a `P2-match` only after the live run agrees with the committed envelope at the revision (ok flag and evidence_id) and that envelope was first added after the claims.json freeze, per `committed_agrees` in the counter. Every row passed that gate.

## Run 2 — selftest

Command: `timeout 120 python3 -I -B clone/tools/round-30/c2-rust-refusals.py --selftest`. UTC start `2026-10-23T03:13:12Z`. **Exit 0.**

Full stdout:

```
ok green-refusal-matches got=P2-match (refused with predicted message)
ok green-acceptance-matches got=P2-match (accepted, packages=1)
ok red-do-nothing got=P2-miss (predicted message absent)
ok red-accepted-when-refusal-predicted got=P2-miss (accepted, refusal predicted)
ok red-other-message got=P2-miss (predicted message absent)
ok red-empty-predicted-message got=P2-miss (predicted message absent)
ok red-refused-when-acceptance-predicted got=P2-miss (not accepted (exit 1))
ok red-accept-wrong-packages got=P2-miss (package multiset differs)
ok red-accept-wrong-offset got=P2-miss (offset/size differ)
ok red-accept-wrong-subject got=P2-miss (subject sha256)
ok green-committed-agrees got=True (ok)
ok green-committed-refusal-agrees got=True (ok)
ok red-committed-absent got=False (committed envelope absent or not added after the freeze)
ok red-committed-before-freeze got=False (committed envelope absent or not added after the freeze)
ok red-committed-ok-differs got=False (committed ok False != live ok True)
ok red-committed-id-differs got=False (committed evidence_id differs)
selftest cases=16 failures=0
```

## Run 3 — separability

Second clone: `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/clone2`, cloned the same way and detached at `92b1dd2ddc119fda89a611ba515bdf6cfe906f76`.

Deletions:

- `git rm -q -r corpus/evidence/round-30/c1/envelopes corpus/evidence/round-30/c1/runs.tsv corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`. This removed 32 envelope files, `runs.tsv` and the C1 entry.
- `PROVINCE.md`: removed the whole `## Round-30 \`inspect-rust-binary\` positive class and refusal signatures — 2026-10-23` section, plus the blank line before it. That is old lines 329–340; the file went from 340 to 328 lines. The section runs to EOF and also contains the R29-C1 carrier-provenance correction paragraph, which was removed with it. `grep -c Round-30 PROVINCE.md` afterwards gave `0`.
- `corpus/evidence/round-30/c1/carriers.tsv` and `pypi-uv-0.13.0.json` were left in place, since they were not in the assignment.

Sandbox commit: `git -c user.name=ctl -c user.email=ctl@sandbox commit` produced **`0b78689b6d566a36806707c95f45792adef2deae`**. `git diff --stat 92b1dd2d HEAD` reported `35 files changed, 126 deletions(-)`, and the working tree is clean.

Command:

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/tmp timeout 900 python3 -I -B clone2/tools/round-30/c2-rust-refusals.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/clone2 --rev 0b78689b6d566a36806707c95f45792adef2deae
```

UTC start `2026-10-23T03:14:07Z`, end `2026-10-23T03:14:21Z`. **Exit 0.** Stderr was empty. The stdout is byte-identical to Run 1 (sha256 `a6c37c721f237b8897df43ee0e0259860a6380c5116649fe5e7ea90aea0f81dc` for both). Its last line is:

```
mutants=19 matches=19 target=19 entry_ok=1 (ok) skill_ok=1 (ok)
```

**Separability verdict: holds** (observation). With the C1 evidence, C1 entry and PROVINCE round-30 section removed, C2 still meets its frozen target.

Supporting reads, all from `clone2` (observation):

- The C2 entry `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` and the C2 counter contain no reference to `r30-rust-auditable-positive`, `c1/envelopes` or `c1/runs` (Grep tool, no match).
- The SKILL.md lines that satisfy `skill_ok` are not shared with C1. Line 970 is the only one: it contains `inspect-rust-binary` and the C2 entry, is not at base `d210fb8f`, and does not name the C1 entry. Line 968 names both entries but is not the line that passes `skill_ok`. I found this with a read-only `python3 -I -B -c` scan using the same filter as `skill_ok()`.

## Residual risk and verification gaps

- **C2 still reads `c1/carriers.tsv` (observation from the code).** `CARRIERS = "corpus/evidence/round-30/c1/carriers.tsv"`, and `base_carrier()` reads it from the working tree rather than with `git show` at `--rev`. So C2 is separable from the C1 *results* but still pins its base carrier through the C1 carrier list. The assignment did not delete that file, so this run did not test separability from it. The risk is bounded: the base carrier is checked against the row's full sha256 and the prefix `2e9105ad94813196`, and every mutant is checked against its frozen full sha256 in `predictions.tsv` (`pin_mismatch=0`) (inference).
- **SKILL.md line 968 (the C1 positive-class line) was not removed**, since that was not in the assignment. The scan above shows C2's `skill_ok` does not depend on it (observation); no counter run was made with it removed.
- Running the counter in measure mode rewrites the shared mutant files: mtime changed and bytes stayed identical. Any seat comparing mutant mtimes will see `2026-10-23 00:12:49 -0300` (03:12:49Z) or `00:14:07 -0300` (03:14:07Z) from these runs (observation).
- I made no REA runs outside the counter and did not execute any carrier or mutant.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC2/`)

| File | sha256 |
|---|---|
| `measure.stdout` | `a6c37c721f237b8897df43ee0e0259860a6380c5116649fe5e7ea90aea0f81dc` |
| `measure.stderr` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `selftest.stdout` | `fa6330a447c67b5b31285e56adb811ed5a833ae42941bc2278cafd7b10d16573` |
| `separability.stdout` | `a6c37c721f237b8897df43ee0e0259860a6380c5116649fe5e7ea90aea0f81dc` |
| `separability.stderr` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `separability-province.diff` | `3c55c37abf5001da3a627e2fff5baa26f2ceff133e3b421243ab25fb2d6842bd` |
| `separability-name-status.txt` (35 deletions) | `74d98fd5dbac63e9f817ce6a020a14685cf58114144fc1d1f927f52bb3ebd883` |
| `mutants-pre.sha256` / `mutants-post1.sha256` / `mutants-post2.sha256` | `cca8363d843638859c2694e5169b6ff8ce09b23a0ff596493053d61b85590fa7` (all three identical) |
| `clone/` | detached at `92b1dd2ddc119fda89a611ba515bdf6cfe906f76`, clean |
| `clone2/` | sandbox commit `0b78689b6d566a36806707c95f45792adef2deae`, clean |
| `tmp/` | REA `TMPDIR` (only `node-compile-cache/`) |

## Process, bounds and tooling

- `pgrep -af 'rea-agents|c2-rust-refusals'` printed `no-procs` at `2026-10-23T03:14:36Z`, so no processes are left running.
- I made no lane writes other than this report, no git or jj writes in the lane or fleet repo, and sent no messages.
- No tools were installed or updated. `npx` used the already-cached `rea-agents@6.5.0`.
