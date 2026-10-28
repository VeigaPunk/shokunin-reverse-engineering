# C1Struct — R47-C1 clauses 1–3: verified, falsified where falsifiable, and drafted

Seat `C1Struct`, leaf. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `5017e1f7299c3a812e87e7950148f54313dd279e`, base
`13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`. Nothing in the lane tree was written: every
fixture is a one-commit repo under `$HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/C1Struct`,
removed before yielding; the reproducible artifacts (drivers + the exact `SKILL.md` inputs)
are archived here.

Scope: clauses 1, 2, 3 of `plans/round-47-claims.md` R47-C1. Adjacent clause-8 behaviour is
reported only where it constrains or contradicts the landing of these three.

## 0. Verdict

| clause | predicate (claims `:70-73`) | at freeze | candidate A | candidate B | kill probes |
|---|---|---|---|---|---|
| 1 | `marker_occurrences == 1`, `block_present == 1`, marked block is the last craft block, title starts `24. ` | **red** (`0`, `0`, 23 blocks) | green | green | 4/4 red as designed |
| 2 | header cells exactly `trigger / v2 hole / v3 arm / exit` | not reached | green | green | red on a 5th cell |
| 3 | `rows == 4`, 4 cells each, exit ∈ `{0,1,2}` | not reached | green | green | red on a pipe in a cell, a second table, exit `3` |
| — | whole counter | exit 1, `failing` = 2 strings | exit 1, `failing` = 8 strings (clauses 4,5,6,8 only) | **exit 0**, battery 4/4/0/1/0 | — |
| — | landed block in the real repo, rev `31b092d1` | — | — | — | **exit 0**, `failing []`, `rule_blocks 24` (§11) — but only under freeze `f54b3b6d`; the original freeze exits 2 `frozen_path_changed` (§12) |

Clauses 1–3 are computable, non-vacuous on this surface, and satisfiable together with
clauses 4–9: candidate B is a measured `failing == []`. What they do **not** bind is the
survival of the other 23 craft blocks (§5 F1) — the one finding L1 must act on outside the
frozen bytes.

## 1. The rule, quoted

`plans/round-47-claims.md:70-73` (R47-C1 predicate):

> 1. `marker_occurrences == 1`; `block_present == 1`; the marked block is the last craft block
>    and its title starts with `24. `.
> 2. Header cells equal `["trigger", "v2 hole", "v3 arm", "exit"]` exactly.
> 3. `rows == 4`; every row four cells; every exit cell in `{0,1,2}`.

`tools/round-47/exact.py` (frozen bytes, sha256 `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`):

```python
# :172-173  the marker is counted over the whole file; the block list is the craft section's
    occurrences = skill.count(MARKER)
    marked = [b for b in blocks if MARKER in b]
# :191-197
    receipt.update({"block_is_last": blocks[-1] is block,
                    "block_title": block.split("**", 1)[0][:24],
                    "header": header, "rows": len(rows)})
    if hard and not receipt["block_is_last"]:
        failing.append("marker block is not the last craft block")
    if hard and not block.startswith("24. "):
        failing.append("marker block title does not start with '24. '")
# :198-215
        header_ok = header == HEADER
    ...
        if len(rows) != 4:
            failing.append(f"rows {len(rows)} != 4")
        if any(len(r) != 4 for r in rows):
            failing.append("a row does not have exactly 4 cells")
    ...
    bad_exit = [r for r in rows if len(r) < 4 or r[3].strip("` ") not in {"0", "1", "2"}]
    if bad_exit:
        failing.append(f"exit cells outside {{0,1,2}}: {len(bad_exit)}")
```

`blocks_of` is `re.split(r"(?m)^- \*\*", craft_section(skill))[1:]` and `craft_section`
splits on the literal `"## Queue-drain craft "` (note the trailing space) and stops at the
next `"\n## "` (`tools/round-47/exact.py:101-110`). `table()` reads the first line starting
with `|` as the header and every later such line as a row (`:113-136`).

## 2. Freeze receipt — clause 1 before the landing

Command (**exact**, cwd = the lane root, `HYAKU_SCRATCH` set):

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/C1Struct python3 -I -B tools/round-47/exact.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze 5017e1f7299c3a812e87e7950148f54313dd279e \
  --rev 5017e1f7299c3a812e87e7950148f54313dd279e \
  --json-out .ufo/waves/round-47/w1/C1Struct/receipt.json
```

