# Round 92 — lesson: a last-block stop-boundary tamper is repaired by the packer's own verdict inside a declared window; the refusal counter stops admitting the three named counterfeits, and not the wider class

Declaration `11f8606178dfd9e72001b31daf412c5463106a63` (`plans/round-92-claims.md`, `.ufo/waves/round-92/claims.json`); base `73a882712907606eba074377b536c6dd82517e25`; candidate commit `a3d3c649ddfef2b4c850ec950e9f633194f08efc` (the measured revision). Wave `r92-w1`: 12 seats, one v1 wave, none dead. Claims: R92-C1 (coverage, capability), R92-C2 (calibration, measured overreach).

## Gate

**Sources opened this round (CORPUS.md rule 1).**

| row | URL | access date | HTTP / size / sha256 | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S313 | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp | 2026-11-05 (re-opened by ScoutSource; sha re-derived) | 200 / 24181 / `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | line 496 `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` | the bound and payload read in the knowledge entry; the entry does not credit S313 with the stop-boundary verdict |
| S317 (new) | https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp | 2026-11-05 (opened by the lane; `curl -fsSL` exit 0; lines re-read by `sed -n 8055,8070p`) | 200 / 373743 / `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` | line 8065 `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` | the caller's end-of-file trailer check that decides the stop boundary |

**Row changes (old → new, CORPUS.md rule 2).** S313 `used-by`: `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md, corpus/knowledge/2026-11-05-r91-stop-boundary-refusal.md` → `…, corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md`. S313 `status` `mined` → `mined`; `recheck` `on-release` → `on-release`; `opened` unchanged (2026-11-04). S317 added (tier A, `mined`, opened 2026-11-05, recheck on-release, used-by the round-92 entry). The S313 teaching sentence is not edited: its caller caveat is recorded in the knowledge entry's Limit 8.

**Admit / reject.** Admitted: S313 (scope re-ground, quote located by the scout and checked against the fetched bytes); S317 (the lane's own opening; both quotes located). Rejected: none this round. The scout found that S313's scope claim "every executable carrier" is too broad (`PackLinuxI386` and `PackBSDI386` inherit `PackUnix::unpack`, which has its own loop); that wording is not used in the entry.

**Assimilation.** `merge/kaidoku/` is absent and the lane has no `considerthese/` directory: `Assimilation: none`.

**Census (frontier step §2b).** Before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `ok`, 221 registry rows, 29 `W04` (`.ufo/waves/round-92/census-before.txt`). After the S317 append: exit 0, `ok`, 222 rows, 30 `W04` (the new S317 duplicates the S311 URL with a distinct scope; a warning, not an error). `E01/E03/E04` findings: none.

**Spot-check.** Pending the non-author closure (`corpus/lessons/round-92-verifier-spotcheck.md`, not written by this lane).

## Measured (frozen counters, at `a3d3c649`)

- R92-C1: `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, met True, exit 0 (`.ufo/waves/round-92/l1/scores/c1-at-a3d3c649….json`). Do-nothing control at base: `repaired 0 of 10 …`, met False (`pre/c1-control-do-nothing-round91-repair.json`).
- R92-C2: v2 positive control (round-91 tool) met True; the three named counterfeits met False (A `intact 4 of 5`, B `intact 4 of 5`, C `typed 0`): admitted 0 of 3. Before, the round-91 label admitted 3 of 3 (`pre/c2-do-nothing-v1-counterfeit-*.json`).
- Round-90 regression on the candidate: `P1 6 of 6; P2 4 of 4; P3 4 of 4`, met True (REA control true). Base (round-91 tool) met True (`pre/regress-base-round91-repair.json`).
- Premise probe (ExecProbe): one packer-green value per carrier, equal to the stored value, in `[stored±16]`; `stored±40` red; packing byte-deterministic.
- Supplementary (not frozen): candidate on `bzip2`, `gzip`, `patch`: near ±7 repaired 2 of 2 each; far ±40 refused 2 of 2 each (`.ufo/waves/round-92/l1/scores/supp-unseen-carriers-at-a3d3c649….json`).

## Mistakes

Each row: class · evidence pointer · captured-by · fix.

