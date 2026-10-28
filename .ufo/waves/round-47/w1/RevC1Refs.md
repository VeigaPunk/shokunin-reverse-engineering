# RevC1Refs — clause 8 of R47-C1 attacked (citations and pins)

Seat `RevC1Refs`, wave 1, round 47, lane `kaidoku`. Scope: **clause 8 only** — "at least
three citations carry a line selector while resolving at the measured revision inside
`corpus/lessons/`, `corpus/knowledge/`, `plans/` or `tools/round-47/`, … both sha256 pins
match" (`plans/round-47-claims.md` `## R47-C1` clause 8, read at
`plans/round-47-claims.md@5017e1f`). Everything below is a fixture measurement, not a
reading of the code.

- **Measured revision** `PIN = 31b092d17e77f5064c919383a9bc1e6cbfd2d1ff`.
- **Counter at PIN** `tools/round-47/exact.py` sha256
  `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5` (the block's own
  `interpreter_sha256` is the same value at PIN).
- **Declared freeze** `5017e1f7299c3a812e87e7950148f54313dd279e`.
- Fixtures are `git archive <PIN> | tar -x` copies of the lane, one commit each, so every
  citation resolves exactly as it does in the lane; only block 24's `Refs:` line (or the
  executing interpreter) is varied. Each fixture's `git -C <fixture> rev-parse
  --show-toplevel` was asserted equal to the fixture before the commit.
- Read-only on the lane: no write, no git mutation, no install. Scratch
  `S=/fast/scratch/hyaku/kaidoku-r47/RevC1Refs` (removed after the receipts were copied
  here); nothing under `/tmp`.

## Verdict

Clause 8 is the loosest clause in the matrix: it asks whether a *string* resolves, never
whether the citation *is evidence for the row it sits beside*. Six of the nine attack
classes I ran reach **exit 0**, including one where the counter's own interpreter pin
certifies bytes other than the ones that produced the verdict.

| # | attack | fixture (receipt) | exit | claim holds? |
|---|---|---|---|---|
| 1 | citations resolve but are off-topic (line 1-1 anchors, every selectored citation contentless) | `fx-x1_contentless` (`x1_all_contentless`) | **0** | hole |
| 2 | path that is a *prefix of* the allowlist (`corpus/lessons-evil/`) | `fx-f2_prefix_evil`, `fx-c2_prefix_evil` (file present, byte-identical) | 1 | **rejected correctly** |
| 3 | range that ends exactly at the last line (and the whole file) | `fx-f3_lastline` | **0** | hole (boundary itself correct) |
| 3b | one line past EOF | `fx-f3b_pasteof` | 1 | rejected correctly |
| 4 | pin computed over a *copy* of the counter — copy executes, original is pinned | `fx-f4_real_interp` vs `fx-f4_lax_copy` | 1 vs **0** | **hole** |
| 4b | block pins a *different* copy's digest | `fx-f4b_pin_over_lax` | 1 | rejected correctly |
| 5 | one citation repeated three times (= `refs 3`) | `fx-f1c_samefile3x` | **0** | hole |
| 6 | selector-less self reference (`tools/round-47/exact.py` bare) | `fx-f1d_bare_self`, `fx-f5_strict_interp` | **0** / 1 | hole |
| 7 | directory citation (`plans/:1-2`) | `fx-f6b_dir` (no battery) / `fx-f6c_dir_battery` | **0** / 2 | hole + crash |
| 8 | off-topic *file* under an allowed prefix | `fx-f2b_sibling_bak` | **0** | hole |
| 9 | legitimate `corpus/knowledge/` citation | `fx-f6_knowledge` | 0 | repaired by A6 |

## F1 (HIGH) — the citation apparatus can be made entirely contentless

Receipt `receipts/x1_all_contentless.json`, fixture `fx-x1_contentless`. Transformation:
every `corpus/lessons/round-46.md:<n>` in block 24 rewritten to `…:1-1` and every
`plans/round-47-claims.md:<n>` to `…:1-1` (line 1 of each file is a heading; the four
routed ids live at lines 57/60/63/65).

```
python3 -I -B <fx>/tools/round-47/exact.py --root <fx> --freeze <fxrev> --rev <fxrev>
exit 0   failing []   refs 9
battery {genuine_green 1, v2_green 4, v3_green 0, forgeries_total 4, crash 0}
stdout sha256 f0ab45818334…
```

The battery is fully green on a block whose citations carry no content. Smaller variants
of the same hole, all exit 0 with the battery green: `f1_offtopic` (`round-46.md:1-1`,
`claims.md:1-1`, `exact.py:1-1`), `f1b_wronground` (`corpus/lessons/round-45.md:1-5` and
`:6-9` cited for round-46 defects), `f2b_sibling_bak`
(`corpus/lessons/round-46-verifier-spotcheck.md:1-5`, `:6-9` — a different document,
allowed by the prefix test), `f1c_samefile3x` (line 5 cited three times).

What clause 8 would have to say: bind the citation to the row. The four rows exist because
`corpus/lessons/round-46.md` names `R46-CL2`/`CL3`/`CL4`/`CL6` at 57/60/63/65 (measured at
PIN: `git show <rev>:corpus/lessons/round-46.md | grep -n '^- \*\*R46-CL'`), so the clause
should require one citation per routed id whose range *contains that id's line at
`--rev`*, re-derived by the counter, instead of `refs >= 3` over the block as a whole.
Today a single range (`57-66`) covers all four rows and a single line (`1-1`) covers none.

## F2 (HIGH) — "every reference carries a line selector" is not what the counter does, and the landed block relies on it

`check_refs` exempts the interpreter's own path (`if name == SELF: continue  # identified by
its own sha256 pin, not by a line selector`). The landed block cites
`` `tools/round-47/exact.py` `` **twice with no selector**, and passes:

- `f0_landed_ascommitted` — landed block unchanged, frozen counter, exit **0**, `refs 9`.
- `f5_strict_interp` — the same block and the same fixture bytes, scored by a copy of the
  same counter with only that two-line exemption removed
  (`interpreters/exact-strict.py`, sha256 `df993d5c738e…`): exit **1**,
  `failing ["unresolved or unvalidated citations: 2"]`.

So the claim's sentence and the code disagree, and the *landed* block is on the code's side,
not the sentence's. What clause 8 would have to say: either "every reference other than
`tools/round-47/exact.py` carries a line selector", or the block cites
`tools/round-47/exact.py:<line>` and the exemption is deleted.

## F3 (HIGH) — `refs >= 3` counts occurrences, not citations

`receipt["refs"] = len(HARD_REF.findall(block))`; `cited` is a set but is only consulted for
`MUST_CITE`. Consequences, both exit 0 with the battery green:

- `f1c_samefile3x` — the *same* line cited three times: `refs 6` (three of them from the
  Refs line I swapped in, three left in the prose).
- `f1d_bare_self` — two selector-less `tools/round-47/exact.py` plus one real selector:
  exit 0, so the block satisfies "at least three citations carry a line selector" with
  **one** selectored citation.

What clause 8 would have to say: "at least three **distinct** citations carry a line
selector" and the code counts `len({name for name, first, _ in refs if first})` over
non-self names. The landed block has five distinct selectored citations, so the stricter
reading costs it nothing.

## F4 (HIGH) — a *directory* resolves as a citation, and crashes the battery

`git show <rev>:plans/` prints a tree listing (15 lines at PIN); `git show
<rev>:tools/round-47/` prints 4. `HARD_REF` matches `plans/` and `tools/round-47/`, the
prefix test accepts them, and `line_count` counts the listing's lines:

- `f6b_dir` — Refs line `tools/round-47/:1-2`, `plans/:1-2`, `round-46.md:1-1`, `--no-battery`:
  exit **0**, `failing []`.
- `f6c_dir_battery` — same block with the battery (the counting command in the claims runs
  the battery): exit **2**, `reason "unhandled IsADirectoryError: [Errno 21] Is a
  directory: '<battery>/fx-…/tools/round-47/'"`. A6's `_fixture_files` copies every cited
  path into the battery fixture and writes `tools/round-47/` as a *file* path.

