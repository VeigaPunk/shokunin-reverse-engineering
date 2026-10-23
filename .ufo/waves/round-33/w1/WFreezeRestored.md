# WFreezeRestored — committed change followed by exact restoration

## Scope, axes, and result

- Axes: **evidence integrity / history-sensitive detector depth**, **reproducibility**, and **isolation / exact restoration**. These are probe axes, not new lane claims or an admission score.
- **Mutant killed.** The pristine fixture was CLEAN (exit **0**); the committed one-byte mutation failed (exit **1**); its later exact-byte restoration also failed (exit **1**) because both post-freeze touching commits remained visible.
- R33-C1 remains **stopped / unprovable** under `.ufo/waves/round-33/claim-stop.json`. This is one independent, text-only instrument probe, not a replacement benchmark, carrier row, revived claim, or promotion judgment.
- Probe UTC: **2026-10-23T09:33:06.706390+00:00 → 2026-10-23T09:33:06.827315+00:00**. No timeout or probe error was recorded.

## Source and measured revision

Observed lane HEAD from the initial read-only `git rev-parse HEAD` call was `d7076120e4f00c6d18aa77b8764d14861e820eb2` (context base: `428315a8f5674b952def862910af6e07a6c2224b`). The probe executed the installed, unmodified file:

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/freeze-integrity.py`

The probe's separately captured command

```text
/usr/bin/git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show d7076120e4f00c6d18aa77b8764d14861e820eb2:tools/round-33/freeze-integrity.py
```

returned exit 0, empty stderr, and the full source in `receipt.json` (`label=pinned-gate-source`), during `09:33:06.709299+00:00 → 09:33:06.711127+00:00` on the same date.

Installed-source SHA-256 before, pinned Git-source SHA-256, and installed-source SHA-256 after were all:

```text
a753b1d70ce8d7062fe9ffae8a31d90eb21fe26c30649d51bd95bd68ad656bb2
```

Expected detector behavior was fixed by that source, not repaired after observing results: lines 258–267 discover the claims-adding freeze and read its pins; lines 270–274 require both matching Git-object digest and an empty `freeze..rev` touching history (`ok = got == digest and not touched`). Thus digest restoration alone must not make this fixture CLEAN.

## Independent fixture and full retained recipe

All fixture/code/receipt artifacts are confined to:

`/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/`

- Full executed recipe and bounded process runner: `probe.py`.
- Recipe SHA-256 recorded at execution: `ac16d35b7c2abe95e0685945f785389b12052606f436df0cc172ecc08ed5052c`.
- Full actual direct-child argv, cwd, UTC start/end, duration, stdout/stderr, exit, timeout flag, output digests, and process-group cleanup: `receipt.json`.
- Retained tiny Git repository: `fixture/`.
- Empty Git initialization template: `empty-template/`.

The fixture is not executable code or a carrier fixture. Its complete initial payload at `config/guard.txt` was the 14 bytes `b'frozen_mode=0\n'`. Its sole mutation changed ASCII `0` to `1` at zero-based offset **12**, producing `b'frozen_mode=1\n'`. Both byte strings and the mutation offset are recorded in the receipt. The original bytes were restored in a third commit, not by rewriting history.

The complete initial `.ufo/waves/round-99/claims.json` (141 bytes, including the trailing newline) was:

```json
{
  "frozen_inputs": {},
  "instruments": {
    "config/guard.txt": "e0592e451ebbe2164d62e786892c2c831b53633328286ea97dbab361a58b984a"
  }
}
```

Round 99 is an artificial namespace inside this private fixture only. No production claims file was created or changed.

The recipe creates the fixture and empty-template directories exclusively; then every fixture Git invocation uses this common argv prefix:

```text
/usr/bin/git -C /fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/fixture -c user.name=WFreezeRestored -c user.email=WFreezeRestored@example.invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null -c core.autocrlf=false -c gc.auto=0 -c core.fsmonitor=false
```

The ordered fixture-Git argv suffixes actually used were:

```text
init -q --initial-branch=main --object-format=sha1 --template=/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/empty-template
add -- config/guard.txt .ufo/waves/round-99/claims.json
commit -q --no-gpg-sign -m 'freeze: pin independent guard bytes'
rev-parse HEAD HEAD:config/guard.txt
[run unchanged detector on pristine bytes]
[write b'frozen_mode=1\n' to config/guard.txt]
add -- config/guard.txt
commit -q --no-gpg-sign -m 'mutation: flip one pinned guard byte'
rev-parse HEAD HEAD:config/guard.txt
[run unchanged detector on mutated bytes]
[finally: write b'frozen_mode=0\n' to config/guard.txt]
add -- config/guard.txt
commit -q --no-gpg-sign -m 'restore: exact frozen guard bytes'
rev-parse HEAD HEAD:config/guard.txt
[run unchanged detector on restored bytes]
log --reverse --format=%H%x09%P%x09%s -- config/guard.txt
```

Bracketed lines describe Python recipe operations, not shell commands. All listed fixture Git commands returned exit 0 and empty stderr. The init/add/commit calls also had empty stdout; object-query and history stdout are retained verbatim in `receipt.json` and identified below.

The actual outer invocation, from the seat scratch directory, was:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /usr/bin/prlimit --as=536870912 --nproc=4096 --nofile=128 --cpu=30 --fsize=1048575 -- /usr/bin/timeout --signal=TERM --kill-after=2s 90s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/probe.py
```

The tool wrapper returned the probe summary and the three detector outputs below; it did not expose a separate outer exit-code field. The actual detector exits are captured directly from `Popen.returncode` in the receipt, not inferred from output text.

