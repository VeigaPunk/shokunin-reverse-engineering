# SEAT SC-4 — seat report (chain c2, role scribe), arc3-loop1-round3

Wave `arc3-loop1-round3` · 2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Task (seat line): **LATE JOIN** — C2 records drafts for the parent (LOG +
SCORECARD round sections), pin-free discipline; read `claims/c2/SC-3/ledger.md`
and the EX-2x/RV-x artifacts first; two files under
`claims/c2/records-drafts/`.

Discipline: no git mutations; no writes to `.ufo/gates/custody-pair/` or any
custody path (read-only sha256/stat/capture only); scratch `/var/tmp/sc4-r3`
(never `/tmp`); LOG.md / SCORECARD.md / SKILL.md untouched — patch-text drafts
only. Everything cited below came from a landed file, a command output, or a
sha256 re-derived in this session.

## Status: COMPLETED missing work + VERIFIED existing work

Both draft files existed when this seat joined (written by an earlier SC-4
attempt that stopped before its seat report — no `seats/SC-4.md` existed).
This seat (a) **verified** every before/after number in the drafts against the
raw transcripts and landed artifacts, (b) **completed** the unfilled slots and
corrected three defects found by that verification, and (c) re-ran the pin-free
census simulation on the revised text. The earlier drafts' evidence base was
sound; the defects were in sourcing/counts, not in the measurements.

## 1. Work performed (evidence pointers)

