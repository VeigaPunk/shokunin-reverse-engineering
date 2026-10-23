# R30 wave 2 — ReRunC1 (fresh-clone re-run of the frozen C1 counter)

Seat: KaidokuR30.ReRunC1. Attack: does the frozen R30-C1 counter, run live in a fresh
sandbox clone at measured revision 92b1dd2ddc119fda89a611ba515bdf6cfe906f76, reproduce the
target line and the committed after-receipt?

**Verdict: holds.** The fresh-clone live run printed
`carriers=16 pass=16 target=16 entry_ok=1 (ok) province_ok=1 (ok)` with exit 0, which
meets the frozen target line `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`. The
selftest printed `selftest cases=25 failures=0` with exit 0. The live stdout is
byte-identical to the committed receipt once that receipt's trailing `exit=0` line is
removed. One low-severity finding about selftest coverage is below; it does not change
the measured result.

## Setup (observation)

| Step | Command | Exit | UTC |
|---|---|---|---|
| clone | `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC1/clone` | 0 | 2026-10-23T03:12:18Z |
| checkout | `git -C clone checkout -q --detach 92b1dd2ddc119fda89a611ba515bdf6cfe906f76` (GIT_* unset) | 0 | 2026-10-23T03:12:18Z |
| verify | `git -C clone rev-parse HEAD` → `92b1dd2ddc119fda89a611ba515bdf6cfe906f76`; `git status --porcelain` → empty (before and after the runs) | 0 | 2026-10-23T03:12:18Z |

- GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE were unset for every git command and for both counter runs. Only GIT_EDITOR, GIT_PAGER and GIT_TERMINAL_PROMPT remained in the environment; none of them redirects the repository (observation).
- `TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC1/tmp`. Python 3.14.8, git 2.56.0, node v24.21.0.
- REA package used by the counter: `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`, version `6.5.0`, sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` (observation).
- Pinned inputs are unchanged since the freeze. `git diff --stat 4ee65c67 92b1dd2d -- corpus/evidence/round-30/c1/carriers.tsv tools/round-30/c1-rust-positive.py tools/round-30/rust_dep_oracle.py` printed nothing (exit 0, 2026-10-23T03:13:37Z). The counter at 92b1dd2d and at instrument commit 0dbabf78 have the same sha256, `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` (observation).
- Before running, I read the counter source. Measure mode without `--write-evidence` performs no file writes; it only reads carriers, runs REA with cwd `/tmp`, and runs read-only `git show` and `git log` (observation, `c1-rust-positive.py` lines 207–267).

## Selftest — full stdout (observation)

Command: `timeout 900 python3 -I -B clone/tools/round-30/c1-rust-positive.py --selftest`
Exit: **0**. UTC: 2026-10-23T03:12:40Z. Stderr: empty.

```
ok green-exact got=P1-pass (packages=2 edges=1)
ok green-reordered-indices got=P1-pass (packages=2 edges=1)
ok red-do-nothing got=P1-fail (envelope not ok)
ok red-nonzero-exit got=P1-fail (exit 1)
ok red-not-ok got=P1-fail (envelope not ok)
ok red-other-operation got=P1-fail (operation 'inspect_go_binary')
ok red-subject-mismatch got=P1-fail (subject sha256 'x')
ok red-null-metadata got=P1-fail (auditable_metadata count 1 or null)
ok red-empty-packages got=P1-fail (package multiset differs (rea 0, oracle 2))
ok red-empty-oracle got=P1-fail (oracle list empty)
ok red-version-differs got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-edge-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-kind-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-root-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-duplicate-package got=P1-fail (package multiset differs (rea 3, oracle 2))
ok red-offset-differs got=P1-fail (file_offset 101 != 100)
ok red-size-differs got=P1-fail (compressed_bytes 49 != 50)
ok green-committed-agrees got=True (ok)
ok red-committed-absent got=False (committed envelope absent or not added after the freeze)
ok red-committed-before-freeze got=False (committed envelope absent or not added after the freeze)
ok red-committed-same-commit-as-freeze got=False (committed envelope absent or not added after the freeze)
ok red-no-freeze-commit got=False (no freeze commit)
ok red-committed-id-differs got=False (committed evidence_id 'ev_2' != live 'ev_1')
ok red-committed-packages-differ got=False (committed metadata shape)
ok red-entry-lacks-id got=False (entry does not name ev_1)
selftest cases=25 failures=0
```

## Measure — full stdout (observation)

Command: `timeout 900 python3 -I -B clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC1/clone --rev 92b1dd2ddc119fda89a611ba515bdf6cfe906f76`
Exit: **0**. UTC: 2026-10-23T03:12:40Z to 2026-10-23T03:13:01Z. Stderr: empty.

```
elf-x86_64-uv	P1-pass	packages=584 edges=3041
elf-x86_64-uvx	P1-pass	packages=584 edges=3041
elf-aarch64-uv	P1-pass	packages=584 edges=3042
elf-aarch64-uvx	P1-pass	packages=584 edges=3042
elf-riscv64-uv	P1-pass	packages=580 edges=3030
elf-riscv64-uvx	P1-pass	packages=580 edges=3030
pe-x86_64-uv	P1-pass	packages=596 edges=3013
pe-x86_64-uvx	P1-pass	packages=596 edges=3013
pe-x86_64-uvw	P1-pass	packages=596 edges=3013
pe-arm64-uv	P1-pass	packages=596 edges=3012
pe-arm64-uvx	P1-pass	packages=596 edges=3012
pe-arm64-uvw	P1-pass	packages=596 edges=3012
macho-x86_64-uv	P1-pass	packages=573 edges=2974
macho-x86_64-uvx	P1-pass	packages=573 edges=2974
macho-arm64-uv	P1-pass	packages=573 edges=2975
macho-arm64-uvx	P1-pass	packages=573 edges=2975
carriers=16 pass=16 target=16 entry_ok=1 (ok) province_ok=1 (ok)
```

## Comparison with the committed receipt (observation)

- Receipt: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/after/c1-rust-positive-at-92b1dd2d.txt`, sha256 `9920a11a27f537075270380684053b6a24beb055363b193aa242f519935ee7a2`, last touched by lane commit `3502b94c`.
- `grep -v '^exit=' <receipt> | diff - measure.stdout` printed nothing (diff exit 0, 2026-10-23T03:13:01Z). All 16 per-carrier rows, including verdicts and the package and edge counts, match. The summary line matches too. The receipt's `exit=0` line matches the live exit code 0.
- Target line: the live summary carries `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, with only the `(ok)` reason annotations added. **Target MET.**

## Carrier integrity (observation)

- All 16 carrier paths have the immutable attribute (`lsattr` shows `----i-----`).
- I took `sha256sum` of all 16 carriers before and after the runs. `cmp carriers-sha-before.txt carriers-sha-after.txt` returned exit 0, and the after-hashes equal the frozen `sha256` column of `carriers.tsv` (diff exit 0). No carrier was executed or written.

## Findings by severity

**Low — the selftest does not guard the committed-envelope package-multiset check.** In `tools/round-30/c1-rust-positive.py`, the comparison at lines 198–199 (`if rea_tuples(metas[0]) != tuples: return False, "committed package multiset differs"`) is never reached by the selftest.
- Evidence (observation): the red case `red-committed-packages-differ` (line 320) uses `env(packages=[dict(pk[0])])`. That package keeps `dependencies: [1]` while only one package exists, so `rea_tuples` raises `IndexError` and the case is rejected for `committed metadata shape` (see the selftest stdout above). The selftest compares only the boolean result, never the reason.
- Counterexample (observation): a scratch copy with lines 198–199 replaced by a bare `rea_tuples(metas[0])` call (`mut/mutant.diff`) still printed `selftest cases=25 failures=0`, exit 0, at 2026-10-23T03:13:23Z. Its stdout is byte-identical to the unmutated selftest (both sha256 `bd5dfdc1…`).
- Impact (inference): the live measure is not affected, since all 16 committed envelopes passed `committed_check`. However, a future regression that drops this P1 clause ("its committed envelope … carries the same … package multiset") would pass the selftest unnoticed. A shape-valid fixture, for example `[dict(pk[0], dependencies=[]), dict(pk[1])]`, would exercise the branch.
- Cosmetic (observation): line 323, `ccases[6][0]  # keep tuple layout explicit`, is a no-op expression statement.