`utc=2026-10-28T17:52:51Z`, **exit 1**, stdout 532 bytes, stdout sha256
`88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba`
(`receipts/exact-freeze.log`, `receipt.json` sha256 identical — the emitted bytes are the
written bytes).

| field | value |
|---|---|
| `marker_occurrences` | `0` |
| `block_present` | `0` |
| `rule_blocks` | `23` |
| `failing` | `["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]` |
| `frozen_derived` | `["tools/round-47/", "plans/round-47-claims.md"]` |
| `frozen_path_changed` | `[]`; `touched 0`; `restored []` |
| `battery` | `{"skipped": "artefact fails a structural clause first"}` |

This reproduces the claims' `Before` cell (`plans/round-47-claims.md:99-103`: "exits 1 with
`block_present 0`, `rule_blocks 23`, `marker_occurrences 0`", and `ctl-c1-2` cannot build a
battery because marker blocks are 0). Class 1 is therefore the only live clause at the
freeze, exactly as the claims state.

## 3. Candidate A — clauses 1–3 satisfied, everything else left red

`candidates/block24-candidate-a.md` (`sha256 3758161eb3df28d0451987271e73ac6593c3f0785cd3149c43f3a55f99f562cf`):
one bullet titled `24. `, the marker once, the exact four-cell header, four rows of four
cells, exits `1 / 1 / 2 / 1` — and deliberately no routed ids, no arm vocabulary, no pins,
no refs. Inserted as the last craft block of the freeze `SKILL.md` and scored v3 in a
one-commit fixture (`receipts/drive.out`, `candidate-A-clauses-1-3-only`):

```
exit 1   rule_blocks 24   marker_occurrences 1   block_present 1
block_is_last True        block_title "24. An exactness matrix "   rows 4
header ["trigger","v2 hole","v3 arm","exit"]
failing:
  rows naming != 1 routed id: [0, 1, 2, 3]                                   -> clause 4
  routed cardinality {} != each of ['R46-CL2','R46-CL3','R46-CL4','R46-CL6'] -> clause 4
  arm cells not exact vocabulary tokens: ['arm one',…,'arm four']            -> clause 5
  mutations_sha256 does not match the counter's own mutation list            -> clause 6
  mutation names not stated in the block: [all four]                         -> clause 6
  refs 0 < 3                                                                 -> clause 8
  does not cite corpus/lessons/round-46.md                                   -> clause 8
  interpreter sha256 pin does not match the bytes at rev                     -> clause 8
```

Clauses 1, 2, 3 all go green and **no 1–3 string remains in `failing`**. The red list is
exactly clauses 4, 5, 6 and 8. Clause 7 stays green because the frozen
`tools/round-46/gate.py` already carries the correct pair once and the reversed pair zero
times (`grep -c` = 1 and 0 at the freeze); clause 9 is not reached — the battery is skipped
when a structural clause is red, and in fixture scoring it is passed `battery=None`.

## 4. Candidate B — the landing form, measured green

`rows.md` carries the paste-ready block. `candidates/block24-candidate-b.md`
(`sha256 b44ef164766ead9817b9ea57e902ec645bd6a9dbb9f2f4ecf72c3b8cc7c1a152`) inserted into
the freeze `SKILL.md` (`candidates/SKILL-with-block24-candidate-b.md`,
`sha256 2819c0e8ad1f491bc6feb22d4c39ef3171683a31a7bb5a87d5cb9d3bcd7a12b9`, 1748 lines) scores
(`receipts/drive.out`, `candidate-B-full`):

```
exit 0   rule_blocks 24   marker_occurrences 1   block_present 1   block_is_last True
battery: forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0, genuine_exit 0
fixtures: substring-arm v2 0 / v3 1; duplicate-routed-id 0 / 1;
          stale-mutations-digest 0 / 1; flag-order-drift 0 / 1
```

Full predicate, clauses 1–9, `failing == []` — so the three clauses I own do not fight the
six I do not: the 4-cell header and the four rows coexist with exact arm tokens, one routed
id per trigger cell, the digest pin, the flag-order arm and six resolving citations. The
pins in the block are the ones measured here, not transcribed:

| pin | value | source |
|---|---|---|
| `interpreter_sha256` | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | `git show 5017e1f7:tools/round-47/exact.py \| sha256sum` |
| `mutations_sha256` | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` | `printf 'substring-arm\nduplicate-routed-id\nstale-mutations-digest\nflag-order-drift' \| sha256sum` (no trailing newline) |

## 5. Findings — where the frozen clauses are loose

Each finding gives the exact command, the differing value and the fixture that shows it.
Fixtures are rebuilt byte-identically by the archived driver named in the row (scratch is
`$HYAKU_SCRATCH`; one-commit repo; `_repo` asserts `rev-parse --show-toplevel == dir` before
committing, `tools/round-47/exact.py:301-319`, the toplevel assertion at `:306-309`).

| id | clause | finding | measured value | fixture / repro |
|---|---|---|---|---|
| **F1** | 1 | **The counter cannot see the other 23 craft blocks.** A craft section reduced to block 24 alone scores met. `rule_blocks` is reported but no clause reads it, so "the marked block is the last craft block" is satisfied by a one-block section. | `exit 0`, `rule_blocks 1`, `failing []`; with one surviving decoy block `exit 0`, `rule_blocks 2` | `tools/drive4.py` cases `craft-section-stripped-to-block24`, `craft-section-stripped-then-two-blocks`; input bytes `candidates/SKILL-craft-stripped-to-block24.md` (`sha256 28269e21ef68c750458d4194b6863e88e4919c72d62b2a261e0ef2014bf4ea83`) |
| **F2** | 8 (adjacent) | `refs >= 3` counts the bare interpreter path, which is exempt from the selector rule, so **two** line-selected citations pass although the claims demand "at least three citations carry a line selector". | 2 selected refs + bare `tools/round-47/exact.py` → `exit 0`, `refs 3`; the same block without the bare path → `exit 1`, `refs 2 < 3` | `tools/drive5.py`; `receipts/refs-count.json` |
| **F3** | 8 (adjacent) | The allowlist is applied to **every** path token in the block, not to "at least three", and `tools/round-46/gate.py` is outside it — so the honest citation of the file clause 7 measures turns clause 8 red. The landing may not contain that path string at all. | `exit 1`, `unresolved_citations ["tools/round-46/gate.py: outside the validated path set"]`, `refs 5` | `tools/drive2.py` case `probe-cite-gate46-honest-flag-citation`; `receipts/probes.json` |
| **F4** | 1 | Numbering is unchecked: a prefix test on the last block only, so an earlier `- **24. Decoy block with the same number.**` passes. | `exit 0`, `rule_blocks 24` | `tools/drive2.py` case `probe-duplicate-24-numbering-decoy` |
| **F5** | 1 | The marker is counted over the whole file but only recognised inside a `- **` bullet: one marker in block 24 plus one quoted anywhere else (prose or fence) → `2`; a marker in the craft section's preamble → `block_present 0`. It must appear once in the file **and** inside the last bullet. | `marker_occurrences 2 != 1`; `marker_block_count 0 != 1` | `tools/drive2.py` cases `attack-marker-quoted-elsewhere`, `probe-marker-in-craft-preamble`, `probe-marker-in-fenced-example`, `probe-block24-outside-craft-section` |

F1 is the finding that matters for landing: the claims' `Landed surface` says "one **new**
rule block", and the counter cannot distinguish "block 24 added" from "blocks 1–23 deleted,
block 24 added". Recommend L1 record the freeze `rule_blocks 23` against the landing receipt's
`rule_blocks 24` in the round report (both values are already in receipts), or add the
`rule_blocks` assertion in a round-48 claim — the frozen bytes must not be edited to close it.

F2/F3 do not touch my clauses; they change what the landing text may say. F3 is a tripwire:
`rows.md` cites `plans/round-47-claims.md:80-82` for the flag order instead of the gate path
and states the arm as "the round-46 gate".

## 6. Kill probes for clauses 1–3 (all red, all named)

`tools/drive.py`, `receipts/drive.out`; each is one mutation of candidate B in a fresh
one-commit fixture:

| mutation | exit | failing |
|---|---|---|
| marker quoted elsewhere in `SKILL.md` | 1 | `marker_occurrences 2 != 1` |
| a 25th block appended after block 24 | 1 | `marker block is not the last craft block` |
| title `24.An exact …` (no space) | 1 | `marker block title does not start with '24. '` |
| header gets a 5th cell `note` | 1 | `header [...,'note'] != ['trigger','v2 hole','v3 arm','exit']` |
| a pipe inside one cell | 1 | `a row does not have exactly 4 cells`; `exit cells outside {0,1,2}: 1`; arm token split |
| exit cell `3` | 1 | `exit cells outside {0,1,2}: 1` |
| a second 2-row table in the block | 1 | `rows 6 != 4`; `exit cells outside {0,1,2}: 2`; `rows naming != 1 routed id: [4, 5]` |

A backticked exit cell passes (`| \`1\` |`, `receipts/probes.json` `probe-backticked-exit-cells`,
exit 0) because the cell is checked as `r[3].strip("` ")`; that is house-style-safe but means
`1` and `` `1` `` are indistinguishable to clause 3 — no semantic loss, stated for completeness.