- **M92-a · report figure not equal to its receipt (round-91 D-91-1).** The round-91 report says "7 W04 duplicate-URL warnings"; `.ufo/waves/round-91/l1/census-before.txt` carries 29 `W04` lines. Evidence: `.ufo/reports/round-91/kaidoku.md` (Sources & frontier) against that receipt. Captured-by: `none`. Fix: QUALITY 187; sweep `.ufo/waves/round-92/w1/ScribeQuality/sweep-w04.sh <report> <receipt>`. Shown able to fail: the real round-91 report against its receipt → `DISAGREE: report 7 != receipt 29`, rc 1; the corrected fixture `fixtures/f2-report-real-sentence-29.md` → `agree`, rc 0. The round-91 report is not edited; this entry and the correction below carry the fix.
- **M92-b · geometry assumed, not measured (first draft).** The candidate's first draft assumed the chain ends at the PackHeader and gated the last-block spot on a residual under 12 bytes. The chain ends 1.1 KB to 343 KB before the PackHeader on all five carriers, so the draft refused all twenty cells. Evidence: `.ufo/waves/round-92/w1/ExecRepair/probe1-firstdraft-failure.json`; the fix receipt `probe2-green-census.json`. Captured-by: `none` (the round-90 walker's end-of-chain behaviour was not measured before the round-91 claim named the class). Fix: the walk's `blocks[-1]` is the tamper site in both directions; the probe showed one green per cell.
- **M92-c · headline wider than the measured set (calibration).** The plan's R92-C2 headline said the refusal label "stops admitting counterfeit refusals". The counter admits two five-carrier counterfeits: CHEAT-D (carrier read over five carriers) and CHEAT-E (five-entry table), `met True`. Evidence: `.ufo/waves/round-92/w1/CriticClaims.md` §(c2); `.ufo/waves/round-92/w1/MutCounter.md` LIM-1, LIM-2. Captured-by: `none` (the claim's declared limits named "an unseen-carrier table", but the headline did not). Fix: the headline is narrowed to "stops admitting the three named round-91 counterfeits" in SCORECARD, the knowledge entry and the report; the frozen predicate is unchanged.
- **M92-d · frozen C1 label admits a pinned-image repair (named, not fixed).** A repair that writes the five pinned packed images and refuses otherwise meets `repaired 10 of 10` (critic `c1-table-repair-5.json`, met True; MutCounter N1i; the ReviewerRepair HIGH). Captured-by: `none` (the counter cannot see the decision rule). Fix: the claim's C1 credit is scoped to "five pinned carriers"; the out-of-set probe is supplementary evidence; the frozen counter is not edited. A fresh-pack oracle is routed to round 93.
- **M92-e · host dependency absent (the regression counter's preflight).** The round-90 regression counter stopped at `rea_pin` (the pinned REA package was absent), then with the package extracted but without runtime dependencies the `rea` control was false (`zod` not found). Evidence: `.ufo/waves/round-92/pre/regress-base-round91-repair.json`; the fail receipts in scratch. Captured-by: the counter's own preflight and controls (existing). Fix: `rea-agents@6.5.0` fetched with `npm pack` and extracted to `~/.local/share/rea-agents/6.5.0`; its `package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` matches the counter's pin; runtime dependencies installed with `npm install --omit=dev --ignore-scripts` in that directory (`package.json` unchanged after install). Base regression then met. Recorded as a tool install in the report.
- **M92-f · control receipts sent to `/` (L1 shell).** Variables assigned in a backgrounded `&&` chain were empty in the subshells, so redirects resolved to `/` and failed with `Permission denied`; no receipt was written to a wrong place. Captured-by: the exit codes (existing). Fix: explicit exported variables on their own line before the runs.

## Routed defects — dispositions (round-91 non-author spot-check §5)

- **D-91-1** (report count 7 vs receipt 29): fixed by M92-a, QUALITY 187 and the sweep; the round-91 report stays as written.
- **D-91-2** (trend vocabulary "mixed"): this round's report uses `improved | harmed | unchanged | unprovable-but-better` only.
- **D-91-3** (block 31 row 3 cites QUALITY 169, which does not state "never refuse an intact input"): **not fixed this round, on purpose.** A correction needs a new craft-block revision or a superseding criterion; depth is not claimed this round, and widening the round to depth would add a third claim the frozen plan does not carry. Routed to round 93 with the same frozen-predicate discipline.
- **D-91-4** (the round-91 label accepts an rc-1 exit and two cheats): answered by R92-C2 (`tools/round-92/stop-boundary-battery-v2.py`, the typed rc-2 assertion and the unseen carrier) and QUALITY 185–186. The two cheat arms are measured as admitted under v2 only where they hold a five-carrier list (M92-c).
- **D-91-5** (README round-91 row "six own errors mined"): fixed; the row now reads eight (M91-1..M91-8).
- **M91-8** (the refusal is a policy, the class is decidable): answered for the declared ±16 window by R92-C1; the far class stays refused.

## Named limits (carried to round 93; none closed here)

1. **Pinned-image table passes the frozen C1 label** (M92-d). Fix: a fresh-pack oracle in the counter; the frozen counter is not edited this round.
2. **Membership counterfeits over the public carrier set pass v2** (CHEAT-D, CHEAT-E; M92-c). Fix: the same fresh-pack oracle; the claim's limit names them.
3. **The two-green branch has no measured instance.** A ±64 sweep around the pristine value found no second green (`ExecRepair.md`); the refusal is code, not measurement.
4. **Inherited from round 91, unchanged by the candidate.** The walker's cost is quadratic in fruitful records and is not bounded by the 256 MiB cap in practice (SentinelRepair F-C1, HIGH; QUALITY 183). No aggregate budget over the 33 verdicts (F-C2, MED). `--out` written through an ancestor symlink lands outside the work tree with rc 0 (F-A3, MED). A missing `TMPDIR` falls back to `/tmp` (F-B1, MED). `--out` as a symlink at the final path is replaced silently (F-A1, LOW, target safe).
5. **Window cap.** The frozen far arm measures `±40`; deltas 17–39 are not in the frozen counter. The critic measured `±17..±56` refused through the round-91 tool on `jq` and `xz` (`receipts/p2-r91-refusal-probes.json`).
6. **Non-ELF packed inputs** (PE, Mach-O) are not measured. The host UPX refuses a .NET DLL as `unsupported machine 0xfd1d`.

## Wave `r92-w1` — seat results (12 seats, none dead)

- **ExecRepair (executor).** Built the candidate in a clone; frozen C1 label met on its first counter run after one design fix from its own probe. Selftest 6 cases, 0 failures. Candidate sha256 `ce1b1769…70c1`.
- **ExecProbe (executor).** Premise holds on five carriers (one green, equal to stored; far red; deterministic pack). `premise.json`.
- **ExecCounterAudit (executor).** Reproduced 8 of 8 control receipts; all pins match; CHEAT-B table equals fresh packs; CHEAT-A/C equal the round-91 critic definitions except the path. Attack: the calibration counter admits five-carrier counterfeits (M92-c).
- **ScoutSource (scout).** S313 re-opened (sha and lines match); master drift at 506; the row's "every executable carrier" wording is too broad; the stop boundary is decided by the caller (S317).
- **ScribeKnowledge (scribe).** Draft knowledge entry; numbers left as placeholders for the L1 (the landed entry uses the L1's measured values).
- **ScribeQuality (scribe).** Drafts for rows 184–187 and the M92-a row; the W04 sweep with a fixture. Integrator advice on folding 186/187 into rows 152/150 was not followed: the rows stay separate and the overlap is recorded in their Attack notes.
- **ReviewerRepair (reviewer).** HIGH: a pinned-image table passes the C1 label (named limit, M92-d). MED: `out == packed` without a packer call (the candidate does call `upx -t`; the counter does not).
- **ReviewerContract (reviewer).** No mis-measurement in C2; the parser is key-presence only; plan wording: the `len(scored) == 10` arithmetic is not spelled out next to the label (documentation nit, recorded).
- **CriticClaims (critic).** Fair in declared scope once narrowed: C1 "five pinned carriers, window as a coverage cap"; C2 "the three named counterfeits"; the do-nothing control is the predecessor refusal, not a no-op (the identity no-op also fails under the same counter).
- **MutCounter (mutation-tester).** 9 of 11 assigned mutants killed; survivors are LIM-1, LIM-2 (C2) and N1i (C1); extras X1, N4i killed; controls behave.
- **SentinelRepair (sentinel).** Findings F-C1 (HIGH, inherited), F-A3, F-B1, F-C2 (MED), F-A1, F-A-TOCTOU, F-B2, F-B3, F-C-ok, F-D1 (LOW). Routed to round 93 (named limit 4).
- **ConnectorOverlap (connector).** No sibling claims the class; `search-repair` and `stop-boundary*` names exist only in kaidoku. Adjacent: revenger's round-73 host probe records `upx 5.2.0`; cited in the knowledge entry only as host corroboration, not as evidence of the class.

## Lane gains

- Capability row enters: `last-block stop-boundary repair (window ±16, packer-verdict uniqueness, five pinned carriers)` — the candidate runs, its selftest passes, and its counter labels are met at `a3d3c649`.
- Calibration: the round-91 refusal label is no longer the only counter; v2 is the instrument for the refusal class (rc 2 typed, unseen carrier).
