# R46W1RegI — round 46 wave 1, tag `reg-i`: three registry rows

Seat `R46W1RegI`. Scope: the three claim-carrying instruments below, read **at the freeze**
(`git -C <lane> show 31820472784284727546808acc31b3ea1e73919b:<path>`), one ready-to-paste
house-format row each. The rows are in `rows.md` verbatim below; every command quoted in a
row was run — exit code, stdout sha256 and UTC time in `receipt.md`, raw stdout in `run/`.

**Deliverable: three rows produced and verified.** The lane moved underneath the seat while
it ran (`87578656` → `17a72375` → `781e19ae` → `04252247` → `1e32827b`, 16:55Z–17:01Z), so
every measurement below names the revision it was taken at. Two of the rows appear verbatim
in the registry landed at `781e19ae`; the third matches it except for one cell (erratum in
§5).

## 1. The three rows (also in `rows.md`, exactly three lines)

| `tools/round-41/indep-eval-v3.py` | probe — R41-C2 independent evaluator: transcribes the round-41 label precedence over envelope feature tuples and prints one (label, action) record per envelope, never reading the SKILL triage table, the interpreter or the generator | 0=every envelope in --envelopes was labelled (a per-envelope read error lands in the errors object, not in the exit) or the selftest passed; 1=a selftest case failed; 2=usage error only: no --envelopes, or a path that is not a directory, so there is no could-not-evaluate exit | python3 -I -B tools/round-41/indep-eval-v3.py --selftest — 46 cases, ok true, exit 0 on 2026-10-28 | plans/round-41-claims.md Label precedence steps it is transcribed from, its own bytes and ACTION_BY_LABEL pinned at the round-41 freeze | --out FILE only; stdout otherwise | kaidoku |
| `tools/round-42/sqfs-triage-v4.py` | probe — R42-C2 interpreter: labels each REA envelope with (label, action) by matching the SKILL craft-section SquashFS triage table v4, and validates that table alone under --table-only | 0=envelopes labelled, or the table validated by --table-only (15 rules from the lane SKILL.md, 2026-10-28), or the selftest passed; 1=a failed --selftest only; 2=table missing, refused by a v1/v2/v3 marker, or malformed, an envelope unreadable, or a usage error | python3 -I -B tools/round-42/sqfs-triage-v4.py --selftest — 123 cases, 123 pass, 0 fail, exit 0 on 2026-10-28 | SKILL.md rule block 21 v4 triage table, frozen at the round-42 freeze; tools/round-42/fixtures.json pins the envelope fixtures | none — stdout only, and the selftest writes its SKILL variants under a TMPDIR work dir | kaidoku |
| `tools/round-46/attest.py` | gate — R46-C1 freeze-integrity counter: scores SKILL rule block 23 against the frozen clauses and runs the nine-forgery discrimination battery, which must score every forgery red and the genuine block green | 0=met with failing empty; 1=not met, each false clause named in failing; 2=could-not-evaluate: unknown or non-ancestor revision, malformed claims file or craft heading, frozen_path_changed, a refused --json-out, an unusable scratch root, or an unhandled exception | python3 -I -B tools/round-46/attest.py --selftest --root . --freeze HEAD --rev HEAD — green, exit 0 on 2026-10-28; 15 cases at the 3182047 and 50862e4a bytes, 16 from the F3 repair at 65678df0 onward; --root/--freeze/--rev are required even for --selftest | plans/round-46-claims.md (frozen) plus the sha256 pin of its own bytes in SKILL.md rule block 23 | --json-out only, refused inside any graded or frozen surface and outside the lane root; selftest and battery fixture repos under HYAKU_SCRATCH or TMPDIR | kaidoku |

All three are census paths (`tools/round-46/census.json` at the freeze: 38 paths, none
`named_but_absent`). Scored by the frozen `registry.py` parser itself, with the rows pasted
under the house header between the two v2 markers: three rows parsed, `registered` contains
all three, `thin == []`, `absent_at_rev == []`, header equals the house schema, and each
verdict-map cell yields exactly `{0,1,2}` under the frozen `\b([012])\s*[=:]` regex. The only
failing clause in that fixture run was `unregistered: 35 of 38`, expected because the fixture
held only my three rows.

## 2. How each row's claims were verified (all run, none inferred)

- `indep-eval-v3.py`: `--selftest` exit 0, JSON `cases 46`, `ok true`, `failures []`, steps
  1–12 and all 13 labels covered. No args → exit 2; `--envelopes /nonexistent` → exit 2
  (both the 2 arm). `--envelopes <dir with one invalid JSON>` → **exit 0** with
  `envelope_count: 0` and an `errors` object — so the 2 arm is usage only and there is no
  could-not-evaluate exit (F5). Bytes unchanged `3182047..HEAD` (no commit touches
  `tools/round-41` in that range).
