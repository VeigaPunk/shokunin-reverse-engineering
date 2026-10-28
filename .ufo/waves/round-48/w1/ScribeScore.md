# ScribeScore — round-48 w1 scoped findings

Seat: ScribeScore (scribe). Assignment: draft the `## Round 48` section for
`SCORECARD.md` — base/freeze/landing, both claims before→after, counting commands,
measured revision, owned scores, learning trends, routed list; every number
receipt-backed. Deliverable: `.ufo/waves/round-48/w1/ScribeScore/score.md`.

## Behavior

Drafted the full `## Round 48` section in house format (rounds 46–47 convention),
plus a verified landing-inputs appendix: both `## Record corrections — round 48`
lines (`seats` + `quote`) executed against the real `record2` code paths and shown
to re-derive; all five grammar hazards the section must satisfy enumerated from the
oracle's own collectors. All "after" cells are marked pending — no landing exists and
none was fabricated.

## Gates exercised (exit code semantic: 0 met / 1 not met / 2 could-not-evaluate)

Counter runs from the lane root, `TMPDIR`/`HYAKU_SCRATCH` set to scratch; receipts:
`.ufo/waves/round-48/w1/ScribeScore/receipts/` (41 files, manifest.tsv + .stderr).

| command (all `python3 -I -B`, `--root .`) | exit | stdout sha256 (head) | UTC |
|---|---|---|---|
| `meanings.py --freeze dc73587a --rev dc73587a --profile v3` | 1 | `594e618c` | 18:50:15 |
| `meanings.py --freeze ac02a79f --rev ac02a79f --profile v3` | 1 | `9e99a59f` | 18:50:15 |
| `meanings.py --freeze ac02a79f --rev ac02a79f --profile v2` | 1 | `5a0c37cb` | 18:50:15 |
| `meanings.py --selftest` (A3 worktree bytes) | **1 crash** (AttributeError at census clause) | `e3b0c442` | 18:50:15 |
| `record2.py --freeze dc73587a --rev dc73587a --profile v3` | 1 | `f0bf3d66` | 18:50:15 |
| `record2.py --freeze ac02a79f --rev ac02a79f --profile v3` | 1 | `539f76ad` | 18:50:16 |
| `record2.py --freeze ac02a79f --rev ac02a79f --profile v2` | 0 | `79834524` | 18:50:21 |
| `record2.py --selftest` | 0 | `b06a8ea4` | 18:50:21 |
| `meanings.py --selftest` (A3 worktree bytes, exact `C1SelfTest` command, scratch cwd) | **1 crash** (same AttributeError) | `e3b0c442` | ~18:51 |
| `meanings.py --freeze f3a7afc4 --rev f3a7afc4 --profile v3` | 1 | `b2c036e5` | ~18:52 |
| `meanings.py --freeze f3a7afc4 --rev f3a7afc4 --profile v2` | 1 | `9d0db34b` | ~18:52 |
| `record2.py --freeze f3a7afc4 --rev f3a7afc4 --profile v3` | 1 | `bc1ccda7` | ~18:52 |
| `record2.py --freeze f3a7afc4 --rev f3a7afc4 --profile v2` | 0 | `5b71be70` | ~18:52 |
| `meanings.py --selftest` (A4 worktree bytes) | 0 `cases=18 failures=0` | `30c163be` | ~18:52 |
| `meanings.py --freeze 0f06251b --rev 0f06251b --profile v3` | 1 | `9c5048d2` | 18:53:53 |
| `meanings.py --freeze 0f06251b --rev 0f06251b --profile v2` | 1 | `8ee187a8` | 18:53:53 |
| `record2.py --freeze 0f06251b --rev 0f06251b --profile v3` | 1 | `1055fb82` | 18:53:54 |
| `record2.py --freeze 0f06251b --rev 0f06251b --profile v2` | 0 | `2f18bcc6` | 18:53:58 |

Not run: battery executions at a landing (no landing exists); `command A` axis counts
(derived from oracle/record2 receipts instead); any mutation of frozen bytes.

## Touched surfaces

Created: `.ufo/waves/round-48/w1/ScribeScore.md`, `.../w1/ScribeScore/score.md`,
`.../w1/ScribeScore/receipts/` (41 files), scratch `$S`. No frozen, product, sibling,
state, watchdog or fleet file was written; no git/jj mutation anywhere. Read-only git:
`log`, `show`, `diff`, `ls-tree`, `rev-parse`, `status --porcelain`.

## Findings (scoped, receipt-backed)

