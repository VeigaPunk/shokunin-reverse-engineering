# RV-6 — seat report (chain c2, reviewer seat, wave arc3-loop1-round3)

Task: **mutation-test D2** — revert only the EACCES closure on a copy → the
fail-open MATCH returns (load-bearing proof).

Verdict: **CONFIRMED on the landed revision.** Removing only the D2 closure —
down to the single 8-line verify-side guard — restores
`VERDICT: MATCH paths=1/1 drift=0 exit=0` on an exists-but-EACCES path, while
the unmutated landed revision returns exit 14 in every EACCES shape. The closure
is load-bearing.

## 1. Work performed (evidence pointers)

All work on copies under `/var/tmp/rv6/` (never `/tmp`). This seat wrote nothing
under `.ufo/gates/` — the real target was read-only for RV-6.

Revisions under test (sha256, all re-derived 13:15:59Z — full list in
`claims/c2/RV-6/identities.txt`):

| arm | what | sha256 |
|---|---|---|
| base | HEAD tool (round-2 revision) | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` |
| closed | base + EX-40 `proposed-edge-classes.patch` | `4aedb0307f8313e77f8d3b3cdf6df82e44ba6865748dda2d0fdf572e0cc349e2` |
| M1 | closed − 4 closure hunks | `f000cf81d685e354c38a40f05677971289c779e2148a75bfb2c5807576375c93` |
| M2 | closed − verify-guard hunk only | `d0becae7b293bc54d7b42a1795e714146c08cfcda9201db2b763c719d01ea1a4` |
| landed3 | **EX-21's landed round-3 tool** (live at 13:16:16Z) | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` |
| LM1 | landed3 − 7 D2-closure runtime hunks | `d9dc097abb09b6b10d9a9cf7a16152c043749d6c7e44c0c405de774dbe80e589` |
| LM2 | landed3 − verify-guard hunk only | `16d4a05d300f21001b5f3139ad50700ebf4ebe240c9c78a5016966e6189d7808` |

The `closed` copy applied EX-40's patch cleanly and is **byte-identical** to
EX-40's own recorded patched identity (`4aedb030…`) — an independent
reproduction of their generator output. `landed3` is the same revision EX-21's
own receipts self-pin (`# tool: custody-pair.py sha256 7cd19c3c…`), so the
mutation targets are the implementer's actual bytes, not a stand-in.

Harness: `claims/c2/RV-6/tools/inject.sh` — four injections + a
receipt-vs-receipt variant, identical fixture and commands per arm:
blocked dir (mode 000, lstat EACCES); chmod-000 file (open EACCES); mixed
good+unreadable capture; `verify --live`; `verify A B`. Plus
`tools/map-sweep.sh` (declared-exit-map sweep) and `tools/mutate.py`
(content-pattern hunk selection → revert patch → reverse-apply; index-free, so
the mutation survives revision drift). Logs: `claims/c2/RV-6/logs/*.inject.log`,
`*.selftest.log`; receipts: `claims/c2/RV-6/receipts/`.

## 3. Before → after (my slice of the c2 claim: D2 injections)

| shape | base `112d01dc` | landed3 `7cd19c3c` | LM1 (7 hunks reverted) | LM2 (1 hunk reverted) |
|---|---|---|---|---|
| capture EACCES-at-lstat | exit 13, `EXISTS: no`+`STAT-ERROR` | exit 14 UNEVALUABLE | exit 13, `EXISTS: no` | exit 14 |
| `verify --live` both-EACCES | **MATCH exit 0 (fail-open)** | UNEVALUABLE exit 14 | **MATCH exit 0** | **MATCH exit 0** |
| `verify` receipt-vs-receipt, both EACCES | **MATCH exit 0 (fail-open)** | UNEVALUABLE exit 14 | **MATCH exit 0** | **MATCH exit 0** |
| `verify --live` chmod-000 file | traceback, exit 1 | UNEVALUABLE exit 14 | traceback, exit 1 | METADATA-DRIFT exit 12 |
| mixed capture | crash, no receipt | receipt survives (2 stanzas), exit 14 | crash, no receipt | receipt survives, exit 14 |
| selftest | 15/15 exit 0 | 22/22 exit 0 | 17/22 (5 fail) exit 3 | 19/22 (3 fail) exit 3 |
| declared-map sweep | 2 out-of-map (`1`) | all declared (incl. D6 → USAGE 2) | 1 out-of-map (`1`) | all declared **but fail-open live** |