## Same detector, three observed states

The exact same detector argv was used all three times; `HEAD` advanced through the private commits:

```text
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-33/freeze-integrity.py --root /fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/fixture --round 99 --rev HEAD
```

All detector stderr streams were empty; all three completed without timeout.

| State | Actual UTC start → end, 2026-10-23 | Actual exit | Private commit |
|---|---|---:|---|
| Pristine | 09:33:06.716020+00:00 → 09:33:06.748483+00:00 | 0 | `fcc6807cdc6242bb6fdb550640722f319106f992` |
| Mutated | 09:33:06.751967+00:00 → 09:33:06.785928+00:00 | 1 | `01e758a25ef7ca5841649c55f2b56ad99a6d9020` |
| Restored | 09:33:06.790913+00:00 → 09:33:06.825853+00:00 | 1 | `80e551ceb9db88ab367050aa1181c22f37fde004` |

Actual pristine stdout:

```text
ok	config/guard.txt	sha=e0592e451ebb	commits_after_freeze=0
freeze-integrity: CLEAN pins=1 freeze=fcc6807cdc62 rev=HEAD
```

Actual mutated stdout:

```text
FAIL	config/guard.txt	sha=52d29e0d5a4c	commits_after_freeze=01e758a
freeze-integrity: FAIL pins=1 changed=1 freeze=fcc6807cdc62 rev=HEAD
```

Actual restored stdout:

```text
FAIL	config/guard.txt	sha=e0592e451ebb	commits_after_freeze=80e551c,01e758a
freeze-integrity: FAIL pins=1 changed=1 freeze=fcc6807cdc62 rev=HEAD
```

The CLEAN baseline makes this a killed mutant rather than a baseline-failure/inconclusive result. Most importantly, the restored run reports the original digest **and** both post-freeze touching commits while still exiting 1.

## Before/after hashes and restoration evidence

| State | Payload SHA-256 | Git blob ID |
|---|---|---|
| Before mutation / pristine | `e0592e451ebbe2164d62e786892c2c831b53633328286ea97dbab361a58b984a` | `7b69a23b9ee9327cd613485307f37364203876c8` |
| Mutated | `52d29e0d5a4c1317cdc116363d46c94ff0b34b9fe18bb19afe45a5d275371e61` | `5d401adbf0d70b372ae7482fe0449ca3b18c77a2` |
| After exact restoration | `e0592e451ebbe2164d62e786892c2c831b53633328286ea97dbab361a58b984a` | `7b69a23b9ee9327cd613485307f37364203876c8` |

Claims SHA-256 was unchanged in all three states:

`be07d4be42dd91375987b5a5296cc4345525022dd624e39a7ece8a45562ef2a2`

The recipe also compared final working bytes directly against the saved original bytes: `exact_working_bytes_restored=true`. The restore write was inside `finally`, and the restore commit returned exit 0. No reset, amend, or history rewrite was used.

Actual retained pin-touching history stdout (tabs between columns; root has no parent):

```text
fcc6807cdc6242bb6fdb550640722f319106f992		freeze: pin independent guard bytes
01e758a25ef7ca5841649c55f2b56ad99a6d9020	fcc6807cdc6242bb6fdb550640722f319106f992	mutation: flip one pinned guard byte
80e551ceb9db88ab367050aa1181c22f37fde004	01e758a25ef7ca5841649c55f2b56ad99a6d9020	restore: exact frozen guard bytes
```

## Containment and limits

- Only this assigned report was written in the production lane. All Git writes were in the private tiny fixture. The lane Git calls were read-only `rev-parse HEAD` and `show <pinned-revision>:<gate-path>`.
- `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were removed for all launched commands. System/global Git configuration was disabled; fixture hooks and automatic GC were disabled via command-local options. No host configuration/routing/service changes occurred.
- The runner imposed a 32 direct-child command budget and allowed only one direct child at a time, each with a 12-second timeout. The outer `timeout` bounded wall time to 90 seconds; `prlimit` set address space to 512 MiB, UID process limit to 4096, CPU to 30 seconds, open files to 128, and output-file size to 1,048,575 bytes. Each explicit fixture write was checked below 1 MiB.
- Each direct child had its own process group. Cleanup attempted group termination after waiting; all recorded groups were already absent, including all three detector groups. No background job/service was started or left running.
- Used existing Python **3.14.8**, Git **2.56.0**, GNU timeout **9.12**, and util-linux prlimit **2.42.4**. Their version argv/stdout/exit are in the receipt. **No tool was installed or updated**; no pacman transaction occurred.
- Read only permitted stopped-claim/safety metadata. No held builder artifact, quarantine finding, carrier manifest, native carrier, classifier, upstream runtime, REA/MCP, or alternative model/runtime was used. No separate installed selftest or historical production gate run was performed by this seat.
- This demonstrates one history-sensitive freeze case at the pinned gate bytes. It does not audit all Git topologies, malformed inputs, carrier independence, CHPE structure, or admission criteria. No detector, contract, claims, corpus, or caller was changed.

## Artifact handoff

- Report: `.ufo/waves/round-33/w1/WFreezeRestored.md`.
- Full recipe: `/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/probe.py`.
- Full command receipts and source-output capture: `/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/receipt.json`.
- Restored-byte repository with all three commits retained: `/fast/scratch/hyaku/kaidoku-r33/w1/WFreezeRestored/fixture/`.

Final probe verdict: **killed; exact restoration evidenced; no production repair or admission judgment**.
