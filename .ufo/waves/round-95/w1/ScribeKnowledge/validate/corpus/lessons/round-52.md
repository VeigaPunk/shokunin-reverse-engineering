# Round 52 — pre-freeze rejection, not a re-scored success

Declared claims: R52-C1 coverage and R52-C2 depth, `plans/round-52-claims.md` at
`ab0eafedc41402b43b41a4362084119578dfe7ce`. Neither claim acquired a final freeze,
production instrument, fresh extraction receipt or Core promotion. Wave-1 artifacts
are retained under `.ufo/waves/round-52/w1/`; they are drafts and adversarial evidence,
not registered gates. LOG.md records this round's recovery and disposition.

## Gate

- Admit S252 as scoped primary documentation, not as proof of extractor behavior.
  URL: https://man7.org/linux/man-pages/man2/mknod.2.html ; accessed 2026-10-30
  by the prior L1, ScribeSources, ScoutMknod and the recovering L1.
  Located quote: ERRORS, EPERM, Linux man-pages 6.19 (2026-02-11):
  “mode requested creation of something other than a regular file, FIFO (named pipe), or UNIX domain socket, and the caller is not privileged”
  (23 whitespace-separated words). The continuation names CAP_MKNOD. Retained HTML
  and fetch receipts: `.ufo/waves/round-52/l1/mknod.2.html`, `s252-l1-open.txt`,
  and `w1/ScribeSources/receipts/`. New row used-by points here rather than to the
  unlanded planned knowledge entry. No existing source cells changed.
- Reject the shared device/FIFO/socket omission explanation in the declaration.
  S252 expressly exempts FIFO/socket from this privilege condition; the previous
  outside spot-check also rejected this inference (`round-51-verifier-spotcheck.md:58-61`).
  Flip: separate measured producer behavior per inode kind, never capability inference
  from an unqualified user identity. R52-C1 remains unverified, not narrowed to devices.
- Reject treating LB4Mknod as an unprivileged test: its character-device creation
  succeeded twice; attempted nobody runs failed before executing the probes.
  `w1/LB4Mknod.md` and its probe receipts retain both outcomes. S252's documented
  condition is not falsified by an execution context whose capabilities were unmeasured.
- Reject freezing the incomplete counter/control/v6/fetcher drafts. ExecCounterV2
  reports missing predicate clauses; ExecTriV6 produced no instrument; ExecFetchVendor
  reports an invalid edited draft; RevFetchGuards leaves deleted-guard proof unmet.
- Reject promotion based on CTL-NEW 4/4 alone. RevGrammarOffline and LB2OfflineClause
  independently reproduce old-rule 2/4 and proposed-law 4/4 on historical envelopes,
  but CritRuleDerive proves alternative device-blind/tolerant rules share that result.
  Those controls neither authenticate fresh carriers nor establish the full predicate.
- Assimilation: none. ScoutMergeThemes scanned the package (77 knowledge candidates,
  132 rows, 44 numeric collisions; see its scan/receipts). Its proposed S252 allocation
  conflicts with the already-declared mknod row. No staged row or entry appended;
  re-grounding/renumbering/mirror gates were not completed. No considerthese directory
  was found by the same scan. Candidate admits remain provisional seat recommendations.
- Outside spot-check: pending; the round's own seats are not non-author verifiers.

## Mistakes

| class | evidence | captured-by | fix / demonstrated limit |
|---|---|---|---|
| stale-premise | plans/round-52-claims.md device/FIFO/socket explanation; previous outside rejection at round-51-verifier-spotcheck.md:60 | QUALITY 96 | Reject the repeated shared inference; S252's EPERM branch is the counterexample. No executable repair claimed. |
| attribution | w1/LB4Mknod.md, probe-receipts.json: device creation succeeds; runuser refuses before probe | QUALITY 96 | Record the context as unmeasured, not unprivileged; the actual success makes the expected EPERM assertion fail. |
| vacuous | w1/CritRuleDerive/findings.md; w1/MutControlsV2/findings.md | QUALITY 79, 94, 95 | Preserve the wrong-rule green witnesses; do not turn CTL-NEW into full-claim credit. No counter fix landed. |
| stale-premise | w1/MutTriV6.md; w1/CritTriV6.md | QUALITY 77, 97 | The proposed before command points at a directory, future-freeze ancestry is incompatible, and new registry paths break unchanged census3. Reject freeze rather than waive these failures. |
| provider | inherited attempt termination, missing completed instruments; r52-w1-results.json | QUALITY 98 | Recover durable seat evidence and file an honest report after settlement. Provider termination does not prove claim failure or success by itself. |
| reference-drift | w1/CritBand.md (rendered dispatch and status-directory blind spots) | QUALITY 76, 79 | Existing checkers are not admitted as prevention; keep missing/malformed status and role-source uncertainty explicit. |

## Claim disposition

C1 before: historical round-50 full predicate matched 2 of 4, exit 1
(`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`). C1 after: unmeasured,
not zero and not 4. C2 before: internal probes identify the one FAILED ddwrt route
but no valid v6 instrument implements the specified exit-1 audit. C2 after:
unmeasured. Production SKILL.md and PROVINCE.md are intentionally unchanged.
All owned-axis scores remain unchanged; no capability is added. This is a
rejected-honest-stop round, not an admitted improvement or a substitute claim.