The single-hunk LM2 is the sharpest statement: **removing the 8-line
`compare_section` guard alone** (landed hunk `@@ -425,6 +482,14 @@`, lines
`ref_uneval = bool(...)` through the `UNEVALUABLE` return) restores
`VERDICT: MATCH paths=1/1 drift=0 exit=0` while the capture-side closure stays
intact — the fail-open lives on the verify path, and that guard is the line that
kills it.

Precision (identity discipline, re-derived): `diff landed3 LM1` = exactly 7
hunks; `diff base LM1` = 16 = 23 − 7, i.e. the non-closure hunks only;
`diff landed3 LM2` = exactly 1 hunk. The mutations remove the closure and only
the closure. Same containment shown for the EX-40 closure (M1 4 hunks / M2 1
hunk).

## 4. Attacks / refutations attempted, with verdicts

- **A1 — closure over-triggers.** A genuinely absent path (ENOENT, no error
  recorded) must stay MATCH: held on base, closed, M2 and landed3/M1/LM2
  (`receipts/absent.txt`, exit 13 capture / MATCH 0 verify). The guards key on
  recorded `STAT-ERROR`/`READ-ERROR`, not on `exists=no`.
- **A2 — fail-open return could be caused by the other 16 hunks.** Refuted:
  base (0 closure hunks) shows the identical fail-open, and `base → LM1`
  contains no closure hunk while reproducing base's behavior case-for-case.
- **A3 — capture-side closure is the load-bearing part.** Refuted by LM2/M2:
  reverting only the verify-side guard restores MATCH while capture stays closed.
- **A4 — residual, verdict OPEN (for EX-21/parent):** a genuinely-absent pair
  still verifies `MATCH exit 0` at the landed revision (both-sides ENOENT is
  exit 0, and the verifier line says `MATCH paths=1/1 drift=0`). The D2 claim
  closes the EACCES class only; whether "absent=absent" should print MATCH (or a
  weaker "AGREE-ABSENT") is a semantic call, not a regression. Named.
- **A5 — EX-40's proposed closure is sufficient.** Refuted first-hand: with the
  EX-40 closure applied, a **receipt-vs-receipt** EACCES pair still reads
  `MATCH exit 0` (`closed` case2rr) because the parser does not carry
  `STAT-ERROR` from the receipt text. EX-21's landed revision fixes this (parser
  hunks + guard) and returns 14 — verified.
- **A6 — declared-map conformance is enough to detect D2.** Refuted: LM2 passes
  the declared-exit sweep with every exit in-map while the fail-open MATCH is
  live. The mutation test, not the map sweep, is the D2 detector.

## 5. Blockers, gaps, follow-ups

- **Cross-check gap:** EX-21's seat report (`seats/EX-21.md`) had not landed at
  13:16Z; its *artifact* tree is landed (receipts/transcripts/selftest/matrix/
  `proposed-skill-registry-row.patch`) and its receipts self-pin
  `7cd19c3c…` = my mutated revision, so the mutation is against its real bytes,
  but the declared-class wording in its report was not available verbatim.
- **Re-derivation rule #14:** all identities above re-derived at 13:15:59Z; live
  tool re-checked 13:16:16Z still `7cd19c3c…`. If EX-21 writes the tool again
  before the round's work commit, the mutation must be re-run against the new
  sha: `python3 tools/mutate.py <base> <newtool> <outdir> {full|guard}` then
  `tools/inject.sh` — one command each; the selection is content-patterned so it
  does not depend on hunk indices.
- **A4** above is the only open semantic item this seat names.

## 2. Proposed changes (patch-text paths or "none")

**None.** Reviewer seat: no proposal to land. The revert patches under
`claims/c2/RV-6/mutations/` (`landed-m1-revert-closure-7hunks.patch`,
`landed-m2-revert-verify-guard-1hunk.patch`, `m1-…`, `m2-…`) are mutation
artifacts, not proposed edits; applying any of them to the landed tool would
re-introduce a measured defect.