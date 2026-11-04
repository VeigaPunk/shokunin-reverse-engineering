# Kernel-side environment witness and the forged child-dump control

source: S277 (opened source; registry append not observed at drafting) — Linux man-pages 6.19, proc_pid_cmdline(5), https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html#DESCRIPTION; ScoutSource opening evidence described below. S275, proc_pid_environ(5), grounds the environment channel.
verified-at: 2026-11-04 — source/code reading and retained pre receipts only; required landing receipt `.ufo/waves/round-73/l1/scores/c1-at-landing.json` was not present at drafting, so this entry does not certify the 12/12 landing result.
recheck: use the frozen R73-C1 command in `plans/round-73-claims.md` with `python3 -I -B`, explicit lane root, measured revision, declared route/battery, REA 6.5.0, seat scratch, declaration receipt, non-default pinned UPX copy and nonce commitment; retain the JSON under the lane and inspect every arm plus the A12 observations, instrument pins and disclosed base-arm conflict before claiming success.

## Scope and evidence status

This entry covers `A12_kernel_witness` in `tools/round-73/seam-probe.py` at declaration
`da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b`. The probe adds an observer-side channel to
the round-72 child-side witnesses. A child's clean dump is its claim; an independent
read of that process's `/proc/<pid>/environ` can contradict it. This is not general
wrapper authentication, a full descendant census, or evidence for another operating system.
The lane's separate axes are coverage (C1), calibration (C2), and operability (C3);
this guide describes C1 and does not award any of those claims.

`kernel_witness()` scans numeric `/proc` entries, reads NUL-separated argv from
`/proc/<pid>/cmdline`, selects a process when any argument starts with the absolute shim
directory, and reads its environment through `/proc/<pid>/environ`. It retries unreadable
environments, keeps the first readable sample per PID, and sleeps 0.004 seconds between
scans. `_name_samples()` retains the first sample per matched shim basename. The record
is thus independent of a shim's printed dump, but process selection is still based on
argv controlled by the observed process or its launcher, not verified process ancestry.

S277's opened page states, under DESCRIPTION: “This read-only file holds the complete
command line for the process, unless the process is a zombie.” This grounds the lookup
mechanism, not an assertion that argv is immutable or that matching argv proves identity.
Do not confuse `proc_pid_cmdline(5)` with `proc_cmdline(5)`, the kernel boot command line.

## Exact A12 decision clauses

The allowlist is exactly `HOME`, `LANG`, `PATH`, `TMPDIR`. The pure function
`a12_verdict(genuine, forged, allow_keys)` returns these conjuncts:

| Clause | Implemented condition | Boundary |
| --- | --- | --- |
| `genuine_ok` | Genuine `rc == 0`; kernel sample names include both `git` and `readelf`; every retained genuine sample has exactly the four keys and a falsey `canary_present`. | Every retained genuine sample, not every process ever executed. The code uses a falsey check, not `is False`; missing canary fields are therefore not independently rejected. |
| `lie_clean` | The forged `shims` mapping is nonempty and every entry has exactly the four keys and a falsey `canary_present`. | The pure predicate does not require both names, `recorded`, or `keys_exact`; the concrete fixture supplies two dumps and the frozen claim requires both. |
| `forged_detected` | The forged kernel mapping is nonempty and at least one sample has a different key set or a truthy `canary_present`. | One dirty retained sample suffices. The pure predicate does not require both forged child names or inspect forged return codes. |
| `ok` | Boolean conjunction of `genuine_ok`, `lie_clean`, and `forged_detected`. | A clean kernel world or a dirty child-side dump cannot demonstrate the claimed lie. |

The frozen after-state additionally requires `arms_passed 12`, `target 12`,
`A12_kernel_witness` true, genuine `git` and `readelf` samples with
`canary_present false`, and **both** forged child dumps keys-exact and canary-free while
the forged kernel evidence is dirty and `verdict.forged_detected` is true. Do not replace
those clauses with the arm's final boolean alone. A12 does not itself check HOME/TMPDIR
containment or consume the checker summary; those are separate A11/route properties.