| what | evidence |
|---|---|
| read-first set | `claims/c2/SC-3/ledger.md` (four-hole injection ledger), `seats/EX-21.md`, `claims/c2/EX-29/*` (pre/post pair), `EX-30` patch texts, `RV-5` before/after batteries, `VZ-2` evidence, `EX-28` v1-compat |
| drafts located + verified | `claims/c2/records-drafts/LOG-entry-draft.md`, `scorecard-section-draft.md`; every quoted number re-checked against `/var/tmp/sc4-r3/before-injections.out`, `after-latest.out`, and the landed receipts |
| identity re-derivations (rule #14) | tool `7cd19c3c…` (1155 L) and README `f30df42e…` (185 L) re-derived at 13:22:19Z, 13:23:40Z and at report close; HEAD `c07af80`; census instrument `d0772ce8…` (610 L); receipts `d31ece6f…` (pre), `553fe82d…` (pre-revised), `4969133b…` (post) all `sha256sum -c` OK; sidecar digests == receipt digests |
| gap 1 — churn count corrected | the drafts said "≥12 tool identities / README through 5". Mechanical union of five watcher logs (this seat's 15 s watcher, EX-24 `stable-poll.log`, EX-29 `stability-watch.txt`, EX-33 `evidence/poll.log` + `legC.log`, EX-28 `gate-snapshots.sha256`) = **19 distinct repo-path tool identities** (r2 base + 18 in-window) and **7 README identities**. List: `SC-4/evidence/churn-union3.txt` (`b49db29d…`). (A first late-join recount of mine overcounted at 21 by including receipt digests from legC3 — corrected before it landed anywhere.) |
| gap 2 — D2-stat before-row unsourced | the drafts' before-transcript (pass 1) never executed the EACCES-directory shape; the row rested on a peer's file. Re-measured by this seat: capture `PARTIAL paths=0/1 exit=13`, stanza `EXISTS: no` + `STAT-ERROR: [Errno 13]`, and that receipt then reads `MATCH … exit 0` vs live and vs itself — transcript `SC-4/evidence/before-d2stat.out` (`1754cf97…`, 13:25:22Z) |
| gap 3 — hardlink arm silently never ran | the after-harness's `ln -f` from `$HOME` to `/var/tmp` failed cross-device, so the hardlink row in the after table had no transcript behind it. Re-ran both arms on same-directory scratch links: before `OK exit=0`, X replaced by receipt text (`hl-before.out`, `511d46d0…`); after `USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode)` exit 2, X intact (`hl-after.out`, `396962f6…`) |
| gap 4 — post-pair slots filled | post-pair `receipts/config-post-pair-v2r3.txt` sha256 `4969133b…` = sidecar, captured-utc 13:17:23Z by the revised tool (header self-pins `7cd19c3c…`), 5/5 present exit 0; MATCH 5/5 vs live and vs the round-start pre-pair, with and without `--require-paths 5` (`EX-29/verify-post-vs-live{,-require5}.out`, `verify-roundstart-vs-post{,-require5}.out`, `verify-pre-vs-post{,-require5}.out`, `verify-post-vs-pre-reverse{,-require5}.out`) |
| gap 5 — before selftest sourced | basename-preserving copy of the r2 blob: `CLEAN cases=15 passed=15 failed=0 exit=0` (`selftest-before.out`, `e66f6031…`, 13:25:41Z) — the 15→22 growth baseline is now first-hand, not quoted |
| registry-application state checked | `SKILL.md` still at base `c134afcb…` (390 L), zero `UNEVALUABLE`/`require-paths` hits ⇒ the registry-row patch is apply-ready and NOT yet applied; recorded in both drafts as an open same-commit coupling (honest gap, not smoothed) |
| census sim re-run after edits | `python3 /var/tmp/sc4-r3/census-sim.py <scorecard draft> rev7-final`: base `c8d97713…` PASS / records `a9817f14…` PASS (9 → 9 loci) / control `a5dd6dcb…` FAIL undeclared=1 — zero added loci, detector live |
| artifacts written | `claims/c2/records-drafts/LOG-entry-draft.md` (`4a1d30e1…`), `claims/c2/records-drafts/scorecard-section-draft.md` (`31c00c71…`; literal section `93b221ca…`, 124 lines); `claims/c2/SC-4/evidence/` (transcripts + `SHA256SUMS`) |

## 2. Proposed changes

Patch-text only (this seat writes no real target):

- `.ufo/waves/arc3-loop1-round3/claims/c2/records-drafts/LOG-entry-draft.md`
  — literal append-ready entry for `LOG.md` EOF (after the `arc3-loop1-round2`
  entry; file 1455 L at HEAD).
- `.ufo/waves/arc3-loop1-round3/claims/c2/records-drafts/scorecard-section-draft.md`
  — literal append-ready section for `SCORECARD.md` EOF (after the
  `arc3-loop1-round2` section; file 1496 L at HEAD), plus §2 before/after
  measurement tables, §3 pin-free census simulation, §4 evidence manifest.
- Both files remain **pin-free** in their literal regions (no version literal,
  no `@`-pin, no `path:line` pointer into a mutable file, no client config
  filename; the five custody paths are named as "three client configs + two
  shell profiles"). Measured, not asserted — see §3 of the scorecard draft and
  the attacks below.

No other file was written by this seat.

## 3. Before → after measurement for the chain's claim (C2)

This seat's contribution to the claim's falsifiable pair (all rows measured on
scratch copies; custody paths read-only throughout):

| # | injection | before (`112d01dc…`, 889 L) | after (`7cd19c3c…`, 1155 L) |
|---|---|---|---|
| D2a | capture over exists-but-EACCES file | `PermissionError` traceback, exit 1, no receipt | receipt written with `READ-ERROR`, `UNEVALUABLE paths=1/1 exit=14` |
| D2-stat | path inside EACCES directory | `EXISTS: no` + `STAT-ERROR`, capture exit 13; receipt reads `MATCH` exit 0 in both verify modes | `UNEVALUABLE paths=0/1 exit=14`; verify `UNEVALUABLE exit=14` |
| D2b | that receipt vs itself / vs live | `MATCH paths=1/1 drift=0`, `compared=0/11`, `SHA256-CONTRACT 0/0` | `UNEVALUABLE exit=14` — no fail-open MATCH |
| D2c | `--live`, candidate unreadable after clean capture | `PermissionError` traceback exit 1 | `UNEVALUABLE exit=14`, no traceback |
| D3 | 1-of-5 reference vs live | `MATCH paths=1/1 drift=0 exit=0` (coverage unaccounted; flag unrecognized) | plain `MATCH` by design; `--require-paths 5` → `USAGE … exit=2` |
| WG-a | `--out <custody path>` | `USAGE … exit=2` (guard held) | `USAGE … exit=2` |
| WG-b | `--paths X --out X` | **X clobbered**, exit 0 | refused, exit 2, X byte-intact |
| WG-c | hardlink alias as `--out` | **alias target clobbered**, exit 0 | refused, exit 2, X byte-intact |
| D6 | `selftest --scratch <missing parent>` | `FileNotFoundError` traceback, exit 1 | `USAGE: scratch base is not a directory`, exit 2 |
| L0 | selftest | `CLEAN cases=15 passed=15 failed=0 exit=0` | `CLEAN cases=22 passed=22 failed=0 exit=0` |
| — | post-pair vs live / vs pre-pair | (no revised-tool receipt existed) | `MATCH paths=5/5 drift=0 exit=0`, with and without gate |

Every after-row is from a transcript in `SC-4/evidence/` (sha256s in
`SHA256SUMS`) or a landed file under `claims/c2/EX-29/`; the observation pin
`7cd19c3c…` is a timestamped observation — the parent re-derives the landed
identity at the commit point (rule #14).

## 4. Attacks / refutations attempted, with verdicts

| # | attack | result / verdict |
|---|---|---|
| A1 | "the drafts' before-numbers are the earlier seat's, quoted not re-run" | **refuted** — every number re-checked against the raw transcripts; where the transcript lacked a shape (D2-stat, hardlink, before-selftest) this seat re-measured it and the drafts now cite the new files |
| A2 | "the hardlink after-row is real" | **refuted, then fixed** — the arm never executed (cross-device `ln`); re-ran both arms explicitly, now measured (this is the finding: the original draft's row was unbacked) |
| A3 | "the churn count is whatever the drafts said" | **refuted** — mechanical union gives 19 tool / 7 README identities; both drafts corrected; the intermediate overcount of 21 (my own, from receipt digests) was caught by provenance-checking every hash in the union and does not appear in any artifact |
| A4 | "the pin-free property still holds after the fills" | **confirmed** — census sim rev 4/5/7: records tree PASS, 9 → 9 SCORECARD loci, PROVINCE 6 / SKILL 2 unchanged; control with one planted pin still FAILs (detector live on the same region) |
| A5 | "the registry row landed" (frozen claim's same-commit clause) | **refuted at draft close** — `SKILL.md` is still the base blob `c134afcb…`, 390 L, zero `UNEVALUABLE`/`require-paths` hits; the drafts record the coupling as OPEN rather than asserting the claim's clause |
| A6 | "the post-pair receipt's self-pin is stale" | **refuted** — header `# tool: custody-pair.py  sha256 7cd19c3c…` equals an independent `sha256sum` of the tool at 13:23:40Z; sidecar == receipt digest (`sha256sum -c` OK) |
| A7 | "custody paths were touched by this seat's runs" | **refuted** — all injections on scratch fixtures; the two canonical-path aims (`.bashrc`, `.profile`-alias) were refused by the tool before any write (exit 2); `.profile` nlink still 1, all five custody mtimes unchanged from the round-start state |
| A8 | "the LOG/SCORECARD drafts leak a pin" | **refuted by grep** — literal regions carry no version literal, no `@`-pin, no `absolute/path.toml:NNN`, no client config filename; the only `@`-shaped token in either file is the words "no `@`-pin" in the methodology note, outside the literal region (and that note itself is not appended by the parent) |
| A9 | "the drafts' claim about EX-21's churn history is fabricated" | **partially refuted, then corrected** — the intermediate identities the drafts list are all attested (EX-28 `v1-compat.md`/`gate-snapshots.sha256`, EX-24/EX-29/EX-33 watchers); the drafts' *counts* were wrong, the *chain members* were right; both corrected to the union list |
| A10 | "the drafts double-count the pre-pair as two receipts" | **clarified** — three pre-pair receipts exist by design: round-start (`d31ece6f…`, captured by the r2 revision at 13:06:57Z), revised-tool pre-pair (`553fe82d…`, 13:15:44Z), post-pair (`4969133b…`, 13:17:23Z); the drafts cite the round-start one as the claim's pre-pair and the revised one as a cross-revision control — not a duplicate |

## 5. Blockers

None for this seat's scope. Two open items for the parent (not blockers):

1. **Same-commit coupling is still open**: the registry row is not applied
   (`SKILL.md` at `c134afcb…`). The tool (`7cd19c3c…`, 1155 L) and README
   (`f30df42e…`, 185 L) are in place in the worktree; the row patch texts are
   `claims/c2/EX-30/registry-row.patch.md` (+ `readme.patch.md`) with the
   implementer's revision-pinned form at
   `claims/c2/EX-21/proposed-skill-registry-row.patch.md`. The drafts' literal
   text carries a `⟨PARENT⟩` slot naming this state — fill it with the landed
   outcome, not the intention.
2. **Remaining `⟨PARENT-FILL⟩` slots** in both drafts: C1/C3 phrases and rows
   (single-source them from `claims/c1/records-drafts/` and
   `claims/c3/records-drafts/`), the delivery count (roster reconciliation,
   never the declared 64), the round/wave commit identifiers, and the
   calibration row. Any text added later must be re-measured for pin-freeness —
   one planted pin flips the census to FAIL (measured control).

Scratch residue: `/var/tmp/sc4-r3/` (transcripts + harnesses, kept for
re-derivation). `/dev/shm` selftest scratch dirs are the tool's own and are
cleaned by it. No custody path was opened for writing at any point.
