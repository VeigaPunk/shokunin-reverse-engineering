# MutationTester — round 84, wave r84-w1

Independent mutation probe beyond the frozen 13. Claims touched: **R84-C2 only** (read-only on the
C1/C3 predicates). No lane tool, predicate, counter, mutant table or fixture was edited.

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Measured revision: `fa92d34aec31ae59cb19a8a6ea9e6c0ac7a2392f` (HEAD)
- Declaration revision: `e0de2088a7bddc16305357f90ac7e889fa0a0d11`; first container `a5663ddedd157bb9113928f5fe80509d6f3fc7a1`
- Receipts: `.ufo/waves/round-84/w1/MutationTester/{probe.json,evidence.json,manifest.json,battery/}`

## Inputs and the state of the nine declared cases

Read (never edited), sha256:

| frozen input | sha256 |
|---|---|
| `tools/round-82/conjunction-gate.py` | `f009009993160ca40dd55d771f8c05ce1e32799c22450f5430cae2c6e0bf163a` |
| `tools/round-82/printed-command.py` | `88b1dff2385547e1bdb2ecf802d667c38eabe929747075c27ae88f0c5c061487` |
| `tools/round-83/source-bind.py` | `800a759e20096859a145cfbe3f95e199502f7aa38b8ca796575d00af5963db3c` |
| `.ufo/waves/round-84/mutants.json` | 13 rows, ids `floor, failure, binder, membership, pin-call, static-refusal, source-mined, source-date, source-base, source-plan, source-entry, sb-header-position, sb-duplicate-last` |
| `plans/round-84-claims.md`, `.ufo/waves/round-84/claims.json` | read for the predicate and the nine case names |

**The nine newly declared cases do not exist at the declaration revision, nor at HEAD.** The three
target tools are byte-identical across `e0de2088`, `a5663dde` and `HEAD` (`git diff --stat` empty
for all three), and none of `runtime-pin-mismatch-refused`, `static-defect-no-execution`,
`sourced-row-rejected-status`, `sourced-row-wrong-date`, `sourced-row-at-base`,
`sourced-plan-missing`, `sourced-entry-uncited`, `late-single-header`, `duplicate-target-second`
appears in any of the three scripts. The probe therefore worked against the **frozen detectors
only** — the three tools' existing `--selftest` case sets — as the assignment directs.

## Method

For each mutant: copy the target out of the lane into
`/fast/scratch/hyaku/kaidoku-r84/MutationTester/pristine/`, assert the `find` string occurs
**exactly once**, write the patched copy under `work/<id>/`, run
`python3 -I -B <copy> --selftest` with `cwd=<mutant dir>`, `TMPDIR` inside that dir and
`PYTHONDONTWRITEBYTECODE=1`, and score:

- **killed** — pristine `--selftest` green (rc 0, zero failures) *and* the mutant run is red, with
  the failing case named;
- **survived** — pristine green and the mutant run green with zero failures;
- **inconclusive** — anchor count ≠ 1 or pristine not green.

Pristine bytes were never written to: the copy's sha256 was re-read after every mutant run and is
equal to its pre-run digest for all 24 probes (`restored_equal: true` in `probe.json`). The lane
tools were untouched; the battery runs below only `git show` the lane and write inside scratch.

The `--selftest` is the bounded detector the frozen C2 closure uses, so it is the verdict here.
Two mutants were additionally classified with the instrument's own `--battery` on the real lane
(read-only; work under scratch) to say whether the *production* path sees them. That is
classification evidence, not the verdict.

## Case inventory (frozen detectors, pristine, all green)

- `tools/round-82/conjunction-gate.py` — rc 0, **21 cases**: `binder-deficiency-frozen-accepts,
  binder-refused, detector-absent-refused, detector-nonunique-refused, detector-passing-refused,
  failures-deficiency-frozen-accepts, failures-refused, first-declared-defect-binder,
  floor-deficiency-frozen-accepts, floor-refused, frozen-rule-agrees-genuine,
  frozen-rule-not-killed-refused, genuine-synthetic-passes, mutants-refused,
  original-names-refused, pristine-exit-refused, summary-bool-refused,
  summary-floor-independent, survivors-refused, validate-consistent-clean,
  validate-refused-mismatch`
