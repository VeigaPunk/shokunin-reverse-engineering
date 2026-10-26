# R36W2ExecC2Final — re-run and falsify R36-C2 at four revisions

Seat: R36W2ExecC2Final (leaf, wave 2). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope: **R36-C2 only** (C1 is another seat). All work read-only on the lane; every mutation probe ran in a
scratch clone under `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ExecC2Final` (removed at exit).

## Verdict

**Reproduced, not falsified.** The frozen `c2-counter.py` yields exactly the claimed numbers at all four
revisions (`3 → 0 → 0 → 0` mismatches), its `--selftest` is 13/13 as frozen, and its bytes are identical to
the freeze blob at every revision where the file exists. A second, independently written non-counter
re-derivation (every-occurrence enumeration, no key shadowing) agrees with the counter field-for-field at
all four revisions. Two instrument blind spots that wave 1 named are **proved live at the tip state** in a
scratch clone, but the tip state contains no duplicate rows/boxes and no second-table rows, so neither
blind spot is exploited by the landed surfaces. One evidence-retention gap is reported (F1).

## 1. Counter byte identity at each revision

```
$ for r in 790561d4… cab59f22… d2e46ef5… ffc81341… 01a44dbf…; do git show "$r":tools/round-36/c2-counter.py | sha256sum; done
790561d4e3aca732a434081aa9573ec2fa5fd7d0  f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f
cab59f221fe19726b5692bfa4d9a9679e96b8a73  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855   <- absent (empty stdout)
d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be  f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f
ffc813417d3bceeeb7b028b12ce0be8a5dc33d95  f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f
01a44dbf45913a1bdcabbbfb85b7bb9d232cb930  f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f
worktree tools/round-36/c2-counter.py      f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f
$ git diff --stat HEAD -- tools/round-36/c2-counter.py   # empty
$ git status --porcelain | grep -c 'tools/round-36'      # 0
```

- Equal to the freeze bytes `f079aff1…` at the freeze commit and at all three measured revisions.
- **Base `cab59f22` is the exception and cannot be otherwise**: the counter is introduced by the freeze
  commit, whose parent is `cab59f22` (`git rev-list --parents -n 1 790561d4` →
  `790561d4… cab59f22…`). `git cat-file -e cab59f22:tools/round-36/c2-counter.py` exits 128. So the base
  measurement necessarily executes the freeze-identical blob against base **git objects**; same finding as
  wave-1 `R36ExecRecountC2.md:17`. This is a property of the freeze, not a lane defect.

## 2. Four counter runs (frozen command, pinned hashes)

```
$ python3 -I -B tools/round-36/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev <REV> --base cab59f221fe19726b5692bfa4d9a9679e96b8a73 --json-out "$S/c2-at-<REV>.json"
```

| revision | stdout | exit |
|---|---|---|
| `cab59f221fe19726b5692bfa4d9a9679e96b8a73` | `{"assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [122, 122], "stated": [116, 116]}], "guards_ok": false, "met_target": false, "mismatches": 3, "revision": "cab59f221fe19726b5692bfa4d9a9679e96b8a73", "unresolved": [["cap:pre-registered two-lane live battery on REA 6.5.0", "receipts-B/"], ["shonen:No cross-domain bleed (PROVINCE.md still accurate)", "ScoutSkillPlacement.md"]]}` | **1** |
| `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` | `{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be", "unresolved": []}` | **0** |
| `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` | `{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "ffc813417d3bceeeb7b028b12ce0be8a5dc33d95", "unresolved": []}` | **0** |
| `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` | `{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0, "revision": "01a44dbf45913a1bdcabbbfb85b7bb9d232cb930", "unresolved": []}` | **0** |

Receipt detail (all four, from the `--json-out` files, identical shape):

| field | base | d2e46ef5 | ffc81341 | tip 01a44dbf |
|---|---|---|---|---|
| `pointers` | 34 | 36 | 38 | 41 |
| `guards.base_pointers` | 34 | 34 | 34 | 34 |
| `guards.missing_units` | `[]` | `[]` | `[]` | `[]` |
| `guards.unrepaired` | both bad pointers | `[]` | `[]` | `[]` |
| `observed.command_a` mapped/files | 122/122 (unmapped `[]`, dangling verification below) | 122/122 | 124/124 | 124/124 |
| `observed.command_a` resolved_rules/rule_blocks | 17/17 | 17/17 | 17/17 | 17/17 |
| `observed.command_b` | `[9, 9]` | `[9, 9]` | `[9, 9]` | `[9, 9]` |
| `observed.craft_range` | `[81, 314]` | `[81, 314]` | `[81, 314]` | `[81, 314]` |
| `observed.adjacent_range` | `[97, 118]` | `[97, 118]` | `[97, 125]` | `[97, 125]` |
| `mismatches` / `guards_ok` / `met_target` | 3 / false / false | 0 / true / true | 0 / true / true | 0 / true / true |
| exit | 1 | 0 | 0 | 0 |

