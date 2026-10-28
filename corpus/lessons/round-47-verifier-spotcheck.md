# Round 47 verifier spot-check — hyaku closure

author: hyaku closure (non-author integrator, @m_zfl)
lane: kaidoku · round 47 · attempt 1
base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5` → tip `242e8b973b28c10953e59688626e9092db89031a`
report: `.ufo/reports/round-47/kaidoku.md` (fleet commit `c1669ca4`, author `kaidoku-shokunin <kaidoku@shokunin.local>`)
checked: 2026-10-28.

## Conformance (step 1)

| item | result |
|---|---|
| report committed by lane identity | `git log -- .ufo/reports/round-47/kaidoku.md` → `c1669ca4` and `3b68855c`, both `kaidoku-shokunin <kaidoku@shokunin.local>` |
| `## SHONEN` heading | `grep -c '^## SHONEN'` → 1; four `[~]` lines, one per `SHONEN.md` box |
| cited lane commits exist + ancestor of `main` | all 17 cited hashes resolve (`git rev-parse`) and `merge-base --is-ancestor <h> main` holds, including base `13a9e9e1` and tip `242e8b97` (= branch tip) |
| lane pushed | `jj-lane.sh state` → `local=remote=242e8b97…, ahead=0, behind=0` |
| no uncommitted round work | **defect:** `git status --porcelain` → 128 entries; 46 under `.ufo/waves/round-47/` (23 modified tracked, 23 untracked) plus round-45/46 inherited leftovers. Seats kept writing after `242e8b97`; routed to round 48 |
| prompt carries template contract | `.ufo/prompts/kaidoku-round-47.md` embeds the five child-lane items (report path, commit-before-report, SHONEN heading, hash citation, write scope) |
| marker | report names real committed work — not a marker |

## Claims re-checked

### R47-C1 (depth) — evidence-verified + independently re-measured: **improved**

The claim rests on the lane-owned gate `tools/round-47/exact.py`; per §Gate standard
(Closure consequence) the committed evidence is verified, never re-executed.

- Committed before-receipt `.ufo/waves/round-47/controls/ctl-c1-0-do-nothing.json` (rev `5017e1f7`,
  do-nothing control): `block_present 0`, `rule_blocks 23`, `marker_occurrences 0`, `met_target
  false` — the control cannot reach the target.
- Committed after-receipt `l1/scores/c1-at-A7.json` (rev `a0753786`): `rule_blocks 24`, `rows 4`,
  `refs 9`, `unresolved_citations []`, battery `forgeries_total 4 / v2_green 4 / v3_green 0 /
  genuine_green 1 / crash 0`, `met_target true`, `failing []`.
- My own re-derivation over committed bytes at tip `242e8b97`:
  - `git show $TIP:SKILL.md | grep -c 'exactness-table v3'` → **1** (marker present once).
  - Craft rule blocks (`awk` over `## Queue-drain craft `, `- **` bullets): base **23** → tip **24**.
  - Block 24 table rows carry routed ids `R46-CL2, R46-CL3, R46-CL4, R46-CL6` exactly once each;
    arm cells are exactly the vocabulary `symbol, once, digest, order` (matches receipt).
  - Interpreter pin re-derived: `git show $TIP:tools/round-47/exact.py | sha256sum` →
    `01a4bca7…5bcd5` — equals the pin inside block 24 and `interpreter_sha256_expected` in the
    receipt.
  - The block cites `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`
    (file exists; the M47-6 proxy-harm repair is real).
- Freeze-series honesty: 6 disclosed amendments A1–A6 each with a committed red-before receipt;
  `ctl-c1-1-v2-profile.json` shows the ported round-46 (v2) profile would accept the artefact
  (`met_target true` under v2) while v3 scores the forgeries red — the tightening is documented,
  not hidden. R47-CL10 (a gold forgery can still satisfy both predicates) is the lane's own routed
  defect and bounds this verdict: the counter grades the stated form, and the artefact as landed
  satisfies it.

### R47-C2 (calibration) — evidence-verified + corrected atoms independently re-derived: **improved**

- Committed before-receipt `ctl-c2-0-do-nothing.json` (rev `13a9e9e1`): `mismatches 4`,
  `corrections 0`, `met_target false`.
- Committed after-receipt `c2-at-A7.json` (rev `a0753786`): `atoms 42`, `mismatches []`,
  `corrections 2`, `exempted 1`, battery `correction_forgeries 3 / forgeries_green 0`.
