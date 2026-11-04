# SentinelScope — round-73 security review

Disposition: **BLOCKING findings SS73-1, SS73-2 and SS73-5; review only, no remediation applied.**
Axes: witness identity, secret minimization, path/command confinement, cleanup. Static review of all six round-73 instruments; read-only committed-receipt scan at HEAD `d36c6ee00122e9c991d7c8efc2e179dc0a10d9ed`. No exploit, instrument suite, or other agent runtime executed.

## SS73-1 — HIGH / BLOCKING: A12 does not authenticate child identity

Evidence: `tools/round-73/seam-probe.py:439-457` enumerates every numeric `/proc` entry, reads its cmdline, then reads its environment if **any argument starts with** the scratch shim-directory string. There is no parent/descendant, expected executable, exact shim filename, UID, or process-start-time check. `:544-554` repeats the prefix match and keeps the first sample per basename with `setdefault`.

Exploit path [INFERENCE, not executed]: an unrelated same-user process with an ordinary argument naming that directory, a sibling-prefix directory, or a matching basename is eligible. The kernel's normal permissions are the only read boundary; accessible other-user processes also qualify. The probe reads cmdlines of unrelated processes even before filtering, and full environments of matching processes. It retains argv, all key names, HOME, TMPDIR and canary presence, not arbitrary other values (`:455-457`). PID reuse can also invalidate the identity assumption.

This is not merely hypothetical selection breadth: the legitimate dirty Python producer itself is started with the shim path as its argument (`:620-623`), and therefore qualifies before its Perl child does. Both map to the same `git`/`readelf` key. A dirty parent sample can satisfy `forged_detected` without establishing the environment of the shim exec boundary (`:483-485`). Kernel bytes are independent of the producer's dump, but process attribution is not established.

Impact: overbroad sensitive reads and an A12 false-green attribution route; the claim that these are exclusively the probe's tool-child samples is unsupported. No lane-local pid-selection file is read: this widening comes directly from argv. A lane-local implicit capsule pointer is a separate reader, not a `/proc` selector.

Smallest remediation: bind sampling to exact expected shim processes in the launched process tree, exclude the Python producer, match an exact canonical shim path rather than any prefix argument, and bind PID to process start time. Reject missing authenticated tool-child samples rather than accepting a parent substitute.

## SS73-2 — HIGH / BLOCKING: caller text becomes executable Perl source

Evidence: `seam-probe.py:319-325,492-507,515-527,608-611`; also `packed-elf.py:1322-1328`. Scratch-derived filenames are interpolated into single-quoted Perl literals without escaping; the lying shim interpolates caller PATH and scratch HOME/TMPDIR into a double-quoted Perl literal. These values are not passed as data arguments.

Exploit path [INFERENCE, not executed]: a legal caller-controlled `--work` path containing a quote can change or break the generated Perl program. Caller PATH containing Perl interpolation metacharacters can change the fabricated dump or execute interpolated Perl. A missing `/usr/bin/git` or `/usr/bin/readelf` additionally allows `shutil.which` to inject an unescaped fallback executable path (`seam-probe.py:310-325,520-527`). No receipt field selects the shim destination or real tool.

Impact: caller-controlled directory/environment strings can change executed code, its output destinations, and real-tool invocation; inherited dirty fixture environment makes accidental credential access consequential. This is source injection, despite subprocess callers using argv arrays and not `shell=True`.

Smallest remediation: keep generated programs constant and supply record filename, real executable and synthetic environment values through argv/data; fail closed if the fixed trusted executables are absent. Do not embed these strings into Perl literals.

## SS73-3 — MEDIUM / NON-BLOCKING: caller-authorized paths are not a sandbox

Evidence: `seam-probe.py:299-303,569,676-680,1247-1249`; `mutation-check.py:200-211,342-344`; `controls.py:98,217-219`; `record-audit.py:330-332`; `packed-elf.py:672-681,966-972,1025-1026,1141-1142`. `--work` controls scratch parent; output/log flags permit absolute paths, traversal and symlink-following writes. Checker mode without `--work` and selftests without explicit work use tempfile defaults (`packed-elf.py:672,1240,1314`). There is no universal lane-root confinement. The mkdtemp-created root is private by default, limiting other-user races, but does not make an untrusted parent or same-user attacker safe.

PATH remains caller-controlled (`packed-elf.py:221-225,540-547`; probe extraction `seam-probe.py:116-118`). Fixed `/usr/bin/git` and `/usr/bin/readelf` protect the shim's real-tool selection on this host; they do not pin every initial git/node/tool execution. No receipt field changes shim destinations; the implicit capsule field can select a lane-local file for reading. Its realpath containment rejects relative escapes and skips external absolute pointers (`packed-elf.py:600-638`), although ordinary resolution/open races remain. Explicit `--capsule` is caller-authorized separately.

Impact: incorrect invocation can write outside the lane or execute caller PATH tools. This is non-blocking for trusted operator CLI usage with explicit bounded work/output paths; it must not be advertised as a hostile-input sandbox. Smallest remediation: enforce canonical allowed roots for this wave's wrapper and require explicit scratch/log paths; pin executables if PATH is intended to be untrusted.

