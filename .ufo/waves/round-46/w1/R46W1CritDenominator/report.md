# R46W1CritDenominator — interrogating the denominators

Seat: `R46W1CritDenominator` (critic, wave 1). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read-only on the lane tree; every write is under
`.ufo/waves/round-46/w1/R46W1CritDenominator/`. Scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1CritDenominator`, removed at the end.

Window: 2026-10-28T17:03Z–17:16Z. The lane moved under the seat: HEAD was `0425224`
when I started and `58eb04b6` (A4) when I stopped; `332f4884` = F5 landed at 17:09:45Z
while I was probing. Every receipt below therefore names the bytes it ran. Where a
finding was closed by F5 I say so rather than re-reporting it as open.

Frozen at `31820472784284727546808acc31b3ea1e73919b` (the commit the claims file's own
rule re-derives: `git log -1 --format=%H -- plans/round-46-claims.md`):
`attest.py` `dd1e7df1…`, `gate.py` `64626cca…`, `registry.py` `307506d5…`.

## 1. Verdict

| # | claim | what I measured | verdict |
|---|---|---|---|
| 1 | R46-C1 clause 8 / the shared freeze rule | at the derivable freeze both counters exit 2 at every rev ≥ `50862e4a`; every green receipt in `.ufo/waves/round-46/l1/scores/` is green only under a freeze at or after the commit that edited the instrument | **claim not met as frozen** |
| 2 | R46-C1 clause 5 (path set validated) | a block citing `SKILL.md:12` and `docs/plan.md:3` scores **0**, `refs` unchanged | **predicate ≠ implementation (open)** |
| 3 | R46-C2 clause 5 (presence) | a row for `tools/round-41/ghost-tool.py` inside the section scores **0**, 39 rows, `absent_at_rev []` | **the R45-CL2 shape survives (open)** |
| 4 | both batteries (`forgeries_total == 9`/`7`) | the denominator is an integer, not a name set: swap/duplicate a mutation and the battery still scores 9-0 / 7-0 | **substitution invisible (open)** |
| 5 | `genuine_green == 1` | tautological in the counter's own call graph; cannot be 0 when it is observed | **not a guard (open, low)** |
| 6 | `v1_green == 9` | measures the v1 port's row floor, not the forgery's severity: floor 9+ → `v1_green 8` → claim red | **clause mis-specified (open)** |
| 7 | frozen set derived at tip only | one commit rewriting `## Frozen paths (exact)` scored the tampered tree **clean, met_target true** against the committed `0425224` bytes | **closed by F5 at `58eb04b6`** (verified: exit 2) |
| 8 | counters execute from the worktree | `attest.py`/`gate.py` were dirty at 17:09Z while HEAD was `0425224`; the pin attested HEAD, not the running bytes | **closed by F5** (dirty arm) — reported for the record |
| 9 | claim's `Before` controls | 2 of 4 named control receipts were never committed; 1 exists under another name measuring something else; the C1 v1-profile control is unproducible at the freeze | **evidence gap (open)** |
| 10 | claim's preflight numbers | `registry.py --selftest` prints `cases=12`, the claim says 11; both documented commands exit 2 on argument parsing | **record drift (open, low)** |

## 2. The four assigned questions

### A1 — delete a mutation from `MUTATIONS`: what breaks, where?

Three nets, and only the first is in the battery:

1. `forgeries_total` drops to 8, and `score()` compares it to a hard-coded 9
   (`attest.py:254`, `registry.py:216`) → exit **1** with
   `battery forgeries_total 8 != 9` **and** `battery v1_green 8 != 9`: the error path in
   `run_battery` increments `forgeries_total` but not `v1_green` (`attest.py:415-418`),
   so a dropped mutation reports as *two* clauses and names neither the mutation nor the
   cause. Receipt `probe_c1.out` P12, `survivors-at-A4.json` S2 (re-confirmed at A4).
2. Deleting from the list changes `attest.py`'s bytes → block 23's pin mismatches at any
   rev that still pins the old bytes (code fact: `attest.py:245-252` compares the block's
   pin with `files(spec["pin"])`; not executed), and the quorum of the freeze arm is
   destroyed.
3. `tools/round-46/` is a frozen directory, so an *honest* freeze makes the commit that
   deletes it exit 2 `frozen_path_changed`.

