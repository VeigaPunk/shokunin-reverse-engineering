# SEAT VZ-2 — seat report (chain c2, role convergence, LATE JOIN), arc3-loop1-round3

Wave `arc3-loop1-round3` · 2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
· HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (no seat commits; parent integrates).

Seat line: **LATE JOIN — reconcile the c2 chain end-to-end into `claims/c2/verdict.md`:
the four closures (before/after evidence), selftest count, live pair, v1 back-compat,
regression matrix, patch texts; poll the seats dir; name gaps; adopt and complete
`claims/c2/VZ-2/` if partial.**

**Scope note.** The wave's token-plan lane hit its monthly quota mid-run; this seat
was redirected here as a Devin backfill and joined at ~13:21Z, after the real-path
writes (custody-pair tool + README) had already landed and after most of the chain's
work existed. Per the late-join rules this seat **did not redo landed work**:
it read every landed artifact, **completed what was missing** (the chain verdict,
EX-32's placeholder post-EX-21 measurement, this packet's after-state evidence,
this report) and **independently re-derived every load-bearing measurement** rather
than trusting seat text.

**Explicit declaration:** this seat **COMPLETED missing work** — the c2 chain's
end-to-end verdict (`claims/c2/verdict.md`) did not exist, and neither did
EX-32's post-EX-21 probe reading, this packet's after-state evidence, or the
identity sidecar; all four are now written. It also **VERIFIED existing work** —
every landed artifact of the chain was read and every load-bearing measurement
behind the verdict was independently re-derived on scratch copies (the four
injections on both revisions, the selftest count, the live pair and sidecars, the
v1 shapes, command A, census, probe, EX-27's 41-row battery on both phases,
CR-3's 51-case matrix, RV-5's four sabotage arms). Both verbs apply; neither
half was skipped.

## 1. Work performed (evidence pointers)

**Completions (work that did not exist before this seat):**