## SS73-4 — MEDIUM / NON-BLOCKING: cleanup fails on A12 timeout

Evidence: `seam-probe.py:582-598,620-632`. `communicate(timeout=1800)` and `wait(timeout=600)` are not guarded by a finally that stops polling, terminates/reaps process trees and drains pipes. Forged producer pipes are not consumed. A timeout can leave descendants and a daemon sampler running until process exit; fixture scratch is caller-cleaned rather than automatically removed.

Impact: interrupted runs can retain processes and sensitive scratch material. Smallest remediation: finally-based stop/join and process-group terminate/reap/drain on all exits; preserve only sanitized receipts before deleting work.
## SS73-5 — MEDIUM / BLOCKING: environment-value serialization violates the wave contract

Evidence: `seam-probe.py:455-457` stores HOME and TMPDIR values in each kernel sample; `:599-601,633-641` attaches these samples to the returned arm, and `:1246-1250` serializes them into the receipt/stdout. `_parse_shims` likewise stores full parsed environment values (`:533-540`). These are not merely transient reads: they are receipt fields. The canonical wave bounds permit key names and canary presence only when showing an environment, with values excluded from committed files. A future committed A12 receipt would violate that constraint even if HOME/TMPDIR happen to be harmless paths. No already-committed A12 disclosure was observed in the scanned snapshot.

Impact: receipt generation is not safe to commit under the explicit data-minimization contract; dirty truthful-shim observations could serialize additional secret values. Smallest remediation: remove raw values from returned/persisted observations and compute needed containment predicates in memory. Retain raw witnesses only in private, ephemeral scratch. This also addresses the kernel-field issue independently reported by ConnectorCross-9; no sibling-lane content was read or written.


## Secret-capture and configuration results

* **Lying fixture:** `seam-probe.py:501-512` does not read `/proc/self/environ` or serialize `%ENV`; it fabricates only HOME/LANG/PATH/TMPDIR. The dirty producer inherits the caller environment (`:615-623`), but the kernel witness retains key names, canary, HOME/TMPDIR and argv rather than full environment values. PATH still originates with the caller and interpolation is SS73-2.
* **Truthful fixtures differ:** A11 and A12 truthful shims write raw `/proc/self/environ` bytes (`:319-325,492-496`). `_parse_shims` includes their values in output (`:533-540`). Correct children have four allowlisted keys; a broken/dirty child could put secrets in scratch and then receipt output. The route capture launcher also writes `dict(os.environ)` before exec (`packed-elf.py:312-322`), normally supplied an allowlisted environment. Therefore absence of leaks in the current committed corpus is not a guarantee under a future dirty-child failure. Keep raw witnesses scratch-only and persist key names/canary predicates, not values.
* **Committed scan:** all **8 committed round-73 files, 440409 bytes** scanned at the stated HEAD. Zero matches for OpenAI/Anthropic/GitHub/AWS/Slack token/private-key shapes, uppercase env-assignment lines, four-assignment `=`-heavy lines, or JSON `"env": {` objects. Evidence: `SentinelScope/committed-receipt-scan.json` records exact regexes and file hashes, no values. Scope excludes concurrently untracked receipts and older rounds; regexes cannot prove absence of every secret encoding.
* **Operator config:** no direct `~/.omp`, `~/.config`, XDG or home-expansion config reads found in the six instruments. Operator RULES was read by this reviewer as explicitly required, not by an instrument. Probe/battery/audit git extraction inherits caller environment (`seam-probe.py:116-118`, `mutation-check.py:181-183`, `record-audit.py:65-78`), and controls inherits its environment (`controls.py:55-56`); those child tools can read normal git configuration or use environment-selected config paths. Python `-I -B` does not suppress git config. This is an indirect read possibility, not an observed operator-config access trace. Smallest remediation if complete config isolation is required: provide isolated HOME and fixed git config policy to these entrypoint readers too.

## Delivery

Only this report, its identical nested Report.md and the sanitized scan receipt were written inside the assigned lane. No source edits, git mutations, installs, raw environment dumps or offensive probes. One explicitly named scratch directory was used with TMPDIR for the scan's child git processes and deleted in finally before delivery; no pinned UPX copy was needed because no packer was executed. No `resume_continuity_v1` implementation occurs on this assigned surface; no continuity rejection contract was exercised or claimed.

Self-evaluation: accuracy 4/5 (exploit paths are statically inferred, not executed); completeness 4/5 (snapshot excludes later/untracked receipts); clarity 4/5 (four findings distinguish blocking from caller-trust limitations); actionability 4/5 (specific fixes, no remediation authorization); conciseness 4/5 (detail retained for file:line evidence). Overall 4.0. Improvements: authenticate witness identities first; remove generated-source interpolation; extend sanitized scanning to final committed landing receipts. A scoped static-security-review assessment, not a release judgment.

Report: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/SentinelScope/Report.md