## 7. Exit-2 paths this clause depends on (verified, not assumed)

`tools/drive6.py`, `receipts/exit2.json`:

| case | exit | reason |
|---|---|---|
| craft heading loses its trailing space (`## Queue-drain craft(rounds …`) | **2** | ``no `## Queue-drain craft ` section`` — `Malformed`, never a verdict |
| `tools/round-47/exact.py` appended to after the freeze commit, scored freeze→rev | **2** | `frozen_path_changed ["tools/round-47/", "tools/round-47/exact.py"]` |

So a `24. ` block cannot be scored against malformed section bytes (exit 2, not a silent 1),
and the frozen-path guard fires on the file both pins bind — the pins cannot be re-frozen
under the counter's nose.

## 8. Receipts (exact command, exit, stdout sha256, UTC)

| receipt | command | utc | exit | stdout sha256 |
|---|---|---|---|---|
| `receipts/exact-freeze.log` | `python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f7… --rev 5017e1f7… --json-out .ufo/waves/round-47/w1/C1Struct/receipt.json` | 2026-10-28T17:52:51Z | 1 | `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba` |
| `receipts/fixture-runs.log` | `python3 -B drive.py` (candidates + 7 attacks, v3) | 2026-10-28T17:54:27Z | 0 | `f6b881f07aba6749709c6e81791293e991d7c3d917015df5210fe69928ea6e86` |
| `receipts/fixture-runs.log` | `python3 -B drive2.py` (7 clause-1/2 probes) | 2026-10-28T17:54:27Z | 0 | `a725a1c38d8986074b0ae4571864f09278c120c5abc2d51db230e42956469270` |
| `receipts/fixture-runs.log` | `python3 -B drive3.py` (6 citation probes, `record.py` present) | 2026-10-28T17:54:28Z | 0 | `cfc896798abf68c15ec77a16a20cdbe63a39a937b722f8a342c398228a150587` |
| `receipts/fixture-runs.log` | `python3 -B drive4.py` (F1 destruction, refs) | 2026-10-28T17:54:28Z | 0 | `dcea19e62592dac903eaf0250fba67ecfc33c71a47e8c191da5a5b527c8206f0` |
| `receipts/drive5.out` | `python3 -B drive5.py` (F2 isolation) | 2026-10-28T17:54:48Z | 0 | `c200bb85ced1ea1f5db45c31a3704ca47ec6e7818800f2cf0959b11fc812fb5d` |
| `receipts/drive6.out` | `python3 -B drive6.py` (exit-2 paths) | 2026-10-28T17:55:22Z | 0 | `3362790a90abee6e95ef2e8d2882246c196a9fd7dc57727360a023f54c3c8917` |
| `receipts/candidates.log` | `python3 -B gen_candidates.py` | 2026-10-28T17:54:27Z | 0 | in file (4 artifact sha256s) |

The drivers exit 0 because they record cases; each case's own exit code is the counter's and
is printed in every JSON line. `receipts/hashes.txt` carries sha256 for every archived
receipt, candidate and driver.

## 9. Risks, limits, and what I did not run

- **Not run:** the battery at the real landing revision (the block does not exist in the lane;
  candidate B's battery was run on a one-commit fixture whose only difference from the lane is
  history depth — the flag-order forgery edits the fixture's `gate.py` copy, which is the
  frozen byte-for-byte file). L1 must re-measure after landing.
- **Not run:** any mutating git/jj command, any write to the lane tree, any pacman/uv install
  (none was needed; `python3` + git only).
- **Frozen bytes untouched**; F1–F5 are reported, not "fixed".
- The `## Queue-drain craft` section is 23 blocks at the freeze and the landing must be 24:
  the one thing clause 1 cannot check (F1).
- If the landing author writes the literal marker anywhere else in `SKILL.md` — including a
  fenced example documenting this very table — clause 1 goes red (F5).

## 10. Files written (this seat only)