- `sqfs-triage-v4.py`: `--selftest` exit 0, `SELFTEST cases=123 pass=123 fail=0`;
  `--skill SKILL.md --table-only` against the lane's own `SKILL.md` exit 0,
  `rules: 15` — that confirms the 0 arm of the table-validation path. No args and
  `--table-only` without `--skill` both exit 2 (`--skill is required`). Bytes unchanged
  `3182047..HEAD`.
- `attest.py`: at the frozen bytes with the three path flags supplied → exit 0,
  `ATTEST_SELFTEST: cases=15 failures=0`; the same command **without** them → exit 2
  (F1/F6). At `65678df0` and later the count is 16 (the F3 repair added a
  `green-with-battery` case). The exit-2 arms were verified on the real lane by the freeze
  runs in §3.

## 3. Findings (each with the revision and UTC it was measured at)

**F1 — the pinned `attest.py` could not produce a verdict: `REF` undefined.**
At rev `87578656` (16:54:28Z), the bytes `SKILL.md` block 23 then pinned
(`sha256:eba59958…` = `attest.py` at `50862e4a`) crashed inside the battery:

```
python3 -I -B attest.py --root <LANE> --freeze 50862e4a… --rev 87578656… --json-out …
→ exit 2, {"reason": "unhandled NameError: name 'REF' is not defined"}
```

`REF` existed in neither byte set (both define `HARD_REF`/`LOOSE_REF`); `m_self_refs`
(`attest.py:322`) was the only user, and a direct call reproduced the NameError. Without the
battery the same run was exit 0, `met_target: true`, `failing: []` (16:54:48Z), so the defect
was isolated to one forgery. The 15-case selftest never ran the battery, so it could not see
it. **Fixed at `65678df0`** ("round-46 F3 … the battery's dead REF name"): at rev `17a72375`,
freeze `65678df0` → exit 0, `met_target: true`, `failed []`, battery
`forgeries_total 9 / v1_green 9 / v2_green 0 / genuine_green 1`, `rows 13`, `refs 9`, pin
matching (16:59:10Z). The repair added a sixteenth selftest case.

**F2 — the ticket's freeze (`3182047`) cannot score anything; every counter exits 2 there.**
`50862e4a` is inside `3182047..HEAD` and touches all three frozen round-46 files, and the
history arm sees it:

```
--freeze 3182047… --rev 87578656… → exit 2, reason frozen_path_changed
frozen_path_changed [tools/round-46/, tools/round-46/attest.py,
                     tools/round-46/gate.py, tools/round-46/registry.py]
```

Any commit in `FREEZE..REV` that touches the frozen directory makes the score inadmissible,
and this round repaired its instruments **three times after the first freeze**
(`50862e4a`, `65678df0`, `04252247`). Measured at 17:01Z with rev `1e32827b`: freeze
`50862e4a` → exit 2 `frozen_path_changed [tools/round-46/, tools/round-46/attest.py]`
(16:59:24Z); freeze `65678df0` → exit 2 `frozen_path_changed [tools/round-46/,
tools/round-46/registry.py]` (17:01:25Z). So the board's `<FREEZE>` must be the **latest**
commit that touched `tools/round-46/`, and it moves with every repair. This is a structural
property of a *directory* freeze of instruments that are still being debugged, not a clerical
slip: the freeze cannot be declared final before the instrument is proven, and proving it
requires running it, which is the only way to find the next repair.

**F3 — with `freeze == rev == 04252247` both counters are green (measured, 17:01:05Z).**
`attest.py` exit 0 `met_target: true`, `failing []`, battery `9/9/0/1`; `registry.py` exit 0
`met_target: true`, `failing []`, battery `7/7/0/1`, `registry_rows 38`, `unregistered []`,
`thin []`, `absent_at_rev []`, `frozen_path_changed []`. So both predicates are satisfiable
today — but only on a self-freeze (`REV == FREEZE`), which is what the frozen-path clause
reduces to once the instruments are still being edited. The L1 has to choose and state that
in the round report; the ticket's value (`3182047`) yields exit 2, which never counts toward
a target.

**F4 — `gate.dirty()` is defined and never called: the block-23 `dirty` arm is not wired.**
`tools/round-46/gate.py:132` defines `dirty(root, pathspecs)`; `freeze_state()` does not call
it, and neither counter does (`grep -n "dirty(" tools/round-46/*.py` returns only the
definition). Block 23's `R45-CL15` row maps to the arm token `dirty`, and the vocabulary
clause passes on the token alone. During this seat the worktree **was** dirty on a frozen
path (` M tools/round-46/attest.py`, worktree sha `a8e6e152…` vs committed `eba59958…`, seen
at 16:58Z) and no counter noticed. The hole that row claims to close is closed only on
paper.

