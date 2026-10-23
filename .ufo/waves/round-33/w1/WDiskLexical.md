# WDiskLexical — unchanged disk scanner, text-only probes

## Scope and axes

- Seat: `KaidokuR33.WDiskLexical`; lane advice, not outside/non-author verification or admission.
- Axes: **lexical precision**, **explicit-path detection scope**, **CLI exit fidelity**, **containment/exact restoration**. Independent initial cases ran concurrently; only mutation/restoration dependencies were serialized.
- Read `claim-stop.json`: **R33-C1 remains STOPPED / UNPROVABLE**. These instrument observations neither revive it nor replace its missing carrier benchmark.
- Measured scanner revision: `d7076120e4f00c6d18aa77b8764d14861e820eb2`; task-supplied base: `428315a8f5674b952def862910af6e07a6c2224b`.
- Scanner: `tools/round-33/disk-command-audit.py`, Git blob `21919d64dc8423e31888498d30d61ebcc1c1f4f9`; 13,252 bytes; SHA-256 `e61217206fe2a815ff3a2316e87370bfa430a6268900c108ee76f941de8d7f67`.
- A byte-identical copy was materialized from that pinned blob at `/fast/scratch/hyaku/kaidoku-r33/w1/WDiskLexical/disk-command-audit.py`. Live production source and private copy matched initially and finally. **No scanner/source edits.** All inputs, outputs and receipts are under `/fast/scratch/hyaku/kaidoku-r33/w1/WDiskLexical`; this report is the only lane write.

## Mutant and expected detector

**Input-only mutant:** change only the path argument on line 2 of `probe.txt` from `/fast/scratch/hyaku` to `"$ROOT"`. The unchanged scanner is the detector. The existing assignment on line 1 is identical in every phase.

Pristine and restored bytes:

```text
ROOT=/fast/scratch/hyaku
find /fast/scratch/hyaku -maxdepth 0
```

Mutated bytes:

```text
ROOT=/fast/scratch/hyaku
find "$ROOT" -maxdepth 0
```

Expected from source (`disk-command-audit.py:31-50,79-107,126-155`): the literal form produces `RED`, `bare-find`, exit **1**; the variable form has no explicit literal path in the command tail, produces no finding, and exits **0**. The same scanner argv and same `probe.txt` path were used for pristine, mutated and restored phases. These are text inputs, **not shell executions**.

The pristine behavioral check passed: its expected exit 1 / `RESULT FAIL` means the scanner found a red command. It is not a failed test baseline.

## Other assigned UTF-8 cases

`quoted.txt` (53 bytes):

```text
printf '%s\n' 'find /fast/scratch/hyaku -maxdepth 0'
```

`allowed.txt` (81 bytes):

```text
/usr/bin/find /fast/scratch/hyaku -maxdepth 0
/usr/bin/du -s /fast/scratch/hyaku
```

`cwd-relative.txt` (45 bytes):

```text
cd /fast/scratch/hyaku && find . -maxdepth 0
```

`probe.txt` is 62 bytes pristine/restored and 50 bytes mutated. Every fixture write was below 1 MiB. ASCII content is valid UTF-8; no encoding-error case was added.

## Actual CLI outputs and exits

Execution interval: **2026-10-23T09:33:53.527830+00:00 — 2026-10-23T09:33:53.643670+00:00**.

| Case/phase | Start UTC | End UTC | CLI exit | Actual finding fields | RESULT |
|---|---|---|---:|---|---|
| quoted | 2026-10-23T09:33:53.530356+00:00 | 2026-10-23T09:33:53.569668+00:00 | 1 | RED@1:bare-find | FAIL |
| allowed | 2026-10-23T09:33:53.530459+00:00 | 2026-10-23T09:33:53.569983+00:00 | 0 | GREEN@1:absolute-find, GREEN@2:absolute-du | PASS |
| cwd-relative | 2026-10-23T09:33:53.530610+00:00 | 2026-10-23T09:33:53.568991+00:00 | 0 | none | PASS |
| pristine | 2026-10-23T09:33:53.530895+00:00 | 2026-10-23T09:33:53.569410+00:00 | 1 | RED@2:bare-find | FAIL |
| mutated-variable | 2026-10-23T09:33:53.574872+00:00 | 2026-10-23T09:33:53.606683+00:00 | 0 | none | PASS |
| restored | 2026-10-23T09:33:53.612899+00:00 | 2026-10-23T09:33:53.641413+00:00 | 1 | RED@2:bare-find | FAIL |

All six executions matched the prewritten lexical expectations, had empty stderr, and had zero scanner errors. This is an observation count, not an admission score. Raw stdout/stderr for every run, complete unmodified argv arrays, cwd, UTC timestamps, exit values, input text/digest, duration and process cleanup are retained in `runs.json` and `<case>.stdout.txt` / `<case>.stderr.txt`.

Every invocation emitted these exact limitation messages:

```text
LIMITATION	quoted-prose	quoted-prose limitation: the scan is lexical, so a command quoted, echoed, commented, or cited in prose is indistinguishable from an executed command. RED hits can be false positives, and GREEN lines do not prove execution.
LIMITATION	scope	scope limitation: only an explicit /fast/scratch argument in the same simple command is seen; cwd (cd /fast/scratch && find .), variables, aliases, and command substitution are not resolved.
```