The base values match the frozen claim's before-state exactly: unresolved `receipts-B/` (capability row
"pre-registered two-lane live battery on REA 6.5.0"), unresolved `ScoutSkillPlacement.md` (SHONEN box 4),
and `116/116` stated vs `[122, 122]` observed.

## 3. Selftest (frozen command), run twice

```
$ python3 -I -B tools/round-36/c2-counter.py --selftest        # HYAKU_SCRATCH/TMPDIR inside seat scratch
{"selftest": "c2-counter", "cases": 13, "green_ok": 1, "red_ok": 12, "failures": []}
exit=0
{"selftest": "c2-counter", "cases": 13, "green_ok": 1, "red_ok": 12, "failures": []}
exit=0
```

13 cases = 1 green + the 12 red cases the frozen plan names (do-nothing, junk count, deleted count, deleted
pointer, substitution by another document, box removed, craft range off by one, Adjacent range wrong, range
beyond file, new unresolved pointer, wrong calibration count, wrong SHONEN count). Deterministic across two
runs; the selftest fixture directory (`$HYAKU_SCRATCH/kaidoku-r36/`) is left empty, and the fixtures assert
their own `rev-parse --show-toplevel` before committing (`c2-counter.py:307-312`).

## 4. Byte-level reproduction of the retained lane receipts

Both C2 receipts the lane retains are reproduced by my re-runs **identically except the `argv` path
fields** (`--root .` / `--json-out` differ; every measured field, including `guards`, `observed`,
`pointers`, `mismatches`, `predicate` is equal):

- `.ufo/waves/round-36/c2/after-at-d2e46ef5.json` vs my `c2-at-d2e46ef5….json` → equal (excluding `argv`).
- `.ufo/waves/round-36/after/c2-at-ffc81341.json` vs my `c2-at-ffc81341….json` → equal (excluding `argv`).
- `.ufo/waves/round-36/controls/ctl-c2-0-do-nothing.json` vs my `c2-at-cab59f22….json` → equal (excluding
  `argv`); its `.out` line is byte-identical to my stdout plus `ctl-c2-0-do-nothing exit=1`.

The other three C2 controls (`.ufo/waves/round-36/controls/ctl-c2-{1,2,3}.json`) are receipts over scratch
fixture roots that no longer exist (`/fast/scratch/hyaku/kaidoku-r36/L1/ctl.*` in their `argv`), so they can
be read but not re-executed byte-for-byte. Their recorded outcomes are the ones the frozen plan requires:
junk count `mismatches 3`, delete-bad-pointers and substitute-other-document `mismatches 0` but
`guards_ok false`, all `met_target false` with `.out` exit 1.

## 5. Independent non-counter re-derivation (the stricter check the lesson promises for wave 2)

I wrote a separate checker (`$S/indep.py`, ~180 lines, scratch only, reads `git cat-file` blobs directly; it
does not import, exec, or read `c2-counter.py`) that differs from the counter in four ways that matter:

1. **Every occurrence, not first-per-key.** Axis rows, capability rows and SHONEN boxes are collected as a
   list; the occurrence count per key is reported (`duplicate_units`), and every occurrence's pointers are
   checked. The counter stores `units[key] = text`, so a later occurrence silently replaces an earlier one.
2. **`## Capabilities` scanned to the section end**, not to the first non-table line.
3. **Per-unit pointer identity** base→rev (path-level), not only a population count.
4. **Strict guard**: `guards_ok` additionally requires `duplicate_units == {}`.

Results (exit codes from the checker itself):

| revision | exit | mismatches | guards_ok | met_target | pointers | unit counts (axis/cap/shonen) | duplicate_units | unresolved |
|---|---|---|---|---|---|---|---|---|
| `cab59f22` | 1 | 3 | false | false | 34 | 3/8/4 | `{}` | `[receipts-B/ (line 619), ScoutSkillPlacement.md (line 11)]` |
| `d2e46ef5` | 0 | 0 | true | true | 36 | 3/8/4 | `{}` | `[]` |
| `ffc81341` | 0 | 0 | true | true | 38 | 3/8/4 | `{}` | `[]` |
| `01a44dbf` | 0 | 0 | true | true | 41 | 3/**9**/4 | `{}` | `[]` |

