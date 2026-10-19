# EX-05 — census interplay test of EX-01's rule-#14 patch text, arc3-loop1-round2

Seat: EX-05, chain c1, executor. Scope: does appending EX-01's rule #14 to the
queue-drain craft section introduce any token the census instrument counts?

**Verdict: no.** Under both payload revisions (v1 896 B, v2 1,071 B) and both
census revisions available (`6f1d19ff…` committed, live revisions
`82fb807e…`/`df9ffdf9…`/`a4c16763…`), the treated scratch root reads
`PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` with per-file loci
**unchanged (SKILL 2, PROVINCE 6, SCORECARD 9)**; the full `--json` delta is 0
apart from the benign `SKILL.md lines=` growth.

## Method

1. Scratch root `/var/tmp/ex05-r2/{baseline,treated,treated2,control,clean}-root`
   — copies of `PROVINCE.md`/`SKILL.md`/`SCORECARD.md` at HEAD `14b1682b`
   (`SKILL.md` pre-image 371 lines,
   `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb`).
2. Apply EX-01's payload from the artifact per its §2 anchor recipe:
   `python3 claims/c1/EX-05/apply-rule14-from-artifact.py
   claims/c1/EX-01/rule14.patch.md <root> <payload-sha> <skill-sha>`
   — extracts the marker-delimited payload, asserts the requested identities,
   inserts it after the `kernel-OOM-killed (…)` line (239).
   v1 → `SKILL.md` 385 lines `19057c13…`; v2 → 387 lines `a8170b96…`; anchor
   hits 1 in both; lines 1–239 byte-identical afterwards (`cmp`).
3. Census: `python3 .ufo/gates/c1-census-v10.py --root <root> [--json|--quiet]`
   plus the committed revision (`git show HEAD:… > /var/tmp/ex05-r2/instrument-head-v10.py`).
4. Independent checks: `needle-scan.py` (line-level, census's own four needle
   patterns over the diff's added lines), `payload-token-scan.py` (imports the
   census and runs its `classify()` on the payload alone),
   `census-delta.py` (locus-class delta between two `--json` runs),
   `commandA-worktree.py` (recipe A, source swapped to a worktree read).

## Results (outputs in `evidence/`)

| Check | Result |
|---|---|
| census baseline (live `a4c16763…`) | `PASS 0/0/0/0`, `SKILL.md lines=371 loci=2` |
| census treated v1 / v2 (live) | `PASS 0/0/0/0`, `lines=385/387 loci=2` |
| census treated v1 / v2 (committed `6f1d19ff…`) | `PASS 0/0/0/0`, `loci=2` (v1 reproduces EX-01 §3) |
| JSON delta baseline→treated (same revision) | `DELTAS=0`; only `lines SKILL.md 371 -> 387 (benign)` |
| native payload scan (census `classify()`), v1+v2, both revisions | `needle_total=0 loci_records=0 record_classes=[]` |
| line scan of applied diff | v1 `added_lines=14 needle_hits=0`; v2 `16/0` |
| command A (worktree variant) | 13 → **14 rule blocks, 14/14 citation-resolved**, `mapped 82/82`, `missing []`, `dangling []` |
| alt insertion position (before `## Config custody…`) | `PASS`, `loci=2`, `lines=385` |
| **positive control** (rule text with `rea-agents@6.7.0` + `~/.kimi-code/config.toml:1290`) | `FAIL`, `undeclared=1` at `SKILL.md 242-246`, `loci 2→3`; native scan 6 needles / 1 UNDECLARED record |
| real repo, unpatched, live instrument | `PASS 0/0/0/0` (`evidence/census-real-head.txt`) |

The positive control is what keeps this verdict from being vacuous: the same
pipeline, on a token-bearing text, reads a declared FAIL — so the PASS above
is a measurement, not an absence of observation.

## Identity discipline (rule #14 applied to its own patch)

The artifact under test was revised mid-wave (v1 → v2). This seat re-derived
both generations from the artifact rather than trusting the record:

- v2 artifact `rule14.patch.md`: 11,084 B `885fa537…`; payload 1,071 B
  `6cc388cb…`; patched scratch `SKILL.md` 387 lines `a8170b96…`.
- At `12:14Z` the sidecar `identity-final.txt` still described v1 (8,833 B /
  896 B payload / 385 lines) — a live instance of the rule's own defect class.
  EX-01's `12:14:21Z` re-derivation closed it; all three v2 identities then
  matched this seat's independent re-derivation exactly
  (`evidence/ex01-identity-recheck.txt`).
- Integrator: land the **v2** payload and re-derive the fresh `SKILL.md`
  identity at landing; refresh `SHONEN.md:6` (`81-243`/"13/13" → `81-254`,
  14/14; craft heading `258` in v2) in the same commit.

## Evidence index (`claims/c1/EX-05/evidence/`)

`rule14.diff`, `rule14-v2.diff`, `needle-scan-treated.txt`,
`needle-scan-treated-v2.txt`, `needle-scan-control.txt`,
`payload-token-scan-{live,committed,control}.txt`, `payload-token-scan-v2-live.txt`,
`census-{baseline,control,clean,treated}-live.json`,
`census-treated-v2-live.json`, `census-treated-alt2-live.json`,
`census-{baseline,control}-live4.json`, `census-treated-live.txt`,
`census-treated-v2-live.txt`, `census-treated-committed-rev.txt`,
`census-treated-v2-committed-rev.txt`, `census-real-head.txt`,
`delta-baseline-treated.txt`, `delta-baseline-treated-v2.txt`,
`delta-baseline4-treated2.txt`, `delta-baseline-control.txt`,
`apply-output.txt`, `apply-v2-output.txt`, `prefix-and-diff-comparison.txt`,
`shonen-range-check.txt`, `probe-head.txt`, `instrument-rev-live.txt`,
`instrument-rev-committed.txt`, `ex01-identity-recheck.txt`.
