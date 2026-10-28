# C1Tokens — R47-C1 clause 5: verified, attacked, and the block-24 rows drafted

Seat `C1Tokens`, round 47 wave 1 (verification / drafting / attack, before landing).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `5017e1f7299c3a812e87e7950148f54313dd279e`; base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`.
Scope: **R47-C1 clause 5 only** — the v3-arm cell is an equality, not a containment.
Everything measured with the frozen counter, nothing in the lane tree edited.

## 1. The clause, quoted from both frozen sources

Claims — `plans/round-47-claims.md:76-77` (`plans/round-47-claims.md` sha256
`c8615eb811f598a35cad514523225e320185ec3c6481035fc95f844071e41f67`, 190 lines):

> 5. Every v3-arm cell, stripped of backticks and spaces, is one of `symbol`, `once`, `digest`,
>    `order` — an equality, not a containment.

Code — `tools/round-47/exact.py:235-243` (`tools/round-47/exact.py` sha256
`dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`, 561 lines):

```python
    # clause 5: arm token, exactly ------------------------------------------------
    arm = [r[2].strip("` ") if len(r) > 2 else "" for r in rows]
    receipt["arm_tokens"] = arm
    if hard:
        if any(a not in VOCAB for a in arm):
            failing.append(f"arm cells not exact vocabulary tokens: {arm}")
    else:
        if any(not any(t in a.lower() for t in VOCAB) for a in arm):
            failing.append("arm cells outside the vocabulary")
```

`VOCAB = ("symbol", "once", "digest", "order")` at `tools/round-47/exact.py:35`;
`hard = profile == "v3"` at `tools/round-47/exact.py:167`; the cell is column index 2, and
`_cells` (`tools/round-47/exact.py:129-130`) has already run `c.strip()` on it, so the
`.strip("` ")` in clause 5 only removes leftover backticks.

The v2 hole this closes is the round-46 substring test, still present at
`tools/round-46/attest.py:219`:

```python
                       and not any(t in r[arm_col].lower() for t in ARMS)]
```

Measured: on the same block, `order-ish` in every arm cell scores **v2 exit 0 / v3 exit 1**
(battery fixture `substring-arm`, `receipt-cli-full.json`). The containment hole is closed at
the level clause 5 claims to close.

## 2. Run ledger (exact command, exit, UTC, stdout sha256)

Root for the lane runs is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; every fixture run
is `python3 -I -B tools/round-47/exact.py --root <FIXTURE> --freeze <FIXTURE-REV> --rev
<FIXTURE-REV> --json-out <FIXTURE>/receipt.json` with `HYAKU_SCRATCH` and `TMPDIR` set to the
seat scratch. Fixtures are one-commit repos created under that scratch with
`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before the commit.