```
.ufo/waves/round-47/w1/C1Struct/report.md                    this report
.ufo/waves/round-47/w1/C1Struct/rows.md                       paste-ready block 24 + rows
.ufo/waves/round-47/w1/C1Struct/receipt.json                  counter at the freeze (exit 1)
.ufo/waves/round-47/w1/C1Struct/receipts/                     logs, per-case JSON, landed-revision
                                                              receipts and their two freeze checks, hashes.txt
.ufo/waves/round-47/w1/C1Struct/candidates/                   4 SKILL/block artifacts
.ufo/waves/round-47/w1/C1Struct/tools/                        drive.py … drive7.py, gen_candidates.py
```

## 11. Postscript — the block had already landed; clauses 1–3 measured on it

While this seat was verifying, siblings landed block 24 (and kept moving HEAD). Measured
read-only at rev `31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` (`tools/drive7.py`, receipt
`receipts/drive7.out`, `utc=2026-10-28T17:59:24Z`, stdout sha256
`47946e1d3f84a6c4ff40c14d34ff758653d68378549bf4867f1f60ef036e5117`), freeze guard bypassed so
the structural clauses are visible:

| clause 1–3 field | landed value |
|---|---|
| `rule_blocks` | `24` (blocks 1–23 survive — F1's hole is not exercised by this landing) |
| `marker_occurrences` / `block_present` | `1` / `1` |
| `block_is_last` / `block_title` | `true` / `"24. An instrument's bind…"` |
| `header` | `["trigger","v2 hole","v3 arm","exit"]` |
| `rows` | `4`, every row four cells |
| row exit cells | `1 / 1 / 1 / 1` |
| arm tokens after strip | `symbol / once / digest / order` |

Full CLI in the real repo, `--rev 31b092d1 --freeze f54b3b6de9085d3db449ed5d0916296cb29c1f6d`
(receipt `receipts/landed-c1-at-A6-freeze.json`, `utc=2026-10-28T17:59:44Z`, exit **0**,
stdout sha256 `b95251e88c4adc085f9317a12b34f8b2e4385235e5f1f886ed176bca5219c0a3`):
`failing []`, `frozen_path_changed []`, `rows 4`, `refs 9`, both pins matching
(`interpreter_sha256 01a4bca7…`, `mutations_sha256 19a2166e…`), battery
`forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0`, and each forgery red for
its own clause. **Clauses 1–3 are green on the artefact that is actually in the tree**, not only
on my fixture candidate. `rows.md` stays as the pre-landing draft the ticket asked for; the landed
text differs (per-row prose, nine refs) and passes the same three clauses.

## 12. Frozen-path drift since the declared freeze — C1 exits 2 under two of three freezes

`receipts/landed-freeze-check.log`, `--rev 31b092d1`:

| `--freeze` | exit | `frozen_path_changed` |
|---|---|---|
| `5017e1f7299c3a812e87e7950148f54313dd279e` (the ticket's freeze) | **2** | `plans/round-47-claims.md`, `tools/round-47/`, `tools/round-47/exact.py`, `tools/round-47/record.py` |
| `62e33f7dd75c8e3285967b26419842c106f6c965` (what `git log --format=%H -1 -- plans/round-47-claims.md` re-derives now) | **2** | `tools/round-47/`, `tools/round-47/exact.py`, `tools/round-47/record.py` |
| `f54b3b6de9085d3db449ed5d0916296cb29c1f6d` (A6) | **0** | `[]` |

Cause: the declared freeze is a series (`A1`/`A2` disclosed in `plans/round-47-claims.md:23-43`; `A3`–`A6` are commit messages), but
`record.py` moved in `A3`/`A4`/`A5` and `exact.py` moved in `A6` — after the last commit that
touched the claims file. So the file's own re-derivation
(`git log --format=%H -1 -- plans/round-47-claims.md` → `62e33f7d`) no longer names a commit whose
`tools/round-47/` bytes match; only `f54b3b6d` does. Consequences for this claim:

- the counting command's `--freeze` must be `f54b3b6d`-or-later, or C1 returns 2 and no clause is
  evaluated — a 2 never counts toward a target;
- `interpreter_sha256` computed at `5017e1f7` is `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`;
  at the landed revision it is `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5`.
  The landed block pins the latter, so the pin is internally consistent — but a report that quotes
  the freeze-era pin against the landed bytes is false;
- A6's diff is confined to `_fixture_files` (one hunk, `tools/round-47/exact.py:322-344`): the
  clause-1–3 code I quote in §1 is byte-identical at `5017e1f7` and `31b092d1`, so the clause
  semantics verified here are the landed semantics;
- the working tree also carries an uncommitted `SKILL.md` `Refs:` edit, so a score of the *tree*
  is not a score of a revision; every value above is from git objects at a named rev.