What clause 8 would have to say: "each reference names a **blob** at `--rev`" and the
counter rejects names ending in `/` (or checks `git cat-file -t <rev>:<name> == blob`);
`_fixture_files` must skip non-blobs instead of trying to write them.

## F5 (HIGH) — the interpreter pin certifies the committed bytes, not the bytes that ran

Two runs, byte-identical fixture (`fx-f4_real_interp` / `fx-f4_lax_copy`, same fixture
content, same `--freeze`/`--rev`), different executing file:

```
python3 -I -B <fx>/tools/round-47/exact.py --root <fx> --freeze <r> --rev <r> --no-battery
  exit 1  failing ["unresolved or unvalidated citations: 2"]     (citation outside the set)
python3 -I -B /fast/scratch/hyaku/kaidoku-r47/RevC1Refs/lax/exact.py --root <fx> \
        --freeze <r> --rev <r> --no-battery
  exit 0  failing []   met_target true
```

`interpreters/exact-lax.py` is the frozen counter with one line changed
(`return bad, cited` → `return [], cited`, sha256 `bb950d83cf5d…`). Both receipts report
`interpreter_sha256_expected = 01a4bca…` (the pinned bytes at `--rev`) and neither reports
the digest of the file that executed. The block's pin therefore *is* equal to "the sha256 of
`tools/round-47/exact.py` at the measured revision" in the run that returned 0 — clause 8
as written is satisfied by a verdict produced by different bytes.