What is **not** caught: a deletion *paired with a duplicate*. Keep the count at 9 and
replace `missing-routed-id` with a second `two-markers`:

```
P13 / S3: forgeries_total 9, v1_green 9, v2_green 0, genuine_green 1 → score exit 0
```

Same for C2: replace `no-header` with a second `off-section` →

```
S5: forgeries_total 7, v1_green 7, v2_green 0 → score exit 0
```

Nothing in either file compares the mutation *names* to the nine/seven names the frozen
claim file enumerates in parentheses. The names are documentation; the instrument asserts
an integer. `grep -c "m_missing_id"` is the only thing that would notice, and it is not a
clause.

### A2 — does `v1_green == 9` measure the forgery or the port?

The port. It is a *threshold* statement in disguise:

- `m_thin` deletes data rows from index 8 on (`attest.py:283-288`), leaving exactly **8**
  data rows; the v1 floor for the `r46` spec is `v1_min_rows: 8` (`attest.py:70`).
  The forgery is cut to sit on the floor. It is a v1 hole *because* the floor is 8.
- Make the v1 port stricter — floor 9, 10 or 11, all defensible readings of "round-45's
  clause set" given round-45's artefact had 10 rows and its spec floor was 8 — and:

```
P15 (floor 10): v1_green 8 → failing ['battery v1_green 8 != 9']  exit 1
P16 (floor 11): v1_green 8 → failing ['battery v1_green 8 != 9']  exit 1
```

So a *stricter, arguably more faithful* v1 port does not strengthen the measure — it
**fails the claim**, with a message ("v1_green 8 != 9") that does not distinguish "the
port is stricter" from "a forgery is weaker". The clause cannot tell those apart, so it
cannot be the evidence that the nine forgeries are severe; it is the evidence that the
port is loose in nine specific places, one of which is a knob.

The claim's intended independent control for this (`controls/ctl-c1-1-v1-profile.json`)
was never committed (§5), so there is no second measurement to lean on.

### A3 — is "the nine" the right denominator? Compare R45-CL13 a–f and R45-CL14 a–f.

No. There are **three different denominators in play and no map between them**:

- block 23's table: **13 rows / 13 routed `R45-CL` ids**;
- the battery: **9 mutations**;
- the predicate: **8 clauses, ~14 sub-arms**;
- the round-45 lessons: **12 letters** (CL13 a–f, CL14 a–f).

Mapping, from the fixtures' own `v2_failing` at A4:

| routed class | mutation | isolated? |
|---|---|---|
| CL13 (a) no sha256 pin | `stub-pin` | yes (clause 6) |
| CL13 (b) selector-less / self citation | `lineless-refs`, `self-refs` | yes (clause 5) |
| CL13 (c) header substring | `header-substring` | yes (clause 2) |
| CL13 (d) marker counted per block | `two-markers` | yes (clause 1, occurrence arm) |
| CL13 (e) block count inflated by a column-zero `- **…**` | **none** | v2 kills it (`P1`: "marker block is not the last craft block") — **defended, untested** |
| CL13 (f) malformed heading → exit 2 | **not a battery item** | selftest only |
| CL14 (a) fenced / comment / off-section rows | `fenced`, `html-comment`, `off-section` | yes (clause 1) |
| CL14 (b) `re.search` on cell 0 | `substring-cell` | yes (clause 3) |
| CL14 (c) first-wins shadow | `first-wins-shadow` | v1 shape fixed; **v2's `setdefault` is still order-dependent** (§4 F6) |
| CL14 (d) no header / any cell with 0,1,2 | `no-header`, `prose-exit` | yes (clauses 2, 4) |
| CL14 (e) a row naming a path at no revision | **no forgery** | **not defended at all** (`S4`) |
| CL14 (f) merge-introduced touch | **not a battery item** | freeze arm / selftest |

Plus two mutations that are **not** round-45 classes (`missing-routed-id`,
`no-vocab-arm` — round 45 had no routed-id or vocabulary check to hole), and
`garbage-rows`, which is CL13's 44-line artefact read at the clause-4 level.

Net: of the twelve routed letters, **ten are represented and two are not** (CL13 e, CL14 e —
one defended but unfixtured, one not defended); of the nine mutations, **two** are new-clause
guards rather than round-45 holes; and one mutation is **not arm-isolating**
(`missing-routed-id` also trips `rows 12 < 13`, so "a routed id is missing" has no unique
detector — R45-CL15's "arm-covering but not arm-isolating" recurring inside the battery
built to answer R45-CL15).