1. **The declared freeze moved twice mid-wave.** Prompt/dispatch: `dc73587a` (A1).
   Claims file at report time: A4 `0f06251b` ("the commit that carries this
   paragraph"), HEAD `663f30ee`. Frozen-path integrity since A4 verified: `git log
   --name-status 0f06251b..HEAD -- tools/round-48 plans/round-48-claims.md` empty.
   Draft names the five-commit disclosed series `7fe11332 → 0f06251b` and flags the
   dispatch/claims divergence to the L1 (CritClaims reached the same conclusion
   when the lag was two amendments).
2. **C1 before (A4, this seat):** exit 1, `marker_occurrences 0`, `block_present 0`,
   `rule_blocks 24`, `frozen_path_changed []`, `touched 0`, battery skipped —
   identical clause shape to committed control `ctl-c1-0-do-nothing.json` (A1).
   v2 also exits 1 (the block itself is a v2 clause).
3. **C2 before (A4, this seat):** exit 1 with oracle green (`atoms 44`,
   `mismatches []`, `met_target true` — matching committed `l1/scores/
   probe-record47.json`), `axis_score_cells` coverage 138/138→(9.72,10.0) and depth
   24/24→(10.0,10.0), `corrections 0`, three failing clauses: no round-47 seat
   atom/correction, no round-48 corrections section, `exempted 2` unbacked.
   `--profile v2` exits 0 — the hole being closed.
4. **A3-era selftest crash is real and now closed:** at A3 bytes `meanings.py
   --selftest` raised `AttributeError: 'list' object has no attribute 'get'` at the
   census clause (fixture stub returned a list while the clause called
   `derived.get("paths")`); at A4 bytes it exits 0 `cases=18 failures=0`. C1SelfTest's
   earlier `cases=16` run was on pre-A3 bytes (16-case file at `7fe11332..ac02a79f`).
   Historical only — the operative bytes are green.
5. **`## Record corrections — round 48` lines verified end-to-end (scratch, in-memory
   at `0f06251b`, not a counter pass):** `corrects seats round-47: 1 wave, 75 seats
   total` → oracle `corrects()` True (dispatch [75]); `corrects quote round-47:
   exempted 1` → `_quote_correction()` True (round-47 section quotes `exempted 2`;
   the cited `c2-at-A7.json` `exempted` list has length 1). Negative controls:
   `exempted 0` → unbacked; `exempted 2` → "already quotes that value";
   `2 waves, 75 seats total` → claimed≠derived.
6. **`Waves: 75 + 0 = 75 seats.` is the only seat-prose form that derives** for a
   one-wave round: `Wave 1: 75 seats` matches neither `SEATS_SUM` nor `SEATS_PAIR`
   (round-47 section carries a "waves" sentence with no collectible seat atom — the
   exact reason the floor fails there). Any `w2-dispatch.json` addition changes the
   derived total; re-derive at the measured revision.
7. **Commit-ordering dependency (fresh finding):** `.ufo/waves/round-48/` is entirely
   untracked at HEAD `663f30ee` (`git status --porcelain` → `?? .ufo/waves/round-48/`;
   `git ls-tree 0f06251b .ufo/waves/round-48/` empty). `path` atoms, the seats
   correction's `w1-dispatch.json`, and every `receipts_at` binding fail at a measured
   revision unless the evidence tree is committed first. Round-47's pattern
   (evidence commits land before the final tip) applies here.
8. **Claim-id floor is zero-tolerant to cross-section literals:** claim ids must be
   unique across the last two sections; the round-48 draft must not contain a literal
   `R47-C\d` or `R46-C\d` (routed ids like `R46-CL7`, `R47-CL10` are `CL`-class and
   safe — `R\d\d-C\d` only).
9. **QUOTE key collisions:** `atoms|exempted|corrections|mismatches N` anywhere in
   the section must equal a cited receipt's cell or a `quote` correction. The draft
   keeps all such numbers in receipt-bound form and leaves after-values as fills.
10. **Claims file names a control that does not exist:** `ctl-c1-1-v2-profile.json`
    is listed under Controls; the controls dir has `ctl-c1-0`, `ctl-c1-a3-simulation`,
    `ctl-c2-0`, `ctl-c2-1`, `ctl-c2-a1-before`, `probe-c2-{v2,v3}` only. C1V2's report
    confirms it cannot be produced until a block exists.

## Out of scope / limits

- No landing, no after-measurements; battery runs are structurally impossible pre-landing
  (both counters skip the battery on any failing clause — C2Battery's gating note).
- Scratch correction checks used `importlib` on worktree bytes (== HEAD `663f30ee` ==
  A4 frozen bytes by sha256 `00f768c5…` for `meanings.py`) with a `files()` shim over
  `git show <rev>:path`; no fixture repo needed (no commit anywhere was required).
- `corpus/SOURCES.md` and `.ufo/waves/round-4[567]/` carry pre-existing user
  modifications, untouched by this seat.
- Installs: none. `disk-guard.sh status` observed 376K in this seat's scratch before the pass.
- Scratch `/fast/scratch/hyaku/kaidoku-r48/ScribeScore` removed after receipt copy.