| what | where |
|---|---|
| **`claims/c2/verdict.md`** — the chain's end-to-end convergence verdict (the seat line's deliverable; did not exist) | `claims/c2/verdict.md`, 239 lines, sha256 `2a80dfc01b012f96859aecc62fa5eda004836972610cde28d1caa2a31b606bf4` (re-derived after the last revision) |
| **EX-32's §5 post-EX-21 probe measurement** — its `probe.md` carried `PLACEHOLDER`; this seat supplied the reading: scratch clone of `c07af80` + landed tool/README committed as `be8333c` → probe `findings=0` (default + `--strict`), selftest 13/13 | `verdict.md` §Claim-11 row and §Regression; clone at `/var/tmp/vz2/clone` |
| **this packet's after-state evidence** — one re-runnable harness producing both columns verbatim in a single run | `claims/c2/VZ-2/evidence/run-latejoin.sh` (`ac566c0f…`), `latejoin-before-after.out` (`d2262d5f…`, 142 lines) |
| **identity sidecar** for the verdict and every object its claims rest on (rule #14) | `claims/c2/VZ-2/evidence/verdict-identity.txt` (`9fd9f9a8…`) |
| **the R2 clobber finding** (see §5) | `verdict.md` §R2; corroborated independently by RV-9's `rv9-third-party-clobber-observation.out` |

**Adopted-and-verified (pre-existing packet, not re-authored):**
`before-injections.out` (`c6e45443…`), `before-injections-2.out` (`19d565f6…`),
`final-harness-7cd19c3c.out` (`7ea049f4…`), `final-harness-7cd19c3c-prev.out`
(`5f832849…`), `run-before.sh` (`33bfd103…`), `run-after.sh` (`e18789f2…`),
`v1-sums-four-undrifted-paths.txt` (`c5f99132…`). These carry the seat's
pre-interruption before/after work; this seat re-read them, checked the numbers
against its own runs, and **re-ran the harnesses** rather than citing them alone.

**Independently re-derived first-hand at write time (13:22–13:27Z)** — the load-bearing
set behind every verdict row:

- tool `7cd19c3c…` (1155 L, 54279 B) and README `f30df42e…` (185 L, 9603 B) at the
  worktree path; base blob `112d01dc…` (889 L) and README `fa484d57…` (132 L) via
  `git show HEAD:`; `SKILL.md` `c134afcb…` unmodified at 390 L.
- the four injections on **both** revisions (`/var/tmp/vz2/base` vs `/var/tmp/vz2/final`),
  plus hardlink and symlink alias forms; selftest 15/15 → 22/22.
- live pair (this seat's own fresh capture pair, plain + `--require-paths 5`),
  the chain's round pair in `claims/c2/receipts/` in all four directions
  (revised-pre↔post, each↔live, round-start↔post cross-revision), and all three
  sidecars via `sha256sum -c`.
- v1 shapes against live (4-path undrifted control, r1 sums, r1 canonical stanza).
- command A (verbatim SCORECARD recipe) at HEAD: 82/82, `missing []`, `dangling []`,
  14/14, 10.0/10.0; census `PASS 0/0/0/0` at HEAD and on the landed-revision clone;
  citation-drift probe both modes + selftest 13/13 on that clone.
- **re-ran the chain's own harnesses**: EX-27's 41-row regression (both phases),
  CR-3's 51-case type-swap matrix, RV-5's four sabotage arms — results in §3.
- re-derived the sha256 of every patch text cited in the verdict's index.

## 2. Proposed changes

**None authored by this seat.** The real target (`.ufo/gates/custody-pair/`) is
EX-21's write scope; this seat wrote nothing there and nothing under
`.ufo/gates/`. All proposals live in the chain's patch texts, indexed with
re-derived identities in `verdict.md` §Patch texts. No `*.patch.md` was created
by this seat: the verdict's job was reconciliation, and every clause it would
have proposed is already packaged by a chain seat.

## 3. Before → after measurement for the chain's claim

Full verbatim transcript: `VZ-2/evidence/latejoin-before-after.out`
(base `112d01dc…` vs after `7cd19c3c…`, same harness, same host, same minute).

| # | injection (declared class) | before | after |
|---|---|---|---|
| L0 | selftest | `CLEAN cases=15 passed=15 failed=0 exit=0` | `CLEAN cases=22 passed=22 failed=0 exit=0` |
| L1 | D6 `selftest --scratch <missing>` (USAGE) | `FileNotFoundError` traceback, exit 1 | `USAGE: scratch base is not a directory: …`, exit 2 |
| L2 | D2a blocked parent dir (14) | capture `PARTIAL paths=0/1 exit=13` + `STAT-ERROR`; verify **`MATCH paths=1 exit=0`** | capture `UNEVALUABLE paths=0/1 exit=14`; verify `UNEVALUABLE paths=1 exit=14` |
| L3 | D2b chmod-000 file (14) | `PermissionError` traceback, exit 1, **no receipt** | `UNEVALUABLE paths=1/1 exit=14`, receipt written (`EXISTS: yes` + `READ-ERROR`) |
| L4 | D3 1-of-5 (USAGE) | plain `MATCH exit=0`; `--require-paths` unrecognised (exit 2) | plain `MATCH exit=0` (declared default); gated `USAGE` + `REFERENCE-COVERAGE: 1/5 … unaccounted: …`, exit 2 |
| L5 | write guard `--paths X --out X` (USAGE) | `exit=0`, X **CLOBBERED** | `exit=2`, X sha unchanged |
| L6 | write guard, hardlink + symlink alias (USAGE) | both **CLOBBERED** (exit 0) | both `exit=2`, target sha unchanged |
| L7 | live pair + gate | `MATCH 5/5 exit 0`; gate unrecognised | `MATCH 5/5 exit 0` plain **and** `--require-paths 5`; receipts self-pin the tool sha; sidecar `sha256sum -c` OK |
| L8 | v1 shapes | sums 4/4 `MATCH-V1-PARTIAL 0`; r1 sums `CONTENT-DRIFT 10` / `SHA256-CONTRACT 4/5` | identical classes both |
| L9 | custody digests | round-1 pins, path 3 at `bc66d543…` | identical (read-only block) |

**Chain-claim headline:** the four named holes close as their declared classes on
both sides of the matrix; selftest **15 → 22** (bar ≥17); live pair **MATCH 5/5**;
v1 receipts remain sha256-verifiable; command A unchanged at 82/82, 14/14,
10.0/10.0. **Chain verdict: VERIFIED** (`claims/c2/verdict.md`).

**Regression matrix re-run first-hand** (not read):

| harness | this seat's run | result |
|---|---|---|
| EX-27 41-row regression, revised phase | vs the landed bytes | `rows=41 hold=41 fail=0 observed-only=0` — **matches EX-27's recorded tally** |
| EX-27 41-row regression, baseline phase | vs the HEAD blob | `rows=41 hold=37 fail=0 observed-only=4` — the 4 observed rows are the four hole before-states, also matching |
| CR-3 51-case type-swap matrix | landed tool, harness copied to my scratch | **exit-line diffs vs `CR-3/matrix-AFTER2.out` = 0 of 51**; identical case-name set |
| RV-5 four sabotage arms | landed tool | **identical to RV-5's log**: S1 DIRTY (3 named cases), S2 DIRTY (2 guard cases), S4 DIRTY (gate case), **S3 CLEAN with the case missing from the run** (recorded as residual R1, not smoothed) |
| RV-7 5-arm guard mutation matrix | read + cross-checked | both guard arms and the gate load-bearing, each arm failing exactly its own cases |

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the chain's verdict is seat text, not measurement" | **partially sustained, then discharged** — every load-bearing number was re-run by this seat; the chain's own harnesses were re-executed rather than cited. Result: full agreement except one self-caused run (A8 below) |
| A2 | "the 22-case selftest is a rubber stamp" | **refuted** — RV-5's sabotage arms re-run here reproduce DIRTY with exactly the expected failing sets; the 15 legacy cases stay green on both revisions |
| A3 | "the D2 closure is cosmetic" | **refuted** — the fail-open is a *verdict* change (`MATCH exit 0` → `UNEVALUABLE exit 14`), and RV-6's single-hunk mutation restores it while capture-side stays closed |
| A4 | "the guard refuses only the one spelling" | **refuted** — hardlink and symlink aliases refused too, targets byte-intact |
| A5 | "the D3 gate breaks v1/fixture workflows" | **refuted** — opt-in; plain 1-of-5 still `MATCH exit 0`; 5-of-5 under the gate passes |
| A6 | "the receipts' self-pin is stale" | **refuted** — all three `# tool:` lines re-checked against an independent `sha256sum`; sidecars `-c` OK; cross-revision verify shows the pair valid |
| A7 | "C2's edits broke a neighbouring instrument" | **refuted** — census `PASS` byte-identical at HEAD and on the landed clone; probe `findings=0` both modes; command A unchanged |
| A8 | "my baseline regression run is evidence against the chain" | **self-refuted** — my first baseline run showed 8 FAILs; cause found: a **third-party clobber** of a round-1 receipt mid-run (not the tool). Re-run against a pristine clone → 37 HOLD / 0 FAIL / 4 obs. Recorded rather than hidden |
| A9 | "the live pair is stale because the tool moved after capture" | **refuted** — VZ-4's 60 s poller shows the tool at `7cd19c3c…` unchanged from r17 (13:17:30Z) through r41 (13:25:30Z); this seat re-derived the sha at 13:22Z |
| A10 | "the late-landing seat reports contradict the verdict" | **refuted** — EX-23/29/30/31/32/RV-7/RV-9 all landed after the verdict's first write; all were read and none contradicts a row. Three strengthen it (EX-32's isolation matrix + collision case, RV-7's arm isolation, RV-9's six pair directions) and were folded into rev 2 |

## 5. Blockers

**None for this seat.** Three items for the parent:

1. **R2 — third-party clobber of a round-1 historical receipt.** At 13:25:02Z,
   VZ-4's late C2 after-state suite overwrote
   `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`
   (worktree 21017 B / 305 lines, content beginning `== VZ-4 C2 after-state suite ==`,
   vs the HEAD blob `b8ed1936…`, 2045 B / 52 lines). RV-9 independently observed it
   and exonerated itself. **Re-checked at 13:27Z: the worktree file is back to the
   HEAD blob** (2045 B, clean against HEAD) — another seat restored it inside the
   same minute. No restore action is outstanding; the parent should only confirm
   the file is not committed clobbered, and should not quote it from a snapshot
   taken between 13:25:02Z and 13:25:55Z.
2. **Landing order (EX-32's collision case).** If the extended pointer table lands
   together with a registry row whose text the table pins, the row entry reads
   `citation_dead` (EX-32 world G: `60/61 clean`, strict `exit=1`). Take EX-32's
   re-anchored table form (`pointer-table-reanchor.patch.md`) and re-run the probe
   at the work commit. This is C3's instrument, but the row this chain lands is
   one of the two inputs to the collision.
3. **Remaining c2 paperwork.** At 13:27Z the seats dir held 56 files; **SC-3, SC-4
   and RV-5 still lack seat reports** (VZ-2's is this file). All three have landed
   artifacts that were read here and, for RV-5, re-executed — the missing reports
   are paperwork, not evidence. The parent's roster reconciliation counts the
   items array, not this tally.

**Named residuals carried in the verdict** (none voids the claim): RV-5's S3 arm
not load-bearing (the `mkdtemp` `OSError` wrapper masks it — reproduced exactly);
the unguarded derived sidecar path; `out.parent.mkdir(...)` outside the guarded
`try`; the coverage gate counting stanzas rather than distinct paths; the
contract-denominator and self-pin-context proposals; CR-3's W4 wording; the
untracked `__pycache__` residue.

## 6. Identity discipline (rule #14)

Every artifact this seat produced re-derives its own byte-identity **after** its
last revision: `claims/c2/VZ-2/evidence/verdict-identity.txt` carries the verdict's
final sha256 (`f08fa936…`, 240 L) plus the tool/README/base-blob/SKILL/receipt
digests the verdict's rows rest on, each re-derived at write time with the command
listed. That sidecar deliberately does **not** record this report's sha256 (this
report quotes the sidecar; a mutual pair would be a self-referential cycle), so
this report's final identity is the parent's to re-derive at landing — as it is
for every seat report in the wave.

Two stale citations were caught and corrected by this discipline: EX-30's two
patch drafts were re-emitted at 13:25:56–58Z after this seat's first hash read
(the verdict quotes the re-read identities `29c5dd82…`, `353ff2b6…` and discloses
the re-emission); and the verdict's own rev-1 identity (`2a80dfc0…`) was
invalidated by a rev-2 tally edit, superseded in the sidecar by `f08fa936…`.