The pin is content-addressed, so the other direction is safe: a block that pins a *copy's*
digest fails (`f4b_pin_over_lax`, exit 1, `"interpreter sha256 pin does not match the bytes
at rev"`). What is missing is provenance, not integrity.

Mitigation that already exists: `gate.freeze_state` refuses a dirty worktree under the
frozen paths — `x2_clean` exit 0, then one appended line in the worktree copy,
`x2_dirty_worktree` exit **2** `frozen_worktree_dirty`. So in-lane tampering is caught; the
residual hole is any interpreter outside `plans/round-47-claims.md`/`tools/round-47/` (a
copy in scratch, a wrapper, a different Python entry point).

What clause 8 would have to say: the receipt records `sha256(open(__file__,'rb').read())`
as `interpreter_sha256_running`, and clause 8 requires
`interpreter_sha256_running == interpreter_sha256 == sha256(tools/round-47/exact.py at
--rev)`. One line in `score()` plus one sentence in the claim closes it.

## F6 (MEDIUM) — the last-line boundary is right, but the whole file is a legal "selector"

`f3_lastline`: `round-46.md:1-102`, `:102`, `:102-102` (file has 102 lines at PIN) →
exit **0**, battery green. The boundary itself is correct — `f3b_pasteof` (`:103`) → exit 1,
`"unresolved or unvalidated citations: 1"`. But `:1-102` selects the entire file, which is
the degenerate case of F1. What clause 8 would have to say: a range length cap (e.g. ≤ 40
lines) or "the range lies inside the section the row names".

## F7 (MEDIUM) — the landed block's own labels are off their ranges

Measured at PIN (`git show <rev>:plans/round-47-claims.md | grep -n`):

- `plans/round-47-claims.md:45-113` is labelled "the R47-C1 predicate and its nine clauses";
  the predicate heading is at 89 and `**Target.**` at 112. Lines 45–88 are causal
  separability, prior state and landed surface.
- `plans/round-47-claims.md:141-176` is labelled "the R47-C2 predicate and its result"; the
  predicate heading is at 162, `**Target.**` at 182. Lines 141–161 are prior state and the
  result is excluded.

The counter cannot see this (both ranges resolve), and every freeze amendment shifts the
targets again. What clause 8 would have to say: cite the predicate's own range, or have the
counter require the cited range to contain the literal `**Predicate` line of the section
the label names.

## F8 (BLOCKING, project-level) — at the declared freeze both counters exit 2

`receipts/L_lane_declared_freeze.json`:

```
python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f7299c… --rev 31b092d1… --no-battery
exit 2  reason frozen_path_changed
frozen_path_changed ["plans/round-47-claims.md", "tools/round-47/", "tools/round-47/exact.py",
                     "tools/round-47/record.py"]
```

Amendments A1–A6 committed changes to both frozen paths (`9018c53`, `62e33f7`, `2e4ae43`,
`1e2c310`, `07d2894`, `f54b3b6`). The claims file's own sentence — "a change makes both
counters exit 2 `frozen_path_changed`" — is therefore true of the round as it stands. The
round cannot score against `5017e1f`; the freeze must be re-cut and the report must cite
`plans/round-47-claims.md@<new freeze>`.

Related pin churn: A6 (`f54b3b6`) rewrote `tools/round-47/exact.py`, which made the block's
`interpreter_sha256` stale (observed: exit 1 `"interpreter sha256 pin does not match the
bytes at rev"` at `f54b3b6`); the pin is current again at PIN
(`01a4bca…` = counter digest). Any further counter edit re-opens this, so the pin refresh
must be the **last** edit before the landing commit, and the freeze must be re-cut after it.

