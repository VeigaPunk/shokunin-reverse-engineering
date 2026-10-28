# R46W1RevGateMerge — the freeze core's merge arm (R45-CL6)

Seat: reviewer, merge arm of `tools/round-46/gate.py` (`history_touched`, `blob_changed`,
`freeze_state`). Read-only on the lane. Evidence dossier + scripts:
`.ufo/waves/round-46/w1/R46W1RevGateMerge/report.md` and the same directory's
`drive_gate_merge.py`, `extras.py`, `lane_probe.py`, `receipts.json`,
`lane_receipts.json`, `extras_receipts.json`, `gate_frozen.py`.

## Frozen bytes under test

| item | value |
|---|---|
| dispatch freeze | `31820472784284727546808acc31b3ea1e73919b` |
| `tools/round-46/gate.py` at the freeze | `sha256:64626cca85b2de25d495155318493b3b9eab73c6f31ad7b78f4e76c4344d772e` |
| `plans/round-46-claims.md` at the freeze | `sha256:a09564e0a2e200c46f6c1fc56991813ad13c5b67f1b5e70721ab3ceee7afad01` |
| `tools/round-46/gate.py` at HEAD `deee6595` | `sha256:847aa33baf545131bed14b90af0425aef12bdc5ed8fb375d8ddb172e5c853223` |

The only delta between the two gate.py revisions is in `main_guard`
(`print(...); return 2` → `return 2, {...}`), outside the three functions under test, so the
arm behaves identically at both. All fixture results below were produced by importing the
freeze-commit bytes (`gate_frozen.py`, sha `64626cca…`) and calling `freeze_state` directly.

## The four requested shapes, plus controls

`expected` is what `plans/round-46-claims.md` requires ("A score at REV is admissible only if
no commit in FREEZE..REV touches a frozen path … A later restore does not un-block", plus the
stated squash limit). `restored` shown only where it is non-empty or wrong.