- `tools/round-82/printed-command.py` — rc 0, **15 cases**: `bare-name-refused, ellipsis-refused,
  entry-cites-no-source-line, entry-cites-true, entry-cites-wrong-row, fixture-repo-top,
  metachar-refused, pin-match-accepts, pin-mismatch-refused, placeholder-refused,
  prefix-refused, row-parse-absent, row-parse-mined, row-parse-queued-unmet,
  unpinned-path-refused`
- `tools/round-83/source-bind.py` — rc 0, **6 checks**: `positive, withdrawn, malformed,
  duplicate, duplicate-after-window, unavailable`

Case-name inventories for these three are also recorded in `probe.json` under `pristine`.

## Results — 24 mutants, 2 killed, 22 survived, 0 inconclusive

None of the 24 reuses a frozen-table edit: every `(find, replace)` pair differs from the 13 frozen
edits, and each targets one of the six assigned areas (A–F) plus two auxiliary conjunction-gate
probes (G). Seven probes reuse a frozen *anchor site* with a different replacement
(`cells[8] == "mined"` ×2, `cells[9] == "2026-11-04"`, `len(cases) < PRISTINE_FLOOR`,
`if script not in pins:`, `if len(fields) != 1 or fields[0][0] >= 12:` ×2); the behavior change in
each is distinct from the frozen one, as the table shows.

