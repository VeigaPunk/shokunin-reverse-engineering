# Scout — SKILL.md measurement registry for rounds 27–28, and the round-29 rows

Item: `ScoutSkillRegistry` (Kaidoku round 29, wave 1). Read-only seat; no REA, no network, no
subagents. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` at measured tip
`18be864a528873b2b70d8c94e31f880290249e90` (base `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`).
All UTC times below are 2026-10-22.

## 1. Answer: the row format as observed

Two registry tables were read at the tip.

**Earlier table, round 24.** Lead-in prose `SKILL.md:763-768` ends with the freeze instruction and
the `--disclosures` invocation (`:767`), then:

| element | line |
|---|---|
| `### Round-24 measurement registry` | 770 |
| blank | 771 |
| header `\| Name \| Kind / owner \| Entry / verdict map \| Self-invocation \| Pinned values / write scope \|` | 772 |
| separator `\|---\|---\|---\|---\|---\|` | 773 |
| rows `round24-C1`, `round24-C2`, `round24-producer`, `round24-repro` | 774–777 |

(Earlier still: `### Round-22 measurement registry` at `:679` with header `:681`, separator `:682`,
rows `:683-686`; `### Round-23 measurement registry` at `:731`, header `:733`, separator `:734`,
rows `:735-738`. The round-25 rows follow the same shape, e.g. `round25-custody-ruler` at `:807`.)

**Later table, round 27/28.** `SKILL.md:948` `### Round-27/28 measurement registry`, blank `:949`,
header `:950`, separator `:951`, rows `round27-C1` `:952`, `round27-C2` `:953`, `round28-C1`
`:954`, `round28-C2` `:955` (end of file; the tip blob ends `…private temp dirs \|\n`, i.e. one
trailing newline and no blank line).

**Format rules, identical in both tables** (observation):

1. Five columns, exactly: `Name` | `Kind / owner` | `Entry / verdict map` | `Self-invocation` |
   `Pinned values / write scope`. One physical line per instrument — no wrapped rows; every cell
   is separated by ` | ` and the line ends with `|`.
2. `Name`: the round's measurement gates take `round<NN>-C<k>` (`round24-C1`, `round24-C2`,
   `round27-C2`, `round28-C2`); gates and probes that are not the round's numbered gates take a
   kebab name (`round25-custody-ruler`, `round23-final-producer`, `round22-capture-probes`).
3. `Kind / owner`: `gate / kaidoku` for anything with an exit map; `probe / kaidoku` for producers;
   `—`/`No selftest: …` in the self-invocation cell for producers.
4. `Entry / verdict map`: backticked argv with `<LANE>`/`<REV>`/`[--base <BASE>]` placeholders, then
   `; 0 <success predicate>, 1 <failure>, 2 <input/unevaluable>`, then `;`-separated notes on what it
   reads, what it refuses and what it never does (e.g. `:952` `Reads Git objects at --rev only;
   per row, base/repeat/renamed envelopes re-derive the verdict…`).
5. `Self-invocation`: backticked `--selftest` argv (no `--root`/`--rev`), the case list shape and
   count, `0 all pass, 1 any failure`, then a tip status line —
   `Green at tip (selftest cases=N failures=0, exit 0, <UTC>); freeze receipt <.ufo/…/before/…>`.
   Where the instrument has no selftest the cell says `none in the instrument` (`round24-C2` `:775`).
6. `Pinned values / write scope`: `Counter sha256 <hash> (…/claims.json instruments).` then the
   `loaded_by_counter` inputs with their sha256, the package pin, the refusal rule, and the write
   scope — e.g. `Refuses runs/lookups from before the counter commit. Git reads only; selftest
   writes private temp dirs` (`:954`).
7. Path style differs by era: round-24 rows address instruments as `.ufo/waves/round-24/tools/…`;
   round-27/28 rows use `tools/round-27/…`, `tools/round-28/…`. Round 29's instruments live in
   `tools/round-29/`, so the round-27/28 style is the matching precedent.
8. Section heading names the round(s) the rows belong to; when two rounds share a table the heading
   is `Round-27/28`. Nothing follows the round-27/28 table, so round 29's table is an append.

## 2. Proposed round-29 rows

Append after `:955` as: one blank line, then the heading, one blank line, the header row, the
separator, then the four rows below. They are byte-shaped like `:952-955` (one line each; the
wrapping below is presentation only).

