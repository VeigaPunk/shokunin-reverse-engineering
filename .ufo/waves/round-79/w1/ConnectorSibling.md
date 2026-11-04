# ConnectorSibling — round 79, wave 1 (cross-lane, read-only)

Scope: does a sibling lane already implement (a) a selftest-mutation battery or (b) a
line-bound pointer / source-position checker, and what does this lane's version add or miss?

Method: read-only grep over `/home/vgpnk/Projects/shokunin/*/tools/` and `*/scripts/`; no
sibling lane written, no sibling gate run. Two probes imported this lane's own modules
under `/fast/scratch/hyaku/kaidoku-r79/ConnectorSibling/` (deleted before yield) and are
retained as receipts in `ConnectorSibling/`.

---

## 1. Precedents

Both surfaces **already exist** in sibling lanes. Four concrete precedents, quoted at line.

### P1 — tameshi `tools/pointer-recheck.py:41-44` (line-bound pointer binder)

> "a row is met when its verdict equals its expect (an expect=miss row is the standing red
> arm: the drift is MEASURED on every sweep, never assumed, and stays measured until a
> superseding record carries the correction — the r48/r69/r70 append-only precedent)."

Supporting clauses at `:36` — "A row whose defect does not exist in the record bytes is
refused, not passed (the r70 mistake-1 practice one level up)"; `:58` — "record_rev (40-hex;
pin the revision whose bytes you verified against, never \"tip\")"; `:59` — "start, end
(1-indexed inclusive)"; `:104` — "def `sed_span`", the engine of record
`git cat-file blob <rev>:<path> | sed -n 'START,ENDp'` (no shell, `sed` unspawnable = exit 2,
never a silent fallback).

Properties:

| | verdict |
|---|---|
| (i) counts an absent detector as a pass | **No.** A row whose cited token is absent from the record bytes is an ERROR (unexpected), exit 1. |
| (ii) treats a pointer's line or range | **Yes.** 1-indexed inclusive `start`/`end`, span materialized from git objects at `target_rev`, never the worktree. |
| (iii) pins the mutated target by digest | n/a (no mutation). Pins both record and target by 40-hex revision. |

### P2 — tameshi `tools/mutate-and-run.sh:36` (generic mutation battery)

> "Per-defect verdicts: KILLED (suite exit != 0) | SURVIVED (suite exit 0) |
> INCONCLUSIVE (timeout 124, or 126/127 = suite not runnable)."

Supporting clauses at `:31` — "every mutant is a fresh copy of a pinned pristine; one exact
edit per copy with a uniqueness assert; a green control run; killed/survived recorded per
defect; sha256 before/after as the restore proof"; `:228` — "`git show <rev>:<path>` —
immune to working-tree drift"; `:542` — "control run on the pristine copy is red …; cannot
attribute kills".

Properties:

| | verdict |
|---|---|
| (i) counts an absent detector as a pass | **No.** A suite that cannot run is a third bucket, INCONCLUSIVE, never counted as killed; a red control exits 2 rather than attributing kills. |
| (ii) treats a pointer's line or range | **No.** |
| (iii) pins the mutated target by digest | **Partial.** Revision-pinned (`git show <rev>:<path>`) with sha256 as a *restore proof*; it does not assert a declared digest equality on the mutated copy. |

### P3 — kama `tools/round75-survivor-probe.py:20` (selftest-arm mutation battery)

> "…runs the pristine module's selftest green and every mutated copy's selftest red, and
> names for each mutant the selftest arm that fails — `case-hex` …, `kind-boundary` …,
> `paragraph-scope` …, `conflict-off` … and `header-window` …"

The kill rule is `:87-89` — `killed = sum(row["mutant_exit"] == 1 and
EXPECTED_ARMS.get(row["mutant"]) in row["failed_arms"] for row in rows)`.

Properties:

| | verdict |
|---|---|
| (i) counts an absent detector as a pass | **No.** An absent declared arm is not in `failed_arms`, so the mutant is escaped. Note the sharper edge: an arm missing from the *whole* output trips `REQUIRED_ARMS.issubset(names)` at `:72-73` and raises `CouldNotEvaluate` (exit 2) — it aborts rather than being enumerated. |
| (ii) treats a pointer's line or range | **No.** |
| (iii) pins the mutated target by digest | **No.** `git clone --shared` at `:102` and mutate the clone's copy; only anchor uniqueness `original.count(old) != 1` at `:120`. |

This is the closest structural twin of R79-C1 in the fleet: same object (a committed
instrument), same unit (one named selftest arm), same rule (absent ⇒ not killed).

### P4 — tsukuroi `tools/mutants-kernel-taint.py:12` (inverted-polarity should-fail battery)

> "A mutant is ACCEPTED when the counter exits 0 with verified_rows 6."

Supporting clause at `:14-15` — "`should_fail_total`, `should_fail_accepted`,
`control_verified_rows`, and, for information, `other_accepted` (accepted mutants outside
the declared set)"; `:85` — `return rev, hashlib.sha256(blob).hexdigest()`; `:395` —
`'counter_sha256': COUNTER_SHA`.

Properties:

| | verdict |
|---|---|
| (i) counts an absent detector as a pass | **Yes, by declared polarity.** Non-detection is the *expected* outcome, but only for a declaratively enumerated set; acceptance outside that set lands in `other_accepted` and is never counted as satisfaction. |
| (ii) treats a pointer's line or range | **No.** |
| (iii) pins the mutated target by digest | **Yes.** `counter_sha256` of the blob at `counter_rev`, carried in the receipt. |

**Contradiction stated, not scored:** P3 and P4 disagree on polarity. P3 requires the mutant
to be *caught*; P4 requires it to be *missed*. Both are sound for their own claim, and
"absent ⇒ not a pass" survives in both — in P4 because the accepted set is declared, so an
undeclared acceptance is visible as `other_accepted` rather than silently green.

---

## 2. What this lane's version adds or misses

### R79-C1 `tools/round-79/gate-mutation.py` vs P3 (nearest twin) and P2

Adds:

- `--rev`: mutates the target at an arbitrary measured revision, not the clone's HEAD.
- `target_pin.matched`: a declared 64-hex digest of the mutated file
  (`TARGET_SHA256`), which P3 lacks entirely and P2 has only as a restore proof.
- **Absent declared case ⇒ SURVIVOR, counted against** — stricter than P2, which parks an
  unrunnable suite in an INCONCLUSIVE bucket, and stricter than P3, which aborts at exit 2.
  The absent detector can neither hide in an inconclusive count nor masquerade as an
  evaluation failure.
- Per-case attribution (`declared_case`, `failed_cases`, `detector_count`, `sole_detector`)
  — P2 grades only suite exit; P3 names one arm but records no detector count.
- `pristine` 29 cases / 0 failures as a literal pass precondition.

Misses:

- **`sole_detector` is computed and never graded.** `ok` at `:239-240` is
  `len(mutants)==len(MUTANTS) and survivors==0 and pin.matched and pristine.ok`;
  `validate_receipt` never inspects `detector_count` or `sole_detector`.
- No `expect`-style field, so a deliberately-red mutant cannot be a met arm (P1's pattern,
  adapted).

### R79-C2 `tools/round-79/pointer-bind.py` vs P1

Adds:

- Bespoke to a prose record: five *named* drift-prone cells (three REA pins, the Ghidra
  `application.version` line, the `.bashrc` export range), each bound to a declared token.
- `--control path-only`: reproduces the round-78 rule (path exists, line unread) on the same
  stale record to show it cannot fail. Neither sibling has a *rule-reproduction* control;
  P1's `expect=miss` arms are a different device.
- `line_sha256` of the pointed span instead of its bytes — matches kama
  `tools/append-only-audit.py:176` (`DHEADER = "commit\tfile\tline_sha256\tcount\tclass\tnote"`)
  and satisfies the bounds' digest-not-bytes rule.
- `unparsed` is a first-class failure and `ok` additionally requires `checks_total == 5`, so
  a vanished record cell fails rather than vacuously passing (the same instinct as P1's
  zero-row manifest guard at `:51`).

Misses:

- **No `expect` field** (P1 `:41-44`): a known-stale pointer that cannot be repaired has no
  representable met state, so the only remedy is to delete the pointer — the drift
  laundering the instrument exists to prevent.
- **Regex-discovered, not manifest-enumerated cells.** Multiplicity collapses silently; see
  §3.
- **`validate_receipt` re-derives counts only from the receipt's own `checks` list** and
  never re-reads PROVINCE.md or any target. The lane's own selftest enshrines this as
  `green-forged-consistent`: a fabricated receipt with plausible 64-char digests validates
  with `defects: []`.
- `line_sha256` is tested only for truthiness (`if check.get("matched") and not
  check.get("line_sha256")`), never for 64-hex shape — contrast `record.sha256`, which is
  length-checked.
- Targets are read from the worktree while the record is read from git (`read_lines` vs
  `git_show`). This is **forced, not a defect**: the pointed targets are ambient host files
  (`~/.config/devin/mcp_config.json`, `~/.kimi-code/config.toml`, `~/.bashrc`, the Ghidra
  properties) that are not in any git object store, so P1's `target_rev` device cannot
  apply. `line_sha256` is the only available pin, and it is taken.

---

## 3. Gap — one attack a sibling pattern catches that round 79 does not

**Attack: multiplicity laundering in the record.** `pointer-bind.py` *discovers* its five
checks by regex instead of enumerating them, and both discovery paths collapse duplicates
without a count:

- `parse_record` builds `pins = {name: (pin, pointer) for name, pin, pointer in
  RE_PIN.findall(text)}` — a dict comprehension, so a second cell for the same client
  silently overwrites the first (last wins).
- `RE_GHIDRA_PTR` and `RE_BASHRC_PTR` use `.search()`, so a stale quotation placed earlier
  in the file wins over the live cell.

Measured with the lane's own module (receipt: `ConnectorSibling/parse-multiplicity-probe.txt`):

```
duplicate-client:  parsed=5 unparsed=[]   devin-pin binds -> /h/devin.json:999
ordered-quotation: parsed=5 unparsed=[]   bashrc-exports binds -> /h/.bashrc:23-24
VERDICT: checks_total stays 5 and unparsed stays [] in both shapes,
         so the 5-check predicate cannot distinguish 5 cells from more.
```

A record carrying six or more pointer cells — e.g. a corrected cell appended below a stale
one, or a historical range quoted in backticked pointer form above the live one — still
reports `checks_total 5, matched 5, mismatches 0, unparsed 0`. The 5-check guard is
cardinality over *parsed results*, not exhaustiveness over the record.

The sibling pattern that closes it is **P1's manifest form**: each row carries an explicit
`id` and "the exact cited token", and a row whose token is absent from the record bytes is
"refused, not passed" (`:36`). Multiplicity must then be *written down* — a second stale
cell needs a second row, and that row measures `miss` or ERROR instead of vanishing. P4
closes the same hole from the other side by making the accepted set declarative and
reporting everything outside it.

Search that located the pattern (exact command and count):

```
grep -rlE 'mutant|survivor|mutation' --include='*.py' --include='*.sh' --include='*.md' \
  */tools/ */scripts/ | grep -v '^kaidoku-shokunin/' | wc -l
176
```

and for the pointer surface:

```
grep -rlE 'line_sha256|line_sha|line number|line-number|pointer|expected_line|line_no|lineno' \
  --include='*.py' --include='*.sh' --include='*.md' */tools/ */scripts/ \
  | grep -v '^kaidoku-shokunin/' | wc -l
189
```

**Secondary finding (not the declared gap), same shape.** `gate-mutation.py` records
`sole_detector` and never grades it. Measured (`ConnectorSibling/sole-detector-probe.txt`):
a mutant under which all 29 cases are red yields `killed: True, detector_count: 29,
sole_detector: False`, and a receipt carrying eight such mutants validates with
`defects: []`. The kill is real (the gate did go red) but is not attributable to the
declared case, so a mass-failure mutant is indistinguishable from a discriminating one.
tameshi `tools/shrink-case.py:11` is the sibling that closes this class — "A kill is the
round-49 generator's oracle read of the pair: `check` passes on the pristine guard and fails
on the mutant", reduced "to a fixpoint, so the result is 1-minimal: removing any one unit
loses the kill."

Both findings are one structural property: **singularity of the evidence**. R79-C1 accepts a
kill many cases produced; R79-C2 accepts a check set a regex discovered. Neither instrument
currently distinguishes *one witness* from *at least one witness*.

Neither finding falsifies a frozen arm. The live record at the freeze parses exactly five
cells with no duplicates, and the three mutants named sole in the predicate are sole in the
receipt. Both attacks are latent, and both are bounded to what the receipts already carry.

---

## 4. Registry pre-append duplicate check (referee for the source seat)

**Do not append. Both rows already exist in the working tree — but neither is in the freeze.**

| id | worktree line | source | status |
|---|---|---|---|
| `S295` | 212 | POSIX.1-2024 `grep` — `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html` | `mined`, 2026-11-04 |
| `S296` | 213 | cargo-mutants book, Welcome — `https://mutants.rs/` | `mined`, 2026-11-04 |

Revision detail, because it changes what "already holds" means:

```
git show ed68cd0a:corpus/SOURCES.md | grep -cE '^\| S[0-9]+ \|'   -> 200   (329 lines)
grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md                        -> 202   (331 lines)
git show ed68cd0a:corpus/SOURCES.md | grep -E '^\| S29[56] \|'      -> no match
```

So at the freeze `ed68cd0a` neither source is registered; both rows arrived afterwards as
**uncommitted working-tree additions** (the `+S295` / `+S296` hunks in
`git diff corpus/SOURCES.md`). The line numbers 212 and 213 are therefore worktree-relative,
not freeze-relative. A source seat working from the freeze revision will find them absent and
be tempted to append; it must not — the duplicate already landed.

Both name snapshots in `.ufo/waves/round-79/l1/sources/` (`grep-posix.html` 21 316 B, sha256
`9473205c…`; `cargo-mutants.html` 22 602 B, sha256 `d056b2b3…`). S295 already grounds `pointer-bind.py`'s
1-based per-file line rule; S296 already grounds the survivor rule in `gate-mutation.py`
("a mutant is killed only when a case fails; a mutant with no failing detector survives").

### Live-state note (concurrent seat, not my write)

`git status` at survey time shows `tools/round-79/pointer-bind.py` modified. The diff is
**CLI-only** — `--battery` becomes optional when `--rev` is supplied, plus the docstring and
usage line at `:17-22` and `:316-323`. `parse_record` is byte-identical to the freeze, so the
probes in §3 were taken against the live parser and remain valid, and the frozen counting
command still runs unchanged.

---

## 5. Proposed move (bounded, one)

Record the **singularity diagnostic** as a falsification artifact, additively, without
touching the frozen predicate, `claims.json`, or any landed receipt.

- R79-C1 already emits `detector_count` and `sole_detector` per mutant; the round-79 lesson
  draft should state, for all eight mutants, whether the declared case was the sole failing
  case — not just for `m03`, `m05`, `m08`. No new measurement is required.
- R79-C2 should record `cells_parsed` (pin cells found, Ghidra cells found, `.bashrc` cells
  found) beside `checks_total`, so a duplicate becomes visible instead of collapsing. Again
  no new I/O: the matches are already in hand at `parse_record`.

Axes improved: falsification and lesson draft. Axes unharmed: freeze integrity (no predicate
or receipt changes), re-derivation (counts stay re-derivable), source rows (no new row),
security review (no new bytes retained — digests only).

Risk: a reader could mistake the added diagnostic for a contract tightening. It MUST be
labelled post-freeze and non-enforcing; if either instrument is re-run for a future round,
the extra field is new information, not a silent change to R79-C1 or R79-C2.

---

## 6. Evidence index

| file | what |
|---|---|
| `ConnectorSibling/parse-multiplicity-probe.txt` | live import of `pointer-bind.py`; duplicate-cell and ordered-quotation collapse |
| `ConnectorSibling/sole-detector-probe.txt` | live import of `gate-mutation.py`; mass-failure mutant judged killed, receipt valid |
| `ConnectorSibling/connector-receipt.json` | machine receipt: precedents, gap, registry_hits |

No sibling lane was written; no sibling gate was run; no production file was edited. Scratch
`/fast/scratch/hyaku/kaidoku-r79/ConnectorSibling/` was removed before yield.