| run | fixture rev | exit | UTC | stdout sha256 | `failing` |
| --- | --- | --- | --- | --- | --- |
| freeze `5017e1f…` (the mandated command) | `5017e1f7299c…` | **1** | 2026-10-28T17:51:36Z | `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba` | `["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]` |
| A: clause-5-only block | `7f296d32b9ab…` | **1** | 2026-10-28T17:51:12Z | `e9720b5476118ec4e7ccf909164b9b978e6a07dc7d944af8ff79cf68d699d556` | clause 6 ×2, clause 8 pin (see §3) |
| B: full block, battery | `f629c3415086…` | **0** | 2026-10-28T17:51:13Z | `1111dedc3e1a6116692d7c25b6c86864bd8d1442421052c1f315aa7440277c9d` | `[]` |
| C: all four arms `order` (forgery) | `f0de6ace88f0…` | **0** | 2026-10-28T17:51:13Z | `00e3f77e10e0cf56b0794a97a1f6a9221c3e140dda08e4f6a188191b0ac735a5` | `[]` |
| D: the bytes published in `rows.md` | `ea3cf1f03bd6…` | **0** | 2026-10-28T17:53:06Z | `31dba08513985416ab5b7c46ba77a4699db38c768d2238c49b80beb4a9b4bd32` | `[]` |
| E: **lane tip** `1e2c3102`, freeze `5017e1f` (this prompt's freeze) | `1e2c3102952d…` | **2** | 2026-10-28T17:55:37Z | `706cf11c4b17acb95c78afc1ac690addc3de81a0d479685ba4f11cd66625790f` | `reason: frozen_path_changed`, `['plans/round-47-claims.md', 'tools/round-47/', 'tools/round-47/record.py']` |
| F: lane tip `1e2c3102`, freeze `1e2c3102` (the landed block) | `1e2c3102952d…` | **0** | 2026-10-28T17:55:37Z | `98ef390e1c1a3eaa1e0d2b9f3a9c635a4870c257b2cdebad4c4a87497616ea6d` | `[]`, `refs 8`, battery 4/4/0/1/0 |
| G: **landed** block, all four arm cells `order` | `b1af38d3b175…` | **0** | 2026-10-28T17:55:51Z | `3b3b8bdb0e23278436aa47bf18835f70e1a0765c0e99b1def595920a4e4d0092` | `[]`, battery 4/4/0/1/0 |
| H: **landed** block, arms CL2↔CL6 swapped | `2f6a8ad38ddc…` | **0** | 2026-10-28T17:55:51Z | `a2f8f042bcde901f177bdf315f44b9dbbc72324579a93a78133835955882c0f3` | `[]`, battery 4/4/0/1/0 |
| I: tip `a631bba0` (two commits later), freeze `5017e1f` | `a631bba01633…` | **2** | 2026-10-28T17:57:18Z | `37c625849576a5b2b88f043580ff7fa4cfeb09b8ceece4ca38081fbf2143c280` | `reason: frozen_path_changed`, same three paths |
| J: tip `a631bba0`, freeze `a631bba0` | `a631bba01633…` | **0** | 2026-10-28T17:57:18Z | `3908cc6e50a36ad74c57ce4cd3e3c6e1cadb4eea5fe0d15628e0622483901edd` | `[]`, `refs 8`, battery 4/4/0/1/0 |

Freeze receipt (`receipt.json`, byte-identical to its stdout): `rule_blocks 23`,
`marker_occurrences 0`, `block_present 0`, `met_target false`. So the claims' "Before" cell is
reproduced exactly, and the counter short-circuits at the marker clause — nothing later is
evaluated at the freeze.

Run B (`receipt-cli-full.json`) reports `refs 7`, `rows 4`, `header_ok true`,
`block_is_last true`, `gate_order_literal 1`, `gate_order_reversed 0`,
`mutations_sha256 == mutations_sha256_expected`, `interpreter_sha256 ==
interpreter_sha256_expected`, and `battery = {forgeries_total 4, v2_green 4, v3_green 0,
genuine_green 1, crash 0}`. Under `--profile v2` the same block is also exit 0 — expected,
since v2 is strictly weaker.

## 3. The failing list shrinking, and exactly what stays red

| block in the fixture | `failing` | clause | in my scope? |
| --- | --- | --- | --- |
| none (freeze) | `marker_occurrences 0 != 1`, `marker_block_count 0 != 1` | 1 | no |
| A: clause-5-only (marker, `24. `, last block, exact header, 4×4 rows, exits `1`, exact arms, and the row cells already carry the round-46 citations) | `mutations_sha256 does not match the counter's own mutation list` | 6 | no |
| | `mutation names not stated in the block: ['substring-arm', 'duplicate-routed-id', 'stale-mutations-digest', 'flag-order-drift']` | 6 | no |
| | `interpreter sha256 pin does not match the bytes at rev` | 8 (pin half) | no |
| B / D: full block | `[]` | — | — |

Two ordering facts worth stating plainly, because they are what make clause 5 cheap to land
and easy to mis-land:

1. **Clause 5 is satisfied by the arm cells alone.** In run A the counter already reports
   `arm_tokens ['symbol','once','digest','order']` with `refs 4` — clauses 2, 3, 4, 5, 7 and
   clause 8's `refs >= 3` and `MUST_CITE` arms are all green from the four rows plus their
   `corpus/lessons/round-46.md` selectors, before any pin exists. Only the two pins are left.
2. Nothing in run A's remainder touches clause 5's code path. The three red strings are
   `tools/round-47/exact.py:250-251` (digest equality), `:252-255` (mutation names) and
   `:277-286` (interpreter pin). All three are satisfied by the prose in the block published
   in `rows.md`, and run D confirms it on exactly those bytes.

## 4. Attack matrix — clause 5 alone

Each variant rewrites the four arm cells of the verified block and re-scores it in a fresh
one-commit fixture. `v3`/`v2` are counter exit codes (`0` met, `1` not met). Matrix in
`attack-matrix.json` and `attack-matrix-vacuity.json`.

| arm cells | v3 | v2 | reads as |
| --- | --- | --- | --- |
| `symbol`, `once`, `digest`, `order` (control) | 0 | 0 | genuine |
| `` `symbol` ``, `` `once` ``, `` `digest` ``, `` `order` `` | 0 | 0 | passes — the claims authorise the backticks |
| `  symbol  `, `once `, ` digest`, `order  ` | 0 | 0 | passes — spaces are in the strip set |
| `symbol\t`, … | 0 | 0 | passes — `_cells` already stripped the tab |
| `symbol-ish`, `once-ish`, `digest-ish`, `order-ish` | **1** | 0 | hole closed (the round-46 shape) |
| `symbolmap`, `onceover`, `digested`, `orderly` | **1** | 0 | hole closed (prefix/suffix containment) |
| `the symbol arm`, `exactly once`, `a digest pin`, `flag order` | **1** | 0 | hole closed (prose-cell containment) |
| `Symbol`, `Once`, `Digest`, `Order` | **1** | 0 | stricter than v2 — v3 is case-exact |
| `""`, `once`, `digest`, `order` | **1** | 1 | both red |
| `symbol\u200b`, … (zero width) | **1** | 0 | red under v3 |
| **`order`, `order`, `order`, `order`** | **0** | 0 | **passes, including the 4/4/0/1/0 battery** |
| **`order`, `digest`, `once`, `symbol`** (permuted) | **0** | 0 | **passes** |
| **`symbol`, `once`, `digest`, `symbol`** (one id wrong, one token twice) | **0** | 0 | **passes** |

## 5. Findings

### F1 — HIGH — clause 5 binds the token *set per cell*, not the arm↔defect pairing or the multiset

**Exact command** (fixture C, arms all `order`):

```sh
python3 -I -B tools/round-47/exact.py --root /fast/scratch/hyaku/kaidoku-r47/C1Tokens/fx-allorder-BvQP8m \
  --freeze f0de6ace88f00469ffc56b6e1f04bb2b6b0123f6 --rev f0de6ace88f00469ffc56b6e1f04bb2b6b0123f6 \
  --json-out /fast/scratch/hyaku/kaidoku-r47/C1Tokens/fx-allorder-BvQP8m/receipt.json
```

**Differing value**: exit **0**, `failing []`, `arm_tokens ["order","order","order","order"]`,
`battery {forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}`
(`receipt-cli-allorder.json`, stdout sha256 `00e3f77e…`). A table whose every row says the
flag-order arm closed a substring hole scores met, battery and all.

**Why it is not a code-vs-claim divergence.** The claims sentence is "every row's v3-arm cell
**is exactly one token of** `symbol`, `once`, `digest`, `order`" — satisfied by four `order`
cells. The code implements that sentence faithfully. The defect is in the claim's strength:
nothing states, and nothing measures, `sorted(arm) == sorted(VOCAB)` (the multiset) or
`arm[i] == ARM_OF[trigger_i]` (the pairing). The claims' own kill rule —
"a block with `blobberish` in a v3-arm cell fails clause 5" — is a one-cell test and cannot
catch it, and the counter's selftest has `red-arm-substring` but no multiset case (16 cases,
`selftest.json`, `EXACT_SELFTEST: cases=16 failures=0`).