Field-for-field agreement with the counter at all four revisions, including the pointer totals
34/36/38/41 and every `assertion_mismatches` entry. Additional facts the counter does not print:

- **Command A is clean beyond the count**: at all four revisions `unmapped == []` and `dangling == []`, so the
  equality is not produced by an off-by-one pair of unrelated names. Rule-block citations resolve
  individually (`rule_bad == []`), 17/17 at every measured revision.
- **No unit was removed or renamed away**: at the tip, capability units grow 8 → 9 (the round-36 sasquatch
  row lands at `01a44dbf`, not at `ffc81341`), axis stays 3, SHONEN stays 4, `missing_units == []`.
- **Base-unresolved repairs are to the same documents, and those documents existed at the base**:
  `.ufo/waves/luna-round-6/receipts-B/` is present in `git ls-tree -r cab59f22`
  (`…/receipts-B/MANIFEST.txt`, `leg-1.md` … `leg-10.md`, `census-laneB-final.txt`), and
  `.ufo/waves/round-30/w1/ScoutSkillPlacement.md` is present at the base too. The repair is path
  qualification, not substitution; `ctl-c2-3`'s class (substitute another resolving document) is not what
  landed.
- **Pointer identity base→tip, per unit**: exactly 2 base pointer paths are absent at the tip — the two that
  were unresolved at the base — and each is replaced inside the same unit by the path-qualified form
  (`receipts-B/` → `.ufo/waves/luna-round-6/receipts-B/`;
  `ScoutSkillPlacement.md` → `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`). 9 pointer paths are new
  (4 in the coverage row: the two round-36 entries, `tools/round-36/c2-counter.py`, `plans/round-36-claims.md`;
  1 in the repaired capability row; 3 in the new round-36 capability row; 1 in the repaired SHONEN box). No
  resolving pointer was traded for a resolving pointer elsewhere.
- **Historical numbers stated inside the rows are true at the revisions they cite** (outside the frozen
  four-count assertion, so this is extra): command A at `c369242f` = 116/116, 17/17; at `ebe2cb4a` =
  109/109, 17/17; command B = 9/9 at both; 122/122 at `cab59f22`.
