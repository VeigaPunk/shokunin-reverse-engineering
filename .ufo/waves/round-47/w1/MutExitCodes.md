# MutExitCodes — exit-code semantics of the round-47 frozen counters

Seat: `MutExitCodes` (leaf, no dispatch). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Lane head at measurement **`09a9f912f4a639b91bce7dcd3711d8f391969d4f`** (2026-10-28T18:03Z). The lane was
live and moved repeatedly during the seat (`1e2c3102` → `07d2894e` → `f54b3b6d` → `a0753786` →
`31b092d1` → `09a9f912` → `b1a058f3`), so every receipt names the rev it measured, the load-bearing
rows have their full receipt in `evidence/`, and the final check was repeated at `b1a058f3`
(freeze derived by `git rev-list -1` → `f54b3b6d`, C1 exit 0 `met_target true`).

Frozen surfaces read only: `plans/round-47-claims.md`, `tools/round-47/exact.py`,
`tools/round-47/record.py` — all mutated only as **copies under scratch**, never in place
(§5 Restoration).

Installs: **none** (`pacman` paused; no `uv`/`npx`/binary install was needed).

---

## 1. Verdict

The five assigned could-not-evaluate input classes are handled as the exit contract requires, with one
exception: **C2 has no freeze arm at all**, so a mutation of its own frozen bytes reads as `met` (exit 0).
Beyond that, five exit-code paths leave the 0/1/2 contract (`--json-out` open failures, import-time
failure, post-guard crash, `BaseException`), and two frozen clauses are false:

| # | what | kind | exit seen | expected |
|---|---|---|---|---|
| F1 | C2 scores `met` (0) over a rewritten frozen `record.py` / frozen claims file | **frozen clause false + exit-2 → 0** | 0 | 2 |
| F2 | C1 at the *declared* freeze (A2) against any landing rev exits 2 — the declared freeze is stale | frozen record stale (converges with `R47-CL11`) | 2 | — |
| F3 | C1 receipt's `restored` names two files as clean that both changed (15+/1− and 21+/4−) | **receipt false** | 2 | — |
| F4 | C2's `axes` correction class is unparsed: a false axes correction cannot redden, a true one cannot repair | **frozen clause vacuous** | 0 / 1 | 1 / 0 |
| F5 | `--json-out` open failure, import failure, post-guard crash, `BaseException` exit 1 / SIGINT, no receipt | exit contract broken | 1, 1, 1, −2 | 2 |
| F6 | "Causal separability": C2 *does* read the craft section C1 lands on | **frozen clause false** | 1 | 0 |
| F7 | `--selftest` alone cannot run (required `--root/--freeze/--rev`) | usability | 2 | 0/1 |

All other assigned inputs behave: unknown revisions, non-ancestor freeze, malformed claims file,
unreadable `SCORECARD` (absent / invalid UTF-8 / directory / blob object removed) → exit 2 each,
never 0. 91 receipts: `MutExitCodes/receipts.jsonl`; full receipts for the load-bearing rows:
`MutExitCodes/evidence/`.

---

## 2. Matrix

`$L` = lane root, `<FX>` = a scratch fixture repo (`git -C <FX> rev-parse --show-toplevel` asserted
before every commit), `<HEAD>` = `09a9f912` unless the row names another rev. Every command was run as
`python3 -I -B <counter> …` with `HYAKU_SCRATCH=$S`, `TMPDIR=$S`.

### 2.1 Assigned class (a) unknown revisions

| probe | command (abridged) | exit | expect |
|---|---|---|---|
| `c1-unknown-freeze` | `exact.py --root $L --freeze cafe… --rev $HEAD --no-battery` | 2 | 2 |
| `c1-unknown-rev` | `exact.py --root $L --freeze $F1 --rev deadbeef… --no-battery` | 2 | 2 |
| `c1-rev-noncommit-object` | `exact.py --root $L --rev HEAD:SKILL.md` | 2 | 2 |
| `c1-unknown-freeze-v2-profile` | same as row 1 with `--profile v2` | 2 | 2 |
| `c1-root-not-a-repo` / `c1-root-missing` | `--root <plain dir>` / `--root <nonexistent>` | 2 / 2 | 2 |
| `c2-unknown-rev` | `record.py --root $L --rev not-a-rev --no-battery` | 2 | 2 |
| `c2-root-not-a-repo` | `record.py --root <plain dir> --rev HEAD` | 2 | 2 |