| # | shape | expected | exit | `touched` | `blob_changed` | `restored` | verdict |
|---|---|---|---|---|---|---|---|
| a1 | conflict **on** the frozen file, both branches edit it, resolution restores freeze bytes | 2 | **2** | `tools/round-46/gate.py` | `[]` | `[gate.py]` | correct |
| a2 | one-sided frozen edit, clean auto-merge, the merge's resolution reverts it | 2 | **2** | `[gate.py]` | `[]` | `[gate.py]` | correct |
| a3 | conflict on `notes.txt`, one-sided frozen edit, resolution restores it (brief's (a), isolating) | 2 | **2** | `[gate.py]` | `[]` | `[gate.py]` | correct |
| b | same conflict, resolution **keeps** the tampered bytes | 2 | **2** | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` | exit right, `restored` **wrong** (F2) |
| c | `git merge --squash` folds a branch tamper+restore away | **0** (stated limit) | **0** | `[]` | `[]` | `[]` | gate silent — row says 2 (F1) |
| o | squash merge, the **resolution** performs the restore | **0** (stated limit) | **0** | `[]` | `[]` | `[]` | gate silent (F1) |
| c2 | control: squash folds a tamper that is **not** restored | 2 | **2** | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` | correct |
| d | plain fast-forward, nothing frozen touched | 0 | **0** | `[]` | `[]` | `[]` | correct; 0 merge commits created |
| d2 | control: fast-forward carrying a frozen tamper | 2 | **2** | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` | correct |
| e | **the merge's own resolution** adds the frozen edit; no branch commit does | 2 | **2** | `[gate.py]` | `[tools/round-46/]` | `[gate.py]` | correct — R45-CL6 closed |
| f | tamper committed, restored by a later commit, no merge | 2 | **2** | `[gate.py]` | `[]` | `[gate.py]` | correct ("a later restore does not un-block") |
| g | conflict resolved on the side branch (first parent = tampered side), main fast-forwards to it | 2 | **2** | `[gate.py]` | `[]` | `[gate.py]` | correct |
| h | merge whose **second parent predates the freeze** (false-positive probe) | 0 | **0** | `[]` | `[]` | `[]` | correct |
| i | `git merge -s ours` discards the tamper | 2 | **2** | `[gate.py]` | `[]` | `[gate.py]` | correct (side commit is still in range) |
| j | rename **inside** the frozen dir | 2 | **2** | `[tools/round-46/census.json]` (old path) | `[tools/round-46/]` | `[census.json]` | exit right; `touched` names only the source (F2/F5 note) |
| k | rename **into** the frozen dir from outside | 2 | **2** | `[tools/round-46/thing.py]` | `[tools/round-46/]` | `[thing.py]` | correct: pathspec turns it into `A`, no outside-path leakage |
| m | tamper commit rewritten away with `git commit --amend --allow-empty` | not claimed | **0** | `[]` | `[]` | `[]` | silent — unstated sibling of (c) (F7) |
| n | **uncommitted** frozen tamper (`git status` shows `M gate.py`) | row CL15 says 1 | **0** | `[]` | `[]` | `[]` | silent — no dirty arm is wired (F6) |

Notable negative result worth recording: in `a2` the merge's own first-parent diff is **empty**
(`git diff HEAD^1 HEAD` → no output); the path is caught solely because the side commit is in
`FREEZE..REV`. In `e` the merge's first-parent diff **is** the only witness. Both are in the
receipts.

## Findings

### F1 — HIGH: the squash row advertises exit 2; the gate returns 0 (the limit is real, the table denies it)

`SKILL.md:624` at HEAD `deee6595` (row unchanged since `781e19ae`, where it was line 617):

> `| R45-CL19 a tamper-then-restore folded away by `git merge --squash` | the surviving history names nothing | blob: the blob arm still compares the two revisions; the limit is stated in the table, not claimed away | 2 |`

`plans/round-46-claims.md` says the opposite about the row set: "a tamper+restore committed and
folded away with `git merge --squash` leaves nothing in the surviving history for either arm to
read; **no table row claims otherwise**."

Measured, `c` and `o`: `freeze_state` returns **0**, `touched []`, `blob_changed []`,
`restored []`; `git diff --quiet <freeze> <tip> -- plans/round-46-claims.md tools/round-46/`
exits **0** (the trees are identical). The branch ref still exists in the fixture, so this is
not a reachability artefact: `git log FREEZE..TIP` simply never contains the tamper commit.
Counter level (frozen `attest.py` against fixture `c`):

```
{"counter": "round-46-c1", "reason": "SKILL.md absent at rev"}   exit 2
```

— i.e. the freeze gate returned clean and the counter moved on to the artefact. (Against `a1`
the same binary returns `{"reason": "frozen_path_changed", …}`, exit 2, no `met_target`.)

Consequence: the table's fourth column asserts a catch that no code path performs, and the
claims file's sentence "no table row claims otherwise" is false as landed. The claims file is
frozen, so the correction must be in `SKILL.md`: the honest row is **exit 0** with the arm cell
still naming `blob` but saying the blob arm finds the two revisions equal (both tokens are
already legal: `0` is in the exit set, `blob` is in the vocabulary). `attest.py`'s own
`GOOD_ROWS` carries the same wrong `("R45-CL19", …, "blob", "2")` at `tools/round-46/attest.py:516` —
it is the selftest fixture, not the landed block, but it is the same claim written twice.

I did not edit either file.

### F2 — MEDIUM: `restored` mislabels every touched file under a directory-frozen entry

`gate.py` computes

```python
changed = blob_changed(root, base, tip, entries)          # dir entries come back as "tools/round-46/"
restored = [p for p in touched if p.rstrip("/") not in {c.rstrip("/") for c in changed}]
```

`touched` holds *file* paths from `git log`; `blob_changed` holds the *directory* `tools/round-46/`.
The two never compare equal, so every touched file under the frozen directory is reported as
"restored" even when its bytes still differ:

| fixture `b` | value |
|---|---|
| `blob(FREEZE, tools/round-46/gate.py)` | `d7cd9aace31098aa9a5f2d4b962b0e78729ae12b` |
| `blob(TIP, tools/round-46/gate.py)` | `f257e61c4447d4676bb11e741df0ba63fcb84267` |
| `blob_changed` | `["tools/round-46/"]` |
| `restored` | `["tools/round-46/gate.py"]` ← false |

This is not fixture-only. At lane HEAD `deee6595`, base `3182047`: `frozen_path_changed` and
`restored` name the **same three paths**:

```
frozen_path_changed: [tools/round-46/, tools/round-46/attest.py, tools/round-46/gate.py, tools/round-46/registry.py]
restored:            [tools/round-46/attest.py, tools/round-46/gate.py, tools/round-46/registry.py]
```

The claims file defines `restored` as "a path the history arm saw and the blob arm finds clean".
The blob arm did not find them clean. No verdict flips (the union still exits 2), but both
counters echo this field into their receipts (`attest.py:467`, `registry.py:415`), and it is the
only place the "the two must agree" property is expressed — so a landing report that reads
`restored` as "the bytes are back" is quoting a false field. A per-path fix exists:
`restored = [p for p in touched if blob(root, base, p) is not None and blob(root, base, p) == blob(root, tip, p)]`.
Fixtures `b`, `c2`, `d2`, `e`, `j`, `k` all exhibit the mislabel.

### F3 — LOW: `-m` is inert in the arm's argv, and `-m` alone is a measured false positive

`history_touched` runs `git log -m --diff-merges=first-parent …`. The later `--diff-merges`
wins, so `-m` contributes nothing today — `v2_exact` and `without_dash_m` produce **identical
stdout** in both probe fixtures (`e`: sha `0dff1df0…`; `h`: sha `e3b0c44…` = empty). If the
flags are ever reordered or `-m` is kept while `--diff-merges=first-parent` is dropped, the arm
becomes second-parent-inclusive: fixture `h` (merge whose second parent predates the freeze,
nothing in `FREEZE..REV` touching a frozen path) yields, under `--diff-merges=separate`:

```
plans/round-46-claims.md, tools/round-46/attest.py, tools/round-46/census.json,
tools/round-46/census.py, tools/round-46/gate.py, tools/round-46/registry.py
```

i.e. six false touches and exit 2 on a clean history. Recommendation: drop `-m` (or comment
that it is deliberate dead weight); the discriminator is `--diff-merges=first-parent`.

### F4 — BLOCKING for scoring (outside my arm): the dispatch freeze is not the freeze the counters accept

At HEAD `deee6595` (HEAD moved four times during this seat: `781e19ae` → `49e6cac` → `21b55a8f`
→ `deee6595`):

| base | exit | `frozen_path_changed` |
|---|---|---|
| `3182047…` (dispatch freeze; also what `git log -1 -- plans/round-46-claims.md` re-derives) | **2** | `tools/round-46/`, `attest.py`, `gate.py`, `registry.py` |
| `50862e4a` ("declared as the authoritative freeze") | **2** | `attest.py`, `registry.py` |
| `65678df0` | **2** | `registry.py` |
| `04252247` | **0** | `[]` |

Both frozen counters at HEAD with `--freeze 3182047`:

```
attest.py   exit 2  reason frozen_path_changed  met_target absent  (stdout sha 3a471c33…)
registry.py exit 2  reason frozen_path_changed  met_target absent  (stdout sha dec44f87…)
```

So the counting command printed in the claims file cannot produce a score at any rev after
`50862e4a`, and the claims file's sentence "Nothing in this file or in `tools/round-46/` changes
after the freeze" is false in fact for four commits — each of which re-declares itself the
freeze in its message, while the frozen file still re-derives `3182047`. Only base `04252247`
is clean. Related: block 23's pin `sha256:e6c44d2d…` equals `attest.py` at HEAD and at
`04252247`, but **not** at the freeze (`dd1e7df1…`), so the pin binds the landing bytes, not the
frozen ones. L1 must decide which commit the round scores against; I did not touch the freeze
or the claims file.

### F5 — LOW: `touched` changes type between exit paths

`attest.py:467` / `registry.py:415` set `"touched": len(fs["touched"])` only on the non-2 path;
the exit-2 branch returns `dict(fs, …)`, where `touched` is the **list**. Measured:
`touched_type: "list"` in both lane receipts. A consumer that compares `touched == 0` or does
arithmetic silently changes meaning between a clean and an inadmissible score.

### F6 — MEDIUM-LOW (adjacent, not merge): the `dirty` arm is advertised but never called

`SKILL.md:622` (row R45-CL15) gives the `dirty` arm exit 1. In the frozen instrument `dirty` is
only a vocabulary token (`attest.py:46`) and a selftest row literal (`attest.py:508`); neither
counter calls `gate.dirty`, and no selftest red case exercises it (`grep -n dirty
tools/round-46/{attest,registry}.py` → those two lines, nothing in `registry.py`). Probe `n`:
an uncommitted frozen tamper (`git status --porcelain` → ` M tools/round-46/gate.py`) gives
`freeze_state` exit **0**, `touched []`, `blob_changed []`; `gate.dirty(D, pathspecs)` does
return `['tools/round-46/gate.py']`, so the helper works and simply has no caller. Same pattern
as F1: a row's exit that no code produces.

### F7 — INFORMATIONAL (adjacent): the "inherent limit" is stated for squash only, and amend has the same silence

`git commit --amend --allow-empty` after restoring the bytes replaces the tamper commit with an
empty one: `git log FREEZE..TIP --name-status` prints only the commit line, `blob_changed []`,
`freeze_state` exit **0**. This is the same class as the squash fold (history rewritten so the
tamper never enters the surviving graph) and has no row. The claims file's "Inherent limit,
stated not claimed (R45-CL19)" therefore understates the limit set. Informational: it needs a
rewrite of an already-pushed commit, and the round's receipts cite shas.

## What is confirmed closed

R45-CL6 is genuinely closed for the merge shapes that leave history behind. On fixture `e` —
the merge's own resolution is the only writer of the frozen edit — the v2 arm names
`tools/round-46/gate.py` while the round-45 argv (`git log --name-only`, no diff-merges) emits
**byte-empty** output (`sha256 e3b0c442…`, the empty-string digest). `a1`/`a2`/`a3`/`b`/`g`/`i`
show the restore and keep variants are all caught, including `-s ours` (blob clean, side commit
still read) and a merge whose first parent is the tampered branch. `d`/`d2` show fast-forward
merges are read through the side commit, not through a merge diff.

## Residual risk / not run

- `git replace --graft`, shallow clones, reflog-based recovery of a squashed branch: **not run**.
  The claims file does not claim them; a graft could hide a second parent from `git log`.
- The C1 battery, the sha pin's resolution, and the C2 census/registry arms: other seats.
- A full `met`/`not met` counter run over the landed block: **not run** — HEAD moved four times
  during the seat and `SKILL.md` was being edited, so any score would measure a moving artefact;
  the clean base `04252247` exists but the landed table is not final.
- Tool installs: none.

## Repro

```sh
S=/fast/scratch/hyaku/kaidoku-r46/R46W1RevGateMerge   # scratch, removed after the seat
python3 -I -B <seatdir>/drive_gate_merge.py    # 15 fixtures incl. a1-a3,b,c,c2,d,d2,e,f,g,h,i,j,k
python3 -I -B <seatdir>/extras.py              # m (amend), n (dirty), o (squash-resolution)
python3 -I -B <seatdir>/lane_probe.py          # four freeze bases, both counters at HEAD
# frozen gate bytes are reconstructed with:
git -C <LANE> show 31820472784284727546808acc31b3ea1e73919b:tools/round-46/gate.py
```

`receipts.json` (355 command receipts), `lane_receipts.json`, `extras_receipts.json` each carry
per step `{cmd, exit, stdout_sha256, utc}`.