| id | area | target | find | replace | verdict | failing case |
|---|---|---|---|---|---|---|
| pc-row-last | A row-parse | printed-command.py | `"    for line in text.splitlines():\n        if ROW_RE.match(line) and ROW_RE.match(line).group(\"id\") == sid:\n            return line\n    return None\n"` | `"    rows = [line for line in text.splitlines()\n            if ROW_RE.match(line) and ROW_RE.match(line).group(\"id\") == sid]\n    return rows[-1] if rows else None\n"` | survived | — |
| pc-row-prefix | A row-parse | printed-command.py | `"        if ROW_RE.match(line) and ROW_RE.match(line).group(\"id\") == sid:"` | `"        if ROW_RE.match(line) and ROW_RE.match(line).group(\"id\").startswith(sid):"` | survived | — |
| pc-cells-len-ge | B cells | printed-command.py | `"row_ok = bool(len(cells) == 13 and cells[8] == \"mined\""` | `"row_ok = bool(len(cells) >= 13 and cells[8] == \"mined\""` | survived | — |
| pc-cells-status-ne-queued | B cells | printed-command.py | `"cells[8] == \"mined\""` | `"cells[8] != \"queued\""` | survived | — |
| pc-cells-date-ge | B cells | printed-command.py | `"cells[9] == \"2026-11-04\""` | `"cells[9] >= \"2026-11-04\""` | survived | — |
| pc-cells-index-shift | B cells | printed-command.py | `"cells[8] == \"mined\""` | `"cells[7] == \"mined\""` | survived | — |
| sb-window-13th | C entry_cites | source-bind.py | `"if len(fields) != 1 or fields[0][0] >= 12:"` | `"if len(fields) != 1 or fields[0][0] > 12:"` | survived | — |
| sb-two-fields-first | C entry_cites | source-bind.py | `"if len(fields) != 1 or fields[0][0] >= 12:"` | `"if len(fields) < 1 or fields[0][0] >= 12:"` | **killed** | `duplicate`, `duplicate-after-window` |
| sb-emdash-optional | C entry_cites | source-bind.py | `"r\"source: (S[0-9]{3,}(?:, *S[0-9]{3,})*) — .*\""` | `"r\"source: (S[0-9]{3,}(?:, *S[0-9]{3,})*) .*\""` | survived | — |
| sb-id-substring | C entry_cites | source-bind.py | `"return sid in [part.strip() for part in match.group(1).split(\",\")]"` | `"return sid in match.group(1)"` | survived | — |
| pc-entry-any-line | C entry_cites | printed-command.py | `"    for line in text.splitlines():\n        if line.startswith(\"source:\"):\n            return sid in re.findall(r\"\\bS[0-9]+\\b\", line)\n    return False\n"` | `"    return any(line.startswith(\"source:\")\n               and sid in re.findall(r\"\\bS[0-9]+\\b\", line)\n               for line in text.splitlines())\n"` | survived | — |
| pc-pin-normprefix | D pin-membership | printed-command.py | `"if script not in pins:"` | `"if script.removeprefix(\"./\") not in pins:"` | survived | — |
| pc-pin-traversal-basename | D pin-membership | printed-command.py | `"if \"..\" in script:"` | `"if \"..\" in os.path.basename(script):"` | survived | — |
| pc-run-rc1-strict | E run-defects | printed-command.py | `"    if proc.returncode != 0 and not (expect_counter is None\n                                     and proc.returncode == 1):\n"` | `"    if proc.returncode != 0:\n"` | survived | — |
| pc-run-counter-type | E run-defects | printed-command.py | `"if not isinstance(value, int):"` | `"if value is None:"` | survived | — |
| pc-run-counter-mismatch-raw | E run-defects | printed-command.py | `"elif str(value) != expect_counter:"` | `"elif value != expect_counter:"` | survived | — |
| pc-run-defects-static-dropped | E run-defects | printed-command.py | `"result[\"defects\"] = list(result[\"static_defects\"])"` | `"result[\"defects\"] = []"` | survived | — |
| pc-battery-verdict-drop-sourced | E run-defects | printed-command.py | `"ok = all(a[\"met\"] for a in arms)"` | `"ok = all(a[\"met\"] for a in arms[:-1])"` | survived | — |
| pc-token-metachar-drop-pipe | F tokenizer | printed-command.py | `"METACHARS = (\";\", \"|\", \"&\", \"$(\", \"`\", \">\", \"<\")"` | `"METACHARS = (\";\", \"&\", \"$(\", \"`\", \">\", \"<\")"` | survived | — |
| pc-token-ellipsis-drop-ascii | F tokenizer | printed-command.py | `"ELLIPSIS = (\"\\u2026\", \"...\")"` | `"ELLIPSIS = (\"\\u2026\",)"` | survived | — |
| pc-token-allowlist-widened | F tokenizer | printed-command.py | `"ALLOWED_VARS = {\"REV\", \"WORK\", \"OUT\", \"ROOT\"}"` | `"ALLOWED_VARS = {\"REV\", \"WORK\", \"OUT\", \"ROOT\", \"PLAN\"}"` | survived | — |
| pc-token-unbound-maxlen | F tokenizer | printed-command.py | `"UNBOUND_RE = re.compile(r\"<[^>\\n]{1,120}>\")"` | `"UNBOUND_RE = re.compile(r\"<[^>\\n]{1,20}>\")"` | survived | — |
| cg-frozen-detector-ge | G aux conjunction | conjunction-gate.py | `"        and len(detector) == 1\n        and detector[0].get(\"pass\") is False"` | `"        and len(detector) >= 1\n        and detector[0].get(\"pass\") is False"` | survived | — |
| cg-floor-le | G aux conjunction | conjunction-gate.py | `"len(cases) < PRISTINE_FLOOR"` | `"len(cases) <= PRISTINE_FLOOR"` | **killed** | `genuine-synthetic-passes` |

Anchors: every `find` occurred exactly once in its pristine target (`anchor_occurrences: 1` for all
24); no probe was inconclusive.

## Survivor classification

### 1. Genuine gaps — no existing case and none of the nine declared cases closes them (15)

Each survivor below leaves the frozen detector green, and the nine declared case names do not
name the behavior. Where a production difference exists it is stated.

1. **pc-row-last** (A). Two rows for one id: pristine binds the first, the mutant the last. No
   fixture has two rows for one id; no declared case covers row-selection order. Neutral on today's
   ledger (one `S299` row).
2. **pc-row-prefix** (A). Id binds by prefix, so `S299` matches a row whose id is `S2999`. No
   declared case covers the id grammar boundary. Neutral on today's ledger.
3. **pc-cells-len-ge** (B). Row width becomes a floor: a 14+-cell row is accepted. No declared case
   names row width; neutral on today's 13-cell row.
4. **pc-cells-index-shift** (B). Status is read from `cells[7]` (the `teaches` column) instead of
   `cells[8]`. Would be killed only by a case asserting a fully-mined row is **green** — none of the
   nine names one; the five sourced-arm cases all assert a *red* arm. Production: neutral today
   (pristine is already red on the real row).
5. **sb-emdash-optional** (C). The frozen grammar's `space-em-dash-space` separator becomes
   optional. Demonstrated with the tool's own CLI: entry `source: S299 is cited here` (sid `S299`) —
   pristine `rc 1, cites false, not-attributed`; mutant `rc 0, cites true, attributed`. No frozen
   mutant touches the separator at all, and none of the nine does either. **False attribution.**
6. **sb-id-substring** (C). Membership becomes a substring test. Demonstrated: entry
   `source: S2999 — https://example.com/b` (sid `S299`) — pristine `rc 1, not-attributed`; mutant
   `rc 0, attributed`. The frozen table's `sb-header-position`/`sb-duplicate-last` cover the window
   and the duplicate-direction only. **False attribution across id boundaries.**