### 2.2 Assigned class (b) non-ancestor freeze

| probe | command | exit | expect |
|---|---|---|---|
| `c1-nonancestor-freeze` | `exact.py --root $L --freeze <HEAD> --rev 13a9e9e1` (freeze is a descendant of rev) | 2 | 2 |
| `c1-freeze-side-branch` | fixture: `main` + diverged `side`; `--freeze <side> --rev <main>` | 2 | 2 |

Reason string is `freeze is not an ancestor of rev` in both. C2 takes no `--freeze` at all (§3 F1/F6),
so this class does not exist for it — see the side-branch row in 2.6.

### 2.3 Assigned class (c) malformed claims file (scratch copies; freeze == rev, so only the parse can fail)

| probe | claims bytes in the fixture | exit | expect |
|---|---|---|---|
| `c1-claims-absent` | file absent | 2 | 2 |
| `c1-claims-no-frozen-heading` | no `## Frozen paths (exact)` section | 2 | 2 |
| `c1-claims-frozen-empty` | heading present, no `- \`path\`` list item | 2 | 2 |
| `c1-claims-binary` | `b"\xff\xfe\x00claims\x00\n"` | 2 | 2 |
| `c1-claims-is-a-directory` | `plans/round-47-claims.md/part.md` | 2 | 2 |
| `c1-claims-tip-empty-list` | valid at the freeze, empty list at the rev | 2 | 2 |
| `c1-claims-valid-control` | well-formed claims, freeze == rev | 1 (artifact) | not 2 |

Reasons: `claims file absent at rev`, `claims file has no '## Frozen paths (exact)' section`,
`frozen section lists no path`, `unhandled UnicodeDecodeError: …` (binary), `at rev: frozen section
lists no path` (union arm). The valid-shape control never returns 2, so the 2s above are attributable
to the malformation rather than to "the claims file differs". Boundary (F8, minor): a well-formed file
naming a frozen path that exists nowhere (`tools/round-47-ghost/`) is accepted — `frozen_set` never
requires existence; result was exit 1 on the artefact, not 2 and not 0.

### 2.4 Assigned class (d) unreadable SCORECARD

| probe | mutation at the measured rev | exit | expect |
|---|---|---|---|
| `c2-card-deleted` | `SCORECARD.md` removed | 2 | 2 |
| `c2-card-binary-utf8` | `b"\xff\xfe# card\n\x00\x80\n"` | 2 | 2 |
| `c2-card-is-a-directory` | `SCORECARD.md/part.md` | 2 | 2 |
| `c2-card-object-missing` | tree intact, loose blob deleted from `.git/objects` | 2 | 2 |
| `c2-card-worktree-chmod000` | worktree file `chmod 000`, committed bytes fine | 0 | 0 (by design) |
| `c2-green-control` | unmutated | 0 | 0 |

The `chmod 000` row is **not** a hole: the counter reads git objects (`gate.show`), so an unreadable
*worktree* copy is not an input to the graded surface. It is listed so the difference is not misread.

### 2.5 Assigned class (e) crash injected into a scratch copy

Mutants are written to `$S/mut/tools/round-47/exact.py` (with `gate.py` beside it; `drive7.py`
recreates them, the scratch tree is removed on yield) and run against a freeze==rev fixture, so the
frozen-path arm cannot pre-empt the crash:

| probe | injection point | exit | expect |
|---|---|---|---|
| `c1-crash-control-HEAD` | none (fixture is green when the counter is unmutated) | 0 | 0 |
| `c1-crash-score-runtimeerror` | `raise RuntimeError` at `score()` entry | 2 | 2 |
| `c1-crash-score-memoryerror` | `raise MemoryError` at `score()` entry | 2 | 2 |
| `c1-crash-emit-unserialisable` | receipt carries a `set`; crash inside `gate.emit` | **1** | 2 |
| `c1-crash-keyboardinterrupt` | `raise KeyboardInterrupt` at `score()` entry | **−2 (SIGINT)** | 2 |
| `c2-crash-control-green` | none | 0 | 0 |
| `c2-crash-evaluate-text-runtimeerror` | `raise RuntimeError` at `evaluate_text()` entry | 2 | 2 |
| `c2-crash-post-guard-emit` | receipt carries a `set`; crash inside `gate.emit` | **1** | 2 |
| `c1-import-failure` / `c2-import-failure` | `tools/round-46/gate.py` absent → `import gate` fails | **1** / **1** | 2 |

