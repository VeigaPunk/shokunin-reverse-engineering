# Round 73 — a kernel-side witness, record calibration, and named reader-seam cases

author: round-73 L1; draft prepared by ScribeLesson (non-author seat)
round: 73, attempt 1
base: `05bf065684e52d72ea25aad95f7acb71fcd7874c`
declaration: `da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b`
status: wave draft, not a landing or admission verdict

## Round narrative

Three frozen claims work three axes: **coverage** (R73-C1), **calibration** (R73-C2), and
**operability** (R73-C3). Coverage is the declared tied-lowest axis; no stagnation waiver is claimed.
The declaration contains six instruments under `tools/round-73/`: `packed-elf.py`,
`seam-probe.py`, `mutation-check.py`, `record-audit.py`, `controls.py`, and `capsule_audit.py`.
The plan is `plans/round-73-claims.md`; pins and disclosures are in
`.ufo/waves/round-73/claims.json`. The route receipt is
`.ufo/waves/round-73/pre/route-at-declaration.json`.

- **R73-C1 — coverage.** A12 adds an observer that discovers running shims through
  `/proc/<pid>/cmdline` and samples `/proc/<pid>/environ`. Its target is 12/12 arms:
  genuine git/readelf kernel samples have exactly HOME/LANG/PATH/TMPDIR and no canary;
  the forged control writes clean child-side dumps while its kernel samples expose pollution.
  This is an acquisition of a probe channel, not an established immunity to arbitrary hostile
  processes. The originally frozen route-differential before is contradicted by its receipt:
  the round-73 probe against the round-72 route records **8/12**, not 11/12. The receipt is
  bound to the round-73 producer; the older checker rejects it before the expected children run.
  The disclosed erratum substitutes the round-72 **probe**, which records **11/11 with no A12**.
  This is a changed before-arm stipulation, not evidence that the original frozen predicate passed.
- **R73-C2 — calibration.** Seven atoms derive from the non-author round-72 spot-check's
  routed defects, not from the record being graded. The target is six base mismatches to zero
  landing mismatches. The observed declaration audit still has six mismatches, D1–D6, with
  D7 true (`w1/ExecSweep/declaration-audit.json` under the round-73 wave directory).
  Repairs and a measured landing result must not be inferred from the declared target.
- **R73-C3 — operability.** The route introduces seams and the named cases
  `git-reader-allowlisted-exec`, `checker-readelf-allowlisted-exec`, and
  `implicit-capsule-polluted-raw-log`. The target is three base survivors to zero landing
  survivors, with every kill attributed to its declared case, a pinned target, and 38 pristine
  cases green. Declaration receipts expose a wrong-case kill and inconsistent readelf-mutant
  outcomes (see Mistakes); zero survivors alone is not the predicate.

**What landed at the declaration:** the six instruments and the claim plan, not a verified
three-claim landing. This draft records the available receipts without certifying later wave
repairs, freeze gates, final source registration, or a record commit. No instrument was executed
by this scribe.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A producer-side witness was mistaken for the observation boundary** — round 72's A11 consumed a shim dump and checker statements, then treated a wrapper forging both as outside the measurable class. | `corpus/lessons/round-72.md` §What the wave found (CriticClaims); `plans/round-73-claims.md` §R73-C1 | no independent observer in A11; a witness claim must name its channel, and producer-side evidence remains a producer claim | A12 adds a kernel-side environment channel and a forged-clean child-dump control. The channel is implemented at the declaration; its complete landing predicate remains a separate measurement. |
| **The before arm changed the wrong component** — the frozen C1 comparator swapped the route while retaining a receipt bound to the new producer. It promised 11/12 but recorded 8/12. | `.ufo/waves/round-73/pre/c1-at-base.json`; `pre/c1-at-base-r72probe.json`; `claims.json` errata[0] | the actual pre measurement and receipt binding, not a prose explanation | the disclosed erratum compares probe generations instead (11/11, no A12). Retain the frozen text, the failed before receipt, and the amendment; the canonical judge must decide its admissibility. |
| **A zero-survivor aggregate hid case attribution failure** — the git-reader mutation fails `checker-readelf-allowlisted-exec`, not its promised git-reader case. | `.ufo/waves/round-73/pre/c3-at-landing-preview.json` mutants[0]; `w1/ExecSweep/declaration-mutations.json` mutants[0], `ok: false`, `survivor_count: 0` | the battery's `killed_wrong_case` check and named-case conjunct; the aggregate alone would not catch it | repair the actual seam/case binding under a disclosed instrument supersession and retain a pinned remeasurement. No repair or landing success is established by these receipts. |

The preview also records `readelf_env_dropped` surviving; ExecSweep records it killed at the
same declaration. Their receipts differ in target-pin expectations (preview pinned, ExecSweep
`expect: null`). These observations are not interchangeable; this draft assigns no cause.

## Gate — source opened this round
| row | URL | opened | quote (≤25 words) | snapshot |
|---|---|---|---|---|
| S277 (declared row id; registration not observed in this draft) | https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html | 2026-11-04, HTTP 200 | DESCRIPTION, snapshot lines 73–74: "This read-only file holds the complete command line for the process, unless the process is a zombie." (17 words) | 7 918 B; sha256 `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`; `.ufo/waves/round-73/w1/ScribeLesson/proc_pid_cmdline.5.html` |

The page grounds the process-discovery mechanism, **not** an unforgeable identity guarantee:
DESCRIPTION lines 84–97 explain that processes can overwrite argv storage or move the referenced
memory. The A12 claim is bounded to the measured shims/control. S277 was absent from
`corpus/SOURCES.md` when inspected; this seat does not register or admit sources.

## Non-author closure

`[L1 — filled by the non-author closure.]`