**Fixture path** that shows it: `fx-allorder-BvQP8m`, rev
`f0de6ace88f00469ffc56b6e1f04bb2b6b0123f6`; rebuildable from
`fixtures/mkb.py allorder` + `fixtures/cli.sh` (the `allorder` variant is the third case in
`mkb.py`, and `drive.py` carries the same three variants under `attack:` labels).

**Measured again on the block that actually landed** (see §7): mutating the landed block's
four arm cells to `order` gives exit **0** (`receipt-landed-allorder.json`, stdout sha256
`3b3b8bdb…`), and swapping CL2's and CL6's arms — `order`, `once`, `digest`, `symbol`, a
matrix that now states the *opposite* of what the rows describe — gives exit **0**
(`receipt-landed-swapped.json`, stdout sha256 `a2f8f042…`). Both keep the full battery at
4/4/0/1/0. The gap is therefore a property of the instrument that shipped, not of this
seat's draft.

**Not fixed here** — the claims file and `tools/round-47/` are byte-frozen and this seat does
not edit them. A later round's repair is one line of code plus one claim sentence:
`if sorted(arm) != sorted(VOCAB): failing.append(...)`, and an id→arm map beside `ROUTED`.

### F2 — MEDIUM — the landing trap: the block cannot name the file clause 7 is about