`Exception` inside the guarded region is handled exactly as documented (`{"reason": "unhandled
RuntimeError: …"}` + exit 2). The last four rows are the guard's boundary: `main_guard` wraps
`evaluate` only, so everything outside it — the import, `gate.emit`, and `BaseException` — escapes as
a **violation-looking** exit 1 or a signal, with **empty stdout and no receipt**.

### 2.6 Reproducible lane-level rows

| probe | command | exit | note |
|---|---|---|---|
| `c1-freeze-F1-at-F1` | `exact.py --freeze 5017e1f --rev 5017e1f` | 1 | the claims' own Before control (block absent) |
| `c1-freeze-F1-at-HEAD` | `exact.py --freeze 5017e1f --rev <HEAD>` | 2 | `frozen_path_changed`: claims **and** `tools/round-47/` |
| `c1-freeze-A2-at-HEAD` | `exact.py --freeze 62e33f7d --rev <HEAD>` | 2 | `blob_changed ["tools/round-47/"]` (F2) |
| `c1-freeze-A6-at-HEAD` | `exact.py --freeze f54b3b6d --rev <HEAD>` | 0 | battery 4/4/0/1/0, `met_target true` |
| `c2-at-base` | `record.py --rev 13a9e9e1` | 1 | exactly the 4 mismatches the claims' Before names |
| `c2-at-A2` | `record.py --rev 62e33f7d` | 0 | the frozen instrument changed twice after this rev |
| `c2-at-HEAD-battery` | `record.py --rev <HEAD>` | 0 | `correction_forgeries 3`, `forgeries_green 0` |
| (final check) | `exact.py --freeze $(git rev-list -1 b1a058f3 -- plans/round-47-claims.md tools/round-47/) --rev b1a058f3` | 0 | `met_target true` — the derivation rule of F2 holds at the newest head |
| `c2-rev-side-branch-off-landing` | `record.py --rev <side commit off the landing>` | 0 | no freeze and no ancestry arm (F6) |
| `c1-selftest-with-required-args` | `exact.py --root /nonexistent --freeze x --rev y --selftest` | 0 | 16 cases, 0 failures |
| `c2-selftest-with-required-args` | `record.py --root /nonexistent --rev y --selftest` | 0 | 10 cases, 0 failures |
| `c1-selftest` | `exact.py --selftest` (as documented) | 2 | argparse: required `--root/--freeze/--rev` (F7) |
| `c1-selftest-no-scratch` / `-tmp-scratch` | unset scratch root / `HYAKU_SCRATCH=/tmp` | 2 / 2 | `no HYAKU_SCRATCH/TMPDIR root set` / `scratch root is a temporary partition: /tmp` |
| `c2-selftest-no-scratch` / `-tmp-scratch` | same, C2 | 2 / 2 | same two reasons |

`c2-at-base` reproduces the claims' Before exactly: `mismatches 4` = seats round-45 claimed `[40,32]`
vs derived `[40,36]`, the round-46 window naming `<tip>`, coverage claimed `133/133` vs derived
`138/138`, depth claimed `20/20` vs derived `23/23` (evidence `c2-at-base.json`).

---

## 3. Findings

### F1 — C2 has no freeze arm: a rewritten frozen counter scores `met` (exit 0)

The claims file states, sentence-initial and unqualified:

> Nothing in this file or in `tools/round-47/` changes after the freeze: a change makes **both
> counters** exit 2 `frozen_path_changed`.