The right denominator is the predicate's clause set, because that is what the claim promises;
none of the three enumerations is that, and nothing checks that they agree.

### A4 — is `genuine_green == 1` a real guard against a counter that rejects everything?

No — as written it cannot fail. In the counter path the battery only runs when the structural
pass already returned 0 (`attest.py:449-451`, `registry.py:397-399`), and `genuine_green` is
set from *that same call* with `battery=None` (`attest.py:405-406`, `registry.py:337-339`).
`genuine_green` is therefore 1 whenever it is observable, and 0 never reaches a receipt
(a structural failure prints `battery: {"skipped": …}`). It is an echo, not a guard.

The property it is supposed to certify is held by the *structural* pass instead: a
reject-everything counter exits 1 on the clause list, and round-46's own do-nothing control
(`ctl-c1-0-do-nothing.json`) is the evidence for that. Meanwhile the opposite failure — a
counter that accepts only the exact landed bytes — is not covered by `genuine_green` either,
because the positive control *is* the landed artefact. I probed for it and v2 survived:

```
P10: a differently-shaped valid block (14 rows, an extra valid ref, two reworded cells)
     → exit 0, rows 14, refs 10
```

So v2 is a checker, not a checksum — that is a real result, but it is *my* probe, not the
claim's evidence. The battery has **nine negatives and one positive that is the artefact
itself**; a second, independently valid artefact is missing, and without it "green genuine"
cannot distinguish "accepts valid evidence" from "accepts these bytes".

## 3. The finding that decides the release: the freeze is caller-supplied

`gate.freeze_state(root, freeze, rev, claims)` resolves `--freeze`, checks it is an ancestor,
derives the frozen **set** at both ends (F5, `gate.py:144-190`) — and never checks that
`--freeze` *is* the freeze. The derivation the frozen claims file states
(`git log --format=%H -1 -- plans/round-46-claims.md`) is never computed.

Consequence, measured on one revision with two freezes:

| command | exit | `frozen_path_changed` |
|---|---|---|
| `attest.py --root L --freeze 3182047 --rev 0425224` (`base-c1.json`) | **2** | `['tools/round-46/', attest.py, gate.py, registry.py]`, `restored` same three |
| `attest.py --root L --freeze 0425224 --rev 0425224` (the L1's `c1-at-F4.json`) | **0** | `[]`, `touched 0` |
| `attest.py --root L --freeze 58eb04b6 --rev 58eb04b6` (`vacuous-c1-at-A4.json`) | **0** | `[]`, `touched 0` |
| `attest.py --root L --freeze 3182047 --rev 58eb04b6` (`base-c1-at-A4.json`) | **2** | `['tools/round-46/', attest.py, gate.py, registry.py]` |

Both counters behave identically (`base-c2.json`, `vacuous-c2-at-A4.json`). With
`freeze == rev` the history arm is empty and the blob arm compares a tree with itself; the
arm that the claim calls "the freeze-integrity **discrimination** matrix" is identically
satisfied. That is the round-45 disease in the round-46 instrument: a forgery — here the
choice of `--freeze` — satisfies the predicate.

The round's own receipts use **four distinct freezes, none of them the derivable one**:
`50862e4a` ×1, `65678df0` ×4, `0425224` ×4, `332f4884` ×2
(`grep -rho '"freeze": *"[0-9a-f]*"' .ufo/waves/round-46/l1/scores/`). `65678df0` and
`0425224` are the commits that *edited* the instrument (F3, F4); the freeze is moved to each
edit. The pin shows the same thing without needing the freeze argument at all:

| SKILL rev | pinned `sha256` | that hash is |
|---|---|---|
| `227d6982` | `eba5995…` | `50862e4a`'s attest.py, *not* the freeze's |
| `e3dfdbad`…`0425224` | `e6c44d2…` | `65678df0`'s (F3) attest.py |
| `58eb04b6` (A4) | `c405613…` | `332f4884`'s (F5) attest.py |
| **the freeze** | — | `dd1e7df1…` — **never pinned by any revision of block 23** |

Clause 6 says the pin matches "the interpreter's bytes at `--rev`", which it does; the
Freeze section says the interpreter's bytes do not change after the freeze. Both cannot hold
while the round edits the interpreter four times. So the claim, as frozen, is unsatisfiable:

> Under `--freeze 3182047` no revision ≥ `50862e4a` can score anything but exit 2, because
> `FREEZE..REV` contains commits that touched `tools/round-46/`. The round's green is only
> obtainable by passing a freeze the frozen file forbids.

This is `R45-CL24` (record drifted from the instrument) recurring one level up: the round
built a row for it and then declared a new freeze in a commit message. Note the F5 code
comment already credits two wave-1 seats (`R46W1RevRestoredUnion F2`, `F3`) for the tip-only
and dirty-worktree halves; my receipts independently confirm both against the pre-F5 bytes,
and I re-verified F5 closes them (tamper: exit 2; dirty: exit 2). The freeze-identity half is
*not* closed, and no amount of F5-style hardening can close it: the derivation must be
internal to `freeze_state`.

### Attacking the frozen set itself (attempted, then closed)

Against the committed `0425224` bytes I rewrote `## Frozen paths (exact)` in a clone to list
one harmless path and committed it on top of `0425224`:

```
attest.py (HEAD 0425224 bytes) --root clone --freeze 3182047 --rev <tampered>
→ exit 0, frozen_derived ['tools/round-46/census.json'], frozen_path_changed [],
  touched 0, met_target true, battery 9/9/0/1/0      (tamper-head.json)
```

The same command against F5's bytes: `exit 2`, `frozen_derived` unioned to three entries,
`frozen_path_changed` non-empty (`tamper-f5.json`). F5 closes it; I report it because it is
the receipt for *why* the union is needed, and because at `0425224` — the revision the
release headlines — the claim's clause 8 was false.

## 4. Findings, in the order the L1 should triage them

**F1 (HIGH; C1 + C2, shared `gate.py`) — the freeze argument is unvalidated.**
Counterexample as above (one rev, two freezes, opposite verdicts). Axis: both, because
`gate.py` is the shared prerequisite. Smallest safe correction: in `freeze_state`, derive
`derived = git log --diff-filter=A --format=%H -- <claims> | tail -1` and return
`exit 2 {"reason": "freeze_not_derived", "derived": …}` when `resolve(freeze) != derived`;
one selftest case (`freeze-mismatch-is-exit-2`). Also fix the claims file's own
re-derivation command: `git log -1 -- <path>` re-derives the *latest* touch, not the commit
that "first contains" the file — harmless only because the file was never edited, and the
one sentence a future L1 will use to re-declare a freeze.

**F2 (HIGH; release, both claims) — no admissible green at the declared freeze.**
`base-c1.json` / `base-c2.json` (exit 2) versus the L1's green receipts (exit 0, freeze =
instrument commit). Axis: both. Not an instrument defect: the instrument is right to exit 2.
Correction: do not score this round at a non-derived freeze. Either land C1/C2 at
`--freeze 3182047` (blocked until the instrument stops changing) or re-issue the claim so the
claims file *first appears* in a commit after the last instrument edit (round 47), which is
the only way the Freeze section's words can be true. Recommend the latter and record round 46
as `instrument landed, claim not met`.

