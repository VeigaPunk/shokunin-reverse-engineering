# ConnAxes — cross-axis defect scan, round 48 w1

Seat: `ConnAxes`. Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the
lane tree; all mutation work done in a scratch clone `$S/clone`. Receipts:
`.ufo/waves/round-48/w1/ConnAxes/receipts/`. No installs (pacman paused; nothing needed).
Executed counter runs: `meanings.py`/`record2.py` at `ac02a79f` (A2) and `0f06251b` (A4),
tip `663f30ee`.

## 0. Freeze is STALE in the prompt — declared freeze is now A4 `0f06251b`

The prompt names `dc73587a` (A1); the claims file names the freeze as "the commit that
carries this paragraph" per amendment, and A3 `f3a7afc4` + A4 `0f06251b` (both stamped
"declared freeze", committed 15:50/15:52, before this report's first counter run) are
already in `git log`. `git log -1 -- plans/round-48-claims.md` = `0f06251b`. Everything
below is measured against A4 bytes unless marked otherwise; where A2 semantics differ I say
so. A4 hardens the exit-0 classifier (NEGATED guard), `ROW_START` indented-row parsing, and
A3 fixes `derived.get("paths")`. Two of my findings (battery starvation, gate.py hole)
survive A4 unchanged; one finding (my own reading of the old `registry_rows` skip) was fixed
by A4 itself — recorded as evidence the scan works.

## 1. The six routed defects → closing clause → status