7. **pc-entry-any-line** (C). printed-command's own `entry_cites` accepts *any* source line instead
   of the first. Fixtures carry one source line each; neutral on today's round-82 entry (one
   `source:` line), so no declared case and no battery arm sees it.
8. **pc-pin-normprefix** (D). Membership is checked after `./`-stripping. Demonstrated at
   `build_argv`: `python3 -I -B ./tools/round-82/conjunction-gate.py …` — pristine
   `REFUSED: SCRIPT_NOT_PINNED`; mutant `ADMITTED`. The frozen `membership` mutant only disables the
   check outright; what the check *admits* is untested by both the frozen table and the nine.
9. **pc-run-rc1-strict** (E). The no-expectation rc-1 executability acceptance is deleted, so every
   rc-1 block becomes `EXECUTION_FAILED`. The selftest never calls `run_block`, and
   `static-defect-no-execution` (absent) asserts the static early return, not the rc policy.
10. **pc-run-counter-type** (E). `COUNTER_NOT_INTEGER` degrades to a `None` check; a string counter
    now passes the executability arm. No case exercises it (no declared case names it).
11. **pc-run-counter-mismatch-raw** (E). `COUNTER_MISMATCH` compares raw values, so an int `13`
    against expectation `"13"` would be flagged. The battery always passes `expect_counter=None`,
    so this branch is dead in production *and* unasserted in the selftest.
12. **pc-token-metachar-drop-pipe** (F). `|` is no longer a static defect. The only metacharacter
    exercised anywhere is `;` (`metachar-refused` and the `shell-meta` control); `|`, `&`, `$(`,
    the backtick and `>` have no case.
13. **pc-token-ellipsis-drop-ascii** (F). ASCII `...` is no longer refused; only `…` is exercised
    (`ellipsis-refused`). No declared case names the abbreviation set.
14. **pc-token-allowlist-widened** (F). The four-key variable allowlist gains `PLAN`. **No fixture in
    the selftest or the battery contains an unbound variable at all** (`$REV`/`$OUT` only), so
    `VARIABLE_UNBOUND` has zero coverage.
15. **cg-frozen-detector-ge** (G). The re-derived frozen rule accepts duplicate detector rows.
    Demonstrated: `synthetic_genuine()` with the detector row duplicated — pristine
    `frozen_killed False`; mutant `frozen_killed True` (while `conjunction` still refuses). The
    existing `detector-nonunique-refused` asserts only the conjunction verdict, so the
    **re-derivation of the pinned rule itself** is unasserted for duplicates.

### 2. Covered by one of the nine declared-but-absent cases (2)

- **pc-cells-status-ne-queued** (B). Status is accepted by exclusion (`!= "queued"`). This is the
  highest-severity survivor: on the real lane the `S299` row's status cell is `rejected`, so the
  pristine battery is **red** (`rc 1, arms_ok 5, unmet ["sourced"]`, matching the round-82 landing
  receipt `c2-at-landing.json`, defects `["SOURCED_ROW_UNMET"]`), while the mutant battery is
  **green** (`rc 0, arms_ok 6, unmet []`). The instrument would certify a `rejected` row as mined.
  The declared case **`sourced-row-rejected-status`** would kill this mutant (a rejected-status row
  must keep the arm red), so this is a detector gap at HEAD, not a plan-coverage gap.
- **sb-window-13th** (C). `>= 12` → `> 12` admits a single source field on the 13th line.
  Demonstrated with the CLI: entry with 12 empty lines then `source: S299 — …` (line 13, index 12) —
  pristine `rc 1, not-attributed`; mutant `rc 0, attributed`. Line 12 (index 11) is admitted by both,
  so the fixture must sit exactly on line 13. The declared case **`late-single-header`** would kill
  it. Note the existing `duplicate-after-window` fixture cannot: it has two fields, so the
  `len(fields) != 1` conjunct rejects it before the window is consulted.

### 3. Conditional — depends on how the declared fixture is built (2)

- **pc-cells-date-ge** (B). Date bound by `>=`. The declared `sourced-row-wrong-date` kills it only
  if its wrong-date fixture is **later** than `2026-11-04`; a fixture with an earlier wrong date is
  refused by the mutant too and the mutant survives that case.