- My own re-derivation:
  - seats atom: `.ufo/waves/round-45/w2-dispatch.json` `counts.spawn` → **36**; the card's "wave 2:
    32 seats" was indeed wrong and `## Record corrections — round 47` says so.
  - window atom: `git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46
    plans/round-46-claims.md` → **0 lines** — the corrected window is genuinely empty.
  - coverage head: `git ls-tree -r --name-only $TIP corpus/knowledge | grep -c '\.md$'` → **138**
    (matches `138/138`; base also 138).
  - depth head: 24 rule blocks (above) matches `24/24`.
  - corrections section present at `SCORECARD.md:3663`, append-only, both correction lines parse
    the grammar the counter documents.
- Separability defect honestly recorded (M47-8): C2's `axes` class reads `SKILL.md`, so C2 is not
  independent of C1's artefact; reported as falsified in one direction rather than smoothed.

### No axis harmed

`git diff 13a9e9e1 242e8b97 -- SCORECARD.md` shows only the corrections append, the round section
and head updates (coverage 9.72→10.0, depth 10→10, calibration 0→10). `git diff … -- PROVINCE.md
corpus/knowledge` → 0 lines. Coverage/calibration not harmed; no third axis touched.

## Spot-check (LEARNING.md — non-author, ≥1 admit + ≥1 reject)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S143 `https://docs.python.org/3/library/re.html` | admit (tier A, mined) | `curl -sL` re-fetch 2026-10-28: 257,706 bytes, sha256 `f169ed06…d11f6a` — **identical bytes** to the row's pin | **agree** | `re.fullmatch` anchor present; the located quote "If the whole string matches … does not match the pattern" is verbatim in the rendered text and grounds the equality-vs-containment arm clause (nit: quote is 23 words, lesson counts 24 — inside the ≤25 bound either way) |
| S144 `https://docs.python.org/3/howto/regex.html` | reject | `curl -sL` re-fetch: 165,172 bytes, sha256 `5e205f7d…f9be` — identical bytes; `grep -c fullmatch` → **0** | **agree** | the HOWTO never defines `fullmatch`; rejection as redundant/unfit stands, flip condition is falsifiable |
| SOURCES rows S143/S144 | new rows | `corpus/SOURCES.md:149-150` | **agree** | rows parse (census-clean), tier/kind/status enums valid, `used-by` points at the lesson for the mined row and `—` for the rejected row |
| census | — | `scripts/sources-census.sh validate --root … kaidoku` | exit **0** (`kaidoku ok`), 14 W04 duplicate-URL warnings, none on the new rows | consistent with report's "warnings only" |
| row count | — | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | **144** at tip vs 142 claim — matches "142 → 144" | — |

## Trend verdicts

- **expansion — `unchanged`.** Agree: knowledge files 138→138, PROVINCE byte-identical, no
  coverage-map row moved; the two opened sources are instrument documentation.
- **quality — `improved`.** Agree with bound: block 24 turns four routed instrument defects into
  checkable clauses and the battery receipt shows the counter scoring its own forgeries red while
  the ported v2 profile greens them; QUALITY.md row 78 added. Bound: R47-CL10 shows the predicate
  still grades form, not work — stated, not closed.
- **discernment — `improved`.** Agree: admit and reject decisions both verified against re-fetched
  byte-identical sources; the freeze series (A1–A6) and M47-6/8/9 are self-found defects recorded
  with red-before receipts; wave findings are routed, not smoothed.

## Routed defects for round 48 (lane must fix or answer)

1. **Worktree debt (conformance):** 128 uncommitted paths, 46 of them round-47 late seat writes —
   resolve per §Inherited state (commit under round 48 or revert), and reconcile the settlement
   record: the report says `SentFixtures` "wrote nothing" yet its committed receipts
   (`receipts/`, `MANIFEST.sha256` utc 18:15:13Z, inside `242e8b97`) show it did write output —
   the honest settlement is 75/75 with late writes, or the measurement was stale.
2. **Landed-changes table imprecision:** commits `09a9f912`, `f7d6e58d`, `6f9fd7f8` exist between
   cited hashes but are absent from the table (they are described in the measurements section;
   status-neutral, tidy next time).
3. Lane's own routed queue stands: R47-CL1…CL15 plus inherited R46-CL1/CL5/CL7/CL8 — the HIGH items
   (CL10 gold-forgery satisfiability, R46-CL7 digit-binding) deserve priority.

## Verdict

Both declared claims verify against committed gate evidence and independent re-measurement; no
axis harmed; gate spot-check agrees on admit and reject. **Admitted.** Verdicts: depth `improved`,
calibration `improved`; trends expansion `unchanged`, quality `improved`, discernment `improved`.