`record.py` never calls `gate.freeze_state`. `grep -c 'freeze_state\|frozen' tools/round-47/record.py`
→ **0**; `main()` has no `--freeze` argument. Measured on two nested fixtures (green C2 fixture →
`exit 0`; clone → one tampering commit → run the lane's own `record.py` at the tampering rev):

```
$ python3 -I -B <FX>/tools/round-47/record.py --root <FX> --rev <tamper-rev> --no-battery \
      --json-out <FX>/receipt.json
exit 0        receipt: "met_target": true, "mismatches": [], "corrections": 2
```

* tamper 1 — `tools/round-47/record.py` gains one comment line after the freeze
  (commit `ca7d86275cc1e0e0fc63b9cd7c9c0d05bfa73b81`, patch: `evidence/c2-frozen-counter-tampered.patch`):
  exit **0**, expected 2. Receipt: `evidence/c2-frozen-counter-tampered.json`.
* tamper 2 — `plans/round-47-claims.md` is cut down to one frozen entry: exit **0**, expected 2.
  Receipt: `evidence/c2-frozen-claims-tampered.json`.

Live instance in the lane, not just a fixture: `tools/round-47/record.py` was rewritten by **A3
`2e4ae434`, A4 `1e2c3102`, A5 `07d2894e`** and `exact.py` by **A6 `f54b3b6d`**, all after the declared
freeze `62e33f7d`, and C2 scores `met` at both ends:

```
$ python3 -I -B tools/round-47/record.py --root $L --rev 62e33f7d --no-battery   # exit 0
$ python3 -I -B tools/round-47/record.py --root $L --rev $HEAD                   # exit 0
```

So the sentence is true only for C1. A landing whose `record.py` is rewritten between the freeze and
the measured rev is scored as clean by that same rev's bytes — the class the round exists to close
(R46-CL4's "delete a mutation and the denominator moves silently" has a C2 twin: rewrite the
re-deriver and every atom re-derives).

### F2 — the declared freeze is stale; the only scoring freeze is the last frozen-path commit

```
$ git rev-list --count 62e33f7d..HEAD -- tools/round-47/      → 4
$ git rev-list -1 HEAD -- plans/round-47-claims.md tools/round-47/  → f54b3b6d  (A6)
$ python3 -I -B tools/round-47/exact.py --root $L --freeze 62e33f7d --rev $HEAD --no-battery
exit 2   "reason": "frozen_path_changed", "blob_changed": ["tools/round-47/"]
         "touched": ["tools/round-47/exact.py","tools/round-47/record.py"]
$ python3 -I -B tools/round-47/exact.py --root $L --freeze 5017e1f  --rev $HEAD --no-battery
exit 2   "blob_changed": ["plans/round-47-claims.md", "tools/round-47/"]
$ python3 -I -B tools/round-47/exact.py --root $L --freeze f54b3b6d --rev $HEAD   # battery on
exit 0   battery {"forgeries_total":4,"v2_green":4,"v3_green":0,"genuine_green":1,"crash":0}
```

Evidence: `evidence/c1-freeze-A2-at-HEAD.json`, `evidence/c1-freeze-F1-at-HEAD.json`,
`evidence/c1-freeze-A6-at-HEAD.json`, `evidence/c1-freeze-A6-at-HEAD-battery.json`.

A1 declares "the declared freeze is the commit that carries this paragraph"; the A2 receipt set
(`.ufo/waves/round-47/l1/scores/c1-at-A2.json`) uses `62e33f7d`, and that pair now exits 2 at every
rev after A3. The claims file also calls the series "a series of **two**"; six commits after the first freeze touch
the frozen pathspec (`9018c53b`, `62e33f7d`, `2e4ae434`, `1e2c3102`, `07d2894e`, `f54b3b6d` — four of
them rewrite `tools/round-47/` itself), and the file is byte-frozen, so it cannot disclose the later
four without becoming the changed path itself. Operationally: **freeze := `git rev-list -1 <rev> -- plans/round-47-claims.md
tools/round-47/`** is the only derivation that scores, and each future instrument edit invalidates the
previous pair. (Converges with the finding the lane already routed in `09a9f912` as `R47-CL11`; the
numbers above are the reproduction.)

### F3 — the C1 receipt's `restored` list is false when a frozen entry is a directory

```
$ python3 -I -B tools/round-47/exact.py --root $L --freeze 62e33f7d --rev $HEAD --no-battery
"blob_changed": ["tools/round-47/"],
"touched":      ["tools/round-47/exact.py","tools/round-47/record.py"],
"restored":     ["tools/round-47/exact.py","tools/round-47/record.py"]
$ git diff --numstat 62e33f7d HEAD -- tools/round-47/
15  1  tools/round-47/exact.py
21  4  tools/round-47/record.py
```

`gate.py`'s docstring defines `restored` as "a path the history arm saw and the blob arm finds clean".
Both files **differ**. Cause: `blob_changed()` reports a directory entry as `"path/"`, while
`freeze_state()` computes `restored = [p for p in touched if p.rstrip("/") not in {c.rstrip("/") …}]`
— a file path never equals the directory string, so every changed file under a frozen directory is
labelled restored. Receipt: `evidence/c1-freeze-A2-at-HEAD.json`. This is the same defect class the
round is about (a receipt that is false about its own state, R46-V2); it is in frozen round-46
infrastructure, so it is reported, not fixed.

### F4 — C2's `axes` correction class is invisible to the parser: the clause is vacuous in both directions

Claims clause 3: "every correction line itself re-derives … an `axes` correction must state
`<resolved>/<total>`". `record.py:50` parses corrections with

```python
CORR = re.compile(r"^- corrects (seats|window|path|rev) (\S+):\s*(.+)$")
```

`axes` is absent, and `corrects()`'s `axes` branch is unreachable (dead code). Measured, green card
plus one forged line:

| card | appended line | exit | clause 3 wants |
|---|---|---|---|
| green | `- corrects axes coverage: 999/999` | **0** (`corrections` 2, `corrections_bad []`) | 1 |
| green | `- corrects axes depth: not a fraction at all` | **0** | 1 |
| red `coverage 9/9` | `- corrects axes coverage: 1/1` (true) | **1** | 0 |
| red `coverage 9/9` | nothing | 1 | 1 |

Evidence: rows 1–2 are probes `c2-false-axes-correction` / `c2-garbage-axes-correction` (green card,
exit 0) in `MutExitCodes/receipts.jsonl`; rows 3–4 are `evidence/c2-axes-true-correction-red-atom.json`
(red row + true `1/1`, exit 1) and `evidence/c2-axes-false-correction.json` (red row + `999/999`,
exit 1 — the false line neither repairs nor is re-derived), with the exact card bytes in the matching
`.card.md` files. Controls that do bind: a false `seats` correction (`9 waves, 99 seats
total`) exits 1 with `corrections_bad` populated, and a ghost `rev` correction exits 1 — so the
class is specifically `axes`, not the re-derivation machinery. Consequence: a false axes correction
never reddens, a true one cannot repair, and the battery's three forgeries (`seats` total, `window`
emptiness, ghost atom) do not cover the class.