### Round-29 measurement registry

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round29-C1 | gate / kaidoku | `python3 -I -B tools/round-29/c1-fresh-naming.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1, 1 otherwise (FAIL reasons listed), 2 a pinned input absent or differing. Reads Git objects at --rev only, never network or REA; also `--emit-tally` (recompute the tally from the working tree; L1 use, not a verdict). Byte-identical lookup bodies across selectors are legitimate (responses are keyed by manifest entry, not by bytes); entry_ok accepts only the claim's own SOURCES row S088 | `python3 -I -B tools/round-29/c1-fresh-naming.py --selftest`: 20 listed cases + planted-wrong-name check + pin refusal, 22 cases in private temp repos; 0 all pass, 1 any failure. Receipts record green at tip (cases=22 failures=0, exit 0, 2026-10-22T20:16:37Z); freeze receipt `.ufo/waves/round-29/before/c1-selftest.txt`, re-run `.ufo/waves/round-29/after/c1-selftest.txt` | Counter sha256 6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda (`.ufo/waves/round-29/claims.json` instruments; equals the blob at `18be864a`). Pinned inputs (`loaded_by_counter`): resolver `tools/round-25/a2/resolve-selectors.py` 4be915668ea20a643d04c9b8ae3c83bc9f5fd1b4d8821e06cabdccce36b3c23d, `corpus/evidence/round-29/c1/carriers.tsv` 94438ede707d98987af7d8a869aa5fdb5ac18872fb9cf57fe621e9593bdc6e9c, `heldout.tsv` 2db9e658d5076771ee249f9d027938103edb7933201abb4b391f1053323dca23; package pin 6.5.0 + package.json a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c. Refuses runs or lookups first committed before the counter commit. Git reads only; selftest writes private temp dirs |
| round29-C2 | gate / kaidoku | `python3 -I -B tools/round-29/c2-filtered-unseen.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 responses_complete=178/178 entries>=1 mismatches=0 predicted_true>=1 predicted_false>=1 entry_ok=1, 1 otherwise (FAIL reasons listed), 2 a pinned input absent or different. Reads Git objects at --rev only, never network or REA; a non-boolean `filtered` counts as a mismatch and both branches must hold on unseen data; entry_ok accepts only the claim's own SOURCES row S087 | `python3 -I -B tools/round-29/c2-filtered-unseen.py --selftest`: 18 listed cases + pin refusal, 19 cases in private temp repos; 0 all pass, 1 any failure. Receipts record green at tip (cases=19 failures=0, exit 0, 2026-10-22T20:16:38Z); freeze receipt `.ufo/waves/round-29/before/c2-selftest.txt`, re-run `.ufo/waves/round-29/after/c2-selftest.txt` | Counter sha256 00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801 (`.ufo/waves/round-29/claims.json` instruments; equals the blob at `18be864a`). Pinned inputs: `corpus/evidence/round-29/c2/selectors.tsv` 3a93f7837accb9acd66874707922317d9a8e0f8afb0c9cd87ee79f3d9fa15b5d, `canonical-signatures.json` 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2. Refuses responses fetched or files first committed before the counter commit. Git reads only; selftest writes private temp dirs |
| round29-freeze-gate | gate / kaidoku | `python3 -I -B tools/round-29/freeze-gate.py --root <LANE> --rev <REV> [--require-clean round-N]... [--disclosures <LANE_PATH>]`; 0 every --require-clean freeze exists and is CLEAN and, when --disclosures is given, every audited freeze is disclosed exactly with no stray row, 1 otherwise, 2 unevaluable. Reads Git objects at --rev only; audits every `.ufo/waves/round-*/claims*.json` (19 at `18be864a`) under key `round-N` for `claims.json` and `round-N/<file>` otherwise; finding codes INSTRUMENT_NONE/UNRESOLVED/ABSENT/UNPINNED/PIN_MISMATCH/REVISED; a sha256 recorded under `loaded_by_counter` or `producers_not_counters` pins a path like `instruments` does. Exercised at tip without --require-clean: audited 19 clean 2 disclosures exact 19/19, exit 0 (2026-10-22T20:22:53Z); with `--require-clean round-29` exit 1 on the disclosed INSTRUMENT_UNPINNED `tools/round-28/c1-heldout-naming.py` (M29-3), so the row must not claim a round-29 require-clean green | none in the instrument (no --selftest) | Instrument sha256 25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2 (blob at `18be864a`; named in no `claims*.json` — this row is its only pin). Disclosures ledger `corpus/claim-freezes-v2.tsv` (header + 19 rows) read at MEASURED; the round-24 gate and `corpus/claim-freezes.tsv` stay the round-24 pair. Git reads only; refuses a `--root` that is not the repository top; no writes |
| round29-prefile | gate / kaidoku | `sh tools/round-29/prefile-check.sh <LANE>`; 0 the tree is clean (`git status --porcelain` empty: no modified, staged or untracked path) and both disclosure steps exit 0, 1 when any step fails (each failure is printed, last line `prefile: PASS` or `prefile: FAIL`), 2 on usage or when git cannot read the tree. Steps: tree cleanliness; `.ufo/waves/round-24/tools/freeze-gate.py --disclosures corpus/claim-freezes.tsv` at HEAD; and, when HEAD holds `corpus/claim-freezes-v2.tsv`, the `freeze-gate.py` beside this script with `--disclosures` on it. Read-only: unsets GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE and runs `GIT_OPTIONAL_LOCKS=0 git status`, no git write. It cannot see a dispatched seat still running, so run it after the last seat settles and the last lane commit lands, immediately before the report commit (QUALITY rows 46–47) | none in the instrument (no --selftest); exercised mid-wave on the live lane: `prefile: tree NOT CLEAN (19 paths)` and both gates `exit=0` → `prefile: FAIL`, exit 1 (2026-10-22T20:27:07Z); negative control on the real r28 state: scratch clone at `242b0d8b` with the later seat bytes → exit 1, restored → exit 0 (`.ufo/waves/round-29/after/prefile-check-red-r28-v2.txt`) | Instrument sha256 5c3586b277e16b7c43ae32a4160643442f6b9612b7e2d74cd6e76c12c688cdd9 (working tree at 2026-10-22T20:27:07Z, uncommitted; the measured tip `18be864a` holds the earlier status-only version 34edba0460cf9c5d3eb51e15367b3f54718da81bdd6b993d8cacc03379dd5672). Pin the blob committed at filing; named in no `claims*.json`, so this row is its only pin. Reads `git status` and the two gate scripts; no writes |