- **SHONEN box 4's prose sub-ranges hold at the tip** (not part of the three frozen ranges, checked because
  the box asserts them): `PROVINCE.md:97-125` is the `## Adjacent` range with last non-blank line 125;
  safety refusal at `:116-118` is the "Quality/safety verdicts on findings" bullet (lines 116-118);
  the dated tooling bullet is `:119-125`; the installer line is `:110-115` ("Installing engines … never runs
  the installer"); `:8-14` and `:24` do carry the version statements (line 24: "Installed shared REA skill is
  v42/207 tools"). `:8-14` ends on a blank line 14 — pedantic, correct in substance, and outside the frozen
  three.

## 6. Mutation probes against the tip state (scratch clone, not the lane)

Method: `git clone --no-hardlinks . "$S/lane"` (read-only on the lane), `user.name/email` set to a fixture,
each probe a fresh `checkout -B <name> 01a44dbf…` + one-line surface edit + `git commit`, then the frozen
counter run as `--rev HEAD --base cab59f22…` **and** my independent checker on the same commit.

| probe | mutation at tip | counter | independent checker | reading |
|---|---|---|---|---|
| P1 | insert a stale `| coverage | … 116/116 … `corpus/missing-doc.md`` row **above** the valid coverage row | **exit 0, `met_target true`** | exit 1 — `duplicate_units {'axis:coverage': [23, 24]}`, unresolved `corpus/missing-doc.md` at line 23 | M36-3 shadowing **is still live at the tip state**: a stale duplicate is invisible when a later valid duplicate of the same first cell exists |
| P2 | insert a stale duplicate of SHONEN box 1 (title-identical) with `9/9 rule blocks` and `nope/missing.md` | **exit 0, `met_target true`** | exit 1 — `duplicate_units` on the box key, unresolved `nope/missing.md` at line 5 | same class on the SHONEN surface |
| P3 | add a **new** capability row with an unresolved pointer `nope/missing.md` | **exit 1**, `unresolved [["cap:injected capability", "nope/missing.md"]]` | exit 1 | sensitivity control: new rows on a parsed table are covered, so the tip's new round-36 capability row really is measured |
| P4b | add a row **after** the prose note inside `## Capabilities` (line 630, before `## Saturation`) | **exit 0, `met_target true`** | exit 1 (after making the section scan exhaustive) | the counter stops at the first non-table line (`c2-counter.py:71-78`), so a second table in that section is invisible; the tip has no such row |
| — | tip unmodified (`01a44dbf`) | exit 0 | exit 0, `duplicate_units {}` | **neither blind spot is exercised by the landed state** |

P4c note on my own instrument: my first `## Capabilities` parse reproduced the counter's stop-at-first-blank
bug and therefore scored P4b green; I fixed it (scan to section end) and P4b then correctly fails. The
corrected exhaustive parse changes **nothing** at `cab59f22`, `d2e46ef5`, `ffc81341`, `01a44dbf` (unit counts
3/8/4, 3/8/4, 3/8/4, 3/9/4; mismatch counts unchanged), because the tip has exactly one table there.

## 7. Findings (disagreements / gaps), with evidence

- **F1 — the plan's "then again at the final tip" measurement is not retained as a receipt.**
  `plans/round-36-claims.md` §Separability: C2 "is measured at its own landing commit … then again at the
  final tip". Retained C2 receipts stop at `ffc81341`:
  `git ls-tree -r 01a44dbf -- .ufo/waves/round-36/c2` → `after-at-d2e46ef5.json` only;
  `.ufo/waves/round-36/after/` → `c1-at-ffc81341.json`, `c2-at-ffc81341.json`. The tip **did** move a
  predicate surface (capability row 8 → 9, coverage row restated 122/122 → 124/124, Adjacent range 97-118 →
  97-125), and `SCORECARD.md` `## Round 36` itself lists `measured at d2e46ef5, ffc81341` — so no committed
  artifact records the tip measurement the frozen plan promises. Severity: **evidence gap, not a false
  claim** — my pinned re-run at `01a44dbf` (exit 0, `mismatches 0`, `pointers 41`, receipt pasted in §2)
  supplies the missing measurement and it is green. Routable to L1 as a retained-receipt item for round 37.
- **F2 — M36-3's shadow-row class survives at the tip state** (P1/P2). The lesson's claim that the verdict
  "also rests on a stricter non-counter re-derivation in wave 2" is now satisfied by §5, and §5 shows the
  tip document contains **no** duplicate axis row, capability row or box, so the class is an instrument
  limit only. QUALITY 77 stands as written; nothing in the landed data is wrong.
- **F3 — the counter cannot see a second table in `## Capabilities`** (P4b, `c2-counter.py:82-89`). The
  frozen predicate says "the SCORECARD `## Capabilities` **table** rows"; whether a second table in that
  section counts is a predicate-scope question I do not decide. The tip has one table there (`SCORECARD.md`
  tip lines 619-627), so the measure is complete for the landed state.
- **F4 — the base "run" cannot use a counter blob present at the base** (§1): the freeze commit's parent is
  the base, so `cab59f22:tools/round-36/c2-counter.py` is absent (exit 128) and the base number is the
  freeze blob against base objects. Consistent with the frozen plan's own counting command, and already
  recorded by wave 1; restated because my seat's byte-identity clause names the base.
- **F5 — minor, prose only**: SHONEN box 4's `PROVINCE.md:8-14` includes the trailing blank line 14 (versions
  are at 8-12). It resolves, and it is not one of the three frozen ranges; I am not treating it as a
  mismatch and it is not a defect worth a ledger row.
- **F6 — no disagreement found on the claim itself.** The before-state is exactly the 3 mismatches the claim
  states; the target is met at the landing commit, at the C1 landing and at the tip; the two base-unresolved
  pointers are repaired by pointers to the same documents, which existed at the base; no unit removed; no
  fewer pointers (34 → 41); the four stated counts and three stated ranges equal observed values at every
  measured revision. I could not falsify the C2 landing.

## 8. Risks / limits of this seat

- I did not re-run C1 (`c1-counter.py`, carriers, REA receipts) — out of this seat's assignment; the C1
  verdict's provenance rests on the wave-1 reproductions, not on this report.
- I did not execute the three C2 control fixtures (`ctl-c2-1..3`) because their scratch roots are gone; I
  verified their recorded outcomes and reproduced `ctl-c2-0` byte-for-byte.
- The independent checker is mine, not frozen; it is stricter (duplicates, per-unit pointer identity,
  exhaustive capability scan) and agrees with the counter everywhere it is comparable. Its source lived only
  in scratch and is removed with it; the algorithm is described in §5 so the L1 can re-derive it if wanted.
- No tool was installed or upgraded (no pacman transaction, no `uv`, no REA invocation); `npx`/REA were not
  needed for C2. No VCS mutation in the lane; the only `git` writes were `init`-free clones/commits inside
  `$S/lane`.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ExecC2Final` removed on exit; no file under `/tmp`.

## 9. Files changed by this seat

- `.ufo/waves/round-36/w2/R36W2ExecC2Final.md` (this report). Nothing else in the lane.