### F5 — four exit-2 inputs leave the 0/1/2 contract

`gate.py`'s contract line: "An unhandled exception is a defect, never a verdict: every entry point
catches it and returns 2." Measured, both counters, scratch fixtures:

| input | stdout | stderr | exit |
|---|---|---|---|
| `--json-out <root>/no/such/x.json` | empty | `FileNotFoundError: [Errno 2] …` | **1** |
| `--json-out <root>/logs` (a directory) | empty | `IsADirectoryError: [Errno 21] …` | **1** |
| `--json-out <root>/ro.json` (mode 444) | empty | `PermissionError: [Errno 13] …` | **1** |
| `import gate` fails (`tools/round-46/gate.py` absent) | empty | `ModuleNotFoundError: No module named 'gate'` | **1** |
| receipt payload not JSON-serialisable (crash in `gate.emit`) | empty | `TypeError: Object of type set is not JSON serializable` | **1** |
| `raise KeyboardInterrupt` inside `score()`/`evaluate_text()` | empty | `KeyboardInterrupt` | **−2 (SIGINT)** |

Controls on the same fixtures: `--json-out <root>/receipt.json` → 0 with a printed receipt; the
unmutated counters → 0. So an *unusable output target* or a missing dependency is reported as
**violation (1)** with **no evidence at all**, and a SIGINT is not a code at all. `main_guard` covers
`evaluate` only; everything after it, before it, and any `BaseException` escapes. The claims' counting
commands pass `--json-out <OUT>`, so this is on the graded path, not a hypothetical.

### F6 — "Causal separability" is false: C2 reads the craft section C1 lands on

Claims: "R47-C2's counter reads `SCORECARD.md` and the `.ufo/waves/round-*/` dispatch and receipt
files; it never reads the craft section." `record.py:115-137 depth_pair()` splits `SKILL.md` on
`CRAFT = "## Queue-drain craft "` and counts resolvable rule blocks — the `depth` row of
`## Owned axes` is derived from exactly the surface C1 modifies.

Fixture proof (card untouched, one craft block appended to `SKILL.md`):

```
$ python3 -I -B <FX>/tools/round-47/record.py --root <FX> --rev <rev> --no-battery
exit 1   "mismatches": [["axes","depth",{"claimed":[3,3],"derived":[4,4]}]]
```

Receipt: `evidence/c2-separability-craft-block-added.json`. In the lane this is live: `axis_pairs` at
`09a9f912` is `{'coverage': (138, 138), 'depth': (24, 24)}`, the card claims `24/24`, and the 24th
block exists only because C1 landed it. "Either lands and scores without the other" therefore holds
for C1 over C2's *other* atoms but not in the direction that matters: C2's depth atom is a function of
C1's landing, so a landing of C2 alone would need the card to keep claiming `23/23`.