## Closed by A6 (verified, not a finding)

Before A6, the battery's private five-path fixture dict (`SKILL.md`, claims, exact.py,
gate.py, `round-46.md`, `round-45.md`) rejected any citation outside it, so a *legitimate*
`corpus/knowledge/` citation — which clause 8 explicitly allows — turned the block red:
`receipts/c6_knowledge_battery.json`, exit 1, `["battery v2_green 0 != 4", "battery
genuine_green 0 != 1"]`. A6's `_fixture_files` now copies every cited path, and
`f6_knowledge` (the block citing
`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`) exits
**0** with the battery green. The same repair introduced F4's crash for directory
citations.

## Residual risk (not run)

- `gate.dirty` is blind to gitignored bytes under the frozen paths (`.gitignore` carries
  `__pycache__/` and `*.pyc`): `b5_ignored_worktree` — a forged
  `tools/round-47/__pycache__/forged.pyc` present, counter exit 0, nothing flagged.
  `exact.py` runs as a script so that file is inert, but `gate` is *imported* from
  `tools/round-46/` and a poisoned `tools/round-46/__pycache__/gate.cpython-*.pyc` is
  neither frozen nor dirty-checked. I did not attempt to fabricate a pyc header — **not
  run**.
- A non-UTF-8 blob under an allowed path: none exists at PIN (`iconv` over every blob in
  `corpus/lessons/`, `corpus/knowledge/`, `plans/`, `tools/round-47/`), so the
  `text=True` decode path is untested — **not run**.
- R47-C2's clauses are out of this seat's scope; not measured.

## Recommended clause-8 wording (minimal, meets the landed block)

> 8. Each of the four rows' routed id is cited once: the block carries, per routed id, one
>    `<path>:<start>-<end>` whose path resolves at `--rev` to a **blob** inside
>    `corpus/lessons/`, `corpus/knowledge/`, `plans/` or `tools/round-47/` and whose range
>    contains the line at which `corpus/lessons/round-46.md` names that id at `--rev`; every
>    reference other than `tools/round-47/exact.py` carries a line selector; the distinct
>    selectored set has at least three members; `corpus/lessons/round-46.md` is cited;
>    `mutations_sha256` and `interpreter_sha256` match, and the receipt's
>    `interpreter_sha256_running` — the digest of the file that executed — equals
>    `interpreter_sha256`.

The landed block already satisfies all but the per-row binding and the running-digest field;
both are cheap. Alternatively the block's Refs line gains four routed-id-tagged citations
and `score()` gains two lines: reject a name ending in `/`, and record `__file__`'s digest.

## Evidence index (this directory)

- `receipts/final_matrix.json` — every row of the matrix: `variant`, `lane_pin`,
  `base_skill_sha256`, `fixture`, `fixture_rev`, full `cmd`, `exit`, `stdout_sha256`,
  `utc`, `failing`, `battery`, `interpreter_sha256`.
- `receipts/x1_all_contentless.json`, `receipts/x2_*.json` — the contentless-citation and
  dirty-guard runs (`extras.py`).
- `receipts/repro-final-matrix.log` — the same matrix re-run end to end at `PIN` with the
  shipped driver; every exit code reproduced.
- `receipts/L_lane_declared_freeze.json` — the lane itself at the declared freeze.
- `receipts/c*_*.json`, `receipts/b*_*.json`, `receipts/f6_*`, `c6_*` — the earlier
  reduced-fixture rounds: `c2_prefix_evil_nobat` (prefix attack with the file present),
  `c6_knowledge_battery` (the pre-A6 false red), `b4_dirty_exact_worktree`.
- `final_matrix.py`, `extras.py` — the drivers. Re-run with
  `R47_PIN=31b092d17e77f5064c919383a9bc1e6cbfd2d1ff python3 final_matrix.py` (recreates the
  scratch root, the two patched interpreters and every fixture, then rewrites the receipts).
- `interpreters/exact-lax.py` (F5) and `interpreters/exact-strict.py` (F2) — the two
  one-line variants of the frozen counter, digests in the receipts.
- `f7_dirty_worktree` / `f7b_dirty_after_edit` in `final_matrix.py` are **superseded**:
  `measure()` rebuilds its fixture, so the edit was discarded between the two runs. The
  valid pair is `x2_clean` / `x2_dirty_worktree` (`extras.py`), which edit in place.
