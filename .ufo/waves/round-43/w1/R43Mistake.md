# R43Mistake — round-43 lesson `## Mistakes` candidates (pre-freeze mine)

Verdict: **CONFIRMED** — 4 candidate M43 rows mined from the assigned sources; every evidence pointer re-verified against the base tree `6b9e64fe7e0de202d9383baad5792fbfe039a743` / closure commits.

## Axes (godspeed)

- **coverage** — all assigned sources mined: round-42 verifier spot-check §§1–5, round-43 prompt §6 (run-10/run-9/run-8 addenda), round-42 lesson M42-1..M42-3 (read for exclusion); supporting passes over the round-41 and round-40 spot-checks (the other two rejected closures in the fresh-start streak).
- **depth** — each candidate carries a re-verified evidence pointer (command + observed output recorded below and in `artifacts/R43Mistake/evidence-verification.txt`), an exact captured-by citation (`git show 6b9e64fe:corpus/QUALITY.md` row numbers or prompt §6 line), and a red-check sketch aimed at the historical defect instance itself.
- **calibration** — candidates are tagged against what round 43 actually fixes per `plans/round-43-claims.md`; two spares and the exclusions are recorded under "Considered and set aside" so the L1's selection is a downgrade, not a guess.

## Sources and exclusions (assigned)