Clause 7 is a statement about `tools/round-46/gate.py`, but `ALLOW`
(`tools/round-47/exact.py:36`) is `corpus/lessons/`, `corpus/knowledge/`, `plans/`,
`tools/round-47/` **only**. One path token naming `tools/round-46/gate.py` inside block 24
fails clause 8 with `tools/round-46/gate.py: outside the validated path set`
(`tools/round-47/exact.py:144-147`). Block 23 — the block 24 continues — cites
`tools/round-46/attest.py` (`SKILL.md:612`), so the natural continuation is the failing one.

The published draft therefore says *"the history arm's flag order"* in prose and never names
the gate file; the counter reads `GATE46` itself (`tools/round-47/exact.py:256`, `:260-264`).
Verified: run D scores `[]` with that wording. Reproduced in the selftest as well
(`red-ref-outside-allowlist`), so the behaviour is intended — the consequence for the L1 is
just that the block must **not** cite the instrument it binds.

### F3 — LOW — `--selftest` is unreachable without the three required arguments

`python3 -I -B tools/round-47/exact.py --selftest` exits **2** with
`exact.py: error: the following arguments are required: --root, --freeze, --rev`
(`selftest.json`, first run, exit 2). The selftest itself is green — 16 cases, 0 failures,
exit 0 — only when invoked as
`… --root <any> --freeze <any> --rev <any> --selftest`, because `--selftest` is dispatched
inside `main()` after `parse_args`. This matches the documented round-46 spelling for
`attest.py` (`SKILL.md:1743` records that `--root/--freeze/--rev` are required even there),
so it is a family convention, not a new defect — but the instrument row the L1 registers for
`tools/round-47/exact.py` must carry the argument-bearing spelling, or the next reader records
a false "selftest broken".

### F4 — INFO — what the strip set does and does not tolerate

`strip("` ")` is a character-set strip on both ends, applied after `_cells` has already
stripped whitespace. Measured consequences: backticked and space-padded cells pass (authorised
by the claims wording), tabs pass (stripped earlier, not by clause 5), and any other
decoration fails — a zero-width space after the token is red. No over-accept was found in the
strip path beyond decoration: the only strings that survive are the four tokens with
backticks/spaces removed. The looseness in this clause is F1, not F4.

## 6. What this seat drafted (`rows.md`)

`rows.md` in this directory holds the ready-to-paste block and the values it must carry:

| item | value |
| --- | --- |
| v3-arm cells (clause 5's four cells) | R46-CL2 `symbol`, R46-CL3 `once`, R46-CL4 `digest`, R46-CL6 `order` |
| block sha256 | `a57ce1214f830ca62fe7ef52e3b4d9403814a6e616ad5e9e39b9408f22e0694b` (1916 bytes: the fenced text + one newline) |
| `mutations_sha256` | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` |
| `interpreter_sha256` | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` |
| insertion point | after block 23 (`SKILL.md:612-631`), before `## Config custody for live-probe rounds (SOP)` (`SKILL.md:632`) |
| citations used, each with a selector | `corpus/lessons/round-46.md:51-69`, `:57-59`, `:60-62`, `:63-64`, `:65-69`; `plans/round-47-claims.md:76-77`; `tools/round-47/exact.py` (pin only, exempt at `:149-150`) |

`corpus/lessons/round-46.md` sha256 `0da8a24c02f828495035ddf7e3481ef1d4c39485a422be9d9818f27fa6ff0bdc`
(102 lines) at the freeze, so every selector above resolves inside `1..102`. Run D is the
counter executed on exactly the fenced bytes published in `rows.md` — not on a paraphrase.

## 7. The tip moved while this seat measured (the block has landed)

The lane was not static: between my first reading and my last run, the L1 landed the round and
amended the freeze repeatedly (amendments A1–A5 are recorded in the claims file). The tip advanced twice **during this section's own measurement**
(`1e2c3102` → `07d2894e` → `a631bba0`), which is the operational fact F5 records: a freeze
pinned to `5017e1f` can never see the landed state as a pass. `git log` at measurement time:

| commit | subject |
| --- | --- |
| `9018c53b` | round-47: freeze amendment A1 — drop the unreachable window-pair clause |
| `e856beb5` | round-47: land craft block 24, the record corrections, the current axis heads and S143 |
| `62e33f7d` | round-47: A2 — … block 24 arm cells carry only the token |
| `2e4ae434` | round-47: A3 — a seats/window correction for a round older than the window stays valid evidence |
| `1e2c3102` | round-47: A4 — the historical-correction selftest fixture gets its round-3 dispatch |
| `07d2894e` | round-47: A5 — the ghost-atom forgery lands inside the corrections section |
| `a631bba0` | round-47: A5 in the record, the LOG and the lesson; both claims' A5 receipts |

Three consequences for the record, all measured:

1. **At the prompt's freeze the counter now exits 2, not 1.** `--freeze 5017e1f… --rev
   1e2c3102…` returns `reason: frozen_path_changed` with
   `['plans/round-47-claims.md', 'tools/round-47/', 'tools/round-47/record.py']`
   (`tip-freeze-5017e1f.json`, stdout sha256 `706cf11c…`; re-measured two commits later at
   `a631bba0`, same verdict, sha256 `37c62584…` in `tip-a631bba-at-promptfreeze.json`).
   The claims file's own wording —
   "a change makes both counters exit 2 `frozen_path_changed`" — is what fires. A 2 is not a
   pass, so **the round cannot be scored at the tip against `5017e1f`**; the freeze series must
   end at the last commit that touches either frozen path. The claims file declares a
   two-commit series (`5017e1f` then A1), but A2/A3/A4 also edit `plans/round-47-claims.md`,
   so a third endpoint is needed or R47-C1 scores 2 no matter how green the block is.
2. **At a self-consistent freeze the landed block is green.** `--freeze 1e2c3102 --rev
   1e2c3102` exits **0**, `failing []`, `refs 8`, `arm_tokens ['symbol','once','digest',
   'order']`, `refs 8`, battery 4/4/0/1/0 (`tip-freeze-1e2c310.json`, stdout sha256
   `98ef390e…`; at `a631bba0` the same block still exits 0 with the same battery —
   `tip-a631bba-at-self.json`, sha256 `3908cc6e…`). The
   landed arm cells are the same four tokens in the same id order this seat drafted, so the
   arm-cell table in §6 agrees with what landed cell for cell; the landed cells carry
   backticks, which clause 5 strips. The landed block's prose and `Refs` line are the L1's own
   wording and differ from this seat's draft — only the four clause-5 cells are identical.
3. **The landed block is red-capable only one cell at a time** (F1): runs G and H above.

`tools/round-47/exact.py` itself is byte-unchanged across all of this —
`dcef54f1…` at `5017e1f`, at `e856beb5` and at `1e2c3102` — so every measurement in §2–§5 was
taken against the same counter bytes that are frozen today.

## Evidence index

| file in this directory | what it is |
| --- | --- |
| `receipt.json` | the mandated freeze run, exit 1, stdout sha256 `88fafc60…` |
| `receipt-cli-min.json` | run A, clause-5-only block, exit 1 |
| `receipt-cli-full.json` | run B, full block + battery, exit 0 |
| `receipt-cli-allorder.json` | run C, F1 forgery, exit 0 |
| `receipt-cli-rows.json` | run D, the published bytes, exit 0 |
| `attack-matrix.json` | 12 arm-cell variants, v3 and v2 exits with failing lists |
| `attack-matrix-vacuity.json` | the three multiset/pairing variants with the full battery |
| `selftest.json` | `--selftest` without args (exit 2) and with args (16 cases, 0 failures) |
| `tip-freeze-5017e1f.json` | run E: tip `1e2c3102` against the prompt's freeze — exit 2, `frozen_path_changed` |
| `tip-a631bba-at-promptfreeze.json` | run I: the same at tip `a631bba0` — exit 2, same three paths |
| `tip-a631bba-at-self.json` | run J: the landed block at tip `a631bba0`, self-freeze — exit 0 |
| `tip-freeze-1e2c310.json` | run F: the landed block at a self-consistent freeze — exit 0 |
| `receipt-landed-allorder.json` | run G: the landed block with four `order` arms — exit 0 |
| `receipt-landed-swapped.json` | run H: the landed block with CL2/CL6 arms swapped — exit 0 |
| `fixtures/` | `drive.py`, `mkb.py`, `cli.sh`, `verify_rows.sh`, `gen_rows.py` — rebuild every fixture above |

The lane worktree also carried other seats' uncommitted modifications while this seat read it
(`SCORECARD.md`, `corpus/SOURCES.md`, four round-45/round-46 wave artefacts). This seat wrote
none of them: its only writes are `SKILL.md`-free, under
`.ufo/waves/round-47/w1/C1Tokens/` plus the report file `.ufo/waves/round-47/w1/C1Tokens.md`,
and no tracked lane file was staged, committed or edited.

Nothing under `/tmp` is cited: every fixture and receipt lived under
`/fast/scratch/hyaku/kaidoku-r47/C1Tokens`, which was removed after these files were copied
here. No `pacman` transaction, no install, no `uv`/`npx` tool was used.

## Risks for the landing

1. **The block lands green while being semantically wrong** (F1). Landing the drafted block is
   correct; treating "clause 5" as "the matrix binds each hole to its arm" is not. The L1's
   record should say what the instrument measures.
2. **A block that cites `tools/round-46/gate.py` is red** (F2). If the L1 edits my draft to add
   that citation, the counter goes to exit 1 on clause 8 and the failure looks like a pin
   problem, not a citation problem.
3. The four arm cells are correct only in the order shown; any permutation still scores 0
   (measured on the landed block, runs G and H), so a red arm cell cannot be used as the signal
   that the pairing is wrong.
4. **Freeze drift is the round's live scoring risk.** At the tip, the prompt's freeze yields
   exit 2 `frozen_path_changed` (run E). The measured revision, the freeze the report cites and
   the bytes in `plans/round-47-claims.md` must all name the same commit, or R47-C1 is a 2 and
   not a met.
