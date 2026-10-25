# Round 35 — declared claims (frozen before data)

Base revision: `aa04633a686d49756763b1feed4be6830d5bb479` (lane tip; clean, pushed).
Owned axes at base: coverage 10, depth 10, calibration 10 (finite proxies, none retired) —
a tie makes every owned axis a lowest axis; no stagnation waiver needed. This is a fresh-start
round after three straight rejections (r32 text presence, r33 provider hold, r34 fixed-offset
replay): every claim below is sized so a do-nothing control cannot reach it, and both counters
are committed before any data.

Assimilation duty (§10): one theme from `merge/kaidoku/` — the **`.jsc` → source mapping**
frontier (`PROVINCE.md` Frontier bullet "`.jsc` → source mapping"); preferred over the
sasquatch/unblob theme because its two candidate entries cite only external, now-fetched
sources (S125/S129), avoiding own-work measurement rows we can no longer re-run. This lands as
claim C1 (coverage). `considerthese/` does not exist in this lane → one report line says so.

## Claim C1 — coverage: jsc2js mapper enters Core (assimilation)

**After-state (one concrete value):** at the measured revision, both of these land:
- `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md` — opens with the provenance
  trio and cites new row **S125**;
- `corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md` — opens with the provenance
  trio and cites new row **S129**;
- `corpus/SOURCES.md` rows S125/S129 exist, `status=mined`, `opened=2026-10-25`, `used-by`
  naming the corresponding entry;
- `PROVINCE.md` carries a Round-35 Core-addition table row naming both entry stems;
- `corpus/README.md` coverage map holds both entry filenames.

**Counting command:** `python3 -I -B tools/round-35/c1-coverage-counter.py --root <LANE> --freeze <freeze-rev> --rev <measured-rev> [--json-out <receipt>]` — exit 0 iff all checks pass; exit 1 with named failures; exit 2 unevaluable (claims absent/unparseable/predicate mismatch).

**Controls (scored before data):** do-nothing = base revision (entries absent → fail); junk-row = an entry file that lacks the trio or cites the wrong row fails; one-entry-only fails; the counter reads immutable git objects only (`git show`/`ls-tree`) — no worktree, no REA run, no source fetch at score time.

**Kill rule:** any frozen check failing at the measured revision stops the claim (honest stop; no re-freeze/relabel). Sources were opened and captured in prep before the freeze (captures in `.ufo/waves/round-35/prep/jsc-sources/`).

## Claim C2 — calibration: round-34 routed record defects closed

**After-state (one concrete value):** at the measured revision, all four round-34 verifier-routed record defects (D-1..D-4, `corpus/lessons/round-34-verifier-spotcheck.md`) are closed:
- **D-1** — the round-35 census-start receipt `.ufo/waves/round-35/assimilation/census-start.txt` is committed no later than the first commit that changes `corpus/SOURCES.md` after the base, and carries the base count (rows=106, EXIT=0, 9 W04 warnings);
- **D-2** — `corpus/lessons/round-35.md` records the r34 w2 seat-accounting correction (31/32 reports; `AAdjacencyCite` unreported) and a line `Seat accounting (round 35): spawned=<N> settled=<M> dead=<K>` identical to the totals in the committed settle receipts `.ufo/waves/round-35/w1-settle.json` + `w2-settle.json`;
- **D-3** — `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` carries an appended provenance trio (`source:`/`verified-at:`/`recheck:`) citing S106;
- **D-4** — every data row of the round-32 and round-34 run-6 instrument-registry tables in `SKILL.md` has exactly 8 cells (NF=9).

**Counting command:** `python3 -I -B tools/round-35/c2-calibration-counter.py --root <LANE> --base <base-rev> --freeze <freeze-rev> --rev <measured-rev> [--json-out <receipt>]` — exit 0 iff all four pass; exit 1 with named failing IDs; exit 2 unevaluable.

**Controls (scored before data):** do-nothing = base revision (all four fail); junk = a lesson line whose numbers mismatch the settle receipts fails; an 8-cell table with a 5-cell row fails; the counter reads immutable git objects only.

**Kill rule:** any of the four failing at the measured revision stops the claim (honest stop).

## Claim discipline (both)

- Predicate sentence is byte-identical in this plan, `claims.json`, each counter constant and each receipt (counter reads the predicate from the claims file at the freeze revision and refuses on mismatch).
- Instruments (counters + selftests + red fixtures) are committed before `claims.json`; the freeze commit is the first that adds `claims.json`; `corpus/claim-freezes.tsv` gets the row at freeze validation.
- No score is computed on anything authored after the freeze for the claim's own data set; the claim is judged on the frozen counter, kill rule and predicate.
- Red receipts at the base are committed before any data; the do-nothing control must fail (exit 1) at base.