**F3 (HIGH; C1 clause 5) — citations outside the three prefixes are invisible.**
Counterexample: append `` `SKILL.md:12`, `docs/plan.md:3` `` to block 23's Refs →
`exit 0`, `failing []`, `refs 9` (S1 at A4; `probe_fix.out` N1/N2 at `0425224`). `HARD_REF`
requires a `corpus|plans|tools` prefix, so "the path set is validated" is enforced only for
paths inside the set, and the comment above `HARD_REF` ("Every path-like citation is seen, so
a citation OUTSIDE the validated set is rejected rather than silently unmatched") is false.
Axis: depth. Correction: match every backticked token containing `/` or a `:line` selector,
then validate against `ALLOW`; add the two fixtures to the battery.

**F4 (HIGH; C2 clause 5) — the presence arm cannot see the R45-CL2 shape.**
Counterexample: insert a house-shaped row for `` `tools/round-41/ghost-tool.py` `` inside the
registry section → `exit 0`, `registry_rows 39`, `absent_at_rev []` (S4). `absent` is
computed over `registered`, i.e. census paths with a row (`registry.py:196-198`), and
`census.py` restricts the scope to paths that exist. So the arm fires only if a census tool is
deleted *after* the census was generated, never for a row naming something that never existed.
The one red case for this clause is `registry.py --selftest`'s `red-absent-at-rev`, and it
hand-writes a census naming `tools/round-46/ghost.py` with `files_present=two` — an input the
production generator cannot emit. The claim's own control for it
(`controls/ctl-c2-2-ghost-tool.json`) does not exist. Axis: calibration. Correction: check
presence for every backticked path in a row, not only scope paths; add the ghost row as
forgery #8.

**F5 (MEDIUM; both batteries) — the denominator is a count, not a name set.**
Swap/duplicate evidence above (S3, S5, P13, P14, N6). Axis: depth + calibration. Correction:
a frozen tuple `EXPECTED = ("garbage-rows", …)` in each counter, asserted equal to
`[n for n, *_ in MUTATIONS]` and to the claim file's parenthetical list; report the
`set(MUTATIONS)` names in the receipt so a swap is visible after the fact even if the tuple is
also edited (which changes the pin and the freeze arm).

**F6 (MEDIUM; C2 clause 3/4) — `by_path.setdefault` is still first-wins, so honest duplicate
rows are order-dependent.** A thin row before a good row for the same census path →
`exit 1 thin verdict-map cells: 1`; the same two rows reversed → `exit 0`. The *v1* shadow
forgery is gone (fenced rows no longer register), but the defect class it names — order
decides — survives in a shape the predicate permits. Calibration reading: the predicate says
"a row whose cell 0 is exactly the path", so the good-first case is compliant and the
thin-first case is a **false red**. Correction: choose the row deterministically (any row that
satisfies clauses 3 and 4; or fail if duplicates disagree).

**F7 (MEDIUM; C1 battery) — five predicate sub-arms have no red case anywhere.**
Matrix in §5. Concretely: a row with five cells (works, `P3`), a citation that does not
resolve at rev (works, `P6`), a block that drops `S142` (works, `N3`), `refs < 6`, and
CL13(e)'s column-zero bullet (works, `P1`) — all red when I build them, none of them a
fixture. Axis: depth. Correction: one fixture per sub-arm, named in the claim, plus make
`missing-routed-id` a *substitution* (13 rows kept) so the id arm has a unique detector.

**F8 (LOW; both counters) — `genuine_green` cannot fail.** §A4. Correction: replace it with
two positives (a second valid artefact and a degenerate-but-valid one) and a negative
(a counter setting that must reject the genuine artefact); or delete the key and state that
the structural clause list is the guard.

**F9 (LOW; claim record) — the `Before` controls do not resolve.**
`plans/round-46-claims.md` names `controls/ctl-c1-1-v1-profile.json` and
`controls/ctl-c2-2-ghost-tool.json`; `git log --all --diff-filter=A` shows neither was ever
committed. `ctl-c2-1-v1-profile.json` exists only as `ctl-c2-1-v1-scope.json`
(`"counter": "round-45-c2"`, `scope_size 6`) — a different measurement. And the C1 v1-profile
control is **unproducible at the freeze**: block 23 does not exist at `3182047` or at
`50862e4a` (`git show <rev>:SKILL.md | grep -c 'freeze-integrity-table v2'` → 0), so "the nine
forgery fixtures … at the freeze" has no block to mutate. Correction: cite the receipts that
exist, and put "the v1 profile accepts all nine forgeries" in the receipt that actually
measured it (`c1-at-A3`/`c1-at-F4` battery `v1_green`), with the freeze it used.

**F10 (LOW; claim record) — preflight numbers and commands.**
`registry.py --selftest` prints `cases=12 failures=0` at the freeze bytes and at A4; the claim
says 11. `attest.py --selftest` at the freeze prints 15 (claim correct); at A4 it prints 18
(F5's two new cases). Both documented commands, run literally, exit **2** on argparse because
`--root/--freeze/--rev` are required before the `--selftest` branch. Correction: write
`--selftest` as the command actually run (with the three args, or make them optional when
`--selftest` is set) and update the count.

**F11 (informational, closed) — frozen set derived at tip only.** Receipt `tamper-head.json`
(exit 0, met true). Closed by F5 (`tamper-f5.json`, exit 2). Keep the union; the residual is
that the *freeze* end is still whatever the caller passed (F1).

**F12 (informational, closed) — the counters executed dirty bytes.** At 17:09:07–17:09:19Z
`gate.py`/`attest.py` were modified in the worktree while HEAD was `0425224`; the pin matched
HEAD, so a green score at that moment would have attested bytes that were not executing.
Closed by F5's `frozen_worktree_dirty` arm (`gate.py:186-190`); confirmed by the empty
`git status --porcelain tools/round-46/` at A4.

**F13 (positive results, retained for the L1's evidence).**
- `out_path` refuses `--json-out` outside the lane root: my first invocation exited 2
  `--json-out outside the lane root: /fast/scratch/...` (R45-CL22 arm works).
- A valid variant block passes (`P10`) — v2 is a checker, not a byte hash.
- Structural red cases work where they are tested: 5-cell row, exit `3`, non-resolving ref,
  out-of-allow ref, dropped `S142`, column-zero bullet, `marker is not last`, malformed
  heading → exit 2.

## 5. Clause → red-case coverage (measured at A4, except where noted)

C1 (`attest.py`, battery 9 + selftest 18):

| clause | sub-arm | battery fixture | selftest case | standing |
|---|---|---|---|---|
| 1 | `marker_occurrences == 1` | `two-markers` | `red-no-marker`, `red-two-markers` | covered |
| 1 | block is last | — | `red-marker-not-last` | selftest only (CL13 e) |
| 1 | title starts `23. ` | — | `red-title-unnumbered` | selftest only |
| 2 | header equality | `header-substring` | `red-header-inexact` | covered |
| 3 | `rows >= 13` | `thin-rows` | `red-rows-thin` | covered |
| 3 | exactly four cells | — | — | **nothing** (`P3` red when built) |
| 3 | exit ∈ {0,1,2} | — | `red-exit-cell` | selftest only (`P4`) |
| 4 | routed ids | `garbage-rows`, `missing-routed-id` | `red-routed-id-missing` | covered, **not isolating** |
| 4 | arm vocabulary | `no-vocab-arm`, `garbage-rows` | `red-arm-vocabulary` | covered |
| 5 | `refs >= 6` | — | — | **nothing** |
| 5 | selector | `lineless-refs` | `red-ref-no-selector` | covered |
| 5 | path set | — | `red-ref-outside-allowlist` | selftest only, **and not universal** (F3) |
| 5 | resolves at rev | — | — | **nothing** (`P6`) |
| 5 | cites `round-45.md` | `self-refs` | — | battery only |
| 6 | `S142` | — | — | **nothing** (`N3`) |
| 6 | sha256 pin | `stub-pin` | `red-pin-mismatch` | covered (rev-relative, F2) |
| 8 | frozen touch | — | `red-frozen-touched`, `red-frozen-section-shrink`, `red-dirty-frozen-tool` | selftest only; **freeze-identity gap (F1)** |

C2 (`registry.py`, battery 7 + selftest 12): clauses 1–4 covered by
`fenced`/`off-section`/`html-comment`/`substring-cell`/`prose-exit`/`no-header` and
`red-unregistered`/`red-thin-exit`/`red-header-not-house`; clause 5 is the gap (F4);
clause 6 is the count-only denominator (F5); clause 7 is the freeze arm (F1).

## 6. Receipts

Every row: exact command, exit, sha256 of the captured stdout/receipt, UTC. Files are in
`.ufo/waves/round-46/w1/R46W1CritDenominator/`. `L` = lane root.

| # | command | exit | sha256 | UTC |
|---|---|---|---|---|
| R1 | `python3 -I -B tools/round-46/attest.py --root L --freeze 3182047 --rev 0425224 --json-out …/base-c1.json` | 2 | `18d2c32f…` (stdout) | 17:04:07Z |
| R2 | same with `registry.py` → `base-c2.json` | 2 | `2f6a9035…` | 17:04Z |
| R3 | `python3 -I -B probe_c1.py` (imports the lane's `attest`, fixtures under `$HYAKU_SCRATCH`) | 0 | `c7e0ef09…` (`probe_c1.out`) | 17:06:12Z |
| R4 | `python3 -I -B probe_c2.py` | 0 | `38504afc…` (`probe_c2.out`) | 17:07Z |
| R5 | `python3 -I -B probe_fix.py` | 0 | `270374ab…` (`probe_fix.out`) | 17:08Z |
| R6 | freeze bytes `attest.py --root / --freeze 0425224 --rev 0425224 --selftest` | 0 | `ac22e9c7…` `ATTEST_SELFTEST: cases=15 failures=0` | 17:09Z |
| R7 | freeze bytes `registry.py … --selftest` | 0 | `0fa8c31a…` `REGISTRY_SELFTEST: cases=12 failures=0` | 17:09Z |
| R8 | A4 bytes `attest.py … --selftest` | 0 | `6aa73c61…` `cases=18 failures=0` | 17:12Z |
| R9 | A4 bytes `attest.py --root L --freeze 3182047 --rev 58eb04b6 --json-out …/base-c1-at-A4.json` | 2 | `1fd60fd3…` | 17:12Z |
| R10 | tamper clone (`3182047` vs clone HEAD `f6cb8894…`), **0425224 bytes** | 0 | `bde40ccb…` (`tamper-head.json`) | 17:09–17:10Z |
| R11 | same tamper, **58eb04b6 (F5) bytes** | 2 | `f8300202…` (`tamper-f5.json`) | 17:11Z |
| R12 | `attest.py --root L --freeze 58eb04b6 --rev 58eb04b6 --json-out …/vacuous-c1-at-A4.json` | 0 | `eaf76a0f…` | 17:12Z |
| R13 | `registry.py` same pair → `vacuous-c2-at-A4.json` | 0 | `2550a1da…` | 17:12Z |
| R14 | `survivors-at-A4.json` (S1–S5 at A4, in-process, fixtures in scratch) | 0 | `318e229e…` | 17:13Z |
| R15 | `python3 -I -B tools/round-46/attest.py --selftest` (literal, as the claim writes it) | 2 | usage: `--root, --freeze, --rev required` | 17:09Z |

Reproduction: `probe_c1.py`, `probe_c2.py`, `probe_fix.py` are in the receipt dir and import
the lane's counters by path; every fixture repo is `git init`ed under `$HYAKU_SCRATCH` and
asserted to be its own toplevel before the first commit. No lane file was written outside this
seat directory; no git/jj mutation was run in the lane (the tamper clone is
`git clone --shared` into scratch, with its own identity).

## 7. Not run, and what I would not claim

- **Not run:** a wave-2 falsification of the landed `SKILL.md` block 23 against the real
  census (that is wave 2's job; I only attacked the predicate with constructed artefacts);
  `census.py` regeneration at A4 (I read the frozen `census.json`; 38 paths, all present);
  the registry 7-fixture battery's own fixture-level `v1_failing` (the receipt exposes only
  `v2_failing` for C2).
- **Not claimed:** that the nine forgeries are "the round-45 defect classes" — the claim does
  not say that, and §A3 shows three incompatible enumerations; that `v2_green == 0` is weak
  (it is the strongest clause in either instrument, and `P10` shows it is a real check); that
  the landed block 23 is forged (it is genuine and resolves; the defects are in the measure
  and in the freeze discipline).
- **Ceiling:** I did not test merge-shaped histories (R45-CL6) or `--json-out` targets inside
  the graded set beyond the one refusal above; both are covered by F5's selftest cases, which
  I ran but did not independently re-derive.

## 8. Hand-off to L1

1. **Do not paste the `freeze == rev` receipts as landing evidence.** `c1-at-F4.json` and
  `vacuous-c1-at-A4.json` are green because the freeze arm compared a tree with itself.
  Under the claims file's own derivation (`3182047`) both counters exit 2 at every rev from
  `50862e4a` on. If the round must land something this week, land *F1/F3/F4/F5* as the next
  round's instrument and record R46 as `instrument landed, claim not met` — the alternative is
  a green that the claim file's own words exclude.
2. **If block 23 is to keep its pin**, the pin's value must be the *freeze's* attest.py
  (`dd1e7df1…` at `3182047`) or the clause must say "at `--rev`" and the freeze must be
  derived — the two cannot both be optional.
3. **Registry rows for this seat's findings** (if the L1 wants them in block 23's successor):
  F1 → `R46-CL1` candidate "the freeze argument is not the freeze"; F3 → `R46-CL2`
  "citations outside the validated set are invisible"; F4 → `R46-CL3` "a ghost row outside the
  census is not a registered path"; F5 → `R46-CL4` "the battery denominator is a count, not a
  name set". Each has a receipt above and a one-line reproducer.
4. No installs were made (nothing needed; `python3`, `git` only). No tool was upgraded.