## Forged control and observed result

The genuine sub-run invokes the declared route's receipt checker under truthful Perl
shims. Each reads its own initial environment, records it in scratch, sleeps 0.4 seconds
so the poller can sample, and executes the real `/usr/bin/git` or `/usr/bin/readelf`.
The checker receives a caller environment seeded with the canary and must scrub its
children to the four-key set.

The forged sub-run is a fixture producer, not a hostile replacement of the measured
route. Its Python child invokes each lying shim with `subprocess.run(..., env=None)`;
it therefore inherits the producer's caller environment, including the canary. Each shim
writes a fabricated four-key, canary-free dump, sleeps 0.4 seconds and executes the real
tool. The intended contradiction is clean child testimony versus a dirty kernel sample.

The retained `.ufo/waves/round-73/pre/c1-at-base.json` actually records that contradiction:
both forged shim dumps have `keys_exact true` and `canary_present false`; both named
forged kernel samples have extra keys and `canary_present true`; `lie_clean` and
`forged_detected` are true. However, `genuine.rc` is 1 and `genuine_ok` is false, so
A12 is false and the whole probe reports **8/12**, not 11/12. This is observed pre-state
evidence for the forged control, **not** evidence of a successful landing.

The required after-state evidence is
`.ufo/waves/round-73/l1/scores/c1-at-landing.json`. It was absent when this draft was
written; no landing count, genuine success, or final claim verification is asserted here.
The separate `.ufo/waves/round-73/pre/c1-at-base-r72probe.json` records 11/11 with no
failed arms for the older probe. It is a different instrument/control from the frozen
round-73-probe-versus-round-72-route comparison.

## Base-arm conflict

The frozen sentence requires the same round-73 probe against the round-72 route to
report “11 of 12 naming `A12_kernel_witness` false”. The pre receipt instead reports
8/12 with `A2_threaded_path`, `A10_run_binding`, `A11_checker_env`, and
`A12_kernel_witness` false. `.ufo/waves/round-73/claims.json` discloses an erratum that
re-stipulates the base as the round-72 **probe**, 11/11 and no A12. That disclosure must
travel with the receipts; a prose entry cannot amend the canonical frozen predicate or
turn the alternate control into proof of its original clause.

## Limits and interpretation

- A process the observer never samples is unseen: a short-lived wrapper can exit between
  scans or before polling starts. The fixture's 0.4-second sleep is an observation aid,
  not a guarantee for arbitrary wrappers.
- A PID/mount namespace, procfs access restriction or different observer-visible procfs
  can prevent the observer from seeing the relevant process. No namespace escape or
  all-process security guarantee is measured here.
- A producer can run a clean, visible decoy while spawning the real tool elsewhere, without
  a matching argv prefix, through another namespace or supervisor. This observer does not
  bind the sampled shim to all actual work, nor verify executable identity or ancestry.
- The prefix match can select a launcher whose argv merely contains a shim path. First-PID
  sampling and first-basename reduction can miss later execs or additional dirty instances.
  “Producer-independent” describes the kernel-read channel, not an unforgeable selection key.
- `/proc/<pid>/environ` concerns the process's initial environment, not arbitrary later
  environment mutation (S275). The fixed canary detects its named key, not every secret.
- Persist only key names and canary-presence facts when documenting dirty worlds. Raw
  environment values are not needed to establish this contradiction and must not be copied
  into the lane. Existing producer-side receipt fields are not a license to repeat values.

## Source opening provenance

ScoutSource reported opening the S277 candidate on 2026-11-04: HTTP 200, 7,918 bytes,
sha256 `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`,
Linux man-pages 6.19 (page date 2026-02-08). Its designated snapshot is
`.ufo/waves/round-73/w1/ScoutSource/proc_pid_cmdline.5.html`. The source was opened by
that seat, not fetched again by this scribe. At drafting the registry search found no
S277 row and that snapshot directory had not yet landed; the row number is the assigned
next row, not an assertion that the registry append or retained snapshot was observed.