Actual per-phase summaries (`files=1`, `errors=0` throughout):

| Case | lines | hits | red | green |
|---|---:|---:|---:|---:|
| quoted | 1 | 1 | 1 | 0 |
| allowed | 2 | 2 | 0 | 2 |
| cwd-relative | 1 | 0 | 0 | 0 |
| pristine | 2 | 1 | 1 | 0 |
| mutated-variable | 2 | 0 | 0 | 0 |
| restored | 2 | 1 | 1 | 0 |

Exact detector argv prefix (followed by the explicit fixture path; full arrays are in `runs.json`):

```text
/usr/bin/prlimit --as=268435456 --cpu=5 --fsize=1048576 --nofile=64 /usr/bin/timeout --foreground --signal=TERM --kill-after=1s 5s /usr/bin/python3 -I -B /fast/scratch/hyaku/kaidoku-r33/w1/WDiskLexical/disk-command-audit.py
```

## Verdict and true lexical limits

**SURVIVED — variable-path input mutation.** The intended literal-path detector is active on pristine/restored bytes but does not flag the variable form. This confirms its stated coverage limitation; it does not authorize changing the contract or expanding this task into shell analysis.

- **Quoted prohibited command:** exit 1 and `bare-find` even though the fixture only quotes a command as a `printf` argument. This demonstrates a lexical false positive relative to a command-execution interpretation.
- **Allowed absolute forms:** exit 0 with two explicit GREEN findings. These mean lexical spelling acceptance only, never observed execution, safe traversal, or compliance proof.
- **Cwd-relative form:** exit 0 with **no GREEN finding and no RED finding**. The earlier `cd` literal does not make `find .` visible to the same-simple-command path check.
- **Variable form:** likewise exit 0 with **no findings**, not an affirmative GREEN classification. Assignment/expansion are not evaluated.
- No `find` or `du` was executed. Shell equivalence or actual filesystem effects were not tested or claimed.

## Restoration evidence

| Bytes | Before | Mutated before/after detector | Restored before/after detector |
|---|---|---|---|
| `probe.txt` SHA-256 | `5353d5b395ebd9ecbeadcdea65bac36777c2ae133877378fa99b7f7ead1c2b09` | `73c8e1daea85034793cee28fd141dfedb441f954fa8fe59c6bf849cf23a2b118` | `5353d5b395ebd9ecbeadcdea65bac36777c2ae133877378fa99b7f7ead1c2b09` |
| Scanner SHA-256 | `e61217206fe2a815ff3a2316e87370bfa430a6268900c108ee76f941de8d7f67` | same | same |

Five recorded checksum snapshots (`hashes.json`) show the exact expected transition and no scanner-byte changes. Initial and final digest maps are identical for both scanner paths and all four fixture paths. Restoration ran in `finally`; the restored detector then reproduced exit 1 / line-2 `bare-find`.

## Bounds, tools and retained evidence

- Six detector invocations and five checksum commands; at most four concurrent bounded process trees (at most eight timeout/scanner processes). Normal scan mode does not spawn subprocesses.
- Each command used 256 MiB address-space, 5 CPU-second, 1 MiB output-file and 64-descriptor limits; 5-second wall timeout, 1-second kill grace, and an 8-second parent communication bound. No timeouts occurred.
- Each command used a private process session; cleanup attempted group termination and reaped the child. All eleven completed groups were observed absent. No background job remains.
- Python **3.14.8**; `/usr/bin/timeout` **GNU coreutils 9.12**; `/usr/bin/prlimit` **util-linux 2.42.4**. **Installs/updates: none.**
- Setup-only anomaly: preliminary `python3 --version && timeout --version` printed Python 3.14.8, then the shell-resolved timeout emitted a usage error, exit 125. All detector commands instead used the absolute GNU binary shown above; this was not a behavioral run.
- Reader tooling note: ranged `:raw` source text omitted its final LF. This was reported through `xd://report_issue`; the actual copy came from the exact pinned Git blob and retained that LF, as confirmed by checksums.
- No built-in selftest, unrelated tests/builds/linters, held artifacts, carrier manifests, source changes, Git/JJ writes, tool installations, or service/config changes.

| Receipt under `/fast/scratch/hyaku/kaidoku-r33/w1/WDiskLexical` | SHA-256 |
|---|---|
| `runs.json` | `a52b0c51d9d259644593033b8fef3bc2b3b48d8967b4625d0bd3d2f38e7d805d` |
| `hashes.json` | `4f462f8e2f62e8b201bf49e908f96afeff08a35f1aea8b7b2bf89d107f207b89` |
| `summary.json` | `6641267f0c34f76eb21a935be47a99222e739832ebd51635e67bc05d1e67aa37` |

`expected.json` was written before execution. `provenance.json` retains source-capture argv, UTC start/end, exit/stderr and the exact source-output digest. Raw checksum stdout/stderr are also retained. No broader check was substituted or proposed.

Report: `.ufo/waves/round-33/w1/WDiskLexical.md`