No other actionable finding in scope.

## Residual risk and verification gaps

- I did not inspect the REA envelopes from this run: measure mode keeps them in memory, and I did not use `--write-evidence`. The comparison covers the counter's printed verdicts, not envelope bytes (unknown beyond the counter's own checks).
- The independent oracle `rust_dep_oracle.py` was used as is. I did not re-derive the `.dep-v0` decoding; other seats own that.
- The godspeed skill named in the assignment does not exist anywhere on this host. `find / -xdev -type d -name godspeed` returned nothing (2026-10-23T03:12Z), so it could not be read.
- Installs or updates: none. The npx cache already held rea-agents 6.5.0.
- No processes left running: `pgrep -af rea-agents` was empty after the runs.

## Scratch artifacts (/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReRunC1/)

| File | sha256 |
|---|---|
| selftest.stdout | bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18 |
| selftest.stderr (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| measure.stdout | b913d0755dc7d124b8a976a6927ae92d604d5412235c12b7ed358e4b4bafac4c |
| measure.stderr (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| carriers-sha-before.txt | 856aa77ee42fe2aa9952996732e18aeb89d64af326999fe9d0f4c99b2cc01867 |
| carriers-sha-after.txt | 856aa77ee42fe2aa9952996732e18aeb89d64af326999fe9d0f4c99b2cc01867 |
| paths.txt | 8f1dea5eb07e90cb43fc7f2728228997fcf18957861bc5b190c1467fee18b758 |
| mut/c1-rust-positive.py (mutant) | 079c7265257bad34dde90d4c85a7a032162e7834e460da1e30b6cdc142540aa6 |
| mut/rust_dep_oracle.py (unmodified copy) | f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d |
| mut/mutant.diff | 648891d021b47686f94ed8d145c875d8ecf8de23ed4ec389f15a888d338fcb36 |
| mut/mutant-selftest.stdout | bd5dfdc1fcf6cb3b08f2e02ad9c4feb38c1a5e5e4d806c443a1c2a8f9f769e18 |
| clone/ (checkout at 92b1dd2d; counter e07563d6…, oracle f0b144c6…, carriers.tsv c968cd1e…) | — |