- **pc-run-defects-static-dropped** (E). Static defects stop being copied into the aggregated
  `defects` ledger (the early return still fires, `static_defects` still populated). Killed by
  `static-defect-no-execution` only if that case asserts the aggregated ledger rather than the
  `static_defects` list; the battery's own `static-refusal` arm reads `static_defects`, so it stays
  green either way.

### 4. Verdict-neutral / equivalent mutants — not coverage findings (3)

- **pc-pin-traversal-basename** (D). Narrowing the `..` guard to the basename is neutral because the
  allowlist membership refuses every token that still contains a directory `..` (demonstrated:
  `tools/round-82/../round-82/conjunction-gate.py` → `REFUSED: script escapes the lane tree` on
  pristine, `REFUSED: SCRIPT_NOT_PINNED` on the mutant — same verdict, different reason). Like the
  frozen `floor` pair, the guard is doubled; only one of the two is load-bearing.
- **pc-token-unbound-maxlen** (F). Narrowing the placeholder bound to 20 characters is neutral on
  every existing input: the only placeholder anywhere is `<measured>` (8 inner characters), and `<`
  is independently a `SHELL_METACHAR`.
- **pc-battery-verdict-drop-sourced** (E). Dropping the sourced arm from the battery verdict line is
  caught by `validate_battery`: `rc 1, arms_ok 5, unmet [], validate_defects
  ["verdict_not_rederived"]` (pristine: `unmet ["sourced"], validate_defects []`). The receipt stays
  red, so the second guard holds — but note `validate_battery` itself has **no selftest case at
  all**, and the frozen table has no mutant on it.

## Kills and the boundaries they prove measured

- **sb-two-fields-first** — two source fields accepted, first authoritative: killed by `duplicate`
  and `duplicate-after-window`. The *field-count* boundary is measured in both directions (the
  frozen `sb-duplicate-last` covers last-wins).
- **cg-floor-le** — `len(cases) < PRISTINE_FLOOR` → `<=`: killed by `genuine-synthetic-passes`
  (the genuine control carries exactly 11 = `PRISTINE_FLOOR` cases), so the floor boundary at 11 is
  measured inclusively. This is the direct contrast with the 12-line window: the floor's boundary is
  pinned exactly, the window's 13th line is not.

## Does any survivor indicate a declared case the frozen table does not cover?

Yes — 15, listed in §1. The strongest are `sb-emdash-optional` and `sb-id-substring` (both produce
demonstrated false attribution in `entry_cites` and the frozen table has **no mutant at all** on the
separator or on id membership), `cg-frozen-detector-ge` (the gate's own re-derived frozen rule
over-accepts duplicate detectors), and the run-path/tokenizer set (`pc-run-rc1-strict`,
`pc-run-counter-type`, `pc-run-counter-mismatch-raw`, `pc-token-allowlist-widened`,
`pc-token-metachar-drop-pipe`, `pc-token-ellipsis-drop-ascii`), whose sites the selftest never
reaches — the selftest never calls `run_block`, never tests an unbound variable, and tests exactly
one metacharacter and one abbreviation.

A survivor is a coverage finding only. None of the 22 changes the frozen contract, table, fixtures
or any predicate; nothing here is proposed as an edit. The frozen C2 closure (13/13) is unaffected
by this probe — the nine declared cases are the declared work, and this probe shows the margin
*beyond* them, plus two survivors the nine already close (`pc-cells-status-ne-queued`,
`sb-window-13th`) and one date-fixture shape (`sourced-row-wrong-date` must use a later date) that
matters for that closure.

## Write scope, restoration, tooling

- Writes: only `.ufo/waves/round-84/w1/MutationTester/` (this report, `probe.json`,
  `evidence.json`, `manifest.json`, `battery/`) and the scratch dir
  `/fast/scratch/hyaku/kaidoku-r84/MutationTester/`, which was **removed** after the receipts were
  copied. No production edits; no fleet or sibling-lane writes; no `git`/`jj` mutations, commits or
  pushes; no `task` spawns; no `agent://all`; never `/tmp`.
- Restoration: every mutant ran from its own copy; each pristine copy's sha256 was re-read after its
  mutant run and matched the pre-run digest (`restored_equal: true`, 24/24). The lane targets were
  only ever read (`git show` / file reads).
- Tooling: **nothing installed or upgraded** — the probe used `python3` (stdlib) and `git` only.
  No pacman invocation.
- Milestone relation: claim metadata (R84-C1) and the nested container chain (R84-C3) were only
  read; this seat's evidence bears on R84-C2's mutation closure.
