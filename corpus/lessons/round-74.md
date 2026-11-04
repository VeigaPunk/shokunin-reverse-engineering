# Round 74 — declared mutation kills and records derived from bytes

Base: `04fdc2c4dbedbe5ee50a069af14310068393233e`.
Declaration: `b3a7e28089582ce5fb002a1b88e5295caf696b9f`.
Freeze: `021914c0e638454e507087accfe41af1ab69f185`.
Contract: `plans/round-74-claims.md` and `.ufo/waves/round-74/claims.json`.
Axes: operability (R74-C1, declared-case mutation closure) and calibration
(R74-C2, the record's agreement with an outside defect population and committed bytes).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| **A record value written from a plan rather than from bytes.** Round 73 froze the same-probe/round-72-route comparator as 11 of 12, but its retained measurement is 8 of 12. It also pinned two producer digests that are not the blobs at its freeze. These are one provenance mistake, not two independent capability losses. | Freeze container `8b928422b51e2f03039ab365f7bafa838389c6d2:.ufo/waves/round-73/claims.json`, `frozen_atoms.A6` and `loaded_by_counter`; `.ufo/waves/round-73/pre/c1-at-base.json` (8/12) versus `.ufo/waves/round-73/pre/c1-at-base-r72probe.json` (11/11, different runner); `.ufo/waves/round-73/l1/scores/gate-at-freeze.json`; `corpus/lessons/round-73-verifier-spotcheck.md` §6, items 6, 8 and 9. | The pre-freeze producer-pin procedure should compare every declared digest with its actual blob; the before-arm selection block should name the selected runner and receipt, with all other receipts assigned explicit roles. The old D7 checked pointer existence, not this semantic selection. D7b, D14 and D15 in `plans/round-74-claims.md` bind those missing criteria. | Derive pins from bytes before freezing, retain the pin preflight, and check the actual freeze again. Name the round-72 probe's 11/11 receipt as the R73-C1 before-arm; retain the same-probe/older-route 8/12 receipt as a diagnostic, not an interchangeable comparator. Bind runner path and sha256. Append corrections rather than rewriting history: the round-73 freeze remains FLAGGED. Round-74 `.ufo/waves/round-74/pre/freeze-pins-before-freeze.json` records nine matching rows, no mismatches; its `world: worktree`, `rev: null` is a preflight, not proof of the eventual committed freeze. |

The wrong frozen producer pins were `973d504b…` and `7f46e3ef…`; the corresponding
round-72 packed-elf and seam-probe blobs were `330ecf89…` and `602b305d…`.
The standing `INSTRUMENT_PIN_MISMATCH` is historical debt, not erased by a later correction.

## Gate

All five pages below were opened on **2026-11-04**. Quotes are literal excerpts;
locations identify the relevant heading or index entry, not a search-result snippet.
The four rejections concern the round-73 process-command-line quotation, not the
sources' general quality. They are reopened here for the missing rejection record.

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S278, ptrace(2), admit | https://man7.org/linux/man-pages/man2/ptrace.2.html#NOTES | 2026-11-04 | “Defined as PTRACE_MODE_READ \| PTRACE_MODE_FSCREDS.” (5 words; NOTES → Ptrace access mode checking → PTRACE_MODE_READ_FSCREDS) | READ_FSCREDS combines the read-access class with filesystem credentials. The same subsection lists `/proc/pid/environ` among READ operations. Credentials, capabilities and LSM checks can deny access; unreadable is missing observation, not an empty environment. This grounds R74-C1's `a12-proc-environ-unreadable` case without claiming universal procfs access. |
| proc(5), reject for the target quote | https://man7.org/linux/man-pages/man5/proc.5.html#DESCRIPTION | 2026-11-04 | “The proc filesystem is a pseudo-filesystem which provides an interface to kernel data structures.” (14 words; DESCRIPTION, opening sentence) | General procfs overview; its per-process overview sends the reader to proc_pid(5). Do not attribute the process command-line quotation to this umbrella page. Flip only if this page itself carries the sought passage in a later version. |
| proc_cmdline(5), reject | https://man7.org/linux/man-pages/man5/proc_cmdline.5.html#DESCRIPTION | 2026-11-04 | “Arguments passed to the Linux kernel at boot time.” (9 words; DESCRIPTION → /proc/cmdline) | `/proc/cmdline` describes boot arguments, not `/proc/<pid>/cmdline`. Similar naming is not evidence of the same interface. Flip only if the question changes to kernel boot arguments. |
| proc_pid(5), reject for the target quote | https://man7.org/linux/man-pages/man5/proc_pid.5.html#DESCRIPTION | 2026-11-04 | “There is a numerical subdirectory for each running process; the subdirectory is named by the process ID.” (17 words; DESCRIPTION → /proc/pid/, opening sentence) | This is the process-directory overview and navigation to the split leaf pages, including proc_pid_cmdline(5), not the leaf's command-line semantics. Flip if the directory layout becomes the question, or the target passage moves here. |
| section-5 index, reject as semantic evidence | https://man7.org/linux/man-pages/dir_section_5.html | 2026-11-04 | “proc_pid_cmdline(5)” (1 word; alphabetic proc entries, link to man5/proc_pid_cmdline.5.html) | The index locates the leaf page; a link label does not establish that leaf's semantics. Flip only for a navigation/indexing claim, not the process-observation claim. |

The frozen audit's index identifier is `index.html#_section_5`; the opened page is
`dir_section_5.html`. Preserve the distinction when recording the rejection; an alias
in the record must not be presented as a fetched URL. The round-73 spot-check §4
(source decisions) and §6 item 4 identify the four rejected pages.

## What the wave found

- **ExecProbeCases** independently reproduced five one-case bindings and one cross-binding:
  deleting the sample's `canary_present` field fails both `a12-kernel-multiple-samples` and
  `a12-kernel-canary-field` (the multi-sample case reads that field), so the canary-field case is
  not the sole detector — named as planned item (a).
- **CriticClaims** found three further A12 survivors outside the frozen ten classes (`home_under`
  truthiness, `_name_samples` last-wins, `lie_clean`'s key equality) and demonstrated four
  cosmetic-passes for D9–D12 (a used-by cell that negates the path, a search-log line with the
  tokens only, an erratum that reverses the values, empty reason/flip cells) — debt for a
  strengthened atom table, never a reason to edit the frozen one.
- **MutationTester** mutated five atoms: D9 and D13 are killed by the committed base receipt;
  D8, D11 and D14 survive both the base receipt and the parser selftest, whose 12 cases never
  execute an atom — the structural finding that the atoms have no red-arm coverage.
- **ExecAuditRun** reproduced 11 mismatches at base and 9 at the freeze, and named the coverage
  limits: D14 binds the round-74 receipt rather than the routed defect-6 receipt, D15 cannot
  restate the round-73 standing debt, and D11's detail claims reason/flip checks its predicate
  does not perform.
- **SentinelScope** routed four code items (path containment in `freeze-pins.py`,
  pin-before-execution in `probe-mutation.py`, exception-safe child cleanup, A11's Perl source
  interpolation) and one carried item (A12's `_parse_shims` still serializes shim `values`, the
  round-72 QUALITY 128 class, inherited from round 73).
- **ScoutSource** verified S278's quote and digest, confirmed the split-page rejections, and
  found the D11 token is a round-73 label rather than an opened URL: the row registers
  `dir_section_5.html` and says so, and the atom's string check is shallow (debt (b)).
- **ExecArm / the L1 re-run** — the refactor preserves the runtime arms: A1–A12 at the record
  revision is 12/12 with `A12_kernel_witness` true; the seat's 11/12 was its `--expect-upx` path
  differing from the route receipt's recorded argv0 path (planned item (e)).

