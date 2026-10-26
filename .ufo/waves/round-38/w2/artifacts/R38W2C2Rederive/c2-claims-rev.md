## R38-C2 — calibration: self-assessment surfaces vs observed repo state

**Predicate P38-C2.** At the measured revision, the lane's current self-assessment surfaces —
the SCORECARD `## Owned axes` rows, the SCORECARD `## Capabilities` table rows, the SHONEN.md
boxes, and the PROVINCE.md `## Core` and `## Frontier` rows — carry zero mismatches with
observed repo state: every backticked lane-repo pointer in them resolves at that revision (path
exists, line range inside the file), the four stated counts equal the counts the lane's command
A / command B observe at that revision, and the three stated section ranges equal the observed
heading-to-last-non-blank-line ranges; with no unit removed, no fewer pointers than at the
base, and every pointer unresolved at the base repaired by a resolving pointer to the same
document.

- Before (base `77091b49`): **1 mismatch** — `evidence/doctor/` in the PROVINCE Core `REA MCP
  server` row does not resolve; the intended document is the committed
  `.ufo/waves/round-19/evidence/doctor/` tree (doctor-6.5.0.txt, doctor-6.7.0.txt).
- **Target:** `mismatches == 0` and `guards_ok` (`met_target`).
- **Counting command:**
  `python3 -I -B tools/round-38/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --base 77091b492cc53f8743bd0701b1e7d5e66123dd84 --json-out <RECEIPT>`
- Selftest: `python3 -I -B tools/round-38/c2-counter.py --selftest` — 14 cases (1 green; red:
  do-nothing, junk count, deleted count, deleted pointer, substitution by another document,
  unresolved province pointer kept, box removed, craft range off by one, Adjacent range wrong,
  range beyond file, new unresolved pointer, wrong calibration count, wrong SHONEN count).
  Wave-1 disclosure (R38ExecSelftests): several red cases fail via `guards_ok` rather than the
  named clause, and three cases use paths the LANE allowlist rejects — disclosed, not repaired
  in frozen bytes.
- **Kill rule:** a frozen control meeting the target stops C2 before data: CTL-C2-0
  do-nothing at the base, CTL-C2-1 junk counts, CTL-C2-2 delete the bad pointer, CTL-C2-3
  substitute other resolving documents — all exit 1. A miss at the measured revision is an
  honest stop; no counter change after this commit.
- Separability: C2 reads SCORECARD/SHONEN/PROVINCE/SKILL/README/knowledge/result.json only,
  and never touches C1's receipts or carriers. C1 reads none of SCORECARD/SHONEN.

## Frontier step (§2b), assimilation, routed defects