Optional (considered, not part of the four): the producers `tools/round-29/make-carriers.py`,
`select-heldout.py`, `preseen.py`, `collect-c1.py`, `collect-c2.py` are pinned under
`producers_not_counters` in the same `claims.json` and are one-shot this round; registry precedent
(`round24-producer`, `round23-final-producer`) registers a producer only when it is reused. A row
for them is defensible but not required. `[INFERENCE]`

## 3. Evidence

Every command below was run from
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` except where noted. Exit codes and UTC are the
runs of this seat unless a line says "receipt" (a lane file read, not re-run here).

| # | command | output excerpt | exit | UTC |
|---|---|---|---|---|
| E1 | `git rev-parse HEAD` | `18be864a528873b2b70d8c94e31f880290249e90` | 0 | session start, not logged exactly; the same revision is re-read by E15 at 20:20Z |
| E2 | `grep -n 'measurement registry\|^\|---\|---\|---\|---\|---\|$' SKILL.md` | `679:### Round-22 measurement registry` … `731:` … `770:### Round-24 measurement registry` … `948:### Round-27/28 measurement registry`; separators `682/734/773/951` | 0 | 20:19Z |
| E3 | `grep -n '^\| round' SKILL.md` | `952:\| round27-C1` … `955:\| round28-C2`; `774-777` round-24 rows; `683-686` round-22 rows | 0 | 20:19Z |
| E4 | `read SKILL.md:948-955:raw` | header `\| Name \| Kind / owner \| Entry / verdict map \| Self-invocation \| Pinned values / write scope \|`; four rows, one line each; last bytes `…private temp dirs \|\n` | — | 20:19Z |
| E5 | `git show 18be864a…:SKILL.md \| tail -c 120 \| od -c \| tail -4` | `0000160   …   d i r s   \|  \n` | 0 | 20:20Z |
| E6 | `grep -n 'add_argument' tools/round-29/freeze-gate.py` | `201:--root`, `202:--rev`, `203:--require-clean`, `204:--disclosures`; no `--selftest` anywhere | 0 | 20:19Z |
| E7 | `read tools/round-29/freeze-gate.py:3-47:raw` and `:145-215:raw` | `Exit: 0 when every --require-clean freeze exists and is CLEAN and, when --disclosures is given, every audited freeze is disclosed exactly with no stray rows; 1 otherwise; 2 when the input cannot be evaluated.`; `failed = [r for r in require_clean …]; code = 1 if failed else 0` | — | 20:19Z |
| E8 | `python3 -I -B tools/round-29/freeze-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 18be864a… --disclosures corpus/claim-freezes-v2.tsv` (full JSON in scratch) | `{"audited": 19, "clean": 2, … "disclosures": {"exact": 19, "mismatched": [], "missing": [], "of": 19, "path": "corpus/claim-freezes-v2.tsv", "present": true, "stray": []}}` | **0** | 2026-10-22T20:22:53Z |
| E9 | same argv plus `--require-clean round-29` | `audited 19 clean 2 required_failed ['round-29']`; round-29 findings `['INSTRUMENT_UNPINNED']` → `tools/round-28/c1-heldout-naming.py` | **1** | 2026-10-22T20:22:53Z |
| E10 | `grep -n '^round-29' corpus/claim-freezes-v2.tsv` | `round-29<TAB>FLAGGED<TAB>INSTRUMENT_UNPINNED<TAB>… only tools/round-28/c1-heldout-naming.py stays unpinned (…; M29-3)`; 19 rows + header | 0 | 20:21Z |
| E11 | `read tools/round-29/prefile-check.sh:raw` (intermediate status-only version, 20:20Z) | `[ $# -eq 1 ] \|\| { … exit 2; }`; `out=$(git -C "$1" status --porcelain) \|\| exit 2`; `prefile: NOT CLEAN (…)`, `exit 1`; `prefile: clean`, `exit 0` (the composite version's wording is in E12/E13) | — | 20:20Z |
| E12 | `GIT_OPTIONAL_LOCKS=0 sh tools/round-29/prefile-check.sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin` (composite working-tree version) | ` M LOG.md`, ` M SCORECARD.md`, ` M corpus/knowledge/2026-10-22-r29-…`, ` M tools/round-29/prefile-check.sh`, `?? .ufo/waves/round-29/…`; then `prefile: tree NOT CLEAN (19 paths)`, `prefile: round-24 gate --disclosures corpus/claim-freezes.tsv at 18be864a… exit=0`, `prefile: round-29 gate --disclosures corpus/claim-freezes-v2.tsv at 18be864a… exit=0`, `prefile: FAIL` | **1** | 2026-10-22T20:27:07Z |
| E13 | `grep -n 'GIT_OPTIONAL_LOCKS' LOG.md tools/round-29/prefile-check.sh` | `LOG.md:2983` (quoted below); script `:4` comment and `:20:out=$(GIT_OPTIONAL_LOCKS=0 git -C "$root" status --porcelain) \|\| exit 2`; `:45 … echo "prefile: PASS" \|\| echo "prefile: FAIL"` | 0 | 20:27Z |
| E14 | `git diff --stat -- tools/round-29/prefile-check.sh; sha256sum tools/round-29/prefile-check.sh` | `1 file changed, 40 insertions(+), 9 deletions(-)`; working blob `5c3586b2…` vs tip `34edba04…`; an intermediate working version at 20:23:13Z hashed `20507911…` and differed from tip only by `GIT_OPTIONAL_LOCKS=0` (`3 insertions(+), 2 deletions(-)`) | 0 | 20:27Z |
| E15 | `for f in …; do git show 18be864a…:$f \| sha256sum; done` | c1 `6ad79d10…93fdda`, c2 `00ca0a3d…c5a801`, gate `25b54339…93eb2`, prefile `34edba04…dd5672` (the last differs from the working tree's `5c3586b2…` per E14) | 0 | 20:20Z |
| E16 | `read .ufo/waves/round-29/claims.json` | `"instruments": {c1, c2}` only; `"loaded_by_counter"` 5 paths incl. carriers 94438ede…, heldout 2db9e658…, selectors 3a93f783…, canonical 5572beb5…; `"producers_not_counters"` 5 producers; `"target"` 16/16, 152/152 for C1 and 178/178 for C2 | — | 20:20Z |
| E17 | `read .ufo/waves/round-29/after/{c1-selftest,c2-selftest,c1-at-18be864a,c2-at-18be864a,freeze-gates-v2,prefile-check-red-r28-v2}.txt` (receipts) | `selftest cases=22 failures=0` / `cases=19 failures=0`; `runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1` / `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1`; both `exit=0` | receipt | receipt |
| E18 | `grep -n 'add_argument\|selftest cases' tools/round-29/c1-fresh-naming.py tools/round-29/c2-filtered-unseen.py`; `sed -n '520,600p;290,347p'` | c1: `--root/--rev/--base/--emit-tally/--selftest`, 20 listed cases, `print("selftest cases=%d failures=%d" % (len(cases) + 2, fails))`; c2: 18 listed cases, `len(cases) + 1` | 0 | 20:20Z |
| E19 | `grep -n 'round-28' tools/round-29/c1-fresh-naming.py`; `grep -n '^EVDIR'` | docstring `:14 carriers in corpus/evidence/round-28/c1/carriers.tsv`, `:27 corpus/evidence/round-28/c1/tally.json`; code `:56 EVDIR = "corpus/evidence/round-29/c1"` | 0 | 20:21Z |
| E20 | `grep -n '^| 4[5-7]' corpus/QUALITY.md` | row 45 (claim_row citation), row 46 (every `claims*.json`, `--disclosures` before filing, exit in report), row 47 (pre-file check exits 0 immediately before the report commit; output in the report) | 0 | 20:21Z |
| E21 | `grep -n 'M29-1\|M29-2\|M29-3' corpus/lessons/round-29.md` | M29-1 names the new pre-file check; M29-2 the ledger/`--disclosures` run; M29-3 the round-29 INSTRUMENT_UNPINNED flag on `tools/round-28/c1-heldout-naming.py` | 0 | 20:21Z |
| E22 | `git ls-tree -r --name-only 18be864a… -- tools/round-29/`; first-commit loop | nine tools at tip; c1/c2 first added `dbd87cfa`, gate `7431096b`, prefile `18be864a` | 0 | 20:20Z |

Exact bytes of the disclosure cited in E13 and O4 (`LOG.md:2983`, read with
`sed -n '2983p' LOG.md`):

```
- Disclosure: five wave-1 seats ran plain `git status` in the lane, which can rewrite `.git/index` (`.ufo/waves/round-27/w2/ReviewRoundShape.md`); no tracked content, ref or commit changed. Next wave contexts should require `GIT_OPTIONAL_LOCKS=0`.
```

## 4. Observations, inference, unknowns

- **O1 (observation).** Both registry tables use the same five columns, one line per instrument, and
  the same `0 / 1 / 2` exit-map phrasing; the round-27/28 rows add "Counter sha256 … (`claims.json`
  instruments)" and a "Green at tip (selftest cases=…, exit 0, UTC); freeze receipt …" clause. The
  proposed rows follow both clauses because their evidence exists at this tip (E8, E17).
- **O2 (observation).** `corpus/lessons/round-29.md` M29-3 and E9/E10 show round-29's own freeze is
  FLAGGED (`INSTRUMENT_UNPINNED tools/round-28/c1-heldout-naming.py`, a prose reference to the
  round-28 counter, not a file the counter runs). Hence the gate row records the exercised argv
  without `--require-clean` (exit 0) and states the `--require-clean round-29` result (exit 1);
  registering only `--require-clean round-29` would register a red as the entry, and registering
  only the no-flag argv without saying so would overstate the audit.
- **O3 (observation).** Neither hygiene instrument is pinned in any `claims*.json`:
  `"instruments"` in `.ufo/waves/round-29/claims.json` names only the two counters (E16), and the
  v2 gate/prefile are hygiene (QUALITY 46/47, M29-1..3), not claims. Their SKILL rows are therefore
  the only public pin; E15 gives the tip blob hashes. `[INFERENCE]` This is acceptable under
  QUALITY 33 as written (counting scripts that decide a claim), but a reader must not take the
  registry as a claims-freeze pin for them.
- **O4 (observation + inference).** `tools/round-29/prefile-check.sh` moved twice during this wave.
  At the measured tip `18be864a` it is a status-only check (`34edba04…`, 15 lines) whose comment
  says "Read-only: it runs no git write", yet it runs a plain `git status`; LOG.md:2983 discloses
  that plain `git status` in the lane can rewrite `.git/index`, so the tip blob's comment overstates
  what the tip bytes guarantee. At 20:23:13Z the working tree added `GIT_OPTIONAL_LOCKS=0`
  (`20507911…`, 3+/2−). At 20:27:07Z it had become a composite pre-file gate (`5c3586b2…`, 40+/9−)
  that also runs both freeze gates with `--disclosures` and prints `prefile: PASS`/`prefile: FAIL`
  (E12–E14); its own header names M29-1, M29-2 and a new M29-4. Nothing has committed these edits,
  and the round-29 lesson file read at 20:21Z has no M29-4 row yet, so the registry must pin the blob
  committed at filing and the ledger/lesson must catch up to it. `[INFERENCE]` on the index write is
  from LOG.md:2983 and git's documented `GIT_OPTIONAL_LOCKS` behaviour; this seat did not diff
  `.git/index` (it runs no git writes in the lane).
- **O5 (observation).** `tools/round-29/c1-fresh-naming.py`'s docstring cites
  `corpus/evidence/round-28/c1/…` at `:14` and `:27` while its constants use
  `corpus/evidence/round-29/c1` (`:56`). Documentation-only: the counters read `EVDIR`, and the tip
  receipt counts 16 carriers / 152 rows from the round-29 lists. Registry text must use the
  round-29 paths as written above.
- **O6 (observation).** The `claims.json` instrument sha256 for both counters equal the tip blobs
  (E15 vs E16), so the pins are honest at the measured revision.
- **O7 (observation).** File order and headings: the round-27/28 table is the last section; the tip
  blob ends with the last row's newline (E5), so appending a new section needs one blank line, not
  two. Round-22/23/24 precedent has the table header one blank line under its heading.
- **U1 (unknown).** Which `prefile-check.sh` blob the L1 commits before filing, and therefore which
  sha256 the row ends up pinning: `34edba04…` if the tip's status-only version ships unchanged,
  `5c3586b2…` if the composite working-tree gate is committed as drafted (the `20507911…`
  intermediate is already superseded).
- **U2 (unknown).** Whether the L1 wants the five `producers_not_counters` scripts registered as
  rows; this report proposes four rows as asked and marks the producer row optional with reasoning.
- **U3 (not evaluated here).** The counters' tip numbers rest on lane receipts (E17); this seat did
  not re-run the counters, REA or any lookup (item bounds), so the values are receipt-sourced, not
  re-measured.

## 5. Artifacts

Scratch root: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScoutSkillRegistry/`

| file | sha256 |
|---|---|
| `gate-norequire.txt` (E8 transcript, exit 0, 2026-10-22T20:22:53Z) | 296bf6a32598aa189ea70a53a7d2ba8ba826fcf3d063263d6648deef14b3cf12 |
| `gate-norequire.json` (E8 full JSON, 10180 B) | 217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c |
| `gate-require29.txt` (E9 transcript, exit 1, 2026-10-22T20:22:53Z) | 6e039862bcd3054ff7b59a629f6ee549d7324e9779d8c64605995eab9843a838 |
| `gate-require29.json` (E9 full JSON, 10200 B) | 8e3544e255994f10c644e9564a2a58fec2a4d732c9ee0245ede29d521a2befc8 |
| `prefile-now-full.txt` (E12 transcript of the composite script, exit 1, 2026-10-22T20:27:07Z) | 4ecb2eb6c545f0ce8bc1cfa67ac1fe2c0a4f9fb735785181eca0a1b1d708e502 |
| `prefile-now.txt` (earlier status-only script, exit 1, 2026-10-22T20:23:13Z; superseded by the 20:27:07Z run, transcript head-truncated at 12 lines) | 8fbda07e03663b1d001d150eb2a4d86cc2f10ae4f22c4e92977b81cbeb566ba8 |

No installs or updates were made (no `uv`, `npx`, pacman or binary fetch ran). Lane files were not
modified; `SKILL.md` and the four instruments were read with `read`/`git show` only. At
2026-10-22T20:27:07Z `git status --porcelain` (E12) listed no `SKILL.md` entry, so the working copy
equals the tip blob and the line numbers above are the tip's.