**F5 — `indep-eval-v3.py` has no could-not-evaluate exit; the row says so.** A directory
containing one invalid JSON envelope → **exit 0**, `envelope_count: 0`,
`errors: {broken: "… Expecting property name …"}`. Exit 2 is argparse usage only; exit 1 is
a failed selftest only. A receipt consumer mapping 2 to "could not evaluate" will read an
all-errors run as success, so the row states the true map rather than the conventional one.

**F6 — the claims file's preflight quotes a command that exits 2 and a count that no byte
set prints.** `plans/round-46-claims.md:192-194`: "`attest.py --selftest` prints
`cases=15 failures=0` … `registry.py --selftest` prints `cases=11 failures=0`". Both commands
as written exit 2 — `error: the following arguments are required: --root, --freeze, --rev`,
because all three are `required=True` and argparse rejects before `if args.selftest`. With
the flags supplied, `attest.py` prints 15 (true) but `registry.py` prints
**`cases=12 failures=0`** at `3182047`, at `50862e4a` and at HEAD. No clause scores either
number, so no verdict turns on it — but the preflight paragraph is what licenses the freeze
and two of its three values are wrong.

**F7 — the C2 v1 profile was red on the landed artefact: `battery v1_green 0 != 7`.**
Measured at rev `781e19ae` (16:59:38Z), freeze `65678df0`:
`registry.py` exit 1, `met_target false`, `failing ['battery v1_green 0 != 7']`,
`unregistered []`, `thin []`, `absent_at_rev []` — i.e. the v2 clauses all passed and only
the discrimination clause failed. Cause, measured directly with the module: v1's
fence-blind whole-file parse (`rows_anywhere`) scored the **genuine** 38-row artefact red
first (`unregistered: 32 of 38`, `rows 45`), because `PATHCELL` only sees cell 0 when it is
exactly a backticked tool path and v1 also carried the v2-only presence/shape expectations
into the port — so it accepted none of the seven forgeries and the "v1 accepts every
forgery" premise held for zero of them. **Fixed at `04252247`** ("the v1 registry profile
applies its own loose checks … so the port is the round-45 clause set it claims to be"):
the F3 run above then reads `v1_green 7`, `v2_green 0`.

## 4. Limits of this seat (not run, not claimed)

- No row was pasted into the lane `SKILL.md` (read-only for this seat); the registry parser
  was exercised against the pasted text in memory, and separately against the real section at
  `HEAD` for the `registered`/`thin`/`absent_at_rev` values in F3.
- The C1 and C2 batteries are reported from their own receipts; I did not re-derive the nine
  or seven mutations' expected classes beyond the per-fixture `v1_exit`/`v2_exit` fields the
  counter prints, and I did not inspect the round-45 fidelity receipts.
- `R45-CL20`/`R45-CL22` arms were read in `gate.py` source at the freeze, not re-fired.
- Whether the v4 table's 15 rules still match the round-42 freeze bytes was not checked.
- The lane advanced after 17:01Z; if a later commit touches `tools/round-46/`, F3's freeze
  (`04252247`) stops being admissible and the value in F3 must be re-measured.

## 5. Row erratum for the landed registry

Rows 1 and 2 at `781e19ae` are byte-identical to mine. Row 3 differs in **cell 4 only**: the
landed text says "15 cases, 0 failures at the freeze", which is true of the `3182047` and
`50862e4a` bytes but not of the bytes the round now pins (`65678df0` onward report
`cases=16` after the F3 repair added `green-with-battery`). My `rows.md` cell 4 now carries
both counts and the revision each belongs to; pasting that line over the landed one is the
whole erratum. Nothing else in the three rows changed.

## 6. Risks the L1 should weigh

- Landing or re-pinning block 23 at the `eba59958…` bytes while the board's freeze is
  `3182047` guarantees exit 2 twice over (frozen_path_changed, then the F1 NameError) — F1
  is fixed only from `65678df0`.
- The freeze value is the round's exposed flank (F2): three repairs inside one wave each
  invalidated it. The report should name `04252247` (or the last repair) as the freeze, not
  the ticket's `3182047`, and say plainly that `REV == FREEZE` was the measured pair.
- The three rows are otherwise safe to paste as-is: they record each tool's actual exit
  paths, including the two awkward ones (no could-not-evaluate exit for `indep-eval-v3.py`;
  a selftest that requires the three path flags for `attest.py`).