1. `corpus/lessons/round-42-verifier-spotcheck.md` §§1–5 — conformance D1/D2, routed R42-V1..V5. Read in full.
2. `/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-43.md` §6 — run-10 directive, run-9 lessons (file-only-after-WAVE-DONE 9 incidents; counters-bind-final-text mori r55; 64–128 floor), run-8 fresh-start rule. Read.
3. `corpus/lessons/round-42.md` M42-1..M42-3 — read; **not re-mined** per assignment. M42-1 (probe frozen on single-writer fixtures), M42-2 (generator's declared tuple unobserved), M42-3 (tool seams found only by end-to-end dry run).
4. Exclusion cascade: R42-V4 == M42-2 (the spot-check itself routes it "as R42-CL1 / QUALITY 85") → excluded. R42-CL1/R42-CL3 are the round-43 claims themselves (fixed in-claim), not lesson mistakes. R41-CL1/CL2/CL4/D1..D5 from the round-41 spot-check §5 were dispositioned in the round-42 lesson table and are not fresh disagreements.

## Evidence verification (this seat, base tree)

| candidate evidence | command run | observed |
|---|---|---|
| round-42 wave size 43 | `jq '.results\|length' .ufo/waves/round-42/r42-w1-results.json` | `43` — matches spot-check §1 D1 |
| uncommitted gate citation | `grep -n -i 'gate green' /home/vgpnk/Projects/shokunin/.ufo/reports/round-42/kaidoku.md` | line 65: "Pre-file gate: `tools/round-42/prefile-gate.py --round 42` GATE GREEN at `af50af81`." |
| no committed r42 gate output | `grep -rn 'GATE GREEN' .ufo/waves/round-42/ LOG.md SHONEN.md` | only `w1/artifacts/R42PrefileGate/prefile-gate.py` (selftest strings) and `w1/artifacts/R42PrefileGate/round-41-real.txt:15` / `w1/R42PrefileGate.md:97` — both are the **round-41** live run, none at `af50af81`. Matches §1 D2 verbatim claim ("no committed output") |
| round-41 file-before-WAVE-DONE | `grep -n 'green.err\|red.err' corpus/lessons/round-41-verifier-spotcheck.md` | §1 conformance row + §5 D1: report filed before wave 2 WAVE-DONE; 2 tracked edits + 16 untracked paths incl. stray `green.err`/`red.err` in lane root and `corpus/evidence/round-41/c1/V4/` |
| QUALITY row 47 | `git show 6b9e64fe:corpus/QUALITY.md` | "A round is filed only after its last seat has settled, and `tools/round-29/prefile-check.sh <LANE>` exits 0 immediately before the report commit … the lane tree is clean … Fails when the check exits non-zero at filing, is skipped, or its output is absent from the report." |
| QUALITY row 52 | same | "A report cites a gate result only when a committed receipt shows that result; otherwise it cites only committed runs." |
| prompt §6 rules | read | run-9 'File only after WAVE-DONE' (9 incidents); run-9 'Counters that bind seat votes' (mori r55); run-9 'Round size: 64–128 seats … 64 is the floor'; run-8 fresh-start rule; run-10 keeps the 64–128 band |

Full transcript: `artifacts/R43Mistake/evidence-verification.txt`.

## Candidate M43 rows

### M43-cand-1 — report cites a gate result with no committed receipt

- **class:** conformance / citation hygiene: a claimed gate green rested on no committed run; the citation was unverifiable by the closure (and the closure's sweep proved the negative).
- **evidence pointer:** `corpus/lessons/round-42-verifier-spotcheck.md` §1 D2; fleet report `.ufo/reports/round-42/kaidoku.md:65` (claim) vs lane grep showing `GATE GREEN` only in the seat tool's selftest strings and the round-41 live run (`w1/artifacts/R42PrefileGate/round-41-real.txt:15`).
- **captured-by:** QUALITY 52 ("A report cites a gate result only when a committed receipt shows that result") — the row existed since round 30/31 and was not operationalized for the pre-file gate citation.
- **fix (red-check sketch):** extend the cited-runs gate family to pre-file citations: scan the round report for gate-result sentences (`GATE GREEN|GATE RED|exit \d` within two lines of a gate command), and require a committed receipt under `.ufo/waves/round-N/**` at the cited revision naming the same gate command and revision. **Red:** run it on the round-42 report at `af50af81` — the line-65 citation has no receipt → exit 1 `UNBACKED` (same vocabulary as `tools/round-31/cited-runs-gate.py`). **Green:** a report whose every gate citation resolves to a committed receipt at the named revision → exit 0. Round-43 calibration: the claims doc already commits all control receipts at the freeze (`plans/round-43-claims.md` "Controls scored at the freeze"), so the gate is satisfiable this round.

### M43-cand-2 — round shape below the run floor; no falsify wave dispatched

- **class:** round-shape / dispatch conformance: one v1 wave of 43 seats against a binding 64-seat floor, and no wave 2 to attack the round-41/round-42 landings (self-reported as R42-CL2; closure re-filed it as R42-V1).
- **evidence pointer:** `corpus/lessons/round-42-verifier-spotcheck.md` §1 D1 + §5 R42-V1; `jq '.results\|length' .ufo/waves/round-42/r42-w1-results.json` → 43 (re-verified).
- **captured-by:** prompt §6 run-9 line "Round size: 64–128 seats in total, every round … 64 is the floor" (kept binding by the run-10 paragraph); no QUALITY row covers round size.
- **fix (red-check sketch):** a filing-time shape check over the dispatch ledger: for each `<wave>-results.json`, assert seat count ≥ 64 (or an operator-granted residual recorded in the report) and, when the claims doc routes a falsify duty (R42-CL2 pattern), assert a wave-2 results file exists. **Red:** round-42's ledger — 43 results, no wave-2 file → exit 1 `below_floor`. **Green:** round 43 files with wave-1 + wave-2 results summing ≥ 64 → exit 0. Round-43 calibration: `plans/round-43-claims.md` states wave 2 "includes re-running the round-42 C1 counter against a fresh carrier cache" and discharges R42-CL2 — the check is designed to pass only if that wave actually settles before filing.

### M43-cand-3 — L1 files before WAVE-DONE; late seat work left uncommitted at closure

- **class:** filing discipline: the report committed before the last wave settled; 2 tracked edits + 16 untracked paths (incl. stray `green.err`/`red.err` in the lane root) were live at closure. Same class as the run-9 lesson (9 incidents) — the L1 got woken by late seat results after its closure.
- **evidence pointer:** prompt §6 run-9 'File only after WAVE-DONE' (9 incidents); `corpus/lessons/round-41-verifier-spotcheck.md` §1 conformance row + §5 D1.
- **captured-by:** prompt §6 run-9 WAVE-DONE lesson, operationalized as QUALITY 47 ("filed only after its last seat has settled … lane tree is clean … Fails when the check … is skipped, or its output is absent from the report").
- **fix (red-check sketch):** make the prefile gate's WAVE-DONE clause read the dispatch ledger instead of trusting the L1: for every `.ready` file written, require the matching `<wave>-results.json` to exist and cover every dispatched seat id; then assert `git status --porcelain` is empty and scan the lane root and evidence dirs for stray build artifacts (`*.err`, `*.tmp`). **Red:** the round-41 filing state — `w2.ready.dispatched` present with late wave-2 reports untracked and stray `.err` files → exit 1. **Green:** all waves settled, tree clean → exit 0. Round-43 calibration: the run-10 prompt keeps the lesson binding; the check is satisfiable at filing only after the round-43 wave-2 handoff lands.

### M43-cand-4 — counters that bind seat final text break on output wrapping

- **class:** instrument brittleness: a counter that parses a seat's final text to bind its verdict fails silently when the seat wraps output (JSON-wrapped vote lines vs plain lines); the run-9 incident is mori r55.
- **evidence pointer:** prompt §6 run-9 'Counters that bind seat votes' paragraph (mori r55: JSON-wrapped vote lines failed a counter that bound plain lines).
- **captured-by:** prompt §6 run-9 counters-bind-final-text lesson; adjacent QUALITY 22 (seat-status statements must be reproducible from a retained per-seat record) — cited as related, not the catching row.
- **fix (red-check sketch):** before any wave whose counter reads seat text, freeze a parser with committed fixtures of both wrappings (plain line; JSON-wrapped line carrying the same verdict), or bind the counter to a file the seat writes (e.g. a verdict line in `<Seat>.md` plus a machine-readable `<seat>-result.json` sidecar the wave validator reads). **Red:** feed the mori r55 wrapped lines to a plain-line-bound counter → it must miss the verdict and exit non-zero (a miss that still exits 0 is itself the finding, per the round-34 lesson that a self-reported flag a no-op gate trusts certifies nothing — QUALITY 72). **Green:** the frozen parser scores both fixture classes identically. Round-43 calibration: round-43's own counters (`c1-counter.py`, `local-source-gate.py`) bind committed manifests and git state, not seat text, so this row is forward-looking for the wave validator and any vote-counting seat — included because the assignment names the run-9 lesson as a mine source and the class is unaddressed by any committed lane gate.

## Considered and set aside (spares, not proposed)

- **R42-V3 — SKILL rule blocks 20/21 carry no in-SKILL claim status** (`round-42-verifier-spotcheck.md` §5): real and fixable (one-line stopped/unscored marker per table until a claim verifies it), but captured-by = none — no QUALITY row or prompt rule covers in-SKILL claim status, so as a Mistakes row it names no existing bar that failed. Hold as spare if the L1 wants a registry-hygiene row anyway.
- **R42-V5 — knowledge entry opens `status:` before the provenance trio** (same §5; `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md` line 3 vs 5): CORPUS §Additional-corpus-rules territory, not a QUALITY row (captured-by = none). Hold as spare.
- **Run-8/run-10 fresh-start rule** (declare only claims a do-nothing control cannot reach, after reading the last three rejected closures): round 43 complies — the claims doc cites the streak, scores CTL-C1-0/CTL-C2-0 do-nothing receipts at the freeze, and §9 control-first shape. No violation evidence to mine.
- **R42-V4 / R42-CL1 / R42-CL3**: excluded per assignment (M42-2 not re-mined; the other two are the round-43 claims themselves).

## Tooling

No installs or upgrades: the mine is read-only over committed bytes (`git show`, `grep`, `jq`). Nothing was run against REA/unblob/sasquatch; no reserved-input objects were touched. Scratch discipline: no scratch dir needed; the artifacts dir holds only this evidence log.

Report: `.ufo/waves/round-43/w1/R43Mistake.md`
Artifacts: `.ufo/waves/round-43/w1/artifacts/R43Mistake/evidence-verification.txt`
