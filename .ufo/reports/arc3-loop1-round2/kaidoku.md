# arc3-loop1-round2 — kaidoku round report

Date: 2026-10-19. Wave: 64 seats on `opencode-go-2/deepseek-v4.1-flash` (key 2 of
7). **64/64 seat reports delivered** — the arc's first full wave. Seat reports
`.ufo/waves/arc3-loop1-round2/seats/`; claim artifacts
`.ufo/waves/arc3-loop1-round2/claims/`; frozen claims
`.ufo/waves/arc3-loop1-round2/claims-frozen.md` (whose header records one
discarded draft: a roster-arithmetic slip caught parent-side pre-dispatch).

## Work performed

- C1 (depth, owned): rule #14 drafted, adversarially reviewed (decoration
  attack, laundering attack, citation-form audit), dry-run measured on scratch
  trees, and reconciled across six candidate texts; the chain verdict pinned
  the landing condition (form fix required).
- C2 (freshness, fleet): the H1/H3 patch texts from round 1 analyzed against
  the current instrument, merged, implemented (implementer-only real-path
  write), and exercised with a 24-fixture battery; mutation tests prove both
  guards load-bearing; two independent creep audits; frozen-run stability.
- C3 (operability, fleet): custody-pair v2 tool built (implementer-only),
  attacked across 13+ rewrite forms (restore-tool class included), verified
  live (selftest 15/15; pair captures; v1 shapes), registry row drafted and
  merged.
- Cross: connector consistency sweep (all shared readings re-derived
  independently), records reconciliation with census projection, custody
  corroboration, wave-integrator first-hand re-verification of all three
  after-states.

## Landed changes

- `SKILL.md`: queue-drain rule #14 (form-fixed payload) + custody-pair
  registry row + preamble update (work commit `28aa7a9`).
- `SHONEN.md:6`: range `81-243` → `81-255`, `13/13` → `14/14` (same commit).
- `.ufo/gates/c1-census-v10.py`: H1 absent-file guard + H3 blind-instrument
  floor + declared FAIL classes (`d0772ce8…`).
- `.ufo/gates/custody-pair/`: new committed tool + README (`112d01dc…`,
  `fa484d57…`).
- Wave tree `.ufo/waves/arc3-loop1-round2/` committed (pycache excluded).

## Before → after measurements

- C1: command A — rules 13 → 14, 13/13 → 14/14 at the work commit; prior
  rules pure insertion, 0 modified bytes, rstrip-normalized byte-identical.
  The form fix was claim-blocking: the raw payload's bare range failed the
  freeze's rule-#11 clause (reviewer + integrator measured).
- C2: injection matrix (chain harness, re-runnable `tools/battery.sh`) —
  absent-SKILL: PASS silent → FAIL `UNREADABLE`; neutered needles: PASS
  silent → FAIL `BLIND-INSTRUMENT`; ordinary run: PASS 0/0/0/0 both sides;
  scope rows 20 → 20, creep flags [].
- C3: same-content rewrite visibility 0/13 → 13/13 (CR-4 matrix; sha
  contract intact in every row); v1 stanza re-read: LABEL-DEFECT ×5 + exit 12
  with SHA256-CONTRACT 5/5; live pair verify MATCH 5/5 (zero drift across the
  wave for 4/5 paths; the Kimi client config drifted between integration
  captures — recorded as operator-side, the tool's first live catch).
- Custody: 4/5 byte-identical across the whole round; one operator-side drift
  recorded verbatim.

## SHONEN

- [~] SKILL.md real decision tables — 14/14 rule blocks with resolvable
  citations at the work commit (command A); the landed rule #14 is itself
  form-conforming (reviewer-verified); verifier: none non-author.
- [~] End-to-end domain task executed and logged — instrument engineering
  round (census fail-closures + custody tool) with live probes; verifier:
  none non-author.
- [~] Executable without oral context — `custody-pair.py selftest` (15
  cases) and the census battery run verbatim; verifier: none non-author.
- [~] No cross-domain bleed — registry rows state non-validation; safety
  verdicts untouched; verifier: none non-author.

## Notes for the next round

- Rotation amendment (operator directive): the deepseek-v4.1-flash swarms ride the token-plan lanes instead of opencode-go (3 keys, round robin); round 3 = token-plan key 1.
- Named debt: census H2/H4/H5/H6 + partial-needle narrowing; custody D1-D7
  (TOCTOU, EACCES fail-open, verify coverage, receipt self-authentication,
  write-guard scope); the pre-existing dirty `arc2-loop1-round10/C3.md`;
  host `/tmp` quota (standing).