### F7 — `--selftest` cannot run as documented

Both counters declare `--root/--freeze/--rev` as `required=True`, so `exact.py --selftest` and
`record.py --selftest` exit 2 with an argparse usage error and never run the liveness check. Supplying
dump values makes both pass (`exact.py` 16 cases / 0 failures, `record.py` 10 cases / 0 failures,
exit 0 — legacy-compatible `pip`-free probe `c1-selftest-with-required-args`,
`c2-selftest-with-required-args`). Semantically the exit is still "could-not-evaluate", so nothing
scores `2` as a pass; the defect is that the instrument's own check is unreachable by its documented
invocation, which is how a broken counter would go unnoticed.

---

## 4. What holds (so the L1 does not re-derive it)

* Unknown `--rev` / `--freeze`, blob-instead-of-commit refs, non-repo and missing `--root`: exit 2 with
  a named reason, on both counters, under both profiles (`--profile v2` does not weaken it).
* Non-ancestor freeze: exit 2 (`merge-base --is-ancestor`), lane-level and in a diverged fixture.
* Malformed claims: six shapes, all exit 2, and a well-formed control never returns 2.
* Unreadable `SCORECARD`: absent, invalid UTF-8, directory-at-rev, and loose-object-deleted all exit 2.
  Worktree-only unreadability is invisible (committed bytes are the graded surface) and scores 0.
* `Exception` (incl. `MemoryError`) raised inside `score()` / `evaluate_text()`: exit 2 with an
  `unhandled <Type>: …` receipt.
* Scratch-root refusal (unset, `/tmp`) : exit 2, before any repo work.
* `--json-out` outside the lane root, or over a graded/frozen path: exit 2 before evaluation.
* C2's claims' Before reproduces exactly (4 mismatches, the four named atoms); C1 at its freeze exits 1
  with `block_present 0`, and at (A6, HEAD) exits 0 with the battery `4/4/0/1/0`.

---

## 5. Restoration and frozen-byte evidence

All mutation happened on copies under `S=/fast/scratch/hyaku/kaidoku-r47/MutExitCodes`
(fixtures + `$S/mut/tools/round-47/exact.py`); no lane byte was written. Before yielding:

```
$ git -C $L status --porcelain -- plans/round-47-claims.md tools/round-47/ | wc -l
0
$ for p in plans/round-47-claims.md tools/round-47/exact.py tools/round-47/record.py; do
    printf '%s %s %s\n' "$p" "$(sha256sum $p|cut -d' ' -f1)" "$(git show HEAD:$p|sha256sum|cut -d' ' -f1)"; done
plans/round-47-claims.md  2b5d1bef4c0339325331f0197631b7580657337bde1b5311dd94365f085c6460  (worktree == HEAD)
tools/round-47/exact.py   01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5  (worktree == HEAD)
tools/round-47/record.py  abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7  (worktree == HEAD)
```

Worktree bytes equal the committed bytes for all three frozen files and `git status` is empty over the
frozen pathspec; `$S` was removed after the receipts and drivers were copied into this seat's directory.

## 6. Reproduce

`MutExitCodes/` holds the drivers (`drive.py` … `drive9.py`, `final.py`, `pickup.py`, `pickup2.py`), the raw
`receipts.jsonl` (91 rows: `probe`, `utc`, `cmd`, `exit`, `expect`, `verdict`, `stdout_sha256`,
`stdout`, `stderr`) and `evidence/` with the full untruncated receipts, the tamper patches and the
card inputs. Every fixture is built by the drivers (identity `fx@round47`, `rev-parse --show-toplevel`
asserted before the first commit); no fixture path is required to be preserved.

## 7. Sources

* `plans/round-47-claims.md` (frozen) — clause 3 of R47-C2, the frozen-path sentence, the declared-freeze
  paragraphs A1/A2, the causal-separability paragraph.
* `tools/round-47/exact.py`, `tools/round-47/record.py` (frozen), `tools/round-46/gate.py` (round-46
  infrastructure) — `freeze_state`, `blob_changed`/`restored`, `main_guard`, `emit`, `CORR`, `depth_pair`.
* `.ufo/waves/round-47/l1/scores/` — the L1's freeze choices (`c1-at-A2/A4/A5/A6`, `c1-at-R1`).
* `corpus/lessons/round-46.md` `## Routed defects` (`R46-CL2`..`CL7`, `R46-V1`..`V3`).