| defect | closes via | status | residuals / scope of the residual |
|---|---|---|---|
| **R46-CL7** registry verdict maps bind digits 0/1/2, not meanings | C1 clause 8 (`meaning_classes` per segment + census-equality) | CLOSED for the registry section | `tools/round-46/registry.py` still runs digit/thin checks — deliberately superseded, untouched. Any verdict-bearing tool the census rule cannot *name* is outside the clause entirely (finding 4): registry rows = census paths and `meaning_rows_failed 0` while 8 real tools carry no examined verdict map. |
| **R47-CL10** counters grade form, never completeness | C1 clause 3 (EXPECTED_ARM per id) + clause 9 battery; C2 clause 2 floor + clause 6 battery | CLOSED (battery kill-demonstration pending genuine green — see finding 1, which makes C1's battery unreachable for a different reason) | `tools/round-47/record.py` itself untouched — still consistency-only by design (it is the v2 port's hole). The floor binds the **last two** round sections: rounds ≤46's sections remain floorless forever. |
| **R47-CL1** counters execute own code from the worktree | oracle + census tool exec'd from `--rev` bytes (record2.py:62-73, meanings.py:296-304); `interpreter_sha256` (C1 clause 6) | **OPEN** — finding 2 is the kill demonstration | Every pre-48 counter still executes from the worktree (class persists fleet-wide). Worse: both counters `import gate` from the worktree and `gate.py` is NOT in the round-48 frozen set (`frozen_derived` = `plans/round-48-claims.md`, `tools/round-48/` only) — a patched `gate.py` is refused by nothing. The interpreter pin grades rev-bytes while worktree bytes execute — the pin does not close it, it widens it. |
| **R47-CL2** `axes` atom binds leading fraction, not the 0–10 score cell | C2 clause 5 (`axis_scores`, A1's `cell[0]` fix) | CLOSED for `coverage`/`depth` | The `calibration` row's score cell is unbound — `AXIS_SCORE` regexes only `(coverage|depth)`. Claimed scope literally covers the two rows, so the clause matches its text; the *class* persists on the third row. Multi-fraction cells bind the FIRST `n/d` only (same first-fraction shape as the defect). |
| **R47-CL13** quoted receipt numbers never bound to their receipt | C2 clause 4 (`QUOTE` binding + `quote` correction class) | CLOSED for `key N` prose inside the last two sections | Inverted phrasing `N key` is never bound — **exactly the wording of the original misquote** ("over 50 atoms" while `exempted 2`/`atoms 50` bind; M47-9's own phrasing survives the fix). Verified: `QUOTE.findall("over 50 atoms, exempted 2")` → `[('exempted','2')]`. Sections older than the last two are out of scope. Receipts must live under `l1/scores/*.json` (`RECEIPT` regex) — a quote citing a control receipt is declared unbacked (harder-than-needed semantics, not a forgery hole). |
| **R47-CL14** `axes` correction silently inert | C2 clause 3 (CORR grammar gains `axes|quote`; axes verified inline, quote by `_quote_correction`) | CLOSED for `axes`/`quote` | Lines matching no class are still silently skipped (`corrections_section` `continue`s). Untouched `record.py` carries a DEAD `axes` branch at line 292 referencing an undefined `atom` — would `NameError` if grammar admitted it. Older `## Record corrections — round <N>` sections are never re-parsed (harder scope, not a hole). |

## 2. Kill finding — R47-CL1 is open: the worktree helper decides refusal AND bytes

`tools/round-48/{meanings,record2}.py` exec the oracle/census-tool from `--rev` bytes but
`import gate` from the worktree, and `tools/round-46/gate.py` is not in the round-48 frozen
set. In `$S/clone` I appended an ~8-line stub to `gate.py`:

```python
_ORIG_SHOW = show
def show(root, rev, path):
    if path == "SKILL.md" and os.path.exists(os.path.join(root, "_fake_skill.txt")):
        return open(os.path.join(root, "_fake_skill.txt")).read()
    return _ORIG_SHOW(root, rev, path)
```

- `git status` shows `M tools/round-46/gate.py`; `gate.dirty(paths)` sees only the round-48
  pathspecs → `dirty []` → `freeze_state` returns 0.
- With the stub serving a forged SKILL.md, `meanings.py --freeze ac02a79f --rev ac02a79f`
  GRADES the forged artefact instead of the committed bytes (`c1-stubbed-gate.json`,
  exit 1 with failing clauses — the artefact reached `score()`, which is the hole).
- Second stub — `freeze_state` returning a clean receipt — over a commit that tampered
  `tools/round-48/meanings.py` itself (`d581887d` in the clone): real gate exits
  `frozen_path_changed` correctly; stubbed gate proceeds to grading (`c1-stub-freezelie.json`,
  exit 1, `fpc []`). Refusal → grading flip, one appended stub, nothing refused it.
- The pin does not bind the executed bytes: `interpreter_sha256` hashes `files(SELF)` =
  `--rev` bytes; `score()` runs worktree code. During a drafting window the artefact can only
  ever carry the *committed* hash — the executed code is by construction different from the
  pinned code whenever the next amendment exists in the tree.

## 3. Kill finding — R48-C1 is unsatisfiable: `run_battery` starves its own census check

`evaluate()` calls `run_battery` only when the artefact is already green; inside
`run_battery`, `score()` is re-run against `_fixture_files`, a map containing: the round-48
claims file, `SELF`, census json, `census2.py`, the two mandatory refs, SKILL.md, and
**only the paths cited inside the marked block** (meanings.py:468-489).

`census_rederive` then runs `census_text(read=files.get)`: `present` = paths *loadable in
the fixture*. A loadable path must be either unconditionally loaded (only `tools/round-48/*`)
or cited in the block — and `check_refs` FORBIDS any citation outside
`corpus/lessons/ | corpus/knowledge/ | plans/ | tools/round-48/` (clause 7 / `ALLOW`).
The 40 census paths under `tools/round-4[1-7]/` therefore can never be present in the
fixture ⇒ `derived.paths` ⊆ {the round-48 tools} ≠ the committed 42 ⇒
`census_rederived_equal` false ⇒ `genuine_green` is `0` for **every** artefact ⇒ clause 9's
`genuine_green 1` is unreachable ⇒ **R48-C1 cannot exit 0 at the declared freeze**.

Measured (real `score()` + real `_fixture_files` semantics at A2; the narrowing is
unchanged at A4): a clause-minimal conforming SKILL scores `exit 0` full-scope but `exit 1`
(`committed census2.json does not equal a fresh derivation`) battery-scope
(`GENUINE-IN-BATTERY`); citing all 8 claims files rescues it *in emulation*, but the real
fixture can still never hold the 40 tool paths, so the rescue does not exist in the real
code path — citing them fails clause 7 (`c1-stub-rescue.json`: `unresolved citations: 40`).

Contrast: `record2.run_battery` passes full `files` (rev-bytes lambda) — the starvation is
C1-only, an inconsistency between the two frozen counters. The same class as M47-1 (a
clause no truthful artefact can satisfy), one round later, and it will only be *visible* at
landing time as `battery genuine_green 0 != 1` on a perfectly good block.

## 4. Census-rule blind spots — the registry can be complete against an incomplete census

`census2.py`'s `TOOL` regex sees only fully-spelled `tools/round-4X/<name>.{py,sh}` strings.
On disk vs census, 8 instruments are unregistered:

- **Bare-name references** (invisible to the regex): `tools/round-42/c1-extra.py` (named
  `c1-extra.py` in round-42 claims), `round-43/{build-copies-r43.py, c2-controls-r43.py,
  receipt-wrap.py}` (named only inside `tools/round-43/{…}` brace lists — the regex stops
  at `{`).
- **Directory-frozen, never named**: `tools/round-44/{c1-controls.py, c1-oracle.py,
  c1-run.py, c2-controls.py}` — the round-44 claims file freezes `tools/round-44/` as a
  directory and names none of them.
- **Self-reference impossible**: `tools/round-48/census2.py` — named nowhere in the claims
  file; the registry cannot ever contain its own derivation tool.

Clause 8 binds registry rows to the census path set and the census to a re-derivation of
its own rule — both hold while 8 instruments carry no row and no verdict-map examination.
This is the R47-CL10 class (completeness) moved one layer down: the census measures
*naming*, not *presence*.

## 5. Smaller verified seams (each ≤ a clause's own text)

- **Clause 7 vs code**: `check_refs` exempts a bare `tools/round-48/meanings.py` citation
  from the line-selector requirement (`name == SELF: continue` at meanings.py:268-269,
  before the selector check); the claim text says "each with a line selector". One
  selector-less citation is admissible.
- **Battery count inflation**: in `run_battery`, a no-op mutation increments
  `forgeries_total` AND `v2_green` without any scoring (meanings.py:497-504) — the `4/4/0/1`
  tuple does not require four scored forgeries. Currently unused (all four mutate).
- **Directory citation resolves**: `git show rev:plans/` returns a tree listing, so a
  `plans/:N` citation "resolves" with a line count (the R47-CL15 crash becomes a quiet
  accept in `check_refs` — the fixture-builder crash guard never sees it).
- **A4's own prose overstates**: A4 says the row parser "fails closed on a row that does
  not have seven cells" — but `ROW_START = ^\|\s*\`` still silently *skips* rows whose cell
  lacks a backtick; only backtick-led rows are 7-cell-checked. Narrower than advertised.
- **Owned-axes `calibration` row** unbound (residual noted in the table).

## 6. Contradictions stated, not smoothed

- Prompt freeze `dc73587a` vs file-derived freeze `0f06251b` — the file is the rule; the
  prompt is two amendments behind. L1 should confirm every seat is measuring `0f06251b`.
- Claimed "registry = census" vs 8 unregistered on-disk instruments — the equality is
  between the table and a *derivation rule*, not between the table and the tool set.
- "Battery discriminates" vs `genuine_green` unreachable — clause 9's witness cannot exist
  in the real code path.
- `ctl-c1-a3-simulation.json` (`exit 0`, `census_rederived_equal true`) was produced by
  `score()` outside `run_battery`'s narrowing — a simulation receipt that cannot reproduce
  under `evaluate()`.

## 7. The one bounded connector move (advisory)

The cheapest single move that repairs three axes at once — **swap the battery's file map
for the full reader in `meanings.run_battery`**: `files = lambda p: gate.show(root, rev, p)`
(the `record2.run_battery` shape, already frozen as precedent). It costs one line in the
frozen tool (an A5 amendment), makes `genuine_green` reachable (depth: clause 9 becomes
satisfiable), keeps every existing kill (the forgeries still fail under v3 on the *same*
clauses — they fail in score(), before the fixture question), and converts the current
unreachable-clause trap into an observable red-before at the first landing. The
alternative — cite all 42 paths — is forbidden by clause 7, so there is no landing-side
workaround. Risks: one more amendment in the series (R47-CL5/CL8 cost already paid four
times this round); the starved fixture also covers path-citation checks, so re-check that
`_fixture_files`' narrowed map isn't load-bearing for some other clause — my sweep found
only the census check depends on it.

## 8. What I ran (exit codes, receipts under `receipts/`)

| command (lane, read-only) | exit |
|---|---|
| `meanings.py --freeze ac02a79f --rev ac02a79f` | 1 (marker absent — correct red-before; battery skipped) |
| `meanings.py --freeze 0f06251b --rev 663f30ee` | 1 (marker absent; `c1-tip-A4.json`) |
| `record2.py --freeze 0f06251b --rev 663f30ee` | 1 (`round-47 seats`, `no round-48 corrections`, `1 unbacked quote`; `c2-tip-A4.json`) |
| `census2.py --rev ac02a79f` re-derivation vs committed | equal, 42/42 |
| clone: `meanings.py` + stub `gate.show` → grades forged SKILL | exit 1 reaching `score()` (`c1-stubbed-gate.json`) |
| clone: committed `tools/round-48/meanings.py` tamper, real gate | exit 2 `frozen_path_changed` (control) |
| clone: same rev, stub `gate.freeze_state` lying clean | refusal gone, grading proceeds (`c1-stub-freezelie.json`) |
| micro: `QUOTE` / `TOOL` / `check_refs` / dir-citation | as reported inline |

Not run (said plainly): the C1/C2 forgery batteries end-to-end at tip (both counters exit 1
at tip on structural clauses, so batteries are skipped by construction); `record2`'s
battery exercised only statically — its `files` is un-narrowed, so it does not carry the
C1 trap.

Scratch `/fast/scratch/hyaku/kaidoku-r48/ConnAxes` holds the clone + forge artefacts;
receipts copied above before cleanup. One accidental `git stash`/`stash pop` executed
inside `$S/clone` only — the lane was never touched.
