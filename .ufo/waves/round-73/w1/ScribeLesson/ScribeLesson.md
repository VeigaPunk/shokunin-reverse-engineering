# ScribeLesson — round-73 wave-1 report

## Behavior and touched surfaces

Drafted `lesson.md` in this directory, not `corpus/`. It follows round-72's voice and table
shape, names coverage/calibration/operability, describes all three claims and six instruments,
separates declaration implementation from unobserved landing success, records three mistake
classes, supplies S277's located source quote and snapshot, and retains the non-author closure
placeholder. The parent `../ScribeLesson.md` is the requested report index. No product code,
instrument, source registry, judgment, or git state was changed.

Artifacts (lane-relative):
- `.ufo/waves/round-73/w1/ScribeLesson/lesson.md`
- `.ufo/waves/round-73/w1/ScribeLesson/proc_pid_cmdline.5.html`
- `.ufo/waves/round-73/w1/ScribeLesson/ScribeLesson.md` (this report)
- `.ufo/waves/round-73/w1/ScribeLesson.md` (report index)

## Findings and conflicts

1. **Frozen C1 before clause contradicted by pre receipt.** Exact frozen plan text:
   "reports 11 of 12 naming `A12_kernel_witness` false". Receipt
   `pre/c1-at-base.json` instead records 8/12 and failures A2/A10/A11/A12.
   Exact erratum text: "The base arm is re-stipulated as the round-72 PROBE at the same revision and the same route receipt: 11 arms, 11 passed, no arm id A12_kernel_witness".
   This report preserves the conflict for the canonical judge; it does not decide that a
   changed before arm satisfies the original frozen predicate. `frozen_atoms.A6` still
   describes the first receipt as "11 of 12, A12 false".
2. **Wrong-case kill despite zero survivors.** `w1/ExecSweep/declaration-mutations.json`
   has `survivor_count: 0` but `ok: false`; git_reader_env_dropped fails
   checker-readelf-allowlisted-exec instead of git-reader-allowlisted-exec.
   Its `target_pin.expect` is null. The separately pinned
   `pre/c3-at-landing-preview.json` also records the wrong-case kill and records a
   readelf_env_dropped survivor. No causal explanation is established by this scribe.
3. **Record repairs not yet evidenced at declaration.**
   `w1/ExecSweep/declaration-audit.json` records 6/7 mismatches (D1–D6), D7 true.
4. **Source limit.** The live source supports cmdline discovery but explicitly describes
   writable argv storage. It cannot support an unrestricted unforgeable-PID-identity claim.
   S277 was not present in corpus/SOURCES.md at inspection time; its id is declared in
   claims.json, not registered by this seat.

## Gates and provenance

No probes, tests, mutation batteries, validators, build, formatter, source census, or judge
were run by this seat. Receipt outcomes above are reads of others' artifacts, not execution
evidence for this seat. No final landing/freeze/closure outcome is asserted. Source fetch:
HTTP 200, 7 918 bytes, SHA256
`1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`.
Quote at saved HTML lines 73–74, DESCRIPTION (17 words):
"This read-only file holds the complete command line for the process, unless the process is a zombie."

Exact shell commands exercised, cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

```sh
S=/fast/scratch/hyaku/kaidoku-r73/ScribeLesson; export TMPDIR="$S"; trap 'rm -rf -- "$S"' EXIT; mkdir -p -- "$S" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ScribeLesson; printf '%s\n' 'Scratch created and removed by EXIT trap; no probes executed.'
```
Outcome: exit 0; scratch removed at shell exit, before drafting/yield. No scratch receipts
were generated; source evidence was written directly under the permitted report directory.

```sh
curl --fail --silent --show-error --location --output /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ScribeLesson/proc_pid_cmdline.5.html --write-out 'HTTP %{http_code}\n' https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html && sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ScribeLesson/proc_pid_cmdline.5.html && wc -c /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ScribeLesson/proc_pid_cmdline.5.html
```
Outcome: exit 0; HTTP/status/hash/size as above.

```sh
jq '{rev,ok,arms_passed,target,failed}' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/pre/c1-at-base.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/pre/c1-at-base-r72probe.json
```
Outcome: exit 0; first receipt 8/12, ok false; second 11/11, ok true; both
rev da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b. This is extraction, not a probe rerun.

Specialized read/grep/glob tools supplied the prior lesson, frozen plan/claims, outside
spot-check, wave inventory, existing audit/mutation receipts, and source quote locator.
An initial read/search for lane-root SOURCES.md failed; discovery located corpus/SOURCES.md.
No tool installation/update, environment-value dump, git/jj write, or external runtime invocation.

## Out of scope and integration limits

No corpus publication, source admission, instrument repair, commit/push, or judgment. Main
should reconcile the frozen-before conflict, retain supersession evidence for any repairs,
and use actual pinned landing receipts before promoting draft targets to completed claims.
Final wave findings and closure are intentionally not fabricated in this early draft.

## Self-evaluation

Accuracy 4: cited existing receipts; moving wave state may later supersede them.
Completeness 4: requested draft/report/source fields present; landing is deliberately unasserted.
Clarity 4: claim targets and observed declaration outcomes explicitly separated.
Actionability 4: artifact paths and exact conflicting clauses support integration/judgment.
Conciseness 4: command provenance adds length but is required for auditability.
Overall 4.0. Highest-value improvement belongs to integration: incorporate final landing and
source-registration evidence without erasing the failed-before and wrong-case observations.

Report: .ufo/waves/round-73/w1/ScribeLesson/ScribeLesson.md
